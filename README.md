# Plugins do Claude para escritórios de advocacia

Plugins para o advogado instalar no Claude e colocar o escritório para rodar: a fundação da automação, os motores de cada setor e o marketing jurídico. Cada plugin vem pronto no método e vazio no conteúdo: o escritório preenche as fichas, ajusta ao próprio jeito de trabalhar, e cada correção vira regra para as próximas vezes.

## Os plugins

| Plugin | O que faz |
|---|---|
| `inicio-automacao` | A fundação: diagnóstico, código do escritório, setores, POPs e a base que os outros plugins leem |
| `motor-comercial` | De quem escreve pela primeira vez até o contrato assinado: triagem, consulta, proposta, contrato, retorno |
| `motor-experiencia` | O suporte ao cliente, do contrato ao encerramento: boas-vindas, andamento traduzido, resumo do mês, página do caso |
| `motor-juridico` | A produção das peças: dossiê, estratégia, minuta no padrão do escritório, conferência de cada citação e dado, protocolo |
| `motor-controladoria` | Publicações e prazos: captação, triagem, conta do prazo pelo calendário do tribunal e dupla conferência antes da agenda |
| `marketing-juridico-claude` | Vídeo: Rito PICO, roteiro e edição de vídeo, com a Trava OAB |
| `editor-de-carrossel-mjc` | Carrossel: texto com a camada da OAB, arte no Canva ou no motor próprio, linha editorial, protocolo e rotinas |
| `plugin-copywriter` | Copy para qualquer nicho: repertório, gatilhos, arquitetura, polimento, humanização e figuras de linguagem |

Os quatro motores usam a mesma pasta `escritorio/` e o mesmo código de cliente: um enxerga o que o outro produziu.

## Como instalar

**Claude Code** (com acesso a este repositório):

```
/plugin install motor-comercial --marketplace raphaelRPC/plugins-para-advocacia
```

Troque `motor-comercial` pelo plugin que quiser. Em versões mais antigas do Claude Code, em dois passos:

```
/plugin marketplace add raphaelRPC/plugins-para-advocacia
/plugin install motor-comercial@plugins-para-advocacia
```

Para atualizar depois: `/plugin marketplace update plugins-para-advocacia`.

**App do Claude (Cowork e chat):** baixe o zip do plugin e envie em Personalizar > Plugins > Adicionar > Enviar plugin. Os menus podem mudar com as atualizações do Claude: conferir na configuração da conta.

Depois de instalar, rode o comando de começo do plugin, por exemplo `/motor-comercial:comecar`. Ele faz até 8 perguntas e mostra um resultado com casos de treino.

## Cuidados

- Documento de cliente só em conta profissional ou de equipe.
- Nada sai para o cliente, para o processo ou para a agenda sem uma pessoa aprovar.
- Os plugins seguem o Código de Ética e Disciplina da OAB e a LGPD. Pesquisa de jurisprudência, quando aparece, é no Jus IA.

Criado por Raphael Cardoso.
