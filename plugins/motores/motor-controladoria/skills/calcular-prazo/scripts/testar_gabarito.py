#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
testar_gabarito.py · roda o calcular_prazo.py contra o gabarito de docs/casos-ficticios.md
(lote de 2026-04-14, linhas 1, 3, 4, 8 e 10; exercícios E1 a E3) com o calendário e as regras
de treino, e mais os casos extras que protegem as regras de contagem.md.

Uso:
  python3 testar_gabarito.py            (mostra OK ou FALHOU em cada caso)
  python3 testar_gabarito.py --detalhe  (mostra também a saída do script quando falha)

Sai com código 0 se tudo passou e 1 se algum caso falhou. Os arquivos temporários do teste
vão para a pasta temporária do sistema, nunca para a pasta do plugin.
"""

import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(AQUI, "calcular_prazo.py")
ASSETS = os.path.normpath(os.path.join(AQUI, "..", "..", "calendario-forense", "assets"))
CAL = os.path.join(ASSETS, "calendario-de-treino.md")
REGRAS = os.path.join(ASSETS, "regras-de-treino.md")
HOJE = "2026-04-14"
DETALHE = "--detalhe" in sys.argv

resultados = []


def rodar(args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-B", SCRIPT] + args, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def registrar(nome, ok, detalhe=""):
    resultados.append((nome, ok))
    print("%-8s %s%s" % ("OK" if ok else "FALHOU", nome, "" if ok else "  · " + detalhe))


def conta(nome, args, esperado, avisos=(), pulados=(), outra_leitura=None, codigo=0):
    base = ["--calendario", CAL, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE, "--json"]
    cod, out, err = rodar(args + base)
    if cod != codigo:
        registrar(nome, False, "código %d (esperado %d): %s" % (cod, codigo, (err or out).strip()[:300]))
        return None
    try:
        j = json.loads(out)
    except ValueError:
        registrar(nome, False, "saída não é JSON: %s" % out[:200])
        return None
    erros = []
    for k, v in esperado.items():
        if str(j.get(k)) != str(v):
            erros.append("%s = %s (esperado %s)" % (k, j.get(k), v))
    if not j.get("batem"):
        erros.append("as duas contas não bateram")
    texto_avisos = " ".join(j.get("avisos", []))
    for a in avisos:
        if a not in texto_avisos:
            erros.append("faltou o aviso '%s'" % a)
    datas_puladas = [x["data"] for x in j.get("pulados", [])]
    for d in pulados:
        if d not in datas_puladas:
            erros.append("não pulou %s" % d)
    if outra_leitura:
        venc = [x["vencimento"] for x in j.get("leituras", [])]
        if outra_leitura not in venc:
            erros.append("faltou a outra leitura com vencimento %s" % outra_leitura)
    registrar(nome, not erros, "; ".join(erros))
    if erros and DETALHE:
        print(out)
    return j


def recusa(nome, args, trecho, extra_base=True):
    base = ["--calendario", CAL, "--regras", REGRAS, "--hoje", HOJE] if extra_base else []
    cod, out, err = rodar(args + base)
    ok = cod == 1 and trecho in err
    registrar(nome, ok, "código %d, mensagem: %s" % (cod, (err or out).strip()[:300]))


def texto_contem(nome, args, trechos, codigo=0):
    cod, out, err = rodar(args)
    faltam = [t for t in trechos if t not in out]
    ok = cod == codigo and not faltam
    registrar(nome, ok, "código %d; faltou: %s; %s" % (cod, ", ".join(faltam), err.strip()[:200]))
    if not ok and DETALHE:
        print(out, err)


def calendario_temporario(pasta, linhas_extra, nome="cal.md", cidade=None, tribunal="TRF6, TRT3, TJMG"):
    with open(CAL, encoding="utf-8") as f:
        texto = f.read()
    if cidade:
        texto = texto.replace("cidade: Belo Horizonte", "cidade: %s" % cidade)
    texto = texto.replace("tribunal: TRF6, TRT3, TJMG", "tribunal: %s" % tribunal)
    texto = texto.rstrip("\n") + "\n" + "\n".join(linhas_extra) + "\n"
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)
    return caminho


def main():
    print("Gabarito de docs/casos-ficticios.md (calendário e regras de treino, hoje = %s)" % HOJE)
    print("")
    conta(
        "Lote, linha 1 · Otávio · JEF · recurso inominado (tabela)",
        ["--disponibilizacao", "2026-04-13", "--ato", "recurso inominado", "--rito", "juizado-federal", "--tribunal", "TRF6"],
        {"publicada_em": "2026-04-14", "inicio": "2026-04-15", "vencimento": "2026-04-30", "data_seguranca": "2026-04-28", "dias": 10},
        pulados=("2026-04-16", "2026-04-21"),
    )
    conta(
        "Lote, linha 3 · Camila · TRT3 · recurso ordinário (tabela)",
        ["--disponibilizacao", "2026-04-09", "--ato", "recurso ordinário", "--rito", "trabalhista", "--tribunal", "TRT3"],
        {"publicada_em": "2026-04-10", "inicio": "2026-04-13", "vencimento": "2026-04-24", "data_seguranca": "2026-04-22", "dias": 8},
        pulados=("2026-04-16", "2026-04-21"),
    )
    conta(
        "Lote, linha 4 · Renata · TJMG · custas em 5 dias (o ato)",
        ["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG"],
        {"publicada_em": "2026-04-15", "inicio": "2026-04-17", "vencimento": "2026-04-24", "data_seguranca": "2026-04-22"},
        avisos=("indisponibilidade programada sem certidão",),
        pulados=("2026-04-16",),
    )
    conta(
        "Lote, linha 8 · Marta · JEF · relatório médico em 15 dias (o ato)",
        ["--disponibilizacao", "2026-04-14", "--dias", "15", "--rito", "juizado-federal", "--tribunal", "TRF6"],
        {"publicada_em": "2026-04-15", "inicio": "2026-04-17", "vencimento": "2026-05-11", "data_seguranca": "2026-05-07"},
        pulados=("2026-04-16", "2026-04-21", "2026-05-01"),
    )
    j = conta(
        "Lote, linha 10 · Paulo · TRT3 · portal, ciência tácita em feriado",
        ["--envio-portal", "2026-04-06", "--dias", "5", "--rito", "trabalhista", "--tribunal", "TRT3"],
        {"ciencia": "2026-04-16", "inicio": "2026-04-17", "vencimento": "2026-04-24", "data_seguranca": "2026-04-22"},
        avisos=("DÚVIDA DA CIÊNCIA", "ciência tácita calculada"),
        outra_leitura="2026-04-27",
    )
    if j is not None:
        registrar("Lote, linha 10 · ciência tácita em até 2 dias úteis vai para PESSOA AGORA", "PESSOA AGORA" in (j.get("pessoa_agora") or ""))
    conta(
        "E1 · Renata · TJMG · embargos de declaração com recesso",
        ["--disponibilizacao", "2026-12-17", "--ato", "embargos de declaração", "--rito", "civel", "--tribunal", "TJMG"],
        {"publicada_em": "2026-12-18", "inicio": "2027-01-21", "vencimento": "2027-01-27"},
        pulados=("2026-12-21", "2027-01-20"),
    )
    conta(
        "E1 · Renata · TJMG · apelação com recesso e carnaval",
        ["--disponibilizacao", "2026-12-17", "--ato", "apelação", "--rito", "civel", "--tribunal", "TJMG"],
        {"publicada_em": "2026-12-18", "inicio": "2027-01-21", "vencimento": "2027-02-12"},
        pulados=("2027-02-08", "2027-02-09"),
    )
    conta(
        "E2 · Marta · JEF · prazo do INSS em 5 dias, sem dobro",
        ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "juizado-federal", "--tribunal", "TRF6"],
        {"dias": 5, "em_dobro": "nao"},
    )
    conta(
        "E2 · com --dobro: só dobra, avisa juizado-sem-dobro e deixa a decisão com a pessoa",
        ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "juizado-federal", "--tribunal", "TRF6", "--dobro", "fazenda-dobro"],
        {"dias": 10, "dias_base": 5, "em_dobro": "sim"},
        avisos=("juizado-sem-dobro", "decisão da pessoa", "O script não decide se cabe"),
    )
    recusa("E3 · decadência do Jorge: o script recusa (pelo ato)", ["--disponibilizacao", "2026-04-13", "--ato", "decadência para revisar o benefício", "--rito", "juizado-federal", "--tribunal", "TRF6"], "prazo-material")
    recusa("E3 · decadência do Jorge: o script recusa (--prazo-material)", ["--prazo-material"], "prazo-material")

    print("")
    print("Casos extras (regras de contagem.md e robustez)")
    print("")
    pasta = tempfile.mkdtemp(prefix="teste-calcular-prazo-")
    try:
        args1 = ["--disponibilizacao", "2026-04-13", "--ato", "recurso inominado", "--rito", "juizado-federal", "--tribunal", "TRF6"]
        for nome, args in (
            ("Duas contas batem · linha 1", args1),
            ("Duas contas batem · linha 10", ["--envio-portal", "2026-04-06", "--dias", "5", "--rito", "trabalhista", "--tribunal", "TRT3"]),
            ("Duas contas batem · E1 apelação", ["--disponibilizacao", "2026-12-17", "--ato", "apelação", "--rito", "civel", "--tribunal", "TJMG"]),
        ):
            texto_contem(nome + " (--duplo)", args + ["--calendario", CAL, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE, "--duplo"], ["AS DUAS CONTAS BATEM", "Conta 2 (lista de dias úteis"])
        conta("Data DD/MM/AAAA aceita · linha 1", ["--disponibilizacao", "13/04/2026", "--ato", "recurso inominado", "--rito", "juizado-federal", "--tribunal", "TRF6"], {"vencimento": "2026-04-30"})

        cal_cert = calendario_temporario(pasta, ["| 2026-04-24 | indisponibilidade-certificada | PJe fora do ar, certidão do TJMG | TJMG | certidão de treino | 2026-04-24 |"], "cert.md")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_cert, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        registrar("Indisponibilidade certificada no vencimento empurra para 2026-04-27", j.get("vencimento") == "2026-04-27" and "indisponibilidade" in j.get("regra", "") and j.get("batem"), out[:200] + err[:200])

        cal_meio = calendario_temporario(pasta, ["| 2026-04-22 | indisponibilidade-certificada | PJe fora do ar no meio do prazo | TJMG | certidão de treino | 2026-04-22 |"], "meio.md")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_meio, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        registrar("Indisponibilidade no meio do prazo não muda a conta (2026-04-24)", j.get("vencimento") == "2026-04-24" and j.get("batem"), out[:200] + err[:200])

        cal_red = calendario_temporario(pasta, ["| 2026-04-17 | expediente-reduzido | Expediente até 13h | TJMG | portaria de treino | 2026-04-01 |"], "red.md")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_red, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        registrar("Expediente reduzido no começo: início 2026-04-20, vencimento 2026-04-27", j.get("inicio") == "2026-04-20" and j.get("vencimento") == "2026-04-27" and j.get("batem"), out[:200] + err[:200])

        cal_red2 = calendario_temporario(pasta, ["| 2026-04-24 | expediente-reduzido | Expediente até 13h | TJMG | portaria de treino | 2026-04-01 |"], "red2.md")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_red2, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        registrar("Expediente reduzido no vencimento empurra para 2026-04-27", j.get("inicio") == "2026-04-17" and j.get("vencimento") == "2026-04-27" and j.get("batem"), out[:200] + err[:200])

        conta("Penal · dias corridos, vencimento no domingo vai para 2026-04-20", ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "penal", "--tribunal", "TJMG"], {"contagem": "corridos", "inicio": "2026-04-15", "vencimento": "2026-04-20"})
        conta("Penal · sem --recesso-penal, o recesso não suspende (2026-12-21)", ["--disponibilizacao", "2026-12-14", "--dias", "5", "--rito", "penal", "--tribunal", "TJMG"], {"vencimento": "2026-12-21"}, avisos=("recesso-penal",))
        conta("Penal · com --recesso-penal, suspende (2027-01-21)", ["--disponibilizacao", "2026-12-14", "--dias", "5", "--rito", "penal", "--tribunal", "TJMG", "--recesso-penal"], {"vencimento": "2027-01-21"})
        conta("Ciência informada em dia útil · TRT3 · 5 dias", ["--ciencia", "2026-04-14", "--dias", "5", "--rito", "trabalhista", "--tribunal", "TRT3"], {"inicio": "2026-04-15", "vencimento": "2026-04-23"})

        recusa("Sem calendário para o tribunal: recusa", ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "civel", "--tribunal", "TJSP"], "sem calendário para o tribunal TJSP")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "civel", "--tribunal", "TJSP", "--calendario", CAL, "--sem-calendario", "--hoje", HOJE])
        registrar("--sem-calendario conta só fins de semana e avisa em destaque", cod == 0 and "SEM CALENDÁRIO PARA O TRIBUNAL TJSP" in out, err[:200])
        recusa("Sem número de dias: recusa", ["--disponibilizacao", "2026-04-13", "--rito", "civel", "--tribunal", "TJMG"], "falta o número de dias")
        recusa("Ato fora da tabela: recusa e pede a fonte", ["--disponibilizacao", "2026-04-13", "--ato", "agravo de instrumento", "--rito", "civel", "--tribunal", "TJMG"], "não está na tabela")
        recusa("Calendário que não existe: recusa", ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", os.path.join(pasta, "nao-existe.md")], "calendário não encontrado", extra_base=False)

        pasta_cid = os.path.join(pasta, "cidades")
        os.makedirs(pasta_cid)
        calendario_temporario(pasta_cid, [], "tjmg-bh-2026.md", tribunal="TJMG")
        calendario_temporario(pasta_cid, [], "tjmg-contagem-2026.md", cidade="Contagem", tribunal="TJMG")
        recusa("Dois calendários do TJMG de cidades diferentes sem --cidade: recusa", ["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", pasta_cid], "mais de uma cidade", extra_base=False)
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", pasta_cid, "--cidade", "Belo Horizonte", "--hoje", HOJE, "--json"])
        registrar("Com --cidade, usa só o calendário da cidade", cod == 0 and json.loads(out).get("vencimento") == "2026-04-24", err[:200])

        cal_sem_conf = calendario_temporario(pasta, [], "semconf.md")
        with open(cal_sem_conf, encoding="utf-8") as f:
            t = f.read()
        t = t.replace("treino: sim", "treino: nao").replace("conferido_por: treino (calendário fictício, não vale para prazo real)", "conferido_por: [A PREENCHER]")
        with open(cal_sem_conf, "w", encoding="utf-8") as f:
            f.write(t)
        regras_nv = os.path.join(pasta, "regras-nao-validadas.md")
        with open(REGRAS, encoding="utf-8") as f:
            t = f.read()
        t = t.replace("validada_por: treino (tabela de partida, não vale para prazo real)", "validada_por: [A PREENCHER]").replace("treino: sim", "treino: nao")
        with open(regras_nv, "w", encoding="utf-8") as f:
            f.write(t)
        cod, out, err = rodar(["--disponibilizacao", "2026-04-13", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_sem_conf, "--regras", regras_nv, "--hoje", HOJE])
        registrar("Avisos: calendário não conferido e regra ainda não validada", cod == 0 and "calendário não conferido" in out and "regra ainda não validada pelo escritório" in out, err[:200])

        cod, out, err = rodar(["--disponibilizacao", "2027-03-01", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", CAL, "--regras", REGRAS, "--hoje", HOJE])
        registrar("Conta fora do período do calendário avisa em destaque", cod == 0 and "não cobre" in out, err[:200])

        # G1 · linha do calendário não conferida que muda a conta: as duas leituras, fica a mais cedo
        with open(CAL, encoding="utf-8") as f:
            t = f.read()
        linha_cc = "| 2026-06-04 | feriado | Corpus Christi (sem expediente no treino) | todos | treino: casos-ficticios.md | 2026-04-01 |"
        assert linha_cc in t
        cal_nc = os.path.join(pasta, "nao-conferida.md")
        with open(cal_nc, "w", encoding="utf-8") as f:
            f.write(t.replace(linha_cc, "| 2026-06-04 | feriado | Corpus Christi | todos | ato do tribunal do ano [CONFERIR] |  |"))
        cod, out, err = rodar(["--disponibilizacao", "2026-05-29", "--dias", "8", "--rito", "trabalhista", "--tribunal", "TRT3", "--calendario", cal_nc, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        duv = " ".join(j.get("duvidas", []))
        registrar(
            "G1 · Corpus Christi não conferido: fica 2026-06-11 (segurança 06-09), dúvida com a outra leitura 06-12",
            j.get("vencimento") == "2026-06-11" and j.get("data_seguranca") == "2026-06-09" and "DÚVIDA DO CALENDÁRIO" in duv
            and "2026-06-04" in duv and "2026-06-12" in duv and "conferir no ato do tribunal" in duv.lower() and j.get("batem"),
            (out + err)[:300],
        )
        cod, out, err = rodar(["--disponibilizacao", "2026-05-29", "--dias", "8", "--rito", "trabalhista", "--tribunal", "TRT3", "--calendario", cal_nc, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE])
        registrar("G1 · a dúvida do calendário sai em destaque no texto, antes dos passos", cod == 0 and out.find(">> DÚVIDA DO CALENDÁRIO") != -1 and out.find(">> DÚVIDA DO CALENDÁRIO") < out.find("Passo 1."), err[:200])
        conta("G1 · linha não conferida fora do período não muda a conta nem cria dúvida (linha 1)", args1[:-2] + ["--tribunal", "TRF6", "--calendario", cal_nc], {"vencimento": "2026-04-30", "duvidas": []})
        cal_pend = calendario_temporario(pasta, ["| [A PREENCHER] | feriado | Feriado municipal da cidade do juízo | TJMG | [CONFERIR] |  |"], "pendente.md")
        cod, out, err = rodar(["--disponibilizacao", "2026-04-14", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG", "--calendario", cal_pend, "--seguranca", "2", "--hoje", HOJE, "--json"])
        j = json.loads(out) if cod == 0 else {}
        registrar("G1 · linha com data [A PREENCHER]: conta pela mais cedo (2026-04-24) e dúvida do calendário", j.get("vencimento") == "2026-04-24" and "DÚVIDA DO CALENDÁRIO" in " ".join(j.get("duvidas", [])), (out + err)[:300])

        # G4 · disponibilização ou ciência dentro do recesso: data mais cedo e aviso
        j = conta("G4 · disponibilização em 2026-12-22, dentro do recesso: 2027-01-27 e aviso", ["--disponibilizacao", "2026-12-22", "--dias", "5", "--rito", "civel", "--tribunal", "TJMG"],
                  {"publicada_em": "2026-12-23", "inicio": "2027-01-21", "vencimento": "2027-01-27"},
                  avisos=("disponibilização dentro do recesso: conferir no ato do tribunal como ele trata a publicação no período",))
        j = conta("G4 · ciência informada dentro do recesso: aviso", ["--ciencia", "2027-01-05", "--dias", "5", "--rito", "trabalhista", "--tribunal", "TRT3"],
                  {"inicio": "2027-01-21", "vencimento": "2027-01-27"}, avisos=("ciência dentro do recesso",))
        conta("G4 · E1 (disponibilização antes do recesso) não ganha o aviso do recesso", ["--disponibilizacao", "2026-12-17", "--ato", "embargos de declaração", "--rito", "civel", "--tribunal", "TJMG"], {"vencimento": "2027-01-27", "duvidas": []})
        # M8 · disponibilização em dia sem expediente
        conta("M8 · disponibilização no sábado 2026-04-18: avisa e conta do primeiro dia útil", ["--disponibilizacao", "2026-04-18", "--dias", "5", "--rito", "juizado-federal", "--tribunal", "TRF6"],
              {"publicada_em": "2026-04-20", "inicio": "2026-04-22", "vencimento": "2026-04-28"}, avisos=("disponibilização em dia sem expediente",))

        # o lote por csv, com ponto e vírgula e BOM, e com vírgula em cp1252
        pub_cab = "id,fonte,disponibilizada_em,publicada_em,tribunal,orgao,processo,codigo_caso,cliente_curto,tipo_ato,resumo,teor,triagem,triada_por,prazo_id,atualizado_em".split(",")
        pz_cab = "id,publicacao_id,codigo_caso,cliente_curto,processo,tipo,providencia,rito,dias,contagem,regra,em_dobro,publicada_em,inicio,vencimento,data_seguranca,responsavel,status,calculado_por,conferido_por,conferido_em,cumprido_em,peca_id,observacao,atualizado_em".split(",")
        pubs = [
            ["PUB-2026-00001", "djen", "2026-04-13", "", "TRF6", "3º JEF de Belo Horizonte", "0000101-11.2026.4.06.3800", "C-2026-0012", "Otávio", "sentenca", "Sentença de improcedência", "", "prazo", "ia", "PZ-2026-0001", HOJE],
            ["PUB-2026-00003", "djen", "2026-04-09", "", "TRT3", "8ª Vara do Trabalho de Belo Horizonte", "0000303-33.2025.5.03.0008", "C-2026-0010", "Camila", "sentenca", "Sentença de improcedência", "", "prazo", "ia", "PZ-2026-0002", HOJE],
            ["PUB-2026-00004", "djen", "2026-04-14", "", "TJMG", "2ª Vara de Família de Belo Horizonte", "0000404-44.2026.8.13.0024", "C-2026-0005", "Renata", "despacho", "Custas complementares", "", "prazo", "ia", "PZ-2026-0003", HOJE],
            ["PUB-2026-00008", "djen", "2026-04-14", "", "TRF6", "1º JEF de Belo Horizonte", "0000505-55.2026.4.06.3800", "C-2026-0001", "Marta", "despacho", "Juntar relatório médico", "", "prazo", "ia", "PZ-2026-0004", HOJE],
            ["PUB-2026-00010", "painel", "2026-04-06", "", "TRT3", "12ª Vara do Trabalho de Belo Horizonte", "0000202-22.2025.5.03.0012", "C-2026-0002", "Paulo", "intimacao", "Manifestar sobre documentos", "", "prazo", "ia", "PZ-2026-0005", HOJE],
        ]
        def pz(i, pub, cod_caso, cli, proc, prov, rito, dias, regra, pubd, ini, venc, seg):
            return [i, pub, cod_caso, cli, proc, "prazo", prov, rito, dias, "uteis", regra, "nao", pubd, ini, venc, seg, "advogada", "sugerido", "ia", "", "", "", "", "", HOJE]
        prazos = [
            pz("PZ-2026-0001", "PUB-2026-00001", "C-2026-0012", "Otávio", "0000101-11.2026.4.06.3800", "recurso inominado", "juizado-federal", "10", "publicacao-diario+juizado-federal", "2026-04-14", "2026-04-15", "2026-04-30", "2026-04-28"),
            pz("PZ-2026-0002", "PUB-2026-00003", "C-2026-0010", "Camila", "0000303-33.2025.5.03.0008", "recurso ordinário", "trabalhista", "8", "publicacao-diario+trabalhista-clt", "2026-04-10", "2026-04-13", "2026-04-24", "2026-04-22"),
            pz("PZ-2026-0003", "PUB-2026-00004", "C-2026-0005", "Renata", "0000404-44.2026.8.13.0024", "recolher custas", "civel", "5", "publicacao-diario+civel-cpc", "2026-04-15", "2026-04-17", "2026-04-27", "2026-04-23"),
            pz("PZ-2026-0004", "PUB-2026-00008", "C-2026-0001", "Marta", "0000505-55.2026.4.06.3800", "juntar relatório médico", "juizado-federal", "15", "publicacao-diario+juizado-federal", "", "", "", ""),
            pz("PZ-2026-0005", "PUB-2026-00010", "C-2026-0002", "Paulo", "0000202-22.2025.5.03.0012", "manifestar sobre documentos", "trabalhista", "5", "intimacao-portal+trabalhista-clt", "2026-04-16", "2026-04-17", "2026-04-24", "2026-04-22"),
        ]

        def gravar(caminho, cab, linhas, sep, enc):
            buf = io.StringIO()
            w = csv.writer(buf, delimiter=sep)
            w.writerow([c.upper() if c == "status" else c for c in cab])
            for l in linhas:
                w.writerow(l)
            with open(caminho, "w", encoding=enc, newline="") as f:
                f.write(buf.getvalue())

        for rotulo, sep, enc in (("ponto e vírgula com BOM", ";", "utf-8-sig"), ("vírgula em cp1252", ",", "cp1252")):
            d = os.path.join(pasta, "lote-" + enc)
            os.makedirs(d)
            pc = os.path.join(d, "publicacoes.csv")
            zc = os.path.join(d, "prazos.csv")
            gravar(pc, pub_cab, pubs, sep, enc)
            gravar(zc, pz_cab, prazos, sep, enc)
            cod, out, err = rodar(["--csv", zc, "--publicacoes", pc, "--calendario", CAL, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE])
            ok = (
                cod == 2
                and "PZ-2026-0003" in out.split("SEPARADAS")[-1]
                and "vencimento: registro 2026-04-27, conta 2026-04-24" in out
                and out.count("| ok |") == 3
                and "registro em branco" in out
            )
            registrar("Lote por csv (%s): 3 ok, a linha 4 com 04-27 separada, código 2" % rotulo, ok, (out + err)[:400])
            if not ok and DETALHE:
                print(out, err)
            cod, out, err = rodar(["--csv", zc, "--publicacoes", pc, "--calendario", CAL, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE, "--gravar"])
            with open(zc, encoding=enc) as f:
                novo = f.read()
            linha_marta = [l for l in novo.splitlines() if "PZ-2026-0004" in l][0]
            linha_renata = [l for l in novo.splitlines() if "PZ-2026-0003" in l][0]
            ok = (
                "2026-05-11" in linha_marta
                and "2026-05-07" in linha_marta
                and "2026-04-27" in linha_renata
                and "conta do lote" in linha_renata
                and sep in novo.splitlines()[0]
                and os.path.isdir(os.path.join(d, "lotes"))
                and "conferido" not in linha_marta.lower().split(sep)[17]
            )
            registrar("--gravar (%s): preenche só o branco, anota a divergência, não muda status" % rotulo, ok, (out + err)[:300])

        # M2 · linha sem número de dias entra no lote, vai para PESSOA AGORA se o ato é de hoje ou ontem
        # G1 · no lote, a dúvida do calendário vai para a observacao
        d = os.path.join(pasta, "lote-sem-dias")
        os.makedirs(d)
        pc = os.path.join(d, "publicacoes.csv")
        zc = os.path.join(d, "prazos.csv")
        pubs2 = [
            ["PUB-2026-00011", "djen", "2026-04-13", "", "TJMG", "2ª Vara de Família de Belo Horizonte", "0000404-44.2026.8.13.0024", "C-2026-0005", "Renata", "despacho", "Manifestar no prazo legal", "", "prazo", "ia", "PZ-2026-0011", HOJE],
            ["PUB-2026-00012", "djen", "2026-05-29", "", "TRT3", "12ª Vara do Trabalho de Belo Horizonte", "0000202-22.2025.5.03.0012", "C-2026-0002", "Paulo", "despacho", "Manifestar em 8 dias", "", "prazo", "ia", "PZ-2026-0012", HOJE],
        ]
        sem = pz("PZ-2026-0011", "PUB-2026-00011", "C-2026-0005", "Renata", "0000404-44.2026.8.13.0024", "manifestar no prazo legal", "civel", "", "", "", "", "", "")
        sem[23] = "[A CONFIRMAR: quantos dias]"
        prazos2 = [sem, pz("PZ-2026-0012", "PUB-2026-00012", "C-2026-0002", "Paulo", "0000202-22.2025.5.03.0012", "manifestar", "trabalhista", "8", "publicacao-diario+trabalhista-clt", "", "", "", "")]
        gravar(pc, pub_cab, pubs2, ",", "utf-8")
        gravar(zc, pz_cab, prazos2, ",", "utf-8")
        cod, out, err = rodar(["--csv", zc, "--publicacoes", pc, "--calendario", cal_nc, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE])
        agora = out.split("PESSOA AGORA")[1].split("\n\n")[0] if "PESSOA AGORA" in out else ""
        registrar(
            "M2 · lote com linha sem número de dias: não quebra, aparece e vai para PESSOA AGORA (ato de ontem)",
            cod == 0 and "SEM NÚMERO DE DIAS" in out and "PZ-2026-0011" in agora and "PESSOA AGORA: PESSOA AGORA" not in out
            and "PESSOA AGORA:" not in agora,
            (out + err)[:400],
        )
        registrar("G1 · no lote, a dúvida do calendário aparece em destaque", "DÚVIDAS DA CONTA" in out and "2026-06-12" in out, out[:300])
        cod, out, err = rodar(["--csv", zc, "--publicacoes", pc, "--calendario", cal_nc, "--regras", REGRAS, "--seguranca", "2", "--hoje", HOJE, "--gravar"])
        with open(zc, encoding="utf-8") as f:
            linhas_novas = list(csv.reader(f))
        cab_n = linhas_novas[0]
        reg = {l[0]: dict(zip([c.lower() for c in cab_n], l)) for l in linhas_novas[1:]}
        ok = (
            reg["PZ-2026-0012"]["vencimento"] == "2026-06-11"
            and "dúvida do calendário" in reg["PZ-2026-0012"]["observacao"]
            and "2026-06-12" in reg["PZ-2026-0012"]["observacao"]
            and reg["PZ-2026-0011"]["vencimento"] == ""
            and "A CONFIRMAR: quantos dias" in reg["PZ-2026-0011"]["observacao"]
            and reg["PZ-2026-0011"]["status"] == "sugerido"
        )
        registrar("G1 e M2 · --gravar: dúvida na observacao, linha sem dias fica sugerido e sem vencimento", ok, (out + err)[:300])

        vazio = os.path.join(pasta, "vazio.csv")
        with open(vazio, "w", encoding="utf-8") as f:
            f.write("id;publicacao_id\n")
        recusa("csv sem as colunas obrigatórias: recusa", ["--csv", vazio, "--calendario", CAL], "sem as colunas obrigatórias", extra_base=False)
        recusa("csv que não existe: recusa", ["--csv", os.path.join(pasta, "nao.csv"), "--calendario", CAL], "arquivo não encontrado", extra_base=False)
    finally:
        shutil.rmtree(pasta, ignore_errors=True)

    falhas = [n for n, ok in resultados if not ok]
    print("")
    print("Resultado: %d casos, %d OK, %d FALHOU" % (len(resultados), len(resultados) - len(falhas), len(falhas)))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
