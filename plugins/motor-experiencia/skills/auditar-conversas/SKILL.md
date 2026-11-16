---
name: auditar-conversas
description: >
  Audita uma amostra de conversas reais anonimizadas com clientes ativos (coladas ou exportadas do
  WhatsApp) contra as fichas e a jornada: tempo de resposta contra o prazo da ficha, máximo sem
  notícia, notícia ruim por mensagem, promessa de prazo ou resultado, termo técnico sem
  explicação, confirmação do que uma IA disse ao cliente, dado sensível e pedido de senha.
  Entrega o relatório com achados por gravidade e trechos anonimizados, propõe ajustes na
  biblioteca, na jornada, nas fichas e nos aprendizados (aplicados só com o ok) e faz a revisão
  mensal dos aprendizados da experiência. Use quando o advogado disser "audita as conversas com os
  clientes", "a equipe está respondendo os clientes certo?", "revisão dos aprendizados", "por que
  os clientes reclamam de demora?". Não use para conversas de quem ainda não é cliente (use
  auditar-conversas-comerciais do motor-comercial).
---

# Auditar conversas com clientes

> Uma vez por mês, uma amostra das conversas com quem já é cliente lida contra o que o escritório combinou: prazo de resposta, régua de notícia, o que nunca vai por mensagem. O que aparece vira ajuste concreto no método.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-da-experiencia.md`, `../../docs/ficha-da-experiencia-modelo.md` e `../../docs/ficha-do-escritorio-modelo.md`. Carteira e jornada: `../../docs/carteira.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

A ficha diz "primeira resposta em até 4 horas úteis" e "notícia ruim só por ligação". Nas conversas do mês, as respostas saíram rápido. Uma delas dizia "saiu a sentença, infelizmente foi improcedente". Outra confirmava o que o ChatGPT tinha dito à filha de uma cliente: "o juiz decide essa semana". Ninguém fez por mal. Sem auditoria, isso só aparece quando o cliente cobra a semana prometida.

**Regras fixas desta habilidade:**
1. Só conversa anonimizada entra no relatório. A conversa bruta não é gravada; só os trechos dos achados, anonimizados.
2. Achado tem trecho. Nada de "o tom está frio" sem a frase que mostra isso.
3. A auditoria aponta e propõe. Nada muda na biblioteca, na jornada, nas fichas ou nos aprendizados sem o ok, item por item.
4. Achado crítico (linha vermelha, ética, dado sensível, senha) vai para o advogado na hora, antes do resto do relatório.
5. O relatório fala de condutas e mensagens, não de pessoas.

## 1. Quando usar

**Use quando:**
- Fechou o mês e o escritório quer saber se o cuidado com os clientes seguiu as fichas e a jornada.
- Os aprendizados passaram de 30 linhas `em uso`, ou faz um mês da última revisão.
- A `reclamacao-e-recuperacao` (se instalada) achou uma causa e o advogado quer ver se é caso isolado.
- O `painel-da-carteira` (se instalado) mostrou muitos clientes além do máximo sem notícia.
- A `pesquisa-de-satisfacao` (se instalada) trouxe comentários repetidos ("demora para responder").

**Não use quando:**
- As conversas são com quem ainda não é cliente (contato novo, negociação): `auditar-conversas-comerciais` do motor-comercial (se instalado).
- O pedido é o que fazer com a mensagem que acabou de chegar: `triar-mensagem-do-cliente` (se instalada).
- O pedido é avaliar um colaborador: a auditoria olha mensagens contra a ficha, não serve de avaliação individual.

## 2. Antes de começar

1. **Leia a régua:** as duas fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), o `nicho.md` se existir, os aprendizados (`aprendizados-experiencia.md`), a biblioteca (`04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`), as jornadas (`jornada-*.md`) e o glossário do cliente, se existirem.
2. **Leia a auditoria anterior** (`escritorio/07-operacao/experiencia/auditorias/`). Achado que se repete sobe de gravidade.
3. **Leia a carteira** (`escritorio/07-operacao/experiencia/carteira.csv`) para montar a amostra e cruzar ligações e reuniões que não aparecem na conversa.
4. **Conta de IA:** conversa real, mesmo anonimizada, só em conta profissional ou de equipe (`conta_de_ia`). Em conta pessoal: só o treino.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tom_em_tres_palavras`, `frases_que_nunca_usamos` · X: `primeira_resposta_cliente_ativo`.
- **Melhora:** as duas fichas inteiras.

Na prática, os que mais pesam: X: `maximo_sem_noticia`, `resposta_ponte`, `resposta_completa`, `nunca_por_mensagem`, `quem_le_antes_de_enviar`, `avisa_movimentacao_relevante`, `resumo_mensal`; E: `tratamento`, `emoji`, `audio`, `assinatura_das_mensagens`, `horario_de_atendimento`, `sempre_vai_para_pessoa`. Sem `primeira_resposta_cliente_ativo`, a auditoria mede o tempo mas não diz se está no prazo, e o relatório marca `[A DEFINIR]`.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Auditoria do mês | Rotina mensal | A amostra montada pela carteira | Relatório completo e revisão dos aprendizados |
| Conversa avulsa | Reclamação, caso estranho | Uma conversa colada | Os achados daquela conversa |
| Só aprendizados | Arquivo cresceu ou passou um mês | O arquivo de aprendizados | A revisão da seção 6 |
| Treino | Conhecer a habilidade | Conversas fictícias dos casos do plugin | Relatório gravado em `_treino/experiencia/auditorias/` |

A auditoria é interna e não produz mensagem para cliente, por isso não entra no ciclo nem na fila. A tarefa agendada da `rotina-da-experiencia` (se instalada) pode lembrar a auditoria todo mês.

### Passo 1. Montar a amostra pela carteira
Proponha a amostra, para ninguém escolher só as conversas boas:
- **Tamanho:** 10 conversas no escritório solo, 15 a 20 com equipe.
- **Entram sempre:** clientes com `reclamacao_aberta = sim` ou `humor = insatisfeito`; os além do `maximo_sem_noticia`; quem teve decisão no período (`fase = decisao` ou mudança recente); quem teve compromisso no período.
- **O resto:** sorteado entre os ativos, de áreas diferentes.
- Mostre a lista: "Me exporte estas conversas: C-2026-0001, C-2025-0088...". Sem carteira: "as 10 últimas conversas com clientes, sem escolher".

### Passo 2. Receber e anonimizar
- Pergunte: "Vai colar aqui ou exportar? No WhatsApp, a opção é exportar a conversa sem mídia (o nome do menu muda conforme o aparelho; conferir no celular)."
- Um arquivo por conversa, com o código da carteira no nome (`C-2026-0001.txt`), numa pasta temporária (sugestão: `escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD-conversas/`). Não use a `entrada/`: o ciclo leria as conversas como mensagens novas.
- Quem escreve pelo escritório vira a função (`ADVOGADA`, `SECRETARIA`), a resposta automática vira `AUTOMATICO`. Quem fala pelo cliente (filha, procurador) segue como o cliente.
- O resto pela tabela das regras: `[CLIENTE]`, `[DOC]`, `[PROCESSO]`, `[ENDEREÇO]`, `[CONTATO]`. Saúde e violência: só a descrição ("intercorrência de saúde").
- No fim, lembre a pessoa de apagar a pasta temporária. A habilidade não apaga arquivo.

### Passo 3. Medir os tempos e os intervalos sem notícia
Rode o script da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/tempos.py" escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD-conversas/*.txt \
  --equipe "ADVOGADA,SECRETARIA" --automatico "AUTOMATICO" --prazo-horas [N] \
  --horario 09:00-18:00 --dias seg-sex --maximo-sem-noticia [N] --hoje "AAAA-MM-DD HH:MM" \
  --csv escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD-tempos.csv
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/auditar-conversas`. Ele devolve, por conversa: esperas respondidas e fora do prazo, cobranças repetidas sem resposta, se termina sem retorno, o maior intervalo sem mensagem do escritório e os dias desde a última. Sem conversa lida, para com erro. Depois cruze com a carteira e o `historico.md`: ligação, reunião, resumo ou página registrados como contato fecham o intervalo. Linha de trabalho do escritório (canal `trabalho-do-escritorio`), resposta-ponte, cortesia, lembrete de documento e pesquisa não fecham: o cliente continuou sem notícia (`../../docs/agentes-e-fila.md`). Mas olhe as linhas de trabalho do escritório do período: trabalho feito e nunca contado ao cliente é achado de comunicação (o escritório trabalhou e o cliente não soube), com o ajuste "levar ao resumo do mês ou à página do caso". Sem o script: meça à mão pelas regras do critério 1 de `references/criterios-da-auditoria.md`.

### Passo 4. Ler cada conversa contra os nove critérios
Na ordem de `references/criterios-da-auditoria.md`: (1) tempo de resposta, (2) máximo sem notícia, (3) notícia ruim por mensagem, (4) promessa de prazo ou resultado, (5) termo técnico sem explicação, (6) confirmação do que a IA disse ao cliente, (7) dado sensível, (8) senha e credencial, (9) tom. Para cada achado: conversa, critério, trecho (até duas linhas, anonimizado), gravidade, por que importa.

### Passo 5. Avisar o crítico na hora
Achado crítico: pare e mostre ao advogado antes de seguir, com o trecho e a pergunta: "Quer que eu prepare o que precisa agora (roteiro de ligação, resposta para corrigir) para você decidir?". Notícia ruim já dada por mensagem: roteiro de ligação pela `status-para-o-cliente` (se instalada). Senha enviada: orientar o cliente a trocar, por ligação. Vulnerabilidade sem passagem para pessoa: a advogada liga.

### Passo 6. Achar o padrão
Junte os achados que se repetem. Três conversas com o mesmo problema são um padrão, e a causa provável está na biblioteca, na jornada, na ficha ou na rotina, não na pessoa. Achado que já estava na auditoria anterior sobe um nível.

### Passo 7. Propor os ajustes
Cada padrão vira uma proposta, num destes destinos:
- **Biblioteca:** mensagem nova ou trecho que muda (por exemplo, a resposta-padrão a pedido de senha).
- **Jornada:** momento de contato novo ou frequência diferente numa fase (pela `jornada-do-cliente`, se instalada).
- **Fichas:** campo que falta ou não bate com a prática (`nunca_por_mensagem`, `sempre_vai_para_pessoa`, `frases_que_nunca_usamos`, prazo que ninguém cumpre).
- **Glossário do cliente:** termo que apareceu sem explicação.
- **Aprendizados:** regra curta, com verbo, objeto e exemplo anonimizado.
- **Carteira:** `proximo_contato` para quem está além do máximo; reclamação a registrar.

### Passo 8. Mostrar, aprovar item por item, gravar
Mostre o relatório (`assets/relatorio-modelo.md`). Para cada proposta: "Aplico esta? (sim, não, depois)". Aplique só o que teve sim, mostrando o trecho com `[NOVO]` ou `[ALTERADO]`. Ficha alterada: suba a versão e acrescente a linha no histórico. Grave o relatório em `escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD.md`, com a coluna "decisão".

### Passo 9. Revisão mensal dos aprendizados
Na auditoria do mês, ou no modo "só aprendizados", siga a seção 6.

### Passo 10. Aprender
Pergunte: "Algum achado você não considera erro aqui no escritório?". A resposta ajusta a régua: vira aprendizado ("Áudio para cliente idoso que pediu áudio não é achado") ou campo da ficha. Se o advogado discordar de um achado ético (notícia ruim por mensagem, promessa, senha), explique a regra do plugin e não guarde a exceção (`../../docs/aprender-com-o-uso.md`, regra 5).

## 4. Gravidade

| Gravidade | O que entra | O que acontece |
|---|---|---|
| **Crítica** | Notícia ruim por mensagem; promessa de resultado ou de data de decisão; confirmação do que a IA disse; senha ou credencial; vulnerabilidade sem passagem para pessoa; dado de um cliente enviado a outro; mensagem de rotina para quem pediu para não receber; reclamação respondida com mensagem pronta | Aviso ao advogado na hora (passo 5). Proposta obrigatória |
| **Alta** | Além do máximo sem notícia; "te retorno" descumprido; cobrança repetida sem resposta; compromisso próximo sem preparação; dado sensível pedido sem necessidade | Proposta obrigatória. Volta na próxima auditoria |
| **Média** | Prazo da ficha estourado sem dano visível; tom fora da ficha; frase da lista do que nunca se usa; ridicularizar pergunta | Proposta quando for padrão |
| **Baixa** | Termo técnico sem explicação isolado; assinatura; tamanho | Só no resumo, se for padrão |

## 5. Formato da saída

O relatório segue `assets/relatorio-modelo.md`: cabeçalho, amostra e régua, resumo em cinco linhas, tempos e intervalos, achados por gravidade (críticos primeiro), comparação com a auditoria anterior, propostas com a coluna de decisão, revisão dos aprendizados, linhas da carteira e a próxima auditoria. Cada achado usa o formato do fim de `references/criterios-da-auditoria.md`. Cada proposta:

```
Proposta [N] · [biblioteca | jornada | ficha | glossário | aprendizados | carteira]
Achados: [números]
O que muda: [o texto atual] > [o texto proposto]
Por quê: [o padrão, com quantas conversas]
Decisão: sim | não | depois
```

O exemplo completo, com sete conversas da carteira fictícia, está no fim de `assets/relatorio-modelo.md`.

## 6. Revisão mensal dos aprendizados

Segue `../../docs/aprender-com-o-uso.md`, seção "Revisão", com as conversas como prova. O passo a passo está em `references/revisao-dos-aprendizados.md`. Em resumo:

1. **Juntar repetidas.**
2. **Subir para a ficha ou para a jornada** o que virou política. A linha fica `retirada`, com a nota "incorporada à ficha: [campo]".
3. **Retirar** o que não vale mais.
4. **Decidir as `em teste`** com mais de 30 dias.
5. **Conferir com as conversas:** regra `em uso` que ninguém segue vira proposta de mensagem pronta na biblioteca ou de momento na jornada; correção que se repete e não está no arquivo vira regra nova `em teste`.
6. **Conferir conflitos** com a ficha (pergunte qual vale) e com a ética (explique e proponha a versão que cabe).

Mostre a tabela de mudanças, aplique com o ok, suba a `versao` do arquivo e atualize `revisado_em`. Nenhuma linha é apagada.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Relatório da auditoria | `escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD.md` |
| Tempos do script (opcional) | `escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD-tempos.csv` |
| Propostas aprovadas para a biblioteca, a jornada e o glossário | `escritorio/04-base/relacionamento-com-o-cliente/` (`biblioteca-de-mensagens.md`, `jornada-<tipo-de-caso>.md`, `glossario-do-cliente.md`) |
| Propostas aprovadas para as fichas | `escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`, com versão e linha no histórico |
| Propostas aprovadas e revisão dos aprendizados | `escritorio/04-base/comum/aprendizados-experiencia.md` |
| Carteira | `escritorio/07-operacao/experiencia/carteira.csv`, só as linhas aprovadas |
| Treino | `escritorio/07-operacao/_treino/experiencia/auditorias/` |

As conversas não são gravadas: só os trechos que entram no relatório. Sem pasta aberta: o relatório sai no chat, com o caminho onde ficaria, e as mudanças aprovadas saem em blocos para colar no Projeto.

## 8. Solo e equipe

**Solo:** o advogado audita a si mesmo. Dez conversas, uma hora por mês. O achado mais comum é o intervalo sem notícia: quem atende sozinho responde quem pergunta e esquece quem não pergunta. A proposta costuma ser de rotina (o ciclo diário) e de jornada.

**Equipe:** o relatório vai para a reunião mensal junto com o painel e a pesquisa. Achados por conversa, nunca por pessoa; se um padrão é de uma pessoa só, o advogado conversa em particular. Quem atende participa da revisão dos aprendizados.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Auditar só as conversas boas | Falsa tranquilidade | Amostra pela carteira, com insatisfeitos, além da régua e decisões |
| Medir só a velocidade | Resposta rápida e errada passa | Nove critérios, conteúdo depois do tempo |
| Contar como "sem notícia" quem recebeu ligação | Achado falso | Cruzar com a carteira e o histórico |
| Conversa crua no relatório | Dado de cliente exposto | Anonimizar antes; conversa não é gravada |
| Culpar a pessoa | Equipe esconde a conversa no mês seguinte | Achado por conduta; padrão vira ajuste de método |
| Ajuste aplicado sem ok | Ficha e jornada mudam sem dono | Decisão item por item |
| Aprendizados que crescem sem fim | Regras repetidas e contraditórias | Revisão mensal com as conversas como prova |

## 10. Próximo passo

- Notícia ruim dada por mensagem, cliente sem notícia: `status-para-o-cliente` (se instalada).
- Insatisfação achada na conversa: `reclamacao-e-recuperacao` (se instalada).
- Momento novo na régua: `jornada-do-cliente` (se instalada).
- Pergunta com resposta de IA mal tratada: `cliente-com-ia` (se instalada).
- Números da carteira para ler junto: `painel-da-carteira` (se instalada).
- Campo novo na ficha: `/motor-experiencia:ficha`.

Se a habilidade indicada não estiver instalada, deixe a proposta no relatório para a pessoa aplicar à mão.

## Referências desta habilidade

- `references/criterios-da-auditoria.md`: os nove critérios, a régua de cada um, frases típicas, gravidade e o uso do script. Leia nos passos 3 e 4.
- `references/revisao-dos-aprendizados.md`: o passo a passo da revisão mensal, com exemplo. Leia no passo 9.
- `assets/relatorio-modelo.md`: o modelo do relatório e o exemplo com a carteira fictícia. Use no passo 8.
- `scripts/tempos.py`: tempos de resposta e intervalos sem notícia. Rode no passo 3.
