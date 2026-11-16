# Mensagens da agenda (reserva)

A `agenda-da-consulta` tira as mensagens da biblioteca comercial do escritório (`escritorio/04-base/comercial/biblioteca-comercial.md`), pela chave. Este arquivo é a reserva para quando a biblioteca ainda não existe ou não tem a chave: os mesmos textos crus da `mensagens-comerciais`, com as mesmas chaves. A habilidade escreve no tom das fichas antes de mostrar e oferece guardar na biblioteca pela `mensagens-comerciais` (se instalada).

Tudo aqui é A: quem cuida da agenda lê e envia. O "Antes de enviar" é interno e nunca vai para o contato.

Os colchetes a habilidade preenche com a ficha e o registro; nada entre colchetes vai ao contato. Entre chaves fica o que quem envia preenche na hora, de propósito: o horário que alguém conferiu na agenda (`{DIA E HORA}`, `{OPÇÃO 1}`) e o link da videochamada (`{LINK DA VIDEOCHAMADA}`). A fila não deixa marcar `enviado` com chave no texto.

## `confirmacao-de-consulta`
- **Antes de enviar (interno):** o horário está confirmado na agenda; o "o que trazer" não pede laudo, documento de criança, senha ou acesso a sistema; o valor só aparece se `informa_valor_da_consulta_por_mensagem` permite.
```
[NOME], sua consulta está marcada:

Dia: {DIA E HORA}  (ou o dia e a hora escritos, se a pessoa já conferiu na agenda)
Onde: [ENDEREÇO OU "por vídeo; o link vai na véspera"]
Com: [QUEM FAZ A CONSULTA]
Duração: cerca de [DURAÇÃO]
O que trazer: [LISTA CURTA]

Se precisar remarcar, me avise por aqui com antecedência, combinado?

[ASSINATURA]
```

## `lembrete-de-consulta`
- **Antes de enviar (interno):** a consulta continua na agenda; a pessoa não pediu para parar; o horário do envio é o de `confirmacao_e_lembrete`.
```
VÉSPERA
Oi, [NOME]! Passando para lembrar da sua consulta amanhã, [DATA], às [HORA], [ONDE].
Pode me confirmar que está tudo certo? Se surgir algum imprevisto, me avise por aqui que a gente remarca.

NO DIA (consulta online)
[NOME], sua consulta é hoje às [HORA]. O link é este: {LINK DA VIDEOCHAMADA}. Vale entrar uns minutos antes para testar câmera e áudio.
```

## `remarcacao`
- **Antes de enviar (interno):** os candidatos sugeridos pela habilidade (seção 4.1 da `agenda-da-consulta`); cada horário que entrar no lugar das chaves foi conferido na agenda; a regra de `remarcacao` da ficha está respeitada (quantas vezes, com ou sem custo).
```
QUANDO O CONTATO PEDE
Sem problema, [NOME]. Tenho estes horários:
* {OPÇÃO 1}
* {OPÇÃO 2}
* {OPÇÃO 3}
Qual fica melhor para você? Assim que você escolher, te mando a confirmação.

QUANDO O ESCRITÓRIO PRECISA REMARCAR
[NOME], preciso te pedir para remarcar a consulta de [DATA], por [MOTIVO CURTO]. Peço desculpas pelo transtorno.
Tenho estes horários: {OPÇÕES}. Algum serve para você?

DEPOIS DA FALTA
Oi, [NOME]. Sentimos sua falta na consulta de [DATA]. Imprevisto acontece.
Se ainda quiser conversar, tenho estes horários: {OPÇÕES}. É só me dizer qual fica melhor.
```

## Variação com link de agenda
Quando `como_agenda` é um link que o próprio contato usa, troque a lista de opções por:
```
Você escolhe o horário que for melhor por aqui: [LINK DA AGENDA, DA FICHA]. Assim que marcar, me avise que eu confirmo.
```
