#!/usr/bin/env python3
"""Lê a carteira de clientes (carteira.csv) e aponta o que o escritório precisa fazer hoje.

Uso:
    python3 carteira.py CAMINHO/carteira.csv [AAAA-MM-DD] [opções]

Opções:
    --data AAAA-MM-DD        data de referência (treino ou outro dia); o mesmo que a data depois
                             do caminho. Sem data, vale a de hoje
    --maximo-sem-noticia N   dias corridos sem notícia (campo maximo_sem_noticia da ficha)
    --docs-dias N            dias até o documento pendente pedir decisão (cobranca_de_documentos)
    --dia-resumo N           dia do mês em que o resumo mensal sai (resumo_mensal); 0 = não fazemos
    --dias-compromisso N     janela dos compromissos (padrão 7)
    --feriados D1,D2         feriados (AAAA-MM-DD ou DD/MM/AAAA), para achar o próximo dia útil
    --ficha CAMINHO          ficha-da-experiencia.md (sem a opção, o script procura em
                             escritorio/04-base/comum/ subindo a partir da carteira)
    --jornadas PASTA         pasta das jornadas por tipo de caso (padrão:
                             escritorio/04-base/relacionamento-com-o-cliente/)
    --clientes PASTA         pasta clientes/ (padrão: ao lado da carteira)
    --passagens PASTA        pasta das passagens do comercial (padrão: ../comercial/passagens)
    --sem-registro-de-envio  o escritório não marca "status: enviado" nos resumos: "aprovado" basta
    --treino                 obrigatório para ler uma carteira dentro de _treino/
    --conferir               só confere o arquivo (colunas, datas, códigos), sem o resumo

Lê csv com vírgula ou ponto e vírgula, com ou sem BOM, salvo pelo Excel ou não.
Compara fase, humor e sim/não sem diferenciar maiúscula nem acento. Aceita datas
AAAA-MM-DD e DD/MM/AAAA. Sai com código 1 e uma mensagem clara quando falta o
arquivo, uma coluna obrigatória ou quando nenhuma linha de cliente foi lida.
Da ficha, cada campo é lido só pelo texto antes do parêntese: o parêntese de opções e
exemplos do modelo ("(opções: não fazemos | mensagem | PDF ...)") pode ter ficado e não conta.

ultimo_contato é a data do último contato que informou algo do caso (status, resumo,
página, ligação, reunião, boas-vindas). Resposta-ponte, cortesia, lembrete de documento
e pesquisa não contam (docs/agentes-e-fila.md); o script avisa quando o
ultimo_contato_tipo é um desses.

Máximo sem notícia por cliente: se existe a jornada do tipo de caso
(jornada-<tipo-de-caso>.md), vale o "Máximo sem notícia nesta fase" da fase do cliente
(fase confirmada) ou, sem ele, o "Máximo sem notícia" da régua da jornada. Fase da
jornada ainda [A CONFIRMAR], valor em aberto ou sem jornada: vale o da ficha.

Reclamação aberta e humor insatisfeito saem de PESSOA AGORA quando a pessoa já falou e
gravou o combinado: motivo_proximo_contato = retorno-combinado, proximo_contato no futuro
e ultimo_contato_tipo ligacao ou reuniao. No dia combinado, voltam para o topo.
motivo_proximo_contato = ligacao-pendente vencido ou de hoje vai para PESSOA AGORA.
Compromisso até o próximo dia útil sai de PESSOA AGORA (e fica na seção 2) quando o
historico.md do cliente tem a ligação de preparação: canal ligacao e "preparação" no texto,
nos 30 dias antes do compromisso.

Resumo do mês só conta como feito com "status: enviado" no cabeçalho de
clientes/<codigo>/resumos/AAAA-MM.md ("aprovado" também, com --sem-registro-de-envio).
Rascunho, descartado ou sem status contam como por fazer.

Só lê. Não altera a carteira nem nenhum outro arquivo.
"""

import csv
import io
import os
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta

CABECALHO = (
    "codigo,nome_curto,area,tipo_de_caso,responsavel,inicio,fase,ultimo_contato,"
    "ultimo_contato_tipo,proximo_contato,motivo_proximo_contato,proximo_compromisso,"
    "data_compromisso,documentos_pendentes,humor,reclamacao_aberta,resumo_mensal,"
    "pagina_do_caso,satisfacao,pediu_para_nao_receber,encerrado_em,atualizado_em"
)
COLUNAS = CABECALHO.split(",")
OBRIGATORIAS = ["codigo", "nome_curto", "fase", "ultimo_contato"]
FASES = [
    "entrada", "documentos", "preparacao", "protocolado", "aguardando",
    "audiencia-pericia", "decisao", "recurso", "cumprimento", "encerramento", "encerrado",
]
HUMORES = ["tranquilo", "ansioso", "insatisfeito", "a-confirmar"]
TIPOS_CONTATO = ["mensagem", "ligacao", "reuniao", "resumo", "pagina"]
MOTIVOS = ["boas-vindas", "ligacao-pendente", "resumo-mensal", "maximo-sem-noticia", "compromisso",
           "documento", "retorno-combinado", "pesquisa", "depois-do-caso"]
JANELA_PREPARACAO = 30  # dias antes do compromisso em que a ligação de preparação vale
# Contatos que entram no histórico, mas não zeram o "sem notícia" (docs/agentes-e-fila.md).
NAO_CONTAM = ["resposta-ponte", "ponte", "cortesia", "agradecimento", "lembrete", "lembrete-de-documento",
              "cobranca-de-documento", "documento", "pesquisa"]
FALOU = ["ligacao", "reuniao"]
COMPROMISSOS = ["audiencia", "pericia", "reuniao", "prazo-do-cliente"]
DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
RE_CODIGO = re.compile(r"^C-\d{4}-\d{4}(-\d+)?$")


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in texto if not unicodedata.combining(c))


def norm(valor):
    """Minúsculas, sem acento, espaços e sublinhados viram hífen."""
    v = sem_acento(valor).strip().lower()
    v = re.sub(r"[\s_]+", "-", v)
    return v


def norm_coluna(nome):
    v = sem_acento(nome).strip().lower().lstrip("﻿")
    v = re.sub(r"[\s-]+", "_", v)
    return v


def sim(valor):
    return norm(valor) in ("sim", "s", "yes", "true", "1", "x")


def ler_data(valor):
    v = (valor or "").strip()
    if not v:
        return None
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(v, formato).date()
        except ValueError:
            continue
    return "invalida"


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for codificacao in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(codificacao)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_csv(caminho):
    texto = ler_texto(caminho)
    primeira = texto.splitlines()[0] if texto.strip() else ""
    separador = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.reader(io.StringIO(texto), delimiter=separador)
    linhas = [l for l in leitor if any(c.strip() for c in l)]
    if not linhas:
        return separador, [], []
    cabeca = [norm_coluna(c) for c in linhas[0]]
    registros = []
    for numero, linha in enumerate(linhas[1:], start=2):
        r = {}
        for i, nome in enumerate(cabeca):
            r[nome] = linha[i].strip() if i < len(linha) else ""
        r["_linha"] = numero
        registros.append(r)
    return separador, cabeca, registros


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


def achar_escritorio(carteira):
    pasta = os.path.dirname(os.path.abspath(carteira))
    while True:
        if os.path.basename(pasta) == "escritorio":
            return pasta
        acima = os.path.dirname(pasta)
        if acima == pasta:
            return None
        pasta = acima


def slug(texto):
    return re.sub(r"[^a-z0-9]+", "-", sem_acento(texto or "").lower()).strip("-")


def dias_do_texto(valor):
    """O número de dias de uma linha da jornada, ou None se está em aberto."""
    v = (valor or "").strip()
    if not v or re.search(r"\[(N|A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]", v, re.I):
        return None
    v = v.split("(", 1)[0]
    m = re.search(r"\b(\d{1,3})\b", v)
    return int(m.group(1)) if m else None


def ler_jornada(caminho):
    """{'titulo', 'regua', 'fases': {fase: {'maximo', 'confirmada'}}} de uma jornada-<tipo>.md."""
    jornada = {"titulo": "", "regua": None, "fases": {}, "arquivo": os.path.basename(caminho)}
    secao, fase = None, None
    for linha in ler_texto(caminho).splitlines():
        s = linha.strip()
        m = re.match(r"^documento\s*:\s*jornada\s*[·:\-]\s*(.+)$", sem_acento(s), re.I)
        if m and not jornada["titulo"]:
            jornada["titulo"] = m.group(1).strip()
            continue
        if s.startswith("## "):
            secao = slug(s[3:])
            fase = None
            continue
        if s.startswith("### "):
            nome = norm(re.split(r"\s+[·:\-]\s+|\s+", s[4:].strip(), maxsplit=1)[0].strip("`"))
            fase = nome if nome in FASES else None
            if fase:
                jornada["fases"].setdefault(fase, {"maximo": None, "confirmada": True})
            continue
        m = re.match(r"^[-*]\s*(.+?)\s*:\s*(.*)$", s)
        if not m:
            continue
        chave, valor = slug(m.group(1)), m.group(2)
        if fase is None and secao and secao.startswith("a-regua") and chave == "maximo-sem-noticia":
            jornada["regua"] = dias_do_texto(valor)
        elif fase and chave.startswith("maximo-sem-noticia"):
            jornada["fases"][fase]["maximo"] = dias_do_texto(valor)
        elif fase and chave == "situacao":
            jornada["fases"][fase]["confirmada"] = "a confirmar" not in sem_acento(valor).lower()
    return jornada


def ler_jornadas(pasta):
    """{slug do tipo de caso: jornada}, pelo nome do arquivo e pelo título do cabeçalho."""
    jornadas = {}
    if not pasta or not os.path.isdir(pasta):
        return None
    for nome in sorted(os.listdir(pasta)):
        if not (nome.startswith("jornada-") and nome.endswith(".md")):
            continue
        j = ler_jornada(os.path.join(pasta, nome))
        jornadas.setdefault(nome[len("jornada-"):-3], j)
        if j["titulo"]:
            jornadas.setdefault(slug(j["titulo"]), j)
    return jornadas


def status_do_resumo(caminho):
    """O status do cabeçalho do resumo do mês: None sem arquivo, "" sem status."""
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


def linhas_do_historico(caminho):
    """(data, canal, texto) de cada linha da tabela do historico.md."""
    linhas = []
    if not os.path.isfile(caminho):
        return linhas
    for linha in ler_texto(caminho).splitlines():
        s = linha.strip()
        if not s.startswith("|"):
            continue
        cel = [c.strip() for c in s.strip("|").split("|")]
        if len(cel) < 4:
            continue
        d = ler_data(cel[0][:10])
        if d in (None, "invalida"):
            continue
        linhas.append((d, norm(cel[1]), sem_acento(" | ".join(cel[2:])).lower()))
    return linhas


def ligacao_de_preparacao(historico, data_compromisso, hoje):
    """A data da ligação de preparação registrada para o compromisso, ou None."""
    inicio = data_compromisso - timedelta(days=JANELA_PREPARACAO)
    fim = min(hoje, data_compromisso)
    achadas = [d for d, canal, texto in historico
               if canal == "ligacao" and "preparacao" in texto and inicio <= d <= fim]
    return max(achadas) if achadas else None


def ler_ficha(caminho):
    campos = {}
    if not caminho or not os.path.isfile(caminho):
        return campos
    for linha in ler_texto(caminho).splitlines():
        m = re.match(r"^\s*[-*]\s*([a-z_]+)\s*:\s*(.*)$", linha)
        if m:
            campos[m.group(1)] = m.group(2).strip()
    return campos


def antes_do_parentese(valor):
    """O valor do campo sem o parêntese de opções ou exemplos que o modelo traz.

    Se não sobrar nada antes do parêntese e o parêntese não for o do modelo
    (opções, exemplo, mínimo), vale o que a pessoa escreveu dentro dele."""
    valor = (valor or "").strip()
    antes = valor.split("(", 1)[0].strip()
    if antes or "(" not in valor:
        return antes
    dica = sem_acento(valor).lower()
    if re.search(r"\((opcoes|ex\.|minimo|quantos|em horas|o que|quem|a frase|a partir)", dica):
        return ""
    return valor.strip("() ")


def preenchido(valor):
    return bool(valor) and "[A PREENCHER]" not in valor and "[A DEFINIR]" not in valor


def criterios_da_ficha(campos):
    achados = {}
    campos = {k: antes_do_parentese(v) for k, v in campos.items()}
    v = campos.get("maximo_sem_noticia", "")
    if preenchido(v):
        m = re.search(r"\d+", v)
        if m:
            achados["maximo"] = int(m.group(0))
    v = campos.get("cobranca_de_documentos", "")
    if preenchido(v):
        numeros = [int(n) for n in re.findall(r"\d+", v)]
        if numeros:
            achados["docs"] = max(numeros)
    v = campos.get("resumo_mensal", "")
    if preenchido(v):
        texto = sem_acento(v).lower()
        if re.search(r"\bnao (fazemos|usamos|enviamos|mandamos)\b", texto):
            achados["dia_resumo"] = 0
        else:
            m = re.search(r"dia\s+(\d{1,2})\b", texto)
            if m and 1 <= int(m.group(1)) <= 31:
                achados["dia_resumo"] = int(m.group(1))
    return achados


def opcoes(argv):
    args, op = [], {}
    i = 0
    com_valor = {"--maximo-sem-noticia", "--docs-dias", "--dia-resumo", "--dias-compromisso",
                 "--feriados", "--ficha", "--clientes", "--passagens", "--data", "--jornadas"}
    while i < len(argv):
        a = argv[i]
        if a in com_valor:
            if i + 1 >= len(argv):
                sair("a opção %s precisa de um valor." % a)
            op[a] = argv[i + 1]
            i += 2
        elif a.startswith("--"):
            op[a] = True
            i += 1
        else:
            args.append(a)
            i += 1
    return args, op


def sair(mensagem):
    print("ERRO: " + mensagem)
    sys.exit(1)


def inteiro(op, nome):
    if nome not in op:
        return None
    try:
        return int(op[nome])
    except ValueError:
        sair("a opção %s precisa de um número inteiro (veio '%s')." % (nome, op[nome]))


def proximo_dia_util(hoje, feriados):
    d = hoje + timedelta(days=1)
    while d.weekday() >= 5 or d in feriados:
        d += timedelta(days=1)
    return d


def rotulo(r):
    partes = [r.get("codigo") or "(sem código)", r.get("nome_curto") or "(sem nome)"]
    if r.get("area"):
        partes.append(r["area"])
    return " · ".join(partes[:2]) + (" · " + partes[2] if len(partes) > 2 else "")


def dia_semana(d):
    return DIAS_SEMANA[d.weekday()]


def main(argv):
    args, op = opcoes(argv[1:])
    if "--help" in op or "--ajuda" in op:
        print(__doc__)
        return 0
    if not args:
        print(__doc__)
        sair("informe o caminho da carteira.csv.")
    caminho = args[0]
    if not os.path.isfile(caminho):
        sair("não encontrei a carteira em '%s'. Confira o caminho "
             "(o padrão é escritorio/07-operacao/experiencia/carteira.csv) ou importe a carteira "
             "pela habilidade rotina-da-experiencia. Nada foi calculado." % caminho)

    partes_caminho = os.path.abspath(caminho).replace("\\", "/").split("/")
    em_treino = "_treino" in partes_caminho
    if em_treino and "--treino" not in op:
        sair("esta carteira está em _treino/. Treino não entra na rotina real. "
             "Para rodar o treino, repita o comando com --treino.")
    if "--treino" in op and not em_treino:
        print("AVISO: --treino usado numa carteira fora de _treino/. O resultado vale como treino.")

    data_pedida = op.get("--data")
    if data_pedida and len(args) > 1 and ler_data(args[1]) != ler_data(data_pedida):
        sair("duas datas diferentes: '%s' depois do caminho e '%s' em --data. Use uma só." % (args[1], data_pedida))
    data_pedida = data_pedida or (args[1] if len(args) > 1 else None)
    if data_pedida:
        hoje = ler_data(data_pedida)
        if hoje in (None, "invalida"):
            sair("a data '%s' não está em AAAA-MM-DD nem em DD/MM/AAAA." % data_pedida)
    else:
        hoje = date.today()

    feriados = set()
    for f in (op.get("--feriados") or "").split(","):
        if f.strip():
            d = ler_data(f)
            if d in (None, "invalida"):
                sair("feriado '%s' fora do formato AAAA-MM-DD ou DD/MM/AAAA." % f)
            feriados.add(d)

    separador, cabeca, registros = ler_csv(caminho)
    if not cabeca:
        sair("a carteira '%s' está vazia (nem a primeira linha com os nomes das colunas). "
             "A primeira linha esperada é:\n%s" % (caminho, CABECALHO))
    faltam = [c for c in OBRIGATORIAS if c not in cabeca]
    if faltam:
        sair("faltam colunas obrigatórias na carteira: %s. Colunas lidas: %s. "
             "A primeira linha esperada é:\n%s" % (", ".join(faltam), ", ".join(cabeca), CABECALHO))
    if not registros:
        sair("a carteira tem só a linha de títulos, nenhum cliente. Nada foi calculado. "
             "Importe a carteira atual ou rode a boas-vindas do primeiro cliente.")
    ausentes = [c for c in COLUNAS if c not in cabeca]

    # Critérios: opção > ficha > padrão
    ficha = op.get("--ficha") or achar_ficha(caminho)
    da_ficha = criterios_da_ficha(ler_ficha(ficha))
    origem = {}

    def criterio(chave, opcao, padrao):
        v = inteiro(op, opcao)
        if v is not None:
            origem[chave] = "opção"
            return v
        if chave in da_ficha:
            origem[chave] = "ficha"
            return da_ficha[chave]
        origem[chave] = "padrão do script, confirme na ficha"
        return padrao

    maximo = criterio("maximo", "--maximo-sem-noticia", 30)
    docs_dias = criterio("docs", "--docs-dias", 7)
    dia_resumo = criterio("dia_resumo", "--dia-resumo", 5)
    janela = inteiro(op, "--dias-compromisso") or 7
    util = proximo_dia_util(hoje, feriados)

    pasta_carteira = os.path.dirname(os.path.abspath(caminho))
    pasta_clientes = op.get("--clientes") or os.path.join(pasta_carteira, "clientes")
    pasta_passagens = op.get("--passagens") or os.path.join(os.path.dirname(pasta_carteira), "comercial", "passagens")
    raiz = achar_escritorio(caminho)
    pasta_jornadas = op.get("--jornadas") or (
        os.path.join(raiz, "04-base", "relacionamento-com-o-cliente") if raiz else None)
    if op.get("--jornadas") and not os.path.isdir(op["--jornadas"]):
        sair("não encontrei a pasta das jornadas em '%s'." % op["--jornadas"])
    jornadas = ler_jornadas(pasta_jornadas)
    aprovado_basta = "--sem-registro-de-envio" in op

    def maximo_do_cliente(r):
        """(dias, de onde veio) para este cliente."""
        if not jornadas:
            return maximo, None
        j = jornadas.get(slug(r.get("tipo_de_caso", "")))
        if not j:
            return maximo, None
        f = j["fases"].get(r["_fase"])
        if f and not f["confirmada"]:
            return maximo, "%s: fase %s ainda a confirmar, vale a ficha" % (j["arquivo"], r["_fase"])
        if f and f["maximo"]:
            return f["maximo"], "%s, fase %s" % (j["arquivo"], r["_fase"])
        if j["regua"]:
            return j["regua"], "%s, régua do tipo de caso" % j["arquivo"]
        return maximo, "%s sem máximo preenchido, vale a ficha" % j["arquivo"]

    # Conferência das linhas
    corrigir = []
    vistos = {}
    ativos, encerrados = [], []
    for r in registros:
        cod = r.get("codigo", "")
        if not cod:
            corrigir.append("linha %d: código vazio" % r["_linha"])
        elif not RE_CODIGO.match(cod):
            corrigir.append("linha %d: código '%s' fora do formato C-AAAA-NNNN" % (r["_linha"], cod))
        if cod:
            if cod in vistos:
                corrigir.append("linha %d: código %s repetido (já na linha %d; segundo caso leva o sufixo -2)"
                                % (r["_linha"], cod, vistos[cod]))
            else:
                vistos[cod] = r["_linha"]
        fase = norm(r.get("fase", ""))
        r["_fase"] = fase
        if fase not in FASES:
            corrigir.append("linha %d (%s): fase '%s' fora da lista" % (r["_linha"], cod or "?", r.get("fase", "")))
        for col in ("inicio", "ultimo_contato", "proximo_contato", "data_compromisso", "encerrado_em", "atualizado_em"):
            if col in cabeca:
                d = ler_data(r.get(col, ""))
                if d == "invalida":
                    corrigir.append("linha %d (%s): %s '%s' fora do formato de data" % (r["_linha"], cod or "?", col, r.get(col, "")))
                    d = None
                r["_" + col] = d
            else:
                r["_" + col] = None
        r["_humor"] = norm(r.get("humor", "")) if "humor" in cabeca else ""
        if r["_humor"] and r["_humor"] not in HUMORES:
            corrigir.append("linha %d (%s): humor '%s' fora da lista" % (r["_linha"], cod or "?", r.get("humor", "")))
        tipo = norm(r.get("ultimo_contato_tipo", ""))
        if tipo in NAO_CONTAM:
            corrigir.append("linha %d (%s): ultimo_contato_tipo '%s' não conta como contato com o cliente "
                            "(resposta-ponte, cortesia, lembrete de documento e pesquisa ficam só no histórico); "
                            "ultimo_contato deve ser a data do último contato que informou algo do caso"
                            % (r["_linha"], cod or "?", r.get("ultimo_contato_tipo", "")))
        elif tipo and tipo not in TIPOS_CONTATO:
            corrigir.append("linha %d (%s): ultimo_contato_tipo '%s' fora da lista" % (r["_linha"], cod or "?", r.get("ultimo_contato_tipo", "")))
        r["_ultimo_tipo"] = tipo
        motivo = norm(r.get("motivo_proximo_contato", ""))
        if motivo and motivo not in MOTIVOS:
            corrigir.append("linha %d (%s): motivo_proximo_contato '%s' fora da lista" % (r["_linha"], cod or "?", r.get("motivo_proximo_contato", "")))
        r["_motivo"] = motivo
        comp = norm(r.get("proximo_compromisso", ""))
        if comp and comp not in COMPROMISSOS:
            corrigir.append("linha %d (%s): proximo_compromisso '%s' fora da lista" % (r["_linha"], cod or "?", r.get("proximo_compromisso", "")))
        r["_comp"] = comp
        if comp and not r["_data_compromisso"]:
            corrigir.append("linha %d (%s): compromisso '%s' sem data_compromisso" % (r["_linha"], cod or "?", comp))
        pend = (r.get("documentos_pendentes") or "").strip()
        try:
            r["_docs"] = int(pend) if pend else 0
        except ValueError:
            corrigir.append("linha %d (%s): documentos_pendentes '%s' não é número" % (r["_linha"], cod or "?", pend))
            r["_docs"] = 0
        if r["_ultimo_contato"] is None and r.get("ultimo_contato", "") == "":
            corrigir.append("linha %d (%s): ultimo_contato vazio (conta como sem notícia desde o início)" % (r["_linha"], cod or "?"))
        if r["_ultimo_contato"] and r["_ultimo_contato"] > hoje:
            corrigir.append("linha %d (%s): ultimo_contato no futuro (%s)" % (r["_linha"], cod or "?", r["_ultimo_contato"]))
        r["_reclamacao"] = sim(r.get("reclamacao_aberta", ""))
        r["_nao_receber"] = sim(r.get("pediu_para_nao_receber", ""))
        r["_resumo"] = sim(r.get("resumo_mensal", ""))
        if fase == "encerrado" or r["_encerrado_em"]:
            if fase != "encerrado" and r["_encerrado_em"]:
                corrigir.append("linha %d (%s): encerrado_em preenchido e fase '%s'" % (r["_linha"], cod or "?", r.get("fase", "")))
            encerrados.append(r)
        else:
            ativos.append(r)

    titulo_treino = " · TREINO" if (em_treino or "--treino" in op) else ""

    if "--conferir" in op:
        print("# Conferência da carteira%s · %s" % (titulo_treino, os.path.basename(caminho)))
        print()
        print("Lidas %d linhas de cliente (%d ativas, %d encerradas). Separador: '%s'." % (len(registros), len(ativos), len(encerrados), separador))
        if ausentes:
            print("Colunas que faltam (o resumo diário fica incompleto sem elas): %s." % ", ".join(ausentes))
        print()
        if corrigir:
            print("## Registro a corrigir (%d)" % len(corrigir))
            for c in corrigir:
                print("- " + c)
        else:
            print("Nenhum problema de formato encontrado.")
        return 0

    # Cálculos
    def dias_sem_noticia(r):
        base = r["_ultimo_contato"] or r["_inicio"]
        return (hoje - base).days if base else None

    pessoa = []
    combinados = []
    sem_noticia = []
    compromissos = []
    previstos = []
    documentos = []
    resumos = []
    nao_recebem = []
    encerramento = []
    cuidado = []

    fim_janela = hoje + timedelta(days=janela)
    mes = hoje.strftime("%Y-%m")
    com_jornada = []
    for r in ativos:
        dias = dias_sem_noticia(r)
        r["_dias"] = dias
        r["_maximo"], r["_regua_de"] = maximo_do_cliente(r)
        if r["_regua_de"]:
            com_jornada.append(r)
        alem = dias is not None and dias > r["_maximo"]
        dc = r["_data_compromisso"]
        comp_proximo = bool(r["_comp"] and dc and hoje <= dc <= fim_janela)
        historico = linhas_do_historico(os.path.join(pasta_clientes, r.get("codigo", ""), "historico.md"))
        r["_preparacao"] = ligacao_de_preparacao(historico, dc, hoje) if (comp_proximo and dc) else None
        if r["_preparacao"] and r["_ultimo_contato"] and r["_ultimo_contato"] < r["_preparacao"]:
            corrigir.append("linha %d (%s): o histórico tem a ligação de preparação em %s, mas o ultimo_contato é %s; "
                            "atualizar ultimo_contato e ultimo_contato_tipo = ligacao"
                            % (r["_linha"], r.get("codigo", "?"), r["_preparacao"].isoformat(), r["_ultimo_contato"].isoformat()))
        motivos_pessoa = []
        pc = r["_proximo_contato"]
        ja_falou = bool(r["_motivo"] == "retorno-combinado" and pc and pc > hoje and r["_ultimo_tipo"] in FALOU)
        motivos_combinado = []
        if r["_reclamacao"]:
            (motivos_combinado if ja_falou else motivos_pessoa).append("reclamação aberta")
        if r["_humor"] == "insatisfeito":
            (motivos_combinado if ja_falou else motivos_pessoa).append("humor insatisfeito")
        if motivos_combinado:
            combinados.append((r, motivos_combinado))
        if r["_motivo"] == "ligacao-pendente" and (pc is None or pc <= hoje):
            motivos_pessoa.append("ligação pendente: uma pessoa precisa ligar%s" % (
                " (desde %s)" % pc.isoformat() if pc and pc < hoje else ""))
        if not r["_preparacao"]:
            if r["_comp"] and dc and hoje <= dc <= util:
                quando = "hoje" if dc == hoje else ("amanhã" if dc == hoje + timedelta(days=1) else "até o próximo dia útil")
                motivos_pessoa.append("%s %s (%s, %s), sem ligação de preparação no histórico" % (
                    r["_comp"], quando, dc.isoformat(), dia_semana(dc)))
            if alem and comp_proximo and not (dc <= util):
                motivos_pessoa.append("%d dias sem notícia e %s em %d dias" % (dias, r["_comp"], (dc - hoje).days))
        if motivos_pessoa:
            pessoa.append((r, motivos_pessoa))
        if alem:
            sem_noticia.append(r)
        if comp_proximo:
            compromissos.append(r)
        elif r["_comp"] and dc and dc < hoje:
            corrigir.append("linha %d (%s): compromisso de %s já passou; atualizar proximo_compromisso" % (r["_linha"], r.get("codigo", "?"), dc.isoformat()))
        if pc and pc <= hoje:
            previstos.append(r)
        if r["_docs"] > 0:
            base = r["_ultimo_contato"] or r["_inicio"]
            idade = (hoje - base).days if base else None
            if idade is None or idade > docs_dias:
                documentos.append((r, idade))
        if r["_nao_receber"]:
            nao_recebem.append(r)
        elif r["_resumo"] and dia_resumo:
            st = status_do_resumo(os.path.join(pasta_clientes, r.get("codigo", ""), "resumos", mes + ".md"))
            feito = st == "enviado" or (st == "aprovado" and aprovado_basta)
            if not feito:
                r["_resumo_st"] = st
                resumos.append(r)
                if r["_ultimo_tipo"] == "resumo" and r["_ultimo_contato"] and r["_ultimo_contato"].strftime("%Y-%m") == mes:
                    corrigir.append("linha %d (%s): a carteira registra resumo enviado em %s, mas clientes/%s/resumos/%s.md "
                                    "não está com status: enviado (%s); marque o envio no arquivo"
                                    % (r["_linha"], r.get("codigo", "?"), r["_ultimo_contato"].isoformat(),
                                       r.get("codigo", ""), mes, "arquivo não existe" if st is None else "status: %s" % (st or "vazio")))
        if r["_fase"] == "encerramento":
            encerramento.append(r)
        avisos = []
        if r["_fase"] in ("decisao", "recurso"):
            avisos.append("fase %s: a advogada confirma se há notícia a dar por ligação antes de qualquer rascunho" % r["_fase"])
        if r["_humor"] == "a-confirmar":
            avisos.append("humor a confirmar: quem falou com o cliente atualiza")
        if avisos:
            cuidado.append((r, avisos))

    # Passagens sem boas-vindas
    passagens = []
    passagens_lidas = None
    if os.path.isdir(pasta_passagens):
        passagens_lidas = 0
        for nome in sorted(os.listdir(pasta_passagens)):
            if not nome.endswith(".md"):
                continue
            passagens_lidas += 1
            cod = nome[:-3]
            abertura = os.path.join(pasta_clientes, cod, "abertura.md")
            if not os.path.isfile(abertura):
                passagens.append((cod, cod in vistos))

    # Saída
    print("# Carteira%s · %s (%s)" % (titulo_treino, hoje.isoformat(), dia_semana(hoje)))
    print()
    print("Lidos: %d clientes ativos e %d encerrados (fora da conta), de %s." % (len(ativos), len(encerrados), os.path.basename(caminho)))
    print("Critérios: máximo sem notícia %d dias corridos (%s); documento pendente além de %d dias (%s); "
          "resumo mensal %s (%s); compromissos nos próximos %d dias; próximo dia útil %s."
          % (maximo, origem["maximo"], docs_dias, origem["docs"],
             ("até o dia %d" % dia_resumo) if dia_resumo else "não fazemos", origem["dia_resumo"],
             janela, util.isoformat()))
    if ficha:
        print("Ficha lida: %s" % ficha)
    if jornadas is None:
        print("Jornadas: pasta não encontrada (%s); vale o máximo da ficha para todos." % (pasta_jornadas or "sem pasta escritorio/"))
    elif not jornadas:
        print("Jornadas: nenhuma jornada-<tipo-de-caso>.md em %s; vale o máximo da ficha para todos." % pasta_jornadas)
    else:
        usam = [r for r in com_jornada if "vale a ficha" not in r["_regua_de"]]
        print("Jornadas lidas: %s. Régua da jornada em %d cliente(s)%s; os outros seguem a ficha."
              % (", ".join(sorted({j["arquivo"] for j in jornadas.values()})), len(usam),
                 (" (%s)" % ", ".join("%s: %d dias" % (r.get("codigo"), r["_maximo"]) for r in usam)) if usam else ""))
        for r in com_jornada:
            if "vale a ficha" in r["_regua_de"]:
                print("- %s · %s" % (rotulo(r), r["_regua_de"]))
    if aprovado_basta:
        print("Resumo do mês: o escritório não registra o envio; status aprovado conta como feito.")
    print("Hoje, em uma linha: %d para uma pessoa agora, %d sem notícia além da régua, %d compromissos em %d dias, "
          "%d contatos previstos vencidos ou de hoje, %d com documento pendente além da régua, %d resumos do mês por fazer."
          % (len(pessoa), len(sem_noticia), len(compromissos), janela, len(previstos), len(documentos), len(resumos)))
    print()

    print("## 1. PESSOA AGORA")
    if pessoa:
        for r, motivos in sorted(pessoa, key=lambda x: -len(x[1])):
            print("- %s · %s · responsável: %s" % (rotulo(r), "; ".join(motivos), r.get("responsavel") or "[A CONFIRMAR]"))
    else:
        print("Ninguém pelos critérios da carteira (reclamação aberta, insatisfeito, ligação pendente, compromisso até o "
              "próximo dia útil sem ligação de preparação). Mensagens novas ainda precisam ser triadas.")
    if combinados:
        print()
        print("Já falaram, com retorno combinado (voltam para cá no dia do retorno):")
        for r, motivos in combinados:
            print("- %s · %s · %s em %s; retorno combinado para %s (%s)" % (
                rotulo(r), "; ".join(motivos), r["_ultimo_tipo"], r["_ultimo_contato"].isoformat() if r["_ultimo_contato"] else "?",
                r["_proximo_contato"].isoformat(), dia_semana(r["_proximo_contato"])))
    print()

    print("## 2. Compromissos nos próximos %d dias" % janela)
    if compromissos:
        for r in sorted(compromissos, key=lambda x: x["_data_compromisso"]):
            dc = r["_data_compromisso"]
            falta = (dc - hoje).days
            quando = "hoje" if falta == 0 else ("amanhã" if falta == 1 else "em %d dias" % falta)
            print("- %s (%s) · %s · %s · %s · humor: %s%s" % (
                dc.isoformat(), dia_semana(dc), r["_comp"], rotulo(r), quando, r["_humor"] or "não registrado",
                " · ligação de preparação em %s" % r["_preparacao"].isoformat() if r["_preparacao"] else ""))
    else:
        print("Nenhum compromisso registrado na janela.")
    print()

    print("## 3. Sem notícia além da régua (mais de %d dias pela ficha, ou o máximo da jornada)" % maximo)
    if sem_noticia:
        for r in sorted(sem_noticia, key=lambda x: -x["_dias"]):
            base = r["_ultimo_contato"] or r["_inicio"]
            print("- %s · %d dias · último contato %s · máximo %d (%s)%s" % (
                rotulo(r), r["_dias"], base.isoformat(), r["_maximo"], r["_regua_de"] or "ficha",
                " (pediu para não receber rotina: avisar como ele prefere)" if r["_nao_receber"] else ""))
    else:
        print("Ninguém além da régua.")
    sem_data = [r for r in ativos if r["_dias"] is None]
    for r in sem_data:
        print("- %s · sem ultimo_contato nem inicio: não dá para calcular" % rotulo(r))
    print()

    print("## 4. Contatos previstos (hoje e vencidos)")
    if previstos:
        for r in sorted(previstos, key=lambda x: x["_proximo_contato"]):
            pc = r["_proximo_contato"]
            atraso = (hoje - pc).days
            print("- %s · %s · %s" % (rotulo(r), r["_motivo"] or "motivo não registrado",
                                      "hoje" if atraso == 0 else "venceu há %d dias (%s)" % (atraso, pc.isoformat())))
    elif "proximo_contato" in cabeca:
        print("Nenhum contato previsto para hoje ou vencido.")
    else:
        print("A carteira não tem a coluna proximo_contato.")
    print()

    print("## 5. Documentos pendentes além da régua (mais de %d dias)" % docs_dias)
    if documentos:
        for r, idade in documentos:
            print("- %s · %d documento(s) · %s · detalhe em clientes/%s/documentos.md" % (
                rotulo(r), r["_docs"], ("%d dias desde o último contato" % idade) if idade is not None else "sem data",
                r.get("codigo", "")))
    elif "documentos_pendentes" in cabeca:
        print("Nenhum documento pendente além da régua.")
    else:
        print("A carteira não tem a coluna documentos_pendentes.")
    print()

    print("## 6. Resumos do mês (%s)" % mes)
    if not dia_resumo:
        print("O escritório não faz resumo mensal (ficha).")
    elif "resumo_mensal" not in cabeca:
        print("A carteira não tem a coluna resumo_mensal.")
    elif resumos:
        prazo = date(hoje.year, hoje.month, min(dia_resumo, 28))
        situacao = "venceu em %s" % prazo.isoformat() if prazo < hoje else ("vence hoje" if prazo == hoje else "vence em %s" % prazo.isoformat())
        print("Por fazer (%s):" % situacao)
        cuidado_cod = {r.get("codigo") for r, _ in cuidado}
        situacoes = {None: "", "": " · arquivo do mês sem status no cabeçalho",
                     "rascunho": " · rascunho no arquivo do mês: falta aprovar e enviar",
                     "pendente": " · rascunho no arquivo do mês: falta aprovar e enviar",
                     "aprovado": " · aprovado: falta enviar e marcar status: enviado",
                     "descartado": " · descartado: refazer"}
        for r in resumos:
            nota = situacoes.get(r.get("_resumo_st"), " · status '%s' no arquivo do mês" % r.get("_resumo_st"))
            if r["_humor"] == "insatisfeito" or r["_reclamacao"]:
                nota += " · uma pessoa fala antes; resumo só depois"
            elif r.get("codigo") in cuidado_cod:
                nota += " · conferir a notícia antes (seção 9)"
            print("- %s%s" % (rotulo(r), nota))
    else:
        print("Todos os resumos do mês foram enviados (status: enviado%s) ou não se aplicam."
              % (" ou aprovado" if aprovado_basta else ""))
    if nao_recebem:
        print("Não recebem resumo nem mensagem de rotina (pediram): %s. Notícia relevante continua, do jeito que o cliente prefere."
              % ", ".join(rotulo(r) for r in nao_recebem))
    print()

    print("## 7. Encerramento em aberto")
    if encerramento:
        for r in encerramento:
            print("- %s · fase encerramento · conferir prestação de contas e o que falta para encerrar" % rotulo(r))
    else:
        print("Nenhum caso em encerramento.")
    print()

    print("## 8. Passagens sem boas-vindas")
    if passagens_lidas is None:
        print("Pasta de passagens não encontrada (%s). Sem o motor-comercial, cliente novo entra pela boas-vindas." % pasta_passagens)
    elif passagens:
        for cod, na_carteira in passagens:
            print("- %s · sem clientes/%s/abertura.md%s" % (cod, cod, "" if na_carteira else " · e sem linha na carteira"))
    else:
        print("%d passagens lidas, todas com boas-vindas." % passagens_lidas)
    print()

    print("## 9. Cuidado antes de qualquer mensagem de rotina")
    if cuidado:
        for r, avisos in cuidado:
            print("- %s · %s" % (rotulo(r), "; ".join(avisos)))
    else:
        print("Nada a observar.")
    print()

    print("## 10. Registro a corrigir")
    if corrigir:
        for c in corrigir:
            print("- " + c)
    else:
        print("Nenhum problema de formato.")
    if ausentes:
        print("- colunas ausentes (seções que dependem delas ficam incompletas): %s" % ", ".join(ausentes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
