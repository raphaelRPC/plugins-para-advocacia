#!/usr/bin/env python3
"""Compara de 3 a 5 peças boas do mesmo tipo e monta o mapa bruto da peça (peca-vira-habilidade).

Uso:
    python3 mapear_pecas.py <peca1> <peca2> <peca3> [<peca4> <peca5>] [--saida mapa-bruto.md]
    python3 mapear_pecas.py <minuta-gerada.md> <minuta-revisada.md> --correcao

--correcao compara a minuta que a habilidade própria gerou (P1) com a versão que o advogado
revisou (P2): "só de uma peça" e "fixos com variáveis" mostram o que ele mudou, para a
habilidade decidir o que vira ajuste na habilidade própria e o que era só daquele caso.

Aceita .md, .txt e .docx (o .docx é lido só com a biblioteca padrão). As peças devem chegar
anonimizadas ([CLIENTE], [DOC], [PROCESSO], [ENDEREÇO]).

O que o script faz, só por comparação de texto (não entende direito, não escolhe nada):
1. separa cada peça em títulos e parágrafos e agrupa os parágrafos parecidos entre as peças;
2. classifica cada grupo:
   - fixo: está em todas as peças, com o mesmo texto (candidato a trecho padrão);
   - fixo com variáveis: está em todas, mas com palavras que mudam (datas, valores, função,
     gênero); mostra o texto com {{variavel}} no lugar e o que muda em cada peça;
   - em algumas: está em mais de uma peça, mas não em todas (exceção: quando entra?);
   - só nesta peça: aparece em uma só (fato específico do caso ou escolha daquela peça);
3. sugere as variáveis, com o tipo provável (data, mes, valor, numero, genero, texto) e os
   valores; MM/AAAA é competência (tipo mes), não data completa; data e mes ganham nome pelo rótulo jurídico mais perto
   (data_cessacao, data_admissao, dib, der) ou data_1, data_2;
4. lista as citações que achou (lei, artigo, súmula, tema, julgado), todas com [CONFERIR]:
   a conferência é da conferir-citacoes, nunca deste script;
5. avisa de dado que não devia estar numa peça anonimizada (CPF, telefone, e-mail, número de
   processo fora de citação).

O resultado é um RASCUNHO para a habilidade e o advogado revisarem e transformarem no mapa da
peça. Nada aqui vira regra sem o advogado confirmar.

Saída: 0 com o mapa bruto; 1 em erro de uso ou de arquivo (menos de 2 peças, arquivo que não
existe, peça vazia).
"""

import difflib
import os
import re
import sys
import unicodedata
import zipfile

LIMIAR_GRUPO = 0.80
LIMIAR_IGUAL = 0.985

RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_DATA = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{4}-\d{2}\b|\b\d{1,2} de [a-zç]+ de \d{4}\b", re.I)
RE_COMPETENCIA = re.compile(r"\d{1,2}/\d{4}|\d{4}-\d{2}")
# rótulos jurídicos que dão nome à variável de data (o mais perto da data vale)
ROTULOS_DATA = [
    (r"cessa[cç][aã]o|cessad[oa]|cessou|dcb", "data_cessacao"),
    (r"admiss[aã]o|admitid[oa]", "data_admissao"),
    (r"dispensa|dispensad[oa]|demiss[aã]o|demitid[oa]|rescis[aã]o|desligad[oa]", "data_dispensa"),
    (r"dib|in[ií]cio do benef[ií]cio|concedid[oa]", "dib"),
    (r"der|requerimento|requereu", "der"),
    (r"nascimento|nascid[oa]", "data_nascimento"),
    (r"[oó]bito|faleceu|falecimento", "data_obito"),
    (r"per[ií]cia", "data_pericia"),
    (r"relat[oó]rio|laudo|atestado", "data_relatorio"),
    (r"acidente", "data_acidente"),
    (r"casamento|casaram", "data_casamento"),
    (r"separa[cç][aã]o", "data_separacao"),
]
RE_VALOR = re.compile(r"R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?")
RE_NUM = re.compile(r"\b\d+(?:[.,]\d+)*\b")
RE_MARCA = re.compile(r"\[[^\[\]\n]+\]")
RE_GEN_ART = re.compile(r"\b(o|a|do|da|ao|à|pelo|pela|no|na)\s+(?=(autor|autora|requerente|reclamante|segurado|segurada|impetrante|exequente|embargante|recorrente|apelante|executado|executada|reclamado|reclamada)\b)", re.I)
PALAVRAS_GENERO = {"autora": "autor", "segurada": "segurado", "executada": "executado", "reclamada": "reclamado"}
RE_CITACAO = re.compile(
    r"(art(?:igo)?s?\.?\s*\d+[\w\-º°]*(?:,?\s*(?:§|inc(?:iso)?\.?|par[áa]grafo)\s*[\w\-º°]+)*\s*,?\s*(?:d[oa]s?\s+)?(?:Lei(?: Complementar)?\s*(?:n[ºo°.]*\s*)?[\d.]+/\d{2,4}|C[óo]digo [A-Z][\wçãé ]+?(?=[,.;)]|\s(?:e|ou)\s)|CPC|CLT|CF|Constitui[çc][ãa]o(?: Federal)?|CDC|CC))"
    r"|((?:Lei(?: Complementar)?|Decreto)\s*(?:n[ºo°.]*\s*)?[\d.]+/\d{2,4})"
    r"|(S[úu]mula(?: Vinculante)?\s*(?:n[ºo°.]*\s*)?\d+(?:\s*d[oa]\s+[A-Z]{2,5}\d?)?)"
    r"|(Tema\s*(?:n[ºo°.]*\s*)?\d+(?:\s*d[oa]\s+[A-Z]{2,5})?)"
    r"|((?:STF|STJ|TST|TNU|TRF\d|TRT\d{1,2}|TJ[A-Z]{2}|TR[A-Z]{1,2})\s*,\s*[A-ZÁ-Ú][\wÀ-ÿ ]{1,40}?\s*n[ºo°.]*\s*[\d.\-/]+)",
    re.I,
)
RE_CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
RE_FONE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-\d{4}\b")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")
PARADAS = {"de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "a", "o", "as", "os", "e", "que",
           "por", "para", "com", "como", "um", "uma", "ao", "à", "se", "sua", "seu", "pelo", "pela", "valor"}


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def ler_texto(caminho):
    if caminho.lower().endswith(".docx"):
        try:
            with zipfile.ZipFile(caminho) as z:
                xml = z.read("word/document.xml").decode("utf-8")
        except (zipfile.BadZipFile, KeyError):
            raise ValueError("não parece um .docx válido: %s" % caminho)
        partes = []
        for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
            t = "".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", p, flags=re.S))
            t = t.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")
            partes.append(t)
        return "\n\n".join(partes)
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    raise ValueError("não consegui ler como texto: %s" % caminho)


def blocos(texto):
    """Devolve a lista de (tipo, texto): tipo 'titulo' ou 'paragrafo'."""
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    saida, atual = [], []

    def fechar():
        if atual:
            saida.append(("paragrafo", " ".join(x.strip() for x in atual)))
            atual.clear()

    for linha in texto.splitlines():
        limpa = linha.strip()
        if not limpa:
            fechar()
            continue
        m = RE_TITULO.match(limpa)
        if m:
            fechar()
            saida.append(("titulo", m.group(2).strip()))
            continue
        if re.match(r"^(\d+[.)]|[-*+])\s+", limpa):
            fechar()
            saida.append(("paragrafo", limpa))
            continue
        atual.append(limpa)
    fechar()
    return saida


def mascarar(texto):
    t = RE_MARCA.sub(" <M> ", texto)
    t = RE_VALOR.sub(" <V> ", t)
    t = RE_DATA.sub(" <D> ", t)
    t = RE_NUM.sub(" <N> ", t)
    t = RE_GEN_ART.sub("<g> ", t)
    t = sem_acento(t)
    for fem, masc in PALAVRAS_GENERO.items():
        t = re.sub(r"\b%s\b" % fem, masc, t)
    return " ".join(t.split())


RE_TOKEN = re.compile(
    r"\[[^\[\]\n]+\]"
    r"|R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?"
    r"|\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}(?:-\d{2})?"
    r"|\d+(?:[.,/]\d+)*\.?"
    r"|[\wÀ-ÿº°§]+|[^\w\s]"
)
ARTIGOS = {"o", "a", "do", "da", "ao", "pelo", "pela", "no", "na"}
SUBSTANTIVOS_GENERO = {"autor", "autora", "requerente", "reclamante", "segurado", "segurada", "impetrante",
                       "exequente", "embargante", "recorrente", "apelante", "executado", "executada",
                       "reclamado", "reclamada"}


def palavras(texto):
    return RE_TOKEN.findall(texto)


def chaves(tokens):
    """A chave de comparação de cada palavra: datas, valores e números viram classe; gênero vira <g>."""
    saida = []
    for i, tok in enumerate(tokens):
        s = sem_acento(tok)
        prox = sem_acento(tokens[i + 1]) if i + 1 < len(tokens) else ""
        if RE_MARCA.fullmatch(tok):
            saida.append("<M>")
        elif RE_VALOR.fullmatch(tok):
            saida.append("<V>")
        elif RE_DATA.fullmatch(tok):
            saida.append("<D>")
        elif re.fullmatch(r"\d+(?:[.,/]\d+)*\.?", tok):
            saida.append("<N>")
        elif s in ARTIGOS and prox in SUBSTANTIVOS_GENERO:
            saida.append("<g>")
        else:
            saida.append(PALAVRAS_GENERO.get(s, s))
    return saida


def tipo_dos_valores(valores):
    vs = [v for v in valores if v]
    if not vs:
        return "texto"
    if all(RE_VALOR.fullmatch(v.strip()) for v in vs):
        return "valor"
    if all(RE_COMPETENCIA.fullmatch(v.strip()) for v in vs):
        return "mes"  # MM/AAAA ou AAAA-MM: competência (mês), não data completa; tipo "mes" do mapa
    if all(RE_DATA.fullmatch(v.strip()) for v in vs):
        return "data"
    if all(re.fullmatch(r"[\d.,]+", v.strip()) for v in vs):
        return "numero"
    def eh_genero(v):
        partes = sem_acento(v.strip()).split()
        if not partes or len(partes) > 2 or partes[0] not in ARTIGOS | {"a", "o"} | SUBSTANTIVOS_GENERO:
            return False
        return len(partes) == 1 or partes[1] in SUBSTANTIVOS_GENERO

    if all(eh_genero(v) for v in vs):
        return "genero"
    return "texto"


def nome_de_data(tipo, antes, usados):
    """Nome de data pelo rótulo jurídico mais perto (data_cessacao, data_admissao, dib, der...).

    Sem rótulo: a data do fecho ("Cidade, {{data}}.") vira data_da_peca; competência (MM/AAAA)
    no começo e no fim de um período vira competencia_inicio e competencia_fim; o resto,
    data_1, data_2 (ou competencia_1, competencia_2). Palavra vizinha qualquer não vira nome.
    """
    toks = [sem_acento(p) for p in antes]
    for k in range(len(toks) - 1, -1, -1):
        for rx, nome in ROTULOS_DATA:
            if re.fullmatch(rx, toks[k]) or re.fullmatch(rx, " ".join(toks[k:k + 3])):
                if tipo == "mes":
                    nome = "competencia_" + nome.replace("data_", "")
                return nome
    if tipo == "data" and toks[-1:] == [","] and len(toks) >= 2 and len(antes) <= 4 and antes[-2][:1].isupper():
        return "data_da_peca"
    if tipo == "mes" and toks:
        if toks[-1] in ("de", "desde", "entre"):
            return "competencia_inicio"
        if toks[-1] in ("a", "ate", "e"):
            return "competencia_fim"
    prefixo = "competencia" if tipo == "mes" else "data"
    n = 1
    while "%s_%d" % (prefixo, n) in usados:
        n += 1
    return "%s_%d" % (prefixo, n)


def nome_sugerido(tipo, antes, usados):
    if tipo in ("data", "mes"):
        nome = nome_de_data(tipo, antes, usados)
        final, n = nome, 2
        while final in usados:
            final = "%s_%d" % (nome, n)
            n += 1
        usados.add(final)
        return final
    antes = antes[-4:]
    base = ""
    for p in reversed(antes):
        s = sem_acento(p)
        if re.fullmatch(r"[a-z]+", s) and s not in PARADAS and len(s) > 2:
            base = s
            break
    nome = "genero" if tipo == "genero" else ("%s_%s" % (tipo, base) if base else tipo)
    final, n = nome, 2
    while final in usados:
        final = "%s_%d" % (nome, n)
        n += 1
    usados.add(final)
    return final


def agrupar(pecas):
    """pecas: lista de listas de blocos. Devolve grupos: {'tipo','membros':{i: texto},'ordem'}."""
    grupos = []
    for i, bl in enumerate(pecas):
        for pos, (tipo, texto) in enumerate(bl):
            m = mascarar(texto)
            melhor, nota = None, 0.0
            for g in grupos:
                if g["tipo"] != tipo or i in g["membros"]:
                    continue
                r = difflib.SequenceMatcher(None, g["mascara"], m).ratio()
                if r > nota:
                    melhor, nota = g, r
            if melhor and nota >= LIMIAR_GRUPO:
                melhor["membros"][i] = texto
            else:
                grupos.append({"tipo": tipo, "mascara": m, "membros": {i: texto}, "ordem": (pos if i == 0 else 1000 + i * 100 + pos)})
    return grupos


def variacoes(grupo, total):
    """Para um grupo presente em todas, devolve (base_i, tokens da base, slots).

    slots: {(a1, a2): {peca: texto}}, com as posições na peça base.
    """
    base_i = min(grupo["membros"])
    base = palavras(grupo["membros"][base_i])
    kb = chaves(base)
    slots = {}
    for i, texto in sorted(grupo["membros"].items()):
        if i == base_i:
            continue
        outra = palavras(texto)
        ko = chaves(outra)
        sm = difflib.SequenceMatcher(None, kb, ko, autojunk=False)
        for op, a1, a2, b1, b2 in sm.get_opcodes():
            if op != "equal":
                slots.setdefault((a1, a2), {})[i] = " ".join(outra[b1:b2])
                continue
            k = 0
            while k < a2 - a1:
                if base[a1 + k] != outra[b1 + k]:
                    ini = k
                    while k < a2 - a1 and base[a1 + k] != outra[b1 + k]:
                        k += 1
                    fim = k
                    if kb[a1 + ini] == "<g>" and fim - ini == 1 and fim < a2 - a1:
                        fim += 1
                        k = fim
                    slots.setdefault((a1 + ini, a1 + fim), {})[i] = " ".join(outra[b1 + ini:b1 + fim])
                else:
                    k += 1
    return base_i, base, slots


def juntar(tokens):
    texto = " ".join(tokens)
    texto = re.sub(r"\s+([,.;:)\]!?])", r"\1", texto)
    texto = re.sub(r"([(\[])\s+", r"\1", texto)
    texto = re.sub(r"\s+-\s+", "-", texto)
    texto = re.sub(r'"\s+(.*?)\s+"', r'"\1"', texto)
    return texto


def main(argv):
    args = argv[1:]
    saida = None
    if "--saida" in args:
        i = args.index("--saida")
        if i + 1 >= len(args):
            print("ERRO: --saida precisa do caminho do arquivo do mapa bruto.")
            return 1
        saida = args[i + 1]
        args = args[:i] + args[i + 2:]
    if "--ajuda" in args or "--help" in args:
        print(__doc__)
        return 0
    correcao = "--correcao" in args
    args = [a for a in args if a != "--correcao"]
    if correcao and len(args) != 2:
        print("ERRO: --correcao compara exatamente duas peças: a minuta gerada e a revisada pelo advogado.")
        return 1
    if len(args) < 2:
        print("ERRO: preciso de pelo menos 2 peças do mesmo tipo (o ideal são de 3 a 5).")
        print("Exemplo: python3 scripts/mapear_pecas.py escritorio/04-base/juridico/modelos/peticao-inicial/*.md --saida mapa-bruto.md")
        return 1
    avisos = []
    if len(args) < 3 and not correcao:
        avisos.append("só %d peças: com menos de 3, o que parece fixo pode ser coincidência. Peça mais uma." % len(args))
    if len(args) > 5:
        avisos.append("%d peças: acima de 5, o mapa fica pesado sem ganhar muito. Use as 5 melhores." % len(args))
    pecas, nomes = [], []
    for caminho in args:
        if not os.path.isfile(caminho):
            print("ERRO: não encontrei a peça: %s" % caminho)
            return 1
        try:
            bl = blocos(ler_texto(caminho))
        except ValueError as erro:
            print("ERRO: %s" % erro)
            return 1
        if not [b for b in bl if b[0] == "paragrafo"]:
            print("ERRO: a peça está vazia ou não tem parágrafos: %s" % caminho)
            return 1
        pecas.append(bl)
        nomes.append(os.path.basename(caminho))
    total = len(pecas)
    grupos = agrupar(pecas)
    grupos.sort(key=lambda g: g["ordem"])

    out = []
    w = out.append
    if correcao:
        w("# Correção do advogado · P1 = minuta gerada, P2 = minuta revisada")
        w("")
        w("> O que aparece em \"só de uma peça\" e em \"fixos com variáveis\" é o que mudou. Para cada mudança, "
          "a habilidade pergunta: vale para todo caso (ajuste na habilidade própria) ou só para este?")
    else:
        w("# Mapa bruto · %d peças comparadas" % total)
    w("")
    w("> Rascunho do script mapear_pecas.py. Não é o mapa da peça: a habilidade e o advogado revisam, "
      "dão nome às variáveis, decidem as exceções e conferem cada citação. Nada daqui vale como regra sem o ok.")
    w("")
    for av in avisos:
        w("AVISO: " + av)
        w("")
    w("## Peças lidas")
    w("")
    w("| # | Arquivo | Títulos | Parágrafos |")
    w("|---|---|---|---|")
    for i, bl in enumerate(pecas):
        w("| P%d | %s | %d | %d |" % (i + 1, nomes[i], sum(1 for b in bl if b[0] == "titulo"), sum(1 for b in bl if b[0] == "paragrafo")))
    w("")

    w("## Estrutura (títulos)")
    w("")
    w("| Título | Em quais peças | Classe |")
    w("|---|---|---|")
    for g in grupos:
        if g["tipo"] != "titulo":
            continue
        quais = ", ".join("P%d" % (i + 1) for i in sorted(g["membros"]))
        classe = "fixo" if len(g["membros"]) == total else ("em algumas" if len(g["membros"]) > 1 else "só nesta peça")
        texto = re.sub(r"^\d+(\.\d+)*\.?\s*", "", g["membros"][min(g["membros"])])
        w("| %s | %s | %s |" % (texto, quais, classe))
    w("")

    fixos, com_var, algumas, unicos = [], [], [], []
    for g in grupos:
        if g["tipo"] != "paragrafo":
            continue
        n = len(g["membros"])
        if n == total:
            textos = list(g["membros"].values())
            iguais = all(difflib.SequenceMatcher(None, textos[0], t).ratio() >= LIMIAR_IGUAL for t in textos[1:])
            (fixos if iguais else com_var).append(g)
        elif n > 1:
            algumas.append(g)
        else:
            unicos.append(g)

    w("## Trechos fixos (iguais em todas as peças)")
    w("")
    w("Candidatos a trecho padrão. Confira se são mesmo do escritório ou se só se repetiram nestas peças.")
    w("")
    for k, g in enumerate(fixos, 1):
        w("F%d. %s" % (k, g["membros"][min(g["membros"])]))
        w("")

    usados = set()
    variaveis = []
    w("## Trechos fixos com variáveis")
    w("")
    w("O texto da primeira peça, com {{variavel}} no lugar do que muda. Os nomes são sugestão: renomeie no mapa.")
    w("")
    for k, g in enumerate(com_var, 1):
        base_i, base, slots = variacoes(g, total)
        trocas = {}
        for (a1, a2), valores in sorted(slots.items()):
            todos = [" ".join(base[a1:a2])] + [valores.get(i, " ".join(base[a1:a2])) for i in sorted(g["membros"]) if i != base_i]
            tipo = tipo_dos_valores(todos)
            nome = nome_sugerido(tipo, base[max(0, a1 - 10):a1], usados)
            trocas[(a1, a2)] = nome
            variaveis.append((nome, tipo, todos, "V%d" % k))
        tokens = []
        j = 0
        for (a1, a2) in sorted(trocas):
            if a1 < j:
                continue
            tokens += base[j:a1]
            tokens.append("{{%s}}" % trocas[(a1, a2)])
            j = max(a2, a1)
        tokens += base[j:]
        w("V%d. %s" % (k, juntar(tokens)))
        w("")

    w("## Variáveis sugeridas")
    w("")
    w("| Variável (sugestão) | Tipo provável | Trecho | %s |" % " | ".join("P%d" % (i + 1) for i in range(total)))
    w("|---|---|---|%s" % ("---|" * total))
    for nome, tipo, todos, onde in variaveis:
        w("| %s | %s | %s | %s |" % (nome, tipo, onde, " | ".join(v if v else "(vazio)" for v in todos)))
    marcas = sorted(set(m.group(0) for bl in pecas for _, t in bl for m in RE_MARCA.finditer(t)))
    if marcas:
        w("")
        w("Marcas de anonimização que viram variável com origem no cliente ou no sistema do escritório: %s" % ", ".join(marcas))
    w("")

    w("## Trechos que aparecem em algumas peças (exceções)")
    w("")
    w("Para cada um, pergunte ao advogado quando ele entra. Vira bloco condicional no modelo ou fica fora.")
    w("")
    for k, g in enumerate(algumas, 1):
        quais = ", ".join("P%d" % (i + 1) for i in sorted(g["membros"]))
        w("E%d (%s). %s" % (k, quais, g["membros"][min(g["membros"])]))
        w("")
    w("## Trechos só de uma peça")
    w("")
    w("Fato específico do caso ou escolha daquela peça. Se for exceção que se repete em outros casos, vira bloco condicional.")
    w("")
    for k, g in enumerate(unicos, 1):
        i = min(g["membros"])
        w("U%d (P%d). %s" % (k, i + 1, g["membros"][i]))
        w("")

    w("## Citações encontradas")
    w("")
    w("Todas entram no mapa com a marca. A conferência é da conferir-citacoes, na fonte (`citacoes.md`).")
    w("")
    w("| Citação como está | Em quais peças | Marca no mapa |")
    w("|---|---|---|")
    vistas = {}
    for i, bl in enumerate(pecas):
        for _, t in bl:
            for m in RE_CITACAO.finditer(t):
                c = " ".join(m.group(0).split()).rstrip(",. ")
                vistas.setdefault(c, set()).add(i)
    if not vistas:
        w("| (nenhuma citação reconhecida: confira à mão) | | |")
    for c, quais in sorted(vistas.items(), key=lambda x: (-len(x[1]), x[0])):
        w("| %s | %s | [CONFERIR: existe, vigente, diz o que a peça diz] |" % (c, ", ".join("P%d" % (i + 1) for i in sorted(quais))))
    w("")

    w("## Alertas de dados")
    w("")
    alertas = []
    for i, bl in enumerate(pecas):
        for n, (_, t) in enumerate(bl, 1):
            sem_cit = RE_CITACAO.sub(" ", t)
            for rotulo, rx in (("CPF", RE_CPF), ("telefone", RE_FONE), ("e-mail", RE_EMAIL), ("número de processo fora de citação", RE_CNJ)):
                if rx.search(sem_cit):
                    alertas.append("P%d, bloco %d: %s. Anonimize antes de seguir e não repita no mapa." % (i + 1, n, rotulo))
    if alertas:
        for a in sorted(set(alertas)):
            w("- " + a)
    else:
        w("- Nenhum CPF, telefone, e-mail ou número de processo fora de citação encontrado. Confira nomes à mão.")
    w("")
    w("## Resumo")
    w("")
    w("%d títulos e %d grupos de parágrafos: %d fixos, %d fixos com variáveis, %d em algumas peças, %d só de uma peça; "
      "%d variáveis sugeridas; %d citações para conferir; %d alertas de dados."
      % (sum(1 for g in grupos if g["tipo"] == "titulo"), sum(1 for g in grupos if g["tipo"] == "paragrafo"),
         len(fixos), len(com_var), len(algumas), len(unicos), len(variaveis), len(vistas), len(set(alertas))))

    texto = "\n".join(out) + "\n"
    if saida:
        with open(saida, "w", encoding="utf-8") as f:
            f.write(texto)
        print("Mapa bruto gravado em %s." % saida)
        print(out[-1])
    else:
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
