import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lerFrontmatter } from '../ferramentas/lib/frontmatter.mjs';

test('lê name e description dobrada em várias linhas', () => {
  const t = '---\nname: triar-contato\ndescription: >\n  Faz a triagem\n  de cada mensagem.\n---\n# Corpo';
  assert.deepEqual(lerFrontmatter(t), { name: 'triar-contato', description: 'Faz a triagem de cada mensagem.' });
});

test('aceita CRLF e aspas; sem frontmatter devolve null', () => {
  assert.equal(lerFrontmatter('---\r\nname: "x"\r\ndescription: y\r\n---\r\n').name, 'x');
  assert.equal(lerFrontmatter('# sem frontmatter'), null);
});
