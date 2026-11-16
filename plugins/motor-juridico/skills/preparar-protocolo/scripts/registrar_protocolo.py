#!/usr/bin/env python3
"""Registra no pecas.csv o protocolo que a pessoa já fez (motor-juridico, preparar-protocolo).

Depois que a pessoa protocolou no sistema do tribunal, o script atualiza a linha da peça:
etapa `protocolada`, protocolo_sistema, protocolo_numero, protocolo_data e atualizado_em.
E mostra a linha de trabalho do escritório para o histórico do cliente do
motor-experiencia (se instalado), sem o número do processo e com o nome da peça em
linguagem de cliente ("petição inicial", não "peticao-inicial-restabelecimento").
Registro sob _treino/: o comprovante vai para a pasta de treino (07-operacao/_treino/juridico/casos/).

Por padrão só mostra o antes e o depois. Grava só com --gravar, e guarda uma cópia do
arquivo anterior em pecas.csv.bak, na mesma pasta. Mantém o separador, o BOM e a
codificação da planilha. Só biblioteca padrão (Python 3.9+).

Só registra peça na etapa `aprovada`, com citações `verde` e dados `ok`
(docs/producao.md, regras 3 e 4). Quem aprova é o advogado; quem protocola é a pessoa.

Uso:
  python3 registrar_protocolo.py CAMINHO/pecas.csv --id P-AAAA-NNNN --sistema PJe \
    --numero "NÚMERO DO PROTOCOLO OU DO PROCESSO" --data "AAAA-MM-DD HH:MM" [--gravar]

Opções:
  --id ID           a peça (coluna id)
  --sistema TEXTO   PJe, eproc, e-SAJ, Projudi ou outro
  --numero TEXTO    o número que o sistema deu (protocolo ou processo)
  --data TEXTO      data e hora do protocolo, AAAA-MM-DD HH:MM ou DD/MM/AAAA HH:MM
  --quem TEXTO      função de quem protocolou, para a linha do histórico (padrão: a pessoa)
  --hoje AAAA-MM-DD data para atualizado_em (padrão: hoje)
  --gravar          grava a mudança no pecas.csv
  --treino          permite mexer no registro de treino (pasta _treino)

Sai com código 1 e "ERRO:" quando falta o arquivo ou uma coluna, quando a peça não existe
ou aparece duas vezes, quando não está aprovada, quando já está protocolada, quando
citações ou dados não estão ok, ou quando a data não dá para ler.
"""
import argparse
import csv
import io
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

OBRIGATORIAS = ["id", "codigo_caso", "peca", "etapa", "citacoes", "dados",
                "protocolo_sistema", "protocolo_numero", "protocolo_data", "atualizado_em"]
SISTEMAS = {"pje": "PJe", "eproc": "eproc", "e-saj": "e-SAJ", "esaj": "e-SAJ", "projudi": "Projudi"}
# nome da peça em linguagem de cliente, para a linha do histórico (o tipo técnico fica no pecas.csv)
NOMES_DE_PECA = {
    "peticao-inicial": "petição inicial",
    "peticao-inicial-restabelecimento": "petição inicial",
    "reclamacao-trabalhista": "reclamação trabalhista",
    "divorcio-consensual": "petição de divórcio consensual",
    "contestacao": "contestação",
    "replica": "réplica",
    "impugnacao": "impugnação",
    "recurso-inominado": "recurso",
    "recurso-ordinario": "recurso",
    "apelacao": "apelação",
    "contrarrazoes": "contrarrazões",
    "embargos-de-declaracao": "embargos de declaração",
    "agravo-de-instrumento": "agravo de instrumento",
    "pedido-de-prorrogacao": "pedido de prorrogação",
    "requerimento-administrativo": "requerimento administrativo",
    "memoriais": "memoriais",
    "manifestacao": "manifestação",
    "cumprimento-de-sentenca": "pedido de cumprimento de sentença",
}
ACENTOS = {
    "peticao": "petição", "contestacao": "contestação", "reclamacao": "reclamação", "replica": "réplica",
    "impugnacao": "impugnação", "apelacao": "apelação", "contrarrazoes": "contrarrazões",
    "declaracao": "declaração", "prorrogacao": "prorrogação", "manifestacao": "manifestação",
    "divorcio": "divórcio", "sentenca": "sentença", "execucao": "execução", "concessao": "concessão",
    "revisao": "revisão", "pensao": "pensão", "acao": "ação", "uniao": "união", "estavel": "estável",
    "previdenciario": "previdenciário", "beneficio": "benefício", "auxilio": "auxílio",
    "incapacidade": "incapacidade", "indenizacao": "indenização", "tutela": "tutela",
    "urgencia": "urgência", "audiencia": "audiência", "pericia": "perícia", "rescisao": "rescisão",
    "rescisoria": "rescisória", "homologacao": "homologação", "habilitacao": "habilitação",
    "juridico": "jurídico", "medico": "médico", "minuta": "minuta",
}


def nome_da_peca(tipo):
    """Tipo técnico da peça (peticao-inicial-restabelecimento) em linguagem de cliente (petição inicial)."""
    chave = norm(tipo)
    if not chave:
        return "peça"
    if chave in NOMES_DE_PECA:
        return NOMES_DE_PECA[chave]
    for k in sorted(NOMES_DE_PECA, key=len, reverse=True):
        if chave.startswith(k + "-"):
            return NOMES_DE_PECA[k]
    return " ".join(ACENTOS.get(p, p) for p in chave.split("-") if p)


def com_artigo(nome):
    """'a petição inicial', 'o recurso', 'os embargos de declaração'."""
    primeira = nome.split()[0] if nome.split() else ""
    if primeira in ("memoriais", "contrarrazões", "embargos", "cálculos", "quesitos"):
        return "os " + nome
    if primeira in ("recurso", "pedido", "requerimento", "agravo", "mandado", "acordo") or (primeira.endswith("o") and not primeira.endswith("ão")):
        return "o " + nome
    if primeira.endswith("s"):
        return "as " + nome
    return "a " + nome


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def norm(valor):
    v = "".join(c for c in unicodedata.normalize("NFKD", (valor or "").strip()) if not unicodedata.combining(c))
    return re.sub(r"[\s_]+", "-", v.lower())


def ler(caminho):
    p = Path(caminho)
    if not p.exists():
        falhar(f"não encontrei o registro de peças em `{caminho}`. O padrão é "
               "escritorio/07-operacao/juridico/pecas.csv. Nada foi registrado.")
    bruto = p.read_bytes()
    bom = bruto.startswith(b"\xef\xbb\xbf")
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    fim = "\r\n" if "\r\n" in texto else "\n"
    linhas = texto.splitlines()
    sep_linha = None
    if linhas and linhas[0].strip().lower().startswith("sep="):
        sep_linha = linhas.pop(0)
    if not linhas or not linhas[0].strip():
        falhar(f"o arquivo `{caminho}` está vazio. Nada foi registrado.")
    separador = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    tabela = list(csv.reader(io.StringIO("\n".join(linhas)), delimiter=separador))
    cab = [norm(c).replace("-", "_") for c in tabela[0]]
    faltam = [c for c in OBRIGATORIAS if c not in cab]
    if faltam:
        falhar("faltam colunas no registro de peças: " + ", ".join(faltam)
               + ". Copie a primeira linha de docs/producao.md do plugin.")
    return {"tabela": tabela, "cab": cab, "sep": separador, "fim": fim, "bom": bom,
            "cod": cod, "sep_linha": sep_linha}


def ler_data_hora(texto):
    t = (texto or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})[ T]+(\d{1,2}):(\d{2})", t) or None
    if m:
        a, me, d, h, mi = m.groups()
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})[ ,]+(\d{1,2})[:h](\d{2})", t)
        if not m:
            return None
        d, me, a, h, mi = m.groups()
    try:
        return datetime(int(a), int(me), int(d), int(h), int(mi))
    except ValueError:
        return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--id", required=True)
    p.add_argument("--sistema", required=True)
    p.add_argument("--numero", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--quem", default="a pessoa que protocolou")
    p.add_argument("--hoje")
    p.add_argument("--gravar", action="store_true")
    p.add_argument("--treino", action="store_true")
    args = p.parse_args()

    if "_treino" in Path(args.csv).parts and not args.treino:
        falhar(f"`{args.csv}` é o registro de treino. Para registrar mesmo assim, rode com --treino.")
    momento = ler_data_hora(args.data)
    if not momento:
        falhar(f"data do protocolo `{args.data}` não dá para ler. Use \"AAAA-MM-DD HH:MM\", como está no comprovante.")
    if args.hoje:
        try:
            hoje = date.fromisoformat(args.hoje)
        except ValueError:
            falhar(f"--hoje `{args.hoje}` inválido. Use AAAA-MM-DD.")
    else:
        hoje = date.today()
    numero = args.numero.strip()
    if not numero or re.fullmatch(r"\[[^\]]*\]|\{[^}]*\}", numero):
        falhar("o número do protocolo está vazio ou é uma marcação. Copie o número do comprovante do sistema.")
    sistema = SISTEMAS.get(norm(args.sistema), args.sistema.strip())

    r = ler(args.csv)
    cab, tabela = r["cab"], r["tabela"]
    col = {c: i for i, c in enumerate(cab)}
    achadas = [i for i, linha in enumerate(tabela[1:], start=1)
               if len(linha) > col["id"] and linha[col["id"]].strip().upper() == args.id.strip().upper()]
    if not achadas:
        falhar(f"a peça `{args.id}` não está no registro. Confira o id na coluna id.")
    if len(achadas) > 1:
        falhar(f"a peça `{args.id}` aparece {len(achadas)} vezes no registro. Corrija o registro antes "
               "(a rotina-juridica aponta em \"registro a corrigir\").")
    i = achadas[0]
    linha = tabela[i] + [""] * (len(cab) - len(tabela[i]))
    antes = list(linha)
    etapa = norm(linha[col["etapa"]])
    if etapa == "protocolada":
        falhar(f"a peça `{args.id}` já está protocolada ({linha[col['protocolo_data']] or 'sem data'}). "
               "Se o registro está errado, corrija com o advogado; o script não sobrescreve um protocolo.")
    if etapa != "aprovada":
        falhar(f"a peça `{args.id}` está em `{linha[col['etapa']] or 'vazio'}`. Só peça aprovada pelo advogado é "
               "registrada como protocolada (docs/producao.md, regra 3). Se ela foi protocolada sem passar por "
               "aprovada, leve ao advogado antes de registrar.")
    if norm(linha[col["citacoes"]]) != "verde" or norm(linha[col["dados"]]) != "ok":
        falhar(f"a peça `{args.id}` está aprovada com citações `{linha[col['citacoes']] or 'vazio'}` e dados "
               f"`{linha[col['dados']] or 'vazio'}`. O registro diz que ela não podia ir para protocolo "
               "(docs/producao.md, regra 4). Leve ao advogado antes de registrar.")

    linha[col["etapa"]] = "protocolada"
    linha[col["protocolo_sistema"]] = sistema
    linha[col["protocolo_numero"]] = numero
    linha[col["protocolo_data"]] = momento.strftime("%Y-%m-%d %H:%M")
    linha[col["atualizado_em"]] = hoje.isoformat()
    tabela[i] = linha

    peca = nome_da_peca(linha[col["peca"]])
    codigo = linha[col["codigo_caso"]]
    print(f"Peça {linha[col['id']]} · {codigo} · {linha[col['peca']]}")
    print("")
    print("| Coluna | Antes | Depois |")
    print("|---|---|---|")
    for c in ("etapa", "protocolo_sistema", "protocolo_numero", "protocolo_data", "atualizado_em"):
        print(f"| {c} | {antes[col[c]] or '(vazio)'} | {linha[col[c]]} |")
    print("")
    print("Linha para o histórico do cliente, se o motor-experiencia estiver instalado")
    print(f"(07-operacao/experiencia/clientes/{codigo}/historico.md; não muda o ultimo_contato):")
    print(f"| {momento:%Y-%m-%d %H:%M} | trabalho-do-escritorio | {args.quem} | Protocolamos {com_artigo(peca)} no {sistema}. |")
    print("")
    pasta_casos = "07-operacao/_treino/juridico/casos" if "_treino" in Path(args.csv).parts else "07-operacao/juridico/casos"
    print(f"Comprovante: guardar em {pasta_casos}/{codigo}/protocolo/, "
          f"com o nome {linha[col['peca']]}-{momento:%Y-%m-%d}-comprovante.pdf")

    if not args.gravar:
        print("")
        print("Nada foi gravado. Depois do ok, rode de novo com --gravar.")
        return
    destino = Path(args.csv)
    shutil.copy2(destino, destino.with_name(destino.name + ".bak"))
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=r["sep"], lineterminator=r["fim"])
    for l in tabela:
        escritor.writerow(l)
    texto = (r["sep_linha"] + r["fim"] if r["sep_linha"] else "") + saida.getvalue()
    cod = "utf-8" if r["cod"] == "utf-8-sig" else r["cod"]
    dados = texto.encode(cod)
    if r["bom"]:
        dados = b"\xef\xbb\xbf" + dados
    temp = destino.with_name(destino.name + ".tmp")
    temp.write_bytes(dados)
    temp.replace(destino)
    print("")
    print(f"Gravado em `{destino}`. Cópia do arquivo anterior em `{destino.name}.bak`.")


if __name__ == "__main__":
    main()
