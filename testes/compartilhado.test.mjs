import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { encontrarRepetidos, gerarMapa, divergencias, aplicar } from '../ferramentas/lib/compartilhado.mjs';

const TEXTO = 'regra do escritorio\n'.repeat(20);

function repo(arquivos) {
  const raiz = mkdtempSync(join(tmpdir(), 'repo-'));
  for (const [c, v] of Object.entries(arquivos)) { mkdirSync(join(raiz, c, '..'), { recursive: true }); writeFileSync(join(raiz, c), v); }
  return raiz;
}

test('acha repetidos mesmo com CRLF numa cópia e ignora arquivo pequeno', () => {
  const raiz = repo({
    'plugins/motores/a/docs/regras.md': TEXTO,
    'plugins/motores/b/docs/regras.md': TEXTO.replace(/\n/g, '\r\n'),
    'plugins/motores/c/docs/regras.md': Buffer.from(TEXTO),
    'plugins/motores/a/x.md': 'curto', 'plugins/motores/b/x.md': 'curto',
  });
  assert.deepEqual(encontrarRepetidos(raiz), [[
    'plugins/motores/a/docs/regras.md', 'plugins/motores/b/docs/regras.md', 'plugins/motores/c/docs/regras.md',
  ]]);
});

test('mapa aponta para compartilhado/<grupo>/<caminho no plugin>', () => {
  const mapa = gerarMapa([['plugins/motores/a/docs/regras.md', 'plugins/motores/b/docs/regras.md'],
                          ['plugins/marketing/x/skills/s/SKILL.md', 'plugins/marketing/y/skills/s/SKILL.md'],
                          ['plugins/fundacao/i/a.md', 'plugins/motores/a/a.md']]);
  assert.deepEqual(mapa.grupos.map(g => g.fonte), [
    'compartilhado/motores/docs/regras.md', 'compartilhado/marketing/skills/s/SKILL.md', 'compartilhado/geral/a.md',
  ]);
});

test('editar a cópia dentro do plugin é acusado pelo nome; aplicar corrige', () => {
  const raiz = repo({ 'compartilhado/motores/docs/regras.md': TEXTO, 'plugins/motores/a/docs/regras.md': TEXTO, 'plugins/motores/b/docs/regras.md': TEXTO + 'editado' });
  const mapa = { grupos: [{ fonte: 'compartilhado/motores/docs/regras.md', destinos: ['plugins/motores/a/docs/regras.md', 'plugins/motores/b/docs/regras.md', 'plugins/motores/c/docs/regras.md'] }] };
  assert.deepEqual(divergencias(raiz, mapa), [
    'plugins/motores/b/docs/regras.md difere de compartilhado/motores/docs/regras.md',
    'plugins/motores/c/docs/regras.md não existe (deveria ser cópia de compartilhado/motores/docs/regras.md)',
  ]);
  assert.equal(aplicar(raiz, mapa), 2);
  assert.deepEqual(divergencias(raiz, mapa), []);
  assert.equal(readFileSync(join(raiz, 'plugins/motores/b/docs/regras.md'), 'utf8'), TEXTO);
});

test('fonte que sumiu é erro, não "tudo certo"', () => {
  const raiz = repo({ 'plugins/motores/a/docs/r.md': TEXTO });
  assert.deepEqual(divergencias(raiz, { grupos: [{ fonte: 'compartilhado/motores/docs/r.md', destinos: ['plugins/motores/a/docs/r.md'] }] }),
    ['compartilhado/motores/docs/r.md não existe']);
});
