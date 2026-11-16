#!/usr/bin/env python3
"""Painel interno da carteira de clientes (motor-experiencia).

Lê a carteira.csv (formato em docs/carteira.md) e mostra, para uso só do escritório:
  - clientes por fase e por área;
  - dias sem notícia: a distribuição e os piores casos;
  - compromissos dos próximos 7 e 30 dias, e os que passaram sem atualização;
  - documentos pendentes;
  - reclamações abertas e humor;
  - satisfação (notas da pesquisa);
  - quem recebe resumo mensal e página do caso, e quem pediu para não receber;
  - próximos contatos vencidos;
  - problemas de preenchimento da carteira.

Uso:
  python3 painel_carteira.py CARTEIRA.csv --hoje AAAA-MM-DD [--maximo-sem-noticia 30] \
      [--ficha ficha-da-experiencia.md] [--saida painel.md] [--html painel.html] \
      [--modelo assets/painel-modelo.html] [--nome-do-escritorio "Escritório Modelo"]

O máximo sem notícia vem, nesta ordem: da opção --maximo-sem-noticia; do campo
maximo_sem_noticia da ficha da experiência (--ficha, ou escritorio/04-base/comum/
ficha-da-experiencia.md, procurada subindo a partir da carteira, como o carteira.py
da rotina-da-experiencia faz). O campo é lido só pelo texto antes do parêntese (o
parêntese de opções e exemplos do modelo não conta). Sem nenhum dos dois, o painel
mostra a distribuição e marca a régua [A DEFINIR]. --data é o mesmo que --hoje.

Leitura robusta: vírgula ou ponto e vírgula, com ou sem BOM, maiúsculas e acentos nos
nomes de coluna e nas opções, datas AAAA-MM-DD ou DD/MM/AAAA.
Sai com código 1 e mensagem clara quando falta o arquivo, falta coluna obrigatória
(codigo, area, fase, ultimo_contato) ou a carteira não tem nenhum cliente.
Só biblioteca padrão. Não imprime nada além de código, primeiro nome e números.
"""

import argparse
import csv
import io
import json
import os
import re
import statistics
import sys
import unicodedata
from datetime import date, datetime, timedelta

OBRIGATORIAS = ["codigo", "area", "fase", "ultimo_contato"]
OPCIONAIS = ["nome_curto", "tipo_de_caso", "responsavel", "inicio", "ultimo_contato_tipo",
             "proximo_contato", "motivo_proximo_contato", "proximo_compromisso",
             "data_compromisso", "documentos_pendentes", "humor", "reclamacao_aberta",
             "resumo_mensal", "pagina_do_caso", "satisfacao", "pediu_para_nao_receber",
             "encerrado_em", "atualizado_em"]
FASES = ["entrada", "documentos", "preparacao", "protocolado", "aguardando",
         "audiencia-pericia", "decisao", "recurso", "cumprimento", "encerramento", "encerrado"]
FAIXAS = [(0, 7, "0 a 7 dias"), (8, 15, "8 a 15 dias"), (16, 30, "16 a 30 dias"),
          (31, 60, "31 a 60 dias"), (61, 100000, "mais de 60 dias")]
SIM = {"sim", "s", "x", "yes", "y", "true", "1"}


def erro(msg):
    sys.stderr.write("ERRO: " + msg + "\n")
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def norm_coluna(nome):
    return sem_acento(nome.strip().strip('"').lower()).replace(" ", "_").replace("-", "_")


def norm_opcao(valor):
    v = sem_acento((valor or "").strip().lower())
    return "-".join(v.replace("_", " ").replace("/", " ").split())


def ler_data(valor):
    v = (valor or "").strip()
    if not v:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    raise ValueError(v)


def ler_carteira(caminho):
    if not os.path.isfile(caminho):
        erro("não encontrei a carteira em '%s'. Confira o caminho (o padrão é "
             "escritorio/07-operacao/experiencia/carteira.csv)." % caminho)
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    texto = texto.lstrip("﻿")
    linhas = [l for l in texto.splitlines() if l.strip()]
    if not linhas:
        erro("a carteira '%s' está vazia (nem a linha de títulos)." % caminho)
    primeira = linhas[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cabecalho = [norm_coluna(c) for c in next(leitor)]
    faltam = [c for c in OBRIGATORIAS if c not in cabecalho]
    if faltam:
        erro("a carteira não tem a(s) coluna(s) obrigatória(s): %s. Colunas lidas: %s. "
             "O formato está em docs/carteira.md." % (", ".join(faltam), ", ".join(cabecalho)))
    registros = []
    for n, linha in enumerate(leitor, start=2):
        if not any(v.strip() for v in linha):
            continue
        valores = [v.strip() for v in linha] + [""] * (len(cabecalho) - len(linha))
        registros.append((n, dict(zip(cabecalho, valores))))
    if not registros:
        erro("a carteira '%s' só tem a linha de títulos: nenhum cliente para mostrar." % caminho)
    ausentes = [c for c in OPCIONAIS if c not in cabecalho]
    return registros, ausentes, sep


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def achar_ficha(carteira):
    """Sobe a partir da carteira até a pasta escritorio/ e devolve a ficha da experiência, se existir."""
    pasta = os.path.dirname(os.path.abspath(carteira))
    while True:
        if os.path.basename(pasta) == "escritorio":
            candidata = os.path.join(pasta, "04-base", "comum", "ficha-da-experiencia.md")
            return candidata if os.path.isfile(candidata) else None
        acima = os.path.dirname(pasta)
        if acima == pasta:
            return None
        pasta = acima


def antes_do_parentese(valor):
    """O valor sem o parêntese de opções ou exemplos do modelo (igual ao carteira.py)."""
    valor = (valor or "").strip()
    antes = valor.split("(", 1)[0].strip()
    if antes or "(" not in valor:
        return antes
    if re.search(r"\((opcoes|ex\.|minimo|quantos|em horas|o que|quem|a frase|a partir)", sem_acento(valor).lower()):
        return ""
    return valor.strip("() ")


def maximo_da_ficha(caminho):
    """Devolve (dias, situação): dias é None quando o campo falta ou está em aberto."""
    if not caminho or not os.path.isfile(caminho):
        return None, "sem ficha"
    for linha in ler_texto(caminho).splitlines():
        m = re.match(r"^\s*[-*]\s*maximo_sem_noticia\s*:\s*(.*)$", linha)
        if m:
            v = antes_do_parentese(m.group(1))
            if not v or "[A PREENCHER]" in v or "[A DEFINIR]" in v:
                return None, "campo em aberto na ficha"
            n = re.search(r"\d+", v)
            return (int(n.group(0)), "ficha") if n else (None, "campo sem número na ficha")
    return None, "campo ausente na ficha"


def faixa(dias):
    for a, b, rotulo in FAIXAS:
        if a <= dias <= b:
            return rotulo
    return FAIXAS[-1][2]


def montar(registros, hoje, maximo):
    avisos = []
    clientes = []
    for n, r in registros:
        c = {"linha": n, "codigo": r.get("codigo", "") or "(sem código)",
             "nome": r.get("nome_curto", "") or "", "area": norm_opcao(r.get("area")) or "(sem área)",
             "fase": norm_opcao(r.get("fase")) or "(sem fase)",
             "responsavel": r.get("responsavel", "") or "",
             "humor": norm_opcao(r.get("humor")) or "", "motivo": norm_opcao(r.get("motivo_proximo_contato")),
             "compromisso": norm_opcao(r.get("proximo_compromisso")),
             "reclamacao": norm_opcao(r.get("reclamacao_aberta")) in SIM,
             "resumo": norm_opcao(r.get("resumo_mensal")), "pagina": norm_opcao(r.get("pagina_do_caso")),
             "nao_receber": norm_opcao(r.get("pediu_para_nao_receber")) in SIM}
        if c["fase"] not in FASES:
            avisos.append("linha %d (%s): fase '%s' fora da lista de docs/carteira.md" % (n, c["codigo"], r.get("fase", "")))
        for campo in ("ultimo_contato", "proximo_contato", "data_compromisso", "encerrado_em", "inicio"):
            try:
                c[campo] = ler_data(r.get(campo))
            except ValueError as e:
                c[campo] = None
                avisos.append("linha %d (%s): data '%s' em %s não lida (use AAAA-MM-DD ou DD/MM/AAAA)"
                              % (n, c["codigo"], e.args[0], campo))
        try:
            c["docs"] = int(float((r.get("documentos_pendentes") or "0").replace(",", ".")))
        except ValueError:
            c["docs"] = 0
            avisos.append("linha %d (%s): documentos_pendentes '%s' não é número"
                          % (n, c["codigo"], r.get("documentos_pendentes")))
        nota = (r.get("satisfacao") or "").replace(",", ".").strip()
        c["nota"] = None
        if nota:
            try:
                c["nota"] = float(nota)
                if not 0 <= c["nota"] <= 10:
                    avisos.append("linha %d (%s): satisfacao %s fora de 0 a 10" % (n, c["codigo"], nota))
                    c["nota"] = None
            except ValueError:
                avisos.append("linha %d (%s): satisfacao '%s' não é número" % (n, c["codigo"], nota))
        c["ativo"] = c["fase"] != "encerrado"
        if c["ativo"] and c["ultimo_contato"]:
            c["dias"] = (hoje - c["ultimo_contato"]).days
        else:
            c["dias"] = None
        if c["ativo"] and not c["ultimo_contato"]:
            avisos.append("linha %d (%s): cliente ativo sem ultimo_contato" % (n, c["codigo"]))
        clientes.append(c)

    ativos = [c for c in clientes if c["ativo"]]
    encerrados = [c for c in clientes if not c["ativo"]]
    d = {"hoje": hoje.isoformat(), "maximo": maximo, "total": len(clientes), "ativos": len(ativos),
         "encerrados": len(encerrados)}
    d["encerrados_no_mes"] = sum(1 for c in encerrados if c["encerrado_em"]
                                 and (c["encerrado_em"].year, c["encerrado_em"].month) == (hoje.year, hoje.month))

    def contar(chave, lista):
        out = {}
        for c in lista:
            out[c[chave]] = out.get(c[chave], 0) + 1
        return out

    fases = contar("fase", ativos)
    d["por_fase"] = [[f, fases.get(f, 0)] for f in FASES if f != "encerrado" and fases.get(f)] + \
                    [[f, n] for f, n in sorted(fases.items()) if f not in FASES]
    d["por_area"] = sorted(contar("area", ativos).items(), key=lambda x: (-x[1], x[0]))
    areas = [a for a, _ in d["por_area"]]
    cruz = []
    for f, _ in d["por_fase"]:
        cruz.append([f] + [sum(1 for c in ativos if c["fase"] == f and c["area"] == a) for a in areas])
    d["fase_area"] = {"areas": areas, "linhas": cruz}

    com_dias = [c for c in ativos if c["dias"] is not None]
    dist = {r: 0 for _, _, r in FAIXAS}
    for c in com_dias:
        dist[faixa(c["dias"])] += 1
    d["distribuicao"] = [[r, dist[r]] for _, _, r in FAIXAS]
    d["sem_data"] = len(ativos) - len(com_dias)
    d["mediana_dias"] = statistics.median([c["dias"] for c in com_dias]) if com_dias else None
    piores = sorted(com_dias, key=lambda c: -c["dias"])
    d["acima_do_maximo"] = sum(1 for c in com_dias if maximo is not None and c["dias"] > maximo)
    d["piores"] = [{"codigo": c["codigo"], "nome": c["nome"], "area": c["area"], "fase": c["fase"],
                    "dias": c["dias"], "humor": c["humor"], "nao_receber": c["nao_receber"],
                    "acima": maximo is not None and c["dias"] > maximo}
                   for c in piores[:max(5, d["acima_do_maximo"])]]

    def comp(c):
        return {"codigo": c["codigo"], "nome": c["nome"], "tipo": c["compromisso"] or "(sem tipo)",
                "data": c["data_compromisso"].isoformat(), "em_dias": (c["data_compromisso"] - hoje).days}
    com_comp = [c for c in ativos if c["data_compromisso"]]
    d["compromissos_7"] = [comp(c) for c in sorted(com_comp, key=lambda c: c["data_compromisso"])
                           if 0 <= (c["data_compromisso"] - hoje).days <= 7]
    d["compromissos_30"] = [comp(c) for c in sorted(com_comp, key=lambda c: c["data_compromisso"])
                            if 7 < (c["data_compromisso"] - hoje).days <= 30]
    d["compromissos_passados"] = [comp(c) for c in com_comp if c["data_compromisso"] < hoje]

    docs = [c for c in ativos if c["docs"] > 0]
    d["documentos"] = {"clientes": len(docs), "total": sum(c["docs"] for c in docs),
                       "lista": [{"codigo": c["codigo"], "nome": c["nome"], "fase": c["fase"], "docs": c["docs"]}
                                 for c in sorted(docs, key=lambda c: -c["docs"])]}

    d["reclamacoes"] = [{"codigo": c["codigo"], "nome": c["nome"], "humor": c["humor"]}
                        for c in clientes if c["reclamacao"]]
    d["insatisfeitos"] = [{"codigo": c["codigo"], "nome": c["nome"], "reclamacao": c["reclamacao"]}
                          for c in ativos if c["humor"] == "insatisfeito"]
    humores = contar("humor", ativos)
    d["humor"] = [[h, humores.get(h, 0)] for h in ("tranquilo", "ansioso", "insatisfeito", "a-confirmar")] + \
                 [[h or "(vazio)", n] for h, n in humores.items() if h not in ("tranquilo", "ansioso", "insatisfeito", "a-confirmar")]

    notas = [c["nota"] for c in clientes if c["nota"] is not None]
    d["satisfacao"] = {"com_nota": len(notas), "sem_nota": len(clientes) - len(notas),
                       "media": round(sum(notas) / len(notas), 1) if notas else None,
                       "mediana": statistics.median(notas) if notas else None,
                       "faixas": [["0 a 6", sum(1 for x in notas if x <= 6)],
                                  ["7 e 8", sum(1 for x in notas if 6 < x <= 8)],
                                  ["9 e 10", sum(1 for x in notas if x > 8)]],
                       "baixas": [{"codigo": c["codigo"], "nome": c["nome"], "nota": c["nota"],
                                   "reclamacao": c["reclamacao"]} for c in clientes
                                  if c["nota"] is not None and c["nota"] <= 6]}

    d["resumo"] = {"recebe": sum(1 for c in ativos if c["resumo"] in SIM and not c["nao_receber"]),
                   "nao_recebe": sum(1 for c in ativos if c["resumo"] not in SIM or c["nao_receber"]),
                   "pediu_para_nao_receber": [{"codigo": c["codigo"], "nome": c["nome"]} for c in ativos if c["nao_receber"]],
                   "pagina": [[p, sum(1 for c in ativos if (c["pagina"] or "nao") == p)] for p in ("link", "pdf", "os-dois", "nao")]}

    vencidos = [c for c in ativos if c["proximo_contato"] and c["proximo_contato"] < hoje]
    d["contatos_vencidos"] = [{"codigo": c["codigo"], "nome": c["nome"], "motivo": c["motivo"] or "(sem motivo)",
                               "data": c["proximo_contato"].isoformat(), "atraso": (hoje - c["proximo_contato"]).days}
                              for c in sorted(vencidos, key=lambda c: c["proximo_contato"])]
    d["contatos_hoje"] = [{"codigo": c["codigo"], "nome": c["nome"], "motivo": c["motivo"] or "(sem motivo)"}
                          for c in ativos if c["proximo_contato"] == hoje]
    d["sem_proximo_contato"] = [c["codigo"] for c in ativos if not c["proximo_contato"]]
    d["avisos"] = avisos
    return d


def numero(x):
    if x is None:
        return "-"
    if float(x) == int(x):
        return str(int(x))
    return ("%.1f" % x).replace(".", ",")


def rotulo(c):
    return "%s %s" % (c["codigo"], c["nome"]) if c.get("nome") else c["codigo"]


def markdown(d, origem, treino, ausentes, escritorio):
    o = []
    add = o.append
    titulo = "Painel da carteira" + (" · TREINO" if treino else "")
    add("# %s · %s" % (titulo, d["hoje"][:7]))
    add("")
    add("Uso interno do escritório. Não compartilhar com cliente. %sData de referência: %s. Carteira: `%s`."
        % (("Escritório: %s. " % escritorio) if escritorio else "", d["hoje"], origem))
    add("Máximo sem notícia: %s." % ("%d dias corridos (%s)" % (d["maximo"], d.get("origem_maximo", "opção"))
                                       if d["maximo"] is not None
                                       else "[A DEFINIR] (campo maximo_sem_noticia da ficha da experiência)"))
    add("")
    add("## Números")
    add("")
    add("| Medida | Valor |")
    add("|---|---|")
    add("| Clientes na carteira | %d (ativos: %d; encerrados: %d, dos quais %d neste mês) |"
        % (d["total"], d["ativos"], d["encerrados"], d["encerrados_no_mes"]))
    if d["maximo"] is not None:
        add("| Ativos sem notícia além do máximo | %d de %d |" % (d["acima_do_maximo"], d["ativos"]))
    if d["mediana_dias"] is not None:
        add("| Mediana de dias sem notícia (ativos) | %s |" % numero(d["mediana_dias"]))
    add("| Compromissos nos próximos 7 dias | %d |" % len(d["compromissos_7"]))
    add("| Clientes com documento pendente | %d (%d documentos) |" % (d["documentos"]["clientes"], d["documentos"]["total"]))
    add("| Reclamações abertas | %d |" % len(d["reclamacoes"]))
    add("| Ativos com humor insatisfeito | %d |" % len(d["insatisfeitos"]))
    s = d["satisfacao"]
    add("| Notas de satisfação registradas | %d%s |" % (s["com_nota"], (", média %s, mediana %s" % (
        numero(s["media"]), numero(s["mediana"]))) if s["com_nota"] else ""))
    add("| Próximos contatos vencidos | %d |" % len(d["contatos_vencidos"]))
    add("")
    add("## Clientes ativos por fase e área")
    add("")
    areas = d["fase_area"]["areas"]
    add("| Fase | " + " | ".join(areas) + " | Total |")
    add("|---|" + "---|" * (len(areas) + 1))
    for linha in d["fase_area"]["linhas"]:
        add("| %s | %s | %d |" % (linha[0], " | ".join(str(x) for x in linha[1:]), sum(linha[1:])))
    add("")
    add("## Dias sem notícia")
    add("")
    add("| Faixa | Clientes ativos |")
    add("|---|---|")
    for r, n in d["distribuicao"]:
        add("| %s | %d |" % (r, n))
    if d["sem_data"]:
        add("| sem data de último contato | %d |" % d["sem_data"])
    add("")
    add("Os piores:")
    add("")
    add("| Cliente | Área | Fase | Dias | Humor | Observação |")
    add("|---|---|---|---|---|---|")
    for c in d["piores"]:
        obs = []
        if c["acima"]:
            obs.append("além do máximo")
        if c["nao_receber"]:
            obs.append("pediu para não receber rotina; notícia relevante continua")
        add("| %s | %s | %s | %d | %s | %s |" % (rotulo(c), c["area"], c["fase"], c["dias"], c["humor"] or "-",
                                                  "; ".join(obs) or "-"))
    add("")
    add("## Compromissos")
    add("")
    if not (d["compromissos_7"] or d["compromissos_30"] or d["compromissos_passados"]):
        add("Nenhum compromisso com data na carteira.")
    for nome, lista in (("Próximos 7 dias", d["compromissos_7"]), ("De 8 a 30 dias", d["compromissos_30"]),
                        ("Data passada e a linha não foi atualizada", d["compromissos_passados"])):
        if lista:
            add("- %s: %s" % (nome, "; ".join("%s, %s em %s (%s)" % (
                rotulo(c), c["tipo"], c["data"], ("em %d dia%s" % (c["em_dias"], "" if c["em_dias"] == 1 else "s"))
                if c["em_dias"] >= 0 else ("há %d dias" % -c["em_dias"])) for c in lista)))
    add("")
    add("## Documentos pendentes")
    add("")
    if d["documentos"]["lista"]:
        for c in d["documentos"]["lista"]:
            add("- %s · fase %s · %d documento%s" % (rotulo(c), c["fase"], c["docs"], "" if c["docs"] == 1 else "s"))
    else:
        add("Nenhum documento pendente na carteira.")
    add("")
    add("## Reclamações e humor")
    add("")
    add("- Reclamação aberta: %s" % ("; ".join(rotulo(c) for c in d["reclamacoes"]) or "nenhuma"))
    add("- Humor insatisfeito: %s" % ("; ".join(rotulo(c) + ("" if c["reclamacao"] else " (sem reclamação registrada)")
                                                  for c in d["insatisfeitos"]) or "nenhum"))
    add("- Humor dos ativos: %s" % ", ".join("%s %d" % (h, n) for h, n in d["humor"] if n))
    add("")
    add("## Satisfação")
    add("")
    if s["com_nota"]:
        add("- Faixas: %s" % ", ".join("%s: %d" % (f, n) for f, n in s["faixas"]))
        add("- Notas de 0 a 6: %s" % ("; ".join("%s (%s%s)" % (rotulo(c), numero(c["nota"]),
                                                                 "" if c["reclamacao"] else ", sem reclamação registrada")
                                                for c in s["baixas"]) or "nenhuma"))
    else:
        add("Nenhuma nota registrada na coluna satisfacao.")
    add("- Sem nota: %d" % s["sem_nota"])
    add("")
    add("## Resumo mensal e página do caso")
    add("")
    r = d["resumo"]
    add("- Recebem resumo mensal: %d · não recebem: %d" % (r["recebe"], r["nao_recebe"]))
    add("- Pediram para não receber rotina: %s" % ("; ".join(rotulo(c) for c in r["pediu_para_nao_receber"]) or "ninguém"))
    add("- Página do caso: %s" % ", ".join("%s %d" % (p, n) for p, n in r["pagina"]))
    add("")
    add("## Próximos contatos")
    add("")
    if d["contatos_vencidos"]:
        add("Vencidos:")
        add("")
        for c in d["contatos_vencidos"]:
            add("- %s · %s · previsto para %s (%d dia%s de atraso)" % (rotulo(c), c["motivo"], c["data"], c["atraso"],
                                                                     "" if c["atraso"] == 1 else "s"))
        add("")
    if d["contatos_hoje"]:
        add("Previstos para hoje: %s" % "; ".join("%s (%s)" % (rotulo(c), c["motivo"]) for c in d["contatos_hoje"]))
        add("")
    if d["sem_proximo_contato"]:
        add("Ativos sem próximo contato marcado: %s" % ", ".join(d["sem_proximo_contato"]))
        add("")
    if not (d["contatos_vencidos"] or d["contatos_hoje"] or d["sem_proximo_contato"]):
        add("Nenhum contato vencido.")
        add("")
    if d["avisos"] or ausentes:
        add("## Avisos de preenchimento")
        add("")
        if ausentes:
            add("- Colunas que não existem nesta carteira (as seções que dependem delas saem vazias): %s"
                % ", ".join(ausentes))
        for a in d["avisos"]:
            add("- " + a)
        add("")
    return "\n".join(o)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Painel interno da carteira de clientes.")
    ap.add_argument("carteira", help="caminho da carteira.csv")
    ap.add_argument("--hoje", "--data", dest="hoje", help="data de referência, AAAA-MM-DD ou DD/MM/AAAA (padrão: hoje)")
    ap.add_argument("--maximo-sem-noticia", type=int, help="dias corridos (sem a opção, vem da ficha)")
    ap.add_argument("--ficha", help="ficha-da-experiencia.md (padrão: procurada subindo a partir da carteira)")
    ap.add_argument("--saida", help="grava o painel em .md neste caminho")
    ap.add_argument("--html", help="grava a versão HTML neste caminho")
    ap.add_argument("--modelo", help="modelo HTML (padrão: ../assets/painel-modelo.html)")
    ap.add_argument("--nome-do-escritorio", default="")
    a = ap.parse_args(argv)

    try:
        hoje = ler_data(a.hoje) if a.hoje else date.today()
    except ValueError:
        erro("--hoje '%s' não é uma data (use AAAA-MM-DD ou DD/MM/AAAA)." % a.hoje)
    registros, ausentes, _ = ler_carteira(a.carteira)
    maximo, origem_maximo = a.maximo_sem_noticia, "opção"
    ficha = a.ficha or achar_ficha(a.carteira)
    if a.ficha and not os.path.isfile(a.ficha):
        erro("não encontrei a ficha em '%s'." % a.ficha)
    if maximo is None:
        maximo, origem_maximo = maximo_da_ficha(ficha)
    d = montar(registros, hoje, maximo)
    d["origem_maximo"] = origem_maximo
    treino = "_treino" in os.path.abspath(a.carteira).replace("\\", "/") or "treino" in os.path.basename(a.carteira)
    md = markdown(d, a.carteira, treino, ausentes, a.nome_do_escritorio)
    if maximo is None:
        sys.stderr.write("AVISO: sem --maximo-sem-noticia e sem o campo maximo_sem_noticia na ficha (%s), "
                         "o painel não diz quem passou da régua.\n" % origem_maximo)
    print(md)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(md + "\n")
        sys.stderr.write("painel: %s\n" % a.saida)
    if a.html:
        modelo = a.modelo or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "painel-modelo.html")
        if not os.path.isfile(modelo):
            erro("não encontrei o modelo HTML em '%s'." % modelo)
        with open(modelo, encoding="utf-8") as f:
            html = f.read()
        if "__DADOS_DO_PAINEL__" not in html:
            erro("o modelo HTML não tem o marcador __DADOS_DO_PAINEL__.")
        d["treino"] = treino
        d["escritorio"] = a.nome_do_escritorio
        d["ausentes"] = ausentes
        dados = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
        with open(a.html, "w", encoding="utf-8") as f:
            f.write(html.replace("__DADOS_DO_PAINEL__", dados))
        sys.stderr.write("html: %s\n" % a.html)


if __name__ == "__main__":
    main()
