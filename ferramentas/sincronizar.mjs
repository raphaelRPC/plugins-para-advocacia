import { join } from 'node:path';
import { lerMapa, divergencias, aplicar, pluginsAfetados } from './lib/compartilhado.mjs';

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
  const afetados = pluginsAfetados(raiz, mapa);
  console.log(`${aplicar(raiz, mapa)} arquivo(s) atualizado(s).`);
  if (afetados.length) {
    console.log(`Plugins que receberam arquivo alterado: ${afetados.join(', ')}.`);
    console.log('Lembrete: rode "node ferramentas/versao.mjs subir <plugin> patch \"<o que mudou>\"" para cada um.');
  }
}
