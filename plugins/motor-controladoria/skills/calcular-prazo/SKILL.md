---
name: calcular-prazo
description: Faz a conta do prazo processual pelo calendário do tribunal, com cada passo à vista (disponibilização, publicação, início, cada dia contado e cada dia pulado com o motivo, vencimento e data de segurança), por um script com duas contas independentes. O número de dias vem do próprio ato ou da tabela de prazos por ato do escritório, nunca da memória. Aplica a ciência tácita do portal com as duas leituras, ignora indisponibilidade sem certidão, só dobra quando a pessoa decide, recusa prazo de direito material e grava a linha sugerido em prazos.csv. Use quando disserem "conta esse prazo", "quando vence o recurso do Otávio?", "o prazo de 5 dias das custas cai quando?", "calcula a ciência tácita dessa intimação do PJe", "esse prazo pega o recesso?". Não use para conferir um prazo já contado (use dupla-conferencia).
---

# Calcular prazo

> A conta do prazo com cada passo à vista, pelo calendário do tribunal, para uma pessoa conferir antes de valer.

Regras de contagem (a mais importante do plugin): `../../docs/contagem.md`. Registros, status e dupla conferência: `../../docs/prazos.md`. Regras gerais: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 9h40. A sentença do Otávio saiu no DJEN ontem. A estagiária conta dez dias no calendário de parede e chega a 2026-04-28. A conta do script chega a 2026-04-30 e mostra por quê: quinta é feriado municipal e a outra terça é Tiradentes. Quem estava certo não importa agora; importa que as duas contas ficaram à vista, e a advogada confere as duas antes de o prazo entrar na agenda.

**Regras fixas desta habilidade:**
1. A IA capta e calcula, mas não interpreta. O que o ato pede, o número de dias e a regra são confirmados por uma pessoa na `dupla-conferencia`. Toda linha que esta habilidade grava é `sugerido`.
2. O número de dias vem do próprio ato ("no prazo de 5 dias") ou da tabela de prazos por ato do escritório. Sem um dos dois: `[A CONFIRMAR: quantos dias]`, e a conta não sai.
3. Na dúvida entre duas datas, vale a mais cedo, e a dúvida vai para a pessoa. Indisponibilidade só empurra o vencimento quando certificada.
4. Prazo em dobro, ciência tácita e prazo de direito material são da pessoa. O script só dobra com `--dobro`, mostra as duas leituras da ciência e recusa prazo material.
5. Prazo com segurança ou fatal hoje ou amanhã vai para PESSOA AGORA antes de qualquer outra coisa, em qualquer modo.

## 1. Quando usar

**Use quando:**
- A `triar-publicacoes` (se instalada) marcou uma publicação como `prazo`, ou a pessoa colou um ato que pede alguma coisa num prazo.
- O `agente-de-controladoria` chamou no ciclo (modo "no ciclo"), ou o revisor refaz a conta de um item.
- A pessoa quer saber quando vence um prazo informado à mão (ciência no painel, Domicílio Judicial Eletrônico).
- O `/motor-controladoria:comecar` pediu as contas do lote de treino, ou alguém quer treinar com os exercícios E1 a E3.
- A `adaptar-controladoria` (se instalada) chamou no modo "adaptar".

**Não use quando:**
- O prazo já foi contado e precisa de conferência: `dupla-conferencia`.
- São dezenas de prazos de uma vez: `prazos-em-lote` (se instalada; sem ela, um por um aqui).
- É audiência, perícia ou sessão: a data é a do ato, sem conta (`audiencias-e-pericias`, se instalada; sem ela, grave a linha com `tipo` próprio, como em `prazos.md`).
- É prazo de decadência, prescrição ou de contrato: o script recusa, e a pessoa informa a data.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-da-controladoria.md` e `nicho.md`, se existir (o nicho diz quais atos aparecem mais e em que ritos).
2. **Leia os aprendizados** (`aprendizados-controladoria.md`). Nenhum aprendizado muda o número de dias de um ato nem afrouxa as regras fixas.
3. **Ache a base:** `escritorio/04-base/controladoria/regras-de-contagem.md` e `calendario/`. Sem calendário do tribunal, a conta recusa; ofereça a `calendario-forense`. Sem tabela validada, a conta sai com o aviso "regra ainda não validada pelo escritório".
4. **Ache o ato:** a linha de `publicacoes.csv` e o teor em `publicacoes/AAAA-MM-DD/<id>.md`, ou o texto colado. Número de processo não vai para o Projeto nem para a resposta além do necessário.
5. **Conta de IA:** prazo de cliente só em conta profissional ou de equipe. Em conta pessoal, só o treino.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `dias_de_seguranca`, `tribunais` |
| Melhora | K: `prazo_em_dobro`, `regras_proprias` |

Sem `dias_de_seguranca`, o script usa 2 dias úteis (o padrão do modelo da ficha) e avisa; pergunte uma vez: "Quantos dias úteis antes do fatal vocês querem o prazo na agenda? Se não tiver um número, fica 2." e ofereça gravar. `tribunais` diz qual calendário usar. `prazo_em_dobro` diz se o escritório atua com Fazenda, Defensoria ou litisconsortes em autos físicos: quando diz "não", a pergunta do dobro só aparece se o ato for da outra parte. `regras_proprias` pode adiantar a data de segurança ("nenhum prazo no último dia"), nunca a fatal.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | A pessoa pede a conta | O ato, ou os dados | A conta no chat; a linha `sugerido` com o ok |
| No ciclo | O agente chama | A publicação triada como `prazo` | Linha `sugerido` e `item: conferir-prazo` na fila. Não pergunta nada |
| Treino | `comecar`, "é teste", exercícios | `../../docs/casos-ficticios.md` e os arquivos de treino | As contas do gabarito; grava em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | `nicho.md` e a ficha | Atos e ritos do nicho que faltam na tabela, para a `calendario-forense` |

Pedido direto ("conta 15 dias úteis da disponibilização de ontem no JEF"): não faça entrevista. Rode e pergunte só o que faltar.

### Passo 1. O ato e o trecho literal
Mostre o trecho do ato que pede alguma coisa, entre aspas, como veio da fonte. Se não há trecho (o ato não pede nada, ou o prazo é da outra parte, como "intime-se o INSS para..."), pare: não há prazo do escritório, e a triagem é `ciencia`. Diga em uma frase de quem é o prazo.

### Passo 2. O que a conta precisa
Monte a lista e pergunte só o que faltar, um item por vez:

| Dado | De onde vem | Sem ele |
|---|---|---|
| Ponto de partida | DJEN ou diário: data de disponibilização. Portal: data de envio. Painel aberto ou Domicílio Judicial Eletrônico: data da ciência que a pessoa viu | "Qual é a data de disponibilização (ou de envio, ou da ciência)?" |
| Número de dias | O próprio ato ou a tabela de prazos por ato do escritório | `[A CONFIRMAR: quantos dias]`, para a pessoa. Nunca da memória |
| Rito | O órgão e o tipo de processo (`civel`, `trabalhista`, `juizado-civel`, `juizado-federal`, `penal`, `outro`) | "É juizado, vara cível, trabalho ou penal?" |
| Tribunal e cidade | A publicação e a ficha | "De que tribunal e de que cidade é o juízo?" |
| Dobro | Só a pessoa | Sem dobro. Se o ato envolve Fazenda, Defensoria, MP ou litisconsortes: "Este prazo é em dobro? Quem decide é você." |
| Dias de segurança | `dias_de_seguranca` da ficha | 2, com aviso |

### Passo 3. Rodar a conta
Rode o script da pasta desta habilidade, com o calendário e a tabela do escritório:

```
python3 "<pasta desta habilidade>/scripts/calcular_prazo.py" \
  --disponibilizacao 2026-04-13 --ato "recurso inominado" \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md \
  --rito juizado-federal --tribunal TRF6 \
  --calendario escritorio/04-base/controladoria/calendario/ --seguranca 2 --duplo
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/calcular-prazo`. Com o número de dias do próprio ato, troque `--ato` por `--dias 5`. Intimação do portal: `--envio-portal AAAA-MM-DD`. Ciência vista no painel: `--ciencia AAAA-MM-DD` (e `--domicilio` se veio do Domicílio Judicial Eletrônico). Todas as opções estão na seção 5.

Sem o script (chat sem código): faça a mesma conta à mão, dia por dia, com o calendário na conversa, escrevendo cada dia contado e cada dia pulado com o motivo, e diga que foi à mão. A dupla conferência vale do mesmo jeito.

### Passo 4. Mostrar a conta
Mostre a saída do script como veio (seção 8). Em cima, uma linha: "Vencimento [data fatal], segurança [data], pelo [de onde veio o número de dias]". Embaixo, os avisos, sem esconder nenhum. Se as duas contas não bateram (código 2), diga isso primeiro: vale a data mais cedo, e o prazo vai para a pessoa com as duas datas. Se o script abriu "PARA A PESSOA DECIDIR" (linha do calendário não conferida que muda a conta, ciência em dia sem expediente, partida no recesso), diga a dúvida logo depois da primeira linha, com as duas datas e onde conferir: a data mais cedo é a que fica até a pessoa conferir no ato do tribunal.

### Passo 5. Hoje ou amanhã
Se o script escreveu PESSOA AGORA (segurança ou fatal hoje ou amanhã, vencido, ou ciência tácita em até 2 dias úteis), diga isso antes de tudo, em uma frase, e pergunte: "Quem cuida deste prazo agora?". No ciclo, o item vai para o topo do resumo em PESSOA AGORA.

### Passo 6. Gravar a linha `sugerido`
Pergunte: "Posso gravar este prazo como sugerido em prazos.csv?". Com o ok, acrescente a linha em `escritorio/07-operacao/controladoria/prazos.csv` (sem o arquivo, crie com a linha de títulos de `prazos.md`):

| Coluna | O que vai |
|---|---|
| `id` | O próximo `PZ-AAAA-NNNN` |
| `publicacao_id`, `codigo_caso`, `cliente_curto`, `processo` | Da publicação |
| `tipo` · `providencia` | `prazo` · o que o ato pede, em poucas palavras ("recolher custas complementares") |
| `rito` · `dias` · `contagem` | O rito · o número de dias **antes de dobrar** (vazio quando o ato não diz e a tabela não traz) · `uteis` ou `corridos` |
| `regra` | As chaves do script, separadas por `+` (ex.: `publicacao-diario+juizado-federal`) |
| `em_dobro` | `nao`, ou `sim` só com a decisão da pessoa |
| `publicada_em` | A publicação; na intimação do portal e na ciência informada, a data da ciência usada |
| `inicio`, `vencimento`, `data_seguranca` | Da conta (a mais cedo, quando houve dúvida). Vazios quando falta o número de dias |
| `responsavel` | O que a triagem trouxe; sem ele, vazio (o resumo mostra "sem responsável") |
| `status` · `calculado_por` | `sugerido` · `ia` |
| `conferido_por`, `conferido_em`, `cumprido_em`, `peca_id` | Vazios. A IA nunca escreve nome em `conferido_por` |
| `observacao` | De onde veio o número de dias, a outra leitura da ciência ou do calendário (a dúvida inteira), os avisos curtos. Sem número de dias: "[A CONFIRMAR: quantos dias]" |
| `atualizado_em` | Hoje |

Na mesma rodada, em `publicacoes.csv`: `publicada_em` calculada e `prazo_id`, com `atualizado_em`.

### Passo 7. A fila (no ciclo e a pedido)
Grave o item `item: conferir-prazo` (seção 6) e diga: "O prazo está como sugerido. Ele só vai para a agenda depois da dupla conferência." Ofereça a `dupla-conferencia` agora.

### Passo 8. Aprender
Pergunte: "Tem alguma coisa nesta conta que vocês fazem diferente?". Correção de calendário vira linha nova pela `calendario-forense`; regra do escritório ("todo recurso também na agenda do sócio") vira proposta para `regras_proprias` ou para `aprendizados-controladoria.md`, com o ok (`../../docs/aprender-com-o-uso.md`). Correção que pediria data mais tarde sem fonte ("pode contar mais um dia, sempre dá") não vira regra: explique a regra fixa 3.

### Modo no ciclo
1. O agente passa a publicação triada. Não pergunte nada e não mostre nada.
2. Rode o passo 3 com `--json --duplo --hoje <hoje>`. Número de dias: do teor (o ato diz) ou da tabela por `--ato`. Sem os dois: não rode a conta; o prazo entra em `prazos.csv` como `sugerido`, com `dias`, `inicio`, `vencimento` e `data_seguranca` vazios e `observacao` "[A CONFIRMAR: quantos dias]", e o item vai para a fila com a mesma marca em `antes_de_enviar`. Se o ato é de hoje ou de ontem (disponibilização ou ciência), ele vai também para PESSOA AGORA: a pessoa precisa ver e dizer os dias. O `--csv` mostra essa linha na seção "SEM NÚMERO DE DIAS" e não quebra o lote.
3. Código 1 (sem calendário, prazo material, ato fora da tabela): grave um `item: aviso` com a mensagem do script e siga.
4. Grave a linha `sugerido` (passo 6) e o item (seção 6), com todos os avisos em `antes_de_enviar` e PESSOA AGORA quando o script disser.
5. Devolva ao agente: quantos prazos sugeridos, quantos em PESSOA AGORA, quantos não contados e por quê.

### Modo treino
Use `../calendario-forense/assets/calendario-de-treino.md` e `../calendario-forense/assets/regras-de-treino.md`, com `--hoje 2026-04-14 --seguranca 2`. Grave em `escritorio/07-operacao/_treino/controladoria/prazos.csv`, nunca no registro real. O gabarito está na seção 7, e o teste roda tudo de uma vez:

```
python3 "<pasta desta habilidade>/scripts/testar_gabarito.py"
```

Ele diz OK ou FALHOU em cada caso do gabarito e nos casos extras das regras. Qualquer FALHOU: não use o script em prazo real até corrigir.

### Modo adaptar
1. Leia `nicho.md`, a ficha, a tabela de regras e os aprendizados.
2. Liste os atos que o nicho cumpre sempre e que não estão em "Prazos por ato", e os ritos que aparecem (por exemplo, juizado federal e recurso inominado no previdenciário).
3. Marque `[NOVO]` e passe a lista para a `calendario-forense` (passo 7 dela), onde a pessoa preenche o número e a fonte. Nenhum número sai daqui.

## 4. As regras que o script aplica

Cada chave de `../../docs/contagem.md`, como o script conta (os artigos estão lá, marcados `[CONFERIR]`):

| Chave | O script faz |
|---|---|
| `publicacao-diario` | Publicação no primeiro dia com expediente depois da disponibilização; início no primeiro dia útil depois da publicação |
| `civel-cpc`, `trabalhista-clt`, `juizado-civel`, `juizado-federal` | Dias úteis; o dia 1 é o início |
| `penal-cpp` | Dias corridos a partir do dia seguinte; só o vencimento vai para o dia útil seguinte |
| `recesso-forense`, `recesso-trabalhista` | Os dias marcados `recesso` no calendário não contam |
| `recesso-penal` | No penal, o recesso só suspende com `--recesso-penal` (a pessoa confirmou que a exceção não se aplica) |
| `intimacao-portal` | Ciência tácita no fim do prazo de ciência da tabela (10 dias corridos do envio). Se cai em dia sem expediente, duas leituras: ciência no próprio dia ou no dia útil seguinte; fica a mais cedo, e a dúvida vai para a pessoa |
| `domicilio-eletronico` | Não calcula a ciência: conta a partir da data que a pessoa viu (`--ciencia --domicilio`) |
| `indisponibilidade` | Só a `indisponibilidade-certificada` no dia do vencimento empurra. A programada só avisa; no meio do prazo, nada muda |
| `expediente-reduzido` | No dia do começo, o início vai para o dia útil seguinte; no vencimento, empurra |
| `fazenda-dobro`, `defensoria-dobro`, `mp-dobro`, `litisconsortes-dobro` | Só com `--dobro <chave>`, decisão da pessoa. Avisa `juizado-sem-dobro` nos juizados e o processo eletrônico nos litisconsortes |
| `prazo-material` | Recusa com código 1 |
| Linha do calendário não conferida | Linha sem `conferido_em`, sem fonte ou com `[CONFERIR]` que muda a conta: o script faz as duas leituras (contando e não contando o dia), fica com a mais cedo no vencimento e na segurança, e mostra em destaque "DÚVIDA DO CALENDÁRIO: [data] não conferida; a outra leitura daria [data]; conferir no ato do tribunal". Linha com data `[A PREENCHER]` não entra na conta e também sai como dúvida |
| Partida no recesso, numa suspensão ou em dia sem expediente | Disponibilização, publicação ou ciência dentro do recesso ou de suspensão: a data mais cedo e o aviso "conferir no ato do tribunal como ele trata a publicação no período" (`contagem.md`, regra de ouro 6). Disponibilização em sábado, domingo ou feriado: aviso para conferir a data no diário |

## 5. O script

```
python3 calcular_prazo.py --disponibilizacao AAAA-MM-DD | --ciencia AAAA-MM-DD | --envio-portal AAAA-MM-DD
    --dias N | --ato "<ato>" --regras <regras-de-contagem.md>
    --rito civel|trabalhista|juizado-civel|juizado-federal|penal|outro
    --tribunal SIGLA --calendario <arquivo ou pasta>
    [--contagem uteis|corridos] [--dobro [CHAVE]] [--seguranca N] [--json] [--duplo]
    [--recesso-penal] [--domicilio] [--cidade NOME] [--hoje AAAA-MM-DD] [--sem-calendario] [--prazo-material]
python3 calcular_prazo.py --csv prazos.csv --publicacoes publicacoes.csv --calendario <pasta> --regras <arquivo> [--gravar] [--saida <arquivo.md>]
```

- **Duas contas.** A conta 1 anda dia a dia, olhando o calendário a cada dia. A conta 2 monta de uma vez a lista dos dias úteis do período e pega o dia pelo índice. Sem `--duplo`, a segunda roda em silêncio e só aparece se não bater.
- **Códigos de saída:** 0 conta feita; 1 erro ou recusa (prazo material, falta de dias, falta de calendário para o tribunal, arquivo ou coluna que falta, calendário com tipo ou data fora do formato); 2 as duas contas não bateram, ou o lote tem linha que diverge.
- **Datas** entram como `AAAA-MM-DD` ou `DD/MM/AAAA` e saem sempre `AAAA-MM-DD`.
- **Calendário:** arquivo ou pasta. Tribunal sem calendário: recusa, a não ser com `--sem-calendario` (só fins de semana, aviso em destaque). Mais de um calendário do mesmo tribunal para cidades diferentes: pede `--cidade`. Conta que sai do período do calendário: aviso em destaque.
- **`--ato`** procura o ato na seção "Prazos por ato" da tabela, sem diferenciar maiúscula e acento, e para o rito pedido. `--dias` e `--ato` juntos e diferentes: usa o menor e avisa.
- **Dúvidas em destaque.** Tudo o que tem duas leituras (calendário não conferido, ciência em dia sem expediente, recesso, número de dias) sai no topo, em "PARA A PESSOA DECIDIR", e no JSON em `duvidas`. A data que fica é sempre a mais cedo.
- **`--csv`:** conta todos os prazos abertos de `prazos.csv` (`tipo = prazo`, status `sugerido`, `conferido` ou `agendado`), com as duas contas, e compara com o registro (`prazos-em-lote`). Lê vírgula ou ponto e vírgula, com ou sem BOM, cp1252. Linha sem número de dias aparece em "SEM NÚMERO DE DIAS" (e em PESSOA AGORA se o ato é de hoje ou ontem), sem quebrar o lote. `--gravar` só preenche datas em branco e anota na `observacao` de linhas `sugerido` a divergência, a dúvida do calendário ou do recesso e o "[A CONFIRMAR: quantos dias]", e guarda uma cópia de antes em `lotes/`. Nunca muda status nem `conferido_por`.
- **Número de processo:** nenhum script recusa número por dígito verificador.

## 6. O item da fila

`escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-prazo.md`, no formato de `../../docs/agentes-e-fila.md`:

```markdown
---
status: pendente
codigo: C-2026-0012
para: controladoria (dupla conferência)
canal: interno
tipo: conferir-prazo
item: conferir-prazo
prazo_id: PZ-2026-0001
motivo: PUB-2026-00001, djen, disponibilizada 2026-04-13
revisor: pendente
conta_do_revisor: pendente
prazo: segurança 2026-04-28 · fatal 2026-04-30
antes_de_enviar:
  - regra ainda não validada pelo escritório
  - número de dias pela tabela do escritório (recurso inominado, juizado-federal)
---

## Trecho literal do ato
> "[o trecho, como veio]"

## Dados da conta (o revisor refaz só com estes)
partida: disponibilizacao 2026-04-13 · dias: 10 (tabela: recurso inominado) · rito: juizado-federal
tribunal: TRF6 · contagem: uteis · em dobro: nao · segurança: 2
comando: [o comando do passo 3, com --duplo]

## A conta sugerida
[a saída do script]

## Para a dupla conferência
Pergunta sem a sugestão: "O que este ato pede, em quantos dias, e há prazo em dobro?"
```

## 7. O gabarito de treino

Calendário e regras de treino, `--hoje 2026-04-14 --seguranca 2`:

| Caso | Comando (o essencial) | Tem que sair |
|---|---|---|
| Lote 1 · Otávio · JEF | `--disponibilizacao 2026-04-13 --ato "recurso inominado" --rito juizado-federal --tribunal TRF6` | Publicada 2026-04-14, início 2026-04-15, **vencimento 2026-04-30**, segurança 2026-04-28; pula 04-16 e 04-21 |
| Lote 3 · Camila · TRT3 | `--disponibilizacao 2026-04-09 --ato "recurso ordinário" --rito trabalhista --tribunal TRT3` | Publicada 2026-04-10, início 2026-04-13, **vencimento 2026-04-24**, segurança 2026-04-22; vai para o topo (captada com atraso) |
| Lote 4 · Renata · TJMG | `--disponibilizacao 2026-04-14 --dias 5 --rito civel --tribunal TJMG` | Publicada 2026-04-15, início 2026-04-17, **vencimento 2026-04-24**, segurança 2026-04-22; aviso: manutenção sem certidão não empurra |
| Lote 8 · Marta · JEF | `--disponibilizacao 2026-04-14 --dias 15 --rito juizado-federal --tribunal TRF6` | Publicada 2026-04-15, início 2026-04-17, **vencimento 2026-05-11**, segurança 2026-05-07 |
| Lote 10 · Paulo · TRT3 | `--envio-portal 2026-04-06 --dias 5 --rito trabalhista --tribunal TRT3` | Ciência 2026-04-16 (feriado de treino), início 2026-04-17, **vencimento 2026-04-24**, segurança 2026-04-22; a outra leitura daria 2026-04-27; PESSOA AGORA pela ciência tácita |
| E1 · Renata · TJMG | `--disponibilizacao 2026-12-17 --ato "embargos de declaração" --rito civel --tribunal TJMG` (e `--ato "apelação"`) | Publicada 2026-12-18, início 2027-01-21, embargos **2027-01-27**, apelação **2027-02-12** (pula o carnaval de treino) |
| E2 · Marta · JEF | O ato da linha 5 | O prazo é do INSS: nenhuma linha em `prazos.csv`. Se alguém rodar com `--dobro`, o script só dobra e avisa `juizado-sem-dobro`: vai para a pessoa |
| E3 · Jorge | "decadência para revisar o benefício" | Recusa com código 1: `prazo-material`. A pessoa informa a data |

As linhas 2, 5, 6, 7 e 9 do lote não geram conta: pauta, prazo da outra parte, duplicada, sem caso e RPV.

## 8. Formato da saída

```
CONTA DO PRAZO · TRF6 · rito juizado-federal · 10 dias úteis
[PESSOA AGORA, quando for o caso]
PARA A PESSOA DECIDIR (dúvidas da conta; vale a data mais cedo até a decisão):
  >> [DÚVIDA DO CALENDÁRIO | DA CIÊNCIA | DO RECESSO | DA DISPONIBILIZAÇÃO, quando houver]
Passo 1. Disponibilização: 2026-04-13 (seg)
Passo 2. Publicação: 2026-04-14 (ter) · primeiro dia útil depois da disponibilização (publicacao-diario)
Passo 3. Início: 2026-04-15 (qua) · primeiro dia útil depois de 2026-04-14
Passo 4. Dias contados:
      1  2026-04-15 (qua)
         2026-04-16 (qui) pulado: feriado: Feriado municipal de treino em Belo Horizonte (inventado)
      ...
     10  2026-04-30 (qui)
Passo 5. Vencimento (data fatal): 2026-04-30 (qui)
Passo 6. Data de segurança (a data da agenda): 2026-04-28 (ter) · 2 dias úteis antes do vencimento
Regras usadas: publicacao-diario, juizado-federal, cada uma com o artigo de contagem.md [CONFERIR]
Número de dias: tabela do escritório (linha, ato, rito, fonte) | informado: o próprio ato
Conta 1 e conta 2 · AS DUAS CONTAS BATEM
Avisos: regra ainda não validada, calendário não conferido, indisponibilidade sem certidão, dúvida da ciência...
Linha sugerida para prazos.csv: ...
```

## 9. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Linha `sugerido` | `escritorio/07-operacao/controladoria/prazos.csv` |
| `publicada_em` e `prazo_id` da publicação | `escritorio/07-operacao/controladoria/publicacoes.csv` |
| Item de conferência | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-prazo.md` |
| Aviso (sem calendário, ato fora da tabela, prazo material) | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-<assunto>.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: a conta sai no chat, e a linha do `prazos.csv` vai em bloco para colar na planilha.

## 10. Solo e equipe

**Solo:** rode a conta logo que a publicação chega e deixe a conferência para outro turno do mesmo dia: a advogada sozinha confere melhor depois do almoço do que logo em seguida. A data da agenda é a de segurança.

**Equipe:** a estagiária roda a conta e grava `sugerido`; quem confere é outra pessoa, pela `dupla-conferencia`. Ninguém agenda pela conta da IA. Se a conta da estagiária e a do script diferem, as duas vão para o item, e a mais cedo vale até a decisão.

## 11. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Número de dias de memória | Prazo errado com aparência de certo | Regra fixa 2; o script recusa sem `--dias` ou sem o ato na tabela |
| Feriado local esquecido | Vencimento um dia antes ou depois | Calendário do tribunal obrigatório; cada dia pulado aparece com o motivo |
| Manutenção sem certidão empurrando o prazo | Prazo perdido no dia seguinte | Só `indisponibilidade-certificada` empurra; a programada só avisa |
| Ciência tácita em feriado contada pela data mais tarde | Prazo perdido por um dia | As duas leituras à vista; fica a mais cedo |
| Dobro aplicado sem ninguém decidir | Prazo perdido pela metade | `--dobro` só com a pessoa; aviso nos juizados |
| Prazo da outra parte na agenda do escritório | Trabalho à toa e confusão no caso | Passo 1: sem trecho que peça algo ao escritório, não há conta |
| Prazo material contado como processual | Decadência perdida | O script recusa `prazo-material` |
| Conta da IA agendada sem conferência | Erro do script vira prazo | Toda linha é `sugerido`; a agenda só lê `conferido` |

## 12. Próximo passo

- Prazo sugerido: `dupla-conferencia`, de preferência no mesmo dia.
- Conferido: `agenda-de-prazos` (se instalada; sem ela, mostre o texto do compromisso com a data de segurança e a fatal para a pessoa lançar).
- Sem calendário ou tabela: `calendario-forense`.
- Muitos prazos de uma vez: `prazos-em-lote` (se instalada).

## Referências desta habilidade

- `scripts/calcular_prazo.py`: a conta (seção 5). Usado também pela `dupla-conferencia`, pela `prazos-em-lote`, pelo `agente-de-controladoria` e pelo `revisor-de-controladoria`.
- `scripts/testar_gabarito.py`: roda o gabarito da seção 7 e os casos extras das regras; diz OK ou FALHOU. Rode depois de qualquer mudança no script ou nos arquivos de treino.
- `../calendario-forense/assets/calendario-de-treino.md` e `../calendario-forense/assets/regras-de-treino.md`: o calendário e as regras de treino.
