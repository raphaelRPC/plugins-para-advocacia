import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, mkdirSync, cpSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { montarTodas, selecionar, conferirEntrega, filtrarChangelog, processarGuia, regraTickets } from '../ferramentas/lib/entregas.mjs';
import { listarArquivos } from '../ferramentas/lib/arquivos.mjs';
import { lerZip } from '../ferramentas/lib/zip.mjs';

const RAIZ = join(import.meta.dirname, '..');
const SAIDA = join(mkdtempSync(join(tmpdir(), 'entregas-')), 'saida');
const resultado = montarTodas(RAIZ, '9.9.9', SAIDA);
const por = Object.fromEntries(resultado.map(r => [r.ticket, r]));
const arvore = t => join(SAIDA, t, 'repositorio');

test('as três entregas cumprem a promessa e passam nas conferências', () => {
  assert.deepEqual(resultado.map(r => [r.ticket, r.plugins, r.habilidades]), [['classico', 2, 37], ['moderno', 5, 83], ['futuro', 8, 123]]);
  for (const r of resultado) assert.deepEqual(r.erros, [], r.ticket);
});

test('o Clássico só tem os seus plugins e nada da equipe', () => {
  const arquivos = listarArquivos(arvore('classico'));
  const plugins = new Set(arquivos.filter(a => a.startsWith('plugins/')).map(a => a.split('/').slice(0, 3).join('/')));
  assert.deepEqual([...plugins].sort(), ['plugins/fundacao/inicio-automacao', 'plugins/motores/motor-juridico']);
  for (const proibido of ['ferramentas/', 'testes/', 'compartilhado/', 'guia/equipe/', '.github/', 'edicoes.json', 'tickets.json']) {
    assert.equal(arquivos.some(a => a.startsWith(proibido)), false, proibido);
  }
  const skills = new Set(arquivos.filter(a => /^plugins\/motores\/motor-juridico\/skills\/[^/]+\/SKILL\.md$/.test(a)).map(a => a.split('/')[4]));
  assert.equal(skills.size, 17);
  assert.equal(skills.has('sustentacao-oral'), false);
});

test('marketplace, README, guias e changelog são do ticket', () => {
  const cat = JSON.parse(readFileSync(join(arvore('classico'), '.claude-plugin', 'marketplace.json'), 'utf8'));
  assert.equal(cat.name, 'plugins-advocacia-classico');
  assert.equal(cat.metadata.version, '9.9.9');
  assert.deepEqual(cat.plugins.map(p => p.name), ['inicio-automacao', 'motor-juridico']);
  assert.equal(JSON.stringify(cat).includes('marketing'), false);
  const comece = readFileSync(join(arvore('classico'), 'guia', 'comece-aqui.md'), 'utf8');
  assert.match(comece, /\/motor-juridico:comecar/);
  assert.equal(/carrossel|copywriter|motor-comercial|<!--/.test(comece), false);
  const changelog = readFileSync(join(arvore('classico'), 'CHANGELOG.md'), 'utf8');
  assert.equal(/motor-comercial|plugin-copywriter|guia\/equipe/.test(changelog), false);
  const readme = readFileSync(join(arvore('moderno'), 'README.md'), 'utf8');
  assert.match(readme, /5 plugins · 83 habilidades · versão do pacote \*\*9\.9\.9\*\*/);
  assert.match(readme, /C -->\|passagem-para-o-caso\| E/);
});

test('zips: um por plugin e o pacote com o LEIA-ME', () => {
  const pacote = lerZip(readFileSync(join(SAIDA, 'classico', 'zips', 'plugins-advocacia-classico-v9.9.9.zip'))).map(e => e.caminho);
  assert.deepEqual(pacote.sort(), ['LEIA-ME.md', 'plugins/inicio-automacao-0.3.2.zip', 'plugins/motor-juridico-1.0.1.zip'].sort());
  assert.match(readFileSync(join(SAIDA, 'SHA256SUMS.txt'), 'utf8'), /classico\/zips\/plugins-advocacia-classico-v9\.9\.9\.zip/);
});

test('arquivo estranho na entrega e promessa não cumprida são barrados', () => {
  const copia = join(mkdtempSync(join(tmpdir(), 'vaza-')), 'repo');
  cpSync(arvore('classico'), copia, { recursive: true });
  mkdirSync(join(copia, 'ferramentas'), { recursive: true });
  writeFileSync(join(copia, 'ferramentas', 'x.mjs'), '');
  mkdirSync(join(copia, 'plugins', 'motores', 'motor-controladoria'), { recursive: true });
  writeFileSync(join(copia, 'plugins', 'motores', 'motor-controladoria', 'README.md'), 'x');
  const sel = selecionar(RAIZ, 'classico');
  const erros = conferirEntrega(copia, { ...sel, ticket: { ...sel.ticket, promessa: 999 } }).join('\n');
  assert.match(erros, /ferramentas\/x\.mjs não pertence/);
  assert.match(erros, /motor-controladoria\/README\.md não pertence/);
  assert.match(erros, /abaixo da promessa de 999/);
});

test('changelog filtrado e guia processado', () => {
  const log = '# M\n\n## [1.1.0] - 2026-11-16\n\n- `motor-juridico` 1.0.1: a\n- `motor-comercial` 2.0.1: b\n- Repositório reorganizado\n\n## [1.0.0] - 2026-11-16\n\n- Primeira: `motor-juridico`, `motor-comercial`\n';
  const filtrado = filtrarChangelog(log, ['motor-juridico']);
  assert.match(filtrado, /- `motor-juridico` 1\.0\.1: a/);
  assert.equal(/motor-comercial|reorganizado|\[1\.0\.0\]/.test(filtrado), false);
  const guia = processarGuia('a\n<!-- so-fonte:inicio -->\nsegredo\n<!-- so-fonte:fim -->\n`raphaelRPC/plugins-para-advocacia` `/motor-comercial:comecar`\n',
    { dono: 'org', repositorio: 'r', exemplo: 'motor-juridico', grupos: '' });
  assert.equal(guia, 'a\n`org/r` `/motor-juridico:comecar`\n');
});

test('tickets.json do repositório está coerente', () => {
  assert.deepEqual(regraTickets(RAIZ), []);
});
