#!/usr/bin/env python3
"""Painel interno da controladoria a partir do prazos.csv e do publicacoes.csv (motor-controladoria).

Cópia própria da painel-da-controladoria: a leitura dos registros e do calendário é a mesma da
rotina-da-controladoria, para esta habilidade funcionar sozinha.

Mostra, em markdown e (com --html) numa página interna responsiva, com modo claro e escuro:
  números da semana; prazos da semana por responsável; carga por responsável e status; risco
  (fatal passada sem cumprimento, sugerido perto do fatal, sem data, conferido ou agendado sem os
  dois nomes, conferido sem agenda, sem responsável); publicações por fonte e por triagem;
  audiências e perícias próximas.

"Sugerido perto do fatal" é o prazo `sugerido` com a fatal em até dias_de_seguranca + 1 dias
úteis: a data de segurança já chegou ou chega amanhã e ninguém conferiu. O número vem de
--dias-de-seguranca, senão do campo dias_de_seguranca da ficha da controladoria
(escritorio/04-base/comum/ficha-da-controladoria.md, procurada subindo a partir do prazos.csv, ou
--ficha), senão do padrão do modelo da ficha (2), com aviso.

O painel é só do escritório: nunca vai para cliente. Mostra id, código, primeiro nome, tribunal,
providência, datas, status e responsável; nunca o número do processo. Prazo `sugerido` sai sempre
marcado "sugerido, sem dupla conferência (ainda não vale)". Não altera os registros.

Só biblioteca padrão (Python 3.9+).

Uso:
  python3 painel_controladoria.py CAMINHO/prazos.csv --publicacoes CAMINHO/publicacoes.csv \
      --data AAAA-MM-DD [--semana 5] [--audiencias 15] [--dias-de-seguranca N] [--ficha ARQ] \
      [--calendario CAMINHO] [--feriados TEXTO] [--saida painel.md] [--html painel.html] \
      [--modelo assets/painel-modelo.html] [--nome-do-escritorio "Escritório Modelo"] [--treino]

Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio, falta coluna obrigatória, os
registros não têm nenhuma linha, a data é inválida ou recebe registro de treino sem --treino.
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




def ler_dias_de_seguranca(caminho):
    """Lê `dias_de_seguranca` da ficha da controladoria (só o número antes do parêntese)."""
    try:
        texto = decodificar(Path(caminho).read_bytes())
    except OSError:
        return None
    m = re.search(r"^\s*-?\s*dias_de_seguranca:\s*([^\n(]*)", texto, re.M)
    if not m or vazio(m.group(1)):
        return None
    n = re.search(r"\d+", m.group(1))
    return int(n.group(0)) if n else None


def item(p, hoje, cal):
    sug = p["_status"] == "sugerido"
    limite = cal.proximo_util(hoje, p["_trib"])
    datas = [d for d in (p["_seg"], p["_venc"]) if d]
    agora = bool(datas) and min(datas) <= limite
    return {
        "id": p["id"], "cliente": p.get("cliente_curto") or "", "codigo": p.get("codigo_caso") or "",
        "tribunal": p["_trib"], "providencia": p.get("providencia") or p["tipo"], "tipo": p["_tipo"],
        "seguranca": fmt(p["_seg"]) if p["_seg"] else "", "fatal": fmt(p["_venc"]) if p["_venc"] else "",
        "status": p["_status"], "sugerido": sug, "agora": agora,
        "responsavel": p.get("responsavel") or "", "observacao": p.get("observacao") or "",
    }


def linha_md(i):
    st = "sugerido, sem dupla conferência (ainda não vale)" if i["sugerido"] else i["status"]
    nome = " · ".join(x for x in (i["id"], i["cliente"], i["codigo"]) if x)
    datas = (f"segurança {i['seguranca'] or 'sem data'} · fatal {i['fatal'] or 'sem data'}"
             if i["tipo"] not in ATOS else f"{i['tipo']} em {i['fatal'] or 'sem data'}")
    return (f"- {nome} · {i['tribunal']} · {i['providencia']} · {datas} · {st}"
            + (" · hoje ou no próximo dia útil" if i["agora"] else ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Painel interno da controladoria (motor-controladoria).")
    ap.add_argument("prazos", help="caminho do prazos.csv")
    ap.add_argument("--publicacoes")
    ap.add_argument("--data", "--hoje", dest="data")
    ap.add_argument("--calendario", action="append")
    ap.add_argument("--feriados", default=None)
    ap.add_argument("--semana", type=int, default=5)
    ap.add_argument("--audiencias", type=int, default=15)
    ap.add_argument("--dias-de-seguranca", type=int)
    ap.add_argument("--ficha")
    ap.add_argument("--treino", action="store_true")
    ap.add_argument("--saida")
    ap.add_argument("--html")
    ap.add_argument("--modelo")
    ap.add_argument("--nome-do-escritorio", default="")
    a = ap.parse_args(argv)

    if a.data:
        hoje = ler_data(a.data)
        if not hoje or not re.fullmatch(r"\s*(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})\s*", a.data):
            falhar(f"data inválida em --data: `{a.data}`. Use AAAA-MM-DD.")
    else:
        hoje = date.today()
    caminho_prazos = Path(a.prazos)
    if "_treino" in {x.lower() for x in caminho_prazos.resolve().parts} and not a.treino:
        falhar("este é um registro de treino (pasta _treino). Rode com --treino; treino nunca entra "
               "no painel real.")
    prazos, aus_prazos = ler_csv(a.prazos, OBRIG_PRAZOS, OPC_PRAZOS, "prazos.csv",
                                 "escritorio/07-operacao/controladoria/prazos.csv")
    destaque, avisos = [], []
    pub_caminho = a.publicacoes
    if not pub_caminho:
        vizinho = caminho_prazos.with_name("publicacoes.csv")
        pub_caminho = str(vizinho) if vizinho.exists() else None
    pubs = []
    if pub_caminho:
        if "_treino" in {x.lower() for x in Path(pub_caminho).resolve().parts} and not a.treino:
            falhar("o publicacoes.csv é de treino (pasta _treino). Rode com --treino.")
        pubs, _aus = ler_csv(pub_caminho, OBRIG_PUBS, OPC_PUBS, "publicacoes.csv",
                             "escritorio/07-operacao/controladoria/publicacoes.csv")
    else:
        avisos.append("publicações não lidas: não achei o publicacoes.csv; a seção por fonte saiu vazia")
    if not prazos and not pubs:
        falhar("os registros não têm nenhuma linha além dos títulos: não há o que mostrar no painel. "
               "O painel começa depois da primeira captação.")
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
    avisos += cal.avisos
    if a.feriados is not None:
        limpo = MARCACAO.sub(" ", a.feriados).strip()
        if limpo:
            cal.extra = ler_feriados(limpo, hoje.year)
        else:
            avisos.append("campo feriados_e_recessos vazio ou [A PREENCHER]: ignorado")
    if cal.vazio():
        destaque.append("Sem calendário de tribunal: só fins de semana foram pulados nas janelas de dias "
                        "úteis. Monte o calendário pela calendario-forense.")

    dias_seg, fonte_seg = a.dias_de_seguranca, "opção --dias-de-seguranca"
    if dias_seg is None:
        ficha = Path(a.ficha) if a.ficha else (
            escritorio / "04-base" / "comum" / "ficha-da-controladoria.md" if escritorio else None)
        if ficha and ficha.exists():
            dias_seg = ler_dias_de_seguranca(ficha)
            fonte_seg = f"ficha ({ficha.name})"
        if dias_seg is None:
            dias_seg, fonte_seg = 2, "padrão do modelo da ficha; confirme na ficha"

    for p in prazos:
        pub = pub_por_id.get(p.get("publicacao_id", ""))
        trib = (pub or {}).get("tribunal", "").upper().replace(" ", "") or tribunal_do_processo(
            p.get("processo") or (pub or {}).get("processo", ""))
        p["_trib"] = trib or "?"
        p["_status"] = norm(p["status"]) if norm(p["status"]) in STATUS else "sugerido"
        if norm(p["status"]) not in STATUS:
            avisos.append(f"{p['id']}: status `{p['status']}` fora da lista; contado como sugerido")
        p["_tipo"] = norm(p["tipo"])
        p["_venc"] = ler_data(p["vencimento"])
        p["_seg"] = ler_data(p["data_seguranca"])

    abertos = [p for p in prazos if p["_status"] in ABERTOS]
    prazos_ab = [p for p in abertos if p["_tipo"] not in ATOS]
    atos = sorted([p for p in abertos if p["_tipo"] in ATOS and p["_venc"]
                   and hoje <= p["_venc"] <= hoje + timedelta(days=a.audiencias)], key=lambda p: p["_venc"])

    def resp(p):
        return p.get("responsavel") if not vazio(p.get("responsavel", "")) else "sem responsável"

    semana = {}
    for p in prazos_ab:
        fim = cal.somar_uteis(hoje, a.semana, p["_trib"])
        datas = [d for d in (p["_seg"], p["_venc"]) if d]
        if datas and min(datas) <= fim:
            semana.setdefault(resp(p), []).append(p)
    for lista in semana.values():
        lista.sort(key=lambda p: (min(d for d in (p["_seg"], p["_venc"]) if d), p["id"]))

    carga = {}
    for p in abertos:
        c = carga.setdefault(resp(p), {"sugerido": 0, "conferido": 0, "agendado": 0, "atos": 0,
                                        "semana": 0, "total": 0})
        c["total"] += 1
        if p["_tipo"] in ATOS:
            c["atos"] += 1
        else:
            c[p["_status"]] += 1
    for r, lista in semana.items():
        carga[r]["semana"] = len(lista)

    perto, sem_agenda, sem_dupla, sem_resp, sem_data, vencidos = [], [], [], [], [], []
    for p in prazos_ab:
        if p["_venc"] and p["_venc"] < hoje:
            vencidos.append(p)
        if not p["_venc"]:
            sem_data.append(p)
        if p["_status"] == "sugerido" and p["_venc"] and p["_venc"] <= cal.somar_uteis(hoje, dias_seg + 1, p["_trib"]):
            perto.append(p)
        if p["_status"] == "conferido":
            sem_agenda.append(p)
    for p in abertos:
        if p["_status"] in ("conferido", "agendado"):
            nomes, turno = nomes_conferencia(p.get("conferido_por", ""))
            if any(norm(x) == "ia" for x in nomes) or (len(nomes) < 2 and not (len(nomes) == 1 and turno)):
                sem_dupla.append(p)
        if vazio(p.get("responsavel", "")):
            sem_resp.append(p)

    fontes, triagens = {}, {}
    for u in pubs:
        f = norm(u.get("fonte")) or "sem fonte"
        x = fontes.setdefault(f, {"fonte": f, "total": 0, "ultimos_30": 0, "nao_triadas": 0})
        x["total"] += 1
        d = ler_data(u["disponibilizada_em"])
        if d and hoje - timedelta(days=30) <= d <= hoje:
            x["ultimos_30"] += 1
        t = norm(u["triagem"]) or "nao-triada"
        if t == "nao-triada":
            x["nao_triadas"] += 1
        triagens[t] = triagens.get(t, 0) + 1
    sem_caso = [u for u in pubs if norm(u["triagem"]) == "sem-caso" and norm(u.get("triada_por")) in ("", "ia")]

    it = lambda lista: [item(p, hoje, cal) for p in lista]
    agora_n = sum(1 for p in abertos if item(p, hoje, cal)["agora"])
    d = {
        "hoje": hoje.isoformat(), "dia": dia_semana(hoje), "treino": a.treino,
        "escritorio": a.nome_do_escritorio, "semana_n": a.semana, "audiencias_n": a.audiencias,
        "dias_seg": dias_seg, "fonte_dias_seg": fonte_seg,
        "lidos": f"prazos lidos: {len(prazos)}; publicações lidas: {len(pubs)}",
        "calendario": cal.arquivos,
        "numeros": {
            "abertos": len(abertos), "agora": agora_n,
            "semana": sum(len(v) for v in semana.values()),
            "sugeridos": sum(1 for p in prazos_ab if p["_status"] == "sugerido"),
            "risco": len({p["id"] for p in perto + sem_agenda + sem_dupla + sem_resp + sem_data + vencidos}),
            "atos": len(atos), "nao_triadas": triagens.get("nao-triada", 0), "sem_caso": len(sem_caso),
        },
        "por_responsavel": [{"responsavel": r, "itens": it(v)} for r, v in sorted(semana.items())],
        "carga": [dict(responsavel=r, **c) for r, c in sorted(carga.items(), key=lambda x: -x[1]["total"])],
        "risco": {"vencidos": it(vencidos), "perto": it(perto), "sem_data": it(sem_data),
                  "sem_dupla": it(sem_dupla), "sem_agenda": it(sem_agenda), "sem_resp": it(sem_resp)},
        "fontes": sorted(fontes.values(), key=lambda x: -x["total"]),
        "triagens": sorted(triagens.items(), key=lambda x: -x[1]),
        "sem_caso": [{"id": u["id"], "tribunal": u.get("tribunal", ""), "orgao": u.get("orgao", ""),
                      "disponibilizada": fmt(ler_data(u["disponibilizada_em"]))} for u in sem_caso],
        "atos": it(atos),
        "destaque": destaque, "avisos": avisos + ([f"colunas que não existem no prazos.csv: {', '.join(aus_prazos)}"]
                                                  if aus_prazos else []),
    }

    out = []
    w = out.append
    w(f"# Painel da controladoria · {hoje.isoformat()} ({dia_semana(hoje)})" + (" · TREINO" if a.treino else ""))
    w("")
    w("> Uso interno do escritório. Não compartilhar com cliente.")
    for x in destaque:
        w(f"> **ATENÇÃO:** {x}")
    w("")
    w(f"Registros: {d['lidos']}. Calendário: {', '.join(cal.arquivos) or 'nenhum'}. Dias de segurança: "
      f"{dias_seg} ({fonte_seg}).")
    w("")
    n = d["numeros"]
    w("## Números")
    w(f"- Em aberto: {n['abertos']} · hoje ou no próximo dia útil: {n['agora']} · na semana: {n['semana']}"
      f" · sugeridos (sem dupla conferência): {n['sugeridos']} · em risco: {n['risco']}")
    w(f"- Audiências e perícias em {a.audiencias} dias: {n['atos']} · publicações não triadas: "
      f"{n['nao_triadas']} · sem caso esperando decisão: {n['sem_caso']}")
    w("")
    w(f"## Prazos da semana por responsável (próximos {a.semana} dias úteis)")
    if semana:
        for r, lista in sorted(semana.items()):
            w(f"### {r} ({len(lista)})")
            for p in lista:
                w(linha_md(item(p, hoje, cal)))
    else:
        w(f"Nenhum prazo em aberto na semana ({len(prazos_ab)} prazos em aberto lidos).")
    w("")
    w("## Carga por responsável (em aberto)")
    w("| Responsável | Sugeridos | Conferidos | Agendados | Audiências e perícias | Na semana | Total |")
    w("|---|---|---|---|---|---|---|")
    for c in d["carga"]:
        w(f"| {c['responsavel']} | {c['sugerido']} | {c['conferido']} | {c['agendado']} | {c['atos']} | "
          f"{c['semana']} | {c['total']} |")
    if not d["carga"]:
        w(f"| nenhum prazo em aberto ({len(prazos)} lidos) | | | | | | |")
    w("")
    w("## Risco")
    rotulos = [("vencidos", "Fatal passou sem registro de cumprimento"),
               ("perto", f"Sugerido com a fatal em até {dias_seg + 1} dias úteis"),
               ("sem_data", "Sem data calculada"), ("sem_dupla", "Conferido ou agendado sem os dois nomes"),
               ("sem_agenda", "Conferido sem agenda"), ("sem_resp", "Sem responsável")]
    algum = False
    for chave, titulo in rotulos:
        if d["risco"][chave]:
            algum = True
            w(f"### {titulo}")
            for i in d["risco"][chave]:
                w(linha_md(i))
    if not algum:
        w(f"Nenhum prazo em risco pelos critérios do painel ({len(abertos)} em aberto lidos).")
    w("")
    w("## Publicações por fonte")
    if pubs:
        w("| Fonte | Total | Últimos 30 dias | Não triadas |")
        w("|---|---|---|---|")
        for f in d["fontes"]:
            w(f"| {f['fonte']} | {f['total']} | {f['ultimos_30']} | {f['nao_triadas']} |")
        w("")
        w("Por triagem: " + ", ".join(f"{t} {q}" for t, q in d["triagens"]) + ".")
        for u in d["sem_caso"]:
            w(f"- Sem caso esperando decisão: {u['id']} · {u['tribunal']} · {u['orgao']} · disponibilizada {u['disponibilizada']}")
    else:
        w("Publicações não lidas.")
    w("")
    w(f"## Audiências e perícias (próximos {a.audiencias} dias)")
    if atos:
        for i in d["atos"]:
            w(linha_md(i) + (f" · {i['observacao']}" if i["observacao"] else ""))
    else:
        w(f"Nenhuma nos próximos {a.audiencias} dias.")
    if d["avisos"]:
        w("")
        w("## Avisos de preenchimento")
        for x in d["avisos"]:
            w(f"- {x}")
    texto = "\n".join(out) + "\n"
    sys.stdout.write(texto)
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        sys.stderr.write(f"gravado: {a.saida}\n")
    if a.html:
        modelo = Path(a.modelo) if a.modelo else Path(__file__).resolve().parent.parent / "assets" / "painel-modelo.html"
        if not modelo.exists():
            falhar(f"não encontrei o modelo HTML em `{modelo}`.")
        html = modelo.read_text(encoding="utf-8")
        if "__DADOS_DO_PAINEL__" not in html:
            falhar("o modelo HTML não tem o marcador __DADOS_DO_PAINEL__.")
        dados = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
        Path(a.html).parent.mkdir(parents=True, exist_ok=True)
        Path(a.html).write_text(html.replace("__DADOS_DO_PAINEL__", dados), encoding="utf-8")
        sys.stderr.write(f"html: {a.html}\n")


if __name__ == "__main__":
    main()
