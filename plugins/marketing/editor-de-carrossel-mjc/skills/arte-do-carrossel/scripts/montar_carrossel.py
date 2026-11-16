#!/usr/bin/env python3
"""Motor da arte do carrossel (Plugin Editor de Carrossel - MJC, RPC Educação).

Lê o roteiro de lâminas (carrossel.json), aplica um estilo do catálogo e as cores e fontes do
advogado, e entrega:
    laminas/lamina-NN.html   cada lâmina em HTML (1080 x 1350)
    png/carrossel-NN.png     a lâmina pronta para postar (1080 x 1350)
    alta/carrossel-NN.png    original em 2160 x 2700 (com --alta)
    prancha.html             todas as lâminas numa página, com campo de ajuste e "Copiar para o Claude"
    prancha.png              todas as lâminas numa imagem só, para a conferência do Claude
    relatorio.json           verificador de texto, lâminas que estouraram, contraste das cores

Antes de desenhar, roda o verificador de vícios (verificar_texto.py). Achado para CORRIGIR para
tudo, a não ser com --forcar. O título se ajusta sozinho ao espaço; se nem no tamanho mínimo couber,
a lâmina sai marcada como "estourou" no relatório e deve ser encurtada.

Uso:
    python3 montar_carrossel.py <carrossel.json> [--base PASTA] [--saida PASTA] [--estilo C02]
                                [--alta] [--so 1,3] [--forcar] [--sem-png]

--base é a pasta meu-marketing-juridico (para achar fotos/ e prints); sem ela, o motor procura
subindo a partir do JSON. Caminhos de imagem no JSON podem ser relativos à base ou ao JSON.
Precisa do Google Chrome (ou Edge, Chromium, ou o navegador do instalador da Ilha de edição).
"""
import concurrent.futures as cf
import html
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ESTILOS = AQUI.parent / "assets" / "estilos"
sys.path.insert(0, str(AQUI))
import verificar_texto  # noqa: E402

LARG, ALT = 1080, 1350

# ---------------------------------------------------------------- navegador


def achar_chrome():
    ferr = Path(os.environ.get("MJ_FERRAMENTAS", Path.home() / ".marketing-juridico" / "ferramentas"))
    baixado = None
    try:
        baixado = json.loads((ferr / "caminhos.json").read_text(encoding="utf-8")).get("chrome")
    except Exception:
        pass
    pf = os.environ.get("PROGRAMFILES", "C:/Program Files")
    pf86 = os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")
    local = os.environ.get("LOCALAPPDATA", "")
    opcoes = [
        os.environ.get("CHROME_PATH"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        f"{pf}/Google/Chrome/Application/chrome.exe", f"{pf86}/Google/Chrome/Application/chrome.exe",
        f"{local}/Google/Chrome/Application/chrome.exe", f"{pf86}/Microsoft/Edge/Application/msedge.exe",
        f"{pf}/Microsoft/Edge/Application/msedge.exe",
        shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
        baixado,
    ]
    for c in opcoes:
        if c and Path(c).exists():
            return c
    return None


def chrome(exe, args, timeout=90):
    perfil = tempfile.mkdtemp(prefix="carrossel-chrome-")
    try:
        base = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                "--no-default-browser-check", "--allow-file-access-from-files", "--force-color-profile=srgb",
                f"--user-data-dir={perfil}"]
        return subprocess.run(base + args, capture_output=True, text=True, timeout=timeout)
    finally:
        shutil.rmtree(perfil, ignore_errors=True)


def foto_da_tela(exe, pagina, saida, largura, altura, escala=1, espera=9000):
    r = chrome(exe, [f"--force-device-scale-factor={escala}", f"--window-size={largura},{altura}",
                     f"--virtual-time-budget={espera}", f"--screenshot={saida}", Path(pagina).as_uri()])
    if not Path(saida).exists():
        raise RuntimeError(f"o navegador não gerou {Path(saida).name}: {r.stderr[-400:]}")


def ler_dom(exe, pagina):
    r = chrome(exe, ["--window-size=1080,1350", "--virtual-time-budget=9000", "--dump-dom", Path(pagina).as_uri()])
    return r.stdout


# ---------------------------------------------------------------- cores


def rgb(hexa):
    h = hexa.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(hexa):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb(hexa))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def melhor_sobre(fundo, claro="#FFFFFF", escuro="#141414"):
    return claro if contraste(fundo, claro) >= contraste(fundo, escuro) else escuro


# ---------------------------------------------------------------- traços à mão


def _rng(semente):
    return random.Random(str(semente))


def circulo_svg(semente):
    r = _rng(semente)
    rot = r.uniform(-4, 4)
    return ('<svg class="traco circulo-t" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
            f'<ellipse vector-effect="non-scaling-stroke" cx="50" cy="50" rx="49" ry="45" transform="rotate({rot:.1f} 50 50)"/>'
            f'<path vector-effect="non-scaling-stroke" d="M{50 + r.uniform(5, 15):.0f} 4 C 80 2, 99 20, 98 50"/></svg>')


SETA_SVG = ('<svg class="seta" viewBox="0 0 120 40" aria-hidden="true"><path d="M2 20 C 40 16, 80 24, 112 20"/>'
            '<path d="M96 8 L114 20 L96 32"/></svg>')

# ---------------------------------------------------------------- marcação do texto

_contador = [0]


def fmt(s):
    """Marcação simples do roteiro: *destaque*, **negrito**, ==marca-texto==, ~~riscado à mão~~,
    __sublinhado à mão__, [[circulado à mão]]. Quebra de linha vira <br>."""
    if s is None:
        return ""
    s = html.escape(str(s), quote=False)

    def mao(classe, svg):
        def f(m):
            _contador[0] += 1
            return f'<span class="{classe}">{m.group(1)}{svg(_contador[0])}</span>'
        return f
    def marca_js(classe):
        def f(m):
            _contador[0] += 1
            return f'<span class="{classe}" data-s="{_contador[0]}">{m.group(1)}</span>'
        return f
    s = re.sub(r"~~(.+?)~~", marca_js("risco"), s)
    s = re.sub(r"__(.+?)__", marca_js("sublinha"), s)
    s = re.sub(r"\[\[(.+?)\]\]", mao("circulo", circulo_svg), s)
    s = re.sub(r"==(.+?)==", r"<mark>\1</mark>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s.replace("\n", "<br>")


def rotulo_html(texto, classe="rotulo"):
    if not texto:
        return ""
    _contador[0] += 1
    return f'<div class="{classe}"><span>{fmt(texto)}</span>{circulo_svg(f"r{_contador[0]}")}</div>'


def el(tag, classe, conteudo, extra=""):
    if conteudo in (None, "", []):
        return ""
    return f'<{tag} class="{classe}"{extra}>{conteudo}</{tag}>'


# ---------------------------------------------------------------- mídia


class Midia:
    def __init__(self, base, pasta_json, saida):
        self.base, self.pasta_json, self.dest = base, pasta_json, saida / "midia"
        self.faltando = []

    def caminho(self, ref):
        if not ref:
            return None
        p = Path(os.path.expanduser(str(ref)))
        candidatos = [p] if p.is_absolute() else [self.base / p, self.pasta_json / p, self.base / "fotos" / p]
        for c in candidatos:
            if c.exists():
                return c
        self.faltando.append(str(ref))
        return None

    def src(self, ref):
        """Copia a imagem para midia/ e devolve o endereço relativo à pasta laminas/."""
        c = self.caminho(ref)
        if not c:
            return None
        self.dest.mkdir(parents=True, exist_ok=True)
        nome = re.sub(r"[^\w.\-]+", "-", c.name)
        alvo = self.dest / nome
        if not alvo.exists() or alvo.stat().st_size != c.stat().st_size:
            shutil.copy2(c, alvo)
        return f"../midia/{nome}"


# ---------------------------------------------------------------- lâminas


def bloco_imagem(l, midia, classe_padrao="foto", modo="moldura"):
    """Foto ou print da lâmina. Print que falta vira a área marcada, nunca uma tela desenhada."""
    if l.get("print") or l.get("print_descricao"):
        src = midia.src(l.get("print")) if l.get("print") else None
        if src:
            grifos = ""
            for i, g in enumerate(l.get("grifos") or []):
                x, y, w, h = (list(g) + [0, 0, 0, 0])[:4]
                if w and h:
                    grifos += (f'<div class="grifo" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%">'
                               f'{circulo_svg(f"g{i}{x}{y}")}</div>')
            return (f'<div class="print"><div class="quadro"><img src="{src}" alt="">{grifos}</div></div>')
        desc = html.escape(l.get("print_descricao") or "o print deste passo")
        return (f'<div class="print"><div class="falta"><div class="r">Print a capturar</div>'
                f'<div class="d">{desc}</div></div></div>')
    if l.get("foto"):
        src = midia.src(l["foto"])
        foco = html.escape(l.get("foco", "50% 30%"))
        if src:
            leg = el("figcaption", "legenda-foto", fmt(l.get("legenda_foto"))) if modo == "moldura" else ""
            return (f'<figure class="{classe_padrao} fm-{modo}"><div class="foto-img"><img src="{src}" alt="" '
                    f'style="object-position:{foco}"></div>{leg}</figure>')
        return '<figure class="foto falta-foto"><div class="falta"><div class="r">Foto não encontrada</div></div></figure>'
    return ""


def montar_lamina(l, n, total, dados, marca, midia, cfg=None):
    cfg = cfg or {}
    tipo = l.get("tipo", "texto")
    padrao_tipo = {"capa": "metade", "texto": "moldura", "convite": "recorte"}
    modo = (l.get("foto_modo") or dados.get("foto_modo") or (cfg.get("foto_modos") or {}).get(tipo)
            or cfg.get("foto_modo") or padrao_tipo.get(tipo, "cartao"))
    if modo == "padrao":
        modo = "moldura"
    permitidos = cfg.get("foto_modos_permitidos")
    if permitidos and modo not in permitidos and tipo != "convite":
        modo = "moldura" if "moldura" in permitidos else permitidos[0]
    if tipo == "convite" and modo in ("moldura", "recorte"):
        modo = "recorte"          # no convite, a foto vira o retrato redondo ao lado da chamada
    fundo_foto = ""
    if l.get("foto") and modo in ("sangrada", "cartao", "metade", "janela"):
        src = midia.src(l["foto"])
        if src:
            foco = html.escape(l.get("foco", "50% 30%"))
            fundo_foto = (f'<figure class="foto-livre fl-{modo}"><div class="foto-img"><img src="{src}" alt="" '
                          f'style="object-position:{foco}"></div></figure><div class="veu" aria-hidden="true"></div>')
        l = dict(l)
        l.pop("foto")
    secao_padrao = {"passo": l.get("rotulo") or f"Passo {l.get('numero', '')}".strip(), "regra": "A regra",
                    "mito": "Mito ou fato", "numero": "", "convite": "", "capa": dados.get("secao_capa", "")}
    secao = l.get("secao", secao_padrao.get(tipo, ""))
    rotulo = l.get("rotulo")
    fonte = l.get("fonte")
    fonte_html = el("div", "fonte", "Fonte: " + fmt(fonte)) if fonte else ""
    img = bloco_imagem(l, midia, modo=modo)
    titulo = el("h1", "titulo", fmt(l.get("titulo")), ' data-ajuste="1"')
    texto = el("p", "texto", fmt(l.get("texto")), ' data-ajuste="1" data-min="26"')

    if tipo == "capa":
        corpo = (el("div", "ante", fmt(l.get("antetitulo"))) + titulo + el("div", "sub", fmt(l.get("subtitulo")))
                 + img)
    elif tipo == "passo":
        num = l.get("numero")
        rot = rotulo or (f"Passo {num}" if num else "")
        corpo = rotulo_html(rot) + titulo + texto + img
    elif tipo == "lista":
        itens = l.get("itens") or []
        numerada = l.get("numerada", True)
        lis = ""
        for i, it in enumerate(itens, 1):
            t = it.get("texto") if isinstance(it, dict) else it
            d = it.get("detalhe") if isinstance(it, dict) else None
            t_html = fmt(f"~~{t}~~" if l.get("riscar") else t)
            lis += (f'<li><span class="num">{i:02d}</span><span class="txt"><span class="item">{t_html}</span>'
                    f'{el("span", "det", fmt(d))}</span></li>')
        corpo = (rotulo_html(rotulo) + titulo + texto
                 + f'<ol class="itens{" numerada" if numerada else ""}" data-ajuste="1" data-min="24">{lis}</ol>' + img)
    elif tipo == "mito":
        corpo = (rotulo_html(l.get("rotulo_mito", "Mito"), "rotulo mito-r")
                 + el("div", "mito", fmt(f"~~{l.get('mito', '')}~~"), ' data-ajuste="1" data-min="34"')
                 + rotulo_html(l.get("rotulo_fato", "Fato"), "rotulo fato-r")
                 + el("div", "fato", fmt(l.get("fato")), ' data-ajuste="1" data-min="28"'))
    elif tipo == "numero":
        corpo = (rotulo_html(rotulo) + el("div", "numero", fmt(l.get("numero")), ' data-ajuste="1" data-min="90"')
                 + texto + img)
    elif tipo == "regra":
        trecho = el("blockquote", "trecho", fmt(l.get("trecho")), ' data-ajuste="1" data-min="28"')
        refs = ""
        if l.get("itens"):
            refs = "".join(f'<li><span>{fmt(i.get("texto") if isinstance(i, dict) else i)}</span>'
                           f'<span class="ref">{fmt(i.get("ref", "") if isinstance(i, dict) else "")}</span></li>'
                           for i in l["itens"])
            refs = f'<ul class="refs" data-ajuste="1" data-min="26">{refs}</ul>'
        corpo = rotulo_html(rotulo) + titulo + texto + trecho + refs
    elif tipo == "citacao":
        corpo = (rotulo_html(rotulo) + '<div class="aspas" aria-hidden="true">“</div>'
                 + el("blockquote", "trecho", fmt(l.get("trecho") or l.get("texto")), ' data-ajuste="1" data-min="30"')
                 + el("div", "autor", fmt(l.get("autor"))) + img)
    elif tipo == "comparacao":
        cols = ""
        for lado, padrao in (("antes", "Antes"), ("depois", "Depois")):
            b = l.get(lado) or {}
            cols += (f'<div class="col col-{lado}">{el("div", "col-t", fmt(b.get("titulo", padrao)))}'
                     f'{el("div", "col-x", fmt(b.get("texto")))}</div>')
        corpo = rotulo_html(rotulo) + titulo + f'<div class="cols" data-ajuste="1" data-min="24">{cols}</div>'
    elif tipo == "convite":
        assinatura = " · ".join(x for x in (marca.get("nome"), marca.get("oab")) if x)
        foto = ""
        if l.get("foto"):
            src = midia.src(l["foto"])
            if src:
                foto = f'<figure class="retrato"><img src="{src}" alt="" style="object-position:{html.escape(l.get("foco", "50% 25%"))}"></figure>'
        corpo = (rotulo_html(rotulo) + titulo + texto
                 + f'<div class="cta">{foto}<div class="cta-txt">{el("div", "chamada", fmt(l.get("chamada")))}'
                 + el("div", "detalhe", fmt(l.get("detalhe"))) + "</div></div>"
                 + el("div", "assinatura", html.escape(marca.get("arroba", "")) + (f"<br><span>{html.escape(assinatura)}</span>" if assinatura else "")))
    else:  # texto
        corpo = rotulo_html(rotulo) + titulo + texto + img

    fundo = l.get("fundo")
    classes = [f"l", f"t-{tipo}", f"n-{n}"]
    if n == 1:
        classes.append("primeira")
    if n == total:
        classes.append("ultima")
    if fundo:
        classes.append(f"f-{fundo}")
    classes.append("par" if n % 2 == 0 else "impar")
    if fundo_foto:
        classes.append(f"com-foto fm-{modo}" + (" foto-sangrada" if modo == "sangrada" else ""))
    elif l.get("foto") and tipo != "convite":
        classes.append(f"com-foto fm-{modo}" + (" foto-padrao" if modo == "moldura" else ""))
    if l.get("print") or l.get("print_descricao"):
        classes.append("com-print")
    esq = l.get("rodape", dados.get("rodape", marca.get("nome", "")))
    arraste = "" if n == total else f'<span class="arraste">{SETA_SVG}</span>'
    progresso = '<span class="progresso">' + "".join(f'<i class="{"on" if k <= n else ""}"></i>' for k in range(1, total + 1)) + "</span>"
    return (f'<div class="{" ".join(classes)}">{fundo_foto}<div class="textura" aria-hidden="true"></div>'
            f'<header class="topo"><span class="marca">{html.escape(marca.get("arroba", ""))}</span>'
            f'<span class="secao">{fmt(secao)}</span></header>'
            f'<main class="corpo">{corpo}{fonte_html}</main>'
            f'<footer class="rodape"><span class="esq">{fmt(esq)}</span>'
            f'<span class="pag"><span class="pag-n">{n:02d}</span><span class="pag-t">/{total:02d}</span></span>{progresso}{arraste}</footer></div>')


JS = r"""
<script>
(function(){
  function afastar(){
    var f=document.querySelector('.fl-metade, .fl-janela'); if(!f) return;
    var rf=f.getBoundingClientRect(), folga=46;
    if(f.classList.contains('fl-metade')){
      var c=document.querySelector('.corpo'), rc=c.getBoundingClientRect();
      var pad=parseFloat(getComputedStyle(c).paddingTop)||0, falta=rf.bottom-rc.top+folga;
      if(falta>pad) c.style.paddingTop=falta+'px';
      return;
    }
    var direita=rf.left>540;
    ['.topo','.corpo','.rodape'].forEach(function(sel){
      var e=document.querySelector(sel); if(!e) return; var r=e.getBoundingClientRect();
      if(direita){ var a=r.right-rf.left+folga; if(a>0) e.style.paddingRight=(parseFloat(getComputedStyle(e).paddingRight)+a)+'px'; }
      else { var b=rf.right-r.left+folga; if(b>0) e.style.paddingLeft=(parseFloat(getComputedStyle(e).paddingLeft)+b)+'px'; }
    });
  }
  function encaixar(){
    document.querySelectorAll('.print').forEach(function(p){
      var q=p.querySelector('.quadro'), img=q&&q.querySelector('img'); if(!img||!img.naturalWidth) return;
      var bw=p.clientWidth, bh=p.clientHeight, r=img.naturalWidth/img.naturalHeight;
      var w=bw, h=bw/r;
      if(h>bh){ var w2=bh*r; if(w2>=bw*0.62){ w=w2; h=bh; } }   // cabe inteiro sem ficar miúdo; senão corta embaixo
      q.style.width=w+'px'; q.style.height=h+'px'; q.style.left=((bw-w)/2)+'px'; q.style.top=(h<bh?(bh-h)/2:0)+'px';
    });
  }
  function estoura(corpo, alvos){
    if(corpo.scrollHeight>corpo.clientHeight+2) return true;
    var pri=corpo.firstElementChild;   // texto alinhado embaixo que vaza por cima não aparece no scrollHeight
    if(pri && pri.getBoundingClientRect().top < corpo.getBoundingClientRect().top+(parseFloat(getComputedStyle(corpo).paddingTop)||0)-2) return true;
    for(var i=0;i<alvos.length;i++){ if(alvos[i].scrollWidth>alvos[i].clientWidth+2) return true; }
    var p=document.querySelector('.print'); if(p && p.clientHeight<200) return true;
    return false;
  }
  function fundo(alvos, corpo){
    // altura do bloco de texto (do primeiro ao último elemento), para valer também com texto centralizado
    var t=1e9, b=-1e9, pad=parseFloat(getComputedStyle(corpo).paddingTop)||0, ct=corpo.getBoundingClientRect().top+pad;
    [].slice.call(corpo.children).forEach(function(e){ if(e.matches('figure,.print,.fonte')) return; var r=e.getBoundingClientRect(); if(r.height){ t=Math.min(t,r.top); b=Math.max(b,r.bottom); } });
    if(b<0) return 0;
    var cs=getComputedStyle(corpo).justifyContent;
    return (cs==='flex-start'||cs==='normal') ? b-ct : b-t;
  }
  function crescer(corpo, alvos, original){
    // lâmina sem foto nem print: o texto cresce até ocupar a parte da lâmina que o estilo pede
    if(document.querySelector('.corpo .print, .corpo figure')) return;
    var meta=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--preencher'))||0.6;
    var voltas=0;
    var util=corpo.clientHeight-(parseFloat(getComputedStyle(corpo).paddingTop)||0)-(parseFloat(getComputedStyle(corpo).paddingBottom)||0);
    while(fundo(alvos,corpo)<util*meta && !estoura(corpo,alvos) && voltas<40){
      var mudou=false;
      alvos.forEach(function(a,i){
        var fs=parseFloat(getComputedStyle(a).fontSize), max=parseFloat(a.dataset.max||original[i]*1.6);
        if(fs<max){ a.style.fontSize=Math.min(max,fs*1.04)+'px'; mudou=true; }
      });
      if(!mudou) break; voltas++;
    }
  }
  function rnd(semente){ var x=semente*9301+49297; return function(){ x=(x*9301+49297)%233280; return x/233280; }; }
  function marcas(){
    var l=document.querySelector('.l'), base=l.getBoundingClientRect(), ns='http://www.w3.org/2000/svg';
    document.querySelectorAll('.traco-js').forEach(function(e){ e.remove(); });
    document.querySelectorAll('.risco,.sublinha').forEach(function(sp,k){
      var r=rnd(parseInt(sp.dataset.s||k+1,10)), risco=sp.classList.contains('risco');
      [].slice.call(sp.getClientRects()).forEach(function(rc){
        if(rc.width<6) return;
        var h=risco?rc.height*0.42:Math.max(10,rc.height*0.2);
        var top=risco?rc.top-base.top+rc.height*0.3:rc.bottom-base.top-h*0.35;
        var svg=document.createElementNS(ns,'svg');
        svg.setAttribute('class','traco traco-js '+(risco?'risco-t':'sublinha-t'));
        svg.setAttribute('viewBox','0 0 100 100'); svg.setAttribute('preserveAspectRatio','none');
        svg.style.cssText='left:'+(rc.left-base.left-rc.width*0.02)+'px;top:'+top+'px;width:'+(rc.width*1.04)+'px;height:'+h+'px;z-index:3';
        var d;
        if(risco){ d='M-1 '+(50+(r()-.5)*16)+' C33 '+(50+(r()-.5)*36)+' 66 '+(50+(r()-.5)*36)+' 101 '+(50+(r()-.5)*16); }
        else { d='M0 '+(50+(r()-.5)*40); for(var i=1;i<=6;i++){ d+=' L'+(100*i/6)+' '+(50+(r()-.5)*44); } }
        var p=document.createElementNS(ns,'path'); p.setAttribute('d',d); p.setAttribute('vector-effect','non-scaling-stroke');
        svg.appendChild(p); l.appendChild(svg);
      });
    });
  }
  function caber(){
    var corpo=document.querySelector('.corpo');
    var alvos=[].slice.call(document.querySelectorAll('[data-ajuste]'));
    var original=alvos.map(function(a){return parseFloat(getComputedStyle(a).fontSize);});
    crescer(corpo, alvos, original);
    var voltas=0;
    while(estoura(corpo,alvos) && voltas<80){
      var mudou=false;
      alvos.forEach(function(a){
        var fs=parseFloat(getComputedStyle(a).fontSize), min=parseFloat(a.dataset.min||'40');
        if(fs>min){ a.style.fontSize=Math.max(min,fs*0.96)+'px'; mudou=true; }
      });
      if(!mudou) break; voltas++;
    }
    var menor=1; alvos.forEach(function(a,i){ menor=Math.min(menor, parseFloat(getComputedStyle(a).fontSize)/original[i]); });
    document.body.setAttribute('data-estouro', estoura(corpo,alvos)?'1':'0');
    document.body.setAttribute('data-reducao', menor.toFixed(2));
  }
  var imgs=[].slice.call(document.images).map(function(i){ return i.decode?i.decode().catch(function(){}):Promise.resolve(); });
  Promise.all([document.fonts?document.fonts.ready:Promise.resolve()].concat(imgs)).then(function(){
    afastar(); encaixar(); caber(); encaixar(); marcas(); document.body.setAttribute('data-pronto','1');
  });
})();
</script>
"""

PAGINA = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080">
{fontes}
<style>
:root{{{vars}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:var(--fundo)}}
body{{-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}}
.l{{position:relative;width:1080px;height:1350px;overflow:hidden;display:flex;flex-direction:column}}
.corpo{{position:relative;flex:1;min-height:0;display:flex;flex-direction:column;overflow:hidden}}
.textura{{position:absolute;inset:0;pointer-events:none;z-index:0}}
.topo,.corpo,.rodape{{position:relative;z-index:2}}
.print{{position:relative;flex:1;min-height:0;overflow:hidden}}
.print .quadro{{position:absolute;top:0;left:0;width:100%;overflow:hidden}}
.print .quadro img{{display:block;width:100%;height:auto}}
.print .grifo{{position:absolute}}
.traco{{position:absolute;overflow:visible;pointer-events:none}}
.traco path,.traco ellipse{{fill:none;stroke-linecap:round;stroke-linejoin:round}}
.circulo{{position:relative;display:inline-block}}
.circulo .traco,.grifo .traco{{left:-8%;top:-14%;width:116%;height:128%}}
.seta path{{fill:none;stroke-linecap:round;stroke-linejoin:round}}
figure img{{display:block;width:100%;height:100%;object-fit:cover}}
.fundo-foto{{position:absolute;inset:0;z-index:0}}.veu{{position:absolute;inset:0;z-index:1;pointer-events:none}}
/* fotos: tratamento único do estilo e grão leve, para fotos de sessões diferentes conversarem */
figure{{position:relative}}.foto-img{{position:relative;width:100%;height:100%;overflow:hidden}}
.foto-img img{{filter:var(--tratamento,none)}}
.foto-img::after{{content:"";position:absolute;inset:0;pointer-events:none;opacity:var(--grao-foto,.22);mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .5 0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E")}}
.foto-livre{{position:absolute;margin:0;z-index:0}}
.fl-sangrada,.fl-cartao{{inset:0}}
.fl-metade{{left:0;right:0;top:0;height:var(--altura-metade,48%)}}
.fl-janela{{top:0;bottom:0;right:0;width:var(--largura-janela,43%)}}.par .fl-janela{{right:auto;left:0}}
/* sangrada: a lâmina inteira vira foto e o texto fica claro */
.fm-sangrada{{--texto:#FFF8EE;--suave:rgba(255,248,238,.84);--destaque:var(--destaque-claro);--linha:rgba(255,248,238,.45);color:var(--texto)}}
.fm-sangrada .veu{{background:linear-gradient(180deg,rgba(8,7,6,.34) 0%,rgba(8,7,6,.12) 32%,rgba(8,7,6,.58) 64%,rgba(8,7,6,.9) 100%)}}
.l.fm-sangrada .corpo{{justify-content:flex-end}}
.fm-sangrada .textura{{opacity:.25}}
/* cartão: folha lisa sobre a foto */
.fm-cartao .veu{{background:linear-gradient(180deg,rgba(0,0,0,.42),transparent 13%,transparent 85%,rgba(0,0,0,.42))}}
.fm-cartao .topo,.fm-cartao .rodape,.fm-metade .topo{{color:#FFF8EE}}
.fm-cartao .topo *,.fm-cartao .rodape *,.fm-metade .topo *{{color:inherit;border-color:currentColor}}
.fm-cartao .seta path{{stroke:#FFF8EE}}
.fm-cartao .corpo{{flex:0 1 auto;margin:auto 14px;background:var(--fundo);padding:66px 58px;justify-content:center;box-shadow:0 30px 70px rgba(0,0,0,.28)}}
.fm-cartao .textura{{opacity:0}}
/* metade: foto em cima, texto embaixo */
.fm-metade .veu{{height:var(--altura-metade,48%);background:linear-gradient(180deg,rgba(0,0,0,.4),transparent 26%)}}
.l.fm-metade .corpo{{justify-content:flex-start}}
/* moldura: a foto como foto impressa, com borda e legenda */
figure.fm-moldura{{margin-bottom:28px;display:flex;flex-direction:column;background:#FBF8F2;padding:16px 16px 0;box-shadow:0 18px 40px rgba(0,0,0,.2);transform:rotate(-1.4deg);overflow:visible}}
.par figure.fm-moldura{{transform:rotate(1.4deg)}}
figure.fm-moldura .foto-img{{flex:1;min-height:0}}
figure.fm-moldura .legenda-foto{{flex:none;padding:14px 4px 16px;font-family:var(--f-detalhe);font-size:22px;line-height:1.3;color:#3b362f;text-align:left}}
figure.fm-moldura:not(:has(figcaption)){{padding-bottom:16px}}
/* recorte: foto pequena, no canto, sem moldura */
.l .corpo figure.fm-recorte{{flex:none;width:330px;height:412px;margin-top:44px;align-self:flex-end;transform:none;border:0;padding:0;box-shadow:none;border-radius:0}}
.par .corpo figure.fm-recorte{{align-self:flex-start}}
.progresso{{display:none}}.rotulo{{position:relative}}.rotulo>span{{position:relative;z-index:1}}.rotulo .traco{{display:none;left:-16%;top:-34%;width:132%;height:168%}}
.falta{{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px}}
{css}
</style></head><body>{corpo}{js}</body></html>"""


def carregar_estilo(codigo):
    for pasta in sorted(ESTILOS.glob(f"{codigo}*")):
        if (pasta / "estilo.json").exists():
            cfg = json.loads((pasta / "estilo.json").read_text(encoding="utf-8"))
            return cfg, (pasta / "estilo.css").read_text(encoding="utf-8"), pasta
    disponiveis = ", ".join(p.name for p in sorted(ESTILOS.iterdir()) if p.is_dir())
    raise SystemExit(f"Estilo {codigo} não encontrado. Disponíveis: {disponiveis}")


def link_fonte(familia):
    f = familia.strip().replace(" ", "+")
    return (f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={f}:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&display=block">'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={f}:wght@400;700&display=block">'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={f}&display=block">')


def variaveis(cfg, marca):
    cores = dict(cfg.get("cores", {}))
    aceita = cfg.get("usa_da_marca", ["fundo", "texto", "destaque", "apoio", "suave"])
    cores.update({k: v for k, v in (marca.get("cores") or {}).items() if v and k in aceita})
    cores.setdefault("suave", cores.get("texto", "#333333"))
    cores.setdefault("apoio", cores.get("fundo", "#FFFFFF"))
    cores["sobre-destaque"] = melhor_sobre(cores["destaque"], cores.get("fundo") if luminancia(cores.get("fundo", "#fff")) > 0.6 else "#FFFFFF",
                                           cores.get("texto") if luminancia(cores.get("texto", "#000")) < 0.2 else "#141414")
    cores["sobre-escuro"] = cores.get("fundo") if luminancia(cores.get("fundo", "#fff")) > 0.6 else "#F5F2EC"
    cores.setdefault("escuro", cores.get("texto", "#141414"))
    r_, g_, b_ = rgb(cores["destaque"])
    if luminancia(cores["destaque"]) < 0.35:
        r_, g_, b_ = (round(c + (255 - c) * 0.62) for c in (r_, g_, b_))
    cores["destaque-claro"] = f"#{r_:02X}{g_:02X}{b_:02X}"
    fontes = dict(cfg.get("fontes", {}))
    for chave in ("titulo", "texto", "detalhe"):
        if marca.get(f"fonte_{chave}"):
            fontes[chave] = marca[f"fonte_{chave}"]
    linhas = [f"--{k}:{v}" for k, v in cores.items()]
    if cfg.get("tratamento"):
        linhas.append(f"--tratamento:{cfg['tratamento']}")
    pilha = {"titulo": "Georgia,serif", "texto": "system-ui,sans-serif", "detalhe": "ui-monospace,monospace"}
    for k, v in fontes.items():
        linhas.append(f"--f-{k}:'{v}',{pilha.get(k, 'sans-serif')}")
    proprias = [v for k, v in fontes.items() if marca.get(f"fonte_{k}")]
    links = "".join(f'<link rel="stylesheet" href="{html.escape(u)}">' for u in cfg.get("google_fonts", []))
    links += "".join(link_fonte(v) for v in dict.fromkeys(proprias))
    if not cfg.get("google_fonts"):
        links += "".join(link_fonte(v) for v in dict.fromkeys(fontes.values()))
    return ";".join(linhas), links, cores


def avisos_de_cor(cores):
    out = []
    pares = [("texto", "fundo", 4.5, "texto sobre o fundo"), ("destaque", "fundo", 3.0, "destaque sobre o fundo (título grande)"),
             ("sobre-destaque", "destaque", 4.5, "texto sobre a cor de destaque")]
    for a, b, minimo, nome in pares:
        if a in cores and b in cores:
            c = contraste(cores[a], cores[b])
            if c < minimo:
                out.append({"nivel": "CONFERIR", "onde": "cores", "sinal": "contraste baixo",
                            "trecho": f"{nome}: {c:.1f}:1", "troca": f"o mínimo é {minimo}:1; escureça ou clareie uma das cores"})
    return out


def prancha_html(dados, n, com_png, avisos, estouros):
    tema = html.escape(dados.get("tema", "Carrossel"))
    cards = ""
    for i in range(1, n + 1):
        tipo = html.escape(dados["laminas"][i - 1].get("tipo", ""))
        img = (f'<img src="png/carrossel-{i:02d}.png" alt="Lâmina {i}">' if com_png
               else f'<iframe src="laminas/lamina-{i:02d}.html" scrolling="no"></iframe>')
        alerta = '<span class="alerta">estourou</span>' if i in estouros else ""
        cards += (f'<div class="card"><div class="mini">{img}</div><div class="leg"><b>{i}</b> {tipo} {alerta}</div>'
                  f'<textarea data-n="{i}" placeholder="o que mudar nesta lâmina (deixe vazio se está bom)"></textarea></div>')
    lista = "".join(f"<li><b>{html.escape(a['nivel'])}</b> · {html.escape(a['onde'])} · {html.escape(a['sinal'])}: "
                    f"{html.escape(str(a['trecho']))}</li>" for a in avisos) or "<li>Nenhum alerta.</li>"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prancha do carrossel</title><style>
:root{{--fundo:#f4f2ee;--cartao:#fff;--tinta:#1d1b18;--suave:#6d675e;--linha:#ddd6ca;--acento:#8e1b2b}}
@media (prefers-color-scheme:dark){{:root{{--fundo:#1b1a18;--cartao:#262421;--tinta:#efebe4;--suave:#a8a196;--linha:#3a3631;--acento:#e59aa6}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--fundo);color:var(--tinta);font:16px/1.5 system-ui,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:28px 16px 80px}}h1{{font-size:24px;margin:0 0 4px}}p.s{{color:var(--suave);margin:0 0 22px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}}
.card{{background:var(--cartao);border:1px solid var(--linha);border-radius:12px;padding:10px}}
.mini{{aspect-ratio:4/5;overflow:hidden;border-radius:6px;background:#ccc;position:relative}}
.mini img{{width:100%;height:100%;display:block}}.mini iframe{{border:0;width:1080px;height:1350px;transform-origin:0 0;position:absolute;top:0;left:0}}
.leg{{font-size:14px;margin:8px 2px;color:var(--suave)}}.leg b{{color:var(--tinta)}}
.alerta{{background:var(--acento);color:#fff;border-radius:4px;padding:1px 6px;font-size:12px}}
textarea{{width:100%;min-height:54px;border:1px solid var(--linha);border-radius:8px;background:transparent;color:var(--tinta);font:inherit;font-size:14px;padding:6px}}
.barra{{position:sticky;bottom:0;margin-top:24px;background:var(--cartao);border:1px solid var(--linha);border-radius:12px;padding:12px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
button{{background:var(--acento);color:#fff;border:0;border-radius:8px;padding:10px 16px;font:inherit;cursor:pointer}}
details{{margin-top:22px}}ul{{padding-left:20px}}
</style></head><body><main>
<h1>{tema}</h1><p class="s">{n} lâminas · estilo {html.escape(dados.get('estilo', ''))}. Escreva o que mudar em cada lâmina e clique em "Copiar para o Claude". Tudo certo? Responda "aprovo" na conversa.</p>
<div class="grade">{cards}</div>
<div class="barra"><button id="copiar">Copiar para o Claude</button><span id="ok" class="s"></span></div>
<details><summary>Alertas do verificador ({len(avisos)})</summary><ul>{lista}</ul></details>
</main><script>
document.querySelectorAll('.mini iframe').forEach(function(f){{var m=f.parentNode;function r(){{f.style.transform='scale('+(m.clientWidth/1080)+')';}}r();addEventListener('resize',r);}});
document.getElementById('copiar').onclick=function(){{
  var linhas=[].slice.call(document.querySelectorAll('textarea')).filter(function(t){{return t.value.trim();}}).map(function(t){{return 'lâmina '+t.dataset.n+': '+t.value.trim();}});
  var txt=linhas.length?'Ajustes no carrossel "{tema}":\\n'+linhas.join('\\n'):'Aprovo o carrossel "{tema}".';
  try{{navigator.clipboard.writeText(txt).then(function(){{document.getElementById('ok').textContent='Copiado. Cole na conversa.';}});}}catch(e){{prompt('Copie o texto:',txt);}}
}};
</script></body></html>"""


def prancha_imagem_html(n):
    cols = 5 if n > 6 else n
    cards = "".join(f'<div class="c"><img src="png/carrossel-{i:02d}.png"><span>{i}</span></div>' for i in range(1, n + 1))
    return (f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}body{{background:#7a766e;padding:16px;display:grid;grid-template-columns:repeat({cols},324px);gap:16px;width:max-content}}
.c{{position:relative;width:324px;height:429px;padding-top:24px}}.c img{{width:324px;height:405px;display:block}}
.c span{{position:absolute;left:0;top:0;color:#fff;font:600 16px system-ui;line-height:20px}}
</style></head><body>{cards}</body></html>""", cols)


# ---------------------------------------------------------------- principal


def achar_base(pasta_json):
    for p in [pasta_json] + list(pasta_json.parents):
        if (p / "base").is_dir() or p.name == "meu-marketing-juridico":
            return p
    return pasta_json


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    arq = Path(argv[0]).resolve()
    opc = {}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a in ("--base", "--saida", "--estilo", "--so"):
            opc[a] = argv[i + 1]
            i += 2
        else:
            opc[a] = True
            i += 1
    dados = json.loads(arq.read_text(encoding="utf-8"))
    if opc.get("--estilo"):
        dados["estilo"] = opc["--estilo"]
    dados.setdefault("estilo", "C01")
    saida = Path(opc["--saida"]).resolve() if opc.get("--saida") else arq.parent
    base = Path(opc["--base"]).resolve() if opc.get("--base") else achar_base(arq.parent)
    marca = dados.get("marca") or {}

    achados = verificar_texto.verificar_carrossel(dados)
    verificar_texto.imprimir(achados)
    if any(a[0] == "CORRIGIR" for a in achados) and not opc.get("--forcar"):
        print("\nCorrija os itens acima no carrossel.json antes de montar (ou rode com --forcar só para ver um rascunho).")
        return 3

    cfg, css, _ = carregar_estilo(dados["estilo"])
    vars_css, links, cores = variaveis(cfg, marca)
    midia = Midia(base, arq.parent, saida)
    laminas = dados["laminas"]
    total = len(laminas)
    so = {int(x) for x in str(opc.get("--so", "")).split(",") if x.strip().isdigit()}
    (saida / "laminas").mkdir(parents=True, exist_ok=True)
    paginas = {}
    for n, l in enumerate(laminas, 1):
        corpo = montar_lamina(l, n, total, dados, marca, midia, cfg)
        pag = saida / "laminas" / f"lamina-{n:02d}.html"
        pag.write_text(PAGINA.format(fontes=links, vars=vars_css, css=css, corpo=corpo, js=JS), encoding="utf-8")
        paginas[n] = pag

    avisos = verificar_texto.como_dicts(achados) + avisos_de_cor(cores)
    for f in midia.faltando:
        avisos.append({"nivel": "CORRIGIR", "onde": "imagens", "sinal": "arquivo não encontrado", "trecho": f,
                       "troca": "confira o caminho (relativo à pasta meu-marketing-juridico)"})

    exe = achar_chrome()
    estouros, reducoes = set(), {}
    com_png = False
    if exe and not opc.get("--sem-png"):
        (saida / "png").mkdir(exist_ok=True)
        if opc.get("--alta"):
            (saida / "alta").mkdir(exist_ok=True)
        alvo = [n for n in paginas if not so or n in so]

        def render(n):
            pag = paginas[n]
            foto_da_tela(exe, pag, saida / "png" / f"carrossel-{n:02d}.png", LARG, ALT)
            if opc.get("--alta"):
                foto_da_tela(exe, pag, saida / "alta" / f"carrossel-{n:02d}.png", LARG, ALT, escala=2, espera=11000)
            dom = ler_dom(exe, pag)
            m = re.search(r'data-reducao="([\d.]+)"', dom)
            return n, ('data-estouro="1"' in dom), float(m.group(1)) if m else 1.0

        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for n, estourou, red in ex.map(render, alvo):
                print(f"ok lâmina {n}" + ("  (ESTOUROU: encurte o texto)" if estourou else ""))
                if estourou:
                    estouros.add(n)
                reducoes[n] = red
        com_png = all((saida / "png" / f"carrossel-{n:02d}.png").exists() for n in paginas)
        for n in sorted(estouros):
            avisos.append({"nivel": "CORRIGIR", "onde": f"lâmina {n}", "sinal": "texto não coube",
                           "trecho": "mesmo no tamanho mínimo", "troca": "encurte ou divida em duas lâminas"})
        for n, red in sorted(reducoes.items()):
            if n not in estouros and red < 0.7:
                avisos.append({"nivel": "CONFERIR", "onde": f"lâmina {n}", "sinal": "título encolheu muito",
                               "trecho": f"{round(red * 100)}% do tamanho do estilo", "troca": "texto mais curto deixa a lâmina mais forte"})
    elif not exe:
        print("\nNavegador não encontrado: as lâminas ficaram em HTML, sem PNG. Instale o Google Chrome "
              "(ou rode o instalador da Ilha de edição) e rode de novo, ou use o caminho do Canva.")

    (saida / "prancha.html").write_text(prancha_html(dados, total, com_png, avisos, estouros), encoding="utf-8")
    if com_png:
        pi, cols = prancha_imagem_html(total)
        tmp = saida / "_prancha-imagem.html"
        tmp.write_text(pi, encoding="utf-8")
        linhas = (total + cols - 1) // cols
        foto_da_tela(exe, tmp, saida / "prancha.png", 16 + cols * 340, 16 + linhas * 445, espera=4000)
        tmp.unlink(missing_ok=True)
    rel = {"tema": dados.get("tema"), "estilo": dados["estilo"], "laminas": total, "png": com_png,
           "estouros": sorted(estouros), "avisos": avisos, "saida": str(saida)}
    (saida / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nPronto: {saida}")
    print("prancha.html (para o advogado) e prancha.png (para a sua conferência)" if com_png else "prancha.html")
    corrigir = [a for a in avisos if a["nivel"] == "CORRIGIR"]
    if corrigir:
        print(f"{len(corrigir)} item(ns) para corrigir no relatório antes de mostrar.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
