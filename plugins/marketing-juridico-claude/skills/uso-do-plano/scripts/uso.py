#!/usr/bin/env python3
"""Uso do plano: soma o que cada conversa gastou e mostra o peso ao advogado.

Só biblioteca padrão do Python. Lê:
  ~/.marketing-juridico/uso/sessoes.jsonl   (gravado pelo hook hooks/registrar-uso.sh)
  ~/.marketing-juridico/uso/limites.jsonl   (gravado pela linha de status, se o advogado ligou)
  o histórico de cada conversa (arquivo .jsonl do Claude Code), só os números de uso.

Comandos:
  uso.py conversa [--sessao ID]       peso da conversa atual (ou de uma conversa)
  uso.py resumo [--dias N]            hoje e os últimos N dias (padrão 7), por tarefa
  uso.py painel <arquivo uso.js>      dados de uso num arquivo .js (window.MJC_USO)
  uso.py linha-de-status              lê o JSON da linha de status e imprime a linha
  uso.py configurar-linha-de-status [--aplicar]
  Todos aceitam --json (exceto linha-de-status).

O peso é uma estimativa: soma os tokens medidos com a proporção dos preços públicos
(leitura de cache vale menos, texto escrito pelo Claude vale mais). A Anthropic não
publica quantos tokens cabem no limite do plano. Detalhes em references/regua-de-peso.md.
"""
import glob
import json
import os
import shutil
import statistics
import sys
from datetime import datetime, timedelta, timezone

PASTA = os.path.join(os.path.expanduser("~"), ".marketing-juridico", "uso")
SESSOES = os.path.join(PASTA, "sessoes.jsonl")
LIMITES = os.path.join(PASTA, "limites.jsonl")

# Proporções dos preços públicos por token (entrada = 1). Ver references/regua-de-peso.md.
PESO_ENTRADA = 1.0
PESO_CACHE_5M = 1.25
PESO_CACHE_1H = 2.0
PESO_LEITURA_CACHE = 0.1
PESO_SAIDA = 5.0
MODELO = {"opus": 5 / 3, "sonnet": 1.0, "haiku": 1 / 3}

# Faixas provisórias, em mil pontos de peso. Calibrar com o teste da equipe.
FAIXAS = [(500, "leve"), (2500, "médio"), (10000, "pesado")]
ACIMA = "muito pesado"

TAREFAS = {
    "edicao-de-video": "Edição de vídeo",
    "banca-de-conteudo": "Minutas (Banca de Conteúdo)",
    "linha-editorial": "Linha editorial",
    "rito-pico": "Rito PICO",
    "trava-oab": "Trava OAB",
    "arte-no-canva": "Arte no Canva",
    "protocolo": "Protocolo",
    "informativo-diario": "Informativo",
    "rotinas": "Rotinas",
    "uso-do-plano": "Uso do plano",
}
PLUGIN = "marketing-juridico-claude"
OUTRAS = "Outras conversas"


def agora():
    return datetime.now(timezone.utc)


def ler_jsonl(caminho):
    if not os.path.exists(caminho):
        return
    with open(caminho, encoding="utf-8", errors="ignore") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                yield json.loads(linha)
            except ValueError:
                continue


def data_iso(texto):
    if not texto:
        return None
    try:
        return datetime.fromisoformat(texto.replace("Z", "+00:00"))
    except ValueError:
        return None


def fator_modelo(nome):
    nome = (nome or "").lower()
    for chave, fator in MODELO.items():
        if chave in nome:
            return fator
    return 1.0


def tarefa_da_skill(nome):
    nome = (nome or "").strip().lstrip("/")
    if ":" in nome:
        dono, nome = nome.split(":", 1)
        if dono != PLUGIN:
            return None
    return nome if nome in TAREFAS else None


def pedido_do_advogado(conteudo):
    """Mensagem digitada pelo advogado (avisos automáticos do sistema começam com '<')."""
    if isinstance(conteudo, list):
        textos = [b.get("text", "") for b in conteudo if isinstance(b, dict) and b.get("type") == "text"]
        conteudo = textos[0] if textos else None
    if not isinstance(conteudo, str):
        return False
    texto = conteudo.lstrip()
    return bool(texto) and (not texto.startswith("<") or texto.startswith("<command-name>"))


def historicos_da_conversa(caminho):
    base = caminho[:-6] if caminho.endswith(".jsonl") else caminho
    return [caminho] + sorted(glob.glob(os.path.join(base, "subagents", "*.jsonl")))


def somar_conversa(sessao, caminho, ja_contadas=None):
    """Soma os números de uso de uma conversa (e dos subagentes dela). Não lê texto.

    ja_contadas: respostas já somadas em outra conversa (uma conversa retomada repete o
    histórico da anterior); elas não entram de novo.
    """
    por_mensagem = {}
    imagens = 0
    skills = []
    inicio = fim = None
    turnos = 0
    for arquivo in historicos_da_conversa(caminho):
        for d in ler_jsonl(arquivo):
            quando = data_iso(d.get("timestamp"))
            if quando:
                inicio = quando if inicio is None or quando < inicio else inicio
                fim = quando if fim is None or quando > fim else fim
            m = d.get("message") or {}
            conteudo = m.get("content")
            if d.get("type") == "assistant" and isinstance(m.get("usage"), dict):
                chave = m.get("id") or d.get("uuid")
                if ja_contadas is None or chave not in ja_contadas:
                    por_mensagem[chave] = (m.get("model"), m["usage"])
            if isinstance(conteudo, str) and "<command-name>" in conteudo:
                nome = conteudo.split("<command-name>", 1)[1].split("<", 1)[0]
                t = tarefa_da_skill(nome)
                if t and t not in skills:
                    skills.append(t)
            if d.get("type") == "user" and arquivo == caminho and not d.get("isMeta"):
                if pedido_do_advogado(conteudo):
                    turnos += 1
            if not isinstance(conteudo, list):
                continue
            for b in conteudo:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("name") == "Skill":
                    t = tarefa_da_skill((b.get("input") or {}).get("skill"))
                    if t and t not in skills:
                        skills.append(t)
                elif b.get("type") == "tool_result" and isinstance(b.get("content"), list):
                    imagens += sum(
                        1 for x in b["content"] if isinstance(x, dict) and x.get("type") == "image"
                    )
                elif b.get("type") == "image" and d.get("type") == "user":
                    imagens += 1

    tokens = {"entrada": 0, "cache_escrita": 0, "cache_leitura": 0, "saida": 0}
    partes = {"historico": 0.0, "retomadas": 0.0, "entrada": 0.0, "saida": 0.0}
    for modelo, u in por_mensagem.values():
        fator = fator_modelo(modelo)
        entrada = u.get("input_tokens") or 0
        leitura = u.get("cache_read_input_tokens") or 0
        escrita = u.get("cache_creation_input_tokens") or 0
        saida = u.get("output_tokens") or 0
        detalhe = u.get("cache_creation") or {}
        uma_hora = detalhe.get("ephemeral_1h_input_tokens") or 0
        cinco_min = max(escrita - uma_hora, 0)
        tokens["entrada"] += entrada
        tokens["cache_leitura"] += leitura
        tokens["cache_escrita"] += escrita
        tokens["saida"] += saida
        partes["entrada"] += entrada * PESO_ENTRADA * fator
        partes["historico"] += leitura * PESO_LEITURA_CACHE * fator
        partes["retomadas"] += (uma_hora * PESO_CACHE_1H + cinco_min * PESO_CACHE_5M) * fator
        partes["saida"] += saida * PESO_SAIDA * fator
    peso = sum(partes.values()) / 1000
    return {
        "_ids": list(por_mensagem),
        "sessao": sessao,
        "inicio": inicio.isoformat() if inicio else None,
        "fim": fim.isoformat() if fim else None,
        "tarefa": TAREFAS[skills[0]] if skills else OUTRAS,
        "skills": [TAREFAS[s] for s in skills],
        "respostas": len(por_mensagem),
        "pedidos": turnos,
        "imagens": imagens,
        "tokens": tokens,
        "peso": round(peso, 1),
        "nivel": nivel(peso),
        "partes": {k: round(v / 1000, 1) for k, v in partes.items()},
    }


def nivel(peso):
    for limite, nome in FAIXAS:
        if peso < limite:
            return nome
    return ACIMA


def conversas_registradas():
    vistas = {}
    for r in ler_jsonl(SESSOES):
        if r.get("sessao") and r.get("historico"):
            vistas[r["sessao"]] = r["historico"]
    return [(s, h) for s, h in vistas.items() if os.path.exists(h)]


def todas(dias=None):
    corte = agora() - timedelta(days=dias) if dias else None
    saida = []
    ja_contadas = set()
    registradas = sorted(conversas_registradas(), key=lambda r: os.path.getmtime(r[1]))
    for sessao, caminho in registradas:
        if corte and datetime.fromtimestamp(os.path.getmtime(caminho), timezone.utc) < corte:
            continue
        c = somar_conversa(sessao, caminho, ja_contadas)
        ja_contadas.update(c.pop("_ids"))
        if c["respostas"]:
            saida.append(c)
    return saida


def limites_da_conversa(sessao):
    vistos = [r for r in ler_jsonl(LIMITES) if r.get("sessao") == sessao]
    if not vistos:
        return None
    primeiro, ultimo = vistos[0], vistos[-1]
    return {
        "sessao5h": [primeiro.get("cinco_horas"), ultimo.get("cinco_horas")],
        "semana": [primeiro.get("semana"), ultimo.get("semana")],
        "zera5h": ultimo.get("zera_cinco_horas"),
        "zeraSemana": ultimo.get("zera_semana"),
    }


def ultimo_limite():
    ultimo = None
    for r in ler_jsonl(LIMITES):
        ultimo = r
    return ultimo


def comparacao(c, outras):
    """Compara com o histórico do próprio advogado (30 dias). Sem histórico, não compara."""
    minutas = [o["peso"] for o in outras if o["tarefa"] == TAREFAS["banca-de-conteudo"]]
    if len(minutas) >= 3 and c["tarefa"] != TAREFAS["banca-de-conteudo"]:
        ref = statistics.median(minutas)
        if ref > 0:
            return "como %s das suas conversas de minuta" % arredondar_vezes(c["peso"] / ref)
    pesos = [o["peso"] for o in outras]
    if len(pesos) >= 5:
        ref = statistics.median(pesos)
        if ref > 0:
            return "%s uma conversa típica sua" % arredondar_vezes(c["peso"] / ref, vezes=True)
    return None


def arredondar_vezes(x, vezes=False):
    if x < 0.75:
        return "menos que" if vezes else "menos de uma"
    n = max(1, round(x))
    if vezes:
        return "parecido com" if n == 1 else "%d vezes" % n
    return "uma" if n == 1 else str(n)


def o_que_mais_pesou(c):
    p = c["partes"]
    total = sum(p.values()) or 1
    motivos = []
    if c["imagens"] >= 5:
        motivos.append("%d imagens conferidas pelo Claude" % c["imagens"])
    if p["historico"] / total > 0.4 and c["pedidos"] >= 8:
        motivos.append("conversa longa (%d pedidos; cada um reenvia o histórico)" % c["pedidos"])
    if p["retomadas"] / total > 0.4:
        motivos.append("arquivos lidos e retomadas depois de pausa")
    if p["saida"] / total > 0.35:
        motivos.append("textos longos escritos pelo Claude")
    return motivos[:2]


def descrever_conversa(c, outras):
    linhas = ["Peso desta conversa: %s." % c["nivel"]]
    comp = comparacao(c, outras)
    if comp:
        linhas[0] = "Peso desta conversa: %s, %s." % (c["nivel"], comp)
    motivos = o_que_mais_pesou(c)
    if motivos:
        linhas.append("O que mais pesou: %s." % "; ".join(motivos))
    lim = limites_da_conversa(c["sessao"])
    if lim and lim["sessao5h"][0] is not None:
        a, b = lim["sessao5h"]
        linhas.append(
            "Sessão de 5 horas do plano: de %d%% para %d%% durante a conversa (medido; inclui o que você usou em paralelo)."
            % (round(a), round(b))
        )
    return linhas


def cmd_conversa(args, como_json):
    sessao = valor(args, "--sessao")
    registradas = conversas_registradas()
    if not registradas:
        return sem_registro(como_json)
    if sessao:
        escolhida = [r for r in registradas if r[0] == sessao]
    else:
        escolhida = [max(registradas, key=lambda r: os.path.getmtime(r[1]))]
    if not escolhida:
        print("Conversa não encontrada no registro.")
        return 1
    c = somar_conversa(*escolhida[0])
    c.pop("_ids")
    corte = agora() - timedelta(days=30)
    outras = [o for o in todas(30) if o["sessao"] != c["sessao"]]
    outras = [o for o in outras if not o["fim"] or data_iso(o["fim"]) >= corte]
    if como_json:
        c["comparacao"] = comparacao(c, outras)
        c["oQueMaisPesou"] = o_que_mais_pesou(c)
        c["limites"] = limites_da_conversa(c["sessao"])
        print(json.dumps(c, ensure_ascii=False, indent=2))
    else:
        print("\n".join(descrever_conversa(c, outras)))
    return 0


def agrupar(lista):
    grupos = {}
    for c in lista:
        g = grupos.setdefault(c["tarefa"], {"tarefa": c["tarefa"], "conversas": 0, "peso": 0.0, "imagens": 0})
        g["conversas"] += 1
        g["peso"] += c["peso"]
        g["imagens"] += c["imagens"]
    total = sum(g["peso"] for g in grupos.values()) or 1
    for g in grupos.values():
        g["parte"] = round(100 * g["peso"] / total)
        g["peso"] = round(g["peso"], 1)
    return sorted(grupos.values(), key=lambda g: -g["peso"])


def resumo(dias):
    lista = todas(dias)
    hoje = agora().astimezone().date()
    de_hoje = [c for c in lista if c["fim"] and data_iso(c["fim"]).astimezone().date() == hoje]
    pesadas = sorted(lista, key=lambda c: -c["peso"])[:3]
    return {
        "dias": dias,
        "hoje": {"conversas": len(de_hoje), "porTarefa": agrupar(de_hoje)},
        "periodo": {"conversas": len(lista), "porTarefa": agrupar(lista)},
        "maisPesadas": [
            {"tarefa": c["tarefa"], "fim": c["fim"], "nivel": c["nivel"], "oQueMaisPesou": o_que_mais_pesou(c)}
            for c in pesadas
        ],
        "limites": ultimo_limite(),
        "atualizadoEm": agora().astimezone().strftime("%Y-%m-%dT%H:%M"),
    }


def cmd_resumo(args, como_json):
    if not conversas_registradas():
        return sem_registro(como_json)
    dias = int(valor(args, "--dias") or 7)
    r = resumo(dias)
    if como_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print("Hoje: %d conversas." % r["hoje"]["conversas"])
    for g in r["hoje"]["porTarefa"]:
        print("  %s: %d%% do peso de hoje (%d conversas)" % (g["tarefa"], g["parte"], g["conversas"]))
    print("Últimos %d dias: %d conversas." % (dias, r["periodo"]["conversas"]))
    for g in r["periodo"]["porTarefa"]:
        extra = ", %d imagens" % g["imagens"] if g["imagens"] else ""
        print("  %s: %d%% do peso (%d conversas%s)" % (g["tarefa"], g["parte"], g["conversas"], extra))
    for c in r["maisPesadas"]:
        if c["oQueMaisPesou"]:
            print("Mais pesada: %s (%s): %s." % (c["tarefa"], c["nivel"], "; ".join(c["oQueMaisPesou"])))
    lim = r["limites"]
    if lim and lim.get("cinco_horas") is not None:
        print(
            "Último percentual medido do plano: sessão de 5 horas %d%%, semana %s (em %s)."
            % (round(lim["cinco_horas"]), "%d%%" % round(lim["semana"]) if lim.get("semana") is not None else "sem dado", lim.get("quando"))
        )
    else:
        print("Percentual oficial do plano: Configurações > Uso, no aplicativo do Claude.")
    return 0


def cmd_painel(args, como_json):
    if not args:
        print("Uso: uso.py painel <caminho do uso.js>")
        return 1
    r = resumo(7)
    os.makedirs(os.path.dirname(os.path.abspath(args[0])), exist_ok=True)
    with open(args[0], "w", encoding="utf-8") as f:
        f.write("window.MJC_USO = %s;\n" % json.dumps(r, ensure_ascii=False, indent=2))
    print("Painel de uso atualizado: %s" % args[0])
    return 0


def sem_registro(como_json):
    msg = (
        "Ainda não há registro de uso. O registro funciona no Claude Code com o plugin ativo "
        "e começa a contar a partir da primeira conversa depois da instalação. "
        "O percentual oficial do plano fica em Configurações > Uso."
    )
    print(json.dumps({"semRegistro": True, "mensagem": msg}, ensure_ascii=False) if como_json else msg)
    return 0


def hora_local(epoch):
    try:
        quando = datetime.fromtimestamp(float(epoch), timezone.utc).astimezone()
    except (TypeError, ValueError):
        return None
    if quando.date() == datetime.now().date():
        return quando.strftime("%Hh%M")
    dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    return "%s %s" % (dias[quando.weekday()], quando.strftime("%Hh%M"))


def cmd_linha_de_status():
    try:
        d = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        d = {}
    partes = []
    lim = d.get("rate_limits") or {}
    cinco = lim.get("five_hour") or {}
    semana = lim.get("seven_day") or {}
    if cinco.get("used_percentage") is not None:
        z = hora_local(cinco.get("resets_at"))
        partes.append("Sessão %d%%%s" % (round(cinco["used_percentage"]), " (zera %s)" % z if z else ""))
    if semana.get("used_percentage") is not None:
        z = hora_local(semana.get("resets_at"))
        partes.append("Semana %d%%%s" % (round(semana["used_percentage"]), " (zera %s)" % z if z else ""))
    contexto = (d.get("context_window") or {}).get("used_percentage")
    if contexto is not None:
        partes.append("Conversa %d%% cheia" % round(contexto))
    print(" · ".join(partes) if partes else "Uso do plano: aparece depois da primeira resposta")
    if cinco or semana:
        guardar_limite(d.get("session_id"), cinco, semana)
    return 0


def guardar_limite(sessao, cinco, semana):
    novo = {
        "sessao": sessao,
        "cinco_horas": cinco.get("used_percentage"),
        "semana": semana.get("used_percentage"),
        "zera_cinco_horas": cinco.get("resets_at"),
        "zera_semana": semana.get("resets_at"),
    }
    ultimo = ultimo_limite() or {}
    if all(ultimo.get(k) == v for k, v in novo.items()):
        return
    novo["quando"] = agora().astimezone().strftime("%Y-%m-%dT%H:%M")
    try:
        os.makedirs(PASTA, exist_ok=True)
        with open(LIMITES, "a", encoding="utf-8") as f:
            f.write(json.dumps(novo, ensure_ascii=False) + "\n")
    except OSError:
        pass


def cmd_configurar(args, como_json):
    """Mostra (ou aplica, com --aplicar) a linha de status no settings.json do Claude Code."""
    config = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
    destino = os.path.join(PASTA, "uso.py")
    comando = '"%s" "%s" linha-de-status' % (sys.executable, destino)
    atual = {}
    if os.path.exists(config):
        with open(config, encoding="utf-8") as f:
            try:
                atual = json.load(f)
            except ValueError:
                print("O settings.json do Claude Code não está legível; nada foi alterado.")
                return 1
    existente = atual.get("statusLine")
    if "--aplicar" not in args:
        info = {"configAtual": existente, "comandoNovo": comando, "arquivo": config}
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0
    os.makedirs(PASTA, exist_ok=True)
    shutil.copyfile(os.path.abspath(__file__), destino)
    if os.path.exists(config):
        shutil.copyfile(config, config + ".antes-da-linha-de-status")
    else:
        os.makedirs(os.path.dirname(config), exist_ok=True)
    atual["statusLine"] = {"type": "command", "command": comando, "padding": 0}
    with open(config, "w", encoding="utf-8") as f:
        json.dump(atual, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Linha de status ligada. Cópia da configuração anterior: %s.antes-da-linha-de-status" % config)
    return 0


def valor(args, nome):
    if nome in args:
        i = args.index(nome)
        if i + 1 < len(args):
            return args[i + 1]
    return None


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    comando, args = argv[0], argv[1:]
    como_json = "--json" in args
    if comando == "linha-de-status":
        return cmd_linha_de_status()
    if comando == "conversa":
        return cmd_conversa(args, como_json)
    if comando == "resumo":
        return cmd_resumo(args, como_json)
    if comando == "painel":
        return cmd_painel([a for a in args if a != "--json"], como_json)
    if comando == "configurar-linha-de-status":
        return cmd_configurar(args, como_json)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
