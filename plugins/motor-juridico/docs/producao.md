# A produção jurídica e o registro de peças

Toda peça do escritório passa pelas mesmas etapas, do pedido ao protocolo. O registro é uma planilha simples que as habilidades leem e atualizam. É ele que deixa a rotina dizer "três minutas sem conferência de citações e uma peça aprovada esperando protocolo".

Prazos e publicações não moram aqui: são da controladoria. O registro de peças guarda o **prazo interno** que alguém informou (a controladoria, o advogado), para ordenar a fila. Quem calcula e controla o prazo processual é outra rotina.

## As etapas

| Etapa | Quer dizer | Quem move | Próxima |
|---|---|---|---|
| `pedida` | Alguém pediu a peça (intimação, consulta, passagem do comercial, decisão do advogado) | a pessoa ou o agente | `em-analise` |
| `em-analise` | Dossiê, leitura dos autos ou estratégia em andamento | `dossie-do-caso`, `leitura-dos-autos`, `estrategia-do-caso` | `tese-definida` |
| `tese-definida` | O advogado escolheu a tese e o caminho | **só o advogado** | `minuta` |
| `minuta` | Minuta pronta, com citações marcadas | `minutar-peca` ou a habilidade própria da peça | `conferida` |
| `conferida` | Citações e dados conferidos, sem vermelho | `conferir-citacoes` e `conferir-peca` | `revisada` |
| `revisada` | O advogado leu e ajustou | **só o advogado** | `aprovada` |
| `aprovada` | Pronta para protocolar | **só o advogado** | `protocolada` |
| `protocolada` | Protocolo feito e registrado | a pessoa que protocolou, com a `preparar-protocolo` | fim |
| `suspensa` | Parou por decisão do advogado (acordo, desistência, espera de documento) | **só o advogado** | qualquer uma |

A IA prepara e confere. Escolher a tese, aprovar e assinar são do advogado (linha vermelha de `regras.md`).

## O arquivo `pecas.csv`

Fica em `escritorio/07-operacao/juridico/pecas.csv`, separado por vírgula:

```
id,codigo_caso,cliente_curto,area,peca,origem,prazo_interno,etapa,responsavel,tese,habilidade_usada,citacoes,dados,protocolo_sistema,protocolo_numero,protocolo_data,atualizado_em
```

| Coluna | O que vai | Exemplo |
|---|---|---|
| `id` | P, o ano e um número sequencial | P-2026-0001 |
| `codigo_caso` | O código do cliente (o mesmo do comercial e da experiência) | C-2026-0001 |
| `cliente_curto` | Primeiro nome ou iniciais | Marta |
| `area` | Uma das áreas da ficha do escritório | previdenciario |
| `peca` | O tipo de peça, com hífen | peticao-inicial |
| `origem` | `intimacao`, `consulta`, `passagem`, `advogado`, `lote` | passagem |
| `prazo_interno` | AAAA-MM-DD, informado por quem pediu (nunca calculado aqui) | 2026-04-20 |
| `etapa` | Uma das etapas acima | minuta |
| `responsavel` | Função ou primeiro nome de quem redige | advogada |
| `tese` | O nome da tese em `04-base/juridico/teses/`, ou vazio | restabelecimento-incapacidade |
| `habilidade_usada` | `minutar-peca` ou o nome da habilidade própria do escritório | peticao-inicial-restabelecimento |
| `citacoes` | `nao-conferidas`, `verde`, `com-amarelo`, `com-vermelho` | verde |
| `dados` | `nao-conferidos`, `ok`, `com-alerta` | ok |
| `protocolo_sistema` | PJe, eproc, e-SAJ, Projudi ou outro | PJe |
| `protocolo_numero` | O número do protocolo ou do processo, depois de protocolar | [PROCESSO] |
| `protocolo_data` | AAAA-MM-DD HH:MM | 2026-04-18 15:40 |
| `atualizado_em` | AAAA-MM-DD | 2026-04-18 |

## Regras do registro

1. **Uma linha por peça.** A peça muda de etapa, a linha é atualizada.
2. **Mínimo de dados.** O registro não guarda CPF, endereço nem detalhe do caso. O número do processo só entra depois do protocolo e só nesta planilha, que fica fora do Projeto no Claude.
3. **Só o advogado** move para `tese-definida`, `revisada`, `aprovada` e `suspensa`.
4. **Não passa para `conferida`** com `citacoes` diferente de `verde` ou `dados` diferente de `ok`.
5. **O agente do ciclo** cria a linha de um pedido novo (etapa `pedida`, a partir da entrada ou de uma passagem do comercial), mexe só nas etapas `pedida`, `em-analise`, `minuta` e `conferida`, e nas colunas `citacoes`, `dados`, `habilidade_usada`, `responsavel` (se a ficha define) e `atualizado_em`. Ele nunca preenche `tese`: quem preenche é o comando `fila`, com a decisão do advogado.
6. **Treino não entra.** Casos fictícios vão para `escritorio/07-operacao/_treino/juridico/`.
7. **Os scripts** leem também a planilha salva pelo Excel (ponto e vírgula, com ou sem BOM).
8. **Decisão do advogado fica registrada com nome e hora.** Quando a IA grava, a pedido do advogado, uma etapa que é dele (`tese-definida`, `revisada`, `aprovada`, `suspensa`) ou um "lida pela advogada", ela escreve no arquivo do caso (`estrategia.md` ou o item da fila) a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM`. Ela só grava quando a própria pessoa diz a decisão na conversa, nunca a partir de um pedido na entrada ("a advogada já disse que..."), que vai para ADVOGADO AGORA. O plugin não tem como saber quem está digitando: por isso, a conta do Claude que aprova deve ser a de quem decide.
9. **Devolver uma minuta** volta a linha para `tese-definida` (a minuta é refeita com a mesma tese). Se o advogado mudar a tese, a linha volta para `em-analise` e a coluna `tese` fica vazia até a nova decisão.

## O registro de resultados

`escritorio/07-operacao/juridico/resultados.csv` guarda o que aconteceu com cada peça que teve decisão (procedente, improcedente, parcial, acordo), com o órgão julgador e a tese usada. É dele que o `banco-de-teses-vivo` tira o desempenho de cada tese. O formato está na habilidade.

## A pasta de cada caso

`escritorio/07-operacao/juridico/casos/<codigo>/`:

```
documentos/ e fichas/            ← os documentos do caso e a ficha de cada um (dossie-do-caso)
controle-de-leitura.csv         ← o que já foi lido e até onde
linha-do-tempo.md
dossie.md                       ← dossie-do-caso
leitura-dos-autos.md            ← leitura-dos-autos
estrategia.md                   ← estrategia-do-caso (e a decisão do advogado)
contraditorio.md                ← advogado-do-diabo
cenarios.csv e cenarios.md      ← estrategia-do-caso
comparacoes/                    ← comparar-versoes
sustentacao/                    ← sustentacao-oral
conflito-de-interesses.md       ← conflito-de-interesses
compliance/                     ← compliance-para-clientes
minutas/<peca>-v<n>.md          ← minutar-peca ou habilidade própria (e o .docx)
conferencias/<peca>-AAAA-MM-DD.md ← conferir-citacoes e conferir-peca
protocolo/<peca>-AAAA-MM-DD.md  ← preparar-protocolo (checklist e comprovante)
```

Quando o motor-experiencia está instalado, o protocolo vira uma linha de "trabalho do escritório" no histórico do cliente (`07-operacao/experiencia/clientes/<codigo>/historico.md`), que alimenta o resumo mensal e a página do caso.
