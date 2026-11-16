#!/usr/bin/env python3
"""Cruza as partes de um caso novo com a base de partes do escritório (motor-juridico).

Lê 04-base/juridico/partes.csv (clientes e partes contrárias de casos anteriores) e as
partes do caso novo, e aponta:

  coincidência  mesmo CNPJ, ou o mesmo nome depois de normalizar (minúsculas, sem acento,
                sem pontuação, sem sufixo societário como Ltda., ME, EPP, Eireli, S.A.)
  semelhança    mesma raiz de CNPJ (matriz e filial, mesmo grupo), o mesmo nome sem as
                palavras genéricas (restaurante, comércio, serviços), nomes quase iguais
                (erro de digitação) ou a maior parte das palavras em comum
  fraca         só o primeiro nome bate com um nome curto da base

E diz o que cada coincidência significa pelo papel: parte contrária do caso novo que é ou
foi cliente, novo cliente que foi parte contrária, cliente repetido, parte contrária repetida.
O script não decide nada: a decisão de aceitar o caso é do advogado. Só biblioteca padrão
(Python 3.9+). Não altera a base.

Uso:
  python3 checar_conflito.py CAMINHO/partes.csv --caso C-AAAA-NNNN \
    --parte "NOME; papel; CNPJ" [--parte ...] [--novas ARQUIVO.csv] [--saida ARQUIVO.md]

Opções:
  --caso CODIGO      o código do caso novo (C-AAAA-NNNN)
  --parte TEXTO      uma parte do caso novo: "nome; papel" ou "nome; papel; CNPJ" (separador
                     ponto e vírgula ou barra vertical). Papel: cliente, parte-contraria ou outra.
                     Repita para cada parte
  --novas ARQUIVO    as partes do caso novo num csv com as colunas nome, papel e, se houver, cnpj
  --saida ARQUIVO    grava o registro da checagem (cria o arquivo ou acrescenta uma seção)
  --data AAAA-MM-DD  data da checagem (padrão: hoje)
  --treino           permite ler a base de treino (pasta _treino)

Colunas da base: nome, papel, codigo_caso (obrigatórias); cnpj, area, ano, situacao,
observacao (opcionais). Sai com código 1 e "ERRO:" quando falta a base, ela está vazia,
falta coluna obrigatória, nenhuma parte nova foi informada, ou recebe a base de treino sem
--treino. Nunca diz "nada encontrado" sem ter lido a base.
"""
import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

OBRIGATORIAS = ["nome", "papel", "codigo_caso"]
OPCIONAIS = ["cnpj", "area", "ano", "situacao", "observacao"]
SUFIXOS = {
    "ltda", "limitada", "me", "epp", "eireli", "sa", "cia", "companhia", "mei", "ss", "slu",
    "sociedade", "empresaria", "simples", "unipessoal", "filial", "matriz", "holding",
}
LIGACAO = {"de", "da", "do", "das", "dos", "e", "em", "na", "no", "the", "and"}
GENERICAS = {
    "restaurante", "bar", "lanchonete", "padaria", "comercio", "comercial", "servicos", "servico",
    "industria", "industrial", "transportes", "transporte", "construtora", "construcoes", "empresa",
    "grupo", "loja", "lojas", "distribuidora", "mercado", "supermercado", "farmacia", "drogaria",
    "clinica", "hospital", "escola", "colegio", "consultoria", "associacao", "condominio", "banco",
    "administradora", "imobiliaria", "agropecuaria", "engenharia", "tecnologia", "solucoes",
    "participacoes", "representacoes", "importacao", "exportacao", "alimentos", "advogados",
    "advocacia", "brasil", "nacional",
}
CONTRARIA = {"parte-contraria", "contraria", "parte contraria", "adversa", "adverso", "re", "reu", "requerido"}
NIVEL_ORDEM = {"coincidência": 0, "semelhança": 1, "fraca": 2}


def falhar(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def sem_acento(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto or "") if not unicodedata.combining(c))


def papel(texto):
    t = sem_acento((texto or "").strip()).lower()
    t = re.split(r"[(,]", t)[0].strip()
    t = re.sub(r"[\s_]+", "-", t)
    if t.startswith("cliente") or t.startswith("ex-cliente"):
        return "cliente"
    if t in CONTRARIA or t.replace("-", " ") in CONTRARIA or t.startswith("parte-contr") or t.startswith("contr"):
        return "parte-contraria"
    return "outra"


def tokens(nome):
    t = sem_acento(nome or "").lower().replace("&", " e ")
    t = re.sub(r"\bs\s*[/.]?\s*a\b\.?", " ", t)  # S.A., S/A
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return [x for x in t.split() if x not in SUFIXOS and x not in LIGACAO and len(x) > 1]


def normalizado(nome):
    return " ".join(tokens(nome))


def distintivos(nome):
    return [x for x in tokens(nome) if x not in GENERICAS]


def digitos(cnpj):
    d = re.sub(r"\D", "", cnpj or "")
    return d if len(d) == 14 else ""


def decodificar(bruto):
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(cod)
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace")


def ler_csv(caminho, obrigatorias, rotulo):
    p = Path(caminho)
    if not p.is_file():
        if rotulo == "a base de partes":
            falhar(f"Não há base de partes (partes.csv). Pergunte ao advogado e registre a checagem sem base. "
                   f"(Procurei em `{caminho}`; o padrão é escritorio/04-base/juridico/partes.csv. Nada foi "
                   "checado, então não dá para dizer que não há conflito.)")
        falhar(f"não encontrei {rotulo} em `{caminho}`.")
    texto = decodificar(p.read_bytes())
    linhas = texto.splitlines()
    if linhas and linhas[0].strip().lower().startswith("sep="):
        linhas = linhas[1:]
    if not linhas or not "".join(linhas).strip():
        falhar(f"{rotulo} em `{caminho}` está vazia, sem nem a primeira linha. Nada foi checado.")
    sep = ";" if linhas[0].count(";") > linhas[0].count(",") else ","
    leitor = csv.reader(io.StringIO("\n".join(linhas)), delimiter=sep)
    cab = [re.sub(r"[\s-]+", "_", sem_acento(c).strip().lower()) for c in next(leitor)]
    faltam = [c for c in obrigatorias if c not in cab]
    if faltam:
        falhar(f"faltam colunas ({rotulo}): {', '.join(faltam)}. Colunas encontradas: "
               f"{', '.join(c for c in cab if c) or 'nenhuma'}. A primeira linha da base é: "
               "nome,cnpj,papel,codigo_caso,area,ano,situacao,observacao")
    saida = []
    for n, valores in enumerate(leitor, start=2):
        if not any(v.strip() for v in valores):
            continue
        l = {c: (valores[i].strip() if i < len(valores) else "") for i, c in enumerate(cab) if c}
        l["_linha"] = n
        saida.append(l)
    return saida, sep, [c for c in OPCIONAIS if c not in cab]


def comparar(nova, antiga):
    """Devolve (nível, por quê) ou None."""
    c1, c2 = digitos(nova.get("cnpj")), digitos(antiga.get("cnpj"))
    if c1 and c2:
        if c1 == c2:
            return "coincidência", "mesmo CNPJ"
        if c1[:8] == c2[:8]:
            return "semelhança", "mesma raiz de CNPJ (matriz e filial, ou o mesmo grupo)"
    n1, n2 = normalizado(nova["nome"]), normalizado(antiga["nome"])
    if not n1 or not n2:
        return None
    if n1 == n2:
        return "coincidência", "mesmo nome, sem acento e sem sufixo societário"
    d1, d2 = distintivos(nova["nome"]), distintivos(antiga["nome"])
    if d1 and d2 and d1 == d2 and (len(d1) >= 2 or len(d1[0]) >= 6):
        return "semelhança", "mesmo nome sem as palavras genéricas (" + " ".join(d1) + ")"
    razao = SequenceMatcher(None, n1, n2).ratio()
    if razao >= 0.88:
        return "semelhança", f"nomes quase iguais ({razao:.0%} parecidos), pode ser erro de digitação"
    s1, s2 = set(d1), set(d2)
    comuns = s1 & s2
    if len(comuns) >= 2 and len(comuns) / len(s1 | s2) >= 0.5:
        return "semelhança", "a maior parte das palavras em comum (" + " ".join(sorted(comuns)) + ")"
    t1, t2 = n1.split(), n2.split()
    if (len(t2) == 1 and t1 and t1[0] == t2[0]) or (len(t1) == 1 and t2 and t2[0] == t1[0]):
        return "fraca", "só o primeiro nome bate; a base guarda nome curto: conferir no sistema do escritório"
    return None


def significado(p_nova, p_antiga):
    if p_nova == "parte-contraria" and p_antiga == "cliente":
        return "CONFLITO PROVÁVEL: a parte contrária do caso novo é ou foi cliente do escritório"
    if p_nova == "cliente" and p_antiga == "parte-contraria":
        return "CONFLITO PROVÁVEL: o novo cliente foi parte contrária de um cliente do escritório"
    if p_nova == "cliente" and p_antiga == "cliente":
        return "já é ou foi cliente: não é conflito por si; conferir se o caso novo vai contra outro cliente"
    if p_nova == "parte-contraria" and p_antiga == "parte-contraria":
        return "já foi parte contrária em outro caso: sem conflito aparente; fica registrado"
    return "papel diferente de cliente e parte contrária: o advogado confere"


def ler_parte(texto):
    partes = [x.strip() for x in re.split(r"[;|]", texto)]
    if not partes or not partes[0]:
        falhar(f"--parte vazia: `{texto}`. Use \"nome; papel\" ou \"nome; papel; CNPJ\".")
    if len(partes) < 2 or not partes[1]:
        falhar(f"--parte sem papel: `{texto}`. Diga se é cliente, parte-contraria ou outra.")
    return {"nome": partes[0], "papel": partes[1], "cnpj": partes[2] if len(partes) > 2 else "", "_linha": "-"}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("base", nargs="?", default="")
    p.add_argument("--caso", required=True)
    p.add_argument("--parte", action="append", default=[])
    p.add_argument("--novas")
    p.add_argument("--saida")
    p.add_argument("--data")
    p.add_argument("--treino", action="store_true")
    args = p.parse_args()
    if not args.base.strip():
        falhar("Não há base de partes (partes.csv). Pergunte ao advogado e registre a checagem sem base. "
               "(Nenhum caminho de partes.csv foi passado; o padrão é escritorio/04-base/juridico/partes.csv.)")

    if "_treino" in Path(args.base).parts and not args.treino:
        falhar(f"`{args.base}` é a base de treino. Para ler mesmo assim, rode com --treino.")
    if not re.fullmatch(r"C-\d{4}-\d{4}(-\d+)?", args.caso.strip(), re.I):
        falhar(f"código do caso `{args.caso}` fora do padrão C-AAAA-NNNN.")
    try:
        hoje = date.fromisoformat(args.data) if args.data else date.today()
    except ValueError:
        falhar(f"--data `{args.data}` inválida. Use AAAA-MM-DD.")

    novas = [ler_parte(t) for t in args.parte]
    if args.novas:
        lidas, _, _ = ler_csv(args.novas, ["nome", "papel"], "o arquivo das partes novas")
        novas.extend(lidas)
    if not novas:
        falhar("nenhuma parte do caso novo foi informada. Use --parte \"nome; papel\" para cada parte "
               "(cliente, parte contrária e quem mais estiver no caso), ou --novas com um csv.")

    base, sep, ausentes = ler_csv(args.base, OBRIGATORIAS, "a base de partes")
    caso = args.caso.strip().upper()
    achados = []
    for nova in novas:
        for antiga in base:
            if (antiga.get("codigo_caso") or "").strip().upper() == caso:
                continue
            r = comparar(nova, antiga)
            if r:
                pn, pa = papel(nova["papel"]), papel(antiga["papel"])
                achados.append({"nivel": r[0], "porque": r[1], "nova": nova, "antiga": antiga,
                                "pn": pn, "pa": pa, "sig": significado(pn, pa)})
    achados.sort(key=lambda a: (0 if a["sig"].startswith("CONFLITO") else 1, NIVEL_ORDEM[a["nivel"]]))
    provaveis = [a for a in achados if a["sig"].startswith("CONFLITO") and a["nivel"] != "fraca"]

    out = [f"## Checagem de conflito · {caso} · {hoje:%Y-%m-%d}", ""]
    if provaveis:
        out.append(f"**ACUSOU: {len(provaveis)} coincidência(s) com conflito provável.** A habilidade para aqui: "
                   "aceitar o caso, recusar ou pedir mais informação é decisão do advogado.")
    elif achados:
        out.append(f"**{len(achados)} coincidência(s) para o advogado olhar, sem conflito provável pelo papel.** "
                   "A decisão de aceitar continua do advogado.")
    else:
        out.append(f"**Nada encontrado nos {len(base)} registros da base.** Isso diz só o que a base sabe: "
                   "a decisão de aceitar continua do advogado.")
    out.append("")
    out.append(f"Base lida: `{args.base}`, {len(base)} registro(s)"
               + (", separada por ponto e vírgula" if sep == ";" else "")
               + (f"; colunas opcionais ausentes: {', '.join(ausentes)}" if ausentes else "") + ".")
    out.append("")
    out.append("Partes checadas:")
    for n in novas:
        out.append(f"- {n['nome']} · {papel(n['papel'])}" + (" · CNPJ informado" if digitos(n.get("cnpj")) else ""))
    out.append("")
    if achados:
        out.append("| Nível | Parte do caso novo | Papel | Na base | Papel na base | Caso | Por quê | O que significa |")
        out.append("|---|---|---|---|---|---|---|---|")
        for a in achados:
            out.append(f"| {a['nivel']} | {a['nova']['nome']} | {a['pn']} | {a['antiga']['nome']} | {a['pa']} | "
                       f"{a['antiga'].get('codigo_caso', '')} | {a['porque']} | {a['sig']} |")
        out.append("")
    out.append("Decisão do advogado: [A DEFINIR] (aceitar | recusar | aceitar depois de ouvir os envolvidos, "
               "como manda o Código de Ética e Disciplina da OAB [CONFERIR: artigos sobre conflito de "
               "interesses e sigilo, redação vigente])")
    out.append("Quem decidiu: [A DEFINIR] · Em: [A DEFINIR]")
    out.append("")
    out.append("Gerado pelo script da conflito-de-interesses. A base não foi alterada.")
    texto = "\n".join(out)
    print(texto)

    if args.saida:
        destino = Path(args.saida)
        destino.parent.mkdir(parents=True, exist_ok=True)
        if destino.exists():
            with destino.open("a", encoding="utf-8") as f:
                f.write("\n\n" + texto + "\n")
        else:
            cab = (f"---\ndocumento: Checagem de conflito de interesses · {caso}\nversao: 1\n"
                   f"revisado_em: {hoje:%Y-%m-%d}\ndono: [A PREENCHER]\n---\n\n"
                   f"# Conflito de interesses · {caso}\n\n")
            destino.write_text(cab + texto + "\n", encoding="utf-8")
        print(f"\nRegistro da checagem em `{destino}`.")


if __name__ == "__main__":
    main()
