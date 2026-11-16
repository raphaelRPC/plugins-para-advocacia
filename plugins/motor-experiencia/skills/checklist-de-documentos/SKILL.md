---
name: checklist-de-documentos
description: >
  Cuida dos documentos do caso depois do contrato: monta a lista de cada tipo de caso (o que é
  cada documento em palavras simples, onde o cliente consegue, como mandar), pede ao cliente,
  abre o controle do caso, dá baixa no que chegou, avisa o que veio com problema e cobra com
  gentileza pela régua da ficha, atualizando a coluna de documentos pendentes da carteira.
  Todo requisito de documento sai marcado para conferir na fonte. Use quando o advogado disser
  "pede os documentos da Renata", "o que falta ela mandar?", "chegou a certidão, dá baixa",
  "quem está devendo documento?", "cobra com jeito", "monta a lista de documentos de BPC",
  "mandei por e-mail, chegou?". Não use para o que o contato traz na consulta, antes do
  contrato (use roteiro-da-consulta do motor-comercial, se instalado), nem para arquivar o
  documento no sistema do escritório.
---

# Checklist de documentos

> "Me manda o CNIS" funciona para quem sabe o que é CNIS. A lista diz o que é cada papel, onde a pessoa consegue e como mandar. O controle diz, sem rolar a conversa, o que já chegou e o que falta.

Regras comuns: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Carteira: `../../docs/carteira.md`. Onde gravar: `../../docs/pasta.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

A Renata assinou no dia 1º e ficou de mandar a certidão de casamento e a matrícula do imóvel. Nove dias depois, nada chegou e ninguém cobrou. Na sexta ela escreve "esqueci a certidão, mando segunda". Com o controle, a secretária responde "pode sim", anota a segunda no controle, e o lembrete daquele dia já está marcado. A matrícula, que ninguém lembrou, aparece na lista de cobrança da manhã.

**Regras fixas desta habilidade:**
1. Todo requisito de documento (validade, versão atualizada, autenticação, formato que o órgão exige) sai `[CONFERIR]` na fonte, no cabeçalho interno da lista. As listas-base de `references/` são exemplo até o advogado confirmar.
2. Nunca se pede senha, código de acesso ou login (gov.br, Meu INSS, banco). O "onde conseguir" ensina o caminho; quem entra no sistema é o cliente.
3. Cobrança é gentil, sem pressão e sem urgência falsa, no máximo o número de cobranças da régua (`cobranca_de_documentos`). Depois disso, o advogado decide. Prazo do processo correndo: o advogado acompanha a cobrança.
4. Laudo, exame, documento de criança ou adolescente e de processo em segredo de justiça vão só pelo canal oficial e não entram na IA sem autorização expressa do advogado.
5. O controle registra o nome do documento, a data e a situação. Nunca o conteúdo.

## 1. Quando usar

**Use quando:**
- O contrato foi assinado e é preciso pedir os documentos do caso (a passagem do comercial ou as boas-vindas trazem a lista do que ficou pendente).
- O processo ou o órgão fez uma exigência de documento.
- Chegou documento e é preciso dar baixa, ou avisar que veio com problema.
- O cliente pergunta "chegou o que eu mandei?" ou avisa que vai atrasar.
- É dia de cobrar, ou o `agente-de-suporte` chamou no ciclo.
- O escritório quer a lista de um tipo de caso, para usar sempre.

**Não use quando:**
- Quem pergunta ainda não é cliente: o que trazer na consulta é do motor-comercial (`roteiro-da-consulta`, se instalado; sem ele, a lista curta da coluna "consulta" das listas-base).
- O pedido é salvar e arquivar o documento: segue o sistema do escritório.
- O cliente quer que o escritório entre no sistema com a senha dele: não se faz (regra fixa 2); o advogado conversa sobre outro caminho, como procuração.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), `nicho.md` e `aprendizados-experiencia.md`, se existirem.
2. Sem fichas: ofereça `/motor-experiencia:comecar`. Para seguir agora, pergunte só "Como o cliente costuma mandar documento para vocês?" e "Depois de quantos dias vocês lembram quem não mandou?". Ofereça gravar no fim.
3. Leia a lista do tipo de caso, se existir: `escritorio/04-base/atendimento-e-triagem/checklist-documentos-<tipo-de-caso>.md`. O `inicio-automacao` grava no mesmo lugar: amplie sem duplicar.
4. Leia o que existe do cliente: a linha da `carteira.csv`, `clientes/<codigo>/documentos.md`, `abertura.md` e a passagem do comercial (`escritorio/07-operacao/comercial/passagens/<codigo>.md`), que diz o que ficou pendente na consulta.
5. Leia a biblioteca (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`), se existir: chaves `pedido-de-documento`, `cobranca-gentil`, `documento-com-problema`, `documentos-completos`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas`, `casos_mais_comuns` · X: `como_o_cliente_manda`.
- **Melhora:** X: `cobranca_de_documentos`.
- Lê também, se preenchidos: E: `tratamento`, `canais`, `assinatura_das_mensagens`, `cliente_tipico`; X: `quem_cuida_dos_casos`.

`cobranca_de_documentos` vazio: pergunte "Depois de quantos dias do pedido a gente lembra?" e sugira o exemplo da ficha (3 e 7 dias corridos), marcado `[A DEFINIR]` no controle até o advogado decidir.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Lista do tipo de caso | Tipo de caso sem lista | Área e tipo de caso | `checklist-documentos-<tipo>.md` |
| B. Pedir | Contrato assinado, exigência | Código | Mensagem de pedido e `documentos.md` aberto |
| C. Dar baixa | Chegou documento, o cliente pergunta ou remarca | Código e o que chegou | Controle atualizado e a resposta |
| D. Cobrar | Data de cobrança, "quem está devendo?" | Um código ou todos | Cobranças do dia, uma por cliente |
| No ciclo | O `agente-de-suporte` chama | A pasta `clientes/` | Cobranças na fila, contagem na carteira; nada mostrado |
| Adaptar | `adaptar-experiencia` | Ficha, nicho, listas do escritório | Listas e textos reescritos para o nicho |

**Modo direto:** "pede os documentos de BPC para a C-2026-0007, até dia 20". Execute, mostre e pergunte só o que falta.

### Modo A. Lista do tipo de caso
1. Pergunte: "Para qual tipo de caso vamos montar a lista?". Sugira os de `casos_mais_comuns`.
2. Leia a lista-base da área em `references/` e mostre a do tipo de caso, com os documentos pessoais da área. A coluna "Quando" das listas-base separa o que costuma vir já na consulta (do comercial) do que se pede depois do contrato. Área sem lista-base: "No último caso desse tipo, que documentos você precisou pedir?".
3. Ajuste com o advogado, uma pergunta por vez: "Destes, quais você corta e quais faltam?"; "Quais são obrigatórios e quais são 'se houver'?"; "Algum tem exigência de validade ou de versão que você confere sempre?" (anote onde conferir, `[CONFERIR]`).
4. Mostre no formato da seção 6.1. Com o ok, grave como `em uso`; sem ok de tudo, `rascunho`.

### Modo B. Pedir os documentos do caso
1. **Partir do que já se sabe:** a lista do tipo de caso, menos o que já chegou na consulta (passagem do comercial), mais a exigência do processo, se houver. Pergunte: "Algum documento a mais, ou a menos, para este caso?". A lista do caso é aprovada pelo advogado.
2. **Escrever o pedido** (seção 7.1, sigla A): um item por documento, com o que é, onde conseguir e como mandar (`como_o_cliente_manda`). Até cinco documentos por mensagem; mais que isso, duas mensagens, na ordem em que o caso precisa.
3. **Prazo:** "Até quando ele precisa mandar? É prazo do processo ou combinado nosso?". Prazo do processo: anote no controle e a cobrança passa pelo advogado.
4. **Abrir o controle:** crie ou atualize `clientes/<codigo>/documentos.md` (seção 6.2), com a régua de `cobranca_de_documentos`.
5. **Carteira:** proponha `documentos_pendentes` (quantos itens abertos), `proximo_contato` (a primeira cobrança), `motivo_proximo_contato = documento` e `atualizado_em`. Se a fase ainda é `entrada`, proponha `fase = documentos` para quem conduz o caso confirmar (a fase é do jurídico).

### Modo C. Dar baixa
1. "Qual documento, e chegou por onde?". Se o documento está na conversa, olhe só o que precisa para conferir (legível, inteiro, do titular certo, com data), e só em conta profissional.
2. Situação de cada item: `chegou-ok`; `chegou-com-problema` (cortado, ilegível, de outra pessoa, desatualizado `[CONFERIR]`); `nao-existe` (o cliente diz que não tem: vai para o advogado); `dispensado` (o advogado decidiu); `pendente`.
3. **O cliente remarca** ("mando segunda", mensagem 3 de `../../docs/casos-ficticios.md`): responda que pode, grave a data em "Combinado até" e a cobrança passa a ser nesse dia. Sem pressão.
4. Resposta: confirmação (7.3), o que refazer (7.4) ou, quando fecha, lista completa (7.5).
5. "Mandei por e-mail, chegou?": sem acesso ao e-mail, "Recebi sua mensagem, vou conferir e te confirmo até [HORA]" (prazo de `primeira_resposta_cliente_ativo`). Com conector de e-mail ligado (conferir na configuração da conta), procure a mensagem só para ver o nome dos anexos.
6. Atualize o controle e a carteira (`documentos_pendentes`, `atualizado_em`). Lista fechada: situação `fechada em AAAA-MM-DD` e avise quem conduz o caso.

### Modo D. Cobrar
1. Rode o script com a régua da ficha (dias corridos):
```
python3 <pasta-desta-habilidade>/scripts/documentos_pendentes.py escritorio/07-operacao/experiencia/clientes --carteira escritorio/07-operacao/experiencia/carteira.csv --regua 3,7 --hoje AAAA-MM-DD
```
   O script lê todos os `documentos.md`, diz quem cobrar hoje (data combinada ou régua), quem está atrasado, o que vai para o advogado decidir e a contagem de pendentes por cliente, comparada com a carteira. Lê carteira com vírgula ou ponto e vírgula, com ou sem BOM, e datas AAAA-MM-DD ou DD/MM/AAAA. Sem pasta, sem nenhum controle ou sem a coluna `documentos_pendentes`, ele para com erro: não conclua que não há cobrança.
2. Antes de cada cobrança, confira: `pediu_para_nao_receber = sim` (o script marca LIGAÇÃO: uma pessoa liga, sem mensagem de rotina); prazo do processo (o advogado acompanha); cliente idoso ou sem familiaridade com o celular que não respondeu à primeira (ligação); reclamação aberta ou humor `insatisfeito` (uma pessoa fala primeiro).
3. Cobrança: mensagem da seção 7.2. Depois da última cobrança da régua, não há outra mensagem: o advogado decide (ligar, pedir prazo, seguir sem, mudar o caminho).
4. Registre cada cobrança na coluna "Cobranças" do controle, com a data, e uma linha de contato no `historico.md` (seção 8.1).

### No ciclo (o agente chama)
1. Rode o script do modo D com a régua da ficha e a data do dia.
2. Para cada "cobrar hoje" com mensagem: rascunho da seção 7.2 na fila, `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-cobranca-de-documento.md`, no formato de `agentes-e-fila.md`, com `tipo: cobranca-de-documento`.
3. LIGAÇÃO, régua cumprida, `nao-existe` e controle travado: devolva ao agente para "PARA DECIDIR", uma frase por item.
4. Atualize na carteira só `documentos_pendentes`, `proximo_contato`, `motivo_proximo_contato` e `atualizado_em`. Não envie nada e não mostre nada.

### Modo adaptar
Leia `nicho.md` (documentos típicos, onde o cliente consegue, como ele fala) e as listas do escritório. Reescreva as listas-base e os textos de "o que é" e "onde consegue" na linguagem desse cliente, marcando cada mudança `[ALTERADO]`. Grave cada lista em `checklist-documentos-<tipo>.md` só com o ok, como nova versão.

### Passo final. Aprender
Pergunte: "Alguma coisa na lista ou na mensagem você faria diferente?". Cada correção vira uma regra curta ("Pedido de carteira de trabalho: todas as páginas com anotação, não só a da foto") e, com o ok, entra nos aprendizados. Correção que muda a lista vira versão nova do checklist, com linha em "Mudanças". Régua de cobrança combinada pela primeira vez: ofereça gravar em `cobranca_de_documentos`, na ficha.

## 4. Como o cliente manda

Use `como_o_cliente_manda` da ficha. Sem o campo, o texto-padrão (ajuste aos `canais`):
- "Pode mandar por aqui mesmo, um de cada vez, e me diga qual é qual."
- "Se for foto: boa luz, a folha inteira aparecendo, sem dobra e sem dedo na frente. Se tiver em PDF, melhor ainda."
- "Documento com mais de uma página: uma foto por página, na ordem."
- Laudo, exame e documento de criança: "Esse, por favor, só por este número" (ou pelo e-mail oficial, o que estiver em `canais`). Nunca para o celular pessoal de alguém da equipe.
- Cliente sem familiaridade com o celular: entrega no escritório ou uma ligação para fazer junto, com o cliente digitando a própria senha.
- Original: só se o advogado pedir.

## 5. Exemplo resolvido (Escritório Modelo)

**Renata (C-2026-0005), divórcio consensual, fase `documentos`.** Pedido em 2026-04-01: certidão de casamento atualizada e matrícula atualizada do imóvel. Régua da ficha: 3 e 7 dias corridos. Ninguém cobrou. Na sexta, 2026-04-10, ela escreve "Esqueci de mandar a certidão, mando segunda, pode ser?".
- Resposta (A, a secretária envia): "Pode sim, Renata, obrigada por avisar! Fico esperando a certidão na segunda. Se tiver dificuldade para tirar, me fala."
- Controle: certidão com "Combinado até" 2026-04-13; matrícula segue pela régua.
- Script na sexta: matrícula "atrasada desde 2026-04-04", 1ª cobrança; certidão "aguardando, próxima em 2026-04-13". Carteira: `documentos_pendentes = 2`, `proximo_contato = 2026-04-13`, `motivo_proximo_contato = documento`.
- Cobrança da matrícula, junto na mesma mensagem da sexta ou no dia útil seguinte (escolha da secretária): "Ah, e a matrícula do imóvel também ficou faltando. Ela sai no cartório de registro de imóveis da cidade onde o imóvel fica. Se estiver difícil, me conta que a gente vê outro caminho."
- Falha da régua (9 dias sem cobrança): vira item para a `rotina-da-experiencia` (se instalada) e um aprendizado se a causa for a régua não estar na ficha.

## 6. Formato da saída

### 6.1 A lista do tipo de caso (`checklist-documentos-<tipo-de-caso>.md`)
```
---
documento: Checklist de documentos · [TIPO DE CASO]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
situacao: rascunho | em uso
area: [ÁREA]
---
# Checklist de documentos · [TIPO DE CASO]

## Antes de usar (interno)
- Requisitos a conferir na fonte: [CONFERIR] ...

| Documento | Quando | Obrigatório | O que é (para o cliente) | Onde consegue | O que conferir |
|---|---|---|---|---|---|

## Como mandar (texto do escritório)
## Cuidados (sensíveis, senha, celular pessoal)
## Mudanças
- 1 · AAAA-MM-DD · criado
```

### 6.2 O controle do caso (`clientes/<codigo>/documentos.md`)
```
---
documento: Documentos do caso · [CÓDIGO]
versao: [N]
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---
# Documentos do caso · [CÓDIGO] · [nome curto]
Lista: checklist-documentos-[tipo].md v[n] · Aprovada por: [advogado] · Pedido em: AAAA-MM-DD
Prazo do processo: não | sim, AAAA-MM-DD [CONFERIR]
Régua de cobrança: [dias] corridos depois do pedido (ficha: cobranca_de_documentos)
Situação: aberta | fechada em AAAA-MM-DD | travada (decisão do advogado: ...)

| Documento | Situação | Pedido em | Combinado até | Chegou em | Cobranças | Observação |
|---|---|---|---|---|---|---|
| Certidão de casamento atualizada | pendente | 2026-04-01 | 2026-04-13 | | | avisou que manda na segunda |
| Matrícula atualizada do imóvel | pendente | 2026-04-01 | | | | |
```
As colunas Documento, Situação e Pedido em são obrigatórias para o script. A observação descreve o problema ("página 2 cortada"), nunca o conteúdo. `documentos_pendentes` da carteira = itens `pendente`, `chegou-com-problema` e `nao-existe`.

## 7. As mensagens (rascunhos para a biblioteca, todas A)

### 7.1 Pedido (`pedido-de-documento`)
```
Oi, [NOME], tudo bem? Para dar o próximo passo no seu caso, preciso destes documentos:

1. [DOCUMENTO]: [O QUE É, EM UMA FRASE]. Você consegue em [ONDE].
2. [DOCUMENTO]: [O QUE É]. Você consegue em [ONDE].

Como mandar: [COMO O CLIENTE MANDA].

Consegue me enviar até [DATA]? Se tiver dificuldade com algum, me fala que a gente resolve junto.
```

### 7.2 Cobrança gentil (`cobranca-gentil`)
```
Oi, [NOME], tudo bem? Passando para lembrar do [DOCUMENTO] que combinamos [no dia DATA].

Ele é importante porque [POR QUE O CASO PRECISA, EM UMA FRASE].

Se estiver difícil de conseguir, me conta o que está acontecendo que eu te ajudo a achar outro caminho. Se já mandou e eu não vi, me desculpa e me avisa por aqui.
```
Sem "urgente", sem "último aviso", sem "seu caso vai parar".

### 7.3 Confirmação
```
Recebi [DOCUMENTOS], obrigada! Ainda falta [O QUE FALTA, OU "nada por enquanto"].
```

### 7.4 Documento com problema (`documento-com-problema`)
```
Oi, [NOME], recebi o [DOCUMENTO], obrigada! Ele chegou [O PROBLEMA]. Consegue mandar de novo, [COMO REFAZER]?
```

### 7.5 Lista completa (`documentos-completos`)
```
Oi, [NOME], chegou tudo o que a gente precisava, obrigada! O próximo passo é [PRÓXIMO PASSO EM TERMOS GERAIS], e eu te aviso quando [QUANDO VOLTA A FALAR].
```
Os `[CAMPOS]` são preenchidos pela habilidade antes de ir para a fila (a `[DATA]` é a combinada no controle ou a da régua). Com conteúdo do caso que o modelo não traz, o advogado lê antes. Campo que só quem envia sabe na hora (um horário para passar no escritório, o link de uma pasta compartilhada criada para o cliente) fica entre chaves, como `{LINK DA PASTA}`, e a fila não deixa marcar como enviado com chave no texto.

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Lista do tipo de caso | `escritorio/04-base/atendimento-e-triagem/checklist-documentos-<tipo-de-caso>.md` |
| Controle do caso | `escritorio/07-operacao/experiencia/clientes/<codigo>/documentos.md` |
| Linha do histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` (pedido, baixa, cobrança; seção 8.1) |
| Carteira | `carteira.csv`: `documentos_pendentes`, `proximo_contato`, `motivo_proximo_contato`, `atualizado_em`; `fase` só proposta |
| Cobranças no ciclo | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-cobranca-de-documento.md` |
| Correções e régua aprovadas | `aprendizados-experiencia.md`; `cobranca_de_documentos` e `como_o_cliente_manda` na ficha da experiência |
| Treino | `escritorio/07-operacao/_treino/experiencia/clientes/<codigo>/documentos.md` |

Sem pasta aberta: lista, controle e mensagens no chat, com o caminho de cada arquivo; o controle pode virar tabela para a planilha da equipe.

### 8.1 As linhas do histórico

Na tabela de `boas-vindas-do-cliente/assets/historico-modelo.md` (se instalada; sem ela, `Data e hora | Canal | Quem falou | O que foi dito`):
- **Pedido, cobrança, confirmação e "chegou tudo":** linha de contato (`| 2026-04-10 09h20 | whatsapp | secretária | confirmou que a certidão pode vir na segunda |`). Lembrete e cobrança de documento entram no histórico, mas não mudam o `ultimo_contato` da carteira: não informam o caso (`../../docs/agentes-e-fila.md`).
- **O que o escritório fez com os documentos sem falar com o cliente** (conferiu os que chegaram, pediu certidão ao cartório ou cópia ao INSS em nome do cliente): linha de trabalho do escritório, canal `trabalho-do-escritorio` (`| 2026-04-14 11h00 | trabalho-do-escritorio | secretária | conferiu a certidão de casamento e a matrícula do imóvel |`). Também não muda o `ultimo_contato`; aparece na página do caso e no resumo do mês em "o que o escritório fez".

## 9. Solo e equipe

**Solo:** o titular aprova a lista do caso e roda o modo D uma vez por dia, num horário fixo; as cobranças saem do modelo aprovado e os itens para decidir ficam para o fim da semana.

**Equipe:** a secretária pede, dá baixa e cobra; o advogado aprova a lista de cada caso e decide `nao-existe`, régua cumprida e controle travado. Se a mesma pendência aparece em muitos casos (o PPP de empresa que fechou, a certidão que demora), vale um "onde consegue" mais detalhado na lista do tipo de caso.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Pedir pelo nome técnico | Cliente manda o papel errado | "O que é" e "onde consegue" em cada item |
| Pedir a senha do cliente | Risco de segurança e problema ético | Regra fixa 2 |
| Requisito de validade dito de cabeça | Documento recusado | `[CONFERIR]` no cabeçalho interno |
| Cobrança com pressão | Desgaste e cliente que some | Régua da ficha e texto 7.2 |
| Ninguém cobrar | Caso parado sem ninguém ver | Script lê todos os controles e mostra o atraso |
| Cobrar quem pediu só ligação | Incômodo e risco de reclamação | Script marca LIGAÇÃO |
| Carteira dizendo 0 com documento faltando | Rotina não vê a pendência | Contagem do script comparada com a carteira |
| Documento que não existe tratado como atraso | Cobrança sem fim | `nao-existe` vai ao advogado |

## 11. Próximo passo

- Lista fechada: quem conduz o caso define o próximo ato; `status-para-o-cliente` (se instalada) avisa o cliente quando houver movimentação.
- Documento pendente na página do caso: `pagina-do-caso` (se instalada) mostra em "o que depende de você"; sem ela, entra no resumo do mês.
- Cobrança todo dia sem ninguém pedir: `rotina-da-experiencia` (se instalada) e `/motor-experiencia:ciclo`.
- Mensagem nova aprovada: guarde na biblioteca, com a chave da seção 7.

## Referências desta habilidade

Listas-base por tipo de caso, marcadas como exemplo para o escritório confirmar. Leia no modo A e no modo B quando o tipo de caso ainda não tem lista do escritório. Todo requisito segue `[CONFERIR]`.

- `references/listas-base-previdenciario.md`: incapacidade, aposentadoria, atividade especial, rural, BPC, pensão por morte, revisão.
- `references/listas-base-trabalhista.md`: rescisão e verbas, jornada, vínculo sem registro, acidente e doença, assédio, defesa da empresa.
- `references/listas-base-familia.md`: divórcio consensual e litigioso, alimentos, guarda, união estável, inventário.
- `references/listas-base-consumidor.md`: cobrança e negativação, produto e serviço, plano de saúde, transporte aéreo, banco e fraude, serviço essencial.
- `references/listas-base-civel.md`: contrato e cobrança, dívida cobrada, acidente de trânsito, locação, imóvel.
- `scripts/documentos_pendentes.py`: as cobranças do dia e a contagem por cliente. Modo D e ciclo.
