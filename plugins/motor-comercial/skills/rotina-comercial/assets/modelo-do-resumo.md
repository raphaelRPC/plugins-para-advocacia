# Modelo do resumo do dia

O arquivo que o ciclo (agente ou à mão) grava em `escritorio/07-operacao/comercial/rotina/AAAA-MM-DD.md`. As seções marcadas "script" saem do `scripts/pendencias.py` (ou das mesmas regras aplicadas à mão, seção 4 do SKILL.md). As outras vêm do ciclo: a triagem, a fila e o revisor.

```markdown
---
documento: Ciclo comercial · AAAA-MM-DD
gerado_em: AAAA-MM-DD HH:MM
como_rodou: agente (tarefa agendada) | agente (comando) | à mão | só o resumo
desde: AAAA-MM-DD HH:MM
dono: [FUNÇÃO QUE LÊ]
---

# Ciclo comercial · AAAA-MM-DD ([DIA DA SEMANA])

## Comece por aqui
1. [AÇÃO] · [CÓDIGO E NOME CURTO] · [QUEM FAZ] · [POR QUÊ, EM 6 PALAVRAS]
(no máximo cinco; PESSOA AGORA primeiro, depois urgência alta, depois o mais atrasado)

## PESSOA AGORA
(script, mais o que a triagem de hoje separou: risco, prisão, prazo de hoje ou amanhã, vulnerabilidade forte, urgência alta sem responsável, rascunho parado na fila há mais de um dia útil. Uma frase de porquê para cada um. Nenhuma mensagem pronta aqui.)

## Sem resposta além do prazo
(script)

## Consultas de hoje
(script; com conector de agenda, também consulta na agenda que não está no registro, e o contrário. Lembretes da véspera viram rascunhos na fila.)

## Fila para aprovar
- [N] rascunhos em `07-operacao/comercial/fila/AAAA-MM-DD/`: [CÓDIGO · CHAVE · ATÉ QUANDO]
- Revisor: [N] ok, [N] ajustados, [N] bloqueados (os bloqueados estão em PESSOA AGORA ou em Para decidir)

## Para decidir
(mudanças de etapa que só uma pessoa faz: `negociando` a confirmar, `encaminhado`, `recusado`, `perdido`, `nao-compareceu`, consulta que passou; correções do registro, cada uma com a linha proposta)

## Para a experiência do cliente
(mensagens de cliente ativo que chegaram ao comercial; foram para a `triar-mensagem-do-cliente`, do motor-experiencia, ou para quem cuida do caso)

## Retornos, propostas e quem pediu para parar
(script, seções 3 a 5)

## Registro a corrigir
(script, seção 6)

## O que não deu para fazer e por quê
(uma linha por falha, que a equipe entenda: "não achei o contatos.csv"; "conector de e-mail desconectado"; "falta encaminhamos_para na ficha")

## Desde a última rodada
(script: entradas, triagens de todos os dias do período, inclusive fim de semana, e a fila)

## Semana anterior
(script, só às segundas)
```

Regras de escrita do resumo:
- Uma pessoa precisa ler em três minutos. Seção vazia vira uma linha ("Nenhuma consulta hoje.").
- Só código, primeiro nome ou iniciais, área e assunto curto. Nada de telefone, documento, número de processo ou detalhe de saúde.
- Nenhuma mensagem pronta para o contato dentro do resumo. Mensagem fica na fila, com revisor e status.
- Contato com `pediu_para_parar = sim` nunca aparece como retorno a fazer.
- Treino nunca entra: o resumo de treino, se alguém pedir, grava em `07-operacao/_treino/comercial/rotina/`.
