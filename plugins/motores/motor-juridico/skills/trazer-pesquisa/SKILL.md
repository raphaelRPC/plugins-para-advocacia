---
name: trazer-pesquisa
description: >
  Transforma a pesquisa de jurisprudência feita no Jus IA em base do escritório: separa cada
  julgado numa ficha (tribunal, número, órgão, relator, data, tese em uma frase, a favor ou
  contra, fonte com link), marca tudo como não conferido, pergunta a que tema e a que tese
  serve, e grava em 04-base/juridico/jurisprudencia/[tema].md por script, sem duplicar o que já
  está lá. Julgado sem número, data ou link não entra. Também roda o lote de conferência dos
  temas vencidos e grava o resultado de cada conferência. Use quando o advogado disser "guarda
  essa pesquisa na base", "trouxe isto do Jus IA", "organiza esses julgados", "atualiza o tema",
  "o que está vencido na base?", "vamos conferir os julgados do tema". Não use para conferir as
  citações de uma peça (use conferir-citacoes) nem para vigiar mudança de precedente (use
  monitor-de-precedentes).
---

# Trazer a pesquisa

> O que o advogado pesquisou no Jus IA vira ficha de julgado, por tema, com fonte e data, e fica na base do escritório para a próxima peça.

Como a pesquisa vira base: `../../docs/pesquisa-jus-ia.md` (o formato do arquivo de tema está lá). Regra de citação: `../../docs/citacoes.md`. Regras: `../../docs/regras.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quarta, 15h. A advogada pesquisou no Jus IA sobre perícia que ignora o relatório do médico assistente, achou três julgados bons e colou no chat. Daqui a dois meses, na próxima petição igual, ninguém vai lembrar onde ficou. Guardado como ficha, com o link, a data e um "contra" no julgado que a outra parte vai usar, ele aparece sozinho quando a `conferir-citacoes` cruzar a peça com a base.

**Regras fixas desta habilidade:**
1. Só entra com fonte: julgado sem tribunal, número, data do julgamento ou link não entra na base. Volta para o Jus IA.
2. Tudo entra "não conferido" e com a situação `[CONFERIR]`. A resposta do Jus IA ajuda a montar a ficha; quem dá a ficha por conferida é a leitura do inteiro teor na fonte.
3. A IA nunca completa relator, órgão, data ou número de memória. O que veio faltando fica `[CONFERIR]`.
4. Contra também entra, marcado "contra". A base sem o julgado contrário engana quem minuta.
5. A base guarda o julgado, não o caso: nenhum nome, código ou dado de cliente nas fichas.

## 1. Quando usar

**Use quando:**
- O advogado trouxe o resultado de uma pesquisa no Jus IA (texto colado, exportação, página salva).
- Um tema da base precisa de atualização com uma pesquisa nova (modo "atualização").
- É dia de conferir os temas vencidos da base (modo "lote de conferência").
- O `agente-juridico` achou uma pesquisa na pasta de entrada (modo "no ciclo").
- O `/motor-juridico:comecar` ou o advogado quer treinar com a pesquisa de exemplo (modo "treino").
- A `adaptar-juridico` (se instalada) pediu os temas e o roteiro de pesquisa do nicho (modo "adaptar").

**Não use quando:**
- O pedido é conferir as citações de uma peça: `conferir-citacoes`. Ela usa a base que esta habilidade grava.
- O pedido é saber se um precedente mudou e se uma tese foi afetada: `monitor-de-precedentes` (se instalada; sem ela, rode o lote de conferência e compare à mão).
- O pedido é ver como o tema é decidido, por tribunal e no tempo: `mapa-jurisprudencial` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`), em especial os da `trazer-pesquisa` (como o escritório nomeia temas, o que nunca guarda).
3. **Veja a base:** os temas em `escritorio/04-base/juridico/jurisprudencia/` e as teses em `escritorio/04-base/juridico/teses/`, se existirem. O roteiro de pesquisa do escritório, se o modo adaptar já gravou: `escritorio/04-base/juridico/jurisprudencia/_como-pesquisamos.md`.
4. **Conta de IA:** a pesquisa pode ter o caso do cliente na pergunta. Tire o que identifica antes de seguir; a base fica sem dado de cliente.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `pesquisa_de_jurisprudencia` |
| Melhora | J: `tribunais_principais`, `validade_da_conferencia` |

`pesquisa_de_jurisprudencia` já vem como Jus IA. `tribunais_principais` ordena as fichas e diz quais julgados pesam mais para o escritório. `validade_da_conferencia` (padrão de 90 dias) define o lote de conferência; sem ele, pergunte uma vez e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Uma pesquisa | O advogado trouxe o resultado | O que veio do Jus IA | Rascunho de fichas, e o tema gravado com o ok |
| Atualização | O tema já existe na base | A pesquisa nova e o tema | Só as fichas novas entram; a comparação vai ao advogado |
| Lote de conferência | Temas vencidos | A pasta da base | A lista do lote e cada conferência gravada |
| No ciclo | O agente achou pesquisa em `entrada/` | O arquivo da pesquisa | Rascunho e item na fila. Não grava na base |
| Treino | Pesquisa de exemplo | `assets/pesquisa-de-exemplo.md` | As três fichas, gravadas em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Ficha e nicho | Temas do nicho e roteiro de pesquisa, para aprovar |

Pedido direto ("guarda isso no tema tal"): não faça entrevista. Monte, mostre e pergunte só o que faltar.

### Passo 1. Receber e limpar
Leia o que veio. Separe: a pergunta feita, a data da pesquisa, a resposta do Jus IA e a lista de julgados. Se a pergunta tem dado de cliente ("a Marta, CPF tal"), troque pela situação ("segurada com benefício cessado") e avise em uma linha. Sem a data da pesquisa, pergunte: "Em que dia foi feita esta pesquisa?".

### Passo 2. O tema
Liste os temas que já existem na base e pergunte: "A que tema esta pesquisa serve? Pode ser um destes ou um novo." Tema novo: proponha um nome curto, com hífen e sem acento (por exemplo `pericia-e-relatorio`), e um título por extenso. Tema que já existe: siga no modo atualização.

### Passo 3. A tese
Pergunte: "A que tese do escritório ela serve?" e mostre as teses de `04-base/juridico/teses/`, se houver. Sem tese, a ficha diz para que serve em uma frase e o campo `teses_do_escritorio` do tema fica vazio.

### Passo 4. Montar as fichas
Uma ficha por julgado, no formato de `../../docs/pesquisa-jus-ia.md`:
- **Título:** `### TRIBUNAL · CLASSE E NÚMERO · AAAA-MM-DD` (data do julgamento).
- **Órgão e relator** como vieram; o que faltar, `[CONFERIR]`.
- **Tese em uma frase:** paráfrase do que a ementa trazida diz. Sem aspas.
- **Trecho útil:** paráfrase até a conferência. Entre aspas só depois de conferido palavra por palavra no inteiro teor.
- **Para que serve no escritório:** comece por `a favor`, `contra` ou `neutro`, e diga de qual tese ou contra qual argumento. A IA propõe; o advogado confirma cada "contra" (passo 6).
- **Fonte:** `Jus IA, pesquisa de AAAA-MM-DD, <link>`.
- **Conferência no inteiro teor:** `não conferido`.
- **Situação:** `` `[CONFERIR]` ``.

Julgado sem tribunal, número, data ou link: fica fora e vai para a lista "voltar ao Jus IA" ("faltou o link do terceiro julgado"). Súmula, tema ou precedente qualificado citado só na resposta do Jus IA, sem ficha: lista "citado na resposta, sem ficha", para pesquisar ou conferir no portal do tribunal. A resposta do Jus IA não é fonte: ela pode inspirar um rascunho do "Como o tema está hoje", marcado `[A CONFIRMAR]`, que só o advogado escreve ou aprova.

### Passo 5. Rascunho e validação
Grave o rascunho em `escritorio/04-base/juridico/jurisprudencia/rascunhos/<tema>-AAAA-MM-DD.md` (o modelo é `assets/fichas-do-exemplo.md`) e rode:

```
python3 "<pasta desta habilidade>/scripts/fichas.py" validar \
  escritorio/04-base/juridico/jurisprudencia/rascunhos/<tema>-AAAA-MM-DD.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/trazer-pesquisa`. O script aponta, ficha por ficha: o que não entra (sem tribunal, número, data, link; dado de cliente), e os avisos (órgão e relator vazios, posição não marcada, fonte sem data, aspas sem conferência, situação fora das opções, ficha repetida). Ele sai com erro e uma mensagem clara quando falta o arquivo ou não há ficha nenhuma. Corrija o rascunho até não sobrar "NÃO ENTRA" que não seja de propósito.

### Passo 6. Mostrar
Mostre as fichas (seção 5), com os "contra" no topo, e pergunte: "Confere os que eu marquei contra, e posso gravar no tema [nome]?". Tema que já existe: antes, a comparação do modo atualização.

### Passo 7. Gravar no tema
Com o ok:

```
python3 "<pasta desta habilidade>/scripts/fichas.py" juntar \
  escritorio/04-base/juridico/jurisprudencia/rascunhos/<tema>-AAAA-MM-DD.md \
  escritorio/04-base/juridico/jurisprudencia/<tema>.md \
  --titulo "<título do tema>" --teses <tese> --gravar
```

Sem `--gravar`, o script só mostra o que faria. Ele cria o tema pelo modelo se não existir, junta só as fichas novas (a ficha que já está na base não muda, mesmo que o rascunho diga outra coisa), sobe a versão, atualiza `revisado_em` e escreve a linha do histórico. Ficha repetida com conferência diferente aparece como aviso, para conferir.

### Passo 8. Conferir agora ou na hora de usar
Pergunte: "Quer conferir agora no inteiro teor? São N julgados." Se sim, siga o modo lote de conferência só para este tema. Se não, as fichas ficam "não conferido", e a `conferir-citacoes` pede a conferência quando uma peça usar o julgado.

### Passo 9. Aprender
Pergunte: "Alguma ficha você montaria diferente, ou algum jeito de nomear tema que vocês preferem?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Correção que afrouxa a regra fixa 1 ("pode guardar sem o link, eu acho depois"): explique por que não entra e proponha "a ficha fica no rascunho até o link chegar".

### Modo atualização
1. Monte o rascunho da pesquisa nova (passos 1 a 5).
2. Se a `monitor-de-precedentes` estiver instalada, rode a comparação dela (rascunho contra o tema) e mostre o resultado: julgados novos a favor e contra, mudança de situação, precedente qualificado novo, tese que pode estar afetada.
3. Sem ela, mostre o que o `juntar` sem `--gravar` diz (entram, já estavam, não entram) e destaque os "contra" novos.
4. O "Como o tema está hoje" não muda sozinho: se a pesquisa nova mexe na corrente, proponha o texto `[A CONFIRMAR]` e o advogado decide.

### Modo lote de conferência
1. Rode o lote dos temas vencidos:

```
python3 "<pasta desta habilidade>/scripts/fichas.py" vencidos escritorio/04-base/juridico/jurisprudencia
```

   Ele lista, por tema: julgados não conferidos, com conferência vencida (pela `validade_da_conferencia` da ficha jurídica, ou 90 dias), amarelos e com situação a conferir; e os temas cuja última pesquisa passou da validade ("PESQUISA NOVA NO JUS IA"). `--hoje` e `--validade` valem por cima.
2. Para cada julgado: abra o link e o inteiro teor no portal do tribunal (ou peça ao advogado para colar). Confira os cinco dados (tribunal, número, órgão, relator, data), a tese, e se não foi reformado ou superado. Sem o inteiro teor na conversa, não marque: a ficha fica como está.
3. Mostre o resultado de cada um e, com o ok, grave:

```
python3 "<pasta desta habilidade>/scripts/fichas.py" marcar escritorio/04-base/juridico/jurisprudencia/<tema>.md \
  --julgado <número> --cor verde|amarelo|vermelho --data AAAA-MM-DD \
  --onde "inteiro teor no portal do tribunal" [--situacao vigente] --gravar
```

4. Tema com pesquisa vencida: a lista do que pesquisar de novo no Jus IA vai ao advogado (a `monitor-de-precedentes`, se instalada, monta essa lista com mais detalhe).

### Modo no ciclo
1. O agente passa o arquivo de `07-operacao/juridico/entrada/` (por exemplo `2026-04-08-1500-jus-ia.txt`). Não pergunte nada e não mostre nada.
2. Rode os passos 1, 4 e 5 com o tema mais provável (pela base e pela pergunta da pesquisa), marcado `[A CONFIRMAR]` no cabeçalho do rascunho.
3. Não grave no tema. Grave um item na fila (`07-operacao/juridico/fila/AAAA-MM-DD/NN-base-<tema>.md`), no formato de `../../docs/agentes-e-fila.md`, com `tipo: pesquisa-para-a-base`, `revisor: pendente`, o caminho do rascunho e, em `antes_de_enviar`, o tema proposto, os "contra" para confirmar e o que não entrou.
4. Devolva ao agente: o caminho do rascunho, quantas fichas, quantas contra, quantas não entraram.

### Modo treino
A pesquisa de `assets/pesquisa-de-exemplo.md` (três julgados inventados, marcados EXEMPLO). O resultado esperado está em `assets/fichas-do-exemplo.md`. Tudo grava em `escritorio/07-operacao/_treino/juridico/jurisprudencia/`, nunca na base real.

```
python3 "<pasta desta habilidade>/scripts/fichas.py" validar "<pasta desta habilidade>/assets/fichas-do-exemplo.md"
```

O teste passa quando: as três viram fichas; as três ficam "não conferido" e com a situação `[CONFERIR]`; a terceira entra marcada "contra"; nenhuma tem aspas; e, numa peça que cite uma delas, a `conferir-citacoes` diz "está na base sem conferência" (nenhuma é usada sem a conferência). Numa conferência de verdade, as três saem vermelhas: os números não existem.

### Modo adaptar
1. Leia a ficha, `nicho.md` e os temas que já existem.
2. Proponha: os temas que o nicho mais pesquisa, com nome curto; as perguntas de pesquisa que funcionam no Jus IA para cada tema (do jeito que o escritório pesquisa); e os tribunais e órgãos que pesam mais.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Algum tema vocês chamam de outro jeito?".
4. Com o ok, grave em `escritorio/04-base/juridico/jurisprudencia/_como-pesquisamos.md` (o sublinhado no começo deixa o arquivo fora da leitura dos scripts).

## 4. O que a base guarda e o que não guarda

| Guarda | Não guarda |
|---|---|
| O julgado: tribunal, número, órgão, relator, data, tese, link | Nome, código ou documento de cliente |
| Para que serve no escritório, a favor ou contra | A estratégia de um caso específico |
| A data da pesquisa e a da conferência, com a cor | A resposta do Jus IA como se fosse fonte |
| O histórico do tema | Julgado sem número, data ou link |
| Paráfrase até a conferência; aspas depois dela | Aspas que ninguém conferiu |

## 5. Formato da saída

```
PESQUISA PARA A BASE · tema [nome] · pesquisa de AAAA-MM-DD
Fichas: N · a favor N · contra N · neutro N · não entram N
CONTRA (confirme)
  - [TRIBUNAL · CLASSE E NÚMERO · DATA] · [tese em uma frase]
A FAVOR
  - ...
NÃO ENTRAM (voltar ao Jus IA): [o que faltou em cada um]
Citado na resposta, sem ficha: [súmula, tema, precedente]
Rascunho: [caminho] · Tema: [caminho] (novo | versão N)
Conferência: todas "não conferido"; lote agora? [sim | na hora de usar]
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Rascunho das fichas | `escritorio/04-base/juridico/jurisprudencia/rascunhos/<tema>-AAAA-MM-DD.md` |
| Tema da base (criado ou atualizado) | `escritorio/04-base/juridico/jurisprudencia/<tema>.md` |
| Roteiro de pesquisa do escritório (modo adaptar) | `escritorio/04-base/juridico/jurisprudencia/_como-pesquisamos.md` |
| Item da fila (modo no ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-base-<tema>.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/jurisprudencia/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O registro de peças (`pecas.csv`) não muda. A base fica em `04-base/` e pode ir inteira para o Projeto no Claude. Sem pasta aberta: as fichas saem num bloco pronto para colar no arquivo do tema, com o caminho.

## 7. Solo e equipe

**Solo:** guarde toda pesquisa que valeu a pena, mesmo a pequena. Em seis meses, a base responde metade das perguntas antes de abrir o Jus IA. Separe meia hora por mês para o lote de conferência.

**Equipe:** quem pesquisa pode ser o estagiário; quem confirma os "contra" e escreve o "Como o tema está hoje" é o advogado responsável pela área (campo `dono` do tema). O lote de conferência pode ser dividido por tema, e a cor verde fica com quem leu o inteiro teor.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Pesquisa boa perdida no chat | Pesquisar de novo na próxima peça | Ficha no tema, com link e data |
| Julgado sem link na base | Ninguém consegue conferir depois | Regra fixa 1: não entra |
| Resposta do Jus IA tratada como fonte | Tese que nenhum julgado sustenta | A resposta só inspira o rascunho `[A CONFIRMAR]` |
| Base só com o que é a favor | Peça surpreendida pelo contrário | Regra fixa 4: contra entra marcado |
| Aspas de ementa nunca conferidas | Trecho errado copiado na peça | Paráfrase até a conferência; o script avisa |
| Ficha duplicada com dados diferentes | Duas versões do mesmo julgado | `juntar` não mexe no que já está e avisa |
| Dado de cliente na base | Exposição no Projeto do escritório | Regra fixa 5; o script barra código e CPF |

## 9. Próximo passo

- Peça que vai usar o tema: `conferir-citacoes` (se instalada) cruza a peça com a base.
- Tema com muita divergência: `mapa-jurisprudencial` (se instalada).
- Temas vencidos e teses afetadas, toda semana: `monitor-de-precedentes` (se instalada); sem ela, o lote de conferência desta habilidade uma vez por mês.
- Julgado contrário novo: `advogado-do-diabo` (se instalada) usa os "contra" do tema.

## Referências desta habilidade

- `scripts/fichas.py`: valida fichas, junta o rascunho ao tema sem duplicar, monta o lote de conferência e grava cada conferência. Rode nos passos 5 e 7 e no modo lote.
- `assets/pesquisa-de-exemplo.md`: um resultado colado do Jus IA com três julgados inventados (EXEMPLO), um contrário à tese. Use no modo treino.
- `assets/fichas-do-exemplo.md`: as três fichas montadas a partir da pesquisa de exemplo, o resultado esperado do treino e o modelo do rascunho. Use nos passos 4 e 5 e no modo treino.
