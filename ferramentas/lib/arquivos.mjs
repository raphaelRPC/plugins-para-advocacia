import { readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const IGNORAR = new Set(['.git', '.DS_Store', '__pycache__', 'node_modules']);

export function listarArquivos(raiz) {
  const saida = [];
  (function andar(dir) {
    for (const nome of readdirSync(dir).sort()) {
      if (IGNORAR.has(nome) || nome.endsWith('.pyc')) continue;
      const caminho = join(dir, nome);
      if (statSync(caminho).isDirectory()) andar(caminho);
      else saida.push(relative(raiz, caminho).split(sep).join('/'));
    }
  })(raiz);
  return saida;
}
