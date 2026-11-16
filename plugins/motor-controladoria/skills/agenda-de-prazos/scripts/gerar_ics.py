#!/usr/bin/env python3
"""Gera arquivos .ics (iCalendar) dos prazos conferidos do prazos.csv.

Parte da habilidade agenda-de-prazos do motor-controladoria.

Só entram linhas com status conferido ou agendado (a remarcação de quem já
está na agenda). Linha sugerido é recusada: nada entra na agenda antes da
dupla conferência. Gerar o .ics não muda o status: a linha só vira agendado
com --importado, quando a pessoa diz que importou o arquivo (ou o conector de
agenda confirma). Cada prazo vira um compromisso: a data de segurança é o
compromisso, a data fatal vai no texto como limite. Audiência, perícia e
sessão viram compromisso com hora (lida da observação) na data do ato.
O UID é estável pelo id do prazo, então gerar de novo depois de uma
remarcação atualiza o compromisso na agenda em vez de duplicar.

Uso:
  python3 gerar_ics.py prazos.csv --saida <pasta da agenda> [--id PZ-2026-0001,...]
      [--lembretes "5,2,0"] [--hora-lembrete 08:00] [--preparacao N]
      [--calendario <arquivo ou pasta>] [--publicacoes publicacoes.csv]
      [--do-dia] [--cancelados] [--com-processo] [--duracao-min 60]
      [--hoje AAAA-MM-DD] [--treino] [--gravar] [--json]
  python3 gerar_ics.py prazos.csv --saida <pasta da agenda> --importado PZ-2026-0001,...|todos
      [--origem-importacao "conector de agenda"]
  python3 gerar_ics.py --validar arquivo.ics [outro.ics ...]

Códigos de saída: 0 ok; 1 erro (arquivo ou coluna que falta, id pedido que
não existe ou que foi recusado, .ics inválido).
Python 3.9+, só biblioteca padrão.
"""

import argparse
import codecs
import csv
import datetime as dt
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys
import unicodedata

PRODID = "-//motor-controladoria//agenda-de-prazos//PT-BR"
TZID = "America/Sao_Paulo"
OFFSET_HORAS = 3  # Brasilia, sem horario de verao: UTC-03:00
COLUNAS_OBRIGATORIAS = [
    "id", "codigo_caso", "tipo", "providencia", "vencimento",
    "data_seguranca", "responsavel", "status", "conferido_por",
]
TIPOS_COM_HORA = {"audiencia", "pericia", "sessao"}
STATUS_AGENDAVEIS = {"conferido", "agendado"}
STATUS_FECHADOS = {"cumprido", "perdido", "cancelado"}
DIAS_SEM_EXPEDIENTE = {"feriado", "recesso", "suspensao"}


class Falha(Exception):
    pass


# ---------------------------------------------------------------- leitura

def sem_acento(texto):
    nfkd = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def chave(texto):
    return sem_acento(texto).strip().lower()


class Planilha:
    def __init__(self, caminho):
        if not os.path.isfile(caminho):
            raise Falha("Não achei o arquivo %s. Confira o caminho (o registro fica em "
                        "escritorio/07-operacao/controladoria/prazos.csv)." % caminho)
        bruto = open(caminho, "rb").read()
        self.caminho = caminho
        self.bom = bruto.startswith(codecs.BOM_UTF8)
        texto = None
        for enc in ("utf-8-sig", "cp1252"):
            try:
                texto = bruto.decode(enc)
                self.encoding = enc
                break
            except UnicodeDecodeError:
                continue
        if texto is None or not texto.strip():
            raise Falha("O arquivo %s está vazio: falta ao menos a linha de títulos." % caminho)
        self.nova_linha = "\r\n" if "\r\n" in texto else "\n"
        primeira = texto.splitlines()[0]
        self.sep = ";" if primeira.count(";") > primeira.count(",") else ","
        leitor = csv.reader(io.StringIO(texto), delimiter=self.sep)
        linhas = [l for l in leitor]
        self.titulos = [t.strip() for t in linhas[0]]
        self.chaves = [chave(t) for t in self.titulos]
        self.linhas = []
        for crua in linhas[1:]:
            if not any(c.strip() for c in crua):
                continue
            registro = {}
            for i, k in enumerate(self.chaves):
                registro[k] = crua[i].strip() if i < len(crua) else ""
            self.linhas.append(registro)

    def exigir(self, colunas):
        faltam = [c for c in colunas if c not in self.chaves]
        if faltam:
            raise Falha("Faltam colunas em %s: %s. A linha de títulos certa está em "
                        "docs/prazos.md." % (self.caminho, ", ".join(faltam)))

    def gravar(self):
        saida = io.StringIO()
        escritor = csv.writer(saida, delimiter=self.sep, lineterminator=self.nova_linha)
        escritor.writerow(self.titulos)
        for r in self.linhas:
            escritor.writerow([r.get(k, "") for k in self.chaves])
        enc = "utf-8" if self.encoding == "utf-8-sig" else self.encoding
        dados = saida.getvalue().encode(enc)
        if self.bom:
            dados = codecs.BOM_UTF8 + dados
        temp = self.caminho + ".tmp"
        with open(temp, "wb") as f:
            f.write(dados)
        os.replace(temp, self.caminho)


def ler_data(texto, campo="data"):
    t = (texto or "").strip()
    if not t:
        return None
    t = t.split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(t, fmt).date()
        except ValueError:
            continue
    raise Falha("Data que não entendi em %s: %r. Use AAAA-MM-DD ou DD/MM/AAAA." % (campo, texto))


# ---------------------------------------------------------- calendario

def ler_calendarios(caminho):
    """Le o calendario no formato da calendario-forense. Devolve lista de
    (inicio, fim, tipo, vale_para) e os avisos."""
    if not caminho:
        return [], []
    arquivos = []
    if os.path.isdir(caminho):
        arquivos = sorted(glob.glob(os.path.join(caminho, "*.md")))
    elif os.path.isfile(caminho):
        arquivos = [caminho]
    else:
        raise Falha("Não achei o calendário %s." % caminho)
    dias = []
    avisos = []
    for arq in arquivos:
        texto = open(arq, encoding="utf-8-sig", errors="replace").read()
        cab = re.search(r"^---\s*$(.*?)^---\s*$", texto, re.M | re.S)
        if cab and re.search(r"conferido_por:\s*(\[|$)", cab.group(1), re.M):
            avisos.append("calendário não conferido: %s" % os.path.basename(arq))
        cols = None
        for linha in texto.splitlines():
            if not linha.strip().startswith("|"):
                continue
            partes = [p.strip() for p in linha.strip().strip("|").split("|")]
            if cols is None:
                if "data" in [chave(p) for p in partes] and "tipo" in [chave(p) for p in partes]:
                    cols = [chave(p) for p in partes]
                continue
            if set("".join(partes)) <= set("-: "):
                continue
            reg = dict(zip(cols, partes))
            data = reg.get("data", "").replace("`", "")
            m = re.findall(r"\d{4}-\d{2}-\d{2}", data)
            if not m:
                continue
            ini = ler_data(m[0])
            fim = ler_data(m[-1]) if len(m) > 1 else ini
            vale = [chave(v) for v in re.split(r"[,;]", reg.get("vale_para", "todos")) if v.strip()]
            dias.append((ini, fim, chave(reg.get("tipo", "")), vale or ["todos"]))
    if arquivos and not dias:
        avisos.append("calendário sem nenhuma data lida: confira a tabela (colunas data | tipo | descricao | vale_para | fonte | conferido_em)")
    return dias, avisos


def dia_util(data, calendario, tribunal):
    if data.weekday() >= 5:
        return False
    trib = chave(tribunal)
    for ini, fim, tipo, vale in calendario:
        if tipo not in DIAS_SEM_EXPEDIENTE:
            continue
        if ini <= data <= fim and ("todos" in vale or (trib and trib in vale)):
            return False
    return True


def recuar(data, n, uteis, calendario, tribunal):
    atual = data
    if not uteis:
        return atual - dt.timedelta(days=n)
    contados = 0
    while contados < n:
        atual -= dt.timedelta(days=1)
        if dia_util(atual, calendario, tribunal):
            contados += 1
    return atual


def proximo_dia_util(data, calendario, tribunal):
    atual = data + dt.timedelta(days=1)
    while not dia_util(atual, calendario, tribunal):
        atual += dt.timedelta(days=1)
    return atual


# ------------------------------------------------------------- lembretes

def ler_lembretes(texto):
    """'5,2,0', '5u,2u,0', '7c' ou o texto da ficha ('5 dias uteis antes, 2 dias
    uteis antes e no dia'). Devolve lista de (n, uteis)."""
    if texto is None:
        return None
    t = chave(texto)
    if not t:
        return None
    itens = []
    for m in re.finditer(r"(\d+)\s*(u\b|c\b|dias?\s+uteis|dias?\s+corridos|dias?)?", t):
        n = int(m.group(1))
        tipo = m.group(2) or ""
        uteis = not (tipo.startswith("c") or "corrido" in tipo)
        itens.append((n, uteis))
    if "no dia" in t or "no proprio dia" in t:
        itens.append((0, True))
    vistos = []
    for item in itens:
        if item not in vistos:
            vistos.append(item)
    if not vistos:
        raise Falha("Não entendi os lembretes %r. Use números de dias úteis antes, por exemplo \"5,2,0\"." % texto)
    return sorted(vistos, key=lambda x: -x[0])


def ler_hora(texto):
    t = chave(texto)
    m = re.search(r"(?<![\d/-])([01]?\d|2[0-3])\s*(?:h(?:oras?|s)?(?:\s*([0-5]\d))?(?![a-z\d])|:([0-5]\d)(?!\d))", t)
    if not m:
        return None
    minuto = m.group(2) or m.group(3) or "00"
    return dt.time(int(m.group(1)), int(minuto))


def ler_link(texto):
    m = re.search(r"https?://[^\s;,)]+", texto or "")
    return m.group(0) if m else ""


def ler_modalidade(texto):
    t = chave(texto)
    if re.search(r"video|virtual|telepresencial|on-?line|teams|meet|zoom|link|https?://", t):
        return "videoconferencia"
    if re.search(r"presencial|forum|sala \w|endereco|predio|consultorio", t):
        return "presencial"
    return ""


# ------------------------------------------------------------------ ics

def escapar(texto):
    t = (texto or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
    return t.replace("\r\n", "\\n").replace("\n", "\\n")


def dobrar(linha):
    """Dobra a linha em 75 octetos, sem quebrar caractere UTF-8."""
    dados = linha.encode("utf-8")
    if len(dados) <= 75:
        return [linha]
    partes = []
    atual = ""
    limite = 75
    for c in linha:
        if len((atual + c).encode("utf-8")) > limite:
            partes.append(atual)
            atual = c
            limite = 74  # a linha de continuacao comeca com um espaco
        else:
            atual += c
    partes.append(atual)
    return [partes[0]] + [" " + p for p in partes[1:]]


def utc(data, hora):
    local = dt.datetime.combine(data, hora)
    return (local + dt.timedelta(hours=OFFSET_HORAS)).strftime("%Y%m%dT%H%M%SZ")


VTIMEZONE = [
    "BEGIN:VTIMEZONE", "TZID:%s" % TZID, "BEGIN:STANDARD", "DTSTART:19700101T000000",
    "TZOFFSETFROM:-0300", "TZOFFSETTO:-0300", "TZNAME:-03", "END:STANDARD", "END:VTIMEZONE",
]


def montar_calendario(blocos, com_fuso, nome):
    linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:%s" % PRODID, "CALSCALE:GREGORIAN",
              "METHOD:PUBLISH", "X-WR-CALNAME:%s" % escapar(nome)]
    if com_fuso:
        linhas += VTIMEZONE
    for b in blocos:
        linhas += b
    linhas.append("END:VCALENDAR")
    saida = []
    for l in linhas:
        saida += dobrar(l)
    return "\r\n".join(saida) + "\r\n"


# ------------------------------------------------------------- validacao

def validar_ics(texto, nome="arquivo"):
    erros = []
    if "\r\n" not in texto:
        erros.append("linhas sem CRLF")
    brutas = texto.split("\r\n")
    if brutas and brutas[-1] == "":
        brutas = brutas[:-1]
    for i, l in enumerate(brutas, 1):
        if len(l.encode("utf-8")) > 75:
            erros.append("linha %d com mais de 75 octetos" % i)
        if "\n" in l or "\r" in l:
            erros.append("quebra de linha solta na linha %d" % i)
    linhas = []
    for l in brutas:
        if l.startswith((" ", "\t")) and linhas:
            linhas[-1] += l[1:]
        else:
            linhas.append(l)
    pilha = []
    componentes = []
    for i, l in enumerate(linhas, 1):
        if ":" not in l:
            erros.append("linha %d sem ':' (%s)" % (i, l[:30]))
            continue
        nome_prop, valor = l.split(":", 1)
        base = nome_prop.split(";")[0].upper()
        if base == "BEGIN":
            pilha.append({"tipo": valor.upper(), "props": {}})
        elif base == "END":
            if not pilha or pilha[-1]["tipo"] != valor.upper():
                erros.append("END:%s sem BEGIN correspondente (linha %d)" % (valor, i))
                continue
            comp = pilha.pop()
            componentes.append(comp)
            if pilha and pilha[-1]["tipo"] == "VEVENT" and comp["tipo"] == "VALARM":
                pilha[-1]["props"].setdefault("_ALARMES", []).append(comp)
        else:
            if not pilha:
                erros.append("propriedade fora de componente na linha %d" % i)
                continue
            pilha[-1]["props"].setdefault(base, []).append((nome_prop, valor))
    if pilha:
        erros.append("componente sem END: %s" % ", ".join(p["tipo"] for p in pilha))
    cal = [c for c in componentes if c["tipo"] == "VCALENDAR"]
    if len(cal) != 1:
        erros.append("precisa de exatamente um VCALENDAR")
    else:
        p = cal[0]["props"]
        if [v for _, v in p.get("VERSION", [])] != ["2.0"]:
            erros.append("VCALENDAR sem VERSION:2.0")
        if not p.get("PRODID"):
            erros.append("VCALENDAR sem PRODID")
    eventos = [c for c in componentes if c["tipo"] == "VEVENT"]
    if not eventos:
        erros.append("nenhum VEVENT")
    uids = []
    for ev in eventos:
        p = ev["props"]
        for obrig in ("UID", "DTSTAMP", "DTSTART", "SUMMARY"):
            if len(p.get(obrig, [])) != 1:
                erros.append("VEVENT sem %s (ou repetido)" % obrig)
        if p.get("UID"):
            uids.append(p["UID"][0][1])
        for prop in ("DTSTART", "DTEND"):
            for nome_prop, valor in p.get(prop, []):
                if "VALUE=DATE" in nome_prop.upper() and "DATE-TIME" not in nome_prop.upper():
                    if not re.fullmatch(r"\d{8}", valor):
                        erros.append("%s com data invalida: %s" % (prop, valor))
                elif not re.fullmatch(r"\d{8}T\d{6}Z?", valor):
                    erros.append("%s com data e hora invalida: %s" % (prop, valor))
                elif "TZID=" in nome_prop.upper() and not [c for c in componentes if c["tipo"] == "VTIMEZONE"]:
                    erros.append("%s usa TZID sem VTIMEZONE" % prop)
        for al in p.get("_ALARMES", []):
            ap = al["props"]
            for obrig in ("ACTION", "TRIGGER", "DESCRIPTION"):
                if len(ap.get(obrig, [])) != 1:
                    erros.append("VALARM sem %s" % obrig)
    if len(uids) != len(set(uids)):
        erros.append("UID repetido no mesmo arquivo")
    return erros


# ------------------------------------------------------------ o trabalho

def conferencia_completa(conferido_por):
    t = (conferido_por or "").strip()
    if not t:
        return False, "conferido sem os nomes da dupla conferência em conferido_por"
    tc = chave(t)
    if "turno" in tc:
        return True, ""
    nomes = [n.strip() for n in re.split(r"[;/+]|,", t) if n.strip()]
    if len(nomes) < 2:
        return False, "conferido_por com um nome só (%s): falta a segunda conferência ou o \"2º turno\"" % t
    if len({chave(n) for n in nomes}) < 2:
        return False, "conferido_por com a mesma pessoa duas vezes: no escritório de uma pessoa só, escreva o nome e \"2º turno\""
    return True, ""


def ler_publicacoes(caminho):
    if not caminho:
        return {}
    pl = Planilha(caminho)
    pl.exigir(["id", "tribunal"])
    return {r["id"]: r for r in pl.linhas}


def assinatura(partes):
    return hashlib.sha1("|".join(partes).encode("utf-8")).hexdigest()[:16]


def ler_existente(caminho):
    if not os.path.isfile(caminho):
        return None
    texto = open(caminho, encoding="utf-8", errors="replace").read()
    desdobrado = re.sub(r"\r\n[ \t]", "", texto)
    seq = re.search(r"^SEQUENCE:(\d+)", desdobrado, re.M)
    ass = re.search(r"^X-MOTOR-ASSINATURA:(\w+)", desdobrado, re.M)
    return {"sequencia": int(seq.group(1)) if seq else 0, "assinatura": ass.group(1) if ass else ""}


def nome_arquivo(id_prazo):
    return re.sub(r"[^a-z0-9._-]", "-", id_prazo.lower()) + ".ics"


def montar_compromisso(r, a, pub, calendario, hoje, agora_utc):
    """Devolve (bloco, resumo, avisos) ou levanta Falha com o motivo da recusa."""
    avisos = []
    id_prazo = r["id"]
    tipo = chave(r.get("tipo")) or "prazo"
    tribunal = pub.get("tribunal", "") if pub else ""
    fatal = ler_data(r.get("vencimento"), "vencimento de " + id_prazo)
    seguranca = ler_data(r.get("data_seguranca"), "data_seguranca de " + id_prazo)
    obs = r.get("observacao", "")
    codigo = r.get("codigo_caso") or "sem codigo"
    cliente = r.get("cliente_curto", "")
    quem = (codigo + " " + cliente).strip()
    prov = r.get("providencia") or "[A CONFIRMAR: providencia]"
    prefixo = "TREINO - " if a.treino else ""
    descr = []
    hora = None
    if tipo in TIPOS_COM_HORA:
        if not fatal:
            raise Falha("%s sem a data do ato em vencimento" % id_prazo)
        data_ag = fatal
        hora = ler_hora(obs)
        modalidade = ler_modalidade(obs)
        nome_tipo = {"audiencia": "AUDIÊNCIA", "pericia": "PERÍCIA", "sessao": "SESSÃO"}[tipo]
        titulo = "%s%s %s: %s" % (prefixo, nome_tipo, quem, prov)
        if hora:
            titulo += " às %s" % hora.strftime("%Hh%M")
        if modalidade:
            titulo += " (%s)" % {"videoconferencia": "videoconferência"}.get(modalidade, modalidade)
        if not hora:
            avisos.append("%s: a hora do ato não está na observação; compromisso de dia inteiro, hora [A CONFIRMAR]" % id_prazo)
        if not modalidade:
            avisos.append("%s: local ou link não está na observação [A CONFIRMAR]" % id_prazo)
        descr += [
            "Data do ato: %s%s" % (data_ag.isoformat(), " às " + hora.strftime("%Hh%M") if hora else " (hora a confirmar)"),
            "Modalidade: %s" % ({"videoconferencia": "videoconferência"}.get(modalidade, modalidade) or "a confirmar"),
            "Local ou link: %s" % (ler_link(obs) or "ver a observação"),
            "Providência: %s" % prov,
            "Responsável: %s" % (r.get("responsavel") or "[A PREENCHER]"),
            "Preparação do cliente: aviso na entrada da experiência (preparar-o-cliente, do motor-experiencia, se instalado) e o checklist da audiencias-e-pericias.",
        ]
    else:
        if not seguranca:
            raise Falha("%s sem data_seguranca: rode a calcular-prazo antes" % id_prazo)
        if fatal and seguranca > fatal:
            raise Falha("%s com data de segurança (%s) depois da fatal (%s): a conta precisa ser refeita" % (id_prazo, seguranca, fatal))
        data_ag = seguranca
        titulo = "%sPRAZO %s: %s (meta; fatal %s)" % (prefixo, quem, prov, fatal.isoformat() if fatal else "a confirmar")
        descr += [
            "Data de segurança (a meta, este compromisso): %s" % seguranca.isoformat(),
            "Data fatal (o limite, nunca a meta): %s" % (fatal.isoformat() if fatal else "[A CONFIRMAR]"),
            "Providência: %s" % prov,
            "Responsável: %s" % (r.get("responsavel") or "[A PREENCHER]"),
            "Conta: %s dias %s; regra %s; publicada %s; início %s%s" % (
                r.get("dias") or "?", r.get("contagem") or "?", r.get("regra") or "?",
                r.get("publicada_em") or "?", r.get("inicio") or "?",
                "; em dobro" if chave(r.get("em_dobro")) == "sim" else ""),
        ]
    descr.append("Dupla conferência: %s%s" % (r.get("conferido_por"), " em " + r["conferido_em"] if r.get("conferido_em") else ""))
    if a.com_processo and r.get("processo"):
        descr.append("Processo: %s" % r["processo"])
    descr.append("Prazo %s%s" % (id_prazo, "; publicação " + r["publicacao_id"] if r.get("publicacao_id") else ""))
    if obs:
        descr.append("Observação: %s" % obs)
    descr.append("Prazo mudou? Gere de novo pelo mesmo id: o compromisso é atualizado, não duplicado.")

    # lembretes
    alarmes = []
    datas_lembrete = []
    lista = a.lista_lembretes if a.lista_lembretes is not None else [(0, True)]
    hora_lembrete = a.hora_lembrete_t
    for n, uteis in lista:
        dlem = recuar(data_ag, n, uteis, calendario, tribunal)
        if dlem < hoje:
            avisos.append("%s: o lembrete de %d dia(s) antes cairia em %s, que já passou; ficou de fora" % (id_prazo, n, dlem))
            continue
        if hora and dlem == data_ag and hora_lembrete >= hora:
            gatilho = utc(data_ag, (dt.datetime.combine(data_ag, hora) - dt.timedelta(hours=1)).time())
        else:
            gatilho = utc(dlem, hora_lembrete)
        datas_lembrete.append(dlem.isoformat())
        texto_al = "Lembrete (%s): %s" % ("no dia" if n == 0 else "%d dia(s) %s antes" % (n, "úteis" if uteis else "corridos"), titulo)
        alarmes.append(["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:%s" % escapar(texto_al),
                        "TRIGGER;VALUE=DATE-TIME:%s" % gatilho, "END:VALARM"])

    if tipo in TIPOS_COM_HORA and a.preparacao is not None:
        dprep = recuar(data_ag, a.preparacao, True, calendario, tribunal)
        if dprep < hoje:
            avisos.append("%s: a preparação do cliente (%d dias úteis antes) cairia em %s, que já passou: a preparação é agora" % (id_prazo, a.preparacao, dprep))
            dprep = hoje
        datas_lembrete.append("preparação " + dprep.isoformat())
        texto_al = "Preparar o cliente (%d dias úteis antes): orientação, o que levar e, se for por vídeo, o teste da sala. %s" % (a.preparacao, titulo)
        alarmes.append(["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:%s" % escapar(texto_al),
                        "TRIGGER;VALUE=DATE-TIME:%s" % utc(dprep, hora_lembrete), "END:VALARM"])
        descr.insert(-1, "Preparação do cliente: até %s" % dprep.isoformat())

    partes_ass = [data_ag.isoformat(), hora.isoformat() if hora else "", titulo, "\n".join(descr), "|".join(datas_lembrete)]
    ass = assinatura(partes_ass)
    uid = "%s@motor-controladoria" % id_prazo.lower()
    bloco = ["BEGIN:VEVENT", "UID:%s" % uid, "DTSTAMP:%s" % agora_utc]
    if hora:
        fim = dt.datetime.combine(data_ag, hora) + dt.timedelta(minutes=a.duracao_min)
        bloco += ["DTSTART;TZID=%s:%s" % (TZID, dt.datetime.combine(data_ag, hora).strftime("%Y%m%dT%H%M%S")),
                  "DTEND;TZID=%s:%s" % (TZID, fim.strftime("%Y%m%dT%H%M%S"))]
    else:
        bloco += ["DTSTART;VALUE=DATE:%s" % data_ag.strftime("%Y%m%d"),
                  "DTEND;VALUE=DATE:%s" % (data_ag + dt.timedelta(days=1)).strftime("%Y%m%d")]
    bloco += ["SUMMARY:%s" % escapar(titulo), "DESCRIPTION:%s" % escapar("\n".join(descr))]
    if tipo in TIPOS_COM_HORA:
        bloco.append("LOCATION:%s" % escapar(ler_link(obs) or {"videoconferencia": "videoconferência"}.get(ler_modalidade(obs), ler_modalidade(obs)) or "local a confirmar"))
    bloco += ["CATEGORIES:%s" % {"audiencia": "Audiência", "pericia": "Perícia", "sessao": "Sessão"}.get(tipo, "Prazo"),
              "STATUS:CONFIRMED", "TRANSP:OPAQUE"]
    resumo = {
        "id": id_prazo, "tipo": tipo, "codigo_caso": codigo, "data_compromisso": data_ag.isoformat(),
        "hora": hora.strftime("%H:%M") if hora else "", "fatal": fatal.isoformat() if fatal else "",
        "seguranca": seguranca.isoformat() if seguranca else "", "lembretes": datas_lembrete,
        "titulo": titulo, "uid": uid,
    }
    return bloco, alarmes, ass, resumo, avisos


def gerar(a):
    pl = Planilha(a.prazos)
    pl.exigir(COLUNAS_OBRIGATORIAS)
    hoje = ler_data(a.hoje, "--hoje") if a.hoje else dt.date.today()
    agora_utc = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    calendario, avisos = ler_calendarios(a.calendario)
    if not a.calendario:
        avisos.append("sem --calendario: os lembretes em dias úteis pulam só sábados e domingos")
    pubs = ler_publicacoes(a.publicacoes)
    if a.calendario and not a.publicacoes:
        avisos.append("sem --publicacoes: o tribunal de cada prazo não é conhecido, só os dias 'todos' do calendário valem nos lembretes")
    a.lista_lembretes = ler_lembretes(a.lembretes)
    if a.lista_lembretes is None:
        avisos.append("lembretes da ficha não informados (--lembretes): só o lembrete do dia")
    h, m = (a.hora_lembrete.split(":") + ["0"])[:2]
    a.hora_lembrete_t = dt.time(int(h), int(m))

    pedidos = None
    if a.id:
        pedidos = [p.strip() for p in a.id.split(",") if p.strip()]
        existentes = {r["id"] for r in pl.linhas}
        nao_achados = [p for p in pedidos if p not in existentes]
        if nao_achados:
            raise Falha("Não achei no prazos.csv: %s" % ", ".join(nao_achados))

    os.makedirs(a.saida, exist_ok=True)
    resultado = {"pessoa_agora": [], "gerados": [], "sem_mudanca": [], "cancelados": [],
                 "recusados": [], "avisos": avisos, "lidas": len(pl.linhas), "arquivo_do_dia": "", "importar": []}
    blocos_do_dia = []
    fuso_do_dia = False
    mudou_csv = False

    for r in pl.linhas:
        id_prazo = r.get("id", "")
        status = chave(r.get("status"))
        pub = pubs.get(r.get("publicacao_id", ""), {})
        tribunal = pub.get("tribunal", "")
        # PESSOA AGORA vem antes de tudo, em qualquer status aberto
        if status not in STATUS_FECHADOS:
            try:
                limite = proximo_dia_util(hoje, calendario, tribunal)
                for rotulo, campo in (("seguranca", "data_seguranca"), ("fatal", "vencimento")):
                    d = ler_data(r.get(campo), campo)
                    if d and d <= limite:
                        quando = "hoje" if d == hoje else ("já passou" if d < hoje else "amanhã (próximo dia útil)")
                        resultado["pessoa_agora"].append("%s %s (%s): %s %s %s, status %s" % (
                            id_prazo, r.get("codigo_caso", ""), r.get("providencia", ""), rotulo, d.isoformat(), quando, status))
                        break
            except Falha as e:
                resultado["avisos"].append(str(e))
        if pedidos is not None and id_prazo not in pedidos:
            continue
        arquivo = os.path.join(a.saida, nome_arquivo(id_prazo))
        if status == "cancelado" and a.cancelados:
            ex = ler_existente(arquivo)
            if ex is None:
                continue
            if ex["assinatura"] == "cancelado":
                resultado["sem_mudanca"].append({"id": id_prazo, "motivo": "cancelamento já gerado"})
                continue
            bloco = ["BEGIN:VEVENT", "UID:%s@motor-controladoria" % id_prazo.lower(), "DTSTAMP:%s" % agora_utc,
                     "SEQUENCE:%d" % (ex["sequencia"] + 1), "STATUS:CANCELLED", "X-MOTOR-ASSINATURA:cancelado"]
            antigo = open(arquivo, encoding="utf-8").read()
            dtstart = re.search(r"^DTSTART[^\r\n]*", antigo, re.M)
            bloco.insert(3, dtstart.group(0) if dtstart else "DTSTART;VALUE=DATE:%s" % hoje.strftime("%Y%m%d"))
            bloco += ["SUMMARY:%s" % escapar("CANCELADO: " + (r.get("providencia") or id_prazo)), "END:VEVENT"]
            guardar_anterior(arquivo, ex["sequencia"])
            texto = montar_calendario([bloco], "TZID=" in bloco[3], "Prazos")
            texto = texto.replace("METHOD:PUBLISH", "METHOD:CANCEL")
            open(arquivo, "w", encoding="utf-8", newline="").write(texto)
            resultado["cancelados"].append({"id": id_prazo, "arquivo": arquivo})
            continue
        if status not in STATUS_AGENDAVEIS:
            if status == "sugerido":
                motivo = ("sugerido: falta a dupla conferência (dupla-conferencia). "
                          "Nada sugerido entra na agenda; na dúvida, a data mais cedo fica no resumo, não na agenda")
            elif status in STATUS_FECHADOS:
                motivo = "%s: prazo fechado, não vai para a agenda" % status
            else:
                motivo = "status %r desconhecido: só conferido ou agendado entram" % r.get("status")
            if pedidos is not None or status == "sugerido":
                resultado["recusados"].append({"id": id_prazo, "motivo": motivo})
            continue
        ok, motivo = conferencia_completa(r.get("conferido_por"))
        if not ok:
            resultado["recusados"].append({"id": id_prazo, "motivo": motivo})
            continue
        try:
            bloco, alarmes, ass, resumo, av = montar_compromisso(r, a, pub, calendario, hoje, agora_utc)
        except Falha as e:
            resultado["recusados"].append({"id": id_prazo, "motivo": str(e)})
            continue
        resultado["avisos"] += av
        ex = ler_existente(arquivo)
        seq = 0
        if ex is not None:
            if ex["assinatura"] == ass:
                resumo["arquivo"] = arquivo
                resultado["sem_mudanca"].append(resumo)
                if a.do_dia:
                    blocos_do_dia.append(open(arquivo, encoding="utf-8").read())
                if status == "conferido":
                    resultado["importar"].append({"id": id_prazo, "arquivo": arquivo})
                continue
            seq = ex["sequencia"] + 1
        bloco_final = bloco + ["SEQUENCE:%d" % seq, "X-MOTOR-ASSINATURA:%s" % ass]
        for al in alarmes:
            bloco_final += al
        bloco_final.append("END:VEVENT")
        com_fuso = bool(resumo["hora"])
        texto = montar_calendario([bloco_final], com_fuso, "Prazos")
        erros = validar_ics(texto)
        if erros:
            raise Falha("O .ics de %s saiu inválido: %s" % (id_prazo, "; ".join(erros)))
        if ex is not None:
            guardar_anterior(arquivo, ex["sequencia"])
            resumo["remarcado"] = "sequência %d para %d" % (ex["sequencia"], seq)
            resultado["avisos"].append("%s remarcado na agenda: confirme que a data nova passou pela conferência (conferido_em %s)" % (
                id_prazo, r.get("conferido_em") or "vazio"))
        open(arquivo, "w", encoding="utf-8", newline="").write(texto)
        resumo["arquivo"] = arquivo
        resultado["gerados"].append(resumo)
        if a.do_dia:
            blocos_do_dia.append(bloco_final)
            fuso_do_dia = fuso_do_dia or com_fuso
        # gerar o .ics não muda o status: agendado só quando a pessoa diz que importou (--importado)
        resultado["importar"].append({"id": id_prazo, "arquivo": arquivo, "remarcado": ex is not None})
        if a.gravar:
            nota = ".ics %s em %s (seq %d): importar na agenda" % ("atualizado" if ex is not None else "gerado", hoje.isoformat(), seq)
            if "observacao" in r:
                r["observacao"] = (r["observacao"] + "; " if r["observacao"] else "") + nota
            if "atualizado_em" in r:
                r["atualizado_em"] = hoje.isoformat()
            mudou_csv = True

    if a.do_dia and blocos_do_dia:
        blocos = []
        for b in blocos_do_dia:
            if isinstance(b, str):
                desdobrado = re.sub(r"\r\n[ \t]", "", b)
                m = re.search(r"BEGIN:VEVENT.*?END:VEVENT", desdobrado, re.S)
                blocos.append(m.group(0).split("\r\n"))
                fuso_do_dia = fuso_do_dia or "TZID=" in m.group(0)
            else:
                blocos.append(b)
        caminho_dia = os.path.join(a.saida, "%s.ics" % hoje.isoformat())
        texto = montar_calendario(blocos, fuso_do_dia, "Prazos do dia %s" % hoje.isoformat())
        erros = validar_ics(texto)
        if erros:
            raise Falha("O .ics do dia saiu inválido: %s" % "; ".join(erros))
        open(caminho_dia, "w", encoding="utf-8", newline="").write(texto)
        resultado["arquivo_do_dia"] = caminho_dia
    if mudou_csv:
        pl.gravar()
    resultado["csv_gravado"] = mudou_csv
    if pedidos is not None and [x for x in resultado["recusados"] if x["id"] in pedidos]:
        resultado["codigo"] = 1
    else:
        resultado["codigo"] = 0
    return resultado


def marcar_importado(a):
    """--importado: a pessoa disse que importou o .ics (ou o conector de agenda confirmou). Só aí vira agendado."""
    pl = Planilha(a.prazos)
    pl.exigir(COLUNAS_OBRIGATORIAS)
    hoje = ler_data(a.hoje, "--hoje") if a.hoje else dt.date.today()
    alvo = a.importado.strip()
    todos = chave(alvo) == "todos"
    pedidos = [] if todos else [p.strip() for p in alvo.split(",") if p.strip()]
    existentes = {r["id"] for r in pl.linhas}
    nao_achados = [p for p in pedidos if p not in existentes]
    if nao_achados:
        raise Falha("Não achei no prazos.csv: %s" % ", ".join(nao_achados))
    res = {"agendados": [], "ja_agendados": [], "recusados": [], "lidas": len(pl.linhas)}
    mudou = False
    for r in pl.linhas:
        id_prazo = r.get("id", "")
        if not todos and id_prazo not in pedidos:
            continue
        status = chave(r.get("status"))
        arquivo = os.path.join(a.saida, nome_arquivo(id_prazo))
        if status == "agendado":
            if not todos:
                res["ja_agendados"].append(id_prazo)
            continue
        if status != "conferido":
            if not todos:
                res["recusados"].append({"id": id_prazo, "motivo": "status %s: só conferido com o .ics gerado vira agendado" % (status or "vazio")})
            continue
        ok, motivo = conferencia_completa(r.get("conferido_por"))
        if not ok:
            res["recusados"].append({"id": id_prazo, "motivo": motivo})
            continue
        if not os.path.isfile(arquivo):
            if not todos:
                res["recusados"].append({"id": id_prazo, "motivo": "não há .ics gerado em %s: gere antes de dizer que importou" % arquivo})
            continue
        r["status"] = "agendado"
        nota = "importado na agenda em %s (%s)" % (hoje.isoformat(), a.origem_importacao)
        if "observacao" in r:
            r["observacao"] = (r["observacao"] + "; " if r["observacao"] else "") + nota
        if "atualizado_em" in r:
            r["atualizado_em"] = hoje.isoformat()
        res["agendados"].append(id_prazo)
        mudou = True
    if mudou:
        pl.gravar()
    res["codigo"] = 1 if res["recusados"] else 0
    return res


def guardar_anterior(arquivo, sequencia):
    pasta = os.path.join(os.path.dirname(arquivo), "anteriores")
    os.makedirs(pasta, exist_ok=True)
    base = os.path.basename(arquivo)[:-4]
    shutil.move(arquivo, os.path.join(pasta, "%s-seq%d.ics" % (base, sequencia)))


def imprimir(res):
    if res["pessoa_agora"]:
        print("PESSOA AGORA (vence hoje ou no próximo dia útil, em qualquer status):")
        for l in res["pessoa_agora"]:
            print("  - " + l)
        print()
    print("Agenda: %d gerado(s) ou atualizado(s), %d sem mudança, %d cancelado(s), %d recusado(s). Linhas lidas: %d." % (
        len(res["gerados"]), len(res["sem_mudanca"]), len(res["cancelados"]), len(res["recusados"]), res["lidas"]))
    for g in res["gerados"]:
        limite = "data do ato" if g["tipo"] in TIPOS_COM_HORA else "fatal %s" % (g["fatal"] or "a confirmar")
        print("  + %s · %s · %s%s · %s · lembretes %s%s · %s" % (
            g["id"], g["tipo"], g["data_compromisso"], " " + g["hora"] if g["hora"] else "",
            limite, ", ".join(g["lembretes"]) or "nenhum",
            " · remarcado (" + g["remarcado"] + ")" if g.get("remarcado") else "", g["arquivo"]))
    for g in res["sem_mudanca"]:
        print("  = %s · sem mudança desde o último arquivo" % g["id"])
    for g in res["cancelados"]:
        print("  x %s · cancelamento gerado · %s" % (g["id"], g["arquivo"]))
    if res["recusados"]:
        print("Recusados (não vão para a agenda):")
        for x in res["recusados"]:
            print("  - %s · %s" % (x["id"], x["motivo"]))
    if res["arquivo_do_dia"]:
        print("Arquivo do dia: %s" % res["arquivo_do_dia"])
    if res["lidas"] == 0:
        print("O prazos.csv só tem a linha de títulos: nenhum prazo registrado ainda.")
    elif not res["gerados"] and not res["sem_mudanca"] and not res["cancelados"]:
        print("Nenhum prazo conferido sem agenda nesta leitura.")
    if res["avisos"]:
        print("Avisos:")
        for av in res["avisos"]:
            print("  ! " + av)
    if res.get("importar"):
        print("Importar na agenda (o status continua conferido até a pessoa dizer que importou; depois: --importado <id ou todos>):")
        for x in res["importar"]:
            print("  > %s · %s%s" % (x["id"], x["arquivo"], " · remarcação: importar o arquivo novo por cima do antigo" if x.get("remarcado") else ""))
    if res.get("csv_gravado"):
        print("prazos.csv atualizado: só a observacao (.ics gerado, importar na agenda) e atualizado_em. O status não muda aqui.")


def main():
    p = argparse.ArgumentParser(description="Gera .ics dos prazos conferidos (agenda-de-prazos).")
    p.add_argument("prazos", nargs="?", help="caminho do prazos.csv")
    p.add_argument("--saida", help="pasta da agenda (escritorio/07-operacao/controladoria/agenda)")
    p.add_argument("--id", help="um ou mais ids separados por virgula")
    p.add_argument("--lembretes", help="dias úteis antes da data do compromisso, ex.: \"5,2,0\" (ficha: lembretes)")
    p.add_argument("--hora-lembrete", default="08:00")
    p.add_argument("--calendario", help="calendário do tribunal (arquivo ou pasta) para contar os lembretes em dias úteis")
    p.add_argument("--publicacoes", help="publicacoes.csv, para saber o tribunal de cada prazo")
    p.add_argument("--do-dia", action="store_true", help="também grava um arquivo AAAA-MM-DD.ics com os compromissos desta rodada")
    p.add_argument("--cancelados", action="store_true", help="gera o cancelamento dos prazos cancelados que já tinham .ics")
    p.add_argument("--com-processo", action="store_true", help="põe o número do processo no texto (o padrão é não pôr)")
    p.add_argument("--duracao-min", type=int, default=60)
    p.add_argument("--preparacao", type=int, help="audiência, perícia e sessão: lembrete de preparação do cliente N dias úteis antes (ficha da experiência: cadencia_da_preparacao)")
    p.add_argument("--hoje")
    p.add_argument("--treino", action="store_true")
    p.add_argument("--gravar", action="store_true", help="anota na observacao que o .ics foi gerado (o status não muda)")
    p.add_argument("--importado", metavar="ID|todos", help="a pessoa disse que importou (ou o conector confirmou): conferido com .ics vira agendado")
    p.add_argument("--origem-importacao", dest="origem_importacao", default="a pessoa confirmou na conversa",
                   help="quem confirmou a importação, para a observacao (ex.: \"conector de agenda\")")
    p.add_argument("--json", action="store_true")
    p.add_argument("--validar", nargs="+", metavar="ICS", help="só valida a estrutura de arquivos .ics")
    a = p.parse_args()
    try:
        if a.validar:
            ruim = 0
            for arq in a.validar:
                if not os.path.isfile(arq):
                    print("%s: não achei o arquivo" % arq)
                    ruim += 1
                    continue
                erros = validar_ics(open(arq, encoding="utf-8", newline="").read(), arq)
                print("%s: %s" % (arq, "ok" if not erros else "; ".join(erros)))
                ruim += bool(erros)
            sys.exit(1 if ruim else 0)
        if not a.prazos or not a.saida:
            raise Falha("Informe o prazos.csv e a pasta --saida. Exemplo: python3 gerar_ics.py "
                        "escritorio/07-operacao/controladoria/prazos.csv --saida escritorio/07-operacao/controladoria/agenda")
        if a.importado:
            res = marcar_importado(a)
            if a.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print("Agendados agora (a pessoa disse que importou): %s" % (", ".join(res["agendados"]) or "nenhum"))
                if res["ja_agendados"]:
                    print("Já estavam agendados: %s" % ", ".join(res["ja_agendados"]))
                for x in res["recusados"]:
                    print("  - %s · %s" % (x["id"], x["motivo"]))
                if res["agendados"]:
                    print("prazos.csv atualizado: conferido vira agendado, com observacao e atualizado_em.")
            sys.exit(res["codigo"])
        res = gerar(a)
    except Falha as e:
        print("ERRO: %s" % e, file=sys.stderr)
        sys.exit(1)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        imprimir(res)
    sys.exit(res["codigo"])


if __name__ == "__main__":
    main()
