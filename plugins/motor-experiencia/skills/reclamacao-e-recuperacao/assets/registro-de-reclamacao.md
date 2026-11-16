# Modelo do registro de reclamação

Gravado em `escritorio/07-operacao/experiencia/reclamacoes/<codigo>-AAAA-MM-DD.md`, com a data em que a reclamação chegou. Um arquivo por reclamação. Se o mesmo cliente reclamar de novo, abra outro arquivo e cite o anterior em "Desde quando".

Fatos com data e fonte. Nada de nome de quem errou. O que ninguém sabe fica `[A CONFIRMAR]`, com quem confirma.

```markdown
---
documento: Reclamação
cliente: [CÓDIGO]
aberta_em: AAAA-MM-DD
situacao: aberta            # aberta | combinada | fechada
quem_assume: [FUNÇÃO, de quem_assume_reclamacao]
prazo_de_retorno: [DATA E HORA, de prazo_de_retorno_da_reclamacao]
fechada_em:
---

# Reclamação · [CÓDIGO] · [PRIMEIRO NOME] · AAAA-MM-DD

## O que o cliente disse
"[AS PALAVRAS DELE, ANONIMIZADAS]"
Canal: [whatsapp | e-mail | ligação | pessoalmente | pesquisa] · Hora: [HH:MM]

## Desde quando
- Primeira vez que a queixa aparece: [DATA, FONTE]
- Reclamações anteriores registradas: [ARQUIVOS, ou "nenhuma"]

## O que o escritório fez
| Data | O que foi feito | Fonte |
|---|---|---|
| AAAA-MM-DD | [ATO NO CASO OU CONTATO COM O CLIENTE] | [historico.md, carteira, sistema] |

## O que falhou de fato
| O combinado | O que aconteceu | Fonte |
|---|---|---|
| [EX.: máximo sem notícia de N dias (ficha)] | [EX.: N dias sem notícia] | [carteira, historico.md] |

## O que ainda não se sabe
- [PERGUNTA] `[A CONFIRMAR]` com [QUEM]

## A ligação
- Data e hora: [AAAA-MM-DD HH:MM] · Quem ligou: [FUNÇÃO]
- O que o cliente contou: [RESUMO EM TRÊS LINHAS]
- Roteiro usado: `clientes/[CÓDIGO]/ligacoes/AAAA-MM-DD.md`

## O que foi combinado
| O que muda | Quem faz | Até quando |
|---|---|---|
| [AÇÃO] | [FUNÇÃO] | [DATA] |

O que o escritório ofereceu: [ITENS DA SEÇÃO 6 DA HABILIDADE]
Mensagem de retorno: [enviada em AAAA-MM-DD | na fila | não enviada, por quê]
Próximo contato combinado: AAAA-MM-DD

## Causa e ajuste
- Causa: [UMA DAS CAUSAS DE references/causas-e-ajustes.md, em uma frase]
| Proposta | Destino | Decisão |
|---|---|---|
| [O QUE MUDA] | [jornada | ficha | biblioteca | aprendizado | carteira] | [sim | não | depois] |

## Fechamento
- Combinado cumprido em: AAAA-MM-DD · Confirmado por: [FUNÇÃO]
- Como o cliente está: [UMA PALAVRA, a leitura de quem falou com ele]
```

## Regras do registro

1. **Mínimo de dados.** Sem CPF, sem número do processo, sem endereço. Dado de saúde só se a queixa depender dele, e em uma palavra ("intercorrência de saúde").
2. **Sem nomes da equipe.** Função, nunca a pessoa. "A mensagem de 2026-02-20 prometeu retorno e o retorno não aconteceu", nunca "a secretária não retornou".
3. **Falha é contra um combinado.** Ficha, jornada, aprendizado ou algo que alguém do escritório disse ao cliente. Sem combinado, o ponto sai de "o que falhou de fato" e entra na causa, como "expectativa criada sem combinado".
4. **Situação muda com a pessoa.** `aberta` quando alguém assume; `combinada` depois da ligação; `fechada` quando o combinado foi cumprido e quem assumiu confirma.
