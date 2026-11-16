#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
comparar_leituras.py · a dupla conferência de um lote de prazos, linha por linha.

  python3 comparar_leituras.py modelo --prazos prazos.csv [--publicacoes publicacoes.csv] --saida <leitura.csv>
      Gera a planilha da leitura cega: uma linha por prazo sugerido, com o caso e o caminho do teor,
      e as colunas que a pessoa preenche. Não leva a sugestão da IA (dias, datas, providência).

  python3 comparar_leituras.py comparar <leitura-1.csv> <leitura-2.csv> [--prazos prazos.csv] [--saida <relatorio.md>]
      Compara as duas leituras linha por linha (o que pede, dias, fonte, rito, dobro, data contada) e,
      com --prazos, a leitura combinada contra a sugestão da IA.

Códigos de saída: 0 tudo bate; 1 erro (arquivo ou coluna que falta); 2 há linhas que divergem ou
que as pessoas precisam confirmar. Lê vírgula ou ponto e vírgula, com ou sem BOM, cp1252.
Só biblioteca padrão. Python 3.9 ou mais novo.
"""

import argparse
import csv
import io
import os
import re
import sys
import unicodedata

COLUNAS_LEITURA = ["id", "codigo_caso", "cliente_curto", "publicacao_id", "teor", "o_que_pede", "dias", "fonte_dos_dias", "rito", "dobro", "data_contada"]
PREENCHE = ["o_que_pede", "dias", "fonte_dos_dias", "rito", "dobro", "data_contada"]


class Erro(Exception):
    pass


def normal(t):
    t = unicodedata.normalize("NFKD", str(t or ""))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.strip().lower())


def ler_csv(caminho, obrigatorias, nome):
    if not os.path.isfile(caminho):
        raise Erro("arquivo não encontrado: %s" % caminho)
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if texto is None:
        texto = bruto.decode("latin-1")
    if not texto.strip():
        raise Erro("%s está vazio: %s" % (nome, caminho))
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    mapa = {c: normal(c).replace(" ", "_") for c in (leitor.fieldnames or [])}
    faltam = [c for c in obrigatorias if c not in mapa.values()]
    if faltam:
        raise Erro("%s (%s) sem as colunas obrigatórias: %s." % (nome, caminho, ", ".join(faltam)))
    linhas = [{mapa[k]: (v or "").strip() for k, v in l.items() if k in mapa} for l in leitor]
    if not linhas:
        raise Erro("%s não tem nenhuma linha: %s" % (nome, caminho))
    return linhas


def sim_nao(v):
    n = normal(v)
    if n in ("sim", "s", "yes", "y", "dobro", "em dobro"):
        return "sim"
    if n in ("nao", "n", "no", "sem dobro", "-"):
        return "nao"
    return ""


def rito_normal(v):
    n = normal(v).replace(" ", "-")
    trocas = {"trabalho": "trabalhista", "jef": "juizado-federal", "jec": "juizado-civel"}
    return trocas.get(n, n)


def data_normal(v):
    s = (v or "").strip()
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1)))
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3)))
    return normal(s)


def modelo(args):
    prazos = ler_csv(args.prazos, ["id", "tipo", "status", "publicacao_id", "codigo_caso"], "prazos.csv")
    teor = {}
    if args.publicacoes:
        for p in ler_csv(args.publicacoes, ["id"], "publicacoes.csv"):
            teor[p["id"]] = p.get("teor", "")
    linhas = [l for l in prazos if normal(l.get("tipo")) == "prazo" and normal(l.get("status")) == "sugerido"]
    if not linhas:
        raise Erro("prazos.csv não tem nenhum prazo sugerido para conferir.")
    if os.path.exists(args.saida):
        raise Erro("%s já existe: a planilha da leitura não é escrita por cima. Use outro nome." % args.saida)
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)) or ".", exist_ok=True)
    with open(args.saida, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLUNAS_LEITURA)
        for l in sorted(linhas, key=lambda x: x.get("id", "")):
            w.writerow([l.get("id", ""), l.get("codigo_caso", ""), l.get("cliente_curto", ""), l.get("publicacao_id", ""), teor.get(l.get("publicacao_id", ""), "")] + [""] * len(PREENCHE))
    print("Planilha da leitura cega gravada em %s (%d prazos). Faça uma cópia para cada pessoa; cada uma preenche a sua sem ver a outra." % (args.saida, len(linhas)))
    return 0


def comparar(args):
    obrig = ["id", "o_que_pede", "dias", "rito", "dobro"]
    l1 = {l["id"]: l for l in ler_csv(args.leitura1, obrig, "leitura 1")}
    l2 = {l["id"]: l for l in ler_csv(args.leitura2, obrig, "leitura 2")}
    sug = {}
    if args.prazos:
        sug = {l["id"]: l for l in ler_csv(args.prazos, ["id", "dias", "rito", "em_dobro"], "prazos.csv")}
    ids = sorted(set(l1) | set(l2))
    linhas = []
    for i in ids:
        a, b = l1.get(i), l2.get(i)
        item = {"id": i, "caso": (a or b).get("codigo_caso", ""), "diverge": [], "confirmar": [], "corrige_ia": []}
        if a is None or b is None:
            item["diverge"].append("sem a leitura %d" % (1 if a is None else 2))
            linhas.append(item)
            continue
        vazios = [c for c in ("o_que_pede", "dias", "rito", "dobro") if not a.get(c) or not b.get(c)]
        if vazios:
            item["diverge"].append("não preenchido: %s" % ", ".join(vazios))
        if a.get("dias") and b.get("dias") and a["dias"].strip() != b["dias"].strip():
            item["diverge"].append("dias: %s e %s" % (a["dias"], b["dias"]))
        if a.get("rito") and b.get("rito") and rito_normal(a["rito"]) != rito_normal(b["rito"]):
            item["diverge"].append("rito: %s e %s" % (a["rito"], b["rito"]))
        if a.get("dobro") and b.get("dobro") and sim_nao(a["dobro"]) != sim_nao(b["dobro"]):
            item["diverge"].append("dobro: %s e %s" % (a["dobro"], b["dobro"]))
        if a.get("dobro") and not sim_nao(a["dobro"]) or b.get("dobro") and not sim_nao(b["dobro"]):
            item["confirmar"].append("dobro respondido sem sim ou não")
        fa, fb = normal(a.get("fonte_dos_dias")), normal(b.get("fonte_dos_dias"))
        if fa and fb and fa != fb:
            item["confirmar"].append("fonte dos dias diferente: %s e %s" % (a.get("fonte_dos_dias"), b.get("fonte_dos_dias")))
        if a.get("o_que_pede") and b.get("o_que_pede") and normal(a["o_que_pede"]) != normal(b["o_que_pede"]):
            item["confirmar"].append("o que pede, em palavras diferentes: '%s' e '%s' (as duas pessoas confirmam se é o mesmo ato)" % (a["o_que_pede"], b["o_que_pede"]))
        da, db = data_normal(a.get("data_contada")), data_normal(b.get("data_contada"))
        if da and db and da != db:
            item["diverge"].append("data contada: %s e %s" % (da, db))
        s = sug.get(i)
        if s and not item["diverge"]:
            if a.get("dias") and s.get("dias") and a["dias"].strip() != s["dias"].strip():
                item["corrige_ia"].append("dias: IA %s, leituras %s" % (s["dias"], a["dias"]))
            if a.get("rito") and s.get("rito") and rito_normal(a["rito"]) != rito_normal(s["rito"]):
                item["corrige_ia"].append("rito: IA %s, leituras %s" % (s["rito"], a["rito"]))
            if a.get("dobro") and sim_nao(a["dobro"]) and sim_nao(a["dobro"]) != (sim_nao(s.get("em_dobro")) or "nao"):
                item["corrige_ia"].append("dobro: IA %s, leituras %s" % (s.get("em_dobro") or "nao", a["dobro"]))
        linhas.append(item)

    def situacao(it):
        if it["diverge"]:
            return "diverge"
        if it["confirmar"]:
            return "confirmar"
        if it["corrige_ia"]:
            return "bate, corrige a IA"
        return "bate"

    R = ["DUPLA CONFERÊNCIA DO LOTE · %d prazos" % len(linhas)]
    cont = {}
    for it in linhas:
        cont[situacao(it)] = cont.get(situacao(it), 0) + 1
    R.append("Resumo: " + " · ".join("%s %d" % (k, v) for k, v in sorted(cont.items())))
    R.append("")
    R.append("| id | caso | situação | detalhe |")
    R.append("|---|---|---|---|")
    for it in linhas:
        det = "; ".join(it["diverge"] + it["confirmar"] + it["corrige_ia"]) or "as duas leituras iguais"
        R.append("| %s | %s | %s | %s |" % (it["id"], it["caso"], situacao(it), det))
    R.append("")
    sep = [it for it in linhas if situacao(it) != "bate"]
    if sep:
        R.append("SEPARADAS (não viram conferido neste lote)")
        for it in sep:
            R.append("  - %s %s: %s" % (it["id"], it["caso"], situacao(it)))
        R.append("")
    R.append("Só as linhas 'bate' seguem para as duas contas do script (calcular_prazo.py --csv). Nenhum status muda por este script.")
    rel = "\n".join(R)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)) or ".", exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(rel + "\n")
        print("Relatório gravado em %s" % args.saida)
    print(rel)
    return 0 if not sep else 2


def main():
    ap = argparse.ArgumentParser(description="Dupla conferência de um lote de prazos, linha por linha.")
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("modelo")
    m.add_argument("--prazos", required=True)
    m.add_argument("--publicacoes")
    m.add_argument("--saida", required=True)
    c = sub.add_parser("comparar")
    c.add_argument("leitura1")
    c.add_argument("leitura2")
    c.add_argument("--prazos")
    c.add_argument("--saida")
    args = ap.parse_args()
    try:
        if args.cmd == "modelo":
            return modelo(args)
        if args.cmd == "comparar":
            return comparar(args)
        ap.print_help()
        return 1
    except Erro as ex:
        sys.stderr.write("ERRO: %s\n" % ex)
        return 1


if __name__ == "__main__":
    sys.exit(main())
