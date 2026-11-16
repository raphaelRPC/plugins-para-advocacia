#!/usr/bin/env python3
"""Índice do lote de documentos de um caso (motor-juridico, dossie-do-caso).

Lê a pasta com os documentos do caso (PDF, DOCX, imagens, texto) e monta ou atualiza
o controle de leitura: um código por documento (D1, D2..., sem zero à esquerda), tipo, páginas, tamanho,
duplicados e a situação da leitura. Serve para lotes grandes: a habilidade lê o lote
em etapas e este controle diz o que já foi lido e o que falta.

Só biblioteca padrão (Python 3.9+). Não abre o conteúdo dos documentos além do
necessário para contar páginas de PDF e achar duplicados. Não apaga nada.

Uso:
  python3 indice_do_lote.py PASTA_DOS_DOCUMENTOS CAMINHO/controle-de-leitura.csv [opções]

Opções:
  --fichas PASTA            pasta das fichas por documento (<doc>.md); a situação e as
                            páginas lidas de cada ficha passam para o controle
  --marcar DOC=SITUACAO[:PAGINAS]
                            muda a situação de um documento à mão (pode repetir).
                            Situações: a-ler, lido, lido-em-parte, ilegivel, duplicado,
                            fora-do-caso
  --paginas-por-etapa N     tamanho da próxima etapa de leitura, em páginas (padrão 60)
  --prefixo LETRA           prefixo do código dos documentos (padrão D)
  --codigo-do-nome          usa o código que já está no começo do nome do arquivo
                            (d1-carta.pdf vira D1, doc-07.pdf vira DOC7); sem código no
                            nome, ou código repetido, segue a numeração sequencial
  --so-mostrar              não grava o controle, só mostra o resumo

Sai com código 1 e mensagem clara quando a pasta não existe, quando não há nenhum
documento nela ou quando o controle existente não tem as colunas obrigatórias.
"""
import argparse
import csv
import hashlib
import io
import re
import sys
import unicodedata
from pathlib import Path

COLUNAS = ["doc", "arquivo", "tipo", "paginas", "tamanho_kb", "hash", "situacao",
           "paginas_lidas", "ficha", "observacao"]
OBRIGATORIAS = ["doc", "arquivo", "situacao"]
SITUACOES = ["a-ler", "lido", "lido-em-parte", "ilegivel", "duplicado", "fora-do-caso"]
TIPOS = {
    ".pdf": "pdf", ".docx": "docx", ".doc": "doc", ".odt": "odt", ".rtf": "texto",
    ".txt": "texto", ".md": "texto", ".html": "texto", ".htm": "texto", ".eml": "email",
    ".jpg": "imagem", ".jpeg": "imagem", ".png": "imagem", ".heic": "imagem",
    ".tif": "imagem", ".tiff": "imagem", ".webp": "imagem",
    ".mp3": "audio", ".m4a": "audio", ".ogg": "audio", ".opus": "audio", ".wav": "audio",
    ".mp4": "video", ".mov": "video", ".xlsx": "planilha", ".xls": "planilha", ".csv": "planilha",
}
IGNORAR = {"controle-de-leitura.csv", ".ds_store", "thumbs.db", "desktop.ini"}


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn").lower().strip()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def ler_csv(caminho):
    bruto = caminho.read_bytes().decode("utf-8-sig", errors="replace")
    if not bruto.strip():
        return []
    primeira = bruto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(bruto), delimiter=sep)
    campos = {sem_acento(c or ""): c for c in (leitor.fieldnames or [])}
    faltam = [c for c in OBRIGATORIAS if c not in campos]
    if faltam:
        erro(f"o controle {caminho} não tem a(s) coluna(s) {', '.join(faltam)}. "
             f"Colunas esperadas: {','.join(COLUNAS)}")
    linhas = []
    for l in leitor:
        nova = {c: (l.get(campos[c]) or "").strip() if c in campos else "" for c in COLUNAS}
        nova["situacao"] = sem_acento(nova["situacao"]) or "a-ler"
        linhas.append(nova)
    return linhas


def contar_paginas_pdf(dados):
    n = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", dados))
    return str(n) if n else "?"


def pdf_tem_texto(dados):
    return b"/Font" in dados


def frontmatter(texto):
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                v = re.sub(r"\s+#.*$", "", v).strip()
                campos[sem_acento(k)] = v
    return campos


def main():
    ap = argparse.ArgumentParser(description="Índice e controle de leitura do lote de documentos do caso.")
    ap.add_argument("pasta")
    ap.add_argument("controle")
    ap.add_argument("--fichas")
    ap.add_argument("--marcar", action="append", default=[])
    ap.add_argument("--paginas-por-etapa", type=int, default=60)
    ap.add_argument("--prefixo", default="D")
    ap.add_argument("--so-mostrar", action="store_true")
    ap.add_argument("--codigo-do-nome", action="store_true")
    a = ap.parse_args()

    pasta = Path(a.pasta)
    if not pasta.is_dir():
        erro(f"a pasta {pasta} não existe. Nada foi indexado.")
    controle = Path(a.controle)

    arquivos = sorted(
        p for p in pasta.rglob("*")
        if p.is_file() and not any(parte.startswith(".") for parte in p.relative_to(pasta).parts)
        and p.name.lower() not in IGNORAR and "lidos" not in p.relative_to(pasta).parts[:-1]
    )
    if not arquivos:
        erro(f"nenhum documento encontrado em {pasta}. Nada foi indexado.")

    antigas = ler_csv(controle) if controle.exists() else []
    por_arquivo = {l["arquivo"]: l for l in antigas}
    usados = [int(m.group(1)) for l in antigas for m in [re.match(r"^[A-Za-z]+(\d+)$", l["doc"])] if m]
    proximo = max(usados, default=0) + 1

    linhas, vistos, hashes = [], set(), {}
    codigos = {l["doc"] for l in antigas}

    def codigo_do_nome(p):
        m = re.match(r"^([A-Za-z]{1,3})[-_ ]?(\d{1,4})(?=[-_ .])", p.name) if a.codigo_do_nome else None
        return f"{m.group(1).upper()}{int(m.group(2))}" if m else ""

    # códigos que vêm do nome dos arquivos novos ficam reservados antes da numeração sequencial
    reservados = {c for p in arquivos if p.relative_to(pasta).as_posix() not in por_arquivo
                  for c in [codigo_do_nome(p)] if c}
    for p in arquivos:
        rel = p.relative_to(pasta).as_posix()
        dados = p.read_bytes()
        h = hashlib.sha256(dados).hexdigest()[:16]
        tipo = TIPOS.get(p.suffix.lower(), "outro")
        paginas = contar_paginas_pdf(dados) if tipo == "pdf" else ("1" if tipo == "imagem" else "")
        linha = por_arquivo.get(rel)
        if linha is None:
            linha = {c: "" for c in COLUNAS}
            codigo = codigo_do_nome(p)
            if not codigo or codigo in codigos:
                while f"{a.prefixo}{proximo}" in codigos or f"{a.prefixo}{proximo}" in reservados:
                    proximo += 1
                codigo = f"{a.prefixo}{proximo}"
                proximo += 1
            linha["doc"] = codigo
            linha["arquivo"] = rel
            linha["situacao"] = "a-ler"
        linha.update({"tipo": tipo, "paginas": paginas or linha.get("paginas", ""),
                      "tamanho_kb": str(max(1, round(len(dados) / 1024))), "hash": h})
        obs = [o for o in linha.get("observacao", "").split("; ")
               if o and not o.startswith(("provável imagem", "pedir transcrição", "mesmo conteúdo de", "arquivo não encontrado"))]
        if tipo == "pdf" and not pdf_tem_texto(dados):
            obs.append("provável imagem sem texto: pedir versão pesquisável ou ler página a página")
        if tipo in ("audio", "video"):
            obs.append("pedir transcrição: a habilidade não ouve áudio")
        if h in hashes:
            obs.append(f"mesmo conteúdo de {hashes[h]}")
            if linha["situacao"] == "a-ler":
                linha["situacao"] = "duplicado"
        else:
            hashes[h] = linha["doc"]
        linha["observacao"] = "; ".join(obs)
        linhas.append(linha)
        vistos.add(rel)
        codigos.add(linha["doc"])

    for l in antigas:
        if l["arquivo"] not in vistos:
            obs = [o for o in l["observacao"].split("; ") if o and not o.startswith("arquivo não encontrado")]
            obs.append("arquivo não encontrado na pasta")
            l["observacao"] = "; ".join(obs)
            linhas.append(l)

    avisos = []
    if a.fichas:
        pf = Path(a.fichas)
        if not pf.is_dir():
            avisos.append(f"a pasta de fichas {pf} não existe; o controle não foi sincronizado com as fichas")
        else:
            por_doc = {l["doc"].lower(): l for l in linhas}
            for f in sorted(pf.glob("*.md")):
                fm = frontmatter(f.read_text(encoding="utf-8", errors="replace"))
                doc = (fm.get("doc") or f.stem).strip().lower()
                l = por_doc.get(doc)
                if l is None:
                    avisos.append(f"ficha {f.name} fala de {doc.upper()}, que não está no índice")
                    continue
                sit = sem_acento(fm.get("situacao") or fm.get("status") or "lido")
                l["situacao"] = sit if sit in SITUACOES else "lido"
                l["paginas_lidas"] = fm.get("paginas_lidas", l["paginas_lidas"])
                l["ficha"] = f.name

    for m in a.marcar:
        mm = re.match(r"^\s*([A-Za-z]+\d+)\s*=\s*([a-zA-Z-]+)\s*(?::\s*(.+))?$", m)
        if not mm:
            erro(f"--marcar '{m}' não está no formato DOC=SITUACAO[:PAGINAS], por exemplo D3=lido-em-parte:1-20")
        doc, sit, pags = mm.group(1).lower(), sem_acento(mm.group(2)), mm.group(3)
        if sit not in SITUACOES:
            erro(f"situação '{sit}' não existe. Use uma destas: {', '.join(SITUACOES)}")
        alvo = [l for l in linhas if l["doc"].lower() == doc]
        if not alvo:
            erro(f"{doc.upper()} não está no índice")
        alvo[0]["situacao"] = sit
        if pags:
            alvo[0]["paginas_lidas"] = pags.strip()

    for l in linhas:
        if l["situacao"] not in SITUACOES:
            avisos.append(f"{l['doc']}: situação '{l['situacao']}' desconhecida, tratada como a-ler")
            l["situacao"] = "a-ler"

    if not a.so_mostrar:
        controle.parent.mkdir(parents=True, exist_ok=True)
        with controle.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUNAS)
            w.writeheader()
            for l in linhas:
                w.writerow({c: l.get(c, "") for c in COLUNAS})

    def pags(l):
        return int(l["paginas"]) if (l.get("paginas") or "").isdigit() else 0

    total_pag = sum(pags(l) for l in linhas)
    cont = {s: sum(1 for l in linhas if l["situacao"] == s) for s in SITUACOES}
    print(f"# Índice do lote · {pasta.name}\n")
    print(f"- Documentos: {len(linhas)} · páginas contadas: {total_pag}"
          + (" (alguns PDFs sem contagem: '?')" if any(l.get("paginas") == "?" for l in linhas) else ""))
    print("- Situação: " + " · ".join(f"{s} {n}" for s, n in cont.items() if n))
    print(f"- Controle: {controle}" + (" (não gravado: --so-mostrar)" if a.so_mostrar else " (gravado)"))
    for av in avisos:
        print(f"- Aviso: {av}")
    print("\n| doc | arquivo | tipo | páginas | situação | páginas lidas | observação |")
    print("|---|---|---|---|---|---|---|")
    for l in linhas:
        print(f"| {l['doc']} | {l['arquivo']} | {l['tipo']} | {l['paginas']} | {l['situacao']} | "
              f"{l['paginas_lidas']} | {l['observacao']} |")

    pendentes = [l for l in linhas if l["situacao"] in ("a-ler", "lido-em-parte")]
    print("\n## Próxima etapa de leitura")
    if not pendentes:
        print("Nenhum documento por ler. Siga para a matriz e as contradições.")
    else:
        etapa, soma = [], 0
        for l in pendentes:
            if etapa and soma + max(pags(l), 1) > a.paginas_por_etapa:
                break
            etapa.append(l)
            soma += max(pags(l), 1)
        print(f"Ler agora ({soma} páginas, limite {a.paginas_por_etapa}): " + ", ".join(l["doc"] for l in etapa))
        resto = len(pendentes) - len(etapa)
        if resto:
            print(f"Depois desta etapa ainda faltam {resto} documento(s).")
    problemas = [l for l in linhas if l["situacao"] == "ilegivel" or "imagem sem texto" in l["observacao"]
                 or "transcrição" in l["observacao"] or "não encontrado" in l["observacao"]]
    if problemas:
        print("\n## O que não dá para ler como está")
        for l in problemas:
            print(f"- {l['doc']} ({l['arquivo']}): {l['observacao'] or l['situacao']}")


if __name__ == "__main__":
    main()
