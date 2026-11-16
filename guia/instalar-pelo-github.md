# Instalar pelo GitHub

Este caminho usa o Claude Code e o repositório `raphaelRPC/plugins-para-advocacia`. Por ele vem também a edição avançada dos motores.

## Antes de começar

O repositório é privado. O acesso ao repositório é liberado pela equipe; veja com quem te enviou o curso. Você precisa de duas coisas:

1. Uma conta no GitHub com o acesso ao repositório liberado. Peça a liberação a quem administra o repositório.
2. Estar logado no GitHub neste computador. Faça isso de um destes jeitos:
   - Instale o GitHub Desktop e entre com a sua conta.
   - Ou, no terminal, rode `gh auth login` e depois `gh auth setup-git`.

O Claude Code não pede senha. Ele usa o login que o git já tem no computador.

Se você não tem chave SSH no GitHub, defina antes a variável de ambiente `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`. Só ter a variável `GITHUB_TOKEN` não basta.

## Instalar em um passo

1. Abra o Claude Code.
2. Escreva o comando abaixo, trocando `motor-comercial` pelo plugin que você quer:

```
/plugin install motor-comercial --marketplace raphaelRPC/plugins-para-advocacia
```

3. Se o Claude Code pedir para adicionar o marketplace, confirme.
4. Escreva `/reload-plugins`, ou reinicie o Claude Code.
5. Rode o comando de começo do plugin, por exemplo `/motor-comercial:comecar`.

Esse comando de um passo existe a partir do Claude Code 2.1.275. Se o seu for mais antigo, use os dois passos abaixo.

## Instalar em dois passos

1. Adicione o marketplace:

```
/plugin marketplace add raphaelRPC/plugins-para-advocacia
```

2. Instale o plugin:

```
/plugin install motor-comercial@plugins-para-advocacia
```

3. Escreva `/reload-plugins`, ou reinicie o Claude Code.

Os mesmos comandos funcionam no terminal comum, escrevendo `claude plugin marketplace add ...` e `claude plugin install ...`.

## Atualizar

Você só recebe uma versão nova quando o número da versão do plugin muda.

Para atualizar tudo:

1. No Claude Code, escreva `/plugin`.
2. Abra a aba Marketplaces.
3. Escolha `plugins-para-advocacia`.
4. Clique em Update marketplace.

Para atualizar um plugin só, no terminal:

```
claude plugin update motor-comercial@plugins-para-advocacia
```

A atualização automática vem desligada em repositório privado. Para ligar: `/plugin`, aba Marketplaces, Enable auto-update.

## Se der problema

Veja [problemas-comuns.md](problemas-comuns.md).
