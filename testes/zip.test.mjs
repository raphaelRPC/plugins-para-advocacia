import { test } from 'node:test';
import assert from 'node:assert/strict';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { criarZip, lerZip } from '../ferramentas/lib/zip.mjs';

const entradas = [
  { caminho: '.claude-plugin/plugin.json', dados: Buffer.from('{"name":"x"}\n') },
  { caminho: 'hooks/registrar-uso.sh', dados: Buffer.from('#!/bin/sh\necho ok\n'), executavel: true },
  { caminho: 'skills/ação/SKILL.md', dados: Buffer.from('---\nname: ação\n---\n') },
];

test('ida e volta preserva caminhos, conteúdo e bit de executável', () => {
  const lidos = lerZip(criarZip(entradas));
  assert.deepEqual(lidos.map(e => e.caminho), entradas.map(e => e.caminho));
  lidos.forEach((e, i) => assert.deepEqual(e.dados, entradas[i].dados));
  assert.equal(lidos[1].modo & 0o777, 0o755);
  assert.equal(lidos[0].modo & 0o777, 0o644);
});

test('mesmo conteúdo gera o mesmo zip (data fixa)', () => {
  assert.deepEqual(criarZip(entradas), criarZip(entradas));
});

test('um leitor de zip do sistema aceita o arquivo', (t) => {
  const pasta = mkdtempSync(join(tmpdir(), 'zip-'));
  const arquivo = join(pasta, 't.zip');
  writeFileSync(arquivo, criarZip(entradas));
  // unzip existe no Git Bash e no Ubuntu do GitHub Actions. Não usar o tar do Git Bash: é GNU e não lê zip.
  try { execFileSync('unzip', ['-t', arquivo], { stdio: 'pipe' }); }
  catch (e) { if (e.code === 'ENOENT') t.skip('unzip não disponível'); else throw e; }
});
