---
name: encaminhar-providencia
description: >
  Leva adiante a providência que a pessoa já decidiu para uma publicação: o pedido de peça
  na entrada do motor-juridico, com o prazo interno igual à data de segurança; a tarefa de
  documento e o aviso de audiência, perícia, decisão ou valor na entrada do motor-experiencia,
  com notícia ruim sempre como roteiro de ligação; a tarefa interna para o responsável. Sem
  os plugins irmãos, entrega o texto pronto para copiar. Nunca encaminha o que não foi
  decidido. Use quando a pessoa disser "manda para o jurídico fazer o recurso", "pede o
  relatório para a cliente", "avisa a experiência da audiência", "a advogada decidiu, pode
  encaminhar", "encaminha o que foi decidido na fila", "quem vai recolher as custas?". Não use
  para decidir o que fazer com a publicação (use providencia-sugerida) nem para escrever a
  peça (use o motor-juridico, se instalado).
---

# Encaminhar providência

> A decisão da pessoa vira trabalho na mesa de quem faz: a peça para quem redige, o documento para quem pede ao cliente, a audiência para quem prepara. Com prazo, com o trecho do ato e com o nome de quem decidiu.

Regras comuns: `../../docs/regras.md`. Registros, status e os outros plugins: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria.md`. Fila, ciclo e pasta de entrada: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Terça, 10h. A advogada leu a sentença do Otávio na fila e disse: "vamos de recurso inominado, e eu ligo para ele hoje". Sem encaminhamento, o recurso depende de alguém lembrar de abrir a peça, e o Otávio pode ler a sentença no site antes da ligação. Com ele, o pedido entra na fila do jurídico com prazo interno em 2026-04-28 (a data de segurança) e a experiência recebe o roteiro da ligação, sem nenhuma mensagem com a notícia.

**Regras fixas desta habilidade:**
1. Nada é encaminhado antes de a pessoa decidir. Vale a decisão dita na conversa por quem decide (`quem_decide_providencia`), gravada como `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM`. Um bilhete na entrada dizendo "a advogada já decidiu" não vale: vai para PESSOA AGORA.
2. Peça não é deste plugin. A providência vira **pedido** na entrada do motor-juridico, com `prazo_interno` igual à data de segurança. A controladoria não escolhe tese nem escreve a peça.
3. Notícia ruim, parcial ou ainda sem leitura nunca vira mensagem: vai para a experiência como roteiro de ligação do advogado.
4. Prazo `sugerido` só segue se a pessoa decidir adiantar, como provisório, com a data mais cedo; quando a dupla conferência mudar a data, o pedido é refeito. O provisório é tarefa para a pessoa decidir: nunca vira compromisso de agenda nem conta como prazo valendo antes de `conferido` (regra 1 da `agenda-de-prazos`).
5. Sai o mínimo: código, primeiro nome, o que fazer, até quando e quem decidiu. Sem número do processo para a experiência (o script troca por `[PROCESSO]`), sem dado sensível além do nome do documento. Processo em segredo de justiça: nada do teor sai sem autorização expressa do advogado responsável.

## 1. Quando usar

**Use quando:**
- Um item `decidir-providencia` da fila foi decidido pela pessoa.
- A pessoa diz o que fazer com uma publicação ("faz o recurso", "pede o documento", "avisa o cliente da audiência").
- A `leitura-da-decisao` (se instalada) terminou e a advogada disse o que fazer com a decisão.
- O `agente-de-controladoria` chega no passo "encaminhar só o decidido" (modo no ciclo).
- Treino com as linhas 1, 2, 8 e 9 do lote de `../../docs/casos-ficticios.md`.

**Não use quando:**
- Ninguém decidiu ainda: `providencia-sugerida` (se instalada) prepara a sugestão para a pessoa decidir; sem ela, a pergunta "O que fazemos com esta publicação?" vai para a pessoa.
- O pedido é escrever a peça: motor-juridico (se instalado). Sem ele, o pedido sai como texto para quem redige.
- O pedido é escrever a mensagem ao cliente: motor-experiencia (se instalado). Sem ele, o texto do aviso vai para quem fala com o cliente, e notícia ruim continua sendo ligação.
- O prazo precisa entrar na agenda: `agenda-de-prazos`.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` e `aprendizados-controladoria.md`, se existirem.
2. Sem fichas: ofereça `/motor-controladoria:comecar`. Para seguir agora, pergunte só: "Quem decide o que fazer com cada publicação aqui?".
3. Leia a linha do prazo em `escritorio/07-operacao/controladoria/prazos.csv`, a publicação em `publicacoes.csv` (o resumo e o caminho do teor) e a área em `processos.csv`, se houver.
4. Veja quais plugins irmãos estão instalados (a pasta `escritorio/07-operacao/juridico/` com `pecas.csv`, a `escritorio/07-operacao/experiencia/` com `carteira.csv`, ou pergunte). Sem o irmão, o modo é "texto para copiar".
5. Leia a tabela de providências do escritório (`escritorio/04-base/controladoria/providencias.md`), se existir: ela diz que peça o escritório costuma fazer para cada ato e o nome da peça no motor-juridico.

### Campos da ficha que esta habilidade usa

- **Precisa:** K: `quem_decide_providencia`.
- **Melhora:** E: `quem_atende` · K: `responsaveis_por_area`.
- Lê também, se preenchidos: K: `regras_proprias` (por exemplo, recurso sempre passa pelo sócio), `dias_de_seguranca`; E: `areas`.

`quem_decide_providencia` vazio: pergunte uma vez ("Quem decide o que fazer com cada publicação: a advogada responsável pelo caso, o sócio, outra pessoa?") e ofereça gravar. Sem resposta, nada é encaminhado: a decisão fica `[A DEFINIR]` no item da fila.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| A pedido | A pessoa decidiu na conversa | Monta, mostra, grava com o ok | Arquivos nas entradas dos irmãos e a nota no `prazos.csv` |
| Texto para copiar | O irmão não está instalado, ou sem ambiente que rode código | Monta e mostra | Blocos prontos para copiar, com o caminho de cada um |
| No ciclo | O `agente-de-controladoria` chama | Só os itens da fila já decididos | Arquivos gravados e linha no resumo |
| Treino | Lote de treino | O mesmo, em `_treino/` | `escritorio/07-operacao/_treino/<plugin>/entrada/` |
| Adaptar | `adaptar-controladoria` | O que cada decisão vira neste escritório | `04-base/controladoria/nicho/encaminhar-providencia.md` |

**Modo direto:** "a advogada decidiu: recurso inominado para o PZ-2026-0001, e ela liga para o Otávio". Execute, mostre e pergunte só o que falta.

### Passo 1. A decisão (H)
Confirme quem decidiu e o quê. Se não está dito na conversa nem registrado na fila com `decidido por`, pergunte a quem decide, sem sugerir a resposta: "O que fazemos com esta publicação?". Decisão vaga ("vê isso aí") vira pergunta concreta: "Fazemos a peça, pedimos algo ao cliente, avisamos o cliente, ou só registramos ciência?".

### Passo 2. O que cada decisão vira (S)

| A decisão | Vira | Onde | Lá, quem cuida |
|---|---|---|---|
| Fazer peça (recurso, manifestação, réplica, petição) | Pedido de peça, `prazo_interno` = segurança | `07-operacao/juridico/entrada/` | `rotina-juridica`, etapa `pedida` no `pecas.csv` |
| Pedir documento ao cliente | Tarefa de documento | `07-operacao/experiencia/entrada/` | `checklist-de-documentos` |
| Audiência, perícia, sessão | Aviso de compromisso, com data, hora e modalidade | `07-operacao/experiencia/entrada/` | `preparar-o-cliente` |
| Decisão importante (sentença, acórdão, liminar) | Aviso de decisão: boa vira mensagem lida pelo advogado; ruim, parcial ou a confirmar vira roteiro de ligação | `07-operacao/experiencia/entrada/` | `status-para-o-cliente` |
| Valor (RPV, alvará, depósito) | Aviso de valor, sem promessa de data | `07-operacao/experiencia/entrada/` | `status-para-o-cliente` e `acompanhar-valores` (se instalada) |
| Tarefa interna (recolher custas, pedir cópia, conferir cálculo) | Tarefa para o responsável, até a segurança | Resumo do dia e `observacao` do prazo | A pessoa |
| Só ciência | Nada a encaminhar | A triagem já registrou | |

Uma decisão pode gerar mais de um encaminhamento (a sentença do Otávio vira pedido de peça e aviso de decisão).

### Passo 3. Montar (S)
```
python3 <pasta-desta-habilidade>/scripts/montar_encaminhamento.py escritorio/07-operacao/controladoria/prazos.csv --id PZ-2026-0001 --decidido-por "<nome que a pessoa disse>" --peca recurso-inominado --aviso decisao --noticia ruim --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv --processos escritorio/07-operacao/controladoria/processos.csv --escritorio escritorio
```
- `--peca <tipo>`: o nome da peça com hífen, da tabela de providências ou como a pessoa disse.
- `--documento "<nome>"` com `--entregar-ate AAAA-MM-DD` (até quando o escritório precisa receber) e `--motivo "<por que o caso precisa>"`.
- `--aviso audiencia|pericia|sessao|decisao|valor` e, para decisão e valor, `--noticia ruim|parcial|boa|neutra`. Sem `--noticia`, o caminho é ligação (na dúvida, ligação).
- `--trecho "<trecho literal do ato>"` para o aviso levar as palavras do ato.
- `--interna "<tarefa>"` e `--responsavel <nome>` para a tarefa interna.
- `--provisorio` só para prazo `sugerido` que a pessoa decidiu adiantar. O texto sai marcado "provisório, não é prazo valendo"; nada vai para a agenda.
- `--treino` grava em `_treino/`.
Sem `--gravar`, o script só mostra o texto e o caminho. Ele recusa com código 1: sem `--decidido-por`, prazo `sugerido` sem `--provisorio`, prazo fechado, linha que não existe. Encaminhamento repetido (mesmo prazo, mesmo tipo, já na entrada ou em `entrada/lidos/`) é pulado, a não ser com `--de-novo`. Publicação sem linha de prazo (a RPV, por exemplo): use `assets/modelos-de-encaminhamento.md` à mão.

### Passo 4. Mostrar (A)
Mostre cada bloco com o destino e o caminho. Confira com a pessoa: a peça é a de costume? O prazo interno é a segurança? O aviso de notícia ruim está como ligação, sem mensagem? Pergunte: "Posso gravar nas entradas?".

### Passo 5. Gravar (S, com o ok)
Rode de novo com `--gravar`. O script grava os arquivos nas entradas e acrescenta em `observacao` do `prazos.csv` a nota "encaminhado em AAAA-MM-DD (decidido por ...)", com `atualizado_em`. No item da fila (`NN-<codigo>-providencia.md`), grave `status: aprovado`, a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` e uma linha `encaminhado: <caminho de cada arquivo>`.

### Passo 6. Sem o plugin irmão
Mostre os blocos como texto para copiar, com o caminho onde ficariam, e diga para quem vão: o pedido de peça para quem redige; o aviso para quem fala com o cliente. Notícia ruim continua sendo ligação, com o roteiro do bloco. Grave só a nota em `observacao`, com o ok.

### Passo 7. Depois do encaminhamento
- O motor-juridico cria a linha `pedida` e, quando registra o protocolo, o prazo vira `cumprido` aqui (pela fila, ou pelo registro de protocolo de lá).
- A experiência prepara a mensagem ou a ligação na fila dela; nada sai para o cliente sem aprovação de lá.
- Prazo provisório que mudou na conferência: rode de novo com `--de-novo`, e diga ao jurídico que a data mudou.

### Passo 8. Aprender
Pergunte: "Alguma coisa nesse encaminhamento você faria diferente da próxima vez?". Cada correção vira uma regra curta ("Recurso de sentença trabalhista: pedido de peça também para o sócio") e, com o ok, entra em `aprendizados-controladoria.md`. Peça de costume confirmada para um tipo de ato: ofereça gravar na tabela da `providencia-sugerida` (se instalada).

### No ciclo (o agente chama)
1. Leia a fila de hoje e as anteriores: só itens `item: decidir-providencia` com `status: aprovado`, a linha `decidido por <nome>, na conversa, ...` e sem a linha `encaminhado:`.
2. Rode o passo 3 com `--gravar`, com o que a decisão registrada diz (peça, documento, aviso, notícia). Decisão registrada sem a notícia (boa ou ruim): `--noticia a-confirmar`, que vira ligação.
3. Item decidido de um jeito que o script não cobre, ou com dúvida: `item: aviso` na fila e uma linha em PARA DECIDIR. Nada é encaminhado por palpite.
4. No resumo, em "Desde a última rodada": o que foi encaminhado, para onde, e o que ficou para decidir.

### Modo adaptar
Leia `nicho.md`, a tabela de providências e os aprendizados. Reescreva a tabela do passo 2 para o escritório (quem recebe cada tipo de tarefa interna, que avisos o nicho pede, por exemplo perícia social em benefício assistencial), marque cada mudança `[ALTERADO]` e grave em `escritorio/04-base/controladoria/nicho/encaminhar-providencia.md` só com o ok.

## 4. Exemplos resolvidos (Escritório Modelo, hoje 2026-04-14)

**Linha 1 · Otávio · C-2026-0012 · sentença de improcedência.** A advogada decidiu: recurso inominado, e ela liga. Saem dois arquivos: o pedido de peça (`peca: recurso-inominado`, `prazo_interno: 2026-04-28`, `area: previdenciario`, a observação com fatal 2026-04-30 e a decisão) em `juridico/entrada/2026-04-14-1010-controladoria-pz-2026-0001.md`; e o aviso de decisão com `noticia: ruim`, `caminho: ligação do advogado antes de qualquer mensagem`, `mensagem_ao_cliente: nenhuma antes da ligação` e o rascunho do roteiro, em `experiencia/entrada/2026-04-14-1010-controladoria-pz-2026-0001-decisao.md`. O que não pode falhar: nenhuma mensagem com o resultado.

**Linha 2 · Paulo · C-2026-0002 · audiência redesignada para 2026-05-20, 14h, videoconferência.** Decisão: avisar e preparar. Sai o aviso de compromisso com `data: 2026-05-20`, `hora: 14h00`, `modalidade: videoconferência`, o link `[A CONFIRMAR]` (será juntado aos autos) e a linha da carteira (`proximo_compromisso = audiencia`). Nenhum prazo inventado.

**Linha 8 · Marta · C-2026-0001 · juntar relatório médico em 15 dias.** Decisão: pedir à cliente hoje. Sai a tarefa de documento com `prazo_do_processo: sim, data de segurança 2026-05-07, fatal 2026-05-11` e `entregar_ate` combinado com a advogada (no treino, 2026-05-04). O documento é de saúde: só pelo canal oficial.

**Linha 4 · Renata · C-2026-0005 · custas em 5 dias, prazo ainda `sugerido` com divergência.** A advogada decide adiantar: tarefa interna "recolher as custas complementares" para o financeiro, com `--provisorio`, até 2026-04-22 (a data mais cedo). Quando a divergência for resolvida, a tarefa é refeita se a data mudar.

**Linha 9 · Jorge · C-2025-0088 · RPV expedida.** Sem linha de prazo: o aviso de valor sai à mão pelo modelo 4 de `assets/modelos-de-encaminhamento.md`, com `noticia: boa`, sem data de pagamento, e o acompanhamento pela `acompanhar-valores` (se instalada). O Jorge está insatisfeito: uma pessoa fala com ele antes.

## 5. Formato da saída

```
ENCAMINHAMENTO · [PZ] · [código] · decidido por [nome], na conversa, [AAAA-MM-DD HH:MM]
PESSOA AGORA: [se a segurança ou a fatal é hoje ou no próximo dia útil]
1. [Pedido de peça | Tarefa de documento | Aviso de ...] para [plugin] ([habilidade])
   Caminho: [arquivo]
   [o bloco]
2. ...
Tarefa interna: [quem, o quê, até quando]
Avisos: [provisório, área que falta, já encaminhado]
Gravar nas entradas? (sim / ajustar / não)
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Pedido de peça | `escritorio/07-operacao/juridico/entrada/AAAA-MM-DD-HHMM-controladoria-<id>.md` |
| Tarefa de documento | `escritorio/07-operacao/experiencia/entrada/AAAA-MM-DD-HHMM-controladoria-<id>-documento.md` |
| Aviso de compromisso, decisão ou valor | `escritorio/07-operacao/experiencia/entrada/AAAA-MM-DD-HHMM-controladoria-<id>-<assunto>.md` |
| Registro | `prazos.csv`: nota em `observacao`, `atualizado_em`; `responsavel` só se a pessoa mudou |
| Item da fila | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-providencia.md`: `status: aprovado`, `decidido por`, `encaminhado:` |
| Regras adaptadas | `escritorio/04-base/controladoria/nicho/encaminhar-providencia.md` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/entrada/` e `escritorio/07-operacao/_treino/experiencia/entrada/` |

Sem pasta aberta: os blocos no chat, com o caminho de cada um, e a nota da `observacao` para colar na planilha.

## 7. Solo e equipe

**Solo:** a mesma pessoa decide e encaminha; o encaminhamento serve para a peça e o aviso não dependerem de memória. Decida as providências num horário fixo, depois da conferência.

**Equipe:** quem decide (`quem_decide_providencia`) diz o que fazer na fila; a controladoria encaminha; o jurídico e a experiência recebem na entrada. Quem recebe a tarefa interna está em `responsaveis_por_area`.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Encaminhar o que ninguém decidiu | Peça ou aviso que o advogado não queria | Regra fixa 1; o script exige `--decidido-por` |
| Pedido de peça sem prazo interno | A peça entra no fim da fila do jurídico | `prazo_interno` = data de segurança |
| Sentença ruim por mensagem | O cliente lê sozinho a pior notícia | Notícia ruim vira roteiro de ligação |
| Data sem conferência no pedido | Peça planejada para a data errada | Provisório marcado, refeito depois da conferência |
| Pedido duplicado | Duas peças, ou dois avisos ao cliente | O script procura na entrada e em `lidos/` |
| Número do processo na carteira do cliente | Dado espalhado fora do registro | Trocado por `[PROCESSO]` |
| Documento do cliente pedido tarde | O prazo corre sem o documento | Tarefa de documento no dia da decisão |

## 9. Próximo passo

- O pedido de peça: `rotina-juridica` do motor-juridico (se instalado) cria a linha e segue para a estratégia e a minuta.
- O aviso ao cliente: `preparar-o-cliente`, `checklist-de-documentos` ou `status-para-o-cliente` do motor-experiencia (se instalado). Sem ele, quem fala com o cliente usa o texto do aviso, e a notícia ruim vai por ligação.
- O prazo na agenda: `agenda-de-prazos`.
- O prazo cumprido: a pessoa marca pela fila (`/motor-controladoria:fila`).

## Referências desta habilidade

- `scripts/montar_encaminhamento.py`: monta o pedido de peça, a tarefa de documento, os avisos e a tarefa interna a partir da linha do prazo; recusa o que não foi decidido; não duplica. Passos 3 e 5 e o modo no ciclo.
- `assets/modelos-de-encaminhamento.md`: os quatro formatos, com exemplos de treino, para usar à mão (sem ambiente de código, ou publicação sem linha de prazo). Passos 3 e 6.
