---
name: roteiro-da-consulta
description: >
  Prepara a consulta inicial. Monta o roteiro da consulta por área e tipo de caso (abertura,
  escuta, perguntas de fatos e papéis, o que nunca prometer, os caminhos sem decidir pelo cliente,
  o momento dos honorários, o fechamento e as perguntas prévias). Para cada consulta marcada, monta
  o briefing de uma página, registra consulta-agendada e anota os documentos pedidos antes do
  contrato. Roda a pedido, no ciclo do agente e no modo adaptar, que reescreve os roteiros para o
  nicho. Use quando o advogado disser "monta o roteiro da consulta de
  previdenciário", "como eu conduzo a primeira conversa", "prepara a consulta de amanhã", "briefing
  da consulta da Marta", "o que eu pergunto nesse caso". Não use para decidir se o contato merece
  consulta (use qualificar-contato) nem para registrar o que aconteceu nela (use ata-da-consulta).
---

# Roteiro da consulta

> A consulta inicial é a hora em que o contato vira cliente ou vai embora. O roteiro garante que nada importante fica sem perguntar, que ninguém promete o que não pode e que o cliente sai sabendo o próximo passo. O briefing garante que o advogado não descobre o caso quando o cliente senta na frente dele.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

A consulta das 14h é sobre um auxílio-doença cortado. A advogada abre a conversa sem ter lido a triagem e descobre, aos 35 minutos, que a perícia foi há mais de um ano e que ninguém recorreu. Sobram cinco minutos para falar de honorários, a cliente pergunta "mas eu ganho?" e sai sem saber o que fazer na segunda-feira.

**Regras fixas desta habilidade:**
1. O roteiro organiza a conversa. A estratégia do caso e o "vale a pena entrar com a ação" são do advogado, ditos por ele na consulta.
2. Os roteiros-base de `references/` trazem só perguntas de fatos, datas e papéis, sem tese, e só valem como roteiro do escritório depois que o advogado confirma.
3. Nada de promessa de resultado, de prazo de decisão ou de chance de ganho, nem no roteiro, nem no briefing, nem em mensagem.
4. Honorário na consulta segue a política do escritório. Nenhum valor sai da IA.
5. O briefing leva o mínimo de dados. Gravar ou transcrever a consulta só com o consentimento do cliente, pedido no começo.

## 1. Quando usar

**Use quando:**
- O escritório vai montar, pela primeira vez, o roteiro da consulta de uma área.
- O roteiro existe e precisa de revisão (consulta que deu errado, aprendizado novo, tipo de caso novo).
- Há uma consulta marcada e o advogado quer o briefing antes dela.
- A consulta foi agendada agora e é preciso registrar a etapa `consulta-agendada`.
- O `agente-comercial` chamou para os briefings do dia seguinte, ou a `adaptar-comercial` chamou no modo "adaptar".

**Não use quando:**
- A dúvida é se o contato vai para consulta, com prioridade, encaminhado ou recusado: use `qualificar-contato` (se instalada).
- O pedido é marcar, confirmar, lembrar ou remarcar: use `agenda-da-consulta` (se instalada; sem ela, a confirmação sai do modelo `confirmacao-de-consulta` da biblioteca, seção 6).
- A consulta já aconteceu: use `ata-da-consulta` (se instalada).
- O pedido é a lista de documentos do caso depois do contrato: é da `checklist-de-documentos` do motor-experiencia (se instalado). Antes do contrato, os documentos pedidos ficam no arquivo da consulta.
- O pedido é a proposta de honorários: use `proposta-de-honorarios`.

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir) e `aprendizados-comercial.md`. Aprendizado da `roteiro-da-consulta` vale antes do padrão desta habilidade.
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Se o advogado quiser seguir, pergunte só: "Em que áreas vocês atuam?", "Quanto tempo dura a consulta?" e "Quem faz a consulta?". Use as respostas e ofereça gravar no fim.
3. **Leia o roteiro da área**, se existir: `escritorio/04-base/atendimento-e-triagem/roteiro-consulta-<area>.md`. Se o escritório usa o `inicio-automacao` e existe um `roteiro-triagem-<area>.md` na mesma pasta, leia também: o que a triagem já pergunta não se repete na consulta.
4. **Para o briefing, leia o que já se sabe do contato:** a linha em `escritorio/07-operacao/comercial/contatos.csv`, o cartão da triagem e a seção "Qualificação" em `escritorio/07-operacao/comercial/triagens/`, e o arquivo da consulta, se já existir.
5. **Conta e treino.** Briefing tem dado de cliente: só em conta profissional ou de equipe. Em conta pessoal, use os casos de `../../docs/casos-ficticios.md`, gravando em `escritorio/07-operacao/_treino/comercial/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas` · C: `duracao`, `quem_faz_a_consulta`.
- **Melhora:** E: `casos_mais_comuns`, `nicho` · C: `consulta`, `valor_da_consulta`.

Campo que falta e a tarefa pede: pergunte aquele campo, uma vez, e ofereça gravar. O momento de falar de honorários vem da política do escritório (`proposta-de-honorarios`, se instalada) ou do advogado, na montagem do roteiro.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A. Montar o roteiro | Primeira vez numa área | A área e os tipos de caso | `roteiro-consulta-<area>.md` |
| B. Revisar o roteiro | Depois de consultas, ou com aprendizado novo | O roteiro e as correções | Nova versão do roteiro |
| C. Briefing | Consulta marcada | Código ou nome curto, data e hora | `consultas/<codigo>-AAAA-MM-DD.md` e a linha `consulta-agendada` |
| D. No ciclo | O `agente-comercial` chamou | As linhas `consulta-agendada` do dia útil seguinte | Briefings gravados, nada no chat |
| E. Adaptar | A `adaptar-comercial` chamou | `nicho.md` e os roteiros atuais | Roteiros reescritos para o nicho, com `[ALTERADO]` |

**Modo direto:** "briefing da consulta da C-2026-0001, quinta às 14h, online". Execute, mostre e pergunte só o que falta.

### Modo A. Montar o roteiro da área

**A1. A área.** Pergunte: "Para qual área vamos montar o roteiro primeiro?". Se o `contatos.csv` existir, sugira a área com mais contatos no último mês.

**A2. Os tipos de caso.** Se `casos_mais_comuns` ou o `nicho.md` trazem a lista, mostre e confirme. Se não: "Quais são os três tipos de caso que mais chegam nessa área?".

**A3. Partir do roteiro-base.** Previdenciário, trabalhista, família, consumidor ou cível: leia o roteiro-base em `references/` e mostre as perguntas dos tipos de caso escolhidos, marcadas como proposta, já com as palavras do `nicho.md` (seção "Como ele fala"), se existir. Outra área: use a estrutura da seção 4 e pergunte: "Na última consulta desse tipo, o que você precisou perguntar que o cliente não tinha contado na mensagem?".

**A4. Ajustar parte por parte**, uma pergunta por vez:
1. "Como você costuma abrir a consulta? Se não tiver um jeito, uso o padrão e você ajusta."
2. "Destas perguntas, quais você corta, quais faltam?" (para cada tipo de caso)
3. "Tem alguma frase que você já ouviu de cliente, tipo 'o outro advogado disse que era ganho', que o roteiro precisa tratar?"
4. "Nesse tipo de caso, quais caminhos você costuma explicar?" (a IA não preenche: o roteiro guarda só o nome de cada caminho que o advogado disser)
5. "Em que momento você fala de honorários: no fim da consulta, só se o cliente perguntar, ou depois, na proposta por escrito? Você diz algum valor na consulta?"
6. "O que o cliente precisa levar combinado ao sair?"
7. "Que perguntas valem mandar antes da consulta, por mensagem?" (de 3 a 5 por tipo de caso; regras da `qualificar-contato`, seção 5)

**A5. O tempo.** Divida a `duracao` pelas partes. Exemplo para 40 minutos (só exemplo): abertura 2, escuta 10, perguntas 10, caminhos 8, honorários 5, fechamento 5. Pergunte se faz sentido.

**A6. Mostrar e gravar.** Mostre o roteiro inteiro no formato da seção 6. Com o ok, grave com situação `em uso`. Sem o ok de todas as perguntas, grave como `rascunho`.

### Modo B. Revisar o roteiro

1. Pergunte: "O que aconteceu na consulta que o roteiro não previu?". Peça a cena concreta.
2. Leia os aprendizados da `roteiro-da-consulta` e as atas recentes (a seção "Lacunas" da `ata-da-consulta`, se instalada, mostra o que sempre falta perguntar).
3. Proponha as mudanças marcadas `[NOVO]` ou `[ALTERADO]`. Com o ok, suba a versão e acrescente uma linha em "Mudanças".

### Modo C. Briefing de uma consulta marcada

**C1. Identificar.** "Qual é o código ou o primeiro nome do contato, e o dia e a hora da consulta?". Nome que aparece em mais de uma linha: mostre as opções.

**C2. Juntar o que existe.** Cartão da triagem, qualificação e respostas às perguntas prévias. Se as respostas vieram pelo WhatsApp: "Cola aqui o que ele respondeu?".

**C3. Escolher o roteiro.** Sem roteiro da área: "Quer montar o roteiro agora (uns 10 minutos) ou sigo com o roteiro-base, marcado como não confirmado?".

**C4. Montar o briefing** no formato da seção 6, em uma página. O que veio do contato entra como "segundo o contato". Data que pode indicar prazo vai em "Datas que importam" com `[CONFERIR]`, sem cálculo. Das perguntas do roteiro, entram só as que a triagem e as respostas ainda não cobriram, até oito.

**C5. Documentos pedidos antes do contrato.** O que a pessoa traz ou manda antes da consulta sai da lista "Documentos para a consulta" do roteiro, ou da seção "Documentos típicos" do `nicho.md`. Lista curta; nada de documento sensível por mensagem. Anote na seção "Documentos pedidos antes do contrato" do arquivo da consulta: o que foi pedido, quando, o que chegou.

**C6. Registrar.** Proponha: `etapa` = `consulta-agendada`, `responsavel` = quem faz a consulta, `proximo_passo` = "fazer consulta", `data_proximo_passo` = dia da consulta, `atualizado_em` = hoje. Mostre e grave com o ok. Remarcação segue `../../docs/funil.md`, regra 6 ("Remarcação").

**C7. Confirmação ao contato.** É da `agenda-da-consulta` (se instalada). Sem ela, monte a confirmação da seção 6 a partir do modelo `confirmacao-de-consulta` da biblioteca (`escritorio/04-base/comercial/biblioteca-comercial.md`), sigla A, e mostre para quem atende ler e enviar. Com conector de agenda, só leitura para conferir dia, hora e link; mudar compromisso só com o ok do advogado.

### Modo D. No ciclo (chamada pelo agente)

1. Não mostre nada no chat. Para cada linha `consulta-agendada` com `data_proximo_passo` no próximo dia útil, rode C2 a C5 e grave o briefing no arquivo da consulta, com a nota "briefing preparado pelo ciclo, a advogada lê antes".
2. Sem `agenda-da-consulta` instalada e sem confirmação registrada, a confirmação vira rascunho na fila: `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-confirmacao-de-consulta.md`, no formato de `../../docs/agentes-e-fila.md`, com `tipo: confirmacao-de-consulta` e `revisor: pendente`, e passa pelo `revisor-comercial`. Link da videochamada fica `{LINK DA VIDEOCHAMADA}` para quem envia.
3. Consulta de contato com vulnerabilidade, parada imediata, `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:` (marcador de pessoa, `funil.md`, regra 4) ou `pediu_para_parar = sim`: briefing sim, rascunho para o contato não. Vai para "PESSOA AGORA" ou "PARA DECIDIR" no resumo.
4. O ciclo não mexe na etapa nem marca consulta: no registro, só as colunas que `funil.md` permite ao agente (regra 11).
5. **Saída de PESSOA AGORA.** Depois que a pessoa falou com o contato, o comando `fila` pergunta "Já falou? O que ficou combinado?" e troca o `proximo_passo` que começa com `pessoa agora:` ou `pessoa liga:` pelo combinado, com data (`agentes-e-fila.md`). O briefing ganha uma linha em "Alertas" com o combinado. Sem isso, o item volta ao topo do resumo seguinte.

### Modo E. Adaptar (chamada pela adaptar-comercial)

1. Leia `escritorio/04-base/comum/nicho.md` inteiro.
2. Para cada roteiro da área em uso (ou roteiro-base, se ainda não houver), reescreva: as perguntas com as palavras de "Como ele fala"; um tipo de caso para cada linha de "Os casos que chegam"; "Documentos para a consulta" a partir de "Documentos típicos"; alertas a partir de "Os momentos de aflição" e "Cuidados do nicho"; e, na tabela "não diga, diga", os erros que "O que este nicho pesquisa sozinho" traz.
3. Mostre cada mudança marcada `[ALTERADO]` ou `[NOVO]`. Prazo de fase vindo do nicho continua `[CONFERIR]` e nunca vira promessa.
4. Grave só com o ok, como nova versão, com a linha em "Mudanças". Devolva à `adaptar-comercial` a lista do que mudou.

### Passo final. Aprender

Pergunte: "Alguma coisa no roteiro ou no briefing você faria diferente?". Cada correção vira regra curta (por exemplo, "Consulta de divórcio: perguntar no começo se há filhos menores") e, com o ok, entra em `escritorio/04-base/comum/aprendizados-comercial.md` (`../../docs/aprender-com-o-uso.md`). Se a correção muda a conduta da área inteira, ofereça subir para o roteiro como nova versão. Se muda a `duracao` ou a política de consulta, ofereça gravar na ficha.

## 4. O roteiro: as sete partes

| Parte | Para que serve | O que o advogado faz | Tempo (exemplo, 40 min) |
|---|---|---|---|
| 1. Abertura | Deixar a pessoa à vontade e combinar a conversa | Apresenta-se, diz quanto tempo têm, como a consulta funciona e pede consentimento se for gravar | 2 |
| 2. Escuta | Ouvir o caso do jeito do cliente | Deixa contar sem interromper, anota, repete o que entendeu | 10 |
| 3. Perguntas | Completar fatos, datas e papéis | Faz as perguntas do tipo de caso que a escuta não respondeu | 10 |
| 4. Caminhos | Mostrar as opções sem decidir pelo cliente | Explica cada caminho que vê, os riscos e o que depende de quem | 8 |
| 5. Honorários | Falar do valor com clareza e dignidade | Segue a política do escritório, no momento combinado | 5 |
| 6. Fechamento | Sair com combinados | Recapitula o que cada um faz e até quando | 5 |
| 7. Depois | Não perder o que foi dito | Anota ou dita o essencial para a ata | fora da consulta |

### 4.1 Abertura (frases de exemplo para o advogado ajustar)

- "Obrigada por vir. A gente tem uns [DURAÇÃO]. Primeiro eu quero ouvir você, depois faço algumas perguntas e no fim te explico o que eu vejo e quais são os próximos passos."
- Consulta paga, se a ficha disser: "Como combinado, a consulta é paga [e o valor é abatido se você contratar o escritório]."
- Gravação: "Posso transcrever a nossa conversa para não perder nenhum detalhe? Fica só com o escritório. Se preferir que não, eu anoto." Sem o sim, não grava.
- Quem acompanha: se veio outra pessoa (a filha pela mãe), confirme quem é o cliente e se ele quer o acompanhante presente.

### 4.2 Escuta

- "Me conta o que aconteceu, do seu jeito, desde o começo."
- Não interromper nos primeiros minutos. Anotar datas e nomes.
- Espelho: "Deixa eu ver se entendi: [resumo em três frases]. É isso?"
- Aflição forte, choro, relato de violência: o roteiro para. O advogado acolhe e, se houver risco imediato, a orientação é procurar ajuda de emergência: 190, 180 (violência contra a mulher), 188 (CVV) ou 192 `[CONFERIR]` os números vigentes.

### 4.3 Perguntas por tipo de caso

Vêm do roteiro da área (ou do roteiro-base, até o advogado confirmar). Perguntas de fato: o quê, quando, quem, onde está o papel. Nenhuma pergunta de tese. Ordem: datas primeiro (para o advogado ver prazo), depois papéis, depois o que a pessoa já tentou.

### 4.4 O que nunca prometer

| Não diga | Diga |
|---|---|
| "Seu caso é ganho." | "Pelo que você contou, existe um caminho. Garantir resultado ninguém pode: depende das provas e de quem decide." |
| "Em seis meses está resolvido." | "Não tenho como prometer prazo. Posso te explicar as fases, e eu te aviso a cada novidade." |
| "Você vai receber uns [VALOR]." | "Valor, só depois de olhar os documentos e fazer a conta. Um número agora pode errar para mais ou para menos." |
| "Esse juiz sempre decide assim." | "Cada caso é olhado pelo que tem nele." |
| "O advogado anterior errou." | "Vou olhar o que foi feito e te digo o que dá para fazer a partir daqui." |
| "Não tem risco nenhum." | Os riscos que existem: tempo, despesas, possibilidade de pagar custas e honorários da outra parte `[CONFERIR]`. |
| "A IA te falou certo." | "Essa resposta vem de um caso geral. Vou olhar o seu com os seus papéis e te digo o que vale para você." |

Se o cliente diz que outro profissional prometeu resultado, o roteiro não comenta o colega: o advogado explica por que ele mesmo não promete.

### 4.5 Explicar os caminhos sem decidir pelo cliente

O roteiro guarda a forma. Quais caminhos existem em cada caso, quem diz é o advogado. Para cada caminho, cinco pontos, em linguagem simples: o que é; o que precisa; como costuma ser o tempo, sem prometer data; o que pode dar errado e o que custa `[CONFERIR]`; o que acontece se não fizer nada. Depois, o advogado pode dizer qual recomendaria e por quê. A decisão é do cliente, informado: "Esses são os caminhos que eu vejo. Se fosse para escolher, eu iria por [CAMINHO], porque [MOTIVO]. Mas quem decide é você."

### 4.6 Honorários: o momento e o jeito

| Política do escritório | Momento | Como falar |
|---|---|---|
| Valor dito na consulta | Depois dos caminhos | "Para esse trabalho, o escritório cobra [MODELO]. Eu te mando tudo por escrito até [DATA], com o que está incluído e o que não está." |
| Só proposta por escrito | No fechamento | "Vou montar a proposta com calma e te mando até [DATA], com o valor, o que está incluído e as formas de pagamento." |
| Depende do caso | O advogado decide na hora | O roteiro lembra as duas frases acima |

- Preço logo no começo: "A gente fala disso antes de você sair. Primeiro preciso entender o caso para saber o tamanho do trabalho."
- Desconto na hora: "Prefiro te mandar por escrito, com calma, e aí a gente conversa sobre a forma de pagamento." Nada de leilão de preço.

### 4.7 Fechamento

Três combinados, ditos em voz alta e anotados: o que o cliente faz e até quando; o que o escritório faz e até quando; quando voltam a falar e por qual canal. "Para eu ter certeza de que fui claro: me diz com suas palavras o que a gente combinou?"

## 5. Exemplos resolvidos (Escritório Modelo, casos fictícios)

**Caso 1, modo C.** C-2026-0001, Marta, previdenciário, auxílio-doença cortado. Consulta marcada para quinta, 2026-03-12, às 14h, online. Briefing (trecho):

```
BRIEFING DA CONSULTA · C-2026-0001 · Marta
Quando: 2026-03-12 14:00 · Online · Advogada titular · 40 min
Área e tipo de caso: previdenciário · benefício por incapacidade cortado
Roteiro: roteiro-consulta-previdenciario.md v1 · Prioridade: alta (benefício cortado)
1. O caso (segundo o contato): recebia auxílio-doença; cortado na semana
   passada; diz que segue sem condição de trabalhar.
2. Datas: corte "semana passada" [A CONFIRMAR a data da carta]. Alerta de
   prazo aparente [CONFERIR].
3. O que quer: voltar a receber. Perguntou quanto custa.
5. Documentos pedidos antes do contrato: carta do INSS; laudos recentes
   (trazer na consulta, não mandar por mensagem).
6. Alertas: pode estar sem renda [A CONFIRMAR].
7. Perguntas que faltam: desde quando está afastada; profissão; fez perícia
   antes do corte; tem outra renda em casa.
```

Registro: `consulta-agendada`, responsável advogada titular, próximo passo "fazer consulta", data 2026-03-12.

**Caso 7, modo C.** C-2026-0007. Quem escreveu foi a Helena, pela mãe de 72 anos. O briefing abre com "quem fala por quem": a cliente é a mãe; confirmar se ela participa e se autoriza a filha `[A CONFIRMAR]`. A advogada liga antes para combinar o melhor formato para a mãe e decide a isenção da consulta.

**Caso 5.** C-2026-0005, Renata, divórcio consensual, "é rápido?". O briefing traz em "Expectativa já dita": "acha que é rápido". O roteiro lembra a advogada de explicar as fases sem prometer prazo.

**Caso 11.** C-2026-0011, Diego, revisão vista em vídeo e "confirmada" por uma IA. O briefing traz o alerta "expectativa vinda de vídeo e de resposta de IA" e a linha da tabela 4.4 para a IA.

## 6. Formato da saída

**O roteiro da área** (`roteiro-consulta-<area>.md`):

```
---
documento: Roteiro da consulta · [ÁREA]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
situacao: rascunho | em uso
---
# Roteiro da consulta · [ÁREA]
Duração: [duracao] · Quem faz: [quem_faz_a_consulta] · Tipos de caso: [lista] · Nicho: [nicho.md v N, ou "sem nicho"]
## 1. Abertura (frases do escritório)
## 2. Escuta
## 3. Perguntas por tipo de caso
### [Tipo de caso]
- Fatos e datas: ...
- Documentos para a consulta: ...
- Alertas para o advogado: ...
- Caminhos que o advogado costuma explicar: [A PREENCHER pelo advogado]
## 4. O que nunca prometer (a tabela, com as frases do escritório)
## 5. Caminhos: a forma da explicação
## 6. Honorários: momento e frases
## 7. Fechamento: os três combinados
## Perguntas prévias (de 3 a 5 por tipo de caso, para mandar antes da consulta)
## Mudanças
- 1 · AAAA-MM-DD · criado
```

**O briefing** (início do arquivo `consultas/<codigo>-AAAA-MM-DD.md`, no máximo uma página):

```
# Consulta · [CÓDIGO] · [AAAA-MM-DD]
## Briefing
Quando · Formato · Quem faz · Duração · Roteiro usado · Origem e canal · Prioridade
1. O caso em cinco linhas (segundo o contato)
2. Datas que importam (alerta de prazo aparente [CONFERIR], sem cálculo)
3. O que a pessoa quer, nas palavras dela
4. Respostas às perguntas prévias (ou "não enviadas" ou "sem resposta")
5. Documentos: já tem · pedimos para trazer · já chegaram
6. Alertas: vulnerabilidade · quem fala por quem · conflito de interesse
   [A CONFIRMAR] · outro advogado no caso · expectativa já dita
7. Perguntas do roteiro que faltam (até 8)
8. Honorários nesta consulta: paga? já paga? abate? como a política manda falar
9. Em aberto [A CONFIRMAR]
## Documentos pedidos antes do contrato
| Documento | Pedido em | Por qual canal | Chegou em |
```

A seção "Ata" (da `ata-da-consulta`) entra depois, no mesmo arquivo.

**A confirmação ao contato (A, só sem a agenda-da-consulta):**

```
Oi, [NOME], tudo bem? Sua consulta está marcada:
[DIA DA SEMANA], [DATA], às [HORA], [no endereço ... | por vídeo, neste link: {LINK DA VIDEOCHAMADA}].
Ela dura cerca de [DURAÇÃO], com [QUEM FAZ].
Se puder, traga: [LISTA CURTA].
Se precisar remarcar, é só avisar por aqui.
[ASSINATURA]
```

O dia e a hora vêm do registro, porque a consulta já está marcada; a habilidade preenche todos os colchetes com a ficha e o registro, e nada entre colchetes vai ao contato. O link da videochamada fica entre chaves: quem envia cola na hora, e a fila não deixa marcar `enviado` com chave no texto. Data ainda não marcada é da `agenda-da-consulta` (se instalada), que deixa `{DIA E HORA}` para quem confirma.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Roteiro da área (inclui as perguntas prévias) | `escritorio/04-base/atendimento-e-triagem/roteiro-consulta-<area>.md` (área sem acento: `previdenciario`, `familia`, `civel`) |
| Briefing e documentos pedidos antes do contrato | `escritorio/07-operacao/comercial/consultas/<codigo>-AAAA-MM-DD.md` (a data é a da consulta) |
| Rascunho de confirmação no ciclo | `escritorio/07-operacao/comercial/fila/AAAA-MM-DD/NN-<codigo>-confirmacao-de-consulta.md` |
| Linha do funil | `escritorio/07-operacao/comercial/contatos.csv`: `etapa`, `responsavel`, `proximo_passo`, `data_proximo_passo`, `atualizado_em` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Treino | `escritorio/07-operacao/_treino/comercial/` |

Consulta remarcada: renomeie o arquivo para a nova data e acrescente no topo "Remarcada de AAAA-MM-DD". Sem pasta aberta: entregue tudo no chat, com o caminho de cada arquivo.

## 8. Solo e equipe

**Solo:** o titular monta o roteiro uma vez por área e lê o briefing na véspera, num horário fixo. Com o tempo, o roteiro vira o jeito do escritório e o titular só consulta as partes de honorários e de promessas.

**Equipe:** a secretária gera o briefing e cuida da confirmação. Quem faz a consulta lê e ajusta. Com vários advogados, cada área tem um dono do roteiro, e o roteiro é o mesmo para todos. Consulta que sempre estoura o tempo costuma ter problema na escuta ou nas perguntas: revise o roteiro com quem atende.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Advogado conhece o caso só na consulta | Metade do tempo vai em perguntar o que a triagem já sabia | Briefing de uma página, lido antes |
| Prometer resultado ou prazo | Cliente frustrado, risco ético | Tabela "não diga, diga" |
| Roteiro com tese pronta | A IA decide a estratégia no lugar do advogado | Roteiros-base só com fatos e papéis |
| Decidir pelo cliente | Cliente que não entendeu o risco e depois cobra | Cinco pontos por caminho e "quem decide é você" |
| Honorário nos últimos dois minutos | Cliente sai sem saber o preço, ou com desconto sob pressão | Momento definido pela política |
| Documento pedido antes do contrato que ninguém controla | Consulta sem o papel, ou papel sensível no WhatsApp | Seção "Documentos pedidos antes do contrato" e lista curta |
| Roteiro genérico para um nicho específico | Pergunta que o cliente não entende | Modo adaptar com as palavras do `nicho.md` |
| Gravar sem avisar | Quebra de confiança e problema de dados | Consentimento na abertura |

## 10. Próximo passo

- Consulta feita: `ata-da-consulta` (se instalada) monta a ata no mesmo arquivo. Sem ela, anote os combinados na seção "Ata" e mude a etapa para `consulta-feita`.
- Confirmar, lembrar, remarcar ou registrar falta: `agenda-da-consulta` (se instalada); sem ela, a pessoa faz pela biblioteca.
- Cliente quer a proposta: `proposta-de-honorarios`.
- Faltou à consulta: a pessoa marca `nao-compareceu` e o `follow-up` (se instalada) cuida do retorno; sem ela, uma mensagem curta oferecendo nova data.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

Os roteiros-base são exemplos para o escritório confirmar. Leia no passo A3, no passo C3 (área sem roteiro do escritório) e no modo E, como ponto de partida da adaptação. Nenhum vale como roteiro do escritório até o advogado confirmar, pergunta por pergunta.

- `references/roteiro-base-previdenciario.md`: incapacidade, aposentadoria, BPC, pensão por morte, revisão.
- `references/roteiro-base-trabalhista.md`: demissão e verbas, jornada, vínculo sem registro, acidente e doença, assédio, e a parte para quem atende empresa.
- `references/roteiro-base-familia.md`: divórcio consensual e litigioso, alimentos, guarda e convivência, união estável, inventário.
- `references/roteiro-base-consumidor.md`: cobrança e negativação, produto e serviço, plano de saúde, transporte aéreo, banco e fraude.
- `references/roteiro-base-civel.md`: contrato e cobrança, dívida cobrada, indenização por dano, locação, imóvel.
