#!/usr/bin/env python3
"""Monta e confere a linha nova da carteira.csv do motor-experiencia.

Uso:
    python3 linha_da_carteira.py <carteira.csv> campo=valor [campo=valor ...] [--gravar] [--criar]

Exemplo:
    python3 linha_da_carteira.py escritorio/07-operacao/experiencia/carteira.csv \\
        codigo=C-2026-0001 nome_curto=Marta area=previdenciario \\
        "tipo_de_caso=restabelecimento de auxílio" responsavel=advogada inicio=2026-03-20

O que faz:
- Lê a carteira (vírgula ou ponto e vírgula, com ou sem BOM) e confere se a
  primeira linha tem as colunas de docs/carteira.md do motor-experiencia.
- Monta a linha com os campos dados. Os que faltam recebem o padrão de
  entrada: fase=entrada, reclamacao_aberta=nao, pediu_para_nao_receber=nao,
  atualizado_em=hoje; os outros ficam vazios.
- Recusa a linha se: o código já está na carteira (cliente com segundo caso
  usa o sufixo -2, como C-2026-0001-2); falta codigo, nome_curto, area,
  tipo_de_caso, responsavel ou inicio; uma data não está em AAAA-MM-DD ou
  DD/MM/AAAA; um campo de opção tem valor fora da lista; algum valor tem
  vírgula, ponto e vírgula ou quebra de linha; algum valor parece CPF, número
  de processo, telefone ou e-mail (a carteira guarda o mínimo).
- Sem --gravar, só mostra a linha. Se a carteira ainda não existe, mostra
  também a primeira linha de colunas que seria criada, e não grava nada.
- Com --gravar, acrescenta a linha no fim do arquivo, com o mesmo separador
  que ele já usa. Nunca apaga nem reescreve.
- --criar (junto com --gravar): se a carteira não existe, cria com a primeira
  linha de docs/carteira.md (só use quando o motor-experiencia está em uso).

Saída: 0 quando a linha está certa (mostrada, ou gravada com --gravar); 1
quando falta coluna, um campo está errado, o código já existe ou, com
--gravar sem --criar, a carteira não existe.
"""

import csv
import datetime
import io
import os
import re
import sys
import unicodedata

COLUNAS = [
    "codigo", "nome_curto", "area", "tipo_de_caso", "responsavel", "inicio", "fase",
    "ultimo_contato", "ultimo_contato_tipo", "proximo_contato", "motivo_proximo_contato",
    "proximo_compromisso", "data_compromisso", "documentos_pendentes", "humor",
    "reclamacao_aberta", "resumo_mensal", "pagina_do_caso", "satisfacao",
    "pediu_para_nao_receber", "encerrado_em", "atualizado_em",
]
OBRIGATORIOS = ["codigo", "nome_curto", "area", "tipo_de_caso", "responsavel", "inicio"]
DATAS = ["inicio", "ultimo_contato", "proximo_contato", "data_compromisso", "encerrado_em", "atualizado_em"]
OPCOES = {
    "fase": ["entrada", "documentos", "preparacao", "protocolado", "aguardando", "audiencia-pericia",
             "decisao", "recurso", "cumprimento", "encerramento", "encerrado"],
    "ultimo_contato_tipo": ["mensagem", "ligacao", "reuniao", "resumo", "pagina"],
    "motivo_proximo_contato": ["boas-vindas", "ligacao-pendente", "resumo-mensal", "maximo-sem-noticia",
                               "compromisso", "documento", "retorno-combinado", "pesquisa", "depois-do-caso"],
    "proximo_compromisso": ["audiencia", "pericia", "reuniao", "prazo-do-cliente"],
    "humor": ["tranquilo", "ansioso", "insatisfeito", "a-confirmar"],
    "reclamacao_aberta": ["sim", "nao"],
    "resumo_mensal": ["sim", "nao"],
    "pagina_do_caso": ["link", "pdf", "os-dois", "nao"],
    "pediu_para_nao_receber": ["sim", "nao"],
}
PADRAO = {"fase": "entrada", "reclamacao_aberta": "nao", "pediu_para_nao_receber": "nao", "humor": "a-confirmar"}
RE_CODIGO = re.compile(r"^C-\d{4}-\d{4}(-\d+)?$")
SENSIVEIS = [
    (re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "parece CPF"),
    (re.compile(r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b"), "parece número de processo"),
    (re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b"), "parece telefone"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "parece e-mail"),
]


def normal(texto):
    texto = unicodedata.normalize("NFD", (texto or "").strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def ler_data(texto):
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(texto.strip()[:10], formato).date()
        except ValueError:
            continue
    return None


def ler_carteira(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            texto = bruto.decode(codificacao)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("não consegui ler a carteira como texto (UTF-8 ou Windows-1252)")
    linhas_txt = [l for l in texto.splitlines() if l.strip()]
    if not linhas_txt:
        raise ValueError("a carteira está vazia, sem nem a primeira linha de colunas: %s" % caminho)
    separador = ";" if linhas_txt[0].count(";") > linhas_txt[0].count(",") else ","
    linhas = [l for l in csv.reader(io.StringIO(texto), delimiter=separador) if any(c.strip() for c in l)]
    nomes = [normal(c).replace(" ", "_") for c in linhas[0]]
    faltam = [c for c in COLUNAS if c not in nomes]
    if faltam:
        raise ValueError("faltam colunas na carteira.csv: %s. A primeira linha precisa ser a de docs/carteira.md do motor-experiencia."
                         % ", ".join(faltam))
    i = nomes.index("codigo")
    codigos = {l[i].strip().upper() for l in linhas[1:] if i < len(l)}
    codificacao = "utf-8" if codificacao == "utf-8-sig" else codificacao
    fim_de_linha = "\r\n" if "\r\n" in texto else "\n"
    return separador, codigos, texto.endswith("\n") or texto.endswith("\r"), codificacao, fim_de_linha


def conferir(valores, codigos):
    erros = []
    for campo in OBRIGATORIOS:
        if not valores.get(campo):
            erros.append("falta %s" % campo)
    codigo = valores.get("codigo", "")
    if codigo and not RE_CODIGO.match(codigo):
        erros.append("codigo \"%s\" fora do formato C-AAAA-NNNN (segundo caso: C-AAAA-NNNN-2)" % codigo)
    if codigo and codigo.upper() in codigos:
        erros.append("o código %s já está na carteira; se é um segundo caso do mesmo cliente, use %s-2" % (codigo, codigo))
    for campo, valor in valores.items():
        if any(s in valor for s in (",", ";", "\n", "\r")):
            erros.append("%s tem vírgula, ponto e vírgula ou quebra de linha: troque a frase" % campo)
        for regex, motivo in SENSIVEIS:
            if campo not in DATAS and campo != "codigo" and regex.search(valor):
                erros.append("%s %s: a carteira guarda só o mínimo (docs/carteira.md, regra 4)" % (campo, motivo))
    for campo in DATAS:
        v = valores.get(campo, "")
        if v:
            d = ler_data(v)
            if d is None:
                erros.append("%s com data inválida: %s (use AAAA-MM-DD)" % (campo, v))
            else:
                valores[campo] = d.isoformat()
    for campo, opcoes in OPCOES.items():
        v = valores.get(campo, "")
        if v:
            if normal(v) not in opcoes:
                erros.append("%s = \"%s\" fora das opções: %s" % (campo, v, " | ".join(opcoes)))
            else:
                valores[campo] = normal(v)
    v = valores.get("documentos_pendentes", "")
    if v and not v.isdigit():
        erros.append("documentos_pendentes precisa ser um número (o detalhe fica em clientes/<codigo>/documentos.md)")
    v = valores.get("satisfacao", "")
    if v and not (v.isdigit() and 0 <= int(v) <= 10):
        erros.append("satisfacao precisa ser uma nota de 0 a 10, ou vazio")
    if len(valores.get("tipo_de_caso", "").split()) > 5:
        erros.append("tipo_de_caso com mais de 5 palavras")
    return erros


def main(argv):
    if "--ajuda" in argv or "--help" in argv:
        print(__doc__)
        return 0
    opcoes = [a for a in argv[1:] if a.startswith("--")]
    args = [a for a in argv[1:] if not a.startswith("--")]
    caminhos = [a for a in args if "=" not in a]
    pares = [a for a in args if "=" in a]
    if len(caminhos) != 1 or not pares:
        print("ERRO: diga o caminho da carteira.csv e os campos (campo=valor).")
        print("Exemplo: python3 scripts/linha_da_carteira.py escritorio/07-operacao/experiencia/carteira.csv codigo=C-2026-0001 nome_curto=Marta ...")
        return 1
    caminho = caminhos[0]

    valores = {}
    for par in pares:
        campo, _, valor = par.partition("=")
        campo = normal(campo).replace(" ", "_")
        if campo not in COLUNAS:
            print("ERRO: campo desconhecido \"%s\". Os campos são os de docs/carteira.md: %s" % (campo, ", ".join(COLUNAS)))
            return 1
        valores[campo] = valor.strip()
    for campo, valor in PADRAO.items():
        valores.setdefault(campo, valor)
    valores.setdefault("atualizado_em", datetime.date.today().isoformat())

    criou = False
    if not os.path.isfile(caminho):
        if "--gravar" in opcoes and "--criar" not in opcoes:
            print("ERRO: não achei a carteira em: %s" % caminho)
            print("Nada foi gravado. Se o motor-experiencia está em uso e a carteira ainda não existe, rode de novo com --gravar --criar.")
            return 1
        separador, codigos, termina_com_quebra, codificacao, fim_de_linha = ",", set(), True, "utf-8", "\n"
        criou = True
    else:
        try:
            separador, codigos, termina_com_quebra, codificacao, fim_de_linha = ler_carteira(caminho)
        except ValueError as erro:
            print("ERRO: %s" % erro)
            return 1

    erros = conferir(valores, codigos)
    if erros:
        print("ERRO: a linha não está pronta. Nada foi gravado.")
        for e in erros:
            print("  - %s" % e)
        return 1

    buf = io.StringIO()
    csv.writer(buf, delimiter=separador, lineterminator=fim_de_linha).writerow([valores.get(c, "") for c in COLUNAS])
    linha = buf.getvalue()
    if criou:
        print("A carteira ainda não existe em %s. Com o ok, ela seria criada assim:" % caminho)
        print()
        print("Primeira linha (colunas de docs/carteira.md do motor-experiencia):")
        print(",".join(COLUNAS))
        print()
    print("Linha da carteira (separador \"%s\"):" % separador)
    print(linha.rstrip("\r\n"))

    if "--gravar" not in opcoes:
        print()
        if criou:
            print("Só mostrei, nada foi criado. Para criar a carteira com estas duas linhas, rode de novo com --gravar --criar, depois do ok.")
        else:
            print("Só mostrei. Para gravar no fim da carteira, rode de novo com --gravar, depois do ok.")
        return 0
    if criou:
        pasta = os.path.dirname(os.path.abspath(caminho))
        os.makedirs(pasta, exist_ok=True)
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            f.write(",".join(COLUNAS) + "\n" + linha)
        print("OK: carteira criada em %s, com a primeira linha de colunas e esta linha." % caminho)
        return 0
    with open(caminho, "a", encoding=codificacao, newline="") as f:
        if not termina_com_quebra:
            f.write(fim_de_linha)
        f.write(linha)
    print("OK: linha acrescentada no fim de %s." % caminho)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
