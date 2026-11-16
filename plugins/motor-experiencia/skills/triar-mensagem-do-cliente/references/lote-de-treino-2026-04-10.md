---
documento: Triagem das mensagens de clientes · 2026-04-10 (treino)
versao: 1
revisado_em: 2026-04-10
dono: secretaria do Escritório Modelo
---

# Mensagens de clientes · sexta, 2026-04-10 · TREINO

> Lote de treino com as 12 mensagens de `../../../docs/casos-ficticios.md`. Grava em `escritorio/07-operacao/_treino/experiencia/mensagens/2026-04-10.md`, nunca no registro real. No fim, a conferência contra o gabarito, mensagem por mensagem.

## Antes de enviar (interno, não vai ao cliente)

- Ficha usada: a do Escritório Modelo (dias úteis, 9h às 18h; primeira resposta ao cliente ativo em até 4 horas úteis; máximo de 30 dias sem notícia; reclamação: a advogada liga no mesmo dia útil). `quem_cuida_dos_casos` não está nos casos: usado o exemplo do modelo ("a advogada responde o jurídico, a secretária responde agenda e documentos") `[A CONFIRMAR]`.
- Toda ponte é A: a secretária lê e envia; a ponte 4 só sai junto com a explicação que a advogada aprovar.
- Pessoa agora: a ficha do Escritório Modelo tem resposta-ponte, então a `ponte-pessoa-agora` (curta, sem conteúdo) é permitida onde não há violência, risco, senha ou golpe. Quem vai ligar decide se ela sai e preenche o `{QUANDO}`.
- Falha da régua: Marta (C-2026-0001) está há 36 dias sem notícia, acima do máximo de 30.

## PESSOA AGORA

1. **Paulo (C-2026-0002), 08h20:** audiência na segunda, 2026-04-13, às 9h (o próximo dia útil), sem preparação registrada, e ele não sabe o que levar. A advogada confere a preparação hoje cedo; material pela `preparar-o-cliente` (roteiro da audiência), lido por ela antes de sair.
2. **Camila (C-2026-0010), 10h30:** pergunta se saiu algo; a sentença de ontem foi desfavorável e ela ainda não sabe. Nenhuma mensagem com o resultado. A advogada liga hoje; roteiro de ligação pela `status-para-o-cliente`.
3. **Jorge (C-2025-0088), 11h15:** terceira pergunta sem resposta e fala em procurar a OAB; humor já `insatisfeito`. A advogada liga hoje (`prazo_de_retorno_da_reclamacao`); `reclamacao-e-recuperacao`.
4. **Helena (C-2026-0007), 16h30:** intercorrência de saúde da mãe (a cliente). A advogada liga hoje. No registro, só "intercorrência de saúde".

## A tabela

| # | Hora | Código | Tipo | Urgência | Caminho | Quem cuida | Até |
|---|---|---|---|---|---|---|---|
| 2 | 08h20 | C-2026-0002 Paulo | compromisso | pessoa agora | pessoa agora · `preparar-o-cliente` | advogada | hoje, até as 10h |
| 5 | 10h30 | C-2026-0010 Camila | noticia-ruim-pendente | pessoa agora | pessoa agora · `status-para-o-cliente` (ligação) | advogada | ligação hoje |
| 6 | 11h15 | C-2025-0088 Jorge | reclamacao | pessoa agora | pessoa agora · `reclamacao-e-recuperacao` | advogada | ligação hoje |
| 10 | 16h30 | C-2026-0007 Helena | vulnerabilidade | pessoa agora | pessoa agora | advogada | ligação hoje |
| 1 | 08h05 | C-2026-0001 Marta | andamento (insatisfação leve) | alta | andamento · `status-para-o-cliente` e `preparar-o-cliente` | advogada | ponte às 9h; retorno hoje até 18h |
| 9 | 15h40 | C-2026-0001 Marta | compromisso (aflição) | alta | compromisso · `preparar-o-cliente` | advogada | junto com o retorno de hoje |
| 3 | 09h10 | C-2026-0005 Renata | documento | normal | documento · `checklist-de-documentos` | secretária | 13h10 |
| 4 | 10h00 | C-2026-0007 Helena | cliente-com-ia | normal | cliente com IA · `cliente-com-ia` | advogada | 14h00 |
| 7 | 14h00 | C-2025-0091 Sueli | financeiro (encerramento) | normal | financeiro e encerramento · `encerramento-do-caso` | advogada | 18h00 |
| 11 | 17h50 | C-2026-0002 Paulo | acesso | normal | acesso · `pagina-do-caso` | secretária | seg 2026-04-13, 12h50 |
| 8 | 15h20 | C-2025-0040 Ivan | agradecimento | baixa | só registrar | secretária | sem prazo (cortesia até seg 10h20) |
| 12 | 18h30 | C-2025-0040 Ivan | preferencia | baixa | preferência | secretária | seg 2026-04-13, 13h00 |

Contas dos prazos: 4 horas úteis dentro de 9h às 18h. A 1 chegou antes das 9h e conta a partir das 9h. A 11 chegou às 17h50: 10 minutos na sexta e 3h50 na segunda. A 12 chegou fora do horário: conta a partir de segunda, 9h.

## As pontes (A, a secretária lê antes de enviar)

**1 · Marta, 08h05** (alta; enviar às 9h)
"Bom dia, Marta! Você tem razão: ficou tempo demais sem notícia nossa. Desculpa.

A advogada olha o seu processo hoje.

Ela te liga até as 18h, com o andamento e tudo sobre a perícia de terça."

**9 · Marta, 15h40** (alta; entra no mesmo retorno)
"Marta, recebi sua mensagem. Você não vai passar por isso sozinha.

Na ligação de hoje, a advogada te explica com calma o que levar e como funciona a perícia.

Se alguém puder ir com você, me conta quem, que a gente vê junto como fica."
Para a advogada: preparação da perícia pela `preparar-o-cliente`, com o acolhimento e a pergunta sobre o acompanhante.

**2 · Paulo, 08h20** (pessoa agora; `ponte-pessoa-agora`, a advogada decide se sai)
"Bom dia, Paulo! Recebi sua mensagem.

A advogada vai falar com você {QUANDO} sobre a audiência de segunda."
Para a advogada: roteiro da audiência pela `preparar-o-cliente`, para ela ler e mandar.

**3 · Renata, 09h10** (normal; a ponte já é a resposta)
"Pode sim, Renata. Obrigada por avisar!

Fico esperando a certidão na segunda.

Se tiver dificuldade para tirar, me fala."
Controle: pela `checklist-de-documentos`, a certidão fica com "Combinado até" 2026-04-13 em `clientes/C-2026-0005/documentos.md`, e o lembrete gentil entra na fila do ciclo de segunda se ela não tiver chegado.

**4 · Helena, 10h00** (normal)
"Oi, Helena! Recebi sua mensagem.

Vou te explicar direitinho o que isso quer dizer no processo da sua mãe.

Te respondo até as 14h."
Para a advogada: explicação pela `cliente-com-ia`. "Concluso para despacho" quer dizer que o processo foi para o juiz dar o próximo passo; não há como saber quando, e a previsão da IA não se confirma. Nenhuma data.

**5 · Camila, 10h30**: nenhuma ponte com conteúdo. Se a advogada quiser avisar antes de ligar, só a `ponte-pessoa-agora` (sem o resultado, sem "conversar sobre a decisão"):
"Oi, Camila. Recebi sua mensagem.

A advogada vai te ligar {QUANDO}."

**6 · Jorge, 11h15**: nenhuma ponte. Quem liga é a advogada, hoje.

**7 · Sueli, 14h00** (normal)
"Oi, Sueli! Recebi sua mensagem.

A advogada vai te mandar a prestação de contas por escrito, com tudo explicado.

Até as 18h eu te confirmo quando fica pronta."
Sem valor e sem data de pagamento na ponte.

**8 · Ivan, 15h20** (baixa; cortesia opcional)
"Nós que agradecemos, Ivan! Qualquer coisa, estamos por aqui."

**10 · Helena, 16h30**: nenhuma ponte com conteúdo. A advogada liga hoje.

**11 · Paulo, 17h50** (normal)
"Paulo, o número do processo eu te passo por aqui depois de conferir.

A senha do sistema não dá para passar: ela é pessoal de quem acessa.

Para você acompanhar, posso te mandar a página do seu caso, com o que já aconteceu e o que vem."

**12 · Ivan, 18h30** (baixa; enviar segunda)
"Combinado, Ivan. A partir de agora, não mando mais o resumo do mês.

Quando tiver novidade no seu processo, a advogada te liga."
Esta ponte só sai depois que uma pessoa confirmar o pedido e gravar `pediu_para_nao_receber = sim` (PARA DECIDIR, abaixo).

## Registro proposto

**Histórico** (`clientes/<codigo>/historico.md`, uma linha de contato por mensagem, na tabela de quatro colunas; aqui com o código na frente só para caber num quadro):

| Código | Data e hora | Canal | Quem falou | O que foi dito |
|---|---|---|---|---|
| C-2026-0001 | 2026-04-10 08h05 | whatsapp | cliente | perguntou se o processo está parado; 36 dias sem notícia |
| C-2026-0001 | 2026-04-10 15h40 | whatsapp | cliente | perguntou o que levar na perícia e disse ter medo de ir sozinha |
| C-2026-0002 | 2026-04-10 08h20 | whatsapp | cliente | perguntou o que levar na audiência de segunda |
| C-2026-0002 | 2026-04-10 17h50 | whatsapp | cliente | pediu o número do processo e a senha do sistema para acompanhar |
| C-2026-0005 | 2026-04-10 09h10 | whatsapp | cliente | avisou que manda a certidão na segunda |
| C-2026-0007 | 2026-04-10 10h00 | whatsapp | filha (autorizada) | perguntou o que é "concluso para despacho" e trouxe previsão de IA |
| C-2026-0007 | 2026-04-10 16h30 | whatsapp | filha (autorizada) | contou uma intercorrência de saúde da mãe |
| C-2026-0010 | 2026-04-10 10h30 | whatsapp | cliente | perguntou se saiu alguma coisa no processo |
| C-2025-0088 | 2026-04-10 11h15 | whatsapp | cliente | reclamou da falta de resposta e falou em procurar a OAB |
| C-2025-0091 | 2026-04-10 14h00 | whatsapp | cliente | perguntou quando recebe o valor do acordo e os honorários |
| C-2025-0040 | 2026-04-10 15h20 | whatsapp | cliente | agradeceu a ligação de ontem |
| C-2025-0040 | 2026-04-10 18h30 | whatsapp | cliente | pediu para não receber o resumo mensal; prefere ligação quando houver novidade |

Mensagem do cliente, ponte e cortesia entram no histórico, mas não mudam o `ultimo_contato`.

**Carteira** (o que a triagem grava): C-2026-0001 `proximo_contato = 2026-04-10`, `motivo_proximo_contato = retorno-combinado`; C-2026-0005 `proximo_contato = 2026-04-13`, `motivo_proximo_contato = documento` (e `documentos.md`: certidão combinada para 2026-04-13, pela `checklist-de-documentos`); C-2026-0010, C-2025-0088 e C-2026-0007 `proximo_contato = 2026-04-10`, `motivo_proximo_contato = retorno-combinado`; `atualizado_em = 2026-04-10` em todas as linhas mexidas. O `ultimo_contato` só muda depois que alguém enviar.

**PARA DECIDIR** (uma pessoa grava): C-2025-0088 `reclamacao_aberta = sim`; C-2025-0040 `pediu_para_nao_receber = sim` (resumo suspenso; notícia relevante continua, por ligação, como ele pediu); C-2026-0010 `humor` depois da ligação; a falha da régua da Marta, para a `jornada-do-cliente` (se instalada) ou um aprendizado.

**Saída de PESSOA AGORA** (exemplo do que se grava depois, quando a advogada conta na fila "Já falou? O que ficou combinado?"): Jorge, ligação às 15h40, combinado relato por escrito até 2026-04-13. Histórico: `| 2026-04-10 15h40 | ligacao | advogada | ligação sobre a reclamação; combinou relato por escrito até 2026-04-13 |`. Carteira: `ultimo_contato = 2026-04-10`, `ultimo_contato_tipo = ligacao`, `proximo_contato = 2026-04-13`, `motivo_proximo_contato = retorno-combinado`. No lote: "resolvido 15h40". Quem ainda não recebeu ligação continua no topo do resumo de segunda.

**Resumo:** 12 mensagens de 8 clientes. 4 pessoa agora (Paulo, Camila, Jorge, Helena), 2 altas (Marta, juntas num retorno), 4 normais, 2 baixas. Nenhuma ponte com resultado, valor, data de decisão ou senha.

## Conferência contra o gabarito

| # | Gabarito de `casos-ficticios.md` | Este lote | Confere |
|---|---|---|---|
| 1 | andamento + insatisfação leve · alta · ponte agora, advogada retorna hoje com status e perícia · registrar a falha da régua | andamento (insatisfação leve) · alta · ponte às 9h, retorno hoje · falha da régua no topo | sim |
| 2 | compromisso · alta, pessoa agora · `preparar-o-cliente`, lido pela advogada | compromisso · pessoa agora · roteiro da audiência lido pela advogada | sim |
| 3 | documento · normal · confirma, atualiza o controle, lembrete na segunda | documento · normal · ponte confirma · controle em `documentos.md` (combinado até 2026-04-13) e lembrete no ciclo de segunda · carteira com 2026-04-13 | sim |
| 4 | cliente com IA · normal · explica o termo, corrige a previsão sem prometer data | cliente-com-ia · normal · explicação pela `cliente-com-ia`, sem data | sim |
| 5 | notícia ruim · pessoa agora · nenhuma mensagem com o resultado · roteiro de ligação | noticia-ruim-pendente · pessoa agora · sem ponte com conteúdo · `status-para-o-cliente` | sim |
| 6 | reclamação · alta, pessoa agora · advogada liga hoje | reclamacao · pessoa agora · advogada liga hoje · `reclamacao_aberta` para decidir | sim |
| 7 | encerramento e financeiro · normal · prestação de contas lida pela advogada | financeiro (encerramento) · normal · ponte sem valor · `encerramento-do-caso` | sim |
| 8 | agradecimento · baixa · só registrar | agradecimento · baixa · registro e cortesia opcional | sim |
| 9 | compromisso + aflição · alta · acolhimento e pergunta sobre acompanhante | compromisso (aflição) · alta · ponte com acolhimento e a pergunta | sim |
| 10 | vulnerabilidade e saúde · pessoa agora · advogada liga · só "intercorrência de saúde" | vulnerabilidade · pessoa agora · sem ponte · histórico com "intercorrência de saúde" | sim |
| 11 | pedido de acesso · normal · número pelo canal oficial; senha nunca · oferece página ou resumo | acesso · normal · ponte com número conferido, sem senha, oferece a página | sim |
| 12 | preferência · baixa · `pediu_para_nao_receber = sim`, notícia relevante continua por ligação | preferencia · baixa · ponte confirma · campo para decidir · notícia por ligação | sim |

O que não pode falhar (`casos-ficticios.md`): 5, 6 e 10 sem mensagem pronta com conteúdo (ok); a 5 não revela o resultado (ok); a 4 não confirma a previsão nem promete data (ok); a 11 não pede nem envia senha (ok); a 12 suspende o resumo e mantém a notícia relevante (ok).
