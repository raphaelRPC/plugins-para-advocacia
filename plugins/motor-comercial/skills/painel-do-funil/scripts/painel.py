#!/usr/bin/env python3
"""Painel do mês a partir do registro de contatos do motor-comercial.

Lê o contatos.csv (formato em docs/funil.md do plugin) e calcula, para os
contatos que entraram no período pedido: entradas por origem, área e canal;
quantos chegaram a cada etapa do funil e a conversão entre elas; tempo até a
primeira resposta de uma pessoa e quem ficou sem resposta; propostas enviadas
e valor; fechamentos; motivos de perda; quem pediu para parar; e a qualidade
do próprio registro.

Imprime um markdown com tabelas e grava um .csv resumido ao lado. Com --html,
grava também uma página para abrir como artefato do Claude, só para uso
interno do escritório. Com --xlsx e openpyxl instalado, grava um .xlsx.
Só usa a biblioteca padrão. Não altera o contatos.csv. Mostra contatos só
pelo código: nunca nome, assunto, telefone ou documento.

Uso (rode da pasta de trabalho, com o caminho da pasta da habilidade):
  python3 <pasta-da-habilidade>/scripts/painel.py escritorio/07-operacao/comercial/contatos.csv 2026-03
  python3 <pasta-da-habilidade>/scripts/painel.py escritorio/07-operacao/comercial/contatos.csv 2026-01:2026-03

Opções:
  --saida PASTA          onde gravar AAAA-MM-numeros.csv (padrão: painel/ ao lado do csv)
  --md ARQUIVO           grava também o markdown neste arquivo
  --html ARQUIVO         grava a versão HTML do painel (uso interno, nunca para cliente)
  --xlsx                 grava AAAA-MM-numeros.xlsx, se openpyxl existir
  --prazo-horas TEXTO    primeira_resposta_contato_novo da ficha comercial, em horas úteis. Aceita o
                         número (2, 1.5, 1,5) ou o texto da ficha ("até 2 horas úteis", "1h30",
                         "30 minutos"). Vazio ou [A PREENCHER]: o painel sai sem o prazo, com aviso
  --horario TEXTO        horario_de_atendimento da ficha do escritório, como está escrito ou em
                         HH:MM-HH:MM (padrão 09:00-18:00). Exemplos aceitos: "dias úteis, das 9h às
                         18h", "9h-18h", "8h30 às 12h e 14h às 18h", "09:00-12:00,14:00-18:00",
                         "dias úteis das 9h às 18h; sábado das 9h às 12h"
  --dias seg-sex         dias de atendimento (padrão seg-sex; aceita lista: seg,ter,qua)
  --origens LISTA        opções de origem_dos_contatos da ficha comercial, separadas por vírgula
  --areas LISTA          áreas da ficha do escritório, separadas por vírgula
  --hoje AAAA-MM-DD      data de referência (mês em curso e espera de quem está sem resposta)
  --treino               permite ler um registro de treino (pasta _treino); o painel sai marcado

Regras de leitura: vírgula ou ponto e vírgula; com ou sem BOM; cabeçalho, etapa e
opções sem diferenciar maiúscula; datas AAAA-MM-DD HH:MM ou DD/MM/AAAA HH:MM.
Sai com código 1 e uma mensagem clara quando falta o arquivo, quando ele está vazio
ou quando falta uma coluna obrigatória (codigo, entrada, etapa).
"""

import argparse
import csv
import html
import io
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter, OrderedDict
from datetime import date, datetime, time, timedelta

COLUNAS_DO_FUNIL = [
    "codigo", "entrada", "canal", "origem", "nome_curto", "tipo", "area", "assunto",
    "urgencia", "etapa", "responsavel", "proximo_passo", "data_proximo_passo",
    "primeira_resposta", "valor_proposta", "motivo_perda", "perdido_na_etapa",
    "pediu_para_parar", "atualizado_em",
]
OBRIGATORIAS = ["codigo", "entrada", "etapa"]

ETAPAS = [
    "novo", "triado", "consulta-agendada", "nao-compareceu", "consulta-feita",
    "proposta-enviada", "negociando", "fechado",
    "encaminhado", "recusado", "sem-caso", "perdido",
]

# Até onde o contato chegou no caminho principal, pela etapa atual.
# 0 entrou, 1 triado, 2 consulta agendada, 3 consulta feita, 4 proposta, 5 fechado.
PROFUNDIDADE = {
    "novo": 0, "triado": 1, "encaminhado": 1, "recusado": 1,
    "consulta-agendada": 2, "nao-compareceu": 2,
    "consulta-feita": 3, "sem-caso": 3,
    "proposta-enviada": 4, "negociando": 4,
    "fechado": 5,
}

EM_ANDAMENTO = {"novo", "triado", "consulta-agendada", "nao-compareceu",
                "consulta-feita", "proposta-enviada", "negociando"}
ANTES_DA_CONSULTA = {"novo", "triado"}
# Marcador de pessoa no proximo_passo (funil.md, regra 4), já normalizado (minúsculas, sem acento).
MARCADORES_DE_PESSOA = ("pessoa agora", "pessoa liga")

MOTIVOS = ["preco", "fechou-com-outro", "desistiu", "sem-resposta", "outro"]
TIPOS = {"novo", "antigo", ""}

DIAS_NOMES = {"seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5, "dom": 6}

MINIMO_PARA_PERCENTUAL = 10
AMOSTRA_PEQUENA = 20


def falhar(msg):
    sys.stderr.write("painel.py: " + msg + "\n")
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def norm(texto):
    return sem_acento((texto or "").strip().lower())


# ---------------------------------------------------------------- leitura

def ler_csv(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    texto = (texto or "").lstrip("\ufeff")
    if not texto.strip():
        falhar("o arquivo %s está vazio. O registro começa com a primeira linha de docs/funil.md." % caminho)
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    colunas = [norm(c) for c in (leitor.fieldnames or [])]
    leitor.fieldnames = colunas
    linhas = []
    for bruta in leitor:
        linha = {}
        for k, v in bruta.items():
            if k is None:
                continue
            linha[k] = (v or "").strip() if isinstance(v, str) else ""
        if any(linha.values()):
            linhas.append(linha)
    return colunas, linhas, sep


def data_hora(texto):
    texto = (texto or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, fmt)
        except ValueError:
            continue
    return None


def valor(texto):
    t = (texto or "").replace("R$", "").replace(" ", "").strip()
    if not t:
        return None
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    elif t.count(".") == 1 and len(t.split(".")[1]) == 3:
        t = t.replace(".", "")
    elif t.count(".") > 1:
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


# ---------------------------------------------------------------- horas úteis

# Leitura do horário e do prazo como estão escritos na ficha. Cópia própria da leitura do
# pendencias.py da rotina-comercial (cada habilidade funciona sozinha).
HORARIO_RE = re.compile(r"(\d{1,2})\s*(?:(?:h|:)\s*(\d{2})?|horas?\b)", re.I)


def horarios_do_texto(trecho):
    """'das 8h30 às 12h e das 14h às 18h' -> [(08:30, 12:00), (14:00, 18:00)]."""
    pontos = []
    for m in HORARIO_RE.finditer(trecho):
        hh, mi = int(m.group(1)), int(m.group(2) or 0)
        if hh > 24 or mi > 59:
            continue
        pontos.append(time(23, 59) if hh == 24 else time(hh, mi))
    if not pontos:
        for m in re.finditer(r"\b(\d{1,2})\s*(?:a|as|ate|-)\s*(\d{1,2})\b", trecho):
            if int(m.group(1)) < int(m.group(2)) <= 24:
                pontos += [time(int(m.group(1)), 0), time(23, 59) if m.group(2) == "24" else time(int(m.group(2)), 0)]
    turnos = []
    for i in range(0, len(pontos) - 1, 2):
        if pontos[i + 1] > pontos[i]:
            turnos.append((pontos[i], pontos[i + 1]))
    return turnos


def ler_horario(texto):
    """horario_de_atendimento da ficha -> (turnos dos dias úteis, turnos do sábado)."""
    bruto = (texto or "").strip()
    if not bruto or "a preencher" in norm(bruto):
        falhar("o horário de atendimento está vazio ou [A PREENCHER] na ficha. Passe em --horario o texto do "
               "campo horario_de_atendimento (ex.: \"dias úteis, das 9h às 18h\") ou HH:MM-HH:MM. "
               "Nenhum número foi calculado.")
    uteis, sabado = [], []
    for parte in re.split(r"[;\n]", bruto):
        n = norm(parte)
        if not n:
            continue
        turnos = horarios_do_texto(n)
        fala_de_sabado = "sabado" in n and not re.search(r"(exceto|menos|sem|nao)\s+(aos\s+|no\s+)?sabado", n)
        so_sabado = fala_de_sabado and not re.search(r"segunda|dias uteis|semana|seg\b", n)
        if so_sabado:
            sabado += turnos
        else:
            uteis += turnos
            if fala_de_sabado:
                sabado += turnos
    if not uteis:
        falhar("não consegui ler horas em --horario \"%s\". Use o horário com horas, como \"dias úteis, das 9h "
               "às 18h\", \"8h30 às 12h e 14h às 18h\" ou 09:00-18:00. Nenhum número foi calculado." % texto)
    return uteis, sabado


def fmt_turnos(turnos):
    return " e ".join("%s-%s" % (a.strftime("%H:%M"), b.strftime("%H:%M")) for a, b in turnos)


def ler_prazo(texto):
    """primeira_resposta_contato_novo da ficha -> horas úteis (float), ou None se o campo está vazio."""
    bruto = (texto or "").strip()
    n = norm(bruto).replace(",", ".")
    if not re.sub(r"[\s\[\]]", "", n) or "a preencher" in n or "a definir" in n:
        return None
    if re.fullmatch(r"\d+(\.\d+)?", n):
        return float(n)
    if "meia hora" in n:
        return 0.5
    m = re.search(r"(\d+(?:\.\d+)?)\s*h(?:oras?)?\s*(\d{1,2})?\b", n)
    if m and "dia" not in n[m.end():m.end() + 4]:
        return float(m.group(1)) + (int(m.group(2)) / 60 if m.group(2) else 0)
    m = re.search(r"(\d+)\s*min", n)
    if m:
        return int(m.group(1)) / 60
    falhar("não consegui ler --prazo-horas \"%s\" como horas úteis. Converta antes de rodar: \"no mesmo dia\" "
           "ou \"em 1 dia útil\" viram um número de horas úteis que o escritório decide (pergunte: \"Em horas "
           "úteis, quanto é isso para vocês?\")." % texto)


def turnos_por_dia(uteis, sabado, dias):
    """Dia da semana (0 = segunda) -> turnos. Sábado com horário próprio na ficha entra mesmo fora de --dias."""
    mapa = {}
    for d in dias:
        mapa[d] = (sabado or uteis) if d == 5 else uteis
    if sabado and 5 not in mapa:
        mapa[5] = sabado
    return mapa


def ler_dias(texto):
    texto = norm(texto)
    try:
        if "-" in texto and "," not in texto:
            a, b = texto.split("-")
            return set(range(DIAS_NOMES[a.strip()], DIAS_NOMES[b.strip()] + 1))
        return {DIAS_NOMES[d.strip()] for d in texto.split(",") if d.strip()}
    except KeyError:
        falhar("dias inválidos: %s. Use seg-sex ou uma lista como seg,ter,qua." % texto)


def horas_uteis(inicio, fim, horario, dias=None):
    """Horas dentro dos turnos de atendimento entre inicio e fim. Ignora feriados.

    horario: dia da semana (0 = segunda) -> lista de turnos (time, time), de turnos_por_dia."""
    if fim <= inicio:
        return 0.0
    total = 0.0
    dia = inicio.date()
    while dia <= fim.date():
        for t_ini, t_fim in horario.get(dia.weekday(), []):
            a = max(datetime.combine(dia, t_ini), inicio)
            b = min(datetime.combine(dia, t_fim), fim)
            if b > a:
                total += (b - a).total_seconds() / 3600.0
        dia += timedelta(days=1)
    return total


# ---------------------------------------------------------------- período

def mes_anterior(mes):
    ano, m = [int(x) for x in mes.split("-")]
    if m == 1:
        return "%04d-12" % (ano - 1)
    return "%04d-%02d" % (ano, m - 1)


def ultimo_dia(mes):
    ano, m = [int(x) for x in mes.split("-")]
    prox = date(ano + 1, 1, 1) if m == 12 else date(ano, m + 1, 1)
    return prox - timedelta(days=1)


def nome_do_mes(mes):
    ano, m = mes.split("-")
    return "%s/%s" % (m, ano)


def meses_do_periodo(texto):
    """'2026-03' vira ['2026-03']; '2026-01:2026-03' vira os três meses."""
    ini, fim = texto.split(":") if ":" in texto else (texto, texto)
    for t in (ini, fim):
        datetime.strptime(t, "%Y-%m")
    if fim < ini:
        raise ValueError("fim antes do início")
    meses = [ini]
    while meses[-1] != fim:
        ano, m = [int(x) for x in meses[-1].split("-")]
        meses.append("%04d-%02d" % (ano + (m == 12), 1 if m == 12 else m + 1))
    return meses


def periodo_anterior(meses):
    saida = [mes_anterior(meses[0])]
    while len(saida) < len(meses):
        saida.insert(0, mes_anterior(saida[0]))
    return saida


def nome_do_periodo(meses):
    if len(meses) == 1:
        return nome_do_mes(meses[0])
    return "%s a %s" % (nome_do_mes(meses[0]), nome_do_mes(meses[-1]))


# ---------------------------------------------------------------- cálculo

def profundidade(linha):
    etapa = norm(linha.get("etapa"))
    if etapa in PROFUNDIDADE:
        return PROFUNDIDADE[etapa], False
    if etapa == "perdido":
        antes = norm(linha.get("perdido_na_etapa"))
        if antes in PROFUNDIDADE:
            return PROFUNDIDADE[antes], False
        if valor(linha.get("valor_proposta")) is not None:
            return 4, False
        return 1, True
    return 0, False


def coorte(linhas, meses):
    """Contatos que entraram no período (tipo novo, antigo ou vazio). Linha de cliente fica fora."""
    saida = []
    for l in linhas:
        dt = data_hora(l.get("entrada"))
        if dt is None or dt.strftime("%Y-%m") not in meses:
            continue
        if norm(l.get("tipo")) == "cliente":
            continue
        saida.append(l)
    return saida


def funil(contatos):
    prof = []
    perdidos_sem_etapa = 0
    for l in contatos:
        p, sem = profundidade(l)
        prof.append(p)
        if sem:
            perdidos_sem_etapa += 1

    def chegaram(n):
        return sum(1 for p in prof if p >= n)

    etapas = Counter(norm(l.get("etapa")) for l in contatos)
    n = len(contatos)
    triados = chegaram(1)
    fora = etapas["encaminhado"] + etapas["recusado"]
    agendados = chegaram(2)
    feitas = chegaram(3)
    sem_caso = etapas["sem-caso"]
    propostas = chegaram(4)
    fechados = chegaram(5)
    passagens = [
        ("Entraram > triados", triados, n),
        ("Triados atendíveis > consulta agendada", agendados, triados - fora),
        ("Consulta agendada > consulta feita", feitas, agendados),
        ("Consulta feita com caso > proposta enviada", propostas, feitas - sem_caso),
        ("Proposta enviada > fechado", fechados, propostas),
        ("Entraram > fechado", fechados, n),
    ]
    em_andamento = sum(1 for l in contatos if norm(l.get("etapa")) in EM_ANDAMENTO)
    return {
        "n": n, "etapas": etapas, "passagens": passagens,
        "em_andamento": em_andamento, "perdidos_sem_etapa": perdidos_sem_etapa,
        "fechados": fechados, "propostas": propostas,
        "encaminhados": etapas["encaminhado"], "recusados": etapas["recusado"],
        "nao_compareceu": etapas["nao-compareceu"], "sem_caso": sem_caso,
    }


def taxa(x, de):
    if de <= 0:
        return "sem base"
    if de < MINIMO_PARA_PERCENTUAL:
        return "poucos casos"
    return "%d%%" % round(100.0 * x / de)


def fechou(l):
    return norm(l.get("etapa")) == "fechado"


def por_campo(contatos, campo, vazio):
    tabela = OrderedDict()
    for l in contatos:
        chave = norm(l.get(campo)) or vazio
        linha = tabela.setdefault(chave, {"entraram": 0, "propostas": 0, "fecharam": 0, "valor_fechado": 0.0})
        linha["entraram"] += 1
        v = valor(l.get("valor_proposta"))
        if profundidade(l)[0] >= 4:
            linha["propostas"] += 1
        if fechou(l):
            linha["fecharam"] += 1
            if v is not None:
                linha["valor_fechado"] += v
    return OrderedDict(sorted(tabela.items(), key=lambda kv: (-kv[1]["entraram"], kv[0])))


def tempos(contatos, horario, dias, prazo, agora):
    medidas = []
    sem_resposta = []          # novo ou triado, primeira_resposta vazia
    perdidos_sem_resposta = []  # perdido sem nunca ter recebido resposta de uma pessoa
    com_pessoa = []             # marcador de pessoa (funil.md, regra 4) sem retorno registrado
    for l in contatos:
        ini = data_hora(l.get("entrada"))
        fim = data_hora(l.get("primeira_resposta"))
        etapa = norm(l.get("etapa"))
        if ini is None:
            continue
        if fim is None:
            if etapa in ANTES_DA_CONSULTA:
                sem_resposta.append((l.get("codigo") or "(sem código)", horas_uteis(ini, agora, horario, dias),
                                     norm(l.get("urgencia"))))
                if norm(l.get("proximo_passo")).startswith(MARCADORES_DE_PESSOA):
                    com_pessoa.append(l.get("codigo") or "(sem código)")
            elif etapa == "perdido" and norm(l.get("perdido_na_etapa")) in ANTES_DA_CONSULTA | {""}:
                perdidos_sem_resposta.append(l.get("codigo") or "(sem código)")
            continue
        if fim < ini:
            continue
        corridas = (fim - ini).total_seconds() / 3600.0
        uteis = horas_uteis(ini, fim, horario, dias)
        medidas.append((l, corridas, uteis))
    res = {"com_dado": len(medidas), "sem_resposta": sorted(sem_resposta, key=lambda x: (x[2] != "alta", -x[1])),
           "perdidos_sem_resposta": perdidos_sem_resposta, "com_pessoa": com_pessoa}
    if not medidas:
        return res
    uteis = [m[2] for m in medidas]
    corridas = [m[1] for m in medidas]
    res.update({
        "mediana_uteis": statistics.median(uteis),
        "maior_uteis": max(uteis),
        "mediana_corridas": statistics.median(corridas),
        "por_canal": OrderedDict(),
        "fora_do_prazo": [],
    })
    canais = {}
    for l, c, u in medidas:
        canais.setdefault(norm(l.get("canal")) or "(sem canal)", []).append(u)
    for canal in sorted(canais, key=lambda k: (-len(canais[k]), k)):
        res["por_canal"][canal] = (len(canais[canal]), statistics.median(canais[canal]))
    if prazo is not None:
        res["dentro"] = sum(1 for m in medidas if m[2] <= prazo)
        res["fora_do_prazo"] = [(m[0].get("codigo", "?"), m[2]) for m in medidas if m[2] > prazo]
    return res


def propostas_e_valores(contatos):
    soma = {"total": 0.0, "fechado": 0.0, "aberto": 0.0, "perdido": 0.0}
    qtd = {"total": 0, "fechado": 0, "aberto": 0, "perdido": 0}
    for l in contatos:
        v = valor(l.get("valor_proposta"))
        if v is None:
            continue
        etapa = norm(l.get("etapa"))
        soma["total"] += v
        qtd["total"] += 1
        chave = {"fechado": "fechado", "proposta-enviada": "aberto", "negociando": "aberto",
                 "perdido": "perdido"}.get(etapa)
        if chave:
            soma[chave] += v
            qtd[chave] += 1
    return {"n_total": qtd["total"], "total": soma["total"],
            "n_fechado": qtd["fechado"], "fechado": soma["fechado"],
            "n_aberto": qtd["aberto"], "aberto": soma["aberto"],
            "n_perdido": qtd["perdido"], "perdido": soma["perdido"]}


def atualizados_no_mes(linhas, meses):
    """Fechados e perdidos cuja última atualização caiu no período, de qualquer entrada."""
    fech = perd = 0
    for l in linhas:
        dt = data_hora(l.get("atualizado_em"))
        if dt is None or dt.strftime("%Y-%m") not in meses or norm(l.get("tipo")) == "cliente":
            continue
        etapa = norm(l.get("etapa"))
        if etapa == "fechado":
            fech += 1
        elif etapa == "perdido":
            perd += 1
    return fech, perd


def qualidade(linhas, colunas, origens_ficha, areas_ficha):
    problemas = OrderedDict()

    def anota(chave, codigo):
        lista = problemas.setdefault(chave, [])
        cod = codigo or "(sem código)"
        if cod not in lista:
            lista.append(cod)

    vistos = Counter(l.get("codigo", "") for l in linhas)
    for l in linhas:
        cod = l.get("codigo", "")
        etapa = norm(l.get("etapa"))
        tipo = norm(l.get("tipo"))
        if not cod:
            anota("linha sem código", "")
        elif vistos[cod] > 1:
            anota("código repetido (uma linha por contato)", cod)
        if data_hora(l.get("entrada")) is None:
            anota("entrada vazia ou fora do formato AAAA-MM-DD HH:MM", cod)
        if etapa not in ETAPAS:
            anota("etapa fora da lista do funil", cod)
        if tipo == "cliente":
            anota("linha de cliente ativo no registro comercial (cliente ativo sai do comercial)", cod)
        elif tipo not in TIPOS:
            anota("tipo diferente de novo ou antigo", cod)
        if tipo != "cliente":
            if not norm(l.get("origem")):
                anota("contato sem origem", cod)
            elif origens_ficha and norm(l.get("origem")) not in origens_ficha:
                anota("origem fora das opções da ficha", cod)
        if not norm(l.get("area")):
            anota("sem área", cod)
        elif areas_ficha and norm(l.get("area")) not in areas_ficha | {"fora-da-area", "a-confirmar"}:
            anota("área fora das áreas da ficha (use fora-da-area)", cod)
        if etapa == "perdido" and not norm(l.get("motivo_perda")):
            anota("perdido sem motivo", cod)
        if etapa == "perdido" and norm(l.get("motivo_perda")) and norm(l.get("motivo_perda")) not in MOTIVOS:
            anota("motivo de perda fora da lista", cod)
        if "perdido_na_etapa" in colunas and etapa == "perdido" and not norm(l.get("perdido_na_etapa")):
            anota("perdido sem perdido_na_etapa", cod)
        if etapa in ("proposta-enviada", "negociando", "fechado") and valor(l.get("valor_proposta")) is None:
            anota("proposta sem valor registrado (ou proposta só de êxito: confirmar)", cod)
        if ("primeira_resposta" in colunas and etapa in PROFUNDIDADE and PROFUNDIDADE[etapa] >= 2
                and not norm(l.get("primeira_resposta"))):
            anota("passou da triagem sem primeira_resposta registrada", cod)
        if norm(l.get("pediu_para_parar")) not in ("sim", "nao", ""):
            anota("pediu_para_parar diferente de sim ou nao", cod)
        ini, pr = data_hora(l.get("entrada")), data_hora(l.get("primeira_resposta"))
        if ini and pr and pr < ini:
            anota("primeira_resposta antes da entrada", cod)
    return problemas


def calcular(colunas, linhas, meses, opcoes):
    atual = coorte(linhas, set(meses))
    anteriores = periodo_anterior(meses)
    anterior = coorte(linhas, set(anteriores))
    r = OrderedDict()
    r["mes"] = nome_do_periodo(meses)
    r["mes_anterior"] = nome_do_periodo(anteriores)
    r["varios_meses"] = len(meses) > 1
    r["treino"] = opcoes["treino"]
    r["n"] = len(atual)
    r["n_antigos"] = sum(1 for l in atual if norm(l.get("tipo")) == "antigo")
    r["n_anterior"] = len(anterior)
    r["funil"] = funil(atual)
    r["funil_anterior"] = funil(anterior)
    r["origem"] = por_campo(atual, "origem", "(sem origem)")
    r["area"] = por_campo(atual, "area", "(sem área)")
    r["canal"] = por_campo(atual, "canal", "(sem canal)")
    r["origem_ant"] = Counter(norm(l.get("origem")) or "(sem origem)" for l in anterior)
    r["area_ant"] = Counter(norm(l.get("area")) or "(sem área)" for l in anterior)
    r["canal_ant"] = Counter(norm(l.get("canal")) or "(sem canal)" for l in anterior)
    faltam = [c for c in COLUNAS_DO_FUNIL if c not in colunas]
    r["colunas_faltando"] = faltam
    r["tempos"] = (tempos(atual, opcoes["horario"], opcoes["dias"], opcoes["prazo"], opcoes["agora"])
                   if "primeira_resposta" in colunas else None)
    r["valores"] = propostas_e_valores(atual)
    perdidos = [l for l in atual if norm(l.get("etapa")) == "perdido"]
    r["perdidos"] = len(perdidos)
    r["motivos"] = Counter(norm(l.get("motivo_perda")) or "(sem motivo)" for l in perdidos)
    r["pararam"] = [l.get("codigo", "?") for l in atual if norm(l.get("pediu_para_parar")) == "sim"]
    r["pararam_total"] = sum(1 for l in linhas if norm(l.get("pediu_para_parar")) == "sim")
    r["atualizados"] = atualizados_no_mes(linhas, set(meses))
    r["qualidade"] = qualidade(linhas, colunas, opcoes["origens"], opcoes["areas"])
    r["total_registro"] = len(linhas)
    r["prazo"] = opcoes["prazo"]

    cuidados = []
    if r["treino"]:
        cuidados.append("TREINO: este painel foi feito com o registro de treino (_treino). Nada daqui vale "
                        "como número do escritório nem vai para o painel real.")
    hoje = opcoes["hoje"]
    fim = ultimo_dia(meses[-1])
    if hoje.strftime("%Y-%m") == meses[-1] and hoje < fim:
        cuidados.append("Período em curso: os números vão até %s, dia %d de %d. Compare com o período anterior "
                        "com cuidado." % (hoje.strftime("%d/%m"), hoje.day, fim.day))
    if hoje < date(int(meses[0][:4]), int(meses[0][5:]), 1):
        cuidados.append("O período pedido ainda não começou na data de referência.")
    if faltam:
        cuidados.append("O registro não tem as colunas %s, que fazem parte de docs/funil.md. O que depende "
                        "delas fica de fora (veja cada seção). Acrescente as colunas no fim da primeira linha."
                        % ", ".join(faltam))
    if r["n"] < AMOSTRA_PEQUENA:
        cuidados.append("Amostra pequena: %d contatos no período. Com menos de %d numa passagem, o painel mostra "
                        "'x de y' e não percentual. Uma variação de dois ou três contatos muda tudo.%s" % (
                            r["n"], MINIMO_PARA_PERCENTUAL,
                            "" if r["varios_meses"] else " Vale rodar o trimestre junto (AAAA-MM:AAAA-MM)."))
    if r["n"] and r["n_anterior"] == 0:
        cuidados.append("O período anterior (%s) não tem nenhum contato no registro: primeiro mês do registro, ou "
                        "os contatos antigos estão em outro lugar. A coluna Anterior não serve para comparar."
                        % r["mes_anterior"])
    if r["n_antigos"]:
        cuidados.append("Contatos do período com tipo antigo (já falavam com o escritório antes do registro): %d. "
                        "Entram no funil, mas não são entrada nova de verdade." % r["n_antigos"])
    if r["funil"]["em_andamento"]:
        cuidados.append("%d contatos do período ainda estão em andamento. A conversão das etapas finais ainda vai "
                        "mudar; o período fecha de verdade quando eles chegarem a um fim." % r["funil"]["em_andamento"])
    if r["funil"]["perdidos_sem_etapa"]:
        n_pse = r["funil"]["perdidos_sem_etapa"]
        cuidados.append("%s sem perdido_na_etapa e sem valor de proposta: %s como perdido logo depois da triagem. "
                        "Se foi perdido mais adiante, a conversão real das etapas do meio é maior."
                        % ("1 perdido" if n_pse == 1 else "%d perdidos" % n_pse, "conta" if n_pse == 1 else "contam"))
    repetidos = r["qualidade"].get("código repetido (uma linha por contato)")
    if repetidos:
        cuidados.append("Códigos repetidos no registro (%s): o painel conta cada linha. Corrija o registro e rode "
                        "de novo." % ", ".join(repetidos))
    t = r["tempos"]
    if t is not None:
        if t["com_dado"] < r["n"]:
            cuidados.append("Tempo de resposta medido em %d de %d contatos. Os outros estão sem primeira_resposta: "
                            "ou ainda não foram respondidos (seção 3) ou a hora não foi registrada (seção 7)."
                            % (t["com_dado"], r["n"]))
        cuidados.append("Horas úteis contadas no horário %s, sem descontar feriados." % opcoes["horario_txt"])
    if opcoes.get("prazo_vazio"):
        cuidados.append("Campo primeira_resposta_contato_novo da ficha vazio (%s): o painel saiu sem a conta "
                        "do prazo." % opcoes["prazo_vazio"])
    r["cuidados"] = cuidados
    return r


# ---------------------------------------------------------------- saída em markdown

def dinheiro(v):
    return "{:,.0f}".format(v).replace(",", ".")


def horas(h):
    if h < 1:
        return "%d min" % round(h * 60)
    return ("%.1f h" % h).replace(".", ",")


def variacao(atual, anterior):
    d = atual - anterior
    return ("+%d" % d) if d > 0 else ("%d" % d)


def markdown(r):
    m = []
    add = m.append
    add("# Painel do funil · %s%s" % (r["mes"], " · TREINO" if r["treino"] else ""))
    add("")
    add("Números calculados pelo script a partir de `contatos.csv` (%d linhas no registro). "
        "Contatos que entraram no período: **%d**. Coluna \"Anterior\": %s, com %d contatos. As leituras "
        "e as ações vêm depois, escritas com o advogado. Uso interno: o painel não vai para cliente."
        % (r["total_registro"], r["n"], r["mes_anterior"], r["n_anterior"]))
    add("")
    if r["cuidados"]:
        add("## Cuidados antes de ler")
        add("")
        for c in r["cuidados"]:
            add("- " + c)
        add("")

    if r["n"] == 0:
        add("Nenhum contato com entrada neste período. Confira se o período pedido está certo e se a coluna "
            "`entrada` está no formato AAAA-MM-DD HH:MM.")
        add("")
        secao_qualidade(r, add)
        return "\n".join(m)

    add("## 1. Entradas")
    add("")
    for titulo, chave, ant in (("Por origem", "origem", "origem_ant"),
                               ("Por área", "area", "area_ant"),
                               ("Por canal", "canal", "canal_ant")):
        add("### %s" % titulo)
        add("")
        add("| %s | Entraram | Anterior | Variação | Propostas | Fecharam | Valor fechado |" % titulo[4:].capitalize())
        add("|---|---|---|---|---|---|---|")
        for k in linhas_da_tabela(r, chave, ant):
            d = r[chave].get(k, {"entraram": 0, "propostas": 0, "fecharam": 0, "valor_fechado": 0.0})
            add("| %s | %d | %d | %s | %d | %d | %s |" % (
                k, d["entraram"], r[ant].get(k, 0), variacao(d["entraram"], r[ant].get(k, 0)),
                d["propostas"], d["fecharam"], dinheiro(d["valor_fechado"]) if d["valor_fechado"] else "0"))
        add("")

    f = r["funil"]
    fa = r["funil_anterior"]
    add("## 2. Funil dos contatos do período")
    add("")
    add("| Passagem | Chegaram | De | Taxa | Anterior |")
    add("|---|---|---|---|---|")
    for (nome, x, de), (_, xa, dea) in zip(f["passagens"], fa["passagens"]):
        add("| %s | %d | %d | %s | %d de %d |" % (nome, x, de, taxa(x, de), xa, dea))
    add("")
    add("Onde estão hoje:")
    add("")
    add("| Etapa | Contatos |")
    add("|---|---|")
    for e in ETAPAS:
        if f["etapas"].get(e):
            add("| %s | %d |" % (e, f["etapas"][e]))
    for e in [e for e in f["etapas"] if e not in ETAPAS]:
        add("| %s (fora da lista) | %d |" % (e or "(vazia)", f["etapas"][e]))
    add("")
    add("Encaminhados: %d. Recusados: %d. Não compareceram: %d. Sem caso: %d. Ainda em andamento: %d." % (
        f["encaminhados"], f["recusados"], f["nao_compareceu"], f["sem_caso"], f["em_andamento"]))
    add("")

    add("## 3. Primeira resposta de uma pessoa")
    add("")
    t = r["tempos"]
    if t is None:
        add("O registro não tem a coluna `primeira_resposta` (docs/funil.md). Sem ela, não dá para medir o tempo "
            "nem saber quem ficou sem resposta. A `auditar-conversas-comerciais`, se instalada, mede o tempo direto "
            "nas conversas exportadas.")
    else:
        if t["com_dado"]:
            add("| Medida | Valor |")
            add("|---|---|")
            add("| Contatos com a hora registrada | %d de %d |" % (t["com_dado"], r["n"]))
            add("| Mediana em horas úteis | %s |" % horas(t["mediana_uteis"]))
            add("| Maior espera em horas úteis | %s |" % horas(t["maior_uteis"]))
            add("| Mediana em horas corridas | %s |" % horas(t["mediana_corridas"]))
            if "dentro" in t:
                add("| Dentro do prazo da ficha (%s úteis) | %d de %d (%s) |" % (
                    horas(r["prazo"]), t["dentro"], t["com_dado"], taxa(t["dentro"], t["com_dado"])))
            else:
                add("| Dentro do prazo da ficha | sem o prazo (rode com --prazo-horas) |")
            add("")
            add("| Canal | Medidos | Mediana em horas úteis |")
            add("|---|---|---|")
            for canal, (qtd, med) in t["por_canal"].items():
                add("| %s | %d | %s |" % (canal, qtd, horas(med)))
            add("")
            if t.get("fora_do_prazo"):
                add("Fora do prazo: " + ", ".join("%s (%s)" % (c, horas(h)) for c, h in t["fora_do_prazo"]) + ".")
                add("")
        else:
            add("Nenhum contato do período tem a hora da primeira resposta registrada.")
            add("")
        if t["sem_resposta"]:
            add("**Sem resposta de uma pessoa até a data de referência** (novo ou triado com `primeira_resposta` "
                "vazia): " + ", ".join("%s (%s úteis%s)" % (c, horas(h), ", urgência alta" if u == "alta" else "")
                                       for c, h, u in t["sem_resposta"]) + ".")
            add("")
        if t["perdidos_sem_resposta"]:
            add("Perdidos sem nunca terem recebido resposta de uma pessoa: %s." % ", ".join(t["perdidos_sem_resposta"]))
            add("")
        if t.get("com_pessoa"):
            add("**Com uma pessoa (PESSOA AGORA), sem retorno registrado:** %s. Se a ligação ou a conversa já "
                "aconteceu, registre o combinado pelo comando `fila` (ele grava a `primeira_resposta` e troca o "
                "`proximo_passo`); se não aconteceu, é o primeiro item do dia." % ", ".join(t["com_pessoa"]))
            add("")

    v = r["valores"]
    add("## 4. Propostas e fechamentos")
    add("")
    add("| Item | Quantidade | Valor somado |")
    add("|---|---|---|")
    add("| Propostas com valor registrado (contatos do período) | %d | %s |" % (v["n_total"], dinheiro(v["total"])))
    add("| Fechadas | %d | %s |" % (v["n_fechado"], dinheiro(v["fechado"])))
    add("| Em aberto (enviada ou negociando) | %d | %s |" % (v["n_aberto"], dinheiro(v["aberto"])))
    add("| Perdidas com proposta | %d | %s |" % (v["n_perdido"], dinheiro(v["perdido"])))
    add("")
    if r["funil"]["fechados"] != v["n_fechado"]:
        add("Fechados no funil: %d. Com valor de proposta registrado: %d. A diferença está na seção 7 (ou é "
            "proposta só de êxito, que fica sem valor)." % (r["funil"]["fechados"], v["n_fechado"]))
        add("")
    if r["funil"]["propostas"] != v["n_total"]:
        add("Chegaram à proposta no funil: %d. Com valor registrado: %d." % (r["funil"]["propostas"], v["n_total"]))
        add("")
    if v["n_fechado"]:
        add("Valor médio das fechadas: %s (%d propostas)." % (dinheiro(v["fechado"] / v["n_fechado"]), v["n_fechado"]))
        add("")
    fech, perd = r["atualizados"]
    add("Movimento do período, de qualquer mês de entrada, pela data da última atualização (aproximado): "
        "%d fechados e %d perdidos." % (fech, perd))
    add("")

    add("## 5. Motivos de perda")
    add("")
    if r["perdidos"]:
        add("| Motivo | Contatos |")
        add("|---|---|")
        for k, qtd in sorted(r["motivos"].items(), key=lambda kv: (-kv[1], kv[0])):
            add("| %s | %d |" % (k, qtd))
    else:
        add("Nenhum contato do período perdido até agora.")
    add("")

    add("## 6. Pediram para parar")
    add("")
    if r["pararam"]:
        add("%s do período: %s. No registro inteiro: %d. Nenhum deles recebe retorno." % (
            "1 contato" if len(r["pararam"]) == 1 else "%d contatos" % len(r["pararam"]),
            ", ".join(r["pararam"]), r["pararam_total"]))
    else:
        add("Nenhum contato do período. No registro inteiro: %d." % r["pararam_total"])
    add("")

    secao_qualidade(r, add)
    return "\n".join(m)


def linhas_da_tabela(r, chave, ant):
    return list(r[chave].keys()) + [k for k in sorted(r[ant]) if k not in r[chave]]


def secao_qualidade(r, add):
    add("## 7. Qualidade do registro")
    add("")
    if r["qualidade"]:
        add("| Problema | Linhas | Códigos |")
        add("|---|---|---|")
        for k, cods in r["qualidade"].items():
            mostra = ", ".join(cods[:8]) + (" e outros" if len(cods) > 8 else "")
            add("| %s | %d | %s |" % (k, len(cods), mostra))
    else:
        add("Nenhum problema encontrado nas colunas conferidas.")
    add("")


# ---------------------------------------------------------------- saída em html (uso interno)

CSS = """
:root{--bg:#f7f6f2;--card:#ffffff;--tx:#1f2328;--mu:#5b6270;--li:#d9dce1;--ac:#2f5d8a;--ac2:#9db8d3;--al:#a2462e}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16181c;--card:#1f2228;--tx:#e8e9ec;--mu:#a3a9b4;--li:#363a42;--ac:#7fa8d1;--ac2:#3b5875;--al:#e0866e}}
:root[data-theme="dark"]{--bg:#16181c;--card:#1f2228;--tx:#e8e9ec;--mu:#a3a9b4;--li:#363a42;--ac:#7fa8d1;--ac2:#3b5875;--al:#e0866e}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px 48px}h1{font-size:1.5rem;margin:0 0 4px}h2{font-size:1.1rem;margin:28px 0 10px}
.aviso{border-left:4px solid var(--al);background:var(--card);padding:10px 14px;margin:12px 0;color:var(--tx)}
.sub{color:var(--mu);margin:0 0 16px}.grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.cartao{background:var(--card);border:1px solid var(--li);border-radius:8px;padding:12px}.cartao b{display:block;font-size:1.4rem}
.cartao span{color:var(--mu);font-size:.85rem}table{width:100%;border-collapse:collapse;background:var(--card);font-size:.9rem}
th,td{border-bottom:1px solid var(--li);padding:6px 8px;text-align:left;vertical-align:top}th{color:var(--mu);font-weight:600}
.tab{overflow-x:auto}.barra{background:var(--ac2);height:10px;border-radius:5px}.barra i{display:block;height:10px;border-radius:5px;background:var(--ac)}
ul{padding-left:20px}li{margin:4px 0}
"""


def h(t):
    return html.escape(str(t))


def tabela_html(cabecalho, linhas):
    out = ['<div class="tab"><table><thead><tr>']
    out += ["<th>%s</th>" % h(c) for c in cabecalho]
    out.append("</tr></thead><tbody>")
    for l in linhas:
        out.append("<tr>" + "".join("<td>%s</td>" % c for c in l) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def barra(x, de):
    p = 0 if de <= 0 else min(100, round(100.0 * x / de))
    return '<div class="barra" title="%d de %d"><i style="width:%d%%"></i></div>' % (x, de, p)


def pagina_html(r):
    f = r["funil"]
    v = r["valores"]
    t = r["tempos"]
    p = ['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         "<title>Painel do funil %s</title><style>%s</style></head><body><main>" % (h(r["mes"]), CSS)]
    p.append("<h1>Painel do funil · %s%s</h1>" % (h(r["mes"]), " · TREINO" if r["treino"] else ""))
    p.append('<p class="sub">%d contatos no período · anterior (%s): %d · %d linhas no registro</p>'
             % (r["n"], h(r["mes_anterior"]), r["n_anterior"], r["total_registro"]))
    p.append('<div class="aviso">Uso interno do escritório. Não compartilhe este link e não envie a clientes. '
             'Contatos aparecem só pelo código.</div>')
    p.append('<div class="grade">')
    cartoes = [("Entraram", r["n"]), ("Chegaram à proposta", f["propostas"]), ("Fechados", f["fechados"]),
               ("Em andamento", f["em_andamento"])]
    if t is not None:
        cartoes.append(("Sem resposta agora", len(t["sem_resposta"])))
        if "dentro" in t:
            cartoes.append(("No prazo da ficha", "%d de %d" % (t["dentro"], t["com_dado"])))
    for rot, val in cartoes:
        p.append('<div class="cartao"><b>%s</b><span>%s</span></div>' % (h(val), h(rot)))
    p.append("</div>")
    if r["cuidados"]:
        p.append("<h2>Cuidados antes de ler</h2><ul>" + "".join("<li>%s</li>" % h(c) for c in r["cuidados"]) + "</ul>")
    if r["n"]:
        p.append("<h2>Funil</h2>")
        p.append(tabela_html(["Passagem", "Chegaram", "De", "Taxa", "", "Anterior"],
                             [[h(n), x, de, h(taxa(x, de)), barra(x, de), "%d de %d" % (xa, dea)]
                              for (n, x, de), (_, xa, dea) in zip(f["passagens"], r["funil_anterior"]["passagens"])]))
        for titulo, chave, ant in (("Entradas por origem", "origem", "origem_ant"),
                                   ("Entradas por área", "area", "area_ant"),
                                   ("Entradas por canal", "canal", "canal_ant")):
            linhas = []
            for k in linhas_da_tabela(r, chave, ant):
                d = r[chave].get(k, {"entraram": 0, "propostas": 0, "fecharam": 0, "valor_fechado": 0.0})
                linhas.append([h(k), d["entraram"], r[ant].get(k, 0), d["propostas"], d["fecharam"],
                               h(dinheiro(d["valor_fechado"]) if d["valor_fechado"] else "0")])
            p.append("<h2>%s</h2>" % titulo)
            p.append(tabela_html(["", "Entraram", "Anterior", "Propostas", "Fecharam", "Valor fechado"], linhas))
        p.append("<h2>Primeira resposta</h2>")
        if t is None:
            p.append("<p>Sem a coluna primeira_resposta no registro.</p>")
        else:
            if t["com_dado"]:
                p.append("<p>Mediana de %s úteis; maior espera de %s úteis; medido em %d de %d contatos.</p>"
                         % (h(horas(t["mediana_uteis"])), h(horas(t["maior_uteis"])), t["com_dado"], r["n"]))
                if t.get("fora_do_prazo"):
                    p.append("<p>Fora do prazo: %s.</p>" % h(", ".join("%s (%s)" % (c, horas(x)) for c, x in t["fora_do_prazo"])))
            if t["sem_resposta"]:
                p.append("<p><b>Sem resposta agora:</b> %s.</p>" % h(", ".join(
                    "%s (%s úteis%s)" % (c, horas(x), ", alta" if u == "alta" else "") for c, x, u in t["sem_resposta"])))
            if t.get("com_pessoa"):
                p.append("<p><b>Com uma pessoa, sem retorno registrado:</b> %s.</p>" % h(", ".join(t["com_pessoa"])))
        p.append("<h2>Propostas</h2>")
        p.append(tabela_html(["Item", "Quantidade", "Valor somado"], [
            ["Enviadas", v["n_total"], h(dinheiro(v["total"]))], ["Fechadas", v["n_fechado"], h(dinheiro(v["fechado"]))],
            ["Em aberto", v["n_aberto"], h(dinheiro(v["aberto"]))], ["Perdidas", v["n_perdido"], h(dinheiro(v["perdido"]))]]))
        if r["perdidos"]:
            p.append("<h2>Motivos de perda</h2>")
            p.append(tabela_html(["Motivo", "Contatos"], [[h(k), q] for k, q in
                                                          sorted(r["motivos"].items(), key=lambda kv: (-kv[1], kv[0]))]))
        p.append("<h2>Pediram para parar</h2><p>%s</p>" % h(
            ("Do período: %s. " % ", ".join(r["pararam"]) if r["pararam"] else "Nenhum do período. ")
            + "No registro inteiro: %d." % r["pararam_total"]))
    p.append("<h2>Qualidade do registro</h2>")
    if r["qualidade"]:
        p.append(tabela_html(["Problema", "Linhas", "Códigos"],
                             [[h(k), len(c), h(", ".join(c[:8]) + (" e outros" if len(c) > 8 else ""))]
                              for k, c in r["qualidade"].items()]))
    else:
        p.append("<p>Nenhum problema encontrado nas colunas conferidas.</p>")
    p.append('<p class="sub">As leituras e as ações do mês ficam no arquivo AAAA-MM.md do painel, escritas com o advogado.</p>')
    p.append("</main></body></html>")
    return "\n".join(p)


# ---------------------------------------------------------------- csv e xlsx resumidos

def linhas_resumo(r):
    out = [("secao", "item", "valor", "anterior", "observacao")]
    out.append(("geral", "contatos no periodo", r["n"], r["n_anterior"],
                "periodo %s; anterior %s%s" % (r["mes"], r["mes_anterior"], "; TREINO" if r["treino"] else "")))
    for chave, ant, rot in (("origem", "origem_ant", "origem"), ("area", "area_ant", "area"), ("canal", "canal_ant", "canal")):
        for k in linhas_da_tabela(r, chave, ant):
            d = r[chave].get(k, {"entraram": 0, "fecharam": 0})
            out.append(("entradas por " + rot, k, d["entraram"], r[ant].get(k, 0), "fecharam: %d" % d["fecharam"]))
    for (nome, x, de), (_, xa, dea) in zip(r["funil"]["passagens"], r["funil_anterior"]["passagens"]):
        out.append(("funil", nome, "%d de %d" % (x, de), "%d de %d" % (xa, dea), taxa(x, de)))
    for e in ETAPAS:
        if r["funil"]["etapas"].get(e):
            out.append(("etapa atual", e, r["funil"]["etapas"][e], "", ""))
    t = r["tempos"]
    if t and t["com_dado"]:
        out.append(("primeira resposta", "mediana horas uteis", round(t["mediana_uteis"], 2), "", "%d medidos" % t["com_dado"]))
        out.append(("primeira resposta", "maior espera horas uteis", round(t["maior_uteis"], 2), "", ""))
        if "dentro" in t:
            out.append(("primeira resposta", "dentro do prazo", "%d de %d" % (t["dentro"], t["com_dado"]), "", ""))
    if t:
        out.append(("primeira resposta", "sem resposta agora", len(t["sem_resposta"]), "",
                    " ".join(c for c, _, _ in t["sem_resposta"])))
        out.append(("primeira resposta", "com uma pessoa sem retorno registrado", len(t.get("com_pessoa", [])), "",
                    " ".join(t.get("com_pessoa", []))))
    else:
        out.append(("primeira resposta", "sem dado", "", "", "coluna primeira_resposta ausente"))
    v = r["valores"]
    for rot, n, s in (("enviadas", "n_total", "total"), ("fechadas", "n_fechado", "fechado"),
                      ("em aberto", "n_aberto", "aberto"), ("perdidas", "n_perdido", "perdido")):
        out.append(("propostas", rot, v[n], "", "valor %.2f" % v[s]))
    for k, qtd in sorted(r["motivos"].items(), key=lambda kv: (-kv[1], kv[0])):
        out.append(("motivo de perda", k, qtd, "", ""))
    out.append(("pediram para parar", "contatos do periodo", len(r["pararam"]), "", "registro inteiro: %d" % r["pararam_total"]))
    for k, cods in r["qualidade"].items():
        out.append(("qualidade do registro", k, len(cods), "", " ".join(cods[:20])))
    for c in r["cuidados"]:
        out.append(("cuidado", "", "", "", c))
    return out


def gravar_csv(linhas, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for l in linhas:
            w.writerow(l)


def gravar_xlsx(linhas, caminho):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError:
        return False
    wb = Workbook()
    ws = wb.active
    ws.title = "painel"
    for l in linhas:
        ws.append(list(l))
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, larg in zip("ABCDE", (24, 40, 14, 14, 60)):
        ws.column_dimensions[col].width = larg
    wb.save(caminho)
    return True


# ---------------------------------------------------------------- principal

def main(argv=None):
    p = argparse.ArgumentParser(description="Painel do mês a partir do contatos.csv do motor-comercial.")
    p.add_argument("csv", help="caminho do contatos.csv")
    p.add_argument("mes", help="AAAA-MM, ou AAAA-MM:AAAA-MM para um período")
    p.add_argument("--saida")
    p.add_argument("--md")
    p.add_argument("--html")
    p.add_argument("--xlsx", action="store_true")
    p.add_argument("--prazo-horas")
    p.add_argument("--horario", default="09:00-18:00")
    p.add_argument("--dias", default="seg-sex")
    p.add_argument("--origens", default="")
    p.add_argument("--areas", default="")
    p.add_argument("--hoje")
    p.add_argument("--treino", action="store_true")
    a = p.parse_args(argv)

    try:
        meses = meses_do_periodo(a.mes)
    except ValueError:
        falhar("período inválido: use AAAA-MM (2026-03) ou AAAA-MM:AAAA-MM (2026-01:2026-03).")
    if not os.path.isfile(a.csv):
        falhar("não encontrei o arquivo %s. O registro fica em escritorio/07-operacao/comercial/contatos.csv; "
               "nenhum número foi calculado." % a.csv)
    caminho_abs = os.path.abspath(a.csv)
    eh_treino = "_treino" in caminho_abs.replace("\\", "/").split("/")
    if eh_treino and not a.treino:
        falhar("este registro está na pasta _treino (casos fictícios). O painel do escritório nunca conta treino. "
               "Para testar com ele, rode de novo com --treino.")
    try:
        hoje = datetime.strptime(a.hoje, "%Y-%m-%d").date() if a.hoje else date.today()
    except ValueError:
        falhar("data inválida em --hoje: use AAAA-MM-DD.")

    colunas, linhas, _ = ler_csv(a.csv)
    faltando = [c for c in OBRIGATORIAS if c not in colunas]
    if faltando:
        falhar("o csv não tem as colunas obrigatórias %s. Confira a primeira linha com docs/funil.md; "
               "nenhum número foi calculado." % ", ".join(faltando))
    if not linhas:
        falhar("o registro %s tem só o cabeçalho, sem nenhum contato. Nada a contar ainda: o funil aparece "
               "depois das primeiras triagens." % a.csv)

    uteis, sabado = ler_horario(a.horario)
    dias = ler_dias(a.dias)
    horario = turnos_por_dia(uteis, sabado, dias)
    horario_txt = fmt_turnos(uteis) + (", sábado %s" % fmt_turnos(sabado) if sabado else "")
    if horario_txt != a.horario.strip():
        horario_txt += " (lido de \"%s\")" % a.horario.strip()
    prazo = ler_prazo(a.prazo_horas) if a.prazo_horas is not None else None
    prazo_vazio = (a.prazo_horas.strip() or "vazio") if a.prazo_horas is not None and prazo is None else ""
    if a.hoje:
        fim_do_dia = max(t[1] for t in horario.get(hoje.weekday(), uteis))
        agora = datetime.combine(hoje, fim_do_dia)
    else:
        agora = datetime.now()
    opcoes = {
        "horario": horario,
        "horario_txt": horario_txt,
        "dias": dias,
        "prazo": prazo,
        "prazo_vazio": prazo_vazio,
        "origens": {norm(o) for o in a.origens.split(",") if o.strip()},
        "areas": {norm(o) for o in a.areas.split(",") if o.strip()},
        "hoje": hoje,
        "agora": agora,
        "treino": eh_treino,
    }
    r = calcular(colunas, linhas, meses, opcoes)
    texto = markdown(r)
    print(texto)

    rotulo = meses[0] if len(meses) == 1 else "%s-a-%s" % (meses[0], meses[-1])
    saida = a.saida or os.path.join(os.path.dirname(caminho_abs), "painel")
    os.makedirs(saida, exist_ok=True)
    resumo = linhas_resumo(r)
    cam_csv = os.path.join(saida, "%s-numeros.csv" % rotulo)
    gravar_csv(resumo, cam_csv)
    avisos = ["csv resumido: %s" % cam_csv]
    if a.md:
        with open(a.md, "w", encoding="utf-8") as fmd:
            fmd.write(texto + "\n")
        avisos.append("markdown: %s" % a.md)
    if a.html:
        with open(a.html, "w", encoding="utf-8") as fh:
            fh.write(pagina_html(r) + "\n")
        avisos.append("html (uso interno, não compartilhar): %s" % a.html)
    if a.xlsx:
        cam_x = os.path.join(saida, "%s-numeros.xlsx" % rotulo)
        if gravar_xlsx(resumo, cam_x):
            avisos.append("planilha: %s" % cam_x)
        else:
            avisos.append("openpyxl não está instalado: ficou só o .csv, que abre em qualquer planilha")
    sys.stderr.write("\n".join(avisos) + "\n")


if __name__ == "__main__":
    main()
