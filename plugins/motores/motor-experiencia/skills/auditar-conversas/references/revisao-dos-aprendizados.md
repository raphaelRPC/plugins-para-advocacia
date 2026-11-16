# Revisão mensal dos aprendizados da experiência

O arquivo `escritorio/04-base/comum/aprendizados-experiencia.md` cresce a cada correção que o escritório faz nas mensagens, roteiros e resumos para clientes. Sem revisão, ele acumula regras repetidas, regras que já viraram política e regras que ninguém segue. A revisão acontece uma vez por mês, ou quando o arquivo passa de 30 linhas `em uso` (`../../../docs/aprender-com-o-uso.md`, seção "Revisão"). Quando a auditoria do mês roda, a revisão vem junto e usa as conversas com clientes como prova.

## 1. Ler o arquivo inteiro

Monte uma tabela de trabalho, sem mudar nada ainda:

| Linha | Habilidade | Regra | Situação | Data | Aparece nas conversas? |
|---|---|---|---|---|---|

"Aparece nas conversas?" tem três respostas: **seguida** (a amostra mostra a regra sendo cumprida), **descumprida** (a amostra mostra o contrário, com o trecho), **sem caso** (a amostra não teve situação para testar).

## 2. As seis perguntas

Para cada linha, na ordem:

1. **Repete outra?** Duas regras com o mesmo efeito viram uma, com a redação mais clara. A outra vai para `retirada`, com a nota "juntada à linha [N]".
2. **Já é política?** Se a regra aparece em várias habilidades, ou o advogado diz "isso é sempre assim", proponha subir para o campo certo da ficha (por exemplo, `nunca_por_mensagem`, `resposta_ponte`, `maximo_sem_noticia`) ou para a jornada do tipo de caso. A linha vai para `retirada`, com a nota "incorporada à ficha: [campo]" ou "incorporada à jornada: [arquivo]".
3. **Ainda vale?** Mudou a política, a equipe, a área? A linha vai para `retirada`, com a nota do motivo.
4. **Está `em teste` há mais de 30 dias?** Pergunte ao advogado: vira `em uso` ou `retirada`.
5. **As conversas descumprem?** Regra `em uso` descumprida na amostra não se resolve com outra regra. Proponha: uma mensagem da biblioteca que já traga a regra pronta, um momento na jornada, uma linha na rotina, ou a combinação com a equipe. Se a regra é das habilidades (a IA não seguiu), proponha deixá-la mais concreta, com verbo, objeto e exemplo.
6. **Conflita com a ficha ou com a ética?** Com a ficha: mostre as duas versões e pergunte qual vale; ajuste as duas. Com as regras de ética do plugin: explique por que não pode ficar e proponha a versão que cabe.

## 3. Regras novas a partir das conversas

Correção que a equipe fez à mão em várias conversas, e que não está no arquivo, vira proposta de regra nova. Exemplo: a secretária troca "conclusos para despacho" por "o processo está com o juiz para o próximo passo" em todas as mensagens geradas; a proposta é "Traduzir 'conclusos para despacho' como 'o processo está com o juiz para o próximo passo, sem data para a decisão'", se ainda não estiver lá, e a mesma tradução no glossário do cliente.

Regra nova entra como `em teste`, com a data, e volta na revisão do mês seguinte.

## 4. Mostrar e aplicar

Mostre só as mudanças, nesta tabela:

| Linha | Hoje | Proposta | Motivo | Decisão |
|---|---|---|---|---|
| 3 | em uso: "Não usar 'fique tranquilo'" | retirada, juntada à linha 9 | mesma regra da linha 9 | |
| 6 | em uso: "Notícia de perícia negada só por ligação" | retirada, incorporada à ficha: `nunca_por_mensagem` | aparece em status, resumo e triagem | |
| 11 | em teste há 40 dias: "Cliente que já reclamou recebe notícia a cada 15 dias até fechar a reclamação" | em uso | carteira mostra os retornos cumpridos | |
| nova | (não existe) | em teste: "Pedido de senha recebe a resposta-padrão: nunca mandamos nem pedimos senha; oferecemos a página do caso" | 2 de 12 conversas com senha combinada | |

Com o ok, linha por linha:
- mude a situação e acrescente a nota na coluna "Situação" (ex.: "retirada · incorporada à ficha: nunca_por_mensagem · AAAA-MM-DD");
- nunca apague uma linha;
- regra que subiu para a ficha: grave o campo, suba a versão da ficha e acrescente a linha no histórico;
- suba a `versao` do arquivo de aprendizados e atualize `revisado_em`.

## 5. Exemplo com o Escritório Modelo (fictício)

Arquivo com 12 linhas `em uso` e 2 `em teste`. Amostra de 10 conversas com clientes ativos de março e abril.

- Linhas 3 e 9 dizem a mesma coisa sobre "fique tranquilo": juntadas na 9.
- Linha 6 ("Notícia de perícia negada só por ligação") aparece em três habilidades: sobe para `nunca_por_mensagem` na ficha.
- Linha 8 ("Explicar 'concluso' sem dar prazo") foi descumprida em 1 conversa (C-2026-0007), em que a resposta confirmou a previsão do ChatGPT. Proposta: a mensagem `cliente-com-ia` da biblioteca passa a trazer a explicação pronta, em vez de outra regra.
- Linha 11 (`em teste` há 40 dias, "Cliente que já reclamou recebe notícia a cada 15 dias até fechar a reclamação") virou `em uso` com o ok.
- Nova regra `em teste`: pedido de senha com resposta-padrão, tirada da conversa C-2026-0002.

Resultado: nenhuma linha apagada, ficha na versão seguinte com `nunca_por_mensagem` ampliado, uma mensagem da biblioteca ajustada.
