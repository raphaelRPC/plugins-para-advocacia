# Catálogo de rotinas

Cada rotina vira um arquivo em `rotinas/` na pasta do advogado. O modelo de cada uma está abaixo: preencha `{CAMINHO}` (caminho completo de `meu-marketing-juridico`), `{NOME}` e os demais campos com a base. Todas seguem as regras da seção 4 do `SKILL.md` e terminam com o resumo de até 5 linhas.

| Rotina | Quando (sugestão) | O que faz por você | O que você aprova | Precisa de |
|---|---|---|---|---|
| Informativo da manhã | Dias úteis, 7h30 | Pautas novas com fonte oficial; painel atualizado | Escolher a pauta (ou deixar para a Pauta da semana) | Busca na web |
| Pauta da semana | Segunda, 8h | Escolhe as melhores pautas e prepara as minutas da semana | Cada minuta, depois o pacote pronto | Base completa |
| Ilha de edição (precisa do plugin de vídeo) | Todo dia, 20h | Prepara os vídeos novos de `videos/crus/` (transcrição, revisão da fala) e deixa a prancha de cada um pronta | A prancha do vídeo (depois do seu "sim", o vídeo editado) | Ferramentas de edição instaladas |
| Conferência da fila | Dias úteis, 18h | Confere o que está agendado nos próximos 3 dias e avisa buracos ou falhas | O alerta, se houver | Agendador (ou o registro) |
| Balanço da semana | Sexta, 17h | Resultados, comparação com a meta, uma recomendação e pautas de continuidade | Nada (é leitura); as pautas entram na fila | Métricas (agendador ou prints) |
| Newsletter da semana | Quinta, 9h | Rascunho da newsletter com o melhor conteúdo da semana | O rascunho | Lista própria de inscritos |
| Revisão trimestral | A cada 90 dias | Propõe ajustes na base a partir do que funcionou | A proposta de base | 3 meses de registro |
| Vigia OAB | Dia 1 de cada mês | Confere se houve mudança nas regras de publicidade da OAB | O alerta, se houver | Busca na web |

---

## Informativo da manhã

Use o modelo de `../../informativo-diario/references/modelo-rotina.md`. Acrescente ao fim: "Se houver pauta com novidade das últimas 24 horas e alta relevância para o público, crie um item de alerta na caixa de aprovação sugerindo produzir hoje."

## Pauta da semana

```markdown
Você executa a Pauta da semana de {NOME}. Pasta: {CAMINHO}.
1. Leia base/posicionamento.md, base/oferta.md, registro-de-pecas.md, pautas.md e a caixa aprovacoes/.
2. Escolha {N} pautas para a semana, equilibrando: objetivo (maioria atrair e educar), públicos da base e pelo menos uma pauta de continuidade, se houver. Nunca repita tema do registro nem duplique minuta já na caixa.
3. Para cada pauta, rode a Banca de Conteúdo SÓ na Etapa 1 (texto inteiro da peça âncora com a estrutura em blocos, três capas, convite, legenda, base legal com fonte e parecer da trava OAB). Não gere derivadas.
4. Grave cada minuta como item na caixa: aprovacoes/AAAA-MM-DD-minuta-<tema>.md, status aguardando. Marque as pautas como usadas em pautas.md.
Nunca publique, agende ou envie nada.
```

## Ilha de edição

```markdown
Você executa a Ilha de edição de {NOME}. Pasta: {CAMINHO}.
1. Liste os vídeos em videos/crus/ que ainda não têm versão em videos/editados/.
2. Nenhum vídeo novo: encerre com "nenhum vídeo novo".
3. Para cada vídeo novo, siga a skill edicao-de-video até a prancha: transcreva, prepare, revise a fala e gere a prancha do vídeo. Sem o advogado para escolher no Catálogo, poupe o plano: se o arquivo vier com um pedido do Catálogo ao lado (mesmo nome, terminado em .pedido.txt) ou se houver favorito em base/edicao-memoria.json, use o pedido ou o último favorito como visual travado e gere a prancha curta (só momentos e fatos); sem nenhum dos dois, gere a prancha completa (formato sugerido pelo roteiro e alternativas). Se o nome do arquivo ou a transcrição baterem com um roteiro do registro-de-pecas.md, use o roteiro para conferir a fala e a legenda. Não monte o vídeo: a montagem só acontece depois que o advogado colar as escolhas da prancha.
4. Rode a trava OAB nos textos das peças oferecidas na prancha.
5. Crie um item por vídeo na caixa: aprovacoes/AAAA-MM-DD-prancha-<tema>.md, com o caminho da prancha.html, a duração depois dos cortes e o visual usado (favorito, pedido ou formato sugerido). Status aguardando.
Nunca publique nem apague o vídeo cru.
```

## Conferência da fila

```markdown
Você executa a Conferência da fila de {NOME}. Pasta: {CAMINHO}. Agendador: {CONEXAO_AGENDADOR}.
1. Leia os agendamentos dos próximos 3 dias (agendador conectado) ou o campo Protocolo do registro-de-pecas.md.
2. Confira: algum dia útil sem publicação, considerando a meta de {PECAS_SEMANA} peças por semana? Algum agendamento com erro ou mídia inacessível?
3. Se houver buraco: crie um item de alerta na caixa sugerindo qual pacote aprovado ou minuta aguardando pode cobrir o dia. Se houver falha: alerta com o que houve e a correção proposta.
Nunca agende, publique ou altere agendamento.
```

## Balanço da semana

```markdown
Você executa o Balanço da semana de {NOME}. Pasta: {CAMINHO}. Métricas: {CONEXAO_METRICAS}.
1. Leia os resultados dos últimos 7 dias (agendador conectado) ou os prints que estiverem em acervo/metricas/.
2. Compare cada peça com a reação-alvo dela (peça para salvar se mede por salvamentos) e com a média das últimas 4 semanas. Compare a produção com a meta de 90 dias.
3. Escreva acervo/balancos/AAAA-MM-DD.md: o que funcionou, o que não funcionou, o placar da meta e UMA recomendação prática.
4. Proponha até 3 pautas de continuidade (peças 30% acima da média) no topo de pautas.md.
Nunca invente número; sem dado, diga "sem dados nesta semana".
```

## Newsletter da semana

```markdown
Você executa a Newsletter da semana de {NOME}. Pasta: {CAMINHO}.
1. Leia o registro-de-pecas.md dos últimos 7 dias e a base.
2. Escreva o rascunho: 2 opções de assunto, abertura em 2 frases, o tema da semana explicado, uma dica prática, link para a peça do feed, identificação (nome, OAB/UF) e lembrete de descadastro.
3. Rode a trava OAB (newsletter só para inscritos, sem oferta de serviço).
4. Grave na caixa: aprovacoes/AAAA-MM-DD-newsletter.md, status aguardando.
Nunca envie.
```

## Revisão trimestral

```markdown
Você executa a Revisão trimestral de {NOME}. Pasta: {CAMINHO}.
1. Leia a base inteira, o registro dos últimos 90 dias e os balanços em acervo/balancos/.
2. Identifique: temas, formatos e ganchos que mais funcionaram; públicos que responderam mais; padrões novos de construção.
3. Proponha alterações concretas na base (seção, texto atual, texto proposto, por quê). Sem dado suficiente, proponha manter.
4. Grave na caixa: aprovacoes/AAAA-MM-DD-proposta-base.md, status aguardando.
Nunca altere a base sem aprovação.
```

## Vigia OAB

```markdown
Você executa o Vigia OAB de {NOME}. Pasta: {CAMINHO}.
1. Busque em fontes oficiais (oab.org.br e o Diário Eletrônico da OAB) se houve, no último mês, alteração do Provimento 205/2021, do seu Anexo Único, do Código de Ética nos artigos de publicidade, ou nova orientação do Comitê Regulador do Marketing Jurídico.
2. Sem mudança confirmada: encerre com "sem mudança nas regras de publicidade".
3. Com mudança: crie um item de alerta na caixa com o link oficial, o que mudou em linguagem simples e quais regras da trava podem ser afetadas. A atualização das regras do plugin é feita pela equipe do curso; avise o advogado para conferir as atualizações do plugin.
Nunca altere as regras da trava por conta própria.
```
