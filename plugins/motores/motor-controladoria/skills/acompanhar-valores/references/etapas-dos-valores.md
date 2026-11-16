# As etapas de cada tipo de valor

Leia no passo 3 (abrir a linha) e no passo 5 (atualizar a etapa). As etapas são as do registro (`valores.csv`) e servem para todos os tipos; cada tipo usa só algumas. O caminho de cada valor no tribunal muda com a Justiça, o tribunal, o ente que paga e as regras do ano: tudo o que está abaixo sobre o caminho é ponto de partida, marcado `[CONFERIR]` no portal e nos atos do tribunal, e o escritório ajusta pela `adaptar-controladoria`.

## 1. As etapas do registro

| Etapa | Quer dizer | O que a pessoa registra |
|---|---|---|
| `pedido` | O escritório pediu (expedição de alvará, requisição, levantamento de depósito) | A data do pedido em `etapa_em` |
| `deferido` | O juízo deferiu o pedido | A data da decisão |
| `expedido` | O alvará, a RPV ou o precatório foi expedido pelo juízo | A data da expedição (a publicação ou a certidão) |
| `transmitido` | A requisição foi enviada ao tribunal que paga, ou o precatório foi inscrito | A data que o portal mostra `[CONFERIR]` |
| `depositado` | O valor está disponível (conta judicial ou banco indicado) | A data do depósito que o portal ou o extrato mostra |
| `levantado` | O valor saiu da conta judicial (para o cliente ou para a conta do escritório, conforme o contrato) | A data do levantamento |
| `repassado` | O escritório repassou ao cliente o que é dele, com a prestação de contas | A data do repasse |
| `suspenso` | Impugnação, bloqueio, cancelamento da requisição, erro de dado | A data e, na `observacao`, o motivo em poucas palavras |
| `cancelado` | O valor deixou de existir no processo (acordo, decisão) | A data e o motivo |

Nada é apagado: a linha muda de etapa, com a data nova em `etapa_em`, e o que aconteceu vai em uma linha curta da `observacao`.

## 2. O caminho de cada tipo (ponto de partida, tudo `[CONFERIR]`)

| Tipo | Caminho comum | Onde acompanhar |
|---|---|---|
| `rpv` | pedido (ou expedição de ofício pelo juízo) → expedido → transmitido → depositado → levantado → repassado | O portal do tribunal que paga e o banco indicado `[CONFERIR]` |
| `precatorio` | expedido → transmitido (inscrito no orçamento) → depositado → levantado → repassado | O portal de precatórios do tribunal `[CONFERIR]` |
| `alvara` | pedido → deferido → expedido → levantado → repassado | O processo e o banco depositário `[CONFERIR]` |
| `deposito-judicial` | depositado (pela outra parte ou por ordem do juízo) → pedido de levantamento → deferido → levantado → repassado | O processo e o extrato da conta judicial `[CONFERIR]` |

Quanto tempo cada etapa costuma levar não entra aqui: depende do tribunal, do ente e do ano, e qualquer número vira promessa. O "parado há N dias" do script é só o lembrete para alguém conferir o portal.

## 3. O que nunca vai para o cliente

- Data de pagamento ("cai em maio", "sai em 60 dias", "deve pagar até o fim do ano").
- Valor calculado, atualizado ou com desconto feito pela IA. Se a mensagem citar valor, é o valor do documento do tribunal, copiado e conferido por uma pessoa, com o desconto de honorários só como está no contrato.
- Comparação com o caso de outro cliente ("o do seu vizinho já caiu").

O que pode ir, pela experiência e com aprovação: o que aconteceu (a RPV foi expedida), o que isso quer dizer em palavras simples (é a ordem de pagamento enviada ao tribunal), o que vem depois (o tribunal paga no calendário dele, e o escritório avisa quando o valor estiver disponível) e o que depende do cliente (documento, conta, ida ao banco).

## 4. O aviso para a experiência

Com o motor-experiencia instalado, o aviso ao cliente é um arquivo na entrada da experiência, `escritorio/07-operacao/experiencia/entrada/AAAA-MM-DD-HHMM-controladoria.md`, no formato da `encaminhar-providencia` (se instalada) ou, sem ela, este texto puro:

```
origem: controladoria · acompanhar-valores
codigo_caso: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME]
o_que_aconteceu: [TIPO] [ETAPA] em AAAA-MM-DD (ex.: RPV expedida em 2026-04-13)
tipo_de_noticia: boa | neutra | ruim (ruim vai por ligação)
o_que_dizer: o que aconteceu, o que quer dizer, o que vem depois, o que depende do cliente
o_que_nunca_dizer: data de pagamento; valor calculado
observacao: [UMA LINHA, SEM DADO SENSÍVEL; ex.: cliente insatisfeito, vale a ligação]
```

A experiência rascunha a mensagem (status-para-o-cliente) e a pessoa aprova na fila de lá. Sem o motor-experiencia, a habilidade mostra o texto para a pessoa enviar pelo canal oficial. Depois do envio, a pessoa grava a data em `cliente_avisado_em`.
