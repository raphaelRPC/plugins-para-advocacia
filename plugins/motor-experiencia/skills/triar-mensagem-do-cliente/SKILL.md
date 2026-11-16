---
name: triar-mensagem-do-cliente
description: >
  Faz a triagem das mensagens de quem já é cliente (WhatsApp, e-mail, ligação anotada): separa
  primeiro o que é para uma pessoa agora (notícia ruim pendente, reclamação, aflição,
  vulnerabilidade, dado de saúde, compromisso amanhã, senha ou golpe), classifica o resto
  (andamento, documento, compromisso, financeiro, cliente com IA, pedido de acesso,
  preferência, agradecimento), diz o caminho, quem cuida e o prazo da ficha, sugere a
  resposta-ponte no tom do escritório e registra no histórico do cliente e no lote do dia,
  uma mensagem ou o lote. Use quando o advogado disser "tria as mensagens dos
  clientes", "o que eu respondo primeiro?", "chegou isso da Marta", "quem precisa de mim
  agora?", "separa o que é urgente dos clientes". Não use para quem ainda não é cliente (use
  triar-contato do motor-comercial, se instalado) nem para traduzir a movimentação (use
  status-para-o-cliente).
---

# Triar a mensagem do cliente

> Toda mensagem de cliente passa pelo mesmo caminho: separar o que pede uma pessoa agora, classificar o resto, dar a cada uma um dono e um prazo, responder com uma ponte honesta e deixar registrado.

Regras comuns: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Carteira e histórico: `../../docs/carteira.md`. Onde gravar: `../../docs/pasta.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

Sexta, 8h. Doze mensagens de clientes desde a noite. No meio delas: a sentença que saiu ontem e a cliente ainda não sabe, o cliente que diz que vai procurar a OAB, a audiência de segunda às 9h sem preparação e uma filha contando que a mãe foi internada. Quem responde na ordem de chegada manda "alguma novidade?" com o resultado antes de a advogada ligar.

**Regras fixas desta habilidade:**
1. Pessoa agora vem antes de tudo e não ganha mensagem pronta com conteúdo: notícia ruim, reclamação, desespero ou crise, vulnerabilidade e dado de saúde vão para uma pessoa, que liga. A única mensagem possível antes da ligação é a ponte curta sem conteúdo da seção 5, e só se a ficha permitir. Sinal de violência ou risco à vida: para tudo e segue a seção 5 de `regras.md`.
2. A resposta-ponte só promete o que o escritório cumpre: quem vai responder e até quando. Nunca resultado, data de decisão, valor ou explicação de decisão.
3. Senha, código de acesso e login (gov.br, Meu INSS, banco, sistema do tribunal) nunca se pedem, nunca se recebem por mensagem e nunca se enviam.
4. Dado de saúde e de vulnerabilidade não entra no registro: no histórico vai só "intercorrência de saúde" ou "situação pessoal delicada".
5. Na dúvida entre duas urgências, vale a mais alta. Na dúvida entre IA e pessoa, vale a pessoa.

## 1. Quando usar

**Use quando:**
- Chegaram mensagens de clientes ativos e é preciso saber o que fazer com cada uma.
- É o começo do dia, a volta do almoço ou o fim do expediente, e há um lote para separar.
- O `agente-de-suporte` chamou no ciclo do dia (modo "no ciclo").
- A `triar-contato` do motor-comercial (se instalado) mandou para cá uma mensagem de cliente ativo.

**Não use quando:**
- Quem escreveu não está na carteira e não fala de um caso do escritório: é contato novo, vai para a `triar-contato` do motor-comercial (se instalado; sem ele, para quem faz o primeiro atendimento).
- O pedido é traduzir a movimentação para o cliente: `status-para-o-cliente` (se instalada). A triagem só aponta o caminho.
- O pedido é tratar a reclamação inteira: `reclamacao-e-recuperacao` (se instalada). A triagem só separa e avisa.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` e `aprendizados-experiencia.md`, se existirem. Aprendizado de triagem vale antes das tabelas desta habilidade.
2. Sem fichas: ofereça `/motor-experiencia:comecar`. Para seguir agora, pergunte só "O que é urgente com um cliente para vocês?" e "Quem cuida de cada coisa e em quanto tempo o cliente recebe a primeira resposta?". Ofereça gravar no fim.
3. Leia a carteira (`escritorio/07-operacao/experiencia/carteira.csv`): fase, último contato, compromisso, humor, reclamação aberta, `pediu_para_nao_receber`. E o `clientes/<codigo>/historico.md` de quem escreveu: o que já foi dito, o que foi prometido.
4. Leia a biblioteca (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`), se existir: as pontes saem das chaves `recebi-retorno-ate`, `ponte-<tipo>` e `cortesia`. Sem biblioteca, rascunhe e marque "rascunho, ainda não está na biblioteca".
5. Conta e dados: mensagem real só em conta profissional ou de equipe. Troque o que a tarefa não precisa (CPF por `[DOC]`, processo por `[PROCESSO]`, endereço por `[ENDEREÇO]`) e avise em uma linha. Em conta pessoal, só os casos fictícios, gravando em `escritorio/07-operacao/_treino/experiencia/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `o_que_e_urgente`, `palavras_de_alerta` · X: `quem_cuida_dos_casos`, `primeira_resposta_cliente_ativo`.
- **Melhora:** X: `resposta_ponte`, `nunca_por_mensagem`.
- Lê também, se preenchidos: E: `horario_de_atendimento` (para contar horas úteis), `urgencia_vai_para`, `tratamento`, `tom_em_tres_palavras`, `assinatura_das_mensagens`; X: `resposta_completa`, `quem_le_antes_de_enviar`, `maximo_sem_noticia`, `quem_assume_reclamacao`, `prazo_de_retorno_da_reclamacao`.

Campo vazio que a mensagem pede: pergunte só aquele, uma vez. Sem resposta, siga com `[A PREENCHER]` no cabeçalho interno do lote, nunca na ponte.

## 3. Fluxo

### Modos

| Modo | Quem chama | Entrada | Saída |
|---|---|---|---|
| Uma mensagem | O advogado ou a equipe | A mensagem colada (ou a transcrição do áudio) | O cartão da seção 6, no chat |
| Lote | Começo do dia, rotina | Várias mensagens, com hora | A tabela do lote, pessoa agora no topo |
| No ciclo | O `agente-de-suporte` | Arquivos de `07-operacao/experiencia/entrada/` desde a última rodada | Lote gravado, pontes na fila, PESSOA AGORA devolvida ao agente; nada mostrado |
| Adaptar | `adaptar-experiencia` | Ficha, nicho e mensagens reais anonimizadas | Sinais e pontes reescritos para o nicho |

**Modo direto:** "tria isso: [mensagem]". Execute, mostre o cartão e pergunte só o que falta.

### Passo 1. Receber e conferir quem é
- Áudio: peça a transcrição ou o resumo de quem ouviu. A triagem não adivinha o que não leu.
- Ache o cliente na carteira pelo nome curto ou pelo código. Não está: é contato novo (seção 1, "Não use"). Está com dois casos: pergunte de qual caso fala, se a mensagem não deixar claro.
- Mais de uma mensagem do mesmo cliente no lote: triagem de cada uma, mas um retorno só, com o prazo da mais urgente.

### Passo 2. Pessoa agora
Leia procurando os sinais da seção 4.1, na mensagem e no que a carteira e o histórico dizem. Achou um:
- marque `pessoa agora`, urgência alta, e diga em uma frase o que apareceu e quem precisa agir (`urgencia_vai_para`, `quem_assume_reclamacao`);
- não escreva ponte com conteúdo. **A resposta-ponte de quem está em pessoa agora** é, no máximo, uma mensagem curta sem conteúdo do caso, a `ponte-pessoa-agora` da seção 5 ("Recebi sua mensagem. A advogada vai te ligar {QUANDO}."), e só se a ficha permitir: `resposta_ponte` preenchida e nenhum aprendizado dizendo o contrário. Ela não explica, não adianta resultado, não pede desculpa pelo que ainda não foi conversado e não promete o que a ligação vai dizer. Quem vai ligar decide se ela sai e preenche o `{QUANDO}`. Nunca há ponte em violência, ameaça, risco à vida, senha ou golpe: só a ligação. No ciclo, nenhuma ponte para pessoa agora;
- indique o material que ajuda a pessoa (roteiro de ligação, preparação, histórico resumido) e a habilidade que faz;
- violência, ameaça ou risco à vida: pare, diga ao advogado agora e lembre os números de emergência de `regras.md` (190, 180, 188, 192 `[CONFERIR]` na região).

### Passo 3. Classificar
| Campo | Como decidir |
|---|---|
| Tipo | Um da seção 4.2. Dois pedidos: o principal e o outro entre parênteses |
| Assunto | Até 8 palavras, sem dado sensível |
| Urgência | Pela árvore da seção 4.3 |
| Sinal | O que pesou: palavra de alerta, data, dias sem notícia, humor |

### Passo 4. Caminho, quem cuida e prazo
- Caminho e próxima habilidade: tabela da seção 4.4.
- Quem cuida: `quem_cuida_dos_casos` (por área ou função). Conteúdo jurídico ou do processo: quem a ficha diz que lê (`quem_le_antes_de_enviar`).
- Prazo: seção 4.5. Escreva o horário exato ("até 13h10"), não "4 horas úteis".

### Passo 5. Resposta-ponte
Só para quem não está em pessoa agora. Parta de `resposta_ponte` da ficha ou da biblioteca. Três partes, uma por parágrafo: recebi (com o nome), o que vai acontecer (quem responde ou o que foi combinado), até quando. Nunca comece elogiando a pergunta ("Boa pergunta"): comece pelo recebimento. Pedido simples que a ponte já resolve (documento remarcado, preferência, agradecimento) ganha a resposta completa. Tratamento, tom e assinatura da ficha. Sigla A: alguém lê antes de enviar. Mensagem automática diz que é automática.

### Passo 6. Registrar
- **Histórico** (`clientes/<codigo>/historico.md`): uma linha por mensagem recebida, no formato da seção 6.3. A mensagem do cliente não muda o `ultimo_contato` da carteira: ele conta quando o escritório informa algo, e é atualizado depois do envio (comando `/motor-experiencia:fila`).
- **Carteira:** proponha `proximo_contato`, `motivo_proximo_contato` (`retorno-combinado`, `documento`, `compromisso`) e `atualizado_em`. Proponha à pessoa, sem gravar sozinho: `humor`, `reclamacao_aberta`, `pediu_para_nao_receber`. Falha da régua (último contato além do `maximo_sem_noticia`): aponte no lote.
- **Documento** (mensagem que manda, promete ou remarca documento, como a 3 dos casos fictícios): o documento ganha controle e lembrete. Com a `checklist-de-documentos` (se instalada), no modo dar baixa: em `clientes/<codigo>/documentos.md`, a situação do documento e a data combinada em "Combinado até" (ou "chegou em", se veio); na carteira, `documentos_pendentes` recontado, `proximo_contato` = a data combinada e `motivo_proximo_contato = documento`. No dia combinado, o ciclo (pelo script da `checklist-de-documentos`) põe o lembrete gentil na fila; se o documento chegar antes, a baixa no controle cancela o lembrete. Sem a `checklist-de-documentos`: a mesma data em `proximo_contato` com `motivo_proximo_contato = documento` e uma linha no histórico com o combinado ("certidão combinada para 2026-04-13"); no dia, quem cuida manda o lembrete pelo modelo de pedido de documento da biblioteca.
- **Lote do dia:** `escritorio/07-operacao/experiencia/mensagens/AAAA-MM-DD.md` (seção 6.2). Lotes seguintes entram no mesmo arquivo, com a hora.
- Mostre as linhas e grave com o ok. No lote, mostre tudo junto e grave de uma vez.

### Passo 7. Aprender
Pergunte: "Alguma classificação ou ponte você faria diferente?". Cada correção vira uma regra curta ("Cliente que cita a OAB vai para a titular, mesmo sem humor insatisfeito") e, com o ok, entra nos aprendizados. Palavra de alerta nova: ofereça gravar em `palavras_de_alerta` na ficha. Ponte aprovada que não existia: ofereça guardar na biblioteca. Tipo que se repete sem caminho: aponte, é um fluxo que o escritório ainda não escreveu.

### No ciclo (o agente chama)
1. Leia os arquivos novos de `escritorio/07-operacao/experiencia/entrada/` desde a data da última rodada no registro de uso, inclusive os de fim de semana.
2. Rode os passos 1 a 4 para cada mensagem.
3. Pessoa agora: devolva ao agente a lista para o topo do resumo, uma frase por item. Nada na fila, nem a `ponte-pessoa-agora`: quem vai ligar decide se ela sai.
4. Pontes: um arquivo por cliente em `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-resposta-ponte.md`, no formato de `agentes-e-fila.md`, com `prazo` da seção 4.5 e `motivo: triagem HHhMM, <tipo>`.
5. Grave o lote do dia e as linhas do histórico (registro, sigla S). Mensagem de documento: o controle e a data combinada pela `checklist-de-documentos` (se instalada), como no passo 6. Na carteira, só `proximo_contato`, `motivo_proximo_contato`, `documentos_pendentes` e `atualizado_em`; `humor`, `reclamacao_aberta` e `pediu_para_nao_receber` vão para "PARA DECIDIR": a triagem propõe, uma pessoa confirma e grava.
6. Não envie nada e não mostre nada no chat.

### Depois que a pessoa falou (saída de PESSOA AGORA)
O item fica no topo do resumo do dia até alguém dizer que falou com o cliente. Quando a pessoa contar, ou quando o comando `/motor-experiencia:fila` perguntar "Já falou? O que ficou combinado?", grave, com o ok:
1. **Histórico:** uma linha de contato com o combinado, sem o conteúdo da conversa (`| 2026-04-10 15h40 | ligacao | advogada | ligação sobre a reclamação; combinou relato por escrito até 2026-04-13 |`).
2. **Carteira:** `ultimo_contato` = a data e `ultimo_contato_tipo = ligacao`, se a conversa informou algo do caso (uma ligação só para marcar outra não conta); `proximo_contato` = a data combinada e `motivo_proximo_contato = retorno-combinado`; `atualizado_em`. `humor` e `reclamacao_aberta` pela pessoa que falou.
3. **Lote do dia:** no `mensagens/AAAA-MM-DD.md`, o item ganha "resolvido HHhMM: [o combinado em uma frase]".
Sem essa resposta, o item continua em PESSOA AGORA no resumo seguinte.

### Modo adaptar
Leia `nicho.md` e as mensagens reais anonimizadas que o advogado separar. Reescreva os sinais de `references/sinais-do-cliente-ativo.md` com as palavras desse cliente e as pontes da seção 5 no tom da ficha. Mostre cada mudança marcada `[ALTERADO]`. Com o ok: sinais vão para `palavras_de_alerta` na ficha do escritório (com linha no histórico da ficha) e pontes para a biblioteca, chaves `ponte-<tipo>`.

## 4. Critérios

### 4.1 Pessoa agora

| Sinal | Exemplos do jeito que chega | O que a pessoa faz |
|---|---|---|
| Violência, ameaça, risco à vida, criança em risco | "ele disse que vai me matar", "não aguento mais viver" | Advogado agora; emergência se houver risco imediato |
| Notícia ruim pendente | Cliente pergunta e a carteira mostra decisão ou movimentação desfavorável ainda não conversada (fase `decisao` sem ligação no histórico depois dela) | Advogado liga; roteiro pela `status-para-o-cliente` |
| Reclamação | "terceira vez que pergunto", "vou procurar a OAB", "vou trocar de advogado", `reclamacao_aberta = sim`, humor `insatisfeito` com queixa nova | Quem a ficha manda liga no prazo da reclamação; `reclamacao-e-recuperacao` |
| Desespero ou crise | desespero, choro, crise, "não sei mais o que fazer", fala em desistir de tudo | Advogado liga |
| Vulnerabilidade nova ou dado de saúde | internação, doença grave, morte na família, perda do emprego, violência em casa | Advogado liga; registro só "intercorrência" |
| Compromisso hoje ou amanhã | audiência, perícia, prazo do cliente, ou a janela de `o_que_e_urgente` se for maior | Advogado confere a preparação; `preparar-o-cliente` |
| Senha, código ou golpe | cliente manda senha ou código, pede que o escritório entre com a senha dele, conta que alguém pediu dinheiro, código ou senha em nome do escritório | Pessoa liga pelo número oficial; nada se pede nem se envia |

Aflição tem dois pesos, os mesmos do `agente-de-suporte`: desespero ou crise é **pessoa agora**; medo ou ansiedade ligado a um compromisso que ainda está a mais de um dia ("tenho medo de ir sozinha") é **alta**, com acolhimento na ponte e a `preparar-o-cliente`. Queixa de demora sem ameaça ("faz um mês que ninguém me fala nada") é **alta**, e a régua que falhou é apontada.

### 4.2 Tipos

`andamento`, `documento`, `compromisso`, `financeiro`, `encerramento`, `cliente-com-ia`, `acesso` (quer acompanhar o processo: número, página, "senha do sistema"), `preferencia` (como quer receber notícias), `agradecimento`, `reclamacao`, `aflicao`, `vulnerabilidade`, `noticia-ruim-pendente`, `seguranca` (senha, código, golpe), `outro`.

### 4.3 Árvore da urgência

1. Sinal da 4.1? **Alta, pessoa agora.**
2. Palavra de alerta da ficha; compromisso em até 7 dias corridos; cliente além do `maximo_sem_noticia`; queixa de demora sem ameaça; medo ligado a compromisso (sem desespero nem crise); segunda pergunta sem resposta? **Alta**, com acolhimento quando há medo.
3. Pedido concreto (andamento, documento, financeiro, encerramento, acesso, cliente com IA, compromisso mais distante)? **Normal.**
4. Agradecimento, "ok", figurinha, preferência, informação sem pedido? **Baixa.**

### 4.4 Caminhos

| Caminho | Quando | Ponte | Próxima habilidade (se instalada) |
|---|---|---|---|
| Pessoa agora | Seção 4.1 | Nenhuma com conteúdo; no máximo a `ponte-pessoa-agora`, se a ficha permitir e quem liga quiser | `status-para-o-cliente` (roteiro), `reclamacao-e-recuperacao`, `preparar-o-cliente` |
| Andamento | Pergunta do processo | "Recebi, olho e te retorno até [HORA]" | `status-para-o-cliente` |
| Documento | Manda, pergunta ou remarca documento | Confirmação ou o combinado | `checklist-de-documentos`: controle do documento e lembrete na data combinada (passo 6) |
| Compromisso | Audiência, perícia, reunião | "A [FUNÇÃO] te manda o que levar até [HORA]" | `preparar-o-cliente` |
| Financeiro e encerramento | Repasse, honorários, acordo, prestação de contas | "A advogada te manda a prestação de contas por escrito"; nunca valor na ponte | `encerramento-do-caso` |
| Cliente com IA | Traz resposta de IA, print do tribunal, vídeo | "Recebi. Te explico o que isso quer dizer até [HORA]" (sem elogiar a pergunta) | `cliente-com-ia` |
| Acesso | Quer acompanhar, pede número ou senha | Número do processo pelo canal oficial depois de conferido; senha nunca; oferece a página ou o resumo | `pagina-do-caso` |
| Preferência | Quer menos ou outro tipo de contato | Confirma, sem insistir | (registro) |
| Só registrar | Agradecimento, "ok" | Cortesia curta opcional | (fim) |

Sem as habilidades indicadas: a ponte segue igual, e quem cuida responde pelo modelo da biblioteca.

### 4.5 Prazos

- **Pessoa agora:** assim que a mensagem é vista, pelo caminho de `urgencia_vai_para`; reclamação no `prazo_de_retorno_da_reclamacao`.
- **Alta:** ponte assim que o expediente abre e retorno completo no mesmo dia útil (ou antes do compromisso, o que vier primeiro).
- **Normal:** `primeira_resposta_cliente_ativo`, em horas úteis contadas dentro de `horario_de_atendimento`. Mensagem fora do horário conta a partir da abertura do próximo dia útil. Feriado: o que a ficha disser `[A CONFIRMAR]`.
- **Baixa:** sem prazo; se houver cortesia, no prazo normal.
- **Resposta completa:** `resposta_completa`; se depender do advogado, a ponte já diz até quando.

## 5. Pontes-base (rascunho até o escritório aprovar)

Como toda ponte é escrita:
- **Começa pelo recebimento, nunca por elogio à pergunta.** Nada de "Boa pergunta", "Ótima pergunta" ou "Que bom que perguntou": soa automático e não diz nada.
- **Uma ideia por parágrafo**, separados por linha em branco: recebi; o que vai acontecer (ou o acolhimento); até quando. Pedido simples resolvido na ponte pode juntar recebi e resposta num parágrafo curto.
- Sem resultado, data de decisão, valor ou explicação de decisão (regra fixa 2).

**`ponte-pessoa-agora`** (só para pessoa agora, só se a ficha permitir, nunca em violência, risco, senha ou golpe; nada além disso)
```
Oi, [NOME]. Recebi sua mensagem.

A [FUNÇÃO DE QUEM LIGA] vai te ligar {QUANDO}.
```

**`ponte-andamento`**
```
Oi, [NOME]! Recebi sua mensagem.

Vou olhar o seu processo com calma.

Te retorno até [HORA] com tudo explicado.
```

**`ponte-atraso`**
```
Oi, [NOME]. Você tem razão: ficou tempo demais sem notícia nossa. Desculpa.

A [FUNÇÃO] olha o seu processo hoje.

Ela te liga até [HORA].
```

**`ponte-documento`**
```
Pode sim, [NOME]. Obrigada por avisar!

Fico esperando [DOCUMENTO] na [DIA].

Se tiver dificuldade para conseguir, me fala.
```

**`ponte-compromisso`**
```
Recebi, [NOME].

A [FUNÇÃO] te manda ainda hoje o que levar e como vai ser.
```

**`ponte-financeiro`**
```
Oi, [NOME]! Recebi sua mensagem.

A advogada vai te mandar a prestação de contas por escrito, com tudo explicado.

Até [HORA] eu te confirmo quando fica pronta.
```

**`ponte-cliente-com-ia`**
```
Oi, [NOME]! Recebi sua mensagem.

Vou te explicar direitinho o que isso quer dizer no seu processo.

Te respondo até [HORA].
```

**`ponte-acesso`**
```
[NOME], o número do processo eu te passo por aqui depois de conferir.

A senha do sistema não dá para passar: ela é pessoal de quem acessa.

Para você acompanhar, posso te mandar a página do seu caso, com o que já aconteceu e o que vem.
```

**`ponte-preferencia`**
```
Combinado, [NOME]. [O QUE MUDA].

Quando tiver novidade no seu processo, [COMO VAI SER AVISADO].
```

**`cortesia`**
```
Nós que agradecemos, [NOME]! Qualquer coisa, estamos por aqui.
```

A ponte e a cortesia entram no histórico, mas não mudam o `ultimo_contato` da carteira: elas não informam o caso (`../../docs/agentes-e-fila.md`).

Os `[CAMPOS]` são preenchidos pela habilidade antes de ir para a fila (o `[HORA]` sai da conta da seção 4.5, a `[FUNÇÃO]` de `quem_cuida_dos_casos`). Uma ponte com `[A PREENCHER]` não sai. Os campos entre chaves (`{QUANDO}`) são do envio: quem envia preenche na hora, e a fila não deixa marcar como enviado com chave no texto.

## 6. Formato da saída

### 6.1 Uma mensagem (o cartão)
```
TRIAGEM · [CÓDIGO] [nome curto] · [dia HHhMM] · [canal]
Tipo: ...   Urgência: pessoa agora | alta | normal | baixa
Assunto: ...   Sinal: ... (ou "nenhum")
Caminho: ...   Quem cuida: ...   Até: [dia HHhMM]
Ponte (A, [quem lê] lê antes de enviar): "..."  (ou "nenhuma: [motivo]")
Para a pessoa: [o que ela faz e com que material]
Registro: [linha do histórico] · [proposta na carteira]
Antes de enviar: [campos da ficha que faltaram, conferências]
```

### 6.2 O lote do dia (`mensagens/AAAA-MM-DD.md`)
Cabeçalho (documento, versão, data, dono), "Antes de enviar" (o que falta conferir, interno), depois: **PESSOA AGORA** (uma frase por item), a tabela (hora, código, tipo, urgência, caminho, quem cuida, até, ponte em uma linha), as pontes completas numeradas, as propostas para a carteira, "PARA DECIDIR" e o resumo ("12 mensagens: 4 pessoa agora, 2 altas, 4 normais, 2 baixas"). Exemplo completo: `references/lote-de-treino-2026-04-10.md`.

### 6.3 A linha do histórico
Se o `historico.md` não existir, crie com cabeçalho (documento, versão, data, dono) e a tabela abaixo. Se existir, siga o formato dele.
```
| Data e hora | Canal | Quem falou | O que foi dito (uma frase) |
|---|---|---|---|
| 2026-04-10 08h05 | whatsapp | cliente | perguntou se o processo está parado; triagem alta, advogada retorna hoje |
```
Nunca o texto inteiro da mensagem. Nunca dado de saúde: "intercorrência de saúde".

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Lote do dia | `escritorio/07-operacao/experiencia/mensagens/AAAA-MM-DD.md` |
| Linha do histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Pontes no ciclo | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-resposta-ponte.md` |
| Carteira | `carteira.csv`: `proximo_contato`, `motivo_proximo_contato`, `atualizado_em`; o resto só proposto |
| Correções, sinais e pontes aprovados | `aprendizados-experiencia.md`, `ficha-do-escritorio.md` (`palavras_de_alerta`), `biblioteca-de-mensagens.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` (mesma estrutura) |

Uma mensagem só, sem pedido de gravar: entregue o cartão e grave só a linha do histórico. Sem pasta aberta: tudo no chat, com o caminho de cada arquivo.

## 8. Solo e equipe

**Solo:** "quem cuida" é quase sempre o titular. A triagem serve para a ordem: o que é agora, o que é hoje, o que espera o horário fixo. Responda as normais em dois horários do dia, com a ponte valendo no meio tempo.

**Equipe:** a secretária ou a assistente tria com esta habilidade; o advogado recebe só pessoa agora e o que é jurídico. Se o mesmo nome aparece em todos os caminhos, aponte: ali está o gargalo. Se a mesma falha da régua aparece em vários clientes, leve para a `jornada-do-cliente` (se instalada).

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Responder "saiu a sentença" por mensagem | O cliente lê sozinho a pior notícia | Notícia ruim pendente vai para pessoa agora |
| Tratar ameaça de ir à OAB como dúvida de andamento | Cliente se sente ignorado e a reclamação cresce | Sinais de reclamação na 4.1 |
| Mandar ou pedir senha | Risco de golpe e de acesso indevido | Regra fixa 3 e caminho "acesso" |
| Gravar "internada na UTI" no histórico | Dado de saúde fora do lugar | Regra fixa 4 |
| Ponte que promete data do juiz | Promessa que o escritório não cumpre | Regra fixa 2 |
| Audiência de amanhã atrás de dez "obrigado" | Cliente chega despreparado | Pessoa agora e lote ordenado |
| Mensagem de domingo esquecida | Cliente sem resposta na segunda | Ciclo lê desde a última rodada |
| Resumo cortado e notícia relevante cortada junto | Escritório deixa de informar o que deve | Preferência suspende só a rotina |

## 10. Próximo passo

- Notícia ruim: `status-para-o-cliente` (se instalada) para o roteiro de ligação; sem ela, o advogado liga com o histórico aberto.
- Reclamação: `reclamacao-e-recuperacao` (se instalada); sem ela, quem a ficha manda liga no prazo e registra.
- Compromisso: `preparar-o-cliente` (se instalada); sem ela, o advogado liga com a lista do que levar.
- Cliente com IA: `cliente-com-ia` (se instalada); sem ela, explique o termo com o glossário e não confirme nada sem o advogado.
- Triagem todo dia sem ninguém pedir: `rotina-da-experiencia` e `/motor-experiencia:ciclo`.

## Referências desta habilidade

- `references/sinais-do-cliente-ativo.md`: sinais de pessoa agora e de alta por área, do jeito que o cliente escreve, para o escritório confirmar. Leia no passo 2 quando a ficha não tiver `palavras_de_alerta`, e no modo adaptar.
- `references/lote-de-treino-2026-04-10.md`: o lote completo das 12 mensagens de `../../docs/casos-ficticios.md`, com as pontes e os registros, conferido contra o gabarito. Use para testar a habilidade e para treinar a equipe.
