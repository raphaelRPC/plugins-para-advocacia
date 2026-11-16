# Citação de norma, súmula e julgado

No motor-juridico, citar é o trabalho. Uma peça sem artigo, súmula e precedente não se sustenta, e uma peça com citação errada ou inventada é o pior erro que a IA pode levar ao processo. Por isso, aqui a regra dos outros plugins motor (normas só pelo nome) não vale. Vale esta.

## A regra

1. **Toda citação nasce marcada.** Lei, artigo, súmula, tese de repetitivo, tema de repercussão geral, julgado, doutrina: quando uma habilidade escreve ou recebe uma citação que ainda não foi conferida, ela entra assim:

   `art. 59 da Lei 8.213/1991 [CONFERIR: vigência e redação]`
   `Súmula X do TRIBUNAL [CONFERIR: existe, não foi cancelada, enunciado igual]`
   `TRIBUNAL, RECURSO nº [NÚMERO], Rel. [NOME], julgado em [DATA] [CONFERIR: existe, número, relator, data, diz o que a peça diz]`

2. **A conferência tira a marca.** Quando a `conferir-citacoes` (ou o advogado) confere a citação na fonte, a marca sai do texto e a conferência vai para o registro da peça (seção 4). A peça final não tem nenhuma marca.
3. **Citação que não passou** fica em vermelho no relatório e não vai para a peça: sai, é trocada por outra conferida, ou o advogado decide.
4. **A IA nunca completa número, relator, data ou enunciado de julgado, súmula, tema ou doutrina de memória.** Se ela não tem a fonte na conversa, na base do escritório ou numa pesquisa trazida, escreve o molde (`TRIBUNAL, RECURSO nº [NÚMERO]...`) e o que precisa ser achado, e marca. Um julgado "provável" não existe para o plugin.
   **Lei e artigo são a exceção, sempre marcados.** A IA pode indicar a lei e o artigo que entende aplicáveis (`art. 59 da Lei 8.213/1991 [CONFERIR: vigência e redação]`), porque a conferência é rápida e a fonte é pública. Ela nunca põe entre aspas o texto da lei de memória: transcrição só depois de conferida no texto oficial (regra 6). Sem certeza do artigo, escreve `[ARTIGO] da Lei 8.213/1991 [CONFERIR: qual artigo trata de X]`.
5. **Citação já conferida e guardada na base** (`04-base/juridico/jurisprudencia/`) pode ser usada sem nova marca, se a conferência tiver menos de 90 dias (ou o prazo que a ficha jurídica definir em `validade_da_conferencia`). Passado o prazo, volta a ser marcada.
6. **Trecho entre aspas** é conferido palavra por palavra. Paráfrase não vai entre aspas. Trecho de documento do próprio caso (carta do INSS, laudo, contrato) entre aspas é conferido contra o documento, não como citação.
7. **Quem conferiu fica escrito.** No registro (seção abaixo), a coluna "O que foi feito" diz quem conferiu: `conferido pela habilidade na fonte <link ou arquivo>` ou `conferido por <nome>, informado na conversa em AAAA-MM-DD`. A IA só escreve que uma pessoa conferiu quando a própria pessoa diz isso na conversa.

## Onde conferir

| O que | Onde |
|---|---|
| Lei e artigo | Texto compilado no portal oficial da legislação federal, estadual ou municipal (Planalto, assembleia, câmara). Conferir a redação vigente na data dos fatos e na data da peça |
| Súmula, tese de repetitivo, tema de repercussão geral | Portal do próprio tribunal (STF, STJ, TST, TNU, tribunal local), página de súmulas e de temas |
| Julgado | Pesquisa no Jus IA e conferência do inteiro teor na fonte; ou o inteiro teor no portal do tribunal |
| Doutrina | O livro ou artigo, com edição e página |

O jeito de trazer a pesquisa do Jus IA para a base está em `pesquisa-jus-ia.md`.

## As cores do relatório de conferência

| Cor | Quer dizer | O que acontece |
|---|---|---|
| verde | Conferida na fonte: existe, vigente, número, data e relator certos, e diz o que a peça diz | A marca sai |
| amarelo | Existe, mas tem algo a ajustar: redação mudou, número trocado, a peça diz mais do que o julgado diz, precedente superado em parte | O advogado ajusta, e a citação volta a ser conferida |
| vermelho | Não encontrada, cancelada, revogada, ou diz o contrário | Sai da peça ou o advogado decide |
| cinza | Não deu para conferir agora (fonte fora do ar, sem acesso) | A marca fica; a peça não vai para protocolo |

## O registro da conferência

Cada peça tem, em `07-operacao/juridico/casos/<codigo>/conferencias/<peca>-AAAA-MM-DD.md`, a tabela:

| # | Citação como está na peça | Fonte consultada | Data da consulta | Cor | O que foi feito |
|---|---|---|---|---|---|

Esse registro fica com o escritório. Ele não vai para o processo.
