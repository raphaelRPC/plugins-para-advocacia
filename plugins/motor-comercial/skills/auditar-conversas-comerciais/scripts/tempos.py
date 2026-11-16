#!/usr/bin/env python3
"""Tempos e sinais de conduta em conversas comerciais exportadas do WhatsApp (ou coladas no mesmo formato).

Cópia própria da auditar-conversas-comerciais (motor-comercial). Funciona sozinha.

Para cada conversa (um arquivo .txt por conversa, com o código do contato no nome, por exemplo
C-2026-0002.txt), mede:
  - a primeira resposta de uma pessoa do escritório à primeira mensagem do contato;
  - a primeira resposta automática, se houver (não conta como resposta de pessoa);
  - cada vez que o contato escreveu e quanto esperou por uma pessoa;
  - se a conversa terminou com o contato sem retorno;
  - quantos retornos seguidos o escritório mandou depois da última mensagem do contato
    (um por dia com mensagem do escritório), para comparar com o maximo_de_retornos da ficha;
  - se o escritório escreveu depois de o contato pedir para parar.

Mede em horas corridas e em horas úteis (horário e dias de atendimento da ficha). Não imprime o
texto das mensagens nem o nome de quem escreveu: só o nome do arquivo e os números.

Formatos de linha aceitos:
  15/03/2026 21:14 - Nome: texto            (Android)
  [15/03/2026, 21:14:05] Nome: texto        (iPhone)
  2026-03-15 21:14 Nome: texto              (colado à mão)
Linhas sem data e hora são continuação da mensagem anterior. Avisos do próprio WhatsApp (sem
"Nome:") são ignorados.

Uso (da pasta de trabalho, com o caminho da pasta da habilidade):
  python3 <pasta-da-habilidade>/scripts/tempos.py conversas/*.txt --equipe "SECRETARIA,ADVOGADA" \
      --automatico "AUTOMATICO" --prazo-horas 2 --horario 09:00-18:00 --dias seg-sex \
      --maximo-retornos 3 [--hoje AAAA-MM-DD] [--csv saida.csv] [--treino]

--equipe       nomes (como aparecem na conversa) de quem responde pelo escritório
--automatico   nome de quem envia a resposta automática, se houver
Quem não está em nenhuma das duas listas é tratado como o contato.

Sai com código 1 e uma mensagem clara quando nenhum arquivo existe, quando nenhuma conversa
foi lida ou quando um arquivo está na pasta _treino sem a opção --treino.
"""

import argparse
import csv
import os
import re
import statistics
import sys
import unicodedata
from datetime import datetime, timedelta

PADROES = [
    re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}),? (\d{1,2}:\d{2})(?::\d{2})?\]?\s*(?:-\s*)?([^:]{1,60}?):\s?(.*)$"),
    re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{1,2}:\d{2})(?::\d{2})?\s*(?:-\s*)?([^:]{1,60}?):\s?(.*)$"),
]
SO_DATA = re.compile(r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}),? \d{1,2}:\d{2}")
MIDIA = re.compile(r"(m[íi]dia oculta|arquivo de m[íi]dia oculto|[áa]udio omitido|imagem omitida|"
                   r"v[íi]deo omitido|<attached:|\.opus|\.ogg|ptt-)", re.I)
# Pedido de parar: o contato não quer mais receber mensagens. Lista curta e conservadora; a leitura
# da conversa confirma (critério 9 da auditoria).
PARAR = re.compile(r"(n[aã]o quero mais (receber|que me mandem|mensage)|para(r)? de (me )?mandar|"
                   r"pode parar|n[aã]o me mande mais|n[aã]o mandem mais|me tira(m)? da lista|"
                   r"n[aã]o tenho mais interesse|sem interesse|descadastr)", re.I)
INVISIVEIS = dict.fromkeys(map(ord, "\u200e\u200f\u202a\u202c\ufeff"), None)
DIAS_NOMES = {"seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5, "dom": 6}


def falhar(msg):
    sys.stderr.write("tempos.py: " + msg + "\n")
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def ler_data(d, h):
    if "-" in d:
        return datetime.strptime("%s %s" % (d, h), "%Y-%m-%d %H:%M")
    dia, mes, ano = d.split("/")
    if len(ano) == 2:
        ano = "20" + ano
    hh, mm = h.split(":")
    return datetime(int(ano), int(mes), int(dia), int(hh), int(mm))


def ler_conversa(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = ""
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
            msgs.append({"quando": quando, "quem": quem.strip(), "midia": bool(MIDIA.search(conteudo)),
                         "parar": bool(PARAR.search(conteudo))})
        elif SO_DATA.match(linha):
            continue
        elif msgs:
            if MIDIA.search(linha):
                msgs[-1]["midia"] = True
            if PARAR.search(linha):
                msgs[-1]["parar"] = True
    return msgs


def ler_horario(texto):
    try:
        ini, fim = texto.split("-")
        return tuple(int(x) for x in ini.split(":")), tuple(int(x) for x in fim.split(":"))
    except ValueError:
        falhar("horário inválido: %s. Use HH:MM-HH:MM, por exemplo 09:00-18:00." % texto)


def ler_dias(texto):
    texto = sem_acento(texto.strip().lower())
    try:
        if "-" in texto and "," not in texto:
            a, b = texto.split("-")
            return set(range(DIAS_NOMES[a.strip()], DIAS_NOMES[b.strip()] + 1))
        return {DIAS_NOMES[d.strip()] for d in texto.split(",") if d.strip()}
    except KeyError:
        falhar("dias inválidos: %s. Use seg-sex ou uma lista como seg,ter,qua." % texto)


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
    n = sem_acento(nome.strip().lower())
    if n in automatico:
        return "auto"
    if n in equipe:
        return "equipe"
    return "contato"


def analisar(msgs, equipe, automatico, horario, dias, prazo, agora):
    r = {"mensagens": len(msgs), "do_contato": 0, "midia_do_contato": 0, "vezes": 0,
         "esperas": [], "fora_do_prazo": 0, "primeira": None, "primeira_auto": None,
         "sem_retorno": None, "remetentes_contato": set(), "retornos_seguidos": 0,
         "depois_de_parar": 0, "pediu_parar": False}
    if not msgs:
        return r
    esperando_desde = None
    primeira_do_contato = None
    pediu_parar_em = None
    confirmou_parar = False
    ultima_do_contato = None
    for m in msgs:
        p = papel(m["quem"], equipe, automatico)
        if p == "contato":
            r["do_contato"] += 1
            r["remetentes_contato"].add(m["quem"].lower())
            ultima_do_contato = m["quando"]
            if m["midia"]:
                r["midia_do_contato"] += 1
            if m["parar"] and pediu_parar_em is None:
                pediu_parar_em = m["quando"]
                r["pediu_parar"] = True
            if primeira_do_contato is None:
                primeira_do_contato = m["quando"]
            if esperando_desde is None:
                esperando_desde = m["quando"]
            continue
        if pediu_parar_em is not None and m["quando"] >= pediu_parar_em:
            # a primeira mensagem depois do pedido é a confirmação curta, que a ficha prevê; as outras contam
            if confirmou_parar:
                r["depois_de_parar"] += 1
            confirmou_parar = True
        if p == "auto":
            if primeira_do_contato is not None and r["primeira_auto"] is None:
                r["primeira_auto"] = (m["quando"] - primeira_do_contato).total_seconds() / 3600.0
            continue
        if esperando_desde is not None:
            u = horas_uteis(esperando_desde, m["quando"], horario, dias)
            c = (m["quando"] - esperando_desde).total_seconds() / 3600.0
            r["vezes"] += 1
            r["esperas"].append(u)
            if prazo is not None and u > prazo:
                r["fora_do_prazo"] += 1
            if r["primeira"] is None and esperando_desde == primeira_do_contato:
                r["primeira"] = (u, c)
            esperando_desde = None
    if esperando_desde is not None:
        r["sem_retorno"] = horas_uteis(esperando_desde, agora, horario, dias)
    # retornos seguidos: dias distintos com mensagem de pessoa do escritório depois da última do contato
    dias_com_retorno = set()
    for m in msgs:
        if papel(m["quem"], equipe, automatico) == "equipe" and (ultima_do_contato is None or m["quando"] > ultima_do_contato):
            dias_com_retorno.add(m["quando"].date())
    # o primeiro dia depois da última do contato é a resposta; os outros são retornos sem resposta
    r["retornos_seguidos"] = max(0, len(dias_com_retorno) - 1) if ultima_do_contato else len(dias_com_retorno)
    return r


def fmt(h):
    if h is None:
        return "-"
    if h < 1:
        return "%d min" % round(h * 60)
    return ("%.1f h" % h).replace(".", ",")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tempos e sinais em conversas comerciais exportadas.")
    ap.add_argument("arquivos", nargs="+")
    ap.add_argument("--equipe", required=True)
    ap.add_argument("--automatico", default="")
    ap.add_argument("--prazo-horas", type=float)
    ap.add_argument("--maximo-retornos", type=int)
    ap.add_argument("--horario", default="09:00-18:00")
    ap.add_argument("--dias", default="seg-sex")
    ap.add_argument("--hoje")
    ap.add_argument("--csv")
    ap.add_argument("--treino", action="store_true")
    a = ap.parse_args(argv)

    equipe = {sem_acento(n.strip().lower()) for n in a.equipe.split(",") if n.strip()}
    if not equipe:
        falhar("--equipe vazio: diga como a anonimização chamou quem responde pelo escritório (ex.: SECRETARIA,ADVOGADA).")
    automatico = {sem_acento(n.strip().lower()) for n in a.automatico.split(",") if n.strip()}
    horario = ler_horario(a.horario)
    dias = ler_dias(a.dias)
    try:
        agora = datetime.strptime(a.hoje, "%Y-%m-%d") + timedelta(hours=23, minutes=59) if a.hoje else datetime.now()
    except ValueError:
        falhar("data inválida em --hoje: use AAAA-MM-DD.")

    existentes = [c for c in a.arquivos if os.path.isfile(c)]
    if not existentes:
        falhar("não encontrei nenhum dos arquivos (%s). Nada foi medido." % ", ".join(a.arquivos[:5]))
    treino = [c for c in existentes if "_treino" in os.path.abspath(c).replace("\\", "/").split("/")]
    if treino and not a.treino:
        falhar("%d arquivo(s) estão na pasta _treino (casos fictícios). A auditoria do escritório nunca mistura "
               "treino. Para treinar, rode de novo com --treino." % len(treino))

    linhas = []
    avisos = ["não encontrei: %s" % c for c in a.arquivos if not os.path.isfile(c)]
    for caminho in existentes:
        msgs = ler_conversa(caminho)
        nome = os.path.splitext(os.path.basename(caminho))[0]
        if not msgs:
            avisos.append("%s: nenhuma mensagem no formato esperado" % nome)
            continue
        r = analisar(msgs, equipe, automatico, horario, dias, a.prazo_horas, agora)
        if not any(papel(m["quem"], equipe, automatico) == "equipe" for m in msgs):
            avisos.append("%s: nenhum remetente da equipe encontrado; confira --equipe" % nome)
        if len(r["remetentes_contato"]) > 1:
            avisos.append("%s: %d remetentes tratados como contato; confira --equipe e --automatico"
                          % (nome, len(r["remetentes_contato"])))
        r["nome"] = nome
        r["inicio"] = msgs[0]["quando"]
        linhas.append(r)

    if not linhas:
        falhar("nenhuma conversa lida. " + " ".join(avisos))

    out = []
    add = out.append
    add("# Tempos e sinais das conversas · %d conversas%s" % (len(linhas), " · TREINO" if treino else ""))
    add("")
    add("Horas úteis no horário %s, dias %s, sem descontar feriados. A resposta automática não conta "
        "como resposta de uma pessoa.%s O script mede tempo e sinais; o conteúdo é lido na auditoria."
        % (a.horario, a.dias, " Prazo usado: %s úteis." % fmt(a.prazo_horas) if a.prazo_horas else ""))
    add("")
    add("| Conversa | Início | Primeira resposta (úteis) | Corridas | Automática antes | Esperas | Maior | "
        "Fora do prazo | Termina sem retorno | Retornos seguidos sem resposta | Pediu para parar | Escreveu depois da confirmação |")
    add("|---|---|---|---|---|---|---|---|---|---|---|---|")
    todas, primeiras, sem_retorno, acima, depois = [], [], [], [], []
    for r in linhas:
        todas.extend(r["esperas"])
        if r["primeira"]:
            primeiras.append(r["primeira"][0])
        if r["sem_retorno"] is not None:
            sem_retorno.append((r["nome"], r["sem_retorno"]))
        if a.maximo_retornos is not None and r["retornos_seguidos"] > a.maximo_retornos:
            acima.append(r["nome"])
        if r["depois_de_parar"]:
            depois.append(r["nome"])
        add("| %s | %s | %s | %s | %s | %d | %s | %s | %s | %d | %s | %s |" % (
            r["nome"], r["inicio"].strftime("%d/%m %H:%M"),
            fmt(r["primeira"][0]) if r["primeira"] else "sem resposta",
            fmt(r["primeira"][1]) if r["primeira"] else "-",
            fmt(r["primeira_auto"]) if r["primeira_auto"] is not None else "não",
            r["vezes"],
            fmt(max(r["esperas"])) if r["esperas"] else "-",
            str(r["fora_do_prazo"]) if a.prazo_horas else "-",
            ("sim, há %s úteis" % fmt(r["sem_retorno"])) if r["sem_retorno"] is not None else "não",
            r["retornos_seguidos"],
            "sim" if r["pediu_parar"] else "não",
            ("%d mensagem(ns)" % r["depois_de_parar"]) if r["depois_de_parar"] else "não"))
    add("")
    add("## Resumo")
    add("")
    add("| Medida | Valor |")
    add("|---|---|")
    add("| Conversas | %d |" % len(linhas))
    add("| Com primeira resposta de pessoa | %d de %d |" % (len(primeiras), len(linhas)))
    if primeiras:
        add("| Mediana da primeira resposta (úteis) | %s |" % fmt(statistics.median(primeiras)))
    if a.prazo_horas and primeiras:
        add("| Primeira resposta dentro do prazo | %d de %d |" % (sum(1 for p in primeiras if p <= a.prazo_horas), len(primeiras)))
    add("| Vezes que um contato esperou uma pessoa | %d |" % len(todas))
    if todas:
        add("| Maior espera (úteis) | %s |" % fmt(max(todas)))
    if a.prazo_horas:
        add("| Esperas fora do prazo | %d de %d |" % (sum(r["fora_do_prazo"] for r in linhas), len(todas)))
    add("| Conversas que terminam sem retorno | %d |" % len(sem_retorno))
    if a.maximo_retornos is not None:
        add("| Retornos acima do máximo da ficha (%d) | %d |" % (a.maximo_retornos, len(acima)))
    add("| Escritório escreveu depois de confirmar o pedido para parar | %d |" % len(depois))
    add("")
    if sem_retorno:
        add("Sem retorno: " + ", ".join("%s (%s úteis)" % (n, fmt(h)) for n, h in sem_retorno) + ".")
        add("")
    if acima:
        add("Retornos acima do máximo: " + ", ".join(acima) + ".")
        add("")
    if depois:
        add("Mensagem depois do pedido para parar (conferir na leitura, achado crítico se confirmado): "
            + ", ".join(depois) + ".")
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
            w.writerow(["conversa", "inicio", "primeira_resposta_uteis_h", "primeira_resposta_corridas_h",
                        "automatica_antes_h", "esperas", "maior_uteis_h", "fora_do_prazo",
                        "sem_retorno_uteis_h", "retornos_seguidos", "pediu_parar", "mensagens_depois_de_parar"])
            for r in linhas:
                w.writerow([r["nome"], r["inicio"].strftime("%Y-%m-%d %H:%M"),
                            round(r["primeira"][0], 2) if r["primeira"] else "",
                            round(r["primeira"][1], 2) if r["primeira"] else "",
                            round(r["primeira_auto"], 2) if r["primeira_auto"] is not None else "",
                            r["vezes"],
                            round(max(r["esperas"]), 2) if r["esperas"] else "",
                            r["fora_do_prazo"] if a.prazo_horas else "",
                            round(r["sem_retorno"], 2) if r["sem_retorno"] is not None else "",
                            r["retornos_seguidos"], "sim" if r["pediu_parar"] else "nao", r["depois_de_parar"]])
        sys.stderr.write("csv: %s\n" % a.csv)


if __name__ == "__main__":
    main()
