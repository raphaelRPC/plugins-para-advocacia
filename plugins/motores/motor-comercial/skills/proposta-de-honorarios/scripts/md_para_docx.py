#!/usr/bin/env python3
"""Converte a proposta de honorários (.md) em .docx e confere se está pronta.

Uso:
    python3 md_para_docx.py <proposta.md> [saida.docx] [--manter-cabecalho] [--forcar]
    python3 md_para_docx.py <proposta.md> --so-conferir
    python3 md_para_docx.py --conferir-docx <proposta.docx>

O que fica fora do .docx (é controle interno do escritório):
- o cabeçalho YAML do topo (entre linhas ---): versão, dono, contato;
- a seção "Antes de enviar" (um título de qualquer nível que começa com
  "Antes de enviar"), até o próximo título do mesmo nível ou maior, ou até a
  linha <!-- fim: antes de enviar -->;
- comentários HTML (<!-- ... -->).

O que o script confere no corpo (o que vai ao cliente):
1. marcações, com ou sem texto dentro: [A PREENCHER], [A DEFINIR],
   [A CONFIRMAR], [CONFERIR], [CONFERIR na tabela vigente] etc.;
2. campos em maiúsculas que sobraram: [NOME], [DATA DA VALIDADE], [X];
3. trechos entre colchetes que parecem instrução do modelo: [Se houver ...].
E, na seção "Antes de enviar", os itens de conferência sem marcar ("- [ ]").

Enquanto houver qualquer um desses, a primeira linha da saída diz
"NÃO ESTÁ PRONTO PARA ENVIAR", lista o que falta com a linha de cada item,
e o .docx NÃO é criado (saída 2). Para criar mesmo assim (por exemplo, para
ler no Word), acrescente --forcar: o .docx sai, o que sobrou fica destacado
em amarelo e o aviso diz que não pode ir ao cliente assim.

Campos do envio entre chaves ({QUALIFICAÇÃO COMPLETA}, {DADOS PARA
PAGAMENTO}, {LINK}): são preenchidos de propósito por quem envia, no .docx,
no sistema do escritório. Não impedem criar o .docx: a primeira linha diz
"PRONTO PARA GERAR O .DOCX" e lista os campos, destacados em amarelo no
.docx. Na conferência do .docx (--conferir-docx), chave que sobrou é
pendência: o documento ainda não pode ir ao cliente.
Sem nenhuma pendência e sem chaves, a primeira linha diz "PRONTO PARA ENVIAR".

--so-conferir     confere o .md sem criar o .docx.
--forcar          cria o .docx mesmo com pendência e avisa (não use para
                  enviar ao cliente).
--conferir-docx   confere um .docx já preenchido pelo escritório (lê só o
                  texto, com a biblioteca padrão, e não mostra o conteúdo
                  preenchido; mostra só o que ainda está pendente).

Saída: 0 quando o .docx foi criado (inclusive com --forcar) ou quando a
conferência diz "pronto" (no .md, com ou sem campos do envio); 2 quando não
está pronto e nenhum .docx foi criado, ou quando --so-conferir ou
--conferir-docx dizem "não está pronto"; 1 em erro de uso, de arquivo ou
quando falta a biblioteca python-docx para criar o .docx (nesse caso a
conferência sai do mesmo jeito).
"""

import os
import re
import sys
import unicodedata
import zipfile

RE_MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]\n]*\]", re.I)
RE_COLCHETE = re.compile(r"\[([^\[\]\n]*)\](?!\()")
RE_CHECK = re.compile(r"^\s*[-*+]\s+\[( |x|X)\]\s+")
RE_CHECK_ABERTO = re.compile(r"^\s*[-*+]\s+\[ \]\s+")
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_FIM_INTERNO = re.compile(r"^\s*<!--\s*fim:\s*antes de enviar\s*-->\s*$", re.I)
RE_INLINE = re.compile(
    r"(\*\*[^*]+\*\*|__[^_]+__|\*[^*\s][^*]*\*|(?<![\w])_[^_\s][^_]*_(?![\w])|`[^`]+`|\[[^\]]+\]\([^)]+\))"
)
RE_MARCADOR = re.compile(r"^(\s*)[-*+]\s+(.*)$")
RE_NUMERO = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
RE_SEPARADOR_TABELA = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
RE_DESTAQUE = re.compile(r"(\[[^\[\]\n]*[A-Za-zÀ-ÿ][^\[\]\n]*\]|\{[^{}\n]*[A-Za-zÀ-ÿ][^{}\n]*\})")
RE_CHAVE = re.compile(r"\{([^{}\n]*[A-Za-zÀ-ÿ][^{}\n]*)\}")


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


def separar(texto, manter_yaml=False):
    """Marca cada linha como corpo ou interno. Devolve (linhas_corpo, linhas_internas, achou_secao).

    linhas_corpo e linhas_internas são listas de (numero_da_linha, texto).
    """
    linhas = texto.splitlines()
    interno = [False] * len(linhas)

    # 1. YAML do topo
    if linhas and linhas[0].strip() == "---" and not manter_yaml:
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for j in range(0, i + 1):
                    interno[j] = True
                break

    # 2. Seção "Antes de enviar"
    achou = False
    i = 0
    em_codigo = False
    while i < len(linhas):
        limpa = linhas[i].strip()
        if limpa.startswith("```"):
            em_codigo = not em_codigo
        m = RE_TITULO.match(limpa) if not em_codigo else None
        if m and sem_acento(m.group(2)).startswith("antes de enviar"):
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

    # 3. Comentários HTML (podem ocupar várias linhas)
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
    """Classifica um [..] do corpo: None (não é pendência), 'marcacao', 'campo' ou 'instrucao'."""
    bruto = conteudo.strip()
    if bruto in ("", "x", "X") and RE_CHECK.match(linha):
        return None
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
    pendencias = {"marcacao": [], "campo": [], "instrucao": [], "envio": []}
    for numero, linha in corpo:
        for m in RE_COLCHETE.finditer(linha):
            tipo = tipo_do_colchete(m.group(1), linha)
            if tipo:
                pendencias[tipo].append((numero, m.group(0)))
        for m in RE_CHAVE.finditer(linha):
            pendencias["envio"].append((numero, m.group(0)))
    abertos = [(n, l.strip()) for n, l in internas if RE_CHECK_ABERTO.match(l)]
    marcados = [(n, l.strip()) for n, l in internas if RE_CHECK.match(l) and not RE_CHECK_ABERTO.match(l)]
    return pendencias, abertos, marcados


ROTULOS = {
    "marcacao": "Marcações no texto que vai ao cliente",
    "campo": "Campos em maiúsculas que ainda não foram preenchidos",
    "instrucao": "Trechos entre colchetes que parecem instrução do modelo",
    "envio": "Campos do envio entre chaves (quem envia preenche no .docx, antes de enviar)",
}

BLOQUEIAM = ("marcacao", "campo", "instrucao")


def relatar(pendencias, abertos, marcados, achou_secao, origem, mostrar_linhas=True, chave_bloqueia=False):
    """Mostra o resultado e devolve o total de pendências que impedem o .docx.

    chave_bloqueia=True (conferência do .docx): campo do envio que sobrou é pendência.
    """
    bloqueiam = BLOQUEIAM + (("envio",) if chave_bloqueia else ())
    total = sum(len(pendencias[c]) for c in bloqueiam) + len(abertos)
    nomes = {"marcacao": "marcação(ões)", "campo": "campo(s) em maiúsculas",
             "instrucao": "trecho(s) de instrução", "envio": "campo(s) do envio sem preencher"}
    if total:
        partes = []
        for chave in bloqueiam:
            if pendencias[chave]:
                partes.append("%d %s" % (len(pendencias[chave]), nomes[chave]))
        if abertos:
            partes.append("%d conferência(s) do \"Antes de enviar\" sem marcar" % len(abertos))
        print("NÃO ESTÁ PRONTO PARA ENVIAR: %s." % "; ".join(partes))
    elif pendencias["envio"]:
        print("PRONTO PARA GERAR O .DOCX: o texto está resolvido; falta preencher no .docx %d campo(s) do envio, entre chaves." % len(pendencias["envio"]))
    else:
        print("PRONTO PARA ENVIAR: nenhuma pendência no texto que vai ao cliente.")
    print("Arquivo conferido: %s" % origem)
    for chave in ("marcacao", "campo", "instrucao", "envio"):
        if pendencias[chave]:
            print()
            print("%s:" % ROTULOS[chave])
            for numero, trecho in pendencias[chave]:
                if mostrar_linhas:
                    print("  linha %d: %s" % (numero, trecho))
                else:
                    print("  %s" % trecho)
    if achou_secao is not None:
        print()
        if achou_secao:
            print("Antes de enviar: %d item(ns) conferido(s), %d sem marcar." % (len(marcados), len(abertos)))
            for numero, texto in abertos:
                print("  linha %d: %s" % (numero, texto))
        else:
            print("AVISO: não achei a seção \"Antes de enviar\" no topo. Confira se as conferências foram feitas.")
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
    """Quebra o markdown em trechos simples: (tipo, dados)."""
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
            saida.append(("citacao", limpa.lstrip(">").strip()))
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


def escrever_inline(paragrafo, texto, negrito_base=False):
    from docx.enum.text import WD_COLOR_INDEX

    for trecho, negrito, italico, codigo in pedacos_inline(texto):
        if codigo and RE_DESTAQUE.fullmatch(trecho):
            codigo = False
        for parte in RE_DESTAQUE.split(trecho):
            if not parte:
                continue
            run = paragrafo.add_run(parte)
            run.bold = negrito or negrito_base
            run.italic = italico
            if codigo:
                run.font.name = "Courier New"
            if RE_DESTAQUE.fullmatch(parte):
                run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                run.bold = True


def estilo_ou_padrao(doc, nome, padrao="Normal"):
    try:
        doc.styles[nome]
        return nome
    except KeyError:
        return padrao


def montar_docx(trechos_md, saida):
    from docx import Document
    from docx.shared import Cm, Pt

    doc = Document()
    for secao in doc.sections:
        secao.top_margin = Cm(2.5)
        secao.bottom_margin = Cm(2.5)
        secao.left_margin = Cm(2.5)
        secao.right_margin = Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)

    contagem = [0, 0]
    for tipo, dados in trechos_md:
        if tipo != "numero":
            contagem = [0, 0]
        if tipo == "titulo":
            nivel, texto = dados
            p = doc.add_heading(level=min(nivel, 4))
            escrever_inline(p, texto)
        elif tipo == "paragrafo":
            escrever_inline(doc.add_paragraph(), dados)
        elif tipo == "marcador":
            nivel, texto = dados
            nome = "List Bullet 2" if nivel == 2 else "List Bullet"
            escrever_inline(doc.add_paragraph(style=estilo_ou_padrao(doc, nome)), texto)
        elif tipo == "numero":
            nivel, texto = dados
            # Número escrito no texto: cada lista recomeça em 1 em qualquer programa.
            if nivel == 1:
                contagem = [contagem[0] + 1, 0]
                rotulo = "%d." % contagem[0]
            else:
                contagem[1] += 1
                rotulo = "%s)" % "abcdefghijklmnopqrstuvwxyz"[(contagem[1] - 1) % 26]
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9 if nivel == 1 else 1.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.add_run(rotulo + " ")
            escrever_inline(p, texto)
        elif tipo == "citacao":
            escrever_inline(doc.add_paragraph(style=estilo_ou_padrao(doc, "Quote")), dados)
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
            if estilo_ou_padrao(doc, "Table Grid", "") == "Table Grid":
                tabela.style = "Table Grid"
            for j in range(colunas):
                escrever_inline(tabela.rows[0].cells[j].paragraphs[0], cabeca[j] if j < len(cabeca) else "", negrito_base=True)
            for i, linha in enumerate(corpo, start=1):
                for j in range(colunas):
                    escrever_inline(tabela.rows[i].cells[j].paragraphs[0], linha[j] if j < len(linha) else "")
            doc.add_paragraph()
    doc.save(saida)


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


def main(argv):
    opcoes = [a for a in argv[1:] if a.startswith("--")]
    args = [a for a in argv[1:] if not a.startswith("--")]
    if "--ajuda" in opcoes or "--help" in opcoes:
        print(__doc__)
        return 0
    if not args:
        print("ERRO: diga qual arquivo converter ou conferir.")
        print("Exemplo: python3 scripts/md_para_docx.py escritorio/07-operacao/comercial/propostas/C-2026-0001-proposta-v1.md")
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
        corpo = list(enumerate(paragrafos, start=1))
        pendencias, abertos, marcados = conferir_linhas(corpo, [])
        total = relatar(pendencias, abertos, marcados, None, caminho, mostrar_linhas=False, chave_bloqueia=True)
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
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1

    corpo, internas, achou = separar(texto, manter_yaml="--manter-cabecalho" in opcoes)
    if not any(l.strip() for _, l in corpo):
        print("ERRO: depois de tirar o cabeçalho interno, o documento ficou vazio: %s" % entrada)
        return 1
    pendencias, abertos, marcados = conferir_linhas(corpo, internas)
    total = relatar(pendencias, abertos, marcados, achou, entrada)

    if "--so-conferir" in opcoes:
        return 2 if total else 0

    forcar = "--forcar" in opcoes
    if total and not forcar:
        print()
        print("Nenhum .docx foi criado: resolva o que está acima e rode de novo.")
        print("Para criar mesmo assim (por exemplo, para ler no Word), acrescente --forcar.")
        return 2

    saida = args[1] if len(args) > 1 else os.path.splitext(entrada)[0] + ".docx"
    try:
        import docx  # noqa: F401
    except ImportError:
        print()
        print("ERRO: a biblioteca python-docx não está instalada neste ambiente. Nenhum .docx foi criado.")
        print("O documento continua em: %s" % entrada)
        print("Para gerar o .docx: instale python-docx (pip install python-docx), ou abra o .md")
        print("no Word ou no Google Docs, apague a seção \"Antes de enviar\" e salve como .docx.")
        return 1
    montar_docx(trechos([l for _, l in corpo]), saida)
    print()
    print("OK: .docx criado em %s (sem o cabeçalho interno e sem a seção \"Antes de enviar\")." % saida)
    if total:
        print("AVISO: criado com --forcar e com pendência. O que sobrou está destacado em amarelo.")
        print("Este .docx não pode ir ao cliente assim: resolva no .md e gere de novo sem --forcar.")
    elif pendencias["envio"]:
        print("Os campos do envio estão em amarelo no .docx. Preencha no sistema do escritório e confira com --conferir-docx antes de enviar.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
