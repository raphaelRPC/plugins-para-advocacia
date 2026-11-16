---
documento: Mapa da peça
peca: peticao-inicial-restabelecimento
area: previdenciario
versao: 1
revisado_em: 2026-04-16
dono: advogada titular
---

# Mapa da peça · Petição inicial de restabelecimento de benefício por incapacidade (JEF)

> Exemplo resolvido, Escritório Modelo, fictício. Saiu das peças P1 a P3 desta pasta, do mapa bruto do script e de seis respostas da advogada titular. Nenhuma pessoa, número ou julgado daqui existe.

## 1. Origem
| Peça | O que era | Por que entrou |
|---|---|---|
| P1 | Inicial de restabelecimento, JEF de BH, segurado pedreiro, 2025 | A estrutura que o escritório usa desde 2024 |
| P2 | A mesma peça, segurada diarista sem outra renda, com tutela de urgência, 2025 | A única com tutela: mostra a exceção |
| P3 | A mesma peça, segurada auxiliar de limpeza, 2025 | Confirma o que é fixo |

## 2. Estrutura
| Ordem | Parte | Fixa ou condicional | Observação |
|---|---|---|---|
| 1 | Endereçamento | fixa | O juízo vem da ficha |
| 2 | Qualificação e nome da ação | fixa | A qualificação sai do sistema do escritório, como campo de quem protocola |
| 3 | 1. DOS FATOS (1.1 a 1.5) | fixa | Um fato por parágrafo, com o documento |
| 4 | Fato 1.6 (sem outra renda) | condicional: `pedir_tutela = sim` | |
| 5 | 2. DOS FUNDAMENTOS (2.1 a 2.3) | fixa | |
| 6 | Fundamento 2.4 (tutela) | condicional: `pedir_tutela = sim` | Decisão da advogada: a tutela vira o item 2.4, e não uma seção própria como em P2, para a numeração das seções não mudar |
| 7 | 3. DOS PEDIDOS | fixa, com o pedido de tutela condicional em primeiro | A numeração dos pedidos é refeita na montagem |
| 8 | 4. DAS PROVAS | fixa | |
| 9 | 5. DO VALOR DA CAUSA | fixa | Valor da conta do advogado |
| 10 | Local, data e assinatura | fixa | A data é de quem protocola |

## 3. Variáveis
| variavel | tipo | origem | obrigatoria | exemplo | regra |
|---|---|---|---|---|---|
| genero | genero | cliente | sim | f | f ou m; P1 tinha "o autor", P2 e P3 "a autora" |
| nome_curto | texto | cliente | sim | Marta | Só no cabeçalho interno e no nome do arquivo; nunca no corpo |
| funcao | texto | dossie | sim | auxiliar de cozinha | A do último vínculo, igual no extrato de vínculos e na carteira |
| inicio_vinculo | mes | dossie | sim | 06/2019 | Do extrato de vínculos |
| fim_vinculo | mes | dossie | sim | 09/2025 | Do extrato de vínculos |
| data_cessacao | data | dossie | sim | 28/02/2026 | Se dois documentos dão datas diferentes, para (seção 7) |
| data_relatorio | data | dossie | sim | 20/01/2026 | Relatório anterior à cessação: avisa "pedir relatório atual" |
| pedir_tutela | opcao(sim/nao) | advogado | sim | nao | Só o advogado decide; "sim" acrescenta 1.6, 2.4 e o pedido de tutela |
| documentos | lista | dossie | sim | carta de cessação; negativa da prorrogação; extrato de vínculos; relatório médico; resumo da perícia | Na ordem de juntada |
| valor_causa | valor | advogado | sim | R$ 18.000,00 | Da conta em anexo; a habilidade nunca estima |
| juizo | texto | ficha | sim | JUIZADO ESPECIAL FEDERAL DE BELO HORIZONTE/MG | |
| cidade | texto | ficha | sim | Belo Horizonte | |
| assinatura | texto | ficha | sim | Advogada titular do Escritório Modelo, OAB/MG 00.000 | |

### Valores do escritório
- juizo: JUIZADO ESPECIAL FEDERAL DE BELO HORIZONTE/MG
- cidade: Belo Horizonte
- assinatura: Advogada titular do Escritório Modelo, OAB/MG 00.000 (exemplo fictício)

## 4. Teses
| tese | quando entra | arquivo | citações |
|---|---|---|---|
| restabelecimento-incapacidade | Sempre: é a tese desta peça, definida pelo advogado em cada caso | `04-base/juridico/teses/restabelecimento-incapacidade.md` | seção 9, itens 1 e 2 |
| tutela de urgência por falta de renda | Só com `pedir_tutela = sim` | sem arquivo próprio ainda (sugestão: criar no banco de teses) | seção 9, item 3 |

## 5. Trechos padrão
### T1 · abertura
{QUALIFICAÇÃO COMPLETA}, vem, por sua advogada, propor AÇÃO DE RESTABELECIMENTO DE BENEFÍCIO POR INCAPACIDADE TEMPORÁRIA contra o INSTITUTO NACIONAL DO SEGURO SOCIAL, pelos fatos e fundamentos a seguir.

### T2 · perícia que não enfrenta o relatório
A perícia administrativa concluiu pela capacidade sem mencionar esse relatório (doc. 5).

### T3 · fecho dos pedidos
O restabelecimento do benefício desde a cessação, com fundamento no item 2.1 e nos fatos 1.2 a 1.5.

## 6. Escolhas de estilo
- Um fato por parágrafo, numerado 1.1, 1.2, com o documento no fim: "(doc. 3)".
- Pedidos numerados, cada um com o item do fundamento e os fatos ao lado.
- "A autora" ou "o autor"; nunca "a requerente" nem "a segurada" nesta peça.
- Datas em DD/MM/AAAA; meses em MM/AAAA.
- Sem latim, sem adjetivo sobre o INSS ou sobre o perito, sem "data venia".
- Sem fecho "Nestes termos, pede deferimento".
- A limitação aparece como "sem condição para atividade com esforço físico"; o diagnóstico nunca entra.

## 7. Exceções e quando parar
| Situação | O que a habilidade faz |
|---|---|
| Dois documentos com datas de cessação diferentes | Para de escolher: marca `[A CONFIRMAR]` com os dois documentos e leva ao advogado. No lote, a linha não sai até alguém decidir a data |
| Relatório médico anterior à cessação | Monta e põe no "Antes de protocolar": pedir relatório atual ao cliente |
| Sem tese definida pelo advogado | Para. O caso vai para a `estrategia-do-caso` |
| Área diferente de previdenciário, ou outra peça (recurso, réplica, concessão) | Para: esta habilidade só faz a inicial de restabelecimento; outra peça vai para a `minutar-peca` |
| Benefício nunca concedido | Para: é pedido de concessão, outra peça e outra tese |
| Cliente sem renda, com doença grave ou com dependente sem sustento | Monta só o que o advogado decidiu; marca a vulnerabilidade para ele (H); tutela só com `pedir_tutela = sim` |
| Pedido de dano moral, ou qualquer pedido fora do modelo | Não acrescenta. Pedido novo é decisão do advogado e sai pela `minutar-peca` |

## 8. Modelo da peça
<!-- modelo: inicio -->
# EXCELENTÍSSIMO SENHOR JUIZ FEDERAL DO {{juizo}}

{QUALIFICAÇÃO COMPLETA}, vem, por sua advogada, propor AÇÃO DE RESTABELECIMENTO DE BENEFÍCIO POR INCAPACIDADE TEMPORÁRIA contra o INSTITUTO NACIONAL DO SEGURO SOCIAL, pelos fatos e fundamentos a seguir.

## 1. DOS FATOS

1.1. {{genero:A autora|O autor}} trabalhou como {{funcao}} de {{inicio_vinculo}} a {{fim_vinculo}}, com contribuições em dia (doc. 3).

1.2. Recebia auxílio por incapacidade temporária, cessado em {{data_cessacao}} por "não constatação de incapacidade" (doc. 1).

1.3. O pedido de prorrogação foi negado (doc. 2).

1.4. O relatório do médico assistente de {{data_relatorio}} diz que {{genero:a autora|o autor}} segue sem condição para atividade com esforço físico, sem prazo de melhora (doc. 4).

1.5. A perícia administrativa concluiu pela capacidade sem mencionar esse relatório (doc. 5).

{{#se pedir_tutela=sim}}
1.6. Desde a cessação, {{genero:a autora|o autor}} não tem outra renda (doc. 6).
{{/se}}

## 2. DOS FUNDAMENTOS

2.1. O benefício é devido enquanto durar a incapacidade para a atividade habitual, nos termos do art. 59 da Lei 8.213/1991 [CONFERIR: vigência e redação na data dos fatos].

2.2. A conclusão pericial que não enfrenta o relatório do médico assistente não afasta a prova da incapacidade (TRF6, Apelação Cível nº 0000001-00.2024.4.06.0000) [CONFERIR: julgado das peças de origem; conferir no Jus IA e no inteiro teor, ou trocar por um do tema da base].

2.3. A função de {{funcao}} exige esforço físico contínuo (doc. 3), o que torna a limitação do doc. 4 incompatível com a atividade habitual.

{{#se pedir_tutela=sim}}
2.4. A prova da incapacidade (doc. 4) e a falta de outra renda (doc. 6) justificam o restabelecimento imediato, nos termos do art. 300 do Código de Processo Civil [CONFERIR: requisitos da tutela de urgência e redação vigente].
{{/se}}

## 3. DOS PEDIDOS

Diante do exposto, requer:

{{#se pedir_tutela=sim}}
1. A tutela de urgência para restabelecer o benefício já, com fundamento no item 2.4 e nos fatos 1.4 e 1.6.
{{/se}}
1. O restabelecimento do benefício desde a cessação, com fundamento no item 2.1 e nos fatos 1.2 a 1.5.
2. A realização de perícia médica judicial, com fundamento no item 2.2 e no fato 1.5.
3. O pagamento das parcelas vencidas desde a cessação, com correção, com fundamento no item 2.1.

## 4. DAS PROVAS

Documentos juntados: {{documentos}}{{#se pedir_tutela=sim}}; comprovante de que não há outra renda{{/se}}. Requer perícia médica judicial.

## 5. DO VALOR DA CAUSA

Dá-se à causa o valor de {{valor_causa}}, conforme a conta em anexo.

{{cidade}}, {DATA DO PROTOCOLO}.

{{assinatura}}
<!-- modelo: fim -->

## 9. Citações
| # | Citação | Onde aparece no modelo | Marca |
|---|---|---|---|
| 1 | art. 59 da Lei 8.213/1991 | 2.1 | [CONFERIR: vigência e redação na data dos fatos] |
| 2 | TRF6, Apelação Cível nº 0000001-00.2024.4.06.0000 | 2.2 | [CONFERIR: veio das peças de origem; no treino, sai vermelho, porque não existe] |
| 3 | art. 300 do Código de Processo Civil | 2.4, só com tutela | [CONFERIR: requisitos e redação vigente] |

## 10. Histórico
| Data | Versão | O que mudou | Por quê |
|---|---|---|---|
| 2026-04-16 | 1 | Criada a partir de P1 a P3 | Primeira habilidade própria do escritório |
