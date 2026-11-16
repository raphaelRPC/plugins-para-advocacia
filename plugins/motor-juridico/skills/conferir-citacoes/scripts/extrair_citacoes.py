#!/usr/bin/env python3
"""Extrai e pré-classifica todas as citações de uma peça (motor-juridico, conferir-citacoes).

Lê a peça (.md, .txt ou .docx) e monta a tabela das citações:
  - leis e artigos (art. 59 da Lei 8.213/1991, art. 300 do CPC, art. 5º, LXXIV, da CF);
  - súmulas (Súmula 999 do TRF6, Súmula Vinculante N);
  - temas de repercussão geral e de repetitivo, IRDR e IAC;
  - julgados por padrão de número (classe e número, número único do CNJ);
  - trechos entre aspas e em recuo, ligados à citação mais próxima;
  - menções vagas ("entendimento pacífico", "jurisprudência dominante"), que saem amarelas
    por falta de fonte.
Para cada uma: a linha, se tem a marca [CONFERIR], se está na base do escritório
(04-base/juridico/jurisprudencia/), a situação da conferência na base, a cor sugerida e o que
fazer. O que não está na base vira a lista "Pesquisar no Jus IA". Leis e artigos vão para a
lista "Conferir no portal oficial". Com --fontes (texto oficial salvo do portal), os trechos
entre aspas são comparados palavra por palavra.

O script NUNCA dá uma citação por conferida sozinho: verde só sai de uma conferência da base
dentro da validade, ou de aspas que batem com a fonte oficial salva. O resto fica "pendente"
até a conferência na fonte (citacoes.md).

Uso:
  python3 extrair_citacoes.py PECA.md [--base escritorio/04-base/juridico/jurisprudencia]
      [--validade 90] [--ficha ficha-juridica.md] [--hoje AAAA-MM-DD]
      [--fontes pasta-ou-arquivo ...] [--vagas "expressão;expressão"] [--treino]
      [--saida relatorio.md] [--json]

Sem --base, procura a base subindo a partir da peça. Quando a peça está sob uma pasta
_treino/ (escritorio/07-operacao/_treino/juridico/...), procura primeiro a base de treino,
escritorio/07-operacao/_treino/juridico/jurisprudencia/ (onde a trazer-pesquisa grava as
fichas de treino); sem ela, escritorio/04-base/juridico/jurisprudencia.
Sem --validade, lê validade_da_conferencia da ficha jurídica (só o número antes do
parêntese); sem ficha, 90 dias, com aviso.
--treino: casos fictícios. Súmula, tema ou julgado fora da base sai com vermelho sugerido,
porque os números do material de treino são inventados de propósito.

Sai com código 1 e mensagem clara quando falta o arquivo, ele está vazio ou não dá para ler.
Só biblioteca padrão.
"""

import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
import zipfile
from datetime import date, datetime
from xml.etree import ElementTree

DIPLOMA = (r"Lei(?:\s+Complementar)?\s*(?:n[º°o.]*\s*)?\d[\d.]*\s*/\s*\d{2,4}"
           r"|Decreto(?:-Lei)?\s*(?:n[º°o.]*\s*)?\d[\d.]*\s*/\s*\d{2,4}"
           r"|Emenda\s+Constitucional\s*(?:n[º°o.]*\s*)?\d+(?:\s*/\s*\d{2,4})?"
           r"|Constitui[çc][ãa]o(?:\s+Federal)?|CF(?:/88)?\b|CPC\b|CPP\b|CLT\b|CDC\b|ECA\b|CTN\b|CC\b"
           r"|C[óo]digo\s+(?:Civil|Penal|de\s+Processo\s+Civil|de\s+Processo\s+Penal|Tribut[áa]rio\s+Nacional|de\s+Defesa\s+do\s+Consumidor)"
           r"|Estatuto\s+d[ao]\s+[A-ZÁ-Ú][\wá-ú]+(?:\s+e\s+do\s+[A-ZÁ-Ú][\wá-ú]+)?")
NUM_ART = r"\d+[º°o]?(?:-[A-Z])?"
ARTIGO = re.compile(
    r"\b(?:[Aa]rts?\.|[Aa]rtigos?)\s*" + NUM_ART + r"(?:\s*(?:,|e|a)\s*" + NUM_ART + r")*"
    r"(?:\s*,?\s*(?:§+|[Pp]ar[áa]grafo)\s*(?:\d+[º°o]?|[úu]nico))?"
    r"(?:\s*,?\s*(?:inc(?:iso)?\.?\s*)?\b[IVXLC]+\b)?"
    r"(?:\s*,?\s*al[íi]nea\s*[\"“]?[a-z][\"”]?)?"
    r"(?:\s*,?\s*(?:d[aoe]s?|desta|deste)\s+(?:" + DIPLOMA + r"))?")
LEI = re.compile(r"\b(?:" + DIPLOMA + r")")
TRIB = r"STF|STJ|TST|TNU|TSE|STM|TRF\s?\d|TRT\s?\d{1,2}|TJ[A-Z]{2}|TJDFT|TR[A-Z]{0,3}"
SUMULA = re.compile(r"\b[Ss][úu]mula\s+(Vinculante\s+)?(?:n[º°o.]*\s*)?(\d+)(?:\s*,?\s*d[oa]\s+(?:[A-Za-zé]+\s+)?(" + TRIB + r"))?")
TEMA = re.compile(r"\bTema\s+(?:n[º°o.]*\s*)?(\d+)(?:\s*,?\s*d[oa]\s+(" + TRIB + r"))?")
IRDR = re.compile(r"\b(IRDR|IAC)\s*(?:n[º°o.]*\s*)?(\d[\d.\-/]*\d|\d)")
CLASSES = (r"RE|ARE|AI|ADI|ADC|ADO|ADPF|MS|MI|HC|RHC|Rcl|REsp|AREsp|EREsp|RMS|RR|AIRR|ROT|RO|PEDILEF|ApCiv|AgInt(?:\s+no\s+(?:REsp|AREsp|RE|ARE))?"
           r"|AgRg(?:\s+no\s+(?:REsp|AREsp|RE|ARE|HC))?|EDcl(?:\s+no\s+(?:REsp|AREsp|AgInt|RE))?"
           r"|Recurso\s+Especial|Recurso\s+Extraordin[áa]rio|Recurso\s+Inominado|Recurso\s+de\s+Revista|Apela[çc][ãa]o\s+C[íi]vel|Apela[çc][ãa]o"
           r"|Agravo\s+de\s+Instrumento|Agravo\s+Interno|Agravo\s+Regimental|Mandado\s+de\s+Seguran[çc]a|Pedido\s+de\s+Uniformiza[çc][ãa]o")
JULGADO = re.compile(r"\b(" + CLASSES + r")\s*(?:n[º°o.]*\s*)?(\d[\d.\-/]*\d)(?:/[A-Z]{2}\b)?")
CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
VAGAS = [
    r"entendimento\s+(?:j[áa]\s+)?(?:pac[íi]fico|consolidado|dominante|majorit[áa]rio|firme|assente|sedimentado|remansoso|predominante)",
    r"jurisprud[êe]ncia\s+(?:j[áa]\s+)?(?:pac[íi]fica|dominante|majorit[áa]ria|consolidada|firme|remansosa|iterativa|assente|sedimentada|un[íi]ssona|predominante|farta|vasta)",
    r"(?:é|j[áa] é|tornou-se)\s+pac[íi]fico",
    r"(?:os|nossos)\s+tribunais\s+(?:t[êe]m|v[êe]m)\s+(?:decidido|entendendo|reconhecendo|afirmando)",
    r"doutrina\s+(?:majorit[áa]ria|dominante|abalizada|especializada|moderna)",
    r"(?:conforme|segundo|como\s+ensina|como\s+afirma)\s+a\s+(?:melhor\s+)?doutrina",
    r"\b(?:o|a)\s+(?:" + TRIB + r")\s+(?:j[áa]\s+)?(?:decidiu|tem\s+decidido|entende|firmou|pacificou|reconhece|consolidou)",
    r"(?:reiterados|in[úu]meros|v[áa]rios)\s+(?:precedentes|julgados)",
]
VAGA = re.compile("|".join("(?:%s)" % v for v in VAGAS), re.I)
MARCA = re.compile(r"\[(CONFERIR[^\]]*)\]")
ABREVIATURAS = {"rel", "min", "des", "desa", "desemb", "dr", "dra", "juiz", "juíza", "nº", "n", "art", "arts", "p", "pp",
               "ed", "fls", "fl", "inc", "al", "sr", "sra", "prof", "profa", "cf", "dj", "dje", "julg", "publ", "j", "v",
               "rev", "conv", "proc", "trib", "reg", "conf"}


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



DOC_CASO = re.compile(
    r"(?i)(?:\bdocs?\.\s*\d+|\bdocumentos?\b|\b[DT]\d{1,3}\b|\bcarta\b|\blaudo\b|\brelat[óo]rio\b|\bper[íi]cia\b|"
    r"\bparecer\b|\batestado\b|\bcomunica[çc][ãa]o\b|\bextrato\b|\bCNIS\b|\bcarteira\b|\bholerites?\b|"
    r"\btermo de rescis[ãa]o\b|\bmensage(?:m|ns)\b|\be-mail\b|\bcontrato\b|\bcertid[ãa]o\b|\bmatr[íi]cula\b|"
    r"\brecibo\b|\bnotifica[çc][ãa]o\b|\bgerente\b|\bcliente\b|\bperito\b)")
REF_DOC_DEPOIS = re.compile(
    r"(?i)^\W{0,4}(?:conforme\s+|v\.\s+|ver\s+|cf\.\s+)?(?:o\s+|a\s+)?(?:docs?\.\s*\d+|[DT]\d{1,3}\b|documento\s*(?:n[º°o.]*\s*)?\d+)")
CITACAO_LEGAL = re.compile(r"(?i)\b(?:arts?\.|artigos?|lei\b|decreto|c[óo]digo|s[úu]mula|tema\b|ementa|enunciado|"
                           r"ac[óo]rd[ãa]o|voto|rel\.|relator|julgad|tese|doutrina|STF|STJ|TST|TNU|TRF|TRT|TJ[A-Z]{2})")


def eh_trecho_de_documento(linha, i, j):
    """Aspas tiradas de documento do caso (carta, laudo, D1, doc. 1): não são citação de lei ou julgado.

    Vale quando a referência ao documento vem logo depois das aspas ("..." (doc. 1), "..." D1)
    ou na mesma oração, logo antes (a carta de cessação diz "..."), sem palavra de citação legal.
    """
    if REF_DOC_DEPOIS.search(linha[j:j + 40]):
        return True
    oracao = re.split(r"[.;:]\s", linha[max(0, i - 80):i])[-1]
    return bool(DOC_CASO.search(oracao)) and not CITACAO_LEGAL.search(oracao)


def inicio_da_frase(l, pos):
    """Começo da frase que termina em pos (abreviatura como Rel. e Min. não conta como fim)."""
    ini = 0
    for m in re.finditer(r"([\wÀ-ÿº]+)?[.;!?]\s+(?=[A-ZÁÉÍÓÚÂÊÔ\[\"“(])", l[:pos]):
        antes = (m.group(1) or "").lower()
        if antes in ABREVIATURAS or (len(antes) <= 2 and not antes.isdigit()):
            continue
        ini = m.end()
    for m in MARCA.finditer(l[:pos]):
        ini = max(ini, m.end())
    return ini


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def ler_bytes(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod).lstrip("﻿")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_docx(caminho):
    try:
        with zipfile.ZipFile(caminho) as z:
            xml = z.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError):
        erro("'%s' não parece um .docx válido. Salve de novo pelo Word ou converta para .md." % caminho)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    linhas = []
    for p in ElementTree.fromstring(xml).iter(ns + "p"):
        partes = []
        for n in p.iter():
            if n.tag == ns + "t" and n.text:
                partes.append(n.text)
            elif n.tag == ns + "tab":
                partes.append(" ")
            elif n.tag in (ns + "br", ns + "cr"):
                partes.append("\n")
        linhas.extend("".join(partes).split("\n"))
    return linhas


def ler_peca(caminho):
    if not os.path.isfile(caminho):
        erro("não encontrei a peça em '%s'. Confira o caminho (o padrão é "
             "escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md)." % caminho)
    linhas = ler_docx(caminho) if caminho.lower().endswith(".docx") else ler_bytes(caminho).splitlines()
    # cabeçalho YAML, seção interna "Antes de protocolar" e comentários não são a peça
    linhas, _, _ = cortar_interno(linhas)
    if not any(l.strip() for l in linhas):
        erro("a peça '%s' está vazia (depois de tirar o cabeçalho e a seção interna)." % caminho)
    return linhas


def ler_data(txt):
    txt = (txt or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(txt, fmt).date()
        except ValueError:
            pass
    return None


def achar_para_cima(inicio, *partes):
    pasta = os.path.dirname(os.path.abspath(inicio))
    while True:
        if os.path.basename(pasta) == "escritorio":
            alvo = os.path.join(pasta, *partes)
            return alvo if os.path.exists(alvo) else None
        cand = os.path.join(pasta, "escritorio", *partes)
        if os.path.exists(cand):
            return cand
        cima = os.path.dirname(pasta)
        if cima == pasta:
            return None
        pasta = cima


def achar_base(peca):
    """Pasta da base de jurisprudência. Peça sob _treino/: a base de treino primeiro."""
    partes = os.path.abspath(peca).split(os.sep)
    if "_treino" in partes:
        raiz_treino = os.sep.join(partes[:partes.index("_treino") + 1]) or os.sep
        for cand in (os.path.join(raiz_treino, "juridico", "jurisprudencia"),
                     os.path.join(raiz_treino, "jurisprudencia")):
            if os.path.isdir(cand):
                return cand, "base de treino"
    real = achar_para_cima(peca, "04-base", "juridico", "jurisprudencia")
    return real, ("base do escritório" if real else "")


def ler_validade(a):
    if a.validade:
        return a.validade, "opção --validade"
    ficha = a.ficha or achar_para_cima(a.peca, "04-base", "comum", "ficha-juridica.md")
    if ficha and os.path.isfile(ficha):
        for l in ler_bytes(ficha).splitlines():
            m = re.match(r"^\s*-?\s*validade_da_conferencia\s*:\s*(.*)$", l)
            if m:
                valor = m.group(1).split("(")[0]
                n = re.search(r"\d+", valor)
                if n and "PREENCHER" not in valor.upper():
                    return int(n.group(0)), "ficha jurídica (%s)" % ficha
                break
    return 90, "padrão de 90 dias (a ficha jurídica não tem validade_da_conferencia)"


def chave_trib(t):
    return re.sub(r"\s+", "", (t or "").upper())


def ler_base(pasta):
    """Lê os arquivos de tema e devolve as fichas de julgado com as chaves de busca."""
    fichas = []
    if not pasta or not os.path.isdir(pasta):
        return fichas, 0
    temas = 0
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".md") or nome.startswith(("_", ".")):
            continue
        temas += 1
        texto = ler_bytes(os.path.join(pasta, nome))
        atual = None
        for l in texto.splitlines():
            if l.startswith("### "):
                partes = [p.strip() for p in re.split(r"\s+·\s+|\s+\|\s+", l[4:].strip())]
                atual = {"tema": nome[:-3], "titulo": l[4:].strip(), "tribunal": partes[0] if partes else "",
                         "numero": partes[1] if len(partes) > 1 else "", "data": partes[2] if len(partes) > 2 else "",
                         "campos": {}}
                fichas.append(atual)
            elif l.startswith("## "):
                atual = None
            elif atual is not None:
                m = re.match(r"^\s*-\s*([^:]{2,60}):\s*(.*)$", l)
                if m:
                    atual["campos"][sem_acento(m.group(1).strip().lower())] = m.group(2).strip()
        for f in fichas:
            if f["tema"] != nome[:-3] or "tipo" in f:
                continue
            num = f["numero"]
            ms, mt = SUMULA.search(num), TEMA.search(num)
            if ms:
                f["tipo"], f["chave"] = "súmula", ms.group(2)
            elif mt:
                f["tipo"], f["chave"] = "tema", mt.group(1)
            else:
                f["tipo"], f["chave"] = "julgado", re.sub(r"\D", "", num)
            conf = f["campos"].get("conferencia no inteiro teor", "")
            md = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", conf)
            f["conf_data"] = ler_data(md.group(0)) if md else None
            cor = "não conferido"
            for c in ("verde", "amarelo", "vermelho"):
                if re.search(r"\b%s\b" % c, conf.lower()) and not re.search(r"verde\s*\|\s*amarelo", conf.lower()):
                    cor = c
            f["conf_cor"] = cor if f["conf_data"] or cor == "não conferido" else "não conferido"
            f["situacao"] = f["campos"].get("situacao", "")
            f["tese"] = f["campos"].get("tese em uma frase", "")
    return fichas, temas


def na_base(cit, fichas):
    for f in fichas:
        if cit["tipo"] == "súmula" and f["tipo"] == "súmula" and f["chave"] == cit["chave"]:
            if not cit.get("trib") or chave_trib(cit["trib"]) == chave_trib(f["tribunal"]):
                return f
        if cit["tipo"] == "tema" and f["tipo"] == "tema" and f["chave"] == cit["chave"]:
            if not cit.get("trib") or chave_trib(cit["trib"]) == chave_trib(f["tribunal"]):
                return f
        if cit["tipo"] in ("julgado", "irdr") and f["tipo"] == "julgado" and cit["chave"] and f["chave"]:
            if cit["chave"] == f["chave"] or (len(cit["chave"]) >= 6 and (cit["chave"] in f["chave"] or f["chave"] in cit["chave"])):
                return f
    return None


def ler_fontes(caminhos):
    fontes = []
    for c in caminhos or []:
        arquivos = []
        if os.path.isdir(c):
            arquivos = [os.path.join(c, n) for n in sorted(os.listdir(c)) if n.endswith((".txt", ".md"))]
        elif os.path.isfile(c):
            arquivos = [c]
        else:
            erro("não encontrei a fonte '%s'." % c)
        for arq in arquivos:
            linhas = ler_bytes(arq).splitlines()
            meta = " ".join(l.lstrip("# ").strip() for l in linhas if l.startswith("#"))
            corpo = " ".join(l for l in linhas if not l.startswith("#"))
            fontes.append({"arquivo": os.path.basename(arq), "meta": meta, "palavras": palavras(corpo)})
    return fontes


def palavras(t):
    return re.findall(r"[\wÀ-ÿ]+(?:-[\wÀ-ÿ]+)*|\(\w+\)", t.lower())


def comparar_aspas(trecho, fontes):
    p = palavras(trecho)
    if not p or not fontes:
        return None
    melhor = None
    for f in fontes:
        fp = f["palavras"]
        n = len(p)
        for i in range(0, max(1, len(fp) - n + 1)):
            if fp[i:i + n] == p:
                return {"resultado": "bate", "fonte": f["arquivo"], "meta": f["meta"], "diferencas": []}
        for i in range(0, max(1, len(fp) - n + 1)):
            janela = fp[max(0, i - 3):i + n + 3]
            r = difflib.SequenceMatcher(None, p, janela, autojunk=False).ratio()
            if not melhor or r > melhor[0]:
                melhor = (r, f, janela)
    if melhor and melhor[0] >= 0.6:
        r, f, janela = melhor
        sm = difflib.SequenceMatcher(None, p, janela, autojunk=False)
        blocos = sm.get_opcodes()
        # descarta sobra da janela antes do começo e depois do fim do trecho
        while blocos and blocos[0][0] == "delete" and blocos[0][1] == blocos[0][2]:
            blocos.pop(0)
        dif = []
        for op, i1, i2, j1, j2 in blocos:
            if op == "equal":
                continue
            if op == "insert" and (i1 == 0 or i1 == len(p)):
                continue
            dif.append("na peça: '%s' · na fonte: '%s'" % (" ".join(p[i1:i2]) or "(nada)", " ".join(janela[j1:j2]) or "(nada)"))
        if not dif:
            return {"resultado": "bate", "fonte": f["arquivo"], "meta": f["meta"], "diferencas": []}
        return {"resultado": "não bate", "fonte": f["arquivo"], "meta": f["meta"], "diferencas": dif}
    return {"resultado": "não achado", "fonte": ", ".join(f["arquivo"] for f in fontes), "meta": "", "diferencas": []}


def main():
    ap = argparse.ArgumentParser(description="Extrai e pré-classifica as citações de uma peça.")
    ap.add_argument("peca")
    ap.add_argument("--base", help="pasta da base (padrão: 04-base/juridico/jurisprudencia; peça sob _treino/: "
                    "primeiro 07-operacao/_treino/juridico/jurisprudencia)")
    ap.add_argument("--validade", type=int, help="dias de validade da conferência (padrão: ficha ou 90)")
    ap.add_argument("--ficha", help="caminho da ficha-juridica.md")
    ap.add_argument("--hoje", help="data de referência AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--fontes", nargs="*", help="texto oficial salvo (.txt/.md), arquivos ou pastas")
    ap.add_argument("--treino", action="store_true", help="material fictício: fora da base sai vermelho sugerido")
    ap.add_argument("--vagas", default="", help="expressões vagas a mais, do escritório, separadas por ';'")
    ap.add_argument("--saida", help="grava o relatório neste arquivo .md")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    linhas = ler_peca(a.peca)
    global VAGA
    extras = [re.escape(x.strip()) for x in a.vagas.split(";") if x.strip()]
    if extras:
        VAGA = re.compile("|".join("(?:%s)" % v for v in VAGAS + extras), re.I)
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    if a.hoje and not hoje:
        erro("data '%s' não lida; use AAAA-MM-DD ou DD/MM/AAAA." % a.hoje)
    validade, de_onde = ler_validade(a)
    if a.base and not os.path.isdir(a.base):
        erro("não encontrei a pasta da base em '%s'." % a.base)
    base, base_de = (a.base, "opção --base") if a.base else achar_base(a.peca)
    fichas, n_temas = ler_base(base)
    fontes = ler_fontes(a.fontes)

    cits = []
    usadas = set()  # (linha, posição) de cada marca [CONFERIR] já ligada a uma citação
    for n, l in enumerate(linhas):
        ocupado = []

        def livre(i, j):
            return all(j <= x or i >= y for x, y in ocupado)

        def add(tipo, m, chave="", trib="", ini=None, fim=None):
            i = m.start() if ini is None else ini
            j = m.end() if fim is None else fim
            if not livre(i, j):
                return
            texto = l[i:j].strip().rstrip(",;:")
            ocupado.append((i, j))
            cits.append({"tipo": tipo, "texto": texto, "linha": n + 1, "ini": i, "fim": j,
                         "marca": "", "chave": chave, "trib": trib})

        for m in JULGADO.finditer(l):
            add("julgado", m, re.sub(r"\D", "", m.group(2)))
        for m in CNJ.finditer(l):
            add("julgado", m, re.sub(r"\D", "", m.group(0)))
        for m in SUMULA.finditer(l):
            add("súmula", m, m.group(2), m.group(3) or ("STF" if m.group(1) else ""))
        for m in TEMA.finditer(l):
            add("tema", m, m.group(1), m.group(2) or "")
        for m in IRDR.finditer(l):
            add("irdr", m, re.sub(r"\D", "", m.group(2)))
        for m in ARTIGO.finditer(l):
            add("artigo", m)
        for m in LEI.finditer(l):
            add("lei", m)
        # a marca é a primeira [CONFERIR] depois da citação, antes da próxima citação e do fim da frase
        da_linha = sorted([c for c in cits if c["linha"] == n + 1], key=lambda c: c["ini"])
        for k, c in enumerate(da_linha):
            ate = da_linha[k + 1]["ini"] if k + 1 < len(da_linha) else len(l)
            trecho_depois = l[c["fim"]:ate]
            m = MARCA.search(trecho_depois)
            if m and m.start() <= 200 and not tem_quebra(trecho_depois[:m.start()]):
                c["marca"] = m.group(1)
                usadas.add((n, c["fim"] + m.start()))

    # trechos entre aspas e em recuo
    aspas = []
    for n, l in enumerate(linhas):
        recuo = l.lstrip().startswith(">")
        for m in re.finditer(r"[\"“]([^\"”]{20,})[\"”]", l):
            aspas.append((n, m.start(), m.end(), m.group(1), recuo))
        if recuo and not re.search(r"[\"“]", l) and len(l.strip("> ").strip()) >= 20:
            aspas.append((n, 0, len(l), l.strip("> ").strip(), True))
    for n, i, j, txt, recuo in aspas:
        l = linhas[n]
        if eh_trecho_de_documento(l, i, j):
            continue  # trecho tirado de documento do caso (carta, laudo, doc. 1): não é citação de lei ou julgado
        mm = MARCA.match(l[j:].lstrip())
        if mm:
            usadas.add((n, j + (len(l[j:]) - len(l[j:].lstrip()))))
        fonte = None
        antes = [c for c in cits if c["linha"] == n + 1 and c["fim"] <= i and c["tipo"] not in ("aspas", "vaga")]
        if antes:
            fonte = antes[-1]
        else:
            k, vistas = n - 1, 0
            while k >= 0 and vistas < 3 and not fonte:
                if linhas[k].strip():
                    vistas += 1
                    cand = [c for c in cits if c["linha"] == k + 1 and c["tipo"] not in ("aspas", "vaga")]
                    if cand:
                        fonte = cand[-1]
                k -= 1
            if not fonte:
                depois = [c for c in cits if c["linha"] == n + 1 and c["ini"] >= j and c["tipo"] not in ("aspas", "vaga")]
                fonte = depois[0] if depois else None
        cits.append({"tipo": "aspas", "texto": txt, "linha": n + 1, "ini": i, "fim": j,
                     "marca": (mm.group(1) if mm else "") or (fonte or {}).get("marca", ""), "chave": "", "trib": "",
                     "de": fonte["texto"] if fonte else "", "de_tipo": fonte["tipo"] if fonte else ""})

    # menções vagas (fora das aspas), só quando a frase não tem citação concreta
    for n, l in enumerate(linhas):
        if l.lstrip().startswith(">"):
            continue
        sem_aspas = re.sub(r"[\"“][^\"”]*[\"”]", lambda m: " " * len(m.group(0)), l)
        for m in VAGA.finditer(sem_aspas):
            ini = max(sem_aspas.rfind(".", 0, m.start()), sem_aspas.rfind(";", 0, m.start())) + 1
            fim_f = [p for p in (sem_aspas.find(".", m.end()), sem_aspas.find(";", m.end())) if p >= 0]
            fim = min(fim_f) if fim_f else len(sem_aspas)
            concreta = [c for c in cits if c["linha"] == n + 1 and c["tipo"] in ("julgado", "súmula", "tema", "irdr")
                        and ini <= c["ini"] < fim]
            if concreta:
                continue
            cits.append({"tipo": "vaga", "texto": l[m.start():m.end()], "linha": n + 1, "ini": m.start(), "fim": m.end(),
                         "marca": "", "chave": "", "trib": "", "frase": l[ini:fim].strip()})

    # marca [CONFERIR] sem citação reconhecida (o molde "[TRIBUNAL], [CLASSE] nº [NÚMERO], Rel. [NOME]",
    # julgado sem número, norma sem artigo): vira citação pendente, com o trecho da frase
    for n, l in enumerate(linhas):
        for m in MARCA.finditer(l):
            if (n, m.start()) in usadas:
                continue
            ini = inicio_da_frase(l, m.start())
            frase = l[ini:m.start()].replace("`", "").replace("**", "").strip().lstrip(">.;,: ").strip().rstrip(",;:")
            if not frase:
                frase = "(marca sem texto antes)"
            norma = bool(re.match(r"(?i)(?:o\s+|a\s+|no\s+|do\s+)?(?:arts?\.|artigos?|lei\b|decreto|c[óo]digo|constitui)", frase)) \
                and not re.search(r"(?i)\brel\.|relator|julgad|s[úu]mula|tema\b|recurso|apela|agravo", frase)
            juris = bool(re.search(r"(?i)\brel\.|relator|julgad|s[úu]mula|tema\b|recurso|apela|agravo|tribunal|\bST[FJ]\b|\bTRF|\bTRT|\bTST\b|\bTNU\b|\bTJ|precedente|entendimento|ac[óo]rd|jurisprud", frase))
            tipo = "norma a identificar" if norma else ("a identificar" if juris else "outra conferencia")
            cits.append({"tipo": tipo, "texto": frase if len(frase) <= 180 else "..." + frase[-180:].split(" ", 1)[-1],
                         "linha": n + 1, "ini": m.start(), "fim": m.end(), "marca": m.group(1),
                         "chave": "", "trib": ""})

    cits.sort(key=lambda c: (c["linha"], c["ini"]))

    pesquisar, portal = [], []
    for c in cits:
        c["base"], c["cor"], c["fazer"] = "", "pendente", ""
        if c["tipo"] == "vaga":
            c["cor"] = "amarelo"
            c["fazer"] = "sem fonte: troque por julgado conferido da base, cite o precedente qualificado conferido ou tire a frase"
            pesquisar.append("tema da frase \"%s\": julgados do tribunal citado, com número, órgão, relator, data e link" % c["frase"][:140])
            continue
        if c["tipo"] == "a identificar":
            c["fazer"] = ("citação marcada sem número reconhecido: achar no Jus IA o que a frase descreve "
                          "(tribunal, classe, número, relator, data) e conferir no inteiro teor; sem fonte, sai da peça")
            pesquisar.append("trecho \"%s\" [%s]: achar a citação que a frase descreve, com número, órgão, relator, "
                             "data e link (depois, inteiro teor no portal do tribunal)" % (c["texto"], c["marca"]))
            continue
        if c["tipo"] == "outra conferencia":
            c["fazer"] = "marca que não é citação (valor, requisito formal, dado): conferir com o advogado; não vai para o Jus IA"
            continue
        if c["tipo"] == "norma a identificar":
            c["fazer"] = "norma marcada sem número reconhecido: completar artigo e lei pela fonte e conferir no texto compilado do portal oficial"
            portal.append("%s [%s]" % (c["texto"], c["marca"]))
            continue
        if c["tipo"] in ("artigo", "lei"):
            if c["tipo"] == "artigo" and not LEI.search(c["texto"]):
                c["fazer"] = "o trecho não diz de qual lei é o artigo: confirme o diploma e confira no texto compilado do portal oficial"
            else:
                c["fazer"] = "conferir no texto compilado do portal oficial: vigência na data dos fatos e na data da peça, redação"
            portal.append(c["texto"])
        elif c["tipo"] == "aspas":
            if not c["de"]:
                c["cor"] = "amarelo"
                c["fazer"] = "trecho entre aspas sem fonte indicada: diga de onde é ou tire as aspas (paráfrase não vai entre aspas)"
            else:
                comp = comparar_aspas(c["texto"], fontes)
                c["comparacao"] = comp
                if not comp:
                    c["fazer"] = "conferir palavra por palavra na fonte de '%s' (salve o texto oficial e rode com --fontes)" % c["de"]
                elif comp["resultado"] == "bate":
                    c["cor"] = "verde"
                    c["base"] = "fonte: %s" % comp["fonte"]
                    c["fazer"] = "aspas batem palavra por palavra com %s; confira a vigência da redação" % comp["fonte"]
                elif comp["resultado"] == "não bate":
                    c["cor"] = "amarelo"
                    c["base"] = "fonte: %s" % comp["fonte"]
                    c["fazer"] = "aspas não batem com %s: %s" % (comp["fonte"], " | ".join(comp["diferencas"]))
                else:
                    c["fazer"] = "não achei este trecho em %s: confira se a fonte salva é a certa" % comp["fonte"]
        else:
            f = na_base(c, fichas)
            if f:
                exemplo = " (EXEMPLO)" if "EXEMPLO" in (f["titulo"] + " ".join(f["campos"].values())) else ""
                c["base"] = "%s.md · %s%s" % (f["tema"], f["conf_cor"] + (" em %s" % f["conf_data"] if f["conf_data"] else ""), exemplo)
                sit = sem_acento(f["situacao"].lower())
                vencida = f["conf_data"] and (hoje - f["conf_data"]).days > validade
                if f["conf_cor"] == "vermelho" or re.match(r"superado\b(?! em parte)", sit):
                    c["cor"] = "vermelho"
                    c["fazer"] = "a base diz %s / situação '%s': tire da peça ou o advogado decide" % (f["conf_cor"], f["situacao"] or "sem situação")
                elif f["conf_cor"] == "verde" and not vencida:
                    if "em parte" in sit:
                        c["cor"] = "amarelo"
                        c["fazer"] = "conferido, mas superado em parte: confira se a peça usa a parte que vale"
                    else:
                        c["cor"] = "verde"
                        c["fazer"] = "conferido na base dentro da validade: confira se a peça usa o julgado para o que ele diz (\"%s\")" % f["tese"][:120]
                elif f["conf_cor"] == "verde" and vencida:
                    c["fazer"] = "conferência da base vencida (%s, mais de %d dias): conferir de novo no inteiro teor" % (f["conf_data"], validade)
                elif f["conf_cor"] == "amarelo":
                    c["cor"] = "amarelo"
                    c["fazer"] = "a base marcou amarelo: veja a nota da ficha e ajuste antes de usar"
                else:
                    c["fazer"] = "está na base sem conferência: conferir no inteiro teor antes de usar (lote da trazer-pesquisa)"
            else:
                c["base"] = "não está"
                onde = {"súmula": "portal do tribunal, página de súmulas", "tema": "portal do tribunal, página de temas",
                        "irdr": "portal do tribunal, página de IRDR e IAC", "julgado": "inteiro teor no portal do tribunal"}[c["tipo"]]
                pesquisar.append("%s: existe? número, órgão, relator, data, situação e o que decide (depois, %s)" % (c["texto"], onde))
                if a.treino:
                    c["cor"] = "vermelho"
                    c["fazer"] = "treino: o número é inventado de propósito (casos-ficticios.md); na conferência real, %s" % onde
                else:
                    c["fazer"] = "não está na base: pesquisar no Jus IA e conferir no %s" % onde
        if not c["marca"] and c["cor"] != "verde" and c["tipo"] not in ("vaga",):
            c["sem_marca"] = True
            c["fazer"] = "SEM MARCA e sem conferência (regra 1 de citacoes.md): marque [CONFERIR] e confira. " + c["fazer"]

    cont = {}
    for c in cits:
        cont[c["tipo"]] = cont.get(c["tipo"], 0) + 1
    cores = {}
    for c in cits:
        cores[c["cor"]] = cores.get(c["cor"], 0) + 1
    sem_marca = [c for c in cits if c.get("sem_marca")]

    resultado = {"arquivo": a.peca, "treino": a.treino, "base": base or "", "temas_na_base": n_temas,
                 "fichas_na_base": len(fichas), "validade": validade, "validade_de": de_onde,
                 "citacoes": [{k: v for k, v in c.items() if k not in ("ini", "fim")} for c in cits],
                 "pesquisar_no_jus_ia": pesquisar, "conferir_no_portal": portal}
    if a.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2, default=str))
        return

    o = []
    o.append("# Conferência de citações · %s%s" % (os.path.basename(a.peca), " · TREINO" if a.treino else ""))
    o.append("")
    o.append("Base: %s%s (%d temas, %d fichas). Validade da conferência: %d dias (%s). Referência: %s." %
             (base or "não encontrada", (" · " + base_de) if base and base_de else "", n_temas, len(fichas),
              validade, de_onde, hoje.isoformat()))
    if not base:
        o.append("Sem base do escritório: todo julgado, súmula e tema vai para a lista do Jus IA.")
    o.append("")
    o.append("## Resumo")
    o.append("")
    nomes = [("artigo", "artigos"), ("lei", "leis sem artigo"), ("súmula", "súmulas"), ("tema", "temas"),
             ("irdr", "IRDR ou IAC"), ("julgado", "julgados"), ("aspas", "trechos entre aspas"), ("vaga", "menções vagas"),
             ("a identificar", "marcas sem citação reconhecida"), ("norma a identificar", "normas marcadas sem número"), ("outra conferencia", "marcas que não são citação")]
    o.append("- %d citações: %s." % (len(cits), ", ".join("%d %s" % (cont[k], v) for k, v in nomes if cont.get(k)) or "nenhuma"))
    o.append("- Cor sugerida: %s. Pendente quer dizer: ainda não conferida na fonte." %
             ", ".join("%s %d" % (k, cores[k]) for k in ("verde", "amarelo", "vermelho", "cinza", "pendente") if cores.get(k)))
    o.append("- Sem marca e sem conferência: %d%s." % (len(sem_marca), (" (" + "; ".join("%s, linha %d" % (c["texto"][:50], c["linha"]) for c in sem_marca) + ")") if sem_marca else ""))
    o.append("")
    o.append("## Citações")
    o.append("")
    o.append("| # | Tipo | Citação como está na peça | Linha | Marca | Base | Cor sugerida | O que fazer |")
    o.append("|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(cits, start=1):
        txt = c["texto"] if c["tipo"] != "aspas" else "\"%s\"%s" % (c["texto"][:90] + ("..." if len(c["texto"]) > 90 else ""), (" (de: %s)" % c["de"]) if c.get("de") else "")
        marca = "sim" if c["marca"] else ("não se aplica" if c["tipo"] == "vaga" else "NÃO")
        o.append("| %d | %s | %s | %d | %s | %s | %s | %s |" % (i, c["tipo"], txt.replace("|", "/"), c["linha"], marca,
                 (c["base"] or "-").replace("|", "/"), c["cor"], c["fazer"].replace("|", "/")))
    o.append("")
    o.append("## Pesquisar no Jus IA")
    o.append("")
    o.extend(["%d. %s" % (i, p) for i, p in enumerate(pesquisar, start=1)] or
             ["Nada: nenhum julgado, súmula, tema ou marca [CONFERIR] fora da base."])
    o.append("")
    o.append("## Conferir no portal oficial da legislação")
    o.append("")
    o.extend(["%d. %s" % (i, p) for i, p in enumerate(portal, start=1)] or ["Nenhuma lei ou artigo citado."])
    o.append("")
    o.append("## Registro da conferência (rascunho, seção 4 de citacoes.md)")
    o.append("")
    o.append("| # | Citação como está na peça | Fonte consultada | Data da consulta | Cor | O que foi feito |")
    o.append("|---|---|---|---|---|---|")
    for i, c in enumerate(cits, start=1):
        txt = c["texto"] if c["tipo"] != "aspas" else "\"%s\"" % c["texto"]
        fonte = c["base"] if c["cor"] in ("verde", "amarelo", "vermelho") and c["base"] and c["base"] != "não está" else ""
        cor = c["cor"] if c["cor"] in ("verde", "amarelo", "vermelho") and (fonte or c["tipo"] in ("vaga", "aspas")) else "pendente"
        if c["cor"] == "vermelho":
            cor = "vermelho"  # o mesmo da tabela de citações: não vai para a peça sem o advogado decidir
        quando = ""
        if fonte:
            quando = hoje.isoformat()
            md = re.search(r"\d{4}-\d{2}-\d{2}", (c.get("comparacao") or {}).get("meta", ""))
            if md:
                quando = md.group(0)
        o.append("| %d | %s | %s | %s | %s | |" % (i, txt.replace("|", "/"), fonte.replace("|", "/"), quando, cor))
    o.append("")
    o.append("Nada aqui tira marca da peça. A marca sai pela tirar_marcas.py, só das linhas verdes do registro conferido.")
    texto = "\n".join(o) + "\n"
    if a.saida:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto)
    sys.stdout.write(texto)


if __name__ == "__main__":
    main()
