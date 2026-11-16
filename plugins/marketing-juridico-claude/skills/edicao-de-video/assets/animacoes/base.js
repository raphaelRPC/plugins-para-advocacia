// Utilidades comuns dos modelos de animação.
// Regra de todos os modelos: o quadro depende só do tempo t (em segundos desde a entrada do insert),
// sem relógio e sem memória entre quadros. window.desenhar(t) desenha; window.PRONTO avisa que carregou.
// O mesmo modelo serve para o vídeo final (gravado por animar.js), para a vitrine, para o catálogo
// e para a prancha do vídeo: aberto com "?previa", ele anima sozinho em ciclo, com os dados do endereço (#{...}).
window.DADOS = window.DADOS || {};
if (!Object.keys(window.DADOS).length && location.hash.length > 1) {
  try { window.DADOS = JSON.parse(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
}
window.FAMILIA = DADOS.familia || 'institucional';   // editorial, revista, atras, celular, institucional
window.SECO = FAMILIA === 'celular';                   // celular: entra e sai em corte seco, sem mola
window.U = {
  clamp: (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)),
  pr: (t, a, b) => (b > a ? U.clamp((t - a) / (b - a)) : (t >= b ? 1 : 0)),
  eo: x => 1 - Math.pow(1 - U.clamp(x), 3),
  eio: x => { x = U.clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; },
  // mola amortecida: chega ao alvo em cerca de d segundos, com um passo além de no máximo 8%
  mola: (t, d = 0.6) => { if (t <= 0) return 0; if (SECO) return 1; const x = t / d; return x >= 1.8 ? 1 : 1 - Math.exp(-6 * x) * Math.cos(7.5 * x); },
  lerp: (a, b, x) => a + (b - a) * x,
  // opacidade de entrada e saída: entra em ent segundos, sai depois de fim
  janela: (t, fim, ent = 0.35, sai = 0.35) => SECO ? (t >= 0 && t <= fim ? 1 : 0) : U.eo(t / ent) * (1 - U.eo((t - fim) / sai)),
  // tempo em que cada parte entra: marcas (relativas à entrada) ou distribuídas até o fim
  marcas: (n, fim) => {
    const mk = (DADOS.marcas || []).slice(0, n);
    while (mk.length < n) { const ult = mk.length ? mk[mk.length - 1] : 0; mk.push(ult + Math.max(0.35, (fim - 0.6 - ult) / (n - mk.length + 1))); }
    return mk;
  },
  // sorteio com semente: o mesmo t sempre dá o mesmo quadro
  semente: n => { let s = (n * 9301 + 49297) % 233280; return () => (s = (s * 9301 + 49297) % 233280) / 233280; },
  // texto sendo digitado: p de 0 a 1 vira quantas letras aparecem
  digitar: (txt, p) => txt.slice(0, Math.round(U.clamp(p) * txt.length)),
  // letras sorteando até travar na palavra certa, da esquerda para a direita
  embaralhar: (txt, p, t) => {
    const sim = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&', fixas = Math.floor(U.clamp(p) * txt.length);
    const r = U.semente(Math.floor(t * 18) + 7);
    return [...txt].map((c, i) => (i < fixas || c === ' ' ? c : sim[Math.floor(r() * sim.length)])).join('');
  },
  // traço que se desenha (SVG): p de 0 a 1
  traco: (el, p) => { const L = el.getTotalLength(); el.style.strokeDasharray = L; el.style.strokeDashoffset = L * (1 - U.clamp(p)); },
  // endereço de uma imagem da pasta midia/: no gravador vem de /midia/; na prévia, de DADOS.baseMidia (pasta da página)
  midia: a => { a = String(a || '').replace(/^\/?midia\//, ''); return /[?&]previa/.test(location.search) ? (DADOS.baseMidia || '') + a : '/midia/' + a; },
  // zona segura do Reels (1080 x 1920): texto entre estes limites
  ZONA: { x0: 72, x1: 1008, y0: 232, y1: 1500 }
};
window.COR = Object.assign({ fundo: '#14243F', destaque: '#F2B33D', papel: '#F8F4EB', texto: '#FFFFFF', ok: '#4CC38A', alerta: '#DE3430' }, DADOS.cores || {});
window.FIM = DADOS.fim ?? 4;   // segundos até a saída, relativos à entrada

// letras de cada família (o advogado pode trocar pelas fontes do padrão dele: DADOS.fontes)
(() => {
  const sans = '"Avenir Next","Segoe UI",Helvetica,Arial,sans-serif';
  const cond = '"Avenir Next Condensed","Bahnschrift Condensed","Arial Narrow",sans-serif';
  const serifa = 'Didot,"Bodoni 72","New York",Georgia,serif';
  const mono = 'Menlo,Consolas,"Courier New",monospace';
  const F = Object.assign({
    titulo: FAMILIA === 'revista' ? serifa : FAMILIA === 'celular' || FAMILIA === 'institucional' ? sans : cond,
    texto: sans, serifa, mono, cond
  }, DADOS.fontes || {});
  const r = document.documentElement.style;
  for (const [k, v] of Object.entries(F)) r.setProperty('--t-' + k, v);
  for (const [k, v] of Object.entries(COR)) r.setProperty('--c-' + k, v);
  r.setProperty('--titulo-estilo', FAMILIA === 'revista' ? 'italic' : 'normal');
  r.setProperty('--titulo-peso', FAMILIA === 'revista' ? '400' : '800');
  // na prévia (páginas abertas do disco), as fontes vêm do Google Fonts
  if (DADOS.googleFontes && /[?&]previa/.test(location.search)) { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = DADOS.googleFontes; document.head.appendChild(l); }
  // arquivos de fonte do padrão do advogado (servidos em /fontes/ pelo gravador e copiados ao lado das páginas)
  for (const a of /[?&]previa/.test(location.search) ? [] : DADOS.arquivosFontes || []) {
    const s = document.createElement('style');
    s.textContent = `@font-face{font-family:"${a.familia}";src:url("${a.url}");font-weight:${a.peso || 400};font-style:${a.estilo || 'normal'}}`;
    document.head.appendChild(s);
  }
})();

// tempo pedido por outra página (o palco do vídeo sem rosto, a prancha das cenas), que funciona também com as páginas
// abertas do disco: {mjT: t} desenha o tempo t; {mjPergunta: 1} responde se o modelo está pronto e a área que ocupa
addEventListener('message', e => {
  const m = e.data || {};
  if (typeof m.mjT === 'number') { window.MJ_T = m.mjT; if (!/[?&]previa/.test(location.search) && window.PRONTO && window.desenhar) window.desenhar(m.mjT); }
  if (m.mjPergunta && e.source) e.source.postMessage({ mjPronto: !!window.PRONTO, area: window.AREA || null, regua: window.REGUA || null }, '*');
});

// prévia: com "?previa" no endereço, o modelo anima sozinho em ciclo (vitrine, catálogo, prancha do vídeo)
if (/[?&]previa/.test(location.search)) {
  const ciclo = () => FIM + 1.2;
  const inicia = () => {
    const t0 = performance.now();
    const passo = agora => { if (window.desenhar) window.desenhar(window.MJ_T ?? ((agora - t0) / 1000) % ciclo()); requestAnimationFrame(passo); };
    requestAnimationFrame(passo);
  };
  const espera = () => (window.PRONTO ? inicia() : setTimeout(espera, 60));
  espera();
}
