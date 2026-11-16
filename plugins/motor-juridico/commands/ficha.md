---
description: Completa ou revisa as fichas do produção jurídica (a do escritório e a jurídica), seção por seção. Mostra o que está preenchido, o que falta e quais habilidades melhoram com cada campo.
---

# /motor-juridico:ficha

Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`. As fichas são o contexto que todas as habilidades leem (`${CLAUDE_PLUGIN_ROOT}/docs/ficha-juridica.md`).

## 1. Ler

1. Abra `escritorio/04-base/comum/ficha-do-escritorio.md` e `escritorio/04-base/comum/ficha-juridica.md`. Se não existirem, ofereça `/motor-juridico:comecar`, ou crie a partir de `${CLAUDE_PLUGIN_ROOT}/docs/ficha-do-escritorio-modelo.md` e `${CLAUDE_PLUGIN_ROOT}/docs/ficha-juridica-modelo.md` se o advogado quiser preencher tudo agora.
2. Leia também `escritorio/04-base/comum/aprendizados-juridico.md` e `nicho.md`, se existirem.

## 2. Mostrar o quadro

| Ficha · seção | Preenchidos | Faltam | Habilidades que esperam por ela |
|---|---|---|---|

Use a tabela "Quais campos cada habilidade usa" de `${CLAUDE_PLUGIN_ROOT}/docs/ficha-juridica.md`. Mostre só as habilidades instaladas (as pastas de `${CLAUDE_PLUGIN_ROOT}/skills/`). Pergunte por qual seção começar e sugira a que destrava mais habilidades.

## 3. Preencher

- Uma pergunta por campo. Mostre o exemplo do modelo como exemplo, nunca como resposta.
- Peça a cena concreta quando a resposta vier vaga ("a gente cita direitinho" vira "e a última peça que voltou com erro de citação, o que tinha?").
- "Não sei" ou "depois": o campo segue `[A PREENCHER]`. Decisão que ninguém tomou: `[A DEFINIR]`, com a pergunta que resolve.
- Campo da ficha do escritório mudou: avise que vale também para os outros plugins motor.

## 4. Revisar aprendizados

Aprendizado `em uso` que já é política do escritório: proponha subir para o campo certo e mudar a situação para `retirada`, com a nota "incorporada à ficha: <campo>".

## 5. Gravar

Mostre a seção revisada com cada mudança marcada `[NOVO]` ou `[ALTERADO]`. Com o ok: grave, suba a versão, atualize `revisado_em` e acrescente uma linha no "Histórico da ficha". Sem pasta aberta: entregue a ficha inteira em bloco para colar no Projeto.
