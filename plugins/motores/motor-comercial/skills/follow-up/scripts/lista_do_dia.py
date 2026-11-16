#!/usr/bin/env python3
"""Lista do dia do follow-up, a partir do contatos.csv do funil.

Uso:
    python3 lista_do_dia.py <contatos.csv> [--data AAAA-MM-DD] [--ficha <ficha-comercial.md>]
                            [--regua "nao-agendou: 2, 7, 15 · faltou: 0, 3, 10 · proposta-sem-resposta: 2, 7, 15"]
                            [--maximo 3] [--dias-para-decidir 7] [--json]
                            [--feriados "2026-04-21, 2026-06-04"] [--ficha-do-escritorio <ficha-do-escritorio.md>]

O que faz (só lê; quem grava é a habilidade, depois do ok):
1. PARA UMA PESSOA, FORA DA RÉGUA (nunca entram na lista de mensagem pronta,
   conforme docs/funil.md, regra 4, marcador de pessoa, e regra 5, fora da
   régua): proximo_passo com "pessoa agora:" ou "pessoa liga:", urgência alta
   sem pessoa designada, área fora-da-area, parada imediata e caso sensível
   (violência, ameaça, criança, risco, prisão, vulnerabilidade).
2. RETORNOS DE HOJE: etapas triado, nao-compareceu, proposta-enviada e
   negociando (ou qualquer etapa aberta, quando o proximo_passo nomeia uma
   situação nova da régua), com proximo_passo "retorno N de M" (o que a triagem
   arma) ou "retorno combinado", e data_proximo_passo até a data pedida. Para
   cada um, a linha do registro depois do envio, com a data pela régua em dias
   corridos. Data que cai em sábado, domingo ou feriado da ficha passa para o
   próximo dia útil (triar-contato, seção 4.4). Convite recém-triado com retorno
   em data futura não aparece: ainda não é dia.
3. PARA DECIDIR: "confirmar perdido", retorno passado do máximo, retorno sem
   data, data vencida sem retorno marcado, e retorno vencido de quem ainda não
   recebeu a primeira resposta (o convite saiu?).
4. NÃO ENVIAR: pediu_para_parar = sim. Se a linha ainda tem retorno marcado,
   aparece como linha a corrigir.

A régua vem do campo follow_up da ficha comercial (dias corridos, contados do
fato que abriu a régua), por situação: "nao-agendou: 2, 7, 15 · faltou: 0, 3, 10
· proposta-sem-resposta: 2, 7, 15", com as situações separadas por "·", por ";"
ou uma por linha. Situação nova do escritório entra com o nome que estiver no
campo (ex.: "documentos-pendentes: 3, 7"), e vale para a linha cujo
proximo_passo traz esse nome ("retorno 1 de 2 · documentos-pendentes"). Texto
entre parênteses no campo (a explicação do modelo da ficha) é ignorado. Sem
--ficha e sem --regua, o script procura escritorio/04-base/comum/ficha-comercial.md
a partir do csv.

Os feriados vêm de --feriados ou do campo feriados_e_recessos da ficha do
escritório (--ficha-do-escritorio, ou escritorio/04-base/comum/ficha-do-escritorio.md
procurada a partir do csv): datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM (este ano e o
seguinte), e "de DD/MM a DD/MM" para recesso. Campo vazio ou [A PREENCHER]: só
sábado e domingo passam para o próximo dia útil, com aviso no topo da lista.

O csv pode ter vírgula ou ponto e vírgula, BOM, UTF-8 ou Windows-1252, datas
AAAA-MM-DD ou DD/MM/AAAA, e etapas em maiúsculas ou com acento.

Saída: 0 quando lê o registro; 1 quando falta o arquivo, falta coluna
obrigatória, o registro não tem nenhuma linha ou um argumento está errado.
"""

import csv
import datetime
import io
import json
import os
import re
import sys
import unicodedata

OBRIGATORIAS = [
    "codigo", "nome_curto", "area", "urgencia", "etapa", "responsavel",
    "proximo_passo", "data_proximo_passo", "pediu_para_parar",
]
OPCIONAIS = ["canal", "assunto", "primeira_resposta", "atualizado_em", "entrada", "tipo"]

ETAPAS_DA_REGUA = {
    "triado": "nao-agendou",
    "nao-compareceu": "faltou",
    "proposta-enviada": "proposta-sem-resposta",
    "negociando": "proposta-sem-resposta",
}
ENCERRADAS = {"fechado", "encaminhado", "recusado", "sem-caso", "perdido"}
NOME_SITUACAO = {
    "nao-agendou": "não agendou",
    "faltou": "faltou à consulta",
    "proposta-sem-resposta": "proposta sem resposta",
}
# Nomes antigos ou do jeito que a pessoa escreve, levados ao nome da ficha.
APELIDOS = {
    "nao-agendou": "nao-agendou", "nao-agendaram": "nao-agendou", "sem-agendamento": "nao-agendou",
    "faltou": "faltou", "faltou-a-consulta": "faltou", "faltou-na-consulta": "faltou",
    "nao-compareceu": "faltou", "falta": "faltou",
    "proposta-sem-resposta": "proposta-sem-resposta", "proposta": "proposta-sem-resposta",
    "proposta-sem-retorno": "proposta-sem-resposta",
}

# Palavras que, no assunto ou no próximo passo, indicam parada imediata ou caso
# sensível. Comparadas sem acento e sem maiúscula, como palavra inteira ou começo.
SINAIS_SENSIVEIS = [
    r"parada imediata", r"pessoa agora", r"violenci\w*", r"ameac\w*", r"agress\w*",
    r"medida protetiva", r"crianc\w*", r"adolescent\w*", r"menor(es)? de idade",
    r"risco\w*", r"suicid\w*", r"preso", r"presa", r"pris(ao|oes)", r"flagrante",
    r"vulnerab\w*", r"sem renda", r"idos[oa]s?", r"abuso\w*", r"estupro",
    r"sensivel", r"advogad[oa] liga\w*", r"ligar agora", r"pessoa liga",
]
RE_SENSIVEL = re.compile(r"\b(" + "|".join(SINAIS_SENSIVEIS) + r")\b")
RE_RETORNO = re.compile(r"retorno\s+(\d+)\s*(?:de|/)\s*(\d+)")
RE_COMBINADO = re.compile(r"retorno\s+combinado")
RE_PERDIDO = re.compile(r"confirmar\s+perdido")
SEM_PESSOA = {"", "-", "a-definir", "a definir", "[a definir]", "[a preencher]", "ninguem", "nenhum", "?"}


def normal(texto):
    texto = unicodedata.normalize("NFD", (texto or "").strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def normal_1a1(texto):
    """Minúsculas e sem acento, com o mesmo tamanho do texto original."""
    saida = []
    for c in (texto or "").lower():
        base = "".join(x for x in unicodedata.normalize("NFD", c) if unicodedata.category(x) != "Mn")
        saida.append(base if len(base) == 1 else c)
    return "".join(saida)


def etapa_normal(texto):
    return re.sub(r"[\s_]+", "-", normal(texto))


def ler_data(texto):
    texto = (texto or "").strip()
    if not texto:
        return None
    for formato, tamanho in (("%Y-%m-%d", 10), ("%d/%m/%Y", 10), ("%d/%m/%y", 8), ("%d-%m-%Y", 10)):
        try:
            return datetime.datetime.strptime(texto[:tamanho], formato).date()
        except ValueError:
            continue
    return None


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(codificacao)
        except UnicodeDecodeError:
            continue
    raise ValueError("não consegui ler o arquivo como texto (UTF-8 ou Windows-1252)")


def ler_registro(caminho):
    texto = ler_texto(caminho)
    linhas_nao_vazias = [l for l in texto.splitlines() if l.strip()]
    if not linhas_nao_vazias:
        raise ValueError("o arquivo está vazio: %s" % caminho)
    cabecalho = linhas_nao_vazias[0]
    separador = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
    leitor = csv.reader(io.StringIO(texto), delimiter=separador)
    linhas = [l for l in leitor if any(c.strip() for c in l)]
    nomes = [normal(c).replace(" ", "_") for c in linhas[0]]
    faltam = [c for c in OBRIGATORIAS if c not in nomes]
    if faltam:
        raise ValueError(
            "faltam colunas obrigatórias no contatos.csv: %s. A primeira linha precisa ser a de docs/funil.md."
            % ", ".join(faltam))
    registros = []
    for numero, valores in enumerate(linhas[1:], start=2):
        r = {nome: (valores[i].strip() if i < len(valores) else "") for i, nome in enumerate(nomes)}
        r["_linha"] = numero
        registros.append(r)
    return registros, separador, [c for c in OPCIONAIS if c not in nomes]


# ---------- régua ----------

def situacao_do_texto(texto):
    """Nome da situação como a ficha escreve: 'não agendou' -> 'nao-agendou'.
    Nome que não é um dos três vira situação nova, com o nome que estiver no campo."""
    nome = re.sub(r"[^a-z0-9-]+", "-", normal(texto)).strip("-")
    nome = re.sub(r"-+", "-", nome)
    if not nome:
        return None
    return APELIDOS.get(nome, nome)


def sem_parenteses(texto):
    anterior = None
    while anterior != texto:
        anterior, texto = texto, re.sub(r"\([^()]*\)", " ", texto or "")
    return texto


def partes_da_regua(texto):
    return [p for p in re.split(r"[;\n\u00b7]|\s\|\s", sem_parenteses(texto or "")) if p.strip()]


def ler_regua(texto):
    """'nao-agendou: 2, 7, 15 · faltou: 0, 3, 10' -> {'nao-agendou': [2, 7, 15], ...}"""
    regua = {}
    for parte in partes_da_regua(texto):
        if ":" not in parte:
            continue
        nome, _, numeros = parte.partition(":")
        situacao = situacao_do_texto(nome.lstrip("-* "))
        dias = [int(n) for n in re.findall(r"\d+", numeros)]
        if situacao and dias:
            regua[situacao] = dias
    return regua


def ler_maximo(texto):
    """'3' ou 'nao-agendou: 3 · proposta-sem-resposta: 2' -> {'*': 3} ou {...}"""
    texto = sem_parenteses(texto or "")
    if ":" not in texto:
        n = re.findall(r"\d+", texto)
        return {"*": int(n[0])} if n else {}
    maximo = {}
    for parte in partes_da_regua(texto):
        nome, _, numeros = parte.partition(":")
        situacao = situacao_do_texto(nome.lstrip("-* "))
        n = re.findall(r"\d+", numeros)
        if situacao and n:
            maximo[situacao] = int(n[0])
    return maximo


def nome_da_situacao(situacao):
    return NOME_SITUACAO.get(situacao, situacao.replace("-", " "))


def campo_da_ficha(texto, campo):
    """Valor do campo, com as linhas de continuação (mais recuadas que a do campo)."""
    linhas = texto.splitlines()
    padrao = re.compile(r"^(\s*)[-*]?\s*%s\s*:\s*(.*)$" % re.escape(campo))
    for i, linha in enumerate(linhas):
        m = padrao.match(linha)
        if not m:
            continue
        recuo = len(m.group(1).replace("\t", "    "))
        partes = [m.group(2).strip()]
        for seguinte in linhas[i + 1:]:
            if not seguinte.strip():
                break
            recuo_seg = len(seguinte) - len(seguinte.lstrip(" \t"))
            if recuo_seg <= recuo or seguinte.lstrip().startswith("#"):
                break
            partes.append(seguinte.strip().lstrip("-* ").strip())
        valor = "\n".join(p for p in partes if p)
        if "[A PREENCHER]" in valor.upper() or "[A DEFINIR]" in valor.upper():
            return ""
        return valor
    return ""


def achar_ficha(caminho_csv):
    pasta = os.path.dirname(os.path.abspath(caminho_csv))
    for _ in range(5):
        candidato = os.path.join(pasta, "04-base", "comum", "ficha-comercial.md")
        if os.path.isfile(candidato):
            return candidato
        pasta = os.path.dirname(pasta)
    return None


# ---------- feriados e dia útil ----------

MARCACAO_RE = re.compile(r"\[\s*(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]", re.I)
DATA_TXT = r"\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}(?:/\d{2,4})?"


def datas_do_texto(texto, ano):
    """Datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM (no ano dado) em qualquer texto, com intervalos."""
    datas = set()
    for m in re.finditer(r"(\d{4})-(\d{1,2})-(\d{1,2})|(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", texto or ""):
        try:
            if m.group(1):
                datas.add(datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
            else:
                a = int(m.group(6)) if m.group(6) else ano
                a += 2000 if a < 100 else 0
                datas.add(datetime.date(a, int(m.group(5)), int(m.group(4))))
        except ValueError:
            raise ValueError("feriado inválido: %s. Use AAAA-MM-DD ou DD/MM/AAAA." % m.group(0))
    for m in re.finditer(r"(%s)\s*(?:a|ate|até|-)\s*(%s)" % (DATA_TXT, DATA_TXT), texto or ""):
        d_ini, d_fim = min(datas_do_texto(m.group(1), ano)), min(datas_do_texto(m.group(2), ano))
        if d_fim < d_ini and m.group(2).count("/") == 1:
            datas.discard(d_fim)
            d_fim = d_fim.replace(year=d_fim.year + 1)
        if 0 < (d_fim - d_ini).days <= 60:
            d = d_ini
            while d <= d_fim:
                datas.add(d)
                d += datetime.timedelta(days=1)
    return datas


def ler_feriados(texto, hoje):
    """Campo feriados_e_recessos -> (datas, aviso). Marcação nunca vira data."""
    limpo = MARCACAO_RE.sub(" ", texto or "")
    if not re.sub(r"[\s;,.\u00b7-]", "", limpo):
        return set(), "campo feriados_e_recessos da ficha vazio: só sábado e domingo passam para o próximo dia útil"
    datas = datas_do_texto(limpo, hoje.year) | datas_do_texto(limpo, hoje.year + 1)
    sobra = re.sub(DATA_TXT, "", limpo)
    if not datas and re.search(r"\d", sobra):
        raise ValueError("não achei datas em feriados_e_recessos: %s. Use AAAA-MM-DD ou DD/MM/AAAA, "
                         "separadas por vírgula." % texto.strip())
    return datas, ""


def achar_ficha_do_escritorio(caminho_csv):
    pasta = os.path.dirname(os.path.abspath(caminho_csv))
    for _ in range(5):
        candidato = os.path.join(pasta, "04-base", "comum", "ficha-do-escritorio.md")
        if os.path.isfile(candidato):
            return candidato
        pasta = os.path.dirname(pasta)
    return None


def dia_util(d, feriados):
    """A própria data, ou o próximo dia que não é sábado, domingo nem feriado."""
    for _ in range(60):
        if d.weekday() < 5 and d not in feriados:
            return d
        d += datetime.timedelta(days=1)
    return d


# ---------- classificação ----------

def sem_pessoa(responsavel):
    return normal(responsavel) in SEM_PESSOA


def motivo_fora(r):
    """Motivo para ficar fora da régua (funil.md, regra 4, marcador de pessoa, e regra 5,
    fora da régua), ou None."""
    area = etapa_normal(r.get("area"))
    urgencia = normal(r.get("urgencia"))
    original = (r.get("assunto") or "") + " | " + (r.get("proximo_passo") or "")
    texto = normal_1a1(original)
    m = RE_SENSIVEL.search(texto)
    if m:
        return "parada imediata ou caso sensível (\"%s\"): uma pessoa decide se e como retomar" % original[m.start():m.end()]
    if area == "fora-da-area":
        return "área fora-da-area: encaminhamento com uma pessoa, sem retorno de venda"
    if urgencia == "alta" and sem_pessoa(r.get("responsavel")):
        return "urgência alta sem pessoa designada: designar quem cuida antes de qualquer retorno"
    return None


def no_dia_util(passo, candidata, nota, feriados):
    """Data que cai em sábado, domingo ou feriado da ficha passa para o próximo dia útil."""
    util = dia_util(candidata, feriados)
    if util != candidata:
        motivo = "feriado" if candidata in feriados else ("sábado" if candidata.weekday() == 5 else "domingo")
        nota += "; %s caía em %s: passou para o próximo dia útil" % (candidata.isoformat(), motivo)
    return passo, util, nota


def proxima_data(r, situacao, n, regua, hoje, dias_para_decidir, total, feriados=frozenset()):
    """Linha do registro depois do envio deste retorno."""
    data = ler_data(r.get("data_proximo_passo"))
    if n >= total:
        return no_dia_util("confirmar perdido", hoje + datetime.timedelta(days=dias_para_decidir),
                           "exemplo: %d dias corridos para o advogado decidir" % dias_para_decidir, feriados)
    dias = regua.get(situacao)
    if not dias or len(dias) < n + 1:
        return "retorno %d de %d" % (n + 1, total), None, "sem a régua desta situação na ficha: data [A DEFINIR]"
    intervalo = dias[n] - dias[n - 1] if n >= 1 else dias[0]
    fato = data - datetime.timedelta(days=dias[n - 1]) if data else None
    candidata = fato + datetime.timedelta(days=dias[n]) if fato else hoje + datetime.timedelta(days=intervalo)
    if candidata <= hoje:
        candidata = hoje + datetime.timedelta(days=max(intervalo, 1))
    return no_dia_util("retorno %d de %d" % (n + 1, total), candidata, "régua em dias corridos", feriados)


def classificar(registros, hoje, regua, maximo, dias_para_decidir, tem_primeira_resposta, feriados=frozenset()):
    grupos = {"pessoa": [], "retornos": [], "decidir": [], "nao_enviar": []}
    for r in registros:
        etapa = etapa_normal(r.get("etapa"))
        passo = normal(r.get("proximo_passo"))
        parar = normal(r.get("pediu_para_parar")) in ("sim", "s", "yes", "true", "1")
        data = ler_data(r.get("data_proximo_passo"))
        m = RE_RETORNO.search(passo)
        tem_retorno = bool(m or RE_COMBINADO.search(passo))

        if parar:
            if tem_retorno or (etapa in ETAPAS_DA_REGUA and passo not in ("", "nenhum", "-")):
                grupos["nao_enviar"].append((r, "pediu para parar, mas a linha ainda tem próximo passo: trocar por \"nenhum\""))
            else:
                grupos["nao_enviar"].append((r, "pediu para parar: fora de qualquer retorno"))
            continue
        situacao_nova = next((s for s in regua if s not in NOME_SITUACAO
                              and re.search(r"\b%s\b" % re.escape(s), etapa_normal(r.get("proximo_passo")))), None)
        if etapa in ENCERRADAS or (etapa not in ETAPAS_DA_REGUA and not situacao_nova):
            continue

        motivo = motivo_fora(r)
        if motivo:
            if tem_retorno:
                motivo += "; a linha tem retorno marcado: tirar da régua"
            grupos["pessoa"].append((r, motivo))
            continue

        if (tem_retorno and data is not None and data > hoje):
            continue  # convite recém-triado ou retorno marcado para depois: ainda não é dia

        if (tem_retorno and etapa == "triado" and tem_primeira_resposta
                and not (r.get("primeira_resposta") or "").strip()):
            grupos["decidir"].append((r, "retorno vencido e primeira_resposta vazia: o convite saiu? "
                                         "Se saiu, preencher primeira_resposta e mandar o retorno; se não, "
                                         "mandar o convite primeiro (o retorno não conta)"))
            continue

        situacao = situacao_nova or ETAPAS_DA_REGUA[etapa]
        if RE_PERDIDO.search(passo):
            grupos["decidir"].append((r, "encerramento enviado sem resposta: marcar `perdido` com `motivo_perda = sem-resposta`? Só com o ok do advogado"))
            continue
        if RE_COMBINADO.search(passo):
            if data is None:
                grupos["decidir"].append((r, "retorno combinado sem data: definir a data que a pessoa pediu"))
            elif data <= hoje:
                grupos["retornos"].append({"r": r, "situacao": situacao, "n": 0, "total": 0,
                                           "atraso": (hoje - data).days, "depois": ("retorno combinado feito: definir próximo passo", None, "")})
            continue
        if m:
            n, total = int(m.group(1)), int(m.group(2))
            limite = maximo.get(situacao)
            if limite is None:
                limite = len(regua[situacao]) if situacao not in NOME_SITUACAO and situacao in regua else maximo.get("*")
            if n < 1 or total < 1:
                grupos["decidir"].append((r, "próximo passo \"%s\" com número inválido: conferir a linha" % (r.get("proximo_passo") or "-")))
                continue
            if data is None:
                grupos["decidir"].append((r, "retorno %d de %d sem data: definir a data pela régua" % (n, total)))
                continue
            if n > total or (limite and n > limite):
                grupos["decidir"].append((r, "retorno %d de %d passa do máximo (%s): conferir a linha" % (n, total, limite or total)))
                continue
            if data <= hoje:
                obs = []
                if limite and total != limite:
                    obs.append("a linha diz %d retornos e a ficha diz %d" % (total, limite))
                if normal(r.get("urgencia")) == "alta":
                    obs.append("urgência alta: quem cuida lê com atenção e decide se liga em vez de escrever")
                grupos["retornos"].append({"r": r, "situacao": situacao, "n": n, "total": total,
                                           "atraso": (hoje - data).days, "obs": obs,
                                           "depois": proxima_data(r, situacao, n, regua, hoje, dias_para_decidir, total, feriados)})
            continue
        if data is not None and data < hoje:
            grupos["decidir"].append((r, "próximo passo \"%s\" venceu em %s e não há retorno marcado: entrar na régua?" % (
                r.get("proximo_passo") or "-", data.isoformat())))
    return grupos


# ---------- saída ----------

def celula(texto):
    return (texto or "").replace("|", "/").strip() or "-"


def imprimir(grupos, hoje, n_linhas, origem_regua, regua, maximo, faltando, origem_feriados=""):
    print("# Follow-up do dia · %s" % hoje.isoformat())
    print()
    print("Linhas lidas no registro: %d. Régua: %s." % (n_linhas, origem_regua))
    if origem_feriados:
        print("Dias sem expediente: %s." % origem_feriados)
    if regua:
        print("Dias corridos por situação: %s. Máximo: %s." % (
            "; ".join("%s %s" % (nome_da_situacao(k), ", ".join(map(str, v))) for k, v in regua.items()),
            ", ".join("%s" % v if k == "*" else "%s %d" % (nome_da_situacao(k), v) for k, v in maximo.items()) or "não informado"))
    if faltando:
        print("Colunas que o registro não tem (o script segue sem elas): %s." % ", ".join(faltando))
    print()

    print("## 1. Para uma pessoa, fora da régua (nenhuma mensagem pronta)")
    print()
    if grupos["pessoa"]:
        for r, motivo in grupos["pessoa"]:
            print("- %s · %s · %s · %s: %s" % (celula(r["codigo"]), celula(r["nome_curto"]),
                                              celula(r.get("area")), celula(r.get("responsavel")), motivo))
    else:
        print("Ninguém nesta situação hoje.")
    print()

    print("## 2. Retornos de hoje (mensagem pronta, uma pessoa lê e envia)")
    print()
    if grupos["retornos"]:
        print("| Código | Nome | Situação | Retorno | Atraso | Canal | Quem envia | Depois do envio | Observação |")
        print("|---|---|---|---|---|---|---|---|---|")
        for item in sorted(grupos["retornos"], key=lambda i: (-i["atraso"], i["r"]["codigo"])):
            r, n, total = item["r"], item["n"], item["total"]
            if total == 0:
                rotulo = "retorno combinado"
            elif n >= total:
                rotulo = "encerramento (%d de %d)" % (n, total)
            else:
                rotulo = "retorno %d de %d" % (n, total)
            passo, data, nota = item["depois"]
            depois = "%s em %s" % (passo, data.isoformat()) if data else passo
            if nota and "A DEFINIR" in nota:
                depois += " (%s)" % nota
            elif nota and "próximo dia útil" in nota:
                depois += " (%s)" % nota.split("; ", 1)[1]
            print("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                celula(r["codigo"]), celula(r["nome_curto"]), nome_da_situacao(item["situacao"]), rotulo,
                "%d dia(s)" % item["atraso"] if item["atraso"] else "hoje",
                celula(r.get("canal")), celula(r.get("responsavel")), celula(depois),
                celula("; ".join(item.get("obs", [])))))
    else:
        print("Nenhum retorno vence hoje.")
    print()

    print("## 3. Para decidir")
    print()
    if grupos["decidir"]:
        for r, motivo in grupos["decidir"]:
            print("- %s · %s: %s" % (celula(r["codigo"]), celula(r["nome_curto"]), motivo))
    else:
        print("Nada para decidir.")
    print()

    print("## 4. Não enviar")
    print()
    if grupos["nao_enviar"]:
        for r, motivo in grupos["nao_enviar"]:
            print("- %s · %s: %s" % (celula(r["codigo"]), celula(r["nome_curto"]), motivo))
    else:
        print("Ninguém pediu para parar.")
    print()
    print("Resumo: %d para uma pessoa, %d retorno(s) hoje, %d para decidir, %d não enviar." % (
        len(grupos["pessoa"]), len(grupos["retornos"]), len(grupos["decidir"]), len(grupos["nao_enviar"])))


def em_json(grupos, hoje, n_linhas, origem_regua, origem_feriados=""):
    def base(r):
        return {k: r.get(k, "") for k in ("codigo", "nome_curto", "area", "canal", "responsavel",
                                            "urgencia", "etapa", "proximo_passo", "data_proximo_passo")}
    saida = {"data": hoje.isoformat(), "linhas_lidas": n_linhas, "regua": origem_regua,
             "dias_sem_expediente": origem_feriados,
             "para_uma_pessoa": [dict(base(r), motivo=m) for r, m in grupos["pessoa"]],
             "retornos": [], "para_decidir": [dict(base(r), motivo=m) for r, m in grupos["decidir"]],
             "nao_enviar": [dict(base(r), motivo=m) for r, m in grupos["nao_enviar"]]}
    for item in grupos["retornos"]:
        passo, data, nota = item["depois"]
        saida["retornos"].append(dict(base(item["r"]), situacao=item["situacao"], retorno=item["n"],
                                      de=item["total"], encerramento=bool(item["total"] and item["n"] >= item["total"]),
                                      atraso_dias=item["atraso"], observacoes=item.get("obs", []),
                                      depois_proximo_passo=passo,
                                      depois_data=data.isoformat() if data else "", nota=nota))
    print(json.dumps(saida, ensure_ascii=False, indent=2))


def valor_da_opcao(argv, nome):
    if nome not in argv:
        return None
    i = argv.index(nome)
    if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
        raise ValueError("falta o valor depois de %s" % nome)
    return argv[i + 1]


def main(argv):
    if "--ajuda" in argv or "--help" in argv:
        print(__doc__)
        return 0
    try:
        data_txt = valor_da_opcao(argv, "--data")
        ficha_txt = valor_da_opcao(argv, "--ficha")
        regua_txt = valor_da_opcao(argv, "--regua")
        maximo_txt = valor_da_opcao(argv, "--maximo")
        decidir_txt = valor_da_opcao(argv, "--dias-para-decidir")
        feriados_txt = valor_da_opcao(argv, "--feriados")
        ficha_esc_txt = valor_da_opcao(argv, "--ficha-do-escritorio")
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1
    usados = {v for v in (data_txt, ficha_txt, regua_txt, maximo_txt, decidir_txt, feriados_txt, ficha_esc_txt)
              if v is not None}
    args = [a for a in argv[1:] if not a.startswith("--") and a not in usados]
    if not args:
        print("ERRO: diga onde está o contatos.csv.")
        print("Exemplo: python3 scripts/lista_do_dia.py escritorio/07-operacao/comercial/contatos.csv")
        return 1

    if len(args) > 1:
        # a data também pode vir logo depois do csv, como no script da rotina
        if data_txt is None and len(args) == 2 and ler_data(args[1]) is not None:
            data_txt = args[1]
        else:
            print("ERRO: argumento a mais que não entendi: %s" % " ".join(args[1:]))
            print("Use --data AAAA-MM-DD para a data da lista.")
            return 1
    hoje = datetime.date.today()
    if data_txt is not None:
        hoje = ler_data(data_txt)
        if hoje is None:
            print("ERRO: data inválida em --data (use AAAA-MM-DD ou DD/MM/AAAA): %s" % data_txt)
            return 1
    dias_para_decidir = 7
    if decidir_txt is not None:
        if not decidir_txt.isdigit():
            print("ERRO: --dias-para-decidir precisa ser um número de dias")
            return 1
        dias_para_decidir = int(decidir_txt)

    caminho = args[0]
    if not os.path.isfile(caminho):
        print("ERRO: não achei o contatos.csv em: %s" % caminho)
        print("Nada foi lido. Confira o caminho (o registro fica em escritorio/07-operacao/comercial/contatos.csv).")
        return 1
    try:
        registros, _, faltando = ler_registro(caminho)
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1
    if not registros:
        print("ERRO: o contatos.csv só tem a linha de cabeçalho. Nenhum contato foi lido, então não há lista do dia.")
        return 1

    regua, maximo, origem = {}, {}, "não informada"
    if regua_txt is not None:
        regua = ler_regua(regua_txt)
        origem = "informada no comando"
    else:
        ficha = ficha_txt or achar_ficha(caminho)
        if ficha_txt and not os.path.isfile(ficha_txt):
            print("ERRO: não achei a ficha comercial em: %s" % ficha_txt)
            return 1
        if ficha:
            texto = ler_texto(ficha)
            regua = ler_regua(campo_da_ficha(texto, "follow_up"))
            maximo = ler_maximo(campo_da_ficha(texto, "maximo_de_retornos"))
            origem = "campo follow_up de %s" % ficha
            if "uteis" in normal(campo_da_ficha(texto, "follow_up")):
                origem += " (a ficha fala em dias úteis; a régua conta em dias corridos, docs/funil.md, regra 3)"
    if maximo_txt is not None:
        maximo = ler_maximo(maximo_txt)
    if not regua:
        origem += "; sem a régua, as datas do próximo retorno ficam [A DEFINIR]"

    origem_feriados = "sábado e domingo"
    try:
        if feriados_txt is not None:
            feriados, aviso = ler_feriados(feriados_txt, hoje)
            fonte = "informados no comando"
        else:
            ficha_esc = ficha_esc_txt or achar_ficha_do_escritorio(caminho)
            if ficha_esc_txt and not os.path.isfile(ficha_esc_txt):
                print("ERRO: não achei a ficha do escritório em: %s" % ficha_esc_txt)
                return 1
            if ficha_esc:
                feriados, aviso = ler_feriados(campo_da_ficha(ler_texto(ficha_esc), "feriados_e_recessos"), hoje)
                fonte = "campo feriados_e_recessos de %s" % ficha_esc
            else:
                feriados, aviso, fonte = set(), "sem a ficha do escritório e sem --feriados: só sábado e domingo passam para o próximo dia útil", ""
    except ValueError as erro:
        print("ERRO: %s" % erro)
        return 1
    if feriados:
        origem_feriados += ", e os feriados %s (%s)" % (", ".join(d.isoformat() for d in sorted(feriados)), fonte)
    if aviso:
        origem_feriados += ". AVISO: %s" % aviso

    grupos = classificar(registros, hoje, regua, maximo, dias_para_decidir, "primeira_resposta" not in faltando,
                         feriados)
    if "--json" in argv:
        em_json(grupos, hoje, len(registros), origem, origem_feriados)
    else:
        imprimir(grupos, hoje, len(registros), origem, regua, maximo, faltando, origem_feriados)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
