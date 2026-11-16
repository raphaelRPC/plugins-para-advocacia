---
name: uso-do-plano
description: >-
  Uso do plano do curso Marketing Jurídico com Claude (RPC Educação). Mostra quanto cada tarefa do plugin
  pesou no limite de uso do plano do advogado (edição de vídeo, minutas, Rito PICO e o resto), o que mais
  pesou e como gastar menos. No Claude Code, liga a linha de status com a sessão de 5 horas e a semana.
  Use quando o advogado disser "quanto eu gastei?", "quanto gastei hoje", "quanto essa edição gastou",
  "meu limite está acabando", "como gastar menos do plano", "por que meu limite acabou rápido",
  "liga a linha de status" ou variação.
---

# Uso do plano

O advogado quer saber quanto do limite do plano cada tarefa consome e como gastar menos. Fale em "uso do seu plano" e em peso (leve, médio, pesado, muito pesado). Token (a unidade de texto que o Claude conta) só aparece se ele pedir o detalhe, e vem explicado na mesma frase.

## O que é medido e o que é estimativa (diga sempre qual dos dois)

| Onde ele usa | Medido | Estimativa |
|---|---|---|
| Claude Code | Os tokens de cada conversa (registro automático do plugin) e, com a linha de status ligada, o percentual da sessão de 5 horas e da semana | O peso (a régua que traduz tokens em leve, médio, pesado) |
| Cowork e aplicativo | Nada chega ao plugin. O percentual oficial está em Configurações > Uso | O peso de cada tarefa pela tabela de `references/regua-de-peso.md` |

Nunca diga "você gastou X% do plano" sem o dado vir da linha de status ou da página de Uso. A Anthropic não publica quantos tokens cabem no limite, então o plugin não converte peso em percentual.

## "Quanto eu gastei?"

Use o `python` de `~/.marketing-juridico/ferramentas/caminhos.json` (instalado pela Ilha de edição); se não houver, `python3` ou `python`. O script está em `scripts/uso.py` desta skill.

1. Rode `PY scripts/uso.py resumo` (hoje e 7 dias; `--dias 30` para o mês).
2. Conte em até cinco linhas: quanto pesou hoje e na semana, por tarefa; a conversa mais pesada e o que mais pesou nela; o último percentual medido do plano, se houver.
3. Feche com **uma** dica de `references/gaste-menos.md`, a que responde ao que mais pesou (muitas imagens: dica das imagens; conversa longa: dica da conversa nova). Uma só.
4. Se o script disser que não há registro (Cowork, aplicativo ou instalação recente): explique em uma frase, mande o advogado a Configurações > Uso para o percentual oficial e ofereça a tabela de pesos por tarefa (`references/regua-de-peso.md`), dizendo que é estimativa.

## "Quanto essa conversa gastou?"

Rode `PY scripts/uso.py conversa`. Ele lê a conversa mais recente do registro, que é esta. Repasse as linhas como vieram: peso, comparação com as conversas do próprio advogado (só aparece depois de 5 conversas registradas), o que mais pesou e, com a linha de status, o percentual medido da sessão de 5 horas.

## Linha de status (só Claude Code, com o "sim")

Mostra no rodapé: `Sessão 34% (zera 15h20) · Semana 12% (zera sex 09h00) · Conversa 41% cheia`. Também passa a guardar o percentual antes e depois de cada conversa, o que deixa o resumo mais preciso.

1. Rode `PY scripts/uso.py configurar-linha-de-status` (só mostra). Se `configAtual` não for vazio, ele já tem uma linha de status: conte qual é e pergunte se troca. Nunca substitua sem o "sim".
2. Explique o que muda e peça o "sim": "vou ligar no rodapé do Claude Code o uso da sessão e da semana; guardo uma cópia da configuração atual".
3. Com o "sim": `PY scripts/uso.py configurar-linha-de-status --aplicar`. O percentual aparece depois da primeira resposta de uma conversa nova. Só funciona nos planos Pro e Max.
4. No Cowork e no aplicativo não existe linha de status. Diga isso e mostre o caminho da página de Uso.

Detalhes em `references/linha-de-status.md`.

## No fim de cada edição de vídeo

A Ilha de edição chama `PY <pasta desta skill>/scripts/uso.py conversa` depois de entregar o vídeo e mostra uma linha só: "Peso desta edição: médio. O que mais pesou: 14 quadros conferidos por imagem." Sem registro, a linha vem da tabela de `references/regua-de-peso.md` e diz "estimativa".

## "Como gastar menos?"

Leia `references/gaste-menos.md` e responda com as dicas que servem ao jeito dele de usar (olhe o resumo antes, se houver registro). No máximo três por vez, cada uma com o "faça assim".

## Privacidade

O registro guarda só números (tokens, quantidade de imagens, nome da tarefa) e o endereço do histórico de cada conversa em `~/.marketing-juridico/uso/`. Nenhum texto de conversa é copiado. Nada sai do computador. Para apagar o registro, basta apagar essa pasta, com o "sim" dele.
