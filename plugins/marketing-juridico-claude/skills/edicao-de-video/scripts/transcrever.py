"""Transcrição local com tempo por palavra, para a Ilha de edição.

Uso:
  python transcrever.py <video_ou_audio> <saida.json> [--modelo medium] [--rapido] [--nomes "Claude, OAB, CPC"]
  python transcrever.py <audio> --janelas 12.4,30.1,55.0 [--raio 1.5] [--modelo medium]
  python transcrever.py <pasta_mesa>/_revisao/audio-editado.wav --emendas <pasta_mesa>/_revisao/emendas.json

Inteiro: grava a lista de frases com as palavras ({w, s, e, p}), no formato que o motor lê.
  A transcrição é pedida "com hesitações": o modelo é guiado a escrever "é...", "hum", "ah" e repetições,
  que a transcrição comum esconde. É isso que deixa o comando `revisar` do motor achar o que cortar.
--janelas: transcreve trechos curtos em torno de cada tempo, com uma carga só do modelo (rápido).
--emendas: lê o emendas.json do comando `revisar` e escreve, para cada emenda, o que se ouve ali.
--rapido: modelo pequeno, só para escolher cortes; a legenda final usa o modelo médio.
--nomes: nomes próprios e termos que o modelo deve escrever certo (vão no texto de partida).
"""
import sys, json, argparse
from faster_whisper import WhisperModel, decode_audio

# texto de partida com hesitações: faz o modelo manter "é...", "hum" e repetições na transcrição
PARTIDA = "Hum, é... eu, eu acho que... ah, então, né. Tá. É, bom, olha só."


def carregar(modelo):
    print(f'carregando o modelo {modelo} (na primeira vez ele é baixado)', flush=True)
    return WhisperModel(modelo, device='cpu', compute_type='int8')


def transcrever(m, audio, nomes='', partida=True):
    prompt = ' '.join(x for x in ((PARTIDA if partida else ''), nomes) if x) or None
    segs, _ = m.transcribe(audio, language='pt', word_timestamps=True, vad_filter=False, beam_size=5,
                           condition_on_previous_text=False, initial_prompt=prompt)
    return segs


def inteiro(a):
    m = carregar('small' if a.rapido else a.modelo)
    out = []
    for s in transcrever(m, a.entrada, a.nomes):
        out.append({'start': s.start, 'end': s.end, 'text': s.text,
                    'words': [{'w': w.word, 's': round(w.start, 3), 'e': round(w.end, 3), 'p': round(w.probability, 3)} for w in s.words]})
        print(f'[{s.start:6.2f} - {s.end:6.2f}] {s.text}', flush=True)
    json.dump(out, open(a.saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def ouvir(m, som, tempos, raio, nomes=''):
    """o que se ouve em cada janela [t - raio, t + raio] do áudio já decodificado"""
    sr = 16000; res = []
    for t in tempos:
        a, b = max(0, int((t - raio) * sr)), min(len(som), int((t + raio) * sr))
        txt = ' '.join(s.text.strip() for s in transcrever(m, som[a:b], nomes, partida=True))
        res.append(txt)
    return res


def janelas(a):
    m = carregar(a.modelo); som = decode_audio(a.entrada, sampling_rate=16000)
    tempos = [float(x) for x in a.janelas.split(',') if x.strip()]
    for t, txt in zip(tempos, ouvir(m, som, tempos, a.raio, a.nomes)):
        print(f'{t:7.2f} s | {txt}', flush=True)


def emendas(a):
    E = json.load(open(a.emendas, encoding='utf-8'))
    m = carregar(a.modelo); som = decode_audio(a.entrada, sampling_rate=16000)
    ouvidos = ouvir(m, som, [e['t'] for e in E['emendas']], a.raio, a.nomes)
    for e, txt in zip(E['emendas'], ouvidos):
        e['ouvido'] = txt
        print(f"emenda {e['n']:>2} em {e['t']:6.2f} s (original {e['corte'][0]:.2f} a {e['corte'][1]:.2f})\n"
              f"   esperado: {e['esperado']}\n   ouvido:   {txt}", flush=True)
    json.dump(E, open(a.emendas, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('entrada'); p.add_argument('saida', nargs='?')
    p.add_argument('--modelo', default='medium'); p.add_argument('--rapido', action='store_true')
    p.add_argument('--nomes', default=''); p.add_argument('--janelas'); p.add_argument('--emendas')
    p.add_argument('--raio', type=float, default=1.5)
    a = p.parse_args()
    if a.emendas: emendas(a)
    elif a.janelas: janelas(a)
    elif a.saida: inteiro(a)
    else: print(__doc__)
