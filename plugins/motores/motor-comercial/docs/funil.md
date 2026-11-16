# O funil e o registro de contatos

Todo contato que chega ao escritório e ainda não é cliente passa pelas mesmas etapas, do primeiro "oi" ao contrato assinado. O registro é uma planilha simples que as habilidades leem e atualizam. É ele que permite à rotina dizer "três contatos sem resposta há mais de duas horas" e ao painel dizer de onde vêm os clientes que fecham.

Quem já é cliente não entra aqui. Mensagem de cliente ativo vai para o plugin `motor-experiencia` (se instalado), na `triar-mensagem-do-cliente`. Sem ele, a triagem avisa que é cliente e entrega à pessoa que cuida do caso.

## As etapas

| Etapa | Quer dizer | Quem move | Próxima etapa |
|---|---|---|---|
| `novo` | Registrado, ninguém classificou ainda | entrada manual, agente do ciclo | `triado` |
| `triado` | Classificado: área, urgência, caminho | `triar-contato` | `consulta-agendada`, `encaminhado`, `recusado`, `perdido` |
| `consulta-agendada` | Data marcada | `agenda-da-consulta`, `roteiro-da-consulta` ou a pessoa | `consulta-feita` ou `nao-compareceu` |
| `nao-compareceu` | Faltou à consulta | a pessoa | `consulta-agendada` (remarcou) ou `perdido` |
| `consulta-feita` | A consulta aconteceu | `ata-da-consulta` ou a pessoa | `proposta-enviada`, `sem-caso` ou `perdido` |
| `proposta-enviada` | A proposta saiu (alguém confirmou o envio) | `proposta-de-honorarios` | `fechado`, `negociando` ou `perdido` |
| `negociando` | Pediu ajuste ou tem dúvida sobre a proposta | `objecoes-comerciais` ou a pessoa | `proposta-enviada` (versão nova), `fechado` ou `perdido` |
| `fechado` | Contrato assinado | o advogado | sai do funil pela `passagem-para-o-caso` |
| `encaminhado` | Mandado para outro profissional ou órgão | o advogado, com sugestão da triagem | fim |
| `recusado` | O escritório não atende | o advogado, com sugestão da triagem | fim |
| `sem-caso` | Na consulta, não havia ação viável | o advogado | fim |
| `perdido` | Desistiu, fechou com outro, sumiu | o advogado, com sugestão do `follow-up` | fim, com o motivo |

Só uma pessoa move para `fechado`, `perdido`, `sem-caso`, `recusado` e `encaminhado`. A IA sugere, a pessoa confirma. Contato que volta depois de `perdido`, `encaminhado` ou `recusado` volta para `triado`, com "reaberto" no `proximo_passo`.

## O arquivo `contatos.csv`

Fica em `escritorio/07-operacao/comercial/contatos.csv`, separado por vírgula, com esta primeira linha:

```
codigo,entrada,canal,origem,nome_curto,tipo,area,assunto,urgencia,etapa,responsavel,proximo_passo,data_proximo_passo,primeira_resposta,valor_proposta,motivo_perda,perdido_na_etapa,pediu_para_parar,atualizado_em
```

| Coluna | O que vai | Exemplo |
|---|---|---|
| `codigo` | C, o ano e um número sequencial, nunca reaproveitado. Segue o mesmo no caso e na experiência | C-2026-0001 |
| `entrada` | Data e hora da primeira mensagem, AAAA-MM-DD HH:MM | 2026-03-10 21:14 |
| `canal` | whatsapp, email, telefone, instagram, site, presencial | whatsapp |
| `origem` | Uma das opções de `origem_dos_contatos` da ficha comercial | indicacao |
| `nome_curto` | Primeiro nome ou iniciais, nada mais | Marta |
| `tipo` | `novo` (primeira vez) ou `antigo` (já falou com o escritório antes do registro existir) | novo |
| `area` | Uma das áreas da ficha do escritório, `fora-da-area` ou `a-confirmar` | previdenciario |
| `assunto` | Até 8 palavras, sem dado sensível | benefício cortado; quer recorrer |
| `urgencia` | `alta`, `normal` ou `baixa` (árvore da `triar-contato`) | alta |
| `etapa` | Uma das etapas acima | triado |
| `responsavel` | Função ou primeiro nome de quem cuida | secretaria |
| `proximo_passo` | O que precisa acontecer, com verbo. Na régua de retorno: "retorno 1 de 3", "retorno combinado", "confirmar perdido" | retorno 1 de 3 |
| `data_proximo_passo` | AAAA-MM-DD. Em `consulta-agendada`, é a data da consulta | 2026-03-12 |
| `primeira_resposta` | Data e hora em que uma pessoa respondeu pela primeira vez. Vazio até alguém responder | 2026-03-11 09:05 |
| `valor_proposta` | Total da parte fixa, só número, já descontada a consulta quando a ficha diz que abate. Vazio em proposta só de êxito | 4500 |
| `motivo_perda` | `preco`, `fechou-com-outro`, `desistiu`, `sem-resposta`, `outro` | sem-resposta |
| `perdido_na_etapa` | A etapa em que estava quando virou `perdido` | proposta-enviada |
| `pediu_para_parar` | `sim` ou `nao` | nao |
| `atualizado_em` | AAAA-MM-DD | 2026-03-11 |

## Regras do registro

1. **Sem resposta** quer dizer `primeira_resposta` vazia. Vale em qualquer etapa antes de `consulta-agendada`. O prazo conta da `entrada`, em horas úteis do `horario_de_atendimento` da ficha do escritório.
2. **A triagem já deixa a régua armada.** Quando o caminho é convite para consulta, a linha sai com `proximo_passo = retorno 1 de N` e a `data_proximo_passo` do primeiro retorno da régua de "não agendou" (`follow_up` da ficha comercial). Assim ninguém some do retorno.
3. **Régua de retorno em dias corridos.** Prazo de resposta em horas úteis. Os dois ficam escritos assim na ficha.
4. **Marcador de pessoa:** quando a triagem manda o contato para uma pessoa, o `proximo_passo` começa com `pessoa agora:` (parada imediata, urgência) ou `pessoa liga:` (vulnerabilidade). Os scripts acham esses contatos por esse começo.
5. **Fora da régua, sempre:** urgência `alta` sem pessoa designada, área `fora-da-area`, parada imediata, caso sensível (violência, criança, risco), `pediu_para_parar = sim`. Esses contatos aparecem para uma pessoa, nunca numa lista de mensagem pronta.
6. **Remarcação:** pedido de remarcar põe `proximo_passo = remarcar consulta (era AAAA-MM-DD)` e a `data_proximo_passo` de hoje, até a nova data ser marcada.
7. **Proposta nova:** de `negociando`, quando sai a versão 2, a etapa volta para `proposta-enviada` e o `valor_proposta` passa a ser o da versão nova.
8. **Mínimo de dados.** Nada de telefone, CPF, endereço, número de processo ou detalhe de saúde. Quem precisa do contato completo vai ao sistema do escritório.
9. **Sem vírgula dentro dos campos.** Use ponto e vírgula dentro do texto ou troque a frase. Os scripts leem também a planilha salva pelo Excel (ponto e vírgula, com ou sem BOM).
10. **Uma linha por contato.** Mudou de etapa, atualiza a linha.
11. **Mostrar antes de gravar,** ou gravar em lote depois de mostrar a tabela. O agente do ciclo mexe só nas etapas `novo` e `triado` e nas colunas `urgencia`, `proximo_passo`, `data_proximo_passo` e `atualizado_em`. Numa linha nova, preenche também `codigo`, `entrada`, `canal`, `origem` (ou `[A CONFIRMAR]`), `nome_curto`, `tipo`, `area`, `assunto`, `responsavel` e `pediu_para_parar = nao`, e deixa `primeira_resposta` vazia.
12. **Treino não entra.** Casos fictícios vão para `escritorio/07-operacao/_treino/comercial/contatos.csv`.
13. **Quem já tem CRM** pode continuar nele: o registro vira a exportação da semana, ou o advogado diz que o CRM é a fonte e as habilidades só leem o que ele colar.
