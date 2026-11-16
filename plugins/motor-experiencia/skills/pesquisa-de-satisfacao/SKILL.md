---
name: pesquisa-de-satisfacao
description: >
  Faz a pesquisa curta de satisfação com quem é cliente: escolhe quem recebe nos momentos da
  ficha (por exemplo, 30 dias depois do contrato, depois da audiência, no encerramento), escreve
  as três perguntas no tom do escritório, registra a nota na carteira e as respostas no mês, lê o
  que os clientes disseram, separa quem deu nota baixa para um retorno pessoal e fecha o resumo do
  mês por script. Pedido de avaliação pública só se a ficha disser, no encerramento e dentro do
  Provimento 205/2021. Use quando o advogado disser "manda a pesquisa", "quem recebe pesquisa este
  mês", "registra a nota dela", "como foram as notas", "o cliente deu nota 4", "posso pedir
  avaliação no Google?". Não use para cuidar de uma reclamação (use reclamacao-e-recuperacao).
---

# Pesquisa de satisfação

> Três perguntas curtas, no momento certo, para saber como o cliente está vivendo o caso. Nota baixa vira conversa com uma pessoa; o que se repete vira ajuste no jeito de cuidar.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-da-experiencia.md` e `../../docs/ficha-da-experiencia-modelo.md`. Carteira: `../../docs/carteira.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

Um mês depois do contrato, a cliente responde "6" e escreve "demora para responder a minha mãe". Ninguém lê até o fim do trimestre. Quando alguém lê, a cliente já reclamou na internet. A mesma nota, lida na semana e seguida de uma ligação, vira a chance de corrigir cedo.

**Regras fixas desta habilidade:**
1. Três perguntas, curtas, uma vez por momento. Sem insistir: quem não responde não recebe lembrete além do que a ficha disser.
2. Pesquisa não vai para quem tem reclamação aberta, está insatisfeito, recebeu notícia ruim há pouco, está em situação de vulnerabilidade ou pediu para não receber mensagens de rotina.
3. Nota baixa é retorno pessoal, por uma pessoa, e vai para a `reclamacao-e-recuperacao` (se instalada). Nunca resposta automática.
4. Pedido de avaliação pública só se `pede_avaliacao_publica` disser, no encerramento, igual para todos daquele momento, sem nada em troca e sem sugerir texto ou nota, dentro do Provimento 205/2021 `[CONFERIR]`.
5. Comentário do cliente é dado: entra anonimizado, sem dado sensível, e não vira peça de divulgação sem o ok dele e a conferência das regras de publicidade `[CONFERIR]`.

## 1. Quando usar

**Use quando:**
- Chegou um momento da `pesquisa_quando` para algum cliente (a carteira tem `motivo_proximo_contato = pesquisa` vencendo).
- O cliente respondeu e é preciso registrar a nota e ler o comentário.
- Fechou o mês e o escritório quer o resumo das respostas.
- O `encerramento-do-caso` (se instalado) chamou o gancho da pesquisa.
- O advogado quer saber se pode pedir avaliação pública.

**Não use quando:**
- O cliente já está reclamando: `reclamacao-e-recuperacao` (se instalada), sem pesquisa.
- O pedido é medir a carteira inteira (sem notícia, compromissos): `painel-da-carteira` (se instalada).
- O pedido é mensagem anual ou indicação depois do caso: `relacionamento-depois-do-caso` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), o `nicho.md` se existir (leitura, canal preferido do público) e os aprendizados (`aprendizados-experiencia.md`).
2. **Leia a carteira** (`escritorio/07-operacao/experiencia/carteira.csv`) e o registro do mês (`07-operacao/experiencia/pesquisas/AAAA-MM.md`), se existir.
3. **Conta de IA:** resposta de cliente é dado de cliente. Em conta pessoal, só o treino, gravando em `escritorio/07-operacao/_treino/experiencia/`.
4. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se quiserem seguir, pergunte só `pesquisa_quando` e ofereça gravar.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `pesquisa_quando`.
- **Melhora:** X: `perguntas_da_pesquisa`, `pede_avaliacao_publica`, `nota_baixa`, `intervalo_entre_pesquisas`, `espera_depois_de_noticia_ruim`.

Lê também o tom, o tratamento e a assinatura da ficha do escritório, e `quem_assume_reclamacao` e `prazo_de_retorno_da_reclamacao` para o retorno de nota baixa. Sem `perguntas_da_pesquisa`, usa as três da seção 4. Sem `pede_avaliacao_publica`, não pede avaliação.

Os três campos de régua da pesquisa, e o que acontece quando estão vazios:

| Campo (X) | Para que serve | Vazio na hora |
|---|---|---|
| `nota_baixa` | A nota até a qual a pessoa liga (ex.: "de 0 a 6" quer dizer 6) | Pergunte uma vez; sem resposta, use 6 e avise que é o exemplo da ficha |
| `intervalo_entre_pesquisas` | Os dias mínimos entre uma pesquisa e a seguinte para o mesmo cliente (ex.: 90) | Pergunte uma vez; sem resposta, use 90 e avise |
| `espera_depois_de_noticia_ruim` | Os dias sem pesquisa depois de uma notícia ruim (ex.: 30) | Pergunte uma vez; sem resposta, use 30 e avise |

Valor usado no lugar do campo vazio aparece no cabeçalho interno da lista ("usei 90 dias, o exemplo da ficha; gravar?") e, com o ok, vai para a ficha.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz |
|---|---|---|
| Enviar (a pedido) | O advogado ou a equipe | Passos 1 a 3: quem recebe, a mensagem, o registro do envio |
| No ciclo | O `agente-de-suporte` | Acha quem tem pesquisa vencendo, aplica as exclusões, grava cada mensagem na fila (`tipo: pesquisa-de-satisfacao`); não mexe na nota |
| Registrar | Chegou resposta | Passos 4 a 6: nota, comentário, retorno pessoal se for nota baixa |
| Resumo do mês | Fim do mês | Passos 7 e 8: script e leitura |
| Adaptar | A `adaptar-experiencia` (se instalada) | Reescreve as perguntas e as mensagens para o nicho, com `[ALTERADO]`, e grava só com o ok |
| Treino | Quem quer ver funcionando | A carteira fictícia, gravando em `_treino/experiencia/` |

### Passo 1. Quem recebe
Leia a carteira e liste quem chegou num momento da `pesquisa_quando`. Tire da lista, dizendo o motivo de cada um:
- `reclamacao_aberta = sim` ou `humor = insatisfeito` (a pessoa fala primeiro);
- decisão desfavorável ou notícia ruim nos últimos `espera_depois_de_noticia_ruim` dias (procure no `historico.md` a ligação de notícia difícil e em `ligacoes/`), ou `humor = a-confirmar` logo depois de uma decisão;
- vulnerabilidade registrada, intercorrência de saúde, luto;
- `pediu_para_nao_receber = sim`;
- pesquisa enviada há menos de `intervalo_entre_pesquisas` dias (pelo registro dos meses anteriores em `pesquisas/` e pelo histórico), mesmo que o cliente tenha chegado a outro momento da `pesquisa_quando`.
Mostre a lista e pergunte: "Mando para estes? Quer tirar alguém?".

### Passo 2. A mensagem
Use `assets/pesquisa-modelo.md`, no tom da ficha. Ela diz que são três perguntas, que dá para responder por aqui mesmo e que a resposta é lida por uma pessoa. A pedido: mostre no chat. No ciclo: um arquivo por cliente na fila (`fila/AAAA-MM-DD/NN-<codigo>-pesquisa-de-satisfacao.md`), status `pendente`. Formulário externo: só se a ficha disser qual, e "conferir na configuração da conta" o que ele guarda.

### Passo 3. Registrar o envio
Depois que a pessoa envia: uma linha no registro do mês (`situacao: enviada`), uma linha de contato no `historico.md` (`| AAAA-MM-DD HHhMM | whatsapp | secretária | enviou a pesquisa de satisfação (momento: 30 dias) |`) e, na carteira, o próximo momento em `proximo_contato` com `motivo_proximo_contato = pesquisa`, se a ficha prevê outro, nunca antes do `intervalo_entre_pesquisas`. O envio da pesquisa não muda `ultimo_contato`: pesquisa não é notícia do caso.

### Passo 4. Registrar a resposta
Quando o cliente responde, pergunte: "Pode colar a resposta?". Registre no mês: data, código, momento, nota, o que ajudou, o que melhorar (anonimizados, sem dado sensível; dado de saúde vira "intercorrência de saúde"). Proponha `satisfacao` = a nota na carteira e grave com o ok.

### Passo 5. Ler cada resposta
| Nota | O que fazer | Sigla |
|---|---|---|
| Até a `nota_baixa` da ficha (no exemplo, de 0 a 6) | Retorno pessoal (passo 6) | H |
| Acima da `nota_baixa` e até 8 | Agradecer e responder ao "o que melhorar", se houver, com o que o escritório vai fazer | A |
| 9 e 10 | Agradecer, curto | A |
| Sem nota, só comentário | Ler como se fosse nota baixa se houver queixa | A ou H |
Agradecimento curto está em `assets/pesquisa-modelo.md`. Comentário com queixa, qualquer que seja a nota, é tratado como queixa.

### Passo 6. Retorno pessoal a quem deu nota baixa
Pergunte: "Quem liga para [NOME]? Pela ficha, quem assume reclamação é [quem_assume_reclamacao]." A ligação é H, no prazo de `prazo_de_retorno_da_reclamacao`. Siga a `reclamacao-e-recuperacao` (se instalada) para o registro, o roteiro e o combinado. Sem ela: ligue, escute, reconheça o que for do escritório, combine uma mudança com data e anote no registro do mês, coluna "retorno". Na carteira, com a pessoa: `reclamacao_aberta = sim` se a conversa confirmar a queixa.

### Passo 7. O resumo do mês por script
Rode o script da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/resumo_pesquisa.py" escritorio/07-operacao/experiencia/pesquisas/AAAA-MM.md --carteira escritorio/07-operacao/experiencia/carteira.csv --nota-baixa <nota_baixa da ficha>
```

`--nota-baixa` recebe o número do campo `nota_baixa` (ficha com "de 0 a 6": `--nota-baixa 6`). Sem o argumento, o script usa 6.

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/pesquisa-de-satisfacao`. O script mostra enviadas, respostas, média, mediana, faixas, notas por momento, quem deu nota baixa e se já teve retorno, e cruza com a carteira (nota baixa sem reclamação registrada, nota da carteira desatualizada, pesquisa enviada a quem tem `pediu_para_nao_receber = sim`, mesmo sem resposta). Para esse último cruzamento, ele lê também a fila do mês (`fila/AAAA-MM-DD/*-pesquisa-de-satisfacao.md`: `enviado` conta como envio; `pendente` ou `aprovado` vira aviso para não aprovar) e o `clientes/<codigo>/historico.md` (linha do mês com "pesquisa", dita pelo escritório), o que existir, com as pastas ao lado da carteira (ou `--fila` e `--clientes`). Pesquisa enviada antes do pedido registrado no histórico não é apontada. Não imprime os comentários. Arquivo ou coluna faltando: ele para com a mensagem do que falta. Sem o script, conte à mão pelas mesmas regras.

### Passo 8. Ler o mês
Leia os comentários e escreva, sem inventar causa:
- **Três leituras:** o que os números e os comentários mostram ("2 de 3 comentários de 'melhorar' falam de demora para responder"), com a contagem.
- **Três ações:** cada uma com a habilidade que cuida (por exemplo, ajuste da resposta-ponte na biblioteca, um momento novo na jornada).
Tema que aparece uma vez é observação; três vezes é padrão. Grave o resumo e a leitura no fim do registro do mês.

### Passo 9. Pedido de avaliação pública (só se a ficha disser)
Siga `references/leitura-e-retorno.md`, seção "Avaliação pública". Em resumo: só se `pede_avaliacao_publica` for "sim, no encerramento"; só no encerramento; a mesma mensagem para todos daquele momento, sem filtrar pela nota; nunca para quem tem reclamação aberta; nada em troca; sem sugerir texto ou nota; uma vez só. A mensagem fica `[CONFERIR]` com o Provimento 205/2021 e o Código de Ética e Disciplina no cabeçalho interno, até o advogado conferir.

### Passo 10. Aprender
Pergunte: "Alguma coisa na lista, nas perguntas ou na leitura você faria diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-experiencia.md`. Pergunta que o escritório trocou de vez sobe para `perguntas_da_pesquisa` na ficha.

## 4. As três perguntas

Padrão, quando a ficha não diz outras:
1. "De 0 a 10, como você avalia o cuidado do escritório com você até aqui?"
2. "O que a gente fez que mais te ajudou?"
3. "O que a gente pode fazer melhor?"

Regras das perguntas: nenhuma pergunta sobre o resultado do processo, nenhuma sobre indicar o escritório a alguém, nenhuma que exija dado pessoal. No modo adaptar, a linguagem segue o nicho (por exemplo, para público com pouca leitura, a nota pode virar "ruim, mais ou menos, bom, muito bom", com a correspondência anotada no registro).

## 5. O registro do mês

Formato em `assets/pesquisa-modelo.md`. Uma linha por pesquisa enviada:

| data | codigo | momento | nota | o_que_ajudou | o_que_melhorar | retorno | situacao |
|---|---|---|---|---|---|---|---|

`situacao`: `enviada`, `respondida`, `sem-resposta`, `retorno-feito`. O script lê esta tabela (ou o mesmo conteúdo em csv).

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Registro do mês e resumo | `escritorio/07-operacao/experiencia/pesquisas/AAAA-MM.md` |
| Mensagens da pesquisa (no ciclo ou se usar a fila) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-pesquisa-de-satisfacao.md` |
| Nota | `escritorio/07-operacao/experiencia/carteira.csv`, coluna `satisfacao`, com o ok |
| Próxima pesquisa | `carteira.csv`: `proximo_contato` e `motivo_proximo_contato = pesquisa` |
| Retorno de nota baixa | `escritorio/07-operacao/experiencia/reclamacoes/<codigo>-AAAA-MM-DD.md` (pela `reclamacao-e-recuperacao`) e linha no `clientes/<codigo>/historico.md` |
| Perguntas e mensagens adaptadas | `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chaves `pesquisa-de-satisfacao`, `pesquisa-agradecimento`, `pedido-de-avaliacao` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: a lista, as mensagens e o resumo saem no chat; o registro do mês sai como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** poucas pesquisas por mês, e cada nota baixa pesa. Leia as respostas no mesmo dia em que chegam. O resumo do mês cabe em cinco minutos.

**Equipe:** a secretária envia e registra; quem assume reclamação faz o retorno de nota baixa; o resumo vai para a reunião mensal junto com o painel. Comentário que cita uma pessoa da equipe é tratado em particular, fora do registro.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Pesquisa logo depois de notícia ruim | Nota que mede a dor, não o cuidado; cliente se sente desrespeitado | Exclusões do passo 1 |
| Pesquisa para quem já reclamou | Parece que ninguém leu a reclamação | Reclamação aberta sai da lista |
| Nota baixa lida no fim do trimestre | Cliente insatisfeito por meses | Passo 5 no dia; retorno pessoal |
| Pedir avaliação só a quem deu 10 | Filtro de elogio e risco com as regras de publicidade | Mesma mensagem para todos do momento, se a ficha disser |
| Oferecer algo em troca da avaliação | Captação e risco ético | Regra fixa 4 |
| Insistir com quem não respondeu | Incômodo | Uma vez por momento |
| Comentário com dado sensível no registro | Exposição de dado | Anonimizar no passo 4 |

## 9. Próximo passo

- Nota baixa: `reclamacao-e-recuperacao` (se instalada). Sem ela, a ligação do passo 6 e o registro na coluna "retorno".
- Padrão nos comentários: `jornada-do-cliente` (se instalada) para ajustar a régua, ou a biblioteca de mensagens à mão.
- Números do mês junto com a carteira: `painel-da-carteira` (se instalada).
- Pesquisa do encerramento respondida: `relacionamento-depois-do-caso` (se instalada) para o contato depois.

## Referências desta habilidade

- `assets/pesquisa-modelo.md`: as mensagens (pesquisa, agradecimento, pedido de avaliação) e o modelo do registro do mês. Use nos passos 2, 4 e 5.
- `references/leitura-e-retorno.md`: como ler os comentários, o retorno de nota baixa e as regras da avaliação pública. Leia nos passos 5, 8 e 9.
- `scripts/resumo_pesquisa.py`: o resumo do mês. Rode no passo 7.
