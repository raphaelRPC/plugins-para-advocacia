#!/usr/bin/env python3
"""Confere e empacota uma habilidade própria do escritório em .zip, pronta para instalar.

Uso:
    python3 empacotar_habilidade.py CAMINHO/DA/PASTA/DA/HABILIDADE \
        --testes escritorio/04-base/casos-de-teste/experiencia/<nome>-testes.md [--saida ARQUIVO.zip]

Confere, antes de gerar o .zip:
  - a pasta tem SKILL.md;
  - o nome da pasta só tem letras minúsculas sem acento, números e hífen;
  - todo arquivo e pasta dentro dela só usa [a-z0-9._-], sem arquivo oculto ou temporário,
    e nenhum caminho (nome-da-habilidade/arquivo) passa de 100 caracteres;
  - o frontmatter tem name igual ao nome da pasta e description com até 900 caracteres;
  - o SKILL.md tem a seção "Campos da ficha que esta habilidade usa" e o passo "Aprender";
  - não há travessão nem meia-risca;
  - os arquivos citados como references/..., assets/... ou scripts/... existem;
  - não sobrou campo do modelo em maiúsculas entre colchetes (ex.: [NOME-DA-PASTA]);
  - o registro dos testes (--testes, formato em assets/modelo-registro-dos-testes.md)
    tem pelo menos três casos ("## Caso"), cada um com a linha "Resultado: passou".
    Só "passou" conta: o texto cru do modelo ("passou | falhou"), "...", vazio,
    "falhou" ou qualquer resultado que mencione falha não passam.
Avisa, sem barrar, as marcações [A PREENCHER], [A DEFINIR], [A CONFIRMAR] e [CONFERIR].

Sem problema: grava o .zip ao lado da pasta (ou em --saida) e sai com código 0.
Com problema: lista tudo, não grava nada e sai com código 1.
"""

import os
import re
import sys
import unicodedata
import zipfile

RE_NOME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_ARQUIVO = re.compile(r"^[a-z0-9._-]+$")
RE_MARCACAO = re.compile(r"\[(?:A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]")
RE_CAMPO_MODELO = re.compile(r"\[[A-ZÀ-Ý][A-ZÀ-Ý0-9 ,./:;_()-]*\]")
RE_CITADO = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+)`")
IGNORAR = {".DS_Store", "__pycache__"}


def ler(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    try:
        return bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        return bruto.decode("cp1252", errors="replace")


def frontmatter(texto):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if not m:
        return None, None
    bloco = m.group(1)
    nome = re.search(r"^name:\s*(.+)$", bloco, re.M)
    desc = re.search(r"^description:\s*(>-?|\|)?\s*\n?(.*?)(?=^\w+:|\Z)", bloco, re.M | re.S)
    return (nome.group(1).strip() if nome else None), (" ".join(desc.group(2).split()) if desc else "")


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def resultado_passou(valor):
    """True só para um resultado que diz que passou e nada mais que indique falha ou modelo cru."""
    v = sem_acento(valor).strip()
    if not v.startswith("passou"):
        return False
    resto = v[len("passou"):]
    if "|" in resto or "falh" in resto or "nao passou" in resto or "[" in resto or "..." in resto:
        return False
    return re.fullmatch(r"[\s.!]*(\([^()]*\)|[,;:]\s*.*)?[\s.!]*", resto) is not None


def conferir_testes(caminho):
    if not caminho:
        return ["falta o registro dos três testes (--testes): a habilidade só é empacotada depois de testada "
                "com o caso comum, o caso com exceção e o caso que deve parar "
                "(modelo em assets/modelo-registro-dos-testes.md)"]
    if not os.path.isfile(caminho):
        return ["não encontrei o registro dos testes: %s" % caminho]
    erros = []
    casos = re.split(r"^##\s+Caso\b", ler(caminho), flags=re.M)[1:]
    if len(casos) < 3:
        erros.append("o registro dos testes tem %d caso(s); são três: o comum, o com exceção e o que deve parar"
                     % len(casos))
    for i, c in enumerate(casos, 1):
        r = re.search(r"^Resultado:[ \t]*(.*)$", c, re.M | re.I)
        if not r:
            erros.append("caso %d dos testes sem a linha 'Resultado:'" % i)
        elif not resultado_passou(r.group(1)):
            erros.append("caso %d dos testes não passou (Resultado: %s). Escreva 'Resultado: passou' só depois de "
                         "rodar o caso e conferir; o texto do modelo não vale" % (i, r.group(1).strip() or "vazio"))
    return erros


def conferir(pasta):
    erros, avisos = [], []
    nome = os.path.basename(os.path.normpath(pasta))
    if not RE_NOME.match(nome):
        erros.append("nome da pasta '%s': use só letras minúsculas sem acento, números e hífen (ex.: ligacao-de-boas-vindas)" % nome)
    skill = os.path.join(pasta, "SKILL.md")
    if not os.path.isfile(skill):
        erros.append("falta o arquivo SKILL.md na pasta")
        return nome, erros, avisos, []

    arquivos = []
    for raiz, dirs, nomes in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in IGNORAR]
        for d in dirs:
            if not RE_ARQUIVO.match(d):
                erros.append("pasta com caractere não aceito: %s" % os.path.relpath(os.path.join(raiz, d), pasta))
        for n in nomes:
            if n in IGNORAR:
                continue
            rel = os.path.relpath(os.path.join(raiz, n), pasta).replace(os.sep, "/")
            if n.startswith((".", "~$")):
                erros.append("arquivo oculto ou temporário: %s" % rel)
                continue
            if not RE_ARQUIVO.match(n) and n != "SKILL.md":
                erros.append("arquivo com caractere não aceito (use a-z, 0-9, ponto, hífen): %s" % rel)
            caminho = "%s/%s" % (nome, rel)
            if len(caminho) > 100:
                erros.append("caminho com %d caracteres (máximo 100): %s" % (len(caminho), caminho))
            arquivos.append(rel)

    texto = ler(skill)
    fm_nome, descricao = frontmatter(texto)
    if fm_nome is None:
        erros.append("SKILL.md sem frontmatter (as linhas --- com name e description no topo)")
    else:
        if fm_nome != nome:
            erros.append("name do frontmatter ('%s') diferente do nome da pasta ('%s')" % (fm_nome, nome))
        if not descricao:
            erros.append("description vazia no frontmatter")
        elif len(descricao) > 900:
            erros.append("description com %d caracteres (máximo 900)" % len(descricao))
    if "Campos da ficha que esta habilidade usa" not in texto:
        erros.append("falta a seção 'Campos da ficha que esta habilidade usa'")
    if not re.search(r"Aprender", texto):
        erros.append("falta o passo 'Aprender' no fluxo")

    for rel in arquivos:
        if not rel.endswith((".md", ".py", ".csv", ".txt", ".json")):
            continue
        conteudo = ler(os.path.join(pasta, rel))
        for numero, linha in enumerate(conteudo.splitlines(), start=1):
            if chr(0x2014) in linha or chr(0x2013) in linha:
                erros.append("travessão ou meia-risca em %s:%d" % (rel, numero))
            if rel.endswith(".md"):
                for m in RE_MARCACAO.finditer(linha):
                    avisos.append("marcação %s em %s:%d" % (m.group(0), rel, numero))
                for m in RE_CAMPO_MODELO.finditer(linha):
                    if not RE_MARCACAO.fullmatch(m.group(0)):
                        erros.append("campo do modelo não preenchido %s em %s:%d" % (m.group(0), rel, numero))
        for citado in RE_CITADO.findall(conteudo):
            if not os.path.exists(os.path.join(pasta, citado)):
                erros.append("%s cita %s, que não existe na pasta" % (rel, citado))
    return nome, erros, avisos, arquivos


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if "--help" in argv or "--ajuda" in argv:
        print(__doc__)
        return 0
    saida = None
    if "--saida" in argv:
        i = argv.index("--saida")
        if i + 1 >= len(argv):
            print("ERRO: --saida precisa do caminho do .zip.")
            return 1
        saida = argv[i + 1]
        args = [a for a in args if a != saida]
    testes = None
    if "--testes" in argv:
        i = argv.index("--testes")
        if i + 1 >= len(argv):
            print("ERRO: --testes precisa do caminho do registro dos testes.")
            return 1
        testes = argv[i + 1]
        args = [a for a in args if a != testes]
    if not args:
        print(__doc__)
        print("ERRO: informe a pasta da habilidade.")
        return 1
    pasta = args[0]
    if not os.path.isdir(pasta):
        print("ERRO: pasta não encontrada: %s. Nada foi empacotado." % pasta)
        return 1

    nome, erros, avisos, arquivos = conferir(pasta)
    erros += conferir_testes(testes)
    for a in avisos:
        print("AVISO: " + a)
    if avisos:
        print("As marcações acima não barram o pacote, mas a habilidade ainda tem decisões em aberto.")
    if erros:
        print("NÃO EMPACOTADO. Corrija:")
        for e in erros:
            print("  - " + e)
        return 1

    destino = saida or os.path.join(os.path.dirname(os.path.abspath(pasta)), nome + ".zip")
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(arquivos):
            z.write(os.path.join(pasta, rel), "%s/%s" % (nome, rel))
    print("OK: %d arquivo(s) em %s" % (len(arquivos), destino))
    print("Para instalar: Personalizar > Habilidades > Enviar (conferir na configuração da conta).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
