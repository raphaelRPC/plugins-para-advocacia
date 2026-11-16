// Gravador da camada animada: abre um modelo de assets/animacoes/ no Chrome sem janela,
// desenha cada quadro a partir do tempo (window.desenhar(t)) e salva PNG com fundo transparente.
//
// Uso: node animar.js <modelo> <dados.json> <pasta_saida> <duracao_s> [fps]
//      (<modelo> é o nome de um modelo do plugin, ex. trilha, ou o caminho de um .html feito sob encomenda)
//      node animar.js <modelo> <dados.json> <pasta_saida> --tempos 0.5,1.2,3.0
//      node animar.js cenas <dados.json> <pasta_saida> --regua   (só lê a régua de leitura do vídeo sem rosto e grava regua.json)
// Precisa de: Google Chrome instalado (ou CHROME_PATH) e, na pasta de trabalho, os pacotes
// puppeteer-core e three (NODE_PATH aponta para o node_modules da pasta de trabalho).
// Saída: quadro_00000.png ... e area.json (recorte {x, y, w, h} no quadro de 1080 x 1920).

const fs = require('fs'), path = require('path'), http = require('http');
const puppeteer = require('puppeteer-core');

const [modelo, arqDados, saida, ...resto] = process.argv.slice(2);
const ANIM = path.join(__dirname, '..', 'assets', 'animacoes');
const PROPRIO = modelo.endsWith('.html');                    // modelo sob encomenda, fora do plugin
const RAIZ = PROPRIO ? path.dirname(path.resolve(modelo)) : ANIM;
const NOME = PROPRIO ? path.basename(modelo, '.html') : modelo;
const THREE = path.dirname(path.dirname(require.resolve('three')));   // .../node_modules/three
const dados = JSON.parse(fs.readFileSync(arqDados, 'utf8'));
const MIDIA = dados.pastaMidia ? path.resolve(dados.pastaMidia) : null;

let tempos;
const REGUA = resto[0] === '--regua';
if (REGUA) tempos = [];
else if (resto[0] === '--tempos') tempos = resto[1].split(',').map(Number);
else { const dur = parseFloat(resto[0]), fps = parseFloat(resto[1] || '30'); tempos = []; for (let i = 0; i < Math.ceil(dur * fps); i++) tempos.push(i / fps); }

const TIPOS = { '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.css': 'text/css', '.json': 'application/json' };
function servir(raizes) {
  // servidor local só com as pastas permitidas: modelos, three e a mídia do projeto
  return http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    if (url === '/base.js') { res.writeHead(200, { 'Content-Type': TIPOS['.js'] }); return fs.createReadStream(path.join(ANIM, 'base.js')).pipe(res); }
    for (const [pref, raiz] of raizes) {
      if (!raiz || !url.startsWith(pref)) continue;
      const arq = path.join(raiz, url.slice(pref.length));
      if (!arq.startsWith(raiz) || !fs.existsSync(arq) || fs.statSync(arq).isDirectory()) break;
      res.writeHead(200, { 'Content-Type': TIPOS[path.extname(arq)] || 'application/octet-stream' });
      return fs.createReadStream(arq).pipe(res);
    }
    res.writeHead(404); res.end();
  });
}

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

(async () => {
  fs.mkdirSync(saida, { recursive: true });
  const FONTES = path.join(process.env.MJ_FERRAMENTAS || path.join(require('os').homedir(), '.marketing-juridico', 'ferramentas'), 'fontes');
  const srv = servir([['/three/', THREE], ['/midia/', MIDIA], ['/fontes/', FONTES], ['/', RAIZ]]);
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const porta = srv.address().port;
  const nav = await puppeteer.launch({ executablePath: chrome(), headless: true,
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--hide-scrollbars', '--force-color-profile=srgb'] });
  try {
    const pg = await nav.newPage();
    pg.on('pageerror', e => console.error('erro no modelo:', e.message));
    await pg.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
    await pg.evaluateOnNewDocument(d => { window.DADOS = d; }, dados);
    await pg.goto(`http://127.0.0.1:${porta}/${NOME}.html`, { waitUntil: 'load' });
    await pg.waitForFunction('window.PRONTO === true', { timeout: 30000 });
    if (REGUA) {
      const r = await pg.evaluate(() => window.REGUA || null);
      fs.writeFileSync(path.join(saida, 'regua.json'), JSON.stringify(r));
      console.log('régua', r ? r.total + ' s' : 'ausente');
      return;
    }
    const area = await pg.evaluate(() => window.AREA || { x: 0, y: 0, w: 1080, h: 1920 });
    fs.writeFileSync(path.join(saida, 'area.json'), JSON.stringify(area));
    for (let i = 0; i < tempos.length; i++) {
      await pg.evaluate(t => window.desenhar(t), tempos[i]);
      await pg.screenshot({ path: path.join(saida, `quadro_${String(i).padStart(5, '0')}.png`), omitBackground: true,
        clip: { x: area.x, y: area.y, width: area.w, height: area.h } });
    }
    console.log('quadros', tempos.length, 'área', JSON.stringify(area));
  } finally { await nav.close(); srv.close(); }
})().catch(e => { console.error(e.message); process.exit(1); });
