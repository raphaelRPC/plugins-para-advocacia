# Mensagens do resumo mensal (modelos crus)

Use quando a biblioteca do escritório (`escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`) não tiver o modelo da chave. Se tiver (no plugin `inicio-automacao`, `resumo-mensal` é o modelo 9), o da biblioteca vale. Os textos estão num tom de exemplo e são reescritos no tom da ficha e do nicho antes de sair. Nenhuma marcação vai ao cliente: campo que não se sabe sai da mensagem e vai para o "Antes de enviar" do resumo.

Esta habilidade é dona das chaves `resumo-mensal` e `resumo-mensal-anexo`.

## Resumo em mensagem
- **Chave:** `resumo-mensal`
- **Quando:** ficha com `resumo_mensal` em mensagem; todo cliente com `resumo_mensal = sim`, inclusive o de processo parado.
- **Quem lê:** `quem_le_antes_de_enviar`. **Sigla:** A.
```
Oi, [NOME]! Aqui vai o resumo de [MÊS] do seu caso.

Em que pé está: [FASE EM PALAVRAS SIMPLES].
O que aconteceu: [O QUE ACONTECEU, OU O QUE ESTÁ SENDO ESPERADO].
O que o escritório fez: [O QUE FOI FEITO].
O que vem agora: [PRÓXIMA ETAPA, SEM DATA DE DECISÃO].
O que depende de você: [AÇÃO E PRAZO, OU "nada por enquanto"].

O próximo resumo chega até o dia [DIA] de [MÊS]. Se acontecer algo importante antes, a gente te avisa.

[ASSINATURA]
```
- **Nunca usar quando:** houve no mês notícia ruim ainda não dada por ligação; o cliente pediu para não receber; o cliente está insatisfeito ou com reclamação aberta (uma pessoa fala antes).

## Mensagem que acompanha o arquivo ou o link
- **Chave:** `resumo-mensal-anexo`
- **Quando:** ficha com `resumo_mensal` em PDF ou página do caso. Vai junto com o arquivo, pelo canal oficial, ou com o link da página.
- **Quem lê:** quem envia confere nome, mês e anexo. **Sigla:** S depois de aprovado (não traz conteúdo do processo).
```
Oi, [NOME]! Segue o resumo de [MÊS] do seu caso, com o que aconteceu, o que o escritório fez e o que vem agora. Se ficar alguma dúvida, é só me escrever aqui.

[ASSINATURA]
```
Com a página do caso por link, a primeira frase vira: "Oi, [NOME]! A página do seu caso foi atualizada com o resumo de [MÊS]: {LINK DA PÁGINA}". O `{LINK DA PÁGINA}` é campo do envio: quem envia cola o link na hora, e a fila não deixa marcar como enviado com a chave no texto.
- **Nunca usar quando:** o arquivo ainda tem pendência no "Antes de enviar"; a página do caso não foi aprovada por `quem_aprova_publicar`.
