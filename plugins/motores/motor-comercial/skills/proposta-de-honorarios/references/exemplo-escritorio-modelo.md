# Exemplo resolvido: proposta do caso 1 do Escritório Modelo

Caso fictício 1 de `../../../docs/casos-ficticios.md` (Marta, auxílio-doença cortado). Todos os valores são **de exemplo**, inventados para mostrar a conta. Não são referência de honorário para nenhum escritório nem para nenhuma seccional. Feito com caso fictício, o arquivo grava em `escritorio/07-operacao/_treino/comercial/propostas/`.

## O que a habilidade recebeu

- **Contato:** C-2026-0001, Marta, previdenciário, auxílio-doença cortado. Etapa `consulta-feita`. Consulta em 2026-03-12 (quinta), online, com a advogada titular.
- **Resumo da ata (três linhas):** o benefício foi cessado e ela segue sem condição de trabalhar. A advogada titular decidiu começar pelo pedido administrativo com os laudos atuais. Se negado, ação judicial, com proposta à parte.
- **Política do Escritório Modelo (exemplo):** pedido administrativo com honorário fixo de 1.800; consulta de 250 abatida; entrada mínima de 30% e até 5 parcelas sem juros; Pix ou boleto; validade de 10 dias corridos; quem aprova é a advogada titular.
- **Fichas:** E: `cidade_uf` Belo Horizonte/MG; tratamento por "você"; tom "próximo, claro, sem pressa". C: `modelo` depende do caso; `formas_de_pagamento` Pix ou boleto; `validade_da_proposta` 10 dias corridos; `follow_up` "proposta sem resposta: 2, 7, 15"; `maximo_de_retornos` 3.

## As perguntas que a habilidade fez (uma por vez)

1. "O trabalho vai até onde: só a fase administrativa, até a sentença, ou inclui recurso e a fase de receber o valor?" Resposta: só a fase administrativa.
2. "A política tem 1.800 para o pedido administrativo, com a consulta de 250 abatida. Vale este valor para este caso ou você ajusta?" Resposta: vale.
3. "Confirma o que fica de fora: ação judicial, recurso administrativo e perícia particular?" Resposta: confirmo.

## A conta (valores de exemplo)

- Total: 1.800 menos 250 da consulta = 1.550.
- Cenário 1: à vista, 1.550 por Pix.
- Cenário 2: entrada de 30% = 465, e 4 parcelas de 271,25 (465 + 4 x 271,25 = 1.550).
- Cenário 3: entrada de 465 e 5 parcelas de 217 (465 + 5 x 217 = 1.550). Máximo da política.

## A proposta (o arquivo .md)

```markdown
---
documento: Proposta de honorários
contato: C-2026-0001
versao: v1
revisado_em: 2026-03-16
dono: advogada titular
mudanca_desta_versao: primeira versão
---

## Antes de enviar (interno, não vai para o cliente)

- Quem aprova: advogada titular · Sigla: A
- Fonte da consulta: 07-operacao/_treino/comercial/consultas/C-2026-0001-2026-03-12.md
- Versão: v1 · o que mudou: primeira versão

**Conferências**

- [x] Valor e cenários: todo número veio da política e a conta fecha.
- [x] Tabela de honorários da seccional da OAB/MG: valor comparado com a tabela vigente `[CONFERIR]`.
- [x] Escopo: as duas listas batem com a ata.
- [x] Validade escrita como data e despesas explicadas.
- [x] Texto sem promessa, prazo de decisão, chance de ganho ou comparação.
- [x] Aprovada pela advogada titular: valor final e condições.

**Pendências**

- nenhuma

<!-- fim: antes de enviar -->

# Proposta de honorários

**Escritório Modelo** · Belo Horizonte/MG · 16 de março de 2026

Para: Marta

Obrigada pela conversa de quinta. Aqui está, por escrito, o que combinamos: o que vamos fazer, o que fica de fora, os valores e como pagar.

## O que você nos trouxe

Seu auxílio-doença foi cortado e você continua sem condição de trabalhar. Você quer pedir de novo o benefício ao INSS.

## O que vamos fazer

- Analisar seus documentos e o histórico do benefício.
- Organizar os laudos e exames que você já tem e dizer o que falta.
- Montar e protocolar o pedido no INSS.
- Acompanhar o pedido e responder às exigências do INSS.
- Preparar você para a perícia do INSS: o que levar e como funciona.
- Avisar você de cada movimentação e explicar o resultado.

## O que não está incluído

- Ação judicial, se o pedido for negado: proposta à parte.
- Recurso administrativo contra a decisão do INSS: proposta à parte.
- Perícia ou laudo particular.
- Despesas com cópias, exames e deslocamento.

Se surgir uma necessidade fora desta lista, a gente conversa antes e manda uma proposta à parte. Nada é cobrado sem o seu de acordo por escrito.

## Como o trabalho anda

1. Você manda os documentos da lista que vamos enviar.
2. A gente monta e protocola o pedido.
3. O INSS marca a perícia. A gente prepara você antes.
4. O INSS decide. A gente explica a decisão e o que dá para fazer depois.

Os prazos de cada etapa dependem do INSS, e não do escritório. A cada etapa, você recebe notícia por WhatsApp.

## Honorários

Valor fixo para a fase administrativa: 1.800, com os 250 da consulta já descontados. Total a pagar: 1.550.

| Forma | Como fica |
|---|---|
| À vista | 1.550 por Pix, na assinatura do contrato |
| Entrada e 4 parcelas | Entrada de 465 e 4 parcelas de 271,25, todo dia 10 |
| Entrada e 5 parcelas | Entrada de 465 e 5 parcelas de 217, todo dia 10 |

Formas de pagamento: Pix ou boleto. Parcelamento sem juros.

## Despesas

Cópias, exames e deslocamentos não estão nos honorários. Antes de qualquer gasto, a gente avisa o valor e o motivo, e você decide.

## Validade

Esta proposta vale até 26 de março de 2026. Depois dessa data, os valores podem ser revistos.

## Próximos passos

1. Se estiver de acordo, é só responder dizendo qual forma de pagamento prefere.
2. A gente envia o contrato de honorários para leitura e assinatura.
3. Entrada ou pagamento à vista, conforme a forma escolhida.
4. Lista de documentos para o pedido.

Fico à disposição para qualquer dúvida.

Advogada titular do Escritório Modelo

---

*Esta proposta descreve o trabalho e os honorários. Ela não garante resultado: a decisão do caso depende do INSS.*
```

(Na proposta real, os valores aparecem com "R$" e a assinatura sai de `dados_para_documentos`. Aqui ficam assim para não parecerem referência.)

## O que o script disse

Na primeira rodada, a conferência da tabela da seccional ainda estava sem marcar:

```
NÃO ESTÁ PRONTO PARA ENVIAR: 1 conferência(s) do "Antes de enviar" sem marcar.
...
Nenhum .docx foi criado: resolva o que está acima e rode de novo.
```

O script saiu com código 2 e não criou o .docx.

A advogada conferiu, marcou `[x]` e rodou de novo:

```
PRONTO PARA ENVIAR: nenhuma pendência no texto que vai ao cliente.
Antes de enviar: 6 item(ns) conferido(s), 0 sem marcar.
OK: .docx criado em ... (sem o cabeçalho interno e sem a seção "Antes de enviar").
```

O `[CONFERIR]` da tabela ficou no cabeçalho interno, onde é lembrete para a equipe. O texto que a Marta recebe não tem nenhuma marcação.

## A mensagem de envio (modelo `envio-de-proposta` da biblioteca)

```
Oi, Marta, tudo bem? Aqui é a advogada do Escritório Modelo.
Como combinamos na consulta, segue a proposta para o seu pedido no INSS.
Nela estão o que vamos fazer, o que não está incluído, os valores e as formas de pagamento.
A proposta vale até 26 de março.
Leia com calma. Se ficar qualquer dúvida, me escreva por aqui ou marcamos uma ligação rápida.
```

## A linha do funil (depois que a secretária confirmou o envio, em 2026-03-16)

```
C-2026-0001,2026-03-09 21:14,whatsapp,indicacao,Marta,novo,previdenciario,auxílio-doença cortado; quer pedir de novo,alta,proposta-enviada,secretaria,retorno 1 de 3,2026-03-18,2026-03-10 09:05,1550,,,nao,2026-03-16
```

`valor_proposta` 1550 já sem a consulta, porque a ficha diz que abate. Retorno 1 em 2 dias corridos (régua "proposta sem resposta"), em 2026-03-18.

## O que a checagem pegou

- Na primeira versão, a ata dizia "boa chance de restabelecer". A frase saiu da proposta: chance de ganho não entra.
- O item "acompanhamento completo" virou quatro itens com verbo e objeto.
- O `[CONFERIR]` da tabela da seccional estava no parágrafo de honorários. Subiu para o "Antes de enviar".
