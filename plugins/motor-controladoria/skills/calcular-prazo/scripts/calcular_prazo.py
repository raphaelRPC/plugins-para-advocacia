#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calcular_prazo.py · a conta do prazo processual, passo a passo, pelo calendário do tribunal.

A IA capta e calcula, mas não interpreta: este script só conta. O número de dias vem do ato
publicado (--dias) ou da tabela de prazos por ato do escritório (--ato com --regras). Quem
confirma o prazo é uma pessoa, na dupla conferência.

Uso (uma conta):
  python3 calcular_prazo.py --disponibilizacao AAAA-MM-DD | --ciencia AAAA-MM-DD | --envio-portal AAAA-MM-DD
      --dias N | --ato "<ato>" --regras <regras-de-contagem.md>
      --rito civel|trabalhista|juizado-civel|juizado-federal|penal|outro
      --tribunal SIGLA --calendario <arquivo ou pasta>
      [--contagem uteis|corridos] [--dobro [CHAVE]] [--seguranca N] [--json]
      [--duplo] [--recesso-penal] [--domicilio] [--cidade NOME] [--hoje AAAA-MM-DD]
      [--sem-calendario] [--prazo-material]

Uso (um lote):
  python3 calcular_prazo.py --csv prazos.csv --publicacoes publicacoes.csv
      --calendario <pasta> --regras <arquivo> [--seguranca N] [--gravar] [--saida relatorio.md]

Códigos de saída: 0 conta feita; 1 erro ou recusa (prazo material, falta de dias, falta de
calendário, arquivo ou coluna que falta); 2 as duas contas independentes não bateram, ou o lote
tem linhas que divergem do registro.

Só biblioteca padrão. Python 3.9 ou mais novo.
"""

import argparse
import bisect
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import sys
import unicodedata

UM_DIA = dt.timedelta(days=1)
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

TIPOS = (
    "feriado",
    "recesso",
    "suspensao",
    "expediente-reduzido",
    "indisponibilidade-programada",
    "indisponibilidade-certificada",
)
RITOS = ("civel", "trabalhista", "juizado-civel", "juizado-federal", "penal", "outro")
CHAVES_DOBRO = ("fazenda-dobro", "defensoria-dobro", "mp-dobro", "litisconsortes-dobro")

# Onde está cada regra, como em docs/contagem.md. Sempre [CONFERIR] até o escritório validar.
NORMAS = {
    "civel-cpc": "CPC, art. 219 e art. 224",
    "publicacao-diario": "CPC, art. 224, §§ 2º e 3º; Lei 11.419/2006, art. 4º",
    "intimacao-portal": "Lei 11.419/2006, art. 5º; CPC, art. 231",
    "domicilio-eletronico": "Resolução do CNJ sobre o Domicílio Judicial Eletrônico e CPC, art. 231",
    "recesso-forense": "CPC, art. 220",
    "trabalhista-clt": "CLT, art. 775",
    "recesso-trabalhista": "CLT, art. 775-A",
    "juizado-civel": "Lei 9.099/1995, art. 12-A",
    "juizado-federal": "Lei 10.259/2001 e Lei 9.099/1995, art. 12-A",
    "penal-cpp": "CPP, art. 798",
    "recesso-penal": "CPP, art. 798-A",
    "fazenda-dobro": "CPC, art. 183",
    "defensoria-dobro": "CPC, art. 186",
    "mp-dobro": "CPC, art. 180",
    "litisconsortes-dobro": "CPC, art. 229",
    "juizado-sem-dobro": "Lei 10.259/2001, art. 9º, e a jurisprudência do tribunal",
    "indisponibilidade": "Lei 11.419/2006, art. 10, § 2º; CPC, art. 224, § 1º",
    "expediente-reduzido": "CPC, art. 224, § 1º",
    "prazo-material": "Código Civil e lei própria",
}
CHAVE_DO_RITO = {
    "civel": "civel-cpc",
    "trabalhista": "trabalhista-clt",
    "juizado-civel": "juizado-civel",
    "juizado-federal": "juizado-federal",
    "penal": "penal-cpp",
    "outro": "civel-cpc",
}
RECESSO_DO_RITO = {
    "civel": "recesso-forense",
    "trabalhista": "recesso-trabalhista",
    "juizado-civel": "recesso-forense",
    "juizado-federal": "recesso-forense",
    "penal": "recesso-penal",
    "outro": "recesso-forense",
}
PRAZO_CIENCIA_PADRAO = 10  # docs/contagem.md, linha intimacao-portal
SEGURANCA_PADRAO = 2  # docs/ficha-da-controladoria-modelo.md, dias_de_seguranca
PALAVRAS_MATERIAL = (
    "decadencia",
    "decadencial",
    "prescricao",
    "prescricional",
    "prazo material",
    "direito material",
    "prazo de contrato",
    "prazo contratual",
)

# Justiça (J) e tribunal (TR) do número CNJ, para achar o tribunal quando nada mais diz.
UF_DO_TJ = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DFT", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SE", "SP", "TO",
]


class Erro(Exception):
    """Erro que encerra o script com código 1 e uma mensagem clara."""


# ---------------------------------------------------------------- utilidades


def sem_acento(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in texto if not unicodedata.combining(c))


def normal(texto):
    return re.sub(r"\s+", " ", sem_acento(texto).strip().lower())


def limpar_celula(texto):
    texto = texto.strip()
    texto = texto.replace("`", "").replace("**", "")
    return texto.strip()


def ler_data(texto, campo="data"):
    if texto is None:
        raise Erro("falta a %s." % campo)
    s = str(texto).strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        a, mes, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if not m:
            raise Erro("%s inválida: '%s'. Use AAAA-MM-DD ou DD/MM/AAAA." % (campo, s))
        d, mes, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return dt.date(a, mes, d)
    except ValueError:
        raise Erro("%s inexistente no calendário: '%s'." % (campo, s))


def fmt(d):
    return "%s (%s)" % (d.isoformat(), DIAS_SEMANA[d.weekday()])


def ler_texto(caminho):
    if not os.path.isfile(caminho):
        raise Erro("arquivo não encontrado: %s" % caminho)
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return bruto.decode("latin-1"), "latin-1"


def cabecalho_yaml(texto):
    """Lê o cabeçalho simples entre as duas primeiras linhas '---'."""
    linhas = texto.splitlines()
    meta = {}
    if not linhas or linhas[0].strip() != "---":
        return meta, 0
    for i in range(1, len(linhas)):
        linha = linhas[i]
        if linha.strip() == "---":
            return meta, i + 1
        m = re.match(r"\s*([A-Za-z0-9_\-]+)\s*:\s*(.*)$", linha)
        if m:
            valor = m.group(2).strip()
            valor = re.sub(r"\s+#.*$", "", valor) if not valor.startswith("[") else valor
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                valor = valor[1:-1]
            meta[m.group(1).strip().lower()] = valor.strip()
    return meta, 0


def tabelas_markdown(texto):
    """Devolve as tabelas do texto: lista de (numero_da_linha_do_cabecalho, cabecalho, linhas)."""
    linhas = texto.splitlines()
    tabelas = []
    i = 0
    while i < len(linhas):
        if linhas[i].strip().startswith("|"):
            bloco = []
            inicio = i
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append((i + 1, linhas[i]))
                i += 1
            celulas = []
            for num, linha in bloco:
                partes = linha.strip().strip("|").split("|")
                partes = [limpar_celula(p) for p in partes]
                if all(re.fullmatch(r":?-{2,}:?", p) or p == "" for p in partes):
                    continue
                celulas.append((num, partes))
            if celulas:
                cab = [normal(c) for c in celulas[0][1]]
                tabelas.append((inicio + 1, cab, celulas[1:]))
        else:
            i += 1
    return tabelas


def vazio_ou_pendente(valor):
    v = (valor or "").strip()
    return v == "" or "A PREENCHER" in v.upper() or "A DEFINIR" in v.upper() or "A CONFIRMAR" in v.upper()


# ---------------------------------------------------------------- calendário


def ler_calendario(caminho):
    texto, _ = ler_texto(caminho)
    meta, _ = cabecalho_yaml(texto)
    nome = os.path.basename(caminho)
    if "tribunal" not in meta:
        return None
    tribunais = [t.strip().upper() for t in re.split(r"[,;]", meta.get("tribunal", "")) if t.strip()]
    anos = [int(a) for a in re.findall(r"\d{4}", meta.get("ano", ""))]
    cobre_ate = None
    if meta.get("cobre_ate"):
        cobre_ate = ler_data(meta["cobre_ate"], "cobre_ate do calendário %s" % nome)
    linhas = []
    pendentes = []
    achou_tabela = False
    for _, cab, corpo in tabelas_markdown(texto):
        if "data" not in cab or "tipo" not in cab:
            continue
        achou_tabela = True
        faltam = [c for c in ("data", "tipo", "descricao", "vale_para", "fonte", "conferido_em") if c not in cab]
        if faltam:
            raise Erro(
                "calendário %s: faltam as colunas %s. As colunas são: data | tipo | descricao | vale_para | fonte | conferido_em."
                % (nome, ", ".join(faltam))
            )
        idx = {c: cab.index(c) for c in cab}
        for num, partes in corpo:
            partes = partes + [""] * (len(cab) - len(partes))
            celula = lambda c: partes[idx[c]].strip()
            data_txt = celula("data")
            if "A PREENCHER" in data_txt.upper() or "A DEFINIR" in data_txt.upper():
                pendentes.append("%s (linha %d)" % (celula("descricao") or "sem descrição", num))
                continue
            m = re.fullmatch(
                r"(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4})(?:\s+a\s+(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4}))?",
                data_txt,
            )
            if not m:
                raise Erro(
                    "calendário %s, linha %d: data '%s' fora do formato (AAAA-MM-DD ou AAAA-MM-DD a AAAA-MM-DD)."
                    % (nome, num, data_txt)
                )
            ini = ler_data(m.group(1), "data do calendário %s, linha %d" % (nome, num))
            fim = ler_data(m.group(2), "data do calendário %s, linha %d" % (nome, num)) if m.group(2) else ini
            if fim < ini:
                raise Erro("calendário %s, linha %d: o período termina antes de começar." % (nome, num))
            tipo = normal(celula("tipo")).replace(" ", "-")
            if tipo not in TIPOS:
                raise Erro(
                    "calendário %s, linha %d: tipo '%s' desconhecido. Use: %s."
                    % (nome, num, celula("tipo"), ", ".join(TIPOS))
                )
            vale_txt = celula("vale_para")
            if vale_txt == "":
                raise Erro("calendário %s, linha %d: vale_para vazio (use 'todos' ou as siglas)." % (nome, num))
            if normal(vale_txt) == "todos":
                vale = None
            else:
                vale = set(v.strip().upper() for v in re.split(r"[,;]", vale_txt) if v.strip())
            linhas.append(
                {
                    "ini": ini,
                    "fim": fim,
                    "tipo": tipo,
                    "descricao": celula("descricao"),
                    "vale_para": vale,
                    "fonte": celula("fonte"),
                    "conferido_em": celula("conferido_em"),
                    "arquivo": nome,
                    "linha": num,
                }
            )
    if not achou_tabela:
        raise Erro("calendário %s: não achei a tabela com as colunas data e tipo." % nome)
    return {
        "arquivo": nome,
        "caminho": caminho,
        "meta": meta,
        "tribunais": tribunais,
        "anos": anos,
        "cobre_ate": cobre_ate,
        "cidade": "" if vazio_ou_pendente(meta.get("cidade", "")) else normal(meta.get("cidade", "")),
        "linhas": linhas,
        "pendentes": pendentes,
    }


def carregar_calendarios(caminho):
    if caminho is None:
        return [], []
    if not os.path.exists(caminho):
        raise Erro("calendário não encontrado: %s" % caminho)
    avisos = []
    arquivos = []
    if os.path.isdir(caminho):
        for nome in sorted(os.listdir(caminho)):
            if nome.lower().endswith(".md"):
                arquivos.append(os.path.join(caminho, nome))
        if not arquivos:
            raise Erro("a pasta de calendários %s não tem nenhum arquivo .md." % caminho)
    else:
        arquivos = [caminho]
    cals = []
    for arq in arquivos:
        c = ler_calendario(arq)
        if c is None:
            avisos.append("arquivo %s ignorado: sem 'tribunal' no cabeçalho." % os.path.basename(arq))
            continue
        cals.append(c)
    return cals, avisos


def selecionar_calendario(cals, tribunal, cidade, sem_calendario):
    """Escolhe os calendários e as linhas que valem para o tribunal."""
    t = tribunal.upper()
    avisos = []
    proprios = [c for c in cals if t in c["tribunais"]]
    gerais = [c for c in cals if "TODOS" in c["tribunais"] and t not in c["tribunais"]]
    if not proprios:
        if not sem_calendario:
            raise Erro(
                "sem calendário para o tribunal %s. Monte o calendário do ano na calendario-forense, "
                "ou rode com --sem-calendario (só pula fins de semana, e a data pode sair errada)." % t
            )
        avisos.append(
            "ATENÇÃO: SEM CALENDÁRIO PARA O TRIBUNAL %s. A conta pulou só fins de semana%s. "
            "Feriados, recesso e suspensões não foram considerados. Não use esta data sem conferir no calendário do tribunal."
            % (t, " e as linhas gerais" if gerais else "")
        )
    cidades = set(c["cidade"] for c in proprios if c["cidade"])
    if cidade:
        cid = normal(cidade)
        outros = [c for c in proprios if c["cidade"] and c["cidade"] != cid]
        proprios = [c for c in proprios if not c["cidade"] or c["cidade"] == cid]
        if not proprios and outros and not sem_calendario:
            raise Erro(
                "não há calendário de %s para a cidade '%s' (há para: %s). Feriado municipal de outra cidade "
                "mudaria a conta: monte o calendário dessa cidade na calendario-forense." % (t, cidade, ", ".join(sorted(cidades)))
            )
    elif len(cidades) > 1:
        raise Erro(
            "há calendários de %s para mais de uma cidade (%s). Diga a cidade do juízo com --cidade, "
            "para não misturar feriados municipais." % (t, ", ".join(sorted(cidades)))
        )
    escolhidos = proprios + gerais
    linhas = []
    for c in escolhidos:
        for l in c["linhas"]:
            if l["vale_para"] is None or t in l["vale_para"]:
                linhas.append(l)
    cobertura = []
    for c in proprios:
        for a in c["anos"]:
            cobertura.append((dt.date(a, 1, 1), dt.date(a, 12, 31)))
        if c["cobre_ate"] and c["anos"]:
            cobertura.append((dt.date(min(c["anos"]), 1, 1), c["cobre_ate"]))
    for c in escolhidos:
        m = c["meta"]
        if normal(m.get("treino", "")) == "sim":
            avisos.append("calendário de treino (%s): vale só para os casos fictícios." % c["arquivo"])
        elif vazio_ou_pendente(m.get("conferido_por")) or vazio_ou_pendente(m.get("conferido_em")):
            avisos.append("calendário não conferido: %s (sem conferido_por ou conferido_em no cabeçalho)." % c["arquivo"])
        if c["pendentes"]:
            avisos.append(
                "DÚVIDA DO CALENDÁRIO: %s tem linhas sem data (%s). Esses dias não entraram na conta: se algum cair dentro do prazo, "
                "a data real fica mais tarde, e a conta ficou com a mais cedo. Conferir no ato do tribunal e preencher a data."
                % (c["arquivo"], "; ".join(c["pendentes"]))
            )
    return {"linhas": linhas, "arquivos": [c["arquivo"] for c in escolhidos], "cobertura": cobertura, "avisos": avisos}


# ---------------------------------------------------------------- regras do escritório


def ler_regras(caminho):
    texto, _ = ler_texto(caminho)
    meta, _ = cabecalho_yaml(texto)
    nome = os.path.basename(caminho)
    chaves = {}
    atos = []
    for _, cab, corpo in tabelas_markdown(texto):
        if cab and cab[0] == "chave":
            col_onde = None
            for i, c in enumerate(cab):
                if c.startswith("onde"):
                    col_onde = i
            for num, partes in corpo:
                chave = normal(partes[0]).replace(" ", "-")
                if not chave:
                    continue
                chaves[chave] = {
                    "linha": " | ".join(partes),
                    "onde": partes[col_onde].strip() if col_onde is not None and col_onde < len(partes) else "",
                    "como": partes[-1].strip(),
                }
        elif "ato" in cab and "dias" in cab and "rito" in cab:
            idx = {c: cab.index(c) for c in cab}
            for num, partes in corpo:
                partes = partes + [""] * (len(cab) - len(partes))
                atos.append(
                    {
                        "ato": partes[idx["ato"]].strip(),
                        "rito": normal(partes[idx["rito"]]).replace(" ", "-"),
                        "dias": partes[idx["dias"]].strip(),
                        "contagem": normal(partes[idx["contagem"]]) if "contagem" in idx else "",
                        "fonte": partes[idx["fonte"]].strip() if "fonte" in idx else "",
                        "linha": num,
                    }
                )
    if not chaves:
        raise Erro("tabela de regras %s: não achei a tabela com a coluna 'Chave' primeiro." % nome)
    return {"arquivo": nome, "meta": meta, "chaves": chaves, "atos": atos}


def prazo_de_ciencia(regras, avisos):
    if regras is None:
        return PRAZO_CIENCIA_PADRAO
    item = regras["chaves"].get("intimacao-portal")
    if item:
        m = re.search(r"(\d+)\s*dias\s*corridos", item["como"]) or re.search(r"(\d+)\s*dias\s*corridos", item["linha"])
        if m:
            return int(m.group(1))
    avisos.append(
        "a tabela de regras não diz o prazo de ciência da intimacao-portal: usei %d dias corridos (docs/contagem.md)."
        % PRAZO_CIENCIA_PADRAO
    )
    return PRAZO_CIENCIA_PADRAO


def eh_prazo_material(texto):
    t = normal(texto or "")
    return any(p in t for p in PALAVRAS_MATERIAL)


def achar_ato(regras, ato, rito):
    alvo = normal(ato)
    achados = [a for a in regras["atos"] if normal(a["ato"]) == alvo]
    if not achados:
        raise Erro(
            "o ato '%s' não está na tabela de prazos por ato (%s). O número de dias nunca vem da memória: "
            "informe --dias N com a fonte (o próprio ato) ou acrescente a linha na tabela do escritório (calendario-forense)."
            % (ato, regras["arquivo"])
        )
    do_rito = [a for a in achados if a["rito"] in (rito, "todos")]
    if not do_rito:
        raise Erro(
            "o ato '%s' está na tabela só para o rito %s, e a conta pediu o rito %s. Confirme o rito ou informe --dias N com a fonte."
            % (ato, ", ".join(sorted(set(a["rito"] for a in achados))), rito)
        )
    a = do_rito[0]
    if not re.fullmatch(r"\d+", a["dias"]):
        raise Erro(
            "a tabela de prazos por ato não traz o número de dias de '%s' (%s): [A CONFIRMAR: quantos dias]. A pessoa informa."
            % (ato, a["dias"] or "vazio")
        )
    return a


# ---------------------------------------------------------------- conta 1: dia a dia


class DiasDiaADia:
    """Classifica um dia por vez, varrendo as linhas do calendário (conta 1)."""

    def __init__(self, linhas, aplica_recesso):
        self.linhas = linhas
        self.aplica_recesso = aplica_recesso
        self.usadas = []

    def do_dia(self, d):
        return [l for l in self.linhas if l["ini"] <= d <= l["fim"]]

    def tem(self, d, tipo):
        return any(l["tipo"] == tipo for l in self.do_dia(d))

    def usar(self, d, tipos):
        for l in self.do_dia(d):
            if l["tipo"] in tipos and l not in self.usadas:
                self.usadas.append(l)

    def fim_de_semana(self, d):
        return d.weekday() >= 5

    def com_expediente(self, d):
        return not self.fim_de_semana(d) and not self.tem(d, "feriado")

    def suspenso(self, d):
        return self.tem(d, "suspensao") or (self.aplica_recesso and self.tem(d, "recesso"))

    def util(self, d):
        return self.com_expediente(d) and not self.suspenso(d)

    def motivo(self, d):
        partes = []
        if self.fim_de_semana(d):
            partes.append("fim de semana")
        for l in self.do_dia(d):
            if l["tipo"] == "feriado":
                partes.append("feriado: %s (%s)" % (l["descricao"], l["arquivo"]))
            elif l["tipo"] == "suspensao":
                partes.append("suspensão de prazos: %s (%s)" % (l["descricao"], l["arquivo"]))
            elif l["tipo"] == "recesso" and self.aplica_recesso:
                partes.append("recesso, prazos suspensos: %s (%s)" % (l["descricao"], l["arquivo"]))
        self.usar(d, ("feriado", "suspensao", "recesso") if self.aplica_recesso else ("feriado", "suspensao"))
        return "; ".join(partes) or "sem expediente"


def conta_dia_a_dia(ref, n, contagem, seguranca, D):
    """Conta a partir do dia de referência (excluído): a publicação ou a ciência."""
    pulados = []
    contados = []
    chaves_extra = []
    d = ref + UM_DIA
    if contagem == "uteis":
        while True:
            if not D.util(d):
                pulados.append((d, D.motivo(d)))
                d += UM_DIA
                continue
            if D.tem(d, "expediente-reduzido"):
                D.usar(d, ("expediente-reduzido",))
                pulados.append((d, "expediente reduzido no dia do começo: o início vai para o dia útil seguinte (expediente-reduzido)"))
                if "expediente-reduzido" not in chaves_extra:
                    chaves_extra.append("expediente-reduzido")
                d += UM_DIA
                continue
            break
        inicio = d
        k = 1
        contados.append((k, d))
        while k < n:
            d += UM_DIA
            if D.util(d):
                k += 1
                contados.append((k, d))
            else:
                pulados.append((d, D.motivo(d)))
    else:
        while D.suspenso(d):
            pulados.append((d, D.motivo(d)))
            d += UM_DIA
        inicio = d
        k = 1
        contados.append((k, d))
        while k < n:
            d += UM_DIA
            if D.suspenso(d):
                pulados.append((d, D.motivo(d)))
            else:
                k += 1
                contados.append((k, d))
    vencimento_contado = d
    empurrado = []
    while True:
        if not D.util(d):
            empurrado.append((d, D.motivo(d)))
            d += UM_DIA
            continue
        if D.tem(d, "expediente-reduzido"):
            D.usar(d, ("expediente-reduzido",))
            empurrado.append((d, "expediente reduzido no dia do vencimento (expediente-reduzido)"))
            if "expediente-reduzido" not in chaves_extra:
                chaves_extra.append("expediente-reduzido")
            d += UM_DIA
            continue
        if D.tem(d, "indisponibilidade-certificada"):
            D.usar(d, ("indisponibilidade-certificada",))
            empurrado.append((d, "indisponibilidade certificada pelo tribunal no dia do vencimento (indisponibilidade)"))
            if "indisponibilidade" not in chaves_extra:
                chaves_extra.append("indisponibilidade")
            d += UM_DIA
            continue
        break
    vencimento = d
    s = vencimento
    k = 0
    while k < seguranca:
        s -= UM_DIA
        if D.util(s):
            k += 1
    return {
        "inicio": inicio,
        "vencimento": vencimento,
        "vencimento_contado": vencimento_contado,
        "data_seguranca": s,
        "contados": contados,
        "pulados": pulados,
        "empurrado": empurrado,
        "chaves_extra": chaves_extra,
    }


def partida_dia_a_dia(modo, data, prazo_ciencia, D):
    """Devolve as leituras do ponto de partida: [(rotulo, referencia, passos)]."""
    if modo == "disponibilizacao":
        pulados = []
        d = data + UM_DIA
        while not D.com_expediente(d):
            pulados.append((d, D.motivo(d)))
            d += UM_DIA
        return [("unica", d, {"disponibilizacao": data, "publicacao": d, "pulados_publicacao": pulados})]
    if modo == "envio-portal":
        ciencia = data + dt.timedelta(days=prazo_ciencia)
    else:
        ciencia = data
    base = {"envio": data if modo == "envio-portal" else None, "ciencia_calculada": ciencia}
    if D.com_expediente(ciencia):
        return [("unica", ciencia, dict(base, ciencia=ciencia))]
    motivo = D.motivo(ciencia)
    d = ciencia + UM_DIA
    while not D.com_expediente(d):
        d += UM_DIA
    return [
        ("a", ciencia, dict(base, ciencia=ciencia, motivo_ciencia=motivo)),
        ("b", d, dict(base, ciencia=d, motivo_ciencia=motivo)),
    ]


# ---------------------------------------------------------------- conta 2: lista de dias úteis


class ListaDeDias:
    """Monta, de uma vez, as listas de dias do período e indexa nelas (conta 2)."""

    def __init__(self, linhas, aplica_recesso):
        self.mapa = {}
        for l in linhas:
            for o in range(l["ini"].toordinal(), l["fim"].toordinal() + 1):
                self.mapa.setdefault(o, set()).add(l["tipo"])
        self.aplica_recesso = aplica_recesso

    @staticmethod
    def _fds(o):
        # dt.date(1, 1, 1) tem ordinal 1 e é segunda-feira: resto 6 é sábado, 0 é domingo.
        return o % 7 in (6, 0)

    def montar(self, de, ate):
        exp, uteis, corridos, venc_ok, reduzidos = [], [], [], [], set()
        for o in range(de, ate + 1):
            t = self.mapa.get(o, ())
            sem_exp = self._fds(o) or ("feriado" in t)
            susp = ("suspensao" in t) or (self.aplica_recesso and "recesso" in t)
            if not sem_exp:
                exp.append(o)
            if not susp:
                corridos.append(o)
            if not sem_exp and not susp:
                uteis.append(o)
                if "expediente-reduzido" in t:
                    reduzidos.add(o)
                if "expediente-reduzido" not in t and "indisponibilidade-certificada" not in t:
                    venc_ok.append(o)
        return exp, uteis, corridos, venc_ok, reduzidos


def conta_pela_lista(modo, data, n, contagem, seguranca, prazo_ciencia, L):
    janela = max(800, n * 3 + 500)
    for _ in range(6):
        try:
            return _conta_pela_lista(modo, data, n, contagem, seguranca, prazo_ciencia, L, janela)
        except IndexError:
            janela *= 2
    raise Erro("a conta 2 não achou o vencimento dentro de %d dias: confira o calendário." % janela)


def _conta_pela_lista(modo, data, n, contagem, seguranca, prazo_ciencia, L, janela):
    base = data.toordinal()
    exp, uteis, corridos, venc_ok, reduzidos = L.montar(base - 40, base + janela)
    exp_set = set(exp)
    leituras = []
    if modo == "disponibilizacao":
        pub = exp[bisect.bisect_right(exp, base)]
        leituras.append(("unica", pub))
    else:
        c = base + (prazo_ciencia if modo == "envio-portal" else 0)
        if c in exp_set:
            leituras.append(("unica", c))
        else:
            leituras.append(("a", c))
            leituras.append(("b", exp[bisect.bisect_right(exp, c)]))
    saida = []
    for rotulo, ref in leituras:
        if contagem == "uteis":
            i = bisect.bisect_right(uteis, ref)
            while uteis[i] in reduzidos:
                i += 1
            ini = uteis[i]
            v0 = uteis[i + n - 1]
        else:
            i = bisect.bisect_right(corridos, ref)
            ini = corridos[i]
            v0 = corridos[i + n - 1]
        venc = venc_ok[bisect.bisect_left(venc_ok, v0)]
        k = bisect.bisect_left(uteis, venc)
        if k - seguranca < 0:
            raise IndexError
        seg = uteis[k - seguranca]
        saida.append(
            {
                "leitura": rotulo,
                "referencia": dt.date.fromordinal(ref),
                "inicio": dt.date.fromordinal(ini),
                "vencimento": dt.date.fromordinal(venc),
                "data_seguranca": dt.date.fromordinal(seg),
            }
        )
    return saida


# ---------------------------------------------------------------- a conta completa


def coberto(d, cobertura):
    return any(a <= d <= b for a, b in cobertura)


def proximo_util_depois(d, D):
    x = d + UM_DIA
    while not D.util(x):
        x += UM_DIA
    return x


def linha_nao_conferida(l):
    """Linha do calendário que ainda não foi conferida no ato do tribunal."""
    return vazio_ou_pendente(l["conferido_em"]) or not l["fonte"] or "CONFERIR" in (l["fonte"] + l["descricao"]).upper()


def pessoa_agora_de(p, linhas, aplica_recesso, venc_final, seg_final, escolhida):
    hoje = p["hoje"]
    D_hoje = DiasDiaADia(linhas, aplica_recesso)
    amanha = max(hoje + UM_DIA, proximo_util_depois(hoje, D_hoje))
    pessoa_agora = None
    if venc_final < hoje:
        pessoa_agora = "VENCIDO: o vencimento (%s) já passou. PESSOA AGORA." % venc_final.isoformat()
    elif venc_final <= amanha or seg_final <= amanha:
        pessoa_agora = "PESSOA AGORA: vence hoje ou amanhã (segurança %s, fatal %s)." % (seg_final.isoformat(), venc_final.isoformat())
    if p["modo"] == "envio-portal":
        dois = hoje
        k = 0
        while k < 2:
            dois = proximo_util_depois(dois, D_hoje)
            k += 1
        ciencia_esc = escolhida["ciencia"]
        if hoje <= ciencia_esc <= dois:
            texto = "ciência tácita em até 2 dias úteis (%s)." % ciencia_esc.isoformat()
            pessoa_agora = (pessoa_agora + " Também: " + texto) if pessoa_agora else "PESSOA AGORA: " + texto
    return pessoa_agora


def calcular(p, cal, regras):
    """A conta com as duas leituras do calendário quando há linha não conferida (contagem.md, regra de ouro 3).

    Leitura com todas as linhas e leitura sem as linhas ainda não conferidas. Se mudam o resultado,
    fica a mais cedo (vencimento e data de segurança, cada uma pela mais cedo) e a dúvida vai em destaque.
    """
    r_todas = _calcular_base(p, cal, regras)
    duvidosas = [l for l in cal["linhas"] if linha_nao_conferida(l)]
    if not duvidosas:
        return r_todas
    cal_sem = dict(cal, linhas=[l for l in cal["linhas"] if not linha_nao_conferida(l)])
    r_sem = _calcular_base(p, cal_sem, regras)

    def datas(r):
        e = r["escolhida"]
        return (e.get("publicacao") or e.get("ciencia"), e["inicio"], r["vencimento"], r["data_seguranca"])

    if datas(r_todas) == datas(r_sem):
        return r_todas
    base = r_sem if (r_sem["vencimento"], r_sem["data_seguranca"]) <= (r_todas["vencimento"], r_todas["data_seguranca"]) else r_todas
    outra = r_todas if base is r_sem else r_sem
    venc = min(r_todas["vencimento"], r_sem["vencimento"])
    seg = min(r_todas["data_seguranca"], r_sem["data_seguranca"])
    fim = max(r_todas["vencimento"], r_sem["vencimento"])
    no_periodo = [l for l in duvidosas if l["ini"] <= fim and l["fim"] >= p["data"]] or duvidosas
    quais = "; ".join(
        "%s%s (%s, %s linha %d)"
        % (l["ini"].isoformat(), "" if l["fim"] == l["ini"] else " a " + l["fim"].isoformat(), l["descricao"], l["arquivo"], l["linha"])
        for l in no_periodo
    )
    duvida = (
        "DÚVIDA DO CALENDÁRIO: %s não conferida no ato do tribunal. Ficou a leitura mais cedo: vencimento %s, segurança %s. "
        "A outra leitura (%s esse dia) daria vencimento %s, segurança %s. Conferir no ato do tribunal e refazer a conta."
        % (
            quais,
            venc.isoformat(),
            seg.isoformat(),
            "contando" if outra is r_todas else "sem contar",
            outra["vencimento"].isoformat(),
            outra["data_seguranca"].isoformat(),
        )
    )
    r = dict(base)
    r["vencimento"] = venc
    r["data_seguranca"] = seg
    r["batem"] = r_todas["batem"] and r_sem["batem"]
    r["leitura_calendario"] = {
        "contando_nao_conferidas": {"vencimento": r_todas["vencimento"], "data_seguranca": r_todas["data_seguranca"]},
        "sem_contar_nao_conferidas": {"vencimento": r_sem["vencimento"], "data_seguranca": r_sem["data_seguranca"]},
    }
    avisos = [duvida]
    for a in base["avisos"] + [x for x in outra["avisos"] if x.startswith("linha do calendário usada")]:
        if a not in avisos:
            avisos.append(a)
    if not outra["batem"] and base["batem"]:
        avisos.insert(1, "AS DUAS CONTAS NÃO BATEM na outra leitura do calendário: confira o calendário e os dados.")
    r["avisos"] = avisos
    r["duvidas"] = [a for a in avisos if a.startswith("DÚVIDA")]
    r["dias_em_duvida"] = sorted(set(
        l["ini"] + dt.timedelta(days=k) for l in no_periodo for k in range((l["fim"] - l["ini"]).days + 1)))
    r["pessoa_agora"] = pessoa_agora_de(p, cal["linhas"], base["aplica_recesso"], venc, seg, base["escolhida"])
    return r


def _calcular_base(p, cal, regras):
    """p: dicionário com modo, data, dias, ato, rito, tribunal, contagem, dobro, seguranca, hoje, flags."""
    avisos = list(cal["avisos"])
    rito = p["rito"]
    if rito not in RITOS:
        raise Erro("rito '%s' desconhecido. Use: %s." % (rito, ", ".join(RITOS)))

    # prazo material: o script não calcula
    if p.get("prazo_material") or eh_prazo_material(p.get("ato")):
        raise Erro(
            "prazo de direito material (prazo-material: %s [CONFERIR]). O script não calcula decadência, prescrição "
            "nem prazo de contrato: a pessoa informa a data, que entra em prazos.csv com a observação de onde ela veio."
            % NORMAS["prazo-material"]
        )

    # de onde vêm os dias
    origem_dias = None
    contagem_tabela = ""
    n_ato = None
    if p.get("ato"):
        if regras is None:
            raise Erro("--ato precisa de --regras (a tabela de prazos por ato do escritório).")
        a = achar_ato(regras, p["ato"], rito)
        n_ato = int(a["dias"])
        contagem_tabela = "corridos" if "corrid" in a["contagem"] else ("uteis" if "uteis" in a["contagem"] else "")
        origem_dias = "tabela do escritório (%s, linha %d): %s · %s · %s dias · fonte: %s" % (
            regras["arquivo"],
            a["linha"],
            a["ato"],
            a["rito"],
            a["dias"],
            a["fonte"] or "sem fonte [CONFERIR]",
        )
        if not a["fonte"] or "CONFERIR" in a["fonte"].upper():
            avisos.append("a linha do ato '%s' na tabela do escritório está sem fonte conferida." % a["ato"])
    n = p.get("dias")
    if n is not None and n_ato is not None and n != n_ato:
        avisos.append(
            "DÚVIDA NO NÚMERO DE DIAS: --dias %d e a tabela do escritório diz %d para '%s'. Usei o menor (%d), "
            "que dá a data mais cedo. A pessoa decide." % (n, n_ato, p["ato"], min(n, n_ato))
        )
        n = min(n, n_ato)
        origem_dias = "o menor entre o informado (%d) e a tabela (%d)" % (p["dias"], n_ato)
    elif n is None:
        n = n_ato
    elif origem_dias is None:
        origem_dias = "informado (--dias %d): o próprio ato publicado ou a pessoa; confira com o trecho literal" % n
    if n is None:
        raise Erro(
            "falta o número de dias. Ele vem do próprio ato (--dias N) ou da tabela de prazos por ato do escritório "
            "(--ato \"<ato>\" --regras <arquivo>). Sem um dos dois: [A CONFIRMAR: quantos dias], para a pessoa."
        )
    if n <= 0:
        raise Erro("número de dias inválido: %d." % n)

    # contagem
    if p.get("contagem"):
        contagem = p["contagem"]
        if contagem_tabela and contagem_tabela != contagem:
            avisos.append("--contagem %s diferente da tabela do escritório (%s): usei a informada; confira." % (contagem, contagem_tabela))
    elif contagem_tabela:
        contagem = contagem_tabela
    else:
        contagem = "corridos" if rito == "penal" else "uteis"
    if rito == "penal" and contagem == "uteis":
        avisos.append("rito penal com contagem em dias úteis: a regra penal-cpp conta em dias corridos. Confira.")
    if rito == "outro":
        avisos.append("rito 'outro': usei a contagem do civel-cpc (dias úteis). Confirme a regra do rito com a pessoa.")

    # prazo em dobro: só dobra, quem decide é a pessoa
    chave_dobro = None
    if p.get("dobro"):
        chave_dobro = p["dobro"] if p["dobro"] in CHAVES_DOBRO else None
        n_base = n
        n = n * 2
        avisos.append(
            "PRAZO EM DOBRO aplicado por decisão da pessoa (%d x 2 = %d dias)%s. O script não decide se cabe."
            % (n_base, n, " pela regra %s" % chave_dobro if chave_dobro else "")
        )
        if rito in ("juizado-civel", "juizado-federal"):
            avisos.append(
                "juizado-sem-dobro (%s [CONFERIR]): nos juizados a regra do dobro tem limites próprios. "
                "Não dobre sem a confirmação expressa da pessoa." % NORMAS["juizado-sem-dobro"]
            )
        if chave_dobro == "litisconsortes-dobro":
            avisos.append("litisconsortes-dobro: em processo eletrônico não dobra. Confira se os autos são físicos.")
        if chave_dobro is None:
            avisos.append("diga qual regra do dobro a pessoa confirmou (--dobro fazenda-dobro, defensoria-dobro, mp-dobro ou litisconsortes-dobro).")

    seguranca = p.get("seguranca")
    if seguranca is None:
        seguranca = SEGURANCA_PADRAO
        avisos.append("dias de segurança não informados: usei %d dias úteis (padrão da ficha). Confira dias_de_seguranca na ficha." % seguranca)

    aplica_recesso = rito != "penal" or bool(p.get("recesso_penal"))
    modo = p["modo"]
    prazo_ciencia = prazo_de_ciencia(regras, avisos) if modo == "envio-portal" else None

    # conta 1 e conta 2
    D = DiasDiaADia(cal["linhas"], aplica_recesso)
    leituras_1 = []
    for rotulo, ref, passos in partida_dia_a_dia(modo, p["data"], prazo_ciencia, D):
        r = conta_dia_a_dia(ref, n, contagem, seguranca, D)
        r.update(passos)
        r["leitura"] = rotulo
        r["referencia"] = ref
        leituras_1.append(r)
    L = ListaDeDias(cal["linhas"], aplica_recesso)
    leituras_2 = conta_pela_lista(modo, p["data"], n, contagem, seguranca, prazo_ciencia, L)

    batem = len(leituras_1) == len(leituras_2) and all(
        a["referencia"] == b["referencia"]
        and a["inicio"] == b["inicio"]
        and a["vencimento"] == b["vencimento"]
        and a["data_seguranca"] == b["data_seguranca"]
        for a, b in zip(leituras_1, leituras_2)
    )

    escolhida = min(leituras_1, key=lambda r: r["vencimento"])
    outra = [r for r in leituras_1 if r is not escolhida]
    venc_final = escolhida["vencimento"]
    seg_final = escolhida["data_seguranca"]
    if not batem:
        menor = min([r["vencimento"] for r in leituras_1] + [r["vencimento"] for r in leituras_2])
        if menor < venc_final:
            venc_final = menor
            seg_final = min([r["data_seguranca"] for r in leituras_1] + [r["data_seguranca"] for r in leituras_2])
        avisos.insert(
            0,
            "AS DUAS CONTAS NÃO BATEM. Vale a data mais cedo (%s) até a pessoa decidir. Confira o calendário e os dados."
            % venc_final.isoformat(),
        )

    # chaves de regra
    chaves = []
    if modo == "disponibilizacao":
        chaves.append("publicacao-diario")
    elif modo == "envio-portal":
        chaves.append("intimacao-portal")
    elif p.get("domicilio"):
        chaves.append("domicilio-eletronico")
    chaves.append(CHAVE_DO_RITO[rito])
    recesso_usado = any(l["tipo"] == "recesso" for l in D.usadas)
    suspensao_usada = any(l["tipo"] == "suspensao" for l in D.usadas)
    if recesso_usado:
        chaves.append(RECESSO_DO_RITO[rito])
    for c in escolhida["chaves_extra"]:
        if c not in chaves:
            chaves.append(c)
    if chave_dobro:
        chaves.append(chave_dobro)

    # avisos sobre o calendário e a regra
    if regras is None:
        avisos.append("sem a tabela de regras do escritório (--regras): regra ainda não validada pelo escritório.")
    else:
        m = regras["meta"]
        if normal(m.get("treino", "")) == "sim":
            avisos.append("regras de treino (%s): valem só para os casos fictícios." % regras["arquivo"])
        elif vazio_ou_pendente(m.get("validada_por")) or vazio_ou_pendente(m.get("validada_em")):
            avisos.append("regra ainda não validada pelo escritório (%s sem validada_por ou validada_em)." % regras["arquivo"])
        else:
            try:
                v = ler_data(m.get("validada_em"), "validada_em")
                if (p["hoje"] - v).days > 366:
                    avisos.append("a tabela de regras foi validada há mais de um ano (%s): conferir de novo." % v.isoformat())
            except Erro:
                avisos.append("validada_em da tabela de regras fora do formato AAAA-MM-DD.")
        for c in chaves:
            if c not in regras["chaves"]:
                avisos.append("a chave %s não está na tabela de regras do escritório: confira." % c)

    inicio_periodo = min(p["data"], escolhida["referencia"])
    fim_periodo = max(r["vencimento"] for r in leituras_1)
    if cal["cobertura"]:
        d = inicio_periodo
        fora = []
        while d <= fim_periodo:
            if not coberto(d, cal["cobertura"]):
                fora.append(d)
            d += UM_DIA
        if fora:
            avisos.append(
                "ATENÇÃO: o calendário de %s não cobre de %s a %s. Nesses dias só os fins de semana foram pulados, "
                "e a data pode sair mais cedo que a real. Monte o calendário que falta (calendario-forense)."
                % (p["tribunal"], fora[0].isoformat(), fora[-1].isoformat())
            )
    # recesso que o calendário não marca
    if rito != "penal" or p.get("recesso_penal"):
        d = escolhida["referencia"]
        sem_marca = []
        while d <= fim_periodo:
            no_periodo = (d.month == 12 and d.day >= 20) or (d.month == 1 and d.day <= 20)
            if no_periodo and not any(l["tipo"] == "recesso" and l["ini"] <= d <= l["fim"] for l in cal["linhas"]):
                sem_marca.append(d)
            d += UM_DIA
        if sem_marca:
            avisos.append(
                "o calendário não marca o recesso entre %s e %s: a conta não suspendeu os prazos nesses dias. Confira o calendário."
                % (sem_marca[0].isoformat(), sem_marca[-1].isoformat())
            )
    if rito == "penal" and not p.get("recesso_penal"):
        d = escolhida["referencia"]
        while d <= fim_periodo:
            if any(l["tipo"] == "recesso" and l["ini"] <= d <= l["fim"] for l in cal["linhas"]):
                avisos.append(
                    "recesso-penal (%s [CONFERIR]): a conta não suspendeu no recesso, porque há exceções (réu preso, medidas urgentes). "
                    "Se a pessoa confirmar que a exceção não se aplica, rode de novo com --recesso-penal." % NORMAS["recesso-penal"]
                )
                break
            d += UM_DIA
    if contagem == "corridos" and (recesso_usado or suspensao_usada):
        avisos.append(
            "na contagem corrida, a conta voltou a correr no dia seguinte ao fim da suspensão. Se o escritório entende que "
            "volta no primeiro dia útil, a data fica mais tarde; vale a mais cedo até a pessoa decidir."
        )
    # indisponibilidades
    for l in cal["linhas"]:
        if l["tipo"] == "indisponibilidade-programada" and l["ini"] <= escolhida["vencimento_contado"] <= l["fim"]:
            avisos.append(
                "indisponibilidade programada sem certidão em %s (%s): não empurra o prazo. Se o tribunal certificar a "
                "indisponibilidade, registre como indisponibilidade-certificada na calendario-forense e refaça a conta."
                % (escolhida["vencimento_contado"].isoformat(), l["descricao"])
            )
        if l["tipo"] == "indisponibilidade-certificada" and l["ini"] <= escolhida["inicio"] <= l["fim"]:
            avisos.append(
                "indisponibilidade certificada no dia do começo (%s): a conta só empurra o vencimento. Se a pessoa entender "
                "que o começo também muda, a data fica mais tarde; vale a mais cedo." % escolhida["inicio"].isoformat()
            )
        if l["tipo"] in ("indisponibilidade-programada", "indisponibilidade-certificada"):
            if escolhida["inicio"] < l["ini"] <= escolhida["vencimento_contado"] - UM_DIA:
                avisos.append("indisponibilidade no meio do prazo (%s): não muda a conta." % l["ini"].isoformat())
    # ponto de partida em dia sem expediente, no recesso ou numa suspensão (contagem.md, regra de ouro 6)
    def periodo_de(d, tipos):
        return [l for l in cal["linhas"] if l["tipo"] in tipos and l["ini"] <= d <= l["fim"]]

    if modo == "disponibilizacao":
        disp = p["data"]
        if not D.com_expediente(disp):
            avisos.append(
                "DÚVIDA DA DISPONIBILIZAÇÃO: disponibilização em dia sem expediente (%s: %s): conferir no diário se a data "
                "está certa. A conta seguiu do primeiro dia com expediente depois dela." % (disp.isoformat(), D.motivo(disp))
            )
        if periodo_de(disp, ("recesso",)):
            avisos.append(
                "DÚVIDA DO RECESSO: disponibilização dentro do recesso: conferir no ato do tribunal como ele trata a "
                "publicação no período (disponibilização em %s). A conta ficou com a leitura que dá a data mais cedo." % disp.isoformat()
            )
        elif periodo_de(escolhida["publicacao"], ("recesso",)):
            avisos.append(
                "DÚVIDA DO RECESSO: publicação dentro do recesso: conferir no ato do tribunal como ele trata a "
                "publicação no período (publicação em %s). A conta ficou com a leitura que dá a data mais cedo." % escolhida["publicacao"].isoformat()
            )
        for l in periodo_de(disp, ("suspensao",)) or periodo_de(escolhida["publicacao"], ("suspensao",)):
            avisos.append(
                "DÚVIDA DA SUSPENSÃO: disponibilização ou publicação dentro de uma suspensão (%s, %s): conferir no ato do "
                "tribunal como ele trata a publicação no período. A conta ficou com a leitura que dá a data mais cedo."
                % (l["descricao"], l["arquivo"])
            )
    else:
        cien = escolhida["ciencia"]
        datas_c = sorted(set([cien, escolhida.get("ciencia_calculada") or cien]))
        if any(periodo_de(d, ("recesso",)) for d in datas_c):
            avisos.append(
                "DÚVIDA DO RECESSO: ciência dentro do recesso: conferir no ato do tribunal como ele trata a ciência "
                "no período (ciência em %s). A conta ficou com a leitura que dá a data mais cedo." % cien.isoformat()
            )
        for l in [x for d in datas_c for x in periodo_de(d, ("suspensao",))][:1]:
            avisos.append(
                "DÚVIDA DA SUSPENSÃO: ciência dentro de uma suspensão (%s, %s): conferir no ato do tribunal como ele trata "
                "a ciência no período. A conta ficou com a leitura que dá a data mais cedo." % (l["descricao"], l["arquivo"])
            )
    # linhas do calendário usadas sem conferência
    for l in D.usadas:
        if linha_nao_conferida(l):
            avisos.append(
                "linha do calendário usada na conta e ainda não conferida: %s %s (%s, linha %d)."
                % (l["ini"].isoformat(), l["descricao"], l["arquivo"], l["linha"])
            )
    # ciência
    if modo in ("envio-portal", "ciencia"):
        if len(leituras_1) > 1:
            a = [r for r in leituras_1 if r["leitura"] == "a"][0]
            b = [r for r in leituras_1 if r["leitura"] == "b"][0]
            avisos.append(
                "DÚVIDA DA CIÊNCIA: a ciência cai em %s, dia sem expediente (%s). Leitura a: ciência no próprio dia, vencimento %s. "
                "Leitura b: ciência no primeiro dia útil seguinte (%s), vencimento %s. Ficou a mais cedo (%s). A pessoa decide."
                % (
                    a["ciencia"].isoformat(),
                    a.get("motivo_ciencia", ""),
                    a["vencimento"].isoformat(),
                    b["ciencia"].isoformat(),
                    b["vencimento"].isoformat(),
                    escolhida["vencimento"].isoformat(),
                )
            )
        if modo == "envio-portal":
            avisos.append(
                "ciência tácita calculada (%d dias corridos do envio): quem decide a ciência é a pessoa. Se alguém abriu a "
                "intimação antes, a ciência é na abertura e a conta muda (rode com --ciencia)." % prazo_ciencia
            )
        else:
            avisos.append("ciência informada: confira no painel a data exata da ciência.")

    # pessoa agora
    hoje = p["hoje"]
    pessoa_agora = pessoa_agora_de(p, cal["linhas"], aplica_recesso, venc_final, seg_final, escolhida)
    if seg_final < escolhida["inicio"]:
        avisos.append("a data de segurança (%s) cai antes do início do prazo: o prazo é curto, trate como urgente." % seg_final.isoformat())
    if seg_final < hoje <= venc_final:
        avisos.append("a data de segurança (%s) já passou: o prazo está na margem." % seg_final.isoformat())

    normas = {}
    for c in chaves:
        onde = NORMAS.get(c, "")
        if regras is not None and c in regras["chaves"] and regras["chaves"][c]["onde"]:
            onde = regras["chaves"][c]["onde"].replace("[CONFERIR]", "").strip()
        normas[c] = onde

    # tira avisos repetidos mantendo a ordem
    vistos = set()
    avisos_unicos = []
    for a in avisos:
        if a not in vistos:
            vistos.add(a)
            avisos_unicos.append(a)

    return {
        "modo": modo,
        "tribunal": p["tribunal"],
        "rito": rito,
        "dias": n,
        "contagem": contagem,
        "em_dobro": "sim" if p.get("dobro") else "nao",
        "origem_dias": origem_dias,
        "seguranca": seguranca,
        "chaves": chaves,
        "regra": "+".join(chaves),
        "normas": normas,
        "calendarios": cal["arquivos"],
        "leituras": leituras_1,
        "escolhida": escolhida,
        "outras": outra,
        "conta_2": leituras_2,
        "batem": batem,
        "vencimento": venc_final,
        "data_seguranca": seg_final,
        "pessoa_agora": pessoa_agora,
        "avisos": avisos_unicos,
        "duvidas": [a for a in avisos_unicos if a.startswith("DÚVIDA")],
        "usadas": list(D.usadas),
        "aplica_recesso": aplica_recesso,
    }


# ---------------------------------------------------------------- saída


def texto_da_conta(r, duplo):
    e = r["escolhida"]
    linhas = []
    titulo = "CONTA DO PRAZO · %s · rito %s · %d dias %s%s" % (
        r["tribunal"],
        r["rito"],
        r["dias"],
        "úteis" if r["contagem"] == "uteis" else "corridos",
        " · em dobro" if r["em_dobro"] == "sim" else "",
    )
    linhas.append(titulo)
    if r["pessoa_agora"]:
        linhas.append(r["pessoa_agora"])
    if r.get("duvidas"):
        linhas.append("")
        linhas.append("PARA A PESSOA DECIDIR (dúvidas da conta; vale a data mais cedo até a decisão):")
        for a in r["duvidas"]:
            linhas.append("  >> %s" % a)
    linhas.append("")
    passo = 1
    if r["modo"] == "disponibilizacao":
        linhas.append("Passo %d. Disponibilização: %s" % (passo, fmt(e["disponibilizacao"])))
        passo += 1
        for d, m in e["pulados_publicacao"]:
            linhas.append("         %s pulado: %s" % (fmt(d), m))
        linhas.append("Passo %d. Publicação: %s · primeiro dia útil depois da disponibilização (publicacao-diario)" % (passo, fmt(e["publicacao"])))
        passo += 1
    else:
        if r["modo"] == "envio-portal":
            linhas.append("Passo %d. Envio da intimação no portal: %s" % (passo, fmt(e["envio"])))
            passo += 1
            linhas.append(
                "Passo %d. Ciência tácita: %s · fim do prazo de ciência em dias corridos (intimacao-portal)"
                % (passo, fmt(e["ciencia_calculada"]))
            )
            passo += 1
        else:
            linhas.append("Passo %d. Ciência informada: %s" % (passo, fmt(e["ciencia_calculada"])))
            passo += 1
        if e["leitura"] != "unica":
            linhas.append(
                "         a ciência caiu em dia sem expediente; leitura usada: %s (ciência em %s), a que dá a data mais cedo"
                % (e["leitura"], e["ciencia"].isoformat())
            )
    ref = e["referencia"]
    pulados_inicio = [x for x in e["pulados"] if x[0] < e["inicio"]]
    pulados_meio = [x for x in e["pulados"] if x[0] > e["inicio"]]
    for d, m in pulados_inicio:
        linhas.append("         %s pulado: %s" % (fmt(d), m))
    if r["contagem"] == "uteis":
        linhas.append("Passo %d. Início: %s · primeiro dia útil depois de %s" % (passo, fmt(e["inicio"]), ref.isoformat()))
    else:
        linhas.append("Passo %d. Início: %s · dia seguinte a %s, em dias corridos" % (passo, fmt(e["inicio"]), ref.isoformat()))
    passo += 1
    linhas.append("Passo %d. Dias contados:" % passo)
    passo += 1
    linhas_dias = [(d, "c", k) for k, d in e["contados"]] + [(d, "p", m) for d, m in pulados_meio]
    linhas_dias.sort(key=lambda x: x[0])
    em_duvida = set(r.get("dias_em_duvida") or [])
    for d, tipo, info in linhas_dias:
        if tipo == "c":
            linhas.append("    %3d  %s%s" % (info, fmt(d), "  << dia em dúvida no calendário: contado nesta leitura" if d in em_duvida else ""))
        else:
            linhas.append("         %s pulado: %s" % (fmt(d), info))
    for d, m in e["empurrado"]:
        linhas.append("         %s vencimento empurrado: %s" % (fmt(d), m))
    linhas.append("Passo %d. Vencimento (data fatal): %s" % (passo, fmt(r["vencimento"])))
    passo += 1
    linhas.append(
        "Passo %d. Data de segurança (a data da agenda): %s · %d dias úteis antes do vencimento"
        % (passo, fmt(r["data_seguranca"]), r["seguranca"])
    )
    linhas.append("")
    linhas.append("Regras usadas (chaves de contagem.md):")
    for c in r["chaves"]:
        linhas.append("  - %s: %s [CONFERIR]" % (c, r["normas"].get(c) or "sem artigo na tabela"))
    linhas.append("Número de dias: %s" % r["origem_dias"])
    linhas.append("Calendário: %s" % (", ".join(r["calendarios"]) or "nenhum (--sem-calendario)"))
    linhas.append("")
    c2 = [x for x in r["conta_2"] if x["leitura"] == e["leitura"]] or r["conta_2"][:1]
    c2 = c2[0]
    if duplo or not r["batem"]:
        linhas.append("Conta 1 (dia a dia): início %s, vencimento %s, segurança %s" % (
            e["inicio"].isoformat(), e["vencimento"].isoformat(), e["data_seguranca"].isoformat()))
        linhas.append("Conta 2 (lista de dias úteis do período): início %s, vencimento %s, segurança %s" % (
            c2["inicio"].isoformat(), c2["vencimento"].isoformat(), c2["data_seguranca"].isoformat()))
        if len(r["conta_2"]) > 1:
            for x in r["conta_2"]:
                linhas.append("  conta 2, leitura %s: ciência %s, vencimento %s" % (x["leitura"], x["referencia"].isoformat(), x["vencimento"].isoformat()))
        linhas.append("AS DUAS CONTAS BATEM." if r["batem"] else "AS DUAS CONTAS NÃO BATEM: vale a data mais cedo até a pessoa decidir.")
        linhas.append("")
    outros_avisos = [a for a in r["avisos"] if a not in (r.get("duvidas") or [])]
    if outros_avisos:
        linhas.append("Avisos:")
        for a in outros_avisos:
            linhas.append("  - %s" % a)
        linhas.append("")
    linhas.append(
        "Linha sugerida para prazos.csv: publicada_em=%s · inicio=%s · vencimento=%s · data_seguranca=%s · dias=%d · contagem=%s · regra=%s · em_dobro=%s · status=sugerido · calculado_por=ia"
        % (
            (e.get("publicacao") or e.get("ciencia")).isoformat(),
            e["inicio"].isoformat(),
            r["vencimento"].isoformat(),
            r["data_seguranca"].isoformat(),
            r["dias"] // (2 if r["em_dobro"] == "sim" else 1),
            r["contagem"],
            r["regra"],
            r["em_dobro"],
        )
    )
    linhas.append("A conta é uma sugestão: o prazo só vale depois da dupla conferência de uma pessoa.")
    return "\n".join(linhas)


def para_json(obj):
    if isinstance(obj, dt.date):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: para_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [para_json(v) for v in obj]
    return obj


def json_da_conta(r):
    e = r["escolhida"]
    saida = {
        "tribunal": r["tribunal"],
        "rito": r["rito"],
        "modo": r["modo"],
        "dias": r["dias"],
        "dias_base": r["dias"] // (2 if r["em_dobro"] == "sim" else 1),
        "contagem": r["contagem"],
        "em_dobro": r["em_dobro"],
        "origem_dias": r["origem_dias"],
        "disponibilizacao": e.get("disponibilizacao"),
        "publicada_em": e.get("publicacao") or e.get("ciencia"),
        "envio": e.get("envio"),
        "ciencia": e.get("ciencia"),
        "inicio": e["inicio"],
        "vencimento": r["vencimento"],
        "data_seguranca": r["data_seguranca"],
        "seguranca_dias_uteis": r["seguranca"],
        "regra": r["regra"],
        "normas": r["normas"],
        "calendarios": r["calendarios"],
        "contados": [{"n": k, "data": d} for k, d in e["contados"]],
        "pulados": [{"data": d, "motivo": m} for d, m in e["pulados"]],
        "vencimento_empurrado": [{"data": d, "motivo": m} for d, m in e["empurrado"]],
        "leituras": [
            {"leitura": x["leitura"], "ciencia_ou_publicacao": x["referencia"], "inicio": x["inicio"], "vencimento": x["vencimento"], "data_seguranca": x["data_seguranca"]}
            for x in r["leituras"]
        ],
        "conta_2": r["conta_2"],
        "batem": r["batem"],
        "pessoa_agora": r["pessoa_agora"],
        "duvidas": r.get("duvidas", []),
        "leitura_calendario": r.get("leitura_calendario"),
        "avisos": r["avisos"],
    }
    return json.dumps(para_json(saida), ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- csv


def ler_csv(caminho, obrigatorias, nome_do_arquivo):
    texto, enc = ler_texto(caminho)
    if not texto.strip():
        raise Erro("%s está vazio: %s" % (nome_do_arquivo, caminho))
    primeira = texto.splitlines()[0]
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    campos_orig = leitor.fieldnames or []
    mapa = {c: normal(c).replace(" ", "_") for c in campos_orig}
    faltam = [c for c in obrigatorias if c not in mapa.values()]
    if faltam:
        raise Erro("%s (%s) sem as colunas obrigatórias: %s." % (nome_do_arquivo, caminho, ", ".join(faltam)))
    linhas = []
    for linha in leitor:
        linhas.append({mapa[k]: (v or "").strip() for k, v in linha.items() if k in mapa})
    with open(caminho, "rb") as f:
        tinha_bom = f.read(3) == b"\xef\xbb\xbf"
    return {"linhas": linhas, "sep": sep, "enc": enc, "bom": tinha_bom, "campos": [mapa[c] for c in campos_orig], "campos_orig": campos_orig}


def tribunal_do_processo(processo):
    """Acha o tribunal pelo número CNJ (J.TR). Não confere dígito verificador."""
    m = re.search(r"\d{7}-?\d{2}\.?\d{4}\.?(\d)\.?(\d{2})\.?\d{4}", processo or "")
    if not m:
        return None
    j, tr = m.group(1), int(m.group(2))
    if j == "4" and 1 <= tr <= 6:
        return "TRF%d" % tr
    if j == "5" and 1 <= tr <= 24:
        return "TRT%d" % tr
    if j == "8" and 1 <= tr <= len(UF_DO_TJ):
        return "TJ" + UF_DO_TJ[tr - 1]
    return None


def ultimo_com_expediente_antes(hoje, cals, tribunal):
    """O último dia com expediente antes de hoje (fim de semana e feriados do calendário do tribunal)."""
    linhas = []
    t = (tribunal or "").upper()
    for c in cals:
        if t in c["tribunais"] or "TODOS" in c["tribunais"]:
            linhas += [l for l in c["linhas"] if l["vale_para"] is None or t in l["vale_para"]]
    D = DiasDiaADia(linhas, True)
    d = hoje - UM_DIA
    for _ in range(40):
        if D.com_expediente(d):
            return d
        d -= UM_DIA
    return hoje - UM_DIA


def modo_csv(args, regras, cals, avisos_cal):
    prazos = ler_csv(
        args.csv,
        ["id", "publicacao_id", "tipo", "rito", "dias", "contagem", "regra", "em_dobro", "publicada_em", "inicio", "vencimento", "data_seguranca", "status"],
        "prazos.csv",
    )
    pubs = {}
    if args.publicacoes:
        pc = ler_csv(args.publicacoes, ["id", "disponibilizada_em", "tribunal"], "publicacoes.csv")
        pubs = {l["id"]: l for l in pc["linhas"]}
    hoje = ler_data(args.hoje, "--hoje") if args.hoje else dt.date.today()
    seguranca = args.seguranca
    resultado = []
    avisos_gerais = list(avisos_cal)
    if seguranca is None:
        seguranca = SEGURANCA_PADRAO
        avisos_gerais.append("dias de segurança não informados: usei %d dias úteis (padrão da ficha)." % seguranca)
    for l in prazos["linhas"]:
        item = {"id": l.get("id", ""), "caso": l.get("codigo_caso", ""), "cliente": l.get("cliente_curto", ""), "status": l.get("status", "").lower()}
        if normal(l.get("tipo", "")) != "prazo":
            continue
        if item["status"] in ("cumprido", "perdido", "cancelado"):
            continue
        if not re.fullmatch(r"\d+", l.get("dias", "")):
            # linha sem número de dias: entra no lote, aparece e vai para a pessoa (não é erro do lote)
            pub = pubs.get(l.get("publicacao_id", "")) or {}
            data = None
            for bruto in (pub.get("disponibilizada_em"), l.get("publicada_em")):
                try:
                    data = ler_data(bruto) if bruto else None
                except Erro:
                    data = None
                if data:
                    break
            tribunal = pub.get("tribunal") or tribunal_do_processo(l.get("processo", "")) or args.tribunal or ""
            item["situacao"] = "sem número de dias"
            item["linha"] = l
            item["data_ato"] = data
            item["sem_dias"] = "[A CONFIRMAR: quantos dias] (dias: %s; o ato não diz e a tabela do escritório não traz)" % (
                l.get("dias") or "vazio")
            ontem = min(hoje - UM_DIA, ultimo_com_expediente_antes(hoje, cals, tribunal))
            if data is None:
                item["pessoa_agora"] = "sem número de dias e sem a data do ato: a pessoa confere hoje (%s)" % (
                    l.get("providencia") or "providência a confirmar")
            elif data >= ontem:
                item["pessoa_agora"] = "ato de %s sem número de dias: a pessoa diz quantos dias hoje (%s)" % (
                    data.isoformat(), l.get("providencia") or "providência a confirmar")
            resultado.append(item)
            continue
        try:
            pub = pubs.get(l.get("publicacao_id", ""))
            regra = normal(l.get("regra", ""))
            tribunal = (pub or {}).get("tribunal") or tribunal_do_processo(l.get("processo", "")) or args.tribunal
            if not tribunal:
                raise Erro("sem tribunal (nem na publicação, nem no número do processo, nem --tribunal)")
            if pub is None and l.get("publicacao_id"):
                if "publicacao-diario" in regra or "intimacao-portal" in regra:
                    raise Erro("a publicação %s não está em publicacoes.csv" % l["publicacao_id"])
            if "intimacao-portal" in regra:
                modo, data = "envio-portal", ler_data(pub["disponibilizada_em"], "disponibilizada_em")
            elif "publicacao-diario" in regra or (pub and normal(pub.get("fonte", "")) in ("djen", "email", "e-mail", "planilha", "sistema")):
                modo, data = "disponibilizacao", ler_data((pub or {}).get("disponibilizada_em"), "disponibilizada_em")
            else:
                modo, data = "ciencia", ler_data(l.get("publicada_em"), "publicada_em (ciência)")
            rito = normal(l.get("rito", "")).replace(" ", "-")
            dobro = None
            if normal(l.get("em_dobro", "")) == "sim":
                achadas = [c for c in CHAVES_DOBRO if c in regra]
                dobro = achadas[0] if achadas else "sim"
            cont = normal(l.get("contagem", "")).replace("ú", "u") or None
            if cont and cont not in ("uteis", "corridos"):
                cont = None
            cal = selecionar_calendario(cals, tribunal, None, args.sem_calendario)
            p = {
                "modo": modo,
                "data": data,
                "dias": int(l["dias"]),
                "ato": None,
                "rito": rito,
                "tribunal": tribunal.upper(),
                "contagem": cont,
                "dobro": dobro,
                "seguranca": seguranca,
                "hoje": hoje,
                "recesso_penal": "recesso-penal" in regra,
                "domicilio": "domicilio-eletronico" in regra,
            }
            r = calcular(p, cal, regras)
            item["r"] = r
            reg = {k: l.get(k, "") for k in ("publicada_em", "inicio", "vencimento", "data_seguranca")}
            calc = {
                "publicada_em": (r["escolhida"].get("publicacao") or r["escolhida"].get("ciencia")).isoformat(),
                "inicio": r["escolhida"]["inicio"].isoformat(),
                "vencimento": r["vencimento"].isoformat(),
                "data_seguranca": r["data_seguranca"].isoformat(),
            }
            item["calc"] = calc
            diverge = []
            vazios = []
            for k in calc:
                if reg[k] == "":
                    vazios.append(k)
                else:
                    try:
                        if ler_data(reg[k], k).isoformat() != calc[k]:
                            diverge.append("%s: registro %s, conta %s" % (k, reg[k], calc[k]))
                    except Erro:
                        diverge.append("%s: registro '%s' fora do formato" % (k, reg[k]))
            item["diverge"] = diverge
            item["vazios"] = vazios
            item["linha"] = l
            if not r["batem"]:
                item["situacao"] = "contas não batem"
            elif diverge:
                item["situacao"] = "diverge do registro"
            elif vazios:
                item["situacao"] = "registro em branco"
            else:
                item["situacao"] = "ok"
        except Erro as ex:
            item["situacao"] = "erro"
            item["erro"] = str(ex)
        resultado.append(item)

    if not resultado:
        raise Erro("prazos.csv não tem nenhuma linha de prazo aberta (tipo prazo, status sugerido, conferido ou agendado) para contar.")
    rel = relatorio_csv(resultado, avisos_gerais, args, hoje)
    if args.saida:
        os.makedirs(os.path.dirname(os.path.abspath(args.saida)) or ".", exist_ok=True)
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(rel + "\n")
        print("Relatório gravado em %s" % args.saida)
    print(rel)
    if args.gravar:
        gravar_csv(args.csv, prazos, resultado, hoje)
    ruins = [i for i in resultado if i["situacao"] in ("contas não batem", "diverge do registro", "erro")]
    return 2 if ruins else 0


def relatorio_csv(resultado, avisos_gerais, args, hoje):
    L = []
    L.append("CONTA DO LOTE · %s · %d prazos abertos" % (hoje.isoformat(), len(resultado)))
    cont = {}
    for i in resultado:
        cont[i["situacao"]] = cont.get(i["situacao"], 0) + 1
    L.append("Resumo: " + " · ".join("%s %d" % (k, v) for k, v in sorted(cont.items())))
    L.append("")
    agora = []
    for i in resultado:
        texto = (i.get("r") or {}).get("pessoa_agora") or i.get("pessoa_agora")
        if texto:
            texto = re.sub(r"^PESSOA AGORA:\s*", "", texto)
            agora.append("%s%s: %s" % (i["id"], " " + i["caso"] if i["caso"] else "", texto))
    if agora:
        L.append("PESSOA AGORA")
        for t in agora:
            L.append("  - %s" % t)
        L.append("")
    L.append("| id | caso | status | vencimento no registro | conta 1 | conta 2 | segurança | regra | situação |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for i in sorted(resultado, key=lambda x: (x.get("calc") or {}).get("vencimento", "9999")):
        if i["situacao"] == "erro":
            L.append("| %s | %s | %s | %s | | | | | erro: %s |" % (i["id"], i["caso"], i["status"], "", i["erro"]))
            continue
        if i["situacao"] == "sem número de dias":
            L.append("| %s | %s | %s | %s | | | | | sem número de dias: [A CONFIRMAR: quantos dias] |" % (
                i["id"], i["caso"], i["status"], i["linha"].get("vencimento", "") or "vazio"))
            continue
        r = i["r"]
        e = r["escolhida"]
        c2 = [x for x in r["conta_2"] if x["leitura"] == e["leitura"]] or r["conta_2"]
        L.append(
            "| %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                i["id"],
                i["caso"],
                i["status"],
                i["linha"].get("vencimento", "") or "vazio",
                e["vencimento"].isoformat(),
                c2[0]["vencimento"].isoformat(),
                r["data_seguranca"].isoformat(),
                r["regra"],
                i["situacao"],
            )
        )
    L.append("")
    div = [i for i in resultado if i["situacao"] in ("diverge do registro", "contas não batem")]
    if div:
        L.append("SEPARADAS (divergem: vale a data mais cedo até a pessoa decidir)")
        for i in div:
            detalhe = "; ".join(i.get("diverge") or []) or "as duas contas deram datas diferentes"
            L.append("  - %s %s: %s" % (i["id"], i["caso"], detalhe))
        L.append("")
    sem_dias = [i for i in resultado if i["situacao"] == "sem número de dias"]
    if sem_dias:
        L.append("SEM NÚMERO DE DIAS (sugerido, sem vencimento: a pessoa informa os dias e a conta é refeita)")
        for i in sem_dias:
            L.append("  - %s %s: ato de %s · %s · %s" % (
                i["id"], i["caso"], i["data_ato"].isoformat() if i.get("data_ato") else "data a confirmar",
                i["linha"].get("providencia") or "providência a confirmar", i["sem_dias"]))
        L.append("")
    duv = [i for i in resultado if i.get("r") and i["r"].get("duvidas")]
    if duv:
        L.append("DÚVIDAS DA CONTA (vale a data mais cedo até a pessoa decidir)")
        for i in duv:
            for a in i["r"]["duvidas"]:
                L.append("  - %s %s: %s" % (i["id"], i["caso"], a))
        L.append("")
    erros = [i for i in resultado if i["situacao"] == "erro"]
    if erros:
        L.append("NÃO CONTADAS (para a pessoa)")
        for i in erros:
            L.append("  - %s %s: %s" % (i["id"], i["caso"], i["erro"]))
        L.append("")
    av = list(avisos_gerais)
    for i in resultado:
        if i.get("r"):
            for a in i["r"]["avisos"]:
                if a in (i["r"].get("duvidas") or []):
                    continue
                linha = "%s: %s" % (i["id"], a)
                av.append(linha)
    if av:
        L.append("Avisos")
        for a in av:
            L.append("  - %s" % a)
        L.append("")
    L.append("Nenhuma linha muda de status por este script. Conferido e agendado só depois da dupla conferência de uma pessoa.")
    return "\n".join(L)


def gravar_csv(caminho, prazos, resultado, hoje):
    pasta = os.path.dirname(os.path.abspath(caminho))
    lotes = os.path.join(pasta, "lotes")
    os.makedirs(lotes, exist_ok=True)
    copia = os.path.join(lotes, "prazos-antes-do-lote-%s.csv" % dt.datetime.now().strftime("%Y-%m-%d-%H%M%S"))
    shutil.copy2(caminho, copia)
    por_id = {i["id"]: i for i in resultado if i.get("r")}
    sem_dias = {i["id"]: i for i in resultado if i["situacao"] == "sem número de dias"}
    mudou = 0
    for l in prazos["linhas"]:
        if l.get("id", "") in sem_dias and l.get("status", "").lower() == "sugerido":
            if "A CONFIRMAR: quantos dias" not in l.get("observacao", ""):
                l["observacao"] = (l.get("observacao", "") + "; [A CONFIRMAR: quantos dias]").strip("; ")
                l["atualizado_em"] = hoje.isoformat()
                mudou += 1
            continue
        i = por_id.get(l.get("id", ""))
        if not i or l.get("status", "").lower() != "sugerido":
            continue
        alterou = False
        for k in i["vazios"]:
            l[k] = i["calc"][k]
            alterou = True
        if not l.get("regra"):
            l["regra"] = i["r"]["regra"]
            alterou = True
        if i["diverge"] or not i["r"]["batem"]:
            nota = "conta do lote %s: vencimento %s, segurança %s; diverge do registro, vale a mais cedo até a pessoa decidir" % (
                hoje.isoformat(), i["calc"]["vencimento"], i["calc"]["data_seguranca"])
            l["observacao"] = (l.get("observacao", "") + "; " + nota).strip("; ")
            alterou = True
        for d in i["r"].get("duvidas") or []:
            nota = re.sub(r"^DÚVIDA ([^:]+):", lambda m: "dúvida " + m.group(1).lower() + ":", d)
            if nota not in l.get("observacao", ""):
                l["observacao"] = (l.get("observacao", "") + "; " + nota).strip("; ")
                alterou = True
        if alterou:
            l["atualizado_em"] = hoje.isoformat()
            mudou += 1
    campos = prazos["campos"]
    for extra in ("observacao", "atualizado_em"):
        if extra not in campos:
            campos.append(extra)
    enc = "utf-8-sig" if prazos["bom"] else ("cp1252" if prazos["enc"] == "cp1252" else "utf-8")
    with open(caminho, "w", encoding=enc, newline="") as f:
        w = csv.writer(f, delimiter=prazos["sep"])
        cab = []
        for c in campos:
            orig = [o for o in prazos["campos_orig"] if normal(o).replace(" ", "_") == c]
            cab.append(orig[0] if orig else c)
        w.writerow(cab)
        for l in prazos["linhas"]:
            w.writerow([l.get(c, "") for c in campos])
    print("prazos.csv atualizado: %d linhas (só sugerido: datas em branco preenchidas e observação de divergência). Cópia de antes: %s" % (mudou, copia))


# ---------------------------------------------------------------- linha de comando


def montar_args():
    ap = argparse.ArgumentParser(
        description="A conta do prazo processual, passo a passo, pelo calendário do tribunal. Só sugere: quem confirma é uma pessoa.",
    )
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--disponibilizacao", help="data de disponibilização no diário (DJEN ou do tribunal)")
    g.add_argument("--ciencia", help="data da ciência informada pela pessoa (portal aberto, Domicílio Judicial Eletrônico)")
    g.add_argument("--envio-portal", dest="envio_portal", help="data de envio da intimação no portal (ciência tácita)")
    ap.add_argument("--dias", type=int, help="número de dias do próprio ato")
    ap.add_argument("--ato", help="o ato, para buscar o número de dias na tabela do escritório (precisa de --regras)")
    ap.add_argument("--regras", help="regras-de-contagem.md do escritório (ou regras-de-treino.md)")
    ap.add_argument("--rito", choices=RITOS)
    ap.add_argument("--tribunal", help="sigla do tribunal (TRF6, TRT3, TJMG...)")
    ap.add_argument("--calendario", help="arquivo do calendário ou a pasta 04-base/controladoria/calendario/")
    ap.add_argument("--cidade", help="cidade do juízo, quando há calendários de mais de uma cidade para o tribunal")
    ap.add_argument("--contagem", choices=("uteis", "corridos"))
    ap.add_argument("--dobro", nargs="?", const="sim", help="dobra o prazo (decisão da pessoa); diga a chave: " + ", ".join(CHAVES_DOBRO))
    ap.add_argument("--seguranca", type=int, help="dias úteis de segurança antes do vencimento (dias_de_seguranca da ficha)")
    ap.add_argument("--recesso-penal", dest="recesso_penal", action="store_true", help="a pessoa confirmou que a exceção do recesso penal não se aplica")
    ap.add_argument("--domicilio", action="store_true", help="a ciência veio do Domicílio Judicial Eletrônico")
    ap.add_argument("--prazo-material", dest="prazo_material", action="store_true", help="prazo de direito material: o script recusa")
    ap.add_argument("--sem-calendario", dest="sem_calendario", action="store_true", help="conta só com fins de semana, com aviso em destaque")
    ap.add_argument("--hoje", help="data de hoje para o PESSOA AGORA (padrão: a data do computador)")
    ap.add_argument("--duplo", action="store_true", help="mostra as duas contas independentes e diz se batem")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--csv", help="prazos.csv: conta todos os prazos abertos do lote")
    ap.add_argument("--publicacoes", help="publicacoes.csv, para o modo --csv")
    ap.add_argument("--gravar", action="store_true", help="no modo --csv, preenche as datas em branco das linhas sugerido")
    ap.add_argument("--saida", help="no modo --csv, grava o relatório neste arquivo .md")
    return ap


def principal(argv=None):
    ap = montar_args()
    args = ap.parse_args(argv)
    if args.seguranca is not None and args.seguranca < 0:
        raise Erro("--seguranca não pode ser negativo.")
    regras = ler_regras(args.regras) if args.regras else None
    cals, avisos_cal = carregar_calendarios(args.calendario)
    if not cals and not args.sem_calendario:
        raise Erro(
            "falta o calendário (--calendario <arquivo ou pasta>). Sem ele, só com --sem-calendario, que conta apenas fins de semana."
        )
    if args.csv:
        return modo_csv(args, regras, cals, avisos_cal)
    if args.disponibilizacao:
        modo, data = "disponibilizacao", ler_data(args.disponibilizacao, "--disponibilizacao")
    elif args.ciencia:
        modo, data = "ciencia", ler_data(args.ciencia, "--ciencia")
    elif args.envio_portal:
        modo, data = "envio-portal", ler_data(args.envio_portal, "--envio-portal")
    else:
        if args.prazo_material or eh_prazo_material(args.ato):
            raise Erro(
                "prazo de direito material (prazo-material: %s [CONFERIR]). O script não calcula decadência, prescrição "
                "nem prazo de contrato: a pessoa informa a data." % NORMAS["prazo-material"]
            )
        raise Erro("diga de onde a conta parte: --disponibilizacao, --ciencia ou --envio-portal (AAAA-MM-DD).")
    if not args.rito:
        raise Erro("falta o rito (--rito civel|trabalhista|juizado-civel|juizado-federal|penal|outro).")
    if not args.tribunal:
        raise Erro("falta o tribunal (--tribunal SIGLA), para usar o calendário certo.")
    if args.dobro and args.dobro != "sim" and args.dobro not in CHAVES_DOBRO:
        raise Erro("--dobro %s: chave desconhecida. Use %s, ou --dobro sem chave." % (args.dobro, ", ".join(CHAVES_DOBRO)))
    cal = selecionar_calendario(cals, args.tribunal, args.cidade, args.sem_calendario)
    cal["avisos"] = avisos_cal + cal["avisos"]
    p = {
        "modo": modo,
        "data": data,
        "dias": args.dias,
        "ato": args.ato,
        "rito": args.rito,
        "tribunal": args.tribunal.upper(),
        "contagem": args.contagem,
        "dobro": args.dobro,
        "seguranca": args.seguranca,
        "hoje": ler_data(args.hoje, "--hoje") if args.hoje else dt.date.today(),
        "recesso_penal": args.recesso_penal,
        "domicilio": args.domicilio,
        "prazo_material": args.prazo_material,
    }
    r = calcular(p, cal, regras)
    if args.json:
        print(json_da_conta(r))
    else:
        print(texto_da_conta(r, args.duplo))
    return 0 if r["batem"] else 2


def main():
    try:
        codigo = principal()
    except Erro as ex:
        sys.stderr.write("ERRO: %s\n" % ex)
        sys.exit(1)
    sys.exit(codigo)


if __name__ == "__main__":
    main()
