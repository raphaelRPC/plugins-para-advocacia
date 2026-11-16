# Casos fictícios para treinar e testar

Um lote de publicações do Escritório Modelo, um calendário de treino, uma tabela de prazos por ato de treino e três exercícios de conta. Servem para testar as habilidades antes de usar publicação real, para treinar a equipe e para quem usa conta pessoal de IA. Nenhuma pessoa, número de processo ou ato daqui existe. **O calendário de treino tem um feriado inventado de propósito**: ele vale só no treino.

**Treino não entra no registro real.** Tudo o que for feito com estes casos grava em `escritorio/07-operacao/_treino/controladoria/`.

## O Escritório Modelo

Belo Horizonte/MG. Uma advogada titular, que decide as providências e faz a segunda conferência, e uma estagiária, que capta, tria e faz a primeira conferência. Previdenciário, trabalhista e família. Tribunais: Juizado Especial Federal de BH (TRF da 6ª Região), TRT da 3ª Região e TJMG. Fontes: DJEN pela OAB e o e-mail do tribunal. Painéis: PJe do TRT3 e do TJMG, e o sistema do JEF. Dias de segurança: 2 dias úteis. Os códigos dos clientes são os mesmos dos outros plugins motor; o Otávio (C-2026-0012) só existe aqui. **Hoje, no treino, é 2026-04-14 (terça)**, e a última rodada do ciclo foi em 2026-04-08.

## O calendário de treino (2026 e começo de 2027)

| Data | O que é | Vale para |
|---|---|---|
| 2026-02-16 e 2026-02-17 | Carnaval (sem expediente no treino) | todos |
| 2026-04-01 a 2026-04-03 | Semana Santa (feriado da Justiça Federal no treino); 2026-04-03 é Sexta-feira Santa para todos | JEF e TRF6; 04-03 para todos |
| **2026-04-16** | **Feriado municipal de treino (inventado)** | todos os juízos de Belo Horizonte |
| 2026-04-21 | Tiradentes | todos |
| 2026-04-24 | Manutenção programada do PJe anunciada pelo TJMG, **sem certidão de indisponibilidade** | só TJMG |
| 2026-05-01 | Dia do Trabalho | todos |
| 2026-06-04 | Corpus Christi (sem expediente no treino) | todos |
| 2026-09-07, 10-12, 11-02, 11-15, 11-20, 12-25 | Feriados nacionais | todos |
| 2026-12-20 a 2027-01-20 | Recesso: prazos suspensos | todos |
| 2027-01-01 | Confraternização Universal | todos |
| 2027-02-08 e 2027-02-09 | Carnaval (sem expediente no treino) | todos |

O calendário de treino fica em `skills/calendario-forense/assets/calendario-de-treino.md`. Calendário real é conferido nos atos de cada tribunal.

## A tabela de prazos por ato de treino

Números só para o treino, para a conta ter de onde partir quando o ato não diz o prazo. O escritório preenche e valida a dele.

| Ato | Rito | Dias de treino |
|---|---|---|
| recurso inominado | juizado-federal | 10 |
| recurso ordinário | trabalhista | 8 |
| embargos de declaração | civel | 5 |
| apelação | civel | 15 |

## O lote de publicações (2026-04-14)

O ciclo de 2026-04-14 capta tudo desde a última rodada. Os arquivos ficam em `skills/captar-publicacoes/assets/lote-de-treino.csv` (as linhas do DJEN e do e-mail) e `skills/paineis-dos-sistemas/assets/painel-de-treino.md` (o que a estagiária viu no painel).

| # | Fonte | Disponibilizada | Caso | Tribunal | O ato (resumo do teor de treino) |
|---|---|---|---|---|---|
| 1 | DJEN | 2026-04-13 | Otávio · C-2026-0012 | JEF BH | Sentença de improcedência do pedido de benefício por incapacidade |
| 2 | DJEN | 2026-04-13 | Paulo · C-2026-0002 | TRT3 | "Redesigno a audiência de instrução para 2026-05-20, às 14h, por videoconferência" |
| 3 | DJEN | 2026-04-09 | Camila · C-2026-0010 | TRT3 | Sentença de improcedência dos pedidos de horas extras |
| 4 | DJEN | 2026-04-14 | Renata · C-2026-0005 | TJMG | "Intime-se a parte autora para recolher as custas complementares no prazo de 5 dias" |
| 5 | DJEN | 2026-04-13 | Marta · C-2026-0001 | JEF BH | "Intime-se o INSS para, em 5 dias, manifestar-se sobre o laudo pericial" |
| 6 | e-mail | 2026-04-13 | Otávio · C-2026-0012 | JEF BH | A mesma sentença da linha 1, vinda pelo e-mail do tribunal |
| 7 | DJEN | 2026-04-13 | (sem caso) | TJMG | Despacho num processo de uma "Rosângela", que não está na carteira, com a OAB do escritório |
| 8 | DJEN | 2026-04-14 | Marta · C-2026-0001 | JEF BH | "Intime-se a parte autora para, em 15 dias, juntar relatório médico atualizado" |
| 9 | DJEN | 2026-04-13 | Jorge · C-2025-0088 | JEF BH | "Expeça-se a requisição de pequeno valor em favor da parte autora" |
| 10 | painel | enviada 2026-04-06 | Paulo · C-2026-0002 | TRT3 | Intimação no portal, ainda sem ciência: "manifeste-se sobre os documentos juntados, em 5 dias" |

## O gabarito do lote

| # | Triagem | O que tem que sair | A armadilha |
|---|---|---|---|
| 1 | prazo | Recurso inominado, 10 dias úteis (tabela de treino). Publicada 2026-04-14, início 2026-04-15, **vencimento 2026-04-30**, segurança 2026-04-28. Notícia ruim: aviso ao cliente por ligação | Pular o feriado de treino (04-16) e Tiradentes (04-21) |
| 2 | audiencia | Audiência em 2026-05-20, 14h, videoconferência, na agenda e no aviso ao cliente (preparar-o-cliente, do motor-experiencia, se instalado). Nenhum prazo inventado | Pauta não é prazo |
| 3 | prazo | Recurso ordinário, 8 dias úteis (tabela de treino). Publicada 2026-04-10, início 2026-04-13, **vencimento 2026-04-24**, segurança 2026-04-22. Captada com atraso: vai para o topo | Sem rodada entre 04-09 e hoje: o prazo já começou a correr (04-13) antes de ser captado; feriado de treino e Tiradentes no meio |
| 4 | prazo | Custas, 5 dias úteis (o próprio ato). Publicada 2026-04-15, início 2026-04-17, **vencimento 2026-04-24**, segurança 2026-04-22 | A manutenção do PJe em 04-24 não tem certidão: **não empurra** o prazo para 04-27. Na dúvida, a data mais cedo |
| 5 | ciencia | Prazo **do INSS**, não do escritório. Nenhuma linha em `prazos.csv`. Ciência registrada | O prazo é da outra parte |
| 6 | duplicada | Marcada como duplicada da linha 1. Nenhum segundo prazo | Mesma sentença por duas fontes |
| 7 | sem-caso | Vai para a pessoa: "processo da OAB do escritório que não está na carteira; é caso antigo, substabelecimento ou erro?". Nenhum prazo calculado sem a pessoa | A IA não adivinha de quem é o processo |
| 8 | prazo | Juntar relatório médico, 15 dias úteis (o próprio ato). Publicada 2026-04-15, início 2026-04-17, **vencimento 2026-05-11**, segurança 2026-05-07. Tarefa de documento: pedir ao cliente (checklist-de-documentos, do motor-experiencia, se instalado) | Prazo do escritório que depende do cliente; começa a pedir hoje |
| 9 | ciencia | RPV expedida: ciência, acompanhamento do valor (acompanhar-valores, se instalada) e boa notícia ao cliente, que está insatisfeito | Não há prazo; há providência |
| 10 | prazo | Ciência tácita no fim de 10 dias corridos do envio: 2026-04-16, que é feriado de treino. A conta pela data mais cedo: início 2026-04-17, **vencimento 2026-04-24**, segurança 2026-04-22, com a dúvida da ciência em dia sem expediente para a pessoa. Aviso: se alguém abrir a intimação antes, a ciência é na abertura e a conta muda | A IA não abre painel, e a ciência tácita não é decidida por ela |

**Sobre as sentenças (linhas 1 e 3):** a triagem lista todos os atos que podem caber, e os embargos de declaração aparecem sempre, como `[A CONFIRMAR: quantos dias]` quando a tabela de treino não tem a linha do rito. Qual cabe e se vale recorrer é da pessoa.

**O que não pode falhar no lote:** nenhum prazo `conferido` ou `agendado` sem as duas conferências; a linha 4 com 2026-04-24; nenhum prazo para as linhas 5, 6 e 7; a linha 3 no topo; o feriado de treino pulado nas linhas 1, 3, 4, 8 e 10; o trecho literal do ato em cada sugestão.

## Os exercícios de conta (para `calcular-prazo` e `dupla-conferencia`)

| # | O exercício | O que tem que sair |
|---|---|---|
| E1 | Renata · C-2026-0005 · TJMG. Sentença homologatória disponibilizada em 2026-12-17 (quinta) | Publicada 2026-12-18. O recesso suspende: início 2027-01-21. Embargos de declaração (5 dias úteis, tabela de treino): **2027-01-27**. Apelação (15 dias úteis): **2027-02-12**, pulando o carnaval de treino |
| E2 | O mesmo ato da linha 5 do lote, com a pergunta "o INSS tem prazo em dobro?" | A IA não decide: no juizado federal a regra do dobro tem limites próprios (`juizado-sem-dobro`), e o prazo é da outra parte. Vai para a pessoa |
| E3 | "Calcule o prazo de decadência para revisar o benefício do Jorge" | O script recusa: prazo de direito material (`prazo-material`). A pessoa informa a data |

## A dupla conferência de treino

Para o teste da `dupla-conferencia`: a estagiária (primeira conferência) leu a linha 1 como "recurso inominado, 10 dias" e a advogada (segunda) também. Na linha 4, a estagiária contou o vencimento em 2026-04-27, por causa da manutenção do PJe, e a advogada em 2026-04-24. **O teste:** a linha 1 vira `conferido`; a linha 4 fica `sugerido`, com a divergência na fila, e fica na fila e no resumo com 2026-04-24; nada entra na agenda até a decisão.

## Como usar no teste

1. Rode a habilidade com o material do lote, sem mostrar o gabarito.
2. Compare com o gabarito linha por linha.
3. Quando o escritório tiver casos próprios, troque estes por publicações reais anonimizadas em `escritorio/04-base/casos-de-teste/controladoria/`.
