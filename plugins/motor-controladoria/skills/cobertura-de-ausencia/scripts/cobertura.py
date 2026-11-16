#!/usr/bin/env python3
"""Plano de cobertura de ausência da controladoria (motor-controladoria).

Cópia própria da cobertura-de-ausencia: a leitura do prazos.csv e do calendário é a mesma da
rotina-da-controladoria, para esta habilidade funcionar sozinha.

Lê o prazos.csv e monta, em markdown, o plano de passagem de quem vai sair (férias, licença,
viagem): o que vence antes de sair, no período e nos primeiros dias úteis da volta, prazos,
audiências, perícias e sessões, com quem assume e o que fazer antes de sair em cada linha. Sem
--responsavel, lista o período de todos, por responsável (por exemplo, para o recesso do
escritório). Com --devolucao, monta a devolução na volta: o que venceu no período e como ficou,
e o que entrou com quem assumiu.

Não muda o registro: a troca de responsável é feita linha a linha, com o ok das duas pessoas.
Prazo `sugerido` sai marcado "sem dupla conferência (ainda não vale)", com a instrução de
conferir antes de sair. Não mostra número de processo.

Só biblioteca padrão (Python 3.9+).

Uso:
  python3 cobertura.py CAMINHO/prazos.csv --de AAAA-MM-DD --ate AAAA-MM-DD \
      [--responsavel NOME] [--assume NOME] [--confere NOME] [--volta 3] [--data AAAA-MM-DD] \
      [--publicacoes CAMINHO] [--calendario CAMINHO] [--feriados TEXTO] [--saida plano.md] \
      [--devolucao] [--treino]

Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio, falta coluna obrigatória, o
registro não tem nenhuma linha, uma data é inválida ou recebe registro de treino sem --treino.
"""
import argparse
import csv
import io
import json
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




def mesmo_nome(a, b):
    return norm(a) == norm(b) and not vazio(a)


def linha_tab(p, assume, extra=""):
    st = "sugerido, sem dupla conferência (ainda não vale)" if p["_status"] == "sugerido" else p["_status"]
    if p["_tipo"] in ATOS:
        datas = f"{p['_tipo']} em {fmt(p['_venc'])} | -"
    else:
        datas = f"{fmt(p['_seg']) if p['_seg'] else 'sem data'} | {fmt(p['_venc']) if p['_venc'] else 'sem data'}"
    nome = " · ".join(x for x in (p["id"], p.get("cliente_curto"), p.get("codigo_caso")) if x)
    return (f"| {nome} | {p['_trib']} | {p.get('providencia') or p['tipo']} | {datas} | {st} | "
            f"{p.get('responsavel') or 'sem responsável'} | {assume} | {extra} |")


CAB_TAB = ("| Caso | Tribunal | Providência | Segurança | Fatal | Status | Responsável hoje | Quem assume | Antes de sair |\n"
           "|---|---|---|---|---|---|---|---|---|")


CAB_DEV = ("| Caso | Tribunal | Providência | Segurança | Fatal | Status | Responsável hoje | Volta para | Decisão |\n"
           "|---|---|---|---|---|---|---|---|---|")


def antes_de_sair(p):
    s = p["_status"]
    if p["_tipo"] in ATOS:
        return "confirmar data, hora e link; preparar o cliente" if s != "agendado" else "passar a pauta e o checklist"
    if s == "sugerido":
        return "fazer a dupla conferência antes de sair"
    if s == "conferido":
        return "agendar antes de sair, já na agenda de quem assume"
    return "passar a peça ou a tarefa no estado em que está"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cobertura de ausência da controladoria (motor-controladoria).")
    ap.add_argument("prazos", help="caminho do prazos.csv")
    ap.add_argument("--de", required=True, help="primeiro dia da ausência (AAAA-MM-DD)")
    ap.add_argument("--ate", required=True, help="último dia da ausência (AAAA-MM-DD)")
    ap.add_argument("--responsavel", help="quem sai; sem a opção, lista o período de todos, por responsável")
    ap.add_argument("--assume", default="[A DEFINIR]", help="quem assume (campo cobertura_de_ausencia)")
    ap.add_argument("--confere", default="", help="quem faz a segunda conferência no período")
    ap.add_argument("--volta", type=int, default=3, help="dias úteis depois da volta que entram no plano")
    ap.add_argument("--data", "--hoje", dest="data", help="hoje (padrão: hoje)")
    ap.add_argument("--publicacoes")
    ap.add_argument("--calendario", action="append")
    ap.add_argument("--feriados", default=None)
    ap.add_argument("--devolucao", action="store_true", help="monta a devolução, na volta")
    ap.add_argument("--treino", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args(argv)

    def data_arg(valor, nome):
        d = ler_data(valor or "")
        if not d or not re.fullmatch(r"\s*(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})\s*", valor):
            falhar(f"data inválida em {nome}: `{valor}`. Use AAAA-MM-DD.")
        return d

    de, ate = data_arg(a.de, "--de"), data_arg(a.ate, "--ate")
    if ate < de:
        falhar(f"--ate ({ate}) antes de --de ({de}).")
    hoje = data_arg(a.data, "--data") if a.data else date.today()
    caminho_prazos = Path(a.prazos)
    if "_treino" in {x.lower() for x in caminho_prazos.resolve().parts} and not a.treino:
        falhar("este é um registro de treino (pasta _treino). Rode com --treino.")
    prazos, _aus = ler_csv(a.prazos, OBRIG_PRAZOS, OPC_PRAZOS, "prazos.csv",
                           "escritorio/07-operacao/controladoria/prazos.csv")
    if not prazos:
        falhar("o prazos.csv tem só a linha de títulos: nenhum prazo lido, então não há o que passar. "
               "Confira se o registro é o certo antes de dizer que o período está livre.")
    pubs = []
    pub_caminho = a.publicacoes or (str(caminho_prazos.with_name("publicacoes.csv"))
                                    if caminho_prazos.with_name("publicacoes.csv").exists() else None)
    if pub_caminho:
        pubs, _ = ler_csv(pub_caminho, OBRIG_PUBS, OPC_PUBS, "publicacoes.csv",
                          "escritorio/07-operacao/controladoria/publicacoes.csv")
    pub_por_id = {u["id"]: u for u in pubs}

    escritorio = subir_ate_escritorio(caminho_prazos.resolve().parent)
    cal = Calendario()
    caminhos = list(a.calendario or [])
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
    avisos = list(cal.avisos)
    if a.feriados is not None:
        limpo = MARCACAO.sub(" ", a.feriados).strip()
        if limpo:
            cal.extra = ler_feriados(limpo, de.year)
    if cal.vazio():
        avisos.insert(0, "SEM CALENDÁRIO DE TRIBUNAL: só fins de semana foram pulados no último dia útil "
                         "antes de sair e na janela da volta. Confira os feriados.")

    for p in prazos:
        pub = pub_por_id.get(p.get("publicacao_id", ""))
        trib = (pub or {}).get("tribunal", "").upper().replace(" ", "") or tribunal_do_processo(
            p.get("processo") or (pub or {}).get("processo", ""))
        p["_trib"] = trib or "?"
        p["_status"] = norm(p["status"]) if norm(p["status"]) in STATUS else "sugerido"
        p["_tipo"] = norm(p["tipo"])
        p["_venc"] = ler_data(p["vencimento"])
        p["_seg"] = ler_data(p["data_seguranca"])
        p["_atual"] = ler_data(p["atualizado_em"])

    ultimo_antes = de - timedelta(days=1)
    while not cal.util(ultimo_antes, "?"):
        ultimo_antes -= timedelta(days=1)
    volta = ate + timedelta(days=1)
    while not cal.util(volta, "?"):
        volta += timedelta(days=1)
    fim_volta = cal.somar_uteis(volta - timedelta(days=1), a.volta, "?")

    def datas(p):
        return [d for d in (p["_seg"], p["_venc"]) if d]

    def no_intervalo(p, ini, fim):
        return any(ini <= d <= fim for d in datas(p))

    abertos = [p for p in prazos if p["_status"] in ABERTOS]
    da_pessoa = [p for p in abertos if not a.responsavel or mesmo_nome(p.get("responsavel"), a.responsavel)]
    sem_resp = [p for p in abertos if vazio(p.get("responsavel", ""))]
    ordem = lambda p: (min(datas(p)) if datas(p) else date.max, p["id"])

    periodo = sorted([p for p in da_pessoa if no_intervalo(p, de, ate)], key=ordem)
    antes = sorted([p for p in da_pessoa if p not in periodo and no_intervalo(p, hoje, ultimo_antes)], key=ordem)
    na_volta = sorted([p for p in da_pessoa if p not in periodo and p not in antes
                       and no_intervalo(p, volta, fim_volta)], key=ordem)
    sem_data = [p for p in da_pessoa if not datas(p)]
    vencidos = [p for p in da_pessoa if datas(p) and max(datas(p)) < hoje]

    quem = a.responsavel or "todos os responsáveis"
    out = []
    w = out.append
    if a.devolucao:
        w(f"## Devolução · {quem} · volta em {fmt(volta)}" + (" · TREINO" if a.treino else ""))
        w("")
        w(f"Prazos lidos: {len(prazos)}. Ausência de {fmt(de)} a {fmt(ate)}. Quem assumiu: {a.assume}.")
        w("")
        doperiodo = sorted([p for p in prazos if (not a.responsavel or mesmo_nome(p.get("responsavel"), a.responsavel)
                            or mesmo_nome(p.get("responsavel"), a.assume)) and no_intervalo(p, de, ate)], key=ordem)
        novos = sorted([p for p in abertos if p not in doperiodo and p["_atual"] and de <= p["_atual"] <= ate
                        and (mesmo_nome(p.get("responsavel"), a.assume) or vazio(p.get("responsavel", "")))], key=ordem)
        w("### O que venceu no período e como ficou")
        if doperiodo:
            w("| Caso | Providência | Fatal | Status agora | Cumprido em | Devolver? |")
            w("|---|---|---|---|---|---|")
            for p in doperiodo:
                dev = ("não: fechado" if p["_status"] in ("cumprido", "cancelado")
                       else "PESSOA AGORA: perdido? só a pessoa registra" if p["_venc"] and p["_venc"] < hoje
                       else "sim, com o estado em que está")
                nome = " · ".join(x for x in (p["id"], p.get("cliente_curto"), p.get("codigo_caso")) if x)
                w(f"| {nome} | {p.get('providencia') or p['tipo']} | {fmt(p['_venc'])} | {p['_status']} | "
                  f"{p.get('cumprido_em') or '-'} | {dev} |")
        else:
            w(f"Nenhum prazo do período no registro ({len(prazos)} lidos).")
        w("")
        w("### O que entrou durante a ausência com quem assumiu")
        if novos:
            w(CAB_DEV)
            for p in novos:
                w(linha_tab(p, a.responsavel or "[A DEFINIR]", "devolver ou manter? decisão da pessoa"))
        else:
            w("Nenhum prazo novo em aberto com quem assumiu, pelo atualizado_em do período.")
        w("")
        w("A troca de `responsavel` no prazos.csv é feita com o ok de quem volta e de quem assumiu, linha a linha.")
    else:
        titulo = f"Cobertura de ausência · {quem} · {fmt(de)} a {fmt(ate)}"
        w("---")
        w(f"documento: {titulo}")
        w("versao: 1")
        w(f"gerado_em: {hoje.isoformat()}")
        w("dono: [A DEFINIR]")
        w(f"treino: {'sim' if a.treino else 'nao'}")
        w("---")
        w("")
        w(f"# {titulo}" + (" · TREINO" if a.treino else ""))
        w("")
        w(f"Prazos lidos: {len(prazos)} ({len(abertos)} em aberto). Calendário: "
          f"{', '.join(cal.arquivos) or 'nenhum'}. Último dia útil antes de sair: {fmt(ultimo_antes)}. "
          f"Volta: {fmt(volta)}. Janela da volta: até {fmt(fim_volta)} ({a.volta} dias úteis).")
        for x in avisos:
            w(f"> **Aviso:** {x}")
        w("")
        w("Uso interno. Prazo `sugerido` ainda não vale: quem assume recebe só prazo conferido, ou a "
          "conferência marcada na passagem.")
        w("")
        secoes = [
            (f"1. Antes de sair (segurança ou fatal de {fmt(hoje)} a {fmt(ultimo_antes)})", antes),
            (f"2. No período ({fmt(de)} a {fmt(ate)})", periodo),
            (f"3. Na volta (até {fmt(fim_volta)})", na_volta),
        ]
        for tit, lista in secoes:
            w(f"## {tit}")
            prazos_l = [p for p in lista if p["_tipo"] not in ATOS]
            atos_l = [p for p in lista if p["_tipo"] in ATOS]
            if not lista:
                w(f"Nenhum prazo, audiência ou perícia ({len(da_pessoa)} em aberto de {quem} lidos).")
            if prazos_l:
                w(CAB_TAB)
                for p in prazos_l:
                    w(linha_tab(p, a.assume if tit.startswith("2") else (a.responsavel or p.get("responsavel") or "[A DEFINIR]"),
                                antes_de_sair(p)))
            if atos_l:
                w("")
                w("Audiências, perícias e sessões:")
                w(CAB_TAB)
                for p in atos_l:
                    w(linha_tab(p, a.assume if tit.startswith("2") else (a.responsavel or "[A DEFINIR]"),
                                antes_de_sair(p) + (f"; {p.get('observacao')}" if p.get("observacao") else "")))
            w("")
        if not a.responsavel:
            w("## Por responsável no período")
            grupos = {}
            for p in periodo:
                grupos.setdefault(p.get("responsavel") or "sem responsável", []).append(p)
            for r, lista in sorted(grupos.items()):
                w(f"- {r}: {len(lista)} (" + ", ".join(p["id"] for p in lista) + ")")
            if not grupos:
                w("Ninguém tem prazo no período.")
            w("")
        w("## 4. Pendências do registro")
        algum = False
        for p in vencidos:
            algum = True
            w(f"- {p['id']}: fatal {fmt(p['_venc'])} já passou e segue `{p['_status']}`: resolver antes de sair (só a pessoa registra)")
        for p in sem_data:
            algum = True
            w(f"- {p['id']}: sem data calculada; confirmar o número de dias antes de sair")
        if a.responsavel:
            for p in sem_resp:
                if no_intervalo(p, hoje, fim_volta):
                    algum = True
                    w(f"- {p['id']}: sem responsável e vence até a volta; definir quem cuida")
        if not algum:
            w("Nada pendente no registro para este plano.")
        w("")
        w("## 5. Passagem")
        w(f"- Quem assume os prazos do período: {a.assume}")
        w(f"- Quem faz a segunda conferência no período: {a.confere or '[A DEFINIR]'}"
          " (se quem sai é quem confere, alguém precisa assumir também a conferência)")
        w("- Painéis dos sistemas no período: [A DEFINIR] (quem abre, com a própria senha ou certificado)")
        w("- Agenda: cada prazo do período vai para a agenda de quem assume, com os lembretes da ficha")
        w("- Clientes avisados de quem cuida no período: [A DEFINIR] (pela experiência, se instalada)")
        w("- Combinado em: [AAAA-MM-DD], por [quem sai] e [quem assume]")
        w("")
        w("## 6. Devolução")
        w(f"Na volta ({fmt(volta)}), rode o script com --devolucao e registre aqui o que foi cumprido, o que "
          "segue aberto e o que entrou no período.")
    texto = "\n".join(out) + "\n"
    sys.stdout.write(texto)
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        if a.devolucao and Path(a.saida).exists():
            with open(a.saida, "a", encoding="utf-8") as f:
                f.write("\n" + texto)
        else:
            Path(a.saida).write_text(texto, encoding="utf-8")
        sys.stderr.write(f"gravado: {a.saida}\n")


if __name__ == "__main__":
    main()
