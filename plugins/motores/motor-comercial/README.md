# motor-comercial

Plugin do Claude que coloca o comercial do escritório de advocacia para rodar, do primeiro contato ao contrato assinado. Cada mensagem é triada e registrada, e o convite para a consulta sai no tom do escritório. A consulta é preparada e registrada em ata. A proposta e o contrato saem prontos para revisar. O retorno a quem sumiu vem na hora certa, sem insistência. E um agente roda o ciclo do dia e deixa tudo numa fila para uma pessoa aprovar.

As habilidades vêm prontas no método e vazias no conteúdo. Elas sabem triar, convidar, conduzir a consulta e montar a proposta. O que elas não sabem é como o seu escritório funciona: o nicho, o tom, o que é urgente, quanto e como vocês cobram, as rotinas da casa. Isso vai em duas **fichas**, uma do escritório e uma comercial, que você preenche uma vez e melhora com o uso. Toda correção que você fizer pode virar um **aprendizado**, e as habilidades passam a seguir. A habilidade `adaptar-comercial` ajusta o plugin inteiro ao seu nicho e transforma rotinas próprias do escritório em habilidades novas.

Quem já é cliente fica com o plugin irmão, o `motor-experiencia`, que cuida do suporte ao cliente do contrato ao encerramento. Os dois usam a mesma pasta e o mesmo código de cliente, e a habilidade `passagem-para-o-caso` entrega o cliente de um para o outro.

## Como começar

```
/motor-comercial:comecar
```

Em cerca de 15 minutos e até 8 perguntas: as fichas mínimas e a triagem de doze mensagens de treino funcionando no jeito do escritório. Depois:

```
/motor-comercial:ciclo     roda o ciclo do dia: o agente lê o que chegou, tria, rascunha e deixa a fila
/motor-comercial:fila      aprova, ajusta ou descarta os rascunhos, um por um
/motor-comercial:status    o funil agora: sem resposta, consultas e retornos do dia, propostas abertas
/motor-comercial:ficha     completa as fichas, seção por seção
```

## As habilidades

| Edição | Habilidade | O que faz |
|---|---|---|
| essencial | `triar-contato` | Classifica cada mensagem de quem ainda não é cliente (área, urgência, sinal de alerta), escolhe o caminho, sugere a resposta e registra no funil com o retorno já agendado |
| essencial | `mensagens-comerciais` | A biblioteca de mensagens comerciais no tom do escritório, e a resposta pronta para a mensagem de agora |
| essencial | `roteiro-da-consulta` | O roteiro da consulta inicial por área e o briefing de cada consulta marcada |
| essencial | `proposta-de-honorarios` | A política de honorários do escritório e a proposta de cada caso, em .md e .docx |
| essencial | `rotina-comercial` | O motor: o resumo do dia, a tarefa agendada que roda o ciclo e o ciclo à mão para quem usa o chat |
| essencial | `adaptar-comercial` | O plugin ajustado ao seu nicho e às suas rotinas, com casos de teste do próprio escritório |
| completo | `qualificar-contato` | Consulta normal, com prioridade, encaminhar ou recusar, e as perguntas antes da consulta |
| completo | `agenda-da-consulta` | Marcar, confirmar, lembrar, remarcar e registrar falta |
| completo | `ata-da-consulta` | A ata, as pendências e a mensagem de resumo depois da consulta |
| completo | `follow-up` | O retorno a quem não agendou, faltou ou não respondeu a proposta |
| completo | `objecoes-comerciais` | Respostas éticas para "está caro", "vou pensar" e as outras objeções |
| completo | `contrato-de-honorarios` | A minuta do contrato a partir da proposta aceita |
| completo | `passagem-para-o-caso` | O que o comercial prometeu e combinou, entregue a quem vai cuidar do caso e do cliente |
| avançado | `painel-do-funil` | O painel do mês: de onde vêm os contatos, quanto converte, por que se perde |
| avançado | `assistente-de-primeira-resposta` | O assistente que responde a primeira mensagem fora do horário, com limites e bateria de teste |
| avançado | `auditar-conversas-comerciais` | A auditoria das conversas comerciais contra as fichas, com ajustes |

Agentes: `agente-comercial` (roda o ciclo do dia) e `revisor-comercial` (confere cada rascunho contra as regras de ética e as fichas antes da fila). Funcionam no Cowork e no Claude Code. No chat com Projeto, a `rotina-comercial` faz o mesmo ciclo, passo a passo.

A edição **essencial** traz 6 habilidades, a **completa** traz 13 e a **avançada** traz 16. As três são o mesmo plugin: para subir de edição, instale o zip novo no lugar do antigo. O que está na pasta `escritorio/` continua valendo.

## Onde fica o que o plugin produz

Na pasta `escritorio/`, dentro da pasta de trabalho:

- `04-base/comum/`: as fichas, o perfil do nicho e os aprendizados;
- `04-base/comercial/`: biblioteca de mensagens, política de honorários, objeções, modelos;
- `07-operacao/comercial/`: o registro de contatos (`contatos.csv`), triagens, consultas, propostas, contratos, passagens, a fila de aprovação e os resumos do dia;
- `07-operacao/_treino/`: tudo o que for feito com casos fictícios, fora dos registros reais.

## Como instalar

- **App do Claude (Cowork e chat):** Personalizar > Plugins > Adicionar > Enviar plugin, com o zip da edição.
- **Uma habilidade sozinha:** Personalizar > Habilidades > + > Criar habilidade > Enviar, com o zip da habilidade. Comandos e agentes só existem no plugin inteiro.
- **Claude Code:** `claude --plugin-dir caminho/do/plugin`.

Os menus podem mudar com as atualizações do Claude: conferir na configuração da conta.

## Cuidados

- Mensagem real de cliente só em conta profissional ou de equipe. Em conta pessoal, use os casos de treino.
- A IA prepara, uma pessoa decide e envia. Nada sai para o cliente sem passar pela fila.
- Segue o Código de Ética e Disciplina da OAB e o Provimento 205/2021 do CFOAB. Por isso não faz promessa de resultado, não orienta juridicamente quem ainda não é cliente, não informa valor de ação por mensagem e não faz captação.
- Quando aparece sinal de violência, ameaça, risco à vida ou prisão, a habilidade para e a conversa vai para uma pessoa.

Criado por Raphael Cardoso. Licença MIT.
