---
name: estrategia-do-caso
description: >
  Organiza a decisão estratégica do caso a partir do dossiê ou da leitura dos autos: os
  caminhos possíveis, os riscos de cada um em palavras (alto, médio, baixo, com o porquê),
  os cenários, acordo ou litígio com os valores que o advogado informar (um script monta o
  quadro do líquido do cliente), o plano de provas e os próximos atos. Nunca dá chance de
  êxito em percentual e nunca escolhe o caminho: termina na decisão do advogado registrada
  em estrategia.md e, só com o ok dele, na etapa tese-definida. Use quando o advogado
  disser "qual o caminho desse caso", "vale fazer acordo?", "monta a estratégia", "quais
  as opções", "o que a gente faz agora", "organiza a decisão do caso".
  Não use para montar o dossiê (use dossie-do-caso) nem para minutar a peça (use
  minutar-peca, depois da decisão).
---

# Estratégia do caso

> Os caminhos, os riscos e os números ficam lado a lado e a escolha fica escrita com o nome de quem decidiu.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Etapas e `pecas.csv`: `../../docs/producao.md`. Pesquisa: `../../docs/pesquisa-jus-ia.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quarta, 16h. O INSS propôs acordo com 80% dos atrasados. A cliente liga perguntando "vale a pena?". O estagiário responde "a gente tem 70% de chance de ganhar", número que ninguém calculou, e a cliente recusa o acordo por causa dele.

**Regras fixas desta habilidade:**
1. Nenhuma chance de êxito em percentual, nenhuma previsão de resultado ou de data de decisão. Risco é `alto`, `médio` ou `baixo`, com o porquê.
2. Nenhum valor sai da cabeça da IA. Valores de cenário, proposta, custos e honorários vêm do advogado ou do cliente, ou ficam `[A DEFINIR]`.
3. A habilidade mostra caminhos e não escolhe. A decisão é de quem assina, e só entra na seção 10 com o ok dele.
4. A etapa `tese-definida` só é gravada depois de um "sim" explícito do advogado à pergunta do passo 9. No ciclo, nunca.
5. Toda citação de norma ou julgado nasce marcada (`citacoes.md`). Prazo processual é `[A CONFIRMAR pela controladoria]`.

## 1. Quando usar

**Use quando:**
- O dossiê ou a leitura dos autos está pronta e a peça está em `em-analise`, esperando o caminho.
- Chegou uma proposta de acordo, uma decisão ou um laudo que muda o caso (modo "rever").
- O `agente-juridico` achou um caso sem estratégia (modo "no ciclo": rascunho para o advogado decidir).
- O comando `fila` está registrando a decisão do advogado sobre um item de ADVOGADO AGORA (modo "registrar").
- Treino com os casos fictícios, ou a `adaptar-juridico` (se instalada) pediu as perguntas por tipo de caso do nicho (modo "adaptar").

**Não use quando:**
- Ainda não há dossiê nem leitura dos autos: `dossie-do-caso` ou `leitura-dos-autos` (se instalada) antes. Sem eles, a estratégia sai com "base: só o relato do advogado" no cabeçalho.
- O pedido é a melhor resposta da outra parte à nossa tese: `advogado-do-diabo` (se instalada).
- A decisão já foi tomada e o pedido é a peça: `minutar-peca` (se instalada).
- O pedido é dizer ao cliente se vale entrar com a ação por mensagem: isso é do advogado, de preferência em conversa (`regras.md`, seção 5).

## 2. Antes de começar

1. **Leia as fichas** (`ficha-do-escritorio.md` e `ficha-juridica.md`, em `escritorio/04-base/comum/`), `nicho.md` (se existir) e `04-base/juridico/nicho/estrategia-do-caso.md` (perguntas por tipo de caso, do modo adaptar).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`).
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "Quem decide a estratégia e assina neste caso?".
4. **Leia o caso** em `escritorio/07-operacao/juridico/casos/<codigo>/`: `dossie.md`, `leitura-dos-autos.md`, `contraditorio.md` e `estrategia.md` (se já existe, o modo é "rever"). Leia a passagem do comercial (`07-operacao/comercial/passagens/<codigo>.md`), se existir: o que foi combinado com o cliente.
5. **Leia a base do escritório:** as teses (`04-base/juridico/teses/`) e a jurisprudência (`04-base/juridico/jurisprudencia/`) do tema. Julgado da base com conferência vencida volta a ser marcado (`citacoes.md`, regra 5).
6. **Conflito de interesses.** Caso novo com parte contrária e sem checagem registrada: pare. A estratégia não começa antes da checagem (`conflito-de-interesses`, se instalada; sem ela, ou sem base de partes, a pergunta vai ao advogado na hora: "Alguma parte deste caso já foi cliente do escritório?", e a resposta fica registrada em `casos/<codigo>/conflito-de-interesses.md`).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `quem_assina` |
| Melhora | J: `tribunais_principais` |

`quem_assina` diz de quem é a decisão da seção 10. Sem ele, pergunte o campo uma vez e ofereça gravar. `tribunais_principais` orienta a pesquisa no Jus IA (onde o caso vai ser julgado).

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | O advogado quer a estratégia | Dossiê ou leitura dos autos | O rascunho no chat e a pergunta da decisão |
| Rever | Fato novo (acordo, laudo, decisão) | A estratégia anterior e o fato novo | Nova versão, com `[ALTERADO]` e a decisão perguntada de novo |
| Registrar | O advogado decidiu (aqui ou pelo comando `fila`) | A decisão dele | Seção 10 preenchida e `tese-definida` no `pecas.csv` |
| No ciclo | O agente chama | O caso em `em-analise` | Rascunho gravado, item na fila e ADVOGADO AGORA. Nunca decide |
| Treino | Casos fictícios | Casos 1 e 2 | O mesmo, em `_treino/`, e a diferença com a seção 4.5 |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | Perguntas e caminhos típicos por tipo de caso, para aprovar |

### Passo 1. O caso em cinco linhas
A partir do dossiê ou da leitura dos autos: o que aconteceu, o que está provado, o que diverge, o que falta, em que fase está. Cada afirmação com a fonte (documento ou folha).

### Passo 2. O que o cliente quer
Leia a passagem e a ata da consulta, se existirem. Falta o objetivo do cliente, o que ele não aceita ou a condição mínima para acordo: pergunte ao advogado, uma por vez: "O que a cliente quer, no fim: o benefício de volta, os atrasados, as duas coisas?". Não deduza o que o cliente quer.

### Passo 3. Caminhos possíveis
Liste de dois a quatro caminhos reais (por exemplo: ação judicial agora; novo requerimento administrativo com documento novo; aguardar o documento que falta e depois agir; acordo). Para cada um: o que exige, o que está a favor e contra, com a fonte. Tese do escritório que cabe: pelo nome, de `04-base/juridico/teses/`. Requisito legal ou processual de cada caminho: `[CONFERIR]`. Jurisprudência que apoia ou contraria: da base, ou vai para a lista do que pesquisar no Jus IA.

### Passo 4. Riscos
Para cada caminho, os riscos com nível e porquê (seção 4.1) e o que reduz cada um (um documento, uma prova, um pedido subsidiário). Se a `advogado-do-diabo` já rodou, os argumentos fortes dela entram aqui.

### Passo 5. Cenários e valores
Para cada caminho, o que pode acontecer (procedência, procedência parcial, improcedência, acordo), sem dizer qual vai acontecer. Peça os valores ao advogado, um de cada vez: "Qual o valor que a cliente recebe em cada cenário, pela sua conta?", "Tem proposta de acordo? De quanto?", "Os honorários do contrato são em percentual, fixos ou os dois?". Grave os valores num `cenarios.csv` do caso e rode o script (seção 4.3). Sem valores, os cenários ficam em palavras e o quadro fica `[A DEFINIR]`.

### Passo 6. Acordo ou litígio
Com o quadro: a diferença de líquido entre o acordo e cada cenário, a condição mínima do cliente e quando rever a conta. Nada de "compensa" ou "não compensa": o quadro mostra os números, o advogado e o cliente decidem.

### Passo 7. Plano de provas e próximos atos
Do dossiê: fato, prova que temos, prova a produzir, como, quem. Próximos atos com quem faz e o prazo interno informado; prazo processual `[A CONFIRMAR pela controladoria]`.

### Passo 8. Mostrar
Grave o rascunho em `casos/<codigo>/estrategia.md` (`situacao: rascunho`) com o ok e mostre o resumo (seção 5). A seção 10 fica vazia.

### Passo 9. Perguntar a decisão
Pergunte a quem assina, com as palavras exatas: "Qual caminho você escolhe, e com qual tese? Se você disser, eu registro a decisão no `estrategia.md` e mudo a peça para `tese-definida`." Só um "sim" com o caminho dito pelo advogado conta ("sim, vamos pela ação com a tese X"). "Acho que sim", "deixa eu pensar" ou silêncio: nada muda, a peça continua `em-analise` e a pergunta fica nas perguntas da seção 9.

### Passo 10. Registrar a decisão
Com o sim: preencha a seção 10 (caminho, tese, o que fica de fora e por quê, condição de acordo, quem decidiu, data, como foi registrada), mude `situacao: decidida`, suba a versão e acrescente uma linha no histórico. No `pecas.csv`, a linha da peça vai para `tese-definida`, com a coluna `tese` (o nome da tese, ou vazio se não está no banco) e `atualizado_em`. Mostre as duas mudanças antes de gravar.

### Passo 11. Aprender
Pergunte: "Algum caminho que vocês sempre consideram e eu não listei, ou risco que eu pesei errado?". A correção vira regra curta e, com o ok, entra em `aprendizados-juridico.md`. Pedido para pôr percentual ("coloca uns 70% aí"): explique que a habilidade não trabalha com chance em percentual e proponha o que cabe ("risco baixo, porque o laudo e o relatório do assistente dizem a mesma coisa").

### Modo rever
1. Leia a estratégia anterior e o fato novo (o laudo, a proposta, a decisão).
2. Refaça só o que o fato novo muda. Marque `[ALTERADO]` e `[NOVO]`.
3. Se a decisão da seção 10 pode mudar, pergunte de novo (passo 9). A decisão antiga fica no histórico, nunca é apagada.

### Modo registrar
Chamado pelo comando `fila` (passo 0) ou quando o advogado diz a decisão no meio de outra conversa: rode os passos 9 e 10 com o que ele disse. Sem estratégia gravada, registre a decisão numa estratégia curta (seções 1, 9 e 10) e avise que o resto está por fazer.

### Modo no ciclo
1. O agente passa o caso. Não pergunte nada e não mostre nada.
2. Rode os passos 1, 3, 4, 7 e o 5 sem valores (cenários em palavras; o quadro só com valores que já estiverem na passagem ou no caso, com a fonte). Nunca os passos 9 e 10.
3. Grave `estrategia.md` com `situacao: rascunho` e a seção 10 vazia.
4. Grave um item na fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-estrategia.md`), no formato de `agentes-e-fila.md`: `para: advogado`, `canal: interno`, `tipo: estrategia`, `revisor: pendente`, `prazo` (o prazo interno do `pecas.csv`) e, em `antes_de_enviar`, as perguntas da seção 9.
5. Ponha em ADVOGADO AGORA: "peça esperando tese" e, se houver, proposta de acordo da outra parte.
6. No `pecas.csv`, nada além de `atualizado_em`. A etapa continua `em-analise`.

### Modo treino
Casos 1 e 2 de `../../docs/casos-ficticios.md`, com o dossiê de treino (`dossie-do-caso`, se instalada; sem ela, a tabela do caso em `casos-ficticios.md`) e `assets/cenarios-exemplo.csv`. Grave em `escritorio/07-operacao/_treino/juridico/casos/<codigo>/`. Mostre a diferença com a seção 4.5.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Por tipo de caso do nicho: as perguntas que o advogado sempre faz antes de decidir, os caminhos que costumam existir e os riscos que se repetem, tudo `[CONFERIR]` com ele.
3. Marque `[NOVO]` ou `[ALTERADO]`, mostre e pergunte: "Falta algum caminho que vocês sempre avaliam?".
4. Com o ok, grave em `04-base/juridico/nicho/estrategia-do-caso.md`.

## 4. Critérios

### 4.1 Nível de risco
| Nível | Quando |
|---|---|
| alto | O caminho depende de um fato sem prova, de um documento que diverge de outro, de uma tese que a base mostra perdendo no juízo do caso, ou de um requisito ainda não conferido |
| médio | Há prova, mas indireta ou contestável; há jurisprudência dos dois lados na base; o caminho é mais longo ou mais caro |
| baixo | Fato provado por documento direto, sem contradição, com a base a favor e conferida |

Sempre com o porquê, citando a fonte (doc, folha, julgado da base). Na dúvida, o nível mais alto.

### 4.2 O que nunca sai
"Chance de êxito", "probabilidade", "X% de ganhar", "caso ganho", "o juiz vai decidir em N meses", "compensa aceitar", "não compensa". Se o cliente pediu um número, a resposta é do advogado, em conversa, e a habilidade prepara o material dessa conversa (os riscos em palavras e o quadro de valores).

### 4.3 O script do quadro de cenários
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/estrategia-do-caso`; sem a variável, use o caminho da pasta desta habilidade.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/estrategia-do-caso/scripts/cenarios.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/cenarios.csv" \
  --acordo "11.520,00" --honorarios-percentual 30 \
  --saida "escritorio/07-operacao/juridico/casos/C-2026-0001/cenarios.md"
```

O `scripts/cenarios.py` lê o csv (colunas `cenario`, `valor_bruto`, `custos`, `tempo_estimado`, `observacao`; vírgula ou ponto e vírgula, com ou sem BOM) e monta o quadro: honorários pelo contrato, custos, líquido para o cliente e a diferença para o acordo. Valor vazio ou marcado fica `[A DEFINIR]` e vai para as pendências. Coluna de chance ou probabilidade é recusada, com código 1. Outras opções: `--honorarios-fixo VALOR`, `--custos-acordo VALOR`. Arquivo que não existe, vazio ou sem as colunas obrigatórias: código 1 e a mensagem. O modelo de csv está em `assets/cenarios-exemplo.csv` (valores de exemplo).

### 4.4 Decisão registrada
A seção 10 tem sete campos, todos preenchidos. Sem "quem decidiu" e "data", não há decisão. O `pecas.csv` só vai para `tese-definida` com a seção 10 preenchida, e o `revisor-juridico` bloqueia minuta de peça sem essa etapa.

### 4.5 Conferência com os casos fictícios
| Caso | Tem que sair | Não pode sair |
|---|---|---|
| 1 Marta (inicial) | Dois a quatro caminhos (por exemplo, ação judicial agora com o que já existe; pedir antes o relatório médico atual; novo requerimento administrativo), cada um com riscos em palavras ligados ao dossiê: a data de cessação divergente, a perícia que não enfrentou o relatório, a falta de relatório atual | Percentual; escolha do caminho; `tese-definida` sem o sim |
| 1 Marta (acordo, com `assets/cenarios-exemplo.csv`) | O quadro do script com o líquido de cada cenário e a diferença para o acordo; a pergunta da condição mínima da cliente | "Compensa aceitar"; valor que não veio do advogado |
| 2 Paulo | Parada antes de começar: parte contrária (Restaurante Sabor Mineiro Ltda.) foi cliente do escritório na base de treino; sem checagem de conflito registrada, nenhuma estratégia | Qualquer caminho antes da checagem |

E, em todos: a seção 10 vazia até o sim, a etapa em `em-analise` e as citações marcadas.

## 5. Formato da saída

**No chat, primeiro:**

```
ESTRATÉGIA · [CODIGO] · [primeiro nome] · [área] · rascunho v[N]
Base: dossiê de AAAA-MM-DD [e autos até fl. N]
O cliente quer: [uma frase, com a fonte] | [A CONFIRMAR]
Caminhos: 1) ... 2) ... 3) ...
Risco principal de cada um: 1) [nível, porquê] 2) ... 3) ...
Acordo: [proposta feita | nenhuma] · quadro: [diferença de líquido, em uma frase]
Provas a produzir: [N] · próximos atos: [N]
Para decidir: Qual caminho você escolhe, e com qual tese?
```

Depois, o `estrategia.md` no formato de `assets/modelo-estrategia.md`.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Estratégia e decisão | `escritorio/07-operacao/juridico/casos/<codigo>/estrategia.md` |
| Cenários (csv e quadro) | `escritorio/07-operacao/juridico/casos/<codigo>/cenarios.csv` e `cenarios.md` |
| Item na fila (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-estrategia.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/casos/<codigo>/` |
| Materiais do nicho | `escritorio/04-base/juridico/nicho/estrategia-do-caso.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

No `pecas.csv`: a pedido, só `tese-definida` (com `tese` e `atualizado_em`) depois do sim do passo 9; no ciclo, só `atualizado_em`. Sem pasta aberta: a estratégia no chat, em bloco pronto para copiar, e a linha do `pecas.csv` como tabela para colar.

## 7. Solo e equipe

**Solo:** a estratégia escrita é o que você relê antes de ligar para o cliente e quando o caso muda. Rode o modo rever a cada laudo, decisão ou proposta.

**Equipe:** o estagiário ou o advogado júnior monta o rascunho; quem assina decide e o registro mostra quem foi. Se a estratégia passa dias em rascunho, o `/motor-juridico:status` mostra a peça esperando tese.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "70% de chance" | O cliente decide por um número que ninguém calculou | Risco em palavras, com o porquê |
| Valor de cenário inventado | Acordo recusado por conta errada | Valores do advogado no script, o resto `[A DEFINIR]` |
| A IA escolhe o caminho | Linha vermelha cruzada | Seção 10 só com o sim de quem assina |
| Minuta sem tese decidida | Peça escrita na direção errada | `tese-definida` só depois da decisão registrada |
| Decisão só "de boca" | Ninguém sabe por que o caso foi por ali | Seção 10 com quem, quando e o que ficou de fora |
| Estratégia que não muda com o laudo | Caso conduzido pelo plano antigo | Modo rever a cada fato novo |
| Seguir com caso de ex-cliente do outro lado | Conflito de interesses | Parada antes de começar |

## 9. Próximo passo

- Testar o caminho escolhido contra a melhor resposta do outro lado: `advogado-do-diabo` (se instalada; sem ela, os riscos da seção 4 são a lista).
- Com `tese-definida`: `minutar-peca`, ou a habilidade própria do escritório para a peça (se instaladas).
- Contar ao cliente o caminho escolhido: o advogado, em conversa; a `preparar-o-cliente` ou a `status-para-o-cliente`, do motor-experiencia (se instalado), ajudam a preparar.
- Pesquisa que faltou: Jus IA, e depois a `trazer-pesquisa` (se instalada) para guardar na base.

## Referências desta habilidade

- `assets/modelo-estrategia.md`: o formato da estratégia, com a seção 10 da decisão. Use no passo 8.
- `assets/cenarios-exemplo.csv`: modelo do csv de cenários, com valores de exemplo do caso 1. Use no passo 5 e no treino.
- `scripts/cenarios.py`: o quadro de cenários (seção 4.3).
