import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { listarArquivos } from './arquivos.mjs';
import { ehTextoNormalizavel, paraLF } from './texto.mjs';

function conteudo(raiz, rel) {
  const dados = readFileSync(join(raiz, rel));
  return ehTextoNormalizavel(rel) ? paraLF(dados) : dados;
}

export function encontrarRepetidos(raiz, tamanhoMinimo = 200) {
  const porHash = new Map();
  for (const rel of listarArquivos(join(raiz, 'plugins')).map(r => `plugins/${r}`)) {
    if (statSync(join(raiz, rel)).size < tamanhoMinimo) continue;
    const hash = createHash('sha1').update(conteudo(raiz, rel)).digest('hex');
    porHash.set(hash, [...(porHash.get(hash) ?? []), rel]);
  }
  return [...porHash.values()].filter(g => g.length > 1).map(g => g.sort()).sort((a, b) => a[0].localeCompare(b[0]));
}

export function gerarMapa(grupos) {
  return {
    grupos: grupos.map(destinos => {
      const gruposDosPlugins = new Set(destinos.map(d => d.split('/')[1]));
      const grupo = gruposDosPlugins.size === 1 ? [...gruposDosPlugins][0] : 'geral';
      const dentroDoPlugin = destinos[0].split('/').slice(3).join('/');
      return { fonte: `compartilhado/${grupo}/${dentroDoPlugin}`, destinos };
    }),
  };
}

export function divergencias(raiz, mapa) {
  const saida = [];
  for (const { fonte, destinos } of mapa.grupos) {
    if (!existsSync(join(raiz, fonte))) { saida.push(`${fonte} não existe`); continue; }
    const original = conteudo(raiz, fonte);
    for (const d of destinos) {
      if (!existsSync(join(raiz, d))) saida.push(`${d} não existe (deveria ser cópia de ${fonte})`);
      else if (!conteudo(raiz, d).equals(original)) saida.push(`${d} difere de ${fonte}`);
    }
  }
  return saida;
}

export function pluginsAfetados(raiz, mapa) {
  const nomes = new Set();
  for (const { fonte, destinos } of mapa.grupos) {
    if (!existsSync(join(raiz, fonte))) continue;
    const original = conteudo(raiz, fonte);
    for (const d of destinos) {
      if (!existsSync(join(raiz, d)) || !conteudo(raiz, d).equals(original)) nomes.add(d.split('/')[2]);
    }
  }
  return [...nomes].sort();
}

export function aplicar(raiz, mapa) {
  let copiados = 0;
  for (const { fonte, destinos } of mapa.grupos) {
    const original = conteudo(raiz, fonte);
    for (const d of destinos) {
      if (existsSync(join(raiz, d)) && conteudo(raiz, d).equals(original)) continue;
      mkdirSync(dirname(join(raiz, d)), { recursive: true });
      writeFileSync(join(raiz, d), original);
      copiados++;
    }
  }
  return copiados;
}

export function lerMapa(raiz) {
  return JSON.parse(readFileSync(join(raiz, 'compartilhado', 'mapa.json'), 'utf8'));
}
