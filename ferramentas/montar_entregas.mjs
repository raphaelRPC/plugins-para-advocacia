import { join, resolve } from 'node:path';
import { montarTodas } from './lib/entregas.mjs';

const args = process.argv.slice(2);
const falha = (msg) => { console.error(`ERRO: ${msg}`); process.exit(1); };
const valor = (nome) => {
  const i = args.indexOf(nome);
  if (i < 0) return undefined;
  const v = args[i + 1];
  if (!v || v.startsWith('--')) falha(`${nome} precisa de um valor logo depois`);
  return v;
};
const versao = valor('--versao');
if (!versao || !/^\d+\.\d+\.\d+(-[\w.]+)?$/.test(versao)) {
  falha('use --versao X.Y.Z (sem o "v"). Exemplo: npm run entregas -- --versao 1.2.0');
}
const raiz = join(import.meta.dirname, '..');
const saida = resolve(valor('--saida') ?? join(raiz, 'entregas-geradas'));
let resultado;
try { resultado = montarTodas(raiz, versao, saida, valor('--ticket')); } catch (e) { falha(e.message); }
let problemas = 0;
for (const r of resultado) {
  console.log(`${r.ticket}: ${r.plugins} plugins, ${r.habilidades} habilidades (promessa ${r.promessa}) → ${r.repositorio}`);
  for (const e of r.erros) console.error(`  ERRO: ${e}`);
  problemas += r.erros.length;
}
console.log(`Entregas em ${saida}. Relatório de citações em <ticket>/relatorio-de-referencias.md`);
if (problemas) falha(`${problemas} problema(s) nas entregas; nada deve ser publicado`);
