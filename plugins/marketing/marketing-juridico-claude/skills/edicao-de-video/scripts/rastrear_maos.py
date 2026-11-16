"""Rastreia as mãos num trecho do vídeo cru e grava a trilha para a peça Logo em 3D no modo "maos".

Uso: python rastrear_maos.py <ffmpeg> <video> <inicio_s> <fim_s> <saida.json> [--modelo hand_landmarker.task]
Saída: {"marcas": [...], "dados": {"trilhas": [[[x, topo], ...], ...]}}: uma trilha por mão aberta (esquerda da tela primeiro),
com x e o topo da mão no quadro 1080 x 1920 e os tempos do vídeo cru. Copie "marcas" e "trilhas" para o insert.
Precisa do mediapipe e do modelo hand_landmarker.task (ainda fora do instalador). Sem eles, o script avisa e sai com
código 2: escreva a trilha à mão, com 4 a 8 pontos tirados dos quadros (comando quadros do motor).
"""
import sys, os, json, glob, subprocess, tempfile, statistics as st

W, H, FPS = 1080, 1920, 15

def args():
    a = sys.argv[1:]
    modelo = None
    if '--modelo' in a:
        i = a.index('--modelo'); modelo = a[i + 1]; del a[i:i + 2]
    if len(a) != 5: sys.exit(__doc__)
    ff, video, ini, fim, saida = a
    ferr = os.environ.get('MJ_FERRAMENTAS') or os.path.join(os.path.expanduser('~'), '.marketing-juridico', 'ferramentas')
    return ff, video, float(ini), float(fim), saida, modelo or os.path.join(ferr, 'modelos', 'hand_landmarker.task')

def detectar(ff, video, ini, fim, modelo):
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
    except ImportError:
        print('rastreador de mãos indisponível (falta o mediapipe): escreva a trilha à mão a partir dos quadros'); sys.exit(2)
    if not os.path.exists(modelo):
        print(f'rastreador de mãos indisponível (falta o modelo {modelo}): escreva a trilha à mão a partir dos quadros'); sys.exit(2)
    tmp = tempfile.mkdtemp()
    subprocess.run([ff, '-v', 'error', '-y', '-ss', str(ini), '-t', str(fim - ini), '-i', video,
                    '-vf', f'fps={FPS},scale={W // 2}:{H // 2}', os.path.join(tmp, 'f_%05d.jpg')], check=True)
    det = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
        base_options=mpt.BaseOptions(model_asset_path=modelo), num_hands=2, min_hand_detection_confidence=0.3,
        running_mode=vision.RunningMode.IMAGE))
    out = []
    for i, f in enumerate(sorted(glob.glob(os.path.join(tmp, 'f_*.jpg')))):
        r = det.detect(mp.Image.create_from_file(f)); maos = []
        for lm in r.hand_landmarks:
            pts = [(p.x * W, p.y * H) for p in lm]
            palma = [pts[k] for k in (0, 5, 9, 13, 17)]                       # pulso e base dos dedos
            maos.append({'x': sum(p[0] for p in palma) / 5, 'top': min(p[1] for p in pts)})
        out.append((ini + i / FPS, maos))
    return out

def trilha(quadros, esquerda):
    """uma mão por lado da tela; descarta saltos (outra mão confundida) e suaviza (mediana e média móveis)"""
    pts, prev, saltos = [], None, 0
    for t, maos in quadros:
        c = [h for h in maos if (h['x'] < W / 2) == esquerda]
        if not c: continue
        if prev: c.sort(key=lambda h: abs(h['x'] - prev['x']) + abs(h['top'] - prev['top']))
        h = c[0]
        if prev and abs(h['x'] - prev['x']) + abs(h['top'] - prev['top']) > 160 and saltos < 2:
            saltos += 1; continue                                 # salto isolado: ignora; três seguidos: a mão é essa
        if saltos >= 2 and len(pts) <= 2: pts = []                # o começo é que estava errado
        pts.append((t, h['x'], h['top'])); prev = h; saltos = 0
    if len(pts) < 3: return None
    def suav(v):
        v = [st.median(v[max(0, i - 2):i + 3]) for i in range(len(v))]
        return [sum(v[max(0, i - 2):i + 3]) / len(v[max(0, i - 2):i + 3]) for i in range(len(v))]
    xs, ys = suav([p[1] for p in pts]), suav([p[2] for p in pts])
    return [(round(t, 3), round(x), round(y)) for (t, _, _), x, y in zip(pts, xs, ys)][::2]

if __name__ == '__main__':
    ff, video, ini, fim, saida, modelo = args()
    q = detectar(ff, video, ini, fim, modelo)
    trs = [tr for tr in (trilha(q, True), trilha(q, False)) if tr]
    res = {'marcas': [t for tr in trs for t, _, _ in tr], 'dados': {'trilhas': [[[x, y] for _, x, y in tr] for tr in trs]}}
    json.dump(res, open(saida, 'w'))
    for tr, lado in zip(trs, ('primeira', 'segunda')):
        print(f'{lado} mão: {tr[0][0]:.2f} a {tr[-1][0]:.2f} s, {len(tr)} pontos')
    if not trs: print('nenhuma mão aberta encontrada no trecho')
