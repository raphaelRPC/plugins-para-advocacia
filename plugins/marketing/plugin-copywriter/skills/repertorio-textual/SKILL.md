---
name: repertorio-textual
description: Escolhe, aplica, adapta, corrige e analisa gêneros e tipos textuais em textos de marketing e redes sociais (crônica, depoimento, relato de caso, notícia, artigo de opinião, manifesto, consultório, verbete, aula, diário, parábola, cena, carta aberta, anúncio). Use quando o usuário pedir para criar um post ou carrossel e for preciso decidir a forma do texto, quando pedir para adaptar um texto pronto para outro formato ou tom, quando um texto estiver confuso por misturar formatos, quando pedir análise de que tipo de texto é aquele, ou quando pedir ajuda para desenvolver o corpo do texto e não apenas o gancho. Não use para limpar linguagem de IA (use humanizar-texto) nem para melhorar frase a frase (use polimento-textual). Autor advogado com o Editor de Carrossel instalado: prefira a habilidade dele, com a camada da OAB.
---

# Repertório textual

Esta habilidade decide e governa a **forma** do texto: qual gênero e qual sequência textual sustentam melhor aquele conteúdo, e como cada um se constrói do começo ao fim. Ela não trata de qualidade de frase nem de assinatura de IA.

Fichas completas em `references/fichas-tipos-generos.md`. Leia apenas a ficha do gênero e da sequência escolhidos, depois de rodar a camada de decisão.

## Regra de comando

O gênero vem primeiro e comanda, porque é a resposta a uma situação social. A sequência textual é consequência dele, confirmada pelo objetivo do post.

Todo texto declara **um gênero e uma sequência dominante antes da primeira linha**, e ambos governam a peça inteira. Uma frase de outra natureza não quebra a regra se servir à sequência dominante. O que se proíbe é a troca de comando, quando o texto muda de função no meio do caminho: começa relato, vira aula, termina anúncio.

Exceção declarada: o aforismo não desenvolve sequência nenhuma.

## Camada de decisão

Rode as três entradas antes de qualquer escrita. A primeira manda nas outras.

### Entrada 1: qual matéria-prima existe

| Matéria-prima disponível | Gêneros candidatos |
|---|---|
| Caso real vivido ou atendido | relato de caso, crônica, depoimento |
| Erro próprio, algo que deu errado | depoimento, diário |
| Padrão observado em vários casos | reportagem, artigo de opinião |
| Opinião que incomoda parte do público | artigo de opinião, manifesto |
| Princípio inegociável do autor | manifesto, aforismo |
| Dado, decisão nova, mudança de regra | notícia, verbete |
| Dúvida que se repete no atendimento | consultório, entrevista, conversa digital |
| Conceito que o público entende errado | verbete, aula |
| Rotina, bastidor, cena de trabalho | diário, crônica, cena |
| Nada concreto | pare e peça matéria-prima ao autor |

Sem matéria-prima, não escolha forma nenhuma. Peça o caso, o número, a data ou a opinião que falta.

### Entrada 2: o que o leitor deve fazer ao terminar

| Objetivo | Sequência |
|---|---|
| Entrar numa história e querer o desfecho | narrativa |
| Enxergar um detalhe que passava batido | descritiva |
| Concordar, discordar ou mudar de ideia | argumentativa |
| Entender como uma coisa funciona | expositiva |
| Executar um passo agora | injuntiva |
| Se reconhecer numa conversa | dialogal |

### Entrada 3: quem lê

Questão de custo cognitivo, não de permissão. Público leigo processa melhor sequências narrativas e dialogais. Público técnico absorve expositivas e argumentativas com menos atrito. Público misto rende com narrativa que fecha em explicação, mantida a narrativa no comando.

## Modos de operação

**Criar.** Roda a camada de decisão, declara gênero e sequência com justificativa, abre a ficha correspondente e desenvolve o texto seguindo abertura, progressão e fecho daquela ficha.

**Adaptar.** Recebe texto pronto e forma de destino. Mantém a matéria-prima, troca abertura, progressão e fecho conforme a ficha de destino, e aponta o que se perde na troca.

**Corrigir.** Identifica gênero e sequência praticados, localiza o ponto exato da troca de comando e reescreve o trecho desviado para voltar à sequência dominante.

**Analisar.** Diagnóstico sem reescrita: gênero praticado, sequência dominante, pontos de deriva, adequação entre forma e matéria-prima, e recomendação alternativa quando houver ganho claro.

## Saída padrão

Antes do texto, declare em uma linha: gênero, sequência dominante e por que a matéria-prima sustenta essa combinação.

Depois entregue o que o modo pede. No fim, confira dois itens: o texto manteve a sequência declarada do começo ao fim, e a forma escolhida se apoia em matéria-prima real.

## Regras de escrita desta habilidade

Zero travessões, em qualquer quantidade e também nas suas respostas. Evite picote, que são três ou mais frases curtas seguidas terminando em ponto. O formato de campos rotulados das fichas é material de consulta e nunca deve aparecer no texto entregue ao leitor.
