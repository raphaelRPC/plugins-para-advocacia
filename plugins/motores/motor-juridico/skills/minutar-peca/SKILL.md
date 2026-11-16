---
name: minutar-peca
description: >
  Redige a minuta de uma peça quando o escritório ainda não tem habilidade própria para ela:
  parte do dossiê do caso, da estratégia com a tese que o advogado definiu, da tese do banco do
  escritório, do modelo do escritório e do padrão da ficha jurídica. Toda citação sai marcada até
  a conferência, nada de julgado de memória. Entrega a minuta em .md com o cabeçalho interno
  "Antes de protocolar" e o .docx no padrão visual, por um script que não gera o arquivo enquanto
  houver pendência ou citação por conferir. Use quando o advogado disser "minuta a inicial da
  Marta", "redige a réplica, a tese é essa", "faz a primeira versão do recurso", "nova versão com
  o pedido de tutela". Não use para escolher a tese (use estrategia-do-caso) nem para a peça que já
  tem habilidade própria do escritório (use a habilidade própria).
---

# Minutar a peça

> A primeira versão da peça, no jeito do escritório, com cada fato ligado a um documento, cada pedido ligado a um fundamento e cada citação marcada até alguém conferir na fonte.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md` (a regra mais importante daqui). Etapas, `pecas.csv` e a pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Pesquisa: `../../docs/pesquisa-jus-ia.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quinta, 17h. A advogada definiu a tese da Marta de manhã e o prazo interno é segunda. O estagiário pega uma inicial antiga, troca o nome, cola um julgado "que sempre usamos" e escreve a data de cessação que achou primeiro. Na segunda, a advogada encontra "o autor" no meio da peça, uma súmula que ninguém conferiu e a data errada.

**Regras fixas desta habilidade:**
1. **Sem tese definida pelo advogado, não há minuta.** A habilidade não escolhe tese, caminho nem pedido. Sem a decisão registrada (`tese-definida` no `pecas.csv` ou em `estrategia.md`), ela para e indica a `estrategia-do-caso`.
2. **Toda citação nasce marcada `[CONFERIR: ...]`.** A IA nunca completa número, relator, data ou enunciado de julgado, súmula ou tema de memória: escreve o molde e manda pesquisar no Jus IA. Lei e artigo ela pode indicar, sempre com a marca e sem transcrever o texto de memória (`../../docs/citacoes.md`, regra 4). Só sai sem marca a citação da base do escritório conferida dentro de `validade_da_conferencia`.
3. **Cada fato com o documento, cada pedido com o fundamento e os fatos.** Fato sem prova e pedido sem fundamento vão para o "Antes de protocolar", e não para a peça como se estivessem resolvidos.
4. **Contradição do dossiê não é resolvida no chute.** Data, valor ou nome que diverge entre documentos fica `[A CONFIRMAR]` com os dois documentos, e o advogado decide.
5. **O mínimo de dados.** Qualificação, CPF, endereço e número de benefício saem do sistema do escritório no protocolo, como campo entre chaves. Dado de saúde só na medida que a tese precisa.

## 1. Quando usar

**Use quando:**
- O advogado definiu a tese e pede a minuta de uma peça que ainda não tem habilidade própria do escritório.
- A minuta precisa de nova versão (o advogado decidiu acrescentar um pedido, trocar um argumento).
- O `agente-juridico` chama no ciclo uma peça em `tese-definida` sem habilidade própria (modo "no ciclo").
- O `/motor-juridico:comecar` ou alguém do escritório quer ver a minuta de treino do caso 1 (modo "treino").
- A `adaptar-juridico` pede a estrutura das peças mais feitas (modo "adaptar").

**Não use quando:**
- Existe `escritorio/04-base/habilidades-do-escritorio/<peca>/`: use a habilidade própria, que já sabe o jeito do escritório para aquela peça.
- A tese ainda não foi escolhida: `estrategia-do-caso` (se instalada; sem ela, pergunte ao advogado a tese e o caminho, e registre a resposta dele em `estrategia.md`).
- São muitos casos iguais de uma vez: `pecas-em-lote` (se instalada), com a habilidade própria da peça.
- O pedido é conferir uma minuta pronta: `conferir-peca` e `conferir-citacoes`.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md` e `ficha-juridica.md`. Leia `nicho.md`, se existir, para o vocabulário do tipo de caso.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`). Regra de escrita guardada vale antes do padrão desta habilidade, desde que não afrouxe as regras fixas.
3. **Confira se há habilidade própria** para a peça em `escritorio/04-base/habilidades-do-escritorio/`. Se houver, diga e passe a ela.
4. **Leia o caso**, em `escritorio/07-operacao/juridico/casos/<codigo>/`: `dossie.md` (linha do tempo, matriz fato x prova, contradições, lacunas, dado sensível), `estrategia.md` (a tese, o caminho, os pedidos e o plano de provas que o advogado decidiu), `leitura-dos-autos.md` e `contraditorio.md`, se existirem.
5. **Leia a base:** a tese em `escritorio/04-base/juridico/teses/<tese>.md`, os temas de `04-base/juridico/jurisprudencia/` que a tese cita, o modelo do escritório em `04-base/juridico/modelos/<peca>/` (ou onde `onde_estao_os_modelos` disser) e o padrão visual em `04-base/juridico/padrao-visual.md`.
6. **Conta e dados.** Caso real só em conta profissional ou de equipe. Em conta pessoal, só os casos fictícios. Documento com dado de criança, laudo completo ou processo em segredo de justiça: só com autorização expressa do advogado responsável.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `quem_redige`, `fonte_e_corpo`, `citacao_em_recuo` |
| Melhora | J: `estilo`, `pedidos`, `tamanho_preferido`, `timbre`, `onde_estao_os_modelos` · também: `quem_revisa`, `quem_assina`, `validade_da_conferencia` |

Campo que falta e a minuta precisa: pergunte aquele campo, uma vez, e ofereça gravar. Sem `estilo` e `pedidos`, a minuta segue o padrão da seção 4 e o fim avisa. Sem `padrao-visual.md`, o .docx sai no padrão do script com aviso, e a habilidade oferece gravar um padrão mínimo a partir de `fonte_e_corpo` e `citacao_em_recuo` (ou a `adaptar-juridico`, que lê uma peça boa do escritório).

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | O advogado pede a minuta de um caso com tese | O código do caso e a peça | Minuta .md e .docx, resumo no chat, linha do `pecas.csv` |
| Direto | O advogado já entrega tudo ("inicial da C-2026-0001, tese tal, sem tutela, valor tal") | O pedido | O mesmo, perguntando só o que falta |
| Nova versão | O advogado decidiu mudar algo | A versão anterior e a decisão | `<peca>-v<n+1>.md`; a anterior fica intacta |
| No ciclo | O `agente-juridico` chama | A linha do `pecas.csv` em `tese-definida` | Minuta gravada e devolvida ao agente; nada no chat |
| Treino | Caso fictício ou "é teste" | O caso 1 de `../../docs/casos-ficticios.md` | O mesmo, gravado em `_treino/`; compare com `references/exemplo-caso-1.md` |
| Adaptar | A `adaptar-juridico` chama | As peças mais feitas e os modelos | A estrutura de cada peça, para aprovar |

### Passo 1. Conferir se pode minutar
Pergunte, se não estiver claro: "Qual é o caso e qual é a peça?". Depois confira, sem perguntar o que já está escrito:
- a tese está definida pelo advogado (etapa `tese-definida` ou decisão datada em `estrategia.md`)? Não: pare. "A tese deste caso ainda não foi definida. A estrategia-do-caso prepara os caminhos para a advogada escolher."
- a peça tem habilidade própria? Sim: passe a ela.
- o prazo interno é hoje ou amanhã? Diga logo no começo, para quem pediu decidir a ordem do dia.
- há dado sensível que o dossiê marcou como "não vai à peça"? Anote para o passo 4.

### Passo 2. Juntar o material
Monte, para você, a lista do que a minuta vai usar: fatos com o documento de cada um (da matriz do dossiê), a tese e a ordem dos argumentos (do banco de teses), as citações da base com a data da conferência, os pedidos e as provas da estratégia, os trechos do modelo do escritório. O que falta para a peça e não está em nenhum lugar: pergunte uma coisa por vez ("O valor da causa já tem a conta?"). Sem resposta, `[A DEFINIR]` ou `[A CONFIRMAR]` no lugar, e a pendência vai para o cabeçalho.

### Passo 3. Escrever
Siga a seção 4, a estrutura do modelo do escritório (ou a de `assets/modelo-minuta.md`, se o escritório não tiver modelo) e o padrão da ficha. Uma seção por vez, nesta ordem: fatos, fundamentos, pedidos, provas, valor, fecho, endereçamento e qualificação por último (são os que mais carregam sobra de outra peça).

### Passo 4. Marcar e montar o "Antes de protocolar"
Marque cada citação pela seção 5. Monte o cabeçalho interno pela seção 6: quem revisa e assina, a tese e quem decidiu, as citações marcadas, as contradições, o que pedir ao cliente, o dado sensível que ficou fora de propósito, a lista de documentos citados, as conferências com `- [ ]`.

### Passo 5. Mostrar
Mostre a minuta inteira e, por cima, o resumo da seção 7 ("Formato da saída"). Pergunte: "Quer ajustar alguma coisa antes de eu gravar?". Grave com o ok.

### Passo 6. Gravar e gerar o .docx
Grave em `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md` e rode, com o caminho da pasta desta habilidade (a que contém este SKILL.md) e o da minuta como argumentos:

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" "escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md" --padrao "escritorio/04-base/juridico/padrao-visual.md"
```

A primeira linha diz uma de três coisas:
- **"NÃO ESTÁ PRONTA"**: lista as citações por conferir (cada `[CONFERIR]` da peça é pendência), as marcações, os campos em maiúsculas que sobraram, as variáveis `{{...}}` sem preencher e as conferências do cabeçalho sem `[x]`. **Nenhum .docx é criado** (saída 2). Na primeira versão de uma peça com citações, este é o resultado esperado: a minuta segue para a conferência.
- **"PRONTA PARA GERAR O .DOCX"**: o texto está resolvido e só sobraram campos entre chaves de quem protocola (`{QUALIFICAÇÃO COMPLETA}`, `{DATA DO PROTOCOLO}`). O .docx sai com eles em amarelo.
- **"SEM PENDÊNCIA NO TEXTO DA PEÇA"**: o .docx sai no padrão visual, sem o cabeçalho e sem o "Antes de protocolar".

Para o advogado ler no Word uma minuta ainda com pendência, `--forcar`: o .docx sai com o que sobrou em amarelo e o aviso de que não pode ser protocolado assim. Nunca use `--forcar` no ciclo. Para só conferir, `--so-conferir`. Para conferir um .docx que alguém editou, `--conferir-docx <arquivo.docx>`. Sem `python-docx`, o script confere do mesmo jeito e diz como gerar o .docx. Sem execução de código: entregue o .md e diga para abrir no Word, apagar o cabeçalho e a seção "Antes de protocolar" e salvar como .docx.

### Passo 7. Registrar e passar adiante
Mostre a linha do `pecas.csv` e grave com o ok: `etapa = minuta`, `habilidade_usada = minutar-peca`, `tese`, `citacoes = nao-conferidas` (ou `verde` só quando nenhuma citação ficou marcada e todas as da base estão dentro da validade), `dados = nao-conferidos`, `responsavel`, `atualizado_em`. Diga o próximo passo: `conferir-citacoes` e `conferir-peca`.

### Passo 8. Aprender
Pergunte: "Alguma coisa nesta minuta você faria diferente nas próximas?". Cada correção de escrita vira regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Se a mesma peça já saiu três vezes boa pela `minutar-peca`, ofereça: "Esta peça já tem três versões aprovadas. Quer que ela vire habilidade própria do escritório?" (`peca-vira-habilidade`, se instalada). Correção que pede citação de memória ou escolha de tese pela IA: explique por que não pode guardar e proponha a versão que cabe.

### Modo no ciclo
1. O agente passa a linha do `pecas.csv`. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 4 e 6, sem `--forcar`. O que faltar vira `[A CONFIRMAR]` ou `[A DEFINIR]` na peça e item no cabeçalho.
3. Caso que deve parar (sem tese, habilidade própria existente, dado sensível sem autorização, área que não é do escritório): nenhuma minuta; devolva ao agente a frase do porquê, para "ADVOGADO AGORA".
4. Atualize no `pecas.csv` só o que `../../docs/producao.md` (regra 5) permite ao agente: `etapa = minuta`, `citacoes`, `dados`, `atualizado_em`.
5. Devolva ao agente: caminho da minuta, número de citações marcadas, as citações que precisam de pesquisa no Jus IA (tema e o que procurar), as pendências para o advogado e a primeira linha do script. O agente grava o item na fila com `revisor: pendente`.

### Modo treino
Use o caso 1 (Marta) de `../../docs/casos-ficticios.md`, com a tese `restabelecimento-incapacidade` como se a advogada a tivesse definido. Grave em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/minutas/`. Compare com `references/exemplo-caso-1.md`: a data de cessação não escolhida, o relatório médico atual pedido, nenhum diagnóstico na peça, nenhum dano moral, três citações marcadas e o script dizendo "NÃO ESTÁ PRONTA".

### Modo adaptar
1. Leia `pecas_mais_feitas`, `onde_estao_os_modelos`, `estilo`, `pedidos` e `nicho.md`.
2. Para cada peça mais feita sem habilidade própria, monte a estrutura do escritório a partir de uma peça boa (partes na ordem, abertura, fecho, jeito de numerar e de pedir), marcando `[NOVO]` ou `[ALTERADO]` em relação a `assets/modelo-minuta.md`.
3. Mostre e pergunte: "É assim que essa peça sai do escritório?". Com o ok, grave em `escritorio/04-base/juridico/modelos/<peca>/estrutura.md`.
4. Devolva à `adaptar-juridico` a lista das peças com três ou mais peças boas, candidatas à `peca-vira-habilidade`.

## 4. Como a minuta é escrita

| Parte | Como escrever |
|---|---|
| Fatos | Um fato por parágrafo, na ordem da linha do tempo do dossiê, com o documento no fim: "(doc. 3)". Nada de fato que não está no dossiê. Fato importante sem documento: escreve e põe no cabeçalho "fato sem prova" |
| Fundamentos | A tese do banco, na ordem dos argumentos de lá. Cada argumento ligado aos fatos que ele usa. Resposta provável da outra parte (do `contraditorio.md`, se existir) enfrentada no lugar certo |
| Pedidos | Numerados, cada um com o fundamento e os fatos ao lado ("com fundamento no item 2.1 e nos fatos 1.2 a 1.5"), só os que a estratégia decidiu |
| Provas | As do plano de provas da estratégia |
| Valor da causa | Do advogado, com a conta em anexo. Sem a conta: `[A DEFINIR]`. A regra de cálculo da peça entra no cabeçalho como `[CONFERIR]` |
| Requisitos formais | Endereçamento, competência, documentos obrigatórios, alçada: o que a peça exige vai no cabeçalho como conferência `[CONFERIR]`, nunca afirmado de memória |
| Qualificação | Campo entre chaves de quem protocola, do sistema do escritório |

Escrita: português jurídico claro, frases curtas, um assunto por parágrafo, sem latim desnecessário, sem adjetivo sobre a outra parte, o juízo ou o perito, sem "data venia", sem caixa alta em frase inteira. O tratamento da parte (a autora, o requerente) é um só na peça toda e segue o gênero do dossiê. O tamanho segue `tamanho_preferido`; passou, diga onde dá para cortar.

## 5. As citações na minuta

| Situação | Como entra |
|---|---|
| Norma citada pela tese, ainda não conferida | `art. N da Lei N/AAAA [CONFERIR: vigência e redação na data dos fatos]` |
| Julgado da base conferido há menos de `validade_da_conferencia` | Sem marca, e no cabeçalho: "da base, `<tema>.md`, conferido em AAAA-MM-DD" |
| Julgado da base com conferência vencida | Com a marca: `[CONFERIR: conferência vencida em AAAA-MM-DD]` |
| A tese precisa de um julgado e a base não tem | Molde `[TRIBUNAL], [CLASSE] nº [NÚMERO], Rel. [NOME], julgado em [DATA] [CONFERIR: pesquisar no Jus IA: <o que procurar>]`, e a busca vai para a lista "pesquisar no Jus IA" |
| Trecho entre aspas | Só se veio da fonte conferida palavra por palavra; senão, paráfrase sem aspas e com a marca |
| Súmula, tema ou tese de repetitivo | `[CONFERIR: existe, não foi cancelada, enunciado igual]` |
| Julgado contrário à tese, na base | Não vai à peça como se fosse a favor; se a estratégia mandou enfrentar, entra com a marca e a distinção |

A conferência é da `conferir-citacoes` (se instalada; sem ela, a lista de citações vai no cabeçalho para o advogado conferir na fonte). A pesquisa de julgado é sempre no Jus IA (`../../docs/pesquisa-jus-ia.md`).

## 6. O cabeçalho interno "Antes de protocolar"

Fica logo depois do cabeçalho YAML, num título que começa com "Antes de protocolar", e termina na linha `<!-- fim: antes de protocolar -->`. O script não leva nada disso para o .docx. O modelo está em `assets/modelo-minuta.md`.

| Item | Exemplo |
|---|---|
| Quem revisa e assina, com a sigla | advogada titular · H |
| A tese e quem decidiu | definida pela advogada em 2026-04-13, `estrategia.md` |
| Citações | 3 marcadas; 1 da base, conferida em 2026-04-15 |
| Contradições do dossiê | data de cessação: D1 diz 28/02, D2 diz 05/03 |
| O que pedir ao cliente | relatório médico posterior à cessação |
| Dado sensível fora da peça | o diagnóstico do relatório médico |
| Documentos citados, na ordem | doc. 1 a doc. 6 |
| Conferências, uma por linha com `- [ ]` | citações, dados, requisitos formais, leitura do advogado |

## 7. Formato da saída

**No chat, por cima da minuta:**

```
MINUTA · [codigo] · [peca] v[n] · tese [nome]
Prazo interno: [AAAA-MM-DD]    Quem revisa: [função]    Quem assina: [função]
Citações: [N] marcadas · [N] da base dentro da validade · pesquisar no Jus IA: [temas]
Pendências para o advogado: [lista curta]
O que pedir ao cliente: [lista ou "nada"]
Script: [primeira linha da saída]
Próximo passo: conferir-citacoes e conferir-peca
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Minuta | `escritorio/07-operacao/juridico/casos/<codigo>/minutas/<peca>-v<n>.md` e o `.docx` ao lado |
| Linha do registro | `escritorio/07-operacao/juridico/pecas.csv`: `etapa`, `habilidade_usada`, `tese`, `citacoes`, `dados`, `responsavel`, `atualizado_em` |
| Decisão do advogado registrada na hora (modo direto) | `escritorio/07-operacao/juridico/casos/<codigo>/estrategia.md`, na seção da decisão, com data e quem decidiu |
| Estrutura das peças (modo adaptar) | `escritorio/04-base/juridico/modelos/<peca>/estrutura.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

No modo "no ciclo", o item da fila (`07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-<peca>.md`) é gravado pelo agente. Sem pasta aberta: a minuta sai no chat, em bloco, com o caminho onde ficaria, e a linha do registro como tabela.

## 9. Solo e equipe

**Solo:** quem minuta e quem revisa é a mesma pessoa. Minute num momento e revise em outro, de preferência no dia seguinte; o cabeçalho interno é a lista da revisão. **Equipe:** o estagiário (ou quem `quem_redige` disser) roda esta habilidade; a advogada recebe a minuta depois da conferência, com o relatório. Se o advogado pede sempre a mesma correção, ela vira aprendizado, e a peça vira candidata a habilidade própria.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Minutar sem a tese do advogado | A IA escolhe o caminho do caso | Regra fixa 1 e passo 1 |
| Julgado "que sempre usamos" de memória | Citação inventada ou superada no processo | Toda citação marcada; molde e pesquisa no Jus IA quando a base não tem |
| Sobra de outra peça (nome, gênero, data) | Peça que expõe outro cliente e perde credibilidade | Partir do dossiê e do modelo, não de uma peça antiga; qualificação por último; a `conferir-peca` depois |
| Data escolhida no chute entre dois documentos | Parcelas erradas e contradição usada pela outra parte | `[A CONFIRMAR]` com os dois documentos |
| Pedido sem fundamento | Pedido negado e peça fraca | Cada pedido com o item do fundamento e os fatos |
| .docx gerado com marca e protocolado | Peça com `[CONFERIR]` no processo | O script não cria o .docx com pendência sem `--forcar` |
| Diagnóstico ou dado de criança na peça | Exposição do cliente | Só o que a tese precisa; o resto vai para o cabeçalho |

## 11. Próximo passo

- Conferência: `conferir-citacoes` e `conferir-peca` (se instaladas; sem elas, o cabeçalho é a lista do que o advogado confere).
- Citação sem fonte: pesquisa no Jus IA e `trazer-pesquisa` (se instalada) para guardar na base.
- Resposta da outra parte: `advogado-do-diabo` (se instalada), antes da revisão.
- Depois da aprovação: `preparar-protocolo` (se instalada).
- Peça que sai sempre igual: `peca-vira-habilidade` (se instalada).

## Referências desta habilidade

- `assets/modelo-minuta.md`: o esqueleto da minuta com o cabeçalho "Antes de protocolar". Leia no passo 3 quando o escritório não tem modelo da peça, e no modo adaptar.
- `references/exemplo-caso-1.md`: a minuta da Marta (caso 1, fictício) resolvida, com o que o script responde. Leia no modo treino e quando tiver dúvida sobre como marcar.
- `scripts/md_para_docx.py`: confere a minuta e gera o .docx no padrão visual. Rode no passo 6.
