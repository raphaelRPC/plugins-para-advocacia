---
name: qualificar-contato
description: >
  Depois da triagem, decide o que o escritório faz com cada contato novo: consulta normal, consulta
  com prioridade, encaminhar ou recusar, por critérios escritos (encaixe na área, momento e urgência,
  vulnerabilidade, agenda, origem), sem pontuação que rebaixe alguém por renda ou perfil. Monta de 3
  a 5 perguntas para antes da consulta, a mensagem de cada decisão e a linha do funil. Roda com um
  contato, com a fila do dia ou no ciclo do agente, e reescreve as perguntas para o nicho. Use quando
  o advogado disser "esse contato vale consulta?", "quem eu atendo primeiro?", "tenho dois horários e
  cinco pedidos", "manda as perguntas antes da consulta", "isso a gente encaminha?". Não use para
  dizer se vale entrar com a ação, que é do advogado na consulta, nem para classificar a mensagem
  que acabou de chegar (use triar-contato).
---

# Qualificar o contato

> A triagem diz o que a mensagem é. A qualificação decide o que o escritório faz com quem escreveu: quando atender, com que prioridade, ou para onde indicar. O mérito do caso fica para o advogado, na consulta.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

Quarta-feira, 17h. Quinta tem dois horários de consulta livres e há três contatos triados esperando. Uma é a Helena, que escreve pela mãe de 72 anos, sem renda, com o BPC negado. Outra é a Renata, com um divórcio consensual. Quem marca pela ordem de chegada dá a quinta para quem escreveu primeiro e deixa a idosa para a semana seguinte.

**Regras fixas desta habilidade:**
1. Qualificar decide o encaixe no escritório e a ordem de atendimento. Se vale entrar com a ação é decisão do advogado, depois de ouvir o caso, e nunca vai por mensagem.
2. Nenhum critério exclui ou rebaixa alguém por renda, bairro, profissão, escolaridade, gênero, raça, idade, deficiência, religião, origem ou jeito de escrever. Vulnerabilidade só sobe a prioridade.
3. Pessoa em situação de vulnerabilidade não recebe mensagem escrita da habilidade, nem com valor de consulta: uma pessoa liga, com o roteiro da seção 6, e o que se oferece segue o campo `vulnerabilidade_e_consulta`, com a decisão do advogado.
4. Encaminhar e recusar são sugestões, e só uma pessoa move para `encaminhado` ou `recusado`. Encaminhamento com urgência (prisão, prazo de hoje ou amanhã) vai para PESSOA AGORA, sem rascunho; encaminhamento sem urgência vira rascunho na fila, revisado, e sai só com a aprovação de uma pessoa; no ciclo, recusa nunca vai para a fila (seção 4.6 e passo 9).
5. As perguntas prévias são de 3 a 5, sobre fatos, datas e papéis que a pessoa já tem. Nunca pedem senha, dado de saúde, documento sensível ou opinião sobre a tese. No ciclo, só vão ao contato as que o escritório já aprovou no roteiro da área.

## 1. Quando usar

**Use quando:**
- A triagem apontou "convite para consulta" ou "consulta com prioridade" e é preciso decidir quando e como.
- Há mais pedidos de consulta do que horários e o escritório quer uma ordem com critério.
- O advogado quer mandar perguntas antes da consulta para ela render.
- Um contato pediu algo que o escritório talvez não faça, e é preciso decidir entre consulta, encaminhar ou recusar.
- O agente do ciclo (`agente-comercial`) ou a `rotina-comercial` chamou para os contatos `triado` sem consulta marcada.
- A `adaptar-comercial` chamou no modo "adaptar".

**Não use quando:**
- A mensagem acabou de chegar e ainda não foi classificada: use `triar-contato`.
- A consulta está decidida e o pedido é marcar, confirmar ou remarcar: use `agenda-da-consulta` (se instalada; sem ela, a pessoa marca e a `roteiro-da-consulta` registra).
- A consulta está marcada e o pedido é o briefing: use `roteiro-da-consulta`.
- O contato pergunta "eu tenho direito?" ou "vale a pena?": isso é a consulta. A qualificação manda o convite, nunca a resposta.
- O contato sumiu e é preciso retomar: use `follow-up` (se instalada; sem ela, um único lembrete gentil no prazo da régua da ficha).
- Quem escreveu já é cliente: vai para a `triar-mensagem-do-cliente` do motor-experiencia (se instalado) ou para quem cuida do caso.

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir) e `aprendizados-comercial.md`. Aprendizado da `qualificar-contato` vale antes dos critérios desta habilidade, menos quando contraria a regra fixa 2: aí explique e proponha outra redação (`../../docs/aprender-com-o-uso.md`, conflito com a ética).
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Em que áreas vocês atuam e o que vocês recusam?" e "A consulta é paga ou gratuita?". Use as respostas e ofereça gravar no fim.
3. **Leia o contato:** a linha em `escritorio/07-operacao/comercial/contatos.csv` e o cartão da triagem em `escritorio/07-operacao/comercial/triagens/AAAA-MM-DD.md` (procure pelo código). Sem triagem, rode antes a parada imediata da `triar-contato` ou peça a triagem.
4. **Leia a agenda,** se a decisão envolve horário: com o conector de agenda que a ficha lista em `conectores_no_claude`, só para ler os horários livres (conferir na configuração da conta). Sem conector, pergunte: "Quais horários de consulta estão livres nos próximos dias?".
5. **Leia o roteiro da área** (`escritorio/04-base/atendimento-e-triagem/roteiro-consulta-<area>.md`), se existir: as perguntas prévias saem da seção "Perguntas prévias" dele.
6. **Treino:** com os casos de `../../docs/casos-ficticios.md`, tudo grava em `escritorio/07-operacao/_treino/comercial/`, nunca no registro real. Em conta pessoal, só treino ou mensagem anonimizada.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas`, `nao_atendemos` · C: `consulta`.
- **Melhora:** E: `casos_mais_comuns` · C: `origem_dos_contatos`, `vulnerabilidade_e_consulta`.

Campo que falta e a decisão pede: pergunte aquele campo, uma vez, e ofereça gravar. Sem `vulnerabilidade_e_consulta`, a habilidade não sugere isenção nem encaminhamento por conta própria: pergunta ao advogado "O que o escritório faz quando a pessoa não pode pagar a consulta?" e marca `[A DEFINIR]` até ele responder. O tom das mensagens e o caminho de encaminhamento vêm da ficha do escritório, como em toda mensagem.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Um contato | Triagem recém-feita | O código ou o cartão da triagem | O cartão da qualificação (seção 8) no chat |
| Fila | Começo do dia, agenda apertada | Os contatos `triado` sem consulta e os horários livres | A fila ordenada, com a data proposta para cada um |
| Só perguntas prévias | Decisão tomada, consulta a marcar | Código, área e tipo de caso | A mensagem com 3 a 5 perguntas |
| No ciclo | O `agente-comercial` chamou | Os contatos `triado` do registro e a fila do dia | Perguntas aprovadas acrescentadas ao convite que a triagem gravou, encaminhamento sem urgência na fila, roteiros de ligação no arquivo da triagem, nada no chat (passo 9) |
| Adaptar | A `adaptar-comercial` chamou | `nicho.md` e as perguntas atuais | Perguntas prévias reescritas para o nicho, com `[ALTERADO]` (passo 10) |

**Modo direto:** "qualifica a C-2026-0007, BPC da mãe, e manda as perguntas". Execute, mostre e pergunte só o que falta.

### Passo 1. Conferir a parada
Se o cartão da triagem ou a mensagem tem sinal de violência, ameaça, risco à vida, criança em risco ou prisão, a qualificação não roda: o contato já é do advogado agora (`triar-contato`). Diga isso em uma linha e pare.

### Passo 2. Conferir impedimentos
1. **Conflito de interesse:** o registro não guarda a parte contrária, então pergunte: "A outra parte já foi cliente de vocês? Dá para conferir no sistema?". Sim ou dúvida: pare e leve ao advogado.
2. **Outro advogado no caso:** a consulta pode acontecer, mas o advogado precisa saber antes `[CONFERIR]` no Código de Ética e Disciplina da OAB.
3. **Pedido que o escritório não faz:** parecer por mensagem, "só uma dúvida rápida" sem consulta, pedido para mentir ou esconder fato. Vai para recusa, com convite para a consulta quando couber.

### Passo 3. Aplicar os critérios
Percorra os cinco critérios da seção 4, nesta ordem. Para cada um, uma linha com o que foi visto e de onde veio (triagem, ficha, nicho, agenda). Critério sem informação: `[A CONFIRMAR]`.

### Passo 4. Decidir
Use a árvore da seção 4.6. Uma decisão por contato, com o motivo em uma frase. Encaminhar ou recusar sai como "sugestão", com a pergunta: "Confirma o encaminhamento para [DESTINO DA FICHA]?". A etapa `encaminhado` ou `recusado` só é gravada quando a pessoa confirma que a mensagem saiu.

### Passo 5. Falta informação para decidir
Se o encaixe depende de um fato que a triagem não trouxe (por exemplo, se o contrato é de consumo ou entre empresas), mande uma pergunta só, sem orientação, e marque o próximo passo "aguardar resposta". As outras perguntas vão nas perguntas prévias.

### Passo 6. Montar as perguntas prévias
Pela seção 5. De 3 a 5, do roteiro da área (seção "Perguntas prévias", as aprovadas) ou, a pedido e só para o advogado aprovar, de `references/perguntas-previas-por-area.md`, no vocabulário do `nicho.md` quando existir. Pergunta de exemplo vai ao contato só depois que o advogado aprova; com o ok, ofereça gravar no roteiro da área, para o ciclo poder usar. Com prioridade, no máximo 3. Vulnerabilidade: as perguntas vão no roteiro da ligação, em voz, nunca por escrito. Pedido de documento antes da consulta é curto e vai anotado no arquivo da consulta (seção 9), nunca documento sensível.

### Passo 7. Escrever a mensagem da decisão
Pela seção 6, a partir da biblioteca (`escritorio/04-base/comercial/biblioteca-comercial.md`, chaves `convite-consulta-paga`, `convite-consulta-gratuita`, `encaminhamento-outra-area`, `recusa-educada`), se existir. Toda mensagem é A: alguém lê antes de enviar. Encaminhar e recusar só saem depois do ok de uma pessoa (a pedido, no chat; no ciclo, o encaminhamento sem urgência pela fila). Vulnerabilidade: nenhuma mensagem escrita; a habilidade entrega o roteiro da ligação (seção 6) para a pessoa que liga, e o contato fica com `proximo_passo` começando por `pessoa liga:` (`funil.md`, regra 4, marcador de pessoa).

### Passo 8. Registrar
Proponha a atualização da linha no `contatos.csv` pela tabela da seção 9 e grave a qualificação no arquivo da triagem do dia, numa seção "Qualificação · [CÓDIGO]". Mostre e grave com o ok. Na fila, mostre todas as linhas juntas e grave de uma vez.

### Passo 9. No ciclo (chamada pelo agente)
1. Não mostre nada no chat. Para cada contato `triado` sem consulta marcada e sem perguntas prévias enviadas, aplique os passos 1 a 7. Pule quem tem `pediu_para_parar = sim` ou `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:`: esse contato está com uma pessoa.
2. **Perguntas aprovadas, e só elas.** No ciclo, só entram no texto ao contato as perguntas da seção "Perguntas prévias" do roteiro da área (`roteiro-consulta-<area>.md`) para o tipo de caso, gravadas com o ok do advogado (roteiro `em uso`, ou a seção gravada com o ok no passo 10). Pergunta de `references/perguntas-previas-por-area.md`, ou marcada como exemplo, `[A CONFIRMAR]` ou `[NOVO]`, nunca vai para a fila. Sem perguntas aprovadas para o tipo de caso: o convite segue sem perguntas, as de exemplo ficam no cartão da qualificação marcadas "exemplo, para o advogado aprovar", e em "PARA DECIDIR" vai uma linha: "C-2026-0005: sem perguntas prévias aprovadas para divórcio consensual; aprovar no roteiro da área".
3. **Consulta normal ou com prioridade: um convite só.** Procure na fila (`escritorio/07-operacao/comercial/fila/`, pastas do dia e dos dias anteriores) o rascunho que a triagem gravou para o código, com `tipo: convite-consulta-paga` ou `convite-consulta-gratuita`:
   - `status: pendente` ou `aprovado`: acrescente as perguntas aprovadas **no mesmo arquivo**, depois da pergunta sobre o horário e antes da assinatura, com a frase de abertura da seção 6. No cabeçalho: `revisor: pendente` de novo (o texto mudou e o `revisor-comercial` confere outra vez), `status: pendente` se estava `aprovado`, e no fim do `motivo` "+ perguntas prévias (qualificar-contato, AAAA-MM-DD HH:MM)". O `tipo` continua o do convite.
   - `status: enviado`: o convite já saiu. Não grave outra mensagem: as perguntas ficam no cartão da qualificação e vão junto com a próxima mensagem para o contato (a confirmação da consulta pela `agenda-da-consulta`, se instalada, ou a resposta da pessoa). Em "PARA DECIDIR": "C-2026-0001: perguntas prévias prontas; mandar junto com a confirmação".
   - `status: descartado` ou `bloqueado`: não mexa. Em "PARA DECIDIR", uma linha com o porquê.
   - Nenhum convite na fila (a triagem foi feita à mão): grave um convite só, com as perguntas aprovadas (ou sem perguntas, pelo item 2), em `fila/AAAA-MM-DD/NN-<codigo>-<chave do convite>.md`, no formato de `../../docs/agentes-e-fila.md`, com `status: pendente` e `revisor: pendente`.
   O horário fica `{DIA E HORA}`, para quem envia escolher na agenda. Com conector de agenda, os horários livres vão no `motivo`, como sugestão.
4. **Vulnerabilidade:** nenhum rascunho para o contato. Grave o roteiro da ligação (seção 6) no arquivo da triagem do dia, na seção "Qualificação · [CÓDIGO]", ponha `proximo_passo = pessoa liga: <o que combinar>` com a data de hoje, e o contato vai para "PESSOA AGORA" no resumo. Se a triagem tinha gravado um convite para ele, marque esse arquivo com `status: bloqueado` e `revisor: bloqueado: vulnerabilidade, uma pessoa liga (qualificar-contato)`. Nada é apagado.
5. **Encaminhar, a mesma regra da `triar-contato` (seção 4.3):**
   - **Com urgência** (prisão, flagrante, prazo de hoje ou amanhã, em área que o escritório não atende): nenhum rascunho. O contato vai para "PESSOA AGORA" com `proximo_passo = pessoa agora: enviar encaminhamento` e a chave `encaminhamento-urgente` para a pessoa usar na hora.
   - **Sem urgência** (área que o escritório não atende): um rascunho na fila, `tipo: encaminhamento-outra-area`, `status: pendente`, `revisor: pendente`, com o destino de `encaminhamos_para`. Se a triagem já gravou esse rascunho para o código, não grave outro. Se a triagem tinha gravado um convite e a qualificação concluiu que a área não é atendida, marque o convite com `status: bloqueado` e `revisor: bloqueado: qualificação sugere encaminhar (qualificar-contato)`. Sem `encaminhamos_para` na ficha: nenhum rascunho, uma linha em "PARA DECIDIR" ("falta o campo encaminhamos_para").
   - Nos dois, o `proximo_passo` fica `confirmar encaminhado` (ou o marcador de pessoa agora) e a etapa continua `triado`. `encaminhado` só uma pessoa grava, depois que a mensagem saiu.
6. **Conflito aparente e recusar:** nenhum rascunho. Vão para "PARA DECIDIR", com uma frase do porquê.
7. No registro, o agente só mexe nas colunas que `../../docs/funil.md` permite (regra 11). Encaminhado e recusado, nunca.
8. **Saída de PESSOA AGORA.** Depois da ligação, o comando `fila` pergunta "Já falou? O que ficou combinado?" e grava: a hora em `primeira_resposta` (se vazia), o `proximo_passo` combinado no lugar do que começa com `pessoa liga:`, com data, e uma linha no arquivo da triagem (`agentes-e-fila.md`). A pedido, esta habilidade faz o mesmo quando a pessoa conta como foi. Sem isso, o contato volta ao topo do resumo seguinte.

### Passo 10. Modo "adaptar" (chamada pela adaptar-comercial)
1. Leia `escritorio/04-base/comum/nicho.md`: os casos que chegam, como o cliente fala, os documentos típicos e os cuidados do nicho.
2. Para cada tipo de caso do nicho, reescreva as perguntas prévias com as palavras do cliente ("encostado" no lugar de "benefício por incapacidade", se é assim que ele fala), sem perder as regras da seção 5.
3. Mostre lado a lado, cada mudança marcada `[ALTERADO]` (ou `[NOVO]` para tipo de caso que não existia). Grave só com o ok, na seção "Perguntas prévias" do roteiro da área, com uma linha em "Mudanças" (data e "perguntas prévias aprovadas"): a partir daí o ciclo pode usá-las. Se o roteiro da área ainda não existe, crie o arquivo com situação `rascunho` e só essa seção, e avise que a `roteiro-da-consulta` completa o resto.
4. Devolva à `adaptar-comercial` a lista do que mudou.

### Passo 11. Aprender
Pergunte: "Alguma decisão você tomaria diferente?". Cada correção vira uma regra curta (por exemplo, "Revisão de benefício vista em anúncio: consulta normal, nunca prioridade") e, com o ok, entra em `aprendizados-comercial.md`. Área ou tipo de caso que o escritório não atende: ofereça gravar em `nao_atendemos` e `encaminhamos_para`. Correção que excluiria alguém por perfil (regra fixa 2) não entra: explique e proponha uma versão que olha o caso, e não a pessoa.

## 4. Os critérios

### 4.1 Encaixe na área e no tipo de caso
- A área está em `areas`? O tipo de caso está em `casos_mais_comuns` ou nos casos do `nicho.md`?
- Área atendida, tipo de caso raro: consulta normal, com a observação "tipo de caso pouco comum: o advogado confirma se atende" `[A CONFIRMAR]`.
- Área em `nao_atendemos` ou fora de `areas`: encaminhar, para o destino de `encaminhamos_para`.

### 4.2 Momento e urgência
- **Fase:** ainda não aconteceu, aconteceu e não tem processo, já tem processo, já tem decisão.
- **Data próxima** citada pelo contato, benefício ou salário cortado, carta do fórum, ou o que a ficha lista em `o_que_e_urgente`: sobe para prioridade. Prazo aparente fica `[CONFERIR]`, sem cálculo.
- **Data antiga:** não decide nada sozinha. Vai como alerta para o advogado, que avalia na consulta.
- **Remarcação e demissão** não são urgência por si: seguem como consulta normal, com o alerta no briefing.

### 4.3 Vulnerabilidade
Idoso sem renda, pessoa com deficiência, doença grave, gestante, criança envolvida, pessoa muito confusa ou aflita, e os cuidados que o `nicho.md` listar. Efeito: prioridade, uma pessoa liga antes da consulta, e a mensagem não traz valor. O que o escritório oferece (isenção, Defensoria Pública, núcleo de prática jurídica de faculdade) vem de `vulnerabilidade_e_consulta` e é decisão do advogado. Vulnerabilidade nunca é motivo para recusar.

### 4.4 Capacidade da agenda
- Prioridade ocupa o primeiro horário livre. Normal recebe a próxima data real, sem promessa ("o próximo horário é terça às 10h").
- Agenda cheia por mais de uma semana para quem tem prioridade: aponte ao advogado (encaixe extra ou ligação antes).
- A agenda muda a data, nunca a decisão.

### 4.5 Origem
- Vem de `origem_dos_contatos`. Serve para registrar e, só como desempate entre dois contatos iguais nos outros critérios, para cliente antigo do escritório.
- Indicação: a mensagem pode agradecer a confiança, mas nada do caso é contado a quem indicou.
- Contato que chegou por vídeo, anúncio ou resposta de IA com promessa ("todo aposentado tem direito") chega com expectativa alta: vai como alerta no briefing, e a mensagem não confirma nem desmente a tese.

### 4.6 A árvore da decisão

1. Sinal de parada imediata? **Pessoa agora** (sai desta habilidade).
2. Conflito de interesse aparente? **Para**, o advogado decide.
3. Área fora do escritório? **Encaminhar** (sugestão): no ciclo, rascunho `encaminhamento-outra-area` na fila, revisado e aprovado por uma pessoa. Urgência fora da área, como prisão: **encaminhar com urgência**, para PESSOA AGORA, sem rascunho; a pessoa usa a chave `encaminhamento-urgente` e envia em minutos, sem orientação. Nos dois, `encaminhado` só com a pessoa.
4. Pedido que o escritório não faz, ou antiético? **Recusar** (sugestão), com convite para a consulta se couber.
5. Falta um fato para saber se encaixa? **Perguntar** (passo 5).
6. Vulnerabilidade ou urgência da ficha? **Consulta com prioridade.**
7. Nenhum dos anteriores: **consulta normal.**

### 4.7 O que nunca entra como critério

Pontuação de contato que dá menos pontos para quem tem renda baixa, mora em certo bairro, escreve com erro, é idoso, usa áudio ou pediu parcelamento acaba excluindo quem mais precisa e trata pessoas de forma discriminatória. Esta habilidade não pontua pessoas. Ela olha o caso (área, fase, urgência) e a capacidade do escritório. Quando a pessoa diz que não pode pagar, a habilidade não recusa: mostra ao advogado o que a ficha prevê, e quem decide contratar ou não é o contato, informado.

## 5. As perguntas prévias

**Para que servem:** a consulta começa com o caso organizado, e o advogado usa o tempo para ouvir e explicar.

**Regras:**
1. De 3 a 5 perguntas, numeradas, numa mensagem só.
2. Fatos, datas e "o que você tem em mãos". Nada de "você acha que tem direito a X?".
3. Fáceis de responder pelo celular. Aceitam "não sei".
4. Nada de CPF, número de benefício, senha, laudo, documento de criança ou relato de violência por mensagem. Nada de dado de saúde: diagnóstico, doença, tratamento, remédio. "Que tratamento você faz hoje?" vira "Você ainda está sem condição de trabalhar?"; o resto fica para a consulta.
5. Responder é opcional: a consulta acontece do mesmo jeito.
6. A primeira pergunta é sempre a data que importa (o corte, a demissão, a separação, a compra).

**De onde saem:** da seção "Perguntas prévias" do roteiro da área, se existir. Sem roteiro, a pedido, de `references/perguntas-previas-por-area.md`, marcadas como exemplo, e só vão ao contato depois que o advogado aprova (com o ok, ofereça gravar no roteiro). No ciclo, só as do roteiro: pergunta de exemplo nunca vai sozinha para a fila (passo 9).

## 6. A mensagem de cada decisão

**Consulta normal** (base `convite-consulta-paga` ou `convite-consulta-gratuita`):
```
Oi, [NOME], tudo bem? Aqui é [FUNÇÃO] do [ESCRITÓRIO].
Para entender o seu caso direito, o melhor caminho é uma consulta com [QUEM FAZ]. [Como funciona, conforme a ficha: duração, formato e, se a ficha manda informar, se é paga e o valor.]
O próximo horário livre é {DIA E HORA}. Serve para você?

Para a consulta render, se puder, me responda por aqui (o que não souber, pode deixar em branco):
1. ...
2. ...
3. ...
```

Os colchetes a habilidade preenche com a ficha e o registro; nada entre colchetes vai ao contato (o que faltar vai para o cabeçalho "Antes de enviar"). Só o que quem envia escolhe na hora fica entre chaves, como `{DIA E HORA}`. No ciclo, este texto entra no convite que a triagem já gravou (passo 9).

**Consulta com prioridade, sem vulnerabilidade:** a mesma, com no máximo 3 perguntas, mais "Vou pedir para [FUNÇÃO] te ligar ainda hoje para combinar o melhor horário." Só escreva "hoje" se alguém de fato vai ligar hoje; na dúvida, fica só o `{DIA E HORA}` do primeiro horário livre.

**Vulnerabilidade: roteiro para a pessoa que liga** (H; nada disto vai por escrito ao contato):
```
ROTEIRO DA LIGAÇÃO · [CÓDIGO] · [nome curto] · ligar até [prazo]
Quem liga: [função, de quem_atende, ou o advogado]
Antes de ligar: o que o escritório oferece já foi decidido pelo advogado?
  [o que ele decidiu, pelo campo vulnerabilidade_e_consulta] ou "perguntar antes de ligar"
1. Apresente-se: nome, função, escritório. "Recebemos a sua mensagem e quis
   ligar para conversar com calma."
2. Escute. Deixe a pessoa contar. Não diga se tem direito nem se vale a ação.
3. Se quem escreveu fala por outra pessoa (a filha pela mãe): pergunte se a
   pessoa sabe e concorda, e se ela pode participar da consulta.
4. As perguntas prévias, em voz (até 3): [perguntas da seção 5].
5. O que o escritório oferece: só o que o advogado decidiu. Sem decisão, diga
   que vai confirmar e retornar, e com que prazo.
6. Combine a consulta: dia, formato (ligação, visita, online com ajuda de
   alguém) e o que trazer. Documento sensível não vai por WhatsApp.
7. Sinal de violência, ameaça ou risco à vida durante a ligação: pare o
   roteiro e chame o advogado agora. Risco imediato: os números de
   emergência de regras.md, seção 5.
8. Feche repetindo o combinado e quem fala de novo, e quando.
Depois: conte ao comando fila (ou a esta habilidade) o que ficou combinado.
```
As palavras do roteiro seguem o tratamento da ficha e o `nicho.md` (por exemplo, falar devagar e confirmar cada combinado com quem tem pouca leitura).

**Encaminhar** (base `encaminhamento-outra-area`; a pedido, depois do ok no chat; no ciclo, rascunho na fila para uma pessoa aprovar): "Oi, [NOME], obrigada por procurar a gente. O escritório não atua em [ÁREA], então não vamos conseguir cuidar do seu caso. Para não te deixar sem caminho: [ENCAMINHAMENTO DA FICHA]." Urgente fora da área (base `encaminhamento-urgente`): a mesma, curta, sem orientação, enviada em minutos pela pessoa que está com o contato em PESSOA AGORA; no ciclo, nenhum rascunho.

**Recusar** (depois do ok, base `recusa-educada`): motivo neutro ("Esse tipo de pedido o escritório não faz por mensagem") e, se couber, o convite para a consulta. Nunca diz que o caso "não tem chance": isso seria avaliação de mérito.

## 7. Exemplos resolvidos (Escritório Modelo, casos fictícios)

Escritório Modelo de `../../docs/casos-ficticios.md`. Fila da quarta, 2026-03-11, 17h. Quinta tem dois horários livres (10h e 14h); sexta, três.

| # | Contato | Decisão | Motivo | Data proposta |
|---|---|---|---|---|
| 7 | C-2026-0007 · Helena, pela mãe de 72 anos sem renda, BPC negado | Consulta com prioridade | Idosa sem renda; a filha fala pela mãe `[A CONFIRMAR]` autorização | quinta, 10h; a advogada liga hoje e decide a isenção |
| 1 | C-2026-0001 · Marta, auxílio-doença cortado | Consulta com prioridade | Benefício cortado está em `o_que_e_urgente` | quinta, 14h |
| 5 | C-2026-0005 · Renata, divórcio consensual, "é rápido?" | Consulta normal | Expectativa de prazo vai para o briefing | sexta |

Paulo (caso 2, C-2026-0002, demissão) foi qualificado na terça como consulta normal, com a data da saída como alerta `[CONFERIR]`, e fez a consulta hoje. Diego (caso 11, C-2026-0011) chega na quinta e entra na fila daquele dia: consulta normal, com o alerta de expectativa vinda de vídeo e de IA, e a mensagem não confirma nem desmente a tese. Lúcia (caso 4, C-2026-0004, filho preso, criminal) já saiu da triagem como "encaminhar com urgência"; a qualificação só confere que o destino é o da ficha. Joana (3), Sérgio (6), Bruno (8), Antônio (9) e Fernanda (12) não passam por aqui: parada imediata, objeção, remarcação, pedido de parar e cliente ativo.

Perguntas prévias do caso 1 (roteiro de previdenciário aprovado pela advogada, `situacao: em uso`):
1. Em que data chegou a carta do INSS cortando o benefício?
2. Quando foi a sua última perícia?
3. Você ainda está sem condição de trabalhar?
4. Você guarda as cartas do INSS e os papéis do médico? Não precisa mandar: traga na consulta.

Helena não recebe mensagem escrita. A advogada liga com o roteiro da seção 6 e decide a isenção antes. A linha dela: `urgencia` alta, `responsavel` advogada, `proximo_passo` "pessoa liga: combinar a consulta da mãe com prioridade", `data_proximo_passo` 2026-03-11. Depois da ligação, pelo comando `fila`: `primeira_resposta` 2026-03-11 17:40, `proximo_passo` "consulta da mãe na quinta 10h, com a Helena junto", `data_proximo_passo` 2026-03-12.

No ciclo, a Renata, que escreveu às 07h12, tem o convite da triagem ainda pendente na fila (`fila/2026-03-11/03-C-2026-0005-convite-consulta-paga.md`, numeração de exemplo). Se o roteiro de família tem perguntas aprovadas para divórcio consensual, elas entram nesse arquivo, que volta a `revisor: pendente`; se não tem, o convite segue sem perguntas e o resumo pede a aprovação em "PARA DECIDIR". A Lúcia, com o filho preso e o criminal fora da área, está em PESSOA AGORA desde a triagem, sem rascunho. O convite da Marta já foi enviado na terça: nenhuma mensagem nova; as perguntas dela vão junto com a confirmação da consulta. Nenhum contato recebe dois convites.

## 8. Formato da saída

```
QUALIFICAÇÃO · [CÓDIGO] · [nome curto] · [AAAA-MM-DD]
Área: ...   Tipo de caso: ...   Triagem: urgência ..., caminho ...
Impedimentos: nenhum | conflito a conferir | outro advogado | pedido que não fazemos
Critérios:
- Encaixe: ...
- Momento e urgência: ...
- Vulnerabilidade: ... (ou "nenhuma aparente")
- Agenda: próximo horário livre ...
- Origem: ...
Decisão: consulta normal | consulta com prioridade | sugestão: encaminhar para ... | sugestão: recusar
Motivo: (uma frase)
Perguntas prévias: (3 a 5, ou "não se aplica")
Mensagem (A, [função] lê antes de enviar): "..."  (ou "nenhuma: uma pessoa liga", com o roteiro da ligação)
Registro: [linha proposta do contatos.csv]
Em aberto: ...
```

**Na fila:** uma tabela com código, nome curto, área, decisão, motivo, data proposta e quem cuida, prioridade no topo. Depois, os cartões e as linhas do registro.

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Cartão da qualificação (ou a fila) | `escritorio/07-operacao/comercial/triagens/AAAA-MM-DD.md`, seção "Qualificação · [CÓDIGO]" |
| Documentos pedidos antes do contrato | `escritorio/07-operacao/comercial/consultas/<codigo>-AAAA-MM-DD.md`, seção "Documentos pedidos antes do contrato" (criada quando a consulta tem data) |
| Perguntas no ciclo | No convite que a triagem gravou: `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave do convite>.md` (o mesmo arquivo, `revisor: pendente` de novo) |
| Encaminhamento sem urgência no ciclo | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-encaminhamento-outra-area.md`, se a triagem não gravou |
| Roteiro da ligação (vulnerabilidade) | `escritorio/07-operacao/comercial/triagens/AAAA-MM-DD.md`, seção "Qualificação · [CÓDIGO]" |
| Perguntas adaptadas ao nicho | `escritorio/04-base/atendimento-e-triagem/roteiro-consulta-<area>.md`, seção "Perguntas prévias" |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Área ou destino novo aprovado | `escritorio/04-base/comum/ficha-do-escritorio.md` (`nao_atendemos`, `encaminhamos_para`), com linha no histórico |
| Treino | `escritorio/07-operacao/_treino/comercial/` |

| Decisão | `etapa` | `urgencia` | `proximo_passo` e data |
|---|---|---|---|
| Consulta normal | `triado` (vira `consulta-agendada` quando a data for marcada) | mantém | mantém a régua da triagem ("retorno 1 de N" na data do primeiro retorno de "não agendou"); se a régua não estava armada, arma |
| Consulta com prioridade (urgência da ficha) | `triado` | `alta` | mantém a régua da triagem; `responsavel` designado (urgência alta sem pessoa designada fica fora da régua, `funil.md`, regra 5) |
| Consulta com prioridade por vulnerabilidade | `triado` | `alta` | "pessoa liga: <o que combinar>", hoje (fora da régua) |
| Perguntar antes | `triado` | mantém | "aguardar resposta", com a data do primeiro retorno da régua |
| Encaminhar, antes da mensagem sair | `triado` | mantém | "confirmar encaminhado", hoje (com urgência: "pessoa agora: enviar encaminhamento") |
| Encaminhar (a pessoa confirma que saiu) | `encaminhado` | mantém | "nenhum" |
| Recusar (com o ok) | `recusado` | mantém | "nenhum" |

O motivo de encaminhar ou recusar fica no cartão, não no `contatos.csv`. Sem pasta aberta: entregue tudo no chat, com o caminho de cada arquivo.

## 10. Solo e equipe

**Solo:** o titular qualifica a fila uma vez por dia, no mesmo horário em que lê a triagem. A árvore evita que a decisão dependa do cansaço do fim do dia. Prioridade tem o primeiro horário livre, mesmo que isso empurre um contato mais antigo.

**Equipe:** a secretária aplica a árvore e manda as perguntas prévias. O advogado recebe só o que é dele: conflito de interesse, encaminhar, recusar, vulnerabilidade e prioridade. Se uma área recebe sempre prioridade e a agenda não acompanha, é sinal de abrir mais horários para ela.

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Atender pela ordem de chegada | Quem é vulnerável espera mais | Prioridade por critério escrito |
| Pontuação que rebaixa por renda ou perfil | Discriminação e exclusão de quem mais precisa | Regra fixa 2 e seção 4.7 |
| Valor de consulta para idosa sem renda | Constrangimento e pessoa que desiste | Regra fixa 3: uma pessoa liga com roteiro, campo `vulnerabilidade_e_consulta` |
| Dois convites para o mesmo contato no mesmo dia | Contato confuso, escritório parece desorganizado | No ciclo, as perguntas entram no convite que a triagem gravou |
| Dizer por mensagem que "não vale a pena" | Avaliação de mérito sem consulta | Recusa com motivo neutro |
| Recusa ou encaminhamento sem uma pessoa | Caso perdido por engano | Sugestão e confirmação; no ciclo, recusa fora da fila, encaminhamento sem urgência só pela fila, com aprovação |
| Pergunta de exemplo enviada sem aprovação | Pergunta que o escritório não faria, às vezes sobre saúde | No ciclo, só as perguntas aprovadas no roteiro da área |
| Encaminhamento de prisão esperando a fila | Horas perdidas numa hora crítica | Urgência fora da área vai para PESSOA AGORA, sem rascunho |
| Qualificação que desarma a régua | Contato some do retorno | A régua da triagem fica na linha |
| Perguntas que pedem laudo ou CPF | Dado sensível no WhatsApp | Regra fixa 5 |
| Conflito de interesse descoberto na consulta | Constrangimento e risco ético | Impedimentos antes dos critérios |

## 12. Próximo passo

- Consulta decidida: `agenda-da-consulta` (se instalada) marca e confirma; sem ela, a pessoa marca e a `roteiro-da-consulta` registra `consulta-agendada`.
- Consulta marcada: `roteiro-da-consulta` faz o briefing.
- Contato que não respondeu ao convite: `follow-up` (se instalada); sem ela, um lembrete gentil no prazo da régua.
- Mensagem nova que não existia na biblioteca: `mensagens-comerciais`, para aprovar e guardar.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

- `references/perguntas-previas-por-area.md`: exemplos de perguntas prévias por tipo de caso (previdenciário, trabalhista, família, consumidor, cível), para o advogado aprovar. Leia no passo 6, a pedido, quando a área ainda não tem roteiro, e no passo 10 como ponto de partida da adaptação. Nunca vão direto para a fila do ciclo.
