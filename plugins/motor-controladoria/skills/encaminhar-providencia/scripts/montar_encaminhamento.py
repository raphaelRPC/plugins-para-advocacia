#!/usr/bin/env python3
"""Monta o encaminhamento de uma providência já decidida, a partir da linha do prazo.

Parte da habilidade encaminhar-providencia do motor-controladoria.

Saídas possíveis (uma ou mais na mesma rodada):
  --peca <tipo>          pedido de peça na entrada do motor-juridico, no formato
                         de rotina-juridica/assets/tarefa-agendada.md, com
                         prazo_interno igual à data de segurança;
  --documento "<nome>"   tarefa de documento na entrada do motor-experiencia
                         (checklist-de-documentos);
  --aviso <assunto>      aviso na entrada do motor-experiencia: audiencia,
                         pericia ou sessao (preparar-o-cliente), decisao ou
                         valor (status-para-o-cliente). Notícia ruim, parcial
                         ou a confirmar vira roteiro de ligação, nunca mensagem;
  --interna "<tarefa>"   tarefa interna para o responsável.

Nada é encaminhado sem --decidido-por (quem decidiu, dito pela própria pessoa
na conversa). Prazo sugerido só com --provisorio. Sem --gravar, só mostra o
texto e o caminho (para copiar quando o plugin irmão não está instalado).

Uso:
  python3 montar_encaminhamento.py prazos.csv --id PZ-2026-0001 --decidido-por "advogada"
      [--peca recurso-inominado] [--documento "relatório médico atualizado" --entregar-ate AAAA-MM-DD]
      [--aviso decisao --noticia ruim] [--interna "texto"] [--responsavel nome]
      [--publicacoes publicacoes.csv] [--processos processos.csv] [--area previdenciario]
      [--trecho "texto literal do ato"] [--motivo "por que o caso precisa"]
      [--escritorio escritorio] [--treino] [--gravar] [--de-novo] [--provisorio]
      [--hoje AAAA-MM-DD] [--hora HHMM] [--json]

Códigos de saída: 0 ok; 1 erro ou recusa (sem decisão, prazo sugerido sem
--provisorio, prazo fechado, arquivo ou coluna que falta, id que não existe).
Python 3.9+, só biblioteca padrão.
"""

import argparse
import codecs
import csv
import datetime as dt
import glob
import io
import json
import os
import re
import sys
import unicodedata

COLUNAS_OBRIGATORIAS = ["id", "codigo_caso", "tipo", "providencia", "vencimento",
                        "data_seguranca", "responsavel", "status"]
STATUS_VALIDOS = {"conferido", "agendado"}
STATUS_FECHADOS = {"cumprido", "perdido", "cancelado"}
ASSUNTOS = {
    "audiencia": "preparar-o-cliente", "pericia": "preparar-o-cliente", "sessao": "preparar-o-cliente",
    "documento": "checklist-de-documentos", "decisao": "status-para-o-cliente", "valor": "status-para-o-cliente",
}
NOTICIAS_LIGACAO = {"ruim", "parcial", "a-confirmar"}
RE_CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")


class Falha(Exception):
    pass


def sem_acento(texto):
    nfkd = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def chave(texto):
    return sem_acento(texto).strip().lower()


def limpar(texto):
    """Tira número de processo e CPF do que sai da controladoria."""
    t = RE_CNJ.sub("[PROCESSO]", texto or "")
    return RE_CPF.sub("[DOC]", t)


def uma_linha(texto):
    return re.sub(r"\s+", " ", limpar(texto)).strip()


class Planilha:
    def __init__(self, caminho, nome):
        if not os.path.isfile(caminho):
            raise Falha("Não achei o %s em %s. Confira o caminho." % (nome, caminho))
        bruto = open(caminho, "rb").read()
        self.caminho = caminho
        self.bom = bruto.startswith(codecs.BOM_UTF8)
        texto = None
        for enc in ("utf-8-sig", "cp1252"):
            try:
                texto = bruto.decode(enc)
                self.encoding = enc
                break
            except UnicodeDecodeError:
                continue
        if texto is None or not texto.strip():
            raise Falha("O %s (%s) está vazio: falta ao menos a linha de títulos." % (nome, caminho))
        self.nova_linha = "\r\n" if "\r\n" in texto else "\n"
        primeira = texto.splitlines()[0]
        self.sep = ";" if primeira.count(";") > primeira.count(",") else ","
        linhas = list(csv.reader(io.StringIO(texto), delimiter=self.sep))
        self.titulos = [t.strip() for t in linhas[0]]
        self.chaves = [chave(t) for t in self.titulos]
        self.linhas = []
        for crua in linhas[1:]:
            if not any(c.strip() for c in crua):
                continue
            self.linhas.append({k: (crua[i].strip() if i < len(crua) else "") for i, k in enumerate(self.chaves)})

    def exigir(self, colunas, nome):
        faltam = [c for c in colunas if c not in self.chaves]
        if faltam:
            raise Falha("Faltam colunas no %s: %s. A linha de títulos certa está em docs/prazos.md." % (nome, ", ".join(faltam)))

    def gravar(self):
        saida = io.StringIO()
        escritor = csv.writer(saida, delimiter=self.sep, lineterminator=self.nova_linha)
        escritor.writerow(self.titulos)
        for r in self.linhas:
            escritor.writerow([r.get(k, "") for k in self.chaves])
        enc = "utf-8" if self.encoding == "utf-8-sig" else self.encoding
        dados = saida.getvalue().encode(enc)
        if self.bom:
            dados = codecs.BOM_UTF8 + dados
        temp = self.caminho + ".tmp"
        with open(temp, "wb") as f:
            f.write(dados)
        os.replace(temp, self.caminho)


def ler_data(texto, campo):
    t = (texto or "").strip().split(" ")[0]
    if not t:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(t, fmt).date()
        except ValueError:
            continue
    raise Falha("Data que não entendi em %s: %r. Use AAAA-MM-DD ou DD/MM/AAAA." % (campo, texto))


def proximo_dia_util(d):
    d = d + dt.timedelta(days=1)
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def ler_hora(texto):
    t = chave(texto)
    m = re.search(r"(?<![\d/-])([01]?\d|2[0-3])\s*(?:h(?:oras?|s)?(?:\s*([0-5]\d))?(?![a-z\d])|:([0-5]\d)(?!\d))", t)
    if not m:
        return ""
    return "%02dh%s" % (int(m.group(1)), m.group(2) or m.group(3) or "00")


def ler_modalidade(texto):
    t = chave(texto)
    if re.search(r"video|virtual|telepresencial|on-?line|link|https?://", t):
        return "videoconferência"
    if re.search(r"presencial|forum|sala \w|endereco|predio|consultorio", t):
        return "presencial"
    return ""


def nome_de_peca(texto):
    return re.sub(r"[^a-z0-9]+", "-", chave(texto)).strip("-")


def ja_encaminhado(pasta_entrada, id_prazo, sufixo):
    padrao = "*-controladoria-%s%s.md" % (id_prazo.lower(), sufixo)
    achados = glob.glob(os.path.join(pasta_entrada, padrao))
    achados += glob.glob(os.path.join(pasta_entrada, "lidos", "*", padrao))
    return sorted(achados)


# ----------------------------------------------------------- os textos

def texto_pedido_de_peca(r, a, pub, area, decisao, provisorio):
    if provisorio:
        conferencia = ("prazo provisório, ainda sem a dupla conferência: vale a data mais cedo; não é prazo valendo "
                       "e não entra na agenda até ser conferido")
    else:
        conferencia = "prazo conferido (%s)" % (r.get("conferido_por") or "[A CONFIRMAR]")
    partes = [
        r["id"],
        uma_linha(pub.get("resumo", "")) or uma_linha(r.get("providencia", "")),
        "disponibilizada %s" % pub["disponibilizada_em"] if pub.get("disponibilizada_em") else "",
        "fatal %s" % r.get("vencimento", ""),
        conferencia,
        decisao,
    ]
    if a.noticia in NOTICIAS_LIGACAO:
        partes.append("o cliente ainda vai receber a ligação do advogado; recorrer ou não é conversa com ele")
    observacao = "; ".join(p for p in partes if p)
    documentos = "casos/%s/documentos/" % r["codigo_caso"]
    if pub.get("teor"):
        documentos += " e o teor em 07-operacao/controladoria/%s" % pub["teor"]
    linhas = [
        "pedido: peça nova",
        "codigo_caso: %s" % r["codigo_caso"],
        "cliente_curto: %s" % (r.get("cliente_curto") or "[A CONFIRMAR]"),
        "area: %s" % area,
        "peca: %s" % nome_de_peca(a.peca),
        "origem: intimacao",
        "prazo_interno: %s" % r["data_seguranca"],
        "quem_pediu: controladoria",
        "documentos: %s" % documentos,
        "observacao: %s" % uma_linha(observacao),
    ]
    return "\n".join(linhas) + "\n"


def cabecalho_aviso(r, assunto, decisao, urgencia, extra):
    linhas = [
        "aviso: controladoria",
        "para: %s (motor-experiencia)" % ASSUNTOS[assunto],
        "codigo: %s" % r["codigo_caso"],
        "cliente_curto: %s" % (r.get("cliente_curto") or "[A CONFIRMAR]"),
        "assunto: %s" % assunto,
    ]
    linhas += extra
    linhas += [
        "prazo: %s, %s%s" % (r["id"], chave(r.get("status")), " (%s)" % r["conferido_por"] if r.get("conferido_por") else ""),
        "decidido_por: %s" % decisao.replace("decidido por ", "", 1),
        "urgencia: %s" % urgencia,
    ]
    return "\n".join(linhas)


def texto_aviso_compromisso(r, a, assunto, decisao, urgencia):
    obs = r.get("observacao", "")
    hora = ler_hora(obs)
    modal = ler_modalidade(obs)
    link = re.search(r"https?://[^\s;,)]+", obs)
    extra = [
        "compromisso: %s" % assunto,
        "descricao: %s" % uma_linha(r.get("providencia")),
        "data: %s" % r["vencimento"],
        "hora: %s" % (hora or "[A CONFIRMAR]"),
        "modalidade: %s" % (modal or "[A CONFIRMAR]"),
        "local_ou_link: %s" % (link.group(0) if link else ("[A CONFIRMAR: link da sala virtual, quando juntado aos autos]" if modal == "videoconferência" else "[A CONFIRMAR]")),
        "para_a_carteira: proximo_compromisso = %s; data_compromisso = %s; motivo_proximo_contato = compromisso" % (
            {"sessao": "audiencia"}.get(assunto, assunto), r["vencimento"]),
    ]
    corpo = [cabecalho_aviso(r, assunto, decisao, urgencia, extra), ""]
    if a.trecho:
        corpo += ["## O que o ato diz (trecho literal)", "", "> " + uma_linha(a.trecho), ""]
    corpo += ["## Para a preparação (interno, não é texto para o cliente)", ""]
    corpo.append("- A orientação e os lembretes saem pela preparar-o-cliente, na cadência da ficha da experiência, e só depois de uma pessoa aprovar na fila.")
    if modal == "videoconferência":
        corpo.append("- Por vídeo: combinar com o cliente o teste do link, da câmera e do áudio antes do dia, e onde ele vai estar na hora.")
    if assunto == "audiencia":
        corpo.append("- Testemunhas não são preparadas pela IA: aviso de data e local, e a conversa é do advogado.")
    if assunto == "pericia":
        corpo.append("- Quesitos e assistente técnico são do advogado [CONFERIR] no processo; ao cliente, só o que levar e como vai ser.")
    corpo.append("- Hora, local e link vêm do ato; o que não veio fica para confirmar antes de qualquer mensagem.")
    return "\n".join(corpo) + "\n"


def texto_aviso_documento(r, a, decisao, urgencia):
    seg = r["data_seguranca"]
    entregar = a.entregar_ate or ("[A DEFINIR: até quando o escritório precisa receber, antes de %s]" % seg)
    extra = [
        "documento: %s" % uma_linha(a.documento),
        "prazo_do_processo: sim, data de segurança %s, fatal %s%s" % (seg, r["vencimento"], " (provisório)" if chave(r.get("status")) == "sugerido" else ""),
        "entregar_ate: %s" % entregar,
        "por_que: %s" % uma_linha(a.motivo or "o processo pediu este documento; o prazo do escritório depende dele"),
        "para_a_carteira: proximo_compromisso = prazo-do-cliente; data_compromisso = %s; motivo_proximo_contato = documento" % (a.entregar_ate or seg),
    ]
    corpo = [cabecalho_aviso(r, "documento", decisao, urgencia, extra), ""]
    if a.trecho:
        corpo += ["## O que o ato diz (trecho literal)", "", "> " + uma_linha(a.trecho), ""]
    corpo += [
        "## Para o pedido ao cliente (interno, não é texto para o cliente)",
        "",
        "- O pedido e a cobrança saem pela checklist-de-documentos, com prazo do processo: o advogado acompanha a cobrança.",
        "- Começar a pedir hoje: o prazo corre enquanto o documento não chega.",
        "- Documento de saúde, de criança ou de processo em segredo: só pelo canal oficial; o controle guarda o nome do documento, nunca o conteúdo.",
        "- Se o cliente disser que não tem o documento, a decisão volta para o advogado antes da data de segurança.",
    ]
    return "\n".join(corpo) + "\n"


def texto_aviso_noticia(r, a, assunto, pub, decisao, urgencia, peca_pedida):
    noticia = a.noticia or "a-confirmar"
    resumo = uma_linha(pub.get("resumo", "")) or uma_linha(r.get("providencia", ""))
    disp = pub.get("disponibilizada_em", "")
    ligacao = noticia in NOTICIAS_LIGACAO
    extra = [
        "noticia: %s" % noticia,
        "caminho: %s" % ("ligação do advogado antes de qualquer mensagem" if ligacao
                         else "mensagem pela status-para-o-cliente, lida pelo advogado antes de sair"),
    ]
    if ligacao:
        extra.append("mensagem_ao_cliente: nenhuma antes da ligação; o registro por escrito só depois dela, pela status-para-o-cliente")
        extra.append("quem_liga: %s" % (r.get("responsavel") or "[A PREENCHER]"))
    extra += [
        "o_que_aconteceu: %s%s" % (resumo, " (disponibilizada em %s)" % disp if disp else ""),
        "prazo_que_corre: %s, data de segurança %s, fatal %s" % (uma_linha(r.get("providencia")), r["data_seguranca"], r["vencimento"]),
    ]
    if peca_pedida:
        extra.append("o_que_o_escritorio_faz: pedido de peça ao jurídico (%s); a decisão final é conversa do advogado com o cliente" % nome_de_peca(peca_pedida))
    if assunto == "valor":
        extra.append("cuidado: valor e data de pagamento só conferidos pelo advogado; nunca prometer data")
    corpo = [cabecalho_aviso(r, assunto, decisao, urgencia, extra), ""]
    if ligacao:
        frase = "[A DEFINIR PELO ADVOGADO: uma frase, sem termo técnico]"
        if "improced" in chave(resumo):
            frase = "Sugestão para ajustar: \"O juiz decidiu o seu processo e, desta vez, não deu razão ao nosso pedido.\""
        corpo += [
            "## Roteiro de ligação (rascunho interno, H: quem liga é o advogado)",
            "",
            "1. O que aconteceu: %s%s." % (resumo, ", disponibilizada em %s" % disp if disp else ""),
            "2. Como dizer: %s" % frase,
            "3. O que isso significa para o cliente: [A DEFINIR PELO ADVOGADO]",
            "4. O que dá para fazer: [A DEFINIR PELO ADVOGADO]. Prazo processual para decidir: a peça precisa estar pronta até %s (data de segurança); a conversa com o cliente vem antes." % r["data_seguranca"],
            "5. Perguntas prováveis e o que não dizer: o roteiro completo da status-para-o-cliente (assets/roteiro-de-ligacao.md), se instalada.",
            "6. Depois da ligação: a linha `ligacao` no histórico do cliente; só então o registro por escrito.",
        ]
    else:
        corpo += [
            "## Para a mensagem (interno)",
            "",
            "- A status-para-o-cliente escreve nas quatro partes (o que aconteceu, o que significa, o que vem, quando volta a falar), sem prever resultado nem data de decisão.",
        ]
    return "\n".join(corpo) + "\n"


# ------------------------------------------------------------ o trabalho

def montar(a):
    if not a.decidido_por or not a.decidido_por.strip():
        raise Falha("Nada é encaminhado antes de a pessoa decidir. Pergunte a quem decide a providência "
                    "(ficha: quem_decide_providencia) e passe --decidido-por com o nome que ela disser na conversa.")
    if not (a.peca or a.documento or a.aviso or a.interna):
        raise Falha("Diga o que encaminhar: --peca, --documento, --aviso ou --interna.")
    if a.aviso and a.aviso not in ASSUNTOS:
        raise Falha("--aviso precisa ser um destes: %s." % ", ".join(sorted(ASSUNTOS)))
    if a.gravar and not a.escritorio:
        raise Falha("Para gravar, diga onde está a pasta do escritório (--escritorio escritorio).")
    pl = Planilha(a.prazos, "prazos.csv")
    pl.exigir(COLUNAS_OBRIGATORIAS, "prazos.csv")
    linha = next((r for r in pl.linhas if r["id"] == a.id), None)
    if linha is None:
        raise Falha("Não achei %s no prazos.csv." % a.id)
    status = chave(linha.get("status"))
    if status in STATUS_FECHADOS:
        raise Falha("%s está %s: prazo fechado não é encaminhado." % (a.id, status))
    provisorio = False
    if status not in STATUS_VALIDOS:
        if status == "sugerido" and a.provisorio:
            provisorio = True
        elif status == "sugerido":
            raise Falha("%s ainda está sugerido: a data não passou pela dupla conferência. Confira antes (dupla-conferencia) "
                        "ou, se a pessoa decidir adiantar o pedido, rode de novo com --provisorio (a data mais cedo vale até a conferência)." % a.id)
        else:
            raise Falha("%s com status %r: só conferido, agendado ou (com --provisorio) sugerido." % (a.id, linha.get("status")))
    if not linha.get("data_seguranca") and chave(linha.get("tipo")) not in {"audiencia", "pericia", "sessao"}:
        raise Falha("%s sem data de segurança: rode a calcular-prazo antes." % a.id)

    pub = {}
    if a.publicacoes:
        pp = Planilha(a.publicacoes, "publicacoes.csv")
        pub = next((r for r in pp.linhas if r.get("id") == linha.get("publicacao_id")), {})
    area = a.area
    if not area and a.processos:
        proc = Planilha(a.processos, "processos.csv")
        achado = next((r for r in proc.linhas if r.get("processo") == linha.get("processo")), None)
        if achado:
            area = achado.get("area", "")
    area = area or "[A CONFIRMAR]"

    hoje = ler_data(a.hoje, "--hoje") if a.hoje else dt.date.today()
    hora = a.hora or dt.datetime.now().strftime("%H%M")
    decisao = "decidido por %s, na conversa, %s %s:%s" % (a.decidido_por.strip(), hoje.isoformat(), hora[:2], hora[2:4])

    pessoa_agora = []
    limite = proximo_dia_util(hoje)
    for rotulo, campo in (("segurança", "data_seguranca"), ("fatal", "vencimento")):
        d = ler_data(linha.get(campo), campo)
        if d and d <= limite:
            pessoa_agora.append("%s %s: %s em %s (hoje ou no próximo dia útil)" % (a.id, linha.get("codigo_caso"), rotulo, d.isoformat()))
            break
    urgencia = "pessoa agora (vence hoje ou no próximo dia útil)" if pessoa_agora else "normal"

    raiz = a.escritorio or "escritorio"
    oper = os.path.join(raiz, "07-operacao", "_treino") if a.treino else os.path.join(raiz, "07-operacao")
    entrada_jur = os.path.join(oper, "juridico", "entrada")
    entrada_exp = os.path.join(oper, "experiencia", "entrada")
    base_nome = "%s-%s-controladoria-%s" % (hoje.isoformat(), hora[:4], a.id.lower())

    saidas = []
    avisos = []
    if provisorio:
        avisos.append("prazo provisório: %s ainda está sugerido; nada disto entra na agenda nem conta como prazo valendo antes "
                      "de conferido. Quando a dupla conferência mudar a data, encaminhe de novo com --de-novo" % a.id)
    if area == "[A CONFIRMAR]" and a.peca:
        avisos.append("área do caso não encontrada: passe --area ou --processos (processos.csv)")

    if a.peca:
        saidas.append({"destino": "motor-juridico", "habilidade": "rotina-juridica (entrada)", "tipo": "pedido de peça",
                       "pasta": entrada_jur, "arquivo": base_nome + ".md", "sufixo": "",
                       "texto": texto_pedido_de_peca(linha, a, pub, area, decisao, provisorio)})
    if a.documento:
        saidas.append({"destino": "motor-experiencia", "habilidade": "checklist-de-documentos", "tipo": "tarefa de documento",
                       "pasta": entrada_exp, "arquivo": base_nome + "-documento.md", "sufixo": "-documento",
                       "texto": texto_aviso_documento(linha, a, decisao, urgencia)})
    if a.aviso and a.aviso != "documento":
        assunto = a.aviso
        if assunto in {"audiencia", "pericia", "sessao"}:
            texto = texto_aviso_compromisso(linha, a, assunto, decisao, urgencia)
        else:
            texto = texto_aviso_noticia(linha, a, assunto, pub, decisao, urgencia, a.peca)
        saidas.append({"destino": "motor-experiencia", "habilidade": ASSUNTOS[assunto], "tipo": "aviso (%s)" % assunto,
                       "pasta": entrada_exp, "arquivo": base_nome + "-" + assunto + ".md", "sufixo": "-" + assunto,
                       "texto": texto})
    elif a.aviso == "documento" and not a.documento:
        raise Falha("--aviso documento precisa de --documento \"<nome do documento>\".")

    interna = ""
    if a.interna:
        quem = a.responsavel or linha.get("responsavel") or "[A PREENCHER]"
        interna = "TAREFA INTERNA%s · %s · %s · %s: %s · até %s (fatal %s) · %s" % (
            " PROVISÓRIA (prazo ainda sugerido: tarefa para a pessoa decidir, não é compromisso de agenda nem prazo valendo)"
            if provisorio else "",
            a.id, linha.get("codigo_caso"), quem, uma_linha(a.interna),
            linha.get("data_seguranca") or linha.get("vencimento"), linha.get("vencimento"), decisao)

    gravados = []
    for s in saidas:
        s["caminho"] = os.path.join(s["pasta"], s["arquivo"])
        antes = ja_encaminhado(s["pasta"], a.id, s["sufixo"]) if a.escritorio else []
        if antes and not a.de_novo:
            s["pulado"] = "já encaminhado antes (%s); não duplico. Para encaminhar de novo, use --de-novo." % ", ".join(antes)
            continue
        if a.gravar:
            os.makedirs(s["pasta"], exist_ok=True)
            if os.path.exists(s["caminho"]):
                raise Falha("Já existe %s: rode de novo com outra --hora." % s["caminho"])
            with open(s["caminho"], "w", encoding="utf-8") as f:
                f.write(s["texto"])
            gravados.append(s)

    if a.gravar and (gravados or interna):
        notas = ["%s ao %s" % (s["tipo"], s["destino"]) for s in gravados]
        if interna:
            notas.append("tarefa interna: %s" % uma_linha(a.interna))
        nota = "encaminhado em %s (%s): %s" % (hoje.isoformat(), decisao, "; ".join(notas))
        if "observacao" in linha:
            linha["observacao"] = (linha["observacao"] + "; " if linha["observacao"] else "") + nota
        if a.responsavel:
            linha["responsavel"] = a.responsavel
        if "atualizado_em" in linha:
            linha["atualizado_em"] = hoje.isoformat()
        pl.gravar()

    return {"pessoa_agora": pessoa_agora, "saidas": saidas, "interna": interna, "avisos": avisos,
            "gravou": bool(a.gravar and (gravados or interna)), "provisorio": provisorio}


def imprimir(res, gravar):
    if res["pessoa_agora"]:
        print("PESSOA AGORA:")
        for l in res["pessoa_agora"]:
            print("  - " + l)
        print()
    for s in res["saidas"]:
        print("=" * 70)
        print("%s para o %s (%s)" % (s["tipo"].upper(), s["destino"], s["habilidade"]))
        if s.get("pulado"):
            print("PULADO: " + s["pulado"])
            continue
        print(("Gravado em: " if gravar else "Copie para: ") + s["caminho"])
        print("-" * 70)
        print(s["texto"].rstrip())
    if res["interna"]:
        print("=" * 70)
        print(res["interna"])
    if res["avisos"]:
        print()
        print("Avisos:")
        for av in res["avisos"]:
            print("  ! " + av)
    if not gravar:
        print()
        print("Nada foi gravado. Com o ok da pessoa, rode de novo com --gravar --escritorio <pasta do escritório>.")
    elif res["gravou"]:
        print()
        print("prazos.csv atualizado: observacao e atualizado_em da linha.")


def main():
    p = argparse.ArgumentParser(description="Monta o pedido de peça, a tarefa de documento e o aviso de uma providência decidida.")
    p.add_argument("prazos", help="caminho do prazos.csv")
    p.add_argument("--id", required=True)
    p.add_argument("--decidido-por")
    p.add_argument("--peca")
    p.add_argument("--documento")
    p.add_argument("--entregar-ate")
    p.add_argument("--motivo")
    p.add_argument("--aviso")
    p.add_argument("--noticia", choices=["ruim", "parcial", "boa", "neutra", "a-confirmar"])
    p.add_argument("--interna")
    p.add_argument("--responsavel")
    p.add_argument("--publicacoes")
    p.add_argument("--processos")
    p.add_argument("--area")
    p.add_argument("--trecho")
    p.add_argument("--escritorio")
    p.add_argument("--treino", action="store_true")
    p.add_argument("--gravar", action="store_true")
    p.add_argument("--de-novo", action="store_true")
    p.add_argument("--provisorio", action="store_true")
    p.add_argument("--hoje")
    p.add_argument("--hora", help="HHMM, para o nome do arquivo de entrada")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.hora and not re.fullmatch(r"\d{4}", a.hora):
        print("ERRO: --hora no formato HHMM, por exemplo 1010.", file=sys.stderr)
        sys.exit(1)
    if a.aviso:
        a.aviso = chave(a.aviso)
    if a.entregar_ate:
        try:
            a.entregar_ate = ler_data(a.entregar_ate, "--entregar-ate").isoformat()
        except Falha as e:
            print("ERRO: %s" % e, file=sys.stderr)
            sys.exit(1)
    try:
        res = montar(a)
    except Falha as e:
        print("ERRO: %s" % e, file=sys.stderr)
        sys.exit(1)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        imprimir(res, a.gravar)
    sys.exit(0)


if __name__ == "__main__":
    main()
