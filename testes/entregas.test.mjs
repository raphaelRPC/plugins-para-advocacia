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
  const pacote = lerZip(readFileSync(join(SAIDA, 'classico', 'zips', 'plugins-advocacia-classico.zip'))).map(e => e.caminho);
  assert.equal(pacote.length, 3);
  assert.ok(pacote.includes('LEIA-ME.md'));
  assert.ok(pacote.includes('plugins/inicio-automacao.zip'));
  assert.ok(pacote.includes('plugins/motor-juridico.zip'));
  assert.equal(pacote.some(c => /\d+\.\d+\.\d+/.test(c)), false);
  assert.match(readFileSync(join(SAIDA, 'SHA256SUMS.txt'), 'utf8'), /classico\/zips\/plugins-advocacia-classico\.zip/);
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

test('habilidade de edição acima, nome de ticket e guia avulso são barrados', () => {
  const copia = join(mkdtempSync(join(tmpdir(), 'vaza2-')), 'repo');
  cpSync(arvore('moderno'), copia, { recursive: true });
  const exp = join(copia, 'plugins', 'motores', 'motor-experiencia');
  mkdirSync(join(exp, 'skills', 'pagina-do-caso'), { recursive: true });
  writeFileSync(join(exp, 'skills', 'pagina-do-caso', 'SKILL.md'), '---\nname: pagina-do-caso\ndescription: x\n---\n');
  writeFileSync(join(exp, 'docs', 'nota.md'), 'Disponível no ticket Futuro.\n');
  mkdirSync(join(copia, 'guia'), { recursive: true });
  writeFileSync(join(copia, 'guia', 'notas-internas.md'), 'x');
  writeFileSync(join(exp, 'commands', 'extra.md'), 'Rode a `pagina-do-caso` agora.\n');
  const erros = conferirEntrega(copia, selecionar(RAIZ, 'moderno')).join('\n');
  assert.match(erros, /motor-experiencia traz skills\/pagina-do-caso, que não é da edição essencial/);
  assert.match(erros, /docs\/nota\.md:1 cita ticket/);
  assert.match(erros, /guia\/notas-internas\.md não pertence/);
  assert.match(erros, /commands\/extra\.md:1 manda usar pagina-do-caso/);
});

test('LEIA-ME do pacote se basta sozinho, sem GitHub', () => {
  const pacote = lerZip(readFileSync(join(SAIDA, 'moderno', 'zips', 'plugins-advocacia-moderno.zip')));
  const leiaMe = pacote.find(e => e.caminho === 'LEIA-ME.md').dados.toString('utf8');
  assert.match(leiaMe, /## Problemas comuns/);
  assert.match(leiaMe, /Enviar plugin/);
  assert.equal(/github\.com|Repositório não encontrado|<!--/.test(leiaMe), false);
});

test('README do motor cortado só lista as habilidades que vieram', () => {
  const readme = readFileSync(join(arvore('classico'), 'plugins', 'motores', 'motor-juridico', 'README.md'), 'utf8');
  assert.equal(readme.includes('`sustentacao-oral`'), false);
  assert.equal(/A edição \*\*essencial\*\* traz/.test(readme), false);
  assert.match(readme, /`banco-de-teses-vivo`/);
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
