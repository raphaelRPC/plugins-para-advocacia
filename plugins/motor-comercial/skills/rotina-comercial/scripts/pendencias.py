#!/usr/bin/env python3
"""Pendências comerciais a partir do contatos.csv (motor-comercial).

Lê o registro do funil (formato em docs/funil.md do plugin) e imprime, em markdown,
o resumo do dia, na ordem que o agente-comercial usa:

  PESSOA AGORA (inclui rascunhos parados na fila há mais de um dia útil)
  1. sem resposta além do prazo (primeira_resposta vazia antes de consulta-agendada,
     em horas úteis desde a entrada)
  2. consultas de hoje, as do próximo dia útil (lembrete) e as que passaram
  3. retornos da régua (dias corridos) e outros próximos passos de hoje ou vencidos
  4. propostas paradas
  5. quem pediu para parar
  6. registro a corrigir
  desde a última rodada (entradas e triagens de todos os dias, inclusive fim de semana)
  por responsável; semana anterior (às segundas)

Só biblioteca padrão (Python 3.9+). Não altera nada. Mostra só código, nome curto,
área, assunto e responsável.

Uso:
  python3 pendencias.py CAMINHO/contatos.csv [AAAA-MM-DD] [opções]

Opções:
  --data AAAA-MM-DD          dia do resumo (padrão: hoje)
  --hora HH:MM               hora da leitura (padrão: agora, se o dia é hoje; senão o início do expediente)
  --expediente TEXTO         horario_de_atendimento da ficha, como está escrito ou em HH:MM-HH:MM
                             (padrão 09:00-18:00). Exemplos aceitos: "dias úteis, das 9h às 18h",
                             "9h-18h", "8h30 às 12h e 14h às 18h", "09:00-12:00,14:00-18:00",
                             "dias úteis das 9h às 18h; sábado das 9h às 12h"
  --sabado                   conta o sábado como dia de atendimento, com o mesmo horário
  --feriados TEXTO           dias sem expediente: datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM (ano do
                             resumo), separadas por vírgula, ponto e vírgula ou espaço; pode ser o
                             campo feriados_e_recessos da ficha copiado como está. Vazio ou só
                             [A PREENCHER]: ignorado, com aviso no resumo
  --prazo-novo TEXTO         primeira_resposta_contato_novo, em horas úteis (padrão 2). Aceita o
                             número (2, 1.5, 1,5) ou o texto da ficha ("até 2 horas úteis", "1h30",
                             "30 minutos")
  --alertas TEXTO            palavras_de_alerta de prioridade máxima da ficha, separadas por ponto
                             e vírgula, vírgula ou "·". Somam-se aos sinais fixos do script.
                             Marcações ([A PREENCHER], [A DEFINIR], [A CONFIRMAR], [CONFERIR]) nunca
                             viram palavra de alerta; campo vazio ou só marcação: aviso no resumo
  --dias-proposta DIAS       dias corridos sem atualização para a proposta contar como parada (padrão 3)
  --desde "AAAA-MM-DD HH:MM" início da leitura (vale mais que o registro de uso)
  --registro-de-uso ARQUIVO  registro de uso do ciclo; a leitura começa na última rodada registrada
  --triagens PASTA           pasta das triagens diárias
  --fila PASTA               pasta da fila de aprovação
  --semana / --sem-semana    força ou tira o resumo da semana anterior (padrão: só às segundas)
  --treino                   permite ler o registro de treino (pasta _treino)

Marcador de pessoa (docs/funil.md, regra 4) e fora da régua (regra 5): contato com
proximo_passo começando por "pessoa agora:" ou "pessoa liga:", ou com sinal de alerta no
assunto, nunca entra nos retornos da régua.

Sai com código 1 e uma mensagem clara quando falta o arquivo, quando ele está vazio,
quando falta uma coluna obrigatória ou quando o expediente ou o prazo da ficha não dá
para ler como horas.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import Counter
from datetime import date, datetime, time, timedelta
from pathlib import Path

OBRIGATORIAS = [
    "codigo", "entrada", "etapa", "urgencia", "responsavel", "proximo_passo",
    "data_proximo_passo", "primeira_resposta", "pediu_para_parar", "atualizado_em",
]
OPCIONAIS = [
    "canal", "origem", "nome_curto", "tipo", "area", "assunto", "valor_proposta",
    "motivo_perda", "perdido_na_etapa",
]
ETAPAS = [
    "novo", "triado", "consulta-agendada", "nao-compareceu", "consulta-feita",
    "proposta-enviada", "negociando", "fechado", "encaminhado", "recusado",
    "sem-caso", "perdido",
]
ENCERRADAS = {"encaminhado", "recusado", "sem-caso", "perdido"}
ANTES_DA_CONSULTA = {"novo", "triado"}
ORDEM_URGENCIA = {"alta": 0, "normal": 1, "baixa": 2}
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
SEM_PROXIMO = {"", "nenhum", "nenhuma", "-", "n/a"}
SIM = {"sim", "s", "yes", "y", "x", "true", "1"}
NAO = {"nao", "n", "no", "false", "0", ""}

# Sinais de parada imediata ou caso sensível no assunto (triar-contato, seção 4.1). Comparados
# sem acento e sem maiúscula, como palavra inteira ou começo de palavra.
SINAIS_FIXOS = [
    r"violenci\w*", r"ameac\w*", r"agress\w*", r"agrediu", r"medida protetiva", r"preso", r"presa",
    r"pris(ao|oes)", r"flagrante", r"custodia", r"suicid\w*", r"abuso\w*", r"estupro",
    r"sumir com", r"risco de vida", r"risco a vida", r"parada imediata", r"pessoa agora", r"pessoa liga",
]


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto or "") if not unicodedata.combining(c))


def norm(valor):
    """Valor de opção comparável: minúsculas, sem acento, sem espaço nas pontas."""
    return sem_acento((valor or "").strip()).lower()


# ---------------------------------------------------------------- leitura do csv

def decodificar(bruto):
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_csv(caminho):
    p = Path(caminho)
    if not p.exists():
        falhar(f"não encontrei o registro em `{caminho}`. Confira o caminho (o padrão é "
               "escritorio/07-operacao/comercial/contatos.csv). Se o funil ainda não existe, "
               "rode a triar-contato primeiro. Nada foi lido, então não há resumo.")
    if p.is_dir():
        falhar(f"`{caminho}` é uma pasta. Passe o arquivo contatos.csv.")
    texto = decodificar(p.read_bytes())
    linhas_texto = texto.splitlines()
    if linhas_texto and linhas_texto[0].strip().lower().startswith("sep="):
        linhas_texto = linhas_texto[1:]
    texto = "\n".join(linhas_texto)
    if not texto.strip():
        falhar(f"o arquivo `{caminho}` está vazio, sem nem a primeira linha. Copie a primeira "
               "linha de docs/funil.md do plugin. Nada foi lido, então não há resumo.")
    primeira = linhas_texto[0]
    separador = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO(texto), delimiter=separador)
    cabecalho = [norm(c).replace(" ", "_") for c in next(leitor)]
    faltando = [c for c in OBRIGATORIAS if c not in cabecalho]
    if faltando:
        falhar("faltam colunas obrigatórias no registro: " + ", ".join(faltando)
               + f". Colunas encontradas: {', '.join(c for c in cabecalho if c) or 'nenhuma'}. "
               "Copie a primeira linha de docs/funil.md do plugin e confira se a planilha "
               "foi salva como CSV.")
    linhas = []
    for n, valores in enumerate(leitor, start=2):
        if not any((v or "").strip() for v in valores):
            continue
        linha = {}
        for i, nome in enumerate(cabecalho):
            if nome:
                linha[nome] = (valores[i] if i < len(valores) else "").strip()
        linha["_linha"] = n
        linhas.append(linha)
    ausentes = [c for c in OPCIONAIS if c not in cabecalho]
    return linhas, separador, ausentes


DATA_RE = re.compile(r"^\s*(\d{4})-(\d{1,2})-(\d{1,2})|^\s*(\d{1,2})/(\d{1,2})/(\d{2,4})")
HORA_RE = re.compile(r"(\d{1,2}):(\d{2})(?::\d{2})?")


def ler_data(valor):
    m = DATA_RE.match(valor or "")
    if not m:
        return None
    try:
        if m.group(1):
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        ano = int(m.group(6))
        ano += 2000 if ano < 100 else 0
        return date(ano, int(m.group(5)), int(m.group(4)))
    except ValueError:
        return None


def ler_data_hora(valor):
    d = ler_data(valor)
    if not d:
        return None
    resto = DATA_RE.sub("", valor or "", count=1)
    h = HORA_RE.search(resto)
    if h:
        try:
            return datetime.combine(d, time(int(h.group(1)), int(h.group(2))))
        except ValueError:
            return None
    return datetime.combine(d, time(0, 0))


def ler_hora(valor):
    m = HORA_RE.fullmatch((valor or "").strip())
    if not m:
        falhar(f"hora inválida: `{valor}`. Use HH:MM.")
    return time(int(m.group(1)), int(m.group(2)))


def numero(valor):
    valor = (valor or "").replace("R$", "").replace(" ", "")
    if not valor:
        return None
    if "," in valor and "." in valor:
        valor = valor.replace(".", "").replace(",", ".")
    elif "," in valor:
        valor = valor.replace(",", ".")
    try:
        return float(valor)
    except ValueError:
        return None


# ---------------------------------------------------------------- horas úteis

class Expediente:
    """Horas úteis com um ou mais turnos por dia (ex.: 8h30 às 12h e 14h às 18h)."""

    def __init__(self, turnos, sabado, feriados, turnos_sabado=None):
        self.turnos = turnos
        self.turnos_sabado = turnos_sabado or (turnos if sabado else [])
        self.feriados = feriados
        self.inicio = turnos[0][0]

    def turnos_do_dia(self, d):
        if d in self.feriados:
            return []
        if d.weekday() < 5:
            return self.turnos
        if d.weekday() == 5:
            return self.turnos_sabado
        return []

    def dia_util(self, d):
        return bool(self.turnos_do_dia(d))

    def horas_entre(self, de, ate):
        if ate <= de:
            return 0.0
        total, d = 0.0, de.date()
        while d <= ate.date():
            for t_ini, t_fim in self.turnos_do_dia(d):
                ini = max(de, datetime.combine(d, t_ini))
                fim = min(ate, datetime.combine(d, t_fim))
                if fim > ini:
                    total += (fim - ini).total_seconds() / 3600
            d += timedelta(days=1)
        return total

    def somar_horas(self, de, horas):
        restante, atual = horas * 3600, de
        for _ in range(400):
            d = atual.date()
            for t_ini, t_fim in self.turnos_do_dia(d):
                ini = max(atual, datetime.combine(d, t_ini))
                fecha = datetime.combine(d, t_fim)
                if ini < fecha:
                    disp = (fecha - ini).total_seconds()
                    if disp >= restante:
                        return ini + timedelta(seconds=restante)
                    restante -= disp
            atual = datetime.combine(d + timedelta(days=1), time(0, 0))
        return atual

    def proximo_dia_util(self, d):
        d += timedelta(days=1)
        for _ in range(15):
            if self.dia_util(d):
                return d
            d += timedelta(days=1)
        return d

    def dias_uteis_entre(self, de, ate):
        n, d = 0, de
        while d < ate:
            d += timedelta(days=1)
            if self.dia_util(d):
                n += 1
        return n


# ---------------------------------------------------------------- valores da ficha

HORARIO_RE = re.compile(r"(\d{1,2})\s*(?:(?:h|:)\s*(\d{2})?|horas?\b)", re.I)


def horarios_do_texto(trecho):
    """'das 8h30 às 12h e das 14h às 18h' -> [(08:30, 12:00), (14:00, 18:00)]."""
    pontos = []
    for m in HORARIO_RE.finditer(trecho):
        h, mi = int(m.group(1)), int(m.group(2) or 0)
        if h > 24 or mi > 59:
            continue
        pontos.append(time(23, 59) if h == 24 else time(h, mi))
    if not pontos:
        for m in re.finditer(r"\b(\d{1,2})\s*(?:a|as|ate|-)\s*(\d{1,2})\b", trecho):
            if int(m.group(1)) < int(m.group(2)) <= 24:
                pontos += [time(int(m.group(1)), 0), time(23, 59) if m.group(2) == "24" else time(int(m.group(2)), 0)]
    turnos = []
    for i in range(0, len(pontos) - 1, 2):
        if pontos[i + 1] > pontos[i]:
            turnos.append((pontos[i], pontos[i + 1]))
    return turnos


def ler_expediente(texto, sabado_forcado):
    """horario_de_atendimento da ficha -> (turnos dos dias úteis, turnos do sábado)."""
    bruto = (texto or "").strip()
    if not bruto or "a preencher" in norm(bruto):
        falhar("o horário de atendimento está vazio ou `[A PREENCHER]` na ficha. Passe em --expediente "
               "o texto do campo horario_de_atendimento (ex.: \"dias úteis, das 9h às 18h\") ou "
               "HH:MM-HH:MM. Nada foi lido, então não há resumo.")
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
        falhar(f"não consegui ler horas em --expediente `{texto}`. Use o horário com horas, como "
               "\"dias úteis, das 9h às 18h\", \"8h30 às 12h e 14h às 18h\" ou 09:00-18:00. "
               "Nada foi lido, então não há resumo.")
    if sabado_forcado and not sabado:
        sabado = list(uteis)
    return uteis, sabado


def ler_prazo(texto):
    """primeira_resposta_contato_novo da ficha -> horas úteis (float)."""
    bruto = (texto or "").strip()
    n = norm(bruto).replace(",", ".")
    if not n or "a preencher" in n:
        falhar("o prazo de primeira resposta está vazio ou `[A PREENCHER]`. Passe em --prazo-novo as "
               "horas úteis do campo primeira_resposta_contato_novo (ex.: 2 ou \"até 2 horas úteis\").")
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
    falhar(f"não consegui ler --prazo-novo `{texto}` como horas úteis. Converta antes de rodar: "
           "\"no mesmo dia\" ou \"em 1 dia útil\" viram um número de horas úteis que o escritório "
           "decide (pergunte: \"Em horas úteis, quanto é isso para vocês?\").")


# Marcações das fichas: nunca viram feriado nem palavra de alerta.
MARCACAO_RE = re.compile(r"\[\s*(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]", re.I)
COLCHETE_MAIUSCULO_RE = re.compile(r"\[[A-ZÀ-Ý][A-ZÀ-Ý0-9 ]+[^\]]*\]")


def limpar_campo(texto):
    """Tira as marcações do texto copiado da ficha. Devolve (texto limpo, se havia marcação)."""
    bruto = texto or ""
    limpo = COLCHETE_MAIUSCULO_RE.sub(" ", MARCACAO_RE.sub(" ", bruto))
    return limpo, limpo != bruto


def campo_vazio(texto):
    return not re.sub(r"[\s;,.·\-]", "", texto or "")


def ler_feriados(texto, ano):
    """Datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM (no ano do resumo) em qualquer texto."""
    datas = set()
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", texto or ""):
        try:
            if m.group(1):
                datas.add(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            else:
                a = int(m.group(6)) if m.group(6) else ano
                a += 2000 if a < 100 else 0
                datas.add(date(a, int(m.group(5)), int(m.group(4))))
        except ValueError:
            falhar(f"feriado inválido em --feriados: `{m.group(0)}`. Use AAAA-MM-DD ou DD/MM/AAAA.")
    data_txt = r"\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}(?:/\d{2,4})?"
    for m in re.finditer(r"(%s)\s*(?:a|ate|até|-)\s*(%s)" % (data_txt, data_txt), texto or ""):
        d_ini, d_fim = min(ler_feriados(m.group(1), ano)), min(ler_feriados(m.group(2), ano))
        if d_fim < d_ini and "/" in m.group(2) and m.group(2).count("/") == 1:
            datas.discard(d_fim)
            d_fim = d_fim.replace(year=d_fim.year + 1)
        if 0 < (d_fim - d_ini).days <= 60:
            d = d_ini
            while d <= d_fim:
                datas.add(d)
                d += timedelta(days=1)
    sobra = re.sub(r"\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}(/\d{2,4})?", "", texto or "")
    if datas == set() and re.search(r"\d", sobra):
        falhar(f"não achei datas em --feriados `{texto}`. Use AAAA-MM-DD ou DD/MM/AAAA, separadas por vírgula.")
    return datas


def fmt_turnos(turnos):
    return " e ".join(f"{a:%H:%M}-{b:%H:%M}" for a, b in turnos)


# ---------------------------------------------------------------- formatos

def fmt_horas(h):
    if h < 1:
        return f"{int(round(h * 60))} min"
    inteiro, minutos = int(h), int(round((h - int(h)) * 60))
    if minutos == 60:
        inteiro, minutos = inteiro + 1, 0
    return f"{inteiro}h{minutos:02d}" if minutos else f"{inteiro}h"


def fmt_momento(m, hoje):
    if m.date() == hoje:
        return f"hoje às {m:%H:%M}"
    return f"{DIAS[m.weekday()]} {m:%d/%m} às {m:%H:%M}"


def fmt_valor(v):
    if v is None:
        return "sem valor"
    t = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return t[:-3] if t.endswith(",00") else t


def contar(n, sing, plur):
    return f"{n} {sing if n == 1 else plur}"


def quem(l):
    return f"{l.get('codigo') or '(sem código)'} · {l.get('nome_curto') or 'sem nome'}"


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for l in linhas:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in l) + " |")
    return out


def etapa(l):
    return norm(l.get("etapa"))


def urg(l):
    return ORDEM_URGENCIA.get(norm(l.get("urgencia")), 1)


def parou(l):
    return norm(l.get("pediu_para_parar")) in SIM


def passo(l):
    return norm(l.get("proximo_passo"))


RE_ALERTA = re.compile(r"\b(" + "|".join(SINAIS_FIXOS) + r")\b")


def montar_alertas(texto):
    """Acrescenta as palavras de alerta da ficha (--alertas) aos sinais fixos."""
    global RE_ALERTA
    extras = [re.escape(norm(x)) for x in re.split(r"[;,·\n]", texto or "") if norm(x)]
    extras = [x for x in extras if "a preencher" not in x and "a definir" not in x]
    if extras:
        RE_ALERTA = re.compile(r"\b(" + "|".join(SINAIS_FIXOS + extras) + r")")
    return len(extras)


def sinal_no_assunto(l):
    m = RE_ALERTA.search(norm(l.get("assunto")))
    return m.group(0) if m else None


def para_pessoa(l):
    """Motivo de o contato ir para uma pessoa (funil.md, regra 4, marcador de pessoa;
    regra 5, fora da régua)."""
    if etapa(l) in ENCERRADAS:
        return None
    p = passo(l)
    marcador = None
    if p.startswith("pessoa agora"):
        marcador = "pessoa agora"
    elif p.startswith("pessoa liga"):
        marcador = "pessoa liga (vulnerabilidade)"
    if marcador:
        if l.get("primeira_resposta"):
            marcador += (f"; já houve contato em {l.get('primeira_resposta')}: trocar o marcador "
                         "pelo combinado, com data")
        return marcador
    if p.startswith("retorno") and not parou(l):
        sinal = sinal_no_assunto(l)
        if sinal:
            return (f"sinal de alerta no assunto (\"{sinal}\") com retorno da régua marcado: "
                    "a régua não vale; uma pessoa decide e troca o próximo passo")
    if norm(l.get("urgencia")) == "alta" and not (l.get("responsavel") or "").strip() and not parou(l):
        return "urgência alta sem responsável"
    return None


def fora_da_regua(l):
    if parou(l):
        return "pediu para parar"
    if norm(l.get("area")) == "fora-da-area":
        return "fora da área"
    if sinal_no_assunto(l):
        return "sinal de alerta no assunto"
    return para_pessoa(l)


# ---------------------------------------------------------------- registro de uso e fila

def ultima_rodada(caminho, agora):
    p = Path(caminho)
    if not p.exists():
        return None, f"registro de uso não encontrado em `{caminho}`"
    melhor = None
    for linha in decodificar(p.read_bytes()).splitlines():
        if not linha.strip().startswith("|"):
            continue
        if "nao rodou" in norm(linha) or "so o resumo" in norm(linha):
            continue  # dia sem ciclo, ou só o resumo: a leitura continua da última rodada completa
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        for i, c in enumerate(celulas):
            d = ler_data(c)
            if d and DATA_RE.match(c) and len(c) <= 16:
                h = HORA_RE.search(c[10:]) or (HORA_RE.fullmatch(celulas[i + 1]) if i + 1 < len(celulas) else None)
                momento = datetime.combine(d, time(int(h.group(1)), int(h.group(2))) if h else time(0, 0))
                if momento <= agora and (melhor is None or momento > melhor):
                    melhor = momento
                break
    if melhor is None:
        return None, f"registro de uso em `{caminho}` sem nenhuma rodada"
    return melhor, "última rodada do registro de uso"


def ler_fila(pasta, hoje, exp, treino):
    p = Path(pasta)
    if not p.exists():
        return None
    pendentes, parados = [], []
    for arq in sorted(p.glob("*/*.md")):
        if "_treino" in arq.parts and not treino:
            continue
        d = ler_data(arq.parent.name)
        texto = decodificar(arq.read_bytes())
        m = re.search(r"^status:\s*([a-zA-Z]+)", texto, re.M)
        if not m or norm(m.group(1)) != "pendente":
            continue
        pendentes.append(arq)
        if d and exp.dias_uteis_entre(d, hoje) > 1:
            parados.append((arq, d))
    return pendentes, parados


# ---------------------------------------------------------------- resumo do dia

def resumo(linhas, hoje, agora, exp, args, criterios, desde, origem_desde, avisos):
    out = []
    abertas = [l for l in linhas if etapa(l) not in ENCERRADAS]

    # PESSOA AGORA
    pessoa = [(l, para_pessoa(l)) for l in abertas if para_pessoa(l)]
    pessoa.sort(key=lambda i: (urg(i[0]), ler_data(i[0].get("data_proximo_passo")) or hoje))
    em_pessoa = {id(l) for l, _ in pessoa}

    # 1. sem resposta
    estourados, no_prazo = [], []
    for l in abertas:
        if etapa(l) not in ANTES_DA_CONSULTA or l.get("primeira_resposta") or id(l) in em_pessoa:
            continue
        entrada = ler_data_hora(l.get("entrada"))
        if not entrada:
            continue
        passadas = exp.horas_entre(entrada, agora)
        limite = exp.somar_horas(entrada, args.prazo_novo)
        (estourados if passadas > args.prazo_novo else no_prazo).append((l, passadas, limite))
    estourados.sort(key=lambda i: (urg(i[0]), -i[1]))
    no_prazo.sort(key=lambda i: (urg(i[0]), i[2]))

    # 2. consultas
    proximo_util = exp.proximo_dia_util(hoje)
    c_hoje, c_lembrete, c_passadas = [], [], []
    for l in abertas:
        if etapa(l) != "consulta-agendada" or passo(l).startswith("remarcar"):
            continue
        d = ler_data(l.get("data_proximo_passo"))
        if d == hoje:
            c_hoje.append(l)
        elif d and hoje < d <= proximo_util:
            c_lembrete.append((l, d))
        elif d and d < hoje:
            c_passadas.append((l, (hoje - d).days))

    # 3. retornos da régua e outros próximos passos
    regua_hoje, regua_vencidos, outros = [], [], []
    for l in linhas:
        if etapa(l) in ENCERRADAS or id(l) in em_pessoa or parou(l):
            continue
        if etapa(l) == "consulta-agendada" and not passo(l).startswith("remarcar"):
            continue
        if passo(l) in SEM_PROXIMO:
            continue
        d = ler_data(l.get("data_proximo_passo"))
        if not d or d > hoje:
            continue
        atraso = (hoje - d).days
        if passo(l).startswith("retorno") and not fora_da_regua(l):
            (regua_hoje if atraso == 0 else regua_vencidos).append((l, atraso))
        else:
            outros.append((l, atraso))
    for lista in (regua_hoje, regua_vencidos, outros):
        lista.sort(key=lambda i: (urg(i[0]), -i[1]))

    # 4. propostas paradas
    paradas = []
    for l in linhas:
        if etapa(l) not in {"proposta-enviada", "negociando"}:
            continue
        d = ler_data(l.get("atualizado_em"))
        if d and (hoje - d).days >= args.dias_proposta:
            paradas.append((l, (hoje - d).days))
    paradas.sort(key=lambda i: -i[1])

    # 5. pediu para parar
    conflitos, recentes, total_parar = [], [], 0
    for l in linhas:
        if not parou(l):
            continue
        total_parar += 1
        problema = []
        if passo(l) not in SEM_PROXIMO:
            problema.append(f"próximo passo \"{l.get('proximo_passo')}\"")
        if l.get("data_proximo_passo"):
            problema.append(f"data {l.get('data_proximo_passo')}")
        if problema:
            conflitos.append((l, "; ".join(problema)))
        d = ler_data(l.get("atualizado_em"))
        if d and 0 <= (hoje - d).days <= 7:
            recentes.append(l)

    # 6. registro a corrigir
    correcoes = []
    for cod, n in Counter(l.get("codigo") for l in linhas if l.get("codigo")).items():
        if n > 1:
            correcoes.append(f"código {cod} aparece {n} vezes (uma linha por contato)")
    for l in linhas:
        ref = f"linha {l['_linha']} ({l.get('codigo') or 'sem código'})"
        e = etapa(l)
        if not l.get("codigo"):
            correcoes.append(f"{ref}: sem código")
        if e not in ETAPAS:
            correcoes.append(f"{ref}: etapa \"{l.get('etapa')}\" não é uma das etapas do funil")
        if "tipo" in l and norm(l.get("tipo")) not in {"novo", "antigo", ""}:
            if norm(l.get("tipo")) == "cliente":
                correcoes.append(f"{ref}: tipo cliente. Cliente ativo não entra no funil comercial; "
                                 "vai para a carteira da experiência do cliente")
            else:
                correcoes.append(f"{ref}: tipo \"{l.get('tipo')}\" (use novo ou antigo)")
        if norm(l.get("urgencia")) not in set(ORDEM_URGENCIA) | {""}:
            correcoes.append(f"{ref}: urgência \"{l.get('urgencia')}\" (use alta, normal ou baixa)")
        if norm(l.get("pediu_para_parar")) not in SIM | NAO:
            correcoes.append(f"{ref}: pediu_para_parar \"{l.get('pediu_para_parar')}\" (use sim ou nao)")
        for campo in ("entrada", "primeira_resposta"):
            if l.get(campo) and not ler_data_hora(l.get(campo)):
                correcoes.append(f"{ref}: {campo} \"{l.get(campo)}\" fora do formato AAAA-MM-DD HH:MM")
        for campo in ("data_proximo_passo", "atualizado_em"):
            if l.get(campo) and not ler_data(l.get(campo)):
                correcoes.append(f"{ref}: {campo} \"{l.get(campo)}\" fora do formato AAAA-MM-DD")
        if e == "triado" and passo(l) in SEM_PROXIMO and not parou(l):
            correcoes.append(f"{ref}: triado sem próximo passo (a régua não foi armada)")
        if e == "perdido" and not l.get("motivo_perda"):
            correcoes.append(f"{ref}: perdido sem motivo")
        if (e in ANTES_DA_CONSULTA and passo(l).startswith("retorno") and not l.get("primeira_resposta")
                and (ler_data(l.get("data_proximo_passo")) or hoje + timedelta(days=1)) <= hoje):
            correcoes.append(f"{ref}: retorno da régua vencendo e primeira_resposta vazia. "
                             "O convite saiu? Se saiu, preencher primeira_resposta")

    # desde a última rodada
    entraram = [l for l in linhas if (ler_data_hora(l.get("entrada")) or datetime.min) >= desde]
    triagens = []
    if args.triagens:
        pasta = Path(args.triagens)
        if "_treino" in pasta.parts and not args.treino:
            avisos.append("pasta de triagens de treino ignorada (use --treino)")
        elif pasta.exists():
            for arq in sorted(pasta.glob("*.md")):
                d = ler_data(arq.stem)
                if d and desde.date() <= d <= hoje:
                    triagens.append(d)
        else:
            avisos.append(f"pasta de triagens `{args.triagens}` não encontrada")
    fila = ler_fila(args.fila, hoje, exp, args.treino) if args.fila else None
    if args.fila and fila is None:
        avisos.append(f"pasta da fila `{args.fila}` não encontrada")

    # ---------------------------------------------------------- saída
    titulo = "Pendências comerciais" + (" · TREINO" if args.treino else "")
    out += [f"# {titulo} · {hoje:%Y-%m-%d} ({DIAS[hoje.weekday()]})", ""]
    out.append(f"Leitura de {agora:%d/%m/%Y} às {agora:%H:%M}. {len(linhas)} contatos no registro, "
               f"{len(abertas)} em aberto. Desde {desde:%d/%m/%Y %H:%M} ({origem_desde}).")
    out += ["", "**Critérios usados:** " + "; ".join(criterios) + ".", ""]
    if avisos:
        out += ["**Avisos:** " + "; ".join(avisos) + ".", ""]
    out.append("**Hoje, em uma linha:** "
               f"{contar(len(pessoa), 'contato', 'contatos')} para uma pessoa agora, "
               f"{contar(len(estourados), 'sem resposta', 'sem resposta')} além do prazo, "
               f"{contar(len(c_hoje), 'consulta', 'consultas')} hoje, "
               f"{contar(len(regua_hoje), 'retorno', 'retornos')} da régua hoje, "
               f"{contar(len(regua_vencidos) + len([o for o in outros if o[1] > 0]), 'item vencido', 'itens vencidos')}, "
               f"{contar(len(paradas), 'proposta parada', 'propostas paradas')}, "
               f"{contar(len(conflitos), 'conflito', 'conflitos')} de quem pediu para parar, "
               f"{contar(len(correcoes), 'correção', 'correções')} no registro.")
    out.append("")

    out += ["## PESSOA AGORA", ""]
    if pessoa:
        out += tabela(["Urgência", "Contato", "Área", "Assunto", "Por quê", "Responsável", "Desde"],
                      [[norm(l.get("urgencia")) or "?", quem(l), l.get("area") or "?", l.get("assunto") or "",
                        motivo, l.get("responsavel") or "SEM RESPONSÁVEL", l.get("entrada") or "?"]
                       for l, motivo in pessoa])
        out.append("")
        out.append("Nenhum destes recebe mensagem pronta nem entra na régua. Uma pessoa assume.")
    else:
        out.append("Nenhum contato marcado para uma pessoa agora no registro. Mensagens que ainda não "
                   "foram triadas não aparecem aqui: confira a pasta de entrada.")
    if fila:
        pend, parados = fila
        if parados:
            out += ["", f"Rascunhos parados na fila há mais de um dia útil ({len(parados)}):"]
            for arq, d in parados:
                out.append(f"- {arq.parent.name}/{arq.name}")
    out.append("")

    out += ["## 1. Sem resposta além do prazo", ""]
    if estourados:
        out += tabela(["Urgência", "Contato", "Tipo", "Área", "Assunto", "Entrada", "Horas úteis",
                       "Prazo", "Responsável"],
                      [[norm(l.get("urgencia")) or "?", quem(l), l.get("tipo") or "?", l.get("area") or "?",
                        l.get("assunto") or "", l.get("entrada"), fmt_horas(h), fmt_horas(args.prazo_novo),
                        l.get("responsavel") or "sem responsável"] for l, h, _ in estourados])
    else:
        out.append(f"Nenhum contato com `primeira_resposta` vazia passou de {fmt_horas(args.prazo_novo)} úteis.")
    if no_prazo:
        out += ["", "Ainda no prazo, responder até:"]
        for l, h, limite in no_prazo:
            out.append(f"- {quem(l)} ({norm(l.get('urgencia')) or '?'}, {l.get('area') or '?'}): "
                       f"{fmt_momento(limite, hoje)}")
    out.append("")

    out += ["## 2. Consultas", ""]
    if c_hoje:
        out.append("Hoje:")
        for l in c_hoje:
            out.append(f"- {quem(l)} · {l.get('area') or '?'} · {l.get('proximo_passo') or ''} · "
                       f"com {l.get('responsavel') or 'sem responsável'}")
    else:
        out.append("Nenhuma consulta com data de hoje no registro. Confira a agenda.")
    if c_lembrete:
        out += ["", f"Até o próximo dia útil ({proximo_util:%d/%m}), lembrete da véspera:"]
        for l, d in c_lembrete:
            out.append(f"- {quem(l)} · {DIAS[d.weekday()]} {d:%d/%m} · {l.get('proximo_passo') or ''}"
                       + (" · pediu para parar: uma pessoa decide o lembrete" if parou(l) else ""))
    if c_passadas:
        out += ["", "Data passada e etapa ainda `consulta-agendada` (aconteceu ou faltou?):"]
        for l, dias in c_passadas:
            out.append(f"- {quem(l)}: marcada para {l.get('data_proximo_passo')}, há {contar(dias, 'dia', 'dias')}. "
                       "Uma pessoa atualiza para `consulta-feita` ou `nao-compareceu`.")
    out.append("")

    out += ["## 3. Retornos e próximos passos", ""]
    if regua_hoje:
        out.append("Retornos da régua para hoje (dias corridos):")
        out += tabela(["Urgência", "Contato", "Etapa", "Próximo passo", "Responsável"],
                      [[norm(l.get("urgencia")) or "?", quem(l), etapa(l), l.get("proximo_passo"),
                        l.get("responsavel") or "sem responsável"] for l, _ in regua_hoje])
    else:
        out.append("Nenhum retorno da régua com data de hoje.")
    if regua_vencidos:
        out += ["", "Retornos da régua vencidos:"]
        out += tabela(["Urgência", "Contato", "Etapa", "Próximo passo", "Venceu em", "Atraso", "Responsável"],
                      [[norm(l.get("urgencia")) or "?", quem(l), etapa(l), l.get("proximo_passo"),
                        l.get("data_proximo_passo"), contar(d, "dia", "dias"),
                        l.get("responsavel") or "sem responsável"] for l, d in regua_vencidos])
    if outros:
        out += ["", "Outros próximos passos de hoje ou vencidos (para uma pessoa, fora da régua):"]
        out += tabela(["Urgência", "Contato", "Etapa", "Próximo passo", "Data", "Atraso", "Responsável"],
                      [[norm(l.get("urgencia")) or "?", quem(l), etapa(l), l.get("proximo_passo"),
                        l.get("data_proximo_passo"), "hoje" if d == 0 else contar(d, "dia", "dias"),
                        l.get("responsavel") or "sem responsável"] for l, d in outros])
    out.append("")

    out += [f"## 4. Propostas paradas ({args.dias_proposta} dias corridos ou mais sem atualização)", ""]
    if paradas:
        out += tabela(["Contato", "Etapa", "Valor", "Dias", "Próximo passo", "Pediu para parar"],
                      [[quem(l), etapa(l), fmt_valor(numero(l.get("valor_proposta"))), str(d),
                        l.get("proximo_passo") or "?", "sim, não retomar" if parou(l) else "não"]
                       for l, d in paradas])
        soma = sum(numero(l.get("valor_proposta")) or 0 for l, _ in paradas)
        out += ["", f"Valor somado das propostas paradas: {fmt_valor(soma)}."]
    else:
        out.append("Nenhuma proposta parada pelo critério.")
    out.append("")

    out += ["## 5. Quem pediu para parar", "",
            f"{contar(total_parar, 'contato', 'contatos')} com `pediu_para_parar = sim`. Nenhum entra em retorno."]
    if conflitos:
        out += ["", "Conflito (pediu para parar e ainda tem próximo passo):"]
        for l, problema in conflitos:
            out.append(f"- {quem(l)}: {problema}. Limpar o próximo passo e a data.")
    if recentes:
        out += ["", "Pediram para parar nos últimos 7 dias (conferir se saíram de toda lista):"]
        for l in recentes:
            out.append(f"- {quem(l)}, atualizado em {l.get('atualizado_em')}")
    out.append("")

    out += ["## 6. Registro a corrigir", ""]
    out += [f"- {c}" for c in correcoes] if correcoes else ["Nenhuma correção encontrada nas linhas lidas."]
    out.append("")

    out += ["## Desde a última rodada", ""]
    out.append(f"- Entradas desde {desde:%d/%m %H:%M}: {len(entraram)}"
               + (" (" + "; ".join(f"{quem(l)}, {norm(l.get('urgencia')) or '?'}" for l in
                                   sorted(entraram, key=urg)) + ")." if entraram else "."))
    if args.triagens:
        out.append("- Triagens do período (ler todas, inclusive sábado e domingo): "
                   + (", ".join(f"{d:%Y-%m-%d} ({DIAS[d.weekday()]})" for d in triagens) if triagens
                      else "nenhuma encontrada."))
    if fila:
        pend, parados = fila
        out.append(f"- Fila de aprovação: {contar(len(pend), 'rascunho pendente', 'rascunhos pendentes')}"
                   f", {len(parados)} há mais de um dia útil.")
    out.append("")

    resp = Counter()
    for l, _ in pessoa:
        resp[l.get("responsavel") or "SEM RESPONSÁVEL"] += 1
    for l, *_ in estourados:
        resp[l.get("responsavel") or "sem responsável"] += 1
    for l in c_hoje:
        resp[l.get("responsavel") or "sem responsável"] += 1
    for l, _ in regua_hoje + regua_vencidos + outros:
        resp[l.get("responsavel") or "sem responsável"] += 1
    if resp:
        out += ["## Por responsável", ""] + [f"- {r}: {n}" for r, n in resp.most_common()] + [""]
    return out


def resumo_da_semana(linhas, hoje):
    seg = hoje - timedelta(days=hoje.weekday() + 7)
    dom = seg + timedelta(days=6)
    dentro = lambda d: d is not None and seg <= d <= dom
    out = [f"## Semana anterior ({seg:%d/%m} a {dom:%d/%m})", ""]
    entradas = [l for l in linhas if dentro((ler_data_hora(l.get("entrada")) or datetime.min).date())]
    out.append(f"- Entradas: {len(entradas)}.")
    for campo, rotulo in (("area", "Por área"), ("canal", "Por canal"), ("origem", "Por origem")):
        c = Counter((l.get(campo) or "não informado") for l in entradas)
        if c:
            out.append(f"- {rotulo}: " + ", ".join(f"{k} {v}" for k, v in c.most_common()) + ".")
    etapas = Counter(etapa(l) or "?" for l in entradas)
    if etapas:
        out.append("- Onde estão hoje: " + ", ".join(f"{k} {v}" for k, v in etapas.most_common()) + ".")
    mexidos = [l for l in linhas if dentro(ler_data(l.get("atualizado_em")))]
    propostas = [l for l in mexidos if etapa(l) in {"proposta-enviada", "negociando"}]
    fechados = [l for l in mexidos if etapa(l) == "fechado"]
    perdidos = [l for l in mexidos if etapa(l) == "perdido"]
    soma = lambda ls: fmt_valor(sum(numero(l.get("valor_proposta")) or 0 for l in ls))
    out.append(f"- Propostas em aberto atualizadas na semana: {len(propostas)}, somando {soma(propostas)}.")
    out.append(f"- Fechados atualizados na semana: {len(fechados)}, somando {soma(fechados)}.")
    motivos = Counter(l.get("motivo_perda") or "sem motivo" for l in perdidos)
    out.append(f"- Perdidos na semana: {len(perdidos)}"
               + (" (" + ", ".join(f"{k} {v}" for k, v in motivos.most_common()) + ")." if perdidos else "."))
    out.append(f"- Pediram para parar: {len([l for l in mexidos if parou(l)])}.")
    out += ["", "Leitura com cuidado: o registro guarda só a etapa atual. O que mudou na semana é "
            "estimado pela coluna `atualizado_em`.", ""]
    return out


# ---------------------------------------------------------------- principal

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("data_posicional", nargs="?", metavar="AAAA-MM-DD")
    p.add_argument("--data")
    p.add_argument("--hora")
    p.add_argument("--expediente")
    p.add_argument("--sabado", action="store_true")
    p.add_argument("--feriados")
    p.add_argument("--prazo-novo")
    p.add_argument("--alertas")
    p.add_argument("--dias-proposta", type=int)
    p.add_argument("--desde")
    p.add_argument("--registro-de-uso")
    p.add_argument("--triagens")
    p.add_argument("--fila")
    p.add_argument("--semana", action="store_true")
    p.add_argument("--sem-semana", action="store_true")
    p.add_argument("--treino", action="store_true")
    args = p.parse_args()

    if "_treino" in Path(args.csv).parts and not args.treino:
        falhar(f"`{args.csv}` é o registro de treino. O treino não entra na rotina real. "
               "Para ler mesmo assim, rode com --treino.")

    criterios, avisos = [], []
    texto_data = args.data or args.data_posicional
    if texto_data:
        hoje = ler_data(texto_data)
        if not hoje:
            falhar(f"data inválida: `{texto_data}`. Use AAAA-MM-DD.")
    else:
        hoje = date.today()
    uteis, sabado = ler_expediente(args.expediente or "09:00-18:00", args.sabado)
    texto_exp = f"expediente {fmt_turnos(uteis)}" + (f", sábado {fmt_turnos(sabado)}" if sabado else "")
    if args.expediente and fmt_turnos(uteis) != args.expediente.strip():
        texto_exp += f" (lido de \"{args.expediente.strip()}\")"
    criterios.append(texto_exp + ("" if args.expediente else " (padrão do script, confirme na ficha)"))
    feriados_txt, marcado = limpar_campo(args.feriados)
    if args.feriados is not None and campo_vazio(feriados_txt):
        avisos.append("campo feriados_e_recessos da ficha vazio"
                      + (f" (`{args.feriados.strip()}`)" if args.feriados.strip() else "")
                      + ": contei como dia sem expediente só o fim de semana")
    elif marcado:
        avisos.append("marcação ignorada no campo feriados_e_recessos da ficha (li só as datas)")
    feriados = ler_feriados(feriados_txt, hoje.year)
    if feriados:
        criterios.append("feriados " + ", ".join(f"{d:%Y-%m-%d}" for d in sorted(feriados)))
    exp = Expediente(uteis, False, feriados, sabado)
    ini = exp.inicio
    if args.prazo_novo is None:
        args.prazo_novo = 2.0
        criterios.append("primeira resposta ao contato novo em 2h úteis (padrão do script, confirme na ficha)")
    else:
        texto_prazo = args.prazo_novo
        args.prazo_novo = ler_prazo(texto_prazo)
        criterios.append(f"primeira resposta ao contato novo em {fmt_horas(args.prazo_novo)} úteis"
                         + ("" if re.fullmatch(r"[\d.,]+", texto_prazo.strip()) else f" (lido de \"{texto_prazo.strip()}\")"))
    alertas_txt, marcado = limpar_campo(args.alertas)
    if args.alertas is not None and campo_vazio(alertas_txt):
        avisos.append("campo palavras_de_alerta da ficha vazio"
                      + (f" (`{args.alertas.strip()}`)" if args.alertas.strip() else "")
                      + ": só os sinais fixos do script tiram o contato da régua")
    elif marcado:
        avisos.append("marcação ignorada no campo palavras_de_alerta da ficha (ela não vira palavra de alerta)")
    n_alertas = montar_alertas(alertas_txt)
    criterios.append("sinais de alerta fixos" + (f" e {n_alertas} da ficha" if n_alertas else "")
                     + " no assunto tiram o contato da régua")
    if args.dias_proposta is None:
        args.dias_proposta = 3
        criterios.append("proposta parada com 3 dias corridos (padrão do script, confirme na ficha)")
    else:
        criterios.append(f"proposta parada com {args.dias_proposta} dias corridos")
    if args.hora:
        agora = datetime.combine(hoje, ler_hora(args.hora))
    elif hoje == date.today():
        agora = datetime.now().replace(second=0, microsecond=0)
    else:
        agora = datetime.combine(hoje, ini)

    if args.desde:
        desde = ler_data_hora(args.desde)
        if not desde:
            falhar(f"--desde inválido: `{args.desde}`. Use \"AAAA-MM-DD HH:MM\".")
        origem_desde = "informado no comando"
    else:
        desde, origem_desde = (None, "")
        if args.registro_de_uso:
            desde, origem_desde = ultima_rodada(args.registro_de_uso, agora)
        if desde is None:
            motivo = origem_desde or "sem registro de uso"
            desde = agora - timedelta(hours=24)
            origem_desde = f"{motivo}: últimas 24 horas"
            avisos.append(f"{motivo}; li as últimas 24 horas")

    linhas, separador, ausentes = ler_csv(args.csv)
    if separador == ";":
        criterios.append("registro separado por ponto e vírgula")
    if ausentes:
        avisos.append("colunas opcionais ausentes: " + ", ".join(ausentes))
    if not linhas:
        avisos.append("o registro tem só a primeira linha, nenhum contato ainda")

    saida = resumo(linhas, hoje, agora, exp, args, criterios, desde, origem_desde, avisos)
    if (hoje.weekday() == 0 or args.semana) and not args.sem_semana:
        saida += resumo_da_semana(linhas, hoje)
    saida.append("Gerado pelo script de pendências da rotina-comercial. Nada foi enviado e o registro não foi alterado.")
    print("\n".join(saida))


if __name__ == "__main__":
    main()
