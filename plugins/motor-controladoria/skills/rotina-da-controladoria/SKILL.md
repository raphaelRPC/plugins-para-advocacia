---
name: rotina-da-controladoria
description: >
  O motor da controladoria sem depender de agente. Configura e explica o ciclo do dia: as duas
  tarefas agendadas que chamam /motor-controladoria:ciclo (manhã e tarde, texto pronto), o "ciclo
  à mão" no chat quando não há agente, e o resumo do dia pelo script de pendências sobre o
  prazos.csv e o publicacoes.csv (vence hoje e no próximo dia útil pelo calendário do tribunal,
  vence na semana, captada com atraso, sugerido parado, conferido sem agenda, sem responsável, não
  triadas, sem caso, audiências e perícias). Grava a ficha da automação, o registro de uso e o
  plano para quando não roda. Use quando disserem "configura o ciclo das publicações", "roda as
  intimações de hoje à mão", "o que vence amanhã", "o que espera conferência", "o ciclo não
  rodou". Não use para contar um prazo (use calcular-prazo) nem para conferir (use
  dupla-conferencia).
---

# Rotina da controladoria

> Duas vezes por dia, a equipe precisa saber o que vence hoje e no próximo dia útil, o que chegou e ainda não tem dono, e o que espera a dupla conferência. O ciclo capta, tria, calcula e aponta. Uma pessoa confere, decide e cumpre.

Regras: `../../docs/regras.md`. Contagem: `../../docs/contagem.md`. Publicações, prazos e status: `../../docs/prazos.md`. Ciclo, agente, revisor e fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-da-controladoria-modelo.md` e a tabela de campos em `../../docs/ficha-da-controladoria.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 8h. A estagiária abre o resumo e o primeiro item é o recurso ordinário da Camila: a sentença foi disponibilizada na quinta, mas o ciclo não rodou na quinta nem na sexta, e o prazo já corre desde segunda. Ninguém perdeu nada ainda, e o resumo diz isso em uma linha, antes do recurso do Otávio, que vence só no fim do mês.

**Regras fixas desta habilidade:**
1. A IA capta e calcula, mas não interpreta. O ciclo nunca move prazo para `conferido`, `cumprido`, `perdido` ou `cancelado`, nunca escreve nome em `conferido_por` e nunca agenda o que está `sugerido`.
2. Prazo com data de segurança ou fatal vencida, de hoje ou do próximo dia útil do tribunal vai para PESSOA AGORA antes de qualquer outra coisa, em qualquer status.
3. Prazo `sugerido` nunca aparece como se valesse: no resumo, a data é "sugerida" e o status é "sugerido, sem dupla conferência".
4. O ciclo não abre painel de tribunal e não usa senha, certificado ou token. O que está nos painéis chega pelo registro que a pessoa faz.
5. Treino nunca entra no resumo real. No resumo, só id, código, primeiro nome, tribunal, providência, datas, status e responsável.

## 1. Quando usar

**Use quando:**
- O escritório quer o ciclo rodando duas vezes por dia sem ninguém pedir (modo configurar).
- Não há agente (chat com Projeto) e alguém quer o ciclo de agora (modo ciclo à mão).
- O `/motor-controladoria:ciclo` não achou o agente e caiu aqui (ciclo à mão, com a revisão pela tabela de `agents/revisor-de-controladoria.md`).
- Alguém quer só a lista do que está pendente (modo só o resumo; o `/motor-controladoria:status` usa o mesmo script).
- O status mostrou que o ciclo não roda há dias, ou apareceu "captada com atraso" (modo não rodou).

**Não use quando:**
- O pedido é contar um prazo: `calcular-prazo` (se instalada; sem ela, a conta passo a passo de `contagem.md`, com a pessoa).
- O pedido é conferir um prazo: `dupla-conferencia`, ou o `/motor-controladoria:fila`.
- O pedido é o retrato da semana por responsável, para a reunião: `painel-da-controladoria` (se instalada).
- O pedido é a passagem de férias: `cobertura-de-ausencia` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`), `nicho.md` se existir e `aprendizados-controladoria.md`. Se existir, leia a ficha da automação (`escritorio/05-automacoes/ciclo-da-controladoria/ficha.md`): as janelas dela valem para o script.
2. **Sem ficha:** ofereça `/motor-controladoria:comecar`. Para seguir, pergunte só: "Quem cuida dos prazos e quem faz a segunda conferência?", depois "Em que horários o ciclo deve rodar?".
3. **Leia os registros** (`escritorio/07-operacao/controladoria/prazos.csv` e `publicacoes.csv`). Sem eles, o ciclo pode ser configurado: o agente cria os dois só com a linha de títulos de `prazos.md`.
4. **Base:** a tabela de regras (`04-base/controladoria/regras-de-contagem.md`) validada ou não, e os calendários (`04-base/controladoria/calendario/`) de cada tribunal da ficha, do ano. O que faltar vai para o resumo como aviso, e o script avisa em destaque quando não há calendário.
5. **Onde roda** (`onde_roda`): Cowork ou Claude Code têm o comando e o agente; o chat com Projeto, só o ciclo à mão. Conferir na configuração da conta se agentes de plugin e tarefas agendadas estão disponíveis.
6. **Conta de IA.** Publicação tem número de processo e às vezes dado sensível. Em conta pessoal, só os casos fictícios.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `horario_da_rotina_diaria` · K: `responsavel_controladoria` |
| Melhora | E: `onde_roda`, `conectores_no_claude`, `feriados_e_recessos` · K: `horario_da_captacao` |

Também lê, quando preenchidos, K: `quem_confere`, `oabs_monitoradas`, `tribunais` e `dias_de_seguranca`, para o texto da tarefa e o resumo. Campo que falta e o ciclo precisa: pergunte aquele campo, uma vez, e ofereça gravar na ficha e na ficha da automação.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Configurar | Primeira vez | O jeito de rodar, as duas tarefas agendadas (se houver), ficha da automação, registro de uso, primeiro ciclo |
| Ciclo com agente | Cowork ou Claude Code | O `agente-de-controladoria` roda; esta habilidade explica e confere o que ele precisa |
| Ciclo à mão | Chat com Projeto, ou o agente falhou | O mesmo ciclo, passo a passo, mostrado e gravado com o ok |
| Só o resumo | "o que vence amanhã?" | O resumo do script, sem captação nem conta |
| Não rodou | Faltou o resumo, ou "captada com atraso" | A causa provável, o ciclo de agora e o ajuste do plano |
| Treino | Casos fictícios ou "é teste" | O resumo dos registros de treino, gravado em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | Horários, janelas e o que entra no resumo no jeito do escritório |

Pedido direto ("o que vence amanhã?"): não faça entrevista. Rode o script e mostre.

### Modo configurar

**Passo 1. Conferir as fontes.** Veja se existem `publicacoes.csv`, `prazos.csv`, `entrada/`, `fila/`, `rotina/` em `escritorio/07-operacao/controladoria/`, e os calendários. Mostre em duas linhas o que o ciclo vai ler e o que falta; crie as pastas que faltam com o ok.

**Passo 2. Combinar os horários.** Pergunte: "Em que horários vocês querem o ciclo rodando? Eu sugiro antes do expediente e depois do almoço." A resposta vai para `horario_da_captacao`. Depois: "Até que horas o resumo da manhã precisa estar pronto?" (`horario_da_rotina_diaria`).

**Passo 3. Combinar quem lê.** Pergunte: "Quem lê o resumo e a fila de conferência, e em que horário?". Quem lê é o `responsavel_controladoria`; quem faz a segunda conferência é o `quem_confere`.

**Passo 4. Janelas.** Mostre o padrão (semana de 5 dias úteis, audiências e perícias de 15 dias corridos) e pergunte: "Essas janelas servem para vocês?". Grave na ficha da automação.

**Passo 5. Conectores.** Se houver (`conectores_no_claude`), combine só leitura: e-mail do tribunal para a entrada, agenda para sugerir horário. O ciclo nunca entra em sistema de tribunal.

**Passo 6. Escolher o jeito de rodar.** Pergunte: "Você usa o Claude no Cowork, no Claude Code ou no chat com Projeto?".
- **Cowork ou Claude Code, com tarefas agendadas:** preencha `assets/tarefa-agendada.md`, seção 1, e entregue as duas tarefas para colar. Elas chamam `/motor-controladoria:ciclo`. Conferir na configuração da conta o nome do recurso, se precisa do computador ligado e se enxerga a pasta.
- **Cowork ou Claude Code, sem tarefa agendada:** o comando duas vezes por dia, por alguém com dono.
- **Chat com Projeto:** o ciclo à mão, com o pedido pronto para colar (seção 3 do asset).

**Passo 7. Conferir o que o agente precisa.** O `agente-de-controladoria` espera: os dois registros com a linha de títulos de `prazos.md`; a entrada; os calendários e a tabela de regras; o registro de uso em `05-automacoes/ciclo-da-controladoria/registro-de-uso.md`; este script, em `scripts/pendencias_controladoria.py`; o modelo `assets/modelo-do-resumo.md`; e as habilidades que ele chama (`captar-publicacoes`, `triar-publicacoes`, `calcular-prazo`, `agenda-de-prazos`, `encaminhar-providencia`). O que faltar vai para o resumo como "o que não deu para fazer".

**Passo 8. Gravar.** Preencha `assets/ficha-da-automacao.md` e `assets/registro-de-uso.md` e grave em `escritorio/05-automacoes/ciclo-da-controladoria/`. No "Quando não roda", cole o plano combinado de `references/quando-a-rotina-nao-roda.md`, seção 3. Mostre antes de gravar.

**Passo 9. Rodar a primeira vez.** Rode o ciclo agora, para a pessoa ver o resumo antes da primeira manhã. Sem publicação real ainda: o treino (seção 5).

**Passo 10. Aprender**, como no ciclo à mão.

### Modo ciclo com agente

O `agente-de-controladoria` faz o ciclo com os passos do arquivo dele; o `revisor-de-controladoria` refaz cada conta e confere o trecho literal; o comando `ciclo` fecha o resumo com a linha da revisão. Esta habilidade não substitui o agente: configura, explica e é o plano B. Na primeira semana, leia os resumos com a pessoa e ajuste as janelas.

### Modo ciclo à mão

Os mesmos passos do agente, mostrados à pessoa, com o ok antes de gravar.

1. **Desde quando.** Leia o registro de uso e ache a última rodada completa (nem `não rodou` nem `só o resumo`). Sem registro: o dia útil anterior, e avise. Todo arquivo que ainda está em `entrada/` é lido, de qualquer data.
2. **PESSOA AGORA do último resumo.** Para cada item, pergunte: "O que foi feito ou decidido?". Com a resposta, atualize o registro só no que a pessoa disse e grave no item a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM`. Sem resposta, o item continua no topo.
3. **Captar.** Pela `captar-publicacoes` (se instalada): DJEN pelas OABs da ficha desde o dia seguinte à última rodada (sem internet, registre "DJEN não consultado" e siga), a entrada e o registro dos painéis do dia. Sem ela: peça a planilha ou o e-mail e normalize para as colunas de `prazos.md`. O teor vai para `publicacoes/AAAA-MM-DD/<id>.md`, com a data da captação na pasta (o script usa essa data para achar a captação com atraso).
4. **Tirar as duplicadas.** Mesmo processo, mesma data e mesmo teor: `duplicada`, apontando no `resumo` para o id original.
5. **Triar** pela `triar-publicacoes` (se instalada): tipo do ato, triagem, código do caso pela carteira, trecho literal. Processo que não está em nenhum registro: `sem-caso`, para a pessoa. Prazo da outra parte: `ciencia`, sem linha de prazo.
6. **Calcular** pela `calcular-prazo` (se instalada) o que tem triagem `prazo`: dias do ato ou da tabela do escritório (sem um dos dois, `[A CONFIRMAR: quantos dias]`), rito, regra, calendário do tribunal. Linha nova em `prazos.csv` com `status = sugerido` e `calculado_por = ia`. Audiência, perícia e sessão entram com o `tipo` próprio e a data do ato. Na dúvida entre duas datas, a mais cedo.
7. **Revisar.** Aplique a tabela de doze perguntas de `agents/revisor-de-controladoria.md` a cada item, refazendo a conta pelo script da `calcular-prazo`, e mostre o veredito ao lado (ok, ajustado, conferir, bloqueado). Na dúvida entre ok e conferir, conferir.
8. **Gravar a fila** em `07-operacao/controladoria/fila/AAAA-MM-DD/`: `NN-<codigo>-prazo.md` (`item: conferir-prazo`), `NN-<codigo>-providencia.md` (`item: decidir-providencia`) e `NN-aviso-<assunto>.md` (`item: aviso`), no formato de `agentes-e-fila.md`, com o trecho literal, a conta e as dúvidas em `antes_de_enviar`.
9. **Agendar só o conferido** pela `agenda-de-prazos` (se instalada). **Encaminhar só o decidido** pela `encaminhar-providencia` (se instalada). Sem elas, mostre o texto do compromisso ou do pedido para a pessoa copiar.
10. **Resumir.** Rode o script (seção 4) e monte o resumo no formato de `assets/modelo-do-resumo.md`, com "Comece por aqui" no topo (no máximo cinco ações) e a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados". Grave em `07-operacao/controladoria/rotina/AAAA-MM-DD.md`; na segunda rodada do dia, acrescente uma seção com a hora.
11. **Registrar** a rodada no registro de uso, com `à mão`.
12. **Aprender.** Pergunte: "Alguma coisa nesse resumo não devia estar aí, ou faltou alguma?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md` (`../../docs/aprender-com-o-uso.md`). Se muda uma janela, atualize a ficha da automação, com linha no histórico.

### Modo só o resumo
Rode o script, mostre o resultado com "Comece por aqui" e grave com o ok. No registro de uso a linha é `só o resumo`, que não conta como rodada completa. Depois, **Aprender**, como no passo 12.

### Modo não rodou
1. Leia o registro de uso e a pasta `rotina/` e diga desde quando não há ciclo (o script avisa quando passa de dois dias úteis).
2. Aponte a causa provável pela tabela de `references/quando-a-rotina-nao-roda.md`, seção 2.
3. Rode o ciclo à mão agora, com a captação desde a última rodada completa. O que já corria aparece como "captada com atraso" em PESSOA AGORA.
4. Registre as rodadas faltantes como `não rodou`, com a causa.
5. **Aprender.** Pergunte: "O que fez o ciclo não rodar, e o que muda para não se repetir?". A resposta vira ajuste no plano da ficha da automação e, se for regra de uso, aprendizado com o ok.

### Modo adaptar
1. Leia `nicho.md`, a ficha da controladoria (`tribunais`, `horario_da_captacao`, `regras_proprias`) e os aprendizados.
2. Proponha as janelas e o que entra no resumo no jeito do escritório (por exemplo, audiências com janela maior para quem faz muita perícia; recurso também na agenda do sócio, se for regra própria). Marque cada mudança `[ALTERADO]`.
3. Com o ok, grave na ficha da automação e no texto da tarefa agendada. Devolva à `adaptar-controladoria` uma linha de `prazos.csv` real anonimizada por status, para os casos de teste do escritório.

## 4. O script de pendências

Rode com o caminho da pasta desta habilidade e o dos registros como argumentos. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/rotina-da-controladoria`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-da-controladoria/scripts/pendencias_controladoria.py" \
  "escritorio/07-operacao/controladoria/prazos.csv" \
  --publicacoes "escritorio/07-operacao/controladoria/publicacoes.csv" --data AAAA-MM-DD
```

Sem `${CLAUDE_PLUGIN_ROOT}`, troque pelo caminho da pasta desta habilidade. Outras opções: `--calendario` (arquivo ou pasta; padrão `escritorio/04-base/controladoria/calendario/`), `--feriados` (o campo `feriados_e_recessos` da ficha, como está), `--semana N` (dias úteis, padrão 5), `--audiencias N` (dias corridos, padrão 15), `--registro-de-uso`, `--ultima-rodada AAAA-MM-DD`, `--fila`, `--saida`, `--treino` (obrigatório para ler `_treino/`). `--help` mostra tudo.

### 4.1 O que o script lê

Csv de vírgula ou ponto e vírgula, com ou sem BOM, em UTF-8 ou no padrão do Excel, a linha `sep=;`, datas AAAA-MM-DD ou DD/MM/AAAA, status, tipo e triagem sem diferenciar maiúscula nem acento ("Conferido" vale `conferido`). Colunas obrigatórias do `prazos.csv`: `id`, `codigo_caso`, `tipo`, `vencimento`, `data_seguranca`, `responsavel`, `status`, `atualizado_em`; do `publicacoes.csv`: `id`, `disponibilizada_em`, `tribunal`, `triagem`. Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio, falta coluna obrigatória, a data é inválida ou recebe o registro de treino sem `--treino`. Registro só com a linha de títulos não é erro, mas o resumo diz que nada foi lido. Nunca diz que está tudo em dia sem ter lido linhas.

O tribunal de cada prazo vem da publicação ligada (`publicacao_id`) e, sem ela, do número do processo (segmento da Justiça e tribunal). O "próximo dia útil" pula fins de semana e os dias de `feriado`, `recesso` e `suspensao` do calendário que valem para aquele tribunal. Indisponibilidade programada e expediente reduzido não contam como dia sem expediente: na dúvida, a data mais cedo. Sem calendário, o aviso sai em destaque no topo.

### 4.2 O que o script aponta

| Seção | Entra | Critério |
|---|---|---|
| PESSOA AGORA | Segurança ou fatal vencida, de hoje ou do próximo dia útil (em `sugerido`, `conferido` ou `agendado`); audiência ou perícia hoje ou no próximo dia útil; prazo sem data calculada; divergência da dupla conferência sem decisão com a data mais cedo a 2 dias úteis ou menos (nunca na agenda antes de `conferido`); captada com atraso (o `inicio` é anterior à data da captação, tirada da pasta do teor ou da coluna `captada_em`, se existir); ciência tácita de intimação de portal em até 2 dias úteis; `conferido` ou `agendado` sem os dois nomes em `conferido_por`; publicação `urgente` ou `sem-caso` com `triada_por` vazio ou `ia` | Primeiro o que vence, depois o que falta calcular, depois atraso, ciência tácita e conferência incompleta, por último o sem caso |
| PARA DECIDIR | Divergência anotada na `observacao`; prazo sem número de dias; item da fila pendente há mais de um dia útil, providência a decidir, bloqueado | Uma linha cada |
| Vence na semana | Segurança ou fatal nos próximos N dias úteis | Por data, com o status por extenso |
| Esperando a dupla conferência | Todos os `sugerido` | Do mais antigo; "sugerido há N dias úteis" quando passa de um |
| Publicações sem caso | `sem-caso` sem decisão de uma pessoa | Com a pergunta para a pessoa |
| Audiências e perícias | `audiencia`, `pericia`, `sessao` nos próximos 15 dias; as novas desde a última rodada | Por data |
| Agenda | `conferido` ainda sem agenda; prazos em aberto sem responsável | Lista |
| O que não deu para fazer | Não triadas por fonte; triada como prazo sem linha em `prazos.csv`; registro a corrigir (id repetido, status ou tipo fora da lista, data ilegível, segurança depois da fatal, `prazo-material` no registro, cumprido sem data, audiência que passou sem registro); avisos de calendário | Lista |
| Desde a última rodada | Publicações novas por fonte, prazos atualizados por status, a fila | Contagens e o aviso de dois dias úteis sem ciclo |

`cumprido`, `perdido` e `cancelado` ficam fora das listas, menos no registro a corrigir. Sem Python, aplique à mão as mesmas regras, nesta ordem, e diga que foi à mão.

## 5. Exemplo resolvido (treino com os casos fictícios)

Copie `assets/prazos-de-treino.csv` e `assets/publicacoes-de-treino.csv` para `escritorio/07-operacao/_treino/controladoria/rotina-da-controladoria/` com os nomes `prazos.csv` e `publicacoes.csv`. São os registros do lote de 2026-04-14 de `casos-ficticios.md` depois da triagem e da conta, com tudo `sugerido`. Rode na terça, 2026-04-14:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-da-controladoria/scripts/pendencias_controladoria.py" \
  "escritorio/07-operacao/_treino/controladoria/rotina-da-controladoria/prazos.csv" \
  --publicacoes "escritorio/07-operacao/_treino/controladoria/rotina-da-controladoria/publicacoes.csv" \
  --data 2026-04-14 --ultima-rodada 2026-04-08 --treino
```

No treino, o script usa o calendário de treino da `calendario-forense` (se instalada), com o feriado inventado de 2026-04-16. O que tem que sair:
- **PESSOA AGORA:** a Camila (PZ-2026-0003, recurso ordinário, segurança 2026-04-22, fatal 2026-04-24), captada com atraso, com 2 dias úteis já corridos; o Paulo (PZ-2026-0006), com a ciência tácita da intimação do portal em 2026-04-16; a publicação sem caso da Rosângela (PUB-2026-00007), com a pergunta para a pessoa.
- **Fora de PESSOA AGORA:** o Otávio (PZ-2026-0001, fatal sugerida 2026-04-30, segurança 2026-04-28), a Renata (2026-04-22 e 2026-04-24) e a Marta (2026-05-07 e 2026-05-11), todos em "Esperando a dupla conferência".
- **Vence na semana:** Camila, Renata e Paulo, todos com "sugerido, sem dupla conferência (ainda não vale)".
- **Audiências:** a do Paulo em 2026-05-20, como nova desde a última rodada, fora da janela de 15 dias.
- **Nenhuma linha** para as publicações 5, 6 e 9 (prazo do INSS, duplicada e RPV).

Rode de novo com `--data 2026-04-20`: o próximo dia útil é 2026-04-22 (2026-04-21 é Tiradentes) e Camila, Renata e Paulo entram em PESSOA AGORA pela data de segurança. Sem calendário (`--calendario` apontando para uma pasta vazia), o próximo dia útil vira 2026-04-21, Renata e Paulo somem de PESSOA AGORA (a Camila fica só pela captação com atraso) e o aviso em destaque explica por quê: é o teste de que o calendário faz falta.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Resumo do dia | `escritorio/07-operacao/controladoria/rotina/AAAA-MM-DD.md` |
| Itens do ciclo à mão | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/` |
| Ficha da automação, com o plano para quando não roda | `escritorio/05-automacoes/ciclo-da-controladoria/ficha.md` |
| Registro de uso (uma linha por rodada) | `escritorio/05-automacoes/ciclo-da-controladoria/registro-de-uso.md` |
| Texto das duas tarefas agendadas | No chat, para colar no recurso de tarefas agendadas |
| Linhas dos registros | `publicacoes.csv` e `prazos.csv`, só com o ok e só o que `prazos.md` (regra 5) permite |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-controladoria.md` |

O ciclo à mão cria linhas e mexe só em `nao-triada`, na triagem sugerida, no status `sugerido` e no `agendado` de quem já está `conferido`, e nas colunas `atualizado_em` e `observacao`. Sem pasta aberta: o resumo e os itens vêm no chat, e as linhas dos registros como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** o resumo da manhã é a pauta. Cinco minutos com PESSOA AGORA e "Esperando a dupla conferência" dizem o que conferir e o que cumprir. A segunda conferência é da mesma pessoa em outro turno: a rodada da tarde é um bom horário para ela. Em dia de audiência fora, o ciclo da tarde roda à mão no celular, com o modo só o resumo.

**Equipe:** quem capta e tria (`responsavel_controladoria`) lê o resumo inteiro e faz a primeira conferência; quem confere (`quem_confere`) recebe a fila; quem decide a providência recebe PARA DECIDIR. Se o mesmo nome aparece em quase tudo em "Vence na semana", aponte: ali está o gargalo, e a `painel-da-controladoria` (se instalada) mostra a carga. Uma pessoa é dona da ficha da automação.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Prazo de amanhã descoberto amanhã | Recurso às pressas, sem conferência | PESSOA AGORA até o próximo dia útil do tribunal, em qualquer status |
| Feriado do tribunal ignorado | O prazo de depois de amanhã some da lista | Calendário por tribunal; sem ele, aviso em destaque |
| Ciclo que parou e ninguém viu | Publicação chega com dias já corridos | "Captada com atraso" em PESSOA AGORA e aviso de dois dias úteis sem ciclo |
| Prazo sugerido tratado como certo | Agenda com data que ninguém conferiu | "Sugerido, sem dupla conferência" em toda linha; nada sugerido na agenda |
| Agendado sem dupla conferência | Um erro de conta vira compromisso | Conferido ou agendado sem os dois nomes vai para PESSOA AGORA |
| Publicação sem caso esquecida | Processo de cliente antigo sem ninguém olhar | Sem caso sem decisão vai para PESSOA AGORA |
| Script sem arquivo dizendo que está tudo em dia | A equipe confia num resumo que não leu nada | Código 1 e "ERRO:"; seção vazia diz quantas linhas leu |
| Planilha do Excel não lida | Resumo vazio sem motivo | Leitura robusta de separador, BOM, acento, data e maiúscula |
| Treino no resumo real | Equipe cobrando prazo que não existe | `--treino` obrigatório para `_treino/` |

## 9. Próximo passo

- PESSOA AGORA e os sugeridos: a `dupla-conferencia` ou o `/motor-controladoria:fila`, que grava a decisão.
- Conferido sem agenda: `agenda-de-prazos` (se instalada; sem ela, o texto do compromisso para a pessoa lançar).
- Providência a decidir: `encaminhar-providencia` (se instalada).
- Publicação sem caso: a pessoa responde; com a resposta, a `triar-publicacoes` liga ao caso ou marca como erro.
- Sem calendário do ano: `calendario-forense`.
- Carga por responsável: `painel-da-controladoria` (se instalada). Férias à vista: `cobertura-de-ausencia` (se instalada).

## Referências desta habilidade

- `scripts/pendencias_controladoria.py`: o script de pendências (só biblioteca padrão). Rode no passo 10 do ciclo à mão e no modo só o resumo. O `agente-de-controladoria` e o `/motor-controladoria:status` usam o mesmo script.
- `assets/modelo-do-resumo.md`: o formato do resumo do dia, com as seções fixas. Use no passo 10.
- `assets/tarefa-agendada.md`: as duas tarefas agendadas, o comando, o ciclo à mão e o que vai para a entrada. Use no passo 6 do configurar.
- `assets/ficha-da-automacao.md`: modelo da ficha da automação. Use no passo 8 do configurar.
- `assets/registro-de-uso.md`: modelo do registro de uso, com os valores de "Como rodou". Use no passo 8 do configurar.
- `assets/prazos-de-treino.csv` e `assets/publicacoes-de-treino.csv`: os registros do lote de treino depois da triagem e da conta. Use na seção 5.
- `references/quando-a-rotina-nao-roda.md`: sinais, causas, o plano combinado e o que nunca fazer para compensar. Leia no configurar e no modo não rodou.
