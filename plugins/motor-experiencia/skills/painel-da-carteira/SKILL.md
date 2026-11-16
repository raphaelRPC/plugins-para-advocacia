---
name: painel-da-carteira
description: >
  Monta o painel interno da carteira de clientes por script: clientes por fase e por área, dias
  sem notícia (a distribuição e os piores casos), compromissos da semana e do mês, documentos
  pendentes, reclamações e humor, notas de satisfação, quem recebe resumo e página do caso, e os
  próximos contatos vencidos. Entrega o painel em .md e numa página HTML (artefato do Claude, para
  uso só do escritório, responsiva e com modo escuro), com três leituras e três ações sem inventar
  causa. Use quando o advogado disser "como está a carteira", "painel do mês", "quantos clientes
  estão sem notícia", "quem são os piores", "me mostra a carteira num painel", "o que levo para a
  reunião da equipe". Não use para o retrato do dia com a fila de mensagens (use
  rotina-da-experiencia).
---

# Painel da carteira

> Um retrato da carteira inteira, para o escritório decidir onde agir: quem está sem notícia, o que vem aí, o que está travado e como os clientes estão se sentindo. Fica dentro do escritório.

Regras comuns: `../../docs/regras.md` (em especial a seção 6.1). Campos das fichas: `../../docs/ficha-da-experiencia.md` e `../../docs/ficha-da-experiencia-modelo.md`. Carteira: `../../docs/carteira.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

Segunda, reunião da equipe. A pergunta "como está a carteira?" recebe três respostas diferentes, cada uma lembrando dos clientes que mais escreveram. O painel responde com a carteira inteira: dois clientes passaram de 30 dias sem notícia, um deles insatisfeito; duas audiências e uma perícia nos próximos 7 dias; três contatos combinados que venceram. A reunião sai com três ações e um dono para cada.

**Regras fixas desta habilidade:**
1. Painel interno. Nunca é compartilhado com cliente, nem por link nem por imagem (seção 6.1 de `regras.md`).
2. Número só da carteira. Coluna vazia é dado que ainda não existe; o painel diz isso e não completa.
3. Leitura sem causa inventada. O painel mostra o que aconteceu; a causa só entra com dado, senão vira pergunta para a equipe.
4. Treino não entra no painel real. Carteira de `_treino/` gera painel marcado "TREINO".

## 1. Quando usar

**Use quando:**
- Fim do mês, ou a reunião da equipe pede um retrato da carteira.
- O advogado quer saber quantos clientes estão sem notícia e quem são os piores.
- A `reclamacao-e-recuperacao` (se instalada) pediu para achar quem mais está na mesma situação.
- O escritório quer acompanhar se um ajuste da jornada está funcionando (mês a mês).
- Para testar o plugin com a carteira dos casos fictícios.

**Não use quando:**
- O pedido é o dia de hoje, com mensagens para rascunhar e a fila: `rotina-da-experiencia` (se instalada) ou `/motor-experiencia:ciclo`.
- O pedido é mostrar o caso ao cliente: `pagina-do-caso` (se instalada). O painel nunca vai para cliente.
- O pedido é o resumo das respostas da pesquisa com os comentários: `pesquisa-de-satisfacao` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`) e os aprendizados (`aprendizados-experiencia.md`). O `maximo_sem_noticia` é a régua do painel.
2. **Ache a carteira:** `escritorio/07-operacao/experiencia/carteira.csv` (formato em `../../docs/carteira.md`). Planilha do Excel serve (ponto e vírgula, com ou sem BOM).
3. **Leia o painel anterior** em `07-operacao/experiencia/painel/`, se existir, para comparar.
4. **Conta de IA:** o painel tem código e primeiro nome de clientes. Em conta pessoal, só a carteira de treino.
5. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se quiserem seguir, pergunte só o `maximo_sem_noticia` e ofereça gravar.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `maximo_sem_noticia`.
- **Melhora:** X: a ficha inteira.

Na prática, além do `maximo_sem_noticia`: `resumo_mensal` e `pagina_do_caso` (para ler a seção de resumo), `lembrete_de_compromisso` e `cobranca_de_documentos` (para dizer o que está fora da régua), `pesquisa_quando` (para ler a satisfação). Sem `maximo_sem_noticia`, o painel mostra a distribuição e marca a régua `[A DEFINIR]`.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Painel do mês | Rotina mensal ou reunião | Passos 1 a 7, grava `.md` e, se quiserem, o HTML |
| Pergunta rápida | "Quantos sem notícia?" | Passo 2 e a resposta em três linhas, sem gravar |
| Treino | Primeiro uso, teste do plugin | Roda com `assets/carteira-de-treino.csv` (a carteira dos casos fictícios), grava em `_treino/experiencia/painel/` |
| Adaptar | A `adaptar-experiencia` (se instalada) | Ajusta as faixas e os rótulos ao nicho (por exemplo, faixas de dias para casos longos), com `[ALTERADO]`, e grava só com o ok |

O painel é interno e não tem rascunho para cliente, então não entra na fila. A tarefa agendada da `rotina-da-experiencia` (se instalada) pode pedir o painel todo dia 1.

### Passo 1. Data e régua
Pergunte só o que faltar: "Painel com a data de hoje? E o máximo sem notícia é [maximo_sem_noticia] dias?". Com a ficha preenchida, o script lê o `maximo_sem_noticia` sozinho (só o texto antes do parêntese do modelo); a opção `--maximo-sem-noticia` vale por cima da ficha.

### Passo 2. Rodar o script
Rode o script da pasta desta habilidade, com o caminho da carteira:

```
python3 "<pasta desta habilidade>/scripts/painel_carteira.py" escritorio/07-operacao/experiencia/carteira.csv \
  --hoje AAAA-MM-DD --saida escritorio/07-operacao/experiencia/painel/AAAA-MM.md
```

Sem `--maximo-sem-noticia`, o script procura `escritorio/04-base/comum/ficha-da-experiencia.md` subindo a partir da carteira (ou lê a ficha indicada em `--ficha`), como o `carteira.py` da `rotina-da-experiencia` faz, e diz no painel de onde veio a régua. Sem ficha e sem a opção, a régua sai `[A DEFINIR]`. `--data` é o mesmo que `--hoje`. No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/painel-da-carteira`. O script sai com erro e uma mensagem clara quando falta o arquivo, falta uma coluna obrigatória (`codigo`, `area`, `fase`, `ultimo_contato`) ou a carteira não tem cliente. Nunca diz "nada a apontar" sem ter lido. Avisos de preenchimento (data que não leu, fase fora da lista) saem no fim do painel.

**Teste com a carteira fictícia:**

```
python3 "<pasta desta habilidade>/scripts/painel_carteira.py" "<pasta desta habilidade>/assets/carteira-de-treino.csv" \
  --hoje 2026-04-10 --maximo-sem-noticia 30
```

Resultado esperado: 8 ativos; Jorge (49 dias) e Marta (36 dias) além do máximo; Paulo (audiência em 2026-04-13, em 3 dias) e Marta (perícia em 2026-04-14, em 4 dias) nos próximos 7 dias; Renata com 2 documentos; Jorge insatisfeito sem reclamação registrada; ninguém pediu para não receber rotina ainda (o pedido do Ivan é a mensagem 12 dos casos fictícios, e só entra depois de triado); três contatos vencidos (Jorge, Marta, Renata) e dois para hoje (Paulo, Sueli). A carteira de treino é a mesma da `rotina-da-experiencia`.

Sem o script (chat sem arquivos): calcule à mão pelas regras de `references/como-ler-o-painel.md`, seção 1, e diga que foi à mão.

### Passo 3. Conferir o que o script avisou
Leia a seção "Avisos de preenchimento". Data que não foi lida ou fase fora da lista: mostre a linha e pergunte se corrige a carteira agora. Coluna inteira faltando: diga qual parte do painel saiu vazia por isso.

### Passo 4. Três leituras
Escreva três leituras, cada uma com o número e de onde ele vem. Exemplos de forma (`references/como-ler-o-painel.md`, seção 2):
- "2 de 8 ativos passaram de 30 dias sem notícia; os dois são do previdenciário."
- "O único cliente insatisfeito não tem reclamação registrada."
- "3 contatos combinados venceram; o mais antigo há 19 dias."
Sem causa que o dado não mostra. Se houver painel anterior, uma das leituras compara.

### Passo 5. Três ações
Uma ação por leitura, com dono (função), prazo e a habilidade que cuida:
- "Notícia para Jorge e Marta hoje: `status-para-o-cliente`; Jorge pela `reclamacao-e-recuperacao`."
- "Registrar a reclamação do cliente insatisfeito: `reclamacao-e-recuperacao`."
- "Rodar o ciclo ou a rotina para os contatos vencidos: `rotina-da-experiencia`."
Habilidade não instalada: diga em uma linha o que fazer à mão.

### Passo 6. A página HTML (se quiserem)
Pergunte: "Quer a versão em página, para abrir na reunião?". Se sim, rode com `--html`:

```
python3 "<pasta desta habilidade>/scripts/painel_carteira.py" escritorio/07-operacao/experiencia/carteira.csv \
  --hoje AAAA-MM-DD --nome-do-escritorio "[NOME]" \
  --html escritorio/07-operacao/experiencia/painel/AAAA-MM.html
```

O script preenche o modelo `assets/painel-modelo.html` (responsivo, claro e escuro, sem nada externo). Antes de publicar como artefato do Claude, diga: "Esta página é interna. O artefato nasce privado; não compartilhe o link com cliente nem fora da equipe (conferir na configuração da conta como o compartilhamento funciona)." Se o escritório preferir, a página fica só no arquivo, aberta no navegador. A identidade visual da ficha pode trocar as cores dos tokens no topo do modelo, no modo adaptar.

### Passo 7. Gravar
Mostre o painel com as leituras e as ações e grave com o ok em `07-operacao/experiencia/painel/AAAA-MM.md` (as leituras e ações no fim do arquivo, com a coluna de decisão).

### Passo 8. Aprender
Pergunte: "Alguma leitura ou ação você faria diferente? Alguma faixa que não faz sentido para vocês?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-experiencia.md`. Faixa ou rótulo que muda de vez vai para o modo adaptar.

## 4. O que o painel mostra

| Seção | De onde vem | O que responde |
|---|---|---|
| Números | carteira inteira | O tamanho da carteira e os alertas do mês |
| Fase e área | `fase`, `area` dos ativos | Onde a carteira está parada |
| Dias sem notícia | `ultimo_contato` dos ativos, em dias corridos | Se a régua está sendo cumprida, e quem está pior |
| Compromissos | `proximo_compromisso`, `data_compromisso` | O que vem em 7 e em 30 dias, e o que passou sem atualizar |
| Documentos | `documentos_pendentes` | Quem está travando o caso por documento |
| Reclamações e humor | `reclamacao_aberta`, `humor` | Quem precisa de uma pessoa, e insatisfeito sem reclamação registrada |
| Satisfação | `satisfacao` | Notas, faixas, notas baixas sem reclamação registrada |
| Resumo e página | `resumo_mensal`, `pagina_do_caso`, `pediu_para_nao_receber` | Quem recebe o quê |
| Próximos contatos | `proximo_contato`, `motivo_proximo_contato` | O que venceu, o que é hoje, quem está sem próximo contato |

Encerrados (`fase = encerrado`) contam no total e nos encerrados do mês, e ficam fora de "sem notícia", compromissos e documentos.

## 5. Formato da saída

O painel em .md segue a ordem da seção 4, com o cabeçalho "Uso interno do escritório. Não compartilhar com cliente." Depois do painel, no chat e no fim do arquivo:

```
## Leituras
1. [LEITURA COM NÚMERO E FONTE]
2. ...
3. ...

## Ações
| Ação | Dono | Até | Habilidade | Decisão |
|---|---|---|---|---|
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Painel do mês (.md, com leituras e ações) | `escritorio/07-operacao/experiencia/painel/AAAA-MM.md` |
| Página HTML (opcional, interna) | `escritorio/07-operacao/experiencia/painel/AAAA-MM.html` |
| Painel de treino | `escritorio/07-operacao/_treino/experiencia/painel/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-experiencia.md` |

O painel não muda a carteira. Correção de preenchimento que aparecer nos avisos é feita na carteira com o ok, linha por linha. Sem pasta aberta: o painel sai no chat, e a página não é gerada.

## 7. Solo e equipe

**Solo:** o painel do mês leva cinco minutos e evita a sensação de "estou devendo para todo mundo". Olhe primeiro os piores e os vencidos.

**Equipe:** o painel abre a reunião mensal. Cada ação tem um dono. O painel fala de clientes e de régua, nunca de quem atendeu. Se a mesma pessoa aparece como responsável de todos os piores, isso é carga de trabalho, e a conversa é sobre distribuição, em particular.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Painel compartilhado com cliente | Exposição de outros clientes | Regra fixa 1; aviso antes de publicar |
| Script que não leu e diz "tudo certo" | Falsa tranquilidade | Erro claro sem arquivo, sem coluna ou sem linha |
| Média que esconde o pior | Cliente de 60 dias some numa média de 12 | Distribuição por faixas e a lista dos piores |
| Causa inventada na leitura | Ação errada, equipe na defensiva | Leitura com número; causa só com dado |
| Painel sem ação | Reunião que só olha números | Três ações com dono e prazo |
| Treino misturado | Números falsos no mês | `_treino/` marcado "TREINO" |

## 9. Próximo passo

- Clientes sem notícia: `status-para-o-cliente` ou `resumo-mensal-do-caso` (se instaladas).
- Insatisfeito sem reclamação: `reclamacao-e-recuperacao` (se instalada).
- Contatos vencidos todo dia: `rotina-da-experiencia` (se instalada) ou `/motor-experiencia:ciclo`.
- Notas baixas: `pesquisa-de-satisfacao` (se instalada).
- Régua que não se sustenta: `jornada-do-cliente` (se instalada).

## Referências desta habilidade

- `scripts/painel_carteira.py`: o painel por script, em .md e HTML. Rode nos passos 2 e 6.
- `assets/painel-modelo.html`: o modelo da página interna, preenchido pelo script. Use no passo 6.
- `assets/carteira-de-treino.csv`: a carteira dos casos fictícios, para o teste. Use no modo treino.
- `references/como-ler-o-painel.md`: as regras de cálculo e como escrever leituras e ações. Leia nos passos 4 e 5.
