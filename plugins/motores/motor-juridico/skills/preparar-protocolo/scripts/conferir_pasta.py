#!/usr/bin/env python3
"""Confere a pasta dos arquivos a protocolar (motor-juridico, preparar-protocolo).

Olha cada arquivo da pasta e aponta o que o sistema do tribunal pode recusar ou o que
foge do padrão do escritório:

  nome      no padrão da ficha (campo nome_dos_arquivos: número, hífen, descrição,
            minúsculas, sem acento, sem espaço), sem número que pareça CPF ou processo
  ordem     numeração sem buraco e sem repetição, começando em 1, a peça em primeiro;
            com --esperados, os documentos do checklist na ordem combinada
  tamanho   por arquivo e da pasta, contra o limite informado (sempre [CONFERIR] no
            próprio sistema); arquivo vazio
  PDF       extensão .pdf e assinatura de PDF nos primeiros bytes
  sobra     arquivo oculto ou temporário, subpasta
  minuta    com --minuta, a versão final em .md ou .txt sem nenhuma marcação
            ([CONFERIR], [A PREENCHER], [A DEFINIR], [A CONFIRMAR] ou outra entre colchetes).
            O cabeçalho YAML e a seção interna "Antes de protocolar" não são a peça e ficam
            de fora. Campo entre chaves ({DATA DO PROTOCOLO}) é preenchido de propósito por
            quem protocola: sai como aviso, não como problema

O script não abre o conteúdo dos arquivos da pasta: lê só o nome, o tamanho e os
primeiros 5 bytes (para saber se é PDF). Não altera, não move e não apaga nada.
Só biblioteca padrão (Python 3.9+).

Uso:
  python3 conferir_pasta.py PASTA [opções]

Opções:
  --nomes TEXTO        campo nome_dos_arquivos da ficha, como está
                       (ex.: "01-peticao.pdf, 02-procuracao.pdf, 03-documentos-pessoais.pdf").
                       Dele saem a largura do número, o separador e a extensão. Vazio ou só
                       [A PREENCHER]: padrão do script (01-descricao.pdf), com aviso
  --esperados TEXTO    os documentos do checklist, na ordem, separados por vírgula
                       (ex.: "peticao, procuracao, documentos-pessoais")
  --limite-mb N        limite por arquivo, em MB, do campo limite_de_tamanho (o valor vem do
                       sistema e é [CONFERIR] lá). Aceita "5", "5,5" ou "5 MB"
  --limite-total-mb N  limite da soma dos arquivos, se o sistema tiver um
  --minuta ARQUIVO     a versão final da peça em .md ou .txt, para procurar marcação

Sai com código 1 e uma mensagem que começa com "ERRO:" quando a pasta não existe, não é
pasta, está vazia ou quando um valor de opção não dá para ler. Com a pasta lida, sai com
código 0 e a primeira linha diz "PRONTA PARA A PESSOA PROTOCOLAR" ou "CORRIGIR ANTES".
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

OCULTOS = {".ds_store", "thumbs.db", "desktop.ini"}
MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]")
OUTRA_MARCACAO = re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 ]{2,}[^\]]*\]")
CPF = re.compile(r"(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)")
CNJ = re.compile(r"(?<!\d)\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}(?!\d)")
PLACEHOLDER = re.compile(r"\[[^\]]*\]")
CAMPO_ENVIO = re.compile(r"(?<!\{)\{[^{}\n]+\}(?!\})")


# ---------- corte do que não é a peça (o mesmo da md_para_docx, da minutar-peca) ----------
# Copiado de propósito em cada script que lê a peça: a habilidade pode ir sozinha num zip.
RE_TITULO_INTERNO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_FIM_INTERNO = re.compile(r"^\s*<!--\s*fim:\s*antes de (protocolar|enviar)\s*-->\s*$", re.I)


def _minusculo_sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def cortar_interno(linhas):
    """Troca por linha vazia o que é controle interno do escritório e não é a peça.

    Sai: o cabeçalho YAML do topo (entre linhas ---); a seção interna (título de qualquer
    nível que começa com "Antes de protocolar" ou "Antes de enviar"), até o próximo título
    do mesmo nível ou maior, ou até a linha <!-- fim: antes de protocolar -->; e os
    comentários HTML. A numeração das linhas não muda.
    Devolve (linhas_da_peca, achou_secao_interna, quantas_linhas_internas).
    """
    linhas = list(linhas)
    interno = [False] * len(linhas)
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                for j in range(0, i + 1):
                    interno[j] = True
                break
    achou, n_secao = False, 0
    i, em_codigo = 0, False
    while i < len(linhas):
        limpa = linhas[i].strip()
        if limpa.startswith("```"):
            em_codigo = not em_codigo
        m = RE_TITULO_INTERNO.match(limpa) if not em_codigo else None
        titulo = _minusculo_sem_acento(m.group(2)) if m else ""
        if m and titulo.startswith(("antes de protocolar", "antes de enviar")):
            achou = True
            nivel = len(m.group(1))
            interno[i] = True
            n_secao += 1
            j = i + 1
            while j < len(linhas):
                lj = linhas[j].strip()
                if RE_FIM_INTERNO.match(lj):
                    interno[j] = True
                    n_secao += 1
                    j += 1
                    break
                mj = RE_TITULO_INTERNO.match(lj)
                if mj and len(mj.group(1)) <= nivel:
                    break
                interno[j] = True
                n_secao += 1
                j += 1
            i = j
            continue
        i += 1
    dentro = False
    for i, linha in enumerate(linhas):
        if interno[i]:
            continue
        if dentro:
            interno[i] = True
            if "-->" in linha:
                dentro = False
            continue
        if "<!--" in linha:
            antes, _, depois = linha.partition("<!--")
            if "-->" in depois:
                linhas[i] = antes + depois.split("-->", 1)[1]
                if not linhas[i].strip():
                    interno[i] = True
            else:
                linhas[i] = antes
                dentro = True
                if not antes.strip():
                    interno[i] = True
    return [("" if interno[n] else l) for n, l in enumerate(linhas)], achou, n_secao


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto or "") if not unicodedata.combining(c))


def chave(texto):
    t = sem_acento(texto or "").lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def ler_mb(texto, opcao):
    if texto is None:
        return None
    t = PLACEHOLDER.sub("", texto).strip().lower().replace("mb", "").strip()
    if not t:
        return None
    t = t.replace(",", ".")
    try:
        v = float(t)
    except ValueError:
        falhar(f"{opcao} `{texto}` não é um número de MB. Use, por exemplo, 5 ou \"5 MB\".")
    if v <= 0:
        falhar(f"{opcao} precisa ser maior que zero.")
    return v


def padrao_da_ficha(texto):
    """Devolve (largura do número, separador, extensão, descrição do primeiro exemplo, de onde veio)."""
    limpo = PLACEHOLDER.sub(" ", texto or "")
    exemplos = re.findall(r"(\d+)([-_ .])([A-Za-z0-9][\w-]*)\.([A-Za-z0-9]{2,4})", limpo)
    if not exemplos:
        return 2, "-", "pdf", "", "padrão do script (01-descricao.pdf), confirme o campo nome_dos_arquivos da ficha"
    largura = len(exemplos[0][0])
    sep = exemplos[0][1]
    ext = exemplos[0][3].lower()
    return largura, sep, ext, chave(exemplos[0][2]), f"lido da ficha: \"{(texto or '').strip()}\""


def tamanho(n):
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f} MB".replace(".", ",")
    if n >= 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n} B"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pasta")
    p.add_argument("--nomes")
    p.add_argument("--esperados")
    p.add_argument("--limite-mb")
    p.add_argument("--limite-total-mb")
    p.add_argument("--minuta")
    args = p.parse_args()

    pasta = Path(args.pasta)
    if not pasta.exists():
        falhar(f"não encontrei a pasta `{args.pasta}`. Confira o caminho da pasta onde estão os "
               "arquivos a protocolar. Nada foi conferido.")
    if not pasta.is_dir():
        falhar(f"`{args.pasta}` é um arquivo. Passe a pasta que contém os arquivos a protocolar.")
    itens = sorted(pasta.iterdir(), key=lambda f: f.name.lower())
    if not itens:
        falhar(f"a pasta `{args.pasta}` está vazia. Junte ali a peça final e os documentos, no "
               "padrão de nome da ficha. Nada foi conferido.")

    largura, sep, ext, primeira_desc, origem = padrao_da_ficha(args.nomes)
    limite = ler_mb(args.limite_mb, "--limite-mb")
    limite_total = ler_mb(args.limite_total_mb, "--limite-total-mb")
    esperados = [chave(e) for e in re.split(r"[,;\n]", PLACEHOLDER.sub("", args.esperados or "")) if chave(e)]
    sep_re = re.escape(sep)
    padrao = re.compile(rf"^(\d{{{largura}}}){sep_re}([a-z0-9]+(?:-[a-z0-9]+)*)\.{re.escape(ext)}$")

    avisos = []
    if args.nomes is not None and origem.startswith("padrão"):
        avisos.append("campo nome_dos_arquivos da ficha vazio ou sem exemplo: usei o padrão do script")
    if limite is None:
        avisos.append("sem --limite-mb: tamanho mostrado, mas não comparado. O limite vem do sistema [CONFERIR]")

    linhas, problemas, total = [], [], 0
    numerados = []
    for f in itens:
        obs = []
        nome = f.name
        if f.is_dir():
            problemas.append(f"`{nome}/` é uma subpasta: o sistema recebe arquivos soltos [CONFERIR]; tire os arquivos de dentro ou deixe de fora")
            linhas.append((nome + "/", "-", "-", "subpasta"))
            continue
        if nome.lower() in OCULTOS or nome.startswith((".", "~$")):
            problemas.append(f"`{nome}` é arquivo oculto ou temporário: tirar da pasta antes de protocolar")
            linhas.append((nome, tamanho(f.stat().st_size), "-", "oculto ou temporário"))
            continue
        bytes_ = f.stat().st_size
        total += bytes_
        with f.open("rb") as h:
            inicio = h.read(5)
        e_pdf = inicio == b"%PDF-"
        if bytes_ == 0:
            obs.append("arquivo vazio")
        if f.suffix.lower() != ".pdf":
            obs.append(f"extensão `{f.suffix or 'nenhuma'}`: o sistema costuma pedir PDF [CONFERIR]")
        elif not e_pdf and bytes_ > 0:
            obs.append("tem nome de .pdf, mas não é PDF por dentro: gerar o PDF de novo")
        m = padrao.match(nome)
        if not m:
            motivo = []
            if nome != sem_acento(nome):
                motivo.append("acento")
            if " " in nome:
                motivo.append("espaço")
            if nome != nome.lower():
                motivo.append("maiúscula")
            if not re.match(r"^\d+", nome):
                motivo.append("sem número na frente")
            elif not re.match(rf"^\d{{{largura}}}(?!\d)", nome):
                motivo.append(f"número com largura diferente de {largura}")
            if sep == "-" and "_" in nome:
                motivo.append("sublinhado no lugar de hífen")
            obs.append("nome fora do padrão" + (f" ({', '.join(motivo)})" if motivo else "")
                       + f"; sugestão: `{sugestao(nome, largura, sep, ext, len(numerados) + 1)}`")
        if CPF.search(nome) or CNJ.search(nome):
            obs.append("o nome tem número que parece CPF ou processo: tirar do nome do arquivo")
        if limite and bytes_ > limite * 1024 * 1024:
            obs.append(f"acima do limite de {str(limite).replace('.', ',')} MB por arquivo [CONFERIR no sistema]: dividir ou reduzir")
        num = re.match(r"^(\d+)", nome)
        if num:
            numerados.append((int(num.group(1)), nome, chave(re.sub(r"^\d+[-_ .]*", "", f.stem))))
        else:
            numerados.append((None, nome, chave(f.stem)))
        linhas.append((nome, tamanho(bytes_), "sim" if e_pdf else "não", "; ".join(obs) or "ok"))
        problemas.extend(f"`{nome}`: {o}" for o in obs)

    # ordem
    numeros = [n for n, _, _ in numerados if n is not None]
    repetidos = sorted({n for n in numeros if numeros.count(n) > 1})
    for n in repetidos:
        problemas.append(f"número {n:0{largura}d} repetido: {', '.join(nm for x, nm, _ in numerados if x == n)}")
    if numeros:
        if min(numeros) != 1:
            problemas.append(f"a numeração começa em {min(numeros):0{largura}d}; a peça vai em {1:0{largura}d}")
        faltam = sorted(set(range(1, max(numeros) + 1)) - set(numeros))
        if faltam:
            problemas.append("buraco na numeração: falta " + ", ".join(f"{n:0{largura}d}" for n in faltam))
    ordenados = sorted([x for x in numerados if x[0] is not None], key=lambda x: x[0])
    if ordenados and primeira_desc:
        tok = primeira_desc.split("-")[0]
        if tok and tok not in ordenados[0][2]:
            problemas.append(f"o arquivo {ordenados[0][0]:0{largura}d} é `{ordenados[0][1]}`; pela ficha, a peça "
                             f"(`{primeira_desc}`) vai em primeiro")
    if esperados:
        posicoes = []
        for e in esperados:
            achou = [x for x in ordenados if e in x[2]]
            if not achou:
                problemas.append(f"documento do checklist sem arquivo: `{e}`")
            else:
                posicoes.append((e, achou[0][0]))
        seq = [pos for _, pos in posicoes]
        if seq != sorted(seq):
            problemas.append("documentos fora da ordem do checklist: "
                             + " · ".join(f"{e} em {pos:0{largura}d}" for e, pos in posicoes))
        for n, nome, desc in ordenados:
            if not any(e in desc for e in esperados):
                problemas.append(f"`{nome}` não está no checklist: confirmar com quem protocola se vai")
    if limite_total and total > limite_total * 1024 * 1024:
        problemas.append(f"a soma dos arquivos ({tamanho(total)}) passa o limite total de "
                         f"{str(limite_total).replace('.', ',')} MB [CONFERIR no sistema]")

    # minuta final
    minuta_txt = []
    if args.minuta:
        mp = Path(args.minuta)
        if not mp.exists():
            falhar(f"não encontrei a minuta `{args.minuta}`.")
        if mp.suffix.lower() not in {".md", ".txt"}:
            falhar("--minuta lê só .md ou .txt (a versão de texto da peça final). O PDF não é aberto.")
        bruto = mp.read_bytes()
        for cod in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                texto = bruto.decode(cod)
                break
            except UnicodeDecodeError:
                continue
        # cabeçalho YAML e seção interna "Antes de protocolar" não são a peça
        linhas_peca, achou_interno, _ = cortar_interno(texto.lstrip("\ufeff").splitlines())
        texto = "\n".join(linhas_peca)
        if not texto.strip():
            falhar(f"a minuta `{args.minuta}` está vazia depois de tirar o cabeçalho e a seção interna.")
        achadas = [m.group(0) for m in MARCACAO.finditer(texto)]
        outras = [m for m in OUTRA_MARCACAO.findall(texto) if not MARCACAO.match(m)]
        campos = sorted(set(m.group(0) for m in CAMPO_ENVIO.finditer(texto) if re.search(r"[A-Za-zÀ-ÿ]", m.group(0))))
        if campos:
            avisos.append("campos para preencher no envio, na minuta (entre chaves, não impedem o protocolo; "
                          "preencha no .docx antes de assinar): " + ", ".join(campos))
        if achou_interno:
            minuta_txt.append("seção interna \"Antes de protocolar\" fora da conferência (não é a peça)")
        if achadas or outras:
            problemas.append(f"a minuta `{mp.name}` ainda tem {len(achadas) + len(outras)} marcação(ões) entre "
                             "colchetes: a peça final não pode ter nenhuma (citacoes.md, regra 2)")
            minuta_txt.extend(sorted(set(achadas))[:10])
            minuta_txt.extend(sorted(set(outras))[:10])
        else:
            minuta_txt.append("nenhuma marcação entre colchetes no texto da peça")

    status = "CORRIGIR ANTES" if problemas else "PRONTA PARA A PESSOA PROTOCOLAR"
    out = [f"{status} · pasta `{pasta}` · {len(numerados)} arquivo(s), {tamanho(total)} no total", ""]
    out.append(f"Padrão de nome: {largura} dígito(s), separador `{sep}`, extensão .{ext} ({origem}).")
    if limite:
        out.append(f"Limite por arquivo: {str(limite).replace('.', ',')} MB, informado pelo escritório [CONFERIR no sistema].")
    if avisos:
        out.append("")
        out.append("Avisos:")
        out.extend(f"- {a}" for a in avisos)
    out.append("")
    out.append("| Arquivo | Tamanho | PDF | Observação |")
    out.append("|---|---|---|---|")
    for nome, tam, pdf, obs in linhas:
        out.append(f"| {nome} | {tam} | {pdf} | {obs} |")
    out.append("")
    out.append("## O que corrigir")
    out.extend(f"- {pr}" for pr in problemas) if problemas else out.append("Nada. Confira mesmo assim, no próprio sistema, formato e tamanho aceitos [CONFERIR].")
    if minuta_txt:
        out.append("")
        out.append("## Minuta final")
        out.extend(f"- {t}" for t in minuta_txt)
    out.append("")
    out.append("Assinar, usar o certificado e protocolar são da pessoa. O script leu só nome, tamanho e "
               "os primeiros bytes de cada arquivo, e não mudou nada.")
    print("\n".join(out))


def sugestao(nome, largura, sep, ext, ordem):
    stem = CPF.sub("", CNJ.sub("", Path(nome).stem))
    m = re.match(r"^(\d+)[-_ .]*(.*)$", stem)
    numero = int(m.group(1)) if m else ordem
    desc = chave(m.group(2) if m else stem)
    desc = desc.strip("-") or "documento"
    desc = re.sub(r"-+", "-", desc)
    return f"{numero:0{largura}d}{sep}{desc}.{ext}"


if __name__ == "__main__":
    main()
