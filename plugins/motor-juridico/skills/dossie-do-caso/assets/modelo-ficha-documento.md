---
doc: D1
arquivo: [nome do arquivo no lote]
tipo: [o que é o documento, em poucas palavras]
data_do_documento: AAAA-MM-DD
autor: [quem produziu: INSS, empregador, médico assistente, cliente, outra parte]
situacao: lido            # lido | lido-em-parte | ilegivel
paginas_lidas: 1-2 de 2
lido_em: AAAA-MM-DD
---

# D1 · [tipo do documento]

## Fatos

Um fato por linha, do jeito que o documento diz. Sem interpretar e sem completar. A `chave` é curta, com hífen, e se repete igual em todo documento que fala do mesmo fato (por exemplo `cessacao-do-beneficio`, `admissao`, `dispensa`, `pericia-administrativa`). É pela chave que o script cruza as datas. Período: data de início em `data` e de fim em `ate`.

- A `data` é a do fato, não a do documento. A mensagem de 2026-03-20 que diz "trabalho aqui desde março de 2022" entra com `03/2022` na chave `admissao`, e o `onde` diz "mensagem de 20/03".
- Fato que se repete por mês (horas extras de cada holerite) pode usar a mesma chave dentro do mesmo documento. Em documentos separados, ponha o período na chave (`horas-extras-2025-12`), para o script não ver contradição onde há repetição.
- Versão de uma parte (o cliente diz, o gerente diz) fica escrita assim no `fato`.

| data | ate | chave | fato | onde |
|---|---|---|---|---|
| AAAA-MM-DD | | [chave] | [o que o documento diz] | p. 1 |

## O que este documento prova

- [fato do caso] · [como prova: diretamente, indiretamente, só a versão de uma parte]

## O que ele não diz, e devia dizer

- [por exemplo: a perícia não menciona o relatório do médico assistente]

## Dado sensível

- [dado de saúde, de criança, de renda, de terceiro] · [vai à peça | só o mínimo | não vai] · o advogado decide

## Dúvidas para o advogado

- [o que não deu para entender ou precisa de confirmação]
