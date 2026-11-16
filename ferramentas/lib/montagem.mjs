import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, resolve, relative, isAbsolute } from 'node:path';
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

export function conferirSaida(raiz, saida) {
  const alvo = resolve(saida);
  const dentro = relative(alvo, resolve(raiz));
  if (dentro === '' || (!dentro.startsWith('..') && !isAbsolute(dentro))) {
    throw new Error(`a pasta de saída (${alvo}) é o repositório ou uma pasta que o contém; escolha outra, por exemplo dist`);
  }
  if (!existsSync(alvo)) return alvo;
  if (!statSync(alvo).isDirectory()) throw new Error(`${alvo} existe e não é uma pasta`);
  const conteudo = readdirSync(alvo);
  if (conteudo.includes('.git') || conteudo.includes('.claude-plugin')) {
    throw new Error(`${alvo} parece ser um repositório ou plugin (tem .git ou .claude-plugin); escolha outra pasta`);
  }
  if (conteudo.length > 0 && !conteudo.includes('SHA256SUMS.txt')) {
    throw new Error(`${alvo} já tem arquivos que não são de uma montagem anterior; escolha uma pasta vazia ou nova`);
  }
  return alvo;
}

export function montar(raiz, versao, saidaPedida) {
  const config = lerEdicoes(raiz);
  const { plugins } = lerCatalogo(raiz);
  const saida = conferirSaida(raiz, saidaPedida);
  rmSync(saida, { recursive: true, force: true });
  mkdirSync(join(saida, 'plugins'), { recursive: true });
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
