# Checklists de audiência, perícia e sessão

Pontos de partida para o escritório ajustar no modo adaptar. Cada item diz quem faz (S, A ou H, de `../../../docs/regras.md`, seção 5.1). Requisito processual (prazo para rol de testemunhas, para quesitos, para inscrição em sustentação oral, regra do sistema de videoconferência) fica `[CONFERIR]` no ato, no regimento ou na lei, e nunca sai da memória da IA. O número de dias, quando houver, vem do ato ou da tabela do escritório (`regras-de-contagem.md`, "Prazos por ato").

## Para toda audiência, perícia e sessão

| Item | Quem | Observação |
|---|---|---|
| Data, hora e modalidade conferidas no trecho literal do ato | H | Na dupla conferência, como qualquer prazo |
| Local (endereço do fórum, sala, consultório do perito) ou link | S, conferido por H | Sem local ou link no ato: `[A CONFIRMAR]` e pergunta ao responsável |
| Responsável pelo ato e quem acompanha o cliente | H | `responsaveis_por_area` |
| Compromisso na agenda, com lembretes | S | `agenda-de-prazos`, só depois de conferido |
| Aviso para a preparação do cliente | S | `encaminhar-providencia`, aviso de compromisso para a `preparar-o-cliente` (motor-experiencia, se instalado) |
| Conflito na agenda do responsável (duas audiências na mesma hora) | S, decide H | Com conector de agenda, só leitura |
| Prazo anterior ao ato que o próprio ato abre (rol, quesitos, documentos) | S calcula, H confere | Vira linha de prazo própria, pela `calcular-prazo` |

## Audiência

| Item | Quem | Observação |
|---|---|---|
| Tipo de audiência (conciliação, instrução, una, de justificação) | H | Pelo ato; muda o que o cliente precisa levar e se há depoimento |
| Testemunhas: quem, se serão intimadas ou se vêm independentemente de intimação, prazo do rol | H | `[CONFERIR]` no ato e na lei do rito. A IA não prepara testemunha: aviso de data e local, e a conversa é do advogado |
| Depoimento pessoal do cliente e consequência de não comparecer | H | `[CONFERIR]` no ato (por exemplo, "sob pena de confissão") |
| Documentos para levar ou juntar antes | A | Lista do advogado; a experiência pede ao cliente |
| Proposta de acordo: limites que o cliente autorizou | H | Conversa do advogado com o cliente, antes do dia |
| Preposto e carta de preposição (quando o cliente é empresa) | H | `[CONFERIR]` |

## Perícia

| Item | Quem | Observação |
|---|---|---|
| Tipo de perícia (médica, social, técnica no local de trabalho, contábil) | H | Pelo ato |
| Quesitos: prazo e se já foram apresentados | H | `[CONFERIR]` no ato. A IA não escreve quesito aqui; o motor-juridico (se instalado) cuida da peça |
| Assistente técnico: se o escritório indica, quem, prazo | H | `[CONFERIR]` |
| Documentos do cliente para a perícia (exames, laudos, receitas, carteira de trabalho) | A | A experiência pede; documento de saúde só pelo canal oficial |
| Local e horário com o perito, quando o ato diz que o perito vai marcar | S, conferido por H | Data marcada pelo perito vira atualização da mesma linha |
| Acompanhante: se pode entrar na sala | H | `[CONFERIR]` com quem conduz a perícia |

## Sessão de julgamento

| Item | Quem | Observação |
|---|---|---|
| Pauta publicada: data, órgão julgador, se é presencial, virtual ou por vídeo | H | Pelo ato |
| Sustentação oral: se cabe, prazo e forma de inscrição | H | `[CONFERIR]` no regimento do tribunal; o motor-juridico (se instalado) prepara a sustentação |
| Memoriais | H | Decisão do advogado |
| Sessão virtual: prazo para pedir retirada de pauta ou destaque | H | `[CONFERIR]` no regimento |
| Aviso ao cliente | A | O cliente costuma não participar; a experiência avisa a data e conta depois o resultado (notícia ruim por ligação) |

## Por videoconferência

| Item | Quem | Observação |
|---|---|---|
| Link da sala virtual (no ato, nos autos ou enviado pelo juízo) | S, conferido por H | Sem link até a véspera: o responsável procura nos autos ou no juízo |
| Teste do link, da câmera e do áudio com o cliente, antes do dia | A | A experiência combina; quem não tem como entrar sozinho pode vir ao escritório `[CONFERIR]` se o juízo aceita |
| Documento com foto à mão na hora | A | Na orientação da `preparar-o-cliente` |
| Lugar silencioso, sozinho na sala quando for depor | A | `[CONFERIR]` a regra do juízo sobre quem pode estar junto |
| Plano para queda de conexão (telefone do cartório, da vara ou do perito) | H | `[CONFERIR]` no ato ou no juízo |
