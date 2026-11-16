#!/usr/bin/env python3
"""Verificador de vícios de IA e de risco OAB no texto do carrossel.

Roda sozinho antes de qualquer arte (o montar_carrossel.py chama) e também sobre a minuta da Banca.
Não substitui a Trava OAB: só pega o que dá para pegar por padrão de texto, para que nenhum vício
conhecido chegue ao advogado.

Uso:
    python3 verificar_texto.py carrossel.json          # o roteiro de lâminas
    python3 verificar_texto.py --texto minuta.txt      # texto corrido (minuta, legenda)
    echo "texto" | python3 verificar_texto.py --texto -
    python3 verificar_texto.py --texto texto-do-advogado.txt --autor advogado

--autor advogado: o texto foi escrito pelo próprio advogado. Travessão e "não é X, é Y" viram CONFERIR
(avise uma vez e respeite a escolha dele). No texto que o plugin escreve, os dois são sempre CORRIGIR.

Saída: a lista de achados, um por linha, e o código 1 se houver algo para corrigir.
Níveis: CORRIGIR (vício certo, troque antes de mostrar) e CONFERIR (pode ser legítimo, olhe).
"""
import json
import re
import statistics
import sys
import unicodedata

# ---------------------------------------------------------------- padrões

TRAVESSAO = re.compile(r"[—–]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F2FF\U00002600-\U000026FF⭐⬆↔-⇿]")

NAO_E = [
    re.compile(r"\bn[aã]o (?:é|e|são|sao|se trata de|foi|era)\b[^.!?\n]{1,70}?[,.;:]\s*(?:é|são|e sim|mas sim|mas)\b", re.I),
    re.compile(r"\bn[aã]o (?:é|são) (?:só|apenas|somente)\b[^.!?\n]{1,60}?\b(?:é|são|mas)\b", re.I),
    re.compile(r"\bn[aã]o (?:só|apenas|somente)\b[^.!?\n]{1,60}?\bmas (?:também|tambem)\b", re.I),
    re.compile(r"\bmais (?:do )?que (?:um|uma)\b[^.!?\n]{1,40}?[,:]\s*(?:é|um|uma)\b", re.I),
]

PALAVRAS_IA = [
    (r"\bdescubra\b|\bdescobrir o segredo\b", "veja, confira"),
    (r"\bdesvend\w*", "explico, mostro"),
    (r"\bpotencializ\w*", "aumentar, melhorar"),
    (r"\balavanc\w*", "aumentar, usar"),
    (r"\bjornada\b", "caminho, processo"),
    (r"\bno mundo (?:de hoje|atual|moderno|jur[ií]dico atual)\b|\bnos dias (?:de hoje|atuais)\b", "corte; vá direto ao ponto"),
    (r"\bmergulh\w*", "veja, entenda"),
    (r"\bdesbloque\w*", "liberar, conseguir"),
    (r"\brevolucion\w*", "mudar"),
    (r"\btransformador\w*|\bgame.?changer\b", "corte o adjetivo"),
    (r"\bé (?:importante|fundamental|crucial|essencial) (?:ressaltar|destacar|lembrar|frisar)\b|\bvale (?:ressaltar|destacar|lembrar) que\b", "diga direto"),
    (r"\bem suma\b|\bem resumo\b|\bsem mais delongas\b|\bno fim das contas\b", "corte"),
    (r"\baqui est[aá]\b", "corte"),
    (r"\bo segredo (?:é|para)\b|\bpulo do gato\b", "o que funciona, o cuidado"),
    (r"\bincr[ií]vel\b|\bpoderos[oa]s?\b|\brobust[oa]s?\b", "corte o adjetivo ou diga o fato"),
    (r"\bimagine s[oó]\b|\bbora\b|\bvamos l[aá]\b", "comece pelo assunto"),
]

RISCO_OAB = [
    (r"\bgarant\w*\b", "promessa de resultado (Prov. 205/2021, art. 6º): fale em hipótese"),
    (r"\b100 ?%|\bcausa ganha\b|\bsem risco\b|\bganhe (?:a|sua) (?:causa|a[cç][aã]o)\b", "promessa de resultado: corte"),
    (r"\bconsulta (?:gr[aá]tis|gratuita)\b|\bprimeira consulta\b|\bdesconto\b|\bpromo[cç][aã]o\b", "gratuidade ou desconto para captar (art. 3º, I)"),
    (r"\banalis\w* (?:o )?seu caso\b|\bme (?:chama|chame) no (?:direct|privado|whats)\w*", "convite para analisar caso: use um convite da lista da base"),
    (r"\bo melhor advogado\b|\bn[uú]mero 1\b|\bl[ií]der\b", "autopromoção comparativa (art. 3º e CED)"),
    (r"\bespecialista\b", "só com título de especialista; confira na base"),
    (r"\bvit[oó]ria\b|\bganhamos\b|\bconseguimos\b", "resultado de processo: confira na Trava"),
]

SAUDACAO = re.compile(r"^\s*(?:oi|ol[aá]|e a[ií]|fala|bom dia|boa tarde|boa noite)\b", re.I)
MENTE = re.compile(r"\b\w{4,}mente\b", re.I)
NAO_ADVERBIO = {"mente", "somente", "demente", "semente", "clemente", "veemente"}

LIMITE_PALAVRAS = {"capa": 22, "texto": 35, "passo": 25, "lista": 40, "mito": 40, "numero": 30,
                   "regra": 50, "convite": 32, "citacao": 40, "comparacao": 40}
TIPOS = set(LIMITE_PALAVRAS)

# ---------------------------------------------------------------- utilidades


def limpar_marcacao(s):
    return re.sub(r"(\*\*|\*|~~|==)", "", s or "")


def palavras(s):
    return len(re.findall(r"[\wÀ-ÿ%º§]+", limpar_marcacao(s)))


def textos_da_lamina(l):
    """Todos os textos que aparecem na lâmina, com o nome do campo."""
    out = []
    for campo in ("antetitulo", "titulo", "subtitulo", "texto", "mito", "fato", "numero", "trecho", "chamada", "detalhe", "autor", "legenda_foto"):
        if l.get(campo):
            out.append((campo, str(l[campo])))
    for i, it in enumerate(l.get("itens") or []):
        if isinstance(it, dict):
            for k in ("texto", "ref", "titulo"):
                if it.get(k):
                    out.append((f"itens[{i}].{k}", str(it[k])))
        else:
            out.append((f"itens[{i}]", str(it)))
    for lado in ("antes", "depois"):
        b = l.get(lado)
        if isinstance(b, dict):
            for k in ("titulo", "texto"):
                if b.get(k):
                    out.append((f"{lado}.{k}", str(b[k])))
    return out


def achar_no_texto(texto, onde):
    """Vícios que dá para achar em qualquer trecho."""
    achados = []
    for m in TRAVESSAO.finditer(texto):
        achados.append(("CORRIGIR", onde, "travessão", trecho(texto, m), "vírgula, dois pontos, ponto ou parênteses"))
    for m in EMOJI.finditer(texto):
        achados.append(("CORRIGIR" if "titulo" in onde or "capa" in onde else "CONFERIR", onde, "emoji", m.group(0),
                        "nenhum no título; no corpo, só se o advogado usa"))
    for p in NAO_E:
        for m in p.finditer(texto):
            achados.append(("CORRIGIR", onde, "\"não é X, é Y\"", trecho(texto, m), "afirme só o que é"))
    for pad, troca in PALAVRAS_IA:
        for m in re.finditer(pad, texto, re.I):
            achados.append(("CORRIGIR", onde, "palavra de IA", trecho(texto, m), troca))
    for pad, motivo in RISCO_OAB:
        for m in re.finditer(pad, texto, re.I):
            achados.append(("CONFERIR", onde, "risco OAB", trecho(texto, m), motivo))
    for m in MENTE.finditer(texto):
        if m.group(0).lower() not in NAO_ADVERBIO:
            achados.append(("CONFERIR", onde, "advérbio em -mente", m.group(0), "corte se for enfeite"))
    return achados


def trecho(texto, m, folga=25):
    a, b = max(0, m.start() - folga), min(len(texto), m.end() + folga)
    return ("..." if a else "") + texto[a:b].replace("\n", " ") + ("..." if b < len(texto) else "")


# ---------------------------------------------------------------- verificações


def verificar_carrossel(dados):
    achados = []
    laminas = dados.get("laminas") or []
    n = len(laminas)
    tipo_carrossel = (dados.get("tipo") or "").lower()
    if n == 0:
        return [("CORRIGIR", "carrossel", "sem lâminas", "", "o roteiro precisa da lista 'laminas'")]
    minimo, maximo = (6, 10) if "tutorial" in tipo_carrossel else (5, 10)
    if not minimo <= n <= maximo:
        achados.append(("CONFERIR", "carrossel", "quantidade de lâminas", f"{n} lâminas", f"o padrão é de {minimo} a {maximo}"))
    if (laminas[0].get("tipo") or "") != "capa":
        achados.append(("CORRIGIR", "lâmina 1", "a primeira lâmina não é capa", laminas[0].get("tipo", "?"), "comece pela capa"))
    if (laminas[-1].get("tipo") or "") != "convite":
        achados.append(("CONFERIR", f"lâmina {n}", "a última lâmina não é convite", laminas[-1].get("tipo", "?"),
                        "feche com um convite da lista da base"))

    contagens = []
    for i, l in enumerate(laminas, 1):
        onde = f"lâmina {i}"
        tipo = l.get("tipo") or "?"
        if tipo not in TIPOS:
            achados.append(("CORRIGIR", onde, "tipo de lâmina desconhecido", tipo, "use: " + ", ".join(sorted(TIPOS))))
        total = sum(palavras(t) for _, t in textos_da_lamina(l))
        if tipo != "capa":
            contagens.append(total)
        limite = LIMITE_PALAVRAS.get(tipo, 35)
        if total > limite:
            achados.append(("CORRIGIR", onde, "texto demais", f"{total} palavras", f"até {limite}; o resto vai para a legenda"))
        for campo, t in textos_da_lamina(l):
            achados += achar_no_texto(t, f"{onde} ({tipo}, {campo})")
        if tipo == "capa" and SAUDACAO.search(limpar_marcacao(l.get("titulo", ""))):
            achados.append(("CORRIGIR", onde, "capa com saudação", l.get("titulo"), "entre direto no assunto"))
        if tipo in ("regra", "mito", "numero") and not l.get("fonte"):
            achados.append(("CORRIGIR", onde, "sem fonte", tipo, "lei, artigo, súmula ou tema, com a fonte oficial"))
        if tipo == "passo" and not l.get("print") and not l.get("print_descricao"):
            achados.append(("CONFERIR", onde, "passo sem print", "", "print real em fotos/prints/ ou a descrição do que capturar"))
    if len(contagens) >= 4:
        media = statistics.mean(contagens)
        if media and statistics.pstdev(contagens) / media < 0.15:
            achados.append(("CONFERIR", "carrossel", "ritmo igual", f"todas as lâminas com cerca de {round(media)} palavras",
                            "varie: uma lâmina de uma linha, outra com lista curta"))
    titulos = [limpar_marcacao(l.get("titulo", "")).strip().split(" ")[0].lower() for l in laminas if l.get("titulo")]
    for palavra in set(titulos):
        if palavra and titulos.count(palavra) >= 3 and palavra not in ("passo", "o", "a", "os", "as"):
            achados.append(("CONFERIR", "carrossel", "títulos começando igual", f"\"{palavra}\" em {titulos.count(palavra)} títulos", "varie a abertura"))
    legenda = dados.get("legenda")
    if legenda:
        achados += achar_no_texto(legenda, "legenda")
    return achados


def verificar_texto(texto):
    achados = []
    for i, linha in enumerate(texto.splitlines(), 1):
        achados += achar_no_texto(linha, f"linha {i}")
    return achados


def imprimir(achados):
    if not achados:
        print("VERIFICADOR · limpo (nenhum vício da lista, nenhum alerta de OAB por padrão de texto)")
        return
    corrigir = [a for a in achados if a[0] == "CORRIGIR"]
    print(f"VERIFICADOR · {len(corrigir)} para corrigir, {len(achados) - len(corrigir)} para conferir")
    for nivel, onde, sinal, tr, troca in achados:
        print(f"- {nivel} · {onde} · {sinal}: {tr} · troque por: {troca}")


def como_dicts(achados):
    return [dict(zip(("nivel", "onde", "sinal", "trecho", "troca"), a)) for a in achados]


if __name__ == "__main__":
    args = sys.argv[1:]
    autor_advogado = False
    if "--autor" in args:
        i = args.index("--autor")
        autor_advogado = len(args) > i + 1 and args[i + 1] == "advogado"
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "--texto":
        fonte = args[1] if len(args) > 1 else "-"
        texto = sys.stdin.read() if fonte == "-" else open(fonte, encoding="utf-8").read()
        res = verificar_texto(unicodedata.normalize("NFC", texto))
    else:
        res = verificar_carrossel(json.load(open(args[0], encoding="utf-8")))
    if autor_advogado:
        res = [("CONFERIR",) + tuple(a[1:]) if a[2] in ("travessão", "\"não é X, é Y\"") else a for a in res]
    imprimir(res)
    sys.exit(1 if any(a[0] == "CORRIGIR" for a in res) else 0)
