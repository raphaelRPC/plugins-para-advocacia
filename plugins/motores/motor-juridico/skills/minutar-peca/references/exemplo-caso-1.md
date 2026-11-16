# Exemplo resolvido · minuta da Marta (caso 1, fictício)

Caso 1 de `../../docs/casos-ficticios.md`: Marta, C-2026-0001, auxílio por incapacidade temporária cessado. A advogada titular do Escritório Modelo definiu a tese `restabelecimento-incapacidade` na `estrategia.md` (etapa `tese-definida`). Não há habilidade própria da peça, então a `minutar-peca` redige. Tudo grava em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md`.

Leia este exemplo para ver três coisas: como a contradição de datas do dossiê (D1 diz 2026-02-28, D2 diz 2026-03-05) fica marcada em vez de escolhida; como a falta de relatório médico atual vai para o "Antes de protocolar"; e como cada citação nasce marcada. Nenhum número de julgado daqui existe.

## O que a habilidade leu

| Fonte | O que deu à minuta |
|---|---|
| `casos/C-2026-0001/dossie.md` | Linha do tempo, matriz fato x prova, a contradição D1 x D2, a perícia (D5) que não enfrentou o relatório (D4), a falta de relatório atual, função com esforço físico (D3 e D6) |
| `casos/C-2026-0001/estrategia.md` | Tese e caminho definidos pela advogada: restabelecimento desde a cessação, prova pericial judicial, sem pedido de dano moral |
| `04-base/juridico/teses/restabelecimento-incapacidade.md` | Fundamento e a ordem dos argumentos; o julgado da base com conferência vencida volta a ser marcado |
| `04-base/juridico/modelos/peticao-inicial/` | Estrutura e trechos do escritório (endereçamento, qualificação, fecho) |
| Ficha jurídica | Pedidos numerados com o fundamento ao lado; citação em recuo; fonte com serifa, corpo 12 |

## A minuta (como sai)

```markdown
---
documento: Minuta · peticao-inicial · C-2026-0001
versao: 1
gerado_em: 2026-04-14
caso: C-2026-0001
peca: peticao-inicial
tese: restabelecimento-incapacidade
habilidade_usada: minutar-peca
redigiu: estagiário (primeira minuta) · A
fontes: dossie.md v1; estrategia.md (tese definida em 2026-04-13); teses/restabelecimento-incapacidade.md v2; modelos/peticao-inicial/modelo-jef.md
---

## Antes de protocolar (interno)

- Quem revisa e quem assina: advogada titular · H
- Tese e caminho: definidos pela advogada titular em 2026-04-13 (estrategia.md).
- Citações: 3 marcadas [CONFERIR] (itens 2.1, 2.2 e 2.3).
- Contradição do dossiê: data de cessação. D1 diz 2026-02-28; D2 diz 2026-03-05. A peça usa a marca no lugar da data até a advogada decidir qual vale e como explicar a outra.
- Falta relatório médico posterior à cessação (o D4 é de 2026-01-20). Pedir à cliente antes de protocolar (dossie-do-caso, "o que pedir").
- Dado sensível: o diagnóstico do D4 não entrou na peça; a peça fala só da limitação para esforço físico.
- Documentos citados: doc. 1 (D1), doc. 2 (D2), doc. 3 (D3), doc. 4 (D4), doc. 5 (D5), doc. 6 (D6).
- [ ] Citações conferidas na fonte, sem vermelho nem cinza (conferir-citacoes)
- [ ] Dados do cliente, datas, valores, gênero e documentos conferidos (conferir-peca)
- [ ] Requisitos da inicial no Juizado Especial Federal conferidos [CONFERIR]
- [ ] Lida e ajustada pela advogada (etapa revisada)
<!-- fim: antes de protocolar -->

# EXCELENTÍSSIMO SENHOR JUIZ FEDERAL DO JUIZADO ESPECIAL FEDERAL DE BELO HORIZONTE/MG

MARTA [SOBRENOME], [QUALIFICAÇÃO], vem, por sua advogada, propor AÇÃO DE RESTABELECIMENTO DE BENEFÍCIO POR INCAPACIDADE TEMPORÁRIA contra o INSTITUTO NACIONAL DO SEGURO SOCIAL, pelos fatos e fundamentos a seguir.

## 1. DOS FATOS

1.1. A autora trabalhou como auxiliar de cozinha de 06/2019 a 09/2025, com contribuições em dia (doc. 3 e doc. 6).

1.2. Recebia auxílio por incapacidade temporária, cessado em [A CONFIRMAR: data de cessação; doc. 1 diz 28/02/2026 e doc. 2 diz 05/03/2026] por "não constatação de incapacidade" (doc. 1).

1.3. O pedido de prorrogação foi negado (doc. 2).

1.4. O relatório do médico assistente de 20/01/2026 diz que a autora segue sem condição para atividade com esforço físico, sem prazo de melhora (doc. 4).

1.5. A perícia administrativa concluiu pela capacidade sem mencionar esse relatório (doc. 5).

## 2. DOS FUNDAMENTOS

2.1. O benefício é devido enquanto durar a incapacidade para a atividade habitual, nos termos do art. 59 da Lei 8.213/1991 [CONFERIR: vigência e redação na data dos fatos].

2.2. A conclusão pericial que não enfrenta o relatório do médico assistente não afasta a prova da incapacidade, como decidiu o [TRIBUNAL], [CLASSE] nº [NÚMERO], Rel. [NOME], julgado em [DATA] [CONFERIR: julgado da base com conferência vencida; conferir no Jus IA e no inteiro teor].

2.3. A função de auxiliar de cozinha exige esforço físico contínuo (doc. 6), o que torna a limitação do doc. 4 incompatível com a atividade habitual. [CONFERIR: requisito de incapacidade para a atividade habitual no entendimento atual da base]

## 3. DOS PEDIDOS

Diante do exposto, requer:

1. O restabelecimento do benefício desde a cessação, com fundamento no item 2.1 e nos fatos 1.2 a 1.5.
2. A realização de perícia médica judicial, com fundamento no item 2.2 e no fato 1.5.
3. O pagamento das parcelas vencidas desde a cessação, com correção, com fundamento no item 2.1.

## 4. DAS PROVAS

Documentos 1 a 6, perícia médica judicial e o relatório médico atual, a juntar.

## 5. DO VALOR DA CAUSA

[A DEFINIR: valor da causa pela conta das parcelas; conferir a regra de valor do Juizado Especial Federal]

Belo Horizonte, {DATA DO PROTOCOLO}.

Advogada titular do Escritório Modelo, OAB/MG [NÚMERO]
```

## O que o script de .docx diz sobre esta minuta

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" "escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/peticao-inicial-v1.md" --padrao "escritorio/04-base/juridico/padrao-visual.md"
```

A primeira linha sai "NÃO ESTÁ PRONTA", com as três citações por conferir, a data de cessação `[A CONFIRMAR]`, o valor da causa `[A DEFINIR]`, os campos `[SOBRENOME]`, `[QUALIFICAÇÃO]` e `[NÚMERO]`, o molde do julgado e as quatro conferências do "Antes de protocolar" sem marcar. Nenhum .docx é criado. É o resultado certo: a minuta vai para a fila com o relatório, e a advogada decide a data, o valor e o que fica.

Depois da conferir-citacoes (o art. 59 verde; o julgado trocado por um conferido no Jus IA, verde; o item 2.3 reescrito sem citação), da decisão da advogada sobre a data e da qualificação preenchida, o mesmo comando diz "PRONTA PARA GERAR O .DOCX" (só falta `{DATA DO PROTOCOLO}`, que quem protocola preenche) e cria o .docx no padrão visual.

## O que não pode acontecer neste caso

| Erro | Por que é grave |
|---|---|
| Escolher 2026-02-28 ou 2026-03-05 sozinha | A data muda as parcelas e a contradição pode ser usada pela outra parte |
| Completar o julgado da base de memória porque "deve ser esse" | Citação inventada é o pior erro do plugin (`../../docs/citacoes.md`, regra 4) |
| Pedir dano moral porque "costuma entrar" | A estratégia não pediu e não há fato para isso (erro 5 da minuta de treino) |
| Copiar o diagnóstico do relatório médico na peça | Dado de saúde além do necessário |
