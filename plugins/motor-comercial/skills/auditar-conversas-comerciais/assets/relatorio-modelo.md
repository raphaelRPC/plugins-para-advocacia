# Modelo do relatório da auditoria comercial

Gravado em `escritorio/07-operacao/comercial/auditorias/AAAA-MM-DD.md`, com a data do dia da auditoria. Treino grava em `escritorio/07-operacao/_treino/comercial/auditorias/`. Primeiro o modelo, depois o exemplo preenchido com o Escritório Modelo.

## O modelo

```markdown
---
documento: Auditoria comercial AAAA-MM-DD
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Auditoria comercial · AAAA-MM-DD

- Período das conversas: [DE] a [ATÉ]
- Amostra: [N] conversas sorteadas pelo registro.py ([N] que não fecharam; [N] em negociação; [N] que pediram para parar; [N] outros contatos novos) e [N] apontadas pelo registro; [N] automáticas, se o assistente estiver ligado.
- Régua: ficha do escritório versão [N], ficha comercial versão [N], aprendizados versão [N], biblioteca comercial versão [N][, nicho versão N][, instruções do assistente versão N]
- Tempos: tempos.py | medidos à mão · Registro: registro.py | conferido à mão
- Quem leu: a habilidade; quem conferiu os achados críticos: [FUNÇÃO DO ADVOGADO]

## Resumo
[Cinco linhas, no máximo: achados por gravidade, o padrão principal, a proposta mais importante.]

## Tempos
[Resumo do tempos.py: primeira resposta dentro do prazo, maior espera, conversas que terminam sem retorno, retornos acima do máximo, mensagens depois do pedido para parar.]

## O que o registro já mostrava
[A tabela "O que o registro já mostra" do registro.py, com o que a conversa confirmou ou desmentiu.]

## Achados críticos
[Um bloco por achado, no formato de references/criterios-da-auditoria.md. Diga quando o advogado foi avisado e o que decidiu fazer com a pessoa.]

## Achados altos

## Achados médios e baixos
[Só os padrões, agrupados: "frase da lista do que nunca usamos: 3 conversas".]

## Comparação com a auditoria anterior
| Achado | Antes | Agora |
|---|---|---|

## Propostas
| N | Destino | O que muda | Por quê | Decisão |
|---|---|---|---|---|

## Revisão dos aprendizados
[A tabela de mudanças de references/revisao-dos-aprendizados.md, com a decisão.]

## Registro de contatos
[Linhas do contatos.csv que a auditoria propõe atualizar, com a decisão.]

## Próxima auditoria
- Data: [AAAA-MM-DD]
- Conferir de novo: [achados altos e críticos desta]
```

## Exemplo preenchido · Escritório Modelo (fictício)

```markdown
---
documento: Auditoria comercial 2026-04-02
versao: 1
revisado_em: 2026-04-02
dono: secretaria
---

# Auditoria comercial · 2026-04-02

- Período das conversas: 2026-03-01 a 2026-03-31
- Amostra: 10 conversas sorteadas pelo registro.py (3 que não fecharam; 2 em negociação; 2 que pediram para parar; 3 outros contatos novos) e 1 apontada pelo registro (C-2026-0011, sem resposta). Assistente não ligado.
- Régua: ficha do escritório 0.3, ficha comercial 0.3, aprendizados 2, biblioteca comercial 0.2
- Tempos: tempos.py, horário 09:00-18:00, seg-sex, prazo de 2 horas úteis, máximo de 3 retornos
- Quem leu: a habilidade; quem conferiu os achados críticos: advogada titular

## Resumo
1 achado crítico, 6 altos e 2 padrões médios. O padrão principal é a régua que não para: uma mensagem saiu uma semana depois de um pedido para parar, um contato recebeu quatro retornos seguidos com "última chance" e dois contatos fora da régua ainda tinham retorno marcado. A proposta mais importante: o pedido de parar desarma a régua na hora, no registro e na fila.

## Tempos
| Medida | Valor |
|---|---|
| Primeira resposta de pessoa dentro do prazo | 9 de 10 com resposta |
| Conversas que terminam sem retorno | 1 (C-2026-0011, há 137,2 h úteis; só a automática respondeu) |
| Retornos acima do máximo da ficha (3) | 1 (C-2026-0014, 4 retornos seguidos sem resposta) |
| Escritório escreveu depois de confirmar o pedido para parar | 1 (C-2026-0009) |

## O que o registro já mostrava
- C-2026-0011 sem resposta de uma pessoa: a conversa confirma (achado 4).
- C-2026-0017 pediu para parar e ainda tinha "retorno 2 de 3": a conversa não teve mensagem depois, mas o próximo retorno sairia (achado 6).
- C-2026-0004, fora da área, com "retorno 1 de 3": encaminhado com urgência, não podia estar na régua (achado 7).
- C-2026-0014 perdido por sem-resposta: a conversa mostra que o escritório insistiu além da régua (achado 5).

## Achados críticos

Achado 1 · crítica · critério 9
Conversa: C-2026-0009 · contato antigo · whatsapp
Trecho: "Oi! Passando para lembrar que ainda temos horários de consulta esta semana." (uma semana depois do pedido para parar e da confirmação)
Por que importa: mensagem a quem pediu para parar (regras, ética, item 3; funil.md, regra 5).
Repetido da auditoria anterior: não
Avisado à advogada em 2026-04-02. Decisão: nenhuma mensagem nova ao contato; registro conferido (`pediu_para_parar = sim`, próximo passo "nenhum").

## Achados altos

Achado 2 · alta · critério 6 · C-2026-0006 · negociação
Trecho: "Aquele escritório nem tem a experiência que a gente tem, viu?"
Comparação com colega ao responder "o outro cobra metade" (regras, ética, item 3).

Achado 3 · alta · critérios 4 e 5 · C-2026-0006 · negociação
Trecho: "essa condição só vale até sexta, depois sobe." e "Se fechar hoje eu consigo 20% de desconto."
Escassez falsa e desconto como isca, negociado por mensagem fora da política (regras, ética, itens 3 e 4).

Achado 4 · alta · critério 8 · C-2026-0011 · contato novo
Só a mensagem automática respondeu; a conversa termina com o contato há 137,2 h úteis, e o registro tem `primeira_resposta` vazia.

Achado 5 · alta · critérios 5 e 7 · C-2026-0014 · contato novo
Quatro retornos seguidos sem resposta (máximo da ficha: 3), um deles com "Última chance: só restam duas vagas de consulta este mês!".

Achado 6 · alta · critério 9 (registro) · C-2026-0017
`pediu_para_parar = sim` e `proximo_passo` "retorno 2 de 3".

Achado 7 · alta · critério 7 (registro) · C-2026-0004
Contato fora da área, encaminhado com urgência, com "retorno 1 de 3" marcado.

## Achados médios e baixos
- Assinatura diferente da ficha: 3 conversas (baixa).
- "Aguarde nosso retorno" sem prazo: 2 conversas (média).

## Comparação com a auditoria anterior
| Achado | Antes | Agora |
|---|---|---|
| Primeira auditoria comercial | - | - |

## Propostas
| N | Destino | O que muda | Por quê | Decisão |
|---|---|---|---|---|
| 1 | registro | C-2026-0017 e C-2026-0004 com próximo passo "nenhum"; C-2026-0014 com a régua encerrada | achados 5, 6 e 7 | sim |
| 2 | aprendizados | "Depois da confirmação de parar, nenhuma mensagem, nem lembrete de horário" (em uso) | achado 1 | sim |
| 3 | ficha do escritório | `frases_que_nunca_usamos` ganha "só até sexta", "últimas vagas", "se fechar hoje", "última chance" | achados 3 e 5 | sim |
| 4 | biblioteca | Resposta a "achei caro" sem citar colega e sem condição por prazo, pela objecoes-comerciais | achados 2 e 3 | sim |
| 5 | rotina | O resumo do dia passa a listar todo contato com `primeira_resposta` vazia, pela rotina-comercial | achado 4 | sim |
| 6 | ficha comercial | `maximo_de_retornos` confirmado em 3, contando o encerramento | achado 5 | depois |

## Revisão dos aprendizados
[tabela da revisão do mês]

## Registro de contatos
C-2026-0017, C-2026-0004 e C-2026-0014 atualizados conforme a proposta 1, com o ok.

## Próxima auditoria
- Data: 2026-05-04
- Conferir de novo: pedido de parar, régua acima do máximo, comparação com colegas, contato sem resposta.
```
