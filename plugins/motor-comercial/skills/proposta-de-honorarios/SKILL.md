---
name: proposta-de-honorarios
description: >
  Monta a proposta de honorários de cada contato a partir da ata da consulta e da política de
  honorários do escritório, que ela cria por entrevista na primeira vez. A proposta traz o que
  está incluído e o que não está, as etapas, os valores e os cenários de pagamento, as despesas
  e a validade, sem promessa de resultado. Conferências e pendências ficam num cabeçalho interno
  "Antes de enviar", que o script não leva para o .docx e que avisa enquanto a proposta não
  estiver pronta. Escreve a mensagem de envio e registra no funil. Use quando o advogado disser
  "monta a proposta", "faz a proposta da consulta de ontem", "manda o valor por escrito", "cria
  nossa política de honorários", "nova versão com mais parcelas". Não use para a minuta do
  contrato depois do aceite (use contrato-de-honorarios) nem para responder "achei caro" (use
  objecoes-comerciais).
---

# Proposta de honorários

> A proposta responde por escrito ao "e quanto fica?": o que está incluído, o que não está, quanto custa, como se paga e até quando vale. O valor é do advogado. A IA monta o resto.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-comercial.md`. Funil: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Fila: `../../docs/agentes-e-fila.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

A consulta acabou às 17h e a cliente pediu "me manda o valor por escrito". Três dias depois a proposta sai num áudio: "fica uns tantos mil, dá para parcelar". Ela não sabe se o recurso está incluído nem até quando o valor vale. Quando a proposta finalmente sai por escrito, vai com um "[CONFERIR]" no meio do parágrafo de honorários.

**Regras fixas desta habilidade:**
1. Nenhum valor sai da cabeça da IA. Valor vem da política, da ficha comercial ou do advogado nesta conversa. Sem valor, o lugar fica `[A DEFINIR]` e a proposta não sai.
2. Nada de promessa de resultado, de chance de ganho ou de prazo de decisão. O êxito aparece como forma de cobrança, nunca como previsão.
3. Toda proposta tem as duas listas: o que está incluído e o que não está.
4. Conferências e pendências ficam no cabeçalho interno "Antes de enviar". O texto que vai ao cliente não leva marcação nenhuma.
5. Valor final, condição fora da política e envio são de uma pessoa (H). A habilidade monta e mostra; quem aprova marca o ok no cabeçalho interno.

## 1. Quando usar

**Use quando:**
- A consulta aconteceu e o advogado quer mandar a proposta.
- O escritório ainda não tem política de honorários escrita (modo política).
- O cliente pediu ajuste e o advogado já decidiu o que muda (nova versão).
- O agente do ciclo encontrou uma proposta aprovada e pronta, sem mensagem de envio (modo no ciclo).
- A `adaptar-comercial` (se instalada) pediu o modelo de proposta no jeito do nicho (modo adaptar).

**Não use quando:**
- A proposta foi aceita e o próximo passo é o contrato: use `contrato-de-honorarios` (se instalada).
- O cliente respondeu "achei caro", "vou pensar" ou "o outro cobra menos": use `objecoes-comerciais` (se instalada).
- A proposta saiu e a pessoa sumiu: use `follow-up` (se instalada).
- Ainda não houve consulta e a pessoa quer saber o preço por mensagem: a resposta é o convite para a consulta (`triar-contato`).

## 2. Antes de começar

1. **Leia as fichas:** `escritorio/04-base/comum/ficha-do-escritorio.md` e `escritorio/04-base/comum/ficha-comercial.md` (seções 2, Consulta, e 3, Honorários).
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`), se existir. Ele dá as palavras do cliente para "O que você nos trouxe" e as etapas típicas de cada tipo de caso.
3. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado de proposta vale antes do padrão desta habilidade.
4. **Leia a política** (`escritorio/04-base/comercial/politica-de-honorarios.md`). Não existe: modo política primeiro. Se o advogado quiser só esta proposta agora, pergunte os campos que faltam e ofereça criar a política depois.
5. **Leia a fonte da consulta:** a ata ou o briefing em `escritorio/07-operacao/comercial/consultas/<codigo>-AAAA-MM-DD.md` (a `ata-da-consulta` deixa ali o trecho "Dados para a proposta"). Sem ata, peça o resumo (passo B1).
6. **Procure o modelo do escritório** em `escritorio/04-base/comercial/modelos/modelo-proposta.md`. Não existe: use `assets/modelo-proposta.md`.
7. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`) e as propostas anteriores do mesmo código em `escritorio/07-operacao/comercial/propostas/`, para saber a versão.
8. **Conta de IA.** A proposta tem dado de cliente: só em conta profissional ou de equipe. Em conta pessoal, só caso fictício, gravado em `escritorio/07-operacao/_treino/comercial/propostas/`. A proposta usa o primeiro nome; nome completo e documento ficam no contrato, preenchidos no sistema do escritório.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `cidade_uf` · C: `modelo`, `formas_de_pagamento`, `validade_da_proposta`.
- **Melhora:** C: `valores_de_referencia`, `entrada_e_parcelas`, `despesas`, `quem_aprova_a_proposta`, `abate_dos_honorarios`, `diferenciais_verdadeiros`.

O tom, o tratamento e a assinatura saem da ficha do escritório, como em toda habilidade. Campo que falta e a proposta pede: pergunte aquele campo, uma vez, siga com `[A PREENCHER]` se o advogado não souber e ofereça gravar na ficha e na política no fim.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Política | Primeira vez, sem `politica-de-honorarios.md` | Entrevista com o advogado | A política e a seção 3 da ficha comercial |
| B. Proposta, a pedido | Um contato com consulta feita | Ata ou briefing, e a política | Proposta .md e .docx, mensagem de envio no chat, linha do funil |
| C. Direto | O advogado manda tudo ("proposta para a C-2026-0001, fixo de tanto em 5 vezes, só a fase administrativa") | O pedido e a fonte da consulta | O mesmo do modo B, perguntando só o que falta |
| D. Nova versão | O cliente pediu ajuste e o advogado decidiu | A versão anterior e a decisão | `-proposta-v<n+1>` (a anterior fica intacta) |
| E. No ciclo | O `agente-comercial` chama | As propostas da pasta e o registro | Rascunho da mensagem de envio na fila; nada no chat |
| F. Adaptar | A `adaptar-comercial` chama | O nicho e o modelo atual | Modelo de proposta reescrito, com `[ALTERADO]`, gravado só com o ok |

### A. Política de honorários (primeira vez)

Diga: "Vou montar a política com o que vocês já praticam. O que não tiver número fica para decidir caso a caso, e eu não preencho sozinho." Pergunte, uma de cada vez, pulando o que a ficha comercial já tiver:

1. "Como vocês costumam cobrar: valor fixo, percentual no êxito, misto ou mensal? Muda conforme a área?"
2. "Para os casos que mais chegam, vocês já têm um valor de referência? Vamos um por um." (use `casos_mais_comuns`; um tipo de caso por pergunta; sem número, "caso a caso")
3. "Quando há êxito: o percentual incide sobre o quê e quando se paga?"
4. "Entrada e parcelas: qual a entrada mínima e em quantas vezes no máximo? Tem juros no parcelamento?"
5. "Quais formas de pagamento vocês aceitam?"
6. "Despesas (custas, perícia, cópias, deslocamento): quem paga e como o cliente fica sabendo antes?"
7. "A proposta vale por quantos dias corridos?"
8. "A consulta é abatida dos honorários quando a pessoa fecha?"
9. "Quem aprova a proposta antes de sair? E até onde quem atende pode ajustar sem perguntar?"
10. "Há casos que vocês fazem com valor reduzido ou sem cobrar? Qual o critério?"
11. "A tabela de honorários da seccional: vocês usam como piso? Eu deixo a referência para conferir na tabela vigente, sem copiar valores."

Monte com `references/politica-de-honorarios-modelo.md`, mostre, ajuste e grave com o ok. Depois pergunte: "Quer que eu atualize a seção 3 da ficha comercial com estes campos?". Política e ficha divergentes: mostre as duas e pergunte qual vale.

### B. Proposta para um contato (a pedido)

**Passo 1. A fonte.** Confirme o código e leia a ata. Sem ata, pergunte: "Me conta em três linhas o que ficou combinado na consulta: o que a pessoa quer, o que o escritório vai fazer e o que ficou de fora."

**Passo 2. O escopo.** Pergunte: "O trabalho vai até onde: só a fase administrativa, até a sentença, ou inclui recurso e a fase de receber o valor?". Escreva o incluído em itens com verbo e objeto (seção 4) e proponha a lista do não incluído para o advogado confirmar. Etapas em linguagem simples, sem prazo prometido.

**Passo 3. Os valores.** Procure o tipo de caso na política.
- Tem referência: mostre o ponto de partida com a conta e pergunte: "Vale este valor para este caso ou você ajusta?".
- Não tem: pergunte "Qual o valor para este caso?". Não sugira número.
- Monte até três cenários, todos dentro da política (seção 5). Faça a conta das parcelas e mostre o arredondamento.
- Consulta abatida (`abate_dos_honorarios = sim`): mostre o abatimento na conta.

**Passo 4. Despesas, validade e próximos passos.** Despesas como a política diz. Validade: data da proposta mais `validade_da_proposta`, escrita como data. Próximos passos: como aceitar e o que vem depois.

**Passo 5. O cabeçalho interno.** Preencha o "Antes de enviar" do modelo (seção 6): quem aprova, a fonte, as conferências e as pendências. Todo `[CONFERIR]` (tabela da seccional, limite do êxito) e todo valor ainda sem decisão entram ali como item `- [ ]`. No texto do cliente, valor sem decisão fica como `[A DEFINIR]` no lugar dele, e o script acusa e não cria o .docx até alguém decidir.

**Passo 6. Mostrar e aprovar.** Mostre a proposta inteira e o "Antes de enviar" por cima. Diga quem aprova (`quem_aprova_a_proposta`). Quem aprova marca `[x]` em cada conferência que fez.

**Passo 7. Gravar e gerar o .docx.** Com o ok, grave `escritorio/07-operacao/comercial/propostas/<codigo>-proposta-v<n>.md` e rode, com o caminho da pasta desta habilidade (a que contém este SKILL.md) e o caminho da proposta como argumentos:

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" "escritorio/07-operacao/comercial/propostas/<codigo>-proposta-v<n>.md"
```

O script confere antes de criar. A primeira linha da saída diz uma de três coisas:
- **"NÃO ESTÁ PRONTO PARA ENVIAR"**, com a lista do que falta e a linha de cada item: marcações com ou sem texto dentro, campos em maiúsculas que sobraram (`[NOME]`, `[DATA]`), trechos de instrução do modelo e conferências do "Antes de enviar" sem `[x]`. **Nenhum .docx é criado** e a saída é 2. Resolva no .md e rode de novo.
- **"PRONTO PARA GERAR O .DOCX"**: o texto está resolvido, mas há campos do envio entre chaves (`{...}`), que quem envia preenche no .docx. O .docx sai com eles em amarelo; depois de preencher, confira com `--conferir-docx`.
- **"PRONTO PARA ENVIAR"**: o .docx sai ao lado, sem o cabeçalho YAML e sem o "Antes de enviar".

Para criar o .docx mesmo com pendência (por exemplo, para o advogado ler no Word), acrescente `--forcar`: o arquivo sai com o que sobrou em amarelo e o aviso diz que ele não pode ir ao cliente assim. Para só conferir, sem criar nada, `--so-conferir`. Para conferir um .docx que alguém editou, `--conferir-docx <arquivo.docx>` (aí chave que sobrou também é pendência). Sem `python-docx`, o script confere do mesmo jeito e diz como gerar o .docx. Sem execução de código (chat comum), entregue o .md e diga: "Abra no Word ou no Google Docs, apague a seção 'Antes de enviar' e salve como .docx."

**Passo 8. A mensagem de envio.** Use o modelo `envio-de-proposta` da biblioteca (`escritorio/04-base/comercial/biblioteca-comercial.md`), no tom da ficha; sem biblioteca, o formato da seção 8. Só depois de "PRONTO PARA ENVIAR" (ou de "PRONTO PARA GERAR O .DOCX" com os campos do envio já preenchidos e o `--conferir-docx` dizendo "pronto"). Quem envia é uma pessoa (A).

**Passo 9. Registrar.** Mostre a linha do `contatos.csv` e grave com o ok. A etapa muda para `proposta-enviada` só quando alguém disser que a proposta saiu (seção 8).

**Passo 10. Aprender.** Pergunte: "Alguma coisa nesta proposta você faria diferente na próxima?". Correção vira regra curta nos aprendizados, com o ok (`../../docs/aprender-com-o-uso.md`). Correção de política ("parcelamos sempre em até 6 vezes sem juros") vai para a política e para `entrada_e_parcelas`, com o ok.

### D. Nova versão

1. Pergunte: "O que mudou e quem decidiu?". Mudança fora da política precisa do ok de `quem_aprova_a_proposta`.
2. Copie a versão anterior para `-v<n+1>`, mude só o que foi decidido, desmarque as conferências que a mudança afeta e escreva no cabeçalho interno, em uma linha, o que mudou.
3. Rode o script, escreva a mensagem da nova versão e, quando sair, atualize `valor_proposta` e volte a etapa para `proposta-enviada` (`funil.md`, regra 7, "Proposta nova"). A versão anterior não se apaga.

### E. No ciclo (o agente chama)

1. Liste os contatos com etapa `consulta-feita` ou `negociando` e uma proposta em `07-operacao/comercial/propostas/` sem mensagem de envio na fila.
2. Para cada proposta, rode o script com `--so-conferir`. Saída 2 (não está pronta): nada vai para a fila; o resumo do dia ganha, em "PARA DECIDIR", uma linha com o código e o que falta ("C-2026-0001: tabela da seccional sem conferir").
3. Saída 0 (pronta e aprovada no cabeçalho): rode o script sem opção para gerar o .docx (nunca com `--forcar` no ciclo) e grave o rascunho da mensagem em `07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-envio-de-proposta.md`, no formato de `agentes-e-fila.md`, com `tipo: envio-de-proposta`, `revisor: pendente`, `motivo: proposta v<n> pronta; anexar <codigo>-proposta-v<n>.docx` e `prazo` pela validade. Se a primeira linha foi "PRONTO PARA GERAR O .DOCX", acrescente ao motivo: "preencher no .docx os campos entre chaves e conferir com --conferir-docx antes de anexar".
4. Registro: o agente só põe `proximo_passo = confirmar envio da proposta v<n>` e a data de hoje (as colunas que `funil.md` permite ao agente, regra 11). A etapa e o `valor_proposta` mudam quando a pessoa confirma o envio (comando `/motor-comercial:fila`).
5. O ciclo nunca monta valor, nunca marca conferência e nunca cria proposta nova. Proposta a montar aparece em "PARA DECIDIR".
6. Contato com `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:`, ou com `pediu_para_parar = sim`: nenhum rascunho de envio. A proposta pronta entra em "PARA DECIDIR" com a frase "esperando a pessoa falar com o contato". O item sai dali quando a pessoa conta o que ficou combinado, pelo comando `fila` (`agentes-e-fila.md`, "PESSOA AGORA também sai da lista").

### F. Adaptar (a adaptar-comercial chama)

1. Leia `nicho.md`, a política e o modelo atual (o do escritório ou o de `assets/`).
2. Reescreva o modelo para o nicho, marcando cada mudança `[ALTERADO]`:
   - "O que você nos trouxe" e "Como o trabalho anda" nas palavras do cliente do nicho (tabela "Como ele fala");
   - a tabela da seção 4 com os tipos de caso do nicho: o que costuma estar incluído e o que fica de fora, como sugestão para o advogado confirmar;
   - os cenários de pagamento que combinam com o cliente do nicho (por exemplo, vencimento no dia em que o cliente recebe, entrada menor com mais parcelas dentro do máximo), sem nenhum valor.
3. Cenário que a política não prevê aparece separado, como "sugestão de política, decisão de [quem aprova]".
4. Mostre o antes e o depois de cada trecho. Grave em `escritorio/04-base/comercial/modelos/modelo-proposta.md` só com o ok, com versão e data no topo; o que for política vai para a política, também com o ok.

### Último passo, em todos os modos: Aprender

Toda correção do advogado vira proposta de aprendizado, com a pergunta "Quer que eu guarde isto para as próximas vezes?" e a regra em uma linha (`../../docs/aprender-com-o-uso.md`). No ciclo, a correção feita na fila (item `descartado` ou `ajustado` com motivo) vira a mesma proposta no resumo do dia. Nada entra nos aprendizados sem o ok.

## 4. O escopo: o que costuma entrar e o que fica de fora

Lista de partida para o advogado confirmar. Nada aqui entra na proposta sem ele dizer que vale para o caso.

| Tipo de trabalho | Costuma estar incluído | Costuma ficar de fora (confirmar) |
|---|---|---|
| Pedido administrativo (INSS, órgão, empresa) | Análise dos documentos, montagem e protocolo do pedido, acompanhamento, resposta a exigências | Ação judicial se o pedido for negado, perícia particular, recurso administrativo cobrado à parte |
| Ação judicial | Petição inicial, audiências da primeira instância, manifestações, acompanhamento até a sentença | Recursos aos tribunais, cumprimento de sentença, ações ligadas ao mesmo fato, assistente técnico |
| Recurso | Recurso no tribunal indicado e acompanhamento até o julgamento | Recursos seguintes, sustentação oral cobrada à parte |
| Fase de receber o valor | Cálculos, pedido de pagamento, acompanhamento até a liberação | Impugnações longas, novas ações contra o devedor |
| Acordo ou procedimento consensual | Reuniões com a outra parte, minuta do acordo, protocolo ou escritura | Disputa judicial se o acordo não sair |
| Assessoria mensal | O que a política diz que cabe no mês | O que passar disso, ações judiciais |

Cada item com verbo e objeto ("protocolar o pedido no INSS"), nunca "acompanhamento completo do caso".

## 5. Como escrever cada modelo de cobrança

| Modelo | Como aparece na proposta | O que nunca aparece |
|---|---|---|
| Fixo | Valor total, cenários de pagamento, datas | "Valor promocional", "só esta semana" |
| Êxito | "Percentual de [X]% sobre [BASE DA POLÍTICA], pago quando [MOMENTO DA POLÍTICA]. Se não houver valor recebido, não há honorário de êxito." | "Você só paga se ganhar, e vai ganhar"; estimativa de quanto o cliente vai receber |
| Misto | Parte fixa com os cenários e parte de êxito com base e momento, em partes separadas | Soma das duas partes como "custo total previsto" |
| Mensal | Valor do mês, o que cabe no mês, vencimento, como se encerra | Fidelidade sem saída |

Cenários (até três, todos dentro da política): à vista, se a política tiver condição para isso; entrada e parcelas, no máximo da política; outra forma prevista (por exemplo, misto para quem não pode pagar a entrada). Desconto para fechar logo e "condição especial para você" não entram. A validade aparece uma vez, como informação.

## 6. O cabeçalho interno "Antes de enviar"

Fica logo depois do cabeçalho YAML e antes do título da proposta, num título que começa com "Antes de enviar", e termina na linha `<!-- fim: antes de enviar -->`. O script não leva nada disso para o .docx. O que entra:

| Item | Exemplo |
|---|---|
| Quem aprova e a sigla | advogada titular · A |
| Fonte da consulta | caminho da ata |
| Conferências, uma por linha com `- [ ]` | Tabela da seccional `[CONFERIR]`; limite do total de honorários no êxito `[CONFERIR]`; conta fecha; duas listas batem com a ata; aprovada por quem aprova |
| Pendências | "valor da parte fixa `[A DEFINIR]` pela advogada" (e, no texto, o `[A DEFINIR]` no lugar do valor) |
| O que mudou nesta versão | "v2: 6 parcelas em vez de 5" |

**Checagem antes de mostrar** (a habilidade faz; as que dependem de fonte externa viram item do cabeçalho):
- [ ] Todo valor veio da política, da ficha ou do advogado nesta conversa.
- [ ] A conta fecha: entrada mais parcelas igual ao total; abatimento aplicado se a política manda.
- [ ] As duas listas existem: incluído e não incluído.
- [ ] Nenhuma frase promete resultado, prazo ou chance. Nenhuma estimativa do que o cliente vai receber.
- [ ] Nenhuma comparação com outro escritório, desconto como isca ou escassez.
- [ ] Nenhuma marcação no texto do cliente: todo `[CONFERIR]` está no cabeçalho interno.
- [ ] Nada de CPF, endereço, número de processo ou detalhe de saúde além do mínimo.

## 7. Exemplo resolvido (Escritório Modelo)

Caso 1 de `../../docs/casos-ficticios.md`: Marta, auxílio-doença cortado, contato C-2026-0001. Na consulta, a advogada titular decidiu tentar primeiro o pedido administrativo. Política de exemplo: fixo para o pedido administrativo, consulta abatida, entrada e até 5 parcelas, Pix ou boleto, validade de 10 dias corridos. A proposta completa, o cabeçalho interno, o que o script disse, a mensagem de envio e a linha do funil estão em `references/exemplo-escritorio-modelo.md`. Leia na primeira proposta do escritório ou quando o advogado pedir "me mostra como fica".

## 8. Formato da saída

**A proposta:** segue o modelo do escritório ou `assets/modelo-proposta.md`, nesta ordem: cabeçalho YAML, "Antes de enviar", apresentação em duas linhas, o que você nos trouxe, o que vamos fazer, o que não está incluído, etapas, honorários e cenários, despesas, validade, próximos passos, assinatura (de `dados_para_documentos`).

**A mensagem de envio (A, uma pessoa lê e envia), quando não há biblioteca:**

```
Oi, [NOME], tudo bem? Aqui é [QUEM ASSINA], do [ESCRITÓRIO].
Como combinamos na consulta, segue a proposta para o seu caso.
Nela estão o que vamos fazer, o que não está incluído, os valores e as formas de pagamento.
A proposta vale até [DATA DA VALIDADE].
Leia com calma. Se ficar qualquer dúvida, me escreva por aqui ou marcamos uma ligação rápida.
[ASSINATURA DAS MENSAGENS]
```

Sem "não perca", sem "condição especial", sem pressa. Os colchetes do modelo a habilidade preenche com a ficha, o registro e a proposta: nada entre colchetes vai ao cliente (o que faltar vai para "Antes de enviar"). Só o que quem envia escolhe na hora fica entre chaves, como `{DIA E HORA DA LIGAÇÃO}` se a pessoa oferecer uma ligação com horário, e some no envio.

**A linha do funil (depois de enviada):** etapa `proposta-enviada`; `valor_proposta` com a soma da parte fixa, só número, já sem a consulta quando a ficha diz que abate; `proximo_passo` "retorno 1 de [M]", com `M` de `maximo_de_retornos` e a data do primeiro retorno de "proposta sem resposta" em `follow_up`, em dias corridos. Sem `follow_up` na ficha, pergunte: "Quando você quer que eu lembre de retomar esta proposta?". Proposta só de êxito: `valor_proposta` fica vazio.

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Política de honorários | `escritorio/04-base/comercial/politica-de-honorarios.md` |
| Modelo de proposta do escritório (modo F ou quando o advogado fixar um) | `escritorio/04-base/comercial/modelos/modelo-proposta.md` |
| Proposta | `escritorio/07-operacao/comercial/propostas/<codigo>-proposta-v<n>.md` e o `.docx` ao lado |
| Rascunho da mensagem de envio (modo E) | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-envio-de-proposta.md` |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `etapa`, `valor_proposta`, `responsavel`, `proximo_passo`, `data_proximo_passo`, `atualizado_em` |
| Seção 3 da ficha comercial (com o ok) | `escritorio/04-base/comum/ficha-comercial.md`, com linha no histórico |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino com casos fictícios | `escritorio/07-operacao/_treino/comercial/propostas/` e `_treino/comercial/contatos.csv` |

Sem pasta aberta: entregue a proposta e a mensagem em texto pronto para copiar, com o caminho onde cada um ficaria, e a linha do funil como tabela. **Conectores** (conferir na configuração da conta): com Gmail, a mensagem pode ficar como rascunho com o .docx anexo, nunca enviada; com Google Drive, a habilidade pode ler a ata ou salvar a proposta na pasta do cliente.

## 10. Solo e equipe

**Solo:** quem monta e quem aprova é a mesma pessoa. A política faz o papel do sócio: proposta fora dela espera até o dia seguinte antes de sair. As conferências do cabeçalho são feitas em outro momento do dia, longe do cansaço do fim da tarde.

**Equipe:** a secretária ou o atendente monta a proposta a partir da ata. O advogado da consulta revisa escopo e valor, e `quem_aprova_a_proposta` marca as conferências. O limite do que quem atende pode ajustar sozinho fica escrito na política.

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Valor por áudio, sem escopo | Cliente acha que o recurso estava incluído | Duas listas obrigatórias |
| IA sugerir valor | Preço sem base e risco ético | Regra fixa 1 e `[A DEFINIR]` |
| `[CONFERIR]` no parágrafo de honorários | A proposta nunca fica pronta, ou sai com a marcação | Cabeçalho "Antes de enviar" e o script |
| Campo `[NOME]` esquecido no .docx | Cliente recebe documento com lacuna | Script lista cada campo que sobrou e não cria o .docx sem `--forcar` |
| "Você só paga se ganhar, e o seu caso é bom" | Promessa de resultado | Seção 5 e checagem |
| Desconto para fechar hoje | Leilão de preço | Cenários só dentro da política |
| Proposta esquecida depois de enviada | Pessoa some sem retorno | Linha do funil com retorno em dias corridos |
| Sobrescrever a proposta anterior | Ninguém sabe o que foi oferecido | Versões v1, v2, com a mudança no cabeçalho |

## 12. Próximo passo

- A pessoa aceitou: `contrato-de-honorarios` (se instalada). Sem ela, use o modelo de contrato do escritório com os dados da proposta aceita.
- Respondeu com dúvida ou objeção: `objecoes-comerciais` (se instalada). Sem ela, mostre a mensagem ao advogado antes de responder.
- Não respondeu: `follow-up` (se instalada), na data do retorno. Sem ela, a `rotina-comercial` lembra pela data do registro.

## Referências desta habilidade

- `references/politica-de-honorarios-modelo.md`: o modelo da política. Leia no modo A.
- `assets/modelo-proposta.md`: o modelo da proposta, já com o "Antes de enviar". Leia no modo B quando o escritório não tiver modelo próprio, e no modo F.
- `references/exemplo-escritorio-modelo.md`: a proposta do caso 1, com a saída do script. Leia na primeira proposta do escritório.
- `scripts/md_para_docx.py`: confere a proposta e, se não houver pendência no texto do cliente, cria o .docx sem a parte interna (com pendência, sai com código 2 e não cria; `--forcar` cria e avisa). Rode no passo 7, no modo D e no modo E.
