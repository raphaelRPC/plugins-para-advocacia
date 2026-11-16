# Modelo da ficha da automação

Copiar para `escritorio/05-automacoes/ciclo-da-controladoria/ficha.md` no modo configurar, preenchido com as respostas da pessoa e os campos das fichas. Os colchetes são para preencher na configuração; o que ninguém souber fica `[A PREENCHER]`.

```markdown
---
documento: Ficha da automação · ciclo da controladoria
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELO CICLO, CAMPO responsavel_controladoria]
---

# Ciclo da controladoria

## O que faz
Duas vezes por dia útil, lê o que chegou desde a última rodada: a busca no DJEN pelas OABs da ficha, a pasta de entrada (e-mails do tribunal, planilhas, exportações), o registro dos painéis feito pela pessoa e os registros. Tira as duplicadas, tria e liga cada publicação ao caso com o trecho literal, calcula o prazo sugerido pelo calendário do tribunal, separa o que vence hoje ou no próximo dia útil, passa cada item pelo revisor, monta a fila de conferência e o resumo do dia.

## O que não faz
- Não confirma prazo: nada vira `conferido`, `cumprido`, `perdido` ou `cancelado` sem uma pessoa.
- Não escreve nome em `conferido_por`.
- Não agenda prazo `sugerido`.
- Não decide prazo em dobro, ciência tácita, prazo material nem a providência do ato.
- Não completa número de dias de memória.
- Não entra em painel de tribunal e não usa senha, certificado digital ou token.
- Não apaga arquivo nem linha.

## Como roda
- Jeito: [duas tarefas agendadas | comando /motor-controladoria:ciclo duas vezes por dia | ciclo à mão no chat]
- Onde: [Cowork | Claude Code | chat com Projeto] (campo `onde_roda` da ficha do escritório)
- Horários: [EX.: dias úteis, 08h e 14h] (campo `horario_da_captacao`); resumo pronto até [HORA] (campo `horario_da_rotina_diaria`)
- Se até [HORA] não houver resumo do dia: [FUNÇÃO] roda o ciclo à mão (plano em "Quando não roda").

## Quem lê e decide
- Capta, tria e faz a primeira conferência: [FUNÇÃO] (campo `responsavel_controladoria`)
- Faz a segunda conferência: [FUNÇÃO] (campo `quem_confere`)
- Decide a providência: [FUNÇÃO] (campo `quem_decide_providencia`)
- Abre os painéis dos sistemas: [FUNÇÃO E HORÁRIO] (campo `paineis_dos_sistemas`)

## Fontes
| Fonte | Caminho ou conector | Obrigatória |
|---|---|---|
| Registro de publicações | `07-operacao/controladoria/publicacoes.csv` | sim |
| Registro de prazos | `07-operacao/controladoria/prazos.csv` | sim |
| Pasta de entrada | `07-operacao/controladoria/entrada/` | sim |
| Calendários dos tribunais | `04-base/controladoria/calendario/` | sim |
| Tabela de regras validada | `04-base/controladoria/regras-de-contagem.md` | sim |
| DJEN (consulta pública do CNJ) | pela `captar-publicacoes`, com internet | não (sem internet, a planilha) |
| Registro dos painéis | `07-operacao/controladoria/paineis/AAAA-MM-DD.md` | não |
| Carteira de processos | `07-operacao/controladoria/processos.csv` | não |
| E-mail ou agenda | [CONECTOR OU "sem conector"] (só leitura; conferir na configuração da conta) | não |

## Critérios
| Critério | Valor | De onde |
|---|---|---|
| PESSOA AGORA por data | segurança ou fatal vencida, hoje ou no próximo dia útil do tribunal | regra da habilidade |
| Janela da semana | [EX.: 5] dias úteis | combinado no configurar |
| Janela das audiências e perícias | [EX.: 15] dias corridos | combinado no configurar |
| Sugerido parado | mais de um dia útil | regra da habilidade |
| Dias de segurança | [N] dias úteis | K: `dias_de_seguranca` |
| Feriados a mais | [DATAS OU "só o calendário"] | E: `feriados_e_recessos` |

## O comando do script
`python3 "[PASTA DA HABILIDADE rotina-da-controladoria]/scripts/pendencias_controladoria.py" "escritorio/07-operacao/controladoria/prazos.csv" --publicacoes "escritorio/07-operacao/controladoria/publicacoes.csv" --data AAAA-MM-DD --semana [N] --audiencias [N]`

## Onde grava
- Resumo do dia: `07-operacao/controladoria/rotina/AAAA-MM-DD.md`
- Fila de conferência: `07-operacao/controladoria/fila/AAAA-MM-DD/`
- Uma linha por rodada: `05-automacoes/ciclo-da-controladoria/registro-de-uso.md`

## Quando não roda
[COLE AQUI O PLANO COMBINADO, A PARTIR DA SEÇÃO 3 DE references/quando-a-rotina-nao-roda.md DA HABILIDADE]

## Revisão
- A cada mês, junto com a `auditoria-de-prazos` (se instalada), ou quando a ficha mudar quem confere ou os tribunais.
- Dois dias úteis seguidos sem ciclo: o `/motor-controladoria:status` avisa e o dono revisa o jeito de rodar.

## Histórico
- 1 · AAAA-MM-DD · ciclo configurado, [JEITO], às [HORAS]
```
