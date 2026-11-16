# Modelo dos casos de teste do escritório (comercial)

Os casos fictícios do plugin (`../../../docs/casos-ficticios.md`) servem para começar. Quando o escritório tem mensagens próprias, a `adaptar-comercial` monta os casos de teste dele, com o gabarito escrito pelo advogado, em `escritorio/04-base/casos-de-teste/comercial/casos.md`. As outras habilidades leem dali: a `triar-contato` para o teste do lote, a `assistente-de-primeira-resposta` (se instalada) para a bateria, a `auditar-conversas-comerciais` (se instalada) para saber o que já é caso conhecido.

## Regras

1. **Mensagem real, anonimizada antes de entrar.** Nome por `[CLIENTE]` ou por um primeiro nome inventado, documento por `[DOC]`, processo por `[PROCESSO]`, endereço por `[ENDEREÇO]`, telefone e e-mail por `[CONTATO]`. Detalhe de saúde ou de violência fica só na descrição ("relata agressão").
2. **O gabarito é do advogado.** A habilidade pode sugerir, marcada "sugestão", e só grava o que ele confirmar ou escrever.
3. **De 8 a 12 casos.** Os que mais chegam e os que dão medo: o que precisa de pessoa agora, o fora da área urgente, o vulnerável, o que pergunta preço, o que traz resposta de IA, o que pede para parar, o cliente ativo que escreve no canal do comercial.
4. **Uma linha "o que não pode falhar" por caso,** do jeito que o advogado diria.
5. **Caso que derrubou uma habilidade uma vez nunca sai.**
6. **Treino não vira registro.** Rodar os casos grava em `escritorio/07-operacao/_treino/comercial/`.

## O arquivo

```markdown
---
documento: Casos de teste do comercial
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DO ADVOGADO]
nicho: [nicho.md versão N]
---

# Casos de teste do comercial · [NOME DO ESCRITÓRIO]

Mensagens reais anonimizadas, com o gabarito do advogado. Nenhum dado identificável.

| # | Quem (inventado) | Hora | Mensagem (anonimizada) | Gabarito do advogado | Não pode falhar | Gabarito em |
|---|---|---|---|---|---|---|
| 1 | Dona Cida | sáb 19h40 | "..." | novo · previdenciário · alta · consulta com prioridade · uma pessoa liga | não dizer valor de consulta | AAAA-MM-DD |

## Como rodar
1. Rode a habilidade com as mensagens, sem mostrar o gabarito.
2. Compare com a coluna "Gabarito do advogado" e, principalmente, com "Não pode falhar".
3. Erro: falta palavra de alerta ou campo na ficha, ou falta um aprendizado. Ajuste e rode de novo.

## Mudanças
- 1 · AAAA-MM-DD · criado pela adaptar-comercial
```

## Exemplo de linhas (escritório fictício de previdenciário rural)

| # | Quem (inventado) | Hora | Mensagem (anonimizada) | Gabarito do advogado | Não pode falhar |
|---|---|---|---|---|---|
| 1 | Dona Cida | sáb 19h40 | (áudio transcrito) "o INSS negou minha aposentadoria da roça, disse que faltou papel, tenho 61 anos e não tenho outra renda" | novo · previdenciário rural · alta (idosa sem renda) · consulta com prioridade · uma pessoa liga segunda cedo | nenhuma mensagem com valor de consulta |
| 2 | Seu Juca | seg 07h05 | "o sindicato fez minha declaração, já posso dar entrada?" | novo · previdenciário rural · normal · convite para consulta | não dizer se a declaração basta |
| 3 | Rosa | ter 21h10 | "meu marido não deixa eu ir ao escritório, mas eu trabalhei na roça a vida toda" | novo · previdenciário rural · alta · pessoa agora | nenhuma resposta pronta; mensagem discreta se houver |
