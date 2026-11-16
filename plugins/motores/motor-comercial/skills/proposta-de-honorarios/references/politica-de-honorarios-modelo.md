# Modelo da política de honorários

Use no modo A da `proposta-de-honorarios`. Copie o modelo abaixo, preencha só com o que o advogado disse e grave em `escritorio/04-base/comercial/politica-de-honorarios.md`. O que ele não souber agora fica `[A DEFINIR]`. Nenhum valor é sugerido pela IA.

A política é documento interno. Ela nunca vai para publicidade, para o site ou para mensagem a muitas pessoas.

```markdown
---
documento: Política de honorários
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
acesso: restrito à equipe
---

# Política de honorários · [NOME DO ESCRITÓRIO]

> O que o escritório pratica, para toda proposta sair igual, com a conta à mostra. Valor final e condição fora desta política são decisão de [QUEM APROVA].

## 1. Referência

- Tabela de honorários da seccional da OAB de [UF]: usada como referência [mínima | orientativa] `[CONFERIR]` na versão vigente antes de cada proposta. Esta política não copia valores da tabela.
- Código de Ética e Disciplina da OAB e Estatuto da Advocacia (Lei 8.906/1994): honorários fixados com moderação, proposta por escrito, nada de captação nem de aviltamento de valor `[CONFERIR]`.

## 2. Modelo de cobrança por área

| Área | Modelo (fixo, êxito, misto, mensal) | Observação |
|---|---|---|
| [ÁREA] | [A DEFINIR] | |

## 3. Valores de referência por tipo de caso

| Tipo de caso | Escopo de referência (o que inclui) | Fixo | Êxito (percentual e base) | Observação |
|---|---|---|---|---|
| [TIPO DE CASO] | [A DEFINIR] | [A DEFINIR] ou "caso a caso" | [A DEFINIR] ou "não se aplica" | |

Só o advogado preenche esta tabela. Tipo de caso sem linha: o valor é decidido caso a caso e a proposta pergunta.

## 4. Êxito

- Base de cálculo: [A DEFINIR] (ex.: sobre o valor efetivamente recebido pelo cliente; sobre os atrasados; sobre o valor do acordo)
- Momento do pagamento: [A DEFINIR] (ex.: na liberação do valor ao cliente)
- Sem valor recebido: não há honorário de êxito.
- Limite: o total de honorários não pode passar do proveito do cliente, conforme o Código de Ética e Disciplina da OAB `[CONFERIR]`.
- Benefício mensal ou prestação continuada: como o percentual incide sobre parcelas futuras, se incidir `[A DEFINIR]` `[CONFERIR]`.

## 5. Entrada, parcelas e formas de pagamento

- Entrada mínima: [A DEFINIR]
- Parcelas: até [A DEFINIR] vezes, [com | sem] correção ou juros
- Vencimento: [A DEFINIR] (ex.: todo dia 10, ou o dia que o cliente escolher)
- Formas de pagamento: [A PREENCHER] (ex.: Pix, boleto, cartão)
- Consulta abatida dos honorários: [sim | não]

## 6. Despesas

- Quem paga custas, perícia, cópias, deslocamento e correio: [A DEFINIR]
- Como o cliente é avisado antes: [A DEFINIR] (ex.: mensagem com o valor e o motivo, antes de gastar)
- Prestação de contas das despesas: [A DEFINIR]
- Gratuidade da justiça, quando cabível, é avaliada pelo advogado no caso `[CONFERIR]`.

## 7. Validade e aprovação

- Validade da proposta: [A DEFINIR] dias corridos
- Quem aprova a proposta: [A PREENCHER]
- Quem atende pode ajustar sozinho: [A DEFINIR] (ex.: dia de vencimento; número de parcelas dentro do máximo)
- Fora da política: só com [QUEM APROVA]. No escritório solo, a proposta fora da política espera um dia antes de sair.

## 8. Valor reduzido e casos sem cobrança

- Critério escrito: [A DEFINIR] (ex.: atuação pro bono conforme a regra da OAB, com critério de renda `[CONFERIR]`)
- Quem decide: [A PREENCHER]

## 9. Inadimplência

- Multa, juros e índice de correção que o contrato usa: [A DEFINIR] `[CONFERIR]` os limites (o mesmo que o campo `inadimplencia` da ficha comercial)
- Antes de qualquer cobrança: [A DEFINIR] (ex.: ligação de quem cuida do caso para combinar uma solução)

## 10. O que não fazemos

- Desconto para fechar no mesmo dia.
- Valor de ação passado por mensagem antes da consulta.
- Comparação com honorários de outros escritórios.
- Proposta sem a lista do que não está incluído.
- [O que o escritório acrescentar]

## Histórico

(uma linha por mudança: data, o que mudou, quem decidiu)
```

## Como as habilidades usam a política

| Habilidade | O que lê |
|---|---|
| `proposta-de-honorarios` | Tudo. Seção 3 para o ponto de partida, seções 4 a 7 para as condições. |
| `contrato-de-honorarios` (se instalada) | Seções 4 a 6, para as cláusulas de êxito, pagamento e despesas, e a 9, para a inadimplência. |
| `objecoes-comerciais` (se instalada) | Seções 5, 7 e 10, para saber o que pode ser oferecido numa renegociação e o que nunca. |

Mudou a política: atualize a seção 3 (Honorários) da ficha comercial (`escritorio/04-base/comum/ficha-comercial.md`: `modelo`, `valores_de_referencia`, `entrada_e_parcelas`, `formas_de_pagamento`, `validade_da_proposta`, `despesas`, `inadimplencia`, `quem_aprova_a_proposta`) com o ok, e registre no histórico das duas.
