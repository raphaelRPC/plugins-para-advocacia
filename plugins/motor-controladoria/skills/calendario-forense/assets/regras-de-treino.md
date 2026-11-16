---
documento: Regras de contagem de treino
versao: 1
validada_por: treino (tabela de partida, não vale para prazo real)
validada_em: 2026-04-01
treino: sim
dono: treino
---

# Regras de contagem de treino · Escritório Modelo

Cópia da tabela de `../../../docs/contagem.md` com a tabela de prazos por ato de treino de `../../../docs/casos-ficticios.md`. Serve só para os casos fictícios. A tabela real do escritório fica em `escritorio/04-base/controladoria/regras-de-contagem.md`, é copiada pela `calendario-forense` e validada por quem responde pela controladoria, linha por linha, no texto oficial.

O script de conta (`calcular-prazo`) lê as regras pela chave (primeira coluna), o prazo de ciência da linha `intimacao-portal` (o número antes de "dias corridos") e a seção "Prazos por ato".

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

## Prazos por ato

Números só para o treino, para a conta ter de onde partir quando o ato não diz o prazo. O escritório preenche e valida a dele, com a fonte de cada linha conferida no texto oficial.

| ato | rito | dias | contagem | fonte |
|---|---|---|---|---|
| recurso inominado | juizado-federal | 10 | uteis | treino: casos-ficticios.md |
| recurso ordinário | trabalhista | 8 | uteis | treino: casos-ficticios.md |
| embargos de declaração | civel | 5 | uteis | treino: casos-ficticios.md |
| apelação | civel | 15 | uteis | treino: casos-ficticios.md |
