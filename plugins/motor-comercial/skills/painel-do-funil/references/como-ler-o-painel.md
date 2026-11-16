# Como ler o painel

O painel tem duas metades. A primeira é do script: números, sem opinião, e só códigos de contato. A segunda é da conversa com o advogado: três leituras, três ações e as perguntas que ficaram. Esta página diz o que cada seção quer dizer, onde ela engana e quais perguntas fazer quando o número não explica.

## 1. O que cada seção responde

| Seção | Responde | Olhe primeiro |
|---|---|---|
| Cuidados antes de ler | O quanto dá para confiar no resto | Mês em curso, amostra pequena, contatos em andamento |
| 1. Entradas | De onde vêm os contatos e quais chegam longe | A coluna "Fecharam" ao lado de "Entraram" |
| 2. Funil | Em que passagem os contatos param | A passagem com a menor taxa e o "Anterior" ao lado |
| 3. Primeira resposta | Se o escritório responde no prazo da ficha, e quem ainda não recebeu resposta | A lista "Sem resposta de uma pessoa" e quem ficou fora do prazo |
| 4. Propostas | Quanto foi proposto, fechado e está em aberto | O valor em aberto: é o que ainda pode virar contrato |
| 5. Motivos de perda | Por que os perdidos se perderam, no que foi registrado | "(sem motivo)" e "sem-resposta" |
| 6. Pediram para parar | Quem não recebe mais nada | Se o número cresceu de repente |
| 7. Qualidade do registro | O que precisa ser corrigido para o próximo painel | Código repetido e origem vazia |

## 2. Cuidados que mudam a leitura

| Cuidado | O que muda | O que fazer |
|---|---|---|
| **Amostra pequena** (menos de 20 contatos no mês) | Uma diferença de dois contatos parece tendência | Leia em "x de y", não em percentual. Rode o trimestre junto. Não proponha mudança grande com base num mês só |
| **Mês curto ou em curso** | Menos dias, menos contatos, comparação torta | Espere o mês fechar, ou compare só com os mesmos dias do mês anterior, à mão |
| **Mês com feriado ou recesso** | Horas úteis contam o feriado como dia de atendimento | Diga no painel quais dias foram feriado e desconte à mão na leitura do tempo |
| **Contatos em andamento** | As passagens finais (proposta, fechado) ainda vão subir | Releia o painel do mês passado no mês seguinte, quando a coorte fechar |
| **Perdidos sem etapa** | Conversão do meio parece pior do que foi | Preencha `perdido_na_etapa` sempre que mover para perdido |
| **Primeiro mês do registro** | A coluna "Anterior" fica zerada | Leia só o mês; compare a partir do segundo |
| **Contatos antigos** | Quem já falava com o escritório antes do registro conta como entrada | Leia as entradas descontando os antigos |
| **Tempo medido em parte dos contatos** | A mediana fala só de quem tem a hora registrada | Diga "em 28 de 31" junto do número, e separe quem está sem resposta de quem só não teve a hora anotada |
| **Registro com problema** | Origem duplicada, contato contado duas vezes | Corrija e rode de novo antes de levar à reunião |
| **Mudança de forma de registrar** | Um mês com origem detalhada e outro sem parece mudança de público | Anote no painel quando o jeito de registrar mudou |

Regra prática: se o cuidado mexe na leitura, a leitura leva o cuidado na mesma frase. "Indicação fechou 3 de 6 (amostra pequena, primeiro mês do registro)".

## 3. Banco de perguntas

Quando o número aponta e não explica, a leitura termina numa destas perguntas (ou numa parecida). Cada uma tem para quem vai e onde procurar a resposta.

| O painel mostra | Pergunta | Para quem | Onde está a resposta |
|---|---|---|---|
| Origem com muitas entradas e poucos fechamentos | "O que os contatos dessa origem pediam na primeira mensagem? Eram de área atendida?" | Quem faz a triagem | Lotes de `triagens/` do mês |
| Muitos encaminhados ou recusados | "O que estamos recebendo que não atendemos? Vale ajustar o que dizemos nas redes ou no site?" | Advogado | Coluna `area` e `assunto` dos encaminhados |
| Contato sem resposta de uma pessoa | "O rascunho dele foi para a fila? Foi aprovado e não enviado? Quem anota a `primeira_resposta`?" | Quem aprova a fila | `fila/` do dia e o resumo da `rotina-comercial` |
| Com uma pessoa, sem retorno registrado | "A ligação aconteceu? Alguém contou o combinado ao comando `fila`?" | Quem estava em PESSOA AGORA | Resumos de `rotina/` e o arquivo da triagem |
| Triado e não agendou | "Esses contatos receberam o convite para a consulta? Com como agendar?" | Quem responde | Conversas (`auditar-conversas-comerciais`, se instalada) |
| Agendou e não compareceu | "O lembrete da véspera saiu? A consulta era paga e o contato sabia?" | Quem agenda | Agenda e biblioteca comercial |
| Consulta feita e sem proposta | "A proposta ficou para depois ou o caso não tinha ação?" | Advogado | Atas em `07-operacao/comercial/consultas/` |
| Proposta e não fechou | "As perdidas por preço viram a política de honorários? O retorno saiu nos prazos da ficha?" | Advogado | `07-operacao/comercial/propostas/` e a régua de retorno |
| Muitos "sem-resposta" | "O follow-up rodou? A última mensagem foi nossa ou do contato?" | Quem faz o follow-up | Registro e conversas |
| Tempo de resposta alto num canal | "Quem olha esse canal e em que horário?" | Equipe | Ficha (`quem_atende`, `canais`) |
| Tempo alto à noite | "A mensagem de fora do horário saiu? Ela diz quando alguém responde?" | Dono da biblioteca | Biblioteca comercial, modelo `fora-do-horario` |
| Pediram para parar em alta | "O que eles receberam antes de pedir? Foi a mesma mensagem?" | Advogado | Conversas e régua de follow-up |
| "(sem motivo)" alto | "Quem move para perdido sabe que precisa do motivo?" | Equipe | Aprendizado novo, se for o caso |

Pergunta que o painel nunca faz ao cliente: o painel é interno. Ninguém manda pesquisa a quem pediu para parar, e ninguém procura quem não procurou o escritório.

## 4. Leituras que parecem boas e não são (números de exemplo)

| Leitura | Problema | Versão honesta |
|---|---|---|
| "O Google não funciona" | Causa e conclusão a partir de 10 contatos no primeiro mês | "Em março, 1 de 10 do Google fechou; vários seguem em andamento" |
| "A conversão caiu 20%" | Mês em curso contra mês fechado | "Até o dia 15, 2 de 11 fecharam; no mês passado inteiro, 4 de 20" |
| "A gente responde em 24 minutos" | Mediana esconde quem esperou e quem nunca recebeu resposta | "Mediana de 24 minutos; 6 de 28 fora do prazo; 3 contatos sem resposta, um há 119 horas úteis" |
| "Perdemos por preço" | Só 1 perdido tem motivo preço, e 1 está sem motivo | "1 de 6 perdidos foi por preço; 2 por sem-resposta; 1 sem motivo registrado" |
| "Fechamos 2.950 por contrato" | Média de 4 fechadas com valor; duas fechadas estão sem valor | "Média de 2.950 nas 4 fechadas com valor registrado; duas sem valor, talvez só de êxito" |

## 5. O painel completo do exemplo

Escritório Modelo, registro fictício de 31 linhas (os onze primeiros contatos são os casos de `../../../docs/casos-ficticios.md`), primeiro mês do registro. Em treino, o registro fica em `escritorio/07-operacao/_treino/comercial/contatos.csv` e o comando leva `--treino`; aqui ele foi rodado como se fosse o registro real, para mostrar a saída sem a marca TREINO:

```
python3 "<PASTA DA HABILIDADE>/scripts/painel.py" escritorio/07-operacao/comercial/contatos.csv 2026-03 \
  --prazo-horas 2 --origens "indicacao,instagram,google,cliente-antigo,outro" \
  --areas "previdenciario,trabalhista,familia" --hoje 2026-03-31
```

Saída do script, sem edição (valores de exemplo):

````markdown
# Painel do funil · 03/2026

Números calculados pelo script a partir de `contatos.csv` (31 linhas no registro). Contatos que entraram no período: **31**. Coluna "Anterior": 02/2026, com 0 contatos. As leituras e as ações vêm depois, escritas com o advogado. Uso interno: o painel não vai para cliente.

## Cuidados antes de ler

- O período anterior (02/2026) não tem nenhum contato no registro: primeiro mês do registro, ou os contatos antigos estão em outro lugar. A coluna Anterior não serve para comparar.
- Contatos do período com tipo antigo (já falavam com o escritório antes do registro): 3. Entram no funil, mas não são entrada nova de verdade.
- 16 contatos do período ainda estão em andamento. A conversão das etapas finais ainda vai mudar; o período fecha de verdade quando eles chegarem a um fim.
- 1 perdido sem perdido_na_etapa e sem valor de proposta: conta como perdido logo depois da triagem. Se foi perdido mais adiante, a conversão real das etapas do meio é maior.
- Códigos repetidos no registro (C-2026-0029): o painel conta cada linha. Corrija o registro e rode de novo.
- Tempo de resposta medido em 28 de 31 contatos. Os outros estão sem primeira_resposta: ou ainda não foram respondidos (seção 3) ou a hora não foi registrada (seção 7).
- Horas úteis contadas no horário 09:00-18:00, sem descontar feriados.

## 1. Entradas

### Por origem

| Origem | Entraram | Anterior | Variação | Propostas | Fecharam | Valor fechado |
|---|---|---|---|---|---|---|
| google | 10 | 0 | +10 | 4 | 1 | 3.500 |
| instagram | 9 | 0 | +9 | 3 | 2 | 5.500 |
| indicacao | 6 | 0 | +6 | 4 | 3 | 2.800 |
| cliente-antigo | 2 | 0 | +2 | 2 | 0 | 0 |
| outro | 2 | 0 | +2 | 0 | 0 | 0 |
| (sem origem) | 1 | 0 | +1 | 0 | 0 | 0 |
| tiktok | 1 | 0 | +1 | 0 | 0 | 0 |

### Por área

| Área | Entraram | Anterior | Variação | Propostas | Fecharam | Valor fechado |
|---|---|---|---|---|---|---|
| familia | 10 | 0 | +10 | 4 | 3 | 5.300 |
| previdenciario | 9 | 0 | +9 | 5 | 2 | 3.500 |
| trabalhista | 9 | 0 | +9 | 4 | 1 | 3.000 |
| a-confirmar | 1 | 0 | +1 | 0 | 0 | 0 |
| fora-da-area | 1 | 0 | +1 | 0 | 0 | 0 |
| tributario | 1 | 0 | +1 | 0 | 0 | 0 |

### Por canal

| Canal | Entraram | Anterior | Variação | Propostas | Fecharam | Valor fechado |
|---|---|---|---|---|---|---|
| whatsapp | 23 | 0 | +23 | 9 | 3 | 8.800 |
| email | 2 | 0 | +2 | 0 | 0 | 0 |
| instagram | 2 | 0 | +2 | 1 | 1 | 3.000 |
| site | 2 | 0 | +2 | 1 | 0 | 0 |
| telefone | 2 | 0 | +2 | 2 | 2 | 0 |

## 2. Funil dos contatos do período

| Passagem | Chegaram | De | Taxa | Anterior |
|---|---|---|---|---|
| Entraram > triados | 30 | 31 | 97% | 0 de 0 |
| Triados atendíveis > consulta agendada | 19 | 28 | 68% | 0 de 0 |
| Consulta agendada > consulta feita | 16 | 19 | 84% | 0 de 0 |
| Consulta feita com caso > proposta enviada | 13 | 15 | 87% | 0 de 0 |
| Proposta enviada > fechado | 6 | 13 | 46% | 0 de 0 |
| Entraram > fechado | 6 | 31 | 19% | 0 de 0 |

Onde estão hoje:

| Etapa | Contatos |
|---|---|
| novo | 1 |
| triado | 4 |
| consulta-agendada | 2 |
| nao-compareceu | 1 |
| consulta-feita | 2 |
| proposta-enviada | 4 |
| negociando | 2 |
| fechado | 6 |
| encaminhado | 1 |
| recusado | 1 |
| sem-caso | 1 |
| perdido | 6 |

Encaminhados: 1. Recusados: 1. Não compareceram: 1. Sem caso: 1. Ainda em andamento: 16.

## 3. Primeira resposta de uma pessoa

| Medida | Valor |
|---|---|
| Contatos com a hora registrada | 28 de 31 |
| Mediana em horas úteis | 24 min |
| Maior espera em horas úteis | 5,5 h |
| Mediana em horas corridas | 29 min |
| Dentro do prazo da ficha (2,0 h úteis) | 22 de 28 (79%) |

| Canal | Medidos | Mediana em horas úteis |
|---|---|---|
| whatsapp | 20 | 20 min |
| email | 2 | 2,9 h |
| instagram | 2 | 3,1 h |
| site | 2 | 3,6 h |
| telefone | 2 | 14 min |

Fora do prazo: C-2026-0010 (3,7 h), C-2026-0013 (2,2 h), C-2026-0015 (5,5 h), C-2026-0017 (2,5 h), C-2026-0022 (2,8 h), C-2026-0024 (5,0 h).

**Sem resposta de uma pessoa até a data de referência** (novo ou triado com `primeira_resposta` vazia): C-2026-0011 (119,2 h úteis), C-2026-0027 (27,0 h úteis), C-2026-0030 (9,5 h úteis).

## 4. Propostas e fechamentos

| Item | Quantidade | Valor somado |
|---|---|---|
| Propostas com valor registrado (contatos do período) | 11 | 41.400 |
| Fechadas | 4 | 11.800 |
| Em aberto (enviada ou negociando) | 6 | 25.600 |
| Perdidas com proposta | 1 | 4.000 |

Fechados no funil: 6. Com valor de proposta registrado: 4. A diferença está na seção 7 (ou é proposta só de êxito, que fica sem valor).

Chegaram à proposta no funil: 13. Com valor registrado: 11.

Valor médio das fechadas: 2.950 (4 propostas).

Movimento do período, de qualquer mês de entrada, pela data da última atualização (aproximado): 6 fechados e 6 perdidos.

## 5. Motivos de perda

| Motivo | Contatos |
|---|---|
| sem-resposta | 2 |
| (sem motivo) | 1 |
| desistiu | 1 |
| outro | 1 |
| preco | 1 |

## 6. Pediram para parar

2 contatos do período: C-2026-0009, C-2026-0017. No registro inteiro: 2. Nenhum deles recebe retorno.

## 7. Qualidade do registro

| Problema | Linhas | Códigos |
|---|---|---|
| proposta sem valor registrado (ou proposta só de êxito: confirmar) | 2 | C-2026-0007, C-2026-0019 |
| área fora das áreas da ficha (use fora-da-area) | 1 | C-2026-0022 |
| contato sem origem | 1 | C-2026-0023 |
| origem fora das opções da ficha | 1 | C-2026-0024 |
| perdido sem motivo | 1 | C-2026-0024 |
| código repetido (uma linha por contato) | 1 | C-2026-0029 |
| perdido sem perdido_na_etapa | 1 | C-2026-0029 |
````

Depois desta saída vêm as três leituras e as três ações, escritas com o advogado. As do exemplo estão no SKILL.md, seção 5.
