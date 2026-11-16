#!/usr/bin/env python3
"""Monta um lote de minutas a partir da planilha do lote e da habilidade própria da peça (pecas-em-lote).

Uso (da pasta de trabalho):
    python3 montar_lote.py <planilha.csv> <pasta-da-habilidade-ou-mapa> --tese <nome-da-tese> \
        --raiz <escritorio/07-operacao/juridico ou escritorio/07-operacao/_treino/juridico> \
        [--so-conferir] [--decisao "advogada titular, AAAA-MM-DD"] [--registrar] \
        [--responsavel <função>] [--hoje AAAA-MM-DD]

O que lê:
- a planilha do lote (.csv com vírgula ou ponto e vírgula, com ou sem BOM, salva pelo Excel ou
  não). Colunas obrigatórias: codigo_caso e area, mais uma coluna para cada variável do mapa
  que não tem origem "ficha" (o título da coluna é o nome da variável; maiúsculas e acentos não
  importam). Coluna opcional: prazo_interno;
- o mapa da peça da habilidade própria (<pasta>/references/mapa-da-peca.md, ou o caminho do
  mapa): área, variáveis, valores do escritório, teses e o modelo entre
  <!-- modelo: inicio --> e <!-- modelo: fim -->.

O que confere em cada linha (a linha que falha não sai, e o relatório diz por quê):
1. codigo_caso preenchido, no formato C-AAAA-NNNN, sem repetir no lote;
2. area igual à área do mapa (a habilidade própria só faz aquela peça daquela área);
3. toda variável obrigatória preenchida;
4. cada valor no tipo certo: data (AAAA-MM-DD ou DD/MM/AAAA), mes (AAAA-MM ou MM/AAAA), valor,
   numero, genero (f ou m), opcao (só os valores da lista), lista (itens separados por ";").
Alertas que não barram, mas vão para o relatório: valor igual ao exemplo do mapa (pode ser
cópia do modelo) e o mesmo valor em todas as linhas numa variável do caso.

O que nunca faz: escolher tese (a tese do lote vem do advogado, em --tese e --decisao), conferir
citação (toda marca [CONFERIR] continua na minuta), aprovar, protocolar ou apagar arquivo.

--so-conferir   só confere e mostra a tabela do lote; não grava nada. Rode primeiro assim.
Sem --so-conferir, grava (exige --decisao, o registro de quem definiu a tese do lote):
- cada minuta em <raiz>/casos/<codigo>/minutas/<peca>-v<n>.md (n é a próxima versão livre);
- o relatório em <raiz>/lotes/AAAA-MM-DD-<peca>.md, com as linhas propostas do pecas.csv;
- com --registrar, acrescenta essas linhas em <raiz>/pecas.csv (cria com os títulos se faltar).
  No treino (--raiz .../_treino/juridico), o registro é <raiz>/pecas-em-lote/pecas.csv, para não
  colidir com o pecas.csv de treino das outras habilidades.

Saída: 0 quando pelo menos uma linha passou; 2 quando nenhuma passou; 1 em erro de uso, de
arquivo, de coluna obrigatória ou de mapa.
"""

import csv
import datetime as dt
import io
import os
import re
import sys
import unicodedata

COLUNAS_PECAS = ["id", "codigo_caso", "cliente_curto", "area", "peca", "origem", "prazo_interno", "etapa",
                 "responsavel", "tese", "habilidade_usada", "citacoes", "dados", "protocolo_sistema",
                 "protocolo_numero", "protocolo_data", "atualizado_em"]
RE_CODIGO = re.compile(r"^C-\d{4}-\d{4}$")
RE_VAR = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")
RE_GEN = re.compile(r"\{\{\s*genero\s*:([^|{}]*)\|([^{}]*)\}\}")
RE_SE = re.compile(r"\{\{#se\s+([a-z0-9_]+)\s*=\s*([^}]+?)\s*\}\}(.*?)\{\{/se\}\}", re.S)
RE_CONFERIR = re.compile(r"\[CONFERIR[^\]\n]*\]", re.I)


class Erro(Exception):
    pass


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn").lower().strip()


def chave(texto):
    return re.sub(r"[^a-z0-9]+", "_", sem_acento(texto)).strip("_")


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    raise Erro("não consegui ler como texto: %s" % caminho)


def ler_csv(caminho):
    if not os.path.isfile(caminho):
        raise Erro("não encontrei a planilha: %s" % caminho)
    texto = ler_texto(caminho)
    linhas = [l for l in texto.splitlines() if l.strip()]
    if not linhas:
        raise Erro("a planilha está vazia: %s" % caminho)
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    tabela = list(leitor)
    titulos = [chave(t) for t in tabela[0]]
    dados = []
    for numero, valores in enumerate(tabela[1:], start=2):
        if not any(v.strip() for v in valores):
            continue
        dados.append((numero, {titulos[i]: (valores[i].strip() if i < len(valores) else "") for i in range(len(titulos))}))
    return titulos, dados, sep


# ---------- o mapa ----------

def secao(texto, titulo_inicio):
    """Texto da seção cujo título (## N. Nome) começa com titulo_inicio, até o próximo ##."""
    m = re.search(r"^##\s+(?:\d+\.\s*)?%s[^\n]*\n(.*?)(?=^##\s|\Z)" % re.escape(titulo_inicio), texto, re.M | re.S | re.I)
    return m.group(1) if m else None


def tabela_md(bloco):
    linhas = [l.strip() for l in bloco.splitlines() if l.strip().startswith("|")]
    if len(linhas) < 2:
        return []
    def cel(l):
        l = l.strip()[1:]
        if l.endswith("|"):
            l = l[:-1]
        return [c.strip().strip("`") for c in re.split(r"(?<!\\)\|", l)]
    titulos = [chave(c) for c in cel(linhas[0])]
    saida = []
    for l in linhas[2:]:
        c = cel(l)
        saida.append({titulos[i]: (c[i] if i < len(c) else "") for i in range(len(titulos))})
    return saida


def ler_mapa(caminho):
    if os.path.isdir(caminho):
        candidato = os.path.join(caminho, "references", "mapa-da-peca.md")
        if not os.path.isfile(candidato):
            raise Erro("não achei references/mapa-da-peca.md dentro de %s" % caminho)
        caminho = candidato
    if not os.path.isfile(caminho):
        raise Erro("não encontrei o mapa da peça: %s" % caminho)
    texto = ler_texto(caminho)
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if not fm:
        raise Erro("o mapa não abre com o cabeçalho entre linhas --- (peca, area, versao)")
    cab = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", fm.group(1), re.M))
    for k in ("peca", "area", "versao"):
        if not cab.get(k):
            raise Erro("o cabeçalho do mapa não tem '%s'" % k)
    bloco_var = secao(texto, "Variáveis") or secao(texto, "Variaveis")
    if bloco_var is None:
        raise Erro("o mapa não tem a seção '## 3. Variáveis'")
    tab = tabela_md(bloco_var.split("###")[0])
    if not tab or "variavel" not in tab[0] or "tipo" not in tab[0]:
        raise Erro("a tabela de variáveis do mapa precisa das colunas variavel, tipo, origem, obrigatoria, exemplo, regra")
    variaveis = {}
    for linha in tab:
        nome = linha.get("variavel", "").strip()
        if not nome:
            continue
        variaveis[nome] = {
            "tipo": sem_acento(linha.get("tipo", "texto")) or "texto",
            "origem": sem_acento(linha.get("origem", "")),
            "obrigatoria": sem_acento(linha.get("obrigatoria", "sim")).startswith("s"),
            "exemplo": linha.get("exemplo", ""),
        }
    fixos = {}
    m = re.search(r"^###\s+Valores do escrit[óo]rio\s*\n(.*?)(?=^#|\Z)", texto, re.M | re.S | re.I)
    if m:
        for k, v in re.findall(r"^\s*[-*]\s*`?([a-z0-9_]+)`?\s*:\s*(.*?)\s*$", m.group(1), re.M):
            fixos[k] = v
    mm = re.search(r"<!--\s*modelo:\s*inicio\s*-->\s*\n(.*?)\n\s*<!--\s*modelo:\s*fim\s*-->", texto, re.S | re.I)
    if not mm:
        raise Erro("o mapa não tem o modelo entre <!-- modelo: inicio --> e <!-- modelo: fim -->")
    modelo = mm.group(1)
    teses = [l.get("tese", "").strip() for l in tabela_md(secao(texto, "Teses") or "") if l.get("tese", "").strip()]
    usadas = set(RE_VAR.findall(modelo)) | set(x[0] for x in RE_SE.findall(modelo))
    if RE_GEN.search(modelo):
        usadas.add("genero")
    faltam = sorted(v for v in usadas if v not in variaveis)
    if faltam:
        raise Erro("o modelo usa variável que não está na tabela do mapa: %s" % ", ".join(faltam))
    abre, fecha = len(re.findall(r"\{\{#se", modelo)), len(re.findall(r"\{\{/se\}\}", modelo))
    if abre != fecha:
        raise Erro("o modelo tem %d {{#se ...}} e %d {{/se}}: cada bloco precisa fechar" % (abre, fecha))
    sem_valor = [v for v, d in variaveis.items() if d["origem"] == "ficha" and d["obrigatoria"] and not fixos.get(v)]
    if sem_valor:
        raise Erro("variável de origem 'ficha' sem valor em 'Valores do escritório': %s" % ", ".join(sem_valor))
    return {"caminho": caminho, "peca": cab["peca"], "area": cab["area"], "versao": cab["versao"],
            "variaveis": variaveis, "fixos": fixos, "modelo": modelo, "teses": teses}


# ---------- valores ----------

def data(valor):
    v = valor.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return dt.datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def formatar(nome, tipo, valor):
    """Devolve (texto formatado, erro ou None)."""
    v = valor.strip()
    if tipo == "data":
        d = data(v)
        return (d.strftime("%d/%m/%Y"), None) if d else (v, "%s: data inválida (%s); use AAAA-MM-DD ou DD/MM/AAAA" % (nome, v))
    if tipo == "mes":
        m = re.fullmatch(r"(\d{4})-(\d{1,2})", v) or re.fullmatch(r"(\d{1,2})/(\d{4})", v)
        if not m:
            return v, "%s: mês inválido (%s); use AAAA-MM ou MM/AAAA" % (nome, v)
        a, b = m.groups()
        ano, mes = (a, b) if len(a) == 4 else (b, a)
        if not 1 <= int(mes) <= 12:
            return v, "%s: mês inválido (%s)" % (nome, v)
        return "%02d/%s" % (int(mes), ano), None
    if tipo == "valor":
        s = re.sub(r"(?i)r\$|\s", "", v)
        if re.fullmatch(r"\d{1,3}(\.\d{3})*(,\d{1,2})?|\d+(,\d{1,2})?", s):
            numero = float(s.replace(".", "").replace(",", "."))
        elif re.fullmatch(r"\d+\.\d{1,2}", s):
            numero = float(s)
        else:
            return v, "%s: valor inválido (%s); use 1.234,56" % (nome, v)
        inteiro, centavos = ("%.2f" % numero).split(".")
        inteiro = "{:,}".format(int(inteiro)).replace(",", ".")
        return "R$ %s,%s" % (inteiro, centavos), None
    if tipo == "numero":
        return (v, None) if re.fullmatch(r"\d+([.,]\d+)?", v) else (v, "%s: não é número (%s)" % (nome, v))
    if tipo == "genero":
        g = sem_acento(v)[:1]
        return (g, None) if g in ("f", "m") else (v, "%s: use f ou m (veio %s)" % (nome, v))
    if tipo.startswith("opcao"):
        opcoes = [sem_acento(o) for o in re.split(r"[/|,]", tipo[tipo.find("(") + 1:tipo.rfind(")")]) if o.strip()]
        return (sem_acento(v), None) if sem_acento(v) in opcoes else (v, "%s: '%s' fora das opções (%s)" % (nome, v, "/".join(opcoes)))
    if tipo == "lista":
        itens = [i.strip() for i in v.split(";") if i.strip()]
        if not itens:
            return v, "%s: lista vazia" % nome
        return (itens[0] if len(itens) == 1 else ", ".join(itens[:-1]) + " e " + itens[-1]), None
    return v, None


def renumerar(texto):
    """Refaz a numeração das listas numeradas (1., 2., 3.) depois dos blocos condicionais."""
    saida, n = [], 0
    for linha in texto.split("\n"):
        m = re.match(r"^(\s*)(\d+)\.\s+(?!\d)(.*)$", linha)
        if m and not re.match(r"^\s*\d+\.\d", linha):
            n += 1
            saida.append("%s%d. %s" % (m.group(1), n, m.group(3)))
            continue
        if linha.strip() and not m:
            n = 0
        saida.append(linha)
    return "\n".join(saida)


def montar(modelo, valores):
    modelo = re.sub(r"^[ \t]*(\{\{#se[^}]*\}\})[ \t]*\n", r"\1", modelo, flags=re.M)
    modelo = re.sub(r"\n[ \t]*(\{\{/se\}\})[ \t]*$", r"\1", modelo, flags=re.M)

    def se(m):
        return m.group(3) if sem_acento(valores.get(m.group(1), "")) == sem_acento(m.group(2)) else ""
    t = RE_SE.sub(se, modelo)
    t = RE_GEN.sub(lambda m: (m.group(1) if valores.get("genero") == "f" else m.group(2)), t)
    t = RE_VAR.sub(lambda m: valores.get(m.group(1), m.group(0)), t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return renumerar(t).strip() + "\n"


# ---------- principal ----------

def opcao(args, nome, padrao=None):
    if nome in args:
        i = args.index(nome)
        if i + 1 >= len(args) or args[i + 1].startswith("--"):
            raise Erro("%s precisa de um valor" % nome)
        valor = args[i + 1]
        del args[i:i + 2]
        return valor
    return padrao


def proxima_versao(pasta, peca):
    if not os.path.isdir(pasta):
        return 1
    ns = [int(m.group(1)) for f in os.listdir(pasta) for m in [re.match(r"^%s-v(\d+)\.md$" % re.escape(peca), f)] if m]
    return max(ns) + 1 if ns else 1


def ler_ids(caminho, ano):
    """Devolve (maior número do ano, separador, {(codigo, peca): id} das linhas que já existem)."""
    if not os.path.isfile(caminho):
        return 0, ",", {}
    titulos, dados, sep = ler_csv(caminho)
    maior, existentes = 0, {}
    for _, linha in dados:
        m = re.match(r"^P-%d-(\d+)$" % ano, linha.get("id", ""))
        if m:
            maior = max(maior, int(m.group(1)))
        if sem_acento(linha.get("etapa", "")) not in ("protocolada",):
            existentes[(linha.get("codigo_caso", "").upper(), sem_acento(linha.get("peca", "")))] = linha.get("id", "")
    return maior, sep, existentes


def main(argv):
    args = list(argv[1:])
    if "--ajuda" in args or "--help" in args:
        print(__doc__)
        return 0
    try:
        tese = opcao(args, "--tese")
        raiz = opcao(args, "--raiz")
        decisao = opcao(args, "--decisao")
        responsavel = opcao(args, "--responsavel", "")
        hoje_txt = opcao(args, "--hoje")
        so_conferir = "--so-conferir" in args
        registrar = "--registrar" in args
        args = [a for a in args if a not in ("--so-conferir", "--registrar")]
        if len(args) != 2:
            raise Erro("diga a planilha do lote e a pasta da habilidade própria (ou o mapa da peça).\n"
                       "Exemplo: python3 scripts/montar_lote.py lote.csv escritorio/04-base/habilidades-do-escritorio/"
                       "peticao-inicial-restabelecimento --tese restabelecimento-incapacidade "
                       "--raiz escritorio/07-operacao/_treino/juridico --so-conferir")
        if not tese:
            raise Erro("falta --tese: a tese do lote é escolhida pelo advogado antes de montar")
        if not raiz:
            raise Erro("falta --raiz (escritorio/07-operacao/juridico, ou _treino/juridico para casos fictícios)")
        if not so_conferir and not decisao:
            raise Erro("para gravar, falta --decisao com quem definiu a tese do lote e quando "
                       "(ex.: --decisao \"advogada titular, 2026-04-20\"). Para só conferir, use --so-conferir")
        hoje = data(hoje_txt) if hoje_txt else dt.date.today()
        if hoje is None:
            raise Erro("--hoje inválido: use AAAA-MM-DD")
        mapa = ler_mapa(args[1])
        if mapa["teses"] and chave(tese) not in [chave(x) for x in mapa["teses"]]:
            raise Erro("a tese '%s' não está na seção Teses do mapa (%s). Confira com o advogado"
                       % (tese, "; ".join(mapa["teses"])))
        titulos, linhas, _ = ler_csv(args[0])
    except Erro as erro:
        print("ERRO: %s" % erro)
        return 1

    variaveis = mapa["variaveis"]
    do_caso = {n: d for n, d in variaveis.items() if d["origem"] != "ficha"}
    faltam_col = [c for c in ("codigo_caso", "area") if c not in titulos]
    faltam_col += [n for n, d in do_caso.items() if d["obrigatoria"] and n not in titulos]
    if faltam_col:
        print("ERRO: a planilha não tem a(s) coluna(s) obrigatória(s): %s" % ", ".join(faltam_col))
        print("Colunas que a planilha deste lote precisa: codigo_caso, area, %s" % ", ".join(do_caso))
        return 1
    if not linhas:
        print("ERRO: a planilha tem só a linha de títulos; nenhum caso para montar.")
        return 1
    avisos = ["coluna '%s' não é variável do mapa e foi ignorada" % c for c in titulos
              if c not in do_caso and c not in ("codigo_caso", "area", "prazo_interno", "nome_curto", "cliente_curto")]
    avisos += ["variável opcional '%s' sem coluna na planilha: sai vazia" % n for n, d in do_caso.items()
               if not d["obrigatoria"] and n not in titulos]

    resultado = []
    vistos = {}
    for numero, linha in linhas:
        motivos, alertas, valores = [], [], dict(mapa["fixos"])
        codigo = linha.get("codigo_caso", "").strip().upper()
        if not codigo:
            motivos.append("codigo_caso vazio")
        elif not RE_CODIGO.match(codigo):
            motivos.append("codigo_caso fora do formato C-AAAA-NNNN (%s)" % codigo)
        elif codigo in vistos:
            motivos.append("codigo_caso repetido (já está na linha %d)" % vistos[codigo])
        else:
            vistos[codigo] = numero
        area = linha.get("area", "")
        if not area:
            motivos.append("area vazia")
        elif chave(area) != chave(mapa["area"]):
            motivos.append("área diferente: a linha é '%s' e a habilidade é de '%s'" % (area, mapa["area"]))
        for nome, d in do_caso.items():
            bruto = linha.get(nome, "")
            if not bruto:
                if d["obrigatoria"]:
                    motivos.append("falta %s" % nome)
                valores[nome] = ""
                continue
            texto, erro = formatar(nome, d["tipo"], bruto)
            if erro:
                motivos.append(erro)
            valores[nome] = texto
            if d["exemplo"] and sem_acento(bruto) == sem_acento(d["exemplo"]) and d["tipo"] not in ("genero", "lista") and not d["tipo"].startswith("opcao"):
                alertas.append("%s igual ao exemplo do mapa (%s): confira se não é cópia" % (nome, bruto))
        resultado.append({"linha": numero, "codigo": codigo, "nome": linha.get("nome_curto") or linha.get("cliente_curto", ""),
                          "prazo": linha.get("prazo_interno", ""), "motivos": motivos, "alertas": alertas, "valores": valores})

    passaram = [r for r in resultado if not r["motivos"]]
    if len(passaram) > 2:
        for nome, d in do_caso.items():
            if d["tipo"] in ("genero", "lista") or d["tipo"].startswith("opcao") or d["origem"] == "advogado":
                continue
            vs = set(r["valores"].get(nome, "") for r in passaram)
            if len(vs) == 1 and "" not in vs:
                for r in passaram:
                    r["alertas"].append("%s com o mesmo valor em todas as linhas que passaram: confira" % nome)

    lote_id = "%s-%s" % (hoje.isoformat(), mapa["peca"])
    print("LOTE %s · habilidade %s v%s · tese %s" % (lote_id, mapa["peca"], mapa["versao"], tese))
    print("%d linha(s) na planilha: %d passam, %d barradas." % (len(resultado), len(passaram), len(resultado) - len(passaram)))
    print()
    print("| Linha | Código | Nome curto | Situação | Motivo ou alerta |")
    print("|---|---|---|---|---|")
    for r in resultado:
        if r["motivos"]:
            print("| %d | %s | %s | barrada | %s |" % (r["linha"], r["codigo"] or "(vazio)", r["nome"], "; ".join(r["motivos"])))
        else:
            print("| %d | %s | %s | monta | %s |" % (r["linha"], r["codigo"], r["nome"], "; ".join(r["alertas"]) or "ok"))
    for av in avisos:
        print("Aviso: " + av)
    if not passaram:
        print()
        print("Nenhuma linha passou. Nada foi montado: corrija a planilha e rode de novo.")
        return 2
    if so_conferir:
        print()
        print("Só conferência: nada foi gravado. Com o ok do advogado, rode sem --so-conferir e com --decisao.")
        return 0

    pecas_csv = os.path.join(raiz, "pecas.csv")
    partes_raiz = os.path.normpath(os.path.abspath(raiz)).split(os.sep)
    if "_treino" in partes_raiz and partes_raiz[-1] == "juridico" and partes_raiz[-2] == "_treino":
        # treino: cada habilidade tem o próprio pecas.csv, para não colidir com o da rotina-juridica
        # e o do banco-de-teses-vivo (_treino/juridico/<habilidade>/pecas.csv)
        pecas_csv = os.path.join(raiz, "pecas-em-lote", "pecas.csv")
    try:
        maior, sep_pecas, existentes = ler_ids(pecas_csv, hoje.year)
    except Erro as erro:
        print("ERRO: %s" % erro)
        return 1
    novas, gravadas = [], []
    for r in passaram:
        corpo = montar(mapa["modelo"], r["valores"])
        sobra = sorted(set(re.findall(r"\{\{[^{}]*\}\}", corpo)))
        if sobra:
            print("ERRO: a minuta de %s ficou com variável sem preencher: %s. Nada desta linha foi gravado." % (r["codigo"], ", ".join(sobra)))
            r["motivos"].append("variável sem preencher no modelo: %s" % ", ".join(sobra))
            continue
        citacoes = len(RE_CONFERIR.findall(corpo))
        pasta = os.path.join(raiz, "casos", r["codigo"], "minutas")
        versao = proxima_versao(pasta, mapa["peca"])
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, "%s-v%d.md" % (mapa["peca"], versao))
        alertas = "".join("- Alerta da montagem: %s\n" % a for a in r["alertas"])
        cabeca = ("---\ndocumento: Minuta · %s · %s\nversao: %d\ngerado_em: %s\ncaso: %s\npeca: %s\ntese: %s\n"
                  "habilidade_usada: %s v%s\norigem: lote %s, linha %d\nredigiu: montagem do lote (pecas-em-lote) · S; revisão do advogado · A\n---\n\n"
                  "## Antes de protocolar (interno)\n\n"
                  "- Lote %s, linha %d da planilha. Tese do lote definida por: %s.\n"
                  "- Citações: %d marcadas [CONFERIR]; rodar a conferir-citacoes.\n%s"
                  "- [ ] Citações conferidas na fonte, sem vermelho nem cinza (conferir-citacoes)\n"
                  "- [ ] Dados do cliente conferidos com os documentos do caso (conferir-peca)\n"
                  "- [ ] Campos entre chaves preenchidos pelo sistema do escritório no protocolo\n"
                  "- [ ] Lida e ajustada pelo advogado (etapa revisada)\n"
                  "<!-- fim: antes de protocolar -->\n\n"
                  % (mapa["peca"], r["codigo"], versao, hoje.isoformat(), r["codigo"], mapa["peca"], tese,
                     mapa["peca"], mapa["versao"], lote_id, r["linha"], lote_id, r["linha"], decisao, citacoes, alertas))
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(cabeca + corpo)
        ja = existentes.get((r["codigo"], sem_acento(mapa["peca"])))
        if ja:
            r["alertas"].append("já está no pecas.csv como %s: atualize aquela linha (etapa minuta), não crie outra" % ja)
            gravadas.append((r, caminho, citacoes))
            continue
        maior += 1
        novas.append(["P-%d-%04d" % (hoje.year, maior), r["codigo"], r["nome"], mapa["area"], mapa["peca"], "lote",
                      r["prazo"], "minuta", responsavel, tese, mapa["peca"], "nao-conferidas", "nao-conferidos",
                      "", "", "", hoje.isoformat()])
        gravadas.append((r, caminho, citacoes))

    os.makedirs(os.path.join(raiz, "lotes"), exist_ok=True)
    rel = os.path.join(raiz, "lotes", "%s.md" % lote_id)
    n = 2
    while os.path.exists(rel):
        rel = os.path.join(raiz, "lotes", "%s-%d.md" % (lote_id, n))
        n += 1
    barradas = [r for r in resultado if r["motivos"]]
    with open(rel, "w", encoding="utf-8") as f:
        f.write("---\ndocumento: Relatório do lote %s\ngerado_em: %s\nhabilidade: %s v%s\ntese: %s\ndecisao_da_tese: %s\nplanilha: %s\n---\n\n"
                % (lote_id, hoje.isoformat(), mapa["peca"], mapa["versao"], tese, decisao, os.path.basename(args[0])))
        f.write("# Lote %s\n\n%d linha(s): %d minuta(s) montada(s), %d barrada(s).\n\n" % (lote_id, len(resultado), len(gravadas), len(barradas)))
        f.write("## Barradas (não saem)\n\n| Linha | Código | Motivo |\n|---|---|---|\n")
        for r in barradas:
            f.write("| %d | %s | %s |\n" % (r["linha"], r["codigo"] or "(vazio)", "; ".join(r["motivos"])))
        f.write("\n## Montadas\n\n| Linha | Código | Minuta | Citações marcadas | Alertas | conferir-peca | conferir-citacoes |\n|---|---|---|---|---|---|---|\n")
        for r, caminho, citacoes in gravadas:
            f.write("| %d | %s | %s | %d | %s | a rodar | a rodar |\n" % (r["linha"], r["codigo"], os.path.relpath(caminho, raiz), citacoes, "; ".join(r["alertas"]) or "nenhum"))
        f.write("\n## Linhas propostas para o pecas.csv\n\n```\n%s\n" % ",".join(COLUNAS_PECAS))
        for l in novas:
            f.write(",".join(l) + "\n")
        f.write("```\n")
    print()
    for r, caminho, _ in gravadas:
        print("Minuta: %s" % caminho)
    print("Relatório do lote: %s" % rel)
    if registrar and novas:
        novo = not os.path.isfile(pecas_csv)
        os.makedirs(os.path.dirname(os.path.abspath(pecas_csv)), exist_ok=True)
        with open(pecas_csv, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=sep_pecas)
            if novo:
                w.writerow(COLUNAS_PECAS)
            for l in novas:
                w.writerow(l)
        print("pecas.csv: %d linha(s) acrescentada(s) em %s (etapa minuta, origem lote)." % (len(novas), pecas_csv))
    elif novas:
        print("pecas.csv não foi mexido: as linhas propostas estão no relatório (use --registrar para acrescentar).")
    print("Próximo passo: conferir-peca e conferir-citacoes em cada minuta; nenhuma vai ao advogado com vermelho.")
    return 0 if gravadas else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
