---
name: advogado-do-diabo
description: >
  Escreve a melhor resposta da parte contrária contra a nossa tese ou a nossa minuta, na
  versão mais forte e sem caricatura: preliminares, mérito, provas, com os fatos do dossiê e
  a jurisprudência contrária da base do escritório (um script lista os julgados marcados
  "contra" e se a conferência ainda vale). Toda citação sai marcada. Devolve onde a peça
  está exposta, o que reforçar (fato, prova, citação, distinção, pedido subsidiário) e o
  que pesquisar no Jus IA; grava contraditorio.md. Use quando o advogado disser "o que a
  outra parte vai dizer", "faz o advogado do diabo", "ataca a minha tese", "onde essa
  peça é fraca", "simula a contestação", "o que eles vão responder no recurso".
  Não use para escolher a tese (use estrategia-do-caso) nem para conferir as citações da
  peça (use conferir-citacoes).
---

# Advogado do diabo

> Antes de a peça sair, alguém do escritório escreve a melhor resposta do outro lado, com a jurisprudência contrária que o escritório já tem, e a peça é reforçada onde essa resposta acerta.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Base de jurisprudência e Jus IA: `../../docs/pesquisa-jus-ia.md`. Produção e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 11h. A inicial está pronta e bonita. Na contestação, o réu usa o único ponto que ninguém olhou: o relatório médico é anterior à perícia, e não há nada depois da cessação. O julgado que sustenta o argumento estava na base do escritório, marcado "contra", desde a pesquisa de abril.

**Regras fixas desta habilidade:**
1. A resposta da outra parte é escrita na versão mais forte. Argumento fraco é dito fraco, com o porquê, e nunca é inventado só para ser derrubado.
2. Jurisprudência contrária vem da base do escritório (`04-base/juridico/jurisprudencia/`, julgados marcados "contra"). Julgado que não está na base não é citado: vira pergunta de pesquisa no Jus IA.
3. Toda citação sai marcada `[CONFERIR]`, salvo a conferida dentro da validade (`citacoes.md`, regra 5). A IA nunca completa número, relator, data ou enunciado de memória.
4. Força é `forte`, `média` ou `fraca`, com o porquê. Nunca percentual, nunca previsão de resultado.
5. O `contraditorio.md` é documento interno. Não vai para o processo nem para o cliente, e não muda a tese: mudar a tese é do advogado, pela `estrategia-do-caso`.

## 1. Quando usar

**Use quando:**
- A tese foi escolhida e a peça vai ser minutada: testar a tese antes (modo "tese").
- A minuta está pronta e vai para a revisão do advogado (modo "minuta").
- O outro lado já falou (contestação, recurso, contrarrazões) e o advogado quer saber o que ainda vem e onde a nossa resposta deve bater (modo "peça deles").
- Vai haver audiência, sustentação ou reunião de acordo e o advogado quer as objeções prováveis.
- Treino com os casos fictícios, ou a `adaptar-juridico` (se instalada) pediu os argumentos típicos do outro lado no nicho (modo "adaptar").

**Não use quando:**
- O caminho do caso ainda não foi escolhido: `estrategia-do-caso` (esta habilidade pode rodar depois, sobre cada caminho, se o advogado pedir).
- O pedido é conferir se as citações da peça existem: `conferir-citacoes` (se instalada).
- O pedido é pesquisar jurisprudência: a pesquisa é no Jus IA, e a `trazer-pesquisa` (se instalada) guarda o resultado na base.

## 2. Antes de começar

1. **Leia as fichas** (`ficha-do-escritorio.md` e `ficha-juridica.md`, em `escritorio/04-base/comum/`), `nicho.md` (se existir) e `04-base/juridico/nicho/advogado-do-diabo.md` (argumentos típicos do outro lado, do modo adaptar).
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`).
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Para seguir, pergunte só: "Quem é a outra parte e em que juízo ou tribunal o caso vai ser julgado?".
4. **Leia o caso** em `escritorio/07-operacao/juridico/casos/<codigo>/`: `estrategia.md` (a tese da seção 10), `dossie.md` (contradições e lacunas), `leitura-dos-autos.md` (o que a outra parte já disse), `minutas/` (a versão mais nova) e `contraditorio.md` (se existe, o modo é "rever").
5. **Leia a base:** a tese em `04-base/juridico/teses/` (se existir) e os temas dela em `04-base/juridico/jurisprudencia/`. Rode o script da seção 4.3 para listar os julgados contra.
6. **Dados.** O contraditório trabalha com os fatos do caso: mesmo cuidado do dossiê com dado sensível (fica fora do texto se não for o fato do caso).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | E: `areas` |
| Melhora | J: `tribunais_principais` |

`tribunais_principais` decide onde o argumento contrário pesa mais (o juízo do caso) e onde pesquisar no Jus IA. A validade da conferência segue `citacoes.md` (90 dias, ou o que a ficha jurídica definir em `validade_da_conferencia`); passe o número para o script com `--validade`.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Tese | Antes de minutar | `estrategia.md` e `dossie.md` | `contraditorio.md`, com o que a minuta deve antecipar |
| Minuta | Antes da revisão do advogado | A minuta mais nova | `contraditorio.md`, com o que reforçar trecho por trecho |
| Peça deles | O outro lado já falou | A peça deles (na leitura dos autos) | O que eles ainda vão dizer e onde a nossa resposta deve bater |
| Rever | Fato ou pesquisa nova | O contraditório anterior | Nova versão, com `[NOVO]` e `[ALTERADO]` |
| No ciclo | O agente chama sobre uma minuta | A minuta e o caso | Contraditório gravado e resumo no item da fila. Não mostra nada |
| Treino | Casos fictícios | Caso 1 | O mesmo, em `_treino/`, e a diferença com a seção 4.5 |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a ficha | Argumentos típicos da outra parte no nicho, para aprovar |

### Passo 1. A nossa posição em três linhas
Tese (da seção 10 da estratégia ou da minuta), fatos centrais com a fonte, pedidos. Sem tese definida e sem minuta: pergunte "Contra qual tese eu escrevo?" e siga com o que o advogado disser.

### Passo 2. Os julgados contra
Rode o script (seção 4.3) com a tese. Leia a tabela: o que pode entrar sem marca (verde na validade), o que entra com `[CONFERIR]`, o que não entra (vermelho), o que está superado. Nenhum julgado contra na base: escreva isso e siga só com os fatos; a pergunta de pesquisa vai para a seção 5.

### Passo 3. Escrever a resposta deles
Na voz da outra parte, do mais forte para o mais fraco: preliminares e questões processuais `[CONFERIR]`, mérito, provas, pedido subsidiário. Cada argumento com a base nos fatos (o documento ou a folha que eles vão usar: uma contradição do dossiê, uma lacuna, uma folha dos autos) e a base jurídica (julgado da base com a situação da conferência, ou "sem base na nossa base"). As fontes de cada argumento estão na seção 4.1.

### Passo 4. Medir a força
Para cada argumento: `forte`, `média` ou `fraca`, com o porquê (seção 4.2). Na dúvida, o mais forte.

### Passo 5. Onde a peça está exposta
Do lado de cá: os pontos que os argumentos fortes e médios exploram (fato sem prova, contradição sem explicação, citação fraca ou vencida, pedido sem fundamento, dado que diverge entre trechos da minuta).

### Passo 6. O que reforçar
Para cada ponto exposto: o que fazer, o tipo (fato, prova, citação, distinção, pedido, corte), onde na peça e qual argumento responde. Citação sugerida só da base; o que falta vira pesquisa no Jus IA. Distinção de um julgado contrário: escreva por que os fatos do caso são diferentes, com a fonte, e marque o julgado.

### Passo 7. O que pesquisar
Cada argumento sem base na nossa base, e cada reforço que depende de jurisprudência, vira uma pergunta de pesquisa para o Jus IA (tema, pergunta, para que, tribunal). Depois da pesquisa, a `trazer-pesquisa` (se instalada) guarda na base; sem ela, o advogado traz e a base é atualizada à mão pelo formato de `../../docs/pesquisa-jus-ia.md`.

### Passo 8. Mostrar e gravar
Monte o `contraditorio.md` pelo `assets/modelo-contraditorio.md`. Mostre o resumo (seção 5) e grave com o ok. Não mexa na minuta: o que reforçar é sugestão para quem redige e para o advogado.

### Passo 9. Aprender
Pergunte: "Algum argumento que o outro lado sempre usa contra vocês e eu não trouxe?". A resposta vira regra curta e, com o ok, entra em `aprendizados-juridico.md`, ou argumento típico em `04-base/juridico/nicho/advogado-do-diabo.md`. Julgado que o advogado lembrou e não está na base: não guarde o número de memória; vira pesquisa no Jus IA.

### Modo minuta
Leia a minuta trecho por trecho. Cada argumento deles aponta o trecho que ataca (item dos fatos, tópico do direito, pedido). O reforço diz onde mexer na minuta. Citação nova sugerida volta para a `conferir-citacoes` (se instalada) antes da peça seguir.

### Modo peça deles
Leia a peça da outra parte (na `leitura-dos-autos`, ou o arquivo). Separe: o que eles já disseram (com a folha), o que ainda podem dizer (próxima manifestação, recurso) e onde a nossa resposta deve bater. Julgado que eles citaram: registre como citado por eles e marque `[CONFERIR]`; se não está na base, vira pesquisa no Jus IA para conferir se existe e diz o que eles dizem.

### Modo no ciclo
1. Só quando o escritório incluir esta habilidade no ciclo, sobre minutas novas. Não pergunte nada e não mostre nada.
2. Rode os passos 1 a 7 no modo minuta.
3. Grave `contraditorio.md`. No item da fila da minuta, acrescente em `antes_de_enviar`: "contraditório: N argumentos fortes; reforçar: ..." e a lista do que pesquisar no Jus IA. Não crie item novo nem mude etapa.

### Modo treino
Caso 1 de `../../docs/casos-ficticios.md`, com o dossiê de treino (os achados da `dossie-do-caso`, se instalada) e a pesquisa de exemplo da `trazer-pesquisa` (se instalada) gravada como tema no lugar onde ela grava o treino; rode o script nessa pasta. Sem a pesquisa de exemplo, rode só com os fatos e diga que a base de treino está vazia. Grave em `escritorio/07-operacao/_treino/juridico/casos/C-2026-0001/contraditorio.md`. Mostre a diferença com a seção 4.5.

### Modo adaptar
1. Leia `nicho.md` e a ficha.
2. Para cada tipo de caso do nicho: quem costuma ser a outra parte, os argumentos que ela usa sempre e as provas que ela costuma trazer, `[CONFERIR]` com o advogado. Sem julgado: só os argumentos.
3. Marque `[NOVO]` ou `[ALTERADO]`, mostre e pergunte: "É isso que a outra parte costuma dizer contra vocês?".
4. Com o ok, grave em `04-base/juridico/nicho/advogado-do-diabo.md`.

## 4. Critérios

### 4.1 De onde vêm os argumentos
| Fonte | O que dá | Exemplo (fictício) |
|---|---|---|
| Contradição do dossiê | Ataque à credibilidade dos fatos | Duas datas de cessação |
| Lacuna do dossiê | Fato sem prova | Nenhum relatório médico depois da cessação |
| Folha dos autos | O que eles já disseram e vão repetir | A contestação defende a perícia administrativa |
| Julgado contra da base | A base jurídica do argumento | O julgado de exemplo que dá peso à perícia oficial |
| Ponto exposto da minuta | Ataque ao texto | Pedido de dano moral sem fato |
| Nicho | O argumento de sempre daquela parte | O que o advogado contou no modo adaptar |

### 4.2 Força
| Força | Quando |
|---|---|
| forte | Se apoia em fato provado ou em lacuna nossa real, e tem base na nossa base ou nos autos |
| média | Tem base, mas os fatos do caso permitem distinção, ou a nossa base tem julgado nos dois sentidos |
| fraca | Contraria documento direto do caso, ou depende de julgado vermelho, superado ou que não está na base |

### 4.3 O script dos julgados contra
Rode com o caminho da pasta desta habilidade. No plugin instalado, ela é `${CLAUDE_PLUGIN_ROOT}/skills/advogado-do-diabo`; sem a variável, use o caminho da pasta desta habilidade.

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/advogado-do-diabo/scripts/julgados_contra.py" \
  "escritorio/04-base/juridico/jurisprudencia" \
  --tese restabelecimento-incapacidade --validade 90
```

O `scripts/julgados_contra.py` lê os temas no formato de `../../docs/pesquisa-jus-ia.md` e lista os julgados marcados "contra" (a linha "Para que serve no escritório" começa por "contra" ou diz "contra a tese", ou o julgado tem "Posição: contra"), com a conferência (verde na validade, verde vencido, amarelo, vermelho, não conferido), a situação (vigente, superado) e como cada um entra no contraditório: sem marca ou com `[CONFERIR]`. `--tese` filtra pelos temas da tese (`teses_do_escritorio`), `--data AAAA-MM-DD` muda o dia de referência e `--todos` mostra também os a favor. Julgado sem posição aparece nos avisos, para o advogado marcar. Caminho que não existe ou base sem julgado no formato: código 1 e a mensagem.

### 4.4 Citação no contraditório
| A conferência diz | Como entra |
|---|---|
| verde, dentro da validade | Sem marca, com a data da conferência no "Antes de usar" |
| verde vencido, amarelo, não conferido | Com `[CONFERIR: ...]`, como em `citacoes.md` |
| vermelho | Não entra. Se a outra parte citou, registre como citado por ela, marcado |
| superado | Entra com a situação escrita e `[CONFERIR]`; força no máximo média |
| fora da base | Não entra. Vira pergunta de pesquisa no Jus IA |

### 4.5 Conferência com o caso de treino
Rodando no caso 1 (Marta), modo tese, o contraditório tem que trazer:

| # | Argumento deles | Base | Força esperada |
|---|---|---|---|
| 1 | Não há prova de incapacidade atual: o relatório do médico assistente é de 2026-01-20, anterior à perícia de 2026-02-20, e nada depois da cessação | Lacuna do dossiê | forte |
| 2 | A perícia administrativa concluiu pela capacidade e prevalece | Dossiê (D5) e o julgado contra da pesquisa de exemplo, se estiver na base, com `[CONFERIR]` (não conferido) | média (a perícia não enfrentou o relatório D4) |
| 3 | A própria autora erra a data de cessação (D1 e D3 contra D2) | Contradição do dossiê | média, enquanto a data não for conferida |

E no "o que reforçar": pedir relatório médico atual; quesito na perícia judicial sobre o relatório do assistente; data de cessação conferida e explicada na peça; a pesquisa no Jus IA sobre perícia que não analisa relatório do assistente. Não pode: citar julgado da pesquisa de exemplo sem marca; trazer julgado que não está na base; dar percentual; mexer na minuta ou na tese.

## 5. Formato da saída

**No chat, primeiro:**

```
CONTRADITÓRIO · [CODIGO] · [peça ou tese] · modo [tese | minuta | peça deles]
Base: [N] julgados contra na base ([N] na validade, [N] com [CONFERIR], [N] fora)
Argumentos deles: [N] (forte [N], média [N], fraca [N])
O mais forte: [uma frase, com a base]
Onde a peça está exposta: [até 3, uma frase cada]
Reforçar primeiro: [até 3]
Pesquisar no Jus IA: [N] perguntas
```

Depois, o `contraditorio.md` no formato de `assets/modelo-contraditorio.md`.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Contraditório | `escritorio/07-operacao/juridico/casos/<codigo>/contraditorio.md` |
| Resumo no item da fila (ciclo) | o item da minuta em `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/`, campo `antes_de_enviar` |
| Treino | `escritorio/07-operacao/_treino/juridico/casos/<codigo>/contraditorio.md` |
| Argumentos do nicho | `escritorio/04-base/juridico/nicho/advogado-do-diabo.md` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

Não muda o `pecas.csv` nem a minuta. Sem pasta aberta: o contraditório no chat, em bloco pronto para copiar, com o caminho onde ficaria.

## 7. Solo e equipe

**Solo:** rode no modo tese antes de começar a escrever e no modo minuta antes de dar a peça por pronta. A lista "reforçar primeiro" é a sua revisão.

**Equipe:** quem não escreveu a peça roda o contraditório (a leitura fica menos presa ao texto). O advogado lê os argumentos fortes e decide o que muda; o estagiário aplica os reforços e manda as citações novas para a conferência.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Argumento contrário de palha | A peça parece forte até a contestação | A versão mais forte, com a força medida |
| Julgado contrário inventado | O advogado se prepara contra o que não existe | Só a base; o resto vira pesquisa no Jus IA |
| Julgado contra esquecido na base | O réu acha o que o escritório já tinha | O script lista todos os "contra" da tese |
| Conferência vencida usada como certa | Citação que mudou entra sem nova conferência | Validade no script e a marca |
| Contraditório que muda a tese sozinho | Linha vermelha cruzada | Só sugere; a tese muda pela estratégia, com o advogado |

## 9. Próximo passo

- Aplicar os reforços: quem redige, na `minutar-peca` ou na habilidade própria da peça (se instaladas); citações novas para a `conferir-citacoes` (se instalada).
- Pesquisar o que faltou: Jus IA, e a `trazer-pesquisa` (se instalada) para guardar na base.
- Se um argumento forte põe o caminho em dúvida: `estrategia-do-caso`, modo rever, com o advogado.
- Audiência ou sustentação: os argumentos fortes viram perguntas prováveis na `sustentacao-oral` (se instalada).

## Referências desta habilidade

- `assets/modelo-contraditorio.md`: o formato do `contraditorio.md`. Use no passo 8.
- `scripts/julgados_contra.py`: os julgados contra da base, com a conferência (seção 4.3). Rode no passo 2.
