#!/usr/bin/env python3
"""Confere e empacota em .zip uma habilidade própria de peça (peca-vira-habilidade, motor-juridico).

Recebe a pasta da habilidade (escritorio/04-base/habilidades-do-escritorio/<peca>/) e o registro
dos três testes. Só gera o .zip se nada impedir a instalação ou o uso seguro:

Formato
  - a pasta existe e tem SKILL.md e references/mapa-da-peca.md;
  - nomes de arquivo e de pasta só com a-z, 0-9, ponto, hífen e sublinhado; caminho dentro do
    zip com até 100 caracteres; nada de arquivo oculto ou temporário;
  - frontmatter só com name (igual ao nome da pasta) e description (até 900 caracteres);
  - o SKILL.md tem "Campos da ficha que esta habilidade usa", o passo "Aprender", o modo
    "no ciclo" e a regra das citações marcadas ([CONFERIR]);
  - sem travessão nem meia-risca; todo arquivo citado como references/..., assets/... ou
    scripts/... existe.
O mapa da peça
  - cabeçalho com peca (igual ao nome da pasta), area e versao;
  - as seções Variáveis (com as colunas variavel, tipo, origem, obrigatoria), Exceções e o
    modelo entre <!-- modelo: inicio --> e <!-- modelo: fim -->;
  - toda variável do modelo está na tabela; toda variável obrigatória da tabela aparece no
    modelo (ou é de origem ficha com valor em "Valores do escritório"); {{#se}} e {{/se}} fecham;
  - "Versão da habilidade: N" no SKILL.md, se existir, igual à versao do mapa.
Citações
  - toda linha do SKILL.md e do mapa que cita lei, artigo, súmula, tema ou julgado com número
    leva a marca [CONFERIR: ...] na mesma linha. Citação sem marca impede o pacote.
Testes
  - o registro tem os três casos: "## Caso N · comum", "## Caso N · com exceção" e
    "## Caso N · deve parar", cada um com "O que saiu:" preenchido e "Resultado: passou";
  - o título diz "versão N da habilidade" com o mesmo N da versao do mapa (corrigiu a
    habilidade, roda os testes de novo);
  - a linha "Conferido por:" está preenchida.
A linha crua do modelo ("Resultado: passou | falhou") não conta como passou.

Uso (da pasta de trabalho, com o caminho da pasta da habilidade peca-vira-habilidade):
  python3 <pasta-da-peca-vira-habilidade>/scripts/empacotar_habilidade.py \
      escritorio/04-base/habilidades-do-escritorio/<peca> \
      [--testes escritorio/04-base/casos-de-teste/juridico/<peca>-testes.md] [--saida PASTA]

Sem --testes, procura <pasta>/../../casos-de-teste/juridico/<peca>-testes.md.
Gera <saida>/<peca>-v<versao>.zip (padrão: a pasta habilidades-do-escritorio/), com tudo dentro
de <peca>/. Sai com código 1 e a lista do que corrigir quando alguma conferência falha.
"""

import argparse
import os
import re
import sys
import unicodedata
import zipfile

NOME_OK = re.compile(r"^[a-z0-9._-]+$")
MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]")
CITADO = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+)`")
IGNORAR = {".DS_Store", "__pycache__"}
RE_CITACAO = re.compile(
    r"\bart(?:igo)?s?\.?\s*\d+"
    r"|\b(?:Lei|Decreto)(?: Complementar)?\s*(?:n[ºo°.]*\s*)?\d[\d.]*/\d{2,4}"
    r"|\bS[úu]mula(?: Vinculante)?\s*(?:n[ºo°.]*\s*)?\d+"
    r"|\bTema\s*(?:n[ºo°.]*\s*)?\d+"
    r"|\b(?:REsp|AREsp|RE|ARE|HC|MS|ADI|ADC|ADPF|RR|AIRR|IRDR|Apela[çc][ãa]o|Agravo|Recurso)\b[^\n]{0,40}?n[ºo°.]*\s*\d[\d.\-/]+",
    re.I,
)
RE_VAR = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")
RE_SE = re.compile(r"\{\{#se\s+([a-z0-9_]+)\s*=")


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn").lower()


def falhar(msgs):
    sys.stderr.write("empacotar_habilidade.py: não gerei o .zip. Corrija e rode de novo:\n")
    for m in msgs:
        sys.stderr.write("  - " + m + "\n")
    sys.exit(1)


def ler(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def ler_frontmatter(texto):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    if not m:
        return None
    bloco = m.group(1)
    chaves = re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", bloco, re.M)
    nome = re.search(r"^name:\s*(.+)$", bloco, re.M)
    desc = re.search(r"^description:\s*(>-?|\|)?\s*\n?(.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:|\Z)", bloco, re.M | re.S)
    valores = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", bloco, re.M))
    return {"chaves": chaves, "valores": valores, "name": nome.group(1).strip() if nome else None,
            "description": " ".join(desc.group(2).split()) if desc else ""}


def citacoes_sem_marca(texto, rotulo):
    erros = []
    em_codigo = False
    for n, linha in enumerate(texto.splitlines(), 1):
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
        if RE_CITACAO.search(linha) and "[CONFERIR" not in linha.upper():
            trecho = RE_CITACAO.search(linha).group(0)
            erros.append("%s, linha %d: citação sem a marca [CONFERIR: ...] (%s)" % (rotulo, n, trecho.strip()))
    return erros


def tabela(bloco):
    linhas = [l.strip() for l in bloco.splitlines() if l.strip().startswith("|")]
    if len(linhas) < 2:
        return [], []
    def cel(l):
        l = l.strip()[1:]
        if l.endswith("|"):
            l = l[:-1]
        return [c.strip().strip("`") for c in re.split(r"(?<!\\)\|", l)]
    titulos = [sem_acento(c) for c in cel(linhas[0])]
    return titulos, [dict(zip(titulos, cel(l))) for l in linhas[2:]]


def secao(texto, nome):
    m = re.search(r"^##\s+(?:\d+\.\s*)?%s[^\n]*\n(.*?)(?=^##\s|\Z)" % nome, texto, re.M | re.S | re.I)
    return m.group(1) if m else None


def conferir_mapa(caminho, nome):
    erros, versao = [], None
    if not os.path.isfile(caminho):
        return ["falta references/mapa-da-peca.md: a habilidade própria lê o mapa a cada peça"], None
    texto = ler(caminho)
    fm = ler_frontmatter(texto)
    if fm is None:
        return ["o mapa não abre com o cabeçalho entre linhas --- (peca, area, versao)"], None
    v = fm["valores"]
    for k in ("peca", "area", "versao"):
        if not v.get(k):
            erros.append("o cabeçalho do mapa não tem '%s'" % k)
    if v.get("peca") and v["peca"] != nome:
        erros.append("o mapa diz peca: %s, mas a pasta é %s" % (v["peca"], nome))
    versao = v.get("versao")
    bloco = secao(texto, "Vari[áa]veis")
    variaveis = {}
    if bloco is None:
        erros.append("o mapa não tem a seção '## 3. Variáveis'")
    else:
        titulos, linhas = tabela(bloco.split("###")[0])
        if not {"variavel", "tipo", "origem", "obrigatoria"} <= set(titulos):
            erros.append("a tabela de variáveis precisa das colunas variavel, tipo, origem, obrigatoria, exemplo, regra")
        for l in linhas:
            if l.get("variavel"):
                variaveis[l["variavel"]] = l
    if secao(texto, "Exce[çc][õo]es") is None:
        erros.append("o mapa não tem a seção 'Exceções e quando parar': a habilidade precisa saber quando parar")
    mm = re.search(r"<!--\s*modelo:\s*inicio\s*-->\s*\n(.*?)\n\s*<!--\s*modelo:\s*fim\s*-->", texto, re.S | re.I)
    if not mm:
        erros.append("o mapa não tem o modelo entre <!-- modelo: inicio --> e <!-- modelo: fim -->")
        return erros, versao
    modelo = mm.group(1)
    usadas = set(RE_VAR.findall(modelo)) | set(RE_SE.findall(modelo))
    if re.search(r"\{\{\s*genero\s*:", modelo):
        usadas.add("genero")
    for var in sorted(usadas - set(variaveis)):
        erros.append("o modelo usa {{%s}}, que não está na tabela de variáveis" % var)
    fixos = {}
    mf = re.search(r"^###\s+Valores do escrit[óo]rio\s*\n(.*?)(?=^#|\Z)", texto, re.M | re.S | re.I)
    if mf:
        fixos = dict(re.findall(r"^\s*[-*]\s*`?([a-z0-9_]+)`?\s*:\s*(.+?)\s*$", mf.group(1), re.M))
    for var, l in variaveis.items():
        obrig = sem_acento(l.get("obrigatoria", "")).startswith("s")
        origem = sem_acento(l.get("origem", ""))
        if origem == "ficha" and obrig and not fixos.get(var):
            erros.append("a variável %s é de origem ficha e não tem valor em 'Valores do escritório'" % var)
        if obrig and var not in usadas and origem != "ficha" and var not in ("nome_curto",):
            erros.append("a variável obrigatória %s não aparece no modelo (tire da tabela ou use no modelo)" % var)
    if len(re.findall(r"\{\{#se", modelo)) != len(re.findall(r"\{\{/se\}\}", modelo)):
        erros.append("o modelo tem {{#se ...}} sem {{/se}} (ou o contrário)")
    erros += citacoes_sem_marca(texto, "mapa")
    return erros, versao


def conferir_testes(caminho, versao):
    erros = []
    if not caminho or not os.path.isfile(caminho):
        return ["não encontrei o registro dos três testes (%s): a habilidade só é empacotada depois de testada "
                "com o caso comum, o caso com exceção e o caso que deve parar" % (caminho or "--testes")]
    texto = ler(caminho)
    mt = re.search(r"vers[ãa]o\s+(\d+)\s+da habilidade", texto, re.I)
    if versao and (not mt or mt.group(1) != str(versao)):
        erros.append("os testes são da versão %s da habilidade e o mapa está na versão %s: rode os três casos de novo"
                     % (mt.group(1) if mt else "(não diz)", versao))
    partes = re.split(r"^##\s+Caso\b", texto, flags=re.M)[1:]
    tipos = {"comum": False, "excecao": False, "parar": False}
    for i, c in enumerate(partes, 1):
        titulo = sem_acento(c.splitlines()[0] if c.splitlines() else "")
        if "comum" in titulo:
            tipos["comum"] = True
        if "excec" in titulo:
            tipos["excecao"] = True
        if "parar" in titulo:
            tipos["parar"] = True
        r = re.search(r"^Resultado:\s*(.*)$", c, re.M | re.I)
        saiu = re.search(r"^O que saiu:\s*(.*)$", c, re.M | re.I)
        if not r or not r.group(1).strip():
            erros.append("caso %d dos testes sem a linha 'Resultado:' preenchida" % i)
        else:
            valor = r.group(1).strip()
            baixo = valor.lower()
            if "|" in valor or ("passou" in baixo and "falhou" in baixo):
                erros.append("caso %d dos testes ainda está com o texto do modelo (Resultado: %s)" % (i, valor))
            elif not re.match(r"passou\b", baixo):
                erros.append("caso %d dos testes não passou (Resultado: %s)" % (i, valor))
        if not saiu or saiu.group(1).strip() in ("", "...", "…") or saiu.group(1).strip().startswith("["):
            erros.append("caso %d dos testes sem 'O que saiu:' preenchido com o que a habilidade entregou" % i)
    faltam = [n for n, ok in (("comum", tipos["comum"]), ("com exceção", tipos["excecao"]), ("deve parar", tipos["parar"])) if not ok]
    if faltam:
        erros.append("faltam os casos de teste: %s (títulos '## Caso N · comum', '· com exceção', '· deve parar')" % ", ".join(faltam))
    conf = re.search(r"^Conferido por:\s*(.*)$", texto, re.M | re.I)
    if not conf or not conf.group(1).strip() or conf.group(1).strip().startswith("["):
        erros.append("falta 'Conferido por:' preenchido no registro dos testes (quem conferiu e quando)")
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere e empacota uma habilidade própria de peça.")
    ap.add_argument("pasta", help="pasta da habilidade, com SKILL.md e references/mapa-da-peca.md")
    ap.add_argument("--testes", help="registro dos três testes (padrão: 04-base/casos-de-teste/juridico/<peca>-testes.md)")
    ap.add_argument("--saida", help="pasta onde gravar o .zip (padrão: a pasta acima da habilidade)")
    a = ap.parse_args(argv)

    pasta = os.path.abspath(a.pasta.rstrip("/\\"))
    if not os.path.isdir(pasta):
        falhar(["não encontrei a pasta %s" % a.pasta])
    nome = os.path.basename(pasta)
    erros, avisos = [], []
    if not NOME_OK.match(nome):
        erros.append("nome da pasta '%s' fora do padrão: só minúsculas sem acento, números e hífen" % nome)
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

    texto = ler(md)
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
    if not re.search(r"no ciclo", texto, re.I):
        erros.append("falta o modo 'no ciclo' (o que a habilidade faz quando o agente-juridico chama)")
    if "CONFERIR" not in texto:
        erros.append("falta a regra das citações marcadas [CONFERIR] no SKILL.md")
    for caminho, dentro, rel in arquivos:
        if rel.endswith((".md", ".txt", ".py", ".csv", ".json")):
            t = ler(caminho)
            if chr(0x2014) in t or chr(0x2013) in t:
                erros.append("travessão ou meia-risca em %s" % rel)
    for ref in sorted(set(CITADO.findall(texto))):
        if not os.path.isfile(os.path.join(pasta, ref)):
            erros.append("o SKILL.md cita %s, que não existe na pasta" % ref)
    erros += citacoes_sem_marca(texto, "SKILL.md")
    erros_mapa, versao = conferir_mapa(os.path.join(pasta, "references", "mapa-da-peca.md"), nome)
    erros += erros_mapa
    mv = re.search(r"Vers[ãa]o da habilidade:\s*(\d+)", texto)
    if mv and versao and mv.group(1) != str(versao):
        erros.append("o SKILL.md diz 'Versão da habilidade: %s' e o mapa está na versão %s" % (mv.group(1), versao))
    testes = a.testes or os.path.join(os.path.dirname(os.path.dirname(pasta)), "casos-de-teste", "juridico", "%s-testes.md" % nome)
    erros += conferir_testes(testes, versao)

    marcas = sorted(set(m.group(0) for m in MARCACAO.finditer(texto) if not m.group(0).upper().startswith("[CONFERIR")))
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
    destino = os.path.join(saida, "%s-v%s.zip" % (nome, versao))
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for caminho, dentro, _ in sorted(arquivos, key=lambda x: x[1]):
            z.write(caminho, dentro)
    print("Pacote pronto: %s (%d arquivos, versão %s)." % (destino, len(arquivos), versao))
    for av in avisos:
        print("Aviso: " + av)
    print("Para instalar: Personalizar > Habilidades > Enviar, com este .zip (conferir na configuração da conta).")
    print("Versão anterior instalada: remova a antiga antes de enviar a nova, para não ficarem as duas.")


if __name__ == "__main__":
    main()
