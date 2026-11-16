---
name: pecas-em-lote
description: >
  Contencioso de massa: a planilha dos casos mais a habilidade própria da peça viram um lote de
  minutas. Um script lê a planilha (vírgula ou ponto e vírgula, salva pelo Excel ou não), confere
  cada linha contra o mapa da peça (código, área, dado obrigatório, formato de data, valor e
  opção) e monta só as linhas que passam; a linha com dado faltando ou de outra área não sai.
  Cada minuta passa pela conferência de dados e de citações, e o relatório do lote mostra o que
  saiu, o que foi barrado e por quê. A tese do lote é do advogado. Use quando o advogado disser
  "monta as iniciais desses quarenta casos", "roda o lote da semana", "tenho uma planilha com os
  segurados", "confere a planilha antes de montar". Não use para uma peça só (use a habilidade
  própria ou minutar-peca) nem para criar a habilidade da peça (use peca-vira-habilidade).
---

# Peças em lote

> Quarenta casos iguais viram quarenta minutas iguais no que deve ser igual, e diferentes só no que muda de um cliente para outro. A linha que não fecha fica de fora, com o motivo.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção, etapas e `pecas.csv`: `../../docs/producao.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md` (o lote). Aprendizados: `../../docs/aprender-com-o-uso.md`.

Segunda, 8h. Quarenta segurados com o benefício cortado pelo mesmo motivo, todos para o mesmo juizado. O estagiário abre a inicial boa e faz quarenta cópias, trocando os dados à mão. Na décima sétima, a data de cessação ficou a da décima sexta; na vigésima, a cliente virou "o autor"; uma era trabalhista e entrou junto.

**Regras fixas desta habilidade:**
1. **Só com habilidade própria da peça.** O lote sai do mapa da peça (`04-base/habilidades-do-escritorio/<peca>/references/mapa-da-peca.md`). Sem ela, primeiro a `peca-vira-habilidade`. Lote nunca é a `minutar-peca` rodada quarenta vezes.
2. **A tese do lote é do advogado, registrada.** O script não grava sem `--tese` e `--decisao` (quem definiu e quando). Caso que não cabe na tese sai do lote e vai para o advogado.
3. **Linha com dado faltando ou fora do padrão não sai.** A habilidade nunca completa, estima ou copia um dado de outra linha. A linha barrada volta quando alguém corrigir a planilha.
4. **Toda minuta é conferida.** Cada uma passa pela `conferir-peca` e pela `conferir-citacoes`, e nenhuma vai para o advogado com vermelho. Toda citação sai marcada.
5. **Aprovar, assinar e protocolar é por peça, do advogado.** O lote facilita a leitura; não existe "aprovar o lote inteiro" pela IA.

## 1. Quando usar

**Use quando:**
- O escritório tem muitos casos iguais para a mesma peça (o campo `pecas_em_massa` da ficha diz quais) e a peça já tem habilidade própria.
- Chegou a planilha da semana e o advogado quer saber quais linhas estão prontas antes de montar (só conferência).
- O `agente-juridico` achou uma planilha de lote na pasta de entrada (modo "no ciclo", só conferência).
- Alguém quer treinar com o lote fictício (modo "treino").
- A `adaptar-juridico` pede as colunas da planilha para o nicho (modo "adaptar").

**Não use quando:**
- É uma peça só: a habilidade própria da peça, ou a `minutar-peca`.
- A peça não tem habilidade própria: `peca-vira-habilidade` (se instalada; sem ela, as peças saem uma a uma pela `minutar-peca`).
- Os casos não estão decididos: a tese de cada um é da `estrategia-do-caso`, com o advogado.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`), o `nicho.md` (se existir) e `aprendizados-juridico.md`.
2. **Ache a habilidade própria** da peça em `escritorio/04-base/habilidades-do-escritorio/<peca>/` e leia o mapa: as variáveis (cada uma é uma coluna da planilha), a área, as teses e as exceções que param.
3. **Leia o registro** (`escritorio/07-operacao/juridico/pecas.csv`), para não abrir linha nova para peça que já está lá.
4. **Dados.** A planilha do lote guarda o mínimo que a peça usa: código, primeiro nome, área e as variáveis do caso. Nada de CPF, endereço, número de benefício ou senha; isso sai do sistema do escritório no protocolo. Caso real só em conta profissional ou de equipe.
5. **Treino:** com o lote fictício, tudo grava em `escritorio/07-operacao/_treino/juridico/`, e o registro de peças do lote fica em `_treino/juridico/pecas-em-lote/pecas.csv`.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `pecas_em_massa`, `quem_revisa` |
| Melhora | J: `nome_dos_arquivos` · também: `quem_redige`, `validade_da_conferencia` |

Sem `pecas_em_massa`, pergunte: "Que peça sai em lote no escritório?". Sem `quem_revisa`, pergunte quem lê as minutas do lote antes de aprovar; a fila precisa de um nome de função.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Planilha nova | O escritório vai montar a planilha | O mapa da peça | O modelo da planilha (as colunas, com tipo e regra) |
| Conferir | Antes de montar | A planilha e a habilidade | A tabela do lote, sem gravar nada |
| Montar | Com o ok do advogado | A planilha, a habilidade, a tese e a decisão | Minutas, relatório do lote, linhas do `pecas.csv`, conferências, fila |
| No ciclo | O agente acha `lote-*.csv` na entrada | A planilha | Só a conferência, em "PARA DECIDIR" |
| Treino | Lote fictício ou "é teste" | `assets/lote-de-exemplo.csv` | O mesmo do montar, em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | O nicho e o mapa | Os títulos e exemplos das colunas para o nicho |

### Passo 1. A peça e a habilidade
Pergunte, se não estiver claro: "Qual peça sai neste lote?". Confira se existe a habilidade própria. Não existe: pare e indique a `peca-vira-habilidade`.

### Passo 2. A planilha
Pergunte: "Já tem a planilha do lote, ou monto o modelo das colunas?". Sem planilha, gere o modelo pela seção 4 a partir do mapa e entregue como .csv com a linha de títulos e uma linha de exemplo fictícia. Com a planilha, grave em `escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.csv`. Coluna com CPF, endereço ou número de benefício: avise, não repita e peça a planilha sem ela.

### Passo 3. A tese do lote
Pergunte: "Qual tese vale para este lote? Todos os casos da planilha cabem nela?". A resposta do advogado é a decisão: anote quem decidiu e a data. A tese precisa estar na seção Teses do mapa da peça; se não estiver, pare e pergunte (pode ser outra peça, ou a habilidade precisa de revisão pela `peca-vira-habilidade`). Caso que o advogado disser que não cabe: tire da planilha e registre em "fora do lote", com o motivo.

### Passo 4. Conferir a planilha
Rode, com o caminho da pasta desta habilidade, o da planilha e o da habilidade própria:

```
python3 "<pasta desta habilidade>/scripts/montar_lote.py" "escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.csv" "escritorio/04-base/habilidades-do-escritorio/<peca>" --tese <tese> --raiz "escritorio/07-operacao/juridico" --so-conferir
```

O script mostra a tabela do lote: cada linha com "monta" ou "barrada", o motivo da barrada e os alertas. Nada é gravado. Mostre a tabela e o resumo ("40 linhas: 37 montam, 3 barradas"), e para cada barrada diga o que corrigir. Pergunte: "Monto as que passaram, ou corrige as barradas antes?".

Falta de arquivo ou de coluna obrigatória: o script sai com código 1 e a lista das colunas que a planilha precisa. Nenhuma linha passou: código 2, e nada é montado.

### Passo 5. Montar
Com o ok, rode o mesmo comando sem `--so-conferir` e com a decisão e o registro:

```
python3 "<pasta desta habilidade>/scripts/montar_lote.py" "escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.csv" "escritorio/04-base/habilidades-do-escritorio/<peca>" --tese <tese> --raiz "escritorio/07-operacao/juridico" --decisao "<função de quem decidiu>, AAAA-MM-DD" --registrar --responsavel <quem_redige>
```

O script grava cada minuta em `casos/<codigo>/minutas/<peca>-v<n>.md` (a próxima versão livre, nunca por cima), com o cabeçalho "Antes de protocolar" (lote, linha, tese, quem decidiu, citações marcadas, alertas e as conferências com `- [ ]`), o relatório do lote em `lotes/AAAA-MM-DD-<peca>.md` e, com `--registrar`, uma linha por minuta no `pecas.csv` (`origem = lote`, `etapa = minuta`, `habilidade_usada = <peca>`, `citacoes = nao-conferidas`, `dados = nao-conferidos`). Caso que já tem linha aberta da mesma peça no `pecas.csv` não ganha outra: o relatório diz qual linha atualizar.

### Passo 6. Conferir cada minuta
Para cada minuta montada, rode a `conferir-peca` e a `conferir-citacoes` (se instaladas), gravando em `casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md`. Para não conferir quarenta vezes a mesma coisa:
- **Citações do modelo** são as mesmas em todas as minutas: confira uma vez (na base do escritório, dentro de `validade_da_conferencia`) e aplique o resultado a todas. Citação que precisa de pesquisa entra uma vez só na lista "pesquisar no Jus IA" do lote.
- **Dados de cada cliente** são conferidos minuta a minuta, contra os documentos do caso: é aí que mora o erro do lote.
Atualize no relatório as colunas "conferir-peca" e "conferir-citacoes" e, no `pecas.csv`, `citacoes` e `dados` de cada linha. Minuta com vermelho ou alerta aberto não vai para a fila como pronta: vai com `revisor: conferir` ou fica para o advogado decidir. Sem as duas habilidades, o cabeçalho de cada minuta é a lista do que conferir à mão.

### Passo 7. A fila do advogado
Cada minuta conferida vira um item em `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-<peca>.md`, no formato de `../../docs/agentes-e-fila.md`, com `revisor: pendente`, o relatório da conferência em `antes_de_enviar` e `motivo: lote AAAA-MM-DD-<peca>, linha N`. O relatório do lote vai junto, como a visão geral para quem revisa. O .docx de cada uma sai pelo script da `minutar-peca` (se instalada) depois da conferência; o script não gera com citação marcada.

### Passo 8. Aprender
Pergunte: "Alguma coisa no lote você faria diferente na próxima?". Barrada que se repete por formato (data sempre em outro formato, área escrita de outro jeito) vira orientação no modelo da planilha. Correção que o advogado fez em várias minutas do lote é correção da habilidade própria: ofereça a `peca-vira-habilidade`, modo "corrigir". Regra que vale para toda peça vai para `aprendizados-juridico.md`, com o ok.

### Modo no ciclo
1. O `agente-juridico` acha `lote-*.csv` em `07-operacao/juridico/entrada/` ou uma planilha nova em `07-operacao/juridico/lotes/`. Não pergunte nada.
2. Rode só o passo 4 (`--so-conferir`). Nunca monte no ciclo: a decisão da tese do lote é do advogado.
3. Devolva ao agente, para "PARA DECIDIR" no resumo: a peça, quantas linhas montam, quantas barradas e por quê, e a pergunta "Qual tese vale para este lote?".

### Modo treino
Rode com `assets/lote-de-exemplo.csv` e o mapa de exemplo da própria habilidade (`assets/mapa-peticao-inicial-restabelecimento.md`, a mesma peça do exemplo da `peca-vira-habilidade`), com `--raiz "escritorio/07-operacao/_treino/juridico"` e `--tese restabelecimento-incapacidade`. O gabarito (`../../docs/casos-ficticios.md`, o lote):

| Linha | Código (treino) | Nome curto | O que tem que acontecer |
|---|---|---|---|
| 2 | C-2026-9001 | Jair | monta; "o autor"; sem tutela |
| 3 | C-2026-9002 | Cleide | monta; "a autora"; com o fato 1.6, o fundamento 2.4 e o pedido de tutela em primeiro |
| 4 | C-2026-9003 | Rosa | **barrada:** falta `data_cessacao` |
| 5 | C-2026-9004 | Edson | **barrada:** área trabalhista, a habilidade é de previdenciário |
| 6 | C-2026-9005 | Nair | monta, mesmo com "Previdenciário", "F" e "NAO" escritos de outro jeito |

E nas três que montam: as citações do modelo com `[CONFERIR]` (o julgado das peças de origem sai vermelho na conferência, porque não existe); nenhum CPF; a qualificação como campo de quem protocola. Qualquer diferença: falta coluna, regra no mapa ou a planilha está fora do formato.

### Modo adaptar
Leia `nicho.md` e o mapa da peça. Proponha, para cada coluna da planilha, o título e o exemplo no vocabulário do escritório (sem mudar o nome da variável, que é o que o script lê), e o formato de data e de valor que a equipe usa. Mostre com `[ALTERADO]` e grave com o ok no modelo da planilha (`escritorio/04-base/juridico/modelos/<peca>/planilha-do-lote.csv`).

## 4. A planilha do lote

| Coluna | Obrigatória | O que vai |
|---|---|---|
| `codigo_caso` | sim | C-AAAA-NNNN, o mesmo do comercial e da experiência; sem repetir no lote |
| `nome_curto` | não | Primeiro nome ou iniciais; vai para o registro, nunca para o corpo da peça |
| `area` | sim | A área do caso; tem de ser a área do mapa |
| `prazo_interno` | não | AAAA-MM-DD, informado por quem pediu (nunca calculado aqui) |
| uma coluna por variável do mapa | as obrigatórias do mapa | O título da coluna é o nome da variável (`data_cessacao`). Datas em AAAA-MM-DD ou DD/MM/AAAA; mês em AAAA-MM ou MM/AAAA; valor em 1.234,56 (com ou sem R$); gênero f ou m; opção só os valores da lista; lista com itens separados por ponto e vírgula, entre aspas se a planilha usa ponto e vírgula |

As variáveis de origem `ficha` (juízo, cidade, assinatura) não vão na planilha: vêm de "Valores do escritório", no mapa. Maiúsculas, acentos e espaços nos títulos não importam (`Data Cessação` vale `data_cessacao`). O exemplo do Escritório Modelo está em `assets/lote-de-exemplo.csv`.

## 5. O que barra e o que só alerta

| Situação | O que acontece |
|---|---|
| `codigo_caso` vazio, fora do formato ou repetido | Barra a linha |
| Área diferente da área do mapa | Barra a linha |
| Variável obrigatória vazia | Barra a linha |
| Data, mês, valor ou número que não se lê; opção fora da lista; gênero que não é f ou m | Barra a linha |
| Valor igual ao exemplo do mapa | Alerta: pode ser cópia do modelo |
| Mesmo valor em todas as linhas numa variável do caso (datas, função) | Alerta: pode ser cópia entre linhas |
| Coluna que não é variável do mapa | Aviso: ignorada |
| Coluna obrigatória que não existe | Nada roda; o script lista as colunas que faltam |
| Tese que não está no mapa, ou sem `--decisao` para gravar | Nada roda |

O script não conhece o direito do caso: quem vê que um caso do lote tem uma exceção que muda a tese é o advogado, no passo 3, e a seção 7 do mapa ("quando parar").

## 6. O relatório do lote

Em `escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.md`: cabeçalho com a habilidade e a versão, a tese, quem decidiu e a planilha; as barradas com o motivo; as montadas com o caminho da minuta, o número de citações marcadas, os alertas e as colunas da conferência (a habilidade preenche no passo 6); e as linhas propostas para o `pecas.csv`. Rodar de novo no mesmo dia gera `-2`, `-3`; nada é apagado.

## 7. Formato da saída

```
LOTE · AAAA-MM-DD-[peca] · habilidade [peca] v[N] · tese [nome] (decidida por [função], AAAA-MM-DD)
[N] linhas: [N] montadas, [N] barradas
Barradas: linha [N] ([codigo]): [motivo]; ...
Conferência: citações do modelo [cor] · dados: [N] ok, [N] com alerta
Pesquisar no Jus IA: [temas, uma vez para o lote]
Fila: [N] minutas para [quem_revisa]; relatório em [caminho]
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A planilha do lote | `escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.csv` |
| Minutas | `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md` |
| Relatório do lote | `escritorio/07-operacao/juridico/lotes/AAAA-MM-DD-<peca>.md` |
| Conferências | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md` |
| Linhas do registro | `escritorio/07-operacao/juridico/pecas.csv` (uma por minuta, `origem = lote`) |
| Fila do advogado | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-<peca>.md` |
| Modelo da planilha (modo adaptar) | `escritorio/04-base/juridico/modelos/<peca>/planilha-do-lote.csv` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

Sem pasta aberta ou sem execução de código, o lote não roda: diga que ele precisa do script e da pasta, e ofereça as peças uma a uma pela habilidade própria.

## 9. Solo e equipe

**Solo:** o lote é onde a advogada sozinha mais ganha tempo, e onde um erro se repete mais. Leia a primeira minuta inteira e, nas outras, o que muda (fatos, datas, valores, gênero), com o relatório do lote ao lado. **Equipe:** quem monta a planilha não é quem confere os dados; o estagiário roda o lote e a conferência, e quem revisa (`quem_revisa`) recebe as minutas na fila. Se várias minutas voltam com a mesma correção, o problema é da habilidade própria, não do lote.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Copiar a peça boa quarenta vezes à mão | Data, nome e gênero de outro cliente | O modelo do mapa, preenchido por variável |
| Linha com dado faltando que sai "para completar depois" | Peça protocolada sem a data de cessação | Regra fixa 3: linha barrada |
| Caso trabalhista no lote de previdenciário | Peça errada no juízo errado | A área do mapa barra a linha |
| Tese escolhida pelo lote | A IA decide o caminho de quarenta casos | `--tese` e `--decisao` do advogado |
| A mesma citação conferida quarenta vezes, ou nenhuma | Tempo perdido, ou citação vermelha em toda peça | Citação do modelo conferida uma vez; dados de cada cliente, minuta a minuta |
| Duas linhas no registro para a mesma peça | Rotina e status contando em dobro | O script não abre linha nova para peça que já está aberta |

## 11. Próximo passo

- Conferência: `conferir-peca` e `conferir-citacoes` (se instaladas).
- .docx de cada minuta conferida: o script da `minutar-peca` (se instalada).
- Depois da aprovação: `preparar-protocolo` (se instalada), uma por peça.
- Correção repetida nas minutas: `peca-vira-habilidade`, modo "corrigir".
- Resultado dos casos do lote, quando chegar: `banco-de-teses-vivo` (se instalada).

## Referências desta habilidade

- `assets/lote-de-exemplo.csv`: o lote fictício de cinco segurados, com as duas linhas que devem ser barradas. Use no modo treino e como modelo de planilha.
- `assets/mapa-peticao-inicial-restabelecimento.md`: cópia do mapa da habilidade de exemplo, para o treino funcionar sem a `peca-vira-habilidade`. Use só no treino.
- `scripts/montar_lote.py`: confere a planilha e monta o lote. Rode nos passos 4 e 5.
