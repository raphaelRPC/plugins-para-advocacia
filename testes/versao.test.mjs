import { test } from 'node:test';
import assert from 'node:assert/strict';
import { proximaVersao, acrescentarLinha, fecharVersao, notasDaVersao } from '../ferramentas/lib/versao.mjs';

const BASE = '# Mudanças\n\n## [Não publicado]\n\n## [1.0.0] - 2026-11-16\n\n- Primeira.\n';

test('proximaVersao', () => {
  assert.equal(proximaVersao('2.0.0', 'patch'), '2.0.1');
  assert.equal(proximaVersao('0.3.1', 'minor'), '0.4.0');
  assert.equal(proximaVersao('1.1.2', 'major'), '2.0.0');
  assert.throws(() => proximaVersao('1.0', 'patch'), /Versão inválida/);
  assert.throws(() => proximaVersao('1.0.0', 'grande'), /Tipo inválido/);
});

test('acrescentar, fechar e extrair notas', () => {
  let t = acrescentarLinha(BASE, '- `motor-comercial` 2.0.1: corrige a régua.');
  t = acrescentarLinha(t, '- `motor-juridico` 1.1.0: nova habilidade.');
  t = fecharVersao(t, '1.1.0', '2026-11-20');
  assert.match(t, /## \[Não publicado\]\n\n## \[1\.1\.0\] - 2026-11-20\n\n- `motor-comercial` 2\.0\.1: corrige a régua\.\n- `motor-juridico` 1\.1\.0: nova habilidade\.\n\n## \[1\.0\.0\]/);
  assert.equal(notasDaVersao(t, '1.1.0'), '- `motor-comercial` 2.0.1: corrige a régua.\n- `motor-juridico` 1.1.0: nova habilidade.');
});

test('não fecha versão vazia nem repetida; notas de versão inexistente é erro', () => {
  assert.throws(() => fecharVersao(BASE, '1.1.0', '2026-11-20'), /Nada em "Não publicado"/);
  const t = acrescentarLinha(BASE, '- x');
  assert.throws(() => fecharVersao(t, '1.0.0', '2026-11-20'), /já existe/);
  assert.throws(() => notasDaVersao(BASE, '9.9.9'), /não está no CHANGELOG/);
});
