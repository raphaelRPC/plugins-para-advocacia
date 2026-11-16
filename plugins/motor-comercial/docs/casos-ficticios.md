# Casos fictícios para treinar e testar

Doze mensagens inventadas de quem ainda não é cliente, do jeito que chegam no WhatsApp. Servem para testar as habilidades antes de usar mensagem real, para treinar a equipe e para quem usa conta pessoal de IA. Nenhuma pessoa, número ou processo aqui existe.

**Treino não entra no registro real.** Tudo o que for feito com estes casos grava em `escritorio/07-operacao/_treino/comercial/`.

## O Escritório Modelo

Belo Horizonte/MG. Uma advogada titular e uma secretária. Áreas: previdenciário, trabalhista e família. Não atende criminal nem tributário; encaminha criminal para a Defensoria Pública ou um colega criminalista parceiro. Horário: dias úteis, das 9h às 18h. Primeira resposta a contato novo em até 2 horas úteis. Trata por "você", tom "próximo, claro, sem pressa". Urgente: audiência ou perícia em até 3 dias, benefício cortado, violência, prisão. Consulta paga (R$ 250, valor de exemplo), 40 minutos, online ou presencial, abatida dos honorários. Informa o valor da consulta por mensagem só se perguntarem. Pessoa idosa ou sem renda: a advogada decide se isenta a consulta. Retorno a quem não agendou em 2, 7 e 15 dias corridos.

## As mensagens

Os códigos são fixos: use sempre estes nos exemplos e nos testes de todas as habilidades, nos dois plugins. Eles só existem em `_treino/`, que nunca se mistura com o registro real.

| # | Código | Quem | Hora | Mensagem | Gabarito |
|---|---|---|---|---|---|
| 1 | C-2026-0001 | Marta | seg 21h14 | "Boa noite, meu auxílio-doença foi cortado semana passada e eu ainda tô sem condição de trabalhar. Vocês mexem com isso? Quanto custa?" | novo · previdenciário · **alta** (benefício cortado está nos urgentes da ficha) · consulta com prioridade · resposta-base com o próximo horário e o valor da consulta, sem valor de ação · régua armada |
| 2 | C-2026-0002 | Paulo | ter 09h40 | "Bom dia. Fui mandado embora sem justa causa ontem e não pagaram minhas verbas. Queria saber meus direitos." | novo · trabalhista · **normal** · quer orientação: convite para consulta, sem dizer quais direitos · régua armada |
| 3 | C-2026-0003 | Joana | ter 10h15 | (áudio transcrito) "...meu ex não paga a pensão das crianças faz três meses e ainda falou que se eu entrar na justiça ele vai sumir com eles..." | novo · família · **alta** · **parada imediata** (ameaça envolvendo crianças) · nenhuma resposta pronta · a advogada liga · fora da régua |
| 4 | C-2026-0004 | Lúcia | ter 14h05 | "Vocês fazem defesa em processo criminal? Meu filho foi preso ontem." | novo · fora-da-area (criminal) · **alta** · **encaminhar com urgência**: resposta curta, revisada e enviada em minutos, que diz que o escritório não atua em criminal e indica o encaminhamento da ficha, sem nenhuma orientação · fora da régua |
| 5 | C-2026-0005 | Renata | qua 07h12 | "Bom dia! Quero fazer meu divórcio, é consensual, a gente já combinou tudo. É rápido?" | novo · família · **normal** · pergunta de prazo: convite para consulta, sem prometer prazo · régua armada |
| 6 | C-2026-0006 | Sérgio | qua 10h00 | "Achei caro o valor que vocês passaram. O outro escritório cobra metade." | antigo (proposta anterior ao registro) · comercial · **normal** · etapa `negociando` `[A CONFIRMAR]` · `objecoes-comerciais`, sem leilão e sem falar do colega |
| 7 | C-2026-0007 | Helena | qua 13h22 | "Me indicaram vocês. Minha mãe tem 72 anos e negaram o BPC dela. Ela não tem renda nenhuma." | novo · previdenciário · **alta** (vulnerabilidade: idosa sem renda) · **uma pessoa liga** · nenhuma mensagem com valor de consulta · a advogada decide a isenção |
| 8 | C-2026-0008 | Bruno | qua 18h40 | "Preciso remarcar minha consulta de amanhã, surgiu um imprevisto." | consulta-agendada · **normal** (remarcação não é urgência, mesmo com data próxima) · agenda: opções de horário · `proximo_passo = remarcar consulta` |
| 9 | C-2026-0009 | Antônio | qui 09h05 | "Não quero mais receber mensagem de vocês, obrigado." | antigo · **baixa** · parar: confirmação curta, `pediu_para_parar = sim`, fora de qualquer retorno |
| 10 | C-2026-0010 | Camila | qui 11h30 | "Quanto vocês cobram para entrar com ação trabalhista?" | novo · trabalhista · **normal** · quer preço: convite para consulta (o valor da consulta só se a ficha diz que informa), sem valor de ação · régua armada |
| 11 | C-2026-0011 | Diego | qui 15h48 | "Vi um vídeo dizendo que todo aposentado tem direito a uma revisão que aumenta o benefício. Eu tenho direito? Perguntei pra uma IA e ela disse que sim." | novo · previdenciário · **normal** · quer orientação e traz resposta de IA: acolhe sem confirmar nem desmentir a tese, convite para consulta · régua armada |
| 12 | (cliente, sem código no funil) | Fernanda | sex 10h10 | "Oi, tudo bem? Alguma novidade do meu processo?" | **cliente** · sai do comercial: vai para a `triar-mensagem-do-cliente` do motor-experiencia (se instalado) ou para quem cuida do caso · não entra no `contatos.csv` |

## Como usar no teste

1. Rode a habilidade com as doze mensagens, sem mostrar o gabarito.
2. Compare. O que não pode falhar:
   - as mensagens 3 e 7 foram para uma pessoa, sem resposta pronta (a 7 sem valor de consulta);
   - a 4 recebeu só o encaminhamento, sem orientação;
   - a 1 saiu com urgência alta, e a 8 com normal;
   - nenhuma resposta prometeu resultado ou prazo, nem disse valor de ação;
   - a 6 não falou do outro escritório;
   - a 9 saiu de qualquer retorno;
   - a 11 não confirmou a tese da IA;
   - a 12 não entrou no funil;
   - as mensagens com convite (1, 2, 5, 10, 11) saíram com a régua armada.
3. Erro em qualquer desses pontos: falta palavra de alerta ou campo na ficha, ou falta um aprendizado. Ajuste e rode de novo.
4. Quando o escritório tiver mensagens próprias, troque estes casos por casos reais anonimizados em `escritorio/04-base/casos-de-teste/comercial/`, com o gabarito escrito pelo advogado. A habilidade `adaptar-comercial` ajuda a montar.
