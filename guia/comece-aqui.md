# Comece aqui

Estes plugins colocam o escritório para rodar dentro do Claude. Cada plugin vem pronto no método e vazio no conteúdo: você preenche as fichas e ajusta ao seu jeito de trabalhar.

## Os três grupos

- **Fundação:** o `inicio-automacao` faz o diagnóstico, cria o código do escritório, os setores e os POPs. É a base que os outros plugins leem.
- **Motores:** um por setor. `motor-comercial`, `motor-experiencia`, `motor-juridico` e `motor-controladoria`.
- **Marketing:** `marketing-juridico-claude` (vídeo), `editor-de-carrossel-mjc` (carrossel) e `plugin-copywriter` (copy para qualquer nicho).

## Em que ordem instalar

1. Instale primeiro o `inicio-automacao`.
2. Depois, o motor do setor que você quer pôr para rodar.
3. Por fim, os outros plugins que quiser usar.

Cada plugin tem um comando de começo, por exemplo `/motor-comercial:comecar`. Rode esse comando logo depois de instalar.

## As três edições dos motores

Cada motor tem três edições:

- **Essencial:** o que roda o setor desde o primeiro dia.
- **Completa:** a essencial mais as habilidades do dia a dia avançado.
- **Avançada:** a completa mais painéis, lotes e auditorias.

Uma edição contém a anterior. Dá para subir de edição quando quiser: você não perde a pasta `escritorio/`, onde ficam as fichas e tudo o que o escritório já preencheu.

## Como instalar

Escolha um dos dois caminhos:

- Pelo app do Claude, com o arquivo zip: [instalar-pelo-app.md](instalar-pelo-app.md)
- Pelo GitHub, no Claude Code: [instalar-pelo-github.md](instalar-pelo-github.md)

Se algo não funcionar, veja [problemas-comuns.md](problemas-comuns.md).

## Cuidados

- Documento de cliente só em conta profissional ou de equipe.
- Nada sai para o cliente, para o processo ou para a agenda sem uma pessoa aprovar.
- Os plugins seguem o Código de Ética e Disciplina da OAB e a LGPD. Pesquisa de jurisprudência, quando aparece, é no Jus IA.
