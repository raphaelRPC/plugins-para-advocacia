---
name: adaptar-controladoria
description: >
  Adapta o motor-controladoria ao escritório: os tribunais, as cidades e os sistemas onde os
  processos tramitam (com o calendário de cada um); as regras próprias ("nenhum prazo no último
  dia", "recurso também na agenda do sócio"), cada uma classificada e levada ao lugar certo, e a
  que mexe em contagem só vale depois da validação da tabela de regras; o perfil do nicho
  (nicho.md), por entrevista, sem perfil pronto; os materiais de cada habilidade no modo
  adaptar; os casos de teste com gabarito conferido por duas pessoas; e as rotinas
  próprias viradas habilidade, testadas e empacotadas. Use quando disserem "adapta a
  controladoria ao escritório", "a gente nunca cumpre prazo no último dia", "testa com as nossas
  publicações", "transforma essa rotina em habilidade". Não use para preencher a ficha (use
  /motor-controladoria:ficha) nem para montar o calendário (use calendario-forense).
---

# Adaptar a controladoria ao escritório

> O plugin chega com o método pronto e o conteúdo vazio. Esta habilidade faz ele trabalhar nos tribunais do escritório, com as regras que o escritório já pratica e os casos que já pegaram a equipe, sempre a partir do que as pessoas confirmam.

Camadas de adaptação: `../../docs/adaptar-ao-escritorio.md`. Regras: `../../docs/regras.md`. Contagem: `../../docs/contagem.md`. Publicações e prazos: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela de campos em `../../docs/ficha-da-controladoria.md`. Onde gravar: `../../docs/pasta.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

Um escritório trabalhista de Contagem instala o plugin. O primeiro resumo mostra o recurso de um cliente com a fatal numa sexta, e a sócia lembra que ali ninguém cumpre prazo no último dia; que a vara de Contagem segue um feriado municipal que o calendário de BH não tem; e que todo recurso entra também na agenda dela. Nada disso é erro do método: falta o escritório.

**Regras fixas desta habilidade:**
1. **Do escritório, não da internet.** Tribunais, regras, nicho e casos de teste saem da entrevista com as pessoas e do material delas (publicações reais anonimizadas). O plugin não traz perfil de nicho pronto, nem calendário, nem prazo por ato. O que a habilidade sugerir vai marcado "sugestão" e só entra com o ok.
2. **Regra que mexe em contagem passa pela validação da tabela de regras.** Dia útil, início do prazo, número de dias por ato, dobro e ciência vão para `regras-de-contagem.md` ou para o calendário pela `calendario-forense`, e só valem com `validada_por` e `validada_em`. Antes disso, todo prazo sai com o aviso "regra ainda não validada pelo escritório".
3. **Adaptar não afrouxa.** Regra que deixa a data fatal mais tarde do que a tabela, que dispensa a dupla conferência ou que põe senha com a IA não entra, e a habilidade explica por quê e propõe a versão segura. Na dúvida entre duas datas, vale a mais cedo.
4. **Só com o ok.** Cada mudança aparece marcada `[ALTERADO]` ou `[NOVO]`, e nada é gravado sem a pessoa aprovar.
5. **Habilidade nova só sai testada.** Três casos passando e o script de empacotamento sem erro; antes disso, não há .zip.

## 1. Quando usar

**Use quando:**
- O escritório acabou de instalar o plugin e quer que ele trabalhe nos tribunais e no jeito da casa.
- Entrou um tribunal, uma comarca ou um sistema novo; ou o escritório mudou de nicho.
- Uma regra própria apareceu ("nenhum prazo no último dia", "recurso também na agenda do sócio").
- Os aprendizados da controladoria passaram de 30 linhas `em uso`, ou chegou a revisão trimestral.
- A equipe quer testar o plugin com as publicações e as armadilhas dela, e não só com o lote fictício.
- Existe uma rotina da controladoria que o escritório faz sempre do mesmo jeito e nenhuma habilidade cobre.

**Não use quando:**
- O pedido é preencher campos da ficha (OABs, agenda, dias de segurança): `/motor-controladoria:ficha`.
- O pedido é montar o calendário do ano ou validar a tabela de regras: `calendario-forense` (esta habilidade leva a regra até ela).
- O pedido é adaptar triagem de contatos, mensagens ou jornada do cliente: `adaptar-comercial` do motor-comercial ou `adaptar-experiencia` do motor-experiencia (se instalados). O `nicho.md` é o mesmo arquivo.
- A rotina é grande, envolve vários setores e precisa de POP e medição: `pop-para-skill` do `inicio-automacao` (se instalado). Esta habilidade faz o caminho curto.

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-controladoria.md`, `nicho.md` (se existir), `aprendizados-controladoria.md` e `rotinas-do-escritorio.md` (se existir).
2. **Leia a base da controladoria:** `04-base/controladoria/regras-de-contagem.md` (validada? por quem?), os calendários em `04-base/controladoria/calendario/`, `paineis.md` e `providencias.md`, se existirem.
3. **Sem ficha:** ofereça `/motor-controladoria:comecar`. Para seguir, pergunte só: "Em que áreas vocês atuam?" e "Em que tribunais os processos de vocês tramitam?".
4. **Veja o que está instalado:** as pastas de habilidade do plugin (no Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/`) e `escritorio/04-base/habilidades-do-escritorio/`. A lista define quem é chamado no modo "adaptar".
5. **Conta.** Publicação real, mesmo anonimizada, só em conta profissional ou de equipe. Em conta pessoal, a entrevista segue sem material real, e os testes usam só o lote fictício.
6. **Se o `nicho.md` já existe** (escrito por outro plugin motor), ele é comum: atualize, nunca reescreva do zero, e não apague o que outra habilidade escreveu sem perguntar.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · K: `tribunais` |
| Melhora | E: `nicho`, `rotinas_proprias` · K: `regras_proprias` |

Também atualiza, com o ok, K: `cidades_dos_juizos`, `paineis_dos_sistemas`, `dias_de_seguranca`, `lembretes` e `quem_confere`, quando a entrevista responde a eles. O que a entrevista responder que é fato da ficha volta para a ficha, com a linha no histórico.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Completo | Primeira adaptação | Partes A a F, na ordem, uma de cada vez, com pausa entre elas |
| Rápido | Pouco tempo | Quatro perguntas (abaixo); o resto fica para depois |
| Uma parte | "Só as regras", "só os casos de teste", "só essa rotina" | A parte pedida |
| De novo | Tribunal novo, nicho novo, revisão trimestral | As partes que mudaram, com `[ALTERADO]` |

Comece dizendo: "Vou adaptar a controladoria com o que vocês já praticam. O que não tiver resposta fica para preencher, e eu não invento nada: nenhuma data, nenhum prazo, nenhum feriado." Pergunte por onde começar e sugira A e B: é onde a conta muda.

**Modo rápido** (no máximo quatro perguntas): "Em que tribunais e cidades os processos tramitam?" · "Que sistemas alguém abre todo dia?" · "Que regra de prazo vocês seguem que não está em lei nenhuma?" · "Qual armadilha de prazo já pegou vocês?". O resto fica `[A PREENCHER]` e o fechamento diz o que falta.

### Parte A. Tribunais, cidades e sistemas
A1. Pergunte: "Em que tribunais e em que cidades os processos de vocês tramitam?". Para cada um: "Quantos processos, mais ou menos?" (estimativa, marcada assim).
A2. Pergunte: "Que sistemas alguém abre todo dia, e quem abre?" (PJe, eproc, e-SAJ, Projudi, Domicílio Judicial Eletrônico). Quem abre usa a própria senha ou certificado; a IA nunca acessa.
A3. Mostre a tabela da seção 4 e grave na ficha, com o ok: `tribunais`, `cidades_dos_juizos`, `paineis_dos_sistemas`.
A4. Para cada tribunal sem calendário do ano em `04-base/controladoria/calendario/`, diga: "Falta o calendário de [tribunal]: sem ele, o próximo dia útil pode estar errado." e chame a `calendario-forense` (se instalada; sem ela, a pessoa monta o calendário no formato de `contagem.md`, "O que vale como dia útil", com fonte e conferência).
A5. Para cada sistema, chame a `paineis-dos-sistemas` (se instalada) para o roteiro de quem abre e quando.

### Parte B. As regras próprias
B1. Pergunte: "Que regras de prazo vocês seguem que não estão na lei? Por exemplo: nunca cumprir no último dia, recurso também na agenda do sócio, prazo de hoje conferido por duas pessoas presentes." Uma regra de cada vez, na frase do escritório.
B2. Para cada regra, classifique pela tabela de `assets/modelo-regras-proprias.md` (contagem, segurança, agenda, conferência, triagem e providência, painéis) e mostre: "Esta regra é de [classe]. Ela vai para [destino] e passa por [caminho]."
B3. **Contagem:** a regra não é gravada aqui. Ela vai para a `calendario-forense` (se instalada), que conduz a validação da tabela de regras (linha nova com chave própria, em minúsculas e com hífen, a fonte e `[CONFERIR]`; ou a linha da seção "Prazos por ato"; ou a linha do calendário). Até `validada_por` e `validada_em`, a regra fica "em validação". Sem a `calendario-forense`, mostre a linha proposta e diga quem precisa validar e onde.
B4. **Segurança, agenda, conferência:** com o ok, grave em `regras_proprias` (e em `dias_de_seguranca`, `lembretes` ou `quem_confere`, quando for o caso), com linha no histórico da ficha. Diga qual habilidade passa a ler: `calcular-prazo` (segurança), `agenda-de-prazos` (agenda), `dupla-conferencia` (conferência).
B5. **Triagem e providência:** leve à `providencia-sugerida` (se instalada), que monta `providencias.md`.
B6. **Regra recusada:** se a regra deixa a fatal mais tarde, dispensa uma pessoa ou põe senha com a IA, explique em uma frase e proponha a versão segura (exemplo em `assets/modelo-regras-proprias.md`, R4). Registre como `recusada`, com o motivo.
B7. Com o ok, grave o quadro em `escritorio/04-base/controladoria/nicho/adaptar-controladoria.md` (o que esta habilidade ajustou para o escritório), no formato do modelo, e a frase curta de cada regra em uso no campo `regras_proprias` da ficha, que as outras habilidades leem.

### Parte C. O nicho
Siga o formato de `nicho.md` em `../../docs/adaptar-ao-escritorio.md`. O plugin não traz perfil pronto: tudo sai da entrevista e do material do escritório. Para a controladoria, as seções que mais pesam são "Os casos que chegam", "Sazonalidade e ritmo" e "Cuidados do nicho". Pergunte, uma de cada vez, só o que o `nicho.md` ainda não tiver:
1. "Que atos chegam mais, e quais chegam iguais para muitos processos?" (sinal para a `triagem-em-massa`, se instalada)
2. "Tem perícia, audiência ou valor a receber com frequência?" (pauta, `audiencias-e-pericias`; RPV e alvará, `acompanhar-valores`)
3. "Em que época do ano chega mais publicação, e quando a equipe sai de férias?" (`cobertura-de-ausencia`)
4. "Que dado sensível costuma aparecer nas publicações?" (saúde, criança, renda: o resumo da publicação não leva)
Grave com o ok, marcando cada linha nova `[NOVO]` e a origem ("entrevista", "visto em publicação"). Frequência é estimativa, marcada assim; tempo de fase fica `[CONFERIR]`.

### Parte D. Os materiais de cada habilidade
D1. Monte a tabela da seção 5 só com as habilidades instaladas e mostre: "Estas habilidades têm materiais que mudam com o escritório. Quer adaptar todas, ou começar por alguma?" Sugira começar pela `triar-publicacoes` e pela `rotina-da-controladoria`.
D2. Chame cada uma no modo "adaptar", uma de cada vez. Cada uma lê as fichas, o `nicho.md` e as regras próprias, e devolve o que mudou com `[ALTERADO]` e `[NOVO]`. Habilidade sem modo "adaptar": diga em uma linha e siga.
D3. Mostre o que mudou, no formato da seção 6. A pessoa aprova item por item; a habilidade chamada grava só o que teve ok.

### Parte E. Os casos de teste do escritório
E1. Peça de 3 a 6 publicações reais anonimizadas: uma que quase virou prazo perdido, uma com feriado local, uma de outra parte (prazo que não é do escritório), uma duplicada, uma de processo que não estava na carteira, uma intimação de portal.
E2. Para cada uma, pergunte: "Qual é a armadilha deste caso, e o que a habilidade não pode deixar passar?". As datas do gabarito são contadas por uma pessoa e conferidas por outra, com o calendário do ano; a habilidade pode sugerir, marcado "sugestão".
E3. Grave em `escritorio/04-base/casos-de-teste/controladoria/casos.md`, no formato de `assets/modelo-casos-de-teste.md`.
E4. Rode as habilidades nos casos, sem mostrar o gabarito, gravando em `_treino/`. Compare com "Não pode falhar". Erro: falta linha no calendário, regra não validada, campo da ficha, linha do nicho ou aprendizado. Proponha o ajuste e rode de novo.

### Parte F. Rotina própria da controladoria vira habilidade
Para o que o escritório faz sempre do mesmo jeito e não é regra de contagem (a conferência de sexta, a checagem dos painéis na volta do almoço).
F1. A entrevista, uma pergunta por vez: "O que dispara essa rotina?" · "O que se faz, passo a passo?" · "Com que material?" · "Quem faz cada passo e quem confere?" · "O que nunca pode acontecer?" · "Quando a rotina tem de parar e chamar uma pessoa?" · "Como alguém do escritório pede isso, com as palavras de vocês?"
F2. Escreva a rotina em `escritorio/04-base/comum/rotinas-do-escritorio.md`, com S, A e H em cada passo (`../../docs/regras.md`, seção 5.1). Confirmar prazo, decidir dobro, ciência tácita e providência ficam sempre H.
F3. Gere a habilidade em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`, pelo `assets/modelo-rotina-controladoria.md`. Mostre inteira e grave com o ok.
F4. Teste com três casos (o comum, o com exceção, o que deve parar), em `_treino/`, e registre em `escritorio/04-base/casos-de-teste/controladoria/<nome>-testes.md`, no formato de `assets/modelo-registro-dos-testes.md`.
F5. Empacote, da pasta de trabalho:
```
python3 "<pasta desta habilidade>/scripts/empacotar_habilidade.py" "escritorio/04-base/habilidades-do-escritorio/<nome>" --testes "escritorio/04-base/casos-de-teste/controladoria/<nome>-testes.md"
```
No plugin instalado, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/adaptar-controladoria`. O script confere nomes de arquivo (`[a-z0-9._-]`, caminho até 100 caracteres), o frontmatter, a seção de campos, o passo "Aprender", travessões, arquivos citados, norma com número sem `[CONFERIR]`, frase que manda a IA confirmar prazo ou entrar em sistema, e os três testes com "O que saiu" preenchido, "Resultado: passou" e o "Conferido por". Com erro, sai com código 1 e não gera nada. Sem erro, grava `escritorio/04-base/habilidades-do-escritorio/<nome>.zip`.
F6. Instalar e ligar: Personalizar > Habilidades > Enviar, com o .zip (conferir na configuração da conta). Se o ciclo estiver em uso, ofereça marcar a rotina como "no ciclo: sim" em `rotinas-do-escritorio.md` e, com o ok, acrescentar uma linha ao bloco "Controladoria" de `escritorio/CLAUDE.md` e ao texto da tarefa agendada da `rotina-da-controladoria` (se instalada): "Depois do ciclo, rode a habilidade <nome>".

### Passo final. Aprender
Pergunte: "Alguma coisa na adaptação você faria diferente?". Cada correção vira regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Regra que vale para todos os plugins vai para a ficha do escritório. Proponha quando adaptar de novo (seção 7).

## 4. A tabela dos tribunais (parte A)

```
TRIBUNAIS DO ESCRITÓRIO · AAAA-MM-DD
| Tribunal | Cidades dos juízos | Processos (estimativa) | Sistema | Quem abre | Calendário do ano |
|---|---|---|---|---|---|
| TRT3 | Belo Horizonte, Contagem | 40 | PJe | estagiária, 9h | falta: calendario-forense |
| TRF6 | Belo Horizonte (JEF) | 25 | sistema do JEF | estagiária, 9h | conferido em 2026-01-10 |
```

## 5. O que cada habilidade costuma reescrever no modo "adaptar"

| Habilidade | O que costuma mudar com o escritório | Onde fica |
|---|---|---|
| `captar-publicacoes` | As fontes, os horários e o formato da planilha ou do e-mail que chega | K: `fontes_de_publicacao`, `horario_da_captacao` |
| `triar-publicacoes` | Os tipos de ato mais comuns do nicho e o vocabulário dos despachos | A habilidade e `nicho.md` |
| `calendario-forense` | Os tribunais, as cidades e as regras próprias de contagem, validadas | `04-base/controladoria/calendario/` e `regras-de-contagem.md` |
| `calcular-prazo` | A segurança por tipo de ato | K: `dias_de_seguranca`, `regras_proprias` |
| `dupla-conferencia` | Quem confere o quê | K: `quem_confere`, `regras_proprias` |
| `agenda-de-prazos` | Onde o prazo vai e quem mais recebe | K: `onde_fica_a_agenda`, `lembretes`, `regras_proprias` |
| `providencia-sugerida` | A providência de costume para cada ato | `04-base/controladoria/providencias.md` |
| `paineis-dos-sistemas` | Os sistemas, quem abre e quando | `04-base/controladoria/paineis.md` |
| `rotina-da-controladoria` | Horários, janelas e o que entra no resumo | Ficha da automação e a tarefa agendada |
| `painel-da-controladoria` | As janelas e os rótulos | A habilidade |
| `cobertura-de-ausencia` | Quem assume por área e a janela da volta | K: `cobertura_de_ausencia`, `responsaveis_por_area` |
| `acompanhar-valores` | O caminho de cada tipo de valor nos tribunais do escritório | A referência da habilidade |
| `triagem-em-massa` | Os grupos de atos iguais do nicho | A habilidade |

Mostre só as linhas das habilidades instaladas. O que cada uma faz de fato no modo "adaptar" está no SKILL.md dela.

## 6. Formato da saída

**O que mudou, por habilidade (parte D):**

```
ADAPTAÇÃO · [habilidade] · AAAA-MM-DD
| Material | O que mudou | Antes | Depois | Decisão |
|---|---|---|---|---|
| segurança de recurso | [ALTERADO] | 2 dias úteis | 3 dias úteis (regra R1) | sim |
```

**Fechamento da adaptação:** o que foi gravado (com caminho e versão), as regras em validação e quem valida, o que ficou `[A PREENCHER]`, os calendários que faltam, o resultado dos testes, as habilidades próprias (instaladas ou o que falta) e a data sugerida para adaptar de novo.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Tribunais, cidades, sistemas e regras na ficha | `escritorio/04-base/comum/ficha-da-controladoria.md`, com linha no histórico |
| Quadro das regras próprias (classe, destino, situação) | `escritorio/04-base/controladoria/nicho/adaptar-controladoria.md` |
| Regras de contagem (pela validação) | `escritorio/04-base/controladoria/regras-de-contagem.md` e `calendario/`, gravados pela `calendario-forense` |
| Perfil do nicho | `escritorio/04-base/comum/nicho.md` (comum aos plugins motor) |
| Materiais adaptados | Nos caminhos de cada habilidade (seção 5), gravados por ela com o ok |
| Casos de teste do escritório | `escritorio/04-base/casos-de-teste/controladoria/casos.md` |
| Rotinas próprias | `escritorio/04-base/comum/rotinas-do-escritorio.md` |
| Habilidade de rotina e o pacote | `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md` e `<nome>.zip` |
| Testes das habilidades novas | `escritorio/04-base/casos-de-teste/controladoria/<nome>-testes.md` |
| Rodadas de teste | `escritorio/07-operacao/_treino/controladoria/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

**Quando adaptar de novo:** tribunal, comarca ou sistema novo; nicho novo; virada do ano (calendários e tabela de regras); os aprendizados passaram de 30 linhas `em uso`; a revisão trimestral. Sem pasta aberta: o quadro das regras, o perfil e as habilidades novas saem no chat, em blocos, com o caminho de cada um; o .zip só existe com pasta aberta e o script.

## 8. Solo e equipe

**Solo:** a adaptação completa leva uma tarde; o modo rápido, meia hora. Comece pelos calendários (parte A) e pelas regras (parte B): é onde um prazo pode mudar de data. A validação da tabela é sua, com calma, e volta todo ano.

**Equipe:** quem capta e tria participa das partes A, C e E: é quem conhece o despacho que confunde e a armadilha que já pegou. Quem responde pela controladoria valida a tabela de regras e assina o gabarito dos casos de teste, com uma segunda pessoa conferindo. Uma pessoa é dona das habilidades do escritório, e só ela gera versão nova e o .zip.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Regra de contagem gravada sem validação | Prazo contado por regra que ninguém conferiu na fonte | Regra fixa 2: contagem só pela `calendario-forense`, com `validada_por` |
| Regra que empurra a fatal ("manutenção sempre empurra") | Prazo perdido por um dia | Regra fixa 3: recusada com a versão segura |
| Perfil de nicho ou feriado tirado da internet | Calendário com dia errado, triagem fora da realidade | Regra fixa 1: entrevista e material do escritório |
| Tribunal novo sem calendário | "Próximo dia útil" errado no resumo | Parte A4 aponta e chama a `calendario-forense` |
| Teste só com o lote fictício | A armadilha do escritório aparece num prazo real | Casos de teste com gabarito conferido por duas pessoas |
| Habilidade do escritório que confirma prazo | A IA passa a decidir o que é da pessoa | O script de empacotamento barra a frase |
| Dois perfis de nicho, um por plugin | Cada plugin entende o escritório de um jeito | Um `nicho.md` comum, atualizado e nunca reescrito |

## 10. Próximo passo

- Calendário e validação da tabela: `calendario-forense`.
- Painéis: `paineis-dos-sistemas` (se instalada).
- Providências de costume: `providencia-sugerida` (se instalada).
- Ciclo diário no jeito do escritório: `rotina-da-controladoria`.
- Rotina grande, com vários setores: `pop-para-skill` do `inicio-automacao` (se instalado); sem ele, quebre a rotina em partes pequenas e use a parte F para cada uma.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

- `assets/modelo-regras-proprias.md`: as classes de regra, o destino de cada uma, o que não entra e o formato do quadro, com exemplo. Leia na parte B.
- `assets/modelo-casos-de-teste.md`: o formato dos casos de teste do escritório, com exemplo a partir do lote de treino. Leia na parte E.
- `assets/modelo-rotina-controladoria.md`: o esqueleto da habilidade de rotina e um exemplo preenchido. Leia no passo F3.
- `assets/modelo-registro-dos-testes.md`: o formato do registro dos três testes, que o script confere. Leia no passo F4.
- `scripts/empacotar_habilidade.py`: confere e empacota a habilidade de rotina. Rode no passo F5.
