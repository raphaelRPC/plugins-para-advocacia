import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { lerCatalogo } from './lib/catalogo.mjs';
import { proximaVersao, acrescentarLinha, fecharVersao, notasDaVersao } from './lib/versao.mjs';

const raiz = join(import.meta.dirname, '..');
const arqCatalogo = join(raiz, '.claude-plugin', 'marketplace.json');
const arqChangelog = join(raiz, 'CHANGELOG.md');
const [acao, ...args] = process.argv.slice(2);
const json = (obj) => JSON.stringify(obj, null, 2) + '\n';

try {
  if (acao === 'subir') {
    const [nome, tipo, texto] = args;
    if (!texto) throw new Error('uso: versao.mjs subir <plugin> <patch|minor|major> "<o que mudou>"');
    const { plugins } = lerCatalogo(raiz);
    const p = plugins.find(x => x.nome === nome);
    if (!p) throw new Error(`plugin "${nome}" não está no catálogo`);
    const nova = proximaVersao(p.versao, tipo);
    const arqPlugin = join(p.dir, '.claude-plugin', 'plugin.json');
    const manifesto = JSON.parse(readFileSync(arqPlugin, 'utf8'));
    manifesto.version = nova;
    writeFileSync(arqPlugin, json(manifesto));
    writeFileSync(arqChangelog, acrescentarLinha(readFileSync(arqChangelog, 'utf8'), `- \`${nome}\` ${nova}: ${texto}`));
    console.log(`${nome}: ${p.versao} → ${nova}`);
  } else if (acao === 'fechar') {
    const [versao] = args;
    if (!/^\d+\.\d+\.\d+$/.test(versao ?? '')) throw new Error('uso: versao.mjs fechar X.Y.Z');
    const hoje = new Date().toLocaleDateString('sv');
    writeFileSync(arqChangelog, fecharVersao(readFileSync(arqChangelog, 'utf8'), versao, hoje));
    const { dados } = lerCatalogo(raiz);
    dados.metadata.version = versao;
    writeFileSync(arqCatalogo, json(dados));
    console.log(`Pacote ${versao} fechado. Próximo: commit, tag v${versao} e push da tag.`);
  } else if (acao === 'notas') {
    process.stdout.write(notasDaVersao(readFileSync(arqChangelog, 'utf8'), args[0]) + '\n');
  } else {
    throw new Error('ações: subir, fechar, notas');
  }
} catch (e) {
  console.error(`ERRO: ${e.message}`);
  process.exit(1);
}
