# Tom, conferência e convivência com a biblioteca do cliente

Leia no passo 2 (calibrar o tom), no passo 4 (conferir) e no passo 1 quando já existir outra biblioteca de mensagens na pasta.

## 1. Da ficha para o texto

Cada campo da ficha vira uma escolha concreta na mensagem. A IA não escolhe o tom: ela traduz o que a ficha diz.

| Campo da ficha | O que muda na mensagem | Exemplo |
|---|---|---|
| `tratamento: você` | "você", "te", "seu caso" | "Quer que eu veja um horário para você?" |
| `tratamento: senhor e senhora` | "o senhor", "a senhora", "lhe"; abre com "Bom dia, Sr. {NOME}" | "O senhor prefere de manhã ou à tarde?" |
| `tratamento: pelo nome` | o primeiro nome no lugar do pronome, sem "querido" nem diminutivo | "Marta, quer que eu veja um horário?" |
| `tom_em_tres_palavras` | tamanho das frases, abertura, fecho (tabela abaixo) | |
| `frase_que_soa_como_a_gente` | ritmo e vocabulário: a mensagem nova tem que soar como se viesse da mesma pessoa | se a frase real começa com "Oi, tudo certo?", os modelos começam assim |
| `frases_que_nunca_usamos` | nenhuma aparece, nem parecida | "fique tranquilo" some, e também "pode ficar tranquila" |
| `emoji` | `não usamos`: nenhum. `com moderação`: no máximo um, só em cortesia e boas-vindas. `usamos`: o que a frase real mostrar | |
| `assinatura_das_mensagens` | o fecho de toda mensagem que não é cortesia | "Equipe Escritório Modelo" |
| `como_o_cliente_fala` e `nicho.md` | as palavras do contato entram na explicação ("encostado", "a firma") | "Entendi, o seu auxílio (o 'encostado') foi cortado." |
| `horario_de_atendimento`, `fora_do_horario`, `urgencia_vai_para` | o modelo 2 e o "quando uma pessoa responde" | |

### Palavras do tom e o que elas pedem

| Se a ficha diz | Faça | Evite |
|---|---|---|
| próximo, acolhedor | "Oi, {NOME}, tudo bem?", frases curtas, "a gente" | intimidade que o escritório não tem ("querida", "meu bem") |
| formal, sóbrio | "Bom dia, {NOME}.", frases completas, "nós" | "Prezado(a)" se a ficha não usar; juridiquês |
| claro, direto | uma informação por linha, lista com asterisco | parágrafo de abertura longo antes do que importa |
| sem pressa, calmo | "Leia com calma", "quando puder" | qualquer pressa, prazo apertado que não existe |
| técnico | o termo certo, explicado na primeira vez | termo sem explicação |

## 2. O mesmo modelo em três tons

Modelo 3 (convite para a consulta paga), preenchido com o Escritório Modelo de `../../docs/casos-ficticios.md` (consulta paga de 40 minutos, abatida dos honorários; R$ 250 é valor de exemplo).

**Você · próximo, claro, sem pressa**
```
Marta, obrigada por me contar. Para te responder com segurança, a advogada precisa olhar o seu caso com calma, com os documentos na mão.

O primeiro passo é uma consulta de 40 minutos, aqui no escritório ou por vídeo. O valor é R$ 250, descontado dos honorários se você contratar o escritório.

Quer que eu veja um horário para você?
Equipe Escritório Modelo
```

**Senhor e senhora · formal, sóbrio, claro**
```
Bom dia, Sra. Marta. Agradecemos o contato. Para orientá-la com segurança, a advogada precisa analisar o caso com os documentos.

O primeiro passo é uma consulta de 40 minutos, presencial ou por vídeo. O valor é R$ 250, abatido dos honorários caso a senhora contrate o escritório.

A senhora prefere um horário pela manhã ou à tarde?
Equipe Escritório Modelo
```

**Pelo nome · direto, objetivo**
```
Marta, para responder com segurança a advogada precisa ver o caso e os documentos.

Consulta: 40 minutos, presencial ou por vídeo.
Valor: R$ 250, descontado dos honorários se você fechar com a gente.

Te mando os horários desta semana?
Equipe Escritório Modelo
```

## 3. Conferência de cada modelo (antes de mostrar)

Responda sim ou não. Um "não" e o modelo volta para ajuste.

1. O tratamento é o da ficha, do começo ao fim (sem misturar "você" e "o senhor").
2. Nenhuma frase de `frases_que_nunca_usamos` aparece.
3. Nenhuma promessa de resultado, de prazo de decisão ou de chance ("vai dar certo", "seu caso é bom", "em 30 dias sai").
4. Nenhuma orientação jurídica a quem não é cliente ("você tem direito", "pode pedir X"), nem confirmação ou desmentido de tese trazida da internet ou de uma IA.
5. Nenhum valor que não venha da ficha. Valor de consulta só se `informa_valor_da_consulta_por_mensagem` permite. Valor de ação nunca.
6. Nenhuma urgência falsa, escassez ou isca ("só hoje", "últimas vagas", "condição especial", "desconto se fechar agora").
7. Mensagem automática diz que é automática. Nenhuma usa o nome do advogado como se ele estivesse digitando.
8. O caminho de urgência é real: o fora do horário só promete o que `urgencia_vai_para` permite ao contato usar; nunca "escreva URGENTE" num canal que ninguém lê; risco à vida e violência levam os números de emergência de `regras.md`.
9. Cabe na tela do celular: até uns 6 parágrafos curtos; lista quando houver mais de duas informações.
10. Termo técnico explicado na primeira vez, ou trocado por palavra comum.
11. Nenhuma marcação (`[A PREENCHER]`, `[A DEFINIR]`, `[A CONFIRMAR]`, `[CONFERIR]`) nem campo fixo entre colchetes no texto que vai ao contato: pendência mora no "Antes de enviar". O que quem envia preenche na hora está entre chaves (`{NOME}`, `{DIA E HORA}`) e listado em "Campos do envio".
12. O texto é para quem ainda não é cliente. Se fala de processo, audiência do caso ou documento do caso, é da biblioteca do cliente.
13. A chave e o "nunca usar quando" estão escritos.

## 4. Quando já existe outra biblioteca na pasta

A biblioteca comercial é um arquivo só dela: `escritorio/04-base/comercial/biblioteca-comercial.md`. As mensagens a quem já é cliente ficam em `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, que é do motor-experiencia (e pode ter sido criada pelo plugin `inicio-automacao`). Esta habilidade lê esse outro arquivo e nunca o altera.

### Regras de convivência

1. **Não renumere.** O número de um modelo na biblioteca comercial é dele para sempre. Modelo novo entra com o próximo número livre. Quem procura modelo procura pela chave.
2. **Não duplique.** Antes de escrever, procure pela chave e pelo assunto na biblioteca comercial. Se já existe, ajuste no mesmo número, com linha em "Mudanças".
3. **Fora do horário é um só.** O canal tem uma automática só, para contato e para cliente. Se a biblioteca do cliente já tem um `fora-do-horario`, mostre os dois textos lado a lado e pergunte qual vale. O escolhido fica igual nas duas, e a diferença vira linha em "Mudanças" da comercial. Nunca deixe duas automáticas diferentes no mesmo canal.
4. **Tom igual.** Se a biblioteca do cliente tem um tom já aprovado (abertura, assinatura), use como `frase_que_soa_como_a_gente` quando a ficha não tiver uma.
5. **O que é do cliente fica lá.** Boas-vindas ao cliente que fechou, atualização de andamento, "nada mudou", aviso de audiência ou perícia do caso, cobrança de documento do caso e resumo do mês não entram na biblioteca comercial. Se o advogado pedir um desses aqui, diga que é da experiência do cliente e indique a habilidade do motor-experiencia (se instalado); sem ele, escreva no chat e avise que deveria morar na biblioteca do cliente.

### Equivalências com a biblioteca do inicio-automacao

| Modelo de lá | O que a mensagens-comerciais faz |
|---|---|
| Fora do horário | Regra 3: um texto só, com o caminho real de urgência |
| Boas-vindas ao cliente, atualização de andamento, "nada mudou", aviso de audiência ou perícia, cobrança gentil, convite para ligação, resumo mensal, pedido de documento do caso | Não toca. São da experiência do cliente |
| Tabela "Mensagens que a rotina costuma pedir": resposta inicial ao contato novo, convite para a consulta, recusa com indicação, confirmação de recebimento com prazo, lembrete de consulta | Escreve aqui, na biblioteca comercial (`boas-vindas-contato-novo`, `convite-consulta-paga` ou `convite-consulta-gratuita`, `recusa-educada` e `encaminhamento-outra-area`, `recebi-retorno-ate`, `lembrete-de-consulta`). Não altera a tabela de lá; avisa o advogado de que essas linhas agora moram na biblioteca comercial |
