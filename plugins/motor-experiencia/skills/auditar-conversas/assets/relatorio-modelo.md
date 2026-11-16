# Modelo do relatório da auditoria

Gravado em `escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD.md`, com a data do dia da auditoria. Primeiro o modelo, depois o exemplo preenchido com o Escritório Modelo.

## O modelo

```markdown
---
documento: Auditoria das conversas com clientes AAAA-MM-DD
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Auditoria das conversas com clientes · AAAA-MM-DD

- Período das conversas: [DE] a [ATÉ]
- Amostra: [N] conversas ([N] com reclamação ou insatisfeito; [N] além do máximo sem notícia; [N] com decisão no período; [N] com compromisso no período; [N] sorteadas do resto). Escolhida pela carteira.
- Régua: ficha do escritório versão [N], ficha da experiência versão [N], aprendizados versão [N], biblioteca versão [N], jornadas [ARQUIVOS]
- Tempos: script tempos.py | medidos à mão
- Quem leu: a habilidade; quem conferiu os achados críticos: [FUNÇÃO DO ADVOGADO]

## Resumo
[Cinco linhas, no máximo: quantos achados por gravidade, o padrão principal, a proposta mais importante.]

## Tempos e intervalos sem notícia
[Resumo do script: esperas respondidas fora do prazo, esperas sem retorno que passaram do prazo, cobranças repetidas, conversas sem retorno, conversas acima do máximo sem notícia, conferidas com a carteira.]

## Achados críticos
[Um registro por achado, no formato de references/criterios-da-auditoria.md. Diga quando o advogado foi avisado e o que decidiu.]

## Achados altos

## Achados médios e baixos
[Só os padrões, agrupados: "termo sem explicação: 3 conversas".]

## Comparação com a auditoria anterior
| Achado | Antes | Agora |
|---|---|---|

## Propostas
| N | Destino | O que muda | Por quê | Decisão |
|---|---|---|---|---|

## Revisão dos aprendizados
[A tabela de mudanças de references/revisao-dos-aprendizados.md, com a decisão.]

## Carteira
[Linhas da carteira.csv que a auditoria propõe atualizar, com a decisão.]

## Próxima auditoria
- Data: [AAAA-MM-DD]
- Conferir de novo: [achados altos e críticos desta]
```

## Exemplo preenchido · Escritório Modelo (fictício)

Sete conversas de clientes da carteira fictícia, exportadas em 2026-04-10 às 18h40. Régua: primeira resposta em até 4 horas úteis, máximo de 30 dias sem notícia, dias úteis das 9h às 18h.

```markdown
---
documento: Auditoria das conversas com clientes 2026-04-10
versao: 1
revisado_em: 2026-04-10
dono: secretaria
---

# Auditoria das conversas com clientes · 2026-04-10

- Período das conversas: 2026-02-20 a 2026-04-10
- Amostra: 7 conversas (1 insatisfeito; 2 além do máximo sem notícia; 1 com decisão no período; 2 com compromisso; 1 sorteada). Escolhida pela carteira.
- Régua: ficha do escritório 0.3, ficha da experiência 0.2, aprendizados 2, biblioteca 0.2
- Tempos: script tempos.py, 09:00-18:00, seg-sex, prazo de 4 horas úteis, máximo de 30 dias
- Quem leu: a habilidade; quem conferiu os achados críticos: advogada titular

## Resumo
5 achados críticos, 3 altos e 1 padrão médio. O padrão principal é a resposta rápida com conteúdo errado: as esperas respondidas ficaram todas no prazo, mas três respostas confirmaram, prometeram ou anunciaram o que não podiam. O segundo padrão é a notícia que não vem: duas conversas acima de 30 dias sem mensagem do escritório. A proposta mais importante: a biblioteca ganha as respostas-padrão para "pergunta com resposta de IA", "pedido de senha" e "intercorrência de saúde", e a jornada da fase de cumprimento ganha contato quinzenal.

## Tempos e intervalos sem notícia
| Medida | Valor |
|---|---|
| Esperas respondidas fora do prazo | 0 de 7 |
| Esperas sem retorno que já passaram do prazo | 2 (C-2025-0088, C-2026-0001) |
| Cobranças repetidas sem resposta | 2 (C-2025-0088) |
| Conversas acima do máximo sem notícia | 2: C-2025-0088 (49 dias), C-2026-0001 (36 dias); a carteira confirma, sem ligação registrada |

## Achados críticos

Achado 1 · crítica · critério 3
Conversa: C-2026-0010 · fase decisao · whatsapp
Trecho: "Saiu a sentença, infelizmente foi improcedente. A Dra. vai te explicar."
Por que importa: notícia ruim por mensagem (nunca_por_mensagem; regras, linha vermelha, item 2). "Improcedente" sem explicação.
Repetido da auditoria anterior: não
Avisado à advogada em 2026-04-10. Decisão: ela liga hoje; a mensagem fica registrada no histórico.

Achado 2 · crítica · critério 6
Conversa: C-2026-0007 · fase protocolado · whatsapp
Trecho: "Isso mesmo, concluso para despacho quer dizer que o juiz vai decidir essa semana."
Por que importa: confirma a previsão de uma IA e promete data de decisão (regras, ética, itens 1 e 6).
Repetido da auditoria anterior: não

Achado 3 · crítica · critério 7 (linha vermelha)
Conversa: C-2026-0007 · fase protocolado · whatsapp
Trecho: "Que pena! Ela está com o quê? Manda o laudo aqui que a gente junta."
Por que importa: internação (vulnerabilidade) respondida com mensagem comum, sem passagem para a advogada; pede dado de saúde por mensagem.
Repetido da auditoria anterior: não

Achado 4 · crítica · critério 4
Conversa: C-2026-0002 · fase audiencia-pericia · whatsapp
Trecho: "Seu caso é ganho, fica tranquilo."
Por que importa: promessa de resultado; "fica tranquilo" está em frases_que_nunca_usamos.
Repetido da auditoria anterior: não

Achado 5 · crítica · critério 8
Conversa: C-2026-0002 · fase audiencia-pericia · whatsapp
Trecho: "Te mando a senha amanhã cedo."
Por que importa: senha nunca é enviada nem pedida (regras, dados de cliente, item 4). O número do processo pode ir ao cliente; a senha, nunca.
Repetido da auditoria anterior: não

## Achados altos

Achado 6 · alta · critérios 1 e 2 · C-2025-0088 · fase cumprimento
"Vou ver com a Dra. e te retorno" (2026-02-20) sem retorno; duas cobranças sem resposta; 49 dias sem notícia. Virou reclamação em 2026-04-10 (reclamacao-e-recuperacao).

Achado 7 · alta · critério 2 · C-2026-0001 · fase aguardando
36 dias sem notícia, com perícia em 4 dias; última mensagem do escritório prometia "mais perto da data eu te mando o que levar".

Achado 8 · alta · critério 1 · C-2026-0002 · fase audiencia-pericia
"Amanhã te mando o que levar" (2026-04-08) não aconteceu; o cliente cobrou na sexta, 2026-04-10, o último dia útil antes da audiência de segunda, 2026-04-13.

## Achados médios e baixos
- Termo sem explicação ("improcedente", "concluso para despacho"): 2 conversas.

## Comparação com a auditoria anterior
| Achado | Antes | Agora |
|---|---|---|
| Primeira auditoria de clientes ativos | | linha de base |

## Propostas
| N | Destino | O que muda | Por quê | Decisão |
|---|---|---|---|---|
| 1 | biblioteca | Mensagem `cliente-com-ia`: acolhe, explica o termo, diz que a data não é previsível e que a advogada confere | achado 2 | sim |
| 2 | biblioteca | Resposta-padrão a pedido de senha: "nunca pedimos nem mandamos senha; posso te mandar a página do caso ou o resumo" | achado 5 | sim |
| 3 | ficha | `sempre_vai_para_pessoa` ganha "internação, luto ou doença grave na família" | achado 3 | sim |
| 4 | jornada | Fase `cumprimento` da aposentadoria com notícia a cada 15 dias até o pagamento | achado 6 | sim |
| 5 | aprendizados | "Promessa de mandar algo 'amanhã' vira proximo_contato na carteira no mesmo dia" | achados 7 e 8 | sim |
| 6 | ficha | `frases_que_nunca_usamos` ganha "seu caso é ganho" | achado 4 | sim |

## Revisão dos aprendizados
[tabela da revisão do mês]

## Carteira
C-2026-0001: proximo_contato 2026-04-10, motivo compromisso (preparação da perícia), com o ok. C-2025-0088: reclamacao_aberta = sim, pela reclamacao-e-recuperacao.

## Próxima auditoria
- Data: 2026-05-08
- Conferir de novo: notícia ruim por mensagem, confirmação de IA, senha, "te retorno" descumprido.
```
