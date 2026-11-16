---
name: rotinas
description: >-
  Rotinas programadas do curso Marketing Jurídico com Claude (RPC Educação). Liga, ajusta, pausa e lista
  as rotinas que trabalham sozinhas no marketing do advogado (Informativo da manhã, Pauta da semana,
  Ilha de edição, Conferência da fila, Balanço da semana, Newsletter, Revisão trimestral, Vigia OAB) e
  administra a caixa de aprovação, onde tudo o que as rotinas produzem espera o "aprovo" dele. Use
  quando o advogado disser "configura minhas rotinas", "liga a rotina de...", "pausa...", "quais rotinas
  eu tenho", "o que tem para eu aprovar", "aprovo o item...", "ajusta o item...", "descarta..." ou
  quando uma tarefa agendada pedir para executar um arquivo de rotinas/.
---

# Rotinas programadas

As rotinas fazem o trabalho de bastidor nos dias e horários que o advogado escolher. Ele configura uma vez e, a partir daí, só aprova. **Nenhuma rotina publica, agenda, envia mensagem ou altera a base sozinha.** Tudo o que elas produzem entra na caixa de aprovação.

O catálogo completo, com o que cada rotina faz e o modelo de cada uma, está em `references/catalogo.md`.

## 1. Configurar (Fase 7 do Rito, ou a qualquer momento)

1. Leia `andamento.md` e a base para saber o que já existe (identidade fixa e modelos de carrossel, agendador, plugin de vídeo e favoritos de edição).
2. Mostre o catálogo em linguagem simples, numa tabela curta: nome, o que faz por ele, quando roda e o que ele aprova. Marque como "recomendada" o conjunto inicial: Informativo da manhã, Pauta da semana, Conferência da fila e Balanço da semana. As outras ele liga se quiser.
3. **Um bloco de perguntas numerado:** quais rotinas ligar, os horários (sugira os do catálogo) e quantas peças por semana a Pauta da semana deve preparar (padrão: o número da base).
4. Para cada rotina escolhida:
   - gere o arquivo `rotinas/<nome>.md` na pasta do advogado, a partir do modelo do catálogo, com todos os campos preenchidos e caminhos completos;
   - crie a tarefa agendada com o pedido "leia e execute o arquivo [caminho completo]/rotinas/<nome>.md", na frequência e no horário escolhidos;
   - registre no `andamento.md`, seção "Rotinas": nome, frequência, horário, data de criação.
5. Mostre a lista de tarefas criadas e explique o combinado: "as rotinas trabalham, você aprova. Para ver o que está esperando, me pergunte 'o que tem para eu aprovar?'."

**Sem a ferramenta de tarefas agendadas na sessão:** gere os arquivos mesmo assim, ensine a criar as tarefas no aplicativo do Claude (em até 3 passos, com o pedido acima) e lembre que cada rotina também roda sob demanda ("roda a pauta da semana").

**Funcionamento:** as tarefas agendadas rodam no computador do advogado, então dependem dele ligado e do aplicativo do Claude disponível no horário. Se o computador estiver desligado, a rotina roda na próxima oportunidade ou ele pede manualmente. [VERIFICAR o comportamento exato das tarefas agendadas no aplicativo antes da imersão.]

## 2. A caixa de aprovação

Pasta `aprovacoes/` na pasta do advogado. Cada item é um arquivo `AAAA-MM-DD-tipo-tema.md` com: tipo (minuta, pacote pronto, prancha do vídeo, vídeo editado, newsletter, proposta de base, alerta), o que foi produzido, o parecer da Trava OAB, a rotina que gerou e o status (`aguardando`, `aprovado`, `ajustar`, `descartado`, `concluido`). O painel mostra a contagem em "Aguardando você".

**"O que tem para eu aprovar?":** liste os itens `aguardando` do mais antigo para o mais novo, numerados, com uma linha cada e o tipo. Mostre o conteúdo do item que ele abrir.

**O que acontece depois de cada decisão:**

| Item | "Aprovo" leva a | Próxima aprovação |
|---|---|---|
| Texto (da Pauta da semana) | A `linha-editorial` continua da estação 3: arte do carrossel até a prévia (sem salvar no Canva), que volta para a caixa | Prévia da arte |
| Prévia da arte | A arte é salva no Canva e exportada; a `linha-editorial` faz as versões e o vídeo editado, se houver; tudo vira um "pacote pronto" | Pacote pronto |
| Pacote pronto | Protocolo agenda nos horários mostrados no preview do item | Nenhuma (este "aprovo" é o "sim" da publicação) |
| Prancha do vídeo | O advogado abre a prancha, escolhe e cola as escolhas na conversa; o vídeo é montado e volta com a Mesa como "vídeo editado" | Vídeo editado |
| Vídeo editado | Entra no pacote da rodada dele | Pacote pronto |
| Newsletter | Fica pronta para ele enviar na ferramenta de e-mail dele | Nenhuma |
| Proposta de base | O arquivo da base é atualizado | Nenhuma |
| Alerta (fila vazia, mudança na OAB) | Executa a ação proposta no alerta | Conforme a ação |

- **"Ajusta o item N: ..."**: refaça só o necessário, rode a trava de novo e devolva o item como `aguardando`.
- **"Descarta o item N"**: marque `descartado`. Se for pauta, ela volta para `pautas.md` como usada.
- **Aprovação em bloco** ("aprovo todos os pacotes"): só para itens que ele já viu nesta conversa. Antes de executar, repita a lista do que será agendado (rede, dia e hora) e peça a confirmação final. Publicar exige ver o preview.

Item aprovado e executado vira `concluido` e atualiza o `registro-de-pecas.md`.

## 3. Ajustar, pausar, listar

- **"Quais rotinas eu tenho"**: tabela com nome, quando roda e a última execução (do `andamento.md`).
- **"Muda o horário de..."** ou **"pausa..."**: altere ou pause a tarefa agendada e atualize o `andamento.md`.
- **"Desliga..."**: remova a tarefa agendada (o arquivo em `rotinas/` fica, para religar depois).

## 4. Regras que valem para toda rotina

- Nunca publica, agenda, envia ou apaga nada; nunca altera a base sem aprovação.
- Toda peça produzida passa pela `trava-oab` antes de entrar na caixa.
- Nunca duplica: antes de produzir, confere a caixa e o registro.
- Falhou (conector fora, fonte fora do ar)? Registra no item de alerta o que houve e segue com o resto. Nunca falha em silêncio.
- Termina sempre com um resumo de até 5 linhas: o que produziu, e o que está aguardando aprovação.
