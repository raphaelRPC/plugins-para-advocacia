---
name: jornada-do-cliente
description: >
  Desenha a jornada e a régua de cada tipo de caso: para cada fase (entrada, documentos,
  protocolo, espera, audiência ou perícia, decisão, recurso, cumprimento, encerramento), o que
  o cliente sente, o que o escritório diz sem ser perguntado, de quanto em quanto tempo, por
  qual canal, quem fala, o que nunca vai por mensagem e o que vira resumo ou página do caso.
  Parte de jornadas-base por área para confirmar, com tempos de fase sempre para conferir e
  nunca prometidos. Use quando o advogado disser "monta a régua do BPC", "o que eu falo em cada
  fase", "como o cliente fica sabendo do processo", "quero chegar antes da pergunta", "jornada
  do cliente", "de quanto em quanto tempo eu aviso". Não use para escrever a mensagem de uma
  movimentação (use status-para-o-cliente) nem para receber quem acabou de fechar (use
  boas-vindas-do-cliente).
---

# Jornada do cliente

> Cada tipo de caso tem os seus momentos de silêncio e de aflição. A jornada escreve, fase por fase, o que o escritório diz antes de o cliente perguntar, quando, por onde e quem fala. É ela que faz o escritório chegar antes da IA e do site do tribunal.

Regras comuns do plugin: `../../docs/regras.md`. A carteira e as fases: `../../docs/carteira.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Adaptação ao nicho: `../../docs/adaptar-ao-escritorio.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`.

Toda cliente de BPC pergunta a mesma coisa na mesma semana: logo depois da avaliação social, quando o Meu INSS mostra "em análise" e nada mais. O escritório que sabe disso manda, no dia seguinte à avaliação, duas linhas explicando o que vem e de quem depende. O que não sabe responde a mesma pergunta vinte vezes por mês, uma de cada vez.

**Regras fixas desta habilidade:**
1. Tempo de fase é sempre `[CONFERIR]`, para uso interno. Nunca vai para mensagem, resumo ou página como promessa de data.
2. A jornada-base do plugin é sugestão. Cada linha vale só depois que o advogado confirmar, ajustar ou tirar. Linha não confirmada fica `[A CONFIRMAR]` e o agente segue a ficha naquela fase.
3. A jornada só promete o que o escritório cumpre hoje. Cadência que ninguém vai cumprir sai, ou fica `[A DEFINIR]`.
4. Notícia ruim, mudança de estratégia, proposta de acordo e o que estiver em `nunca_por_mensagem` são ligação em qualquer fase.
5. A jornada é da base: sem nome de cliente, número de processo ou dado de saúde.

## 1. Quando usar

**Use quando:**
- O escritório quer a régua de um tipo de caso ("o BPC", "as trabalhistas de verbas", "os divórcios").
- O mesmo "e aí?" chega muitas vezes na mesma fase.
- O `/motor-experiencia:comecar` ou a `rotina-da-experiencia` apontou clientes sem notícia além da régua com frequência.
- A `adaptar-experiencia` chamou esta habilidade no modo adaptar.
- O escritório entrou num tipo de caso novo.

**Não use quando:**
- O pedido é a mensagem de uma movimentação: use `status-para-o-cliente`.
- O pedido é o resumo do mês de um cliente: use `resumo-mensal-do-caso`.
- O pedido é receber quem acabou de fechar: use `boas-vindas-do-cliente`. A jornada diz o que a boas-vindas promete; a boas-vindas executa.
- O pedido é a lista de documentos de um tipo de caso: use `checklist-de-documentos` (se instalada). Sem ela, a fase `documentos` da jornada lista os principais e marca `[A CONFIRMAR]`.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`) e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`).
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`), se existir. As seções "Como ele fala", "Os momentos de aflição" e "O que este nicho pesquisa sozinho" entram direto nas colunas "o que o cliente sente" e nos momentos de aflição.
3. **Leia o que já existe** em `escritorio/04-base/relacionamento-com-o-cliente/`: outras jornadas (para não repetir), a biblioteca de mensagens (para apontar o modelo de cada fase) e, se o escritório usa o plugin `inicio-automacao`, a `regua-de-atualizacao.md`. Se houver régua, ela é o ponto de partida, antes da base do plugin.
4. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "Quantos dias, no máximo, um cliente pode ficar sem notícia?" e "Quando sai uma movimentação importante, em quanto tempo vocês avisam?".
5. **Escolha a base** em `references/`, pela área do tipo de caso (seção 6).

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas`, `casos_mais_comuns` · X: `avisa_movimentacao_relevante`, `maximo_sem_noticia`.
- **Melhora:** E: `nicho` · X: `resumo_mensal`, `lembrete_de_compromisso`, `nunca_por_mensagem`.

Campo que falta e a jornada pede: pergunte aquele campo, uma vez, e ofereça gravar na ficha.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Entrevista | Primeira jornada de um tipo de caso | O tipo de caso | A jornada, fase por fase, confirmada |
| Rápido | O advogado quer ver pronto e corrigir | O tipo de caso | A base preenchida com as fichas, e até 4 perguntas |
| Adaptar | Chamado pela `adaptar-experiencia` | As jornadas gravadas e o `nicho.md` | As jornadas reescritas para o nicho, com `[ALTERADO]` |
| Revisar | Perguntas repetidas na mesma fase, ou revisão trimestral | A jornada e os aprendizados | A versão nova, com o que mudou |

### Modo entrevista

**Passo 1. O tipo de caso.** Pergunte: "Para qual tipo de caso vamos desenhar a jornada?". Sugira os de `casos_mais_comuns`. Um tipo de caso por vez. Caso administrativo e judicial do mesmo assunto podem ser uma jornada só, com as fases dos dois, se o advogado preferir.

**Passo 2. As fases.** Mostre as fases da base da área, em uma linha cada, e pergunte: "Esse é o caminho desse caso aqui no escritório? Falta ou sobra alguma fase?". Use os nomes de fase da carteira (`../../docs/carteira.md`), para a rotina reconhecer.

**Passo 3. A régua do tipo de caso.** Mostre o que vem da ficha (`maximo_sem_noticia`, `avisa_movimentacao_relevante`, `resumo_mensal`, `lembrete_de_compromisso`) e pergunte: "Para esse tipo de caso vale a régua da ficha, ou precisa ser mais curta em alguma fase?". Exemplo: BPC com cliente idoso pode pedir notícia a cada 15 dias na espera. A régua mais curta de uma fase vai na linha "Máximo sem notícia nesta fase" (com o número), que é a que a rotina lê para apontar quem está sem notícia.

**Passo 4. Fase por fase.** Para cada fase, mostre a linha da base já preenchida com as fichas e o nicho e pergunte uma coisa só: "Confirma, ajusta ou tira?". Se o advogado ajustar, peça a cena concreta: "E a última cliente nessa fase, o que ela perguntou?". O que o cliente sente vai com as palavras do cliente, do nicho ou da resposta do advogado.

**Passo 5. Os momentos de aflição.** Mostre os da base e do nicho e pergunte: "Quando o cliente desse tipo de caso costuma se desesperar?". Para cada momento, o que o escritório faz e quem. Sinal de violência, risco à vida ou criança em risco nunca é "momento da jornada": é parada imediata, para o advogado (`../../docs/regras.md`, seção 5).

**Passo 6. As perguntas que chegam.** Pergunte: "Quais perguntas desse tipo de caso chegam sempre?". Liste as cinco mais comuns. Se a `cliente-com-ia` estiver instalada, aponte que ela responde cada uma antes de o cliente perguntar; sem ela, as perguntas ficam na jornada para a `status-para-o-cliente` usar.

**Passo 7. Tempos de fase.** Para cada fase, `[CONFERIR]`. Se o advogado der um tempo típico, grave como estimativa dele, com `[CONFERIR]` ao lado, na seção de uso interno.

**Passo 8. Mostrar e gravar.** Monte no formato de `assets/modelo-da-jornada.md`, mostre inteira e grave com o ok. Diga o que ficou `[A CONFIRMAR]`.

**Passo 9. Aprender.** Pergunte: "Tem alguma coisa nessa jornada que vale para todos os tipos de caso?". Uma regra que vale para todos vai para a ficha (por exemplo, `nunca_por_mensagem`) ou para os aprendizados ("Cliente idoso sempre recebe ligação na fase de perícia"), com o ok (`../../docs/aprender-com-o-uso.md`).

### Modo rápido

1. Pergunte o tipo de caso.
2. Monte a jornada inteira a partir da base, das fichas e do nicho, e mostre.
3. Pergunte até três coisas: "Alguma fase sobra ou falta?", "A régua da ficha vale para esse caso?" e "Alguma linha você mudaria?".
4. Grave com o ok. Linhas sem resposta ficam `[A CONFIRMAR]`. Feche com o passo Aprender.

### Modo adaptar

Chamado pela `adaptar-experiencia` depois que o `nicho.md` foi escrito.
1. Leia todas as jornadas gravadas e o `nicho.md`.
2. Reescreva o que o nicho muda: o que o cliente sente (com as palavras do nicho), os momentos de aflição, as perguntas que chegam, o canal (por exemplo, ligação para público com pouca leitura), a cadência na espera.
3. Marque cada mudança `[ALTERADO]`, com uma linha do porquê. Não mexa em linha que o advogado já confirmou sem mostrar.
4. Nicho sem jornada ainda: proponha as jornadas dos três `casos_mais_comuns` do nicho, no modo rápido.
5. Mostre tudo, grave com o ok, suba a versão. **Aprender**, como no modo entrevista.

### Modo revisar

1. Leia a jornada, os aprendizados e, se houver, os históricos de clientes desse tipo de caso que perguntaram duas vezes no mesmo mês (a `rotina-da-experiencia` aponta).
2. Mostre em que fase as perguntas se repetem e proponha a mudança (uma mensagem a mais, cadência mais curta, ligação em vez de mensagem).
3. Grave com o ok, versão nova e linha no histórico. **Aprender**, como no modo entrevista.

## 4. O que cada coluna quer dizer

| Coluna | O que vai | Erro comum |
|---|---|---|
| O que o cliente sente | Uma frase, com as palavras do cliente | Escrever o que o advogado sente ("o processo está regular") |
| O que o escritório diz sem ser perguntado | O assunto da mensagem, não o texto inteiro | Prometer data de decisão |
| Quando | Um gatilho (no protocolo, na marcação) ou um intervalo (a cada 15 dias) | Intervalo que ninguém cumpre |
| Canal | Mensagem, ligação, reunião, resumo, página | Mensagem para notícia que pede conversa |
| Quem fala | Função | Nome de cliente |
| Nunca por mensagem | O que dessa fase vai por ligação | Deixar vazio na fase de decisão |
| Vira resumo ou página | O que entra no resumo do mês ou na página do caso | Pôr na página o que o cliente ainda não ouviu por ligação |

## 5. Exemplo resolvido (Escritório Modelo)

Tipo de caso: BPC idoso, previdenciário (caso da Helena, que fala pela mãe, nos casos fictícios). Base: `references/jornada-base-previdenciario.md`. Ficha: máximo 30 dias sem notícia, aviso em 2 dias úteis, resumo em PDF no dia 5. O advogado ajustou a espera na fase `aguardando` para 15 dias, porque a família fica aflita. Hoje (2026-04-10) a Helena está em `protocolado`, então vale a régua da ficha: notícia até 2026-04-27, como está na carteira e na página do caso. Os 15 dias passam a valer quando o caso entrar em `aguardando`.

```
### aguardando · o pedido está com o INSS ou com o juiz
- O que o cliente sente: "Olhei no site e tá parado, será que esqueceram da minha mãe?"
- O que o escritório diz sem ser perguntado: o que está sendo esperado e de quem depende, mesmo sem movimentação; que o escritório olha o processo [A DEFINIR: de quanto em quanto tempo]
- Quando: a cada 15 dias e no resumo do dia 5
- Máximo sem notícia nesta fase: 15 dias corridos
- Canal: mensagem para a filha (autorizada); ligação se a mãe preferir
- Quem fala: secretária
- Nunca por mensagem: previsão de data; qualquer notícia sobre a saúde da mãe
- Vira resumo ou página: o resumo do mês explica a espera e conta o trabalho do escritório registrado no histórico (canal `trabalho-do-escritorio`); a página mostra a linha do tempo e o "o que já fizemos por você"
- Modelo da biblioteca: nada-mudou
- Situação: confirmado
```

E na seção de uso interno: "Análise do pedido: `[CONFERIR]`". Esse tempo nunca aparece no resumo da Helena.

## 6. As jornadas-base

| Área | Arquivo | Tipos de caso de exemplo |
|---|---|---|
| Previdenciário | `references/jornada-base-previdenciario.md` | aposentadoria, incapacidade, BPC, revisão |
| Trabalhista | `references/jornada-base-trabalhista.md` | verbas, horas extras, vínculo, acidente |
| Família | `references/jornada-base-familia.md` | divórcio, alimentos, guarda |
| Consumidor | `references/jornada-base-consumidor.md` | negativação, banco, plano de saúde |
| Cível | `references/jornada-base-civel.md` | cobrança, indenização, contratos, locação |

Área fora da lista: monte a partir da base mais próxima e marque cada linha `[A CONFIRMAR]`.

## 7. Formato da saída

No chat, antes de gravar: a jornada inteira, no formato de `assets/modelo-da-jornada.md`, e no fim a lista do que ficou `[A CONFIRMAR]` e `[CONFERIR]`. O arquivo gravado tem: cabeçalho (documento, versão, data, dono, área, base), a régua do tipo de caso, uma seção por fase com as dez linhas (sente, diz, quando, máximo sem notícia, canal, quem, nunca por mensagem, resumo ou página, modelo da biblioteca, situação), os momentos de aflição, as perguntas que chegam, os tempos de fase em uso interno e o histórico.

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Jornada do tipo de caso | `escritorio/04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md` |
| Régua que passou a valer para todos | `escritorio/04-base/comum/ficha-da-experiencia.md`, com linha no histórico |
| Regras aprendidas | `escritorio/04-base/comum/aprendizados-experiencia.md` |

A jornada não muda a carteira nem manda nada a cliente. Quem usa: o agente de suporte (o que rascunhar em cada fase), a `status-para-o-cliente` (o "quando volto a falar"), a `resumo-mensal-do-caso` (o que vem na próxima fase) e a `boas-vindas-do-cliente` (o combinado de comunicação). Sem pasta aberta: a jornada vem no chat, para colar nas instruções do Projeto.

## 9. Solo e equipe

**Solo:** comece pelo tipo de caso que mais gera "e aí?". Uma jornada bem feita vale mais que cinco pela metade. A coluna "quem fala" é quase sempre o titular; aproveite para marcar o que pode ser mensagem aprovada (A) e o que só ele faz (H).

**Equipe:** a advogada confirma as fases de decisão e o que nunca vai por mensagem; a secretária, que ouve as perguntas, preenche o que o cliente sente e as perguntas que chegam. A jornada é o acordo entre as duas sobre quem fala o quê.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Em seis meses sai" na jornada | A data vira promessa no resumo | Regra fixa 1, tempos só em uso interno |
| Régua igual para todo tipo de caso | O cliente de BPC fica aflito e o de cobrança acha excessivo | Uma jornada por tipo de caso |
| Copiar a base do plugin sem conferir | Fase que não existe no escritório, cadência que ninguém cumpre | Linha só vale confirmada |
| Notícia de decisão por mensagem | O cliente lê sozinho a pior notícia | Fase de decisão sempre com ligação primeiro |
| Silêncio na espera | Cliente pesquisa sozinho e chega com a resposta da IA | Fase `aguardando` com mensagem mesmo sem movimentação |
| Jornada com nome de cliente | Dado de cliente na base do Projeto | Regra fixa 5 |

## 11. Próximo passo

- Mensagens de cada fase no tom do escritório: `status-para-o-cliente` (andamento) e `boas-vindas-do-cliente` (combinado de comunicação).
- O resumo do mês com o "o que vem" da jornada: `resumo-mensal-do-caso`.
- As perguntas do tipo de caso respondidas antes: `cliente-com-ia` (se instalada). Sem ela, deixe as perguntas na jornada.
- O ciclo do dia seguindo a jornada: `rotina-da-experiencia`.
- A jornada no jeito do nicho: `adaptar-experiencia`.

## Referências desta habilidade

- `assets/modelo-da-jornada.md`: o formato do arquivo da jornada. Use no passo 8.
- `references/jornada-base-previdenciario.md`, `references/jornada-base-trabalhista.md`, `references/jornada-base-familia.md`, `references/jornada-base-consumidor.md`, `references/jornada-base-civel.md`: as jornadas-base por área, para confirmar. Leia no passo 2, pela área do tipo de caso.
