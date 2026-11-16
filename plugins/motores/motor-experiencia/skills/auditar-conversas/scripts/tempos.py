#!/usr/bin/env python3
"""Tempos de resposta e intervalos sem notícia em conversas com clientes ativos.

Para cada conversa (um arquivo .txt por cliente, de preferência com o nome igual ao código
da carteira, por exemplo C-2026-0001.txt), mede:
  - cada vez que o cliente escreveu e quanto esperou por uma pessoa do escritório
    (em horas úteis, contra o prazo da ficha: primeira_resposta_cliente_ativo);
  - quantas vezes o cliente cobrou de novo, em outro dia, enquanto ainda esperava;
  - se a conversa termina com o cliente sem retorno;
  - o maior intervalo sem nenhuma mensagem do escritório, em dias corridos, contando até
    a data de referência (contra o maximo_sem_noticia da ficha).

Mensagem curta de cortesia do cliente ("ok", "obrigada", "valeu", figurinha) não abre espera.
A resposta automática não conta como resposta de uma pessoa nem como notícia.
Não imprime o texto das mensagens nem o nome de quem escreveu: só o nome do arquivo e números.

Formatos de linha aceitos:
  15/03/2026 21:14 - Nome: texto            (Android)
  [15/03/2026, 21:14:05] Nome: texto        (iPhone)
  2026-03-15 21:14 Nome: texto              (colado à mão)
Linhas sem data e hora são continuação da mensagem anterior. Avisos do próprio WhatsApp
(sem "Nome:") são ignorados.

Uso:
  python3 tempos.py CONVERSAS/*.txt --equipe "ADVOGADA,SECRETARIA" [--automatico AUTOMATICO] \
      --prazo-horas 4 --horario 09:00-18:00 --dias seg-sex --maximo-sem-noticia 30 \
      --hoje "AAAA-MM-DD HH:MM" [--csv saida.csv]

--equipe       nomes (como aparecem na conversa) de quem responde pelo escritório
--automatico   nome de quem envia a resposta automática, se houver
Quem não está em nenhuma das duas listas é tratado como o cliente (ou quem fala por ele).
Sai com código 1 e mensagem clara quando nenhum arquivo é lido.
"""

import argparse
import csv
import os
import re
import statistics
import sys
from datetime import datetime, timedelta

PADROES = [
    re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}),? (\d{1,2}:\d{2})(?::\d{2})?\]?\s*(?:-\s*)?([^:]{1,60}?):\s?(.*)$"),
    re.compile(r"^(\d{4}-\d{2}-\d{2}),? (\d{1,2}:\d{2})(?::\d{2})?\]?\s*(?:-\s*)?([^:]{1,60}?):\s?(.*)$"),
]
SO_DATA = re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}),? \d{1,2}:\d{2}")
MIDIA = re.compile(r"(m[íi]dia oculta|arquivo de m[íi]dia oculto|[áa]udio omitido|imagem omitida|"
                   r"v[íi]deo omitido|<attached:|\.opus|\.ogg|ptt-)", re.I)
FIGURINHA = re.compile(r"(figurinha omitida|sticker omitted|\.webp)", re.I)
CORTESIA = re.compile(r"^\W*(ok+|okay|blz|beleza|certo|ta bom|tá bom|t[áa]|obrigad[oa]s?|obg|brigad[oa]|"
                      r"valeu|vlw|de nada|combinado|perfeito|entendi|show|amem|amém|bom dia|boa tarde|"
                      r"boa noite|tudo bem|\U0001F44D|\U0001F64F|\u2764\ufe0f?)(\W+(ok+|obrigad[oa]|dra\.?|dr\.?|doutora|doutor|"
                      r"viu|mesmo|tá|ta|pela ajuda|pela liga[çc][ãa]o( ontem)?(, dra\.?)?))*\W*$", re.I)
INVISIVEIS = dict.fromkeys(map(ord, "‎‏‪‬﻿"), None)
DIAS_NOMES = {"seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5, "sáb": 5, "dom": 6}
CODIGO = re.compile(r"^C-\d{4}-\d{4}(-\d+)?$", re.I)


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def ler_data(d, h="00:00"):
    hh, mm = h.split(":")[:2]
    if "-" in d:
        a, m, dia = d.split("-")
    else:
        dia, m, a = d.split("/")
        if len(a) == 2:
            a = "20" + a
    return datetime(int(a), int(m), int(dia), int(hh), int(mm))


def ler_hoje(texto):
    t = texto.strip()
    partes = t.split()
    try:
        if len(partes) == 1:
            return ler_data(partes[0]) + timedelta(hours=23, minutes=59)
        return ler_data(partes[0], partes[1])
    except (ValueError, IndexError):
        erro("--hoje '%s' não é uma data (use AAAA-MM-DD, DD/MM/AAAA ou 'AAAA-MM-DD HH:MM')." % texto)


def ler_conversa(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    msgs = []
    for linha in texto.splitlines():
        linha = linha.translate(INVISIVEIS).strip()
        if not linha:
            continue
        achou = None
        for p in PADROES:
            m = p.match(linha)
            if m:
                achou = m
                break
        if achou:
            d, h, quem, conteudo = achou.groups()
            try:
                quando = ler_data(d, h)
            except ValueError:
                continue
            msgs.append({"quando": quando, "quem": quem.strip(), "texto": conteudo.strip(),
                         "midia": bool(MIDIA.search(conteudo))})
        elif SO_DATA.match(linha):
            continue
        elif msgs:
            msgs[-1]["texto"] += " " + linha
            if MIDIA.search(linha):
                msgs[-1]["midia"] = True
    return msgs


def ler_horario(texto):
    try:
        ini, fim = texto.split("-")
        return tuple(int(x) for x in ini.split(":")), tuple(int(x) for x in fim.split(":"))
    except ValueError:
        erro("--horario '%s' não está no formato HH:MM-HH:MM." % texto)


def ler_dias(texto):
    texto = texto.strip().lower()
    try:
        if "-" in texto and "," not in texto:
            a, b = texto.split("-")
            return set(range(DIAS_NOMES[a], DIAS_NOMES[b] + 1))
        return {DIAS_NOMES[d.strip()] for d in texto.split(",") if d.strip()}
    except KeyError:
        erro("--dias '%s' não reconhecido (use seg-sex ou seg,ter,qua...)." % texto)


def horas_uteis(inicio, fim, horario, dias):
    if fim <= inicio:
        return 0.0
    (h1, m1), (h2, m2) = horario
    total = 0.0
    dia = inicio.date()
    while dia <= fim.date():
        if dia.weekday() in dias:
            a = max(datetime(dia.year, dia.month, dia.day, h1, m1), inicio)
            b = min(datetime(dia.year, dia.month, dia.day, h2, m2), fim)
            if b > a:
                total += (b - a).total_seconds() / 3600.0
        dia += timedelta(days=1)
    return total


def papel(nome, equipe, automatico):
    n = nome.strip().lower()
    if n in automatico:
        return "auto"
    if n in equipe:
        return "equipe"
    return "cliente"


def e_cortesia(m):
    t = m["texto"].strip()
    return bool(FIGURINHA.search(t)) or bool(CORTESIA.match(t)) or t == ""


def analisar(msgs, equipe, automatico, horario, dias, prazo, agora):
    r = {"mensagens": len(msgs), "do_cliente": 0, "midia_do_cliente": 0, "esperas": [],
         "fora_do_prazo": 0, "cobrou_de_novo": 0, "sem_retorno": None, "remetentes_cliente": set(),
         "maior_sem_noticia": None, "dias_desde_ultima": None, "auto_sem_pessoa": 0}
    esperando_desde = None
    ultimo_dia_cobranca = None
    auto_na_espera = False
    datas_escritorio = []
    for m in msgs:
        p = papel(m["quem"], equipe, automatico)
        if p == "cliente":
            r["do_cliente"] += 1
            r["remetentes_cliente"].add(m["quem"].lower())
            if m["midia"]:
                r["midia_do_cliente"] += 1
            if esperando_desde is None:
                if not e_cortesia(m):
                    esperando_desde = m["quando"]
                    ultimo_dia_cobranca = m["quando"].date()
            elif m["quando"].date() != ultimo_dia_cobranca and not e_cortesia(m):
                r["cobrou_de_novo"] += 1
                ultimo_dia_cobranca = m["quando"].date()
        elif p == "auto":
            if esperando_desde is not None:
                auto_na_espera = True
        else:
            datas_escritorio.append(m["quando"])
            if esperando_desde is not None:
                u = horas_uteis(esperando_desde, m["quando"], horario, dias)
                r["esperas"].append(u)
                if prazo is not None and u > prazo:
                    r["fora_do_prazo"] += 1
                esperando_desde = None
                auto_na_espera = False
    if esperando_desde is not None:
        r["sem_retorno"] = horas_uteis(esperando_desde, agora, horario, dias)
        if auto_na_espera:
            r["auto_sem_pessoa"] = 1
    if datas_escritorio:
        pontos = sorted(datas_escritorio) + [agora]
        r["maior_sem_noticia"] = max((b.date() - a.date()).days for a, b in zip(pontos, pontos[1:]))
        r["dias_desde_ultima"] = (agora.date() - max(datas_escritorio).date()).days
    return r


def fmt(h):
    if h is None:
        return "-"
    if h < 1:
        return "%d min" % round(h * 60)
    return ("%.1f h" % h).replace(".", ",")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tempos e intervalos sem notícia em conversas com clientes.")
    ap.add_argument("arquivos", nargs="*")
    ap.add_argument("--equipe", required=True)
    ap.add_argument("--automatico", default="")
    ap.add_argument("--prazo-horas", type=float, help="primeira_resposta_cliente_ativo, em horas úteis")
    ap.add_argument("--horario", default="09:00-18:00")
    ap.add_argument("--dias", default="seg-sex")
    ap.add_argument("--maximo-sem-noticia", type=int, help="maximo_sem_noticia, em dias corridos")
    ap.add_argument("--hoje", help="data de referência (padrão: agora)")
    ap.add_argument("--csv")
    a = ap.parse_args(argv)

    if not a.arquivos:
        erro("nenhum arquivo de conversa informado. Passe os .txt exportados (um por cliente).")
    equipe = {n.strip().lower() for n in a.equipe.split(",") if n.strip()}
    if not equipe:
        erro("--equipe vazio: diga como aparecem na conversa as pessoas do escritório.")
    automatico = {n.strip().lower() for n in a.automatico.split(",") if n.strip()}
    horario = ler_horario(a.horario)
    dias = ler_dias(a.dias)
    agora = ler_hoje(a.hoje) if a.hoje else datetime.now()

    linhas, avisos = [], []
    for caminho in a.arquivos:
        if not os.path.isfile(caminho):
            avisos.append("não encontrei: %s" % caminho)
            continue
        msgs = ler_conversa(caminho)
        nome = os.path.splitext(os.path.basename(caminho))[0]
        if not msgs:
            avisos.append("%s: nenhuma mensagem no formato esperado" % nome)
            continue
        if not CODIGO.match(nome):
            avisos.append("%s: o nome do arquivo não é um código da carteira (C-AAAA-NNNN)" % nome)
        r = analisar(msgs, equipe, automatico, horario, dias, a.prazo_horas, agora)
        if not any(papel(m["quem"], equipe, automatico) == "equipe" for m in msgs):
            avisos.append("%s: nenhum remetente da equipe encontrado; confira --equipe" % nome)
        if len(r["remetentes_cliente"]) > 1:
            avisos.append("%s: %d remetentes tratados como cliente; confira --equipe e --automatico"
                          % (nome, len(r["remetentes_cliente"])))
        if msgs[-1]["quando"] > agora:
            avisos.append("%s: há mensagens depois da data de referência (--hoje)" % nome)
        r["nome"] = nome
        r["inicio"] = msgs[0]["quando"]
        linhas.append(r)

    if not linhas:
        erro("nenhuma conversa lida. " + " ".join(avisos))

    maximo = a.maximo_sem_noticia
    out = []
    add = out.append
    add("# Tempos com clientes ativos · %d conversas" % len(linhas))
    add("")
    add("Referência: %s. Horas úteis no horário %s, dias %s, sem descontar feriados. A resposta automática "
        "não conta como resposta nem como notícia. Cortesia do cliente (\"ok\", \"obrigada\") não abre espera.%s%s"
        % (agora.strftime("%Y-%m-%d %H:%M"), a.horario, a.dias,
           " Prazo de resposta: %s úteis." % fmt(a.prazo_horas) if a.prazo_horas else " Prazo de resposta: [A DEFINIR].",
           " Máximo sem notícia: %d dias corridos." % maximo if maximo is not None else " Máximo sem notícia: [A DEFINIR]."))
    add("")
    add("| Conversa | Início | Esperas respondidas | Mediana | Maior | Respondidas fora do prazo | Cobrou de novo sem resposta | Termina sem retorno | Maior intervalo sem mensagem do escritório | Dias desde a última | Mídias do cliente |")
    add("|---|---|---|---|---|---|---|---|---|---|---|")
    todas, sem_retorno, acima = [], [], []
    for r in linhas:
        todas.extend(r["esperas"])
        if r["sem_retorno"] is not None:
            sem_retorno.append(r)
        if maximo is not None and r["maior_sem_noticia"] is not None and r["maior_sem_noticia"] > maximo:
            acima.append(r)
        intervalo = "-" if r["maior_sem_noticia"] is None else "%d dias%s" % (
            r["maior_sem_noticia"], " (acima do máximo)" if r in acima else "")
        add("| %s | %s | %d | %s | %s | %s | %d | %s | %s | %s | %d |" % (
            r["nome"], r["inicio"].strftime("%d/%m/%Y"), len(r["esperas"]),
            fmt(statistics.median(r["esperas"])) if r["esperas"] else "-",
            fmt(max(r["esperas"])) if r["esperas"] else "-",
            str(r["fora_do_prazo"]) if a.prazo_horas else "-",
            r["cobrou_de_novo"],
            ("sim, há %s úteis%s%s" % (fmt(r["sem_retorno"]),
                                       (", fora do prazo" if r["sem_retorno"] > a.prazo_horas else ", ainda no prazo")
                                       if a.prazo_horas else "",
                                       ", só a automática respondeu" if r["auto_sem_pessoa"] else ""))
            if r["sem_retorno"] is not None else "não",
            intervalo,
            "-" if r["dias_desde_ultima"] is None else str(r["dias_desde_ultima"]),
            r["midia_do_cliente"]))
    add("")
    add("## Resumo")
    add("")
    add("| Medida | Valor |")
    add("|---|---|")
    add("| Conversas | %d |" % len(linhas))
    add("| Vezes que um cliente esperou e foi respondido | %d |" % len(todas))
    if todas:
        add("| Mediana das esperas (úteis) | %s |" % fmt(statistics.median(todas)))
        add("| Maior espera (úteis) | %s |" % fmt(max(todas)))
    if a.prazo_horas:
        add("| Esperas respondidas fora do prazo | %d de %d |" % (sum(r["fora_do_prazo"] for r in linhas), len(todas)))
        add("| Esperas sem retorno que já passaram do prazo | %d |" % sum(
            1 for r in sem_retorno if r["sem_retorno"] > a.prazo_horas))
    add("| Cobranças repetidas sem resposta | %d |" % sum(r["cobrou_de_novo"] for r in linhas))
    add("| Conversas que terminam sem retorno | %d |" % len(sem_retorno))
    if maximo is not None:
        add("| Conversas com intervalo acima do máximo sem notícia | %d |" % len(acima))
    add("")
    if sem_retorno:
        add("Sem retorno: " + ", ".join("%s (%s úteis)" % (r["nome"], fmt(r["sem_retorno"])) for r in sem_retorno) + ".")
        add("")
    if acima:
        add("Acima do máximo sem notícia: " + ", ".join("%s (%d dias)" % (r["nome"], r["maior_sem_noticia"]) for r in acima)
            + ". Confira na carteira se houve ligação ou reunião fora desta conversa.")
        add("")
    add("O script mede tempo, não conteúdo: \"vou ver\" conta como resposta e como notícia. A leitura dos critérios corrige isso.")
    add("")
    if avisos:
        add("## Avisos")
        add("")
        for av in avisos:
            add("- " + av)
        add("")
    print("\n".join(out))

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["conversa", "inicio", "esperas", "mediana_uteis_h", "maior_uteis_h", "fora_do_prazo",
                        "cobrou_de_novo", "sem_retorno_uteis_h", "maior_sem_noticia_dias", "dias_desde_ultima",
                        "midias_do_cliente"])
            for r in linhas:
                w.writerow([r["nome"], r["inicio"].strftime("%Y-%m-%d %H:%M"), len(r["esperas"]),
                            round(statistics.median(r["esperas"]), 2) if r["esperas"] else "",
                            round(max(r["esperas"]), 2) if r["esperas"] else "",
                            r["fora_do_prazo"] if a.prazo_horas else "", r["cobrou_de_novo"],
                            round(r["sem_retorno"], 2) if r["sem_retorno"] is not None else "",
                            "" if r["maior_sem_noticia"] is None else r["maior_sem_noticia"],
                            "" if r["dias_desde_ultima"] is None else r["dias_desde_ultima"],
                            r["midia_do_cliente"]])
        sys.stderr.write("csv: %s\n" % a.csv)


if __name__ == "__main__":
    main()
