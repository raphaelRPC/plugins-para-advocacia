#!/usr/bin/env python3
"""Monta a lista do lote de resumos mensais a partir da carteira.

Uso:
    python3 lote_do_mes.py CAMINHO/carteira.csv [AAAA-MM] [--clientes PASTA] [--ficha CAMINHO]
                           [--sem-registro-de-envio] [--treino]

Para cada cliente ativo, diz em que grupo ele cai neste mês:
  - FEITO: o resumo do mês já foi enviado: clientes/<codigo>/resumos/AAAA-MM.md com
    "status: enviado" no cabeçalho. Com --sem-registro-de-envio (o escritório não marca
    o envio no arquivo), "status: aprovado" também conta;
  - APROVADO, FALTA ENVIAR: status aprovado sem --sem-registro-de-envio. Conta como
    por fazer até alguém enviar e marcar "status: enviado". O script confere o texto do
    cliente com a mesma política do resumo_para_docx.py: com marcação, campo do modelo
    ou instrução entre colchetes no corpo, o .docx não sai (sem --forcar); campos do
    envio entre chaves ({...}) são listados para quem envia preencher;
  - FAZER: recebe resumo e não tem o arquivo do mês, ou o arquivo está em rascunho,
    descartado ou sem status (rascunho e descartado contam como por fazer);
  - LIGAÇÃO ANTES: recebe resumo, mas está insatisfeito, tem reclamação aberta,
    está em fase de decisão ou recurso, ou com humor a confirmar; uma pessoa fala
    primeiro, e o resumo só sai depois;
  - NÃO RECEBE: pediu para não receber (pediu_para_nao_receber = sim) ou
    resumo_mensal = nao. Notícia relevante continua, do jeito que ele prefere.

Lê a ficha da experiência (--ficha, ou escritorio/04-base/comum/ficha-da-experiencia.md,
procurada subindo a partir da carteira): o campo resumo_mensal é lido só pelo texto
antes do parêntese (o parêntese de opções do modelo não conta). "não fazemos" antes
do parêntese: o script diz que o escritório não faz resumo e não monta lote.

Lê csv com vírgula ou ponto e vírgula, com ou sem BOM. Compara sim/não, fase e
humor sem diferenciar maiúscula nem acento. Aceita datas AAAA-MM-DD e DD/MM/AAAA.
Sai com código 1 e mensagem clara quando falta o arquivo, uma coluna obrigatória
ou quando nenhuma linha de cliente foi lida. Só lê; não altera nada.
"""

import csv
import io
import os
import re
import sys
import unicodedata
from datetime import date, datetime

OBRIGATORIAS = ["codigo", "nome_curto", "fase", "resumo_mensal"]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t or "") if not unicodedata.combining(c))


def norm(v):
    return re.sub(r"[\s_]+", "-", sem_acento(v).strip().lower())


def norm_coluna(v):
    return re.sub(r"[\s-]+", "_", sem_acento(v).strip().lower().lstrip("﻿"))


def sim(v):
    return norm(v) in ("sim", "s", "yes", "true", "1", "x")


def ler_data(v):
    v = (v or "").strip()
    if not v:
        return None
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(v, f).date()
        except ValueError:
            pass
    return None


def ler_csv(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    texto = None
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    primeira = texto.splitlines()[0] if texto.strip() else ""
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    linhas = [l for l in csv.reader(io.StringIO(texto), delimiter=sep) if any(c.strip() for c in l)]
    if not linhas:
        return [], []
    cabeca = [norm_coluna(c) for c in linhas[0]]
    regs = []
    for l in linhas[1:]:
        regs.append({cabeca[i]: (l[i].strip() if i < len(l) else "") for i in range(len(cabeca))})
    return cabeca, regs


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def achar_ficha(carteira):
    pasta = os.path.dirname(os.path.abspath(carteira))
    while True:
        if os.path.basename(pasta) == "escritorio":
            candidata = os.path.join(pasta, "04-base", "comum", "ficha-da-experiencia.md")
            return candidata if os.path.isfile(candidata) else None
        acima = os.path.dirname(pasta)
        if acima == pasta:
            return None
        pasta = acima


def antes_do_parentese(valor):
    """O valor sem o parêntese de opções ou exemplos do modelo (igual ao carteira.py)."""
    valor = (valor or "").strip()
    antes = valor.split("(", 1)[0].strip()
    if antes or "(" not in valor:
        return antes
    if re.search(r"\((opcoes|ex\.|minimo|quantos|em horas|o que|quem|a frase|a partir)", sem_acento(valor).lower()):
        return ""
    return valor.strip("() ")


def resumo_da_ficha(caminho):
    """Devolve (formato, dia, texto lido): formato None quando o campo falta ou está em aberto."""
    if not caminho or not os.path.isfile(caminho):
        return None, None, ""
    for linha in ler_texto(caminho).splitlines():
        m = re.match(r"^\s*[-*]\s*resumo_mensal\s*:\s*(.*)$", linha)
        if not m:
            continue
        v = antes_do_parentese(m.group(1))
        if not v or "[A PREENCHER]" in v or "[A DEFINIR]" in v:
            return None, None, v
        t = sem_acento(v).lower()
        if re.search(r"\bnao (fazemos|usamos|enviamos|mandamos)\b", t):
            return "nao fazemos", None, v
        formato = ("pagina do caso" if "pagina" in t else "pdf" if ("pdf" in t or "docx" in t)
                   else "mensagem" if "mensagem" in t else "a confirmar")
        dia = re.search(r"dia\s+(\d{1,2})\b", t)
        return formato, (int(dia.group(1)) if dia else None), v
    return None, None, ""


# Conferência do texto do cliente, com a mesma política do resumo_para_docx.py
RE_MARCACAO = re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]\n]*\]", re.I)
RE_COLCHETE = re.compile(r"\[([^\[\]\n]*)\](?!\()")
RE_CHAVE = re.compile(r"\{([^{}\n]*[A-Za-zÀ-ÿ][^{}\n]*)\}")
RE_CHECK = re.compile(r"^\s*[-*+]\s+\[( |x|X)\]\s+")
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*)$")
RE_INICIO_INTERNO = re.compile(r"^\s*<!--\s*antes-de-enviar\s*-->\s*$", re.I)
RE_FIM_INTERNO = re.compile(r"^\s*<!--\s*(/\s*antes-de-enviar|fim:\s*antes de enviar)\s*-->\s*$", re.I)


def texto_do_cliente(texto):
    """As linhas que vão ao cliente: sem o YAML, sem o "Antes de enviar" e sem comentários."""
    linhas = texto.splitlines()
    i = 0
    if linhas and linhas[0].strip() == "---":
        for j in range(1, len(linhas)):
            if linhas[j].strip() == "---":
                i = j + 1
                break
    corpo = []
    while i < len(linhas):
        limpa = linhas[i].strip()
        if RE_INICIO_INTERNO.match(limpa):
            i += 1
            while i < len(linhas) and not RE_FIM_INTERNO.match(linhas[i].strip()):
                i += 1
            i += 1
            continue
        m = RE_TITULO.match(limpa)
        if m and sem_acento(m.group(2)).lower().startswith("antes de enviar"):
            nivel = len(m.group(1))
            i += 1
            while i < len(linhas):
                lj = linhas[i].strip()
                if RE_FIM_INTERNO.match(lj):
                    i += 1
                    break
                mj = RE_TITULO.match(lj)
                if mj and len(mj.group(1)) <= nivel:
                    break
                i += 1
            continue
        corpo.append(re.sub(r"<!--.*?-->", "", linhas[i]))
        i += 1
    return corpo


def pendencias_do_resumo(caminho):
    """(pendências no corpo, campos do envio) do resumo já escrito."""
    pend, chaves = [], []
    for linha in texto_do_cliente(ler_texto(caminho)):
        for m in RE_COLCHETE.finditer(linha):
            bruto = m.group(1).strip()
            if bruto in ("", "x", "X") and RE_CHECK.match(linha):
                continue
            if any(c.isalpha() for c in bruto):
                pend.append(m.group(0))
        chaves += [m.group(0) for m in RE_CHAVE.finditer(linha)]
    return pend, chaves


def status_do_resumo(caminho):
    """O status do cabeçalho do resumo: None sem arquivo, "" sem status."""
    if not os.path.isfile(caminho):
        return None
    linhas = ler_texto(caminho).splitlines()
    if not linhas or linhas[0].strip() != "---":
        return ""
    for linha in linhas[1:]:
        if linha.strip() == "---":
            break
        m = re.match(r"^\s*status\s*:\s*([^#]*)", linha, re.I)
        if m:
            return norm(m.group(1))
    return ""


def nota_do_texto(arquivo, rel, formato):
    pend, chaves = pendencias_do_resumo(arquivo)
    nota = rel
    if pend:
        nota += (" · %d pendência(s) no texto do cliente (%s): o .docx não sai sem --forcar"
                 % (len(pend), ", ".join(pend[:3]) + (" ..." if len(pend) > 3 else "")))
    elif formato == "pdf":
        nota += " · texto do cliente sem pendência: pronto para o .docx"
    if chaves:
        nota += " · %d campo(s) do envio para preencher (%s)" % (len(chaves), ", ".join(chaves[:3]))
    return nota


def sair(msg):
    print("ERRO: " + msg)
    sys.exit(1)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    op = [a for a in argv[1:] if a.startswith("--")]
    clientes = None
    if "--clientes" in argv:
        i = argv.index("--clientes")
        if i + 1 >= len(argv):
            sair("--clientes precisa de uma pasta.")
        clientes = argv[i + 1]
        args = [a for a in args if a != clientes]
    ficha = None
    if "--ficha" in argv:
        i = argv.index("--ficha")
        if i + 1 >= len(argv):
            sair("--ficha precisa do caminho da ficha-da-experiencia.md.")
        ficha = argv[i + 1]
        args = [a for a in args if a != ficha]
        if not os.path.isfile(ficha):
            sair("não encontrei a ficha em '%s'." % ficha)
    if "--help" in op or "--ajuda" in op:
        print(__doc__)
        return 0
    if not args:
        print(__doc__)
        sair("informe o caminho da carteira.csv.")
    caminho = args[0]
    if not os.path.isfile(caminho):
        sair("não encontrei a carteira em '%s'. Nada foi calculado." % caminho)
    if "_treino" in os.path.abspath(caminho).replace("\\", "/").split("/") and "--treino" not in op:
        sair("esta carteira está em _treino/. Para o lote de treino, repita com --treino.")
    if len(args) > 1:
        if not re.fullmatch(r"\d{4}-\d{2}", args[1]):
            sair("o mês '%s' precisa estar em AAAA-MM." % args[1])
        mes = args[1]
    else:
        mes = date.today().strftime("%Y-%m")

    cabeca, regs = ler_csv(caminho)
    if not cabeca:
        sair("a carteira '%s' está vazia." % caminho)
    faltam = [c for c in OBRIGATORIAS if c not in cabeca]
    if faltam:
        sair("faltam colunas na carteira: %s. Colunas lidas: %s." % (", ".join(faltam), ", ".join(cabeca)))
    if not regs:
        sair("a carteira tem só a linha de títulos, nenhum cliente. Nada foi calculado.")
    pasta = clientes or os.path.join(os.path.dirname(os.path.abspath(caminho)), "clientes")
    ficha = ficha or achar_ficha(caminho)
    formato, dia, lido = resumo_da_ficha(ficha)
    treino = " · TREINO" if "--treino" in op else ""
    if formato == "nao fazemos":
        print("# Lote de resumos · %s%s" % (mes, treino))
        print()
        print("O escritório não faz resumo mensal (ficha, resumo_mensal: \"%s\"). Nenhum lote a montar." % lido)
        print("Notícia relevante continua pela régua da jornada. Para começar a fazer, mude o campo na ficha.")
        return 0

    aprovado_basta = "--sem-registro-de-envio" in op
    grupos = {"FAZER": [], "LIGAÇÃO ANTES": [], "APROVADO, FALTA ENVIAR": [], "FEITO": [], "NÃO RECEBE": []}
    situacoes = {"rascunho": "rascunho no arquivo do mês, falta aprovar e enviar",
                 "pendente": "rascunho no arquivo do mês, falta aprovar e enviar",
                 "descartado": "o resumo do mês foi descartado: refazer",
                 "": "arquivo do mês sem status no cabeçalho: conferir se saiu"}
    encerrados = 0
    for r in regs:
        fase = norm(r.get("fase", ""))
        if fase == "encerrado" or ler_data(r.get("encerrado_em", "")):
            encerrados += 1
            continue
        rot = "%s · %s · %s" % (r.get("codigo") or "(sem código)", r.get("nome_curto") or "?", r.get("tipo_de_caso") or r.get("area") or "")
        if sim(r.get("pediu_para_nao_receber", "")):
            grupos["NÃO RECEBE"].append((rot, "pediu para não receber"))
            continue
        if not sim(r.get("resumo_mensal", "")):
            grupos["NÃO RECEBE"].append((rot, "resumo_mensal = nao"))
            continue
        arquivo = os.path.join(pasta, r.get("codigo", ""), "resumos", mes + ".md")
        rel = "clientes/%s/resumos/%s.md" % (r.get("codigo", ""), mes)
        st = status_do_resumo(arquivo)
        if st == "enviado" or (st == "aprovado" and aprovado_basta):
            grupos["FEITO"].append((rot, "%s · status: %s" % (rel, st)))
            continue
        if st == "aprovado":
            grupos["APROVADO, FALTA ENVIAR"].append((rot, nota_do_texto(arquivo, rel, formato)
                                                      + " · depois do envio, status: enviado no arquivo"))
            continue
        situacao = None
        if st is not None:
            situacao = situacoes.get(st, "status '%s' no arquivo do mês: conta como por fazer" % st)
            situacao = nota_do_texto(arquivo, rel, formato) + " · " + situacao
        motivos = []
        if sim(r.get("reclamacao_aberta", "")):
            motivos.append("reclamação aberta")
        humor = norm(r.get("humor", ""))
        if humor == "insatisfeito":
            motivos.append("insatisfeito")
        if humor == "a-confirmar":
            motivos.append("humor a confirmar")
        if fase in ("decisao", "recurso"):
            motivos.append("fase %s: conferir se há notícia a dar por ligação" % fase)
        if motivos:
            grupos["LIGAÇÃO ANTES"].append((rot, "; ".join(motivos) + (" · " + situacao if situacao else "")))
        else:
            grupos["FAZER"].append((rot, "fase %s" % (fase or "?") + (" · " + situacao if situacao else "")))

    total = sum(len(v) for v in grupos.values())
    print("# Lote de resumos · %s%s" % (mes, treino))
    print()
    if formato:
        print("Ficha: resumo_mensal \"%s\" (formato: %s%s)." % (lido, formato, (", dia %d" % dia) if dia else ""))
    else:
        print("Ficha: resumo_mensal %s. Formato e dia [A PREENCHER]: pergunte antes de montar."
              % ("em aberto" if ficha else "não encontrado (sem ficha)"))
    print("Lidos %d clientes ativos (%d encerrados fora). Fazer: %d · ligação antes: %d · aprovados, falta enviar: %d · "
          "feitos: %d · não recebem: %d."
          % (total, encerrados, len(grupos["FAZER"]), len(grupos["LIGAÇÃO ANTES"]), len(grupos["APROVADO, FALTA ENVIAR"]),
             len(grupos["FEITO"]), len(grupos["NÃO RECEBE"])))
    print("Feito quer dizer enviado: status: enviado no cabeçalho do arquivo do mês%s. Rascunho e descartado contam como por fazer."
          % (" (ou aprovado, porque o escritório não registra o envio)" if aprovado_basta else ""))
    for nome, itens in grupos.items():
        print()
        print("## %s (%d)" % (nome, len(itens)))
        if not itens:
            print("Ninguém.")
        for rot, nota in itens:
            print("- %s · %s" % (rot, nota))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
