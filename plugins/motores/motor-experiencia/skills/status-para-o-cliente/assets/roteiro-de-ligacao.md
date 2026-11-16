# Roteiro de ligação para notícia difícil (H)

Quem liga é o advogado responsável. A IA prepara o roteiro a partir da movimentação e do histórico; a conversa é dele. O roteiro é para ler em cinco minutos antes de ligar, não para ler em voz alta. Grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md`: é documento interno, nunca vai ao cliente.

Use para: decisão desfavorável, parcial ou que encerra o processo sem decidir; benefício negado; laudo contrário; bloqueio contra o cliente; decisão que o cliente precisa tomar (acordo, recorrer, desistir); erro ou atraso do próprio escritório; pergunta de andamento que veio com aflição, reclamação ou vontade de desistir.

```
ROTEIRO DE LIGAÇÃO · [CÓDIGO DO CLIENTE] · preparado em [DATA]
Quem liga: [ADVOGADO RESPONSÁVEL]       Quando: [HOJE, ATÉ HH:MM]
Antes, mandar o convite para ligação? [SIM: chave convite-para-ligacao, aprovado por quem liga | NÃO: ligar direto]

1. O QUE ACONTECEU (para o advogado, em duas frases)
[FATO, COM A DATA DA MOVIMENTAÇÃO]

2. COMO DIZER (uma frase, sem rodeio, sem termo técnico)
"[EX.: O juiz decidiu o seu processo e, desta vez, não deu razão ao nosso pedido.]"

3. O QUE ISSO SIGNIFICA PARA ELE
- [O QUE MUDA NA VIDA DELE AGORA, EX.: o benefício continua suspenso]
- [O QUE NÃO MUDA, EX.: ainda não é o fim; cabe recurso]

4. O QUE DÁ PARA FAZER (o advogado define; a IA não sugere estratégia)
- Opções: [A DEFINIR PELO ADVOGADO]
- Prazo processual para decidir: [DATA LIMITE, SE HOUVER, CONFERIDA NO PROCESSO]
- Custo de cada opção, se houver: [A DEFINIR]

5. PERGUNTAS QUE ELE PODE FAZER (e como responder sem prometer)
- "Vou perder?" → "Não tenho como te prometer um resultado. O que posso te dizer é o que dá para fazer agora e o que eu penso de cada caminho."
- "Quanto tempo mais?" → "Não sei te dizer quando sai a próxima decisão. Depende de [QUEM]. Te aviso a cada passo."
- "A culpa foi de quem?" → [SE FOR DO ESCRITÓRIO: reconhecer, dizer o que está sendo feito. SE NÃO: explicar o motivo da decisão, sem culpar o juiz ou a outra parte.]
- "Vale recorrer?" → [A RECOMENDAÇÃO DO ADVOGADO, COM O QUE ELA CUSTA E O RISCO, SEM PERCENTUAL DE CHANCE]
- [OUTRA PERGUNTA QUE O HISTÓRICO SUGERE]

6. O QUE NÃO DIZER
- Nada de "eu tinha certeza que ia dar certo", "o juiz errou", "isso nunca acontece".
- Nada de chance em percentual nem de prazo de decisão.
- Nada de pressa para decidir na ligação, se o prazo permite pensar.

7. FECHAR A LIGAÇÃO
- Repetir em uma frase o que foi combinado.
- Dizer quando volta a falar: [DATA OU "assim que houver novidade, e no máximo até DATA"].
- Perguntar: "Ficou alguma dúvida? Pode me escrever depois também."

8. DEPOIS DA LIGAÇÃO (é assim que o cliente sai de PESSOA AGORA)
- Mandar o registro por escrito (chave registro-depois-da-ligacao), no mesmo dia, pela fila de aprovação.
- Atualizar a carteira: `ultimo_contato` (hoje, `ligacao`, porque a ligação informou o caso), `proximo_contato` e `motivo_proximo_contato` (ex.: `retorno-combinado` na data limite para o cliente decidir), `humor` pela leitura de quem ligou.
- Anotar no histórico do cliente (`clientes/<codigo>/historico.md`) uma linha de contato, com o que foi combinado em uma frase e sem o conteúdo da conversa: | AAAA-MM-DD HHhMM | ligacao | advogada | ligação sobre a decisão; combinou novo contato em AAAA-MM-DD |
- Não ligou ainda? O item continua em PESSOA AGORA no resumo seguinte.
```

## Cuidados

- **Não por áudio, não por mensagem.** Se o cliente não atende, mande só o convite para ligação. A notícia não vai escrita antes da conversa.
- **Cliente idoso, doente ou com pouca familiaridade com o celular:** pergunte se ele quer alguém de confiança junto na ligação. Só fale do caso com outra pessoa se o cliente autorizou.
- **Luto, crise ou reação forte:** pare o roteiro, ouça, e combine falar de novo no dia seguinte. A decisão pode esperar se o prazo deixar.
- **Sinal de risco à vida** ("não aguento mais", "vou acabar com tudo"): a conversa deixa de ser sobre o processo. Fique na linha, oriente procurar ajuda agora (CVV, 188; emergência, 192 ou 190) e avise alguém próximo se o cliente concordar.
- **Cliente que pediu para não receber mensagens** (`pediu_para_nao_receber = sim`): a ligação continua sendo devida, porque notícia relevante do caso é dever do advogado; combine com ele o canal que vale.
- **Cliente que trouxe resposta de IA ou print do tribunal com a notícia:** ele pode já saber, ou achar que sabe. Comece perguntando o que ele entendeu, e corrija com calma.
