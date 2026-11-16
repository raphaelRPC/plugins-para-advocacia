#!/usr/bin/env python3
"""Busca as comunicações do DJEN (consulta pública do CNJ) pelas OABs do escritório.

A consulta é pública: não usa senha, certificado nem token. Ela traz o que foi
disponibilizado no Diário de Justiça Eletrônico Nacional para cada OAB, num
intervalo de datas de disponibilização, e grava uma planilha no formato do
lote (fonte,disponibilizada_em,tribunal,orgao,processo,partes,tipo_ato,teor,link)
para o importar_publicacoes.py levar ao publicacoes.csv.

Uso:
  python3 captar_djen.py --oab 123456/MG [--oab 654321/SP] --de AAAA-MM-DD [--ate AAAA-MM-DD] --saida djen.csv
  python3 captar_djen.py --ficha ficha-da-controladoria.md --registro-de-uso registro-de-uso.md --saida djen.csv
  python3 captar_djen.py --simular lote-de-treino.csv --de 2026-04-08 --ate 2026-04-14 --saida djen.csv

--simular lê o arquivo no lugar da rede (teste sem internet).
Sem internet ou com erro da consulta: código 1 e a orientação para importar a planilha.
Os nomes dos parâmetros e o limite por página seguem a documentação pública do CNJ [CONFERIR].
"""
import argparse
import csv
import datetime as dt
import html
import io
import json
import os
import re
import sys
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

URL_PADRAO = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
COLUNAS = ["fonte", "disponibilizada_em", "tribunal", "orgao", "processo", "partes", "tipo_ato", "teor", "link"]
ITENS_POR_PAGINA = 100   # [CONFERIR] o máximo aceito pela consulta pública
MAX_PAGINAS = 100

ORIENTACAO = ("Nada foi captado pelo DJEN nesta rodada. Faça a consulta pública no navegador (ou exporte "
              "do sistema do escritório), salve como planilha em 07-operacao/controladoria/entrada/ e rode "
              "importar_publicacoes.py. Registre no resumo: \"DJEN não consultado\".")


def erro(msg, codigo=1):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(codigo)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def data_iso(valor):
    v = (valor or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        a, mes, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})", v)
        if not m:
            return ""
        d, mes, a = m.groups()
    try:
        return dt.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return ""


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def parse_oab(valor):
    """Aceita 123456/MG, MG123456, 123.456/MG, OAB/MG 123456."""
    v = sem_acento(valor or "").upper()
    uf = re.search(r"\b([A-Z]{2})\b", v.replace("OAB", " "))
    num = re.sub(r"\D", "", v)
    if not uf or not num:
        return None
    # a OAB é texto: os zeros à esquerda ficam como a pessoa escreveu (000000 não vira 0)
    return num, uf.group(1)


def oabs_da_ficha(caminho):
    if not os.path.exists(caminho):
        erro(f"não encontrei a ficha {caminho}")
    texto = ler_texto(caminho)
    m = re.search(r"(?im)^\s*-?\s*oabs_monitoradas\s*:\s*(.+)$", texto)
    if not m or "[A PREENCHER]" in m.group(1):
        erro("a ficha não tem oabs_monitoradas preenchido. Preencha (número e UF de cada advogado) "
             "pelo /motor-controladoria:ficha ou passe --oab 123456/MG")
    valor = re.sub(r"\(.*?\)", "", m.group(1))
    oabs = [parse_oab(p) for p in re.split(r"[,;]| e ", valor) if p.strip()]
    oabs = [o for o in oabs if o]
    if not oabs:
        erro(f"não consegui ler as OABs da ficha: {m.group(1).strip()}. Use o formato 123456/MG")
    return oabs


def ultima_rodada(caminho):
    if not os.path.exists(caminho):
        erro(f"não encontrei o registro de uso {caminho}. Passe --de AAAA-MM-DD")
    datas = re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", ler_texto(caminho))
    if not datas:
        erro(f"o registro de uso {caminho} não tem nenhuma rodada com data. Passe --de AAAA-MM-DD")
    return max(datas)


def limpar_html(texto):
    if "<" not in (texto or ""):
        return (texto or "").strip()
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", texto)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n\n", t).strip()


def partes_do_item(it):
    ativo, passivo, outros = [], [], []
    for d in it.get("destinatarios") or []:
        nome = (d.get("nome") or "").strip()
        polo = (d.get("polo") or "").upper()
        if not nome:
            continue
        (ativo if polo == "A" else passivo if polo == "P" else outros).append(nome)
    partes = ", ".join(ativo)
    if passivo:
        partes += " x " + ", ".join(passivo)
    if outros:
        partes += (" · " if partes else "") + ", ".join(outros)
    return partes


def item_para_linha(it):
    processo = it.get("numeroprocessocommascara") or it.get("numero_processo") or ""
    return {
        "fonte": "djen",
        "disponibilizada_em": data_iso(it.get("data_disponibilizacao") or it.get("datadisponibilizacao") or ""),
        "tribunal": (it.get("siglaTribunal") or "").strip(),
        "orgao": (it.get("nomeOrgao") or "").strip(),
        "processo": processo.strip(),
        "partes": partes_do_item(it),
        "tipo_ato": (it.get("tipoDocumento") or it.get("tipoComunicacao") or "").strip(),
        "teor": limpar_html(it.get("texto") or ""),
        "link": (it.get("link") or "").strip(),
        "_chave": str(it.get("hash") or it.get("id") or ""),
    }


def consultar(url, oab, uf, de, ate, timeout):
    linhas = []
    vistos_paginas = set()
    pagina = 1
    while pagina <= MAX_PAGINAS:
        params = {"numeroOab": oab, "ufOab": uf, "dataDisponibilizacaoInicio": de,
                  "dataDisponibilizacaoFim": ate, "pagina": str(pagina), "itensPorPagina": str(ITENS_POR_PAGINA)}
        req = Request(f"{url}?{urlencode(params)}")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "motor-controladoria/1.0 (consulta publica)")
        with urlopen(req, timeout=timeout) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
        if isinstance(dados, dict) and str(dados.get("status", "success")).lower() not in ("success", "sucesso"):
            raise ValueError(f"a consulta respondeu: {dados.get('message') or dados.get('status')}")
        itens = dados.get("items", []) if isinstance(dados, dict) else (dados or [])
        # o campo count não serve para parar (vem igual ao tamanho da página): para quando a página vem
        # incompleta, vazia ou repetida
        primeiro = str(itens[0].get("id")) if itens else ""
        if not itens or primeiro in vistos_paginas:
            break
        vistos_paginas.add(primeiro)
        linhas.extend(item_para_linha(i) for i in itens)
        if len(itens) < ITENS_POR_PAGINA:
            break
        pagina += 1
        time.sleep(0.5)
    else:
        raise ValueError(f"mais de {MAX_PAGINAS} páginas para uma OAB; diminua o intervalo de datas")
    return linhas


def simular(caminho, de, ate):
    if not os.path.exists(caminho):
        erro(f"não encontrei o arquivo para simular: {caminho}")
    texto = ler_texto(caminho)
    primeira = texto.splitlines()[0] if texto.strip() else ""
    leitor = csv.DictReader(io.StringIO(texto), delimiter=";" if primeira.count(";") > primeira.count(",") else ",")
    cab = [c.strip().lower() for c in (leitor.fieldnames or [])]
    faltam = [c for c in ("disponibilizada_em", "processo", "teor") if c not in cab]
    if faltam:
        erro(f"{caminho}: faltam as colunas {', '.join(faltam)} (formato do lote de treino)")
    linhas = []
    for l in leitor:
        l = {(k or "").strip().lower(): (v or "").strip() for k, v in l.items()}
        if l.get("fonte", "djen").lower() not in ("djen", ""):
            continue
        d = data_iso(l.get("disponibilizada_em", ""))
        if not d or d < de or d > ate:
            continue
        linha = {c: l.get(c, "") for c in COLUNAS}
        linha["fonte"] = "djen"
        linha["disponibilizada_em"] = d
        linha["_chave"] = ""
        linhas.append(linha)
    return linhas


def main():
    ap = argparse.ArgumentParser(description="Busca publicações no DJEN (consulta pública do CNJ) pelas OABs")
    ap.add_argument("--oab", action="append", default=[], help="número e UF, ex.: 123456/MG (pode repetir)")
    ap.add_argument("--ficha", help="ficha-da-controladoria.md, para ler oabs_monitoradas")
    ap.add_argument("--de", help="primeira data de disponibilização, AAAA-MM-DD")
    ap.add_argument("--ate", help="última data de disponibilização (padrão: hoje)")
    ap.add_argument("--registro-de-uso", help="registro de uso do ciclo: --de vira a data da última rodada")
    ap.add_argument("--saida", required=True, help="planilha de saída (formato do lote)")
    ap.add_argument("--simular", help="lê este csv no lugar da rede (teste sem internet)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--url", default=URL_PADRAO, help=argparse.SUPPRESS)
    a = ap.parse_args()

    de = data_iso(a.de) if a.de else (ultima_rodada(a.registro_de_uso) if a.registro_de_uso else "")
    if not de:
        erro("diga desde quando buscar: --de AAAA-MM-DD ou --registro-de-uso <arquivo> (vale a data da última rodada)")
    ate = data_iso(a.ate) if a.ate else dt.date.today().isoformat()
    if not ate or ate < de:
        erro(f"intervalo inválido: de {de} até {a.ate}")

    if a.simular:
        linhas = simular(a.simular, de, ate)
        print(f"SIMULAÇÃO: nenhuma consulta foi feita; li {a.simular}")
        oabs = []
    else:
        oabs = [parse_oab(o) for o in a.oab]
        if any(o is None for o in oabs):
            erro("OAB em formato que não reconheço. Use 123456/MG")
        if a.ficha:
            oabs += oabs_da_ficha(a.ficha)
        if not oabs:
            erro("diga as OABs: --oab 123456/MG ou --ficha <ficha-da-controladoria.md>")
        oabs = list(dict.fromkeys(oabs))
        linhas, falhas = [], []
        for num, uf in oabs:
            try:
                linhas.extend(consultar(a.url, num, uf, de, ate, a.timeout))
            except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as e:
                falhas.append(f"OAB {num}/{uf}: {e}")
        if falhas and not linhas:
            erro("não consegui consultar o DJEN (" + "; ".join(falhas) + "). " + ORIENTACAO)

    vistos, unicas = set(), []
    for l in linhas:
        chave = l.get("_chave") or (re.sub(r"\D", "", l["processo"]), l["disponibilizada_em"],
                                    re.sub(r"\W+", "", l["teor"].lower()))
        if chave in vistos:
            continue
        vistos.add(chave)
        unicas.append(l)

    pasta = os.path.dirname(os.path.abspath(a.saida))
    os.makedirs(pasta, exist_ok=True)
    with open(a.saida, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for l in unicas:
            w.writerow(l)

    print(f"DJEN · disponibilizadas de {de} a {ate}"
          + (f" · OABs: {', '.join(f'{n}/{u}' for n, u in oabs)}" if oabs else ""))
    print(f"Comunicações: {len(unicas)} (repetidas entre OABs tiradas: {len(linhas) - len(unicas)})")
    print(f"Planilha: {a.saida}")
    if not a.simular and falhas:
        print("FALHOU PARCIALMENTE: " + "; ".join(falhas))
        print(ORIENTACAO)
        return 1
    if not unicas:
        print("Nenhuma comunicação no período. Confira as OABs e as datas antes de registrar \"nada novo\".")
    print("Próximo passo: importar_publicacoes.py com esta planilha.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
