#!/usr/bin/env python3
"""A carteira de processos da controladoria (processos.csv).

Colunas (contrato do plugin):
  processo,codigo_caso,cliente_curto,area,tribunal,orgao,responsavel,situacao,ultima_movimentacao,atualizado_em

Comandos:
  importar <exportacao.csv|.xlsx> --carteira processos.csv [--hoje AAAA-MM-DD] [--gravar]
      Lê a exportação do sistema ou a planilha do escritório, guarda só o mínimo (primeiro nome do
      cliente, sem CPF nem endereço), junta com a carteira que já existe (pelo número do processo)
      e nunca apaga linha. Código do caso só entra se a exportação trouxer, ou se o processo já
      estava na carteira: nada é ligado por nome.

  conferir --carteira processos.csv [--publicacoes publicacoes.csv] [--parado-dias N | --ficha <ficha>]
           [--hoje AAAA-MM-DD] [--gravar]
      Processo que publica e não está na carteira; processo ativo sem publicação e parado há mais de N
      dias; carteira com movimentação mais velha que a última publicação (com --gravar, atualiza a
      ultima_movimentacao); linhas sem código, sem responsável, repetidas.

  incluir --carteira processos.csv --processo N --codigo C-AAAA-NNNN --cliente Nome [--area] [--tribunal]
          [--orgao] [--responsavel] [--situacao ativo] [--hoje] [--gravar]
      Inclui (ou corrige) uma linha depois que a pessoa disse de quem é o processo.

Sem --gravar, só mostra. Código 1 quando falta arquivo ou coluna obrigatória.
"""
import argparse
import csv
import datetime as dt
import io
import os
import re
import sys
import unicodedata

COLUNAS = ["processo", "codigo_caso", "cliente_curto", "area", "tribunal", "orgao", "responsavel", "situacao",
           "ultima_movimentacao", "atualizado_em"]
SITUACOES = ["ativo", "suspenso", "arquivado", "encerrado"]
APELIDOS = {
    "processo": ["processo", "numero_processo", "numero_do_processo", "n_processo", "autos", "numero", "num_processo",
                 "numero_cnj", "processo_cnj"],
    "codigo_caso": ["codigo_caso", "codigo", "codigo_do_caso", "codigo_cliente", "pasta", "caso", "id_caso"],
    "cliente_curto": ["cliente_curto", "cliente", "nome_do_cliente", "nome_cliente", "parte_cliente", "nome", "constituinte"],
    "area": ["area", "area_do_direito", "materia", "assunto"],
    "tribunal": ["tribunal", "sigla", "sigla_tribunal"],
    "orgao": ["orgao", "vara", "juizo", "vara_juizo", "orgao_julgador", "comarca_vara"],
    "responsavel": ["responsavel", "advogado", "advogado_responsavel", "responsavel_pelo_caso"],
    "situacao": ["situacao", "status", "fase", "estado"],
    "ultima_movimentacao": ["ultima_movimentacao", "data_ultima_movimentacao", "ultimo_andamento",
                            "data_do_ultimo_andamento", "ultima_atualizacao", "movimentacao"],
}
SENSIVEIS = ["cpf", "rg", "cnpj", "endereco", "telefone", "celular", "email", "e_mail", "nascimento", "valor_da_causa",
             "cid", "doenca", "renda", "salario"]
UFS_TJ = {"01": "AC", "02": "AL", "03": "AP", "04": "AM", "05": "BA", "06": "CE", "07": "DFT", "08": "ES", "09": "GO",
          "10": "MA", "11": "MT", "12": "MS", "13": "MG", "14": "PA", "15": "PB", "16": "PR", "17": "PE", "18": "PI",
          "19": "RJ", "20": "RN", "21": "RS", "22": "RO", "23": "RR", "24": "SC", "25": "SE", "26": "SP", "27": "TO"}


def erro(msg):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(1)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def chave_coluna(nome):
    return re.sub(r"[^a-z0-9]+", "_", sem_acento((nome or "").strip().lower())).strip("_")


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc), bruto.startswith(b"\xef\xbb\xbf")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace"), False


def ler_linhas(caminho):
    """Devolve (linhas com nomes crus, delimitador, bom)."""
    if not os.path.exists(caminho):
        erro(f"não encontrei {caminho}")
    if caminho.lower().endswith(".xlsx"):
        try:
            import openpyxl  # opcional
        except ImportError:
            erro(f"{caminho}: para ler .xlsx é preciso o openpyxl. Sem ele, salve a planilha como .csv e rode de novo")
        folha = openpyxl.load_workbook(caminho, read_only=True, data_only=True).worksheets[0]
        linhas = list(folha.iter_rows(values_only=True))
        if not linhas:
            erro(f"{caminho}: planilha vazia")
        cab = [str(c) if c is not None else "" for c in linhas[0]]
        saida = []
        for lin in linhas[1:]:
            d = {}
            for c, v in zip(cab, lin):
                if isinstance(v, (dt.date, dt.datetime)):
                    v = v.strftime("%Y-%m-%d")
                d[c] = "" if v is None else str(v).strip()
            saida.append(d)
        return saida, ",", False
    texto, bom = ler_texto(caminho)
    if not texto.strip():
        erro(f"{caminho} está vazio")
    primeira = texto.splitlines()[0]
    delim = ";" if primeira.count(";") > primeira.count(",") else ","
    return [{k: (v or "").strip() for k, v in l.items() if k is not None}
            for l in csv.DictReader(io.StringIO(texto), delimiter=delim)], delim, bom


def data_iso(valor):
    v = (valor or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        a, mes, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})", v)
        if not m:
            return ""
        d, mes, a = m.groups()
        a = "20" + a if len(a) == 2 else a
    try:
        return dt.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return ""


def digitos(p):
    return re.sub(r"\D", "", p or "")


def mascara(p):
    d = digitos(p)
    if len(d) == 20:
        return f"{d[0:7]}-{d[7:9]}.{d[9:13]}.{d[13]}.{d[14:16]}.{d[16:20]}"
    return (p or "").strip()


def tribunal_pelo_numero(p):
    d = digitos(p)
    if len(d) != 20:
        return ""
    j, tr = d[13], d[14:16]
    return {"4": f"TRF{int(tr)}", "5": f"TRT{int(tr)}"}.get(j) or (("TJ" + UFS_TJ[tr]) if j == "8" and tr in UFS_TJ else "")


def primeiro_nome(nome):
    n = (nome or "").strip()
    if not n:
        return ""
    if re.fullmatch(r"(?:[A-Za-zÀ-ÿ]\.\s*)+", n):
        return n
    return n.split()[0].capitalize() if n.isupper() else n.split()[0]


def situacao_normalizada(v):
    s = chave_coluna(v)
    if not s:
        return ""
    for chave, sit in (("arquiv", "arquivado"), ("baixad", "arquivado"), ("encerr", "encerrado"), ("finaliz", "encerrado"),
                       ("suspens", "suspenso"), ("sobrest", "suspenso"), ("ativ", "ativo"), ("andamento", "ativo"),
                       ("tramit", "ativo"), ("cumprimento", "ativo"), ("execu", "ativo"), ("recurso", "ativo"),
                       ("instru", "ativo"), ("conhecimento", "ativo")):
        if chave in s:
            return sit
    return "[A CONFIRMAR: " + v.strip() + "]"


def ler_carteira(caminho, exigir=True):
    if not os.path.exists(caminho):
        if exigir:
            erro(f"não encontrei a carteira {caminho}. Monte com: carteira_processos.py importar <exportação> --carteira {caminho} --gravar")
        return [], ",", False
    linhas, delim, bom = ler_linhas(caminho)
    if linhas:
        cab = {chave_coluna(c) for c in linhas[0].keys()}
        faltam = [c for c in ("processo", "codigo_caso", "cliente_curto", "situacao", "ultima_movimentacao") if c not in cab]
        if faltam:
            erro(f"{caminho}: faltam as colunas {', '.join(faltam)}. Colunas da carteira: {','.join(COLUNAS)}")
    return [{chave_coluna(k): v for k, v in l.items()} for l in linhas], delim, bom


def gravar_carteira(caminho, linhas, delim=",", bom=False):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with open(caminho, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=delim, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in COLUNAS})


def hoje_de(a):
    h = data_iso(a.hoje) if a.hoje else dt.date.today().isoformat()
    if not h:
        erro(f"--hoje inválido: {a.hoje}")
    return h


# ---------------------------------------------------------------- importar

def cmd_importar(a):
    hoje = hoje_de(a)
    brutas, _, _ = ler_linhas(a.exportacao)
    if not brutas:
        erro(f"{a.exportacao}: nenhuma linha")
    chaves = {chave_coluna(c): c for c in brutas[0].keys()}
    mapa = {}
    for campo, apel in APELIDOS.items():
        for ap in apel:
            if ap in chaves:
                mapa[campo] = chaves[ap]
                break
    if "processo" not in mapa:
        erro(f"{a.exportacao}: não achei a coluna do número do processo. Colunas: {', '.join(brutas[0].keys())}. "
             f"Nomes aceitos: {', '.join(APELIDOS['processo'])}")
    descartadas = [c for k, c in chaves.items() if any(s in k for s in SENSIVEIS)]
    existentes, delim, bom = ler_carteira(a.carteira, exigir=False)
    por_num = {digitos(l["processo"]): l for l in existentes}
    novas, atualizadas, sem_codigo, avisos = [], [], [], []
    vistos = set()
    for n, b in enumerate(brutas, start=2):
        v = {campo: b.get(col, "").strip() for campo, col in mapa.items()}
        if not v.get("processo"):
            continue
        num = digitos(v["processo"])
        if len(num) != 20:
            avisos.append(f"linha {n}: número fora do padrão CNJ ({v['processo']}); entra como veio, conferir")
        if num in vistos:
            avisos.append(f"linha {n}: processo {v['processo']} repetido na exportação; fica a primeira linha")
            continue
        vistos.add(num)
        nova = {
            "processo": mascara(v["processo"]),
            "codigo_caso": v.get("codigo_caso", "") if re.fullmatch(r"C-\d{4}-\d{4}", v.get("codigo_caso", "")) else "",
            "cliente_curto": primeiro_nome(v.get("cliente_curto", "")),
            "area": chave_coluna(v.get("area", "")).replace("_", "-"),
            "tribunal": v.get("tribunal", "").upper().replace(" ", "") or tribunal_pelo_numero(v["processo"]),
            "orgao": v.get("orgao", ""),
            "responsavel": v.get("responsavel", ""),
            "situacao": situacao_normalizada(v.get("situacao", "")) or "ativo",
            "ultima_movimentacao": data_iso(v.get("ultima_movimentacao", "")),
            "atualizado_em": hoje,
        }
        if v.get("codigo_caso") and not nova["codigo_caso"]:
            avisos.append(f"linha {n}: código '{v['codigo_caso']}' fora do formato C-AAAA-NNNN; fica vazio para a pessoa")
        antiga = por_num.get(num)
        if antiga:
            mudou = {}
            for c in COLUNAS:
                if c in ("processo", "atualizado_em"):
                    continue
                if c == "codigo_caso" and antiga.get(c) and nova[c] and antiga[c] != nova[c]:
                    avisos.append(f"{nova['processo']}: código na carteira {antiga[c]} e na exportação {nova[c]}. "
                                  "Fica o da carteira até a pessoa decidir")
                    continue
                if nova[c] and nova[c] != antiga.get(c, ""):
                    if c == "ultima_movimentacao" and antiga.get(c, "") > nova[c]:
                        continue
                    if c == "codigo_caso" and antiga.get(c):
                        continue
                    mudou[c] = (antiga.get(c, ""), nova[c])
            if mudou:
                for c, (_, novo) in mudou.items():
                    antiga[c] = novo
                antiga["atualizado_em"] = hoje
                atualizadas.append((antiga["processo"], mudou))
            if not antiga.get("codigo_caso"):
                sem_codigo.append(antiga)
        else:
            novas.append(nova)
            if not nova["codigo_caso"]:
                sem_codigo.append(nova)
    fora = [l for l in existentes if digitos(l["processo"]) not in vistos and l.get("situacao") == "ativo"]
    resultado = existentes + novas
    if a.gravar:
        gravar_carteira(a.carteira, resultado, delim, bom)
    print(f"CARTEIRA · importação de {os.path.basename(a.exportacao)} · {hoje} · "
          f"{'gravado' if a.gravar else 'SIMULAÇÃO (nada gravado; use --gravar)'}")
    print(f"Carteira: {a.carteira} · {len(existentes)} linhas antes · {len(novas)} novas · {len(atualizadas)} atualizadas")
    print(f"Colunas lidas: {', '.join(f'{k}<-{v}' for k, v in mapa.items())}")
    if descartadas:
        print(f"Colunas que NÃO entram (dado que a carteira não guarda): {', '.join(descartadas)}")
    if "cliente_curto" in mapa:
        print("Cliente: só o primeiro nome entra na carteira.")
    if sem_codigo:
        print(f"\nSEM CÓDIGO DO CASO ({len(sem_codigo)}): a pessoa diz o código; nada é ligado por nome")
        for l in sem_codigo:
            print(f"  {l['processo']} · {l.get('cliente_curto') or '[A CONFIRMAR]'} · {l.get('tribunal', '')} · {l.get('orgao', '')}")
    if atualizadas:
        print("\nATUALIZADAS:")
        for p, m in atualizadas:
            print(f"  {p}: " + "; ".join(f"{c} {v[0] or 'vazio'} -> {v[1]}" for c, v in m.items()))
    if fora:
        print(f"\nATIVOS NA CARTEIRA QUE NÃO VIERAM NA EXPORTAÇÃO ({len(fora)}): encerrado, arquivado ou fora da exportação? "
              "Nada muda sem a pessoa")
        for l in fora:
            print(f"  {l['processo']} · {l.get('codigo_caso', '')} · {l.get('cliente_curto', '')}")
    if avisos:
        print("\nAVISOS:")
        for av in avisos:
            print(f"  - {av}")
    return 0


# ---------------------------------------------------------------- conferir

def parado_da_ficha(caminho):
    if not os.path.exists(caminho):
        erro(f"não encontrei a ficha {caminho}")
    texto, _ = ler_texto(caminho)
    m = re.search(r"(?im)^\s*-?\s*processo_parado_dias\s*:\s*(\d+)", texto)
    return int(m.group(1)) if m else None


def cmd_conferir(a):
    hoje = hoje_de(a)
    carteira, delim, bom = ler_carteira(a.carteira)
    if not carteira:
        erro(f"{a.carteira} não tem nenhum processo. Importe a carteira primeiro (comando importar)")
    parado = a.parado_dias
    if parado is None and a.ficha:
        parado = parado_da_ficha(a.ficha)
    pubs = []
    if a.publicacoes:
        linhas, _, _ = ler_linhas(a.publicacoes)
        if linhas:
            cab = {chave_coluna(c) for c in linhas[0].keys()}
            faltam = [c for c in ("id", "processo", "disponibilizada_em", "triagem") if c not in cab]
            if faltam:
                erro(f"{a.publicacoes}: faltam as colunas {', '.join(faltam)}")
        pubs = [{chave_coluna(k): v for k, v in l.items()} for l in linhas]
    por_num = {}
    repetidos = []
    for l in carteira:
        d = digitos(l["processo"])
        if d in por_num:
            repetidos.append(l["processo"])
        por_num[d] = l
    ultima_pub = {}
    fora_da_carteira = {}
    for p in pubs:
        if p.get("triagem") == "duplicada":
            continue
        d = digitos(p.get("processo", ""))
        data = data_iso(p.get("disponibilizada_em", ""))
        if d in por_num:
            if data and data > ultima_pub.get(d, ""):
                ultima_pub[d] = data
        elif d:
            fora_da_carteira.setdefault(p.get("processo", ""), []).append(p)

    hoje_d = dt.date.fromisoformat(hoje)
    parados, desatualizadas, sem_codigo, sem_resp = [], [], [], []
    for l in carteira:
        d = digitos(l["processo"])
        mov = data_iso(l.get("ultima_movimentacao", ""))
        pub = ultima_pub.get(d, "")
        efetiva = max(mov, pub)
        if pub and pub > mov:
            desatualizadas.append((l, mov, pub))
        ativo = (l.get("situacao") or "ativo") == "ativo"
        if ativo and parado is not None and efetiva and (hoje_d - dt.date.fromisoformat(efetiva)).days > parado:
            parados.append((l, efetiva, (hoje_d - dt.date.fromisoformat(efetiva)).days))
        if ativo and parado is not None and not efetiva:
            parados.append((l, "", None))
        if not l.get("codigo_caso"):
            sem_codigo.append(l)
        if ativo and not l.get("responsavel"):
            sem_resp.append(l)

    if a.gravar and desatualizadas:
        for l, _, pub in desatualizadas:
            l["ultima_movimentacao"] = pub
            l["atualizado_em"] = hoje
        gravar_carteira(a.carteira, carteira, delim, bom)

    print(f"CONFERÊNCIA DA CARTEIRA · {hoje} · {len(carteira)} processos"
          + (f" · {len(pubs)} publicações lidas" if a.publicacoes else " · sem publicações (use --publicacoes)")
          + (" · gravado" if a.gravar and desatualizadas else ""))
    print(f"\n1. PUBLICOU E NÃO ESTÁ NA CARTEIRA ({len(fora_da_carteira)}): para a pessoa. Caso antigo, substabelecimento "
          "ou erro? Nada é ligado por nome")
    for proc, ps in sorted(fora_da_carteira.items()):
        print(f"  {proc} · {ps[0].get('tribunal', '')} · {ps[0].get('orgao', '')} · " +
              ", ".join(f"{p['id']} ({data_iso(p.get('disponibilizada_em', '')) or 'sem data'})" for p in ps))
    if parado is None:
        print("\n2. PARADOS: não conferido. Falta processo_parado_dias na ficha da controladoria "
              "(passe --parado-dias N ou --ficha). [A PREENCHER]")
    else:
        print(f"\n2. ATIVOS PARADOS HÁ MAIS DE {parado} DIAS ({len(parados)}), contando a última publicação:")
        for l, ef, dias in sorted(parados, key=lambda x: x[1] or ""):
            print(f"  {l['processo']} · {l.get('codigo_caso') or 'sem código'} · {l.get('cliente_curto', '')} · "
                  + (f"última movimentação {ef} ({dias} dias)" if ef else "sem data de movimentação [A CONFIRMAR]"))
    print(f"\n3. CARTEIRA ATRÁS DAS PUBLICAÇÕES ({len(desatualizadas)})"
          + (": ultima_movimentacao atualizada" if a.gravar else ": use --gravar para atualizar a ultima_movimentacao"))
    for l, mov, pub in desatualizadas:
        print(f"  {l['processo']} · {l.get('codigo_caso', '')} · carteira {mov or 'vazia'} · publicou em {pub}")
    print(f"\n4. SEM CÓDIGO DO CASO ({len(sem_codigo)}): a pessoa diz o código")
    for l in sem_codigo:
        print(f"  {l['processo']} · {l.get('cliente_curto') or '[A CONFIRMAR]'}")
    print(f"\n5. ATIVOS SEM RESPONSÁVEL ({len(sem_resp)})")
    for l in sem_resp:
        print(f"  {l['processo']} · {l.get('codigo_caso', '')}")
    if repetidos:
        print(f"\n6. REPETIDOS NA CARTEIRA ({len(repetidos)}): " + ", ".join(repetidos))
    return 0


# ---------------------------------------------------------------- incluir

def cmd_incluir(a):
    hoje = hoje_de(a)
    if not re.fullmatch(r"C-\d{4}-\d{4}", a.codigo):
        erro(f"código fora do formato C-AAAA-NNNN: {a.codigo}")
    carteira, delim, bom = ler_carteira(a.carteira, exigir=False)
    d = digitos(a.processo)
    linha = next((l for l in carteira if digitos(l["processo"]) == d), None)
    novo = {"processo": mascara(a.processo), "codigo_caso": a.codigo, "cliente_curto": primeiro_nome(a.cliente),
            "area": a.area or "", "tribunal": (a.tribunal or tribunal_pelo_numero(a.processo)).upper(),
            "orgao": a.orgao or "", "responsavel": a.responsavel or "", "situacao": a.situacao,
            "ultima_movimentacao": data_iso(a.ultima_movimentacao) if a.ultima_movimentacao else "", "atualizado_em": hoje}
    if linha:
        antes = dict(linha)
        for c, v in novo.items():
            if v:
                linha[c] = v
        acao = "corrigida"
        print("Antes: " + ",".join(antes.get(c, "") for c in COLUNAS))
    else:
        carteira.append(novo)
        linha = novo
        acao = "incluída"
    print(f"Linha {acao}{'' if a.gravar else ' (SIMULAÇÃO; use --gravar)'}: " + ",".join(linha.get(c, "") for c in COLUNAS))
    if a.gravar:
        gravar_carteira(a.carteira, carteira, delim, bom)
    print("Próximo passo: triar de novo a publicação que estava sem-caso (apoio_triagem.py --ids <id> --todas).")
    return 0


def main():
    ap = argparse.ArgumentParser(description="A carteira de processos da controladoria")
    sub = ap.add_subparsers(dest="cmd")
    i = sub.add_parser("importar")
    i.add_argument("exportacao")
    i.add_argument("--carteira", required=True)
    i.add_argument("--hoje")
    i.add_argument("--gravar", action="store_true")
    c = sub.add_parser("conferir")
    c.add_argument("--carteira", required=True)
    c.add_argument("--publicacoes")
    c.add_argument("--parado-dias", type=int)
    c.add_argument("--ficha")
    c.add_argument("--hoje")
    c.add_argument("--gravar", action="store_true")
    n = sub.add_parser("incluir")
    n.add_argument("--carteira", required=True)
    n.add_argument("--processo", required=True)
    n.add_argument("--codigo", required=True)
    n.add_argument("--cliente", required=True)
    n.add_argument("--area")
    n.add_argument("--tribunal")
    n.add_argument("--orgao")
    n.add_argument("--responsavel")
    n.add_argument("--situacao", default="ativo", choices=SITUACOES)
    n.add_argument("--ultima-movimentacao")
    n.add_argument("--hoje")
    n.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    if a.cmd == "importar":
        return cmd_importar(a)
    if a.cmd == "conferir":
        return cmd_conferir(a)
    if a.cmd == "incluir":
        return cmd_incluir(a)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
