---
name: banco-de-teses-vivo
description: >
  Mantém as teses do escritório vivas: cada tese em um arquivo com a frase da tese, quando usar,
  o fundamento com a jurisprudência da base e a data da conferência, os argumentos na ordem, a
  resposta da outra parte, as peças que a usam e o resultado de cada caso por órgão julgador. Um
  script resume o desempenho de cada tese a partir do pecas.csv e do registro de resultados, em
  números absolutos, e aponta quando ela enfraquece (derrotas seguidas no mesmo juízo, queda,
  fundamento vencido ou superado). Quem decide o que fazer com a tese é o advogado. Use quando o
  advogado disser "escreve a nossa tese de restabelecimento", "saiu a sentença do caso da Marta,
  registra", "como essa tese está indo?", "essa tese ainda funciona no 3º juizado?". Não use para
  escolher a tese de um caso (use estrategia-do-caso) nem para pesquisar jurisprudência nova (use
  trazer-pesquisa, com a pesquisa do Jus IA).
---

# Banco de teses vivo

> Cada tese do escritório com o fundamento conferido, o lugar onde ganhou e onde perdeu, e o aviso de quando começou a perder.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Pesquisa e base de jurisprudência: `../../docs/pesquisa-jus-ia.md`. Produção e `pecas.csv`: `../../docs/producao.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

A advogada usa a mesma tese de restabelecimento há três anos e lembra que "ganha quase sempre". O registro mostra outra coisa: no 3º juizado, perdeu as duas últimas, e o julgado que sustenta a tese foi conferido há oito meses. A memória guarda as vitórias; o banco guarda tudo.

**Regras fixas desta habilidade:**
1. **A tese é do advogado.** O banco guarda, mede e avisa. Escolher a tese de um caso é da `estrategia-do-caso`, com o advogado; mudar a situação de uma tese (em uso, em observação, enfraquecida, aposentada) é só do advogado.
2. **Fundamento só com fonte e conferência.** Toda citação da tese fica marcada `[CONFERIR: ...]` até a conferência na fonte, e vale pela `validade_da_conferencia`. Julgado vem da base do escritório ou de pesquisa no Jus IA, nunca de memória.
3. **Resultado é contagem do que aconteceu.** Números absolutos ("perdeu 2 de 3"), nada de percentual, "chance de êxito" ou previsão. Com menos de 5 decisões, a habilidade diz que a amostra é pequena.
4. **Sem dado de cliente na base.** O arquivo da tese guarda só o código do caso e da peça. Nome, detalhe e documento ficam no caso; o registro de resultados fica em `07-operacao/`, fora do Projeto.
5. **O contra também entra.** Julgado contrário e derrota ficam no arquivo da tese, marcados; é deles que a `advogado-do-diabo` se alimenta.

## 1. Quando usar

**Use quando:**
- O escritório quer escrever uma tese que já usa (modo "nova tese").
- Chegou uma decisão num caso que usou uma tese (modo "registrar resultado").
- O advogado quer saber como uma tese está indo, ou o mês virou (modo "desempenho").
- O script apontou sinal de enfraquecimento, ou a `monitor-de-precedentes` avisou que um tema da tese mudou (modo "revisar").
- A `estrategia-do-caso`, a `minutar-peca` ou uma habilidade própria precisam do fundamento e da situação da tese (modo "consultar").
- O `agente-juridico` chama no ciclo, ou alguém treina com os casos fictícios.

**Não use quando:**
- O pedido é escolher a tese de um caso: `estrategia-do-caso` (se instalada; sem ela, o advogado decide e a habilidade registra em `estrategia.md`).
- O pedido é pesquisar julgado novo: pesquisa no Jus IA e `trazer-pesquisa` (se instalada) para guardar na base.
- O pedido é o mapa do tema por tribunal: `mapa-jurisprudencial` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`), o `nicho.md` (se existir) e `aprendizados-juridico.md`.
2. **Leia o banco:** `escritorio/04-base/juridico/teses/` (as teses), `04-base/juridico/jurisprudencia/` (os temas que elas citam, com a data da conferência).
3. **Leia os registros:** `escritorio/07-operacao/juridico/pecas.csv` (que peças usaram cada tese) e `escritorio/07-operacao/juridico/resultados.csv` (as decisões). Sem `resultados.csv`, ele nasce no primeiro resultado registrado, só com a linha de títulos da seção 5.
4. **Treino:** com os casos fictícios, copie os arquivos de `assets/` para `escritorio/07-operacao/_treino/juridico/banco-de-teses-vivo/` e trabalhe lá. Nunca rode `--atualizar` sobre os arquivos de `assets/`.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `tribunais_principais` |
| Melhora | J: `validade_da_conferencia` · também: `quem_assina`, `doutrina_de_referencia` |

Sem `tribunais_principais`, pergunte: "Em que juízos e tribunais os casos de vocês mais tramitam?"; é a lista de órgãos que o registro de resultados usa. Sem `validade_da_conferencia`, use 90 dias e avise.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Nova tese | Tese que o escritório já usa e não está escrita | Entrevista e as peças que a usam | `04-base/juridico/teses/<tese>.md` |
| Registrar resultado | Chegou uma decisão | O caso, a peça e a decisão | Linha nova em `resultados.csv` |
| Desempenho | A pedido ou todo mês | Os dois registros e as teses | O resumo no chat; com o ok, os blocos de resultado e desempenho nas teses |
| Revisar | Sinal de enfraquecimento | O sinal e a tese | A decisão do advogado registrada na tese |
| Consultar | Outra habilidade pede | O nome da tese | Fundamento, situação, sinais em aberto |
| No ciclo | O agente chama (uma vez por mês, ou quando chega resultado) | Os registros | Sinais em "PARA DECIDIR"; nada gravado sem o ok |
| Treino | Casos fictícios | `assets/` | O mesmo, em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | As áreas e os tribunais | A lista de teses a escrever e os nomes dos órgãos |

### Modo nova tese
Pergunte, uma de cada vez:
1. "Como você diria essa tese a um colega, em uma frase?"
2. "Em que caso ela serve? E em qual parece servir e não serve?"
3. "Qual é o fundamento: que norma e que julgados da base?" (mostre os temas de `jurisprudencia/` que parecem servir, com a data da conferência; o que não está na base vira busca no Jus IA)
4. "Em que ordem os argumentos entram na peça?"
5. "O que a outra parte costuma responder, e como vocês respondem?"
6. "Que peças usam esta tese?"
Escreva no formato de `assets/modelo-tese.md` (seção 4). O nome do arquivo é o nome da tese em minúsculas com hífen, e é o mesmo que vai na coluna `tese` do `pecas.csv`. Toda citação ainda não conferida leva a marca. Mostre inteira e grave com o ok, com `situacao: em uso`.

### Modo registrar resultado
1. Pergunte o que faltar, uma coisa por vez: "Qual caso e qual peça?" (o `id` do `pecas.csv`), "Qual órgão julgou?" (mostre os nomes já usados em `resultados.csv` e use o mesmo texto: "3º JEF BH" não pode virar "Terceiro Juizado"), "Primeira instância ou recurso?", "Qual foi o resultado?" (procedente, parcial, improcedente, acordo, extinto, desistencia), "A decisão enfrentou a tese, ou decidiu por outro motivo?" (sim, nao, em-parte).
2. Observação curta, sem dado de saúde nem nome: "juízo seguiu a perícia administrativa".
3. Mostre a linha e grave com o ok em `resultados.csv`. Resultado de recurso é linha nova, com a mesma peça.
4. Rode o desempenho só da tese (`--tese`) e mostre se apareceu sinal.
5. Notícia ruim ao cliente não é daqui: indique o advogado e, se instalado, o motor-experiencia (a notícia ruim é por ligação).

### Modo desempenho
Rode, com o caminho da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/desempenho_teses.py" --pecas "escritorio/07-operacao/juridico/pecas.csv" --resultados "escritorio/07-operacao/juridico/resultados.csv" --teses "escritorio/04-base/juridico/teses" --validade <validade_da_conferencia>
```

O script lê os dois .csv (vírgula ou ponto e vírgula, com ou sem BOM, datas AAAA-MM-DD ou DD/MM/AAAA) e mostra, por tese: as peças no registro por etapa, as decisões, a tabela por órgão julgador (ganhou, em parte, perdeu, outras) e os sinais da seção 6. Falta arquivo ou coluna obrigatória: sai com código 1 e diz qual. Mostre o resumo. Com o ok, rode de novo com `--atualizar`: o script reescreve só os blocos entre `<!-- resultados: inicio -->` e `<!-- resultados: fim -->` e entre `<!-- desempenho: inicio -->` e `<!-- desempenho: fim -->` em cada tese; o resto do arquivo não muda. Para uma tese só: `--tese <nome>`.

### Modo revisar
Para cada sinal, mostre o que ele quer dizer e o que o advogado pode decidir (seção 6). Pergunte: "O que você quer fazer com esta tese?". Registre a resposta na seção 9 do arquivo da tese (data, sinal, decisão do advogado) e, se ele decidiu, mude a `situacao` no cabeçalho e acrescente uma linha no histórico. Se a tese é usada por uma habilidade própria (seção 6 do arquivo da tese), avise que ela precisa de revisão pela `peca-vira-habilidade` (se instalada). Pesquisa nova: indique o Jus IA e a `trazer-pesquisa`; tema vigiado: `monitor-de-precedentes` (se instaladas).

### Modo consultar
Mostre, da tese pedida: a frase, a situação, o fundamento com a data e a cor de cada conferência (citação vencida volta a ser marcada, `../../docs/citacoes.md`, regra 5), os sinais em aberto e as decisões do advogado. Tese `aposentada`: diga que o escritório decidiu não usar mais, e quando. Nada aqui escolhe a tese do caso.

### Modo no ciclo
1. O agente chama no primeiro ciclo do mês, ou quando há linha nova em `resultados.csv`. Não pergunte nada.
2. Rode o desempenho sem `--atualizar`.
3. Devolva ao agente, para "PARA DECIDIR": cada sinal novo, em uma linha ("restabelecimento: perdeu as duas últimas no 3º JEF BH"), e as peças protocoladas há mais de 180 dias sem resultado registrado. A situação da tese nunca muda no ciclo.

### Modo treino
Copie `assets/teses/`, `assets/pecas-exemplo.csv` e `assets/resultados-exemplo.csv` para `escritorio/07-operacao/_treino/juridico/banco-de-teses-vivo/` e rode o desempenho lá, com `--hoje 2026-04-20`. O que tem que aparecer:
- `restabelecimento-incapacidade`: no 3º JEF BH, perdeu as duas últimas; queda (3 nas mais antigas, 1 nas mais recentes); o julgado das peças de origem sem conferência; o julgado contra com conferência vencida, amarelo e superado em parte; a P-2025-0108 protocolada há mais de 180 dias sem resultado.
- `rescisao-divida-reconhecida`: amostra pequena e conferência vencida.
- `partilha-consensual` e `tese-sem-arquivo`: tese usada sem arquivo.
- Aviso: o resultado da C-2025-0300 cita uma peça que não está no `pecas.csv`.
Depois, com `--atualizar` na cópia, confira que só os dois blocos mudaram.

### Modo adaptar
Leia `areas`, `tribunais_principais`, `pecas_mais_feitas` e `nicho.md`. Proponha a lista de teses que o escritório já usa e ainda não escreveu (uma por peça mais feita, pelo que o advogado disser) e a lista dos órgãos julgadores com o nome padrão para o registro. Mostre e grave com o ok: as teses entram como arquivos novos pelo modo nova tese; os nomes padrão dos órgãos vão para o campo `tribunais_principais` da ficha jurídica, com linha no histórico da ficha, e passam a ser os nomes do registro de resultados.

### Passo final de todos os modos. Aprender
Pergunte: "Alguma coisa no banco você faria diferente?". Correção vira regra curta e, com o ok, entra em `aprendizados-juridico.md` (por exemplo: "resultado de acordo não conta como derrota nem como vitória"). Correção que pede percentual ou previsão de ganho: explique por que não pode guardar e proponha a contagem.

## 4. O arquivo da tese

Em `escritorio/04-base/juridico/teses/<tese>.md`, no formato de `assets/modelo-tese.md`:

| Seção | O que guarda | Quem escreve |
|---|---|---|
| Cabeçalho | `tese`, `area`, `versao`, `revisado_em`, `dono`, `situacao` | a habilidade; a `situacao`, só o advogado |
| 1. A tese em uma frase | A tese como o advogado diria | o advogado |
| 2. Quando usar e quando não usar | O caso típico e o parecido que não serve | o advogado |
| 3. Fundamento | Tabela: citação (com a marca até conferir), base, a favor ou contra, conferida em, cor, situação | a habilidade, da base; a conferência é da `conferir-citacoes` |
| 4. Argumentos, na ordem | A ordem em que a tese entra na peça | o advogado |
| 5. O que a outra parte responde | Resposta provável e como responder | o advogado, a `advogado-do-diabo` |
| 6. Peças e habilidades que usam | As peças e as habilidades próprias | a habilidade |
| 7. Resultados por caso | Bloco do script: data, caso (código), peça, órgão, instância, resultado, tese enfrentada | o script |
| 8. Desempenho por órgão julgador | Bloco do script: a tabela por órgão e os sinais | o script |
| 9. Sinais e decisões do advogado | Data, sinal, decisão | a habilidade, com a palavra do advogado |
| 10. Histórico | O que mudou na tese | a habilidade |

Exemplos preenchidos: `assets/teses/restabelecimento-incapacidade.md` e `assets/teses/rescisao-divida-reconhecida.md` (fictícios).

## 5. O registro de resultados

`escritorio/07-operacao/juridico/resultados.csv`, uma linha por decisão, separado por vírgula (o script também lê o salvo pelo Excel):

```
data_decisao,id_peca,codigo_caso,tese,orgao_julgador,instancia,resultado,tese_enfrentada,observacao
```

| Coluna | O que vai |
|---|---|
| `data_decisao` | AAAA-MM-DD |
| `id_peca` | O `id` do `pecas.csv` (P-AAAA-NNNN) |
| `codigo_caso` | C-AAAA-NNNN |
| `tese` | O nome da tese, igual ao arquivo |
| `orgao_julgador` | O nome padrão do escritório para aquele juízo, câmara ou colegiado |
| `instancia` | `primeira`, `recurso`, `superior` |
| `resultado` | `procedente`, `parcial`, `improcedente`, `acordo`, `extinto`, `desistencia` |
| `tese_enfrentada` | `sim`, `nao` (decidiu por outro motivo), `em-parte` |
| `observacao` | Uma frase, sem nome e sem dado sensível |

Só conta para ganhou e perdeu a decisão em que a tese foi enfrentada. Acordo, extinção, desistência e decisão por outro motivo ficam em "outras".

## 6. Os sinais de enfraquecimento

| Sinal (do script) | O que quer dizer | O que o advogado pode decidir |
|---|---|---|
| Perdeu as duas últimas no mesmo órgão | Aquele juízo pode ter mudado de entendimento | Ler as duas decisões; pesquisar o órgão no Jus IA; reforçar o argumento para aquele juízo; usar com distinção |
| Mais derrotas que vitórias (3 ou mais decisões) | A tese não está convencendo | Revisar argumentos com a `advogado-do-diabo`; trocar fundamento; `em observação` |
| Queda (6 ou mais decisões) | Funcionava e parou de funcionar | Procurar a virada: `monitor-de-precedentes`, `mapa-jurisprudencial` |
| Fundamento sem conferência ou vencido | A tese se apoia em citação que ninguém conferiu agora | `conferir-citacoes`; pesquisa nova no Jus IA |
| Fundamento amarelo, vermelho ou superado | O apoio mudou | Trocar o fundamento antes da próxima peça |
| Julgado contra na base | Existe resposta pronta para a outra parte | Enfrentar na peça; `advogado-do-diabo` |
| Tese usada sem arquivo | O escritório usa uma tese que não escreveu | Modo nova tese, ou corrigir o nome no registro |
| Protocolada há mais de 180 dias sem resultado | O registro de resultados está atrasado | Registrar o que já chegou |

Nenhum sinal muda a tese sozinho. Amostra pequena (menos de 5 decisões enfrentadas) aparece escrita no resumo, para ninguém tirar conclusão de dois casos.

## 7. Formato da saída

```
BANCO DE TESES · AAAA-MM-DD · validade da conferência: N dias
## [tese] · [area] · situação: [situacao]
Peças no registro: N (etapa N, ...). Decisões: N, das quais N com a tese enfrentada.
| Órgão julgador | Decisões | Ganhou | Em parte | Perdeu | Outras | Última |
Sinais para o advogado olhar:
- ...
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Teses | `escritorio/04-base/juridico/teses/<tese>.md` |
| Registro de resultados | `escritorio/07-operacao/juridico/resultados.csv` |
| Blocos de resultado e desempenho (com o ok) | Dentro de cada tese, entre os marcadores |
| Decisões do advogado sobre a tese | Seção 9 e cabeçalho (`situacao`) da tese, com linha no histórico |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O `pecas.csv` não muda por esta habilidade: ela só lê a coluna `tese`. Sem pasta aberta: a tese e a linha de resultado saem no chat, em bloco, com o caminho onde ficariam; o desempenho precisa do script.

## 9. Solo e equipe

**Solo:** registre o resultado no dia em que a decisão chega, junto com a leitura dela; leva um minuto e é o que faz o banco valer. Rode o desempenho uma vez por mês. **Equipe:** quem lê as decisões registra o resultado; o advogado responsável pela área é o dono das teses e o único que muda a situação. Na reunião da equipe, os sinais do mês entram na pauta.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Essa tese ganha sempre", de memória | O escritório insiste onde está perdendo | Resultado por caso e por órgão, contado |
| Percentual de êxito em dois casos | Conclusão sem base, que pode virar promessa ao cliente | Números absolutos e aviso de amostra pequena |
| Fundamento conferido há um ano | Peça apoiada em julgado superado | Validade da conferência e sinal de vencida |
| Derrota apagada do arquivo | A `advogado-do-diabo` fica sem o contra | O contra entra e fica |
| Nome do cliente no arquivo da tese | Dado de cliente na base que vai para o Projeto | Só o código; o registro fica em `07-operacao/` |
| "3º JEF" e "Terceiro Juizado" como órgãos diferentes | Desempenho partido e sinal que não aparece | Nome padrão do órgão, mostrado no registro |
| A IA aposentando a tese | Decisão de estratégia fora do advogado | Situação muda só com o advogado |

## 11. Próximo passo

- Sinal de órgão ou de queda: pesquisa nova no Jus IA e `trazer-pesquisa`; `monitor-de-precedentes` e `mapa-jurisprudencial` (se instalados).
- Fundamento vencido: `conferir-citacoes` (se instalada).
- Contra na base: `advogado-do-diabo` (se instalada), antes da próxima peça.
- Tese mudou e tem habilidade própria: `peca-vira-habilidade`, modo "revisar".
- Caso novo: a `estrategia-do-caso` consulta o banco; a escolha é do advogado.

## Referências desta habilidade

- `assets/modelo-tese.md`: o formato do arquivo de tese, com os marcadores do script. Leia no modo nova tese.
- `assets/teses/restabelecimento-incapacidade.md` e `assets/teses/rescisao-divida-reconhecida.md`: duas teses fictícias do Escritório Modelo. Use no treino e como exemplo de nível.
- `assets/pecas-exemplo.csv` e `assets/resultados-exemplo.csv`: o registro de peças e o de resultados do treino. Copie para `_treino/` antes de rodar.
- `scripts/desempenho_teses.py`: o resumo do desempenho e os sinais. Rode no modo desempenho, no registrar resultado e no ciclo.
