# Como o painel calcula e como ler

## 1. Regras do cálculo

O script `painel_carteira.py` segue estas regras. Quem calcular à mão segue as mesmas.

| Medida | Regra |
|---|---|
| Ativo | `fase` diferente de `encerrado` |
| Encerrado no mês | `fase = encerrado` e `encerrado_em` no mês da data de referência |
| Dias sem notícia | data de referência menos `ultimo_contato`, em dias corridos, só para ativos (`docs/carteira.md`, regra 1) |
| Além do máximo | dias sem notícia maior que `maximo_sem_noticia` |
| Faixas | 0 a 7, 8 a 15, 16 a 30, 31 a 60, mais de 60 dias. Faixas fixas para comparar mês a mês; o modo adaptar pode mudar, e a mudança vale dali para a frente |
| Os piores | os ativos com mais dias sem notícia: no mínimo 5, e todos os que passaram do máximo |
| Compromissos | `data_compromisso` de ativos: de 0 a 7 dias, de 8 a 30 dias, e data já passada (linha não atualizada) |
| Documentos | ativos com `documentos_pendentes` maior que zero, e a soma |
| Reclamações | `reclamacao_aberta = sim` (qualquer fase) |
| Insatisfeitos | ativos com `humor = insatisfeito`, marcando quem não tem reclamação registrada |
| Satisfação | coluna `satisfacao` de 0 a 10: quantas notas, média, mediana, faixas 0 a 6, 7 e 8, 9 e 10; notas até 6 listadas |
| Recebe resumo | ativo com `resumo_mensal = sim` e `pediu_para_nao_receber` diferente de `sim` |
| Contato vencido | ativo com `proximo_contato` antes da data de referência |
| Sem próximo contato | ativo com `proximo_contato` vazio |

Leitura do arquivo: vírgula ou ponto e vírgula, com ou sem BOM, nomes de coluna e opções sem diferenciar maiúscula nem acento ("Aguardando" vale "aguardando"), datas AAAA-MM-DD ou DD/MM/AAAA. Opções de sim aceitas: sim, s, x.

O que o script não faz: não lê feriado (os dias são corridos, como a régua), não lê o histórico do cliente (só a carteira), não sabe se houve ligação que ninguém registrou. Por isso a carteira desatualizada aparece como "sem notícia": o painel acerta se a carteira estiver em dia, e o aviso de preenchimento ajuda a deixá-la assim.

## 2. Como escrever as três leituras

Uma leitura é um fato com número, de onde ele vem, e o que ele quer dizer para a régua. Sem adjetivo, sem causa que o dado não mostra.

| Em vez de | Escreva |
|---|---|
| "A carteira está ruim." | "2 de 8 ativos passaram de 30 dias sem notícia." |
| "A secretária não está dando conta." | "Os 3 contatos vencidos são de documento e resumo mensal; o mais antigo venceu há 19 dias." |
| "Os clientes estão felizes." | "4 notas registradas, mediana 8,5; uma nota 5 sem reclamação registrada." |
| "O previdenciário está abandonado." | "Os dois clientes além do máximo são do previdenciário, um em cumprimento e um aguardando perícia." |

Leitura boa compara quando pode: com o painel anterior ("eram 4 além do máximo no mês passado, agora são 2") ou com a ficha ("a ficha diz resumo mensal no dia 5; 1 cliente que recebe resumo está há 36 dias sem notícia").

Se a causa importa e o dado não mostra, escreva como pergunta: "Por que os resumos de abril não saíram para quem está aguardando perícia?".

## 3. Como escrever as três ações

Uma ação por leitura. Cada uma com:
- **o que fazer**, com verbo e objeto ("dar notícia a Jorge e Marta");
- **dono** (função);
- **até quando**;
- **a habilidade que cuida** (ou "à mão", se não estiver instalada).

Ações que o painel não propõe: avaliar uma pessoa, mudar honorário, contatar quem pediu para não receber rotina com mensagem de rotina (para essas pessoas, só notícia relevante, do jeito que preferem).

## 4. Exemplo com a carteira de treino (2026-04-10, máximo 30 dias)

Leituras:
1. 2 de 8 ativos passaram de 30 dias sem notícia: Jorge (49) e Marta (36), os dois do previdenciário.
2. Jorge está insatisfeito e não tem reclamação registrada.
3. Duas datas nos próximos 7 dias: audiência do Paulo amanhã e perícia da Marta em 4 dias; Marta é a mesma cliente sem notícia há 36 dias.

Ações:
| Ação | Dono | Até | Habilidade |
|---|---|---|---|
| Registrar a reclamação do Jorge e a advogada ligar | advogada | hoje | `reclamacao-e-recuperacao` |
| Notícia para Marta junto com a preparação da perícia | advogada | hoje | `status-para-o-cliente`, `preparar-o-cliente` |
| Confirmar a preparação do Paulo para a audiência | advogada | hoje | `preparar-o-cliente` |
