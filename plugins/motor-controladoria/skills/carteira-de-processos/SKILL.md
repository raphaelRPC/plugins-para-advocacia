---
name: carteira-de-processos
description: Monta e mantém a carteira de processos da controladoria (processos.csv), a lista que liga cada número de processo ao código do caso. Importa a exportação do sistema jurídico ou a planilha do escritório, guarda só o mínimo (primeiro nome do cliente, sem CPF nem endereço), junta com o que já existe sem apagar nada e nunca liga processo a caso por nome. Confere a carteira contra as publicações: processo que publica e não está na carteira, processo ativo parado há mais de processo_parado_dias, carteira atrás das publicações, linha sem código ou sem responsável. Use quando a pessoa disser "monta a lista de processos", "quais processos estão parados?", "esse processo não está na carteira", "inclui esse processo no caso tal". Não use para triar a publicação (use triar-publicacoes) nem para o andamento ao cliente (use status-para-o-cliente, do motor-experiencia).
---

# Carteira de processos

> Cada número de processo ligado ao código do caso, para a triagem nunca precisar adivinhar de quem é a publicação.

Regras: `../../docs/regras.md`. As colunas de `publicacoes.csv` e o caminho da publicação: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 17h. A advogada exporta a lista de processos do sistema: 180 linhas, com nome completo, CPF e "situação" escrita de seis jeitos. A carteira guarda o número, o código do caso, o primeiro nome e a situação, e deixa o CPF de fora. Na terça, quando sair uma publicação de um processo que não está ali, a triagem diz "sem caso" em vez de ligar ao cliente de nome parecido. E o processo do Jorge, sem movimentação desde dezembro, aparece na lista dos parados.

**Regras fixas desta habilidade:**
1. Processo e caso se ligam pelo código que a exportação traz ou que a pessoa diz. Nunca por nome, área ou palpite. Sem código: `[A CONFIRMAR]`, para a pessoa.
2. Mínimo de dados: número do processo, código, primeiro nome ou iniciais, área, tribunal, órgão, responsável, situação e datas. CPF, endereço, telefone e valor da causa não entram.
3. Nada se apaga. Processo que saiu da exportação continua na carteira até a pessoa dizer que encerrou ou arquivou.
4. O número do processo fica em `07-operacao/controladoria/`, fora do Projeto no Claude.

## 1. Quando usar

**Use quando:**
- O escritório vai montar a carteira pela primeira vez, a partir do sistema ou de uma planilha (modo "importar").
- Uma vez por semana, ou quando a `rotina-da-controladoria` pedir, para conferir a carteira contra as publicações (modo "conferir").
- A triagem achou um processo sem caso e a pessoa disse de quem é (modo "incluir").
- O `agente-de-controladoria` roda o ciclo e pede a conferência (modo "no ciclo").
- A pessoa quer treinar com a exportação de treino (modo "treino").
- A `adaptar-controladoria` (se instalada) pede o mapa da exportação do sistema do escritório (modo "adaptar").

**Não use quando:**
- O pedido é triar a publicação: `triar-publicacoes`, que lê esta carteira.
- O pedido é a carteira de clientes ativos e o "sem notícia": `rotina-da-experiencia`, do motor-experiencia (se instalado; sem ele, a carteira de processos não substitui a de clientes).
- O pedido é contar prazo: `calcular-prazo`.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-controladoria.md`), em especial os da `carteira-de-processos` (como o sistema chama cada coluna, que situação conta como ativa).
3. **Veja a carteira** que já existe: `escritorio/07-operacao/controladoria/processos.csv`.
4. **Veja os registros dos irmãos,** se existirem: a passagem do caso (`07-operacao/comercial/passagens/<codigo>.md`, do motor-comercial) e a pasta do caso (`07-operacao/juridico/casos/<codigo>/`, do motor-juridico) podem trazer o número do processo escrito. Só o número exato serve; nome não serve.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `carteira_de_processos` |
| Melhora | K: `processo_parado_dias` |

`carteira_de_processos` diz de onde vem a lista (sistema jurídico, planilha). Sem ele, pergunte: "Onde fica a lista dos processos ativos de vocês: o sistema jurídico exporta, ou é uma planilha?" e ofereça gravar. `processo_parado_dias` (por exemplo, 90) define o "parado"; sem ele, a conferência diz que não conferiu os parados e pergunta uma vez: "Depois de quantos dias sem movimentação um processo deve aparecer como parado?".

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Importar | Primeira carteira ou exportação nova | csv ou xlsx do sistema ou do escritório | `processos.csv` criado ou atualizado, com o ok |
| Conferir | Toda semana, ou a pedido | `processos.csv` e `publicacoes.csv` | As seis listas da seção 4 |
| Incluir | A pessoa disse de quem é um processo | Número, código, primeiro nome | Uma linha nova ou corrigida |
| No ciclo | O agente pede | O mesmo do conferir | Lista para o resumo; avisos na fila. Não mostra nada |
| Treino | Pedido de treino | `assets/exportacao-de-treino.csv` | A carteira de treino, em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | Ficha, nicho, a linha de títulos da exportação | Mapa de colunas e situações, para aprovar |

### Passo 1. Receber a exportação
Peça: "Pode salvar a exportação dos processos em `07-operacao/controladoria/entrada/`? Csv ou xlsx servem." Se o arquivo tiver colunas que a carteira não guarda (CPF, endereço, telefone), avise em uma linha que elas ficam de fora.

### Passo 2. Importar sem gravar

```
python3 "<pasta desta habilidade>/scripts/carteira_processos.py" importar \
  escritorio/07-operacao/controladoria/entrada/<exportacao>.csv \
  --carteira escritorio/07-operacao/controladoria/processos.csv --hoje AAAA-MM-DD
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/carteira-de-processos`. O script acha as colunas pelo nome ("Número do processo", "Pasta", "Cliente", "Situação", "Data do último andamento"), lê vírgula ou ponto e vírgula, utf-8 ou cp1252, datas AAAA-MM-DD ou DD/MM/AAAA, e mostra: o que entra, o que muda, as colunas descartadas, os processos sem código e os ativos que não vieram na exportação. Sem a coluna do número do processo, ele para e diz os nomes que aceita.

### Passo 3. Os códigos
Para cada processo sem código, pergunte, um de cada vez ou em lista curta: "O processo [número], cliente [primeiro nome], é de qual caso? Se não souber, fica sem código e a triagem manda a publicação para você." Nunca proponha um código por nome. Se o código está numa passagem ou na pasta do caso (número exato escrito lá), mostre onde está e peça o ok.

### Passo 4. Gravar
Mostre o resultado (seção 5) e pergunte: "Posso gravar a carteira?". Com o ok, rode o passo 2 com `--gravar`. O script junta pelo número: o que já estava não perde o código, a data de movimentação só anda para a frente, e nada é apagado. Para incluir um código que a pessoa disse:

```
python3 "<pasta desta habilidade>/scripts/carteira_processos.py" incluir \
  --carteira escritorio/07-operacao/controladoria/processos.csv \
  --processo 0000000-00.0000.0.00.0000 --codigo C-AAAA-NNNN --cliente <primeiro nome> \
  [--area] [--tribunal] [--orgao] [--responsavel] [--situacao ativo] --gravar
```

### Passo 5. Conferir contra as publicações

```
python3 "<pasta desta habilidade>/scripts/carteira_processos.py" conferir \
  --carteira escritorio/07-operacao/controladoria/processos.csv \
  --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv \
  --ficha escritorio/04-base/comum/ficha-da-controladoria.md --hoje AAAA-MM-DD
```

Mostre as seis listas (seção 4), a primeira no topo. `--parado-dias N` vale no lugar de `--ficha`. Com `--gravar`, o script atualiza a `ultima_movimentacao` dos processos que publicaram depois da data da carteira; isso a IA pode fazer. Mudar situação para `arquivado` ou `encerrado` é só com a pessoa (`incluir --situacao`).

### Passo 6. Os que publicaram e não estão na carteira
Para cada um, pergunte: "O processo [número] publicou com a OAB do escritório e não está na carteira. É caso antigo, substabelecimento ou erro?". Caso do escritório: passo 4, comando `incluir`, e a `triar-publicacoes` tria de novo a publicação. Erro ou substabelecimento sem reserva: fica fora da carteira, e a publicação continua `sem-caso` com a nota da pessoa.

### Passo 7. Aprender
Pergunte: "Alguma coluna da exportação que eu li errado, ou situação que vocês tratam diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Correção que afrouxa uma regra fixa ("pode ligar pelo nome, é sempre o mesmo cliente") não entra; proponha a que cabe ("o número do processo entra na passagem do caso, e a carteira lê de lá").

### Modo no ciclo
1. O agente pede a conferência (uma vez por semana, ou no dia que a ficha disser). Não pergunte nada e não mostre nada.
2. Rode o passo 5 com `--gravar` (só a `ultima_movimentacao` muda).
3. Devolva ao agente: os que publicaram e não estão na carteira (a triagem já os marcou `sem-caso`), os parados, os sem código e os sem responsável. Os parados e os sem responsável viram um `item: aviso` só (`NN-aviso-carteira.md`), no formato de `../../docs/agentes-e-fila.md`, com a lista em `antes_de_enviar`.

### Modo treino
A exportação de treino traz os seis processos dos casos fictícios, com nome completo e CPF zerado (para mostrar o que fica de fora), ponto e vírgula e datas DD/MM/AAAA, e o processo do Jorge sem código. Grave em `escritorio/07-operacao/_treino/controladoria/processos.csv`:

```
python3 "<pasta desta habilidade>/scripts/carteira_processos.py" importar \
  "<pasta desta habilidade>/assets/exportacao-de-treino.csv" \
  --carteira escritorio/07-operacao/_treino/controladoria/processos.csv --hoje 2026-04-08 --gravar
python3 "<pasta desta habilidade>/scripts/carteira_processos.py" incluir \
  --carteira escritorio/07-operacao/_treino/controladoria/processos.csv \
  --processo 0000909-99.2023.4.06.3800 --codigo C-2025-0088 --cliente Jorge --hoje 2026-04-08 --gravar
```

O teste passa quando: o CPF fica de fora; só o primeiro nome entra ("OTÁVIO RIBEIRO SANTOS" vira "Otávio"); o Jorge aparece sem código até o `incluir`; depois do `incluir`, a carteira fica igual a `../triar-publicacoes/assets/processos-de-treino.csv`. Na conferência de 2026-04-14 com 90 dias e sem publicações, o Jorge aparece parado (última movimentação 2025-12-15). Com as publicações do lote de treino, a Rosângela aparece em "publicou e não está na carteira" e os seis processos em "carteira atrás das publicações".

### Modo adaptar
1. Leia a ficha, `nicho.md` e a linha de títulos da exportação do sistema do escritório (sem dados de cliente).
2. Proponha: o mapa de colunas (o nome lá e a coluna aqui), o que cada situação do sistema quer dizer (ativo, suspenso, arquivado, encerrado), o `processo_parado_dias` por área se o escritório quiser (por exemplo, previdenciário 60, família 90), e o dia da conferência semanal.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "É assim que o sistema de vocês exporta?".
4. Com o ok, grave em `escritorio/04-base/controladoria/nicho/carteira-de-processos.md`.

## 4. As seis listas da conferência

| # | Lista | O que fazer |
|---|---|---|
| 1 | Publicou e não está na carteira | Para a pessoa, no mesmo dia (passo 6) |
| 2 | Ativo parado há mais de `processo_parado_dias`, contando a última publicação | A advogada responsável olha o processo no sistema do tribunal; com o motor-experiencia (se instalado), o cliente pode estar há tempo demais sem notícia |
| 3 | Carteira atrás das publicações | `--gravar` atualiza a `ultima_movimentacao` |
| 4 | Sem código do caso | A pessoa diz o código (passo 3) |
| 5 | Ativo sem responsável | A pessoa diz quem cuida (`responsaveis_por_area` ajuda) |
| 6 | Número repetido na carteira | Juntar as linhas, com a pessoa |

As situações: `ativo`, `suspenso`, `arquivado`, `encerrado`. "Em andamento", "cumprimento de sentença" e "recurso" contam como `ativo`; o que o script não reconhece fica `[A CONFIRMAR: <como veio>]`.

## 5. Formato da saída

```
CARTEIRA · importação de [arquivo] · AAAA-MM-DD · [gravado | SIMULAÇÃO]
N linhas antes · N novas · N atualizadas
Colunas lidas: [campo <- coluna da exportação]
Colunas que NÃO entram: [CPF, endereço...]
SEM CÓDIGO DO CASO (N): [processo · primeiro nome · tribunal · órgão]
ATIVOS QUE NÃO VIERAM NA EXPORTAÇÃO (N): [processo · código]

CONFERÊNCIA DA CARTEIRA · AAAA-MM-DD · N processos · N publicações
1. PUBLICOU E NÃO ESTÁ NA CARTEIRA: [processo · tribunal · ids]
2. ATIVOS PARADOS HÁ MAIS DE N DIAS: [processo · código · última movimentação]
3. CARTEIRA ATRÁS DAS PUBLICAÇÕES  4. SEM CÓDIGO  5. SEM RESPONSÁVEL  6. REPETIDOS
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A carteira de processos | `escritorio/07-operacao/controladoria/processos.csv` |
| A exportação recebida | `escritorio/07-operacao/controladoria/entrada/` (e `entrada/lidos/AAAA-MM-DD/` depois) |
| Mapa da exportação (modo adaptar) | `escritorio/04-base/controladoria/nicho/carteira-de-processos.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/processos.csv` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Colunas, nesta ordem: `processo,codigo_caso,cliente_curto,area,tribunal,orgao,responsavel,situacao,ultima_movimentacao,atualizado_em`. A exportação do sistema tem dado de cliente: o resumo do dia lembra a pessoa de apagar `entrada/lidos/` com mais de 7 dias. Sem pasta aberta: a carteira sai numa tabela para colar na planilha, e a conferência, no chat.

## 7. Solo e equipe

**Solo:** importe uma vez e mantenha pela triagem: cada sem caso que você resolve vira uma linha nova. A conferência dos parados uma vez por mês já evita o processo esquecido.

**Equipe:** quem importa é o `responsavel_controladoria`; quem diz o código e a situação é a advogada responsável. Caso novo que vira processo (o comercial fecha, o jurídico protocola) entra na carteira no dia do protocolo, com o número.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Ligar processo ao cliente de nome parecido | Prazo no caso errado | Regra fixa 1: só o código dito ou exportado |
| Planilha do sistema com CPF copiada inteira | Dado de cliente onde não precisa | Regra fixa 2: colunas sensíveis ficam de fora |
| Processo sumido da exportação apagado | Publicação dele vira sem caso sem motivo | Regra fixa 3: nada se apaga |
| Processo parado que ninguém vê | Cliente sem notícia, prazo prescricional esquecido | Lista 2, com `processo_parado_dias` |
| Carteira com movimentação velha | Parado que não está parado | Lista 3 atualiza pela última publicação |
| Situação escrita de seis jeitos | Ativo tratado como arquivado | Situações normalizadas e `[A CONFIRMAR]` no resto |

## 9. Próximo passo

- Publicação sem caso resolvida: `triar-publicacoes` de novo, com `--ids <id> --todas`.
- Processo parado com cliente esperando notícia: `status-para-o-cliente`, do motor-experiencia (se instalado; sem ele, a advogada liga).
- O resumo do dia com os parados: `rotina-da-controladoria`.

## Referências desta habilidade

- `scripts/carteira_processos.py`: `importar` a exportação (mínimo de dados, sem apagar), `conferir` contra as publicações (as seis listas) e `incluir` o processo que a pessoa disse de quem é. Rode nos passos 2, 4 e 5, no ciclo e no treino.
- `assets/exportacao-de-treino.csv`: uma exportação de sistema de treino com os seis processos dos casos fictícios, nomes completos, CPF zerado, ponto e vírgula e o Jorge sem código. Use no modo treino.
