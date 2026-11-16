#!/usr/bin/env python3
"""Lê os controles de documentos dos clientes e diz quem precisa de cobrança hoje.

Uso:
    python3 documentos_pendentes.py <pasta clientes> [--carteira carteira.csv] [--regua 3,7] [--hoje AAAA-MM-DD]

<pasta clientes> é escritorio/07-operacao/experiencia/clientes (cada cliente tem
<codigo>/documentos.md, no formato da seção 6.2 do SKILL.md).

Para cada documento pendente ou com problema, calcula a próxima cobrança:
  - se há data combinada com o cliente e ela ainda não foi cobrada, a cobrança é nessa data;
  - senão, a régua de cobrança (dias corridos depois do pedido, ex.: 3,7);
  - depois da última cobrança da régua, "o advogado decide" (sem mensagem automática).
Mostra também quantos documentos faltam por cliente (a coluna documentos_pendentes da
carteira) e, com --carteira, as diferenças e quem pediu para não receber mensagens.

Sai com código 1 e mensagem clara quando falta a pasta, nenhum documentos.md é encontrado,
a tabela não tem as colunas obrigatórias ou a carteira não tem as colunas que o script usa.
Só biblioteca padrão. Python 3.9+.
"""
import argparse
import csv
import io
import re
import sys
from datetime import date
from pathlib import Path

ABERTAS = {"pendente", "chegou-com-problema", "nao-existe", "não-existe"}
FECHADAS = {"chegou-ok", "dispensado"}
COLUNAS = {"documento", "situacao", "pedido_em"}


class Erro(Exception):
    pass


def ler_data(s):
    s = (s or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        a, me, d = map(int, m.groups())
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if not m:
            return None
        d, me, a = map(int, m.groups())
    try:
        return date(a, me, d)
    except ValueError:
        return None


def datas_em(texto):
    achadas = re.findall(r"\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4}", texto or "")
    return [d for d in (ler_data(x) for x in achadas) if d]


def chave(t):
    t = t.strip().lower().translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def ler_controle(caminho):
    texto = caminho.read_text(encoding="utf-8-sig")
    situacao_geral = ""
    m = re.search(r"^Situa[cç][aã]o:\s*(.+)$", texto, re.M | re.I)
    if m:
        situacao_geral = m.group(1).strip().lower()
    linhas = [l for l in texto.splitlines() if l.strip().startswith("|")]
    if not linhas:
        raise Erro(f"{caminho}: não achei a tabela de documentos")
    cab = [chave(c) for c in linhas[0].strip().strip("|").split("|")]
    faltam = COLUNAS - set(cab)
    if faltam:
        raise Erro(f"{caminho}: a tabela não tem as colunas {', '.join(sorted(faltam))} "
                   f"(esperado: Documento | Situação | Pedido em | Combinado até | Chegou em | Cobranças | Observação)")
    itens = []
    for l in linhas[1:]:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cel if c):
            continue
        cel += [""] * (len(cab) - len(cel))
        itens.append(dict(zip(cab, cel)))
    return situacao_geral, itens


def proxima_cobranca(item, regua):
    pedido = ler_data(item.get("pedido_em"))
    combinado = ler_data(item.get("combinado_ate"))
    cobrancas = sorted(datas_em(item.get("cobrancas", "")))
    ultima = cobrancas[-1] if cobrancas else None
    if combinado and (ultima is None or ultima < combinado):
        return combinado, "data combinada com o cliente"
    if not pedido:
        return None, "sem data de pedido: preencha 'Pedido em'"
    feitas_na_regua = [c for c in cobrancas if not (combinado and c == combinado)]
    n = len(feitas_na_regua)
    if n < len(regua):
        return date.fromordinal(pedido.toordinal() + regua[n]), f"{n + 1}ª cobrança da régua"
    return None, "régua cumprida: o advogado decide (ligar, pedir prazo, seguir sem)"


def ler_carteira(caminho):
    p = Path(caminho)
    if not p.exists():
        raise Erro(f"não encontrei a carteira: {p}")
    bruto = p.read_bytes().decode("utf-8-sig", errors="replace")
    primeira = bruto.splitlines()[0] if bruto.strip() else ""
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(bruto), delimiter=sep)
    campos = {(c or "").strip().lower(): c for c in (leitor.fieldnames or [])}
    for obrig in ("codigo", "documentos_pendentes"):
        if obrig not in campos:
            raise Erro(f"a carteira não tem a coluna obrigatória '{obrig}' (separador lido: '{sep}')")
    saida = {}
    for linha in leitor:
        lin = {k.strip().lower(): (v or "").strip() for k, v in linha.items() if k}
        if lin.get("codigo"):
            saida[lin["codigo"].upper()] = lin
    return saida


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cobranças de documentos do dia, pela régua.")
    ap.add_argument("clientes", help="pasta escritorio/07-operacao/experiencia/clientes")
    ap.add_argument("--carteira", help="carteira.csv, para conferir documentos_pendentes e quem pediu para não receber")
    ap.add_argument("--regua", default="3,7", help="dias corridos depois do pedido, separados por vírgula (ficha: cobranca_de_documentos)")
    ap.add_argument("--hoje", help="data de referência, AAAA-MM-DD ou DD/MM/AAAA (padrão: hoje)")
    a = ap.parse_args(argv)
    try:
        hoje = ler_data(a.hoje) if a.hoje else date.today()
        if a.hoje and not hoje:
            raise Erro(f"data --hoje não reconhecida: {a.hoje}")
        try:
            regua = sorted(int(x) for x in a.regua.split(",") if x.strip())
        except ValueError:
            raise Erro(f"régua inválida: '{a.regua}' (use números de dias, ex.: 3,7)")
        if not regua:
            raise Erro("régua vazia: use, por exemplo, --regua 3,7")
        pasta = Path(a.clientes)
        if not pasta.is_dir():
            raise Erro(f"não encontrei a pasta de clientes: {pasta}")
        controles = sorted(pasta.glob("*/documentos.md"))
        if not controles:
            raise Erro(f"nenhum documentos.md em {pasta}/<codigo>/: nada foi lido, então não dá para dizer que não há cobrança")
        carteira = ler_carteira(a.carteira) if a.carteira else {}

        cobrar, aguardando, decidir, contagem = [], [], [], {}
        for c in controles:
            codigo = c.parent.name.upper()
            geral, itens = ler_controle(c)
            abertos = [i for i in itens if i.get("situacao", "").strip().lower() in ABERTAS]
            contagem[codigo] = len(abertos)
            if geral.startswith("fechada") or geral.startswith("travada"):
                if abertos and geral.startswith("travada"):
                    decidir.append((codigo, "controle travado", geral))
                continue
            lin = carteira.get(codigo, {})
            nao_receber = lin.get("pediu_para_nao_receber", "").lower() == "sim"
            for i in abertos:
                sit = i.get("situacao", "").strip().lower()
                doc = i.get("documento", "")
                if sit in {"nao-existe", "não-existe"}:
                    decidir.append((codigo, doc, "o cliente diz que não tem: o advogado decide"))
                    continue
                prox, motivo = proxima_cobranca(i, regua)
                if prox is None:
                    decidir.append((codigo, doc, motivo))
                elif prox <= hoje:
                    atraso = (hoje - prox).days
                    quando = "hoje" if atraso == 0 else f"atrasada desde {prox.isoformat()} ({atraso} dias)"
                    como = "LIGAÇÃO (pediu para não receber mensagens de rotina)" if nao_receber else "mensagem de cobrança gentil"
                    cobrar.append((codigo, doc, sit, quando, motivo, como))
                else:
                    aguardando.append((codigo, doc, prox.isoformat(), motivo))

        print(f"DOCUMENTOS · referência {hoje.isoformat()} · régua {','.join(map(str, regua))} dias corridos · "
              f"{len(controles)} controles lidos")
        print("\nCOBRAR HOJE")
        if cobrar:
            for codigo, doc, sit, quando, motivo, como in cobrar:
                extra = " (chegou com problema)" if sit == "chegou-com-problema" else ""
                print(f"- {codigo} · {doc}{extra} · {quando} · {motivo} · {como}")
        else:
            print("- nenhuma cobrança vence hoje nos controles lidos")
        print("\nPARA O ADVOGADO DECIDIR")
        for codigo, doc, motivo in decidir or [("-", "nada", "")]:
            print(f"- {codigo} · {doc}" + (f" · {motivo}" if motivo else ""))
        print("\nAGUARDANDO")
        for codigo, doc, data_, motivo in aguardando or [("-", "nada", "", "")]:
            print(f"- {codigo} · {doc}" + (f" · próxima em {data_} ({motivo})" if data_ else ""))
        print("\nDOCUMENTOS PENDENTES POR CLIENTE (coluna documentos_pendentes)")
        for codigo, n in contagem.items():
            linha = f"- {codigo}: {n}"
            if carteira:
                if codigo not in carteira:
                    linha += " · não está na carteira"
                else:
                    atual = carteira[codigo].get("documentos_pendentes", "")
                    if atual != str(n):
                        linha += f" · carteira diz '{atual or 'vazio'}': atualizar para {n}"
            print(linha)
        return 0
    except Erro as ex:
        print(f"ERRO: {ex}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
