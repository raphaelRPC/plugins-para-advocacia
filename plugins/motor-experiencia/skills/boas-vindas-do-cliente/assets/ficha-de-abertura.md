# Modelo da abertura do cliente

Grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/abertura.md` (no ciclo, `abertura-rascunho.md` até a pessoa aprovar). É o mínimo para qualquer pessoa da equipe (e o agente) saber, sem rolar a conversa, quem cuida, o que foi combinado e o que está pendente. Dados completos (telefone, documento, endereço, número do processo) ficam no sistema do escritório, fora desta abertura.

```markdown
---
documento: Abertura · [CÓDIGO]
versao: 1
revisado_em: AAAA-MM-DD
dono: [ADVOGADO RESPONSÁVEL]
status: aprovada        # rascunho | aprovada
---

# Abertura · [CÓDIGO] · [NOME CURTO]

## O caso
- Área: [ÁREA]
- Tipo de caso: [ATÉ 5 PALAVRAS, SEM DADO SENSÍVEL]
- Contrato assinado em: [AAAA-MM-DD] (confirmado por [QUEM OU "passagem do comercial"])
- Escopo, em uma linha: [DA PASSAGEM, DA PROPOSTA OU DO CONTRATO]
- Não inclui: [DA PASSAGEM OU DO CONTRATO, OU "A CONFIRMAR"]
- O que foi prometido na venda: [DA PASSAGEM: ex. "ligação de retorno em toda movimentação"]
- Passagem do comercial: [07-operacao/comercial/passagens/CÓDIGO.md OU "não houve"]
- Jornada do tipo de caso: [04-base/relacionamento-com-o-cliente/jornada-TIPO.md OU "ainda não existe"]
- Dados completos e número do processo: [ONDE, EX.: "sistema jurídico do escritório"]

## Quem cuida
- Advogado responsável: [FUNÇÃO OU NOME]
- No dia a dia: [FUNÇÃO OU PRIMEIRO NOME]
- Substituto: [FUNÇÃO OU PRIMEIRO NOME]

## O combinado de comunicação
- Canal oficial: [CANAL]
- Horário: [HORÁRIO DE ATENDIMENTO]
- Prazo de resposta: [PRIMEIRA RESPOSTA AO CLIENTE ATIVO]
- Notícias do caso (régua): [DA JORNADA OU DA FICHA, OU "A DEFINIR"]
- Resumo mensal: [SIM, FORMATO E DIA | NÃO | PEDIU PARA NÃO RECEBER]
- Ligação e áudio: [PREFERÊNCIA DO CLIENTE E REGRA DO ESCRITÓRIO]
- Quem mais pode receber informação do caso: [NINGUÉM | QUEM, COM AUTORIZAÇÃO DE AAAA-MM-DD]
- Cuidado com o canal: [NENHUM | EX.: "confirmar canal seguro antes de cada mensagem"]

## Próximos passos
| O quê | Quem | Até |
|---|---|---|
| [PRIMEIRO ATO DO ESCRITÓRIO] | [QUEM] | [AAAA-MM-DD] |
| [PRÓXIMO] | [QUEM] | [AAAA-MM-DD OU "sem data"] |

## Documentos pendentes
| Documento | Onde conseguir | Pedido em | Chegou em |
|---|---|---|---|
| [DOCUMENTO] | [ONDE] | [AAAA-MM-DD] | |

Controle detalhado: [clientes/CÓDIGO/documentos.md, SE A checklist-de-documentos ESTIVER EM USO]

## Mensagens enviadas na entrada
| Data | Chave | Quem enviou |
|---|---|---|
| [AAAA-MM-DD] | boas-vindas-cliente | [QUEM] |

## Em aberto
- [O QUE FICOU A DEFINIR OU A CONFIRMAR; É AQUI, E NÃO NA MENSAGEM, QUE AS MARCAÇÕES FICAM]
```

Nunca entram nesta abertura: CPF, RG, telefone, endereço, senha ou login (gov.br, Meu INSS, banco), dado de saúde além do que o tipo de caso exige, nome de criança ou da outra parte em caso de família, valor da causa.
