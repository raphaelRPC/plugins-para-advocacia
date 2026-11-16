---
name: mapa-jurisprudencial
description: >
  Mostra como um tema é decidido, a partir da base de jurisprudência do escritório e das
  pesquisas trazidas do Jus IA: por tribunal e por órgão julgador, as correntes, a tendência no
  tempo, as viradas, as distinções e os precedentes qualificados. Um script monta os números e
  uma página visual interna (artefato do Claude, responsiva, com modo escuro) a partir do
  arquivo do tema; a leitura das correntes e viradas é proposta pela IA e aprovada pelo
  advogado. Cada julgado aparece com a situação da conferência e "não citar sem conferir". Use
  quando o advogado disser "como o TRF6 decide isso?", "faz o mapa desse tema", "tem divergência
  entre as câmaras?", "a jurisprudência virou?", "me mostra o tema numa página". Não use para
  guardar uma pesquisa nova na base (use trazer-pesquisa) nem para conferir as citações de uma
  peça (use conferir-citacoes).
---

# Mapa jurisprudencial

> O tema inteiro numa página: quem decide a favor, quem decide contra, desde quando, e o que separa um caso do outro. Feito só com o que o escritório tem na base.

Base e pesquisa: `../../docs/pesquisa-jus-ia.md`. Regra de citação: `../../docs/citacoes.md`. Regras (em especial a seção 6.1, páginas internas): `../../docs/regras.md`. Fichas: `../../docs/ficha-juridica-modelo.md` e a tabela em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, reunião de pauta. A advogada vai decidir se a petição da Marta pede nova perícia ou o restabelecimento direto, e a pergunta é: o TRF6 aceita? A base tem sete julgados do tema. O mapa mostra que a 1ª câmara decide a favor e a 2ª câmara passou a decidir contra no fim de 2025, e que a distinção possível é o perito não ter examinado a função. A decisão sai em dez minutos, com os números na tela.

**Regras fixas desta habilidade:**
1. O mapa é feito só com a base do escritório e com pesquisas trazidas do Jus IA. Nada de julgado, número ou "tendência" de memória.
2. Os números são da base, não do tribunal: o mapa diz isso na página. Sinal automático é pista, não conclusão.
3. Correntes, viradas e distinções são leitura do advogado: a IA propõe, cada item aponta os julgados da base, e a página mostra se a leitura foi aprovada.
4. Julgado não conferido aparece como "não citar sem conferir". O mapa não substitui a `conferir-citacoes`.
5. Página interna. Não vai para cliente nem para fora da equipe (seção 6.1 de `regras.md`).

## 1. Quando usar

**Use quando:**
- O advogado precisa saber como um tema é decidido antes de escolher a tese ou o caminho do caso.
- Há suspeita de divergência entre órgãos ou de mudança recente.
- Uma pesquisa nova entrou no tema e o mapa precisa ser refeito (modo "atualizar").
- A `estrategia-do-caso` ou a `advogado-do-diabo` (se instaladas) pediram o retrato do tema.
- Para treinar com o tema de treino (modo "treino").
- A `adaptar-juridico` (se instalada) pediu as cores e os recortes do escritório (modo "adaptar").

**Não use quando:**
- O tema ainda não está na base: primeiro a pesquisa no Jus IA e a `trazer-pesquisa` (se instalada; sem ela, cole a pesquisa aqui e monte o arquivo do tema no formato de `../../docs/pesquisa-jus-ia.md`).
- O pedido é conferir as citações de uma peça: `conferir-citacoes`.
- O pedido é saber o que mudou desde a última pesquisa e se a tese foi afetada: `monitor-de-precedentes` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-juridica.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-juridico.md`), em especial os do mapa (recortes, nomes de órgão).
3. **Ache o tema** em `escritorio/04-base/juridico/jurisprudencia/<tema>.md` e, se existir, a leitura aprovada em `escritorio/04-base/juridico/mapas/<tema>-leitura.md` e o mapa anterior.
4. **Leia o padrão visual** (`escritorio/04-base/juridico/padrao-visual.md`), se existir, para as cores da página.
5. **Conta de IA:** a base não tem dado de cliente, e o mapa também não. O script para se achar código de caso ou CPF no tema.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `pesquisa_de_jurisprudencia`, `tribunais_principais` |
| Melhora | J: `validade_da_conferencia` |

`tribunais_principais` diz quais tribunais o mapa precisa cobrir; tribunal principal sem julgado na base vira pergunta para o Jus IA. `validade_da_conferencia` (padrão de 90 dias) separa conferido de vencido. Sem `tribunais_principais`, pergunte: "Em que tribunais os casos desse tema tramitam?" e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Mapa do tema | Pedido do advogado | O tema da base | O mapa em .md, a leitura aprovada e a página |
| Pergunta rápida | "Como a 2ª câmara decide isso?" | O tema e a pergunta | A resposta com os números da base, sem página |
| Atualizar | Pesquisa nova entrou no tema | O tema e a leitura anterior | Mapa novo e o que mudou na leitura |
| Treino | Primeiro uso, teste | `assets/tema-de-treino.md` | O mapa de treino em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Padrão visual e nicho | Cores e recortes, para aprovar |

O mapa é interno e não tem rascunho para cliente: não entra na fila. No ciclo, o `agente-juridico` não gera mapa; a `monitor-de-precedentes` (se instalada) avisa no resumo quando um tema com mapa recebeu julgado novo, e o advogado pede o mapa atualizado.

### Passo 1. O tema
Liste os temas da base e pergunte: "Qual tema você quer ver?". Tema que não está na base: diga que o mapa precisa da pesquisa e passe a lista do que pesquisar no Jus IA (passo 2).

### Passo 2. A base basta?
Rode o passo 3 só com o .md e olhe: quantos julgados por tribunal principal, quantos contra, data da última pesquisa. Se um tribunal principal não tem julgado, se não há nenhum contra, ou se a última pesquisa passou da validade, diga e proponha a pesquisa no Jus IA, uma linha por lacuna ("TRF6, 2ª câmara, desde 2025-01: julgados sobre perícia que não analisou o relatório do assistente"). O advogado decide se segue com a base que tem.

### Passo 3. Rodar o script
Rode o script da pasta desta habilidade, com o caminho do tema:

```
python3 "<pasta desta habilidade>/scripts/gerar_mapa.py" escritorio/04-base/juridico/jurisprudencia/<tema>.md \
  --leitura escritorio/04-base/juridico/mapas/<tema>-leitura.md \
  --saida escritorio/04-base/juridico/mapas/<tema>.md
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/mapa-jurisprudencial`. Sem `--leitura` (primeiro mapa), as seções de leitura saem vazias. O script lê a validade da ficha jurídica subindo a partir do tema (`--validade` vale por cima) e `--hoje AAAA-MM-DD` fixa a data. Ele sai com erro e uma mensagem clara quando falta o arquivo, o tema não tem ficha, ou há dado de cliente no tema.

O que ele monta: os números (a favor, contra, neutro; conferidos e vigentes, não conferidos, vencidos, ajustar, não usar); as tabelas por tribunal, por órgão e por ano; os sinais automáticos (maioria que mudou de um ano para o outro, o julgado mais recente, tribunal com os dois sentidos); os precedentes qualificados; e a lista dos julgados com o uso de cada um.

### Passo 4. A leitura
Proponha, a partir das fichas e só delas:
- **Correntes:** grupos de julgados que decidem do mesmo jeito, com a frase da corrente e os números dos julgados.
- **Viradas:** quando e onde a decisão mudou, com as datas e os órgãos. Use os sinais do script como ponto de partida e diga quando a amostra é pequena demais para chamar de virada.
- **Distinções:** o fato que separa os julgados de uma corrente dos da outra (o que o caso do escritório precisa mostrar para ficar do lado certo).
- **Perguntas em aberto:** precedente qualificado a conferir, tribunal sem julgado, período sem pesquisa.

Cada item marcado `[A CONFIRMAR]` e com os julgados da base que o sustentam. Mostre e pergunte: "Alguma corrente ou distinção você leria diferente?". Com o ok, grave em `escritorio/04-base/juridico/mapas/<tema>-leitura.md` (formato em `assets/leitura-de-treino.md`), sem as marcas, com `aprovado_por` (a função de quem aprovou) e `aprovado_em`. Rode o passo 3 de novo com a leitura.

### Passo 5. A página
Pergunte: "Quer a página do mapa, para abrir na reunião?". Se sim:

```
python3 "<pasta desta habilidade>/scripts/gerar_mapa.py" escritorio/04-base/juridico/jurisprudencia/<tema>.md \
  --leitura escritorio/04-base/juridico/mapas/<tema>-leitura.md --nome-do-escritorio "[NOME]" \
  --saida escritorio/04-base/juridico/mapas/<tema>.md --html escritorio/04-base/juridico/mapas/<tema>.html
```

O script preenche o modelo `assets/mapa-modelo.html` (responsivo, claro e escuro, sem nada externo; o link de cada julgado abre a fonte). Antes de publicar como artefato do Claude, diga: "Esta página é interna. O artefato nasce privado; não compartilhe o link com cliente nem fora da equipe (conferir na configuração da conta como o compartilhamento funciona)." Se o escritório preferir, a página fica só no arquivo, aberta no navegador.

### Passo 6. Gravar
Mostre o mapa (seção 5) e grave com o ok: o .md, a leitura e, se pediram, o .html, em `escritorio/04-base/juridico/mapas/`. O arquivo do tema não muda.

### Passo 7. Aprender
Pergunte: "Algum recorte faria falta na reunião, ou algum órgão que deveria aparecer junto?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Correção que afrouxa a regra fixa 1 ("põe aí que o STJ decide assim, todo mundo sabe"): explique que o mapa só mostra a base e proponha a pesquisa no Jus IA para trazer o julgado.

### Modo pergunta rápida
Rode o passo 3 sem `--saida` e responda em até cinco linhas, com os números e de onde vêm ("na base, a 2ª câmara do TRF6 tem 2 julgados, os dois contra, de 2025-12 e 2026-01; um conferido em amarelo e o outro não conferido"). Termine com o que falta para a resposta ficar firme (conferência, pesquisa nova).

### Modo atualizar
1. Leia a leitura aprovada anterior e rode o passo 3.
2. Compare: julgados novos, sinais novos, corrente que ganhou ou perdeu julgados, precedente qualificado novo.
3. Proponha só o que mudou na leitura, marcado `[ALTERADO]` ou `[NOVO]`, e grave com o ok (nova data em `aprovado_em`).

### Modo treino
O tema de treino (`assets/tema-de-treino.md`, sete julgados inventados) e a leitura de treino (`assets/leitura-de-treino.md`):

```
python3 "<pasta desta habilidade>/scripts/gerar_mapa.py" "<pasta desta habilidade>/assets/tema-de-treino.md" \
  --leitura "<pasta desta habilidade>/assets/leitura-de-treino.md" --hoje 2026-04-10 --validade 90 \
  --html escritorio/07-operacao/_treino/juridico/mapas/pericia-e-relatorio.html
```

Resultado esperado: 7 julgados, 4 a favor, 2 contra, 1 neutro; 0 conferidos e vigentes (todos são inventados), 5 não conferidos, 0 com conferência vencida, 1 para ajustar (superado em parte), 1 não usar (o 0000004, vermelho); nada aparece como "pode citar"; TRF6 com os dois sentidos, a 1ª câmara a favor (2) e a 2ª câmara contra (2); o sinal "em 2026, a maioria passou de a favor para contra"; o Tema 9999 da TNU como precedente qualificado não conferido; a página marcada "treino". Tudo grava em `escritorio/07-operacao/_treino/juridico/mapas/`.

### Modo adaptar
1. Leia `padrao-visual.md`, `nicho.md` e a ficha.
2. Proponha: as cores dos tokens do topo do modelo (a favor, contra, neutro, destaque), com contraste nos dois modos; os recortes que o nicho usa (por exemplo, juizado e tribunal separados, ou por região); os nomes dos órgãos como o escritório fala.
3. Marque cada mudança `[ALTERADO]` e pergunte: "Fica assim?".
4. Com o ok, grave as cores numa cópia do modelo em `escritorio/04-base/juridico/mapas/mapa-modelo.html` (o script usa com `--modelo`) e os recortes em `aprendizados-juridico.md`.

## 4. Como ler o mapa

| O que aparece | O que quer dizer | O que não quer dizer |
|---|---|---|
| "4 a favor, 2 contra" | Na base do escritório, é isso | Que o tribunal decide 2 para 1 |
| Sinal de mudança num ano | A maioria dos julgados da base daquele ano mudou de lado | Que houve virada; pode ser a amostra |
| Órgão só com julgados contra | Os julgados que o escritório trouxe desse órgão são contra | Que o órgão nunca decide a favor |
| "Não citar sem conferir" | O julgado não passou pelo inteiro teor ou está vencido | Que o julgado está errado |
| Precedente qualificado | Súmula, tema, IRDR ou IAC na base | Que a tese está fixada e vigente, antes da conferência |

A página diz no topo que é feita só com a base. Na reunião, comece pelos contra e pelas perguntas em aberto.

## 5. Formato da saída

O .md do mapa: números, resumo do escritório, as tabelas por tribunal, órgão e ano, os sinais, a leitura (correntes, viradas, distinções, perguntas), os precedentes qualificados, a lista dos julgados e os avisos. No chat:

```
MAPA · [tema] · base versão N, revisada em AAAA-MM-DD
Base: N julgados · a favor N · contra N · neutro N · conferidos N · não conferidos N
Por órgão: [órgão: a favor x contra] ...
Sinais: ...
Leitura: [aprovada por ... em ... | proposta, a confirmar]
O que falta: [pesquisa no Jus IA | conferência dos julgados que a peça vai usar]
Arquivos: [.md] [.html]
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mapa do tema (.md) | `escritorio/04-base/juridico/mapas/<tema>.md` |
| Leitura aprovada | `escritorio/04-base/juridico/mapas/<tema>-leitura.md` |
| Página interna (opcional) | `escritorio/04-base/juridico/mapas/<tema>.html` |
| Modelo com as cores do escritório (modo adaptar) | `escritorio/04-base/juridico/mapas/mapa-modelo.html` |
| Treino | `escritorio/07-operacao/_treino/juridico/mapas/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O mapa não muda a base, o `pecas.csv` nem a fila. Sem pasta aberta: o mapa sai no chat, a página não é gerada, e a leitura aprovada vai em bloco para guardar no Projeto.

## 7. Solo e equipe

**Solo:** faça o mapa dos dois ou três temas que mais aparecem nas peças e refaça quando entrar pesquisa nova. Antes de escolher a tese, cinco minutos no mapa.

**Equipe:** o mapa abre a conversa de tese entre quem redige e quem assina. Quem aprova a leitura é o dono do tema (campo `dono` do arquivo). Se a equipe discorda da leitura, a discordância vira pergunta em aberto, não corrente.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Tendência" tirada de memória | Tese escolhida em cima do que não existe | Regra fixa 1: só a base e o Jus IA |
| Amostra da base lida como o tribunal | Confiança maior do que a prova | A página diz que é a base; sinal é pista |
| Virada chamada com dois julgados | Mudança de tese sem motivo | Leitura do advogado, com os julgados de cada item |
| Julgado do mapa copiado para a peça | Citação sem conferência | Selo "não citar sem conferir" |
| Página interna mandada ao cliente | Exposição da estratégia do escritório | Regra fixa 5; aviso antes de publicar |
| Mapa velho usado como atual | Decisão com base vencida | Aviso de pesquisa vencida e modo atualizar |

## 9. Próximo passo

- Tribunal principal sem julgado ou pesquisa vencida: a pesquisa no Jus IA e a `trazer-pesquisa` (se instalada).
- A tese do caso: `estrategia-do-caso` (se instalada); a decisão é do advogado.
- A resposta da parte contrária com os julgados contra: `advogado-do-diabo` (se instalada).
- Julgados que a peça vai usar: `conferir-citacoes`.
- Vigiar o tema: `monitor-de-precedentes` (se instalada).

## Referências desta habilidade

- `scripts/gerar_mapa.py`: lê o tema e a leitura e monta o mapa em .md e a página HTML. Rode nos passos 2, 3 e 5.
- `assets/mapa-modelo.html`: o modelo da página interna (responsivo, claro e escuro), preenchido pelo script. Use no passo 5 e no modo adaptar.
- `assets/tema-de-treino.md`: um tema de treino com sete julgados inventados (EXEMPLO), em dois tribunais, três anos e dois sentidos. Use no modo treino.
- `assets/leitura-de-treino.md`: a leitura aprovada do tema de treino, no formato que o script lê. Use no passo 4 como modelo e no modo treino.
