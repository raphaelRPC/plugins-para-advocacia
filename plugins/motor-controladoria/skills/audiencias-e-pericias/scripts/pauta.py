#!/usr/bin/env python3
"""A pauta de audiências, perícias e sessões do prazos.csv, com o que falta em cada uma.

Parte da habilidade audiencias-e-pericias do motor-controladoria.

Lista as linhas com tipo audiencia, pericia ou sessao que não estão fechadas,
dos próximos N dias (e as que já passaram sem baixa), e aponta: hoje ou no
próximo dia útil (PESSOA AGORA), sem hora, sem local ou link, ainda sugerida
(falta a conferência), conferida e sem agenda, por vídeo (teste da sala),
perícia (quesitos e assistente técnico para o advogado conferir) e, com
--escritorio, se o aviso para a preparação do cliente já foi encaminhado.

Uso:
  python3 pauta.py prazos.csv [--hoje AAAA-MM-DD] [--dias 15] [--escritorio escritorio] [--treino] [--json]

Códigos de saída: 0 ok; 1 erro (arquivo ou coluna que falta, data ilegível).
Python 3.9+, só biblioteca padrão.
"""

import argparse
import csv
import datetime as dt
import glob
import io
import json
import os
import re
import sys
import unicodedata

TIPOS = {"audiencia": "audiência", "pericia": "perícia", "sessao": "sessão"}
FECHADOS = {"cumprido", "perdido", "cancelado"}
COLUNAS = ["id", "codigo_caso", "tipo", "providencia", "vencimento", "responsavel", "status", "observacao"]


class Falha(Exception):
    pass


def chave(texto):
    nfkd = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c)).strip().lower()


def ler_csv(caminho):
    if not os.path.isfile(caminho):
        raise Falha("Não achei o arquivo %s. O registro fica em escritorio/07-operacao/controladoria/prazos.csv." % caminho)
    bruto = open(caminho, "rb").read()
    texto = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if texto is None or not texto.strip():
        raise Falha("O arquivo %s está vazio: falta ao menos a linha de títulos." % caminho)
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    linhas = list(csv.reader(io.StringIO(texto), delimiter=sep))
    chaves = [chave(t) for t in linhas[0]]
    faltam = [c for c in COLUNAS if c not in chaves]
    if faltam:
        raise Falha("Faltam colunas em %s: %s. A linha de títulos certa está em docs/prazos.md." % (caminho, ", ".join(faltam)))
    saida = []
    for crua in linhas[1:]:
        if any(c.strip() for c in crua):
            saida.append({k: (crua[i].strip() if i < len(crua) else "") for i, k in enumerate(chaves)})
    return saida


def ler_data(texto, campo):
    t = (texto or "").strip().split(" ")[0]
    if not t:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(t, fmt).date()
        except ValueError:
            continue
    raise Falha("Data que não entendi em %s: %r. Use AAAA-MM-DD ou DD/MM/AAAA." % (campo, texto))


def proximo_dia_util(d):
    d = d + dt.timedelta(days=1)
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def ler_hora(texto):
    t = chave(texto)
    m = re.search(r"(?<![\d/-])([01]?\d|2[0-3])\s*(?:h(?:oras?|s)?(?:\s*([0-5]\d))?(?![a-z\d])|:([0-5]\d)(?!\d))", t)
    if not m:
        return ""
    return "%02dh%s" % (int(m.group(1)), m.group(2) or m.group(3) or "00")


def ler_modalidade(texto):
    t = chave(texto)
    if re.search(r"video|virtual|telepresencial|on-?line|link|https?://", t):
        return "videoconferência"
    if re.search(r"presencial|forum|sala \w|endereco|predio|consultorio", t):
        return "presencial"
    return ""


LUGARES = r"sede|forum|sala|predio|endereco|rua|avenida|av\.|praca|juizado|vara|tribunal|consultorio|clinica|hospital|local|cejusc|posto"


def ler_local(texto):
    """O local ou o link escrito na observação (como está, até o próximo ponto e vírgula)."""
    t = texto or ""
    m = re.search(r"https?://\S+", t)
    if m:
        return m.group(0).rstrip(".,;)")
    esp = "".join(unicodedata.normalize("NFD", c)[0].lower() for c in t)
    m = re.search(r"\b(?:na|no|nas|nos|em)\s+(?:a\s+|o\s+)?(?:" + LUGARES + r")\b", esp)
    if not m:
        m = re.search(r"\b(?:local|endereco|sala)\s*:\s*", esp)
    if not m:
        return ""
    fim = t.find(";", m.start())
    return t[m.start():fim if fim >= 0 else len(t)].strip().rstrip(".,")


def aviso_encaminhado(escritorio, treino, id_prazo):
    base = os.path.join(escritorio, "07-operacao", "_treino" if treino else "", "experiencia", "entrada")
    padroes = ["*-controladoria-%s-*.md" % id_prazo.lower()]
    achados = []
    for pad in padroes:
        achados += glob.glob(os.path.join(base, pad))
        achados += glob.glob(os.path.join(base, "lidos", "*", pad))
    return sorted(achados)


def montar(a):
    linhas = ler_csv(a.prazos)
    hoje = ler_data(a.hoje, "--hoje") if a.hoje else dt.date.today()
    ate = hoje + dt.timedelta(days=a.dias)
    limite = proximo_dia_util(hoje)
    pauta, pessoa_agora, passadas = [], [], []
    for r in linhas:
        tipo = chave(r.get("tipo"))
        status = chave(r.get("status"))
        if tipo not in TIPOS or status in FECHADOS:
            continue
        data = ler_data(r.get("vencimento"), "vencimento de " + r.get("id", "?"))
        obs = r.get("observacao", "")
        item = {
            "id": r["id"], "codigo_caso": r.get("codigo_caso", ""), "cliente_curto": r.get("cliente_curto", ""),
            "tipo": TIPOS[tipo], "data": data.isoformat() if data else "", "hora": ler_hora(obs),
            "modalidade": ler_modalidade(obs), "local": ler_local(obs), "responsavel": r.get("responsavel", ""), "status": status,
            "o_que_falta": [],
        }
        if item["local"] and not item["modalidade"]:
            item["modalidade"] = "presencial"
        f = item["o_que_falta"]
        if not data:
            f.append("data do ato [A CONFIRMAR]")
        if not item["hora"]:
            f.append("hora [A CONFIRMAR] (não está na observação)")
        if not item["modalidade"] and not item["local"]:
            f.append("local ou link [A CONFIRMAR] (não está na observação)")
        elif item["modalidade"] == "videoconferência" and not item["local"]:
            f.append("link da sala virtual [A CONFIRMAR] (a observação diz videoconferência, sem o link)")
        if status == "sugerido":
            f.append("conferir a data, a hora e o tipo do ato (dupla-conferencia) antes de agendar e de avisar o cliente")
        elif status == "conferido":
            f.append("conferida e sem agenda: agenda-de-prazos")
        if item["modalidade"] == "videoconferência":
            f.append("teste do link e da sala virtual com o cliente antes do dia")
        if tipo == "pericia":
            f.append("quesitos e assistente técnico: o advogado confere no processo [CONFERIR]")
        if tipo == "audiencia":
            f.append("testemunhas e documentos: o advogado decide quem e o quê [CONFERIR]")
        if not item["responsavel"]:
            f.append("sem responsável")
        if a.escritorio:
            enc = aviso_encaminhado(a.escritorio, a.treino, r["id"])
            item["aviso_ao_cliente"] = enc[0] if enc else ""
            if not enc:
                f.append("aviso para a preparação do cliente ainda não encaminhado (encaminhar-providencia)")
        if data and data < hoje:
            passadas.append(item)
            continue
        if data and data <= limite:
            pessoa_agora.append(item)
        if not data or data <= ate:
            pauta.append(item)
    pauta.sort(key=lambda x: (x["data"] or "9999", x["hora"]))
    return {"hoje": hoje.isoformat(), "ate": ate.isoformat(), "pessoa_agora": pessoa_agora,
            "pauta": pauta, "passadas_sem_baixa": passadas, "lidas": len(linhas)}


def imprimir(res):
    if res["pessoa_agora"]:
        print("PESSOA AGORA (hoje ou no próximo dia útil):")
        for i in res["pessoa_agora"]:
            print("  - %s %s %s: %s %s · %s" % (i["id"], i["codigo_caso"], i["tipo"], i["data"], i["hora"] or "hora a confirmar", i["status"]))
        print()
    print("Pauta de %s até %s: %d compromisso(s). Linhas lidas: %d." % (res["hoje"], res["ate"], len(res["pauta"]), res["lidas"]))
    for i in res["pauta"]:
        print("  %s %s · %s · %s %s · %s · %s · %s" % (
            i["data"] or "sem data", i["hora"] or "--h--", i["tipo"], i["codigo_caso"], i["cliente_curto"],
            (i["modalidade"] + (": " + i["local"] if i.get("local") else "")) if i["modalidade"] or i.get("local") else "local a confirmar",
            i["responsavel"] or "sem responsável", i["status"]))
        for f in i["o_que_falta"]:
            print("      - " + f)
    if res["passadas_sem_baixa"]:
        print("Já passaram e não têm baixa (cumprido, cancelado ou redesignado: a pessoa diz):")
        for i in res["passadas_sem_baixa"]:
            print("  - %s %s %s em %s · %s" % (i["id"], i["codigo_caso"], i["tipo"], i["data"], i["status"]))
    if res["lidas"] == 0:
        print("O prazos.csv só tem a linha de títulos: nenhum compromisso registrado ainda.")
    elif not res["pauta"] and not res["passadas_sem_baixa"]:
        print("Nenhuma audiência, perícia ou sessão aberta no período.")


def main():
    p = argparse.ArgumentParser(description="Pauta de audiências, perícias e sessões (audiencias-e-pericias).")
    p.add_argument("prazos")
    p.add_argument("--hoje")
    p.add_argument("--dias", type=int, default=15)
    p.add_argument("--escritorio")
    p.add_argument("--treino", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    try:
        res = montar(a)
    except Falha as e:
        print("ERRO: %s" % e, file=sys.stderr)
        sys.exit(1)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        imprimir(res)


if __name__ == "__main__":
    main()
