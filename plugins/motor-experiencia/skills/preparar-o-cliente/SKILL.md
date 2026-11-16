---
name: preparar-o-cliente
description: >
  Prepara o cliente para audiência, perícia e reunião: lembretes nos prazos da ficha, o que
  levar, como vai ser, quanto tempo costuma durar (conferido pelo advogado), o que dizer e o
  que evitar de forma ética (sempre a verdade, nunca esconder fato), acolhimento para quem está
  com medo e o roteiro da ligação de preparação para o advogado. Tem roteiros-base por tipo de
  compromisso, para o escritório adaptar. Use quando o advogado disser "a audiência do Paulo é
  amanhã", "prepara a Marta para a perícia", "o que ela leva?", "manda o lembrete da perícia",
  "ela está com medo de ir", "monta a ligação de preparação", "como funciona a audiência por
  vídeo?". Não use para preparar testemunha (é conversa do advogado) nem para contar como foi o
  compromisso depois (use status-para-o-cliente).
---

# Preparar o cliente

> O cliente que sabe onde vai, o que levar, quem vai estar na sala e que só precisa dizer a verdade chega no horário e com menos medo. A habilidade prepara o material; o advogado confere e, quando precisa, liga.

Regras comuns: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Carteira: `../../docs/carteira.md`. Onde gravar: `../../docs/pasta.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Sexta, 15h40, a Marta escreve: "Na perícia eu levo o quê? Tenho medo de ir sozinha." A perícia é terça, 2026-04-14. Uma resposta com a lista seca resolve metade. A outra metade é o medo: ela precisa ouvir que é normal, saber como a perícia funciona do começo ao fim, e alguém perguntar se tem quem possa ir com ela.

**Regras fixas desta habilidade:**
1. Nunca orientar a mentir, a exagerar, a esconder fato ou a "decorar" resposta. A orientação é dizer a verdade, com as próprias palavras, e dizer quando não sabe ou não lembra.
2. Testemunha não é preparada por esta habilidade. O máximo é o aviso de data e local; a conversa com testemunha é do advogado, dentro do que a ética permite `[CONFERIR]`.
3. Duração, horário de chegada, regras do local, quem pode entrar na sala e o que o órgão exige ficam `[CONFERIR]` no cabeçalho interno até o advogado confirmar. Nenhum prazo ou horário entra na mensagem se não veio da ficha, da intimação ou do advogado: o horário de chegada que a advogada vai confirmar na hora fica `{HORÁRIO DE CHEGADA}`, para quem envia preencher, ou a frase sai.
4. Toda orientação de audiência e perícia é A: o advogado lê antes de sair. Lembrete que só repete o que a orientação aprovada já disse pode ser S.
5. Compromisso hoje ou amanhã sem preparação feita é pessoa agora: o advogado liga.

## 1. Quando usar

**Use quando:**
- Foi marcada audiência, perícia (médica, social, técnica) ou reunião com o cliente.
- Chegou a data de um lembrete (`lembrete_de_compromisso`).
- O cliente pergunta o que levar, como vai ser, ou diz que está com medo.
- O advogado vai ligar para preparar o cliente e quer o roteiro.
- O `agente-de-suporte` ou a `triar-mensagem-do-cliente` (se instalada) apontou compromisso nos próximos dias.

**Não use quando:**
- O compromisso já aconteceu e é preciso contar como foi: `status-para-o-cliente` (se instalada). Resultado ruim: ligação do advogado antes de qualquer mensagem.
- O pedido é pedir redesignação ou remarcação de ato do processo: decisão do advogado.
- É consulta de quem ainda não é cliente: `agenda-da-consulta` do motor-comercial (se instalado).

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` e `aprendizados-experiencia.md`, se existirem.
2. Sem fichas: ofereça `/motor-experiencia:comecar`. Para seguir agora, pergunte só "Quantos dias antes vocês lembram o cliente de audiência e perícia?" e, depois, "Quantos dias antes vocês preparam o cliente, por ligação ou mensagem?".
3. Leia a carteira (`proximo_compromisso`, `data_compromisso`, `humor`, `pediu_para_nao_receber`) e o `clientes/<codigo>/historico.md`: já houve orientação? O cliente confirmou presença?
4. Leia o roteiro do escritório para o tipo de compromisso, se existir (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chaves `orientacao-<tipo>` e `lembrete-compromisso`). Sem ele, use os roteiros-base de `references/`.
5. Dados: o tipo de perícia pode revelar dado de saúde. Use só o que a orientação precisa ("perícia médica"), nunca o diagnóstico. Laudo completo não entra sem autorização expressa do advogado.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `lembrete_de_compromisso`.
- **Melhora:** X: `preparacao`, `cadencia_da_preparacao` · E: `nicho`.
- Lê também, se preenchidos: E: `tratamento`, `canais`, `assinatura_das_mensagens`, `o_que_e_urgente`, `urgencia_vai_para`; X: `quem_le_antes_de_enviar`.

`lembrete_de_compromisso` vazio: pergunte uma vez; sem resposta, use o exemplo da ficha (7 dias e 1 dia antes) marcado `[A DEFINIR]` no cabeçalho interno. `cadencia_da_preparacao` vazia: pergunte uma vez ("Quantos dias antes de audiência e de perícia vocês preparam o cliente?"); sem resposta, a orientação sai no primeiro lembrete e a cadência fica `[A DEFINIR]` no cabeçalho interno.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | Saída |
|---|---|---|---|
| Preparar | Compromisso marcado ou pergunta do cliente | Orientação completa, lembretes e, se preciso, roteiro de ligação | No chat, para aprovar |
| Lembrete | Data da régua de lembrete | Lembrete curto que repete a orientação aprovada | No chat ou na fila |
| Ligação | O advogado vai ligar | Roteiro da ligação de preparação | `clientes/<codigo>/ligacoes/AAAA-MM-DD.md` |
| No ciclo | O `agente-de-suporte` | Lembretes e orientações que vencem, na fila; véspera sem preparação vira PESSOA AGORA | Fila e lista para o agente |
| Adaptar | `adaptar-experiencia` | Reescreve os roteiros-base para o nicho | `biblioteca-de-mensagens.md`, chaves `orientacao-<tipo>` |

**Modo direto:** "a perícia da Marta é terça, 14/04, prepara". Execute e pergunte só o que falta (o horário e o local vêm da intimação ou do advogado).

### Passo 1. Os dados do compromisso
Pergunte o que faltar, uma pergunta por vez: tipo (audiência de quê, perícia de quê, reunião), data e hora, local ou link, se é presencial ou por vídeo, se o cliente precisa levar alguém (testemunha é do advogado). Data e local vêm da intimação ou do advogado, nunca de suposição.

### Passo 2. Quanto tempo falta
A cadência vem da ficha: `cadencia_da_preparacao` diz quantos dias antes de cada tipo de compromisso acontece a preparação (ligação ou mensagem, conforme `preparacao`), e `lembrete_de_compromisso` diz quando saem os lembretes. Com o exemplo da ficha (audiência 5 dias, perícia 3 dias; lembrete 7 dias e 1 dia antes):
- **Hoje ou amanhã (ou o próximo dia útil), sem orientação registrada no histórico:** pessoa agora. Diga ao advogado em uma frase e prepare o material do passo 4 para ele ler e mandar ainda hoje.
- **Dentro da cadência do tipo** (a data da preparação já chegou ou passou): orientação completa agora e lembrete na véspera.
- **Antes da cadência:** aviso de data (se o cliente ainda não sabe) e a orientação na data que a cadência marca. Na carteira, `proximo_contato` = essa data, `motivo_proximo_contato = compromisso`.
- **Pergunta ou medo do cliente antes da cadência:** a orientação sai agora, mesmo assim. A cadência é o mínimo, não um limite.

### Passo 3. Ler a pessoa
Procure medo, ansiedade, confusão ou dificuldade prática (transporte, trabalho, criança pequena, dificuldade com celular). Achou medo: a orientação começa pelo acolhimento (seção 5). Achou dificuldade prática: pergunte como ajudar e anote para o advogado. Sinal de risco ou de vulnerabilidade nova: pare e leve ao advogado (seção 5 de `regras.md`).

### Passo 4. Montar a orientação
Use o roteiro-base do tipo (`references/`) e preencha as seis partes:
1. **O que é**, em uma frase.
2. **Onde e quando**, com o horário de chegada que o advogado confirmar. Sem a confirmação, `{HORÁRIO DE CHEGADA}` no texto, para quem envia preencher, e `[CONFERIR]` no cabeçalho interno.
3. **O que levar**, em lista curta.
4. **Como vai ser**, na ordem em que acontece, e quem vai estar lá.
5. **Quanto tempo costuma durar**, só com o número que o advogado confirmar; até lá, `[CONFERIR]` no cabeçalho interno e "o tempo varia" na mensagem.
6. **O que dizer e o que evitar** (seção 4), em linguagem simples.

Feche com quem acompanha o cliente (o advogado vai? encontra onde?), o pedido de confirmação de presença e o que acontece depois ("depois a gente te conta o próximo passo").

### Passo 5. Lembretes
Pelos dias de `lembrete_de_compromisso`. O lembrete repete data, hora, local, o que levar e o pedido de confirmação. Quem não confirmou até a véspera recebe ligação de uma pessoa (H), não mais mensagem.

### Passo 6. Ligação de preparação
Se a ficha diz que há ligação (`preparacao`), se é a primeira audiência ou perícia do cliente, se ele está com medo, ou se o advogado pedir: preencha `references/ligacao-de-preparacao.md` e entregue ao advogado. A ligação é H, no dia que `cadencia_da_preparacao` marca para o tipo de compromisso. Depois da ligação: uma linha de contato no histórico, com canal `ligacao` e a palavra "preparação" no texto (`| 2026-04-10 14h00 | ligacao | advogada | ligação de preparação da perícia de 2026-04-14 |`), e `ultimo_contato` e `ultimo_contato_tipo = ligacao` na carteira (a preparação informa o caso). Se o cliente estava em PESSOA AGORA (compromisso até o próximo dia útil), é essa linha que o tira de lá: o `carteira.py` da `rotina-da-experiencia` passa a mostrar o compromisso só em "compromissos dos próximos 7 dias". A orientação só por mensagem não basta para o script; quem mandou diz na fila que falou com o cliente.

### Passo 7. Mostrar, conferir e registrar
- Mostre a orientação com o cabeçalho "Antes de enviar" (o que está `[CONFERIR]` ou `[A DEFINIR]`), quem lê (`quem_le_antes_de_enviar`) e a sigla A. A mensagem só sai sem marcações.
- Com o ok, grave: a orientação a pedido em `escritorio/07-operacao/experiencia/clientes/<codigo>/preparacao-<tipo>-AAAA-MM-DD.md` (o tipo do compromisso e a data dele, por exemplo `preparacao-pericia-2026-04-14.md`), com o "Antes de enviar" separado do texto, e os lembretes do mesmo compromisso no fim desse arquivo; linha no `historico.md`; roteiro de ligação em `ligacoes/AAAA-MM-DD.md`; na carteira, proponha `proximo_compromisso`, `data_compromisso` (se ainda vazios), `proximo_contato` (o próximo lembrete), `motivo_proximo_contato = compromisso` e `atualizado_em`.

### Passo 8. Aprender
Pergunte: "Alguma coisa na orientação você mudaria para os próximos?". Cada correção vira uma regra curta ("Perícia no fórum de [CIDADE]: chegar 40 minutos antes, a fila da portaria é longa") e entra nos aprendizados com o ok. Duração e regra de local confirmadas pelo advogado: ofereça gravar no roteiro do escritório (`orientacao-<tipo>`), para não perguntar de novo.

### No ciclo (o agente chama)
1. Leia na carteira os compromissos dos próximos 7 dias (ou o maior número de dias da `cadencia_da_preparacao`) e, no histórico, o que já foi enviado.
2. Véspera ou dia, sem orientação registrada: PESSOA AGORA para o agente, com uma frase.
3. Data da cadência de preparação sem orientação enviada: rascunho da orientação na fila (`tipo: orientacao-de-compromisso`), ou item para quem liga, se `preparacao` diz ligação. Data de lembrete: rascunho do lembrete na fila (`escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-lembrete-de-compromisso.md`), só se a orientação já foi aprovada antes. Sem orientação aprovada: rascunho da orientação, com `tipo: orientacao-de-compromisso`, para o advogado ler.
4. `pediu_para_nao_receber = sim`: o lembrete do compromisso continua, porque é do caso, mas no jeito que o cliente pediu (ligação vira item para a pessoa). Humor `insatisfeito` ou reclamação aberta: uma pessoa fala primeiro.
5. Atualize na carteira só `proximo_contato`, `motivo_proximo_contato` e `atualizado_em`. Não envie nada.

## 4. O que dizer e o que evitar (para o cliente)

| Dizer ou fazer | Evitar |
|---|---|
| Contar a verdade, com as suas palavras | Inventar, aumentar ou diminuir o que aconteceu ou o que você sente |
| Responder o que foi perguntado, com calma | Decorar respostas ou ler um texto pronto |
| Dizer "não sei" ou "não lembro" quando for assim | Chutar uma data ou um número |
| Pedir para repetir a pergunta se não entendeu | Discutir com a outra parte, com o perito ou com o juiz |
| Falar do seu dia a dia como ele é, inclusive o que você consegue fazer (perícia) | Falar do caso no corredor, com a outra parte ou com o advogado dela |
| Levar os documentos da lista | Assinar qualquer papel sem o advogado ver |
| Avisar o escritório se não puder ir, antes da data | Faltar sem avisar |
| Desligar o celular durante o ato | Gravar ou postar sobre o compromisso nas redes |

O que nunca sai desta habilidade: sugestão de sintoma para a perícia, versão combinada de fato, orientação para omitir documento, conversa de preparação com testemunha.

## 5. Acolhimento (quem está com medo)

1. **Reconhecer:** "É normal ficar nervosa antes de uma perícia. Quase todo mundo fica."
2. **Explicar o concreto:** o medo diminui quando a pessoa sabe a ordem das coisas. Vá ao "como vai ser" do roteiro.
3. **Tirar o peso da performance:** "Você não precisa saber falar bonito. É só contar como é a sua vida hoje."
4. **Perguntar pela companhia:** "Tem alguém que possa ir com você?". Se pode entrar na sala é regra do local ou de quem conduz `[CONFERIR]`; acompanhar até o local, sempre pode.
5. **Oferecer a ligação:** "A advogada pode te ligar antes para conversar com calma."
6. **Nunca:** "fique tranquila", "não vai dar nada", "é só uma formalidade", promessa de resultado.

## 6. Exemplos resolvidos (Escritório Modelo)

**Marta (C-2026-0001), mensagem 9 de `../../docs/casos-ficticios.md`: perícia médica judicial na terça, 2026-04-14; medo de ir sozinha.** Hoje é sexta, 2026-04-10: faltam 4 dias. Pela cadência de exemplo (perícia 3 dias antes), a preparação cairia no sábado, 2026-04-11, fora do expediente, e por isso sairia hoje, o último dia útil antes; e ela perguntou e está com medo. A orientação sai agora: alta, lembrete na véspera. Ela também está há 36 dias sem notícia (mensagem 1): a advogada liga hoje e a preparação vai junto.

Antes de enviar (interno): horário da perícia e horário de chegada `[CONFERIR]` com a advogada, na intimação (ela preenche `{HORÁRIO DE CHEGADA}` antes de enviar); duração `[CONFERIR]`; se acompanhante entra na sala `[CONFERIR]`.

Rascunho (A, a advogada lê):
```
Marta, é normal ter medo antes da perícia, quase todo mundo fica. Vou te explicar como funciona, e a advogada te liga hoje para conversar com calma.

A perícia é uma conversa com um médico indicado pelo juiz. Ele não é do INSS nem do escritório. Ele vai perguntar como você está e como é o seu dia a dia, e pode fazer um exame simples.

O que levar:
1. Documento com foto.
2. Os documentos médicos que você tem (exames, laudos e receitas), em ordem de data.

A perícia é na terça, 14/04. Chegue às {HORÁRIO DE CHEGADA}. A espera pode demorar, então vale levar água e um lanche.

Na conversa, é só contar a verdade com as suas palavras, como a sua vida é hoje. Se não lembrar de alguma coisa, pode dizer que não lembra.

Tem alguém que possa ir com você? Me conta quem, que a gente vê junto como fica.

Me confirma que vai conseguir ir na terça?
```

**Paulo (C-2026-0002), mensagem 2: audiência trabalhista na segunda, 2026-04-13, às 9h (o próximo dia útil); "não sei o que levar!!!".** Pessoa agora (compromisso no próximo dia útil, sem preparação registrada). A advogada recebe o material do `references/roteiro-audiencia.md` (audiência trabalhista), preenchido com: documento com foto, carteira de trabalho, os documentos que ela indicar; chegar com antecedência; como vai ser (tentativa de acordo e, se não houver, os depoimentos `[CONFERIR]` o tipo de audiência na intimação); o que dizer e evitar (seção 4); onde ela encontra o Paulo. Ela lê, ajusta e manda ainda de manhã, e decide se liga. O horário de chegada fica `{HORÁRIO DE CHEGADA}` até ela confirmar. A orientação fica em `clientes/C-2026-0002/preparacao-audiencia-2026-04-13.md`. Quando ela ligar, a linha `ligacao` com "ligação de preparação da audiência de 2026-04-13" no histórico tira o Paulo de PESSOA AGORA; se ela só mandar a mensagem, diz na fila que falou com ele.

## 7. Formato da saída

```
PREPARAÇÃO · [CÓDIGO] · [tipo] · [AAAA-MM-DD HHhMM] · faltam [N] dias
Urgência: pessoa agora | alta | normal
Antes de enviar (interno): [o que está CONFERIR ou A DEFINIR]
Orientação (A, [quem lê]): "[mensagem]"
Preparação: [data, pela cadencia_da_preparacao] · Lembretes: [datas, pela ficha]
Ligação de preparação: sim ([motivo]) | não
Registro: [linha do histórico] · [proposta na carteira]
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Orientação e lembretes (a pedido) | No chat e em `escritorio/07-operacao/experiencia/clientes/<codigo>/preparacao-<tipo>-AAAA-MM-DD.md` (data do compromisso; por exemplo `preparacao-pericia-2026-04-14.md`) |
| Orientação e lembretes (no ciclo) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-<tipo>.md` |
| Roteiro da ligação | `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md` |
| Histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Carteira | `proximo_contato`, `motivo_proximo_contato`, `atualizado_em`; `proximo_compromisso` e `data_compromisso` só com o ok |
| Roteiros adaptados e aprovados | `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chaves `orientacao-<tipo>` e `lembrete-compromisso`, cada mudança `[ALTERADO]` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: tudo no chat, com o caminho de cada arquivo.

## 9. Solo e equipe

**Solo:** o titular aprova a orientação uma vez por tipo de compromisso e local; depois, os lembretes saem do modelo aprovado. A ligação de preparação fica para a primeira audiência ou perícia do cliente e para quem está com medo.

**Equipe:** a secretária monta a orientação e os lembretes e liga para quem não confirmou presença; o advogado aprova a orientação e faz a ligação de preparação. Quem vai ao ato com o cliente fica escrito na orientação.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Cliente chega sem documento | Ato prejudicado ou adiado | Lista curta do que levar e lembrete |
| Orientar o que falar ao perito | Problema ético e risco ao caso | Regra fixa 1 e seção 4 |
| Duração ou regra de local de cabeça | Cliente perde o horário ou é barrado | `[CONFERIR]` até o advogado confirmar |
| Medo tratado com "fique tranquila" | O medo fica, a confiança cai | Acolhimento da seção 5 |
| Audiência amanhã sem ninguém ver | Cliente sozinho e despreparado | Pessoa agora na véspera |
| Lembrete só por mensagem para quem não confirmou | Falta no ato | Ligação de uma pessoa |
| Testemunha preparada pela IA | Risco ético | Regra fixa 2 |

## 11. Próximo passo

- Depois do compromisso: `status-para-o-cliente` (se instalada) conta como foi; resultado ruim é ligação. Sem ela, o advogado manda a mensagem de depois a partir da anotação dele.
- Documento que faltou para o ato: `checklist-de-documentos` (se instalada).
- Compromisso na página do caso: `pagina-do-caso` (se instalada) em "próximos passos".
- Lembretes todo dia sem ninguém pedir: `rotina-da-experiencia` (se instalada) e `/motor-experiencia:ciclo`.

## Referências desta habilidade

- `references/roteiro-audiencia.md`: audiência trabalhista, de família (conciliação e mediação), de juizado e por vídeo. Passo 4.
- `references/roteiro-pericia.md`: perícia médica (judicial e do INSS), avaliação social e perícia técnica no local de trabalho. Passo 4.
- `references/roteiro-reuniao.md`: reunião com o escritório, presencial e por vídeo, e assinatura de documentos. Passo 4.
- `references/ligacao-de-preparacao.md`: o roteiro da ligação do advogado, com perguntas difíceis e o que não dizer. Passo 6.
