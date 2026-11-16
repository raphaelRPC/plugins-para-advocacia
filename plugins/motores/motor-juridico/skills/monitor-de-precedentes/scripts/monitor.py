#!/usr/bin/env python3
"""Monitor de precedentes da base do escritório (motor-juridico, monitor-de-precedentes).

Dois comandos:

  vigiar BASE_JURIDICO [--hoje AAAA-MM-DD] [--validade N] [--ficha ficha-juridica.md]
         [--pecas pecas.csv] [--saida relatorio.md]
      BASE_JURIDICO é a pasta escritorio/04-base/juridico (com jurisprudencia/ e teses/).
      Lista: temas com a última pesquisa vencida e o que pesquisar de novo no Jus IA;
      precedentes qualificados (súmula, tema, IRDR, IAC) a vigiar; julgados não conferidos ou
      com conferência vencida (o lote de conferência); teses que podem estar afetadas
      (julgado a favor que virou vermelho ou superado, qualificado sem conferência); e as
      peças em andamento do pecas.csv que usam essas teses (ADVOGADO AGORA).

  comparar TEMA.md PESQUISA_NOVA.md [--hoje AAAA-MM-DD] [--saida relatorio.md]
      Compara as fichas de uma pesquisa nova (rascunho da trazer-pesquisa, mesmo formato do
      tema) com o tema da base: julgados novos a favor e contra, julgados que mudaram de
      situação, de posição ou de conferência, precedentes qualificados novos ou mudados, e se
      a tese pode ter sido afetada (sim, possível, não). A decisão é do advogado.

A validade vem de --validade, ou de validade_da_conferencia da ficha jurídica (procurada
subindo a partir da base), ou 90 dias. O pecas.csv vem de --pecas, ou de
escritorio/07-operacao/juridico/pecas.csv procurado subindo a partir da base.

Leitura robusta: .md e .csv com ou sem BOM, vírgula ou ponto e vírgula, maiúsculas nas
etapas, datas AAAA-MM-DD ou DD/MM/AAAA. Sai com código 1 e mensagem clara quando falta a
pasta, o arquivo, o tema não tem ficha, ou o pecas.csv não tem as colunas necessárias.
Nunca diz "nada a apontar" sem dizer quantos temas e fichas leu. Só biblioteca padrão.
"""

import argparse
import csv
import io
import os
import re
import sys
import unicodedata
from datetime import date, datetime

ABERTAS = {"pedida", "em-analise", "tese-definida", "minuta", "conferida", "revisada", "aprovada"}
COLUNAS_PECAS = ["id", "codigo_caso", "peca", "etapa", "tese"]


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


def ler_tema(caminho):
    linhas = ler(caminho).splitlines()
    fm, corpo = {}, linhas
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for l in linhas[1:i]:
                    m = re.match(r"^([\w_]+)\s*:\s*(.*)$", l)
                    if m:
                        fm[m.group(1)] = m.group(2).strip()
                corpo = linhas[i + 1:]
                break
    titulo, fichas, atual = "", [], None
    for l in corpo:
        if l.startswith("# ") and not titulo:
            titulo = l[2:].strip()
        elif l.startswith("## "):
            atual = None
        elif l.startswith("### "):
            atual = {"titulo": l[4:].strip(), "partes": [p.strip() for p in re.split(r"\s+·\s+|\s+\|\s+", l[4:].strip())], "campos": {}}
            fichas.append(atual)
        elif atual is not None:
            m = re.match(r"^\s*-\s*([^:]{2,80}):\s*(.*)$", l)
            if m:
                atual["campos"][sem_acento(m.group(1).strip().lower())] = m.group(2).strip()
    teses = [x.strip() for x in re.sub(r"[\[\]]", "", fm.get("teses_do_escritorio", "")).split(",") if x.strip()]
    return {"fm": fm, "titulo": titulo, "fichas": [info(f) for f in fichas], "teses": teses}


def campo(c, inicio):
    for k, v in c.items():
        if k.startswith(inicio):
            return v
    return ""


def info(f):
    p, c = f["partes"], f["campos"]
    d = {"titulo": f["titulo"], "tribunal": p[0] if p else "", "numero": p[1] if len(p) > 1 else "",
         "data": ler_data(p[2]) if len(p) > 2 else None}
    num = d["numero"]
    ms = re.search(r"S[úu]mula\s+(?:Vinculante\s+)?(?:n[º°o.]*\s*)?(\d+)", num)
    mt = re.search(r"Tema\s+(?:n[º°o.]*\s*)?(\d+)", num)
    mi = re.search(r"(IRDR|IAC)\s*(?:n[º°o.]*\s*)?([\d.\-/]+)", num)
    trib = re.sub(r"\W", "", d["tribunal"].upper())
    if ms:
        d["chave"], d["tipo"] = "sumula-%s-%s" % (ms.group(1), trib), "súmula"
    elif mt:
        d["chave"], d["tipo"] = "tema-%s-%s" % (mt.group(1), trib), "tema"
    elif mi:
        d["chave"], d["tipo"] = "%s-%s-%s" % (mi.group(1).lower(), re.sub(r"\D", "", mi.group(2)), trib), mi.group(1)
    else:
        d["chave"], d["tipo"] = "julgado-%s" % re.sub(r"\D", "", num), "julgado"
    d["qualificado"] = d["tipo"] != "julgado" or bool(re.search(r"repercuss[ãa]o geral|repetitivo|IRDR|IAC", campo(c, "tese"), re.I))
    s = sem_acento(campo(c, "para que serve").lower())
    d["posicao"] = "contra" if s.startswith("contra") else ("a favor" if s.startswith("a favor") else ("neutro" if s.startswith("neutro") else "sem posição"))
    fonte = campo(c, "fonte")
    mp = re.search(r"pesquisa de (\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", fonte)
    d["pesquisa"] = ler_data(mp.group(1)) if mp else None
    ml = re.search(r"https?://\S+", fonte)
    d["link"] = ml.group(0).rstrip(").,;") if ml else ""
    conf = campo(c, "conferencia no inteiro teor")
    mc = re.search(r"\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}", conf)
    d["conf_data"] = ler_data(mc.group(0)) if mc else None
    cor = "não conferido"
    cl = sem_acento(conf.lower())
    if d["conf_data"] and not re.search(r"verde\s*\|\s*amarelo", cl):
        for k in ("verde", "amarelo", "vermelho"):
            if re.search(r"\b%s\b" % k, cl):
                cor = k
    d["cor"] = cor
    d["situacao"] = campo(c, "situacao").replace("`", "").strip() or "[CONFERIR]"
    d["tese"] = campo(c, "tese em uma frase")
    d["orgao"] = campo(c, "orgao e relator").split(";")[0].strip()
    return d


def caiu(d):
    sit = sem_acento(d["situacao"].lower())
    return d["cor"] == "vermelho" or bool(re.match(r"superado", sit))


def subir_ate(inicio, *partes):
    pasta = os.path.abspath(inicio)
    while True:
        for cand in (os.path.join(pasta, *partes), os.path.join(pasta, "escritorio", *partes)):
            if os.path.exists(cand) and (os.path.basename(pasta) == "escritorio" or "escritorio" in cand):
                return cand
        cima = os.path.dirname(pasta)
        if cima == pasta:
            return None
        pasta = cima


def validade(a, inicio):
    if getattr(a, "validade", None):
        return a.validade, "opção --validade"
    ficha = getattr(a, "ficha", None) or subir_ate(inicio, "04-base", "comum", "ficha-juridica.md")
    if ficha and os.path.isfile(ficha):
        for l in ler(ficha).splitlines():
            m = re.match(r"^\s*-?\s*validade_da_conferencia\s*:\s*(.*)$", l)
            if m:
                v = m.group(1).split("(")[0]
                n = re.search(r"\d+", v)
                if n and "PREENCHER" not in v.upper():
                    return int(n.group(0)), "ficha jurídica"
    return 90, "padrão de 90 dias (sem validade_da_conferencia na ficha)"


def ler_pecas(caminho):
    texto = ler(caminho)
    linhas = [l for l in texto.splitlines() if l.strip()]
    if not linhas:
        erro("o pecas.csv '%s' está vazio (nem a linha de títulos)." % caminho)
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cab = [sem_acento(c.strip().strip('"').lower()).replace(" ", "_") for c in next(leitor)]
    faltam = [c for c in COLUNAS_PECAS if c not in cab]
    if faltam:
        erro("o pecas.csv não tem a(s) coluna(s): %s. O formato está em docs/producao.md." % ", ".join(faltam))
    regs = []
    for linha in leitor:
        if not any(v.strip() for v in linha):
            continue
        linha = [v.strip() for v in linha] + [""] * (len(cab) - len(linha))
        regs.append(dict(zip(cab, linha)))
    return regs


def escrever(texto, saida):
    if saida:
        os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
        with open(saida, "w", encoding="utf-8") as f:
            f.write(texto)
    sys.stdout.write(texto)


def cmd_vigiar(a):
    base = a.base
    jur = os.path.join(base, "jurisprudencia")
    if not os.path.isdir(jur):
        erro("não encontrei '%s'. Passe a pasta escritorio/04-base/juridico (a que tem jurisprudencia/)." % jur)
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    if a.hoje and not hoje:
        erro("data '%s' não lida; use AAAA-MM-DD." % a.hoje)
    dias, de_onde = validade(a, base)
    nomes = [n for n in sorted(os.listdir(jur)) if n.endswith(".md") and not n.startswith(("_", "."))]
    if not nomes:
        erro("a pasta '%s' não tem nenhum tema (.md). Comece pela trazer-pesquisa." % jur)
    temas = {n[:-3]: ler_tema(os.path.join(jur, n)) for n in nomes}
    pasta_teses = os.path.join(base, "teses")
    teses_arq = {}
    if os.path.isdir(pasta_teses):
        for n in sorted(os.listdir(pasta_teses)):
            if n.endswith(".md") and not n.startswith(("_", ".")):
                teses_arq[n[:-3]] = ler(os.path.join(pasta_teses, n))
    # tese -> temas: pelo cabeçalho do tema e pelo texto da tese
    liga = {}
    for t, d in temas.items():
        for tese in d["teses"]:
            liga.setdefault(tese, set()).add(t)
    for tese, texto in teses_arq.items():
        for t in temas:
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t), texto):
                liga.setdefault(tese, set()).add(t)

    pesquisar, lote, qualif, sinais_tema = [], [], [], {}
    total_fichas = 0
    for t, d in temas.items():
        fs = d["fichas"]
        total_fichas += len(fs)
        ultima = max([f["pesquisa"] for f in fs if f["pesquisa"]], default=None)
        tribs = sorted({f["tribunal"] for f in fs if f["tribunal"]})
        s = []
        if not ultima:
            s.append("sem data de pesquisa")
            pesquisar.append("%s (%s): sem data de pesquisa nas fichas; refazer a pesquisa no Jus IA e guardar com a data." % (d["titulo"] or t, t))
        elif (hoje - ultima).days > dias:
            s.append("pesquisa vencida (%s)" % ultima)
            pesquisar.append("%s (%s): julgados desde %s em %s, a favor e contra; última pesquisa há %d dias." %
                             (d["titulo"] or t, t, ultima.isoformat(), ", ".join(tribs) or "[tribunais principais]", (hoje - ultima).days))
        for f in fs:
            if f["qualificado"]:
                qualif.append((t, f))
                pesquisar.append("%s: situação atual no portal do tribunal (tese fixada, revisão, cancelamento, modulação, suspensão) [tema %s]." % (f["numero"], t))
            if f["cor"] == "não conferido":
                lote.append((t, f, "não conferido"))
            elif f["cor"] == "verde" and f["conf_data"] and (hoje - f["conf_data"]).days > dias:
                lote.append((t, f, "conferência vencida (%s)" % f["conf_data"]))
            elif f["cor"] == "amarelo":
                lote.append((t, f, "amarelo: ajuste pendente"))
        caidos = [f for f in fs if caiu(f) and f["posicao"] == "a favor"]
        if caidos:
            s.append("julgado a favor vermelho ou superado: %s" % "; ".join(f["numero"] for f in caidos))
        q_pend = [f for f in fs if f["qualificado"] and (f["cor"] != "verde" or "conferir" in f["situacao"].lower())]
        if q_pend:
            s.append("precedente qualificado sem conferência: %s" % "; ".join(f["numero"] for f in q_pend))
        sinais_tema[t] = {"sinais": s, "caidos": caidos, "q_pend": q_pend, "ultima": ultima}

    afetadas, olhar = {}, {}
    for tese, ts in sorted(liga.items()):
        for t in sorted(ts):
            st = sinais_tema[t]
            if st["caidos"]:
                afetadas.setdefault(tese, []).append("%s: %s" % (t, "; ".join("%s %s" % (f["numero"], f["situacao"] if caiu(f) else f["cor"]) for f in st["caidos"])))
            elif st["q_pend"] or any("vencida" in x or "sem data" in x for x in st["sinais"]):
                olhar.setdefault(tese, []).append("%s: %s" % (t, "; ".join(st["sinais"])))

    # peças em andamento
    pecas_txt, pecas_aviso = [], ""
    caminho_pecas = a.pecas or subir_ate(base, "07-operacao", "juridico", "pecas.csv")
    if a.pecas and not os.path.isfile(a.pecas):
        erro("não encontrei o pecas.csv em '%s'." % a.pecas)
    if caminho_pecas and os.path.isfile(caminho_pecas):
        for r in ler_pecas(caminho_pecas):
            etapa = sem_acento(r.get("etapa", "").lower()).replace(" ", "-").replace("_", "-")
            tese = r.get("tese", "").strip()
            if etapa in ABERTAS and tese and (tese in afetadas or tese in olhar):
                grav = "AFETADA" if tese in afetadas else "a olhar"
                pecas_txt.append("%s · %s · %s · etapa %s · tese %s (%s)" % (r.get("id", ""), r.get("codigo_caso", ""), r.get("peca", ""), etapa, tese, grav))
    else:
        pecas_aviso = "Sem pecas.csv: não cruzei com as peças em andamento."

    o = ["# Monitor de precedentes · %s" % hoje.isoformat(), ""]
    o.append("Li %d temas e %d fichas em %s, e %d teses. Validade da conferência: %d dias (%s)." %
             (len(temas), total_fichas, jur, len(teses_arq), dias, de_onde))
    o.append("")
    o.append("## ADVOGADO AGORA")
    o.append("")
    if pecas_txt:
        o.extend("- Peça em andamento: %s" % x for x in pecas_txt)
    else:
        o.append("- Nenhuma peça em andamento com tese afetada." if not pecas_aviso else "- " + pecas_aviso)
    o.append("")
    o.append("## Teses que podem estar afetadas")
    o.append("")
    if afetadas:
        for tese, motivos in afetadas.items():
            o.append("- **%s**: %s. O advogado decide se a tese muda." % (tese, " | ".join(motivos)))
    else:
        o.append("- Nenhuma tese com julgado a favor que caiu.")
    for tese, motivos in olhar.items():
        if tese not in afetadas:
            o.append("- %s, a olhar: %s." % (tese, " | ".join(motivos)))
    o.append("")
    o.append("## Pesquisar de novo no Jus IA")
    o.append("")
    o.extend("%d. %s" % (i, x) for i, x in enumerate(pesquisar, start=1)) if pesquisar else o.append("Nenhum tema com pesquisa vencida.")
    o.append("")
    o.append("## Precedentes qualificados a vigiar")
    o.append("")
    if qualif:
        for t, f in qualif:
            o.append("- %s · tema %s · conferência: %s%s · situação: %s" % (f["numero"], t, f["cor"], (" em %s" % f["conf_data"]) if f["conf_data"] else "", f["situacao"]))
    else:
        o.append("- Nenhum na base.")
    o.append("")
    o.append("## Lote de conferência (trazer-pesquisa)")
    o.append("")
    if lote:
        for t, f, motivo in lote:
            o.append("- [ ] %s · %s · %s · %s" % (t, f["titulo"], motivo, f["link"] or "sem link"))
    else:
        o.append("- Nada a conferir.")
    o.append("")
    o.append("## Temas e teses")
    o.append("")
    o.append("| Tema | Fichas | Última pesquisa | Teses | Sinais |")
    o.append("|---|---|---|---|---|")
    for t, d in temas.items():
        st = sinais_tema[t]
        ts = sorted(x for x, temas_x in liga.items() if t in temas_x)
        o.append("| %s | %d | %s | %s | %s |" % (t, len(d["fichas"]), st["ultima"] or "-", ", ".join(ts) or "nenhuma", "; ".join(st["sinais"]) or "ok"))
    sem_tema = sorted(x for x in teses_arq if x not in liga)
    if sem_tema:
        o.append("")
        o.append("Teses sem nenhum tema na base: %s. Sem jurisprudência guardada, o monitor não vigia essas teses." % ", ".join(sem_tema))
    o.append("")
    o.append("Este relatório não muda a base nem as teses. Pesquisa nova entra pela trazer-pesquisa; a comparação, pelo comando comparar.")
    escrever("\n".join(o) + "\n", a.saida)


def cmd_comparar(a):
    base = ler_tema(a.tema)
    nova = ler_tema(a.pesquisa)
    if not base["fichas"]:
        erro("o tema '%s' não tem nenhuma ficha." % a.tema)
    if not nova["fichas"]:
        erro("a pesquisa nova '%s' não tem nenhuma ficha. Monte as fichas pela trazer-pesquisa antes." % a.pesquisa)
    hoje = ler_data(a.hoje) if a.hoje else date.today()
    idx = {f["chave"]: f for f in base["fichas"]}
    novos, mudou, iguais = [], [], 0
    for f in nova["fichas"]:
        v = idx.get(f["chave"])
        if not v:
            novos.append(f)
            continue
        dif = []
        if v["posicao"] != f["posicao"]:
            dif.append("posição: %s -> %s" % (v["posicao"], f["posicao"]))
        if sem_acento(v["situacao"].lower()) != sem_acento(f["situacao"].lower()) and "conferir" not in f["situacao"].lower():
            dif.append("situação: %s -> %s" % (v["situacao"], f["situacao"]))
        if f["cor"] != "não conferido" and (v["cor"], v["conf_data"]) != (f["cor"], f["conf_data"]):
            dif.append("conferência: %s -> %s em %s" % (v["cor"], f["cor"], f["conf_data"]))
        if dif:
            mudou.append((v, f, dif))
        else:
            iguais += 1
    ausentes = [f for k, f in idx.items() if k not in {x["chave"] for x in nova["fichas"]}]
    motivos_sim, motivos_possivel = [], []
    for f in novos:
        if f["posicao"] == "contra":
            (motivos_sim if f["qualificado"] else motivos_possivel).append("novo contra: %s (%s, %s)" % (f["numero"], f["tribunal"], f["orgao"] or "órgão a conferir"))
        elif f["qualificado"]:
            motivos_possivel.append("precedente qualificado novo: %s" % f["numero"])
    for v, f, dif in mudou:
        if v["posicao"] == "a favor" and (caiu(f) or f["posicao"] == "contra"):
            motivos_sim.append("%s era a favor e agora: %s" % (f["numero"], "; ".join(dif)))
        elif f["qualificado"] and (f["posicao"] == "contra" or caiu(f) or any(x.startswith("situação") for x in dif)):
            (motivos_sim if f["posicao"] == "contra" or caiu(f) else motivos_possivel).append("precedente qualificado %s: %s" % (f["numero"], "; ".join(dif)))
        elif f["posicao"] == "contra":
            motivos_possivel.append("%s (contra): %s" % (f["numero"], "; ".join(dif)))
    # órgão que decidia a favor e aparece com um contra novo
    orgaos_favor = {(f["tribunal"], f["orgao"]) for f in base["fichas"] if f["posicao"] == "a favor"}
    for f in novos:
        if f["posicao"] == "contra" and (f["tribunal"], f["orgao"]) in orgaos_favor:
            motivos_sim.append("%s · %s decidia a favor na base e tem um contra novo (%s)" % (f["tribunal"], f["orgao"], f["numero"]))
    afetada = "sim" if motivos_sim else ("possível" if motivos_possivel else "não")

    o = ["# Comparação · %s x pesquisa nova · %s" % (os.path.basename(a.tema), hoje.isoformat()), ""]
    o.append("Base: %d fichas. Pesquisa nova: %d fichas. Teses do tema: %s." % (len(base["fichas"]), len(nova["fichas"]), ", ".join(base["teses"]) or "nenhuma"))
    o.append("")
    o.append("## A tese pode ter sido afetada? %s" % afetada.upper())
    o.append("")
    o.extend("- " + x for x in motivos_sim + motivos_possivel) if (motivos_sim or motivos_possivel) else o.append("- Nada na pesquisa nova muda a posição dos julgados da base.")
    o.append("")
    o.append("A decisão é do advogado: manter a tese, ajustar, fazer a distinção ou suspender as peças que a usam.")
    o.append("")
    o.append("## Julgados novos (%d)" % len(novos))
    o.append("")
    o.extend("- %s · %s · %s%s" % (f["posicao"], f["titulo"], f["tese"][:140], " · QUALIFICADO" if f["qualificado"] else "") for f in novos) if novos else o.append("- nenhum")
    o.append("")
    o.append("## Julgados que mudaram (%d)" % len(mudou))
    o.append("")
    o.extend("- %s: %s" % (v["titulo"], "; ".join(dif)) for v, f, dif in mudou) if mudou else o.append("- nenhum")
    o.append("")
    o.append("## Iguais: %d. Na base e fora da pesquisa nova: %d" % (iguais, len(ausentes)))
    o.append("")
    if ausentes:
        o.append("Não estar na pesquisa nova não quer dizer que caiu: pode ser o recorte da pesquisa. %s" % "; ".join(f["numero"] for f in ausentes))
        o.append("")
    o.append("Próximo passo: a trazer-pesquisa junta as fichas novas ao tema (sem mudar as que já estão); as mudanças nas fichas existentes passam pela conferência no inteiro teor e pelo comando marcar dela.")
    escrever("\n".join(o) + "\n", a.saida)


def main():
    ap = argparse.ArgumentParser(description="Monitor de precedentes da base do escritório.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("vigiar")
    p.add_argument("base", help="pasta escritorio/04-base/juridico")
    p.add_argument("--hoje")
    p.add_argument("--validade", type=int)
    p.add_argument("--ficha")
    p.add_argument("--pecas")
    p.add_argument("--saida")
    p = sub.add_parser("comparar")
    p.add_argument("tema")
    p.add_argument("pesquisa")
    p.add_argument("--hoje")
    p.add_argument("--saida")
    a = ap.parse_args()
    if a.cmd == "vigiar":
        cmd_vigiar(a)
    elif a.cmd == "comparar":
        cmd_comparar(a)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
