---
name: rotina-comercial
description: >
  O motor do comercial. Configura e explica o ciclo do dia: o agente do plugin pelo comando
  /motor-comercial:ciclo, a tarefa agendada que chama esse comando (texto pronto), o "ciclo à
  mão" no chat quando não há agente, e o resumo do dia pelo script de pendências (PESSOA AGORA,
  contatos sem resposta além do prazo em horas úteis, consultas, retornos da régua em dias
  corridos, propostas paradas, quem pediu para parar, o que corrigir no registro), lendo desde
  a última rodada, inclusive fim de semana. Grava a ficha da automação, o registro de uso e o
  plano para quando não roda. Use quando o advogado disser "configura o ciclo", "quero o
  comercial rodando sozinho", "roda o comercial de hoje à mão", "o que ficou pendente", "quem
  está sem resposta", "o ciclo não rodou". Não use para triar uma mensagem nova (use
  triar-contato) nem para o painel do mês (use painel-do-funil).
---

# Rotina comercial

> Todo dia, no mesmo horário, alguém precisa saber quem está esperando resposta, quem é para uma pessoa agora e que retorno vence hoje. O ciclo lê, separa, rascunha e resume. Uma pessoa aprova e envia.

Regras do plugin: `../../docs/regras.md`. Ciclo, agente, revisor e fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-comercial-modelo.md` e a tabela de campos em `../../docs/ficha-comercial.md`. Funil: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 8h30. No sábado, uma mulher escreveu que o ex ameaçou sumir com as crianças. A rotina de sexta tinha rodado, e a de segunda leu só "a triagem do dia útil anterior". A mensagem do sábado ficou de fora. O ciclo certo lê desde a última rodada registrada, sábado e domingo incluídos, e põe essa mensagem no topo, em PESSOA AGORA.

**Regras fixas desta habilidade:**
1. O ciclo prepara e aponta. Não envia nada a ninguém e só mexe no `contatos.csv` dentro do que `funil.md` permite (regra 11, o que o agente pode mexer).
2. PESSOA AGORA vem antes de tudo, e quem está ali não recebe rascunho nem retorno da régua (`funil.md`, regras 4 e 5). Sai da lista só quando a pessoa conta o que combinou.
3. Sem resposta é `primeira_resposta` vazia antes de `consulta-agendada`, contado em horas úteis. A régua de retorno é em dias corridos.
4. Lê desde a última rodada do registro de uso, todos os dias do período. Sem registro, as últimas 24 horas, com aviso.
5. Treino nunca entra no resumo real. No resumo, só código, primeiro nome ou iniciais, área e assunto curto.

## 1. Quando usar

**Use quando:**
- O escritório quer o comercial rodando todo dia sem ninguém pedir (modo configurar).
- Não há agente (chat com Projeto) e alguém quer o ciclo de hoje (modo "ciclo à mão").
- O `/motor-comercial:ciclo` não achou o agente e caiu aqui (modo "ciclo à mão").
- Alguém quer só a lista do que está pendente agora (modo "só o resumo").
- O `/motor-comercial:status` mostrou que o ciclo não roda há dias (modo "não rodou").

**Não use quando:**
- Chegou uma mensagem e o pedido é classificá-la: `triar-contato`.
- O pedido é o painel do mês, com conversão e origem: `painel-do-funil` (se instalada). Sem ela, o resumo da semana desta habilidade dá uma primeira leitura.
- O pedido é a mensagem de retorno para cada contato parado: `follow-up` (se instalada). Sem ela, o convite da biblioteca, com alguém lendo e respeitando `pediu_para_parar`.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-comercial.md`), `nicho.md` se existir e os aprendizados (`aprendizados-comercial.md`). Se existir, leia a ficha da automação (`escritorio/05-automacoes/ciclo-comercial/ficha.md`): os critérios dela valem para o ciclo.
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Qual é o horário de atendimento?", depois "Em quanto tempo, em horas úteis, uma pessoa responde quem escreve pela primeira vez?".
3. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`). Sem registro, o ciclo pode ser configurado mesmo assim; o resumo começa a ter conteúdo depois da primeira triagem.
4. **Os valores da ficha vão para o script como estão** (formato exato na seção 4.1). O script lê "dias úteis, das 9h às 18h" e "até 2 horas úteis" sem conversão. Só "no mesmo dia" ou "em 1 dia útil" pedem uma pergunta antes: "Em horas úteis, quanto é 'no mesmo dia' para vocês?". A régua do `follow_up` fica em dias corridos; o primeiro intervalo de `proposta-sem-resposta` vira `--dias-proposta`.
5. **Onde roda** (`onde_roda`): Cowork ou Claude Code têm o comando e o agente; o chat com Projeto, só o ciclo à mão. Conferir na configuração da conta se agentes de plugin e tarefas agendadas estão disponíveis.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `quem_atende`, `horario_de_atendimento`, `horario_da_rotina_diaria` · C: `primeira_resposta_contato_novo`, `follow_up` |
| Melhora | E: `agenda`, `conectores_no_claude`, `onde_roda`, `quem_aprova_rascunhos` |

Campo que falta e o ciclo precisa: pergunte aquele campo, uma vez, e ofereça gravar na ficha e na ficha da automação.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Configurar | Primeira vez | O jeito de rodar escolhido, a tarefa agendada pronta (se houver), ficha da automação, registro de uso, primeiro ciclo |
| Ciclo com agente | Cowork ou Claude Code | O `agente-comercial` roda; esta habilidade explica e confere o que ele precisa |
| Ciclo à mão | Chat com Projeto, ou o agente falhou | O mesmo ciclo, passo a passo, mostrado e gravado com o ok |
| Só o resumo | "o que está pendente?" | O resumo do script, sem triagem nem rascunhos |
| Semana | Segundas, ou "resumo da semana" | O resumo com a semana anterior no fim |
| Não rodou | Faltou o resumo do dia | A causa provável, o ciclo de hoje e o ajuste do plano |

### Modo configurar

**Passo 1. Conferir as fontes.** Veja se existem `contatos.csv`, `entrada/`, `triagens/` e `fila/` em `escritorio/07-operacao/comercial/`. Mostre em duas linhas o que o ciclo vai ler e o que falta; crie as pastas que faltam com o ok.

**Passo 2. Combinar a entrada.** Pergunte: "Quem solta as conversas do dia na pasta de entrada, e quando?". O ciclo não lê o WhatsApp sozinho: lê o que alguém exporta ou cola em `entrada/`, mais os conectores.

**Passo 3. Combinar o horário e quem lê.** Pergunte: "Que horas você quer o resumo pronto?" e depois "Quem aprova a fila, e em que horário?". Sugestão: 30 minutos antes de começar a responder. As respostas vão para `horario_da_rotina_diaria` e `quem_aprova_rascunhos`.

**Passo 4. Critérios.** Mostre os critérios convertidos (expediente, prazo do contato novo, régua, proposta parada, feriados do mês) e peça o ok.

**Passo 5. Conectores.** Se houver (`conectores_no_claude`), combine: e-mail para ler mensagens de contato; agenda para ler as consultas e horários livres. Só leitura.

**Passo 6. Escolher o jeito de rodar.** Pergunte: "Você usa o Claude no Cowork, no Claude Code ou no chat com Projeto?".
- **Cowork ou Claude Code, com tarefas agendadas:** preencha `assets/tarefa-agendada.md`, seção 1, e entregue para colar no recurso de tarefas agendadas. A tarefa chama `/motor-comercial:ciclo`. Conferir na configuração da conta o nome do recurso, se precisa do computador ligado e se enxerga a pasta.
- **Cowork ou Claude Code, sem tarefa agendada:** o comando `/motor-comercial:ciclo` todo dia no horário combinado, por alguém com dono (seção 2).
- **Chat com Projeto:** o ciclo à mão (seção 3), com o pedido pronto para colar.

**Passo 7. Conferir o que o agente precisa.** Confirme que existem: esta habilidade com `scripts/pendencias.py`; a seção 4.1 e o modo no ciclo da `triar-contato`; a biblioteca comercial (`04-base/comercial/biblioteca-comercial.md`; sem ela, o agente usa os modelos crus da `mensagens-comerciais` e avisa); o registro de uso. O que faltar vai para o resumo como "o que não deu para fazer".

**Passo 8. Gravar.** Preencha `assets/ficha-da-automacao.md` e `assets/registro-de-uso.md` e grave em `escritorio/05-automacoes/ciclo-comercial/`. No "Quando não roda" da ficha, cole o plano combinado de `references/quando-a-rotina-nao-roda.md`, seção 3. Mostre antes de gravar.

**Passo 9. Rodar a primeira vez.** Rode o ciclo agora (comando ou à mão) para o advogado ver o resumo antes da primeira manhã.

**Passo 10. Aprender**, como no ciclo à mão.

### Modo ciclo com agente

O `agente-comercial` faz o ciclo de `agentes-e-fila.md` e usa: a `triar-contato` (seção 4.1 e modo no ciclo), a `mensagens-comerciais` (modo no ciclo), a `follow-up` e a `agenda-da-consulta` (se instaladas), o `revisor-comercial` e o script desta habilidade para o resumo. Esta habilidade não substitui o agente: configura, explica e é o plano B. Depois de cada rodada, confira com o advogado a primeira semana de resumos e ajuste os critérios.

### Modo ciclo à mão

Mesmos passos do agente, mostrados ao advogado, com o ok antes de gravar.

1. **Desde quando.** Leia o registro de uso e ache a última rodada completa (nem `não rodou` nem `só o resumo`). Sem registro: últimas 24 horas, e avise.
2. **Coletar.** Arquivos novos em `escritorio/07-operacao/comercial/entrada/` desde essa hora, conectores (só leitura) e as linhas do `contatos.csv`. Sem pasta: peça as mensagens e o registro colados (`assets/tarefa-agendada.md`, seção 3).
3. **PESSOA AGORA primeiro.** Comece pelo que já estava em PESSOA AGORA no último resumo: para cada item, pergunte "Já falou com essa pessoa? O que ficou combinado?" e, com a resposta, grave como manda `agentes-e-fila.md` (seção 4.6 da `triar-contato`): `primeira_resposta` com a hora do contato, o `proximo_passo` que começa com `pessoa agora:` ou `pessoa liga:` trocado pelo combinado, com data, e a linha na triagem do dia. Sem resposta, o item fica no topo. Depois, passe cada mensagem nova pela seção 4.1 da `triar-contato`. Achou: nada de rascunho; uma frase do porquê e o aviso a quem cuida (`urgencia_vai_para`). Se a `triar-contato` não estiver instalada, use os sinais da seção 5 de `regras.md`.
4. **Triar** o resto pela `triar-contato`. Cliente ativo vai para a lista "para a experiência do cliente".
5. **Rascunhar** cada resposta-base pela `mensagens-comerciais`; retornos do dia pela `follow-up`; confirmações e lembretes pela `agenda-da-consulta` (as que estiverem instaladas). Sem elas, o modelo da biblioteca comercial.
6. **Revisar** cada rascunho pelo `revisor-comercial`, se disponível. No chat, aplique você mesmo a tabela de dez perguntas dele, item por item, e mostre o resultado ao lado de cada rascunho.
7. **Gravar a fila** em `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/`, no formato de `agentes-e-fila.md`, e as linhas do registro, com o ok.
8. **Resumir.** Rode o script (seção 4) e monte o resumo no formato de `assets/modelo-do-resumo.md`, com "Comece por aqui" no topo (no máximo cinco ações). Grave em `escritorio/07-operacao/comercial/rotina/AAAA-MM-DD.md`; se já existir, acrescente uma seção com a hora.
9. **Registrar** a rodada no registro de uso, com `à mão`.
10. **Aprender.** Pergunte: "Alguma coisa nesse resumo não devia estar aí, ou faltou alguma?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-comercial.md` (`../../docs/aprender-com-o-uso.md`). Se muda um critério, atualize a ficha e a ficha da automação, com linha no histórico das duas.

### Modo só o resumo
Rode o script (seção 4), mostre o resultado com "Comece por aqui" e grave com o ok. No registro de uso, a linha é `só o resumo`, que não conta como rodada completa: o próximo ciclo continua lendo desde a última rodada de verdade.

### Modo não rodou
1. Leia o registro de uso e a pasta da rotina e diga desde quando não há ciclo.
2. Aponte a causa provável pela tabela de `references/quando-a-rotina-nao-roda.md`, seção 2.
3. Rode o ciclo à mão com a data de hoje. Como ele lê desde a última rodada, cobre os dias sem ciclo; o que venceu aparece como vencido.
4. Registre os dias faltantes como `não rodou`, com a causa.
5. Dois dias seguidos sem ciclo: proponha revisar o jeito de rodar.
6. **Aprender.** Pergunte: "O que fez o ciclo não rodar, e o que muda para não se repetir?". A resposta vira ajuste no plano da ficha da automação e, se for regra de uso, aprendizado com o ok.

## 4. O script de pendências

Rode com o caminho da pasta desta habilidade e o do csv como argumentos. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/rotina-comercial`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-comercial/scripts/pendencias.py" \
  "escritorio/07-operacao/comercial/contatos.csv" --data AAAA-MM-DD \
  --expediente "dias úteis, das 9h às 18h" --prazo-novo "até 2 horas úteis" \
  --dias-proposta 2 --feriados "2026-04-21, 2026-06-04" --alertas "ameaça; medida protetiva" \
  --registro-de-uso "escritorio/05-automacoes/ciclo-comercial/registro-de-uso.md" \
  --triagens "escritorio/07-operacao/comercial/triagens" --fila "escritorio/07-operacao/comercial/fila"
```

Sem `${CLAUDE_PLUGIN_ROOT}`, troque pelo caminho da pasta desta habilidade. Outras opções: `--hora HH:MM`, `--sabado`, `--desde "AAAA-MM-DD HH:MM"` (vale mais que o registro de uso), `--semana` ou `--sem-semana`, `--treino` (só para o registro de `_treino/`). `--help` mostra tudo.

### 4.1 Os valores da ficha, no formato que o script aceita

O `agente-comercial` (e quem roda à mão) copia os campos da ficha para o comando, sempre entre aspas:

| Opção | Campo da ficha | Formato aceito | Exemplos que funcionam |
|---|---|---|---|
| `--expediente` | E: `horario_de_atendimento` | O texto do campo como está, ou `HH:MM-HH:MM`. Horas como `9h`, `8h30`, `09:00` ou `9 às 18`. Dois turnos com "e" ou vírgula. Um trecho depois de ponto e vírgula que fala só de sábado vira o horário do sábado; "segunda a sábado" usa o mesmo horário no sábado; "exceto sábado" tira | `"dias úteis, das 9h às 18h"` · `"9h-18h"` · `09:00-18:00` · `"8h30 às 12h e 14h às 18h"` · `"09:00-12:00,14:00-18:00"` · `"dias úteis das 9h às 18h; sábado das 9h às 12h"` |
| `--prazo-novo` | C: `primeira_resposta_contato_novo` | Horas úteis: o número (ponto ou vírgula) ou o texto do campo com horas ou minutos | `2` · `1,5` · `"até 2 horas úteis"` · `"1h30"` · `"30 minutos"` |
| `--feriados` | E: `feriados_e_recessos` | Datas `AAAA-MM-DD`, `DD/MM/AAAA` ou `DD/MM` (no ano do resumo), em qualquer texto. "De DD/MM a DD/MM" vira todos os dias do intervalo (até 60) | `"2026-04-21, 2026-06-04"` · `"Carnaval 16/02 e 17/02; recesso de 20/12 a 06/01"` |
| `--dias-proposta` | C: `follow_up`, primeiro número de `proposta-sem-resposta` | Um número inteiro de dias corridos | `2` |
| `--alertas` | E: `palavras_de_alerta` de prioridade máxima (as da seção 4.1 da `triar-contato`) | Palavras ou frases separadas por ponto e vírgula, vírgula ou "·" | `"ameaça; medida protetiva · levar o filho"` |

O script recusa, com código 1 e uma frase do que fazer: `--expediente` ou `--prazo-novo` vazio ou `[A PREENCHER]`, expediente sem nenhuma hora ("horário comercial"), prazo em dias ("no mesmo dia", "em 1 dia útil": converta para horas úteis com o advogado antes) e feriado sem data. Sem `--expediente` e sem `--prazo-novo`, usa 09:00-18:00 e 2 horas e escreve "padrão do script, confirme na ficha" nos critérios. A primeira linha do resumo mostra sempre como cada valor foi lido ("expediente 08:30-12:00 e 14:00-18:00, lido de ...").

`--feriados` e `--alertas` vazios ou só com marcação (`[A PREENCHER]`, `[A DEFINIR]`, `[A CONFIRMAR]`, `[CONFERIR]` ou outro texto entre colchetes em maiúsculas) não param o script: o valor é ignorado e o resumo traz o aviso "campo feriados_e_recessos da ficha vazio" (só o fim de semana conta como dia sem expediente) ou "campo palavras_de_alerta da ficha vazio" (só os sinais fixos tiram o contato da régua). A marcação nunca vira palavra de alerta. Campo com datas ou palavras e uma marcação no meio: o script lê o que há e ignora a marcação, com aviso.

### 4.2 O que o script lê e o que aponta

O script lê o csv de vírgula ou ponto e vírgula, com ou sem BOM, em UTF-8 ou no padrão do Excel, datas AAAA-MM-DD ou DD/MM/AAAA, etapas e opções sem diferenciar maiúscula. Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio ou falta coluna obrigatória, e quando recebe o registro de treino sem `--treino`. Nunca diz que não há nada a apontar sem ter lido. Sem Python, aplique à mão as mesmas regras:

| Seção | Entra | Critério |
|---|---|---|
| PESSOA AGORA | Linha aberta com `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:` (`funil.md`, regra 4); linha com retorno da régua e sinal de alerta no `assunto` (sinais fixos de parada imediata, como ameaça, violência, preso, medida protetiva, e as `--alertas`); urgência `alta` sem responsável; rascunho `pendente` na fila há mais de um dia útil | Antes de tudo. Sem rascunho e fora da régua (`funil.md`, regra 5). Marcador com `primeira_resposta` já preenchida aparece com "trocar o marcador pelo combinado" |
| 1. Sem resposta | `novo` ou `triado`, `primeira_resposta` vazia | Horas úteis desde a `entrada` maiores que `primeira_resposta_contato_novo`; fora do horário conta da abertura. Os no prazo vêm abaixo, com a hora em que vencem |
| 2. Consultas | `consulta-agendada` sem "remarcar" no próximo passo | Hoje; até o próximo dia útil (lembrete da véspera); data passada (aconteceu ou faltou? uma pessoa decide) |
| 3. Retornos | Próximo passo "retorno ..." com data até hoje, fora de quem pediu para parar, fora da área, com sinal de alerta no assunto ou em PESSOA AGORA | Dias corridos de atraso |
| 3. Outros próximos passos | Qualquer outro próximo passo com data até hoje ("remarcar consulta", "responder dúvida da proposta", "confirmar encaminhado") | Para uma pessoa |
| 4. Propostas paradas | `proposta-enviada` ou `negociando` | Dias corridos desde `atualizado_em` maiores ou iguais a `--dias-proposta` |
| 5. Pediu para parar | `pediu_para_parar = sim` | Conflito se ainda tem próximo passo ou data |
| 6. Registro a corrigir | Qualquer linha | Código repetido ou vazio, etapa, tipo, urgência ou data fora do padrão, `tipo = cliente`, `triado` sem próximo passo, `perdido` sem motivo, retorno vencendo com `primeira_resposta` vazia |
| Desde a última rodada | Entradas e triagens do período, todos os dias | E a contagem da fila |

Etapas encerradas (`encaminhado`, `recusado`, `sem-caso`, `perdido`) ficam fora, menos em "pediu para parar". O registro guarda só a etapa atual; o resumo da semana estima o que mudou pela coluna `atualizado_em`, e diz isso.

## 5. Exemplo resolvido (treino com os casos fictícios)

As onze linhas que a `triar-contato` grava para `../../docs/casos-ficticios.md` (a Fernanda é cliente e não entra), em `escritorio/07-operacao/_treino/comercial/contatos.csv`, sem nenhuma primeira resposta preenchida. Quinta, 2026-03-12, 17h, com expediente das 9h às 18h e contato novo em 2 horas úteis:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-comercial/scripts/pendencias.py" \
  "escritorio/07-operacao/_treino/comercial/contatos.csv" --data 2026-03-12 --hora 17:00 \
  --expediente "dias úteis, das 9h às 18h" --prazo-novo "até 2 horas úteis" --treino
```

O script devolve: PESSOA AGORA com Joana (C-2026-0003, ameaça com crianças), Lúcia (C-2026-0004, filho preso, encaminhar) e Helena (C-2026-0007, pessoa liga); sem resposta além do prazo Marta (alta, 26h úteis), Paulo, Renata, Camila e Antônio (baixa, só a confirmação de parar); Diego ainda no prazo até 17h48; retornos de hoje de Marta e Paulo, com o aviso no registro de que o convite deles não saiu; Bruno em "remarcar consulta", e não como consulta de hoje; Sérgio com a dúvida da proposta vencida há um dia.

O "Comece por aqui":
```
1. Ligar para Joana · C-2026-0003 · advogada · ameaça envolvendo as crianças
2. Enviar o encaminhamento a Lúcia · C-2026-0004 · quem estiver no canal · prisão, criminal não atendido
3. Ligar para Helena · C-2026-0007 · advogada · mãe idosa sem renda
4. Mandar o convite com prioridade a Marta · C-2026-0001 · secretaria · benefício cortado, 26h sem resposta
5. Mandar as opções de horário a Bruno · C-2026-0008 · secretaria · remarcação pedida ontem
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Resumo do dia (e da semana, às segundas) | `escritorio/07-operacao/comercial/rotina/AAAA-MM-DD.md` |
| Rascunhos do ciclo à mão | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/` |
| Ficha da automação, com o plano para quando não roda | `escritorio/05-automacoes/ciclo-comercial/ficha.md` |
| Registro de uso (uma linha por rodada) | `escritorio/05-automacoes/ciclo-comercial/registro-de-uso.md` |
| Texto da tarefa agendada | No chat, para colar no recurso de tarefas agendadas |
| Linhas e correções do registro | `escritorio/07-operacao/comercial/contatos.csv`, só com o ok e só o que `funil.md` permite |
| Treino | `escritorio/07-operacao/_treino/comercial/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Critério novo (prazo, expediente, horário do ciclo) | A ficha do escritório ou a comercial, e a ficha da automação, com linha no histórico |

Sem pasta aberta: o resumo e os rascunhos vêm no chat, para guardar com o nome da data, e as linhas do registro vêm como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** o resumo é para o titular, num horário fixo, antes de abrir o WhatsApp. Dez minutos com o "Comece por aqui" e a fila substituem a ansiedade de abrir cada notificação. Em semana de audiência pela manhã, o ciclo roda no almoço.

**Equipe:** a secretária lê o resumo inteiro, aprova a fila do que é dela e distribui. O advogado recebe PESSOA AGORA e "para decidir". Quando o mesmo nome aparece em quase tudo, aponte: a solução é redistribuir, não apertar o prazo. Uma pessoa é dona da ficha da automação.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Ler só o dia útil anterior | A mensagem de sábado some | Leitura desde a última rodada registrada |
| "Sem resposta" só para quem está em `novo` | Contato triado e nunca respondido some da lista | `primeira_resposta` vazia antes de `consulta-agendada` |
| Horas úteis e dias corridos misturados | Prazo de resposta estourado no fim de semana, ou retorno adiantado | Resposta em horas úteis; régua em dias corridos |
| Script sem arquivo dizendo que está tudo em dia | A equipe confia num resumo que não leu nada | Código 1 e "ERRO:" claro |
| Planilha do Excel não lida | Resumo vazio sem motivo | Leitura robusta de separador, BOM, acento, data e maiúscula |
| Retorno de venda para quem contou uma ameaça | Mensagem pronta para quem precisava de uma pessoa | Marcador `pessoa agora:` e sinal no assunto tiram da régua |
| Prazo da ficha convertido errado à mão | Contatos acusados cedo ou tarde demais | O script lê o texto da ficha e mostra como leu |
| Treino no resumo real | Equipe ligando para quem não existe | `--treino` obrigatório para `_treino/` |
| Ciclo que envia sozinho | Mensagem errada sem ninguém ler | Fila de aprovação; quem envia é a pessoa |
| Ciclo que para e ninguém percebe | Pendências acumulam em silêncio | Registro de uso, plano B e o aviso do status |

## 9. Próximo passo

- PESSOA AGORA: quem cuida da urgência liga, pela ficha.
- Contatos sem resposta: a fila do dia (`/motor-comercial:fila`) e, para o que nem foi triado, `triar-contato`.
- Retornos e propostas paradas: `follow-up` (se instalada); sem ela, o convite ou o envio de proposta da biblioteca, com alguém lendo.
- Consultas de hoje e de amanhã: `agenda-da-consulta` e `roteiro-da-consulta` (se instaladas); sem elas, a pessoa confere a agenda.
- Mês fechado: `painel-do-funil` (se instalada).

## Referências desta habilidade

- `scripts/pendencias.py`: o script de pendências (só biblioteca padrão). Rode no passo 8 do ciclo à mão e no modo só o resumo. O `agente-comercial` usa o mesmo script.
- `assets/tarefa-agendada.md`: a tarefa agendada que chama `/motor-comercial:ciclo`, o comando e o ciclo à mão, com a versão para o chat sem pasta. Use no passo 6 do configurar.
- `assets/ficha-da-automacao.md`: modelo da ficha da automação. Use no passo 8 do configurar.
- `assets/registro-de-uso.md`: modelo do registro de uso, com os valores de "Como rodou". Use no passo 8 do configurar.
- `assets/modelo-do-resumo.md`: o formato do resumo do dia. Use no passo 8 do ciclo à mão.
- `references/quando-a-rotina-nao-roda.md`: sinais, causas, o plano combinado e o que nunca fazer para compensar. Leia no configurar e no modo não rodou.
