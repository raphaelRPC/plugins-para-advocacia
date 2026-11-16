---
documento: Contrato de honorários advocatícios
contato: [CÓDIGO]
versao: v1
revisado_em: AAAA-MM-DD
dono: [ADVOGADO RESPONSÁVEL]
proposta_aceita: [CÓDIGO]-proposta-v[N]
mudanca_desta_versao: primeira versão
---

## Antes de enviar (interno, não vai para o cliente)

> Esta seção e o cabeçalho de cima ficam no escritório. O script `md_para_docx.py` não leva nenhum dos dois para o .docx. Marque cada item com `[x]` quando estiver conferido. Enquanto houver item sem marcar, ou marcação e campo aberto entre colchetes no texto de baixo, o script avisa que o contrato não está pronto e não cria o .docx (só com `--forcar`, para leitura interna). Os campos entre chaves, como `{QUALIFICAÇÃO COMPLETA}`, são de propósito: o escritório preenche no .docx, no próprio sistema, e confere com `--conferir-docx`.

- Quem confere e assina pelo escritório: [ADVOGADO RESPONSÁVEL] · Sigla: H (a IA escreveu a minuta; assinar e fechar o valor é de uma pessoa)
- Proposta aceita: [CÓDIGO]-proposta-v[N] · cenário escolhido: [CENÁRIO]
- Versão: v1 · o que mudou: primeira versão

**Proposta e contrato lado a lado**

| Ponto | Proposta | Contrato | Igual? |
|---|---|---|---|
| Escopo (itens) | | | |
| Não incluído (itens) | | | |
| Valor total | | | |
| Entrada e parcelas | | | |
| Vencimentos | | | |
| Êxito (percentual, base, momento) | | | |
| Despesas | | | |
| Abatimento da consulta | | | |

**Conferências** (uma por cláusula sensível; o porquê de cada uma está em `references/clausulas-comentadas.md`)

- [ ] Cláusula 1, partes: contratante é quem recebe o serviço; responsável financeiro, representação ou poderes de quem assina por empresa `[CONFERIR]`.
- [ ] Cláusula 2, objeto: o texto descreve trabalho, não resultado, e é igual ao escopo da proposta.
- [ ] Cláusula 5, êxito: base, momento e limite do total de honorários em relação ao proveito do cliente, no Código de Ética e Disciplina da OAB `[CONFERIR]`.
- [ ] Cláusula 6, sucumbência: titularidade pelo Estatuto da Advocacia e a regra que o escritório adota `[CONFERIR]`.
- [ ] Cláusula 8, prestação de contas de valores recebidos em nome do cliente `[CONFERIR]`.
- [ ] Cláusula 11, sigilo e LGPD: finalidade, mínimo necessário e canal do titular `[CONFERIR]`.
- [ ] Cláusula 12, revogação e renúncia: honorários proporcionais, êxito depois da revogação e prazo de responsabilidade depois da renúncia `[CONFERIR]`.
- [ ] Cláusula 13, substabelecimento: com ou sem reserva e ciência do cliente `[CONFERIR]`.
- [ ] Cláusula 14, inadimplência: limites de multa e juros e o contrato como título para cobrar os honorários `[CONFERIR]`.
- [ ] Cláusula 16, foro: relação de consumo e foro do domicílio do contratante `[CONFERIR]`.
- [ ] Assinaturas: ferramenta de assinatura eletrônica, tipo de assinatura aceito e testemunhas `[CONFERIR]`.
- [ ] Valor final e condições fechados pelo advogado (H).

**O que o escritório preenche no .docx, fora da IA**

- `{NOME COMPLETO}` e `{QUALIFICAÇÃO COMPLETA}` das partes (documento, endereço, estado civil).
- `{DADOS PARA PAGAMENTO}`.
- `{DATA DA ASSINATURA}` e, se a assinatura for eletrônica, o que a ferramenta pedir.
- Depois de preencher, confira o .docx com `--conferir-docx` antes de mandar para assinatura: chave que sobrou é pendência.

**Pendências** (decisões que faltam; cada uma também aparece no texto de baixo até ser resolvida)

- [ ] [Ex.: multa, juros e índice da Cláusula 14 `[A DEFINIR]`; campo `inadimplencia` da ficha comercial vazio]

<!-- fim: antes de enviar -->

# Contrato de prestação de serviços advocatícios e honorários

## Cláusula 1. Partes

**Contratante:** {NOME COMPLETO}, {QUALIFICAÇÃO COMPLETA, preenchida no sistema do escritório}.

[Só se houver responsável financeiro: **Responsável financeiro:** {NOME COMPLETO}, {QUALIFICAÇÃO COMPLETA, preenchida no sistema do escritório}, que assume o pagamento dos honorários com a concordância do contratante. O responsável financeiro só recebe informação sobre o caso se o contratante autorizar por escrito.]

[Só se o contratante for representado ou assistido: a forma de representação que o advogado decidiu.]

**Contratado:** [CONTRATADO, de `dados_para_documentos`: advogado com inscrição na OAB/UF e número, ou sociedade de advogados com o registro na OAB], com endereço profissional em [ENDEREÇO PROFISSIONAL DO ESCRITÓRIO], [CIDADE/UF].

## Cláusula 2. Objeto e escopo

O contratado vai prestar ao contratante os seguintes serviços:

1. [Item do escopo, igual à proposta]
2. [Item]
3. [Item]

O contratado se compromete a trabalhar com zelo e técnica. O resultado do caso depende da decisão do órgão ou do juízo, e por isso não é garantido.

## Cláusula 3. O que não está incluído

Não fazem parte deste contrato:

1. [Item do não incluído, igual à proposta]
2. [Item]
3. [Item]

Qualquer serviço fora da Cláusula 2 depende de nova proposta e de aceite por escrito.

## Cláusula 4. Honorários e forma de pagamento

Pelos serviços da Cláusula 2, o contratante paga ao contratado o valor total de R$ [VALOR] ([VALOR POR EXTENSO]), da seguinte forma: [CENÁRIO ESCOLHIDO NA PROPOSTA, COM DATAS E VALORES].

[Só se a consulta for abatida: "O valor da consulta, já pago, foi descontado do total."]

Formas de pagamento: [FORMAS DA FICHA COMERCIAL]. Dados para pagamento: {DADOS PARA PAGAMENTO, preenchidos no sistema do escritório}.

## Cláusula 5. Honorários de êxito

[Sem êxito: "Não há honorários de êxito neste contrato."]

[Com êxito: "Além dos honorários da Cláusula 4, o contratante paga ao contratado [X]% ([POR EXTENSO] por cento) sobre [BASE DE CÁLCULO DA POLÍTICA], no momento em que [MOMENTO DO PAGAMENTO DA POLÍTICA]. Se não houver valor recebido pelo contratante, não há honorários de êxito. A soma de todos os honorários não passa do proveito obtido pelo contratante, conforme o Código de Ética e Disciplina da OAB."]

## Cláusula 6. Honorários de sucumbência

Os honorários de sucumbência fixados pelo juízo pertencem ao contratado, conforme o Estatuto da Advocacia (Lei 8.906/1994), e não se compensam com os honorários deste contrato. [Ou a regra que o escritório adota, escrita pelo advogado.]

## Cláusula 7. Despesas

As despesas do caso, como custas, perícias, cópias, deslocamentos e correio, não estão incluídas nos honorários e ficam a cargo de [QUEM PAGA, CONFORME A POLÍTICA E O CAMPO `despesas`]. Antes de qualquer despesa, o contratado informa o valor e o motivo, e o contratante aprova. O contratado presta contas das despesas pagas com recursos do contratante.

## Cláusula 8. Obrigações do contratado

1. Prestar os serviços da Cláusula 2 com zelo e técnica.
2. Informar o contratante sobre o andamento do caso e sobre cada decisão relevante.
3. Guardar sigilo sobre tudo o que souber em razão do caso.
4. Devolver os documentos originais ao fim do contrato.
5. Prestar contas de valores recebidos em nome do contratante.

## Cláusula 9. Obrigações do contratante

1. Dar informações verdadeiras e completas e entregar os documentos pedidos nos prazos combinados.
2. Avisar o contratado de qualquer mudança de endereço, telefone ou e-mail.
3. Comparecer a perícias, audiências e reuniões quando chamado.
4. Pagar os honorários e as despesas aprovadas nas datas combinadas.
5. Não fazer acordo nem tratar do caso diretamente com a outra parte sem avisar o contratado.

## Cláusula 10. Comunicação

O contratado se comunica com o contratante por [CANAIS DA FICHA DO ESCRITÓRIO], em [HORÁRIO DE ATENDIMENTO]. Mensagens recebidas fora desse horário são respondidas no dia útil seguinte. Notícia importante sobre o caso é dada por escrito e, quando for o caso, também por ligação.

## Cláusula 11. Sigilo e proteção de dados

O contratado trata os dados pessoais do contratante só para a prestação dos serviços deste contrato e para cumprir obrigações legais e éticas, conforme a LGPD (Lei 13.709/2018), com o mínimo necessário e com medidas de segurança. Dados sensíveis, como os de saúde, são usados só no que o caso exige. O contratante pode pedir informação sobre o tratamento dos seus dados pelo canal [CANAL PARA O TITULAR DOS DADOS].

## Cláusula 12. Revogação e renúncia

1. O contratante pode revogar o mandato a qualquer tempo. Nesse caso, são devidos os honorários proporcionais ao trabalho já feito[, e os de êxito na forma da Cláusula 5, se o resultado vier depois: só se o advogado decidir manter].
2. O contratado pode renunciar ao mandato, avisando o contratante por escrito, e continua responsável pelo caso pelo prazo previsto em lei.
3. Em qualquer caso, o contratado entrega os documentos e as informações para quem assumir o caso.

## Cláusula 13. Substabelecimento

O contratado pode substabelecer os poderes [COM RESERVA OU SEM RESERVA] a outro advogado de sua confiança, avisando o contratante. Substabelecimento sem reserva depende da concordância do contratante.

## Cláusula 14. Inadimplência

O atraso no pagamento gera [MULTA, JUROS E ÍNDICE, do campo `inadimplencia` da ficha comercial], a partir do vencimento. Antes de qualquer medida, o contratado procura o contratante para combinar uma solução. Este contrato, assinado, serve como título para a cobrança dos honorários, conforme o Estatuto da Advocacia.

## Cláusula 15. Vigência

Este contrato vale da assinatura até a conclusão dos serviços da Cláusula 2, ou até a revogação ou a renúncia.

## Cláusula 16. Foro

Fica eleito o foro da comarca de [CIDADE/UF] para resolver qualquer questão sobre este contrato.

## Assinaturas

[CIDADE], {DATA DA ASSINATURA}.

Contratante: ______________________________

[Só se houver responsável financeiro: "Responsável financeiro: ______________________________"]

Contratado: ______________________________ [NOME E OAB, de `dados_para_documentos`]

[Só se o escritório usar testemunhas: "Testemunhas: 1. ______________ 2. ______________"]

[Só se a assinatura for eletrônica: "Assinado eletronicamente pela ferramenta [FERRAMENTA DO ESCRITÓRIO]."]
