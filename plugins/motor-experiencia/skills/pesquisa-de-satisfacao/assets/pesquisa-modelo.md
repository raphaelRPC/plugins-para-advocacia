# Modelo da pesquisa e do registro do mês

Textos de partida, no tom de exemplo. Reescreva no tom da ficha e do nicho antes de usar. Toda mensagem aqui é A: alguém lê antes de enviar.

## 1. A mensagem da pesquisa

Chave na biblioteca: `pesquisa-de-satisfacao`.

```
Oi, [NOME]! Tudo bem?

Queria te fazer três perguntas rápidas sobre como tem sido o nosso cuidado com você. Pode responder por aqui mesmo, do jeito que quiser. Quem lê é [FUNÇÃO], pessoalmente.

1. De 0 a 10, como você avalia o cuidado do escritório com você até aqui?
2. O que a gente fez que mais te ajudou?
3. O que a gente pode fazer melhor?

Obrigada pelo seu tempo.
[ASSINATURA]
```

Variação para o encerramento: troque "até aqui" por "no seu caso".
Variação para público com pouca leitura (modo adaptar): a pergunta 1 vira "Para você, o nosso cuidado foi: ruim, mais ou menos, bom ou muito bom?". No registro, anote a correspondência usada pelo escritório (por exemplo, ruim = 3, mais ou menos = 6, bom = 8, muito bom = 10 `[A DEFINIR]`).

## 2. Agradecimentos

Chave: `pesquisa-agradecimento`.

Nota alta:
```
Obrigada, [NOME]! Fico muito feliz de saber. Qualquer coisa, estamos por aqui.
```

Nota média, com sugestão:
```
Obrigada, [NOME], pela sinceridade. Anotei o que você falou sobre [ASSUNTO]. A partir de agora, [O QUE MUDA, em uma frase, só se for verdade].
```

Nota baixa: não há mensagem pronta. Uma pessoa liga (passo 6 da habilidade).

## 3. Pedido de avaliação pública (só se a ficha disser)

Chave: `pedido-de-avaliacao`. Só no encerramento, só se `pede_avaliacao_publica` for "sim, no encerramento", e só depois de o advogado conferir com o Provimento 205/2021 e o Código de Ética e Disciplina `[CONFERIR]` (a conferência fica no cabeçalho interno do rascunho, nunca no texto).

```
[NOME], se você quiser contar como foi a sua experiência com o escritório, pode deixar uma avaliação em [ONDE, ex.: nosso perfil no Google]. É totalmente opcional, e o que você escrever é seu.
```

Nunca: oferecer algo em troca, sugerir nota ou texto, mandar só para quem deu nota alta, insistir, pedir para quem tem reclamação aberta.

## 4. O registro do mês

Arquivo `escritorio/07-operacao/experiencia/pesquisas/AAAA-MM.md`. O script `resumo_pesquisa.py` lê a tabela abaixo. Nome das colunas como está (o script aceita maiúsculas e acentos).

```markdown
---
documento: Pesquisa de satisfação AAAA-MM
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Pesquisa de satisfação · AAAA-MM

| data | codigo | momento | nota | o_que_ajudou | o_que_melhorar | retorno | situacao |
|---|---|---|---|---|---|---|---|
| AAAA-MM-DD | C-AAAA-NNNN | 30-dias-do-contrato | | | | | enviada |

## Resumo do mês
(saída do script, colada aqui)

## Leitura do mês
- Três leituras: ...
- Três ações: ...
```

Regras do registro:
1. **momento:** use os nomes da `pesquisa_quando` (por exemplo, `30-dias-do-contrato`, `depois-da-audiencia`, `depois-da-pericia`, `encerramento`).
2. **nota:** número de 0 a 10. Vazia enquanto não houver resposta.
3. **comentários:** anonimizados, sem nome de outra pessoa, sem dado de saúde, sem número de processo. Se o cliente citar alguém da equipe, escreva a função.
4. **retorno:** para nota baixa, quem ligou, quando e o que foi combinado em uma frase.
5. **situacao:** `enviada`, `respondida`, `sem-resposta` (passou o prazo da ficha), `retorno-feito`.
6. **Treino** grava em `escritorio/07-operacao/_treino/experiencia/pesquisas/`.
