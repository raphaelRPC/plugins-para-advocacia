---
documento: Prestação de contas
cliente: [CÓDIGO]
versao: v1
revisado_em: AAAA-MM-DD
dono: [QUEM CONFERE, de quem_le_antes_de_enviar]
mudanca_desta_versao: primeira versão
---

## Antes de enviar (interno, não vai para o cliente)

> Esta seção e o cabeçalho de cima ficam no escritório. O script `md_para_docx.py` não leva nenhum dos dois para o .docx. Marque cada item com `[x]` quando estiver conferido. Enquanto houver item sem marcar, ou marcação no texto de baixo, o script avisa que a prestação de contas não está pronta.

- Quem confere: [FUNÇÃO, de `quem_le_antes_de_enviar`] · Sigla: A (a IA monta com os números que o advogado deu; o advogado confere cada valor e decide enviar). Resultado ruim ou parcial: H antes (ligação do advogado), A depois.
- De onde vieram os números: [FONTE: comprovante do depósito, alvará, guia de levantamento, termo do acordo, contrato de honorários, comprovantes das despesas]
- O que a ficha diz (`prestacao_de_contas`): [O QUE ENTRA E O PRAZO DO REPASSE]

**Conferências dos valores**

- [ ] Valor recebido igual ao comprovante (depósito, alvará, guia ou termo do acordo) `[CONFERIR]`.
- [ ] Honorários iguais ao contrato assinado: percentual ou valor e a base de cálculo `[CONFERIR]`.
- [ ] Honorários pagos pela outra parte ao advogado (sucumbência), se houver, tratados como o contrato diz `[CONFERIR]`.
- [ ] Cada despesa com comprovante e prevista no contrato.
- [ ] A conta fecha: valor recebido menos honorários menos despesas é igual ao valor do repasse.
- [ ] Imposto ou retenção, se houver, conferido com quem cuida da contabilidade `[CONFERIR]`.
- [ ] Prazo do repasse igual ao do contrato ou da ficha.

**Conferências do resto**

- [ ] Conta de destino confirmada com o cliente por ligação ou pessoalmente, nunca só por mensagem. O número da conta não entra no documento.
- [ ] Resultado ruim ou parcial: o advogado já falou com o cliente antes deste documento.
- [ ] O que muda para o cliente: cada orientação conferida pelo advogado; prazo, valor de benefício ou regra de lei com fonte `[CONFERIR]`.
- [ ] Documentos: lista do que volta ao cliente e do que fica guardado bate com `guarda_de_documentos`.
- [ ] Texto sem promessa, sem CPF, sem número de conta, sem dado de saúde e sem nome da outra parte além do necessário.

**Pendências** (o que ainda falta; cada uma também aparece no texto de baixo até ser resolvida)

- [ ] [Ex.: valor das despesas `[A PREENCHER]`, a advogada traz os comprovantes]

<!-- fim: antes de enviar -->

# Prestação de contas

**[NOME DO ESCRITÓRIO]** · [CIDADE/UF] · [DATA]

Para: [PRIMEIRO NOME] · Caso: [TIPO DE CASO, EM ATÉ 5 PALAVRAS]

[Uma ou duas linhas no tom da ficha. Ex.: "Como combinamos na nossa conversa, aqui está, por escrito, tudo o que entrou no seu caso, o que fica com o escritório e o que vai para você."]

## O que aconteceu no caso

[Duas a quatro linhas, sem juridiquês, com o resultado e a data. Termo técnico explicado na primeira vez. Ex.: "O acordo foi aprovado pelo juiz em [DATA]. Isso quer dizer que ele vale como uma decisão: se não for cumprido, dá para cobrar na Justiça."]

## Os valores

| Item | Valor | De onde vem |
|---|---|---|
| Valor recebido no caso | R$ [VALOR RECEBIDO] | [ORIGEM, ex.: depósito feito pela outra parte em DATA] |
| Honorários do escritório | R$ [VALOR DOS HONORÁRIOS] | [BASE, ex.: o percentual combinado no contrato de DATA] |
| Despesas do caso | R$ [VALOR DAS DESPESAS] | lista logo abaixo |
| **Valor que vai para você** | **R$ [VALOR DO REPASSE]** | valor recebido menos honorários e despesas |

Despesas:
- [DESPESA, ex.: cópias e autenticações]: R$ [VALOR]
- [DESPESA]: R$ [VALOR]

[Se não houve valor a receber, troque a tabela por uma frase: "Neste caso não houve valor a receber. Os honorários foram os combinados no contrato e já estão quitados." Ou o que for verdade.]

## Quando e como você recebe

- O valor de R$ [VALOR DO REPASSE] vai para a conta que você confirmou com a gente, até [DATA DO REPASSE].
- Quando o depósito for feito, a gente te avisa e manda o comprovante.

## Seus documentos

- Voltam para você: [LISTA DOS ORIGINAIS, ex.: certidões, carteira de trabalho]. [COMO, ex.: retirar no escritório ou entregamos em mãos na reunião].
- Ficam guardados no escritório: [O QUE FICA, ex.: cópias digitais do processo], por [PRAZO DE `guarda_de_documentos`], para o caso de você precisar. Depois disso, são descartados com segurança.

## O que muda para você agora

[Três a cinco itens, do material de references/o-que-muda-por-area.md, conferidos pelo advogado. Ex.: "A pensão passa a ser depositada todo dia [DIA]. Guarde os comprovantes."; "Se o pagamento atrasar, fale com a gente. Dá para cobrar na Justiça, e a gente te explica como."]

## Se precisar de nós

[Porta aberta, no tom da ficha. Ex.: "Seu caso terminou, mas o nosso número continua o mesmo. Se surgir uma dúvida sobre ele, é só escrever."]

O escritório nunca pede depósito, taxa ou código por mensagem para liberar valor. Se alguém pedir em nosso nome, não pague e ligue para o número oficial: [TELEFONE OFICIAL, DE `canais` NA FICHA DO ESCRITÓRIO].

[ASSINATURA, de `assinatura_das_mensagens` ou `dados_para_documentos`]
