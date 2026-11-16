import { join, resolve } from 'node:path';
import { montar } from './lib/montagem.mjs';

const args = process.argv.slice(2);
const valor = (nome) => { const i = args.indexOf(nome); return i >= 0 ? args[i + 1] : undefined; };
const versao = valor('--versao');
if (!versao || !/^\d+\.\d+\.\d+(-[\w.]+)?$/.test(versao)) {
  console.error('ERRO: use --versao X.Y.Z (sem o "v"). Exemplo: npm run zips -- --versao 1.1.0');
  process.exit(1);
}
const raiz = join(import.meta.dirname, '..');
const saida = resolve(valor('--saida') ?? join(raiz, 'dist'));
const gerados = montar(raiz, versao, saida);
console.log(`${gerados.length} zips em ${saida}`);
