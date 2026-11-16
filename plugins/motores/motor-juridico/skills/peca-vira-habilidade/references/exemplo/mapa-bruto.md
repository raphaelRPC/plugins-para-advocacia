# Mapa bruto · 3 peças comparadas

> Rascunho do script mapear_pecas.py. Não é o mapa da peça: a habilidade e o advogado revisam, dão nome às variáveis, decidem as exceções e conferem cada citação. Nada daqui vale como regra sem o ok.

## Peças lidas

| # | Arquivo | Títulos | Parágrafos |
|---|---|---|---|
| P1 | peca-1.md | 6 | 17 |
| P2 | peca-2.md | 7 | 20 |
| P3 | peca-3.md | 6 | 17 |

## Estrutura (títulos)

| Título | Em quais peças | Classe |
|---|---|---|
| EXCELENTÍSSIMO SENHOR JUIZ FEDERAL DO JUIZADO ESPECIAL FEDERAL DE BELO HORIZONTE/MG | P1, P2, P3 | fixo |
| DOS FATOS | P1, P2, P3 | fixo |
| DOS FUNDAMENTOS | P1, P2, P3 | fixo |
| DOS PEDIDOS | P1, P2, P3 | fixo |
| DAS PROVAS | P1, P2, P3 | fixo |
| DO VALOR DA CAUSA | P1, P2, P3 | fixo |
| DA TUTELA DE URGÊNCIA | P2 | só nesta peça |

## Trechos fixos (iguais em todas as peças)

Candidatos a trecho padrão. Confira se são mesmo do escritório ou se só se repetiram nestas peças.

F1. [CLIENTE], [QUALIFICAÇÃO], vem, por sua advogada, propor AÇÃO DE RESTABELECIMENTO DE BENEFÍCIO POR INCAPACIDADE TEMPORÁRIA contra o INSTITUTO NACIONAL DO SEGURO SOCIAL, pelos fatos e fundamentos a seguir.

F2. 1.3. O pedido de prorrogação foi negado (doc. 2).

F3. 1.5. A perícia administrativa concluiu pela capacidade sem mencionar esse relatório (doc. 5).

F4. 2.1. O benefício é devido enquanto durar a incapacidade para a atividade habitual, nos termos do art. 59 da Lei 8.213/1991.

F5. 2.2. A conclusão pericial que não enfrenta o relatório do médico assistente não afasta a prova da incapacidade (TRF6, Apelação Cível nº 0000001-00.2024.4.06.0000, fictício).

F6. Diante do exposto, requer:

F7. 1. O restabelecimento do benefício desde a cessação, com fundamento no item 2.1 e nos fatos 1.2 a 1.5.

F8. 2. A realização de perícia médica judicial, com fundamento no item 2.2 e no fato 1.5.

F9. 3. O pagamento das parcelas vencidas desde a cessação, com correção, com fundamento no item 2.1.

F10. Advogada titular do Escritório Modelo, OAB/MG 00.000

## Trechos fixos com variáveis

O texto da primeira peça, com {{variavel}} no lugar do que muda. Os nomes são sugestão: renomeie no mapa.

V1. 1.1. {{genero}} trabalhou como {{texto_trabalhou}} de {{competencia_inicio}} a {{competencia_fim}}, com contribuições em dia (doc. 3).

V2. 1.2. Recebia auxílio por incapacidade temporária, cessado em {{data_cessacao}} por "não constatação de incapacidade" (doc. 1).

V3. 1.4. O relatório do médico assistente de {{data_relatorio}} diz que {{genero_2}} segue sem condição para atividade com esforço físico, sem prazo de melhora (doc. 4).

V4. 2.3. A função de {{texto_funcao}} exige esforço físico contínuo (doc. 3), o que torna a limitação do doc. 4 incompatível com a atividade habitual.

V5. Documentos 1 a {{numero_documentos}} e perícia médica judicial.

V6. Dá-se à causa o valor de {{valor_causa}}, conforme a conta em anexo (doc. {{numero_doc}}).

V7. Belo Horizonte, {{data_da_peca}}.

## Variáveis sugeridas

| Variável (sugestão) | Tipo provável | Trecho | P1 | P2 | P3 |
|---|---|---|---|---|---|
| genero | genero | V1 | O autor | A autora | A autora |
| texto_trabalhou | texto | V1 | pedreiro | diarista | auxiliar de limpeza |
| competencia_inicio | mes | V1 | 03/2015 | 08/2012 | 01/2018 |
| competencia_fim | mes | V1 | 11/2024 | 02/2025 | 05/2025 |
| data_cessacao | data | V2 | 10/01/2025 | 15/04/2025 | 30/06/2025 |
| data_relatorio | data | V3 | 05/12/2024 | 28/03/2025 | 02/06/2025 |
| genero_2 | genero | V3 | o autor | a autora | a autora |
| texto_funcao | texto | V4 | pedreiro | diarista | auxiliar de limpeza |
| numero_documentos | numero | V5 | 5 | 6 | 5 |
| valor_causa | valor | V6 | R$ 21.400,00 | R$ 17.850,00 | R$ 19.120,00 |
| numero_doc | numero | V6 | 6 | 7 | 6 |
| data_da_peca | data | V7 | 03/02/2025 | 12/05/2025 | 21/07/2025 |

Marcas de anonimização que viram variável com origem no cliente ou no sistema do escritório: [CLIENTE], [QUALIFICAÇÃO]

## Trechos que aparecem em algumas peças (exceções)

Para cada um, pergunte ao advogado quando ele entra. Vira bloco condicional no modelo ou fica fora.

## Trechos só de uma peça

Fato específico do caso ou escolha daquela peça. Se for exceção que se repete em outros casos, vira bloco condicional.

U1 (P2). 1.6. Desde a cessação, a autora não tem outra renda (doc. 6).

U2 (P2). 3.1. A prova da incapacidade (doc. 4) e a falta de outra renda (doc. 6) justificam o restabelecimento imediato, nos termos do art. 300 do Código de Processo Civil.

U3 (P2). 1. A tutela de urgência para restabelecer o benefício já, com fundamento no item 3.1 e nos fatos 1.4 e 1.6.

## Citações encontradas

Todas entram no mapa com a marca. A conferência é da conferir-citacoes, na fonte (`citacoes.md`).

| Citação como está | Em quais peças | Marca no mapa |
|---|---|---|
| TRF6, Apelação Cível nº 0000001-00.2024.4.06.0000 | P1, P2, P3 | [CONFERIR: existe, vigente, diz o que a peça diz] |
| art. 59 da Lei 8.213/1991 | P1, P2, P3 | [CONFERIR: existe, vigente, diz o que a peça diz] |
| art. 300 do Código de Processo Civil | P2 | [CONFERIR: existe, vigente, diz o que a peça diz] |

## Alertas de dados

- Nenhum CPF, telefone, e-mail ou número de processo fora de citação encontrado. Confira nomes à mão.

## Resumo

7 títulos e 20 grupos de parágrafos: 10 fixos, 7 fixos com variáveis, 0 em algumas peças, 3 só de uma peça; 12 variáveis sugeridas; 3 citações para conferir; 0 alertas de dados.
