#!/usr/bin/env python3
"""Pendências da controladoria a partir do prazos.csv e do publicacoes.csv (motor-controladoria).

Lê os registros (formato em docs/prazos.md do plugin) e imprime, em markdown, as seções do
resumo do dia na ordem do modelo (assets/modelo-do-resumo.md):

  Comece por aqui                 até cinco ações, PESSOA AGORA primeiro (sugestão)
  PESSOA AGORA                    data de segurança ou fatal vencida, de hoje ou do próximo dia
                                  útil, em qualquer status em aberto; prazo sem data calculada;
                                  publicação captada depois que o prazo já corria; ciência tácita
                                  de intimação de portal em até 2 dias úteis; conferido ou
                                  agendado sem os dois nomes da dupla conferência; divergência
                                  sem decisão a 2 dias úteis ou menos da data mais cedo; publicação
                                  sem caso ou urgente ainda sem decisão de uma pessoa
  PARA DECIDIR                    itens da fila esperando decisão, divergências, dias a confirmar
  Vence na semana                 segurança ou fatal nos próximos N dias úteis
  Esperando a dupla conferência   todos os sugeridos, o mais antigo primeiro, e os parados há
                                  mais de um dia útil
  Publicações sem caso
  Audiências e perícias           dos próximos 15 dias, e as novas desde a última rodada
  Agenda                          conferido sem agenda, sem responsável
  O que não deu para fazer        não triadas, triadas como prazo sem linha, registro a corrigir
  Desde a última rodada

O "próximo dia útil" usa o calendário de cada tribunal (04-base/controladoria/calendario/, formato
da calendario-forense). Sem calendário, só fins de semana são pulados, com aviso em destaque.
Na dúvida, o script põe mais dias como sem expediente: isso só aumenta o que entra em PESSOA AGORA.

Só biblioteca padrão (Python 3.9+). Não altera nada. Não calcula prazo: lê as datas que a
calcular-prazo gravou. Mostra só id, código, nome curto, tribunal, providência, datas, status e
responsável; o número do processo não sai no resumo. Prazo `sugerido` sai sempre marcado como
"sugerido, sem dupla conferência": ainda não vale.

Uso:
  python3 pendencias_controladoria.py CAMINHO/prazos.csv --publicacoes CAMINHO/publicacoes.csv \
      --data AAAA-MM-DD [opções]

Opções:
  --publicacoes ARQUIVO   publicacoes.csv (sem a opção, procura ao lado do prazos.csv)
  --data AAAA-MM-DD       dia do resumo (padrão: hoje); --hoje é o mesmo
  --calendario CAMINHO    arquivo ou pasta de calendários (padrão: 04-base/controladoria/calendario/
                          subindo a partir do prazos.csv; no treino, o calendário de treino da
                          calendario-forense, se instalada)
  --feriados TEXTO        dias sem expediente a mais (campo feriados_e_recessos da ficha, como está:
                          AAAA-MM-DD, DD/MM/AAAA ou DD/MM); vazio ou [A PREENCHER]: ignorado com aviso
  --semana N              janela de "Vence na semana", em dias úteis (padrão 5)
  --audiencias N          janela das audiências e perícias, em dias corridos (padrão 15)
  --registro-de-uso ARQ   registro de uso do ciclo (padrão: 05-automacoes/ciclo-da-controladoria/
                          registro-de-uso.md, subindo a partir do prazos.csv)
  --ultima-rodada DATA    data da última rodada completa, por cima do registro de uso
  --fila PASTA            pasta da fila (padrão: fila/ ao lado do prazos.csv)
  --treino                obrigatório para ler os registros de _treino/
  --saida ARQUIVO         grava o markdown também neste arquivo

Sai com código 1 e uma mensagem que começa com "ERRO:" quando falta o arquivo, ele está vazio,
falta coluna obrigatória, a data é inválida ou recebe registro de treino sem --treino. Nunca diz
que não há nada a apontar sem ter lido: toda seção vazia diz quantas linhas foram lidas.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

OBRIG_PRAZOS = ["id", "codigo_caso", "tipo", "vencimento", "data_seguranca", "responsavel",
                "status", "atualizado_em"]
OPC_PRAZOS = ["publicacao_id", "cliente_curto", "processo", "providencia", "rito", "dias",
              "contagem", "regra", "em_dobro", "publicada_em", "inicio", "calculado_por",
              "conferido_por", "conferido_em", "cumprido_em", "peca_id", "observacao"]
OBRIG_PUBS = ["id", "disponibilizada_em", "tribunal", "triagem"]
OPC_PUBS = ["fonte", "publicada_em", "orgao", "processo", "codigo_caso", "cliente_curto",
            "tipo_ato", "resumo", "teor", "triada_por", "prazo_id", "atualizado_em"]
STATUS = ["sugerido", "conferido", "agendado", "cumprido", "perdido", "cancelado"]
ABERTOS = {"sugerido", "conferido", "agendado"}
TIPOS = ["prazo", "audiencia", "pericia", "sessao", "tarefa"]
ATOS = {"audiencia", "pericia", "sessao"}
TRIAGENS = ["nao-triada", "sem-providencia", "ciencia", "prazo", "audiencia", "pericia",
            "urgente", "sem-caso", "duplicada"]
FONTES = ["djen", "email", "sistema", "planilha", "painel"]
SEM_EXPEDIENTE = {"feriado", "recesso", "suspensao"}
TIPOS_CAL = SEM_EXPEDIENTE | {"expediente-reduzido", "indisponibilidade-programada",
                              "indisponibilidade-certificada"}
DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MARCACAO = re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+[^\]]*\]")
DATA_RE = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})/(\d{2,4})")
# Código do segmento estadual do número CNJ (J = 8): TR -> UF. [CONFERIR] na tabela do CNJ.
UF_TJ = {"01": "AC", "02": "AL", "03": "AP", "04": "AM", "05": "BA", "06": "CE", "07": "DFT",
         "08": "ES", "09": "GO", "10": "MA", "11": "MT", "12": "MS", "13": "MG", "14": "PA",
         "15": "PB", "16": "PR", "17": "PE", "18": "PI", "19": "RJ", "20": "RN", "21": "RS",
         "22": "RO", "23": "RR", "24": "SC", "25": "SE", "26": "SP", "27": "TO"}


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto or "")
                   if not unicodedata.combining(c))


def norm(valor):
    v = sem_acento((valor or "").strip()).lower()
    return re.sub(r"[\s_]+", "-", v)


def vazio(valor):
    v = (valor or "").strip()
    return not v or v in {"-", "?"} or bool(MARCACAO.fullmatch(v))


# ------------------------------------------------------------------ leitura

def decodificar(bruto):
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_csv(caminho, obrigatorias, opcionais, nome, onde):
    p = Path(caminho)
    if not p.exists():
        falhar(f"não encontrei o {nome} em `{caminho}`. Confira o caminho (o padrão é {onde}). "
               "Se o registro ainda não existe, ele nasce com a primeira captação, com a linha de "
               "títulos de docs/prazos.md. Nada foi lido, então não há resumo.")
    if p.is_dir():
        falhar(f"`{caminho}` é uma pasta. Passe o arquivo {nome}.")
    texto = decodificar(p.read_bytes())
    linhas = texto.splitlines()
    if linhas and linhas[0].strip().lower().startswith("sep="):
        linhas = linhas[1:]
    if not "\n".join(linhas).strip():
        falhar(f"o arquivo `{caminho}` está vazio, sem nem a linha de títulos. Copie a linha de "
               "títulos de docs/prazos.md do plugin. Nada foi lido, então não há resumo.")
    primeira = linhas[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cab = [norm(c).replace("-", "_") for c in next(leitor)]
    faltando = [c for c in obrigatorias if c not in cab]
    if faltando:
        falhar(f"faltam colunas obrigatórias no {nome}: {', '.join(faltando)}. Colunas "
               f"encontradas: {', '.join(c for c in cab if c) or 'nenhuma'}. Copie a linha de "
               "títulos de docs/prazos.md e confira se a planilha foi salva como CSV.")
    saida = []
    for n, valores in enumerate(leitor, start=2):
        if not any((v or "").strip() for v in valores):
            continue
        linha = {c: (valores[i] if i < len(valores) else "").strip() for i, c in enumerate(cab) if c}
        for c in opcionais:
            linha.setdefault(c, "")
        linha["_linha"] = n
        saida.append(linha)
    return saida, [c for c in opcionais if c not in cab]


def ler_data(valor):
    m = DATA_RE.search(valor or "")
    if not m:
        return None
    try:
        if m.group(1):
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        ano = int(m.group(6))
        return date(ano + (2000 if ano < 100 else 0), int(m.group(5)), int(m.group(4)))
    except ValueError:
        return None


def fmt(d):
    return d.isoformat() if d else "sem data"


# ------------------------------------------------------------------ calendário

class Calendario:
    """Dias sem expediente por tribunal. Fins de semana sempre contam como sem expediente."""

    def __init__(self):
        self.por_trib = {}      # sigla -> set(date)
        self.todos = set()
        self.extra = set()
        self.cobertura = {}     # sigla ou "todos" -> list[(inicio, fim)]
        self.arquivos = []
        self.avisos = []

    def vazio(self):
        return not self.arquivos

    def fora(self, trib):
        trib = (trib or "").upper()
        if trib in ("", "?"):
            todos = set(self.todos) | self.extra
            for s in self.por_trib.values():
                todos |= s
            return todos
        return self.todos | self.extra | self.por_trib.get(trib, set())

    def util(self, d, trib):
        return d.weekday() < 5 and d not in self.fora(trib)

    def proximo_util(self, d, trib):
        x = d + timedelta(days=1)
        for _ in range(400):
            if self.util(x, trib):
                return x
            x += timedelta(days=1)
        return x

    def somar_uteis(self, d, n, trib):
        x = d
        for _ in range(n):
            x = self.proximo_util(x, trib)
        return x

    def uteis_entre(self, a, b, trib):
        """Dias úteis d com a < d <= b (0 se b <= a)."""
        n, x = 0, a
        while x < b:
            x += timedelta(days=1)
            if self.util(x, trib):
                n += 1
        return n

    def cobre(self, trib, d):
        faixas = self.cobertura.get((trib or "").upper(), []) + self.cobertura.get("todos", [])
        return any(i <= d <= f for i, f in faixas)


def ler_cabecalho(texto):
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n", texto, re.S)
    cab = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                cab[norm(k).replace("-", "_")] = v.split("#")[0].strip()
    return cab


def intervalo(texto):
    datas = [ler_data(x) for x in re.split(r"\s+a\s+|\s+até\s+", texto.strip())]
    datas = [d for d in datas if d]
    if not datas:
        return []
    ini, fim = datas[0], datas[-1]
    if fim < ini:
        ini, fim = fim, ini
    return [ini + timedelta(days=i) for i in range((fim - ini).days + 1)]


def carregar_calendario(caminhos, treino, cal):
    arquivos = []
    for c in caminhos:
        p = Path(c)
        if p.is_dir():
            arquivos += sorted(x for x in p.rglob("*.md") if x.is_file())
        elif p.is_file():
            arquivos.append(p)
    for arq in arquivos:
        texto = decodificar(arq.read_bytes())
        cab = ler_cabecalho(texto)
        eh_treino = norm(cab.get("treino", "")) in ("sim", "s", "yes", "true")
        if eh_treino and not treino:
            cal.avisos.append(f"calendário de treino ignorado no registro real: {arq.name}")
            continue
        if treino and not eh_treino:
            cal.avisos.append(f"calendário real usado no treino ({arq.name}): o feriado de treino "
                              "pode não estar nele")
        tribs = [t.strip().upper() for t in re.split(r"[,;/]| e ", cab.get("tribunal", "")) if t.strip()]
        ano = re.search(r"\d{4}", cab.get("ano", ""))
        cobre_ate = ler_data(cab.get("cobre_ate", ""))
        if ano:
            ini = date(int(ano.group(0)), 1, 1)
            fim = cobre_ate or date(int(ano.group(0)), 12, 31)
            for t in (tribs or ["todos"]):
                cal.cobertura.setdefault(t, []).append((ini, fim))
        conf = cab.get("conferido_em", "")
        if vazio(conf) or not ler_data(conf):
            cal.avisos.append(f"calendário não conferido: {arq.name} (sem conferido_em)")
        linhas_lidas = 0
        colunas = None
        for linha in texto.splitlines():
            if not linha.strip().startswith("|"):
                continue
            partes = [x.strip() for x in linha.strip().strip("|").split("|")]
            if colunas is None:
                nomes = [norm(x).replace("-", "_") for x in partes]
                if "data" in nomes and "tipo" in nomes:
                    colunas = nomes
                continue
            if set("".join(partes)) <= set("-: "):
                continue
            reg = dict(zip(colunas, partes))
            tipo = norm(reg.get("tipo", ""))
            if tipo not in TIPOS_CAL:
                cal.avisos.append(f"{arq.name}: tipo `{reg.get('tipo', '')}` fora da lista; "
                                  "a linha conta como sem expediente, por cautela")
                tipo = "feriado"
            if tipo not in SEM_EXPEDIENTE:
                continue
            dias = intervalo(reg.get("data", ""))
            if not dias:
                cal.avisos.append(f"{arq.name}: data que não li (`{reg.get('data', '')}`)")
                continue
            linhas_lidas += 1
            vale = [v.strip().upper() for v in re.split(r"[,;]| e ", reg.get("vale_para", "")) if v.strip()]
            if not vale or "TODOS" in vale:
                cal.todos.update(dias)
            else:
                for v in vale:
                    cal.por_trib.setdefault(v, set()).update(dias)
        cal.arquivos.append(f"{arq.name} ({linhas_lidas} linhas sem expediente)")


def ler_feriados(texto, ano):
    dias = set()
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", texto):
        try:
            if m.group(1):
                dias.add(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            else:
                a = int(m.group(6)) if m.group(6) else ano
                dias.add(date(a + (2000 if a < 100 else 0), int(m.group(5)), int(m.group(4))))
        except ValueError:
            pass
    return dias


def subir_ate_escritorio(p):
    for pai in [p] + list(p.parents):
        if pai.name == "escritorio":
            return pai
    return None


def tribunal_do_processo(numero):
    m = re.search(r"\d{7}-?\d{2}\.?\d{4}\.?(\d)\.?(\d{2})\.?\d{4}", numero or "")
    if not m:
        return ""
    j, tr = m.group(1), m.group(2)
    if j == "4":
        return f"TRF{int(tr)}"
    if j == "5":
        return f"TRT{int(tr)}"
    if j == "8" and tr in UF_TJ:
        return "TJ" + UF_TJ[tr]
    return ""


# ------------------------------------------------------------------ análise

def nomes_conferencia(texto):
    t = (texto or "").strip()
    if vazio(t):
        return [], False
    turno = bool(re.search(r"2\s*[ºo°]?\s*turno|segundo turno", t, re.I))
    partes = [x.strip() for x in re.split(r";|,|\se\s|/", t) if x.strip()]
    partes = [x for x in partes if not re.search(r"turno", x, re.I)]
    return partes, turno


def data_da_captacao(pub):
    """Data em que a publicação entrou no registro: coluna captada_em, se houver, ou a pasta do teor
    (publicacoes/AAAA-MM-DD/<id>.md, docs/prazos.md)."""
    d = ler_data(pub.get("captada_em", ""))
    if d:
        return d
    m = re.search(r"(\d{4}-\d{2}-\d{2})", pub.get("teor", "") or "")
    return ler_data(m.group(1)) if m else None


def rotulo(p):
    nome = p.get("cliente_curto") or ""
    cod = p.get("codigo_caso") or "sem código"
    return f"{p['id']} · {nome + ' · ' if nome else ''}{cod}"


def status_txt(p):
    s = p["_status"]
    if s == "sugerido":
        return "sugerido, sem dupla conferência (ainda não vale)"
    return s


def dia_semana(d):
    return DIAS_SEMANA[d.weekday()]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pendências da controladoria (motor-controladoria).")
    ap.add_argument("prazos", help="caminho do prazos.csv")
    ap.add_argument("--publicacoes")
    ap.add_argument("--data", "--hoje", dest="data")
    ap.add_argument("--calendario", action="append")
    ap.add_argument("--feriados", default=None)
    ap.add_argument("--semana", type=int, default=5)
    ap.add_argument("--audiencias", type=int, default=15)
    ap.add_argument("--registro-de-uso")
    ap.add_argument("--ultima-rodada")
    ap.add_argument("--fila")
    ap.add_argument("--treino", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args(argv)

    if a.data:
        hoje = ler_data(a.data)
        if not hoje or not re.fullmatch(r"\s*(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})\s*", a.data):
            falhar(f"data inválida em --data: `{a.data}`. Use AAAA-MM-DD.")
    else:
        hoje = date.today()

    caminho_prazos = Path(a.prazos)
    partes_caminho = {x.lower() for x in caminho_prazos.resolve().parts}
    eh_treino = "_treino" in partes_caminho
    if eh_treino and not a.treino:
        falhar("este é um registro de treino (pasta _treino). Rode com --treino; treino nunca entra "
               "no resumo real.")

    prazos, aus_prazos = ler_csv(a.prazos, OBRIG_PRAZOS, OPC_PRAZOS, "prazos.csv",
                                 "escritorio/07-operacao/controladoria/prazos.csv")
    avisos, destaque = [], []

    pub_caminho = a.publicacoes
    if not pub_caminho:
        vizinho = caminho_prazos.with_name("publicacoes.csv")
        pub_caminho = str(vizinho) if vizinho.exists() else None
    pubs, aus_pubs = [], []
    if pub_caminho:
        if "_treino" in {x.lower() for x in Path(pub_caminho).resolve().parts} and not a.treino:
            falhar("o publicacoes.csv é de treino (pasta _treino). Rode com --treino.")
        pubs, aus_pubs = ler_csv(pub_caminho, OBRIG_PUBS, OPC_PUBS, "publicacoes.csv",
                                 "escritorio/07-operacao/controladoria/publicacoes.csv")
    else:
        destaque.append("Publicações não lidas: não achei o publicacoes.csv. As seções de sem caso, "
                        "não triadas e captação com atraso não rodaram.")
    pub_por_id = {p["id"]: p for p in pubs}

    # calendário
    cal = Calendario()
    caminhos = list(a.calendario or [])
    escritorio = subir_ate_escritorio(caminho_prazos.resolve().parent)
    if not caminhos:
        if a.treino:
            achados = []
            if escritorio:
                achados.append(escritorio / "07-operacao" / "_treino" / "controladoria" / "calendario")
            achados.append(Path(__file__).resolve().parent.parent.parent / "calendario-forense"
                           / "assets" / "calendario-de-treino.md")
            caminhos = [str(x) for x in achados if x.exists()][:1]
        elif escritorio and (escritorio / "04-base" / "controladoria" / "calendario").exists():
            caminhos = [str(escritorio / "04-base" / "controladoria" / "calendario")]
    carregar_calendario(caminhos, a.treino, cal)
    avisos += cal.avisos
    if a.feriados is not None:
        limpo = MARCACAO.sub(" ", a.feriados).strip()
        if not limpo:
            avisos.append("campo feriados_e_recessos da ficha vazio ou [A PREENCHER]: ignorado")
        else:
            cal.extra = ler_feriados(limpo, hoje.year)
            if not cal.extra:
                avisos.append(f"não li nenhuma data em --feriados (`{a.feriados}`)")
    if cal.vazio():
        destaque.append("SEM CALENDÁRIO DE TRIBUNAL: só sábados e domingos foram pulados. Um feriado "
                        "pode fazer o prazo de depois de amanhã ser o do próximo dia útil. Monte o "
                        "calendário pela calendario-forense e confira os feriados antes de confiar "
                        "nesta lista.")

    # tribunal de cada prazo
    tribs_sem_cal = set()
    for p in prazos:
        pub = pub_por_id.get(p.get("publicacao_id", ""))
        trib = (pub or {}).get("tribunal", "").upper().replace(" ", "") or tribunal_do_processo(
            p.get("processo") or (pub or {}).get("processo", ""))
        p["_trib"] = trib or "?"
        p["_pub"] = pub
        p["_status"] = norm(p["status"])
        p["_tipo"] = norm(p["tipo"])
        p["_venc"] = ler_data(p["vencimento"])
        p["_seg"] = ler_data(p["data_seguranca"])
        p["_inicio"] = ler_data(p.get("inicio", ""))
        p["_pubd"] = ler_data(p.get("publicada_em", ""))
        p["_atual"] = ler_data(p["atualizado_em"])
        if not cal.vazio() and p["_status"] in ABERTOS and trib and not cal.cobre(trib, hoje):
            tribs_sem_cal.add(trib)
    for t in sorted(tribs_sem_cal):
        destaque.append(f"Sem calendário de {hoje.year} para {t}: para ele, só fins de semana e os dias "
                        "marcados como 'todos' foram pulados.")
    if any(p["_trib"] == "?" and p["_status"] in ABERTOS for p in prazos):
        avisos.append("prazo sem tribunal identificado (sem publicação ligada e número fora do padrão): "
                      "usei os dias sem expediente de todos os calendários, por cautela")

    # última rodada
    ultima, fonte_ultima = None, ""
    if a.ultima_rodada:
        ultima = ler_data(a.ultima_rodada)
        if not ultima:
            falhar(f"data inválida em --ultima-rodada: `{a.ultima_rodada}`.")
        fonte_ultima = "informada"
    else:
        reg = a.registro_de_uso
        if not reg and escritorio and not a.treino:
            cand = escritorio / "05-automacoes" / "ciclo-da-controladoria" / "registro-de-uso.md"
            reg = str(cand) if cand.exists() else None
        if reg and Path(reg).exists():
            for linha in decodificar(Path(reg).read_bytes()).splitlines():
                cols = [c.strip() for c in linha.strip().strip("|").split("|")]
                if len(cols) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}$", cols[0]):
                    como = norm(cols[2])
                    if como not in ("nao-rodou", "so-o-resumo"):
                        d = ler_data(cols[0])
                        if d and d <= hoje and (ultima is None or d > ultima):
                            ultima = d
            fonte_ultima = "registro de uso"
        elif reg:
            avisos.append(f"não achei o registro de uso em `{reg}`")

    # ---------------------------------------------------------------- PESSOA AGORA
    agora = []      # (data de ordem, texto, acao)
    para_decidir = []
    corrigir = []
    ids_vistos = {}

    for p in prazos:
        s, t, trib = p["_status"], p["_tipo"], p["_trib"]
        if p["id"] in ids_vistos:
            corrigir.append(f"linha {p['_linha']}: id {p['id']} repetido (também na linha {ids_vistos[p['id']]})")
        ids_vistos.setdefault(p["id"], p["_linha"])
        if s not in STATUS:
            corrigir.append(f"linha {p['_linha']} ({p['id']}): status `{p['status']}` fora da lista; "
                            "tratado como em aberto")
            p["_status"] = s = "sugerido"
        if t not in TIPOS:
            corrigir.append(f"linha {p['_linha']} ({p['id']}): tipo `{p['tipo']}` fora da lista")
        for col in ("vencimento", "data_seguranca", "inicio", "publicada_em", "atualizado_em"):
            v = p.get(col, "")
            if v and not vazio(v) and not ler_data(v):
                corrigir.append(f"linha {p['_linha']} ({p['id']}): data que não li em {col} (`{v}`)")
        if "prazo-material" in norm(p.get("regra", "")):
            corrigir.append(f"{p['id']}: regra prazo-material no registro; prazo de direito material não "
                            "é contado pelo plugin (a pessoa informa a data)")
        if s == "cumprido" and not ler_data(p.get("cumprido_em", "")):
            corrigir.append(f"{p['id']}: cumprido sem data em cumprido_em")
        if p["_seg"] and p["_venc"] and p["_seg"] > p["_venc"]:
            corrigir.append(f"{p['id']}: data de segurança ({fmt(p['_seg'])}) depois da fatal "
                            f"({fmt(p['_venc'])})")
        if s not in ABERTOS:
            continue

        limite = cal.proximo_util(hoje, trib)
        motivos = []    # (prioridade, curto, longo); prioridade 0 vem antes de tudo

        def quando(d):
            return "hoje" if d == hoje else f"no próximo dia útil ({fmt(d)})"

        datas = [d for d in (p["_seg"], p["_venc"]) if d]
        ordem = min(datas) if datas else hoje
        if t in ATOS:
            if p["_venc"] and hoje <= p["_venc"] <= limite:
                motivos.append((0, f"{t} {quando(p['_venc'])}", f"{t} {quando(p['_venc'])}"))
            elif p["_venc"] and p["_venc"] < hoje:
                corrigir.append(f"{p['id']}: {t} de {fmt(p['_venc'])} já passou e segue `{s}`: "
                                "registrar o que aconteceu")
            elif not p["_venc"]:
                motivos.append((1, f"{t} sem data", f"{t} sem data no registro"))
        else:
            if not p["_venc"] or not p["_seg"]:
                falta = "fatal e segurança" if not p["_venc"] and not p["_seg"] else (
                    "fatal" if not p["_venc"] else "segurança")
                dias_txt = "dias a confirmar" if vazio(p.get("dias", "")) else f"{p.get('dias')} dias"
                motivos.append((1, f"sem data {falta} ({dias_txt})",
                                f"sem data {falta} calculada ({dias_txt}): uma pessoa confirma hoje o "
                                "número de dias e a regra"))
            if p["_venc"] and p["_venc"] < hoje:
                motivos.append((0, f"fatal passou em {fmt(p['_venc'])}",
                                f"fatal passou em {fmt(p['_venc'])} sem registro de cumprimento "
                                "(cumprido, perdido ou cancelado: só a pessoa move)"))
            elif p["_venc"] and p["_venc"] <= limite:
                motivos.append((0, f"fatal {quando(p['_venc'])}", f"fatal {quando(p['_venc'])}"))
            if p["_seg"] and (not p["_venc"] or p["_venc"] >= hoje):
                if p["_seg"] < hoje:
                    motivos.append((0, f"segurança passou em {fmt(p['_seg'])}",
                                    f"data de segurança passou em {fmt(p['_seg'])}"))
                elif p["_seg"] <= limite and not any(m[1].startswith("fatal") for m in motivos):
                    motivos.append((0, f"segurança {quando(p['_seg'])}",
                                    f"data de segurança {quando(p['_seg'])}"))
        # captada com atraso
        pub = p["_pub"]
        if s == "sugerido" and pub and p["_inicio"]:
            capt = data_da_captacao(pub)
            if capt and p["_inicio"] < capt:
                corridos = cal.uteis_entre(p["_inicio"] - timedelta(days=1), capt, trib)
                motivos.append((2, f"captada com atraso, {corridos} dias úteis já corridos",
                                f"captada com atraso: disponibilizada em {fmt(ler_data(pub.get('disponibilizada_em')))}, "
                                f"o prazo começou em {fmt(p['_inicio'])} e a publicação só entrou em "
                                f"{fmt(capt)} ({corridos} dias úteis já corridos)"))
        # ciência tácita de portal
        if s == "sugerido" and "intimacao-portal" in norm(p.get("regra", "")) and p["_pubd"]:
            if p["_pubd"] >= hoje and cal.uteis_entre(hoje, p["_pubd"], trib) <= 2:
                motivos.append((2, f"ciência tácita do portal em {fmt(p['_pubd'])}",
                                f"ciência tácita da intimação do portal em {fmt(p['_pubd'])}: se alguém "
                                "abrir antes, a ciência é na abertura e a conta muda (decisão da pessoa)"))
        # divergência sem decisão perto da data mais cedo (dupla-conferencia, passo 8): 2 dias úteis ou menos
        if s == "sugerido" and "diverg" in norm(p.get("observacao", "")):
            datas_d = [d for d in (p["_seg"], p["_venc"]) if d]
            mais_cedo = min(datas_d) if datas_d else None
            if mais_cedo and mais_cedo >= hoje and cal.uteis_entre(hoje, mais_cedo, trib) <= 2 and \
                    not any(m[0] == 0 for m in motivos):
                motivos.append((1, f"divergência sem decisão, data mais cedo {fmt(mais_cedo)}",
                                f"divergência sem decisão: vale a data mais cedo ({fmt(mais_cedo)}), a 2 dias úteis ou "
                                "menos. Quem decide hoje? Nada vai para a agenda antes de conferido"))
        # conferido sem dupla conferência
        if s in ("conferido", "agendado"):
            nomes, turno = nomes_conferencia(p.get("conferido_por", ""))
            if any(norm(x) == "ia" for x in nomes) or (len(nomes) < 2 and not (len(nomes) == 1 and turno)):
                motivos.append((2, f"`{s}` sem a dupla conferência",
                                f"está `{s}` sem os dois nomes da dupla conferência em conferido_por: "
                                "tratar como sugerido até conferir"))
        if motivos:
            motivos.sort(key=lambda m: m[0])
            texto = (f"{rotulo(p)} · {trib} · {p.get('providencia') or p['tipo']} · segurança "
                     f"{fmt(p['_seg'])} · fatal {fmt(p['_venc'])} · {p.get('responsavel') or 'sem responsável'}"
                     f" · {status_txt(p)}: " + "; ".join(m[2] for m in motivos))
            verbo = "Conferir agora" if s == "sugerido" else "Resolver agora"
            agora.append((motivos[0][0], ordem, texto, p,
                          f"{verbo} {rotulo(p)} · {p.get('responsavel') or 'sem responsável'} · "
                          + "; ".join(m[1] for m in motivos)))

        # para decidir
        obs = norm(p.get("observacao", ""))
        if "diverg" in obs:
            para_decidir.append(f"{rotulo(p)} · divergência na dupla conferência anotada; vale a data mais "
                                f"cedo ({fmt(p['_venc'])}) até a decisão")
        if "duvida-do-calendario" in obs or "duvida-do-recesso" in obs or "duvida-da-suspensao" in obs:
            para_decidir.append(f"{rotulo(p)} · dúvida do calendário ou do recesso anotada pela conta; vale a data "
                                f"mais cedo ({fmt(p['_venc'])}) até a pessoa conferir no ato do tribunal")
        if t == "prazo" and vazio(p.get("dias", "")) and s == "sugerido" and p["_venc"]:
            para_decidir.append(f"{rotulo(p)} · número de dias sem fonte no registro: confirmar no ato ou "
                                "na tabela do escritório")

    sem_caso, urgentes, nao_triadas, sem_linha = [], [], [], []
    prazo_por_pub = {p.get("publicacao_id") for p in prazos if p.get("publicacao_id")}
    for u in pubs:
        tri = norm(u["triagem"])
        quem = norm(u.get("triada_por", ""))
        if tri not in TRIAGENS:
            corrigir.append(f"publicação {u['id']}: triagem `{u['triagem']}` fora da lista")
        if tri in ("nao-triada", ""):
            nao_triadas.append(u)
        if tri == "sem-caso" and quem in ("", "ia"):
            sem_caso.append(u)
            agora.append((3, ler_data(u["disponibilizada_em"]) or hoje,
                          f"{u['id']} · sem caso · {u.get('tribunal')} · {u.get('orgao') or 'órgão não informado'}"
                          f" · {u.get('cliente_curto') or 'parte não identificada'}: processo da OAB do "
                          "escritório que não está na carteira; é caso antigo, substabelecimento ou erro? "
                          "Nenhum prazo é calculado antes da resposta", None,
                          f"Decidir de quem é a publicação {u['id']} · sem caso · {u.get('tribunal')}"))
        if tri == "urgente" and quem in ("", "ia"):
            urgentes.append(u)
            agora.append((0, hoje, f"{u['id']} · urgente · {u.get('cliente_curto') or ''} "
                          f"{u.get('codigo_caso') or ''} · {u.get('resumo') or ''}: uma pessoa lê o ato agora", None,
                          f"Ler agora a publicação urgente {u['id']}"))
        if tri in ("prazo", "audiencia", "pericia") and not u.get("prazo_id") and u["id"] not in prazo_por_pub:
            sem_linha.append(u)

    # fila
    fila_pasta = Path(a.fila) if a.fila else caminho_prazos.with_name("fila")
    fila_cont = {}
    if fila_pasta.exists():
        for arq in sorted(fila_pasta.rglob("*.md")):
            cab = ler_cabecalho(decodificar(arq.read_bytes()))
            st, item = norm(cab.get("status", "")), norm(cab.get("item", "")) or "sem-item"
            fila_cont.setdefault((item, st), 0)
            fila_cont[(item, st)] += 1
            dia = ler_data(arq.parent.name)
            if st == "pendente" and dia and cal.uteis_entre(dia, hoje, "?") > 1:
                para_decidir.append(f"fila: {arq.parent.name}/{arq.name} ({item}) pendente desde "
                                    f"{fmt(dia)}, há mais de um dia útil")
            elif st == "pendente" and item == "decidir-providencia":
                para_decidir.append(f"fila: {arq.parent.name}/{arq.name} · decidir a providência"
                                    f"{' · ' + cab.get('codigo') if cab.get('codigo') else ''}")
            elif st == "bloqueado":
                para_decidir.append(f"fila: {arq.parent.name}/{arq.name} bloqueado pelo revisor "
                                    f"({cab.get('revisor', '')})")

    # ---------------------------------------------------------------- outras seções
    abertos = [p for p in prazos if p["_status"] in ABERTOS]
    semana = []
    for p in abertos:
        if p["_tipo"] in ATOS:
            continue
        fim = cal.somar_uteis(hoje, a.semana, p["_trib"])
        datas = [d for d in (p["_seg"], p["_venc"]) if d]
        if datas and hoje <= min(datas) <= fim:
            semana.append((min(datas), p))
    semana.sort(key=lambda x: (x[0], x[1]["id"]))

    sugeridos = sorted([p for p in abertos if p["_status"] == "sugerido" and p["_tipo"] not in ATOS],
                       key=lambda p: (p["_atual"] or hoje, p["_seg"] or date.max, p["id"]))
    atos = sorted([p for p in abertos if p["_tipo"] in ATOS and p["_venc"]], key=lambda p: p["_venc"])
    atos_janela = [p for p in atos if hoje <= p["_venc"] <= hoje + timedelta(days=a.audiencias)]
    atos_novos = [p for p in atos if p not in atos_janela and p["_venc"] >= hoje and ultima
                  and p["_atual"] and p["_atual"] > ultima]
    conferido_sem_agenda = [p for p in abertos if p["_status"] == "conferido"]
    sem_resp = [p for p in abertos if vazio(p.get("responsavel", ""))]

    # ---------------------------------------------------------------- saída
    out = []
    w = out.append
    n_p, n_u = len(prazos), len(pubs)
    lidos = f"prazos lidos: {n_p}; publicações lidas: {n_u}"
    w(f"# Pendências da controladoria · {hoje.isoformat()} ({dia_semana(hoje)})"
      + (" · TREINO" if a.treino else ""))
    w("")
    w(f"Registros: {lidos}. Calendário: {', '.join(cal.arquivos) if cal.arquivos else 'nenhum'}."
      + (f" Última rodada completa: {fmt(ultima)} ({fonte_ultima})." if ultima else ""))
    if a.treino:
        w("")
        w("> TREINO: casos fictícios. Nada daqui entra no resumo real.")
    for d in destaque:
        w("")
        w(f"> **ATENÇÃO:** {d}")
    if n_p == 0:
        w("")
        w("> O prazos.csv tem só a linha de títulos: nenhum prazo foi lido. Isso não quer dizer que não "
          "há prazo; quer dizer que nenhum foi registrado ainda.")
    w("")

    agora.sort(key=lambda x: (x[0], x[1]))
    acoes = []
    for _r, _o, _t, _p, acao in agora:
        acoes.append(acao)
    for x in para_decidir:
        acoes.append("Decidir: " + x[:110])
    for p in sugeridos:
        acoes.append(f"Dupla conferência de {rotulo(p)} · segurança {fmt(p['_seg'])}")
    for p in conferido_sem_agenda:
        acoes.append(f"Agendar {rotulo(p)} · segurança {fmt(p['_seg'])}")
    for p in sem_resp:
        acoes.append(f"Definir o responsável de {rotulo(p)}")
    vistos, unicas = set(), []
    for x in acoes:
        achado = re.search(r"(PZ|PUB)-\d{4}-\d+", x)
        chave = achado.group(0) if achado else x
        if chave not in vistos:
            vistos.add(chave)
            unicas.append(x)
    w("## Comece por aqui (sugestão do script)")
    if unicas:
        for i, x in enumerate(unicas[:5], 1):
            w(f"{i}. {x}")
    elif n_p + n_u == 0:
        w("Nenhuma linha lida nos registros: não há como dizer que está tudo em dia.")
    else:
        w(f"Nada para começar agora nos registros lidos ({lidos}).")
    w("")

    w("## PESSOA AGORA")
    if agora:
        for _r, _o, txt, _p, _a in agora:
            w(f"- {txt}")
    else:
        w(f"Nenhum item nos registros lidos ({lidos}). Próximo dia útil considerado: "
          f"{fmt(cal.proximo_util(hoje, '?'))}.")
    w("")

    w("## PARA DECIDIR")
    if para_decidir:
        for x in para_decidir:
            w(f"- {x}")
    else:
        w("Nada do registro nem da fila esperando decisão"
          + ("" if fila_pasta.exists() else " (pasta da fila não encontrada: só o registro foi lido)") + ".")
    w("")

    w(f"## Vence na semana (próximos {a.semana} dias úteis)")
    if semana:
        w("| Caso | Tribunal | Providência | Segurança | Fatal | Responsável | Status |")
        w("|---|---|---|---|---|---|---|")
        for _, p in semana:
            marca = " (PESSOA AGORA)" if any(x[3] is p for x in agora) else ""
            w(f"| {rotulo(p)}{marca} | {p['_trib']} | {p.get('providencia') or '-'} | {fmt(p['_seg'])} | "
              f"{fmt(p['_venc'])} | {p.get('responsavel') or 'sem responsável'} | {status_txt(p)} |")
    else:
        w(f"Nenhum prazo em aberto com segurança ou fatal nos próximos {a.semana} dias úteis "
          f"({len(abertos)} em aberto lidos).")
    w("")

    w("## Esperando a dupla conferência")
    if sugeridos:
        for p in sugeridos:
            parado = cal.uteis_entre(p["_atual"], hoje, p["_trib"]) if p["_atual"] else None
            flag = f" · sugerido há {parado} dias úteis" if parado and parado > 1 else ""
            w(f"- {rotulo(p)} · {p['_trib']} · {p.get('providencia') or '-'} · data sugerida: segurança "
              f"{fmt(p['_seg'])}, fatal {fmt(p['_venc'])} · regra {p.get('regra') or 'não informada'}"
              f" · {(p.get('dias') + ' ' + (p.get('contagem') or '')).strip() if not vazio(p.get('dias')) else 'dias a confirmar'}{flag}")
        w(f"Total: {len(sugeridos)} sugerido(s). Nenhum vale antes da dupla conferência.")
    else:
        w(f"Nenhum prazo `sugerido` ({len(abertos)} em aberto lidos).")
    w("")

    w("## Publicações sem caso")
    if not pub_caminho:
        w("Não lidas (sem publicacoes.csv).")
    elif sem_caso:
        for u in sem_caso:
            w(f"- {u['id']} · {u.get('fonte') or '-'} · disponibilizada {fmt(ler_data(u['disponibilizada_em']))} · "
              f"{u.get('tribunal')} · {u.get('orgao') or '-'} · {u.get('cliente_curto') or '-'} · "
              f"{u.get('resumo') or '-'}: é caso antigo, substabelecimento ou erro? (decisão da pessoa)")
    else:
        w(f"Nenhuma publicação sem caso esperando decisão ({n_u} publicações lidas).")
    w("")

    w(f"## Audiências e perícias (próximos {a.audiencias} dias)")
    if atos_janela:
        for p in atos_janela:
            em = (p["_venc"] - hoje).days
            w(f"- {fmt(p['_venc'])} ({dia_semana(p['_venc'])}, em {em} dia{'s' if em != 1 else ''}) · "
              f"{p['_tipo']} · {rotulo(p)} · {p.get('observacao') or '-'} · "
              f"{p.get('responsavel') or 'sem responsável'} · {status_txt(p)}")
    else:
        w(f"Nenhuma audiência, perícia ou sessão nos próximos {a.audiencias} dias ({len(atos)} com data lidas).")
    for p in atos_novos:
        w(f"- Nova desde a última rodada, fora da janela: {fmt(p['_venc'])} · {p['_tipo']} · {rotulo(p)} · "
          f"{p.get('observacao') or '-'} · {status_txt(p)}")
    w("")

    w("## Agenda")
    if conferido_sem_agenda:
        w("Conferidos que ainda não estão na agenda:")
        for p in conferido_sem_agenda:
            w(f"- {rotulo(p)} · segurança {fmt(p['_seg'])} · fatal {fmt(p['_venc'])} · conferido por "
              f"{p.get('conferido_por') or '-'} em {p.get('conferido_em') or '-'}")
    else:
        w(f"Nenhum `conferido` sem agenda ({len(abertos)} em aberto lidos).")
    agendados = sum(1 for p in abertos if p["_status"] == "agendado")
    w(f"Agendados em aberto: {agendados}.")
    if sem_resp:
        w("Sem responsável:")
        for p in sem_resp:
            w(f"- {rotulo(p)} · {p.get('providencia') or p['tipo']} · segurança {fmt(p['_seg'])} · {status_txt(p)}")
    else:
        w("Todos os prazos em aberto têm responsável.")
    w("")

    w("## O que não deu para fazer e por quê")
    if pub_caminho:
        if nao_triadas:
            por_fonte = {}
            for u in nao_triadas:
                f = norm(u.get("fonte")) or "sem fonte"
                por_fonte[f] = por_fonte.get(f, 0) + 1
            w("Publicações não triadas: " + ", ".join(f"{k} {v}" for k, v in sorted(por_fonte.items())) + ".")
            for u in nao_triadas:
                w(f"- {u['id']} · {u.get('tribunal')} · disponibilizada {fmt(ler_data(u['disponibilizada_em']))} · "
                  f"{u.get('cliente_curto') or '-'} {u.get('codigo_caso') or ''}")
        else:
            w(f"Nenhuma publicação não triada ({n_u} lidas).")
        for u in sem_linha:
            w(f"- {u['id']} triada como `{norm(u['triagem'])}` e sem linha em prazos.csv "
              f"({u.get('cliente_curto') or '-'} {u.get('codigo_caso') or ''})")
    if corrigir:
        w("Registro a corrigir:")
        for x in corrigir:
            w(f"- {x}")
    else:
        w("Registro sem nada a corrigir nas linhas lidas.")
    for x in avisos:
        w(f"- Aviso: {x}")
    if aus_prazos:
        w(f"- Aviso: colunas que não existem no prazos.csv: {', '.join(aus_prazos)}")
    if aus_pubs:
        w(f"- Aviso: colunas que não existem no publicacoes.csv: {', '.join(aus_pubs)}")
    w("")

    w("## Desde a última rodada")
    if ultima:
        dias_sem = cal.uteis_entre(ultima, hoje, "?")
        novas = {}
        for u in pubs:
            base = data_da_captacao(u) or ler_data(u["disponibilizada_em"])
            if base and base > ultima:
                f = norm(u.get("fonte")) or "sem fonte"
                novas[f] = novas.get(f, 0) + 1
        mexidos = {}
        for p in prazos:
            if p["_atual"] and p["_atual"] > ultima:
                mexidos[p["_status"]] = mexidos.get(p["_status"], 0) + 1
        w(f"- Última rodada completa: {fmt(ultima)}, há {dias_sem} dia(s) útil(eis).")
        if dias_sem > 2:
            w("- O ciclo não roda há mais de dois dias úteis: veja o plano em quando-a-rotina-nao-roda.md.")
        w("- Publicações novas por fonte: " + (", ".join(f"{k} {v}" for k, v in sorted(novas.items())) or "nenhuma") + ".")
        w("- Prazos atualizados, por status: " + (", ".join(f"{k} {v}" for k, v in sorted(mexidos.items())) or "nenhum") + ".")
    else:
        w("- Sem data da última rodada (registro de uso não encontrado e --ultima-rodada não informada).")
    if fila_cont:
        w("- Fila: " + ", ".join(f"{i} {s} {n}" for (i, s), n in sorted(fila_cont.items())) + ".")
    elif fila_pasta.exists():
        w("- Fila vazia.")
    w("- Lembrete: `entrada/lidos/` com mais de 7 dias pode ter dado de cliente; quem apaga é a pessoa.")

    texto = "\n".join(out) + "\n"
    sys.stdout.write(texto)
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        sys.stderr.write(f"gravado: {a.saida}\n")


if __name__ == "__main__":
    main()
