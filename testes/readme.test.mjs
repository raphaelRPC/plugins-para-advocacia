import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { conferirReadme, regraReadme } from '../ferramentas/lib/readme.mjs';

const TEXTO = '1 plugins · 16 habilidades · versão do pacote **1.1.0**\n| [`motor-a`](plugins/motores/motor-a) | 2.0.1 | 16 | 6 / 13 / 16 |\n';

test('README em dia não gera erro', () => {
  assert.deepEqual(conferirReadme(TEXTO, [{ nome: 'motor-a', versao: '2.0.1', habilidades: 16 }], '1.1.0'), []);
});

test('versão, contagem, pacote e plugin ausente são acusados', () => {
  const erros = conferirReadme(TEXTO, [
    { nome: 'motor-a', versao: '2.0.2', habilidades: 17 },
    { nome: 'motor-b', versao: '1.0.0', habilidades: 3 },
  ], '1.2.0');
  assert.deepEqual(erros, [
    'README.md: não mostra a versão do pacote **1.2.0**',
    'README.md: o resumo do topo deveria dizer "2 plugins · 20 habilidades"',
    'README.md: motor-a aparece com versão 2.0.1, mas o plugin.json diz 2.0.2',
    'README.md: motor-a aparece com 16 habilidades, mas tem 17',
    'README.md: motor-b não está na tabela "Os plugins"',
  ]);
});

test('o README atual está em dia', () => {
  assert.deepEqual(regraReadme(join(import.meta.dirname, '..')), []);
});

import { atualizarVersaoDoPlugin, atualizarVersaoDoPacote } from '../ferramentas/lib/readme.mjs';

test('subir e fechar atualizam o README', () => {
  let t = atualizarVersaoDoPlugin(TEXTO, 'motor-a', '2.0.2');
  t = atualizarVersaoDoPacote(t, '1.1.0', '1.2.0');
  assert.deepEqual(conferirReadme(t, [{ nome: 'motor-a', versao: '2.0.2', habilidades: 16 }], '1.2.0'), []);
  assert.equal(atualizarVersaoDoPlugin(TEXTO, 'outro', '9.9.9'), TEXTO);
});
