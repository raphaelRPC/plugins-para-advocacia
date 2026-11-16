import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { lerCatalogo } from './catalogo.mjs';

// O README é o que o advogado e o Claude dele leem primeiro: versões e contagens não podem ficar velhas.
export function conferirReadme(texto, plugins, versaoPacote) {
  const erros = [];
  if (!texto.includes(`**${versaoPacote}**`)) erros.push(`README.md: não mostra a versão do pacote **${versaoPacote}**`);
  const total = plugins.reduce((soma, p) => soma + p.habilidades, 0);
  const resumo = `${plugins.length} plugins · ${total} habilidades`;
  if (!texto.includes(resumo)) erros.push(`README.md: o resumo do topo deveria dizer "${resumo}"`);
  for (const p of plugins) {
    const linha = texto.split('\n').find(l => l.startsWith(`| [\`${p.nome}\`]`));
    if (!linha) { erros.push(`README.md: ${p.nome} não está na tabela "Os plugins"`); continue; }
    const [, versao, habilidades] = linha.split('|').map(c => c.trim()).slice(1);
    if (versao !== p.versao) erros.push(`README.md: ${p.nome} aparece com versão ${versao}, mas o plugin.json diz ${p.versao}`);
    if (Number(habilidades) !== p.habilidades) erros.push(`README.md: ${p.nome} aparece com ${habilidades} habilidades, mas tem ${p.habilidades}`);
  }
  return erros;
}

export function atualizarVersaoDoPlugin(texto, nome, versao) {
  return texto.split('\n').map(l => {
    if (!l.startsWith(`| [\`${nome}\`]`)) return l;
    const celulas = l.split('|');
    celulas[2] = ` ${versao} `;
    return celulas.join('|');
  }).join('\n');
}

export function atualizarVersaoDoPacote(texto, antiga, nova) {
  return texto.replace(`**${antiga}**`, `**${nova}**`);
}

export function regraReadme(raiz) {
  const arquivo = join(raiz, 'README.md');
  if (!existsSync(arquivo)) return ['README.md não existe'];
  const { dados, plugins } = lerCatalogo(raiz);
  const lista = plugins.filter(p => existsSync(p.dir)).map(p => ({
    nome: p.nome,
    versao: p.versao,
    habilidades: existsSync(join(p.dir, 'skills'))
      ? readdirSync(join(p.dir, 'skills'), { withFileTypes: true }).filter(d => d.isDirectory()).length
      : 0,
  }));
  return conferirReadme(readFileSync(arquivo, 'utf8'), lista, dados.metadata?.version);
}
