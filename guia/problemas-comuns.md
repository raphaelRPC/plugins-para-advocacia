# Problemas comuns

## "Repositório não encontrado" ou falha ao clonar

O repositório é privado. Isso quer dizer uma destas duas coisas:

- Você ainda não tem acesso ao repositório. Peça a liberação a quem administra.
- Você não está logado no GitHub neste computador. Entre pelo GitHub Desktop, ou rode `gh auth login` e depois `gh auth setup-git`.

Se você não tem chave SSH, defina a variável `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` e tente de novo. Só a variável `GITHUB_TOKEN` não resolve.

## O comando `/comecar` não aparece

1. Confira se o plugin está ativado na lista de plugins.
2. Escreva `/reload-plugins`, ou reinicie o Claude.
3. Confira se o zip é o do plugin certo. Cada plugin tem o seu comando, por exemplo `/motor-comercial:comecar`.

Se mesmo assim não aparecer, baixe o zip de novo e envie outra vez.

## Um script não roda

Os scripts precisam do Python no computador. Instale pelo site oficial: https://www.python.org/downloads/

Depois de instalar, feche e abra o Claude de novo.

## O hook não roda no Mac

Reinstale o plugin com a versão mais nova. A correção veio em versão nova.

## O app recusou o zip

O app aceita até 5.000 arquivos e 200 MB por plugin. Confira se o arquivo é o zip baixado do Hub ou do release, sem ter sido aberto e refeito.
