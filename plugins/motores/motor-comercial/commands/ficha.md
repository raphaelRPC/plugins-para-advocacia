---
description: Completa ou revisa as fichas do comercial, seção por seção. Mostra o que está preenchido, o que falta e quais habilidades melhoram com cada campo.
---

# /motor-comercial:ficha

Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`. As fichas são o contexto que todas as habilidades leem (`${CLAUDE_PLUGIN_ROOT}/docs/ficha-comercial.md`).

## 1. Ler

1. Abra `escritorio/04-base/comum/ficha-do-escritorio.md` e `escritorio/04-base/comum/ficha-comercial.md`. Se não existir, ofereça `/motor-comercial:comecar`, ou crie a partir de `${CLAUDE_PLUGIN_ROOT}/docs/ficha-do-escritorio-modelo.md` e `${CLAUDE_PLUGIN_ROOT}/docs/ficha-comercial-modelo.md` se o advogado quiser preencher tudo agora.
2. Leia também `escritorio/04-base/comum/aprendizados-comercial.md`, se existir.

## 2. Mostrar o quadro

| Seção | Preenchidos | Faltam | Habilidades que esperam por ela |
|---|---|---|---|

Use a tabela "Quais campos cada habilidade usa" de `${CLAUDE_PLUGIN_ROOT}/docs/ficha-comercial.md` para a última coluna. Mostre só as habilidades que estão instaladas (as pastas de `${CLAUDE_PLUGIN_ROOT}/skills/`).

Pergunte: "Por qual seção quer começar?". Sugira a que destrava mais habilidades.

## 3. Preencher

- Uma pergunta por campo, na ordem da seção. Mostre o exemplo do modelo como exemplo, nunca como resposta.
- Peça a cena concreta quando a resposta vier vaga.
- "Não sei" ou "depois": o campo segue `[A PREENCHER]`.
- Campo que é decisão do escritório e ninguém decidiu: `[A DEFINIR]`, com a pergunta que resolve.
- Valor de honorário: só o que o advogado disser. Comparação com a tabela da seccional fica `[CONFERIR]`.

## 4. Revisar aprendizados

Se houver aprendizados `em uso` que já são política (aparecem em várias tarefas, ou o advogado diz "isso é sempre assim"), proponha subir para o campo certo da ficha e mudar a situação do aprendizado para `retirada`, com a nota "incorporada à ficha: <campo>".

## 5. Gravar

Mostre a seção revisada com cada mudança marcada `[NOVO]` ou `[ALTERADO]`. Com o ok: grave, suba a versão (0.1 para 0.2), atualize `revisado_em` e acrescente uma linha no "Histórico da ficha". Sem pasta aberta: entregue a ficha inteira em bloco para colar no Projeto.
