import { writeFileSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { encontrarRepetidos, gerarMapa } from './lib/compartilhado.mjs';

const raiz = join(import.meta.dirname, '..');
const grupos = encontrarRepetidos(raiz);
for (const g of grupos) console.log(`${g.length}x\n  ${g.join('\n  ')}`);

if (process.argv.includes('--gerar-mapa')) {
  const arquivoMapa = join(raiz, 'compartilhado', 'mapa.json');
  if (existsSync(arquivoMapa)) { console.error('ERRO: compartilhado/mapa.json já existe. Edite à mão para acrescentar grupos.'); process.exit(1); }
  const mapa = gerarMapa(grupos);
  const fontes = new Set();
  for (const { fonte, destinos } of mapa.grupos) {
    if (fontes.has(fonte)) { console.error(`ERRO: dois grupos diferentes iriam para ${fonte}`); process.exit(1); }
    fontes.add(fonte);
    mkdirSync(dirname(join(raiz, fonte)), { recursive: true });
    copyFileSync(join(raiz, destinos[0]), join(raiz, fonte));
  }
  writeFileSync(arquivoMapa, JSON.stringify(mapa, null, 2) + '\n');
  console.log(`\n${mapa.grupos.length} grupos gravados em compartilhado/mapa.json`);
}
