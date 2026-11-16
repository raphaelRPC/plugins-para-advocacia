#!/usr/bin/env python3
"""Quadro de cenários com os valores do advogado (motor-juridico, estrategia-do-caso).

Lê uma planilha de cenários (um por linha) com os valores que o advogado informou e monta
o quadro: valor bruto, honorários, custos, líquido para o cliente, diferença para a
proposta de acordo e tempo estimado. Não trabalha com chance, probabilidade ou percentual
de êxito: planilha com coluna desse tipo é recusada.

Só biblioteca padrão (Python 3.9+). Não altera a planilha.

Uso:
  python3 cenarios.py CAMINHO/cenarios.csv [--acordo VALOR] [--custos-acordo VALOR]
                      [--honorarios-percentual N] [--honorarios-fixo VALOR] [--saida ARQ.md]

Colunas do csv (vírgula ou ponto e vírgula, com ou sem BOM):
  cenario (obrigatória), valor_bruto (obrigatória), custos, tempo_estimado, observacao

Valores aceitos: 12500, 12.500, 12.500,00, R$ 12.500,00, 12500.50. Vazio ou marcação
([A DEFINIR], [A CONFIRMAR]) fica fora da conta e aparece como pendência.

--honorarios-percentual é o percentual contratual sobre o proveito (o que o contrato do
cliente diz), não chance de nada. Sem ele e sem --honorarios-fixo, os honorários ficam
como pendência e o líquido sai "antes dos honorários".

Sai com código 1 e mensagem clara quando o arquivo não existe, está vazio, falta coluna
obrigatória ou aparece coluna de chance ou probabilidade.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

PROIBIDAS = ("chance", "probabilidade", "probab", "exito", "risco_percentual", "percentual_de_ganho",
             "chance_de_ganho", "odds", "likelihood")


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower().strip()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def valor(texto):
    t = (texto or "").strip()
    if not t or re.fullmatch(r"\[.*\]", t):
        return None
    t = re.sub(r"(?i)r\$|\s", "", t)
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", t) or re.fullmatch(r"-?\d+,\d+", t):
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        erro(f"não entendi o valor '{texto}'. Use 12500, 12.500,00 ou R$ 12.500,00.")


def brl(v):
    if v is None:
        return "[A DEFINIR]"
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if v < 0 else "") + "R$ " + s


def main():
    ap = argparse.ArgumentParser(description="Quadro de cenários com os valores do advogado, sem chance de êxito.")
    ap.add_argument("csv")
    ap.add_argument("--acordo")
    ap.add_argument("--custos-acordo")
    ap.add_argument("--honorarios-percentual")
    ap.add_argument("--honorarios-fixo")
    ap.add_argument("--saida")
    a = ap.parse_args()

    p = Path(a.csv)
    if not p.exists():
        erro(f"o arquivo {p} não existe. Nenhum quadro foi montado.")
    bruto = p.read_bytes().decode("utf-8-sig", errors="replace")
    if not bruto.strip():
        erro(f"o arquivo {p} está vazio. Nenhum quadro foi montado.")
    cab = bruto.splitlines()[0]
    sep = ";" if cab.count(";") > cab.count(",") else ","
    leitor = csv.DictReader(io.StringIO(bruto), delimiter=sep)
    campos = {sem_acento(c or "").replace(" ", "_"): c for c in (leitor.fieldnames or [])}
    for c in campos:
        if any(x in c for x in PROIBIDAS):
            erro(f"a coluna '{campos[c]}' fala em chance ou probabilidade. Esta habilidade não trabalha com "
                 "chance de êxito em percentual: tire a coluna e descreva o risco de cada cenário em palavras "
                 "na estratégia.")
    for c in ("cenario", "valor_bruto"):
        if c not in campos:
            erro(f"falta a coluna {c} em {p}. Colunas: cenario, valor_bruto, custos, tempo_estimado, observacao")
    linhas = [{k: (l.get(v) or "").strip() for k, v in campos.items()} for l in leitor]
    linhas = [l for l in linhas if l.get("cenario")]
    if not linhas:
        erro(f"nenhum cenário em {p}. Nenhum quadro foi montado.")

    pct = None
    if a.honorarios_percentual:
        m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*%?\s*", a.honorarios_percentual)
        if not m:
            erro(f"--honorarios-percentual '{a.honorarios_percentual}' não é um número (ex.: 30 ou 30%).")
        pct = float(m.group(1).replace(",", "."))
        if not 0 <= pct <= 100:
            erro("--honorarios-percentual tem de estar entre 0 e 100.")
    fixo = valor(a.honorarios_fixo) if a.honorarios_fixo else None
    tem_hon = pct is not None or fixo is not None

    def honorarios(v):
        if v is None or not tem_hon:
            return None
        return (v * pct / 100 if pct is not None else 0) + (fixo or 0)

    acordo = valor(a.acordo) if a.acordo else None
    custos_acordo = valor(a.custos_acordo) if a.custos_acordo else 0.0
    liquido_acordo = None
    if acordo is not None:
        h = honorarios(acordo)
        liquido_acordo = acordo - (h or 0) - (custos_acordo or 0)

    pend, out = [], []
    o = out.append
    o(f"# Quadro de cenários · {p.stem}\n")
    o(f"- Valores informados pelo advogado; quadro montado em {date.today().isoformat()}.")
    o("- Estimativa. Nenhuma linha diz qual cenário vai acontecer, e nenhum cenário tem chance em percentual.")
    if pct is not None or fixo is not None:
        o("- Honorários: " + " + ".join(x for x in [f"{pct:g}% do valor" if pct is not None else "",
                                                     brl(fixo) if fixo is not None else ""] if x)
          + " (pelo contrato do cliente).")
    else:
        o("- Honorários: não informados. O líquido sai antes dos honorários.")
        pend.append("honorários do contrato do cliente (--honorarios-percentual ou --honorarios-fixo)")
    o("")
    o("| Cenário | Valor bruto | Honorários | Custos | Líquido para o cliente | Diferença para o acordo | Tempo estimado | Observação |")
    o("|---|---|---|---|---|---|---|---|")
    if acordo is not None:
        h = honorarios(acordo)
        o(f"| Acordo proposto | {brl(acordo)} | {brl(h) if tem_hon else '[A DEFINIR]'} | {brl(custos_acordo)} | "
          f"{brl(liquido_acordo)} | (referência) | | proposta feita |")
    for l in linhas:
        v = valor(l.get("valor_bruto"))
        c = valor(l.get("custos")) if l.get("custos") else 0.0
        h = honorarios(v)
        custo_pendente = bool(l.get("custos")) and c is None
        liq = None if v is None or custo_pendente else v - (h or 0) - (c or 0)
        dif = "" if liq is None or liquido_acordo is None else brl(liq - liquido_acordo)
        if v is None:
            pend.append(f"valor bruto do cenário '{l['cenario']}'")
        if l.get("custos") and c is None:
            pend.append(f"custos do cenário '{l['cenario']}'")
        tempo = l.get("tempo_estimado", "") or "[A DEFINIR]"
        if tempo == "[A DEFINIR]":
            pend.append(f"tempo estimado do cenário '{l['cenario']}'")
        o(f"| {l['cenario']} | {brl(v)} | {brl(h) if tem_hon else '[A DEFINIR]'} | {brl(c)} | {brl(liq)} | "
          f"{dif or ('sem proposta de acordo' if liquido_acordo is None else '[A DEFINIR]')} | {tempo} | {l.get('observacao', '')} |")
    o("")
    o("Diferença para o acordo: o líquido do cenário menos o líquido do acordo. Positivo quer dizer que o "
      "cenário, se acontecer, deixa mais para o cliente do que o acordo; não quer dizer que ele vai acontecer.")
    if pend:
        o("\n## Pendências\n")
        for x in dict.fromkeys(pend):
            o(f"- {x} [A DEFINIR]")
    texto = "\n".join(out) + "\n"
    if a.saida:
        Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(a.saida).write_text(texto, encoding="utf-8")
        print(f"Quadro gravado em {a.saida} ({len(linhas)} cenários).")
    else:
        sys.stdout.write(texto)


if __name__ == "__main__":
    main()
