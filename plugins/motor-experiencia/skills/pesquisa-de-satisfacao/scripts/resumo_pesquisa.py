#!/usr/bin/env python3
"""Resumo do mês da pesquisa de satisfação (motor-experiencia).

Lê o registro do mês (escritorio/07-operacao/experiencia/pesquisas/AAAA-MM.md, com a tabela
do modelo, ou o mesmo conteúdo em .csv) e mostra:
  - quantas pesquisas foram enviadas e quantas responderam;
  - média, mediana e faixas das notas (0 a 6, 7 e 8, 9 e 10);
  - as notas por momento da pesquisa;
  - quem deu nota baixa e se já teve retorno pessoal;
  - quantos comentários há para ler (o texto não é impresso).
Com --carteira, cruza com a carteira.csv: nota baixa sem reclamação registrada, nota da
carteira diferente da última resposta e pesquisa enviada a quem tem
pediu_para_nao_receber = sim, respondida ou não. Para achar essas pesquisas, lê o
registro do mês e também, o que existir: a fila (fila/AAAA-MM-DD/*-pesquisa-de-satisfacao.md
do mês, com status enviado; pendente ou aprovado vira aviso para não aprovar) e o
histórico de cada cliente (clientes/<codigo>/historico.md, linha do mês com "pesquisa"
dita pelo escritório). Pesquisa enviada antes do pedido registrado no histórico
("não receber", "parar de mandar") não é apontada.

Uso:
  python3 resumo_pesquisa.py PESQUISA-DO-MES.md [--carteira carteira.csv] [--nota-baixa 6]
                             [--fila PASTA] [--clientes PASTA]

--fila e --clientes têm como padrão as pastas fila/ e clientes/ ao lado da carteira.
O mês é o do nome do registro (AAAA-MM.md).

Colunas obrigatórias: data, codigo, momento, nota. Opcionais: o_que_ajudou, o_que_melhorar,
retorno, situacao. Leitura robusta: tabela markdown ou csv com vírgula ou ponto e vírgula,
com ou sem BOM, nomes de coluna sem diferenciar maiúscula e acento, datas AAAA-MM-DD ou
DD/MM/AAAA. Sai com código 1 e mensagem clara quando falta o arquivo, falta coluna
obrigatória ou o registro não tem nenhuma linha.
"""

import argparse
import csv
import io
import os
import re
import statistics
import sys
import unicodedata
from datetime import datetime

OBRIGATORIAS = ["data", "codigo", "momento", "nota"]
SIM = {"sim", "s", "x", "yes", "true", "1"}


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def norm_coluna(n):
    return sem_acento(n.strip().strip('"').strip("`").lower()).replace(" ", "_").replace("-", "_")


def norm_opcao(v):
    return "-".join(sem_acento((v or "").strip().lower()).replace("_", " ").split())


def ler_texto(caminho, rotulo):
    if not os.path.isfile(caminho):
        erro("não encontrei %s em '%s'." % (rotulo, caminho))
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod).lstrip("﻿")
        except UnicodeDecodeError:
            continue


def ler_csv(texto):
    linhas = [l for l in texto.splitlines() if l.strip()]
    if not linhas:
        return [], []
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cab = [norm_coluna(c) for c in next(leitor)]
    regs = []
    for linha in leitor:
        if any(v.strip() for v in linha):
            valores = [v.strip() for v in linha] + [""] * (len(cab) - len(linha))
            regs.append(dict(zip(cab, valores)))
    return cab, regs


def ler_tabela_md(texto):
    """Primeira tabela markdown que tenha as colunas obrigatórias."""
    linhas = texto.splitlines()
    i = 0
    melhor = ([], [])
    while i < len(linhas):
        l = linhas[i].strip()
        if l.startswith("|") and i + 1 < len(linhas) and set(linhas[i + 1].replace("|", "").strip()) <= set("-: ") \
                and linhas[i + 1].strip().startswith("|"):
            cab = [norm_coluna(c) for c in l.strip("|").split("|")]
            regs = []
            i += 2
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                cel = [c.strip() for c in linhas[i].strip().strip("|").split("|")]
                cel += [""] * (len(cab) - len(cel))
                if any(cel):
                    regs.append(dict(zip(cab, cel)))
                i += 1
            if all(c in cab for c in OBRIGATORIAS):
                return cab, regs
            if not melhor[0]:
                melhor = (cab, regs)
            continue
        i += 1
    return melhor


def ler_data(v):
    v = (v or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def frontmatter(texto):
    linhas = texto.splitlines()
    campos = {}
    if not linhas or linhas[0].strip() != "---":
        return campos
    for linha in linhas[1:]:
        if linha.strip() == "---":
            break
        if ":" in linha:
            k, v = linha.split(":", 1)
            campos[k.strip().lower()] = v.split("#", 1)[0].strip()
    return campos


def pesquisas_na_fila(pasta, mes):
    """{codigo: [(data, status)]} dos rascunhos de pesquisa na fila do mês."""
    achados = {}
    if not pasta or not os.path.isdir(pasta):
        return None
    for dia in sorted(os.listdir(pasta)):
        if mes and not dia.startswith(mes):
            continue
        sub = os.path.join(pasta, dia)
        if not os.path.isdir(sub):
            continue
        for nome in sorted(os.listdir(sub)):
            if not (nome.endswith(".md") and "pesquisa" in nome):
                continue
            with open(os.path.join(sub, nome), "rb") as f:
                bruto = f.read()
            campos = frontmatter(bruto.decode("utf-8", errors="replace").lstrip("\ufeff"))
            if "pesquisa" not in norm_opcao(campos.get("tipo", "")) and "pesquisa" not in nome:
                continue
            cod = (campos.get("codigo") or "").strip().upper()
            if not cod:
                m = re.search(r"C-\d{4}-\d{4}(-\d+)?", nome, re.I)
                cod = m.group(0).upper() if m else ""
            if cod:
                achados.setdefault(cod, []).append((ler_data(dia[:10]), norm_opcao(campos.get("status", ""))))
    return achados


def historico(pasta, cod):
    """(linhas de pesquisa enviada [(data)], data do pedido para não receber) do historico.md."""
    caminho = os.path.join(pasta, cod, "historico.md") if pasta else ""
    if not caminho or not os.path.isfile(caminho):
        return None, None
    with open(caminho, "rb") as f:
        texto = f.read().decode("utf-8", errors="replace")
    enviadas, pedido = [], None
    for linha in texto.splitlines():
        s = linha.strip()
        if not s.startswith("|"):
            continue
        cel = [c.strip() for c in s.strip("|").split("|")]
        if len(cel) < 4:
            continue
        d = ler_data(cel[0][:10])
        if not d:
            continue
        quem, dito = norm_opcao(cel[2]), sem_acento(" ".join(cel[3:]).lower())
        if re.search(r"nao (quer )?receber|parar de (mandar|enviar|receber)|pediu para (parar|nao)", dito):
            pedido = d if pedido is None else min(pedido, d)
        elif "pesquisa" in dito and quem != "cliente" and norm_opcao(cel[1]) != "trabalho-do-escritorio":
            enviadas.append(d)
    return enviadas, pedido


def numero(x):
    if x is None:
        return "-"
    return str(int(x)) if float(x) == int(x) else ("%.1f" % x).replace(".", ",")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Resumo do mês da pesquisa de satisfação.")
    ap.add_argument("registro", help="pesquisas/AAAA-MM.md (ou .csv)")
    ap.add_argument("--carteira", help="carteira.csv, para cruzar notas baixas e reclamações")
    ap.add_argument("--nota-baixa", type=float, default=6, help="o campo nota_baixa da ficha: nota até a qual pede retorno pessoal (padrão 6)")
    ap.add_argument("--fila", help="pasta fila/ da experiência (padrão: ao lado da carteira)")
    ap.add_argument("--clientes", help="pasta clientes/ (padrão: ao lado da carteira)")
    a = ap.parse_args(argv)

    texto = ler_texto(a.registro, "o registro da pesquisa")
    if a.registro.lower().endswith(".csv"):
        cab, regs = ler_csv(texto)
    else:
        cab, regs = ler_tabela_md(texto)
    if not cab:
        erro("não achei nenhuma tabela em '%s'. O modelo está em assets/pesquisa-modelo.md." % a.registro)
    faltam = [c for c in OBRIGATORIAS if c not in cab]
    if faltam:
        erro("o registro não tem a(s) coluna(s) obrigatória(s): %s. Colunas lidas: %s."
             % (", ".join(faltam), ", ".join(cab)))
    regs = [r for r in regs if (r.get("codigo") or "").strip() and not (r.get("codigo") or "").startswith("[")]
    if not regs:
        erro("o registro '%s' não tem nenhuma pesquisa (só a linha de títulos)." % a.registro)

    avisos = []
    respostas = []
    for n, r in enumerate(regs, start=1):
        if not ler_data(r.get("data")):
            avisos.append("linha %d (%s): data '%s' não lida" % (n, r.get("codigo"), r.get("data")))
        nota_txt = (r.get("nota") or "").replace(",", ".").strip()
        r["_nota"] = None
        if nota_txt:
            try:
                r["_nota"] = float(nota_txt)
                if not 0 <= r["_nota"] <= 10:
                    avisos.append("linha %d (%s): nota %s fora de 0 a 10" % (n, r.get("codigo"), nota_txt))
                    r["_nota"] = None
            except ValueError:
                avisos.append("linha %d (%s): nota '%s' não é número" % (n, r.get("codigo"), nota_txt))
        r["_momento"] = norm_opcao(r.get("momento")) or "(sem momento)"
        if r["_nota"] is not None:
            respostas.append(r)

    notas = [r["_nota"] for r in respostas]
    out = []
    add = out.append
    add("# Resumo da pesquisa de satisfação · %s" % os.path.splitext(os.path.basename(a.registro))[0])
    add("")
    add("Uso interno. Os comentários não são impressos aqui: leia no registro.")
    add("")
    add("| Medida | Valor |")
    add("|---|---|")
    add("| Pesquisas enviadas | %d |" % len(regs))
    add("| Responderam com nota | %d (%d%%) |" % (len(respostas), round(100.0 * len(respostas) / len(regs))))
    if notas:
        add("| Média | %s |" % numero(round(sum(notas) / len(notas), 1)))
        add("| Mediana | %s |" % numero(statistics.median(notas)))
        add("| De 0 a %s | %d |" % (numero(a.nota_baixa), sum(1 for x in notas if x <= a.nota_baixa)))
        add("| Acima de %s até 8 | %d |" % (numero(a.nota_baixa), sum(1 for x in notas if a.nota_baixa < x <= 8)))
        add("| 9 e 10 | %d |" % sum(1 for x in notas if x > 8))
    com_coment = sum(1 for r in regs if (r.get("o_que_ajudou") or "").strip() or (r.get("o_que_melhorar") or "").strip())
    add("| Respostas com comentário para ler | %d |" % com_coment)
    add("")
    if respostas:
        add("## Por momento")
        add("")
        add("| Momento | Respostas | Média |")
        add("|---|---|---|")
        momentos = {}
        for r in respostas:
            momentos.setdefault(r["_momento"], []).append(r["_nota"])
        for m, ns in sorted(momentos.items()):
            add("| %s | %d | %s |" % (m, len(ns), numero(round(sum(ns) / len(ns), 1))))
        add("")

    baixas = [r for r in respostas if r["_nota"] <= a.nota_baixa]
    add("## Notas baixas (até %s): retorno pessoal" % numero(a.nota_baixa))
    add("")
    if baixas:
        for r in baixas:
            feito = (r.get("retorno") or "").strip()
            add("- %s · %s · nota %s · %s" % (r.get("codigo"), r["_momento"], numero(r["_nota"]),
                                             ("retorno: " + feito) if feito else "SEM RETORNO PESSOAL AINDA"))
    else:
        add("Nenhuma.")
    add("")

    if a.carteira:
        ctexto = ler_texto(a.carteira, "a carteira")
        ccab, cregs = ler_csv(ctexto)
        if "codigo" not in ccab:
            erro("a carteira '%s' não tem a coluna codigo." % a.carteira)
        carteira = {r["codigo"].strip().upper(): r for r in cregs if r.get("codigo")}
        add("## Cruzamento com a carteira")
        add("")
        achou = False
        ultima = {}
        for r in sorted(respostas, key=lambda r: (ler_data(r.get("data")) or datetime.min.date())):
            ultima[r["codigo"].strip().upper()] = r
        for cod, r in ultima.items():
            c = carteira.get(cod)
            if c is None:
                add("- %s respondeu, mas não está na carteira" % cod)
                achou = True
                continue
            if r["_nota"] <= a.nota_baixa and norm_opcao(c.get("reclamacao_aberta")) not in SIM:
                add("- %s: nota %s e nenhuma reclamação aberta na carteira; confirme se o retorno pessoal "
                    "virou registro em reclamacao-e-recuperacao" % (cod, numero(r["_nota"])))
                achou = True
            nota_cart = (c.get("satisfacao") or "").replace(",", ".").strip()
            try:
                diferente = nota_cart == "" or float(nota_cart) != r["_nota"]
            except ValueError:
                diferente = True
            if "satisfacao" in ccab and diferente:
                add("- %s: a coluna satisfacao da carteira (%s) não é a última nota (%s)"
                    % (cod, nota_cart or "vazia", numero(r["_nota"])))
                achou = True
        # Pesquisa para quem pediu para não receber: respondida ou não, pelo registro, pela fila e pelo histórico.
        base = os.path.dirname(os.path.abspath(a.carteira))
        pasta_fila = a.fila or os.path.join(base, "fila")
        pasta_clientes = a.clientes or os.path.join(base, "clientes")
        mes = os.path.splitext(os.path.basename(a.registro))[0][:7]
        mes = mes if re.fullmatch(r"\d{4}-\d{2}", mes) else ""
        fila = pesquisas_na_fila(pasta_fila, mes)
        fontes = ["registro do mês"]
        if fila is not None:
            fontes.append("fila")
        if os.path.isdir(pasta_clientes):
            fontes.append("histórico")
        pediram = [cod for cod, c in carteira.items() if norm_opcao(c.get("pediu_para_nao_receber")) in SIM]
        for cod in sorted(pediram):
            env_hist, pedido = historico(pasta_clientes, cod)
            envios = []
            for r in regs:
                if (r.get("codigo") or "").strip().upper() == cod:
                    envios.append((ler_data(r.get("data")), "registro" + (", respondeu" if r.get("_nota") is not None else ", sem resposta")))
            for d, st in (fila or {}).get(cod, []):
                if st == "enviado":
                    envios.append((d, "fila, enviado"))
                elif st in ("pendente", "aprovado"):
                    add("- %s: pediu para não receber e tem pesquisa na fila (%s, status %s): não aprovar nem enviar"
                        % (cod, d.isoformat() if d else "?", st))
                    achou = True
            for d in env_hist or []:
                if not mes or d.strftime("%Y-%m") == mes:
                    envios.append((d, "histórico"))
            depois = [(d, o) for d, o in envios if not (pedido and d and d < pedido)]
            if depois:
                quando = sorted({d.isoformat() for d, o in depois if d}) or ["sem data"]
                add("- %s: pediu_para_nao_receber = sim e recebeu pesquisa (%s; fonte: %s)%s; confira e registre o cuidado"
                    % (cod, ", ".join(quando), ", ".join(sorted({o for d, o in depois})),
                       (" depois do pedido de %s" % pedido.isoformat()) if pedido else ""))
                achou = True
        add("")
        add("Fontes lidas para pesquisa a quem pediu para não receber: %s." % ", ".join(fontes))
        if not achou:
            add("Nada a acertar na carteira.")
        add("")

    if avisos:
        add("## Avisos")
        add("")
        for av in avisos:
            add("- " + av)
        add("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
