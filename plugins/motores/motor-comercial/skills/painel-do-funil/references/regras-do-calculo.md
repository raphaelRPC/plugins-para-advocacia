# Regras do cálculo do painel

O script `scripts/painel.py` segue estas regras. Quem não tem como rodar o script conta à mão pelas mesmas regras, na mesma ordem, e marca no topo do painel: "contado sem o script, conferir". Com até uns 40 contatos no mês, a contagem à mão cabe numa conversa; acima disso, peça o script.

## 1. Quem entra no painel do mês

- **Contatos do mês** são as linhas com `entrada` dentro do mês pedido. É uma coorte: o painel acompanha quem entrou no mês, até onde chegou hoje.
- **Tipo:** `novo` e `antigo` entram (`../../../docs/funil.md`). O painel avisa quantos são `antigo`, porque já falavam com o escritório antes do registro e não são entrada nova de verdade.
- **Cliente ativo não fica no registro comercial.** Linha com `tipo = cliente` (registro antigo) fica fora do funil e aparece na qualidade do registro, para sair do csv.
- **Treino nunca entra.** Registro dentro de uma pasta `_treino` só é lido com `--treino`, e o painel sai marcado TREINO.
- **Período** (AAAA-MM:AAAA-MM) junta os meses e compara com o período anterior do mesmo tamanho. Período anterior sem nenhum contato (primeiro mês do registro) vira cuidado: a coluna "Anterior" não serve para comparar.

## 2. Até onde cada contato chegou

O registro guarda só a etapa atual (uma linha por contato). A passagem por etapa é deduzida da etapa onde o contato está:

| Etapa atual | Chegou até |
|---|---|
| `novo` | entrou |
| `triado`, `encaminhado`, `recusado` | triado |
| `consulta-agendada`, `nao-compareceu` | consulta agendada |
| `consulta-feita`, `sem-caso` | consulta feita |
| `proposta-enviada`, `negociando` | proposta enviada |
| `fechado` | fechado |
| `perdido` | a etapa de `perdido_na_etapa`; se vazia, proposta enviada quando há `valor_proposta`; senão, triado |

A última linha é conservadora: um perdido sem pista conta como perdido logo depois da triagem. O painel avisa quantos foram contados assim.

## 3. As passagens do funil

| Passagem | Chegaram | De |
|---|---|---|
| Entraram > triados | chegaram até triado | todos os contatos do mês |
| Triados atendíveis > consulta agendada | chegaram até consulta agendada | triados menos encaminhados e recusados |
| Consulta agendada > consulta feita | chegaram até consulta feita | chegaram até consulta agendada |
| Consulta feita com caso > proposta enviada | chegaram até proposta | chegaram até consulta feita menos `sem-caso` |
| Proposta enviada > fechado | fechados | chegaram até proposta |
| Entraram > fechado | fechados | todos os contatos do mês |

Encaminhado, recusado e sem-caso não são perda: são o escritório dizendo "não é para nós". Por isso saem do denominador da passagem seguinte.

**Taxa:** "x de y" sempre. Percentual só quando y é 10 ou mais. Abaixo disso, "poucos casos".

## 4. Entradas por origem, área e canal

- Conta os contatos do mês por valor da coluna, sem diferenciar maiúscula nem acento. Vazio vira "(sem origem)", "(sem área)", "(sem canal)".
- Para cada valor: quantos entraram, quantos no período anterior, quantos chegaram à proposta (pela tabela da seção 2), quantos fecharam e o valor somado dos que fecharam.
- Com `--origens` e `--areas` (as opções das fichas), o painel aponta na qualidade o valor que não está na ficha. `fora-da-area` e `a-confirmar` são sempre aceitos em `area`.

## 5. Primeira resposta e quem está sem resposta

- `primeira_resposta` é coluna normal do registro: data e hora da primeira resposta de uma pessoa (AAAA-MM-DD HH:MM). A resposta automática não conta.
- **Sem resposta** é `primeira_resposta` vazia em `novo` ou `triado` (`../../../docs/funil.md`, regra 1). O painel lista esses códigos com as horas úteis desde a entrada até a data de referência (`--hoje`, no fim do horário de atendimento), urgência alta primeiro. Lista também os perdidos que nunca receberam resposta.
- Etapa depois da triagem com `primeira_resposta` vazia é falha do registro (alguém respondeu e não anotou): vai para a qualidade.
- **Com uma pessoa, sem retorno registrado:** dos sem resposta, os que têm o `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:` (marcador de pessoa, `../../../docs/funil.md`, regra 4), sem diferenciar maiúscula. Eles estavam em PESSOA AGORA e ninguém registrou a conversa. A saída é o comando `fila`, que pergunta "Já falou? O que ficou combinado?", grava a `primeira_resposta` e troca o `proximo_passo` (`../../../docs/agentes-e-fila.md`).
- **Horas úteis:** só o tempo dentro do horário (`--horario`, padrão 09:00-18:00) e dos dias de atendimento (`--dias`, padrão seg-sex). Mensagem das 21h respondida às 9h30 do dia seguinte conta 30 minutos úteis. Feriado não é descontado: ajuste à mão.
- **Mediana**, e não média: um contato esquecido por três dias não esconde que o resto foi respondido em minutos. O painel mostra também a maior espera.
- **Dentro do prazo:** com `--prazo-horas` (o `primeira_resposta_contato_novo` da ficha comercial em horas úteis), conta quantos ficaram dentro e lista os códigos de quem ficou fora.
- Sem a coluna: o painel diz que não dá para medir, e a `auditar-conversas-comerciais` (se instalada) mede o tempo direto nas conversas exportadas.

## 6. Propostas e valores

- **Chegaram à proposta:** pela tabela da seção 2. **Com valor registrado:** contato do mês com `valor_proposta` preenchido. Proposta só de êxito fica sem valor, e o painel mostra a diferença entre os dois números.
- Valor somado: com valor, fechadas (`fechado`), em aberto (`proposta-enviada` ou `negociando`) e perdidas.
- Valor médio das fechadas: soma das fechadas dividida pelo número de fechadas com valor.
- O valor é o que está no registro, sem R$. "4.500", "4500" e "4500,00" são o mesmo número. O painel nunca completa valor que falta.
- **Movimento do mês:** fechados e perdidos cuja `atualizado_em` caiu no mês, de qualquer mês de entrada. É aproximado, porque `atualizado_em` é a última mudança da linha.

## 7. Perdas e pedidos para parar

- Motivos de perda: contagem de `motivo_perda` entre os perdidos do mês (`preco`, `fechou-com-outro`, `desistiu`, `sem-resposta`, `outro`). Vazio vira "(sem motivo)".
- Pediram para parar: códigos dos contatos do mês com `pediu_para_parar = sim`, e o total no registro inteiro. O painel não propõe nenhuma ação de contato para eles.

## 8. Qualidade do registro

Conferida no registro inteiro, e não só no mês:

| Problema | Por que importa |
|---|---|
| Código repetido | O funil conta duas vezes, e o código não pode ser reaproveitado |
| Entrada vazia ou fora do formato | O contato some do painel |
| Etapa fora da lista | Não entra em nenhuma passagem |
| Linha de cliente ativo, ou tipo diferente de novo e antigo | Cliente ativo sai do comercial |
| Contato sem origem, ou origem fora da ficha | "De onde vêm os clientes" fica sem resposta |
| Sem área, ou área fora da ficha | Use `fora-da-area` para o que o escritório não atende |
| Perdido sem motivo, motivo fora da lista ou sem `perdido_na_etapa` | A seção de perdas e o meio do funil ficam cegos |
| Proposta enviada, negociando ou fechado sem valor | O valor do mês sai menor, ou é proposta só de êxito: confirmar |
| Passou da triagem sem `primeira_resposta` | O tempo de resposta fica sem esse contato |
| `primeira_resposta` antes da `entrada` | Data trocada |
| `pediu_para_parar` diferente de sim ou nao | Risco de mandar retorno a quem pediu para parar |

## 9. Colunas do registro

Todas as colunas de `../../../docs/funil.md` são do registro. Só `codigo`, `entrada` e `etapa` são obrigatórias para o script rodar; sem elas, ele para com código 1. Faltou outra coluna (registro de versão antiga): o painel roda, diz em "Cuidados" quais faltam e o que ficou sem medir. Acrescente a coluna no fim da primeira linha; as linhas antigas ficam vazias nela.

## 10. Registro com outro formato

- **Separador ponto e vírgula** (planilha salva no Excel em português) e **BOM**: o script percebe sozinho.
- **Cabeçalho ou etapa em maiúsculas:** aceitos.
- **Data DD/MM/AAAA HH:MM:** aceita.
- **Cabeçalho com outros nomes** (CRM próprio): renomeie as colunas para os nomes do funil antes de rodar, ou peça à habilidade para montar a correspondência e confirmar com o advogado.
- **Uma linha por mensagem, e não por contato:** junte por código antes, ficando com a linha mais recente de cada contato.
- **Arquivo que falta, vazio ou só com o cabeçalho:** o script para com código 1 e diz o que houve. Ele nunca devolve um painel "sem nada a apontar" sem ter lido contato nenhum.
