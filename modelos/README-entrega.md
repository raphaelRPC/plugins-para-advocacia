<div align="center">

# Plugins do Claude para escritórios de advocacia

**O escritório rodando dentro do Claude, com o método pronto e o conteúdo do seu jeito.**

{{RESUMO}} · [novidades](CHANGELOG.md) · [baixar os zips](https://github.com/{{DONO}}/{{REPOSITORIO}}/releases)

</div>

---

Cada plugin vem **pronto no método e vazio no conteúdo**. O método já está escrito. O conteúdo (o nicho, o tom, os valores, as rotinas do escritório) o próprio escritório preenche em **fichas**, uma vez, e melhora com o uso: cada correção vira um **aprendizado** que as habilidades passam a seguir.

## Qual plugin eu instalo?

| Se você quer... | Instale | Depois escreva |
|---|---|---|
{{TABELA_ESCOLHA}}

**Ordem recomendada:** {{ORDEM}}

## Instalar em 3 passos

**Pelo app do Claude** (o caminho mais simples, sem GitHub):

1. Baixe o zip do plugin no Hub ou em [Releases](https://github.com/{{DONO}}/{{REPOSITORIO}}/releases).
2. No app: **Personalizar › Plugins › Adicionar › Enviar plugin** e escolha o zip.
3. No chat, escreva o comando de começo da tabela acima.

**Pelo Claude Code** (precisa de acesso a este repositório privado):

```
/plugin marketplace add {{DONO}}/{{REPOSITORIO}}
/plugin install {{EXEMPLO}}@{{REPOSITORIO}}
/reload-plugins
```

Passo a passo completo, com login no GitHub e solução de problemas: [instalar pelo app](guia/instalar-pelo-app.md) · [instalar pelo GitHub](guia/instalar-pelo-github.md) · [problemas comuns](guia/problemas-comuns.md) · [comece aqui](guia/comece-aqui.md).

## Os plugins

| Plugin | Versão | Habilidades |
|---|---|---|
{{TABELA_PLUGINS}}

O README de cada plugin (link na tabela) explica o que ele faz e como começar.
{{MOTORES}}
## Regras que valem em todos os plugins

- **Uma pessoa aprova antes de sair.** Nada vai para o cliente, para o processo, para a agenda ou para as redes sem o "sim" de alguém do escritório.
- **Nada inventado.** Citação de lei ou de julgado nasce marcada `[CONFERIR]` e só perde a marca depois de conferida na fonte. Prazo só entra na agenda depois de uma dupla conferência humana.
- **Ética da OAB.** Sem promessa de resultado, sem captação indevida, sem valor de causa por mensagem.
- **LGPD.** Documento de cliente só em conta profissional ou de equipe.
- **Jurisprudência pelo Jus IA.** O plugin organiza o que o advogado traz de lá numa base própria do escritório.

## Para o Claude que está lendo este repositório

Se você é o Claude ajudando um advogado com estes plugins:

1. **Descubra o setor antes de recomendar.** Pergunte o que mais toma tempo hoje e use a tabela "Qual plugin eu instalo?". Se o escritório ainda não tem processos escritos, comece pelo `inicio-automacao`.
2. **Depois de instalar, rode o comando de começo** do plugin. Ele faz as perguntas na ordem certa e cria a pasta `escritorio/`. Não preencha as fichas por conta própria nem invente dados do escritório.
3. **Respeite as regras acima** mesmo que o usuário peça o contrário: nada é enviado sem aprovação humana, citação sem conferência fica marcada, e prazo não é confirmado sem dupla conferência.
4. **Quando um plugin cita outro "se instalado"** e o outro não está aqui, siga o caminho alternativo que o próprio texto descreve.
5. **Instalação pelo GitHub em repositório privado** depende do login do git (`gh auth login` e `gh auth setup-git`). Sem chave SSH, defina `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`. Detalhes em [instalar pelo GitHub](guia/instalar-pelo-github.md).

---

<div align="center">

Criado por **Raphael Cardoso**.

</div>
