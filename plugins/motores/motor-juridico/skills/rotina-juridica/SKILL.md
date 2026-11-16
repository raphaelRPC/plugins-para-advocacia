---
name: rotina-juridica
description: >
  O motor da produção jurídica. Configura e explica o ciclo do dia: o agente do plugin pelo
  comando /motor-juridico:ciclo, a tarefa agendada que chama esse comando (texto pronto), o
  "ciclo à mão" no chat quando não há agente, e o resumo do dia pelo script de pendências sobre o
  pecas.csv (prazos internos de hoje e amanhã sem minuta aprovada, peças paradas por etapa,
  citações não verdes, dados com alerta, aprovadas sem protocolo, peças esperando tese, registro
  a corrigir). Grava a ficha da automação, o registro de uso e o plano para quando não roda. Use
  quando o advogado disser "configura o ciclo das peças", "quero a produção rodando sozinha",
  "roda as peças de hoje à mão", "o que está parado", "o que vence amanhã", "o ciclo não rodou".
  Não use para minutar uma peça (use minutar-peca) nem para conferir citações de uma minuta (use
  conferir-citacoes).
---

# Rotina jurídica

> Todo dia, no mesmo horário, o advogado precisa saber que peça vence amanhã sem minuta aprovada, qual espera a decisão dele e o que está aprovado sem protocolo. O ciclo lê, separa, prepara e confere. O advogado decide, assina e protocola.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e registro de peças: `../../docs/producao.md`. Ciclo, agente, revisor e fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quinta, 8h. A petição inicial da Marta tem prazo interno amanhã. A minuta existe, mas a conferência deu uma súmula vermelha e um nome de outro cliente no item 4 dos fatos. O estagiário acha que está pronta; a advogada acha que ainda nem chegou. O resumo do dia põe a Marta no topo, em ADVOGADO AGORA, com o motivo em uma linha, e as duas pessoas leem a mesma coisa.

**Regras fixas desta habilidade:**
1. O ciclo prepara e aponta. Não protocola, não assina, não escolhe tese e só mexe no `pecas.csv` dentro do que `producao.md` permite (regra 5).
2. ADVOGADO AGORA vem antes de tudo: prazo interno vencido, de hoje ou de amanhã sem minuta aprovada, peça esperando tese, minuta sem tese, peça revisada ou aprovada com citação ou dado pendente.
3. Sem tese definida pelo advogado, não há minuta. Há dossiê e estratégia para ele decidir.
4. Prazo interno é o que alguém informou. A rotina ordena a fila por ele e nunca calcula prazo processual (isso é da controladoria).
5. Treino nunca entra no resumo real. No resumo, só id, código, primeiro nome, área, peça e etapa.

## 1. Quando usar

**Use quando:**
- O escritório quer a produção rodando todo dia sem ninguém pedir (modo configurar).
- Não há agente (chat com Projeto) e alguém quer o ciclo de hoje (modo ciclo à mão).
- O `/motor-juridico:ciclo` não achou o agente e caiu aqui (modo ciclo à mão, com a revisão pela tabela de `agents/revisor-juridico.md`).
- Alguém quer só a lista do que está pendente agora (modo só o resumo).
- O `/motor-juridico:status` mostrou que o ciclo não roda há dias (modo não rodou).

**Não use quando:**
- O pedido é minutar uma peça com a tese já definida: `minutar-peca` (se instalada; sem ela, o advogado minuta a partir do modelo do escritório).
- O pedido é conferir as citações ou os dados de uma minuta: `conferir-citacoes` e `conferir-peca`.
- O pedido é controlar prazo processual ou publicação: é da controladoria do escritório, fora deste plugin.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`), `nicho.md` se existir e os aprendizados (`aprendizados-juridico.md`). Se existir, leia a ficha da automação (`escritorio/05-automacoes/ciclo-juridico/ficha.md`): os limites de etapa dela valem para o ciclo.
2. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Quem faz a primeira minuta e quem revisa?", depois "Que horas o resumo do dia precisa estar pronto?".
3. **Leia o registro** (`escritorio/07-operacao/juridico/pecas.csv`). Sem registro, o ciclo pode ser configurado mesmo assim: o agente cria o arquivo só com a primeira linha de `producao.md`.
4. **Onde roda** (`onde_roda`): Cowork ou Claude Code têm o comando e o agente; o chat com Projeto, só o ciclo à mão. Conferir na configuração da conta se agentes de plugin e tarefas agendadas estão disponíveis.
5. **Conta de IA.** O ciclo lê documentos de caso. Em conta pessoal, só os casos fictícios. Dado de saúde, de criança ou de processo em segredo de justiça só com autorização expressa do advogado responsável (`regras.md`, seção 6).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `horario_da_rotina_diaria` · J: `quem_redige`, `quem_revisa` |
| Melhora | E: `onde_roda`, `quem_aprova_rascunhos`, `conectores_no_claude` |

Também lê, se preenchido, E: `feriados_e_recessos`, para contar dias úteis no script. Campo que falta e o ciclo precisa: pergunte aquele campo, uma vez, e ofereça gravar na ficha e na ficha da automação.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Configurar | Primeira vez | O jeito de rodar escolhido, a tarefa agendada pronta (se houver), ficha da automação, registro de uso, primeiro ciclo |
| Ciclo com agente | Cowork ou Claude Code | O `agente-juridico` roda; esta habilidade explica e confere o que ele precisa |
| Ciclo à mão | Chat com Projeto, ou o agente falhou | O mesmo ciclo, passo a passo, mostrado e gravado com o ok |
| Só o resumo | "o que está pendente?" | O resumo do script, sem análise nem minuta |
| Não rodou | Faltou o resumo do dia | A causa provável, o ciclo de hoje e o ajuste do plano |
| Treino | Casos fictícios ou "é teste" | O resumo do `assets/pecas-de-treino.csv`, gravado em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Limites de etapa e o pedido de peça no jeito do escritório, para aprovar |

Pedido direto ("o que vence amanhã?"): não faça entrevista. Rode o script e mostre.

### Modo configurar

**Passo 1. Conferir as fontes.** Veja se existem `pecas.csv`, `entrada/`, `casos/`, `fila/` e `rotina/` em `escritorio/07-operacao/juridico/`. Mostre em duas linhas o que o ciclo vai ler e o que falta; crie as pastas que faltam com o ok.

**Passo 2. Combinar a entrada.** Pergunte: "Quem avisa que uma peça foi pedida, e como?". O ciclo não lê o sistema do tribunal nem a controladoria: lê o que alguém solta em `entrada/` (o pedido de peça, no formato de `assets/tarefa-agendada.md`, seção 4), as passagens do motor-comercial (se instalado) e o `pecas.csv`.

**Passo 3. Combinar o horário e quem lê.** Pergunte: "Que horas você quer o resumo pronto?" e depois "Quem lê a fila de minutas, e em que horário?". Sugestão: antes da primeira audiência do dia. As respostas vão para `horario_da_rotina_diaria` e `quem_aprova_rascunhos`.

**Passo 4. Limites de etapa.** Mostre os limites padrão do script (seção 4.1) e pergunte: "Quantos dias úteis uma peça pode ficar em análise antes de virar alerta?". Ajuste os outros só se o advogado quiser. Grave na ficha da automação.

**Passo 5. Conectores.** Se houver (`conectores_no_claude`), combine só leitura: e-mail para pedidos de peça, pasta de arquivos para os documentos do caso. O ciclo nunca entra em sistema de tribunal.

**Passo 6. Escolher o jeito de rodar.** Pergunte: "Você usa o Claude no Cowork, no Claude Code ou no chat com Projeto?".
- **Cowork ou Claude Code, com tarefas agendadas:** preencha `assets/tarefa-agendada.md`, seção 1, e entregue para colar no recurso de tarefas agendadas. A tarefa chama `/motor-juridico:ciclo`. Conferir na configuração da conta o nome do recurso, se precisa do computador ligado e se enxerga a pasta.
- **Cowork ou Claude Code, sem tarefa agendada:** o comando `/motor-juridico:ciclo` todo dia no horário combinado, por alguém com dono.
- **Chat com Projeto:** o ciclo à mão, com o pedido pronto para colar (seção 3 do asset).

**Passo 7. Conferir o que o agente precisa.** O `agente-juridico` espera: o `pecas.csv` com a primeira linha de `producao.md`; a pasta `entrada/` com pedidos no formato combinado; `casos/<codigo>/` para dossiê, estratégia, minutas, conferências e protocolo; o registro de uso em `05-automacoes/ciclo-juridico/registro-de-uso.md`; o resumo em `rotina/AAAA-MM-DD.md` no formato de `assets/modelo-do-resumo.md`; e as habilidades que ele chama (`dossie-do-caso`, `estrategia-do-caso`, `minutar-peca`, `conferir-citacoes`, `conferir-peca`, e as do completo, se instaladas). O que faltar vai para o resumo como "o que não deu para fazer".

**Passo 8. Gravar.** Preencha `assets/ficha-da-automacao.md` e `assets/registro-de-uso.md` e grave em `escritorio/05-automacoes/ciclo-juridico/`. No "Quando não roda" da ficha, cole o plano combinado de `references/quando-a-rotina-nao-roda.md`, seção 3. Mostre antes de gravar.

**Passo 9. Rodar a primeira vez.** Rode o ciclo agora (comando ou à mão), para o advogado ver o resumo antes da primeira manhã. Sem peça real ainda: rode o treino (seção 5).

**Passo 10. Aprender**, como no ciclo à mão.

### Modo ciclo com agente

O `agente-juridico` faz o ciclo de `agentes-e-fila.md` com os passos do arquivo dele; o `revisor-juridico` confere cada item com `revisor: pendente`; o comando `ciclo` fecha o resumo com a linha da revisão. Esta habilidade não substitui o agente: configura, explica e é o plano B. Na primeira semana, leia os resumos com o advogado e ajuste os limites de etapa.

### Modo ciclo à mão

Os mesmos passos do agente, mostrados ao advogado, com o ok antes de gravar.

1. **Desde quando.** Leia o registro de uso e ache a última rodada completa (nem `não rodou` nem `só o resumo`). Sem registro: o dia anterior, e avise. Todo arquivo que ainda está em `entrada/` é lido, de qualquer data.
2. **ADVOGADO AGORA do último resumo.** Para cada item, pergunte: "O que você decidiu?" (a tese, o caminho, se aceita o caso). Com a resposta, grave a decisão em `casos/<codigo>/estrategia.md` e, se for o caso, a etapa `tese-definida` ou `suspensa` no `pecas.csv`, que só o advogado move. Sem resposta, o item fica no topo.
3. **Coletar.** Pedidos novos em `entrada/`, passagens em `07-operacao/comercial/passagens/` (se o motor-comercial estiver instalado) e as linhas abertas do `pecas.csv`. Sem pasta: peça o pedido e o registro colados (`assets/tarefa-agendada.md`, seção 3). Depois de lido, o arquivo vai para `entrada/lidos/AAAA-MM-DD/`. Mover não é apagar.
4. **Separar o que é do advogado agora.** Prazo interno de hoje ou de amanhã sem minuta; pedido que envolve escolher tese; caso novo com parte que pode dar conflito (`conflito-de-interesses`, se instalada; sem ela, pergunte ao advogado se alguma parte já foi cliente); dado sensível que não deveria estar no material. Uma frase do porquê e nada de minuta para esses.
5. **Analisar o que chegou.** Caso novo com documentos: `dossie-do-caso`. Processo em andamento recebido inteiro: `leitura-dos-autos` (se instalada; sem ela, o dossiê com os autos como documentos). Caso sem estratégia: rascunho da `estrategia-do-caso`, que termina numa pergunta ao advogado. Linha nova com etapa `pedida` ou `em-analise`.
6. **Minutar só o que tem tese definida.** Para cada peça em `tese-definida`: a habilidade própria do escritório para aquela peça, se existir em `04-base/habilidades-do-escritorio/`; senão, a `minutar-peca`. Toda citação sai marcada (`citacoes.md`). Etapa `minuta`.
7. **Conferir.** Em cada minuta: `conferir-citacoes` e `conferir-peca`, com o relatório em `casos/<codigo>/conferencias/`. O que não está conferido fica marcado e entra em "pesquisar no Jus IA" no resumo. Só com citações verdes e dados ok a etapa vai a `conferida`.
8. **Preparar protocolo** das `aprovadas`: o checklist da `preparar-protocolo` (se instalada; sem ela, a pessoa que protocola confere a peça final, os documentos e a ordem pela ficha). Nunca protocolar.
9. **Revisar.** Aplique a tabela de dez perguntas de `agents/revisor-juridico.md` a cada item, uma a uma, e mostre o veredito ao lado (ok, ajustado, conferir, bloqueado). Na dúvida entre conferir e bloqueado, bloqueie.
10. **Gravar a fila** em `07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-<peca>.md`, no formato de `agentes-e-fila.md`, com o relatório de conferência em `antes_de_enviar` e o caminho da minuta. E as linhas do registro, só nas colunas e etapas que `producao.md` (regra 5) permite.
11. **Resumir.** Rode o script (seção 4) e monte o resumo no formato de `assets/modelo-do-resumo.md`, com "Comece por aqui" no topo (no máximo cinco ações) e a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados". Grave em `07-operacao/juridico/rotina/AAAA-MM-DD.md`; se já existir, acrescente uma seção com a hora.
12. **Registrar** a rodada no registro de uso, com `à mão`.
13. **Aprender.** Pergunte: "Alguma coisa nesse resumo não devia estar aí, ou faltou alguma?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Se muda um limite de etapa, atualize a ficha da automação, com linha no histórico.

### Modo só o resumo
Rode o script, mostre o resultado com "Comece por aqui" e grave com o ok. No registro de uso a linha é `só o resumo`, que não conta como rodada completa.

### Modo não rodou
1. Leia o registro de uso e a pasta `rotina/` e diga desde quando não há ciclo (o script avisa quando passa de dois dias úteis).
2. Aponte a causa provável pela tabela de `references/quando-a-rotina-nao-roda.md`, seção 2.
3. Rode o ciclo à mão com a data de hoje. O que venceu aparece como vencido.
4. Registre os dias faltantes como `não rodou`, com a causa.
5. **Aprender.** Pergunte: "O que fez o ciclo não rodar, e o que muda para não se repetir?". A resposta vira ajuste no plano da ficha da automação e, se for regra de uso, aprendizado com o ok.

### Modo adaptar
1. Leia `nicho.md`, a ficha jurídica (`pecas_mais_feitas`) e os aprendizados.
2. Proponha os limites de etapa para as peças do escritório (peça em massa pode ter limite menor; recurso com tese nova, maior) e o pedido de peça com os campos que o escritório usa. Marque cada mudança `[ALTERADO]`.
3. Com o ok, grave na ficha da automação e no `assets/tarefa-agendada.md` preenchido. Devolva à `adaptar-juridico` uma linha de `pecas.csv` real anonimizada por etapa, para os casos de teste do escritório.

## 4. O script de pendências

Rode com o caminho da pasta desta habilidade e o do csv como argumentos. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/rotina-juridica`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-juridica/scripts/pendencias_juridicas.py" \
  "escritorio/07-operacao/juridico/pecas.csv" --data AAAA-MM-DD \
  --feriados "2026-04-21, 2026-06-04" --parada "em-analise=5, minuta=2" \
  --registro-de-uso "escritorio/05-automacoes/ciclo-juridico/registro-de-uso.md" \
  --fila "escritorio/07-operacao/juridico/fila" --entrada "escritorio/07-operacao/juridico/entrada" \
  --casos "escritorio/07-operacao/juridico/casos"
```

Sem `${CLAUDE_PLUGIN_ROOT}`, troque pelo caminho da pasta desta habilidade. Outras opções: `--sabado` (sábado conta como dia útil), `--proximos N` (janela dos prazos, padrão 7 dias corridos), `--treino` (obrigatório para ler o registro de `_treino/`). `--help` mostra tudo.

### 4.1 O que o script lê

O script lê o csv de vírgula ou ponto e vírgula, com ou sem BOM, em UTF-8 ou no padrão do Excel, datas AAAA-MM-DD ou DD/MM/AAAA, e etapas e opções sem diferenciar maiúscula nem acento ("Em análise" vale `em-analise`). Colunas obrigatórias: `id`, `codigo_caso`, `peca`, `prazo_interno`, `etapa`, `citacoes`, `dados`, `atualizado_em`. Sai com código 1 e "ERRO:" quando falta o arquivo, ele está vazio, falta coluna obrigatória, a data é inválida ou recebe o registro de treino sem `--treino`. Nunca diz que não há nada a apontar sem ter lido.

| Opção | De onde vem | Formato |
|---|---|---|
| `--feriados` | E: `feriados_e_recessos` | O texto do campo como está: datas AAAA-MM-DD, DD/MM/AAAA ou DD/MM, e "de DD/MM a DD/MM". Vazio ou só `[A PREENCHER]`: ignorado, com aviso; só o fim de semana conta |
| `--parada` | Ficha da automação | `etapa=dias úteis`, separados por vírgula. Padrão: pedida 2, em-analise 5, tese-definida 2, minuta 2, conferida 2, revisada 1, aprovada 1 |

### 4.2 O que o script aponta

| Seção | Entra | Critério |
|---|---|---|
| ADVOGADO AGORA | Prazo interno vencido, de hoje ou até o próximo dia útil, em etapa antes de `aprovada`; `aprovada` com prazo agora; `em-analise` sem tese (com `--casos`, só quando existe `estrategia.md`); minuta sem tese registrada; `revisada` ou `aprovada` com citação não verde ou dado não ok; item da fila `pendente` há mais de um dia útil | Antes de tudo, por prazo. Uma linha por peça, com todos os motivos |
| 1. Prazos internos | Peças abertas com prazo nos próximos 7 dias | Por data; quantas estão sem prazo interno |
| 2. Por etapa | Todas | Quantas e o maior tempo na etapa |
| 3. Paradas | Dias úteis desde `atualizado_em` maiores que o limite da etapa | Por atraso |
| 4. Citações não verdes | `minuta` a `aprovada` com `citacoes` diferente de `verde` | Vermelho, não conferidas, amarelo, com o que fazer |
| 5. Dados com alerta | `minuta` a `aprovada` com `dados` diferente de `ok` | Alerta antes de não conferido |
| 6. Aprovadas sem protocolo | `aprovada` | Dias úteis desde a aprovação; com `--casos`, se o checklist de protocolo existe |
| 7. Esperando tese | `em-analise` sem tese | Estratégia pronta ou análise em andamento |
| 8. Registro a corrigir | Qualquer linha | id ou código fora do padrão, id repetido, etapa ou opção que não existe, data inválida, `conferida` com citação ou dado pendente, `protocolada` sem sistema, número ou data, número de processo antes do protocolo, tese anotada antes de `tese-definida`, peça aberta sem responsável |
| Fila, desde a última rodada, por responsável | `fila/`, `entrada/`, registro de uso | Contagens |

`protocolada` e `suspensa` ficam fora das listas, menos no registro a corrigir. Sem Python, aplique à mão as mesmas regras, nesta ordem.

## 5. Exemplo resolvido (treino com os casos fictícios)

Copie `assets/pecas-de-treino.csv` para `escritorio/07-operacao/_treino/juridico/rotina-juridica/pecas.csv` e rode lá (cada habilidade treina no seu próprio registro, para os treinos não se misturarem).

`assets/pecas-de-treino.csv` tem os três casos de `../../docs/casos-ficticios.md` em etapas diferentes: Marta (P-2026-0001, petição inicial, `minuta`, citações `com-vermelho` e dados `com-alerta`, como sai a minuta com erros), Paulo (P-2026-0002, reclamação trabalhista, `em-analise` desde 2026-04-08, sem tese) e Renata (P-2026-0003, divórcio consensual, `aprovada` em 2026-04-14). Copie para `escritorio/07-operacao/_treino/juridico/pecas.csv` e rode na quinta, 2026-04-16:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/rotina-juridica/scripts/pendencias_juridicas.py" \
  "escritorio/07-operacao/_treino/juridico/rotina-juridica/pecas.csv" --data 2026-04-16 --treino
```

O script devolve: ADVOGADO AGORA com Marta (prazo amanhã, minuta não aprovada) e Paulo (esperando a tese do advogado); paradas Renata (aprovada há 2 dias úteis) e Paulo (em análise há 6 dias úteis, limite 5); citação vermelha e dados com alerta da Marta; Renata em aprovadas sem protocolo; registro sem nada a corrigir.

O "Comece por aqui":
```
1. Corrigir a minuta da Marta · P-2026-0001 · estagiário e advogada · súmula vermelha, nome de outro cliente, prazo amanhã
2. Decidir a tese do Paulo · P-2026-0002 · advogada · antes, a checagem de conflito: o restaurante foi cliente
3. Protocolar o divórcio da Renata · P-2026-0003 · quem protocola · aprovada há 2 dias úteis
```

O item 2 mostra o ciclo separando o que é do advogado: no caso 2, a `conflito-de-interesses` (se instalada) acusa o Restaurante Sabor Mineiro, e a peça não anda até ele decidir.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Resumo do dia | `escritorio/07-operacao/juridico/rotina/AAAA-MM-DD.md` |
| Minutas e itens do ciclo à mão | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/` |
| Decisões do advogado sobre ADVOGADO AGORA | `escritorio/07-operacao/juridico/casos/<codigo>/estrategia.md` |
| Ficha da automação, com o plano para quando não roda | `escritorio/05-automacoes/ciclo-juridico/ficha.md` |
| Registro de uso (uma linha por rodada) | `escritorio/05-automacoes/ciclo-juridico/registro-de-uso.md` |
| Texto da tarefa agendada | No chat, para colar no recurso de tarefas agendadas |
| Linhas do registro | `escritorio/07-operacao/juridico/pecas.csv`, só com o ok e só o que `producao.md` permite |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-juridico.md` |

No `pecas.csv`, o ciclo cria linhas em `pedida` ou `em-analise`, move para `minuta` e `conferida`, e atualiza `citacoes`, `dados`, `responsavel` (se a ficha define) e `atualizado_em`. Nunca move para `tese-definida`, `revisada`, `aprovada`, `protocolada` ou `suspensa`. Sem pasta aberta: o resumo e os itens vêm no chat, e as linhas do registro como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** o resumo é a pauta da manhã. Cinco minutos com o "Comece por aqui" dizem o que decidir (tese), o que corrigir (vermelho) e o que protocolar. Em dia de audiência, o ciclo roda no almoço.

**Equipe:** quem redige (`quem_redige`) lê as paradas e as citações não verdes; quem revisa (`quem_revisa`) recebe ADVOGADO AGORA e a fila; quem protocola (`quem_protocola`) recebe as aprovadas. Se o mesmo nome aparece em quase tudo no "por responsável", aponte: ali está o gargalo. Uma pessoa é dona da ficha da automação.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Minuta pronta sem tese do advogado | A IA escolhe o caminho do caso | Sem `tese-definida`, só dossiê e estratégia; minuta sem tese vai para ADVOGADO AGORA |
| Peça aprovada com citação amarela | Citação errada no processo | Revisada ou aprovada sem verde vai para o topo |
| Prazo interno de amanhã descoberto amanhã | Minuta às pressas, sem conferência | ADVOGADO AGORA até o próximo dia útil, sexta pega segunda |
| Aprovada esquecida na pasta | Peça pronta perde o prazo interno | Seção de aprovadas sem protocolo, com dias úteis |
| Script sem arquivo dizendo que está tudo em dia | A equipe confia num resumo que não leu nada | Código 1 e "ERRO:" claro |
| Planilha do Excel não lida | Resumo vazio sem motivo | Leitura robusta de separador, BOM, acento, data e maiúscula |
| Número do processo no registro antes do protocolo | Dado a mais circulando | Registro a corrigir aponta |
| Treino no resumo real | Equipe cobrando peça que não existe | `--treino` obrigatório para `_treino/` |
| Ciclo que para e ninguém percebe | Peças acumulam em silêncio | Registro de uso, aviso de dois dias úteis e o plano da ficha |

## 9. Próximo passo

- ADVOGADO AGORA: o advogado decide pelo `/motor-juridico:fila`, que grava a decisão.
- Peça esperando tese: `estrategia-do-caso`, que termina na decisão registrada.
- Citações não verdes: `conferir-citacoes`; o que faltar vira pesquisa no Jus IA e volta pela `trazer-pesquisa`.
- Dados com alerta: `conferir-peca`.
- Aprovadas: `preparar-protocolo` (se instalada).
- Caso novo com partes: `conflito-de-interesses` (se instalada).

## Referências desta habilidade

- `scripts/pendencias_juridicas.py`: o script de pendências (só biblioteca padrão). Rode no passo 11 do ciclo à mão e no modo só o resumo. O `agente-juridico` usa o mesmo script.
- `assets/pecas-de-treino.csv`: o registro de treino com os três casos fictícios em etapas diferentes. Use na seção 5 e no passo 9 do configurar.
- `assets/tarefa-agendada.md`: a tarefa agendada que chama `/motor-juridico:ciclo`, o comando, o ciclo à mão e o formato do pedido de peça na entrada. Use no passo 6 do configurar.
- `assets/ficha-da-automacao.md`: modelo da ficha da automação. Use no passo 8 do configurar.
- `assets/registro-de-uso.md`: modelo do registro de uso, com os valores de "Como rodou". Use no passo 8 do configurar.
- `assets/modelo-do-resumo.md`: o formato do resumo do dia. Use no passo 11 do ciclo à mão.
- `references/quando-a-rotina-nao-roda.md`: sinais, causas, o plano combinado e o que nunca fazer para compensar. Leia no configurar e no modo não rodou.
