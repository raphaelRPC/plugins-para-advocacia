import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ehTextoNormalizavel, paraLF } from '../ferramentas/lib/texto.mjs';

test('md, sh, py, json são normalizáveis; csv, tsv e binários não', () => {
  for (const c of ['a.md', 'hooks/x.sh', 's.py', 'p.json', 'i.html']) assert.equal(ehTextoNormalizavel(c), true, c);
  for (const c of ['treino.csv', 'plano.tsv', 'foto.png', 'modelo.docx']) assert.equal(ehTextoNormalizavel(c), false, c);
});

test('paraLF troca CRLF por LF e preserva bytes cp1252', () => {
  const entrada = Buffer.from([0x41, 0x0d, 0x0a, 0xe7, 0xe3, 0x0d, 0x0a, 0x0d]);
  assert.deepEqual([...paraLF(entrada)], [0x41, 0x0a, 0xe7, 0xe3, 0x0a, 0x0d]);
});
