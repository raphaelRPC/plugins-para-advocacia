# Exemplo resolvido: o Jorge (caso fictício)

Mensagem 6 de `../../../docs/casos-ficticios.md`. Escritório Modelo, Belo Horizonte/MG. Hoje é sexta, 2026-04-10. Tudo deste exemplo grava em `escritorio/07-operacao/_treino/experiencia/`. Nenhuma pessoa, número ou processo existe.

## A mensagem

Jorge (C-2025-0088, previdenciário, aposentadoria por idade, fase `cumprimento`), 11h15:

> "Já é a terceira vez que eu pergunto e ninguém me dá uma resposta. Vou procurar a OAB."

Na carteira: `ultimo_contato = 2026-02-20`, `humor = insatisfeito`, `reclamacao_aberta = nao`. Observação: reclamou da demora em fevereiro.

## Passo 1. O que para tudo
Nada de violência, saúde ou vulnerabilidade. Não há sinal de falha jurídica, mas a advogada confirma em `[A CONFIRMAR]` se o cumprimento andou como deveria. Segue.

## Passo 2. Dono e prazo
Ficha do Escritório Modelo: reclamação é da advogada titular, ligação no mesmo dia útil. Quem assume: advogada titular. Prazo: hoje, até as 18h.

## Passo 3. Resposta-ponte
A advogada está em audiência até as 14h, então sai a ponte (A, ela lê no intervalo e a secretária envia):

> "Oi, Jorge. Li sua mensagem. A Dra. vai te ligar hoje até as 16h para conversar com calma."

## Passo 4. O registro

`_treino/experiencia/reclamacoes/C-2025-0088-2026-04-10.md`:

```markdown
---
documento: Reclamação
cliente: C-2025-0088
aberta_em: 2026-04-10
situacao: aberta
quem_assume: advogada titular
prazo_de_retorno: 2026-04-10 até 18h
fechada_em:
---

# Reclamação · C-2025-0088 · Jorge · 2026-04-10

## O que o cliente disse
"Já é a terceira vez que eu pergunto e ninguém me dá uma resposta. Vou procurar a OAB."
Canal: whatsapp · Hora: 11h15

## Desde quando
- Primeira vez que a queixa aparece: 2026-02-20, "Já faz tempo que ganhei e até agora nada" (conversa do WhatsApp)
- Reclamações anteriores registradas: nenhuma (a queixa de fevereiro não foi registrada)

## O que o escritório fez
| Data | O que foi feito | Fonte |
|---|---|---|
| 2026-02-20 | Resposta: "Vou ver com a Dra. e te retorno" | conversa |
| [A CONFIRMAR] | Atos no cumprimento desde a decisão | sistema do escritório, com a advogada |

## O que falhou de fato
| O combinado | O que aconteceu | Fonte |
|---|---|---|
| Máximo de 30 dias sem notícia (ficha) | 49 dias sem notícia (2026-02-20 a 2026-04-10) | carteira |
| "Te retorno" de 2026-02-20 | O retorno não aconteceu | conversa |
| Primeira resposta a cliente ativo em até 4 horas úteis (ficha) | Cobranças de 2026-03-05 e 2026-03-24 sem resposta | conversa |
| Queixa vira registro com dono | A queixa de fevereiro ficou sem registro e sem dono | carteira (reclamacao_aberta = nao) |

## O que ainda não se sabe
- O que andou no cumprimento desde a decisão, e o que falta para o pagamento `[A CONFIRMAR]` com a advogada
- Se alguém ligou para ele nesse período fora do WhatsApp `[A CONFIRMAR]` com a secretária
```

A advogada confirma: ninguém ligou; o cumprimento está aguardando o INSS implantar o benefício, e a conta dos valores atrasados está em conferência `[CONFERIR]` no sistema.

## Passo 5. O roteiro (trechos)

- **Reconhecer:** "Você tem razão em cobrar. Você ficou 49 dias sem notícia, e o nosso combinado é de no máximo 30. Em fevereiro a gente disse que ia te retornar e não retornou. Isso falhou do nosso lado."
- **Explicar:** "A sua aposentadoria foi reconhecida na decisão. Agora estamos na fase de cumprimento: é quando o INSS precisa colocar o benefício para pagar e quando se faz a conta do que ficou para trás. A gente acompanha e cobra. O tempo do INSS a gente não controla, então eu não vou te dar uma data que eu não sei."
- **Se falar da OAB:** "É um direito seu, e eu respeito. Eu quero primeiro te mostrar o que foi feito e corrigir o que é nosso."

## Passo 6. O que oferecer
Ficha do Escritório Modelo sem `o_que_o_escritorio_oferece` preenchido: a lista-base aparece com `[A DEFINIR]` e a advogada escolhe na hora:
- explicação por escrito do que já foi feito no cumprimento e do que falta;
- notícia a cada 15 dias até o pagamento, mesmo sem novidade;
- prioridade na resposta enquanto a reclamação estiver aberta.
Nada de desconto. O caso não teve falha jurídica.

## Passo 7. A mensagem do que foi combinado

A ligação acontece às 15h40. Jorge contou que achou que o escritório tinha "esquecido" dele depois da vitória. Ficou combinado o que está na mensagem. A advogada lê e envia (A):

> "Oi, Jorge. Obrigada pela conversa de hoje e por me contar tudo com franqueza.
>
> Como combinamos:
> 1. Até segunda, te mando por escrito o que já foi feito desde a decisão e o que falta para o pagamento.
> 2. Até o pagamento sair, você recebe notícia nossa a cada 15 dias, mesmo sem novidade. A próxima é no dia 24/04.
> 3. Se quiser falar antes, é por aqui, e eu mesma respondo.
>
> Você tinha razão em cobrar. A partir de hoje, isso muda.
>
> {NOME DA ADVOGADA}, Escritório Modelo"

`{NOME DA ADVOGADA}` é campo do envio: a ficha fictícia não traz o nome, então quem envia preenche. Com `assinatura_das_mensagens` preenchida na ficha, a assinatura sai dali.

## Passo 8. Carteira e histórico (com a advogada)

| Coluna | Antes | Depois |
|---|---|---|
| `reclamacao_aberta` | nao | sim |
| `ultimo_contato` | 2026-02-20 | 2026-04-10 |
| `ultimo_contato_tipo` | mensagem | ligacao |
| `proximo_contato` | 2026-03-22 | 2026-04-24 |
| `motivo_proximo_contato` | maximo-sem-noticia | retorno-combinado |
| `humor` | insatisfeito | insatisfeito (a advogada prefere esperar o primeiro retorno cumprido) |
| `atualizado_em` | 2026-02-20 | 2026-04-10 |

Histórico (linha de contato; é ela que tira o Jorge de PESSOA AGORA): `| 2026-04-10 15h40 | ligacao | advogada | reclamação da demora; combinado relato por escrito até 2026-04-13 e notícia a cada 15 dias até o pagamento |`. Quando a advogada conferir de novo a fase de cumprimento e pedir ao INSS a implantação, cada ato entra como linha de trabalho do escritório (canal `trabalho-do-escritorio`), e é dali que sai o relato por escrito.

Registro: `situacao: combinada`. Fecha quando o relato por escrito saiu e o contato de 2026-04-24 aconteceu, com a advogada confirmando.

## Passo 9. Causa e ajuste

Causa principal: **fase sem contato na jornada** (depois da decisão favorável, a jornada da aposentadoria não previa contato no cumprimento). Secundária: **"te retorno" sem dono nem hora**.

| Proposta | Destino | Decisão |
|---|---|---|
| Fase `cumprimento` ganha notícia a cada 15 dias até o pagamento | `jornada-aposentadoria-por-idade.md` | sim |
| "Recebi, te retorno até [HORA]" sempre com hora e com `proximo_contato` na carteira | biblioteca, aprendizado | sim |
| "Queixa de demora, mesmo leve, abre registro de reclamação no mesmo dia" | aprendizado | sim |
| Ver quem mais está em `cumprimento` ou além do máximo | carteira | sim: Marta (36 dias) aparece, e a secretária prepara a notícia dela pela `status-para-o-cliente` |

## Passo 10. Aprender
A advogada corrige: "No roteiro, não diga 'colocar o benefício para pagar'; diga 'começar a pagar o benefício todo mês'." Vira aprendizado, com o ok: "Na fase de cumprimento previdenciário, explicar como 'o INSS começar a pagar o benefício todo mês e pagar o que ficou para trás'."

## O que este exemplo testa
- A reclamação vai para uma pessoa no mesmo dia; a IA não responde com desculpa pronta.
- A ida à OAB é tratada como direito, sem pedido para desistir.
- O registro mostra a falha contra a régua, sem nome de quem errou.
- O combinado tem data, e a carteira só muda com a advogada.
- A causa muda a jornada e acha outro cliente na mesma situação.
