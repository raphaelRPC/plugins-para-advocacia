---
name: auditar-conversas-comerciais
description: >
  Audita uma amostra sorteada de conversas reais anonimizadas com contatos novos e em negociação
  contra as fichas: tempo até a primeira resposta, convite em vez de orientação, promessa, valor por
  mensagem, pressão e escassez, falar de colegas, régua de retorno respeitada, contatos que sumiram
  sem retorno, quem pediu para parar, tom. Dois scripts medem os tempos e cruzam o registro.
  Entrega o relatório com achados por gravidade, trechos anonimizados e propostas aplicadas só com
  o ok, e faz a revisão mensal dos aprendizados. Use quando o advogado disser "audita as conversas do mês",
  "confere se a equipe está respondendo certo", "a gente está insistindo demais?", "o robô está
  falando o que deve?", "revisão dos aprendizados do comercial". Não use para clientes ativos (use
  auditar-conversas do motor-experiencia) nem para os números do funil (use painel-do-funil).
---

# Auditar conversas comerciais

> Uma vez por mês, uma amostra de conversas de verdade com quem ainda não é cliente, lida contra as fichas: o que o escritório combinou que faz, e o que de fato saiu. O que aparece vira ajuste concreto na biblioteca, nas fichas, no registro e nos aprendizados.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-comercial.md`. Funil e registro: `../../docs/funil.md`. Onde gravar: `../../docs/pasta.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Aprender: `../../docs/aprender-com-o-uso.md`. Treino: `../../docs/casos-ficticios.md`.

A ficha diz "no máximo 3 retornos" e "nunca insistimos". Numa conversa de março, o contato não respondeu ao convite e recebeu quatro mensagens em duas semanas, a última com "última chance: só restam duas vagas". Noutra, quem tinha pedido para parar recebeu, uma semana depois, um lembrete de horários. Ninguém fez por mal: a régua não foi desarmada. Sem auditoria, isso só aparece quando chega a reclamação.

**Regras fixas desta habilidade:**
1. Só conversa anonimizada entra no relatório. Conversa com nome, telefone, documento ou detalhe de saúde é anonimizada antes de qualquer leitura, e a conversa bruta nunca é gravada.
2. Achado tem trecho. Nada de "o tom está insistente" sem a frase que mostra isso.
3. A auditoria aponta e propõe. Nada muda na biblioteca, nas fichas, no registro ou nos aprendizados sem o ok do advogado, item por item.
4. Achado crítico (ética, linha vermelha, quem pediu para parar, dado sensível) vai para o topo e para o advogado na hora.
5. O relatório fala de condutas e de mensagens, não de pessoas. A amostra é sorteada, e treino nunca se mistura com conversa real.

## 1. Quando usar

**Use quando:**
- Fechou o mês e o escritório quer saber se o comercial seguiu as fichas.
- O `assistente-de-primeira-resposta` (se instalado) está ligado: toda semana nas primeiras 4 semanas, depois todo mês.
- Os aprendizados comerciais passaram de 30 linhas `em uso`, ou faz um mês da última revisão.
- O `painel-do-funil` (se instalado) deixou uma pergunta aberta ("os contatos do Instagram receberam o convite?", "por que tantos sem-resposta?").
- Chegou uma reclamação de alguém que ainda não era cliente e o advogado quer ver se é caso isolado.
- A `adaptar-comercial` chamou no modo "adaptar".

**Não use quando:**
- A conversa é com cliente ativo: é a `auditar-conversas` do motor-experiencia (se instalado).
- O pedido é o que fazer com a mensagem que acabou de chegar: use `triar-contato`.
- O pedido é avaliar um colaborador: a auditoria olha mensagens contra as fichas e não serve de avaliação individual.
- O pedido é revisar uma peça de marketing ou publicação: fora do escopo.

A auditoria não roda no ciclo do agente: ela lê conversas inteiras, com o advogado conferindo o que é crítico.

## 2. Antes de começar

1. **Leia a régua:** `escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-comercial.md`, `nicho.md` (se existir), `aprendizados-comercial.md` e a biblioteca (`escritorio/04-base/comercial/biblioteca-comercial.md`).
2. **Leia a auditoria anterior** (`escritorio/07-operacao/comercial/auditorias/`), se houver. Achado que se repete sobe de gravidade.
3. **Leia o registro** (`escritorio/07-operacao/comercial/contatos.csv`) para sortear a amostra e cruzar quem ficou sem retorno, quem pediu para parar e onde a régua está.
4. **Se o assistente estiver ligado**, leia as instruções e a bateria em `escritorio/05-automacoes/assistente-de-primeira-resposta/`.
5. **Conta e treino.** Conversa real, mesmo anonimizada, só em conta profissional ou de equipe (`conta_de_ia`). Em conta pessoal: só conversa fictícia, gravando em `escritorio/07-operacao/_treino/comercial/auditorias/` e rodando os scripts com `--treino`.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `tom_em_tres_palavras`, `frases_que_nunca_usamos` · C: `primeira_resposta_contato_novo`.
- **Melhora:** as duas fichas inteiras.

Campo que falta: pergunte aquele, uma vez. Sem `primeira_resposta_contato_novo`, a auditoria mede o tempo mas não diz se está no prazo, e o relatório marca `[A DEFINIR]`. Os campos que cada critério usa estão em `references/criterios-da-auditoria.md`, com o prefixo E ou C.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Auditoria do mês | Rotina mensal | A amostra sorteada, exportada | Relatório completo e revisão dos aprendizados |
| Auditoria do assistente | Assistente ligado | As conversas automáticas da semana | Relatório curto, contra a bateria e os limites |
| Conversa avulsa | Reclamação, dúvida, caso estranho | Uma conversa colada | Os achados daquela conversa |
| Só aprendizados | Arquivo cresceu ou passou um mês | O arquivo de aprendizados | A revisão da seção 5 |
| Adaptar | A `adaptar-comercial` chamou | `nicho.md` | Frases de risco e grupos de amostra do nicho (passo 10) |

### Passo 1. Sortear a amostra
Rode o `scripts/registro.py` da pasta de trabalho (`<PASTA DA HABILIDADE>` é a pasta deste SKILL.md; no Claude Code com o plugin, `${CLAUDE_PLUGIN_ROOT}/skills/auditar-conversas-comerciais`):
```
python3 "<PASTA DA HABILIDADE>/scripts/registro.py" escritorio/07-operacao/comercial/contatos.csv AAAA-MM \
  --tamanho [10 solo | 15 a 20 equipe] --prazo-horas [PRAZO DA FICHA] --maximo-retornos [MÁXIMO DA FICHA] \
  --horario [HH:MM-HH:MM] --dias seg-sex --hoje AAAA-MM-DD
```
- O script sorteia por grupo (não fecharam, em negociação, pediram para parar, outros contatos novos) e lista o que o registro já mostra: sem resposta além do prazo, perdido por sem-resposta, pediu para parar com retorno marcado, régua fora do combinado, retorno vencido, e contato com uma pessoa (`pessoa agora:` ou `pessoa liga:`) com a data vencida e sem conversa registrada.
- Acrescente à amostra os contatos que o registro apontou como "sem resposta" e toda conversa com reclamação. Com o assistente ligado, mais 5 conversas automáticas.
- Mostre a lista: "Me exporte estas conversas, uma por arquivo, com o código no nome: C-2026-0006, C-2026-0009...".
- Saída com código 1 (registro que falta, vazio, sem coluna obrigatória, ou de treino sem `--treino`): mostre a mensagem e não monte amostra. Sem registro: peça "as 10 últimas conversas de contato novo e as 5 últimas em negociação, sem escolher".

### Passo 2. Receber e anonimizar
- Pergunte: "Vai colar aqui ou exportar? No WhatsApp, a opção é exportar a conversa sem mídia (o menu muda conforme o aparelho; conferir no celular)."
- Quem escreve pelo escritório vira a função (`SECRETARIA`, `ADVOGADA`), o contato vira `CONTATO`, a automática vira `AUTOMATICO`.
- Troque o resto pela tabela das regras: `[CLIENTE]`, `[DOC]`, `[PROCESSO]`, `[ENDEREÇO]`, `[CONTATO]`. Relato de violência ou de saúde: só a descrição ("relata agressão"), o suficiente para auditar a conduta.
- Conversa que chega sem anonimizar: avise, anonimize antes de ler, e não grave a versão original em lugar nenhum.

### Passo 3. Medir os tempos e os sinais
Rode `scripts/tempos.py` como em `references/criterios-da-auditoria.md`, critério 1. Ele devolve, por conversa, a primeira resposta de pessoa, cada espera, quem terminou sem retorno, os retornos seguidos sem resposta (contra o `maximo_de_retornos`) e se o escritório escreveu depois de confirmar um pedido para parar. Sem o script, meça à mão pelas mesmas regras.

### Passo 4. Ler cada conversa contra os critérios
Na ordem dos dez critérios de `references/criterios-da-auditoria.md`: (1) tempo até a primeira resposta, (2) convite em vez de orientação, (3) promessa, (4) valor por mensagem, (5) pressão e escassez, (6) falar de colegas, (7) régua respeitada, (8) contatos que sumiram sem retorno, (9) quem pediu para parar, (10) tom e transparência; e a linha vermelha em todos. Para cada achado: conversa, critério, trecho (até duas linhas, anonimizado), gravidade, por que importa (a regra ou o campo da ficha).

### Passo 5. Avisar o crítico na hora
Achado crítico: pare e mostre ao advogado antes de seguir, com o trecho e a pergunta: "Quer que eu prepare um rascunho para corrigir com a pessoa, para você ler e decidir?". Quem pediu para parar nunca recebe rascunho de nada: o que se corrige é o registro.

### Passo 6. Achar o padrão
Junte os achados que se repetem. Três conversas com a mesma pressão, ou com a mesma régua passando do máximo, são um padrão: a causa provável está na biblioteca, na ficha, no registro ou na rotina, e não na pessoa. Achado da auditoria anterior sobe um nível.

### Passo 7. Propor os ajustes
Cada padrão vira uma proposta concreta (formato na seção 7), num destes destinos:
- **Biblioteca comercial:** modelo novo ou trecho que muda, pela `mensagens-comerciais` (se instalada); resposta a objeção pela `objecoes-comerciais` (se instalada).
- **Fichas:** campo que falta ou não bate com a prática (frase para `frases_que_nunca_usamos`, palavra de alerta, régua que ninguém cumpre).
- **Registro:** contato sem retorno ganha próximo passo e data; quem pediu para parar ganha `pediu_para_parar = sim` e próximo passo "nenhum"; régua fora do combinado é encerrada; contato com `pessoa agora:` ou `pessoa liga:` vencido volta para a pessoa, e o combinado entra pelo comando `fila` (`../../docs/agentes-e-fila.md`, "PESSOA AGORA também sai da lista").
- **Rotina:** o que o resumo do dia precisa mostrar, pela `rotina-comercial`.
- **Aprendizados:** regra curta, com verbo e objeto, e o exemplo anonimizado.
- **Assistente** (se ligado): caso novo na bateria e correção nas instruções, com novo teste.

### Passo 8. Mostrar, aprovar item por item, gravar
Mostre o relatório. Para cada proposta: "Aplico esta? (sim, não, depois)". Aplique só o que teve sim, mostrando o trecho com `[NOVO]` ou `[ALTERADO]`. Ficha alterada: suba a versão e acrescente a linha no histórico. Grave o relatório em `escritorio/07-operacao/comercial/auditorias/AAAA-MM-DD.md`, com a coluna "decisão" preenchida.

### Passo 9. Revisão mensal dos aprendizados
Na auditoria do mês, ou no modo "só aprendizados", siga a seção 5.

### Passo 10. Modo "adaptar" (chamada pela adaptar-comercial)
1. Leia `nicho.md`: "Como ele fala", "Os momentos de aflição", "Cuidados do nicho" e "O que este nicho pesquisa sozinho".
2. Proponha as frases de risco do nicho para os critérios 2, 3 e 5 (por exemplo, no previdenciário, "a revisão é garantida"; no bancário, "o juro abusivo sempre cai"), como acréscimos a E: `frases_que_nunca_usamos`, e os sinais do nicho para E: `palavras_de_alerta`.
3. Proponha os grupos da amostra que fazem sentido para o nicho (por exemplo, "quem pediu revisão vista em vídeo").
4. Mostre cada mudança marcada `[ALTERADO]` ou `[NOVO]`, grave na ficha só com o ok, e devolva a lista do que mudou.

### Passo 11. Aprender
Pergunte: "Algum achado você não considera erro aqui no escritório?". A resposta ajusta a régua: vira aprendizado ("Retorno por ligação a quem pediu ligação não conta na régua de mensagens") ou campo da ficha. Se o advogado discordar de um achado ético, explique a regra do plugin e não guarde a exceção (`../../docs/aprender-com-o-uso.md`, regra 5).

## 4. Gravidade

| Gravidade | O que entra | O que acontece |
|---|---|---|
| **Crítica** | Orientação jurídica a quem não é cliente; promessa de resultado ou prazo; valor de ação antes da consulta; mensagem depois do pedido para parar; sinal de violência, risco, prisão ou vulnerabilidade sem passagem para pessoa; senha ou dado sensível pedido; automático que se passou por pessoa; pressão sobre pessoa vulnerável | Aviso ao advogado na hora. Proposta obrigatória |
| **Alta** | Contato novo sem retorno; urgência que esperou além do prazo; "te retorno até" descumprido; negociação de preço fora da política; escassez falsa ou desconto como isca; comparação com colegas; retornos acima do máximo; retorno a contato fora da régua; pedido de parar não marcado no registro | Proposta obrigatória. Volta na próxima auditoria |
| **Média** | Prazo estourado sem dano visível; régua fora dos dias combinados; tom fora da ficha; frase da lista do que nunca se usa | Proposta quando for padrão |
| **Baixa** | Assinatura, tamanho, termo técnico sem explicação, falta de padrão entre pessoas | Só no resumo, se for padrão |

## 5. Revisão mensal dos aprendizados

Segue `../../docs/aprender-com-o-uso.md`, seção "Revisão", com as conversas como prova. O passo a passo e os exemplos estão em `references/revisao-dos-aprendizados.md`. Em resumo: juntar repetidas; subir para a ficha o que virou política (a linha fica `retirada`, com "incorporada à ficha: [campo]"); retirar o que não vale mais; decidir as `em teste` com mais de 30 dias; conferir com as conversas (regra que ninguém segue vira proposta de modelo ou de rotina, não regra nova); conferir conflitos com a ficha e com a ética. Mostre a tabela de mudanças, aplique com o ok, suba a `versao` e atualize `revisado_em`. Nenhuma linha é apagada.

## 6. Exemplo resolvido (Escritório Modelo, fictício)

Auditoria de 2026-04-02, conversas de 03/2026. O `registro.py` sorteou 10 conversas e apontou o C-2026-0011 sem resposta. O `tempos.py` mostrou: C-2026-0011 termina sem retorno há 137,2 h úteis (só a automática respondeu); C-2026-0014 com 4 retornos seguidos sem resposta, acima do máximo de 3; C-2026-0009 com uma mensagem depois da confirmação do pedido para parar.

Na leitura: o C-2026-0009 (Antônio, caso 9) recebeu "Oi! Passando para lembrar que ainda temos horários de consulta esta semana" uma semana depois de pedir para parar: crítica, avisada à advogada na hora. O C-2026-0006 (Sérgio, caso 6, negociação) recebeu "Aquele escritório nem tem a experiência que a gente tem" e "Se fechar hoje eu consigo 20% de desconto": falar de colegas, escassez e desconto como isca, altas. O C-2026-0014 recebeu "Última chance: só restam duas vagas de consulta este mês!" no terceiro retorno: pressão e régua passando do máximo.

Propostas aprovadas: régua encerrada no registro para quem pediu para parar e para o contato fora da área; aprendizado "Depois da confirmação de parar, nenhuma mensagem, nem lembrete de horário"; quatro frases novas em `frases_que_nunca_usamos`; resposta a "achei caro" pela `objecoes-comerciais`; o resumo da `rotina-comercial` passa a listar todo contato com `primeira_resposta` vazia. O relatório completo está em `assets/relatorio-modelo.md`.

## 7. Formato da saída

O relatório segue `assets/relatorio-modelo.md`: cabeçalho, amostra e régua, resumo em cinco linhas, tempos, o que o registro já mostrava, achados por gravidade (críticos primeiro), comparação com a anterior, propostas com a coluna de decisão, revisão dos aprendizados, linhas do registro e a próxima auditoria. Cada achado usa o bloco do fim de `references/criterios-da-auditoria.md`. Cada proposta usa este:

```
Proposta [N] · [biblioteca | ficha do escritório | ficha comercial | registro | rotina | aprendizados | assistente]
Achados: [números dos achados]
O que muda: [o texto atual] > [o texto proposto]
Por quê: [o padrão, com quantas conversas]
Decisão: sim | não | depois   (preenchida pelo advogado)
```

## 8. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Relatório (achados, propostas, decisões, revisão dos aprendizados) | `escritorio/07-operacao/comercial/auditorias/AAAA-MM-DD.md` |
| Tempos medidos pelo script | `escritorio/07-operacao/comercial/auditorias/AAAA-MM-DD-tempos.csv` |
| Propostas aprovadas para a biblioteca | `escritorio/04-base/comercial/biblioteca-comercial.md` |
| Propostas aprovadas para as fichas | `escritorio/04-base/comum/ficha-do-escritorio.md` ou `ficha-comercial.md`, com versão e histórico |
| Propostas aprovadas e revisão dos aprendizados | `escritorio/04-base/comum/aprendizados-comercial.md` |
| Linhas do registro aprovadas | `escritorio/07-operacao/comercial/contatos.csv` |
| Caso novo para o assistente (se ligado) | `escritorio/05-automacoes/assistente-de-primeira-resposta/bateria-de-teste.md` |
| Treino | `escritorio/07-operacao/_treino/comercial/auditorias/` |

As conversas não são gravadas, nem anonimizadas: só os trechos que entram no relatório. Sem pasta aberta: o relatório sai no chat, com o caminho onde ficaria, e as mudanças aprovadas saem em blocos para colar.

## 9. Solo e equipe

**Solo:** o advogado audita a si mesmo. Dez conversas, uma hora por mês. Os achados mais comuns são o tempo (quem atende sozinho responde em rajadas) e a régua que não para. A proposta costuma ser de rotina (dois horários fixos de resposta) e de registro (pedido de parar desarma tudo na hora).

**Equipe:** o relatório vai para a reunião mensal do comercial junto com o painel. Achados aparecem por conversa, nunca por pessoa; se um padrão é de uma pessoa só, o advogado conversa em particular, fora do relatório. Quem atende participa da revisão dos aprendizados: é ela que sabe por que a regra não pegou.

## 10. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Auditar só as conversas boas | Falsa tranquilidade | Amostra sorteada pelo registro, com perdidos e quem pediu para parar |
| Achado sem trecho | Discussão de impressão, nada muda | Trecho anonimizado em todo achado |
| Conversa crua no relatório | Dado de cliente exposto | Anonimização antes da leitura; conversa não é gravada |
| Régua que não para | Incômodo, reclamação, risco ético | Critérios 7 e 9, com o script contando retornos e mensagens depois do pedido |
| Pressão e escassez que viram hábito | Comercial com tom de venda | Critério 5, com as frases que a ficha passa a proibir |
| Culpar a pessoa | Equipe esconde a conversa no mês seguinte | Achado por conduta; padrão vira ajuste |
| Ajuste aplicado sem ok | Ficha e biblioteca mudam sem dono | Decisão item por item |
| Script que não leu nada e diz que está tudo bem | Auditoria vazia | Os dois scripts saem com erro quando não leem nada |

## 11. Próximo passo

- Proposta de biblioteca aprovada: `mensagens-comerciais` (se instalada) reescreve e guarda o modelo no tom da ficha; resposta a objeção, `objecoes-comerciais` (se instalada).
- Contatos sem retorno: `follow-up` (se instalada), só com quem não pediu para parar, ou `triar-contato` para registrar o próximo passo.
- Resumo do dia que precisa mostrar mais: `rotina-comercial`.
- Achado no assistente: `assistente-de-primeira-resposta` (se instalada), modo "depois de erro" ou "testar de novo".
- Números do mês para ler junto: `painel-do-funil` (se instalada).

Se a habilidade indicada não estiver instalada, diga em uma linha o que ela faria e deixe a proposta no relatório para a pessoa aplicar à mão.

## Referências desta habilidade

- `references/criterios-da-auditoria.md`: os dez critérios, a linha vermelha, frases típicas, gravidade e o uso dos scripts. Leia nos passos 3 e 4.
- `references/revisao-dos-aprendizados.md`: o passo a passo da revisão mensal, com exemplos. Leia no passo 9.
- `assets/relatorio-modelo.md`: o modelo do relatório e o exemplo completo do Escritório Modelo. Leia no passo 8.
- `scripts/registro.py`: sorteio da amostra e achados do registro. Rode no passo 1.
- `scripts/tempos.py`: tempos, retornos seguidos e mensagens depois do pedido para parar, nas conversas exportadas. Rode no passo 3.
