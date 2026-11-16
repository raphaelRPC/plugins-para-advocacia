---
name: pagina-do-caso
description: >
  Monta a página do caso para o cliente: um HTML pronto para o celular, com modo claro e escuro,
  letra maior opcional e as cores do escritório. No topo, o que o escritório já fez por ele;
  depois, onde o caso está, a linha do tempo (com o trabalho que não aparece no processo), os
  próximos passos, o que depende do cliente, o glossário, quando a página é atualizada de novo
  e o contato oficial em texto. Confere os dados, mostra a lista do que está na página e só
  publica com o ok. Sai por link, em PDF ou dos dois jeitos, como a ficha mandar, e é
  atualizada na mesma página. Use quando o advogado disser "faz a página do caso da Marta",
  "atualiza a página dela", "quero mandar um link com o andamento", "gera o PDF do caso",
  "página com a linha do tempo". Não use para o resumo do mês em mensagem (use
  resumo-mensal-do-caso) nem para o painel interno da carteira (use painel-da-carteira).
---

# Página do caso

> Uma página por cliente, em linguagem simples, que mostra o caminho do caso e o trabalho do escritório. O cliente abre no celular e entende onde está sem precisar perguntar.

Regras comuns: `../../docs/regras.md` (seção 6.1 vale inteira aqui). Fichas: `../../docs/ficha-da-experiencia.md`. Carteira: `../../docs/carteira.md`. Onde gravar: `../../docs/pasta.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

A Marta abriu o site do tribunal e viu "juntada de petição" e nada mais por um mês. Ela não viu a advogada conferir o histórico de contribuições, escrever as perguntas para o perito e separar os documentos da perícia. Com a página, ela lê logo no topo o que o escritório já fez por ela, vê a perícia no meio da barra de etapas, o que precisa separar até segunda e o telefone do escritório escrito por extenso, para copiar.

**Regras fixas desta habilidade:**
1. A página leva o mínimo: primeiro nome, tipo de caso, fase, o que o escritório fez, próximos passos, o que depende do cliente e o contato oficial do escritório. Nunca CPF, número do processo ou de benefício, valor, endereço, nome da outra parte ou dado de saúde (doença, dor, afastamento, laudo, CID, internação, cirurgia, tratamento, remédio, "passou mal", acamada, Alzheimer, demência, AVC, depressão, gestante, gravidez, deficiência). O nome do benefício (auxílio por incapacidade, BPC, aposentadoria) pode aparecer: ele não é dado de saúde. O script bloqueia o que reconhece; o resto é a leitura de uma pessoa.
2. Antes de publicar, a habilidade mostra a lista do que está na página e pede o ok de quem a ficha manda (`quem_aprova_publicar`). Sem ok, nada sai.
3. Nada de promessa, chance de êxito ou previsão de data de decisão ("logo sai", "sai logo", "vai dar tudo certo", "semana que vem", "você vai receber", "com certeza", "garantido", "o juiz decide em 30 dias", "deve decidir até junho"). Data só de ato já marcado (perícia, audiência) ou de compromisso do escritório ("a advogada liga segunda", "a página é atualizada em 05/05").
4. Notícia ruim ainda não conversada não entra na página. Primeiro a ligação do advogado (`status-para-o-cliente`, se instalada), depois a página.
5. Quem publica e quem envia o link é uma pessoa. O agente do ciclo prepara o rascunho e nunca publica.

## 1. Quando usar

**Use quando:**
- O escritório usa página do caso (`pagina_do_caso` = link, PDF ou os dois) e um cliente entra na carteira, tem movimentação relevante ou chega o dia do resumo (`quando_atualiza_a_pagina`).
- O cliente pergunta muito do andamento e o advogado quer dar a ele um lugar para olhar.
- O advogado quer mostrar o trabalho que não aparece no processo.
- O agente do ciclo chamou esta habilidade (modo "no ciclo").

**Não use quando:**
- `pagina_do_caso` = "não usamos": ofereça o resumo do mês (`resumo-mensal-do-caso`, se instalada) e pare.
- Há notícia ruim que o cliente ainda não ouviu do advogado (regra fixa 4).
- O cliente pediu para não receber material de rotina (`pediu_para_nao_receber = sim`) e não pediu a página.
- O pedido é um painel da carteira para a equipe: isso é interno e nunca vai ao cliente (`painel-da-carteira`, se instalada).

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` e `aprendizados-experiencia.md`, se existirem. Aprendizado vale mais que o padrão desta habilidade.
2. Sem fichas: ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só "Vocês mandam a página por link, em PDF ou dos dois jeitos?" e "Quem aprova antes de publicar?".
3. Leia o que existe do cliente, em `escritorio/07-operacao/experiencia/`: a linha da `carteira.csv`, `clientes/<codigo>/abertura.md`, `historico.md` (as linhas de contato e as de trabalho do escritório, canal `trabalho-do-escritorio`), `resumos/`, `documentos.md`, `ligacoes/` e a página anterior em `pagina/conteudo.md`.
4. Leia a base de relacionamento, se existir: `glossario-do-cliente.md` e `perguntas-do-caso-<tipo-de-caso>.md` (da `cliente-com-ia`) em `escritorio/04-base/relacionamento-com-o-cliente/`. O glossário da página sai dali.
5. Conta e dados: só conta profissional ou de equipe com cliente real. Em conta pessoal, só os casos fictícios, gravando em `escritorio/07-operacao/_treino/experiencia/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `pagina_do_caso`, `quem_aprova_publicar`.
- **Melhora:** X: `identidade_visual`, `quando_atualiza_a_pagina`.
- Lê também, se preenchidos: E: `nome`, `canais` (o telefone e o WhatsApp oficiais), `horario_de_atendimento`, `tratamento`, `assinatura_das_mensagens`, `cliente_tipico` (para a letra maior); X: `maximo_sem_noticia`, `resumo_mensal` (para "quando voltamos a falar" e a próxima atualização).

Campo vazio na hora: pergunte só aquele, uma vez, e ofereça gravar. `identidade_visual` vazia: a página sai nas cores neutras do modelo e você avisa. `canais` sem o número do telefone ou do WhatsApp: pergunte "Qual número do escritório o cliente pode copiar da página?" e ofereça gravar em `canais`; sem resposta, a página mostra só o canal oficial em texto.

### Como a página chega ao cliente (o campo `pagina_do_caso`)

| `pagina_do_caso` na ficha | O padrão de entrega |
|---|---|
| link | A página publicada como artefato do Claude, e o link enviado pelo canal oficial |
| PDF | A mesma página salva em PDF e enviada como arquivo pelo canal oficial |
| os dois | O PDF pelo canal oficial e o link para quem preferir abrir no celular |
| não usamos | Não há página (seção 1, "Não use") |

Explique ao advogado, com estas palavras ou parecidas, antes da primeira publicação: "O link abre para qualquer pessoa que tiver o endereço, sem senha. Se o cliente repassar, quem receber também abre. O PDF enviado pelo WhatsApp ou pelo e-mail oficial do escritório fica só na conversa com o cliente: é o caminho mais fechado." Quem escolhe é o escritório, na ficha. Um cliente pode pedir o outro jeito: registre na coluna `pagina_do_caso` da carteira.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | Onde fica o resultado |
|---|---|---|---|
| A pedido | O advogado ou a equipe | Monta, confere, mostra a lista, gera, explica como publicar | No chat e em `clientes/<codigo>/pagina/` |
| No ciclo | O `agente-de-suporte` | Atualiza o conteúdo e gera o rascunho; não mostra nada e não publica | Rascunho em `pagina/` e item na fila |
| Atualizar | Movimentação relevante, resumo do mês | Acrescenta à página existente, mantém o mesmo link | O mesmo artefato ou um PDF novo |
| Adaptar | `adaptar-experiencia` | Reescreve etapas por tipo de caso e textos-padrão para o nicho | `04-base/relacionamento-com-o-cliente/` (seção 7) |

**Modo direto:** "faz a página da C-2026-0001 com o que tem na pasta". Execute os passos 2 a 6 e pergunte só o que falta.

### Passo 1. Confirmar o cliente e o caminho
Confira na carteira: o cliente existe, não está `encerrado`, não tem notícia ruim pendente (fase `decisao` sem ligação registrada no `historico.md` depois da decisão), e a coluna `pagina_do_caso`. Se houver notícia ruim pendente: pare, diga o motivo em uma frase e aponte a `status-para-o-cliente` (se instalada; sem ela, o advogado liga e volta aqui depois).

### Passo 2. Juntar o material
Monte a linha do tempo a partir do `historico.md`, dos resumos, das ligações e das movimentações coladas. Para cada fato, pergunte-se: "isto o cliente entende e precisa saber?". Fatos de rotina repetidos (juntada, ato ordinatório) viram um só item ou saem.

As linhas do `historico.md` com canal `trabalho-do-escritorio` (o que o escritório fez sem falar com o cliente: petição protocolada, cálculo conferido, documento pedido ao INSS, prazo cumprido) são a fonte do trabalho do escritório na página: cada uma vira um item da linha do tempo com origem `escritorio`, e as mais importantes vão para o topo, em "O que já fizemos por você". Ato que também aparece no processo (petição protocolada, perguntas ao perito) leva `aparece_no_processo = sim`. Sem nenhuma linha de trabalho do escritório no histórico, pergunte: "O que o escritório fez neste caso que o cliente não vê no site do tribunal?". Nada inventado para a página parecer cheia.

### Passo 3. Escrever o conteúdo
Grave o conteúdo em `clientes/<codigo>/pagina/conteudo.md`, no formato do exemplo `assets/conteudo-exemplo-marta.md` (ou `.json`, como `assets/conteudo-exemplo-helena.json`). No .md, os campos de topo vão no cabeçalho (`proxima_atualizacao`, `telefone_oficial`, `whatsapp_oficial`, `tamanho_do_texto`) e o resumo do topo na seção `## O que já fizemos por você`, um item por linha. No .json: `proxima_atualizacao`, `o_que_ja_fizemos` (lista de frases), `escritorio.telefone_oficial`, `escritorio.whatsapp_oficial` e `identidade_visual.tamanho_do_texto`. Seção por seção:

- **Cabeçalho:** escritório, primeiro nome, tipo de caso em até cinco palavras sem dado sensível, área, data desta atualização (`atualizado_em`), data da próxima atualização (`proxima_atualizacao`, pela `quando_atualiza_a_pagina` e pelo dia do resumo; sem data, a página diz "quando houver novidade no caso"), assinatura (`assinatura_das_mensagens`), cores e fontes (`identidade_visual`) e o tamanho da letra (`tamanho_do_texto`: `normal` ou `grande`).
- **Contato oficial:** o canal em texto (`canal_oficial`, de `canais`), o telefone (`telefone_oficial`) e o WhatsApp (`whatsapp_oficial`) escritos por extenso, para o cliente copiar, e o horário (`horario_de_atendimento`). O botão "Abrir no WhatsApp" é só conveniência: o número escrito vale sozinho, inclusive no PDF. A página avisa que o contato oficial é só aquele e que o escritório nunca pede dinheiro, senha ou código por mensagem.
- **Letra maior:** `tamanho_do_texto: grande` quando o público tem pouca leitura ou é idoso (`cliente_tipico`, `nicho.md`) ou quando o cliente pediu. Quem lê pode trocar no botão da página: no tamanho normal ele mostra "A+ letra maior"; no grande, "A- letra normal". O rótulo sempre diz o que o toque faz, e a lista do que está na página diz com que letra ela abre.
- **O que já fizemos por você:** de 3 a 5 itens, cada um uma frase com verbo no passado ("Conferimos o seu histórico de contribuições no INSS"), tirados das linhas de trabalho do escritório do `historico.md`. É a primeira coisa que o cliente lê.
- **Onde estamos:** a fase em uma frase simples ("Esperando a perícia médica") e uma explicação de duas ou três frases: o que está acontecendo, o que isso quer dizer, o que o escritório faz enquanto isso.
- **Etapas:** de 4 a 6, com exatamente uma `atual`. Use a jornada do tipo de caso (`jornada-<tipo>.md`, se existir) ou as etapas-base da seção 5.
- **Linha do tempo:** data, origem (`escritorio` ou `processo`), título curto com verbo ("Enviamos as perguntas para o perito"), uma ou duas frases, e se aparece no processo (`sim` ou `nao`). Inclua sempre o trabalho do escritório que não aparece: conferência de documentos, cálculo, reunião, preparação, pesquisa, ligação. É a parte que mostra o valor.
- **Próximos passos:** o que vem, com data só se é ato marcado ou compromisso do escritório; sem data, "a seguir".
- **O que depende de você:** documentos pendentes de `documentos.md` (o nome, nunca o conteúdo), confirmações, avisos que o cliente precisa dar. Vazio: a página diz "por enquanto, nada".
- **Glossário:** só os termos que aparecem na página, na linguagem do `glossario-do-cliente.md`.
- **Quando voltamos a falar:** o compromisso do escritório, pela régua (`maximo_sem_noticia`, `resumo_mensal`) ou pelo que foi combinado.

Tratamento da ficha (você, senhor e senhora, pelo nome). Frases curtas, uma ideia por frase. Nenhuma marcação `[...]` nem campo `{...}` no conteúdo: dúvida vai para o chat, não para a página.

**Quem fala pelo cliente:** se a carteira diz que outra pessoa fala pelo cliente, com autorização (caso da Helena, que fala pela mãe), a página é para quem fala, com o tipo de caso escrito para ela ("BPC da sua mãe"), e a autorização precisa estar registrada em `abertura.md` `[A CONFIRMAR]` antes de publicar.

### Passo 4. Conferir
Rode a conferência sem gerar a página:

```
python3 <pasta-desta-habilidade>/scripts/gerar_pagina.py escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/conteudo.md --so-conferir
```

O script bloqueia CPF, número de processo ou de benefício, valor em dinheiro, endereço, palavras de saúde (doença, dor, afastamento, laudo, CID, internação, cirurgia, tratamento, remédio, "passou mal", acamada, Alzheimer, demência, AVC, depressão, gestante, gravidez, deficiência e semelhantes; "BPC da pessoa com deficiência", como nome do benefício, passa), telefone ou e-mail fora dos campos de contato, empresa da outra parte, promessa ou previsão ("em breve", "deve sair", "logo sai", "sai logo", "vai dar (tudo) certo", "semana que vem", "você vai receber", "com certeza", "garantido", "chance"), prazo do juiz ou do órgão ("decide em 30 dias", "decide até junho", "deve decidir até", "sai até", "o juiz tem 30 dias"; o passado, "foi julgado em março", passa) e qualquer marcação `[A PREENCHER]`, `[CONFERIR]` ou `[MAIÚSCULAS]`. O nome do benefício passa. Avisa quando: "o que já fizemos" não tem de 3 a 5 itens, falta a data da próxima atualização, não há telefone nem WhatsApp do escritório, o glossário explica termo que não está na página, há termo técnico sem explicação, não há trabalho do escritório na linha do tempo, há data futura na linha do tempo, a barra não tem uma etapa atual, o nome tem mais de uma palavra. Corrija e rode de novo até sair sem bloqueio. O que o script não pega (nome de pessoa da outra parte, detalhe de saúde com palavra que ele não conhece) é a sua leitura: releia a página inteira com essa pergunta.

### Passo 5. Mostrar a lista e pedir o ok
Mostre a lista que o script imprime (formato na seção 6) e pergunte a quem aprova (`quem_aprova_publicar`): "Esta é a lista do que vai estar na página. Posso gerar e preparar para publicar?". Ajuste o que a pessoa pedir e mostre de novo. Sem ok, pare aqui com o conteúdo gravado.

### Passo 6. Gerar e olhar
```
python3 <pasta-desta-habilidade>/scripts/gerar_pagina.py escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/conteudo.md escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/pagina-AAAA-MM-DD.html --lista escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/lista-AAAA-MM-DD.md
```
Abra o HTML no navegador (ou num navegador sem tela, se houver) e confira no tamanho de celular: sem rolagem lateral, a barra de etapas legível, o modo escuro, a letra (o botão troca entre "A+ letra maior" e "A- letra normal", e o tamanho acompanha) e o telefone que dá para copiar. Sem navegador, confira ao menos que o arquivo abre e que as seções estão na ordem.

### Passo 7. Publicar (uma pessoa)
Use o padrão de entrega da ficha (`pagina_do_caso`, tabela da seção 2) e explique ao advogado o que ele significa:

- **Link (artefato do Claude):** no Claude, peça para publicar o arquivo HTML como artefato. O link pode ser compartilhado com o cliente pelo canal oficial. Conferir na configuração da conta se a publicação e o compartilhamento por link estão disponíveis e como funcionam. Lembre a pessoa, em linguagem simples: o link abre para quem tiver o endereço, por isso a página não leva dado que não possa vazar, e o rodapé pede ao cliente que não repasse.
- **PDF:** abra o HTML no navegador, use Imprimir e escolha "Salvar como PDF" (o botão "PDF" da página faz o mesmo). O modelo já tem a versão de impressão, com o telefone escrito por extenso e sem os botões. Grave em `pagina/pagina-AAAA-MM-DD.pdf` e envie pelo canal oficial. É o caminho mais fechado.
- **Os dois:** o PDF pelo canal oficial e, na mesma mensagem, o link para quem prefere abrir no celular.

Quem envia é a pessoa. A mensagem que acompanha é curta. Com link: "Oi, Marta! Fiz uma página com tudo o que já aconteceu no seu caso e o que vem agora. Ela é só sua, por isso não repasse: {LINK DA PÁGINA}". Com PDF: "Oi, Marta! Segue um arquivo com tudo o que já aconteceu no seu caso e o que vem agora." O `{LINK DA PÁGINA}` é um campo do envio: quem publica preenche na hora de enviar, e a fila não deixa marcar como enviado com a chave no texto.

### Passo 8. Registrar
Com o ok, grave:
- `pagina/publicacoes.md`: uma linha por versão (data, versão, o que mudou, quem aprovou, link ou PDF). O link fica só aqui, no registro interno.
- `historico.md`: uma linha de contato na tabela (`| AAAA-MM-DD HHhMM | pagina | secretária | enviou a página do caso, versão N, por link ou PDF |`). A página informa o caso, por isso conta como contato com o cliente.
- `carteira.csv`: `pagina_do_caso` (`link` ou `pdf`), `ultimo_contato`, `ultimo_contato_tipo = pagina` e `atualizado_em`, só depois que a pessoa disser que enviou. Mostre as linhas antes de gravar.

### Passo 9. Atualizar a mesma página
A cada movimentação relevante ou no resumo do mês (`quando_atualiza_a_pagina`): edite o `conteudo.md` (novo item na linha do tempo, etapa atual, próximos passos, data), rode os passos 4 a 6 e mostre só o que mudou ("entrou: perícia realizada em 14/04; saiu: separar documentos"). Para o link, republique o mesmo artefato, para o cliente continuar no mesmo endereço (conferir na configuração da conta se a atualização mantém o link). Para o PDF, gere um novo com a data no nome. Nunca apague versão anterior: ela é o registro do que o cliente viu.

### Passo 10. Aprender
Pergunte: "Alguma coisa na página você mudaria para os próximos clientes?". Cada correção vira uma regra curta ("Página de previdenciário: não usar a palavra 'benefício negado' na fase, usar 'pedido não aceito pelo INSS'") e entra nos aprendizados com o ok. Mudança de cor, fonte ou logo vai para `identidade_visual`, na ficha, com linha no histórico.

### No ciclo (o agente chama)
1. O agente indica o cliente e o motivo (movimentação relevante, resumo do mês, cliente novo com `pagina_do_caso` = link ou PDF).
2. Se há notícia ruim pendente, reclamação aberta ou `pediu_para_nao_receber = sim`, não prepare nada: devolva "PESSOA AGORA" ou "PARA DECIDIR" com a frase do motivo.
3. Atualize o conteúdo em `pagina/rascunho-AAAA-MM-DD.md` (o `conteudo.md` aprovado não muda), rode o script e gere `pagina/rascunho-AAAA-MM-DD.html`.
4. Grave na fila `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-pagina-do-caso.md`, no formato de `agentes-e-fila.md`, com `tipo: pagina-do-caso`, os caminhos do rascunho, a lista do que está na página, o jeito de entregar (pela coluna `pagina_do_caso` da carteira ou pela ficha) e a mensagem curta que acompanha (com `{LINK DA PÁGINA}` quando for link). Bloqueio do script: o item vai para "PARA DECIDIR" com o motivo.
5. Não publique, não envie, não mude `pagina_do_caso` nem `ultimo_contato`.

## 4. O que a página nunca traz

| Nunca | No lugar |
|---|---|
| Número do processo, CPF, número do benefício | Nada. O número do processo é do cliente e vai pelo canal oficial, se ele pedir |
| Valor da causa, valor a receber, honorários | "A fase de pagamento" sem valor; valor é conversa do advogado |
| Nome da outra parte (pessoa ou empresa) | "a empresa", "a outra parte". O órgão público que decide o pedido (INSS) pode aparecer pelo nome |
| Doença, dor, crise, internação, cirurgia, tratamento, remédio, laudo, CID, afastamento | "documentos médicos", "perícia médica". O nome do benefício (auxílio por incapacidade, BPC, aposentadoria) pode ficar |
| Endereço do cliente ou do local | "no fórum", "na agência", "por vídeo" |
| "Em breve", "deve sair", "logo sai", "sai logo", "vai dar tudo certo", "o juiz decide em 30 dias", "semana que vem", "você vai receber", "com certeza", "garantido", "a chance é boa" | "Não há como saber quando o juiz decide. A gente avisa assim que sair." |
| Telefone pessoal de alguém da equipe | O telefone e o WhatsApp oficiais, nos campos de contato |
| Erro do escritório explicado por escrito | Ligação do advogado; a página só registra o que foi combinado depois |

## 5. Etapas-base por tipo de caso (exemplo, ajuste pela jornada)

| Tipo | Etapas |
|---|---|
| Benefício por incapacidade (judicial) | Contrato e documentos · Ação na Justiça · Perícia médica · Decisão do juiz · Pagamento |
| BPC | Contrato e documentos · Ação na Justiça · Análise do juiz · Avaliação social · Decisão |
| Pedido administrativo no INSS | Documentos · Pedido no INSS · Análise e exigências · Resposta do INSS · Próximo passo |
| Trabalhista | Contrato e documentos · Ação na Justiça · Audiência · Sentença · Pagamento |
| Divórcio ou alimentos consensual | Documentos · Acordo escrito · Pedido ao juiz · Homologação · Registro |
| Litígio de família | Documentos · Ação · Tentativa de acordo · Instrução · Decisão |

Tempo de cada etapa nunca vai na página: fica `[CONFERIR]` no nicho, para uso interno.

## 6. Formato da saída

**No chat (a pedido):**
```
PÁGINA DO CASO · [CÓDIGO] · [primeiro nome] · versão [N] · [AAAA-MM-DD]
Conferência: sem bloqueio | bloqueado: [o que achou]
[a lista do que está na página, como o script imprime]
Topo: o que já fizemos ([3 a 5] itens) · próxima atualização: [data] · letra: normal | grande
Contato na página: [canal] · telefone [sim | não] · WhatsApp [sim | não]
Quem aprova: [quem_aprova_publicar] · Sigla: A
Arquivos: conteudo.md · pagina-AAAA-MM-DD.html · lista-AAAA-MM-DD.md
Entrega (pela ficha): link | PDF | os dois, e a mensagem curta para acompanhar
Em aberto: [campos da ficha ou dados que faltaram]
```

**Na fila (no ciclo):** o item com `tipo: pagina-do-caso`, `revisor:` (o `revisor-de-suporte` confere as regras 5 e 10 dele), o caminho do rascunho e a lista.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Conteúdo aprovado da página | `escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/conteudo.md` |
| Página gerada e PDF | `escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/pagina-AAAA-MM-DD.html` e `.pdf` |
| Lista do que está na página | `escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/lista-AAAA-MM-DD.md` |
| Registro das publicações | `escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/publicacoes.md` |
| Rascunho do ciclo | `escritorio/07-operacao/experiencia/clientes/<codigo>/pagina/rascunho-AAAA-MM-DD.md` e `.html`, e o item da fila |
| Histórico e carteira | `historico.md` (uma linha) e `carteira.csv` (`pagina_do_caso`, `ultimo_contato`, `ultimo_contato_tipo`, `atualizado_em`), só depois do envio |
| Modo adaptar | etapas por tipo de caso na `jornada-<tipo>.md` (se a `jornada-do-cliente` estiver instalada; sem ela, em `04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chave `pagina-etapas-<tipo>`), cada mudança marcada `[ALTERADO]`, gravada só com o ok |
| Treino | `escritorio/07-operacao/_treino/experiencia/clientes/<codigo>/pagina/` |

Sem pasta aberta: entregue o conteúdo no chat, peça para salvar como `conteudo.md` e, sem script, monte o HTML a partir de `assets/pagina-modelo.html` trocando cada `{{CAMPO}}` com o texto escapado, e faça a conferência da seção 4 à mão.

## 8. Solo e equipe

**Solo:** o titular aprova e publica. Atualize a página junto com o resumo do mês, num horário fixo, para não virar mais uma tarefa solta. Comece pelos clientes que mais perguntam.

**Equipe:** a secretária ou a assistente monta o conteúdo e gera a página; quem está em `quem_aprova_publicar` lê a lista e aprova; o advogado responsável lê tudo o que for decisão, perícia ou audiência. A linha do tempo e o "o que já fizemos" melhoram quando a equipe registra no `historico.md`, no dia em que faz, cada trabalho do escritório (canal `trabalho-do-escritorio`).

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Página com número do processo ou CPF | Dado pessoal exposto a quem tiver o link | Script bloqueia e regra fixa 1 |
| Página que só copia o site do tribunal | O cliente não vê o trabalho do escritório | Linha do tempo com o trabalho que não aparece |
| "Deve sair em breve" na página | Promessa que não depende do escritório | Script bloqueia; seção 4 |
| Notícia ruim lida na página antes da ligação | O cliente descobre sozinho | Regra fixa 4 e passo 1 |
| Termo técnico sem explicação | A pergunta volta pelo WhatsApp | Glossário conferido pelo script |
| Link novo a cada atualização | Cliente com cinco links e a versão errada | Passo 9: republicar o mesmo artefato |
| Agente publicando sozinho | Página sem ninguém ler | Regra fixa 5 e modo no ciclo |
| Dado de saúde de quem fala pelo cliente | Exposição de dado sensível | Script e leitura; só "intercorrência" no histórico |
| Cliente sem saber como falar com o escritório, ou caindo em golpe | Ligação para número errado, Pix para quem não é do escritório | Telefone oficial em texto, para copiar, e o aviso de golpe na página |
| Letra pequena para quem lê pouco | O cliente desiste da página e volta a perguntar | `tamanho_do_texto: grande` e o botão que alterna entre "A+ letra maior" e "A- letra normal" |

## 10. Próximo passo

- Termo que o cliente não entende: `glossario-do-cliente.md` e as perguntas do caso pela `cliente-com-ia` (se instalada; sem ela, escreva a explicação no glossário da própria página).
- Documento pendente na página: `checklist-de-documentos` (se instalada) para o controle e a cobrança.
- Perícia ou audiência nos próximos passos: `preparar-o-cliente` (se instalada; sem ela, o advogado liga na semana).
- Página todo mês sem ninguém pedir: `rotina-da-experiencia` (se instalada) e o ciclo.

## Referências desta habilidade

- `assets/pagina-modelo.html`: o modelo único da página (responsivo, modo claro e escuro, letra maior pela variável `{{TAMANHO_DO_TEXTO}}` e pelo botão que alterna "A+ letra maior" e "A- letra normal", cores em variáveis, fontes do Google Fonts, contato oficial em texto com botão de copiar, versão de impressão). Não edite os `{{CAMPOS}}`.
- `scripts/gerar_pagina.py`: confere e preenche o modelo. Passos 4 e 6.
- `assets/conteudo-exemplo-marta.md`: exemplo de conteúdo em .md (C-2026-0001, perícia em 2026-04-14, letra grande), com a seção "O que já fizemos por você" e os campos de contato.
- `assets/conteudo-exemplo-helena.json`: exemplo em .json (C-2026-0007, filha que fala pela mãe, concluso para despacho, outras cores e fontes, letra normal).
