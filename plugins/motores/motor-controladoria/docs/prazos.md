# As publicações, os prazos e a dupla conferência

Toda publicação passa pelo mesmo caminho: é captada, triada, ligada ao caso e, se pede alguma coisa, vira um prazo, uma audiência ou uma tarefa. O prazo só entra na agenda depois da dupla conferência. Os registros são planilhas simples que as habilidades leem e atualizam, em `escritorio/07-operacao/controladoria/`.

## O caminho de uma publicação

| Passo | O que acontece | Quem faz |
|---|---|---|
| Captar | A publicação chega (DJEN, e-mail do tribunal, exportação do sistema, planilha, painel) e entra em `publicacoes.csv`, com o teor guardado | `captar-publicacoes` ou o agente |
| Triar | O ato é classificado e ligado ao código do caso, com o trecho literal que justifica | `triar-publicacoes` (sugestão) |
| Calcular | O que pede prazo ganha a conta, pela tabela de `contagem.md` e pelo calendário do tribunal | `calcular-prazo` (sugestão) |
| Conferir | Uma pessoa lê o ato, confirma o que ele pede, o número de dias e a regra; a conta é refeita por um segundo cálculo independente; as duas têm que bater | **uma pessoa**, com a `dupla-conferencia` |
| Agendar | A data de segurança e a fatal vão para a agenda do responsável, com os lembretes | `agenda-de-prazos`, depois de conferido |
| Encaminhar | A providência vira pedido de peça para o jurídico, tarefa de documento ou aviso ao cliente | `encaminhar-providencia`, com a decisão da pessoa |
| Cumprir | A peça protocolada ou a tarefa feita fecha o prazo, com a data | a pessoa, ou o registro de protocolo do motor-juridico (se instalado) |

## O arquivo `publicacoes.csv`

```
id,fonte,disponibilizada_em,publicada_em,tribunal,orgao,processo,codigo_caso,cliente_curto,tipo_ato,resumo,teor,triagem,triada_por,prazo_id,atualizado_em
```

| Coluna | O que vai | Exemplo |
|---|---|---|
| `id` | PUB, o ano e um número sequencial | PUB-2026-00001 |
| `fonte` | `djen`, `email`, `sistema`, `planilha`, `painel` | djen |
| `disponibilizada_em` | AAAA-MM-DD, como veio da fonte | 2026-04-13 |
| `publicada_em` | AAAA-MM-DD, calculada (`publicacao-diario`) ou vazia | 2026-04-14 |
| `tribunal` | Sigla | TRF6 |
| `orgao` | Vara, juizado, turma, câmara | 3º JEF de Belo Horizonte |
| `processo` | O número do processo | 0000000-00.2026.4.06.3800 |
| `codigo_caso` | O código do cliente, o mesmo dos outros plugins, ou vazio | C-2026-0001 |
| `cliente_curto` | Primeiro nome ou iniciais | Marta |
| `tipo_ato` | `despacho`, `decisao`, `sentenca`, `acordao`, `intimacao`, `pauta`, `edital`, `certidao`, `outro` | sentenca |
| `resumo` | Até 120 caracteres, sem dado sensível | Sentença de improcedência |
| `teor` | Caminho do teor guardado | publicacoes/2026-04-14/PUB-2026-00001.md |
| `triagem` | `nao-triada`, `sem-providencia`, `ciencia`, `prazo`, `audiencia`, `pericia`, `urgente`, `sem-caso`, `duplicada` | prazo |
| `triada_por` | `ia` ou o nome de quem confirmou | ia |
| `prazo_id` | O id em `prazos.csv`, quando gerou prazo | PZ-2026-0001 |
| `atualizado_em` | AAAA-MM-DD | 2026-04-14 |

Colunas a mais que os scripts aceitam, se existirem: `captada_em` (AAAA-MM-DD, quando entrou no registro; sem ela, vale a data da pasta do teor). O tribunal do prazo sai da publicação ligada.

Duplicada é a mesma publicação vinda de duas fontes (mesmo processo, mesma data, mesmo teor). Ela fica no registro, com `triagem = duplicada`, apontando no `resumo` para o id original.

## O arquivo `prazos.csv`

```
id,publicacao_id,codigo_caso,cliente_curto,processo,tipo,providencia,rito,dias,contagem,regra,em_dobro,publicada_em,inicio,vencimento,data_seguranca,responsavel,status,calculado_por,conferido_por,conferido_em,cumprido_em,peca_id,observacao,atualizado_em
```

| Coluna | O que vai | Exemplo |
|---|---|---|
| `id` | PZ, o ano e um número sequencial | PZ-2026-0001 |
| `publicacao_id` | De onde veio, ou vazio para prazo informado à mão | PUB-2026-00001 |
| `tipo` | `prazo`, `audiencia`, `pericia`, `sessao`, `tarefa` | prazo |
| `providencia` | O que fazer, em poucas palavras | recurso inominado |
| `rito` | `civel`, `trabalhista`, `juizado-civel`, `juizado-federal`, `penal`, `outro` | juizado-federal |
| `dias` | O número de dias antes de dobrar, de onde ele veio na observação | 10 |
| `contagem` | `uteis` ou `corridos` | uteis |
| `regra` | As chaves de `contagem.md` usadas, separadas por `+` | publicacao-diario+juizado-federal |
| `em_dobro` | `nao`, ou `sim` só com a confirmação da pessoa | nao |
| `publicada_em`, `inicio`, `vencimento`, `data_seguranca` | AAAA-MM-DD. Na intimação pelo portal e na ciência informada, `publicada_em` guarda a data da ciência | 2026-04-14, 2026-04-15, 2026-04-30, 2026-04-28 |
| `responsavel` | Primeiro nome ou função | advogada |
| `status` | `sugerido`, `conferido`, `agendado`, `cumprido`, `perdido`, `cancelado` | conferido |
| `calculado_por` | `ia` ou o nome | ia |
| `conferido_por` | Os dois nomes da dupla conferência, ou o nome e "2º turno" | Ana; Bruno |
| `conferido_em` | AAAA-MM-DD HH:MM da segunda conferência | 2026-04-14 15:10 |
| `cumprido_em` | AAAA-MM-DD, quando cumpriu | 2026-04-27 |
| `peca_id` | O id da peça no `pecas.csv` do motor-juridico (se instalado) | P-2026-0004 |
| `observacao` | De onde veio o número de dias, a dúvida, o que a pessoa decidiu | dias pelo ato; tabela do escritório ok |

Para audiência, perícia e sessão: `vencimento` é a data do ato, `observacao` leva hora e local ou link, e `dias`, `contagem` e `regra` ficam vazios.

## As etapas do prazo e quem move

| Status | Quer dizer | Quem move |
|---|---|---|
| `sugerido` | A IA leu e calculou | a habilidade ou o agente |
| `conferido` | A dupla conferência terminou e as duas contas batem | **só pessoas** (as duas conferências) |
| `agendado` | Está na agenda do responsável, com lembretes | a `agenda-de-prazos`, só depois de `conferido` e só quando a pessoa disser que importou o arquivo (ou o conector de agenda confirmar) |
| `cumprido` | Feito e protocolado, com data | a pessoa, ou o registro de protocolo do motor-juridico |
| `perdido` | Venceu sem cumprimento | **só a pessoa**, com a nota do que aconteceu |
| `cancelado` | O ato foi revogado, houve acordo, o prazo deixou de existir | **só a pessoa**, com o motivo |

## A dupla conferência

1. **Primeira conferência.** Uma pessoa lê o trecho literal do ato e confirma: o que o ato pede, o número de dias (do ato ou da tabela do escritório), o rito e a regra, e se há prazo em dobro.
2. **Segunda conferência.** Outra pessoa, ou a mesma em outro turno no escritório de uma pessoa só (o `quem_confere` da ficha), faz a mesma leitura sem ver a primeira resposta.
3. **A conta.** O script calcula o vencimento duas vezes, por dois caminhos (dia a dia e pelo calendário), com os dados confirmados. As duas leituras e as duas contas têm que dar a mesma data.
4. **Bateu:** `status = conferido`, os dois nomes em `conferido_por` (entre aspas na planilha, por causa do ponto e vírgula), a hora em `conferido_em`, e o registro em `conferencias/AAAA-MM-DD.md` (formato em `skills/dupla-conferencia/assets/modelo-do-registro.md`).
5. **Não bateu:** o prazo fica `sugerido`, com a divergência na fila, e vale a data mais cedo até a pessoa decidir. Nada entra na agenda, nem como provisório: o resumo mostra o prazo e ele sobe para PESSOA AGORA quando a data mais cedo está a 2 dias úteis ou menos.

A IA nunca escreve um nome em `conferido_por`. Ela só registra a conferência quando a própria pessoa diz, na conversa, o que conferiu. O plugin não tem como saber quem está digitando: quem confere usa a própria conta.

## Regras dos registros

1. **Uma linha por publicação e uma por prazo.** Mudou de status, a linha é atualizada.
2. **Dados mínimos.** Sem CPF, endereço ou detalhe de saúde. O número do processo fica nestes registros, que ficam fora do Projeto no Claude.
3. **Prazo que vence hoje ou amanhã** (pela data de segurança ou pela fatal) vai para o topo do resumo, em PESSOA AGORA, em qualquer status.
4. **Nada é apagado.** Publicação errada vira `sem-caso` ou `duplicada`; prazo que deixou de existir vira `cancelado`.
5. **O agente do ciclo** cria linhas e mexe só em `nao-triada`, na triagem sugerida, no status `sugerido` e no `agendado` de quem já está `conferido`, e nas colunas `atualizado_em` e `observacao`.
6. **Treino não entra.** Casos fictícios gravam em `escritorio/07-operacao/_treino/controladoria/`.
7. **Os scripts** leem também a planilha salva pelo Excel (ponto e vírgula, com ou sem BOM, cp1252).

## Com os outros plugins

- **motor-juridico (se instalado):** a providência "fazer peça" vira um pedido na entrada do jurídico (`07-operacao/juridico/entrada/`), com o prazo interno igual à data de segurança. Quando o jurídico registra o protocolo, o prazo vira `cumprido`.
- **motor-experiencia (se instalado):** audiência, perícia, documento a pedir e decisão importante viram um item na entrada da experiência, para o aviso ao cliente (preparar-o-cliente, checklist-de-documentos, status-para-o-cliente). Notícia ruim vai por ligação.
