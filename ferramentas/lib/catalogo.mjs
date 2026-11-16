import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

export function lerCatalogo(raiz) {
  const dados = JSON.parse(readFileSync(join(raiz, '.claude-plugin', 'marketplace.json'), 'utf8'));
  const plugins = dados.plugins.map(p => {
    const partes = p.source.replace(/^\.\//, '').split('/');
    const dir = join(raiz, p.source);
    const arquivo = join(dir, '.claude-plugin', 'plugin.json');
    const versao = existsSync(arquivo) ? JSON.parse(readFileSync(arquivo, 'utf8')).version ?? null : null;
    return { nome: p.name, versao, source: p.source, dir, grupo: partes[0] === 'plugins' && partes.length === 3 ? partes[1] : null };
  });
  return { dados, plugins };
}
