# Modelo dos casos de teste do escritório (jurídico)

Os casos de teste do escritório trocam os fictícios por peças e casos reais anonimizados, com o gabarito do advogado. Ficam em `escritorio/04-base/casos-de-teste/juridico/casos.md`. Servem para rodar as habilidades antes de usar em caso novo, depois de cada adaptação e quando uma habilidade própria muda de versão.

Regras: só material anonimizado (nome por `[CLIENTE]`, CPF por `[DOC]`, processo por `[PROCESSO]`); só em conta profissional ou de equipe; o gabarito é do advogado, e o que a habilidade sugerir vai marcado "sugestão" até o ok.

```markdown
---
documento: Casos de teste do jurídico
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DO ADVOGADO]
---

# Casos de teste · jurídico

## Caso J1 · [tipo de peça ou tarefa] · [área]
Material: [o que entra: a minuta anonimizada, o lote de documentos, a pesquisa trazida do Jus IA]
Habilidade: [conferir-peca | conferir-citacoes | dossie-do-caso | minutar-peca | habilidade própria]
Não pode falhar: [a lista do advogado, um item por linha: "achar o nome de outro cliente no item 4", "não usar o julgado sem conferência", "parar porque a tese não foi definida"]
Gabarito escrito por: [função] em AAAA-MM-DD
```

## Exemplo (Escritório Modelo, fictício)

```markdown
## Caso J1 · minuta com erros · previdenciário
Material: a minuta com erros do caso 1 dos casos fictícios (Marta)
Habilidade: conferir-peca e conferir-citacoes
Não pode falhar: "o autor Paulo" no item 4 dos fatos; gênero trocado; as duas datas de cessação; a Súmula 999 do TRF6 vermelha; o "doc. 7" que não existe
Gabarito escrito por: advogada titular em 2026-04-16

## Caso J2 · lote · previdenciário
Material: o lote de treino de cinco segurados (pecas-em-lote)
Habilidade: pecas-em-lote com a peticao-inicial-restabelecimento
Não pode falhar: a linha sem data de cessação barrada; a linha trabalhista barrada; nenhuma citação sem marca nas três minutas que saem
Gabarito escrito por: advogada titular em 2026-04-16
```
