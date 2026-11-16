#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditoria_prazos.py · a auditoria do mês dos prazos do escritório.

  python3 auditoria_prazos.py <prazos.csv> --mes AAAA-MM
      [--conferencias <pasta conferencias/>] [--hoje AAAA-MM-DD] [--treino] [--saida <arquivo.md>]

Lê prazos.csv e, se houver, os registros de conferência do mês (conferencias/AAAA-MM-DD.md) e
mostra: prazos cumpridos no mês contra a data de segurança e a fatal (antes da segurança, na
segurança, entre a segurança e a fatal, no último dia, depois da fatal), perdidos, vencidos sem
registro de cumprimento, prazos que andaram sem a dupla conferência, conferências que
divergiram e sugestões da IA que a pessoa corrigiu, por responsável.

Treino (pasta _treino/) só entra com --treino, e o relatório sai marcado como treino.
Códigos de saída: 0 auditoria feita; 1 erro (arquivo, coluna, mês); 2 achou o que exige ação
agora (vencido sem registro, cumprido depois da fatal, prazo andando sem dupla conferência).
Só biblioteca padrão. Python 3.9 ou mais novo.
"""

import argparse
import calendar
import csv
import datetime as dt
import io
import os
import re
import sys
import unicodedata


class Erro(Exception):
    pass


def normal(t):
    t = unicodedata.normalize("NFKD", str(t or ""))
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.strip().lower())


def ler_data(s):
    s = (s or "").strip()
    if not s:
        return None
    s = s.split(" ")[0]
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    try:
        if m:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if m:
            return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None
    return None


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            continue
    return bruto.decode("latin-1")


def ler_prazos(caminho):
    if not os.path.isfile(caminho):
        raise Erro("arquivo não encontrado: %s" % caminho)
    texto = ler_texto(caminho)
    if not texto.strip():
        raise Erro("prazos.csv está vazio: %s" % caminho)
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    mapa = {c: normal(c).replace(" ", "_") for c in (leitor.fieldnames or [])}
    obrig = ["id", "tipo", "status", "vencimento", "data_seguranca", "cumprido_em", "conferido_por", "responsavel"]
    faltam = [c for c in obrig if c not in mapa.values()]
    if faltam:
        raise Erro("prazos.csv (%s) sem as colunas obrigatórias: %s." % (caminho, ", ".join(faltam)))
    linhas = [{mapa[k]: (v or "").strip() for k, v in l.items() if k in mapa} for l in leitor]
    if not linhas:
        raise Erro("prazos.csv não tem nenhuma linha de prazo: não há o que auditar (%s)." % caminho)
    return linhas


def ler_conferencias(pasta, ini, fim):
    linhas = []
    arquivos = []
    if not pasta:
        return linhas, arquivos
    if not os.path.isdir(pasta):
        raise Erro("pasta de conferências não encontrada: %s" % pasta)
    for nome in sorted(os.listdir(pasta)):
        m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\.md", nome)
        if not m:
            continue
        d = ler_data(m.group(1))
        if d is None or not (ini <= d <= fim):
            continue
        arquivos.append(nome)
        cab = None
        for l in ler_texto(os.path.join(pasta, nome)).splitlines():
            if not l.strip().startswith("|"):
                cab = None if l.strip().startswith("#") else cab
                continue
            partes = [p.strip().replace("`", "") for p in l.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", p) or p == "" for p in partes):
                continue
            norm = [normal(p) for p in partes]
            if "prazo_id" in norm and "resultado" in norm:
                cab = norm
                continue
            if cab is None:
                continue
            partes = partes + [""] * (len(cab) - len(partes))
            item = {cab[i]: partes[i] for i in range(len(cab))}
            if item.get("prazo_id", "").startswith("PZ-AAAA"):
                continue
            item["_arquivo"] = nome
            linhas.append(item)
    return linhas, arquivos


def dupla_ok(conferido_por):
    v = (conferido_por or "").strip()
    if not v:
        return False
    partes = [p.strip() for p in re.split(r"[;/]", v) if p.strip()]
    if len(partes) >= 2:
        return True
    return "2º turno" in v or "2o turno" in normal(v) or "segundo turno" in normal(v)


def main():
    ap = argparse.ArgumentParser(description="Auditoria do mês dos prazos.")
    ap.add_argument("prazos")
    ap.add_argument("--mes", required=True, help="AAAA-MM")
    ap.add_argument("--conferencias")
    ap.add_argument("--hoje")
    ap.add_argument("--treino", action="store_true")
    ap.add_argument("--saida")
    args = ap.parse_args()
    try:
        m = re.fullmatch(r"(\d{4})-(\d{2})", args.mes or "")
        if not m or not (1 <= int(m.group(2)) <= 12):
            raise Erro("--mes precisa ser AAAA-MM.")
        ano, mes = int(m.group(1)), int(m.group(2))
        ini = dt.date(ano, mes, 1)
        fim = dt.date(ano, mes, calendar.monthrange(ano, mes)[1])
        caminho_abs = os.path.abspath(args.prazos)
        eh_treino = "_treino" in caminho_abs.split(os.sep)
        if eh_treino and not args.treino:
            raise Erro("este prazos.csv está em _treino/: treino não entra na auditoria. Para testar, rode com --treino.")
        hoje = ler_data(args.hoje) if args.hoje else dt.date.today()
        if args.hoje and hoje is None:
            raise Erro("--hoje inválido: use AAAA-MM-DD.")
        linhas = ler_prazos(args.prazos)
        pasta_conf = args.conferencias
        if not pasta_conf:
            sugerida = os.path.join(os.path.dirname(caminho_abs), "conferencias")
            if os.path.isdir(sugerida):
                pasta_conf = sugerida
        confs, arqs_conf = ler_conferencias(pasta_conf, ini, fim)
    except Erro as ex:
        sys.stderr.write("ERRO: %s\n" % ex)
        return 1

    limite = min(hoje, fim)
    prazos = [l for l in linhas if normal(l.get("tipo")) == "prazo"]
    cumpridos, perdidos, vencidos, sem_dupla, depois, sem_data, sem_seg = [], [], [], [], [], [], []
    faixas = {"antes da segurança": [], "na segurança": [], "entre a segurança e a fatal": [], "no último dia": [], "depois da fatal": []}
    por_resp = {}
    for l in prazos:
        st = normal(l.get("status"))
        venc = ler_data(l.get("vencimento"))
        seg = ler_data(l.get("data_seguranca"))
        cump = ler_data(l.get("cumprido_em"))
        resp = l.get("responsavel") or "sem responsável"
        r = por_resp.setdefault(resp, {"cumpridos": 0, "ultimo_dia": 0, "perdidos": 0, "abertos_vencidos": 0})
        if st in ("conferido", "agendado", "cumprido") and not dupla_ok(l.get("conferido_por")):
            sem_dupla.append(l)
        if st == "cumprido":
            if cump is None:
                sem_data.append(l)
                continue
            if not (ini <= cump <= fim):
                continue
            cumpridos.append(l)
            r["cumpridos"] += 1
            if venc is None:
                sem_data.append(l)
                continue
            if seg is None:
                sem_seg.append(l)
            if cump > venc:
                faixas["depois da fatal"].append(l)
                depois.append(l)
            elif cump == venc:
                faixas["no último dia"].append(l)
                r["ultimo_dia"] += 1
            elif seg is not None and cump < seg:
                faixas["antes da segurança"].append(l)
            elif seg is not None and cump == seg:
                faixas["na segurança"].append(l)
            else:
                faixas["entre a segurança e a fatal"].append(l)
        elif st == "perdido":
            ref = venc or ler_data(l.get("atualizado_em"))
            if ref and ini <= ref <= fim:
                perdidos.append(l)
                r["perdidos"] += 1
        elif st in ("sugerido", "conferido", "agendado"):
            if venc and venc < limite:
                vencidos.append(l)
                r["abertos_vencidos"] += 1

    divergiu = [c for c in confs if normal(c.get("resultado")) == "divergiu"]
    decididas = [c for c in confs if normal(c.get("resultado")) == "decidida"]
    corrigidas = []
    for c in confs:
        s, f = ler_data(c.get("sugestao_ia")), ler_data(c.get("vencimento_final"))
        if s and f and s != f:
            corrigidas.append(c)
    corrigidas_obs = [l for l in prazos if "corrigido na conferencia" in normal(l.get("observacao"))
                      and ler_data(l.get("atualizado_em")) and ini <= ler_data(l.get("atualizado_em")) <= fim
                      and l["id"] not in set(c.get("prazo_id", "") for c in corrigidas)]

    L = []
    L.append("AUDITORIA DE PRAZOS · %s%s" % (args.mes, " · TREINO" if eh_treino else ""))
    L.append("Li %d linhas de prazos.csv (%d do tipo prazo) e %d registros de conferência do mês (%s)." % (
        len(linhas), len(prazos), len(confs), ", ".join(arqs_conf) or "nenhum arquivo de conferências do mês"))
    L.append("")
    acao = []
    for l in vencidos:
        acao.append("%s %s: venceu em %s e está como %s, sem registro de cumprimento. Foi cumprido? Perdido?" % (l["id"], l.get("codigo_caso", ""), l["vencimento"], l["status"]))
    for l in depois:
        acao.append("%s %s: cumprido em %s, depois da fatal (%s). Confira a data do protocolo e o que aconteceu." % (l["id"], l.get("codigo_caso", ""), l["cumprido_em"], l["vencimento"]))
    for l in sem_dupla:
        acao.append("%s %s: status %s sem os dois nomes da dupla conferência (conferido_por: '%s')." % (l["id"], l.get("codigo_caso", ""), l["status"], l.get("conferido_por", "")))
    if acao:
        L.append("PESSOA AGORA")
        for a in acao:
            L.append("  - %s" % a)
        L.append("")
    L.append("Cumpridos no mês: %d" % len(cumpridos))
    for k, v in faixas.items():
        pct = (100.0 * len(v) / len(cumpridos)) if cumpridos else 0.0
        L.append("  - %s: %d (%.0f%%)%s" % (k, len(v), pct, (" · " + ", ".join(x["id"] for x in v)) if v and k in ("no último dia", "depois da fatal") else ""))
    if sem_data:
        L.append("  - cumpridos sem cumprido_em ou sem vencimento: %d · %s" % (len(sem_data), ", ".join(x["id"] for x in sem_data)))
    if sem_seg:
        L.append("  - cumpridos sem data de segurança registrada: %d · %s" % (len(sem_seg), ", ".join(x["id"] for x in sem_seg)))
    L.append("Perdidos no mês: %d%s" % (len(perdidos), (" · " + ", ".join("%s (%s)" % (x["id"], x.get("observacao", "") or "sem nota") for x in perdidos)) if perdidos else ""))
    L.append("Vencidos sem registro de cumprimento: %d" % len(vencidos))
    L.append("Andando sem dupla conferência: %d" % len(sem_dupla))
    L.append("")
    L.append("Conferências do mês: %d · divergiram %d · decididas depois %d" % (len(confs), len(divergiu), len(decididas)))
    for c in divergiu:
        L.append("  - divergiu: %s %s · %s" % (c.get("prazo_id", ""), c.get("codigo_caso", ""), c.get("observacao", "") or "sem observação"))
    L.append("Sugestões da IA corrigidas pela pessoa: %d" % (len(corrigidas) + len(corrigidas_obs)))
    for c in corrigidas:
        L.append("  - %s %s: IA %s, valeu %s · %s" % (c.get("prazo_id", ""), c.get("codigo_caso", ""), c.get("sugestao_ia", ""), c.get("vencimento_final", ""), c.get("observacao", "")))
    for l in corrigidas_obs:
        L.append("  - %s %s: %s" % (l["id"], l.get("codigo_caso", ""), l.get("observacao", "")))
    L.append("")
    L.append("| responsável | cumpridos | no último dia | perdidos | vencidos sem registro |")
    L.append("|---|---|---|---|---|")
    for resp, r in sorted(por_resp.items()):
        if any(r.values()):
            L.append("| %s | %d | %d | %d | %d |" % (resp, r["cumpridos"], r["ultimo_dia"], r["perdidos"], r["abertos_vencidos"]))
    L.append("")
    L.append("Para discutir (a decisão é da pessoa):")
    if faixas["no último dia"] or faixas["depois da fatal"]:
        L.append("  - prazos cumpridos no último dia ou depois: a data de segurança está sendo usada como meta? Os lembretes chegam a tempo?")
    if divergiu or corrigidas or corrigidas_obs:
        L.append("  - o que fez a conferência divergir ou corrigir a IA se repete (tribunal, rito, tipo de ato, calendário)? Vira ajuste de regra ou aprendizado.")
    if perdidos:
        L.append("  - cada prazo perdido: o que aconteceu, em que passo (captação, triagem, conta, conferência, agenda, cumprimento) e o que muda.")
    if not (faixas["no último dia"] or faixas["depois da fatal"] or divergiu or corrigidas or corrigidas_obs or perdidos):
        L.append("  - nada fora do padrão nos números do mês. Vale olhar uma amostra dos cumpridos entre a segurança e a fatal.")
    rel = "\n".join(L)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)) or ".", exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(rel + "\n")
        print("Relatório gravado em %s" % args.saida)
    print(rel)
    return 2 if acao else 0


if __name__ == "__main__":
    sys.exit(main())
