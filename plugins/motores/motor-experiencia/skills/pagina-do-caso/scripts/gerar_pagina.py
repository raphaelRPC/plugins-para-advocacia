#!/usr/bin/env python3
"""Gera a página do caso (HTML) a partir de um arquivo .md ou .json do caso.

Uso:
    python3 gerar_pagina.py <conteudo.md|conteudo.json> <saida.html> [--modelo caminho] [--lista arquivo.md]
    python3 gerar_pagina.py <conteudo> --so-conferir

O que faz:
  1. Lê o conteúdo do caso (formato em ../assets/conteudo-exemplo-marta.md e
     ../assets/conteudo-exemplo-helena.json).
  2. Confere os dados: bloqueia CPF, número de processo, valor em dinheiro, endereço,
     dado de saúde, empresa da outra parte, promessa ou previsão de decisão e qualquer
     marcação [A PREENCHER], [A DEFINIR], [A CONFIRMAR], [CONFERIR] ou [MAIÚSCULAS].
     Dado de saúde inclui os termos comuns (dor, hérnia, crise de ansiedade, afastada,
     afastamento, laudo, CID, internação, cirurgia, tratamento, medicação, passou mal,
     acamada, Alzheimer, demência, AVC, depressão, gestante, gravidez, deficiência e
     semelhantes);
     "laudo da perícia" e "laudo do perito" passam, porque são o passo do processo.
     O nome do benefício (auxílio-doença, auxílio por incapacidade, BPC, aposentadoria)
     não é dado de saúde e passa, inclusive "BPC da pessoa com deficiência". Promessa
     inclui "logo sai", "sai logo", "semana que vem", "você vai receber", "vai dar
     (tudo) certo", "com certeza", "garantido" e semelhantes. Prazo do juiz ou do órgão:
     "decide em 30 dias", "decide até <mês>", "deve decidir até", "sai até", "o juiz tem
     N dias"; o passado ("foi julgado em <mês>") é fato e passa.
  3. Preenche o modelo ../assets/pagina-modelo.html, escapando todo texto.
  4. Imprime a lista do que está na página, para o advogado dar o ok antes de publicar.

Sai com código 1 e uma mensagem clara quando falta o arquivo, falta campo obrigatório
ou a conferência bloqueia. Só biblioteca padrão. Python 3.9+.
"""
import argparse
import base64
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MODELO_PADRAO = AQUI.parent / "assets" / "pagina-modelo.html"

COR_MARCA_PADRAO = "#1f3a5f"
COR_DESTAQUE_PADRAO = "#b8892b"
FONTE_TITULOS_PADRAO = "Fraunces"
FONTE_TEXTO_PADRAO = "Source Sans 3"
SERIF = ", Georgia, 'Times New Roman', serif"
SANS = ", system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
FONTES_SERIFADAS = {"fraunces", "source serif 4", "merriweather", "lora", "playfair display",
                    "libre baskerville", "eb garamond", "cormorant garamond", "crimson pro",
                    "noto serif", "pt serif", "dm serif display"}

ESTADOS_ETAPA = {"feito": "feito", "feita": "feito", "concluido": "feito", "concluida": "feito",
                 "atual": "atual", "agora": "atual", "em andamento": "atual",
                 "depois": "depois", "proximo": "depois", "próximo": "depois", "a seguir": "depois"}
ROTULO_ETAPA = {"feito": "feito", "atual": "agora", "depois": "a seguir"}

ORIGENS = {"escritorio": "escritorio", "escritório": "escritorio", "trabalho do escritorio": "escritorio",
           "trabalho do escritório": "escritorio", "processo": "processo", "tribunal": "processo",
           "orgao": "processo", "órgão": "processo", "inss": "processo", "voce": "voce", "você": "voce",
           "cliente": "voce"}

# termos que pedem explicação no glossário quando aparecem no texto
TERMOS_TECNICOS = ["concluso", "conclusos", "despacho", "sentença", "citação", "contestação", "réplica",
                   "audiência", "perícia", "perito", "laudo", "quesitos", "recurso", "apelação", "acórdão",
                   "intimação", "juntada", "petição inicial", "distribuído", "distribuição", "protocolo",
                   "protocolado", "liminar", "tutela", "alvará", "rpv", "precatório", "homologação",
                   "homologado", "trânsito em julgado", "cumprimento de sentença", "bpc", "cnis",
                   "exigência", "carta de concessão", "instrução", "conciliação", "mediação",
                   "procuração", "embargos"]

# Decisão no futuro (o passado, "foi julgado em março", é fato e passa).
VERBO_DE_DECISAO = (r"\b(decide|decidem|decidir[áa]|decidir[ãa]o|julga|julgam|julgar[áa]|julgar[ãa]o|sentencia|"
                    r"analisa|analisam|analisar[áa]|aprova|concede|sai|saem|sair[áa]|sair[ãa]o|"
                    r"(vai|v[ãa]o|deve|devem|tende\s+a|costuma)\s+(decidir|julgar|sentenciar|analisar|aprovar|conceder|sair))")
MESES = (r"(janeiro|fevereiro|mar[çc]o|abril|maio|junho|julho|agosto|setembro|outubro|nove[m]bro|dezembro)\b")

BLOQUEIOS = [
    ("CPF", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")),
    ("número de processo", re.compile(r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b")),
    ("número de processo", re.compile(r"\bprocesso\s*(n[º°o.]*|número)\s*:?\s*\d", re.I)),
    ("número de benefício", re.compile(r"\b(nb|benefício\s*n[º°o.]*)\s*:?\s*\d{3}", re.I)),
    ("valor em dinheiro", re.compile(r"R\$|\breais\b|\bvalor da causa\b", re.I)),
    ("endereço", re.compile(r"\b([Rr]ua|[Aa]venida|[Aa]v\.|[Tt]ravessa|[Aa]lameda|[Rr]odovia|[Pp]raça)\s+(d[aeo]s?\s+)?[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]")),
    ("endereço (CEP)", re.compile(r"\b\d{5}-\d{3}\b")),
    ("dado de saúde", re.compile(r"\b(internad[ao]s?|interna[çc][ãa]o|interna[çc][õo]es|hospital\w*|uti|cid|"
                                 r"diagn[óo]stic\w*|doen[çc]a\w*|doente\w*|enfermidade\w*|c[âa]ncer|cirurgi\w*|"
                                 r"cir[úu]rgic\w*|operad[ao]\s+d[aeo]s?|depress[ãa]o|deprimid[ao]s?|hiv|avc|infarto|"
                                 r"tumor\w*|fratura\w*|psiqui[áa]tric\w*|psiquiatr\w*|psic[óo]log\w*|transtorno\w*|"
                                 r"s[íi]ndrome\w*|crises?\s+de\s+(ansiedade|p[âa]nico|choro)|ansiedade\s+generalizada|"
                                 r"p[âa]nico|h[ée]rnias?|dor|dores|les[ãa]o|les[õo]es|sequelas?|afastad[ao]s?|"
                                 r"afastamentos?|atestados?|laudos?|exames?\s+m[ée]dicos?|consultas?\s+m[ée]dicas?|"
                                 r"tratamentos?|terapia\w*|fisioterapia\w*|medica[çc][ãa]o|medica[çc][õo]es|"
                                 r"rem[ée]dio\w*|medicament\w*|quimioterapia|radioterapia|hemodi[áa]lise|"
                                 r"diabet\w*|hipertens\w*|gravidez|gr[áa]vida|gestantes?|gesta[çc][ãa]o|"
                                 r"p[óo]s[\s-]?parto|aborto|"
                                 r"(passou|passando|passa|sentiu|sentindo)[\s-]+mal|mal[\s-]+s[úu]bito|desmai\w*|"
                                 r"acamad[ao]s?|alzheimer|dem[êe]ncia|parkinson|esclerose|epilep\w*|convuls\w*|"
                                 r"derrame|acidente\s+vascular|infartou|autis\w*|esquizofren\w*|bipolar|"
                                 r"deficien\w*|defici[êe]ncias?|"
                                 r"(problemas?|estado|quadro|condi[çc][ãa]o|intercorr[êe]ncias?|quest[ãa]o|quest[õo]es)"
                                 r"\s+de\s+sa[úu]de|sa[úu]de\s+d[aeo]s?\s+(m[ãa]e|pai|cliente|filh[ao]|senhora?|esposa|marido)|"
                                 r"pronto[\s-]socorro|socorrid[ao]s?)\b", re.I)),
    ("empresa da outra parte", re.compile(r"\b(ltda|s\.a\.|s/a|eireli)\b", re.I)),
    ("promessa ou previsão", re.compile(r"\b(chance|chances|garantid[oa]s?|garantimos|garanto|garantia de|êxito|"
                                        r"causa ganha|ganho certo|vamos ganhar|já ganhou|em breve|deve sair|"
                                        r"previsão de|vai sair até|sai até|logo sai|logo,?\s+logo|já já|"
                                        r"semana que vem|mês que vem|ano que vem|"
                                        r"(você|senhora?|o senhor|a senhora)\s+vai\s+receber|vai\s+receber|vão\s+receber|"
                                        r"vai\s+ganhar|vão\s+pagar|vai\s+ser\s+aprovad[oa]|"
                                        r"com certeza|certamente|sem dúvida|é certo que|pode ficar tranquil[ao] que|"
                                        r"sai(r[áa])?\s+logo|vai\s+sair\s+logo|deve\s+sair\s+logo|logo\s+vai\s+sair|"
                                        r"sai\s+r[áa]pido|vai\s+sair\s+r[áa]pido|"
                                        r"(vai|v[ãa]o|deve|tende\s+a|h[áa]\s+de)\s+dar\s+(tudo\s+)?cert[oa]\w*|"
                                        r"tudo\s+vai\s+dar\s+cert[oa]\w*|vai\s+ficar\s+tudo\s+bem|vamos\s+conseguir)\b", re.I)),
    ("prazo do juiz ou do órgão", re.compile(
        VERBO_DE_DECISAO + r"\s+(em\s+at[ée]|em|at[ée]|dentro\s+de|no\s+prazo\s+de|daqui\s+a|nos\s+pr[óo]ximos|nas\s+pr[óo]ximas)\s+"
        r"(\d+|um|uma|dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|quinze|vinte|trinta|sessenta|noventa|"
        r"poucos|poucas|alguns|algumas)?\s*(dias?|semanas?|m[êe]s|meses|anos?)\b"
        r"|" + VERBO_DE_DECISAO + r"\s+(at[ée]|em|no\s+come[çc]o\s+de|no\s+in[íi]cio\s+de|no\s+fim\s+de|no\s+final\s+de)\s+"
        r"((o\s+)?(fim|final|come[çc]o|in[íi]cio)\s+d[eo]\s+)?" + MESES +
        r"|" + VERBO_DE_DECISAO + r"\s+(at[ée]|em)\s+(o\s+)?(fim|final|come[çc]o|in[íi]cio)\s+d[oe]\s+(m[êe]s|ano|semestre)\b"
        r"|\bdeve(m)?\s+(decidir|julgar|sentenciar|analisar)\s+(at[ée]|em|logo|nos\s+pr[óo]ximos|nas\s+pr[óo]ximas)\b"
        r"|\b\d+\s+(dias?|semanas?|meses)\s+para\s+(decidir|julgar|sentenciar|analisar)\b"
        r"|\b(juiz|ju[íi]za|ju[íi]zo|inss|tribunal|desembargador\w*|relator\w*|perito|perita)\s+(tem|t[êe]m)\s+(\d+|at[ée])\b",
        re.I)),
    ("marcação interna", re.compile(r"\[(A PREENCHER|A DEFINIR|A CONFIRMAR|CONFERIR)[^\]]*\]")),
    ("marcação interna", re.compile(r"\[[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 _-]{2,}\]")),
]
# Nomes de benefício não são dado de saúde: saem do texto antes da conferência de saúde.
BENEFICIOS = re.compile(
    r"\b(aux[íi]lio[\s-]+doen[çc]a|aux[íi]lio[\s-]+acidente|aux[íi]lio\s+por\s+incapacidade(\s+tempor[áa]ria)?|"
    r"aposentadoria\s+por\s+incapacidade(\s+permanente)?|aposentadoria\s+por\s+invalidez|"
    r"aposentadoria(\s+(especial|rural|por\s+idade|por\s+tempo\s+de\s+contribui[çc][ãa]o|"
    r"da\s+pessoa\s+com\s+defici[êe]ncia))?|"
    r"bpc(\s*/\s*loas)?(\s+(idoso|(d[ao]|à|para\s+a?)\s*pessoa\s+com\s+defici[êe]ncia))?|"
    r"benef[íi]cio\s+de\s+presta[çc][ãa]o\s+continuada|loas|sal[áa]rio[\s-]+maternidade)\b", re.I)
# "Laudo" do passo do processo, sem o conteúdo, pode aparecer; o resto (laudo médico, o que o laudo diz) bloqueia.
LAUDO_DO_PROCESSO = re.compile(r"\blaudos?\s+(pericial|periciais|da\s+per[íi]cia|do\s+perito|da\s+perita)\b", re.I)
DICA = {
    "dado de saúde": " (a página diz só o passo do processo: \"perícia\", \"laudo da perícia\"; o nome do benefício pode)",
    "promessa ou previsão": " (troque por \"quando houver novidade, a gente avisa\" ou pela data de um ato já marcado)",
    "prazo do juiz ou do órgão": " (não há como saber quando o juiz ou o órgão decide: \"o tempo depende da vara; a gente acompanha e avisa\")",
}
TELEFONE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")


class ErroDeEntrada(Exception):
    pass


# ---------------------------------------------------------------- datas

def ler_data(valor):
    """Aceita AAAA-MM-DD e DD/MM/AAAA. Devolve date ou None."""
    if valor is None:
        return None
    s = str(valor).strip()
    if not s:
        return None
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        a, me, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if not m:
            return None
        d, me, a = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return date(a, me, d)
    except ValueError:
        return None


def mostrar_data(valor):
    d = ler_data(valor)
    return d.strftime("%d/%m/%Y") if d else str(valor or "").strip()


# ---------------------------------------------------------------- leitura

def ler_md(texto):
    """Formato: cabeçalho --- chave: valor --- e seções '## Título' com linhas
    'chave: valor' ou itens '- a | b | c'."""
    texto = texto.replace("\r\n", "\n").lstrip("﻿")
    dados = {"_secoes": {}}
    m = re.match(r"^---\n(.*?)\n---\n?", texto, re.S)
    corpo = texto
    if m:
        for linha in m.group(1).split("\n"):
            if ":" in linha and not linha.strip().startswith("#"):
                k, v = linha.split(":", 1)
                dados[k.strip().lower()] = v.strip()
        corpo = texto[m.end():]
    atual = None
    for linha in corpo.split("\n"):
        if linha.startswith("## "):
            atual = normalizar_chave(linha[3:])
            dados["_secoes"].setdefault(atual, {"itens": [], "campos": {}, "texto": []})
            continue
        if atual is None or not linha.strip() or linha.strip().startswith("<!--"):
            continue
        sec = dados["_secoes"][atual]
        s = linha.strip()
        if s.startswith("- "):
            sec["itens"].append([p.strip() for p in s[2:].split("|")])
        elif re.match(r"^[a-z_]+\s*:", s):
            k, v = s.split(":", 1)
            sec["campos"][k.strip()] = v.strip()
        else:
            sec["texto"].append(s)
    return de_md_para_dict(dados)


def normalizar_chave(t):
    t = t.strip().lower()
    trocas = str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc")
    t = t.translate(trocas)
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def de_md_para_dict(d):
    s = d.get("_secoes", {})

    def sec(*nomes):
        for n in nomes:
            if n in s:
                return s[n]
        return {"itens": [], "campos": {}, "texto": []}

    onde = sec("onde_estamos")
    etapas = [{"estado": i[0], "nome": i[1] if len(i) > 1 else ""} for i in sec("etapas")["itens"]]
    tempo = []
    for i in sec("linha_do_tempo", "o_que_aconteceu_e_o_que_fizemos")["itens"]:
        i = i + [""] * (5 - len(i))
        tempo.append({"data": i[0], "origem": i[1], "titulo": i[2], "texto": i[3],
                      "aparece_no_processo": i[4]})
    passos = [{"quando": i[0], "texto": i[1] if len(i) > 1 else ""} for i in sec("proximos_passos")["itens"]]
    voce = [{"ate": i[0], "texto": i[1] if len(i) > 1 else ""} for i in sec("o_que_depende_de_voce", "depende_de_voce")["itens"]]
    glos = [{"termo": i[0], "explicacao": i[1] if len(i) > 1 else ""} for i in sec("glossario", "palavras_desta_pagina")["itens"]]
    fizemos = [i[0] for i in sec("o_que_ja_fizemos_por_voce", "o_que_ja_fizemos")["itens"] if i and i[0]]
    falar = sec("quando_voltamos_a_falar")
    texto_falar = falar["campos"].get("texto") or " ".join(falar["texto"])
    return {
        "escritorio": {"nome": d.get("escritorio", ""), "canal_oficial": d.get("canal_oficial", ""),
                       "telefone_oficial": d.get("telefone_oficial", ""), "whatsapp_oficial": d.get("whatsapp_oficial", ""),
                       "horario": d.get("horario", ""), "assinatura": d.get("assinatura", "")},
        "identidade_visual": {"cor_principal": d.get("cor_principal", ""), "cor_destaque": d.get("cor_destaque", ""),
                              "fonte_titulos": d.get("fonte_titulos", ""), "fonte_texto": d.get("fonte_texto", ""),
                              "logo": d.get("logo", ""), "tamanho_do_texto": d.get("tamanho_do_texto", "")},
        "cliente": {"primeiro_nome": d.get("cliente", "")},
        "caso": {"tipo": d.get("tipo_de_caso", ""), "area": d.get("area", ""), "codigo": d.get("codigo", "")},
        "atualizado_em": d.get("atualizado_em", ""),
        "proxima_atualizacao": d.get("proxima_atualizacao", ""),
        "o_que_ja_fizemos": fizemos,
        "fase": {"titulo": onde["campos"].get("fase", ""),
                 "explicacao": onde["campos"].get("explicacao", "") or " ".join(onde["texto"])},
        "etapas": etapas,
        "linha_do_tempo": tempo,
        "proximos_passos": passos,
        "depende_de_voce": voce,
        "glossario": glos,
        "voltamos_a_falar": texto_falar,
    }


def ler_entrada(caminho):
    p = Path(caminho)
    if not p.exists():
        raise ErroDeEntrada(f"não encontrei o arquivo do caso: {p}")
    texto = p.read_text(encoding="utf-8-sig")
    if p.suffix.lower() == ".json":
        try:
            return json.loads(texto)
        except json.JSONDecodeError as e:
            raise ErroDeEntrada(f"o JSON do caso não abre (linha {e.lineno}): {e.msg}")
    if p.suffix.lower() in {".md", ".txt"}:
        return ler_md(texto)
    raise ErroDeEntrada("o arquivo do caso precisa ser .md ou .json")


# ---------------------------------------------------------------- conferência

def g(d, *caminho, padrao=""):
    for c in caminho:
        if not isinstance(d, dict):
            return padrao
        d = d.get(c)
        if d is None:
            return padrao
    return d


def campos_obrigatorios(d):
    falta = []
    for rotulo, caminho in [("escritório (nome)", ("escritorio", "nome")),
                            ("primeiro nome do cliente", ("cliente", "primeiro_nome")),
                            ("tipo de caso", ("caso", "tipo")),
                            ("data da atualização", ("atualizado_em",)),
                            ("fase (onde estamos)", ("fase", "titulo")),
                            ("explicação da fase", ("fase", "explicacao")),
                            ("quando voltamos a falar", ("voltamos_a_falar",)),
                            ("canal oficial", ("escritorio", "canal_oficial"))]:
        if not str(g(d, *caminho)).strip():
            falta.append(rotulo)
    if not g(d, "etapas", padrao=[]):
        falta.append("etapas (a barra de onde estamos)")
    if not g(d, "linha_do_tempo", padrao=[]):
        falta.append("linha do tempo (ao menos um item)")
    if not g(d, "proximos_passos", padrao=[]):
        falta.append("próximos passos (ao menos um item)")
    if str(g(d, "atualizado_em")).strip() and not ler_data(g(d, "atualizado_em")):
        falta.append("data da atualização em AAAA-MM-DD ou DD/MM/AAAA")
    return falta


def textos_da_pagina(d):
    """(rótulo, texto) de tudo o que vai aparecer na página."""
    saida = [("escritório", g(d, "escritorio", "nome")), ("assinatura", g(d, "escritorio", "assinatura")),
             ("horário", g(d, "escritorio", "horario")), ("nome", g(d, "cliente", "primeiro_nome")),
             ("tipo de caso", g(d, "caso", "tipo")), ("área", g(d, "caso", "area")),
             ("fase", g(d, "fase", "titulo")), ("explicação da fase", g(d, "fase", "explicacao")),
             ("quando voltamos a falar", g(d, "voltamos_a_falar")),
             ("próxima atualização", g(d, "proxima_atualizacao"))]
    for t in g(d, "o_que_ja_fizemos", padrao=[]) or []:
        saida.append(("o que já fizemos", t))
    for e in g(d, "etapas", padrao=[]):
        saida.append(("etapa", g(e, "nome")))
    for i in g(d, "linha_do_tempo", padrao=[]):
        saida += [("linha do tempo", g(i, "titulo")), ("linha do tempo", g(i, "texto"))]
    for i in g(d, "proximos_passos", padrao=[]):
        saida.append(("próximos passos", g(i, "texto")))
        if not ler_data(g(i, "quando")):
            saida.append(("próximos passos", g(i, "quando")))
    for i in g(d, "depende_de_voce", padrao=[]):
        saida.append(("depende do cliente", g(i, "texto")))
    for i in g(d, "glossario", padrao=[]):
        saida += [("glossário", g(i, "termo")), ("glossário", g(i, "explicacao"))]
    return [(r, str(t)) for r, t in saida if str(t).strip()]


def conferir(d):
    bloqueios, avisos = [], []
    contatos = [("canal oficial", str(g(d, "escritorio", "canal_oficial"))),
                ("canal oficial", str(g(d, "escritorio", "telefone_oficial"))),
                ("canal oficial", str(g(d, "escritorio", "whatsapp_oficial")))]
    for rotulo, texto in textos_da_pagina(d) + contatos:
        for nome, rx in BLOQUEIOS:
            if rotulo == "canal oficial" and nome not in ("CPF", "marcação interna", "valor em dinheiro"):
                continue
            alvo = texto
            if nome == "dado de saúde":
                alvo = LAUDO_DO_PROCESSO.sub(" ", BENEFICIOS.sub(" ", texto))
            achados = list(dict.fromkeys(m.group(0) for m in rx.finditer(alvo)))
            if achados:
                bloqueios.append(f"{nome} em '{rotulo}': " + ", ".join(f'"{a}"' for a in achados) + DICA.get(nome, ""))
        if rotulo != "canal oficial":
            if TELEFONE.search(texto) or EMAIL.search(texto):
                bloqueios.append(f"telefone ou e-mail fora do campo do canal oficial, em '{rotulo}'")
    nome = str(g(d, "cliente", "primeiro_nome")).strip()
    if len(nome.split()) > 1:
        avisos.append(f"o nome '{nome}' tem mais de uma palavra: a página leva só o primeiro nome")
    # trabalho do escritório
    tempo = g(d, "linha_do_tempo", padrao=[])
    do_escritorio = [i for i in tempo if ORIGENS.get(str(g(i, "origem")).strip().lower(), "") == "escritorio"]
    if tempo and not do_escritorio:
        avisos.append("a linha do tempo não mostra nenhum trabalho do escritório: inclua o que foi feito e não aparece no processo")
    for i in tempo:
        if not ler_data(g(i, "data")):
            avisos.append(f"data da linha do tempo não reconhecida: '{g(i, 'data')}' (use AAAA-MM-DD)")
        elif ler_data(g(d, "atualizado_em")) and ler_data(g(i, "data")) > ler_data(g(d, "atualizado_em")):
            avisos.append(f"a linha do tempo tem data depois da atualização ({mostrar_data(g(i, 'data'))}): o que ainda não aconteceu vai em próximos passos")
    estados = [ESTADOS_ETAPA.get(str(g(e, "estado")).strip().lower()) for e in g(d, "etapas", padrao=[])]
    if None in estados:
        avisos.append("estado de etapa não reconhecido (use feito, atual ou depois)")
    if estados.count("atual") != 1:
        avisos.append(f"a barra de etapas precisa de exatamente uma etapa 'atual' (tem {estados.count('atual')})")
    # glossário x texto
    corpo = " ".join(t for r, t in textos_da_pagina(d) if r != "glossário").lower()
    termos = [str(g(i, "termo")).strip() for i in g(d, "glossario", padrao=[])]
    for t in termos:
        if t and t.lower() not in corpo:
            avisos.append(f"o glossário explica '{t}', que não aparece no texto da página")
    sem_explicacao = []
    termos_l = " ".join(termos).lower()
    for t in TERMOS_TECNICOS:
        if re.search(r"\b" + re.escape(t) + r"\b", corpo) and t not in termos_l:
            sem_explicacao.append(t)
    if sem_explicacao:
        avisos.append("termos que aparecem sem estar no glossário: " + ", ".join(sorted(set(sem_explicacao))))
    if not g(d, "depende_de_voce", padrao=[]):
        avisos.append("nada em 'o que depende de você': a página vai dizer que, por enquanto, nada depende do cliente")
    if not g(d, "glossario", padrao=[]):
        avisos.append("glossário vazio")
    n_fiz = len(g(d, "o_que_ja_fizemos", padrao=[]) or [])
    if n_fiz and not 3 <= n_fiz <= 5:
        avisos.append(f"'o que já fizemos por você' tem {n_fiz} itens: o topo da página leva de 3 a 5")
    if not n_fiz:
        avisos.append("'o que já fizemos por você' vazio: usei os últimos itens do trabalho do escritório da linha do tempo")
    pa = str(g(d, "proxima_atualizacao")).strip()
    if not pa:
        avisos.append("sem data da próxima atualização da página: a página diz 'quando houver novidade no caso'")
    elif not ler_data(pa):
        avisos.append(f"data da próxima atualização não reconhecida: '{pa}' (use AAAA-MM-DD)")
    elif ler_data(g(d, "atualizado_em")) and ler_data(pa) < ler_data(g(d, "atualizado_em")):
        avisos.append("a próxima atualização está antes da data desta atualização")
    if not str(g(d, "escritorio", "telefone_oficial")).strip() and not str(g(d, "escritorio", "whatsapp_oficial")).strip():
        avisos.append("sem telefone nem WhatsApp do escritório: a página mostra só o canal oficial em texto")
    return bloqueios, avisos


# ---------------------------------------------------------------- cores e fontes

def cor_valida(valor, padrao):
    v = str(valor or "").strip()
    if re.fullmatch(r"#[0-9a-fA-F]{6}", v):
        return v.lower()
    if re.fullmatch(r"#[0-9a-fA-F]{3}", v):
        return "#" + "".join(c * 2 for c in v[1:]).lower()
    return padrao


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def hexa(r, g_, b):
    return "#%02x%02x%02x" % (round(r), round(g_), round(b))


def misturar(h, com, t):
    a, b = rgb(h), rgb(com)
    return hexa(*[a[i] + (b[i] - a[i]) * t for i in range(3)])


def luminancia(h):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g_, b = rgb(h)
    return 0.2126 * canal(r) + 0.7152 * canal(g_) + 0.0722 * canal(b)


def texto_sobre(h):
    return "#14181f" if luminancia(h) > 0.4 else "#ffffff"


def versao_escura(h):
    """Para o modo escuro: clareia cores escuras, mantém as claras."""
    if luminancia(h) < 0.18:
        return misturar(h, "#ffffff", 0.35)
    return h


def faixa_escura(h):
    """A faixa do topo no modo escuro: a cor da marca um pouco mais escura."""
    return misturar(h, "#000000", 0.25) if luminancia(h) > 0.05 else misturar(h, "#ffffff", 0.08)


def fonte_valida(valor, padrao):
    v = str(valor or "").strip()
    return v if re.fullmatch(r"[A-Za-z0-9 ]{2,40}", v) else padrao


def pilha(fonte):
    return f"'{fonte}'" + (SERIF if fonte.lower() in FONTES_SERIFADAS else SANS)


def link_fontes(f1, f2):
    familias = []
    for f in dict.fromkeys([f1, f2]):
        familias.append("family=" + f.replace(" ", "+") + ":wght@400;600;700")
    url = "https://fonts.googleapis.com/css2?" + "&".join(familias) + "&display=swap"
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{html.escape(url)}">')


def logo_html(valor, base, nome):
    v = str(valor or "").strip()
    if v:
        p = Path(v)
        if not p.is_absolute():
            p = (base / p).resolve()
        tipos = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".svg": "image/svg+xml", ".webp": "image/webp"}
        if p.exists() and p.suffix.lower() in tipos and p.stat().st_size <= 400_000:
            dados = base64.b64encode(p.read_bytes()).decode("ascii")
            return f'<img src="data:{tipos[p.suffix.lower()]};base64,{dados}" alt="">', None
        return None, f"logo não usado ('{v}'): precisa ser .png, .jpg, .svg ou .webp, até 400 KB, no caminho indicado"
    iniciais = "".join(w[0] for w in re.findall(r"[A-Za-zÀ-ú]+", nome) if w.lower() not in {"de", "da", "do", "e"})[:2]
    return f'<span class="monograma" aria-hidden="true">{html.escape(iniciais.upper() or "·")}</span>', None


# ---------------------------------------------------------------- montagem

def e(t):
    return html.escape(str(t or "").strip(), quote=True)


def paragrafos(t):
    partes = [p.strip() for p in re.split(r"\n\s*\n|\\n\\n", str(t or "")) if p.strip()]
    return "\n".join(f"<p>{e(p)}</p>" for p in partes)


def montar(d, modelo, base):
    avisos_extra = []
    iv = g(d, "identidade_visual", padrao={}) or {}
    marca = cor_valida(g(iv, "cor_principal"), COR_MARCA_PADRAO)
    destaque = cor_valida(g(iv, "cor_destaque"), COR_DESTAQUE_PADRAO)
    if str(g(iv, "cor_principal")).strip() and marca == COR_MARCA_PADRAO and g(iv, "cor_principal").lower() != COR_MARCA_PADRAO:
        avisos_extra.append("cor principal fora do formato #RRGGBB: usei a cor padrão")
    f_tit = fonte_valida(g(iv, "fonte_titulos"), FONTE_TITULOS_PADRAO)
    f_txt = fonte_valida(g(iv, "fonte_texto"), FONTE_TEXTO_PADRAO)
    marca_esc = faixa_escura(marca)
    logo, aviso_logo = logo_html(g(iv, "logo"), base, g(d, "escritorio", "nome"))
    if aviso_logo:
        avisos_extra.append(aviso_logo)
        logo, _ = logo_html("", base, g(d, "escritorio", "nome"))

    etapas = g(d, "etapas", padrao=[])
    linhas_etapas, atual_n = [], 0
    for n, et in enumerate(etapas, 1):
        est = ESTADOS_ETAPA.get(str(g(et, "estado")).strip().lower(), "depois")
        if est == "atual":
            atual_n = n
        cur = ' aria-current="step"' if est == "atual" else ""
        linhas_etapas.append(f'      <li class="{est}"{cur}>{e(g(et, "nome"))}'
                             f'<span class="etapa-estado">{ROTULO_ETAPA[est]}</span></li>')
    etapa_txt = (f"Etapa {atual_n} de {len(etapas)}" if atual_n else f"{len(etapas)} etapas")

    tempo = sorted(g(d, "linha_do_tempo", padrao=[]),
                   key=lambda i: ler_data(g(i, "data")) or date.min, reverse=True)
    itens_tempo = []
    for i in tempo:
        origem = ORIGENS.get(str(g(i, "origem")).strip().lower(), "processo")
        aparece = str(g(i, "aparece_no_processo")).strip().lower()
        selo = {"escritorio": "Trabalho do escritório", "processo": "No processo", "voce": "Com você"}[origem]
        nota = ""
        if origem == "escritorio" and aparece in ("", "nao", "não", "false", "0", "no"):
            nota = '\n        <p class="nota-oculto">Este trabalho não aparece no site do tribunal.</p>'
        itens_tempo.append(
            f'      <li class="{origem}">\n'
            f'        <time class="quando" datetime="{e(ler_data(g(i, "data")) or "")}">{e(mostrar_data(g(i, "data")))}</time>'
            f'<span class="selo {origem}">{selo}</span>\n'
            f'        <h3>{e(g(i, "titulo"))}</h3>\n'
            f'        {paragrafos(g(i, "texto"))}{nota}\n'
            f'      </li>')

    passos = []
    for i in g(d, "proximos_passos", padrao=[]):
        passos.append(f'      <li><span class="quando">{e(mostrar_data(g(i, "quando")) or "a seguir")}</span>'
                      f'<div>{e(g(i, "texto"))}</div></li>')

    voce = []
    for i in g(d, "depende_de_voce", padrao=[]):
        ate = mostrar_data(g(i, "ate"))
        ate_txt = f' <span class="ate">até {e(ate)}</span>' if ate and ate.lower() not in ("-", "sem data") else ""
        voce.append(f'      <li><span class="caixa" aria-hidden="true"></span><div>{e(g(i, "texto"))}{ate_txt}</div></li>')
    if not voce:
        voce.append('      <li><span class="caixa" aria-hidden="true"></span><div class="vazio">Por enquanto, nada. '
                    'Se precisarmos de alguma coisa, a gente avisa.</div></li>')

    glos = []
    for i in g(d, "glossario", padrao=[]):
        glos.append(f'      <dt>{e(g(i, "termo"))}</dt><dd>{e(g(i, "explicacao"))}</dd>')
    if not glos:
        glos.append('      <dt>Sem termos técnicos</dt><dd>Esta página não usa palavras do processo que precisem de explicação.</dd>')

    fizemos = [str(t).strip() for t in (g(d, "o_que_ja_fizemos", padrao=[]) or []) if str(t).strip()]
    if not fizemos:
        fizemos = [str(g(i, "titulo")) for i in tempo
                   if ORIGENS.get(str(g(i, "origem")).strip().lower()) == "escritorio"][:5]
    fizemos = fizemos[:5]
    itens_fizemos = "\n".join(f"      <li>{e(t)}</li>" for t in fizemos) or "      <li>Começamos a cuidar do seu caso.</li>"
    tam = str(g(iv, "tamanho_do_texto")).strip().lower()
    tam = "grande" if tam in ("grande", "maior", "sim") else "normal"
    zap = str(g(d, "escritorio", "whatsapp_oficial")).strip()
    digitos = re.sub(r"\D", "", zap)
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    link_zap = f"https://wa.me/{digitos}" if len(digitos) >= 12 else ""
    pa = str(g(d, "proxima_atualizacao")).strip()
    area = str(g(d, "caso", "area")).strip()
    nome = str(g(d, "cliente", "primeiro_nome")).strip().split(" ")[0]
    trocas = {
        "TITULO_ABA": e(f"Caso de {nome}"),
        "DESCRICAO": e(f"Página do caso de {nome}: onde estamos, o que foi feito e os próximos passos."),
        "FONTES_LINK": link_fontes(f_tit, f_txt),
        "COR_MARCA": marca, "COR_MARCA_TEXTO": texto_sobre(marca),
        "COR_DESTAQUE": destaque,
        "COR_MARCA_ESCURO": marca_esc, "COR_MARCA_TEXTO_ESCURO": texto_sobre(marca_esc),
        "COR_DESTAQUE_ESCURO": versao_escura(destaque),
        "FONTE_TITULOS": pilha(f_tit), "FONTE_TEXTO": pilha(f_txt),
        "LOGO": logo,
        "ESCRITORIO": e(g(d, "escritorio", "nome")),
        "PRIMEIRO_NOME": e(nome),
        "TIPO_DE_CASO": e(g(d, "caso", "tipo")),
        "AREA": " · " + e(area) if area else "",
        "ATUALIZADO_EM": e(mostrar_data(g(d, "atualizado_em"))),
        "PROXIMA_ATUALIZACAO": e(mostrar_data(pa) if pa else "quando houver novidade no caso"),
        "O_QUE_JA_FIZEMOS": itens_fizemos,
        "TAMANHO_DO_TEXTO": tam,
        "BOTAO_TEXTO_SINAL": "A-" if tam == "grande" else "A+",
        "BOTAO_TEXTO_ROTULO": " letra normal" if tam == "grande" else " letra maior",
        "BOTAO_TEXTO_ATIVO": "sim" if tam == "grande" else "nao",
        "TELEFONE_OFICIAL": e(g(d, "escritorio", "telefone_oficial")),
        "WHATSAPP_OFICIAL": e(zap),
        "WHATSAPP_LINK": e(link_zap),
        "FASE_TITULO": e(g(d, "fase", "titulo")),
        "FASE_EXPLICACAO": paragrafos(g(d, "fase", "explicacao")),
        "ETAPAS": "\n".join(linhas_etapas),
        "ETAPA_ATUAL_TEXTO": e(etapa_txt),
        "LINHA_DO_TEMPO": "\n".join(itens_tempo),
        "PROXIMOS_PASSOS": "\n".join(passos),
        "DEPENDE_DE_VOCE": "\n".join(voce),
        "GLOSSARIO": "\n".join(glos),
        "VOLTAMOS_A_FALAR": paragrafos(g(d, "voltamos_a_falar")),
        "CANAL_OFICIAL": e(g(d, "escritorio", "canal_oficial")),
        "HORARIO": e(g(d, "escritorio", "horario") or "conforme combinado com o escritório"),
        "ASSINATURA": e(g(d, "escritorio", "assinatura") or g(d, "escritorio", "nome")),
    }
    saida = re.sub(r"<!-- MODELO DA PÁGINA DO CASO.*?-->\n?", "", modelo, flags=re.S)
    for k, v in trocas.items():
        saida = saida.replace("{{" + k + "}}", v)
    sobrou = re.findall(r"\{\{[A-Z_]+\}\}", saida)
    if sobrou:
        raise ErroDeEntrada("o modelo tem campos que o script não conhece: " + ", ".join(sorted(set(sobrou))))
    resumo = {"etapa": etapa_txt, "tempo": tempo, "fontes": (f_tit, f_txt), "cores": (marca, destaque), "letra": tam}
    return saida, avisos_extra, resumo


def lista_do_que_esta(d, resumo, avisos, saida):
    tempo = resumo["tempo"]
    n_esc = sum(1 for i in tempo if ORIGENS.get(str(g(i, "origem")).strip().lower()) == "escritorio")
    datas = [ler_data(g(i, "data")) for i in tempo if ler_data(g(i, "data"))]
    periodo = f", de {min(datas).strftime('%d/%m/%Y')} a {max(datas).strftime('%d/%m/%Y')}" if datas else ""
    linhas = [
        "LISTA DO QUE ESTÁ NA PÁGINA (mostre ao advogado e peça o ok antes de publicar)",
        f"- Para: {str(g(d, 'cliente', 'primeiro_nome')).split(' ')[0]} (só o primeiro nome)",
        f"- Escritório: {g(d, 'escritorio', 'nome')}",
        f"- Tipo de caso: {g(d, 'caso', 'tipo')}" + (f" · {g(d, 'caso', 'area')}" if g(d, 'caso', 'area') else ""),
        f"- Atualizada em: {mostrar_data(g(d, 'atualizado_em'))} · próxima atualização: {mostrar_data(g(d, 'proxima_atualizacao')) or 'quando houver novidade'}",
        f"- Onde estamos: {g(d, 'fase', 'titulo')} ({resumo['etapa']})",
        f"- Linha do tempo: {len(tempo)} itens ({n_esc} do trabalho do escritório){periodo}",
    ]
    for i in tempo:
        linhas.append(f"    {mostrar_data(g(i, 'data'))} · {g(i, 'titulo')}")
    linhas.append(f"- Próximos passos: {len(g(d, 'proximos_passos', padrao=[]))}")
    for i in g(d, "proximos_passos", padrao=[]):
        linhas.append(f"    {mostrar_data(g(i, 'quando')) or 'a seguir'} · {g(i, 'texto')}")
    voce = g(d, "depende_de_voce", padrao=[])
    linhas.append(f"- O que depende do cliente: {len(voce) or 'nada por enquanto'}")
    for i in voce:
        linhas.append(f"    {g(i, 'texto')}" + (f" (até {mostrar_data(g(i, 'ate'))})" if g(i, 'ate') else ""))
    termos = [str(g(i, 'termo')) for i in g(d, 'glossario', padrao=[])]
    linhas.append(f"- Glossário: {', '.join(termos) if termos else 'vazio'}")
    linhas.append(f"- Quando voltamos a falar: {' '.join(str(g(d, 'voltamos_a_falar')).split())}")
    linhas.append("- O que já fizemos (topo): " + ("; ".join(str(t) for t in (g(d, 'o_que_ja_fizemos', padrao=[]) or []))
                                                  or "vazio, usei o trabalho do escritório da linha do tempo"))
    linhas.append(f"- Canal oficial: {g(d, 'escritorio', 'canal_oficial')} · Telefone: {g(d, 'escritorio', 'telefone_oficial') or 'não informado'} · WhatsApp: {g(d, 'escritorio', 'whatsapp_oficial') or 'não informado'} · Horário: {g(d, 'escritorio', 'horario')}")
    linhas.append(f"- Visual: cores {resumo['cores'][0]} e {resumo['cores'][1]}, fontes {resumo['fontes'][0]} e {resumo['fontes'][1]}, modo claro e escuro")
    if resumo["letra"] == "grande":
        linhas.append("- Tamanho da letra: grande desde a abertura (o botão mostra \"A- letra normal\" e volta ao tamanho normal; tocando de novo, \"A+ letra maior\")")
    else:
        linhas.append("- Tamanho da letra: normal (o botão mostra \"A+ letra maior\" e aumenta a página; tocando de novo, \"A- letra normal\")")
    linhas.append("- Conferência dos dados: nenhum CPF, número de processo ou de benefício, valor, endereço, "
                  "dado de saúde, empresa da outra parte, promessa ou marcação interna encontrados pelo script. "
                  "Nome de pessoa da outra parte o script não reconhece: confira na leitura.")
    if avisos:
        linhas.append("- Avisos para conferir:")
        linhas += [f"    {a}" for a in avisos]
    if saida:
        linhas.append(f"- Arquivo gerado: {saida}")
    return "\n".join(linhas)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera a página do caso a partir de um .md ou .json.")
    ap.add_argument("entrada", help="conteúdo do caso (.md ou .json)")
    ap.add_argument("saida", nargs="?", help="arquivo .html a gravar")
    ap.add_argument("--modelo", default=str(MODELO_PADRAO), help="modelo HTML (padrão: assets/pagina-modelo.html)")
    ap.add_argument("--lista", help="grava também a lista do que está na página neste arquivo")
    ap.add_argument("--so-conferir", action="store_true", help="só confere os dados, sem gerar o HTML")
    a = ap.parse_args(argv)
    try:
        if not a.so_conferir and not a.saida:
            raise ErroDeEntrada("diga onde gravar o HTML (segundo argumento) ou use --so-conferir")
        d = ler_entrada(a.entrada)
        falta = campos_obrigatorios(d)
        if falta:
            raise ErroDeEntrada("faltam campos obrigatórios: " + "; ".join(falta))
        bloqueios, avisos = conferir(d)
        if bloqueios:
            print("PÁGINA NÃO GERADA. A conferência encontrou o que não pode ir para o cliente:", file=sys.stderr)
            for b in dict.fromkeys(bloqueios):
                print(f" - {b}", file=sys.stderr)
            print("Tire ou reescreva esses trechos no conteúdo do caso e rode de novo.", file=sys.stderr)
            return 1
        modelo_p = Path(a.modelo)
        if not modelo_p.exists():
            raise ErroDeEntrada(f"não encontrei o modelo HTML: {modelo_p}")
        pagina, avisos_extra, resumo = montar(d, modelo_p.read_text(encoding="utf-8"), Path(a.entrada).resolve().parent)
        avisos += avisos_extra
        if not a.so_conferir:
            Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
            Path(a.saida).write_text(pagina, encoding="utf-8")
        lista = lista_do_que_esta(d, resumo, avisos, None if a.so_conferir else a.saida)
        print(lista)
        if a.lista:
            Path(a.lista).write_text(lista + "\n", encoding="utf-8")
        return 0
    except ErroDeEntrada as ex:
        print(f"ERRO: {ex}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
