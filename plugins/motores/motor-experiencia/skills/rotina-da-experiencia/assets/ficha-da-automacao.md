# Modelo da ficha da automação

Copiar para `escritorio/05-automacoes/ciclo-da-experiencia/ficha.md` no modo configurar, preenchido com as respostas do advogado e os campos das fichas.

```markdown
---
documento: Ficha da automação · ciclo da experiência
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELO CICLO]
---

# Ciclo da experiência

## O que faz
Todo dia útil, lê a carteira de clientes ativos, a pasta de entrada, as passagens do comercial e, se houver conector, a agenda e o e-mail. Separa o que é para uma pessoa agora, aponta quem está sem notícia além da régua, compromissos, documentos e resumos, rascunha o que é A, passa pelo revisor e grava a fila e o resumo do dia.

## O que não faz
- Não envia mensagem, e-mail ou página a ninguém.
- Não publica página do caso.
- Não muda fase, humor, reclamação ou encerramento na carteira.
- Não escreve notícia ruim, resultado de decisão ou proposta de acordo.
- Não escreve rotina para quem pediu para não receber.
- Não lê nem grava fora de `escritorio/` e dos conectores listados. Não apaga arquivo.

## Como roda
- Jeito: [agente pelo /motor-experiencia:ciclo | tarefa agendada que chama o ciclo | ciclo à mão no chat]
- Dias e hora: [EX.: dias úteis, às 8h]
- Se não rodar até [HORA]: [FUNÇÃO] roda à mão (plano em "Quando não roda").

## Quem lê
- Resumo do dia inteiro: [FUNÇÃO]
- Fila de rascunhos: [FUNÇÃO], [HORÁRIO] (quem_aprova_rascunhos)
- PESSOA AGORA: [FUNÇÃO], até [HORA]

## Fontes
| Fonte | Caminho ou conector | Obrigatória |
|---|---|---|
| Carteira | `07-operacao/experiencia/carteira.csv` | sim |
| Entrada | `07-operacao/experiencia/entrada/` | não |
| Passagens do comercial | `07-operacao/comercial/passagens/` | não |
| Agenda | [CONECTOR OU "sem conector"] (conferir na configuração da conta) | não |
| E-mail | [CONECTOR OU "sem conector"] (conferir na configuração da conta) | não |

## Critérios (das fichas)
| Critério | Valor | Campo |
|---|---|---|
| Máximo sem notícia | [N] dias corridos | X: maximo_sem_noticia |
| Primeira resposta ao cliente | [N] horas úteis | X: primeira_resposta_cliente_ativo |
| Cobrança de documentos | [N] e [N] dias | X: cobranca_de_documentos |
| Lembrete de compromisso | [N] dias e véspera | X: lembrete_de_compromisso |
| Dia do resumo mensal | dia [N] | X: resumo_mensal |
| Feriados do ano | [LISTA OU "conferir a cada mês"] | (a rotina pergunta) |
| Registro do envio do resumo | [sim: quem envia marca `status: enviado` no resumo do mês \| não: `aprovado` basta, e a rotina e o lote rodam com `--sem-registro-de-envio`] | (a rotina pergunta) |

## Rotinas próprias no ciclo
| Rotina | Habilidade do escritório | Gatilho na carteira ou no histórico |
|---|---|---|
| [NOME OU "nenhuma"] | [04-base/habilidades-do-escritorio/NOME/] | [EX.: boas-vindas enviada ontem] |

## Onde grava
- Resumo do dia: `07-operacao/experiencia/rotina/AAAA-MM-DD.md`
- Fila: `07-operacao/experiencia/fila/AAAA-MM-DD/`
- Uma linha por rodada: `05-automacoes/ciclo-da-experiencia/registro-de-uso.md`

## Quando não roda
[O PLANO COMBINADO, A PARTIR DE references/quando-o-ciclo-nao-roda.md DA HABILIDADE]

## Revisão
- A cada mês, ou quando uma ficha mudar um critério.
- Dois dias úteis seguidos sem rodar: revisar o jeito de rodar.

## Histórico
- 1 · AAAA-MM-DD · ciclo configurado, [JEITO], às [HORA]
```
