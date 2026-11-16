# Modelo do caso de teste do escritório

Grave em `escritorio/04-base/casos-de-teste/experiencia/<nn>-<assunto-curto>.md` (ex.: `01-pericia-com-medo.md`). Caso real anonimizado: primeiro nome trocado, sem CPF, número do processo, telefone, endereço ou dado de saúde além do necessário. Código de teste no formato `C-0000-NNNN`, para nunca se confundir com cliente real. O gabarito é do advogado.

```markdown
---
documento: Caso de teste · experiência · [NN]
versao: 1
revisado_em: AAAA-MM-DD
dono: [ADVOGADO QUE ESCREVEU O GABARITO]
habilidades: [QUAIS HABILIDADES ESTE CASO TESTA]
---

# Caso [NN] · [ASSUNTO CURTO]

## A situação
- Tipo de caso: [TIPO]
- Fase na carteira: [FASE]
- Último contato: há [N] dias · Compromisso: [TIPO E EM QUANTOS DIAS, OU "nenhum"]
- Humor: [HUMOR] · Pediu para não receber: [SIM | NÃO]

## A mensagem (do jeito que chegou, anonimizada)
"[TEXTO]"

## O gabarito
- Caminho: [PESSOA AGORA | MENSAGEM A | LIGAÇÃO H | SÓ REGISTRAR]
- Urgência: [ALTA | NORMAL | BAIXA]
- O que a resposta precisa ter: [ITENS]
- O que não pode falhar: [EX.: "não confirmar a data que a IA deu", "não revelar a decisão por mensagem"]

## Resultado dos testes
| Data | Habilidade | Passou? | O que falhou | Ajuste feito |
|---|---|---|---|---|
```

Monte de 5 a 12 casos, cobrindo: um de cada momento de aflição do nicho, um cliente que traz resposta de IA ou print do tribunal, uma notícia ruim, um pedido de senha ou credencial, um pedido para parar de receber, e um caso comum sem nada de especial.
