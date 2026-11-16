---
name: audiencias-e-pericias
description: >
  Cuida da pauta de audiências, perícias e sessões de julgamento: registra cada ato em
  prazos.csv com o tipo próprio, a data e a hora do ato e o local ou link, sem inventar prazo;
  mostra a pauta dos próximos dias por script, com o que falta em cada uma; monta o checklist
  por tipo (testemunhas, documentos, link e teste da sala virtual, quesitos e assistente
  técnico para o advogado conferir); manda para a agenda e o aviso para a preparação do
  cliente pela experiência; e trata a redesignação no mesmo registro. Use quando a pessoa
  disser "saiu a pauta", "redesignaram a audiência do Paulo", "quais audiências temos na
  semana?", "a perícia foi marcada", "o que falta para a audiência de quarta?", "o link da sala
  chegou?". Não use para preparar o cliente ou a testemunha (use preparar-o-cliente, do
  motor-experiencia, se instalado) nem para prazo com contagem de dias (use calcular-prazo).
---

# Audiências e perícias

> Pauta não é prazo: é um ato com data, hora e lugar. A habilidade registra o ato do jeito que ele está escrito, lista o que falta para o dia e manda a preparação do cliente para quem fala com ele.

Regras comuns: `../../docs/regras.md`. Registros, status e os outros plugins: `../../docs/prazos.md`. Contagem (para os prazos que a pauta abre): `../../docs/contagem.md`. Fichas: `../../docs/ficha-da-controladoria.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Terça, 9h. Chega o despacho: "redesigno a audiência de instrução para 2026-05-20, às 14h, por videoconferência". O erro comum é ler "instrução" e calcular um prazo que não existe, ou atualizar a agenda e esquecer que o Paulo ainda acha que a audiência é na data antiga. O certo: a linha da audiência muda de data, passa pela conferência, o compromisso é atualizado com a hora, e a experiência recebe o aviso para preparar o Paulo e testar o link com ele.

**Regras fixas desta habilidade:**
1. Pauta não é prazo. Audiência, perícia e sessão entram em `prazos.csv` com `tipo` próprio, a data do ato em `vencimento` e a hora e o local ou link em `observacao`; `dias`, `contagem` e `regra` ficam vazios. Prazo que o ato abre (rol de testemunhas, quesitos) é outra linha, pela `calcular-prazo`.
2. Data, hora e modalidade vêm do trecho literal do ato. O que o ato não diz fica `[A CONFIRMAR]`. O ato passa pela dupla conferência antes de ir para a agenda e para o aviso ao cliente.
3. Testemunha, quesitos e assistente técnico são do advogado. O checklist lembra, marcado `[CONFERIR]`; a IA não prepara testemunha e não escreve quesito.
4. A preparação do cliente é da experiência: daqui sai o aviso, e nada vai ao cliente sem uma pessoa aprovar lá.
5. Ato hoje ou no próximo dia útil vai para PESSOA AGORA. Redesignação atualiza a mesma linha e o mesmo compromisso, e o cliente é avisado de novo.

## 1. Quando usar

**Use quando:**
- A triagem marcou uma publicação como `audiencia` ou `pericia`, ou saiu a pauta de uma sessão de julgamento.
- O perito marcou data e local da perícia.
- A audiência foi redesignada, cancelada ou convertida (presencial para vídeo, por exemplo).
- A pessoa quer a pauta da semana ou dos próximos 15 dias, com o que falta.
- O `agente-de-controladoria` monta a seção "Audiências e perícias" do resumo (modo no ciclo).
- Treino com a linha 2 do lote de `../../docs/casos-ficticios.md`.

**Não use quando:**
- O pedido é preparar o cliente (o que levar, como vai ser, o medo): `preparar-o-cliente` do motor-experiencia (se instalado). Sem ele, o aviso vai como texto para quem fala com o cliente.
- O pedido é preparar testemunha: conversa do advogado, dentro do que a ética permite `[CONFERIR]`.
- O ato pede uma manifestação com prazo em dias: `calcular-prazo`.
- O pedido é contar ao cliente como foi o ato: `status-para-o-cliente` do motor-experiencia (se instalado); resultado ruim é ligação.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` e `aprendizados-controladoria.md`, se existirem.
2. Sem fichas: ofereça `/motor-controladoria:comecar`. Para seguir agora, pergunte só: "Onde fica a agenda de audiências de vocês?".
3. Leia `escritorio/07-operacao/controladoria/prazos.csv` (as linhas de `tipo` audiencia, pericia e sessao), a publicação e o teor em `publicacoes.csv` e `publicacoes/AAAA-MM-DD/`.
4. Leia o checklist do escritório, se existir (`escritorio/04-base/controladoria/nicho/audiencias-e-pericias.md`). Sem ele, use `references/checklists.md`.
5. Dados: o tipo de perícia pode revelar dado de saúde. No registro e no aviso, só o necessário ("perícia médica"), nunca o diagnóstico.

### Campos da ficha que esta habilidade usa

- **Precisa:** K: `onde_fica_a_agenda`.
- **Melhora:** K: `lembretes`, `responsaveis_por_area`.
- Lê também, se preenchidos: E: `o_que_e_urgente`, `dias_e_horarios_fixos` (por exemplo, audiências pela manhã); K: `cobertura_de_ausencia`; X: `cadencia_da_preparacao`, da ficha da experiência (motor-experiencia, se instalado).

Campo vazio que a tarefa pede: pergunte só aquele, uma vez, e ofereça gravar. `responsaveis_por_area` vazio: pergunte "Quem vai a esta audiência pelo escritório?" e grave na linha, em `responsavel`.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| Registrar | Saiu a pauta, o perito marcou | A linha do ato e o checklist | `prazos.csv` (`sugerido`) e o item na fila |
| Pauta | "quais audiências temos?" | A pauta por script, com o que falta | No chat |
| Redesignar | O ato mudou de data, hora ou modalidade | A mesma linha atualizada, nova conferência, agenda e aviso de novo | `prazos.csv`, fila, agenda, entrada da experiência |
| Depois do ato | O ato aconteceu | Baixa pela pessoa e o próximo passo | `prazos.csv` (`cumprido` pela pessoa) |
| No ciclo | O `agente-de-controladoria` chama | Registra o que a triagem marcou, roda a pauta | Linhas `sugerido`, fila, seção do resumo |
| Treino | Linha 2 do lote | O mesmo, em `_treino/` | `escritorio/07-operacao/_treino/controladoria/` |
| Adaptar | `adaptar-controladoria` | Checklists do escritório e do nicho | `04-base/controladoria/nicho/audiencias-e-pericias.md` |

**Modo direto:** "registra a perícia da Marta, dia 2026-05-12, 9h, no consultório do perito". Registre, mostre o checklist e pergunte só o que falta.

### Passo 1. Ler o ato (S)
Do teor, tire o trecho literal que diz o tipo do ato, a data, a hora, a modalidade e o local ou link, e o que o ato manda fazer antes (rol, quesitos, documentos). Mostre o trecho. O que não está escrito fica `[A CONFIRMAR]`.

### Passo 2. Registrar a linha (S)
Se a `calcular-prazo` ou o agente ainda não criou a linha, crie uma em `prazos.csv`: `tipo` = `audiencia`, `pericia` ou `sessao`; `providencia` = o ato em poucas palavras ("audiência de instrução (redesignada)"); `vencimento` = a data do ato; `data_seguranca` vazia; `observacao` = a hora, a modalidade e o local ou link ("14h, por videoconferência; link a ser juntado aos autos"); `status = sugerido`; `calculado_por = ia`. Prazo que o ato abre antes do dia: linha própria, pela `calcular-prazo`.

### Passo 3. A conferência (H)
Na fila, como `item: conferir-prazo` (`NN-<codigo>-prazo.md`), com o trecho literal. A pessoa confirma a data, a hora, a modalidade e o tipo do ato pela `dupla-conferencia` (se instalada). Só depois a linha fica `conferido`.

### Passo 4. O checklist (A)
Use o checklist do tipo (`references/checklists.md`, ou o do escritório). Mostre cada item com quem faz e o que já está resolvido. Pergunte ao responsável, um item por vez, só o que o ato não responde, por exemplo: "As testemunhas do Paulo vêm independentemente de intimação, como diz o despacho, ou vamos pedir a intimação?".

### Passo 5. Agenda e aviso (S, depois de conferido)
- Agenda: `agenda-de-prazos` (se instalada), com `--preparacao N` (N da `cadencia_da_preparacao` da experiência ou o que a pessoa disser). Sem ela, o texto do compromisso para a pessoa lançar.
- Aviso: `encaminhar-providencia` (se instalada), `--aviso audiencia` (ou `pericia`, `sessao`), com o trecho literal. A experiência prepara o cliente e o teste da sala. Sem a experiência, o aviso sai como texto para quem fala com o cliente.

### Passo 6. A pauta (S)
```
python3 <pasta-desta-habilidade>/scripts/pauta.py escritorio/07-operacao/controladoria/prazos.csv --hoje AAAA-MM-DD --dias 15 --escritorio escritorio
```
O script lista as audiências, perícias e sessões abertas até a data, a mais próxima primeiro, e diz o que falta em cada uma (a hora, a modalidade e o local ou link são lidos da `observacao`: "na sede do Juizado", "Fórum", "sala 3", um link; só falta o que não está escrito ali): hora ou local que faltam, ainda sem conferência, conferida e sem agenda, teste da sala virtual, quesitos e testemunhas para o advogado conferir, aviso ao cliente não encaminhado. Ato hoje ou no próximo dia útil vem no topo, em PESSOA AGORA; ato que já passou sem baixa vem no fim. Lê vírgula ou ponto e vírgula, com ou sem BOM, e datas AAAA-MM-DD ou DD/MM/AAAA; sem o arquivo ou sem coluna, para com código 1.

### Passo 7. Redesignação, cancelamento e conversão
1. A publicação nova é lida como no passo 1, e a linha existente do ato é a mesma (mesmo `id`): `vencimento` e `observacao` mudam, e a `observacao` guarda "redesignada de AAAA-MM-DD por PUB-...".
2. A data nova passa pela conferência (passo 3). Até lá, a agenda fica com a data antiga e o item vai para PARA DECIDIR, para ninguém se guiar pela data errada sem saber.
3. Conferida: a `agenda-de-prazos` atualiza o mesmo compromisso (mesmo UID), e a `encaminhar-providencia` manda o aviso de novo, com `--de-novo`, dizendo que a data mudou.
4. Cancelamento sem data nova: só a pessoa muda o status para `cancelado`, com o motivo; a agenda gera o cancelamento; o cliente é avisado.

### Passo 8. Depois do ato
Pergunte ao responsável: "Como foi a audiência? Saiu alguma decisão ou ficou algum prazo?". A baixa (`cumprido`, com `cumprido_em`) é da pessoa. Decisão em audiência vira publicação para a `leitura-da-decisao` (se instalada); prazo aberto em audiência vira linha nova pela `calcular-prazo`; o que contar ao cliente é da `status-para-o-cliente` (resultado ruim por ligação).

### Passo 9. Aprender
Pergunte: "Alguma coisa no checklist ou no registro você faria diferente?". Cada correção vira uma regra curta ("Perícia social no benefício assistencial: avisar o cliente de que a visita pode ser em casa") e, com o ok, entra em `aprendizados-controladoria.md`. Item novo de checklist vira proposta para o checklist do escritório (modo adaptar).

### No ciclo (o agente chama)
1. Para cada publicação triada como `audiencia` ou `pericia` sem linha: passo 2, com `status = sugerido`, e o item `conferir-prazo` na fila.
2. Rode o passo 6 com 15 dias. A seção "Audiências e perícias" do resumo recebe a pauta e o que falta; PESSOA AGORA recebe o que é hoje ou no próximo dia útil sem preparação encaminhada.
3. Redesignação: passo 7, itens 1 e 2. Nada é avisado ao cliente antes da conferência.
4. Não pergunte nada e não mande nada ao cliente.

### Modo adaptar
Leia `nicho.md` e os aprendizados. Reescreva os checklists de `references/checklists.md` para os atos que o escritório tem (por exemplo, audiência una trabalhista, perícia médica em incapacidade, avaliação social), com o que o nicho costuma esquecer. Marque cada mudança `[ALTERADO]` e grave em `escritorio/04-base/controladoria/nicho/audiencias-e-pericias.md` só com o ok.

## 4. Exemplo resolvido (Escritório Modelo, linha 2 do lote, hoje 2026-04-14)

**Paulo · C-2026-0002 · TRT3.** Trecho literal: "redesigno a audiência de instrução para o dia 20/05/2026, às 14h, por videoconferência. As partes deverão comparecer para depoimento pessoal, sob pena de confissão, e trazer suas testemunhas independentemente de intimação. O link da sala virtual será juntado aos autos."

- Linha: `tipo = audiencia`, `providencia = audiência de instrução (redesignada)`, `vencimento = 2026-05-20`, `observacao = 14h, por videoconferência; link da sala virtual a ser juntado aos autos`, `status = sugerido`. Nenhum prazo inventado: o despacho não abre prazo em dias.
- Checklist: depoimento pessoal do Paulo e a consequência de faltar `[CONFERIR]` com a advogada; testemunhas vêm independentemente de intimação (quem são é decisão da advogada); link `[A CONFIRMAR]` até ser juntado; teste da sala com o Paulo antes do dia.
- Depois da conferência: compromisso em 2026-05-20 às 14h00, preparação até 2026-05-13 (5 dias úteis antes, no treino); aviso de compromisso na entrada da experiência com `hora: 14h00` e `modalidade: videoconferência`.
- Na pauta de 2026-04-14 com 40 dias: `2026-05-20 14h00 · audiência · C-2026-0002 Paulo · videoconferência`, com o que falta (agenda, teste da sala, testemunhas para a advogada conferir).

## 5. Formato da saída

```
PAUTA · [AAAA-MM-DD] até [AAAA-MM-DD]
PESSOA AGORA: [ato hoje ou no próximo dia útil, com o que falta]
| Data | Hora | Tipo | Caso | Modalidade | Responsável | Status | O que falta |
Já passaram sem baixa: [id, caso, data]

ATO · [código] · [tipo] · [AAAA-MM-DD HHhMM] · [modalidade]
Trecho literal: "[...]"
Checklist: [item · quem · resolvido | falta | CONFERIR]
Próximo: conferência → agenda → aviso para a preparação
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A linha do ato | `escritorio/07-operacao/controladoria/prazos.csv` (`tipo` audiencia, pericia ou sessao; `sugerido`) |
| Item de conferência | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-prazo.md` (`item: conferir-prazo`) |
| Redesignação à espera de conferência | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-redesignacao.md` (`item: aviso`) |
| A pauta | No chat e na seção "Audiências e perícias" do resumo (`07-operacao/controladoria/rotina/AAAA-MM-DD.md`) |
| Checklists adaptados | `escritorio/04-base/controladoria/nicho/audiencias-e-pericias.md` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |

A agenda grava pela `agenda-de-prazos` e o aviso pela `encaminhar-providencia`. Sem pasta aberta: a linha do registro e o checklist no chat, para colar.

## 7. Solo e equipe

**Solo:** a pauta da semana toda segunda, junto com o resumo; o checklist do ato na semana anterior. Quem vai ao ato é quem conferiu, então o teste da sala com o cliente precisa caber na agenda.

**Equipe:** a controladoria registra, roda a pauta e cobra o que falta; o advogado responsável decide testemunhas, quesitos e assistente técnico; a experiência prepara o cliente. Ato de quem está de férias: `cobertura-de-ausencia` (se instalada).

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Prazo inventado a partir da pauta | Peça desnecessária ou data falsa na agenda | Regra fixa 1 |
| Hora de cabeça | Cliente e advogado no horário errado | Hora do trecho literal; o que falta fica `[A CONFIRMAR]` |
| Redesignação só na agenda | O cliente vai na data antiga | Passo 7: aviso de novo pela experiência |
| Link que nunca chegou | Ninguém entra na sala no dia | A pauta aponta link que falta e o teste da sala |
| Testemunha preparada pela IA | Problema ético | Regra fixa 3 |
| Prazo do rol ou dos quesitos esquecido | Prova perdida | O checklist manda virar linha de prazo própria |
| Audiência amanhã sem ninguém saber | Falta ao ato | PESSOA AGORA no topo da pauta |

## 9. Próximo passo

- Conferir o ato: `dupla-conferencia` (se instalada).
- Pôr na agenda: `agenda-de-prazos`.
- Avisar e preparar o cliente: `encaminhar-providencia` e, lá, `preparar-o-cliente` do motor-experiencia (se instalado).
- O ato aconteceu e saiu decisão: `leitura-da-decisao` (se instalada).

## Referências desta habilidade

- `scripts/pauta.py`: a pauta de audiências, perícias e sessões, com o que falta em cada uma e o PESSOA AGORA. Passo 6 e o modo no ciclo.
- `references/checklists.md`: os checklists de audiência, perícia, sessão e videoconferência, com quem faz cada item. Passo 4 e o modo adaptar.
