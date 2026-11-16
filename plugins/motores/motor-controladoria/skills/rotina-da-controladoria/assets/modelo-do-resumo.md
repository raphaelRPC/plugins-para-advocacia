# Modelo do resumo do dia da controladoria

O arquivo que o ciclo (o `agente-de-controladoria` ou o ciclo à mão) grava em `escritorio/07-operacao/controladoria/rotina/AAAA-MM-DD.md`. O ciclo roda duas vezes por dia: a segunda rodada acrescenta uma seção com a hora ("## Rodada das 14h"), com as mesmas seções, e não apaga a primeira.

As seções marcadas "script" saem do `scripts/pendencias_controladoria.py` desta habilidade (ou das mesmas regras aplicadas à mão, seção 4 do SKILL.md). As outras vêm do ciclo: a captação, a triagem, a conta e o revisor. O agente começa o resumo; o comando `/motor-controladoria:ciclo` acrescenta a linha da revisão e move os bloqueados para PESSOA AGORA ou PARA DECIDIR, com o motivo do revisor.

```markdown
---
documento: Ciclo da controladoria · AAAA-MM-DD
gerado_em: AAAA-MM-DD HH:MM
como_rodou: agente (tarefa agendada) | agente (comando) | à mão | só o resumo
desde: AAAA-MM-DD HH:MM
dono: [FUNÇÃO DE QUEM LÊ, CAMPO responsavel_controladoria]
---

# Ciclo da controladoria · AAAA-MM-DD ([DIA DA SEMANA])

## Comece por aqui
1. [AÇÃO] · [ID · NOME CURTO · CÓDIGO] · [QUEM FAZ] · [POR QUÊ, EM ATÉ 10 PALAVRAS]
(no máximo cinco; PESSOA AGORA primeiro, depois a dupla conferência do que vence primeiro, depois o conferido sem agenda)

## PESSOA AGORA
(script, mais o que o ciclo separou hoje: ato com ordem para cumprir em horas, item bloqueado pelo revisor que não espera. Uma frase do porquê em cada linha. Prazo `sugerido` aparece como "data sugerida, sem dupla conferência", nunca como prazo que vale.)

## PARA DECIDIR
(script e ciclo: providência esperando decisão, divergência da dupla conferência com a data mais cedo valendo, prazo em dobro ou ciência tácita para a pessoa decidir, duplicada a confirmar, bloqueado sem urgência, item da fila parado há mais de um dia útil. Uma linha cada.)

## Vence na semana
(script: tabela curta com caso, tribunal, providência, segurança, fatal, responsável e status; o status `sugerido` sai escrito "sugerido, sem dupla conferência (ainda não vale)")

## Esperando a dupla conferência
(script: todos os `sugerido`, o mais antigo primeiro, com a data sugerida, a regra e o número de dias; os parados há mais de um dia útil marcados. Embaixo: "Revisão: N ok, N ajustados, N para conferir, N bloqueados", que o comando ciclo acrescenta)

## Publicações sem caso
(script: cada uma com tribunal, órgão e a pergunta para a pessoa: caso antigo, substabelecimento ou erro? Nenhum prazo calculado antes da resposta)

## Audiências e perícias
(script: as dos próximos 15 dias, com data, hora, local ou link e responsável; as novas desde a última rodada, mesmo fora da janela; o aviso ao cliente que foi para a entrada do motor-experiencia, se instalado)

## Agenda
(script: conferido sem agenda e sem responsável; e do ciclo: os .ics gerados hoje em `agenda/`, um por linha)

## O que não deu para fazer e por quê
(script: publicações não triadas, publicação triada como prazo sem linha em prazos.csv, registro a corrigir, avisos de calendário. E do ciclo, uma linha por falha que a equipe entenda: "DJEN não consultado: sem internet"; "planilha da entrada sem a coluna processo"; "sem calendário de 2026 para o TJMG"; "tabela de regras ainda não validada pelo escritório")

## Desde a última rodada
(script: publicações novas por fonte, prazos atualizados por status, a fila; o aviso de dois dias úteis sem ciclo; o lembrete de apagar `entrada/lidos/` com mais de 7 dias, que quem apaga é a pessoa)
```

## Regras de escrita do resumo

- Uma pessoa lê em três minutos. Seção vazia vira uma linha que diz quantas linhas foram lidas ("Nenhum prazo `sugerido` (6 em aberto lidos)."). Nunca "nada a apontar" sem ter lido.
- Prazo de hoje ou do próximo dia útil vai para PESSOA AGORA antes de qualquer outra coisa, em qualquer status.
- Prazo `sugerido` nunca aparece como se valesse: a data sai como "data sugerida" e o status como "sugerido, sem dupla conferência".
- Só id, código, primeiro nome ou iniciais, tribunal, providência, datas, status e responsável. O número do processo fica no registro, não no resumo. Nada de CPF, valor, dado de saúde ou de criança no resumo da publicação.
- Nenhuma conta passo a passo dentro do resumo: a conta fica no item da fila (`fila/AAAA-MM-DD/NN-<codigo>-prazo.md`).
- Treino nunca entra: o resumo de treino grava em `07-operacao/_treino/controladoria/rotina/`, com "TREINO" no título.

## Exemplo (treino, Escritório Modelo, 2026-04-14)

Saída do script com os registros de treino (`assets/prazos-de-treino.csv` e `assets/publicacoes-de-treino.csv`), depois do ciclo da manhã:

```markdown
## Comece por aqui
1. Conferir agora o recurso ordinário · PZ-2026-0003 · Camila · C-2026-0010 · estagiária e advogada · captada com atraso, 2 dias úteis já corridos
2. Conferir agora a manifestação · PZ-2026-0006 · Paulo · C-2026-0002 · advogada · ciência tácita do portal em 2026-04-16
3. Decidir de quem é a publicação PUB-2026-00007 · sem caso · TJMG · advogada
4. Pedir ao cliente o relatório médico · PZ-2026-0005 · Marta · C-2026-0001 · quem fala com o cliente · prazo do escritório que depende dela
5. Dupla conferência de PZ-2026-0004 · Renata · C-2026-0005 · segurança sugerida 2026-04-22

## PESSOA AGORA
- PZ-2026-0003 · Camila · C-2026-0010 · TRT3 · recurso ordinário · segurança 2026-04-22 · fatal 2026-04-24 · sugerido, sem dupla conferência (ainda não vale): captada com atraso, o prazo começou em 2026-04-13 e a publicação só entrou em 2026-04-14
- PZ-2026-0006 · Paulo · C-2026-0002 · TRT3 · manifestação sobre documentos · sugerido, sem dupla conferência: ciência tácita da intimação do portal em 2026-04-16; se alguém abrir antes, a conta muda
- PUB-2026-00007 · sem caso · TJMG · 5ª Vara Cível · Rosângela: processo da OAB do escritório que não está na carteira; caso antigo, substabelecimento ou erro?
```

O recurso inominado do Otávio (fatal sugerida 2026-04-30) não está em PESSOA AGORA: fica em "Esperando a dupla conferência".
