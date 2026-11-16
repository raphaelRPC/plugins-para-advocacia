# motor-controladoria

Plugin do Claude para a controladoria do escritório de advocacia: captar as publicações, ligar cada uma ao caso, contar o prazo pelo calendário de cada tribunal e colocar na agenda só o que uma pessoa conferiu. E levar a providência adiante: a peça para quem redige, o documento para pedir ao cliente, a audiência para a preparação.

Perder prazo é o medo mais antigo da advocacia, e a IA pode ajudar e pode atrapalhar. Ajuda porque lê centenas de publicações sem cansar, não esquece o feriado municipal e faz a conta mostrando cada passo. Atrapalha se alguém confiar na conta sem conferir. Por isso a regra deste plugin é uma só: **a IA capta e calcula, mas não interpreta**. Cada sugestão vem com o trecho literal do ato e a conta à vista, e o prazo só entra na agenda depois da dupla conferência de uma pessoa.

As habilidades vêm prontas no método e vazias no conteúdo. A tabela de regras de contagem vem marcada para conferir e é validada pelo próprio escritório. Os calendários são montados para os tribunais onde vocês atuam. O contexto mora em duas **fichas**, a do escritório e a da controladoria, e cada correção pode virar um **aprendizado**.

## Como começar

```
/motor-controladoria:comecar
```

Em cerca de 15 minutos e 8 perguntas, você tem as fichas mínimas e vê a triagem e a conta trabalhando num lote de dez publicações de treino, cada uma com uma armadilha. Depois:

```
/motor-controladoria:ciclo     capta, tria e calcula o que chegou, e monta a mesa de conferência
/motor-controladoria:fila      a dupla conferência de cada prazo e a decisão de cada providência
/motor-controladoria:status    o que vence hoje, amanhã e na semana, e o que espera conferência
/motor-controladoria:ficha     completa as fichas, seção por seção
```

## As habilidades

| Edição | Habilidade | O que faz |
|---|---|---|
| essencial | `captar-publicacoes` | Busca no DJEN pelas OABs do escritório ou importa a planilha, o e-mail do tribunal e a exportação do sistema. Tira as duplicadas |
| essencial | `triar-publicacoes` | Classifica cada ato e liga ao caso, com o trecho literal que justifica |
| essencial | `calendario-forense` | Feriados, recesso, suspensões e indisponibilidades de cada tribunal no ano, e a validação da tabela de regras |
| essencial | `calcular-prazo` | A conta do prazo, passo a passo, pelo rito e pelo calendário do tribunal |
| essencial | `dupla-conferencia` | Duas leituras do ato e duas contas independentes antes de o prazo valer |
| essencial | `agenda-de-prazos` | Data de segurança, data fatal, responsável e lembretes, com arquivo para a agenda |
| essencial | `encaminhar-providencia` | A publicação conferida vira pedido de peça, tarefa ou aviso ao cliente |
| essencial | `rotina-da-controladoria` | O motor: o resumo do dia, a tarefa agendada e o ciclo à mão |
| essencial | `adaptar-controladoria` | O plugin ajustado aos tribunais, às regras próprias e às rotinas do escritório |
| completo | `leitura-da-decisao` | Sentença, acórdão ou decisão em linguagem clara: o que mudou, o que cabe, o que dizer ao cliente |
| completo | `providencia-sugerida` | O que cada tipo de ato costuma pedir no escritório, como sugestão para quem decide |
| completo | `audiencias-e-pericias` | A pauta, o checklist e a preparação do cliente |
| completo | `carteira-de-processos` | Os processos ativos ligados aos casos, e os parados há tempo demais |
| completo | `paineis-dos-sistemas` | O roteiro diário dos painéis que só uma pessoa abre, e o registro do que ela viu |
| completo | `cobertura-de-ausencia` | Férias e licença: quem assume cada prazo, com a passagem registrada |
| completo | `auditoria-de-prazos` | Todo mês: prazos cumpridos, perdidos e quase perdidos, e o que mudar |
| avançado | `painel-da-controladoria` | Painel interno: prazos e carga por responsável, risco da semana |
| avançado | `triagem-em-massa` | Centenas de publicações iguais agrupadas, com uma providência para cada grupo |
| avançado | `acompanhar-valores` | Alvará, RPV, precatório e depósito judicial, do pedido ao levantamento |
| avançado | `prazos-em-lote` | A conta e a conferência de um lote inteiro de prazos |

Agentes: `agente-de-controladoria` (capta, tria e calcula o que chegou) e `revisor-de-controladoria` (refaz cada conta sozinho antes de a pessoa conferir). Funcionam no Cowork e no Claude Code. No chat com Projeto, a `rotina-da-controladoria` faz o mesmo ciclo, passo a passo.

A edição **essencial** traz 9 habilidades, a **completa** traz 16 e a **avançada** traz 20. As três são o mesmo plugin: para subir de edição, instale o zip novo no lugar do antigo.

## O que fica com a pessoa

Dizer o que o ato manda fazer, confirmar o número de dias e a regra, decidir prazo em dobro e ciência tácita, conferir cada prazo e decidir a providência. Abrir os painéis dos tribunais, que pedem senha ou certificado, também é da pessoa. O plugin capta, calcula, organiza e lembra, mas nunca confirma prazo, nunca usa senha ou certificado e nunca entra em sistema de tribunal.

## Onde fica o que o plugin produz

Na pasta `escritorio/`, dentro da pasta de trabalho, que é a mesma dos outros plugins motor:

- `04-base/controladoria/`: a tabela de regras validada, os calendários dos tribunais, os painéis, as providências de cada tipo de ato;
- `07-operacao/controladoria/`: as publicações e o teor de cada uma, os prazos, a carteira de processos, a conferência de cada dia, a agenda, a fila e os resumos;
- `07-operacao/_treino/`: tudo o que for feito com casos fictícios.

## Com os outros plugins motor

- **motor-juridico:** a providência "fazer peça" chega lá como pedido, com o prazo interno igual à data de segurança. O protocolo registrado lá fecha o prazo aqui.
- **motor-experiencia:** audiência, perícia, documento a pedir e decisão importante viram aviso ao cliente. Notícia ruim vai por ligação.

## Como instalar

- **App do Claude (Cowork e chat):** Personalizar > Plugins > Adicionar > Enviar plugin, com o zip da edição.
- **Uma habilidade sozinha:** Personalizar > Habilidades > + > Criar habilidade > Enviar, com o zip da habilidade. Comandos e agentes só existem no plugin inteiro.
- **Claude Code:** `claude --plugin-dir caminho/do/plugin`.

Os menus podem mudar com as atualizações do Claude: conferir na configuração da conta.

## Cuidados

- A busca no DJEN usa a consulta pública do CNJ e precisa de internet no ambiente onde o Claude roda. Sem ela, importe a planilha ou o e-mail.
- Nenhum prazo vale sem a dupla conferência. Na dúvida entre duas datas, vale a mais cedo.
- A tabela de regras e os calendários vêm marcados para conferir. Valide antes do primeiro prazo real e confira de novo todo ano.
- Publicação e prazo ficam fora do Projeto no Claude, com o mínimo de dados.
- Segue o Código de Ética e Disciplina da OAB e a LGPD.

Criado por Raphael Cardoso. Licença MIT.
