#!/usr/bin/env python3
"""Conferência mecânica do mapa dos autos (motor-juridico, leitura-dos-autos).

Lê o leitura-dos-autos.md (formato de assets/modelo-mapa-dos-autos.md) e aponta:

  1. linha de tabela com coluna Fonte vazia, ou com fonte que não indica lugar nos autos
     (fl., fls., id, p., pág., doc.) nem "inferência";
  2. linha com coluna Natureza diferente de "autos" ou "inferência";
  3. as inferências, listadas à parte, para o advogado ver o que não está escrito nos autos;
  4. prazo sem a marca "[A CONFIRMAR pela controladoria]", e qualquer data de vencimento
     que pareça calculada ("vence em", "prazo final", "último dia", "termina em");
  5. a cobertura da leitura ("Páginas lidas: X de Y" e as partes não lidas).

Só biblioteca padrão (Python 3.9+). Não altera o mapa. Não calcula prazo nenhum.

Uso:
  python3 conferir_mapa.py CAMINHO/leitura-dos-autos.md

Sai com código 1 quando o arquivo não existe, está vazio ou não tem nenhuma tabela.
Sai com código 0 e o relatório em todos os outros casos, com "Alertas: 0" só quando
leu tabelas e não achou nada.
"""
import re
import sys
import unicodedata
from pathlib import Path

MARCA_PRAZO = "a confirmar pela controladoria"
FONTE_OK = re.compile(r"\b(fls?|id|p|pag|pg|doc|docs|ids?)\b\.?\s*\d", re.I)
DATA = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b")
CALCULADO = re.compile(r"(vence(m|u)?\s+(em|no dia|dia)|prazo\s+final|ultimo\s+dia|termina(m)?\s+em|"
                       r"vencimento\s+(em|no dia|:)|fatal\s+em|prazo\s+ate\s+\d)", re.I)


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower().strip()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def celulas(linha):
    s = linha.strip()
    if not s.startswith("|"):
        return None
    return [c.strip() for c in s.strip("|").split("|")]


def tabelas(linhas):
    """Gera (secao, numero_da_linha_do_cabecalho, cabecalho, [(numero_linha, dict)])."""
    secao = ""
    i = 0
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("#"):
            secao = l.lstrip("#").strip()
        cab = celulas(l)
        if cab and i + 1 < len(linhas) and re.fullmatch(r"\|?[\s:|-]+\|?", linhas[i + 1].strip() or "x"):
            nomes = [sem_acento(c) for c in cab]
            corpo = []
            j = i + 2
            while j < len(linhas) and celulas(linhas[j]) is not None:
                c = celulas(linhas[j])
                corpo.append((j + 1, dict(zip(nomes, c + [""] * (len(nomes) - len(c))))))
                j += 1
            yield secao, i + 1, nomes, corpo
            i = j
            continue
        i += 1


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 1)
    caminho = Path(sys.argv[1])
    if not caminho.exists():
        erro(f"o arquivo {caminho} não existe. Nada foi conferido.")
    texto = caminho.read_text(encoding="utf-8-sig", errors="replace")
    if not texto.strip():
        erro(f"o arquivo {caminho} está vazio. Nada foi conferido.")
    linhas = texto.splitlines()
    tabs = list(tabelas(linhas))
    if not tabs:
        erro(f"nenhuma tabela em {caminho}. O mapa segue o formato de assets/modelo-mapa-dos-autos.md.")

    alertas, inferencias, prazos_ok = [], [], 0
    linhas_lidas = 0
    for secao, _, nomes, corpo in tabs:
        tem_fonte = "fonte" in nomes
        tem_natureza = "natureza" in nomes
        secao_prazo = "prazo" in sem_acento(secao)
        for n, linha in corpo:
            if not any(v.strip() for v in linha.values()):
                continue
            linhas_lidas += 1
            resumo = next((v for k, v in linha.items() if v and k not in ("fonte", "natureza", "#")), "")[:70]
            nat = sem_acento(linha.get("natureza", ""))
            if tem_fonte:
                fonte = linha.get("fonte", "")
                f_ok = FONTE_OK.search(sem_acento(fonte)) or "inferencia" in sem_acento(fonte)
                if not fonte:
                    alertas.append(f"linha {n} ({secao}): sem fonte · {resumo}")
                elif not f_ok:
                    alertas.append(f"linha {n} ({secao}): fonte '{fonte}' sem o número da folha, do id ou da página · {resumo}")
            if tem_natureza:
                if nat not in ("autos", "inferencia"):
                    alertas.append(f"linha {n} ({secao}): natureza '{linha.get('natureza', '')}' "
                                   "deve ser 'autos' ou 'inferência' · " + resumo)
            if nat == "inferencia" or "inferencia" in sem_acento(linha.get("fonte", "")):
                inferencias.append(f"linha {n} ({secao}): {resumo}")
            if secao_prazo:
                junto = " ".join(linha.values())
                if MARCA_PRAZO in sem_acento(junto):
                    prazos_ok += 1
                else:
                    alertas.append(f"linha {n} ({secao}): prazo sem a marca [A CONFIRMAR pela controladoria] · {resumo}")

    for n, l in enumerate(linhas, 1):
        s = sem_acento(l)
        if CALCULADO.search(s) and MARCA_PRAZO not in s:
            alertas.append(f"linha {n}: parece prazo calculado ou data de vencimento · {l.strip()[:90]}")
        elif "prazo" in s and DATA.search(l) and MARCA_PRAZO not in s and not l.lstrip().startswith(("|", "#", ">")):
            alertas.append(f"linha {n}: prazo com data, sem a marca da controladoria · {l.strip()[:90]}")

    cobertura = "não informada (escreva 'Páginas lidas: X de Y' no registro de leitura)"
    m = re.search(r"p[aá]ginas\s+lidas\s*:\s*(\d+)\s*de\s*(\d+)", texto, re.I)
    parcial = False
    if m:
        lidas, total = int(m.group(1)), int(m.group(2))
        cobertura = f"{lidas} de {total} páginas"
        if lidas < total:
            parcial = True
            alertas.append(f"leitura parcial: {lidas} de {total} páginas. O mapa não fala das páginas não lidas; "
                           "isso precisa estar no cabeçalho 'Antes de usar'")
    else:
        alertas.append("cobertura da leitura não informada")

    print(f"# Conferência do mapa · {caminho.name}\n")
    print(f"- Tabelas lidas: {len(tabs)} · linhas: {linhas_lidas}")
    print(f"- Cobertura: {cobertura}")
    print(f"- Prazos com a marca da controladoria: {prazos_ok}")
    print(f"- Inferências: {len(inferencias)}")
    print(f"- Alertas: {len(alertas)}\n")
    if alertas:
        print("## Alertas\n")
        for a in alertas:
            print(f"- {a}")
    if inferencias:
        print("\n## O que é inferência (não está escrito nos autos)\n")
        for i in inferencias:
            print(f"- {i}")
    if not alertas:
        print("Nenhum alerta nas tabelas lidas." + (" Leitura parcial: confira o cabeçalho." if parcial else ""))


if __name__ == "__main__":
    main()
