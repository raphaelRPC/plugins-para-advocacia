---
name: mensagens-comerciais
description: >
  Escreve e mantém a biblioteca comercial do escritório, no tom das fichas: as mensagens para
  quem ainda não é cliente (boas-vindas ao contato novo, fora do horário com o caminho real de
  urgência, convite para consulta paga ou gratuita, confirmação, lembrete e remarcação de
  consulta, "recebi, te retorno até", encaminhamento comum e com urgência, recusa, quem pediu
  para parar, envio de proposta, cortesia, aviso de automática, resumo depois da consulta), cada
  uma com chave fixa. Tem o
  modo rápido (quatro modelos, até quatro perguntas), o completo, o "responder agora", o adaptar
  e o modo no ciclo. Use quando o advogado disser "escreve as mensagens-padrão", "quero respostas
  prontas", "ajusta ao nosso tom", "me dá a resposta para isso".
  Não use para classificar a mensagem que chegou (use triar-contato) nem para mensagem a cliente
  com caso em andamento (use a biblioteca do motor-experiencia).
---

# Mensagens comerciais

> Dezessete mensagens cobrem quase tudo o que o escritório escreve para quem ainda não é cliente. Escritas uma vez no tom da casa e aprovadas, deixam de ser reinventadas a cada conversa.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-comercial-modelo.md` e a tabela de campos em `../../docs/ficha-comercial.md`. Funil: `../../docs/funil.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 21h14. Marta escreve que o auxílio-doença foi cortado. A automática responde "se for urgente, escreva URGENTE", e ela escreve. Ninguém lê o canal até as 9h. A biblioteca troca isso por uma mensagem que diz a verdade: quando alguém lê, qual é o caminho real de urgência do escritório e, se houver perigo, os números de emergência.

**Regras fixas desta habilidade:**
1. Só mensagens a quem ainda não é cliente. As de cliente ativo moram na biblioteca do motor-experiencia.
2. Nenhum modelo promete resultado, prazo ou chance, orienta quem não é cliente ou diz valor de ação.
3. Valor, prazo, horário, caminho de urgência e encaminhamento vêm da ficha. O que falta vai para o "Antes de enviar" interno, nunca para o texto do contato. O que quem envia escolhe na hora (nome, horário da agenda, link) fica entre chaves, `{DIA E HORA}`.
4. Mensagem automática diz que é automática. O fora do horário nunca promete um caminho de urgência que ninguém atende.
5. Sinal de violência, ameaça, criança em risco ou risco à vida: nenhum modelo. Vai para uma pessoa agora.

## 1. Quando usar

**Use quando:**
- O escritório ainda não tem mensagens-padrão para contatos, ou cada pessoa responde de um jeito.
- O `/motor-comercial:comecar` sugeriu o próximo passo "suas mensagens no tom do escritório" (modo rápido).
- A `triar-contato` sugeriu um rascunho que "ainda não está na biblioteca" e o advogado quer guardar.
- Chegou uma mensagem concreta de contato e o advogado quer a resposta pronta (modo "responder agora").
- O `agente-comercial` precisa de um rascunho a partir de uma chave (modo no ciclo).
- A `adaptar-comercial` pediu os modelos no jeito do nicho (modo adaptar).

**Não use quando:**
- O pedido é decidir o que fazer com a mensagem (urgência, área, caminho): `triar-contato`.
- A mensagem é de cliente com caso em andamento (andamento, documento do caso, resumo do mês): habilidades do motor-experiencia (se instalado). Sem ele, responda com `recebi-retorno-ate` e leve ao advogado.
- O pedido é o retorno a quem sumiu: `follow-up` (se instalada); sem ela, parta do convite e respeite `pediu_para_parar`.
- O pedido é responder objeção de preço: `objecoes-comerciais` (se instalada); sem ela, `recebi-retorno-ate` e o advogado responde.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-comercial.md`. Leia `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado de tom e de frase vale antes de qualquer modelo deste plugin.
3. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, use as perguntas do modo rápido (passo R1).
4. **Leia a biblioteca comercial** (`escritorio/04-base/comercial/biblioteca-comercial.md`), se existir, e a do cliente (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`) só para ler. Siga `references/tom-e-conferencia.md`, seção 4.
5. **Leia o código do escritório**, se existir (`escritorio/01-cultura/codigo-do-escritorio.md`). Divergência com a ficha: mostre e pergunte qual vale.
6. **Conta de IA.** No "responder agora", em conta pessoal, só mensagem fictícia ou anonimizada.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `tratamento`, `tom_em_tres_palavras`, `assinatura_das_mensagens`, `horario_de_atendimento` · C: `consulta`, `como_agenda` |
| Melhora | E: `frase_que_soa_como_a_gente`, `frases_que_nunca_usamos`, `emoji`, `como_o_cliente_fala`, `urgencia_vai_para` · C: `fora_do_horario`, `informa_valor_da_consulta_por_mensagem`, `valor_da_consulta` |

Modelos específicos usam também, se a ficha tiver: `nome`, `quem_atende`, `o_que_e_urgente`, `encaminhamos_para`, `nao_atendemos` (E) e `duracao`, `formato`, `abate_dos_honorarios`, `quem_faz_a_consulta`, `remarcacao`, `validade_da_proposta`, `quem_aprova_a_proposta` (C). Campo que o modelo precisa e falta: pergunte uma vez; se o advogado não souber, a pendência vai para o "Antes de enviar" do modelo e para a lista "em aberto" do fim.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Rápido | "só o básico", primeira vez | Quatro modelos: o convite (`convite-consulta-paga` ou `-gratuita`), `fora-do-horario`, `recebi-retorno-ate`, `encaminhamento-urgente`. No máximo 4 perguntas |
| Completo | Montar ou completar a biblioteca | Os dezessete modelos (ou os que faltam) |
| Responder agora | Chegou uma mensagem de contato | A resposta preenchida, no chat (seção 6) |
| Ajustar | Um modelo saiu errado ou o tom mudou | O modelo novo no mesmo número, com linha em "Mudanças" |
| Adaptar | A `adaptar-comercial` chama | Os modelos reescritos para o nicho, com `[ALTERADO]`. Sem biblioteca, cria pelo modo rápido e adapta em seguida |
| No ciclo | O agente chama com a chave e o contato | O rascunho gravado na fila. Não mostra nada |

Pedido direto ("escreve o modelo de remarcação"): vá ao passo 3 só com aquele modelo.

### Modo rápido

**R1. Perguntas (no máximo quatro, só as que a ficha não responde, uma por vez):**
1. "Vocês tratam quem escreve por você, senhor e senhora, ou pelo nome? E três palavras para o jeito de vocês falarem."
2. "Como vocês assinam as mensagens?"
3. "A consulta é paga ou gratuita, e como a pessoa marca? Vocês dizem o valor por mensagem?"
4. "Fora do horário, alguém atende urgência? Se sim, por qual caminho a pessoa chega até ela?"

**R2.** Escreva os quatro modelos pelos passos 3 e 4. Sem `encaminhamos_para`, o `encaminhamento-urgente` sai com a pendência no "Antes de enviar" e o aviso de que ele não pode ser usado até alguém preencher.

**R3.** Mostre os quatro juntos, ajuste e grave com o ok (passo 6). Feche com o passo 7.

### Passo 1. Ver o que já existe
- Biblioteca comercial existe: liste os modelos (número, título, chave) e diga quais das dezessete chaves já estão cobertas. Pergunte: "Quer que eu escreva só os que faltam?".
- Não existe: diga que vai criar o arquivo com o cabeçalho de `assets/modelos-de-mensagem.md`.
- Existe a biblioteca do cliente: confira o `fora-do-horario` dela (regra 3 da seção 4 de `references/tom-e-conferencia.md`).

### Passo 2. Calibrar o tom
- Traduza `tratamento`, `tom_em_tres_palavras`, `frase_que_soa_como_a_gente`, `frases_que_nunca_usamos`, `emoji` e o vocabulário de `nicho.md` em escolhas concretas (`references/tom-e-conferencia.md`, seção 1).
- Sem `frase_que_soa_como_a_gente`, pergunte uma vez: "Me mande uma mensagem que vocês já mandaram e de que gostaram, sem o nome de ninguém."
- Mostre um modelo só (o convite) já no tom. Pergunte: "Soa como vocês?". Ajuste até o sim, depois siga.

### Passo 3. Escrever os modelos
- Parta de `assets/modelos-de-mensagem.md`. Reescreva no tom, sem mudar a estrutura, a chave, o "Antes de enviar" nem o "nunca usar quando".
- Preencha o que é fixo do escritório com a ficha: na biblioteca aprovada não sobra nenhum campo fixo entre colchetes (ficam só as instruções `[DA ATA: ...]` do modelo 17, que a `ata-da-consulta` preenche a cada consulta). O que muda a cada conversa e quem envia escolhe na hora fica entre chaves (`{NOME}`, `{DIA E HORA}`, `{LINK}`), e cada modelo lista os seus em "Campos do envio". As chaves são de propósito: o `revisor-comercial` aceita, e a fila só deixa marcar `enviado` depois que quem envia preencheu (`../../docs/regras.md`, seção 3).
- Consulta: `paga` escreve o modelo 3; `gratuita`, o 4; `depende do caso`, os dois, dizendo quando usar cada um. Valor da consulta só se `informa_valor_da_consulta_por_mensagem` permite.
- **Fora do horário:** leia `urgencia_vai_para`. Se é um caminho que o contato pode usar sozinho (plantão, telefone de urgência), entra no texto. Se é interno ("o advogado é avisado no celular"), não entra, e vale a variação sem plantão. Os dois levam os números de emergência de `regras.md` para perigo imediato, com `[CONFERIR]` no "Antes de enviar". Nunca "escreva URGENTE".
- Numeração: biblioteca nova, de 1 a 17; existente, a partir do próximo número livre.
- `resumo-depois-da-consulta` (17): o texto fixo fica na biblioteca; o conteúdo `[DA ATA: ...]` só é preenchido pela `ata-da-consulta` (se instalada) a cada consulta. Sem ela, o advogado preenche a partir das anotações dele.

### Passo 4. Conferir
Passe cada modelo pelos treze itens de `references/tom-e-conferencia.md`, seção 3. Modelo que falha volta para o passo 3. Não mostre modelo reprovado.

### Passo 5. Mostrar e ajustar
- Completo: em três partes, pedindo o ok de cada uma (primeiro contato e consulta: 1 a 9; encaminhar, recusar, parar: 10 a 13; proposta, automáticas e resumo depois da consulta: 14 a 17).
- Para cada ajuste, pergunte se vale só para aquele modelo ou para todos.

### Passo 6. Gravar
- Com o ok, grave em `escritorio/04-base/comercial/biblioteca-comercial.md`. Nova: cabeçalho, regras, modelos e "Mudanças". Existente: modelos novos no fim, versão nova e linha em "Mudanças".
- `fora-do-horario` escolhido diferente do da biblioteca do cliente: avise que o do cliente precisa ser trocado pela habilidade do motor-experiencia, para o canal ter um texto só.
- Sem pasta aberta: a biblioteca inteira num bloco para copiar, com o caminho.

### Passo 7. Aprender
Pergunte: "Alguma mensagem você mudaria o jeito de dizer?". Correção que vale além de um modelo vira regra curta ("Não abrir mensagem com 'prezado'") e, com o ok, entra em `aprendizados-comercial.md` (`../../docs/aprender-com-o-uso.md`). Frase proibida, assinatura ou tratamento novo: ofereça gravar direto na ficha do escritório, com linha no histórico.

### Modo "responder agora"
1. **Receber** a mensagem, com hora e canal. Se veio da `triar-contato`, use o caminho do cartão.
2. **Cliente ativo?** Fala do processo ou do caso: não responda daqui (regra fixa 1).
3. **Parada imediata.** Violência, ameaça, criança em risco, risco à vida: nenhuma resposta; diga em uma frase o que apareceu e que vai para o advogado agora. Prisão ou prazo de hoje ou amanhã fora da área: `encaminhamento-urgente`, para enviar em minutos. Vulnerabilidade forte (idoso sem renda, doença grave): nenhum modelo com preço; uma pessoa liga.
4. **Escolher o modelo** pela tabela da seção 4. Dois pedidos: uma mensagem só, o mais sensível primeiro.
5. **Preencher** com a ficha e com a mensagem. Nunca invente data, horário livre ou valor. O que quem envia escolhe na hora (o horário da agenda, o link) fica entre chaves, `{DIA E HORA}`. O que falta na ficha é pendência: vai para o "Antes de enviar", e a mensagem só sai depois que alguém preencher.
6. **Entregar** no formato da seção 6.
7. **Registrar.** Se a resposta muda o funil (convite, consulta marcada, parar, retorno prometido), proponha a linha do `contatos.csv` (`../../docs/funil.md`; `primeira_resposta` só depois que alguém confirmar o envio) e grave com o ok.
8. **Sem modelo que sirva:** rascunhe no tom, marque "rascunho: ainda não está na biblioteca" e pergunte se guarda.
9. **Aprender**, como no passo 7.

### Modo adaptar
0. **Sem biblioteca comercial ainda:** não há o que adaptar. Diga: "Vocês ainda não têm a biblioteca comercial. Vou criar os quatro modelos do modo rápido no tom da ficha e já adaptar ao nicho." Rode o modo rápido (R1 a R3, com as perguntas que a ficha não responde), grave com o ok e siga daqui com a biblioteca recém-criada. Os outros modelos entram depois pelo modo completo, já no jeito do nicho.
1. Leia `nicho.md` (como o cliente fala, cuidados do nicho, o que ele pesquisa sozinho) e a biblioteca comercial.
2. Reescreva cada modelo para o nicho: vocabulário do cliente, a variação de resposta de IA com o erro mais comum do nicho, o "o que trazer" típico, o canal preferido. Não mude chave, estrutura, "Antes de enviar" nem "nunca usar quando".
3. Marque cada trecho mudado com `[ALTERADO]` e passe pela conferência. Mostre por partes.
4. Com o ok, grave no mesmo número, tire as marcas `[ALTERADO]`, suba a versão e escreva em "Mudanças": "adaptado ao nicho [NOME]".

### Modo no ciclo
1. O agente passa a chave, o código do contato e o motivo. Não pergunte nada e não mostre nada.
2. Leia a biblioteca comercial. Sem a chave lá, use o modelo cru de `assets/modelos-de-mensagem.md` no tom da ficha e marque no `motivo` "modelo ainda não aprovado na biblioteca".
3. Preencha. Campo do envio (horário da agenda, link, nome que a mensagem não trouxe): fica entre chaves, `{DIA E HORA}`, e o `motivo` diz quem preenche. Campo da ficha que falta: o texto não leva a linha, a pendência vai para o "Antes de enviar" do rascunho e o `motivo` diz qual campo; se o modelo não fica de pé sem ele (por exemplo, `encaminhamento-urgente` sem `encaminhamos_para`), o rascunho leva a pendência entre colchetes e o `revisor-comercial` bloqueia até alguém preencher.
4. Grave em `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md`, no formato de `agentes-e-fila.md`, com `status: pendente`, `tipo: <chave>`, `revisor: pendente` e o prazo que o agente passou. Treino: `escritorio/07-operacao/_treino/comercial/fila/`.
5. Contato com `pediu_para_parar = sim` ou em PESSOA AGORA (`proximo_passo` com `pessoa agora:` ou `pessoa liga:`, `funil.md`, regra 4): não grave nada e devolva "bloqueado: vai para uma pessoa". Ele só sai dali depois que a pessoa falou e o combinado entrou no lugar do marcador (`agentes-e-fila.md`); a partir daí, rascunho só se o combinado pedir uma mensagem (por exemplo, a confirmação da consulta marcada na ligação).

## 4. A biblioteca

| Nº | Chave | Mensagem | Quando | Rápido |
|---|---|---|---|---|
| 1 | `boas-vindas-contato-novo` | Boas-vindas ao contato novo | Primeira resposta, sem pedido claro | |
| 2 | `fora-do-horario` | Fora do horário | Fora do `horario_de_atendimento` | sim |
| 3 | `convite-consulta-paga` | Convite para a consulta paga | Preço, "tenho direito?", prazo, quer contratar | sim, se paga |
| 4 | `convite-consulta-gratuita` | Convite para a consulta gratuita | O mesmo, sem custo | sim, se gratuita |
| 5 | `confirmacao-de-consulta` | Confirmação de consulta | Logo depois de marcar | |
| 6 | `lembrete-de-consulta` | Lembrete de consulta | Véspera e, se online, no dia | |
| 7 | `remarcacao` | Remarcação | Contato pede, escritório pede, depois da falta | |
| 8 | `recebi-retorno-ate` | Recebi, te retorno até | A resposta completa não sai na hora | sim |
| 9 | `documentos-para-a-consulta` | Documentos para a consulta | Depois de marcar | |
| 10 | `encaminhamento-outra-area` | Encaminhamento | Área não atendida, sem urgência | |
| 11 | `encaminhamento-urgente` | Encaminhamento com urgência | Prisão ou prazo de hoje ou amanhã fora da área | sim |
| 12 | `recusa-educada` | Recusa educada | O advogado decidiu não assumir | |
| 13 | `confirmacao-parar` | Quem pediu para parar | Pediu para não receber mensagens | |
| 14 | `envio-de-proposta` | Envio de proposta | Junto com a proposta aprovada | |
| 15 | `cortesia` | Cortesia curta | Obrigado, ok, despedida | |
| 16 | `aviso-automatico` | Aviso de mensagem automática | Toda mensagem sem pessoa digitando | |
| 17 | `resumo-depois-da-consulta` | Resumo depois da consulta | Dia da consulta ou o seguinte; a `ata-da-consulta` preenche | |

Todas são A: alguém aprova. As automáticas (2 e 16) são aprovadas uma vez e conferidas por amostra. Os caminhos "pessoa agora" e "pessoa liga" são H e não têm modelo.

### Que modelo para cada mensagem (responder agora e ciclo)

| A mensagem diz | Modelo | Observação |
|---|---|---|
| Primeiro contato, sem pedido claro | 1 (ou 2, fora do horário) | |
| "Quanto custa?", "tenho direito?", "é rápido?", "quero entrar com processo" | 3 ou 4, com a variação | Nada de valor de ação, prazo ou opinião sobre o caso |
| "A IA disse que eu tenho direito" | 3 ou 4, variação IA | Acolhe, sem confirmar nem desmentir |
| Urgente da ficha em área atendida (benefício cortado) | 3 ou 4, variação prioridade | Próximo horário real da agenda |
| "Pode ser quinta às 10h?" | 5 | Só depois de confirmar na agenda |
| "Preciso remarcar a consulta" | 7 | Audiência ou perícia de cliente não é daqui |
| "Achei caro", dúvida da proposta | 8 | E a `objecoes-comerciais`; sem desconto, sem falar de colega |
| Área não atendida | 10; 11 se prisão ou prazo de hoje ou amanhã | 11 sai em minutos |
| "Não quero mais receber mensagem" | 13 | Sem perguntar o motivo |
| "Obrigado!", "ok" | 15 | Com queixa junto, volta para a triagem |
| Consulta feita, a pessoa precisa do combinado por escrito | 17 | Pela `ata-da-consulta`; o advogado lê antes |
| Idosa sem renda, doença grave | nenhum | Uma pessoa liga, sem valor de consulta |
| Violência, ameaça, criança em risco | nenhum | Pessoa agora |
| "Alguma novidade do meu processo?" | nenhum | Cliente ativo: motor-experiencia |

## 5. Exemplos resolvidos (Escritório Modelo)

Escritório Modelo de `../../docs/casos-ficticios.md`: você, "próximo, claro, sem pressa", "Equipe Escritório Modelo", dias úteis das 9h às 18h, consulta paga de 40 minutos abatida dos honorários (R$ 250, valor de exemplo). A ficha do exemplo não tem plantão: `urgencia_vai_para` é "ligação para o celular da advogada", caminho interno.

**Mensagem 1 (Marta, seg 21h14, auxílio-doença cortado).** Sai a variação sem plantão do modelo 2. Na terça, até 11h, a secretária manda o modelo 3 na variação prioridade, com o valor da consulta (Marta perguntou "quanto custa?" e a ficha de treino informa só se perguntarem) e o primeiro horário em `{DIA E HORA}`, que ela preenche olhando a agenda.
```
Olá! Esta é uma mensagem automática do Escritório Modelo.

Nosso atendimento é de segunda a sexta, das 9h às 18h. Fora desse horário, ninguém da equipe lê as mensagens. A sua ficou registrada e é das primeiras que vamos ler amanhã, a partir das 9h.

Se você ou alguém estiver em perigo agora, não espere a nossa resposta: ligue 190 (polícia). Violência contra a mulher: 180. Apoio emocional: 188. Emergência médica: 192.
```

**Mensagem 4 (Lúcia, ter 14h05, filho preso, criminal).** Modelo 11, revisado e enviado em minutos:
```
Lúcia, sinto muito pelo que vocês estão passando. Nós não atuamos em criminal, e por isso não somos as pessoas certas para ajudar agora.

Procure hoje mesmo a Defensoria Pública ou um advogado criminalista.
```
Se a ficha tiver o contato de um colega parceiro que autorizou a indicação, ele entra nesta última linha, já preenchido na biblioteca.

**Mensagem 8 (Bruno, qua 18h40, remarcar a consulta de amanhã).** Modelo 2 na hora. Na quinta cedo, modelo 7, com `{OPÇÃO 1}` a `{OPÇÃO 3}` preenchidos por quem envia com três horários livres da agenda.

**Mensagem 11 (Diego, qui 15h48, revisão que a IA disse que ele tem).** Modelo 3, variação IA: "Faz sentido querer entender isso. Para saber se vale para o seu caso, a advogada precisa olhar o seu benefício de perto." Sem dizer se a revisão existe ou não.

**Mensagens 3 e 7 (Joana, ameaça com crianças; Helena, mãe de 72 anos sem renda).** Nenhum modelo. Joana: pessoa agora. Helena: uma pessoa liga, sem valor de consulta.

## 6. Formato da saída

**Biblioteca:** cada modelo no formato de `assets/modelos-de-mensagem.md` (número e título; chave; quando usar; quem lê e sigla; campos fixos; antes de enviar; texto-modelo em bloco; variações; nunca usar quando).

**Responder agora:**
```
RESPOSTA · modelo [Nº] [chave] · A
Quem lê antes de enviar: [função da ficha]
Antes de enviar (interno): [o que conferir; campos que faltam, ou "nada"]
Campos do envio: [os {...} que quem envia preenche, ou "nenhum"]
"[texto pronto, com os campos do envio entre chaves]"
Registro: [linha proposta do contatos.csv, ou "não muda o funil"]
```

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Biblioteca comercial (criada, ampliada ou adaptada) | `escritorio/04-base/comercial/biblioteca-comercial.md` |
| Resposta do "responder agora" | No chat, para copiar |
| Rascunho do modo no ciclo | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md` (treino em `escritorio/07-operacao/_treino/comercial/fila/`) |
| Linha do funil, quando a resposta muda a etapa ou promete retorno | `escritorio/07-operacao/comercial/contatos.csv`, com o ok |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Frase proibida, assinatura ou tratamento novo | `escritorio/04-base/comum/ficha-do-escritorio.md`, com linha no histórico |

A biblioteca fica em `04-base/` e pode ir para o Projeto no Claude. Sem pasta aberta: o bloco da biblioteca vai para os arquivos do Projeto, e as linhas do funil viram tabela para colar na planilha.

## 8. Solo e equipe

**Solo:** comece pelo modo rápido. O fora do horário honesto tira o peso de olhar o celular à noite, e o convite pronto resolve a maior parte do dia. Leia os convites em dois horários fixos.

**Equipe:** a biblioteca é o que faz a secretária e a advogada soarem como o mesmo escritório. Um dono só (campo `dono`) aprova mudança. Quem achar um modelo ruim pede o ajuste, e o ajuste entra em "Mudanças". As automáticas só com o ok do advogado responsável.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Escreva URGENTE" num canal que ninguém lê à noite | A pessoa acha que alguém viu e espera | Fora do horário com o caminho real e os números de emergência |
| Resposta pronta para prisão com orientação | Orientação pela metade numa hora crítica | Modelo 11, só o encaminhamento |
| Valor de consulta para idosa sem renda | Cobrança antes de alguém ouvir | Nenhum modelo para vulnerabilidade forte |
| `[CONFERIR]` no texto que vai ao contato | Mensagem que nunca fica pronta, ou sai com marcação | Pendência no "Antes de enviar" |
| Horário da agenda inventado no rascunho | A pessoa reserva um horário ocupado | `{DIA E HORA}` para quem envia, olhando a agenda |
| Mensagem de cliente misturada com a de contato | Cliente recebe convite para consulta | Biblioteca só comercial; a do cliente fica no motor-experiencia |
| Cada pessoa responde de um jeito | O contato percebe dois escritórios | Biblioteca única, com dono e chave fixa |
| Duas automáticas diferentes no mesmo canal | Ninguém sabe qual está valendo | Um `fora-do-horario` só, igual nas duas bibliotecas |
| "Consulta grátis" como chamariz | Problema de publicidade | Modelo 4 só para quem procurou, `[CONFERIR]` interno |

## 10. Próximo passo

- Biblioteca pronta: rode a `triar-contato` em modo treino com `../../docs/casos-ficticios.md` e veja se as respostas-base saem no tom.
- Contato que aceitou o convite: `agenda-da-consulta` (se instalada); sem ela, a pessoa marca pela `como_agenda`.
- Retorno a quem não agendou: `follow-up` (se instalada).
- Rascunhos todo dia sem ninguém pedir: `rotina-comercial` e `/motor-comercial:ciclo`.
- Primeira mensagem automática de verdade no canal: `assistente-de-primeira-resposta` (se instalada), depois de a biblioteca rodar algumas semanas.

## Referências desta habilidade

- `assets/modelos-de-mensagem.md`: os dezessete modelos crus, com chave, "Antes de enviar", campos do envio, variações e "nunca usar quando", e o cabeçalho da biblioteca nova. Leia no passo 3 e no modo no ciclo.
- `references/tom-e-conferencia.md`: como cada campo da ficha vira escolha no texto, o mesmo modelo em três tons, a conferência de treze itens e a convivência com a biblioteca do cliente. Leia nos passos 1, 2 e 4.
