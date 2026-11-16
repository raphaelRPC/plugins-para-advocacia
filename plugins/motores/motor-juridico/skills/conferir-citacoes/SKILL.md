---
name: conferir-citacoes
description: >
  Audita todas as citações de uma peça antes de ela chegar ao advogado: leis e artigos, súmulas,
  temas de repercussão geral e de repetitivo, IRDR, julgados, doutrina, trechos entre aspas e
  menções vagas como "entendimento pacífico". Um script extrai tudo numa tabela e cruza com a
  base de jurisprudência do escritório; a conferência na fonte dá a cor (verde, amarelo,
  vermelho, cinza), grava o registro e tira a marca [CONFERIR] só do que ficou verde. O que não
  está na base vira a lista do que pesquisar no Jus IA. Nunca completa número, relator, data ou
  enunciado de memória. Use quando o advogado disser "confere as citações", "essa súmula
  existe?", "checa a jurisprudência da minuta", "tem citação inventada aqui?", "posso tirar os
  conferir?". Não use para nomes, datas, valores e documentos da peça (use conferir-peca).
---

# Conferir citações

> Cada citação da peça passa pela fonte antes de sair: o que foi conferido fica verde e perde a marca, o que não foi fica marcado, e o que não existe não vai para o processo.

Regra de citação (a mais importante do plugin): `../../docs/citacoes.md`. Pesquisa e base: `../../docs/pesquisa-jus-ia.md`. Regras: `../../docs/regras.md`. Etapas e `pecas.csv`: `../../docs/producao.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quinta, 17h. A minuta da Marta tem oito citações, e uma delas é a "Súmula 999 do TRF6", que ninguém lembra de onde veio. Outra é um "entendimento pacífico do STJ" sem número. A citação do artigo 59 está entre aspas e parece certa. A conferência abre o texto compilado e mostra que duas palavras foram trocadas: na peça está "e", na lei está "ou". É o tipo de erro que o juiz acha e o advogado não.

**Regras fixas desta habilidade:**
1. A IA nunca completa número, relator, data, órgão ou enunciado de memória. Sem a fonte na conversa, na base ou num texto oficial salvo, a citação fica marcada e entra na lista do que achar.
2. A marca `[CONFERIR]` sai só da citação que ficou verde, com fonte e data no registro. Amarelo, vermelho e cinza ficam com a marca.
3. Vermelho não vai para a peça: sai, é trocado por outra citação conferida, ou o advogado decide. A habilidade propõe; quem decide é o advogado.
4. Pesquisa de jurisprudência é no Jus IA. Lei e artigo, no portal oficial da legislação. Súmula e tema, no portal do tribunal.
5. O registro da conferência fica com o escritório e não vai para o processo.

## 1. Quando usar

**Use quando:**
- Uma minuta ficou pronta (`minutar-peca`, habilidade própria do escritório ou peça escrita à mão) e precisa de conferência antes do advogado.
- O advogado pergunta se uma súmula, um tema ou um julgado existe e diz o que a peça diz.
- O `agente-juridico` chamou no ciclo (modo "no ciclo"), ou a `pecas-em-lote` (se instalada) passou um lote de minutas.
- O `/motor-juridico:comecar` pediu a conferência da minuta de treino (modo "treino").
- A `adaptar-juridico` (se instalada) pediu as expressões vagas e as fontes do nicho (modo "adaptar").

**Não use quando:**
- O pedido é conferir nome, gênero, datas, valores, documentos citados e pedidos: `conferir-peca`. As duas rodam juntas antes da etapa `conferida`.
- O pedido é pesquisar um tema do zero: a pesquisa é no Jus IA; o resultado entra na base pela `trazer-pesquisa` (se instalada; sem ela, cole o resultado aqui e siga o passo 4 com ele na conversa).
- O pedido é saber como o tema é decidido no tribunal: `mapa-jurisprudencial` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-juridica.md`, e `nicho.md`, se existir (o nicho diz quais tribunais e quais tipos de precedente aparecem mais).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`). Linhas da `conferir-citacoes` que começam com "menção vaga:" viram expressões a mais para o script (opção `--vagas`). Nenhum aprendizado afrouxa as regras fixas.
3. **Ache a base** em `escritorio/04-base/juridico/jurisprudencia/` (formato em `../../docs/pesquisa-jus-ia.md`). Sem base, tudo o que é julgado, súmula e tema vai para a lista do Jus IA.
4. **Ache a peça e o caso:** `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md` (ou o .docx). Peça colada no chat: salve num arquivo de trabalho com o ok, ou rode a extração à mão (seção 4).
5. **Conta de IA:** peça de cliente só em conta profissional ou de equipe. Em conta pessoal, só a minuta de treino.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `validade_da_conferencia` |
| Melhora | J: `tribunais_principais`, `doutrina_de_referencia` |

Sem `validade_da_conferencia`, o script usa 90 dias e avisa; pergunte uma vez: "Por quantos dias uma jurisprudência já conferida vale antes de conferir de novo? Se não tiver um número, fica 90." e ofereça gravar. `tribunais_principais` diz em qual portal procurar primeiro. `doutrina_de_referencia` diz qual edição o escritório usa.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Peça inteira | Minuta pronta | A peça | O relatório (seção 5), o registro e a versão nova sem as marcas verdes |
| Citação solta | "Essa súmula existe?" | Uma citação | A resposta com a fonte, ou o que pesquisar; nada de memória |
| Lote | `pecas-em-lote` (se instalada) passa várias | As minutas do lote | Um registro por minuta e a linha de cada uma no relatório do lote |
| No ciclo | O `agente-juridico` chama | A minuta em `minuta` | Registro gravado, `citacoes` atualizada, linhas para a fila. Não pergunta nada |
| Treino | Minuta de treino ou "é teste" | `../conferir-peca/assets/minuta-com-erros.md` | O mesmo, gravado em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | Expressões vagas do nicho e a ordem dos portais, para aprovar |

Pedido direto ("confere as citações desta minuta"): não faça entrevista. Rode e pergunte só o que faltar.

### Passo 1. A peça e o caso
Se não veio junto, pergunte: "Qual é a peça e de qual caso?". Anote o código, o tipo de peça e a versão. Dado do cliente que não precisa estar na conversa (CPF, endereço): não repita.

### Passo 2. Rodar o script
Rode o script da pasta desta habilidade, com o caminho da peça:

```
python3 "<pasta desta habilidade>/scripts/extrair_citacoes.py" \
  escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md \
  --saida escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD-citacoes.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/conferir-citacoes`. O script procura a base e a ficha jurídica subindo a partir da peça; `--base` e `--validade` valem por cima. `--hoje AAAA-MM-DD` fixa a data de referência. `--vagas "expressão;expressão"` acrescenta as expressões vagas dos aprendizados. Ele lê .md, .txt e .docx, e sai com erro e uma mensagem clara quando falta o arquivo ou a peça está vazia.

O que ele entrega: a tabela de citações (tipo, texto exato, linha, marca, base, cor sugerida, o que fazer), a lista "Pesquisar no Jus IA", a lista "Conferir no portal oficial" e o rascunho do registro. **Cor sugerida não é conferência:** verde sai do script só quando a base tem conferência verde dentro da validade, ou quando as aspas batem com um texto oficial salvo.

Sem o script (chat sem arquivos): leia a peça linha por linha com os padrões da seção 4 e monte a mesma tabela, dizendo que foi à mão.

### Passo 3. Completar o que o script não pega
Leia a peça inteira. Acrescente ao registro: doutrina (`references/como-conferir.md`, seção 5), julgado citado por apelido ("o leading case da Corte"), precedente "desta câmara" sem número, citação em nota de rodapé, citação partida em duas linhas. Tudo o que for citação entra no registro, mesmo que o script não tenha visto.

### Passo 4. Conferir na fonte
Uma citação por vez, nesta ordem: as sem marca, as vermelhas sugeridas, as amarelas, as pendentes. Para cada tipo, as perguntas de `references/como-conferir.md`, seção 1.
- **Na base, verde, dentro da validade:** confira só se a peça usa o julgado para o que a ficha diz (seção 3 do mesmo arquivo).
- **Lei e artigo:** abra o texto compilado no portal oficial. Se este ambiente não abre páginas, peça: "Pode colar aqui o artigo [N] da [LEI], do texto compilado do portal?". Sem o texto, cinza.
- **Aspas:** salve o trecho oficial em `conferencias/fontes/` (`references/como-conferir.md`, seção 4) e rode de novo com `--fontes <pasta>`. O script mostra palavra por palavra o que não bate.
- **Súmula, tema, julgado fora da base:** vão para a lista do Jus IA. O advogado pesquisa, traz o resultado, e a `trazer-pesquisa` organiza na base (se instalada). Com o resultado na conversa, confira os cinco dados e o inteiro teor no portal do tribunal. Se o Jus IA estiver conectado à conta, a pesquisa pode ser feita daqui, com a mesma conferência (conferir na configuração da conta).
- **Menção vaga:** amarela sempre. Proponha a troca por um julgado conferido da base ou a retirada da frase.

### Passo 5. A cor de cada uma
Use a tabela de cores de `../../docs/citacoes.md` e os critérios de `references/como-conferir.md`, seção 2. Na dúvida entre duas cores, a pior. Escreva na coluna "O que foi feito" o que a conferência achou, em uma frase ("a súmula não existe no portal do tribunal em AAAA-MM-DD", "aspas com 'e' no lugar de 'ou'").

### Passo 6. Mostrar
Mostre o relatório (seção 5), com vermelhos e sem marca no topo, e as propostas para cada vermelho e amarelo (tirar, trocar por qual citação conferida, reescrever a frase do tamanho da prova). Pergunte: "Quer que eu grave o registro e tire a marca das citações verdes?".

### Passo 7. Gravar e tirar as marcas
Com o ok:
1. Grave o registro em `conferencias/<peca>-AAAA-MM-DD.md`, na seção "Citações" (seção 6).
2. Rode a retirada das marcas, que gera a versão nova e nunca escreve por cima:

```
python3 "<pasta desta habilidade>/scripts/tirar_marcas.py" \
  escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md \
  escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md \
  --saida escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n+1>.md
```

   O script tira a marca só das linhas com `Cor = verde`, fonte e data preenchidas, e só quando acha a citação exatamente como está no registro. Sai com código 2 quando sobra marca: a peça não vai para protocolo.
3. As propostas aprovadas para vermelho e amarelo entram na mesma versão nova, e as citações novas ou mudadas passam de novo pelos passos 2 a 5.
4. Atualize `citacoes` no `pecas.csv`: `com-vermelho` se houver vermelho; senão `com-amarelo` se houver amarelo; senão `nao-conferidas` se houver cinza ou pendente; senão `verde`. A etapa vai para `conferida` só com `citacoes = verde` e `dados = ok` (`../../docs/producao.md`, regra 4).

### Passo 8. A lista do Jus IA
Entregue ao advogado a lista "Pesquisar no Jus IA", uma linha por citação ou tema, com o que perguntar. Quando a pesquisa voltar: `trazer-pesquisa` e esta habilidade de novo, só nas citações que estavam pendentes.

### Passo 9. Aprender
Pergunte: "Alguma conferência você faria diferente, ou alguma expressão que vocês sempre cortam?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Expressão vaga nova: grave como "menção vaga: <expressão>". Correção que afrouxa a regra ("pode deixar a súmula, eu sei que existe"): explique que a regra 1 não muda e proponha "o advogado confere a súmula e o registro guarda quem conferiu".

### Modo no ciclo
1. O agente passa a minuta. Não pergunte nada e não mostre nada.
2. Rode o passo 2 com `--saida`. Confira só com o que está no ambiente: a base dentro da validade, textos oficiais já salvos em `conferencias/fontes/` e pesquisas já trazidas. Nada de memória.
3. Grave o registro, rode `tirar_marcas.py` (só as verdes) e atualize `citacoes` no `pecas.csv`. O resto fica marcado.
4. Devolva ao agente: o caminho do registro, a contagem por cor, as citações sem marca, e a lista "Pesquisar no Jus IA" para o resumo do dia. As linhas vermelhas e sem marca vão em `antes_de_enviar` do item da fila. Vermelho ou cinza com a etapa em `conferida` é bloqueio do revisor.

### Modo treino
A minuta de `../conferir-peca/assets/minuta-com-erros.md`, uma cópia em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md`. Rode com `--treino` (fora da base sai vermelho sugerido, porque os números do treino são inventados) e com a fonte de treino do artigo 59:

```
python3 "<pasta desta habilidade>/scripts/extrair_citacoes.py" \
  escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md \
  --treino --fontes "<pasta desta habilidade>/assets/fonte-de-treino-lei-8213-art-59.txt"
```

Tudo grava em `escritorio/07-operacao/_treino/juridico/`. Compare com a seção 4.2.

### Modo adaptar
1. Leia `nicho.md`, a ficha jurídica e os aprendizados.
2. Monte duas listas: as expressões vagas que aparecem nas peças do nicho ("conforme remansosa jurisprudência", "como é cediço") e a ordem dos portais por tipo de citação para os `tribunais_principais`.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Alguma dessas vocês usam de propósito, com o julgado logo depois?".
4. Com o ok, grave as expressões em `aprendizados-juridico.md` ("menção vaga: ...") e a ordem dos portais na linha da habilidade.

## 4. O que conta como citação

### 4.1 Os padrões do script

| Tipo | Exemplos de forma (números fictícios) | Observação |
|---|---|---|
| artigo | `art. 59 da Lei 8.213/1991`, `arts. 42 e 59 da Lei nº 8.213/91`, `art. 5º, LXXIV, da CF`, `art. 300 do CPC` | Artigo sem lei no trecho pede o diploma |
| lei | `Lei 10.259/2001` sem artigo | Conferir vigência |
| súmula | `Súmula 999 do TRF6`, `Súmula Vinculante [NÚMERO]` | Tribunal no trecho ajuda a achar na base |
| tema | `Tema [NÚMERO] do STJ` | Repercussão geral ou repetitivo |
| irdr | `IRDR nº [NÚMERO]`, `IAC [NÚMERO]` | |
| julgado | `REsp 1.111.111/MG`, `Apelação Cível nº 0000000-00.0000.0.00.0000` | Classe e número, ou número único do CNJ |
| aspas | `"..."` com mais de 20 caracteres, e recuo `>` | Ligadas à citação mais próxima antes delas |
| vaga | "entendimento pacífico", "jurisprudência dominante", "doutrina majoritária", "o STJ já decidiu" sem número | Amarela sempre |

A marca de uma citação é a primeira `[CONFERIR ...]` depois dela, na mesma frase, antes da próxima citação (`TRIBUNAL, RECURSO nº [NÚMERO], Rel. [NOME], julgado em [DATA] [CONFERIR: ...]` conta).

### 4.2 Conferência com o caso de treino

Rodando a minuta de treino com `--treino` e a fonte de treino, o relatório tem que mostrar exatamente isto nos erros do gabarito:

| Erro do gabarito | Linha | O script mostra | Cor depois da conferência |
|---|---|---|---|
| 7. Súmula 999 do TRF6 | 45 | súmula, com marca, fora da base, vermelho sugerido | vermelho: não existe; sai da peça ou o advogado decide |
| 8. "entendimento pacífico do STJ" | 45 | vaga, amarelo; a frase vai para a lista do Jus IA | amarelo: trocar por julgado conferido ou tirar |
| 9. Aspas do art. 59 com palavras trocadas | 37 | aspas, amarelo: "e" no lugar de "ou"; "30 (trinta)" no lugar de "15 (quinze)" | amarelo: corrigir as aspas pelo texto compilado |
| 10. Artigo da Lei 8.213/1991 sem conferência | 41 | `art. 62 da Lei 8.213/1991`, SEM MARCA | marcar e conferir no portal; até lá, pendente |

As outras quatro (art. 3º da Lei 10.259/2001, art. 59 da Lei 8.213/1991, art. 300 e art. 98 do CPC) saem marcadas e pendentes até a conferência no portal: não são erros do gabarito. Sem a fonte de treino, o erro 9 sai pendente ("conferir palavra por palavra") e, sem acesso ao portal, cinza. Os erros 1 a 6 são da `conferir-peca`. Diferença com esta tabela: o script ou a minuta mudaram; ajuste e rode de novo.

## 5. Formato da saída

```
CONFERÊNCIA DE CITAÇÕES · [caso] · [peça v<n>] · [data]
Resumo: N citações · verde N · amarelo N · vermelho N · cinza N · pendente N · sem marca N
VERMELHO (não vai para a peça)
  1. [citação] · linha N · [o que a conferência achou] · proposta: [tirar | trocar por ... | o advogado decide]
SEM MARCA
  ...
AMARELO
  ...
Pesquisar no Jus IA: [uma linha por item, com o que perguntar]
Conferir no portal oficial: [uma linha por item]
Registro: [caminho] · Versão nova: [caminho] · Marcas que sobraram: N
pecas.csv: citacoes = [valor]
```

A citação solta responde em três linhas: o que é, onde foi conferida (ou "não conferida: pesquisar no Jus IA com [termos]") e a cor.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Tabela do script (rascunho) | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD-citacoes.md` |
| Registro da conferência (seção "Citações") | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md` |
| Textos oficiais salvos para as aspas | `escritorio/07-operacao/juridico/casos/<codigo>/conferencias/fontes/` |
| Versão nova da peça, sem as marcas verdes | `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n+1>.md` |
| Coluna `citacoes` (e a etapa `conferida`, se couber) | `escritorio/07-operacao/juridico/pecas.csv` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções e expressões aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O arquivo de conferência é o mesmo da `conferir-peca`: esta habilidade escreve só a seção "Citações" e não mexe na seção "Dados e coerência". Cabeçalho do arquivo: `documento`, `peca` (caminho da versão conferida), `data`, `como_rodou` (pedido, ciclo, treino), `citacoes`, `dados`. Sem pasta aberta: o relatório e o registro saem no chat, e a peça corrigida vai em bloco para copiar, com as marcas verdes tiradas à mão pela mesma regra.

## 7. Solo e equipe

**Solo:** a conferência é o que deixa a advogada assinar sem reler cada número. Rode logo depois da minuta, e guarde na base o que ficou verde: a próxima peça do mesmo tema já sai com metade conferida.

**Equipe:** o estagiário pode rodar e preencher o registro; a cor verde de julgado e de súmula fica com quem leu o inteiro teor, e o nome dela vai na coluna "O que foi feito". O advogado olha primeiro os vermelhos e os sem marca. Se as mesmas menções vagas voltam em toda minuta, a conversa é com quem redige, e o aprendizado entra na habilidade da peça.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Súmula ou julgado inventado na peça | Peça desacreditada, risco ético para quem assina | Regra fixa 1; fora da base vai para o Jus IA, e vermelho não fica |
| Marca tirada de tudo no fim | Citação não conferida vai ao processo como se estivesse | `tirar_marcas.py` tira só das verdes com fonte e data |
| Aspas "quase iguais" à lei | O juiz lê o texto certo e o argumento cai | Comparação palavra por palavra com o texto oficial salvo |
| "Entendimento pacífico" sem fonte | Frase que a outra parte derruba com um julgado contrário | Menção vaga sai amarela e vai para a lista do Jus IA |
| Julgado certo usado para o que ele não diz | Distinção feita pela outra parte | Pergunta "diz o que a peça diz?" em toda citação |
| Base vencida usada como conferida | Precedente superado na peça | Validade da ficha; vencida volta a ser pendente |
| Treino no registro real | `pecas.csv` com peça que não existe | Pasta `_treino/` |

## 9. Próximo passo

- Nome, datas, valores, documentos e pedidos: `conferir-peca` (se instalada; sem ela, o advogado confere esses pontos na leitura).
- Pesquisa trazida do Jus IA: `trazer-pesquisa` (se instalada) para guardar na base, e esta habilidade de novo.
- Tema com muita divergência: `mapa-jurisprudencial` (se instalada).
- Peça conferida: a fila do advogado (`/motor-juridico:fila`) e, depois de aprovada, `preparar-protocolo` (se instalada).

## Referências desta habilidade

- `scripts/extrair_citacoes.py`: extrai e pré-classifica todas as citações, cruza com a base, compara aspas com a fonte salva. Rode no passo 2.
- `scripts/tirar_marcas.py`: tira a marca só das citações verdes do registro e grava a versão nova. Rode no passo 7.
- `references/como-conferir.md`: as perguntas de cada tipo de citação, como decidir a cor, a pergunta "diz o que a peça diz?", o texto oficial salvo e a doutrina. Leia nos passos 3 a 5.
- `assets/fonte-de-treino-lei-8213-art-59.txt`: o caput do art. 59 copiado do texto compilado do portal oficial, com a data da consulta, só para o treino das aspas. Use no modo treino.
