---
name: conferir-peca
description: >
  Confere os dados e a coerência de uma peça antes de ela chegar ao advogado. Um script faz a
  parte mecânica: nome que aparece e não é do caso (sobra de outra peça), gênero trocado, datas e
  valores divergentes, valor da causa diferente no cabeçalho e no fecho, "doc. N" sem documento N
  na lista, pedido sem nenhum fato nem fundamento, marcações que sobraram. A leitura faz a parte
  de coerência: pedidos x fundamentos x fatos do dossiê, documentos citados x anexados,
  requisitos formais [CONFERIR] e o padrão da ficha jurídica. Grava o relatório e a coluna dados
  do pecas.csv. Use quando o advogado disser "confere a minuta", "tem nome de outro cliente
  aqui?", "revisa os dados da petição", "bate os documentos", "a peça está pronta para eu ler?".
  Não use para conferir lei, súmula, julgado e aspas (use conferir-citacoes).
---

# Conferir a peça

> Antes de o advogado ler, a peça passa por uma conferência que não cansa: cada nome, cada data, cada valor, cada documento e cada pedido batem com o caso.

Regras: `../../docs/regras.md`. Etapas e `pecas.csv`: `../../docs/producao.md`. Citações (a outra metade da conferência): `../../docs/citacoes.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino e gabarito: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 9h. O estagiário aproveitou a petição do Paulo para começar a da Marta. Ficou um "o autor Paulo" no item 4 dos fatos, três "o requerente" no meio de "a requerente", a data de cessação de um documento nos fatos e a do outro nos pedidos, e um "conforme doc. 7" numa lista que vai até o 6. Lido de uma vez, às 18h, nada disso salta aos olhos. Para o juiz, salta.

**Regras fixas desta habilidade:**
1. O script aponta e a leitura confirma. Nenhum alerta é descartado sem uma pessoa decidir, e a decisão fica escrita no relatório.
2. Pedido sem fundamento, fato sem pedido e contradição com o dossiê são do advogado: a habilidade mostra e propõe, não corta nem acrescenta pedido sozinha.
3. A etapa `conferida` só com `dados = ok` e `citacoes = verde` (`../../docs/producao.md`, regra 4).
4. Dado sensível entra na peça só no que o pedido precisa. CPF, endereço e documento entram pelo sistema do escritório.
5. Requisito legal da peça, competência e valor de alçada ficam sempre `[CONFERIR]` na norma e no regimento.

## 1. Quando usar

**Use quando:**
- Uma minuta ficou pronta e vai para o advogado.
- O advogado quer saber se sobrou dado de outro caso numa peça aproveitada.
- O `agente-juridico` chamou no ciclo (modo "no ciclo"), ou a `pecas-em-lote` (se instalada) passou um lote.
- O `/motor-juridico:comecar` pediu a conferência da minuta de treino (modo "treino").
- A `adaptar-juridico` (se instalada) pediu os temas de pedido e a lista de requisitos das peças do escritório (modo "adaptar").

**Não use quando:**
- O pedido é conferir lei, artigo, súmula, tema, julgado, doutrina ou aspas: `conferir-citacoes` (as duas rodam juntas).
- O pedido é comparar duas versões de um documento: `comparar-versoes` (se instalada; sem ela, rode esta habilidade em cada versão e compare os relatórios).
- Ainda não há peça, só documentos: `dossie-do-caso` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-juridica.md` e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`). Linhas da `conferir-peca` com "tema de pedido:" viram a opção `--temas-extra` do script.
3. **Leia o caso:** `escritorio/07-operacao/juridico/casos/<codigo>/dossie.md` (índice de documentos, linha do tempo, contradições, lacunas) e `estrategia.md` (a tese que o advogado definiu). Sem dossiê, pergunte: "Quem são as partes do caso e quantos documentos vão com a peça?".
4. **Leia a lista de requisitos da peça**, se o escritório já gravou uma no modo adaptar: `escritorio/04-base/juridico/modelos/<peca>/conferencia.md`.
5. **Conta de IA:** peça de cliente só em conta profissional ou de equipe. Em conta pessoal, só a minuta de treino.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `pecas_mais_feitas` |
| Melhora | J: `estilo`, `pedidos`, `nome_dos_arquivos` |

`areas` e `pecas_mais_feitas` dizem que tipo de peça é e quais temas de pedido olhar. Sem eles, pergunte: "Que peça é esta e de qual área?". `estilo` e `pedidos` são o padrão da seção 4 da referência; `nome_dos_arquivos` confere a lista de documentos com os anexos. Na prática, a habilidade também lê `quem_assina` e `citacao_em_recuo` (J) quando existem.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Peça inteira | Minuta pronta | A peça e o dossiê | O relatório (seção 5), a seção "Dados e coerência" e a coluna `dados` |
| Peça aproveitada | "Usei a peça de outro cliente" | A peça e o nome do outro caso | O mesmo, com o outro nome procurado de propósito (`--nomes` sem ele) |
| Lote | `pecas-em-lote` (se instalada) | As minutas do lote | Um relatório por minuta; linha com alerta não sai do lote |
| No ciclo | O `agente-juridico` chama | A minuta em `minuta` | Relatório gravado, `dados` atualizada, linhas para a fila. Não pergunta nada |
| Treino | Minuta de treino ou "é teste" | `assets/minuta-com-erros.md` | O mesmo, gravado em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Ficha, nicho e peças boas | Temas de pedido e lista de requisitos por peça, para aprovar |

Pedido direto ("confere essa minuta"): não faça entrevista. Rode e pergunte só o que faltar.

### Passo 1. A peça e o caso
Se não vieram, pergunte: "Qual é a peça e de qual caso?". Com o dossiê, anote o primeiro nome do cliente, o gênero pelas palavras do próprio dossiê ("a segurada"), os outros nomes do caso (parte contrária, médico, testemunha) e quantos documentos vão.

### Passo 2. Rodar o script
Rode o script da pasta desta habilidade, com o caminho da peça:

```
python3 "<pasta desta habilidade>/scripts/conferir_dados.py" \
  escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md \
  --cliente <primeiro nome> --codigo <codigo> \
  --saida escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD-dados.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/conferir-peca`. Opções: `--genero feminino|masculino` (sem ela, o script usa a qualificação e, sem qualificação, a maioria); `--nomes "Nome,Nome"` (outros nomes que são do caso); `--docs N` (quantos documentos, quando a peça não traz a lista); `--temas-extra "rótulo=expressão;..."` (temas de pedido dos aprendizados); `--json`. Lê .md, .txt e .docx. Sai com erro e uma mensagem clara quando falta o arquivo, ele está vazio ou o .docx não abre, e sempre diz o que verificou e quanto leu.

O que ele confere: nomes em papel de parte e códigos de outro caso; gênero das palavras de parte (fora das aspas e do recuo); datas por fato (cessação, admissão, dispensa, nascimento, perícia...); valor da causa em todos os pontos; "doc. N" contra a lista; tema de pedido sem menção nos fatos ou no direito, e pedido que aponta item que não existe; marcações que sobraram; CPF e CID escritos na peça.

Sem o script (chat sem arquivos): faça as mesmas verificações à mão, na mesma ordem, e diga que foram à mão.

### Passo 3. Confirmar cada alerta do script
Leia o trecho de cada alerta na peça. Alerta certo vai para o relatório com a correção proposta. Alerta que não é erro (por exemplo, um nome de testemunha que o script não conhecia): rode de novo com `--nomes` e anote no relatório. Nunca apague um alerta sem dizer por quê.

### Passo 4. A coerência
Monte a matriz de `references/coerencia-e-requisitos.md`, seção 1: cada pedido com o fundamento, o fato e a prova; e cada fato importante do dossiê com o lugar dele na peça. Procure sobra de outro caso além do nome (seção 2 da referência).

### Passo 5. Documentos, requisitos e padrão
- Lista de documentos x anexos reais (os arquivos da pasta do caso ou o que o advogado diz), no jeito de `nome_dos_arquivos`.
- Requisitos formais da peça: a lista do escritório, se existir; senão, as perguntas da seção 3 da referência, cada uma `[CONFERIR]`.
- Padrão da ficha (seção 4 da referência): estilo, pedidos, recuo, tamanho.
- Dado sensível além do necessário (seção 5 da referência).

### Passo 6. Mostrar
Mostre o relatório (seção 5): alertas abertos primeiro, depois coerência, requisitos e padrão. Para cada um, a correção proposta. Pergunte: "Quer que eu aplique as correções numa versão nova e grave o relatório?". Pedido sem fundamento, fato sem pedido e contradição com o dossiê: pergunte uma vez, para o conjunto, "O que fica: [opções]?" e espere o advogado.

### Passo 7. Gravar
Com o ok:
1. As correções aprovadas vão para `minutas/<peca>-v<n+1>.md`, nunca por cima da versão conferida. Rode o script de novo na versão nova.
2. Grave a seção "Dados e coerência" em `conferencias/<peca>-AAAA-MM-DD.md` (o mesmo arquivo da `conferir-citacoes`; esta habilidade não mexe na seção "Citações").
3. Atualize `dados` no `pecas.csv` (`ok`, `com-alerta`) e `atualizado_em`. A etapa vai para `conferida` só se `citacoes` também estiver `verde`.

### Passo 8. Aprender
Pergunte: "Tem algum erro que vocês costumam pegar na revisão e que eu não procurei?". Cada resposta vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`): "tema de pedido: <rótulo>=<expressão>" para o script, ou um item novo na lista de requisitos da peça. Correção que afrouxa a regra fixa 2 ("pode cortar o pedido que não tiver fundamento"): explique que o corte é do advogado e proponha "o relatório já traz o pedido sem fundamento no topo".

### Modo no ciclo
1. O agente passa a minuta e o caso. Não pergunte nada e não mostre nada.
2. Rode o passo 2 com `--cliente`, `--codigo` e `--nomes` do dossiê, e `--saida`.
3. Faça os passos 4 e 5 com o dossiê e a estratégia. Não aplique correção na peça: as correções vão como proposta no relatório.
4. Grave a seção "Dados e coerência" e atualize `dados` no `pecas.csv`.
5. Devolva ao agente: o caminho do relatório, o número de alertas por tipo, e uma linha por alerta para `antes_de_enviar` do item da fila. Nome de outro caso, valor da causa divergente e documento que não existe são bloqueio do revisor até alguém corrigir; pedido sem fundamento vai como `conferir`.

### Modo treino
A minuta `assets/minuta-com-erros.md` (caso 1, Marta), copiada para `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md`. O dossiê de treino é a tabela do caso 1 em `../../docs/casos-ficticios.md`.

```
python3 "<pasta desta habilidade>/scripts/conferir_dados.py" \
  escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md \
  --codigo C-2026-0001
```

Rode a `conferir-citacoes` na mesma minuta (modo treino dela) e mostre uma tabela só, em ordem de gravidade. Compare com a seção 4. Tudo grava em `escritorio/07-operacao/_treino/juridico/`.

### Modo adaptar
1. Leia a ficha, `nicho.md` e de 3 a 5 peças boas do tipo (`onde_estao_os_modelos`).
2. Proponha: os temas de pedido que pedem fato (por exemplo, no família, alimentos e guarda; no trabalhista, horas extras e vínculo), como "tema de pedido: rótulo=expressão"; e a lista de requisitos da peça, com cada item `[CONFERIR]` na norma.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Falta algum ponto que vocês sempre olham nessa peça?".
4. Com o ok, grave os temas em `aprendizados-juridico.md` e a lista em `escritorio/04-base/juridico/modelos/<peca>/conferencia.md`.

## 4. Conferência com o caso de treino

Rodando a minuta de treino, o script e o fluxo têm que achar exatamente isto:

| Erro do gabarito | Quem acha | O que aparece | Linha |
|---|---|---|---|
| 1. "o autor Paulo" no item 4 dos fatos | script | nome de fora do caso (e no gênero trocado) | 24 |
| 2. "o requerente" em três trechos | script | gênero trocado, 3 trechos | 25, 39, 45 |
| 3. Cessação em 2026-02-28 nos fatos e 2026-03-05 nos pedidos | script | datas divergentes, cessação do benefício | 22 e 61 |
| 4. Valor da causa diferente no cabeçalho e no fecho | script | valor da causa divergente: R$ 38.400,00 e R$ 34.800,00 | 11 e 69 |
| 5. Dano moral sem fundamento | script e matriz do passo 4 | pedido sem fundamento | 64 |
| 6. "conforme doc. 7" com lista até o doc. 6 | script | documento que não existe | 39 |
| 7. Súmula 999 do TRF6 | `conferir-citacoes` | vermelho: não existe | 45 |
| 8. "entendimento pacífico do STJ" | `conferir-citacoes` | amarelo: sem fonte | 45 |
| 9. Aspas do art. 59 com palavras trocadas | `conferir-citacoes` | amarelo: aspas não batem | 37 |
| 10. Art. 62 da Lei 8.213/1991 sem marca | `conferir-citacoes` | sem marca: conferir na fonte | 41 |

O script não dá nenhum outro alerta nessa minuta. Os avisos esperados: 5 marcas `[CONFERIR]` de citação (da `conferir-citacoes`) e `[DOC]` e `[ENDEREÇO]` como dados que entram pelo sistema do escritório. Na matriz do passo 4, o dossiê de treino ainda mostra a lacuna (falta relatório médico posterior à cessação) e a contradição de data entre D1 e D2, que o advogado resolve ao escolher a data. Qualquer diferença: ajuste e rode de novo.

## 5. Formato da saída

```
CONFERÊNCIA DE DADOS E COERÊNCIA · [caso] · [peça v<n>] · [data]
Li N linhas · cliente: [primeiro nome] · gênero: [..] · documentos: doc. 1 a N
ALERTAS ABERTOS
  1. [tipo] · linha N · "[trecho curto]" · correção proposta: ...
COERÊNCIA (o advogado decide)
  - [pedido sem fundamento | fato sem pedido | contradição com o dossiê | lacuna] · ...
DOCUMENTOS · REQUISITOS [CONFERIR] · PADRÃO DA FICHA
  - ...
Avisos: [marcas de citação, dados que entram pelo sistema, documento da lista não citado]
pecas.csv: dados = [ok | com-alerta]
```

Na seção "Dados e coerência" do arquivo de conferência vão: a tabela de alertas (com a coluna "Decisão": corrigido na v<n+1>, mantido por decisão de [função] em AAAA-MM-DD, aberto), a matriz do passo 4, os requisitos com `[CONFERIR]` e o padrão.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Saída do script (rascunho) | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD-dados.md` |
| Seção "Dados e coerência" | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md` |
| Versão corrigida, com o ok | `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n+1>.md` |
| Coluna `dados` (e a etapa `conferida`, se couber) | `escritorio/07-operacao/juridico/pecas.csv` |
| Lista de requisitos da peça (modo adaptar) | `escritorio/04-base/juridico/modelos/<peca>/conferencia.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

Sem pasta aberta: o relatório sai no chat, a versão corrigida vai em bloco para copiar, e a linha do `pecas.csv` vai como tabela para colar.

## 7. Solo e equipe

**Solo:** rode antes de ler a minuta, não depois. A leitura do advogado fica para a tese e a escrita, e os erros que cansam já estão apontados.

**Equipe:** quem redige roda a conferência antes de mandar para a revisão, e o revisor recebe a peça com o relatório. Se o mesmo tipo de alerta volta sempre do mesmo jeito (peça aproveitada com nome de outro cliente), a conversa é sobre o modelo: a peça boa vira habilidade própria pela `peca-vira-habilidade` (se instalada), com as variáveis no lugar certo.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Nome de outro cliente na peça | Exposição de outro caso e peça desacreditada | Nome em papel de parte comparado com o caso |
| Gênero trocado em alguns trechos | Sinal de peça aproveitada sem revisão | Contagem de todas as palavras de parte |
| Duas datas para o mesmo fato | O pedido pode pedir desde a data errada | Datas agrupadas por fato |
| Valor da causa diferente | Emenda da inicial, rito errado | Valor da causa conferido em todos os pontos |
| "Doc. 7" que não existe | Argumento sem prova e intimação para juntar | Lista de documentos contra cada citação |
| Pedido sem fato | Pedido negado e peça mais fraca | Matriz pedido, fundamento, fato e prova |
| Marcação esquecida no texto | `[NOME]` ou `{CAMPO}` no processo | Marcações procuradas linha por linha |
| Treino no registro real | Peça que não existe no `pecas.csv` | Pasta `_treino/` |

## 9. Próximo passo

- Citações da mesma peça: `conferir-citacoes` (se instalada; sem ela, nenhuma citação perde a marca e o advogado confere cada uma na fonte).
- Peça com `dados = ok` e `citacoes = verde`: etapa `conferida` e a fila do advogado (`/motor-juridico:fila`).
- Peça aprovada: `preparar-protocolo` (se instalada).
- O mesmo erro de peça aproveitada se repete: `peca-vira-habilidade` (se instalada).

## Referências desta habilidade

- `scripts/conferir_dados.py`: a conferência mecânica (nomes, gênero, datas, valores, documentos, pedidos, marcações). Rode no passo 2.
- `references/coerencia-e-requisitos.md`: a matriz pedido, fundamento, fato e prova; sobra de outro caso; requisitos formais `[CONFERIR]`; o padrão da ficha; dado sensível; como fechar o `dados`. Leia nos passos 4 a 6.
- `assets/minuta-com-erros.md`: a minuta de treino do caso 1 (Marta), com os dez erros do gabarito de `../../docs/casos-ficticios.md`. Use no modo treino e no `/motor-juridico:comecar`.
