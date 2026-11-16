"""Recorte da pessoa em qualquer sistema (Windows, Mac sem ferramentas da Apple, Linux).

Usa um modelo aberto de recorte de pessoas (u2net_human_seg, formato ONNX) rodando no processador.
O motor chama este recorte quando o do macOS (recortar.swift) não está disponível.
O modelo fica em <ferramentas>/modelos/u2net_human_seg.onnx (o instalador baixa) ou em MJ_RECORTE_MODELO.

Uso direto, para testar: python recortar.py <quadro.png> <mascara.png>
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

MEDIA, DESVIO, LADO = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225), 320


def caminho_modelo():
    if os.environ.get('MJ_RECORTE_MODELO'): return os.environ['MJ_RECORTE_MODELO']
    base = os.environ.get('MJ_FERRAMENTAS') or os.path.join(os.path.expanduser('~'), '.marketing-juridico', 'ferramentas')
    return os.path.join(base, 'modelos', 'u2net_human_seg.onnx')


class RecorteOnnx:
    def __init__(self, modelo=None):
        import onnxruntime as ort
        modelo = modelo or caminho_modelo()
        if not os.path.exists(modelo): raise FileNotFoundError(modelo)
        op = ort.SessionOptions(); op.log_severity_level = 3
        self.s = ort.InferenceSession(modelo, op, providers=['CPUExecutionProvider'])
        self.ent = self.s.get_inputs()[0].name

    def mascara(self, img):
        """devolve a máscara da pessoa (L, mesmo tamanho do quadro): branco é pessoa"""
        peq = np.asarray(img.convert('RGB').resize((LADO, LADO), Image.LANCZOS), dtype=np.float32)
        peq = peq / max(peq.max(), 1e-6)
        x = np.stack([(peq[..., c] - MEDIA[c]) / DESVIO[c] for c in range(3)])[None].astype(np.float32)
        m = self.s.run(None, {self.ent: x})[0][0, 0]
        m = (m - m.min()) / max(m.max() - m.min(), 1e-6)
        return Image.fromarray((m * 255).astype(np.uint8), 'L').resize(img.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))


if __name__ == '__main__':
    RecorteOnnx().mascara(Image.open(sys.argv[1])).save(sys.argv[2])
