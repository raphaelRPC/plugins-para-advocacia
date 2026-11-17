# Comece aqui

Estes plugins colocam o escritório para rodar dentro do Claude. Cada plugin vem pronto no método e vazio no conteúdo: você preenche as fichas e ajusta ao seu jeito de trabalhar.

<!-- grupos:inicio -->
## Os três grupos

- **Fundação:** o `inicio-automacao` faz o diagnóstico, cria o código do escritório, os setores e os POPs. É a base que os outros plugins leem.
- **Motores:** um por setor. `motor-comercial`, `motor-experiencia`, `motor-juridico` e `motor-controladoria`.
- **Marketing:** `marketing-juridico-claude` (vídeo), `editor-de-carrossel-mjc` (carrossel) e `plugin-copywriter` (copy para qualquer nicho).
<!-- grupos:fim -->

## Em que ordem instalar

1. Instale primeiro o `inicio-automacao`.
2. Depois, o motor do setor que você quer pôr para rodar.
3. Por fim, os outros plugins que quiser usar.

Cada plugin tem um comando de começo, por exemplo `/motor-comercial:comecar`. Rode esse comando logo depois de instalar.

<!-- so-fonte:inicio -->
## As três edições dos motores

Cada motor tem três edições:

- **Essencial:** o que roda o setor desde o primeiro dia.
- **Completa:** a essencial mais as habilidades do dia a dia avançado.
- **Avançada:** a completa mais painéis, lotes e auditorias.

Uma edição contém a anterior. Dá para subir de edição quando quiser: você não perde a pasta `escritorio/`, onde ficam as fichas e tudo o que o escritório já preencheu.
<!-- so-fonte:fim -->

## Como instalar

Resumo para instalar pelo app do Claude, sem precisar do GitHub:

1. Abra o zip do pacote e entre na pasta `plugins`. Cada plugin tem o seu zip. Não descompacte esses zips.
2. No app do Claude, clique em Personalizar, depois em Plugins, depois em Adicionar e em Enviar plugin.
3. Escolha o zip de um plugin (comece pelo `inicio-automacao`) e espere ele aparecer na lista, ativado. Repita para cada plugin que quiser.
4. Escreva no chat o comando de começo do plugin, por exemplo `/motor-comercial:comecar`.

Os guias completos, para quem tem acesso ao GitHub:

- Pelo app do Claude, com o arquivo zip: [instalar-pelo-app.md](https://github.com/raphaelRPC/plugins-para-advocacia/blob/main/guia/instalar-pelo-app.md)
- Pelo GitHub, no Claude Code: [instalar-pelo-github.md](https://github.com/raphaelRPC/plugins-para-advocacia/blob/main/guia/instalar-pelo-github.md)

Se algo não funcionar, veja [problemas-comuns.md](https://github.com/raphaelRPC/plugins-para-advocacia/blob/main/guia/problemas-comuns.md).

## Cuidados

- Documento de cliente só em conta profissional ou de equipe.
- Nada sai para o cliente, para o processo ou para a agenda sem uma pessoa aprovar.
- Os plugins seguem o Código de Ética e Disciplina da OAB e a LGPD. Pesquisa de jurisprudência, quando aparece, é no Jus IA.
