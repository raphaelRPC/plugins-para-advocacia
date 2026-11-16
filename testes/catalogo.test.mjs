import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { lerCatalogo } from '../ferramentas/lib/catalogo.mjs';

const RAIZ = join(import.meta.dirname, '..');
const GRUPOS = {
  'inicio-automacao': 'fundacao',
  'motor-comercial': 'motores', 'motor-experiencia': 'motores',
  'motor-juridico': 'motores', 'motor-controladoria': 'motores',
  'marketing-juridico-claude': 'marketing', 'editor-de-carrossel-mjc': 'marketing',
  'plugin-copywriter': 'marketing',
};

test('cada plugin do catálogo está na pasta do seu grupo e tem plugin.json', () => {
  const { dados, plugins } = lerCatalogo(RAIZ);
  assert.equal(plugins.length, 8);
  for (const p of plugins) {
    assert.equal(p.grupo, GRUPOS[p.nome], p.nome);
    assert.equal(p.source, `./plugins/${p.grupo}/${p.nome}`);
    const arquivo = join(p.dir, '.claude-plugin', 'plugin.json');
    assert.ok(existsSync(arquivo), p.nome);
    const versaoDoPlugin = JSON.parse(readFileSync(arquivo, 'utf8')).version;
    assert.equal(typeof versaoDoPlugin, 'string', p.nome);
    assert.ok(versaoDoPlugin.length > 0, p.nome);
    assert.equal(p.versao, versaoDoPlugin, p.nome);
  }
  for (const bruta of dados.plugins) {
    assert.ok(!('version' in bruta), `${bruta.name}: version só no plugin.json`);
    assert.equal(bruta.category, GRUPOS[bruta.name], bruta.name);
  }
});
