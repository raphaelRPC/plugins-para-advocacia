---
name: calendario-forense
description: Monta e mantém o calendário forense de cada tribunal do escritório (feriados nacionais, estaduais e municipais que o tribunal segue, atos do tribunal, recesso, suspensões, expediente reduzido e indisponibilidades), cada linha com fonte e [CONFERIR] até a pessoa conferir no ato oficial. Copia a tabela de regras de contagem e conduz a validação com quem responde pela controladoria, monta a tabela de prazos por ato sem número de memória, registra a indisponibilidade certificada e traz o calendário e as regras de treino. Use quando disserem "monta o calendário do TRT3 de 2027", "o tribunal suspendeu os prazos", "saiu a certidão de indisponibilidade do PJe", "valida a tabela de regras", "põe a apelação na nossa tabela de prazos". Não use para contar um prazo (use calcular-prazo).
---

# Calendário forense

> O calendário de cada tribunal e a tabela de regras do escritório, conferidos na fonte, para a conta do prazo ter de onde partir.

Regras de contagem (a mais importante do plugin): `../../docs/contagem.md`. Registros e dupla conferência: `../../docs/prazos.md`. Regras gerais: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Fila: `../../docs/agentes-e-fila.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda-feira, 08h. O ciclo calculou o recurso de um cliente para quinta, mas quinta é feriado municipal e ninguém tinha posto no calendário do TJMG. A conta saiu um dia mais cedo, o que ainda é seguro; no ano anterior, sem calendário nenhum, o escritório contou um prazo pulando um feriado que o tribunal não seguia e quase perdeu o dia. O calendário é a régua de toda conta: o que não está nele, o script não vê.

**Regras fixas desta habilidade:**
1. Nenhuma data entra como conferida sem a fonte: o ato do tribunal (portaria, resolução, calendário oficial) ou a lei. A IA monta o rascunho; quem confere cada linha no ato e escreve `conferido_em` é a pessoa.
2. O número de dias de cada ato nunca vem da memória. A tabela de prazos por ato é preenchida pela pessoa, com a fonte que ela conferiu.
3. Indisponibilidade só vira `indisponibilidade-certificada` com a certidão do tribunal. Aviso de manutenção é `indisponibilidade-programada` e não empurra prazo.
4. Na dúvida se um dia tem expediente, o calendário fica sem o dia e a dúvida vai para a pessoa: um dia a menos no calendário deixa a conta mais cedo, nunca mais tarde.
5. Treino usa só `assets/calendario-de-treino.md` e `assets/regras-de-treino.md`, que nunca valem para prazo real.

## 1. Quando usar

**Use quando:**
- O escritório começa a usar o plugin e precisa do calendário do ano de cada tribunal da ficha (`tribunais`).
- Vira o ano, ou o tribunal publica portaria de feriado, ponto facultativo, suspensão de prazos ou expediente reduzido.
- O tribunal certifica uma indisponibilidade do sistema.
- A tabela de regras precisa ser copiada, validada ou revista (uma vez por ano, ou quando lei ou ato mudar).
- A pessoa quer acrescentar um ato à tabela de prazos por ato ("põe a réplica na tabela").
- O `/motor-controladoria:comecar` ou a `calcular-prazo` acusou "sem calendário para o tribunal X" ou "regra ainda não validada pelo escritório".
- A `adaptar-controladoria` (se instalada) chamou no modo "adaptar".

**Não use quando:**
- O pedido é contar um prazo: `calcular-prazo`.
- O pedido é conferir um prazo já contado: `dupla-conferencia`.
- O pedido é saber se cabe prazo em dobro num caso: é decisão da pessoa; a tabela só diz como o script dobra.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-da-controladoria.md` e `nicho.md`, se existir (o nicho diz em que comarcas e varas o escritório mais atua).
2. **Leia os aprendizados** (`aprendizados-controladoria.md`). Linha da `calendario-forense` vale mais que o padrão desta habilidade, nunca para afrouxar as regras fixas.
3. **Veja o que já existe** em `escritorio/04-base/controladoria/`: `regras-de-contagem.md` (validada? por quem e quando?) e `calendario/` (quais tribunais e anos, conferidos quando).
4. **Conta de IA:** calendário e regras não têm dado de cliente e podem ir para o Projeto no Claude.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `tribunais`, `cidades_dos_juizos` |
| Melhora | K: `calendario_conferido_em`, `regras_validadas_por` |

Sem `tribunais`, pergunte: "Em que tribunais os processos de vocês tramitam?". Sem `cidades_dos_juizos`: "Em que cidades ficam os juízos? Os feriados municipais mudam a conta." Ofereça gravar as respostas na ficha. Depois de conferir os calendários, ofereça gravar `calendario_conferido_em`; depois da validação da tabela, `regras_validadas_por` e `regras_validadas_em` com o que a pessoa disser.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Calendário do ano | Começo de uso ou virada do ano | Tribunal, ano, cidade | `calendario/<tribunal>-AAAA.md` em rascunho, depois conferido |
| Atualizar | Portaria nova, suspensão, expediente reduzido | O ato do tribunal | Linha nova no calendário, com fonte |
| Indisponibilidade | Certidão do tribunal | A certidão | Linha `indisponibilidade-certificada` e a lista de prazos a recontar |
| Validar regras | Antes do primeiro prazo real, e uma vez por ano | `contagem.md` | `regras-de-contagem.md` validada |
| Validar em bloco | A pessoa prefere conferir fora do chat, no texto oficial | A tabela de regras ou o calendário inteiro, com "onde conferir" | A pessoa responde só as linhas que mudam; quem e quando registrados |
| Prazos por ato | A pessoa quer acrescentar ou revisar atos | O ato e a fonte que a pessoa conferiu | Linha nova em "Prazos por ato" |
| No ciclo | O agente acha tribunal sem calendário ou ano descoberto | O aviso do script | `item: aviso` na fila; nada é criado sozinho |
| Treino | `comecar` ou "é teste" | `assets/` desta habilidade | Usa os arquivos de treino; não grava calendário real |
| Adaptar | A `adaptar-controladoria` chama | `nicho.md`, ficha | Lista de tribunais, cidades e atos do nicho, para a pessoa confirmar |

Pedido direto ("põe a suspensão do dia 12 no calendário do TRT3, é a portaria tal"): não faça entrevista. Monte a linha, mostre e grave com o ok.

### Passo 1. Qual tribunal, qual ano, qual cidade
Se não veio junto, pergunte: "Qual tribunal e qual ano vamos montar?". Depois, uma vez: "Em que cidade fica o juízo? Se o escritório tem processos desse tribunal em mais de uma cidade, fazemos um calendário por cidade." Calendário por cidade: `calendario/<tribunal>-<cidade>-AAAA.md`, com `cidade` no cabeçalho (o script pede `--cidade` quando há mais de um).

### Passo 2. O rascunho
Rode o script da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/calendario.py" rascunho --tribunal TJMG --ano 2027 \
  --cidade "Belo Horizonte" --saida escritorio/04-base/controladoria/calendario/tjmg-2027.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/calendario-forense`. O script nunca escreve por cima de um arquivo que já existe. Ele traz só o ponto de partida: feriados nacionais de data fixa, as datas móveis calculadas pela Páscoa (carnaval, quarta-feira de cinzas como expediente reduzido, sexta-feira santa, Corpus Christi), o recesso e, para TRF, a lista de feriados próprios da Justiça Federal. Toda linha sai com `[CONFERIR]` na fonte e `conferido_em` vazio. Sem o script: monte a mesma tabela à mão, no formato da seção 4.

### Passo 3. O que o script não sabe
Pergunte, uma de cada vez, e acrescente com a fonte que a pessoa der:
1. "Vocês têm o ato do tribunal com o calendário do ano (portaria, resolução)? Pode colar aqui ou dizer o número?"
2. "Qual é o feriado estadual, e o tribunal segue?"
3. "Quais são os feriados municipais da cidade do juízo, e o tribunal segue?"
4. "O tribunal adota algum ponto facultativo ou dia de expediente reduzido no ano?"
Sem o ato na conversa, a linha fica com `[CONFERIR]` na fonte e entra na lista do que conferir. Se o ambiente abre páginas, a pessoa pode pedir para ler o calendário publicado no portal do tribunal; mesmo assim quem confere a linha é ela.

### Passo 4. Conferir linha por linha
Rode a conferência de formato:

```
python3 "<pasta desta habilidade>/scripts/calendario.py" validar escritorio/04-base/controladoria/calendario/tjmg-2027.md --tribunal TJMG --ano 2027
```

Pergunte uma vez: "Prefere conferir linha por linha aqui, ou em bloco: eu mostro o calendário inteiro com onde conferir, você confere no ato do tribunal e me diz só as linhas que mudam?". Em bloco, siga a seção "Validar em bloco", logo abaixo.

Linha por linha: mostre as pendências e pergunte: "Esta data está no ato? Qual é a fonte?". A cada sim com a fonte, troque o `[CONFERIR]` pelo ato e preencha `conferido_em` com a data de hoje. Linha que a pessoa não confirma: fica marcada, e o script de conta faz as duas leituras (contando e não contando o dia), fica com a mais cedo e mostra a dúvida do calendário sempre que a linha mudar a conta. No fim, peça: "Quem conferiu este calendário?" e grave no cabeçalho só o nome que a pessoa disser, com `conferido_em`.

### Validar em bloco (calendário e tabela de regras)
Para quem não quer responder dezenas de perguntas no chat. Tempo realista, com o texto oficial aberto: **10 a 15 minutos por calendário** e **40 a 60 minutos para a tabela de regras** (19 regras e a seção de prazos por ato). Diga a estimativa antes de começar.
1. Mostre a tabela inteira de uma vez, com uma coluna a mais, "onde conferir": no calendário, a lei federal (Planalto) para os feriados nacionais e o ato do ano do tribunal para o resto; na tabela de regras, o artigo da coluna "Onde está" e, para os prazos por ato, a lei de cada rito.
2. No calendário, destaque em negrito as linhas que **precisam de ato do tribunal** (não saem da lei federal): Corpus Christi, carnaval, quarta-feira de cinzas, Semana Santa da Justiça Federal, feriados estaduais e municipais que o tribunal segue, pontos facultativos, suspensões, expediente reduzido e indisponibilidades. São elas que mais mudam de um ano para outro.
3. Pergunte: "Confira no texto oficial, fora daqui, e me diga só o que muda: por exemplo, 'todas conferem menos a 3 e a 7; a 7 é dia 05/06'. Qual é a fonte que você usou?".
4. Aplique só o que a pessoa disser: as linhas que ela confirmou ganham a fonte que ela deu e `conferido_em` de hoje; as que mudaram, o dado novo marcado `[ALTERADO]` na conversa; as que ela disser que não conferiu continuam `[CONFERIR]` (e o script de conta avisa e fica com a data mais cedo).
5. Pergunte: "Quem conferiu, e em que data?". Grave no cabeçalho (`conferido_por` e `conferido_em` no calendário; `validada_por` e `validada_em` na tabela de regras) só o que a pessoa disser, e uma linha no corpo: "Validação em bloco: [nome], AAAA-MM-DD; linhas alteradas: [lista ou nenhuma]; não conferidas: [lista ou nenhuma]".
6. "Todas conferem" sem a fonte não vale como conferência: pergunte a fonte. A IA nunca marca uma linha como conferida sem a pessoa dizer.

### Passo 5. Gravar
Mostre o calendário inteiro e pergunte: "Posso gravar?". Com o ok, grave em `escritorio/04-base/controladoria/calendario/` e rode `validar` de novo (código 0 é sem pendência; 2 é pendência que a conta vai avisar; 1 é erro que faz a conta recusar o arquivo). Ofereça gravar `calendario_conferido_em` na ficha.

### Passo 6. A tabela de regras (modo "Validar regras")
1. Sem `regras-de-contagem.md`: copie a tabela de `../../docs/contagem.md` com o cabeçalho da seção 5 (`validada_por: [A PREENCHER]`) e a seção `## Prazos por ato` vazia.
2. Pergunte uma vez: "Prefere conferir regra por regra aqui, ou em bloco, no texto oficial, me dizendo só o que muda? Em bloco leva de 40 a 60 minutos.". Em bloco: seção "Validar em bloco", acima. Regra por regra: para cada linha, mostre a chave, o que diz e onde está, e pergunte: "Você conferiu esta regra no texto oficial? Mudou alguma coisa para os ritos de vocês?". Ajuste só o que a pessoa disser, marcando `[ALTERADO]` na conversa.
3. Linha nova do escritório ganha chave nova, em minúsculas e com hífen (ex.: `nenhum-prazo-no-ultimo-dia`). O script de conta só aplica as chaves que ele conhece; chave nova aparece no relatório e vira regra da pessoa e da `adaptar-controladoria` (se instalada; sem ela, registre em `regras_proprias` da ficha).
4. No fim: "Quem validou a tabela, e em que data?". Grave `validada_por` e `validada_em` só com o que a pessoa disser. Enquanto isso não acontecer, todo prazo sai com o aviso "regra ainda não validada pelo escritório".

### Passo 7. Prazos por ato
Para cada ato que o escritório costuma cumprir, pergunte: "Quantos dias para [ato] no rito [rito], em dias úteis ou corridos, e onde você conferiu?". Em bloco: mostre a lista de atos do nicho com as colunas vazias e a lei de cada rito em "onde conferir", e a pessoa devolve a tabela preenchida de uma vez. Inclua os embargos de declaração em cada rito que o escritório usa: sem a linha, a triagem mostra os embargos de uma sentença como `[A CONFIRMAR: quantos dias]`. Grave a linha `ato | rito | dias | contagem | fonte` só com a resposta. Se a pessoa não souber: `[A CONFIRMAR: quantos dias]` na coluna `dias`, e o script recusa contar esse ato até alguém preencher. Nunca sugira o número.

### Passo 8. Indisponibilidade certificada (modo "Indisponibilidade")
1. Peça a certidão: "Pode colar a certidão ou dizer o número e a data dela?". Sem certidão, a linha é `indisponibilidade-programada` (ou não entra) e o prazo não muda.
2. Grave a linha `indisponibilidade-certificada`, com a certidão na fonte e `vale_para` com a sigla do tribunal.
3. Liste os prazos de `07-operacao/controladoria/prazos.csv` desse tribunal com `vencimento` no dia certificado e peça a conta de novo pela `calcular-prazo` ou pela `prazos-em-lote` (se instalada). A data nova só vale depois da dupla conferência; até lá, vale a antiga, que é a mais cedo.

### Passo 9. Aprender
Pergunte: "Teve algum dia sem expediente que pegou vocês de surpresa e que eu devia perguntar todo ano?". Cada resposta vira uma regra curta ("todo ano, perguntar pelo feriado da padroeira de Contagem") e, com o ok, entra em `aprendizados-controladoria.md` (`../../docs/aprender-com-o-uso.md`).

### Modo no ciclo
1. O agente não cria calendário. Quando o script de conta recusa por "sem calendário para o tribunal X" ou avisa que o calendário não cobre o ano, grave um `item: aviso` em `07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-calendario-<tribunal>.md`, no formato de `../../docs/agentes-e-fila.md`, com `revisor: pendente` e o que falta.
2. No resumo do dia, a linha: "Calendário de [tribunal] [ano] falta: os prazos desse tribunal ficaram sem conta (ou com aviso)".

### Modo treino
O calendário e as regras de treino estão em `assets/`. Use-os direto no script de conta (`calcular-prazo`). Para mostrar a validação, rode `validar` em `assets/calendario-de-treino.md`: o único aviso é o feriado de 2026-11-15, que cai no domingo. Nada é gravado em `04-base/`; anotações do treino vão para `escritorio/07-operacao/_treino/controladoria/`.

### Modo adaptar
1. Leia `nicho.md`, a ficha e os aprendizados.
2. Monte três listas: os tribunais e cidades que o nicho mais usa (por exemplo, juízos do interior com competência delegada); os atos que mais aparecem e ainda não estão em "Prazos por ato"; os dias sem expediente que o nicho costuma esquecer.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte qual entra. Atos entram sem número: a pessoa preenche pelo passo 7.

## 4. O formato do calendário

Cabeçalho YAML: `tribunal` (sigla, ou siglas separadas por vírgula), `ano`, `conferido_em`, `conferido_por`, `treino: sim|nao`. Opcionais: `cidade` (quando há um calendário por cidade) e `cobre_ate` (`AAAA-MM-DD`, quando o arquivo vai além do ano, como o de treino). Também `documento`, `versao` e `dono` (`../../docs/regras.md`, seção 7).

Uma tabela, com as colunas exatas `data | tipo | descricao | vale_para | fonte | conferido_em`:

| Coluna | O que vai |
|---|---|
| `data` | `AAAA-MM-DD` ou `AAAA-MM-DD a AAAA-MM-DD` |
| `tipo` | `feriado`, `recesso`, `suspensao`, `expediente-reduzido`, `indisponibilidade-programada`, `indisponibilidade-certificada` |
| `descricao` | O que é, em poucas palavras |
| `vale_para` | `todos` ou as siglas separadas por vírgula (`TRF6`, `TRT3`, `TJMG`) |
| `fonte` | O ato do tribunal ou a lei; `[CONFERIR]` enquanto não conferida |
| `conferido_em` | A data em que a pessoa conferiu a linha |

Como o script de conta lê cada tipo (`../../docs/contagem.md`):

| Tipo | Na publicação e na ciência | Na contagem | No vencimento |
|---|---|---|---|
| `feriado` | Dia sem expediente | Não conta | Empurra para o dia útil seguinte |
| `recesso` | Conta como dia com expediente | Não conta (suspenso); no penal, só com `--recesso-penal` | Não cai: o dia não é contado |
| `suspensao` | Conta como dia com expediente | Não conta | Não cai |
| `expediente-reduzido` | Conta | Conta no meio; no começo, o início vai para o dia útil seguinte | Empurra |
| `indisponibilidade-programada` | Conta | Conta | **Não empurra**: só avisa |
| `indisponibilidade-certificada` | Conta | Conta no meio do prazo | Empurra |

Fins de semana não entram na tabela. Recesso em que o tribunal também fecha (sem expediente) entra duas vezes: como `recesso` e como `feriado`, cada linha com a sua fonte. Linha com data `[A PREENCHER]` é ignorada pela conta, que avisa "calendário incompleto".

## 5. O formato da tabela de regras

Arquivo `escritorio/04-base/controladoria/regras-de-contagem.md`. Cabeçalho YAML com `validada_por`, `validada_em`, `treino: sim|nao` (e `documento`, `versao`, `dono`). Depois, a tabela de `../../docs/contagem.md` com a coluna `Chave` primeiro, e a seção:

```
## Prazos por ato

| ato | rito | dias | contagem | fonte |
|---|---|---|---|---|
| [ato] | civel, trabalhista, juizado-civel, juizado-federal, penal ou outro | [A CONFIRMAR: quantos dias] | uteis ou corridos | [onde a pessoa conferiu] |
```

O script lê as chaves pela primeira coluna, o prazo de ciência da linha `intimacao-portal` (o número antes de "dias corridos") e a seção "Prazos por ato" pelo nome do ato, sem diferenciar maiúscula e acento. Exemplo pronto: `assets/regras-de-treino.md` (os quatro atos de treino).

## 6. Formato da saída

```
CALENDÁRIO · [tribunal] · [ano] · [cidade]
Linhas: N · conferidas N · com [CONFERIR] N · a preencher N
Falta conferir: [data · descrição · o que pedir]
Gravado em: escritorio/04-base/controladoria/calendario/[arquivo] · conferido por: [nome que a pessoa disse] em [data]
Regras: validada por [nome] em [data] | ainda não validada
Prazos por ato: N linhas · sem número N
```

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Calendário de cada tribunal e ano | `escritorio/04-base/controladoria/calendario/<tribunal>-AAAA.md` (ou `<tribunal>-<cidade>-AAAA.md`) |
| Tabela de regras e prazos por ato | `escritorio/04-base/controladoria/regras-de-contagem.md` |
| Aviso de calendário que falta (ciclo) | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-calendario-<tribunal>.md` |
| Data da conferência e quem validou | `escritorio/04-base/comum/ficha-da-controladoria.md` (`calendario_conferido_em`, `regras_validadas_por`, `regras_validadas_em`) |
| Treino | `assets/` desta habilidade; anotações em `escritorio/07-operacao/_treino/controladoria/` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: o calendário e a tabela saem em blocos para colar nas instruções do Projeto, com o caminho onde ficariam. No chat sem código, a conta é feita à mão com esse calendário na conversa.

## 8. Solo e equipe

**Solo:** monte o calendário de cada tribunal uma vez por ano, no começo de janeiro, e reserve dez minutos por mês para as portarias novas. A validação da tabela é sua; anote no aprendizado o que você mudou e por quê.

**Equipe:** a estagiária monta o rascunho e junta os atos; a advogada responsável pela controladoria confere cada linha e assina a validação. Quem confere o calendário não precisa ser quem confere os prazos, mas o nome vai no cabeçalho. Portaria nova que chega por e-mail vai para a `entrada/` e vira linha no mesmo dia.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Feriado municipal fora do calendário | Prazo contado um dia antes (seguro) ou, sem calendário, sem nenhum feriado | Passo 3 pergunta cidade e feriados; o script de conta recusa tribunal sem calendário |
| Feriado de outra cidade aplicado ao juízo | Prazo contado um dia depois: risco de perder | Um calendário por cidade e `--cidade` obrigatório quando há mais de um |
| Manutenção anunciada tratada como indisponibilidade | Prazo empurrado sem certidão: risco de perder | Só a certidão vira `indisponibilidade-certificada` |
| Número de dias de memória na tabela | Prazo errado com aparência de regra | Passo 7: só a pessoa preenche, com a fonte |
| Tabela nunca validada | Toda conta com regra que ninguém conferiu | Aviso em todo prazo até `validada_por` e `validada_em` |
| Calendário do ano novo esquecido | Prazos de janeiro contados sem feriado | O script avisa quando a conta sai do período do calendário |
| Treino misturado com o real | Feriado inventado num prazo real | `treino: sim` no cabeçalho e aviso em toda conta de treino |

## 10. Próximo passo

- Calendário e regras prontos: contar o primeiro prazo com a `calcular-prazo`.
- Indisponibilidade certificada: recontar os prazos do dia pela `calcular-prazo` ou pela `prazos-em-lote` (se instalada; sem ela, um por um na `calcular-prazo`), e a `dupla-conferencia` em cada um.
- Regra própria do escritório que o script não conhece: `adaptar-controladoria` (se instalada; sem ela, registre em `regras_proprias` da ficha).

## Referências desta habilidade

- `scripts/calendario.py`: `rascunho` monta o ponto de partida do ano (passo 2); `validar` confere formato e pendências (passos 4 e 5).
- `assets/calendario-de-treino.md`: o calendário de treino de `../../docs/casos-ficticios.md` (TRF6, TRT3, TJMG; 2026 e começo de 2027), com o feriado inventado de 2026-04-16. Só treino.
- `assets/regras-de-treino.md`: a tabela de `contagem.md` e os quatro atos de treino. Só treino.
- O script de conta que lê estes arquivos: `../calcular-prazo/scripts/calcular_prazo.py` (habilidade `calcular-prazo`).
