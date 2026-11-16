---
name: adaptar-experiencia
description: >
  Adapta o suporte ao cliente ao escritório: escreve com o advogado o perfil do nicho
  (como o cliente fala, os momentos de aflição e o que ele pesquisa sozinho), reescreve a
  jornada, as mensagens e o glossário para esse nicho chamando cada habilidade instalada no
  modo adaptar, monta os casos de teste do escritório com gabarito e transforma uma rotina
  própria do suporte (por exemplo, a ligação de boas-vindas no dia seguinte) numa habilidade
  do escritório, testada e empacotada. Use quando o advogado disser "adapta para o meu
  nicho", "meus clientes não falam assim", "quero o plugin com a cara do escritório", "monta os
  casos de teste", "transforma essa rotina em habilidade", "a gente sempre faz assim". Não use
  para preencher a ficha (use o comando /motor-experiencia:ficha) nem para a régua de um tipo
  de caso só (use jornada-do-cliente).
---

# Adaptar a experiência ao escritório

> O plugin chega pronto no método e vazio no conteúdo. Um escritório de BPC no interior e um de trabalhista em capital usam as mesmas habilidades, mas os clientes falam diferente, se afligem em momentos diferentes e chegam com perguntas diferentes que leram na internet. A adaptação ensina isso às habilidades.

Regras comuns do plugin: `../../docs/regras.md`. As camadas de adaptação: `../../docs/adaptar-ao-escritorio.md`. Fichas: `../../docs/ficha-da-experiencia.md`. Onde gravar: `../../docs/pasta.md`. Como guardar correções: `../../docs/aprender-com-o-uso.md`. Casos fictícios: `../../docs/casos-ficticios.md`.

A secretária copia a mensagem de andamento do plugin e manda: "o processo está concluso para despacho". A cliente, aposentada rural, responde com um áudio: "Moça, não entendi nada, a minha aposentadoria saiu ou não?". No escritório dela, ninguém fala "concluso". Fala "o processo está na mão do juiz". Essa troca, multiplicada por cada mensagem, resumo e página, é o que a adaptação faz de uma vez.

**Regras fixas desta habilidade:**
1. O nicho é do escritório, não da internet. O plugin não traz perfil de nicho pronto: nicho é amplo, e cada escritório descreve o seu. O `nicho.md` sai da entrevista e de mensagens reais anonimizadas, e só entra o que o advogado confirmar, com as palavras dos clientes dele.
2. Nenhuma estatística. Frequência é estimativa do advogado, marcada assim. Tempo de fase fica `[CONFERIR]` e nunca vai para o cliente como promessa.
3. Cada material reescrito marca a mudança `[ALTERADO]` e só é gravado com o ok. Linha que o advogado já confirmou não muda sem ser mostrada.
4. Caso de teste e exemplo saem de mensagem real anonimizada. Dado de cliente nunca entra em `04-base/`.
5. Rotina própria vira habilidade só depois de testada com três casos, e com o empacotador conferindo os nomes.

## 1. Quando usar

**Use quando:**
- O escritório acabou de instalar o plugin e quer que ele fale como os clientes dele.
- As mensagens saem certas, mas "com cara de plugin".
- O escritório entrou num nicho novo ou mudou de público.
- Os aprendizados passaram de 30 linhas em uso, ou chegou a revisão trimestral.
- A equipe tem uma rotina de suporte que sempre faz do mesmo jeito e nenhuma habilidade cobre.

**Não use quando:**
- O pedido é preencher campos das fichas: use `/motor-experiencia:ficha`.
- O pedido é a régua de um tipo de caso só: use `jornada-do-cliente`.
- O pedido é traduzir uma palavra nova num caso: use `status-para-o-cliente`, que guarda no glossário.
- O pedido é adaptar o comercial: use `adaptar-comercial` do motor-comercial (se instalado). O `nicho.md` é o mesmo para os dois; esta habilidade completa as seções do suporte.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`) e os aprendizados (`escritorio/04-base/comum/aprendizados-experiencia.md`).
2. **Leia o `nicho.md`** (`escritorio/04-base/comum/nicho.md`), se existir. Ele pode ter sido escrito pela `adaptar-comercial`: não recomece, complete as seções do suporte e marque `[NOVO]`.
3. **Veja o que está instalado:** as pastas de `skills/` do plugin. Só as habilidades instaladas entram no passo dos materiais.
4. **Leia o que já existe na base:** jornadas, glossário do cliente, biblioteca de mensagens, casos de teste, `rotinas-do-escritorio.md`.
5. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se o advogado quiser seguir, pergunte só: "Qual é o recorte de verdade do escritório?" e, depois, "Quem é o cliente típico?".
6. **Dados.** Mensagem real só anonimizada. Em conta pessoal, só os casos fictícios.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `nicho`, `areas`, `cliente_tipico`.
- **Melhora:** E: `como_o_cliente_fala`, `rotinas_proprias`, `sazonalidade`.

Campo que falta e a adaptação pede: pergunte aquele campo, uma vez, e ofereça gravar na ficha do escritório (vale também para o comercial).

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Completo | Primeira adaptação | Nicho, materiais, glossário, casos de teste e a lista de rotinas próprias |
| Só o nicho | O advogado quer começar pelo perfil | `nicho.md` com as seções do suporte |
| Materiais | O nicho já existe | Jornadas, mensagens, glossário e resumo reescritos |
| Casos de teste | Antes de usar com cliente real, ou depois de uma mudança grande | `04-base/casos-de-teste/experiencia/` com gabarito |
| Rotina nova | "A gente sempre faz assim" | Rotina escrita, habilidade própria testada e o .zip |
| Revisar | Aprendizados acima de 30 linhas, ou revisão trimestral | O que muda no nicho e nos materiais, e o que sobe para a ficha |

O modo completo é a sequência: nicho, materiais, casos de teste, rotina nova. Ao fim de cada parte, pergunte se segue agora ou para.

### Parte 1. O nicho (entrevista, uma pergunta por vez)

**Passo 1. O recorte.** Pergunte: "Qual é o recorte de verdade? Não a área, o cliente: quem é, de onde vem, o que já tentou antes de chegar aqui?". Peça a cena concreta: "Me descreve o último cliente que entrou: idade, cidade, como chegou, o que ele já tinha tentado". Não há perfil pronto para escolher: o nicho começa daqui, com as respostas do escritório.

**Passo 2. Como ele fala.** Pergunte: "Depois que vira cliente, que palavras ele usa para falar do caso? Me cola duas mensagens reais, sem nome". Monte a tabela "O cliente diz · Quer dizer · Como responder" só a partir das mensagens e das respostas do advogado. Para cada linha, confirme com uma pergunta curta ("Quando ele diz 'tô encostado', quer dizer que recebe o auxílio?"). Expressão que ninguém confirmou não entra.

**Passo 3. Os momentos de aflição.** Pergunte: "Quando o cliente costuma se desesperar? Pense na última ligação aflita que vocês receberam". Para cada momento: o sinal na mensagem e o que o escritório faz. Violência, risco à vida e criança em risco não são momento do nicho: são parada imediata (`../../docs/regras.md`, seção 5).

**Passo 4. O que ele pesquisa sozinho.** Pergunte: "O que o cliente traz pronto, da internet ou de uma IA? Qual o erro mais comum que vocês precisam desfazer?". Este é o centro do suporte: é o que a `status-para-o-cliente` e a `cliente-com-ia` (se instalada) vão responder antes da pergunta.

**Passo 5. As perguntas depois do contrato.** Pergunte: "Quais são as dez perguntas que mais chegam de quem já é cliente?". Do jeito que chegam.

**Passo 6. Cuidados, sazonalidade e ritmo.** Pergunte uma coisa por vez: o que nunca dizer a esse público; os meses cheios e vazios (`sazonalidade`); o tempo típico de cada fase, que fica `[CONFERIR]`.

**Passo 7. Gravar o nicho.** Monte no formato fixo de `../../docs/adaptar-ao-escritorio.md`. Se o `nicho.md` existe, mostre só as seções novas ou mudadas, com `[NOVO]` ou `[ALTERADO]`. Grave com o ok. O que valer para todo o escritório (por exemplo, `como_o_cliente_fala`) também vai para a ficha, com linha no histórico.

### Parte 2. Os materiais (as habilidades no modo adaptar)

**Passo 8.** Para cada habilidade instalada, chame o modo adaptar dela, nesta ordem, e mostre o resultado de uma antes de seguir para a outra:

| Habilidade | O que ela reescreve |
|---|---|
| `jornada-do-cliente` | As jornadas gravadas (ou as dos três casos mais comuns do nicho) |
| `status-para-o-cliente` | O glossário do cliente, com a seção "Como o cliente fala", e os modelos de andamento |
| `boas-vindas-do-cliente` | As mensagens de boas-vindas e o combinado de comunicação |
| `resumo-mensal-do-caso` | O modelo do resumo e as mensagens que o acompanham |
| `rotina-da-experiencia` | Os critérios da ficha da automação pela sazonalidade e as palavras de aflição do nicho |
| Outras instaladas (`cliente-com-ia`, `checklist-de-documentos`, `preparar-o-cliente`, `triar-mensagem-do-cliente` e as demais, se instaladas) | O que cada uma diz no modo adaptar dela |

Habilidade não instalada: diga em uma linha o que ela adaptaria e siga. Cada uma marca `[ALTERADO]` e grava só com o ok.

**Passo 9. Conferir a costura.** Uma palavra, uma tradução: o termo que o glossário traduziu de um jeito sai igual na jornada, no resumo e nas mensagens. Mostre as divergências e pergunte qual vale.

### Parte 3. Os casos de teste

**Passo 10.** Pergunte: "Pode me colar de cinco a doze mensagens reais de clientes, anonimizadas, das que dão trabalho?". Para cada uma, monte o caso em `assets/modelo-caso-de-teste.md` e peça ao advogado o gabarito: caminho, urgência e o que não pode falhar. Cubra os momentos de aflição do nicho, um cliente com resposta de IA, uma notícia ruim, um pedido de senha e um pedido para parar.

**Passo 11.** Rode as habilidades instaladas contra os casos (sem mostrar o gabarito antes), compare e registre o resultado em cada caso. Falhou: falta campo, linha no nicho ou aprendizado. Ajuste e rode de novo. Grave em `escritorio/04-base/casos-de-teste/experiencia/`.

### Parte 4. Rotina nova vira habilidade

**Passo 12.** Pergunte: "Tem alguma coisa que vocês fazem sempre do mesmo jeito com o cliente e que nenhuma habilidade faz?" (`rotinas_proprias`). Uma rotina por vez. Siga `references/rotina-nova.md`: entrevista, escrever em `rotinas-do-escritorio.md` com S, A e H, gerar a habilidade pelo `assets/modelo-habilidade-do-escritorio.md`, testar com três casos e empacotar:

```
python3 scripts/empacotar_habilidade.py escritorio/04-base/habilidades-do-escritorio/<nome> \
  --testes escritorio/04-base/casos-de-teste/experiencia/<nome>-testes.md
```

O caminho do script é relativo à pasta desta habilidade, e os da habilidade própria e do registro dos testes, à pasta de trabalho. O registro segue `assets/modelo-registro-dos-testes.md`: três casos (o comum, o com exceção, o que deve parar), cada um com a linha `Resultado:`. O script confere nomes (só `a-z`, `0-9`, ponto e hífen), caminhos de até 100 caracteres, o frontmatter, as seções obrigatórias, os arquivos citados e os três resultados. Só aceita `Resultado: passou`: o texto cru do modelo ("passou | falhou"), "...", vazio ou "falhou" não passam. Com problema, não gera nada e lista o que corrigir.

### Passo final. Aprender

Pergunte: "O que dessa adaptação vale como regra para todas as habilidades?". Correção que é política do escritório sobe para a ficha; regra de comportamento entra nos aprendizados (`../../docs/aprender-com-o-uso.md`), com o ok. No modo revisar, junte regras repetidas, suba para a ficha ou para o nicho o que virou padrão e retire o que não vale mais.

## 4. De onde sai o nicho

O plugin não traz perfil de nicho por área. Cada `nicho.md` sai de três fontes do próprio escritório, nesta ordem:

| Fonte | O que dá | Como pedir |
|---|---|---|
| Entrevista (passos 1 a 6) | Quem é o cliente, as aflições, os cuidados, o ritmo | Uma pergunta por vez, com a cena concreta |
| Mensagens reais anonimizadas | Como o cliente fala, o que ele pesquisa sozinho, as perguntas que mais chegam | "Me cola duas mensagens das que dão trabalho, sem nome" |
| Aprendizados e fichas | O que o escritório já corrigiu e já decidiu | Leitura de `aprendizados-experiencia.md` e das fichas antes de perguntar |

Escritório com mais de uma área: um nicho principal e, se o advogado quiser, uma seção por área no mesmo `nicho.md`. Se o `nicho.md` já existe (escrito pela `adaptar-comercial`, se instalada), complete as seções do suporte em vez de recomeçar.

## 5. Exemplo resolvido (Escritório Modelo)

Previdenciário em Belo Horizonte, muitos idosos e familiares que falam por eles. No passo 2, a advogada cola: "a mãe tá encostada desde março e a carta disse que cortou". No passo 4: "Eles chegam com o print do Meu INSS e a resposta do ChatGPT dizendo que o INSS tem 45 dias para responder".

Linhas gravadas no `nicho.md`:
```
## Como ele fala
| O cliente diz | Quer dizer | Como responder |
|---|---|---|
| "tá encostada" | recebe benefício por incapacidade | usar "o seu auxílio" e explicar uma vez |
| "a carta disse que cortou" | cessação do benefício | pedir a foto da carta, sem dado pessoal |

## O que este nicho pesquisa sozinho
- Prazo do INSS lido na internet ou dado por IA. Erro mais comum: achar que o prazo é garantia de resposta. [CONFERIR] o que a norma diz antes de explicar.
```

No passo 8, a `status-para-o-cliente` acrescenta ao glossário "tá encostado" e troca "concluso para despacho" por "o processo está na mão do juiz para o próximo passo" `[ALTERADO]`. No passo 12, a rotina "ligação de boas-vindas no dia seguinte" vira `ligacao-de-boas-vindas`, testada com o caso comum, com um cliente de família sem canal seguro (exceção) e com um cliente que diz estar arrependido do contrato (para e chama a advogada).

## 6. Formato da saída

Cada parte é mostrada antes de gravar: o `nicho.md` com `[NOVO]` e `[ALTERADO]` nas seções do suporte; para cada habilidade chamada no modo adaptar, o material reescrito com as mudanças marcadas; os casos de teste numa tabela (caso, caminho esperado, resultado, ajuste); e, na rotina nova, a rotina com S, A e H, o SKILL.md da habilidade própria, os três casos testados e a saída do empacotador. No fim, uma lista do que foi gravado e do que ficou em aberto.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Perfil do nicho | `escritorio/04-base/comum/nicho.md` |
| Jornadas, glossário, biblioteca e modelos adaptados | `escritorio/04-base/relacionamento-com-o-cliente/` (cada habilidade grava o dela) |
| Casos de teste | `escritorio/04-base/casos-de-teste/experiencia/` |
| Rotinas próprias | `escritorio/04-base/comum/rotinas-do-escritorio.md` |
| Habilidade própria e o .zip | `escritorio/04-base/habilidades-do-escritorio/<nome>/` e `<nome>.zip` |
| Campos que subiram | `escritorio/04-base/comum/ficha-do-escritorio.md` ou `ficha-da-experiencia.md`, com linha no histórico |
| Regras aprendidas | `escritorio/04-base/comum/aprendizados-experiencia.md` |

Tudo em `04-base/`: pode ir para o Projeto no Claude, por isso nada de dado de cliente. Sem pasta aberta: cada documento vem em bloco para colar, e a habilidade própria vem com a estrutura de pastas para o advogado montar o .zip.

## 8. Solo e equipe

**Solo:** faça em duas sentadas: o nicho numa, os materiais e os casos de teste noutra. A rotina própria do solo costuma ser simples ("ligo para todo cliente novo no dia seguinte"), e vale a pena virar habilidade porque é a primeira que some na semana cheia.

**Equipe:** quem fala com os clientes todo dia (secretária, atendente) responde os passos 2 a 5; a advogada confirma os cuidados, os gabaritos e o que nunca vai por mensagem. Uma pessoa é dona do `nicho.md`.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Nicho copiado da internet | Mensagens com palavras que o cliente não usa | Regra fixa 1 |
| "70% dos clientes perguntam X" | Número inventado na base | Regra fixa 2 |
| Cada habilidade traduzindo de um jeito | Cliente confuso entre mensagem, resumo e página | Passo 9, a costura |
| Reescrever o que o advogado já aprovou | Retrabalho e desconfiança | `[ALTERADO]` e ok a cada material |
| Rotina própria só na cabeça de alguém | Some na semana cheia ou nas férias | Parte 4, rotina vira habilidade |
| Habilidade com nome que não instala | Pacote recusado na hora de enviar | O empacotador confere os nomes |
| Habilidade empacotada sem teste de verdade | "passou \| falhou" do modelo tomado como aprovado | O empacotador só aceita `Resultado: passou` nos três casos |
| Testar com cliente real sem gabarito | Erro descoberto pelo cliente | Parte 3, casos de teste antes |

## 10. Próximo passo

- Uma jornada que ainda não existe para um caso comum do nicho: `jornada-do-cliente`.
- O ciclo do dia já no jeito do nicho: `rotina-da-experiencia`.
- As perguntas do nicho respondidas antes: `cliente-com-ia` (se instalada). Sem ela, elas ficam no `nicho.md` e na jornada.
- O comercial no mesmo nicho: `adaptar-comercial` do motor-comercial (se instalado).

## Referências desta habilidade

- `references/rotina-nova.md`: a entrevista, o registro e o caminho da rotina própria até o .zip. Leia no passo 12.
- `assets/modelo-caso-de-teste.md`: o formato do caso de teste do escritório. Use no passo 10.
- `assets/modelo-habilidade-do-escritorio.md`: o modelo da habilidade própria. Use no passo 12.
- `assets/modelo-registro-dos-testes.md`: o registro dos três testes que o empacotador confere. Use no passo 12.
- `scripts/empacotar_habilidade.py`: confere e gera o .zip da habilidade própria. Rode no passo 12.
