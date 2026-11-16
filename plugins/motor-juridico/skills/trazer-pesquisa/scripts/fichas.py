#!/usr/bin/env python3
"""Fichas de julgado da base de jurisprudência (motor-juridico, trazer-pesquisa).

O formato do arquivo de tema está em docs/pesquisa-jus-ia.md. Quatro comandos:

  validar ARQUIVO.md
      Confere cada ficha (de um rascunho ou de um tema da base): tribunal, classe e número,
      data, órgão e relator, tese, posição (a favor | contra | neutro), fonte com link e data
      da pesquisa, conferência, situação, aspas sem conferência e dado de cliente.
      Ficha sem número, tribunal, data ou link não entra na base.

  juntar RASCUNHO.md TEMA.md [--titulo "..."] [--teses a,b] [--hoje AAAA-MM-DD] [--gravar]
      Junta as fichas novas do rascunho ao tema (cria o tema se não existir). Não mexe nas
      fichas que já estão lá; ficha repetida é só listada. Sobe a versão, atualiza
      revisado_em e escreve uma linha no histórico. Sem --gravar, só mostra o que faria.

  vencidos PASTA_JURISPRUDENCIA [--hoje] [--validade N] [--ficha ficha-juridica.md]
      O lote de conferência: julgados não conferidos, com conferência vencida, amarelos e
      com situação a conferir, por tema; e os temas com a última pesquisa vencida.

  marcar TEMA.md --julgado NUMERO --cor verde|amarelo|vermelho --data AAAA-MM-DD
         --onde "inteiro teor no portal do tribunal" [--situacao vigente] [--gravar]
      Grava o resultado de uma conferência feita por uma pessoa na linha "Conferência no
      inteiro teor" da ficha, e a linha no histórico. Sem --gravar, só mostra.

Leitura robusta: .md com ou sem BOM, "·" ou "|" no título da ficha, datas AAAA-MM-DD ou
DD/MM/AAAA. Sai com código 1 e mensagem clara quando falta arquivo ou não há ficha nenhuma.
Só biblioteca padrão.
"""

import argparse
import os
import re
import sys
import unicodedata
from datetime import date, datetime

CAMPOS = [
    ("orgao e relator", "Órgão e relator"),
    ("tese em uma frase", "Tese em uma frase"),
    ("trecho util", "Trecho útil (entre aspas só se conferido palavra por palavra)"),
    ("para que serve no escritorio", "Para que serve no escritório"),
    ("fonte", "Fonte"),
    ("conferencia no inteiro teor", "Conferência no inteiro teor"),
    ("situacao", "Situação"),
]
SITUACOES = ("vigente", "superado em parte", "superado", "[conferir]", "`[conferir]`")
MODELO_TEMA = """---
documento: Jurisprudência · {titulo}
versao: 0
revisado_em: {hoje}
dono: [A PREENCHER]
teses_do_escritorio: [{teses}]
---

# {titulo}

## Como o tema está hoje (resumo do escritório)
[A PREENCHER] (3 a 6 linhas, escritas pelo advogado ou aprovadas por ele: corrente que prevalece, divergências, o que mudou)

## Julgados

## Histórico do tema
"""


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def ler(caminho):
    if not os.path.isfile(caminho):
        erro("não encontrei '%s'." % caminho)
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod).lstrip("﻿")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_data(t):
    t = (t or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    return None


def chave_campo(rotulo):
    r = sem_acento(rotulo.strip().lower())
    for k, _ in CAMPOS:
        if r.startswith(k):
            return k
    return r


def ler_tema(texto):
    """Divide o arquivo em cabeçalho, partes antes dos julgados, fichas e histórico."""
    linhas = texto.splitlines()
    fm, corpo = {}, linhas
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for l in linhas[1:i]:
                    m = re.match(r"^([\w_]+)\s*:\s*(.*)$", l)
                    if m:
                        fm[m.group(1)] = m.group(2).strip()
                corpo = linhas[i + 1:]
                break
    fichas, historico, antes = [], [], []
    secao, atual = "antes", None
    for n, l in enumerate(corpo):
        if l.startswith("## "):
            t = sem_acento(l[3:].lower())
            secao = "julgados" if t.startswith("julgados") else ("historico" if t.startswith("historico") else "outra")
            atual = None
            if secao == "outra" or secao == "antes":
                antes.append(l)
            continue
        if l.startswith("### "):
            partes = [p.strip() for p in re.split(r"\s+·\s+|\s+\|\s+", l[4:].strip())]
            atual = {"titulo": l[4:].strip(), "partes": partes, "campos": {}, "rotulos": {}, "linhas": [l]}
            fichas.append(atual)
            continue
        if atual is not None and secao in ("julgados", "antes", "outra"):
            atual["linhas"].append(l)
            m = re.match(r"^\s*-\s*([^:]{2,80}):\s*(.*)$", l)
            if m:
                k = chave_campo(m.group(1))
                atual["campos"][k] = m.group(2).strip()
                atual["rotulos"][k] = m.group(1).strip()
            continue
        if secao == "historico":
            if l.strip():
                historico.append(l)
        elif secao in ("antes", "outra"):
            antes.append(l)
    return fm, fichas, historico


def info(f):
    """Dados derivados de uma ficha."""
    p = f["partes"]
    d = {"tribunal": p[0] if p else "", "numero": p[1] if len(p) > 1 else "", "data_txt": p[2] if len(p) > 2 else ""}
    d["data"] = ler_data(d["data_txt"])
    num = d["numero"]
    ms = re.search(r"S[úu]mula\s+(?:Vinculante\s+)?(?:n[º°o.]*\s*)?(\d+)", num)
    mt = re.search(r"Tema\s+(?:n[º°o.]*\s*)?(\d+)", num)
    if ms:
        d["chave"] = "sumula-%s-%s" % (ms.group(1), re.sub(r"\W", "", d["tribunal"].upper()))
    elif mt:
        d["chave"] = "tema-%s-%s" % (mt.group(1), re.sub(r"\W", "", d["tribunal"].upper()))
    else:
        dig = re.sub(r"\D", "", num)
        d["chave"] = "julgado-%s" % dig if dig else ""
    c = f["campos"]
    serve = sem_acento(c.get("para que serve no escritorio", "").lower())
    d["posicao"] = "contra" if serve.startswith("contra") else ("a favor" if serve.startswith("a favor") else ("neutro" if serve.startswith("neutro") else ""))
    fonte = c.get("fonte", "")
    ml = re.search(r"https?://\S+", fonte)
    d["link"] = ml.group(0).rstrip(").,;") if ml else ""
    mp = re.search(r"pesquisa de (\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", fonte)
    d["pesquisa"] = ler_data(mp.group(1)) if mp else None
    conf = c.get("conferencia no inteiro teor", "")
    mc = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", conf)
    d["conf_data"] = ler_data(mc.group(0)) if mc else None
    cor = "não conferido"
    cl = sem_acento(conf.lower())
    if not re.search(r"verde\s*\|\s*amarelo", cl):
        for k in ("verde", "amarelo", "vermelho"):
            if re.search(r"\b%s\b" % k, cl):
                cor = k
    d["cor_escrita"] = cor
    d["cor"] = cor if d["conf_data"] else "não conferido"  # cor sem data não vale
    d["situacao"] = c.get("situacao", "").strip()
    d["exemplo"] = "EXEMPLO" in f["titulo"] or any("EXEMPLO" in v for v in c.values())
    return d


def conferir_ficha(f):
    d = info(f)
    nao_entra, avisos = [], []
    if not d["tribunal"]:
        nao_entra.append("sem tribunal no título")
    if not re.search(r"\d", d["numero"]):
        nao_entra.append("sem classe e número")
    if not d["data"]:
        nao_entra.append("sem data do julgamento (AAAA-MM-DD) no título")
    if not d["link"]:
        nao_entra.append("sem link para conferir")
    c = f["campos"]
    if not c.get("orgao e relator"):
        avisos.append("órgão e relator vazios: `[CONFERIR]` no inteiro teor")
    if not c.get("tese em uma frase"):
        avisos.append("sem tese em uma frase")
    if not d["posicao"]:
        avisos.append("posição não marcada: comece 'Para que serve' por 'a favor', 'contra' ou 'neutro'")
    if not d["pesquisa"]:
        avisos.append("fonte sem a data da pesquisa ('Jus IA, pesquisa de AAAA-MM-DD, link')")
    conf = c.get("conferencia no inteiro teor", "")
    if d["cor_escrita"] != "não conferido" and not d["conf_data"]:
        avisos.append("conferência com cor e sem data: volta a 'não conferido'")
    if not conf:
        avisos.append("sem a linha 'Conferência no inteiro teor'")
    trecho = c.get("trecho util", "")
    if re.search(r"[\"“”]", trecho) and d["cor"] != "verde":
        avisos.append("trecho entre aspas sem conferência verde: tire as aspas (paráfrase não vai entre aspas)")
    sit = d["situacao"].lower()
    if sit and not any(sit.startswith(s) for s in SITUACOES):
        avisos.append("situação fora das opções (vigente, superado em parte, superado, [CONFERIR])")
    texto = "\n".join(f["linhas"])
    if re.search(r"\bC-\d{4}-\d{4}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", texto):
        nao_entra.append("dado de cliente na ficha (código do caso ou CPF): a base guarda o julgado, não o caso")
    return d, nao_entra, avisos


def cmd_validar(a):
    fm, fichas, hist = ler_tema(ler(a.arquivo))
    if not fichas:
        erro("não achei nenhuma ficha ('### TRIBUNAL · CLASSE E NÚMERO · DATA') em '%s'." % a.arquivo)
    print("# Validação · %s" % os.path.basename(a.arquivo))
    print("")
    entram = 0
    vistos = {}
    for i, f in enumerate(fichas, start=1):
        d, nao, avisos = conferir_ficha(f)
        if d["chave"] in vistos:
            avisos.append("repetida: igual à ficha %d" % vistos[d["chave"]])
        vistos.setdefault(d["chave"], i)
        if not nao:
            entram += 1
        print("%d. %s" % (i, f["titulo"]))
        print("   posição: %s · conferência: %s%s · situação: %s%s" % (
            d["posicao"] or "não marcada", d["cor"], (" em %s" % d["conf_data"]) if d["conf_data"] else "",
            d["situacao"] or "vazia", " · EXEMPLO" if d["exemplo"] else ""))
        for x in nao:
            print("   NÃO ENTRA: %s" % x)
        for x in avisos:
            print("   aviso: %s" % x)
    contra = sum(1 for f in fichas if info(f)["posicao"] == "contra")
    nconf = sum(1 for f in fichas if info(f)["cor"] == "não conferido")
    print("")
    print("Fichas: %d · entram: %d · não entram: %d · contra: %d · não conferidas: %d" %
          (len(fichas), entram, len(fichas) - entram, contra, nconf))
    if nconf:
        print("Ficha não conferida não vai para peça sem passar pela conferir-citacoes.")


def cmd_juntar(a):
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    _, novas, _ = ler_tema(ler(a.rascunho))
    if not novas:
        erro("o rascunho '%s' não tem nenhuma ficha." % a.rascunho)
    if os.path.isfile(a.tema):
        texto = ler(a.tema)
        criado = False
    else:
        if not a.titulo:
            erro("o tema '%s' ainda não existe; passe --titulo \"Nome do tema\" para criar." % a.tema)
        texto = MODELO_TEMA.format(titulo=a.titulo, hoje=hoje.isoformat(), teses=a.teses or "")
        criado = True
    fm, existentes, hist = ler_tema(texto)
    chaves = {info(f)["chave"]: f for f in existentes if info(f)["chave"]}
    entram, repetidas, barradas = [], [], []
    for f in novas:
        d, nao, avisos = conferir_ficha(f)
        if nao:
            barradas.append((f["titulo"], nao))
        elif d["chave"] in chaves:
            velha = info(chaves[d["chave"]])
            nota = "" if (velha["cor"], velha["conf_data"]) == (d["cor"], d["conf_data"]) else \
                " (na base: %s; no rascunho: %s; a base não muda, confira)" % (velha["cor"], d["cor"])
            repetidas.append(f["titulo"] + nota)
        else:
            entram.append(f)
            chaves[d["chave"]] = f
    linhas = texto.splitlines()
    # acha onde termina a seção de julgados (antes de "## Histórico")
    idx_hist = next((i for i, l in enumerate(linhas) if l.startswith("## ") and sem_acento(l[3:].lower()).startswith("historico")), None)
    if idx_hist is None:
        linhas += ["", "## Histórico do tema"]
        idx_hist = len(linhas) - 1
    bloco = []
    for f in entram:
        corpo = [l for l in f["linhas"]]
        while corpo and not corpo[-1].strip():
            corpo.pop()
        bloco += corpo + [""]
    while idx_hist > 0 and not linhas[idx_hist - 1].strip():
        idx_hist -= 1
    linhas = linhas[:idx_hist] + ([""] if bloco else []) + bloco + linhas[idx_hist:] if bloco else linhas
    # cabeçalho
    contra = sum(1 for f in entram if info(f)["posicao"] == "contra")
    datas_p = sorted({info(f)["pesquisa"] for f in entram if info(f)["pesquisa"]})
    if entram:
        for i, l in enumerate(linhas):
            if re.match(r"^versao\s*:", l):
                n = re.search(r"\d+", l)
                linhas[i] = "versao: %d" % ((int(n.group(0)) if n else 0) + 1)
            elif re.match(r"^revisado_em\s*:", l):
                linhas[i] = "revisado_em: %s" % hoje.isoformat()
            elif re.match(r"^teses_do_escritorio\s*:", l) and a.teses:
                atuais = [x.strip() for x in re.sub(r"[\[\]]", "", l.split(":", 1)[1]).split(",") if x.strip()]
                for t in a.teses.split(","):
                    if t.strip() and t.strip() not in atuais:
                        atuais.append(t.strip())
                linhas[i] = "teses_do_escritorio: [%s]" % ", ".join(atuais)
            elif l.startswith("## ") and sem_acento(l[3:].lower()).startswith("historico"):
                break
        linhas.append("- %s · %d julgado(s) novo(s), %d contra, da pesquisa no Jus IA de %s · não conferidos até a conferência · trazer-pesquisa" % (
            hoje.isoformat(), len(entram), contra, ", ".join(x.isoformat() for x in datas_p) or "[data não informada]"))
    novo = "\n".join(linhas).rstrip() + "\n"
    print("# Juntar · %s -> %s%s" % (os.path.basename(a.rascunho), a.tema, " (tema novo)" if criado else ""))
    print("Entram: %d (contra: %d)" % (len(entram), contra))
    for f in entram:
        print("  + %s" % f["titulo"])
    if repetidas:
        print("Já estavam na base (não mudou nada): %d" % len(repetidas))
        for t in repetidas:
            print("  = %s" % t)
    if barradas:
        print("Não entram: %d" % len(barradas))
        for t, nao in barradas:
            print("  x %s: %s" % (t, "; ".join(nao)))
    if not a.gravar:
        print("")
        print("Nada foi gravado. Mostre ao advogado e rode de novo com --gravar depois do ok.")
        return
    if not entram and not criado:
        print("Nada novo para gravar.")
        return
    os.makedirs(os.path.dirname(os.path.abspath(a.tema)), exist_ok=True)
    with open(a.tema, "w", encoding="utf-8") as f:
        f.write(novo)
    print("Gravado em %s." % a.tema)


def achar_ficha_juridica(inicio):
    pasta = os.path.abspath(inicio if os.path.isdir(inicio) else os.path.dirname(inicio))
    while True:
        cand = os.path.join(pasta, "04-base", "comum", "ficha-juridica.md") if os.path.basename(pasta) == "escritorio" \
            else os.path.join(pasta, "escritorio", "04-base", "comum", "ficha-juridica.md")
        if os.path.isfile(cand):
            return cand
        cima = os.path.dirname(pasta)
        if cima == pasta:
            return None
        pasta = cima


def validade(a, inicio):
    if a.validade:
        return a.validade, "opção --validade"
    ficha = a.ficha or achar_ficha_juridica(inicio)
    if ficha and os.path.isfile(ficha):
        for l in ler(ficha).splitlines():
            m = re.match(r"^\s*-?\s*validade_da_conferencia\s*:\s*(.*)$", l)
            if m:
                v = m.group(1).split("(")[0]
                n = re.search(r"\d+", v)
                if n and "PREENCHER" not in v.upper():
                    return int(n.group(0)), "ficha jurídica"
    return 90, "padrão de 90 dias (sem validade_da_conferencia na ficha)"


def cmd_vencidos(a):
    if not os.path.isdir(a.pasta):
        erro("não encontrei a pasta da base em '%s' (o padrão é escritorio/04-base/juridico/jurisprudencia)." % a.pasta)
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    dias, de_onde = validade(a, a.pasta)
    arquivos = [n for n in sorted(os.listdir(a.pasta)) if n.endswith(".md") and not n.startswith(("_", "."))]
    if not arquivos:
        erro("a pasta '%s' não tem nenhum tema (.md)." % a.pasta)
    print("# Lote de conferência · %s · validade %d dias (%s)" % (hoje.isoformat(), dias, de_onde))
    total = 0
    for nome in arquivos:
        fm, fichas, hist = ler_tema(ler(os.path.join(a.pasta, nome)))
        itens = []
        ultima = None
        for f in fichas:
            d = info(f)
            if d["pesquisa"] and (not ultima or d["pesquisa"] > ultima):
                ultima = d["pesquisa"]
            motivo = None
            if d["cor"] == "não conferido":
                motivo = "não conferido"
            elif d["conf_data"] and (hoje - d["conf_data"]).days > dias:
                motivo = "conferência vencida (%s, %d dias)" % (d["conf_data"], (hoje - d["conf_data"]).days)
            elif d["cor"] == "amarelo":
                motivo = "amarelo: ajuste pendente"
            elif "conferir" in d["situacao"].lower():
                motivo = "situação a conferir"
            if motivo:
                itens.append((f["titulo"], motivo, d))
        print("")
        print("## %s (%d fichas)" % (nome[:-3], len(fichas)))
        if ultima and (hoje - ultima).days > dias:
            print("- PESQUISA NOVA NO JUS IA: a última é de %s (%d dias)" % (ultima, (hoje - ultima).days))
        elif not ultima:
            print("- sem data de pesquisa nas fichas")
        if not itens:
            print("- nada a conferir neste tema")
        for t, motivo, d in itens:
            total += 1
            print("- [ ] %s · %s · %s%s" % (t, motivo, d["link"] or "sem link", " · EXEMPLO" if d["exemplo"] else ""))
    print("")
    print("Total para conferir: %d. Cada um: inteiro teor no portal do tribunal, depois 'marcar' com a cor e a data." % total)


def cmd_marcar(a):
    if a.cor not in ("verde", "amarelo", "vermelho"):
        erro("cor deve ser verde, amarelo ou vermelho.")
    d0 = ler_data(a.data)
    if not d0:
        erro("data '%s' não lida; use AAAA-MM-DD." % a.data)
    if not a.onde.strip():
        erro("diga onde foi conferido (--onde), por exemplo 'inteiro teor no portal do tribunal'.")
    texto = ler(a.tema)
    fm, fichas, hist = ler_tema(texto)
    alvo = re.sub(r"\D", "", a.julgado)
    achadas = [f for f in fichas if (alvo and alvo == re.sub(r"\D", "", info(f)["numero"])) or a.julgado.lower() in f["titulo"].lower()]
    if not achadas:
        erro("não achei o julgado '%s' em '%s'." % (a.julgado, a.tema))
    if len(achadas) > 1:
        erro("'%s' bate com %d fichas; use o número completo." % (a.julgado, len(achadas)))
    f = achadas[0]
    linhas = texto.splitlines()
    ini = next(i for i, l in enumerate(linhas) if l.strip() == f["linhas"][0].strip())
    fim = ini + 1
    while fim < len(linhas) and not linhas[fim].startswith(("### ", "## ")):
        fim += 1
    mudou = []
    for i in range(ini, fim):
        m = re.match(r"^(\s*-\s*)([^:]{2,80}):\s*(.*)$", linhas[i])
        if not m:
            continue
        k = chave_campo(m.group(2))
        if k == "conferencia no inteiro teor":
            linhas[i] = "%s%s: %s · %s" % (m.group(1), m.group(2), d0.isoformat(), a.cor)
            mudou.append(linhas[i].strip())
        if k == "situacao" and a.situacao:
            linhas[i] = "%s%s: %s" % (m.group(1), m.group(2), a.situacao)
            mudou.append(linhas[i].strip())
    if not mudou:
        erro("a ficha não tem a linha 'Conferência no inteiro teor'; corrija o formato antes.")
    linhas.append("- %s · conferido %s: %s · %s%s" % (d0.isoformat(), a.cor, f["titulo"], a.onde,
                                                    (" · situação: %s" % a.situacao) if a.situacao else ""))
    print("Ficha: %s" % f["titulo"])
    for x in mudou:
        print("  -> %s" % x)
    if not a.gravar:
        print("Nada foi gravado. Rode de novo com --gravar depois do ok.")
        return
    with open(a.tema, "w", encoding="utf-8") as out:
        out.write("\n".join(linhas).rstrip() + "\n")
    print("Gravado em %s." % a.tema)


def main():
    ap = argparse.ArgumentParser(description="Fichas de julgado da base de jurisprudência.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("validar")
    p.add_argument("arquivo")
    p = sub.add_parser("juntar")
    p.add_argument("rascunho")
    p.add_argument("tema")
    p.add_argument("--titulo")
    p.add_argument("--teses", default="")
    p.add_argument("--hoje")
    p.add_argument("--gravar", action="store_true")
    p = sub.add_parser("vencidos")
    p.add_argument("pasta")
    p.add_argument("--hoje")
    p.add_argument("--validade", type=int)
    p.add_argument("--ficha")
    p = sub.add_parser("marcar")
    p.add_argument("tema")
    p.add_argument("--julgado", required=True)
    p.add_argument("--cor", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--onde", required=True)
    p.add_argument("--situacao")
    p.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    if a.cmd == "validar":
        cmd_validar(a)
    elif a.cmd == "juntar":
        cmd_juntar(a)
    elif a.cmd == "vencidos":
        cmd_vencidos(a)
    elif a.cmd == "marcar":
        cmd_marcar(a)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
