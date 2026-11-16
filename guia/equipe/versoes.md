# Versões

## Do plugin (no plugin.json)

- **major** (2.0.0 → 3.0.0): muda a pasta `escritorio/` ou a ficha de um jeito que obriga o escritório a refazer algo.
- **minor** (2.0.0 → 2.1.0): habilidade nova, comando novo ou comportamento novo.
- **patch** (2.0.0 → 2.0.1): correção de texto, regra ou script.

Nunca mude o número à mão. Use:

    node ferramentas/versao.mjs subir motor-comercial patch "corrige a régua de retorno"

Isso muda o plugin.json e escreve a linha no CHANGELOG.md.

## Do pacote (a tag do GitHub)

O pacote junta tudo o que mudou desde a última publicação:

    node ferramentas/versao.mjs fechar 1.1.0

Depois: commit, `git tag v1.1.0` e `git push origin main v1.1.0`. O GitHub monta o release (ver `publicar-uma-versao.md`).
