# Gaste menos do seu plano

Dicas para o advogado. Cada uma diz o que pesa e o que fazer. Base: o que o registro de uso mede (o que mais pesa em cada conversa) e a documentação da Anthropic. Ao recomendar, escolha a que responde ao que mais pesou no resumo dele; no máximo três por vez.

Status: **rascunho para o Raphael revisar** (16/10/2026). As dicas 7 e 8 dependem da decisão dele.

## 1. Uma conversa por tarefa

**O que pesa:** cada mensagem nova reenvia ao Claude toda a conversa até ali. Numa conversa longa, a centésima mensagem carrega as 99 anteriores.

**Faça assim:** terminou a minuta, abra uma conversa nova para a edição. Para retomar, peça "continua de onde paramos": o plugin lê o `andamento.md` e o registro de peças, sem você colar o histórico.

## 2. Junte os ajustes numa mensagem só

**O que pesa:** cada mensagem gera uma resposta, e cada resposta relê a conversa.

**Faça assim:** em vez de três mensagens ("muda o título", "agora a cor", "e tira o M4"), mande uma: "muda o título para X, a cor para azul e tira o M4".

## 3. Peça só o que muda

**O que pesa:** refazer a prancha ou a minuta inteira escreve tudo de novo, e o texto que o Claude escreve é o que mais pesa por palavra.

**Faça assim:** "troca a legenda do M3 para amarelo" ou "reescreve só o segundo parágrafo". Na edição, use a Mesa para o ajuste fino: ela roda no seu computador.

## 4. Imagens pesam

**O que pesa:** cada quadro do vídeo, print ou foto que o Claude olha é lido como imagem, e imagem pesa muito mais que texto.

**Faça assim:** deixe a conferência automática da zona segura trabalhar (ela roda no seu computador e só avisa o que precisa de olho). Peça para conferir por imagem só o momento que mudou: "confere só o M3". Mande prints recortados no trecho que importa.

## 5. Pausas longas custam uma releitura

**O que pesa:** o Claude guarda a conversa numa memória curta (o cache) por um tempo. Depois de uma pausa longa, a próxima resposta relê tudo do zero, e essa releitura pesa mais que a leitura guardada.

**Faça assim:** se você vai parar por horas e a conversa já está grande, peça "anota no andamento onde paramos" e, na volta, comece uma conversa nova.

## 6. Ligue só os conectores da tarefa

**O que pesa:** cada conector e cada plugin ligado acrescenta instruções a todas as conversas, mesmo quando você não usa. No registro de uso, isso aparece como peso alto já na primeira resposta.

**Faça assim:** desligue nas configurações os conectores que você não usa no marketing (por exemplo, o de agenda numa conversa de edição). Ligue de novo quando precisar.

## 7. Modelo certo para cada tarefa (decisão do Raphael)

**O que pesa:** o modelo mais forte gasta mais do limite a cada resposta.

**Proposta:** o mais forte para construir a base (Rito PICO) e para a Trava OAB em caso de dúvida; o intermediário para minutas, versões, legendas e edição. [CONFIRMAR COM O RAPHAEL]

## 8. Lote pequeno na edição (decisão do Raphael)

**O que pesa:** editar vários vídeos na mesma conversa poupa reler as instruções da edição, mas a conversa cresce a cada vídeo e as imagens se acumulam.

**Proposta:** até 3 vídeos parecidos por conversa; depois, conversa nova. Confira no "quanto eu gastei?" se o seu caso pesa menos em lote ou um por conversa. [CONFIRMAR COM O RAPHAEL]

## 9. Mande o trecho, não o arquivo inteiro

**O que pesa:** um PDF de 80 páginas é lido inteiro, mesmo que a pauta esteja em duas.

**Faça assim:** mande as páginas que importam ou diga "só o capítulo 3". O que entra no acervo uma vez fica resumido na base; não precisa mandar de novo.

## 10. Olhe o seu uso uma vez por semana

**Faça assim:** pergunte "quanto eu gastei esta semana?". O resumo mostra qual tarefa pesou mais e o que mais pesou nela. No Claude Code, ligue a linha de status para ver a sessão e a semana no rodapé. No Cowork e no aplicativo, o percentual oficial está em Configurações > Uso.
