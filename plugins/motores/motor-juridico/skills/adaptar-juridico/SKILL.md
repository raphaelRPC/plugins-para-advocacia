---
name: adaptar-juridico
description: >
  Adapta o motor-juridico ao escritório: as áreas e as peças que mais saem, com onde estão as
  peças boas; o perfil do nicho (nicho.md), por entrevista, sem perfil pronto e sem internet; o
  padrão visual das peças (padrao-visual.md), lido de uma peça boa em .docx por script e
  confirmado pelo advogado; os materiais de cada habilidade jurídica reescritos; os casos de
  teste com o gabarito do advogado; a primeira habilidade própria pela peca-vira-habilidade; e
  as rotinas próprias do jurídico viradas habilidade, testadas e empacotadas. Use quando o advogado disser
  "adapta o plugin ao meu escritório", "as peças não saem com a nossa cara", "quero o nosso
  timbre", "testa com as nossas peças", "transforma essa rotina em habilidade". Não use para
  preencher a ficha (use /motor-juridico:ficha) nem para transformar uma peça em habilidade sem
  adaptar o resto (use peca-vira-habilidade).
---

# Adaptar o jurídico ao escritório

> O plugin chega com o método pronto e o conteúdo vazio. Esta habilidade faz ele produzir como o escritório produz: as peças dele, o papel dele, o jeito dele de escrever, os casos dele, sempre a partir do que o advogado confirma.

Camadas de adaptação: `../../docs/adaptar-ao-escritorio.md`. Regras comuns: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Produção: `../../docs/producao.md`. Onde gravar: `../../docs/pasta.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

Um escritório de previdenciário instala o plugin. A primeira minuta sai em fonte que ninguém usa ali, sem o timbre, com os pedidos em parágrafo corrido e "o requerente" onde o escritório sempre escreve "o autor". A conferência não procura o erro que a advogada mais pega na revisão (o número do benefício trocado). Nada disso é erro do método: falta o escritório.

**Regras fixas desta habilidade:**
1. **Do escritório, não da internet.** Nicho, peças, padrão e casos de teste saem da entrevista com o advogado e do material dele (peças boas, mensagens, decisões) anonimizado. O plugin não traz perfil pronto por área nem tese por matéria. O que a habilidade sugerir vai marcado "sugestão" e só entra com o ok.
2. **Só com o ok.** Cada mudança aparece marcada `[ALTERADO]` ou `[NOVO]`, e nada é gravado sem o advogado aprovar.
3. **Adaptar não afrouxa as regras.** Citação marcada até a conferência, tese e aprovação do advogado, mínimo de dados e treino fora do registro valem para qualquer escritório. Pedido de adaptação que contraria isso não entra, e a habilidade explica por quê.
4. **Sem conteúdo de área inventado.** Requisito de peça, prazo, competência e valor de alçada que aparecerem na adaptação ficam `[CONFERIR]`. Frequência de caso é estimativa do advogado, marcada assim.
5. **Habilidade nova só sai testada.** Três casos passando e o script de empacotamento sem erro; antes disso, não há .zip.

## 1. Quando usar

**Use quando:**
- O escritório acabou de instalar o plugin e quer que as peças saiam com a cara dele.
- O escritório abriu uma área, entrou num nicho novo ou trocou o papel timbrado.
- Os aprendizados jurídicos passaram de 30 linhas `em uso`, ou chegou a revisão trimestral.
- O advogado quer testar as habilidades com as peças e os casos dele, e não só com os fictícios.
- Existe uma rotina da produção jurídica que o escritório faz sempre do mesmo jeito e nenhuma habilidade cobre.

**Não use quando:**
- O pedido é preencher campos da ficha (quem assina, sistemas, validade): `/motor-juridico:ficha`.
- O pedido é só transformar uma peça em habilidade: `peca-vira-habilidade` direto.
- O pedido é adaptar a triagem, as mensagens ou a jornada do cliente: `adaptar-comercial` do motor-comercial ou `adaptar-experiencia` do motor-experiencia (se instalados). O `nicho.md` é o mesmo arquivo.
- A rotina é grande, envolve vários setores e precisa de POP e medição: `pop-para-skill` do `inicio-automacao` (se instalado). Esta habilidade faz o caminho curto.

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`, `nicho.md` (se existir), `aprendizados-juridico.md` e `rotinas-do-escritorio.md` (se existir).
2. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "Em que áreas vocês atuam?" e "Quais são as peças que mais saem do escritório?".
3. **Veja o que está instalado:** as pastas de habilidade do plugin (no Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/`) e `escritorio/04-base/habilidades-do-escritorio/`. A lista define quem é chamado no modo "adaptar".
4. **Conta.** Peça, decisão ou mensagem real, mesmo anonimizada, só em conta profissional ou de equipe. Em conta pessoal, a entrevista segue sem material real, e os testes usam só os casos fictícios.
5. **Se o `nicho.md` já existe** (escrito pela `adaptar-comercial` ou pela `adaptar-experiencia`), ele é comum aos plugins: atualize, nunca reescreva do zero, e não apague o que a outra habilidade escreveu sem perguntar.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` · J: `pecas_mais_feitas`, `onde_estao_os_modelos` |
| Melhora | E: `nicho`, `rotinas_proprias` · J: `estilo`, `timbre` · também: `fonte_e_corpo`, `citacao_em_recuo`, `pedidos`, `pecas_em_massa`, `tribunais_principais` |

Campo vazio: pergunte aquele campo, uma vez, e ofereça gravar. O que a entrevista responder que é fato da ficha (as peças mais feitas, onde estão os modelos, a fonte) volta para a ficha, com o ok e a linha no histórico.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Completo | Primeira adaptação | Partes A a G, na ordem, uma de cada vez, com pausa entre elas |
| Rápido | O advogado tem pouco tempo | Quatro perguntas (abaixo) e o padrão visual; o resto fica para depois |
| Uma parte | "Só o timbre", "só os casos de teste", "só essa rotina" | A parte pedida |
| De novo | Nicho novo, área nova, revisão trimestral | As partes que mudaram, com `[ALTERADO]` |

Comece dizendo: "Vou adaptar o plugin com o que vocês já praticam. O que não tiver resposta fica para preencher, e eu não invento nada." Pergunte por onde começar e sugira A, C e F: é onde a peça muda de cara mais rápido.

**Modo rápido** (no máximo quatro perguntas): "Quais são as três peças que mais saem do escritório?" · "Onde estão as peças boas de vocês?" · "Pode me passar uma peça boa em .docx, para eu ler a formatação?" · "Qual dessas peças vocês querem que vire a primeira habilidade própria?". O resto fica `[A PREENCHER]` e o fechamento diz o que falta.

### Parte A. As áreas e as peças
A1. Para cada área da ficha, pergunte: "Quais peças mais saem nesta área? Quantas por mês, mais ou menos?" (estimativa, marcada assim).
A2. Para cada peça: "Vocês têm peças boas dessa, que usariam de modelo? Onde?" e "Ela sai em lote, para muitos clientes iguais?"
A3. Monte e mostre a tabela da seção 4. Grave na ficha jurídica, com o ok: `pecas_mais_feitas`, `onde_estao_os_modelos`, `pecas_em_massa`, `tamanho_preferido`.
A4. Diga qual peça é a melhor candidata à primeira habilidade própria: a que mais sai, tem três peças boas e sai sempre do mesmo jeito.

### Parte B. O nicho
Siga o formato de `nicho.md` em `../../docs/adaptar-ao-escritorio.md`. O plugin não traz perfil pronto: tudo sai da entrevista e do material do escritório. Para o jurídico, as seções que mais pesam são "Os casos que chegam", "Documentos típicos" e "Cuidados do nicho". Pergunte, uma de cada vez, só o que o `nicho.md` ainda não tiver:
1. "Que tipo de caso chega mais, nas palavras do cliente?"
2. "Que documentos esse cliente costuma ter, e quais quase nunca tem?"
3. "Que erro de documento ou de dado aparece sempre nesses casos?" (vira item de conferência)
4. "Que cuidado esse público pede numa peça?" (dado de saúde, criança, renda)
Grave com o ok, marcando cada linha nova `[NOVO]` e a origem ("entrevista", "visto em peça"). Prazo de fase e requisito de peça ficam `[CONFERIR]`.

### Parte C. O padrão visual
C1. Pergunte: "Pode me passar uma ou duas peças boas em .docx? Eu leio só a formatação, não o texto."
C2. Rode, com o caminho da pasta desta habilidade:
```
python3 "<pasta desta habilidade>/scripts/padrao_do_docx.py" "escritorio/04-base/juridico/modelos/<peca>/<peca-boa>.docx" --saida "escritorio/07-operacao/juridico/padrao-proposto.md"
```
O script abre o .docx só com a biblioteca padrão e propõe: fonte e corpo mais usados, espaçamento, alinhamento, recuo da primeira linha, margens, a citação em recuo (recuo, corpo, espaçamento) e se há cabeçalho ou rodapé (sinal de timbre). O que não achou, ou achou com dúvida, sai `[A CONFIRMAR]`. Com duas peças que discordam, avisa.
C3. Confirme com o advogado, linha a linha, e pergunte a seção 2 do padrão (títulos, numeração, pedidos, documentos, fecho, assinatura, o que nunca aparece), uma pergunta por vez.
C4. Timbre: se a peça tem cabeçalho ou rodapé, peça uma cópia do papel timbrado sem texto e grave como `escritorio/04-base/juridico/timbre.docx`; no padrão, `timbre: timbre.docx`.
C5. Grave `escritorio/04-base/juridico/padrao-visual.md` no formato de `assets/modelo-padrao-visual.md`, com o ok. As chaves da seção 1 têm esses nomes exatos porque o script de .docx da `minutar-peca` lê assim. Atualize `fonte_e_corpo`, `citacao_em_recuo` e `timbre` na ficha jurídica.
C6. Teste: gere o .docx da minuta de treino da `minutar-peca` (se instalada) com `--forcar` e o padrão novo, em `_treino/`, e pergunte: "Saiu com a cara de vocês?".

### Parte D. Os materiais de cada habilidade
D1. Monte a tabela da seção 5 só com as habilidades instaladas e mostre: "Estas habilidades têm materiais que mudam com o escritório. Quer adaptar todas, ou começar por alguma?" Sugira começar pela `conferir-peca` (os erros que a revisão pega) e pela `minutar-peca` (a estrutura das peças).
D2. Chame cada uma no modo "adaptar", uma de cada vez. Cada uma lê as fichas, o `nicho.md` e o padrão, e devolve o que mudou com `[ALTERADO]` e `[NOVO]`. Habilidade sem modo "adaptar": diga em uma linha e siga.
D3. Mostre o que mudou, no formato da seção 6. O advogado aprova item por item; a habilidade chamada grava só o que teve ok.

### Parte E. Os casos de teste do escritório
E1. Peça de 3 a 6 casos reais anonimizados: uma minuta que voltou com erro, um lote de documentos de um caso típico, uma pesquisa do Jus IA que virou peça, um caso que deveria ter parado.
E2. Para cada um, pergunte: "O que a habilidade não pode deixar passar de jeito nenhum neste caso?". A habilidade pode sugerir, marcado "sugestão"; grava só o que o advogado confirmar, com a data.
E3. Grave em `escritorio/04-base/casos-de-teste/juridico/casos.md`, no formato de `assets/modelo-casos-de-teste.md`.
E4. Rode as habilidades nos casos, sem mostrar o gabarito, gravando em `_treino/`. Compare com "Não pode falhar". Erro: falta campo da ficha, linha do nicho, item de conferência ou aprendizado. Proponha o ajuste e rode de novo.

### Parte F. A primeira habilidade própria
F1. Com a peça escolhida em A4, chame a `peca-vira-habilidade` (se instalada), modo "adaptar". Ela pede as 3 a 5 peças boas, monta o mapa, gera a habilidade, testa nos três casos e empacota.
F2. Receba o resultado: o caminho da habilidade, os três testes e o .zip, ou o motivo de não ter saído. Mostre e diga o próximo passo (instalar; se a peça sai em lote, a `pecas-em-lote`).
F3. Sem a `peca-vira-habilidade`: diga que a primeira habilidade própria depende dela e, enquanto isso, grave a estrutura da peça pela `minutar-peca`, modo adaptar.

### Parte G. Rotina própria do jurídico vira habilidade
Para o que o escritório faz sempre do mesmo jeito e não é uma peça (a ordem dos documentos, a revisão de sexta das minutas paradas).
G1. A entrevista, uma pergunta por vez: "O que dispara essa rotina?" · "O que se faz, passo a passo?" · "Com que material?" · "Quem faz cada passo e quem aprova?" · "O que nunca pode acontecer?" · "Quando a rotina tem de parar e chamar o advogado?" · "Como alguém do escritório pede isso, com as palavras de vocês?"
G2. Escreva a rotina em `escritorio/04-base/comum/rotinas-do-escritorio.md`, com S, A e H em cada passo (`../../docs/regras.md`, seção 5.1). Escolher tese, aprovar, assinar e protocolar ficam sempre H.
G3. Gere a habilidade em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`, pelo `assets/modelo-rotina-juridica.md`. Mostre inteira e grave com o ok.
G4. Teste com três casos (o comum, o com exceção, o que deve parar), em `_treino/`, e registre em `escritorio/04-base/casos-de-teste/juridico/<nome>-testes.md`, no formato de `assets/modelo-registro-dos-testes.md`.
G5. Empacote, da pasta de trabalho:
```
python3 "<pasta desta habilidade>/scripts/empacotar_habilidade.py" "escritorio/04-base/habilidades-do-escritorio/<nome>" --testes "escritorio/04-base/casos-de-teste/juridico/<nome>-testes.md"
```
O script confere nomes de arquivo (`[a-z0-9._-]`, caminho até 100 caracteres), o frontmatter, a seção de campos, o passo "Aprender", travessões, arquivos citados, citação com número sem a marca `[CONFERIR]` e os três testes (comum, com exceção, deve parar), cada um com "O que saiu" preenchido, "Resultado: passou" e o "Conferido por". Com erro, sai com código 1 e não gera nada. Sem erro, grava `escritorio/04-base/habilidades-do-escritorio/<nome>.zip`. Habilidade de peça não passa por aqui: vai pela `peca-vira-habilidade`, cujo script confere também o mapa.
G6. Instalar e ligar: Personalizar > Habilidades > Enviar, com o .zip (conferir na configuração da conta). Se o agente do ciclo estiver em uso, ofereça marcar a rotina como "no ciclo: sim" em `rotinas-do-escritorio.md` e, com o ok, acrescentar uma linha ao bloco "Jurídico" de `escritorio/CLAUDE.md` e ao texto da tarefa agendada da `rotina-juridica` (se instalada): "Depois do ciclo, rode a habilidade <nome>".

### Passo final. Aprender
Pergunte: "Alguma coisa na adaptação você faria diferente?". Cada correção vira regra curta e, com o ok, entra em `aprendizados-juridico.md`. Regra que vale para todos os plugins (uma palavra que o escritório nunca usa) vai para a ficha do escritório. Proponha quando adaptar de novo (seção 7).

## 4. A tabela das peças (parte A)

```
PEÇAS DO ESCRITÓRIO · AAAA-MM-DD
| Área | Peça | Por mês (estimativa) | Peças boas (onde) | Em lote? | Habilidade própria |
|---|---|---|---|---|---|
| previdenciario | peticao-inicial-restabelecimento | 12 | 4 (Drive > Modelos > Prev) | sim | a criar (candidata 1) |
| previdenciario | recurso-inominado | 3 | 1 | não | ainda não: só 1 peça boa |
```

O nome da peça vai em minúsculas com hífen: é o mesmo da coluna `peca` do `pecas.csv` e o nome da habilidade própria.

## 5. O que cada habilidade jurídica costuma reescrever no modo "adaptar"

| Habilidade | O que costuma mudar com o escritório | Onde fica |
|---|---|---|
| `conferir-peca` | Os erros que a revisão do escritório mais pega; o padrão de pedidos e de nomes de arquivo | Checklist da habilidade e J: `estilo`, `pedidos` |
| `conferir-citacoes` | As fontes oficiais dos tribunais onde o escritório atua | J: `tribunais_principais` |
| `minutar-peca` | A estrutura de cada peça mais feita | `04-base/juridico/modelos/<peca>/estrutura.md` |
| `peca-vira-habilidade` | A primeira habilidade própria | `04-base/habilidades-do-escritorio/<peca>/` |
| `trazer-pesquisa` | Os temas da base por área | `04-base/juridico/jurisprudencia/` |
| `dossie-do-caso` | Documentos típicos e lacunas por tipo de caso do nicho | `nicho.md` e a habilidade |
| `estrategia-do-caso` | Os caminhos que o escritório costuma considerar, sem percentual | A habilidade, com `[CONFERIR]` no que for requisito |
| `rotina-juridica` | Horários e o que entra no resumo do dia | A tarefa agendada e o modelo do resumo |
| `banco-de-teses-vivo` | As teses a escrever e o nome padrão dos órgãos | `04-base/juridico/teses/` e J: `tribunais_principais` |
| `preparar-protocolo` | Sistemas, nomes de arquivo, ordem dos documentos | J: `sistemas`, `nome_dos_arquivos` |
| `pecas-em-lote` | As colunas da planilha no vocabulário da equipe | `04-base/juridico/modelos/<peca>/planilha-do-lote.csv` |
| `advogado-do-diabo` | As respostas típicas da parte contrária no nicho | A habilidade |
| `monitor-de-precedentes` | Os temas vigiados | A habilidade e a base |

Mostre só as linhas das habilidades instaladas. O que cada uma faz de fato no modo "adaptar" está no SKILL.md dela.

## 6. Formato da saída

**O que mudou, por habilidade (parte D):**

```
ADAPTAÇÃO · [habilidade] · AAAA-MM-DD
| Material | O que mudou | Antes | Depois | Decisão |
|---|---|---|---|---|
| checklist da conferir-peca | [NOVO] número do benefício conferido contra a carta | (não havia) | "número do benefício igual ao da carta de cessação" | sim |
```

**Fechamento da adaptação:** o que foi gravado (com caminho e versão), o que ficou `[A PREENCHER]`, o resultado dos testes, a primeira habilidade própria (instalada ou o que falta) e a data sugerida para adaptar de novo.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Peças e modelos na ficha | `escritorio/04-base/comum/ficha-juridica.md`, com linha no histórico |
| Perfil do nicho | `escritorio/04-base/comum/nicho.md` (comum aos plugins motor) |
| Proposta do padrão visual (rascunho do script) | `escritorio/07-operacao/juridico/padrao-proposto.md` |
| Padrão visual | `escritorio/04-base/juridico/padrao-visual.md` e `timbre.docx`, se houver |
| Materiais adaptados | Nos caminhos de cada habilidade (seção 5), gravados por ela com o ok |
| Casos de teste do escritório | `escritorio/04-base/casos-de-teste/juridico/casos.md` |
| Primeira habilidade própria | `escritorio/04-base/habilidades-do-escritorio/<peca>/` e o `.zip`, pela `peca-vira-habilidade` |
| Rotinas próprias | `escritorio/04-base/comum/rotinas-do-escritorio.md` |
| Habilidade de rotina e o pacote | `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md` e `<nome>.zip` |
| Testes das habilidades novas | `escritorio/04-base/casos-de-teste/juridico/<nome>-testes.md` |
| Testes em lote | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

**Quando adaptar de novo:** área nova, nicho novo ou papel timbrado novo; os aprendizados passaram de 30 linhas `em uso`; a revisão trimestral. Sem pasta aberta: o perfil, o padrão e as habilidades novas saem no chat, em blocos, com o caminho de cada um; o padrão lido do .docx e o .zip só existem com pasta aberta e os scripts.

## 8. Solo e equipe

**Solo:** a adaptação completa leva uma tarde; o modo rápido, meia hora. Comece pelo padrão visual e pela primeira habilidade própria, que é onde o tempo volta mais rápido. **Equipe:** quem faz a primeira minuta participa da parte A e da parte E: é quem conhece o erro que volta da revisão. O advogado escreve o gabarito dos casos de teste. Uma pessoa é dona do padrão visual e das habilidades do escritório, e só ela gera versão nova e o .zip.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Perfil de nicho ou tese tirados da internet | Peça com conteúdo que o escritório não conferiu | Regra fixa 1: entrevista e material do escritório |
| Padrão visual de memória ("acho que é Arial 12") | Peça fora do padrão em toda minuta | O script lê a peça boa e o advogado confirma |
| Timbre colado à mão em cada .docx | Peça sem timbre ou com timbre antigo | `timbre.docx` no padrão, usado pelo script da `minutar-peca` |
| Teste só com casos fictícios | O primeiro erro difícil aparece num caso real | Casos do escritório com gabarito do advogado |
| Habilidade do escritório que não instala | Nome com acento, frontmatter errado, arquivo esquecido | Script que valida antes de gerar o .zip |
| Registro de teste copiado do modelo sem rodar | Habilidade empacotada que nunca foi testada | O script recusa o modelo cru e o "Conferido por" vazio |
| Rotina que nunca parou num teste | A rotina segue quando devia chamar o advogado | Caso "deve parar" obrigatório |
| Dois perfis de nicho, um por plugin | Cada plugin fala de um jeito | Um `nicho.md` comum, atualizado e nunca reescrito |

## 10. Próximo passo

- Padrão gravado: a `minutar-peca` passa a gerar o .docx com ele.
- Primeira habilidade própria instalada: as próximas peças desse tipo saem por ela; em lote, `pecas-em-lote` (se instalada).
- Teses que o escritório usa e não escreveu: `banco-de-teses-vivo` (se instalada).
- Ciclo diário: `rotina-juridica` e `/motor-juridico:ciclo`.
- Rotina grande, com vários setores: `pop-para-skill` do `inicio-automacao` (se instalado); sem ele, quebre a rotina em partes pequenas e use a parte G para cada uma.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

- `assets/modelo-padrao-visual.md`: o formato do padrão visual, com as chaves que o script de .docx lê e um exemplo preenchido. Leia na parte C.
- `assets/modelo-casos-de-teste.md`: o formato dos casos de teste do escritório, com exemplo. Leia na parte E.
- `assets/modelo-rotina-juridica.md`: o esqueleto da habilidade de rotina e um exemplo preenchido. Leia no passo G3.
- `assets/modelo-registro-dos-testes.md`: o formato do registro dos três testes, que os scripts conferem. Leia no passo G4.
- `scripts/padrao_do_docx.py`: lê a formatação de uma peça boa em .docx e propõe o padrão. Rode no passo C2.
- `scripts/empacotar_habilidade.py`: confere e empacota a habilidade de rotina. Rode no passo G5.
