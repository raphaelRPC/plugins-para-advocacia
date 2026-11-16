---
name: triar-publicacoes
description: Tria cada publicação captada. Sugere o tipo do ato e a triagem (prazo, audiência, perícia, ciência, urgente, sem caso, sem providência), liga o processo ao caso pela carteira de processos e pelos registros dos plugins irmãos, só pelo número, e mostra o trecho literal do ato que justifica cada sugestão. Separa o prazo da outra parte (que vira ciência), o processo que não está na carteira (sem caso, para a pessoa) e o que é para uma pessoa agora. Um script acha no teor os números de dias, as datas e as expressões de prazo ("no prazo de", "em X dias", "intime-se", "designo audiência") e monta os dados para a conta. Use quando a pessoa disser "tria as publicações de hoje", "isso aqui pede prazo?", "de quem é esse processo?", "o que essa intimação manda fazer?". Não use para contar a data do prazo (use calcular-prazo) nem para decidir a providência (use providencia-sugerida).
---

# Triar as publicações

> Cada ato com o caso certo, o trecho literal à vista e uma sugestão do que ele pede, para uma pessoa confirmar.

Regras: `../../docs/regras.md`. As triagens e as colunas de `publicacoes.csv`: `../../docs/prazos.md`. A contagem e os prazos por ato: `../../docs/contagem.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino e gabarito: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 9h. Dez publicações captadas. Uma diz "Intime-se o INSS para, em 5 dias, manifestar-se sobre o laudo": tem número de dias, mas o prazo é do INSS. Outra é de uma "Rosângela" que ninguém conhece, com a OAB do escritório. A triagem põe a primeira como ciência, sem linha de prazo, e a segunda como sem caso, para a advogada dizer se é caso antigo, substabelecimento ou erro. Ninguém adivinha.

**Regras fixas desta habilidade:**
1. A IA capta o prazo, mas não interpreta. Toda triagem é sugestão, com o trecho literal do ato que a justifica, copiado sem mudar uma vírgula. Sem trecho, não há sugestão.
2. Caso só pelo número do processo: na carteira de processos ou, igual, nos registros dos irmãos. Nunca por nome parecido, área ou palpite. Não achou: `sem-caso`, para a pessoa, e nenhum prazo calculado.
3. Prazo da outra parte não vira prazo do escritório. "Intime-se o INSS", "intime-se o réu": ciência, sem linha em `prazos.csv`.
4. O número de dias vem do próprio ato ou da tabela de prazos por ato do escritório. Nunca da memória. Sem os dois: `[A CONFIRMAR: quantos dias]`. Ato que pede algo à parte do cliente sem dizer os dias ("diga a parte autora", "no prazo legal", "manifeste-se", "especifique provas", "intime-se a parte autora") é `prazo` com essa marca: na dúvida entre `sem-providencia` ou `ciencia` e `prazo`, sugira `prazo`, com a dúvida para a pessoa.
5. Urgência, sem caso, captação atrasada, data de disponibilização em dúvida e ciência tácita perto vão para PESSOA AGORA antes de qualquer outra coisa.

## 1. Quando usar

**Use quando:**
- Há publicações `nao-triada` no registro depois da captação (modo "a pedido").
- O `agente-de-controladoria` roda o ciclo (modo "no ciclo").
- A pessoa cola um ato e pergunta o que ele pede (modo "um ato").
- O `/motor-controladoria:comecar` ou a pessoa quer treinar com o lote (modo "treino").
- A `adaptar-controladoria` (se instalada) pede as expressões e os atos típicos do nicho (modo "adaptar").

**Não use quando:**
- O pedido é a data do prazo: `calcular-prazo`, com os dados que esta triagem monta.
- O pedido é o que fazer com o ato (peça, documento, aviso): `providencia-sugerida` (se instalada; sem ela, a pessoa decide na fila e a `encaminhar-providencia` registra).
- São centenas de atos parecidos no mesmo dia: `triagem-em-massa` (se instalada) agrupa antes, e esta habilidade tria as exceções.
- É sentença ou acórdão que precisa ser lido por inteiro: `leitura-da-decisao` (se instalada; sem ela, a triagem sugere o prazo e a advogada lê a decisão).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-controladoria.md`), em especial os da `triar-publicacoes` (expressões que o juízo usa, atos que o escritório sempre trata como urgentes).
3. **Leia a carteira de processos** (`escritorio/07-operacao/controladoria/processos.csv`, feita pela `carteira-de-processos`). Sem ela, avise: "Sem a carteira de processos, toda publicação sai sem caso, a não ser que o número esteja nos registros dos outros plugins." e ofereça montá-la (`carteira-de-processos`, se instalada; sem ela, a pessoa diz o código de cada processo na conversa e a triagem registra).
4. **Leia a tabela de regras do escritório** (`escritorio/04-base/controladoria/regras-de-contagem.md`), seção "Prazos por ato". Sem ela, sentenças saem com `[A CONFIRMAR: quantos dias]`.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `tribunais` |
| Melhora | E: `areas` · K: `responsaveis_por_area`, `carteira_de_processos` |

`tribunais` diz quais siglas esperar e qual rito sugerir (JEF, Vara do Trabalho, vara cível). Publicação de tribunal fora da lista: aviso, para conferir. `areas` ajuda a reconhecer o ato típico do nicho. `responsaveis_por_area` diz quem recebe cada triagem. `carteira_de_processos` diz de onde vem a carteira; vazio, pergunte uma vez: "Onde fica a lista dos processos ativos de vocês: sistema jurídico ou planilha?".

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | Publicações `nao-triada` | `publicacoes.csv`, teor, carteira, tabela de regras | Triagem sugerida no chat; com o ok, o registro e o arquivo do dia |
| Um ato | A pessoa cola um ato | O texto e o número do processo | A sugestão no chat. Grava só se a pessoa pedir |
| No ciclo | O agente chama | O mesmo do "a pedido" | Registro e arquivo do dia gravados, lista para a fila. Não mostra nada |
| Treino | Comecar ou pedido de treino | O lote de treino já captado e `assets/processos-de-treino.csv` | A triagem das dez, em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | Ficha, nicho, atos reais anonimizados | Expressões e atos típicos do escritório, para aprovar |

### Passo 1. Rodar o apoio da triagem

```
python3 "<pasta desta habilidade>/scripts/apoio_triagem.py" \
  escritorio/07-operacao/controladoria/publicacoes.csv \
  --processos escritorio/07-operacao/controladoria/processos.csv \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md \
  --escritorio escritorio --hoje AAAA-MM-DD --ultima-rodada AAAA-MM-DD
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/triar-publicacoes`. O script lê as linhas `nao-triada` (ou `--ids PUB-...`), acha no teor os números de dias e de horas, as datas, os horários e as expressões de prazo, diz a quem a ordem se dirige e liga ao caso pelo número. Sem `--gravar`, só mostra. Sem a carteira, ele avisa e segue; sem o publicacoes.csv ou com coluna faltando, sai com código 1.

### Passo 2. Ler cada sugestão contra o teor
O script acha; quem lê é você. Para cada publicação, abra o teor guardado e confira:
1. **O trecho literal** está no teor e diz o que a sugestão diz? Se o trecho é ambíguo, mostre os dois trechos e diga a dúvida.
2. **A quem se dirige a ordem:** a parte do cliente, a outra parte, as partes. O script olha as partes ("Marta L. P. x INSS") para saber de que lado está o cliente; pelas iniciais, ele avisa `[CONFERIR]`. Não deu para saber: fica `prazo`, com `[A CONFIRMAR]`, para a pessoa.
3. **O número de dias:** do ato ("no prazo de 5 dias", "em 15 (quinze) dias") ou da tabela ("recurso inominado · juizado-federal"). Dois números no mesmo ato: os dois, para a pessoa dizer qual vale. "No prazo legal" ou nenhum número: `[A CONFIRMAR: quantos dias]`, nunca da memória.
4. **A data e a hora** de audiência e perícia, como estão no ato.
5. **O que não é deste ato:** a sentença vista por outra fonte (duplicada) já saiu na captação e não volta aqui.

### Passo 3. A triagem de cada uma

| Triagem | Quando sugerir | O que acontece depois |
|---|---|---|
| `prazo` | O ato dá prazo ao escritório (dias no ato), pede algo à parte do cliente sem dizer os dias (`[A CONFIRMAR: quantos dias]`) ou é sentença ou decisão de que pode caber recurso (dias da tabela) | `calcular-prazo`, com os dados da seção "Para a conta"; sem os dias, a linha entra `sugerido` sem vencimento, para a pessoa |
| `audiencia` | Designa, redesigna ou pauta audiência ou sessão | Data e hora em `prazos.csv` como `tipo = audiencia` (pela `calcular-prazo` ou `audiencias-e-pericias`, se instalada). Pauta sozinha não é prazo |
| `pericia` | Designa perícia | O mesmo, com `tipo = pericia` |
| `prazo` e também `pericia` ou `audiencia` | O ato marca a pauta e dá prazo à parte do cliente, ou sem destinatário claro ("intime-se a parte autora para, em 10 dias, apresentar quesitos; perícia designada para 03/12/2026") | Duas sugestões: a triagem fica `prazo` (a conta dos quesitos) e a linha "Também neste ato" leva a perícia, que entra em `prazos.csv` como `tipo = pericia`. Nenhuma das duas some |
| `ciencia` | Prazo da outra parte; RPV, precatório ou alvará; trânsito em julgado; "ciência às partes" sem dias e sem pedido | Nenhuma linha em `prazos.csv`. Ciência registrada. Se o ato pede algo à parte do cliente, não é ciência: é `prazo` |
| `urgente` | Prazo em horas, liminar, bloqueio, prisão, ordem imediata | PESSOA AGORA, antes de qualquer outra coisa |
| `sem-caso` | O número não está na carteira nem nos registros dos irmãos | PESSOA AGORA: "é caso antigo, substabelecimento ou erro?". Nenhum prazo |
| `sem-providencia` | O script não achou pedido nem número de dias | Uma pessoa lê o ato antes de fechar. Na dúvida, `prazo` |

Sentença: o script não escolhe recurso. Ele lista todos os atos da tabela do escritório para o rito (inclusive os embargos de declaração, que aparecem como `[A CONFIRMAR: quantos dias]` quando a tabela não traz a linha do rito), cada um com o seu prazo e a sua conta, e o que cabe e se vale recorrer é da pessoa. Sentença de improcedência: além do prazo, o aviso "notícia ruim por ligação" (status-para-o-cliente, do motor-experiencia, se instalado; sem ele, a advogada liga). Prazo para juntar documento do cliente: o aviso para pedir o documento já (checklist-de-documentos, do motor-experiencia, se instalado). RPV: ciência e acompanhamento (`acompanhar-valores`, se instalada).

### Passo 4. O que vai para o topo
Antes da tabela, diga em uma linha cada item de PESSOA AGORA: urgente; sem caso; captada com atraso; data de disponibilização tirada do e-mail ou ausente (a captação avisa, e sem data a publicação fica `urgente`); intimação de painel com ciência tácita prevista em até 2 dias úteis; audiência ou perícia em até 3 dias; prazo de hoje ou amanhã que já estiver no registro.

### Passo 5. Mostrar e gravar
Mostre a saída (seção 5) e pergunte: "Confere as sugestões? Posso gravar a triagem no registro?". Com o ok, rode o passo 1 com `--gravar`: o script muda no `publicacoes.csv` só as linhas `nao-triada` ou já triadas pela IA (linha que uma pessoa confirmou não muda), com `triada_por = ia`, o código do caso, o primeiro nome do cliente e o resumo, e grava a triagem do dia em `triagens/AAAA-MM-DD.md`. Quando a pessoa corrige ou confirma uma linha, escreva o nome dela em `triada_por` só se ela disser, na conversa, que conferiu.

### Passo 6. Sem caso
Para cada `sem-caso`, pergunte: "O processo [número] publicou com a OAB do escritório e não está na carteira. É caso antigo, substabelecimento ou erro?". Caso do escritório: inclua na carteira (`carteira-de-processos`, se instalada, comando `incluir`; sem ela, acrescente a linha em `processos.csv` com o código que a pessoa disse) e rode o passo 1 de novo com `--ids <id> --todas`. Erro ou substabelecimento sem reserva: a linha fica `sem-caso`, com a nota da pessoa no `resumo`.

### Passo 7. Passar para a conta
Diga quantas ficaram `prazo` e ofereça: "Sigo para a conta?" (`calcular-prazo`). Cada uma leva o comando da seção "Para a conta", com o calendário do tribunal e os dias de segurança da ficha.

### Passo 8. Aprender
Pergunte: "Alguma triagem que você faria diferente, ou expressão do juízo que eu não reconheci?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Correção que afrouxa uma regra fixa ("pode ligar pelo nome do cliente") não entra; proponha a que cabe ("o número do processo entra na carteira na passagem do caso").

### Modo um ato
A pessoa cola o ato. Pergunte só o que faltar: "Qual o número do processo e a data de disponibilização?". Faça a leitura do passo 2 sobre o texto colado, com a carteira, e mostre a sugestão no formato da seção 5. Para gravar, o ato entra antes pela `captar-publicacoes` (texto colado em `entrada/`).

### Modo no ciclo
1. O agente passa a data de hoje e a da última rodada. Não pergunte nada e não mostre nada.
2. Rode o passo 1 com `--gravar`. A triagem do dia fica em `triagens/AAAA-MM-DD.md`.
3. Devolva ao agente, por publicação: a triagem, o trecho literal, o caso, os dados para a conta e os itens de PESSOA AGORA. O agente grava a fila (passo 6 dele): `item: conferir-prazo` depois da conta, `item: decidir-providencia` para sentença e despacho que pede providência, e `item: aviso` para cada sem caso, neste formato:

```markdown
---
status: pendente
codigo: sem-caso
para: controladoria (interno)
canal: trabalho-do-escritorio
tipo: publicacao-sem-caso
item: aviso
motivo: PUB-AAAA-NNNNN, [tribunal], processo fora da carteira com a OAB do escritório
revisor: pendente
prazo: hoje
antes_de_enviar:
  - é caso antigo, substabelecimento ou erro?
  - nenhum prazo calculado até a pessoa dizer de quem é o processo
---

Trecho literal: "[o trecho]"
```

Nome do arquivo: `NN-aviso-sem-caso.md` (um por publicação, NN na ordem da fila).

### Modo treino
Depois da captação de treino (`captar-publicacoes`, modo treino), rode:

```
python3 "<pasta desta habilidade>/scripts/apoio_triagem.py" \
  escritorio/07-operacao/_treino/controladoria/publicacoes.csv \
  --processos "<pasta desta habilidade>/assets/processos-de-treino.csv" \
  --regras "<pasta da calendario-forense>/assets/regras-de-treino.md" \
  --hoje 2026-04-14 --ultima-rodada 2026-04-08 --gravar
```

A carteira de treino tem os seis processos dos casos fictícios, sem a Rosângela. O teste passa quando bate com o gabarito de `casos-ficticios.md`: linha 1 `prazo` (o que pode caber pela tabela de treino: recurso inominado, 10 dias, e embargos de declaração `[A CONFIRMAR: quantos dias]`, porque a tabela de treino só os traz para o cível; a escolha é da pessoa; aviso de notícia ruim); linha 2 `audiencia` em 2026-05-20, 14h, por videoconferência, sem prazo; linha 3 `prazo` (recurso ordinário, 8 dias, e os embargos `[A CONFIRMAR]`) e "captada com atraso" no topo; linha 4 `prazo` (5 dias, o próprio ato); linha 5 `ciencia` (prazo do INSS, nenhuma linha de prazo); linha 6 `duplicada`; linha 7 `sem-caso`, no topo, sem prazo; linha 8 `prazo` (15 dias, o próprio ato, aviso de documento do cliente); linha 9 `ciencia` (RPV); linha 10 `prazo` (5 dias, ciência tácita prevista em 2026-04-16, no topo). Toda sugestão com o trecho literal. A conta de cada uma, na `calcular-prazo`, dá as datas do gabarito.

### Modo adaptar
1. Leia a ficha, `nicho.md` e atos reais anonimizados que o escritório trouxer.
2. Proponha: as expressões que os juízos de vocês usam ("fica a parte intimada", "ato ordinatório"), os atos que o escritório sempre trata como urgentes, os que nunca pedem nada.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Faltou alguma expressão que vocês veem toda semana?".
4. Com o ok, grave em `escritorio/04-base/controladoria/nicho/triar-publicacoes.md`. O script não muda: a habilidade lê esse arquivo no passo 2.

## 4. O que o script acha e o que ele não decide

| Acha no teor | Não decide |
|---|---|
| Números de dias e de horas, por algarismo e por extenso ("15 (quinze) dias") | Se o prazo existe: a pessoa confirma o que o ato pede |
| Datas (20/05/2026, 2026-05-20, "10 de junho de 2026") e horários | Qual recurso cabe e se vale recorrer |
| "Intime-se", "manifeste-se", "vista", "no prazo de", "sob pena de" | Prazo em dobro, ciência tácita, prazo material |
| "Designo audiência", "perícia designada", "julgo improcedente", "expeça-se RPV" | A providência |
| A quem a ordem se dirige e de que lado está o cliente | De quem é o processo que não está na carteira |

O resumo que vai para o registro é montado por categoria ("Juntar documento em 15 dias", "Prazo da outra parte (INSS): ciência") e nunca copia o teor: nada de saúde, criança ou renda no resumo.

## 5. Formato da saída

```
TRIAGEM SUGERIDA · AAAA-MM-DD · N publicações · prazo N · audiencia N · ciencia N · sem-caso N
PESSOA AGORA
  [id · caso · por quê, em uma frase]
[id · fonte · disponibilizada · tribunal · órgão]
  Caso: [código · primeiro nome · área (como ligou)] | SEM CASO
  Triagem sugerida: [triagem] · tipo do ato · rito sugerido
  Trecho literal: "[o trecho, exatamente como está no ato]"
  O que o ato parece pedir: [ação]
  Também neste ato (pericia | audiencia): [data, hora, local] · entra em prazos.csv como tipo próprio
  Dias: [N (o próprio ato | tabela do escritório: ato · rito)] | [A CONFIRMAR: quantos dias]
  Avisos: [outra parte, documento do cliente, notícia ruim, lado pelas iniciais]
  Para a conta (calcular-prazo): [--disponibilizacao | --envio-portal | --ciencia ...]
É sugestão: a pessoa confirma o que o ato pede, os dias e a regra.
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A triagem no registro | `escritorio/07-operacao/controladoria/publicacoes.csv` (`triagem`, `triada_por`, `codigo_caso`, `cliente_curto`, `resumo`, `atualizado_em`) |
| A triagem do dia, com os trechos | `escritorio/07-operacao/controladoria/triagens/AAAA-MM-DD.md` |
| Expressões do escritório (modo adaptar) | `escritorio/04-base/controladoria/nicho/triar-publicacoes.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

`prazos.csv` não muda aqui: a linha do prazo nasce na `calcular-prazo`. Linha confirmada por uma pessoa (`triada_por` com nome) nunca é sobrescrita pelo script. Sem pasta aberta: a triagem sai no chat, numa tabela para colar na planilha, com o trecho de cada uma.

## 7. Solo e equipe

**Solo:** tríe logo depois da captação, e leia os sem caso no mesmo dia. O processo esquecido de um caso antigo é o que mais pega quem trabalha sozinho.

**Equipe:** a estagiária tria e marca o que conferiu; a advogada responsável (`responsaveis_por_area`) olha os `prazo`, os `urgente` e os `sem-caso` antes da conta. Toda `ciencia` e `sem-providencia` passa pelo olho de uma pessoa no dia, com o trecho à vista: a amostra semanal serve para achar erro de padrão, nunca é o único olho sobre um ato que pede algo.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Prazo do INSS lançado como do escritório | Peça feita sem precisar, agenda poluída | Regra fixa 3: vira ciência |
| Processo desconhecido ligado ao cliente de nome parecido | Prazo no caso errado, sigilo quebrado | Regra fixa 2: só pelo número; senão, sem caso |
| Número de dias completado de cabeça | Prazo errado que parece certo | Regra fixa 4: do ato ou da tabela |
| Sugestão sem o trecho | A pessoa confere a IA, não o ato | Trecho literal em toda sugestão |
| Pauta tratada como prazo | Prazo inventado | `audiencia`, com a data do ato, sem dias |
| Quesitos em 10 dias perdidos atrás da data da perícia | Prazo do escritório sem linha | Duas sugestões: `prazo` e a perícia em "Também neste ato" |
| "Diga a parte autora, no prazo legal" como sem providência | Manifestação perdida | Regra fixa 4: `prazo` com `[A CONFIRMAR: quantos dias]` |
| Só o recurso entra e os embargos somem | A pessoa não vê que cabia embargar | Todos os atos da tabela para o rito, embargos sempre na lista |
| Resumo com laudo, doença ou criança | Dado sensível espalhado | Resumo por categoria, sem copiar o teor |
| Sentença ruim avisada por mensagem | Cliente sabendo pelo celular | Aviso de notícia ruim por ligação |

## 9. Próximo passo

- As de `prazo`: `calcular-prazo`, com o comando da seção "Para a conta".
- Audiência e perícia: `audiencias-e-pericias` (se instalada; sem ela, a `calcular-prazo` registra a data como `tipo` próprio).
- Sentença e acórdão: `leitura-da-decisao` (se instalada) e a decisão da providência na fila.
- Os sem caso: `carteira-de-processos` (se instalada), comando `incluir`, depois que a pessoa disser de quem é.

## Referências desta habilidade

- `scripts/apoio_triagem.py`: acha dias, horas, datas e expressões de prazo no teor, diz a quem a ordem se dirige, liga ao caso pela carteira (e pelo número exato nos registros dos irmãos) e sugere a triagem com o trecho literal. Rode no passo 1, no ciclo e no treino.
- `assets/processos-de-treino.csv`: a carteira de processos de treino, com os seis casos fictícios (sem a Rosângela). Use no modo treino.
