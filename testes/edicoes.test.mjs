import { test } from 'node:test';
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { lerEdicoes, habilidadesDaEdicao, arquivosDaEdicao, conferirEdicoes } from '../ferramentas/lib/edicoes.mjs';
import { regraEdicoes } from '../ferramentas/lib/regras.mjs';

const RAIZ = join(import.meta.dirname, '..');
const config = lerEdicoes(RAIZ);

test('contagens acumuladas batem com os READMEs', () => {
  const esperado = { 'motor-comercial': [6, 13, 16], 'motor-experiencia': [6, 14, 17], 'motor-juridico': [9, 17, 21], 'motor-controladoria': [9, 16, 20] };
  for (const [plugin, contagens] of Object.entries(esperado)) {
    assert.deepEqual(config.edicoes.map(e => habilidadesDaEdicao(config, plugin, e).size), contagens, plugin);
  }
});

test('plugin sem edições entra inteiro; edição desconhecida é erro', () => {
  assert.equal(habilidadesDaEdicao(config, 'plugin-copywriter', 'essencial'), null);
  assert.throws(() => habilidadesDaEdicao(config, 'motor-comercial', 'premium'), /Edição desconhecida/);
});

test('o filtro só tira pastas de skills/; commands, agents e docs ficam', () => {
  const arquivos = ['.claude-plugin/plugin.json', 'commands/comecar.md', 'agents/agente.md', 'docs/regras.md', 'README.md',
                    'skills/a/SKILL.md', 'skills/a/scripts/x.py', 'skills/b/SKILL.md'];
  assert.deepEqual(arquivosDaEdicao(arquivos, new Set(['a'])), arquivos.filter(a => !a.startsWith('skills/b/')));
  assert.deepEqual(arquivosDaEdicao(arquivos, null), arquivos);
});

test('habilidade sem edição, repetida ou inexistente é erro', () => {
  const c = { edicoes: ['essencial', 'completa'], plugins: { m: { essencial: ['a', 'b'], completa: ['b', 'z'] } } };
  assert.deepEqual(conferirEdicoes(c, { m: ['a', 'b', 'c'] }).sort(), [
    'm: "b" aparece em mais de uma edição',
    'm: "c" não está em nenhuma edição',
    'm: "z" está em edicoes.json mas não existe',
  ]);
});

test('o repositório atual passa', () => {
  assert.deepEqual(regraEdicoes(RAIZ), []);
});
