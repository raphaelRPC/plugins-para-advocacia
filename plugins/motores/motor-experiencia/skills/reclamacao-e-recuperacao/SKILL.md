---
name: reclamacao-e-recuperacao
description: >
  Cuida da reclamação de quem já é cliente: dá um dono (quem assume, no prazo da ficha), monta o
  registro com o que o cliente disse, desde quando, o que o escritório fez e o que falhou de fato,
  prepara o roteiro da ligação (escutar, reconhecer sem culpar ninguém, explicar, combinar o que
  muda e quando), lista o que o escritório pode oferecer sem desconto como regra, escreve a
  mensagem de retorno do que foi combinado para a advogada ler, marca a reclamação na carteira com
  a pessoa e transforma a causa em ajuste na jornada, na ficha e nos aprendizados. Use quando o
  advogado disser "o cliente reclamou", "ele disse que vai na OAB", "a cliente está brava com a
  demora", "quer trocar de advogado", "nota baixa na pesquisa", "como eu ligo para ela". Não use
  para dar notícia ruim do processo (use status-para-o-cliente).
---

# Reclamação e recuperação

> Uma pessoa assume, escuta, reconhece o que falhou, combina o que muda e cumpre. A IA prepara o registro, o roteiro e a mensagem do que foi combinado; a conversa é de gente.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-da-experiencia.md` e `../../docs/ficha-da-experiencia-modelo.md`. Carteira: `../../docs/carteira.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

Sexta, 11h15: "Já é a terceira vez que eu pergunto e ninguém me dá uma resposta. Vou procurar a OAB." A vontade é responder rápido, se explicar ou mandar um "calma, está tudo certo". As três pioram. O cliente quer falar com quem decide, quer saber o que aconteceu e quer ver alguma coisa mudar.

**Regras fixas desta habilidade:**
1. Uma pessoa assume sempre (`quem_assume_reclamacao`), por ligação ou reunião, no prazo da ficha. A IA nunca responde a reclamação com texto pronto de desculpa nem por mensagem automática.
2. Reconhecer sem culpar: nem o cliente ("você não entendeu"), nem a equipe ("a secretária esqueceu"). Fala-se do que o escritório fez e do que falhou.
3. Nada de desconto como regra, nada de oferta para o cliente deixar de reclamar. Procurar a OAB ou outro advogado é direito dele: o escritório nunca desencoraja, ameaça ou condiciona alguma coisa a isso.
4. O registro diz o que falhou de fato, com data e fonte. O que ninguém sabe fica `[A CONFIRMAR]`. Sem defesa inventada, sem culpa inventada.
5. Toda reclamação termina numa causa e num ajuste (jornada, ficha, biblioteca ou aprendizado), aplicado só com o ok.

## 1. Quando usar

**Use quando:**
- O cliente reclamou por mensagem, ligação ou pessoalmente, mesmo de um jeito leve ("de novo ninguém me respondeu").
- O cliente falou em procurar a OAB, trocar de advogado, desistir do caso ou "contar para todo mundo".
- A `pesquisa-de-satisfacao` (se instalada) trouxe nota baixa e a pessoa quer fazer o retorno.
- A carteira mostra `humor = insatisfeito` sem reclamação registrada.
- A `triar-mensagem-do-cliente` (se instalada) ou o ciclo apontaram "reclamação".
- A `auditar-conversas` (se instalada) achou uma falha que o cliente sentiu.

**Não use quando:**
- O problema é a notícia ruim do processo (sentença contrária, benefício negado): é ligação do advogado pela `status-para-o-cliente` (se instalada). Se além da notícia houver queixa do escritório, as duas andam juntas.
- O cliente só pergunta do andamento, sem queixa: `status-para-o-cliente` ou `triar-mensagem-do-cliente`.
- O escritório errou e isso pode ter consequência no processo (prazo perdido, recurso não interposto): pare. Vai agora para o advogado responsável e para o titular. A habilidade só registra os fatos; o resto é decisão jurídica `[CONFERIR]`.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), o `nicho.md` se existir (aflições típicas e o que nunca dizer a esse público) e os aprendizados (`aprendizados-experiencia.md`).
2. **Leia o caso pelo lado do cliente:** a linha dele na `carteira.csv`, o `clientes/<codigo>/historico.md`, as reclamações anteriores em `07-operacao/experiencia/reclamacoes/` e a jornada do tipo de caso (`04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md`), se existir.
3. **A conversa da reclamação:** peça que colem a mensagem ou a conversa. Anonimize o que não for necessário (`[DOC]`, `[PROCESSO]`, `[CONTATO]`) e avise em uma linha.
4. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se quiserem seguir, pergunte só os dois campos de que a tarefa precisa (abaixo), um de cada vez, e ofereça gravar.
5. **Conta de IA:** em conta pessoal, só o caso fictício (o Jorge, de `../../docs/casos-ficticios.md`), gravando em `escritorio/07-operacao/_treino/experiencia/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `quem_assume_reclamacao`, `prazo_de_retorno_da_reclamacao`.
- **Melhora:** X: `o_que_o_escritorio_oferece`.

Lê também, como todas as habilidades, o tom e o tratamento da ficha do escritório. Sem `o_que_o_escritorio_oferece`, a seção 6 sai com a lista-base marcada `[A DEFINIR]` e a pessoa escolhe na hora.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | O que não faz |
|---|---|---|---|
| A pedido | O advogado ou a equipe | Os passos 1 a 10, mostrando cada peça no chat | Não grava nada sem o ok |
| No ciclo | O `agente-de-suporte` | Passos 1, 4 e 5: rascunho do registro e do roteiro, gravados como rascunho; o cliente vai para "PESSOA AGORA" no resumo do dia | Nenhuma mensagem para o cliente na fila; não mexe em `reclamacao_aberta` nem em `humor` |
| Adaptar | A `adaptar-experiencia` (se instalada) | Reescreve o roteiro e a mensagem de retorno para o nicho, cada mudança marcada `[ALTERADO]` | Só grava com o ok |
| Treino | Quem quer ver funcionando | O caso do Jorge do começo ao fim | Grava só em `_treino/experiencia/` |

### Passo 1. Separar o que para tudo
Leia a reclamação procurando: sinal de violência, risco à vida, vulnerabilidade, dado de saúde, ou falha do escritório com consequência no processo. Achou um: diga em uma frase o que apareceu e que vai para o advogado agora, sem rascunho para o cliente (seção 5 de `regras.md`).

### Passo 2. Dar o dono e o prazo
Pergunte, uma de cada vez:
- "Quem assume esta reclamação? Pela ficha, é [quem_assume_reclamacao]."
- "Até quando sai a ligação? Pela ficha, [prazo_de_retorno_da_reclamacao]."
Campo vazio: pergunte e ofereça gravar na ficha. Quem assume é uma pessoa com nome de função, e é ela que liga.

### Passo 3. Resposta-ponte (só se a ligação demorar)
Se a ligação não sai na próxima hora, ofereça uma resposta-ponte curta (A, a pessoa que assume lê, decide se sai e envia). É a mesma regra da `ponte-pessoa-agora` da `triar-mensagem-do-cliente`: no máximo uma mensagem, sem conteúdo do caso, e só se a ficha permitir (`resposta_ponte` preenchida e nenhum aprendizado contra):

> "Oi, [NOME]. Li sua mensagem. A [FUNÇÃO DE QUEM ASSUME] vai te ligar hoje até as {HORÁRIO} para conversar com calma."

`{HORÁRIO}` é campo do envio: quem vai ligar escolhe dentro do `prazo_de_retorno_da_reclamacao` e preenche antes de enviar. Sem desculpa genérica, sem explicação do processo, sem "fique tranquilo". A explicação vem na ligação. No ciclo, nenhuma ponte: o cliente vai para PESSOA AGORA. Se o cliente pediu para não receber ligação, a conversa é por reunião ou pelo canal que ele escolheu.

### Passo 4. Montar o registro
Use `assets/registro-de-reclamacao.md`. Preencha com fatos e fonte:
- **O que o cliente disse:** as palavras dele, anonimizadas.
- **Desde quando:** a primeira vez que a queixa aparece no histórico ou na conversa.
- **O que o escritório fez:** cada ato com data (mensagem, ligação, movimentação, resumo), tirado do histórico e da carteira.
- **O que falhou de fato:** compare com a régua da ficha e da jornada (`maximo_sem_noticia`, `primeira_resposta_cliente_ativo`, retorno prometido, resumo mensal). Escreva a falha, não o culpado.
- **O que não se sabe:** `[A CONFIRMAR]`, com quem sabe.
Mostre e grave com o ok em `escritorio/07-operacao/experiencia/reclamacoes/<codigo>-AAAA-MM-DD.md`.

### Passo 5. Preparar a ligação
Monte o roteiro com `assets/roteiro-da-ligacao.md`: abrir, escutar, reconhecer, explicar, combinar, fechar (seção 5). A parte "explicar" traz o andamento traduzido e conferido pelo advogado (pela `status-para-o-cliente`, se instalada). Grave em `clientes/<codigo>/ligacoes/AAAA-MM-DD.md`. A ligação é H.

### Passo 6. Escolher o que oferecer
Mostre a lista da seção 6 a partir de `o_que_o_escritorio_oferece` e pergunte: "Destas, o que você quer oferecer a [NOME]?". A escolha é de quem assume.

### Passo 7. Depois da ligação: a mensagem do que foi combinado
Pergunte: "Como foi a conversa? O que ficou combinado, e para quando?". Com a resposta, escreva a mensagem de retorno (A, lida por quem assume): o que vai mudar, quem faz, a próxima data de contato e o canal. Mostre no chat. Se o escritório usa a fila, grave como `fila/AAAA-MM-DD/NN-<codigo>-retorno-de-reclamacao.md`, status `pendente`.

### Passo 8. Atualizar a carteira e o histórico (com a pessoa)
É este passo que tira o cliente de PESSOA AGORA: sem ele, o item volta ao topo do resumo seguinte. Quando quem assume contar como foi, ou quando o comando `/motor-experiencia:fila` perguntar "Já falou? O que ficou combinado?", proponha e grave só com o ok de quem assume:
- quando a pessoa assume: `reclamacao_aberta = sim`;
- depois da ligação: `ultimo_contato`, `ultimo_contato_tipo = ligacao`, `proximo_contato` = a data combinada, `motivo_proximo_contato = retorno-combinado`, e o `humor` que a pessoa disser;
- uma linha de contato em `clientes/<codigo>/historico.md`, com o combinado em uma frase e sem o conteúdo da conversa (`| 2026-04-10 15h40 | ligacao | advogada | ligação sobre a reclamação; combinou relato por escrito até 2026-04-13 |`). A ligação informou o caso, por isso muda o `ultimo_contato`; a resposta-ponte do passo 3 não muda;
- no registro, `situacao: combinada`.
**Fechar:** quando o combinado foi cumprido e a pessoa confirma que o cliente está atendido, `reclamacao_aberta = nao` e `situacao: fechada`, com a data. Nunca feche só porque o cliente parou de escrever.

### Passo 9. Causa e ajuste
Classifique a causa com `references/causas-e-ajustes.md` e proponha um ajuste por destino: jornada (pela `jornada-do-cliente`, se instalada), ficha, biblioteca de mensagens, aprendizado. Pergunte também: "Quer que eu veja quem mais está na mesma situação?". Se sim, aponte na carteira os clientes com a mesma falha (por exemplo, além do `maximo_sem_noticia`), pela `rotina-da-experiencia` ou pela `painel-da-carteira`, se instaladas. Cada proposta: sim, não ou depois.

### Passo 10. Aprender
Pergunte: "Alguma coisa no registro, no roteiro ou na mensagem você faria diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-experiencia.md` (`../../docs/aprender-com-o-uso.md`). Correção que contraria a ética (por exemplo, "oferece desconto para ele não ir na OAB") não vira regra: explique e proponha a versão que cabe.

## 4. O registro

O modelo completo está em `assets/registro-de-reclamacao.md`. O que não pode faltar:

| Parte | Pergunta que responde |
|---|---|
| O que o cliente disse | Com as palavras dele, qual é a queixa? |
| Desde quando | Quando apareceu pela primeira vez? É a primeira reclamação? |
| O que o escritório fez | O que foi feito no caso e com o cliente, com data? |
| O que falhou de fato | Onde o escritório não cumpriu o que a ficha, a jornada ou a própria equipe combinou? |
| O que não se sabe | O que precisa de confirmação, e quem confirma? |
| A ligação e o combinado | Quem falou, quando, o que muda e para quando? |
| Causa e ajuste | Por que aconteceu, e o que muda no método para não repetir? |

## 5. O roteiro da ligação

| Parte | Objetivo | Como |
|---|---|---|
| Abrir | Mostrar que alguém que decide está ali | "Oi, [NOME], aqui é [QUEM ASSUME]. Li sua mensagem e quis te ligar para conversar com calma. Você tem uns minutos agora?" |
| Escutar | O cliente contar tudo | Pergunta aberta ("Me conta o que aconteceu do seu lado"), sem interromper, sem corrigir datas no meio. Anotar as palavras dele |
| Reconhecer | Dizer o que falhou, sem culpar | "Você tem razão: você ficou [N] dias sem notícia, e o nosso combinado é no máximo [N]. Isso falhou do nosso lado." |
| Explicar | O cliente entender onde o caso está | O andamento traduzido e conferido pelo advogado, sem prever data nem resultado |
| Combinar | Algo concreto mudar | O que muda, quem faz, quando é o próximo contato, e o que o escritório oferece (seção 6) |
| Fechar | Confirmar o entendimento | "Então, para a gente ficar igual: [RESUMO]. Eu te mando isso por escrito hoje." |

Se o cliente falar da OAB: "É um direito seu, e eu respeito. Eu quero primeiro entender o que aconteceu e corrigir o que for nosso." Nunca: pedir que ele não vá, sugerir consequência, oferecer algo em troca.

Frases que pioram: "você não entendeu", "a secretária esqueceu", "é a Justiça que é lenta" (como desculpa), "fica tranquilo", "isso nunca acontece aqui", "vou ver o que posso fazer" (sem data).

## 6. O que o escritório pode oferecer

Vem de `o_que_o_escritorio_oferece`. A lista-base, para a pessoa escolher:
- reunião (presencial ou por vídeo) com quem conduz o caso;
- explicação por escrito do que já foi feito e do que falta, conferida pelo advogado;
- contato com data marcada até o fim da fase (por exemplo, a cada 15 dias `[A DEFINIR]`), mesmo sem novidade;
- prioridade na resposta enquanto a reclamação estiver aberta;
- mudança de quem atende no dia a dia, se o cliente pedir;
- cópia dos documentos e das peças do caso, pelo canal oficial.

Fora da lista-base: desconto, devolução ou mudança de honorários. Só o titular decide (H), só quando houve falha real do escritório, e nunca como troca para o cliente deixar de reclamar. Nesse caso, marque `[A DEFINIR]` e leve ao titular.

## 7. O caso do Jorge, resolvido

Mensagem 6 dos casos fictícios: Jorge (C-2025-0088, previdenciário, aposentadoria por idade, fase cumprimento), sexta 2026-04-10, 11h15, "vou procurar a OAB". O registro mostra 49 dias sem notícia contra um máximo de 30, um "te retorno" de 2026-02-20 que não aconteceu e duas cobranças sem resposta. A advogada liga no mesmo dia, reconhece a falha, explica a fase de cumprimento sem prometer data, combina notícia a cada 15 dias até o pagamento e manda o combinado por escrito. A causa vira ajuste na jornada da aposentadoria e um aprendizado. O caso completo, com o registro, o roteiro, a mensagem e os ajustes: `references/exemplo-jorge.md`.

## 8. Formato da saída

A pedido, nesta ordem, uma peça por vez e com o ok de cada uma:
1. **Cartão:** cliente, queixa em uma frase, quem assume, prazo da ligação, e se há algo que para tudo.
2. **Resposta-ponte**, se for o caso.
3. **Registro** (`assets/registro-de-reclamacao.md`).
4. **Roteiro da ligação** (`assets/roteiro-da-ligacao.md`).
5. **Mensagem de retorno**, depois da ligação.
6. **Linhas da carteira e do histórico** propostas.
7. **Causa e ajustes**, com a coluna de decisão.

No ciclo: o registro e o roteiro gravados como rascunho, e uma linha no resumo do dia, em "PESSOA AGORA": "[CÓDIGO] [NOME]: reclamação ([QUEIXA EM POUCAS PALAVRAS]); [QUEM ASSUME] liga até [PRAZO]; roteiro em clientes/[CÓDIGO]/ligacoes/AAAA-MM-DD.md".

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Registro da reclamação | `escritorio/07-operacao/experiencia/reclamacoes/<codigo>-AAAA-MM-DD.md` |
| Roteiro da ligação | `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md` |
| Mensagem de retorno (se usar a fila) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-retorno-de-reclamacao.md` |
| Linha do histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Carteira | `escritorio/07-operacao/experiencia/carteira.csv`: `reclamacao_aberta`, `humor`, `ultimo_contato`, `ultimo_contato_tipo`, `proximo_contato`, `motivo_proximo_contato`, `atualizado_em`, sempre com a pessoa |
| Ajustes aprovados | `04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md`, `biblioteca-de-mensagens.md`, `04-base/comum/ficha-da-experiencia.md`, `aprendizados-experiencia.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: cada peça sai no chat, pronta para copiar, com o caminho onde ficaria.

## 10. Solo e equipe

**Solo:** quem assume é sempre o titular, e a reclamação disputa a agenda com o resto. Marque a ligação como compromisso no mesmo dia. O ajuste costuma ser de rotina: um horário fixo para olhar a carteira e o "te retorno" sempre com hora.

**Equipe:** quem assume é a pessoa da ficha, não quem recebeu a mensagem. O registro fala de condutas, nunca de pessoas. Se a falha é de alguém, a conversa é em particular, fora do registro. A causa vai para a reunião da equipe junto com o painel (`painel-da-carteira`, se instalada).

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Responder a reclamação por mensagem pronta | Cliente se sente despachado e escala | Uma pessoa liga; a IA só prepara |
| Pedir desculpa genérica sem dizer o que falhou | Soa como fórmula; nada muda | "Reconhecer" com a falha concreta e a régua |
| Culpar o cliente ou a equipe | Briga, equipe esconde o próximo erro | Regra fixa 2; registro de condutas |
| Desconto para encerrar o assunto | Precedente ruim e risco ético | Lista do que oferecer sem desconto; exceção só com o titular |
| Tentar impedir a ida à OAB | Falta ética e piora a reclamação | Frase pronta que respeita o direito do cliente |
| Combinar sem data | O cliente cobra de novo em uma semana | Mensagem de retorno com o próximo contato marcado |
| Fechar porque o cliente sumiu | A insatisfação volta no encerramento ou na pesquisa | Fecha só com o combinado cumprido e a pessoa confirmando |
| Corrigir só este cliente | O mesmo erro com os outros | Passo 9: causa, ajuste e a busca na carteira |

## 12. Próximo passo

- Explicar o andamento na ligação: `status-para-o-cliente` (se instalada). Sem ela, o advogado explica a partir da movimentação.
- Ajustar a régua do tipo de caso: `jornada-do-cliente` (se instalada). Sem ela, anote o ajuste na jornada à mão.
- Ver quem mais está sem notícia: `rotina-da-experiencia` ou `painel-da-carteira` (se instaladas).
- Cliente que decidiu encerrar o contrato: `encerramento-do-caso` (se instalada), para prestação de contas e documentos.
- Ver, no mês seguinte, se o ajuste pegou: `auditar-conversas` (se instalada).

## Referências desta habilidade

- `assets/registro-de-reclamacao.md`: o modelo do registro. Use no passo 4.
- `assets/roteiro-da-ligacao.md`: o roteiro com as frases de cada parte e o que evitar. Use no passo 5.
- `references/causas-e-ajustes.md`: as causas mais comuns e o ajuste de cada uma. Leia no passo 9.
- `references/exemplo-jorge.md`: o caso fictício resolvido do começo ao fim. Leia no modo treino ou quando quiser ver o resultado esperado.
