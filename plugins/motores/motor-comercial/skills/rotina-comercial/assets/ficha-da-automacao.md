# Modelo da ficha da automação

Copiar para `escritorio/05-automacoes/ciclo-comercial/ficha.md` no modo configurar, preenchido com as respostas do advogado e os campos das fichas. Os colchetes são para preencher na configuração; o que ninguém souber fica `[A PREENCHER]`.

```markdown
---
documento: Ficha da automação · ciclo comercial
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELO CICLO]
---

# Ciclo comercial

## O que faz
Todo dia útil, lê o que chegou desde a última rodada (a pasta de entrada, o registro de contatos e, se houver, o e-mail e a agenda pelos conectores, só leitura). Separa o que é para uma pessoa agora, faz a triagem, arma a régua de retorno, prepara convites, confirmações, lembretes e retornos, passa cada rascunho pelo revisor e deixa a fila de aprovação e o resumo do dia.

## O que não faz
- Não envia mensagem, e-mail ou documento a ninguém. Quem envia é uma pessoa, pelo canal oficial.
- Não escreve para quem está em PESSOA AGORA, pediu para parar ou está fora da área sem encaminhamento na ficha.
- Não move contato para `fechado`, `perdido`, `recusado`, `encaminhado`, `sem-caso` nem `nao-compareceu`.
- Não decide valor, estratégia ou se vale entrar com a ação.
- Não apaga arquivo.

## Como roda
- Jeito: [agente pela tarefa agendada | agente pelo comando /motor-comercial:ciclo | ciclo à mão no chat]
- Onde: [Cowork | Claude Code | chat com Projeto] (campo `onde_roda` da ficha do escritório)
- Dias e hora: [EX.: dias úteis, às 8h30] (campo `horario_da_rotina_diaria`)
- Se até [HORA] não houver resumo do dia: [FUNÇÃO] roda o ciclo à mão (plano em "Quando não roda").

## Quem lê e aprova
- Lê o resumo inteiro: [FUNÇÃO]
- Aprova a fila: [FUNÇÃO E HORÁRIO] (campo `quem_aprova_rascunhos`)
- PESSOA AGORA vai para: [FUNÇÃO E CAMINHO] (campo `urgencia_vai_para`)

## Fontes
| Fonte | Caminho ou conector | Obrigatória |
|---|---|---|
| Registro de contatos | `07-operacao/comercial/contatos.csv` | sim |
| Pasta de entrada (conversas exportadas, e-mails salvos, texto colado) | `07-operacao/comercial/entrada/` | sim |
| Triagens | `07-operacao/comercial/triagens/` | não |
| Fila | `07-operacao/comercial/fila/` | não |
| E-mail | [CONECTOR OU "sem conector"] (conferir na configuração da conta) | não |
| Agenda | [CONECTOR OU "sem conector"] (conferir na configuração da conta) | não |

## Critérios (vindos das fichas)
| Critério | Valor | Campo |
|---|---|---|
| Expediente | [O TEXTO DO CAMPO, EX.: "dias úteis, das 9h às 18h"] | E: `horario_de_atendimento` |
| Primeira resposta ao contato novo | [O TEXTO DO CAMPO EM HORAS ÚTEIS, EX.: "até 2 horas úteis"] | C: `primeira_resposta_contato_novo` |
| Régua de quem não agendou | [EX.: 2, 7 e 15 dias corridos] | C: `follow_up` |
| Proposta parada | [N] dias corridos sem atualização (primeiro intervalo da régua de proposta) | C: `follow_up` |
| Feriados do ano | [DATAS AAAA-MM-DD OU DD/MM OU "conferir a cada mês"] | E: `feriados_e_recessos` |
| Palavras de alerta de prioridade máxima | [AS DA FICHA, SEPARADAS POR PONTO E VÍRGULA] | E: `palavras_de_alerta` |

## O comando do script
`python3 "[PASTA DA HABILIDADE rotina-comercial]/scripts/pendencias.py" "escritorio/07-operacao/comercial/contatos.csv" --expediente "[HORARIO_DE_ATENDIMENTO]" --prazo-novo "[PRIMEIRA_RESPOSTA_CONTATO_NOVO]" --dias-proposta [N] --feriados "[FERIADOS]" --alertas "[PALAVRAS DE ALERTA]" --registro-de-uso "escritorio/05-automacoes/ciclo-comercial/registro-de-uso.md" --triagens "escritorio/07-operacao/comercial/triagens" --fila "escritorio/07-operacao/comercial/fila"`

Formato de cada valor: seção 4.1 do SKILL.md da `rotina-comercial`. O texto do campo vai entre aspas, como está na ficha.

## Onde grava
- Resumo do dia: `07-operacao/comercial/rotina/AAAA-MM-DD.md`
- Fila: `07-operacao/comercial/fila/AAAA-MM-DD/`
- Uma linha por rodada: `05-automacoes/ciclo-comercial/registro-de-uso.md`

## Quando não roda
[COLE AQUI O PLANO COMBINADO, A PARTIR DA SEÇÃO 3 DE references/quando-a-rotina-nao-roda.md DA HABILIDADE]

## Revisão
- A cada mês, ou quando uma ficha mudar um dos critérios.
- Dois dias seguidos sem ciclo: o `/motor-comercial:status` avisa e o dono revisa o jeito de rodar.

## Histórico
- 1 · AAAA-MM-DD · ciclo configurado, [JEITO], às [HORA]
```
