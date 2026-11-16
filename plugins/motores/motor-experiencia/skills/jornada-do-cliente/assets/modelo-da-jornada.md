# Modelo da jornada por tipo de caso

Grave em `escritorio/04-base/relacionamento-com-o-cliente/jornada-<tipo-de-caso>.md` (nome em minúsculas, sem acento, hífen entre palavras; ex.: `jornada-bpc-idoso.md`). É o documento que o agente de suporte, a `status-para-o-cliente` e a `resumo-mensal-do-caso` leem para saber o que dizer em cada fase, e quando.

```markdown
---
documento: Jornada · [TIPO DE CASO]
versao: 1
revisado_em: AAAA-MM-DD
dono: [ADVOGADO RESPONSÁVEL]
area: [ÁREA]
base: references/jornada-base-[AREA].md (sugestão do plugin, confirmada linha a linha)
---

# Jornada · [TIPO DE CASO]

> O que o cliente vive em cada fase deste tipo de caso e o que o escritório diz antes de ele perguntar. Vale para todos os clientes deste tipo de caso. O que é de um cliente só fica na abertura dele.

## A régua deste tipo de caso
- Máximo sem notícia: [N] dias corridos (ficha: [N]; mais curto aqui porque [MOTIVO], ou "igual à ficha")
- Aviso de movimentação relevante: [PRAZO] (ficha: avisa_movimentacao_relevante)
- Resumo mensal: [SIM, DIA N | NÃO] (ficha: resumo_mensal)
- Lembrete de compromisso: [QUANDO] (ficha: lembrete_de_compromisso)
- Nunca por mensagem, neste tipo de caso: [LISTA] (além de nunca_por_mensagem da ficha)

## As fases

### [FASE DA CARTEIRA] · [NOME EM PALAVRAS SIMPLES]
- O que o cliente sente: [UMA FRASE, COM AS PALAVRAS DELE]
- O que o escritório diz sem ser perguntado: [O QUÊ]
- Quando: [NO DIA DO PROTOCOLO | A CADA N DIAS | NO RESUMO]
- Máximo sem notícia nesta fase: [N] dias corridos | o da régua
- Canal: [MENSAGEM | LIGAÇÃO | REUNIÃO | RESUMO | PÁGINA]
- Quem fala: [FUNÇÃO]
- Nunca por mensagem: [O QUÊ]
- Vira resumo ou página: [O QUE ENTRA NO RESUMO DO MÊS OU NA PÁGINA DO CASO, INCLUSIVE O TRABALHO DO ESCRITÓRIO DA FASE QUE A EQUIPE REGISTRA NO HISTÓRICO, EX.: "cálculo conferido", "pedido de cópia ao INSS"]
- Modelo da biblioteca: [CHAVE, EX.: atualizacao-de-andamento | A DEFINIR]
- Situação: [confirmado | [A CONFIRMAR]]

(repetir para cada fase)

## Momentos de aflição deste tipo de caso
| Momento | Sinal na mensagem | O que o escritório faz | Quem |
|---|---|---|---|

## Perguntas que chegam antes de serem respondidas
(as cinco mais comuns, do jeito que chegam; a `cliente-com-ia`, se instalada, responde cada uma em `perguntas-do-caso-<tipo-de-caso>.md`)

## Tempos de fase (uso interno)
| Fase | Tempo típico |
|---|---|
| [FASE] | [CONFERIR] |

Nunca vai para mensagem ao cliente como promessa. Serve para o escritório planejar e para a rotina estranhar um caso parado demais.

## Histórico
- 1 · AAAA-MM-DD · jornada criada por [QUEM], a partir da base [ÁREA]
```

Regras:
- Fase com linha ainda `[A CONFIRMAR]` não vale para o agente. Ele segue a ficha nessa fase.
- O `carteira.py` da `rotina-da-experiencia` lê esta jornada pelo `tipo_de_caso` da carteira (o nome do arquivo ou o título do cabeçalho): na fase do cliente, vale o "Máximo sem notícia nesta fase" com número; com "o da régua", vale o "Máximo sem notícia" da régua deste tipo de caso; com `[N]` ou `Situação: [A CONFIRMAR]`, vale o `maximo_sem_noticia` da ficha. Escreva o número antes de qualquer parêntese.
- Tempo de fase nunca sai do `[CONFERIR]` para o texto do cliente.
- Nada de nome de cliente, número de processo ou dado de saúde nesta jornada: ela é da base e pode ir para o Projeto no Claude.
