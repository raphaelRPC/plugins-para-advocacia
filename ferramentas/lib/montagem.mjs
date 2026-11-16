import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { listarArquivos } from './arquivos.mjs';
import { ehTextoNormalizavel, paraLF } from './texto.mjs';
import { criarZip } from './zip.mjs';
import { lerCatalogo } from './catalogo.mjs';
import { lerEdicoes, habilidadesDaEdicao, arquivosDaEdicao } from './edicoes.mjs';

export function zipDoPlugin(plugin, permitidas) {
  const arquivos = arquivosDaEdicao(listarArquivos(plugin.dir), permitidas);
  return criarZip(arquivos.map(rel => {
    const dados = readFileSync(join(plugin.dir, rel));
    return { caminho: rel, dados: ehTextoNormalizavel(rel) ? paraLF(dados) : dados, executavel: /\.(sh|py)$/.test(rel) };
  }));
}

export function montar(raiz, versao, saida) {
  rmSync(saida, { recursive: true, force: true });
  mkdirSync(join(saida, 'plugins'), { recursive: true });
  const config = lerEdicoes(raiz);
  const { plugins } = lerCatalogo(raiz);
  const gerados = [];
  const porEdicao = Object.fromEntries(config.edicoes.map(e => [e, []]));
  const gravar = (rel, dados) => { writeFileSync(join(saida, rel), dados); gerados.push(rel); };

  for (const p of plugins) {
    if (config.plugins[p.nome]) {
      for (const e of config.edicoes) {
        const rel = `plugins/${p.nome}-${p.versao}-${e}.zip`;
        gravar(rel, zipDoPlugin(p, habilidadesDaEdicao(config, p.nome, e)));
        porEdicao[e].push(rel);
      }
    } else {
      const rel = `plugins/${p.nome}-${p.versao}.zip`;
      gravar(rel, zipDoPlugin(p, null));
      for (const e of config.edicoes) porEdicao[e].push(rel);
    }
  }

  const leiaMe = paraLF(readFileSync(join(raiz, 'guia', 'comece-aqui.md')));
  for (const e of config.edicoes) {
    gravar(`plugins-para-advocacia-v${versao}-${e}.zip`, criarZip([
      { caminho: 'LEIA-ME.md', dados: leiaMe },
      ...porEdicao[e].map(rel => ({ caminho: rel, dados: readFileSync(join(saida, rel)) })),
    ]));
  }

  const somas = gerados.map(rel => `${createHash('sha256').update(readFileSync(join(saida, rel))).digest('hex')}  ${rel}`);
  writeFileSync(join(saida, 'SHA256SUMS.txt'), somas.join('\n') + '\n');
  return gerados;
}
