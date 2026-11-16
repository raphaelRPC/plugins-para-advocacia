---
name: auditoria-de-prazos
description: A auditoria do mês da controladoria, por script. Lê prazos.csv e os registros de conferência e mostra os prazos cumpridos com a data do protocolo contra a data de segurança e a fatal, os cumpridos no último dia, os perdidos, os vencidos sem registro de cumprimento, os que andaram sem dupla conferência, as conferências que divergiram e as sugestões da IA que a pessoa corrigiu, por responsável. Com a pessoa, cada achado vira um ajuste (calendário, tabela de regras, data de segurança, lembretes, rotina) ou um aprendizado. Use quando disserem "como foram os prazos do mês?", "quantos cumprimos no último dia?", "por que perdemos aquele prazo?", "faz a auditoria de abril", "a IA errou muito as contas?". Não use para conferir um prazo aberto (use dupla-conferencia).
---

# Auditoria de prazos

> Uma vez por mês, os números da controladoria à vista: o que foi cumprido com folga, o que foi no limite, o que se perdeu e onde a conferência pegou erro.

Registros, status e dupla conferência: `../../docs/prazos.md`. Regras de contagem: `../../docs/contagem.md`. Regras gerais: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Onde gravar: `../../docs/pasta.md`. Fila: `../../docs/agentes-e-fila.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Primeira segunda-feira do mês, 17h. Nenhum prazo foi perdido em abril, e a sensação é de que está tudo bem. A auditoria mostra outra coisa: um terço dos recursos foi protocolado no último dia, sempre do mesmo responsável, e duas contas da IA foram corrigidas na conferência pelo mesmo motivo, um feriado de Contagem que não estava no calendário. São dois ajustes de quinze minutos que evitam o primeiro prazo perdido de maio.

**Regras fixas desta habilidade:**
1. A auditoria mostra e pergunta; quem decide o que muda é a pessoa. Nenhum prazo muda de status por esta habilidade.
2. Prazo vencido sem registro de cumprimento e prazo que andou sem dupla conferência vão para PESSOA AGORA, antes de qualquer número.
3. Prazo perdido se registra com a nota do que aconteceu, sem procurar culpado: o que importa é o passo que falhou.
4. Treino (`_treino/`) nunca entra na auditoria real.
5. Sem registro lido, não há auditoria: o script diz o que faltou e nunca responde "nada a apontar".

## 1. Quando usar

**Use quando:**
- Fecha o mês (a `rotina-da-controladoria`, se instalada, lembra no primeiro dia útil).
- Um prazo foi perdido ou cumprido depois da fatal e a pessoa quer entender onde falhou.
- A pessoa quer saber se a data de segurança está sendo respeitada ou se as contas da IA estão sendo corrigidas.
- Antes de rever a tabela de regras ou o calendário, para saber o que mais deu problema.
- A `adaptar-controladoria` (se instalada) chamou no modo "adaptar".

**Não use quando:**
- O pedido é conferir um prazo aberto: `dupla-conferencia`.
- O pedido é o que vence hoje e na semana: `/motor-controladoria:status` ou a `rotina-da-controladoria` (se instalada).
- O pedido é o painel do dia por responsável: `painel-da-controladoria` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-da-controladoria.md` e `nicho.md`, se existir.
2. **Leia os aprendizados** (`aprendizados-controladoria.md`): a auditoria confere se os aprendizados do mês passado funcionaram.
3. **Ache os registros:** `escritorio/07-operacao/controladoria/prazos.csv` e a pasta `conferencias/`. Sem `prazos.csv`, pare: "Ainda não há prazos registrados para auditar."
4. **Ache o que já foi auditado:** `escritorio/07-operacao/controladoria/auditorias/` (o mês anterior, para comparar).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `responsavel_controladoria` |
| Melhora | K: `dias_de_seguranca` |

Sem `responsavel_controladoria`, pergunte: "Quem cuida dos prazos e vai ver esta auditoria comigo?" e ofereça gravar. `dias_de_seguranca` ajuda a ler as faixas: se os prazos se acumulam entre a segurança e a fatal, talvez a segurança esteja curta ou os lembretes cheguem tarde.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Mês | Todo mês | `prazos.csv`, `conferencias/` | Relatório do mês e os ajustes decididos |
| Prazo perdido | Um prazo perdido ou depois da fatal | O prazo | A linha do tempo do prazo, o passo que falhou e o ajuste |
| No ciclo | A rotina do primeiro dia útil do mês | Os registros | O relatório gravado e um `item: aviso` para a pessoa marcar a conversa |
| Treino | "é teste" | Um `prazos.csv` de treino | O relatório marcado como treino, em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | `nicho.md` e a ficha | Os cortes do relatório que interessam ao nicho |

### Passo 1. O mês
Se não veio junto, pergunte: "De que mês é a auditoria?". Padrão: o mês que acabou.

### Passo 2. Rodar o script
Rode o script da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/auditoria_prazos.py" \
  escritorio/07-operacao/controladoria/prazos.csv --mes 2026-04 \
  --conferencias escritorio/07-operacao/controladoria/conferencias \
  --saida escritorio/07-operacao/controladoria/auditorias/2026-04.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/auditoria-de-prazos`. O script lê vírgula ou ponto e vírgula, com ou sem BOM, cp1252, datas `AAAA-MM-DD` e `DD/MM/AAAA`, e sai com código 1 e mensagem clara quando falta arquivo ou coluna. Código 2: achou o que exige ação agora. Sem o script: monte as mesmas contagens à mão, com a tabela de `prazos.csv` na conversa, e diga que foi à mão.

### Passo 3. PESSOA AGORA
Antes dos números, para cada linha de PESSOA AGORA, pergunte uma por vez:
- vencido sem registro: "Este prazo venceu em [data] e está como [status]. Foi cumprido? Se foi, em que dia?";
- sem dupla conferência: "Este prazo está como [status] sem os dois nomes. Quem conferiu?".
Com a resposta, atualize `prazos.csv` só com o que a pessoa disse (`cumprido` e `cumprido_em`, ou `perdido` com a nota, ou os nomes da conferência que a pessoa diz ter feito). Sem resposta, o item fica no relatório e no resumo do dia seguinte.

### Passo 4. Ler os números com a pessoa
Mostre o relatório (seção 4) e leia junto, pela ordem:

| O que o relatório mostra | Pergunta para a pessoa |
|---|---|
| Cumpridos no último dia | "Estes [N] foram no último dia. Foi escolha ou aperto?" |
| Cumpridos depois da fatal | "O protocolo foi depois da fatal. O que aconteceu? A data no registro está certa?" |
| Perdidos | "Em que passo falhou: captação, triagem, conta, conferência, agenda ou cumprimento?" |
| Divergências da conferência | "O que fez as leituras divergirem se repete?" |
| Sugestões da IA corrigidas | "A correção foi de calendário, de regra, do número de dias ou do ato?" |
| Por responsável | "Alguém está com carga demais ou cumprindo sempre no limite?" |

### Passo 5. Do achado ao ajuste
Cada achado que a pessoa confirmar vira um ajuste, na habilidade certa:

| Achado | Ajuste | Onde |
|---|---|---|
| Feriado ou suspensão que faltou | Linha nova no calendário, com fonte | `calendario-forense` |
| Regra contada diferente do que o escritório entende | Revisão da linha da tabela, com a validação | `calendario-forense` (passo 6) |
| Muitos cumpridos no último dia | Mais dias de segurança ou um lembrete a mais | Ficha (`dias_de_seguranca`, `lembretes`) e `agenda-de-prazos` (se instalada) |
| Divergência que se repete | Pergunta a mais na leitura cega | `dupla-conferencia` (modo adaptar) |
| Publicação captada tarde | Horário da captação ou painel que ninguém olhou | Ficha (`horario_da_captacao`) e `paineis-dos-sistemas` (se instalada) |
| Prazo sem responsável | Responsável por área | Ficha (`responsaveis_por_area`) |

Mostre a lista de ajustes e pergunte: "Quais destes entram agora?". Grave só os escolhidos, cada um pela habilidade dele.

### Passo 6. Prazo perdido (modo "Prazo perdido")
Monte a linha do tempo do prazo com o que está nos registros: disponibilização e captação (`publicacoes.csv`), triagem, conta (`calculado_por`, datas), conferência (`conferencias/`), agenda (`agenda/`), cumprimento. Mostre onde o tempo se perdeu e pergunte: "O que aconteceu neste passo?". Grave em `prazos.csv` a nota que a pessoa disser na `observacao` (o status `perdido` é só da pessoa) e o ajuste pelo passo 5. Prazo perdido também é assunto de comunicação com o cliente e de responsabilidade profissional: é da advogada responsável, nunca de mensagem automática.

### Passo 7. Gravar
Com o ok, o relatório fica em `escritorio/07-operacao/controladoria/auditorias/AAAA-MM.md`, com uma seção "Ajustes decididos" no fim: o achado, o ajuste, quem decidiu (o nome que a pessoa disse) e onde foi feito.

### Passo 8. Aprender
Pergunte: "Tem alguma coisa que vocês querem acompanhar todo mês e que eu não mostrei?". O que a pessoa pedir vira linha em `aprendizados-controladoria.md` (por exemplo, "auditoria: mostrar à parte os recursos contra o INSS"), com o ok (`../../docs/aprender-com-o-uso.md`). Se os aprendizados passaram de 30 linhas em uso, ofereça a revisão de lá.

### Modo no ciclo
1. No primeiro dia útil do mês, a rotina roda o passo 2 do mês anterior, com `--saida`. Não pergunta nada.
2. Grava um `item: aviso` em `07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-auditoria-AAAA-MM.md`, com `revisor: pendente`, o caminho do relatório e as linhas de PESSOA AGORA em `antes_de_enviar`.
3. Vencido sem registro e prazo sem dupla conferência entram também no resumo do dia, em PESSOA AGORA. Os ajustes ficam para a conversa com a pessoa.

### Modo treino
Monte um `prazos.csv` em `escritorio/07-operacao/_treino/controladoria/` com as linhas do lote de `../../docs/casos-ficticios.md` já conferidas e com datas de cumprimento inventadas para o teste (por exemplo, uma no último dia e uma depois da fatal), e o registro de conferências com a divergência da linha 4. Rode com `--treino`: o relatório sai marcado como treino. Sem `--treino`, o script recusa a pasta `_treino/`.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Proponha os cortes que interessam ao nicho (por exemplo, por tipo de ato, por tribunal, prazos que dependem do cliente, como documento a juntar).
3. Marque `[NOVO]` e grave na linha da habilidade em `aprendizados-controladoria.md`, com o ok.

## 4. Formato da saída

```
AUDITORIA DE PRAZOS · AAAA-MM
Li N linhas de prazos.csv e N registros de conferência do mês.
PESSOA AGORA
  - [prazo vencido sem registro, cumprido depois da fatal, prazo sem dupla conferência]
Cumpridos no mês: N
  - antes da segurança · na segurança · entre a segurança e a fatal · no último dia · depois da fatal
Perdidos no mês: N (com a nota de cada um)
Vencidos sem registro de cumprimento: N · Andando sem dupla conferência: N
Conferências do mês: N · divergiram N · decididas depois N
Sugestões da IA corrigidas pela pessoa: N
| responsável | cumpridos | no último dia | perdidos | vencidos sem registro |
Para discutir (a decisão é da pessoa): ...
Ajustes decididos: [achado · ajuste · quem decidiu · onde]
```

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Relatório do mês e ajustes decididos | `escritorio/07-operacao/controladoria/auditorias/AAAA-MM.md` |
| Respostas da pessoa (cumprido, perdido, nota) | `escritorio/07-operacao/controladoria/prazos.csv` |
| Aviso da auditoria (ciclo) | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-auditoria-AAAA-MM.md` |
| Ajustes | Nas habilidades e fichas de cada um (passo 5) |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: o relatório sai no chat, montado à mão a partir da tabela colada, e os ajustes vão em bloco para copiar.

## 6. Solo e equipe

**Solo:** reserve meia hora no primeiro dia útil do mês. O número que mais importa para quem trabalha sozinho é o de cumpridos no último dia: é ele que mostra quando a agenda está apertando.

**Equipe:** a auditoria é para a reunião do mês, com quem responde pela controladoria e quem cumpre os prazos. Os números por responsável são para dividir a carga, não para comparar pessoas. Prazo perdido é conversa da advogada responsável com o cliente, fora da auditoria.

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Achar que está tudo bem porque nenhum prazo foi perdido | O primeiro perdido vem do hábito de cumprir no limite | Faixas contra a segurança e a fatal |
| Prazo vencido esquecido como `agendado` | Ninguém sabe se foi cumprido | PESSOA AGORA para vencido sem registro |
| Prazo que andou sem dupla conferência | Erro de conta sem ninguém ver | PESSOA AGORA para `conferido_por` sem os dois nomes |
| Correção da IA que se repete todo mês | O mesmo erro em cada conta | Sugestões corrigidas viram ajuste de calendário ou regra |
| Auditoria com o treino misturado | Números falsos | O script recusa `_treino/` sem `--treino` |
| Auditoria sem ler nada dizendo que está tudo certo | Falsa segurança | O script sai com erro quando falta registro |

## 8. Próximo passo

- Calendário ou regra a ajustar: `calendario-forense`.
- Data de segurança ou lembretes: `/motor-controladoria:ficha` e `agenda-de-prazos` (se instalada).
- Divergência que se repete: `dupla-conferencia` no modo adaptar.
- Prazo perdido com reflexo no cliente: a advogada responsável; o roteiro de ligação pode ser preparado pela `status-para-o-cliente`, do motor-experiencia (se instalado; sem ele, a advogada liga com as notas da linha do tempo).

## Referências desta habilidade

- `scripts/auditoria_prazos.py`: o relatório do mês (passo 2). Lê `prazos.csv` e `conferencias/AAAA-MM-DD.md`.
- `../dupla-conferencia/assets/modelo-do-registro.md`: o formato do registro de conferências que o script lê.
