# Estrutura do repositório

```
plugins-para-advocacia/
  .claude-plugin/marketplace.json   a lista dos plugins
  plugins/
    fundacao/
      inicio-automacao/
    motores/
      motor-comercial/
      motor-experiencia/
      motor-juridico/
      motor-controladoria/
    marketing/
      marketing-juridico-claude/
      editor-de-carrossel-mjc/
      plugin-copywriter/
  compartilhado/                    o que se repete em mais de um plugin
    mapa.json                       diz de onde cada cópia vem
  edicoes.json                      habilidades de cada edição dos motores
  tickets.json                      plugins e edições de cada ticket (ver entregas-por-ticket.md)
  modelos/                          o modelo do README das entregas
  ferramentas/                      os scripts de checar, sincronizar, montar zips e versões
  testes/                           os testes dos scripts
  guia/                             os guias para o advogado e para a equipe
  CHANGELOG.md                      o histórico das versões
  .github/workflows/                a checagem e o release automáticos
```

Cada plugin tem dentro a pasta `.claude-plugin/` com o `plugin.json`, e as pastas `skills/`, `commands/` e outras.

## A regra do que se repete

Alguns arquivos aparecem iguais em mais de um plugin. Esses arquivos têm uma fonte única em `compartilhado/`.

1. Edite o arquivo só em `compartilhado/`. Nunca edite a cópia dentro do plugin.
2. Rode `npm run sincronizar`.
3. Rode `npm run checar` para conferir.

O `mapa.json` mostra para quais plugins cada arquivo é copiado.

## Outros comandos

- `npm run testar` roda os testes.
- `npm run checar` confere as regras do repositório.
- `npm run zips` monta os zips em `dist/`.

Versões e publicação: veja `versoes.md` e `publicar-uma-versao.md`.
