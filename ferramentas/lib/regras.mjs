import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, basename, dirname } from 'node:path';
import { listarArquivos } from './arquivos.mjs';
import { lerCatalogo } from './catalogo.mjs';
import { lerFrontmatter } from './frontmatter.mjs';
import { regraReadme } from './readme.mjs';
import { lerEdicoes, conferirEdicoes, habilidadesDaEdicao, arquivosDaEdicao } from './edicoes.mjs';

const GRUPOS_COM_REGRA_DE_TEXTO = new Set(['fundacao', 'motores']);
const PROIBIDAS = /\b(evento|aulas?|nivelamento|apostila|alunos?|ADV 6|RPC)\b/i;
const TRACOS = /[—–]/;
const TEXTO = /\.(md|txt|json|py|sh|html|csv|tsv|yml|yaml)$/i;

const ler = (p, rel) => readFileSync(join(p.dir, rel), 'utf8');

export function regraCatalogo(raiz) {
  const erros = [];
  const { dados, plugins } = lerCatalogo(raiz);
  if (!dados.metadata?.version) erros.push('marketplace.json sem metadata.version');
  plugins.forEach((p, i) => {
    const entrada = dados.plugins[i];
    if ('version' in entrada) erros.push(`${p.nome}: marketplace.json não deve ter "version" (a versão fica só no plugin.json)`);
    const arq = join(p.dir, '.claude-plugin', 'plugin.json');
    if (!existsSync(arq)) { erros.push(`${p.nome}: ${p.source} sem .claude-plugin/plugin.json`); return; }
    const manifesto = JSON.parse(readFileSync(arq, 'utf8'));
    if (manifesto.name !== p.nome) erros.push(`${p.nome}: plugin.json diz name "${manifesto.name}"`);
    if (!manifesto.version) erros.push(`${p.nome}: plugin.json sem version`);
    if (!p.grupo) erros.push(`${p.nome}: source fora de plugins/<grupo>/<nome>`);
    else if (entrada.category !== p.grupo) erros.push(`${p.nome}: category "${entrada.category}" diferente da pasta (${p.grupo})`);
  });
  return erros;
}

export function regraHabilidades(p) {
  const erros = [];
  for (const rel of listarArquivos(p.dir).filter(r => /^skills\/[^/]+\/SKILL\.md$/.test(r))) {
    const pasta = basename(dirname(rel));
    const fm = lerFrontmatter(ler(p, rel));
    if (!fm) { erros.push(`${p.nome}: skills/${pasta} sem frontmatter`); continue; }
    if (fm.name !== pasta) erros.push(`${p.nome}: skills/${pasta} tem name "${fm.name}"`);
    if (!fm.description) erros.push(`${p.nome}: skills/${pasta} sem description`);
    else if (fm.description.length > 1024) erros.push(`${p.nome}: skills/${pasta} description com ${fm.description.length} caracteres (máximo 1024)`);
    if (fm.description && /[<>]/.test(fm.description)) erros.push(`${p.nome}: skills/${pasta} description com < ou > (o app do Claude recusa o zip: "cannot contain XML tags")`);
  }
  return erros;
}

export function regraReferencias(p) {
  const erros = [];
  for (const rel of listarArquivos(p.dir).filter(r => /\.(md|json|sh|py)$/.test(r))) {
    for (const m of ler(p, rel).matchAll(/\$\{CLAUDE_PLUGIN_ROOT\}\/([A-Za-z0-9_.\/-]+)/g)) {
      const alvo = m[1].replace(/[.,]+$/, '').replace(/\/+$/, '');
      if (alvo && !existsSync(join(p.dir, alvo))) erros.push(`${p.nome}: ${rel} cita \${CLAUDE_PLUGIN_ROOT}/${alvo}, que não existe`);
    }
  }
  return erros;
}

export function regraTexto(p) {
  if (!GRUPOS_COM_REGRA_DE_TEXTO.has(p.grupo)) return [];
  const erros = [];
  for (const rel of listarArquivos(p.dir).filter(r => TEXTO.test(r))) {
    const linhas = ler(p, rel).split('\n');
    linhas.forEach((linha, i) => {
      if (TRACOS.test(linha)) erros.push(`${p.nome}: ${rel}:${i + 1} tem travessão ou meia-risca`);
      const m = linha.match(PROIBIDAS);
      if (m) erros.push(`${p.nome}: ${rel}:${i + 1} tem a palavra "${m[0]}"`);
    });
  }
  return erros;
}

export function regraFimDeLinha(p) {
  return listarArquivos(p.dir)
    .filter(r => r.endsWith('.sh') && readFileSync(join(p.dir, r)).includes('\r\n'))
    .map(r => `${p.nome}: ${r} tem CRLF (o script quebra no Mac e no Linux)`);
}

export function regraEdicoes(raiz) {
  const config = lerEdicoes(raiz);
  const { plugins } = lerCatalogo(raiz);
  const habilidades = {};
  for (const p of plugins) {
    if (!config.plugins[p.nome]) continue;
    habilidades[p.nome] = readdirSync(join(p.dir, 'skills'), { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
  }
  const semPlugin = Object.keys(config.plugins).filter(n => !habilidades[n]).map(n => `edicoes.json cita o plugin "${n}", que não está no catálogo`);
  return [...semPlugin, ...conferirEdicoes(config, habilidades)];
}

export function regraReferenciasPorEdicao(raiz) {
  const erros = [];
  const config = lerEdicoes(raiz);
  const { plugins } = lerCatalogo(raiz);
  for (const p of plugins.filter(x => config.plugins[x.nome] && existsSync(x.dir))) {
    const todos = listarArquivos(p.dir).filter(r => /\.(md|json|sh|py)$/.test(r));
    for (const edicao of config.edicoes) {
      const permitidas = habilidadesDaEdicao(config, p.nome, edicao);
      for (const rel of arquivosDaEdicao(todos, permitidas)) {
        ler(p, rel).split('\n').forEach((linha, i) => {
          if (/se instalada|se existir/i.test(linha)) return;
          for (const m of linha.matchAll(/\$\{CLAUDE_PLUGIN_ROOT\}\/skills\/([A-Za-z0-9_.-]+)/g)) {
            if (!permitidas.has(m[1])) erros.push(`${p.nome}: ${rel}:${i + 1} cita a habilidade "${m[1]}", que a edição ${edicao} não inclui (use "se instalada" na mesma linha)`);
          }
        });
      }
    }
  }
  return erros;
}

export function checarTudo(raiz) {
  const erros = [...regraCatalogo(raiz), ...regraEdicoes(raiz), ...regraReferenciasPorEdicao(raiz), ...regraReadme(raiz)];
  for (const p of lerCatalogo(raiz).plugins.filter(x => existsSync(x.dir))) {
    erros.push(...regraHabilidades(p), ...regraReferencias(p), ...regraTexto(p), ...regraFimDeLinha(p));
  }
  return erros;
}
