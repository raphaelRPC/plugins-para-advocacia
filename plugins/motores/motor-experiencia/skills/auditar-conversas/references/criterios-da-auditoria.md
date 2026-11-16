# Critérios da auditoria das conversas com clientes ativos

Nove critérios, sempre nesta ordem. Para cada um: a régua (de onde vem o combinado), o que conferir, frases típicas e a gravidade de partida. A gravidade sobe um nível quando o mesmo achado já estava na auditoria anterior.

As frases típicas são exemplos para reconhecer o problema. Nenhuma é lista fechada, e nenhuma vale como achado sem o contexto da conversa.

## 1. Tempo de resposta contra a ficha

**Régua:** `primeira_resposta_cliente_ativo`, `resposta_completa`, `resposta_ponte`, `horario_de_atendimento`.

**Conferir:**
- Cada vez que o cliente escreveu e esperou uma pessoa: o tempo em horas úteis.
- Pergunta que ficou sem retorno no fim da conversa.
- Cliente que cobrou de novo, em outro dia, sem resposta ("de novo", "e aí?", "alguma novidade?").
- A resposta-ponte ("recebi, te retorno até as 16h"): o retorno saiu até as 16h? E o "te retorno" sem hora: voltou?
- Urgência (compromisso em até 3 dias, palavra de alerta): esperou mais do que o caminho de urgência da ficha?

**Com o script:**
```
python3 "<pasta desta habilidade>/scripts/tempos.py" <pasta das conversas>/*.txt \
  --equipe "ADVOGADA,SECRETARIA" --automatico "AUTOMATICO" \
  --prazo-horas [primeira_resposta_cliente_ativo, em horas úteis] --horario [HH:MM-HH:MM] --dias seg-sex \
  --maximo-sem-noticia [maximo_sem_noticia, em dias] --hoje "AAAA-MM-DD HH:MM" \
  --csv escritorio/07-operacao/experiencia/auditorias/AAAA-MM-DD-tempos.csv
```
- No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/auditar-conversas`.
- Um .txt por conversa, com o código da carteira no nome (`C-2026-0001.txt`).
- `--equipe` leva os nomes que a anonimização deu a quem responde pelo escritório; `--hoje` é a data e hora da exportação.
- Cortesia do cliente ("ok", "obrigada", figurinha) não abre espera. A automática não conta como resposta.
- O script não lê feriado. Mês com feriado: confira à mão as esperas que cruzaram o feriado.
- Ele mede tempo, não conteúdo: "vou ver" conta como resposta. A leitura corrige.
- Sem arquivo lido, ele para com erro; nunca diz que está tudo certo.

**Gravidade:** média quando estoura o prazo; alta quando o "te retorno" foi descumprido, quando o cliente cobrou de novo sem resposta, ou quando é compromisso próximo; crítica quando havia sinal de alerta na mensagem sem resposta.

## 2. Máximo sem notícia

**Régua:** `maximo_sem_noticia`, `avisa_movimentacao_relevante`, `resumo_mensal`, a jornada do tipo de caso.

**Conferir:**
- O maior intervalo sem mensagem do escritório na conversa (o script mostra, em dias corridos, contando até a data da exportação).
- Cruzar com a carteira e o `historico.md`: houve ligação, reunião, resumo ou página fora da conversa (linha de contato que informou o caso)? Se houve, não é achado. Linha de trabalho do escritório (canal `trabalho-do-escritorio`), resposta-ponte, cortesia, lembrete de documento e pesquisa não contam como notícia.
- Movimentação relevante que o cliente soube antes do escritório ("vi no site que mexeu").
- Cliente com `resumo_mensal = sim` sem resumo no mês.
- Cliente com `pediu_para_nao_receber = sim` que recebeu mensagem de rotina (é linha vermelha), ou que ficou sem notícia relevante (também é achado: a notícia relevante continua).

**Gravidade:** alta; crítica quando o cliente reclamou por isso.

## 3. Notícia ruim por mensagem

**Régua:** `nunca_por_mensagem` (notícia ruim, mudança de estratégia, proposta de acordo), `regras.md` (linha vermelha, item 2).

**Conferir:** decisão desfavorável, benefício negado, perícia contrária, proposta de acordo ou mudança de estratégia dada por mensagem, sem ligação antes registrada no histórico.

**Frases típicas:** "infelizmente foi improcedente", "o juiz negou", "perdemos", "o INSS indeferiu", "vamos ter que recorrer", "a empresa ofereceu X, aceita?".

**Gravidade:** crítica.

## 4. Promessa de prazo ou de resultado

**Régua:** `regras.md` (ética, item 1); `frases_que_nunca_usamos`.

**Conferir:** frase que diz ou dá a entender resultado, chance, valor a receber ou data de decisão do juiz, do INSS ou da outra parte.

**Frases típicas:** "seu caso é ganho", "fica tranquilo que vai dar certo", "o juiz decide essa semana", "até o fim do mês o dinheiro cai", "você vai receber uns R$ ...", "é rapidinho".

**Não é achado:** prazo que o próprio escritório controla ("te mando o resumo até sexta"); explicar a etapa sem data ("depois da perícia, o juiz decide; esse tempo depende da vara").

**Gravidade:** crítica.

## 5. Termo técnico sem explicação

**Régua:** `regras.md` (como escrever: termo técnico explicado na primeira vez); glossário do cliente (`04-base/relacionamento-com-o-cliente/glossario-do-cliente.md`), se existir.

**Conferir:** termo copiado da movimentação ou do juridiquês, sem tradução: "conclusos para despacho", "juntada", "trânsito em julgado", "improcedente", "RPV", "cumprimento de sentença", "réplica", "intimação". Explicação errada conta como critério 6 ou 4.

**Gravidade:** baixa; média quando é padrão ou quando o cliente perguntou de novo o que era.

## 6. Confirmação do que a IA ou a internet disse ao cliente

**Régua:** `regras.md` (ética, item 6): acolher, explicar, corrigir com calma, nunca confirmar sem o advogado conferir.

**Conferir:**
- O cliente trouxe resposta de IA, vídeo, site do tribunal ou "um conhecido disse", e a equipe respondeu "isso mesmo" ou repetiu a previsão.
- A equipe ridicularizou a pergunta ("isso aí é bobagem da internet").
- A correção veio sem explicação, e o cliente ficou sem entender.

**Frases típicas:** "isso mesmo", "é verdade, o juiz vai decidir essa semana", "o ChatGPT está certo", "não liga para isso".

**Gravidade:** crítica quando confirma previsão ou direito; média quando ridiculariza.

## 7. Dado sensível

**Régua:** `regras.md` (dados de cliente); a regra de uso de IA do escritório, se existir.

**Conferir:**
- Pedido de laudo, exame ou detalhe de saúde por mensagem além do necessário; pergunta sobre a doença ("ela está com o quê?").
- Dado de um cliente enviado a outra pessoa (familiar, outro cliente) sem autorização registrada.
- Documento de criança ou adolescente comentado além do necessário.
- CPF, número de benefício ou endereço repetidos na resposta sem necessidade.
- Atendimento pelo celular pessoal de alguém da equipe, quando a ficha diz número oficial.
- Vulnerabilidade (internação, luto, violência) respondida com mensagem comum, sem passagem para pessoa: é linha vermelha.

**Gravidade:** alta; crítica para dado de um cliente enviado a outro e para vulnerabilidade sem passagem para pessoa.

## 8. Senha e credencial

**Régua:** `regras.md` (dados de cliente, item 4): senha, código de acesso, certificado digital, login do gov.br ou do Meu INSS nunca entram.

**Conferir:** a equipe pediu ou enviou senha, código, login, token ou certificado, ou combinou enviar ("te mando a senha amanhã"). O cliente mandou a senha e ninguém orientou a trocar.

**Não é achado:** enviar o número do processo ao próprio cliente pelo canal oficial; oferecer a página do caso ou o resumo.

**Gravidade:** crítica.

## 9. Tom contra a ficha

**Régua:** `tratamento`, `tom_em_tres_palavras`, `frase_que_soa_como_a_gente`, `frases_que_nunca_usamos`, `emoji`, `audio`, `assinatura_das_mensagens`, aprendizados de tom, biblioteca.

**Conferir:** tratamento trocado; frase da lista do que nunca se usa; emoji quando a ficha diz que não; notícia importante só em áudio; mensagem longa demais para o celular; resposta seca a quem estava aflito ("ok", "aguarde"); "que pena" sem passar para uma pessoa.

**Gravidade:** média; baixa quando é só padrão (assinatura, tamanho).

## Linha vermelha (sempre crítica, em qualquer critério)

- Vulnerabilidade, violência, risco à vida, internação ou luto respondidos com mensagem comum, sem passagem para pessoa.
- Notícia ruim dada por mensagem, sem ligação antes.
- Reclamação respondida com mensagem pronta, sem uma pessoa assumir.
- Mensagem de rotina para quem pediu para não receber.
- Resposta automática que não disse que era automática, ou assinou como pessoa.
- Senha ou credencial pedida, combinada ou enviada.

## Como registrar cada achado

```
Achado [N] · [crítica | alta | média | baixa] · critério [1 a 9]
Conversa: [CÓDIGO] · fase [FASE] · [canal]
Trecho: "[até duas linhas, anonimizado]"
Por que importa: [a regra do plugin, o campo da ficha ou a jornada]
Repetido da auditoria anterior: sim | não
```
