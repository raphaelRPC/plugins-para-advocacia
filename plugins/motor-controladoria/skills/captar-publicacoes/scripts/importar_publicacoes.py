#!/usr/bin/env python3
"""Importa publicações para o publicacoes.csv da controladoria.

Entradas aceitas (um ou mais arquivos, ou uma pasta como entrada/):
  - planilha .csv (vírgula ou ponto e vírgula, com ou sem BOM, utf-8 ou cp1252);
  - planilha .xlsx (só com openpyxl instalado; sem ele, salve como .csv);
  - e-mail salvo .eml, e texto colado .txt ou .md;
  - o registro dos painéis (07-operacao/controladoria/paineis/AAAA-MM-DD.md);
  - a saída do captar_djen.py.

Normaliza para as colunas de docs/prazos.md, guarda o teor em
publicacoes/AAAA-MM-DD/<id>.md (a data é a da captação), dá ids sequenciais
(PUB-AAAA-NNNNN), marca duplicadas (mesmo processo, mesma data, mesmo teor)
e não repete o que já está no registro.

Uso:
  python3 importar_publicacoes.py <arquivo ou pasta> [...] --registro <pasta da controladoria>
      [--data AAAA-MM-DD] [--fonte djen|email|sistema|planilha|painel]
      [--ultima-rodada AAAA-MM-DD] [--treino] [--gravar] [--json]

Sem --gravar, só mostra o que faria. Código 1 quando falta arquivo, coluna
obrigatória ou quando nada foi lido.
"""
import argparse
import csv
import datetime as dt
import email
import email.policy
import email.utils
import html
import io
import json
import os
import re
import sys
import unicodedata

COLUNAS = ["id", "fonte", "disponibilizada_em", "publicada_em", "tribunal", "orgao",
           "processo", "codigo_caso", "cliente_curto", "tipo_ato", "resumo", "teor",
           "triagem", "triada_por", "prazo_id", "atualizado_em"]
FONTES = {"djen", "email", "sistema", "planilha", "painel"}
TIPOS = ["despacho", "decisao", "sentenca", "acordao", "intimacao", "pauta", "edital", "certidao", "outro"]

# apelidos de coluna aceitos nas planilhas (sem acento, minúsculas)
APELIDOS = {
    "fonte": ["fonte", "origem", "meio"],
    "disponibilizada_em": ["disponibilizada_em", "data_disponibilizacao", "disponibilizacao",
                           "data_de_disponibilizacao", "disponibilizado_em", "data_da_disponibilizacao",
                           "datadisponibilizacao", "data", "data_publicacao", "data_da_publicacao"],
    "tribunal": ["tribunal", "sigla", "siglatribunal", "sigla_tribunal"],
    "orgao": ["orgao", "nomeorgao", "vara", "juizo", "orgao_julgador", "vara_juizo"],
    "processo": ["processo", "numero_processo", "numero_do_processo", "n_processo", "numeroprocesso",
                 "numeroprocessocommascara", "autos", "num_processo", "nprocesso"],
    "partes": ["partes", "parte", "destinatarios", "polos"],
    "tipo_ato": ["tipo_ato", "tipo", "tipo_de_ato", "tipodocumento", "tipo_documento", "tipocomunicacao",
                 "tipo_comunicacao", "ato"],
    "teor": ["teor", "texto", "conteudo", "publicacao", "inteiro_teor", "descricao", "intimacao"],
    "link": ["link", "url"],
}
OBRIGATORIAS = ["processo", "disponibilizada_em", "teor"]
RAIZES = {"processo": ["processo", "autos"], "disponibilizada_em": ["disponibiliza", "data"],
          "teor": ["teor", "texto", "conteudo"], "orgao": ["orgao", "vara", "juizo"], "tribunal": ["tribunal"],
          "tipo_ato": ["tipo"], "partes": ["partes"]}

CNJ = re.compile(r"\b(\d{7})-?(\d{2})\.?(\d{4})\.?(\d)\.?(\d{2})\.?(\d{4})\b")
UFS_TJ = {"01": "AC", "02": "AL", "03": "AP", "04": "AM", "05": "BA", "06": "CE", "07": "DFT",
          "08": "ES", "09": "GO", "10": "MA", "11": "MT", "12": "MS", "13": "MG", "14": "PA",
          "15": "PB", "16": "PR", "17": "PE", "18": "PI", "19": "RJ", "20": "RN", "21": "RS",
          "22": "RO", "23": "RR", "24": "SC", "25": "SE", "26": "SP", "27": "TO"}


def erro(msg):
    print("ERRO: " + msg, file=sys.stderr)
    sys.exit(1)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def chave_coluna(nome):
    s = sem_acento((nome or "").strip().lower())
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def ler_texto(caminho):
    with open(caminho, "rb") as f:
        bruto = f.read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return bruto.decode(enc), bruto.startswith(b"\xef\xbb\xbf")
        except UnicodeDecodeError:
            continue
    return bruto.decode("utf-8", errors="replace"), False


def detectar_delimitador(texto):
    primeira = texto.splitlines()[0] if texto.strip() else ""
    return ";" if primeira.count(";") > primeira.count(",") else ","


def data_iso(valor):
    """Aceita AAAA-MM-DD, DD/MM/AAAA, DD-MM-AAAA, DD/MM/AA e AAAA-MM-DDTHH:MM."""
    v = (valor or "").strip()
    if not v:
        return ""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", v)
    if m:
        a, mes, d = m.groups()
    else:
        m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})", v)
        if not m:
            return ""
        d, mes, a = m.groups()
        if len(a) == 2:
            a = "20" + a
    try:
        return dt.date(int(a), int(mes), int(d)).isoformat()
    except ValueError:
        return ""


def mascara_processo(valor):
    """Devolve (número com máscara CNJ, aviso). Não confere dígito verificador."""
    v = (valor or "").strip()
    digitos = re.sub(r"\D", "", v)
    if len(digitos) == 20:
        d = digitos
        return f"{d[0:7]}-{d[7:9]}.{d[9:13]}.{d[13]}.{d[14:16]}.{d[16:20]}", ""
    if not v:
        return "", "sem número de processo"
    return v, f"número fora do padrão CNJ ({v}): conferir"


def tribunal_pelo_numero(processo):
    d = re.sub(r"\D", "", processo or "")
    if len(d) != 20:
        return ""
    j, tr = d[13], d[14:16]
    if j == "4":
        return f"TRF{int(tr)}"
    if j == "5":
        return f"TRT{int(tr)}"
    if j == "8":
        uf = UFS_TJ.get(tr)
        return ("TJ" + uf) if uf else ""
    if j == "3":
        return "STJ"
    if j == "1":
        return "STF"
    return ""


def tipo_normalizado(valor):
    s = sem_acento((valor or "").lower())
    for chave, tipo in (("acordao", "acordao"), ("sentenc", "sentenca"), ("decis", "decisao"),
                        ("despacho", "despacho"), ("pauta", "pauta"), ("edital", "edital"),
                        ("certid", "certidao"), ("intima", "intimacao"), ("citac", "intimacao"),
                        ("notifica", "intimacao")):
        if chave in s:
            return tipo
    return "outro" if s.strip() else ""


TIPO_LEGIVEL = {"despacho": "Despacho", "decisao": "Decisão", "sentenca": "Sentença", "acordao": "Acórdão",
                "intimacao": "Intimação", "pauta": "Pauta", "edital": "Edital", "certidao": "Certidão",
                "outro": "Ato", "": "Ato"}


def teor_normalizado(teor):
    s = sem_acento((teor or "").lower())
    return re.sub(r"[^a-z0-9]+", "", s)


def limpar_html(texto):
    if "<" not in (texto or ""):
        return texto or ""
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", texto)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n\n", t).strip()


def fonte_pelo_nome(caminho, padrao):
    nome = os.path.basename(caminho).lower()
    for f in ("djen", "email", "e-mail", "sistema", "planilha", "painel"):
        if f in nome:
            return "email" if f == "e-mail" else f
    return padrao


# ---------------------------------------------------------------- leitores

def ler_planilha_linhas(linhas, origem, fonte_padrao):
    """linhas: lista de dicts com nomes de coluna crus."""
    if not linhas:
        return [], [f"{origem}: planilha sem linhas"]
    cabecalho = list(linhas[0].keys())
    mapa = {}
    chaves = {chave_coluna(c): c for c in cabecalho if c is not None}
    for campo, apelidos in APELIDOS.items():
        for a in apelidos:
            if a in chaves:
                mapa[campo] = chaves[a]
                break
    # sem nome exato, a primeira coluna que contém a raiz (ex.: "Nº do Processo", "Data da disponibilização")
    for campo, raizes in RAIZES.items():
        if campo in mapa:
            continue
        for k, original in chaves.items():
            if any(r in k for r in raizes) and original not in mapa.values():
                mapa[campo] = original
                break
    faltam = [c for c in OBRIGATORIAS if c not in mapa]
    if faltam:
        erro(f"{origem}: faltam as colunas obrigatórias {', '.join(faltam)}. "
             f"Colunas encontradas: {', '.join(c for c in cabecalho if c)}. "
             "Nomes aceitos para cada uma: " +
             "; ".join(f"{c}: {', '.join(APELIDOS[c][:5])}" for c in faltam))
    registros = []
    for n, linha in enumerate(linhas, start=2):
        valores = {campo: (linha.get(col) or "").strip() for campo, col in mapa.items()}
        if not any(valores.values()):
            continue
        fonte = chave_coluna(valores.get("fonte", "")).replace("_", "-")
        fonte = "email" if fonte in ("e-mail", "e_mail") else fonte
        if fonte not in FONTES:
            fonte = fonte_padrao
        registros.append({
            "fonte": fonte,
            "disponibilizada_em_bruta": valores.get("disponibilizada_em", ""),
            "tribunal": valores.get("tribunal", "").upper().replace(" ", ""),
            "orgao": valores.get("orgao", ""),
            "processo_bruto": valores.get("processo", ""),
            "partes": valores.get("partes", ""),
            "tipo_na_fonte": valores.get("tipo_ato", ""),
            "teor": limpar_html(valores.get("teor", "")),
            "link": valores.get("link", ""),
            "origem": f"{os.path.basename(origem)} (linha {n})",
            "treino": "de-treino" in os.path.basename(origem),
        })
    return registros, []


def ler_csv(caminho, fonte_padrao):
    texto, _ = ler_texto(caminho)
    if not texto.strip():
        erro(f"{caminho}: arquivo vazio")
    leitor = csv.DictReader(io.StringIO(texto), delimiter=detectar_delimitador(texto))
    return ler_planilha_linhas(list(leitor), caminho, fonte_padrao)


def ler_xlsx(caminho, fonte_padrao):
    try:
        import openpyxl  # opcional
    except ImportError:
        erro(f"{caminho}: para ler .xlsx é preciso o openpyxl. Sem ele, abra a planilha e salve como .csv "
             "(Arquivo > Salvar como > CSV) e rode de novo com o .csv.")
    livro = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    folha = livro.worksheets[0]
    linhas = list(folha.iter_rows(values_only=True))
    if not linhas:
        return [], [f"{caminho}: planilha vazia"]
    cab = [str(c) if c is not None else "" for c in linhas[0]]
    dicts = []
    for lin in linhas[1:]:
        d = {}
        for c, v in zip(cab, lin):
            if isinstance(v, (dt.date, dt.datetime)):
                v = v.strftime("%Y-%m-%d")
            d[c] = "" if v is None else str(v)
        dicts.append(d)
    return ler_planilha_linhas(dicts, caminho, fonte_padrao)


def campo_no_texto(texto, rotulos):
    for r in rotulos:
        m = re.search(r"(?im)^\s*" + r + r"\s*:\s*(.+)$", texto)
        if m:
            return m.group(1).strip()
    return ""


def ler_texto_livre(texto, origem, fonte, data_reserva=""):
    """E-mail do tribunal ou texto colado: uma publicação por número de processo."""
    avisos = []
    achados = list(CNJ.finditer(texto))
    numeros = []
    for m in achados:
        n = "".join(m.groups())
        if n not in numeros:
            numeros.append(n)
    if not numeros:
        return [], [f"{origem}: nenhum número de processo no padrão CNJ; nada importado deste arquivo"]
    pedacos = []
    if len(numeros) == 1:
        pedacos = [(numeros[0], texto)]
    else:
        # divide o texto no começo da linha de cada número novo
        inicios = []
        vistos = set()
        for m in achados:
            n = "".join(m.groups())
            if n in vistos:
                continue
            vistos.add(n)
            ini = texto.rfind("\n", 0, m.start()) + 1
            inicios.append((ini, n))
        inicios.sort()
        for i, (ini, n) in enumerate(inicios):
            fim = inicios[i + 1][0] if i + 1 < len(inicios) else len(texto)
            pedacos.append((n, texto[ini:fim].strip()))
        avisos.append(f"{origem}: {len(numeros)} processos no mesmo texto; separei um por processo, confira os cortes")
    registros = []
    for n, pedaco in pedacos:
        data = ""
        aviso_data = ""
        # a data vem só do bloco deste processo: nunca de outro bloco nem do texto geral do e-mail
        m = re.search(r"(?i)disponibiliza\w*[^0-9\n]{0,30}(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", pedaco)
        if m:
            data = m.group(1)
        elif data_reserva:
            data = data_reserva
            aviso_data = (f"data de disponibilização não encontrada no bloco: usei a data do e-mail ({data_iso(data)}); "
                          "conferir no diário (a real pode ser mais cedo)")
            avisos.append(f"ATENÇÃO {os.path.basename(origem)}, processo {mascara_processo(n)[0] or n}: {aviso_data}")
        registros.append({
            "aviso_data": aviso_data,
            "fonte": fonte,
            "disponibilizada_em_bruta": data,
            "tribunal": campo_no_texto(pedaco, ["tribunal", "sigla do tribunal"]).upper().replace(" ", ""),
            "orgao": campo_no_texto(pedaco, ["órgão", "orgao", "órgão julgador", "vara", "juízo", "juizo"]),
            "processo_bruto": n,
            "partes": campo_no_texto(pedaco, ["partes", "parte"]),
            "tipo_na_fonte": campo_no_texto(pedaco, ["tipo de documento", "tipo de comunicação", "tipo de comunicacao", "tipo"]),
            "teor": pedaco.strip(),
            "link": "",
            "origem": os.path.basename(origem),
            "treino": False,
        })
    return registros, avisos


def ler_eml(caminho, fonte_padrao):
    with open(caminho, "rb") as f:
        msg = email.message_from_bytes(f.read(), policy=email.policy.default)
    corpo = msg.get_body(preferencelist=("plain", "html"))
    texto = corpo.get_content() if corpo is not None else ""
    if corpo is not None and corpo.get_content_type() == "text/html":
        texto = limpar_html(texto)
    data_reserva = ""
    if msg.get("Date"):
        try:
            data_reserva = email.utils.parsedate_to_datetime(msg["Date"]).strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            data_reserva = ""
    return ler_texto_livre(texto, caminho, fonte_pelo_nome(caminho, fonte_padrao), data_reserva)


def tabela_markdown(texto, titulo):
    """Lê a primeira tabela depois do título '## <titulo>'."""
    m = re.search(r"(?im)^##\s+" + re.escape(titulo) + r"\s*$", texto)
    if not m:
        return None
    resto = texto[m.end():]
    prox = re.search(r"(?m)^##\s", resto)
    if prox:
        resto = resto[:prox.start()]
    linhas = [l.strip() for l in resto.splitlines() if l.strip().startswith("|")]
    if len(linhas) < 2:
        return []
    cab = [chave_coluna(c) for c in linhas[0].strip("|").split("|")]
    saida = []
    for l in linhas[2:]:
        cel = [c.strip() for c in l.strip("|").split("|")]
        if len(cel) < len(cab):
            cel += [""] * (len(cab) - len(cel))
        saida.append(dict(zip(cab, cel)))
    return saida


def eh_registro_de_painel(texto):
    return bool(re.search(r"(?im)^documento:\s*registro dos pain", texto)) or \
        "## Intimações e comunicações vistas" in texto


def ler_painel(caminho):
    texto, _ = ler_texto(caminho)
    avisos = []
    treino = bool(re.search(r"(?im)^treino:\s*sim", texto))
    m_data = re.search(r"(?im)^data:\s*(\S+)", texto)
    data_reg = data_iso(m_data.group(1)) if m_data else ""
    sistemas = tabela_markdown(texto, "Sistemas olhados") or []
    for s in sistemas:
        if chave_coluna(s.get("situacao", "")) not in ("olhado",):
            avisos.append(f"painel {s.get('sistema', '')} {s.get('tribunal', '')}: {s.get('situacao', 'sem situação')} "
                          f"({s.get('observacao', '')}). Vai para a pessoa como aviso")
    vistas = tabela_markdown(texto, "Intimações e comunicações vistas")
    if vistas is None:
        erro(f"{caminho}: registro de painel sem a seção '## Intimações e comunicações vistas'")
    registros = []
    for n, v in enumerate(vistas, start=1):
        if not any(v.values()):
            continue
        ciencia = chave_coluna(v.get("ciencia", "")).replace("_", "-")
        enviada = v.get("enviada_em", "")
        aberta = v.get("aberta_em", "")
        teor = v.get("trecho", "").strip()
        if not v.get("trecho", "").strip():
            avisos.append(f"{os.path.basename(caminho)}: intimação do processo {v.get('processo', '')} sem trecho do ato. "
                          "Sem o trecho não há o que conferir: peça a quem olhou o painel")
        if ciencia not in ("sem-ciencia", "aberta", "tacita", "lida"):
            avisos.append(f"{os.path.basename(caminho)}: intimação do processo {v.get('processo', '')} sem a situação da ciência")
        registros.append({
            "fonte": "painel",
            "disponibilizada_em_bruta": enviada,
            "tribunal": v.get("tribunal", "").upper().replace(" ", ""),
            "orgao": v.get("orgao", ""),
            "processo_bruto": v.get("processo", ""),
            "partes": "",
            "tipo_na_fonte": v.get("tipo_ato", "") or "intimacao",
            "teor": teor,
            "link": "",
            "origem": f"{os.path.basename(caminho)} (intimação {n})",
            "treino": treino,
            "painel": {"sistema": v.get("sistema", ""), "enviada_em": data_iso(enviada),
                       "ciencia": ciencia or "[A CONFIRMAR]", "aberta_em": data_iso(aberta),
                       "prazo_no_painel": v.get("prazo_no_painel", ""), "registrado_em": data_reg},
        })
    return registros, avisos


def ler_entrada(caminho, fonte_cli):
    ext = os.path.splitext(caminho)[1].lower()
    padrao = fonte_cli or fonte_pelo_nome(caminho, "planilha" if ext in (".csv", ".xlsx") else "email")
    if ext == ".csv":
        regs, av = ler_csv(caminho, padrao)
        if fonte_cli:
            for r in regs:
                r["fonte"] = fonte_cli
        return regs, av
    if ext == ".xlsx":
        return ler_xlsx(caminho, padrao)
    if ext == ".eml":
        return ler_eml(caminho, padrao)
    if ext in (".txt", ".md"):
        texto, _ = ler_texto(caminho)
        if eh_registro_de_painel(texto):
            return ler_painel(caminho)
        return ler_texto_livre(texto, caminho, padrao)
    return [], [f"{caminho}: tipo de arquivo não lido ({ext or 'sem extensão'})"]


# ---------------------------------------------------------------- registro

def ler_registro(caminho_csv):
    if not os.path.exists(caminho_csv):
        return [], ",", False
    texto, bom = ler_texto(caminho_csv)
    if not texto.strip():
        return [], ",", bom
    delim = detectar_delimitador(texto)
    leitor = csv.DictReader(io.StringIO(texto), delimiter=delim)
    cab = [chave_coluna(c) for c in (leitor.fieldnames or [])]
    faltam = [c for c in ("id", "fonte", "disponibilizada_em", "processo", "teor", "triagem") if c not in cab]
    if faltam:
        erro(f"{caminho_csv}: o registro existe mas faltam as colunas {', '.join(faltam)} (veja docs/prazos.md)")
    linhas = []
    for l in leitor:
        linhas.append({chave_coluna(k): (v or "") for k, v in l.items() if k is not None})
    return linhas, delim, bom


def teor_do_registro(pasta, linha):
    rel = linha.get("teor", "")
    if not rel:
        return ""
    caminho = os.path.join(pasta, rel)
    if not os.path.exists(caminho):
        return ""
    texto, _ = ler_texto(caminho)
    m = re.match(r"(?s)^---\n.*?\n---\n", texto)
    return texto[m.end():] if m else texto


def dia_util_anterior(d):
    d = d - dt.timedelta(days=1)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    return d


def main():
    ap = argparse.ArgumentParser(description="Importa publicações para publicacoes.csv")
    ap.add_argument("entradas", nargs="+", help="arquivos ou pastas (csv, xlsx, eml, txt, md, registro de painel)")
    ap.add_argument("--registro", required=True, help="pasta da controladoria (onde fica publicacoes.csv)")
    ap.add_argument("--data", help="data da captação, AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--fonte", choices=sorted(FONTES), help="força a fonte de todas as linhas")
    ap.add_argument("--ultima-rodada", help="data da última rodada, para apontar o que chegou atrasado")
    ap.add_argument("--treino", action="store_true", help="material de treino: só grava em _treino/")
    ap.add_argument("--gravar", action="store_true", help="grava; sem isto só mostra")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--mover-lidos", action="store_true",
                    help="com --gravar, move os arquivos lidos de entrada/ para entrada/lidos/AAAA-MM-DD/ (mover não é apagar)")
    a = ap.parse_args()

    hoje = data_iso(a.data) if a.data else dt.date.today().isoformat()
    if not hoje:
        erro(f"--data inválida: {a.data}. Use AAAA-MM-DD ou DD/MM/AAAA")
    ultima = data_iso(a.ultima_rodada) if a.ultima_rodada else ""
    pasta = os.path.abspath(a.registro)
    eh_pasta_de_treino = "_treino" in pasta.replace("\\", "/").split("/")
    if a.treino and not eh_pasta_de_treino:
        erro("--treino grava só em escritorio/07-operacao/_treino/controladoria/. Ajuste --registro")

    arquivos = []
    for e in a.entradas:
        if os.path.isdir(e):
            for nome in sorted(os.listdir(e)):
                c = os.path.join(e, nome)
                if os.path.isfile(c) and not nome.startswith((".", "~$")) and \
                        os.path.splitext(nome)[1].lower() in (".csv", ".xlsx", ".eml", ".txt", ".md"):
                    arquivos.append(c)
        elif os.path.isfile(e):
            arquivos.append(e)
        else:
            erro(f"não encontrei {e}")
    if not arquivos:
        erro("nenhum arquivo para ler (csv, xlsx, eml, txt ou md) nas entradas indicadas")

    candidatos, avisos = [], []
    for c in arquivos:
        regs, av = ler_entrada(c, a.fonte)
        candidatos.extend(regs)
        avisos.extend(av)
    if any(r.get("treino") for r in candidatos) and not eh_pasta_de_treino:
        erro("o material é de treino e o registro é o real. Treino grava em escritorio/07-operacao/_treino/controladoria/")
    if not candidatos:
        print("\n".join(avisos), file=sys.stderr)
        erro("nada foi lido das entradas. Confira o formato (veja a captar-publicacoes) e rode de novo")

    caminho_csv = os.path.join(pasta, "publicacoes.csv")
    existentes, delim, bom = ler_registro(caminho_csv)
    ano = hoje[:4]
    maior = 0
    for l in existentes:
        m = re.match(r"PUB-(\d{4})-(\d+)$", l.get("id", ""))
        if m and m.group(1) == ano:
            maior = max(maior, int(m.group(2)))

    # chaves do que já está no registro: (processo, data, teor) -> (id, fonte)
    chaves = {}      # chave -> (id da original, fonte da original)
    presentes = {}   # (chave, fonte) -> id: o que já entrou por aquela fonte
    for l in existentes:
        k = (re.sub(r"\D", "", l.get("processo", "")), l.get("disponibilizada_em", ""),
             teor_normalizado(teor_do_registro(pasta, l)))
        presentes.setdefault((k, l.get("fonte", "")), l.get("id", ""))
        if l.get("triagem", "") != "duplicada":
            chaves.setdefault(k, (l.get("id", ""), l.get("fonte", "")))

    novas, duplicadas, ja_estavam, atrasadas = [], [], [], []
    sem_data, data_do_email = [], []
    hoje_d = dt.date.fromisoformat(hoje)
    limite_atraso = dia_util_anterior(hoje_d).isoformat()
    for r in candidatos:
        proc, aviso_proc = mascara_processo(r["processo_bruto"])
        if aviso_proc:
            avisos.append(f"{r['origem']}: {aviso_proc}")
        data = data_iso(r["disponibilizada_em_bruta"])
        aviso_data = r.get("aviso_data", "")
        if not data:
            aviso_data = (f"sem data de disponibilização ({r['disponibilizada_em_bruta'] or 'vazia'}): "
                          "a pessoa confere no diário; sem data não há conta")
            avisos.append(f"ATENÇÃO {r['origem']}: {aviso_data}. Entra com triagem urgente, para a pessoa")
        tribunal = r["tribunal"]
        if not tribunal:
            tribunal = tribunal_pelo_numero(proc)
            if tribunal:
                avisos.append(f"{r['origem']}: tribunal {tribunal} tirado do número do processo. Conferir")
        teor = r["teor"].strip() or "(a fonte não trouxe o teor)"
        if teor.startswith("(a fonte"):
            avisos.append(f"{r['origem']}: sem teor. Entra para a pessoa buscar o ato na fonte")
        k = (re.sub(r"\D", "", proc), data, teor_normalizado(teor))
        if (k, r["fonte"]) in presentes:
            ja_estavam.append((r, presentes[(k, r["fonte"])]))
            continue
        dup = k in chaves
        maior += 1
        novo_id = f"PUB-{ano}-{maior:05d}"
        presentes[(k, r["fonte"])] = novo_id
        tipo = tipo_normalizado(r["tipo_na_fonte"])
        linha = {c: "" for c in COLUNAS}
        linha.update({
            "id": novo_id, "fonte": r["fonte"], "disponibilizada_em": data, "tribunal": tribunal,
            "orgao": r["orgao"], "processo": proc, "tipo_ato": tipo,
            "teor": f"publicacoes/{hoje}/{novo_id}.md", "atualizado_em": hoje,
        })
        if dup:
            linha["triagem"] = "duplicada"
            linha["resumo"] = f"duplicada de {chaves[k][0]} (mesmo processo, data e teor; fonte {chaves[k][1]})"
            linha["triada_por"] = "ia"
            duplicadas.append((linha, chaves[k][0]))
        elif not data:
            linha["triagem"] = "urgente"
            linha["triada_por"] = "ia"
            linha["resumo"] = f"{TIPO_LEGIVEL.get(tipo, 'Ato')} sem data de disponibilização: para a pessoa"
            chaves[k] = (novo_id, r["fonte"])
            sem_data.append(linha)
        else:
            linha["triagem"] = "nao-triada"
            linha["resumo"] = f"{TIPO_LEGIVEL.get(tipo, 'Ato')}, a triar"
            if aviso_data:
                linha["resumo"] = f"{TIPO_LEGIVEL.get(tipo, 'Ato')}, a triar · data do e-mail, não do bloco: conferir"[:120]
                data_do_email.append(linha)
            chaves[k] = (novo_id, r["fonte"])
            if r["fonte"] != "painel" and data and (data < limite_atraso or (ultima and data < ultima)):
                atrasadas.append(linha)
        cab = ["---", f"id: {novo_id}", f"fonte: {r['fonte']}", f"disponibilizada_em: {data}",
               f"tribunal: {tribunal}", f"orgao: {r['orgao']}", f"processo: {proc}",
               f"partes: {r['partes']}", f"tipo_na_fonte: {r['tipo_na_fonte']}",
               f"captada_em: {hoje}", f"origem: {r['origem']}"]
        if aviso_data:
            cab.append(f"aviso_captacao: {aviso_data}")
        if r.get("link"):
            cab.append(f"link: {r['link']}")
        if r.get("painel"):
            for kk, vv in r["painel"].items():
                cab.append(f"painel_{kk}: {vv}")
        cab.append("---")
        novas.append((linha, "\n".join(cab) + "\n\n" + teor + "\n"))

    movidos = []
    if a.gravar and a.mover_lidos:
        for c in arquivos:
            pasta_arq = os.path.dirname(os.path.abspath(c))
            if os.path.basename(pasta_arq) != "entrada":
                continue
            destino = os.path.join(pasta_arq, "lidos", hoje)
            os.makedirs(destino, exist_ok=True)
            alvo = os.path.join(destino, os.path.basename(c))
            if not os.path.exists(alvo):
                os.replace(c, alvo)
                movidos.append(os.path.basename(c))

    por_fonte = {}
    for linha, _ in novas:
        por_fonte[linha["fonte"]] = por_fonte.get(linha["fonte"], 0) + 1

    if a.gravar and novas:
        os.makedirs(os.path.join(pasta, "publicacoes", hoje), exist_ok=True)
        for linha, conteudo in novas:
            with open(os.path.join(pasta, linha["teor"]), "w", encoding="utf-8") as f:
                f.write(conteudo)
        cab_exist = COLUNAS
        if existentes:
            cab_exist = list(existentes[0].keys())
            for c in COLUNAS:
                if c not in cab_exist:
                    cab_exist.append(c)
        with open(caminho_csv, "w", encoding="utf-8-sig" if bom else "utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cab_exist, delimiter=delim, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            for l in existentes:
                w.writerow(l)
            for linha, _ in novas:
                w.writerow(linha)

    if a.json:
        print(json.dumps({
            "data": hoje, "gravado": bool(a.gravar), "registro": caminho_csv,
            "novas": [l for l, _ in novas], "duplicadas": [{"id": l["id"], "original": o} for l, o in duplicadas],
            "ja_estavam": [{"origem": r["origem"], "id": o} for r, o in ja_estavam],
            "captadas_com_atraso": [l["id"] for l in atrasadas],
            "sem_data": [l["id"] for l in sem_data],
            "data_do_email_conferir": [l["id"] for l in data_do_email], "avisos": avisos,
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"CAPTAÇÃO · {hoje} · {'gravado' if a.gravar else 'SIMULAÇÃO (nada gravado; use --gravar)'}")
    print(f"Registro: {caminho_csv}{'' if existentes else ' (novo)'}")
    print(f"Lidas: {len(candidatos)} · entram: {len(novas)} "
          f"({', '.join(f'{k} {v}' for k, v in sorted(por_fonte.items())) or 'nenhuma'}) · "
          f"duplicadas: {len(duplicadas)} · já estavam no registro: {len(ja_estavam)}")
    if atrasadas:
        print("\nCAPTADAS COM ATRASO (vão para o topo, PESSOA AGORA):")
        for l in atrasadas:
            print(f"  {l['id']} · disponibilizada {l['disponibilizada_em']} · {l['tribunal']} · {l['processo']}")
    if sem_data or data_do_email:
        print("\nDATA A CONFERIR (PESSOA AGORA):")
        for l in sem_data:
            print(f"  {l['id']} · {l['tribunal']} · {l['processo']} · sem data de disponibilização: entra como urgente, "
                  "a pessoa confere no diário")
        for l in data_do_email:
            print(f"  {l['id']} · {l['tribunal']} · {l['processo']} · data de disponibilização não encontrada no bloco: "
                  f"usei a data do e-mail ({l['disponibilizada_em']}); conferir")
    print("\nENTRAM:")
    for linha, _ in novas:
        print(f"  {linha['id']} · {linha['fonte']} · {linha['disponibilizada_em'] or 'SEM DATA'} · "
              f"{linha['tribunal']} · {linha['processo'] or 'SEM PROCESSO'} · {linha['triagem']}"
              + (f" · {linha['resumo']}" if linha['triagem'] == 'duplicada' else ""))
    if ja_estavam:
        print("\nJÁ ESTAVAM (mesma fonte, mesmo processo, data e teor; não entram de novo):")
        for r, o in ja_estavam:
            print(f"  {r['origem']} = {o}")
    if avisos:
        print("\nAVISOS:")
        for av in avisos:
            print(f"  - {av}")
    if movidos:
        print(f"\nMovidos para entrada/lidos/{hoje}/: {', '.join(movidos)}")
    print("\nPróximo passo: triar-publicacoes nas linhas nao-triada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
