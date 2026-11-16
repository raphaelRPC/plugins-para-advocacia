---
name: monitor-de-precedentes
description: >
  Vigia os temas da base de jurisprudência e as teses do escritório: um script lê a base e as
  teses e lista os temas com pesquisa ou conferência vencida, os precedentes qualificados a
  vigiar (súmulas, temas de repercussão geral e de repetitivo, IRDR, IAC), o que pesquisar de
  novo no Jus IA, as teses que podem estar afetadas e as peças em andamento que usam essas
  teses. Quando a pesquisa nova volta, compara com a base e diz se a tese pode ter sido afetada,
  para o advogado decidir. Roda a pedido, no ciclo e numa tarefa agendada semanal. Use quando o
  advogado disser "o que está vencido na base?", "algum precedente mudou?", "essa tese ainda
  vale?", "compara a pesquisa nova com o que a gente tinha", "liga o monitor toda semana". Não
  use para guardar a pesquisa na base (use trazer-pesquisa) nem para ver como o tema é decidido
  (use mapa-jurisprudencial).
---

# Monitor de precedentes

> A base do escritório envelhece em silêncio. O monitor avisa quando um tema precisa de pesquisa nova, quando um precedente qualificado precisa ser olhado de novo e quando uma peça em andamento usa uma tese que pode ter caído.

Base e pesquisa: `../../docs/pesquisa-jus-ia.md`. Regra de citação: `../../docs/citacoes.md`. Regras: `../../docs/regras.md`. Etapas e `pecas.csv`: `../../docs/producao.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 7h30. A petição da Marta está em minuta com a tese do restabelecimento. Na base, o julgado de 2023 da 1ª câmara, que sustentava metade da tese, foi conferido de novo na semana passada e saiu "superado". Ninguém ligou uma coisa à outra. O monitor liga: no resumo do dia, em ADVOGADO AGORA, aparece a peça, a tese e o julgado que caiu.

**Regras fixas desta habilidade:**
1. O monitor avisa; não decide. Mudar a tese, ajustar a peça, fazer a distinção ou suspender é do advogado.
2. O monitor não pesquisa de memória nem completa número de tema, súmula ou julgado: ele monta a lista do que pesquisar no Jus IA e do que conferir no portal do tribunal.
3. O monitor não muda a base, as teses nem o `pecas.csv`. Pesquisa nova entra pela `trazer-pesquisa`; conferência, pelo lote dela.
4. "Fora da pesquisa nova" não quer dizer "caiu": pode ser só o recorte da pesquisa.
5. Tudo o que é da base é do escritório; o relatório não leva dado de cliente além do código e do tipo de peça.

## 1. Quando usar

**Use quando:**
- O advogado quer saber o que está vencido na base e o que pesquisar de novo.
- Uma pesquisa nova voltou do Jus IA para um tema que já existe (modo "comparar").
- O `agente-juridico` chama no primeiro ciclo da semana (modo "no ciclo").
- O escritório quer a vigilância toda semana sem pedir (modo "agendado").
- Para treinar com a base de treino (modo "treino").
- A `adaptar-juridico` (se instalada) pediu a cadência e os temas prioritários (modo "adaptar").

**Não use quando:**
- O pedido é guardar uma pesquisa na base: `trazer-pesquisa` (se instalada; sem ela, monte as fichas no formato de `../../docs/pesquisa-jus-ia.md`).
- O pedido é ver como o tema é decidido: `mapa-jurisprudencial` (se instalada).
- O pedido é conferir as citações de uma peça: `conferir-citacoes`.
- O pedido é prazo processual ou publicação: é da controladoria, fora deste plugin.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-juridica.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`), em especial os do monitor (temas prioritários, cadência).
3. **Ache a base:** `escritorio/04-base/juridico/jurisprudencia/` (os temas) e `escritorio/04-base/juridico/teses/` (as teses, da `banco-de-teses-vivo`, se instalada). Sem temas, o monitor não tem o que vigiar: comece pela `trazer-pesquisa`.
4. **Ache o registro de peças:** `escritorio/07-operacao/juridico/pecas.csv` (formato em `../../docs/producao.md`). Sem ele, o monitor vigia a base, mas não cruza com as peças em andamento.
5. **Leia o último relatório** em `escritorio/07-operacao/juridico/precedentes/`, se existir, para dizer o que mudou desde a última rodada.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `validade_da_conferencia`, `pesquisa_de_jurisprudencia` |
| Melhora | E: `horario_da_rotina_diaria` |

`validade_da_conferencia` define o que está vencido (pesquisa e conferência); sem ele, 90 dias, e o relatório diz isso. `pesquisa_de_jurisprudencia` é o Jus IA. `horario_da_rotina_diaria` dá a hora da tarefa agendada (o monitor roda antes do ciclo). Na prática, o monitor também usa `tribunais_principais` (J) para a lista do que pesquisar, quando existe.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Vigiar | Pedido do advogado | A base, as teses e o `pecas.csv` | O relatório da seção 5, mostrado e gravado |
| Comparar | Pesquisa nova de um tema | O rascunho de fichas e o tema | A comparação e "a tese pode ter sido afetada?" |
| No ciclo | O `agente-juridico` chama | A base | Linhas para o resumo do dia e, se for o caso, um aviso na fila |
| Agendado | Tarefa semanal | A base | O relatório gravado e as linhas no resumo |
| Treino | Teste | `assets/treino/` | O relatório de treino em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Ficha e nicho | Cadência e temas prioritários, para aprovar |

### Passo 1. Rodar a vigilância
Rode o script da pasta desta habilidade, com o caminho da base:

```
python3 "<pasta desta habilidade>/scripts/monitor.py" vigiar escritorio/04-base/juridico \
  --saida escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/monitor-de-precedentes`. O script acha a ficha jurídica e o `pecas.csv` subindo a partir da base; `--validade`, `--ficha`, `--pecas` e `--hoje AAAA-MM-DD` valem por cima. Ele lê o `pecas.csv` com vírgula ou ponto e vírgula, com ou sem BOM, e etapas em maiúsculas. Sai com erro e uma mensagem clara quando falta a pasta, não há tema, ou o `pecas.csv` não tem as colunas `id`, `codigo_caso`, `peca`, `etapa` e `tese`, e sempre diz quantos temas, fichas e teses leu.

O que ele junta:
- **Teses ligadas a cada tema:** pelo campo `teses_do_escritorio` do tema e pelo nome do tema escrito no arquivo da tese.
- **Tese afetada:** um tema dela tem julgado a favor que ficou vermelho ou superado.
- **Tese a olhar:** um tema dela tem pesquisa vencida, ou precedente qualificado sem conferência.
- **ADVOGADO AGORA:** peça em etapa aberta (de `pedida` a `aprovada`) com tese afetada ou a olhar.
- **Pesquisar de novo no Jus IA:** cada tema com a última pesquisa vencida (com a data de corte e os tribunais), e cada precedente qualificado (situação atual no portal do tribunal).
- **Lote de conferência:** julgados não conferidos, com conferência vencida ou amarelos.

Sem o script (chat sem arquivos): faça a mesma leitura à mão, tema por tema, e diga que foi à mão.

### Passo 2. Ler o relatório
Comece por ADVOGADO AGORA e pelas teses afetadas. Para cada uma, escreva em uma frase o que caiu e onde a tese é usada. Compare com o relatório anterior: o que é novo nesta rodada.

### Passo 3. Mostrar
Mostre o relatório (seção 5) e pergunte: "Quer que eu prepare a lista do Jus IA para você pesquisar agora, ou o lote de conferência primeiro?". A lista do Jus IA sai do relatório, uma linha por tema, do jeito que se pergunta no Jus IA. Se o Jus IA estiver conectado à conta, a pesquisa pode ser feita daqui, com a mesma conferência depois (conferir na configuração da conta).

### Passo 4. Comparar quando a pesquisa voltar
Quando o advogado trouxer a pesquisa nova: a `trazer-pesquisa` (se instalada) monta o rascunho de fichas, e esta habilidade compara antes de juntar:

```
python3 "<pasta desta habilidade>/scripts/monitor.py" comparar \
  escritorio/04-base/juridico/jurisprudencia/<tema>.md \
  escritorio/04-base/juridico/jurisprudencia/rascunhos/<tema>-AAAA-MM-DD.md \
  --saida escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD-<tema>.md
```

O script diz: julgados novos (a favor, contra, qualificados), julgados que mudaram de posição, de situação ou de conferência, os que estão na base e não vieram na pesquisa nova, e "a tese pode ter sido afetada?": **sim** (contra novo qualificado, julgado a favor que caiu ou virou contra, órgão que decidia a favor com um contra novo, qualificado que virou contra ou caiu), **possível** (contra novo, qualificado novo ou mudado) ou **não**.

### Passo 5. O advogado decide
Com "sim" ou "possível", mostre a comparação, as teses do tema e as peças em andamento que usam essas teses, e pergunte: "O que fazemos com a tese: manter, ajustar, fazer a distinção, ou suspender as peças até decidir?". A decisão é do advogado. Com a resposta:
- a anotação na tese vai pela `banco-de-teses-vivo` (se instalada; sem ela, o advogado anota no arquivo da tese);
- peça a ajustar volta para `minuta` pelo comando `/motor-juridico:fila`, e a suspensão é do advogado;
- as fichas novas entram pela `trazer-pesquisa`, e as mudanças nas fichas que já estão passam pela conferência no inteiro teor.

### Passo 6. Gravar
Com o ok, o relatório fica em `escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD.md` (e a comparação em `AAAA-MM-DD-<tema>.md`). Nada mais muda.

### Passo 7. Aprender
Pergunte: "Algum tema que não precisa de vigilância tão de perto, ou algum que precisa de mais?". Cada resposta vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`), por exemplo "monitor: tema pericia-e-relatorio com pesquisa a cada 30 dias". Correção que afrouxa a regra fixa 1 ("se cair um julgado, já tira a tese da peça"): explique que a decisão é do advogado e proponha "peça com tese afetada vai para ADVOGADO AGORA no mesmo dia".

### Modo no ciclo
1. O `agente-juridico` chama no primeiro ciclo da semana (ou todo dia, se o aprendizado do escritório pedir). Não pergunte nada e não mostre nada.
2. Rode o passo 1 com `--saida`.
3. Devolva ao agente, para o resumo do dia: uma linha por peça em ADVOGADO AGORA ("P-2026-0001, peticao-inicial: tese restabelecimento-incapacidade afetada; julgado superado no tema pericia-e-relatorio"), e a lista "o que pesquisar no Jus IA".
4. Se houver comparação com "sim" ainda sem decisão do advogado, grave um aviso na fila (`07-operacao/juridico/fila/AAAA-MM-DD/NN-base-<tema>.md`, formato de `../../docs/agentes-e-fila.md`) com `tipo: aviso-de-precedente`, `revisor: pendente`, o caminho da comparação e, em `antes_de_enviar`, as peças em andamento com a tese. O aviso não tem texto para cliente.

### Modo agendado
Para rodar toda semana sem pedir, crie uma tarefa agendada (no Cowork ou no Claude Code; conferir na configuração da conta se tarefas agendadas estão disponíveis), meia hora antes do `horario_da_rotina_diaria`, com este texto:

```
Toda segunda-feira, às [HORÁRIO]: na pasta escritorio/, rode a habilidade monitor-de-precedentes
no modo agendado.
1. Rode: python3 "<pasta da habilidade>/scripts/monitor.py" vigiar escritorio/04-base/juridico
   --saida escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD.md
2. Não pesquise, não mude a base, as teses nem o pecas.csv.
3. Se houver peça em ADVOGADO AGORA, escreva uma linha por peça no topo do resumo do dia
   (escritorio/07-operacao/juridico/rotina/AAAA-MM-DD.md), e a lista "o que pesquisar no Jus IA".
4. Registre a rodada em escritorio/05-automacoes/monitor-de-precedentes/registro-de-uso.md:
   data, hora, temas lidos, peças em ADVOGADO AGORA, erros.
5. Se o script der erro, escreva o erro em uma linha no resumo do dia e pare.
```

Na primeira vez, grave a ficha da automação em `escritorio/05-automacoes/monitor-de-precedentes/ficha.md` (o que roda, quando, o que lê, o que grava, o que nunca faz, quem olha o relatório) e mostre ao advogado. Sem tarefa agendada, o advogado pede "roda o monitor" na segunda-feira, ou o ciclo faz isso.

### Modo treino
A base de treino em `assets/treino/` (dois temas, duas teses e um `pecas.csv` com ponto e vírgula, BOM e etapa em maiúscula):

```
python3 "<pasta desta habilidade>/scripts/monitor.py" vigiar "<pasta desta habilidade>/assets/treino" \
  --hoje 2026-07-20 --validade 90 --pecas "<pasta desta habilidade>/assets/treino/pecas.csv"
python3 "<pasta desta habilidade>/scripts/monitor.py" comparar \
  "<pasta desta habilidade>/assets/treino/jurisprudencia/pericia-e-relatorio.md" \
  "<pasta desta habilidade>/assets/treino/pesquisa-nova.md" --hoje 2026-07-20
```

Resultado esperado da vigilância: 2 temas, 9 fichas, 2 teses; os dois temas com pesquisa vencida; o Tema 9999 da TNU como precedente qualificado sem conferência; a P-2026-0001 (Marta, petição inicial, em minuta) em ADVOGADO AGORA como "a olhar"; a P-2026-0003 fora (já protocolada); a P-2026-0002 fora (sem tese); 9 julgados no lote de conferência; a `tese-sem-tema` apontada como sem tema. Resultado esperado da comparação: **SIM**, com 1 julgado novo contra da 1ª câmara (que decidia a favor), o Tema 9999 que passou de neutro a contra com tese fixada, e o julgado de 2023 a favor que passou a superado; 4 julgados da base fora da pesquisa nova, sem que isso diga que caíram. Tudo grava em `escritorio/07-operacao/_treino/juridico/precedentes/`.

### Modo adaptar
1. Leia a ficha, `nicho.md` e os temas da base.
2. Proponha: a cadência (semanal, quinzenal), os temas prioritários (os que sustentam as peças que mais saem), e os precedentes qualificados que o nicho sempre vigia.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Fica assim?".
4. Com o ok, grave em `aprendizados-juridico.md` (linhas "monitor: ...") e, se mudou a cadência, ajuste o texto da tarefa agendada.

## 4. O que é vencido, afetado e a olhar

| Situação | Quando | O que o monitor faz |
|---|---|---|
| Pesquisa vencida | A pesquisa mais recente do tema passou de `validade_da_conferencia` | Linha na lista do Jus IA, com a data de corte |
| Conferência vencida | Julgado verde conferido há mais do que a validade | Item no lote de conferência |
| Não conferido | Julgado que entrou e ninguém conferiu | Item no lote de conferência |
| Qualificado a vigiar | Súmula, tema, IRDR ou IAC na base | Linha na lista do Jus IA e do portal do tribunal |
| Tese a olhar | Tema da tese com pesquisa vencida ou qualificado sem conferência | Peça em andamento vai para ADVOGADO AGORA como "a olhar" |
| Tese afetada | Tema da tese com julgado a favor vermelho ou superado | Peça em andamento vai para ADVOGADO AGORA como "AFETADA" |

## 5. Formato da saída

```
MONITOR DE PRECEDENTES · AAAA-MM-DD · N temas, N fichas, N teses · validade N dias
ADVOGADO AGORA
  - [id] · [codigo] · [peça] · etapa [..] · tese [..] (AFETADA | a olhar)
TESES QUE PODEM ESTAR AFETADAS
  - [tese]: [tema]: [julgado] [o que mudou]
PESQUISAR DE NOVO NO JUS IA
  1. [tema]: julgados desde AAAA-MM-DD em [tribunais], a favor e contra
  2. [Tema N do TRIBUNAL]: situação atual no portal do tribunal
PRECEDENTES QUALIFICADOS · LOTE DE CONFERÊNCIA · TEMAS E TESES
Desde a última rodada: [o que é novo]
```

A comparação traz, no topo, "A tese pode ter sido afetada? SIM | POSSÍVEL | NÃO" com os motivos, e depois os julgados novos, os que mudaram e os que ficaram de fora.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Relatório da vigilância | `escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD.md` |
| Comparação de uma pesquisa nova | `escritorio/07-operacao/juridico/precedentes/AAAA-MM-DD-<tema>.md` |
| Linhas no resumo do dia (ciclo e agendado) | `escritorio/07-operacao/juridico/rotina/AAAA-MM-DD.md` |
| Aviso para o advogado (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-base-<tema>.md` |
| Ficha e registro de uso da tarefa agendada | `escritorio/05-automacoes/monitor-de-precedentes/` |
| Treino | `escritorio/07-operacao/_treino/juridico/precedentes/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O monitor não muda a base, as teses nem o `pecas.csv`. Sem pasta aberta: o relatório sai no chat, e a tarefa agendada não existe; o advogado pede o monitor uma vez por semana.

## 7. Solo e equipe

**Solo:** deixe a tarefa agendada na segunda de manhã e leia só ADVOGADO AGORA e a lista do Jus IA. Meia hora de pesquisa por semana mantém a base viva.

**Equipe:** o estagiário faz as pesquisas da lista e o lote de conferência; o dono de cada tema (campo `dono`) lê a comparação; a decisão sobre a tese é de quem assina. Se a mesma tese aparece afetada em várias peças, a conversa é na reunião de equipe, uma vez, e a decisão vale para todas.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Base que ninguém atualiza | Peça com precedente superado | Pesquisa vencida vira lista do Jus IA toda semana |
| Tema repetitivo julgado e ninguém viu | Tese contra precedente qualificado | Qualificados sempre na lista do portal |
| Julgado que caiu e peça que segue | Peça protocolada com tese enfraquecida | ADVOGADO AGORA cruza tese e `pecas.csv` |
| "Não veio na pesquisa" lido como "caiu" | Tese abandonada sem motivo | Regra fixa 4, dita no relatório |
| Monitor que muda a tese sozinho | Decisão de estratégia sem o advogado | Regra fixa 1; o monitor só avisa |
| Script que não leu e diz "tudo certo" | Falsa tranquilidade | Erro claro sem base; contagem do que leu |

## 9. Próximo passo

- Lista do Jus IA: o advogado pesquisa, a `trazer-pesquisa` (se instalada) monta as fichas, e o passo 4 compara.
- Lote de conferência: o modo lote da `trazer-pesquisa` (se instalada); sem ela, a conferência é feita na `conferir-citacoes` na hora de usar.
- Tese afetada: `banco-de-teses-vivo` (se instalada) e a decisão do advogado; o tema inteiro na página: `mapa-jurisprudencial` (se instalada).
- Peça que volta para minuta: `/motor-juridico:fila`.

## Referências desta habilidade

- `scripts/monitor.py`: `vigiar` (base, teses e `pecas.csv`) e `comparar` (pesquisa nova contra o tema). Rode nos passos 1 e 4 e nos modos no ciclo, agendado e treino.
- `assets/treino/jurisprudencia/pericia-e-relatorio.md`: tema de treino com sete julgados inventados (EXEMPLO), um qualificado. Use no modo treino.
- `assets/treino/jurisprudencia/qualidade-de-segurado.md`: segundo tema de treino, conferido. Use no modo treino.
- `assets/treino/teses/restabelecimento-incapacidade.md` e `assets/treino/teses/tese-sem-tema.md`: duas teses de treino, uma ligada aos dois temas e uma sem tema. Use no modo treino.
- `assets/treino/pecas.csv`: três peças de treino, com ponto e vírgula, BOM e etapa em maiúscula. Use no modo treino.
- `assets/treino/pesquisa-nova.md`: pesquisa nova de treino, em fichas, para a comparação. Use no modo treino.
