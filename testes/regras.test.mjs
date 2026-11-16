import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { regraCatalogo, regraHabilidades, regraReferencias, regraTexto, regraFimDeLinha, checarTudo } from '../ferramentas/lib/regras.mjs';

function pluginFalso(grupo, arquivos) {
  const dir = mkdtempSync(join(tmpdir(), 'plugin-'));
  for (const [caminho, conteudo] of Object.entries(arquivos)) {
    mkdirSync(join(dir, caminho, '..'), { recursive: true });
    writeFileSync(join(dir, caminho), conteudo);
  }
  return { nome: 'teste', grupo, dir };
}

test('habilidade sem description, com name trocado ou description longa é erro', () => {
  const p = pluginFalso('motores', {
    'skills/a/SKILL.md': '---\nname: a\n---\n',
    'skills/b/SKILL.md': '---\nname: outro\ndescription: ok\n---\n',
    'skills/c/SKILL.md': `---\nname: c\ndescription: ${'x'.repeat(1025)}\n---\n`,
    'skills/d/SKILL.md': '---\nname: d\ndescription: ok\n---\n',
  });
  const erros = regraHabilidades(p);
  assert.equal(erros.length, 3);
  assert.match(erros.join('\n'), /skills\/a.*description/);
  assert.match(erros.join('\n'), /skills\/b.*name/);
  assert.match(erros.join('\n'), /skills\/c.*1024/);
});

test('referência ${CLAUDE_PLUGIN_ROOT} para arquivo que não existe é erro', () => {
  const p = pluginFalso('motores', {
    'docs/regras.md': 'x',
    'commands/comecar.md': 'Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`. Veja ${CLAUDE_PLUGIN_ROOT}/docs/falta.md.',
  });
  assert.deepEqual(regraReferencias(p), ['teste: commands/comecar.md cita ${CLAUDE_PLUGIN_ROOT}/docs/falta.md, que não existe']);
});

test('travessão e palavra proibida valem para motores e não para marketing', () => {
  const arquivos = { 'README.md': 'Material do evento — RPC' };
  assert.equal(regraTexto(pluginFalso('motores', arquivos)).length, 2);
  assert.equal(regraTexto(pluginFalso('marketing', arquivos)).length, 0);
  assert.equal(regraTexto(pluginFalso('motores', { 'docs/prazos.md': 'turma recursal, novembro' })).length, 0);
});

test('.sh com CRLF é erro', () => {
  assert.equal(regraFimDeLinha(pluginFalso('marketing', { 'hooks/x.sh': '#!/bin/sh\r\necho\r\n' })).length, 1);
  assert.equal(regraFimDeLinha(pluginFalso('marketing', { 'hooks/x.sh': '#!/bin/sh\necho\n' })).length, 0);
});

function repoFalso({ metadata = { version: '1.0.0' }, entrada = {}, manifesto = {}, semManifesto = false, pasta = 'motores' }) {
  const raiz = mkdtempSync(join(tmpdir(), 'repo-'));
  const entry = { name: 'x', source: './plugins/motores/x', category: 'motores', ...entrada };
  mkdirSync(join(raiz, '.claude-plugin'), { recursive: true });
  writeFileSync(join(raiz, '.claude-plugin', 'marketplace.json'), JSON.stringify({ metadata, plugins: [entry] }));
  const dir = join(raiz, entry.source);
  mkdirSync(join(dir, '.claude-plugin'), { recursive: true });
  if (!semManifesto) writeFileSync(join(dir, '.claude-plugin', 'plugin.json'), JSON.stringify({ name: 'x', version: '1.0.0', ...manifesto }));
  return raiz;
}

test('regraCatalogo: catálogo correto não tem erros', () => {
  assert.deepEqual(regraCatalogo(repoFalso({})), []);
});

test('regraCatalogo: version na entrada do marketplace é erro', () => {
  assert.deepEqual(regraCatalogo(repoFalso({ entrada: { version: '1.0.0' } })),
    ['x: marketplace.json não deve ter "version" (a versão fica só no plugin.json)']);
});

test('regraCatalogo: plugin.json sem version é erro', () => {
  assert.deepEqual(regraCatalogo(repoFalso({ manifesto: { version: undefined } })), ['x: plugin.json sem version']);
});

test('regraCatalogo: category diferente da pasta é erro', () => {
  assert.deepEqual(regraCatalogo(repoFalso({ entrada: { category: 'marketing' } })),
    ['x: category "marketing" diferente da pasta (motores)']);
});

test('regraCatalogo: sem metadata.version, sem plugin.json, name trocado e fora de plugins/<grupo>/<nome>', () => {
  assert.match(regraCatalogo(repoFalso({ metadata: {} })).join('\n'), /metadata\.version/);
  assert.match(regraCatalogo(repoFalso({ semManifesto: true })).join('\n'), /sem \.claude-plugin\/plugin\.json/);
  assert.match(regraCatalogo(repoFalso({ manifesto: { name: 'y' } })).join('\n'), /plugin\.json diz name "y"/);
  assert.match(regraCatalogo(repoFalso({ entrada: { source: './outro/x' } })).join('\n'), /fora de plugins/);
});

test('o repositório atual passa em todas as regras', () => {
  assert.deepEqual(checarTudo(join(import.meta.dirname, '..')), []);
});
