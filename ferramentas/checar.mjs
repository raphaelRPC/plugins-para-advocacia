import { join } from 'node:path';
import { checarTudo } from './lib/regras.mjs';

const raiz = join(import.meta.dirname, '..');
const erros = checarTudo(raiz);
if (erros.length) {
  console.error(`ERRO: ${erros.length} problema(s)\n` + erros.map(e => `- ${e}`).join('\n'));
  process.exit(1);
}
console.log('Tudo certo.');
