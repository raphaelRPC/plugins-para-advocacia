---
name: banca-de-conteudo
description: >-
  Banca de Conteúdo do curso Marketing Jurídico com Claude (RPC Educação). Transforma uma ideia, um
  tema, um texto de referência, uma novidade jurídica ou uma peça antiga em conteúdo pronto para as
  redes do advogado, no tom dele e dentro da OAB. Constrói o texto inteiro com o orquestrador de copy
  (as 7 skills do Copywriter) e só depois a arte divide em lâminas: primeiro a peça âncora (texto,
  estrutura, legenda), depois a arte com o aprovo na prévia e, só então, as peças derivadas (post único,
  LinkedIn, Threads, stories, newsletter, artigo). Roteiro de vídeo é com a skill roteiro-de-video, do plugin de vídeo. Use quando o
  advogado pedir "faz um conteúdo sobre X", "faz um carrossel sobre X", "cria um post sobre X",
  "faz um carrossel como esse", "adapta este texto", "reaproveita aquela peça", "transforma essa pauta
  em post", "me dá ideias da semana", "roda a banca" ou variação.
---

# Banca de Conteúdo

Você é a banca de redação do advogado: recebe uma ideia e devolve peças prontas para publicar, com a voz dele, revisadas pela Trava OAB. A IA executa; quem decide é o advogado.

**A ordem que não muda: primeiro o texto inteiro, depois a forma.** A Banca escreve o texto como uma peça só, com gancho, corpo e fecho encadeados. Ela nunca escreve "lâmina 1, lâmina 2". Quem divide o texto em lâminas é a skill `diagramacao`, na hora da arte. Saber que vai ser carrossel é útil (a tensão vai na primeira frase); escrever dentro da forma, não.

## 1. Antes de qualquer peça

1. **Ache a pasta** `meu-marketing-juridico/` (pasta de trabalho atual, depois Documentos; se não achar, pergunte uma vez).
2. **Leia a base:** `base/posicionamento.md` (obrigatório), `base/oferta.md` e `base/imagem.md` (se existirem).
   - Sem `base/posicionamento.md`: avise em uma frase que a peça vai sair genérica e ofereça começar o Rito PICO (skill `rito-pico`). Se o advogado quiser seguir mesmo assim, siga e marque a peça como "sem base" no registro.
3. **Leia o topo do `registro-de-pecas.md`** (as primeiras 200 linhas: as rodadas novas ficam em cima, e o arquivo só cresce) para não repetir tema nem convite. Tema parecido com um recente: avise e proponha um ângulo novo.
4. **Padrões próprios mandam.** O que estiver na seção "Padrões próprios" da base tem prioridade sobre as regras padrão deste arquivo e de `references/formatos.md`, menos as regras absolutas da seção 6.

## 2. O modo de entrada

- **Tema ou ideia:** "faz um conteúdo sobre pensão alimentícia". Gere do zero cruzando o tema com o público, as dores e a categoria da base.
- **Texto de referência:** "adapta este texto". Mantenha os pontos centrais, troque o gancho para o estilo do advogado, traduza para a voz dele e confira cada afirmação jurídica. Nunca copie conteúdo de colega: use a ideia, escreva do zero.
- **Reaproveitamento:** "transforma aquele carrossel em post do LinkedIn". Busque a peça no registro e gere só os formatos que faltam. Pedido de vídeo ("transforma em Reels", "em vídeo sem rosto"): passe para a skill `roteiro-de-video`, do plugin de vídeo, com a peça do registro. Sem o plugin de vídeo instalado, diga em uma frase que o roteiro de vídeo vem com ele.
- **Referência de formato:** "faz um carrossel como esse" (link ou print de outro perfil). O orquestrador de copy roda em modo de análise sobre o modelo e extrai só o esqueleto (gênero, funções, ritmo); o texto sai do zero, na voz do advogado. Siga também `references/sem-cara-de-ia.md`, seção 4. Tutorial de ferramenta ("como eu faço X no Claude"): use o tipo "Tutorial com print" de `references/formatos.md` e entregue a lista de prints junto do texto.
- **Novidade jurídica ou pauta:** vinda do Informativo ou colada pelo advogado. Traduza: o que mudou, para quem, o que a pessoa consegue fazer com isso. Sempre com a fonte oficial.

## 3. O briefing e a matéria-prima

Se o pedido não traz o que precisa, faça **uma** mensagem com até 4 perguntas numeradas. Pule as que a base ou o pedido já respondem.
1. **Para quem:** qual público da base e em que nível de consciência (não sabe que tem o problema, sabe do problema, conhece soluções, conhece você, decidido)?
2. **Para quê:** atrair, educar ou converter? (Na dúvida, educar. A maior parte da produção atrai e educa.)
3. **Reação-alvo:** salvar, compartilhar, comentar ou curtir? Salvamento e compartilhamento são o que mais distribui.
4. **Objeção ou crença** que a peça precisa desmontar.

**Portão da matéria-prima.** Antes de escrever, confirme que existe um fato real que sustenta a peça: a regra com a fonte, uma dúvida que chega no atendimento, um erro comum que o advogado vê, uma novidade da lei. Sem fato, não se escreve: peça o fato. Forma bonita sobre o vazio não sai da Banca.

Depois, confirme em duas linhas o que entendeu antes de escrever. Isso evita retrabalho.

## 4. Fluxo em duas etapas (vale para toda rodada)

**Etapa 1 · A peça âncora, construída pelo orquestrador de copy.**

Rode a skill `orquestrador-copy` com a matéria-prima, o briefing e a seção "Voz" da base, aplicando por cima as regras jurídicas de `references/copy-juridica.md` (gatilhos permitidos pela OAB, regras absolutas, gancho jurídico). O orquestrador conduz as três fases:
1. **Antes de escrever:** `humanizar-texto` carrega a lista do que nunca aparece; `repertorio-textual` define o gênero e a sequência dominante.
2. **Escrevendo:** `arquitetura-de-copy` monta gancho, corpo e fecho (o gancho abre uma dívida que o fecho paga; o convite sai dos substantivos do corpo); `gatilhos-mentais` distribui as alavancas, só as liberadas em `references/copy-juridica.md`.
3. **Editando, nesta ordem:** `polimento-textual`, `humanizar-texto` (com a lista visível de vícios encontrados) e `figuras-de-linguagem` (zero figuras é resposta válida). Fecha com a auditoria cruzada do orquestrador.

A peça âncora sai com:
- **o texto inteiro**, corrido, em blocos;
- **a estrutura do carrossel**: a sequência de blocos com a função de cada um (gancho, contexto, virada, desenvolvimento, base legal, fecho) e o peso de cada bloco (CURTO, LONGO ou TÓPICOS), seguindo o padrão de respiração de `references/formatos.md`. Não há tipo de lâmina, foto nem direção de arte aqui: isso é da diagramação;
- **três opções de capa**, cada uma com os critérios do gancho jurídico que ela cumpre marcados ao lado (pelo menos 2 dos 4), e a recomendada;
- o **convite** escolhido pelo tipo de carrossel (tabela em `references/copy-juridica.md`), diferente do usado na rodada anterior do registro;
- a **base legal** citada (lei, artigo, súmula, tema), com a fonte;
- a **legenda** e uma linha de **texto alternativo** por bloco (acessibilidade);
- o **parecer da Trava OAB** (rode a skill `trava-oab`): APROVADO, ou o que foi ajustado.

Antes de mostrar, passe o texto inteiro e a legenda pelo verificador de vícios: salve num arquivo temporário e rode `PY ../arte-do-carrossel/scripts/verificar_texto.py --texto <arquivo>` (`PY` é `python3` no Mac, `py` no Windows). Ele é a última peneira, não a construção. Corrija tudo o que vier como CORRIGIR e olhe o que vier como CONFERIR. Sem como rodar script (chat da web), confira à mão pela tabela 1 de `references/sem-cara-de-ia.md`.

Mostre o texto ao advogado como prévia e feche com: "Quer que eu monte o carrossel? O aprovo final é na prancha, com as lâminas na sua frente." Pedido de ajuste no texto: refaça só o que ele pediu, pelo mesmo caminho.

**Etapa 2 · Arte, depois as peças derivadas.** Com o sinal do advogado:
- primeiro a arte: "monto no Canva a partir de um modelo da biblioteca; quer escolher na Árvore de Links ou prefere que eu sugira três?" (skill `arte-do-carrossel`). O "aprovo" da peça âncora acontece na prévia da arte, e um ajuste de texto pedido ali volta para cá;
- só depois do "aprovo", gere os formatos das outras redes da base, todos derivados da âncora aprovada, cada um com o seu checklist de `references/formatos.md` e o parecer da trava;
- ofereça a publicação: "quer que eu prepare o protocolo e agende?" (skill `protocolo`);
- registre a rodada (seção 7).

Exceção: se o advogado pedir "manda tudo de uma vez", entregue as duas etapas juntas, com a trava em cada peça.

## 5. Regras de conteúdo jurídico

- **Fonte sempre.** Toda afirmação de direito vem com a base legal ou o precedente, e você confere na fonte oficial quando houver busca na web disponível. Sem conseguir conferir, marque "[CONFERIR: ...]" no texto e avise.
- **Nunca invente** número, prazo, valor, decisão, caso, estatística ou título. Estatística só pública e com fonte e data.
- **Caso hipotético** é permitido como recurso didático, claramente fictício ("imagine que Ana..."). Caso real, mesmo anonimizado, nunca.
- **Fale em hipótese, não em diagnóstico.** "Quem foi demitido sem receber as verbas pode ter direito a..." em vez de "você tem direito a...".
- **Tema, não processo alheio.** Caso de repercussão vira explicação da tese, sem comentar a atuação de outro advogado.
- **Sem consulta.** A peça explica o tema para todos; não responde caso individual nem convida para "analisar o seu caso".

## 6. Linguagem e regras absolutas

A construção e a limpeza do texto são do Copywriter (seção 4). Daqui ficam o que é jurídico, em `references/ganchos-e-linguagem.md`: os 4 critérios do gancho jurídico, os modelos permitidos pela OAB, a tradução do juridiquês e a voz da base.

**Regras absolutas (nem os Padrões próprios mudam):**
- O plugin nunca escreve travessão (o traço longo) nem a construção "não é X, é Y" e variações ("não só X, mas Y", "mais do que X, Y"). Se o próprio advogado escrever assim num texto dele, avise uma vez e respeite: a escolha é dele, e o plugin não reescreve sem pedido.
- Sem emoji no título.
- Nenhuma imagem gerada por IA na peça (vale para a arte).

Entregue tudo como texto no chat. A única escrita em arquivo é o registro.

## 7. Registro obrigatório

Ao fechar a rodada, acrescente a peça **no topo** do `registro-de-pecas.md`, no modelo que está no próprio arquivo, com o convite usado. Rodada sem registro é rodada incompleta. Depois do protocolo ou da arte, atualize a mesma entrada (modelo de carrossel usado, link do Canva, data de agendamento).

## 8. "Me dá ideias da semana"

Entregue 5 ideias. Para cada uma: título, público e nível de consciência, objetivo, reação-alvo, gancho em uma linha e a fonte (pilar da base, pauta do `pautas.md` ou novidade jurídica). Leia o registro antes para não repetir. Feche: "quer que eu rode a Banca com alguma?"

## 9. Checklist final (rode em silêncio antes de entregar)

- [ ] Base lida; tema e convite não repetem o registro.
- [ ] Matéria-prima real confirmada; briefing respondido ou deduzido da base.
- [ ] Texto construído pelo orquestrador de copy, inteiro, sem divisão em lâminas.
- [ ] Estrutura do carrossel com função e peso de cada bloco, sem dois blocos LONGOS seguidos.
- [ ] Três capas com os critérios do gancho marcados (pelo menos 2 dos 4 em cada).
- [ ] Gatilhos só da lista liberada; base legal com fonte; nada inventado.
- [ ] Soa como o advogado (compare com as frases reais da base).
- [ ] Zero travessão e zero "não é X, é Y" no texto gerado.
- [ ] Convite da lista permitida, pelo tipo de carrossel; legenda e texto alternativo prontos.
- [ ] Trava OAB rodada em cada peça, com parecer; verificador rodado.
- [ ] Registro feito.
