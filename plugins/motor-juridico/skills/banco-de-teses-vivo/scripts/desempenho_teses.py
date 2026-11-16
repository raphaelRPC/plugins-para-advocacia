#!/usr/bin/env python3
"""Resume o desempenho de cada tese do escritório (banco-de-teses-vivo, motor-juridico).

Uso (da pasta de trabalho):
    python3 desempenho_teses.py --pecas escritorio/07-operacao/juridico/pecas.csv \
        --resultados escritorio/07-operacao/juridico/resultados.csv \
        --teses escritorio/04-base/juridico/teses \
        [--validade 90] [--hoje AAAA-MM-DD] [--tese <nome>] [--atualizar]

O que lê:
- pecas.csv (o registro de peças): quais peças usaram cada tese (coluna tese) e em que etapa
  estão. Colunas obrigatórias: id, codigo_caso, etapa, tese;
- resultados.csv (o registro de resultados): uma linha por decisão que chegou. Colunas
  obrigatórias: data_decisao, codigo_caso, tese, orgao_julgador, resultado. Úteis: id_peca,
  instancia, tese_enfrentada (sim, nao, em-parte), observacao. Resultado: procedente, parcial,
  improcedente, acordo, extinto, desistencia;
- a pasta das teses (04-base/juridico/teses/<tese>.md): situação da tese e a tabela do
  fundamento (seção 3), com "Conferida em", "Cor" e "Situação" de cada citação.
Os dois .csv podem vir com vírgula ou ponto e vírgula, com ou sem BOM; datas em AAAA-MM-DD ou
DD/MM/AAAA; maiúsculas e acentos não importam nos campos de opção.

O que mostra, por tese: peças no registro e por etapa; decisões registradas; por órgão julgador,
quantas a tese ganhou, ganhou em parte e perdeu (só as decisões em que a tese foi enfrentada) e
as outras (acordo, extinção, não enfrentada); e os sinais de enfraquecimento:
  1. derrota nas duas últimas decisões do mesmo órgão julgador;
  2. mais derrotas que vitórias, com pelo menos 3 decisões em que a tese foi enfrentada;
  3. queda: com 6 ou mais decisões enfrentadas, a metade mais recente ganha menos que a antiga;
  4. fundamento com conferência vencida (mais que --validade dias), sem conferência, vermelho,
     amarelo, superado, ou julgado contra na base;
  5. tese usada no registro ou nos resultados sem arquivo na pasta das teses;
  6. peça protocolada há mais de 180 dias sem resultado registrado (só informa).
Contagens em números absolutos ("3 de 5"), nunca em percentual. Abaixo de 5 decisões
enfrentadas, avisa: amostra pequena, nenhuma conclusão sozinha.

--atualizar  reescreve, em cada arquivo de tese, só os blocos entre <!-- resultados: inicio -->
             e <!-- resultados: fim --> e entre <!-- desempenho: inicio --> e
             <!-- desempenho: fim -->. Sem --atualizar, só mostra.
--tese       mostra só uma tese.

O script não muda a situação da tese: isso é do advogado.

Saída: 0 com o resumo; 1 quando falta um arquivo, uma coluna obrigatória ou a pasta das teses.
"""

import csv
import datetime as dt
import io
import os
import re
import sys
import unicodedata

RESULTADOS = {"procedente": "ganhou", "parcial": "em parte", "parcialmente procedente": "em parte",
              "improcedente": "perdeu", "acordo": "outro", "extinto": "outro", "extinta": "outro",
              "desistencia": "outro", "pendente": "pendente"}


class Erro(Exception):
    pass


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn").lower().strip()


def chave(texto):
    return re.sub(r"[^a-z0-9]+", "-", sem_acento(texto)).strip("-")


def data(valor):
    v = (valor or "").strip()[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def ler_csv(caminho, obrigatorias, nome):
    if not caminho:
        raise Erro("falta o caminho do %s" % nome)
    if not os.path.isfile(caminho):
        raise Erro("não encontrei o %s: %s" % (nome, caminho))
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for cod in ("utf-8-sig", "cp1252"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    if texto is None:
        raise Erro("não consegui ler o %s como texto: %s" % (nome, caminho))
    linhas = [l for l in texto.splitlines() if l.strip()]
    if not linhas:
        raise Erro("o %s está vazio: %s" % (nome, caminho))
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    tabela = list(csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep))
    titulos = [re.sub(r"[^a-z0-9]+", "_", sem_acento(t)).strip("_") for t in tabela[0]]
    faltam = [c for c in obrigatorias if c not in titulos]
    if faltam:
        raise Erro("o %s não tem a(s) coluna(s) obrigatória(s): %s (%s)" % (nome, ", ".join(faltam), caminho))
    saida = []
    for n, valores in enumerate(tabela[1:], start=2):
        if any(v.strip() for v in valores):
            saida.append((n, {titulos[i]: (valores[i].strip() if i < len(valores) else "") for i in range(len(titulos))}))
    return saida


def ler_teses(pasta):
    if not pasta or not os.path.isdir(pasta):
        raise Erro("não encontrei a pasta das teses: %s" % pasta)
    teses = {}
    for nome in sorted(os.listdir(pasta)):
        if not nome.endswith(".md"):
            continue
        caminho = os.path.join(pasta, nome)
        texto = open(caminho, encoding="utf-8", errors="replace").read()
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
        cab = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", fm.group(1), re.M)) if fm else {}
        id_tese = chave(cab.get("tese") or nome[:-3])
        fundamento = []
        m = re.search(r"^##\s+(?:\d+\.\s*)?Fundamento[^\n]*\n(.*?)(?=^##\s|\Z)", texto, re.M | re.S | re.I)
        if m:
            linhas = [l.strip() for l in m.group(1).splitlines() if l.strip().startswith("|")]
            if len(linhas) >= 2:
                tit = [re.sub(r"[^a-z0-9]+", "_", sem_acento(c)).strip("_") for c in linhas[0].strip("|").split("|")]
                for l in linhas[2:]:
                    cel = [c.strip() for c in l.strip().strip("|").split("|")]
                    fundamento.append(dict(zip(tit, cel)))
        teses[id_tese] = {"arquivo": caminho, "texto": texto, "situacao": cab.get("situacao", "[A PREENCHER]"),
                          "area": cab.get("area", ""), "fundamento": fundamento}
    return teses


def classe(resultado):
    return RESULTADOS.get(sem_acento(resultado).replace("-", " "), "?")


def enfrentada(valor):
    v = sem_acento(valor)
    return v not in ("nao", "não", "n")


def resumir(id_tese, info, pecas, resultados, hoje, validade):
    linhas, sinais = [], []
    minhas = [p for p in pecas if chave(p.get("tese", "")) == id_tese]
    etapas = {}
    for p in minhas:
        etapas[sem_acento(p.get("etapa", "")) or "(sem etapa)"] = etapas.get(sem_acento(p.get("etapa", "")) or "(sem etapa)", 0) + 1
    decisoes = sorted([r for r in resultados if chave(r.get("tese", "")) == id_tese],
                      key=lambda r: data(r.get("data_decisao")) or dt.date.min)
    validas = [r for r in decisoes if classe(r.get("resultado")) != "pendente"]
    enfrent = [r for r in validas if enfrentada(r.get("tese_enfrentada", "sim")) and classe(r.get("resultado")) in ("ganhou", "em parte", "perdeu")]
    linhas.append("Peças no registro: %d (%s). Decisões registradas: %d, das quais %d com a tese enfrentada."
                  % (len(minhas), ", ".join("%s %d" % (k, v) for k, v in sorted(etapas.items())) or "nenhuma",
                     len(validas), len(enfrent)))
    orgaos = {}
    for r in validas:
        o = r.get("orgao_julgador", "").strip() or "(órgão não informado)"
        d = orgaos.setdefault(o, {"ganhou": 0, "em parte": 0, "perdeu": 0, "outro": 0, "ultima": None, "seq": []})
        c = classe(r.get("resultado"))
        if c in ("ganhou", "em parte", "perdeu") and enfrentada(r.get("tese_enfrentada", "sim")):
            d[c] += 1
            d["seq"].append((data(r.get("data_decisao")), c))
        else:
            d["outro"] += 1
        dd = data(r.get("data_decisao"))
        if dd and (d["ultima"] is None or dd > d["ultima"]):
            d["ultima"] = dd
    tabela = ["| Órgão julgador | Decisões | Ganhou | Em parte | Perdeu | Outras (acordo, extinção, não enfrentada) | Última |",
              "|---|---|---|---|---|---|---|"]
    for o, d in sorted(orgaos.items()):
        total = d["ganhou"] + d["em parte"] + d["perdeu"] + d["outro"]
        tabela.append("| %s | %d | %d | %d | %d | %d | %s |" % (o, total, d["ganhou"], d["em parte"], d["perdeu"], d["outro"],
                                                         d["ultima"].isoformat() if d["ultima"] else ""))
        seq = [c for _, c in sorted(d["seq"], key=lambda x: x[0] or dt.date.min)]
        if len(seq) >= 2 and seq[-1] == "perdeu" and seq[-2] == "perdeu":
            sinais.append("%s: perdeu nas duas últimas decisões em que a tese foi enfrentada." % o)
    if not orgaos:
        tabela.append("| (nenhuma decisão registrada) | | | | | | |")

    ganhou = sum(1 for r in enfrent if classe(r["resultado"]) in ("ganhou", "em parte"))
    perdeu = sum(1 for r in enfrent if classe(r["resultado"]) == "perdeu")
    if len(enfrent) >= 3 and perdeu > ganhou:
        sinais.append("Mais derrotas que vitórias: perdeu %d e ganhou (inteira ou em parte) %d, em %d decisões enfrentadas." % (perdeu, ganhou, len(enfrent)))
    if len(enfrent) >= 6:
        meio = len(enfrent) // 2
        antigas, recentes = enfrent[:meio], enfrent[-meio:]
        ga = sum(1 for r in antigas if classe(r["resultado"]) in ("ganhou", "em parte"))
        gr = sum(1 for r in recentes if classe(r["resultado"]) in ("ganhou", "em parte"))
        if gr < ga:
            sinais.append("Queda: nas %d decisões mais antigas, ganhou (inteira ou em parte) %d; nas %d mais recentes, %d." % (meio, ga, meio, gr))
    if len(enfrent) < 5:
        linhas.append("Amostra pequena: %d decisão(ões) com a tese enfrentada. Nenhuma conclusão sobre a tese sai só destes números." % len(enfrent))

    for f in info.get("fundamento", []) if info else []:
        cit = re.sub(r"\s*\[CONFERIR[^\]]*\]", "", f.get("citacao", "")).strip() or "(citação sem texto)"
        quando = data(f.get("conferida_em", ""))
        cor = sem_acento(f.get("cor", ""))
        situ = sem_acento(f.get("situacao", ""))
        lado = sem_acento(f.get("a_favor_ou_contra", ""))
        if quando is None:
            sinais.append("Fundamento sem conferência: %s." % cit)
        elif (hoje - quando).days > validade:
            sinais.append("Conferência vencida: %s (conferida em %s, mais de %d dias)." % (cit, quando.isoformat(), validade))
        if cor in ("vermelho", "amarelo", "cinza"):
            sinais.append("Fundamento %s na última conferência: %s." % (cor, cit))
        if "superad" in situ:
            sinais.append("Fundamento %s: %s." % (f.get("situacao", "").strip(), cit))
        if lado.startswith("contra"):
            sinais.append("Julgado contra na base: %s (a advogado-do-diabo usa este)." % cit)

    sem_resultado = []
    com_resultado = set(r.get("id_peca", "") for r in decisoes) | set(r.get("codigo_caso", "") for r in decisoes)
    for p in minhas:
        if sem_acento(p.get("etapa")) == "protocolada":
            quando = data(p.get("protocolo_data", "")) or data(p.get("atualizado_em", ""))
            if quando and (hoje - quando).days > 180 and p.get("id") not in com_resultado and p.get("codigo_caso") not in com_resultado:
                sem_resultado.append("%s (%s, protocolada em %s)" % (p.get("id"), p.get("codigo_caso"), quando.isoformat()))
    if sem_resultado:
        linhas.append("Protocoladas há mais de 180 dias sem resultado registrado: %s." % "; ".join(sem_resultado))

    por_caso = ["| Data | Caso | Peça | Órgão julgador | Instância | Resultado | Tese enfrentada |", "|---|---|---|---|---|---|---|"]
    for r in validas:
        d = data(r.get("data_decisao"))
        por_caso.append("| %s | %s | %s | %s | %s | %s | %s |" % (d.isoformat() if d else r.get("data_decisao", ""), r.get("codigo_caso", ""),
                        r.get("id_peca", ""), r.get("orgao_julgador", ""), r.get("instancia", ""),
                        sem_acento(r.get("resultado", "")), sem_acento(r.get("tese_enfrentada", "")) or "sim"))
    if len(por_caso) == 2:
        por_caso.append("| (nenhuma decisão registrada) | | | | | | |")
    return linhas, tabela, sinais, por_caso


def trocar_bloco(texto, nome, conteudo):
    rx = re.compile(r"(<!--\s*%s:\s*inicio\s*-->)(.*?)(<!--\s*%s:\s*fim\s*-->)" % (nome, nome), re.S | re.I)
    if not rx.search(texto):
        return texto, False
    return rx.sub(lambda m: m.group(1) + "\n" + conteudo + "\n" + m.group(3), texto, count=1), True


def opcao(args, nome, padrao=None):
    if nome in args:
        i = args.index(nome)
        if i + 1 >= len(args) or args[i + 1].startswith("--"):
            raise Erro("%s precisa de um valor" % nome)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return padrao


def main(argv):
    args = list(argv[1:])
    if "--ajuda" in args or "--help" in args or not args:
        print(__doc__)
        return 0 if args else 1
    try:
        pecas_arq = opcao(args, "--pecas")
        res_arq = opcao(args, "--resultados")
        pasta = opcao(args, "--teses")
        validade_txt = opcao(args, "--validade", "90")
        hoje_txt = opcao(args, "--hoje")
        so = opcao(args, "--tese")
        atualizar = "--atualizar" in args
        if not re.fullmatch(r"\d+", validade_txt or ""):
            raise Erro("--validade precisa ser um número de dias (o campo validade_da_conferencia da ficha jurídica)")
        validade = int(validade_txt)
        hoje = data(hoje_txt) if hoje_txt else dt.date.today()
        if hoje is None:
            raise Erro("--hoje inválido: use AAAA-MM-DD")
        pecas = [l for _, l in ler_csv(pecas_arq, ["id", "codigo_caso", "etapa", "tese"], "pecas.csv")]
        resultados = [l for _, l in ler_csv(res_arq, ["data_decisao", "codigo_caso", "tese", "orgao_julgador", "resultado"], "resultados.csv")]
        teses = ler_teses(pasta)
    except Erro as erro:
        print("ERRO: %s" % erro)
        return 1

    avisos = []
    ids = set(p.get("id") for p in pecas)
    for r in resultados:
        if r.get("id_peca") and r["id_peca"] not in ids:
            avisos.append("resultado de %s cita a peça %s, que não está no pecas.csv" % (r.get("codigo_caso"), r["id_peca"]))
        if classe(r.get("resultado")) == "?":
            avisos.append("resultado '%s' (%s) fora da lista: procedente, parcial, improcedente, acordo, extinto, desistencia"
                          % (r.get("resultado"), r.get("codigo_caso")))
        if data(r.get("data_decisao")) is None:
            avisos.append("data_decisao inválida (%s) em %s" % (r.get("data_decisao"), r.get("codigo_caso")))
    usadas = set(chave(p["tese"]) for p in pecas if p.get("tese")) | set(chave(r["tese"]) for r in resultados if r.get("tese"))
    sem_arquivo = sorted(usadas - set(teses))
    alvo = sorted(set(teses) | set(sem_arquivo))
    if so:
        alvo = [t for t in alvo if t == chave(so)]
        if not alvo:
            print("ERRO: não achei a tese %s nem no registro nem na pasta das teses." % so)
            return 1

    print("BANCO DE TESES · %s · validade da conferência: %d dias" % (hoje.isoformat(), validade))
    print("%d tese(s) na pasta; %d peça(s) no registro; %d decisão(ões) registrada(s)." % (len(teses), len(pecas), len(resultados)))
    mudados = []
    for t in alvo:
        info = teses.get(t)
        linhas, tabela, sinais, por_caso = resumir(t, info, pecas, resultados, hoje, validade)
        if not info:
            sinais.insert(0, "Tese usada no registro ou nos resultados sem arquivo em %s: escreva a tese (modo nova tese) ou corrija o nome." % pasta)
        print()
        print("## %s%s" % (t, (" · %s · situação: %s" % (info["area"], info["situacao"])) if info else " · sem arquivo"))
        for l in linhas:
            print(l)
        print()
        print("\n".join(tabela))
        print()
        if sinais:
            print("Sinais para o advogado olhar:")
            for s in sinais:
                print("- " + s)
        else:
            print("Sinais para o advogado olhar: nenhum.")
        if atualizar and info:
            bloco_d = "\n".join(["Atualizado em %s pelo desempenho_teses.py." % hoje.isoformat(), ""] + linhas + [""] + tabela + [""] +
                                (["Sinais:"] + ["- " + s for s in sinais] if sinais else ["Sinais: nenhum."]))
            novo, ok1 = trocar_bloco(info["texto"], "resultados", "\n".join(por_caso))
            novo, ok2 = trocar_bloco(novo, "desempenho", bloco_d)
            if not (ok1 and ok2):
                avisos.append("%s sem os marcadores <!-- resultados/desempenho: inicio --> e fim: não atualizei" % info["arquivo"])
            elif novo != info["texto"]:
                with open(info["arquivo"], "w", encoding="utf-8") as f:
                    f.write(novo)
                mudados.append(info["arquivo"])
    if avisos:
        print()
        for a in sorted(set(avisos)):
            print("Aviso: " + a)
    print()
    if atualizar:
        print("Arquivos de tese atualizados: %s" % (", ".join(mudados) if mudados else "nenhum"))
    else:
        print("Só mostrei. Com o ok, rode de novo com --atualizar para gravar os blocos de resultados e desempenho nas teses.")
    print("A situação de cada tese (em uso, em observação, enfraquecida, aposentada) muda só com o advogado.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
