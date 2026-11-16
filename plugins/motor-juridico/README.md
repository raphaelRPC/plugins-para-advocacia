# motor-juridico

Plugin do Claude para a produção jurídica do escritório de advocacia, em qualquer área: entender o caso, minutar no padrão do escritório, conferir cada citação e cada dado, e preparar o protocolo. E, o mais importante, transformar as peças boas do escritório em habilidades próprias, que fazem a próxima peça do jeito que o escritório já faz.

Dois erros assustam todo advogado que usa IA. O primeiro é a jurisprudência inventada. O segundo é o nome do cliente errado que veio de outra peça. Aqui, toda citação nasce marcada "a conferir" e só perde a marca quando é conferida na fonte. E toda peça passa por uma conferência de dados antes de chegar ao advogado: nomes, gênero, datas, valores, documentos citados e pedidos sem fundamento.

A pesquisa de jurisprudência é feita no **Jus IA**. O plugin organiza o que você traz de lá numa base de jurisprudência do próprio escritório, conferida e com data, que as habilidades consultam a cada peça.

As habilidades vêm prontas no método e vazias no conteúdo. Quem traz o conteúdo é o escritório: as peças boas, as teses, a pesquisa e o padrão de escrita. O contexto mora em duas **fichas**, a do escritório e a jurídica, e cada correção pode virar um **aprendizado**.

## Como começar

```
/motor-juridico:comecar
```

Em cerca de 15 minutos e 8 perguntas, você tem as fichas mínimas e vê a conferência trabalhando numa minuta de treino com dez erros escondidos. Depois:

```
/motor-juridico:ciclo     roda a fila de peças do dia: dossiês, minutas e conferências
/motor-juridico:fila      o advogado define a tese, revisa, aprova e registra o protocolo
/motor-juridico:status    a produção agora: etapas, prazos internos, citações por conferir
/motor-juridico:ficha     completa as fichas, seção por seção
```

## As habilidades

| Edição | Habilidade | O que faz |
|---|---|---|
| essencial | `trazer-pesquisa` | Organiza a pesquisa do Jus IA em fichas de julgado por tema e guarda na base do escritório |
| essencial | `conferir-citacoes` | Audita todas as citações de uma peça e devolve um relatório em verde, amarelo e vermelho. Tira a marca só do que foi conferido |
| essencial | `conferir-peca` | Nome de outro cliente, gênero trocado, datas e valores divergentes, documento que não existe, pedido sem fundamento |
| essencial | `minutar-peca` | A minuta a partir do dossiê e da tese que o advogado escolheu, no padrão do escritório, em .md e .docx |
| essencial | `peca-vira-habilidade` | De 3 a 5 peças boas do mesmo tipo viram uma habilidade própria do escritório, testada e pronta para instalar |
| essencial | `dossie-do-caso` | Os documentos do caso viram índice, linha do tempo, matriz de prova, contradições e lacunas |
| essencial | `estrategia-do-caso` | Caminhos, riscos, cenários e plano de provas, até a decisão do advogado |
| essencial | `rotina-juridica` | O motor: o resumo do dia da produção, a tarefa agendada e o ciclo à mão |
| essencial | `adaptar-juridico` | O plugin ajustado às áreas, ao padrão visual e às rotinas do escritório |
| completo | `banco-de-teses-vivo` | Cada tese do escritório com o resultado que ela teve, por juízo e órgão julgador |
| completo | `leitura-dos-autos` | O processo inteiro vira mapa: pedidos, decisões, provas, pontos de ataque |
| completo | `comparar-versoes` | O que mudou entre duas versões de um documento, e o risco de cada mudança |
| completo | `mapa-jurisprudencial` | Como o tema é decidido, por tribunal e órgão, com as viradas e as distinções |
| completo | `advogado-do-diabo` | A melhor resposta da parte contrária contra a nossa tese, e o que reforçar |
| completo | `preparar-protocolo` | Checklist do protocolo por sistema e o registro do protocolo feito |
| completo | `conflito-de-interesses` | O caso novo cruzado com clientes e partes contrárias antigos, antes de aceitar |
| completo | `lgpd-do-escritorio` | Os dados que o escritório trata, bases legais, avisos, pedido de titular e incidente |
| avançado | `pecas-em-lote` | Contencioso de massa: uma planilha e a habilidade da peça viram um lote de minutas conferidas |
| avançado | `monitor-de-precedentes` | Avisa quando um tema da base precisa de pesquisa nova e quando uma tese é afetada |
| avançado | `compliance-para-clientes` | Diagnóstico, programa de integridade e due diligence para cliente empresa |
| avançado | `sustentacao-oral` | Roteiro cronometrado, memorial curto e as perguntas prováveis dos julgadores |

Agentes: `agente-juridico` (roda a fila de peças do dia) e `revisor-juridico` (confere cada minuta antes de ela chegar ao advogado). Funcionam no Cowork e no Claude Code. No chat com Projeto, a `rotina-juridica` faz o mesmo ciclo, passo a passo.

A edição **essencial** traz 9 habilidades, a **completa** traz 17 e a **avançada** traz 21. As três são o mesmo plugin: para subir de edição, instale o zip novo no lugar do antigo.

## O que fica com o advogado

Escolher a tese e o caminho do caso, revisar, aprovar, assinar e protocolar. O plugin prepara, confere e organiza, mas nunca protocola nem mexe em certificado digital ou senha de sistema. Prazos processuais e publicações ficam com a rotina de controladoria do escritório. Aqui entra só o prazo interno que alguém informou, para ordenar a fila.

## Onde fica o que o plugin produz

Na pasta `escritorio/`, dentro da pasta de trabalho, que é a mesma dos outros plugins motor:

- `04-base/juridico/`: jurisprudência por tema, teses, modelos, padrão visual, base de partes;
- `04-base/habilidades-do-escritorio/`: as habilidades próprias que o plugin gera;
- `07-operacao/juridico/`: o registro de peças (`pecas.csv`), a pasta de cada caso (dossiê, estratégia, minutas, conferências, protocolo) e a fila do advogado;
- `07-operacao/_treino/`: tudo o que for feito com casos fictícios.

## Como instalar

- **App do Claude (Cowork e chat):** Personalizar > Plugins > Adicionar > Enviar plugin, com o zip da edição.
- **Uma habilidade sozinha:** Personalizar > Habilidades > + > Criar habilidade > Enviar, com o zip da habilidade. Comandos e agentes só existem no plugin inteiro.
- **Claude Code:** `claude --plugin-dir caminho/do/plugin`.

Os menus podem mudar com as atualizações do Claude: conferir na configuração da conta.

## Cuidados

- Documento de cliente só em conta profissional ou de equipe. Em conta pessoal, use os casos de treino.
- Nenhuma citação vai para o processo sem conferência na fonte. A IA nunca completa número, relator, data ou enunciado de memória.
- Dado sensível do caso (saúde, criança, renda) entra na peça só no que for necessário.
- Segue o Código de Ética e Disciplina da OAB e a LGPD.

Criado por Raphael Cardoso. Licença MIT.
