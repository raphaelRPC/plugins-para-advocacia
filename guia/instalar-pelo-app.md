# Instalar pelo app do Claude

Este caminho usa o arquivo zip do plugin. Serve para o app do Claude no computador e para o Cowork.

## Recebeu o pacote com todos os plugins?

Abra (descompacte) o zip do pacote. Dentro da pasta `plugins` há um zip por plugin. Envie cada zip de plugin, um por vez, pelos passos abaixo. Não descompacte os zips de plugin: o app recebe o zip fechado.

## Antes de começar

Os menus do Claude podem mudar com as atualizações. Se algum nome for diferente, procure um parecido na configuração da conta.

## Passo a passo

1. Baixe o zip do plugin, pelo Hub ou pelo release do GitHub. O zip tem o nome do plugin, por exemplo `motor-comercial.zip`.
2. Abra o app do Claude.
3. Clique em Personalizar.
4. Clique em Plugins.
5. Clique em Adicionar.
6. Clique em Enviar plugin.
7. Escolha o arquivo zip que você baixou.
8. Espere o plugin aparecer na lista e confira se está ativado.
9. Escreva no chat o comando de começo do plugin, por exemplo `/motor-comercial:comecar`.

O comando faz até 8 perguntas e mostra um resultado com casos de treino.

<!-- so-fonte:inicio -->
## Trocar de edição

1. Baixe o zip da edição nova.
2. Envie o zip novo, do mesmo jeito, no lugar do antigo.
3. Depois de enviar, confira na lista de plugins que ficou só um com aquele nome. Se ficaram dois, remova o antigo.

A pasta `escritorio/` não se perde.
<!-- so-fonte:fim -->

## O que funciona onde

No Cowork, tudo funciona. No chat comum do app, os agentes e os hooks são ignorados, então algumas rotinas automáticas não rodam.

## Se der problema

Veja [problemas-comuns.md](problemas-comuns.md).
