#!/usr/bin/env python3
"""Gera o catálogo visual dos estilos (assets/catalogo/catalogo.html e as imagens em assets/catalogo/img/).

Monta o mesmo carrossel de exemplo em cada estilo da pasta assets/estilos/ e guarda a prancha de cada um.
Rode de novo sempre que um estilo novo entrar ou um estilo mudar:
    python3 scripts/gerar_catalogo.py
"""
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ASSETS = AQUI.parent / "assets"
CAT = ASSETS / "catalogo"
EXEMPLO = ASSETS / "exemplos" / "explicativo-pensao.json"
EXEMPLO_FOTO = ASSETS / "exemplos" / "explicativo-pensao-com-foto.json"


def jpg(origem, destino, largura=1400):
    try:
        from PIL import Image
        im = Image.open(origem).convert("RGB")
        if im.width > largura:
            im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
        im.save(destino, quality=82, optimize=True)
    except ImportError:
        subprocess.run(["sips", "-Z", str(largura), "-s", "format", "jpeg", "-s", "formatOptions", "82",
                        str(origem), "--out", str(destino)], check=True, capture_output=True)


def main():
    (CAT / "img").mkdir(parents=True, exist_ok=True)
    estilos = []
    for pasta in sorted(p for p in (ASSETS / "estilos").iterdir() if (p / "estilo.json").exists()):
        cfg = json.loads((pasta / "estilo.json").read_text(encoding="utf-8"))
        exemplo = EXEMPLO_FOTO if cfg.get("foto_modo") == "sangrada" else EXEMPLO
        tmp = Path(tempfile.mkdtemp(prefix="catalogo-"))
        r = subprocess.run([sys.executable, str(AQUI / "montar_carrossel.py"), str(exemplo), "--estilo", cfg["codigo"],
                            "--saida", str(tmp), "--base", str(exemplo.parent)], capture_output=True, text=True)
        if not (tmp / "prancha.png").exists():
            print(r.stdout[-800:], r.stderr[-800:])
            raise SystemExit(f"falhou {cfg['codigo']}")
        jpg(tmp / "prancha.png", CAT / "img" / f"{cfg['codigo']}.jpg")
        jpg(tmp / "png" / "carrossel-01.png", CAT / "img" / f"{cfg['codigo']}-capa.jpg", 540)
        shutil.rmtree(tmp, ignore_errors=True)
        estilos.append(cfg)
        print("ok", cfg["codigo"], cfg["nome"])

    cards = ""
    for c in estilos:
        pedido = f"Monta o carrossel no estilo {c['codigo']} {c['nome']}."
        cards += f"""
<article class="est" id="{c['codigo']}">
  <header><span class="cod">{c['codigo']}</span><h2>{html.escape(c['nome'])}</h2></header>
  <p class="res">{html.escape(c['resumo'])}</p>
  <img src="img/{c['codigo']}.jpg" alt="Carrossel de exemplo no estilo {html.escape(c['nome'])}" loading="lazy">
  <div class="meta">
    <p><b>Bom para:</b> {html.escape(', '.join(c.get('serve', [])))}</p>
    <p><b>Evite:</b> {html.escape(', '.join(c.get('evite', [])))}</p>
    <p><b>Fontes:</b> {html.escape(' · '.join(dict.fromkeys(c.get('fontes', {}).values())))}</p>
  </div>
  <button data-pedido="{html.escape(pedido)}">Copiar pedido</button>
</article>"""
    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Catálogo de estilos</title><style>
:root{{--fundo:#F4F2EE;--cartao:#FFFFFF;--tinta:#1D1B18;--suave:#6B655C;--linha:#E0D9CD;--acento:#8E1B2B;--sobre:#FFFFFF}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--fundo:#191816;--cartao:#24221F;--tinta:#EEEAE3;--suave:#A7A095;--linha:#36332E;--acento:#E39AA6;--sobre:#191816}}}}
:root[data-theme="dark"]{{--fundo:#191816;--cartao:#24221F;--tinta:#EEEAE3;--suave:#A7A095;--linha:#36332E;--acento:#E39AA6;--sobre:#191816}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--fundo);color:var(--tinta);font:16px/1.55 system-ui,-apple-system,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:32px 16px 80px}}
h1{{font-size:30px;margin:0 0 6px;letter-spacing:-.01em}}.intro{{color:var(--suave);max-width:760px;margin:0 0 10px}}
.caminhos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:22px 0 30px}}
.caminhos div{{background:var(--cartao);border:1px solid var(--linha);border-radius:12px;padding:14px 16px}}
.caminhos b{{display:block;margin-bottom:4px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:22px}}
.est{{background:var(--cartao);border:1px solid var(--linha);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:12px}}
.est header{{display:flex;align-items:baseline;gap:12px}}.est h2{{margin:0;font-size:22px}}
.cod{{font:600 13px ui-monospace,monospace;background:var(--acento);color:var(--sobre);padding:3px 8px;border-radius:6px}}
.res{{margin:0;color:var(--suave)}}.est img{{width:100%;height:auto;border-radius:8px;display:block}}
.meta p{{margin:2px 0;font-size:15px}}
button{{align-self:flex-start;background:var(--acento);color:var(--sobre);border:0;border-radius:8px;padding:10px 16px;font:inherit;font-weight:600;cursor:pointer}}
.aviso{{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:var(--tinta);color:var(--fundo);padding:10px 16px;border-radius:8px;opacity:0;transition:opacity .2s}}
.aviso.on{{opacity:1}}
</style></head><body><main>
<h1>Catálogo de estilos do carrossel</h1>
<p class="intro">O mesmo carrossel de exemplo montado em cada estilo. As suas cores, fontes e fotos entram por cima de qualquer um. Escolha um, clique em "Copiar pedido" e cole na conversa com o Claude.</p>
<div class="caminhos">
<div><b>Já sei o que quero</b>Diga o estilo ou um favorito seu: "monta no Ensaio".</div>
<div><b>Me mostra</b>Esta página: compare e copie o pedido do estilo que combinar.</div>
<div><b>Sugere para mim</b>O Claude escolhe pelo tipo de carrossel e pela sua base, e oferece uma alternativa.</div>
</div>
<div class="grade">{cards}</div>
</main><div class="aviso" id="aviso">Pedido copiado. Cole na conversa.</div>
<script>
document.querySelectorAll('button[data-pedido]').forEach(function(b){{b.onclick=function(){{
  var t=b.getAttribute('data-pedido'), a=document.getElementById('aviso');
  function ok(){{a.classList.add('on');setTimeout(function(){{a.classList.remove('on');}},1800);}}
  try{{navigator.clipboard.writeText(t).then(ok,function(){{prompt('Copie o pedido:',t);}});}}catch(e){{prompt('Copie o pedido:',t);}}
}};}});
</script></body></html>"""
    (CAT / "catalogo.html").write_text(pagina, encoding="utf-8")
    print("ok", (CAT / "catalogo.html"))


if __name__ == "__main__":
    main()
