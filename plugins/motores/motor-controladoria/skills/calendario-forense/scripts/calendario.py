#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calendario.py · rascunho e conferência do calendário forense de um tribunal.

  python3 calendario.py rascunho --tribunal TJMG --ano 2027 [--cidade "Belo Horizonte"]
      [--justica estadual|federal|trabalho] [--saida <arquivo.md>]
  python3 calendario.py validar <arquivo.md ou pasta> [--tribunal SIGLA] [--ano AAAA]

O rascunho traz só o ponto de partida: os feriados nacionais de data fixa, as datas móveis
calculadas pela Páscoa (carnaval, quarta-feira de cinzas, sexta-feira santa, Corpus Christi),
o recesso e, na Justiça Federal, a lista de feriados próprios para conferir. Toda linha sai com
[CONFERIR] na fonte e conferido_em vazio: quem confirma cada data no ato do tribunal é a
pessoa. Feriados estaduais e municipais e os atos do tribunal entram depois, com a fonte.

O validar confere o formato (cabeçalho, colunas, tipos, datas, vale_para), aponta fins de
semana na tabela, datas repetidas, linhas sem fonte ou sem conferência, e o que falta para o
calendário valer.

Códigos de saída: 0 ok; 1 erro (arquivo, coluna ou formato); 2 o validar achou pendências.
Só biblioteca padrão. Python 3.9 ou mais novo.
"""

import argparse
import datetime as dt
import os
import re
import sys
import unicodedata

TIPOS = (
    "feriado",
    "recesso",
    "suspensao",
    "expediente-reduzido",
    "indisponibilidade-programada",
    "indisponibilidade-certificada",
)
COLUNAS = ("data", "tipo", "descricao", "vale_para", "fonte", "conferido_em")


class Erro(Exception):
    pass


def normal(t):
    t = unicodedata.normalize("NFKD", str(t))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.strip().lower())


def pascoa(ano):
    """Domingo de Páscoa pelo cálculo gregoriano (algoritmo anônimo de Meeus)."""
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(ano, mes, dia)


def justica_do_tribunal(sigla):
    s = sigla.upper()
    if s.startswith("TRF") or s in ("JF", "JEF"):
        return "federal"
    if s.startswith("TRT") or s == "TST":
        return "trabalho"
    return "estadual"


def rascunho(tribunal, ano, cidade, justica):
    t = tribunal.upper()
    justica = justica or justica_do_tribunal(t)
    p = pascoa(ano)
    dia = dt.timedelta(days=1)
    linhas = []

    def add(ini, fim, tipo, desc, fonte):
        linhas.append((ini, fim, tipo, desc, fonte))

    lei_nacional = "lei federal dos feriados nacionais [CONFERIR]"
    ato = "ato do tribunal do ano [CONFERIR]"
    recesso_fonte = "CLT, art. 775-A [CONFERIR]" if justica == "trabalho" else "CPC, art. 220 [CONFERIR]"
    add(dt.date(ano, 1, 1), dt.date(ano, 1, 20), "recesso", "Recesso: prazos suspensos (fim do recesso do ano anterior)", recesso_fonte)
    add(dt.date(ano, 1, 1), dt.date(ano, 1, 1), "feriado", "Confraternização Universal", lei_nacional)
    add(p - 48 * dia, p - 47 * dia, "feriado", "Carnaval (segunda e terça)", ato)
    add(p - 46 * dia, p - 46 * dia, "expediente-reduzido", "Quarta-feira de cinzas (confirme o horário do expediente)", ato)
    add(p - 2 * dia, p - 2 * dia, "feriado", "Sexta-feira Santa", ato)
    add(dt.date(ano, 4, 21), dt.date(ano, 4, 21), "feriado", "Tiradentes", lei_nacional)
    add(dt.date(ano, 5, 1), dt.date(ano, 5, 1), "feriado", "Dia do Trabalho", lei_nacional)
    add(p + 60 * dia, p + 60 * dia, "feriado", "Corpus Christi", ato)
    add(dt.date(ano, 9, 7), dt.date(ano, 9, 7), "feriado", "Independência do Brasil", lei_nacional)
    add(dt.date(ano, 10, 12), dt.date(ano, 10, 12), "feriado", "Nossa Senhora Aparecida", lei_nacional)
    add(dt.date(ano, 11, 2), dt.date(ano, 11, 2), "feriado", "Finados", lei_nacional)
    add(dt.date(ano, 11, 15), dt.date(ano, 11, 15), "feriado", "Proclamação da República", lei_nacional)
    add(dt.date(ano, 11, 20), dt.date(ano, 11, 20), "feriado", "Dia Nacional de Zumbi e da Consciência Negra", lei_nacional)
    add(dt.date(ano, 12, 25), dt.date(ano, 12, 25), "feriado", "Natal", lei_nacional)
    add(dt.date(ano, 12, 20), dt.date(ano + 1, 1, 20), "recesso", "Recesso: prazos suspensos", recesso_fonte)
    if justica == "federal":
        jf = "lei de organização da Justiça Federal e portaria do tribunal [CONFERIR]"
        add(p - 4 * dia, p - 3 * dia, "feriado", "Semana Santa, feriado da Justiça Federal (quarta e quinta)", jf)
        add(dt.date(ano, 8, 11), dt.date(ano, 8, 11), "feriado", "Feriado da Justiça Federal (11 de agosto)", jf)
        add(dt.date(ano, 11, 1), dt.date(ano, 11, 1), "feriado", "Feriado da Justiça Federal (Todos os Santos)", jf)
        add(dt.date(ano, 12, 8), dt.date(ano, 12, 8), "feriado", "Feriado da Justiça Federal (Dia da Justiça)", jf)
        add(dt.date(ano, 12, 20), dt.date(ano + 1, 1, 6), "feriado", "Feriado da Justiça Federal no fim do ano (sem expediente)", jf)
        add(dt.date(ano, 1, 1), dt.date(ano, 1, 6), "feriado", "Feriado da Justiça Federal no começo do ano (sem expediente)", jf)
    linhas.sort(key=lambda x: (x[0], x[1]))

    def data_txt(ini, fim):
        return ini.isoformat() if ini == fim else "%s a %s" % (ini.isoformat(), fim.isoformat())

    cab = [
        "---",
        "documento: Calendário forense",
        "tribunal: %s" % t,
        "ano: %d" % ano,
        "cidade: %s" % (cidade or "[A PREENCHER]"),
        "conferido_em: [A PREENCHER]",
        "conferido_por: [A PREENCHER]",
        "treino: nao",
        "versao: 0.1",
        "dono: [A PREENCHER]",
        "---",
        "",
        "# Calendário forense · %s · %d" % (t, ano),
        "",
        "Rascunho gerado pela calendario-forense. Cada linha precisa ser conferida no ato do tribunal "
        "(portaria, resolução, calendário oficial) antes de valer: troque o `[CONFERIR]` da fonte pelo ato "
        "e preencha `conferido_em`. Faltam os feriados estaduais e os municipais de %s, os pontos facultativos "
        "que o tribunal adotar, as suspensões e os dias de expediente reduzido do ano." % (cidade or "[CIDADE DO JUÍZO]"),
        "",
        "Fins de semana não entram na tabela.",
        "",
        "| data | tipo | descricao | vale_para | fonte | conferido_em |",
        "|---|---|---|---|---|---|",
    ]
    corpo = [
        "| %s | %s | %s | %s | %s |  |" % (data_txt(i, f), tp, d, t, fo)
        for i, f, tp, d, fo in linhas
    ]
    corpo.append("| [A PREENCHER] | feriado | Feriado estadual de [ESTADO] | %s | lei estadual e ato do tribunal [CONFERIR] |  |" % t)
    corpo.append("| [A PREENCHER] | feriado | Feriado municipal de %s | %s | lei municipal e ato do tribunal [CONFERIR] |  |" % (cidade or "[CIDADE]", t))
    return "\n".join(cab + corpo) + "\n"


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            pass
    return bruto.decode("latin-1")


def ler_data(s):
    s = s.strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    raise ValueError(s)


def validar_arquivo(caminho, tribunal, ano):
    nome = os.path.basename(caminho)
    texto = ler_texto(caminho)
    linhas = texto.splitlines()
    pend = []
    erros = []
    info = []
    meta = {}
    if linhas and linhas[0].strip() == "---":
        for l in linhas[1:]:
            if l.strip() == "---":
                break
            m = re.match(r"\s*([A-Za-z0-9_\-]+)\s*:\s*(.*)$", l)
            if m:
                meta[m.group(1).lower()] = m.group(2).strip()
    for campo in ("tribunal", "ano", "conferido_em", "conferido_por", "treino"):
        if campo not in meta:
            erros.append("cabeçalho sem o campo %s" % campo)
        elif campo in ("conferido_em", "conferido_por") and (not meta[campo] or "A PREENCHER" in meta[campo].upper()):
            pend.append("cabeçalho: %s sem preencher (o calendário sai com o aviso 'calendário não conferido')" % campo)
    tribs = [x.strip().upper() for x in re.split(r"[,;]", meta.get("tribunal", "")) if x.strip()]
    if tribunal and tribunal.upper() not in tribs:
        erros.append("o cabeçalho diz tribunal %s, e a conferência pediu %s" % (meta.get("tribunal", "vazio"), tribunal.upper()))
    anos = [int(a) for a in re.findall(r"\d{4}", meta.get("ano", ""))]
    if ano and ano not in anos:
        erros.append("o cabeçalho diz ano %s, e a conferência pediu %d" % (meta.get("ano", "vazio"), ano))
    cab = None
    vistos = {}
    n_linhas = 0
    for num, l in enumerate(linhas, 1):
        if not l.strip().startswith("|"):
            if cab is not None and l.strip():
                cab = None if l.strip().startswith("#") else cab
            continue
        partes = [p.strip().replace("`", "") for p in l.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", p) or p == "" for p in partes):
            continue
        norm = [normal(p) for p in partes]
        if "data" in norm and "tipo" in norm:
            cab = norm
            faltam = [c for c in COLUNAS if c not in cab]
            if faltam:
                erros.append("linha %d: faltam as colunas %s" % (num, ", ".join(faltam)))
                cab = None
            continue
        if cab is None:
            continue
        partes = partes + [""] * (len(cab) - len(partes))
        cel = {c: partes[cab.index(c)] for c in COLUNAS}
        n_linhas += 1
        if "A PREENCHER" in cel["data"].upper():
            pend.append("linha %d: data a preencher (%s)" % (num, cel["descricao"]))
            continue
        m = re.fullmatch(r"(\S+)(?:\s+a\s+(\S+))?", cel["data"])
        try:
            ini = ler_data(m.group(1)) if m else None
            fim = ler_data(m.group(2)) if m and m.group(2) else ini
        except ValueError:
            ini = fim = None
        if ini is None:
            erros.append("linha %d: data '%s' fora do formato AAAA-MM-DD ou AAAA-MM-DD a AAAA-MM-DD" % (num, cel["data"]))
            continue
        if fim < ini:
            erros.append("linha %d: período termina antes de começar" % num)
        tipo = normal(cel["tipo"]).replace(" ", "-")
        if tipo not in TIPOS:
            erros.append("linha %d: tipo '%s' desconhecido (use %s)" % (num, cel["tipo"], ", ".join(TIPOS)))
        if not cel["vale_para"]:
            erros.append("linha %d: vale_para vazio (use todos ou as siglas)" % num)
        elif normal(cel["vale_para"]) != "todos":
            siglas = [x.strip().upper() for x in re.split(r"[,;]", cel["vale_para"]) if x.strip()]
            estranhas = [s for s in siglas if not re.fullmatch(r"[A-Z0-9]{2,8}", s)]
            if estranhas:
                erros.append("linha %d: vale_para com sigla estranha: %s" % (num, ", ".join(estranhas)))
        if not cel["fonte"] or "CONFERIR" in cel["fonte"].upper():
            pend.append("linha %d: %s %s sem fonte conferida" % (num, cel["data"], cel["descricao"]))
        if not cel["conferido_em"]:
            pend.append("linha %d: %s %s sem conferido_em" % (num, cel["data"], cel["descricao"]))
        if ini == fim and ini.weekday() >= 5 and tipo in ("feriado", "expediente-reduzido", "indisponibilidade-programada", "indisponibilidade-certificada"):
            info.append("linha %d: %s cai em fim de semana; não muda a conta (pode ficar como registro)" % (num, ini.isoformat()))
        if tipo == "indisponibilidade-certificada" and "certid" not in normal(cel["fonte"]):
            pend.append("linha %d: indisponibilidade certificada sem a certidão na fonte" % num)
        chave = (ini, fim, tipo, normal(cel["vale_para"]))
        if chave in vistos:
            pend.append("linha %d: repete a linha %d" % (num, vistos[chave]))
        vistos[chave] = num
    if n_linhas == 0:
        erros.append("não achei a tabela do calendário (colunas %s)" % " | ".join(COLUNAS))
    return nome, meta, erros, pend, info, n_linhas


def main():
    ap = argparse.ArgumentParser(description="Rascunho e conferência do calendário forense.")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("rascunho", help="gera o rascunho do ano para um tribunal")
    r.add_argument("--tribunal", required=True)
    r.add_argument("--ano", type=int, required=True)
    r.add_argument("--cidade")
    r.add_argument("--justica", choices=("estadual", "federal", "trabalho"))
    r.add_argument("--saida")
    v = sub.add_parser("validar", help="confere o formato e as pendências de um calendário")
    v.add_argument("caminho")
    v.add_argument("--tribunal")
    v.add_argument("--ano", type=int)
    args = ap.parse_args()
    try:
        if args.cmd == "rascunho":
            if not (1900 < args.ano < 2200):
                raise Erro("ano inválido: %d" % args.ano)
            texto = rascunho(args.tribunal, args.ano, args.cidade, args.justica)
            if args.saida:
                if os.path.exists(args.saida):
                    raise Erro("%s já existe: o rascunho não escreve por cima. Use outro nome ou confira o arquivo atual com 'validar'." % args.saida)
                os.makedirs(os.path.dirname(os.path.abspath(args.saida)) or ".", exist_ok=True)
                with open(args.saida, "w", encoding="utf-8") as f:
                    f.write(texto)
                print("Rascunho gravado em %s. Nenhuma linha vale antes de conferida no ato do tribunal." % args.saida)
            else:
                print(texto)
            return 0
        if args.cmd == "validar":
            if not os.path.exists(args.caminho):
                raise Erro("não encontrei %s" % args.caminho)
            if os.path.isdir(args.caminho):
                arquivos = [os.path.join(args.caminho, n) for n in sorted(os.listdir(args.caminho)) if n.lower().endswith(".md")]
                if not arquivos:
                    raise Erro("a pasta %s não tem calendário .md" % args.caminho)
            else:
                arquivos = [args.caminho]
            codigo = 0
            for arq in arquivos:
                nome, meta, erros, pend, info, n = validar_arquivo(arq, args.tribunal, args.ano)
                print("CALENDÁRIO %s · tribunal %s · ano %s · %d linhas" % (nome, meta.get("tribunal", "?"), meta.get("ano", "?"), n))
                if erros:
                    codigo = 1
                    print("ERROS (o script de conta recusa este arquivo):")
                    for e in erros:
                        print("  - %s" % e)
                if pend:
                    codigo = max(codigo, 2)
                    print("PENDÊNCIAS (a conta roda, com aviso):")
                    for p in pend:
                        print("  - %s" % p)
                if info:
                    print("INFORMAÇÕES:")
                    for i in info:
                        print("  - %s" % i)
                if not erros and not pend:
                    print("Sem pendências de formato. A conferência das datas no ato do tribunal continua com a pessoa.")
                print("")
            return codigo
        ap.print_help()
        return 1
    except Erro as ex:
        sys.stderr.write("ERRO: %s\n" % ex)
        return 1


if __name__ == "__main__":
    sys.exit(main())
