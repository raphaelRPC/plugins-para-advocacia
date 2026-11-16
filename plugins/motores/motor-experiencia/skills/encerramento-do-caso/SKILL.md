---
name: encerramento-do-caso
description: >
  Fecha o caso com o cliente do jeito certo: monta a prestação de contas (valor recebido,
  honorários, despesas, repasse e prazo, com cada número vindo do advogado e conferido por ele),
  explica o que muda na vida do cliente depois da decisão ou do acordo, organiza a devolução e a
  guarda dos documentos, prepara a mensagem ou a reunião de encerramento (resultado ruim: ligação
  primeiro) e marca o encerramento na carteira com a pessoa. Gera o .docx da prestação de contas
  sem a parte interna. Use quando o advogado disser "o caso acabou", "faz a prestação de contas",
  "quanto fica para ela e para a gente", "como encerro com o cliente", "acordo homologado, e
  agora?", "devolve os documentos". Não use para dar a notícia da decisão ruim (use
  status-para-o-cliente).
---

# Encerramento do caso

> O caso acaba e o cliente precisa saber, por escrito e sem susto, o que entrou, o que ficou com o escritório, o que vai para ele, quando, e o que muda na vida dele a partir de agora.

Regras comuns: `../../docs/regras.md`. Campos das fichas: `../../docs/ficha-da-experiencia.md` e `../../docs/ficha-da-experiencia-modelo.md`. Carteira: `../../docs/carteira.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Pasta: `../../docs/pasta.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`. Adaptação: `../../docs/adaptar-ao-escritorio.md`. Treino: `../../docs/casos-ficticios.md`.

Sexta, 14h: "Quando eu recebo o dinheiro do acordo? E quanto fica para vocês?". O acordo foi homologado há uma semana e a cliente ainda não sabe o valor, a data nem a parte do escritório. Cada dia sem resposta vira desconfiança. Uma prestação de contas clara, conferida e entregue antes da pergunta mostra o trabalho e fecha o caso com confiança.

**Regras fixas desta habilidade:**
1. Nenhum número sai da cabeça da IA. Valor recebido, honorários, despesas, repasse e prazo vêm do advogado e dos comprovantes, e cada um passa pela conferência dele no cabeçalho interno "Antes de enviar".
2. Conferências e pendências ficam no cabeçalho interno. O texto que vai ao cliente não leva marcação; o script do .docx tira a parte interna e diz se está pronto.
3. Resultado ruim ou parcial: o advogado liga antes. A prestação de contas e a mensagem vêm depois da conversa.
4. `fase = encerrado` e `encerrado_em` só com a pessoa, depois do repasse feito e dos documentos resolvidos.
5. Nada de dado bancário no documento nem pedido de pagamento por mensagem. A conta de destino é confirmada por ligação ou pessoalmente.

## 1. Quando usar

**Use quando:**
- Saiu a decisão final, o acordo foi homologado, o benefício foi implantado ou o caso terminou por outro motivo (desistência, troca de advogado, fim do contrato).
- O cliente perguntou quanto vai receber, quando, ou quanto fica para o escritório.
- A carteira mostra o cliente em `fase = encerramento` e a prestação de contas não saiu.
- O ciclo apontou "prestação de contas pendente".

**Não use quando:**
- A decisão acabou de sair e é ruim: primeiro a ligação, pela `status-para-o-cliente` (se instalada). O encerramento vem depois.
- O caso ainda tem recurso ou fase pela frente: é andamento, não encerramento.
- O pedido é calcular o valor da condenação ou dos atrasados: isso é cálculo jurídico do advogado; esta habilidade só usa o número que ele der.
- O cliente quer saber a nota da pesquisa ou receber mensagem depois do caso: `pesquisa-de-satisfacao` e `relacionamento-depois-do-caso` (se instaladas).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-experiencia.md`), o `nicho.md` se existir e os aprendizados (`aprendizados-experiencia.md`).
2. **Leia o caso:** a linha da `carteira.csv`, o `clientes/<codigo>/historico.md`, o `clientes/<codigo>/documentos.md` (o que o cliente entregou), a abertura (`clientes/<codigo>/abertura.md`) e, se o motor-comercial estiver instalado, a passagem (`07-operacao/comercial/passagens/<codigo>.md`) com o que foi combinado de honorários. O contrato assinado é a fonte dos honorários.
3. **Reclamação aberta:** se `reclamacao_aberta = sim`, a pessoa que assumiu fala primeiro. O encerramento não fecha a reclamação sozinho.
4. **Sem ficha:** ofereça `/motor-experiencia:comecar`. Se quiserem seguir, pergunte só `prestacao_de_contas` e ofereça gravar.
5. **Conta de IA:** em conta pessoal, só o caso fictício (a Sueli), gravando em `escritorio/07-operacao/_treino/experiencia/`.

### Campos da ficha que esta habilidade usa

- **Precisa:** X: `prestacao_de_contas`.
- **Melhora:** X: `guarda_de_documentos`, `pesquisa_quando`, `contato_depois_do_caso`.

Lê também o tom, o tratamento, a `assinatura_das_mensagens` e os `dados_para_documentos` da ficha do escritório. Sem `guarda_de_documentos`, a seção de documentos sai com `[A DEFINIR]` e a pendência vai para o cabeçalho interno.

## 3. Fluxo

### Modos

| Modo | Quem chama | O que faz | O que não faz |
|---|---|---|---|
| A pedido | O advogado ou a equipe | Os passos 1 a 10, cada peça mostrada no chat | Não grava sem o ok; não manda nada |
| No ciclo | O `agente-de-suporte` | Acha quem está em `encerramento` sem prestação de contas e grava o rascunho com os campos em aberto; põe o cliente em "PARA DECIDIR" no resumo do dia | Nenhuma mensagem na fila com valor; não muda `fase` nem `encerrado_em` |
| Adaptar | A `adaptar-experiencia` (se instalada) | Reescreve as mensagens de encerramento e o "o que muda" para o nicho, cada mudança marcada `[ALTERADO]` | Só grava com o ok |
| Treino | Quem quer ver funcionando | O caso da Sueli do começo ao fim | Grava só em `_treino/experiencia/` |

### Passo 1. Como o caso terminou
Pergunte: "Como o caso terminou: resultado bom, parcial, ruim, acordo, desistência ou troca de advogado?". Parcial, ruim ou troca de advogado: pergunte "O cliente já sabe, por você, numa ligação?". Se não, pare aqui e prepare a ligação pela `status-para-o-cliente` (se instalada; sem ela, um roteiro curto: o que aconteceu, o que significa, o que dá para fazer, o que o escritório faz agora). Volte depois da conversa.

### Passo 2. Os números, um por vez
Pergunte, uma de cada vez, e anote a fonte de cada resposta:
1. "Quanto entrou no caso, e de onde? (depósito, alvará, acordo, benefício)"
2. "Quanto são os honorários, e qual a base no contrato?"
3. "Houve honorários pagos pela outra parte ao escritório? O contrato diz o que fazer com eles?"
4. "Quais despesas entram, e com comprovante?"
5. "Até quando o repasse sai?"
Resposta que não vem: o campo fica `[A PREENCHER]` no texto e a pendência entra no cabeçalho interno. A conta (recebido menos honorários menos despesas) é feita só com os números dados e marcada para conferência.

### Passo 3. Montar a prestação de contas
Use `assets/prestacao-de-contas-modelo.md`. O cabeçalho interno "Antes de enviar" lista cada conferência como item `- [ ]`, com a fonte. O texto de baixo é o que o cliente lê: o que aconteceu, a tabela de valores, quando e como recebe, documentos, o que muda, porta aberta e o aviso contra golpe. Caso sem valor a receber: a tabela vira uma frase verdadeira sobre os honorários.

### Passo 4. O que muda na vida do cliente
Escolha em `references/o-que-muda-por-area.md` os itens do tipo de caso e adapte ao nicho. Cada item que fala de prazo, valor de benefício ou regra de lei fica `[CONFERIR]` no cabeçalho interno até o advogado confirmar. Três a cinco itens, em linguagem do cliente.

### Passo 5. Documentos
Pergunte: "O que volta para o cliente, e como? O que fica guardado, e por quanto tempo?". Use `guarda_de_documentos` e o `documentos.md` do cliente. O prazo de guarda fica `[CONFERIR]` com a política do escritório e as normas aplicáveis. O que fica guardado e por quê entra no texto, em uma linha.

### Passo 6. Conferir e gerar o .docx
Mostre a prestação de contas e grave com o ok em `clientes/<codigo>/prestacao-de-contas.md`. Rode o script da pasta desta habilidade:

```
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" escritorio/07-operacao/experiencia/clientes/<codigo>/prestacao-de-contas.md --so-conferir
python3 "<pasta desta habilidade>/scripts/md_para_docx.py" escritorio/07-operacao/experiencia/clientes/<codigo>/prestacao-de-contas.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/encerramento-do-caso`. A primeira linha da saída diz "PRONTO PARA ENVIAR" ou "NÃO ESTÁ PRONTO PARA ENVIAR" e lista o que falta. O .docx sai sem o cabeçalho YAML e sem a seção "Antes de enviar". Sem `--forcar`, o .docx não é criado enquanto houver pendência no corpo (`[A PREENCHER]`, `[A DEFINIR]`, `[A CONFIRMAR]`, `[CONFERIR]`, campo do modelo entre colchetes em maiúsculas ou instrução do modelo entre colchetes): o script sai com código 2 e lista o que falta, para alguém resolver no .md e rodar de novo. Com `--forcar`, ele cria o arquivo mesmo assim, com a pendência em amarelo, e avisa que é só para revisão interna, nunca para enviar. Conferência do "Antes de enviar" sem marcar não impede o .docx, mas a saída continua "NÃO ESTÁ PRONTO PARA ENVIAR". Campo do envio entre chaves (`{...}`) não é pendência: aparece em verde no .docx para quem envia preencher. `--so-conferir` só confere o .md, sem criar nada. Para conferir um .docx que alguém editou à mão: `--conferir-docx <arquivo.docx>` (ali as chaves também contam, porque é o que vai ao cliente). É a mesma política do script do resumo mensal. Sem `python-docx`, nada é criado (código 1) e o .md continua sendo o documento.

### Passo 7. Mensagem ou reunião de encerramento
Pergunte: "Vai ser reunião, ligação ou mensagem com o documento?". Use `assets/mensagens-de-encerramento.md`:
- resultado bom: mensagem com o documento, ou reunião se o cliente preferir (A);
- parcial ou ruim: só depois da ligação; a mensagem registra o que foi conversado (A);
- troca de advogado ou desistência: mensagem curta, respeitosa, com a entrega dos documentos e a prestação de contas (A).
A pedido: mostre no chat. Se o escritório usa a fila: grave em `fila/AAAA-MM-DD/NN-<codigo>-encerramento.md`, status `pendente`, só com a prestação de contas pronta.

### Passo 8. Gravar o encerramento
Grave `clientes/<codigo>/encerramento.md` com: como terminou, data da ligação ou reunião, prestação de contas (caminho e versão), data do repasse e comprovante, documentos devolvidos e guardados, o que foi dito sobre o depois, e se o cliente aceitou receber contato depois do caso.

### Passo 9. Carteira e ganchos (com a pessoa)
Proponha e grave só com o ok:
- enquanto falta o repasse ou a entrega: `fase = encerramento`, `proximo_contato` = data do repasse, `motivo_proximo_contato = retorno-combinado`;
- quando tudo foi feito: `fase = encerrado`, `encerrado_em` = a data, `atualizado_em`; no `historico.md`, uma linha de trabalho do escritório para o que foi feito sem falar com o cliente (`| AAAA-MM-DD HHhMM | trabalho-do-escritorio | advogada | fez o repasse e conferiu o comprovante |`) e uma linha de contato para a mensagem, ligação ou reunião de encerramento (essa informa o caso e muda o `ultimo_contato`).
Depois pergunte, um de cada vez:
- "A ficha manda pesquisa no encerramento. Quer agendar?" Se sim: `pesquisa-de-satisfacao` (se instalada; sem ela, anote `motivo_proximo_contato = pesquisa` e a data).
- "O cliente aceitou receber contato depois do caso?" Se sim: `relacionamento-depois-do-caso` (se instalada; sem ela, anote no `encerramento.md` o que o cliente aceitou). Se não: `pediu_para_nao_receber = sim`.

### Passo 10. Aprender
Pergunte: "Alguma coisa na prestação de contas ou na mensagem você faria diferente?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-experiencia.md`. Política que se repete (por exemplo, "repasse sempre em até 5 dias úteis") é proposta para subir para `prestacao_de_contas` na ficha.

## 4. A prestação de contas

| Parte | O que leva | Quem confere |
|---|---|---|
| Valor recebido | Valor e origem (depósito, alvará, acordo) | Advogado, com o comprovante |
| Honorários | Valor e base (percentual ou valor do contrato) | Advogado, com o contrato |
| Honorários pagos pela outra parte | Como o contrato trata | Advogado, com o contrato |
| Despesas | Cada uma, com valor | Advogado, com comprovantes |
| Repasse | A conta, e só ela | Advogado |
| Prazo e forma | Data e "conta que você confirmou com a gente" | Advogado |
| Impostos e retenções | Se houver | Quem cuida da contabilidade `[CONFERIR]` |

Nunca entram: número de conta, CPF, número do processo, nome da outra parte além do necessário, valor que ninguém confirmou.

## 5. O caso da Sueli

Mensagem 7 dos casos fictícios: Sueli (C-2025-0091, família, alimentos, fase `encerramento`), acordo homologado, pergunta quando recebe e quanto fica para o escritório. A secretária manda uma resposta-ponte; a advogada dá os números, um por vez; a prestação de contas sai com o cabeçalho interno; o script mostra o que falta; a advogada confere, marca os itens e envia com a mensagem de encerramento; a carteira só muda para `encerrado` depois do repasse. O caso completo: `references/exemplo-sueli.md`.

## 6. Formato da saída

1. **Cartão:** cliente, como terminou, se o cliente já sabe, o que falta (números, documentos).
2. **Prestação de contas** em .md, com o cabeçalho interno, e o resultado do script.
3. **O que muda para o cliente**, dentro da prestação de contas.
4. **Mensagem de encerramento** ou roteiro da reunião.
5. **Linhas da carteira e do histórico** propostas, e os ganchos.

No ciclo: o rascunho gravado e uma linha em "PARA DECIDIR" no resumo do dia: "[CÓDIGO] [NOME]: prestação de contas esperando [O QUE FALTA]; rascunho em clientes/[CÓDIGO]/prestacao-de-contas.md".

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Prestação de contas (.md e .docx) | `escritorio/07-operacao/experiencia/clientes/<codigo>/prestacao-de-contas.md` e `.docx` |
| Registro do encerramento | `escritorio/07-operacao/experiencia/clientes/<codigo>/encerramento.md` |
| Roteiro da ligação (resultado ruim) | `escritorio/07-operacao/experiencia/clientes/<codigo>/ligacoes/AAAA-MM-DD.md` |
| Mensagem de encerramento (se usar a fila) | `escritorio/07-operacao/experiencia/fila/AAAA-MM-DD/NN-<codigo>-encerramento.md` |
| Linha do histórico | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` |
| Carteira | `escritorio/07-operacao/experiencia/carteira.csv`: `fase`, `encerrado_em`, `proximo_contato`, `motivo_proximo_contato`, `pediu_para_nao_receber`, `atualizado_em`, sempre com a pessoa |
| Mensagens adaptadas (modo adaptar) | `escritorio/04-base/relacionamento-com-o-cliente/biblioteca-de-mensagens.md`, chaves `encerramento-resultado-bom`, `encerramento-depois-da-ligacao`, `encerramento-troca-de-advogado` |
| Treino | `escritorio/07-operacao/_treino/experiencia/` |

Sem pasta aberta: a prestação de contas sai no chat pronta para copiar, sem o cabeçalho interno, e o cabeçalho sai à parte como lista de conferência.

## 8. Solo e equipe

**Solo:** a prestação de contas costuma ficar para "quando sobrar tempo". Faça logo depois do depósito, com os comprovantes abertos. Um modelo pronto e o script cortam a tarefa para minutos.

**Equipe:** a secretária ou o financeiro monta com os comprovantes; o advogado confere e marca os itens; quem envia é quem a ficha diz. O titular decide qualquer exceção de honorários (H).

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Valor escrito de cabeça | Cliente recebe número errado; desconfiança e risco ético | Regra fixa 1; cada número com fonte e conferência |
| `[CONFERIR]` no texto do cliente | Documento nunca fica pronto, ou sai com marcação | Cabeçalho interno; o script tira e avisa |
| Notícia ruim junto com a prestação de contas | Cliente descobre o resultado por um documento | Passo 1: ligação antes |
| Dados bancários por mensagem | Golpe e vazamento | Conta confirmada por ligação; aviso contra golpe no texto |
| Encerrar na carteira antes do repasse | Cliente some da régua com dinheiro pendente | `encerrado` só depois do repasse e dos documentos |
| Esquecer os documentos originais | Cliente volta meses depois procurando | Passo 5 e o registro do encerramento |
| Caso acaba e ninguém diz o que muda | Cliente não sabe o que fazer se a outra parte não cumprir | Passo 4, por área |

## 10. Próximo passo

- Notícia ruim antes do encerramento: `status-para-o-cliente` (se instalada).
- Pesquisa no encerramento: `pesquisa-de-satisfacao` (se instalada). Sem ela, anote a data na carteira e pergunte à mão as três perguntas da ficha.
- Contato depois do caso: `relacionamento-depois-do-caso` (se instalada). Sem ela, registre no `encerramento.md` o que o cliente aceitou.
- Insatisfação na conversa de encerramento: `reclamacao-e-recuperacao` (se instalada).

## Referências desta habilidade

- `assets/prestacao-de-contas-modelo.md`: o modelo com o cabeçalho interno "Antes de enviar". Use no passo 3.
- `assets/mensagens-de-encerramento.md`: as mensagens por tipo de fim e o roteiro da reunião de encerramento. Use no passo 7.
- `references/o-que-muda-por-area.md`: o que muda na vida do cliente, por área, para o advogado conferir. Leia no passo 4.
- `references/exemplo-sueli.md`: o caso fictício resolvido. Leia no modo treino.
- `scripts/md_para_docx.py`: confere e gera o .docx sem a parte interna. Rode no passo 6.
