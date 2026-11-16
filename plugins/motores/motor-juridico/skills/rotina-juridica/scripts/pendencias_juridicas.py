#!/usr/bin/env python3
"""Pendências da produção jurídica a partir do pecas.csv (motor-juridico).

Lê o registro de peças (formato em docs/producao.md do plugin) e imprime, em markdown,
o resumo do dia, na ordem que o agente-juridico usa:

  ADVOGADO AGORA  prazo interno vencido, de hoje ou de amanhã (até o próximo dia útil)
                  sem minuta aprovada; aprovada com prazo agora; peça esperando tese;
                  minuta sem tese; revisada ou aprovada com citação ou dado pendente;
                  item da fila parado há mais de um dia útil
  1. prazos internos dos próximos dias
  2. peças por etapa
  3. peças paradas (dias úteis na mesma etapa, por etapa)
  4. citações não verdes
  5. dados com alerta ou não conferidos
  6. aprovadas sem protocolo
  7. esperando tese
  8. registro a corrigir
  fila, desde a última rodada e por responsável

Só biblioteca padrão (Python 3.9+). Não altera nada. Mostra só id, código, nome curto,
área, peça, etapa e responsável. Prazo interno é o informado por quem pediu a peça;
o script não calcula prazo processual (isso é da controladoria).

Uso:
  python3 pendencias_juridicas.py CAMINHO/pecas.csv [AAAA-MM-DD] [opções]

Opções:
  --data AAAA-MM-DD          dia do resumo (padrão: hoje)
  --feriados TEXTO           dias sem expediente: datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM (ano do
                             resumo), em qualquer texto; "de DD/MM a DD/MM" vira o intervalo. Pode
                             ser o campo feriados_e_recessos da ficha copiado como está. Vazio ou
                             só [A PREENCHER]: ignorado, com aviso
  --sabado                   conta o sábado como dia útil
  --parada TEXTO             dias úteis máximos por etapa, ex.: "em-analise=7, minuta=3"
                             (padrão: pedida 2, em-analise 5, tese-definida 2, minuta 2,
                             conferida 2, revisada 1, aprovada 1)
  --proximos DIAS            quantos dias corridos mostrar em "prazos internos" (padrão 7)
  --registro-de-uso ARQUIVO  registro de uso do ciclo (05-automacoes/ciclo-juridico/registro-de-uso.md)
  --fila PASTA               pasta da fila (07-operacao/juridico/fila)
  --entrada PASTA            pasta de entrada (07-operacao/juridico/entrada)
  --casos PASTA              pasta dos casos (07-operacao/juridico/casos): confere estrategia.md
                             e protocolo/ de cada peça. Sem --casos, usa a pasta casos/ ao lado
                             do pecas.csv (no treino, também a de _treino/juridico/casos/), se
                             existir; sem pasta, essas duas conferências não rodam, com aviso
  --treino                   permite ler o registro de treino (pasta _treino)

Sai com código 1 e uma mensagem que começa com "ERRO:" quando falta o arquivo, quando ele
está vazio, quando falta uma coluna obrigatória, quando a data é inválida ou quando recebe
o registro de treino sem --treino. Nunca diz que não há nada a apontar sem ter lido.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path

OBRIGATORIAS = ["id", "codigo_caso", "peca", "prazo_interno", "etapa", "citacoes", "dados", "atualizado_em"]
OPCIONAIS = [
    "cliente_curto", "area", "origem", "responsavel", "tese", "habilidade_usada",
    "protocolo_sistema", "protocolo_numero", "protocolo_data",
]
ETAPAS = [
    "pedida", "em-analise", "tese-definida", "minuta", "conferida", "revisada",
    "aprovada", "protocolada", "suspensa",
]
FECHADAS = {"protocolada", "suspensa"}
SEM_MINUTA_APROVADA = {"pedida", "em-analise", "tese-definida", "minuta", "conferida", "revisada"}
ANTES_DA_TESE = {"pedida", "em-analise"}
COM_MINUTA = {"minuta", "conferida", "revisada", "aprovada"}
DEPOIS_DA_CONFERENCIA = {"conferida", "revisada", "aprovada", "protocolada"}
CITACOES = {"nao-conferidas", "verde", "com-amarelo", "com-vermelho"}
DADOS = {"nao-conferidos", "ok", "com-alerta"}
ORIGENS = {"intimacao", "consulta", "passagem", "advogado", "lote"}
PARADA_PADRAO = {
    "pedida": 2, "em-analise": 5, "tese-definida": 2, "minuta": 2,
    "conferida": 2, "revisada": 1, "aprovada": 1,
}
ORDEM_CIT = {"com-vermelho": 0, "nao-conferidas": 1, "": 1, "com-amarelo": 2}
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MARCACAO = re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+[^\]]*\]")


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto or "") if not unicodedata.combining(c))


def norm(valor):
    """Valor de opção comparável: minúsculas, sem acento, espaço e sublinhado viram hífen."""
    v = sem_acento((valor or "").strip()).lower()
    return re.sub(r"[\s_]+", "-", v)


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
        falhar(f"não encontrei o registro de peças em `{caminho}`. Confira o caminho (o padrão é "
               "escritorio/07-operacao/juridico/pecas.csv). Se o registro ainda não existe, ele "
               "nasce com a primeira peça pedida (docs/producao.md). Nada foi lido, então não há resumo.")
    if p.is_dir():
        falhar(f"`{caminho}` é uma pasta. Passe o arquivo pecas.csv.")
    texto = decodificar(p.read_bytes())
    linhas_texto = texto.splitlines()
    if linhas_texto and linhas_texto[0].strip().lower().startswith("sep="):
        linhas_texto = linhas_texto[1:]
    texto = "\n".join(linhas_texto)
    if not texto.strip():
        falhar(f"o arquivo `{caminho}` está vazio, sem nem a primeira linha. Copie a primeira linha "
               "de docs/producao.md do plugin. Nada foi lido, então não há resumo.")
    primeira = linhas_texto[0]
    separador = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO(texto), delimiter=separador)
    cabecalho = [norm(c).replace("-", "_") for c in next(leitor)]
    faltando = [c for c in OBRIGATORIAS if c not in cabecalho]
    if faltando:
        falhar("faltam colunas obrigatórias no registro de peças: " + ", ".join(faltando)
               + f". Colunas encontradas: {', '.join(c for c in cabecalho if c) or 'nenhuma'}. "
               "Copie a primeira linha de docs/producao.md do plugin e confira se a planilha foi "
               "salva como CSV.")
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


# ---------------------------------------------------------------- dias úteis

def limpar_campo(texto):
    """Tira marcações ([A PREENCHER] e afins). Devolve (texto limpo, se havia marcação)."""
    if texto is None:
        return "", False
    limpo = MARCACAO.sub(" ", texto)
    return limpo.strip(), limpo.strip() != texto.strip()


def ler_feriados(texto, ano):
    dias = set()
    if not texto:
        return dias

    def para_data(dia, mes, a=None):
        a = int(a) if a else ano
        a += 2000 if a < 100 else 0
        try:
            return date(a, int(mes), int(dia))
        except ValueError:
            return None

    usado = texto
    padrao_intervalo = re.compile(
        r"de\s+(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\s+a\s+(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", re.I)
    for m in padrao_intervalo.finditer(texto):
        ini = para_data(m.group(1), m.group(2), m.group(3))
        fim = para_data(m.group(4), m.group(5), m.group(6))
        if ini and fim:
            if fim < ini:
                fim = date(fim.year + 1, fim.month, fim.day) if not m.group(6) else fim
            d, n = ini, 0
            while d <= fim and n < 60:
                dias.add(d)
                d += timedelta(days=1)
                n += 1
        usado = usado.replace(m.group(0), " ")
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})", usado):
        try:
            dias.add(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    usado = re.sub(r"\d{4}-\d{1,2}-\d{1,2}", " ", usado)
    for m in re.finditer(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", usado):
        d = para_data(m.group(1), m.group(2), m.group(3))
        if d:
            dias.add(d)
    return dias


class Calendario:
    def __init__(self, feriados, sabado):
        self.feriados = feriados
        self.sabado = sabado

    def util(self, d):
        if d in self.feriados:
            return False
        if d.weekday() == 6:
            return False
        if d.weekday() == 5:
            return self.sabado
        return True

    def uteis_entre(self, inicio, fim):
        """Dias úteis depois de `inicio` até `fim`, inclusive."""
        if fim <= inicio:
            return 0
        n, d = 0, inicio + timedelta(days=1)
        while d <= fim:
            if self.util(d):
                n += 1
            d += timedelta(days=1)
        return n

    def proximo_util(self, d):
        d = d + timedelta(days=1)
        while not self.util(d):
            d += timedelta(days=1)
        return d


# ---------------------------------------------------------------- campos da linha

def etapa(l):
    return norm(l.get("etapa"))


def cit(l):
    return norm(l.get("citacoes"))


def dad(l):
    return norm(l.get("dados"))


def tese(l):
    t = (l.get("tese") or "").strip()
    return "" if norm(t) in {"", "-", "nenhuma", "nenhum", "n/a"} or MARCACAO.fullmatch(t) else t


def quem(l):
    return (l.get("responsavel") or "").strip() or "sem responsável"


def rotulo(l):
    partes = [l.get("id") or f"(linha {l['_linha']}, sem id)", l.get("codigo_caso") or "sem código"]
    if l.get("cliente_curto"):
        partes.append(l["cliente_curto"])
    if l.get("area"):
        partes.append(l["area"])
    partes.append(l.get("peca") or "peça sem nome")
    return " · ".join(partes)


def uteis(n):
    return f"{n} dia útil" if n == 1 else f"{n} dias úteis"


def quando(d, hoje, cal):
    if d is None:
        return "sem prazo interno"
    dif = (d - hoje).days
    if dif < 0:
        return f"{d:%Y-%m-%d}, venceu há {-dif} dia{'s' if dif < -1 else ''}"
    if dif == 0:
        return f"{d:%Y-%m-%d}, hoje"
    if dif == 1:
        return f"{d:%Y-%m-%d}, amanhã"
    texto = f"{d:%Y-%m-%d}, {DIAS[d.weekday()]}"
    if d <= cal.proximo_util(hoje):
        texto += ", antes do próximo dia útil"
    return texto


def ler_parada(texto):
    limites = dict(PARADA_PADRAO)
    if not texto:
        return limites, False
    for trecho in re.split(r"[,;]", texto):
        if not trecho.strip():
            continue
        m = re.fullmatch(r"\s*([\w\- áéíóúãõç]+?)\s*[=:]\s*(\d+)\s*", trecho)
        if not m:
            falhar(f"--parada com trecho que não entendi: `{trecho.strip()}`. Use etapa=dias, "
                   "ex.: \"em-analise=7, minuta=3\".")
        e = norm(m.group(1))
        if e not in ETAPAS or e in FECHADAS:
            falhar(f"--parada cita a etapa `{m.group(1).strip()}`, que não existe ou não para. "
                   "Etapas: " + ", ".join(x for x in ETAPAS if x not in FECHADAS) + ".")
        limites[e] = int(m.group(2))
    return limites, True


# ---------------------------------------------------------------- registro de uso, fila, entrada, casos

def ultima_rodada(caminho, hoje):
    p = Path(caminho)
    if not p.exists():
        return None, f"registro de uso não encontrado em `{caminho}`"
    melhor = None
    for linha in decodificar(p.read_bytes()).splitlines():
        if not linha.strip().startswith("|"):
            continue
        n = sem_acento(linha).lower()
        if "nao rodou" in n or "so o resumo" in n:
            continue
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if not celulas:
            continue
        d = ler_data(celulas[0])
        if not d or d > hoje:
            continue
        h = re.fullmatch(r"(\d{1,2}):(\d{2})", celulas[1]) if len(celulas) > 1 else None
        momento = datetime.combine(d, time(int(h.group(1)), int(h.group(2))) if h else time(0, 0))
        if melhor is None or momento > melhor:
            melhor = momento
    if melhor is None:
        return None, f"registro de uso em `{caminho}` sem nenhuma rodada completa"
    return melhor, "última rodada completa do registro de uso"


def campo_cabecalho(texto, nome):
    m = re.search(rf"^{nome}:\s*(.+?)\s*$", texto, re.M)
    return m.group(1).strip() if m else ""


def ler_fila(pasta, hoje, cal, treino):
    p = Path(pasta)
    if not p.exists():
        return None
    itens = []
    for arq in sorted(p.glob("*/*.md")):
        if "_treino" in arq.parts and not treino:
            continue
        texto = decodificar(arq.read_bytes())
        status = norm(campo_cabecalho(texto, "status").split("#")[0])
        revisor = norm(campo_cabecalho(texto, "revisor").split("#")[0].split(":")[0])
        d = ler_data(arq.parent.name)
        itens.append({"arquivo": arq, "status": status, "revisor": revisor, "data": d,
                      "codigo": campo_cabecalho(texto, "codigo")})
    pendentes = [i for i in itens if i["status"] == "pendente"]
    bloqueados = [i for i in itens if i["status"] == "bloqueado"]
    parados = [i for i in pendentes if i["data"] and cal.uteis_entre(i["data"], hoje) > 1]
    return {"pendentes": pendentes, "bloqueados": bloqueados, "parados": parados}


def ler_entrada(pasta):
    p = Path(pasta)
    if not p.exists():
        return None
    return sorted(f for f in p.iterdir() if f.is_file() and not f.name.startswith((".", "~$")))


def caso_tem(casos, codigo, relativo):
    if not casos or not codigo:
        return None
    alvo = Path(casos) / codigo / relativo
    if relativo.endswith("/"):
        return alvo.is_dir() and any(alvo.iterdir())
    return alvo.exists()


# ---------------------------------------------------------------- resumo

def item(l, *extras):
    return "- " + " · ".join([rotulo(l)] + [e for e in extras if e])


def resumo(linhas, hoje, cal, args, limites, criterios, avisos, desde, origem_desde):
    out = []
    prazo = {id(l): ler_data(l.get("prazo_interno")) for l in linhas}
    atual = {id(l): ler_data(l.get("atualizado_em")) for l in linhas}
    abertas = [l for l in linhas if etapa(l) not in FECHADAS and etapa(l) in ETAPAS]
    limite_agora = cal.proximo_util(hoje)
    if limite_agora < hoje + timedelta(days=1):
        limite_agora = hoje + timedelta(days=1)

    def ordem_prazo(l):
        d = prazo[id(l)]
        return (d is None, d or date.max, l.get("id") or "")

    def fmt_prazo(l):
        d = prazo[id(l)]
        return ("prazo " + quando(d, hoje, cal)) if d else "sem prazo interno"

    def parado_ha(l):
        d = atual[id(l)]
        return cal.uteis_entre(d, hoje) if d else None

    agora = {}

    def para_agora(l, porque):
        if id(l) not in agora:
            agora[id(l)] = (l, [])
        agora[id(l)][1].append(porque)

    for l in abertas:
        e, d = etapa(l), prazo[id(l)]
        if d and d <= limite_agora and e in SEM_MINUTA_APROVADA:
            falta = ("tese anotada, mas a etapa não foi movida para tese-definida" if e in ANTES_DA_TESE and tese(l)
                     else "sem tese e sem minuta") if e in ANTES_DA_TESE else (
                "sem minuta" if e == "tese-definida" else "minuta ainda não aprovada")
            para_agora(l, f"{falta}; quem: {quem(l)}")
        elif d and d <= limite_agora and e == "aprovada":
            para_agora(l, "aprovada, protocolar dentro do prazo interno (a pessoa que protocola)")
        if e in {"revisada", "aprovada"} and (cit(l) != "verde" or dad(l) != "ok"):
            para_agora(l, f"{e} com citações `{l.get('citacoes') or 'vazio'}` e dados "
                          f"`{l.get('dados') or 'vazio'}`: não pode seguir para protocolo (producao.md, regra 4)")
        if e in COM_MINUTA and "tese" in l and not tese(l):
            para_agora(l, "minuta sem tese registrada: a escolha da tese é do advogado")

    espera_tese = []
    for l in abertas:
        if etapa(l) == "em-analise" and not tese(l):
            pronta = caso_tem(args.casos, l.get("codigo_caso"), "estrategia.md")
            espera_tese.append((l, pronta))
            if pronta:
                para_agora(l, "estratégia pronta em casos/<codigo>/estrategia.md: falta a decisão do advogado")
            elif pronta is None:
                para_agora(l, "esperando a tese do advogado (confira se a análise terminou)")

    fila = ler_fila(args.fila, hoje, cal, args.treino) if args.fila else None
    out.append(f"# Pendências da produção jurídica · {hoje:%Y-%m-%d} ({DIAS[hoje.weekday()]})")
    out.append("")
    out.append("Critérios: " + "; ".join(criterios) + ".")
    out.append(f"Leitura desde: {desde:%Y-%m-%d %H:%M} ({origem_desde})." if desde else
               f"Leitura desde: {origem_desde}.")
    if avisos:
        out.append("")
        out.append("Avisos:")
        out.extend(f"- {a}" for a in avisos)
    out.append("")

    out.append("## ADVOGADO AGORA")
    extra_agora = []
    if fila:
        for i in fila["parados"]:
            dias = cal.uteis_entre(i["data"], hoje)
            extra_agora.append(((False, date.min, ""), f"- fila: `{i['arquivo'].parent.name}/{i['arquivo'].name}`"
                          f" pendente há {uteis(dias)} (agentes-e-fila.md: rascunho parado vai para o topo)"))
    linhas_agora = [(ordem_prazo(l), item(l, etapa(l), fmt_prazo(l), "; ".join(rs)))
                    for l, rs in agora.values()]
    linhas_agora.extend(extra_agora)
    if linhas_agora:
        out.extend(t for _, t in sorted(linhas_agora, key=lambda x: x[0]))
    else:
        out.append("Nada para o advogado agora.")
    out.append("")

    out.append(f"## 1. Prazos internos dos próximos {args.proximos} dias")
    janela = [l for l in abertas if prazo[id(l)] and prazo[id(l)] <= hoje + timedelta(days=args.proximos)]
    if janela:
        for l in sorted(janela, key=ordem_prazo):
            out.append(item(l, etapa(l), fmt_prazo(l), quem(l)))
    else:
        out.append("Nenhum prazo interno na janela.")
    sem_prazo = [l for l in abertas if not prazo[id(l)]]
    if sem_prazo:
        out.append(f"- {len(sem_prazo)} peça{'s' if len(sem_prazo) > 1 else ''} aberta{'s' if len(sem_prazo) > 1 else ''} "
                   "sem prazo interno: ficam no fim da fila. Quem pediu informa o prazo.")
    out.append("")

    out.append("## 2. Peças por etapa")
    contagem = Counter(etapa(l) for l in linhas if etapa(l) in ETAPAS)
    out.append("| Etapa | Peças | Mais tempo na etapa (dias úteis) |")
    out.append("|---|---|---|")
    for e in ETAPAS:
        if contagem[e]:
            dias = [parado_ha(l) for l in linhas if etapa(l) == e and parado_ha(l) is not None]
            out.append(f"| {e} | {contagem[e]} | {max(dias) if dias and e not in FECHADAS else '-'} |")
    if not contagem:
        out.append("| (nenhuma peça no registro) | 0 | - |")
    out.append("")

    out.append("## 3. Peças paradas")
    paradas = []
    for l in abertas:
        e, dias = etapa(l), parado_ha(l)
        if e in limites and dias is not None and dias > limites[e]:
            paradas.append((-(dias - limites[e]), l, dias))
    if paradas:
        for _, l, dias in sorted(paradas, key=lambda x: (x[0], ordem_prazo(x[1]))):
            out.append(item(l, f"{etapa(l)} há {uteis(dias)} (limite {limites[etapa(l)]})", quem(l)))
    else:
        out.append("Nenhuma peça parada além do limite da etapa.")
    out.append("")

    out.append("## 4. Citações não verdes")
    nao_verdes = [l for l in abertas if etapa(l) in COM_MINUTA and cit(l) != "verde"]
    if nao_verdes:
        oque = {
            "com-vermelho": "vermelho: sai da peça, troca por outra conferida ou o advogado decide",
            "com-amarelo": "amarelo: o advogado ajusta e a citação volta à conferência",
            "nao-conferidas": "não conferidas: conferir-citacoes; o que faltar vira pesquisa no Jus IA",
            "": "coluna vazia: conferir-citacoes",
        }
        for l in sorted(nao_verdes, key=lambda x: (ORDEM_CIT.get(cit(x), 3), ordem_prazo(x))):
            out.append(item(l, etapa(l), oque.get(cit(l), f"valor `{l.get('citacoes')}` fora do padrão")))
    elif not [l for l in abertas if etapa(l) in COM_MINUTA]:
        out.append("Nenhuma minuta aberta.")
    else:
        out.append("Todas as minutas abertas estão com citações verdes.")
    out.append("")

    out.append("## 5. Dados com alerta")
    dados_l = [l for l in abertas if (etapa(l) in COM_MINUTA and dad(l) != "ok")]
    if dados_l:
        for l in sorted(dados_l, key=lambda x: (dad(x) != "com-alerta", ordem_prazo(x))):
            txt = ("com alerta: ver o relatório da conferir-peca em casos/<codigo>/conferencias/"
                   if dad(l) == "com-alerta" else "dados ainda não conferidos: conferir-peca")
            out.append(item(l, etapa(l), txt))
    elif not [l for l in abertas if etapa(l) in COM_MINUTA]:
        out.append("Nenhuma minuta aberta.")
    else:
        out.append("Nenhuma minuta aberta com dado pendente.")
    out.append("")

    out.append("## 6. Aprovadas sem protocolo")
    aprovadas = [l for l in abertas if etapa(l) == "aprovada"]
    if aprovadas:
        for l in sorted(aprovadas, key=ordem_prazo):
            dias = parado_ha(l)
            check = caso_tem(args.casos, l.get("codigo_caso"), "protocolo/")
            nota = ("checklist em casos/<codigo>/protocolo/" if check else
                    "sem checklist de protocolo: preparar-protocolo" if check is False else "")
            out.append(item(l, f"aprovada há {uteis(dias) if dias is not None else '? dias úteis'}",
                            fmt_prazo(l), l.get("protocolo_sistema") or "", nota))
    else:
        out.append("Nenhuma peça aprovada esperando protocolo.")
    out.append("")

    out.append("## 7. Esperando tese")
    if espera_tese:
        for l, pronta in sorted(espera_tese, key=lambda x: ordem_prazo(x[0])):
            estado = ("estratégia pronta, falta a decisão" if pronta else
                      "análise em andamento (sem estrategia.md)" if pronta is False else
                      "confira se a estratégia está pronta")
            out.append(item(l, estado, f"em análise há {uteis(parado_ha(l)) if parado_ha(l) is not None else '? dias úteis'}"))
    else:
        out.append("Nenhuma peça esperando tese.")
    out.append("")

    out.append("## 8. Registro a corrigir")
    corrigir = []
    vistos = Counter((l.get("id") or "").strip().upper() for l in linhas)
    for l in linhas:
        ref = f"linha {l['_linha']} ({l.get('id') or 'sem id'})"
        i = (l.get("id") or "").strip()
        e = etapa(l)
        if not i:
            corrigir.append(f"{ref}: id vazio")
        elif not re.fullmatch(r"P-\d{4}-\d{4}", i, re.I):
            corrigir.append(f"{ref}: id fora do padrão P-AAAA-NNNN")
        if i and vistos[i.upper()] > 1:
            corrigir.append(f"{ref}: id repetido")
        c = (l.get("codigo_caso") or "").strip()
        if not re.fullmatch(r"C-\d{4}-\d{4}(-\d+)?", c, re.I):
            corrigir.append(f"{ref}: codigo_caso `{c or 'vazio'}` fora do padrão C-AAAA-NNNN")
        if e not in ETAPAS:
            corrigir.append(f"{ref}: etapa `{l.get('etapa') or 'vazia'}` não existe (producao.md)")
        if cit(l) and cit(l) not in CITACOES:
            corrigir.append(f"{ref}: citacoes `{l.get('citacoes')}` fora das opções")
        if dad(l) and dad(l) not in DADOS:
            corrigir.append(f"{ref}: dados `{l.get('dados')}` fora das opções")
        if "origem" in l and norm(l.get("origem")) and norm(l.get("origem")) not in ORIGENS:
            corrigir.append(f"{ref}: origem `{l.get('origem')}` fora das opções")
        if (l.get("prazo_interno") or "").strip() and not prazo[id(l)]:
            corrigir.append(f"{ref}: prazo_interno `{l.get('prazo_interno')}` não é data")
        if not atual[id(l)]:
            corrigir.append(f"{ref}: atualizado_em vazio ou inválido (a peça não entra em \"paradas\")")
        if e in DEPOIS_DA_CONFERENCIA and e not in {"revisada", "aprovada"} and (cit(l) != "verde" or dad(l) != "ok"):
            corrigir.append(f"{ref}: em `{e}` com citações `{l.get('citacoes') or 'vazio'}` e dados "
                            f"`{l.get('dados') or 'vazio'}` (producao.md, regra 4)")
        if e == "protocolada":
            faltam = [col for col in ("protocolo_sistema", "protocolo_numero", "protocolo_data")
                      if not (l.get(col) or "").strip()]
            if faltam:
                corrigir.append(f"{ref}: protocolada sem {', '.join(faltam)}")
        elif (l.get("protocolo_numero") or "").strip() and e in ETAPAS:
            corrigir.append(f"{ref}: protocolo_numero preenchido antes de `protocolada` (producao.md, regra 2)")
        if e in ANTES_DA_TESE and tese(l):
            corrigir.append(f"{ref}: tese preenchida em `{e}`: se o advogado já decidiu, ele move para tese-definida")
        if e not in FECHADAS and "responsavel" in l and not (l.get("responsavel") or "").strip():
            corrigir.append(f"{ref}: peça aberta sem responsável")
    if corrigir:
        out.extend(f"- {c}" for c in corrigir)
    else:
        out.append("Nada a corrigir no registro.")
    out.append("")

    out.append("## Fila do advogado")
    if fila is None:
        out.append("Fila não lida (rode com --fila 07-operacao/juridico/fila)." if not args.fila else
                   f"Pasta da fila não encontrada em `{args.fila}`.")
    else:
        rev = Counter(i["revisor"] or "sem revisor" for i in fila["pendentes"])
        out.append(f"- {len(fila['pendentes'])} pendente{'s' if len(fila['pendentes']) != 1 else ''} ("
                   + (", ".join(f"{n} com revisor {k}" for k, n in sorted(rev.items())) or "nenhum") + ")")
        out.append(f"- {len(fila['bloqueados'])} bloqueado{'s' if len(fila['bloqueados']) != 1 else ''}"
                   " (o motivo está no cabeçalho de cada item)")
        out.append(f"- {len(fila['parados'])} pendente{'s' if len(fila['parados']) != 1 else ''} há mais de um dia útil")
    out.append("")

    out.append("## Desde a última rodada")
    if desde:
        mudadas = [l for l in linhas if atual[id(l)] and atual[id(l)] >= desde.date()]
        out.append(f"- {len(mudadas)} linha{'s' if len(mudadas) != 1 else ''} do registro com atualizado_em desde {desde:%Y-%m-%d}")
    entrada = ler_entrada(args.entrada) if args.entrada else None
    if args.entrada:
        if entrada is None:
            out.append(f"- pasta de entrada não encontrada em `{args.entrada}`")
        else:
            out.append(f"- {len(entrada)} arquivo{'s' if len(entrada) != 1 else ''} em entrada/ esperando o ciclo"
                       " (todo arquivo que está lá é novo, de qualquer data)")
    else:
        out.append("- entrada/ não lida (rode com --entrada 07-operacao/juridico/entrada)")
    out.append("")

    out.append("## Por responsável")
    por = defaultdict(Counter)
    for l in abertas:
        por[quem(l)][etapa(l)] += 1
    if por:
        for pessoa, cont in sorted(por.items(), key=lambda x: -sum(x[1].values())):
            out.append(f"- {pessoa}: {sum(cont.values())} ("
                       + ", ".join(f"{n} {e}" for e, n in sorted(cont.items(), key=lambda x: ETAPAS.index(x[0]))) + ")")
    else:
        out.append("Nenhuma peça aberta.")
    out.append("")
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("data_posicional", nargs="?", metavar="AAAA-MM-DD")
    p.add_argument("--data")
    p.add_argument("--feriados")
    p.add_argument("--sabado", action="store_true")
    p.add_argument("--parada")
    p.add_argument("--proximos", type=int, default=7)
    p.add_argument("--registro-de-uso")
    p.add_argument("--fila")
    p.add_argument("--entrada")
    p.add_argument("--casos")
    p.add_argument("--treino", action="store_true")
    args = p.parse_args()

    if "_treino" in Path(args.csv).parts and not args.treino:
        falhar(f"`{args.csv}` é o registro de treino. O treino não entra na rotina real. "
               "Para ler mesmo assim, rode com --treino.")

    texto_data = args.data or args.data_posicional
    if texto_data:
        hoje = ler_data(texto_data)
        if not hoje:
            falhar(f"data inválida: `{texto_data}`. Use AAAA-MM-DD.")
    else:
        hoje = date.today()

    criterios, avisos = [], []
    feriados_txt, marcado = limpar_campo(args.feriados)
    if args.feriados is not None and not re.search(r"\d", feriados_txt):
        avisos.append("campo feriados_e_recessos da ficha vazio"
                      + (f" (`{args.feriados.strip()}`)" if args.feriados.strip() else "")
                      + ": contei como dia sem expediente só o fim de semana")
    elif marcado:
        avisos.append("marcação ignorada no campo feriados_e_recessos (li só as datas)")
    feriados = ler_feriados(feriados_txt, hoje.year)
    cal = Calendario(feriados, args.sabado)
    criterios.append("dias úteis de segunda a " + ("sábado" if args.sabado else "sexta")
                     + (", sem os feriados " + ", ".join(f"{d:%Y-%m-%d}" for d in sorted(feriados)) if feriados else ""))
    limites, mudou = ler_parada(args.parada)
    criterios.append("parada além de " + ", ".join(f"{e} {n}" for e, n in limites.items()) + " dias úteis"
                     + ("" if mudou else " (padrão do script, confirme na ficha da automação)"))
    criterios.append(f"ADVOGADO AGORA com prazo interno até {cal.proximo_util(hoje):%Y-%m-%d} (próximo dia útil)")

    desde, origem_desde = None, ""
    if args.registro_de_uso:
        desde, origem_desde = ultima_rodada(args.registro_de_uso, hoje)
        if desde is None:
            avisos.append(origem_desde + "; \"desde a última rodada\" usa o dia anterior")
            desde = datetime.combine(hoje - timedelta(days=1), time(0, 0))
            origem_desde = "sem rodada registrada: dia anterior"
        elif cal.uteis_entre(desde.date(), hoje) > 2:
            avisos.append(f"o ciclo não roda desde {desde:%Y-%m-%d}: mais de dois dias úteis sem ciclo "
                          "(rotina-juridica, modo não rodou)")
    else:
        origem_desde = "sem --registro-de-uso, a seção \"desde a última rodada\" fica incompleta"

    if not args.casos:
        perto = Path(args.csv).resolve().parent
        candidatos = [perto / "casos"]
        if "_treino" in perto.parts:
            i = perto.parts.index("_treino")
            candidatos.append(Path(*perto.parts[:i + 1]) / "juridico" / "casos")
        achada = next((c for c in candidatos if c.is_dir()), None)
        if achada:
            args.casos = str(achada)
            criterios.append(f"pasta dos casos: `{achada}` (achada sem --casos)")
        else:
            avisos.append("sem pasta casos/ ao lado do pecas.csv (nem --casos): estrategia.md e protocolo/ "
                          "de cada peça não foram conferidos")
    elif not Path(args.casos).is_dir():
        avisos.append(f"a pasta dos casos `{args.casos}` não existe: estrategia.md e protocolo/ não foram conferidos")

    linhas, separador, ausentes = ler_csv(args.csv)
    if separador == ";":
        criterios.append("registro separado por ponto e vírgula")
    if ausentes:
        avisos.append("colunas opcionais ausentes: " + ", ".join(ausentes))
    if not linhas:
        avisos.append("o registro tem só a primeira linha, nenhuma peça ainda")
    if args.treino:
        avisos.append("modo treino: casos fictícios, nada disto entra no resumo real")

    saida = resumo(linhas, hoje, cal, args, limites, criterios, avisos, desde, origem_desde)
    saida.append(f"Lidas {len(linhas)} linhas de `{args.csv}`. Gerado pelo script de pendências da "
                 "rotina-juridica. Nada foi alterado.")
    print("\n".join(saida))


if __name__ == "__main__":
    main()
