---
name: adaptar-comercial
description: >
  Adapta o motor-comercial ao escritório em quatro camadas: monta ou atualiza o perfil do nicho
  (nicho.md) por entrevista, uma pergunta por vez, com mensagens reais anonimizadas como fonte e
  nada da internet, revendo o tratamento e o tom para o público; chama cada habilidade comercial
  instalada no modo adaptar e mostra o que mudou; monta os casos de teste do escritório com o
  gabarito do advogado; e transforma uma rotina própria do comercial em habilidade nova, testada
  em três casos e empacotada em .zip. Use quando o advogado disser
  "adapta o plugin ao meu escritório", "meu público é rural", "as mensagens não soam como a gente",
  "quero testar com as minhas mensagens", "transforma essa rotina em habilidade". Não use para
  preencher a ficha (use /motor-comercial:ficha) nem para a experiência do cliente (use
  adaptar-experiencia do motor-experiencia).
---

# Adaptar o comercial ao escritório

> O plugin chega com o método pronto e o conteúdo genérico. Esta habilidade faz o plugin falar com o cliente do escritório: o vocabulário, as perguntas, as aflições e as rotinas dele, sempre a partir do que o advogado confirma.

Camadas de adaptação: `../../docs/adaptar-ao-escritorio.md`. Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-comercial.md`. Onde gravar: `../../docs/pasta.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

Um escritório de previdenciário rural instala o plugin. O convite para a consulta fala em "benefício por incapacidade", e o cliente escreve "tô encostado". O roteiro pede "extrato de contribuições", e a cliente de 62 anos tem notas de produtor e a certidão de casamento com "lavradora" anotado. A triagem não reconhece "o INSS falou que faltou prova" como urgência. Nada disso é erro do método: falta o nicho.

**Regras fixas desta habilidade:**
1. **Do escritório, não da internet.** O nicho sai da entrevista com o advogado e de mensagens reais anonimizadas. O plugin não traz perfil pronto por área: nicho é amplo, e cada escritório descreve o seu. O que a habilidade sugerir a partir das mensagens vai marcado "sugestão" e só entra com o ok. Nada vem de pesquisa na internet.
2. **Só com o ok.** Cada mudança aparece marcada `[ALTERADO]` ou `[NOVO]`, e nada é gravado sem o advogado aprovar.
3. **Sem estatística e sem promessa.** Frequência é estimativa do advogado, marcada assim. Prazo de fase fica `[CONFERIR]` e nunca vai para mensagem ao cliente.
4. **Adaptar não afrouxa as regras.** Ética, linha vermelha, dados e "nada sai sem uma pessoa" valem igual para qualquer nicho. Pedido de adaptação que contraria isso não entra, e a habilidade explica por quê.
5. **Habilidade nova só sai testada.** Três casos passando e o script de empacotamento sem erro; antes disso, não há .zip.

## 1. Quando usar

**Use quando:**
- O escritório acabou de instalar o plugin e quer que ele fale com o seu público.
- O escritório entrou num nicho novo, mudou de público ou abriu uma área.
- Os aprendizados comerciais passaram de 30 linhas `em uso`, ou chegou a revisão trimestral.
- O advogado quer testar as habilidades com as mensagens dele, e não só com as fictícias.
- Existe uma rotina do comercial que o escritório faz sempre do mesmo jeito e que nenhuma habilidade cobre.

**Não use quando:**
- O pedido é preencher campos da ficha (horário, valores, prazos): use `/motor-comercial:ficha`.
- O pedido é adaptar a jornada, a régua de atualização ou as mensagens do cliente ativo: use `adaptar-experiencia` do motor-experiencia (se instalado). O `nicho.md` é o mesmo arquivo.
- A rotina é grande, envolve vários setores e precisa de POP, versão e medição: use `pop-para-skill` do `inicio-automacao` (se instalado). Esta habilidade faz o caminho curto, para rotinas pequenas.

## 2. Antes de começar

1. **Leia as fichas e o que já foi ensinado:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir), `aprendizados-comercial.md` e `rotinas-do-escritorio.md` (se existir).
2. **Sem ficha:** ofereça `/motor-comercial:comecar`. Para seguir, pergunte só: "Em que áreas vocês atuam?" e "Como você descreveria o cliente típico de vocês?".
3. **Veja o que está instalado:** as pastas de habilidade do plugin (no Claude Code, `${CLAUDE_PLUGIN_ROOT}/skills/`). A lista define quem é chamado no modo "adaptar".
4. **Conta.** Mensagem real, mesmo anonimizada, só em conta profissional ou de equipe. Em conta pessoal, a entrevista segue sem mensagens reais, e os casos de teste usam só os fictícios.
5. **Se o `nicho.md` já existe e foi escrito pela `adaptar-experiencia`,** ele é comum aos dois plugins: atualize, nunca reescreva do zero, e não apague o que a outra habilidade escreveu sem perguntar.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `nicho`, `areas`, `cliente_tipico`.
- **Melhora:** E: `como_o_cliente_fala`, `sazonalidade`, `rotinas_proprias`.

Campo vazio: pergunte aquele campo, uma vez, e ofereça gravar. As respostas da entrevista que são fatos da ficha (o nicho em uma frase, o cliente típico) voltam para a ficha do escritório, com o ok e a linha no histórico.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| Completo | Primeira adaptação | Partes A, B, C e, se houver rotina, D | `nicho.md`, materiais adaptados, casos de teste, habilidade nova |
| Rápido | "Só o básico", até 4 perguntas | 4 perguntas da entrevista, e as mensagens reais se o advogado tiver | `nicho.md` versão 0.1, marcado "rápido, completar na entrevista" |
| Só nicho | Atualizar o perfil | Parte A | `nicho.md` com `[ALTERADO]` |
| Só materiais | O nicho já existe | Parte B | Materiais reescritos, um por habilidade |
| Casos de teste | O advogado quer testar com as mensagens dele | Parte C | `04-base/casos-de-teste/comercial/casos.md` |
| Rotina nova | Uma rotina própria do comercial | Parte D | Habilidade nova em `04-base/habilidades-do-escritorio/` e o .zip |

**Modo direto:** "adapta o plugin para trabalhista patronal, aqui estão 8 mensagens". Execute a parte A com o que o advogado disse e com as mensagens, mostre e pergunte só o que falta.

### Parte A. O perfil do nicho (`nicho.md`)

**A1. O recorte.** Pergunte: "Em uma frase, qual é o recorte de vocês? Por exemplo: previdenciário rural no interior, trabalhista patronal para comércio, família com foco em mulheres em divórcio." Comece sempre do formato vazio de `../../docs/adaptar-ao-escritorio.md`, com o que a ficha do escritório já diz (`nicho`, `cliente_tipico`, `como_o_cliente_fala`, `casos_mais_comuns`). Diga: "O plugin não traz perfil pronto por área, porque cada escritório tem o seu público. Vamos montar o de vocês a partir da conversa e das mensagens que chegam."

**A2. As mensagens reais.** Peça: "Você consegue me mandar de 5 a 10 mensagens reais de quem procurou o escritório, anonimizadas? As que mais chegam e uma que te deu trabalho." Anonimize o que chegar sem anonimizar e avise. As mensagens são a prova: cada linha do perfil que elas confirmam ganha "(visto em mensagem)".

**A3. A entrevista, uma pergunta por vez**, na ordem das seções do formato de `../../docs/adaptar-ao-escritorio.md`:
1. "Quem é o cliente que mais chega? Idade, região, como ele chega até vocês, o que já tentou antes."
2. "Que palavras ele usa que um advogado não usaria?" (mostre as que apareceram nas mensagens, marcadas "sugestão")
3. "Quais são os tipos de caso que mais chegam? E qual você acha que é o mais comum, numa estimativa?"
4. "O que ele quer ouvir na primeira conversa, e o que ele precisa entender que ainda não sabe?"
5. "Quais são as perguntas que mais chegam, do jeito que chegam?"
6. "Em que momento ele costuma se desesperar?"
7. "Que papéis ele costuma ter, e onde consegue os que faltam?"
8. "Tem mês cheio e mês vazio?"
9. "Que cuidado esse público pede? O que vocês nunca dizem para ele?"
10. "Para esse público, o tratamento da ficha continua certo? E o tom de três palavras combina com quem escreve para vocês?" (leia antes, em voz alta, o que a ficha diz em `tratamento` e `tom_em_tres_palavras`) Mostre a abertura do convite nos três tratamentos (você, senhor e senhora, pelo nome) e deixe o advogado escolher. Pergunte também se muda conforme a pessoa ("idosos por senhor e senhora, o resto por você"): a regra vai para "Cuidados do nicho" e para os aprendizados.
11. "O que ele costuma pesquisar sozinho, num vídeo ou numa IA, e qual o erro mais comum que traz?"

Aceite "não sei": a seção fica `[A PREENCHER]`. Resposta vaga: peça a cena concreta ("e a última mensagem desse tipo, o que dizia?").

**A4. Montar o perfil.** No formato de `../../docs/adaptar-ao-escritorio.md`, com cada linha marcada pela origem: "(entrevista)", "(visto em mensagem)" ou "(sugestão, confirmada)". Sugestão que o advogado não confirmou não entra. O tratamento e o tom escolhidos na pergunta 10 entram em "Quem é o cliente" (como ele prefere ser tratado) e, se mudaram, em "Cuidados do nicho".

**A5. Mostrar e gravar.** Mostre o perfil inteiro. Com o ok, grave em `escritorio/04-base/comum/nicho.md`. Perfil existente: só as seções que mudaram, com `[ALTERADO]` ou `[NOVO]`, versão nova e `revisado_em`. Ofereça levar à ficha do escritório o que é fato da ficha (`nicho`, `cliente_tipico`, `como_o_cliente_fala`, `sazonalidade`, e `tratamento` e `tom_em_tres_palavras` se a pergunta 10 mudou alguma coisa), com linha no histórico. Tratamento ou tom novo muda todas as mensagens: avise que a parte B vai reescrever a biblioteca com ele.

**Modo rápido.** Só as perguntas 1, 2, 6 e 10 (tratamento e tom), com as mensagens reais na mesa, se houver. O resto fica `[A PREENCHER]` e o perfil sai com "rápido, completar na entrevista".

### Parte B. Os materiais reescritos para o nicho

**B1. A lista.** Monte a tabela da seção 5 só com as habilidades instaladas e mostre: "Estas habilidades têm materiais que mudam com o nicho. Quer adaptar todas, ou começar por alguma?" Sugira começar pelas que falam com o cliente: `mensagens-comerciais`, `roteiro-da-consulta`, `qualificar-contato`.

**B2. Chamar cada uma no modo "adaptar".** Uma de cada vez, na ordem combinada. Cada habilidade lê o `nicho.md`, reescreve os materiais dela e devolve a lista do que mudou, com `[ALTERADO]` e `[NOVO]`. Habilidade instalada sem modo "adaptar": diga em uma linha e siga para a próxima.

**B3. Mostrar o que mudou.** Depois de cada habilidade, a tabela da seção 6: material, o que mudou, um exemplo antes e depois. O advogado aprova item por item; a habilidade chamada grava só o que teve ok.

**B4. Testar.** Ao fim, rode a `triar-contato` em lote com os casos de teste (parte C) ou com os fictícios, gravando em `escritorio/07-operacao/_treino/comercial/`. Se o assistente de primeira resposta estiver ligado, ele roda de novo os casos P e E antes de qualquer uso.

### Parte C. Os casos de teste do escritório

**C1. As mensagens.** Peça de 8 a 12 mensagens reais anonimizadas: as que mais chegam e as que dão medo (pessoa agora, fora da área urgente, vulnerável, preço, resposta de IA, pedido de parar, cliente ativo no canal do comercial).

**C2. O gabarito do advogado.** Para cada uma, pergunte: "Como você classificaria esta? Tipo, área, urgência, caminho, e o que não pode falhar de jeito nenhum." A habilidade pode sugerir, marcada "sugestão"; grava só o que ele confirmar ou escrever, com a data.

**C3. Gravar** em `escritorio/04-base/casos-de-teste/comercial/casos.md`, no formato de `assets/modelo-casos-de-teste.md`.

**C4. Rodar.** Rode a `triar-contato` no lote, sem mostrar o gabarito, gravando em `_treino`. Compare com "Não pode falhar". Erro: falta palavra de alerta, campo da ficha, linha do nicho ou um aprendizado. Proponha o ajuste e rode de novo.

### Parte D. Rotina própria vira habilidade

**D1. A entrevista**, uma pergunta por vez: "O que dispara essa rotina? Dia, hora, ou o que acontece antes." · "O que se faz, passo a passo?" · "Com que material: mensagem, lista, ligação?" · "Quem faz cada passo e quem aprova?" · "O que nunca pode acontecer?" · "Quando a rotina tem de parar e chamar alguém?" · "Como alguém do escritório pede isso, com as palavras de vocês?"

**D2. Escrever a rotina** em `escritorio/04-base/comum/rotinas-do-escritorio.md`, com S, A e H em cada passo (`../../docs/regras.md`, seção 5.1). O que é de pessoa fica H, e a habilidade só prepara o material em volta.

**D3. Gerar a habilidade** em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`, pelo `assets/modelo-habilidade-do-escritorio.md`: frontmatter só com `name` (igual à pasta, minúsculas e hífen) e `description`; regras fixas; quando usar; antes de começar com "Campos da ficha que esta habilidade usa"; fluxo com S, A e H e o passo "Aprender" por último; o que entrega e onde grava; solo e equipe; erros que evita; próximo passo. Mostre inteira e grave com o ok.

**D4. Testar com três casos:** o comum, o com exceção e o que deve parar. Rode a habilidade com cada um (em `_treino`, se for caso fictício), copie o que saiu sem corrigir e registre em `escritorio/04-base/casos-de-teste/comercial/<nome>-testes.md`, no formato de `assets/modelo-registro-dos-testes.md`. Falhou: ajuste a habilidade e rode os três de novo.

**D5. Empacotar.** Da pasta de trabalho, com `<PASTA DA HABILIDADE>` sendo a pasta deste SKILL.md (no Claude Code com o plugin: `${CLAUDE_PLUGIN_ROOT}/skills/adaptar-comercial`):
```
python3 "<PASTA DA HABILIDADE>/scripts/empacotar_habilidade.py" \
  escritorio/04-base/habilidades-do-escritorio/<nome> \
  --testes escritorio/04-base/casos-de-teste/comercial/<nome>-testes.md
```
O script confere nomes de arquivo (`[a-z0-9._-]`, caminho até 100 caracteres), o frontmatter, a seção de campos, o passo "Aprender", travessões, arquivos citados e os três testes, cada um com "O que saiu" preenchido e "Resultado: passou". A linha do modelo cru ("Resultado: passou | falhou") não conta como passou: o caso precisa ter rodado e alguém escolhido uma das duas. Com erro, sai com código 1 e a lista do que corrigir, e não gera nada. Sem erro, grava `escritorio/04-base/habilidades-do-escritorio/<nome>.zip`.

**D6. Instalar e ligar.** Instalação: Personalizar > Habilidades > Enviar, com o .zip (conferir na configuração da conta). Se o agente do ciclo estiver em uso, ofereça: marcar a rotina como "no ciclo: sim" em `rotinas-do-escritorio.md` e acrescentar, com o ok, uma linha ao bloco "Comercial" de `escritorio/CLAUDE.md` e ao texto da tarefa agendada da `rotina-comercial` (se instalada): "Depois do ciclo, rode a habilidade <nome>". O que ela preparar para cliente vai para a fila de aprovação, como qualquer rascunho.

### Passo final. Aprender

Pergunte: "Alguma coisa no perfil, nos materiais ou na rotina você faria diferente?". Cada correção vira regra curta e, com o ok, entra em `aprendizados-comercial.md`. Regra que vale para os dois plugins (uma palavra que o público nunca deve ouvir) vai para a ficha do escritório. Proponha também quando adaptar de novo (seção 7).

## 4. Sem perfil pronto: de onde vem o nicho

O plugin não traz perfil de nicho por área. Nicho é amplo: dois escritórios de previdenciário podem atender públicos que não se parecem (o segurado rural do interior e o servidor aposentado da capital). Cada escritório descreve o seu, e o mecanismo é sempre o mesmo:

| Fonte | O que dá | Como entra no perfil |
|---|---|---|
| A ficha do escritório | `nicho`, `cliente_tipico`, `como_o_cliente_fala`, `casos_mais_comuns`, `sazonalidade`, `tratamento`, `tom_em_tres_palavras` | Ponto de partida da entrevista, já confirmado |
| A entrevista (A3) | O resto do formato, nas palavras do advogado | "(entrevista)" |
| Mensagens reais anonimizadas (A2) | Vocabulário, perguntas e aflições do jeito que chegam | "(visto em mensagem)" |
| Sugestão da habilidade, tirada das mensagens | Palavras ou padrões que o advogado não citou | "(sugestão, confirmada)", só com o ok |
| Os aprendizados (`aprendizados-comercial.md`) | Correções que já falam do público | Entram na seção que corrigem, com o ok |

Escritório generalista: uma seção "Os casos que chegam" por área, e as outras seções comuns, com a diferença de cada área quando houver (o `painel-do-funil`, se instalado, mostra que área traz mais contatos e por onde começar).

## 5. O que cada habilidade comercial reescreve no modo "adaptar"

| Habilidade | O que costuma mudar com o nicho | Onde fica |
|---|---|---|
| `triar-contato` | Sinais e palavras de alerta do jeito que o cliente escreve; casos mais comuns | E: `palavras_de_alerta`, `casos_mais_comuns` |
| `mensagens-comerciais` | A biblioteca no vocabulário, no tratamento e no tom do público (sem biblioteca ainda, ela cria pelo modo rápido e adapta em seguida) | `04-base/comercial/biblioteca-comercial.md` |
| `roteiro-da-consulta` | Perguntas, documentos e alertas por tipo de caso do nicho | `04-base/atendimento-e-triagem/roteiro-consulta-<area>.md` |
| `qualificar-contato` | Perguntas prévias com as palavras do cliente | Seção "Perguntas prévias" do roteiro da área |
| `ata-da-consulta` | Mensagem de resumo e lacunas típicas do nicho | Biblioteca (`resumo-depois-da-consulta`) e roteiro |
| `proposta-de-honorarios` | O que cada tipo de caso inclui e exclui (nunca valor) | Política de honorários |
| `agenda-da-consulta` | Confirmação e lembrete para o público (horário, canal, quem acompanha) | Biblioteca |
| `follow-up` | Mensagens da régua e momentos do nicho | Régua e biblioteca |
| `objecoes-comerciais` | As objeções que esse público faz | `04-base/comercial/objecoes.md` |
| `contrato-de-honorarios` | Escopo por tipo de caso (nunca valor) | Modelo do contrato |
| `passagem-para-o-caso` | O que o nicho sempre precisa passar ao caso | Modelo da passagem |
| `rotina-comercial` | Horários e cuidados de sazonalidade do resumo | Tarefa e modelo do resumo |
| `painel-do-funil` | Origens, motivos de perda e cuidados de leitura | C: `origem_dos_contatos`, `motivos_de_perda_comuns` |
| `assistente-de-primeira-resposta` | Instruções e casos do nicho na bateria, com novo teste | `05-automacoes/assistente-de-primeira-resposta/` |
| `auditar-conversas-comerciais` | Frases de risco do nicho e grupos da amostra | E: `frases_que_nunca_usamos`, `palavras_de_alerta` |

Mostre só as linhas das habilidades instaladas. O que cada uma faz de fato no modo "adaptar" está no SKILL.md dela.

## 6. Formato da saída

**O que mudou, por habilidade (parte B):**

```
ADAPTAÇÃO · [habilidade] · nicho.md v[N] · AAAA-MM-DD
| Material | O que mudou | Antes | Depois | Decisão |
|---|---|---|---|---|
| roteiro-consulta-previdenciario.md | [ALTERADO] pergunta de tempo rural | "Teve período sem carteira assinada ou na roça?" | "Desde quando você trabalha na roça, e com quem?" | sim |
```

**Fechamento da adaptação:** o que foi gravado (com caminho e versão), o que ficou `[A PREENCHER]`, o resultado do teste em lote e a data sugerida para adaptar de novo.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Perfil do nicho | `escritorio/04-base/comum/nicho.md` (comum aos dois plugins) |
| Fatos que voltam para a ficha | `escritorio/04-base/comum/ficha-do-escritorio.md`, com linha no histórico |
| Materiais adaptados | Nos caminhos de cada habilidade (seção 5), gravados por ela com o ok |
| Casos de teste do escritório | `escritorio/04-base/casos-de-teste/comercial/casos.md` |
| Rotinas próprias | `escritorio/04-base/comum/rotinas-do-escritorio.md` |
| Habilidade nova e o pacote | `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md` e `<nome>.zip` |
| Testes da habilidade nova | `escritorio/04-base/casos-de-teste/comercial/<nome>-testes.md` |
| Testes em lote | `escritorio/07-operacao/_treino/comercial/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-comercial.md` |

**Quando adaptar de novo:** o escritório entrou num nicho novo ou mudou de público; os aprendizados passaram de 30 linhas `em uso`; a revisão trimestral. Sem pasta aberta: o perfil, os materiais e a habilidade nova saem no chat, em blocos, com o caminho de cada um; o .zip só existe com pasta aberta e o script.

## 8. Solo e equipe

**Solo:** a entrevista do nicho leva uns 30 minutos, e o modo rápido, 5. Comece pelo perfil e pelas mensagens, que é onde o cliente sente a diferença. Rotina nova só quando ela se repete toda semana.

**Equipe:** quem atende o primeiro contato participa da entrevista: é quem conhece as palavras do cliente. O advogado escreve o gabarito dos casos de teste. Uma pessoa é dona do `nicho.md` e das habilidades do escritório, e é ela que gera versão nova e o .zip; ninguém edita a cópia instalada.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Nicho copiado da internet | Perfil de outro público, com estatística que ninguém conferiu | Regra fixa 1: entrevista e mensagens reais |
| Sugestão gravada sem conferir | O plugin fala de casos que o escritório nem atende | Cada linha confirmada; a não confirmada não entra |
| Tratamento da ficha que não serve ao público | Idoso tratado por "você" sente falta de respeito; jovem tratado por "senhor" sente distância | Pergunta 10 da entrevista, com a abertura nos três tratamentos |
| Prazo de fase virando promessa | "Sai em 90 dias" numa mensagem | Prazo `[CONFERIR]`, nunca em mensagem |
| Materiais reescritos sem mostrar | O advogado descobre a mudança pelo cliente | `[ALTERADO]` e decisão item por item |
| Teste só com casos fictícios | O primeiro caso difícil é real | Casos do escritório com gabarito do advogado |
| Habilidade do escritório que não instala | Nome com acento, frontmatter errado, arquivo esquecido | Script que valida antes de gerar o .zip |
| Registro de teste copiado do modelo sem rodar | Habilidade empacotada que nunca foi testada | O script recusa "Resultado: passou \| falhou" e "O que saiu" vazio |
| Rotina automatizada que nunca parou num teste | Mensagem para quem pediu para parar | Caso "deve parar" obrigatório |
| Dois perfis de nicho, um por plugin | Cada plugin fala de um jeito | Um `nicho.md` comum, atualizado e nunca reescrito |

## 10. Próximo passo

- Nicho gravado: parte B com as habilidades que falam com o cliente.
- Materiais adaptados: parte C, para ver o efeito com mensagens reais.
- Experiência do cliente no mesmo nicho: `adaptar-experiencia` do motor-experiencia (se instalado), que lê o mesmo `nicho.md`.
- Rotina grande, com vários setores: `pop-para-skill` do `inicio-automacao` (se instalado); sem ele, quebre a rotina em partes pequenas e use a parte D para cada uma.
- Assistente ligado: `assistente-de-primeira-resposta`, novo teste dos casos P e E.

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e siga com o que existe.

## Referências desta habilidade

- `assets/modelo-casos-de-teste.md`: o formato dos casos de teste do escritório, com exemplo. Leia na parte C.
- `assets/modelo-habilidade-do-escritorio.md`: o esqueleto da habilidade nova e um exemplo preenchido. Leia no passo D3.
- `assets/modelo-registro-dos-testes.md`: o formato do registro dos três testes, que o script confere. Leia no passo D4.
- `scripts/empacotar_habilidade.py`: confere e empacota a habilidade nova. Rode no passo D5.
