---
name: follow-up
description: >
  Cuida da régua de retorno de quem procurou o escritório e parou no meio: não agendou depois
  do convite, faltou à consulta ou não respondeu a proposta. O script monta a lista do dia a
  partir do registro de contatos, com a régua em dias corridos da ficha comercial, e separa
  antes quem nunca recebe mensagem pronta: violência, criança, risco, prisão, vulnerabilidade,
  fora da área, urgência sem pessoa designada e quem pediu para parar. Escreve cada retorno no
  tom da ficha, fecha com um encerramento educado e só marca perdido com o ok do advogado. No
  ciclo, grava os rascunhos na fila. Use quando o advogado disser "quem eu preciso retomar
  hoje", "a pessoa sumiu depois da proposta", "faltou à consulta, mando o quê?", "monta nossa
  régua de follow-up", "ela não respondeu, insisto?". Não use para cobrar honorário atrasado
  nem para responder uma objeção que chegou (use objecoes-comerciais).
---

# Follow-up

> Quem procurou o escritório e parou no meio merece um lembrete educado, no tempo certo, e depois um ponto final gentil. Mais do que isso vira insistência. Menos é contato perdido por esquecimento.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-comercial.md`. Funil (regras 2, 3, 4 e 5: régua armada, dias corridos, marcador de pessoa e fora da régua): `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Fila: `../../docs/agentes-e-fila.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

Segunda de manhã. A lista de retornos tem a Renata, que perguntou do divórcio, e a Joana, que contou que o ex ameaçou sumir com as crianças. As duas estão com "retorno 1 de 3" vencido. Se a lista não separar, a Joana recebe um "oi, ainda quer marcar a consulta?".

**Regras fixas desta habilidade:**
1. Fora da régua, sempre (`funil.md`, regra 5): parada imediata, `proximo_passo` com `pessoa agora:` ou `pessoa liga:` (regra 4), caso sensível (violência, criança, risco, prisão, vulnerabilidade), área `fora-da-area`, urgência `alta` sem pessoa designada e `pediu_para_parar = sim`. Esses contatos vão para uma pessoa e nunca aparecem numa lista de mensagem pronta.
2. Follow-up só com quem procurou o escritório. Nada de abordar quem não escreveu.
3. A régua é a do campo `follow_up` da ficha comercial, em dias corridos, por situação. O último retorno é sempre o encerramento.
4. Nada de insistência, culpa ou gatilho: sem "última chance", sem "vagas acabando", sem "você sumiu", sem desconto para voltar.
5. `perdido` só com o ok do advogado. A habilidade sugere, a pessoa confirma. Nenhum retorno sai sem uma pessoa ler (A).

## 1. Quando usar

**Use quando:**
- É hora de saber quem recebe retorno hoje (lista do dia).
- Um contato parou depois do convite, faltou à consulta ou não respondeu a proposta.
- O escritório quer definir ou ajustar a régua.
- O `agente-comercial` ou a `rotina-comercial` chamou para a parte de retornos do dia (modo no ciclo).
- A `adaptar-comercial` (se instalada) pediu as mensagens de retorno no jeito do nicho (modo adaptar).

**Não use quando:**
- A pessoa respondeu com uma objeção ("achei caro", "vou pensar"): use `objecoes-comerciais` (se instalada). A régua fica pausada enquanto a conversa anda.
- É cliente com honorário atrasado: isso é cobrança, fora deste plugin.
- É cliente ativo esperando notícia do processo: use a `status-para-o-cliente` do motor-experiencia (se instalado).
- O contato está fora da régua (regra fixa 1): o advogado decide se e como retomar, sem modelo.

## 2. Antes de começar

1. **Leia as fichas:** `escritorio/04-base/comum/ficha-do-escritorio.md` e `escritorio/04-base/comum/ficha-comercial.md` (seção 4, Retorno e funil, e `remarcacao`).
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`) e os aprendizados (`escritorio/04-base/comum/aprendizados-comercial.md`), se existirem. Exceção da régua guardada nos aprendizados vale antes da régua padrão.
3. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`). É dele que sai a lista. Sem registro, peça a lista de quem está pendente (código ou primeiro nome, situação, data do último contato).
4. **Leia a biblioteca comercial** (`escritorio/04-base/comercial/biblioteca-comercial.md`), se existir. Mensagem de retorno que está lá, pela chave, vale antes da base desta habilidade.
5. **Para propostas:** leia a proposta em `escritorio/07-operacao/comercial/propostas/` para saber a validade.
6. **Conta de IA.** Em conta pessoal, só casos fictícios, gravados em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tratamento` · C: `follow_up`, `maximo_de_retornos`.
- **Melhora:** E: `tom_em_tres_palavras` · C: `motivos_de_perda_comuns`, `remarcacao`.

A assinatura, o horário de atendimento e os feriados (`feriados_e_recessos`, para a data do próximo retorno pular dia sem expediente) saem da ficha do escritório, como em toda habilidade. Sem `follow_up` ou `maximo_de_retornos`: mostre a régua de exemplo (seção 4) e pergunte "Quer usar esta régua, ajustar os dias ou o número de retornos?". Grave com o ok.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Montar a régua | Primeira vez, ou para ajustar | A régua de exemplo e a entrevista | Campos `follow_up` e `maximo_de_retornos` na ficha comercial |
| B. Lista do dia, a pedido | O advogado pede | O `contatos.csv` | A lista no chat, com a mensagem de cada retorno e as linhas do registro |
| C. Um contato | "A Renata sumiu, mando o quê?" | O contato e a situação | A mensagem do retorno certo e a linha do registro |
| D. Resposta chegou | A pessoa respondeu ao retorno | A resposta | O próximo passo e a régua pausada ou encerrada |
| E. No ciclo | O `agente-comercial` chama | O `contatos.csv` e a fila dos dias anteriores | Um rascunho por retorno na fila; nada no chat |
| F. Adaptar | A `adaptar-comercial` chama | O nicho e as mensagens atuais | Mensagens de retorno reescritas, com `[ALTERADO]`, gravadas só com o ok |

### A. Montar a régua

Mostre a régua de exemplo da seção 4 e pergunte, uma de cada vez:
1. "Depois de quantos dias corridos vocês querem o primeiro retorno para quem não agendou? E o segundo e o encerramento?"
2. "E para quem não respondeu a proposta?"
3. "Quem faltou à consulta: mensagem no mesmo dia ou no seguinte?"
4. "Quantos retornos no máximo, contando o de encerramento?"
5. "Tem algum tipo de contato que vocês não retomam nunca, além dos que a régua já tira?"

Explique em uma frase: "A régua conta em dias corridos, e o retorno que cai no fim de semana sai no próximo dia de atendimento." Grave em `follow_up` no formato da seção 4.3 e em `maximo_de_retornos`, mostrando a ficha alterada antes e registrando no histórico dela. Resposta à pergunta 5 que é uma situação nova com retorno (não um "nunca retomar"): siga a seção 4.3, "Situação nova".

### B. Lista do dia (a pedido)

**Passo 1. Rodar o script.** Com pasta aberta e execução de código, rode com o caminho da pasta desta habilidade (a que contém este SKILL.md) e o caminho do registro como argumentos:

```
python3 "<pasta desta habilidade>/scripts/lista_do_dia.py" "escritorio/07-operacao/comercial/contatos.csv"
```

O script acha sozinho a ficha comercial (`escritorio/04-base/comum/ficha-comercial.md`) e lê a régua do campo `follow_up` no formato da seção 4.3. Opções: `--data AAAA-MM-DD` para outro dia, `--ficha <caminho>` se a ficha estiver em outro lugar, `--regua "nao-agendou: 2, 7, 15 · proposta-sem-resposta: 2, 7, 15"` e `--maximo 3` para testar uma régua sem gravar, `--json` para o ciclo. Ele lê vírgula ou ponto e vírgula, com ou sem BOM, datas AAAA-MM-DD ou DD/MM/AAAA, e etapas em maiúsculas. Sai com erro e uma frase clara quando falta o arquivo, falta coluna ou o registro está vazio; nunca diz "nada a fazer" sem ter lido. Como pega tudo com data até hoje, o que venceu no sábado e no domingo aparece na segunda, com o atraso. A data do próximo retorno ("Depois do envio") que cai em sábado, domingo ou feriado passa para o próximo dia útil, como na `triar-contato` (seção 4.4), e a coluna diz quando isso aconteceu. Os feriados vêm do campo `feriados_e_recessos` da ficha do escritório (`escritorio/04-base/comum/ficha-do-escritorio.md`, achada sozinha, ou `--ficha-do-escritorio <caminho>`) ou de `--feriados "2026-04-21, 2026-06-04"`. Campo vazio ou `[A PREENCHER]`: só sábado e domingo passam, e o topo da lista avisa.

Sem execução de código, leia o `contatos.csv` e aplique os critérios da seção 4.4 na mesma ordem. Sem registro, use a lista que o advogado colar.

**Passo 2. Ler as quatro partes da saída.**
- **Para uma pessoa, fora da régua:** nenhuma mensagem. Mostre a lista ao advogado com o motivo de cada um. Se a linha tem retorno marcado, proponha tirar ("proximo_passo" com o que a pessoa decidir). Quem tem `pessoa agora:` ou `pessoa liga:` sai dessa parte só quando a pessoa contar o que combinou: grave `primeira_resposta`, o combinado no `proximo_passo` e a data, como manda `../../docs/agentes-e-fila.md` (seção 4.6 da `triar-contato`, se instalada).
- **Retornos de hoje:** só estes recebem mensagem pronta. Urgência alta com pessoa designada vem com a observação "quem cuida decide se liga".
- **Para decidir:** "confirmar perdido", retorno passado do máximo, data vencida sem retorno marcado, e retorno vencido de quem ainda não recebeu a primeira resposta (o convite saiu? se saiu, preencha `primeira_resposta`; se não, mande o convite antes).
- **Não enviar:** quem pediu para parar. Linha com passo ainda marcado: proponha "nenhum".

**Passo 3. Conferir antes de escrever.** Para cada retorno: a pessoa respondeu depois da última atualização da linha (o advogado ou a conversa dizem)? Então é conversa, modo D. O retorno caiu fora do horário de atendimento? Sai no próximo horário.

**Passo 4. Escrever as mensagens.** Pela chave da situação e do número (seção 5), da biblioteca do escritório ou de `references/regua-e-mensagens.md`, no tom e no tratamento da ficha, no canal que a pessoa usou. Uma mensagem por retorno, curta, sem áudio. Nome e assunto saem do registro; o que só quem envia sabe (a data que a pessoa pediu, o horário da agenda) fica entre chaves, `{DATA}`, e o revisor aceita. Campo da ficha que falta é pendência no "Antes de enviar", nunca no texto.

**Passo 5. Mostrar a lista** no formato da seção 6. Cada mensagem é A.

**Passo 6. Atualizar o registro.** Para cada retorno que a pessoa confirmar que enviou, use a coluna "Depois do envio" do script: `proximo_passo` vira o retorno seguinte com a data pela régua; depois do encerramento, "confirmar perdido". Mostre as linhas e grave com o ok.

**Passo 7. Para decidir.** Pergunte ao advogado, contato por contato: "Marco como perdido, motivo sem-resposta?". Só com o sim: `etapa = perdido`, `motivo_perda = sem-resposta`, `perdido_na_etapa` com a etapa anterior, `proximo_passo = nenhum`.

**Passo 8. Aprender.** Pergunte: "Alguma mensagem ou algum prazo você mudaria?". Correção vira regra curta nos aprendizados, com o ok. Correção da régua (dias, número de retornos) vai para a ficha comercial, com o ok.

### C. Um contato

Ache a situação (pela etapa) e o número do retorno (pelo `proximo_passo`). Confira a regra fixa 1 antes de tudo. Sem linha no registro, pergunte: "Quando foi o último contato e quantas mensagens a pessoa já recebeu depois dele?". Escreva a mensagem certa, mostre e proponha a linha. Se a pessoa já recebeu o máximo: "Ela já recebeu o encerramento. Pela régua, não vai mais nada; quer marcar como perdido?".

### D. A resposta chegou

| A pessoa respondeu | O que fazer | Registro |
|---|---|---|
| Quer agendar | Opções de horário pelo `como_agenda` | `proximo_passo` "agendar consulta", régua encerrada |
| Aceitou a proposta | Agradecimento curto e o contrato (`contrato-de-honorarios`, se instalada) | `proximo_passo` "enviar contrato" |
| Tem dúvida ou objeção | `objecoes-comerciais` (se instalada) | etapa `negociando`, régua pausada |
| "Agora não, me chama em [data]" | Chave `resposta-retorno-combinado` | `proximo_passo` "retorno combinado", na data dela; não conta como retorno extra |
| "Fechei com outro" ou "desisti" | Chave `resposta-despedida`, sem perguntar por quê | Sugerir `perdido` (fechou-com-outro, desistiu), com o ok |
| "Não quero mais mensagem" | Modelo `confirmacao-parar`, uma vez | `pediu_para_parar = sim`, `proximo_passo` nenhum |
| Relato de aflição, piora ou risco | Sem modelo; vai para o advogado agora | urgência `alta`, fora da régua |

### E. No ciclo (o agente chama)

1. **Avançar o que foi enviado.** Leia a fila dos dias anteriores (`07-operacao/comercial/fila/`). Cada item de retorno com `status: enviado` avança a linha: `proximo_passo` e `data_proximo_passo` pela régua (o `motivo` do item diz o passo seguinte). O agente só mexe nessas colunas e em `atualizado_em` (`funil.md`, regra 11, o que o agente pode mexer).
2. **Rodar o script** com `--json`. Saída 1: o ciclo registra o erro no resumo ("não achei o contatos.csv; os retornos de hoje não foram preparados") e não inventa lista.
3. **Para uma pessoa:** urgência `alta`, marcador `pessoa agora:` ou `pessoa liga:` e caso sensível vão para "PESSOA AGORA"; o resto (fora da área sem urgência) vai para "PARA DECIDIR". Sempre com o motivo do script. Nada vai para a fila. Convite recém-triado com o primeiro retorno em data futura não aparece em parte nenhuma: ainda não é dia.
4. **Retornos de hoje:** um arquivo por retorno em `07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-retorno-<n>-de-<m>.md` (encerramento: `NN-<codigo>-encerramento.md`), no formato de `agentes-e-fila.md`: `tipo` com a chave da mensagem, `motivo` com a situação e o passo seguinte ("retorno 1 de 3, não agendou; depois do envio: retorno 2 de 3 em 2026-03-17"), `prazo` até o fim do horário de atendimento de hoje. O texto vai para o `revisor-comercial` antes de entrar na fila.
5. **Para decidir e não enviar:** vão para o resumo do dia, nunca para a fila.
6. O ciclo nunca marca `perdido` e nunca escreve para quem está nas partes 1 e 4 do script.

### F. Adaptar (a adaptar-comercial chama)

1. Leia `nicho.md` e as mensagens atuais (biblioteca do escritório ou `references/regua-e-mensagens.md`).
2. Reescreva cada mensagem de retorno nas palavras do cliente do nicho (tabela "Como ele fala"), marcando cada mudança `[ALTERADO]`. Exemplos: "a consulta" vira "a conversa com a advogada" se é assim que o cliente fala; o retorno de proposta menciona quem decide junto, se no nicho a família decide.
3. Se o ritmo do nicho pede outra régua (por exemplo, quem só tem acesso ao celular no fim de semana), proponha a régua nova como sugestão para a ficha, sem gravar sozinha.
4. Mostre o antes e o depois. Grave na biblioteca comercial (`escritorio/04-base/comercial/biblioteca-comercial.md`), seção de retornos, mantendo as chaves, só com o ok.

### Último passo, em todos os modos: Aprender

Toda correção do advogado vira proposta de aprendizado, com a pergunta "Quer que eu guarde isto para as próximas vezes?" e a regra em uma linha (`../../docs/aprender-com-o-uso.md`). No ciclo, a correção feita na fila (item `descartado` ou `ajustado` com motivo) vira a mesma proposta no resumo do dia. Nada entra nos aprendizados sem o ok.

## 4. A régua

### 4.1 Régua de exemplo (ajuste antes de usar)

Os dias abaixo são **exemplo** (os da ficha-modelo). Contam em dias corridos a partir do fato que abriu a régua: o convite, a consulta perdida, o envio da proposta.

| Situação | Etapa | Retorno 1 | Retorno 2 | Encerramento | Máximo |
|---|---|---|---|---|---|
| Não agendou depois do convite | `triado` | 2 dias | 7 dias | 15 dias | 3 |
| Faltou à consulta | `nao-compareceu` | no mesmo dia (0) | 3 dias | 10 dias | 3 |
| Proposta sem resposta | `proposta-enviada` ou `negociando` | 2 dias | 7 dias | 15 dias | 3 |

### 4.2 Por que o encerramento conta como retorno

Com máximo 3, a pessoa recebe no máximo três mensagens depois do silêncio, e a terceira já diz que o escritório não vai mais escrever. O número da ficha é o número que a pessoa recebe.

### 4.3 Como o escritório ajusta

- **Na ficha comercial,** campo `follow_up`, por situação, com os nomes da ficha: `nao-agendou: 2, 7, 15 · faltou: 0, 3, 10 · proposta-sem-resposta: 2, 7, 15`. As situações podem vir separadas por "·", por ";" ou uma por linha (recuada abaixo do campo). O script também entende os nomes por extenso ("não agendou", "faltou à consulta", "proposta sem resposta") e ignora o texto entre parênteses que sobrou do modelo da ficha. Campo `maximo_de_retornos`: um número, ou um por situação (`nao-agendou: 3 · proposta-sem-resposta: 2`).
- **Quem arma é a triagem.** A `triar-contato` já grava `retorno 1 de N` com a data do primeiro retorno de "não agendou" (`funil.md`, regra 2). Esta habilidade lê esse passo e segue dele.
- **Exceções** vão para os aprendizados ("Proposta de família: retorno 2 só por ligação").
- **Situação nova** (por exemplo, quem pediu a lista de documentos e não mandou): acrescente no `follow_up` com um nome em minúsculas e hífen (`documentos-pendentes: 3, 7`). O script aceita qualquer nome que estiver no campo. A linha do contato entra nessa régua quando o `proximo_passo` traz o nome: `retorno 1 de 2 · documentos-pendentes`, em qualquer etapa aberta. Sem `maximo_de_retornos` próprio, o máximo é o número de dias da régua dela. Escreva as mensagens com a `mensagens-comerciais` (se instalada) ou no modo C, com as chaves `retorno-<situacao>-1`, `retorno-<situacao>-2` e `encerramento-<situacao>`.
- **Validade da proposta** que vence antes do encerramento: o encerramento diz que a proposta pode ser atualizada se a pessoa quiser retomar. Dito uma vez, sem pressa.

### 4.4 Critérios da lista do dia (o que o script faz, na ordem)

1. `pediu_para_parar = sim`: "não enviar", sempre.
2. Só as etapas `triado`, `nao-compareceu`, `proposta-enviada` e `negociando`, ou qualquer etapa aberta quando o `proximo_passo` nomeia uma situação nova do `follow_up`.
3. Fora da régua: `area = fora-da-area`; palavra de caso sensível no `assunto` ou no `proximo_passo` (parada imediata, pessoa agora, pessoa liga, violência, ameaça, agressão, criança, risco, suicídio, preso, prisão, flagrante, vulnerabilidade, sem renda, idoso, advogada liga); urgência `alta` com `responsavel` vazio. Vão para uma pessoa.
4. Retorno com data futura: fica de fora, sem aviso. É o convite recém-triado esperando o dia do primeiro retorno.
5. `triado` com retorno vencido e `primeira_resposta` vazia: o convite pode não ter saído; para decidir.
6. "confirmar perdido": para decidir.
7. "retorno N de M" ou "retorno combinado" com data até hoje: retorno de hoje. Passou do máximo ou sem data: para decidir.
8. Data vencida sem retorno marcado: para decidir.

## 5. As mensagens, pela chave

| Situação | Retorno 1 | Retorno 2 (e os do meio) | Encerramento |
|---|---|---|---|
| Não agendou | `retorno-nao-agendou-1` | `retorno-nao-agendou-2` | `encerramento-nao-agendou` |
| Faltou à consulta | `retorno-faltou-1` | `retorno-faltou-2` | `encerramento-faltou` |
| Proposta sem resposta | `retorno-proposta-1` | `retorno-proposta-2` | `encerramento-proposta` |

Os textos, as respostas aos casos-limite e o que nunca escrever estão em `references/regua-e-mensagens.md`. Leia no passo 4 do modo B, no modo C e no modo F.

**Exemplo resolvido (Escritório Modelo, segunda 2026-03-16).** O teste com os casos fictícios (`assets/contatos-treino.csv`, as onze linhas que entram no funil) mostra o que a lista precisa fazer:

```
python3 "<pasta desta habilidade>/scripts/lista_do_dia.py" "<pasta desta habilidade>/assets/contatos-treino.csv" --data 2026-03-16 --regua "nao-agendou: 2, 7, 15 · faltou: 0, 3, 10 · proposta-sem-resposta: 2, 7, 15" --maximo 3
```

| Parte | Quem | Por quê |
|---|---|---|
| Para uma pessoa | Joana (C-2026-0003), Lúcia (C-2026-0004), Helena (C-2026-0007) | ameaça envolvendo crianças (`pessoa agora:`); filho preso e área criminal, que o escritório não atende (`pessoa agora:`); idosa sem renda (`pessoa liga:`) |
| Retornos de hoje | Marta, Paulo, Renata, Camila | "retorno 1 de 3" armado pela triagem; Marta com a observação de urgência alta |
| Para decidir | Sérgio (C-2026-0006), Diego (C-2026-0011) | "responder objeção" vencido: vai para a `objecoes-comerciais`; Diego com o retorno vencido e `primeira_resposta` vazia: o convite saiu? |
| Não enviar | Antônio (C-2026-0009) | pediu para parar |

Bruno (remarcação) está em `consulta-agendada` e não entra no follow-up. Rodando o mesmo arquivo com `--data 2026-03-12`, Diego, Renata e Camila não aparecem: o primeiro retorno deles é futuro, e convite recém-triado não vai para uma pessoa. Fernanda é cliente e nem está no funil. Se a Joana ou a Lúcia aparecerem em "Retornos de hoje", alguma coisa está errada: falta palavra de alerta no assunto, ou a área não está como `fora-da-area`. Mensagem do retorno 1 da Renata, no tom do Escritório Modelo:

```
Oi, Renata, tudo bem? Aqui é a secretária do Escritório Modelo.
Você nos procurou sobre o divórcio e eu fiquei de te ajudar a marcar a consulta.
Se ainda fizer sentido, me diga o melhor dia e horário para você.
```

## 6. Formato da saída

```
FOLLOW-UP · [DATA]
Para uma pessoa (sem mensagem): [N]   Retornos de hoje: [N]   Para decidir: [N]   Não enviar: [N]

Para uma pessoa: [CÓDIGO] · [NOME] · [MOTIVO]

1. [CÓDIGO] · [NOME] · [SITUAÇÃO] · retorno [N] de [M] · [CANAL] · quem envia: [FUNÇÃO]
   "[mensagem pronta; campos do envio entre chaves, como {DATA}]"
   Depois do envio: [PRÓXIMO PASSO] em [DATA]

Para decidir: [CÓDIGO] · [NOME]: [PERGUNTA]
Não enviar: [CÓDIGO] · [NOME]
Registro: [linhas propostas do contatos.csv]
```

A lista sempre começa pelos que vão para uma pessoa, para ninguém copiar mensagem para eles por engano.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Lista do dia (modo B) | No chat, pronta para copiar |
| Rascunhos de retorno (modo E) | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-retorno-<n>-de-<m>.md` |
| Régua do escritório | `escritorio/04-base/comum/ficha-comercial.md`, campos `follow_up` e `maximo_de_retornos`, com linha no histórico |
| Mensagens de retorno aprovadas (modos B e F) | `escritorio/04-base/comercial/biblioteca-comercial.md`, seção de retornos, pela chave, sem duplicar |
| Linhas do funil | `escritorio/07-operacao/comercial/contatos.csv`: `proximo_passo`, `data_proximo_passo`, `atualizado_em`; com o advogado, `etapa = perdido`, `motivo_perda`, `perdido_na_etapa`; quando pedido, `pediu_para_parar = sim` |
| Exceções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino com casos fictícios | `escritorio/07-operacao/_treino/comercial/contatos.csv` (copie `assets/contatos-treino.csv` para lá) |

Sem pasta aberta: a lista sai no chat e as linhas do registro como tabela para colar na planilha. **Conectores** (conferir na configuração da conta): com Google Agenda, a habilidade pode conferir quais consultas de ontem não aconteceram e perguntar se entram como `nao-compareceu`; com Gmail, os retornos por e-mail podem ficar como rascunho, nunca enviados.

## 8. Solo e equipe

**Solo:** um horário fixo por dia para a lista (por exemplo, depois do almoço). Dez minutos: ler a parte "para uma pessoa" primeiro, depois ajustar, enviar e atualizar o registro.

**Equipe:** a secretária roda a lista e envia os retornos com mensagem aprovada. O advogado recebe a parte "para uma pessoa", o "para decidir" e os de urgência alta. Se os retornos de proposta forem todos para o advogado, aponte: é ali que as propostas param.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Retorno de venda para quem relatou ameaça ou prisão | Exposição e risco para quem pediu ajuda | Regra fixa 1 e a parte "para uma pessoa" do script |
| Mensagem para quem pediu para parar | Incômodo, reclamação, risco ético | "Não enviar" e a linha a corrigir |
| Retorno para quem nunca recebeu o convite | Mensagem sem sentido | `primeira_resposta` vazia vai para uma pessoa |
| Planilha do Excel com ponto e vírgula lida como vazia | Lista do dia em branco e ninguém retomado | Leitura robusta e erro claro quando não lê |
| Dias úteis e corridos misturados | Retorno cedo ou tarde demais | Régua em dias corridos da ficha |
| "E aí, pensou?" toda semana | Insistência que afasta | Máximo de retornos da ficha |
| Marcar perdido sozinho | Funil decide no lugar do advogado | "Para decidir", só com o ok |

## 10. Próximo passo

- A pessoa quer agendar: `agenda-da-consulta` (se instalada) e `roteiro-da-consulta`. Sem elas, agende e registre `consulta-agendada`.
- Aceitou a proposta: `contrato-de-honorarios` (se instalada). Sem ela, use o modelo de contrato do escritório.
- Respondeu com objeção: `objecoes-comerciais` (se instalada). Sem ela, mostre a mensagem ao advogado antes de responder.
- Lista do dia todo dia sem ninguém pedir: `rotina-comercial` (o ciclo chama esta habilidade).

## Referências desta habilidade

- `references/regua-e-mensagens.md`: as mensagens de cada retorno, com a chave, o encerramento, as respostas aos casos-limite e o que nunca escrever. Leia no modo B, passo 4, no modo C e no modo F.
- `scripts/lista_do_dia.py`: lê o `contatos.csv` e a régua da ficha e devolve a lista do dia em quatro partes. Rode no modo B, passo 1, e no modo E.
- `assets/contatos-treino.csv`: as onze linhas dos casos fictícios que entram no funil, para testar o script antes de usar o registro real.
