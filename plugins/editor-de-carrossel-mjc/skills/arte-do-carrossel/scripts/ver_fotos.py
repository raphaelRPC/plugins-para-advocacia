#!/usr/bin/env python3
"""Folha de fotos: todas as fotos de uma pasta numa imagem só, com o nome e o formato de cada uma.

Serve para escolher as fotos do carrossel (e o ponto de enquadramento, o "foco") olhando uma imagem
em vez de abrir foto por foto, o que gasta bem menos do plano.

Uso:
    python3 ver_fotos.py <pasta de fotos> [saida.png]
Padrão da saída: <pasta>/_folha-de-fotos.png. Pastas com mais de 40 fotos saem em várias folhas
(_folha-de-fotos-1.png, -2...).
"""
import html
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_carrossel import achar_chrome, foto_da_tela  # noqa: E402

EXT = {".jpg", ".jpeg", ".png", ".webp"}
POR_FOLHA = 40
COLS = 8


def folha(fotos, saida, exe):
    cards = "".join(
        f'<div class="c"><div class="q"><img src="{f.resolve().as_uri()}"></div>'
        f'<div class="n">{html.escape(f.name)} <span></span></div></div>' for f in fotos)
    pagina = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}body{{background:#5b5852;padding:12px;display:grid;grid-template-columns:repeat({COLS},220px);gap:12px;width:max-content;font:600 14px system-ui;color:#fff}}
.q{{width:220px;height:260px;background:#3f3d39;display:flex;align-items:center;justify-content:center}}
.q img{{max-width:220px;max-height:260px;display:block}}.n{{padding:4px 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.n span{{opacity:.7;font-weight:400}}
</style></head><body>{cards}<script>
document.querySelectorAll('.c').forEach(function(c){{var i=c.querySelector('img');function f(){{var o=i.naturalWidth>i.naturalHeight*1.1?'paisagem':(i.naturalHeight>i.naturalWidth*1.1?'retrato':'quadrada');c.querySelector('span').textContent=i.naturalWidth+'x'+i.naturalHeight+' '+o;}}if(i.complete)f();else i.onload=f;}});
</script></body></html>"""
    tmp = Path(tempfile.mkdtemp(prefix="folha-")) / "folha.html"
    tmp.write_text(pagina, encoding="utf-8")
    linhas = (len(fotos) + COLS - 1) // COLS
    foto_da_tela(exe, tmp, saida, 12 + COLS * 232, 12 + linhas * 296, espera=6000)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pasta = Path(argv[0]).expanduser().resolve()
    fotos = sorted(f for f in pasta.iterdir() if f.suffix.lower() in EXT and not f.name.startswith("_"))
    if not fotos:
        print(f"Nenhuma foto em {pasta}")
        return 1
    exe = achar_chrome()
    if not exe:
        print("Navegador não encontrado: instale o Google Chrome.")
        return 4
    base = Path(argv[1]) if len(argv) > 1 else pasta / "_folha-de-fotos.png"
    grupos = [fotos[i:i + POR_FOLHA] for i in range(0, len(fotos), POR_FOLHA)]
    for k, g in enumerate(grupos, 1):
        saida = base if len(grupos) == 1 else base.with_name(f"{base.stem}-{k}{base.suffix}")
        folha(g, saida, exe)
        print("ok", saida, f"({len(g)} fotos)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
