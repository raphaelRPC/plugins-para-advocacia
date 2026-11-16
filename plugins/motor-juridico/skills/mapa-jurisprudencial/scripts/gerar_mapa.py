#!/usr/bin/env python3
"""Mapa jurisprudencial de um tema da base (motor-juridico, mapa-jurisprudencial).

Lê o arquivo do tema (04-base/juridico/jurisprudencia/<tema>.md, formato em
docs/pesquisa-jus-ia.md) e, se houver, a leitura aprovada pelo advogado
(04-base/juridico/mapas/<tema>-leitura.md: correntes, viradas, distinções, perguntas).
Monta:
  - os números do tema (a favor, contra, neutro; conferidos, não conferidos, vencidos);
  - como decide cada tribunal e cada órgão (a favor x contra x neutro);
  - a linha do tempo por ano e os sinais automáticos de mudança (marcados como sinal, não
    como conclusão);
  - os precedentes qualificados (súmula, tema, IRDR, IAC);
  - a lista dos julgados, com a situação da conferência e "não citar sem conferir".
Entrega em .md (--saida) e numa página HTML interna (--html), preenchendo o modelo
assets/mapa-modelo.html (responsivo, claro e escuro, sem nada externo).

Uso:
  python3 gerar_mapa.py TEMA.md [--leitura LEITURA.md] [--hoje AAAA-MM-DD] [--validade 90]
      [--ficha ficha-juridica.md] [--saida mapa.md] [--html mapa.html]
      [--modelo assets/mapa-modelo.html] [--nome-do-escritorio "Escritório Modelo"] [--treino]

Sai com código 1 e mensagem clara quando falta o arquivo, ele não tem ficha nenhuma, ou o tema
tem dado de cliente (código C-AAAA-NNNN ou CPF): a página é da base, e a base não guarda caso.
Só biblioteca padrão.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(os.path.dirname(AQUI), "assets", "mapa-modelo.html")


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def ler(caminho):
    if not os.path.isfile(caminho):
        erro("não encontrei '%s'." % caminho)
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod).lstrip("﻿")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_data(t):
    t = (t or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    return None


def frontmatter(linhas):
    fm, resto = {}, linhas
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for l in linhas[1:i]:
                    m = re.match(r"^([\w_]+)\s*:\s*(.*)$", l)
                    if m:
                        fm[m.group(1)] = m.group(2).strip()
                resto = linhas[i + 1:]
                break
    return fm, resto


def ler_tema(texto):
    fm, corpo = frontmatter(texto.splitlines())
    titulo, resumo, fichas, secao, atual = "", [], [], "", None
    for l in corpo:
        if l.startswith("# ") and not titulo:
            titulo = l[2:].strip()
            continue
        if l.startswith("## "):
            t = sem_acento(l[3:].lower())
            secao = "resumo" if t.startswith("como o tema") else ("julgados" if t.startswith("julgados") else ("historico" if t.startswith("historico") else "outra"))
            atual = None
            continue
        if l.startswith("### "):
            atual = {"titulo": l[4:].strip(), "partes": [p.strip() for p in re.split(r"\s+·\s+|\s+\|\s+", l[4:].strip())], "campos": {}}
            fichas.append(atual)
            continue
        if atual is not None:
            m = re.match(r"^\s*-\s*([^:]{2,80}):\s*(.*)$", l)
            if m:
                atual["campos"][sem_acento(m.group(1).strip().lower())] = m.group(2).strip()
        elif secao == "resumo" and l.strip():
            resumo.append(l.strip())
    return fm, titulo, " ".join(resumo), fichas


def campo(c, inicio):
    for k, v in c.items():
        if k.startswith(inicio):
            return v
    return ""


def info(f, hoje, validade):
    p = f["partes"]
    c = f["campos"]
    d = {"tribunal": p[0] if p else "", "numero": p[1] if len(p) > 1 else "", "data_txt": p[2] if len(p) > 2 else ""}
    dt = ler_data(d["data_txt"])
    d["data"] = dt.isoformat() if dt else ""
    d["ano"] = dt.year if dt else None
    orel = campo(c, "orgao e relator")
    d["orgao"] = orel.split(";")[0].strip() if orel else ""
    d["orgao_relator"] = orel
    d["tese"] = campo(c, "tese em uma frase")
    serve = campo(c, "para que serve")
    s = sem_acento(serve.lower())
    d["posicao"] = "contra" if s.startswith("contra") else ("a favor" if s.startswith("a favor") else ("neutro" if s.startswith("neutro") else "sem posição"))
    d["serve"] = serve
    fonte = campo(c, "fonte")
    ml = re.search(r"https?://\S+", fonte)
    d["link"] = ml.group(0).rstrip(").,;") if ml else ""
    mp = re.search(r"pesquisa de (\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", fonte)
    pq = ler_data(mp.group(1)) if mp else None
    d["pesquisa"] = pq.isoformat() if pq else ""
    conf = campo(c, "conferencia no inteiro teor")
    mc = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", conf)
    cd = ler_data(mc.group(0)) if mc else None
    cor = "não conferido"
    cl = sem_acento(conf.lower())
    if cd and not re.search(r"verde\s*\|\s*amarelo", cl):
        for k in ("verde", "amarelo", "vermelho"):
            if re.search(r"\b%s\b" % k, cl):
                cor = k
    d["cor"] = cor
    d["conf_data"] = cd.isoformat() if cd else ""
    d["vencida"] = bool(cd and cor == "verde" and (hoje - cd).days > validade)
    d["situacao"] = campo(c, "situacao").replace("`", "") or "[CONFERIR]"
    num = d["numero"]
    d["qualificado"] = bool(re.search(r"S[úu]mula|Tema\s+\d|IRDR|IAC|repercuss[ãa]o geral|repetitivo|ADI|ADC|ADPF", num + " " + d["tese"], re.I))
    d["exemplo"] = "EXEMPLO" in f["titulo"] or any("EXEMPLO" in v for v in c.values())
    sit = sem_acento(d["situacao"].lower())
    # "pode citar" só para verde com data de conferência registrada, dentro da validade e vigente;
    # julgado de EXEMPLO (treino) nunca: os números são inventados (docs/casos-ficticios.md)
    d["pode_citar"] = bool(cd) and cor == "verde" and not d["vencida"] and sit.startswith("vigente") and not d["exemplo"]
    if cor == "vermelho" or re.match(r"superado\b(?! em parte)", sit):
        d["selo"] = "não usar"
    elif d["pode_citar"]:
        d["selo"] = "conferido"
    elif d["exemplo"] and cor == "verde":
        d["selo"] = "exemplo: número inventado, não citar"
    elif d["vencida"]:
        d["selo"] = "conferência vencida"
    elif cor == "amarelo" or "em parte" in sit:
        d["selo"] = "ajustar antes de usar"
    else:
        d["selo"] = "não conferido: não citar sem conferir"
    d["titulo"] = f["titulo"]
    return d


def validade_da_ficha(a, inicio):
    if a.validade:
        return a.validade, "opção --validade"
    ficha = a.ficha
    if not ficha:
        pasta = os.path.dirname(os.path.abspath(inicio))
        while True:
            for cand in (os.path.join(pasta, "04-base", "comum", "ficha-juridica.md"),
                         os.path.join(pasta, "escritorio", "04-base", "comum", "ficha-juridica.md")):
                if os.path.isfile(cand):
                    ficha = cand
            if ficha or os.path.dirname(pasta) == pasta:
                break
            pasta = os.path.dirname(pasta)
    if ficha and os.path.isfile(ficha):
        for l in ler(ficha).splitlines():
            m = re.match(r"^\s*-?\s*validade_da_conferencia\s*:\s*(.*)$", l)
            if m:
                v = m.group(1).split("(")[0]
                n = re.search(r"\d+", v)
                if n and "PREENCHER" not in v.upper():
                    return int(n.group(0)), "ficha jurídica"
    return 90, "padrão de 90 dias"


def ler_leitura(caminho):
    if not caminho:
        return None
    fm, corpo = frontmatter(ler(caminho).splitlines())
    secoes, atual = {}, None
    for l in corpo:
        if l.startswith("## "):
            t = sem_acento(l[3:].strip().lower())
            atual = "correntes" if t.startswith("corrente") else ("viradas" if t.startswith("virada") else ("distincoes" if t.startswith("distin") else ("perguntas" if t.startswith("pergunta") else None)))
            if atual:
                secoes.setdefault(atual, [])
            continue
        if atual and re.match(r"^\s*[-*]\s+\S", l):
            secoes[atual].append(re.sub(r"^\s*[-*]\s+", "", l).strip())
    aprovado = fm.get("aprovado_por", "")
    secoes["aprovada"] = bool(aprovado) and "PREENCHER" not in aprovado.upper() and "CONFIRMAR" not in aprovado.upper()
    secoes["aprovado_por"] = aprovado
    secoes["aprovado_em"] = fm.get("aprovado_em", "")
    return secoes


def contar(js, chave):
    tab = {}
    for j in js:
        k = chave(j)
        if k is None:
            continue
        linha = tab.setdefault(k, {"a favor": 0, "contra": 0, "neutro": 0, "sem posição": 0})
        linha[j["posicao"]] += 1
    return [[k, v["a favor"], v["contra"], v["neutro"] + v["sem posição"]] for k, v in sorted(tab.items(), key=lambda x: str(x[0]))]


def sinais(js, por_ano, por_tribunal):
    s = []
    anos = [x for x in por_ano if x[1] + x[2] > 0]
    for (a1, f1, c1, _), (a2, f2, c2, _) in zip(anos, anos[1:]):
        m1 = "a favor" if f1 > c1 else ("contra" if c1 > f1 else "empate")
        m2 = "a favor" if f2 > c2 else ("contra" if c2 > f2 else "empate")
        if m1 != m2 and "empate" not in (m1, m2):
            s.append("Em %s, a maioria dos julgados da base passou de %s para %s (%d a favor, %d contra). Confira se é virada do tribunal ou só a amostra da base." % (a2, m1, m2, f2, c2))
    datados = sorted([j for j in js if j["data"] and j["posicao"] in ("a favor", "contra")], key=lambda j: j["data"])
    if datados:
        u = datados[-1]
        s.append("O julgado mais recente da base (%s, %s) é %s." % (u["tribunal"], u["data"], u["posicao"]))
    for t, f, c, n in por_tribunal:
        if f + c >= 2 and (f == 0 or c == 0):
            s.append("%s: todos os %d julgados com posição na base são %s." % (t, f + c, "a favor" if c == 0 else "contra"))
        elif f and c:
            s.append("%s: julgados nos dois sentidos (%d a favor, %d contra). Veja por órgão." % (t, f, c))
    return s


def main():
    ap = argparse.ArgumentParser(description="Mapa jurisprudencial de um tema da base.")
    ap.add_argument("tema")
    ap.add_argument("--leitura")
    ap.add_argument("--hoje")
    ap.add_argument("--validade", type=int)
    ap.add_argument("--ficha")
    ap.add_argument("--saida")
    ap.add_argument("--html")
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--nome-do-escritorio", default="")
    ap.add_argument("--treino", action="store_true")
    a = ap.parse_args()

    texto = ler(a.tema)
    if re.search(r"\bC-\d{4}-\d{4}\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", texto):
        erro("o tema tem dado de cliente (código de caso ou CPF). A base guarda o julgado, não o caso: tire antes de gerar o mapa.")
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    if a.hoje and not hoje:
        erro("data '%s' não lida; use AAAA-MM-DD." % a.hoje)
    validade, de_onde = validade_da_ficha(a, a.tema)
    fm, titulo, resumo, fichas = ler_tema(texto)
    if not fichas:
        erro("o tema '%s' não tem nenhuma ficha de julgado ('### TRIBUNAL · CLASSE E NÚMERO · DATA')." % a.tema)
    js = [info(f, hoje, validade) for f in fichas]
    leitura = ler_leitura(a.leitura)
    treino = a.treino or "TREINO" in (fm.get("documento", "") + titulo)

    por_tribunal = contar(js, lambda j: j["tribunal"] or "sem tribunal")
    por_orgao = contar(js, lambda j: "%s · %s" % (j["tribunal"], j["orgao"] or "órgão a conferir"))
    por_ano = contar(js, lambda j: j["ano"])
    avisos = []
    sem_data = [j["titulo"] for j in js if not j["data"]]
    if sem_data:
        avisos.append("Julgados sem data no título (fora da linha do tempo): %s" % "; ".join(sem_data))
    sem_pos = [j["titulo"] for j in js if j["posicao"] == "sem posição"]
    if sem_pos:
        avisos.append("Julgados sem posição marcada (contam como neutros): %s" % "; ".join(sem_pos))
    if "PREENCHER" in resumo.upper() or not resumo:
        avisos.append("O resumo do escritório ('Como o tema está hoje') ainda não foi escrito.")
    if leitura is None:
        avisos.append("Sem leitura aprovada: correntes, viradas e distinções ficam vazias até o advogado aprovar.")
    elif not leitura["aprovada"]:
        avisos.append("A leitura ainda não foi aprovada pelo advogado (campo aprovado_por vazio).")
    ultimas = sorted([j["pesquisa"] for j in js if j["pesquisa"]])
    if ultimas and (hoje - ler_data(ultimas[-1])).days > validade:
        avisos.append("A última pesquisa do tema é de %s, mais de %d dias: o mapa pode estar velho. Pesquisa nova no Jus IA." % (ultimas[-1], validade))

    teses = [x.strip() for x in re.sub(r"[\[\]]", "", fm.get("teses_do_escritorio", "")).split(",") if x.strip()]
    tot = {
        "julgados": len(js),
        "a_favor": sum(1 for j in js if j["posicao"] == "a favor"),
        "contra": sum(1 for j in js if j["posicao"] == "contra"),
        "neutro": sum(1 for j in js if j["posicao"] in ("neutro", "sem posição")),
        "conferidos": sum(1 for j in js if j["pode_citar"]),
        "nao_conferidos": sum(1 for j in js if j["cor"] == "não conferido"),
        "vencidos": sum(1 for j in js if j["vencida"]),
        "nao_usar": sum(1 for j in js if j["selo"] == "não usar"),
        "ajustar": sum(1 for j in js if j["selo"] == "ajustar antes de usar"),
    }
    dados = {
        "titulo": titulo or os.path.basename(a.tema)[:-3], "tema": os.path.basename(a.tema)[:-3],
        "hoje": hoje.isoformat(), "escritorio": a.nome_do_escritorio, "treino": treino,
        "versao": fm.get("versao", ""), "revisado_em": fm.get("revisado_em", ""), "teses": teses,
        "resumo": "" if "PREENCHER" in resumo.upper() else resumo, "validade": validade,
        "totais": tot, "por_tribunal": por_tribunal, "por_orgao": por_orgao,
        "por_ano": [[str(x[0])] + x[1:] for x in por_ano],
        "sinais": sinais(js, por_ano, por_tribunal),
        "qualificados": [j for j in js if j["qualificado"]],
        "julgados": sorted(js, key=lambda j: j["data"] or "0000", reverse=True),
        "leitura": leitura or {}, "avisos": avisos,
    }

    o = []
    o.append("# Mapa jurisprudencial · %s%s" % (dados["titulo"], " (TREINO)" if treino else ""))
    o.append("")
    o.append("Uso interno do escritório. Feito só com a base (%s, versão %s, revisada em %s). Referência: %s. Validade da conferência: %d dias (%s)." %
             (os.path.basename(a.tema), dados["versao"] or "?", dados["revisado_em"] or "?", hoje.isoformat(), validade, de_onde))
    o.append("")
    o.append("## Números")
    o.append("")
    o.append("- %d julgados: %d a favor, %d contra, %d neutros ou sem posição." % (tot["julgados"], tot["a_favor"], tot["contra"], tot["neutro"]))
    o.append("- Conferidos e vigentes (podem ser citados): %d. Não conferidos: %d. Conferência vencida: %d. Ajustar antes de usar: %d. Não usar: %d." %
             (tot["conferidos"], tot["nao_conferidos"], tot["vencidos"], tot["ajustar"], tot["nao_usar"]))
    if teses:
        o.append("- Teses do escritório que usam o tema: %s." % ", ".join(teses))
    o.append("")
    o.append("## Como o tema está hoje (resumo do escritório)")
    o.append("")
    o.append(dados["resumo"] or "[A PREENCHER] pelo advogado.")
    for nome, tab in (("Por tribunal", por_tribunal), ("Por órgão", por_orgao), ("No tempo", dados["por_ano"])):
        o.append("")
        o.append("## %s" % nome)
        o.append("")
        o.append("| | A favor | Contra | Neutro |")
        o.append("|---|---|---|---|")
        for k, f, c, n in tab:
            o.append("| %s | %d | %d | %d |" % (k, f, c, n))
    o.append("")
    o.append("## Sinais da base (automáticos, não são conclusão)")
    o.append("")
    o.extend(["- " + x for x in dados["sinais"]] or ["- nenhum"])
    lt = leitura or {}
    for chave, nome in (("correntes", "Correntes"), ("viradas", "Viradas"), ("distincoes", "Distinções"), ("perguntas", "Perguntas em aberto")):
        o.append("")
        o.append("## %s%s" % (nome, "" if lt.get("aprovada") else " (leitura ainda não aprovada)"))
        o.append("")
        o.extend(["- " + x for x in lt.get(chave, [])] or ["- [A PREENCHER] na leitura do advogado"])
    o.append("")
    o.append("## Precedentes qualificados")
    o.append("")
    o.extend(["- %s · %s · %s" % (j["titulo"], j["situacao"], j["selo"]) for j in dados["qualificados"]] or ["- nenhum na base"])
    o.append("")
    o.append("## Julgados")
    o.append("")
    o.append("| Data | Tribunal e órgão | Número | Posição | Conferência | Situação | Uso |")
    o.append("|---|---|---|---|---|---|---|")
    for j in dados["julgados"]:
        o.append("| %s | %s · %s | %s | %s | %s | %s | %s |" % (j["data"] or "-", j["tribunal"], j["orgao"] or "-", j["numero"], j["posicao"],
                 j["cor"] + (" em %s" % j["conf_data"] if j["conf_data"] else ""), j["situacao"], j["selo"]))
    o.append("")
    if avisos:
        o.append("## Avisos")
        o.append("")
        o.extend(["- " + x for x in avisos])
        o.append("")
    o.append("Nenhuma citação deste mapa vai para a peça sem a conferir-citacoes.")
    md = "\n".join(o) + "\n"
    if a.saida:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(md)
    if a.html:
        modelo = ler(a.modelo)
        if "__DADOS_DO_MAPA__" not in modelo:
            erro("o modelo '%s' não tem o lugar dos dados (__DADOS_DO_MAPA__)." % a.modelo)
        bloco = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
        os.makedirs(os.path.dirname(os.path.abspath(a.html)), exist_ok=True)
        with open(a.html, "w", encoding="utf-8") as f:
            f.write(modelo.replace("__DADOS_DO_MAPA__", bloco))
    sys.stdout.write(md)
    if a.html:
        sys.stdout.write("Página gravada em %s (uso interno).\n" % a.html)


if __name__ == "__main__":
    main()
