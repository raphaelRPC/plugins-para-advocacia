#!/usr/bin/env python3
"""Tira a marca [CONFERIR] só das citações verdes do registro (motor-juridico, conferir-citacoes).

Lê a peça e o registro da conferência (a tabela de citacoes.md, seção 4:
| # | Citação como está na peça | Fonte consultada | Data da consulta | Cor | O que foi feito |).
Para cada linha com Cor = verde, Fonte e Data preenchidas, procura na peça a citação exatamente
como está na coluna 2 e tira a marca [CONFERIR...] que vem logo depois dela. Nada mais muda.
Amarelo, vermelho, cinza e pendente ficam com a marca.

Só a tabela de citações do registro conta (outras tabelas, como as de dados, ficam de fora).
A seção interna "Antes de protocolar" (e o cabeçalho YAML) não é a peça: não muda e a marca
do checklist dela não conta como marca que sobrou.

Grava a peça nova em --saida (nunca por cima da original) e diz quantas marcas sobraram.
Peça com marca não vai para protocolo.

Uso:
  python3 tirar_marcas.py PECA.md REGISTRO.md --saida PECA-v2.md

Sai com código 1 quando falta arquivo, o registro não tem a tabela, ou --saida é a própria
peça. Sai com código 2 quando a peça nova ainda tem marcas (para o ciclo saber que não
pode ir a "conferida"). Só biblioteca padrão.
"""

import argparse
import os
import re
import sys
import unicodedata


# ---------- corte do que não é a peça (o mesmo da md_para_docx, da minutar-peca) ----------
# Copiado de propósito em cada script que lê a peça: a habilidade pode ir sozinha num zip.
RE_TITULO_INTERNO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_FIM_INTERNO = re.compile(r"^\s*<!--\s*fim:\s*antes de (protocolar|enviar)\s*-->\s*$", re.I)


def _minusculo_sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def cortar_interno(linhas):
    """Troca por linha vazia o que é controle interno do escritório e não é a peça.

    Sai: o cabeçalho YAML do topo (entre linhas ---); a seção interna (título de qualquer
    nível que começa com "Antes de protocolar" ou "Antes de enviar"), até o próximo título
    do mesmo nível ou maior, ou até a linha <!-- fim: antes de protocolar -->; e os
    comentários HTML. A numeração das linhas não muda.
    Devolve (linhas_da_peca, achou_secao_interna, quantas_linhas_internas).
    """
    linhas = list(linhas)
    interno = [False] * len(linhas)
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for j in range(0, i + 1):
                    interno[j] = True
                break
    achou, n_secao = False, 0
    i, em_codigo = 0, False
    while i < len(linhas):
        limpa = linhas[i].strip()
        if limpa.startswith("```"):
            em_codigo = not em_codigo
        m = RE_TITULO_INTERNO.match(limpa) if not em_codigo else None
        titulo = _minusculo_sem_acento(m.group(2)) if m else ""
        if m and titulo.startswith(("antes de protocolar", "antes de enviar")):
            achou = True
            nivel = len(m.group(1))
            interno[i] = True
            n_secao += 1
            j = i + 1
            while j < len(linhas):
                lj = linhas[j].strip()
                if RE_FIM_INTERNO.match(lj):
                    interno[j] = True
                    n_secao += 1
                    j += 1
                    break
                mj = RE_TITULO_INTERNO.match(lj)
                if mj and len(mj.group(1)) <= nivel:
                    break
                interno[j] = True
                n_secao += 1
                j += 1
            i = j
            continue
        i += 1
    dentro = False
    for i, linha in enumerate(linhas):
        if interno[i]:
            continue
        if dentro:
            interno[i] = True
            if "-->" in linha:
                dentro = False
            continue
        if "<!--" in linha:
            antes, _, depois = linha.partition("<!--")
            if "-->" in depois:
                linhas[i] = antes + depois.split("-->", 1)[1]
                if not linhas[i].strip():
                    interno[i] = True
            else:
                linhas[i] = antes
                dentro = True
                if not antes.strip():
                    interno[i] = True
    return [("" if interno[n] else l) for n, l in enumerate(linhas)], achou, n_secao


def erro(msg, codigo=1):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(codigo)


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


def norm(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.strip().lower()) if unicodedata.category(c) != "Mn")


ABREVIATURAS = {"rel", "min", "des", "desa", "desemb", "dr", "dra", "juiz", "juíza", "nº", "n", "art", "arts", "p", "pp",
               "ed", "fls", "fl", "inc", "al", "sr", "sra", "prof", "profa", "cf", "dj", "dje", "julg", "publ", "j", "v",
               "rev", "conv", "proc", "trib", "reg", "conf"}


def tem_quebra(texto):
    """Fim de frase ou outra marca no meio do trecho (abreviatura como Rel. e Min. não conta)."""
    if "[" in texto:
        return True
    for m in re.finditer(r"([\wÀ-ÿº]+)?[.;]\s+[A-ZÁÉÍÓÚÂÊÔ]", texto):
        antes = (m.group(1) or "").lower()
        if m.group(0)[len(m.group(1) or "")] == ";":
            return True
        if antes in ABREVIATURAS or len(antes) <= 2:
            continue
        return True
    return False


def tabelas(texto):
    """Cada tabela markdown do texto: uma lista de linhas seguidas que começam com '|'."""
    blocos, atual = [], []
    for l in texto.splitlines():
        if l.strip().startswith("|"):
            atual.append(l)
        else:
            if atual:
                blocos.append(atual)
            atual = []
    if atual:
        blocos.append(atual)
    return blocos


def ler_registro(texto):
    """Lê só a tabela de citações do registro (colunas 'Citação como está na peça' e 'Cor').

    As outras tabelas do registro (dados, documentos, datas da conferir-peca) ficam de fora.
    """
    cab = None
    regs = []
    for bloco in tabelas(texto):
        cel0 = [norm(c) for c in bloco[0].strip().strip("|").split("|")]
        if not (any("citacao" in c for c in cel0) and any(c == "cor" for c in cel0)):
            continue
        if cab is None:
            cab = cel0
        elif cel0 != cab:
            continue
        for l in bloco[1:]:
            cel = [c.strip() for c in l.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cel if c):
                continue
            if len(cel) < len(cab):
                cel += [""] * (len(cab) - len(cel))
            regs.append(dict(zip(cab, cel)))
    if cab is None:
        erro("o registro não tem a tabela com as colunas 'Citação como está na peça' e 'Cor' (citacoes.md, seção 4).")
    col_cit = next(c for c in cab if "citacao" in c)
    col_fonte = next((c for c in cab if "fonte" in c), None)
    col_data = next((c for c in cab if "data" in c), None)
    return regs, col_cit, col_fonte, col_data


def main():
    ap = argparse.ArgumentParser(description="Tira a marca só das citações verdes do registro.")
    ap.add_argument("peca")
    ap.add_argument("registro")
    ap.add_argument("--saida", required=True, help="a peça nova (nunca a mesma da entrada)")
    a = ap.parse_args()
    if os.path.abspath(a.saida) == os.path.abspath(a.peca):
        erro("--saida não pode ser a própria peça. Grave como nova versão (minutas/<peca>-v<n+1>.md).")
    peca = ler(a.peca)
    # a seção interna "Antes de protocolar" (e o cabeçalho YAML) não é a peça: nada muda lá
    # e a marca [CONFERIR] do checklist dela não conta como marca que sobrou
    linhas_orig = peca.split("\n")
    linhas_peca, achou_interno, _ = cortar_interno(linhas_orig)
    eh_peca = [bool(lp.strip()) for lp in linhas_peca]
    regs, col_cit, col_fonte, col_data = ler_registro(ler(a.registro))
    if not regs:
        erro("o registro não tem nenhuma linha de citação.")

    tiradas, nao_achadas, sem_fonte, mantidas = [], [], [], []
    for r in regs:
        cit = re.sub(r"\s*\[CONFERIR[^\]]*\]\s*$", "", r.get(col_cit, "")).strip()
        cor = norm(r.get("cor", ""))
        if not cit:
            continue
        if cit.startswith(("\"", "“")):
            # aspas: a marca fica na citação de onde o trecho vem; nada a tirar aqui
            if cor != "verde":
                mantidas.append((cit[:60], cor or "sem cor"))
            continue
        if cor != "verde":
            mantidas.append((cit, cor or "sem cor"))
            continue
        if (col_fonte and not r.get(col_fonte, "").strip()) or (col_data and not r.get(col_data, "").strip()):
            sem_fonte.append(cit)
            continue
        padrao = re.compile(re.escape(cit) + r"([^\[\]\n]{0,200}?)\s*\[CONFERIR[^\]]*\]")

        def tira(m):
            meio = m.group(1)
            if tem_quebra(meio):
                return m.group(0)  # a marca é de outra frase: não mexe
            return cit + meio

        n = 0
        for k, lk in enumerate(linhas_orig):
            if not eh_peca[k]:
                continue
            nova = padrao.sub(tira, lk)
            if nova != lk:
                n += len(padrao.findall(lk)) - len(padrao.findall(nova))
                linhas_orig[k] = nova
        corpo = "\n".join(l for k, l in enumerate(linhas_orig) if eh_peca[k])
        if n:
            tiradas.append((cit, n))
        elif cit in corpo:
            tiradas.append((cit, 0))
        else:
            nao_achadas.append(cit)

    peca = "\n".join(linhas_orig)
    restantes = [m for k, l in enumerate(linhas_orig) if eh_peca[k] for m in re.findall(r"\[CONFERIR[^\]]*\]", l)]
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(peca)

    print("Peça nova: %s" % a.saida)
    print("Marcas tiradas (citações verdes): %d" % sum(n for _, n in tiradas))
    for cit, n in tiradas:
        print("  - %s%s" % (cit, "" if n else " (já estava sem marca)"))
    if mantidas:
        print("Ficaram com a marca (não verdes): %d" % len(mantidas))
        for cit, cor in mantidas:
            print("  - %s: %s" % (cit, cor))
    if sem_fonte:
        print("Verdes sem fonte ou data no registro (a marca ficou): %d" % len(sem_fonte))
        for cit in sem_fonte:
            print("  - %s" % cit)
    if nao_achadas:
        print("Não achei na peça exatamente como está no registro (a marca ficou): %d" % len(nao_achadas))
        for cit in nao_achadas:
            print("  - %s" % cit)
    if achou_interno:
        print("Seção interna \"Antes de protocolar\": fica como está e não conta (não é a peça).")
    print("Marcas que sobraram na peça: %d" % len(restantes))
    if restantes:
        print("A peça ainda não vai para protocolo.")
        sys.exit(2)
    print("Nenhuma marca na peça. As citações estão no registro da conferência.")


if __name__ == "__main__":
    main()
