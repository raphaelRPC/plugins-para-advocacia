---
name: painel-da-controladoria
description: >
  Monta o painel interno da controladoria por script, a partir do prazos.csv e do
  publicacoes.csv: prazos da semana por responsável, carga de cada pessoa por status, risco
  (sugerido perto do fatal, fatal passada sem cumprimento, sem data, conferido ou agendado sem a
  dupla conferência, conferido sem agenda, sem responsável), publicações por fonte e por triagem,
  audiências e perícias próximas. Entrega em .md e numa página HTML interna (responsiva, clara e
  escura), com três leituras e três ações sem causa inventada. Nunca vai para cliente. Use quando
  disserem "como está a controladoria", "painel da semana", "quem está com mais prazo", "o que
  está em risco", "leva o painel para a reunião". Não use para o resumo do dia com a fila de
  conferência (use rotina-da-controladoria).
---

# Painel da controladoria

> Um retrato da semana para a equipe decidir onde agir: quem está com que prazos, o que está em risco e de onde vêm as publicações. Fica dentro do escritório.

Regras: `../../docs/regras.md` (em especial a seção 6.1). Prazos e status: `../../docs/prazos.md`. Contagem e dia útil: `../../docs/contagem.md`. Campos das fichas: `../../docs/ficha-da-controladoria.md` e `../../docs/ficha-da-controladoria-modelo.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

Segunda, reunião das 8h30. A pergunta "como estamos de prazo?" tem duas respostas: a da estagiária, que lembra dos que captou, e a da advogada, que lembra dos que vai cumprir. O painel mostra os dois lados: quatro prazos na semana, todos com a mesma advogada, três ainda sugeridos com a data de segurança na quarta. A reunião sai com a conferência marcada para a manhã e um prazo redistribuído.

**Regras fixas desta habilidade:**
1. Painel interno. Nunca é compartilhado com cliente, nem por link nem por imagem (seção 6.1 de `regras.md`). Não mostra número de processo.
2. Prazo `sugerido` nunca aparece como se valesse: a data sai "sugerida" e o selo diz "sugerido, ainda não vale".
3. Número só dos registros. Coluna vazia é dado que ainda não existe; o painel diz isso e não completa.
4. Leitura sem causa inventada e sem avaliação de pessoa. O painel mostra distribuição; a conversa sobre desempenho não é com ele.
5. Treino não entra no painel real. Registro de `_treino/` gera painel marcado "treino".

## 1. Quando usar

**Use quando:**
- A reunião da equipe, no começo da semana, pede um retrato dos prazos.
- Alguém quer saber quem está com mais prazo, ou o que está em risco.
- Antes de férias ou licença, para ver a carga de quem sai (depois, a `cobertura-de-ausencia`, se instalada).
- Para acompanhar se a captação está chegando por todas as fontes.
- Para testar o plugin com os registros do lote de treino.

**Não use quando:**
- O pedido é o dia de hoje, com PESSOA AGORA e a fila: `rotina-da-controladoria` ou `/motor-controladoria:status`.
- O pedido é o fechamento do mês (cumpridos no último dia, perdidos, divergências): `auditoria-de-prazos` (se instalada).
- O pedido é mostrar o caso ao cliente: o painel nunca vai para cliente; a página do caso é da `pagina-do-caso`, do motor-experiencia (se instalado).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` se existir e `aprendizados-controladoria.md`.
2. **Ache os registros:** `escritorio/07-operacao/controladoria/prazos.csv` e `publicacoes.csv` (formato em `../../docs/prazos.md`). Planilha do Excel serve.
3. **Calendários:** `escritorio/04-base/controladoria/calendario/`. Sem calendário, as janelas de dias úteis só pulam fins de semana, e o painel avisa em destaque.
4. **Leia o painel anterior** em `07-operacao/controladoria/painel/`, se existir, para comparar.
5. **Conta de IA:** o painel tem código e primeiro nome de clientes. Em conta pessoal, só os registros de treino.
6. **Sem ficha:** ofereça `/motor-controladoria:comecar`. Para seguir, pergunte só: "Quem cumpre os prazos de cada área?" (`responsaveis_por_area`).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `responsaveis_por_area` |
| Melhora | K: `dias_de_seguranca` |

O `responsaveis_por_area` diz quem deveria aparecer na carga: responsável que está na ficha e não tem nenhum prazo, ou prazo com responsável que não está na ficha, vira pergunta na leitura. O `dias_de_seguranca` define o "sugerido perto do fatal"; o script lê o número da ficha sozinho (só o que vem antes do parêntese) e, sem ficha, usa o padrão do modelo (2) com aviso.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Painel da semana | Reunião, rotina semanal | Passos 1 a 7; grava `.md` e, se quiserem, o HTML |
| Pergunta rápida | "Quem está com mais prazo?" | Passo 2 e a resposta em três linhas, sem gravar |
| Treino | Primeiro uso, teste do plugin | Roda com `assets/prazos-de-treino.csv` e `assets/publicacoes-de-treino.csv`, grava em `_treino/controladoria/painel/` |
| Adaptar | A `adaptar-controladoria` chama | Ajusta as janelas e os rótulos ao escritório (por exemplo, semana de 10 dias úteis para quem tem prazos longos), com `[ALTERADO]`, e grava só com o ok |

O painel é interno e não tem rascunho para cliente, então não entra na fila. A tarefa agendada da `rotina-da-controladoria` pode pedir o painel toda segunda.

### Passo 1. Data e janelas
Pergunte só o que faltar: "Painel com a data de hoje? A semana são os próximos 5 dias úteis?". Com a ficha preenchida, o script lê os dias de segurança sozinho.

### Passo 2. Rodar o script
Rode o script da pasta desta habilidade, com o caminho dos registros. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria/scripts/painel_controladoria.py" \
  "escritorio/07-operacao/controladoria/prazos.csv" \
  --publicacoes "escritorio/07-operacao/controladoria/publicacoes.csv" --data AAAA-MM-DD \
  --saida "escritorio/07-operacao/controladoria/painel/AAAA-MM-DD.md"
```

Outras opções: `--semana N` (dias úteis, padrão 5), `--audiencias N` (dias corridos, padrão 15), `--dias-de-seguranca N` (por cima da ficha), `--ficha`, `--calendario`, `--feriados`, `--treino` (obrigatório para `_treino/`). O script lê csv de vírgula ou ponto e vírgula, com ou sem BOM, datas AAAA-MM-DD ou DD/MM/AAAA, e status sem diferenciar maiúscula. Sai com código 1 e "ERRO:" quando falta o arquivo, falta coluna obrigatória (`id`, `codigo_caso`, `tipo`, `vencimento`, `data_seguranca`, `responsavel`, `status`, `atualizado_em`), os registros não têm nenhuma linha ou o registro é de treino sem `--treino`. Nunca mostra um painel vazio como se estivesse tudo em dia.

**Teste com o treino:**

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria/scripts/painel_controladoria.py" \
  "${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria/assets/prazos-de-treino.csv" \
  --publicacoes "${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria/assets/publicacoes-de-treino.csv" \
  --data 2026-04-20 --treino
```

Resultado esperado em 2026-04-20 (segunda), com o calendário de treino da `calendario-forense` (se instalada): 6 em aberto (5 prazos sugeridos e a audiência do Paulo); 3 com segurança no próximo dia útil (2026-04-22, porque 2026-04-21 é Tiradentes): Camila, Renata e Paulo; 4 na semana, todos da "advogada" (os três e o Otávio, segurança sugerida 2026-04-28); risco: os mesmos três como "sugerido com a fatal em até 3 dias úteis"; publicações: djen 8, email 1, painel 1; 1 sem caso esperando decisão (PUB-2026-00007); nenhuma audiência nos próximos 15 dias (a do Paulo é 2026-05-20). Nenhuma data sai como se valesse: tudo está `sugerido`.

Sem o script (chat sem arquivos): calcule à mão pelas regras de `references/como-ler-o-painel.md`, seção 1, e diga que foi à mão.

### Passo 3. Conferir os avisos
Leia "Avisos de preenchimento" e o destaque do topo. Status fora da lista, data que não leu, sem calendário: mostre a linha e pergunte se corrige o registro agora (pela habilidade dona da coluna). O painel não corrige registro.

### Passo 4. Três leituras
Escreva três leituras, cada uma com o número e de onde ele vem (`references/como-ler-o-painel.md`, seção 2). Exemplos, com o treino:
- "Os 4 prazos da semana estão com a advogada, e os 4 ainda estão `sugerido`."
- "3 prazos sugeridos têm a data de segurança na quarta, 2026-04-22, sem dupla conferência."
- "1 publicação sem caso espera decisão desde 2026-04-14: de quem é o processo da Rosângela?"
Se houver painel anterior, uma das leituras compara.

### Passo 5. Três ações
Uma ação por leitura, com dono (função), até quando e a habilidade que cuida:
- "Dupla conferência dos três da quarta, hoje às 14h: `dupla-conferencia`."
- "Decidir se algum prazo da semana muda de responsável: reunião; registrar em `responsavel`."
- "Responder sobre o processo sem caso: a advogada, hoje; depois a `triar-publicacoes` liga ou marca como erro."
Habilidade não instalada: diga em uma linha o que fazer à mão.

### Passo 6. A página HTML (se quiserem)
Pergunte: "Quer a versão em página, para abrir na reunião?". Se sim, rode com `--html`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/painel-da-controladoria/scripts/painel_controladoria.py" \
  "escritorio/07-operacao/controladoria/prazos.csv" \
  --publicacoes "escritorio/07-operacao/controladoria/publicacoes.csv" --data AAAA-MM-DD \
  --nome-do-escritorio "[NOME]" --html "escritorio/07-operacao/controladoria/painel/AAAA-MM-DD.html"
```

O script preenche o modelo `assets/painel-modelo.html`: responsivo até a tela do celular (390 px de largura, sem rolagem lateral), claro e escuro pelo sistema, sem nada externo, com a faixa "Uso interno do escritório. Não compartilhar com cliente." no topo. Antes de publicar como artefato do Claude, diga: "Esta página é interna. O artefato nasce privado; não compartilhe o link com cliente nem fora da equipe (conferir na configuração da conta como o compartilhamento funciona)." Se o escritório preferir, a página fica só no arquivo, aberta no navegador.

### Passo 7. Gravar
Mostre o painel com as leituras e as ações e grave com o ok em `07-operacao/controladoria/painel/AAAA-MM-DD.md` (leituras e ações no fim, com a coluna de decisão).

### Passo 8. Aprender
Pergunte: "Alguma leitura ou ação você faria diferente? Alguma janela que não serve para vocês?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Janela ou rótulo que muda de vez vai para o modo adaptar.

## 4. O que o painel mostra

| Seção | De onde vem | O que responde |
|---|---|---|
| Números | os dois registros | O tamanho da semana e os alertas |
| Prazos da semana por responsável | `responsavel`, `data_seguranca`, `vencimento` | Quem tem o quê nos próximos dias úteis |
| Carga por responsável | `responsavel`, `status`, `tipo` | Onde está o gargalo: muito sugerido parado, ou muito agendado com uma pessoa só |
| Risco | `status`, datas, `conferido_por` | O que pode virar prazo perdido se ninguém agir |
| Publicações por fonte | `fonte`, `disponibilizada_em`, `triagem` | Se todas as fontes estão chegando e se a triagem está em dia |
| Audiências e perícias | `tipo`, `vencimento`, `observacao` | O que vem nos próximos 15 dias |

`cumprido`, `perdido` e `cancelado` ficam fora; o fechamento do mês é da `auditoria-de-prazos` (se instalada).

## 5. Formato da saída

O painel em .md segue a ordem da seção 4, com o cabeçalho "Uso interno do escritório. Não compartilhar com cliente." Depois do painel, no chat e no fim do arquivo:

```
## Leituras
1. [LEITURA COM NÚMERO E FONTE]
2. ...
3. ...

## Ações
| Ação | Dono | Até | Habilidade | Decisão |
|---|---|---|---|---|
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Painel (.md, com leituras e ações) | `escritorio/07-operacao/controladoria/painel/AAAA-MM-DD.md` |
| Página HTML (opcional, interna) | `escritorio/07-operacao/controladoria/painel/AAAA-MM-DD.html` |
| Painel de treino | `escritorio/07-operacao/_treino/controladoria/painel/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

O painel não muda os registros. Sem pasta aberta: o painel sai no chat, calculado à mão, e a página não é gerada.

## 7. Solo e equipe

**Solo:** o painel da segunda leva cinco minutos e mostra a semana inteira de uma vez. Olhe primeiro o risco e os sugeridos: no escritório de uma pessoa só, o gargalo costuma ser a segunda conferência, que fica para depois.

**Equipe:** o painel abre a reunião da semana. Cada ação tem um dono. Se a mesma pessoa aparece com quase todos os prazos da semana, isso é distribuição, e a conversa é sobre redistribuir, nunca sobre culpa. O painel nunca mostra quem errou.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Painel compartilhado com cliente | Exposição de outros clientes e processos | Regra fixa 1; faixa no topo; aviso antes de publicar; sem número de processo |
| Data sugerida lida como certa | Alguém cumpre pela data que ninguém conferiu | Selo "sugerido, ainda não vale" e "fatal sugerida" |
| Script que não leu e mostra tudo zerado | Falsa tranquilidade | Erro claro sem arquivo, sem coluna ou sem linha |
| Feriado ignorado na janela da semana | Prazo da semana que vem aparece como distante | Calendário por tribunal; sem ele, destaque no topo |
| Leitura que culpa uma pessoa | Equipe na defensiva, painel abandonado | Leitura com número; causa só com dado; regra fixa 4 |
| Painel sem ação | Reunião que só olha números | Três ações com dono e prazo |
| Treino misturado | Prazos falsos na semana | `--treino` obrigatório e painel marcado |

## 9. Próximo passo

- Sugeridos e risco: `dupla-conferencia` ou `/motor-controladoria:fila`.
- Conferido sem agenda: `agenda-de-prazos` (se instalada; sem ela, o texto do compromisso para a pessoa lançar).
- Carga concentrada antes de férias: `cobertura-de-ausencia` (se instalada).
- Fonte que não trouxe nada: `captar-publicacoes` ou `paineis-dos-sistemas` (se instaladas).
- Fechamento do mês: `auditoria-de-prazos` (se instalada).

## Referências desta habilidade

- `scripts/painel_controladoria.py`: o painel por script, em .md e HTML (cópia própria da leitura de registros e calendários). Rode nos passos 2 e 6.
- `assets/painel-modelo.html`: o modelo da página interna, preenchido pelo script. Use no passo 6.
- `assets/prazos-de-treino.csv` e `assets/publicacoes-de-treino.csv`: os registros do lote de treino, para o teste. Use no modo treino.
- `references/como-ler-o-painel.md`: as regras de cálculo e como escrever leituras e ações. Leia nos passos 3 a 5.
