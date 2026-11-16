#!/usr/bin/env python3
"""Apoio da triagem das publicações.

Para cada publicação ainda não triada (ou as indicadas por --ids), o script:
  - acha no teor os números de dias e de horas, as datas, as horas marcadas e as
    expressões de prazo ("no prazo de", "em X dias", "intime-se", "manifeste-se",
    "designo audiência", "julgo improcedente", "expeça-se", "sob pena de"...);
  - diz a quem a ordem se dirige (a parte do cliente, a outra parte, as partes);
  - liga o processo ao caso pela carteira de processos (processos.csv), só pelo
    número; com --escritorio, procura o número exato nos registros dos outros
    plugins. Nunca liga por nome, área ou palpite: o que não achou é sem-caso;
  - sugere a triagem (prazo, audiencia, pericia, ciencia, urgente, sem-caso,
    sem-providencia), com o trecho literal que justifica e os dados para a conta.

É sugestão. Quem confirma o que o ato pede, os dias e a regra é uma pessoa.

Uso:
  python3 apoio_triagem.py <publicacoes.csv> --processos <processos.csv>
      [--regras <regras-de-contagem.md>] [--escritorio <pasta escritorio>]
      [--ids PUB-2026-00001,PUB-2026-00002] [--todas] [--hoje AAAA-MM-DD]
      [--ultima-rodada AAAA-MM-DD] [--json] [--gravar [--triagens <arquivo.md>]]

Sem --gravar, só mostra. Com --gravar, atualiza no publicacoes.csv só as linhas
nao-triada (ou já triadas pela ia) e grava a triagem do dia em triagens/AAAA-MM-DD.md.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import unicodedata

TRIAGENS = ["nao-triada", "sem-providencia", "ciencia", "prazo", "audiencia", "pericia", "urgente",
            "sem-caso", "duplicada"]
COL_PROCESSOS = ["processo", "codigo_caso", "cliente_curto", "area", "tribunal", "orgao", "responsavel",
                 "situacao", "ultima_movimentacao", "atualizado_em"]
OBRIG_PUBLICACOES = ["id", "fonte", "disponibilizada_em", "tribunal", "orgao", "processo", "tipo_ato",
                     "teor", "triagem"]


def erro(msg):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(1)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def espelho(texto):
    """Minúsculas sem acento, com o mesmo comprimento do original (posições batem)."""
    saida = []
    for c in texto:
        base = unicodedata.normalize("NFD", c)[0]
        low = base.lower()
        saida.append(low if len(low) == 1 else base)
    return "".join(saida)


def chave_coluna(nome):
    s = sem_acento((nome or "").strip().lower())
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc), bruto.startswith(b"\xef\xbb\xbf")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace"), False


def ler_csv(caminho, obrigatorias, nome):
    if not os.path.exists(caminho):
        erro(f"não encontrei {nome}: {caminho}")
    texto, bom = ler_texto(caminho)
    if not texto.strip():
        erro(f"{caminho} está vazio")
    primeira = texto.splitlines()[0]
    delim = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=delim)
    cab_orig = leitor.fieldnames or []
    cab = [chave_coluna(c) for c in cab_orig]
    faltam = [c for c in obrigatorias if c not in cab]
    if faltam:
        erro(f"{caminho}: faltam as colunas {', '.join(faltam)}")
    linhas = [{chave_coluna(k): (v or "").strip() for k, v in l.items() if k is not None} for l in leitor]
    return linhas, delim, bom, cab


def data_iso(valor):
    v = (valor or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        a, mes, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})", v)
        if not m:
            return ""
        d, mes, a = m.groups()
    try:
        return dt.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return ""


def digitos(processo):
    return re.sub(r"\D", "", processo or "")


def mais_dias_uteis(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def dia_util_anterior(d):
    d -= dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


# ---------------------------------------------------------------- números por extenso

UNIDADES = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7,
            "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13, "catorze": 14, "quatorze": 14,
            "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19}
DEZENAS = {"vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70,
           "oitenta": 80, "noventa": 90}
EXTENSO = r"(?:(?:vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa)(?:\s+e\s+(?:um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove))?|um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|catorze|quatorze|quinze|dezesseis|dezessete|dezoito|dezenove|cem)"


def valor_extenso(s):
    s = s.strip()
    if s == "cem":
        return 100
    total = 0
    for p in re.split(r"\s+e\s+", s):
        total += DEZENAS.get(p, UNIDADES.get(p, 0))
    return total or None


# ---------------------------------------------------------------- padrões (no espelho sem acento)

NUM = r"(\d{1,3}|" + EXTENSO + r")"
PARENTESE = r"(?:\s*\(\s*(?:\d{1,3}|[a-z\s]+)\s*\))?"
RE_DIAS = re.compile(r"\b" + NUM + PARENTESE + r"\s+dias?(?:\s+(uteis|corridos))?\b")
RE_HORAS = re.compile(r"\b" + NUM + PARENTESE + r"\s+horas?\b")
RE_PRAZO_EXPR = re.compile(r"\b(no\s+prazo\s+(?:legal|comum|sucessivo)?\s*de|prazo\s+de|em|dentro\s+de|no\s+prazo\s+de)\s*$")
RE_DATA_BARRA = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")
RE_DATA_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
MESES = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
         "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
RE_DATA_EXTENSO = re.compile(r"\b(\d{1,2})\s+de\s+(" + "|".join(MESES) + r")\s+de\s+(\d{4})\b")
RE_HORA = re.compile(r"\b(?:as|a\s+partir\s+das)\s+(\d{1,2})\s*(?:h|:|horas)\s*(\d{2})?\b|\b(\d{1,2})h(\d{2})\b")

EXPRESSOES = [
    ("intime-se", r"\bintime(?:m)?-se\b|\bintime-?se\b|\bintimem-?se\b"),
    ("manifeste-se", r"\bmanifeste(?:m)?-se\b|\bmanifestar-se\b|\bse\s+manifestar\b"),
    ("vista", r"\bvista\s+(?:a|as|ao|aos)\s"),
    ("no prazo de", r"\bno\s+prazo\s+(?:legal\s+|comum\s+|sucessivo\s+)?de\b|\bprazo\s+de\s+\d"),
    ("designo audiencia", r"\b(?:re)?designo\s+(?:a\s+|nova\s+)?audiencia|\bfica\s+(?:re)?designada\s+(?:a\s+)?audiencia|\baudiencia\s+(?:de\s+\w+\s+)?(?:fica\s+)?(?:re)?(?:designada|marcada)\s+para|\bdesigno\s+o\s+dia\b.{0,40}audiencia"),
    ("pericia", r"\b(?:re)?designo\s+(?:a\s+|nova\s+)?pericia|\bpericia\s+(?:medica\s+|tecnica\s+|contabil\s+|social\s+)?(?:fica\s+)?(?:re)?(?:designada|marcada|agendada)\s+para|\bnomeio\s+(?:como\s+)?perit"),
    ("sessao de julgamento", r"\bsessao\s+(?:virtual\s+)?de\s+julgamento|\bincluido\s+em\s+pauta|\bpauta\s+de\s+julgamento"),
    ("julgo improcedente", r"\bjulgo\s+(?:totalmente\s+)?improcedentes?\b"),
    ("julgo procedente", r"\bjulgo\s+(?:totalmente\s+|parcialmente\s+)?procedentes?\b"),
    ("homologo", r"\bhomologo\b"),
    ("extingo", r"\bextingo\s+o\s+processo|\bjulgo\s+extint"),
    ("acordam", r"\bacordam\b"),
    ("decisao", r"\b(?:defiro|indefiro|concedo\s+a\s+tutela|nego\s+(?:a\s+)?tutela|revogo)\b"),
    ("expeca-se", r"\bexpeca(?:m)?-se\b"),
    ("rpv ou precatorio", r"\brequisicao\s+de\s+pequeno\s+valor\b|\brpv\b|\bprecatorio\b"),
    ("alvara", r"\balvara\b"),
    ("deposito judicial", r"\bdeposito\s+judicial\b"),
    ("sob pena de", r"\bsob\s+pena\s+de\b"),
    ("cumpra-se", r"\bcumpra(?:m)?-se\b"),
    ("cite-se", r"\bcite(?:m)?-se\b"),
    ("transito em julgado", r"\btransit(?:ou|ada|ado)\s+em\s+julgado\b|\btransito\s+em\s+julgado\b"),
    ("arquive-se", r"\barquive(?:m)?-se\b|\bao\s+arquivo\b"),
    ("ciencia", r"\bciencia\s+(?:as|a|ao)\s+part|\bde-se\s+ciencia\b|\bdou\s+ciencia\b"),
    ("juntar documento", r"\b(?:juntar|junte|juntem|apresentar|apresente|trazer\s+aos\s+autos|anexar)\b"),
    ("prazo legal", r"\bprazo\s+legal\b|\bprazo\s+da\s+lei\b|\bprazo\s+de\s+lei\b|\bno\s+prazo\s+regimental\b"),
    ("diga", r"\bdiga(?:m)?\b|\bdizer\s+sobre\b|\bfale(?:m)?\s+(?:a|o|as|os)?\s*(?:parte|partes|autor|autora|reu|re)\b|\bfalar\s+sobre\b"),
    ("especifique provas", r"\bespecifique(?:m)?\b|\bespecificar(?:em)?\s+(?:as\s+)?provas\b"),
    ("querendo", r"\bquerendo\b"),
    ("custas", r"\bcustas\b|\bpreparo\b"),
    ("urgente", r"\burgente\b|\bimediatamente\b|\bprisao\b|\bmandado\s+de\s+prisao\b|\bbloqueio\b|\bpenhora\s+on-?line\b|\bliminar\b|\btutela\s+de\s+urgencia\b|\bbusca\s+e\s+apreensao\b|\bafastamento\s+do\s+lar\b"),
]
EXPRESSOES = [(nome, re.compile(rx)) for nome, rx in EXPRESSOES]

# a quem a ordem se dirige
ATIVO = r"(?:a\s+parte\s+(?:autora|requerente|exequente|reclamante|impetrante|embargante|agravante|recorrente)|o\s+autor|a\s+autora|os\s+autores|o\s+reclamante|a\s+reclamante|o\s+exequente|a\s+exequente|o\s+requerente|a\s+requerente|o\s+impetrante|a\s+impetrante|o\s+embargante|o\s+agravante|o\s+recorrente|a\s+recorrente|o\s+segurado|a\s+segurada)"
PASSIVO = r"(?:a\s+parte\s+(?:re|requerida|executada|reclamada|impetrada|embargada|agravada|recorrida|contraria|adversa)|o\s+reu|a\s+re|os\s+reus|a\s+reclamada|o\s+reclamado|o\s+executado|a\s+executada|o\s+requerido|a\s+requerida|a\s+autoridade\s+impetrada|o\s+embargado|o\s+agravado|o\s+recorrido|a\s+recorrida)"
ENTIDADE = r"(?:o\s+inss|a\s+autarquia|a\s+uniao|a\s+fazenda(?:\s+publica)?|o\s+ministerio\s+publico|o\s+mpf|o\s+mpt|o\s+mp\b|o\s+estado|o\s+municipio|a\s+caixa|a\s+cef|a\s+defensoria(?:\s+publica)?|o\s+perito|a\s+perita)"
AMBAS = r"(?:as\s+partes|ambas\s+as\s+partes|os\s+litigantes)"
RE_ORDEM = re.compile(r"\b(?:intime(?:m)?-se|intimem-?se|manifeste(?:m)?-se|vista|de-se\s+ciencia|ciencia|cite(?:m)?-se|notifique(?:m)?-se|oficie-se|para\s+que|diga(?:m)?|especifique(?:m)?|fale(?:m)?)\b[^.;]{0,25}?\b(" +
                      ATIVO + "|" + PASSIVO + "|" + ENTIDADE + "|" + AMBAS + r")")
RE_FICA = re.compile(r"\b(?:fica(?:m)?|ficam|resta(?:m)?)\s+(" + ATIVO + "|" + PASSIVO + "|" + ENTIDADE + "|" + AMBAS +
                     r")\s+(?:devidamente\s+)?(?:intimad|notificad|cientificad)")
RE_VERBO_1A = re.compile(r"\b(?:intimo|intimando|notifico|notificando|cientifico)\s+(" + ATIVO + "|" + PASSIVO + "|" +
                         ENTIDADE + "|" + AMBAS + r")")
RE_MANIFESTE_SUJ = re.compile(r"\b(" + ATIVO + "|" + PASSIVO + "|" + ENTIDADE + "|" + AMBAS + r")\s*(?:,\s*)?(?:para\s*,?\s*)?(?:em\s+\d+\s+dias,?\s*)?(?:se\s+manifestar|manifestar-se|manifeste-se)")

ABREVIACOES = {"art", "arts", "fls", "fl", "n", "no", "nº", "inc", "par", "dr", "dra", "sr", "sra", "ltda", "s.a", "sa",
               "cpc", "clt", "min", "rel", "des", "proc", "num", "id", "pag", "p", "pp", "ex", "c", "cf", "obs"}


def frases(texto):
    """Divide em frases sem cortar abreviações, iniciais e números. Devolve (início, fim)."""
    limites = []
    ini = 0
    i = 0
    n = len(texto)
    while i < n:
        c = texto[i]
        if c in ".;!?\n":
            j = i + 1
            while j < n and texto[j] in " \t\r":
                j += 1
            fim_de_frase = c == "\n" or j >= n
            if not fim_de_frase and c in ".!?;" and j < n and j > i + 1 and (texto[j].isupper() or texto[j] in "\"“(" or c == ";"):
                palavra = re.search(r"([\wºª]+)$", texto[ini:i])
                p = palavra.group(1) if palavra else ""
                if c == "." and (len(p) <= 1 or p.lower() in ABREVIACOES or p.isdigit()):
                    fim_de_frase = False
                else:
                    fim_de_frase = True
            if fim_de_frase:
                if texto[ini:i + 1].strip():
                    limites.append((ini, i + 1))
                ini = j
                i = j
                continue
        i += 1
    if texto[ini:].strip():
        limites.append((ini, n))
    return limites


def frase_de(texto, limites, pos):
    for a, b in limites:
        if a <= pos < b:
            return texto[a:b].strip(), (a, b)
    return texto.strip(), (0, len(texto))


def classe_destinatario(s):
    if re.fullmatch(AMBAS, s):
        return "ambas"
    if re.fullmatch(ATIVO, s):
        return "ativo"
    if re.fullmatch(PASSIVO, s):
        return "passivo"
    return "entidade"


def polo_do_cliente(cliente, partes):
    """Pelo nome curto do cliente nas partes ("A x B"). Devolve (polo, como)."""
    if not cliente or " x " not in (partes or "").lower():
        return "", ""
    esquerda, direita = re.split(r"\s+[xX]\s+", partes, maxsplit=1)
    c = espelho(cliente.strip())
    e, d = espelho(esquerda), espelho(direita)
    em_e = bool(re.search(r"\b" + re.escape(c) + r"\b", e))
    em_d = bool(re.search(r"\b" + re.escape(c) + r"\b", d))
    if em_e != em_d:
        return ("ativo" if em_e else "passivo"), "nome nas partes"
    ini = c[:1]
    so_iniciais_e = bool(re.fullmatch(r"(?:[a-z]\.\s*)+", e.strip()))
    so_iniciais_d = bool(re.fullmatch(r"(?:[a-z]\.\s*)+", d.strip()))
    if so_iniciais_e and so_iniciais_d:
        ie, idr = e.strip()[:1] == ini, d.strip()[:1] == ini
        if ie != idr:
            return ("ativo" if ie else "passivo"), "iniciais (provável)"
    return "", ""


def entidade_lado(entidade, partes, polo_cliente):
    """A entidade citada (o INSS, a União...) é a outra parte?"""
    if entidade in ("o perito", "a perita", "o ministerio publico", "o mpf", "o mpt", "o mp"):
        return "outra"
    if not partes:
        return "outra" if polo_cliente else ""
    nucleo = re.sub(r"^(o|a)\s+", "", entidade)
    nucleo = {"autarquia": "inss", "fazenda publica": "fazenda", "cef": "caixa"}.get(nucleo, nucleo)
    p = espelho(partes)
    if re.search(r"\b" + re.escape(nucleo), p) or (nucleo == "inss" and "seguro social" in p):
        return "outra"
    return "outra" if polo_cliente else ""


# ---------------------------------------------------------------- leitura das regras do escritório

def ler_regras(caminho):
    """Lê a seção '## Prazos por ato' (ato | rito | dias | contagem | fonte) e o prazo de ciência do portal."""
    info = {"atos": [], "ciencia_portal": None, "validada": False, "arquivo": caminho, "treino": False}
    if not caminho:
        return info
    if not os.path.exists(caminho):
        erro(f"não encontrei a tabela de regras {caminho}")
    texto, _ = ler_texto(caminho)
    m = re.search(r"(?im)^validada_por:\s*(.*)$", texto)
    info["validada"] = bool(m and m.group(1).strip() and "[A PREENCHER]" not in m.group(1))
    info["treino"] = bool(re.search(r"(?im)^treino:\s*sim", texto))
    sec = re.search(r"(?im)^##\s+prazos\s+por\s+ato\s*$", texto)
    if sec:
        resto = texto[sec.end():]
        prox = re.search(r"(?m)^##\s", resto)
        resto = resto[:prox.start()] if prox else resto
        linhas = [l.strip() for l in resto.splitlines() if l.strip().startswith("|")]
        if len(linhas) >= 2:
            cab = [chave_coluna(c) for c in linhas[0].strip("|").split("|")]
            for l in linhas[2:]:
                cel = dict(zip(cab, [c.strip().strip("`") for c in l.strip("|").split("|")]))
                dias = re.search(r"\d+", cel.get("dias", ""))
                if cel.get("ato") and dias:
                    info["atos"].append({"ato": cel["ato"], "rito": chave_coluna(cel.get("rito", "")).replace("_", "-"),
                                         "dias": int(dias.group(0)),
                                         "contagem": chave_coluna(cel.get("contagem", "")) or "uteis",
                                         "fonte": cel.get("fonte", "")})
    for l in texto.splitlines():
        if "intimacao-portal" in l:
            m = re.search(r"(\d+)\s+dias\s+corridos", sem_acento(l))
            if m:
                info["ciencia_portal"] = int(m.group(1))
    return info


def rito_sugerido(tribunal, orgao):
    t = espelho(tribunal or "")
    o = espelho(orgao or "")
    if "jef" in o or "juizado especial federal" in o or "turma recursal" in o and t.startswith("trf"):
        return "juizado-federal"
    if "juizado" in o or "jec" in o:
        return "juizado-civel"
    if t.startswith("trt") or "vara do trabalho" in o or t == "tst":
        return "trabalhista"
    if "criminal" in o or "penal" in o or "juri" in o:
        return "penal"
    if t.startswith(("tj", "trf", "stj", "stf")):
        return "civel"
    return "outro"


# ---------------------------------------------------------------- análise de um teor

def analisar(teor):
    esp = espelho(teor)
    lims = frases(teor)
    achados = {"expressoes": [], "dias": [], "horas": [], "datas": [], "horarios": [], "ordens": []}
    for nome, rx in EXPRESSOES:
        for m in rx.finditer(esp):
            achados["expressoes"].append({"expressao": nome, "pos": m.start(), "texto": teor[m.start():m.end()]})
    for m in RE_DIAS.finditer(esp):
        bruto = m.group(1)
        n = int(bruto) if bruto.isdigit() else valor_extenso(bruto)
        if not n:
            continue
        antes = esp[max(0, m.start() - 30):m.start()]
        contexto = "prazo" if RE_PRAZO_EXPR.search(antes) or re.search(r"\bpara\s*,?\s*$", antes) else "outro"
        frase, _ = frase_de(teor, lims, m.start())
        achados["dias"].append({"dias": n, "contagem_no_ato": m.group(2) or "", "pos": m.start(),
                                "texto": teor[m.start():m.end()], "contexto": contexto, "frase": frase})
    for m in RE_HORAS.finditer(esp):
        bruto = m.group(1)
        n = int(bruto) if bruto.isdigit() else valor_extenso(bruto)
        if n:
            frase, _ = frase_de(teor, lims, m.start())
            achados["horas"].append({"horas": n, "pos": m.start(), "texto": teor[m.start():m.end()], "frase": frase})
    for rx, ordem in ((RE_DATA_BARRA, "dma"), (RE_DATA_ISO, "amd"), (RE_DATA_EXTENSO, "ext")):
        for m in rx.finditer(esp):
            try:
                if ordem == "dma":
                    d = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                elif ordem == "amd":
                    d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                else:
                    d = dt.date(int(m.group(3)), MESES[m.group(2)], int(m.group(1)))
            except ValueError:
                continue
            frase, _ = frase_de(teor, lims, m.start())
            achados["datas"].append({"data": d.isoformat(), "pos": m.start(), "texto": teor[m.start():m.end()], "frase": frase})
    for m in RE_HORA.finditer(esp):
        h = m.group(1) or m.group(3)
        mi = m.group(2) or m.group(4) or "00"
        if h and int(h) < 24:
            achados["horarios"].append({"hora": f"{int(h):02d}:{mi}", "pos": m.start()})
    for m in RE_ORDEM.finditer(esp):
        achados["ordens"].append({"destinatario": m.group(1), "classe": classe_destinatario(m.group(1)),
                                  "destinatario_texto": teor[m.start(1):m.end(1)],
                                  "pos": m.start(1), "texto": teor[m.start():m.end()]})
    for m in list(RE_FICA.finditer(esp)) + list(RE_VERBO_1A.finditer(esp)):
        achados["ordens"].append({"destinatario": m.group(1), "classe": classe_destinatario(m.group(1)),
                                  "destinatario_texto": teor[m.start(1):m.end(1)],
                                  "pos": m.start(1), "texto": teor[m.start():m.end()]})
    for m in RE_MANIFESTE_SUJ.finditer(esp):
        achados["ordens"].append({"destinatario": m.group(1), "classe": classe_destinatario(m.group(1)),
                                  "destinatario_texto": teor[m.start(1):m.end(1)],
                                  "pos": m.start(1), "texto": teor[m.start():m.end()]})
    achados["_lims"] = lims
    return achados


def tem(achados, nome):
    return [e for e in achados["expressoes"] if e["expressao"] == nome]


def ordem_da_frase(achados, teor, pos):
    """O destinatário da ordem na mesma frase do número de dias (o mais próximo antes dele)."""
    _, (a, b) = frase_de(teor, achados["_lims"], pos)
    candidatas = [o for o in achados["ordens"] if a <= o["pos"] < b]
    if not candidatas:
        return None
    antes = [o for o in candidatas if o["pos"] <= pos]
    return (max(antes, key=lambda o: o["pos"]) if antes else candidatas[0])


def lado_da_ordem(ordem, polo_cliente, partes):
    if ordem is None:
        return "nao-diz"
    c = ordem["classe"]
    if c == "ambas":
        return "escritorio"
    if c == "entidade":
        return "outra" if entidade_lado(ordem["destinatario"], partes, polo_cliente) == "outra" else "nao-sei"
    if not polo_cliente:
        return "nao-sei"
    return "escritorio" if c == polo_cliente else "outra"


def acao_do_prazo(frase):
    f = espelho(frase)
    if "custas" in f or "preparo" in f:
        return "recolher custas", "Recolher custas"
    if re.search(r"contrarraz|contra-?razoes", f):
        return "contrarrazões", "Contrarrazões"
    if re.search(r"replica|contestacao", f):
        return "réplica", "Réplica"
    if re.search(r"manifest|\bvista\b|falar\s+sobre|dizer\s+sobre", f):
        return "manifestação", "Manifestação"
    if re.search(r"quesito|assistente\s+tecnico", f):
        return "apresentar quesitos e assistente técnico", "Quesitos e assistente técnico"
    if re.search(r"rol\s+de\s+testemunhas", f):
        return "rol de testemunhas", "Rol de testemunhas"
    if re.search(r"\b(?:juntar|junte|juntem|apresentar|apresente|apresentem|anexar|anexe)\b|trazer\s+aos\s+autos", f):
        return "juntar documento", "Juntar documento"
    if re.search(r"emend", f):
        return "emendar a inicial", "Emendar a inicial"
    if re.search(r"especificar?\s+(?:as\s+)?provas|especifiquem", f):
        return "especificar provas", "Especificar provas"
    if re.search(r"rol\s+de\s+testemunhas", f):
        return "rol de testemunhas", "Rol de testemunhas"
    if re.search(r"cumpr|comprovar|regularizar", f):
        return "cumprir determinação", "Cumprir determinação"
    return "[A CONFIRMAR: o que o ato pede]", "Prazo"


# ---------------------------------------------------------------- a triagem de uma publicação

def teor_do_arquivo(pasta, rel):
    caminho = os.path.join(pasta, rel) if rel else ""
    if not caminho or not os.path.exists(caminho):
        return "", {}
    texto, _ = ler_texto(caminho)
    m = re.match(r"(?s)^---\n(.*?)\n---\n", texto)
    if not m:
        return texto.strip(), {}
    cab = {}
    for l in m.group(1).splitlines():
        if ":" in l:
            k, v = l.split(":", 1)
            cab[k.strip()] = v.strip()
    return texto[m.end():].strip(), cab


def buscar_nos_irmaos(escritorio, processo):
    """Procura o número exato nos registros dos outros plugins. Devolve lista de (codigo, arquivo)."""
    if not escritorio or not processo:
        return []
    dig = digitos(processo)
    if len(dig) != 20:
        return []
    mascara = f"{dig[0:7]}-{dig[7:9]}.{dig[9:13]}.{dig[13]}.{dig[14:16]}.{dig[16:20]}"
    achados = []
    bases = [("07-operacao/juridico/casos", True), ("07-operacao/experiencia/clientes", True),
             ("07-operacao/comercial/passagens", False)]
    for rel, por_pasta in bases:
        raiz = os.path.join(escritorio, rel)
        if not os.path.isdir(raiz):
            continue
        for dirpath, _, nomes in os.walk(raiz):
            for nome in nomes:
                if not nome.endswith((".md", ".txt", ".csv")):
                    continue
                caminho = os.path.join(dirpath, nome)
                try:
                    texto, _ = ler_texto(caminho)
                except OSError:
                    continue
                if mascara in texto or dig in texto:
                    if por_pasta:
                        codigo = os.path.relpath(caminho, raiz).split(os.sep)[0]
                    else:
                        codigo = os.path.splitext(nome)[0]
                    if re.fullmatch(r"C-\d{4}-\d{4}", codigo):
                        achados.append((codigo, os.path.relpath(caminho, escritorio)))
    return achados


def triar(pub, pasta, carteira, regras, escritorio, hoje, ultima):
    teor, cab = teor_do_arquivo(pasta, pub.get("teor", ""))
    r = {"id": pub["id"], "fonte": pub.get("fonte", ""), "disponibilizada_em": pub.get("disponibilizada_em", ""),
         "tribunal": pub.get("tribunal", ""), "orgao": pub.get("orgao", ""), "processo": pub.get("processo", ""),
         "tipo_ato": pub.get("tipo_ato", ""), "codigo_caso": "", "cliente_curto": "", "area": "", "responsavel": "",
         "ligado_por": "", "triagem": "", "trechos": [], "o_que_pede": "", "dias": None, "dias_fonte": "",
         "contagem": "", "rito": rito_sugerido(pub.get("tribunal"), pub.get("orgao")), "datas": [], "horarios": [],
         "destinatario": "", "lado": "", "avisos": [], "pessoa_agora": [], "para_a_conta": "", "resumo": "",
         "candidatos_tabela": []}
    if not teor:
        r["triagem"] = "nao-triada"
        r["avisos"].append("não achei o teor guardado; sem o teor não há triagem")
        r["pessoa_agora"].append("publicação sem teor: buscar o ato na fonte")
        return r
    a = analisar(teor)
    partes = cab.get("partes", "")

    # 1. ligar ao caso: só pelo número
    linha = carteira.get(digitos(pub.get("processo", "")))
    if linha:
        r.update({"codigo_caso": linha.get("codigo_caso", ""), "cliente_curto": linha.get("cliente_curto", ""),
                  "area": linha.get("area", ""), "responsavel": linha.get("responsavel", ""),
                  "ligado_por": "carteira de processos"})
        if not linha.get("codigo_caso"):
            r["avisos"].append("processo na carteira sem código de caso: [A CONFIRMAR] o código")
        if chave_coluna(linha.get("situacao", "")) in ("arquivado", "encerrado", "baixado"):
            r["avisos"].append(f"processo {linha.get('situacao')} na carteira e publicou de novo: conferir")
    else:
        irmaos = buscar_nos_irmaos(escritorio, pub.get("processo", ""))
        codigos = sorted({c for c, _ in irmaos})
        if len(codigos) == 1:
            r.update({"codigo_caso": codigos[0], "ligado_por": "número exato em " + irmaos[0][1]})
            r["avisos"].append(f"processo fora da carteira; o número exato está em {irmaos[0][1]}. "
                               "Confirme e inclua na carteira (carteira-de-processos)")
        elif len(codigos) > 1:
            r["avisos"].append("o número aparece em mais de um caso (" + ", ".join(codigos) + "): sem-caso até a pessoa dizer")

    polo, como_polo = polo_do_cliente(r["cliente_curto"], partes)
    if como_polo == "iniciais (provável)":
        r["avisos"].append("lado do cliente tirado das iniciais nas partes [CONFERIR]")

    # 2. o que o teor diz
    r["datas"] = sorted({d["data"] for d in a["datas"]})
    r["horarios"] = sorted({h["hora"] for h in a["horarios"]})
    urg = tem(a, "urgente")
    aud = tem(a, "designo audiencia")
    per = tem(a, "pericia")
    ses = tem(a, "sessao de julgamento")
    disp = tem(a, "julgo improcedente") + tem(a, "julgo procedente") + tem(a, "homologo") + tem(a, "extingo") + tem(a, "acordam")
    dec = tem(a, "decisao")
    valor = tem(a, "rpv ou precatorio") + tem(a, "alvara") + tem(a, "deposito judicial")
    painel = r["fonte"] == "painel"

    def trecho(pos):
        f, _ = frase_de(teor, a["_lims"], pos)
        if f not in r["trechos"]:
            r["trechos"].append(f)

    prazos_escritorio, prazos_outra, prazos_duvida = [], [], []
    for d in a["dias"]:
        ordem = ordem_da_frase(a, teor, d["pos"])
        lado = "escritorio" if painel and ordem is None else lado_da_ordem(ordem, polo, partes)
        d["ordem"] = ordem["destinatario_texto"] if ordem else ""
        d["lado"] = lado
        if lado == "outra":
            prazos_outra.append(d)
        elif lado == "escritorio":
            prazos_escritorio.append(d)
        else:
            prazos_duvida.append(d)

    sem_caso = not r["codigo_caso"]

    # pedidos sem número de dias ("diga a parte autora", "no prazo legal", "especifique provas",
    # "intime-se a parte autora"): só não contam quando a ordem é claramente da outra parte
    pedidos_sem_dias = []
    for nome in ("prazo legal", "diga", "manifeste-se", "especifique provas", "vista", "querendo"):
        for e in tem(a, nome):
            ordem = ordem_da_frase(a, teor, e["pos"])
            lado = "escritorio" if painel and ordem is None else lado_da_ordem(ordem, polo, partes)
            if lado != "outra":
                pedidos_sem_dias.append({"expressao": nome, "pos": e["pos"], "texto": e["texto"], "lado": lado,
                                         "ordem": ordem["destinatario_texto"] if ordem else ""})
    for o in a["ordens"]:
        if re.match(r"intim", espelho(o["texto"])) and o["classe"] in ("ativo", "passivo", "ambas"):
            lado = lado_da_ordem(o, polo, partes)
            if lado != "outra":
                pedidos_sem_dias.append({"expressao": "intime-se a parte", "pos": o["pos"], "texto": o["texto"],
                                         "lado": lado, "ordem": o["destinatario_texto"]})
    pedidos_sem_dias.sort(key=lambda x: x["pos"])

    def sugerir_prazo_com_dias():
        d = (prazos_escritorio or prazos_duvida)[0]
        r["triagem"] = "prazo"
        trecho(d["pos"])
        r["dias"] = d["dias"]
        r["dias_fonte"] = "o próprio ato"
        r["contagem"] = d["contagem_no_ato"] or "pela regra do rito"
        acao, _ = acao_do_prazo(d["frase"])
        r["o_que_pede"] = acao
        r["destinatario"] = d["ordem"]
        r["lado"] = d["lado"]
        if d in prazos_duvida and not sem_caso:
            if d["ordem"]:
                r["avisos"].append(f"o ato se dirige a \"{d['ordem']}\" e as partes não dizem de que lado está o cliente: "
                                   "[A CONFIRMAR] se o prazo é do escritório. Na dúvida, fica como prazo para a pessoa conferir")
            else:
                r["avisos"].append("o ato não diz a quem se dirige: [A CONFIRMAR] se o prazo é do escritório. "
                                   "Na dúvida, fica como prazo para a pessoa conferir")
        if len(prazos_escritorio + prazos_duvida) > 1:
            r["avisos"].append("o ato tem mais de um número de dias: " +
                               "; ".join(f"{x['dias']} dias ({x['texto']})" for x in prazos_escritorio + prazos_duvida) +
                               ". A pessoa diz qual vale")
        if acao == "juntar documento":
            r["avisos"].append("prazo que depende do cliente: pedir o documento já (checklist-de-documentos, "
                               "do motor-experiencia, se instalado)")
        for e2 in tem(a, "sob pena de"):
            trecho(e2["pos"])

    def sugerir_prazo_sem_dias():
        pd_ = pedidos_sem_dias[0]
        r["triagem"] = "prazo"
        trecho(pd_["pos"])
        frase, _ = frase_de(teor, a["_lims"], pd_["pos"])
        acao, _ = acao_do_prazo(frase)
        if acao.startswith("[A CONFIRMAR") and pd_["expressao"] in ("diga", "manifeste-se", "vista", "querendo"):
            acao = "manifestação"
        r["o_que_pede"] = acao
        r["dias"] = None
        r["dias_fonte"] = "[A CONFIRMAR: quantos dias]"
        r["destinatario"] = pd_["ordem"]
        r["lado"] = pd_["lado"]
        r["avisos"].append("o ato pede algo sem dizer o número de dias (\"" + frase + "\"): [A CONFIRMAR: quantos dias]. "
                           "A pessoa diz quantos dias (da lei ou da tabela do escritório); na dúvida entre ciência e prazo, "
                           "fica como prazo para a pessoa conferir")
        if pd_["lado"] != "escritorio":
            if pd_["ordem"]:
                r["avisos"].append(f"o ato se dirige a \"{pd_['ordem']}\" e as partes não dizem de que lado está o cliente: "
                                   "[A CONFIRMAR] se o pedido é ao escritório")
            else:
                r["avisos"].append("o ato não diz com clareza a quem se dirige: [A CONFIRMAR] se o pedido é ao escritório")
        for e2 in tem(a, "sob pena de"):
            trecho(e2["pos"])

    # 3. a triagem sugerida (a ordem importa)
    if urg or a["horas"]:
        r["triagem"] = "urgente"
        for e in urg:
            trecho(e["pos"])
        for h in a["horas"]:
            trecho(h["pos"])
            r["o_que_pede"] = f"ordem em {h['horas']} horas"
        r["pessoa_agora"].append("sinal de urgência no ato (horas, liminar, bloqueio, prisão ou ordem imediata)")
    elif aud or per or ses:
        e = (aud or per or ses)[0]
        pauta_tipo = "audiencia" if aud or ses else "pericia"
        trecho(e["pos"])
        quando = [d for d in a["datas"] if frase_de(teor, a["_lims"], d["pos"])[1] == frase_de(teor, a["_lims"], e["pos"])[1]]
        data_ato = quando[0]["data"] if quando else ""
        hora = [h["hora"] for h in a["horarios"] if frase_de(teor, a["_lims"], h["pos"])[1] == frase_de(teor, a["_lims"], e["pos"])[1]]
        pauta_txt = ("sessão de julgamento" if ses and not aud else "audiência" if aud else "perícia") + \
            (f" em {data_ato}" if data_ato else " [A CONFIRMAR: data]") + (f", {hora[0]}" if hora else "")
        if re.search(r"videoconferencia|virtual|telepresencial|on-?line", espelho(teor)):
            pauta_txt += ", por videoconferência"
        if data_ato:
            r["data_do_ato"] = data_ato
            if hoje and data_ato <= (dt.date.fromisoformat(hoje) + dt.timedelta(days=3)).isoformat():
                r["pessoa_agora"].append(f"{pauta_txt}: em até 3 dias")
        if prazos_escritorio or prazos_duvida or pedidos_sem_dias:
            # o ato marca a pauta e também dá prazo à parte do cliente (ou sem destinatário claro): as duas sugestões
            if prazos_escritorio or prazos_duvida:
                sugerir_prazo_com_dias()
            else:
                sugerir_prazo_sem_dias()
            r["tambem"] = {"triagem": pauta_tipo, "o_que_pede": pauta_txt, "data_do_ato": data_ato,
                           "hora": hora[0] if hora else ""}
            r["avisos"].append(f"duas sugestões no mesmo ato: o prazo ({r['o_que_pede']}) e a {pauta_txt}. "
                               f"A triagem fica 'prazo' para a conta, e a {'audiência' if pauta_tipo == 'audiencia' else 'perícia'} "
                               f"entra também em prazos.csv como tipo = {pauta_tipo} (audiencias-e-pericias, se instalada)")
        else:
            r["triagem"] = pauta_tipo
            r["o_que_pede"] = pauta_txt
            r["avisos"].append("pauta não é prazo: nenhum prazo inventado. Aviso e preparação do cliente "
                               "(preparar-o-cliente, do motor-experiencia, se instalado)")
        if tem(a, "sob pena de"):
            for e2 in tem(a, "sob pena de"):
                trecho(e2["pos"])
    elif prazos_escritorio or prazos_duvida:
        sugerir_prazo_com_dias()
        if prazos_outra:
            r["avisos"].append("o ato também dá prazo à outra parte (" +
                               ", ".join(f"{x['ordem']}, {x['dias']} dias" for x in prazos_outra) + "): só ciência")
    elif disp or (dec and not pedidos_sem_dias and r["tipo_ato"] in ("decisao", "despacho", "")):
        r["triagem"] = "prazo"
        e = (disp or dec)[0]
        trecho(e["pos"])
        candidatos = [x for x in regras["atos"] if x["rito"] == r["rito"] and not re.match(r"contra-?rraz|contrarraz", espelho(x["ato"]))]
        if tem(a, "acordam") or r["tipo_ato"] == "acordao":
            # recurso de acórdão não sai da tabela por palpite: a pessoa diz qual cabe
            candidatos = [x for x in candidatos if re.search(r"embargos\s+de\s+declara", espelho(x["ato"]))]
        r["candidatos_tabela"] = candidatos
        # o script não escolhe recurso: lista tudo o que a tabela traz para o rito, e os embargos de declaração
        # aparecem sempre (com os dias da tabela, ou [A CONFIRMAR] quando a tabela não traz a linha do rito)
        sem_embargos = not any(re.search(r"embargos\s+de\s+declara", espelho(x["ato"])) for x in candidatos)
        r["sem_linha_na_tabela"] = ["embargos de declaração"] if (disp or dec) and sem_embargos else []
        opcoes = [f"{x['ato']} ({x['dias']} dias)" for x in candidatos] + \
            [f"{x} ([A CONFIRMAR: quantos dias], não está na tabela do escritório para o rito {r['rito']})" for x in r["sem_linha_na_tabela"]]
        if disp:
            r["o_que_pede"] = "[A DEFINIR: recorrer ou não] o que pode caber, pela tabela do escritório: " + \
                ("; ".join(opcoes) if opcoes else "[A CONFIRMAR: qual ato e quantos dias]") + \
                ". O que cabe e se vale recorrer é da pessoa"
        else:
            r["o_que_pede"] = "[A CONFIRMAR: cabe recurso desta decisão?]" + (" Na tabela: " + "; ".join(opcoes) if opcoes else "")
        if candidatos:
            r["dias_fonte"] = "tabela do escritório" + (" (treino)" if regras["treino"] else "") + ", um ato por linha: " + \
                "; ".join(f"{x['ato']} {x['dias']} dias" for x in candidatos) + \
                "".join(f"; {x} [A CONFIRMAR: quantos dias]" for x in r["sem_linha_na_tabela"])
            r["avisos"].append("a conta sai uma por ato da tabela, e a pessoa diz o que cabe e se vale recorrer [A CONFIRMAR: qual ato]")
        else:
            r["dias_fonte"] = "[A CONFIRMAR: quantos dias]" + ("" if regras["arquivo"] else " (sem a tabela de regras: passe --regras)")
        if (tem(a, "acordam") or r["tipo_ato"] == "acordao") and disp:
            r["avisos"].append("acórdão: o recurso que cabe (e o prazo) a pessoa diz; da tabela só entram os embargos de "
                               "declaração, se houver. [A CONFIRMAR: qual recurso]")
        if tem(a, "julgo improcedente"):
            r["avisos"].append("notícia ruim: aviso ao cliente por ligação, nunca por mensagem "
                               "(status-para-o-cliente, do motor-experiencia, se instalado)")
        if prazos_outra:
            r["avisos"].append("o ato dá prazo à outra parte (" +
                               ", ".join(f"{x['ordem']}, {x['dias']} dias" for x in prazos_outra) + "): só ciência")
    elif pedidos_sem_dias:
        sugerir_prazo_sem_dias()
        if dec:
            trecho(dec[0]["pos"])
            r["avisos"].append("o ato também decide (defere, indefere, concede ou revoga): [A CONFIRMAR: cabe recurso desta decisão?]")
        if prazos_outra:
            r["avisos"].append("o ato também dá prazo à outra parte (" +
                               ", ".join(f"{x['ordem']}, {x['dias']} dias" for x in prazos_outra) + "): só ciência")
    elif prazos_outra:
        d = prazos_outra[0]
        r["triagem"] = "ciencia"
        trecho(d["pos"])
        r["o_que_pede"] = f"prazo de {d['dias']} dias para {d['ordem']} (a outra parte): só ciência, nenhuma linha em prazos.csv"
        r["destinatario"] = d["ordem"]
        r["lado"] = "outra"
        r["avisos"].append("o prazo é da outra parte; prazo em dobro dela, se houver, é decisão da pessoa e não muda nada aqui")
    elif valor:
        r["triagem"] = "ciencia"
        trecho(valor[0]["pos"])
        r["o_que_pede"] = "ciência; acompanhar o valor (acompanhar-valores, se instalada)"
        r["avisos"].append("boa notícia ao cliente, revisada por uma pessoa (status-para-o-cliente, do motor-experiencia, se instalado)")
    elif tem(a, "intime-se") or tem(a, "ciencia") or tem(a, "cumpra-se") or tem(a, "transito em julgado") or tem(a, "arquive-se") or tem(a, "cite-se"):
        r["triagem"] = "ciencia"
        e = (tem(a, "transito em julgado") or tem(a, "arquive-se") or tem(a, "ciencia") or tem(a, "cite-se") or
             tem(a, "cumpra-se") or tem(a, "intime-se"))[0]
        trecho(e["pos"])
        r["o_que_pede"] = "ciência; nenhum número de dias no ato"
        r["avisos"].append("ciência sugerida porque o ato não pede nada à parte do cliente; se pedir, é prazo: a pessoa confere")
    else:
        r["triagem"] = "sem-providencia"
        r["trechos"].append(teor[:200].strip())
        r["o_que_pede"] = "o ato não pede nada ao escritório (conferir)"
        r["avisos"].append("sem providência sugerida porque o script não achou pedido nem número de dias; uma pessoa lê o ato "
                           "antes de fechar (se ele pedir algo, é prazo)")

    if painel:
        envio = cab.get("painel_enviada_em") or r["disponibilizada_em"]
        ciencia = cab.get("painel_ciencia", "")
        domicilio = "domicilio" in espelho(cab.get("painel_sistema", ""))
        r["painel"] = {"enviada_em": envio, "ciencia": ciencia, "aberta_em": cab.get("painel_aberta_em", ""),
                       "domicilio": domicilio}
        if domicilio:
            r["avisos"].append("Domicílio Judicial Eletrônico: a ciência tem regra própria e não é calculada aqui. A pessoa "
                               "informa a data da ciência que o painel mostra (domicilio-eletronico, contagem.md)")
            if not cab.get("painel_aberta_em"):
                r["pessoa_agora"].append("comunicação do Domicílio Judicial Eletrônico sem a data da ciência: a pessoa confere no painel")
        elif ciencia == "sem-ciencia" and envio:
            n = regras["ciencia_portal"] or 10
            tacita = (dt.date.fromisoformat(envio) + dt.timedelta(days=n)).isoformat()
            r["painel"]["ciencia_tacita_prevista"] = tacita
            r["avisos"].append(f"intimação de portal sem ciência: pela tabela, a ciência tácita é no fim de {n} dias corridos do "
                               f"envio ({tacita}){'' if regras['ciencia_portal'] else ' [CONFERIR]'}. Se cair em dia sem expediente, "
                               "a conta mostra as duas leituras e fica com a mais cedo. Abrir antes ou esperar é decisão da pessoa; "
                               "se alguém abrir, a ciência é a abertura e a conta muda")
            if hoje and tacita <= mais_dias_uteis(dt.date.fromisoformat(hoje), 2).isoformat():
                r["pessoa_agora"].append(f"ciência tácita prevista para {tacita}, em até 2 dias úteis")
        elif ciencia in ("aberta", "lida") and cab.get("painel_aberta_em"):
            r["avisos"].append(f"intimação aberta em {cab.get('painel_aberta_em')}: a conta parte da ciência (--ciencia)")

    # 3b. a data de disponibilização em dúvida desde a captação
    if cab.get("aviso_captacao"):
        r["avisos"].append("captação: " + cab["aviso_captacao"])
        r["pessoa_agora"].append("data de disponibilização a conferir antes da conta: " + cab["aviso_captacao"])
    if not r["disponibilizada_em"] and not painel and r["triagem"] != "nao-triada":
        sugerida = r["triagem"]
        r["triagem"] = "urgente"
        r["avisos"].append(f"sem data de disponibilização: o teor sugeriria '{sugerida}', mas sem data não há conta")
        r["pessoa_agora"].append("publicação sem data de disponibilização: a pessoa confere no diário")

    # 4. sem caso: nada de prazo sem a pessoa
    if sem_caso and r["triagem"] != "nao-triada":
        sugerida = r["triagem"]
        r["triagem"] = "sem-caso"
        r["pessoa_agora"].append("processo da OAB do escritório que não está na carteira: é caso antigo, substabelecimento ou erro?")
        r["avisos"].append(f"sem caso: o teor sugeriria '{sugerida}', mas nenhum prazo é calculado sem a pessoa dizer de quem é o processo")

    # 5. atraso de captação
    if r["fonte"] != "painel" and r["disponibilizada_em"] and hoje:
        limite = dia_util_anterior(dt.date.fromisoformat(hoje)).isoformat()
        if r["disponibilizada_em"] < limite or (ultima and r["disponibilizada_em"] < ultima):
            r["pessoa_agora"].append(f"captada com atraso: disponibilizada em {r['disponibilizada_em']}, vista só agora. Vai para o topo")

    # 6. dados para a conta
    if r["triagem"] == "prazo":
        partes_cmd = []
        if painel and r.get("painel", {}).get("domicilio"):
            partes_cmd.append(f"--ciencia {r['painel']['aberta_em'] or '[A CONFIRMAR: data da ciência no painel]'} --domicilio")
        elif painel and r.get("painel", {}).get("ciencia") == "sem-ciencia":
            partes_cmd.append(f"--envio-portal {r['painel']['enviada_em']}")
        elif painel and r.get("painel", {}).get("aberta_em"):
            partes_cmd.append(f"--ciencia {r['painel']['aberta_em']}")
        else:
            partes_cmd.append(f"--disponibilizacao {r['disponibilizada_em']}")
        variantes = []
        if r["dias"] and r["dias_fonte"] == "o próprio ato":
            variantes.append(f"--dias {r['dias']}" + (" --contagem corridos" if r["contagem"] == "corridos" else ""))
        elif r["candidatos_tabela"] or r.get("sem_linha_na_tabela"):
            variantes += [f"--ato \"{x['ato']}\"" for x in r["candidatos_tabela"]]
            variantes += [f"--dias [A CONFIRMAR: quantos dias para {x}]" for x in r.get("sem_linha_na_tabela", [])]
        else:
            variantes.append("--dias [A CONFIRMAR: quantos dias]")
        fim = (f"--rito {r['rito']} --tribunal {r['tribunal'] or '[A CONFIRMAR]'} "
               f"--regras \"{regras['arquivo'] or '<regras-de-contagem.md>'}\" --calendario \"<pasta dos calendários>\" "
               "--seguranca <dias_de_seguranca>")
        r["contas"] = [" ".join(partes_cmd + [v, fim]) for v in variantes]
        r["para_a_conta"] = r["contas"][0]

    r["resumo"] = resumo(r)
    return r


def resumo(r):
    """Até 120 caracteres, sem dado sensível: monta por categoria, nunca copia o teor."""
    t = r["triagem"]
    tipo = {"sentenca": "Sentença", "acordao": "Acórdão", "decisao": "Decisão", "despacho": "Despacho"}.get(r["tipo_ato"], "Ato")
    if t == "sem-caso":
        s = "Processo fora da carteira: para a pessoa"
    elif t in ("audiencia", "pericia"):
        s = r["o_que_pede"][:1].upper() + r["o_que_pede"][1:]
    elif t == "prazo" and r["dias_fonte"] == "o próprio ato":
        _, rotulo = acao_do_prazo(" ".join(r["trechos"]))
        s = f"{rotulo} em {r['dias']} dias"
        if r.get("tambem"):
            s += f"; {r['tambem']['o_que_pede']}"
    elif t == "prazo" and not r["candidatos_tabela"] and not r.get("sem_linha_na_tabela") and \
            not re.search(r"julg|homolog|extingo|acordam", espelho(" ".join(r["trechos"]))):
        rotulo = r["o_que_pede"][:1].upper() + r["o_que_pede"][1:] if not r["o_que_pede"].startswith("[") else "Prazo"
        s = f"{rotulo}: dias a confirmar"
        if r.get("tambem"):
            s += f"; {r['tambem']['o_que_pede']}"
    elif t == "prazo":
        if "improcedente" in espelho(" ".join(r["trechos"])):
            s = f"{tipo} de improcedência"
        elif "procedente" in espelho(" ".join(r["trechos"])):
            s = f"{tipo} de procedência"
        elif "homologo" in espelho(" ".join(r["trechos"])):
            s = f"{tipo} homologatória"
        else:
            s = tipo
        s += ": recurso pode caber"
    elif t == "ciencia" and r.get("lado") == "outra":
        quem = re.sub(r"^(o|a)\s+", "", r["destinatario"], flags=re.I) if len(r["destinatario"]) <= 8 else "outra parte"
        s = f"Prazo da outra parte ({quem}): ciência"
    elif t == "ciencia" and "valor" in r["o_que_pede"]:
        s = "Valor expedido (RPV, precatório ou alvará): ciência e acompanhamento"
    elif t == "ciencia":
        s = f"{tipo}: ciência"
    elif t == "urgente":
        s = f"{tipo} com sinal de urgência: para a pessoa agora"
    else:
        s = f"{tipo} sem providência aparente"
    return s[:120]


# ---------------------------------------------------------------- saída

def bloco_texto(r):
    caso = f"{r['codigo_caso']} · {r['cliente_curto'] or '[A CONFIRMAR]'}" + (f" · {r['area']}" if r['area'] else "") + \
        f" ({r['ligado_por']})" if r["codigo_caso"] else "SEM CASO (o número não está na carteira)"
    linhas = [f"{r['id']} · {r['fonte']} · {'enviada' if r['fonte'] == 'painel' else 'disponibilizada'} "
              f"{r['disponibilizada_em'] or 'SEM DATA'} · {r['tribunal']} · {r['orgao']}",
              f"  Caso: {caso}",
              f"  Triagem sugerida: {r['triagem']} · tipo do ato: {r['tipo_ato'] or '[A CONFIRMAR]'} · rito sugerido: {r['rito']}"]
    for t in r["trechos"]:
        linhas.append(f"  Trecho literal: \"{t}\"")
    if r["o_que_pede"]:
        linhas.append(f"  O que o ato parece pedir: {r['o_que_pede']}")
    if r.get("tambem"):
        linhas.append(f"  Também neste ato ({r['tambem']['triagem']}): {r['tambem']['o_que_pede']} · entra em prazos.csv como "
                      f"tipo = {r['tambem']['triagem']}")
    if r["triagem"] == "prazo" or r["dias"]:
        if r["dias"]:
            txt_dias = f"{r['dias']} ({r['dias_fonte'] or 'sem fonte'})"
        elif r["dias_fonte"].startswith("[A CONFIRMAR"):
            txt_dias = r["dias_fonte"]
        else:
            txt_dias = f"[A CONFIRMAR: quantos dias] ({r['dias_fonte'] or 'sem fonte'})"
        linhas.append(f"  Dias: {txt_dias}" + (f" · contagem: {r['contagem']}" if r['contagem'] else ""))
    if r["datas"] or r["horarios"]:
        linhas.append(f"  Datas no teor: {', '.join(r['datas']) or 'nenhuma'} · horários: {', '.join(r['horarios']) or 'nenhum'}")
    for p in r["pessoa_agora"]:
        linhas.append(f"  PESSOA AGORA: {p}")
    for av in r["avisos"]:
        linhas.append(f"  Aviso: {av}")
    for c in r.get("contas") or ([r["para_a_conta"]] if r["para_a_conta"] else []):
        linhas.append(f"  Para a conta (calcular-prazo): {c}")
    linhas.append(f"  Resumo para o registro: {r['resumo']}")
    return "\n".join(linhas)


def arquivo_do_dia(resultados, hoje, duplicadas, treino):
    ordem = {"urgente": 0, "prazo": 1, "audiencia": 2, "pericia": 2, "sem-caso": 3, "ciencia": 4,
             "sem-providencia": 5, "nao-triada": 6}
    agora = [r for r in resultados if r["pessoa_agora"]]
    partes = ["---", "documento: Triagem das publicações", f"data: {hoje}", "triada_por: ia (sugestão)",
              f"treino: {'sim' if treino else 'nao'}", "---", "", f"# Triagem de {hoje}", "",
              "Sugestão da IA, com o trecho literal de cada ato. Quem confirma o que o ato pede, os dias e a regra é uma pessoa, "
              "na dupla conferência. Nada daqui está na agenda.", "", "## PESSOA AGORA", ""]
    partes += [f"- {r['id']} · {r['codigo_caso'] or 'sem caso'} · " + "; ".join(r["pessoa_agora"]) for r in agora] or ["- nada"]
    for titulo, chaves in (("Prazos sugeridos (para a calcular-prazo)", ("prazo",)), ("Audiências e perícias", ("audiencia", "pericia")),
                           ("Urgentes", ("urgente",)), ("Sem caso", ("sem-caso",)), ("Ciência", ("ciencia",)),
                           ("Sem providência", ("sem-providencia",)), ("Não triadas", ("nao-triada",))):
        grupo = [r for r in resultados if r["triagem"] in chaves or (r.get("tambem") or {}).get("triagem") in chaves]
        if not grupo:
            continue
        partes += ["", f"## {titulo}", ""]
        for r in sorted(grupo, key=lambda x: (ordem.get(x["triagem"], 9), x["disponibilizada_em"])):
            partes += ["```", bloco_texto(r), "```", ""]
    if duplicadas:
        partes += ["## Duplicadas (marcadas na captação, nenhum segundo prazo)", ""]
        partes += [f"- {d['id']} · {d.get('resumo', '')}" for d in duplicadas]
    return "\n".join(partes).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Apoio da triagem das publicações")
    ap.add_argument("publicacoes", help="publicacoes.csv")
    ap.add_argument("--processos", help="processos.csv (a carteira de processos)")
    ap.add_argument("--regras", help="regras-de-contagem.md do escritório (prazos por ato)")
    ap.add_argument("--escritorio", help="pasta escritorio/, para procurar o número nos registros dos outros plugins")
    ap.add_argument("--ids", help="só estes ids, separados por vírgula")
    ap.add_argument("--todas", action="store_true", help="inclui as já triadas pela ia (nunca as confirmadas por pessoa)")
    ap.add_argument("--hoje", help="AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--ultima-rodada", help="AAAA-MM-DD da última rodada")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--gravar", action="store_true", help="atualiza publicacoes.csv e grava triagens/AAAA-MM-DD.md")
    ap.add_argument("--triagens", help="caminho do arquivo da triagem do dia (padrão: triagens/AAAA-MM-DD.md ao lado do csv)")
    a = ap.parse_args()

    hoje = data_iso(a.hoje) if a.hoje else dt.date.today().isoformat()
    ultima = data_iso(a.ultima_rodada) if a.ultima_rodada else ""
    pubs, delim, bom, cab_pub = ler_csv(a.publicacoes, OBRIG_PUBLICACOES, "o publicacoes.csv")
    pasta = os.path.dirname(os.path.abspath(a.publicacoes))
    treino = "_treino" in pasta.replace("\\", "/").split("/")

    carteira = {}
    if a.processos:
        procs, _, _, _ = ler_csv(a.processos, ["processo", "codigo_caso", "cliente_curto"], "a carteira de processos")
        if not procs:
            erro(f"{a.processos} não tem nenhum processo. Monte a carteira (carteira-de-processos) ou rode sem --processos")
        for p in procs:
            d = digitos(p["processo"])
            if d in carteira and carteira[d].get("codigo_caso") != p.get("codigo_caso"):
                print(f"AVISO: o processo {p['processo']} está duas vezes na carteira, com códigos diferentes", file=sys.stderr)
            carteira[d] = p
        if "_treino" in os.path.abspath(a.processos) or "de-treino" in os.path.basename(a.processos):
            if not treino:
                erro("a carteira é de treino e o publicacoes.csv é o real. Treino fica em _treino/")
    else:
        print("AVISO: sem --processos. Sem a carteira, toda publicação sai sem-caso, a não ser que --escritorio ache o número "
              "exato nos registros dos outros plugins.", file=sys.stderr)
    regras = ler_regras(a.regras)
    if a.regras and not regras["atos"]:
        print(f"AVISO: {a.regras} não tem a seção '## Prazos por ato' com linhas: sentenças ficam com [A CONFIRMAR: quantos dias]",
              file=sys.stderr)

    ids = {i.strip() for i in a.ids.split(",")} if a.ids else None
    alvo, duplicadas = [], []
    for p in pubs:
        if ids is not None:
            if p["id"] in ids:
                alvo.append(p)
            continue
        t = p.get("triagem", "")
        if t == "duplicada":
            duplicadas.append(p)
            continue
        if t == "nao-triada" or (a.todas and p.get("triada_por", "") in ("", "ia")):
            alvo.append(p)
    if ids is not None:
        faltam = ids - {p["id"] for p in alvo}
        if faltam:
            erro("não achei no registro: " + ", ".join(sorted(faltam)))
    if not alvo:
        nao = sum(1 for p in pubs if p.get("triagem") == "nao-triada")
        print(f"Nenhuma publicação a triar em {a.publicacoes} ({len(pubs)} linhas lidas, {nao} nao-triada).")
        return 0

    resultados = [triar(p, pasta, carteira, regras, a.escritorio, hoje, ultima) for p in alvo]
    if a.regras and not regras["validada"]:
        for r in resultados:
            if r["triagem"] == "prazo" and "tabela" in r["dias_fonte"]:
                r["avisos"].append("regra ainda não validada pelo escritório" + (" (tabela de treino)" if regras["treino"] else ""))

    if a.gravar:
        por_id = {r["id"]: r for r in resultados}
        for p in pubs:
            r = por_id.get(p["id"])
            if not r or r["triagem"] == "nao-triada":
                continue
            if p.get("triada_por", "") not in ("", "ia"):
                continue  # uma pessoa já confirmou: não mexe
            p["triagem"] = r["triagem"]
            p["triada_por"] = "ia"
            p["codigo_caso"] = r["codigo_caso"] if r["triagem"] != "sem-caso" else ""
            p["cliente_curto"] = r["cliente_curto"] if r["triagem"] != "sem-caso" else ""
            if r["tipo_ato"] in ("", "outro", "intimacao") and r["trechos"]:
                f = espelho(" ".join(r["trechos"]))
                if re.search(r"julgo|homologo|extingo", f):
                    p["tipo_ato"] = "sentenca"
                elif "acordam" in f:
                    p["tipo_ato"] = "acordao"
            p["resumo"] = r["resumo"]
            p["atualizado_em"] = hoje
        cab = list(pubs[0].keys())
        with open(a.publicacoes, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cab, delimiter=delim, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            for p in pubs:
                w.writerow(p)
        destino = a.triagens or os.path.join(pasta, "triagens", f"{hoje}.md")
        os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(arquivo_do_dia(resultados, hoje, duplicadas, treino))

    if a.json:
        for r in resultados:
            r.pop("candidatos_tabela", None)
        print(json.dumps({"hoje": hoje, "gravado": bool(a.gravar), "resultados": resultados,
                          "duplicadas": [d["id"] for d in duplicadas]}, ensure_ascii=False, indent=2))
        return 0

    contagem = {}
    for r in resultados:
        contagem[r["triagem"]] = contagem.get(r["triagem"], 0) + 1
    print(f"TRIAGEM SUGERIDA · {hoje} · {len(resultados)} publicações · " +
          " · ".join(f"{k} {v}" for k, v in sorted(contagem.items())) +
          (f" · duplicadas fora: {len(duplicadas)}" if duplicadas else "") +
          (" · gravado" if a.gravar else " · SIMULAÇÃO (nada gravado; use --gravar)"))
    agora = [r for r in resultados if r["pessoa_agora"]]
    if agora:
        print("\nPESSOA AGORA")
        for r in agora:
            print(f"  {r['id']} · {r['codigo_caso'] or 'sem caso'} · " + "; ".join(r["pessoa_agora"]))
    print()
    for r in resultados:
        print(bloco_texto(r))
        print()
    print("É sugestão: o trecho literal está em cada linha para a pessoa conferir. Próximo passo: calcular-prazo nas de prazo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
