---
name: objecoes-comerciais
description: >
  Monta a biblioteca de respostas éticas às objeções que aparecem depois da consulta ou da
  proposta (está caro, vou pensar, outro advogado cobra menos, posso pagar só no fim, preciso
  falar com minha família, demora muito, já tive advogado e não deu certo, por que a consulta é
  paga, dá para garantir que eu ganho) e responde a uma objeção concreta no tom do escritório.
  Quando o pedido é baixar o valor, prepara as opções dentro da política para o advogado
  decidir. Sem desconto como isca, sem escassez, sem falar de colegas, sem promessa. No ciclo,
  grava a resposta na fila. Use quando o advogado disser "ela achou caro, o que eu respondo", "o
  cliente disse que vai pensar", "ele quer pagar só no final", "monta nossas respostas para
  objeções", "posso dar desconto?". Não use para refazer a proposta (use
  proposta-de-honorarios) nem para retomar quem parou de responder (use follow-up).
---

# Objeções comerciais

> Quem diz "está caro" quase sempre está dizendo outra coisa: não entendeu o que está incluído, não tem a entrada, tem medo de pagar e não dar em nada. A resposta boa começa por descobrir qual delas é, e nunca compra o fechamento com desconto, pressa ou promessa.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-comercial.md`. Funil: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Fila: `../../docs/agentes-e-fila.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

Quarta, 10h. Chega no WhatsApp: "Achei caro o valor que vocês passaram. O outro escritório cobra metade." A primeira vontade é dizer que o outro escritório não presta, ou baixar o preço na hora. Uma resposta fere a ética. A outra ensina que o valor do escritório se negocia por mensagem.

**Regras fixas desta habilidade:**
1. Antes de argumentar, entender. Uma pergunta de esclarecimento vem antes de qualquer explicação de valor.
2. Sem desconto como isca, sem escassez ou urgência falsa, sem falar de colegas, sem promessa de resultado ou de chance.
3. Mexer no valor é decisão do advogado (H). A habilidade prepara as opções dentro da política, e nada vai ao cliente sem o ok.
4. O "não" e o "vou pensar" são respeitados. O retorno segue a régua da ficha, e quem pediu para parar não recebe mais nada.
5. Toda resposta sai como rascunho (A): uma pessoa lê e envia. Aflição, vulnerabilidade ou reclamação forte vão para uma pessoa, sem rascunho.

## 1. Quando usar

**Use quando:**
- O cliente respondeu à proposta com uma dúvida, uma resistência ou um pedido de valor menor.
- A objeção aparece antes da proposta ("por que a consulta é paga?").
- O escritório quer montar, de uma vez, as respostas às objeções que mais ouve.
- O advogado escreveu uma resposta e quer conferir se ela passa nas regras.
- O `agente-comercial` achou uma objeção nas mensagens do dia (modo no ciclo), ou a `adaptar-comercial` (se instalada) pediu a biblioteca no jeito do nicho (modo adaptar).

**Não use quando:**
- O advogado já decidiu mudar o valor ou o escopo: use `proposta-de-honorarios` (nova versão).
- A pessoa sumiu depois da proposta: use `follow-up` (se instalada).
- A objeção é sobre um caso em andamento ("por que demora tanto o meu processo?"): é cliente; use a `triar-mensagem-do-cliente` do motor-experiencia (se instalado), ou entregue à pessoa que cuida do caso.
- A mensagem traz aflição ou vulnerabilidade ("perdi o emprego e não sei como vou pagar nada"): vai para uma pessoa; a habilidade só prepara as opções da política, se o advogado pedir.

## 2. Antes de começar

1. **Leia as fichas:** `escritorio/04-base/comum/ficha-do-escritorio.md` (tom, tratamento, `frases_que_nunca_usamos`) e `escritorio/04-base/comum/ficha-comercial.md` (seções 2 e 3, e `diferenciais_verdadeiros`).
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`), se existir: o que o cliente costuma temer e como ele fala muda a pergunta de esclarecimento.
3. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado de objeção vale antes da base desta habilidade.
4. **Leia a biblioteca do escritório** (`escritorio/04-base/comercial/objecoes.md`), se existir. Não existe: use `references/biblioteca-de-objecoes.md` e ofereça montar a do escritório (modo A).
5. **Leia a política** (`escritorio/04-base/comercial/politica-de-honorarios.md`), se existir: parcelas, quem aprova e o que o escritório não faz.
6. **Leia a proposta** do contato em `escritorio/07-operacao/comercial/propostas/` e a linha dele no `contatos.csv`. Proposta anterior ao registro (contato `antigo`): pergunte o que foi oferecido e marque `[A CONFIRMAR]` no registro até alguém confirmar.
7. **Conta de IA.** Em conta pessoal, só caso fictício, gravado em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** C: `modelo`, `entrada_e_parcelas`, `diferenciais_verdadeiros`.
- **Melhora:** C: `motivos_de_perda_comuns`, `consulta`.

O tom, o tratamento, as frases proibidas e a assinatura saem da ficha do escritório, como em toda habilidade. Sem `diferenciais_verdadeiros`, a resposta não cita diferencial nenhum: pergunte "O que vocês fazem de fato que o cliente percebe? Só o que é verdade hoje." e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Montar a biblioteca | Primeira vez, ou para revisar | Entrevista curta | `04-base/comercial/objecoes.md` |
| B. Responder agora, a pedido | Chegou uma objeção | A mensagem do cliente | Rascunho no chat e linha do funil |
| C. Preparar renegociação | O cliente pede valor menor ou outra forma | A proposta e a política | Tabela de opções para o advogado decidir |
| D. Revisar resposta | O advogado escreveu e quer conferir | O texto dele | O texto com os ajustes e o porquê |
| E. No ciclo | O `agente-comercial` chama | As mensagens do dia de quem está em proposta | Rascunho na fila; valor vai para "PARA DECIDIR" |
| F. Adaptar | A `adaptar-comercial` chama | O nicho e a biblioteca atual | Biblioteca reescrita, com `[ALTERADO]`, gravada só com o ok |

### A. Montar a biblioteca

Pergunte, uma de cada vez:
1. "Quais objeções vocês mais ouvem depois da proposta? Me conte a última que travou um fechamento."
2. "O que vocês fazem de fato que o cliente percebe? Só o que é verdade hoje." (grava em `diferenciais_verdadeiros`)
3. "Quando o cliente acha caro, o que dá para mudar sem mexer no valor: número de parcelas, dia de vencimento, escopo?" (confira com a política)
4. "Quem decide quando o pedido é baixar o valor?"
5. "Tem alguma frase que vocês nunca querem ver numa resposta dessas?"

Monte `objecoes.md` com as nove objeções de `references/biblioteca-de-objecoes.md`, reescritas no tom da ficha e com os diferenciais verdadeiros, mais as que o escritório citou e as de `motivos_de_perda_comuns`. Mostre uma por uma, ajuste e grave com o ok.

### B. Responder agora (a pedido)

**Passo 1. Receber.** Anonimize dado identificável. Ache o contato e a proposta. Duas objeções juntas ("caro e preciso falar com meu marido"): trate as duas, a mais sensível primeiro.

**Passo 2. Parar se for o caso.** Aflição, vulnerabilidade, ameaça ou reclamação forte: sem rascunho pronto, vai para o advogado agora (`../../docs/regras.md`, seção 5), com o `proximo_passo` começando por `pessoa agora:` (ou `pessoa liga:`, em vulnerabilidade), pelo marcador de pessoa (`../../docs/funil.md`, regra 4). Contato que já está com esse marcador ou com `pediu_para_parar = sim`: nenhum rascunho.

**Passo 3. Ler o que há por trás.** Use a coluna "o que pode estar por trás" da biblioteca. Se não der para saber, a resposta é a pergunta de esclarecimento, e mais nada.

**Passo 4. Rascunhar.** A partir da biblioteca do escritório (ou da base), no tom da ficha: curto, uma ideia por parágrafo, sem defesa. Termine com uma pergunta aberta ou uma oferta de conversa.

**Passo 5. Se a objeção é de valor.** Rode o modo C e entregue as opções ao advogado. O rascunho ao cliente fica neutro ("vou ver com a advogada o que é possível e te retorno até {PRAZO}") até ele decidir. O prazo fica entre chaves porque é quem envia que escolhe, na hora, um prazo que o escritório cumpre.

**Passo 6. Checagem.** Rode a lista da seção 5. Nenhum campo entre colchetes pode sobrar no rascunho: os colchetes da biblioteca a habilidade preenche com a ficha, a proposta e a política, e o que faltar vai para o cabeçalho interno. Só o que quem envia escolhe na hora fica entre chaves (`{PRAZO}`).

**Passo 7. Mostrar e registrar.** Mostre o rascunho e a linha do `contatos.csv`: etapa `negociando`, `proximo_passo` ("enviar resposta à objeção" ou "advogado decidir renegociação"), data e responsável. A régua de retorno fica pausada enquanto a conversa anda. Grave com o ok.

**Passo 8. Aprender.** Pergunte: "Você mudaria alguma coisa nesta resposta para as próximas?". Correção vira regra curta nos aprendizados, com o ok. Resposta aprovada que funcionou: ofereça guardar em `objecoes.md` como a versão do escritório.

### C. Preparar renegociação (para o advogado)

1. Leia a proposta enviada e a política.
2. Liste só as opções que a política permite, nesta ordem: mudar a forma (mais parcelas dentro do máximo, outro vencimento), mudar o modelo (misto no lugar de fixo, se a política prevê), reduzir o escopo com o valor que a política dá para o escopo menor.
3. Para cada opção: como fica a conta, o que muda para o cliente, se precisa de aprovação.
4. Opção fora da política aparece separada, como "fora da política: só com [quem aprova]", sem recomendação.
5. Nunca entra: desconto para fechar hoje, valor menor sem mudar nada, valor abaixo da referência da tabela da seccional sem o advogado decidir (a comparação com a tabela fica para o "Antes de enviar" da nova versão da proposta, como `[CONFERIR]`).

| Opção | Como fica | O que muda para o cliente | Dentro da política? |
|---|---|---|---|
| Mais parcelas | [conta] | Parcela menor, mesmo total | sim, até [máximo] |
| Escopo menor | [conta da política] | Menos trabalho incluído; o resto vira proposta à parte | sim ou não |
| Outro modelo | [conta] | Parte paga no êxito | sim ou não |

Decidiu: a mudança vira nova versão pela `proposta-de-honorarios` (se instalada). Sem ela, copie a proposta, mude só o que foi decidido e anote no topo o que mudou.

### E. No ciclo (o agente chama)

1. O agente passa as mensagens do dia de contatos em `proposta-enviada` ou `negociando`.
2. Sinal de aflição, vulnerabilidade, ameaça ou reclamação forte: "PESSOA AGORA" no resumo, sem rascunho, e o `proximo_passo` passa a começar por `pessoa agora:` (ou `pessoa liga:`, em vulnerabilidade). Contato que já tem esse marcador ou `pediu_para_parar = sim`: nada de rascunho.
3. Objeção sem valor (vou pensar, família, demora, consulta paga, garantia): rascunho da pergunta de esclarecimento ou da resposta-base em `07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-resposta-a-objecao.md`, no formato de `agentes-e-fila.md`, com `tipo: resposta-a-objecao`, `revisor: pendente` e `motivo` com a objeção em poucas palavras. Passa pelo `revisor-comercial`.
4. Objeção de valor: só o rascunho neutro ("vou ver o que é possível e te retorno até {PRAZO}") vai para a fila, com o prazo entre chaves para quem envia. A tabela do modo C vai para "PARA DECIDIR" no resumo do dia, para o advogado.
5. Registro: o agente põe só `proximo_passo` ("enviar resposta à objeção" ou "advogado decidir renegociação"), a data e `atualizado_em`, as colunas que `funil.md` permite ao agente (regra 11). A etapa `negociando` muda quando uma pessoa confirma o envio.
6. **Saída de PESSOA AGORA.** Depois que o advogado falou com o contato, o comando `fila` pergunta "Já falou? O que ficou combinado?" e troca o `proximo_passo` que começa com `pessoa agora:` ou `pessoa liga:` pelo combinado, com data (`agentes-e-fila.md`). Sem isso, o item volta ao topo do resumo seguinte.

### F. Adaptar (a adaptar-comercial chama)

1. Leia `nicho.md` (como o cliente fala, as perguntas que ele faz, os momentos de aflição, o que ele pesquisa sozinho) e a biblioteca atual.
2. Reescreva cada objeção nas palavras do cliente do nicho, marcando cada mudança `[ALTERADO]`: a pergunta de esclarecimento, a resposta-base e o "o que pode estar por trás".
3. Acrescente, como sugestão, as objeções típicas do nicho que a base não tem (por exemplo, "meu sindicato faz de graça", "o INSS vai me chamar de novo mesmo"), no mesmo formato.
4. Mostre o antes e o depois. Grave em `escritorio/04-base/comercial/objecoes.md` só com o ok.

### Último passo, em todos os modos: Aprender

Toda correção do advogado vira proposta de aprendizado, com a pergunta "Quer que eu guarde isto para as próximas vezes?" e a regra em uma linha (`../../docs/aprender-com-o-uso.md`). No ciclo, a correção feita na fila (item `descartado` ou `ajustado` com motivo) vira a mesma proposta no resumo do dia. Nada entra nos aprendizados sem o ok.

## 4. As objeções em uma tabela

A versão completa (o que pode estar por trás, pergunta de esclarecimento, resposta-base, o que nunca dizer, quando vai para o advogado) está em `references/biblioteca-de-objecoes.md`. Leia no modo A, no modo F e quando a objeção não estiver na biblioteca do escritório.

| Objeção | Primeiro movimento | Nunca |
|---|---|---|
| Está caro | Perguntar o que pesou: o total, a entrada ou a parcela | Baixar o valor na hora |
| Vou pensar | Dar espaço e oferecer tirar dúvidas | "Só até amanhã" |
| Outro advogado cobra menos | Explicar o que está incluído na proposta, sem citar o outro | Comentar o outro escritório |
| Posso pagar só no fim? | Explicar o modelo da política e as parcelas | Mudar para êxito sem o advogado |
| Preciso falar com minha família | Respeitar e oferecer um resumo ou uma conversa junto | Pressionar pela decisão individual |
| Demora muito | Explicar as etapas e como o escritório avisa | Prometer prazo |
| Já tive advogado e não deu certo | Ouvir e explicar como o escritório se comunica | Falar do advogado anterior |
| Por que a consulta é paga? | Explicar o que a consulta entrega | Dar orientação por mensagem para provar valor |
| Dá para garantir que eu ganho? | Dizer com honestidade que ninguém garante | Percentual de chance, "seu caso é bom" |

## 5. Checagem antes de mostrar

- [ ] A resposta começa por entender (pergunta) ou responde ao que o cliente disse, sem sermão.
- [ ] Nenhuma promessa de resultado, de prazo de decisão ou de chance.
- [ ] Nenhuma menção a outro escritório ou advogado, nem elogio, nem crítica.
- [ ] Nenhum desconto, nenhuma condição que vence logo, nenhum "só para você".
- [ ] Diferencial citado só se está em `diferenciais_verdadeiros`.
- [ ] Nenhuma orientação jurídica a quem ainda não é cliente.
- [ ] Valor ou condição nova só depois do ok do advogado.
- [ ] Tom da ficha, sem frase de `frases_que_nunca_usamos`, sem campo entre colchetes sobrando.

## 6. Exemplo resolvido (Escritório Modelo)

Caso 6 de `../../docs/casos-ficticios.md`: Sérgio, C-2026-0006, `tipo = antigo`. "Achei caro o valor que vocês passaram. O outro escritório cobra metade." A proposta é anterior ao registro e não está na pasta.

**Antes de responder:** a habilidade pergunta ao advogado "Qual foi a proposta do Sérgio: escopo, valor e forma de pagamento?". Enquanto ninguém confirma, a linha fica com etapa `negociando` e `proximo_passo` "confirmar proposta anterior `[A CONFIRMAR]`".

**Leitura:** duas objeções juntas, preço e comparação. Não dá para saber se pesou o total ou a entrada. Primeiro movimento: pergunta.

**Rascunho (A, a secretária lê e envia):**

```
Oi, Sérgio, obrigada por me dizer.
Para eu entender melhor: o que pesou mais para você, o valor total ou o valor da entrada?
Se quiser, te explico item por item o que está incluído na proposta, para você comparar com calma o que cada uma cobre.
```

**Para a advogada (modo C), se ele responder que o problema é a entrada:** a política do Escritório Modelo permite até 5 parcelas; se a proposta já está em 5, o que resta dentro da política é mudar o dia de vencimento. Entrada abaixo de 30% está fora da política e é decisão da advogada titular.

**O que a habilidade cortou de um rascunho anterior:** "o outro escritório provavelmente não inclui os recursos" (fala do colega) e "se fechar até sexta mantemos o valor" (escassez).

**Registro:** etapa `negociando`, `proximo_passo` "enviar resposta à objeção", responsável secretaria, data de hoje. No ciclo, o mesmo rascunho iria para `fila/2026-03-11/01-C-2026-0006-resposta-a-objecao.md`.

## 7. Formato da saída

```
OBJEÇÃO · [CÓDIGO] · [NOME] · [etapa]
O que pode estar por trás: ...
Rascunho (A, [função] lê e envia):
"..."
Para o advogado (só se for valor): tabela de opções do modo C
Registro: [linha proposta do contatos.csv]
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Biblioteca de objeções do escritório | `escritorio/04-base/comercial/objecoes.md` |
| Rascunho da resposta (modo B) | No chat, pronto para copiar |
| Rascunho da resposta (modo E) | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-resposta-a-objecao.md` |
| Opções de renegociação | No chat (modo C) ou em "PARA DECIDIR" no resumo do dia (`07-operacao/comercial/rotina/AAAA-MM-DD.md`); a decisão vira nova versão em `escritorio/07-operacao/comercial/propostas/` |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `etapa = negociando`, `responsavel`, `proximo_passo`, `data_proximo_passo`, `atualizado_em` |
| Diferenciais confirmados (com o ok) | `escritorio/04-base/comum/ficha-comercial.md`, campo `diferenciais_verdadeiros`, com linha no histórico |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino com casos fictícios | `escritorio/07-operacao/_treino/comercial/` |

O arquivo `objecoes.md` leva no topo nome, versão, data da revisão e dono, e uma seção por objeção, no formato da referência. Sem pasta aberta: entregue a biblioteca em texto pronto para copiar, com o caminho onde ela ficaria.

## 9. Solo e equipe

**Solo:** a resposta à objeção de preço espera o horário fixo do dia em que o advogado lê as mensagens comerciais. Responder no calor da notificação é como o desconto escapa.

**Equipe:** a secretária responde as objeções que não mexem em valor (vou pensar, família, demora, consulta paga) com a biblioteca aprovada. Objeção de valor, garantia de resultado e experiência ruim com outro advogado vão para o advogado, com o rascunho e as opções prontos.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Baixar o valor na primeira objeção | O cliente aprende que o preço se negocia por mensagem | Regra fixa 3 e modo C |
| Falar mal do colega | Infração ética e imagem ruim | Checagem e "nunca" da biblioteca |
| "Fecha hoje que eu seguro o valor" | Escassez falsa e captação | Regra fixa 2 |
| "Seu caso é muito bom" | Promessa de resultado | Resposta honesta da objeção "garantia" |
| Responder sem entender | Argumento certo para a objeção errada | Pergunta de esclarecimento primeiro |
| Responder sobre proposta que ninguém achou | Valor diferente do que foi oferecido | Proposta antiga `[A CONFIRMAR]` antes de responder |
| Diferencial inventado | Promessa que o escritório não cumpre | Só `diferenciais_verdadeiros` |

## 11. Próximo passo

- O advogado decidiu mudar a proposta: `proposta-de-honorarios` (se instalada), nova versão. Sem ela, copie a proposta, mude o que foi decidido e anote a mudança no topo.
- O cliente aceitou: `contrato-de-honorarios` (se instalada). Sem ela, use o modelo de contrato do escritório.
- Parou de responder: `follow-up` (se instalada). Sem ela, a `rotina-comercial` lembra pela data do registro.
- Disse não: o advogado marca `perdido` com o motivo (preco, fechou-com-outro, desistiu).

## Referências desta habilidade

- `references/biblioteca-de-objecoes.md`: as nove objeções, com o que pode estar por trás, a pergunta de esclarecimento, a resposta-base, o que nunca dizer e quando vai para o advogado. Leia no modo A, no modo F e quando a biblioteca do escritório não tiver a objeção.
