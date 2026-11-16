---
name: resumo-mensal-do-caso
description: >
  Monta o resumo do mês de cada cliente: em que pé está, o que aconteceu no processo, o que o
  escritório fez mesmo sem movimentação, o que vem agora, o que depende do cliente e quando o
  escritório volta a falar. Curto, no tom da ficha, no formato da ficha: mensagem, .docx (por
  script próprio, sem o cabeçalho interno "Antes de enviar") ou página do caso. Faz um cliente
  ou o lote do mês pela carteira, respeita quem pediu para não receber e nunca leva notícia
  ruim, que vai antes por ligação. Roda a pedido ou no ciclo do agente. Use quando o advogado
  disser "faz o resumo do mês", "resumo da Marta", "os resumos de abril", "manda o resumo
  mesmo sem novidade", "gera o PDF do resumo". Não use para avisar uma movimentação na hora
  (use status-para-o-cliente) nem para a prestação de contas do fim do caso (use
  encerramento-do-caso, se instalada).
---

# Resumo mensal do caso

> O resumo do processo parado é o que mais evita pergunta. Uma vez por mês, o cliente lê em uma tela o que aconteceu, o que o escritório fez, o que vem e o que depende dele. O trabalho que não aparece no site do tribunal passa a aparecer.

Regras comuns do plugin: `../../docs/regras.md`. A carteira: `../../docs/carteira.md`. Fichas: `../../docs/ficha-da-experiencia.md`. O agente e a fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`.

Dia 5. O processo do Jorge não se mexe há dois meses, e ele acha que ninguém olha. No mês, a advogada conferiu o processo duas vezes e pediu a implantação do benefício por petição. Nada disso aparece para ele. O resumo diz em quatro linhas: está na fase de cumprimento, o escritório pediu a implantação em 12/03, o próximo passo é o INSS cumprir, e você não precisa fazer nada. Ele não precisa perguntar.

**Regras fixas desta habilidade:**
1. Nunca leva notícia ruim. Se houve decisão desfavorável, parcial ou que pede escolha do cliente, a ligação vem antes, e o resumo só sai depois, sem repetir a notícia além do combinado na ligação.
2. `pediu_para_nao_receber = sim` não recebe resumo. Insatisfeito ou com reclamação aberta: uma pessoa fala primeiro.
3. "O que o escritório fez" só com o que aconteceu de verdade: as linhas de trabalho do escritório do histórico (canal `trabalho-do-escritorio`) ou o que o advogado disser. Nada inventado para o resumo parecer cheio.
4. Nenhuma data de decisão, chance ou valor a receber não conferido. Data, só de ato já marcado.
5. Marcações e conferências ficam no cabeçalho interno "Antes de enviar", que não vai ao cliente. O .docx sai sem ele, e o script não cria o arquivo enquanto sobrar pendência no texto do cliente (a não ser com `--forcar`, que cria e avisa).

## 1. Quando usar

**Use quando:**
- Chegou o dia do resumo da ficha (`resumo_mensal`) e o escritório quer o lote do mês.
- O advogado quer o resumo de um cliente ("o resumo da Marta").
- A `rotina-da-experiencia` ou o agente de suporte apontou resumos que vencem (modo no ciclo).
- O cliente pediu "um resumo de como está" e a ficha faz resumo.

**Não use quando:**
- Saiu uma movimentação relevante hoje: use `status-para-o-cliente`, na hora. O resumo é do mês, não substitui o aviso.
- O caso terminou: use `encerramento-do-caso` (se instalada). Sem ela, a advogada faz a prestação de contas por escrito e o resumo do último mês só a menciona.
- O escritório não faz resumo (`resumo_mensal: não fazemos`): pergunte se quer começar e, se sim, defina formato e dia pelo `/motor-experiencia:ficha`.
- O pedido é a página do caso inteira: use `pagina-do-caso` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` se existir, e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`).
2. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "O resumo vai por mensagem, em arquivo ou na página do caso, e em que dia do mês?" e, depois, "Quem lê o resumo antes de ele sair?".
3. **Leia do cliente:** a linha da `carteira.csv`, o `clientes/<codigo>/historico.md` (as linhas de contato, com o que foi dito, e as de trabalho do escritório, canal `trabalho-do-escritorio`, com o que foi feito sem falar com o cliente), o resumo do mês anterior (`clientes/<codigo>/resumos/`) e os roteiros de ligação do mês (`clientes/<codigo>/ligacoes/`).
4. **Leia a base:** a jornada do tipo de caso (o "o que vem agora" da fase), o glossário do cliente (`escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md`; sem ele, o glossário da `status-para-o-cliente`) e a biblioteca (chaves da seção 6).
5. **As movimentações do mês:** peça a lista colada ou leia da entrada. Sem movimentação conhecida, o resumo explica a espera, mas alguém precisa ter olhado o processo: pergunte "Alguém conferiu o processo deste cliente este mês?".
6. **Dados.** Só em conta profissional. No resumo, só primeiro nome, tipo de caso e fase.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `resumo_mensal`, `quem_le_antes_de_enviar`.
- **Melhora:** E: `tom_em_tres_palavras` · X: `pagina_do_caso`, `identidade_visual`.

Campo que falta e o resumo pede: pergunte aquele campo, uma vez, e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Um cliente | "O resumo da Marta" | Código e movimentações do mês | O resumo no formato da ficha, para aprovar |
| Lote do mês | Dia do resumo | A carteira | A lista do lote e os resumos, um por um |
| No ciclo | O agente pede | Carteira, histórico, entrada | Rascunhos na fila e itens de "ligação antes" |
| Adaptar | Chamado pela `adaptar-experiencia` | `nicho.md` e os modelos | Modelo do resumo no tom do nicho, com `[ALTERADO]` |

### Passo 1. Quem recebe
Um cliente: confira na carteira `resumo_mensal`, `pediu_para_nao_receber`, `humor`, `reclamacao_aberta` e `fase`. Lote: rode, a partir da pasta desta habilidade,

```
python3 scripts/lote_do_mes.py escritorio/07-operacao/experiencia/carteira.csv AAAA-MM
```

O script separa FAZER, LIGAÇÃO ANTES, APROVADO (FALTA ENVIAR), FEITO e NÃO RECEBE. FEITO é só o resumo com `status: enviado` no cabeçalho de `clientes/<codigo>/resumos/AAAA-MM.md`. Arquivo em `rascunho`, `descartado` ou sem status conta como por fazer, e `aprovado` fica à parte até alguém enviar. Se o escritório não registra o envio no arquivo (a ficha da automação diz, em "Registro do envio do resumo"), acrescente `--sem-registro-de-envio`: aí `aprovado` também conta como feito. Carteira de treino: acrescente `--treino`. Sem Python, aplique as mesmas regras lendo a carteira e o cabeçalho de cada resumo. Mostre a lista e pergunte: "Começo pelos que estão em FAZER?".

### Passo 2. Ligação antes
Para cada cliente em LIGAÇÃO ANTES, nada de resumo agora. Diga quem precisa falar com ele e por quê. Notícia ruim do mês ainda não dada: o roteiro sai pela `status-para-o-cliente`. Depois da ligação, o cliente volta para FAZER, e o resumo diz só o próximo passo combinado ("como conversamos por telefone em 08/04, o próximo passo é...").

### Passo 3. Juntar o mês
Do histórico, das movimentações e do advogado: o que aconteceu no processo, o que o escritório fez (as linhas `trabalho-do-escritorio` desde o último resumo, cada uma em palavras do cliente), o que vem pela jornada, o que depende do cliente (documento, presença, decisão). Mostre em cinco linhas e pergunte o que falta, uma coisa por vez. O que ninguém confirma vai para o "Antes de enviar" como `[A CONFIRMAR]`, e a frase sai do texto do cliente.

### Passo 4. Escrever
Preencha `assets/modelo-do-resumo.md`: o "Antes de enviar" (interno) e as seis partes do cliente, uma ou duas frases cada. Traduza cada termo pelo glossário. Tom e tratamento da ficha, palavras do nicho. Formato da mensagem: chave `resumo-mensal` (`assets/mensagens-do-resumo.md`).

### Passo 5. Conferir
- Nenhuma notícia ruim, nenhuma data de decisão, nenhum valor não conferido.
- Nenhum dado fora do mínimo (CPF, processo, valor da causa, outra parte, saúde).
- "O que o escritório fez" tem fonte (histórico ou advogado).
- O texto do cliente não tem marcação nem campo entre colchetes.
- Cabe numa tela de celular.

### Passo 6. O formato
| `resumo_mensal` na ficha | O que sai |
|---|---|
| mensagem | O texto da chave `resumo-mensal`, para copiar |
| PDF | O .docx pelo script (abaixo), salvo como PDF no Word ou no Google Docs, e a mensagem `resumo-mensal-anexo` |
| página do caso | O mesmo resumo vira a atualização da página pela `pagina-do-caso` (se instalada), com a mensagem `resumo-mensal-anexo`. Sem ela, sai como mensagem e o advogado decide se quer a página depois |

O .docx, a partir da pasta desta habilidade:

```
python3 scripts/resumo_para_docx.py escritorio/07-operacao/experiencia/clientes/<codigo>/resumos/AAAA-MM.md --cor RRGGBB
```

`--cor` é opcional (cor da `identidade_visual`). O script tira o cabeçalho e o "Antes de enviar". Sem `--forcar`, o .docx não é criado enquanto houver pendência no texto do cliente (`[A PREENCHER]`, `[A DEFINIR]`, `[A CONFIRMAR]`, `[CONFERIR]`, campo do modelo entre colchetes em maiúsculas ou instrução do modelo entre colchetes): sai com código 2 e lista o que falta, para alguém resolver no .md e rodar de novo. Com `--forcar`, cria o arquivo mesmo assim, com a pendência em amarelo, e avisa que é só para revisão interna, nunca para enviar. Campo do envio entre chaves (`{...}`) não é pendência e sai em verde no .docx, para quem envia preencher. Duas conferências sem criar nada: `--so-conferir` (o .md) e `--conferir-docx <arquivo.docx>` (um .docx que alguém editou à mão; ali as chaves também contam). Sem `python-docx`, nada é criado (código 1) e o .md continua sendo o documento. O `lote_do_mes.py` já aponta, nos resumos em rascunho e nos aprovados que falta enviar, quais ainda têm pendência e não geram o .docx.

### Passo 7. Mostrar, gravar e registrar
Mostre o "Antes de enviar" e o texto do cliente separados. Com o ok, grave `clientes/<codigo>/resumos/AAAA-MM.md` com `status: aprovado` (e o .docx). Descartado: `status: descartado`, e o cliente volta para FAZER. Depois do envio: `status: enviado` no arquivo (sem isso, o lote e a rotina continuam contando o resumo como por fazer), uma linha de contato no histórico (`| 2026-04-10 17h00 | resumo | secretária | enviou o resumo de abril em PDF |`), e na carteira `ultimo_contato` (data do envio), `ultimo_contato_tipo` = `resumo`, `proximo_contato` = dia do próximo resumo, `motivo_proximo_contato` = `resumo-mensal`, `atualizado_em`. O resumo informa o caso, por isso conta como contato; as linhas de trabalho do escritório que ele cita já estão no histórico e não mudam o `ultimo_contato`.

### Passo 8. Aprender
Pergunte: "Você mudaria alguma coisa nesse resumo?". Correção vira regra curta ("Resumo de trabalhista sempre diz quem são as testemunhas confirmadas"; "Não usar 'aguardando' sozinho, sempre dizer o quê") e, com o ok, entra nos aprendizados (`../../docs/aprender-com-o-uso.md`). Tradução nova vai para o glossário do cliente. Modelo reescrito vai para a biblioteca, na chave desta habilidade.

### No ciclo (chamada pelo agente de suporte)
1. Rode o script do lote. Não pergunte nada.
2. FAZER: monte o resumo com o que está no histórico e nas movimentações da entrada. "O que o escritório fez" sai só das linhas `trabalho-do-escritorio` do mês. Sem nenhuma, não invente: a parte sai e o "Antes de enviar" diz "ninguém registrou trabalho do escritório no mês". Grave em `clientes/<codigo>/resumos/AAAA-MM.md` com `status: rascunho` e o item na fila, `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-resumo-mensal.md` (formato de `../../docs/agentes-e-fila.md`), com o texto do cliente e o caminho do arquivo. Arquivo do mês já em `rascunho` com item pendente na fila: não duplique, só aponte no resumo do dia. Em `descartado`: não reescreva o arquivo (o agente não apaga); item em PARA DECIDIR, com o `motivo_descarte`, para a pessoa dizer se refaz.
3. APROVADO, FALTA ENVIAR: nada novo; uma linha em "fila para aprovar" lembrando de enviar e marcar `status: enviado`.
4. LIGAÇÃO ANTES: nenhum rascunho. Uma linha para PESSOA AGORA ou PARA DECIDIR, com o motivo.
5. NÃO RECEBE: nada. Se há movimentação relevante, item para a pessoa avisar como o cliente prefere.
6. Formato .docx: não rode o script no ciclo; o .docx sai depois da aprovação.

### Modo adaptar
1. Leia o `nicho.md`, o modelo de resumo e as mensagens desta habilidade.
2. Reescreva no tom do nicho: as palavras do cliente, o tamanho (público com pouca leitura pede resumo mais curto, ou áudio lido pela pessoa), o canal (família com conflito: confirmar canal seguro).
3. Marque cada mudança `[ALTERADO]`, mostre, grave com o ok. **Aprender**, como no passo 8.

## 4. O que entra em cada parte

| Parte | Entra | Não entra |
|---|---|---|
| Em que pé está | A fase em palavras simples | O nome técnico sem tradução |
| O que aconteceu | As movimentações do mês, traduzidas; ou o que está sendo esperado | Ato de rotina listado um por um; notícia ruim |
| O que o escritório fez | As linhas de trabalho do escritório do histórico: conferência, petição, pedido, preparação, prazo cumprido, contato com o cartório ou o INSS | "Acompanhamos o processo" sem nada por trás |
| O que vem agora | A próxima etapa pela jornada | Data de decisão; "deve sair logo" |
| O que depende de você | Documento, presença, decisão, com prazo | Pedido de senha ou login |
| Quando a gente volta a falar | O próximo resumo e o aviso se algo acontecer antes | Promessa que a régua não cumpre |

## 5. Exemplo resolvido (Escritório Modelo, treino)

Marta, C-2026-0001, previdenciário, restabelecimento de auxílio, fase `aguardando`, perícia em 2026-04-14. Resumo em PDF no dia 5. Ela estava 36 dias sem notícia (último contato em 2026-03-05): no treino de 2026-04-10, o resumo de abril está atrasado, e a advogada já ligou para ela hoje (mensagem 1 dos casos fictícios). Desde o último contato, o histórico tem duas linhas de trabalho do escritório e a ligação de hoje:
```
| 2026-03-18 15h00 | trabalho-do-escritorio | advogada | enviou ao juiz as perguntas para o perito |
| 2026-04-08 10h30 | trabalho-do-escritorio | advogada | revisou os documentos da perícia e separou o que a cliente leva |
| 2026-04-10 11h40 | ligacao | advogada | explicou o andamento e a perícia; combinou nova ligação em 2026-04-13 |
```

Texto do cliente:
```
# Resumo de abril · Marta

**Em que pé está:** o seu pedido está com o juiz, esperando a perícia médica.

**O que aconteceu no processo:** a perícia continua marcada para terça, 14/04. Em 18/03 o juiz recebeu as perguntas que o perito vai responder.

**O que o escritório fez:** mandamos ao juiz as perguntas para o perito, revisamos os documentos que você vai levar e falamos com você por telefone hoje.

**O que vem agora:** depois da perícia, o perito entrega o relatório dele ao juiz. O tempo disso depende da vara.

**O que depende de você:** ir à perícia com o documento com foto e os documentos médicos que você tem. Se alguém puder ir com você, melhor.

**Quando a gente volta a falar:** na segunda, 13/04, para confirmar a perícia, e no resumo de maio, até o dia 5.

Equipe Escritório Modelo
```

No "Antes de enviar": "Conferir com a advogada a orientação da perícia antes de juntar; o horário da perícia fica fora do resumo e vai na orientação da `preparar-o-cliente`; resumo atrasado (devia sair em 05/04): registrar a falha da régua nos aprendizados." O Ivan não recebe resumo (pediu); o Jorge e a Camila ficam em LIGAÇÃO ANTES.

## 6. As chaves da biblioteca (desta habilidade)

| Chave | Modelo | No `inicio-automacao` |
|---|---|---|
| `resumo-mensal` | O resumo em mensagem | modelo 9 |
| `resumo-mensal-anexo` | A mensagem que acompanha o PDF ou o link da página | (novo) |

Biblioteca: `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`. Esta habilidade só cria ou reescreve as chaves dela.

## 7. Formato da saída

**Um cliente:** primeiro o bloco "Antes de enviar" (interno), depois o texto do cliente, separado, e por fim o formato (mensagem, .docx ou página), o caminho do arquivo e as linhas propostas da carteira e do histórico.

**Lote:** a lista do script (FAZER, LIGAÇÃO ANTES, FEITO, NÃO RECEBE), depois os resumos de FAZER, um por um, no formato acima, e no fim: quantos prontos, quantos esperando ligação, quantos com pendência no "Antes de enviar".

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Resumo do mês (.md e, se for o formato, .docx) | `escritorio/07-operacao/experiencia/clientes/<codigo>/resumos/AAAA-MM.md` |
| Rascunho no ciclo | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-resumo-mensal.md` |
| Envio registrado | `clientes/<codigo>/historico.md` e `carteira.csv` (`ultimo_contato`, `ultimo_contato_tipo`, `proximo_contato`, `motivo_proximo_contato`, `atualizado_em`) |
| Modelos aprovados | `biblioteca-de-mensagens.md`, chaves da seção 6 |
| Regras aprendidas | `escritorio/04-base/comum/aprendizados-experiencia.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/clientes/<codigo>/resumos/` |

Sem pasta aberta: o resumo vem no chat, com o "Antes de enviar" separado do texto do cliente, e as linhas da carteira para colar.

## 9. Solo e equipe

**Solo:** faça o lote num horário fixo do dia do resumo, com o script do lote. Vinte resumos de quatro linhas cabem numa manhã, porque o histórico já tem o que aconteceu. Quem não teve nada no mês leva o resumo mais curto, e é ele que mais evita a pergunta.

**Equipe:** a secretária monta o lote e os resumos a partir do histórico; `quem_le_antes_de_enviar` lê cada um; a advogada fica com LIGAÇÃO ANTES. Conferência a fundo por amostra: um resumo por área por mês, contra o processo.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Resumo com a sentença ruim | O cliente lê sozinho a pior notícia | Regra fixa 1 e o grupo LIGAÇÃO ANTES |
| Resumo para quem pediu para parar | Quebra do combinado | NÃO RECEBE no script |
| "Acompanhamos o processo" sem nada | O cliente percebe que é texto pronto | Regra fixa 3 |
| Resumo só de quem teve movimentação | O cliente do processo parado é o que mais pergunta | Lote pela carteira inteira |
| `[CONFERIR]` no PDF do cliente | Documento com cara de rascunho | Cabeçalho interno e o script que barra |
| "A decisão deve sair em maio" | Promessa de data | Regra fixa 4 |
| Resumo longo | Ninguém lê | Seis partes, uma tela |

## 11. Próximo passo

- Cliente em LIGAÇÃO ANTES: `status-para-o-cliente`, roteiro de ligação.
- Formato página do caso: `pagina-do-caso` (se instalada).
- Termo novo no resumo: glossário do cliente, pela `status-para-o-cliente`.
- O que vem em cada fase ainda genérico: `jornada-do-cliente`.
- Aprovar os rascunhos do ciclo: `/motor-experiencia:fila`.

## Referências desta habilidade

- `assets/modelo-do-resumo.md`: o formato do arquivo do mês, com o "Antes de enviar" interno. Use no passo 4.
- `assets/mensagens-do-resumo.md`: os modelos crus das chaves `resumo-mensal` e `resumo-mensal-anexo`. Use nos passos 4 e 6.
- `scripts/lote_do_mes.py`: a lista do lote pela carteira e pelo `status` de cada resumo do mês. Rode no passo 1 (`--sem-registro-de-envio` quando o escritório não marca o envio).
- `scripts/resumo_para_docx.py`: o .docx do cliente, sem o cabeçalho interno. Rode no passo 6.
