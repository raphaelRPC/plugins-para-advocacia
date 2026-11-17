# Casos fictícios para treinar e testar

Três casos do Escritório Modelo, com documentos de mentira, uma minuta com erros de propósito, uma pesquisa de exemplo, uma base de partes e um lote. Servem para testar as habilidades antes de usar caso real, para treinar a equipe e para quem usa conta pessoal de IA. Nenhuma pessoa, número, processo, julgado ou súmula daqui existe. Os números de julgado e de súmula são inventados de propósito e precisam sair vermelhos na conferência.

**Treino não entra no registro real.** Tudo o que for feito com estes casos grava em `escritorio/07-operacao/_treino/juridico/`.

## O Escritório Modelo

Belo Horizonte/MG. Uma advogada titular, que revisa, assina e protocola, e um estagiário, que faz a primeira minuta. Previdenciário, trabalhista e família. Tribunais principais: Juizado Especial Federal de BH, TRF da 6ª Região, TRT da 3ª Região e TJMG. Sistemas: PJe e eproc. Pesquisa de jurisprudência no Jus IA. Conferência vale 90 dias. Os códigos são os mesmos dos outros plugins motor.

## Caso 1 · Marta · C-2026-0001 · previdenciário

Auxílio por incapacidade temporária cessado; ela segue sem condição de trabalhar. Peça: petição inicial de restabelecimento no Juizado Especial Federal.

| Doc | Documento (fictício) | O que diz |
|---|---|---|
| D1 | Carta de cessação do benefício | Benefício cessado em **2026-02-28**, por "não constatação de incapacidade" |
| D2 | Comunicação de decisão do pedido de prorrogação | Pedido de prorrogação negado; menciona cessação em **2026-03-05** |
| D3 | Extrato de vínculos e contribuições (CNIS) | Último vínculo de 2019-06 a 2025-09, auxiliar de cozinha; contribuições em dia |
| D4 | Relatório do médico assistente de 2026-01-20 | Diz que ela segue sem condição para atividade com esforço físico, sem prazo de melhora |
| D5 | Resumo da perícia administrativa | Perito conclui capacidade; não menciona o relatório D4 |
| D6 | Carteira de trabalho (páginas) | Função de auxiliar de cozinha |

**O que o dossiê precisa achar:** a contradição de data entre D1 e D2; que a perícia (D5) não enfrentou o relatório D4; que falta relatório médico atual (posterior à cessação); que a função exige esforço físico (D3 e D6 batem).

## Caso 2 · Paulo · C-2026-0002 · trabalhista

Dispensado sem justa causa; verbas rescisórias não pagas. Empregador: **Restaurante Sabor Mineiro Ltda.** (fictício). Peça: reclamação trabalhista.

| Doc | Documento (fictício) | O que diz |
|---|---|---|
| T1 | Termo de rescisão | Admissão em **2022-03-01**, dispensa em 2026-03-09, verbas "a pagar" |
| T2 | Carteira de trabalho | Admissão registrada em **2022-05-02** |
| T3 | Três holerites | Salário fixo e horas extras pagas em dois deles |
| T4 | Mensagens com o gerente | O gerente diz que "o acerto sai no fim do mês" |

**O que o dossiê precisa achar:** a divergência na data de admissão (T1 contra T2), possível período sem registro; o reconhecimento da dívida na mensagem (T4).

## Caso 3 · Renata · C-2026-0005 · família

Divórcio consensual com partilha de um imóvel e um carro; sem filhos menores. Peça: petição de divórcio consensual. Documentos: certidão de casamento, matrícula do imóvel, documento do carro e um esboço do acordo em que a partilha do carro aparece em duas versões diferentes (as duas versões estão em `skills/comparar-versoes/assets/`). Os documentos de texto dos casos 1 e 2 estão em `skills/dossie-do-caso/assets/documentos-de-treino.md`, e os autos fictícios da Marta em `skills/leitura-dos-autos/assets/autos-de-treino.md`.

## A minuta com erros (para `conferir-peca` e `conferir-citacoes`)

Minuta fictícia da petição inicial da Marta, versão 1, com estes erros plantados:

| # | Erro plantado | Quem deve achar |
|---|---|---|
| 1 | No item 4 dos fatos, aparece "o autor **Paulo**" (sobra de outra peça) | `conferir-peca` |
| 2 | Gênero trocado: "o requerente" em três trechos e "a requerente" no resto | `conferir-peca` |
| 3 | Data de cessação 2026-02-28 nos fatos e 2026-03-05 nos pedidos | `conferir-peca` (e o dossiê já apontou a contradição) |
| 4 | Valor da causa diferente no cabeçalho e no fecho | `conferir-peca` |
| 5 | Pedido de dano moral sem nenhum fundamento nos fatos | `conferir-peca` |
| 6 | "Conforme doc. 7" sem documento 7 na lista | `conferir-peca` |
| 7 | "Súmula 999 do TRF6" | `conferir-citacoes`: vermelho (não existe) |
| 8 | Julgado citado sem número nem data ("conforme entendimento pacífico do STJ") | `conferir-citacoes`: amarelo ou vermelho (sem fonte) |
| 9 | Trecho de lei entre aspas com palavras trocadas | `conferir-citacoes`: amarelo (aspas não batem) |
| 10 | Um artigo da Lei 8.213/1991 citado sem conferência | `conferir-citacoes`: conferir na fonte |

O texto da minuta fica em `skills/conferir-peca/assets/minuta-com-erros.md`, e o gabarito é esta tabela.

## A pesquisa de exemplo (para `trazer-pesquisa`)

Um resultado colado de pesquisa no Jus IA sobre "restabelecimento de benefício por incapacidade quando a perícia não analisa o relatório do médico assistente", com três julgados **inventados**, marcados como exemplo: um de turma recursal, um do TRF6 e um contrário à tese. Fica em `skills/trazer-pesquisa/assets/pesquisa-de-exemplo.md`. O teste: os três viram fichas, todos ficam "não conferido", o contrário entra marcado "contra", e nenhum é usado em peça sem a conferência.

## A base de partes (para `conflito-de-interesses`)

| Parte | Papel | Caso |
|---|---|---|
| Restaurante Sabor Mineiro Ltda. | cliente (consultivo trabalhista, 2025) | C-2025-0071 |
| Jorge | cliente | C-2025-0088 |
| Sueli | cliente | C-2025-0091 |

**O teste:** o caso 2 (Paulo contra o Restaurante Sabor Mineiro) acusa conflito, porque o restaurante foi cliente do escritório. A habilidade para e leva a decisão para a advogada.

## O lote (para `pecas-em-lote`, se instalada)

Cinco segurados fictícios (códigos C-2026-9001 a C-2026-9005) com a mesma situação (benefício cessado, pedido de prorrogação negado), numa planilha com nome curto, data de cessação, função e documentos. Um deles com a data de cessação faltando e outro com área diferente (trabalhista), para a conferência barrar. A planilha e as colunas estão em `skills/pecas-em-lote/assets/`, se a habilidade estiver instalada.

## Como usar no teste

1. Rode a habilidade com o material do caso, sem mostrar o gabarito.
2. O que não pode falhar: os erros 1 a 10 da minuta achados; a Súmula 999 vermelha; nenhum julgado da pesquisa de exemplo usado sem conferência; o conflito do caso 2 acusado; o lote sem as duas linhas com problema; nenhuma escolha de tese feita pela IA.
3. Quando o escritório tiver casos próprios, troque estes por casos reais anonimizados em `escritorio/04-base/casos-de-teste/juridico/`.
