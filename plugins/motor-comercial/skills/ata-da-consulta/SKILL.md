---
name: ata-da-consulta
description: >
  Depois da consulta inicial, transforma as anotações do advogado, o ditado transcrito ou a
  transcrição autorizada em ata: fatos, o que o cliente quer, caminhos explicados, riscos ditos,
  documentos pendentes, decisões e próximo passo, valor conversado. Escreve a mensagem de resumo ao
  cliente (alguém lê antes de enviar), separa os dados para a proposta de honorários, atualiza os
  documentos pedidos antes do contrato e registra consulta-feita, ou sem-caso só com o advogado.
  Roda a pedido, no ciclo do agente (anotações deixadas na entrada) e no modo adaptar. Use quando o
  advogado disser "faz a ata da consulta", "acabei a consulta do Paulo, anota", "resume a reunião
  para o cliente", "o que ficou combinado?", "transforma essa transcrição em ata", "prepara os dados
  da proposta". Não use para preparar a consulta (use roteiro-da-consulta) nem para montar a
  proposta (use proposta-de-honorarios).
---

# Ata da consulta

> A consulta acabou. O que foi dito, o que foi combinado e o que cada um ficou de fazer precisa sair da cabeça do advogado e ir para o papel no mesmo dia, antes que vire "eu achei que você tinha dito".

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

A consulta terminou às 14h45. A advogada tem quatro linhas no caderno. O cliente saiu achando que a proposta chega amanhã; ela lembra de ter dito "até sexta". Na terça seguinte, ninguém sabe quem ficou de mandar o quê, e o cliente escreve: "e aí, vocês desistiram de mim?".

**Regras fixas desta habilidade:**
1. A ata registra o que foi dito. O que não está nas anotações ou na transcrição fica `[A CONFIRMAR]`; a IA não completa fato, data nem valor.
2. Caminhos e riscos entram como o advogado explicou. A IA não acrescenta tese, chance de ganho, avaliação do caso nem cálculo.
3. A mensagem de resumo ao cliente é A: alguém lê antes de enviar. Ela não traz nada que não tenha sido dito na consulta, nem promessa, nem estimativa de valor ou de prazo.
4. `sem-caso` e `perdido` só com o advogado. Se a notícia de que não há caso ainda não foi dada, ela vai por ligação, nunca por mensagem.
5. Transcrição só de consulta gravada com o consentimento do cliente. O arquivo guarda a ata, não a transcrição inteira, e dado sensível entra no mínimo necessário.

## 1. Quando usar

**Use quando:**
- A consulta acabou e o advogado quer a ata, com os combinados.
- Há uma transcrição autorizada, ou o advogado ditou um áudio na saída e quer isso organizado.
- É preciso mandar ao cliente o resumo do que foi conversado.
- A proposta vai ser montada e os dados da consulta precisam estar prontos.
- O `agente-comercial` achou anotações de consulta na pasta de entrada, ou a `adaptar-comercial` chamou no modo "adaptar".

**Não use quando:**
- A consulta ainda não aconteceu: use `roteiro-da-consulta`.
- O pedido é a proposta em si: use `proposta-de-honorarios`, que lê os dados desta ata.
- Quem conversou já é cliente e o assunto é o andamento do caso: o registro vai para o histórico do cliente, pelo motor-experiencia (se instalado); sem ele, a pessoa que cuida do caso anota.
- O pedido é o controle de documentos do caso depois do contrato: é da `checklist-de-documentos` do motor-experiencia (se instalado).

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir) e `aprendizados-comercial.md`. Aprendizado da `ata-da-consulta` vale antes do padrão desta habilidade.
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Quem fez a consulta?". Para a mensagem, use o tratamento que ele indicar e ofereça gravar no fim.
3. **Leia o arquivo da consulta** (`escritorio/07-operacao/comercial/consultas/<codigo>-AAAA-MM-DD.md`): o briefing diz o que se sabia antes, o que estava em aberto e quais documentos foram pedidos. Sem arquivo, a ata cria o arquivo com o cabeçalho.
4. **Leia a linha do contato** em `escritorio/07-operacao/comercial/contatos.csv`.
5. **Conta, consentimento e treino.** Ata tem dado de cliente: só em conta profissional ou de equipe. Se a entrada é transcrição, pergunte: "O cliente autorizou a gravação ou a transcrição?". Sem o sim, peça as anotações. Com casos fictícios, tudo grava em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** C: `quem_faz_a_consulta`.
- **Melhora:** C: `modelo`, `valores_de_referencia`.

Campo que falta e a tarefa pede: pergunte aquele campo, uma vez, e ofereça gravar. `valores_de_referencia` serve só para apontar se o valor conversado destoa da política; a ata registra o valor dito e nunca sugere outro. O tom e a assinatura da mensagem vêm da ficha do escritório, como em toda mensagem.

## 3. Fluxo

### Modos

| Modo | Entrada | Como a habilidade trabalha |
|---|---|---|
| Anotações | Texto curto, tópicos, foto legível do caderno | Organiza nas seções e pergunta o que falta |
| Ditado | Áudio do advogado, já transcrito | Separa fatos de comentários do advogado |
| Transcrição | Transcrição autorizada da reunião (conferir na configuração da ferramenta) | Tira os trechos que importam, com quem disse, e descarta o resto |
| Entrevista | Nada escrito | Pergunta ao advogado, uma de cada vez, as perguntas do passo 3 |
| No ciclo | Anotações em `07-operacao/comercial/entrada/`, com o código no nome | Ata em rascunho e mensagem na fila, nada no chat (passo 9) |
| Adaptar | `nicho.md` | Mensagem de resumo e perguntas de completar reescritas para o nicho (passo 10) |

**Modo direto:** o advogado cola as anotações e diz "ata, mensagem e dados da proposta". Execute tudo, mostre e pergunte só o que falta.

### Passo 1. Receber e limpar
- Troque dado identificável que a ata não precisa pela marcação das regras (`[DOC]`, `[PROCESSO]`, `[ENDEREÇO]`). Avise em uma linha.
- Dado de saúde: só o que a ata precisa ("tem doença que impede o trabalho desde 2025"), nunca o laudo.
- Relato de violência: uma linha na ata ("relato sensível, conduzido pelo advogado") e nada daquele trecho em mensagem ou em outro arquivo.

### Passo 2. Separar quem disse o quê
Marque cada informação com a origem: "segundo o cliente", "explicado pelo advogado", "combinado". Assim o relato do cliente não vira fato confirmado e uma hipótese do advogado não vira promessa.

### Passo 3. Completar o que falta (uma pergunta por vez)
Só o que as anotações não trazem, nesta ordem:
1. "O que o cliente quer, em uma frase?"
2. "Quais caminhos você explicou?"
3. "Que riscos você disse a ele?"
4. "Você recomendou algum caminho? Ele escolheu?"
5. "Que documentos ficaram faltando?"
6. "O que ficou combinado: quem faz o quê, até quando?"
7. "Falaram de honorários? O que foi dito: modelo, valor, forma de pagamento?"
8. "Como você vê o resultado: vai para proposta, o cliente vai pensar, ou não há caso?"

"Não lembro" ou "não falamos": `[A CONFIRMAR]` ou "não tratado na consulta".

### Passo 4. Montar a ata
No formato da seção 5. Uma página, duas no máximo. Datas em AAAA-MM-DD. Conflito entre anotação e transcrição: mostre os dois e pergunte qual vale.

### Passo 5. Definir o resultado
Pela tabela da seção 4. Para `sem-caso` ou `perdido`, pergunte: "Confirma que não há caso? A notícia já foi dada ao cliente?". Se não foi, a mensagem de resumo não sai: o próximo passo é a ligação do advogado.

### Passo 6. Escrever a mensagem de resumo (A)
Parta do modelo de chave `resumo-depois-da-consulta` da biblioteca comercial (`escritorio/04-base/comercial/biblioteca-comercial.md`), no tom da ficha, e preencha com o que a ata diz, no formato da seção 6. Biblioteca antiga, sem essa chave: use a seção 6 e ofereça acrescentar o modelo pela `mensagens-comerciais` (se instalada; sem ela, no fim da biblioteca, sem renumerar). Quem lê antes de enviar: o advogado que fez a consulta, porque a mensagem tem conteúdo jurídico.

### Passo 7. Separar os dados para a proposta
Resultado "vai para proposta": monte o bloco "Dados para a proposta" (seção 7), lido pela `proposta-de-honorarios` (se instalada). Sem ela, o bloco fica no arquivo e o advogado escreve a proposta a partir dele.

### Passo 8. Gravar e registrar
1. Grave a ata como "## Ata" no arquivo da consulta, depois do briefing. Ata refeita: "Ata v2, AAAA-MM-DD", com a anterior resumida abaixo.
2. Atualize a seção "Documentos pedidos antes do contrato" do mesmo arquivo: o que chegou na consulta, o que ficou pendente, com quem e até quando. Depois do `fechado`, a `passagem-para-o-caso` (se instalada) leva os pendentes para o controle do caso no motor-experiencia.
3. Proponha a atualização da linha no `contatos.csv` pela tabela da seção 4. Mostre e grave com o ok.

### Passo 9. No ciclo (chamada pelo agente)
1. Não mostre nada no chat. Para cada arquivo de anotações em `escritorio/07-operacao/comercial/entrada/` com um código de contato em `consulta-agendada` ou `consulta-feita`, monte a ata e grave no arquivo da consulta com o título "## Ata (rascunho do ciclo, o advogado revisa)".
2. A mensagem de resumo vira rascunho na fila: `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-resumo-depois-da-consulta.md`, no formato de `../../docs/agentes-e-fila.md`, com `tipo: resumo-depois-da-consulta`, `revisor: pendente` e, no `motivo`, "ata em rascunho do ciclo; o advogado revisa a ata antes de aprovar". Passa pelo `revisor-comercial`.
3. O agente não move a etapa (`consulta-feita` é da pessoa ou desta habilidade a pedido) e nunca marca `sem-caso` ou `perdido`. No registro, só as colunas que `../../docs/funil.md` permite ao agente (regra 11). Lacunas e resultado sugerido vão para "PARA DECIDIR" no resumo do dia.
4. Transcrição sem registro de consentimento, ou anotação com relato sensível: nada de rascunho. Vai para "PESSOA AGORA", e o `proximo_passo` passa a começar por `pessoa agora:` (marcador de pessoa, `funil.md`, regra 4), com a frase do que falta ("pessoa agora: confirmar o consentimento da gravação").
5. **Saída de PESSOA AGORA.** Depois que o advogado falou com o cliente, o comando `fila` pergunta "Já falou? O que ficou combinado?" e troca o `proximo_passo` que começa com `pessoa agora:` pelo combinado, com data, e registra no arquivo da consulta (`agentes-e-fila.md`). A pedido, esta habilidade faz o mesmo na hora de gravar a ata revisada. Sem isso, o item volta ao topo do resumo seguinte.

### Passo 10. Modo "adaptar" (chamada pela adaptar-comercial)
1. Leia `escritorio/04-base/comum/nicho.md`.
2. Reescreva o modelo da mensagem de resumo (seção 6) com o vocabulário de "Como ele fala" e os cuidados do nicho (por exemplo, cliente com pouca leitura: frases mais curtas e oferta de explicar por ligação).
3. Proponha as "Lacunas típicas do nicho": as perguntas de completar (passo 3) que o nicho pede além das oito (por exemplo, no previdenciário rural, "Quem pode confirmar o trabalho na roça?").
4. Mostre cada mudança marcada `[ALTERADO]` ou `[NOVO]`. Com o ok, o texto novo substitui o do modelo de chave `resumo-depois-da-consulta` na biblioteca, pela `mensagens-comerciais` no modo adaptar (se instalada; sem ela, troque só o texto-modelo daquela chave e registre em "Mudanças"; biblioteca sem a chave: acrescente o modelo no fim, sem renumerar). A chave nunca muda. As lacunas vão para a seção "Perguntas por tipo de caso" do roteiro da área, pela `roteiro-da-consulta`. Devolva a lista do que mudou.

### Passo 11. Aprender
Pergunte: "Alguma coisa na ata ou na mensagem você faria diferente?". Cada correção vira regra curta (por exemplo, "Mensagem de depois da consulta: nunca repetir o valor dos honorários, que vai só na proposta") e, com o ok, entra em `aprendizados-comercial.md`. Se a mesma lacuna aparece em várias atas, ofereça levar a pergunta para o roteiro da área pela `roteiro-da-consulta`, modo B.

## 4. O resultado da consulta e o funil

| Resultado | Quando | `etapa` | `proximo_passo` | Quem confirma |
|---|---|---|---|---|
| Vai para proposta | Há caso e o cliente quer a proposta | `consulta-feita` | "enviar proposta" até a data combinada | a IA sugere |
| Cliente vai pensar | Há caso, o cliente não decidiu | `consulta-feita` | "retorno combinado" na data dita na consulta | a IA sugere |
| Depende de documento | O caminho depende de ver um papel | `consulta-feita` | "receber documentos" | a IA sugere |
| Sem caso | Não há ação viável, segundo o advogado | `sem-caso` | "nenhum" | só o advogado |
| Desistiu na consulta | O cliente disse que não segue | `perdido`, com `motivo_perda` e `perdido_na_etapa` = `consulta-feita` | "nenhum" | só o advogado |
| Não aconteceu | O cliente faltou | `nao-compareceu` | "oferecer nova data" | a pessoa |

Atualize também `responsavel`, `data_proximo_passo` e `atualizado_em`. Valor de honorário só vai para `valor_proposta` quando a proposta for enviada, pela `proposta-de-honorarios`.

## 5. Formato da ata

```
## Ata
Consulta: [CÓDIGO] · [AAAA-MM-DD HH:MM] · [presencial | online] · [duração]
Quem fez: [função] · Presentes: cliente[, acompanhante e relação]
Gravação ou transcrição: autorizada | não autorizada | não houve
Fonte da ata: anotações | ditado | transcrição · Revisada por: [A CONFIRMAR]

1. Fatos (segundo o cliente)
2. O que o cliente quer
3. Caminhos explicados (como o advogado explicou)
- [Caminho]: o que é · o que precisa · tempo dito (se dito) · custo dito
- Recomendação do advogado (se houve) e escolha do cliente (se houve)
4. Riscos ditos ao cliente
5. Documentos (entregues na consulta · pendentes, com quem e até quando)
6. Decisões e próximo passo (cliente · escritório · próxima conversa)
7. Valor conversado (ou "honorários não tratados na consulta")
8. Alertas para o advogado (prazo aparente [CONFERIR] · vulnerabilidade ·
   conflito a conferir · expectativa diferente do que foi dito)
9. Lacunas [A CONFIRMAR]
Resultado: vai para proposta | vai pensar | depende de documento | sem caso (advogado) | desistiu (advogado)
```

- Estimativa que o advogado deu na consulta entra como fala dele, entre aspas, com "estimativa dita na consulta". Ela não vai para a mensagem.
- Nada de adjetivo sobre o caso ("caso forte", "caso fraco").
- Terceiros só pela função ("a ex-empregadora", "o ex-marido"), a não ser que o advogado peça o nome.

## 6. A mensagem de resumo ao cliente (A)

```
Oi, {NOME}, obrigada pela conversa de hoje.

Para você ter tudo por escrito, o que combinamos:

O que conversamos: [DA ATA: uma ou duas frases simples sobre os caminhos explicados, sem promessa].

O que fica com você: [DA ATA: documentos ou decisão], até [DA ATA: data].
O que fica com a gente: [DA ATA: proposta ou análise], até [DA ATA: data].

Se lembrar de alguma coisa que não contou na consulta, pode mandar por aqui.

[ASSINATURA]
```

- Uma ideia por parágrafo, termo técnico explicado na primeira vez.
- Sem valor de honorário (vai na proposta, por escrito), a não ser que o advogado peça.
- Sem estimativa de valor a receber, de chance ou de prazo de decisão.
- Cliente vai pensar: sem pressão. "Fica à vontade para pensar. Se surgir alguma dúvida, é só escrever."
- Sem caso: só depois da ligação do advogado, e só se ele quiser registro escrito.
- É o texto do modelo `resumo-depois-da-consulta` da biblioteca. Os trechos `[DA ATA: ...]` a habilidade preenche com a ata; se a ata não tem a informação, o trecho sai e a lacuna vai para o cabeçalho interno "Antes de enviar", nunca para o texto que vai ao cliente. O `{NOME}` a habilidade preenche com o `nome_curto` do registro; sem ele, fica entre chaves para quem envia. Também entre chaves, o que quem envia escolhe na hora (por exemplo, `{LINK DA PASTA PARA OS DOCUMENTOS}`, se o escritório manda um).

## 7. Dados para a proposta

```
### Dados para a proposta · [CÓDIGO]
Cliente: [nome curto] · Área: ... · Tipo de caso: ...
Serviço conversado: [nas palavras do advogado]
Fase ou escopo: [ex.: tentativa de acordo; ação em primeira instância] [A CONFIRMAR se não foi dito]
O que ficou de fora (se dito): ...
Modelo de honorário conversado: [fixo | êxito | misto | mensal | não tratado]
Valor dito na consulta: [valor dito pelo advogado | nenhum]
Forma de pagamento conversada: [ou "não tratada"]
Despesas mencionadas: [ou "não tratadas"]
Prazo combinado para enviar a proposta: [DATA]
Pendências antes da proposta: [ex.: ver o extrato do FGTS]
Consulta paga e abatimento: [conforme a ficha e o que foi dito]
```

Valor que não foi dito fica "nenhum". A ata não sugere valor a partir de `valores_de_referencia`; se o valor dito destoa da política, aponte como alerta, sem corrigir.

## 8. Casos-limite

| Situação | O que fazer |
|---|---|
| Cliente e acompanhante dizem coisas diferentes | Registre as duas falas, com quem disse |
| Casal na mesma consulta (divórcio consensual) | Registre o que cada um disse e o que os dois combinaram; a mensagem vai para quem o advogado indicar |
| Transcrição com nome, valor ou data trocados | `[A CONFIRMAR]`, nunca correção por conta própria |
| O advogado disse "seu caso é bom" | Registre como fala dele; a mensagem não repete; ofereça um aprendizado para o roteiro |
| Cliente pediu desconto na consulta | Registre em "Valor conversado"; a resposta é do advogado, na proposta |
| Cliente trouxe resposta de IA | Registre em "Alertas" o que ele espera; a mensagem não confirma nem desmente |
| Ata pedida dias depois | Avise que a memória pode falhar, marque mais `[A CONFIRMAR]` e sugira fazer no mesmo dia |

## 9. Exemplo resolvido (Escritório Modelo, caso fictício)

Caso 2 de `../../docs/casos-ficticios.md`: Paulo, C-2026-0002, demissão sem justa causa, verbas não pagas. Consulta online em 2026-03-11, 14h, 40 minutos, com a advogada titular. Anotações dela:

> "saiu 09/03, sem justa, não pagaram nada, FGTS não liberado. 4 anos de casa. hora extra todo dia, sem ponto. expliquei: tentar acordo antes ou ação. risco: prova da hora extra (só colegas). falta TRCT (diz que não recebeu), extrato FGTS. proposta até sexta. falou que outro advogado cobra 30% no fim."

A ata sai com: fatos (saída em 2026-03-09, sem justa causa segundo o cliente, quatro anos na empresa, jornada além do horário sem controle de ponto); o que quer (receber o que não foi pago); caminhos explicados (tentativa de acordo; ação); risco dito (a prova da jornada depende de testemunhas); pendentes (extrato do FGTS com o cliente até 2026-03-12; termo de rescisão, que o cliente diz não ter recebido `[A CONFIRMAR]`); próximo passo (proposta até sexta, 2026-03-13); valor conversado ("honorários não tratados; o cliente mencionou a proposta de outro profissional"); alertas (prazo aparente para a ação `[CONFERIR]`; perda recente do emprego).

A mensagem diz o que foi conversado em duas frases, pede o extrato até quinta e avisa que a proposta chega até sexta. Ela não comenta o outro profissional nem o percentual: isso fica para a advogada, na proposta, pela `objecoes-comerciais` (se instalada). Registro: `consulta-feita`, `proximo_passo` "enviar proposta", `data_proximo_passo` 2026-03-13. A ata completa está em `references/exemplo-ata-completa.md`.

## 10. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Ata e dados para a proposta | `escritorio/07-operacao/comercial/consultas/<codigo>-AAAA-MM-DD.md`, seções "## Ata" e "### Dados para a proposta" (o mesmo arquivo do briefing) |
| Documentos pedidos antes do contrato | No mesmo arquivo, seção "Documentos pedidos antes do contrato" |
| Mensagem de resumo (chave `resumo-depois-da-consulta`) | No chat, para o advogado ler e enviar; no ciclo, `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-resumo-depois-da-consulta.md` |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `etapa`, `responsavel`, `proximo_passo`, `data_proximo_passo`, `motivo_perda` e `perdido_na_etapa` (se perdido), `atualizado_em` |
| Modelo de resumo adaptado ao nicho | `escritorio/04-base/comercial/biblioteca-comercial.md`, chave `resumo-depois-da-consulta` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino | `escritorio/07-operacao/_treino/comercial/` |

A transcrição original fica onde a ferramenta guardou ou no sistema do escritório, e não é copiada para a pasta. Sem pasta aberta: entregue a ata, a mensagem e a linha do registro no chat, com o caminho de cada arquivo.

## 11. Solo e equipe

**Solo:** o titular dita dois minutos de áudio logo depois da consulta, ainda na cadeira, e a ata sai dali. A mensagem ele lê no mesmo dia, no horário fixo de responder mensagens. O que não couber no dia vira `[A CONFIRMAR]`, nunca memória.

**Equipe:** quem fez a consulta dita ou anota; a secretária roda a habilidade, e o advogado revisa a ata e a mensagem antes de sair. Quem monta a proposta recebe só o bloco "Dados para a proposta". Atas que chegam sempre sem "valor conversado" ou sem "próximo passo" pedem reforço no fechamento do roteiro.

## 12. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Ata de memória dias depois | Combinado esquecido ou trocado | Ditado na saída e ata no mesmo dia |
| Relato do cliente registrado como fato | Proposta ou peça com base errada | "Segundo o cliente" e "explicado pelo advogado" |
| IA acrescentando tese ou chance | Avaliação que o advogado não fez | Regra fixa 2 |
| Mensagem com estimativa de valor ou prazo | Promessa por escrito | Estimativa fica só na ata |
| Notícia de "não há caso" por mensagem | Cliente recebe notícia ruim sozinho | `sem-caso` só com o advogado, depois da ligação |
| Documento pendente que ninguém cobra | Proposta atrasa, contato esfria | Seção "Documentos pedidos antes do contrato" com prazo e responsável |
| Transcrição inteira guardada na pasta | Dado de cliente demais | Só a ata fica no arquivo |
| Gravar sem consentimento | Quebra de confiança e problema de dados | Pergunta do consentimento antes; no ciclo, para |

## 13. Próximo passo

- Vai para proposta: `proposta-de-honorarios`, que lê o bloco "Dados para a proposta".
- Cliente vai pensar ou não respondeu: `follow-up` (se instalada), nos prazos da ficha; sem ela, um retorno na data dita na consulta.
- Lacuna que se repete: `roteiro-da-consulta`, modo B.
- Contrato assinado: `passagem-para-o-caso` (se instalada) leva os documentos pendentes e os combinados para o caso; sem ela, a pessoa copia a seção de documentos para quem cuida do caso.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

- `references/exemplo-ata-completa.md`: a ata completa do exemplo da seção 9, com os documentos pedidos antes do contrato, a mensagem e os dados para a proposta. Leia na primeira vez que rodar a habilidade e quando o advogado pedir "me mostra como fica".
