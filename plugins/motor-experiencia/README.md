# motor-experiencia

Plugin do Claude para a experiência e o suporte ao cliente do escritório de advocacia, do contrato assinado ao caso encerrado e depois.

O cliente de hoje consulta o processo sozinho no site do tribunal, lê "concluso para despacho" e pergunta a uma IA o que isso quer dizer, muitas vezes antes de perguntar ao advogado. O escritório que chega antes explica, mostra o trabalho que o cliente não vê e avisa antes de ser perguntado. Esse cliente confia mais, reclama menos e indica.

O plugin faz isso rodar. A jornada e a régua de atualização são definidas por tipo de caso. O andamento chega traduzido em linguagem simples, e a notícia ruim vira roteiro de ligação, nunca mensagem. O resumo mensal sai sem esforço. A página do caso é um artefato do Claude, com linha do tempo e próximos passos, que dá para mandar por link ou em PDF. O plugin também ajuda a responder bem a quem chega com a resposta de uma IA, a preparar o cliente para a audiência e a perícia, a tratar uma reclamação, a fazer a prestação de contas e a pesquisa de satisfação. E um agente varre a carteira todo dia e deixa os rascunhos numa fila para uma pessoa aprovar.

As habilidades vêm prontas no método e vazias no conteúdo. O contexto do escritório (quem cuida dos casos, de quanto em quanto tempo o cliente tem notícia, o que nunca vai por mensagem, o nicho, as rotinas) vai em duas **fichas**, uma do escritório e uma da experiência, que melhoram com o uso. A habilidade `adaptar-experiencia` ajusta o plugin ao seu nicho e transforma rotinas próprias do escritório em habilidades novas.

O comercial (do primeiro contato ao contrato) fica com o plugin irmão, o `motor-comercial`. Os dois usam a mesma pasta e o mesmo código de cliente.

## Como começar

```
/motor-experiencia:comecar
```

Em cerca de 15 minutos e até 8 perguntas, você vê as fichas mínimas e o dia de uma carteira de treino: quem precisa de uma pessoa agora, quem está sem notícia além da régua e uma mensagem de andamento traduzida. Depois:

```
/motor-experiencia:ciclo     roda o ciclo do dia na carteira e deixa a fila de aprovação
/motor-experiencia:fila      aprova, ajusta ou descarta os rascunhos, um por um
/motor-experiencia:status    a carteira agora: pessoa agora, sem notícia, compromissos, documentos
/motor-experiencia:ficha     completa as fichas, seção por seção
```

## As habilidades

| Edição | Habilidade | O que faz |
|---|---|---|
| essencial | `jornada-do-cliente` | A jornada e a régua por tipo de caso: o que o escritório diz em cada fase sem ser perguntado |
| essencial | `boas-vindas-do-cliente` | A entrada do cliente: quem cuida, como e quando ele terá notícia, próximos passos |
| essencial | `status-para-o-cliente` | O andamento traduzido em mensagem simples; notícia ruim vira roteiro de ligação |
| essencial | `resumo-mensal-do-caso` | O resumo do mês de cada cliente, em mensagem, documento ou página |
| essencial | `rotina-da-experiencia` | O motor: o retrato do dia da carteira, a tarefa agendada, o ciclo à mão e a importação da carteira atual |
| essencial | `adaptar-experiencia` | O plugin ajustado ao seu nicho e às suas rotinas |
| completo | `triar-mensagem-do-cliente` | A fila das mensagens de clientes: o que é para uma pessoa agora, o que é andamento, documento, compromisso |
| completo | `pagina-do-caso` | A página do caso como artefato do Claude: linha do tempo, o que o escritório fez, próximos passos |
| completo | `cliente-com-ia` | Quando o cliente chega com a resposta de uma IA, e as perguntas do caso respondidas antes de ele pesquisar |
| completo | `checklist-de-documentos` | O que o cliente precisa mandar, onde consegue cada documento e o controle do que chegou |
| completo | `preparar-o-cliente` | Audiência, perícia e reunião: lembrete, o que levar, como vai ser, acolhimento |
| completo | `reclamacao-e-recuperacao` | Uma pessoa assume, escuta, corrige e registra, e a causa vira ajuste |
| completo | `encerramento-do-caso` | A prestação de contas e o fim do caso bem explicado |
| completo | `pesquisa-de-satisfacao` | Três perguntas nos momentos certos e o retorno a quem deu nota baixa |
| avançado | `painel-da-carteira` | O painel interno da carteira: dias sem notícia, compromissos, reclamações, satisfação |
| avançado | `auditar-conversas` | A auditoria das conversas com clientes contra as fichas e a jornada |
| avançado | `relacionamento-depois-do-caso` | O contato depois do caso, sem oferta, e a avaliação dentro das regras da OAB |

Agentes: `agente-de-suporte` (roda o ciclo do dia na carteira) e `revisor-de-suporte` (confere cada rascunho antes da fila). Funcionam no Cowork e no Claude Code. No chat com Projeto, a `rotina-da-experiencia` faz o mesmo ciclo, passo a passo.

A edição **essencial** traz 6 habilidades, a **completa** traz 14 e a **avançada** traz 17. As três são o mesmo plugin: para subir de edição, instale o zip novo no lugar do antigo.

## Onde fica o que o plugin produz

Na pasta `escritorio/`, dentro da pasta de trabalho:

- `04-base/comum/`: as fichas, o perfil do nicho e os aprendizados;
- `04-base/relacionamento-com-o-cliente/`: jornadas, biblioteca de mensagens, glossário do cliente, perguntas do caso;
- `07-operacao/experiencia/`: a carteira (`carteira.csv`), a pasta de cada cliente (histórico, resumos, página, documentos), reclamações, pesquisas, a fila de aprovação e os resumos do dia;
- `07-operacao/_treino/`: tudo o que for feito com casos fictícios.

## Como instalar

- **App do Claude (Cowork e chat):** Personalizar > Plugins > Adicionar > Enviar plugin, com o zip da edição.
- **Uma habilidade sozinha:** Personalizar > Habilidades > + > Criar habilidade > Enviar, com o zip da habilidade. Comandos e agentes só existem no plugin inteiro.
- **Claude Code:** `claude --plugin-dir caminho/do/plugin`.

Os menus podem mudar com as atualizações do Claude: conferir na configuração da conta.

## Cuidados

- Dado de cliente só em conta profissional ou de equipe. Em conta pessoal, use a carteira de treino.
- Mensagem com conteúdo do processo só sai depois que alguém lê. Notícia ruim, mudança de estratégia e proposta de acordo vão por ligação ou reunião.
- A página do caso leva o mínimo: nada de CPF, número do processo, valor da causa, endereço, nome da outra parte ou dado de saúde. Antes de publicar, o plugin mostra o que está nela e pede o ok.
- Senha, código e login do gov.br ou do Meu INSS nunca entram.
- Segue o Código de Ética e Disciplina da OAB e o Provimento 205/2021 do CFOAB.

Criado por Raphael Cardoso. Licença MIT.
