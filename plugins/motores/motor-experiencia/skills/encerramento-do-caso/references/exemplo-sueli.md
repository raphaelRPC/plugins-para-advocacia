# Exemplo resolvido: a Sueli (caso fictício)

Mensagem 7 de `../../../docs/casos-ficticios.md`. Escritório Modelo, Belo Horizonte/MG. Hoje é sexta, 2026-04-10. Tudo deste exemplo grava em `escritorio/07-operacao/_treino/experiencia/`. Nenhuma pessoa, número ou processo existe. Os valores ficam em aberto de propósito: nesta habilidade, nenhum número sai da IA.

## A mensagem

Sueli (C-2025-0091, família, alimentos, fase `encerramento`), 14h00:

> "Quando eu recebo o dinheiro do acordo? E quanto fica para vocês?"

Na carteira: acordo homologado, `ultimo_contato = 2026-04-03`, `humor = tranquilo`, observação "falta prestação de contas".

## Resposta-ponte (A, a advogada lê)

> "Oi, Sueli! Recebi sua pergunta. Você vai ter tudo por escrito. A Dra. está fechando a prestação de contas, com o valor que entrou, a parte do escritório, as despesas e o que vai para você. Até terça eu te mando."

A carteira ganha `proximo_contato = 2026-04-14` e `motivo_proximo_contato = retorno-combinado` (com o ok da advogada).

## Passo 1. Como terminou
"Acordo, resultado bom." Não precisa de ligação antes. Segue.

## Passo 2. Os números, um por vez

A habilidade pergunta e anota a fonte:

| Pergunta | Resposta da advogada | Fonte |
|---|---|---|
| Quanto entrou, e de onde? | "Ainda não sei o valor exato do depósito dos atrasados; vou olhar o extrato." | `[A PREENCHER]`, extrato da conta judicial |
| Honorários e base | "O percentual do contrato sobre os atrasados." | contrato de honorários, `[CONFERIR]` o percentual |
| Honorários pagos pela outra parte | "Não houve." | termo do acordo |
| Despesas | "Só cópias e autenticações; tenho os recibos." | recibos, `[A PREENCHER]` o valor |
| Prazo do repasse | "Até 5 dias úteis depois do levantamento, como no contrato." | contrato e ficha |

## Passo 3. O rascunho

Trecho do `_treino/experiencia/clientes/C-2025-0091/prestacao-de-contas.md`:

```markdown
## Antes de enviar (interno, não vai para o cliente)

- Quem confere: advogada titular · Sigla: A
- De onde vieram os números: extrato da conta judicial (a trazer), contrato de honorários, recibos de cópias

**Conferências dos valores**

- [ ] Valor recebido igual ao extrato da conta judicial `[CONFERIR]`.
- [ ] Honorários: o percentual do contrato sobre os atrasados `[CONFERIR]`.
- [ ] Despesas: recibos de cópias e autenticações.
- [ ] A conta fecha.
- [ ] Prazo do repasse: até 5 dias úteis depois do levantamento.
...

**Pendências**

- [ ] Valor recebido `[A PREENCHER]`: a advogada traz o extrato.
- [ ] Valor das despesas `[A PREENCHER]`: somar os recibos.

<!-- fim: antes de enviar -->

# Prestação de contas

**Escritório Modelo** · Belo Horizonte/MG · 2026-04-14

Para: Sueli · Caso: alimentos (acordo)

Como combinamos, aqui está, por escrito, tudo o que entrou no seu caso, o que fica com o escritório e o que vai para você.

## O que aconteceu no caso

O acordo sobre a pensão foi aprovado pelo juiz. Isso quer dizer que ele vale como uma decisão: se não for cumprido, dá para cobrar na Justiça.

## Os valores

| Item | Valor | De onde vem |
|---|---|---|
| Valor recebido no caso | R$ [VALOR RECEBIDO] | depósito dos valores atrasados da pensão |
| Honorários do escritório | R$ [VALOR DOS HONORÁRIOS] | o percentual combinado no contrato |
...
```

## Passo 6. O script

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" escritorio/07-operacao/_treino/experiencia/clientes/C-2025-0091/prestacao-de-contas.md --so-conferir
```

Saída (resumo): "NÃO ESTÁ PRONTO PARA ENVIAR: 4 campo(s) em maiúsculas; N conferência(s) do 'Antes de enviar' sem marcar." A lista mostra `[VALOR RECEBIDO]`, `[VALOR DOS HONORÁRIOS]`, `[VALOR DAS DESPESAS]` e `[VALOR DO REPASSE]`. Rodado sem `--so-conferir` nesse momento, o script não cria o .docx: sai com código 2 e repete a lista. Com `--forcar`, criaria o arquivo com os campos em amarelo, só para ver o visual.

Na segunda, a advogada traz o extrato e os recibos. A habilidade preenche os quatro campos com os números dela, faz a conta, mostra, e a advogada confere item por item, trocando `- [ ]` por `- [x]`. O script agora diz "PRONTO PARA ENVIAR" e gera o .docx sem a parte interna.

## Passo 4. O que muda (escolhido de references/o-que-muda-por-area.md, família, conferido pela advogada)

- A pensão passa a ser depositada todo mês na data do acordo. Guarde os comprovantes.
- Se um pagamento atrasar, fale com a gente. Dá para cobrar na Justiça, e a gente te explica como.
- Se a situação de quem paga ou de quem recebe mudar muito, a pensão pode ser revista. Antes de combinar qualquer mudança fora do processo, fale com a gente.

## Passo 5. Documentos
`guarda_de_documentos` está `[A PREENCHER]` na ficha do Escritório Modelo. A habilidade pergunta; a advogada responde "devolvemos a certidão original em mãos; guardamos cópia digital pelo prazo da nossa política" e marca o prazo para conferir `[CONFERIR]`. A pendência fica no cabeçalho interno, e a habilidade oferece gravar o campo na ficha.

## Passo 7. A mensagem
A ficha diz "resumo em PDF", e a Sueli prefere receber por mensagem. Sai a `encerramento-resultado-bom`, com o .docx (ou o PDF salvo dele) em anexo, para a advogada ler e a secretária enviar.

## Passo 9. Carteira e ganchos

| Momento | Coluna | Valor |
|---|---|---|
| Prestação de contas enviada, repasse pendente | `fase` | encerramento |
| | `proximo_contato` | data do repasse |
| | `motivo_proximo_contato` | retorno-combinado |
| Repasse feito e documento entregue (com a advogada) | `fase` | encerrado |
| | `encerrado_em` | a data |

Ganchos: a ficha do Escritório Modelo não tem `pesquisa_quando` preenchido; a habilidade pergunta e a advogada decide mandar a pesquisa 7 dias depois do repasse (`pesquisa-de-satisfacao`, se instalada). A Sueli aceitou a mensagem anual (`relacionamento-depois-do-caso`, se instalada).

## O que este exemplo testa
- Nenhum valor aparece antes de a advogada dar o número.
- O texto da cliente não tem marcação; as conferências ficam no cabeçalho interno e o script diz se está pronto.
- A carteira só vira `encerrado` depois do repasse.
- O "o que muda" é conferido e escrito em linguagem da cliente.
