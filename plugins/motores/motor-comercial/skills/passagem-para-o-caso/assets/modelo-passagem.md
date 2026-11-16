---
documento: Ficha de passagem
codigo: [CÓDIGO]
versao: 1
revisado_em: AAAA-MM-DD
dono: [QUEM FEZ A PASSAGEM]
status: rascunho
---

# Passagem · [CÓDIGO] · [PRIMEIRO NOME]

> O que o comercial entrega a quem vai cuidar do caso. Documento interno: nunca vai para o cliente. Mínimo de dados: qualificação, documentos, número do processo e detalhes de saúde ficam no sistema do escritório. `status` vira `conferida` quando quem cuida do caso leu e confirmou.

## 1. Em três linhas

[Quem é (primeiro nome e área), o que contratou e qual é o primeiro passo do escritório.]

## 2. Quem cuida

| Papel | Quem (função ou primeiro nome) |
|---|---|
| Responsável pelo caso | [RESPONSÁVEL] |
| Fala com o cliente no dia a dia | [QUEM] |
| Substituto | [SUBSTITUTO, de `substituto` da ficha do escritório] |
| Quem mais pode falar pelo cliente (só com autorização escrita dele) | [NINGUÉM OU QUEM, E ONDE ESTÁ A AUTORIZAÇÃO] |

## 3. O caso contratado

- Área e tipo de caso: [ÁREA] · [TIPO DE CASO, ATÉ 5 PALAVRAS]
- Contrato assinado em: [DATA] · arquivo: `07-operacao/comercial/contratos/[CÓDIGO]-contrato-v[N].md`
- Proposta aceita: `07-operacao/comercial/propostas/[CÓDIGO]-proposta-v[N].md`

**O que vamos fazer** (igual ao contrato)

- [ITEM]

**O que não está incluído** (igual ao contrato)

- [ITEM]

## 4. Valores e pagamento

- Modelo: [FIXO, ÊXITO, MISTO OU MENSAL]
- Total da parte fixa: [VALOR] · consulta abatida: [SIM OU NÃO]
- Forma escolhida: [À VISTA EM DATA, OU ENTRADA DE VALOR EM DATA E N PARCELAS DE VALOR TODO DIA X]
- Êxito: [PERCENTUAL, BASE E MOMENTO, OU "não há"]
- Despesas combinadas: [COMO O CONTRATO DIZ]
- Quem acompanha os pagamentos: [QUEM]

## 5. O que foi prometido ou combinado com o cliente

| Quando | Onde | O que foi dito | Quem cumpre | Até quando |
|---|---|---|---|---|
| [DATA] | [consulta, proposta, contrato ou mensagem enviada] | [FRASE CURTA] | [QUEM] | [DATA OU "sempre"] |

Só entra o que está numa fonte (ata, proposta, contrato, mensagem enviada) ou o que o advogado confirmou nesta passagem.

## 6. Prazos ditos ao cliente

[O que o cliente ouviu sobre tempo, do jeito que ouviu, com a fonte. Ex.: "na consulta: o pedido sai em até 10 dias depois que os documentos chegarem". Se alguma frase soa como prazo de decisão ou promessa de resultado, ela vem marcada para o advogado.]

## 7. Documentos pendentes

| Documento | Onde o cliente consegue | Pedido em | Combinado para |
|---|---|---|---|
| [DOCUMENTO] | [ONDE] | [DATA] | [DATA] |

O controle do que chega fica com a `checklist-de-documentos` do motor-experiencia, em `07-operacao/experiencia/clientes/[CÓDIGO]/documentos.md`.

## 8. Como o cliente prefere ser contatado

- Canal: [CANAL] · horário que funciona para ele: [HORÁRIO OU "não disse"]
- Tratamento: [VOCÊ, SENHOR OU SENHORA, PELO NOME]
- Texto ou áudio: [O QUE ELE PREFERE]
- Notícia importante: [POR LIGAÇÃO, ANTES DA MENSAGEM]

## 9. Humor e cuidados

- Humor ao fechar: [TRANQUILO, ANSIOSO, INSATISFEITO OU A-CONFIRMAR]
- O que preocupa o cliente: [EM UMA FRASE, NAS PALAVRAS DELE]
- Cuidados: [EX.: "questão de saúde envolvida; detalhes com a advogada"; "lê pouco, prefere ligação"]

## 10. O que não está aqui

Qualificação completa, documentos, número do processo, dado de saúde e dado de criança ficam em [ONDE, de `historico_do_cliente` e `sistema_juridico` da ficha do escritório].

## 11. Próximos passos da passagem

- [ ] Boas-vindas ao cliente: [QUEM] até [DATA] (`boas-vindas-do-cliente`, do motor-experiencia, se instalado)
- [ ] Linha na carteira: [FEITA EM DATA, OU "sem motor-experiencia: linha guardada abaixo"]
- [ ] Aviso a quem cuida do caso: [ENVIADO EM DATA, POR ONDE]
- [ ] Pasta do cliente no sistema do escritório: [QUEM ABRE]

## 12. Para a carteira (só quando o motor-experiencia ainda não está em uso)

```
[LINHA DA CARTEIRA NO FORMATO DE docs/carteira.md DO MOTOR-EXPERIENCIA]
```
