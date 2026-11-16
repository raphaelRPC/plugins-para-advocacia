import { join } from 'node:path';
import { lerMapa, divergencias, aplicar } from './lib/compartilhado.mjs';

const raiz = join(import.meta.dirname, '..');
const mapa = lerMapa(raiz);
if (process.argv.includes('--verificar')) {
  const lista = divergencias(raiz, mapa);
  if (lista.length) {
    console.error('ERRO: cópias diferentes da fonte em compartilhado/. Edite a fonte e rode "npm run sincronizar".\n' + lista.map(l => `- ${l}`).join('\n'));
    process.exit(1);
  }
  console.log('Cópias iguais à fonte.');
} else {
  console.log(`${aplicar(raiz, mapa)} arquivo(s) atualizado(s).`);
}
