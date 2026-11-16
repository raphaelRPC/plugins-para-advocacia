---
name: agenda-da-consulta
description: >
  Cuida da agenda da consulta inicial de quem ainda não é cliente: oferece horários pelos dias
  fixos e pelo jeito de agendar da ficha, marca, manda a confirmação, prepara o lembrete da
  véspera (um ou o lote do dia), remarca seguindo a regra do funil e registra a falta só com a
  pessoa, armando a régua de quem faltou. Com conector de agenda, só lê os horários livres e
  sugere; quem cria ou muda o compromisso é uma pessoa. As mensagens saem da biblioteca
  comercial. Roda a pedido, no ciclo do agente e no modo adaptar. Use quando o advogado disser
  "marca a consulta dela", "que horários eu ofereço?", "manda a confirmação", "lembretes de
  amanhã", "ele pediu para remarcar", "ela não veio". Não use para preparar a conversa da
  consulta (use roteiro-da-consulta) nem para audiência ou perícia de cliente (use as habilidades
  do motor-experiencia).
---

# Agenda da consulta

> Entre o "quero marcar" e a consulta acontecer, há quatro mensagens e uma linha do registro que precisam estar certas: os horários, a confirmação, o lembrete e, às vezes, a remarcação.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-comercial-modelo.md` e a tabela de campos em `../../docs/ficha-comercial.md`. Funil (etapas `consulta-agendada` e `nao-compareceu`; regra 6, "Remarcação"): `../../docs/funil.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quarta, 18h40. Bruno pede para remarcar a consulta de amanhã. Na quinta cedo, a secretária oferece "amanhã às 10h", que já estava ocupado, e esquece de mudar a data no registro. Na sexta, a rotina mostra Bruno como "consulta que passou, aconteceu ou faltou?". Três horários conferidos e uma linha certa no registro evitam as duas coisas.

**Regras fixas desta habilidade:**
1. Horário só sai depois de conferido na agenda. A habilidade sugere; quem confirma o horário e cria o compromisso é uma pessoa.
2. Com conector de agenda, só leitura: nunca cria, muda, cancela nem responde convite.
3. Falta (`nao-compareceu`) só se registra com a pessoa, nunca no ciclo.
4. Remarcação segue a regra 6 do funil ("Remarcação") e a `remarcacao` da ficha. Remarcar audiência ou perícia não é daqui.
5. Quem pediu para parar ou tem o `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:` (marcador de pessoa, `funil.md`, regra 4) não recebe lembrete nem oferta de horário automática.
6. Horário que ninguém conferiu na agenda vai como `{DIA E HORA}` (ou `{OPÇÃO 1}`, `{OPÇÃO 2}`), entre chaves, para quem confirma preencher. As sugestões ficam no cabeçalho interno ou no `motivo` do rascunho, nunca como horário certo no texto.

## 1. Quando usar

**Use quando:**
- O contato aceitou o convite e é preciso oferecer horários e marcar.
- A consulta foi marcada e falta a confirmação.
- É véspera e há lembretes para mandar (um ou o lote).
- O contato ou o escritório precisa remarcar.
- A pessoa não veio e é preciso registrar a falta e retomar.
- O `agente-comercial` pediu confirmações, lembretes e opções de horário (modo no ciclo).
- A `adaptar-comercial` pediu as mensagens da agenda no jeito do nicho (modo adaptar).

**Não use quando:**
- O pedido é preparar a consulta (briefing, perguntas, documentos): `roteiro-da-consulta` (se instalada; sem ela, a confirmação leva o "o que trazer" curto da ficha).
- A consulta aconteceu e o pedido é a ata: `ata-da-consulta` (se instalada).
- O pedido é retomar quem faltou depois do primeiro retorno: `follow-up` (se instalada; sem ela, a variação "depois da falta" da remarcação, uma vez).
- O compromisso é audiência ou perícia de cliente: habilidades do motor-experiencia (se instalado).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-comercial.md`), `nicho.md` se existir e `aprendizados-comercial.md`.
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Como a pessoa marca a consulta com vocês: link, a secretária marca, horários fixos?" e depois "Quanto tempo dura e é presencial, online ou os dois?".
3. **Leia a biblioteca comercial** (`escritorio/04-base/comercial/biblioteca-comercial.md`): chaves `confirmacao-de-consulta`, `lembrete-de-consulta`, `remarcacao`. Sem ela, use `assets/mensagens-da-agenda.md`, no tom da ficha, e ofereça guardar pela `mensagens-comerciais` (se instalada).
4. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`). Contato sem linha: crie pela `triar-contato` (se instalada) ou proponha a linha mínima de `../../docs/funil.md`.
5. **Agenda.** Veja `agenda` e `conectores_no_claude` na ficha do escritório. Com conector de agenda (conferir na configuração da conta), leia os horários ocupados. Sem conector, peça à pessoa: "Quais destes horários estão livres na agenda?".

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `horario_de_atendimento` · C: `como_agenda`, `formato`, `duracao` |
| Melhora | E: `dias_e_horarios_fixos`, `agenda` · C: `confirmacao_e_lembrete`, `remarcacao` |

A confirmação usa também, se a ficha tiver: `quem_faz_a_consulta`, `valor_da_consulta` e `informa_valor_da_consulta_por_mensagem` (C), `assinatura_das_mensagens` e `tratamento` (E). Campo que falta: pergunte uma vez; sem resposta, a pendência vai para o "Antes de enviar" da mensagem, nunca para o texto do contato.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Oferecer horários | "que horários eu ofereço?" | Três opções conferidas e a mensagem com elas (ou com o link) |
| Marcar | O contato escolheu | A linha do registro e a confirmação |
| Lembrar | Véspera, um ou o lote | Os lembretes, um por consulta |
| Remarcar | Contato ou escritório pede | A linha da regra 6 do funil e as opções |
| Registrar falta | A pessoa não veio | A linha `nao-compareceu`, a régua e, se couber, a mensagem depois da falta |
| No ciclo | O agente chama | Rascunhos na fila. Não mostra nada |
| Adaptar | A `adaptar-comercial` chama | As mensagens da agenda no jeito do nicho |

Pedido direto ("marca a Marta terça às 10h e manda a confirmação"): faça direto e pergunte só o que faltar.

### Passo 1. Achar o contato
Pelo código ou nome curto no `contatos.csv`. Confira: `pediu_para_parar` (se `sim`, nenhuma mensagem automática; diga e pare), o `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:` (uma pessoa cuida primeiro: diga e pare) e a etapa atual.

### Passo 2. Oferecer horários
Siga a seção 4.1. Mostre as três opções com o dia da semana e a data, e a mensagem `remarcacao` (variação "quando o contato pede") ou a variação com link. Pergunte: "Esses horários estão livres?" quando não há conector.

### Passo 3. Marcar
Quando o contato escolher e a pessoa confirmar na agenda:
1. Proponha a linha do registro pela seção 4.2 e grave com o ok.
2. Monte a `confirmacao-de-consulta` com dia, hora, onde, com quem, duração e o "o que trazer" curto (do `roteiro-da-consulta`, se instalada, ou da ficha). Dia e hora entram escritos quando a pessoa confirmou nesta conversa que o horário está na agenda; senão, ficam `{DIA E HORA}` para quem confirma, e o horário sugerido vai para o "Antes de enviar". Link de videochamada: `{LINK DA VIDEOCHAMADA}`, que quem envia cola.
3. Lembre: "O compromisso na agenda é com você. Quer que eu deixe o texto do convite pronto para colar?".

### Passo 4. Lembrar
1. Um: o lembrete da consulta pedida. Lote: as linhas `consulta-agendada` com data até o próximo dia útil (a `rotina-comercial`, se instalada, lista; sem ela, filtre o registro).
2. Para cada uma, o `lembrete-de-consulta` da véspera, no horário de `confirmacao_e_lembrete`. Online: também o do dia, com o link.
3. Fora do lote: quem pediu para parar (a pessoa decide como avisar) e quem já tem "remarcar" no próximo passo.

### Passo 5. Remarcar
1. Pedido do contato: aplique a regra 6 do funil ("Remarcação") já (seção 4.2), mesmo antes da data nova. Pedido do escritório: o mesmo, com a variação "quando o escritório precisa remarcar".
2. Confira a `remarcacao` da ficha (por exemplo, "uma vez sem custo"). Se o pedido passa do que a ficha permite, não ofereça: vai para a pessoa decidir.
3. Ofereça horários (passo 2). Quando o novo for escolhido, marque (passo 3) com "(remarcada)" no próximo passo.

### Passo 6. Registrar a falta
Só com a pessoa dizendo que o contato não veio. Pergunte: "Ele avisou antes, ou simplesmente não apareceu?". Proponha a linha `nao-compareceu` com a régua de quem faltou (seção 4.2) e grave com o ok. Mensagem: a primeira da régua de "faltou à consulta" pela `follow-up` (se instalada); sem ela, a variação "depois da falta" da `remarcacao`, se a ficha permite remarcar. Quem pediu para parar: só o registro.

### Passo 7. Aprender
Pergunte: "Alguma coisa da agenda você faria diferente?". Correção vira regra curta ("Lembrete de consulta presencial sempre com o ponto de referência do prédio") e, com o ok, entra em `aprendizados-comercial.md` (`../../docs/aprender-com-o-uso.md`). Regra que é política (horário do lembrete, quantas remarcações) vai para a ficha comercial, com linha no histórico.

### Modo no ciclo
1. O agente chama. Não pergunte nada e não mostre nada.
2. Leia o registro e faça só três coisas:
   - lembrete da véspera para cada `consulta-agendada` com data até o próximo dia útil;
   - opções de horário para cada linha com `proximo_passo` "remarcar consulta": no texto, `{OPÇÃO 1}`, `{OPÇÃO 2}` e `{OPÇÃO 3}`; no `motivo`, os três candidatos da seção 4.1 e "conferir na agenda e preencher antes de enviar";
   - a lista "para decidir": consultas com data passada ainda em `consulta-agendada` (aconteceu ou faltou?).
3. Cada mensagem vira um arquivo em `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md`, no formato de `agentes-e-fila.md`, com `status: pendente`, `tipo: <chave>`, `revisor: pendente` e `prazo` (lembrete: o horário de `confirmacao_e_lembrete` da véspera; remarcação: o prazo de resposta da ficha). Treino em `escritorio/07-operacao/_treino/comercial/fila/`.
4. Não mude etapa: nada de `consulta-agendada`, `nao-compareceu` ou data nova no ciclo; no registro, só as colunas que `funil.md` permite ao agente (regra 11). Nada para quem pediu para parar ou tem o `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:`: esses vão para "PESSOA AGORA" ou "PARA DECIDIR" ("C-2026-0007: consulta amanhã; a advogada confirma por ligação").
5. **Saída de PESSOA AGORA.** Depois que a pessoa falou com o contato, o comando `fila` pergunta "Já falou? O que ficou combinado?" e grava a hora em `primeira_resposta` (se vazia) e o combinado no lugar do `proximo_passo` que começa com `pessoa agora:` ou `pessoa liga:` (por exemplo, `consulta 2026-03-12 10:00 com advogada`), com a data (`agentes-e-fila.md`). A partir daí, o lembrete volta a sair no ciclo.
6. Devolva ao agente: quantos lembretes, quantas remarcações, a lista "para decidir".

### Modo adaptar
1. Leia `nicho.md` (quem é o cliente, canal preferido, cuidados) e as três mensagens da agenda na biblioteca comercial.
2. Proponha o que muda para o nicho: o lembrete por ligação para público idoso ou com pouca leitura, o "o que trazer" típico, o ponto de referência para quem vem de longe, o horário do lembrete. Marque `[ALTERADO]` em cada trecho.
3. Com o ok, grave no mesmo número e chave da biblioteca comercial, sem as marcas, com linha em "Mudanças" ("agenda adaptada ao nicho [NOME]"). O que é política (horário do lembrete) vai para `confirmacao_e_lembrete` da ficha comercial.

## 4. Regras da agenda

### 4.1 De onde saem os horários

| Situação | O que a habilidade faz |
|---|---|
| `como_agenda` é um link que o contato usa | Manda o link (variação com link). Não oferece horário |
| Com conector de agenda | Lê os compromissos dos próximos dias úteis, dentro de `dias_e_horarios_fixos` e do `horario_de_atendimento`, e sugere três horários livres com a `duracao` da consulta e uma folga entre eles. Só sugere |
| Sem conector | Monta três candidatos pelos `dias_e_horarios_fixos` (ou, sem eles, pelo `horario_de_atendimento`) e pede à pessoa para conferir cada um na agenda antes de enviar |
| Consulta com prioridade (urgência alta da triagem) | O primeiro horário livre vem primeiro, de preferência em até dois dias úteis |
| `formato: os dois` | Cada opção diz se é presencial ou online, ou a mensagem pergunta qual a pessoa prefere |

Nunca invente horário livre. Sem agenda e sem resposta da pessoa, as opções vão entre chaves (`{OPÇÃO 1}`, `{DIA E HORA}`) para quem envia preencher depois de conferir, e os candidatos ficam no cabeçalho interno.

### 4.2 O que muda no registro

| Ação | `etapa` | `proximo_passo` | `data_proximo_passo` | Quem grava |
|---|---|---|---|---|
| Marcar | `consulta-agendada` | `consulta AAAA-MM-DD HH:MM com [QUEM]` (substitui o "retorno N de N" da régua de quem não agendou) | a data da consulta | a pessoa, com o ok |
| Confirmou presença | não muda | acrescenta "(confirmada)" | não muda | a pessoa |
| Pediu para remarcar (regra 6) | `consulta-agendada` | `remarcar consulta (era AAAA-MM-DD)` | hoje | a pessoa; no ciclo, só se a linha já estiver assim |
| Remarcou | `consulta-agendada` | `consulta AAAA-MM-DD HH:MM com [QUEM] (remarcada)` | a data nova | a pessoa |
| Faltou | `nao-compareceu` | `retorno 1 de N (faltou)` (N = retornos da régua "faltou à consulta" do `follow_up`) | a data da falta mais o primeiro intervalo dessa régua, em dias corridos (0 é hoje) | só a pessoa |
| Remarcou depois da falta | `consulta-agendada` | `consulta AAAA-MM-DD HH:MM com [QUEM] (remarcada)` | a data nova | a pessoa |

Sempre `atualizado_em` com a data do dia. `primeira_resposta` não é desta habilidade: se estiver vazia e a pessoa já conversou com o contato, avise para preencher. `pediu_para_parar = sim` com falta: registre, sem régua.

### 4.3 Lembrete
- Horário: o de `confirmacao_e_lembrete` (ex.: véspera às 18h). Sem o campo, véspera dentro do horário de atendimento, e a pergunta vai para o fim.
- Véspera de segunda: o lembrete sai na sexta, dizendo "segunda-feira", nunca "amanhã".
- Online: o link vai no lembrete do dia, nunca antes da confirmação.

## 5. Exemplo resolvido (Escritório Modelo)

Ficha de exemplo: consultas de 40 minutos, online ou presencial, marcadas pela secretária; `dias_e_horarios_fixos` de exemplo: terças e quintas, às 10h e às 14h; lembrete na véspera às 18h; quem faltou pode remarcar uma vez sem custo. Sem conector de agenda.

**Bruno (C-2026-0008, mensagem 8, qua 18h40, remarcar a consulta de 2026-03-12).** Na hora da triagem, a linha já fica `consulta-agendada`, `remarcar consulta (era 2026-03-12)`, data de hoje. Na quinta cedo, a habilidade monta os candidatos e pede à secretária para conferir. Conferidos, a mensagem sai assim (no ciclo, sairia com `{OPÇÃO 1}` a `{OPÇÃO 3}` e os candidatos no `motivo`):
```
Sem problema, Bruno. Tenho estes horários:
* terça, 17/03, às 10h
* terça, 17/03, às 14h
* quinta, 19/03, às 10h
Qual fica melhor para você? Assim que você escolher, te mando a confirmação.
Equipe Escritório Modelo
```
Bruno escolhe terça às 14h. A linha vira `consulta 2026-03-17 14:00 com advogada (remarcada)`, data 2026-03-17, e sai a `confirmacao-de-consulta`. Na segunda, 16/03, às 18h, o lembrete da véspera vai para a fila.

**Marta (C-2026-0001, mensagem 1, seg 21h14, consulta com prioridade).** O primeiro horário livre vem primeiro: a variação prioridade do convite sai com `{DIA E HORA}`, e a habilidade sugere no cabeçalho "quinta, 12/03, às 14h" (a terça já estava cheia). A secretária confere, preenche e envia. Marcado, a linha vira `consulta 2026-03-12 14:00 com advogada` e o "retorno 1 de 3" da régua sai do próximo passo, porque ela agendou.

**Helena (C-2026-0007, mensagem 7, vulnerabilidade).** O `proximo_passo` começa com `pessoa liga:`. Nenhuma oferta de horário nem lembrete automático: a advogada liga e combina. Depois da ligação, o comando `fila` grava o combinado, e só então a consulta entra no lote de lembretes.

## 6. Formato da saída

```
AGENDA · [CÓDIGO] [NOME CURTO] · [AÇÃO]
Antes de enviar (interno): [horários a conferir na agenda; campos que faltam]
Mensagem (A, [função] lê antes de enviar), modelo [chave]:
"..."
Registro: [linha proposta do contatos.csv, ou "não muda"]
Agenda: [o que a pessoa precisa criar ou mudar no compromisso]
```

No lote de lembretes: uma tabela (código, nome curto, dia, hora, formato, situação) e depois as mensagens, numeradas.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mensagens a pedido | No chat, para copiar |
| Rascunhos do modo no ciclo | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-<chave>.md` |
| Linhas do registro | `escritorio/07-operacao/comercial/contatos.csv`, com o ok |
| Mensagens da agenda aprovadas ou adaptadas | `escritorio/04-base/comercial/biblioteca-comercial.md` |
| Treino | `escritorio/07-operacao/_treino/comercial/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Regra nova de lembrete ou remarcação | `escritorio/04-base/comum/ficha-comercial.md`, com linha no histórico |

O compromisso na agenda do escritório é sempre criado ou mudado por uma pessoa. Sem pasta aberta: as mensagens e as linhas do registro vêm no chat, prontas para colar.

## 8. Solo e equipe

**Solo:** o titular costuma ser também quem marca. Guarde horários fixos de consulta na ficha (`dias_e_horarios_fixos`) e ofereça só eles: a agenda para de ser negociada a cada contato. O lote de lembretes sai uma vez por dia, no fim da tarde.

**Equipe:** a secretária marca, confirma e lembra; o advogado só vê a agenda pronta. Com mais de um advogado, cada opção de horário diz com quem é. Quem marcou é quem grava a linha no registro, para não haver duas versões da mesma consulta.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Oferecer horário já ocupado | Duas pessoas no mesmo horário, ou um "desculpe, errei" logo no começo | Horário só depois de conferido; com conector, leitura dos ocupados |
| Remarcação sem mudar o registro | A rotina mostra a consulta antiga como "aconteceu ou faltou?" | Regra 6 do funil aplicada na hora do pedido |
| Horário sugerido pela IA enviado como certo | Contato aparece num horário ocupado | `{DIA E HORA}` entre chaves até alguém conferir |
| Remarcação tratada como urgência | O alto perde o sentido | Remarcar é sempre normal (`triar-contato`) |
| IA marcando falta sozinha | Contato que avisou e foi registrado como faltoso | `nao-compareceu` só com a pessoa |
| Conector que cria ou cancela compromisso | Agenda do escritório mudada sem ninguém saber | Só leitura e sugestão |
| Lembrete "amanhã" enviado na sexta para segunda | Contato aparece no sábado ou não aparece | Regra da véspera de segunda |
| Lembrete para quem pediu para parar | Incômodo e risco de reclamação | Fora do lote; a pessoa decide |

## 10. Próximo passo

- Consulta marcada: `roteiro-da-consulta` (se instalada) para o briefing; sem ela, o advogado lê a triagem antes.
- Consulta feita: `ata-da-consulta` (se instalada); sem ela, a pessoa muda a etapa para `consulta-feita`.
- Faltou e não respondeu: `follow-up` (se instalada), pela régua de quem faltou.
- Lembretes todo dia sem ninguém pedir: `rotina-comercial` e `/motor-comercial:ciclo`.

## Referências desta habilidade

- `assets/mensagens-da-agenda.md`: a confirmação, o lembrete, a remarcação (três variações) e a variação com link, com as mesmas chaves da biblioteca comercial. Leia no passo 2 de "Antes de começar" quando a biblioteca não tiver as chaves.
