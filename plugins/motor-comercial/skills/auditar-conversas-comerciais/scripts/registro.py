#!/usr/bin/env python3
"""Amostra e achados do registro para a auditoria das conversas comerciais (motor-comercial).

Cópia própria da auditar-conversas-comerciais. Lê o contatos.csv (formato em docs/funil.md) e:
  1. sorteia a amostra de conversas a exportar, por grupo, para ninguém escolher só as boas;
  2. aponta no registro o que a auditoria confere nas conversas:
     - contato sem resposta de uma pessoa (primeira_resposta vazia em novo ou triado) além do prazo;
     - perdido por sem-resposta (conferir na conversa se a última mensagem foi do contato);
     - quem pediu para parar e ainda tem retorno marcado;
     - régua fora do combinado: "retorno N de M" com N maior que M, ou M maior que o máximo da ficha;
     - retorno marcado para contato que fica fora da régua (fora da área, urgência alta);
     - contato com uma pessoa (proximo_passo começando por "pessoa agora:" ou "pessoa liga:",
       docs/funil.md, regra 4) com a data vencida: a conversa aconteceu e não foi registrada,
       ou não aconteceu.

Mostra contatos só pelo código. Não altera o csv.

Uso (da pasta de trabalho, com o caminho da pasta da habilidade):
  python3 <pasta-da-habilidade>/scripts/registro.py escritorio/07-operacao/comercial/contatos.csv 2026-03 \
      --tamanho 10 --prazo-horas 2 --maximo-retornos 3 --horario 09:00-18:00 --dias seg-sex \
      [--hoje AAAA-MM-DD] [--semente 7] [--treino]

Regras de leitura: vírgula ou ponto e vírgula; com ou sem BOM; cabeçalho, etapa e opções sem
diferenciar maiúscula; datas AAAA-MM-DD HH:MM ou DD/MM/AAAA HH:MM. Sai com código 1 e uma mensagem
clara quando falta o arquivo, quando ele está vazio ou quando falta uma coluna obrigatória.
"""

import argparse
import csv
import io
import os
import random
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta

OBRIGATORIAS = ["codigo", "entrada", "etapa", "primeira_resposta", "proximo_passo", "pediu_para_parar"]
NAO_FECHOU = {"perdido", "nao-compareceu", "sem-caso"}
NEGOCIACAO = {"proposta-enviada", "negociando"}
ANTES_DA_CONSULTA = {"novo", "triado"}
SEM_PROXIMO = {"", "nenhum", "nenhuma", "-", "n/a"}
# Marcador de pessoa no proximo_passo (funil.md, regra 4), já normalizado (minúsculas, sem acento).
MARCADORES_DE_PESSOA = ("pessoa agora", "pessoa liga")
RETORNO = re.compile(r"retorno\s+(\d+)\s+de\s+(\d+)")
DIAS_NOMES = {"seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5, "dom": 6}


def falhar(msg):
    sys.stderr.write("registro.py: " + msg + "\n")
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def norm(texto):
    return sem_acento((texto or "").strip().lower())


def ler_csv(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = ""
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    texto = texto.lstrip("\ufeff")
    if not texto.strip():
        falhar("o arquivo %s está vazio. Nada foi conferido." % caminho)
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    leitor.fieldnames = [norm(c) for c in (leitor.fieldnames or [])]
    linhas = []
    for bruta in leitor:
        linha = {k: (v or "").strip() if isinstance(v, str) else "" for k, v in bruta.items() if k}
        if any(linha.values()):
            linhas.append(linha)
    return leitor.fieldnames, linhas


def data_hora(texto):
    texto = (texto or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S",
                "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue
    return None


def ler_horario(texto):
    try:
        ini, fim = texto.split("-")
        return tuple(int(x) for x in ini.split(":")), tuple(int(x) for x in fim.split(":"))
    except ValueError:
        falhar("horário inválido: %s. Use HH:MM-HH:MM." % texto)


def ler_dias(texto):
    texto = norm(texto)
    try:
        if "-" in texto and "," not in texto:
            a, b = texto.split("-")
            return set(range(DIAS_NOMES[a.strip()], DIAS_NOMES[b.strip()] + 1))
        return {DIAS_NOMES[d.strip()] for d in texto.split(",") if d.strip()}
    except KeyError:
        falhar("dias inválidos: %s. Use seg-sex ou seg,ter,qua." % texto)


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


def fmt(h):
    if h < 1:
        return "%d min" % round(h * 60)
    return ("%.1f h" % h).replace(".", ",")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Amostra e achados do registro para a auditoria comercial.")
    ap.add_argument("csv")
    ap.add_argument("periodo", help="AAAA-MM: mês das entradas que formam a amostra")
    ap.add_argument("--tamanho", type=int, default=10)
    ap.add_argument("--prazo-horas", type=float)
    ap.add_argument("--maximo-retornos", type=int)
    ap.add_argument("--horario", default="09:00-18:00")
    ap.add_argument("--dias", default="seg-sex")
    ap.add_argument("--hoje")
    ap.add_argument("--semente", type=int)
    ap.add_argument("--treino", action="store_true")
    a = ap.parse_args(argv)

    try:
        datetime.strptime(a.periodo, "%Y-%m")
    except ValueError:
        falhar("período inválido: use AAAA-MM, por exemplo 2026-03.")
    if not os.path.isfile(a.csv):
        falhar("não encontrei o arquivo %s. O registro fica em escritorio/07-operacao/comercial/contatos.csv; "
               "nada foi conferido." % a.csv)
    if "_treino" in os.path.abspath(a.csv).replace("\\", "/").split("/") and not a.treino:
        falhar("este registro está na pasta _treino (casos fictícios). A auditoria do escritório nunca usa treino. "
               "Para treinar, rode de novo com --treino.")
    colunas, linhas = ler_csv(a.csv)
    faltando = [c for c in OBRIGATORIAS if c not in colunas]
    if faltando:
        falhar("o csv não tem as colunas %s. Confira a primeira linha com docs/funil.md; nada foi conferido."
               % ", ".join(faltando))
    if not linhas:
        falhar("o registro tem só o cabeçalho. Sem contatos, não há amostra nem achado.")
    horario = ler_horario(a.horario)
    dias = ler_dias(a.dias)
    try:
        hoje = datetime.strptime(a.hoje, "%Y-%m-%d").date() if a.hoje else date.today()
    except ValueError:
        falhar("data inválida em --hoje: use AAAA-MM-DD.")
    agora = datetime(hoje.year, hoje.month, hoje.day, horario[1][0], horario[1][1]) if a.hoje else datetime.now()

    # ---------------------------------------------------------------- amostra
    do_periodo = []
    for l in linhas:
        dt = data_hora(l.get("entrada"))
        if dt and dt.strftime("%Y-%m") == a.periodo and norm(l.get("tipo")) != "cliente":
            do_periodo.append(l)
    grupos = {
        "não fecharam (perdido, faltou, sem caso)": [l for l in do_periodo if norm(l.get("etapa")) in NAO_FECHOU],
        "em negociação (proposta enviada ou negociando)": [l for l in do_periodo if norm(l.get("etapa")) in NEGOCIACAO],
        "pediram para parar": [l for l in do_periodo if norm(l.get("pediu_para_parar")) == "sim"],
        "outros contatos novos": [],
    }
    usados = set()
    for g in list(grupos)[:3]:
        usados.update(l.get("codigo") for l in grupos[g])
    grupos["outros contatos novos"] = [l for l in do_periodo if l.get("codigo") not in usados]
    rnd = random.Random(a.semente)
    cotas = {"não fecharam (perdido, faltou, sem caso)": max(3, a.tamanho * 3 // 10),
             "em negociação (proposta enviada ou negociando)": max(2, a.tamanho // 5),
             "pediram para parar": len(grupos["pediram para parar"])}
    escolhidos = []
    grupo_de = {}
    for g, membros in grupos.items():
        codigos = sorted({l.get("codigo") for l in membros if l.get("codigo")} - set(escolhidos))
        rnd.shuffle(codigos)
        cota = cotas.get(g, max(0, a.tamanho - len(escolhidos)))
        for c in codigos[:cota]:
            escolhidos.append(c)
            grupo_de[c] = g
    escolhidos = escolhidos[:max(a.tamanho, len(grupos["pediram para parar"]))]

    # ---------------------------------------------------------------- achados do registro
    achados = []
    for l in linhas:
        cod = l.get("codigo") or "(sem código)"
        etapa = norm(l.get("etapa"))
        passo = norm(l.get("proximo_passo"))
        ini = data_hora(l.get("entrada"))
        if norm(l.get("tipo")) == "cliente":
            continue
        if etapa in ANTES_DA_CONSULTA and not norm(l.get("primeira_resposta")) and ini:
            h = horas_uteis(ini, agora, horario, dias)
            if a.prazo_horas is None or h > a.prazo_horas:
                achados.append(("sem resposta de uma pessoa%s" % (" além do prazo" if a.prazo_horas else ""),
                                cod, "%s úteis desde a entrada%s" % (fmt(h), "; urgência alta" if norm(l.get("urgencia")) == "alta" else "")))
        if etapa == "perdido" and norm(l.get("motivo_perda")) == "sem-resposta":
            achados.append(("perdido por sem-resposta: conferir se a última mensagem foi do contato", cod, ""))
        if norm(l.get("pediu_para_parar")) == "sim" and passo not in SEM_PROXIMO:
            achados.append(("pediu para parar e ainda tem próximo passo", cod, "proximo_passo: %s" % l.get("proximo_passo")))
        if passo.startswith(MARCADORES_DE_PESSOA):
            dp = data_hora(l.get("data_proximo_passo"))
            if dp is None or dp.date() < hoje:
                achados.append(("com uma pessoa e sem conversa registrada", cod,
                                "proximo_passo: %s; era %s; registrar o combinado pelo comando fila" % (
                                    l.get("proximo_passo"), dp.strftime("%Y-%m-%d") if dp else "sem data")))
        m = RETORNO.search(passo)
        if m:
            n, de = int(m.group(1)), int(m.group(2))
            if n > de:
                achados.append(("régua passou do combinado", cod, "retorno %d de %d" % (n, de)))
            if a.maximo_retornos is not None and de > a.maximo_retornos:
                achados.append(("régua maior que o máximo da ficha", cod, "retorno %d de %d; máximo %d" % (n, de, a.maximo_retornos)))
            if norm(l.get("area")) == "fora-da-area" or (norm(l.get("urgencia")) == "alta" and not norm(l.get("responsavel"))):
                achados.append(("retorno marcado para contato fora da régua", cod, "área %s, urgência %s" % (
                    l.get("area") or "-", l.get("urgencia") or "-")))
            dp = data_hora(l.get("data_proximo_passo"))
            if dp and dp.date() < hoje and etapa in ANTES_DA_CONSULTA | NEGOCIACAO | {"nao-compareceu"}:
                achados.append(("retorno vencido", cod, "era %s" % dp.strftime("%Y-%m-%d")))

    # ---------------------------------------------------------------- saída
    out = ["# Registro para a auditoria · entradas de %s%s" % (a.periodo, " · TREINO" if a.treino else ""), ""]
    out.append("Registro lido: %d linhas; %d contatos com entrada no período. Contatos só pelo código." % (len(linhas), len(do_periodo)))
    out.append("")
    out.append("## Amostra sorteada (%d conversas)" % len(escolhidos))
    out.append("")
    if not escolhidos:
        out.append("Nenhum contato com entrada no período. Confira o mês pedido.")
    else:
        out.append("| Grupo | Contatos no grupo | Sorteados |")
        out.append("|---|---|---|")
        for g, membros in grupos.items():
            cods = [c for c in escolhidos if grupo_de.get(c) == g]
            out.append("| %s | %d | %s |" % (g, len(membros), ", ".join(cods) or "-"))
        out.append("")
        out.append("Peça a exportação destas conversas, uma por arquivo, com o código no nome: %s." % ", ".join(escolhidos))
    out.append("")
    out.append("## O que o registro já mostra")
    out.append("")
    if achados:
        out.append("| Achado no registro | Contato | Detalhe |")
        out.append("|---|---|---|")
        for k, c, d in achados:
            out.append("| %s | %s | %s |" % (k, c, d or "-"))
    else:
        out.append("Nenhum achado nas colunas conferidas (%d linhas lidas)." % len(linhas))
    out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
