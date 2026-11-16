# Modelo do resumo do dia

O arquivo que o ciclo (agente ou à mão) grava em `escritorio/07-operacao/juridico/rotina/AAAA-MM-DD.md`. As seções marcadas "script" saem do `scripts/pendencias_juridicas.py` (ou das mesmas regras aplicadas à mão, seção 4 do SKILL.md). As outras vêm do ciclo: a análise, a minuta, a conferência e o revisor. O agente começa o resumo; o comando `ciclo` acrescenta a linha da revisão.

```markdown
---
documento: Ciclo jurídico · AAAA-MM-DD
gerado_em: AAAA-MM-DD HH:MM
como_rodou: agente (tarefa agendada) | agente (comando) | à mão | só o resumo
desde: AAAA-MM-DD HH:MM
dono: [FUNÇÃO QUE LÊ]
---

# Ciclo jurídico · AAAA-MM-DD ([DIA DA SEMANA])

## Comece por aqui
1. [AÇÃO] · [ID E NOME CURTO] · [QUEM FAZ] · [POR QUÊ, EM ATÉ 8 PALAVRAS]
(no máximo cinco; ADVOGADO AGORA primeiro, depois prazo interno, depois o mais parado)

## ADVOGADO AGORA
(script, mais o que o ciclo separou hoje: pedido que envolve escolha de tese, conflito de interesses possível em caso novo, dado sensível que não devia estar no material, itens bloqueados pelo revisor. Uma frase do porquê para cada um.)

## PARA DECIDIR
(o que o advogado decide sem urgência: sinais do banco de teses, conferência de lote esperando a tese, coincidência fraca no conflito de interesses, checagem de conflito por fazer, item vencido de plano de compliance. Uma linha cada.)

## Prazos internos de hoje e amanhã
(script, seção 1, só os de hoje até o próximo dia útil; os outros da janela vêm abaixo, em uma linha cada)

## Minutas na fila
- [N] itens em `07-operacao/juridico/fila/AAAA-MM-DD/`: [ID · PEÇA · PRAZO INTERNO]
- Revisão: [N] ok, [N] ajustados, [N] para conferir, [N] bloqueados

## Pesquisar no Jus IA
(uma linha por citação que ficou marcada ou cinza: tema, o que falta achar, a peça; "nada a pesquisar hoje" se vazio)

## Protocolos preparados
(script, seção 6, e o checklist feito hoje pela preparar-protocolo: [ID · SISTEMA · QUEM PROTOCOLA · O QUE FALTA])

## Peças paradas e esperando tese
(script, seções 3 e 7)

## Citações e dados
(script, seções 4 e 5)

## Registro a corrigir
(script, seção 8, cada correção com a linha proposta)

## O que não deu para fazer e por quê
(uma linha por falha, que a equipe entenda: "não achei o pecas.csv"; "pedido sem código do caso: 2026-04-15-1010-controladoria.md"; "falta quem_revisa na ficha")

## Desde a última rodada
(script: linhas atualizadas, arquivos na entrada, a fila; e o lembrete de apagar `entrada/lidos/` com mais de 7 dias, que quem apaga é a pessoa)
```

Regras de escrita do resumo:
- Uma pessoa precisa ler em três minutos. Seção vazia vira uma linha ("Nenhuma peça parada.").
- Só id, código, primeiro nome ou iniciais, área, peça e etapa. Nada de CPF, número de processo, valor da causa ou detalhe de saúde.
- Nenhuma minuta dentro do resumo. A minuta fica em `casos/<codigo>/minutas/` e o item na fila.
- Treino nunca entra: o resumo de treino grava em `07-operacao/_treino/juridico/rotina/`.
