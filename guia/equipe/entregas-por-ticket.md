# Entregas por ticket (Clássico, Moderno e Futuro)

Este repositório é a **fonte**: só a equipe acessa. Os participantes recebem **entregas** montadas a partir dele. Cada entrega tem só os plugins do seu ticket, já cortados na edição certa, e nunca é editada à mão.

| Ticket | Repositório de entrega | Plugins | Habilidades | Promessa |
|---|---|---|---|---|
| Clássico | `plugins-advocacia-classico` | inicio-automacao, motor-juridico (completa) | 37 | 30 |
| Moderno | `plugins-advocacia-moderno` | inicio-automacao, motor-juridico, motor-controladoria e motor-comercial (avançada), motor-experiencia (essencial) | 83 | 80 |
| Futuro | `plugins-advocacia-futuro` | os 8, motores na avançada | 123 | 100 |

A divisão fica em `tickets.json`. Os plugins não citam ticket: o nome do ticket só aparece no nome do repositório de entrega.

## Montar

```
npm run entregas -- --versao 1.2.0
```

Isso cria `entregas-geradas/` (fora do git) com uma pasta por ticket:

- `repositorio/`: a árvore que vai para o repositório de entrega. Tem `.claude-plugin/marketplace.json`, `plugins/`, `README.md`, `CHANGELOG.md` e `guia/` (sem `equipe/`), todos gerados para aquele ticket;
- `zips/`: um zip por plugin (`<plugin>.zip`) e o pacote `<repositorio>.zip` com o LEIA-ME;
- `relatorio-de-referencias.md`: as linhas que citam por nome uma habilidade que não veio no ticket. Não barra nada, mas vale conferir se o texto já diz o que fazer sem ela.

Só entram arquivos **commitados** no git: rascunho local, arquivo ignorado ou não commitado nunca vai para o participante.

A montagem **falha** e não deve ser publicada quando:

- o total de habilidades fica abaixo da promessa;
- aparece na entrega qualquer arquivo que não seja dos plugins do ticket, dos guias listados em `"guias"` no `tickets.json`, do README, do CHANGELOG ou do `marketplace.json` (checagem de vazamento);
- um motor traz uma habilidade de edição acima da do ticket (o corte é recalculado do `edicoes.json`);
- um arquivo de plugin cita ticket ou repositório de entrega;
- um agente ou comando manda usar uma habilidade que não veio no ticket sem dizer "se instalada";
- um plugin manda rodar o comando de um plugin que não está no ticket sem dizer "se instalado" (linhas de tabela ficam de fora: são listas de referência);
- o README, o catálogo ou um plugin falham nas mesmas regras do `npm run checar`;
- sobra o nome do repositório da equipe ou um marcador de montagem num texto.

## Testar a instalação

```
node ferramentas/testar_entregas.mjs
```

Instala cada entrega numa configuração do Claude Code isolada, numa pasta temporária, sem mexer na sua, e confere se todos os plugins entram ativados.

## Guias do participante

Os guias de `guia/` são reaproveitados nas entregas:

- o que está entre `<!-- so-fonte:inicio -->` e `<!-- so-fonte:fim -->` só aparece aqui na fonte (por exemplo, a troca de edição);
- o bloco entre `<!-- grupos:inicio -->` e `<!-- grupos:fim -->` é trocado pela lista dos plugins do ticket;
- o endereço `raphaelRPC/plugins-para-advocacia` vira o do repositório de entrega, e o exemplo `motor-comercial` vira o `exemplo` do ticket.

O README das entregas sai de `modelos/README-entrega.md`.

## Mudar um ticket

1. Edite `tickets.json`.
2. Rode `npm run checar`: ele confere se os plugins existem, se a edição de cada um é válida e se a promessa continua cumprida.
3. Rode `npm run entregas -- --versao X.Y.Z` e `node ferramentas/testar_entregas.mjs`.

## Como os pacotes chegam ao participante (decisão de 17/11)

Os plugins são para o evento, sem atualizações depois. Por isso **não há repositório de entrega nem organização no GitHub**: o `"github": false` do `tickets.json` tira dos guias tudo o que fala de instalar pelo GitHub.

1. Cada tag `vX.Y.Z` gera, neste repositório privado, um release em **rascunho** com três pacotes: `plugins-advocacia-classico.zip`, `plugins-advocacia-moderno.zip` e `plugins-advocacia-futuro.zip` (sem a versão no nome; a versão fica no título do release).
2. Cada pacote tem o `LEIA-ME.md` (como instalar pelo app e problemas comuns) e, na pasta `plugins`, um zip por plugin.
3. A equipe do Hub baixa os três e coloca cada um só na pasta da turma do seu ticket.

Se um dia quiserem a instalação pelo GitHub, o caminho está pronto: criar uma organização, os três repositórios privados com um time por ticket (permissão **Read**), trocar `"dono"` e pôr `"github": true` no `tickets.json`, e ligar a publicação nos repositórios.
