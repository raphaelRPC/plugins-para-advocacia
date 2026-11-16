#!/usr/bin/env python3
"""Linha do tempo do caso a partir das fichas por documento (motor-juridico, dossie-do-caso).

Lê as fichas (<doc>.md, uma por documento, no formato de assets/modelo-ficha-documento.md),
junta os fatos de todas em ordem de data e aponta, de forma mecânica:

  1. a linha do tempo integrada, com o documento e o lugar de cada fato;
  2. mesma chave de fato com datas que não cabem uma na outra, em documentos diferentes
     (possível contradição); fato que se repete no mesmo documento não conta;
  3. quem fala de cada fato (chave x documentos), o começo da matriz fato x prova;
  4. fatos sem data;
  5. o que a linha do tempo não cobre: documentos do controle de leitura sem ficha,
     lidos em parte ou ilegíveis.

Só biblioteca padrão (Python 3.9+). Não altera as fichas. Não interpreta o conteúdo:
quem decide se a divergência é contradição de verdade é quem lê os documentos.

Uso:
  python3 linha_do_tempo.py PASTA_DAS_FICHAS [--controle controle-de-leitura.csv] [--saida ARQUIVO.md]

Datas aceitas na coluna data (e na coluna ate, para períodos): AAAA-MM-DD, DD/MM/AAAA,
AAAA-MM, MM/AAAA e AAAA. Vazio ou "sem data" vai para a lista de fatos sem data.

Sai com código 1 e mensagem clara quando a pasta não existe, quando não há ficha
nenhuma ou quando nenhuma ficha tem a tabela de fatos.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import OrderedDict, defaultdict
from pathlib import Path


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower().strip()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def ler_data(texto):
    """Devolve (chave_de_ordem, texto_normalizado) ou None."""
    t = (texto or "").strip()
    if not t or sem_acento(t) in ("sem data", "-", "?", "s/d"):
        return None
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        return (int(m[1]), int(m[2]), int(m[3])), f"{m[1]}-{m[2]}-{m[3]}"
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", t)
    if m:
        return (int(m[3]), int(m[2]), int(m[1])), f"{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}"
    m = re.fullmatch(r"(\d{4})-(\d{2})", t)
    if m:
        return (int(m[1]), int(m[2]), 0), f"{m[1]}-{m[2]}"
    m = re.fullmatch(r"(\d{1,2})/(\d{4})", t)
    if m:
        return (int(m[2]), int(m[1]), 0), f"{m[2]}-{int(m[1]):02d}"
    m = re.fullmatch(r"(\d{4})", t)
    if m:
        return (int(m[1]), 0, 0), m[1]
    return False


def compativeis(d1, d2):
    """2022-03 e 2022-03-01 são compatíveis (uma cabe na outra); datas completas diferentes não."""
    return d1.startswith(d2) or d2.startswith(d1)


def frontmatter(texto):
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                campos[sem_acento(k)] = re.sub(r"\s+#.*$", "", v).strip()
    return campos


def celulas(linha):
    linha = linha.strip()
    if not linha.startswith("|"):
        return None
    partes = [c.strip() for c in linha.strip("|").split("|")]
    return partes


def tabela_de_fatos(texto):
    """Acha a primeira tabela cujo cabeçalho tem 'data' e 'fato'."""
    linhas = texto.splitlines()
    for i, l in enumerate(linhas):
        cab = celulas(l)
        if not cab:
            continue
        nomes = [sem_acento(c) for c in cab]
        if "data" in nomes and "fato" in nomes:
            if i + 1 < len(linhas) and re.fullmatch(r"\|?[\s:|-]+\|?", linhas[i + 1].strip()):
                corpo = []
                for l2 in linhas[i + 2:]:
                    c = celulas(l2)
                    if c is None:
                        break
                    corpo.append(dict(zip(nomes, c + [""] * (len(nomes) - len(c)))))
                return nomes, corpo
    return None, []


def ler_controle(caminho):
    bruto = caminho.read_bytes().decode("utf-8-sig", errors="replace")
    if not bruto.strip():
        return []
    sep = ";" if bruto.splitlines()[0].count(";") > bruto.splitlines()[0].count(",") else ","
    leitor = csv.DictReader(io.StringIO(bruto), delimiter=sep)
    campos = {sem_acento(c or ""): c for c in (leitor.fieldnames or [])}
    for c in ("doc", "situacao"):
        if c not in campos:
            erro(f"o controle {caminho} não tem a coluna {c}")
    return [{k: (l.get(v) or "").strip() for k, v in campos.items()} for l in leitor]


def main():
    ap = argparse.ArgumentParser(description="Linha do tempo integrada a partir das fichas por documento.")
    ap.add_argument("fichas")
    ap.add_argument("--controle")
    ap.add_argument("--saida")
    a = ap.parse_args()

    pasta = Path(a.fichas)
    if not pasta.is_dir():
        erro(f"a pasta de fichas {pasta} não existe. Nenhuma linha do tempo foi montada.")
    arquivos = sorted(pasta.glob("*.md"))
    if not arquivos:
        erro(f"nenhuma ficha (.md) em {pasta}. Faça as fichas por documento antes da linha do tempo.")

    fatos, sem_data, datas_ruins, fichas_sem_tabela, situacao_ficha = [], [], [], [], {}
    for f in arquivos:
        texto = f.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(texto)
        doc = (fm.get("doc") or f.stem).strip().upper()
        situacao_ficha[doc] = (sem_acento(fm.get("situacao") or fm.get("status") or "lido"),
                               fm.get("paginas_lidas", ""))
        nomes, corpo = tabela_de_fatos(texto)
        if nomes is None:
            fichas_sem_tabela.append(f.name)
            continue
        for linha in corpo:
            fato = linha.get("fato", "").strip()
            if not fato:
                continue
            chave = sem_acento(linha.get("chave", "")).replace(" ", "-")
            onde = linha.get("onde", "") or linha.get("pagina", "") or linha.get("trecho", "")
            item = {"doc": doc, "chave": chave, "fato": fato, "onde": onde,
                    "data_txt": linha.get("data", "").strip(), "ate_txt": linha.get("ate", "").strip()}
            d = ler_data(item["data_txt"])
            if d is None:
                sem_data.append(item)
                continue
            if d is False:
                datas_ruins.append(item)
                continue
            item["ordem"], item["data"] = d
            ate = ler_data(item["ate_txt"])
            item["ate"] = ate[1] if ate else ""
            if ate is False:
                datas_ruins.append(dict(item, data_txt=item["ate_txt"]))
            fatos.append(item)

    if not fatos and not sem_data:
        erro(f"li {len(arquivos)} ficha(s) em {pasta} e nenhuma tem fatos na tabela "
             "(cabeçalho com as colunas data e fato). Nada foi montado.")

    fatos.sort(key=lambda x: (x["ordem"], x["doc"]))
    saida = []
    p = saida.append
    p(f"# Linha do tempo · {pasta.parent.name if pasta.name == 'fichas' else pasta.name}\n")
    p(f"Montada a partir de {len(arquivos)} ficha(s). Cada fato traz o documento e o lugar de onde saiu. "
      "Fato que não está numa ficha não está aqui.\n")
    p("| Data | Até | Fato | Doc | Onde | Chave |")
    p("|---|---|---|---|---|---|")
    for x in fatos:
        p(f"| {x['data']} | {x['ate']} | {x['fato']} | {x['doc']} | {x['onde']} | {x['chave']} |")

    por_chave = OrderedDict()
    for x in fatos + sem_data:
        if x["chave"]:
            por_chave.setdefault(x["chave"], []).append(x)

    p("\n## Mesma chave, datas diferentes (possível contradição)\n")
    p("Só entra aqui quando documentos diferentes dão datas que não cabem uma na outra "
      "(2022-03 e 2022-03-01 cabem; 2022-03-01 e 2022-05-02 não).\n")
    achou = False
    for chave, itens in por_chave.items():
        com_data = [x for x in itens if x.get("data")]
        conflito = any(
            x["doc"] != y["doc"] and not compativeis(x["data"], y["data"])
            for i, x in enumerate(com_data) for y in com_data[i + 1:]
        )
        if conflito:
            achou = True
            datas = defaultdict(set)
            for x in com_data:
                datas[x["data"]].add(x["doc"])
            desc = "; ".join(f"{d} em {', '.join(sorted(docs))}" for d, docs in sorted(datas.items()))
            p(f"- **{chave}**: {desc}. Confira nos documentos qual data vale e por quê.")
    if not achou:
        p("Nenhuma chave com datas que não batem entre documentos. Isso não exclui contradição de conteúdo: "
          "confira a matriz fato x prova.")

    p("\n## Quem fala de cada fato (começo da matriz fato x prova)\n")
    p("| Chave | Documentos | Datas |")
    p("|---|---|---|")
    for chave, itens in por_chave.items():
        docs = sorted({x["doc"] for x in itens})
        datas = sorted({x.get("data", "sem data") for x in itens})
        p(f"| {chave} | {', '.join(docs)} | {', '.join(datas)} |")
    sem_chave = [x for x in fatos + sem_data if not x["chave"]]
    if sem_chave:
        p(f"\n{len(sem_chave)} fato(s) sem chave: não entram no cruzamento. Dê uma chave a cada fato que "
          "possa aparecer em mais de um documento.")

    if sem_data:
        p("\n## Fatos sem data\n")
        for x in sem_data:
            p(f"- {x['fato']} ({x['doc']}, {x['onde'] or 'lugar não indicado'})")
    if datas_ruins:
        p("\n## Datas que o script não entendeu (corrija na ficha)\n")
        for x in datas_ruins:
            p(f"- '{x['data_txt']}' em {x['doc']}: {x['fato']}")

    p("\n## O que esta linha do tempo não cobre\n")
    lacunas = []
    for f in fichas_sem_tabela:
        lacunas.append(f"ficha {f} sem tabela de fatos")
    for doc, (sit, pags) in sorted(situacao_ficha.items()):
        if sit in ("lido-em-parte", "ilegivel"):
            lacunas.append(f"{doc}: {sit}" + (f" (páginas lidas: {pags})" if pags else ""))
    if a.controle:
        c = Path(a.controle)
        if not c.exists():
            lacunas.append(f"controle de leitura {c} não encontrado: não dá para dizer quais documentos ficaram de fora")
        else:
            for l in ler_controle(c):
                doc = l["doc"].upper()
                sit = sem_acento(l["situacao"])
                if sit in ("duplicado", "fora-do-caso"):
                    continue
                if doc not in situacao_ficha:
                    lacunas.append(f"{doc} ({l.get('arquivo', '')}): sem ficha, situação {sit or 'a-ler'}")
    else:
        lacunas.append("sem --controle: não dá para dizer se algum documento do lote ficou sem ficha")
    if lacunas:
        for l in lacunas:
            p(f"- {l}")
    else:
        p("Todos os documentos do controle têm ficha e foram lidos por inteiro.")

    texto = "\n".join(saida) + "\n"
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        print(f"Linha do tempo gravada em {a.saida} ({len(fatos)} fatos com data, {len(sem_data)} sem data).")
    else:
        sys.stdout.write(texto)


if __name__ == "__main__":
    main()
