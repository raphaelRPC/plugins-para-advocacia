"""Motor da Ilha de edição: lê o projeto.js da Mesa de edição e monta qualquer vídeo.

Uso:
  python3 montar_video.py catalogo <memoria.json> <saida.html> [video]
  python3 montar_video.py preparar <ffmpeg> <original> <transcricao.json> <pasta_mesa> [nome]
  python3 montar_video.py quadros  <ffmpeg> <original> <pasta_mesa> <pasta_saida> <t1> [t2 ...]
  python3 montar_video.py video    <ffmpeg> <original> <pasta_mesa> <saida.mp4>
  python3 montar_video.py aplicar  <pasta_mesa> <texto colado da Mesa, da prancha ou do Catálogo> [memoria.json]
  python3 montar_video.py revisar  [<ffmpeg> <original>] <pasta_mesa> [--aplicar]
  python3 montar_video.py zona     <ffmpeg> <original> <pasta_mesa> [organico|impulsionado]
  python3 montar_video.py prancha  <ffmpeg> <original> <pasta_mesa> [memoria.json] [cor_da_marca]
  python3 montar_video.py aprender <pasta_mesa> <respostas da prancha ou da Mesa> <memoria.json>
  python3 montar_video.py favorito <pasta_mesa> <memoria.json> "<nome do favorito>"
  python3 montar_video.py cenas    <ffmpeg> <cenas.json> <pasta_mesa> [--voz <áudio ou vídeo>]

catalogo: o primeiro passo de cada edição, antes de processar o vídeo: grava uma cópia do Catálogo com os favoritos do
          advogado e o caminho do vídeo. Ele escolhe o caminho (já sei o que quero, só corta e legenda, sugere para mim) e cola.
preparar: cria proxy.mp4, picos do áudio, palavras e cortes automáticos de pausa no projeto.js
          (preserva inserts, efeitos, estilo e notas se o projeto já existir) e lista avisos de transcrição.
quadros:  gera quadros finais (com inserts e legenda) nos tempos do vídeo ORIGINAL, para conferir.
video:    gera o vídeo final com cortes, velocidade, cor, zoom, efeitos, inserts e legenda.
revisar:  aponta hesitações ("é...", "hum"), palavra repetida, take repetido e corte que come palavra;
          com ffmpeg e original, monta o áudio editado e a lista de emendas para transcrever.py --emendas.
          --aplicar acrescenta aos cortes o que foi achado (confira antes).
zona:     percorre o vídeo editado (a cada 0,25 s) e aponta texto ou gráfico fora da zona segura da rede,
          com o quadro marcado em <pasta_mesa>/_zona/. Perfil impulsionado = regra de anúncio do Meta. O perfil
          conferido fica gravado em estilo.zona: no impulsionado, o alto desce, a base sobe e a legenda fica em 1200 no máximo.
prancha:  a única página antes de montar (prancha.html na pasta da Mesa): pontos de partida (o formato sugerido em
          P['prancha'], 2 alternativas e os favoritos da memória), o visual sobre o quadro do vídeo (família, legenda e
          altura, cores, tom, fontes, quantidade de peças, corte), a versão B opcional, 2 ou 3 peças por momento de
          P['momentos'] (ordenadas pelo placar) e os fatos a confirmar. As respostas voltam pelo aplicar.
aplicar:  com o pedido do Catálogo (depois do preparar), grava o visual escolhido, trava o visual para a prancha curta e
          recorta as pausas no ritmo dele; favorito pelo nome precisa da memória.
          Com o texto da prancha, grava o visual, recorta as pausas no ritmo escolhido, grava a peça de cada momento
          e, se houver versão B, cria <pasta_mesa>-b.
aprender: atualiza a memória (placar de escolhas por tipo de momento, pontos de partida, ajustes por vídeo).
favorito: guarda o visual do vídeo aprovado como ponto de partida com nome, oferecido nas próximas pranchas.
cenas:    vídeo sem rosto (formato F13): lê o roteiro de cenas, calcula o tempo de cada bloco pela régua de leitura
          (sem voz) ou pela fala (com voz), gera o original fundo.mp4 e o insert único do modelo cenas, e grava a
          prancha das cenas. Com --voz, só cria o fundo com a voz: transcreva, prepare e revise o fundo.mp4 e rode de novo.

Os estilos aceitos estão descritos em references/catalogo-de-estilos.md.
"""
import sys, os, json, re, math, wave, array, subprocess, hashlib, tempfile, colorsys, platform
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # acentos no terminal do Windows
except Exception: pass

W, H, FPS = 1080, 1920, 30
TOPO = 215          # zona dos títulos (abaixo da barra superior da rede)
BASE = 1500         # base da zona de inserts de baixo (acima da legenda do post, zona segura até 1520)
TOPO_TXT = 232      # primeira linha de texto das famílias sem caixa (zona segura começa em 220)
LEG_Y = 1300        # linha de base da legenda
# anúncio pago (estilo.zona = "impulsionado", gravado pelo comando zona): a zona segura vai de y 270 a 1248,
# então os textos do alto descem, os de baixo sobem e a legenda fica acima do botão do anúncio
DY_ANUNCIO = 55     # quanto os textos do alto descem (TOPO 215 -> 270, TOPO_TXT 232 -> 287)
BASE_ANUNCIO = 1240 # base da zona de inserts de baixo no anúncio
LEG_Y_ANUNCIO = 1200  # legenda mais baixa possível no anúncio (a base da letra fica acima de 1248)
MARGEM_X = 66       # primeira coluna dentro da zona segura (65)
# o alto padrão de cada modelo animado (o D.topo de cada .html); no anúncio ele desce DY_ANUNCIO
TOPO_MODELOS = {'antesdepois': 236, 'calendario': 250, 'citacao': 232, 'dado': 262, 'leque': 230, 'linhadotempo': 240,
                'notebook3d': 200, 'logo3d': 210}

def anuncio(C): return C.get('zona') == 'impulsionado'
def topo_txt(C): return TOPO_TXT + (DY_ANUNCIO if anuncio(C) else 0)
def topo_caixa(C): return TOPO + (DY_ANUNCIO if anuncio(C) else 0)
def base_y(C): return BASE_ANUNCIO if anuncio(C) else BASE
def y_legenda_do(est):
    """altura da legenda do vídeo (estilo.yLegenda); no anúncio, nunca abaixo de LEG_Y_ANUNCIO"""
    y = est.get('yLegenda') or LEG_Y
    return min(y, LEG_Y_ANUNCIO) if est.get('zona') == 'impulsionado' else y

def dados_anuncio(modelo, dados, C):
    """no anúncio, o modelo animado do alto desce para dentro da zona (só quando o projeto não fixou o topo)"""
    if not anuncio(C) or 'topo' in dados: return dados
    if modelo == 'frase': base = 300 if dados.get('modo') == 'riscado' else 248
    elif modelo == 'trilha': base = 220 if dados.get('orientacao') == 'horizontal' else None
    elif modelo == 'palavra': return dict(dados, topo=topo_txt(C))      # o fecho sobe para cima da cabeça: embaixo fica o botão
    elif modelo == 'logo3d' and dados.get('modo') == 'maos': base = None
    else: base = TOPO_MODELOS.get(modelo)
    return dict(dados, topo=base + DY_ANUNCIO) if base is not None else dados

# ---------- cor ----------
HLG = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=gamma=1.12:saturation=1.04")
SDR = "format=yuv420p"

def filtro_cor(ff, original):
    info = subprocess.run([ff, '-i', original], capture_output=True, text=True).stderr
    return HLG if 'arib-std-b67' in info else SDR

def fonte_video(ff, original, pasta):
    """(arquivo, filtro de cor) de onde saem os quadros. O vídeo do iPhone em HDR é convertido para a cor das redes
    uma vez só, em <pasta_mesa>/_base/base.mp4 (refeito se o original mudar): a conversão custa mais que ler o vídeo,
    e cada comando (prancha, quadros, zona, vídeo) lia o original de novo. Vídeo comum é lido direto.
    MJ_SEM_BASE=1 volta ao jeito antigo."""
    cor = filtro_cor(ff, original)
    if cor == SDR or os.environ.get('MJ_SEM_BASE'): return original, cor
    d = os.path.join(pasta, '_base'); arq = os.path.join(d, 'base.mp4'); reg = os.path.join(d, 'base.json')
    st = os.stat(original); marca = {'original': os.path.abspath(original), 'tamanho': st.st_size, 'mtime': int(st.st_mtime), 'filtro': cor, 'fps': FPS}
    try: pronto = os.path.exists(arq) and json.load(open(reg, encoding='utf-8')) == marca
    except Exception: pronto = False
    if not pronto:
        os.makedirs(d, exist_ok=True); print('convertendo a cor do vídeo (uma vez só por vídeo)', flush=True)
        tmp = os.path.join(d, 'base-parcial.mp4')
        subprocess.run([ff, '-y', '-loglevel', 'error', '-i', original, '-map', '0:v:0', '-an', '-vf', f'fps={FPS},{cor}', '-c:v', 'libx264',
                        '-preset', 'veryfast', '-crf', '12', '-g', str(FPS), '-pix_fmt', 'yuv420p', '-colorspace', 'bt709',
                        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', tmp], check=True)
        os.replace(tmp, arq); json.dump(marca, open(reg, 'w', encoding='utf-8'))
    return arq, SDR

# ---------- fontes (macOS, com alternativas) ----------
# no Windows: Segoe UI, Bahnschrift (com largura condensada), Georgia e Consolas, que vêm com o sistema
WF = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
FONTES = {
    'heavy': [('/System/Library/Fonts/Avenir Next.ttc', 8), ('/System/Library/Fonts/HelveticaNeue.ttc', 1), (f'{WF}/seguibl.ttf', 0), (f'{WF}/arialbd.ttf', 0)],
    'bold':  [('/System/Library/Fonts/Avenir Next.ttc', 0), ('/System/Library/Fonts/HelveticaNeue.ttc', 1), (f'{WF}/segoeuib.ttf', 0), (f'{WF}/arialbd.ttf', 0)],
    'demi':  [('/System/Library/Fonts/Avenir Next.ttc', 2), ('/System/Library/Fonts/HelveticaNeue.ttc', 0), (f'{WF}/seguisb.ttf', 0), (f'{WF}/arial.ttf', 0)],
    'med':   [('/System/Library/Fonts/Avenir Next.ttc', 5), ('/System/Library/Fonts/HelveticaNeue.ttc', 0), (f'{WF}/segoeui.ttf', 0), (f'{WF}/arial.ttf', 0)],
    'serifa': [('/System/Library/Fonts/NewYorkItalic.ttf', 0), ('/System/Library/Fonts/Supplemental/Georgia Italic.ttf', 0), (f'{WF}/georgiai.ttf', 0)],
    'serif':  [('/System/Library/Fonts/NewYork.ttf', 0), ('/System/Library/Fonts/Supplemental/Georgia.ttf', 0), (f'{WF}/georgia.ttf', 0)],
    'mono':  [('/System/Library/Fonts/Menlo.ttc', 1), (f'{WF}/consolab.ttf', 0)],
    'cond':  [('/System/Library/Fonts/Avenir Next Condensed.ttc', 8), ('/System/Library/Fonts/Supplemental/Futura.ttc', 4), ('/System/Library/Fonts/HelveticaNeue.ttc', 1),
              (f'{WF}/bahnschrift.ttf', 0, 'Bold Condensed'), (f'{WF}/arialnb.ttf', 0), (f'{WF}/arialbd.ttf', 0)],
    'didoti': [('/System/Library/Fonts/Supplemental/Didot.ttc', 1), ('/System/Library/Fonts/NewYorkItalic.ttf', 0), ('/System/Library/Fonts/Supplemental/Georgia Italic.ttf', 0), (f'{WF}/georgiai.ttf', 0)],
}
_fc = {}
FONTES_PAR = {}   # tipo -> (arquivo, peso): as fontes do padrão do advogado (estilo.fontes), por cima das do sistema

def font(tipo, tam):
    k = (tipo, tam)
    if k not in _fc and tipo in FONTES_PAR:
        arq, peso = FONTES_PAR[tipo]
        try:
            f = ImageFont.truetype(arq, tam)
            try:                                  # fonte variável: escolhe o peso, mantém os outros eixos no padrão
                eixos = f.get_variation_axes()
                f.set_variation_by_axes([peso if str(e.get('name', b'')).lower().find('weight') >= 0 else e['default'] for e in eixos])
            except Exception: pass
            _fc[k] = f
        except Exception: pass
    if k not in _fc:
        for p, i, *var in FONTES[tipo]:
            if os.path.exists(p):
                f = ImageFont.truetype(p, tam, index=i)
                if var:                      # fonte variável: escolhe a instância pelo nome (ex.: Bold Condensed)
                    try:
                        nomes = {n.decode('latin-1').lower() if isinstance(n, bytes) else n.lower(): n for n in f.get_variation_names()}
                        if var[0].lower() in nomes: f.set_variation_by_name(nomes[var[0].lower()])
                    except Exception: pass
                _fc[k] = f; break
        else:
            _fc[k] = ImageFont.load_default()
    return _fc[k]

NAVY = (20, 36, 63); AMBAR = (242, 179, 61); WHITE = (255, 255, 255); PEN = (74, 111, 240)
OK = (76, 195, 138); SOFT = (201, 209, 222); RED = (222, 52, 48)

OURO = (233, 196, 120); CREME = (246, 236, 214)
FAMILIAS_VALIDAS = ('editorial', 'revista', 'atras', 'institucional', 'celular')

def cores(P):
    """cores da marca (estilo.cores, em hex) e a família visual do vídeo (estilo.familia).
    estilo.cores = "video": usa a paleta tirada do cenário do próprio vídeo (estilo.coresVideo)"""
    est = P.get('estilo', {}); c = est.get('cores', {})
    if c == 'video': c = est.get('coresVideo', {})
    fam = est.get('familia', 'institucional')
    if fam not in FAMILIAS_VALIDAS: fam = 'institucional'
    conv = lambda v, d: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) if isinstance(v, str) and v.startswith('#') else d
    return {'fundo': conv(c.get('fundo'), NAVY), 'destaque': conv(c.get('destaque'), AMBAR if fam == 'institucional' else OURO),
            'acao': conv(c.get('acao'), PEN), 'ok': conv(c.get('ok'), OK), 'alerta': conv(c.get('alerta'), RED),
            'texto': conv(c.get('texto'), WHITE), 'gigante': conv(c.get('gigante'), CREME), 'familia': fam,
            'destaques': {x.lower() for x in est.get('destaques', [])}, 'zona': est.get('zona', 'organico')}

# ---------- animação ----------
def clamp(x): return max(0.0, min(1.0, x))
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def pr(t, a, b): return clamp((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)
def janela(t, a, b, fade=0.25):
    if t < a or t > b + fade: return 0.0, 0.0
    ent = eo(pr(t, a, a + fade)); sai = 1 - eo(pr(t, b, b + fade))
    return ent * sai, ent

def colar(frame, L, x, y, alpha):
    if alpha <= 0.01: return
    a = L.split()[3]
    if alpha < 0.999: a = a.point(lambda v: int(v * alpha))
    frame.paste(L.convert('RGB'), (int(x), int(y)), a)

def cartao(w, h, cor, alpha=235, raio=30):
    L = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
    ImageDraw.Draw(L).rounded_rectangle([0, 0, w - 1, h - 1], radius=raio, fill=cor + (alpha,))
    return L

def caber(tipo, tam, texto, largura, minimo=24):
    f = font(tipo, tam)
    while f.getlength(texto) > largura and tam > minimo:
        tam -= 2; f = font(tipo, tam)
    return f

# ---------- projeto ----------
def ler_projeto(pasta):
    txt = open(os.path.join(pasta, 'projeto.js'), encoding='utf-8').read()
    return json.loads(txt[txt.index('{'):txt.rindex('}') + 1])

def gravar_projeto(pasta, P):
    open(os.path.join(pasta, 'projeto.js'), 'w', encoding='utf-8').write(
        'window.PROJETO = ' + json.dumps(P, ensure_ascii=False) + ';\n')

class Linha:
    """Converte tempos do original em tempos editados (antes da velocidade)."""
    def __init__(self, P):
        dur = P['duracao']; ant = 0.0; self.seg = []
        for a, b in sorted(P['cortes']):
            if a > ant + 0.02: self.seg.append((ant, a))
            ant = max(ant, b)
        if ant < dur - 0.02: self.seg.append((ant, dur))
        self.off = []; acc = 0.0
        for a, b in self.seg: self.off.append(acc); acc += b - a
        self.total = acc

    def m(self, t):
        for (a, b), o in zip(self.seg, self.off):
            if a - 0.001 <= t <= b + 0.001: return o + (t - a)
        return None

    def mc(self, t, depois=True):
        """como m(), mas um tempo dentro de um corte vai para o começo do trecho seguinte (ou fim do anterior)"""
        v = self.m(t)
        if v is not None: return v
        if depois:
            for (a, b), o in zip(self.seg, self.off):
                if a > t: return o
            return self.total
        res = 0.0
        for (a, b), o in zip(self.seg, self.off):
            if b < t: res = o + (b - a)
        return res

    def orig(self, tn):
        """tempo editado de volta para o tempo do original"""
        for (a, b), o in zip(self.seg, self.off):
            if tn < o + (b - a): return a + tn - o
        return self.seg[-1][1] if self.seg else tn

    def indice(self, tn):
        for i, ((a, b), o) in enumerate(zip(self.seg, self.off)):
            if tn < o + (b - a): return i
        return len(self.seg) - 1

# ---------- inserts ----------
def marcas(ins, L, n):
    """tempos (editados) em que cada parte do insert aparece"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    mk = [L.mc(x) for x in ins.get('marcas', [])][:n]
    if len(mk) < n:
        ini = mk[-1] if mk else a
        resto = n - len(mk); passo = max(0.3, (b - 0.6 - ini) / max(1, resto))
        mk += [ini + passo * (i + (1 if mk else 0)) for i in range(resto)]
    return mk

# inserts da zona de baixo escondem a legenda; os de cima também, se tiverem ocultaLegenda
ZONA_BASE = {'formula', 'chamada', 'cartao', 'fluxo', 'chips', 'lista', 'cta', 'cartaz'}

def ins_duascamadas(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b)
    if al <= 0: return
    w = 900; mk = marcas(ins, L, 3)
    fr_ = caber('demi', 40, ins.get('rotulo', ''), w - 90)
    ft = caber('heavy', 104, ins.get('titulo', ''), w - 90)
    fs = caber('demi', 40, ins.get('sub', ''), w - 90)
    h = 40 + (54 if ins.get('rotulo') else 0) + 112 + (56 if ins.get('sub') else 0) + 26
    Lc = cartao(w, h, C['fundo'], 248); d = ImageDraw.Draw(Lc); y = 40
    if ins.get('rotulo'):
        p = eo(pr(t, mk[0], mk[0] + 0.25))
        d.text((w / 2, y + 22), ins['rotulo'], font=fr_, fill=WHITE + (int(255 * p),), anchor='mm'); y += 54
    p = back(pr(t, mk[1], mk[1] + 0.35)); pa = eo(pr(t, mk[1], mk[1] + 0.2))
    if pa > 0:
        T = Image.new('RGBA', (w, 130), (0, 0, 0, 0))
        ImageDraw.Draw(T).text((w / 2, 62), ins.get('titulo', ''), font=ft, fill=C['destaque'] + (int(255 * pa),), anchor='mm')
        sc = 0.8 + 0.2 * p
        T = T.resize((int(w * sc), int(130 * sc)), Image.BICUBIC)
        Lc.alpha_composite(T, (int((w - T.width) / 2), int(y - 8 + (130 - T.height) / 2)))
    y += 112
    if ins.get('sub'):
        p = eo(pr(t, mk[2], mk[2] + 0.25))
        d.text((w / 2, y + 22), ins['sub'], font=fs, fill=SOFT + (int(255 * p),), anchor='mm')
    colar(fr, Lc, (W - w) / 2, topo_caixa(C) + (1 - ent) * -30, al)

PAPEL = (248, 244, 235)

def espacado(d, xy, texto, f, cor, track):
    """texto centrado com espaço extra entre letras (versalete de convite)"""
    larg = sum(f.getlength(c) for c in texto) + track * (len(texto) - 1)
    x = xy[0] - larg / 2
    for c in texto:
        d.text((x, xy[1]), c, font=f, fill=cor, anchor='lm'); x += f.getlength(c) + track

def ins_bilhete(fr, t, ins, L, C):
    """Cartão-convite: cartão de papel, linha pequena em versalete, linha grande em itálico com serifa"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b, 0.35)
    if al <= 0: return
    mk = marcas(ins, L, 2)
    w, h = 760, 270 + (52 if ins.get('sub') else 0)
    Lc = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(Lc)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=10, fill=PAPEL + (255,))
    d.rounded_rectangle([14, 14, w - 15, h - 15], radius=6, outline=C['destaque'] + (200,), width=2)
    if ins.get('rotulo'):
        p = eo(pr(t, mk[0], mk[0] + 0.3))
        espacado(d, (w / 2, 68), ins['rotulo'].upper(), font('serif', 34), C['fundo'] + (int(235 * p),), 7)
        d.line([(w / 2 - 60 * p, 104), (w / 2 + 60 * p, 104)], fill=C['destaque'] + (int(255 * p),), width=2)
    p = eo(pr(t, mk[1], mk[1] + 0.4))
    if p > 0:
        ft = caber('serifa', 118, ins.get('titulo', ''), w - 90)
        d.text((w / 2, 178 + (1 - p) * 14), ins.get('titulo', ''), font=ft, fill=C['fundo'] + (int(255 * p),), anchor='mm')
    if ins.get('sub'):
        d.text((w / 2, 262), ins['sub'], font=font('demi', 34), fill=(110, 104, 92, int(255 * p)), anchor='mm')
    ang = -2.0 - 4.0 * (1 - ent)
    sombra = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle([40, 52, w + 40, h + 52], radius=12, fill=(0, 0, 0, 110))
    sombra = sombra.filter(ImageFilter.GaussianBlur(16))
    base = Image.new('RGBA', (w + 80, h + 80), (0, 0, 0, 0)); base.alpha_composite(sombra); base.alpha_composite(Lc, (40, 40))
    R = base.rotate(ang, resample=Image.BICUBIC, expand=True)
    colar(fr, R, (W - R.width) / 2, topo_caixa(C) + (1 - ent) * 70, al)

def ins_tarja(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    linhas = [x for x in (ins.get('titulo', ''), ins.get('sub', '')) if x]
    for i, txt in enumerate(linhas):
        al, ent = janela(t, a + 0.15 * i, b)
        if al <= 0: continue
        f = caber('heavy', 64, txt.upper(), 900)
        tw = f.getlength(txt.upper()); h = 64 + 26
        Lt = Image.new('RGBA', (int(tw) + 44, h), C['alerta'] + (255,))
        ImageDraw.Draw(Lt).text((22, h / 2 + 2), txt.upper(), font=f, fill=WHITE + (255,), anchor='lm')
        colar(fr, Lt, 90 + (1 - ent) * -60, ins.get('y', topo_caixa(C) + 20) + i * (h + 8), al)

def ins_rotulos(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    mk = marcas(ins, L, len(ins.get('itens', [])))
    y = topo_caixa(C) + 20
    if ins.get('rotulo'):
        f = font('mono', 30)
        Lr = Image.new('RGBA', (int(f.getlength(ins['rotulo'])) + 10, 44), (0, 0, 0, 0))
        ImageDraw.Draw(Lr).text((0, 22), ins['rotulo'], font=f, fill=WHITE + (255,), anchor='lm', stroke_width=3, stroke_fill=(0, 0, 0, 160))
        colar(fr, Lr, 90, y, al); y += 56
    for item, tm in zip(ins.get('itens', []), mk):
        p = eo(pr(t, tm, tm + 0.25))
        if p <= 0: continue
        f = font('heavy', 46); tw = f.getlength(item.upper())
        Lp = cartao(tw + 56, 76, C['fundo'], 240, 38); d = ImageDraw.Draw(Lp)
        d.text((28, 40), item.upper(), font=f, fill=C['destaque'] + (255,), anchor='lm')
        colar(fr, Lp, 90 + (1 - p) * -50, y, al * p); y += 90

def ins_formula(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b)
    if al <= 0: return
    termos = ins.get('itens', []); n = len(termos)
    mk = marcas(ins, L, n + 1)
    w = 940; lh = 74; h = 36 + (n + 1) * lh + 22
    Lc = cartao(w, h, C['fundo']); d = ImageDraw.Draw(Lc)
    paleta = [C['acao'], C['destaque'], (155, 109, 240), (46, 170, 220)]
    f = font('heavy', 44); fo = font('heavy', 46)
    for i in range(n + 1):
        y = 36 + i * lh; x0 = 110
        res = i == n
        txt = ins.get('titulo', '') if res else termos[i]
        p = eo(pr(t, mk[i], mk[i] + 0.25))
        op = '=' if res else ('+' if i else '')
        if op: d.text((60, y + 30), op, font=fo, fill=WHITE + (255,), anchor='mm')
        fx = caber('heavy', 44, txt, w - x0 - 80)
        tw = fx.getlength(txt) + 48
        if p <= 0:
            d.rounded_rectangle([x0, y, x0 + min(tw, 360), y + 60], radius=14, outline=(255, 255, 255, 90), width=3)
            continue
        cor = C['ok'] if res else paleta[i % len(paleta)]
        tx = NAVY if res or cor == C['destaque'] else WHITE
        d.rounded_rectangle([x0, y, x0 + tw, y + 60], radius=14, fill=cor + (int(255 * p),))
        d.text((x0 + 24, y + 31), txt, font=fx, fill=tx + (int(255 * p),), anchor='lm')
    colar(fr, Lc, (W - w) / 2, base_y(C) - h + (1 - ent) * 40, al)

def ins_chamada(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b)
    if al <= 0: return
    ft = caber('heavy', 96, ins.get('titulo', ''), 860); fr_ = font('demi', 40)
    tw = ft.getlength(ins.get('titulo', '')) + 80; rw = fr_.getlength(ins.get('rotulo', '')) + 48
    w = int(max(tw, rw)); h = 70 + 150
    Lc = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(Lc)
    if ins.get('rotulo'):
        x = (w - rw) / 2
        d.rounded_rectangle([x, 0, x + rw, 64], radius=10, fill=C['fundo'] + (255,))
        d.text((w / 2, 33), ins['rotulo'], font=fr_, fill=WHITE + (255,), anchor='mm')
    x = (w - tw) / 2
    d.rounded_rectangle([x, 72, x + tw, 72 + 140], radius=16, fill=WHITE + (255,))
    d.text((w / 2, 72 + 72), ins.get('titulo', ''), font=ft, fill=C['fundo'] + (255,), anchor='mm')
    sc = 0.85 + 0.15 * back(pr(t, a, a + 0.35))
    L2 = Lc.resize((int(w * sc), int(h * sc)), Image.BICUBIC)
    colar(fr, L2, (W - L2.width) / 2, base_y(C) - L2.height + (1 - ent) * 40, al)

def ins_perfil(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b, 0.3)
    if al <= 0: return
    nome = ins.get('titulo', ''); linha = ins.get('sub', '')
    fn = font('heavy', 44); fl = font('demi', 32)
    w = int(max(fn.getlength(nome), fl.getlength(linha)) + 190); h = 128
    Lc = cartao(w, h, WHITE, 245, 64); d = ImageDraw.Draw(Lc)
    d.ellipse([18, 18, 110, 110], fill=C['fundo'] + (255,))
    ini = ''.join(p[0] for p in nome.split()[:2]).upper()
    d.text((64, 66), ini, font=font('heavy', 38), fill=WHITE + (255,), anchor='mm')
    d.text((132, 46), nome, font=fn, fill=C['fundo'] + (255,), anchor='lm')
    if linha: d.text((132, 90), linha, font=fl, fill=(90, 100, 118, 255), anchor='lm')
    colar(fr, Lc, 70 + (1 - ent) * -(w + 80), topo_caixa(C) + 10, al)

def ins_cartao(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b)
    if al <= 0: return
    w = 960; ft = caber('heavy', 70, ins.get('titulo', ''), w - 88)
    h = 190 + (56 if ins.get('sub') else 0)
    Lc = cartao(w, h, C['fundo']); d = ImageDraw.Draw(Lc)
    d.text((44, 38), ins.get('rotulo', ''), font=font('mono', 28), fill=C['destaque'] + (255,))
    d.text((44, 82), ins.get('titulo', ''), font=ft, fill=WHITE + (255,))
    if ins.get('sub'): d.text((46, 182), ins['sub'], font=font('demi', 40), fill=SOFT + (255,))
    colar(fr, Lc, (W - w) / 2, base_y(C) - h + (1 - ent) * 40, al)

def ins_carimbo(fr, t, ins, L, C):
    """Carimbo: selo girado que bate na tela (escala de 1,7 para 1)"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if t < a or t > b + 0.25: return
    p = pr(t, a, a + 0.3); al = eo(p) * (1 - eo(pr(t, b, b + 0.25)))
    txt = ins.get('titulo', ''); f = font('mono', 50); w = int(f.getlength(txt)) + 70; h = 50 + 40
    cor = C['ok'] if re.search('APROV|SIM', txt, re.I) else C['destaque']
    Ls = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(Ls)
    d.rounded_rectangle([7, 7, 7 + w, 7 + h], radius=h // 2, fill=C['fundo'] + (235,), outline=cor + (255,), width=7)
    d.text((7 + w / 2, 7 + h / 2), txt, font=f, fill=cor + (255,), anchor='mm')
    Ls = Ls.rotate(-6, resample=Image.BICUBIC, expand=True)
    sc = 1 + (1 - eo(p)) * 0.7
    Ls = Ls.resize((int(Ls.width * sc), int(Ls.height * sc)), Image.BICUBIC)
    cy = ins.get('y', 360)          # padrão no alto; use y para mudar
    colar(fr, Ls, (W - Ls.width) / 2, cy - Ls.height / 2, al)

def ins_fluxo(fr, t, ins, L, C):
    """Fluxo: rótulo e itens ligados por seta, cada item entrando na sua marca"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, ent = janela(t, a, b)
    if al <= 0: return
    itens = ins.get('itens', []); mk = marcas(ins, L, len(itens))
    w = 960; h = 250; Lc = cartao(w, h, C['fundo']); d = ImageDraw.Draw(Lc)
    d.text((44, 36), ins.get('rotulo', ''), font=font('mono', 28), fill=C['destaque'] + (255,))
    f = font('heavy', 54); larg = sum(f.getlength(x) + 60 for x in itens) + 110 * (len(itens) - 1)
    x = (w - larg) / 2; cores_ = [C['acao'], C['ok']]
    for i, (it, tm) in enumerate(zip(itens, mk)):
        p = eo(pr(t, tm, tm + 0.3))
        bw = f.getlength(it) + 60
        if i:
            d.line([(x - 95, 160), (x - 95 + 80 * p, 160)], fill=WHITE + (int(255 * p),), width=6)
        if p > 0:
            cor = cores_[min(i, 1)] if i in (0, len(itens) - 1) else C['acao']
            d.rounded_rectangle([x, 115, x + bw, 205], radius=20, fill=cor + (int(255 * p),))
            d.text((x + bw / 2, 160), it, font=f, fill=(NAVY if cor == C['ok'] else WHITE) + (int(255 * p),), anchor='mm')
        x += bw + 110
    colar(fr, Lc, (W - w) / 2, base_y(C) - h + (1 - ent) * 40, al)

# ---------- famílias visuais (sem caixa): editorial, revista e atrás de você ----------
def familia(ins, C):
    """a família do insert: a dele, se tiver, ou a do vídeo"""
    f = ins.get('familia') or C['familia']
    return f if f in FAMILIAS_VALIDAS else 'institucional'

def quebrar(texto, f, largura):
    linhas, cur = [], []
    for w in texto.split():
        if cur and f.getlength(' '.join(cur + [w])) > largura: linhas.append(cur); cur = []
        cur.append(w)
    if cur: linhas.append(cur)
    return linhas

def bloco(fr, pecas, alpha, sombra=0.6, raio=12):
    """desenha peças de texto sem caixa, com sombra suave. Cada peça: dict(x, y, txt | palavras, f, cor, p, track, alinh).
    p (0 a 1) faz a linha subir de uma máscara (revela de baixo para cima)"""
    if alpha <= 0.01 or not pecas: return
    x0 = 0; y0 = max(0, int(min(pc['y'] for pc in pecas)) - 40)
    y1 = min(H, int(max(pc['y'] + pc['f'].size * 1.35 for pc in pecas)) + 40)
    Lb = Image.new('RGBA', (W, y1 - y0), (0, 0, 0, 0))
    for pc in pecas:
        p = clamp(pc.get('p', 1.0))
        if p <= 0: continue
        f = pc['f']; lh = int(f.size * 1.3)
        Ll = Image.new('RGBA', (W, lh), (0, 0, 0, 0)); d = ImageDraw.Draw(Ll)
        dy = (1 - eo(p)) * lh
        palavras = pc.get('palavras') or [(pc['txt'], pc['cor'])]
        track = pc.get('track', 0)
        larg = sum((sum(f.getlength(c) + track for c in t) if track else f.getlength(t)) for t, _ in palavras) + f.getlength(' ') * (len(palavras) - 1)
        x = pc['x'] if pc.get('alinh', 'esq') == 'esq' else (W - larg) / 2
        for t, cor in palavras:
            if track:
                for ch in t: d.text((x, dy), ch, font=f, fill=cor + (255,)); x += f.getlength(ch) + track
            else:
                d.text((x, dy), t, font=f, fill=cor + (255,)); x += f.getlength(t)
            x += f.getlength(' ')
        Lb.alpha_composite(Ll, (0, int(pc['y'] - y0)))
    if sombra:
        s_ = Image.new('RGBA', Lb.size, (0, 0, 0, 0))
        s_.putalpha(Lb.split()[3].point(lambda v: int(v * sombra)).filter(ImageFilter.GaussianBlur(raio)))
        colar(fr, s_, 0, y0 + 4, alpha)
    colar(fr, Lb, 0, y0, alpha)

def colorir(txt, C, cor=None):
    cor = cor or C['texto']
    return [(w, C['destaque'] if re.sub(r'[^\wÀ-ú]', '', w).lower() in C['destaques'] else cor) for w in txt.split()]

def fam_titulo(fr, t, ins, L, C):
    """título em duas camadas nas famílias editorial e revista"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    mk = marcas(ins, L, 3); fam = familia(ins, C); pecas = []; y = ins.get('y', topo_txt(C))
    if fam == 'revista':
        if ins.get('rotulo'):
            pecas.append(dict(x=82, y=y, txt=ins['rotulo'].upper(), f=font('med', 32), cor=C['texto'], p=pr(t, mk[0], mk[0] + .4), track=7)); y += 56
            fio = eo(pr(t, mk[0] + .15, mk[0] + .9))
            if fio > 0: ImageDraw.Draw(fr).rectangle([84, y - 6, 84 + 120 * fio, y - 1], fill=C['destaque'])
            y += 10
        tam = 140                                          # a palavra mais longa precisa caber na largura
        while tam > 70 and max([font('didoti', tam).getlength(w) for w in ins.get('titulo', '').split()] or [0]) > 900: tam -= 8
        f = font('didoti', tam)
        for i, ln in enumerate(quebrar(ins.get('titulo', ''), f, 900)):
            pecas.append(dict(x=86, y=y, txt=' '.join(ln), f=f, cor=C['texto'], p=pr(t, mk[1] + i * .12, mk[1] + i * .12 + .6))); y += int(f.size * 1.05)
        if ins.get('sub'):
            pecas.append(dict(x=82, y=y + 14, txt=ins['sub'], f=font('med', 38), cor=C['texto'], p=pr(t, mk[2], mk[2] + .5)))
        bloco(fr, pecas, al, .65, 14); return
    if ins.get('rotulo'):
        pecas.append(dict(x=80, y=y, txt=ins['rotulo'].upper(), f=font('demi', 36), cor=C['texto'], p=pr(t, mk[0], mk[0] + .4), track=6)); y += 62
    tam = 170
    while True:
        f = font('cond', tam); linhas = quebrar(ins.get('titulo', ''), f, 930)
        larga = max([f.getlength(w) for w in ins.get('titulo', '').split()] or [0]) > 930   # palavra longa não pode passar da borda
        if (len(linhas) <= 2 and not larga) or tam <= 70: break
        tam -= 10
    for i, ln in enumerate(linhas):
        pecas.append(dict(x=72, y=y, palavras=colorir(' '.join(ln), C), f=f, cor=C['texto'], p=pr(t, mk[1] + i * .12, mk[1] + i * .12 + .55))); y += int(f.size * .92)
    if ins.get('sub'):
        pecas.append(dict(x=80, y=y + 18, txt=ins['sub'], f=font('demi', 40), cor=C['texto'], p=pr(t, mk[2], mk[2] + .5)))
    bloco(fr, pecas, al, .6, 14)

def fam_rotulos(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    itens = ins.get('itens', []); mk = marcas(ins, L, len(itens)); y = ins.get('y', topo_txt(C)); pecas = []
    revista = familia(ins, C) == 'revista'
    tam = 84 if revista else 92                       # item longo: a letra diminui até caber na zona segura
    while True:
        f = font('didoti', tam) if revista else font('cond', tam)
        if tam <= 48 or max([f.getlength('/ ' + (x if revista else x.upper())) for x in itens] or [0]) <= 900: break
        tam -= 4
    for it, tm in zip(itens, mk):
        txt = it if revista else it.upper()
        pecas.append(dict(x=80, y=y, palavras=[('·' if revista else '/', C['destaque']), (txt, C['texto'])], f=f, cor=C['texto'], p=pr(t, tm, tm + .5)))
        y += int(f.size * 1.02)
    bloco(fr, pecas, al, .6, 12)

def fam_chamada(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    mk = marcas(ins, L, 2); pecas = []; y = ins.get('y', topo_txt(C) if anuncio(C) else 1250)      # y e tam: chamada no alto, acima da cabeça (anúncio: o botão cobre a parte de baixo)
    if ins.get('rotulo'):
        pecas.append(dict(x=82, y=y, txt=ins['rotulo'].upper(), f=font('demi', 36), cor=C['texto'], p=pr(t, a, a + .4), track=6)); y += 58
    palavra = ins.get('titulo', '')
    if familia(ins, C) == 'revista':
        fio = eo(pr(t, a + .15, a + .9))
        if fio > 0: ImageDraw.Draw(fr).rectangle([84, y - 8, 84 + 120 * fio, y - 3], fill=C['destaque'])
        f = caber('didoti', ins.get('tam', 190), palavra, 930)
        pecas.append(dict(x=74, y=y + 4, txt=palavra, f=f, cor=C['texto'], p=pr(t, mk[0], mk[0] + .6))); y += int(f.size * 1.32)
    else:
        f = caber('cond', ins.get('tam', 200 if anuncio(C) else 280), palavra.upper(), 930)
        for i, ch in enumerate(palavra.upper()):          # letra por letra, cada uma subindo da máscara
            x = 72 + f.getlength(palavra.upper()[:i])
            pecas.append(dict(x=x, y=y, txt=ch, f=f, cor=C['destaque'], p=pr(t, mk[0] + i * .07, mk[0] + i * .07 + .45)))
        y += int(f.size * 1.08)
    if ins.get('sub'):
        pecas.append(dict(x=82, y=y, txt=ins['sub'], f=font('demi', 42), cor=C['texto'], p=pr(t, mk[0] + .6, mk[0] + 1.1)))
    bloco(fr, pecas, al, .6, 12)

def fam_carimbo(fr, t, ins, L, C):
    """frase de destaque: marca-texto na última palavra (editorial) ou sublinhado (revista)"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    txt = ins.get('titulo', ''); revista = familia(ins, C) == 'revista'
    f = font('didoti', 118) if revista else font('cond', 150)
    linhas = quebrar(txt if revista else txt.upper(), f, 930); y = ins.get('y', topo_txt(C)); pecas = []
    for i, ln in enumerate(linhas):
        pecas.append(dict(x=74, y=y + i * int(f.size * (1.05 if revista else .92)), txt=' '.join(ln), f=f, cor=C['texto'], p=pr(t, a + i * .12, a + i * .12 + .55)))
    ult = linhas[-1][-1]; ly = y + (len(linhas) - 1) * int(f.size * (1.05 if revista else .92))
    xu = 74 + f.getlength(' '.join(linhas[-1][:-1]) + (' ' if len(linhas[-1]) > 1 else ''))
    m = eo(pr(t, a + .5, a + 1.0)); d = ImageDraw.Draw(fr)
    if m > 0 and al > .2:
        if revista: d.rectangle([xu, ly + f.size * 1.08, xu + f.getlength(ult) * m, ly + f.size * 1.08 + 6], fill=C['destaque'])
        else:
            x0 = max(xu - 10, MARGEM_X); d.rectangle([x0, ly + f.size * .42, x0 + (xu + f.getlength(ult) + 10 - x0) * m, ly + f.size * 1.02], fill=C['destaque'])
            pecas[-1]['palavras'] = [(w, C['texto']) for w in linhas[-1][:-1]] + [(ult, (20, 22, 26))]
    bloco(fr, pecas, al, .55 if not revista else .65, 12)

def fam_perfil(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b, .35)
    if al <= 0: return
    revista = familia(ins, C) == 'revista'
    pecas = [dict(x=80, y=topo_txt(C), txt=ins.get('titulo', ''), f=font('didoti', 50) if revista else font('demi', 40), cor=C['texto'], p=pr(t, a, a + .5))]
    if ins.get('sub'): pecas.append(dict(x=82, y=topo_txt(C) + 60, txt=ins['sub'], f=font('med', 30), cor=C['texto'], p=pr(t, a + .15, a + .6), track=2 if revista else 0))
    bloco(fr, pecas, al, .6, 10)

def tracos(fr, pts, p, cor, larg):
    """desenha uma linha de vários pontos até a fração p (0 a 1) do comprimento: o traço de caneta"""
    seg = list(zip(pts, pts[1:])); tot = sum(math.dist(a, b) for a, b in seg); falta = tot * clamp(p); d = ImageDraw.Draw(fr)
    for a, b in seg:
        if falta <= 0: break
        l = math.dist(a, b); k = min(1, falta / l); fim = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        d.line([a, fim], fill=cor, width=larg, joint='curve'); d.ellipse([fim[0] - larg / 2, fim[1] - larg / 2, fim[0] + larg / 2, fim[1] + larg / 2], fill=cor)
        falta -= l

def ins_mitofato(fr, t, ins, L, C):
    """Mito e fato: o mito entra, leva um X na marca, e o fato entra com o visto.
    campos: mito, fato, rotulos [mito, fato] (opcional), marcas [mito, X, fato]"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b)
    if al <= 0: return
    mk = marcas(ins, L, 3); fam = familia(ins, C); rot = ins.get('rotulos', ['Mito', 'Fato'])
    revista = fam == 'revista'; caixa = fam == 'institucional'
    tm_, tf_ = ins.get('mito', '') if revista else ins.get('mito', '').upper(), ins.get('fato', '') if revista else ins.get('fato', '').upper()
    def caber_linhas(tipo, tam, txt, larg, n):
        while True:
            f = font(tipo, tam); ln = quebrar(txt, f, larg)
            if len(ln) <= n or tam <= 40: return f, ln
            tam -= 6
    fm, lm = caber_linhas('didoti' if revista else 'cond', 60 if revista else 70, tm_, 860, 2)
    ff_, lf = caber_linhas('didoti' if revista else 'cond', 86 if revista else 100, tf_, 860, 3)
    fr_ = font('demi', 32); x = 84; y = topo_txt(C) + (20 if caixa else 0)
    risco = eo(pr(t, mk[1], mk[1] + .45)); apaga = 1 - .45 * risco
    hm = 52 + len(lm) * int(fm.size * 1.05); hf = 52 + len(lf) * int(ff_.size * (1.02 if revista else .95))
    if caixa:
        colar(fr, cartao(920, hm + 30, C['fundo'], 235, 24), x - 24, y - 18, al * eo(pr(t, mk[0], mk[0] + .3)))
        if t >= mk[2]: colar(fr, cartao(920, hf + 30, C['fundo'], 245, 24), x - 24, y + hm + 40 - 18, al * eo(pr(t, mk[2], mk[2] + .3)))
    pecas = [dict(x=x, y=y, txt=rot[0].upper(), f=fr_, cor=C['texto'], p=pr(t, mk[0], mk[0] + .4), track=6)]
    for i, ln in enumerate(lm):
        cor = tuple(int(v * apaga + 110 * (1 - apaga)) for v in C['texto'])
        pecas.append(dict(x=x, y=y + 52 + i * int(fm.size * 1.05), txt=' '.join(ln), f=fm, cor=cor, p=pr(t, mk[0] + i * .1, mk[0] + i * .1 + .5)))
    yf = y + hm + 40
    if t >= mk[2]:
        pecas.append(dict(x=x + 70, y=yf, txt=rot[1].upper(), f=fr_, cor=C['texto'], p=pr(t, mk[2], mk[2] + .4), track=6))
        for i, ln in enumerate(lf):
            pecas.append(dict(x=x, y=yf + 52 + i * int(ff_.size * (1.02 if revista else .95)), palavras=colorir(' '.join(ln), C), f=ff_, cor=C['texto'], p=pr(t, mk[2] + .1 + i * .1, mk[2] + .6 + i * .1)))
    bloco(fr, pecas, al, .6, 12)
    if risco > 0 and al > .2:              # X em dois traços sobre o mito
        x1 = x + max(fm.getlength(' '.join(l)) for l in lm) + 10; y0, y1 = y + 60, y + 44 + len(lm) * int(fm.size * 1.05)
        cor = C['alerta']
        tracos(fr, [(x - 10, y0), (x1, y1)], pr(t, mk[1], mk[1] + .22), cor, 11)
        tracos(fr, [(x1, y0), (x - 10, y1)], pr(t, mk[1] + .18, mk[1] + .42), cor, 11)
    if t >= mk[2] and al > .2:             # visto ao lado do rótulo do fato
        tracos(fr, [(x + 4, yf + 22), (x + 22, yf + 42), (x + 54, yf + 4)], pr(t, mk[2] + .2, mk[2] + .55), C['ok'], 10)

# atrás de você: a palavra gigante vai atrás da pessoa (recorte nativo do macOS), o resto fica na frente
ATRAS_TIPOS = {'duascamadas', 'chamada', 'carimbo'}

def atras_palavra(ins):
    if ins.get('palavra'): return ins['palavra'].upper()
    base = ins.get('titulo', '')
    return (base if ins['tipo'] == 'chamada' else (base.split()[-1] if base.split() else '')).upper().strip('.,!?')

def atras_fundo(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b, .3)
    if al <= 0: return
    pal = atras_palavra(ins); f = caber('cond', 420, pal, 1015, 60)
    g = eo(pr(t, a + .15, a + .9)); sc = .92 + .08 * g
    Lg = Image.new('RGBA', (W, int(f.size * 1.2)), (0, 0, 0, 0))
    ImageDraw.Draw(Lg).text((W / 2, Lg.height / 2), pal, font=f, fill=C['gigante'] + (255,), anchor='mm')
    if sc < .999: Lg = Lg.resize((int(W * sc), int(Lg.height * sc)), Image.BICUBIC)
    cy = ins.get('yGigante', 560)
    s_ = Image.new('RGBA', Lg.size, (0, 0, 0, 0)); s_.putalpha(Lg.split()[3].point(lambda v: int(v * .35)).filter(ImageFilter.GaussianBlur(14)))
    colar(fr, s_, (W - Lg.width) / 2, cy - Lg.height / 2 + 6, al * g); colar(fr, Lg, (W - Lg.width) / 2, cy - Lg.height / 2, al * g)

def atras_frente(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b, .3)
    if al <= 0: return
    pecas = []; pal = atras_palavra(ins)
    if ins['tipo'] == 'carimbo':
        resto = ins.get('titulo', '').upper().strip('.,!?'); resto = resto[: max(0, len(resto) - len(pal))].strip()
        topo = resto
    else:
        topo = ins.get('rotulo', '')
    if topo: pecas.append(dict(x=0, y=topo_txt(C), txt=topo.upper(), f=font('demi', 38), cor=C['texto'], p=pr(t, a, a + .4), track=6, alinh='centro'))
    if ins.get('sub'): pecas.append(dict(x=0, y=1360, txt=ins['sub'].upper(), f=font('cond', 64), cor=C['texto'], p=pr(t, a + .8, a + 1.3), alinh='centro'))
    bloco(fr, pecas, al, .6, 10)

# celular: o jeito de quem edita no aplicativo do próprio celular. Sem movimento (entra e sai em corte seco),
# letra forte branca pequena e alinhada à esquerda acima da cabeça, uma palavra de destaque, marcas desenhadas
# no lugar de emoji, texto com fundo branco para a frase principal, legenda uma palavra por vez.
def seco(t, a, b): return 1.0 if a <= t <= b else 0.0

def texto_cel(fr, x, y, palavras, f, alpha=1.0, contorno=4):
    """texto com contorno escuro fino, como o texto padrão dos aplicativos de edição"""
    Lt = Image.new('RGBA', (W, int(f.size * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(Lt); xx = x
    for t, cor in palavras:
        d.text((xx, f.size * .2), t, font=f, fill=cor + (255,), stroke_width=contorno, stroke_fill=(0, 0, 0, 150)); xx += f.getlength(t + ' ')
    colar(fr, Lt, 0, y - f.size * .2, alpha)

def cel_titulo(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if not seco(t, a, b): return
    mk = marcas(ins, L, 3); y = topo_txt(C)
    if ins.get('rotulo') and t >= mk[0]:
        f = font('bold', 40); texto_cel(fr, 90, y, [(ins['rotulo'], C['texto'])], f, contorno=3); y += 58
    if t >= mk[1]:
        f = caber('heavy', 66, ins.get('titulo', ''), 10 ** 9)
        for ln in quebrar(ins.get('titulo', ''), f, 880)[:3]:
            texto_cel(fr, 90, y, colorir(' '.join(ln), C), f); y += int(f.size * 1.12)
    if ins.get('sub') and t >= mk[2]:
        texto_cel(fr, 90, y + 6, [(ins['sub'], C['texto'])], font('demi', 38), contorno=3)

def cel_rotulos(fr, t, ins, L, C):
    """lista com visto desenhado; item começando com "não" ou "x " leva um X"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if not seco(t, a, b): return
    itens = ins.get('itens', []); mk = marcas(ins, L, len(itens)); y = topo_txt(C); f = font('heavy', 58)
    for it, tm in zip(itens, mk):
        if t < tm: break
        neg = it.lower().startswith(('não', 'nao', 'x '))
        txt = it[2:] if it.lower().startswith('x ') else it
        if neg: tracos(fr, [(96, y + 14), (140, y + 58)], 1, C['alerta'], 10); tracos(fr, [(140, y + 14), (96, y + 58)], 1, C['alerta'], 10)
        else: tracos(fr, [(94, y + 38), (112, y + 58), (144, y + 14)], 1, C['ok'], 10)
        texto_cel(fr, 166, y, [(txt, C['texto'])], f); y += 84

def cel_chamada(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if not seco(t, a, b): return
    f = font('heavy', 64); y = 1180; pal = [(ins.get('rotulo', ''), C['texto'])] if ins.get('rotulo') else []
    texto_cel(fr, 90, y, pal + [(ins.get('titulo', '').upper(), C['destaque'])], f)
    if ins.get('sub'): texto_cel(fr, 90, y + 84, [(ins['sub'], C['texto'])], font('demi', 40), contorno=3)

def cel_carimbo(fr, t, ins, L, C):
    """frase com fundo branco, como o texto com fundo dos aplicativos"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if not seco(t, a, b): return
    f = font('heavy', 60); y = ins.get('y', topo_txt(C) + 10)
    for ln in quebrar(ins.get('titulo', ''), f, 860):
        txt = ' '.join(ln); w = f.getlength(txt) + 44
        Lc = cartao(w, int(f.size * 1.35), WHITE, 255, 14)
        ImageDraw.Draw(Lc).text((22, f.size * .68), txt, font=f, fill=(17, 17, 17, 255), anchor='lm')
        colar(fr, Lc, 90, y, 1); y += int(f.size * 1.35) + 6

def cel_perfil(fr, t, ins, L, C):
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    if not seco(t, a, b): return
    texto_cel(fr, 90, topo_txt(C), [(ins.get('titulo', ''), C['texto'])], font('bold', 40), contorno=3)
    if ins.get('sub'): texto_cel(fr, 90, topo_txt(C) + 54, [(ins['sub'], C['texto'])], font('med', 32), contorno=3)

def ins_fixo(fr, t, ins, L, C):
    """Título fixo: a ideia do vídeo no alto, do começo ao fim (receita Dica única). Pequeno, para não brigar com a fala.
    campos: titulo, rotulo (opcional)"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b, .3)
    if al <= 0: return
    fam = familia(ins, C); y = topo_txt(C); pecas = []
    if fam == 'celular':
        if ins.get('rotulo'): texto_cel(fr, 90, y, [(ins['rotulo'], C['texto'])], font('bold', 36), contorno=3); y += 50
        f = caber('heavy', 58, ins.get('titulo', ''), 10 ** 9)
        for ln in quebrar(ins.get('titulo', ''), f, 880)[:2]: texto_cel(fr, 90, y, colorir(' '.join(ln), C), f); y += int(f.size * 1.12)
        return
    if fam == 'institucional':
        f = caber('heavy', 54, ins.get('titulo', ''), 10 ** 9); ln = quebrar(ins.get('titulo', ''), f, 840)[:2]
        h = 40 + len(ln) * int(f.size * 1.15) + (44 if ins.get('rotulo') else 0)
        Lc = cartao(920, h, C['fundo'], 235, 24); d = ImageDraw.Draw(Lc); yy = 22
        if ins.get('rotulo'): d.text((40, yy), ins['rotulo'].upper(), font=font('demi', 28), fill=C['destaque'] + (255,)); yy += 44
        for l in ln: d.text((40, yy), ' '.join(l), font=f, fill=WHITE + (255,)); yy += int(f.size * 1.15)
        colar(fr, Lc, 80, y, al); return
    revista = fam == 'revista'
    if ins.get('rotulo'):
        pecas.append(dict(x=82, y=y, txt=ins['rotulo'].upper(), f=font('demi', 30), cor=C['texto'], p=pr(t, a, a + .4), track=6)); y += 50
    f = font('didoti', 68) if revista else font('cond', 76)
    for i, ln in enumerate(quebrar(ins.get('titulo', '') if revista else ins.get('titulo', '').upper(), f, 900)[:2]):
        pecas.append(dict(x=78, y=y, palavras=colorir(' '.join(ln), C), f=f, cor=C['texto'], p=pr(t, a + .1 + i * .1, a + .6 + i * .1))); y += int(f.size * (1.05 if revista else .95))
    bloco(fr, pecas, al, .6, 12)

def ins_cartaz(fr, t, ins, L, C):
    """Cartaz: texto útil na tela, sem fala (receita Cartaz, 6 a 10 s); o conteúdo completo vai na legenda do post.
    Um plano escurece o vídeo e o texto entra em linhas. campos: rotulo, titulo, itens [linhas], assinatura, plano (0 a 1, padrão 0,72)"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    al, _ = janela(t, a, b, .35)
    if al <= 0: return
    colar(fr, Image.new('RGBA', (W, H), C['fundo'] + (int(255 * ins.get('plano', .72)),)), 0, 0, al)
    revista = familia(ins, C) == 'revista'; y = 330; pecas = []
    if ins.get('rotulo'): pecas.append(dict(x=90, y=y, txt=ins['rotulo'].upper(), f=font('demi', 34), cor=C['destaque'], p=pr(t, a, a + .4), track=6)); y += 70
    ft = font('didoti', 104) if revista else font('cond', 124)
    for i, ln in enumerate(quebrar(ins.get('titulo', '') if revista else ins.get('titulo', '').upper(), ft, 900)[:4]):
        pecas.append(dict(x=86, y=y, palavras=colorir(' '.join(ln), C), f=ft, cor=C['texto'], p=pr(t, a + .2 + i * .12, a + .8 + i * .12))); y += int(ft.size * (1.05 if revista else .95))
    y += 40; fi = font('demi', 46); mk = marcas(ins, L, len(ins.get('itens', [])))
    for it, tm in zip(ins.get('itens', []), mk):
        for j, ln in enumerate(quebrar(it, fi, 860)):
            pecas.append(dict(x=92, y=y, palavras=[('·', C['destaque']), (' '.join(ln), C['texto'])] if j == 0 else [(' '.join(ln), C['texto'])], f=fi, cor=C['texto'], p=pr(t, tm, tm + .45))); y += int(fi.size * 1.3)
        y += 14
    if ins.get('assinatura'): pecas.append(dict(x=92, y=min(1440, y + 40), txt=ins['assinatura'], f=font('med', 34), cor=C['texto'], p=pr(t, a + .6, a + 1.1)))
    bloco(fr, pecas, al, .35, 10)

def aplicar_cor(fr, modo, n):
    """cor do vídeo inteiro: 'cinema' (pele suave, contraste, sombras frias, luzes quentes, vinheta e grão leves)
    ou 'arquivo' (dessaturado, quente, grão mais forte): o tom documental"""
    if modo not in ('cinema', 'arquivo'): return fr
    if modo not in COR_LUT:
        if modo == 'cinema':
            curva = lambda v, ganho, desl: max(0, min(255, int(((v / 255 - .5) * 1.12 + .5 + desl) * 255 * ganho)))
            lut = [curva(v, 1.0, .0 - .03 * (1 - v / 255)) for v in range(256)] + [curva(v, 1.0, .005) for v in range(256)] + [curva(v, 1.0, .03 * (1 - v / 255) - .02 * v / 255) for v in range(256)]
            sat, vin, gr = .9, .30, 5
        else:
            lut = [min(255, int(v * .96 + 14)) for v in range(256)] + [min(255, int(v * .93 + 8)) for v in range(256)] + [min(255, int(v * .82 + 4)) for v in range(256)]
            sat, vin, gr = .55, .42, 12
        m = Image.new('L', (W // 8, H // 8), 0); ImageDraw.Draw(m).ellipse([-W // 16, -H // 32, W // 8 + W // 16, H // 8 + H // 32], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BICUBIC).point(lambda v: int(255 - (255 - v) * vin))
        rnd = __import__('random').Random(7); grao = Image.frombytes('L', (W // 2, H // 2), bytes(rnd.randrange(256) for _ in range(W * H // 4))).resize((W, H))
        COR_LUT[modo] = (lut, sat, m, grao, gr)
    lut, sat, vin, grao, gr = COR_LUT[modo]
    from PIL import ImageEnhance, ImageChops
    fr = ImageEnhance.Color(fr.point(lut)).enhance(sat)
    fr = ImageChops.multiply(fr, Image.merge('RGB', [vin] * 3))
    n //= 3                                        # o grão troca a cada 3 quadros: leve na tela e no tamanho do arquivo
    g = grao.rotate(0, translate=((n * 37) % 160 - 80, (n * 53) % 160 - 80)).point(lambda v: int(128 + (v - 128) * gr / 128))
    return ImageChops.add(fr, Image.merge('RGB', [g] * 3), 1, -128)
COR_LUT = {}

def moldura(fr, C):
    """moldura fina da família Revista (estilo.moldura): fio na cor de destaque a 40 px da borda"""
    d = ImageDraw.Draw(fr); d.rectangle([40, 40, W - 41, H - 41], outline=C['destaque'], width=3)

CELULAR_INSERTS = {'duascamadas': cel_titulo, 'rotulos': cel_rotulos, 'chamada': cel_chamada, 'cta': cel_chamada,
                   'carimbo': cel_carimbo, 'perfil': cel_perfil}

def ins_print(fr, t, ins, L, C):
    """Print: imagem real (tela, publicação, página), acima da cabeça. No celular, corte cru sem moldura e sem movimento;
    nas outras famílias, cantos arredondados, sombra suave e entrada curta.
    campos: imagem (em midia/), largura (padrão 620), alturaMax (padrão 560), x, y, fonte"""
    a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
    cel = familia(ins, C) == 'celular'
    al, ent = (seco(t, a, b), 1.0) if cel else janela(t, a, b, .3)
    if al <= 0: return
    arq = os.path.join(CTX['pasta'], ins.get('imagem', '')); larg = ins.get('largura', 620)
    k = (arq, larg, cel)
    if k not in FAIXA_CACHE:
        im = Image.open(arq).convert('RGBA'); im = im.resize((larg, round(im.height * larg / im.width)), Image.BICUBIC)
        im = im.crop((0, 0, im.width, min(im.height, ins.get('alturaMax', 560))))   # print alto: fica a parte de cima
        if not cel:
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=28, fill=255); im.putalpha(m)
            sb = Image.new('RGBA', (im.width + 80, im.height + 80), (0, 0, 0, 0)); ImageDraw.Draw(sb).rounded_rectangle([40, 52, im.width + 40, im.height + 52], radius=30, fill=(0, 0, 0, 120))
            sb = sb.filter(ImageFilter.GaussianBlur(18)); sb.alpha_composite(im, (40, 40)); im = sb
        FAIXA_CACHE[k] = im
    im = FAIXA_CACHE[k]
    x = ins.get('x', 90 - (0 if cel else 40)); y = ins.get('y', topo_txt(C) - (0 if cel else 40))
    if not cel:
        im = im.rotate(-2 * (1 - ent) - 1.2, resample=Image.BICUBIC, expand=True); y += (1 - ent) * 50
    colar(fr, im, x, y, al)

FAMILIA_INSERTS = {'duascamadas': fam_titulo, 'rotulos': fam_rotulos, 'chamada': fam_chamada, 'cta': fam_chamada,
                   'carimbo': fam_carimbo, 'perfil': fam_perfil}

def por_familia(tipo, institucional):
    def desenhar(fr, t, ins, L, C):
        fam = familia(ins, C)
        if fam == 'atras' and tipo in ATRAS_TIPOS and RECORTE.disponivel(): return atras_frente(fr, t, ins, L, C)
        if fam == 'celular' and tipo in CELULAR_INSERTS: return CELULAR_INSERTS[tipo](fr, t, ins, L, C)
        if fam != 'institucional' and tipo in FAMILIA_INSERTS: return FAMILIA_INSERTS[tipo](fr, t, ins, L, C)
        return institucional(fr, t, ins, L, C)
    return desenhar

class Recorte:
    """recorte da pessoa: no macOS, o Vision da Apple (recortar.swift, compilado uma vez e aberto como serviço);
    sem ele (Windows, Mac sem as ferramentas da Apple), o modelo aberto de recortar.py. MJ_RECORTE=onnx força o segundo."""
    def __init__(self): self.proc = None; self.onnx = None; self.ok = None
    def disponivel(self):
        if self.ok is None:
            self.ok = False
            if platform.system() == 'Darwin' and os.environ.get('MJ_RECORTE') != 'onnx':
                fonte = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recortar.swift')
                bin_ = os.path.join(tempfile.gettempdir(), 'mj-recortar-' + hashlib.sha1(open(fonte, 'rb').read()).hexdigest()[:8])
                try:
                    if not os.path.exists(bin_):           # compila num nome próprio e troca: trechos em paralelo não disputam o arquivo
                        tmp_bin = f'{bin_}-{os.getpid()}'
                        subprocess.run(['swiftc', '-O', fonte, '-o', tmp_bin], check=True, capture_output=True); os.replace(tmp_bin, bin_)
                    self.proc = subprocess.Popen([bin_, '--servico'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
                    self.ok = True
                except Exception:
                    pass
            if not self.ok:
                try:
                    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                    from recortar import RecorteOnnx
                    self.onnx = RecorteOnnx(); self.ok = True
                except Exception as e:
                    print(f'AVISO recorte da pessoa indisponível ({e.__class__.__name__}): "atrás de você" sai como editorial; rode o instalador', flush=True)
        return self.ok
    def mascara(self, fr):
        """a máscara fica guardada em <pasta_mesa>/_recorte, pela imagem do quadro: zona, quadros e vídeo (e cada nova
        montagem depois da Mesa) reaproveitam o recorte em vez de refazer"""
        arq = None
        if CTX.get('pasta') not in (None, '.'):
            arq = os.path.join(CTX['pasta'], '_recorte', hashlib.blake2b(fr.tobytes(), digest_size=12).hexdigest() + '.png')
            if os.path.exists(arq):
                try:
                    m = Image.open(arq); m.load(); return m
                except Exception: pass
        m = self._calcular(fr)
        if m is not None and arq:
            os.makedirs(os.path.dirname(arq), exist_ok=True); tmp = f'{arq}.{os.getpid()}'
            m.save(tmp, 'PNG', compress_level=1); os.replace(tmp, arq)
        return m
    def _calcular(self, fr):
        if self.onnx: return self.onnx.mascara(fr)
        d = tempfile.gettempdir(); ent = os.path.join(d, f'mj-q-{os.getpid()}.png'); sai = os.path.join(d, f'mj-m-{os.getpid()}.png')
        fr.save(ent, compress_level=1)
        self.proc.stdin.write(f'{ent}\t{sai}\n'); self.proc.stdin.flush()
        r = self.proc.stdout.readline().strip()
        if r != 'ok': return None
        return Image.open(sai).convert('L').filter(ImageFilter.GaussianBlur(1.5))
RECORTE = Recorte()

INSERTS_INST = {'carimbo': ins_carimbo, 'fluxo': ins_fluxo, 'bilhete': ins_bilhete, 'duascamadas': ins_duascamadas, 'tarja': ins_tarja, 'rotulos': ins_rotulos, 'formula': ins_formula,
           'chamada': ins_chamada, 'perfil': ins_perfil, 'cartao': ins_cartao, 'cta': ins_chamada, 'mitofato': ins_mitofato, 'print': ins_print, 'fixo': ins_fixo, 'cartaz': ins_cartaz}
INSERTS = {k: por_familia(k, f) for k, f in INSERTS_INST.items()}

def ativo_base(P, L, t):
    for i in P.get('inserts', []):
        if i.get('ativo') and (i['tipo'] in ZONA_BASE or i.get('ocultaLegenda')) and L.mc(i['inicio']) - 0.05 <= t <= L.mc(i['fim'], depois=False) + 0.2:
            return True
    return False

# ---------- legenda ----------
CORR_PADRAO = {'cloud': 'Claude', 'Cloud': 'Claude', 'clóude': 'Claude'}

def montar_legenda(P, L):
    corr = dict(CORR_PADRAO, **P.get('estilo', {}).get('correcoes', {}))
    ws = []
    for w in P['palavras']:
        mid = (w['s'] + w['e']) / 2
        if L.m(mid) is None: continue
        txt = w['t']
        base = re.sub(r'[^\wÀ-ú%]', '', txt)
        if base in corr: txt = txt.replace(base, corr[base])
        s = L.m(w['s']); e = L.m(w['e'])
        ws.append({'t': txt, 's': s if s is not None else L.m(mid) - 0.1, 'e': e if e is not None else L.m(mid) + 0.1})
    blocos, cur = [], []
    for w in ws:
        if cur and (len(cur) >= 4 or cur[-1]['t'][-1] in '.,?!' or w['s'] - cur[-1]['e'] > 0.4):
            blocos.append(cur); cur = []
        cur.append(w)
    if cur: blocos.append(cur)
    out = []
    for i, c in enumerate(blocos):
        ini = c[0]['s'] - 0.05
        fim = min(blocos[i + 1][0]['s'] - 0.05, c[-1]['e'] + 0.5) if i + 1 < len(blocos) else c[-1]['e'] + 0.6
        out.append((ini, fim, c))
    return out

def desenhar_legenda(fr, t, LEG, P, C, y_base=None):
    est = P.get('estilo', {}); modo = est.get('legenda', 'nenhuma')
    if modo == 'nenhuma': return
    dest = {x.lower() for x in est.get('destaques', [])}
    for ini, fim, c in LEG:
        if not (ini <= t <= fim): continue
        fam = C['familia']
        if fam == 'celular':          # uma palavra por vez, troca seca, letra forte com contorno
            w = [x for x in c if x['s'] - 0.03 <= t][-1:] or c[:1]
            p_ = w[0]['t'].rstrip('.,')
            k = re.sub(r'[^\wÀ-ú]', '', p_).lower() in dest and modo != 'discreta'
            f = caber('heavy', 84 if modo == 'palavra-grande' else 68, p_, 800)
            Lg = Image.new('RGBA', (W, 200), (0, 0, 0, 0))
            ImageDraw.Draw(Lg).text((W / 2, 100), p_, font=f, fill=(C['destaque'] if k else WHITE) + (255,), anchor='mm', stroke_width=7, stroke_fill=(0, 0, 0, 255))
            colar(fr, Lg, 0, (y_base or y_legenda_do(est)) - 130, 1.0)
            return
        atual = ([i for i, x in enumerate(c) if x['s'] - 0.03 <= t][-1:] or [0])[0]
        if modo == 'palavra': c = [c[atual]]; atual = 0          # uma palavra por vez, na letra da família
        pal = [w['t'].rstrip('.,') for w in c]
        if fam == 'atras': pal = [x.upper() for x in pal]
        chave = [re.sub(r'[^\wÀ-ú]', '', p).lower() in dest for p in pal]
        # cada família tem a sua letra de legenda: condensada (editorial, atrás de você), serifa itálica (revista)
        base_f, forte_f, tam = {'editorial': ('cond', 'cond', 76), 'atras': ('cond', 'cond', 68),
                                'revista': ('serifa', 'demi', 72)}.get(fam, ('demi', 'heavy', 54))   # legenda: New York itálica (traço mais firme que a Didot)
        grande = 1.55 if modo == 'palavra-grande' else 1.0
        if fam == 'revista':      # na revista o destaque vira versalete, sem aumentar
            pal = [x.upper() if k and modo != 'discreta' else x for x, k in zip(pal, chave)]
        def fontes(tam):
            if fam == 'revista': return [font(forte_f, int(tam * .8)) if (k and modo != 'discreta') else font(base_f, tam) for k in chave]
            return [font(forte_f, int(tam * (1.35 if fam != 'institucional' else grande))) if (k and grande > 1) else font(base_f, tam) for k in chave]
        fs = fontes(tam); esp = font(base_f, tam).getlength(' ')
        larg = sum(f.getlength(p) for f, p in zip(fs, pal)) + esp * (len(pal) - 1)
        if larg > 770:                 # até 770 de largura (com a sombra e a itálica): a legenda não encosta na coluna de botões da rede
            tam = int(tam * 770 / larg); fs = fontes(tam); esp = font(base_f, tam).getlength(' ')
            larg = sum(f.getlength(p) for f, p in zip(fs, pal)) + esp * (len(pal) - 1)
        Lh = 220; Lg = Image.new('RGBA', (W, Lh), (0, 0, 0, 0)); d = ImageDraw.Draw(Lg)
        x = (W - larg) / 2; yb = 150
        for i_, (f, p, k) in enumerate(zip(fs, pal, chave)):
            cor = C['destaque'] if (k and modo in ('destaque', 'palavra-grande', 'palavra') and fam not in ('atras', 'revista')) else WHITE
            if modo == 'acende': cor = C['destaque'] if i_ == atual else (200, 200, 200)      # a palavra dita acende
            if est.get('contornoLegenda'):      # roupa clara atrás da legenda: contorno escuro fino
                d.text((x, yb), p, font=f, fill=cor + (255,), anchor='ls', stroke_width=max(3, f.size // 18), stroke_fill=(18, 18, 20, 255))
            else: d.text((x, yb), p, font=f, fill=cor + (255,), anchor='ls')
            x += f.getlength(p) + esp
        sombra = Image.new('RGBA', (W, Lh), (0, 0, 0, 0))
        sombra.putalpha(Lg.split()[3].point(lambda v: int(v * (.95 if fam == 'revista' else .85))).filter(ImageFilter.GaussianBlur(10 if fam == 'revista' else 7)))
        p = eo(pr(t, ini, ini + 0.12))
        y0 = (y_base or y_legenda_do(est)) - yb + (1 - p) * 12      # estilo.yLegenda: altura da legenda neste vídeo (logo abaixo do queixo)
        if fam == 'revista':
            perto = Image.new('RGBA', (W, Lh), (0, 0, 0, 0)); perto.putalpha(Lg.split()[3].filter(ImageFilter.GaussianBlur(3)))
            colar(fr, perto, 0, y0 + 2, .9)
        colar(fr, sombra, 0, y0 + 3, 1.0); colar(fr, Lg, 0, y0, p)
        return

# ---------- camada animada (modelos HTML de assets/animacoes, gravados por animar.js) ----------
ANIMAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'animar.js')
ANIM = {}   # id do insert -> {'a': entrada editada, 'area': {...}, 'quadros': [arquivos]}

FERRAMENTAS = os.environ.get('MJ_FERRAMENTAS') or os.path.join(os.path.expanduser('~'), '.marketing-juridico', 'ferramentas')

def ferramenta(chave, padrao=None):
    """caminho gravado pelo instalador em <ferramentas>/caminhos.json (node, ffmpeg, python, node_path, chrome)"""
    try: return json.load(open(os.path.join(FERRAMENTAS, 'caminhos.json'), encoding='utf-8')).get(chave) or padrao
    except Exception: return padrao

def pasta_node(ff):
    """node_modules com puppeteer-core e three: NODE_PATH, a pasta do instalador ou a pasta onde está o ffmpeg-static"""
    if os.environ.get('NODE_PATH'): return os.environ['NODE_PATH']
    if ferramenta('node_path'): return ferramenta('node_path')
    p = os.path.abspath(ff)
    while p != os.path.dirname(p):
        if os.path.basename(p) == 'node_modules': return p
        p = os.path.dirname(p)
    sys.exit('defina NODE_PATH com a pasta node_modules onde estão puppeteer-core e three')

def gravar_animacoes(P, L, pasta, ff):
    """grava cada insert 'animacao' (com cache) e deixa a prévia transparente para a Mesa (anim-<id>.webm)"""
    ANIM.clear(); previas = {}
    for ins in P.get('inserts', []):
        if ins.get('tipo') != 'animacao' or not ins.get('ativo'): continue
        a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
        dados = dict(ins.get('dados', {}), fim=round(b - a, 3), marcas=[round(L.mc(x) - a, 3) for x in ins.get('marcas', [])],
                     pastaMidia=os.path.abspath(pasta), familia=familia(ins, cores(P)), cores={k: '#%02X%02X%02X' % v for k, v in cores(P).items() if k in ('fundo', 'destaque', 'acao', 'ok', 'alerta', 'gigante')},
                     **fontes_para_modelo())
        dados = dados_anuncio(ins['modelo'], dados, cores(P))
        dur = b - a + 0.45
        # modelo sob encomenda (.html) fica na pasta da Mesa: o caminho certo é que faz a gravação refazer quando ele muda
        arq_modelo = os.path.join(os.path.abspath(pasta), ins['modelo']) if ins['modelo'].endswith('.html') else os.path.join(ASSETS, 'animacoes', ins['modelo'] + '.html')
        versao = ''.join(hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8] for f in (arq_modelo, os.path.join(ASSETS, 'animacoes', 'base.js')) if os.path.exists(f))
        chave = hashlib.sha1(json.dumps([ins['modelo'], dados, round(dur, 3), versao], sort_keys=True).encode()).hexdigest()[:10]   # modelo mudou: grava de novo
        dest = os.path.join(pasta, '_anim', f"{ins['id']}-{chave}")
        if not os.path.exists(os.path.join(dest, 'area.json')):
            os.makedirs(dest, exist_ok=True)
            arq = os.path.join(dest, 'dados.json'); json.dump(dados, open(arq, 'w'), ensure_ascii=False)
            env = dict(os.environ, NODE_PATH=pasta_node(ff))
            modelo = ins['modelo'] if not ins['modelo'].endswith('.html') else os.path.join(os.path.abspath(pasta), ins['modelo'])
            subprocess.run([ferramenta('node', 'node'), ANIMAR, modelo, arq, dest, str(dur), str(FPS)], check=True, env=env)
            webm = os.path.join(pasta, f"anim-{ins['id']}.webm")
            subprocess.run([ff, '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(dest, 'quadro_%05d.png'),
                            '-vf', 'scale=trunc(iw/4)*2:trunc(ih/4)*2', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
                            '-b:v', '0', '-crf', '36', '-auto-alt-ref', '0', '-deadline', 'realtime', '-cpu-used', '8', '-row-mt', '1', webm], check=True)   # só a prévia da Mesa: rápido vale mais que a qualidade
        quadros = sorted(f for f in os.listdir(dest) if f.startswith('quadro_'))
        area = json.load(open(os.path.join(dest, 'area.json')))
        ANIM[ins['id']] = {'a': a, 'area': area, 'quadros': [os.path.join(dest, f) for f in quadros]}
        previas[ins['id']] = {'arquivo': f"anim-{ins['id']}.webm", 'area': area, 'chave': chave}
    if not os.environ.get('MJ_TRECHO'): open(os.path.join(pasta, 'animacoes.js'), 'w').write('window.ANIMACOES = ' + json.dumps(previas) + ';\n')

def colar_animacoes(fr, tn):
    for an in ANIM.values():
        k = int(round((tn - an['a']) * FPS))
        if 0 <= k < len(an['quadros']):
            q = Image.open(an['quadros'][k]).convert('RGBA')
            fr.paste(q.convert('RGB'), (an['area']['x'], an['area']['y']), q)

# ---------- quadro ----------
def zoom(fr, z, cy=0.33):
    if abs(z - 1) < 0.002: return fr
    cw, ch = W / z, H / z
    x0 = (W - cw) / 2; y0 = (H - ch) * cy
    return fr.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)

def dividida(cru, tn, e, P, L, LEG, C):
    """Tela dividida: em cima o quadro cru (como saiu da câmera), embaixo o mesmo instante editado.
    efeito: {tipo: 'dividida', inicio, fim, marcas: [acende_cima, acende_baixo], corte: y da faixa, rotulos: [cima, baixo]}"""
    a, b = L.mc(e['inicio']), L.mc(e['fim'], depois=False)
    y0 = e.get('corte', 260); hh = H // 2
    ed = processar(cru.copy(), tn, P, L, LEG, C, sem_dividida=True, y_legenda=y0 + hh - 60)
    k = eo(pr(tn, a, a + 0.35)) * (1 - eo(pr(tn, b - 0.3, b)))
    if k <= 0.001: return ed
    mk = [L.mc(x) for x in e.get('marcas', [])]
    luz_c = luz_b = 1.0                      # antes da primeira marca, as duas metades acesas
    if len(mk) >= 2 and tn >= mk[0]:
        luz_c, luz_b = (1.0, 0.5) if tn < mk[1] else (0.5, 1.0)
    cima = cru.crop((0, y0, W, y0 + hh)); baixo = ed.crop((0, y0, W, y0 + hh))
    if luz_c < 1: cima = Image.blend(Image.new('RGB', cima.size), cima, luz_c)
    if luz_b < 1: baixo = Image.blend(Image.new('RGB', baixo.size), baixo, luz_b)
    comp = Image.new('RGB', (W, H)); comp.paste(cima, (0, 0)); comp.paste(baixo, (0, hh))
    d = ImageDraw.Draw(comp); d.rectangle([0, hh - 4, W, hh + 4], fill=C['destaque'])
    rot = e.get('rotulos', ['O QUE EU GRAVEI', 'O QUE O CLAUDE DEVOLVEU']); f = font('heavy', 38)
    if C['familia'] != 'institucional':          # sem pílula: versalete com fio, como o resto da família
        for txt, y, luz in [(rot[0], 200, luz_c), (rot[1], hh + 36, luz_b)]:
            bloco(comp, [dict(x=70, y=y, txt=txt.upper(), f=font('demi', 34), cor=C['texto'], track=6)], .55 + .45 * luz, .7, 8)
            ImageDraw.Draw(comp).rectangle([72, y + 52, 72 + 110, y + 57], fill=C['destaque'] if luz >= 1 else (150, 150, 150))
        return comp if k >= 0.999 else Image.blend(ed, comp, k)
    for txt, y, luz in [(rot[0], 230, luz_c), (rot[1], hh + 40, luz_b)]:
        tw = f.getlength(txt) + 48
        Lr = cartao(tw, 70, WHITE if luz >= 1 else C['fundo'], 245, 35)
        ImageDraw.Draw(Lr).text((tw / 2, 37), txt, font=f, fill=(C['fundo'] if luz >= 1 else WHITE) + (255,), anchor='mm')
        colar(comp, Lr, 60, y, 1.0)
    return comp if k >= 0.999 else Image.blend(ed, comp, k)

# ---------- faixa de imagem em cima, advogado embaixo (pauta quente, tutorial, página oficial grifada) ----------
FAIXA_CACHE = {}
CTX = {'pasta': '.', 'ff': 'ffmpeg'}   # pasta da Mesa e ffmpeg do comando em curso

def cobrir(img, w, h, cy=0.5):
    """redimensiona para cobrir w x h e recorta; cy escolhe a altura do recorte (0 topo, 1 base)"""
    s = max(w / img.width, h / img.height); img = img.resize((max(w, round(img.width * s)), max(h, round(img.height * s))), Image.BICUBIC)
    x0 = (img.width - w) // 2; y0 = int((img.height - h) * cy)
    return img.crop((x0, y0, x0 + w, y0 + h)), s, x0, y0

def faixa_midia(e, pasta, ff, alt):
    """quadros da mídia da faixa: imagem fixa, vídeo (extraído uma vez) ou captura de página (.json de capturar_pagina.js)"""
    arq = os.path.join(pasta, e['midia']); k = (arq, alt)
    if k in FAIXA_CACHE: return FAIXA_CACHE[k]
    ext = os.path.splitext(arq)[1].lower(); res = {'tipo': 'imagem'}
    if ext == '.json':                    # página com trecho grifado: imagem + retângulos do trecho
        cap = json.load(open(arq, encoding='utf-8'))
        img = Image.open(os.path.join(os.path.dirname(arq), cap['imagem'])).convert('RGB')
        rects = [r for g in cap['grifos'] for r in g['retangulos']]
        cy = 0.5
        if rects:                         # centra o recorte no trecho grifado
            s = W / img.width; meio = (min(r['y'] for r in rects) + max(r['y'] + r['h'] for r in rects)) / 2 * s
            cy = clamp((meio - alt * .45) / max(1, img.height * s - alt))
        im, s, x0, y0 = cobrir(img, W, alt, cy)
        res = {'tipo': 'captura', 'img': im, 'cap': cap,
               'grifos': [[(r['x'] * s - x0, r['y'] * s - y0, r['w'] * s, r['h'] * s) for r in g['retangulos']] for g in cap['grifos']]}
    elif ext in ('.mp4', '.mov', '.m4v', '.webm'):
        dest = os.path.join(pasta, '_faixa', hashlib.sha1(f"{arq}{alt}{e.get('inicioMidia', 0)}".encode()).hexdigest()[:10])
        if not os.path.exists(os.path.join(dest, 'ok')):
            os.makedirs(dest, exist_ok=True)
            subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', str(e.get('inicioMidia', 0)), '-i', arq, '-an', '-t', '60',
                            '-vf', f'fps={FPS},scale={W}:{alt}:force_original_aspect_ratio=increase,crop={W}:{alt}', '-q:v', '3',
                            os.path.join(dest, 'f_%05d.jpg')], check=True)
            open(os.path.join(dest, 'ok'), 'w').write('ok')
        res = {'tipo': 'video', 'quadros': sorted(os.path.join(dest, f) for f in os.listdir(dest) if f.startswith('f_'))}
    else:
        res['img'] = cobrir(Image.open(arq).convert('RGB'), W, alt, e.get('cy', 0.5))[0]
    FAIXA_CACHE[k] = res; return res

def faixa_ativa(P, L, tn):
    for e in P.get('efeitos', []):
        if e.get('ativo', True) and e['tipo'] == 'faixa' and L.mc(e['inicio']) <= tn <= L.mc(e['fim'], depois=False): return e
    return None

def faixa_fundo(fr, tn, e, L, C, pasta, ff):
    """monta a faixa: mídia em cima (y 0 a altura), advogado descido para baixo dela"""
    alt = e.get('altura', 760); desce = e.get('desce', alt - 460); a = L.mc(e['inicio'])
    M = faixa_midia(e, pasta, ff, alt)
    comp = Image.new('RGB', (W, H), C['fundo'])
    comp.paste(fr.crop((0, 0, W, H - desce)), (0, desce))
    if M['tipo'] == 'video':
        q = M['quadros']; im = Image.open(q[min(len(q) - 1, int((tn - a) * FPS))]).convert('RGB')
    else:
        im = M['img'].copy()
    if M['tipo'] == 'captura':            # marca-texto passa pelo trecho, linha a linha, na marca da fala
        mk = [L.mc(x) for x in e.get('marcas', [])] or [a + 0.6]
        mt = tuple(int(v + (255 - v) * .35) for v in C['destaque'])
        camada = Image.new('RGB', im.size, (255, 255, 255)); d = ImageDraw.Draw(camada)
        for gi, ret in enumerate(M['grifos']):
            t0 = mk[min(gi, len(mk) - 1)]; total = sum(r[2] for r in ret) or 1; feito = eo(pr(tn, t0, t0 + 0.4 + 0.25 * len(ret))) * total
            for x, y, w, h in ret:
                if feito <= 0: break
                d.rectangle([x - 4, y + h * .12, x + min(w, feito) + 4, y + h * .98], fill=mt); feito -= w
        from PIL import ImageChops
        im = ImageChops.multiply(im, camada)
    comp.paste(im, (0, 0))
    ImageDraw.Draw(comp).rectangle([0, alt - 3, W, alt + 3], fill=C['destaque'])
    return comp

def faixa_texto(fr, tn, e, L, C, pasta):
    """etiqueta (ARQUIVO 2014, ILUSTRAÇÃO, nome do site), crédito e manchete opcional"""
    alt = e.get('altura', 760); a = L.mc(e['inicio']); p = eo(pr(tn, a, a + .35))
    M = FAIXA_CACHE.get((os.path.join(pasta, e['midia']), alt), {})
    etiqueta = e.get('etiqueta') or (M.get('cap', {}).get('site', '') if M.get('tipo') == 'captura' else '')
    credito = e.get('credito') or (f"{M['cap']['site']} · acesso em {M['cap']['acesso']}" if M.get('tipo') == 'captura' else '')
    if etiqueta:
        f = font('demi', 30); tw = sum(f.getlength(c) + 4 for c in etiqueta.upper())
        Lt = Image.new('RGBA', (int(tw) + 36, 54), (17, 17, 17, 225)); d = ImageDraw.Draw(Lt); x = 18
        for c in etiqueta.upper(): d.text((x, 28), c, font=f, fill=(255, 255, 255, 255), anchor='lm'); x += f.getlength(c) + 4
        colar(fr, Lt, 92, 236, p)
    if credito:
        f = font('med', 24); tw = f.getlength(credito)
        Lc = Image.new('RGBA', (int(tw) + 24, 38), (0, 0, 0, 150)); ImageDraw.Draw(Lc).text((12, 19), credito, font=f, fill=(255, 255, 255, 235), anchor='lm')
        colar(fr, Lc, 988 - Lc.width, alt + 14, p)
    if e.get('titulo'):                   # manchete no pé da faixa
        f = caber('heavy', 58, e['titulo'], 880); lin = quebrar(e['titulo'], f, 880)[:2]; hh = len(lin) * 70 + 40
        Lm = Image.new('RGBA', (W, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(Lm)
        d.rectangle([0, 0, W, hh], fill=C['fundo'] + (235,))
        for i, ln in enumerate(lin): d.text((96, 24 + i * 70), ' '.join(ln), font=f, fill=WHITE + (255,))
        colar(fr, Lm, 0, alt - hh - 60 + (1 - p) * 30, p)

# ---------- edição acontecendo na tela: o vídeo mostra a própria montagem enquanto a pessoa fala ----------
def edicao_ao_vivo(fr, tn, e, P, L, LEG, C):
    """painel com o tempo, quatro trilhas (vídeo, texto, animação, áudio) que se preenchem conforme cada corte,
    título e legenda entram, contadores e o aviso do último item colocado.
    efeito: {tipo: 'edicaoaovivo', inicio, fim, posicao: 'alto' | 'baixo', y, escala, janela: segundos visíveis (padrão 8)}"""
    a, b = L.mc(e['inicio']), L.mc(e['fim'], depois=False)
    al, ent = janela(tn, a, b, .3)
    if al <= 0: return
    J = e.get('janela', 8.0); w, h = 900, 300; x0, x1 = 150, w - 34
    t_esq = tn - .75 * J
    X = lambda u: x0 + (u - t_esq) / J * (x1 - x0)
    Lp = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(Lp)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=24, fill=(14, 18, 24, 210))
    fm = font('mono', 28); fl = font('demi', 27)
    pisca = (int(tn * 2) % 2) == 0
    d.ellipse([28, 26, 44, 42], fill=C['alerta'] + (255 if pisca else 120,))
    d.text((56, 34), 'O CLAUDE ESTÁ EDITANDO', font=fl, fill=(230, 234, 240, 255), anchor='lm')
    q = int(round(tn * FPS)); d.text((w - 30, 34), f'{q // FPS // 60:02d}:{q // FPS % 60:02d}:{q % FPS:02d}', font=fm, fill=(141, 152, 168, 255), anchor='rm')
    trilhas = ['VÍDEO', 'TEXTO', 'ANIMAÇÃO', 'ÁUDIO']; ys = [76 + i * 44 for i in range(4)]
    for nome, y in zip(trilhas, ys):
        d.text((28, y + 15), nome, font=font('demi', 21), fill=(141, 152, 168, 255), anchor='lm')
        d.rectangle([x0, y, x1, y + 30], fill=(27, 35, 48, 255))
    lim = lambda u: max(x0, min(x1, u))
    def bloco_(y, s, f_, cor, alto=30, top=0):
        if s > tn: return
        xa, xb = lim(X(s)), lim(X(min(f_, tn)))
        if xb - xa >= 2: d.rounded_rectangle([xa, y + top, xb, y + top + alto], radius=5, fill=cor + (255,))
    cortes = 0
    for k, ((sa, sb), o) in enumerate(zip(L.seg, L.off)):          # vídeo: trechos mantidos, corte em vermelho
        bloco_(ys[0], o, o + sb - sa, (74, 111, 240) if k % 2 else (96, 132, 245))
        if k and o <= tn:
            cortes += 1; xc = X(o)
            if x0 <= xc <= x1: d.rectangle([xc - 2, ys[0] - 4, xc + 2, ys[0] + 34], fill=C['alerta'] + (255,))
    ultimo = None; graficos = 0
    for i in P.get('inserts', []):
        if not i.get('ativo'): continue
        s, f_ = L.mc(i['inicio']), L.mc(i['fim'], depois=False)
        anim = i['tipo'] == 'animacao'
        bloco_(ys[2] if anim else ys[1], s, f_, C['acao'] if anim else C['destaque'], 30 if anim else 16)
        if s <= tn:
            graficos += 1
            if tn - s < 1.4 and (ultimo is None or s > ultimo[0]):
                ultimo = (s, ('animação' if anim else NOME_CURTO.get(i['tipo'], 'título')), (i.get('dados') or {}).get('palavra') or i.get('titulo') or i.get('mito') or ', '.join(i.get('itens', [])[:2]))
    for x in P.get('efeitos', []):
        if x.get('ativo', True) and x['tipo'] in ('faixa', 'dividida', 'aproximacao', 'pb'):
            bloco_(ys[2], L.mc(x['inicio']), L.mc(x['fim'], depois=False), C['ok'], 30)
    legs = 0
    for ini, fim, c in LEG:                                          # legendas: tirinhas brancas embaixo da trilha de texto
        bloco_(ys[1], ini, fim, (230, 234, 240), 10, 20)
        if ini <= tn:
            legs += 1
            if tn - ini < .6 and ultimo is None: ultimo = (ini, 'legenda', ' '.join(w['t'] for w in c))
    pp = P.get('picos', []); passo = P.get('passoPicos', .05); u = max(a, t_esq)
    while u <= tn:                                                   # áudio: a onda do que já foi montado
        o_ = L.orig(u); v = pp[min(len(pp) - 1, int(o_ / passo))] if pp else .3; xx = X(u)
        if x0 <= xx <= x1: d.rectangle([xx, ys[3] + 15 - 13 * v, xx + 3, ys[3] + 15 + 13 * v], fill=(76, 195, 138, 255))
        u += .1
    xp = X(tn); d.rectangle([xp - 1, 62, xp + 1, ys[3] + 36], fill=(255, 255, 255, 255))   # agulha
    d.text((28, h - 26), f'{cortes} cortes · {legs} legendas · {graficos} gráficos', font=font('med', 25), fill=(201, 209, 222, 255), anchor='lm')
    if ultimo:
        txt = f'+ {ultimo[1]} “{ultimo[2][:22]}”'
        d.text((w - 30, h - 26), txt, font=font('demi', 25), fill=C['destaque'] + (255,), anchor='rm')
    y = e.get('y') or (topo_txt(C) if e.get('posicao', 'alto') == 'alto' else 1180)      # y: altura própria (anúncio: abaixo de 270)
    if e.get('escala'): Lp = Lp.resize((int(Lp.width * e['escala']), int(Lp.height * e['escala'])), Image.LANCZOS); w = Lp.width      # escala: painel menor, acima da cabeça
    colar(fr, Lp, (W - w) / 2, y + (1 - ent) * (-24 if e.get('posicao', 'alto') == 'alto' else 24), al)

NOME_CURTO = {'duascamadas': 'título', 'carimbo': 'frase', 'rotulos': 'rótulos', 'chamada': 'chamada', 'perfil': 'identificação',
              'mitofato': 'mito e fato', 'print': 'print', 'formula': 'fórmula', 'tarja': 'tarja', 'bilhete': 'convite', 'cartao': 'cartão', 'fluxo': 'fluxo'}

# ---------- holofote e transições (agem sobre o quadro inteiro) ----------
def holofote(fr, tn, e, L, C):
    """tudo escurece menos a pessoa: frase séria, revelação. Sem recorte disponível, vinheta no rosto.
    efeito: {tipo: 'holofote', inicio, fim, forca (0,3 a 0,8; padrão 0,6)}"""
    a, b = L.mc(e['inicio']), L.mc(e['fim'], depois=False)
    k = eo(pr(tn, a, a + 0.5)) * (1 - eo(pr(tn, b - 0.4, b))) * e.get('forca', 0.6)
    if k <= 0.01: return fr
    escuro = Image.blend(fr, Image.new('RGB', fr.size, (0, 0, 0)), k)
    m = RECORTE.mascara(fr) if RECORTE.disponivel() else None
    if m is None:                                    # vinheta: claro no rosto, escuro nas bordas
        m = Image.new('L', (W // 8, H // 8), 0); ImageDraw.Draw(m).ellipse([W // 8 * .18, H // 8 * .14, W // 8 * .82, H // 8 * .62], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BICUBIC)
    escuro.paste(fr, (0, 0), m); return escuro

def transicao(fr, tn, e, L, C):
    """troca de cena no corte: modo 'cor' (faixa de cor atravessa a tela), 'iris' (círculo fecha e abre)
    ou 'card' (o vídeo encolhe para um cartão e volta). efeito: {tipo: 'transicao', modo, inicio, fim} em volta do corte
    (cerca de 0,6 s; o ponto da troca é o meio, ou 'em' se informado)"""
    a, b = L.mc(e['inicio']), L.mc(e['fim'], depois=False); em = L.mc(e['em']) if 'em' in e else (a + b) / 2
    if not (a <= tn <= b): return fr
    modo = e.get('modo', 'cor'); cor = C['destaque'] if modo == 'cor' else C['fundo']
    if modo == 'cor':
        if tn < em: x0, x1 = 0, int(W * eio(pr(tn, a, em)))           # cobre da esquerda para a direita
        else: x0, x1 = int(W * eio(pr(tn, em, b))), W                  # descobre no mesmo sentido
        out = fr.copy(); ImageDraw.Draw(out).rectangle([x0, 0, x1, H], fill=cor); return out
    if modo == 'iris':
        r = math.hypot(W, H) / 2 * (1 - eio(pr(tn, a, em)) if tn < em else eio(pr(tn, em, b)))
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([W / 2 - r, H * .4 - r, W / 2 + r, H * .4 + r], fill=255)
        out = Image.new('RGB', (W, H), cor); out.paste(fr, (0, 0), m); return out
    if modo == 'card':
        p = eio(pr(tn, a, em)) if tn < em else 1 - eio(pr(tn, em, b))
        s = 1 - 0.24 * p; w, h = int(W * s), int(H * s)
        peq = fr.resize((w, h), Image.BICUBIC).rotate(-3 * p, resample=Image.BICUBIC, expand=True, fillcolor=cor)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(60 * p) + 1, fill=255)
        m = m.rotate(-3 * p, resample=Image.BICUBIC, expand=True)
        out = Image.new('RGB', (W, H), cor); out.paste(peq, ((W - peq.width) // 2, (H - peq.height) // 2), m); return out
    return fr

def eio(t):
    t = clamp(t); return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2

def processar(fr, tn, P, L, LEG, C, sem_dividida=False, y_legenda=None, base=None):
    """base: lista que recebe o quadro antes dos textos e gráficos (usada pelo verificador de zona segura)"""
    est = P.get('estilo', {})
    if not sem_dividida:
        for e in P.get('efeitos', []):
            if e.get('ativo', True) and e['tipo'] == 'dividida' and L.mc(e['inicio']) <= tn <= L.mc(e['fim'], depois=False):
                return dividida(fr, tn, e, P, L, LEG, C)
    z = 1.0 + (est.get('zoomAlternado', 0.05) if L.indice(tn) % 2 else 0.0)
    pb = False
    for e in P.get('efeitos', []):
        if not e.get('ativo', True): continue
        a, b = L.mc(e['inicio']), L.mc(e['fim'], depois=False)
        if not (a <= tn <= b): continue
        if e['tipo'] == 'aproximacao':
            z *= 1 + (e.get('forca', 1.15) - 1) * eo(pr(tn, a, a + 0.15))
        elif e['tipo'] == 'pb':
            pb = True
    fr = zoom(fr, z)
    if est.get('cor'): fr = aplicar_cor(fr, est['cor'], int(round(tn * FPS)))
    if pb: fr = Image.merge('RGB', [fr.convert('L').point(lambda v: int(min(255, max(0, (v - 128) * 1.12 + 128))))] * 3)
    for e in P.get('efeitos', []):
        if e.get('ativo', True) and e['tipo'] == 'holofote' and L.mc(e['inicio']) <= tn <= L.mc(e['fim'], depois=False): fr = holofote(fr, tn, e, L, C)
    fx = faixa_ativa(P, L, tn)
    if fx:
        fr = faixa_fundo(fr, tn, fx, L, C, CTX['pasta'], CTX['ff'])
        y_legenda = y_legenda or fx.get('yLegenda', 1495)
    atras = [] if fx else [i for i in P.get('inserts', []) if i.get('ativo') and i['tipo'] in ATRAS_TIPOS and familia(i, C) == 'atras'
             and L.mc(i['inicio']) - .05 <= tn <= L.mc(i['fim'], depois=False) + .35]
    if atras and RECORTE.disponivel():
        m = RECORTE.mascara(fr)
        if m is not None:                  # palavra gigante atrás, pessoa colada por cima
            pessoa = fr.copy()
            for i in atras: atras_fundo(fr, tn, i, L, C)
            fr.paste(pessoa, (0, 0), m)
    if est.get('moldura'): moldura(fr, C)              # decoração: fica no fundo, fora da conferência de zona segura
    if base is not None: base.append(fr.copy())
    for i in P.get('inserts', []):
        if i.get('ativo') and i['tipo'] in INSERTS: INSERTS[i['tipo']](fr, tn, i, L, C)
    colar_animacoes(fr, tn)
    if fx: faixa_texto(fr, tn, fx, L, C, CTX['pasta'])
    for e in P.get('efeitos', []):
        if e.get('ativo', True) and e['tipo'] == 'edicaoaovivo': edicao_ao_vivo(fr, tn, e, P, L, LEG, C)
    if y_legenda is None:              # insert com yLegenda: a legenda muda de altura só enquanto ele está na tela (ex.: peça nas mãos)
        y_legenda = next((i['yLegenda'] for i in P.get('inserts', []) if i.get('ativo') and i.get('yLegenda')
                          and L.mc(i['inicio']) - .05 <= tn <= L.mc(i['fim'], depois=False) + .2), None)
    if not ativo_base(P, L, tn) and not (fx and fx.get('legenda') is False): desenhar_legenda(fr, tn, LEG, P, C, y_legenda)
    for e in P.get('efeitos', []):
        if e.get('ativo', True) and e['tipo'] == 'transicao': fr = transicao(fr, tn, e, L, C)
    return fr

# ---------- cores do vídeo (identidade adaptada ao cenário) ----------
def paleta_do_video(ff, original, cor, n=8):
    """tira a paleta do cenário (sem a pessoa) e devolve cores de texto que combinam com o vídeo"""
    hh, mm, ss = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([ff, '-i', original], capture_output=True, text=True).stderr).groups()
    dur = int(hh) * 3600 + int(mm) * 60 + float(ss)
    amostra = []; tmp = os.path.join(tempfile.gettempdir(), f'mj-pal-{os.getpid()}.png')
    for k in range(n):
        t = dur * (k + .5) / n
        subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', original, '-frames:v', '1', '-vf', cor, tmp], check=True)
        fr = Image.open(tmp).convert('RGB').resize((W, H))
        m = RECORTE.mascara(fr) if RECORTE.disponivel() else None
        peq = fr.resize((108, 192)); mp = m.resize((108, 192)) if m is not None else None
        for i, px in enumerate(peq.getdata()):
            if mp is None or mp.getdata()[i] < 60: amostra.append(px)
    img = Image.new('RGB', (len(amostra), 1)); img.putdata(amostra)
    q = img.quantize(12, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:36]
    contagem = sorted(q.getcolors(), reverse=True)
    cores_ = [(cnt, tuple(pal[i * 3:i * 3 + 3])) for cnt, i in contagem]
    def hls(c): return colorsys.rgb_to_hls(*[v / 255 for v in c])
    def rgb(h, l, s_): return tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(h, l, s_))
    # destaque: a cor mais presente com saturação de verdade, clareada para ler sobre o vídeo
    viva = max(cores_, key=lambda x: x[0] * max(0, hls(x[1])[2] - .15)) [1]
    h, l, s_ = hls(viva)
    destaque = rgb(h, .72, min(max(s_, .45), .72))
    gigante = rgb(h, .91, min(s_, .30))            # tom claro do cenário para a palavra gigante
    fundo = rgb(h, .14, min(s_, .35))              # escuro do mesmo tom (cartões, painéis)
    hexa = lambda c: '#%02X%02X%02X' % c
    return {'destaque': hexa(destaque), 'gigante': hexa(gigante), 'fundo': hexa(fundo), 'texto': '#FFFFFF',
            'origem': [hexa(c) for _, c in cores_[:6]]}

def pares_fontes():
    arq = os.path.join(ASSETS, 'animacoes', 'fontes.js')
    r = subprocess.run([ferramenta('node', 'node'), '-e', 'global.window={};require(process.argv[1]);console.log(JSON.stringify({b:window.FONTES_BASE,p:window.PARES_FONTES}))', arq],
                       capture_output=True, text=True, encoding='utf-8')
    return json.loads(r.stdout) if r.returncode == 0 else {'b': '', 'p': []}

PAR_ATIVO = {}
def aplicar_fontes(P):
    """estilo.fontes = id de um par de assets/animacoes/fontes.js: baixa os arquivos uma vez e passa a usá-los"""
    from urllib.request import urlretrieve
    from urllib.parse import quote
    FONTES_PAR.clear(); _fc.clear(); PAR_ATIVO.clear()
    pid = P.get('estilo', {}).get('fontes')
    if not pid: return
    d = pares_fontes(); par = next((x for x in d['p'] if x['id'] == pid), None)
    if not par: print('AVISO par de fontes desconhecido:', pid); return
    pasta = os.path.join(FERRAMENTAS, 'fontes'); os.makedirs(pasta, exist_ok=True)
    loc = {}
    for papel in ('titulo', 'texto', 'serifa'):
        f = par.get(papel)
        if not f: continue
        dest = os.path.join(pasta, os.path.basename(f['arquivo']))
        if not os.path.exists(dest):
            try: urlretrieve(d['b'] + quote(f['arquivo']), dest)
            except Exception as e: print('AVISO não consegui baixar a fonte', f['familia'], e); continue
        loc[papel] = (dest, f.get('peso', 400)); PAR_ATIVO[papel] = dict(f, local=dest)
    if 'titulo' in loc:
        for t in ('heavy', 'cond'): FONTES_PAR[t] = loc['titulo']
    ser = loc.get('serifa') or loc.get('titulo')
    if ser:
        for t in ('didoti', 'serifa', 'serif'): FONTES_PAR[t] = ser
    if 'texto' in loc:
        FONTES_PAR['demi'] = (loc['texto'][0], max(loc['texto'][1], 600)); FONTES_PAR['med'] = loc['texto']; FONTES_PAR['bold'] = (loc['texto'][0], 700)
    PAR_ATIVO['google'] = par.get('google', '')

def fontes_para_modelo():
    """o par de fontes ativo no formato dos modelos animados (DADOS.fontes, arquivosFontes e googleFontes)"""
    if not PAR_ATIVO: return {}
    pilha = lambda f: f'"{f["familia"]}", "Avenir Next", "Segoe UI", sans-serif'
    fontes = {k: pilha(PAR_ATIVO[k]) for k in ('titulo', 'texto', 'serifa') if k in PAR_ATIVO}
    if 'serifa' not in fontes and 'titulo' in fontes: fontes['serifa'] = fontes['titulo']
    arqs = [{'familia': f['familia'], 'url': '/fontes/' + os.path.basename(f['local']), 'peso': f.get('peso', 400), 'estilo': 'italic' if f.get('italico') else 'normal'}
            for k, f in PAR_ATIVO.items() if k != 'google']
    return {'fontes': fontes, 'arquivosFontes': arqs, 'googleFontes': 'https://fonts.googleapis.com/css2?' + PAR_ATIVO['google'] + '&display=swap' if PAR_ATIVO.get('google') else ''}

def garantir_paleta(P, pasta, ff, original):
    aplicar_fontes(P)
    est = P.setdefault('estilo', {})
    if est.get('cores') == 'video' and not est.get('coresVideo'):
        est['coresVideo'] = paleta_do_video(ff, *fonte_video(ff, original, pasta))
        gravar_projeto(pasta, P)
        print('paleta do vídeo:', est['coresVideo'], flush=True)

# ---------- áudio ----------
def montar_audio(ff, original, L, trab):
    bruto = os.path.join(trab, 'audio48.wav')
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', original, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s16le', bruto], check=True)
    w = wave.open(bruto); sr = w.getframerate(); ch = w.getnchannels()
    data = array.array('h', w.readframes(w.getnframes())); w.close()
    out = array.array('h'); fade = int(0.012 * sr)
    for a, b in L.seg:
        fa = math.ceil(a * FPS - 1e-6); fb = math.floor(b * FPS + 1e-6)
        ia, ib = round(fa / FPS * sr), round((fb + 1) / FPS * sr)
        seg = data[ia * ch:ib * ch]; n = len(seg) // ch
        for i in range(min(fade, n)):
            g = i / fade
            for c in range(ch):
                seg[i * ch + c] = int(seg[i * ch + c] * g)
                j = (n - 1 - i) * ch + c; seg[j] = int(seg[j] * g)
        out.extend(seg)
    saida = os.path.join(trab, 'audio-editado.wav')
    wo = wave.open(saida, 'wb'); wo.setnchannels(ch); wo.setsampwidth(2); wo.setframerate(sr); wo.writeframes(out.tobytes()); wo.close()
    return saida

# ---------- comandos ----------
def preparar(ff, original, transc, pasta, nome=None):
    os.makedirs(pasta, exist_ok=True)
    ov, cor = fonte_video(ff, original, pasta)
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', ov, '-i', original, '-map', '0:v:0', '-map', '1:a:0?', '-vf', cor + ',scale=540:960', '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '27', '-g', '15', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', os.path.join(pasta, 'proxy.mp4')], check=True)
    wav = os.path.join(pasta, '_audio16k.wav')
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', original, '-ac', '1', '-ar', '16000', wav], check=True)
    w = wave.open(wav); sr = w.getframerate(); data = array.array('h', w.readframes(w.getnframes())); w.close(); os.remove(wav)
    dur = len(data) / sr; passo = int(sr * 0.05); picos = []
    for i in range(0, len(data), passo):
        s = data[i:i + passo]; picos.append(math.sqrt(sum(x * x for x in s) / max(1, len(s))))
    mx = max(picos) or 1; picos = [round(min(1, (p / mx) ** 0.7), 3) for p in picos]
    palavras = []
    for s in json.load(open(transc, encoding='utf-8')):
        for wd in s['words']:
            t = wd['w'].strip()
            if not t: continue
            if palavras and (t == '%' or t.startswith('-')):
                palavras[-1]['t'] += t; palavras[-1]['e'] = round(wd['e'], 2); continue
            palavras.append({'t': t, 's': round(wd['s'], 2), 'e': round(wd['e'], 2)})
            if 'p' in wd: palavras[-1]['p'] = round(wd['p'], 2)
    avisos = [f"palavra '{p['t']}' dura {p['e'] - p['s']:.1f} s em {p['s']:.1f} s: transcreva esse trecho de novo"
              for p in palavras if p['e'] - p['s'] > 1.2]
    # cortes automáticos: antes da primeira palavra, pausas acima de 0,3 s e depois da última palavra
    cortes = []; MA, MD = 0.10, 0.08
    if palavras and palavras[0]['s'] - MA > 0.05: cortes.append([0.0, round(palavras[0]['s'] - MA, 2)])
    for x, y in zip(palavras, palavras[1:]):
        if y['s'] - x['e'] > 0.30: cortes.append([round(x['e'] + MD, 2), round(y['s'] - MA, 2)])
    if palavras and dur - palavras[-1]['e'] > 0.15:
        # porta na cara: o vídeo acaba logo depois do fim do som da última palavra (medido no áudio, não na transcrição)
        jan = int(sr * 0.01); ult = palavras[-1]
        rms = lambda k: math.sqrt(sum(x * x for x in data[k:k + jan]) / max(1, len(data[k:k + jan])))
        janelas = [rms(k) for k in range(int(ult['s'] * sr), int(ult['e'] * sr), jan)] or [1]
        limiar = 0.25 * sorted(janelas)[len(janelas) // 2]       # um quarto da energia típica da última palavra (acima do ruído da sala)
        fim_som, baixos = ult['e'], 0
        for k in range(int((ult['e'] - 0.08) * sr), min(len(data), int((ult['e'] + 0.6) * sr)), jan):
            if rms(k) > limiar: fim_som, baixos = k / sr + 0.01, 0
            else:
                baixos += 1
                if baixos >= 8: break                              # 80 ms abaixo: a palavra acabou
        cortes.append([round(min(dur - 0.02, fim_som + 0.06), 2), round(dur, 2)])
    arq = os.path.join(pasta, 'projeto.js')
    P = ler_projeto(pasta) if os.path.exists(arq) else {}
    P.update({'video': 'proxy.mp4', 'duracao': round(dur, 2), 'picos': picos, 'passoPicos': 0.05, 'palavras': palavras})
    P.setdefault('id', re.sub(r'[^a-z0-9]+', '-', (nome or os.path.basename(original)).lower()).strip('-'))
    P.setdefault('nome', nome or os.path.basename(original))
    P.setdefault('velocidade', 1.1); P.setdefault('cortes', cortes)
    P.setdefault('inserts', []); P.setdefault('efeitos', []); P.setdefault('notas', [])
    P.setdefault('estilo', {'receita': '', 'familia': 'editorial', 'legenda': 'destaque', 'destaques': [], 'zoomAlternado': 0.05})
    gravar_projeto(pasta, P)
    print('ok', len(palavras), 'palavras', len(P['cortes']), 'cortes', round(dur, 2), 's')
    for a in avisos: print('AVISO', a)

def decodificar(ff, original, L, cor, cada=1, pecas=None):
    """quadros do vídeo editado; a cor (o HDR do iPhone) só é convertida nos trechos que ficam.
    cada > 1 entrega só um quadro a cada `cada` (o verificador de zona não precisa dos outros).
    pecas: só esses pedaços do original (um trecho da montagem em paralelo); o vídeo é aberto perto do primeiro,
    com os tempos do original preservados, e a grade de quadros é a mesma da leitura inteira."""
    seg = pecas or L.seg
    sel = '+'.join(f'between(t\\,{a:.3f}\\,{b:.3f})' for a, b in seg)
    pulo = f"select='not(mod(n\\,{cada}))',setpts=N/{FPS}/TB," if cada > 1 else ''
    busca = ['-ss', f'{max(0.0, seg[0][0] - 2):.3f}', '-copyts'] if pecas and seg[0][0] > 3 else []
    return subprocess.Popen([ff, '-loglevel', 'error', *busca, '-i', original, '-an', '-vf',
                             f"fps={FPS},select='{sel}',setpts=N/{FPS}/TB,{pulo}{cor},scale=in_color_matrix=bt709:in_range=tv,format=rgb24",
                             '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)

def quadros(ff, original, pasta, saida, tempos):
    CTX.update(pasta=pasta, ff=ff)
    P = ler_projeto(pasta); garantir_paleta(P, pasta, ff, original); L = Linha(P); LEG = montar_legenda(P, L); C = cores(P); ov, cor = fonte_video(ff, original, pasta)
    os.makedirs(saida, exist_ok=True); tmp = os.path.join(saida, '_q.png')
    gravar_animacoes(P, L, pasta, ff)
    feitos = []
    for to in tempos:
        tn = L.m(to)
        if tn is None: print('cortado', to); continue
        subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', str(to), '-i', ov, '-frames:v', '1', '-vf', cor, tmp], check=True)
        fr = Image.open(tmp).convert('RGB').resize((W, H))
        q = processar(fr, tn, P, L, LEG, C); q.save(os.path.join(saida, f'q_{to:06.2f}.jpg'), quality=88)
        feitos.append((to, q.resize((W // 3, H // 3), Image.BILINEAR)))
    if os.path.exists(tmp): os.remove(tmp)
    for f in folhas_de_contato(feitos, saida): print('folha', f)

def folhas_de_contato(feitos, saida, por_folha=9):
    """9 quadros numa imagem só (3 x 3, com o tempo do original): o Claude confere a folha e só abre o quadro
    grande do trecho com problema. Uma folha pesa no plano o mesmo que um quadro."""
    for velho in os.listdir(saida):
        if velho.startswith('folha_'): os.remove(os.path.join(saida, velho))
    lw, lh = W // 3, H // 3; nomes = []
    for i in range(0, len(feitos), por_folha):
        grupo = feitos[i:i + por_folha]; linhas = (len(grupo) + 2) // 3
        folha = Image.new('RGB', (W, lh * linhas), (0, 0, 0)); d = ImageDraw.Draw(folha); f = font('bold', 30)
        for j, (to, mini) in enumerate(grupo):
            x, y = (j % 3) * lw, (j // 3) * lh
            folha.paste(mini, (x, y)); d.rectangle([x, y, x + lw - 1, y + lh - 1], outline=(0, 0, 0), width=3)
            rot = f'{to:.1f} s'; tw = d.textlength(rot, font=f)
            d.rectangle([x + 8, y + 8, x + 24 + tw, y + 52], fill=(0, 0, 0)); d.text((x + 16, y + 12), rot, font=f, fill=(255, 220, 0))
        nome = os.path.join(saida, f'folha_{i // por_folha + 1:02d}.jpg'); folha.save(nome, quality=85); nomes.append(nome)
    return nomes

def grade(L):
    """os quadros que o decodificador entrega, por trecho mantido: (a, b, k0, k1), com k0..k1 os índices da grade
    de 1/FPS dentro de [a, b] (a mesma conta do ffmpeg: t = k * (1/FPS) contra os limites escritos com 3 casas)"""
    passo = 1.0 / FPS; out = []
    for a, b in L.seg:
        a3, b3 = float(f'{a:.3f}'), float(f'{b:.3f}')
        k0 = max(0, math.floor(a3 * FPS) - 1)
        while k0 * passo < a3: k0 += 1
        k1 = math.ceil(b3 * FPS) + 1
        while k1 * passo > b3: k1 -= 1
        if k1 >= k0: out.append((a3, b3, k0, k1))
    return out

def pecas_do_intervalo(g, lo, hi):
    """os pedaços do original que dão os quadros lo..hi (índices do vídeo editado, antes da velocidade).
    O corte cai no meio de dois quadros da grade, longe do arredondamento de 3 casas."""
    pecas = []; base = 0
    for a3, b3, k0, k1 in g:
        cnt = k1 - k0 + 1; s_, e_ = max(lo, base), min(hi, base + cnt - 1)
        if s_ <= e_:
            ks, ke = k0 + s_ - base, k0 + e_ - base
            pecas.append((a3 if ks == k0 else (ks - 0.5) / FPS, b3 if ke == k1 else (ke + 0.5) / FPS))
        base += cnt
    return pecas

def trechos(L, n, vel=1.0):
    """divide o vídeo final em n trechos do mesmo tamanho. A velocidade entra aqui: o quadro j do vídeo final mostra o
    quadro round(j * vel) do editado, e os que sairiam na aceleração nem são desenhados."""
    g = grade(L); total = sum(k1 - k0 + 1 for *_, k0, k1 in g)
    saida = max(1, int((total - 1) / vel) + 1)                       # quadros do vídeo final
    fonte = lambda j: min(total - 1, int(round(j * vel)))
    alvo = [round(saida * k / n) for k in range(n + 1)]; res = []
    for k in range(n):
        j0, j1 = alvo[k], alvo[k + 1] - 1
        if j1 < j0: continue
        lo, hi = fonte(j0), fonte(j1)
        res.append({'n0': lo, 'quadros': hi - lo + 1, 'pecas': pecas_do_intervalo(g, lo, hi), 'mostrar': [fonte(j) for j in range(j0, j1 + 1)]})
    return res, total, saida

def preparar_montagem(ff, original, pasta):
    CTX.update(pasta=pasta, ff=ff)
    P = ler_projeto(pasta); garantir_paleta(P, pasta, ff, original); L = Linha(P); LEG = montar_legenda(P, L); C = cores(P)
    ov, cor = fonte_video(ff, original, pasta)
    return P, L, LEG, C, ov, cor, float(P.get('velocidade', 1.0))

def cor_saida():
    return ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']

def codificador(ff, saida, extra=()):
    """o vídeo final: 1080 x 1920, H.264 (até 12 Mbps), 30 quadros por segundo, cor BT.709; recebe os quadros prontos já na velocidade final"""
    return subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *extra,
                             '-vf', 'scale=out_color_matrix=bt709:out_range=tv', *cor_saida(), '-c:v', 'libx264', '-preset', os.environ.get('MJ_PRESET', 'medium'),
                             '-crf', '18', '-maxrate', '12M', '-bufsize', '24M', '-pix_fmt', 'yuv420p', saida], stdin=subprocess.PIPE)

def processos_paralelos(quadros_total):
    """quantos trechos montar ao mesmo tempo: MJ_PARALELO manda; sem ele, os núcleos menos 2 (até 6), e 1 GB de memória por trecho"""
    if os.environ.get('MJ_PARALELO'): return max(1, int(os.environ['MJ_PARALELO']))
    if quadros_total < 300: return 1                       # menos de 10 s: não compensa
    n = min(6, max(1, (os.cpu_count() or 2) - 2))
    try: n = min(n, max(1, int(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 2 ** 30) - 2))
    except (ValueError, OSError, AttributeError): n = min(n, 2)   # Windows: sem a conta da memória, 2 de cada vez
    return n

def video(ff, original, pasta, saida):
    P, L, LEG, C, ov, cor, vel = preparar_montagem(ff, original, pasta)
    trab = os.path.join(os.path.dirname(os.path.abspath(saida)), '_trabalho'); os.makedirs(trab, exist_ok=True)
    aud = montar_audio(ff, original, L, trab)
    gravar_animacoes(P, L, pasta, ff)
    _, total, _ = trechos(L, 1, vel)
    partes, total, n_final = trechos(L, processos_paralelos(total), vel)
    mp4s = [os.path.join(trab, f'trecho-{k:02d}.mp4') for k in range(len(partes))]
    if len(partes) > 1:
        print(f'montando em {len(partes)} trechos ao mesmo tempo ({n_final} quadros)', flush=True)
        procs = []
        for k, t in enumerate(partes):
            arq_t = os.path.join(trab, f'trecho-{k:02d}.json'); json.dump(t, open(arq_t, 'w'))
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), '_trecho', ff, original, pasta, arq_t, mp4s[k]],
                                          env=dict(os.environ, MJ_TRECHO='1')))
        falhou = [k for k, pr in enumerate(procs) if pr.wait() != 0]
        if falhou: sys.exit(f'trecho(s) {falhou} falharam; rode de novo com MJ_PARALELO=1 para montar de uma vez')
    else:
        montar_trecho(ff, ov, cor, partes[0], mp4s[0], P, L, LEG, C, mostrar=True)
    lista = os.path.join(trab, 'trechos.txt')
    open(lista, 'w', encoding='utf-8').write(''.join(f"file '{m}'\n" for m in mp4s))
    af = (f'atempo={vel},' if abs(vel - 1) > 0.001 else '') + 'loudnorm=I=-14:TP=-1.5:LRA=11'
    subprocess.run([ff, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-i', aud, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', af, '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', saida], check=True)
    for f in os.listdir(trab): os.remove(os.path.join(trab, f))
    os.rmdir(trab)
    print('quadros', n_final, 'duração final', round(L.total / vel, 2), 's')

def montar_trecho(ff, ov, cor, t, saida, P, L, LEG, C, mostrar=False):
    """desenha os quadros do trecho que aparecem no vídeo final (na velocidade escolhida) e grava já na qualidade final"""
    dec = decodificar(ff, ov, L, cor, pecas=t['pecas']); enc = codificador(ff, saida)
    tam = W * H * 3; n = t['n0'] - 1; pronto = None; feitos = 0
    for alvo in t['mostrar']:
        while n < alvo:
            buf = dec.stdout.read(tam)
            if len(buf) < tam: break
            n += 1; pronto = None
            if n == alvo: pronto = processar(Image.frombytes('RGB', (W, H), buf), n / FPS, P, L, LEG, C).tobytes()
        if pronto is None: break                           # o original acabou antes do previsto
        enc.stdin.write(pronto); feitos += 1                # câmera lenta: o mesmo quadro sai de novo
        if mostrar and feitos % 300 == 0: print('quadro', feitos, flush=True)
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.wait()
    if feitos != len(t['mostrar']): print(f"AVISO {os.path.basename(saida)}: {feitos} quadros, esperados {len(t['mostrar'])}", flush=True)

def video_trecho(ff, original, pasta, arq_trecho, saida):
    """um trecho da montagem em paralelo (processo próprio)"""
    t = json.load(open(arq_trecho))
    P, L, LEG, C, ov, cor, vel = preparar_montagem(ff, original, pasta)
    gravar_animacoes(P, L, pasta, ff)
    t['pecas'] = [tuple(x) for x in t['pecas']]
    montar_trecho(ff, ov, cor, t, saida, P, L, LEG, C)

# ---------- zona segura: nada de texto atrás da interface da rede ----------
# organico: Reels, TikTok e Shorts; impulsionado: anúncio do Meta (14 % em cima, 35 % embaixo, 6 % nas laterais)
ZONAS = {'organico': {'x': (65, 1015), 'y': (220, 1520), 'botoes': (940, 1150)},
         'impulsionado': {'x': (65, 1015), 'y': (270, 1248), 'botoes': None}}

def mascara_proibida(perfil):
    z = ZONAS[perfil]; m = Image.new('L', (W, H), 255); d = ImageDraw.Draw(m)
    d.rectangle([z['x'][0], z['y'][0], z['x'][1], z['y'][1]], fill=0)
    if z['botoes']: d.rectangle([z['botoes'][0], z['botoes'][1], W, H], fill=255)   # coluna de curtir, comentar, enviar
    return m

def ativos_em(P, L, tn):
    nomes = [f"{i['id']} ({i['tipo']})" for i in P.get('inserts', []) if i.get('ativo') and L.mc(i['inicio']) - .05 <= tn <= L.mc(i['fim'], depois=False) + .3]
    return nomes or ['legenda']

def zona(ff, original, pasta, perfil='organico', passo=0.25):
    """percorre o vídeo editado e aponta todo texto ou gráfico fora da zona segura, com o quadro marcado"""
    CTX.update(pasta=pasta, ff=ff)
    from PIL import ImageChops
    P = ler_projeto(pasta); est = P.setdefault('estilo', {})
    if est.get('zona', 'organico') != perfil:        # o perfil conferido vale para o vídeo: no anúncio, os textos entram na zona dele
        est['zona'] = perfil; gravar_projeto(pasta, P)
        print('perfil gravado no projeto:', perfil, '(textos do alto, de baixo e legenda dentro da zona do anúncio)' if perfil == 'impulsionado' else '')
    garantir_paleta(P, pasta, ff, original); L = Linha(P); LEG = montar_legenda(P, L); C = cores(P)
    ov, cor = fonte_video(ff, original, pasta); gravar_animacoes(P, L, pasta, ff)
    proib = mascara_proibida(perfil); z = ZONAS[perfil]
    saida = os.path.join(pasta, '_zona'); os.makedirs(saida, exist_ok=True)
    for f in os.listdir(saida): os.remove(os.path.join(saida, f))
    cada = max(1, round(passo * FPS)); dec = decodificar(ff, ov, L, cor, cada); tam = W * H * 3; k = 0; faltas = []
    while True:
        buf = dec.stdout.read(tam)
        if len(buf) < tam: break
        n = k * cada; k += 1               # o decodificador já pula os quadros que não são conferidos
        cheia = any(an['area']['w'] >= W and an['area']['h'] >= H and 0 <= int(round((n / FPS - an['a']) * FPS)) < len(an['quadros']) for an in ANIM.values())
        cheia = cheia or any(e.get('ativo', True) and e['tipo'] == 'transicao' and L.mc(e['inicio']) <= n / FPS <= L.mc(e['fim'], depois=False) for e in P.get('efeitos', []))
        if not cheia:                        # animação de tela cheia (diagrama) é fundo: o modelo já põe o texto dentro da zona
            tn = n / FPS; base = []
            fim = processar(Image.frombytes('RGB', (W, H), buf), tn, P, L, LEG, C, base=base)
            if base:                         # quadros da tela dividida não passam por aqui (rótulos fixos)
                dif = ImageChops.difference(base[0], fim).convert('L').point(lambda v: 255 if v > 48 else 0)
                caixa = ImageChops.multiply(dif, proib).getbbox()
                if caixa:
                    quem = ativos_em(P, L, tn)
                    if faltas and faltas[-1]['quem'] == quem and tn - faltas[-1]['ate'] <= passo * 1.5:
                        faltas[-1]['ate'] = tn
                    else:
                        faltas.append({'de': tn, 'ate': tn, 'quem': quem, 'caixa': caixa})
                        q = fim.copy(); d = ImageDraw.Draw(q)
                        d.rectangle([z['x'][0], z['y'][0], z['x'][1], z['y'][1]], outline=(0, 220, 120), width=4)
                        if z['botoes']: d.rectangle([z['botoes'][0], z['botoes'][1], W - 1, H - 1], outline=(0, 220, 120), width=4)
                        d.rectangle(caixa, outline=(255, 40, 40), width=6)
                        q.resize((W // 2, H // 2)).save(os.path.join(saida, f'fora_{L.orig(tn):06.2f}.jpg'), quality=82)
    dec.stdout.close(); dec.wait()
    if not faltas:
        print(f'zona segura OK ({perfil})'); return
    print(f'{len(faltas)} trecho(s) fora da zona segura ({perfil}); quadros marcados em {saida}')
    for f in faltas:
        x0, y0, x1, y1 = f['caixa']
        print(f"  {L.orig(f['de']):6.2f} a {L.orig(f['ate']):6.2f} s (original) | {', '.join(f['quem'])} | área x {x0}-{x1}, y {y0}-{y1}")

# ---------- revisão da fala: hesitações, takes repetidos, palavra comida, emendas ----------
HESITA = re.compile(r'^(é{2,}|eh+|ã+h*|ah+n?|hum+|hm+|uh+m*|ahn|hã+|éh+)$')

def norma(t): return re.sub(r'[^\wÀ-ú]', '', t).lower()

def achados_fala(P):
    """lista de achados {tipo, corte, texto} a partir das palavras do projeto"""
    pw = P['palavras']; ach = []
    for i, w in enumerate(pw):
        n = norma(w['t'])
        antes = w['s'] - pw[i - 1]['e'] if i else 1.0
        depois = pw[i + 1]['s'] - w['e'] if i + 1 < len(pw) else 1.0
        # "é" só é hesitação quando arrasta, vem com reticências ou fica isolado entre pausas
        solto = n == 'é' and ('...' in w['t'] or w['e'] - w['s'] >= 0.45 or (antes > 0.25 and depois > 0.25))
        if HESITA.match(n) or solto:
            ach.append({'tipo': 'hesitação', 'corte': [round(w['s'] - 0.03, 2), round(w['e'] + 0.03, 2)], 'texto': w['t']})
    for x, y in zip(pw, pw[1:]):          # palavra dita duas vezes seguidas ("eu eu")
        if norma(x['t']) and norma(x['t']) == norma(y['t']) and y['s'] - x['e'] < 0.8:
            ach.append({'tipo': 'palavra repetida', 'corte': [round(x['s'] - 0.03, 2), round(y['s'] - 0.03, 2)], 'texto': f"{x['t']} {y['t']}"})
    nz = [norma(w['t']) for w in pw]; usado = set()
    for n in (7, 6, 5, 4, 3):              # take repetido: fica o último, sai o primeiro e o que veio entre eles
        for i in range(len(pw) - n):
            if i in usado or not all(nz[i:i + n]): continue
            for j in range(i + n, min(len(pw) - n + 1, i + 60)):
                if pw[j]['s'] - pw[i]['s'] > 15: break
                fecho = ''.join(w['t'][-1:] for w in pw[i:j])
                minimo = 5 if ('?' in fecho or '!' in fecho) else 4 if '.' in fecho else 3   # pergunta e resposta não é retake
                if n >= minimo and nz[j:j + n] == nz[i:i + n] and j not in usado:
                    ach.append({'tipo': 'take repetido', 'corte': [round(pw[i]['s'] - 0.05, 2), round(pw[j]['s'] - 0.05, 2)],
                                'texto': ' '.join(w['t'] for w in pw[i:j + n])})
                    usado.update(range(i, j + n)); break
    return sorted(ach, key=lambda a: a['corte'][0])

def revisar(pasta, ff=None, original=None, aplicar_=False):
    """aponta o que cortar na fala e prepara a escuta das emendas (os pontos onde dois trechos se juntam)"""
    P = ler_projeto(pasta); ach = achados_fala(P)
    cortes = sorted(P.get('cortes', []))
    dentro = lambda a, b: any(c0 - 0.02 <= a and b <= c1 + 0.02 for c0, c1 in cortes)
    novos = [a for a in ach if not dentro(*a['corte'])]
    print(f'{len(novos)} achado(s) na fala ({len(ach) - len(novos)} já cortados)')
    for a in novos: print(f"  {a['tipo']:<16} {a['corte'][0]:7.2f} a {a['corte'][1]:7.2f} s | {a['texto']}")
    for c0, c1 in cortes:                  # corte que começa ou termina no meio de uma palavra
        for w in P['palavras']:
            for borda in (c0, c1):
                if w['s'] + 0.04 < borda < w['e'] - 0.04:
                    print(f"  palavra comida   corte {c0:.2f} a {c1:.2f} s pega '{w['t']}' ({w['s']:.2f} a {w['e']:.2f} s)")
    if aplicar_ and novos:
        P['cortes'] = sorted(cortes + [a['corte'] for a in novos]); gravar_projeto(pasta, P)
        print('cortes acrescentados ao projeto:', len(novos))
    if not (ff and original): return
    L = Linha(P); trab = os.path.join(pasta, '_revisao'); os.makedirs(trab, exist_ok=True)
    aud = montar_audio(ff, original, L, trab)
    dentro_seg = lambda w, k: L.seg[k][0] <= (w['s'] + w['e']) / 2 <= L.seg[k][1]
    em = []
    for k in range(1, len(L.seg)):
        antes = [w['t'] for w in P['palavras'] if dentro_seg(w, k - 1)][-3:]
        depois = [w['t'] for w in P['palavras'] if dentro_seg(w, k)][:3]
        em.append({'n': k, 't': round(L.off[k], 2), 'corte': [round(L.seg[k - 1][1], 2), round(L.seg[k][0], 2)],
                   'esperado': ' '.join(antes) + ' | ' + ' '.join(depois)})
    json.dump({'audio': aud, 'emendas': em}, open(os.path.join(trab, 'emendas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(em)} emendas. Para ouvir cada uma (uma carga só do modelo):')
    print(f'  python transcrever.py "{aud}" --emendas "{os.path.join(trab, "emendas.json")}"')

# ---------- prancha do vídeo: a única página antes de montar ----------
# O advogado escolhe o ponto de partida (um formato do catálogo ou um favorito dele), ajusta o visual vendo o próprio
# quadro, pode pedir uma versão B em outro ponto de partida, escolhe a peça de cada momento e confirma os fatos.
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')

def url_arquivo(p):
    """endereço file:// de um caminho, certo também no Windows (C:\\... vira file:///C:/...)"""
    import pathlib
    return pathlib.Path(os.path.abspath(p)).as_uri()

def catalogo(memoria, saida, video=''):
    """grava a cópia do Catálogo que o advogado abre antes de cada edição: os arquivos continuam na pasta do plugin
    (a cópia aponta para lá), e entram os favoritos da memória e o caminho do vídeo"""
    M = ler_memoria(memoria)
    base = url_arquivo(os.path.join(ASSETS, 'catalogo')) + '/'
    html = open(os.path.join(ASSETS, 'catalogo', 'index.html'), encoding='utf-8').read()
    favs = [{'nome': f['nome'], 'formato': f.get('formato', ''), 'data': f.get('data', ''), 'visual': f.get('visual', {})} for f in M.get('favoritos', [])]
    extra = ('<script>window.FAVORITOS = ' + json.dumps(favs, ensure_ascii=False) + '; window.CATALOGO_VIDEO = '
             + json.dumps(video, ensure_ascii=False) + ';</script>\n')
    html = html.replace('<head>\n', f'<head>\n<base href="{base}">\n', 1)
    k = html.index('<script src=')
    html = html[:k] + extra + html[k:]
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    open(saida, 'w', encoding='utf-8').write(html)
    print('catálogo:', os.path.abspath(saida), '·', len(favs), 'favorito(s)', '· vídeo ' + video if video else '')

FAMILIAS_INFO = [('editorial', 'Editorial', 'Sem caixa, letra condensada, à esquerda. Ritmo, tutorial, pauta quente.'),
                 ('revista', 'Revista', 'Serifa itálica com fio. Opinião, institucional, temas sérios.'),
                 ('atras', 'Atrás de você', 'Uma palavra gigante atrás da pessoa no gancho e na frase principal.'),
                 ('celular', 'Celular', 'Cara de editado no aplicativo do celular: sem movimento, texto seco.'),
                 ('institucional', 'Institucional', 'Cartão com caixa, para quem prefere tudo emoldurado.')]
ALTURAS = {'alta': ('Mais alta', 1150), 'meio': ('No meio', LEG_Y), 'baixa': ('Mais baixa', 1460)}
RITMOS = {'seco': (0.15, 0.06, 0.05), 'respiro': (0.30, 0.10, 0.08), 'pausas': (0.80, 0.15, 0.12)}   # pausa mínima, folga antes e depois da palavra
DENSIDADE = {'poucas': 1, 'medias': 2, 'cheia': 3}
FONTES_DA_FAMILIA = {'editorial': ['condensada', 'impacto', 'moderna'], 'revista': ['revista', 'editorial', 'elegante'],
                     'atras': ['impacto', 'condensada', 'jornal'], 'celular': ['moderna', 'impacto', 'condensada'],
                     'institucional': ['classica', 'tradicao', 'tecnica']}

def ler_js(arq, chaves):
    """lê um arquivo de dados do plugin (window.X = ...) pelo node e devolve {chave: valor}"""
    cod = 'global.window={};require(process.argv[1]);console.log(JSON.stringify({' + ','.join(f'{k}:window.{k}' for k in chaves) + '}))'
    r = subprocess.run([ferramenta('node', 'node'), '-e', cod, arq], capture_output=True, text=True, encoding='utf-8')
    return json.loads(r.stdout) if r.returncode == 0 else {k: None for k in chaves}

def catalogo_pecas():
    """o catálogo único de peças (assets/animacoes/pecas.js), com o código de cada peça (P01, P02...)"""
    d = ler_js(os.path.join(ASSETS, 'animacoes', 'pecas.js'), ['PECAS', 'MOMENTOS'])
    pecas = d.get('PECAS') or []
    return {p['id']: dict(p, cod='P%02d' % (i + 1)) for i, p in enumerate(pecas)}, d.get('MOMENTOS') or {}

def catalogo_formatos():
    d = ler_js(os.path.join(ASSETS, 'catalogo', 'formatos.js'), ['FORMATOS', 'LEGENDAS', 'CORES_VIDEO'])
    fs = d.get('FORMATOS') or []
    return {f['id']: dict(f, cod='F%02d' % (i + 1)) for i, f in enumerate(fs)}, d.get('LEGENDAS') or [], d.get('CORES_VIDEO') or []

def ler_memoria(arq):
    try: M = json.load(open(arq, encoding='utf-8'))
    except Exception: M = {}
    for k, v in (('versao', 2), ('placar', {}), ('regras', []), ('historico', []), ('favoritos', []), ('partidas', {})): M.setdefault(k, v)
    return M

def visual_do_formato(f):
    """o visual que um formato traz quando vira ponto de partida"""
    return {'familia': f.get('familia', 'editorial'), 'legenda': f.get('legenda', 'destaque'), 'altura': 'meio',
            'cores': 'video', 'paleta': 'video', 'tom': f.get('cor', 'natural'), 'fontes': '', 'moldura': bool(f.get('moldura')),
            'densidade': f.get('densidade', 'medias'), 'ritmo': f.get('corte', 'respiro'), 'velocidade': f.get('velocidade', 1.1)}

def visual_do_projeto(P):
    est = P.get('estilo', {}); y = est.get('yLegenda') or LEG_Y
    altura = min(ALTURAS, key=lambda k: abs(ALTURAS[k][1] - y))
    return {'familia': est.get('familia', 'editorial'), 'legenda': est.get('legenda', 'destaque'), 'altura': altura,
            'cores': est.get('cores') or 'padrao', 'paleta': est.get('paleta') or ('video' if est.get('cores') == 'video' else ''),
            'tom': est.get('cor') or 'natural', 'fontes': est.get('fontes') or '', 'moldura': bool(est.get('moldura')),
            'densidade': est.get('densidade', 'medias'), 'ritmo': est.get('ritmo', 'respiro'), 'velocidade': P.get('velocidade', 1.1)}

def recortar_pausas(P, ritmo):
    """troca os cortes de pausa (os que ficam inteiros entre duas palavras) pelos do ritmo escolhido;
    cortes que tiram palavra (hesitação, take repetido) e os das pontas ficam como estão"""
    lim, MA, MD = RITMOS.get(ritmo, RITMOS['respiro'])
    pal = P.get('palavras', [])
    vaos = [(x['e'], y['s']) for x, y in zip(pal, pal[1:])]
    dentro = lambda c: any(a - 0.001 <= c[0] and c[1] <= b + 0.001 for a, b in vaos)
    manter = [c for c in P.get('cortes', []) if not dentro(c)]
    novos = [[round(a + MD, 2), round(b - MA, 2)] for a, b in vaos if b - a > lim and b - MA > a + MD]
    P['cortes'] = sorted(manter + novos)

def aplicar_visual(P, partida, v):
    """grava no projeto o ponto de partida e o visual escolhidos na prancha"""
    est = P.setdefault('estilo', {})
    est['receita'] = partida
    for k in ('familia', 'legenda', 'densidade', 'ritmo'):
        if v.get(k): est[k] = v[k]
    est['yLegenda'] = ALTURAS.get(v.get('altura'), ALTURAS['meio'])[1]
    if v.get('tom') and v['tom'] != 'natural': est['cor'] = v['tom']
    else: est.pop('cor', None)
    if v.get('moldura'): est['moldura'] = True
    else: est.pop('moldura', None)
    if v.get('fontes'): est['fontes'] = v['fontes']
    else: est.pop('fontes', None)
    c = v.get('cores')
    if c == 'video': est['cores'] = 'video'
    elif isinstance(c, dict): est['cores'] = c
    else: est.pop('cores', None)
    if v.get('paleta'): est['paleta'] = v['paleta']
    if v.get('velocidade'): P['velocidade'] = float(v['velocidade'])
    if v.get('ritmo'): recortar_pausas(P, v['ritmo'])

def peca_da_opcao(m, op, PECAS):
    """o insert ou efeito de uma opção: o que o Claude escreveu na opção, sobre o modelo do catálogo"""
    base = (PECAS.get(op.get('peca')) or {}).get('como', {})
    if 'efeito' in op or 'efeito' in base:
        e = dict(base.get('efeito', {}), **op.get('efeito', {}))
        e.setdefault('inicio', m['inicio']); e.setdefault('fim', m['fim']); e['ativo'] = True; return None, e
    ins = dict(base, **op.get('insert', {}))
    if 'dados' in base and 'dados' in op.get('insert', {}): ins['dados'] = dict(base['dados'], **op['insert']['dados'])
    ins.setdefault('inicio', m['inicio']); ins.setdefault('fim', m['fim']); ins['ativo'] = True
    for k in ('fonte', 'prova', 'naoProva', 'oab'):
        if op.get(k) and not ins.get(k): ins[k] = op[k]
    return ins, None

def prancha(ff, original, pasta, memoria=None, cor_marca=''):
    """grava prancha.html na pasta da Mesa. Precisa de P['prancha'] = {sugerido, porque, alternativas, chamada {rotulo, titulo}}
    e de P['momentos'] (cada um com nivel 1, 2 ou 3: aparece com poucas, médias ou sem trecho vazio)."""
    import copy, shutil
    CTX.update(pasta=pasta, ff=ff)
    P = ler_projeto(pasta); PR = P.get('prancha', {})
    PECAS, MOMENTOS = catalogo_pecas(); FORM, LEGENDAS, TONS = catalogo_formatos(); ov, cor = fonte_video(ff, original, pasta)
    MEM = ler_memoria(memoria) if memoria else ler_memoria('')
    plac = MEM.get('placar', {})
    est = P.setdefault('estilo', {})
    if not est.get('coresVideo'):
        est['coresVideo'] = paleta_do_video(ff, ov, cor); gravar_projeto(pasta, P)
    # pontos de partida: o sugerido pelo roteiro, as alternativas e os favoritos do advogado
    sug = PR.get('sugerido') if PR.get('sugerido') in FORM else 'pauta-quente'
    trava = est.get('travado')
    if trava:                                       # visual escolhido no Catálogo: prancha curta, só os momentos
        sug = est.get('receita') if est.get('receita') in FORM else sug
    partidas = []
    for i, fid in enumerate([] if trava else [sug] + [x for x in PR.get('alternativas', []) if x in FORM and x != sug][:2]):
        f = FORM[fid]
        partidas.append({'id': fid, 'tipo': 'formato', 'cod': f['cod'], 'nome': f['nome'], 'quando': f['quando'], 'sugerido': i == 0,
                         'porque': PR.get('porque', '') if i == 0 else '', 'estrutura': f.get('estrutura', []), 'visual': visual_do_formato(f)})
    favs = [] if trava else list(MEM.get('favoritos', []))
    if trava:
        nome = ('Seu favorito ' + trava['favorito']) if trava.get('favorito') else (FORM[est['receita']]['nome'] if est.get('receita') in FORM else 'Seu pedido')
        partidas.append({'id': 'pedido', 'tipo': 'pedido', 'cod': FORM.get(est.get('receita'), {}).get('cod', ''), 'nome': nome, 'formato': est.get('receita') or sug,
                         'quando': 'O visual que você escolheu no Catálogo.', 'sugerido': False, 'porque': '',
                         'estrutura': FORM.get(est.get('receita'), {}).get('estrutura', []), 'visual': visual_do_projeto(P)})
    antigo = {} if trava else (MEM.get('padrao') or {})
    if antigo.get('familia') and not favs:          # memória de antes da prancha: o padrão escolhido vira um favorito
        favs = [{'nome': 'Meu padrão', 'formato': sug, 'visual': dict(visual_do_formato(FORM[sug]), familia=antigo['familia'],
                 cores=antigo.get('cores') or 'video', paleta=antigo.get('paleta') or '', fontes=antigo.get('fontes') or '')}]
    for k, fv in enumerate(favs):
        partidas.append({'id': 'fav-' + (re.sub(r'[^a-z0-9]+', '-', fv['nome'].lower()).strip('-') or str(k + 1)), 'tipo': 'favorito', 'cod': '', 'nome': fv['nome'], 'formato': fv.get('formato', sug),
                         'quando': 'Seu favorito, guardado em ' + fv.get('data', '') if fv.get('data') else 'Seu favorito.',
                         'estrutura': FORM.get(fv.get('formato'), {}).get('estrutura', []), 'visual': fv['visual']})
    dest = os.path.join(pasta, 'prancha'); os.makedirs(dest, exist_ok=True)
    for velho in os.listdir(dest):
        if velho.endswith('.jpg'): os.remove(os.path.join(dest, velho))
    url = url_arquivo
    # o quadro de amostra: uma palavra dita no meio do trecho escolhido, fora dos cortes
    L = Linha(P); LEG = montar_legenda(P, L)
    alvo = PR.get('quadro') or (((P['momentos'][0]['inicio'] + P['momentos'][0]['fim']) / 2) if P.get('momentos') else P['duracao'] / 3)
    vivas = [w for w in P['palavras'] if L.m((w['s'] + w['e']) / 2) is not None]
    w0 = min(vivas, key=lambda w: abs((w['s'] + w['e']) / 2 - alvo)); t_am = (w0['s'] + w0['e']) / 2
    tmp = os.path.join(dest, '_q.png')
    def quadro(t):
        subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', ov, '-frames:v', '1', '-vf', cor, tmp], check=True)
        return Image.open(tmp).convert('RGB').resize((W, H))
    cru = quadro(t_am); tn = L.m(t_am)
    ch = PR.get('chamada') or {'rotulo': '', 'titulo': P.get('nome', '')}
    titulo = {'id': 'pr', 'tipo': 'duascamadas', 'rotulo': ch.get('rotulo', ''), 'titulo': ch.get('titulo', ''), 'marcas': [], 'ativo': True,
              'inicio': L.orig(max(0, tn - 2.5)), 'fim': L.orig(min(L.total - 0.01, tn + 2.5))}
    def desenhar(nome, v, com_titulo=True, legenda=None, fixo=False):
        tit = dict(titulo, familia=v['familia'], tipo='fixo') if fixo else dict(titulo, familia=v['familia'])
        P2 = copy.deepcopy(P); P2['inserts'] = [tit] if com_titulo else []; P2['efeitos'] = []
        aplicar_visual(P2, sug, dict(v, ritmo=None, velocidade=None)); aplicar_fontes(P2)
        if legenda: P2['estilo']['legenda'] = legenda
        processar(cru.copy(), tn, P2, L, LEG, cores(P2)).resize((540, 960), Image.LANCZOS).save(os.path.join(dest, nome), quality=84)
        return 'prancha/' + nome
    for p in partidas: p['imagem'] = desenhar(f"partida-{p['id']}.jpg", p['visual'], fixo='fixo' in FORM.get(p.get('formato', p['id']), {}).get('pecas', []))
    v0 = partidas[0]['visual']
    if trava:                                       # o visual já veio escolhido: sem as variações de família, legenda, altura e tom
        familias = [dict(id=f[0], nome=f[1], txt=f[2], imagem='') for f in FAMILIAS_INFO]
        legendas = [dict(l, imagem='') for l in LEGENDAS]
        alturas = [{'id': k, 'nome': n, 'y': y, 'imagem': ''} for k, (n, y) in ALTURAS.items()]
        tons = [dict(t, imagem='') for t in TONS]
    else:
        familias = [{'id': fid, 'nome': n, 'txt': t, 'imagem': desenhar(f'familia-{fid}.jpg', dict(v0, familia=fid))} for fid, n, t in FAMILIAS_INFO]
        legendas = [dict(l, imagem=desenhar(f"legenda-{l['id']}.jpg", v0, False, l['id'])) for l in LEGENDAS]
        alturas = [{'id': k, 'nome': n, 'y': y, 'imagem': desenhar(f'altura-{k}.jpg', dict(v0, altura=k), False)} for k, (n, y) in ALTURAS.items()]
        tons = [dict(t, imagem=desenhar(f"tom-{t['id']}.jpg", dict(v0, tom=t['id']), False)) for t in TONS]
    # os momentos, desenhados no visual sugerido (as prévias animadas acompanham o visual que ele escolher)
    P1 = copy.deepcopy(P); aplicar_visual(P1, sug, dict(v0, ritmo=None, velocidade=None)); aplicar_fontes(P1); C = cores(P1)
    hexa = {k: '#%02X%02X%02X' % v for k, v in C.items() if k in ('fundo', 'destaque', 'acao', 'ok', 'alerta', 'gigante', 'texto')}
    saida = []
    for m in P.get('momentos', []):
        tab = plac.get(m.get('tipo', ''), {})
        nota = lambda o: tab.get(o.get('peca'), {}).get('escolhido', 0) - 0.5 * tab.get(o.get('peca'), {}).get('preterido', 0) + (100 if o.get('peca') in (trava or {}).get('pecas', []) else 0)   # as peças marcadas no Catálogo vêm primeiro
        ops = sorted(m.get('opcoes', []), key=lambda o: -nota(o))
        rec = ops[0]['id'] if ops else None
        t_ref = m.get('quadro', (m['inicio'] + m['fim']) / 2)
        if L.m(t_ref) is None: t_ref = L.orig(L.mc(t_ref))
        base_m = quadro(t_ref); tnm = L.m(t_ref)
        P0 = copy.deepcopy(P1); P0['inserts'] = []; P0['efeitos'] = []
        processar(base_m.copy(), tnm, P0, L, LEG, C).resize((540, 960), Image.LANCZOS).save(os.path.join(dest, f"{m['id']}.jpg"), quality=84)
        opcoes = []
        for op in ops:
            ins, ef = peca_da_opcao(m, op, PECAS); pc = PECAS.get(op.get('peca'), {}); fonte_de = ins or ef or {}
            o = {'id': op['id'], 'peca': op.get('peca'), 'cod': pc.get('cod', ''), 'nome': op.get('nome') or pc.get('nome', op.get('peca')),
                 'desc': op.get('desc') or pc.get('uso', ''), 'cuidado': pc.get('oab', ''),
                 'fonte': fonte_de.get('fonte', ''), 'prova': fonte_de.get('prova', ''), 'naoProva': fonte_de.get('naoProva', ''), 'oab': fonte_de.get('oab', {})}
            if ins and ins.get('tipo') == 'animacao':
                a, b = L.mc(ins['inicio']), L.mc(ins['fim'], depois=False)
                dados = dict(ins.get('dados', {}), fim=round(b - a, 3), marcas=[round(L.mc(x) - a, 3) for x in ins.get('marcas', [])] or ins.get('dados', {}).get('marcas', []),
                             familia=familia(ins, C), cores=hexa, baseMidia=url(os.path.join(pasta, 'midia')) + '/', **fontes_para_modelo())
                dados = dados_anuncio(ins['modelo'], dados, C)
                o['previa'] = {'modelo': url(os.path.join(ASSETS, 'animacoes', ins['modelo'] + '.html')), 'dados': dados}
            else:
                P2 = copy.deepcopy(P1); P2['inserts'] = [dict(ins, id='sb')] if ins else []; P2['efeitos'] = [dict(ef, id='sb')] if ef else []
                t_op = t_ref
                if ef and ef['tipo'] == 'transicao': t_op = L.orig((L.mc(ef['inicio']) + L.mc(ef['fim'], depois=False)) / 2 - 0.08)
                elif ins and ins.get('marcas'): t_op = L.orig(min(L.mc(ins['fim'], depois=False) - 0.2, L.mc(ins['marcas'][-1]) + 1.0))
                tn2 = L.m(t_op) if L.m(t_op) is not None else tnm
                fr2 = quadro(t_op) if abs(t_op - t_ref) > 0.05 else base_m.copy()
                processar(fr2, tn2, P2, L, LEG, C).resize((540, 960), Image.LANCZOS).save(os.path.join(dest, f"{m['id']}-{op['id']}.jpg"), quality=84)
                o['imagem'] = f"prancha/{m['id']}-{op['id']}.jpg"
            opcoes.append(o)
        fala = ' '.join(w['t'] for w in P['palavras'] if w['s'] >= m['inicio'] - 0.05 and w['e'] <= m['fim'] + 0.3)
        saida.append({'id': m['id'], 'titulo': m.get('titulo', ''), 'tipo': m.get('tipo', ''), 'tipoNome': MOMENTOS.get(m.get('tipo', ''), ''),
                      'nivel': int(m.get('nivel', 1)), 'inicio': m['inicio'], 'fim': m['fim'], 'fala': fala, 'quadro': f"prancha/{m['id']}.jpg",
                      'opcoes': opcoes, 'recomendada': rec})
    if os.path.exists(tmp): os.remove(tmp)
    aplicar_fontes(P)
    dados = {'projeto': P.get('id'), 'nome': P.get('nome'), 'travado': bool(trava), 'pecasPedidas': (trava or {}).get('pecas', []), 'partidas': partidas, 'familias': familias, 'legendas': legendas,
             'alturas': alturas, 'tons': tons, 'coresVideo': est['coresVideo'], 'corMarca': cor_marca or MEM.get('corMarca') or '',
             'fontesDaFamilia': FONTES_DA_FAMILIA, 'momentos': saida, 'fatos': P.get('fatos', []), 'cortes': len(P.get('cortes', [])),
             'duracao': round(L.total / float(P.get('velocidade', 1.0)), 1),
             'urls': {'fontesJs': url(os.path.join(ASSETS, 'animacoes', 'fontes.js')), 'catalogo': url(os.path.join(ASSETS, 'catalogo', 'index.html'))}}
    open(os.path.join(dest, 'dados.js'), 'w', encoding='utf-8').write('window.PRANCHA = ' + json.dumps(dados, ensure_ascii=False) + ';\n')
    shutil.copy(os.path.join(ASSETS, 'prancha', 'index.html'), os.path.join(pasta, 'prancha.html'))
    print('prancha:', os.path.abspath(os.path.join(pasta, 'prancha.html')), '·', 'curta (visual do Catálogo)' if trava else f'{len(partidas)} pontos de partida', '·', len(saida), 'momentos')
    sem_fonte = [f"{m['id']}{o['id']}" for m in saida for o in m['opcoes'] if (o.get('previa') or {}).get('dados', {}).get('imagem') and not o['fonte']]
    if sem_fonte: print('AVISO opção com imagem de fora e sem fonte:', ', '.join(sem_fonte))

def aprender(pasta, respostas, memoria):
    """memória do advogado: placar das peças por tipo de momento, pontos de partida escolhidos e ajustes por vídeo.
    respostas = o texto colado da prancha ou da Mesa. A métrica: os ajustes por vídeo têm que cair."""
    import datetime
    txt = open(respostas, encoding='utf-8').read()
    if '```json' in txt: txt = txt.split('```json', 1)[1].split('```', 1)[0]
    r = json.loads(txt[txt.index('{'):txt.rindex('}') + 1]); M = ler_memoria(memoria)
    hoje = datetime.date.today().isoformat()
    P = ler_projeto(pasta)
    if r.get('catalogo'):                           # pedido do Catálogo: só conta o ponto de partida escolhido
        k = ('fav-' + r['favorito']) if r.get('favorito') else (r.get('formato') or r.get('caminho') or '')
        if k: M['partidas'][k] = M['partidas'].get(k, 0) + 1
        os.makedirs(os.path.dirname(os.path.abspath(memoria)), exist_ok=True)
        json.dump(M, open(memoria, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('memória atualizada: pedido do Catálogo,', r.get('caminho'), k); return
    if r.get('prancha') or r.get('storyboard'):
        for m in P.get('momentos', []):
            esc = r.get('escolhas', {}).get(m['id'])
            if not esc or esc == '-': continue
            tab = M['placar'].setdefault(m.get('tipo', 'outro'), {})
            for op in m.get('opcoes', []):
                st = tab.setdefault(op.get('peca'), {'escolhido': 0, 'preterido': 0})
                st['escolhido' if op['id'] == esc else 'preterido'] += 1
        if r.get('partida'): M['partidas'][r['partida']] = M['partidas'].get(r['partida'], 0) + 1
        if r.get('corMarca'): M['corMarca'] = r['corMarca']
        ajustes, rodada = len(r.get('mudar', [])), 'prancha'
    else:
        ajustes = len(r.get('insertsAlterados', [])) + len(r.get('efeitosAlterados', [])) + len(r.get('pedidos', [])) + (1 if r.get('cortesMudaram') else 0)
        rodada = 'mesa'
    M['historico'].append({'video': P.get('id'), 'data': hoje, 'rodada': rodada, 'ajustes': ajustes})
    os.makedirs(os.path.dirname(os.path.abspath(memoria)), exist_ok=True)
    json.dump(M, open(memoria, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    por_video = {}
    for h in M['historico']: por_video.setdefault(h['video'], 0); por_video[h['video']] += h['ajustes']
    vids = list(por_video)
    print(f"memória atualizada: {rodada}, {ajustes} ajuste(s) neste vídeo")
    if len(vids) >= 2: print(f"ajustes por vídeo: {vids[-2]} = {por_video[vids[-2]]}, {vids[-1]} = {por_video[vids[-1]]}")

def favorito(pasta, memoria, nome):
    """guarda o visual do vídeo aprovado como ponto de partida com nome ("minha pauta quente"); mesmo nome substitui"""
    import datetime
    P = ler_projeto(pasta); M = ler_memoria(memoria)
    fav = {'nome': nome, 'formato': P.get('estilo', {}).get('receita', ''), 'visual': visual_do_projeto(P),
           'video': P.get('id'), 'data': datetime.date.today().strftime('%d/%m/%Y')}
    if isinstance(fav['visual'].get('cores'), str) and fav['visual']['cores'] not in ('video', 'padrao'): fav['visual']['cores'] = 'video'
    M['favoritos'] = [f for f in M['favoritos'] if f['nome'].lower() != nome.lower()] + [fav]
    os.makedirs(os.path.dirname(os.path.abspath(memoria)), exist_ok=True)
    json.dump(M, open(memoria, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    v = fav['visual']
    print(f"favorito '{nome}' guardado: formato {fav['formato']}, família {v['familia']}, legenda {v['legenda']} ({v['altura']}), "
          f"peças {v['densidade']}, corte {v['ritmo']}. Total de favoritos: {len(M['favoritos'])}")

def aplicar_prancha(pasta, P, r):
    """grava a prancha no projeto: ponto de partida, visual, peça de cada momento (insert ou efeito sb-<momento>),
    fatos e pedidos. Com variação, cria a pasta <pasta>-b com a versão B (outro ponto de partida, as mesmas peças)."""
    import copy, shutil
    PECAS, _ = catalogo_pecas()
    if r.get('visual'): aplicar_visual(P, r.get('formato') or r.get('partida', ''), r['visual'])
    nivel = DENSIDADE.get(P.get('estilo', {}).get('densidade', 'cheia'), 3)
    for m in P.get('momentos', []):
        sid = 'sb-' + m['id']; esc = r.get('escolhas', {}).get(m['id'])
        P['inserts'] = [i for i in P.get('inserts', []) if i.get('id') != sid]; P['efeitos'] = [e for e in P.get('efeitos', []) if e.get('id') != sid]
        m.pop('escolhida', None)
        if not esc or esc == '-' or int(m.get('nivel', 1)) > nivel: continue
        op = next((o for o in m.get('opcoes', []) if o['id'] == esc), None)
        if not op: continue
        m['escolhida'] = esc; ins, ef = peca_da_opcao(m, op, PECAS)
        if ins: P['inserts'].append(dict(ins, id=sid))
        if ef: P['efeitos'].append(dict(ef, id=sid))
    for f in r.get('fatos', []):
        k = int(f['id'][1:]) - 1
        if 0 <= k < len(P.get('fatos', [])) and f.get('resposta') in ('confere', 'tirar'):
            P['fatos'][k]['status'] = 'conferido' if f['resposta'] == 'confere' else 'tirar'
            if f.get('nota'): P['fatos'][k]['nota'] = f['nota']
    P['notas'] = [{'t': next((m['inicio'] for m in P.get('momentos', []) if m['id'] == x['id']), 0), 'texto': f"{x['id']}: {x.get('nota', '')}"} for x in r.get('mudar', [])]
    if r.get('geral'): P['notas'].append({'t': 0, 'texto': 'Geral: ' + r['geral']})
    gravar_projeto(pasta, P)
    est = P.get('estilo', {}); n = sum(1 for m in P.get('momentos', []) if m.get('escolhida'))
    print(f"prancha aplicada: ponto de partida {r.get('partida') or est.get('receita')}, família {est.get('familia')}, legenda {est.get('legenda')}, "
          f"{n} peça(s) da prancha, corte {est.get('ritmo')}, {len(P['cortes'])} cortes, {len(r.get('mudar', []))} pedido(s)")
    for nt in P['notas']: print(f"PEDIDO em {nt['t']:.1f} s: {nt['texto']}")
    var = r.get('variacao')
    if var and var.get('visual'):
        b = os.path.normpath(pasta) + '-b'; os.makedirs(b, exist_ok=True)
        for arq in ('index.html', 'proxy.mp4'):
            if os.path.exists(os.path.join(pasta, arq)): shutil.copy(os.path.join(pasta, arq), os.path.join(b, arq))
        if os.path.isdir(os.path.join(pasta, 'midia')): shutil.copytree(os.path.join(pasta, 'midia'), os.path.join(b, 'midia'), dirs_exist_ok=True)
        PB = copy.deepcopy(P); PB['id'] = P['id'] + '-b'; PB['nome'] = P.get('nome', '') + ' (versão B)'
        aplicar_visual(PB, var.get('formato') or var.get('partida', ''), var['visual'])
        nb = DENSIDADE.get(PB['estilo'].get('densidade', 'cheia'), 3)
        PB['inserts'] = [i for i in PB['inserts'] if not (i.get('id', '').startswith('sb-') and
                         int(next((m.get('nivel', 1) for m in PB.get('momentos', []) if 'sb-' + m['id'] == i['id']), 1)) > nb)]
        PB['efeitos'] = [e for e in PB['efeitos'] if not (e.get('id', '').startswith('sb-') and
                         int(next((m.get('nivel', 1) for m in PB.get('momentos', []) if 'sb-' + m['id'] == e['id']), 1)) > nb)]
        gravar_projeto(b, PB)
        print(f"versão B em {os.path.abspath(b)}: ponto de partida {var.get('partida')}, família {PB['estilo'].get('familia')}, "
              f"legenda {PB['estilo'].get('legenda')}, corte {PB['estilo'].get('ritmo')}, {len(PB['cortes'])} cortes")


def aplicar_catalogo(pasta, P, r, memoria=None):
    """grava o pedido do Catálogo, colado antes de processar: o visual (favorito, formato e o que ele marcou por cima) fica
    travado, a prancha sai curta (só os momentos) e as peças marcadas guiam as opções de cada momento"""
    FORM, _, _ = catalogo_formatos()
    est = P.setdefault('estilo', {}); caminho = r.get('caminho') or 'escolhido'
    if caminho == 'sugere':
        est.pop('travado', None); gravar_projeto(pasta, P)
        print('pedido do Catálogo: sugere para mim. Siga com a prancha completa.'); return
    M = ler_memoria(memoria or '')
    fav = next((f for f in M['favoritos'] if f['nome'].lower() == (r.get('favorito') or '').lower()), None)
    if r.get('favorito') and not fav: print(f"AVISO favorito '{r['favorito']}' não está na memória; segui sem ele")
    marcou = any(r.get(k) for k in ('formato', 'familia', 'legenda', 'cor', 'fontes'))
    if caminho == 'so-corta' and not fav and not marcou and M['favoritos']: fav = M['favoritos'][-1]   # o último favorito, como no atalho
    if r.get('formato') in FORM: v, partida = visual_do_formato(FORM[r['formato']]), r['formato']
    elif fav: v, partida = dict(fav['visual']), fav.get('formato', '')
    else: v, partida = visual_do_formato({}), ''
    if fav and r.get('formato') in FORM:            # favorito e formato juntos: o formato dá a estrutura, o favorito o visual
        v.update({k: fav['visual'][k] for k in ('familia', 'legenda', 'altura', 'cores', 'paleta', 'tom', 'fontes', 'moldura') if k in fav['visual']})
    if r.get('familia'): v['familia'] = r['familia']
    if r.get('legenda'): v['legenda'] = r['legenda']
    if r.get('cor'): v['tom'] = r['cor']
    if r.get('fontes'): v['fontes'] = '' if r['fontes'] == 'sistema' else r['fontes']
    if r.get('moldura'): v['moldura'] = True
    if caminho == 'so-corta': v['densidade'] = 'poucas'
    aplicar_visual(P, partida, v)
    est['travado'] = {'caminho': caminho, 'favorito': fav['nome'] if fav else '', 'pecas': r.get('pecas', []), 'adaptacoes': r.get('adaptacoes', '')}
    if caminho == 'so-corta': est['travado']['pecas'] = []
    gravar_projeto(pasta, P)
    PECAS, _ = catalogo_pecas()
    print(f"pedido do Catálogo aplicado: {'só corta e legenda' if caminho == 'so-corta' else 'visual travado'}, ponto de partida {partida or '(nenhum)'}"
          f"{', favorito ' + fav['nome'] if fav else ''}, família {est.get('familia')}, legenda {est.get('legenda')}, corte {est.get('ritmo')}, {len(P['cortes'])} cortes")
    if est['travado']['pecas']: print('peças pedidas:', ', '.join(f"{PECAS[x]['cod']} {PECAS[x]['nome']}" if x in PECAS else x for x in est['travado']['pecas']))
    if r.get('adaptacoes'): print('PEDIDO:', r['adaptacoes'])

# ---------- vídeo sem rosto (formato F13): o vídeo inteiro é a animação das cenas ----------
# O roteiro de cenas (cenas.json) vem da Banca de Conteúdo. O motor gera o próprio original (fundo.mp4: a cor do fundo,
# com a voz do advogado por baixo ou em silêncio) e um insert só, o modelo cenas, do começo ao fim. Daí em diante,
# quadros, video, zona e Mesa funcionam como em qualquer vídeo.
PAPEL = (246, 244, 239)

def duracao_midia(ff, arq):
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([ff, '-i', arq], capture_output=True, text=True).stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0

def gerar_fundo(ff, saida, cor, dur, voz=None):
    """vídeo liso na cor do fundo, 1080 x 1920: com a voz (dura o que ela dura) ou com silêncio (dur segundos)"""
    cmd = [ff, '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=0x%02X%02X%02X:s=%dx%d:r=%d' % (*cor, W, H, FPS)]
    cmd += ['-i', voz] if voz else ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{dur:.2f}']
    cmd += ['-map', '0:v', '-map', '1:a', '-shortest', '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'stillimage', '-crf', '28',
            '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', saida]
    subprocess.run(cmd, check=True)

def regua_cenas(ff, dados, pasta):
    """a régua de leitura calculada pelo próprio modelo cenas (a mesma conta da prévia e da gravação)"""
    dest = os.path.join(pasta, '_regua'); os.makedirs(dest, exist_ok=True)
    arq = os.path.join(dest, 'dados.json'); json.dump(dados, open(arq, 'w', encoding='utf-8'), ensure_ascii=False)
    subprocess.run([ferramenta('node', 'node'), ANIMAR, 'cenas', arq, dest, '--regua'], check=True, env=dict(os.environ, NODE_PATH=pasta_node(ff)))
    r = json.load(open(os.path.join(dest, 'regua.json'), encoding='utf-8'))
    if not r: sys.exit('o modelo cenas não devolveu a régua: confira o roteiro')
    return r

def marcas_da_fala(P, reg):
    """com voz: cada parte com "na" entra na palavra indicada; as outras são distribuídas entre essas âncoras na
    proporção da régua (encolhem se a fala for mais rápida) e, depois da última, cabem até o fim da fala.
    Devolve as marcas (tempo do original) e os avisos de texto que a fala não dá tempo de ler."""
    pal, partes, avisos, pos = P.get('palavras', []), reg['partes'], [], 0
    n = len(partes); ancora = [None] * n
    for i, p in enumerate(partes):
        if not p.get('na'): continue
        seq = [norma(x) for x in p['na'].split() if norma(x)]
        achou = next((j for j in range(pos, len(pal) - len(seq) + 1) if seq and [norma(pal[j + k]['t']) for k in range(len(seq))] == seq), None)
        if achou is None: avisos.append(f"cena {p['cena'] + 1}, {p['id']}: não achei \"{p['na']}\" na fala; segui pela régua"); continue
        ancora[i] = pal[achou]['s']; pos = achou + 1
    inicio = pal[0]['s'] if pal else 0.0
    if ancora[0] is None: ancora[0] = min([inicio] + [a for a in ancora if a is not None])
    fim_fala = (pal[-1]['e'] if pal else P.get('duracao', 0)) + 0.3
    em = [p['em'] for p in partes] + [partes[-1]['em'] + partes[-1]['dur']]
    idx = [i for i in range(n) if ancora[i] is not None]
    out = [0.0] * n
    for a, b in zip(idx, idx[1:] + [None]):
        ta = ancora[a]
        if b is None: tb, eb = max(ta + 0.5, fim_fala), em[n]; esc = min(1.0, (tb - ta) / max(0.01, eb - em[a]))
        else: tb, eb = ancora[b], em[b]; esc = (tb - ta) / max(0.01, eb - em[a])
        for i in range(a, b if b is not None else n): out[i] = ta + (em[i] - em[a]) * esc
    for i in range(1, n):
        if out[i] < out[i - 1] + 0.05: out[i] = out[i - 1] + 0.05
    out = [round(t, 3) for t in out]
    L, vel = Linha(P), float(P.get('velocidade', 1.0))
    fim_ed = L.mc(fim_fala, depois=False)
    for k in sorted({p['cena'] for p in partes}):     # por cena: a fala dá tempo de ler o que está na tela?
        ii = [i for i, p in enumerate(partes) if p['cena'] == k]
        prox = L.mc(out[ii[-1] + 1]) - reg['ponte'] if ii[-1] + 1 < n else fim_ed
        da = (prox - L.mc(out[ii[0]])) / vel
        pede = sum(partes[i]['dur'] for i in ii if partes[i]['texto'])
        if da < 0.7 * pede:                         # com a voz junto, ler pode ser um pouco mais rápido que a régua
            avisos.append(f"cena {k + 1}: o texto pede {pede:.1f} s de leitura e a fala dá {max(0, da):.1f} s; encurte o texto da tela ou fale um pouco mais devagar")
    return out, avisos

def fatos_do_roteiro(R, antigos):
    """cada lei, número, prazo e ressalva com a fonte vira um fato a confirmar na prancha das cenas"""
    st = {f.get('texto'): f for f in antigos or []}
    novos = []
    for k, c in enumerate(R.get('cenas', [])):
        pedacos = []
        if c.get('tipo') == 'lei': pedacos.append(c.get('texto', ''))
        elif c.get('tipo') == 'passos': pedacos += [p['texto'] + (' (' + p['ressalva'] + ')' if p.get('ressalva') else '') for p in c.get('passos', [])]
        elif c.get('tipo') == 'cuidado': pedacos.append(' '.join(x for x in (c.get('titulo'), c.get('texto'), c.get('numero'), c.get('numeroLegenda'), c.get('mito') and 'Mito: ' + c['mito'], c.get('fato') and 'Fato: ' + c['fato']) if x))
        if c.get('fonte') and pedacos: novos.append({'texto': f"Cena {k + 1}: " + ' · '.join(x for x in pedacos if x), 'fonte': c['fonte'], 'status': 'a confirmar'})
        if c.get('explica') and c.get('explicaFonte'): novos.append({'texto': f"Cena {k + 1}: {c.get('termo', '')} {c['explica']}".strip(), 'fonte': c['explicaFonte'], 'status': 'a confirmar'})
    for f in novos:
        if f['texto'] in st: f['status'] = st[f['texto']].get('status', f['status']); f.update({k: v for k, v in st[f['texto']].items() if k == 'nota'})
    return novos

def cenas(ff, roteiro, pasta, voz=None):
    R = json.load(open(roteiro, encoding='utf-8'))
    if not R.get('cenas'): sys.exit('o roteiro não tem cenas')
    os.makedirs(pasta, exist_ok=True)
    P = ler_projeto(pasta) if os.path.exists(os.path.join(pasta, 'projeto.js')) else {}
    fundo = os.path.join(pasta, 'fundo.mp4')
    P.setdefault('id', re.sub(r'[^a-z0-9]+', '-', (R.get('nome') or os.path.basename(roteiro)).lower()).strip('-') or 'sem-rosto')
    P.setdefault('nome', R.get('nome') or os.path.basename(roteiro))
    est = P.setdefault('estilo', {})
    est.update({'receita': 'sem-rosto', 'familia': R.get('familia') or est.get('familia') or 'editorial', 'legenda': 'nenhuma', 'zoomAlternado': 0})
    est.setdefault('destaques', [])
    if isinstance(R.get('cores'), dict): est['cores'] = R['cores']
    elif est.get('cores') == 'video': est.pop('cores')
    if 'fontes' in R: est['fontes'] = R['fontes'] or ''
    aplicar_fontes(P); C = cores(P)
    ins_dados = {'cenas': R['cenas'], 'fundo': 'cor' if R.get('fundo') == 'cor' else 'papel', 'barra': R.get('barra', True) is not False}
    cor_fundo = C['fundo'] if ins_dados['fundo'] == 'cor' else PAPEL
    sr = P.setdefault('semRosto', {}); sr.update({'roteiro': os.path.abspath(roteiro), 'original': 'fundo.mp4'})
    if voz:                                    # 1ª passada com voz: o fundo leva a voz; depois transcrever, preparar e revisar
        gerar_fundo(ff, fundo, cor_fundo, 0, voz)
        sr['voz'] = True; P.setdefault('velocidade', 1.0)
        gravar_projeto(pasta, P)
        print('fundo com a voz:', fundo, f'({duracao_midia(ff, fundo):.1f} s)')
        print('PRÓXIMO: transcreva e prepare o fundo.mp4 como um vídeo comum (transcrever.py, preparar, revisar) e rode cenas de novo, sem a voz.')
        return
    com_voz = bool(sr.get('voz') and P.get('palavras'))
    if sr.get('voz') and not P.get('palavras'): sys.exit('a voz ainda não foi preparada: rode transcrever.py e preparar no fundo.mp4 antes')
    dados_mod = dict(ins_dados, familia=C['familia'], cores={k: '#%02X%02X%02X' % v for k, v in C.items() if k in ('fundo', 'destaque', 'acao', 'ok', 'alerta', 'gigante')}, **fontes_para_modelo())
    reg = regua_cenas(ff, dados_mod, pasta)
    avisos = list(reg.get('avisos', []))
    if com_voz:
        marcas, av = marcas_da_fala(P, reg); avisos += av
        total = P['duracao']
    else:
        marcas = [p['em'] for p in reg['partes']]
        total = round(reg['total'] + 0.4, 2)
        gerar_fundo(ff, fundo, cor_fundo, total)
        subprocess.run([ff, '-y', '-loglevel', 'error', '-i', fundo, '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '30', '-g', '15',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', os.path.join(pasta, 'proxy.mp4')], check=True)
        P.update({'video': 'proxy.mp4', 'duracao': total, 'picos': [0] * int(total / 0.05 + 1), 'passoPicos': 0.05, 'palavras': [], 'cortes': [], 'velocidade': 1.0})
    ins = {'id': 'cenas', 'tipo': 'animacao', 'modelo': 'cenas', 'inicio': 0.0, 'fim': total, 'marcas': marcas, 'ativo': True, 'ocultaLegenda': True, 'dados': ins_dados}
    P['inserts'] = [i for i in P.get('inserts', []) if i.get('id') != 'cenas'] + [ins]
    P.setdefault('efeitos', []); P.setdefault('notas', [])
    sr.update({'voz': com_voz, 'regua': reg, 'avisos': avisos})
    P['fatos'] = fatos_do_roteiro(R, P.get('fatos', []))
    if R.get('oab'): P['oab'] = R['oab']
    gravar_projeto(pasta, P)
    L, vel = Linha(P), float(P.get('velocidade', 1.0))
    prancha_cenas(pasta, P, dados_mod, reg, [round(L.mc(m) / vel, 3) for m in marcas] if com_voz else None, round(L.total / vel, 2))
    print(f"cenas: {len(R['cenas'])}, {'com voz' if com_voz else 'sem voz (régua de leitura)'}, duração {L.total / vel:.1f} s")
    for k, c in enumerate(reg['cenas']):
        ini = next(L.mc(m) / vel for m, p in zip(marcas, reg['partes']) if p['cena'] == k)
        print(f"  {ini:5.1f} s  {c['tipo']:<9} {c['rotulo']}")
    for a in avisos: print('AVISO', a)
    print('original para quadros, video e zona:', fundo)
    print('prancha das cenas:', os.path.join(pasta, 'prancha-cenas.html'))

def prancha_cenas(pasta, P, dados, reg, marcas_editadas, total):
    """a prancha das cenas (antes de montar): a animação inteira com tocador, a régua de cada bloco, os fatos com fonte,
    o parecer da Trava OAB e um ajuste por cena; o advogado copia e cola na conversa"""
    base = url_arquivo(os.path.join(ASSETS, 'prancha-cenas')) + '/'
    html = open(os.path.join(ASSETS, 'prancha-cenas', 'index.html'), encoding='utf-8').read()
    d = dict(dados)
    if marcas_editadas: d.update(marcas=marcas_editadas, fim=total)
    info = {'projeto': P.get('id'), 'nome': P.get('nome'), 'dados': d, 'regua': reg, 'fatos': P.get('fatos', []), 'oab': P.get('oab'),
            'voz': bool(P.get('semRosto', {}).get('voz')), 'avisos': P.get('semRosto', {}).get('avisos', []), 'total': total}
    extra = '<script>window.PRANCHA_CENAS = ' + json.dumps(info, ensure_ascii=False) + ';</script>\n'
    html = html.replace('<head>\n', f'<head>\n<base href="{base}">\n', 1)
    k = html.index('<script')
    open(os.path.join(pasta, 'prancha-cenas.html'), 'w', encoding='utf-8').write(html[:k] + extra + html[k:])

def aplicar(pasta, pacote, memoria=None):
    """junta ao projeto.js o que o advogado mudou na Mesa, escolheu na prancha ou pediu no Catálogo; os pedidos escritos ficam para o Claude"""
    txt = open(pacote, encoding='utf-8').read()
    if '```json' in txt: txt = txt.split('```json', 1)[1].split('```', 1)[0]
    p = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
    if p.get('catalogo') and p.get('formato') == 'sem-rosto':
        return print('pedido do Catálogo: vídeo sem rosto (F13). Não há visual a gravar no vídeo cru: peça o roteiro de cenas à Banca, '
                     'rode cenas (com a voz deste vídeo, se ele quiser) e mostre a prancha das cenas.' + (' PEDIDO: ' + p['adaptacoes'] if p.get('adaptacoes') else ''))
    P = ler_projeto(pasta)
    if p.get('projeto') and p['projeto'] != P.get('id'):
        sys.exit(f"o pacote é do projeto {p['projeto']}, não de {P.get('id')}")
    if p.get('catalogo'): return aplicar_catalogo(pasta, P, p, memoria)
    if p.get('prancha') or p.get('storyboard'): return aplicar_prancha(pasta, P, p)
    P['cortes'] = p.get('cortes', P['cortes'])
    P['velocidade'] = p.get('velocidade', P.get('velocidade', 1.0))
    if p.get('legenda'): P.setdefault('estilo', {})['legenda'] = p['legenda']
    if p.get('familia'): P.setdefault('estilo', {})['familia'] = p['familia']
    for grupo, chave in (('inserts', 'insertsAlterados'), ('efeitos', 'efeitosAlterados')):
        lista = P.setdefault(grupo, [])
        for novo in p.get(chave, []):
            for k, velho in enumerate(lista):
                if velho['id'] == novo['id']: lista[k] = novo; break
            else: lista.append(novo)
    P['notas'] = p.get('pedidos', [])
    gravar_projeto(pasta, P)
    print('aplicado:', len(p.get('insertsAlterados', [])), 'insert(s),', len(p.get('efeitosAlterados', [])), 'efeito(s), legenda', P['estilo'].get('legenda'))
    for n in P['notas']: print(f"PEDIDO em {n['t']:.1f} s: {n['texto']}")

# ---------- resumo e juntar: o Claude lê e escreve o projeto sem abrir o projeto.js inteiro ----------
# o projeto.js leva os picos do áudio e todas as palavras (de 30 a 60 KB); lido inteiro, pesa no plano a cada vez.
PROTEGIDOS = ('picos', 'passoPicos', 'palavras', 'duracao', 'video')

def _tempo(ins, L):
    return f"{ins.get('inicio', 0):.2f}-{ins.get('fim', 0):.2f}"

def resumo(pasta, so_fala=False):
    """o projeto em texto curto: visual, peças, momentos e a fala em frases com o tempo do original"""
    P = ler_projeto(pasta); L = Linha(P); vel = float(P.get('velocidade', 1.0))
    if not so_fala:
        print(f"projeto {P.get('nome', '')} | original {P['duracao']:.1f} s | editado {L.total / vel:.1f} s a {vel}x | {len(P.get('cortes', []))} cortes")
        print('estilo', json.dumps(P.get('estilo', {}), ensure_ascii=False))
        for chave in ('inserts', 'efeitos'):
            for i in P.get(chave, []):
                extra = i.get('modelo') or i.get('texto') or i.get('titulo') or ''
                print(f"{chave[:-1]} {i.get('id', '?')} {i.get('tipo', '')} {_tempo(i, L)} {'' if i.get('ativo', True) else '(desligado) '}{str(extra)[:60]}")
        for m in P.get('momentos', []):
            print(f"momento {m.get('id')} {m.get('tipo', '')} n{m.get('nivel', '')} {_tempo(m, L)} {m.get('titulo', '')} | opções {','.join(o.get('peca', '?') for o in m.get('opcoes', []))}")
        for k in sorted(k for k in P if k not in PROTEGIDOS + ('estilo', 'inserts', 'efeitos', 'momentos', 'cortes', 'nome', 'id', 'velocidade')):
            v = json.dumps(P[k], ensure_ascii=False); print(k, v[:300] + (' ...' if len(v) > 300 else ''))
        print('fala (tempo do original; [corte] = trecho que sai):')
    frase, ini, ant, cort = [], None, None, False
    def solta():
        if frase: print(f"{ini:7.2f} {' '.join(frase)}{'  [corte]' if cort else ''}")
    for w in P['palavras']:
        fora = L.m((w['s'] + w['e']) / 2) is None
        if frase and (w['s'] - ant > 0.6 or len(frase) >= 14 or fora != cort):
            solta(); frase = []
        if not frase: ini, cort = w['s'], fora
        frase.append(w['t']); ant = w['e']
        if w['t'][-1:] in '.?!': solta(); frase = []
    solta()

def juntar(pasta, arquivo):
    """junta ao projeto um JSON curto escrito pelo Claude: inserts e efeitos entram ou trocam pelo id,
    estilo soma os campos, o resto (momentos, prancha, fatos, cortes, notas) troca inteiro"""
    P = ler_projeto(pasta); novo = json.load(open(arquivo, encoding='utf-8')); feito = []
    for k, v in novo.items():
        if k in PROTEGIDOS: print('ignorado (o motor cuida):', k); continue
        if k == 'estilo' and isinstance(v, dict):
            P.setdefault('estilo', {}).update(v); feito.append('estilo: ' + ', '.join(v))
        elif k in ('inserts', 'efeitos') and isinstance(v, list):
            lista = P.setdefault(k, []); pos = {i.get('id'): n for n, i in enumerate(lista)}
            for i in v:
                if i.get('id') in pos: lista[pos[i['id']]] = i
                else: lista.append(i)
            feito.append(f"{k}: {', '.join(str(i.get('id')) for i in v)}")
        else:
            P[k] = v; feito.append(k)
    gravar_projeto(pasta, P); print('juntado', '; '.join(feito) or 'nada')

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'catalogo': catalogo(*sys.argv[2:5])
    elif cmd == 'preparar': preparar(*sys.argv[2:6], *(sys.argv[6:7]))
    elif cmd == 'aplicar': aplicar(*sys.argv[2:5])
    elif cmd == 'quadros': quadros(*sys.argv[2:6], [float(x) for x in sys.argv[6:]])
    elif cmd == 'video': video(*sys.argv[2:6])
    elif cmd == '_trecho': video_trecho(*sys.argv[2:7])
    elif cmd == 'resumo': resumo(sys.argv[2], '--fala' in sys.argv)
    elif cmd == 'juntar': juntar(*sys.argv[2:4])
    elif cmd in ('prancha', 'storyboard'): prancha(*sys.argv[2:5], *(sys.argv[5:7]))
    elif cmd == 'aprender': aprender(*sys.argv[2:5])
    elif cmd == 'favorito': favorito(*sys.argv[2:5])
    elif cmd == 'zona': zona(*sys.argv[2:5], *(sys.argv[5:6]))
    elif cmd == 'cenas':
        a = sys.argv[2:]; voz = a[a.index('--voz') + 1] if '--voz' in a else None
        a = [x for i, x in enumerate(a) if x != '--voz' and (i == 0 or a[i - 1] != '--voz')]
        cenas(a[0], a[1], a[2], voz)
    elif cmd == 'revisar':
        args = [a for a in sys.argv[2:] if a != '--aplicar']
        revisar(args[-1], *(args[:2] if len(args) == 3 else []), aplicar_='--aplicar' in sys.argv)
    else: print(__doc__)
