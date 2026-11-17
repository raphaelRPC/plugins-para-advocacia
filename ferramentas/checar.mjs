import { join } from 'node:path';
import { checarTudo } from './lib/regras.mjs';
import { conferirTag } from './lib/versao.mjs';
import { regraTickets } from './lib/entregas.mjs';

const raiz = join(import.meta.dirname, '..');
const erros = [...checarTudo(raiz), ...regraTickets(raiz)];
const i = process.argv.indexOf('--tag');
if (i >= 0) erros.push(...conferirTag(raiz, process.argv[i + 1] ?? ''));
if (erros.length) {
  console.error(`ERRO: ${erros.length} problema(s)\n` + erros.map(e => `- ${e}`).join('\n'));
  process.exit(1);
}
console.log('Tudo certo.');
