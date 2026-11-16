#!/usr/bin/env python3
"""Confere e empacota em .zip uma rotina da controladoria virada habilidade (adaptar-controladoria).

Cópia própria da adaptar-controladoria (motor-controladoria). Recebe a pasta da habilidade (por
exemplo escritorio/04-base/habilidades-do-escritorio/conferencia-de-sexta/) e o registro dos três
testes. Só gera o .zip se nada impedir a instalação:

  - a pasta existe e tem SKILL.md;
  - nomes de arquivo e de pasta só com a-z, 0-9, ponto, hífen e sublinhado; caminho dentro do zip
    com até 100 caracteres; nada de arquivo oculto ou temporário;
  - o SKILL.md abre com frontmatter só com name (igual ao nome da pasta) e description (até 900
    caracteres);
  - o SKILL.md tem a seção "Campos da ficha que esta habilidade usa" e o passo "Aprender";
  - sem travessão nem meia-risca;
  - todo arquivo citado como references/..., assets/... ou scripts/... existe;
  - toda linha do SKILL.md que cita artigo, lei, resolução ou súmula com número leva a marca
    [CONFERIR] na mesma linha (regra de normas do motor-controladoria);
  - o SKILL.md não manda a IA confirmar prazo: frases como "marca como conferido", "preenche
    conferido_por", "agenda o sugerido" ou "decide o prazo em dobro" barram o pacote;
  - o registro dos testes tem os três casos (comum, com exceção, deve parar), todos com
    "O que saiu:" preenchido e "Resultado: passou", e o "Conferido por:" preenchido. A linha crua
    do modelo ("Resultado: passou | falhou") não conta.

Avisa, sem impedir: marcações [A PREENCHER], [A DEFINIR], [A CONFIRMAR] ou [CONFERIR] que
ficaram no SKILL.md, e SKILL.md muito curto ou muito longo.

Uso (da pasta de trabalho, com o caminho da pasta da habilidade adaptar-controladoria):
  python3 <pasta-da-adaptar-controladoria>/scripts/empacotar_habilidade.py \
      escritorio/04-base/habilidades-do-escritorio/<nome> \
      [--testes escritorio/04-base/casos-de-teste/controladoria/<nome>-testes.md] [--saida PASTA]

Sem --testes, procura <pasta>/../../casos-de-teste/controladoria/<nome>-testes.md.
Gera <saida>/<nome>.zip (padrão: a pasta habilidades-do-escritorio/), com tudo dentro de <nome>/.
Sai com código 1 e a lista do que corrigir quando alguma conferência falha.
"""

import argparse
import os
import re
import sys
import zipfile

NOME_OK = re.compile(r"^[a-z0-9._-]+$")
MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]")
CITADO = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+)`")
IGNORAR = {".DS_Store", "__pycache__"}
RE_NORMA = re.compile(
    r"\bart(?:igo)?s?\.?\s*\d+"
    r"|\b(?:Lei|Decreto|Resolu[çc][ãa]o|Provimento|Portaria)(?: Complementar| Conjunta)?\s*(?:n[ºo°.]*\s*)?\d[\d.]*(?:/\d{2,4})?"
    r"|\bS[úu]mula(?: Vinculante)?\s*(?:n[ºo°.]*\s*)?\d+",
    re.I,
)
RE_CONFIRMA = re.compile(
    r"(marca(?:r)? (?:o prazo )?como conferido|preenche(?:r)? (?:o )?conferido_por|escreve(?:r)? (?:o )?nome em conferido_por"
    r"|agenda(?:r)? o (?:prazo )?sugerido|move(?:r)? para conferido|decide(?:r)? (?:o )?prazo em dobro"
    r"|decide(?:r)? a ci[êe]ncia t[áa]cita|entra(?:r)? no painel do tribunal|usa(?:r)? (?:a )?senha)",
    re.I,
)


def falhar(msgs):
    sys.stderr.write("empacotar_habilidade.py: não gerei o .zip. Corrija e rode de novo:\n")
    for m in msgs:
        sys.stderr.write("  - " + m + "\n")
    sys.exit(1)


def ler_frontmatter(texto):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    if not m:
        return None
    bloco = m.group(1)
    chaves = re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", bloco, re.M)
    nome = re.search(r"^name:\s*(.+)$", bloco, re.M)
    desc = re.search(r"^description:\s*(>-?|\|)?\s*\n?(.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:|\Z)", bloco, re.M | re.S)
    return {
        "chaves": chaves,
        "name": nome.group(1).strip() if nome else None,
        "description": " ".join(desc.group(2).split()) if desc else "",
    }


def conferir_testes(caminho):
    if not caminho or not os.path.isfile(caminho):
        return ["não encontrei o registro dos três testes (%s): a habilidade só é empacotada depois de "
                "testada com o caso comum, o caso com exceção e o caso que deve parar" % (caminho or "--testes")]
    erros = []
    texto = open(caminho, encoding="utf-8", errors="replace").read()
    casos = re.split(r"^##\s+Caso\b", texto, flags=re.M)[1:]
    if len(casos) < 3:
        erros.append("o registro dos testes tem %d caso(s); são três: o comum, o com exceção e o que deve parar"
                     % len(casos))
    achou = {"comum": False, "excec": False, "parar": False}
    for c in casos:
        titulo = (c.splitlines()[0] if c.splitlines() else "").lower().replace("ç", "c").replace("ã", "a")
        for k in achou:
            if k in titulo:
                achou[k] = True
    faltam = [n for n, k in (("comum", "comum"), ("com exceção", "excec"), ("deve parar", "parar")) if not achou[k]]
    if casos and faltam:
        erros.append("faltam os casos de teste: %s (títulos '## Caso N · comum', '· com exceção', '· deve parar')"
                     % ", ".join(faltam))
    for i, c in enumerate(casos, 1):
        r = re.search(r"^Resultado:\s*(.*)$", c, re.M | re.I)
        saiu = re.search(r"^O que saiu:\s*(.*)$", c, re.M | re.I)
        if not r or not r.group(1).strip():
            erros.append("caso %d dos testes sem a linha 'Resultado:' preenchida" % i)
        else:
            valor = r.group(1).strip()
            baixo = valor.lower()
            if "|" in valor or ("passou" in baixo and "falhou" in baixo):
                erros.append("caso %d dos testes ainda está com o texto do modelo (Resultado: %s): rode o caso "
                             "e deixe só \"passou\" ou \"falhou (o que falhou)\"" % (i, valor))
            elif not re.match(r"passou\b", baixo):
                erros.append("caso %d dos testes não passou (Resultado: %s)" % (i, valor))
        if not saiu or saiu.group(1).strip() in ("", "...", "…") or saiu.group(1).strip().startswith("["):
            erros.append("caso %d dos testes sem 'O que saiu:' preenchido com o que a habilidade entregou, "
                         "copiado sem corrigir" % i)
    conf = re.search(r"^Conferido por:\s*(.*)$", texto, re.M | re.I)
    if not conf or not conf.group(1).strip() or conf.group(1).strip().startswith("["):
        erros.append("registro dos testes sem 'Conferido por:' preenchido (função e data de quem conferiu)")
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere e empacota uma rotina da controladoria virada habilidade.")
    ap.add_argument("pasta", help="pasta da habilidade, com o SKILL.md dentro")
    ap.add_argument("--testes", help="registro dos três testes")
    ap.add_argument("--saida", help="pasta onde gravar o .zip (padrão: a pasta acima da habilidade)")
    a = ap.parse_args(argv)

    pasta = os.path.abspath(a.pasta.rstrip("/\\"))
    if not os.path.isdir(pasta):
        falhar(["não encontrei a pasta %s" % a.pasta])
    nome = os.path.basename(pasta)
    erros, avisos = [], []
    if not NOME_OK.match(nome):
        erros.append("nome da pasta '%s' fora do padrão: use só minúsculas sem acento, números e hífen" % nome)
    md = os.path.join(pasta, "SKILL.md")
    if not os.path.isfile(md):
        falhar(["falta o SKILL.md dentro de %s" % a.pasta])

    arquivos = []
    for raiz, dirs, files in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in IGNORAR]
        for d in dirs:
            if not NOME_OK.match(d) or d.startswith("."):
                erros.append("pasta com nome fora do padrão: %s" % os.path.relpath(os.path.join(raiz, d), pasta))
        for f in files:
            if f in IGNORAR:
                continue
            rel = os.path.relpath(os.path.join(raiz, f), pasta).replace(os.sep, "/")
            dentro = "%s/%s" % (nome, rel)
            if f.startswith((".", "~$")):
                erros.append("arquivo oculto ou temporário: %s" % rel)
            elif f != "SKILL.md" and not NOME_OK.match(f):
                erros.append("arquivo com nome fora do padrão (só a-z, 0-9, ponto, hífen, sublinhado): %s" % rel)
            if len(dentro) > 100:
                erros.append("caminho com %d caracteres (máximo 100): %s" % (len(dentro), dentro))
            arquivos.append((os.path.join(raiz, f), dentro, rel))

    texto = open(md, encoding="utf-8", errors="replace").read()
    fm = ler_frontmatter(texto)
    if fm is None:
        erros.append("o SKILL.md não abre com o frontmatter entre linhas ---")
    else:
        extras = [c for c in fm["chaves"] if c not in ("name", "description")]
        if extras:
            erros.append("frontmatter com campos além de name e description: %s" % ", ".join(extras))
        if fm["name"] != nome:
            erros.append("name do frontmatter (%s) diferente do nome da pasta (%s)" % (fm["name"], nome))
        if not fm["description"]:
            erros.append("frontmatter sem description")
        elif len(fm["description"]) > 900:
            erros.append("description com %d caracteres (máximo 900)" % len(fm["description"]))
    if "Campos da ficha que esta habilidade usa" not in texto:
        erros.append("falta a seção 'Campos da ficha que esta habilidade usa'")
    if "Aprender" not in texto:
        erros.append("falta o passo 'Aprender' no fim do fluxo")
    for caminho, _dentro, rel in arquivos:
        if rel.endswith((".md", ".txt", ".py", ".csv", ".json", ".html")):
            t = open(caminho, encoding="utf-8", errors="replace").read()
            if chr(0x2014) in t or chr(0x2013) in t:
                erros.append("travessão ou meia-risca em %s" % rel)
    for ref in sorted(set(CITADO.findall(texto))):
        if not os.path.isfile(os.path.join(pasta, ref)):
            erros.append("o SKILL.md cita %s, que não existe na pasta" % ref)
    for n, linha in enumerate(texto.splitlines(), 1):
        achou = RE_NORMA.search(linha)
        if achou and "[CONFERIR" not in linha.upper():
            erros.append("SKILL.md, linha %d: norma com número sem a marca [CONFERIR] (%s)" % (n, achou.group(0).strip()))
        conf = RE_CONFIRMA.search(linha)
        if conf and not re.search(r"\b(nunca|não|nem|jamais)\b", linha, re.I):
            erros.append("SKILL.md, linha %d: a habilidade parece confirmar prazo ou entrar em sistema (%s); "
                         "isso é sempre de uma pessoa" % (n, conf.group(0)))
    testes = a.testes or os.path.join(os.path.dirname(os.path.dirname(pasta)), "casos-de-teste", "controladoria",
                                      "%s-testes.md" % nome)
    erros += conferir_testes(testes)

    marcas = sorted(set(m.group(0) for m in MARCACAO.finditer(texto)))
    if marcas:
        avisos.append("marcações que ficaram no SKILL.md (confira se são de propósito): %s" % ", ".join(marcas))
    n_linhas = texto.count("\n")
    if n_linhas < 40:
        avisos.append("SKILL.md com %d linhas: confira se tem quando usar, fluxo, o que entrega e erros que evita" % n_linhas)
    if n_linhas > 400:
        avisos.append("SKILL.md com %d linhas: passe o material longo para references/" % n_linhas)

    if erros:
        falhar(erros)

    saida = os.path.abspath(a.saida) if a.saida else os.path.dirname(pasta)
    os.makedirs(saida, exist_ok=True)
    destino = os.path.join(saida, "%s.zip" % nome)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for caminho, dentro, _rel in sorted(arquivos, key=lambda x: x[1]):
            z.write(caminho, dentro)
    print("Pacote pronto: %s (%d arquivos)." % (destino, len(arquivos)))
    for av in avisos:
        print("Aviso: " + av)
    print("Para instalar: Personalizar > Habilidades > Enviar, com este .zip (conferir na configuração da conta).")


if __name__ == "__main__":
    main()
