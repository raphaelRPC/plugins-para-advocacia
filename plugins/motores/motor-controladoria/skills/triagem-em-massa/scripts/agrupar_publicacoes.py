#!/usr/bin/env python3
"""Agrupa publicações de teor igual ou quase igual, para triar um grupo de cada vez.

Feito para centenas de publicações por dia. O script:
  - normaliza o teor (sem acento, sem número de processo, data, valor, folha e nome das partes);
  - junta os iguais e, dentro do mesmo "perfil", os quase iguais (proporção de palavras em comum, na ordem);
  - nunca junta atos com número de dias ou de horas diferente, com destinatário diferente
    (parte autora, parte ré, INSS...) ou com sinal de urgência, audiência, perícia ou dispositivo
    de sentença diferentes;
  - separa as exceções (sozinhas, urgentes, sem caso na carteira) para a triagem uma a uma;
  - sorteia a amostra de cada grupo, para a pessoa ler inteira antes de aplicar a triagem.

A conta do prazo continua uma por publicação.

Uso:
  python3 agrupar_publicacoes.py agrupar <publicacoes.csv> [--processos processos.csv] [--limiar 0.9]
      [--todas] [--hoje AAAA-MM-DD] [--gravar]
  python3 agrupar_publicacoes.py aplicar <grupos.csv> --publicacoes <publicacoes.csv> --grupo G01
      --triagem prazo|ciencia|sem-providencia|audiencia|pericia --amostra-conferida
      [--fora PUB-...,PUB-...] [--resumo "<sem dado sensível>"] [--processos processos.csv] [--por ia]
      [--hoje AAAA-MM-DD] [--gravar]

agrupar, com --gravar, grava lotes/AAAA-MM-DD-grupos.csv e lotes/AAAA-MM-DD-triagem-em-massa.md
ao lado do publicacoes.csv. aplicar muda só as linhas nao-triada (ou triadas pela ia) do grupo.
"""
import argparse
import csv
import datetime as dt
import difflib
import io
import math
import os
import random
import re
import sys
import unicodedata

TRIAGENS_DE_GRUPO = ["prazo", "ciencia", "sem-providencia", "audiencia", "pericia"]


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


def ler_csv(caminho, obrigatorias):
    if not os.path.exists(caminho):
        erro(f"não encontrei {caminho}")
    texto, bom = ler_texto(caminho)
    if not texto.strip():
        erro(f"{caminho} está vazio")
    primeira = texto.splitlines()[0]
    delim = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=delim)
    cab = [chave_coluna(c) for c in (leitor.fieldnames or [])]
    faltam = [c for c in obrigatorias if c not in cab]
    if faltam:
        erro(f"{caminho}: faltam as colunas {', '.join(faltam)}")
    return [{chave_coluna(k): (v or "").strip() for k, v in l.items() if k is not None} for l in leitor], delim, bom


def digitos(p):
    return re.sub(r"\D", "", p or "")


def teor_e_partes(pasta, rel):
    caminho = os.path.join(pasta, rel) if rel else ""
    if not caminho or not os.path.exists(caminho):
        return "", ""
    texto, _ = ler_texto(caminho)
    m = re.match(r"(?s)^---\n(.*?)\n---\n", texto)
    if not m:
        return texto.strip(), ""
    partes = re.search(r"(?m)^partes:\s*(.*)$", m.group(1))
    return texto[m.end():].strip(), (partes.group(1).strip() if partes else "")


EXT = (r"(?:\d{1,3}|um|uma|dois|duas|tres|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|catorze|quatorze|"
       r"quinze|vinte|trinta|quarenta|sessenta|noventa|vinte\s+e\s+quatro|quarenta\s+e\s+oito|setenta\s+e\s+duas)")
RE_DIAS = re.compile(r"\b(" + EXT + r")(?:\s*\([^)]{1,30}\))?\s+dias?(?:\s+(uteis|corridos))?\b")
RE_HORAS = re.compile(r"\b(" + EXT + r")(?:\s*\([^)]{1,30}\))?\s+horas?\b")
DESTINATARIOS = [
    ("parte autora", r"\b(?:a\s+parte\s+autora|o\s+autor|a\s+autora|o\s+reclamante|a\s+reclamante|o\s+exequente|a\s+exequente|o\s+requerente|a\s+requerente)\b"),
    ("parte re", r"\b(?:a\s+parte\s+re|o\s+reu|a\s+re|a\s+reclamada|o\s+reclamado|o\s+executado|a\s+executada|o\s+requerido|a\s+requerida)\b"),
    ("inss", r"\b(?:o\s+inss|a\s+autarquia)\b"),
    ("uniao ou fazenda", r"\b(?:a\s+uniao|a\s+fazenda|o\s+estado|o\s+municipio)\b"),
    ("ministerio publico", r"\b(?:o\s+ministerio\s+publico|o\s+mpf|o\s+mpt)\b"),
    ("as partes", r"\b(?:as\s+partes|ambas\s+as\s+partes)\b"),
    ("perito", r"\b(?:o\s+perito|a\s+perita)\b"),
]
DESTINATARIOS = [(n, re.compile(r)) for n, r in DESTINATARIOS]
SINAIS = [
    ("urgente", re.compile(r"\burgente\b|\bimediatamente\b|\bprisao\b|\bbloqueio\b|\bliminar\b|\btutela\s+de\s+urgencia\b|\bbusca\s+e\s+apreensao\b")),
    ("audiencia", re.compile(r"\b(?:re)?designo\s+(?:a\s+|nova\s+)?audiencia|\baudiencia\s+(?:de\s+\w+\s+)?(?:designada|redesignada|marcada)\s+para")),
    ("pericia", re.compile(r"\b(?:re)?designo\s+(?:a\s+|nova\s+)?pericia|\bpericia\s+(?:\w+\s+)?(?:designada|marcada|agendada)\s+para")),
    ("improcedente", re.compile(r"\bjulgo\s+(?:totalmente\s+)?improcedentes?\b")),
    ("procedente", re.compile(r"\bjulgo\s+(?:totalmente\s+|parcialmente\s+)?procedentes?\b")),
    ("homologo", re.compile(r"\bhomologo\b")),
    ("valor", re.compile(r"\brequisicao\s+de\s+pequeno\s+valor\b|\brpv\b|\bprecatorio\b|\balvara\b")),
]


RE_PEDIDO = re.compile(r"\bprazo\s+legal\b|\bprazo\s+da\s+lei\b|\bdiga(?:m)?\b|\bmanifeste(?:m)?-se\b|\bmanifestar-se\b|"
                       r"\bse\s+manifestar\b|\bespecifique(?:m)?\b|\bespecificar\s+(?:as\s+)?provas\b|\bquerendo\b|"
                       r"\bintime(?:m)?-se\s+(?:a\s+parte\s+(?:autora|re)|o\s+autor|a\s+autora|o\s+reu|a\s+re|as\s+partes|"
                       r"o\s+reclamante|a\s+reclamante|a\s+reclamada|o\s+reclamado)\b")
OUTRA_PARTE = ("inss", "uniao ou fazenda", "ministerio publico", "perito")


def pede_algo_ao_cliente(teor):
    """O ato pede algo que pode ser da parte do cliente (dias sem destinatário da outra parte, ou pedido sem dias)?"""
    t = sem_acento(teor).lower()
    if RE_PEDIDO.search(t):
        return True
    if RE_DIAS.search(t):
        dest = [n for n, rx in DESTINATARIOS if rx.search(t)]
        return not dest or any(d not in OUTRA_PARTE for d in dest)
    return False


def normalizar(teor, partes):
    t = sem_acento(teor).lower()
    t = re.sub(r"\b\d{7}-?\d{2}\.?\d{4}\.?\d\.?\d{2}\.?\d{4}\b", " <proc> ", t)
    t = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b", " <data> ", t)
    t = re.sub(r"r\$\s*[\d.,]+", " <valor> ", t)
    t = re.sub(r"\b(?:id|fls?|folhas?|seq|doc)\.?\s*n?[ºo.]?\s*\d+\b", " <ref> ", t)
    t = re.sub(r"\b\d{1,2}h\d{0,2}\b|\b\d{1,2}:\d{2}\b", " <hora> ", t)
    for nome in re.split(r"\s+[xX]\s+|,|;", sem_acento(partes).lower()):
        nome = nome.strip()
        if len(nome) >= 4:
            t = t.replace(nome, " <parte> ")
    t = re.sub(r"[^a-z0-9<> ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def perfil(norm):
    dias = tuple(sorted({m.group(1) + (" " + m.group(2) if m.group(2) else "") for m in RE_DIAS.finditer(norm)}))
    horas = tuple(sorted({m.group(1) for m in RE_HORAS.finditer(norm)}))
    dest = tuple(n for n, rx in DESTINATARIOS if rx.search(norm))
    sinais = tuple(n for n, rx in SINAIS if rx.search(norm))
    return (dias, horas, dest, sinais)


def semelhanca(a, b, limiar):
    """Proporção de palavras em comum, na ordem (0 a 1). Corta cedo o que não tem chance."""
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    if m.real_quick_ratio() < limiar or m.quick_ratio() < limiar:
        return 0.0
    return m.ratio()


def descreve_perfil(pf):
    dias, horas, dest, sinais = pf
    partes = []
    partes.append("dias: " + (", ".join(dias) if dias else "nenhum"))
    if horas:
        partes.append("horas: " + ", ".join(horas))
    partes.append("destinatário: " + (", ".join(dest) if dest else "não diz"))
    if sinais:
        partes.append("sinais: " + ", ".join(sinais))
    return " · ".join(partes)


def diferencas(a, b, n=8):
    pa, pb = a.split(), b.split()
    sa, sb = set(pa), set(pb)
    so_a = [w for w in pa if w not in sb][:n]
    so_b = [w for w in pb if w not in sa][:n]
    return so_a, so_b


def cmd_agrupar(a):
    hoje = a.hoje or dt.date.today().isoformat()
    pubs, _, _ = ler_csv(a.publicacoes, ["id", "processo", "teor", "triagem"])
    pasta = os.path.dirname(os.path.abspath(a.publicacoes))
    carteira = None
    if a.processos:
        procs, _, _ = ler_csv(a.processos, ["processo", "codigo_caso"])
        carteira = {digitos(p["processo"]): p for p in procs}
    alvo = [p for p in pubs if p.get("triagem") == "nao-triada" or
            (a.todas and p.get("triagem") not in ("duplicada",) and p.get("triada_por", "") in ("", "ia"))]
    if not alvo:
        print(f"Nenhuma publicação nao-triada em {a.publicacoes} ({len(pubs)} linhas lidas). Nada a agrupar.")
        return 0
    itens, excecoes, sem_teor = [], [], []
    for p in alvo:
        teor, partes = teor_e_partes(pasta, p.get("teor", ""))
        if not teor:
            sem_teor.append(p)
            excecoes.append((p, "sem teor guardado"))
            continue
        norm = normalizar(teor, partes)
        pf = perfil(norm)
        item = {"pub": p, "teor": teor, "norm": norm, "perfil": pf, "palavras": norm.split()}
        if carteira is not None and digitos(p.get("processo", "")) not in carteira:
            excecoes.append((p, "sem caso na carteira: triagem uma a uma, para a pessoa"))
            continue
        if "urgente" in pf[3] or pf[1]:
            excecoes.append((p, "sinal de urgência ou prazo em horas: triagem uma a uma, PESSOA AGORA"))
            continue
        itens.append(item)

    # 1. iguais
    por_texto = {}
    for it in itens:
        por_texto.setdefault((it["norm"], it["perfil"]), []).append(it)
    blocos = list(por_texto.values())
    # 2. quase iguais, só dentro do mesmo perfil
    por_perfil = {}
    for b in blocos:
        por_perfil.setdefault(b[0]["perfil"], []).append(b)
    grupos = []
    for pf, bs in por_perfil.items():
        pai = list(range(len(bs)))

        def raiz(i):
            while pai[i] != i:
                pai[i] = pai[pai[i]]
                i = pai[i]
            return i
        sims = {}
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                s = semelhanca(bs[i][0]["palavras"], bs[j][0]["palavras"], a.limiar)
                if s >= a.limiar:
                    ri, rj = raiz(i), raiz(j)
                    if ri != rj:
                        pai[rj] = ri
                    sims[(i, j)] = s
        juntos = {}
        for i in range(len(bs)):
            juntos.setdefault(raiz(i), []).append(i)
        for idxs in juntos.values():
            membros = [it for i in idxs for it in bs[i]]
            menor = min([sims.get((min(i, j), max(i, j)), 1.0) for i in idxs for j in idxs if i < j] or [1.0])
            grupos.append({"membros": sorted(membros, key=lambda x: x["pub"]["id"]), "perfil": pf,
                           "tipo": "igual" if len(idxs) == 1 else "quase igual", "menor_semelhanca": menor})
    sozinhos = [g for g in grupos if len(g["membros"]) == 1]
    grupos = sorted([g for g in grupos if len(g["membros"]) > 1], key=lambda g: (-len(g["membros"]), g["membros"][0]["pub"]["id"]))
    for g in sozinhos:
        excecoes.append((g["membros"][0]["pub"], "teor sem par no lote: triagem uma a uma"))

    linhas_csv = []
    rel = [f"---", "documento: Triagem em massa", f"data: {hoje}", "feito_por: ia (agrupamento sugerido)",
           f"treino: {'sim' if '_treino' in pasta.replace(os.sep, '/').split('/') else 'nao'}", "---", "",
           f"# Triagem em massa de {hoje}", "",
           f"{len(alvo)} publicações a triar · {len(grupos)} grupos com {sum(len(g['membros']) for g in grupos)} publicações · "
           f"{len(excecoes)} exceções para triar uma a uma.", "",
           "Cada grupo recebe uma triagem e uma providência depois que a pessoa lê a amostra inteira. "
           "A conta do prazo continua uma por publicação (calcular-prazo ou prazos-em-lote).", ""]
    for n, g in enumerate(grupos, start=1):
        gid = f"G{n:02d}"
        g["id"] = gid
        membros = g["membros"]
        k = min(len(membros), max(2, math.ceil(math.sqrt(len(membros)))))
        rnd = random.Random(f"{hoje}-{gid}-{membros[0]['pub']['id']}")
        meio = membros[1:-1]
        amostra = [membros[0]] + ([membros[-1]] if len(membros) > 1 else [])
        amostra += rnd.sample(meio, max(0, min(len(meio), k - len(amostra))))
        ids_amostra = {m["pub"]["id"] for m in amostra}
        rep = membros[0]
        datas_variam = "<data>" in rep["norm"]
        rel += [f"## {gid} · {len(membros)} publicações · {g['tipo']}"
                + (f" (menor semelhança {g['menor_semelhanca']:.2f})" if g["tipo"] == "quase igual" else ""), "",
                f"- Perfil: {descreve_perfil(g['perfil'])}",
                f"- Representante: {rep['pub']['id']} · {rep['pub'].get('tribunal', '')} · {rep['pub'].get('orgao', '')}",
                f"- Teor do representante: \"{rep['teor'][:400]}{'...' if len(rep['teor']) > 400 else ''}\"",
                f"- Amostra para ler inteira ({len(amostra)}): {', '.join(sorted(ids_amostra))}",
                f"- Todos: {', '.join(m['pub']['id'] for m in membros)}"]
        if datas_variam:
            rel.append("- As datas mudam de um ato para outro: a triagem é a mesma, mas cada linha leva a sua data")
        if g["tipo"] == "quase igual":
            variantes, vistos = [], {rep["norm"]}
            for m in membros:
                if m["norm"] not in vistos:
                    vistos.add(m["norm"])
                    variantes.append(m)
            for m in variantes[:5]:
                so_rep, so_m = diferencas(rep["norm"], m["norm"])
                n_var = sum(1 for x in membros if x["norm"] == m["norm"])
                rel.append(f"- Variante {m['pub']['id']} ({n_var} com este texto): sai \"{' '.join(so_rep)}\" · "
                           f"entra \"{' '.join(so_m)}\". Se a diferença muda o que fazer, a variante sai do grupo")
            if len(variantes) > 5:
                rel.append(f"- Mais {len(variantes) - 5} variantes: leia a lista inteira antes de aplicar")
        rel += ["- Triagem do grupo: [A DEFINIR pela pessoa, depois da amostra]", ""]
        for m in membros:
            linhas_csv.append({"grupo": gid, "id": m["pub"]["id"], "papel": "amostra" if m["pub"]["id"] in ids_amostra else "membro",
                               "processo": m["pub"].get("processo", ""), "perfil": descreve_perfil(g["perfil"])})
    rel += ["## Exceções (uma a uma, pela triar-publicacoes)", ""]
    for p, motivo in sorted(excecoes, key=lambda x: x[0]["id"]):
        rel.append(f"- {p['id']} · {p.get('tribunal', '')} · {p.get('processo', '')} · {motivo}")
        linhas_csv.append({"grupo": "excecao", "id": p["id"], "papel": "excecao", "processo": p.get("processo", ""),
                           "perfil": motivo})
    texto = "\n".join(rel).rstrip() + "\n"

    if a.gravar:
        destino = os.path.join(pasta, "lotes")
        os.makedirs(destino, exist_ok=True)
        with open(os.path.join(destino, f"{hoje}-grupos.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["grupo", "id", "papel", "processo", "perfil"], lineterminator="\n")
            w.writeheader()
            for l in linhas_csv:
                w.writerow(l)
        with open(os.path.join(destino, f"{hoje}-triagem-em-massa.md"), "w", encoding="utf-8") as f:
            f.write(texto)
    print(texto)
    if a.gravar:
        print(f"Gravado: {os.path.join(pasta, 'lotes', hoje + '-grupos.csv')} e {hoje}-triagem-em-massa.md")
    else:
        print("SIMULAÇÃO: nada gravado (use --gravar).")
    if carteira is None:
        print("AVISO: sem --processos, o sem caso não foi separado. Rode com a carteira de processos.")
    return 0


def cmd_aplicar(a):
    hoje = a.hoje or dt.date.today().isoformat()
    if not a.amostra_conferida:
        erro("antes de aplicar a triagem ao grupo, a pessoa lê a amostra inteira. Quando ela disser que leu e "
             "que a triagem vale para todos, rode de novo com --amostra-conferida")
    grupos, _, _ = ler_csv(a.grupos, ["grupo", "id", "papel"])
    ids = [g["id"] for g in grupos if g["grupo"] == a.grupo]
    if not ids:
        erro(f"o grupo {a.grupo} não está em {a.grupos}")
    fora = {i.strip() for i in (a.fora or "").split(",") if i.strip()}
    desconhecidos = fora - set(ids)
    if desconhecidos:
        erro("não são do grupo " + a.grupo + ": " + ", ".join(sorted(desconhecidos)))
    ids = [i for i in ids if i not in fora]
    pubs, delim, bom = ler_csv(a.publicacoes, ["id", "processo", "triagem"])
    if a.triagem in ("ciencia", "sem-providencia") and not a.li_todas:
        pasta_pub = os.path.dirname(os.path.abspath(a.publicacoes))
        pedem = []
        for p in pubs:
            if p["id"] in ids:
                teor, _ = teor_e_partes(pasta_pub, p.get("teor", ""))
                if not teor or pede_algo_ao_cliente(teor):
                    pedem.append(p["id"])
        if pedem:
            erro(f"o grupo {a.grupo} tem atos que podem pedir algo à parte do cliente (número de dias, 'diga', 'no prazo legal', "
                 f"'manifeste-se', 'intime-se a parte'): {', '.join(pedem[:10])}{' ...' if len(pedem) > 10 else ''}. "
                 f"A amostra não basta para marcar {a.triagem}: aplique --triagem prazo (os dias ficam [A CONFIRMAR] quando "
                 "o ato não diz) ou trie uma a uma na triar-publicacoes. Só se a pessoa disser que leu todas, e não só a amostra, "
                 "rode com --li-todas")
    carteira = {}
    if a.processos:
        procs, _, _ = ler_csv(a.processos, ["processo", "codigo_caso", "cliente_curto"])
        carteira = {digitos(p["processo"]): p for p in procs}
    mudou, pulou = [], []
    for p in pubs:
        if p["id"] not in ids:
            continue
        if p.get("triagem") not in ("nao-triada",) and p.get("triada_por", "") not in ("", "ia"):
            pulou.append((p["id"], f"já triada por {p.get('triada_por')}"))
            continue
        if p.get("triagem") == "duplicada":
            pulou.append((p["id"], "duplicada"))
            continue
        linha = carteira.get(digitos(p.get("processo", "")))
        if a.processos and not linha:
            p["triagem"] = "sem-caso"
            p["codigo_caso"] = ""
            p["resumo"] = "Processo fora da carteira: para a pessoa"
            pulou.append((p["id"], "sem caso na carteira: ficou sem-caso"))
        else:
            p["triagem"] = a.triagem
            if linha:
                p["codigo_caso"] = linha.get("codigo_caso", "")
                p["cliente_curto"] = linha.get("cliente_curto", "")
            p["resumo"] = (f"Grupo {a.grupo} ({hoje}): {a.resumo}" if a.resumo else f"Grupo {a.grupo} ({hoje}): triagem {a.triagem}")[:120]
            mudou.append(p["id"])
        p["triada_por"] = a.por
        p["atualizado_em"] = hoje
    if a.gravar:
        cab = list(pubs[0].keys())
        with open(a.publicacoes, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cab, delimiter=delim, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            for p in pubs:
                w.writerow(p)
    print(f"GRUPO {a.grupo} · triagem {a.triagem} · por {a.por} · {len(mudou)} publicações"
          + (" · gravado" if a.gravar else " · SIMULAÇÃO (use --gravar)"))
    if pulou:
        for i, m in pulou:
            print(f"  fora: {i} · {m}")
    if a.triagem == "prazo":
        print("Próximo passo: a conta de cada uma (calcular-prazo, ou prazos-em-lote se instalada). Nada vai para a agenda "
              "sem a dupla conferência.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Agrupa publicações de teor igual ou quase igual")
    sub = ap.add_subparsers(dest="cmd")
    g = sub.add_parser("agrupar")
    g.add_argument("publicacoes")
    g.add_argument("--processos")
    g.add_argument("--limiar", type=float, default=0.9, help="semelhança mínima para quase igual (0 a 1)")
    g.add_argument("--todas", action="store_true")
    g.add_argument("--hoje")
    g.add_argument("--gravar", action="store_true")
    p = sub.add_parser("aplicar")
    p.add_argument("grupos")
    p.add_argument("--publicacoes", required=True)
    p.add_argument("--grupo", required=True)
    p.add_argument("--triagem", required=True, choices=TRIAGENS_DE_GRUPO)
    p.add_argument("--resumo", help="resumo sem dado sensível, até 120 caracteres")
    p.add_argument("--processos")
    p.add_argument("--por", default="ia", help="ia, ou o nome de quem decidiu, só quando a pessoa disse na conversa")
    p.add_argument("--amostra-conferida", action="store_true")
    p.add_argument("--li-todas", dest="li_todas", action="store_true",
                   help="ciencia ou sem-providencia em grupo com ato que pede algo: só quando a pessoa disse que leu todas, não só a amostra")
    p.add_argument("--fora", help="ids que a pessoa tirou do grupo (variante que pede outra coisa), separados por vírgula")
    p.add_argument("--hoje")
    p.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    if a.cmd == "agrupar":
        if not 0 < a.limiar <= 1:
            erro("--limiar entre 0 e 1")
        return cmd_agrupar(a)
    if a.cmd == "aplicar":
        return cmd_aplicar(a)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
