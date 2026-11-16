import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export function lerEdicoes(raiz) {
  return JSON.parse(readFileSync(join(raiz, 'edicoes.json'), 'utf8'));
}

export function habilidadesDaEdicao(config, plugin, edicao) {
  const indice = config.edicoes.indexOf(edicao);
  if (indice < 0) throw new Error(`Edição desconhecida: ${edicao}`);
  const p = config.plugins[plugin];
  if (!p) return null;
  return new Set(config.edicoes.slice(0, indice + 1).flatMap(e => p[e] ?? []));
}

export function arquivosDaEdicao(arquivos, permitidas) {
  if (!permitidas) return arquivos;
  return arquivos.filter(a => {
    const m = a.match(/^skills\/([^/]+)\//);
    return !m || permitidas.has(m[1]);
  });
}

export function conferirEdicoes(config, habilidadesPorPlugin) {
  const erros = [];
  for (const [plugin, porEdicao] of Object.entries(config.plugins)) {
    const existentes = new Set(habilidadesPorPlugin[plugin] ?? []);
    const vistas = new Map();
    for (const e of config.edicoes) for (const h of porEdicao[e] ?? []) vistas.set(h, (vistas.get(h) ?? 0) + 1);
    for (const [h, n] of vistas) {
      if (n > 1) erros.push(`${plugin}: "${h}" aparece em mais de uma edição`);
      if (!existentes.has(h)) erros.push(`${plugin}: "${h}" está em edicoes.json mas não existe`);
    }
    for (const h of existentes) if (!vistas.has(h)) erros.push(`${plugin}: "${h}" não está em nenhuma edição`);
  }
  return erros;
}
