#!/usr/bin/env python3
"""Cronômetro do roteiro de sustentação oral (motor-juridico, sustentacao-oral).

Lê o roteiro (formato de assets/modelo-roteiro.md), conta as palavras faladas de cada parte,
estima o tempo de fala pelo ritmo de quem vai falar e compara com o tempo planejado de cada
parte e com o tempo total informado (o do regimento, conferido pelo advogado). Mostra
também em que minuto cada parte deve começar, para a marcação durante a fala.

Só biblioteca padrão (Python 3.9+). Não altera o roteiro.

Uso:
  python3 cronometro.py CAMINHO/roteiro.md [--tempo MINUTOS] [--ritmo PALAVRAS_POR_MINUTO]
                        [--folga PERCENTUAL]

  --tempo   tempo total da fala, em minutos (aceita 15, 12,5 ou 12:30). Sem ele, o script usa
            tempo_do_regimento do cabeçalho do roteiro; com [CONFERIR] ou vazio, não compara
            com o total e avisa.
  --ritmo   palavras por minuto (padrão 130, ou ritmo do cabeçalho). Meça lendo uma parte em
            voz alta com cronômetro: palavras lidas divididas pelos minutos.
  --folga   reserva para interrupção e respiração, em percentual do total (padrão 10).

O que conta como fala: o texto das seções "##" com tempo planejado no título, como
"## 2. Os fatos (2:00)" ou "## 2. Os fatos (2 min)". Não contam: linhas que começam com ">"
(notas internas), tabelas, comentários e as seções sem tempo no título (Antes de usar,
Perguntas prováveis, Memorial).

Sai com código 1 quando o arquivo não existe, está vazio ou não tem nenhuma parte com tempo
planejado no título.
"""
import argparse
import math
import re
import sys
from pathlib import Path

TEMPO_TITULO = re.compile(
    r"\((\s*\d+\s*:\s*\d{2}\s*|\s*\d+(?:[.,]\d+)?\s*min(?:utos?)?(?:\s*(?:e\s*)?\d+\s*s(?:eg(?:undos?)?)?)?\s*|\s*\d+\s*s(?:eg(?:undos?)?)?\s*)\)",
    re.I)


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def segundos(txt):
    t = txt.strip().lower()
    m = re.fullmatch(r"(\d+)\s*:\s*(\d{2})", t)
    if m:
        return int(m[1]) * 60 + int(m[2])
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*min(?:utos?)?(?:\s*(?:e\s*)?(\d+)\s*s\w*)?", t)
    if m:
        return round(float(m[1].replace(",", ".")) * 60) + (int(m[2]) if m[2] else 0)
    m = re.fullmatch(r"(\d+)\s*s\w*", t)
    if m:
        return int(m[1])
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)", t)
    if m:
        return round(float(m[1].replace(",", ".")) * 60)
    return None


def mmss(s):
    s = int(round(s))
    sinal = "-" if s < 0 else ""
    s = abs(s)
    return f"{sinal}{s // 60}:{s % 60:02d}"


def frontmatter(texto):
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                campos[k.strip().lower()] = re.sub(r"\s+#.*$", "", v).strip()
    return campos, (texto[m.end():] if m else texto)


def main():
    ap = argparse.ArgumentParser(description="Cronômetro do roteiro de sustentação oral.")
    ap.add_argument("roteiro")
    ap.add_argument("--tempo")
    ap.add_argument("--ritmo", type=float)
    ap.add_argument("--folga", type=float, default=10.0)
    a = ap.parse_args()

    p = Path(a.roteiro)
    if not p.exists():
        erro(f"o arquivo {p} não existe. Nada foi cronometrado.")
    texto = p.read_text(encoding="utf-8-sig", errors="replace")
    if not texto.strip():
        erro(f"o arquivo {p} está vazio. Nada foi cronometrado.")
    fm, corpo = frontmatter(texto)

    ritmo = a.ritmo
    if ritmo is None:
        try:
            ritmo = float((fm.get("ritmo") or "130").replace(",", "."))
        except ValueError:
            ritmo = 130.0
    if ritmo <= 0:
        erro("--ritmo tem de ser maior que zero.")

    avisos = []
    total = None
    fonte_total = ""
    if a.tempo:
        total = segundos(a.tempo)
        if total is None:
            erro(f"--tempo '{a.tempo}' não é um tempo (use 15, 12,5 ou 12:30).")
        fonte_total = "informado em --tempo"
    else:
        bruto = fm.get("tempo_do_regimento", "")
        if bruto and not re.search(r"\[.*\]", bruto):
            total = segundos(bruto)
            fonte_total = "tempo_do_regimento do roteiro"
        if total is None:
            avisos.append("tempo do regimento não informado [CONFERIR]: confira no regimento interno do tribunal "
                          "e rode com --tempo; o roteiro foi comparado só com o tempo planejado das partes")

    partes, atual = [], None
    for linha in corpo.splitlines():
        if linha.startswith("## "):
            titulo = linha[3:].strip()
            m = TEMPO_TITULO.search(titulo)
            atual = {"titulo": TEMPO_TITULO.sub("", titulo).strip(), "plan": segundos(m.group(1)) if m else None,
                     "palavras": 0} if m else None
            if atual:
                partes.append(atual)
            continue
        if atual is None:
            continue
        s = linha.strip()
        if not s or s.startswith((">", "|", "<!--", "#")):
            continue
        s = re.sub(r"\[[A-Z][^\]]*\]", " ", s)
        s = re.sub(r"[*_`]", "", s)
        atual["palavras"] += len(re.findall(r"[\wÀ-ÿ]+(?:[-'][\wÀ-ÿ]+)*", s))

    if not partes:
        erro(f"nenhuma parte com tempo planejado no título em {p}. Use títulos como '## 2. Os fatos (2:00)'.")

    soma_plan = sum(x["plan"] or 0 for x in partes)
    soma_est = 0.0
    inicio = 0.0
    print(f"# Cronômetro · {p.name}\n")
    print(f"- Ritmo: {ritmo:g} palavras por minuto")
    if total is not None:
        print(f"- Tempo total: {mmss(total)} ({fonte_total}); folga de {a.folga:g}%: falar até {mmss(total * (1 - a.folga / 100))}")
    print()
    print("| Parte | Começa em | Planejado | Palavras | Estimado | Diferença |")
    print("|---|---|---|---|---|---|")
    for x in partes:
        est = x["palavras"] / ritmo * 60
        soma_est += est
        dif = est - (x["plan"] or 0)
        print(f"| {x['titulo']} | {mmss(inicio)} | {mmss(x['plan'] or 0)} | {x['palavras']} | {mmss(est)} | "
              f"{'+' if dif > 0 else ''}{mmss(dif)} |")
        inicio += x["plan"] or est
        if x["palavras"] == 0:
            avisos.append(f"'{x['titulo']}' sem texto falado")
        elif dif > 15:
            avisos.append(f"'{x['titulo']}' passa {mmss(dif)} do planejado: corte cerca de "
                          f"{math.ceil(dif / 60 * ritmo)} palavras")
    print(f"| **Total** | | {mmss(soma_plan)} | {sum(x['palavras'] for x in partes)} | {mmss(soma_est)} | "
          f"{'+' if soma_est > soma_plan else ''}{mmss(soma_est - soma_plan)} |")

    print()
    if total is not None:
        limite = total * (1 - a.folga / 100)
        if soma_est > total:
            print(f"PASSA DO TEMPO: o roteiro leva {mmss(soma_est)} e o tempo é {mmss(total)}. "
                  f"Corte cerca de {math.ceil((soma_est - limite) / 60 * ritmo)} palavras.")
        elif soma_est > limite:
            print(f"SEM FOLGA: o roteiro leva {mmss(soma_est)}, cabe em {mmss(total)}, mas come a folga. "
                  f"Corte cerca de {math.ceil((soma_est - limite) / 60 * ritmo)} palavras.")
        else:
            print(f"CABE: o roteiro leva {mmss(soma_est)}, com {mmss(total - soma_est)} de sobra no tempo de {mmss(total)}.")
        if soma_plan > total:
            avisos.append(f"o planejado das partes ({mmss(soma_plan)}) passa do tempo total ({mmss(total)})")
    for av in avisos:
        print(f"- Aviso: {av}")


if __name__ == "__main__":
    main()
