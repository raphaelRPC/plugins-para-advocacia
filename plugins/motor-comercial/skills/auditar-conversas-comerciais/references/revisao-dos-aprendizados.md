# Revisão mensal dos aprendizados comerciais

O arquivo `escritorio/04-base/comum/aprendizados-comercial.md` cresce a cada correção. Sem revisão, ele acumula regras repetidas, regras que já viraram política e regras que ninguém segue. A revisão acontece uma vez por mês, ou quando o arquivo passa de 30 linhas `em uso` (`../../../docs/aprender-com-o-uso.md`, seção "Revisão"). Quando a auditoria do mês roda, a revisão vem junto e usa as conversas como prova.

## 1. Ler o arquivo inteiro

Monte uma tabela de trabalho, sem mudar nada ainda:

| Linha | Habilidade | Regra | Situação | Data | Aparece nas conversas? |
|---|---|---|---|---|---|

"Aparece nas conversas?" tem três respostas: **seguida** (a amostra mostra a regra cumprida), **descumprida** (a amostra mostra o contrário, com o trecho), **sem caso** (a amostra não teve situação para testar).

## 2. As seis perguntas

Para cada linha, na ordem:

1. **Repete outra?** Duas regras com o mesmo efeito viram uma, com a redação mais clara. A outra vai para `retirada`, com a nota "juntada à linha [N]".
2. **Já é política?** Se a regra aparece em várias habilidades, ou o advogado diz "isso é sempre assim", proponha subir para o campo certo da ficha (do escritório, se vale para os dois plugins; comercial, se é só do comercial). A linha vai para `retirada`, com a nota "incorporada à ficha: [campo]".
3. **Ainda vale?** Mudou a política, a equipe, o nicho? A linha vai para `retirada`, com a nota do motivo.
4. **Está `em teste` há mais de 30 dias?** Pergunte ao advogado: vira `em uso` ou `retirada`.
5. **As conversas descumprem?** Regra `em uso` descumprida na amostra não se resolve com outra regra. Proponha: um modelo da biblioteca comercial que já traga a regra pronta, uma linha na rotina, ou a combinação com a equipe. Se quem não seguiu foi a habilidade, proponha deixar a regra mais concreta, com verbo, objeto e exemplo.
6. **Conflita com a ficha ou com a ética?** Com a ficha: mostre as duas versões e pergunte qual vale; ajuste as duas. Com as regras de ética do plugin: explique por que não pode ficar e proponha a versão que cabe. Exemplo: "Oferecer 10% para quem fechar no mesmo dia" não pode ficar (desconto como isca); a versão que cabe é "Proposta com as formas de pagamento da ficha, sem condição por prazo de decisão".

## 3. Regras novas a partir das conversas

Correção que a equipe fez à mão em várias conversas e que não está no arquivo vira proposta de regra nova. Exemplo: a secretária troca "Prezado" por "Oi, [NOME]" em todas as mensagens geradas: proposta "Não abrir mensagem com prezado ou prezada", se ainda não estiver lá.

Regra nova entra como `em teste`, com a data, e volta na revisão do mês seguinte.

## 4. Mostrar e aplicar

Mostre só as mudanças:

| Linha | Hoje | Proposta | Motivo | Decisão |
|---|---|---|---|---|
| 4 | em uso: "Não usar 'prezado'" | retirada, juntada à linha 9 | mesma regra da linha 9 | |
| 7 | em uso: "Parcelamento sem juros em até 6 vezes" | retirada, incorporada à ficha: `entrada_e_parcelas` | aparece em proposta, objeções e retorno | |
| 12 | em teste há 45 dias: "Contato de cliente antigo entra como origem cliente-antigo" | em uso | o painel usou nos dois últimos meses sem correção | |
| nova | (não existe) | em teste: "Ao responder 'achei caro', nunca citar o outro escritório; falar do que está incluído" | 2 de 10 conversas citaram o colega | |

Com o ok, linha por linha:
- mude a situação e acrescente a nota na coluna "Situação" (ex.: "retirada · incorporada à ficha: entrada_e_parcelas · AAAA-MM-DD");
- nunca apague uma linha;
- regra que subiu para a ficha: grave o campo, suba a versão da ficha e acrescente a linha no histórico;
- suba a `versao` do arquivo de aprendizados e atualize `revisado_em`.

## 5. Exemplo com o Escritório Modelo (fictício)

Arquivo com 14 linhas `em uso` e 3 `em teste`. Amostra de 10 conversas de 03/2026.

- Linhas 2 e 11 dizem a mesma coisa sobre pensão com criança (vai para a advogada titular, prioridade alta): juntadas na 2.
- Linha 5 ("Proposta com validade de 7 dias") aparece em três habilidades: sobe para `validade_da_proposta` na ficha comercial.
- Linha 8 ("Fora do horário, nunca prometer retorno antes das 9h") foi descumprida em 2 conversas, as duas pela mesma mensagem de fora do horário, que dizia "te respondemos logo cedo". Proposta: ajustar o modelo `fora-do-horario` para "a partir das 9h", em vez de outra regra.
- Linha 15 (`em teste` há 40 dias, "Divórcio com imóvel vai direto para a advogada") virou `em uso` com o ok.
- Nova regra `em teste`: "Contato que manda só áudio recebe proposta de ligação curta", tirada de 3 conversas em que a secretária fez isso à mão.

Resultado: 14 linhas `em uso` viraram 13, nenhuma apagada, ficha comercial na versão seguinte com `validade_da_proposta` preenchido, um modelo da biblioteca ajustado.
