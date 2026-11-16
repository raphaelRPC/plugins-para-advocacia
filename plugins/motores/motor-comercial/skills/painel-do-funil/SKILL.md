---
name: painel-do-funil
description: >
  Monta o painel do mês do comercial a partir do registro de contatos (contatos.csv): entradas por
  origem, área e canal, quantos chegaram a cada etapa e a conversão entre elas, tempo até a primeira
  resposta e quem está sem resposta, propostas e valor, fechamentos, motivos e etapa da perda, quem
  pediu para parar e a qualidade do registro. Roda um script que nunca conta treino e, se pedido,
  gera a versão HTML para abrir como artefato do Claude, só para uso interno. Depois dos números, faz
  três leituras e três ações, sem inventar causa. Use quando o advogado disser "painel do mês",
  "como foi o comercial em março", "de onde vêm os clientes que fecham", "quantas propostas a gente
  mandou", "por que estamos perdendo contato", "fecha o mês do comercial". Não use para a lista do
  dia (use rotina-comercial) nem para a qualidade das conversas (use auditar-conversas-comerciais).
---

# Painel do funil

> Uma vez por mês, os números do comercial numa página: de onde veio quem procurou, até onde cada um chegou, quem ficou sem resposta, quanto foi proposto e fechado. Depois do número, três leituras honestas e três ações com dono.

Regras comuns: `../../docs/regras.md` (painel interno: seção 6.1). Campos das fichas: `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Aprender: `../../docs/aprender-com-o-uso.md`.

É dia 1º e a advogada quer saber se o Instagram "está trazendo cliente". A impressão dela é que sim, porque o celular não para. O registro mostra 9 contatos do Instagram e 2 fechamentos, contra 6 indicações e 3 contratos, e um contato de 2026-03-12 que até hoje não recebeu resposta de ninguém. O número não diz por quê. Diz qual pergunta fazer na reunião de segunda.

**Regras fixas desta habilidade:**
1. Número vem do registro, pelo script ou pela contagem de `references/regras-do-calculo.md`. Nada estimado, arredondado para impressionar ou comparado com "o mercado".
2. Causa que o dado não mostra vira pergunta. "O Instagram traz curioso" é hipótese, e sai como pergunta ao advogado.
3. Com menos de 10 casos numa passagem, o painel mostra "x de y", nunca percentual. Com menos de 20 contatos no mês, avisa e sugere o trimestre.
4. O painel fala de contatos pelo código. Nome, assunto e qualquer dado sensível ficam fora, também na versão HTML, que é interna e nunca vai para cliente nem tem o link compartilhado.
5. Treino nunca entra no painel do escritório. Ação proposta tem dono, prazo e habilidade, e nada vira regra sem o ok do advogado.

## 1. Quando usar

**Use quando:**
- O mês fechou e o advogado quer ver o comercial numa página.
- A equipe vai se reunir para decidir onde pôr esforço: canal, área, tempo de resposta, retorno.
- O advogado quer saber de onde vêm os clientes que fecham, ou por que tantos contatos param no meio.
- A `rotina-comercial` lembrou, no primeiro dia útil do mês, que o painel do mês anterior está pendente.
- A `adaptar-comercial` chamou no modo "adaptar".

**Não use quando:**
- O pedido é o que fazer hoje (sem resposta, consultas e retornos do dia): use `rotina-comercial` ou `/motor-comercial:status`.
- O pedido é saber se as conversas seguem o tom, os prazos e a ética: use `auditar-conversas-comerciais` (se instalada).
- O pedido é a carteira de clientes ativos: é o `painel-da-carteira` do motor-experiencia (se instalado).

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir) e `aprendizados-comercial.md`. Aprendizado do painel ("contato de cliente antigo entra como origem cliente-antigo", por exemplo) vale antes do padrão desta habilidade.
2. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`). Sem registro, não há painel: diga que o funil aparece depois das primeiras triagens e ofereça a `triar-contato`. Quem usa CRM pode colar a exportação no formato de `../../docs/funil.md`.
3. **Leia o painel anterior** (`escritorio/07-operacao/comercial/painel/`), se existir. As ações do mês passado são o primeiro assunto: foram feitas? Mudaram o número?
4. **Conta.** O registro tem o mínimo de dados, mas é dado de cliente. Em conta pessoal, rode só com o registro de treino (`escritorio/07-operacao/_treino/comercial/contatos.csv`, opção `--treino`), que sai marcado TREINO e nunca se mistura com o real.
5. **Onde roda o script.** No Cowork, no app desktop com pasta aberta ou no Claude Code, rode `scripts/painel.py`. No chat com execução de código ligada (conferir na configuração da conta), suba o csv e rode ali. Sem nenhum dos dois, conte por `references/regras-do-calculo.md` e marque no topo: "contado sem o script, conferir".

### Campos da ficha que esta habilidade usa

- **Precisa:** C: `origem_dos_contatos`.
- **Melhora:** C: `motivos_de_perda_comuns`, `primeira_resposta_contato_novo`.

`origem_dos_contatos` vazio: pergunte "Por onde chegam os contatos de vocês? Me diga as opções que vocês usam no registro." e ofereça gravar. `primeira_resposta_contato_novo` vazio: o painel mede o tempo, mas não diz se está no prazo. O script também aproveita, se preenchidos, o horário de atendimento e as áreas da ficha do escritório, para as horas úteis e a conferência da coluna `area`.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Direto | "Painel de março" e o registro está na pasta | O mês (AAAA-MM) | O painel completo, para revisar e gravar |
| Entrevista | Primeiro painel, ou o advogado não sabe o que quer olhar | As perguntas do passo 1 | O mesmo painel, com a pergunta do mês no topo |
| Registro colado | Sem pasta aberta, ou CRM próprio | O csv ou a tabela colada | O painel no chat, com o caminho onde ficaria |
| Trimestre | Menos de 20 contatos por mês | AAAA-MM:AAAA-MM | O painel do período, comparado ao anterior |
| Adaptar | A `adaptar-comercial` chamou | `nicho.md` e a ficha | Opções de origem, motivos de perda e cortes do painel para o nicho (passo 9) |

O painel não roda no ciclo do agente: é interno e mensal, e a `rotina-comercial` só lembra que ele está pendente.

### Passo 1. Combinar o mês e a pergunta
- Modo direto: confirme o mês em uma linha e siga.
- Entrevista, uma pergunta por vez: "Qual mês você quer ver?" e "Tem alguma pergunta que o painel deve responder? Por exemplo: o Instagram traz cliente, as propostas estão paradas, a gente demora para responder."
- Mês em curso: "O mês está em curso. Posso fazer até hoje, mas a comparação fica torta. Prefere esperar o primeiro dia útil do mês seguinte?"

### Passo 2. Conferir o registro antes de contar
- `codigo`, `entrada` e `etapa` são obrigatórias: sem elas, o script para com código 1 e diz qual falta. Mostre a primeira linha de `../../docs/funil.md`.
- As outras colunas do funil (incluindo `primeira_resposta` e `perdido_na_etapa`) são colunas normais do registro. Faltou alguma: o script avisa em "Cuidados" o que ficou sem medir. Sugira acrescentar no fim da primeira linha.
- Registro com dado que não devia estar ali (telefone, CPF, detalhe de saúde no `assunto`): avise, não repita e sugira limpar a linha.
- Caminho com `_treino`: o script recusa, a não ser com `--treino`. Painel de treino nunca vai para `07-operacao/comercial/painel/`.

### Passo 3. Rodar os números
```
python3 "<PASTA DA HABILIDADE>/scripts/painel.py" escritorio/07-operacao/comercial/contatos.csv AAAA-MM \
  --prazo-horas "[primeira_resposta_contato_novo]" --horario "[horario_de_atendimento]" --dias seg-sex \
  --origens "[OPÇÕES DE origem_dos_contatos]" --areas "[ÁREAS DA FICHA]" \
  --md escritorio/07-operacao/comercial/painel/AAAA-MM-numeros.md
```
- `<PASTA DA HABILIDADE>` é a pasta onde está este SKILL.md (no Claude Code com o plugin: `${CLAUDE_PLUGIN_ROOT}/skills/painel-do-funil`). Rode da pasta de trabalho, a que contém `escritorio/`.
- Valores entre colchetes saem das fichas, copiados como estão escritos: `--horario "dias úteis, das 9h às 18h"` ou `"8h30 às 12h e 14h às 18h"` (sábado com horário próprio, como `"dias úteis das 9h às 18h; sábado das 9h às 12h"`, entra na conta), e `--prazo-horas "até 2 horas úteis"`, `"1h30"` ou `2`. Prazo que não é em horas ("no mesmo dia"): o script para e pede o número de horas úteis; pergunte ao advogado. Campo vazio ou `[A PREENCHER]`: no prazo, o painel sai sem a conta do prazo e avisa em "Cuidados"; no horário, o script para e pede o campo.
- O script imprime o markdown dos números e grava `painel/AAAA-MM-numeros.csv` ao lado do registro (`--xlsx` grava também a planilha, se o `openpyxl` existir).
- Saída com código 1 é erro de verdade (arquivo que falta, vazio, coluna obrigatória, treino sem a opção): mostre a mensagem e não monte painel nenhum.

### Passo 4. Mostrar os cuidados primeiro
Mostre a seção "Cuidados antes de ler": mês em curso, primeiro mês do registro, amostra pequena, contatos antigos, em andamento, perdidos sem etapa, colunas que faltam, tempo medido em parte. Leitura que depende de um número com cuidado leva o cuidado junto.

### Passo 5. Três leituras
No formato da seção 4. Para escolher: a pergunta que o advogado trouxe; quem está sem resposta agora (seção 3 do script, sempre que houver alguém), com os que estavam em PESSOA AGORA e não têm a conversa registrada ("Com uma pessoa, sem retorno registrado"), que vêm primeiro; o maior desvio (passagem com a menor taxa, origem com muitas entradas e poucos fechamentos, canal com o maior tempo); o que mudou em relação ao mês anterior, se a amostra deixar. O que o número não permite afirmar vira pergunta, tirada de `references/como-ler-o-painel.md`.

### Passo 6. Três ações
Uma por leitura: o que fazer (com verbo), por quê (o número), quem (função da ficha), até quando (`[A DEFINIR]` se ninguém disse) e a habilidade que cuida.

### Passo 7. A versão HTML (opcional, uso interno)
Se o advogado quiser ver o painel como página:
1. Rode de novo com `--html escritorio/07-operacao/comercial/painel/AAAA-MM.html`. A página tem só códigos, números e os cuidados, com o aviso "uso interno" no topo, modo claro e escuro e leitura no celular.
2. Onde for possível publicar artefatos do Claude (conferir na configuração da conta), abra o arquivo como artefato privado. O link não é compartilhado com ninguém, nem com cliente, nem em grupo; quem do escritório precisa ver abre o arquivo da pasta. Sem artefato, abra o .html no navegador.
3. Leituras e ações ficam no `AAAA-MM.md`; a página mostra só os números.

### Passo 8. Mostrar, ajustar e gravar
Mostre o painel inteiro: cuidados, números, leituras, ações, perguntas. Pergunte: "Alguma leitura você faria diferente? Alguma ação não cabe agora?". Ajuste e grave com o ok em `escritorio/07-operacao/comercial/painel/AAAA-MM.md`.

### Passo 9. Modo "adaptar" (chamada pela adaptar-comercial)
1. Leia `nicho.md`: "Os casos que chegam", "Sazonalidade e ritmo", "Quem é o cliente" (como chega ao escritório).
2. Proponha: as opções de `origem_dos_contatos` que o nicho usa (por exemplo, "sindicato", "pastoral", "contador parceiro", se for assim que os contatos chegam); os `motivos_de_perda_comuns` do nicho; e os cuidados de leitura do nicho (o corte continua por `area`, porque o `assunto` nunca entra no painel; a sazonalidade vira um cuidado fixo, como "compare com o mesmo mês do ano anterior").
3. Mostre cada mudança marcada `[ALTERADO]` ou `[NOVO]`. Com o ok, grave na ficha comercial (com linha no histórico) e as regras de contagem nos aprendizados. Devolva a lista do que mudou.

### Passo 10. Aprender
Pergunte: "Tem algo que eu deveria contar diferente nos próximos meses?". Correção vira regra curta e, com o ok, entra em `aprendizados-comercial.md`. Exemplos: "Contato de cliente antigo entra como origem cliente-antigo, nunca como indicação"; "No painel, separar previdenciário administrativo do judicial". Opção nova de origem ou motivo de perda que sempre aparece: ofereça gravar na ficha.

## 4. Como ler

### 4.1 Formato de cada leitura

```
Leitura [N]. [Título curto, com o número]
O número: [o que o painel mostra, com "x de y"]
O que dá para dizer: [só o que o número sustenta]
O que não dá para dizer: [a causa provável que o dado não mostra]
Pergunta: [a pergunta que resolve, para quem ela vai]
```

### 4.2 Afirmação e pergunta

| O painel mostra | Pode afirmar | Não pode afirmar (vira pergunta) |
|---|---|---|
| 9 contatos do Instagram, 2 fechamentos | "No mês, 2 de 9 do Instagram fecharam." | "O Instagram traz curioso." Pergunta: "O que os contatos do Instagram pediam na primeira mensagem?" |
| Proposta enviada > fechado: 6 de 13 | "6 de 13 fecharam; 6 seguem em aberto." | "O preço está alto." Pergunta: "Nas perdidas, o motivo registrado foi preço?" |
| 3 contatos sem resposta, um há 119 h úteis | "Três contatos não receberam resposta de uma pessoa." | "A secretária esqueceu." Pergunta: "O rascunho deles foi para a fila? Quem aprovou?" |
| 2 com uma pessoa, sem retorno registrado | "Dois contatos de PESSOA AGORA não têm a conversa registrada." | "Ninguém ligou." Pergunta: "A ligação aconteceu? O combinado foi contado ao comando `fila`, que grava a `primeira_resposta` e troca o `proximo_passo`?" |
| Canais fora do WhatsApp com mediana acima do prazo | "E-mail, direct e site demoram mais." | "Ninguém liga para o e-mail." Pergunta: "Quem olha esses canais, e em que horário?" |

### 4.3 Ação boa e ação ruim

| Ruim | Boa |
|---|---|
| "Responder mais rápido" | "Incluir e-mail, direct e site nas leituras fixas das 9h e das 14h. Quem: secretária. Habilidade: rotina-comercial." |
| "Melhorar o Instagram" | "Ler as 9 primeiras mensagens do Instagram de março e marcar o que cada uma pedia. Quem: advogada. Habilidade: auditar-conversas-comerciais (se instalada)." |
| "Baixar o preço" | "Conferir a proposta perdida por preço contra a política de honorários antes de mexer em valor. Quem: advogada. Habilidade: objecoes-comerciais (se instalada)." |

Ação que o painel nunca propõe: desconto como isca, abordagem a quem não procurou o escritório, mensagem para quem pediu para parar, comparação com colegas.

## 5. Exemplo resolvido · Escritório Modelo (registro fictício)

Registro de treino com 31 linhas, todas com entrada em 03/2026, primeiro mês do registro. As onze primeiras são os casos de `../../docs/casos-ficticios.md` (C-2026-0001 Marta a C-2026-0011 Diego; a Fernanda, caso 12, é cliente e não entra). Rodado com `--prazo-horas 2`, as cinco origens da ficha e `--hoje 2026-03-31`.

| Origem | Entraram | Chegaram à proposta | Fecharam |
|---|---|---|---|
| google | 10 | 4 | 1 |
| instagram | 9 | 3 | 2 |
| indicacao | 6 | 4 | 3 |
| cliente-antigo | 2 | 2 | 0 |

Funil: 30 de 31 triados; 19 de 28 atendíveis agendaram; 16 de 19 fizeram a consulta; 13 de 15 com caso receberam proposta; 6 de 13 fecharam; 16 ainda em andamento. Primeira resposta: mediana de 24 minutos úteis, 22 de 28 no prazo de 2 horas. Sem resposta de uma pessoa: C-2026-0011 (119,2 h úteis), C-2026-0027 (27,0 h), C-2026-0030 (9,5 h).

**Leitura 1. Três contatos sem resposta, um desde 2026-03-12.** Dá para dizer que o C-2026-0011 foi triado, teve a régua armada e nunca recebeu resposta de uma pessoa: `primeira_resposta` vazia. Não dá para dizer onde parou. Pergunta para a secretária: "O convite dele chegou à fila? Foi aprovado e não enviado?"

**Leitura 2. Indicação fechou 3 de 6; Instagram, 2 de 9; Google, 1 de 10.** Dá para dizer que, em março, quem chegou por indicação foi mais longe. Não dá para dizer que o Google traz contato pior: amostra pequena, primeiro mês, e vários ainda em andamento. Pergunta para a advogada: "O que os contatos do Google pediam na primeira mensagem, e eram de área atendida?"

**Leitura 3. 6 de 28 primeiras respostas fora do prazo; e-mail, direct do Instagram e site com mediana acima de 2 horas, contra 20 minutos no WhatsApp.** Dá para dizer que o atraso se concentra fora do WhatsApp. Não dá para dizer por quê. Pergunta para a equipe: "Quem olha e-mail, direct e site, e em que horário?"

**Ações:** (1) responder hoje os três sem resposta pela `triar-contato` e pela fila, e conferir com a `rotina-comercial` por que o C-2026-0011 não apareceu no resumo do dia, secretária, hoje; (2) incluir e-mail, direct e site nas leituras fixas, secretária, até `[A DEFINIR]`, `rotina-comercial`; (3) corrigir 7 linhas do registro (código repetido, origem vazia, origem "tiktok" fora da ficha, área "tributario" que devia ser `fora-da-area`, perdido sem motivo, perdido sem `perdido_na_etapa`, dois fechados sem valor que podem ser só de êxito), secretária, esta semana.

A saída completa do script, sem edição, está em `references/como-ler-o-painel.md`, seção 5.

## 6. Formato da saída

```markdown
---
documento: Painel do funil AAAA-MM
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Painel do funil · MM/AAAA

Feito com: script painel.py | contado sem o script, conferir
Pergunta do mês: [a do advogado, ou "nenhuma"]
Ações do painel anterior: [feita | não feita | em andamento, uma linha cada]
Versão HTML: [AAAA-MM.html, uso interno | não gerada]

## Cuidados antes de ler
## Números            (as seções 1 a 7 do script, sem mexer)
## Três leituras      (formato 4.1)
## Três ações         (tabela: ação | por quê | quem | até | habilidade)
## Perguntas em aberto (para quem vai cada uma)
```

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Painel do mês (números, leituras, ações) | `escritorio/07-operacao/comercial/painel/AAAA-MM.md` |
| Números em planilha | `escritorio/07-operacao/comercial/painel/AAAA-MM-numeros.csv` e, se pedido, `.xlsx` |
| Versão HTML, interna | `escritorio/07-operacao/comercial/painel/AAAA-MM.html` |
| Trimestre | `escritorio/07-operacao/comercial/painel/AAAA-MM-a-AAAA-MM.md` |
| Opções do nicho e regras de contagem aprovadas | `escritorio/04-base/comum/ficha-comercial.md` (com histórico) e `aprendizados-comercial.md` |
| Painel de treino | `escritorio/07-operacao/_treino/comercial/painel/` |

O painel não altera o `contatos.csv`. Problema de registro vira ação, feita pela pessoa ou pela habilidade que move aquela etapa. Sem pasta aberta: entregue o painel no chat, com o caminho onde ficaria.

## 8. Solo e equipe

**Solo:** o painel é a conversa do advogado com ele mesmo, uma vez por mês, 20 minutos. Com poucos contatos, prefira o trimestre. As três ações viram no máximo uma por semana.

**Equipe:** o painel abre a reunião mensal do comercial. Quem cuida do registro traz o painel; o advogado responde as perguntas; cada ação sai com um nome. Tempo ruim num canal só é pergunta de escala (quem olha aquele canal), e não de pessoa.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Decidir pelo celular cheio | Esforço onde há barulho e não fechamento | Entradas e fechamentos por origem, lado a lado |
| Contato que nunca recebeu resposta passa despercebido | Quem procurou fecha com outro | `primeira_resposta` vazia listada com as horas úteis |
| Percentual com 3 casos | "67% de conversão" que é 2 de 3 | "x de y" abaixo de 10 casos |
| Inventar a causa | Ação baseada em impressão | Causa sem dado vira pergunta |
| Treino misturado ao real | Número do escritório falso | O script recusa `_treino` sem `--treino` e marca TREINO |
| Painel com nome de cliente compartilhado por link | Dado de cliente exposto | Só códigos; HTML interno, link nunca compartilhado |
| Script que "não acha nada" porque não leu nada | Falsa tranquilidade | Arquivo que falta, vazio ou sem coluna obrigatória sai com erro |
| Registro sujo virar número | Origem duplicada, código repetido | Seção de qualidade e ação de correção |

## 10. Próximo passo

- Contato sem resposta ou canal atrasado: `rotina-comercial`, para entrar na leitura do dia, e `triar-contato` para responder agora.
- Propostas paradas ou contatos sem retorno: `follow-up` (se instalada), respeitando `pediu_para_parar`.
- Perda por preço: `objecoes-comerciais` (se instalada) e a política da `proposta-de-honorarios`.
- Dúvida sobre o que as conversas dizem: `auditar-conversas-comerciais` (se instalada).
- Origem ou motivo de perda novo: `/motor-comercial:ficha`.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e deixe a ação no painel para a pessoa fazer à mão.

## Referências desta habilidade

- `scripts/painel.py`: o cálculo, o csv resumido e a versão HTML. Rode nos passos 3 e 7. Biblioteca padrão do Python; `openpyxl` só para o `.xlsx` opcional.
- `references/regras-do-calculo.md`: como cada número é contado e como contar sem o script. Leia no passo 2, quando o registro tiver formato diferente, e no passo 3, quando não houver como rodar o script.
- `references/como-ler-o-painel.md`: o que cada seção quer dizer, os cuidados, o banco de perguntas e a saída completa do exemplo. Leia nos passos 4 a 6.
