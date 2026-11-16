"""Teste da instalação da Ilha de edição (Mac e Windows).

Gera um vídeo de 5 segundos passando por todas as peças: corte, título, legenda, recorte da pessoa,
camada animada no navegador e transcrição. Se o vídeo sair, a máquina está pronta para editar.

Uso: python testar_instalacao.py [pasta_ferramentas]
Lê <ferramentas>/caminhos.json (gravado pelo instalador) e grava <ferramentas>/teste/teste-instalacao.mp4.
"""
import os, sys, json, subprocess, shutil

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

AQUI = os.path.dirname(os.path.abspath(__file__))
FERR = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('MJ_FERRAMENTAS') or os.path.join(os.path.expanduser('~'), '.marketing-juridico', 'ferramentas')
CAM = json.load(open(os.path.join(FERR, 'caminhos.json'), encoding='utf-8'))
FF = CAM['ffmpeg']; T = os.path.join(FERR, 'teste'); falhas = []
shutil.rmtree(T, ignore_errors=True); os.makedirs(T)


def etapa(nome, fn):
    print(f'- {nome}...', flush=True)
    try:
        fn(); print(f'  ok: {nome}', flush=True)
    except Exception as e:
        falhas.append(nome); print(f'  FALHOU: {nome}: {e}', flush=True)


# vídeo cru sintético: fundo com um "rosto" (círculo claro) e um tom de áudio, 6 segundos, vertical
cru = os.path.join(T, 'cru.mp4')
def gerar_cru():
    subprocess.run([FF, '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=0x2C485F:s=1080x1920:d=6',
                    '-f', 'lavfi', '-i', 'sine=frequency=220:duration=6', '-vf',
                    "drawbox=x=0:y=1100:w=1080:h=820:color=0x6B7F99:t=fill,drawbox=x=360:y=520:w=360:h=460:color=0xD9B59A:t=fill",
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', cru], check=True)

def transcricao_falsa():
    pal = [('Este', .2, .5), ('é', .5, .6), ('o', .6, .7), ('teste', .7, 1.1), ('da', 1.1, 1.2), ('Ilha', 1.2, 1.6), ('de', 1.6, 1.7), ('edição.', 1.7, 2.3),
           ('Tudo', 3.0, 3.3), ('pronto', 3.3, 3.8), ('para', 3.8, 4.0), ('editar.', 4.0, 4.7)]
    json.dump([{'start': 0, 'end': 5, 'text': '', 'words': [{'w': ' ' + w, 's': s, 'e': e} for w, s, e in pal]}],
              open(os.path.join(T, 'transc.json'), 'w', encoding='utf-8'), ensure_ascii=False)

def motor(*args):
    env = dict(os.environ, NODE_PATH=CAM.get('node_path', ''), MJ_FERRAMENTAS=FERR)
    r = subprocess.run([sys.executable, os.path.join(AQUI, 'montar_video.py'), *args], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    if r.returncode: raise RuntimeError((r.stderr or r.stdout)[-600:])
    return r.stdout

def montar():
    mesa = os.path.join(T, 'mesa')
    motor('preparar', FF, cru, os.path.join(T, 'transc.json'), mesa, 'teste')
    sys.path.insert(0, AQUI); import montar_video as m
    P = m.ler_projeto(mesa)
    P['estilo'].update(familia='editorial', legenda='destaque', destaques=['edição'])
    P['inserts'] = [{'id': 'i1', 'tipo': 'duascamadas', 'familia': 'atras', 'ativo': True, 'inicio': 0.2, 'fim': 2.4, 'rotulo': 'Teste da', 'titulo': 'Ilha'},
                    {'id': 'a1', 'tipo': 'animacao', 'modelo': 'palavra', 'ativo': True, 'inicio': 3.0, 'fim': 4.8, 'marcas': [3.3],
                     'dados': {'rotulo': 'Tudo', 'palavra': 'PRONTO'}, 'ocultaLegenda': True}]
    m.gravar_projeto(mesa, P)
    print(motor('video', FF, cru, mesa, os.path.join(T, 'teste-instalacao.mp4')).strip().splitlines()[-1])
    if not os.path.exists(os.path.join(T, 'teste-instalacao.mp4')): raise RuntimeError('o vídeo não foi gerado')

def transcrever():
    from faster_whisper import WhisperModel
    WhisperModel('medium', device='cpu', compute_type='int8', local_files_only=True)

def recorte():
    sys.path.insert(0, AQUI); from PIL import Image
    import montar_video as m
    if not m.RECORTE.disponivel(): raise RuntimeError('recorte da pessoa indisponível')
    m.RECORTE.mascara(Image.new('RGB', (1080, 1920), (90, 90, 90)))

etapa('gerar vídeo de teste', gerar_cru)
transcricao_falsa()
etapa('recorte da pessoa (palavra atrás de você)', recorte)
etapa('montar o vídeo com título, legenda e animação', montar)
etapa('modelo de transcrição baixado', transcrever)
if falhas:
    print('FALTA AJUSTAR:', ', '.join(falhas)); sys.exit(1)
print('PRONTO! Vídeo de teste:', os.path.join(T, 'teste-instalacao.mp4'))
