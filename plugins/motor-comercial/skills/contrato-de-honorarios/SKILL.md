---
name: contrato-de-honorarios
description: >
  Escreve a minuta do contrato de honorários a partir da proposta aceita: partes, objeto e
  escopo, o que não está incluído, honorários e pagamento, êxito, sucumbência, despesas,
  obrigações, comunicação, sigilo e LGPD, revogação e renúncia, substabelecimento,
  inadimplência, vigência e foro. Usa o modelo do escritório quando existe. Cada cláusula
  sensível vira uma conferência no cabeçalho interno "Antes de enviar", que o script não leva
  para o .docx e que avisa enquanto o contrato não estiver pronto. Prepara a mensagem de envio
  para assinatura. Use quando o advogado disser "a cliente aceitou, faz o contrato", "minuta do
  contrato de honorários", "contrato da proposta v2", "confere nosso modelo de contrato", "o
  filho vai assinar pela mãe, como fica". Não use para montar ou ajustar a proposta (use
  proposta-de-honorarios) nem para receber o cliente que assinou (use passagem-para-o-caso).
---

# Contrato de honorários

> A proposta aceita vira contrato com as mesmas palavras: o mesmo escopo, os mesmos valores, as mesmas exclusões. A IA escreve a minuta e lista o que precisa de olho de advogado. Assinar e fechar o valor final é de uma pessoa.

Regras do plugin: `../../docs/regras.md`. Fichas: `../../docs/ficha-comercial.md`. Funil: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Fila: `../../docs/agentes-e-fila.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

A cliente respondeu "aceito, pode mandar o contrato" numa sexta à noite. Na segunda, a advogada abre um contrato antigo, troca o nome e esquece de trocar o escopo. O contrato fala em "acompanhamento até o trânsito em julgado", a proposta falava só da fase administrativa. E o arquivo sai com três "[CONFERIR]" no meio das cláusulas.

**Regras fixas desta habilidade:**
1. O contrato repete a proposta aceita. Escopo, exclusões, valores e condições vêm dela, sem arredondar nem melhorar. Divergência entre os dois para tudo e vai para o advogado.
2. Toda cláusula sensível (partes, êxito, sucumbência, revogação e renúncia, inadimplência, foro, substabelecimento, LGPD, assinatura) vira item de conferência no "Antes de enviar". O texto das cláusulas sai sem marcação.
3. Qualificação completa das partes e dados de pagamento não passam pela IA: ficam como campos do envio entre chaves (`{QUALIFICAÇÃO COMPLETA}`, `{DADOS PARA PAGAMENTO}`), o escritório preenche no .docx, no próprio sistema, e confere com o script.
4. Valor final e assinatura são de uma pessoa (H). A etapa `fechado` só muda quando o advogado disser que o contrato foi assinado.
5. Nada de promessa de resultado. O objeto descreve o trabalho, nunca o desfecho.

## 1. Quando usar

**Use quando:**
- A proposta foi aceita e é hora da minuta.
- O cliente pediu um ajuste no contrato já enviado e o advogado decidiu (nova versão).
- O escritório tem um modelo de contrato e quer conferir se ele cobre as cláusulas essenciais (modo revisar modelo).
- Quem assina não é quem veio à consulta (filha pela mãe, empresa, curador).
- O agente do ciclo achou um contrato pronto sem mensagem de envio (modo no ciclo), ou a `adaptar-comercial` (se instalada) pediu o modelo no jeito do nicho (modo adaptar).

**Não use quando:**
- Ainda não há proposta aceita: use `proposta-de-honorarios`.
- O contrato foi assinado e é hora de passar o caso adiante: use `passagem-para-o-caso` (se instalada).
- O pedido é outro tipo de contrato (do cliente com terceiros, acordo com a outra parte): esta habilidade só faz o contrato entre o escritório e o cliente.

## 2. Antes de começar

1. **Leia as fichas:** `escritorio/04-base/comum/ficha-do-escritorio.md` (`nome`, `cidade_uf`, `dados_para_documentos`, `canais`, `horario_de_atendimento`) e `escritorio/04-base/comum/ficha-comercial.md` (seção 3, Honorários).
2. **Leia o nicho** (`escritorio/04-base/comum/nicho.md`), se existir: ele diz quais obrigações do cliente pesam mais (perícia, audiência, mediação).
3. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-comercial.md`). Aprendizado de contrato vale antes do padrão desta habilidade.
4. **Leia a proposta aceita** em `escritorio/07-operacao/comercial/propostas/<codigo>-proposta-v<n>.md`. Mais de uma versão: pergunte qual foi aceita.
5. **Leia a política** (`escritorio/04-base/comercial/politica-de-honorarios.md`), se existir: êxito, despesas, parcelamento e inadimplência.
6. **Procure o modelo do escritório** em `escritorio/04-base/comercial/modelos/modelo-contrato.md`. Existe: ele manda na ordem e nas palavras, e esta habilidade só aponta o que falta. Não existe: use `assets/modelo-contrato.md`. Modelo só em .docx que a habilidade não lê: peça o texto colado.
7. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`) para a etapa e o responsável.
8. **Conta de IA.** Em conta pessoal, só caso fictício, gravado em `escritorio/07-operacao/_treino/comercial/contratos/`. Em qualquer conta, a qualificação completa fica fora (regra fixa 3).

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `nome`, `cidade_uf`, `dados_para_documentos` · C: `modelo`, `formas_de_pagamento`.
- **Melhora:** C: `despesas`, `entrada_e_parcelas`, `inadimplencia`.

A cláusula de comunicação usa também `canais` e `horario_de_atendimento` da ficha do escritório e, se o motor-experiencia estiver em uso, `primeira_resposta_cliente_ativo` da ficha da experiência. Campo que falta: pergunte aquele campo, uma vez; sem resposta, o lugar fica `[A PREENCHER]` e a pendência vai para o cabeçalho interno.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Minuta, a pedido | Proposta aceita | A proposta e o cenário escolhido | Contrato .md e .docx, mensagem de envio no chat |
| B. Direto | O advogado diz tudo ("contrato da C-2026-0001, proposta v1, cenário 2, vencimento dia 10") | O pedido | O mesmo da minuta, perguntando só o que falta |
| C. Nova versão | O cliente pediu ajuste e o advogado decidiu | A versão anterior e a decisão | `-contrato-v<n+1>`, com a mudança no cabeçalho |
| D. Revisar modelo | O escritório tem modelo próprio | O modelo | Tabela das cláusulas: tem, falta, precisa conferir |
| E. No ciclo | O `agente-comercial` chama | Os contratos da pasta e o registro | Rascunho da mensagem de envio na fila; nada no chat |
| F. Adaptar | A `adaptar-comercial` chama | O nicho e o modelo atual | Modelo de contrato reescrito, com `[ALTERADO]`, gravado só com o ok |

### Passo 1. O aceite

Pergunte, uma de cada vez, o que não estiver escrito:
1. "Qual versão da proposta a pessoa aceitou e qual forma de pagamento ela escolheu?"
2. "Houve alguma mudança combinada depois da proposta, como dia de vencimento ou data da entrada?" Mudança de valor ou de escopo volta para a `proposta-de-honorarios` como nova versão, para o papel bater.

### Passo 2. As partes

Pergunte: "O contrato é com a própria pessoa que veio à consulta ou com outra (por exemplo, a filha que contrata pela mãe, uma empresa, um curador)?"
- Contratante é quem recebe o serviço. Quem só paga entra como responsável financeiro, com a concordância de quem recebe o serviço.
- Pessoa incapaz, menor ou interditada: o advogado decide a representação ou a assistência. A habilidade não escolhe.
- Empresa: quem assina e com que poderes.
- Contratado: sai de `dados_para_documentos` (advogado com OAB ou sociedade com registro). Campo vazio: pergunte "O contrato é em nome de quem: você, com a OAB e o número, ou a sociedade, com o registro?".

Cada um desses pontos vira item de conferência no cabeçalho interno. O nome e a qualificação saem como campos do envio, entre chaves: `{NOME COMPLETO}, {QUALIFICAÇÃO COMPLETA, preenchida no sistema do escritório}`. Entre chaves porque são de propósito: quem prepara o contrato para assinatura preenche, e o revisor aceita. Pendência de decisão continua entre colchetes e impede o .docx.

### Passo 3. As cláusulas

Monte a partir do modelo, cláusula por cláusula, com as fontes da seção 4. O que decidir e o que conferir em cada uma está em `references/clausulas-comentadas.md`. Leia antes da primeira minuta do escritório e sempre que o advogado perguntar "por que essa cláusula?". A cláusula de inadimplência sai do campo `inadimplencia` da ficha comercial; vazio, o texto fica com `[A DEFINIR]` e a pendência vai para o cabeçalho.

### Passo 4. Proposta e contrato lado a lado

Preencha a tabela de conferência do cabeçalho interno (seção 5) e rode a checagem da seção 6. Qualquer diferença: pare, mostre as duas frases e pergunte qual vale.

### Passo 5. Mostrar ao advogado

Mostre primeiro o "Antes de enviar", com três listas curtas:
- **O que conferir:** cada item `[CONFERIR]`, com uma linha do porquê.
- **O que é decisão sua (H):** valor final e as cláusulas que o escritório escolhe (multa, foro, testemunhas, assinatura eletrônica).
- **O que o escritório preenche fora da IA:** qualificação e dados de pagamento.

Depois a minuta. O advogado marca `[x]` em cada conferência que fez.

### Passo 6. Gravar e gerar o .docx

Com o ok, grave `escritorio/07-operacao/comercial/contratos/<codigo>-contrato-v<n>.md` e rode, com o caminho da pasta desta habilidade (a que contém este SKILL.md) e o caminho do contrato como argumentos:

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" "escritorio/07-operacao/comercial/contratos/<codigo>-contrato-v<n>.md"
```

O script confere antes de criar. A primeira linha da saída diz uma de três coisas:
- **"NÃO ESTÁ PRONTO PARA ENVIAR"**: sobrou marcação ou campo entre colchetes no texto das cláusulas (`[A DEFINIR]` da multa, `[CIDADE/UF]`), trecho de instrução do modelo ou conferência do "Antes de enviar" sem `[x]`. A saída lista cada item com a linha, sai com código 2 e **não cria o .docx**. Resolva no .md e rode de novo. Para ler a minuta no Word mesmo assim, acrescente `--forcar`: o .docx sai com o que sobrou em amarelo e o aviso diz que ele não pode ir para assinatura.
- **"PRONTO PARA GERAR O .DOCX"**: o texto está resolvido e só restam os campos do envio entre chaves (nome, qualificação, dados de pagamento, data da assinatura). É o resultado normal da minuta. O .docx sai com esses campos em amarelo.
- **"PRONTO PARA ENVIAR"**: nada a preencher (raro em contrato).

A pessoa do escritório preenche os campos entre chaves no .docx e confere de novo:

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" --conferir-docx "escritorio/07-operacao/comercial/contratos/<codigo>-contrato-v<n>.docx"
```

Essa conferência lê só o texto do .docx e mostra só o que ainda está pendente, sem repetir o que foi preenchido. Aqui chave que sobrou também é pendência. Saída 0 é "pronto"; saída 2, não. Contrato com pendência não vai para assinatura. Sem `python-docx`, o script confere do mesmo jeito e diz como gerar o .docx. Sem execução de código (chat comum), entregue o .md e diga: "Abra no Word ou no Google Docs, apague a seção 'Antes de enviar', preencha a qualificação e salve como .docx."

### Passo 7. A mensagem de envio

Escreva no tom da ficha, no formato da seção 8, só depois de "PRONTO PARA ENVIAR" no `--conferir-docx` do .docx preenchido. Uma pessoa lê e envia (A). Assinatura eletrônica só pela ferramenta que o escritório usa (conferir na configuração da conta).

### Passo 8. Registrar

- Enquanto o contrato não volta assinado, a etapa fica como está (`proposta-enviada` ou `negociando`) e o `proximo_passo` vira "assinar contrato", com a data combinada.
- Quando o advogado disser "assinou": mostre a linha com `etapa = fechado`, `valor_proposta` com o valor do contrato e `proximo_passo` "passagem para o caso". Grave só com o ok dele. A partir daí, a `passagem-para-o-caso` (se instalada) assume.

### Passo 9. Aprender

Pergunte: "Alguma cláusula você escreveria diferente nos próximos contratos?". Correção vira regra curta nos aprendizados, com o ok. Se o advogado aprovar a minuta como padrão do escritório, ofereça gravar em `escritorio/04-base/comercial/modelos/modelo-contrato.md`, com o "Antes de enviar" vazio, a versão e a data no topo. A partir daí, esse modelo manda.

### C. Nova versão

Pergunte o que mudou e quem decidiu. Copie a versão anterior para `-v<n+1>`, mude só o que foi decidido, desmarque as conferências afetadas, anote a mudança no cabeçalho interno e rode o script. A versão anterior não se apaga.

### D. Revisar modelo

Leia o modelo do escritório inteiro e preencha a tabela de `references/clausulas-comentadas.md` (tem, falta, conferir). Não reescreva o modelo sem o advogado pedir. Se o modelo tiver `[CONFERIR]` ou notas internas no meio das cláusulas, aponte e ofereça passar para um "Antes de enviar".

### E. No ciclo (o agente chama)

1. Liste os contatos com `proximo_passo` "enviar contrato" ou "assinar contrato".
2. "Enviar contrato" sem minuta: vai para "PARA DECIDIR" no resumo do dia ("C-2026-0001 aceitou a proposta v1; falta a minuta"). O ciclo não escreve contrato sozinho.
3. Com minuta e .docx: rode `--conferir-docx`. Saída 2: "PARA DECIDIR", com o que falta (o ciclo nunca preenche qualificação nem usa `--forcar`). Saída 0: grave o rascunho da mensagem em `07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-envio-de-contrato.md`, no formato de `agentes-e-fila.md`, com `tipo: envio-de-contrato`, `revisor: pendente` e `motivo: contrato v<n> pronto; anexar <codigo>-contrato-v<n>.docx`. No registro, só as colunas que `funil.md` permite ao agente (regra 11).
4. "Assinar contrato" com data vencida: "PARA DECIDIR" ("contrato enviado em 2026-03-18, sem assinatura"). Retorno sobre contrato não assinado é decisão do advogado.
5. O ciclo nunca muda a etapa para `fechado`.
6. Contato com `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:`, ou com `pediu_para_parar = sim`: nenhum rascunho. Vai para "PARA DECIDIR" com "esperando a pessoa falar com o contato", até a pessoa contar o combinado pelo comando `fila` (`agentes-e-fila.md`, "PESSOA AGORA também sai da lista").

### F. Adaptar (a adaptar-comercial chama)

1. Leia `nicho.md` e o modelo atual.
2. Reescreva, marcando cada mudança `[ALTERADO]`: as obrigações das partes (cláusulas 8 e 9) com o que pesa no nicho (perícia, audiência, documentos típicos, mediação); a cláusula de comunicação no jeito que o cliente do nicho prefere (canal, ligação para notícia importante); e, como sugestão separada, cláusulas que o nicho costuma pedir (por exemplo, responsável financeiro quando quem procura é o filho).
3. Nada de mudar êxito, sucumbência, revogação, inadimplência ou foro no modo adaptar: isso é decisão do advogado, cláusula a cláusula.
4. Mostre o antes e o depois. Grave em `escritorio/04-base/comercial/modelos/modelo-contrato.md` só com o ok.

### Último passo, em todos os modos: Aprender

Toda correção do advogado vira proposta de aprendizado, com a pergunta "Quer que eu guarde isto para as próximas vezes?" e a regra em uma linha (`../../docs/aprender-com-o-uso.md`). No ciclo, a correção feita na fila (item `descartado` ou `ajustado` com motivo) vira a mesma proposta no resumo do dia. Nada entra nos aprendizados sem o ok.

## 4. De onde vem cada cláusula

| Cláusula | Fonte | Vai para o "Antes de enviar" |
|---|---|---|
| Partes | Passo 2; `dados_para_documentos`, `nome`, `cidade_uf` | Sempre: representação, responsável financeiro, poderes |
| Objeto e escopo | "O que vamos fazer" da proposta, item por item | Sim, se diferente da proposta |
| O que não está incluído | "O que não está incluído" da proposta | Sim, se diferente da proposta |
| Honorários e pagamento | Cenário escolhido; política; `formas_de_pagamento` | Dados para pagamento: preencher fora da IA |
| Êxito | Proposta e política | Sempre |
| Sucumbência | Política ou advogado | Sempre |
| Despesas | Proposta, política, `despesas` | Sim, se diferente da proposta |
| Obrigações das partes | Modelo e nicho | Não |
| Comunicação | `canais`, `horario_de_atendimento`; `primeira_resposta_cliente_ativo` se houver | Campo vazio |
| Sigilo e LGPD | Modelo | Sempre |
| Revogação e renúncia | Modelo | Sempre |
| Substabelecimento | Modelo | Sempre |
| Inadimplência | `inadimplencia` e política | Sempre; valor vazio vira pendência |
| Vigência | Escopo da proposta | Não |
| Foro | `cidade_uf` | Sempre |
| Assinaturas | Ferramenta do escritório | Sempre |

## 5. Tabela de conferência (proposta e contrato)

Fica dentro do "Antes de enviar" e sai preenchida, linha por linha: escopo, não incluído, valor total, entrada e parcelas, vencimentos, êxito (percentual, base, momento), despesas, abatimento da consulta. Coluna "Igual?" com sim ou não. Um "não" para a minuta até o advogado decidir.

## 6. Checagem antes de mostrar

- [ ] Todos os itens da tabela de conferência estão iguais, ou a diferença foi decidida pelo advogado e anotada.
- [ ] A conta fecha: entrada mais parcelas igual ao total; valor por extenso igual ao número.
- [ ] O objeto descreve trabalho, não resultado. Nenhuma frase de chance ou garantia.
- [ ] Cada cláusula marcada "sempre" na seção 4 tem o seu item no "Antes de enviar".
- [ ] O texto das cláusulas não tem `[CONFERIR]` nem nota interna.
- [ ] Nenhum CPF, endereço, número de processo ou dado de saúde escrito pela IA.
- [ ] Normas só pelo nome, sem artigo.

## 7. Exemplos resolvidos (Escritório Modelo)

**Caso 1, Marta (C-2026-0001).** Aceitou a proposta v1, cenário "entrada e 4 parcelas" (valores de exemplo: entrada de 465 e 4 de 271,25, todo dia 10). A minuta copia os seis itens do escopo e os quatro do não incluído. Sem êxito: a cláusula 5 sai com "Não há honorários de êxito neste contrato." A tabela de conferência fecha em tudo. O "Antes de enviar" lista: partes (a própria Marta), sucumbência (não se aplica na fase administrativa, mas a cláusula fica), revogação, inadimplência (campo `inadimplencia` vazio no Escritório Modelo: pendência para a advogada), foro de Belo Horizonte/MG e assinatura. Na primeira rodada, o script disse "NÃO ESTÁ PRONTO" pela multa da cláusula 14 (`[A DEFINIR]`), saiu com código 2 e não criou o .docx. A advogada decidiu a multa. Na segunda, disse "PRONTO PARA GERAR O .DOCX", com quatro campos do envio em amarelo: nome, qualificação, dados de pagamento e data da assinatura. A secretária preencheu no .docx e o `--conferir-docx` disse "PRONTO PARA ENVIAR".

**Caso 7, Helena, BPC da mãe de 72 anos.** Quem procurou foi a filha. O serviço é para a mãe, então ela é a contratante. Helena entra como responsável financeira, com a concordância da mãe, e a cláusula de comunicação diz que o escritório pode falar com ela sobre o caso porque a mãe autorizou por escrito. No "Antes de enviar": "partes: responsável financeira e autorização da mãe `[CONFERIR]`". Se a mãe não puder manifestar vontade, a habilidade para e o advogado decide a representação. Sem a autorização, a filha não recebe informação do processo.

**Erro pego na checagem.** O modelo antigo do escritório dizia "até o trânsito em julgado". A proposta era só da fase administrativa. A habilidade parou e mostrou as duas frases. Vale a proposta.

## 8. Formato da saída

Ordem da entrega: o "Antes de enviar" (tabela de conferência, conferências, o que preencher fora da IA, pendências), a minuta, a saída do script, a mensagem de envio e a linha do funil.

**Mensagem de envio (A, uma pessoa lê e envia):**

```
Oi, [NOME], tudo bem? Aqui é [QUEM ASSINA], do [ESCRITÓRIO].
Segue o contrato de honorários, com o que combinamos na proposta.
Leia com calma. Se alguma parte não ficar clara, me pergunte antes de assinar, por aqui ou numa ligação rápida.
Para assinar: [COMO ASSINAR, pela ferramenta do escritório ou impresso] {LINK PARA ASSINAR, se a ferramenta gerar}.
[ASSINATURA DAS MENSAGENS]
```

Os colchetes a habilidade preenche com a ficha e o registro; nada entre colchetes vai ao contato (o que faltar vai para "Antes de enviar"). O link de assinatura eletrônica fica entre chaves: quem envia cola na hora, e a fila não deixa marcar `enviado` com chave no texto. Sem prazo inventado para assinar: se a proposta tinha validade, ela já disse.

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Minuta do contrato | `escritorio/07-operacao/comercial/contratos/<codigo>-contrato-v<n>.md` e o `.docx` ao lado |
| Rascunho da mensagem de envio (modo E) | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-envio-de-contrato.md` |
| Modelo do escritório (com o ok) | `escritorio/04-base/comercial/modelos/modelo-contrato.md` |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `proximo_passo`, `data_proximo_passo`, `atualizado_em`; com o advogado, `etapa = fechado` e `valor_proposta` |
| Campo `inadimplencia` decidido (com o ok) | `escritorio/04-base/comum/ficha-comercial.md`, com linha no histórico |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino com casos fictícios | `escritorio/07-operacao/_treino/comercial/contratos/` |

Sem pasta aberta: entregue a minuta e a mensagem em texto pronto para copiar, com o caminho de cada uma. **Conectores** (conferir na configuração da conta): com Google Drive, a habilidade pode ler o modelo do escritório e salvar a minuta na pasta do cliente; com Gmail, a mensagem pode ficar como rascunho com o .docx anexo, nunca enviada.

## 10. Solo e equipe

**Solo:** o advogado que escreveu a proposta revisa o contrato. Para não revisar o próprio texto no automático, leia primeiro só o "Antes de enviar" e, em outro momento do dia, a minuta inteira.

**Equipe:** a secretária ou o atendente gera a minuta. O advogado do caso marca as conferências e decide as pendências. A secretária preenche os campos entre chaves (qualificação, dados de pagamento, data) no .docx e roda o `--conferir-docx`. O modelo aprovado fica em `04-base/comercial/modelos/` para todo mundo usar o mesmo.

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Contrato copiado de outro cliente | Escopo, nome ou valor errado | Minuta sempre a partir da proposta aceita |
| Escopo do contrato maior que o da proposta | Cobrança à parte vira discussão | Tabela de conferência |
| `[CONFERIR]` no meio da cláusula | Cliente recebe nota interna, ou o contrato nunca fica pronto | Conferências no "Antes de enviar"; o script não cria o .docx com marcação no texto |
| Qualificação esquecida no .docx | Contrato assinado com lacuna | Campos entre chaves e `--conferir-docx`, que acusa chave que sobrou |
| Contrato com quem só paga | Sigilo quebrado e contratante errado | Passo 2 |
| CPF e endereço na conversa com a IA | Dado pessoal fora do necessário | Qualificação preenchida no sistema do escritório |
| `fechado` antes da assinatura | Funil mente e o caso começa sem contrato | Etapa só com o advogado |

## 12. Próximo passo

- Contrato assinado: `passagem-para-o-caso` (se instalada), que entrega o caso a quem cuida e prepara a entrada na experiência. Sem ela, avise quem vai cuidar do caso e use a `boas-vindas-do-cliente` do motor-experiencia (se instalado).
- O cliente quer mudar valor ou escopo antes de assinar: `proposta-de-honorarios` (nova versão) e depois volte aqui.
- Contrato enviado e sem assinatura: o advogado decide se e como retomar; a `rotina-comercial` mostra pela data do registro.

## Referências desta habilidade

- `assets/modelo-contrato.md`: o modelo do plugin, já com o "Antes de enviar". Leia quando o escritório não tiver modelo próprio e no modo F.
- `references/clausulas-comentadas.md`: o que cada cláusula decide, o que perguntar e o que conferir. Leia na primeira minuta do escritório e no modo D.
- `scripts/md_para_docx.py`: confere a minuta e, sem pendência entre colchetes no texto, cria o .docx sem a parte interna (com pendência, sai com código 2 e não cria; `--forcar` cria e avisa); com `--conferir-docx`, confere o .docx preenchido. Rode no passo 6 e no modo E.
