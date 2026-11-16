import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { lerCatalogo } from './catalogo.mjs';

const CABECALHO = '## [Não publicado]';

export function proximaVersao(atual, tipo) {
  const m = atual.match(/^(\d+)\.(\d+)\.(\d+)$/);
  if (!m) throw new Error(`Versão inválida: ${atual}`);
  const [ma, mi, pa] = m.slice(1).map(Number);
  if (tipo === 'major') return `${ma + 1}.0.0`;
  if (tipo === 'minor') return `${ma}.${mi + 1}.0`;
  if (tipo === 'patch') return `${ma}.${mi}.${pa + 1}`;
  throw new Error(`Tipo inválido: ${tipo} (use patch, minor ou major)`);
}

function partes(texto) {
  const i = texto.indexOf(CABECALHO);
  if (i < 0) throw new Error(`CHANGELOG sem "${CABECALHO}"`);
  const depois = texto.slice(i + CABECALHO.length);
  const proxima = depois.search(/\n## \[/);
  const corpo = proxima < 0 ? depois : depois.slice(0, proxima);
  return { antes: texto.slice(0, i), linhas: corpo.split('\n').filter(l => l.trim()), resto: proxima < 0 ? '' : depois.slice(proxima + 1) };
}

export function acrescentarLinha(texto, linha) {
  const { antes, linhas, resto } = partes(texto);
  return `${antes}${CABECALHO}\n\n${[...linhas, linha].join('\n')}\n\n${resto}`;
}

export function fecharVersao(texto, versao, data) {
  const { antes, linhas, resto } = partes(texto);
  if (!linhas.length) throw new Error('Nada em "Não publicado": suba a versão de algum plugin antes de fechar.');
  if (texto.includes(`## [${versao}]`)) throw new Error(`A versão ${versao} já existe no CHANGELOG`);
  return `${antes}${CABECALHO}\n\n## [${versao}] - ${data}\n\n${linhas.join('\n')}\n\n${resto}`;
}

export function notasDaVersao(texto, versao) {
  const i = texto.indexOf(`## [${versao}]`);
  if (i < 0) throw new Error(`A versão ${versao} não está no CHANGELOG`);
  const corpo = texto.slice(i).split('\n').slice(1);
  const fim = corpo.findIndex(l => l.startsWith('## ['));
  return (fim < 0 ? corpo : corpo.slice(0, fim)).filter(l => l.trim()).join('\n');
}

export function conferirTag(raiz, tag) {
  if (!tag.startsWith('v')) return [`a tag ${tag} precisa começar com "v" (exemplo: v1.1.0)`];
  const versao = tag.slice(1);
  const erros = [];
  const pacote = lerCatalogo(raiz).dados.metadata?.version;
  if (pacote !== versao) erros.push(`tag ${tag}, mas o marketplace.json diz ${pacote}`);
  try { notasDaVersao(readFileSync(join(raiz, 'CHANGELOG.md'), 'utf8'), versao); } catch (e) { erros.push(e.message); }
  return erros;
}
