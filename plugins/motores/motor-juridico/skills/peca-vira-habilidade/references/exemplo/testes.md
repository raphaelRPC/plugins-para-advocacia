---
documento: Testes da habilidade peticao-inicial-restabelecimento
versao: 1
revisado_em: 2026-04-16
dono: advogada titular
---

# Testes · peticao-inicial-restabelecimento · versão 1 da habilidade

> Exemplo resolvido, fictício. No escritório, este arquivo fica em `escritorio/04-base/casos-de-teste/juridico/peticao-inicial-restabelecimento-testes.md`. Os três casos rodaram em `escritorio/07-operacao/_treino/juridico/`. "O que saiu" está copiado do que a habilidade entregou, sem corrigir.

## Caso 1 · comum
Entrada: C-2026-9001 (treino, Jair, linha 1 do lote de treino), tese definida pela advogada em 2026-04-16; dossiê com os cinco documentos; relatório médico de 05/12/2025, cessação em 10/01/2026; sem tutela.
Esperado: monta a peça inteira pelo modelo (A); "o autor" em todo o texto; as duas citações marcadas `[CONFERIR]`; sem o item 1.6, sem o 2.4 e sem o pedido de tutela; qualificação como campo de quem protocola; o relatório anterior à cessação vira "pedir relatório atual" no "Antes de protocolar".
O que saiu: minuta `casos/C-2026-9001/minutas/peticao-inicial-restabelecimento-v1.md` com 5 fatos, 3 fundamentos, 3 pedidos numerados de 1 a 3, "o autor" nas três menções, 2 marcas `[CONFERIR]` (art. 59 e o julgado das peças de origem), `{QUALIFICAÇÃO COMPLETA}` e `{DATA DO PROTOCOLO}`; no cabeçalho interno, "pedir relatório médico atual (o de 05/12/2025 é anterior à cessação)".
Resultado: passou

## Caso 2 · com exceção
Entrada: C-2026-0001 (caso 1 dos casos fictícios, Marta). A carta de cessação (D1) diz 28/02/2026 e a comunicação da prorrogação (D2) diz 05/03/2026; o relatório médico (D4) é de 20/01/2026; função auxiliar de cozinha.
Esperado: monta, mas não escolhe a data: `[A CONFIRMAR: data de cessação; doc. 1 diz 28/02/2026 e doc. 2 diz 05/03/2026]` no fato 1.2; a contradição e o pedido de relatório atual no "Antes de protocolar"; nenhum diagnóstico na peça; "a autora" em todo o texto.
O que saiu: minuta v1 com o fato 1.2 marcado `[A CONFIRMAR]` citando os dois documentos, "a autora" nas três menções, a limitação descrita só como "sem condição para atividade com esforço físico"; no cabeçalho interno, "decidir a data de cessação (D1 x D2)" e "pedir relatório médico posterior à cessação". O script de .docx da minutar-peca respondeu "NÃO ESTÁ PRONTA" e não criou o .docx.
Resultado: passou

## Caso 3 · deve parar
Entrada: C-2026-0002 (caso 2 dos casos fictícios, Paulo), trabalhista, reclamação trabalhista contra o Restaurante Sabor Mineiro; o pedido foi "usa a de restabelecimento, é só trocar os dados".
Esperado: para antes de escrever; nenhuma minuta; diz que esta habilidade só faz a inicial de restabelecimento do previdenciário e que a reclamação trabalhista vai para a `minutar-peca`, depois da tese definida (e da checagem de conflito de interesses, porque o restaurante foi cliente).
O que saiu: "Parei: esta habilidade só faz a petição inicial de restabelecimento (previdenciário). O caso C-2026-0002 é trabalhista. A reclamação vai para a minutar-peca depois que a advogada definir a tese; antes, a conflito-de-interesses, porque o Restaurante Sabor Mineiro aparece na base de partes." Nenhum arquivo gravado.
Resultado: passou

Conferido por: advogada titular em 2026-04-16
