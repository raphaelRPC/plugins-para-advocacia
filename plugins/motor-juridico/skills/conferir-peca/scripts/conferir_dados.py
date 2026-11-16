#!/usr/bin/env python3
"""Conferência mecânica de uma peça (motor-juridico, conferir-peca).

Lê a peça (.md, .txt ou .docx) e aponta, com a linha de cada achado:
  - nome em papel de parte que não é do caso (sobra de outra peça) e código de outro caso;
  - gênero trocado nas palavras de parte (o requerente / a requerente, o autor / a autora);
  - datas divergentes para o mesmo fato (cessação, admissão, dispensa, nascimento...);
  - valor da causa diferente entre o cabeçalho e o fecho;
  - "doc. N" citado sem documento N na lista de documentos;
  - pedido sobre um tema que não aparece nos fatos nem no direito (dano moral, tutela...);
  - pedido que aponta para um item da peça que não existe;
  - marcações que sobraram ([A PREENCHER], [NOME], {{variavel}}, XXX), de qualquer tamanho;
  - campos entre chaves ({DATA DO PROTOCOLO}), que quem envia preenche de propósito: saem
    como aviso "campos para preencher no envio" e não mudam o resultado.

O cabeçalho YAML e a seção interna "Antes de protocolar" (até o próximo título do mesmo
nível ou até <!-- fim: antes de protocolar -->) não são a peça e ficam de fora, como na
md_para_docx.
  - dado sensível que talvez não precise estar na peça (CPF, CID).

A coerência de fundo (o pedido decorre dos fatos? o fato importante do dossiê tem pedido?)
é do fluxo da habilidade, com o advogado. Este script faz só a parte mecânica.

Uso:
  python3 conferir_dados.py PECA.md [--cliente Marta] [--genero feminino]
      [--nomes "Marta,Joana"] [--codigo C-2026-0001] [--docs 6]
      [--temas-extra "rótulo=expressão;..."] [--saida relatorio.md] [--json]

Sem --cliente, o script tenta ler o nome da qualificação ("MARTA SILVA, brasileira").
Sem --genero, usa a qualificação (brasileira, casada) e, sem ela, a maioria.
Sem --docs, lê a lista de documentos da própria peça (seção "Documentos", "Anexos" ou
"Rol de documentos", itens "Doc. N"). Sem lista e sem --docs, avisa e não acusa doc. N.

Sai com código 1 e mensagem clara quando falta o arquivo, ele está vazio ou não dá para ler.
Nunca diz "nada a apontar" sem dizer quanto leu. Só biblioteca padrão.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import zipfile
from xml.etree import ElementTree

PAPEIS = r"autora?|requerente|reclamante|demandante|exequente|impetrante|recorrente|embargante|segurad[oa]|cliente|interessad[oa]|benefici[aá]ri[oa]"
ARTIGOS_M = {"o", "do", "ao", "pelo", "este", "esse", "deste", "desse", "neste", "nesse"}
ARTIGOS_F = {"a", "da", "à", "pela", "esta", "essa", "desta", "dessa", "nesta", "nessa"}
QUALIF_F = r"brasileira|solteira|casada|divorciada|vi[uú]va|separada|aposentada|desempregada|portadora|nascida|inscrita"
QUALIF_M = r"brasileiro|solteiro|casado|divorciado|vi[uú]vo|separado|aposentado|desempregado|portador|nascido|inscrito"
ANONIMIZACAO = {"DOC", "ENDEREÇO", "ENDERECO", "CLIENTE", "PROCESSO", "CONTATO", "CPF", "RG"}
PENDENCIAS = ("A PREENCHER", "A DEFINIR", "A CONFIRMAR")
FATOS_DATA = [
    ("cessação do benefício", r"cessa[çc][ãa]o|cessad[oa]|cessou|\bDCB\b|cancelamento do benef"),
    ("início do benefício", r"\bDIB\b|in[ií]cio do benef[ií]cio|concedid[oa] em"),
    ("requerimento", r"\bDER\b|requerimento administrativo|requereu"),
    ("admissão", r"admiss[ãa]o|admitid[oa]|contratad[oa] em"),
    ("dispensa", r"dispens[ao]|demiss[ãa]o|demitid[oa]|rescis[ãa]o|desligad[oa]"),
    ("nascimento", r"nasciment|nascid[oa]"),
    ("casamento", r"casament|casaram|casou"),
    ("separação de fato", r"separa[çc][ãa]o de fato|separaram"),
    ("óbito", r"[óo]bito|faleceu|falecimento"),
    ("acidente", r"acidente"),
    ("audiência", r"audi[êe]ncia"),
    ("perícia", r"per[ií]cia"),
]
TEMAS_PEDIDO = [
    ("dano moral", r"danos? mora(l|is)|indeniza[çc][ãa]o (por|a t[ií]tulo de) (dano|abalo) moral|abalo moral"),
    ("dano material", r"danos? materia(l|is)|lucros cessantes|danos emergentes"),
    ("dano estético", r"danos? est[ée]tico"),
    ("tutela de urgência ou liminar", r"tutela (de urg[êe]ncia|antecipada|provis[óo]ria|de evid[êe]ncia)|liminar"),
    ("multa diária", r"multa di[áa]ria|astreinte"),
    ("aposentadoria por incapacidade", r"aposentadoria por (incapacidade|invalidez)"),
    ("adicional de 25%", r"adicional de 25|acr[ée]scimo de 25"),
    ("reabilitação profissional", r"reabilita[çc][ãa]o profissional"),
    ("horas extras", r"horas? extras?"),
    ("adicional de insalubridade ou periculosidade", r"insalubridade|periculosidade"),
    ("vínculo de emprego", r"reconhecimento d[oe] v[íi]nculo"),
    ("alimentos", r"\balimentos\b|pens[ãa]o aliment[íi]cia"),
    ("guarda", r"\bguarda\b"),
    ("partilha", r"partilha"),
    ("gratuidade da justiça", r"gratuidade|justi[çc]a gratuita|assist[êe]ncia judici[áa]ria"),
]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


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


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def ler_docx(caminho):
    try:
        with zipfile.ZipFile(caminho) as z:
            xml = z.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError):
        erro("'%s' não parece um .docx válido. Salve de novo pelo Word ou converta para .md." % caminho)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    raiz = ElementTree.fromstring(xml)
    linhas = []
    for p in raiz.iter(ns + "p"):
        partes = []
        for n in p.iter():
            if n.tag == ns + "t" and n.text:
                partes.append(n.text)
            elif n.tag in (ns + "tab",):
                partes.append(" ")
            elif n.tag in (ns + "br", ns + "cr"):
                partes.append("\n")
        linhas.extend("".join(partes).split("\n"))
    return linhas


def ler_peca(caminho):
    if not os.path.isfile(caminho):
        erro("não encontrei a peça em '%s'. Confira o caminho (o padrão é "
             "escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md)." % caminho)
    if caminho.lower().endswith(".docx"):
        linhas = ler_docx(caminho)
    else:
        with open(caminho, "rb") as f:
            bruto = f.read()
        texto = None
        for cod in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                texto = bruto.decode(cod)
                break
            except UnicodeDecodeError:
                continue
        linhas = texto.lstrip("﻿").splitlines()
    # cabeçalho YAML, seção interna "Antes de protocolar" e comentários não são a peça:
    # viram linha vazia (a numeração das linhas não muda)
    linhas, achou, n_interno = cortar_interno(linhas)
    if not any(l.strip() for l in linhas):
        erro("a peça '%s' está vazia (depois de tirar o cabeçalho e a seção interna)." % caminho)
    return linhas, achou, n_interno


def sem_citacoes_literais(linha):
    """Troca o que está entre aspas por espaços (o texto citado não é da peça)."""
    if linha.lstrip().startswith(">"):
        return " " * len(linha)
    return re.sub(r"[\"“][^\"”]*[\"”]", lambda m: " " * len(m.group(0)), linha)


def eh_titulo(linha):
    l = linha.strip()
    if not l:
        return 0
    m = re.match(r"^(#{1,6})\s+\S", l)
    if m:
        return len(m.group(1))
    if len(l) > 70 or l.endswith((".", ",", ";", ":")):
        return 0
    letras = re.sub(r"[^A-Za-zÀ-ÿ]", "", l)
    if len(l) >= 3 and letras and letras.isupper():
        return 2
    # texto vindo do Word: "III. Dos pedidos", "II.1 Da competência", "Documentos"
    m = re.match(r"^([IVXLC]+)((?:\.\d+)*)[.)\s-]+\S", l)
    if m:
        return 3 if m.group(2) else 2
    if re.match(r"^(d[oa]s?\s+\w+|pedidos?|documentos|anexos|rol de documentos|provas|fatos|direito)\b", sem_acento(l.lower())) and len(l.split()) <= 6:
        return 2
    return 0


def secoes(linhas):
    """Devolve (inicio, fim, nivel, titulo) de cada seção."""
    titulos = [(i, eh_titulo(l), l.strip("# ").strip()) for i, l in enumerate(linhas) if eh_titulo(l)]
    out = []
    for k, (i, nivel, titulo) in enumerate(titulos):
        fim = len(linhas)
        for j, n2, _ in titulos[k + 1:]:
            if n2 <= nivel:
                fim = j
                break
        out.append((i, fim, nivel, titulo))
    return out


def faixa(secs, chave):
    for i, fim, nivel, titulo in secs:
        if re.search(chave, sem_acento(titulo.lower())):
            return (i, fim)
    return None


def ler_data(txt):
    txt = txt.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", txt)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", txt)
    if m:
        return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1)))
    m = re.fullmatch(r"(\d{1,2})º? de ([a-zç]+) de (\d{4})", sem_acento(txt.lower()))
    if m:
        for n, p in enumerate(MESES, start=1):
            if m.group(2).startswith(p):
                return "%s-%02d-%02d" % (m.group(3), n, int(m.group(1)))
    return None


def trecho(linha, ini, fim, folga=35):
    a = max(0, ini - folga)
    b = min(len(linha), fim + folga)
    t = linha[a:b].strip()
    return ("..." if a > 0 else "") + t + ("..." if b < len(linha) else "")


def main():
    ap = argparse.ArgumentParser(description="Conferência mecânica de uma peça jurídica.")
    ap.add_argument("peca")
    ap.add_argument("--cliente", help="primeiro nome da cliente ou do cliente do caso")
    ap.add_argument("--genero", help="feminino ou masculino (f ou m)")
    ap.add_argument("--nomes", default="", help="outros nomes que são do caso, separados por vírgula")
    ap.add_argument("--codigo", help="código do caso (C-AAAA-NNNN); outro código na peça é alerta")
    ap.add_argument("--docs", type=int, help="quantos documentos a peça tem (doc. 1 a N)")
    ap.add_argument("--temas-extra", default="", help="temas de pedido do escritório: 'rótulo=expressão;rótulo2=expressão2'")
    ap.add_argument("--saida", help="grava o relatório neste arquivo .md")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    a = ap.parse_args()

    linhas, achou_interno, n_interno = ler_peca(a.peca)
    for item in [x for x in a.temas_extra.split(";") if "=" in x]:
        rotulo, expr = item.split("=", 1)
        try:
            re.compile(expr.strip())
        except re.error:
            erro("a expressão do tema '%s' não é válida: %s" % (rotulo.strip(), expr.strip()))
        TEMAS_PEDIDO.append((rotulo.strip(), expr.strip()))
    limpas = [sem_citacoes_literais(l) for l in linhas]
    secs = secoes(linhas)
    f_ped = faixa(secs, r"pedido")
    f_doc = faixa(secs, r"^(documentos|anexos|rol de documentos|documentos anexos|lista de documentos)")
    alertas, avisos, conferido = [], [], []
    if achou_interno:
        conferido.append("seção interna \"Antes de protocolar\" fora da conferência (%d linhas: é controle do escritório, não é a peça)" % n_interno)

    def alerta(tipo, n, txt, fazer):
        alertas.append({"tipo": tipo, "linha": n + 1, "trecho": txt, "fazer": fazer})

    # 1. cliente e gênero esperados pela qualificação
    cliente, genero_q, linha_q = a.cliente, None, None
    for n, l in enumerate(linhas):
        m = re.match(r"^\s*\**([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ' ]{2,80}?)\**\s*,\s*(" + QUALIF_F + "|" + QUALIF_M + r")\b", l)
        if m:
            linha_q = n
            if not cliente:
                cliente = m.group(1).split()[0].title()
            genero_q = "feminino" if re.match(QUALIF_F, m.group(2)) else "masculino"
            break
    genero = None
    if a.genero:
        genero = "feminino" if a.genero.lower().startswith("f") else "masculino"
    elif genero_q:
        genero = genero_q

    permitidos = {sem_acento(x.strip().lower()) for x in a.nomes.split(",") if x.strip()}
    if cliente:
        permitidos.add(sem_acento(cliente.lower()))

    # 2. nomes em papel de parte e códigos de outro caso
    usados = set()
    padrao_nome = re.compile(r"\b(o|a|do|da|ao|à|pelo|pela)\s+(" + PAPEIS + r")\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)", re.I)
    for n, l in enumerate(limpas):
        for m in padrao_nome.finditer(l):
            nome = m.group(3)
            if not nome[0].isupper() or nome.lower() in {"que", "não", "nao", "por", "para"}:
                continue
            if cliente and sem_acento(nome.lower()) not in permitidos:
                art = m.group(1).lower()
                gen_txt = ""
                if genero:
                    masc = art in ARTIGOS_M or m.group(2).lower() == "autor"
                    if (genero == "feminino") == masc:
                        gen_txt = ", e no gênero trocado"
                alerta("nome de fora do caso", n, trecho(linhas[n], m.start(), m.end()),
                       "'%s' não é %s nem está nos nomes do caso%s. Sobra de outra peça? Troque e procure o resto do parágrafo." % (nome, cliente, gen_txt))
                usados.add((n, m.start(1)))
    for n, l in enumerate(limpas):
        for m in re.finditer(r"\bC-\d{4}-\d{4}\b", l):
            if a.codigo and m.group(0) != a.codigo:
                alerta("código de outro caso", n, trecho(linhas[n], m.start(), m.end()),
                       "o caso é %s. Tire o código %s." % (a.codigo, m.group(0)))
    conferido.append("nomes em papel de parte (cliente: %s)" % (cliente or "não identificada; passe --cliente"))

    # 3. gênero nas palavras de parte
    padrao_gen = re.compile(r"\b(o|a|do|da|ao|à|pelo|pela|este|esta|esse|essa)\s+(" + PAPEIS + r")\b", re.I)
    ocorr = []
    for n, l in enumerate(limpas):
        for m in padrao_gen.finditer(l):
            art, nome = m.group(1).lower(), m.group(2).lower()
            if nome in ("segurado", "segurada", "cliente", "interessado", "interessada", "beneficiario", "beneficiária", "beneficiaria", "beneficiário"):
                continue  # uso genérico comum ("o segurado tem direito"); fica de fora
            if nome == "autora":
                g = "feminino"
            elif nome == "autor":
                g = "masculino"
            elif art in ARTIGOS_F:
                g = "feminino"
            elif art in ARTIGOS_M:
                g = "masculino"
            else:
                continue
            ocorr.append((n, m.start(), m.end(), g, m.group(0)))
    if ocorr and not genero:
        fem = sum(1 for o in ocorr if o[3] == "feminino")
        genero = "feminino" if fem * 2 >= len(ocorr) else "masculino"
        avisos.append("gênero da parte pela maioria das ocorrências (%s); confirme com --genero" % genero)
    trocados = [o for o in ocorr if genero and o[3] != genero and (o[0], o[1]) not in usados]
    if trocados:
        onde = "; ".join("linha %d: '%s'" % (n + 1, txt) for n, ini, fim, g, txt in trocados)
        alerta("gênero trocado", trocados[0][0], "%d trecho(s): %s" % (len(trocados), onde),
               "a parte é do gênero %s. Corrija cada trecho e releia as concordâncias em volta (segurada, ela)." % genero)
    conferido.append("gênero das palavras de parte (%d ocorrências, esperado: %s)" % (len(ocorr), genero or "a confirmar"))

    # 4. datas por fato
    pad_data = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}º? de [A-Za-zç]+ de \d{4})\b")
    por_fato, total_datas = {}, 0
    for n, l in enumerate(limpas):
        for m in pad_data.finditer(l):
            d = ler_data(m.group(1))
            if not d:
                continue
            total_datas += 1
            antes = sem_acento(l[max(0, m.start() - 70):m.start()].lower())
            achado = None
            melhor = -1
            for nome, rx in FATOS_DATA:
                for mm in re.finditer(sem_acento(rx), antes, re.I):
                    if mm.start() > melhor:
                        melhor, achado = mm.start(), nome
            if achado:
                por_fato.setdefault(achado, []).append((d, n, m.start(), m.end()))
    for fato, lista in por_fato.items():
        distintas = sorted({x[0] for x in lista})
        if len(distintas) > 1:
            onde = "; ".join("%s na linha %d" % (x[0], x[1] + 1) for x in lista)
            n0 = lista[0][1]
            alerta("datas divergentes", n0, "%s: %s" % (fato, onde),
                   "a mesma data (%s) aparece diferente na peça. Confira no documento e use uma só." % fato)
    conferido.append("datas (%d lidas; fatos com data: %s)" % (total_datas, ", ".join(sorted(por_fato)) or "nenhum"))

    # 5. valores
    pad_valor = re.compile(r"R\$\s?([\d.]+,\d{2}|\d+)")
    causa, total_val = [], 0
    for n, l in enumerate(limpas):
        for m in pad_valor.finditer(l):
            total_val += 1
            antes = sem_acento(l[:m.start()].lower())
            if re.search(r"valor da causa|a causa o valor|atribui-se a causa|da-se a causa|valor de alcada da causa", antes):
                causa.append((m.group(1), n))
    if len({c[0] for c in causa}) > 1:
        alerta("valor da causa divergente", causa[0][1],
               "; ".join("R$ %s na linha %d" % (c[0], c[1] + 1) for c in causa),
               "o valor da causa precisa ser um só. Confira o cálculo e corrija os dois pontos.")
    elif not causa:
        avisos.append("não achei o valor da causa; se a peça precisa dele, inclua `[CONFERIR]` o requisito")
    conferido.append("valores (%d em R$; valor da causa em %d ponto(s))" % (total_val, len(causa)))

    # 6. documentos citados x lista
    lista_docs = set()
    if a.docs:
        lista_docs = set(range(1, a.docs + 1))
    elif f_doc:
        for n in range(f_doc[0] + 1, f_doc[1]):
            m = re.match(r"^\s*[-*]?\s*(?:doc(?:umento)?\.?|anexo)\s*(?:n[º°o.]*\s*)?(\d+)", linhas[n], re.I)
            if m:
                lista_docs.add(int(m.group(1)))
    citados = {}
    pad_doc = re.compile(r"\b(?:docs?\.|documentos?|anexos?)\s*(?:n[º°o.]*\s*)?(\d+(?:\s*(?:,|e|a)\s*\d+)*)", re.I)
    for n, l in enumerate(limpas):
        if f_doc and f_doc[0] <= n < f_doc[1]:
            continue
        for m in pad_doc.finditer(l):
            grupo = m.group(1)
            nums = [int(x) for x in re.findall(r"\d+", grupo)]
            if re.search(r"\d+\s*a\s*\d+", grupo) and len(nums) == 2:
                nums = list(range(nums[0], nums[1] + 1))
            for x in nums:
                citados.setdefault(x, []).append((n, m.start(), m.end()))
    if lista_docs:
        for x in sorted(citados):
            if x not in lista_docs:
                n, ini, fim = citados[x][0]
                alerta("documento que não existe", n, trecho(linhas[n], ini, fim),
                       "a peça cita o doc. %d, e a lista vai até o doc. %d. Falta juntar ou o número está errado." % (x, max(lista_docs)))
        nao_citados = sorted(lista_docs - set(citados))
        if nao_citados:
            avisos.append("documentos da lista que a peça não cita: %s (confira se precisam estar lá)" % ", ".join("doc. %d" % x for x in nao_citados))
    elif citados:
        avisos.append("não achei a lista de documentos; rode com --docs N para conferir os %d números citados" % len(citados))
    conferido.append("documentos (%d números citados; lista: %s)" % (len(citados), ("doc. 1 a %d" % max(lista_docs)) if lista_docs else "não achada"))

    # 7. pedidos: tema sem fundamento e item que não existe
    if f_ped:
        fora = "\n".join(l for k, l in enumerate(limpas) if not (f_ped[0] <= k < f_ped[1]) and not (f_doc and f_doc[0] <= k < f_doc[1]))
        fora_s = sem_acento(fora.lower())
        codigos_itens = {re.match(r"^#*\s*([IVXLC]+(?:\.\d+)*)", l.strip("# ").strip() + " ").group(1)
                         for l in linhas if eh_titulo(l) and re.match(r"^#*\s*[IVXLC]+(?:\.\d+)*[\s.)]", l.strip("# ").strip() + " ")}
        n_ped = 0
        for n in range(f_ped[0] + 1, f_ped[1]):
            l = limpas[n]
            if not re.match(r"^\s*(\d+[.)]|[a-z]\)|[-*])\s+\S", l):
                continue
            n_ped += 1
            ls = sem_acento(l.lower())
            for nome, rx in TEMAS_PEDIDO:
                if re.search(sem_acento(rx), ls) and not re.search(sem_acento(rx), fora_s):
                    alerta("pedido sem fundamento", n, trecho(linhas[n], 0, min(len(linhas[n]), 60), 40),
                           "o pedido de %s não tem nenhum fato nem fundamento na peça. Fundamente com o dossiê ou tire o pedido (o advogado decide)." % nome)
            for ref in re.findall(r"\bitens?\s+([IVXLC]+(?:\.\d+)*)", l):
                if codigos_itens and ref not in codigos_itens:
                    alerta("pedido aponta item que não existe", n, trecho(linhas[n], 0, 60, 40),
                           "o pedido cita o item %s, que não está na peça." % ref)
        conferido.append("pedidos (%d itens lidos)" % n_ped)
    else:
        avisos.append("não achei a seção de pedidos; a conferência de pedido sem fundamento não rodou")

    # 8. marcações que sobraram e dados para o sistema do escritório
    marcas_citacao, anon, campos_envio = 0, {}, []
    for n, l in enumerate(linhas):
        for m in re.finditer(r"\[([^\]\[]+)\]", l):
            dentro = m.group(1).strip()
            cabeca = dentro.split(":")[0].strip()
            if cabeca.upper().startswith("CONFERIR"):
                marcas_citacao += 1
            elif cabeca.upper() in ANONIMIZACAO:
                anon[cabeca.upper()] = anon.get(cabeca.upper(), 0) + 1
            elif cabeca.startswith(PENDENCIAS) or (cabeca.upper() == cabeca and re.search(r"[A-Z]", cabeca)):
                alerta("marcação que sobrou", n, trecho(l, m.start(), m.end()),
                       "complete '%s' antes de a peça seguir." % m.group(0))
        for m in re.finditer(r"\{\{[^{}]+\}\}|\bX{3,}\b|_{4,}|\?\?\?|\b(?:TODO|inserir aqui|completar aqui|lorem ipsum)\b", l, re.I):
            alerta("marcação que sobrou", n, trecho(l, m.start(), m.end()), "complete ou tire '%s'." % m.group(0))
        # {CAMPO DO ENVIO}: quem protocola preenche de propósito (regras.md, seção 3); não é pendência
        for m in re.finditer(r"(?<!\{)\{([^{}]+)\}(?!\})", l):
            if re.search(r"[A-Za-zÀ-ÿ]", m.group(1)):
                campos_envio.append("%s (linha %d)" % (m.group(0), n + 1))
    if marcas_citacao:
        avisos.append("%d marcas [CONFERIR] de citação: são da conferir-citacoes" % marcas_citacao)
    if campos_envio:
        avisos.append("campos para preencher no envio (entre chaves, não mudam o resultado): %s" % "; ".join(campos_envio))
    if anon:
        avisos.append("dados que entram pelo sistema do escritório antes do protocolo: %s" %
                      ", ".join("[%s] %d" % (k, v) for k, v in sorted(anon.items())))
    conferido.append("marcações ([CONFERIR] de citação: %d)" % marcas_citacao)

    # 9. dado sensível
    for n, l in enumerate(linhas):
        if re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", l):
            avisos.append("linha %d: CPF escrito na peça; confirme se precisa e se é o da parte certa" % (n + 1))
        if re.search(r"\bCID[- ]?(10|11)?\b|\b[A-TV-Z]\d{2}\.\d\b", l):
            avisos.append("linha %d: código de doença (CID) na peça; dado sensível, use só se necessário" % (n + 1))

    resultado = {
        "arquivo": a.peca,
        "linhas_lidas": sum(1 for l in linhas if l.strip()),
        "cliente": cliente,
        "genero": genero,
        "alertas": alertas,
        "avisos": avisos,
        "conferido": conferido,
        "campos_do_envio": campos_envio,
        "dados": "com-alerta" if alertas else "ok",
    }
    if a.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return
    out = []
    out.append("# Conferência de dados · %s" % os.path.basename(a.peca))
    out.append("")
    out.append("Li %d linhas com texto. Cliente: %s. Gênero esperado: %s." %
               (resultado["linhas_lidas"], cliente or "não identificada", genero or "a confirmar"))
    out.append("")
    out.append("## Alertas (%d)" % len(alertas))
    out.append("")
    if alertas:
        out.append("| # | Tipo | Linha | Trecho | O que fazer |")
        out.append("|---|---|---|---|---|")
        for i, x in enumerate(alertas, start=1):
            out.append("| %d | %s | %d | %s | %s |" % (i, x["tipo"], x["linha"], x["trecho"].replace("|", "/"), x["fazer"].replace("|", "/")))
    else:
        out.append("Nenhum alerta mecânico nas verificações abaixo. A coerência de fundo continua com o fluxo e o advogado.")
    out.append("")
    out.append("## Avisos")
    out.append("")
    out.extend(["- " + x for x in avisos] or ["- nenhum"])
    out.append("")
    out.append("## O que foi verificado")
    out.append("")
    out.extend(["- " + x for x in conferido])
    out.append("")
    out.append("Resultado para o pecas.csv: dados = %s" % resultado["dados"])
    texto = "\n".join(out) + "\n"
    if a.saida:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto)
    sys.stdout.write(texto)


if __name__ == "__main__":
    main()
