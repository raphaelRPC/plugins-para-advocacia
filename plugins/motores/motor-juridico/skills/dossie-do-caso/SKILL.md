---
name: dossie-do-caso
description: >
  Monta o dossiê de um caso a partir do lote de documentos (PDF, Word, fotos, conversas,
  extratos), de poucos papéis a dezenas de arquivos: índice, linha do tempo integrada,
  matriz fato x prova, contradições entre documentos, lacunas, o que pedir ao cliente e a
  terceiros, e o dado sensível que não deve ir à peça. Em lote grande trabalha em etapas
  (índice, fichas por documento, matriz), registra o que já leu e nunca fala do que não
  leu. Roda a pedido, no ciclo do agente e no treino. Use quando o advogado disser
  "monta o dossiê", "organiza esses documentos", "o que esses papéis provam", "tem
  contradição aqui?", "o que falta pedir ao cliente", "faz a linha do tempo do caso".
  Não use para o processo já em andamento recebido inteiro (use leitura-dos-autos) nem
  para escolher a tese (use estrategia-do-caso).
---

# Dossiê do caso

> Cada documento lido vira uma ficha, as fichas viram a linha do tempo, e a linha do tempo mostra o que bate, o que diverge e o que falta, com o lugar exato de onde saiu cada fato.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção, etapas e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quinta, 17h. O cliente mandou 43 arquivos pelo WhatsApp: fotos tortas da carteira, três PDFs do INSS, áudios, prints de conversa. A peça é para a semana que vem. O estagiário abre os cinco primeiros, escreve um resumo e a data de cessação que entra na inicial é a do documento que ele leu, não a do que ficou na pasta.

**Regras fixas desta habilidade:**
1. Só fala do que leu. Documento sem ficha não entra na linha do tempo, na matriz nem nas conclusões, e aparece na lista "o que não foi lido".
2. Cada fato traz o documento e o lugar (página, parágrafo, horário da mensagem). Fato sem lugar não entra.
3. A habilidade aponta a contradição e não escolhe a versão. Qual data, valor ou versão vale é decisão do advogado.
4. Dado sensível é marcado com recomendação, e quem decide o que vai à peça é o advogado.
5. Nenhuma citação de norma ou julgado nasce aqui sem a marca de `citacoes.md`. Requisito legal de prova fica `[CONFERIR]`.

## 1. Quando usar

**Use quando:**
- Chegou um caso novo com documentos e a peça ainda não foi escrita (etapa `pedida` ou `em-analise` no `pecas.csv`).
- Chegou um lote novo de documentos de um caso que já tem dossiê (modo "continuar").
- O `agente-juridico` chamou no ciclo para um caso novo com documentos (modo "no ciclo").
- O `/motor-juridico:comecar` ou o advogado pediu o treino com os casos fictícios (modo "treino").
- A `adaptar-juridico` (se instalada) pediu os documentos típicos e as chaves de fato do nicho (modo "adaptar").

**Não use quando:**
- É um processo em andamento recebido inteiro, com petições e decisões: `leitura-dos-autos` (se instalada; sem ela, use esta habilidade tratando cada peça do processo como um documento).
- O pedido é escolher o caminho do caso: `estrategia-do-caso`, depois do dossiê.
- O pedido é comparar duas versões do mesmo documento: `comparar-versoes` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-juridica.md`. Leia `nicho.md`, se existir, e use os documentos típicos dele para achar lacunas. Leia `04-base/juridico/nicho/dossie-do-caso.md`, se existir (materiais do modo adaptar).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`). Aprendizado vale mais que o padrão desta habilidade, desde que não afrouxe as regras fixas.
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Qual é a área do caso e qual peça vai sair dele?".
4. **Conta de IA e dados.** Documento real de cliente só em conta profissional ou de equipe (`regras.md`, seção 6). Em conta pessoal, só os documentos de treino ou anonimizados. Laudo completo, dado de criança e processo em segredo de justiça só com autorização expressa do advogado.
5. **Leia o que já existe do caso** em `escritorio/07-operacao/juridico/casos/<codigo>/`: `dossie.md`, `controle-de-leitura.csv`, `fichas/`. Se já existe, o modo é "continuar": não recomece.
6. **Conflito de interesses.** Caso novo com parte contrária identificada: confira se a checagem está registrada (`conflito-de-interesses`, se instalada). Sem registro, a primeira linha do dossiê é "checar conflito antes de seguir" e o item vai para ADVOGADO AGORA. Sem a habilidade, a pergunta vai ao advogado.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` |
| Melhora | E: `nicho` · J: `tribunais_principais` |

Sem `areas` e sem resposta à pergunta do item 3, a matriz sai sem a coluna "fato que a peça vai precisar" preenchida, e o fim avisa.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Poucos documentos | Até uns 10 arquivos curtos | Os arquivos ou o texto colado | O dossiê inteiro numa rodada, no chat |
| Lote grande | Dezenas de arquivos ou muitas páginas | A pasta do lote | Índice, etapas de leitura com registro, e o dossiê no fim |
| Continuar | Lote interrompido ou documento novo | A pasta do caso | O dossiê atualizado, com o que mudou marcado `[NOVO]` |
| No ciclo | O agente chama | Pedido em `entrada/` ou caso novo no `pecas.csv` | Fichas, controle, dossiê e item na fila. Não mostra nada |
| Treino | Casos fictícios ou "é teste" | `assets/documentos-de-treino.md` | O mesmo, gravado só em `_treino/`, e a diferença com o gabarito da seção 4.7 |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | Documentos típicos e chaves de fato por tipo de caso, para aprovar |

Pedido direto ("monta o dossiê destes documentos"): não faça entrevista. Execute e pergunte só o que faltar.

### Passo 1. Receber o lote
- Peça a pasta ou os arquivos. Os documentos ficam onde o escritório guarda (sistema ou `casos/<codigo>/documentos/`). A habilidade lê dali e não copia o lote para outro lugar.
- Áudio e vídeo: peça a transcrição. Foto torta ou PDF de imagem: leia página a página; o que não der para ler fica `ilegivel`, com o pedido de nova cópia.
- Dado identificável que a tarefa não precisa: troque pela marcação das regras (`[CLIENTE]`, `[DOC]`, `[PROCESSO]`, `[ENDEREÇO]`, `[CONTATO]`) nas fichas e no dossiê, e avise em uma linha.

### Passo 2. Índice
Rode o script do índice (seção 4.6). Ele dá um código a cada documento, conta páginas de PDF, acha arquivo repetido e grava o `controle-de-leitura.csv`. Mostre o índice e pergunte: "Algum desses é de outro caso ou pode ficar de fora?". O que o advogado tirar fica `fora-do-caso`, nunca apagado.

### Passo 3. Plano de etapas
Lote grande: divida em etapas de até 60 páginas (ou o que o advogado preferir), na ordem que mais ajuda a peça. Diga o plano em uma linha ("4 etapas: primeiro os documentos do INSS, depois os médicos, depois carteira e conversas"). Cada etapa fecha com as fichas gravadas e o controle atualizado, para a próxima conversa continuar de onde parou.

### Passo 4. Fichas por documento
Para cada documento da etapa, uma ficha em `fichas/<doc>.md`, no formato de `assets/modelo-ficha-documento.md`: os fatos com data, chave e lugar; o que prova; o que não diz e devia dizer; dado sensível; dúvidas. Leu só uma parte: `situacao: lido-em-parte` e as páginas lidas. Depois da etapa, rode o índice de novo com `--fichas` para o controle refletir o que foi lido. Nunca escreva ficha de documento que não abriu.

### Passo 5. Linha do tempo
Rode o script da linha do tempo (seção 4.6). Ele junta os fatos de todas as fichas em ordem de data, aponta a mesma chave com datas que não batem entre documentos e lista o que ficou sem ler. Revise: fato fora de lugar volta para a ficha, não para a linha do tempo.

### Passo 6. Matriz fato x prova
Liste os fatos que a peça vai precisar (pelo tipo de peça e pela área) e, para cada um, a prova com documento e lugar, a força (seção 4.3) e o que falta. A coluna "quem fala de cada fato" do script é o ponto de partida.

### Passo 7. Contradições
Junte as divergências de data do script e procure as outras (valor, pessoa, conteúdo, omissão, versão, interna) com `references/contradicoes-e-lacunas.md`. Cada uma com o que cada documento diz, o lugar, por que importa e como resolver.

### Passo 8. Lacunas, pedidos e dado sensível
Lacunas pelas perguntas da referência. Para cada lacuna que um documento resolve: o pedido, ao cliente ou a terceiro. Dado sensível: tabela da seção 4.4, com a recomendação.

### Passo 9. Montar, mostrar e gravar
Monte o `dossie.md` pelo `assets/modelo-dossie.md`, com a cobertura da leitura no cabeçalho. Mostre primeiro, em até 6 linhas: cobertura, contradições, lacunas que mudam a peça, dado sensível, perguntas. Grave com o ok. No `pecas.csv`, a linha da peça vai de `pedida` para `em-analise` (com `atualizado_em`); sem linha, proponha criar. Pedidos ao cliente: entregue a lista para a pessoa que fala com ele, ou para a `checklist-de-documentos`, do motor-experiencia (se instalado). A habilidade não escreve para o cliente.

### Passo 10. Aprender
Pergunte: "Alguma contradição ou lacuna que eu não vi, ou que não é problema para vocês?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md`. Documento típico novo do nicho: ofereça guardar em `04-base/juridico/nicho/dossie-do-caso.md`. Correção que afrouxa as regras fixas (por exemplo, "pode resumir os que você não leu"): explique por que não pode guardar e proponha uma versão que cabe ("ler só a primeira página dos repetidos e marcar `lido-em-parte`").

### Modo continuar
1. Leia o controle, as fichas e o dossiê. Rode o índice: arquivos novos ganham código e ficam `a-ler`.
2. Leia só o que está `a-ler` ou `lido-em-parte`. Rode a linha do tempo.
3. No dossiê, marque `[NOVO]` o que entrou e `[ALTERADO]` o que mudou (uma contradição que se resolveu, uma lacuna que um documento fechou). Suba a versão.

### Modo no ciclo
1. O agente passa o caso. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 9 até o limite da rodada: 150 páginas por caso por ciclo, ou o que a ficha definir `[A DEFINIR]`. Lote maior continua no ciclo seguinte, pelo controle.
3. Grave fichas, controle, linha do tempo e o `dossie.md` (parcial, com a cobertura no cabeçalho, ou completo).
4. Vai para ADVOGADO AGORA, com uma frase: conflito de interesses não checado; dado de criança, laudo completo ou segredo de justiça no lote; prazo interno em até 2 dias úteis com dossiê incompleto.
5. Dossiê completo, ou parcial com contradição que muda a peça: um item na fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-dossie.md`) no formato de `agentes-e-fila.md`, com `para: advogado`, `canal: interno`, `tipo: dossie`, `revisor: pendente`, `prazo` (o prazo interno do `pecas.csv`) e, em `antes_de_enviar`, a cobertura, as contradições e o dado sensível para decidir.
6. No `pecas.csv`, só `pedida` para `em-analise` e `atualizado_em` (`producao.md`, regra 5).
7. Devolva ao agente: caminho do dossiê, documentos lidos e por ler, contradições, itens em ADVOGADO AGORA.

### Modo treino
Use `assets/documentos-de-treino.md` (casos 1 e 2 de `../../docs/casos-ficticios.md`). Copie cada documento para um arquivo em `escritorio/07-operacao/_treino/juridico/casos/<codigo>/documentos/` e rode o fluxo inteiro com os scripts. Tudo grava em `_treino/juridico/`. No fim, mostre a diferença com o gabarito da seção 4.7.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Por tipo de caso do nicho: os documentos típicos (com quem tem cada um), as chaves de fato que se repetem (para as fichas usarem o mesmo nome) e os fatos que a peça daquele tipo costuma precisar `[CONFERIR]` com o advogado.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e mostre. Pergunte: "Falta algum documento que vocês sempre pedem?".
4. Com o ok, grave em `04-base/juridico/nicho/dossie-do-caso.md`. Devolva à `adaptar-juridico` um caso de teste do nicho (os documentos e o que o dossiê tem de achar).

## 4. Critérios

### 4.1 O que conta como lido
- `lido`: a habilidade abriu o documento inteiro e escreveu a ficha.
- `lido-em-parte`: abriu uma parte (páginas indicadas). A ficha diz quais.
- `ilegivel`: abriu e não deu para ler. Vai para "o que pedir" (nova cópia).
- `duplicado`: o mesmo conteúdo de outro documento (o script compara o arquivo). Não precisa de ficha.
- `fora-do-caso`: o advogado tirou. Não precisa de ficha.
- `a-ler`: ainda não foi aberto. Nunca entra em conclusão nenhuma.

### 4.2 Contradição
Divergência entre documentos sobre o mesmo fato, ou omissão de algo que o documento devia tratar. Os tipos e o jeito de registrar estão em `references/contradicoes-e-lacunas.md`. O script acha só as de data, pela chave; as outras saem da leitura.

### 4.3 Força da prova
`direta`, `indireta`, `versão da parte`, `sem prova` (definições na referência). Fato necessário com `versão da parte` ou `sem prova` vira lacuna.

### 4.4 Dado sensível
Saúde, criança e adolescente, terceiro, renda e vida íntima, documentos de identificação: tabela da referência, com a recomendação padrão. O dossiê registra a decisão do advogado na coluna própria, e quem minuta consulta a tabela antes de escrever os fatos. Se a `conferir-peca` estiver instalada, mostre a ela essa tabela na conferência da minuta.

### 4.5 Lote grande
- Etapas de até 60 páginas, cada uma com fichas gravadas e controle atualizado.
- O controle é a memória entre conversas: quem continua lê o controle e as fichas, nunca o lote inteiro de novo.
- Documento muito longo e repetitivo (extrato de 200 páginas): leia o período que importa ao caso, marque `lido-em-parte` com as páginas e diga ao advogado o que ficou de fora.
- Mesmo documento em versões diferentes (o contrato e o aditivo, duas minutas): `comparar-versoes` (se instalada).

### 4.6 Os scripts
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/dossie-do-caso`; sem a variável, use o caminho da pasta desta habilidade.

Índice e controle de leitura (`scripts/indice_do_lote.py`):

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/dossie-do-caso/scripts/indice_do_lote.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/documentos" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/controle-de-leitura.csv" \
  --codigo-do-nome --paginas-por-etapa 60 \
  --fichas "escritorio/07-operacao/juridico/casos/C-2026-0001/fichas"
```

Opções: `--marcar D03=lido-em-parte:1-20` (muda a situação à mão; pode repetir), `--prefixo T`, `--so-mostrar` (não grava). O controle aceita vírgula ou ponto e vírgula, com ou sem BOM. Sem pasta ou sem documento, o script para com código 1 e diz por quê.

Linha do tempo (`scripts/linha_do_tempo.py`):

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/dossie-do-caso/scripts/linha_do_tempo.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/fichas" \
  --controle "escritorio/07-operacao/juridico/casos/C-2026-0001/controle-de-leitura.csv" \
  --saida "escritorio/07-operacao/juridico/casos/C-2026-0001/linha-do-tempo.md"
```

Datas aceitas nas fichas: AAAA-MM-DD, DD/MM/AAAA, AAAA-MM, MM/AAAA, AAAA. Data que o script não entende aparece numa lista própria, para corrigir na ficha. Sem fichas ou sem nenhuma tabela de fatos, para com código 1.

### 4.7 Conferência com os casos fictícios
Rodando o fluxo com `assets/documentos-de-treino.md`, o dossiê tem que achar exatamente isto (os quatro primeiros itens do caso 1 e os dois primeiros do caso 2 são o gabarito de `../../docs/casos-ficticios.md`; os outros vêm dos documentos de treino):

| Caso | Tem que achar | Onde | Tipo |
|---|---|---|---|
| 1 Marta | Cessação em 2026-02-28 (D1, D3) e em 2026-03-05 (D2) | linha do tempo, chave `cessacao-do-beneficio` | contradição de data |
| 1 Marta | A perícia (D5) lista só o exame de 08/2025 e não enfrenta o relatório D4, que é anterior a ela | matriz e contradições | omissão |
| 1 Marta | Nenhum relatório médico posterior à cessação (o D4 é de 2026-01-20) | lacunas; pedir ao cliente relatório atual | lacuna |
| 1 Marta | A função exige esforço físico: D3 (ocupação) e D6 (descrição com carregamento) batem com as restrições do D4 | matriz, prova direta | fato com prova |
| 1 Marta | D6 sem a página de saída | `lido-em-parte`; pedir ao cliente | lacuna |
| 1 Marta | Acompanhamento psicológico (D4) | dado sensível: não vai; diagnóstico só o mínimo | dado sensível |
| 2 Paulo | Admissão em 2022-03-01 (T1) e 2022-05-02 (T2); a versão do cliente em T4 ("começo de março de 2022") apoia T1: possível período sem registro | linha do tempo, chave `admissao` | contradição de data |
| 2 Paulo | O gerente reconhece a dívida ("o acerto sai no fim do mês", "semana que vem resolvo") | matriz, prova direta do não pagamento | fato com prova |
| 2 Paulo | Horas extras pagas em dois de três holerites: pedir controle de jornada | lacunas; pedir ao cliente e, na ação, ao empregador `[CONFERIR]` o caminho | lacuna |
| 2 Paulo | Filho internado (T4) | dado sensível de criança: não vai | dado sensível |
| 2 Paulo | Parte contrária Restaurante Sabor Mineiro Ltda.: checagem de conflito antes de seguir (a base de partes de treino mostra que foi cliente) | cabeçalho e ADVOGADO AGORA | conflito |

E não pode: escolher qual data de cessação ou de admissão vale; tirar conclusão de qualquer documento `a-ler`; levar a ansiedade ou o filho internado para a peça. Qualquer diferença: falta chave igual nas fichas, pergunta da referência ou aprendizado. Ajuste e rode de novo.

## 5. Formato da saída

**No chat, primeiro:**

```
DOSSIÊ · [CODIGO] · [primeiro nome] · [área] · [peça]
Leitura: [N] de [N] documentos lidos; [N] em parte; [N] ilegíveis; [N] por ler
Antes de seguir: [conflito não checado | nada]
Contradições: [N] · a que muda a peça: [uma frase]
Lacunas que mudam a peça: [uma frase cada, até 3]
Pedir: ao cliente [N], a terceiros [N]
Dado sensível para decidir: [N]
Perguntas para o advogado: [a mais importante]
```

Depois, o `dossie.md` completo, no formato de `assets/modelo-dossie.md`.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Dossiê | `escritorio/07-operacao/juridico/casos/<codigo>/dossie.md` |
| Fichas por documento | `escritorio/07-operacao/juridico/casos/<codigo>/fichas/<doc>.md` |
| Controle de leitura | `escritorio/07-operacao/juridico/casos/<codigo>/controle-de-leitura.csv` |
| Linha do tempo do script | `escritorio/07-operacao/juridico/casos/<codigo>/linha-do-tempo.md` |
| Item na fila (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-dossie.md` |
| Treino (tudo acima) | `escritorio/07-operacao/_treino/juridico/` |
| Materiais do nicho | `escritorio/04-base/juridico/nicho/dossie-do-caso.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

No `pecas.csv`, a linha vai de `pedida` para `em-analise` e ganha `atualizado_em`. Nada mais muda ali. Sem pasta aberta: dossiê, fichas e controle no chat, em blocos prontos para copiar, com o caminho de cada um; o lote grande, nesse caso, vai em conversas por etapa, e cada uma começa colando o controle da anterior.

## 7. Solo e equipe

**Solo:** o dossiê é o lugar para parar de reler o caso. Rode o índice no dia em que os documentos chegam e uma etapa por dia; a peça começa da matriz.

**Equipe:** o estagiário roda as etapas e escreve as fichas; o advogado lê o resumo de 6 linhas, decide as contradições e o dado sensível. A coluna "decisão do advogado" mostra o que ainda depende dele. Se o mesmo caso tem fichas de duas pessoas, o controle diz quem leu o quê (coluna `observacao` ou o registro da leitura).

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Resumir o lote pelos primeiros arquivos | A data errada entra na peça | Controle de leitura e a lista do que não foi lido |
| Fato sem lugar | Ninguém acha a prova na hora da réplica | Toda linha com documento e lugar |
| Escolher a versão que favorece | A contradição explode na audiência | A habilidade aponta, o advogado decide |
| Ler o mesmo arquivo duas vezes | Tempo perdido no lote grande | O script acha duplicados |
| Recomeçar o lote a cada conversa | O lote nunca termina | Controle e fichas: continuar de onde parou |
| Diagnóstico ou dado de criança na peça | Exposição desnecessária do cliente | Tabela de dado sensível com decisão do advogado |
| Seguir com caso de ex-cliente do outro lado | Conflito de interesses | Checagem antes de seguir |
| Treino no registro real | Peça fictícia na fila | Pasta `_treino/` |

## 9. Próximo passo

- Escolher o caminho do caso: `estrategia-do-caso`, a partir da matriz e das contradições.
- Testar a tese contra a melhor resposta da outra parte: `advogado-do-diabo` (se instalada; sem ela, a estratégia lista os riscos).
- Pedir os documentos ao cliente: `checklist-de-documentos`, do motor-experiencia (se instalado); sem ele, a lista vai para quem fala com o cliente.
- Com a tese definida pelo advogado: `minutar-peca` (se instalada; sem ela, a matriz é o roteiro dos fatos da peça).

## Referências desta habilidade

- `references/contradicoes-e-lacunas.md`: tipos de contradição, força da prova, perguntas que acham lacunas, o que pedir e a tabela de dado sensível. Leia nos passos 6 a 8.
- `assets/modelo-ficha-documento.md`: a ficha de cada documento. Use no passo 4.
- `assets/modelo-dossie.md`: o dossiê. Use no passo 9.
- `assets/documentos-de-treino.md`: os documentos fictícios dos casos 1 e 2. Use no modo treino.
- `scripts/indice_do_lote.py` e `scripts/linha_do_tempo.py`: seção 4.6.
