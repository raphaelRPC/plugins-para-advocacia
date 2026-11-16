# Onde o assistente roda

Três níveis. Cada um só começa quando o anterior rodou sem erro crítico. Pular nível é a forma mais comum de um escritório descobrir o erro pelo cliente.

## Os níveis

| Nível | Como funciona | Quem envia | Exige |
|---|---|---|---|
| **0 · Texto fixo** | A mensagem de fora do horário e a de saudação, iguais para todos, configuradas no WhatsApp Business ou na ferramenta (conferir na configuração da conta). Sem IA. | A ferramenta, sempre o mesmo texto | Texto aprovado na biblioteca. Não precisa do teste desta habilidade |
| **1 · Assistente no Projeto** | Um Projeto no Claude com as instruções. Quem atende cola a primeira mensagem (anonimizada), recebe a resposta, lê e envia pelo número oficial. | Uma pessoa, depois de ler | Portão cumprido e teste do nível 1 aprovado |
| **2 · Assistente na ferramenta** | A ferramenta de atendimento do escritório usa as instruções para responder sozinha a primeira mensagem, no horário combinado. | A ferramenta, sem ninguém ler antes | Nível 1 por [2 semanas, A DEFINIR] sem erro crítico, teste do nível 2 aprovado na própria ferramenta, plano para erro aprovado, conta e contrato da ferramenta conferidos |

O nível 1 já resolve a maior parte do problema de quem escreve às 21h: no dia seguinte, a pessoa da equipe tem a resposta pronta e só confere. O nível 2 resolve o "ninguém respondeu até amanhã", e é ele que pede todo o cuidado.

## O Projeto no Claude (nível 1)

1. Crie um Projeto chamado "Primeira resposta".
2. Cole o bloco entre `=== INÍCIO ===` e `=== FIM ===` nas instruções do Projeto.
3. Não coloque as fichas inteiras nem o registro de contatos no Projeto: as instruções já trazem o que o assistente pode saber, e o resto ele não deve usar.
4. Para cada mensagem: conversa nova, mensagem anonimizada (nome por `[CLIENTE]`, documento por `[DOC]`), hora de chegada. A resposta vem com a linha "PASSAR PARA PESSOA" quando for o caso.
5. Quem envia lê a resposta inteira antes. Se corrigir alguma coisa, anota: a correção vira aprendizado ou caso novo da bateria.
6. Conta profissional ou de equipe, porque a mensagem é real (conferir na configuração da conta).

## A ferramenta de atendimento (nível 2)

O plugin não conecta o Claude ao WhatsApp. O nível 2 depende de uma ferramenta de atendimento que o escritório contrata e que aceite instruções escritas para um assistente de IA. Cada ferramenta funciona de um jeito, e os recursos mudam. Antes de colar as instruções, confira na configuração da ferramenta (e, se preciso, com o suporte dela):

| Pergunta | Por que importa | Se a resposta for não |
|---|---|---|
| Aceita um texto de instruções do tamanho das nossas? | Instrução cortada perde as regras do fim | Encurte as mensagens da seção 6, nunca as seções 4 e 5 |
| Dá para limitar quando o assistente responde (só fora do horário, só no primeiro contato)? | O assistente não pode responder cliente no meio de uma conversa com a advogada | Não ligue no nível 2 |
| Dá para passar a conversa para uma pessoa (etiqueta, fila, aviso)? | A passagem é metade do trabalho do assistente | Não ligue no nível 2 |
| O assistente para de responder quando uma pessoa assume? | Senão ele volta a falar no meio do atendimento humano | Não ligue no nível 2 |
| Existe um jeito de pausar tudo de uma vez? Quem tem acesso? | O plano para erro depende disso | Não ligue no nível 2 |
| Dá para limitar o número de respostas por conversa? | Evita a conversa longa com o robô | Reforce a regra 9 e acompanhe de perto |
| Guarda o histórico das respostas automáticas? | A revisão diária e a auditoria precisam dele | Não ligue no nível 2 |
| Transcreve áudio ou lê imagem? | Define se a mensagem H vale | Mantenha a mensagem H |
| Que modelo de IA usa, onde ficam os dados, o que diz o contrato sobre tratamento de dados? | Mensagem de quem procura advogado tem dado pessoal e, às vezes, sensível | Leve ao responsável pelo tratamento de dados `[CONFERIR]` LGPD (Lei 13.709/2018) |
| Manda mensagem por iniciativa própria (campanha, lembrete)? | O assistente só responde | Deixe desligado para este assistente |
| As regras do WhatsApp para atendimento automático pelo número do escritório estão atendidas? | As regras do aplicativo mudam e podem limitar o uso | Conferir com a ferramenta e nos termos do WhatsApp |

Cada "não" na coluna da direita que diz "não ligue" é um bloqueio: fica no nível 1 até a ferramenta resolver.

Teste na ferramenta: a bateria roda de novo lá, com um número de teste, porque o modelo e a forma de juntar as instruções podem ser diferentes. Resultado do Projeto não aprova a ferramenta.

## Publicidade e ética

O que o assistente escreve é comunicação do escritório. O Código de Ética e Disciplina da OAB e o Provimento 205/2021 do CFOAB valem para ele como para uma postagem: sem promessa, sem tom de oferta, sem orientação a quem não é cliente, sem se passar por advogado. Na dúvida sobre uma mensagem, o advogado lê o provimento antes de ligar `[CONFERIR]`.
