// Captura de página oficial ou matéria com o trecho que o advogado vai ler, para a faixa em cima do vídeo.
// Abre o endereço no Chrome sem janela (largura de celular), acha cada trecho no texto da página,
// guarda a imagem e onde cada trecho está, para o motor passar o marca-texto no tempo da fala.
//
// Uso: node capturar_pagina.js <endereco> <pasta_midia> <nome> "trecho 1" ["trecho 2" ...]
// Saída: <nome>.png e <nome>.json ({endereco, site, titulo, acesso, imagem, grifos: [{trecho, achado, retangulos}]})
// Precisa de: Google Chrome (ou CHROME_PATH) e puppeteer-core no NODE_PATH.
// Use só fonte pública (DOU, STF, STJ, Planalto, tribunal, matéria jornalística). Nunca página com dado de parte ou cliente.

const fs = require('fs'), path = require('path');
const puppeteer = require('puppeteer-core');
const [endereco, pasta, nome, ...trechos] = process.argv.slice(2);
if (!endereco || !pasta || !nome || !trechos.length) { console.error('uso: node capturar_pagina.js <endereco> <pasta_midia> <nome> "trecho" ...'); process.exit(2); }

function chrome() {
  // Chrome do sistema; no Windows, o Edge também serve (é o mesmo motor); por último, o navegador baixado pelo instalador
  const local = process.env.LOCALAPPDATA || '', pf = process.env.PROGRAMFILES || 'C:/Program Files', pf86 = process.env['PROGRAMFILES(X86)'] || 'C:/Program Files (x86)';
  const ferr = process.env.MJ_FERRAMENTAS || path.join(require('os').homedir(), '.marketing-juridico', 'ferramentas');
  let baixado = null; try { baixado = JSON.parse(fs.readFileSync(path.join(ferr, 'caminhos.json'), 'utf8')).chrome; } catch (e) {}
  const op = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    path.join(pf, 'Google/Chrome/Application/chrome.exe'), path.join(pf86, 'Google/Chrome/Application/chrome.exe'),
    path.join(local, 'Google/Chrome/Application/chrome.exe'), path.join(pf86, 'Microsoft/Edge/Application/msedge.exe'),
    path.join(pf, 'Microsoft/Edge/Application/msedge.exe'), '/usr/bin/google-chrome', baixado];
  const c = op.find(p => p && fs.existsSync(p));
  if (!c) throw new Error('navegador não encontrado: instale o Google Chrome ou rode o instalador da Ilha de edição');
  return c;
}

// tira o que cobriria o texto: barras grudadas, janelas de notificação, cookies e consentimento
async function limpar(pg) {
  await pg.evaluate(() => {
    const suspeito = /onesignal|notif|push|modal|popup|pop-up|cookie|consent|lgpd|gdpr|banner|overlay|newsletter|paywall|slidedown/i;
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el), r = el.getBoundingClientRect();
      const fixo = cs.position === 'fixed' || cs.position === 'sticky';
      const flutua = cs.position === 'absolute' && (+cs.zIndex || 0) >= 100;
      const nome = (el.id || '') + ' ' + (typeof el.className === 'string' ? el.className : '');
      const dialogo = /dialog/.test(el.getAttribute('role') || '') || el.getAttribute('aria-modal') === 'true' || el.tagName === 'DIALOG';
      const texto = (el.innerText || '').slice(0, 200);
      if ((fixo && r.height < innerHeight * 0.6) || dialogo || ((fixo || flutua) && suspeito.test(nome))
          || ((fixo || flutua) && /receber notifica|aceito|aceitar cookies|permitir notifica/i.test(texto)))
        el.style.setProperty('display', 'none', 'important');
    }
    document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
  });
}

(async () => {
  fs.mkdirSync(pasta, { recursive: true });
  const nav = await puppeteer.launch({ executablePath: chrome(), headless: true, args: ['--hide-scrollbars', '--force-color-profile=srgb'] });
  try {
    const pg = await nav.newPage();
    await pg.setViewport({ width: 430, height: 900, deviceScaleFactor: 2.5 });
    await pg.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
    await pg.goto(endereco, { waitUntil: 'networkidle2', timeout: 60000 });
    await new Promise(r => setTimeout(r, 3500));          // espera os avisos que aparecem depois (notificações, cookies)
    await limpar(pg);
    const r = await pg.evaluate(trechos => {
      // texto da página com o mapa de volta para cada nó, espaços normalizados
      const nos = [], mapa = []; let texto = '';
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const n = w.currentNode, v = n.nodeValue; if (!v.trim() || !n.parentElement.offsetParent) continue;
        for (let i = 0; i < v.length; i++) {
          const c = /\s/.test(v[i]) ? ' ' : v[i];
          if (c === ' ' && texto.endsWith(' ')) continue;
          texto += c; mapa.push([n, i]);
        }
        if (!texto.endsWith(' ')) { texto += ' '; mapa.push([n, v.length]); }
      }
      const baixo = texto.toLowerCase();
      return trechos.map(t => {
        const alvo = t.replace(/\s+/g, ' ').trim().toLowerCase(), i = baixo.indexOf(alvo);
        if (i < 0) return { trecho: t, achado: false, retangulos: [] };
        const rg = document.createRange();
        rg.setStart(mapa[i][0], mapa[i][1]); const f = mapa[i + alvo.length - 1]; rg.setEnd(f[0], f[1] + 1);
        const el = rg.startContainer.parentElement; el.scrollIntoView({ block: 'center' });
        const y0 = scrollY;
        return { trecho: t, achado: true, retangulos: [...rg.getClientRects()].filter(q => q.width > 2).map(q => ({ x: q.left, y: q.top + y0, w: q.width, h: q.height })) };
      });
    }, trechos);
    const achados = r.filter(g => g.achado);
    if (!achados.length) { console.error('nenhum trecho encontrado na página:', trechos.join(' | ')); process.exit(3); }
    // enquadra do primeiro ao último trecho, com folga em cima e embaixo
    const ys = achados.flatMap(g => g.retangulos.flatMap(q => [q.y, q.y + q.h]));
    const topo = Math.max(0, Math.min(...ys) - 260), alt = Math.max(560, Math.max(...ys) - topo + 260);
    await pg.evaluate(y => window.scrollTo(0, y), topo); await new Promise(r => setTimeout(r, 400));
    const y0 = await pg.evaluate(() => scrollY);
    await pg.setViewport({ width: 430, height: Math.ceil(alt), deviceScaleFactor: 2.5 });
    await pg.evaluate(y => window.scrollTo(0, y), y0); await new Promise(r => setTimeout(r, 400));
    const yReal = await pg.evaluate(() => scrollY);
    await limpar(pg);                                        // de novo: alguns avisos só aparecem depois da rolagem
    await pg.screenshot({ path: path.join(pasta, nome + '.png') });
    const k = 2.5, url = new URL(endereco), hoje = new Date();
    const saida = {
      endereco, site: url.hostname.replace(/^www\./, ''), titulo: await pg.title(),
      acesso: `${String(hoje.getDate()).padStart(2, '0')}/${String(hoje.getMonth() + 1).padStart(2, '0')}/${hoje.getFullYear()}`,
      imagem: nome + '.png',
      grifos: r.map(g => ({ trecho: g.trecho, achado: g.achado, retangulos: g.retangulos.map(q => ({ x: q.x * k, y: (q.y - yReal) * k, w: q.w * k, h: q.h * k })) }))
    };
    fs.writeFileSync(path.join(pasta, nome + '.json'), JSON.stringify(saida, null, 1));
    for (const g of r) console.log(g.achado ? 'achado' : 'NÃO ACHADO', '|', g.trecho);
    console.log('imagem', path.join(pasta, nome + '.png'));
  } finally { await nav.close(); }
})().catch(e => { console.error(e.message); process.exit(1); });
