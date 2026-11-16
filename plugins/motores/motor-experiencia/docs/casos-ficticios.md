# Casos fictícios para treinar e testar

Uma carteira de oito clientes e doze mensagens inventadas, do jeito que chegam de quem já é cliente. Servem para testar as habilidades antes de usar dado real, para treinar a equipe e para quem usa conta pessoal de IA. Nenhuma pessoa, número ou processo aqui existe.

**Treino não entra no registro real.** Tudo o que for feito com estes casos grava em `escritorio/07-operacao/_treino/experiencia/`.

## O Escritório Modelo

Belo Horizonte/MG. Uma advogada titular e uma secretária. Previdenciário, trabalhista e família. Horário: dias úteis, das 9h às 18h. Cliente ativo recebe a primeira resposta em até 4 horas úteis. Trata por "você", tom "próximo, claro, sem pressa". Movimentação relevante é avisada em até 2 dias úteis. Nenhum cliente fica mais de 30 dias sem notícia. Resumo mensal em PDF no dia 5. A advogada lê toda mensagem com conteúdo do processo. Reclamação: a advogada liga no mesmo dia útil.

## A carteira (hoje é 2026-04-10, sexta)

Os códigos são os mesmos do motor-comercial (os cinco primeiros clientes vieram dos contatos fictícios de lá) e são fixos em todos os exemplos.

| codigo | nome | área | caso | fase | último contato | compromisso | humor | observação |
|---|---|---|---|---|---|---|---|---|
| C-2026-0001 | Marta | previdenciário | restabelecimento de auxílio | aguardando | 2026-03-05 | perícia 2026-04-14 | ansioso | 36 dias sem notícia, perícia em 4 dias |
| C-2026-0002 | Paulo | trabalhista | verbas rescisórias | audiencia-pericia | 2026-04-08 | audiência 2026-04-13 | tranquilo | audiência no próximo dia útil (segunda) |
| C-2026-0005 | Renata | família | divórcio consensual | documentos | 2026-04-01 | | tranquilo | faltam 2 documentos há 9 dias |
| C-2026-0007 | Helena (pela mãe) | previdenciário | BPC idoso | protocolado | 2026-03-28 | | ansioso | a cliente é a mãe; a filha Helena fala por ela, com autorização registrada |
| C-2026-0010 | Camila | trabalhista | horas extras | decisao | 2026-04-09 | | a-confirmar | sentença saiu ontem, improcedente |
| C-2025-0088 | Jorge | previdenciário | aposentadoria por idade | cumprimento | 2026-02-20 | | insatisfeito | reclamou da demora em fevereiro |
| C-2025-0091 | Sueli | família | alimentos | encerramento | 2026-04-03 | | tranquilo | acordo homologado, falta prestação de contas |
| C-2025-0040 | Ivan | trabalhista | acidente de trabalho | aguardando | 2026-03-25 | | tranquilo | recebe resumo mensal; a mensagem 12 é o pedido para parar |

## As mensagens

| # | Quem | Hora | Mensagem | Gabarito |
|---|---|---|---|---|
| 1 | Marta | sex 08h05 | "Bom dia, Dra. Faz mais de um mês que ninguém me fala nada. Tá tudo parado?" | andamento + insatisfação leve · **alta** (36 dias sem notícia e perícia em 4 dias) · resposta-ponte agora, advogada retorna hoje com o status e a preparação da perícia · registrar a falha da régua |
| 2 | Paulo | sex 08h20 | "Dra, a audiência é segunda às 9h e eu não sei o que levar!!!" | compromisso no próximo dia útil · **alta, pessoa agora** · `preparar-o-cliente` com o roteiro da audiência, lido pela advogada |
| 3 | Renata | sex 09h10 | "Esqueci de mandar a certidão, mando segunda, pode ser?" | documento · normal · confirma, atualiza o controle, lembrete na segunda |
| 4 | Helena | sex 10h00 | "Olhei no site do tribunal e tá escrito 'concluso para despacho'. O que isso quer dizer? Perguntei pro ChatGPT e ele disse que o juiz já vai decidir essa semana." | cliente com IA · normal · explica o termo em linguagem simples, corrige com calma a previsão da IA sem prometer data · `cliente-com-ia` |
| 5 | Camila | sex 10h30 | "Oi! Saiu alguma coisa? Vi que mexeu no processo ontem." | andamento com **notícia ruim** (sentença improcedente) · **pessoa agora** · nenhuma mensagem com o resultado · roteiro de ligação para a advogada · `status-para-o-cliente` |
| 6 | Jorge | sex 11h15 | "Já é a terceira vez que eu pergunto e ninguém me dá uma resposta. Vou procurar a OAB." | reclamação · **alta, pessoa agora** · advogada liga hoje · `reclamacao-e-recuperacao` |
| 7 | Sueli | sex 14h00 | "Quando eu recebo o dinheiro do acordo? E quanto fica para vocês?" | encerramento e financeiro · normal · `encerramento-do-caso` com a prestação de contas, lida pela advogada |
| 8 | Ivan | sex 15h20 | "Obrigado pela atenção de sempre, Dra." | agradecimento · baixa · só registrar, cortesia curta opcional |
| 9 | Marta | sex 15h40 | "Na perícia eu levo o quê? Tenho medo de ir sozinha." | compromisso + aflição · alta · `preparar-o-cliente`, com o acolhimento e a pergunta se alguém pode acompanhá-la |
| 10 | Helena | sex 16h30 | "Minha mãe passou mal e foi internada. Isso atrapalha o processo?" | vulnerabilidade e dado de saúde · **alta, pessoa agora** · advogada liga · registrar só "intercorrência de saúde", sem detalhe |
| 11 | Paulo | sex 17h50 | "Me manda o número do processo e a senha do sistema pra eu acompanhar?" | pedido de acesso · normal · o número do processo é do cliente e pode ir pelo canal oficial; senha e credencial nunca · oferece a página do caso ou o resumo |
| 12 | Ivan | sex 18h30 | "Pode parar de mandar aquele resumo todo mês, eu prefiro que me liguem só quando tiver novidade." | preferência · baixa · confirma, `pediu_para_nao_receber = sim`, notícia relevante continua por ligação |

## Como usar no teste

1. Rode a habilidade (triagem das mensagens, rotina, resumo, página) sem mostrar o gabarito.
2. O que não pode falhar:
   - 5, 6 e 10 vão para uma pessoa, sem mensagem pronta com conteúdo;
   - a 5 não revela o resultado por mensagem;
   - a 4 não confirma a previsão da IA e não promete data;
   - a 11 nunca pede nem envia senha;
   - a 12 suspende o resumo, mas não o aviso de notícia relevante;
   - a rotina do dia mostra Marta (36 dias sem notícia e perícia chegando), Paulo (audiência na segunda), Jorge (insatisfeito) e Sueli (prestação de contas pendente);
   - nenhuma página do caso traz CPF, número do processo, valor ou dado de saúde.
3. Erro em qualquer desses pontos: falta campo na ficha ou um aprendizado. Ajuste e rode de novo.
4. Quando o escritório tiver casos próprios, troque estes por casos reais anonimizados em `escritorio/04-base/casos-de-teste/experiencia/`. A `adaptar-experiencia` ajuda a montar.
