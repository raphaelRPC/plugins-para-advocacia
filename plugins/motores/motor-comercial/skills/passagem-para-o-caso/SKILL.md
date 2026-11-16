---
name: passagem-para-o-caso
description: >
  Depois que o advogado marca o contato como fechado, faz a passagem do comercial para quem vai
  cuidar do caso: a ficha de passagem com o que foi prometido e combinado na consulta e na
  proposta, o escopo, os valores e a forma de pagamento, os documentos pendentes, os prazos
  ditos ao cliente, quem cuida, como o cliente prefere ser contatado, o humor e os cuidados. Cria
  a linha da carteira do motor-experiencia, quando ele está em uso, e o aviso a quem cuida do
  caso. Mínimo de dados, e nunca move o contato para fechado sozinha. Use quando o advogado disser "assinou, passa para o caso",
  "fechou, o que eu entrego para a equipe?", "faz a passagem da Marta", "quem vai cuidar desse
  cliente e o que prometemos?". Não use para a minuta do contrato (use contrato-de-honorarios)
  nem para a mensagem de boas-vindas ao cliente (use boas-vindas-do-cliente, do
  motor-experiencia).
---

# Passagem para o caso

> O que o cliente ouviu antes de assinar precisa chegar inteiro a quem vai cuidar dele depois. A passagem junta numa ficha só o que foi prometido, combinado e pago, e avisa quem assume.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-comercial.md`. Funil (etapa `fechado`): `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Agente e fila: `../../docs/agentes-e-fila.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

A cliente assinou na sexta. Na consulta, a advogada disse "te mando a lista de documentos até segunda". Na segunda, quem abre o caso é a secretária, que não estava na consulta. A lista não sai, e na quarta a cliente escreve: "vocês esqueceram de mim?".

**Regras fixas desta habilidade:**
1. Nunca move o contato para `fechado`. A passagem começa quando a etapa já é `fechado`, ou quando o advogado confirma a assinatura nesta conversa e grava a etapa ele mesmo, com o ok.
2. A passagem só repete o que tem fonte: ata, proposta, contrato, mensagem enviada ou o advogado nesta conversa. Nada de promessa nova. Frase que soa como garantia de resultado ou prazo de decisão vai marcada para o advogado, e não para a equipe repetir.
3. Mínimo necessário: primeiro nome, área, tipo de caso, combinados. Nada de CPF, endereço, número do processo, dado de saúde em detalhe ou dado de criança. Vulnerabilidade aparece como cuidado, sem o detalhe.
4. A linha da carteira e o aviso só saem com o ok. Esta habilidade não escreve para o cliente: a boas-vindas é da experiência.
5. Dado da conversa com o cliente que não está em nenhuma fonte é pergunta, uma por vez, nunca suposição.

## 1. Quando usar

**Use quando:**
- O advogado marcou `fechado` (ou acabou de dizer "assinou") e o caso precisa passar para quem vai cuidar dele.
- Há contatos `fechado` sem ficha de passagem e o advogado quer fazer todas (lote).
- O `agente-comercial` encontrou um `fechado` sem passagem (modo no ciclo).
- A `adaptar-comercial` (se instalada) pediu a ficha de passagem no jeito do nicho (modo adaptar).

**Não use quando:**
- O contrato ainda não foi assinado: use `contrato-de-honorarios` (se instalada). A passagem espera.
- O pedido é a mensagem de boas-vindas, o checklist de documentos ou a jornada do cliente: use a `boas-vindas-do-cliente` do motor-experiencia (se instalado). Sem ele, a pessoa que cuida do caso manda a boas-vindas a partir da ficha de passagem.
- O cliente já está na carteira há tempo e o pedido é um resumo do caso: é trabalho da experiência, não do comercial.

## 2. Antes de começar

1. **Leia as fichas:** `escritorio/04-base/comum/ficha-do-escritorio.md` (`quem_atende`, `substituto`, `historico_do_cliente`, `sistema_juridico`, `tratamento`) e `escritorio/04-base/comum/ficha-comercial.md`.
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`), se existir: os cuidados e os documentos típicos do nicho ajudam a ver o que a passagem não pode esquecer.
3. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado de passagem vale antes do padrão desta habilidade.
4. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`) e, para o código, tudo o que existir: `triagens/`, `consultas/<codigo>-*.md`, `propostas/<codigo>-proposta-v*.md`, `contratos/<codigo>-contrato-v*.md` e os itens da fila com o código e `status: enviado` (`fila/*/NN-<codigo>-*.md`).
5. **Veja se o motor-experiencia está em uso:** existe `escritorio/07-operacao/experiencia/`, ou `escritorio/04-base/comum/ficha-da-experiencia.md`, ou o plugin está instalado (a `boas-vindas-do-cliente` aparece entre as habilidades). Se a ficha da experiência existir, leia `quem_cuida_dos_casos`, `maximo_sem_noticia`, `resumo_mensal` e `pagina_do_caso`.
6. **Conta de IA.** A passagem tem dado de cliente: só em conta profissional ou de equipe. Em conta pessoal, só caso fictício, gravado em `escritorio/07-operacao/_treino/comercial/passagens/` e `_treino/experiencia/carteira.csv`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `quem_atende`.
- **Melhora:** E: `historico_do_cliente`, `sistema_juridico`.

Para a linha da carteira, lê também da ficha da experiência do motor-experiencia, se existir: X: `quem_cuida_dos_casos`, `maximo_sem_noticia`, `resumo_mensal`, `pagina_do_caso`. Campo que falta e a passagem pede: pergunte aquele campo, uma vez; sem resposta, siga com `[A PREENCHER]` e diga no fim o que ficou em aberto.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Um contato, a pedido | "Assinou, passa para o caso" | O código e as fontes da pasta | Ficha de passagem, linha da carteira, aviso, linha do funil |
| B. Direto | O advogado diz tudo ("passagem da C-2026-0001, cuida a advogada, faltam 3 documentos") | O pedido e as fontes | O mesmo do modo A, perguntando só o que falta |
| C. Lote | Vários `fechado` sem passagem | O registro | Uma ficha por contato, mostradas uma por uma |
| D. No ciclo | O `agente-comercial` chama | O registro e as fontes | Ficha em rascunho; carteira e aviso vão para "PARA DECIDIR" |
| E. Adaptar | A `adaptar-comercial` chama | O nicho e o modelo da ficha | Modelo da ficha com `[ALTERADO]`, gravado só com o ok |

### A. Um contato (a pedido)

**Passo 1. Confirmar o fechamento.** Leia a linha do contato.
- Etapa `fechado`: siga.
- Outra etapa: pergunte "O contrato foi assinado? A etapa `fechado` é sua: eu só gravo se você confirmar." Com o sim, mostre a linha com `etapa = fechado` e a data, e grave só com o ok explícito. Sem o sim, pare: "A passagem começa depois da assinatura."

**Passo 2. Juntar as fontes.** Leia o que existe (seção 2, item 4) e mostre uma lista curta: o que achou e o que falta ("achei a ata, a proposta v1 e o contrato v1; não achei mensagem enviada depois da proposta").

**Passo 3. Montar a ficha.** Preencha `assets/modelo-passagem.md` pela tabela da seção 4. Cada combinado com a data e a fonte. O que nenhuma fonte responde vira pergunta, uma de cada vez, no máximo estas quatro:
1. "Quem vai cuidar do caso e quem fala com o cliente no dia a dia?"
2. "Ficou combinado mais alguma coisa com o cliente que não está na ata, como 'te mando notícia até sexta'?"
3. "Ele disse como prefere ser contatado: canal, horário, texto ou ligação?"
4. "Como ele saiu da consulta: tranquilo, ansioso, desconfiado?"

**Passo 4. Checar.** Rode a checagem da seção 5. Frase com promessa de resultado ou de prazo de decisão: mostre ao advogado e pergunte se foi dito. Se foi, entra marcada ("dito na consulta; não repetir; o advogado conversa com o cliente"). Se não foi, sai.

**Passo 5. Mostrar e gravar a ficha.** Mostre a ficha inteira. Com o ok, grave `escritorio/07-operacao/comercial/passagens/<codigo>.md` com `status: rascunho`. Quando quem cuida do caso ler e confirmar, o status vira `conferida`.

**Passo 6. A linha da carteira.**
- **Motor-experiencia em uso:** monte a linha pela seção 4.2 e rode o script, primeiro só para mostrar, com o caminho da pasta desta habilidade (a que contém este SKILL.md), o caminho da carteira e os campos como argumentos:

```
python3 "<pasta desta habilidade>/scripts/linha_da_carteira.py" "escritorio/07-operacao/experiencia/carteira.csv" codigo=C-2026-0001 nome_curto=Marta area=previdenciario "tipo_de_caso=restabelecimento de auxílio" responsavel=advogada inicio=2026-03-20
```

O script confere as colunas de `docs/carteira.md` do motor-experiencia, as datas, as opções (em `motivo_proximo_contato`: `boas-vindas`, `ligacao-pendente`, `resumo-mensal`, `maximo-sem-noticia`, `compromisso`, `documento`, `retorno-combinado`, `pesquisa` e `depois-do-caso`; em `pagina_do_caso`: `link`, `pdf`, `os-dois` ou `nao`), o código repetido (segundo caso do mesmo cliente usa `-2`), vírgula dentro de campo e qualquer coisa que pareça CPF, número de processo, telefone ou e-mail. Sem `--gravar`, ele só mostra, e mostra também quando a carteira ainda não existe: a primeira linha de colunas que seria criada e a linha nova, sem gravar nada. Mostre as duas ao advogado. Com o ok, rode de novo com `--gravar` (e `--criar`, se a carteira ainda não existe). Ele acrescenta no fim, com o mesmo separador do arquivo, e nunca reescreve o que já está lá. `--gravar` sem `--criar` numa carteira que não existe sai com erro e não cria nada.
- **Sem o motor-experiencia:** a linha vai para a seção 12 da ficha de passagem, pronta para quando o plugin for instalado. Diga em uma linha: "Sem o motor-experiencia, a pessoa que cuida do caso manda a boas-vindas a partir desta ficha."
- Sem execução de código: mostre a linha no formato de `docs/carteira.md` do motor-experiencia, para colar na planilha.

**Passo 7. Atualizar o funil.** A etapa continua `fechado`. Mostre e grave com o ok: `responsavel` com quem cuida do caso, `proximo_passo` "passagem feita; boas-vindas com [quem]", `data_proximo_passo` com a data da primeira promessa (ou a de hoje) e `atualizado_em`.

**Passo 8. O aviso a quem cuida.** Escreva o aviso no formato da seção 6 e mostre. Quem manda é uma pessoa, pelo canal interno da equipe (mensagem, e-mail, tarefa no sistema). No escritório solo, o aviso vira o primeiro item da agenda do dia seguinte.

**Passo 9. Aprender.** Pergunte: "Faltou alguma coisa nesta passagem que a equipe vai precisar?". Correção vira regra curta nos aprendizados, com o ok ("Passagem de família: sempre dizer quem pode buscar documentos pelo cliente").

### C. Lote

Liste os `fechado` sem `passagens/<codigo>.md`, do mais antigo para o mais novo. Faça um por vez, pelo modo A, e mostre cada ficha antes de gravar. As perguntas do passo 3 vêm agrupadas por contato.

### D. No ciclo (o agente chama)

1. Liste os contatos `fechado` sem ficha de passagem.
2. Para cada um, monte a ficha só com o que as fontes dizem, com `[A CONFIRMAR]` onde faltar resposta, e grave com `status: rascunho`.
3. Não crie a linha da carteira e não grave o funil além de `proximo_passo` ("conferir passagem"), `data_proximo_passo` e `atualizado_em`. No resumo do dia, em "PARA DECIDIR": "C-2026-0001 fechou; passagem em rascunho; conferir e criar a linha da carteira".
4. A passagem não vai para a fila de aprovação: ela é interna. O aviso a quem cuida vai no resumo do dia, na parte "para a experiência do cliente".
5. Contato que não está em `fechado`: o ciclo não faz passagem, mesmo que haja contrato na pasta. Contrato sem `fechado` vai para "PARA DECIDIR" ("contrato v1 na pasta; a assinatura foi confirmada?").

### E. Adaptar (a adaptar-comercial chama)

1. Leia `nicho.md` (cuidados do nicho, documentos típicos, momentos de aflição) e o modelo da ficha.
2. Reescreva as seções 7, 8 e 9 do modelo para o nicho, marcando cada mudança `[ALTERADO]`: os documentos que o nicho sempre pede, as perguntas de contato que importam (quem fala pelo cliente, horário de quem trabalha no campo), os cuidados que a equipe precisa saber.
3. Mostre o antes e o depois. Grave em `escritorio/04-base/comercial/modelos/modelo-passagem.md` só com o ok. A partir daí, esse modelo manda.

### Último passo, em todos os modos: Aprender

Toda correção do advogado vira proposta de aprendizado, com a pergunta "Quer que eu guarde isto para as próximas vezes?" e a regra em uma linha (`../../docs/aprender-com-o-uso.md`). No ciclo, a correção feita na fila (item `descartado` ou `ajustado` com motivo) vira a mesma proposta no resumo do dia. Nada entra nos aprendizados sem o ok.

## 4. De onde vem cada parte

### 4.1 A ficha de passagem

| Seção da ficha | Fonte | Se não houver |
|---|---|---|
| Em três linhas | Contrato e ata | Pergunta 1 e o contrato |
| Quem cuida | `quem_atende`, `substituto`, `quem_cuida_dos_casos` (X), o advogado | Pergunta 1 |
| O caso contratado | Contrato e proposta aceita, itens iguais | Pare: sem contrato, não há passagem |
| Valores e pagamento | Contrato (cenário escolhido, êxito, despesas) | Proposta aceita, com `[A CONFIRMAR]` |
| Prometido e combinado | Ata, proposta, contrato, mensagens com `status: enviado` | Pergunta 2 |
| Prazos ditos ao cliente | Ata e mensagens enviadas, do jeito que foram ditos | "nenhum prazo registrado" |
| Documentos pendentes | Ata e contrato | `[A CONFIRMAR]` |
| Como o cliente prefere | Ata, canal do registro | Pergunta 3 |
| Humor e cuidados | Ata, triagem | Pergunta 4 |
| O que não está aqui | `historico_do_cliente`, `sistema_juridico` | `[A PREENCHER]` |

### 4.2 A linha da carteira

| Coluna | De onde |
|---|---|
| `codigo`, `nome_curto`, `area` | O registro do funil, iguais |
| `tipo_de_caso` | O contrato, em até 5 palavras, sem dado sensível |
| `responsavel` | Quem cuida (passo 3) |
| `inicio` | Data da assinatura |
| `fase` | `entrada` |
| `ultimo_contato`, `ultimo_contato_tipo` | A última mensagem que informou algo (envio do contrato ou confirmação da assinatura) |
| `proximo_contato`, `motivo_proximo_contato` | A primeira data prometida ao cliente (`retorno-combinado`). Sem promessa, a boas-vindas ainda não saiu: o dia seguinte à assinatura (ou o que a jornada da ficha da experiência disser), com `boas-vindas`. Boas-vindas já enviada pelo comercial: `inicio` mais `maximo_sem_noticia` (`maximo-sem-noticia`). Sem nenhum dos três, vazio e dito no fim. `depois-do-caso` não se usa na passagem: é do fim do caso, na experiência |
| `proximo_compromisso`, `data_compromisso` | Só se já houver perícia, audiência ou reunião marcada |
| `documentos_pendentes` | Quantos da seção 7 da ficha |
| `humor` | Pergunta 4, ou `a-confirmar` |
| `reclamacao_aberta`, `pediu_para_nao_receber` | `nao`, a não ser que o cliente tenha pedido |
| `resumo_mensal`, `pagina_do_caso` | Ficha da experiência; sem ela, vazio |
| `satisfacao`, `encerrado_em` | Vazios |
| `atualizado_em` | Hoje |

## 5. Checagem antes de mostrar

- [ ] O contato está em `fechado`, marcado por uma pessoa.
- [ ] Escopo, exclusões e valores iguais aos do contrato.
- [ ] Cada combinado tem data e fonte; nada sem fonte entrou.
- [ ] Nenhuma frase de promessa de resultado ou de prazo de decisão sem a marcação para o advogado.
- [ ] Sem CPF, endereço, número do processo, telefone, e-mail, dado de saúde em detalhe ou dado de criança.
- [ ] Quem cuida está escrito, com substituto.
- [ ] A linha da carteira passou pelo script sem erro, mostrada antes de gravar (com a primeira linha de colunas, se a carteira ainda não existe).

## 6. Formato da saída

Ordem: as fontes encontradas, a ficha de passagem, a linha da carteira (ou a seção 12 da ficha), a linha do funil e o aviso.

**O aviso (interno, uma pessoa manda pelo canal da equipe):**

```
PASSAGEM · [CÓDIGO] · [PRIMEIRO NOME] · [ÁREA]
Fechou em [DATA]. Cuida: [RESPONSÁVEL]. Dia a dia: [QUEM].
Primeiro passo: [O QUE] até [DATA] ([DE ONDE VEIO A PROMESSA]).
Prometido: [UMA LINHA COM OS COMBINADOS].
Faltam [N] documentos. Humor: [UMA PALAVRA E O PORQUÊ EM POUCAS PALAVRAS].
Ficha completa: 07-operacao/comercial/passagens/[CÓDIGO].md
```

O exemplo completo (caso 1, Marta, C-2026-0001), com a ficha, a linha da carteira, o funil, o aviso e o que a checagem pegou, está em `references/exemplo-passagem.md`. Leia na primeira passagem do escritório.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Ficha de passagem | `escritorio/07-operacao/comercial/passagens/<codigo>.md` |
| Linha da carteira (motor-experiencia em uso) | `escritorio/07-operacao/experiencia/carteira.csv`, uma linha nova no fim, pelo script |
| Linha da carteira (sem o motor-experiencia) | Seção 12 da ficha de passagem |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `responsavel`, `proximo_passo`, `data_proximo_passo`, `atualizado_em` (e `etapa = fechado` só com o ok do advogado, passo 1) |
| Aviso a quem cuida | No chat, para a pessoa mandar; no ciclo, no resumo do dia |
| Modelo da ficha do escritório (modo E) | `escritorio/04-base/comercial/modelos/modelo-passagem.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino com casos fictícios | `escritorio/07-operacao/_treino/comercial/passagens/` e `_treino/experiencia/carteira.csv` |

Sem pasta aberta: entregue a ficha, a linha da carteira e o aviso em texto pronto para copiar, com o caminho onde cada um ficaria.

## 8. Solo e equipe

**Solo:** quem vende e quem cuida é a mesma pessoa, e a passagem parece desnecessária até a terceira semana, quando ninguém lembra o que foi prometido a quem. A ficha vira o registro do combinado, e o aviso vira o lembrete do primeiro passo.

**Equipe:** a secretária faz a passagem logo depois que o advogado marca `fechado`. Quem cuida do caso lê, confirma e muda o status para `conferida`. Se a mesma pessoa aparece como responsável em todas as passagens, aponte: ali está o gargalo da experiência.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Promessa da consulta que ninguém cumpre | "Vocês esqueceram de mim?" na primeira semana | Seção 5 da ficha, com quem cumpre e até quando |
| A IA marcar `fechado` | Caso começa sem contrato assinado | Regra fixa 1 |
| Equipe repetindo uma frase de garantia dita no calor da consulta | Promessa de resultado multiplicada | Checagem e marcação para o advogado |
| CPF ou número do processo na carteira | Dado pessoal fora do necessário | Regra fixa 3 e o script |
| Linha duplicada na carteira | Dois cadastros do mesmo cliente | O script recusa código repetido |
| Carteira criada sem ninguém ver | Arquivo novo com colunas que ninguém conferiu | Sem `--gravar`, o script mostra a primeira linha e a linha nova; só cria com `--gravar --criar` |
| Escopo diferente entre contrato e o que a equipe sabe | Trabalho a mais sem cobrança, ou cliente frustrado | Itens copiados do contrato |
| Cliente que prefere ligação recebendo notícia por mensagem | Desconfiança desde o começo | Seção 8 da ficha |

## 10. Próximo passo

- Boas-vindas, documentos e jornada: `boas-vindas-do-cliente` do motor-experiencia (se instalado), que lê esta ficha. Sem ele, quem cuida do caso manda a boas-vindas a partir da ficha e combina a primeira notícia.
- Documentos que faltam: `checklist-de-documentos` do motor-experiencia (se instalado). Sem ele, a secretária cobra pela seção 7 da ficha.
- O funil do mês, com este fechamento: `painel-do-funil` (se instalada). Sem ela, o `/motor-comercial:status` mostra o funil.

## Referências desta habilidade

- `assets/modelo-passagem.md`: o modelo da ficha de passagem. Leia no passo 3 do modo A e no modo E.
- `references/exemplo-passagem.md`: a passagem completa do caso 1. Leia na primeira passagem do escritório.
- `scripts/linha_da_carteira.py`: monta, confere e acrescenta a linha da carteira. Rode no passo 6.
