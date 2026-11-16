#!/usr/bin/env python3
"""Julgados contrários da base de jurisprudência do escritório (motor-juridico, advogado-do-diabo).

Lê os arquivos de tema de 04-base/juridico/jurisprudencia/ (formato de docs/pesquisa-jus-ia.md
do plugin) e lista os julgados marcados "contra" a tese do escritório, com a situação da
conferência: conferido e dentro da validade (pode ser usado sem nova marca), conferido com a
validade vencida, não conferido, amarelo ou vermelho. Diz, para cada um, como ele pode
entrar no contraditório: sem marca ou com [CONFERIR].

Só biblioteca padrão (Python 3.9+). Não altera a base.

Uso:
  python3 julgados_contra.py PASTA_OU_ARQUIVO_DO_TEMA [--tese NOME] [--validade 90]
                             [--data AAAA-MM-DD] [--todos]

Opções:
  --tese NOME        só temas cujo teses_do_escritorio cita esta tese
  --validade DIAS    validade da conferência (validade_da_conferencia da ficha; padrão 90)
  --data AAAA-MM-DD  dia de referência para a validade (padrão: hoje)
  --todos            lista também os julgados a favor, para comparar

Como o "contra" é reconhecido: a linha "Para que serve no escritório" começa por "contra",
diz "contra a tese" ou "contrário", ou o julgado tem a linha "Posição: contra", ou o título
do julgado termina com "(contra)".

Sai com código 1 quando o caminho não existe ou quando não há nenhum arquivo de tema com
julgado no formato da base.
"""
import argparse
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower().strip()


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def ler_data(t):
    t = (t or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    return None


def frontmatter(texto):
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                campos[sem_acento(k)] = v.strip()
    return campos


def julgados(texto):
    partes = re.split(r"^###\s+", texto, flags=re.M)
    for grupo in partes[1:]:
        linhas = grupo.splitlines()
        titulo = linhas[0].strip()
        campos = {}
        for l in linhas[1:]:
            if l.startswith("## "):
                break
            m = re.match(r"^\s*[-*]\s*([^:]+):\s*(.*)$", l)
            if m:
                campos[sem_acento(m.group(1))] = m.group(2).strip()
        yield titulo, campos


def posicao(titulo, campos):
    serve = sem_acento(campos.get("para que serve no escritorio", ""))
    pos = sem_acento(campos.get("posicao", ""))
    if pos:
        return "contra" if pos.startswith("contra") else pos
    if sem_acento(titulo).endswith("(contra)"):
        return "contra"
    if serve.startswith("contra") or "contra a tese" in serve or "contrario" in serve or "contraria" in serve:
        return "contra"
    if serve.startswith("a favor") or "a favor" in serve:
        return "a favor"
    return "sem posição"


def conferencia(campos, hoje, validade):
    txt = campos.get("conferencia no inteiro teor", "")
    s = sem_acento(txt)
    d = None
    m = re.search(r"(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})", txt)
    if m:
        d = ler_data(m.group(1))
    cor = next((c for c in ("verde", "amarelo", "vermelho") if c in s), "")
    if "nao conferido" in s or not txt or not cor:
        return "não conferido", "com [CONFERIR]"
    if cor == "vermelho":
        return "vermelho", "não usar: não passou na conferência"
    if cor == "amarelo":
        return f"amarelo ({d.isoformat() if d else 'sem data'})", "com [CONFERIR]: ajuste pendente"
    if d is None:
        return "verde sem data", "com [CONFERIR]: conferência sem data"
    if d + timedelta(days=validade) < hoje:
        return f"verde vencido ({d.isoformat()})", "com [CONFERIR]: conferência vencida"
    return f"verde ({d.isoformat()})", "sem marca (conferido na validade)"


def main():
    ap = argparse.ArgumentParser(description="Julgados contrários da base, com a situação da conferência.")
    ap.add_argument("caminho")
    ap.add_argument("--tese")
    ap.add_argument("--validade", type=int, default=90)
    ap.add_argument("--data")
    ap.add_argument("--todos", action="store_true")
    a = ap.parse_args()

    base = Path(a.caminho)
    if not base.exists():
        erro(f"{base} não existe. A base de jurisprudência fica em escritorio/04-base/juridico/jurisprudencia/.")
    hoje = ler_data(a.data) if a.data else date.today()
    if a.data and hoje is None:
        erro(f"--data '{a.data}' não é uma data (use AAAA-MM-DD).")
    arquivos = [base] if base.is_file() else sorted(base.glob("*.md"))
    if not arquivos:
        erro(f"nenhum arquivo de tema (.md) em {base}.")

    lidos, total, linhas, avisos = 0, 0, [], []
    for f in arquivos:
        texto = f.read_text(encoding="utf-8-sig", errors="replace")
        fm = frontmatter(texto)
        tema = fm.get("documento", f.stem).replace("Jurisprudência ·", "").strip() or f.stem
        teses = fm.get("teses_do_escritorio", "")
        if a.tese and sem_acento(a.tese) not in sem_acento(teses):
            continue
        js = list(julgados(texto))
        if not js:
            avisos.append(f"{f.name}: nenhum julgado no formato '### TRIBUNAL · CLASSE E NÚMERO · DATA'")
            continue
        lidos += 1
        for titulo, campos in js:
            total += 1
            pos = posicao(titulo, campos)
            if pos == "sem posição":
                avisos.append(f"{f.name}: '{titulo}' sem posição (a favor ou contra) na linha 'Para que serve'")
            if pos != "contra" and not a.todos:
                continue
            conf, uso = conferencia(campos, hoje, a.validade)
            situacao = campos.get("situacao", "") or "[CONFERIR]"
            if "superado" in sem_acento(situacao):
                uso += "; situação: " + situacao
            linhas.append((pos, tema, titulo, campos.get("tese em uma frase", ""), conf, situacao, uso))

    if lidos == 0:
        erro("nenhum tema com julgados no formato da base"
             + (f" para a tese '{a.tese}'" if a.tese else "") + ". Avisos: " + "; ".join(avisos or ["nenhum"]))

    contra = [l for l in linhas if l[0] == "contra"]
    print(f"# Julgados {'da base' if a.todos else 'contrários da base'}\n")
    print(f"- Temas lidos: {lidos} · julgados: {total} · contra: {len(contra)}")
    print(f"- Validade da conferência: {a.validade} dias, contados até {hoje.isoformat()}")
    if a.tese:
        print(f"- Só temas da tese: {a.tese}")
    print()
    if not linhas:
        print("Nenhum julgado marcado contra nos temas lidos. A resposta da outra parte vai depender de "
              "pesquisa nova no Jus IA: liste o que pesquisar.")
    else:
        print("| Posição | Tema | Julgado | Tese em uma frase | Conferência | Situação | Como entra no contraditório |")
        print("|---|---|---|---|---|---|---|")
        for l in sorted(linhas, key=lambda x: (x[0] != "contra", x[1], x[2])):
            print("| " + " | ".join(c.replace("|", "/") for c in l) + " |")
    if avisos:
        print("\n## Avisos\n")
        for av in avisos:
            print(f"- {av}")


if __name__ == "__main__":
    main()
