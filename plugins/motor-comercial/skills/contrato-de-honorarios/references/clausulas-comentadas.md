# Cláusulas comentadas

O que cada cláusula do contrato de honorários decide, o que perguntar ao advogado e o que conferir antes de assinar. Serve para a primeira minuta do escritório e para o modo "revisar modelo". As normas aparecem só pelo nome. Quando a preocupação depende do texto da lei ou de entendimento atual, ela vira um item `- [ ]` com `[CONFERIR]` no cabeçalho interno "Antes de enviar" da minuta, e quem confere é o advogado. O texto da cláusula, que vai ao cliente, sai sem marcação.

## Como usar no modo "revisar modelo"

1. Leia o modelo do escritório inteiro.
2. Para cada cláusula desta lista, diga: **tem** (e onde), **falta** ou **tem, mas precisa conferir** (e por quê, em uma linha).
3. Entregue a tabela abaixo preenchida. Não reescreva o modelo sem o advogado pedir.

| Cláusula | Situação no modelo | Observação |
|---|---|---|
| Partes | tem / falta / conferir | |
| Objeto e escopo | | |
| O que não está incluído | | |
| Honorários e pagamento | | |
| Êxito | | |
| Sucumbência | | |
| Despesas | | |
| Obrigações do contratado | | |
| Obrigações do contratante | | |
| Comunicação | | |
| Sigilo e LGPD | | |
| Revogação e renúncia | | |
| Substabelecimento | | |
| Inadimplência | | |
| Vigência | | |
| Foro | | |
| Assinaturas | | |

## As cláusulas

### 1. Partes
- **Decide:** quem contrata, quem é contratado, quem paga.
- **Fonte do contratado:** `dados_para_documentos` da ficha do escritório (OAB dos advogados e registro da sociedade).
- **Perguntar:** "O contrato é com a própria pessoa que veio à consulta ou com outra?"; "O contratado é você como pessoa ou a sociedade de advogados?"
- **Conferir:** representação de incapaz, menor ou interditado; poderes de quem assina por empresa; concordância do contratante quando outra pessoa paga.
- **Erro comum:** pôr como contratante o filho que pagou, quando o serviço é para a mãe. O sigilo é de quem recebe o serviço.

### 2. Objeto e escopo
- **Decide:** o que o escritório vai fazer.
- **Fonte:** "O que vamos fazer" da proposta aceita, item por item.
- **Conferir:** se a fase (administrativa, primeira instância, recursos, cumprimento) bate com a proposta.
- **Erro comum:** "patrocínio da causa até o final", que inclui recursos e cumprimento que a proposta não cobrava.

### 3. O que não está incluído
- **Decide:** o que fica de fora e como se contrata depois.
- **Fonte:** "O que não está incluído" da proposta.
- **Erro comum:** cláusula ausente. Sem ela, qualquer serviço novo vira discussão.

### 4. Honorários e forma de pagamento
- **Decide:** valor, forma, datas.
- **Fonte:** o cenário que o cliente escolheu.
- **Conferir:** soma das parcelas; abatimento da consulta; valor por extenso igual ao número.
- **Fica com o escritório:** dados bancários e chave de pagamento. A IA não escreve.

### 5. Honorários de êxito
- **Decide:** percentual, base de cálculo, momento do pagamento, o que acontece sem resultado.
- **Perguntar:** "O percentual incide sobre o quê e quando se paga?" (se a política não disser).
- **Conferir sempre:** a regra do Código de Ética e Disciplina da OAB sobre os honorários somados não passarem do proveito do cliente; como o percentual incide sobre benefício mensal ou prestação continuada; êxito devido depois de revogação.
- **Erro comum:** "20% do que ganhar", sem dizer se é sobre o bruto, o líquido, os atrasados ou as parcelas futuras.

### 6. Honorários de sucumbência
- **Decide:** de quem é a sucumbência e se ela abate os contratuais.
- **Conferir sempre:** o que o Estatuto da Advocacia diz sobre a titularidade da sucumbência e a regra que o escritório adota.
- **Erro comum:** silêncio. O cliente descobre a sucumbência na sentença e acha que pagou duas vezes.

### 7. Despesas
- **Decide:** quem paga custas, perícia, cópias e deslocamento, e como se aprova antes.
- **Fonte:** proposta e política.
- **Conferir:** gratuidade da justiça, quando o advogado vai pedir.
- **Erro comum:** gasto feito e cobrado depois, sem aviso.

### 8 e 9. Obrigações das partes
- **Decidem:** o que cada lado faz para o caso andar.
- **Ajuste ao caso:** perícia (previdenciário), audiência (trabalhista), mediação (família).
- **Erro comum:** obrigação só do cliente. O contrato mostra as duas mãos.

### 10. Comunicação
- **Decide:** por onde, em que horário e como chegam as notícias importantes.
- **Fonte:** ficha do escritório (`canais`, `horario_de_atendimento`) e, se existir, a ficha da experiência do motor-experiencia (`primeira_resposta_cliente_ativo`).
- **Erro comum:** prometer no contrato um prazo de resposta que o escritório não cumpre.

### 11. Sigilo e LGPD
- **Decide:** para que os dados são usados, o mínimo necessário, segurança, canal do titular.
- **Conferir:** a LGPD (Lei 13.709/2018) e a política de privacidade do escritório, se houver; uso de ferramentas de IA com dados do cliente (conta profissional, regra de uso de IA do escritório).
- **Erro comum:** cláusula genérica que autoriza "qualquer uso".

### 12. Revogação e renúncia
- **Decide:** o que se paga se o cliente sair, e como o advogado sai.
- **Conferir sempre:** honorários proporcionais na revogação; êxito quando o resultado vem depois da revogação; prazo em que o advogado continua responsável depois de renunciar, conforme o Estatuto da Advocacia e a lei processual.
- **Erro comum:** multa alta por revogação, que pode ser considerada abusiva.

### 13. Substabelecimento
- **Decide:** se outro advogado pode atuar, com ou sem reserva de poderes.
- **Conferir:** ciência do cliente; o que o Código de Ética e Disciplina da OAB diz sobre substabelecimento sem reserva.

### 14. Inadimplência
- **Decide:** multa, juros, correção e o que acontece antes de qualquer medida.
- **Fonte:** campo `inadimplencia` da ficha comercial e seção 9 da política. Vazio: pergunte "Qual multa, juros e índice o escritório usa?". Sem resposta: `[A DEFINIR]` no texto da cláusula e a pendência no cabeçalho interno.
- **Conferir sempre:** limites de multa e juros; o contrato escrito como título para cobrar os honorários, conforme o Estatuto da Advocacia; a régua de cobrança do escritório, se houver.
- **Erro comum:** cláusula que permite parar de atuar no caso por atraso. Saída do caso é renúncia, com as regras dela.

### 15. Vigência
- **Decide:** até quando o contrato vale.
- **Fonte:** o escopo. Contrato mensal: prazo, renovação e aviso para encerrar.

### 16. Foro
- **Decide:** onde se discute o contrato.
- **Conferir sempre:** se a relação é de consumo e o foro do domicílio do contratante; mediação ou arbitragem, se o escritório quiser prever.

### Assinaturas
- **Decide:** como e por quem o contrato é assinado.
- **Conferir:** a ferramenta de assinatura eletrônica do escritório (conferir na configuração da conta) e o tipo de assinatura aceito; testemunhas, se o escritório usa.
- **Linha vermelha:** assinar é sempre de uma pessoa. A IA não envia para assinatura sozinha.
