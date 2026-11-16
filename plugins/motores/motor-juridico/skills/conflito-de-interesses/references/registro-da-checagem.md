# O registro da checagem de conflito

Leia no passo 4. O script cria o arquivo `escritorio/07-operacao/juridico/casos/<codigo>/conflito-de-interesses.md` com o cabeçalho e o resultado. A habilidade completa a decisão com o advogado. Cada nova checagem do mesmo caso (parte nova que apareceu depois) entra como uma seção a mais no mesmo arquivo; nada é apagado.

## Modelo

```markdown
---
documento: Checagem de conflito de interesses · C-AAAA-NNNN
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM DECIDIU]
---

# Conflito de interesses · C-AAAA-NNNN

## Checagem de conflito · C-AAAA-NNNN · AAAA-MM-DD
(o que o script devolveu: se acusou, a base lida, as partes checadas e a tabela)

Decisão do advogado: aceitar | recusar | aceitar com as providências do Código de Ética e Disciplina da OAB [CONFERIR: artigos sobre conflito de interesses e sigilo, redação vigente] | pedir mais informação
Quem decidiu: [FUNÇÃO E PRIMEIRO NOME]
Em: AAAA-MM-DD
O que foi feito: (uma linha por providência, sem o conteúdo de conversa com o outro cliente)
Partes que entram na base: (as linhas para o partes.csv, mostradas e gravadas com o ok)
```

## Os textos de cada decisão

| Decisão | O que a habilidade escreve no registro | O que acontece depois |
|---|---|---|
| Aceitar, sem coincidência | "Nada na base de [N] registros em AAAA-MM-DD. Aceito por [FUNÇÃO]." | Dossiê; partes na base |
| Aceitar, com coincidência sem conflito provável | "Coincidência com [CÓDIGO], papel [PAPEL]. O advogado avaliou e aceitou." | Dossiê; partes na base |
| Aceitar, com conflito provável | "Conflito provável com [CÓDIGO]. O advogado decidiu aceitar e registrou as providências." Sem as providências registradas, o caso fica em ADVOGADO AGORA | Dossiê só depois das providências |
| Recusar | "Recusado por conflito em AAAA-MM-DD, por [FUNÇÃO]." | Mensagem de recusa sem motivo; o caso não entra no `pecas.csv` ou vai para `suspensa` |
| Pedir mais informação | "Falta: [O QUE]. Pedido a [QUEM] em AAAA-MM-DD." | Fica em ADVOGADO AGORA até a resposta |

## O que o registro nunca leva

- O conteúdo do caso do outro cliente (o que ele contou, a estratégia dele, valores).
- A opinião da IA sobre se há ou não conflito. O registro leva o que a base mostrou e o que o advogado decidiu.
- CPF, endereço ou telefone de qualquer parte.

## A mensagem de recusa ao contato

A recusa por conflito nunca diz o motivo. Base para a advogada adaptar (ou a chave `recusa-educada` da biblioteca do motor-comercial, se instalado):

```
[NOME], obrigada por procurar o escritório. Depois de uma checagem interna, não vamos poder assumir o seu caso.

Para não perder tempo, sugerimos procurar [ENCAMINHAMENTO DA FICHA: encaminhamos_para].
```

Quem envia é a pessoa, depois de ler. `[NOME]` e o encaminhamento saem da ficha e da conversa; nada no texto fala de outro cliente.
