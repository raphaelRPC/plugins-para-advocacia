# Modelo da ficha da automação

Copiar para `escritorio/05-automacoes/ciclo-juridico/ficha.md` no modo configurar, preenchido com as respostas do advogado e os campos das fichas. Os colchetes são para preencher na configuração; o que ninguém souber fica `[A PREENCHER]`.

```markdown
---
documento: Ficha da automação · ciclo jurídico
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELO CICLO]
---

# Ciclo jurídico

## O que faz
Todo dia útil, lê o que chegou desde a última rodada (a pasta de entrada, as passagens do comercial, o registro de peças e, se houver, os conectores, só leitura). Separa o que é do advogado agora, monta o dossiê dos casos que chegaram, minuta só as peças com tese definida pelo advogado, confere citações e dados, prepara o checklist de protocolo das aprovadas, passa cada item pelo revisor e deixa a fila do advogado e o resumo do dia.

## O que não faz
- Não escolhe a tese nem o caminho do caso.
- Não move peça para `tese-definida`, `revisada`, `aprovada`, `protocolada` ou `suspensa`.
- Não completa número de julgado, relator, data ou enunciado de memória.
- Não assina, não protocola e não mexe em certificado digital, senha ou sistema de tribunal.
- Não calcula prazo processual (é da controladoria).
- Não apaga arquivo.

## Como roda
- Jeito: [agente pela tarefa agendada | agente pelo comando /motor-juridico:ciclo | ciclo à mão no chat]
- Onde: [Cowork | Claude Code | chat com Projeto] (campo `onde_roda` da ficha do escritório)
- Dias e hora: [EX.: dias úteis, às 8h] (campo `horario_da_rotina_diaria`)
- Se até [HORA] não houver resumo do dia: [FUNÇÃO] roda o ciclo à mão (plano em "Quando não roda").

## Quem lê e decide
- Redige as minutas: [FUNÇÃO] (campo `quem_redige`)
- Revisa, define a tese e aprova: [FUNÇÃO] (campo `quem_revisa`)
- Lê a fila: [FUNÇÃO E HORÁRIO] (campo `quem_aprova_rascunhos`)
- Protocola: [FUNÇÃO] (campo `quem_protocola`)

## Fontes
| Fonte | Caminho ou conector | Obrigatória |
|---|---|---|
| Registro de peças | `07-operacao/juridico/pecas.csv` | sim |
| Pasta de entrada (pedidos de peça) | `07-operacao/juridico/entrada/` | sim |
| Pastas dos casos | `07-operacao/juridico/casos/` | sim |
| Passagens do comercial | `07-operacao/comercial/passagens/` (se o motor-comercial estiver instalado) | não |
| Base do escritório | `04-base/juridico/` e `04-base/habilidades-do-escritorio/` | não |
| E-mail ou pasta de arquivos | [CONECTOR OU "sem conector"] (conferir na configuração da conta) | não |

## Critérios
| Critério | Valor | De onde |
|---|---|---|
| Limite por etapa (dias úteis) | [EX.: pedida 2, em-analise 5, tese-definida 2, minuta 2, conferida 2, revisada 1, aprovada 1] | combinado no configurar |
| ADVOGADO AGORA por prazo | prazo interno até o próximo dia útil | regra da habilidade |
| Feriados do ano | [DATAS OU "conferir a cada mês"] | E: `feriados_e_recessos` |
| Validade da conferência da base | [EX.: 90 dias] | J: `validade_da_conferencia` |

## O comando do script
`python3 "[PASTA DA HABILIDADE rotina-juridica]/scripts/pendencias_juridicas.py" "escritorio/07-operacao/juridico/pecas.csv" --feriados "[FERIADOS]" --parada "[LIMITES]" --registro-de-uso "escritorio/05-automacoes/ciclo-juridico/registro-de-uso.md" --fila "escritorio/07-operacao/juridico/fila" --entrada "escritorio/07-operacao/juridico/entrada" --casos "escritorio/07-operacao/juridico/casos"`

## Onde grava
- Resumo do dia: `07-operacao/juridico/rotina/AAAA-MM-DD.md`
- Fila do advogado: `07-operacao/juridico/fila/AAAA-MM-DD/`
- Uma linha por rodada: `05-automacoes/ciclo-juridico/registro-de-uso.md`

## Quando não roda
[COLE AQUI O PLANO COMBINADO, A PARTIR DA SEÇÃO 3 DE references/quando-a-rotina-nao-roda.md DA HABILIDADE]

## Revisão
- A cada mês, ou quando a ficha jurídica mudar quem redige, revisa ou protocola.
- Dois dias úteis seguidos sem ciclo: o `/motor-juridico:status` avisa e o dono revisa o jeito de rodar.

## Histórico
- 1 · AAAA-MM-DD · ciclo configurado, [JEITO], às [HORA]
```
