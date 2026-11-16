---
name: triagem-em-massa
description: Para os dias de centenas de publicações. Agrupa por script os atos de teor igual ou quase igual (o mesmo despacho padrão em processos diferentes), sem nunca juntar atos com número de dias, horas ou destinatário diferente, e separa as exceções: o que é urgente, o que não está na carteira, o que não tem par. Cada grupo recebe uma triagem e uma providência, decididas pela pessoa depois de ler a amostra inteira; as exceções vão uma a uma para a triagem comum. A conta do prazo continua uma por publicação. Use quando a pessoa disser "chegaram 300 intimações hoje", "são todas iguais, tria de uma vez", "agrupa os despachos padrão", "quero triar por lote". Não use para triar poucas publicações (use triar-publicacoes) nem para contar os prazos do lote (use prazos-em-lote ou calcular-prazo).
---

# Triagem em massa

> Trezentas publicações viram dez grupos e um punhado de exceções, e a pessoa lê a amostra de cada grupo antes de decidir.

Regras: `../../docs/regras.md`. As triagens e as colunas de `publicacoes.csv`: `../../docs/prazos.md`. A contagem: `../../docs/contagem.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda depois do recesso. O escritório tem uma carteira grande de previdenciário e o DJEN trouxe 412 publicações. Duzentas são o mesmo ato ordinatório pedindo comprovante de residência em 15 dias; oitenta são "ciência do retorno dos autos". No meio delas, dois atos iguais aos outros, só que com 5 dias, e um dirigido ao INSS. O agrupamento separa esses três, e a advogada decide os grupos grandes em vinte minutos, depois de ler a amostra.

**Regras fixas desta habilidade:**
1. O grupo é sugestão do script. A triagem e a providência do grupo são decididas pela pessoa, depois de ler a amostra inteira. Sem a amostra lida, o script não aplica nada.
2. Nunca entram no mesmo grupo atos com número de dias ou de horas diferente, com destinatário diferente (parte autora, parte ré, INSS, as partes) ou com sinais diferentes (audiência, perícia, sentença, valor).
3. Urgente, sem caso e sem par ficam fora dos grupos e vão uma a uma para a `triar-publicacoes`, com PESSOA AGORA quando couber.
4. A conta continua uma por publicação, e a dupla conferência também. Grupo não vira prazo em lote sem a conta de cada um.
5. Variante quase igual que muda o que fazer (outro documento, outro ato) sai do grupo.

## 1. Quando usar

**Use quando:**
- Há dezenas ou centenas de publicações `nao-triada` de uma vez (modo "a pedido").
- O `agente-de-controladoria` roda o ciclo num dia de volume alto (modo "no ciclo": agrupa e deixa a decisão na fila).
- A pessoa quer treinar o agrupamento (modo "treino").
- A `adaptar-controladoria` (se instalada) pede os atos padrão do escritório (modo "adaptar").

**Não use quando:**
- São poucas publicações (menos de 30, como regra prática): `triar-publicacoes`, uma a uma.
- O pedido é a conta dos prazos do lote: `prazos-em-lote` (se instalada; sem ela, a `calcular-prazo` uma por uma).
- O pedido é decidir a providência de cada tipo de ato: `providencia-sugerida` (se instalada), que guarda a tabela "tipo de ato, providência de costume".

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-controladoria.md`), em especial os da `triagem-em-massa` (grupos que o escritório já decidiu de um jeito, variantes que sempre saem).
3. **Capte antes:** as publicações precisam estar em `publicacoes.csv`, com o teor guardado (`captar-publicacoes`). As duplicadas já saíram na captação.
4. **Tenha a carteira de processos** (`processos.csv`, da `carteira-de-processos`, se instalada): sem ela, o sem caso não é separado e o script avisa.
5. **Veja a tabela de providências** do escritório (`04-base/controladoria/providencias.md`, da `providencia-sugerida`, se instalada), para sugerir a providência de costume de cada grupo.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `tribunais`, `quem_decide_providencia` |
| Melhora | E: `areas` |

`tribunais` diz o que esperar no lote (publicação de tribunal fora da lista vai para as exceções, para conferir). `quem_decide_providencia` é quem lê a amostra e decide cada grupo; sem ele, pergunte: "Quem decide o que fazer com cada grupo de publicações?" e ofereça gravar. `areas` ajuda a nomear os grupos pelo ato típico do nicho.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | Volume alto no dia | `publicacoes.csv`, teor, carteira | Os grupos e as exceções no chat; a triagem de cada grupo, com o ok |
| No ciclo | O agente chama | O mesmo | Grupos gravados em `lotes/` e um `item: decidir-providencia` por grupo. Não mostra nada |
| Treino | Pedido de treino | `assets/lote-em-massa-de-treino.csv` e `assets/processos-em-massa-de-treino.csv` | Os grupos de treino, em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | Ficha, nicho, atos padrão anonimizados | Os atos padrão do escritório e a providência de costume, para aprovar |

### Passo 1. Agrupar

```
python3 "<pasta desta habilidade>/scripts/agrupar_publicacoes.py" agrupar \
  escritorio/07-operacao/controladoria/publicacoes.csv \
  --processos escritorio/07-operacao/controladoria/processos.csv --hoje AAAA-MM-DD
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/triagem-em-massa`. O script tira do teor o que muda de um processo para outro (número do processo, datas, valores, folhas, nomes das partes), junta os iguais e, dentro do mesmo perfil (dias, horas, destinatário, sinais), os quase iguais pela proporção de palavras em comum, na ordem (`--limiar 0.9` é o padrão; mais baixo junta mais). Sem `--gravar`, só mostra. Sem o publicacoes.csv ou com coluna faltando, sai com código 1; sem publicação `nao-triada`, diz quantas linhas leu.

### Passo 2. Mostrar os grupos
Mostre a lista (seção 5), do maior grupo ao menor, e as exceções embaixo. Para cada grupo quase igual, mostre as variantes e o que muda ("sai: juntar · entra: que junte"). Pergunte: "Quer tirar alguma variante de algum grupo antes de ler a amostra?".

### Passo 3. A amostra
Para cada grupo, mostre o teor inteiro de cada publicação da amostra (a primeira, a última e um sorteio, cerca da raiz quadrada do tamanho do grupo; no mínimo duas) e o trecho literal que a `triar-publicacoes` acharia no representante:

```
python3 "<pasta da triar-publicacoes>/scripts/apoio_triagem.py" \
  escritorio/07-operacao/controladoria/publicacoes.csv \
  --processos escritorio/07-operacao/controladoria/processos.csv \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md --ids <ids da amostra>
```

Pergunte à pessoa de `quem_decide_providencia`, um grupo por vez: "Li com você a amostra do grupo [G01, N publicações]. A triagem de todas é [prazo, 15 dias, juntar documento]? E a providência?". Se a amostra mostrar uma publicação diferente das outras, ela sai do grupo (`--fora`) e vai para as exceções.

### Passo 4. Aplicar a triagem do grupo
Só depois que a pessoa disser que leu a amostra e que a triagem vale para todos:

```
python3 "<pasta desta habilidade>/scripts/agrupar_publicacoes.py" aplicar \
  escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-grupos.csv \
  --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv \
  --processos escritorio/07-operacao/controladoria/processos.csv \
  --grupo G01 --triagem prazo --resumo "Juntar documento em 15 dias" \
  --amostra-conferida [--fora PUB-...,PUB-...] [--por <nome>] --gravar
```

Grupo de `ciencia` ou `sem-providencia` em que algum ato pode pedir algo à parte do cliente (número de dias sem destinatário da outra parte, "diga", "no prazo legal", "manifeste-se", "especifique provas", "intime-se a parte autora"): a amostra não basta, e o script recusa. Aplique `--triagem prazo` (os dias ficam `[A CONFIRMAR: quantos dias]` quando o ato não diz) ou trie uma a uma na `triar-publicacoes`. Na dúvida entre ciência e prazo, prazo. Só se a pessoa disser que leu todas as publicações do grupo, e não só a amostra, rode com `--li-todas`.

Sem `--amostra-conferida`, o script recusa. Ele muda só as linhas `nao-triada` (ou triadas pela IA) do grupo, liga cada uma ao caso pela carteira (a que não está na carteira fica `sem-caso`) e grava o resumo sem dado sensível. `--por` leva o nome de quem decidiu só quando a pessoa disser, na conversa, que conferiu; sem isso, `ia`.

### Passo 5. As exceções
Rode a `triar-publicacoes` só nas exceções (`--ids`), com PESSOA AGORA primeiro (urgente, sem caso, captada com atraso).

### Passo 6. A conta e a providência
Os grupos com `prazo` vão para a conta, uma por publicação: `prazos-em-lote` (se instalada) ou a `calcular-prazo`, uma a uma. A providência decidida para o grupo vai para a `encaminhar-providencia`, uma por caso (cada pedido de peça ou tarefa leva o código e o prazo de cada processo).

### Passo 7. Aprender
Pergunte: "Algum grupo que você separaria diferente, ou ato padrão que sempre tem a mesma providência?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`; providência de costume vai para a `providencia-sugerida` (se instalada). Correção que afrouxa uma regra fixa ("aplica sem amostra, é sempre igual") não entra; proponha a que cabe ("amostra de duas publicações nos grupos que o escritório já decidiu três vezes do mesmo jeito").

### Modo no ciclo
1. O agente chama quando o lote do dia passa do volume que a ficha ou a rotina definir (por exemplo, 30 publicações). Não pergunte nada e não mostre nada.
2. Rode o passo 1 com `--gravar`: os grupos ficam em `lotes/AAAA-MM-DD-grupos.csv` e `lotes/AAAA-MM-DD-triagem-em-massa.md`.
3. Não aplique triagem nenhuma. Devolva ao agente um `item: decidir-providencia` por grupo, em `07-operacao/controladoria/fila/AAAA-MM-DD/NN-grupo-g01-providencia.md`, no formato de `../../docs/agentes-e-fila.md`, com `revisor: pendente`, o tamanho do grupo, o representante, os ids da amostra e o trecho literal, e em `antes_de_enviar`: "ler a amostra inteira", "a triagem do grupo", "a providência do grupo".
4. As exceções seguem pela `triar-publicacoes` no mesmo ciclo.

### Modo treino
Um lote de 32 publicações fictícias de um JEF, com as armadilhas do volume, e a carteira delas (uma fica de fora de propósito). Tudo grava em `escritorio/07-operacao/_treino/controladoria/`:

```
python3 "<pasta da captar-publicacoes>/scripts/importar_publicacoes.py" \
  "<pasta desta habilidade>/assets/lote-em-massa-de-treino.csv" \
  --registro escritorio/07-operacao/_treino/controladoria --data 2026-04-14 --treino --gravar
python3 "<pasta desta habilidade>/scripts/agrupar_publicacoes.py" agrupar \
  escritorio/07-operacao/_treino/controladoria/publicacoes.csv \
  --processos "<pasta desta habilidade>/assets/processos-em-massa-de-treino.csv" --hoje 2026-04-14
```

O teste passa quando saem quatro grupos e cinco exceções: G01 com 11 (o comprovante de residência em 15 dias para a parte autora, com a variante "que junte" mostrada); G02 com 8 (ciência do retorno dos autos, 5 dias, as partes); G03 com 6 (cálculos pelo INSS em 30 dias, com a variante "que apresente"); G04 com 2 (o mesmo comprovante, só que em 5 dias, fora do G01); nas exceções, a publicação do processo que não está na carteira (escondida no meio do G01), a dirigida ao INSS com o texto do G01, a sentença, a audiência e a tutela em 48 horas (PESSOA AGORA). O `aplicar` sem `--amostra-conferida` recusa.

### Modo adaptar
1. Leia a ficha, `nicho.md` e uma amostra de atos padrão anonimizados do escritório.
2. Proponha: os atos padrão que mais chegam (com o texto típico), a triagem e a providência de costume de cada um, o tamanho da amostra que o escritório quer, e o volume a partir do qual o ciclo agrupa.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "São estes os atos que chegam em volume para vocês?".
4. Com o ok, grave em `escritorio/04-base/controladoria/nicho/triagem-em-massa.md`.

## 4. O que separa um grupo

| Entra no mesmo grupo | Nunca entra no mesmo grupo |
|---|---|
| O mesmo texto com outro número de processo, outra data, outro valor, outro nome de parte | Outro número de dias ou de horas |
| A mesma frase com uma palavra trocada ("juntar" e "que junte"), mostrada como variante | Outro destinatário (parte autora e INSS) |
| Atos de órgãos diferentes com o mesmo texto | Um com audiência, perícia, sentença ou valor e outro sem |
| | Urgente, sem caso, sem par |

Grupo com datas que mudam (audiências em dias diferentes, por exemplo) tem a mesma triagem, mas cada linha leva a sua data: o relatório avisa.

## 5. Formato da saída

```
TRIAGEM EM MASSA · AAAA-MM-DD · N publicações · N grupos com N · N exceções
## G01 · N publicações · igual | quase igual (menor semelhança 0,93)
- Perfil: dias: 15 · destinatário: parte autora
- Representante: [id · tribunal · órgão]
- Teor do representante: "[o texto]"
- Amostra para ler inteira (N): [ids]
- Todos: [ids]
- Variante [id] (N com este texto): sai "[...]" · entra "[...]"
- Triagem do grupo: [A DEFINIR pela pessoa, depois da amostra]
## Exceções (uma a uma, pela triar-publicacoes)
- [id · tribunal · processo · motivo]
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Os grupos (uma linha por publicação: grupo, id, papel) | `escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-grupos.csv` |
| O relatório dos grupos | `escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-triagem-em-massa.md` |
| A triagem aplicada | `escritorio/07-operacao/controladoria/publicacoes.csv` |
| Itens da fila (modo no ciclo) | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-grupo-<grupo>-providencia.md` |
| Atos padrão do escritório (modo adaptar) | `escritorio/04-base/controladoria/nicho/triagem-em-massa.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

`prazos.csv` não muda aqui. Linha confirmada por uma pessoa não é sobrescrita. Sem pasta aberta e sem código: a habilidade não roda (o agrupamento precisa de script); a triagem segue uma a uma na `triar-publicacoes`.

## 7. Solo e equipe

**Solo:** volume alto sozinho é onde o prazo escapa. Agrupe, decida os grupos grandes primeiro e deixe as exceções para quando estiver com a cabeça fresca, no mesmo dia.

**Equipe:** quem agrupa e separa a amostra é o `responsavel_controladoria`; quem lê a amostra e decide é a pessoa de `quem_decide_providencia`. Dividir os grupos entre duas advogadas funciona, desde que cada grupo tenha um nome só na decisão.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "São todos iguais" sem ler nenhum | O ato diferente passa junto | Regra fixa 1: amostra lida antes de aplicar |
| Grupo marcado ciência por amostra, com ato que pede algo ao cliente | Prazo sem linha, ninguém olha de novo | `aplicar` recusa `ciencia` e `sem-providencia` quando algum ato pede algo; vira `prazo` ou triagem uma a uma |
| Ato de 5 dias no grupo dos de 15 | Prazo perdido no meio do lote | Regra fixa 2: dias diferentes nunca juntam |
| Prazo do INSS no grupo da parte autora | Prazo da outra parte lançado como do escritório | Destinatário diferente nunca junta |
| Processo fora da carteira aplicado em lote | Prazo em caso de ninguém | Sem caso vai para as exceções |
| Tutela em 48 horas esperando o grupo | Urgência tratada como rotina | Urgente fica fora, em PESSOA AGORA |
| Uma conta para o grupo inteiro | Calendários e datas diferentes ignorados | Regra fixa 4: a conta é uma por publicação |

## 9. Próximo passo

- As exceções: `triar-publicacoes`, uma a uma.
- A conta dos grupos com prazo: `prazos-em-lote` (se instalada; sem ela, `calcular-prazo`).
- A providência de cada grupo: `encaminhar-providencia`, um pedido por caso.
- O ato padrão que se repete toda semana: `providencia-sugerida` (se instalada) guarda a providência de costume.

## Referências desta habilidade

- `scripts/agrupar_publicacoes.py`: `agrupar` (iguais e quase iguais pelo perfil, exceções, amostra) e `aplicar` (a triagem do grupo, só com a amostra conferida). Rode nos passos 1 e 4, no ciclo e no treino.
- `assets/lote-em-massa-de-treino.csv`: 32 publicações fictícias de um JEF com as armadilhas do volume (dias diferentes, outro destinatário, sem caso escondido, urgente). Use no modo treino.
- `assets/processos-em-massa-de-treino.csv`: a carteira de treino do lote em massa, sem um dos processos de propósito. Use no modo treino.
