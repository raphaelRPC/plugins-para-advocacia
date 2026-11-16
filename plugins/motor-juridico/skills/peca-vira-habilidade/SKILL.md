---
name: peca-vira-habilidade
description: >
  Transforma de 3 a 5 peças boas do escritório, do mesmo tipo e anonimizadas, numa habilidade
  própria daquela peça: mapa do que é fixo, do que muda de um cliente para outro (variáveis com
  tipo e origem), das teses, dos trechos padrão e das escolhas de estilo; gera o SKILL.md no
  formato do plugin, testa em três casos (o comum, o com exceção e o que deve parar) e empacota
  por script que valida nomes e só aceita teste preenchido. Quando o advogado corrige uma peça
  gerada, atualiza a habilidade em nova versão. Use quando o advogado disser "transforma essa
  peça em habilidade", "a gente faz essa inicial sempre igual", "ensina o Claude a fazer a nossa
  réplica", "corrigi a minuta, atualiza a habilidade". Não use para redigir uma peça avulsa (use
  minutar-peca) nem para rotina que não é peça (use adaptar-juridico).
---

# A peça vira habilidade

> O modelo já existia, só não estava escrito. Esta habilidade lê as peças boas do escritório, separa o que é do escritório do que é de cada cliente e escreve isso como uma habilidade que redige a peça do mesmo jeito, toda vez.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e `pecas.csv`: `../../docs/producao.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Rotina nova vira habilidade: `../../docs/adaptar-ao-escritorio.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Aprendizados: `../../docs/aprender-com-o-uso.md`.

A advogada escreve a mesma inicial de restabelecimento há dois anos. As peças boas estão em pastas com o nome de cada cliente. O estagiário novo pega a de um homem para fazer a da Marta, e a peça sai com "o autor" no fato 1.4 e o valor da causa do outro cliente. O jeito do escritório existe, mas só na cabeça dela e espalhado em peças antigas.

**Regras fixas desta habilidade:**
1. **Do escritório, e só dele.** O mapa sai de 3 a 5 peças boas do escritório, do mesmo tipo, anonimizadas, e das respostas do advogado. Nada de modelo da internet. O que a habilidade sugerir vai marcado "sugestão" até o ok.
2. **Toda citação entra marcada.** Lei, artigo, súmula e julgado que aparecem nas peças entram no mapa e no modelo com `[CONFERIR: ...]`. Peça boa não é fonte conferida. A conferência é da `conferir-citacoes`.
3. **A habilidade gerada não escolhe tese** e para nas exceções que mudam o caminho do caso. Ela só redige depois da tese definida pelo advogado.
4. **Só sai testada.** Três casos (o comum, o com exceção e o que deve parar) com o resultado copiado sem corrigir, conferidos pelo advogado, e o script de empacotamento sem erro. Antes disso, não há .zip.
5. **Correção vira versão nova.** Quando o advogado corrige uma peça gerada, a mudança que vale para todo caso entra no mapa com nova versão, os três testes rodam de novo e sai um pacote novo. Ninguém edita a cópia instalada.

## 1. Quando usar

**Use quando:**
- Uma peça sai do escritório sempre do mesmo jeito e o advogado tem de 3 a 5 boas (modo "criar").
- O advogado corrigiu uma minuta feita pela habilidade própria e a correção vale para os próximos casos (modo "corrigir"; o comando `/motor-juridico:fila` oferece este caminho no "ajustar").
- A habilidade própria precisa de revisão: tese mudou, peça boa nova, aprendizados acumulados (modo "revisar").
- A `adaptar-juridico` pede a primeira habilidade própria do escritório (modo "adaptar").
- Alguém quer ver o caminho inteiro com o exemplo resolvido (modo "treino").

**Não use quando:**
- O escritório tem uma peça só, ou nenhuma boa: use a `minutar-peca` e volte quando houver três aprovadas.
- As peças são de tipos diferentes (inicial e recurso, ou duas áreas): separe por tipo e faça uma habilidade por peça.
- O pedido é uma rotina que não é peça (ordem dos documentos, lista de sexta): `adaptar-juridico`, parte de rotina nova.
- O pedido é escrever uma peça agora: `minutar-peca`, ou a habilidade própria se já existir.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-juridica.md`), o `nicho.md` (se existir) e `aprendizados-juridico.md`. Regras de escrita guardadas entram nas escolhas de estilo do mapa.
2. **Veja o que já existe:** `escritorio/04-base/habilidades-do-escritorio/` (habilidade da mesma peça já existe? então é modo "revisar" ou "corrigir"), `04-base/juridico/modelos/<peca>/` (as peças boas), `04-base/juridico/teses/` (as teses que a peça usa) e `07-operacao/juridico/pecas.csv` (que peça mais sai sem habilidade própria).
3. **Conta e dados.** Peças reais só em conta profissional ou de equipe, e anonimizadas antes de entrar: nome por `[CLIENTE]`, CPF por `[DOC]`, processo por `[PROCESSO]`, endereço por `[ENDEREÇO]`. Em conta pessoal, use o exemplo resolvido.
4. **Treino:** com o exemplo ou casos fictícios, tudo grava em `escritorio/07-operacao/_treino/juridico/` e a habilidade gerada fica em `_treino/juridico/habilidades/<peca>/`. A habilidade de treino nunca é usada nas peças reais nem instalada: no fim do treino, diga "Esta foi de treino. A do escritório sai das peças boas de vocês, no modo criar."

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `onde_estao_os_modelos`, `pecas_mais_feitas` |
| Melhora | J: `estilo`, `pedidos`, `tamanho_preferido` · também: `quem_redige`, `quem_revisa`, `quem_assina`, `pecas_em_massa` |

Sem `pecas_mais_feitas`, pergunte: "Qual peça sai mais do escritório, e sempre do mesmo jeito?". Sem `onde_estao_os_modelos`, pergunte onde estão as peças boas e ofereça gravar o caminho na ficha.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Criar | Peça sem habilidade própria | 3 a 5 peças boas do mesmo tipo | Mapa, SKILL.md, testes e o .zip |
| Corrigir | O advogado corrigiu uma minuta gerada | A minuta gerada e a revisada | Mapa e SKILL.md na versão seguinte, testes de novo, .zip novo |
| Revisar | Tese mudou, peça boa nova, aprendizados | A habilidade e o motivo | O mesmo do corrigir |
| Adaptar | A `adaptar-juridico` chama | A peça mais feita | O mesmo do criar, com o resultado devolvido a ela |
| Treino | Exemplo resolvido ou "é teste" | `references/exemplo/` | O caminho inteiro em `_treino/` |
| No ciclo | Não roda sozinha | | O ciclo só aponta candidatas e correções (seção 3, "No ciclo") |

### Modo criar

**Passo 1. Escolher a peça.** Sugira pela ficha e pelo `pecas.csv` (a peça que mais aparece com `habilidade_usada = minutar-peca`). Pergunte: "Vamos começar pela [peça]? É a que mais sai e sempre do mesmo jeito?". Uma peça por vez. O nome da habilidade é o da peça, em minúsculas e com hífen (`peticao-inicial-restabelecimento`), e é o mesmo que vai na coluna `peca` do `pecas.csv`.

**Passo 2. Receber as peças boas.** Pergunte: "Me passa de três a cinco peças boas desse tipo, as que você usaria de modelo. Antes, troque nome, CPF, endereço e número de processo por [CLIENTE], [DOC], [ENDEREÇO] e [PROCESSO]." Grave em `escritorio/04-base/juridico/modelos/<peca>/` (ou leia de onde `onde_estao_os_modelos` disser). Para cada uma, pergunte em uma linha: "Por que essa é boa?" (a resposta vai para a seção Origem do mapa). Com duas peças, avise que o que parece fixo pode ser coincidência e siga só se o advogado quiser. Com uma, não siga: `minutar-peca` até ter três.

**Passo 3. O mapa bruto.** Rode, com o caminho da pasta desta habilidade e o das peças:

```
python3 "<pasta desta habilidade>/scripts/mapear_pecas.py" "escritorio/04-base/juridico/modelos/<peca>/peca-1.md" "escritorio/04-base/juridico/modelos/<peca>/peca-2.md" "escritorio/04-base/juridico/modelos/<peca>/peca-3.md" --saida "escritorio/07-operacao/juridico/mapas/<peca>-mapa-bruto.md"
```

Aceita .md, .txt e .docx. O script compara as peças e devolve: os trechos fixos (iguais em todas), os fixos com variáveis (com `{{variavel}}` no lugar do que muda e o valor de cada peça), os que aparecem em algumas (exceções), os que são de uma só, as variáveis sugeridas com o tipo provável, as citações (todas `[CONFERIR]`) e os alertas de dado que não devia estar ali (CPF, telefone, e-mail, processo fora de citação). Alerta de dado: pare, peça a peça anonimizada e rode de novo. O mapa bruto é rascunho: os nomes das variáveis são sugestão e nada vira regra sem o advogado.

**Passo 4. Fechar o mapa com o advogado.** Uma pergunta por vez, só do que o mapa bruto não resolveu:
1. Trecho fixo que pode ser coincidência: "Este trecho está nas três peças. É o texto do escritório ou só repetiu nestas?"
2. Cada variável: "De onde vem [a função do cliente]: do extrato, da carteira ou do que ele conta?" (dá a `origem`). O tipo sai do valor (data, mês, valor, gênero, opção, lista).
3. Cada exceção (trecho em algumas peças ou em uma só): "Quando este trecho entra, e quem decide?" Se uma variável decide (o advogado pede tutela ou não), vira bloco condicional. Se muda a tese ou o caminho, vira "para e leva ao advogado".
4. Teses: "Qual tese do banco esta peça usa?" Sem arquivo da tese: siga, marque "sugestão: criar no banco de teses" e indique a `banco-de-teses-vivo` (se instalada).
5. Estilo: "O que você nunca escreve nesta peça?" e "Os pedidos saem sempre assim?" (junte com `estilo` e `pedidos` da ficha).
6. Quando parar: "Em que caso esta peça parece servir e não serve?"

Peça a cena quando a resposta vier vaga ("depende do caso" vira "e no último caso em que você tirou esse trecho, o que tinha de diferente?").

**Passo 5. Escrever o mapa.** No formato de `references/mapa-da-peca.md`, com as dez seções e os nomes exatos de colunas, porque a habilidade gerada, a `pecas-em-lote` e o script de empacotamento leem o mapa. Mostre inteiro e pergunte: "É assim que essa peça sai do escritório?". Grave com o ok, na versão 1.

**Passo 6. Gerar a habilidade.** Escreva o SKILL.md pelo `references/molde-da-habilidade.md`: frontmatter só com `name` e `description`, "Versão da habilidade: 1", regras fixas, quando usar, antes de começar com "Campos da ficha que esta habilidade usa", fluxo com S, A e H, o modo "No ciclo", o passo "Aprender" por último, o que entrega, solo e equipe, erros que evita, próximo passo. Mostre inteiro e grave com o ok em `escritorio/04-base/habilidades-do-escritorio/<peca>/SKILL.md`, com o mapa em `references/mapa-da-peca.md` da mesma pasta.

**Passo 7. Testar com três casos.** Combine com o advogado, uma pergunta por vez:
- **o comum:** "Qual é o caso típico dessa peça?" (um caso anonimizado ou fictício);
- **o com exceção:** um que ativa um bloco condicional ou tem uma divergência de documento;
- **o que deve parar:** outra área, outra peça, sem tese definida, ou a exceção da seção 7 do mapa.
Rode a habilidade gerada com cada um, em `_treino/`, copie o que saiu sem corrigir e registre em `escritorio/04-base/casos-de-teste/juridico/<peca>-testes.md`, no formato de `references/exemplo/testes.md`. Quem confere e escreve "Conferido por:" é o advogado. Falhou: ajuste o mapa ou o SKILL.md e rode os três de novo.

**Passo 8. Empacotar.** Da pasta de trabalho:

```
python3 "<pasta desta habilidade>/scripts/empacotar_habilidade.py" "escritorio/04-base/habilidades-do-escritorio/<peca>" --testes "escritorio/04-base/casos-de-teste/juridico/<peca>-testes.md"
```

O script confere: nomes de arquivo e pasta (`[a-z0-9._-]`, caminho até 100 caracteres), o frontmatter, a seção de campos, o passo "Aprender", o modo "no ciclo", a regra das citações, travessões, arquivos citados; no mapa, o cabeçalho, as variáveis e o modelo (toda variável do modelo declarada, toda obrigatória usada, blocos condicionais fechados, valores do escritório preenchidos); toda citação com número marcada `[CONFERIR]`; e os três testes com "O que saiu" preenchido, "Resultado: passou", a versão igual à do mapa e o "Conferido por". Com erro, sai com código 1 e a lista do que corrigir, e não gera nada. Sem erro, grava `escritorio/04-base/habilidades-do-escritorio/<peca>-v<versao>.zip`.

**Passo 9. Instalar e ligar.** Instalação: Personalizar > Habilidades > Enviar, com o .zip (conferir na configuração da conta). A partir daí, o `agente-juridico` usa a habilidade própria para as peças em `tese-definida` com aquele `peca` (ele lê `04-base/habilidades-do-escritorio/`), e o `pecas.csv` passa a registrar `habilidade_usada = <peca>`. Se `pecas_em_massa` cita esta peça, ofereça a `pecas-em-lote` (se instalada).

**Passo 10. Aprender.** Pergunte: "Alguma coisa no mapa ou na habilidade você faria diferente?". Correção da habilidade entra no mapa (versão seguinte, se já empacotada). Regra de escrita que vale para toda peça vai para `aprendizados-juridico.md`, com o ok. Sugira a próxima peça candidata.

### Modo corrigir

1. **Entrada:** a minuta que a habilidade própria gerou e a versão que o advogado revisou (o .md ajustado na fila, ou o .docx dele). Pergunte só se faltar: "Qual foi a versão que você aprovou?"
2. **O que mudou:** rode `scripts/mapear_pecas.py` com as duas e `--correcao`:
   ```
   python3 "<pasta desta habilidade>/scripts/mapear_pecas.py" "<minuta gerada>" "<minuta revisada>" --correcao
   ```
   O que aparece em "só de uma peça" e em "fixos com variáveis" é o que o advogado mudou.
3. **Classificar cada mudança**, uma pergunta por vez: "Isto vale para todo caso ou só para este?"

| Tipo de mudança | Onde entra |
|---|---|
| Só deste caso (um fato, um valor) | Fica na minuta; a habilidade não muda |
| Trecho padrão reescrito | Seções 5 e 8 do mapa |
| Variável nova ou regra de variável | Seção 3 do mapa (e coluna nova na planilha do lote) |
| Exceção nova ou "quando parar" | Seção 7 do mapa; bloco condicional na seção 8, se uma variável decide |
| Escolha de estilo | Seção 6 do mapa |
| Argumento ou tese | O banco de teses (`banco-de-teses-vivo`, se instalada); o mapa só aponta |
| Citação trocada ou nova | Seções 8 e 9 do mapa, com a marca `[CONFERIR]`, e a conferência na `conferir-citacoes` |

4. **Versão nova.** Mostre o mapa com cada mudança marcada `[ALTERADO]` ou `[NOVO]`. Com o ok: `versao` + 1 no mapa, uma linha no histórico do mapa com "o que mudou" e "por quê", e "Versão da habilidade: N" no SKILL.md.
5. **Testes de novo.** Rode os três casos com a versão nova e atualize o título do registro ("versão N da habilidade"). Se a correção nasceu de um caso que a habilidade errou, acrescente esse caso como Caso 4. O script recusa testes de versão antiga.
6. **Pacote novo.** Rode o passo 8. Diga: "Remova a versão anterior instalada e envie a nova, para não ficarem as duas."
7. **Aprender:** pergunte se a correção também vale para outras peças; se sim, vai para `aprendizados-juridico.md`.

### Modo revisar
Mesmo caminho do corrigir, com o motivo no lugar da minuta revisada: tese do banco mudou de situação (`banco-de-teses-vivo`), peça boa nova para entrar na origem (rode o mapa bruto com a nova e as antigas), ou aprendizados que já são regra desta peça. Sugira revisar a cada seis meses ou quando a tese mudar.

### Modo adaptar
A `adaptar-juridico` chama com a peça mais feita. Rode o modo criar inteiro e devolva a ela: o caminho da habilidade, o resultado dos três testes e o .zip, ou o motivo de não ter saído (faltam peças boas, teste falhou).

### Modo treino
Siga `references/exemplo/` na ordem: as três peças fictícias (`references/exemplo/peca-1.md`, `peca-2.md`, `peca-3.md`), o mapa bruto que o script devolve (`references/exemplo/mapa-bruto.md`), o mapa fechado com as respostas da advogada (`references/exemplo/mapa-da-peca.md`), a habilidade gerada (`references/exemplo/habilidade-skill.md`, que no escritório se chama SKILL.md) e os três testes (`references/exemplo/testes.md`), em que o caso com exceção é a Marta, caso 1 de `../../docs/casos-ficticios.md`. Grave em `escritorio/07-operacao/_treino/juridico/`. O que não pode falhar: a data de cessação da Marta não é escolhida; o julgado das peças de origem entra marcado; o caso do Paulo (trabalhista) para.

### No ciclo
Esta habilidade não roda sozinha: criar e corrigir pedem o advogado. O ciclo faz duas coisas que levam a ela: o `/motor-juridico:status` mostra "a peça mais feita que ainda não virou habilidade", e o comando `fila`, quando o advogado ajusta uma minuta feita por habilidade própria, oferece o modo corrigir.

## 4. O que entra no mapa

| Parte do mapa | O que é | De onde sai | A pergunta que resolve |
|---|---|---|---|
| Estrutura | As partes da peça, na ordem, fixas ou condicionais | Os títulos do mapa bruto | "Alguma parte só entra às vezes?" |
| Variáveis | O que muda de um cliente para outro, com tipo e origem (cliente, dossiê, advogado, ficha) | Os fixos com variáveis | "De onde vem esse dado?" |
| Teses | As teses do banco que a peça usa e quando cada uma entra | O advogado e `04-base/juridico/teses/` | "Qual tese esta peça defende?" |
| Trechos padrão | O texto que se repete igual | Os trechos fixos | "É do escritório ou coincidência?" |
| Estilo | Como o escritório escreve esta peça | A ficha, os aprendizados e o advogado | "O que você nunca escreve aqui?" |
| Exceções e quando parar | O que muda o texto e o que muda o caminho | Os trechos de algumas peças e de uma só | "Quando isso entra, e quem decide?" |
| Modelo | A peça com `{{variavel}}`, blocos `{{#se}}` e citações marcadas | Tudo acima | (montado pela habilidade, aprovado pelo advogado) |
| Citações | Toda citação do modelo, com a marca | O mapa bruto | (conferência na `conferir-citacoes`) |

Dado de identificação (nome completo, CPF, endereço, número de benefício ou processo) nunca é variável: no modelo, ele é campo entre chaves de quem protocola (`{QUALIFICAÇÃO COMPLETA}`), preenchido pelo sistema do escritório.

## 5. Formato da saída

```
HABILIDADE PRÓPRIA · [peca] · versão [N] · [criada | corrigida | revisada]
Origem: [N] peças boas ([P1 a PN])
Mapa: [N] variáveis ([N] do caso, [N] da ficha) · [N] blocos condicionais · [N] exceções que param · [N] citações marcadas
Teses: [nomes] ([com arquivo | sugestão: criar])
Testes: comum [passou] · com exceção [passou] · deve parar [passou] · conferido por [função] em [data]
Pacote: [caminho do .zip] | não gerado: [o que corrigir]
Próximo passo: instalar; [pecas-em-lote, se a peça sai em massa]
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Peças boas (anonimizadas) | `escritorio/04-base/juridico/modelos/<peca>/` |
| Mapa bruto (rascunho) | `escritorio/07-operacao/juridico/mapas/<peca>-mapa-bruto.md` |
| A habilidade própria | `escritorio/04-base/habilidades-do-escritorio/<peca>/SKILL.md` e `references/mapa-da-peca.md` |
| Registro dos três testes | `escritorio/04-base/casos-de-teste/juridico/<peca>-testes.md` |
| Pacote | `escritorio/04-base/habilidades-do-escritorio/<peca>-v<versao>.zip` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções que valem para toda peça | `escritorio/04-base/comum/aprendizados-juridico.md` |
| Caminho das peças boas (com o ok) | `escritorio/04-base/comum/ficha-juridica.md`, campo `onde_estao_os_modelos`, com linha no histórico |

No `pecas.csv`, esta habilidade não muda nenhuma linha; a partir da instalação, as peças novas registram `habilidade_usada = <peca>`. Sem pasta aberta: o mapa, o SKILL.md e o registro dos testes saem no chat, em blocos, com o caminho de cada um; o .zip só existe com pasta aberta e o script.

## 7. Solo e equipe

**Solo:** a primeira habilidade leva uma tarde: uma hora para separar e anonimizar as peças, meia hora de perguntas, os testes. Comece pela peça que mais toma tempo. **Equipe:** o estagiário separa e anonimiza as peças e roda os testes; o advogado responde as perguntas do passo 4 e confere os testes. Uma pessoa é dona das habilidades do escritório: só ela gera versão nova e o .zip, e ninguém edita a cópia instalada.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Habilidade feita de uma peça só | O caso particular daquela peça vira regra | De 3 a 5 peças e o mapa bruto que separa fixo de coincidência |
| Peça com nome ou CPF de cliente no modelo | Dado de um cliente na peça de outro | Anonimização antes, alerta do script, qualificação como campo de quem protocola |
| Julgado das peças antigas tratado como conferido | Citação superada ou inventada repetida em toda peça | Tudo `[CONFERIR]` no mapa; o script recusa citação sem marca |
| Exceção que muda a tese virando "trecho opcional" | A habilidade decide o caminho do caso | Exceção que muda o caminho para e leva ao advogado |
| Habilidade empacotada sem teste | A primeira falha aparece num caso real | Três casos, "Conferido por", script que recusa o modelo cru |
| Correção feita na cópia instalada | Duas versões diferentes, ninguém sabe qual vale | Versão nova no mapa, testes de novo, pacote novo |
| Testes de uma versão antiga | A versão nova nunca foi testada | O script compara a versão dos testes com a do mapa |

## 9. Próximo passo

- Habilidade instalada: as próximas peças desse tipo saem por ela; muitos casos iguais, `pecas-em-lote` (se instalada).
- Tese sem arquivo: `banco-de-teses-vivo` (se instalada); sem ela, escreva a tese em `04-base/juridico/teses/<tese>.md` com o advogado.
- Citações do modelo: `conferir-citacoes` (se instalada) no modelo, para a base já ter as conferências.
- Próxima peça: a seguinte da `pecas_mais_feitas`.
- Rotina que não é peça: `adaptar-juridico`.

## Referências desta habilidade

- `references/mapa-da-peca.md`: o formato do mapa, as colunas das variáveis e a escrita do modelo. Leia no passo 5 e no modo corrigir.
- `references/molde-da-habilidade.md`: o molde do SKILL.md da habilidade própria. Leia no passo 6.
- `references/exemplo/peca-1.md`, `references/exemplo/peca-2.md`, `references/exemplo/peca-3.md`: três peças fictícias de restabelecimento. Leia no modo treino.
- `references/exemplo/mapa-bruto.md`: o que o script devolve para as três. Leia no modo treino e antes do primeiro passo 4.
- `references/exemplo/mapa-da-peca.md`: o mapa fechado. Leia no passo 5, como referência de nível.
- `references/exemplo/habilidade-skill.md`: a habilidade gerada. Leia no passo 6.
- `references/exemplo/testes.md`: os três testes preenchidos, com a Marta como caso com exceção. Leia no passo 7.
- `scripts/mapear_pecas.py`: o mapa bruto e a comparação da correção. Rode no passo 3 e no modo corrigir.
- `scripts/empacotar_habilidade.py`: confere e empacota. Rode no passo 8.
