---
name: boas-vindas-do-cliente
description: >
  Faz a entrada do cliente que acabou de fechar: lê a passagem do comercial (se houver), escreve
  as boas-vindas no tom da ficha, o combinado de comunicação (canal, horário, prazo de
  resposta, como e quando terá notícia, urgência, quando vira ligação), quem cuida, os próximos
  passos e os documentos pendentes; cria a pasta do cliente com a abertura e o histórico e a
  linha da carteira, se a passagem não criou. Roda a pedido ou no ciclo do agente. Use quando o
  advogado disser "fechou, e agora?", "o contrato foi assinado", "manda as boas-vindas",
  "cliente novo entrou", "abre a ficha do cliente", "o que falta ele mandar", "refaz a entrada
  desse cliente antigo". Não use antes de o contrato estar assinado (use proposta-de-honorarios
  do motor-comercial, se instalado) nem para responder dúvida de andamento (use
  status-para-o-cliente).
---

# Boas-vindas do cliente

> O cliente que assina na sexta e só ouve falar do escritório quando pergunta, duas semanas depois, começa a relação desconfiado. A entrada combina no primeiro dia como ele vai saber do caso, quem cuida e o que falta, e deixa isso escrito para a equipe e para o ciclo.

Regras comuns do plugin: `../../docs/regras.md`. A carteira: `../../docs/carteira.md`. Fichas: `../../docs/ficha-da-experiencia.md`. O agente e a fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`.

Sexta, 17h: o cliente assina o contrato e vai embora. Segunda, a advogada está em audiência e a secretária não sabe que ele fechou. Quarta, ele manda: "Vocês já entraram com o processo? Preciso mandar alguma coisa?". Ninguém combinou nada, e a primeira impressão depois de pagar é de silêncio. Dez minutos no dia da assinatura evitam isso.

**Regras fixas desta habilidade:**
1. Só depois de o contrato estar assinado. Quem confirma é o advogado ou a passagem do comercial; a habilidade não dá ninguém por fechado.
2. O combinado de comunicação só promete o que o escritório cumpre hoje. Régua que não existe fica `[A DEFINIR]` na abertura e não vai na mensagem.
3. Nada de estratégia, chance ou prazo de decisão. Próximo passo é o que o escritório faz e quando, nunca quando o juiz ou o INSS decide.
4. Documento se pede com o que é, onde conseguir e como mandar. Senha, código e login nunca se pedem.
5. A abertura e a carteira guardam o mínimo. Telefone, documento, endereço e número do processo ficam no sistema do escritório.

## 1. Quando usar

**Use quando:**
- O contrato foi assinado e o cliente precisa ser recebido.
- A `passagem-para-o-caso` do motor-comercial (se instalado) gravou a passagem e o cliente ainda não tem abertura.
- A `rotina-da-experiencia` ou o agente de suporte apontou "passagem sem boas-vindas" (modo no ciclo).
- O advogado quer refazer a entrada de um cliente antigo que nunca recebeu o combinado (por exemplo, depois da importação da carteira).

**Não use quando:**
- A proposta foi enviada e o cliente ainda não assinou: use `proposta-de-honorarios` do motor-comercial (se instalado). Sem ele, o advogado fecha e volta aqui depois de assinado.
- O cliente pergunta do processo: use `status-para-o-cliente`.
- O pedido é só a lista de documentos de um tipo de caso: use `checklist-de-documentos` (se instalada).
- O pedido é a régua do tipo de caso: use `jornada-do-cliente`. A boas-vindas só repete a régua ao cliente.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` se existir, e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`).
2. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "Como vocês tratam o cliente?" e, depois, "Qual é o canal oficial com o cliente e o horário de atendimento?".
3. **Leia a passagem** (`escritorio/07-operacao/comercial/passagens/<codigo>.md`), se existir: o que foi prometido, combinado e pago, documentos pendentes e quem cuida saem dali. Sem passagem, procure no comercial a proposta, o contrato e a ata da consulta (`escritorio/07-operacao/comercial/propostas/`, `contratos/`, `consultas/`).
4. **Leia a base de relacionamento:** a jornada do tipo de caso (`escritorio/04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md`), que define a linha "notícias do caso", e a biblioteca (`biblioteca-de-mensagens.md`, na mesma pasta), com as chaves da seção 5.
5. **Leia a carteira** (`escritorio/07-operacao/experiencia/carteira.csv`): a linha do cliente já existe se a passagem criou.
6. **Dados.** Em conta pessoal, só caso fictício ou anonimizado. Se colarem CPF, endereço ou telefone, avise, não repita e siga sem eles.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tratamento`, `canais`, `horario_de_atendimento` · X: `quem_cuida_dos_casos`, `primeira_resposta_cliente_ativo`.
- **Melhora:** X: `resumo_mensal`, `maximo_sem_noticia`, `como_o_cliente_manda`.

O combinado de comunicação (seção 4) também usa, se preenchidos, outros campos das duas fichas. Campo que falta e a mensagem pede: pergunte aquele campo, uma vez, e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido, direto | O advogado manda tudo ("fechou o C-2026-0002, trabalhista, eu cuido, faltam CTPS e TRCT") | O que ele mandou, a passagem e a pasta | Mensagens, abertura, histórico e linha da carteira, no chat, para aprovar |
| A pedido, entrevista | O advogado diz só "fechou" | O código ou o nome curto | As perguntas do passo 3, uma por vez, e a mesma saída |
| No ciclo | O agente de suporte achou passagem sem boas-vindas | A passagem e as fichas | Rascunho na fila e abertura em rascunho, sem mostrar nada |
| Cliente antigo | Cliente que nunca recebeu o combinado | A linha da carteira | Só o combinado e os próximos passos (chave `boas-vindas-caso-novo` ou `boas-vindas-combinado`) |
| Adaptar | Chamado pela `adaptar-experiencia` | `nicho.md` e os modelos das chaves da seção 5 | Os modelos reescritos para o nicho, com `[ALTERADO]` |

### Passo 1. Confirmar que fechou
- Há passagem do comercial: siga.
- Sem passagem: pergunte "O contrato já está assinado?". Sim: siga. Não: pare e aponte a `proposta-de-honorarios` ou a `contrato-de-honorarios` do motor-comercial (se instalado).
- O registro do comercial (`contatos.csv`) é do motor-comercial: esta habilidade não muda a etapa. Se a linha ainda não está `fechado`, avise quem cuida do comercial.

### Passo 2. Juntar o que já se sabe
Da passagem, da proposta, do contrato e da ata: área, tipo de caso, escopo, o que não inclui, o que foi prometido, quem cuida, documentos pendentes, primeiro ato combinado. Da jornada: a régua do tipo de caso. Mostre em cinco linhas o que achou e o que falta.

### Passo 3. Perguntar o que falta (uma por vez)
Só as perguntas cuja resposta não está na passagem:
1. "Quem cuida do caso? E quem fala com o cliente no dia a dia?"
2. "Qual é o primeiro passo do escritório, e até quando vocês fazem?"
3. "Como esse cliente vai saber do caso?" Com jornada do tipo de caso, mostre a régua dela e pergunte se vale. Sem jornada, ofereça só o que a ficha diz que o escritório cumpre; sem escolha, `[A DEFINIR]`.
4. "Falta algum documento? Até quando?"
5. "Tem algum cuidado com esse cliente? Idoso, alguém fala por ele, conflito em casa, prefere ligação?"

### Passo 4. Os documentos pendentes
- Com a `checklist-de-documentos` instalada, use-a para o tipo de caso: lista, onde conseguir e o controle em `clientes/<codigo>/documentos.md`.
- Sem ela, procure `escritorio/04-base/atendimento-e-triagem/checklist-documentos-<tipo-de-caso>.md`. Se não houver, monte a lista a partir da passagem e do passo 3, com `[A CONFIRMAR]` na abertura (não na mensagem) para cada documento que o advogado não citou.
- Nunca peça senha, código de acesso ou login. Extrato de sistema (gov.br, Meu INSS, FGTS): explique como o próprio cliente tira e manda o arquivo.

### Passo 5. Escrever as mensagens
Parta do modelo da biblioteca (chaves da seção 5) ou de `assets/mensagens-de-boas-vindas.md`. Caso simples: uma mensagem. Com documentos ou mais de um passo: três mensagens. Situação da tabela de variações (idoso, empresa, família com conflito, alguém fala pelo cliente): aplique a variação. Reescreva no tom da ficha e do nicho.

Confira antes de mostrar: nenhum prazo de decisão; nenhuma régua que o escritório não cumpre; nenhum termo técnico sem explicação; tratamento e assinatura da ficha; canal oficial correto; nenhuma marcação no texto do cliente (o que falta vai para a abertura, em "Em aberto").

### Passo 6. A abertura e o histórico
Preencha `assets/ficha-de-abertura.md` e grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/abertura.md`. Crie `clientes/<codigo>/historico.md` pelo modelo `assets/historico-modelo.md`, com a primeira linha (a entrada). O que não se sabe fica `[A CONFIRMAR]` ou `[A DEFINIR]` na abertura, em "Em aberto".

O histórico tem dois tipos de linha, e esta habilidade explica os dois a quem vai usar a pasta:
- **Contato:** o que foi dito ao cliente ou pelo cliente. As boas-vindas são a primeira, e contam como contato que informou o caso (zeram o "sem notícia").
- **Trabalho do escritório** (canal `trabalho-do-escritorio`): o que o escritório fez pelo caso sem falar com o cliente (conferiu os documentos, calculou as verbas, protocolou a ação, pediu cópia ao INSS, cumpriu um prazo). Não conta como contato e não muda o `ultimo_contato`. É dali que a `pagina-do-caso` e o `resumo-mensal-do-caso` tiram o "o que o escritório fez". Se na entrada o escritório já fez algo (conferiu os documentos na reunião, por exemplo), registre já como trabalho do escritório.

Diga, na entrega: "Cada vez que alguém fizer algo pelo caso, mesmo sem falar com o cliente, registre uma linha de trabalho do escritório no histórico, no dia."

### Passo 7. A linha da carteira
Se a passagem já criou a linha, proponha só a atualização. Se não, proponha a linha nova (formato em `../../docs/carteira.md`):
- `fase`: `entrada` (ou `documentos`, se há documento pendente)
- `ultimo_contato`: o dia em que as boas-vindas forem enviadas · `ultimo_contato_tipo`: `mensagem` (ou `ligacao`)
- `proximo_contato` e `motivo_proximo_contato`: pela jornada ou pela ficha (`documento`, `compromisso` ou `maximo-sem-noticia`); enquanto as boas-vindas não forem enviadas, `boas-vindas`
- `documentos_pendentes`: quantos · `humor`: o que o advogado disse no passo 3, ou `a-confirmar`
- `resumo_mensal`: `sim` se a ficha faz resumo e o cliente não recusou · `pagina_do_caso`: pela ficha · `pediu_para_nao_receber`: `nao`
- `reclamacao_aberta`: `nao` · `atualizado_em`: hoje

### Passo 8. Mostrar e gravar
Mostre as mensagens (com quem lê e a sigla), a abertura e a linha da carteira. Grave com o ok. Diga quem envia e quando (hoje, se possível). Depois do envio, a linha do histórico e o `ultimo_contato` ficam com a data real.

### Passo 9. Aprender
Pergunte: "Você mudaria alguma coisa na entrada desse cliente?". Cada correção vira uma regra curta ("Boas-vindas de previdenciário com idoso sempre por ligação antes"; "Não citar o prazo do primeiro ato na mensagem, só na abertura") e, com o ok, entra nos aprendizados (`../../docs/aprender-com-o-uso.md`). Modelo novo aprovado entra na biblioteca, na chave dele. Régua definida agora vai para a ficha ou para a jornada do tipo de caso.

### No ciclo (chamada pelo agente de suporte)
1. Leia a passagem, as fichas, a jornada e a biblioteca. Não pergunte nada.
2. Monte as mensagens como no passo 5. O que faltou vira `[A CONFIRMAR]` na abertura, nunca no texto.
3. Grave na fila: `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-boas-vindas.md`, no formato de `../../docs/agentes-e-fila.md` (`tipo: boas-vindas`, `motivo: passagem de AAAA-MM-DD sem boas-vindas`, `prazo`: hoje). Três mensagens vão no mesmo arquivo, numeradas.
4. Grave a abertura como `clientes/<codigo>/abertura-rascunho.md`. Ela vira `abertura.md` quando a pessoa aprovar a fila. Enquanto for rascunho, a rotina continua apontando a passagem.
5. Linha nova da carteira: não grave. Ponha em PARA DECIDIR no resumo do dia, com a linha proposta.
6. Família com sinal de conflito, cliente idoso sem canal definido, alguém falando pelo cliente sem autorização registrada: não rascunhe a mensagem; vai para PESSOA AGORA ou PARA DECIDIR.

### Modo adaptar (chamado pela `adaptar-experiencia`)
1. Leia o `nicho.md` (como o cliente fala, cuidados, canal preferido) e os modelos das chaves da seção 5 na biblioteca, ou os de `assets/mensagens-de-boas-vindas.md`.
2. Reescreva no jeito do nicho: palavras do cliente, tamanho (público com pouca leitura pede mensagem mais curta e a ligação antes), canal (família com conflito: confirmar canal seguro), o que o cliente do nicho mais teme na entrada.
3. Revise a tabela de variações com os cuidados do nicho e acrescente a variação que faltar.
4. Marque cada mudança `[ALTERADO]`, mostre, grave com o ok, cada modelo na chave dele. **Aprender**, como no passo 9.

## 4. O combinado de comunicação

A mensagem do combinado e a abertura dizem a mesma coisa. Cada linha sai de um campo; campo vazio é pergunta, nunca invenção.

| Item | De onde vem | Exemplo (Escritório Modelo) |
|---|---|---|
| Canal oficial | E: `canais` | este WhatsApp, e o telefone oficial escrito por extenso (de `canais`; sem ele, `{TELEFONE OFICIAL}` para quem envia preencher) |
| Horário | E: `horario_de_atendimento` | dias úteis, das 9h às 18h |
| Prazo de resposta | X: `primeira_resposta_cliente_ativo` | até 4 horas úteis |
| Notícias do caso | jornada do tipo de caso; X: `avisa_movimentacao_relevante`, `maximo_sem_noticia`, `resumo_mensal` | aviso a cada novidade importante e resumo em PDF no dia 5 |
| Página do caso | X: `pagina_do_caso` | (o Escritório Modelo manda o resumo em PDF) |
| Urgência | E: `o_que_e_urgente`, `urgencia_vai_para` | audiência ou perícia em até 3 dias: escrever aqui e ligar |
| Ligação e áudio | E: `audio` · X: `nunca_por_mensagem` | assunto que pede conversa, a gente liga |
| Quem cuida | X: `quem_cuida_dos_casos` · E: `quem_atende`, `substituto` | a advogada; agenda e documentos com a secretária |
| Quem escreve | E: `quem_atende` | a secretária; o primeiro nome de quem envia fica `{SEU NOME}` |
| Como mandar documento | X: `como_o_cliente_manda` | foto pelo WhatsApp oficial |

## 5. As chaves da biblioteca (desta habilidade)

A biblioteca do cliente fica em `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`. Cada modelo é uma seção com título (`### <título>`) e, logo abaixo, a linha **Chave:** com a chave entre crases, como nos modelos de `assets/mensagens-de-boas-vindas.md`. Esta habilidade é dona das chaves abaixo: só ela cria ou reescreve esses modelos, e nunca mexe na chave de outra habilidade.

| Chave | Modelo | Sigla |
|---|---|---|
| `boas-vindas-cliente` | Boas-vindas em uma mensagem (no `inicio-automacao`, é o modelo 1) | S depois de aprovado |
| `boas-vindas-quem-cuida` | Parte 1 de 3: boas-vindas e quem cuida | S depois de aprovado |
| `boas-vindas-combinado` | Parte 2 de 3: como a gente se comunica | S depois de aprovado |
| `boas-vindas-proximos-passos` | Parte 3 de 3: próximos passos e documentos | A |
| `boas-vindas-caso-novo` | Cliente que já era cliente, caso novo | A |

Se a biblioteca não tem a chave, use o modelo cru de `assets/mensagens-de-boas-vindas.md` e, com o ok, grave o modelo no tom do escritório.

## 6. Os primeiros 30 dias

Exemplo de cadência de entrada, para o escritório decidir (ou para a jornada do tipo de caso, que vale antes deste exemplo).

| Quando | O que acontece | Quem | Habilidade |
|---|---|---|---|
| Dia da assinatura | Boas-vindas, combinado e próximos passos | quem atende | esta |
| Até a data combinada | Documentos chegam; cobrança gentil se não chegarem | quem acompanha | `checklist-de-documentos` (se instalada) |
| Primeiro ato do escritório | Mensagem de andamento: o que foi feito e o que vem | quem acompanha, advogado lê | `status-para-o-cliente` |
| Primeiro resumo | O cliente recebe o primeiro resumo, mesmo sem novidade | quem acompanha | `resumo-mensal-do-caso` |
| Dia 30 | O cliente perguntou "e aí?" alguma vez? Se sim, o combinado não ficou claro | advogado | (aprendizado) |

Cada data entra na carteira como `proximo_contato`, e a `rotina-da-experiencia` cobra.

## 7. Exemplo resolvido (Escritório Modelo)

Paulo, C-2026-0002 (casos fictícios), trabalhista, verbas rescisórias, na entrada do caso. Passagem do comercial de 2026-02-02 (segunda): a advogada cuida, a secretária fala no dia a dia, primeiro passo preparar a ação até sexta, 13/02, faltam carteira de trabalho, termo de rescisão e extrato do FGTS. Ficha: resposta em até 4 horas úteis, resumo em PDF no dia 5.

Parte 3 (`boas-vindas-proximos-passos`), no tom "próximo, claro, sem pressa":
```
Próximos passos:

1. A advogada prepara a ação com os seus pedidos até sexta, 13/02.
2. Depois que a ação for registrada, eu te aviso e explico o que vem.

O que eu preciso de você:
1. Carteira de trabalho: as páginas da foto, do contrato com a empresa e das anotações. Pode ser a carteira digital, pelo aplicativo.
2. Termo de rescisão: o papel que a empresa entregou na saída, se entregou.
3. Extrato do FGTS: você tira no aplicativo do FGTS ou numa agência da Caixa.

Pode mandar por aqui mesmo, em foto com boa luz ou em PDF. Consegue até sexta, 06/02? Se tiver dificuldade com algum, me fala que a gente resolve junto.

Equipe Escritório Modelo
```

Linha da carteira (a passagem não tinha criado):
```
C-2026-0002,Paulo,trabalhista,verbas rescisórias,advogada,2026-02-02,documentos,2026-02-02,mensagem,2026-02-06,documento,,,3,a-confirmar,nao,sim,pdf,,nao,,2026-02-02
```

Histórico, as primeiras linhas (a de trabalho do escritório entra no dia em que a ação for protocolada, e não muda o `ultimo_contato`):
```
| Data e hora | Canal | Quem falou | O que foi dito |
|---|---|---|---|
| 2026-02-02 17h10 | whatsapp | secretária | boas-vindas, combinado e pedido de 3 documentos até 06/02 |
| 2026-02-13 16h00 | trabalho-do-escritorio | advogada | protocolou a ação com os pedidos das verbas da rescisão |
```

## 8. Formato da saída

```
BOAS-VINDAS · [CÓDIGO] · [NOME CURTO] · [TIPO DE CASO]
Quem lê antes de enviar: [função] · Sigla: [S | A] · Quem envia e quando: [função, hoje]
Mensagens: [1 a 3, numeradas, prontas para copiar, sem marcação]
Abertura: clientes/[CÓDIGO]/abertura.md (prévia)
Histórico: [primeira linha proposta, na tabela de assets/historico-modelo.md]
Carteira: [linha nova ou campos atualizados]
Em aberto: [o que ficou A CONFIRMAR ou A DEFINIR, só na abertura]
```

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mensagens de boas-vindas (a pedido) | No chat, para copiar e enviar |
| Mensagens de boas-vindas (no ciclo) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-boas-vindas.md` |
| Abertura do cliente | `escritorio/07-operacao/experiencia/clientes/<codigo>/abertura.md` (no ciclo, `abertura-rascunho.md`) |
| Histórico do cliente | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Linha da carteira | `escritorio/07-operacao/experiencia/carteira.csv` (a pedido, com o ok; no ciclo, proposta em PARA DECIDIR) |
| Modelo aprovado | `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, na chave da seção 5 |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-experiencia.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

A pasta `clientes/` fica em `07-operacao/`, fora do Projeto no Claude, porque tem dado de cliente. Se ela não existir, crie e avise. Sem pasta aberta: mensagens, abertura, histórico e linha da carteira vêm no chat, com o caminho onde ficariam.

## 10. Solo e equipe

**Solo:** o titular faz a entrada no dia da assinatura, de preferência antes de o cliente sair da reunião: as mensagens podem ser enviadas ali, e as dúvidas resolvidas na hora. A abertura é o que permite lembrar, três meses depois, o que foi combinado.

**Equipe:** o advogado confirma o fechamento e responde as perguntas 1 a 3; a secretária envia, acompanha os documentos e aparece como `responsavel` na carteira. A abertura é a passagem de bastão: quem não estava na consulta lê e sabe por onde começar.

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Cliente fecha e ninguém fala com ele | Primeira impressão de abandono | Entrada no dia; no ciclo, a rotina aponta a passagem |
| Prometer resumo mensal que ninguém manda | Promessa quebrada logo no começo | Regra fixa 2 |
| "Em seis meses sai a sentença" | Prazo de decisão prometido por escrito | Regra fixa 3 e a conferência do passo 5 |
| Pedir "o documento do INSS" sem explicar | O cliente manda a coisa errada ou nada | Documento com o que é, onde conseguir e como mandar |
| Pedir a senha do gov.br | Risco de dado e de responsabilidade | Regra fixa 4 |
| `[A CONFIRMAR]` dentro da mensagem | Mensagem nunca fica pronta, ou sai com a marcação | Pendência vai para a abertura, em "Em aberto" |
| Cliente fora da carteira | O ciclo nunca avisa que ele está sem notícia | Passo 7 cria a linha |
| Mensagem detalhada no celular que a outra parte lê | Exposição em caso de família | Variação de canal seguro |

## 12. Próximo passo

- Documentos pendentes: `checklist-de-documentos` (se instalada). Sem ela, a abertura guarda a lista e a data, e a rotina cobra pela carteira.
- Régua do tipo de caso ainda não desenhada: `jornada-do-cliente`.
- Primeira movimentação: `status-para-o-cliente`.
- Primeiro resumo do mês: `resumo-mensal-do-caso`.
- O ciclo diário: `rotina-da-experiencia`.

## Referências desta habilidade

- `assets/mensagens-de-boas-vindas.md`: os modelos crus das chaves da seção 5 e as variações por situação. Use no passo 5.
- `assets/ficha-de-abertura.md`: o modelo da abertura do cliente, com o que nunca entra nela. Use no passo 6.
- `assets/historico-modelo.md`: o modelo do histórico do cliente, com os dois tipos de linha (contato e trabalho do escritório). Use no passo 6.
