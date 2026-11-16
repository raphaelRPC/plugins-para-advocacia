# Critérios da auditoria comercial

Dez critérios, sempre nesta ordem, e a linha vermelha, que vale em todos. Para cada um: a régua (os campos das fichas e as regras do plugin), o que conferir, frases típicas, o que não é achado e a gravidade de partida. A gravidade sobe um nível quando o mesmo achado já estava na auditoria anterior.

As frases típicas servem para reconhecer o problema. Nenhuma lista é fechada, e nenhuma frase vale como achado sem o contexto da conversa. Quando existir `nicho.md`, acrescente as frases de risco do nicho (seção "O que este nicho pesquisa sozinho" e "Cuidados do nicho").

## 1. Tempo até a primeira resposta

**Régua:** C: `primeira_resposta_contato_novo` (horas úteis) · E: `horario_de_atendimento` · registro: `primeira_resposta` (`../../../docs/funil.md`, regra 1).

**Conferir:**
- A primeira resposta de uma pessoa ao contato novo. A automática não conta.
- Cada vez que o contato escreveu e esperou.
- O "recebi, te retorno até as 16h": o retorno saiu até as 16h?
- Urgência da ficha (benefício cortado, data próxima): esperou mais do que o caminho de urgência permite?
- No registro: `primeira_resposta` vazia em `novo` ou `triado` além do prazo (o `registro.py` lista); conversa com resposta e registro vazio (alguém respondeu e não anotou).

**Com os scripts** (da pasta de trabalho; `<PASTA DA HABILIDADE>` é a pasta deste SKILL.md):
```
python3 "<PASTA DA HABILIDADE>/scripts/tempos.py" conversas/*.txt --equipe "SECRETARIA,ADVOGADA" \
  --automatico "AUTOMATICO" --prazo-horas [PRAZO] --maximo-retornos [MÁXIMO] \
  --horario [HH:MM-HH:MM] --dias seg-sex --hoje AAAA-MM-DD \
  --csv escritorio/07-operacao/comercial/auditorias/AAAA-MM-DD-tempos.csv
```
- Um arquivo .txt por conversa, com o código no nome. `--equipe` leva os nomes que a anonimização deu a quem responde pelo escritório.
- O script não lê feriado. Mês com feriado: confira à mão as esperas que cruzaram o feriado.
- Ele mede tempo, não conteúdo: "ok" em 5 minutos conta como resposta. A leitura do critério 8 corrige isso.
- Arquivos dentro de `_treino` só com `--treino`.

**Sem o script:** para cada vez que o contato escreveu, conte as horas dentro do horário até a próxima mensagem de uma pessoa. Mensagem das 21h respondida às 9h30 do dia seguinte: 30 minutos úteis.

**Gravidade:** média quando estoura o prazo; alta quando o contato não voltou a escrever, quando era urgência ou quando o "te retorno até" foi descumprido.

## 2. Convite em vez de orientação

**Régua:** regras do plugin (ética, item 2) · E: `nao_tratamos_por_mensagem` · etapa no registro (antes de `fechado`, não é cliente).

**Conferir:** resposta a "tenho direito?", "o que eu faço?", "quanto recebo?", "qual o prazo?" que responde a pergunta em vez de convidar para a consulta. Também a resposta que confirma ou desmente o que um vídeo, um site ou outra IA disse ao contato.

**Frases típicas:** "você tem direito a ...", "o prazo para entrar é de ...", "pode pedir ... no INSS", "não assina nada", "nesse caso cabe ...", "a IA está certa", "essa revisão não existe".

**Não é achado:** dizer que o escritório atende a área, explicar como funciona a consulta, listar o que trazer para a consulta, dar o caminho de emergência (190, 180, 188, 192).

**Gravidade:** crítica.

## 3. Promessa de resultado ou de prazo

**Régua:** regras do plugin (ética, item 1) · E: `frases_que_nunca_usamos`.

**Frases típicas:** "seu caso é ganho", "isso é tranquilo", "com certeza você tem direito", "em uns 30 dias resolve", "o juiz vai dar", "a chance é muito boa", "você vai receber uns R$ ...", "é rapidinho".

**Não é achado:** explicar etapas sem prometer data, ou dar o prazo de algo que o próprio escritório controla ("a proposta sai até sexta").

**Gravidade:** crítica.

## 4. Valor por mensagem

**Régua:** C: `informa_valor_da_consulta_por_mensagem`, `valor_da_consulta`, `modelo`, política de honorários do escritório · regras do plugin (ética, item 4).

**Conferir:**
- Valor de ação, de causa ou de honorário dito por mensagem a quem ainda não fez consulta.
- Valor da consulta dito quando a ficha diz que não informa por mensagem, ou dito a quem está em situação de vulnerabilidade.
- Negociação de preço por mensagem fora da política: contraproposta, "faço por menos", "quanto você pode pagar?".
- Faixa ou média ("uns 3 a 5 mil", "a partir de").

**Não é achado:** o valor da consulta quando a ficha manda informar; a proposta escrita enviada pelo modelo `envio-de-proposta`, depois da consulta.

**Gravidade:** alta; crítica quando é valor de ação antes da consulta ou valor a pessoa vulnerável.

## 5. Pressão e escassez

**Régua:** regras do plugin (ética, item 3, e "Como escrever": sem tom de venda, sem escassez ou urgência falsa).

**Conferir:** urgência que não existe no caso, prazo de oferta, "vagas" que acabam, desconto como isca, culpa, insistência para fechar na hora.

**Frases típicas:** "só até sexta", "últimas vagas", "só restam duas consultas este mês", "se fechar hoje eu consigo um desconto", "depois o valor sobe", "não deixa para depois que você vai se arrepender", "todo mundo que esperou perdeu".

**Não é achado:** avisar um prazo real do caso que o advogado conferiu ("o prazo para recorrer vence dia X, conferido pela advogada"); dizer a validade da proposta que a ficha define (`validade_da_proposta`), sem pressão.

**Gravidade:** alta; crítica quando a pressão vai para quem está em situação de vulnerabilidade.

## 6. Falar de colegas

**Régua:** regras do plugin (ética, item 3: sem comparação com outros escritórios) · C: `diferenciais_verdadeiros`.

**Conferir:** comparação com outro escritório ou advogado, crítica ao trabalho de um colega, "aqui é melhor", resposta ao "o outro cobra metade" que fala do outro.

**Frases típicas:** "aquele escritório nem tem experiência", "o outro advogado errou", "esses escritórios baratos", "a gente é o melhor da cidade".

**Não é achado:** dizer o que o escritório faz de fato (`diferenciais_verdadeiros`), sem citar ninguém.

**Gravidade:** alta.

## 7. Régua respeitada

**Régua:** C: `follow_up` (dias corridos por situação), `maximo_de_retornos` · `../../../docs/funil.md`, regras 2 (régua armada na triagem), 3 (dias corridos), 4 (marcador de pessoa) e 5 (fora da régua).

**Conferir:**
- Retornos fora dos dias da régua (cedo demais, ou com intervalo menor que o combinado).
- Mais retornos do que o `maximo_de_retornos` (o `tempos.py` conta os retornos seguidos sem resposta; o `registro.py` aponta "retorno N de M" fora do combinado).
- Retorno a quem fica fora da régua: caso sensível (violência, criança, risco), fora da área, urgência alta sem pessoa, quem pediu para parar, e quem tem o `proximo_passo` começando por `pessoa agora:` ou `pessoa liga:`.
- Contato com uma pessoa e sem conversa registrada: marcador de pessoa com a data vencida (o `registro.py` aponta). A ligação aconteceu e ninguém contou ao comando `fila`, ou não aconteceu. A saída é o comando `fila`, que grava a `primeira_resposta` e troca o `proximo_passo` pelo combinado (`../../../docs/agentes-e-fila.md`).
- Último retorno sem a mensagem de encerramento educada.
- Retorno que repete a mesma mensagem em todas as vezes.

**Gravidade:** média; alta quando passa do máximo, quando é contato fora da régua ou quando há contato com uma pessoa sem conversa registrada; crítica se esse contato tinha sinal de violência ou risco.

## 8. Contatos que sumiram sem retorno

**Régua:** C: `primeira_resposta_contato_novo`, `follow_up` · registro de contatos.

**Conferir:**
- Conversa que termina com mensagem do contato, sem resposta de pessoa (o script marca "termina sem retorno").
- Resposta que não responde: "ok", "vou ver", sem prazo e sem volta.
- Registro: contato em `novo` ou `triado` sem `primeira_resposta`, ou com retorno vencido.
- Cruzamento: `perdido` por `sem-resposta`, mas a última mensagem da conversa foi do contato (quem sumiu foi o escritório).

**Gravidade:** alta para contato novo; crítica se a mensagem sem retorno tinha sinal de alerta.

## 9. Quem pediu para parar

**Régua:** registro: `pediu_para_parar` · `../../../docs/funil.md`, regra 5 (fora da régua) · modelo `confirmacao-parar`.

**Conferir:**
- Mensagem do escritório depois da confirmação do pedido (o `tempos.py` marca "escreveu depois da confirmação").
- Pedido de parar na conversa sem `pediu_para_parar = sim` no registro.
- Contato com `pediu_para_parar = sim` e retorno ainda marcado (`registro.py`).
- Confirmação que insiste, pergunta o motivo ou oferece algo.

**Gravidade:** crítica para mensagem depois do pedido; alta para registro não marcado.

## 10. Tom e transparência

**Régua:** E: `tratamento`, `tom_em_tres_palavras`, `frase_que_soa_como_a_gente`, `frases_que_nunca_usamos`, `emoji`, `assinatura_das_mensagens` · aprendizados de tom · biblioteca comercial · regras do plugin (ética, item 5).

**Conferir:**
- Tratamento trocado no meio da conversa, frase da lista do que nunca se usa, emoji quando a ficha diz que não usa.
- Mensagem longa demais para o celular, juridiquês sem explicação, resposta seca a quem estava aflito.
- Mensagem automática que não diz que é automática, ou que assina com nome de pessoa; IA que fala como se fosse advogado.

**Frases típicas:** "prezado(a)", "conforme informado anteriormente", "fique tranquilo(a)", "querida", "aguarde nosso retorno".

**Gravidade:** média; baixa quando é só padrão (assinatura, tamanho); crítica quando o automático se passa por pessoa.

## Linha vermelha (sempre crítica, em qualquer critério)

- Sinal de violência, ameaça, risco à vida, criança em risco ou prisão respondido com mensagem comum, sem passagem para pessoa.
- Pessoa em situação de vulnerabilidade tratada só por mensagem, ou com valor de consulta, sem a ligação que a ficha prevê.
- Senha, código de acesso, login do gov.br ou do Meu INSS pedidos por mensagem.
- "Não há caso" ou "não vale a pena" dito por mensagem, sem o advogado e sem ligação.
- Mensagem enviada a quem pediu para parar.
- Valor final ou estratégia do caso decididos por mensagem, sem o advogado.

## Como registrar cada achado

```
Achado [N] · [crítica | alta | média | baixa] · critério [1 a 10 | linha vermelha]
Conversa: [CÓDIGO] · [contato novo | negociação] · [canal]
Trecho: "[até duas linhas, anonimizado]"
Por que importa: [a regra do plugin ou o campo da ficha, com o prefixo E ou C]
Repetido da auditoria anterior: sim | não
```
