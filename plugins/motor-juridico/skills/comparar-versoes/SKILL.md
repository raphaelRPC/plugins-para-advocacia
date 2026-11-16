---
name: comparar-versoes
description: >
  Compara duas versões de um documento (contrato e aditivo, a minuta nossa e a devolvida
  pela outra parte, acordo, peça v1 e v2, política antiga e nova): um script divide em
  cláusulas ou trechos, mostra o que ficou igual, mudou, entrou, saiu ou foi movido, com a
  diferença palavra por palavra e os sinais de risco (valor, prazo, negação, obrigação que
  virou faculdade, quitação, foro). Depois vem a leitura de risco de cada mudança, com quem
  ganha, quem perde, o que propor e o que conferir. Use quando o advogado disser "o que
  mudou nessa versão", "compara com a nossa minuta", "eles devolveram o contrato", "o que
  tem de diferente no aditivo", "confere a v2 da peça".
  Não use para conferir citações da peça (use conferir-citacoes) nem para montar o dossiê
  de vários documentos (use dossie-do-caso).
---

# Comparar versões

> Duas versões entram, cada cláusula sai marcada como igual, mudada, nova, excluída ou movida, e cada mudança ganha uma leitura de risco que o advogado decide.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Sexta, 18h. A advogada do outro lado devolve o acordo de divórcio "com pequenos ajustes de redação". São oito cláusulas. Num "deverá" que virou "poderá" e numa quitação geral que apareceu no fim, a cliente perde o direito de cobrar o carro. Lido na pressa, parece igual.

**Regras fixas desta habilidade:**
1. Toda mudança entra na lista, inclusive as que a outra parte não comentou. A habilidade não decide que uma mudança "é só redação".
2. O risco é qualitativo (`alto`, `médio`, `baixo`), sempre com o porquê. Nunca percentual.
3. O efeito jurídico de uma cláusula fica `[CONFERIR]` com o advogado. Aceitar, recusar ou contrapropor é decisão dele (e do cliente).
4. Valor de contraproposta vem do advogado ou do cliente, ou fica `[A DEFINIR]`.
5. O que vai para a outra parte (o e-mail com as observações, a versão com marcas) passa pelo advogado. A habilidade não envia nada.

## 1. Quando usar

**Use quando:**
- A outra parte devolveu uma minuta e o advogado quer saber o que mudou.
- Chegou um aditivo ou uma nova versão de contrato do cliente.
- A peça ganhou uma v2 (revisão do advogado, ajuste do estagiário) e é preciso saber o que mudou antes de conferir de novo.
- O `dossie-do-caso` achou o mesmo documento em duas versões (modo "a pedido de outra habilidade").
- Treino com o acordo fictício do caso 3 (modo "treino"), ou a `adaptar-juridico` (se instalada) pediu as cláusulas sensíveis do nicho (modo "adaptar").

**Não use quando:**
- O pedido é conferir as citações da peça: `conferir-citacoes` (se instalada). Esta habilidade só aponta que uma citação mudou.
- O pedido é conferir dados e coerência da peça: `conferir-peca` (se instalada).
- São muitos documentos diferentes de um caso: `dossie-do-caso`.

## 2. Antes de começar

1. **Leia as fichas** (`ficha-do-escritorio.md` e `ficha-juridica.md`, em `escritorio/04-base/comum/`). Leia `nicho.md`, se existir, e `04-base/juridico/nicho/comparar-versoes.md` (cláusulas sensíveis do nicho, do modo adaptar).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`).
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "Do ponto de vista de quem eu leio o risco: quem é o nosso cliente nesse documento?".
4. **As duas versões em texto.** O script lê `.txt`, `.md` e `.docx`. PDF: peça o .docx ou salve o texto. Versão com marcas de revisão do Word: peça a versão "limpa" de cada lado, ou aceite todas as marcas numa cópia antes.
5. **Dados.** Contrato de cliente só em conta profissional ou de equipe. Dados identificáveis que a tarefa não precisa ficam com a marcação das regras.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` |
| Melhora | J: `estilo` |

`estilo` entra na contraproposta (o texto sugerido sai no jeito de escrever do escritório). Sem ele, a contraproposta segue o estilo do próprio documento.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | O advogado manda as duas versões | Os dois arquivos | O relatório do script e a leitura de risco, no chat |
| Peça v1 x v2 | Nova versão de minuta do escritório | `minutas/<peca>-v1.md` e `-v2.md` | O que mudou e o que volta para conferência |
| No ciclo | O agente acha duas versões no caso | Os dois arquivos | Relatório gravado e item na fila. Não mostra nada |
| Treino | "É teste" | `assets/acordo-renata-v1.md` e `assets/acordo-renata-v2.md` | O mesmo, em `_treino/`, e a diferença com o gabarito da seção 4.4 |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | Cláusulas e palavras sensíveis do nicho, para aprovar |

Pedido direto ("compara estes dois"): não faça entrevista. Pergunte só qual é o nosso cliente, se não estiver claro.

### Passo 1. Identificar as versões
Qual é a A (a anterior, a nossa) e qual é a B (a nova, a deles)? Quem é o nosso cliente? Escreva os rótulos que vão no relatório ("nossa v1", "deles v2").

### Passo 2. Rodar o script
Rode `scripts/comparar.py` (seção 4.3) com os rótulos e, se o nicho tiver, as palavras sensíveis do escritório. O padrão divide por cláusula, artigo, item numerado ou título. Documento sem numeração: `--por paragrafo`.

### Passo 3. Conferir o alinhamento
Olhe a tabela do script. Trecho pareado errado (duas cláusulas diferentes tratadas como "alterado", com diferença quase total): diga isso no relatório e trate como uma exclusão e uma inclusão. Cláusula longa que virou duas: leia as duas juntas.

### Passo 4. Ler o risco de cada mudança
Para cada linha que não é `igual`, responda as perguntas de `references/leitura-de-risco.md`: o que mudou em uma frase, quem ganha e quem perde, o que pode dar errado, risco com o porquê, o que propor, o que conferir. `Movido` e `renumerado` sem mudança de texto: só confira as remissões internas.

### Passo 5. Ordenar e resumir
Ordene por risco (alto primeiro). Escreva o resumo de até 6 linhas (seção 5). Junte as perguntas para o cliente (o que só ele sabe: se aceita pagar o IPTU sozinho, se o valor do carro está certo).

### Passo 6. Mostrar e gravar
Mostre o resumo e a tabela de risco. Grave com o ok em `casos/<codigo>/comparacoes/<documento>-AAAA-MM-DD.md`, com o relatório do script no fim. Se o advogado pedir a resposta à outra parte, rascunhe as observações cláusula por cláusula como documento interno para ele revisar: nada sai daqui.

### Passo 7. Aprender
Pergunte: "Alguma mudança que eu marquei como risco e vocês sempre aceitam, ou o contrário?". A correção vira regra curta e, com o ok, entra em `aprendizados-juridico.md`. Palavra ou cláusula sensível nova: ofereça guardar em `04-base/juridico/nicho/comparar-versoes.md`, para o script receber na próxima vez.

### Modo peça v1 x v2
1. Rode o script nas duas versões da minuta.
2. Toda citação nova ou mudada perde a conferência anterior: liste para a `conferir-citacoes` (se instalada; sem ela, marque `[CONFERIR]` na própria minuta).
3. Todo dado mudado (nome, data, valor, número de documento) vai para a `conferir-peca` (se instalada; sem ela, liste no relatório para o advogado).
4. No `pecas.csv`, peça que estava `conferida` e ganhou mudança de citação ou dado volta a `minuta`, com `citacoes = nao-conferidas` ou `dados = nao-conferidos` (`producao.md`, regra 4). Mostre a mudança e grave com o ok; no ciclo, o agente pode gravar, porque `minuta` e essas colunas são dele.

### Modo no ciclo
1. O agente passa as duas versões e o caso. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 5. O nosso cliente é o do `pecas.csv`; se o documento não deixa claro de que lado ele está, nenhuma leitura de risco: só o relatório do script, e a pergunta vai para "para decidir".
3. Grave o relatório e um item na fila (`escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-comparacao.md`), no formato de `agentes-e-fila.md`, com `para: advogado`, `canal: interno`, `tipo: comparacao`, `revisor: pendente` e, em `antes_de_enviar`, as mudanças de risco alto.
4. Obrigação que virou faculdade, quitação ou renúncia nova, ou cláusula de proteção excluída: também em ADVOGADO AGORA, com uma frase.

### Modo treino
Use `assets/acordo-renata-v1.md` (minuta do escritório) e `assets/acordo-renata-v2.md` (devolvida pela outra parte), do caso 3 de `../../docs/casos-ficticios.md`. Grave em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0005/comparacoes/`. Mostre a diferença com o gabarito da seção 4.4.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Liste as cláusulas que mais importam nos documentos do nicho (no trabalhista patronal, por exemplo, jornada, remuneração variável e não concorrência) e as palavras que o script deve vigiar, `[CONFERIR]` com o advogado.
3. Marque `[NOVO]` ou `[ALTERADO]`, mostre e pergunte: "Falta alguma cláusula que vocês nunca deixam passar?".
4. Com o ok, grave em `04-base/juridico/nicho/comparar-versoes.md`, com uma linha `palavras:` separada por ponto e vírgula, que vai direto para o `--palavras` do script.

## 4. Critérios

### 4.1 Situações
| Situação | Quer dizer |
|---|---|
| igual | Mesmo texto (espaço e maiúscula não contam) e mesmo número |
| renumerado | Mesmo texto, número diferente |
| movido | Mesmo texto (ou quase), em outro lugar do documento |
| alterado | O trecho existe nas duas versões, com texto diferente |
| incluído | Só existe na versão B |
| excluído | Só existe na versão A |

### 4.2 Risco
`alto`: tira do cliente um direito ou uma proteção, cria dever ou custo relevante para ele, ou muda valor, prazo ou exigibilidade. `médio`: muda o jeito de cumprir sem tirar direito (prazo um pouco maior, forma de pagamento). `baixo`: redação, ordem, numeração. Cada um com o porquê. Na dúvida entre dois, o mais alto.

### 4.3 O script
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/comparar-versoes`; sem a variável, use o caminho da pasta desta habilidade.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/comparar-versoes/scripts/comparar.py" \
  "escritorio/07-operacao/juridico/casos/C-2026-0005/documentos/acordo-v1.docx" \
  "escritorio/07-operacao/juridico/casos/C-2026-0005/documentos/acordo-v2.docx" \
  --rotulos "nossa v1" "deles v2" --palavras "partilha; usufruto" \
  --saida "escritorio/07-operacao/juridico/casos/C-2026-0005/comparacoes/acordo-script.md"
```

O `scripts/comparar.py` divide por cláusula (ou `--por paragrafo`), alinha as versões, marca a situação de cada trecho, mostra a diferença palavra por palavra (`[-saiu-]` e `{+entrou+}`) e os sinais: número, valor ou data que mudou; negação que entrou ou saiu; obrigação que virou faculdade (ou o contrário); palavra sensível no trecho que mudou. `--palavras` soma as do escritório às do script (marcação como `[A PREENCHER]` é ignorada). Arquivo que não existe, vazio, PDF ou .docx inválido: código 1 e a mensagem.

### 4.4 Conferência com o acordo de treino
Comparando `assets/acordo-renata-v1.md` com `assets/acordo-renata-v2.md`, do ponto de vista da Renata:

| Mudança | Situação no script | Risco | Por quê |
|---|---|---|---|
| Carro: "deverá" virou "poderá" pagar | alterado; obrigação virou faculdade | alto | O pagamento da metade do carro deixa de ser exigível |
| Carro: valor de R$ 30.000 para R$ 24.000, 3 para 6 parcelas, sem correção, sem multa por atraso (valores de exemplo) | alterado; número mudou; negação entrou | alto | Menos dinheiro, mais tempo e nenhuma consequência pelo atraso |
| Quitação plena e geral sobre todos os bens | incluído | alto | Pode impedir cobrar o que não estiver no acordo `[CONFERIR]` o alcance |
| Multas e IPVA anteriores do carro | excluído | alto | Dívida antiga sem responsável definido |
| Imóvel: venda em 24 meses em vez de 12 | alterado; número mudou | médio | A parte dela no imóvel demora mais a virar dinheiro |
| Imóvel: Renata paga sozinha IPTU e condomínio até a venda | alterado; palavra sensível | alto | Custo novo só para a cliente; perguntar a ela |
| Despesas do processo foram para a cláusula 2ª | movido | baixo | Mesmo texto; conferir remissões |
| Cláusula dos filhos virou 3ª | renumerado | baixo | Mesmo texto |

E não pode: tratar a v2 como "ajustes de redação"; dizer que aceitar é bom ou ruim para a cliente; inventar o valor de uma contraproposta.

## 5. Formato da saída

**No chat, primeiro:**

```
COMPARAÇÃO · [documento] · [rótulo A] x [rótulo B] · do ponto de vista de [cliente]
Mudanças: [N] (alto [N], médio [N], baixo [N]); iguais: [N]
A mais séria: [uma frase]
Para o advogado decidir: [aceitar, recusar ou contrapropor, as de risco alto]
Para perguntar ao cliente: [o que só ele sabe]
Para conferir: [efeito jurídico, citação ou dado que mudou]
```

**A tabela de risco:**

| # | Cláusula | O que mudou | Quem ganha, quem perde | Risco e porquê | O que propor | Conferir |
|---|---|---|---|---|---|---|

Depois, o relatório do script, para quem quiser ver palavra por palavra.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Comparação (resumo, risco e relatório do script) | `escritorio/07-operacao/juridico/casos/<codigo>/comparacoes/<documento>-AAAA-MM-DD.md` |
| Item na fila (ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-comparacao.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/casos/<codigo>/comparacoes/` |
| Cláusulas e palavras do nicho | `escritorio/04-base/juridico/nicho/comparar-versoes.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

No modo peça v1 x v2, o `pecas.csv` volta a peça a `minuta` quando citação ou dado mudou (com o ok, a pedido). Sem pasta aberta: o relatório no chat, em bloco pronto para copiar, com o caminho onde ficaria.

## 7. Solo e equipe

**Solo:** rode antes de responder qualquer minuta devolvida, mesmo a "com pequenos ajustes". A tabela de risco vira o rascunho da sua resposta à outra parte.

**Equipe:** quem negocia o contrato roda a comparação; o advogado responsável lê só as de risco alto e decide. Na produção de peças, o modo v1 x v2 mostra ao revisor só o que mudou desde a última conferência.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Confiar no "só ajustes de redação" | Obrigação que vira faculdade passa sem ninguém ver | Toda mudança na lista, com o sinal do script |
| Ler só o que a outra parte comentou | Cláusula nova de quitação assinada sem leitura | Inclusões e exclusões listadas |
| Risco sem porquê | O advogado não sabe o que priorizar | Risco qualitativo com o motivo |
| Contraproposta com valor inventado | Negociação sobre número sem base | Valor do cliente ou `[A DEFINIR]` |
| Peça v2 com citação nova sem conferir | Citação errada no protocolo | v1 x v2 manda a citação de volta para a conferência |
| Remissão interna quebrada depois da renumeração | "Conforme a cláusula 4ª" aponta para outra coisa | Movidos e renumerados com a conferência das remissões |

## 9. Próximo passo

- Decidir o que fazer com as mudanças de risco alto: o advogado, com o cliente; se o caso muda de rumo, `estrategia-do-caso`.
- Peça v2: `conferir-citacoes` e `conferir-peca` (se instaladas) no que mudou.
- Testar a nossa posição contra a da outra parte: `advogado-do-diabo` (se instalada).
- Contar ao cliente o que mudou no acordo: `status-para-o-cliente`, do motor-experiencia (se instalado), com o advogado aprovando; sem ele, a pessoa que cuida do caso liga.

## Referências desta habilidade

- `references/leitura-de-risco.md`: as perguntas de cada mudança, os sinais do script, o que olhar por tipo de documento e como escrever a contraproposta. Leia no passo 4.
- `assets/acordo-renata-v1.md` e `assets/acordo-renata-v2.md`: as duas versões fictícias do acordo do caso 3. Use no modo treino.
- `scripts/comparar.py`: a diferença por cláusula (seção 4.3). Rode no passo 2.
