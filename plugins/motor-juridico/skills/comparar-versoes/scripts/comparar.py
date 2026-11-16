#!/usr/bin/env python3
"""Diferença por trecho ou cláusula entre duas versões de um documento (motor-juridico, comparar-versoes).

Divide cada versão em trechos (cláusulas, artigos, itens numerados, títulos ou parágrafos),
alinha os trechos da versão A com os da versão B e diz, para cada um: igual, renumerado,
alterado, incluído, excluído ou movido. Nos alterados, mostra a diferença palavra por palavra
([-saiu-] {+entrou+}) e os sinais mecânicos de risco: número, valor, data ou percentual que
mudou; negação que entrou ou saiu; obrigação que virou faculdade (ou o contrário); palavras
sensíveis (multa, prazo, foro, responsabilidade...). A leitura de risco de verdade é de quem
lê: o script só aponta onde olhar.

Só biblioteca padrão (Python 3.9+). Lê .txt, .md e .docx (o texto dos parágrafos). PDF não:
salve o texto antes. Não altera os arquivos.

Uso:
  python3 comparar.py VERSAO_A VERSAO_B [--saida RELATORIO.md] [--palavras "termo1; termo2"]
                      [--por paragrafo|clausula] [--rotulos "nossa minuta" "minuta deles"]

Sai com código 1 e mensagem clara quando um arquivo não existe, está vazio ou tem formato
que o script não lê.
"""
import argparse
import re
import sys
import unicodedata
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree

SENSIVEIS = [
    "multa", "juros", "correcao", "reajuste", "indice", "rescis", "resilicao", "denuncia",
    "foro", "arbitragem", "prazo", "vigencia", "renova", "automatic", "responsabilidade", "indeniz",
    "garanti", "fianca", "aval", "exclusiv", "renunc", "solidari", "subsidiari",
    "quita", "penalidade", "clausula penal", "confidencial", "sigilo", "nao concorrencia",
    "propriedade", "cessao", "transferencia", "honorarios", "custas", "partilha", "guarda",
    "alimentos", "pensao", "visita", "convivencia", "usufruto", "posse", "entrega", "pagamento",
    "parcela", "vencimento", "inadimplemento", "mora", "limitacao", "teto", "dano",
    "iptu", "condominio", "imposto", "tributo", "despesa", "reside", "moradia",
]
ROTULO_PALAVRA = {
    "quita": "quitação", "renunc": "renúncia", "renova": "renovação", "automatic": "automática",
    "rescis": "rescisão", "resilicao": "resilição", "denuncia": "denúncia", "garanti": "garantia",
    "exclusiv": "exclusividade", "indeniz": "indenização", "solidari": "solidariedade",
    "subsidiari": "subsidiariedade", "correcao": "correção", "condominio": "condomínio",
    "indice": "índice", "honorarios": "honorários", "pensao": "pensão", "convivencia": "convivência",
    "cessao": "cessão", "transferencia": "transferência", "limitacao": "limitação",
    "vigencia": "vigência", "clausula penal": "cláusula penal", "nao concorrencia": "não concorrência",
    "confidencial": "confidencialidade", "fianca": "fiança", "rescisao": "rescisão",
}
NEGACOES = r"\b(nao|nunca|nenhum|nenhuma|vedad[oa]|proibid[oa]|sem|exceto|salvo)\b"
OBRIGA = r"\b(devera|deverao|obriga|obrigam|obrigatori|compromete|comprometem|fica responsavel|ficam responsaveis|sera responsavel)\w*"
FACULTA = r"\b(podera|poderao|pode|podem|facultad|a criterio)\w*"
NUMERO = re.compile(r"R\$\s?[\d.]+(?:,\d{2})?|\d+(?:[.,]\d+)*\s?%|\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}|\b\d+(?:[.,]\d+)*\b")
INICIO = re.compile(
    r"^\s*(#{1,6}\s+\S|(cl[aá]usula|art(igo)?\.?|par[aá]grafo|§|item|se[cç][aã]o|cap[ií]tulo)\s*[\dºª°.\-]*\s*\S"
    r"|\d+(\.\d+)*[.)\-]?\s+\S|[IVXLC]+\s*[.)\-]\s+\S|[a-z]\)\s+\S)", re.I)
ROTULO_NUM = re.compile(
    r"^\s*(#{1,6}\s*)?((cl[aá]usula|art(igo)?\.?|par[aá]grafo|item|se[cç][aã]o|cap[ií]tulo)\s*"
    r"([\dIVXLC]+[ºª°]?(\.\d+)*)|§\s*\d+[ºª°]?|(\d+(\.\d+)*)[.)\-]?|([IVXLC]+)\s*[.)\-]|([a-z])\))\s*[.:\-]?\s*", re.I)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def ler(caminho):
    p = Path(caminho)
    if not p.exists():
        erro(f"o arquivo {p} não existe. Nada foi comparado.")
    suf = p.suffix.lower()
    if suf in (".txt", ".md", ""):
        texto = p.read_bytes().decode("utf-8-sig", errors="replace")
    elif suf == ".docx":
        try:
            with zipfile.ZipFile(p) as z:
                xml = z.read("word/document.xml")
        except (zipfile.BadZipFile, KeyError):
            erro(f"{p} não parece um .docx válido. Salve como .docx de novo ou como texto.")
        ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        raiz = ElementTree.fromstring(xml)
        paras = []
        for par in raiz.iter(f"{ns}p"):
            partes = []
            for n in par.iter():
                if n.tag == f"{ns}t" and n.text:
                    partes.append(n.text)
                elif n.tag == f"{ns}tab":
                    partes.append(" ")
            paras.append("".join(partes))
        texto = "\n\n".join(paras)
    elif suf == ".pdf":
        erro(f"{p} é PDF. Salve o texto do PDF (.txt) ou o .docx e rode de novo.")
    else:
        erro(f"formato {suf} não aceito em {p}. Use .txt, .md ou .docx.")
    if not texto.strip():
        erro(f"o arquivo {p} está vazio. Nada foi comparado.")
    return texto


def trechos(texto, modo):
    linhas = [l.rstrip() for l in texto.splitlines()]
    tem_marcas = sum(1 for l in linhas if INICIO.match(l)) >= 2
    grupos, atual = [], []
    if modo == "clausula" and tem_marcas:
        for l in linhas:
            if INICIO.match(l) and atual:
                grupos.append(atual)
                atual = []
            if l.strip() or atual:
                atual.append(l)
        if atual:
            grupos.append(atual)
    else:
        for l in linhas:
            if not l.strip():
                if atual:
                    grupos.append(atual)
                    atual = []
            else:
                atual.append(l)
        if atual:
            grupos.append(atual)
    saida = []
    for b in grupos:
        t = "\n".join(b).strip()
        if not t:
            continue
        primeira = b[0].strip()
        m = ROTULO_NUM.match(primeira)
        numero = ""
        if m and m.group(0).strip():
            numero = re.sub(r"\s+", " ", m.group(0).strip(" .:-#"))
        corpo = ROTULO_NUM.sub("", t, count=1) if numero else t
        saida.append({"rotulo": primeira[:70], "numero": numero, "texto": t, "sem_rotulo": corpo.strip(),
                      "corpo": re.sub(r"\s+", " ", sem_acento(corpo)).strip()})
    return saida


def razao(a, b):
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def diff_palavras(a, b):
    ta, tb = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if op == "equal":
            out.append(" ".join(ta[i1:i2]))
        if op in ("delete", "replace"):
            out.append("[-" + " ".join(ta[i1:i2]) + "-]")
        if op in ("insert", "replace"):
            out.append("{+" + " ".join(tb[j1:j2]) + "+}")
    return " ".join(out)


def sinais(a, b, palavras):
    sa, sb = sem_acento(a), sem_acento(b)
    s = []
    na, nb = set(NUMERO.findall(a)), set(NUMERO.findall(b))
    if na != nb:
        sai, entra = sorted(na - nb), sorted(nb - na)
        s.append("número, valor ou data mudou" + (f" (saiu {', '.join(sai)}" if sai else " (")
                 + ("; " if sai and entra else "") + (f"entrou {', '.join(entra)}" if entra else "") + ")")
    neg_a, neg_b = len(re.findall(NEGACOES, sa)), len(re.findall(NEGACOES, sb))
    if neg_a != neg_b:
        s.append("negação " + ("entrou" if neg_b > neg_a else "saiu"))
    oa, ob = len(re.findall(OBRIGA, sa)), len(re.findall(OBRIGA, sb))
    fa, fb = len(re.findall(FACULTA, sa)), len(re.findall(FACULTA, sb))
    if ob < oa and fb > fa:
        s.append("obrigação virou faculdade")
    elif ob > oa and fb < fa:
        s.append("faculdade virou obrigação")
    elif ob != oa:
        s.append("obrigação " + ("entrou" if ob > oa else "saiu"))
    frases_a = {f.strip() for f in re.split(r"(?<=[.;:])\s+", sa) if f.strip()}
    frases_b = {f.strip() for f in re.split(r"(?<=[.;:])\s+", sb) if f.strip()}
    mudadas = " ".join((frases_a - frases_b) | (frases_b - frases_a))
    tocadas = sorted({p for p in palavras if p in mudadas})
    if tocadas:
        s.append("palavra sensível no trecho que mudou: " + ", ".join(ROTULO_PALAVRA.get(p, p) for p in tocadas))
    return s


def alinhar(A, B):
    """Devolve lista de (i, j) com i em A ou None, j em B ou None, na ordem de B."""
    corpos_a = [x["corpo"] for x in A]
    corpos_b = [x["corpo"] for x in B]
    pares = []
    for op, i1, i2, j1, j2 in SequenceMatcher(None, corpos_a, corpos_b, autojunk=False).get_opcodes():
        if op == "equal":
            pares += [(i1 + k, j1 + k) for k in range(i2 - i1)]
            continue
        livres_a = list(range(i1, i2))
        grupo = []
        for j in range(j1, j2):
            melhor, r_melhor = None, 0.0
            for i in livres_a:
                r = razao(corpos_a[i], corpos_b[j])
                if r < 0.45:
                    continue
                if A[i]["numero"] and A[i]["numero"] == B[j]["numero"]:
                    r += 0.05
                if r > r_melhor:
                    melhor, r_melhor = i, r
            if melhor is not None:
                livres_a.remove(melhor)
                grupo.append((melhor, j))
            else:
                grupo.append((None, j))
        for i in livres_a:
            pos = next((k for k, (ii, _) in enumerate(grupo) if ii is not None and ii > i), len(grupo))
            grupo.insert(pos, (i, None))
        pares += grupo
    return pares


def main():
    ap = argparse.ArgumentParser(description="Diferença por trecho ou cláusula entre duas versões.")
    ap.add_argument("versao_a")
    ap.add_argument("versao_b")
    ap.add_argument("--saida")
    ap.add_argument("--palavras", default="")
    ap.add_argument("--por", choices=["clausula", "paragrafo"], default="clausula")
    ap.add_argument("--rotulos", nargs=2, default=["versão A", "versão B"])
    a = ap.parse_args()

    ta, tb = ler(a.versao_a), ler(a.versao_b)
    A, B = trechos(ta, a.por), trechos(tb, a.por)
    extras = [sem_acento(p).strip() for p in re.split(r"[;,·]", a.palavras) if p.strip()]
    extras = [p for p in extras if not re.fullmatch(r"\[.*\]", p)]
    palavras = SENSIVEIS + extras

    pares = alinhar(A, B)
    excluidos = {i for i, j in pares if j is None}
    incluidos = {j for i, j in pares if i is None}
    movidos = {}
    for i in excluidos:
        for j in incluidos:
            if j not in movidos.values() and razao(A[i]["corpo"], B[j]["corpo"]) >= 0.9:
                movidos[i] = j
                break

    linhas, detalhes, cont = [], [], {}
    n = 0
    for i, j in pares:
        if i is not None and j is None and i in movidos:
            continue
        if i is None and j in movidos.values():
            i = next(k for k, v in movidos.items() if v == j)
            situacao = "movido"
        elif i is None:
            situacao = "incluído"
        elif j is None:
            situacao = "excluído"
        elif A[i]["corpo"] == B[j]["corpo"]:
            situacao = "renumerado" if A[i]["numero"] != B[j]["numero"] else "igual"
        else:
            situacao = "alterado"
        cont[situacao] = cont.get(situacao, 0) + 1
        if situacao == "igual":
            continue
        n += 1
        ra = A[i]["rotulo"] if i is not None else ""
        rb = B[j]["rotulo"] if j is not None else ""
        if situacao == "alterado" or situacao == "movido" and A[i]["corpo"] != B[j]["corpo"]:
            s = sinais(A[i]["texto"], B[j]["texto"], palavras)
            detalhes.append((n, situacao, ra, rb, diff_palavras(A[i]["sem_rotulo"], B[j]["sem_rotulo"]), s))
        elif situacao == "incluído":
            s = sinais("", B[j]["texto"], palavras)
            detalhes.append((n, situacao, ra, rb, "{+" + B[j]["texto"] + "+}", s))
        elif situacao == "excluído":
            s = sinais(A[i]["texto"], "", palavras)
            detalhes.append((n, situacao, ra, rb, "[-" + A[i]["texto"] + "-]", s))
        else:
            s = [f"número mudou: {A[i]['numero'] or 'sem número'} para {B[j]['numero'] or 'sem número'}"] \
                if A[i]["numero"] != B[j]["numero"] else []
        linhas.append((n, ra.replace("|", "/"), rb.replace("|", "/"), situacao, "; ".join(s).replace("|", "/")))

    out = []
    p = out.append
    p(f"# Comparação · {Path(a.versao_a).name} x {Path(a.versao_b).name}\n")
    p(f"- {a.rotulos[0]}: {a.versao_a} ({len(A)} trechos)")
    p(f"- {a.rotulos[1]}: {a.versao_b} ({len(B)} trechos)")
    p("- Divisão: " + ("por cláusula, item ou título" if a.por == "clausula" else "por parágrafo"))
    p("- Resultado: " + " · ".join(f"{k} {v}" for k, v in sorted(cont.items())))
    p("- Os sinais são mecânicos. O risco de cada mudança é lido por uma pessoa.\n")
    if not linhas:
        p("As duas versões têm o mesmo texto, trecho por trecho (diferenças só de espaço ou maiúscula).")
    else:
        p(f"| # | {a.rotulos[0]} | {a.rotulos[1]} | Situação | Sinais |")
        p("|---|---|---|---|---|")
        for l in linhas:
            p(f"| {l[0]} | {l[1]} | {l[2]} | {l[3]} | {l[4]} |")
        p("\n## Mudança por mudança\n")
        for n, sit, ra, rb, d, s in detalhes:
            p(f"### {n} · {sit} · {rb or ra}\n")
            p(d + "\n")
            if s:
                p("Sinais: " + "; ".join(s) + "\n")
    texto = "\n".join(out) + "\n"
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        print(f"Comparação gravada em {a.saida}: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())))
    else:
        sys.stdout.write(texto)


if __name__ == "__main__":
    main()
