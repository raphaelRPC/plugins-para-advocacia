---
name: cliente-com-ia
description: >
  Quando o cliente chega com a resposta de uma IA, o print do site do tribunal ou um vídeo da
  internet: acolhe, explica o que aquilo quer dizer no caso dele, corrige com calma o que
  estiver errado, nunca confirma tese, prazo ou resultado sem o advogado e transforma a
  pergunta em aprendizado. E o "antes da pergunta": por tipo de caso, as perguntas que o
  cliente vai fazer respondidas na linguagem dele, com os erros comuns da internet por área,
  para a boas-vindas, o resumo e a página do caso. Use quando o advogado disser "ele perguntou
  pro ChatGPT", "mandou um print do processo", "viu um vídeo dizendo que tem direito", "o que
  eu respondo pra isso?", "monta as perguntas do caso de BPC". Não use para traduzir
  movimentação sem pergunta do cliente (use status-para-o-cliente) nem para quem ainda não é
  cliente (use triar-contato do motor-comercial, se instalado).
---

# Cliente com IA

> O cliente pesquisa antes de perguntar. Quando ele traz a resposta pronta, o escritório acolhe, explica e corrige sem diminuir ninguém. E, melhor ainda, responde antes: as perguntas do caso já estão escritas na linguagem dele.

Regras comuns: `../../docs/regras.md` (seção 4, item 6). Fichas: `../../docs/ficha-da-experiencia.md`. Carteira: `../../docs/carteira.md`. Onde gravar: `../../docs/pasta.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

A Helena viu "concluso para despacho" no site do tribunal, perguntou a uma IA e ouviu que o juiz decide naquela semana. Se o escritório responde "não é bem assim", ela fica entre duas vozes. Se responde explicando o que o termo quer dizer, por que ninguém sabe a data e o que o escritório faz enquanto isso, ela ganha uma explicação melhor que a da IA e volta a perguntar ao escritório primeiro.

**Regras fixas desta habilidade:**
1. Acolher sempre: a pergunta é boa, pesquisar é direito do cliente. Nunca ridicularizar a IA, o vídeo ou o cliente.
2. Nunca confirmar tese, direito, prazo, valor ou resultado que a IA ou o vídeo disseram sem o advogado conferir. O que depende do caso vai para o advogado, e o cliente fica sabendo disso.
3. Explicar o termo do processo pode ser A, com o glossário. Dizer se o cliente tem direito a algo novo é do advogado (H), por ligação ou reunião.
4. Print do tribunal e vídeo podem trazer número do processo, nome da outra parte e dado de saúde: troque antes de seguir e não repita.
5. Erro comum da internet registrado nesta habilidade fica `[CONFERIR]` até o advogado confirmar, e a confirmação vale por área e por data: regra muda.

## 1. Quando usar

**Use quando:**
- O cliente traz a resposta de uma IA, o print do site do tribunal ou do INSS, ou um vídeo das redes.
- A `triar-mensagem-do-cliente` (se instalada) apontou o caminho "cliente com IA".
- O escritório quer escrever, por tipo de caso, as perguntas que o cliente vai fazer, respondidas antes ("antes da pergunta").
- A `pagina-do-caso`, a `boas-vindas-do-cliente` ou a `resumo-mensal-do-caso` (se instaladas) precisam das perguntas do caso.

**Não use quando:**
- Há notícia ruim pendente no caso: a pergunta vira ligação do advogado (`status-para-o-cliente`, se instalada).
- A pergunta é uma reclamação ("a IA disse que vocês estão enrolando"): `reclamacao-e-recuperacao` (se instalada) ou o advogado liga.
- Quem pergunta ainda não é cliente: isso é orientação a quem não é cliente, e vai para a `triar-contato` do motor-comercial (se instalado), com o convite para a consulta.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` (seção "O que este nicho pesquisa sozinho") e `aprendizados-experiencia.md`, se existirem.
2. Sem fichas: ofereça `/motor-experiencia:comecar`. Para seguir agora, pergunte só "Como vocês tratam o cliente?" e "Em que áreas vocês atuam?".
3. Leia, se existirem: `escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md` e `perguntas-do-caso-<tipo-de-caso>.md` do tipo do cliente. A resposta já aprovada vale antes de qualquer texto novo.
4. Leia a linha da `carteira.csv` e o `clientes/<codigo>/historico.md`: fase, último contato, o que já foi explicado, se há decisão ainda não conversada.
5. Conta e dados: cliente real só em conta profissional ou de equipe; em conta pessoal, só os casos fictícios (`../../docs/casos-ficticios.md`, mensagem 4), gravando em `escritorio/07-operacao/_treino/experiencia/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tratamento`, `areas`.
- **Melhora:** E: `nicho`, `como_o_cliente_fala`.
- Lê também, se preenchidos: E: `tom_em_tres_palavras`, `frases_que_nunca_usamos`, `assinatura_das_mensagens`, `casos_mais_comuns`; X: `quem_le_antes_de_enviar`, `primeira_resposta_cliente_ativo`.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | Saída |
|---|---|---|---|
| Responder | O advogado, a equipe, a triagem | Acolhe, explica, corrige, separa o que é do advogado | Resposta (A) no chat e o pedido ao advogado (H), se houver |
| Antes da pergunta | O advogado, a jornada, a página | Escreve as perguntas do tipo de caso, respondidas | `perguntas-do-caso-<tipo>.md` |
| No ciclo | O `agente-de-suporte` | Rascunha a resposta na fila; tese, prazo e valor viram "PARA DECIDIR" | Fila; nada mostrado |
| Adaptar | `adaptar-experiencia` | Reescreve as perguntas-base e os erros comuns para o nicho | `perguntas-do-caso-<tipo>.md`, `[ALTERADO]` |

**Modo direto:** "ele mandou isso aqui: [print ou texto]". Execute e pergunte só o que falta.

### Modo responder

**Passo 1. Receber e limpar.** Print: leia só o necessário e troque número do processo por `[PROCESSO]`, nomes por `[CLIENTE]` e `[OUTRA PARTE]`; avise em uma linha. Vídeo ou link: não abra; peça ao cliente ou à equipe o resumo do que o vídeo diz ("o que exatamente ele falou?"). Áudio: a transcrição.

**Passo 2. A pergunta por trás da pergunta.** O que o cliente quer saber de verdade: quando sai (ansiedade com o tempo), se tem direito a mais (expectativa), se o escritório está fazendo algo (desconfiança), se deve fazer alguma coisa (medo de perder prazo). Desconfiança forte ou queixa: é reclamação, saia por ela. Aflição forte: o advogado liga.

**Passo 3. Separar o que a IA disse em pedaços.** Para cada afirmação:

| Tipo de afirmação | Exemplo | O que fazer |
|---|---|---|
| Termo do processo | "concluso para despacho é quando o juiz vai decidir" | Explicar com o glossário (A) |
| Previsão de data | "o juiz decide essa semana" | Corrigir com calma: ninguém sabe a data; nunca outra data no lugar |
| Previsão de resultado | "seu caso é ganho" | Não confirmar nem negar: resultado é conversa do advogado |
| Tese ou direito novo | "todo aposentado tem direito a essa revisão" | Não confirmar nem negar: o advogado olha o caso (H) |
| Prazo ou providência | "você tem 15 dias para fazer X" | Advogado confere antes de qualquer resposta |
| Valor | "você vai receber R$ X" | Nunca por mensagem; advogado e financeiro |

Classifique cada uma: **certo** (pode dizer que está certo, com a explicação), **incompleto** (complete), **errado** (corrija com calma), **depende do caso** (advogado). Na dúvida, "depende do caso".

**Passo 4. Escrever a resposta.** Quatro partes, curtas:
1. **Acolher:** "Recebi, e foi bom você trazer isso para cá." (sem elogio à pergunta, que soa automático)
2. **Explicar:** o que aquilo quer dizer, em linguagem simples, no caso dele.
3. **Corrigir ou completar:** o que a IA não tinha como saber ("a IA não enxerga o seu processo nem a agenda do juiz"), sem tom de bronca.
4. **O que vem e o convite:** o que o escritório faz agora, quando volta a falar, e "pode sempre perguntar aqui primeiro".

O que é "depende do caso" sai da mensagem e vira pedido ao advogado: "Isso eu vou levar para a advogada olhar no seu processo e ela te responde até [PRAZO DA FICHA, DE resposta_completa; SEM ELE, {ATÉ QUANDO}]". O prazo sai da ficha; sem ele, fica entre chaves para quem envia preencher com um prazo que a advogada consegue cumprir. Tese ou direito novo: ligação ou reunião, nunca resposta por escrito da IA.

**Passo 5. Conferir.** Nenhuma data de decisão, chance, valor ou "você tem direito". Termo explicado bate com o glossário. Tratamento e tom da ficha. Resposta lida por `quem_le_antes_de_enviar` (sigla A); o que é do advogado, H.

**Passo 6. Registrar e aprender com a pergunta.**
- `historico.md`, linha de contato na tabela: `| AAAA-MM-DD HHhMM | whatsapp | cliente | trouxe resposta de IA sobre [assunto em cinco palavras]; explicado [ou: levado à advogada] |`. A explicação enviada informa o caso e, depois do envio, muda o `ultimo_contato`; a ponte "te respondo até" não muda.
- A pergunta entra em `perguntas-do-caso-<tipo>.md`, seção "Perguntas que chegaram", com a data e a situação `nova`. Se ela se repete, o advogado aprova uma resposta e ela sobe para as perguntas respondidas. Se o erro da IA é um padrão, entra em "Erros comuns da internet", `[CONFERIR]` até o advogado confirmar.

### Modo antes da pergunta

1. Pergunte: "Para qual tipo de caso?". Sugira os de `casos_mais_comuns`.
2. Leia as perguntas-base do tipo em `references/perguntas-base-por-tipo.md` e os erros da área em `references/erros-comuns-por-area.md`. Some as perguntas reais que já chegaram (histórico, nicho, aprendizados).
3. Organize por fase da jornada (entrada, espera, compromisso, decisão, pagamento ou encerramento). Para cada pergunta, a resposta em até quatro frases, na linguagem de `como_o_cliente_fala`, sem prazo de decisão e sem promessa. O que depende do caso fica "a advogada explica no seu caso".
4. Mostre com o cabeçalho interno ("Antes de usar": o que está `[CONFERIR]`). Peça ao advogado que leia cada resposta: as aprovadas ficam `aprovada`, as outras `rascunho`.
5. Grave em `perguntas-do-caso-<tipo-de-caso>.md` (modelo em `assets/modelo-perguntas-do-caso.md`) com o ok.
6. Diga onde usar: duas ou três perguntas da fase de entrada nas boas-vindas; a pergunta da fase atual no resumo do mês; o glossário e uma pergunta na página do caso. Só respostas `aprovada` vão ao cliente.

### No ciclo (o agente chama)
1. A triagem marcou "cliente com IA". Rode os passos 1 a 5 do modo responder.
2. Só termo do processo e correção de previsão de data, sem nada de "depende do caso": rascunho na fila (`escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-cliente-com-ia.md`, `tipo: cliente-com-ia`), com `revisor: pendente` e, no cabeçalho, o que o advogado precisa conferir na explicação (o termo, a fase). O texto ao cliente não leva marcação.
3. **A conferência do advogado não bloqueia.** O `revisor-de-suporte` lê o rascunho e, quando a explicação do termo ou da fase precisa do olho do advogado, grava `revisor: conferir: <o que conferir>` (regra 4 dele). O item aparece na fila de aprovação normalmente, com o aviso; a pessoa só aprova depois de o advogado conferir o ponto indicado. Bloqueio fica para o que não pode sair de jeito nenhum: confirmar o que a IA disse sem conferência, prometer data, tese ou valor.
4. Tese, direito novo, prazo ou valor: nada na fila; "PARA DECIDIR" com a frase do que o cliente perguntou.
5. Grave a linha do histórico e a pergunta nova no arquivo do tipo, com situação `nova`. Não envie nada.

### Modo adaptar
Leia `nicho.md` e as perguntas que chegaram. Reescreva as perguntas-base e os erros comuns para o nicho, com as palavras do cliente, cada mudança `[ALTERADO]`. Grave só com o ok, uma versão nova por arquivo.

### Último passo. Aprender
Pergunte: "Você explicaria isso de outro jeito?". Cada correção vira uma regra curta ("Concluso: não usar 'mesa do juiz', usar 'o processo foi para o juiz olhar'") e entra nos aprendizados com o ok. Explicação de termo aprovada: ofereça gravar no `glossario-do-cliente.md`.

## 4. Exemplo resolvido (mensagem 4 dos casos fictícios)

Helena (C-2026-0007, BPC da mãe, fase `protocolado`), sexta 10h: "Olhei no site do tribunal e tá escrito 'concluso para despacho'. O que isso quer dizer? Perguntei pro ChatGPT e ele disse que o juiz já vai decidir essa semana."

Pedaços: termo do processo (explicar); previsão de data (errada: corrigir, sem outra data). Nada de tese ou valor.

Resposta (A, a advogada lê antes):
```
Oi, Helena! Recebi, e foi bom você trazer isso para cá.

"Concluso para despacho" quer dizer que o processo foi para o juiz olhar e dizer qual é o próximo passo. Nesse momento, não é a decisão final do pedido da sua mãe.

Sobre a previsão: a IA não enxerga o processo nem a agenda do juiz, então ela não tem como saber a data. Ninguém tem, nem a gente. O tempo depende da vara.

Enquanto isso, a gente acompanha o processo. Assim que o juiz der o próximo passo, eu te aviso e explico o que muda. Se ver mais alguma coisa no site, pode me mandar aqui primeiro.
```
Registro: `| 2026-04-10 10h00 | whatsapp | filha (autorizada) | trouxe resposta de IA sobre concluso para despacho; explicado |`. No ciclo, este rascunho vai para a fila com `revisor: conferir: a advogada confere a explicação de "concluso para despacho"`, e não fica bloqueado. Pergunta entra em `perguntas-do-caso-bpc.md` ("O que quer dizer concluso?"), que já tem resposta aprovada se o escritório usou o modo antes da pergunta.

O que não pode sair: "deve sair em breve", "costuma levar X dias", "a IA errou feio".

## 5. Formato da saída

```
CLIENTE COM IA · [CÓDIGO] · [fonte: IA | print do tribunal | vídeo | outro] · [data]
O que o cliente quer saber: [uma frase]
Pedaços: [afirmação] → certo | incompleto | errado | depende do caso
Resposta (A, [quem lê]): "[mensagem]"
Para o advogado (H): [o que depende do caso, ou "nada"]
Registro: [linha do histórico] · pergunta nova em perguntas-do-caso-[tipo].md
Antes de enviar: [o que está CONFERIR]
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Perguntas do caso por tipo | `escritorio/04-base/relacionamento-com-o-cliente/perguntas-do-caso-<tipo-de-caso>.md` |
| Termo explicado e aprovado | `escritorio/04-base/relacionamento-com-o-cliente/glossario-do-cliente.md` |
| Linha do histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Resposta no ciclo | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-cliente-com-ia.md` |
| Correções | `escritorio/04-base/comum/aprendizados-experiencia.md` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: tudo no chat, com o caminho de cada arquivo.

## 7. Solo e equipe

**Solo:** o titular aprova as perguntas do caso uma vez por tipo e depois responde quase tudo com elas. Uma vez por mês, olhe as "perguntas que chegaram": a que se repetiu três vezes merece resposta aprovada.

**Equipe:** a secretária responde termo e previsão de data com as respostas aprovadas; tese, prazo e valor vão para o advogado. Quem atende anota a pergunta nova no arquivo do tipo, no dia em que ela chega.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "A IA está errada, esquece isso" | O cliente se sente ridicularizado e para de perguntar | Acolher primeiro (regra fixa 1) |
| Confirmar o que a IA disse | Promessa que o escritório não fez | Regra fixa 2 e o passo 3 |
| Trocar a data da IA por outra data | Nova promessa de prazo | Nenhuma data de decisão na resposta |
| Responder tese por mensagem | Orientação sem análise do caso | Tese e direito novo vão ao advogado (H) |
| Repetir o número do processo do print | Dado exposto sem necessidade | Passo 1 |
| A mesma pergunta respondida dez vezes de dez jeitos | Retrabalho e respostas diferentes | Perguntas do caso aprovadas por tipo |

## 9. Próximo passo

- Movimentação que precisa de tradução: `status-para-o-cliente` (se instalada).
- Perguntas do caso aprovadas: usar na `boas-vindas-do-cliente`, na `resumo-mensal-do-caso` e na `pagina-do-caso` (se instaladas); sem elas, mande a resposta aprovada quando a pergunta chegar.
- Pergunta que vira reclamação: `reclamacao-e-recuperacao` (se instalada) ou ligação do advogado.

## Referências desta habilidade

- `references/erros-comuns-por-area.md`: os erros que o cliente mais traz da internet, por área, com o que dizer no lugar, todos `[CONFERIR]`. Leia no passo 3 e no modo antes da pergunta.
- `references/perguntas-base-por-tipo.md`: as perguntas que o cliente faz por tipo de caso e fase, com respostas-base. Leia no modo antes da pergunta.
- `assets/modelo-perguntas-do-caso.md`: o formato do arquivo `perguntas-do-caso-<tipo>.md`.
