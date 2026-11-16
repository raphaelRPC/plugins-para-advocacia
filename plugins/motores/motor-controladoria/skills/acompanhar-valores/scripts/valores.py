#!/usr/bin/env python3
"""Acompanhamento de valores judiciais a partir do valores.csv (motor-controladoria).

Alvará, RPV, precatório e depósito judicial, do pedido ao levantamento e ao repasse. Lê o
valores.csv e imprime, em markdown: PESSOA AGORA (prazo interno vencido, de hoje ou do próximo
dia útil; valor levantado sem repasse registrado; depositado sem levantamento além do limite;
suspenso), avisos ao cliente pendentes (etapa nova sem aviso registrado), parados por etapa,
próximos passos por quem faz, publicações que falam de valor e ainda não têm linha (sugestão),
e o registro a corrigir.

O script não lê nem calcula valor: não há coluna de valor, e coluna de valor que alguém
acrescentar é ignorada com aviso. Não prevê data de pagamento: o "parado há N dias" é o tempo
para alguém conferir o andamento no portal do tribunal, nunca uma previsão.

Colunas do valores.csv (as obrigatórias com *):
  id*, codigo_caso*, cliente_curto, processo, tribunal, tipo*, etapa*, etapa_em*, proximo_passo,
  quem_faz, prazo_interno, publicacao_id, cliente_avisado_em, observacao, atualizado_em
tipo:  alvara | rpv | precatorio | deposito-judicial
etapa: pedido | deferido | expedido | transmitido | depositado | levantado | repassado | suspenso | cancelado

Só biblioteca padrão (Python 3.9+). Não altera nada.

Uso:
  python3 valores.py CAMINHO/valores.csv --data AAAA-MM-DD [--publicacoes CAMINHO/publicacoes.csv]
      [--parado "expedido=30, depositado=10"] [--feriados TEXTO] [--treino] [--saida ARQ]

Limites padrão do "parado" (dias corridos desde etapa_em, para conferir o andamento; ajuste com
--parado e grave o combinado na ficha da automação ou nos aprendizados): pedido 30, deferido 15,
expedido 30, transmitido 60, depositado 10, levantado 5, suspenso 30.

Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio, falta coluna obrigatória, a
data é inválida ou recebe registro de treino sem --treino. Nunca diz que não há nada a apontar
sem ter lido linhas.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

OBRIG = ["id", "codigo_caso", "tipo", "etapa", "etapa_em"]
OPC = ["cliente_curto", "processo", "tribunal", "proximo_passo", "quem_faz", "prazo_interno",
       "publicacao_id", "cliente_avisado_em", "observacao", "atualizado_em"]
TIPOS = ["alvara", "rpv", "precatorio", "deposito-judicial"]
ETAPAS = ["pedido", "deferido", "expedido", "transmitido", "depositado", "levantado", "repassado",
          "suspenso", "cancelado"]
FECHADAS = {"repassado", "cancelado"}
AVISAR = {"expedido", "depositado", "levantado", "suspenso"}
PARADO_PADRAO = {"pedido": 30, "deferido": 15, "expedido": 30, "transmitido": 60, "depositado": 10,
                 "levantado": 5, "suspenso": 30}
PALAVRAS_VALOR = re.compile(r"\b(rpv|requisi[cç][aã]o de pequeno valor|precat[oó]rio|alvar[aá]|"
                            r"dep[oó]sito judicial|levantamento|libera[cç][aã]o de valores?)\b", re.I)
MARCACAO = re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+[^\]]*\]")
DATA_RE = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})/(\d{2,4})")


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def norm(valor):
    v = "".join(c for c in unicodedata.normalize("NFKD", (valor or "").strip())
                if not unicodedata.combining(c)).lower()
    return re.sub(r"[\s_]+", "-", v)


def vazio(valor):
    v = (valor or "").strip()
    return not v or v in {"-", "?"} or bool(MARCACAO.fullmatch(v))


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
        falhar(f"não encontrei o {nome} em `{caminho}`. Confira o caminho (o padrão é {onde}). Se o "
               "registro ainda não existe, ele nasce com o primeiro valor acompanhado (a primeira linha "
               "está no SKILL.md). Nada foi lido, então não há resumo.")
    if p.is_dir():
        falhar(f"`{caminho}` é uma pasta. Passe o arquivo {nome}.")
    linhas = decodificar(p.read_bytes()).splitlines()
    if linhas and linhas[0].strip().lower().startswith("sep="):
        linhas = linhas[1:]
    if not "\n".join(linhas).strip():
        falhar(f"o arquivo `{caminho}` está vazio, sem nem a linha de títulos. Nada foi lido.")
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cab = [norm(c).replace("-", "_") for c in next(leitor)]
    faltando = [c for c in obrigatorias if c not in cab]
    if faltando:
        falhar(f"faltam colunas obrigatórias no {nome}: {', '.join(faltando)}. Colunas encontradas: "
               f"{', '.join(c for c in cab if c) or 'nenhuma'}. Confira se a planilha foi salva como CSV.")
    saida = []
    for n, valores in enumerate(leitor, start=2):
        if not any((v or "").strip() for v in valores):
            continue
        linha = {c: (valores[i] if i < len(valores) else "").strip() for i, c in enumerate(cab) if c}
        for c in opcionais:
            linha.setdefault(c, "")
        linha["_linha"] = n
        saida.append(linha)
    return saida, cab


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


def ler_feriados(texto, ano):
    dias = set()
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", texto or ""):
        try:
            if m.group(1):
                dias.add(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            else:
                a = int(m.group(6)) if m.group(6) else ano
                dias.add(date(a + (2000 if a < 100 else 0), int(m.group(5)), int(m.group(4))))
        except ValueError:
            pass
    return dias


def rotulo(v):
    return " · ".join(x for x in (v["id"], v.get("cliente_curto"), v.get("codigo_caso")) if x)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Acompanhamento de valores judiciais (motor-controladoria).")
    ap.add_argument("valores", help="caminho do valores.csv")
    ap.add_argument("--data", "--hoje", dest="data")
    ap.add_argument("--publicacoes")
    ap.add_argument("--parado", default="")
    ap.add_argument("--feriados", default=None)
    ap.add_argument("--treino", action="store_true")
    ap.add_argument("--saida")
    a = ap.parse_args(argv)

    if a.data:
        hoje = ler_data(a.data)
        if not hoje or not re.fullmatch(r"\s*(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4})\s*", a.data):
            falhar(f"data inválida em --data: `{a.data}`. Use AAAA-MM-DD.")
    else:
        hoje = date.today()
    if "_treino" in {x.lower() for x in Path(a.valores).resolve().parts} and not a.treino:
        falhar("este é um registro de treino (pasta _treino). Rode com --treino.")
    valores, cab = ler_csv(a.valores, OBRIG, OPC, "valores.csv",
                           "escritorio/07-operacao/controladoria/valores.csv")
    avisos = []
    colunas_de_valor = [c for c in cab if re.search(r"valor|montante|quantia|r\$", c)]
    if colunas_de_valor:
        avisos.append(f"coluna(s) {', '.join(colunas_de_valor)} ignorada(s): o plugin não lê, não calcula e "
                      "não confere valor. O valor fica no documento do tribunal e no sistema do escritório")

    limites = dict(PARADO_PADRAO)
    for m in re.finditer(r"([a-zA-Z-]+)\s*=\s*(\d+)", a.parado or ""):
        e = norm(m.group(1))
        if e in limites:
            limites[e] = int(m.group(2))
        else:
            avisos.append(f"--parado: etapa `{m.group(1)}` fora da lista, ignorada")

    feriados = set()
    if a.feriados is not None:
        limpo = MARCACAO.sub(" ", a.feriados).strip()
        if limpo:
            feriados = ler_feriados(limpo, hoje.year)
        else:
            avisos.append("campo feriados_e_recessos vazio ou [A PREENCHER]: só fins de semana")
    else:
        avisos.append("sem --feriados: o próximo dia útil do prazo interno pula só fins de semana")

    def util(d):
        return d.weekday() < 5 and d not in feriados

    proximo = hoje + timedelta(days=1)
    while not util(proximo):
        proximo += timedelta(days=1)

    agora, aviso_cliente, parados, corrigir = [], [], [], []
    por_etapa, por_quem = {}, {}
    ids = {}
    for v in valores:
        e, t = norm(v["etapa"]), norm(v["tipo"])
        v["_etapa"], v["_tipo"] = e, t
        if v["id"] in ids:
            corrigir.append(f"linha {v['_linha']}: id {v['id']} repetido (também na linha {ids[v['id']]})")
        ids.setdefault(v["id"], v["_linha"])
        if e not in ETAPAS:
            corrigir.append(f"linha {v['_linha']} ({v['id']}): etapa `{v['etapa']}` fora da lista")
        if t not in TIPOS:
            corrigir.append(f"linha {v['_linha']} ({v['id']}): tipo `{v['tipo']}` fora da lista")
        if vazio(v["codigo_caso"]):
            corrigir.append(f"linha {v['_linha']} ({v['id']}): sem código do caso")
        etapa_em = ler_data(v["etapa_em"])
        v["_em"] = etapa_em.isoformat() if etapa_em else v["etapa_em"]
        if not etapa_em:
            corrigir.append(f"linha {v['_linha']} ({v['id']}): etapa_em vazia ou ilegível (`{v['etapa_em']}`)")
        por_etapa[e] = por_etapa.get(e, 0) + 1
        if e in FECHADAS:
            continue
        motivos = []
        pi = ler_data(v.get("prazo_interno", ""))
        if pi and pi < hoje:
            motivos.append(f"prazo interno passou em {pi.isoformat()}")
        elif pi and pi <= proximo:
            motivos.append(f"prazo interno {'hoje' if pi == hoje else 'no próximo dia útil (' + pi.isoformat() + ')'}")
        dias = (hoje - etapa_em).days if etapa_em else None
        if e == "levantado" and dias is not None and dias > limites["levantado"]:
            motivos.append(f"valor levantado em {etapa_em.isoformat()} ({dias} dias) sem repasse registrado: "
                           "o dinheiro do cliente está com o escritório; repasse e prestação de contas são da pessoa")
        if e == "depositado" and dias is not None and dias > limites["depositado"]:
            motivos.append(f"depositado em {etapa_em.isoformat()} ({dias} dias) sem levantamento registrado")
        if e == "suspenso":
            motivos.append("suspenso: impugnação, bloqueio ou cancelamento; a pessoa decide o caminho")
        if motivos:
            agora.append((v, motivos))
        elif dias is not None and e in limites and dias > limites[e]:
            parados.append((v, dias))
        avisado = ler_data(v.get("cliente_avisado_em", ""))
        if e in AVISAR and etapa_em and (not avisado or avisado < etapa_em):
            aviso_cliente.append(v)
        q = v.get("quem_faz") or "sem quem faz"
        por_quem.setdefault(q, []).append(v)

    sugestoes = []
    if a.publicacoes:
        pubs, _ = ler_csv(a.publicacoes, ["id", "disponibilizada_em", "triagem"],
                          ["resumo", "tipo_ato", "codigo_caso", "cliente_curto", "tribunal"],
                          "publicacoes.csv", "escritorio/07-operacao/controladoria/publicacoes.csv")
        ligadas = {v.get("publicacao_id") for v in valores if v.get("publicacao_id")}
        for u in pubs:
            if norm(u["triagem"]) == "duplicada" or u["id"] in ligadas:
                continue
            if PALAVRAS_VALOR.search(u.get("resumo", "") + " " + u.get("tipo_ato", "")):
                sugestoes.append(u)

    out = []
    w = out.append
    lidos = f"linhas de valores lidas: {len(valores)}"
    w(f"# Valores judiciais · {hoje.isoformat()}" + (" · TREINO" if a.treino else ""))
    w("")
    w(f"{lidos[0].upper() + lidos[1:]}. Próximo dia útil: {proximo.isoformat()}. O plugin não calcula valor nem prevê data "
      "de pagamento.")
    if not valores:
        w("")
        w("> O valores.csv tem só a linha de títulos: nenhum valor foi lido. Isso não quer dizer que não há "
          "valor a acompanhar.")
    w("")
    w("## PESSOA AGORA")
    if agora:
        for v, motivos in agora:
            w(f"- {rotulo(v)} · {v['_tipo']} · etapa {v['_etapa']} desde {v['_em']} · "
              f"{v.get('quem_faz') or 'sem quem faz'}: " + "; ".join(motivos))
    else:
        w(f"Nenhum item ({lidos}).")
    w("")
    w("## Aviso ao cliente pendente")
    if aviso_cliente:
        for v in aviso_cliente:
            w(f"- {rotulo(v)} · {v['_tipo']} {v['_etapa']} em {v['_em']} · último aviso: "
              f"{v.get('cliente_avisado_em') or 'nenhum'} · pela experiência, sem valor calculado e sem data de "
              "pagamento; notícia ruim por ligação")
    else:
        w(f"Nenhum aviso pendente ({lidos}).")
    w("")
    w("## Parados (conferir o andamento no portal do tribunal)")
    if parados:
        for v, dias in sorted(parados, key=lambda x: -x[1]):
            w(f"- {rotulo(v)} · {v['_tipo']} · etapa {v['_etapa']} há {dias} dias (limite {limites[v['_etapa']]}) · "
              f"{v.get('proximo_passo') or 'próximo passo não registrado'}")
    else:
        w(f"Nenhum parado além dos limites ({lidos}).")
    w("")
    w("## Por etapa")
    w(", ".join(f"{e} {por_etapa[e]}" for e in ETAPAS if e in por_etapa)
      + ("" if por_etapa else "nenhuma linha") + ".")
    w("")
    w("## Próximos passos por quem faz")
    if por_quem:
        for q, lista in sorted(por_quem.items()):
            w(f"### {q}")
            for v in lista:
                w(f"- {rotulo(v)} · {v['_tipo']} {v['_etapa']} · {v.get('proximo_passo') or '[A DEFINIR]'}"
                  + (f" · até {v['prazo_interno']}" if v.get("prazo_interno") else ""))
    else:
        w("Nenhum valor em aberto.")
    w("")
    if a.publicacoes:
        w("## Publicações que falam de valor sem linha (sugestão)")
        if sugestoes:
            for u in sugestoes:
                w(f"- {u['id']} · {u.get('cliente_curto') or '-'} {u.get('codigo_caso') or ''} · "
                  f"{u.get('resumo') or u.get('tipo_ato')}: abrir linha? tipo e etapa [A CONFIRMAR] pela pessoa")
        else:
            w("Nenhuma publicação com RPV, precatório, alvará ou depósito sem linha.")
        w("")
    w("## Registro a corrigir")
    if corrigir:
        for x in corrigir:
            w(f"- {x}")
    else:
        w("Nada a corrigir nas linhas lidas.")
    for x in avisos:
        w(f"- Aviso: {x}")
    texto = "\n".join(out) + "\n"
    sys.stdout.write(texto)
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        sys.stderr.write(f"gravado: {a.saida}\n")


if __name__ == "__main__":
    main()
