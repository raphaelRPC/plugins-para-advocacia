#!/usr/bin/env python3
"""O registro dos painéis dos sistemas (07-operacao/controladoria/paineis/AAAA-MM-DD.md).

A IA nunca abre painel de tribunal, nunca usa senha, certificado ou token. Este script só
trabalha com o que a pessoa registrou.

Comandos:
  modelo --roteiro paineis.md --data AAAA-MM-DD [--quem <função>]
      Escreve na tela o registro do dia em branco, com os sistemas do roteiro, para a pessoa preencher.

  conferir <registro.md> [--roteiro paineis.md] [--regras regras-de-contagem.md] [--hoje AAAA-MM-DD]
      Confere o registro: sistemas do roteiro que ninguém olhou, intimação sem trecho, sem data de envio
      ou sem a situação da ciência, aberta sem a data da abertura; e calcula a ciência tácita prevista
      (envio + o prazo de ciência da tabela, em dias corridos) para apontar a que vence em até 2 dias úteis.
      A data exata da ciência e do prazo é da calcular-prazo; abrir ou esperar é decisão da pessoa.

Código 1 quando falta arquivo, seção ou coluna, ou quando o registro está vazio.
"""
import argparse
import datetime as dt
import os
import re
import sys
import unicodedata

COL_SISTEMAS = ["sistema", "tribunal", "quem", "hora", "situacao", "observacao"]
COL_VISTAS = ["sistema", "tribunal", "orgao", "processo", "enviada_em", "ciencia", "aberta_em", "prazo_no_painel",
              "tipo_ato", "trecho"]
COL_ROTEIRO = ["sistema", "tribunal", "quem_olha", "quando", "o_que_olhar", "substituto"]
CIENCIAS = ["sem-ciencia", "aberta", "tacita"]
SITUACOES = ["olhado", "nao-olhado", "fora-do-ar"]


def erro(msg):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(1)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def chave(nome):
    return re.sub(r"[^a-z0-9]+", "_", sem_acento((nome or "").strip().lower())).strip("_")


def ler(caminho):
    if not os.path.exists(caminho):
        erro(f"não encontrei {caminho}")
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return bruto.decode(enc)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def data_iso(v):
    v = (v or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v) or None
    if m:
        a, mes, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})", v)
        if not m:
            return ""
        d, mes, a = m.groups()
    try:
        return dt.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return ""


def tabela(texto, titulo, colunas, origem, obrigatoria=True):
    m = re.search(r"(?im)^##\s+" + re.escape(titulo) + r"\s*$", texto)
    if not m:
        if obrigatoria:
            erro(f"{origem}: falta a seção '## {titulo}'")
        return None
    resto = texto[m.end():]
    prox = re.search(r"(?m)^##\s", resto)
    resto = resto[:prox.start()] if prox else resto
    linhas = [l.strip() for l in resto.splitlines() if l.strip().startswith("|")]
    if not linhas:
        return []
    cab = [chave(c) for c in linhas[0].strip("|").split("|")]
    faltam = [c for c in colunas if c not in cab]
    if faltam:
        erro(f"{origem}, seção '{titulo}': faltam as colunas {', '.join(faltam)}. Colunas: {' | '.join(colunas)}")
    saida = []
    for l in linhas[2:]:
        cel = [c.strip() for c in l.strip("|").split("|")]
        cel += [""] * (len(cab) - len(cel))
        d = dict(zip(cab, cel))
        if any(v.strip() for v in d.values()):
            saida.append(d)
    return saida


def mais_dias_uteis(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def prazo_ciencia(regras):
    if not regras:
        return None
    for l in ler(regras).splitlines():
        if "intimacao-portal" in l:
            m = re.search(r"(\d+)\s+dias\s+corridos", sem_acento(l))
            if m:
                return int(m.group(1))
    return None


def cmd_modelo(a):
    data = data_iso(a.data)
    if not data:
        erro("--data em AAAA-MM-DD")
    sistemas = tabela(ler(a.roteiro), "Os painéis", COL_ROTEIRO, a.roteiro)
    if not sistemas:
        erro(f"{a.roteiro}: o roteiro não tem nenhum painel na tabela '## Os painéis'")
    print("---\ndocumento: Registro dos painéis\n" + f"data: {data}\nquem_registrou: {a.quem or '[A PREENCHER]'}\ntreino: nao\n---\n")
    print(f"# Painéis de {data}\n")
    print("Registro do que a pessoa viu nos painéis dos sistemas, com a própria senha ou certificado. A IA não abre painel.\n")
    print("## Sistemas olhados\n\n| sistema | tribunal | quem | hora | situacao | observacao |\n|---|---|---|---|---|---|")
    for s in sistemas:
        print(f"| {s['sistema']} | {s['tribunal']} | {s['quem_olha']} | [A PREENCHER] | [A PREENCHER] | |")
    print("\n## Intimações e comunicações vistas\n\n| sistema | tribunal | orgao | processo | enviada_em | ciencia | aberta_em "
          "| prazo_no_painel | tipo_ato | trecho |\n|---|---|---|---|---|---|---|---|---|---|")
    print("\n## O que ficou para decidir\n\n- ")
    return 0


def cmd_conferir(a):
    hoje = data_iso(a.hoje) if a.hoje else dt.date.today().isoformat()
    texto = ler(a.registro)
    m = re.search(r"(?im)^data:\s*(\S+)", texto)
    data_reg = data_iso(m.group(1)) if m else ""
    sistemas = tabela(texto, "Sistemas olhados", COL_SISTEMAS, a.registro)
    vistas = tabela(texto, "Intimações e comunicações vistas", COL_VISTAS, a.registro)
    if not sistemas and not vistas:
        erro(f"{a.registro}: registro sem nenhuma linha. Sem registro, os painéis contam como não olhados")
    problemas, agora, avisos = [], [], []
    if not data_reg:
        problemas.append("cabeçalho sem 'data: AAAA-MM-DD'")
    for s in sistemas:
        sit = chave(s.get("situacao", "")).replace("_", "-")
        if sit not in SITUACOES:
            problemas.append(f"{s['sistema']} {s['tribunal']}: situação '{s.get('situacao', '')}' (use {', '.join(SITUACOES)})")
        elif sit != "olhado":
            agora.append(f"{s['sistema']} {s['tribunal']}: {sit} ({s.get('observacao', '')}). Quem olha e quando? "
                         "Se o sistema esteve fora do ar, guarde a certidão de indisponibilidade, se o tribunal publicar")
    if a.roteiro:
        roteiro = tabela(ler(a.roteiro), "Os painéis", COL_ROTEIRO, a.roteiro)
        feitos = {(chave(s["sistema"]), chave(s["tribunal"])) for s in sistemas}
        for r in roteiro or []:
            if (chave(r["sistema"]), chave(r["tribunal"])) not in feitos:
                agora.append(f"{r['sistema']} {r['tribunal']}: está no roteiro e não foi registrado hoje "
                             f"(quem olha: {r.get('quem_olha', '')}; substituto: {r.get('substituto', '') or '[A PREENCHER]'})")
    n = prazo_ciencia(a.regras)
    if n is None:
        avisos.append("prazo de ciência do portal: 10 dias corridos, pela tabela de partida [CONFERIR]; passe --regras "
                      "com a tabela validada do escritório")
        n = 10
    limite = mais_dias_uteis(dt.date.fromisoformat(hoje), 2).isoformat()
    tacitas = []
    for i, v in enumerate(vistas, start=1):
        rot = f"intimação {i} ({v.get('tribunal', '')} {v.get('processo', '') or 'sem processo'})"
        cien = chave(v.get("ciencia", "")).replace("_", "-")
        env = data_iso(v.get("enviada_em", ""))
        aberta = data_iso(v.get("aberta_em", ""))
        if len(re.sub(r"\D", "", v.get("processo", ""))) != 20:
            problemas.append(f"{rot}: número do processo fora do padrão CNJ, conferir")
        if not v.get("trecho"):
            problemas.append(f"{rot}: sem o trecho do ato. Sem o trecho não há o que conferir")
        if not env:
            problemas.append(f"{rot}: sem a data de envio (enviada_em). Sem ela não há ciência tácita a contar")
        if env and env > hoje:
            problemas.append(f"{rot}: data de envio no futuro ({env})")
        if cien not in CIENCIAS:
            problemas.append(f"{rot}: ciência '{v.get('ciencia', '')}' (use {', '.join(CIENCIAS)})")
        if cien == "aberta" and not aberta:
            problemas.append(f"{rot}: marcada como aberta sem a data da abertura (aberta_em). A ciência é a abertura")
        if cien == "sem-ciencia" and env:
            tac = (dt.date.fromisoformat(env) + dt.timedelta(days=n)).isoformat()
            tacitas.append((rot, env, tac))
            if tac <= limite:
                agora.append(f"{rot}: ciência tácita prevista para {tac} (envio {env} + {n} dias corridos), em até 2 dias "
                             "úteis. Abrir agora ou esperar é decisão da pessoa; se abrir, registre aberta_em e a conta muda")
        if v.get("prazo_no_painel"):
            avisos.append(f"{rot}: o painel mostra '{v['prazo_no_painel']}'. Vale como conferência, não como conta: "
                          "a conta é da calcular-prazo")
    print(f"REGISTRO DOS PAINÉIS · {data_reg or '[sem data]'} · conferido em {hoje}")
    print(f"Sistemas registrados: {len(sistemas)} · intimações registradas: {len(vistas)}")
    print("\nPESSOA AGORA" + ("" if agora else ": nada"))
    for x in agora:
        print(f"  - {x}")
    if tacitas:
        print("\nCIÊNCIA TÁCITA PREVISTA (só para ordenar; a data que vale sai da calcular-prazo, com o calendário):")
        for rot, env, tac in sorted(tacitas, key=lambda t: t[2]):
            print(f"  {tac} · {rot} · enviada {env}")
    if problemas:
        print("\nCORRIGIR NO REGISTRO:")
        for x in problemas:
            print(f"  - {x}")
    if avisos:
        print("\nAVISOS:")
        for x in avisos:
            print(f"  - {x}")
    print("\nPróximo passo: importar o registro na captar-publicacoes (importar_publicacoes.py <registro> --registro ...).")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Roteiro e registro dos painéis dos sistemas")
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("modelo")
    m.add_argument("--roteiro", required=True)
    m.add_argument("--data", required=True)
    m.add_argument("--quem")
    c = sub.add_parser("conferir")
    c.add_argument("registro")
    c.add_argument("--roteiro")
    c.add_argument("--regras")
    c.add_argument("--hoje")
    a = ap.parse_args()
    if a.cmd == "modelo":
        return cmd_modelo(a)
    if a.cmd == "conferir":
        return cmd_conferir(a)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
