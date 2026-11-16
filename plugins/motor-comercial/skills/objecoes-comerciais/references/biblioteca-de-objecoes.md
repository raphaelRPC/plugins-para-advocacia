# Biblioteca de objeções (base do plugin)

Base para o escritório montar a sua em `escritorio/04-base/comercial/objecoes.md`. As respostas estão em tom neutro, com tratamento por "você". O modo A da habilidade reescreve cada uma no tom da ficha, com os diferenciais verdadeiros do escritório. Nenhuma resposta sai sem uma pessoa ler (A).

Campos entre colchetes vêm da ficha, da política ou da proposta, e a habilidade preenche antes de mostrar; campo que não existe vai para o cabeçalho interno como `[A PREENCHER]`, nunca no texto que vai ao contato. Entre chaves fica o que quem envia escolhe na hora, como `{PRAZO}`: um prazo que o escritório cumpre.

Cabeçalho do arquivo do escritório:

```markdown
---
documento: Objeções comerciais
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
---

# Objeções comerciais · [NOME DO ESCRITÓRIO]

> Respostas aprovadas para as objeções mais comuns. Sem desconto como isca, sem escassez, sem falar de colegas, sem promessa. Mexer no valor é decisão de [QUEM APROVA].
```

Depois, uma seção por objeção, neste formato.

---

## 1. "Está caro"

- **O que pode estar por trás:** o total assusta; a entrada não cabe agora; não ficou claro o que está incluído; medo de pagar e não dar em nada.
- **Pergunta de esclarecimento:** "Para eu entender: o que pesou mais, o valor total, a entrada ou a parcela?"
- **Resposta-base (depois de entender):**
  > Entendo, é um valor que pesa. Na proposta estão [RESUMO DO INCLUÍDO EM UMA LINHA]. Se o que aperta é [A ENTRADA | A PARCELA], posso ver com [QUEM APROVA] as formas de pagamento que temos e te retorno até {PRAZO}.
- **Se o problema é o valor em si:** modo C, opções dentro da política para o advogado.
- **Nunca:** baixar o valor na hora; "faço um precinho"; "esse valor é só até amanhã".
- **Vai para o advogado quando:** o pedido é valor menor, ou a pessoa conta uma dificuldade séria (desemprego, doença).

## 2. "Vou pensar"

- **O que pode estar por trás:** precisa de tempo de verdade; ficou alguma dúvida que não disse; vai comparar; quer falar com alguém.
- **Pergunta de esclarecimento:** "Claro. Ficou alguma dúvida sobre a proposta que eu possa esclarecer agora?"
- **Resposta-base:**
  > Claro, pense com calma. Se surgir qualquer dúvida, pode me perguntar por aqui. A proposta vale até [DATA DA VALIDADE].
- **Depois:** o retorno segue a régua da ficha (`follow-up`, se instalada). Nada de mensagem no dia seguinte "só para saber se pensou".
- **Nunca:** "as vagas estão acabando"; "outros clientes estão esperando"; "se não fechar agora, não sei se consigo atender".
- **Vai para o advogado quando:** a pessoa diz que está em dúvida sobre entrar ou não com a ação (decisão de estratégia).

## 3. "Outro advogado cobra menos"

- **O que pode estar por trás:** quer entender a diferença; quer um desconto; já decidiu e está avisando.
- **Pergunta de esclarecimento:** "Obrigado por me contar. Quer que eu te explique, item por item, o que está incluído na nossa proposta? Assim você compara com calma o que cada uma cobre."
- **Resposta-base:**
  > Cada escritório organiza o trabalho de um jeito, e eu não consigo falar do trabalho de outro colega. O que posso fazer é te mostrar o que está na nossa: [ITENS DO INCLUÍDO] e [ITENS DO NÃO INCLUÍDO]. [UM DIFERENCIAL VERDADEIRO, SE HOUVER]. Se depois disso você preferir o outro escritório, tudo bem, a decisão é sua.
- **Nunca:** comentar o outro escritório, para o bem ou para o mal; "ele deve estar cobrando abaixo da tabela"; "cubro a oferta".
- **Vai para o advogado quando:** o cliente pede para igualar o valor.

## 4. "Posso pagar só no fim?"

- **O que pode estar por trás:** não tem dinheiro agora; desconfia e quer garantia; ouviu que "advogado só cobra se ganhar".
- **Pergunta de esclarecimento:** "O que fica difícil: pagar a entrada agora ou pagar algo antes de ter um resultado?"
- **Resposta-base (escritório que cobra fixo):**
  > Para este tipo de caso, o escritório trabalha com honorário fixo, porque o trabalho acontece desde o começo: [ETAPAS INICIAIS]. O que dá para fazer é dividir: [CENÁRIOS DA POLÍTICA].
- **Resposta-base (política prevê êxito ou misto para o tipo de caso):**
  > Para este tipo de caso, há a possibilidade de [MODELO DA POLÍTICA]. Vou ver com [QUEM APROVA] e te mando como ficaria.
- **Nunca:** "só paga se ganhar, e você vai ganhar"; mudar para êxito sem a política prever e sem o advogado decidir.
- **Vai para o advogado quando:** a mudança de modelo é pedida.

## 5. "Preciso falar com minha família"

- **O que pode estar por trás:** a decisão é de fato conjunta; quem paga é outra pessoa; precisa de apoio para decidir.
- **Pergunta de esclarecimento:** "Faz todo sentido. Quer que eu mande um resumo curto da proposta para você mostrar?"
- **Resposta-base:**
  > Claro, é uma decisão para tomar junto. Se ajudar, te mando um resumo de cinco linhas com o que está incluído e as formas de pagamento. E se quiser, marcamos uma ligação com você e quem for decidir junto.
- **Cuidado com sigilo:** o caso é do cliente. Conversa com a família só com a pessoa presente ou com autorização dela.
- **Nunca:** "você não precisa da opinião de ninguém"; pressionar pela decisão individual.
- **Vai para o advogado quando:** quem vai contratar é outra pessoa (o contrato muda: veja `contrato-de-honorarios`, se instalada).

## 6. "Demora muito"

- **O que pode estar por trás:** medo de esperar anos; experiência ruim; precisa do dinheiro logo.
- **Pergunta de esclarecimento:** "O que mais preocupa você no tempo: ficar sem notícia ou precisar de uma solução rápida?"
- **Resposta-base:**
  > Eu entendo. O tempo de cada etapa depende do [ÓRGÃO | JUÍZO], e por isso a gente não promete prazo. O que a gente garante é o que depende do escritório: [COMO O ESCRITÓRIO AVISA, DA FICHA OU DOS DIFERENCIAIS]. Na proposta, as etapas estão explicadas uma por uma.
- **Nunca:** "em seis meses está resolvido"; "a gente tem contato lá dentro"; prazo de decisão de qualquer tipo.
- **Vai para o advogado quando:** há pedido de urgência no caso (liminar, tutela): é estratégia.

## 7. "Já tive advogado e não deu certo"

- **O que pode estar por trás:** desconfiança; ficou sem notícia; perdeu o caso; quer saber se agora vai ser diferente.
- **Pergunta de esclarecimento:** "Sinto muito que tenha sido assim. O que mais fez falta naquela vez?"
- **Resposta-base:**
  > Agradeço por você me contar. Não consigo falar do que aconteceu antes, mas posso te dizer como a gente trabalha: [DIFERENCIAIS VERDADEIROS LIGADOS AO QUE FEZ FALTA]. E tudo o que combinamos fica por escrito, na proposta e no contrato.
- **Nunca:** criticar o advogado anterior; "com a gente vai ser diferente, pode ter certeza"; analisar o caso antigo por mensagem.
- **Vai para o advogado quando:** há caso antigo em andamento (troca de advogado, substabelecimento, prazo).

## 8. "Por que a consulta é paga?"

- **O que pode estar por trás:** comparou com escritório que não cobra; não sabe o que acontece na consulta; tem pouco dinheiro.
- **Pergunta de esclarecimento:** dispensável; responda direto.
- **Resposta-base:**
  > Na consulta, [QUEM FAZ A CONSULTA] analisa a sua situação com calma, olha os documentos e explica os caminhos possíveis, com tempo só para isso ([DURAÇÃO]). [SE ABATE: Se você decidir seguir com o escritório, o valor da consulta é descontado dos honorários.]
- **Nunca:** dar uma orientação por mensagem para "provar" que vale a pena; falar dos escritórios que não cobram.
- **Vai para o advogado quando:** a pessoa conta que não tem renda (critério de valor reduzido ou de encaminhamento à Defensoria, conforme a política e a ficha).

## 9. "Dá para garantir que eu ganho?"

- **O que pode estar por trás:** medo de pagar e perder; quer segurança; ouviu promessa de outro lugar.
- **Pergunta de esclarecimento:** dispensável; responda com honestidade.
- **Resposta-base:**
  > Eu entendo a pergunta, e vou te responder com sinceridade: nenhum advogado pode garantir o resultado, porque quem decide é o [ÓRGÃO | JUIZ]. O que a gente garante é o trabalho: [ITENS DO INCLUÍDO] e te manter informado em cada etapa. Na consulta, [QUEM FAZ A CONSULTA] explicou os pontos fortes e os riscos do seu caso; se quiser, revemos isso juntos.
- **Nunca:** percentual de chance; "seu caso é ganho"; "nunca perdi um caso assim".
- **Vai para o advogado quando:** a pessoa quer rediscutir a avaliação do caso (é conversa de advogado, não de mensagem).

---

## Objeções que o escritório acrescenta

Use o mesmo formato: o que pode estar por trás, pergunta de esclarecimento, resposta-base, nunca, vai para o advogado quando. Fontes boas: `motivos_de_perda_comuns` da ficha e as conversas que travaram no último mês.

## Histórico

(uma linha por mudança: data, objeção, o que mudou, quem aprovou)
