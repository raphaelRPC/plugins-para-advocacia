#!/usr/bin/env python3
"""Lê uma peça boa do escritório em .docx e propõe o padrão visual (adaptar-juridico, motor-juridico).

Uso:
    python3 padrao_do_docx.py <peca.docx> [<outra-peca.docx> ...] [--saida padrao-proposto.md]

Só biblioteca padrão: abre o .docx como zip e lê word/document.xml, word/styles.xml e a seção
da página. Não lê nem mostra o texto da peça: só a formatação.

O que procura:
- fonte e corpo do texto (os mais usados, contando os caracteres de cada trecho);
- espaçamento entre linhas, alinhamento e recuo da primeira linha (nos parágrafos longos);
- margens da página;
- a citação em recuo: parágrafos com recuo à esquerda de 2 cm ou mais (recuo, corpo e
  espaçamento mais usados);
- se o documento tem cabeçalho ou rodapé (sinal de papel timbrado).

Com mais de um .docx, junta as contagens e avisa quando as peças discordam.

A saída é a seção 1 do padrão visual (04-base/juridico/padrao-visual.md), com as chaves que o
script de .docx da minutar-peca lê. O que o script não achou, ou achou com dúvida, sai
[A CONFIRMAR]. É uma proposta: o advogado confirma antes de gravar.

Saída: 0 com a proposta; 1 quando falta o arquivo ou ele não é um .docx válido.
"""

import os
import re
import sys
import zipfile
from collections import Counter

TWIP_CM = 567.0


def cm(twips):
    return round(int(twips) / TWIP_CM, 1)


def numero(valor):
    texto = ("%.2f" % valor).rstrip("0").rstrip(".")
    return texto.replace(".", ",")


def atributo(xml, tag, nome):
    m = re.search(r"<w:%s\b[^>]*\bw:%s=\"([^\"]+)\"" % (tag, nome), xml)
    return m.group(1) if m else None


def ler_docx(caminho):
    if not os.path.isfile(caminho):
        raise ValueError("não encontrei o arquivo: %s" % caminho)
    try:
        z = zipfile.ZipFile(caminho)
        doc = z.read("word/document.xml").decode("utf-8")
    except (zipfile.BadZipFile, KeyError):
        raise ValueError("não parece um .docx válido: %s" % caminho)
    estilos = z.read("word/styles.xml").decode("utf-8") if "word/styles.xml" in z.namelist() else ""
    tem_cabecalho = any(n.startswith("word/header") for n in z.namelist())
    tem_rodape = any(n.startswith("word/footer") for n in z.namelist())
    return doc, estilos, tem_cabecalho, tem_rodape


def padroes_dos_estilos(estilos):
    fonte = corpo = None
    dd = re.search(r"<w:docDefaults>(.*?)</w:docDefaults>", estilos, re.S)
    if dd:
        fonte = atributo(dd.group(1), "rFonts", "ascii")
        sz = atributo(dd.group(1), "sz", "val")
        corpo = int(sz) / 2.0 if sz else None
    normal = re.search(r"<w:style\b[^>]*w:styleId=\"Normal\"[^>]*>(.*?)</w:style>", estilos, re.S)
    if normal:
        fonte = atributo(normal.group(1), "rFonts", "ascii") or fonte
        sz = atributo(normal.group(1), "sz", "val")
        corpo = int(sz) / 2.0 if sz else corpo
    return fonte, corpo


def analisar(arquivos):
    c = {k: Counter() for k in ("fonte", "corpo", "espacamento", "alinhamento", "recuo", "rec_cit", "corpo_cit", "esp_cit",
                                 "m_sup", "m_inf", "m_esq", "m_dir")}
    timbre, discordancias = [], []
    por_arquivo = []
    for caminho in arquivos:
        doc, estilos, cab, rod = ler_docx(caminho)
        fonte_padrao, corpo_padrao = padroes_dos_estilos(estilos)
        if cab or rod:
            timbre.append(os.path.basename(caminho))
        sect = re.findall(r"<w:pgMar\b[^>]*/>", doc)
        if sect:
            ultimo = sect[-1]
            for chave_cnt, nome in (("m_sup", "top"), ("m_inf", "bottom"), ("m_esq", "left"), ("m_dir", "right")):
                v = atributo(ultimo, "pgMar", nome)
                if v:
                    c[chave_cnt][cm(v)] += 1
        fontes_deste = Counter()
        for p in re.findall(r"<w:p\b[ >].*?</w:p>", doc, re.S):
            ppr = re.search(r"<w:pPr>(.*?)</w:pPr>", p, re.S)
            ppr = ppr.group(1) if ppr else ""
            textos = re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", p, re.S)
            tamanho = sum(len(t) for t in textos)
            if not tamanho:
                continue
            esquerda = atributo(ppr, "ind", "left") or atributo(ppr, "ind", "start")
            primeira = atributo(ppr, "ind", "firstLine")
            linha = atributo(ppr, "spacing", "line")
            regra = atributo(ppr, "spacing", "lineRule") or "auto"
            jc = atributo(ppr, "jc", "val")
            corpos = []
            for r in re.findall(r"<w:r\b[ >].*?</w:r>", p, re.S):
                t = sum(len(x) for x in re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", r, re.S))
                if not t:
                    continue
                f = atributo(r, "rFonts", "ascii") or fonte_padrao
                sz = atributo(r, "sz", "val")
                s = int(sz) / 2.0 if sz else corpo_padrao
                if f:
                    c["fonte"][f] += t
                    fontes_deste[f] += t
                if s:
                    corpos.append((s, t))
            espac = round(int(linha) / 240.0, 2) if (linha and regra == "auto") else None
            e_citacao = esquerda is not None and cm(esquerda) >= 2.0
            if e_citacao:
                c["rec_cit"][cm(esquerda)] += 1
                for s, t in corpos:
                    c["corpo_cit"][s] += t
                if espac:
                    c["esp_cit"][espac] += 1
            elif tamanho >= 120:
                for s, t in corpos:
                    c["corpo"][s] += t
                if espac:
                    c["espacamento"][espac] += 1
                c["alinhamento"]["justificado" if jc in ("both", "distribute") else "esquerda"] += 1
                c["recuo"][cm(primeira) if primeira else 0.0] += 1
        if fontes_deste:
            por_arquivo.append((os.path.basename(caminho), fontes_deste.most_common(1)[0][0]))
    if len(set(f for _, f in por_arquivo)) > 1:
        discordancias.append("as peças usam fontes diferentes: %s" % ", ".join("%s em %s" % (f, a) for a, f in por_arquivo))
    return c, timbre, discordancias


def valor(contador, formatar=numero, minimo=1):
    if not contador or sum(contador.values()) < minimo:
        return None, False
    mais, n = contador.most_common(1)[0]
    duvida = len(contador) > 1 and n < 0.7 * sum(contador.values())
    return (formatar(mais) if formatar else mais), duvida


def main(argv):
    args = list(argv[1:])
    saida = None
    if "--saida" in args:
        i = args.index("--saida")
        if i + 1 >= len(args):
            print("ERRO: --saida precisa do caminho do arquivo.")
            return 1
        saida = args[i + 1]
        del args[i:i + 2]
    if "--ajuda" in args or "--help" in args:
        print(__doc__)
        return 0
    if not args:
        print("ERRO: diga qual peça .docx ler (uma peça boa do escritório, de preferência anonimizada).")
        print("Exemplo: python3 scripts/padrao_do_docx.py escritorio/04-base/juridico/modelos/peticao-inicial/modelo.docx")
        return 1
    try:
        c, timbre, discordancias = analisar(args)
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1

    linhas = []
    def item(chave_txt, contador, formatar=numero, nota=""):
        v, duvida = valor(contador, formatar)
        if v is None:
            linhas.append("- %s: [A CONFIRMAR] (não achei na peça)" % chave_txt)
        elif duvida:
            linhas.append("- %s: %s [A CONFIRMAR] (o mais usado, mas a peça varia: %s)%s" % (
                chave_txt, v, ", ".join(str(formatar(k) if formatar else k) for k, _ in contador.most_common(3)), nota))
        else:
            linhas.append("- %s: %s%s" % (chave_txt, v, nota))

    item("fonte", c["fonte"], formatar=None)
    item("corpo", c["corpo"])
    item("espacamento", c["espacamento"])
    item("alinhamento", c["alinhamento"], formatar=None)
    item("recuo_primeira_linha", c["recuo"])
    item("margem_superior", c["m_sup"])
    item("margem_inferior", c["m_inf"])
    item("margem_esquerda", c["m_esq"])
    item("margem_direita", c["m_dir"])
    if c["rec_cit"]:
        item("recuo_citacao", c["rec_cit"])
        item("corpo_citacao", c["corpo_cit"])
        item("espacamento_citacao", c["esp_cit"])
    else:
        linhas += ["- recuo_citacao: [A CONFIRMAR] (nenhum parágrafo com recuo de 2 cm ou mais: a peça não tem citação longa?)",
                   "- corpo_citacao: [A CONFIRMAR]", "- espacamento_citacao: [A CONFIRMAR]"]
    if timbre:
        linhas.append("- timbre: [A CONFIRMAR] (%s tem cabeçalho ou rodapé: se for o papel timbrado, salve uma cópia "
                      "sem o texto da peça como 04-base/juridico/timbre.docx e escreva aqui timbre.docx)" % ", ".join(timbre))
    else:
        linhas.append("- timbre: sem timbre (a peça não tem cabeçalho nem rodapé) [A CONFIRMAR]")

    texto = "\n".join(["## 1. O que o script de .docx lê", "",
                       "Proposta lida de: %s. Confirme cada linha com o advogado antes de gravar." % ", ".join(os.path.basename(a) for a in args), ""]
                      + linhas + [""] + ["AVISO: %s" % d for d in discordancias])
    if saida:
        with open(saida, "w", encoding="utf-8") as f:
            f.write(texto.rstrip() + "\n")
        print("Proposta gravada em %s." % saida)
    print(texto.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
