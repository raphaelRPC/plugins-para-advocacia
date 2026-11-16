import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { montar } from '../ferramentas/lib/montagem.mjs';
import { lerZip } from '../ferramentas/lib/zip.mjs';

const RAIZ = join(import.meta.dirname, '..');
const saida = mkdtempSync(join(tmpdir(), 'dist-'));
const gerados = montar(RAIZ, '9.9.9', saida);

test('gera 16 zips de plugin, 3 pacotes e o SHA256SUMS', () => {
  assert.equal(gerados.filter(g => g.startsWith('plugins/')).length, 16);
  for (const e of ['essencial', 'completa', 'avancada']) assert.ok(gerados.includes(`plugins-para-advocacia-v9.9.9-${e}.zip`), e);
  assert.ok(existsSync(join(saida, 'SHA256SUMS.txt')));
});

test('essencial do comercial tem 6 habilidades e mantém comandos, agentes e docs', () => {
  const nome = gerados.find(g => /^plugins\/motor-comercial-.*-essencial\.zip$/.test(g));
  const caminhos = lerZip(readFileSync(join(saida, nome))).map(e => e.caminho);
  assert.equal(new Set(caminhos.filter(c => c.startsWith('skills/')).map(c => c.split('/')[1])).size, 6);
  for (const p of ['.claude-plugin/plugin.json', 'commands/comecar.md', 'agents/agente-comercial.md', 'docs/regras.md']) assert.ok(caminhos.includes(p), p);
});

test('.sh sai com LF e executável; CSV sai byte a byte igual', () => {
  const nome = gerados.find(g => g.startsWith('plugins/editor-de-carrossel-mjc-'));
  const sh = lerZip(readFileSync(join(saida, nome))).find(e => e.caminho === 'hooks/registrar-uso.sh');
  assert.equal(sh.dados.includes('\r'), false);
  assert.equal(sh.modo & 0o111, 0o111);

  const zipControl = gerados.find(g => /^plugins\/motor-controladoria-.*-avancada\.zip$/.test(g));
  const csv = lerZip(readFileSync(join(saida, zipControl))).find(e => e.caminho.endsWith('lote-em-massa-de-treino.csv'));
  const original = readFileSync(join(RAIZ, 'plugins/motores/motor-controladoria/skills/triagem-em-massa/assets/lote-em-massa-de-treino.csv'));
  assert.deepEqual(csv.dados, original);
});

test('pacote leva o LEIA-ME e um zip por plugin', () => {
  const pacote = lerZip(readFileSync(join(saida, 'plugins-para-advocacia-v9.9.9-essencial.zip'))).map(e => e.caminho);
  assert.ok(pacote.includes('LEIA-ME.md'));
  assert.equal(pacote.filter(c => c.startsWith('plugins/') && c.endsWith('.zip')).length, 8);
});
