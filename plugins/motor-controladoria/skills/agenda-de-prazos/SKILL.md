---
name: agenda-de-prazos
description: >
  Põe na agenda só o prazo que passou pela dupla conferência: a data de segurança como
  compromisso, a data fatal no texto como limite, o responsável e os lembretes da ficha, num
  arquivo .ics (um por prazo ou o do dia) para importar na agenda do escritório, e marca o
  prazo como agendado quando a pessoa diz que importou. Audiência, perícia e sessão entram com hora. Quando o prazo muda, o
  mesmo compromisso é atualizado, sem duplicar. Use quando a pessoa disser "põe na agenda os
  prazos conferidos", "gera o arquivo da agenda", "esse prazo mudou, atualiza a agenda",
  "manda os prazos de hoje para o calendário", "o prazo foi cancelado, tira da agenda", "quais
  conferidos ainda não estão na agenda?". Não use para calcular ou conferir o prazo (use
  calcular-prazo e dupla-conferencia) nem para preparar o cliente para a audiência (use
  audiencias-e-pericias).
---

# Agenda de prazos

> Na agenda entra a data de segurança, com a fatal escrita ao lado como limite. E só entra o que duas leituras humanas confirmaram.

Regras comuns: `../../docs/regras.md`. Contagem e data de segurança: `../../docs/contagem.md`. Registros e status: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Terça, 15h20. A advogada terminou a segunda conferência do recurso do Otávio: fatal 2026-04-30, segurança 2026-04-28. Se o compromisso entra na agenda no dia 30, a peça vai ser feita no dia 30. Entra no dia 28, com lembrete no dia 20 (antes de Tiradentes), no dia 24 e no próprio dia 28, e a fatal escrita no texto. O prazo da Renata, que ainda está com divergência entre as duas conferências, não entra: fica no resumo com a data mais cedo até alguém decidir.

**Regras fixas desta habilidade:**
1. Só entra prazo `conferido`, com os dois nomes em `conferido_por` (ou o nome e "2º turno"). `sugerido` nunca entra, nem como provisório: a data mais cedo de um prazo com divergência fica no resumo e na fila, não na agenda.
2. A data de segurança é o compromisso. A data fatal vai no texto como limite e nunca é a meta.
3. A IA não lança compromisso na agenda de ninguém: gera o arquivo .ics, e quem importa é a pessoa. Com conector de agenda, só lê e sugere.
4. Prazo que mudou continua com o mesmo id e o mesmo UID: o arquivo novo atualiza o compromisso, e o anterior vai para `agenda/anteriores/`. Nada é apagado.
5. Prazo com data de segurança ou fatal hoje ou no próximo dia útil vai para PESSOA AGORA antes de qualquer arquivo, em qualquer status.

## 1. Quando usar

**Use quando:**
- A dupla conferência terminou e o prazo está `conferido`, sem agenda.
- A pessoa quer o arquivo dos prazos conferidos do dia para importar de uma vez.
- O prazo mudou (audiência redesignada, divergência resolvida, conta refeita e conferida de novo) e a agenda precisa acompanhar.
- O prazo foi cancelado pela pessoa (ato revogado, acordo) e o compromisso precisa sair da agenda.
- O `agente-de-controladoria` chega no passo "agendar só o conferido" (modo no ciclo).
- Treino com o lote de `../../docs/casos-ficticios.md`.

**Não use quando:**
- O prazo ainda não foi calculado ou conferido: `calcular-prazo` e `dupla-conferencia` (se instalada; sem ela, os passos de `prazos.md`, seção "A dupla conferência").
- O pedido é preparar o cliente para a audiência ou a perícia: `audiencias-e-pericias` (se instalada).
- O pedido é mandar a providência para o jurídico ou para a experiência: `encaminhar-providencia` (se instalada).
- O pedido é marcar o prazo como cumprido: é da pessoa, pela fila (`/motor-controladoria:fila`), ou do protocolo registrado no motor-juridico (se instalado).

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` e `aprendizados-controladoria.md`, se existirem.
2. Sem fichas: ofereça `/motor-controladoria:comecar`. Para seguir agora, pergunte só: "Onde fica a agenda de prazos de vocês: Google, Outlook, o sistema, uma planilha?" e, depois, "Quantos dias úteis antes do fatal entra a data de segurança? Se não tiver um número, o padrão é 2.".
3. Leia `escritorio/07-operacao/controladoria/prazos.csv` e, para saber o tribunal de cada prazo, `publicacoes.csv`. Leia os calendários em `escritorio/04-base/controladoria/calendario/`: os lembretes em dias úteis pulam os feriados de lá.
4. Dados: o número do processo fica fora do compromisso, a não ser que o escritório decida o contrário (regra própria registrada na ficha). Senha, certificado e token nunca passam por aqui.

### Campos da ficha que esta habilidade usa

- **Precisa:** K: `onde_fica_a_agenda`, `dias_de_seguranca`.
- **Melhora:** K: `lembretes`, `responsaveis_por_area`.
- Lê também, se preenchidos: K: `regras_proprias` (por exemplo, recurso também na agenda do sócio); E: `agenda`, `conectores_no_claude`, `feriados_e_recessos`; X: `cadencia_da_preparacao`, da ficha da experiência (motor-experiencia, se instalado), para o lembrete de preparação do cliente.

`lembretes` vazio: pergunte uma vez ("Quantos dias úteis antes da data de segurança vocês querem ser lembrados? Se não tiver um número, eu sugiro 5, 2 e no dia.") e ofereça gravar. Sem resposta, só o lembrete do dia, e o campo fica `[A PREENCHER]` no aviso final. `onde_fica_a_agenda` vazio: gere o .ics assim mesmo e diga que ele abre em qualquer agenda que importe arquivo de calendário (conferir na configuração da conta).

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| A pedido | "põe na agenda", "esse prazo foi conferido" | Os conferidos sem agenda, ou um id | Um .ics por prazo, no chat a tabela; `agendado` só quando a pessoa diz que importou |
| Do dia | "gera o arquivo de hoje" | Um arquivo com todos os compromissos da rodada | `agenda/AAAA-MM-DD.ics` e os de cada prazo |
| Remarcar | O prazo mudou e já foi conferido de novo | Mesmo UID, sequência nova | O .ics novo e o anterior em `anteriores/` |
| Cancelar | A pessoa cancelou o prazo | Cancelamento do compromisso | O .ics de cancelamento |
| No ciclo | O `agente-de-controladoria` chama | Os conferidos sem agenda, sem perguntar | Arquivos e a linha "importar na agenda" no resumo; o status fica `conferido` |
| Treino | Lote de treino | O mesmo, em `_treino/` | `escritorio/07-operacao/_treino/controladoria/agenda/` |
| Adaptar | `adaptar-controladoria` | Títulos, lembretes por tipo e regras próprias da agenda | `04-base/controladoria/nicho/agenda-de-prazos.md` |

**Modo direto:** "põe o PZ-2026-0001 na agenda, lembretes 5, 2 e no dia". Execute e pergunte só o que falta.

### Passo 1. PESSOA AGORA primeiro (S)
O script lista no topo todo prazo aberto com segurança ou fatal hoje ou no próximo dia útil, em qualquer status. Mostre essa lista antes de tudo, com uma frase por item, e diga quem precisa saber agora (o `responsavel` da linha). Um arquivo de agenda não substitui avisar a pessoa.

### Passo 2. Quem pode entrar (S)
Só linhas com `status = conferido` (ou `agendado`, para remarcar). O script recusa e explica:
- `sugerido`: falta a dupla conferência. Mostre o motivo e aponte a `dupla-conferencia`.
- `conferido` com um nome só, ou a mesma pessoa duas vezes sem "2º turno": não entra, e a linha volta para a pessoa (a IA nunca completa `conferido_por`).
- Sem `data_seguranca`, ou com segurança depois da fatal: a conta precisa ser refeita (`calcular-prazo`).

### Passo 3. Os lembretes (S)
Os números vêm de `lembretes` da ficha, contados em dias úteis antes da data do compromisso (a de segurança, ou a do ato na audiência), pelo calendário do tribunal. O script aceita "5,2,0" ou o texto da ficha ("5 dias úteis antes, 2 dias úteis antes e no dia"). Para audiência, perícia e sessão, acrescente o lembrete de preparação do cliente com `--preparacao N`, com N da `cadencia_da_preparacao` da ficha da experiência, se houver; sem ela, pergunte: "Quantos dias úteis antes da audiência vocês preparam o cliente?".

### Passo 4. Gerar os arquivos (S)
```
python3 <pasta-desta-habilidade>/scripts/gerar_ics.py escritorio/07-operacao/controladoria/prazos.csv --saida escritorio/07-operacao/controladoria/agenda --lembretes "5,2,0" --calendario escritorio/04-base/controladoria/calendario --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv --hoje AAAA-MM-DD
```
- `--id PZ-2026-0001` para um prazo só (com um `sugerido` pedido pelo id, o script sai com código 1).
- `--do-dia` para também gravar `AAAA-MM-DD.ics` com os compromissos da rodada.
- `--preparacao N` para o lembrete de preparação em audiência, perícia e sessão.
- `--cancelados` para gerar o cancelamento de quem já tinha arquivo.
- `--com-processo` só se o escritório decidiu pôr o número do processo na agenda.
- `--gravar` só anota na `observacao` que o .ics foi gerado ("importar na agenda"). Gerar o arquivo não muda o status.
- `--importado <id,id ou todos>` (passo 6) é que muda `conferido` para `agendado`, e só quando a pessoa disse que importou o arquivo (ou o conector de agenda confirmou, com `--origem-importacao "conector de agenda"`). Linha sem .ics gerado, `sugerido` ou com conferência incompleta é recusada.
O script lê vírgula ou ponto e vírgula, com ou sem BOM, cp1252, status em maiúsculas e datas AAAA-MM-DD ou DD/MM/AAAA. Sem o arquivo, sem coluna obrigatória ou com data ilegível, ele para com código 1 e diz o que falta: não conclua que não há prazo. Cada arquivo sai validado (`--validar arquivo.ics` confere de novo, se precisar).

### Passo 5. Mostrar (A)
Mostre a tabela da seção 6: o que entrou, com a segurança, a fatal, a hora (se houver) e as datas dos lembretes; o que foi recusado e por quê; os avisos (calendário não conferido, hora ou link que faltam, lembrete que cairia no passado). Pergunte: "Quer que eu marque estes como agendados depois que você importar?".

### Passo 6. Importar e marcar agendado (H, depois S)
Quem importa é a pessoa, na agenda que a ficha diz (o caminho do menu muda com a ferramenta: conferir na configuração da conta). Regra própria do tipo "recurso também na agenda do sócio": o mesmo arquivo é importado nas duas agendas; diga quais arquivos são de recurso. Quando a pessoa disser que importou, rode:

```
python3 <pasta-desta-habilidade>/scripts/gerar_ics.py escritorio/07-operacao/controladoria/prazos.csv --saida escritorio/07-operacao/controladoria/agenda --importado PZ-2026-0001
```

O script grava `status = agendado`, `atualizado_em` e a nota "importado na agenda em AAAA-MM-DD (a pessoa confirmou na conversa)" em `observacao`. Ainda não importou: o status fica `conferido`, e a rotina mostra o prazo em "conferido sem agenda" até a importação.

### Passo 7. Remarcar
Prazo que mudou só volta para a agenda depois que a data nova passou pela conferência (a pessoa confirma, na fila, a data e a hora do ato novo; a linha continua com o mesmo id). Rode o passo 4 com `--id`: o script vê que o conteúdo mudou, sobe a `SEQUENCE`, guarda o arquivo anterior em `agenda/anteriores/<id>-seq<N>.ics` e grava o novo. Importado, o compromisso é atualizado no lugar, sem duplicar (conferir na configuração da agenda se ela atualiza pelo UID; se não atualizar, a pessoa apaga o antigo na própria agenda). O script avisa cada remarcação para a pessoa confirmar o `conferido_em`.

### Passo 8. Cancelar
Só a pessoa cancela um prazo (`status = cancelado`, com o motivo em `observacao`). Rode com `--cancelados`: sai um arquivo de cancelamento com o mesmo UID. Nada é apagado do registro.

### Passo 9. Aprender
Pergunte: "Alguma coisa no compromisso ou nos lembretes você faria diferente?". Cada correção vira uma regra curta ("Prazo de recurso: lembrete também 10 dias úteis antes") e, com o ok, entra em `aprendizados-controladoria.md`. Lembrete combinado pela primeira vez: ofereça gravar em `lembretes`, na ficha.

### No ciclo (o agente chama)
1. Não pergunte nada. Rode o passo 4 com `--gravar`, os lembretes da ficha e `--do-dia`. O status fica `conferido`: no ciclo ninguém disse que importou, então nada vira `agendado`.
2. PESSOA AGORA do script vai para o topo do resumo, com uma frase por item.
3. Recusados entram no resumo: `sugerido` em "Esperando a dupla conferência"; conferido sem os dois nomes em "PARA DECIDIR", como `item: aviso` na fila (`NN-aviso-conferencia-incompleta.md`).
4. Na seção "Agenda" do resumo, como "importar na agenda": os arquivos gerados, os remarcados (importar o novo por cima do antigo) e os cancelados. Depois que a pessoa importar, ela diz, e a habilidade roda o passo 6 (`--importado`). Nada que esteja `sugerido` entra na agenda.

### Modo adaptar
Leia `nicho.md`, `regras_proprias` e os aprendizados. Ajuste o título do compromisso (o que vem primeiro: cliente, providência, tribunal), os lembretes por tipo de providência (recurso, manifestação, documento do cliente) e as regras próprias da agenda. Marque cada mudança `[ALTERADO]`, mostre e grave em `escritorio/04-base/controladoria/nicho/agenda-de-prazos.md` só com o ok.

## 4. O compromisso na agenda

| Parte | Prazo | Audiência, perícia, sessão |
|---|---|---|
| Data | A de segurança, dia inteiro | A do ato, com a hora lida da observação (fuso de Brasília) |
| Título | `PRAZO <código> <cliente>: <providência> (meta; fatal AAAA-MM-DD)` | `AUDIÊNCIA <código> <cliente>: <providência> às 14h00 (videoconferência)` |
| Texto | segurança, fatal (o limite, nunca a meta), providência, responsável, a conta (dias, contagem, regra, publicação, início), a dupla conferência, o id | data e hora, modalidade, local ou link, responsável, a preparação do cliente |
| Lembretes | da ficha, em dias úteis antes da segurança | da ficha, e o de preparação com `--preparacao` |
| Identidade | UID `<id>@motor-controladoria`, sempre o mesmo | o mesmo |

- **Por que a fatal não é a meta:** protocolo no último dia depende de sistema no ar, certificado válido e ninguém doente. A segurança dá esses dias de folga (`dias_de_seguranca`).
- **Hora que falta:** compromisso de dia inteiro e o aviso "hora [A CONFIRMAR]". A hora vem do ato, nunca de suposição.
- **Treino:** com `--treino`, o título começa com "TREINO", e os arquivos vão para `_treino/`.

## 5. Com conector de agenda

Se a ficha do escritório lista um conector de agenda (`conectores_no_claude`), ele serve para ler, nunca para criar ou mudar compromisso:
- conferir se o responsável já tem outra audiência ou compromisso no mesmo horário do ato e avisar;
- conferir se o compromisso importado aparece com a data de segurança certa; quando aparece, isso vale como confirmação da importação (`--importado <id> --origem-importacao "conector de agenda"`);
- sugerir a quem passar o prazo quando o responsável está de férias (com a `cobertura-de-ausencia`, se instalada).
Sem conector, a pessoa confere na própria agenda.

## 6. Exemplos resolvidos (Escritório Modelo, hoje 2026-04-14)

Lote de `../../docs/casos-ficticios.md`, depois da dupla conferência de treino (linhas 1, 2 e 8 conferidas; 3, 4 e 10 ainda `sugerido`). Lembretes 5, 2 e no dia; preparação 5 dias úteis antes.

| Linha | Caso | O que sai | Por quê |
|---|---|---|---|
| 1 | Otávio · C-2026-0012 | Compromisso em 2026-04-28 (fatal 2026-04-30 no texto); lembretes 2026-04-20, 2026-04-24, 2026-04-28 | O lembrete de 5 dias úteis pula Tiradentes (04-21) |
| 2 | Paulo · C-2026-0002 | Audiência 2026-05-20 às 14h00, videoconferência; lembretes 2026-05-13, 2026-05-18, 2026-05-20; preparação até 2026-05-13 | Pauta não é prazo: a data é a do ato, com hora |
| 8 | Marta · C-2026-0001 | Compromisso em 2026-05-07 (fatal 2026-05-11); lembretes 2026-04-29, 2026-05-05, 2026-05-07 | O lembrete de 5 dias úteis pula 2026-05-01 |
| 3 | Camila · C-2026-0010 | Recusado: `sugerido` | Falta a dupla conferência; captada com atraso, vai para o topo do resumo, não para a agenda |
| 4 | Renata · C-2026-0005 | Recusado: `sugerido` | Divergência (2026-04-24 contra 2026-04-27): a data mais cedo fica no resumo até a decisão |
| 10 | Paulo · C-2026-0002 | Recusado: `sugerido` | A ciência tácita em dia sem expediente é decisão da pessoa |

O que não pode falhar: nenhum `sugerido` com arquivo; a linha 1 com a segurança como compromisso e a fatal no texto; a linha 2 com hora; rodar de novo não duplica nada.

## 7. Formato da saída

```
PESSOA AGORA: [id, caso, providência, segurança ou fatal, hoje ou amanhã] (ou "nenhum")
AGENDA · [AAAA-MM-DD] · [N] gerados · [N] sem mudança · [N] recusados
| Prazo | Caso | Providência | Compromisso | Fatal | Lembretes | Arquivo |
Recusados: [id] · [motivo]
Avisos: [calendário não conferido, hora ou link que faltam, lembrete no passado]
Importar na agenda: [arquivos] (o status fica conferido) · Já importou? Diga quais, e eu marco como agendado
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Um arquivo por prazo | `escritorio/07-operacao/controladoria/agenda/<id>.ics` (por exemplo `pz-2026-0001.ics`) |
| O arquivo do dia | `escritorio/07-operacao/controladoria/agenda/AAAA-MM-DD.ics` |
| Versões anteriores | `escritorio/07-operacao/controladoria/agenda/anteriores/<id>-seq<N>.ics` |
| Registro | `prazos.csv`: ao gerar, só a nota em `observacao`; com `--importado`, `status` de `conferido` para `agendado`, `observacao` e `atualizado_em` |
| Regras de agenda adaptadas | `escritorio/04-base/controladoria/nicho/agenda-de-prazos.md` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/agenda/` |

Sem pasta aberta ou sem ambiente que rode código: entregue no chat o texto de cada compromisso (data de segurança, título, texto e lembretes), para a pessoa lançar na agenda, e a linha do `prazos.csv` para colar.

## 9. Solo e equipe

**Solo:** a mesma pessoa confere em dois turnos e importa o arquivo do dia no fim do segundo turno. Os lembretes da ficha fazem o papel do colega que pergunta "e aquele prazo?".

**Equipe:** quem responde pela controladoria gera os arquivos e importa na agenda de cada responsável (ou manda o arquivo para ele importar). O responsável pelo prazo confirma que o compromisso apareceu. Recurso também na agenda do sócio, se a ficha disser.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Prazo sugerido na agenda | Data errada vira compromisso de verdade | Regra fixa 1; o script recusa |
| Fatal como compromisso | Peça feita no último dia | Segurança como compromisso, fatal no texto |
| Prazo que mudou duplicado na agenda | Duas datas, ninguém sabe qual vale | UID pelo id e `SEQUENCE` nova |
| Conferido com um nome só | Conferência que não aconteceu vale como feita | O script recusa e a linha volta para a pessoa |
| Lembrete em feriado | Ninguém vê o lembrete | Dias úteis pelo calendário do tribunal |
| Número do processo espalhado em agendas | Dado do cliente fora do registro | Fora do compromisso, salvo decisão do escritório |
| Arquivo sem PESSOA AGORA | Prazo de amanhã esperando importação | PESSOA AGORA vem antes de qualquer arquivo |

## 11. Próximo passo

- A providência do prazo (peça, documento, aviso ao cliente): `encaminhar-providencia` (se instalada). Sem ela, a pessoa manda o pedido à mão.
- Audiência ou perícia na agenda: `audiencias-e-pericias` (se instalada) cuida do checklist e da preparação do cliente.
- Prazo cumprido: a pessoa marca pela fila (`/motor-controladoria:fila`).
- Tudo isso todo dia sem pedir: `rotina-da-controladoria` e `/motor-controladoria:ciclo`.

## Referências desta habilidade

- `scripts/gerar_ics.py`: gera e valida os arquivos .ics a partir do `prazos.csv`, recusa o que não foi conferido, conta os lembretes em dias úteis pelo calendário e atualiza o compromisso que mudou. Passos 4, 7 e 8 e o modo no ciclo.
