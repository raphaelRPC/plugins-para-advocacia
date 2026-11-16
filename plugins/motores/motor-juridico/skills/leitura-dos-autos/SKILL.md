---
name: leitura-dos-autos
description: >
  Lê o processo inteiro (PDF dos autos, cópia integral ou texto) e devolve o mapa: partes e
  representantes, pedidos e a situação de cada um, decisões e atos, o que cada parte provou,
  o que está em aberto, pontos de ataque e de risco, cada linha com a folha de onde saiu e
  separando o que está nos autos do que é inferência. Prazos aparecem como os autos dizem,
  marcados "a confirmar pela controladoria", sem cálculo. Lê em etapas quando o processo é
  grande e retoma das folhas novas. Use quando o advogado disser "assumi esse processo",
  "lê os autos", "me dá o mapa do processo", "onde esse processo está", "o que a outra
  parte provou", "o que mudou nos autos desde a última vez".
  Não use para documentos soltos de caso novo (use dossie-do-caso) nem para contar prazo
  (é da controladoria).
---

# Leitura dos autos

> O processo inteiro vira um mapa em que cada linha aponta a folha de onde saiu, e o que é conclusão de quem leu vem escrito como inferência.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção, etapas e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 9h. A advogada que cuidava do processo saiu do escritório na sexta. São 312 folhas, uma perícia já feita, uma proposta de acordo do outro lado e um ato ordinatório de que ninguém lembra. A nova advogada tem uma reunião com o cliente às 14h e precisa saber, até lá, o que já foi decidido, o que está pendente e o que pode estar correndo.

**Regras fixas desta habilidade:**
1. Toda linha do mapa traz a fonte (folha, id ou página). Sem fonte, não entra.
2. O que está escrito nos autos é `autos`. O que é conclusão de quem leu é `inferência`, com a base ao lado. As duas nunca se misturam na mesma linha.
3. Prazo aparece com as palavras do ato e a marca `[A CONFIRMAR pela controladoria]`. A habilidade não conta dias, não calcula data final e não diz se o prazo passou.
4. Só fala do que leu. Folha não lida fica no registro da leitura e no cabeçalho, nunca vira "nada consta".
5. Citação de norma ou julgado que aparecer no mapa segue `citacoes.md`: o que a parte citou é registrado como citado pela parte, e o que entrar como argumento nosso nasce marcado.

## 1. Quando usar

**Use quando:**
- O escritório assumiu um processo no meio (substabelecimento, troca de advogado, caso que veio de outro escritório).
- Vai haver audiência, sustentação, acordo ou recurso e o advogado quer o processo inteiro na cabeça.
- Chegaram folhas novas e o pedido é "o que mudou desde a última leitura" (modo "continuar").
- O `agente-juridico` recebeu os autos de um processo em andamento (modo "no ciclo").
- Treino com os autos fictícios (modo "treino") ou a `adaptar-juridico` (se instalada) pediu o mapa do nicho (modo "adaptar").

**Não use quando:**
- São documentos soltos de um caso que ainda não virou processo: `dossie-do-caso`.
- O pedido é contar ou controlar prazo: é da controladoria. O mapa só mostra o que os autos dizem.
- O pedido é decidir o que fazer a partir do mapa: `estrategia-do-caso`.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-juridica.md`. Leia `nicho.md`, se existir, e `04-base/juridico/nicho/leitura-dos-autos.md` (materiais do modo adaptar), se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`).
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "De que área é o processo e em que fase ele está, pelo que você sabe?".
4. **Dados.** Autos de cliente só em conta profissional ou de equipe. Processo em segredo de justiça, com criança ou adolescente, ou com laudo completo de saúde: só com autorização expressa do advogado responsável (`regras.md`, seção 6). Peça e confirme antes de abrir.
5. **Leia o que já existe** em `escritorio/07-operacao/juridico/casos/<codigo>/`: `leitura-dos-autos.md` (se existe, o modo é "continuar", a partir de `lido_ate`) e `dossie.md` (fatos e contradições que o mapa deve confirmar ou atualizar).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` |
| Melhora | J: `tribunais_principais` |

`tribunais_principais` ajuda a reconhecer o sistema e o jeito de numerar (folha, id, página do PDF). Sem ele, pergunte uma vez: "A numeração que vale é a folha, o id do sistema ou a página do PDF?".

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Processo curto | Até umas 80 folhas | O PDF ou o texto | O mapa inteiro numa rodada |
| Processo grande | Centenas de folhas | O PDF dos autos | Índice das peças, leitura em etapas com registro, o mapa no fim |
| Continuar | Folhas novas | O mapa anterior e as folhas depois de `lido_ate` | O mapa atualizado, com `[NOVO]` e `[ALTERADO]` |
| No ciclo | O agente chama | Autos na pasta do caso ou em `entrada/` | Mapa, item na fila e ADVOGADO AGORA. Não mostra nada |
| Treino | "É teste" ou o comando pede | `assets/autos-de-treino.md` | O mapa em `_treino/` e a diferença com o gabarito da seção 4.6 |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | O que procurar nos autos por tipo de caso do nicho, para aprovar |

### Passo 1. Receber os autos
- Peça a cópia integral (PDF baixado do sistema ou o texto). Pedaço do processo: o mapa diz no cabeçalho que é pedaço.
- Combine a numeração (folha, id ou página) e use a mesma em todo o mapa.
- Troque dado identificável que a tarefa não precisa pela marcação das regras; o número do processo fica `[PROCESSO]` no mapa.

### Passo 2. Índice das peças
Antes de ler o conteúdo, faça o índice: cada peça com a folha inicial e final (inicial, documentos, decisão, contestação, laudo, ato, certidão). Use o índice do próprio sistema quando vier no PDF. Processo grande: divida em etapas de até 80 folhas, começando pelas decisões e pelos últimos atos (o que está correndo), depois as peças das partes, depois os documentos.

### Passo 3. Ler por etapa
Para cada etapa, preencha as tabelas do `assets/modelo-mapa-dos-autos.md` com o que leu, e o registro da leitura (folhas, data, quem leu). Etapa interrompida: o registro diz até onde foi, e `lido_ate` no cabeçalho. A próxima conversa começa dali.

### Passo 4. Separar autos de inferência
Releia cada linha das seções 5, 6, 8 e 9 e pergunte: "Isso está escrito nesta folha?". Sim: `autos`. Não, é conclusão de quem leu (a outra parte não contestou um ponto; uma alegação ficou sem prova; um pedido não foi apreciado): `inferência`, com a base. Exemplo: "a contestação não menciona o relatório médico" é `autos` (fl. 35 a 42); "o INSS não tem resposta para o relatório" é `inferência`.

### Passo 5. Prazos
Na seção 7, cada ato que fala em prazo, com as palavras do ato entre aspas, a folha e `[A CONFIRMAR pela controladoria]`. Ato que pede manifestação sem dizer prazo também entra. Não escreva data final, "vence em", "já passou" ou "ainda dá tempo". Se não há nos autos sinal de que uma intimação foi cumprida, escreva isso como `autos` ("não há manifestação da autora depois da fl. 49") e leve para ADVOGADO AGORA: quem diz se o prazo corre é a controladoria.

### Passo 6. Ataque e risco
Pontos de ataque: o que nos autos favorece o nosso lado e ainda não foi usado. Pontos de risco: o que favorece o outro lado ou pode virar contra nós. Cada um com a base e a natureza. Efeito jurídico de um ponto (o que um laudo "parcial" muda no pedido, por exemplo) fica `[CONFERIR]` com o advogado: a habilidade aponta o ponto e não decide o efeito.

### Passo 7. Conferir o mapa
Rode o script (seção 4.5). Corrija cada alerta: fonte que falta, natureza errada, prazo sem a marca, data de vencimento que escapou. Rode de novo até "Alertas: 0", ou até sobrar só o aviso de leitura parcial, que vai no cabeçalho.

### Passo 8. Mostrar e gravar
Mostre o resumo (seção 5) e o mapa. Grave com o ok em `casos/<codigo>/leitura-dos-autos.md`. Se existe dossiê, aponte o que os autos confirmam, desmentem ou acrescentam a ele (por exemplo, a mesma contradição de data aparecendo na contestação). No `pecas.csv`, peça em `pedida` vai para `em-analise`.

### Passo 9. Aprender
Pergunte: "Tem alguma peça ou ato que vocês sempre olham primeiro e eu não destaquei?". A resposta vira regra curta e, com o ok, entra em `aprendizados-juridico.md`. Pedido para calcular prazo ("já põe a data final"): explique que o prazo é da controladoria e proponha o que cabe ("destacar no topo todo ato com prazo").

### Modo continuar
1. Leia o mapa anterior e `lido_ate`. Leia só as folhas seguintes.
2. Atualize as tabelas: o que é novo leva `[NOVO]`; o que mudou de situação (pedido decidido, ponto que perdeu força) leva `[ALTERADO]` e a folha nova.
3. Rode o script, suba a versão, atualize `lido_ate`. Mostre primeiro só o que mudou.

### Modo no ciclo
1. O agente passa o caso e o caminho dos autos. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 7 até 150 folhas por caso por ciclo (ou o que a ficha definir `[A DEFINIR]`); o resto continua no próximo ciclo, pelo `lido_ate`.
3. Vai para ADVOGADO AGORA, com uma frase: todo ato com prazo sem sinal de cumprimento nos autos (para a controladoria confirmar), proposta de acordo da outra parte, decisão nova contra o nosso lado, processo em segredo ou com criança sem autorização registrada (nesse caso, pare antes de ler).
4. Grave o mapa e um item na fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-leitura-dos-autos.md`), no formato de `agentes-e-fila.md`: `para: advogado`, `canal: interno`, `tipo: leitura-dos-autos`, `revisor: pendente`, `prazo` (o prazo interno do `pecas.csv`, se houver) e, em `antes_de_enviar`, a cobertura, os prazos para a controladoria e os alertas do script.
5. No `pecas.csv`, só `pedida` para `em-analise` e `atualizado_em`.
6. Devolva ao agente: caminho do mapa, folhas lidas e por ler, atos com prazo, itens em ADVOGADO AGORA.

### Modo treino
Use `assets/autos-de-treino.md`. Grave em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/leitura-dos-autos.md`. Rode o script e mostre a diferença com o gabarito da seção 4.6.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Por tipo de caso do nicho: as peças e os atos que importam mais (o laudo, a proposta de acordo, a decisão de tutela), os pontos de ataque e de risco que costumam aparecer e o que perguntar ao advogado. Tudo `[CONFERIR]` com ele.
3. Marque `[NOVO]` ou `[ALTERADO]`, mostre e pergunte: "Isso é o que vocês procuram primeiro nesse tipo de processo?".
4. Com o ok, grave em `04-base/juridico/nicho/leitura-dos-autos.md`.

## 4. Critérios

### 4.1 Fonte
Folha (`fl. 31`, `fl. 35 a 42`), id do sistema (`id 1234`) ou página do PDF (`p. 18`), sempre a mesma numeração no mapa. Inferência também leva a fonte da base dela.

### 4.2 Autos e inferência
| É `autos` | É `inferência` |
|---|---|
| A decisão indeferiu a tutela "por ora" | A tutela pode ser pedida de novo depois do laudo |
| A contestação não menciona o relatório | O réu não tem resposta para o relatório |
| O laudo fixa o início da incapacidade em 08/2025 | O laudo favorece o pedido desde a cessação |
| Não há certidão sobre a manifestação da autora | A autora pode ter perdido o prazo |

A última inferência da tabela nunca é escrita assim no mapa: vira "não há manifestação da autora depois da fl. 49 `[A CONFIRMAR pela controladoria]`", em ADVOGADO AGORA.

### 4.3 Prazo
Entra todo ato com prazo ou pedido de manifestação, cumprido ou não, com as palavras do ato e `[A CONFIRMAR pela controladoria]`. Nunca: data final, contagem de dias úteis, "vence", "passou", "ainda dá". O prazo interno do `pecas.csv` é outra coisa: é o que alguém informou para ordenar a fila (`producao.md`).

### 4.4 Ataque e risco
Ataque e risco saem dos autos, não de tese geral. Cada ponto cita a folha. Ponto que depende de jurisprudência ("há precedente que afasta a prescrição") nasce marcado e vai para a lista do que pesquisar no Jus IA (`../../docs/pesquisa-jus-ia.md`). A força do ponto é qualitativa (forte, média, fraca, com o porquê), nunca percentual.

### 4.5 O script de conferência
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/leitura-dos-autos`; sem a variável, use o caminho da pasta desta habilidade.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/leitura-dos-autos/scripts/conferir_mapa.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0001/leitura-dos-autos.md"
```

O `scripts/conferir_mapa.py` aponta: linha sem fonte ou com fonte sem número; natureza diferente de `autos` ou `inferência`; prazo sem `[A CONFIRMAR pela controladoria]`; qualquer "vence em", "prazo final", "último dia" ou "termina em" no texto; a cobertura ("Páginas lidas: X de Y"). Lista as inferências à parte. Arquivo que não existe, vazio ou sem tabela: código 1 e a mensagem.

### 4.6 Conferência com os autos de treino
Lendo `assets/autos-de-treino.md`, o mapa tem que ter:

| Seção | Tem que ter | Natureza |
|---|---|---|
| Pedidos | Quatro pedidos; tutela indeferida "por ora" (fl. 31); perícia feita (fl. 43 a 48); restabelecimento e atrasados pendentes | autos |
| Prazos | Quesitos em 15 dias (fl. 31), cumprido na fl. 32; manifestação sobre o laudo em 5 dias (fl. 49); proposta de acordo sem prazo escrito (fl. 50); todos com `[A CONFIRMAR pela controladoria]` | autos |
| Em aberto | Não há manifestação da autora sobre o laudo nem sobre a proposta depois da fl. 49; a certidão da fl. 52 fala só do INSS | autos, em ADVOGADO AGORA |
| Provou | Laudo: incapacidade parcial e permanente para a atividade habitual, início em 08/2025, relatório do assistente compatível (fl. 43 a 48) | autos |
| Ataque | A contestação não menciona o relatório de 20/01/2026 (fl. 35 a 42) | autos |
| Ataque | A prescrição alegada não alcança parcela nenhuma, pelas datas da cessação e do ajuizamento | inferência, `[CONFERIR]` com o advogado |
| Risco | Cessação em 28/02/2026 na inicial e em 05/03/2026 na contestação e na proposta (diferença nos atrasados) | autos; liga com o dossiê |
| Risco | Laudo "parcial" com sugestão de reabilitação: efeito no pedido `[CONFERIR]` com o advogado | inferência |
| Para o advogado | Aceitar ou não a proposta de acordo é decisão dele e do cliente (`estrategia-do-caso`) | |

E não pode: data final de prazo; "o prazo passou"; opinião sobre aceitar o acordo; chance de êxito. O script tem que dar "Alertas: 0".

## 5. Formato da saída

**No chat, primeiro:**

```
AUTOS · [CODIGO] · [primeiro nome] · [classe] · [fase]
Leitura: fl. 1 a [N] de [N] ([completa | parcial: o que falta])
Advogado agora: [atos com prazo sem sinal de cumprimento; proposta de acordo; decisão nova]
Prazos que aparecem: [N], todos a confirmar pela controladoria
Pedidos: [N] decididos, [N] pendentes
Ataque: [o ponto mais forte, com a folha]
Risco: [o ponto mais sério, com a folha]
Inferências no mapa: [N] (lista no fim)
Conferência do mapa: [Alertas: 0 | o que ficou]
```

Depois, o mapa inteiro, no formato de `assets/modelo-mapa-dos-autos.md`.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mapa dos autos | `escritorio/07-operacao/juridico/casos/<codigo>/leitura-dos-autos.md` |
| Item na fila (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-leitura-dos-autos.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/casos/<codigo>/leitura-dos-autos.md` |
| Materiais do nicho | `escritorio/04-base/juridico/nicho/leitura-dos-autos.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

No `pecas.csv`, só `pedida` para `em-analise` e `atualizado_em`. O mapa não vai para o Projeto no Claude (tem dado do caso). Sem pasta aberta: o mapa no chat, em bloco pronto para copiar, e o processo grande em conversas por etapa, cada uma começando pelo registro da leitura da anterior.

## 7. Solo e equipe

**Solo:** rode a leitura completa quando assumir o processo e o modo continuar a cada leva de folhas novas. O resumo de 9 linhas é o que você lê antes de falar com o cliente.

**Equipe:** quem lê (estagiário, advogado júnior) monta o mapa e roda o script; o advogado responsável lê o resumo e as inferências. Os atos com prazo vão também para a controladoria, que confirma a contagem. Se a controladoria tem planilha própria, o mapa não a substitui.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Contar o prazo na leitura | Data final errada que alguém confia | Prazo só com as palavras do ato e a marca da controladoria |
| Conclusão escrita como fato | O advogado afirma em audiência o que os autos não dizem | Coluna natureza, `autos` ou `inferência` |
| Linha sem folha | Ninguém acha o trecho na hora da sustentação | Fonte obrigatória e o script |
| "Nada consta" de folha não lida | Ponto importante esquecido | Registro da leitura e cobertura no cabeçalho |
| Reler o processo inteiro a cada movimentação | Tempo perdido | Modo continuar, a partir de `lido_ate` |
| Opinar sobre o acordo | Decisão tirada do advogado e do cliente | Acordo vai para a estratégia, com o advogado |

## 9. Próximo passo

- Decidir o que fazer com o que o mapa mostrou: `estrategia-do-caso`.
- Responder ao que a outra parte alegou: `advogado-do-diabo` (se instalada; sem ela, os pontos de risco do mapa são a lista).
- Preparar a fala no tribunal: `sustentacao-oral` (se instalada).
- Peça com tese definida: `minutar-peca` (se instalada).

## Referências desta habilidade

- `assets/modelo-mapa-dos-autos.md`: o formato do mapa. Use nos passos 3 a 6.
- `assets/autos-de-treino.md`: os autos fictícios do caso 1. Use no modo treino.
- `scripts/conferir_mapa.py`: a conferência mecânica do mapa (seção 4.5). Rode no passo 7.
