#!/usr/bin/env python3
"""Converte a minuta da peça (.md) em .docx no padrão visual do escritório e confere se está pronta.

Cópia própria da minutar-peca (motor-juridico). Funciona sozinha, só com a biblioteca padrão
para conferir; para criar o .docx, precisa da python-docx.

Uso:
    python3 md_para_docx.py <minuta.md> [saida.docx] [--padrao padrao-visual.md] [--forcar]
    python3 md_para_docx.py <minuta.md> --so-conferir
    python3 md_para_docx.py --conferir-docx <minuta.docx>

O que fica fora do .docx (é controle interno do escritório):
- o cabeçalho YAML do topo (entre linhas ---): versão, caso, tese, quem redigiu;
- a seção interna (um título de qualquer nível que começa com "Antes de protocolar" ou
  "Antes de enviar"), até o próximo título do mesmo nível ou maior, ou até a linha
  <!-- fim: antes de protocolar --> (ou <!-- fim: antes de enviar -->);
- comentários HTML (<!-- ... -->).

O que o script confere no corpo da peça:
1. citações por conferir: toda marca [CONFERIR] ou [CONFERIR: ...]. Na peça, citação
   não conferida é pendência: a peça não sai sem a conferir-citacoes (ou o advogado)
   tirar a marca;
2. as outras marcações, com ou sem texto dentro: [A PREENCHER], [A DEFINIR], [A CONFIRMAR];
3. campos em maiúsculas que sobraram: [NOME], [CLIENTE], [PROCESSO], [NÚMERO];
4. trechos entre colchetes que parecem instrução do modelo: [Se houver tutela ...];
5. variáveis do modelo que não foram preenchidas: {{nome_da_variavel}}.
E, na seção interna, os itens de conferência sem marcar ("- [ ]").
"[...]" (supressão dentro de citação) não é pendência.

Enquanto houver qualquer um desses, a primeira linha da saída diz "NÃO ESTÁ PRONTA",
lista o que falta com a linha de cada item, e o .docx NÃO é criado (saída 2). Para criar
mesmo assim (por exemplo, para o advogado ler no Word), acrescente --forcar: o .docx sai,
o que sobrou fica destacado em amarelo e o aviso diz que a peça não pode ser protocolada assim.

Campos entre chaves simples ({DATA DO PROTOCOLO}) são preenchidos de propósito por quem
protocola (regras.md, seção 3). Não impedem criar o .docx nem a conferência do .docx
(--conferir-docx): saem num aviso à parte, "campos para preencher no envio".

--padrao ARQ      lê o padrão visual do escritório (04-base/juridico/padrao-visual.md;
                  se o arquivo não existe, usa o padrão do script e avisa):
                  linhas "chave: valor" com fonte, corpo, espacamento, margem_superior,
                  margem_inferior, margem_esquerda, margem_direita, recuo_primeira_linha,
                  recuo_citacao, corpo_citacao, espacamento_citacao, alinhamento, timbre.
                  Medidas em cm; vírgula ou ponto. Valor [A PREENCHER] é ignorado com aviso.
                  timbre: caminho de um .docx com o papel timbrado (cabeçalho e rodapé).
--so-conferir     confere o .md sem criar o .docx.
--forcar          cria o .docx mesmo com pendência e avisa (nunca para protocolar).
--conferir-docx   confere um .docx já editado (lê só o texto, com a biblioteca padrão).

Saída: 0 quando o .docx foi criado (inclusive com --forcar) ou quando a conferência diz
"sem pendência"; 2 quando não está pronta e nenhum .docx foi criado, ou quando --so-conferir
ou --conferir-docx dizem "não está pronta"; 1 em erro de uso, de arquivo ou quando falta a
python-docx para criar o .docx (a conferência sai do mesmo jeito).
"""

import os
import re
import sys
import unicodedata
import zipfile

RE_CITACAO = re.compile(r"\[CONFERIR[^\]\n]*\]", re.I)
RE_MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]\n]*\]", re.I)
RE_COLCHETE = re.compile(r"\[([^\[\]\n]*)\](?!\()")
RE_VARIAVEL = re.compile(r"\{\{[^{}\n]*\}\}")
RE_CHAVE = re.compile(r"(?<!\{)\{([^{}\n]*[A-Za-zÀ-ÿ][^{}\n]*)\}(?!\})")
RE_CHECK = re.compile(r"^\s*[-*+]\s+\[( |x|X)\]\s+")
RE_CHECK_ABERTO = re.compile(r"^\s*[-*+]\s+\[ \]\s+")
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_FIM_INTERNO = re.compile(r"^\s*<!--\s*fim:\s*antes de (protocolar|enviar)\s*-->\s*$", re.I)
RE_INLINE = re.compile(
    r"(\*\*[^*]+\*\*|__[^_]+__|\*[^*\s][^*]*\*|(?<![\w])_[^_\s][^_]*_(?![\w])|`[^`]+`|\[[^\]]+\]\([^)]+\))"
)
RE_MARCADOR = re.compile(r"^(\s*)[-*+]\s+(.*)$")
RE_NUMERO = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
RE_SEPARADOR_TABELA = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
RE_DESTAQUE = re.compile(
    r"(\{\{[^{}\n]*\}\}|\[[^\[\]\n]*[A-Za-zÀ-ÿ][^\[\]\n]*\]|\{[^{}\n]*[A-Za-zÀ-ÿ][^{}\n]*\})"
)

PADRAO_INICIAL = {
    "fonte": "Times New Roman",
    "corpo": 12.0,
    "espacamento": 1.5,
    "margem_superior": 3.0,
    "margem_inferior": 2.0,
    "margem_esquerda": 3.0,
    "margem_direita": 2.0,
    "recuo_primeira_linha": 2.0,
    "recuo_citacao": 4.0,
    "corpo_citacao": 10.0,
    "espacamento_citacao": 1.0,
    "alinhamento": "justificado",
    "timbre": "",
}
NUMERICOS = {"corpo", "espacamento", "margem_superior", "margem_inferior", "margem_esquerda",
             "margem_direita", "recuo_primeira_linha", "recuo_citacao", "corpo_citacao",
             "espacamento_citacao"}


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def ler(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(codificacao)
        except UnicodeDecodeError:
            continue
    raise ValueError("não consegui ler o arquivo como texto (UTF-8 ou Windows-1252)")


def ler_padrao(caminho):
    """Lê o padrão visual. Devolve (padrao, avisos)."""
    padrao = dict(PADRAO_INICIAL)
    avisos = []
    if not caminho:
        avisos.append("sem --padrao: usei o padrão do script (Times New Roman 12, espaçamento 1,5, "
                      "citação em recuo de 4 cm, corpo 10). Confira com a ficha jurídica.")
        return padrao, avisos
    if not os.path.isfile(caminho):
        avisos.append("não encontrei o padrão visual em %s: usei o padrão do script (Times New Roman 12, "
                      "espaçamento 1,5, citação em recuo de 4 cm, corpo 10). Confira o caminho ou monte o "
                      "padrão visual pela adaptar-juridico." % caminho)
        return padrao, avisos
    base = os.path.dirname(os.path.abspath(caminho))
    achados = 0
    em_codigo = False
    for linha in ler(caminho).splitlines():
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
            continue
        if em_codigo:
            continue
        titulo = RE_TITULO.match(linha.strip())
        if titulo and sem_acento(titulo.group(2)).startswith("exemplo"):
            break
        m = re.match(r"^\s*[-*]?\s*`?([a-z_]+)`?\s*:\s*(.*?)\s*$", linha)
        if not m:
            continue
        chave, valor = m.group(1), m.group(2)
        if chave not in padrao:
            continue
        valor = re.sub(r"\s+\(.*\)$", "", valor).strip().strip("`")
        if not valor or RE_MARCACAO.search(valor) or valor.startswith("["):
            avisos.append("padrão visual: %s sem valor (%s); usei %s" % (chave, valor or "vazio", padrao[chave] or "sem timbre"))
            continue
        if chave in NUMERICOS:
            num = re.match(r"^(\d+(?:[.,]\d+)?)", valor)
            if not num:
                avisos.append("padrão visual: %s com valor que não é número (%s); usei %s" % (chave, valor, padrao[chave]))
                continue
            padrao[chave] = float(num.group(1).replace(",", "."))
        elif chave == "timbre":
            if sem_acento(valor) in ("sem timbre", "nao", "nenhum"):
                padrao["timbre"] = ""
            else:
                candidato = valor if os.path.isabs(valor) else os.path.join(base, valor)
                if not os.path.isfile(candidato) and os.path.isfile(valor):
                    candidato = valor
                padrao["timbre"] = candidato
        else:
            padrao[chave] = valor
        achados += 1
    if not achados:
        avisos.append("o padrão visual não tem nenhuma linha 'chave: valor' que eu reconheça; usei o padrão do script")
    return padrao, avisos


def separar(texto):
    """Marca cada linha como corpo ou interno. Devolve (linhas_corpo, linhas_internas, achou_secao)."""
    linhas = texto.splitlines()
    interno = [False] * len(linhas)

    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for j in range(0, i + 1):
                    interno[j] = True
                break

    achou = False
    i = 0
    em_codigo = False
    while i < len(linhas):
        limpa = linhas[i].strip()
        if limpa.startswith("```"):
            em_codigo = not em_codigo
        m = RE_TITULO.match(limpa) if not em_codigo else None
        titulo = sem_acento(m.group(2)) if m else ""
        if m and (titulo.startswith("antes de protocolar") or titulo.startswith("antes de enviar")):
            achou = True
            nivel = len(m.group(1))
            interno[i] = True
            j = i + 1
            while j < len(linhas):
                lj = linhas[j].strip()
                if RE_FIM_INTERNO.match(lj):
                    interno[j] = True
                    j += 1
                    break
                mj = RE_TITULO.match(lj)
                if mj and len(mj.group(1)) <= nivel:
                    break
                interno[j] = True
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
                resto = depois.split("-->", 1)[1]
                linhas[i] = antes + resto
                if not linhas[i].strip():
                    interno[i] = True
            else:
                linhas[i] = antes
                dentro = True
                if not antes.strip():
                    interno[i] = True

    corpo = [(n + 1, l) for n, l in enumerate(linhas) if not interno[n]]
    internas = [(n + 1, l) for n, l in enumerate(linhas) if interno[n]]
    return corpo, internas, achou


def tipo_do_colchete(conteudo, linha):
    """Classifica um [..] do corpo: None, 'citacao', 'marcacao', 'campo' ou 'instrucao'."""
    bruto = conteudo.strip()
    if bruto in ("", "x", "X") and RE_CHECK.match(linha):
        return None
    if RE_CITACAO.fullmatch("[" + conteudo + "]"):
        return "citacao"
    if RE_MARCACAO.fullmatch("[" + conteudo + "]"):
        return "marcacao"
    letras = [c for c in bruto if c.isalpha()]
    if not letras:
        return None
    primeira = re.split(r"[\s:|,.;/()-]+", bruto)[0]
    letras_primeira = [c for c in primeira if c.isalpha()]
    if letras_primeira and all(c.isupper() for c in letras_primeira):
        return "campo"
    return "instrucao"


def conferir_linhas(corpo, internas):
    pendencias = {"citacao": [], "marcacao": [], "campo": [], "instrucao": [], "variavel": [], "envio": []}
    for numero, linha in corpo:
        for m in RE_COLCHETE.finditer(linha):
            tipo = tipo_do_colchete(m.group(1), linha)
            if tipo:
                pendencias[tipo].append((numero, m.group(0)))
        for m in RE_VARIAVEL.finditer(linha):
            pendencias["variavel"].append((numero, m.group(0)))
        for m in RE_CHAVE.finditer(linha):
            pendencias["envio"].append((numero, m.group(0)))
    abertos = [(n, l.strip()) for n, l in internas if RE_CHECK_ABERTO.match(l)]
    marcados = [(n, l.strip()) for n, l in internas if RE_CHECK.match(l) and not RE_CHECK_ABERTO.match(l)]
    return pendencias, abertos, marcados


ROTULOS = {
    "citacao": "Citações por conferir (rode a conferir-citacoes; a marca só sai depois da conferência na fonte)",
    "marcacao": "Marcações no texto da peça",
    "campo": "Campos em maiúsculas que ainda não foram preenchidos",
    "instrucao": "Trechos entre colchetes que parecem instrução do modelo",
    "variavel": "Variáveis do modelo sem preencher",
    "envio": "Campos para preencher no envio (entre chaves; não impedem: quem protocola preenche no .docx)",
}
NOMES = {"citacao": "citação(ões) por conferir", "marcacao": "marcação(ões)",
         "campo": "campo(s) em maiúsculas", "instrucao": "trecho(s) de instrução",
         "variavel": "variável(is) do modelo sem preencher", "envio": "campo(s) entre chaves sem preencher"}
BLOQUEIAM = ("citacao", "marcacao", "campo", "instrucao", "variavel")


def relatar(pendencias, abertos, marcados, achou_secao, origem, mostrar_linhas=True, chave_bloqueia=False):
    bloqueiam = BLOQUEIAM + (("envio",) if chave_bloqueia else ())
    total = sum(len(pendencias[c]) for c in bloqueiam) + len(abertos)
    if total:
        partes = ["%d %s" % (len(pendencias[c]), NOMES[c]) for c in bloqueiam if pendencias[c]]
        if abertos:
            partes.append("%d conferência(s) da seção interna sem marcar" % len(abertos))
        print("NÃO ESTÁ PRONTA: %s." % "; ".join(partes))
    elif pendencias["envio"] and achou_secao is None:
        print("SEM PENDÊNCIA NO TEXTO DA PEÇA: falta só preencher no envio %d campo(s) entre chaves." % len(pendencias["envio"]))
    elif pendencias["envio"]:
        print("PRONTA PARA GERAR O .DOCX: o texto está resolvido; falta preencher no .docx %d campo(s) entre chaves." % len(pendencias["envio"]))
    else:
        print("SEM PENDÊNCIA NO TEXTO DA PEÇA: revisão, aprovação, assinatura e protocolo continuam com o advogado.")
    print("Arquivo conferido: %s" % origem)
    for chave in ("citacao", "marcacao", "campo", "instrucao", "variavel", "envio"):
        if pendencias[chave]:
            print()
            print("%s:" % ROTULOS[chave])
            for numero, trecho in pendencias[chave]:
                print(("  linha %d: %s" % (numero, trecho)) if mostrar_linhas else ("  %s" % trecho))
    if achou_secao is not None:
        print()
        if achou_secao:
            print("Antes de protocolar: %d item(ns) conferido(s), %d sem marcar." % (len(marcados), len(abertos)))
            for numero, texto in abertos:
                print("  linha %d: %s" % (numero, texto))
        else:
            print("AVISO: não achei a seção interna \"Antes de protocolar\". Confira se as conferências foram feitas.")
    return total


# ---------- montagem do .docx ----------

def celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def trechos(linhas):
    i = 0
    paragrafo = []
    saida = []

    def fechar():
        if paragrafo:
            junto = " ".join(p.strip() for p in paragrafo)
            paragrafo.clear()
            return [("paragrafo", junto)]
        return []

    while i < len(linhas):
        linha = linhas[i]
        limpa = linha.strip()
        if limpa.startswith("```"):
            saida += fechar()
            codigo = []
            i += 1
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                codigo.append(linhas[i])
                i += 1
            saida.append(("codigo", codigo))
            i += 1
            continue
        if not limpa:
            saida += fechar()
            i += 1
            continue
        m = RE_TITULO.match(limpa)
        if m:
            saida += fechar()
            saida.append(("titulo", (len(m.group(1)), m.group(2).strip())))
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", limpa):
            saida += fechar()
            saida.append(("linha", None))
            i += 1
            continue
        if limpa.startswith("|") and i + 1 < len(linhas) and RE_SEPARADOR_TABELA.match(linhas[i + 1]):
            saida += fechar()
            cabeca = celulas(linha)
            corpo = []
            i += 2
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                corpo.append(celulas(linhas[i]))
                i += 1
            saida.append(("tabela", (cabeca, corpo)))
            continue
        m = RE_MARCADOR.match(linha)
        if m:
            saida += fechar()
            nivel = 2 if len(m.group(1).replace("\t", "    ")) >= 2 else 1
            saida.append(("marcador", (nivel, m.group(2).strip())))
            i += 1
            continue
        m = RE_NUMERO.match(linha)
        if m:
            saida += fechar()
            nivel = 2 if len(m.group(1).replace("\t", "    ")) >= 2 else 1
            saida.append(("numero", (nivel, m.group(2).strip())))
            i += 1
            continue
        if limpa.startswith(">"):
            saida += fechar()
            texto = limpa.lstrip(">").strip()
            if saida and saida[-1][0] == "citacao" and texto:
                saida[-1] = ("citacao", saida[-1][1] + " " + texto)
            elif texto:
                saida.append(("citacao", texto))
            i += 1
            continue
        paragrafo.append(linha)
        i += 1
    saida += fechar()
    return saida


def pedacos_inline(texto):
    resultado = []
    pos = 0
    for m in RE_INLINE.finditer(texto):
        if m.start() > pos:
            resultado.append((texto[pos:m.start()], False, False, False))
        t = m.group(0)
        if t.startswith("**") or t.startswith("__"):
            resultado.append((t[2:-2], True, False, False))
        elif t.startswith("`"):
            resultado.append((t[1:-1], False, False, True))
        elif t.startswith("["):
            rotulo, endereco = re.match(r"\[([^\]]+)\]\(([^)]+)\)", t).groups()
            resultado.append(("%s (%s)" % (rotulo, endereco), False, False, False))
        else:
            resultado.append((t[1:-1], False, True, False))
        pos = m.end()
    if pos < len(texto):
        resultado.append((texto[pos:], False, False, False))
    return resultado


def escrever_inline(paragrafo, texto, negrito_base=False, padrao=None, corpo=None):
    from docx.enum.text import WD_COLOR_INDEX
    from docx.shared import Pt

    for trecho, negrito, italico, codigo in pedacos_inline(texto):
        if codigo and RE_DESTAQUE.fullmatch(trecho):
            codigo = False
        for parte in RE_DESTAQUE.split(trecho):
            if not parte:
                continue
            run = paragrafo.add_run(parte)
            run.bold = negrito or negrito_base
            run.italic = italico
            if padrao:
                run.font.name = padrao["fonte"]
            if corpo:
                run.font.size = Pt(corpo)
            if RE_DESTAQUE.fullmatch(parte) and parte.strip("[]{} ") not in ("...", "…"):
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                run.bold = True


def limpar_corpo(doc):
    corpo = doc.element.body
    for filho in list(corpo):
        if not filho.tag.endswith("}sectPr"):
            corpo.remove(filho)


def montar_docx(trechos_md, saida, padrao):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    avisos = []
    doc = None
    if padrao.get("timbre"):
        if os.path.isfile(padrao["timbre"]) and padrao["timbre"].lower().endswith(".docx"):
            doc = Document(padrao["timbre"])
            limpar_corpo(doc)
        else:
            avisos.append("timbre não encontrado ou não é .docx (%s): o .docx saiu sem timbre" % padrao["timbre"])
    if doc is None:
        doc = Document()
        for secao in doc.sections:
            secao.top_margin = Cm(padrao["margem_superior"])
            secao.bottom_margin = Cm(padrao["margem_inferior"])
            secao.left_margin = Cm(padrao["margem_esquerda"])
            secao.right_margin = Cm(padrao["margem_direita"])
    normal = doc.styles["Normal"]
    normal.font.name = padrao["fonte"]
    normal.font.size = Pt(padrao["corpo"])
    alinhar = WD_ALIGN_PARAGRAPH.JUSTIFY if sem_acento(padrao["alinhamento"]).startswith("just") else WD_ALIGN_PARAGRAPH.LEFT

    def formatar(p, recuo_primeira=True):
        p.alignment = alinhar
        p.paragraph_format.line_spacing = padrao["espacamento"]
        p.paragraph_format.space_after = Pt(6)
        if recuo_primeira and padrao["recuo_primeira_linha"]:
            p.paragraph_format.first_line_indent = Cm(padrao["recuo_primeira_linha"])

    contagem = [0, 0]
    for tipo, dados in trechos_md:
        if tipo != "numero":
            contagem = [0, 0]
        if tipo == "titulo":
            nivel, texto = dados
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if nivel == 1 else WD_ALIGN_PARAGRAPH.LEFT
            escrever_inline(p, texto, negrito_base=True, padrao=padrao)
        elif tipo == "paragrafo":
            p = doc.add_paragraph()
            formatar(p)
            escrever_inline(p, dados, padrao=padrao)
        elif tipo in ("marcador", "numero"):
            nivel, texto = dados
            if tipo == "numero":
                if nivel == 1:
                    contagem = [contagem[0] + 1, 0]
                    rotulo = "%d." % contagem[0]
                else:
                    contagem[1] += 1
                    rotulo = "%s)" % "abcdefghijklmnopqrstuvwxyz"[(contagem[1] - 1) % 26]
            else:
                rotulo = "-" if nivel == 1 else "·"
            p = doc.add_paragraph()
            formatar(p, recuo_primeira=False)
            p.paragraph_format.left_indent = Cm(0.9 if nivel == 1 else 1.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.add_run(rotulo + " ").font.name = padrao["fonte"]
            escrever_inline(p, texto, padrao=padrao)
        elif tipo == "citacao":
            p = doc.add_paragraph()
            p.alignment = alinhar
            p.paragraph_format.left_indent = Cm(padrao["recuo_citacao"])
            p.paragraph_format.line_spacing = padrao["espacamento_citacao"]
            p.paragraph_format.space_after = Pt(10)
            escrever_inline(p, dados, padrao=padrao, corpo=padrao["corpo_citacao"])
        elif tipo == "codigo":
            for linha in dados:
                run = doc.add_paragraph().add_run(linha)
                run.font.name = "Courier New"
                run.font.size = Pt(10)
        elif tipo == "linha":
            doc.add_paragraph()
        elif tipo == "tabela":
            cabeca, corpo = dados
            colunas = max([len(cabeca)] + [len(l) for l in corpo])
            tabela = doc.add_table(rows=1 + len(corpo), cols=colunas)
            try:
                tabela.style = "Table Grid"
            except (KeyError, ValueError):
                pass
            for j in range(colunas):
                escrever_inline(tabela.rows[0].cells[j].paragraphs[0], cabeca[j] if j < len(cabeca) else "",
                                negrito_base=True, padrao=padrao)
            for i, linha in enumerate(corpo, start=1):
                for j in range(colunas):
                    escrever_inline(tabela.rows[i].cells[j].paragraphs[0], linha[j] if j < len(linha) else "", padrao=padrao)
            doc.add_paragraph()
    doc.save(saida)
    return avisos


# ---------- conferência de um .docx ----------

def texto_do_docx(caminho):
    try:
        with zipfile.ZipFile(caminho) as z:
            xml = z.read("word/document.xml").decode("utf-8")
    except (zipfile.BadZipFile, KeyError):
        raise ValueError("o arquivo não parece um .docx válido: %s" % caminho)
    paragrafos = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        pedacos = re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", p, flags=re.S)
        texto = "".join(pedacos)
        texto = texto.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")
        if texto.strip():
            paragrafos.append(texto)
    return paragrafos


def valor_da_opcao(argv, nome):
    if nome in argv:
        i = argv.index(nome)
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            return argv[i + 1], argv[:i] + argv[i + 2:]
        return "", argv[:i] + argv[i + 1:]
    return None, argv


def main(argv):
    argv = list(argv[1:])
    padrao_arq, argv = valor_da_opcao(argv, "--padrao")
    opcoes = [a for a in argv if a.startswith("--")]
    args = [a for a in argv if not a.startswith("--")]
    if "--ajuda" in opcoes or "--help" in opcoes:
        print(__doc__)
        return 0
    if padrao_arq == "":
        print("ERRO: --padrao precisa do caminho do padrão visual (04-base/juridico/padrao-visual.md).")
        return 1
    if not args:
        print("ERRO: diga qual minuta converter ou conferir.")
        print("Exemplo: python3 scripts/md_para_docx.py escritorio/07-operacao/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md --padrao escritorio/04-base/juridico/padrao-visual.md")
        return 1

    if "--conferir-docx" in opcoes:
        caminho = args[0]
        if not os.path.isfile(caminho):
            print("ERRO: arquivo não encontrado: %s" % caminho)
            return 1
        try:
            paragrafos = texto_do_docx(caminho)
        except ValueError as erro:
            print("ERRO: %s" % erro)
            return 1
        if not paragrafos:
            print("ERRO: não achei texto nenhum no .docx: %s" % caminho)
            return 1
        pendencias, abertos, marcados = conferir_linhas(list(enumerate(paragrafos, start=1)), [])
        total = relatar(pendencias, abertos, marcados, None, caminho, mostrar_linhas=False)
        return 2 if total else 0

    entrada = args[0]
    if not os.path.isfile(entrada):
        print("ERRO: arquivo não encontrado: %s" % entrada)
        return 1
    if not entrada.lower().endswith(".md"):
        print("ERRO: a entrada precisa ser um arquivo .md (para conferir um .docx, use --conferir-docx)")
        return 1
    try:
        texto = ler(entrada)
        padrao, avisos_padrao = ler_padrao(padrao_arq)
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1

    corpo, internas, achou = separar(texto)
    if not any(l.strip() for _, l in corpo):
        print("ERRO: depois de tirar o cabeçalho interno, a minuta ficou vazia: %s" % entrada)
        return 1
    pendencias, abertos, marcados = conferir_linhas(corpo, internas)
    total = relatar(pendencias, abertos, marcados, achou, entrada)

    if "--so-conferir" in opcoes:
        return 2 if total else 0

    if total and "--forcar" not in opcoes:
        print()
        print("Nenhum .docx foi criado: resolva o que está acima e rode de novo.")
        print("Para criar mesmo assim (para ler no Word, nunca para protocolar), acrescente --forcar.")
        return 2

    saida = args[1] if len(args) > 1 else os.path.splitext(entrada)[0] + ".docx"
    try:
        import docx  # noqa: F401
    except ImportError:
        print()
        print("ERRO: a biblioteca python-docx não está instalada neste ambiente. Nenhum .docx foi criado.")
        print("A minuta continua em: %s" % entrada)
        print("Para gerar o .docx: instale python-docx (pip install python-docx), ou abra o .md no Word")
        print("ou no Google Docs, apague o cabeçalho e a seção \"Antes de protocolar\" e salve como .docx.")
        return 1
    avisos = montar_docx(trechos([l for _, l in corpo]), saida, padrao)
    print()
    print("OK: .docx criado em %s (sem o cabeçalho e sem a seção \"Antes de protocolar\")." % saida)
    for aviso in avisos_padrao + avisos:
        print("Aviso: %s" % aviso)
    if total:
        print("AVISO: criado com --forcar e com pendência. O que sobrou está destacado em amarelo.")
        print("Esta peça não pode ser protocolada assim: resolva no .md e gere de novo sem --forcar.")
    elif pendencias["envio"]:
        print("Os campos entre chaves estão em amarelo no .docx. Preencha e confira com --conferir-docx antes de protocolar.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
