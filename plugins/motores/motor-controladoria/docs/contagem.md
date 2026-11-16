# Como o plugin conta um prazo

A IA capta o prazo, mas não interpreta. Ela lê a publicação, mostra o trecho literal, sugere o que o ato pede e faz a conta com as regras desta tabela. Quem diz qual é o prazo e se a conta está certa é uma pessoa, na dupla conferência (`prazos.md`).

## A tabela vem marcada e o escritório valida

As regras abaixo são o ponto de partida, escritas a partir das leis processuais. Todas estão marcadas `[CONFERIR]`, porque lei muda, tribunal tem regra própria e cada escritório atua em ritos diferentes. A primeira tarefa do escritório é validar a tabela:

1. A `calendario-forense` copia esta tabela para `escritorio/04-base/controladoria/regras-de-contagem.md`.
2. Quem responde pela controladoria confere cada linha no texto oficial (Planalto, regimento e atos do tribunal), ajusta o que precisar e escreve no cabeçalho `validada_por` e `validada_em`.
3. Enquanto a tabela do escritório não estiver validada, todo prazo calculado sai com o aviso "regra ainda não validada pelo escritório" no relatório de conferência.
4. A tabela validada volta a ser conferida uma vez por ano, ou quando uma lei ou ato do tribunal mudar.

Os scripts leem as regras pela chave (primeira coluna). Linha nova que o escritório criar ganha chave nova, em minúsculas e com hífen.

## As regras

| Chave | O que diz | Onde está `[CONFERIR]` | Como o script conta |
|---|---|---|---|
| `civel-cpc` | Prazo processual em dias úteis. Exclui o dia do começo e inclui o do vencimento | CPC, art. 219 e art. 224 | Dias úteis, a partir do primeiro dia útil depois da publicação |
| `publicacao-diario` | Publicação no diário eletrônico (DJEN ou diário do tribunal): considera-se publicada no primeiro dia útil seguinte ao da disponibilização, e o prazo começa no primeiro dia útil seguinte ao da publicação | CPC, art. 224, §§ 2º e 3º; Lei 11.419/2006, art. 4º | Disponibilização → publicação (próximo dia útil) → início (próximo dia útil) |
| `intimacao-portal` | Intimação pelo portal do sistema (PJe, eproc e outros): a pessoa tem um prazo em dias corridos para abrir; sem abrir, a intimação se considera feita no fim desse prazo | Lei 11.419/2006, art. 5º; CPC, art. 231 | Data do envio + o prazo de ciência da tabela (10 dias corridos) = ciência tácita; o prazo do ato começa depois, pela regra do rito |
| `domicilio-eletronico` | Comunicação pelo Domicílio Judicial Eletrônico: prazo próprio de ciência, diferente para citação e intimação | Resolução do CNJ sobre o Domicílio Judicial Eletrônico e CPC, art. 231 | Não calcula sozinho: a pessoa informa a data da ciência no painel e o script conta dali |
| `recesso-forense` | Suspensão dos prazos de 20 de dezembro a 20 de janeiro | CPC, art. 220 | Os dias do período não contam; o prazo que cai dentro volta a correr no primeiro dia útil seguinte |
| `trabalhista-clt` | Na Justiça do Trabalho, prazo em dias úteis, com exclusão do dia do começo e inclusão do vencimento | CLT, art. 775 | Dias úteis, mesma lógica do `civel-cpc` |
| `recesso-trabalhista` | Suspensão dos prazos de 20 de dezembro a 20 de janeiro na Justiça do Trabalho | CLT, art. 775-A | Como o `recesso-forense` |
| `juizado-civel` | Nos Juizados Especiais Cíveis, prazo em dias úteis | Lei 9.099/1995, art. 12-A | Dias úteis |
| `juizado-federal` | Nos Juizados Especiais Federais, a contagem segue a lei dos juizados e, no que ela não disser, o CPC | Lei 10.259/2001 e Lei 9.099/1995, art. 12-A | Dias úteis; o prazo de cada recurso vem da tabela do escritório |
| `penal-cpp` | No processo penal, prazos contínuos (dias corridos), sem contar o dia do começo; terminado em dia sem expediente, vai para o dia útil seguinte | CPP, art. 798 | Dias corridos; só o vencimento é empurrado para dia útil |
| `recesso-penal` | Suspensão de prazos no processo penal no fim do ano, com exceções (réu preso, medidas urgentes) | CPP, art. 798-A | Só suspende quando a pessoa marca que a exceção não se aplica |
| `fazenda-dobro` | Fazenda Pública (União, estados, municípios, autarquias como o INSS) tem prazo em dobro, salvo quando a lei fixa prazo próprio para ela | CPC, art. 183 | Dobra só quando o prazo é **da Fazenda** e a pessoa confirma |
| `defensoria-dobro` | Defensoria Pública e quem ela assiste têm prazo em dobro | CPC, art. 186 | Dobra só com a confirmação |
| `mp-dobro` | Ministério Público tem prazo em dobro para se manifestar | CPC, art. 180 | Dobra só com a confirmação |
| `litisconsortes-dobro` | Litisconsortes com advogados de escritórios diferentes têm prazo em dobro, salvo em processo eletrônico | CPC, art. 229 | Em processo eletrônico, não dobra |
| `juizado-sem-dobro` | Nos juizados especiais, a regra do prazo em dobro tem limites próprios | Lei 10.259/2001, art. 9º, e a jurisprudência do tribunal | Não dobra sem confirmação expressa |
| `indisponibilidade` | Sistema fora do ar no último dia do prazo: o prazo vai para o primeiro dia útil seguinte | Lei 11.419/2006, art. 10, § 2º; CPC, art. 224, § 1º | Só empurra o **vencimento**; indisponibilidade no meio do prazo não muda a conta. A indisponibilidade precisa estar certificada pelo tribunal |
| `expediente-reduzido` | Dia em que o expediente começa mais tarde ou acaba mais cedo conta como dia sem expediente quando é o do começo ou o do vencimento | CPC, art. 224, § 1º | Só para começo e vencimento, se o calendário marcar o dia |
| `prazo-material` | Prazo de direito material (decadência, prescrição, prazo de contrato) não segue a contagem processual | Código Civil e lei própria | O script não calcula: a pessoa informa a data |

## Os prazos de cada ato

O prazo de cada recurso e de cada manifestação (quantos dias para apelar, para embargos de declaração, para recurso inominado, para recurso ordinário, para réplica) **não vem pronto no plugin**. A conta só começa com o número de dias que:

1. o próprio ato publicado diz ("em 15 dias", "no prazo de 5 dias"); ou
2. a tabela de prazos por ato do escritório (`regras-de-contagem.md`, seção "Prazos por ato", preenchida e validada na `calendario-forense`) traz.

Sem nenhum dos dois, o prazo fica `[A CONFIRMAR: quantos dias]` e vai para a pessoa. A IA nunca completa o número de dias de memória.

## O que vale como dia útil

O calendário de cada tribunal (`04-base/controladoria/calendario/<tribunal>-AAAA.md`, feito pela `calendario-forense`) diz quais dias não têm expediente:

- sábados e domingos;
- feriados nacionais;
- feriados estaduais e municipais da cidade do juízo, quando o tribunal os segue;
- dias sem expediente do próprio tribunal (portarias, pontos facultativos que o tribunal adota, feriados da Justiça Federal);
- o recesso e as suspensões;
- dias de expediente reduzido e de indisponibilidade certificada, marcados à parte.

Cada linha do calendário traz a fonte (o ato do tribunal ou a lei) e a data em que foi conferida. Calendário sem conferência faz todo prazo sair com o aviso "calendário não conferido".

## A regra de ouro

1. A conta mostra cada passo: disponibilização, publicação, início, os dias contados (com os que pulou e por quê) e o vencimento.
2. A regra usada aparece pela chave, com o artigo marcado.
3. Na dúvida entre duas datas, vale a **mais cedo**, e a dúvida vai para a pessoa.
4. Prazo em dobro, ciência tácita e prazo material nunca são decididos pela IA.
5. A data de segurança (`dias_de_seguranca` da ficha) é a data da agenda. A data fatal é o limite e nunca é a meta.
6. Linha do calendário ainda `[CONFERIR]` (ou com data `[A PREENCHER]`) que muda a conta: o script faz as duas leituras, fica com a mais cedo e mostra a dúvida em destaque. Disponibilização em dia sem expediente também gera aviso.
7. Disponibilização ou ciência dentro do recesso ou de uma suspensão: o script fica com a leitura que dá a data mais cedo e avisa, para a pessoa conferir no ato do tribunal. Na contagem em dias corridos, a conta volta a correr no dia seguinte ao fim da suspensão.
