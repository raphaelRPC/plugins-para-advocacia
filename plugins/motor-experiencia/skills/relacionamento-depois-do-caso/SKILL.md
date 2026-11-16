---
name: relacionamento-depois-do-caso
description: >
  Mantém o contato com quem já foi cliente, sem oferta: a mensagem anual, o aviso quando uma
  mudança de lei pode afetar o cliente (depois de o advogado conferir), a resposta a quem volta a
  procurar o escritório e a porta aberta. Cuida do pedido de avaliação e da indicação sem captação
  nem contrapartida, dentro do Código de Ética e do Provimento 205/2021, respeita quem pediu para
  não receber e registra cada contato na carteira e no histórico. Use quando o advogado disser
  "manda a mensagem anual para os ex-clientes", "mudou a lei, quem a gente avisa?", "a ex-cliente
  voltou a escrever", "posso pedir indicação?", "como fico em contato depois do caso sem parecer
  propaganda". Não use para o encerramento e a prestação de contas (use encerramento-do-caso).
---

# Relacionamento depois do caso

> O caso acabou; a relação, não. Uma mensagem por ano, um aviso quando algo muda para ele, a porta aberta. Nada de oferta: o cliente lembra do escritório porque foi bem cuidado.

Regras comuns: `../../docs/regras.md` (em especial a seção 4, ética). Campos das fichas: `../../docs/ficha-da-experiencia.md` e `../../docs/ficha-da-experiencia-modelo.md`. Carteira: `../../docs/carteira.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

A aposentadoria do cliente saiu há um ano. Desde então, nenhuma palavra do escritório. Uma regra nova de prova de vida começa a valer, e ele fica sabendo por um vídeo que manda "clicar no link para não perder o benefício". Se o escritório tivesse mandado duas linhas, conferidas pela advogada, ele teria ligado antes de clicar.

**Regras fixas desta habilidade:**
1. Sem oferta. Nenhuma mensagem oferece serviço, ação nova, revisão, desconto ou promoção. Informa, pergunta como a pessoa está e deixa a porta aberta.
2. Só com quem aceitou contato depois do caso, e nunca com `pediu_para_nao_receber = sim`. Toda mensagem tem uma saída fácil ("se preferir não receber, é só me dizer").
3. Aviso de mudança de lei só depois de o advogado conferir a mudança e se ela afeta aquele cliente `[CONFERIR]`. A mensagem informa; não diz "você tem direito" e não vende a ação.
4. Avaliação e indicação sem captação e sem contrapartida, dentro do Código de Ética e Disciplina e do Provimento 205/2021 `[CONFERIR]`. O escritório não pede ao cliente que procure outras pessoas e não paga nem recompensa indicação.
5. Cada mensagem é pessoal e lida por alguém (A), mesmo quando sai em lote. Nada de disparo em massa.

## 1. Quando usar

**Use quando:**
- Chegou a data da mensagem anual de um ex-cliente (a carteira mostra `fase = encerrado` com `proximo_contato` vencendo).
- Saiu uma mudança de lei ou de regra que pode afetar ex-clientes de um tipo de caso, e o advogado quer avisar.
- Um ex-cliente voltou a escrever (dúvida do caso antigo, caso novo, indicação).
- O advogado quer saber o que pode e o que não pode no contato depois do caso.
- O `encerramento-do-caso` (se instalado) registrou que o cliente aceitou contato depois.

**Não use quando:**
- O caso ainda não acabou: as habilidades da jornada cuidam (`status-para-o-cliente`, `resumo-mensal-do-caso`).
- O pedido é prestação de contas ou devolução de documentos: `encerramento-do-caso` (se instalada).
- O ex-cliente chega com um caso novo: isso é contato comercial. Registre e passe para a `triar-contato` do motor-comercial (se instalado); sem ele, para quem atende contato novo.
- O pedido é publicidade para o público em geral (post, anúncio): fora deste plugin.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), o `nicho.md` se existir e os aprendizados (`aprendizados-experiencia.md`).
2. **Leia a carteira** (`escritorio/07-operacao/experiencia/carteira.csv`): ex-clientes são as linhas com `fase = encerrado`. Para cada um, o `clientes/<codigo>/encerramento.md` diz se aceitou contato depois e de que tipo.
3. **Conta e dados:** manter o contato depois do caso depende de base legal na LGPD e do que o cliente aceitou `[CONFERIR]`. Use só o mínimo da carteira. Em conta pessoal, só o treino.
4. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se quiserem seguir, pergunte só `contato_depois_do_caso` e ofereça gravar.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `contato_depois_do_caso`.
- **Melhora:** X: `pede_avaliacao_publica`.

Lê também o tom, o tratamento e a assinatura da ficha do escritório. Sem `contato_depois_do_caso`, a habilidade não manda nada: mostra as opções da seção 4 e pede a decisão do escritório.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | O que não faz |
|---|---|---|---|
| A pedido | O advogado ou a equipe | Os passos 1 a 9, mostrando cada mensagem | Não grava nem envia sem o ok |
| No ciclo | O `agente-de-suporte` | Mensagem anual vencida de quem aceitou: um rascunho por pessoa na fila (`tipo: mensagem-anual`) | Nunca aviso de lei, avaliação ou indicação no ciclo |
| Adaptar | A `adaptar-experiencia` (se instalada) | Reescreve as mensagens para o nicho, com `[ALTERADO]` | Só grava com o ok |
| Treino | Quem quer ver funcionando | Com uma carteira fictícia que tenha ex-clientes, gravando em `_treino/experiencia/` | Nada no registro real |

### Passo 1. Quem está no "depois"
Liste os ex-clientes (`fase = encerrado`). Tire da lista, com o motivo: `pediu_para_nao_receber = sim`; quem não aceitou contato no encerramento; quem tem `reclamacao_aberta = sim` (uma pessoa fala antes); quem tem `[A CONFIRMAR]` no aceite (pergunte à pessoa antes de mandar).

### Passo 2. Qual contato
Pergunte: "Que contato é este: mensagem anual, aviso de mudança de lei, resposta a quem voltou a escrever, ou pedido de avaliação?". Cada um tem a sua seção abaixo e o seu texto em `assets/mensagens-depois-do-caso.md`.

### Passo 3. Mensagem anual
- Quando: a data que a ficha diz (por exemplo, um ano depois do encerramento) ou a que ficou no `encerramento.md`.
- Conteúdo: lembrar quem escreve, perguntar como a pessoa está, uma lembrança útil do próprio caso dela (por exemplo, "se o pagamento da pensão atrasar, fale com a gente"), a porta aberta e a saída fácil.
- Nunca: oferta, "revisão do seu benefício", "agora atendemos também", data comemorativa como pretexto de venda.
A pedido: mostre. No ciclo: um arquivo por pessoa na fila, status `pendente`.

### Passo 4. Aviso de mudança de lei
1. Pergunte: "Qual é a mudança, e de onde ela vem?". A fonte é do advogado. A habilidade não pesquisa nem resume lei sozinha.
2. Pergunte: "Que tipo de cliente ela pode afetar?". Liste na carteira os ex-clientes daquele tipo de caso e área. A lista é sugestão: o advogado confirma, um por um, quem de fato é afetado `[CONFERIR]`.
3. Rascunhe a mensagem informativa (A, lida pelo advogado), com a conferência no cabeçalho interno "Antes de enviar" do rascunho: a mudança, a fonte, a data de vigência e se afeta esta pessoa `[CONFERIR]`. O texto ao cliente diz o que mudou em linguagem simples, que pode ou não afetá-lo, e que, se quiser conversar, o escritório está à disposição. Sem "você tem direito", sem "entre com ação", sem urgência falsa.
4. Se a mudança for golpe ou boato circulando ("clique no link para não perder o benefício"), o aviso é de segurança: o que o órgão oficial faz e não faz, conferido `[CONFERIR]`.

### Passo 5. Quem volta a escrever
- Dúvida sobre o caso antigo: responda como cliente da carteira (é dever de informar); se for andamento ou cumprimento, use as habilidades da jornada.
- Caso novo: agradeça a confiança e passe para o contato comercial (`triar-contato` do motor-comercial, se instalado). Sem orientação jurídica sobre o caso novo por mensagem.
- "Posso indicar vocês para uma amiga?": agradeça e diga que a amiga pode procurar o escritório pelo canal oficial. Sem contrapartida, sem pedir o contato da amiga, sem o escritório procurar a amiga.

### Passo 6. Pedido de avaliação (só se a ficha disser)
Só se `pede_avaliacao_publica` for "sim, no encerramento" e o pedido não tiver sido feito no encerramento. Uma vez, igual para todos, sem nada em troca, sem sugerir texto ou nota, nunca para quem teve reclamação não resolvida. A regra completa está em `references/limites-eticos.md`. Na dúvida, não peça.

### Passo 7. Quem pede para parar
Confirmação curta, sem insistir ("Combinado, [NOME]. Não mando mais mensagens. Se precisar, o número continua o mesmo."). Na carteira: `pediu_para_nao_receber = sim`, com o ok. Nunca mais mensagem de rotina, de aviso ou de avaliação.

### Passo 8. Registrar
Depois que a pessoa envia:
- uma linha de contato em `clientes/<codigo>/historico.md`, na tabela de quatro colunas (`| AAAA-MM-DD HHhMM | whatsapp | secretária | mensagem anual depois do caso, sem oferta |`);
- na carteira, com o ok: `ultimo_contato`, `ultimo_contato_tipo = mensagem`, `proximo_contato` (a próxima mensagem anual), `motivo_proximo_contato = depois-do-caso`, `atualizado_em`;
- se a pessoa respondeu, a resposta em uma frase no histórico. Resposta com queixa vai para a `reclamacao-e-recuperacao` (se instalada).

### Passo 9. Aprender
Pergunte: "Alguma mensagem você faria diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-experiencia.md`. Correção que puxa para a oferta ("aproveita e fala da revisão") não vira regra: explique a regra fixa 1 e proponha a versão que cabe.

## 4. O que o escritório escolhe em `contato_depois_do_caso`

| Opção | O que é | Observação |
|---|---|---|
| Nenhum contato | O caso acaba no encerramento | A porta aberta fica só na prestação de contas |
| Mensagem anual | Uma vez por ano, data combinada | Padrão sugerido |
| Aviso de mudança que afeta o cliente | Só quando houver, conferido pelo advogado | Pode existir sem a mensagem anual |
| Porta aberta | Resposta a quem volta a escrever | Sempre vale |

O escritório grava a escolha na ficha. A habilidade nunca inventa uma frequência maior que a da ficha.

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mensagens (a pedido, mostradas no chat; no ciclo, na fila) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-mensagem-anual.md` ou `-aviso-de-mudanca.md` |
| Histórico do ex-cliente | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Carteira | `escritorio/07-operacao/experiencia/carteira.csv`: `ultimo_contato`, `ultimo_contato_tipo`, `proximo_contato`, `motivo_proximo_contato`, `pediu_para_nao_receber`, `atualizado_em`, com o ok |
| Mensagens adaptadas | `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chaves `mensagem-anual`, `aviso-de-mudanca`, `ex-cliente-voltou`, `resposta-indicacao`, `confirmacao-parar` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: as mensagens saem no chat, e as linhas da carteira saem como tabela para colar.

## 6. Formato da saída

- **Lista do mês:** ex-cliente, tipo de contato, data, motivo de quem ficou de fora.
- **Cada mensagem:** para quem, tipo, sigla (A), quem lê, o texto, e o cabeçalho interno quando houver conferência (aviso de lei, avaliação).
- **Linhas da carteira e do histórico** propostas.

## 7. Solo e equipe

**Solo:** um lote por mês, no mesmo dia, leva poucos minutos e mantém a carteira de ex-clientes viva sem virar propaganda. O aviso de mudança de lei é a peça que mais mostra valor, e é sempre o advogado que confere.

**Equipe:** a secretária monta o lote e envia; o advogado confere aviso de lei e qualquer resposta com conteúdo jurídico. Quem volta com caso novo passa pelo comercial, como qualquer contato.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Feliz aniversário! Aproveite 20% na revisão" | Captação e oferta disfarçada | Regra fixa 1 |
| Mensagem para quem pediu para parar | Incômodo e risco de reclamação | Passo 1 e passo 7 |
| Aviso de lei sem conferência | Informação errada ao ex-cliente | O advogado traz a fonte e confirma cada pessoa |
| "Você tem direito a..." no aviso | Promessa e orientação sem análise | O aviso só informa e abre a porta |
| Pedir indicação com recompensa | Captação e contrapartida | Regra fixa 4 e `references/limites-eticos.md` |
| Disparo em massa igual para todos | Soa como propaganda | Cada mensagem pessoal e lida |
| Contato depois sem registro | Ninguém sabe quem recebeu o quê | Passo 8 |

## 9. Próximo passo

- Ex-cliente com caso novo: `triar-contato` do motor-comercial (se instalado).
- Ex-cliente com queixa: `reclamacao-e-recuperacao` (se instalada).
- Pesquisa do encerramento ainda não feita: `pesquisa-de-satisfacao` (se instalada).
- Ver quantos ex-clientes recebem contato: `painel-da-carteira` (se instalada).

Se a habilidade indicada não estiver instalada, diga em uma linha o que fazer à mão e siga.

## Referências desta habilidade

- `assets/mensagens-depois-do-caso.md`: as mensagens de partida (anual, aviso de mudança, quem voltou, indicação, parar, avaliação) e o cabeçalho interno do aviso. Use nos passos 3 a 7.
- `references/limites-eticos.md`: o que pode e o que não pode no contato depois do caso, na avaliação e na indicação. Leia antes do primeiro lote e nos passos 4 a 6.
