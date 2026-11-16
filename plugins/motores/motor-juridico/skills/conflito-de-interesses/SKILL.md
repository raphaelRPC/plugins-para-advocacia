---
name: conflito-de-interesses
description: >
  Antes de aceitar um caso, cruza as partes do caso novo (cliente, parte contrária, terceiros)
  com a base de partes do escritório (04-base/juridico/partes.csv) por script: nome normalizado
  sem acento e sem sufixo societário, semelhança de nome, CNPJ quando houver. Aponta cada
  coincidência com o que ela significa (parte contrária que é ou foi cliente, novo cliente que
  foi parte contrária), registra a checagem na pasta do caso e para na decisão do advogado. Também
  monta e atualiza a base. Use quando o advogado disser "checa conflito", "esse restaurante já foi
  nosso cliente?", "posso pegar esse caso?", "roda o conflito antes da consulta", "atualiza a base
  de partes". Não use para decidir se vale entrar com a ação (use estrategia-do-caso) nem para
  triar o contato (use triar-contato, do motor-comercial).
---

# Conflito de interesses

> Antes de ouvir o caso inteiro, o escritório precisa saber se a outra parte é ou foi cliente dele. O script cruza os nomes e mostra cada coincidência. Quem decide é o advogado.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e pasta do caso: `../../docs/producao.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Paulo foi dispensado e quer entrar contra o antigo empregador, o Restaurante Sabor Mineiro. A consulta está marcada para amanhã. O estagiário não sabe que, em 2025, o escritório fez o consultivo trabalhista desse restaurante. Se a consulta acontece sem a checagem, o escritório ouve a estratégia de um contra o outro. A checagem de dois minutos, antes, mostra a coincidência e leva a decisão à advogada.

**Regras fixas desta habilidade:**
1. A checagem roda antes da consulta ou da análise do caso, assim que se sabe o nome da parte contrária. Caso que chegou sem ela não anda no ciclo.
2. O script aponta; o advogado decide: aceitar, recusar ou aceitar com as providências que o Código de Ética e Disciplina da OAB exigir `[CONFERIR: artigos sobre conflito de interesses e sigilo, redação vigente]`. A IA não diz que "não há conflito": diz o que a base sabe.
3. O motivo de uma recusa por conflito é sigiloso. A mensagem ao contato nunca diz quem é o outro cliente nem que há outro cliente.
4. A base guarda o mínimo: nome, papel, caso, área, ano e CNPJ de empresa. CPF, endereço e telefone ficam no sistema do escritório, fora do plugin.
5. Base vazia ou não lida não vira "nada encontrado". O script sai com erro e a checagem fica por fazer.

## 1. Quando usar

**Use quando:**
- Um contato vai para consulta e já se sabe quem é a parte contrária (modo checar).
- Um caso novo chegou ao jurídico pela passagem do comercial ou por pedido do advogado (modo checar).
- O `agente-juridico` ou a `rotina-juridica` achou caso novo com partes (modo no ciclo).
- O escritório ainda não tem a base de partes, ou quer importar a do sistema (modo montar a base).
- O advogado aceitou um caso e as partes novas precisam entrar na base (modo atualizar a base).
- Teste com o caso 2 dos casos fictícios (modo treino), ou a `adaptar-juridico` pediu as palavras genéricas do nicho (modo adaptar).

**Não use quando:**
- O pedido é decidir se vale entrar com a ação ou qual tese seguir: `estrategia-do-caso`.
- O pedido é classificar a mensagem de quem ainda não é cliente: `triar-contato`, do motor-comercial (se instalado).
- O pedido é checar impedimento ou suspeição de juiz, perito ou servidor: fora deste plugin; o advogado confere.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`), `nicho.md` se existir e os aprendizados (`aprendizados-juridico.md`). O campo `base_de_partes` diz onde o escritório guarda as partes de casos antigos.
2. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Onde estão os clientes e as partes contrárias dos casos antigos de vocês?".
3. **Leia a base** (`escritorio/04-base/juridico/partes.csv`). Sem base: diga que a checagem não tem com o que cruzar e ofereça o modo montar a base. Até lá, a pergunta vai direto ao advogado: "Alguma destas partes já foi cliente ou parte contrária de vocês?".
4. **A base fica fora do Projeto no Claude.** Mesmo estando em `04-base/`, o `partes.csv` tem nomes de pessoas e empresas que o escritório atendeu. Use na pasta de trabalho, em conta profissional.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `base_de_partes` |
| Melhora | E: `quem_atende` |

Campo que falta e a checagem precisa: pergunte aquele campo, uma vez, e ofereça gravar. Sem `quem_atende`, a decisão vai para "o advogado responsável", e o fim da checagem avisa.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Checar | Caso novo, antes da consulta ou da análise | Código do caso e as partes | O relatório da checagem e a pergunta ao advogado |
| No ciclo | O agente chama | Caso novo em `entrada/` ou nas passagens | Registro da checagem e uma linha em ADVOGADO AGORA quando acusa |
| Montar a base | Primeira vez | A lista de casos antigos (planilha ou sistema) | O `partes.csv`, mostrado antes de gravar |
| Atualizar a base | Caso aceito | As partes do caso | Linhas novas no `partes.csv`, com o ok |
| Treino | Caso fictício | Caso 2 e a base de treino | O mesmo, em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | `nicho.md` e a base | Palavras genéricas do nicho e casos de teste |

Pedido direto ("checa conflito do Paulo contra o Restaurante Sabor Mineiro"): não faça entrevista. Rode o script e mostre.

### Passo 1. Juntar as partes do caso novo
Pergunte, uma por vez, só o que falta:
- "Quem é o cliente?" (nome como vai na peça; empresa com o CNPJ, se o contato informou).
- "Quem é a parte contrária?" (todas: empregador e tomador de serviço, réus em conjunto, o ex-cônjuge).
- "Tem mais alguém no caso?" (terceiro interessado, fiador, litisconsorte, sócio da empresa). Papel `outra`.
Nome incompleto ("o restaurante da esquina"): peça o nome que está no documento. Sem ele, rode com o que há e marque `[A CONFIRMAR]` no registro.

### Passo 2. Rodar o script
**Sem base** (`partes.csv` não existe, ou a ficha diz `base_de_partes: não há`): não rode o script. Diga: "Não há base de partes para conferir. Alguma dessas partes já foi cliente ou parte contrária do escritório?" Com a resposta, grave no registro "checagem feita com a informação do advogado, sem base", siga para o passo 4 e ofereça o modo montar a base.

Rode `scripts/checar_conflito.py` (seção 4) com o código do caso e uma `--parte` para cada pessoa ou empresa, e `--saida` para o registro na pasta do caso. Mostre o resultado inteiro: a primeira linha diz se acusou.

### Passo 3. Ler o resultado com o advogado
| O script diz | O que a habilidade faz |
|---|---|
| ACUSOU (conflito provável) | Para. Diz em uma frase: "[PARTE] aparece na base como cliente no caso [CÓDIGO]. A decisão é sua: aceitar, recusar ou aceitar com as providências que a ética exige." Nenhuma consulta, análise ou minuta segue antes da decisão |
| Coincidência sem conflito provável (cliente repetido, parte contrária repetida) | Mostra e pergunta: "Isso muda alguma coisa para vocês?" |
| Fraca (só o primeiro nome) | Pergunta: "Na base está só '[NOME]'. É a mesma pessoa? O sistema do escritório tem o nome completo." |
| Nada encontrado | Diz: "Nada na base de [N] registros. Quer seguir?" A decisão continua do advogado |

### Passo 4. Registrar a decisão
Com a resposta do advogado, complete no registro (`casos/<codigo>/conflito-de-interesses.md`) a decisão, quem decidiu e a data, e o que foi feito (por exemplo, "providências do Código de Ética `[CONFERIR]` tomadas pelo advogado"). Mostre e grave com o ok.
- **Aceitou:** o caso segue para `dossie-do-caso` e a peça pode entrar no `pecas.csv`. Ofereça o modo atualizar a base.
- **Recusou:** o caso não entra no `pecas.csv`. A mensagem de recusa ao contato sai pela `mensagens-comerciais`, do motor-comercial (se instalado; sem ele, a advogada escreve), sem dizer o motivo: "o escritório não pode assumir este caso" e o encaminhamento da ficha. Nada sobre o outro cliente.
- **Pediu mais informação:** o item fica em ADVOGADO AGORA até a resposta.

### Passo 5. Aprender
Pergunte: "Tem algum nome que o script devia ter achado, ou achou sem motivo?". Palavra genérica nova do nicho ("auto peças", "agropecuária") ou um apelido conhecido de cliente ("o Sabor", para o restaurante) vira regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Apelido conhecido também vai para a coluna `observacao` da linha na base, para a próxima checagem.

### Modo no ciclo
1. O agente passa o caso novo com as partes. Não pergunte nada e não mostre nada.
2. Rode o script com `--saida "escritorio/07-operacao/juridico/casos/<codigo>/conflito-de-interesses.md"`.
3. **Acusou:** uma linha em ADVOGADO AGORA no resumo, com o porquê em uma frase e sem o nome do outro cliente ("parte contrária coincide com cliente antigo; ver o registro do conflito"). Nada de dossiê, estratégia ou minuta para esse caso até a decisão.
4. **Fraca ou coincidência sem conflito provável:** linha em "para decidir", e o caso pode seguir para o dossiê.
5. **Nada encontrado:** registro gravado; o caso segue.
6. **Sem base ou sem parte contrária conhecida:** não rode o script. Linha em "PARA DECIDIR" com "checagem de conflito por fazer: [motivo]". O caso pode seguir para o dossiê, mas não para a estratégia, até o advogado responder no comando `fila`.
7. O ciclo nunca grava a decisão nem atualiza a base.

### Modo montar a base
1. Pergunte: "De onde vêm os casos antigos? Sistema, planilha, pastas?" (`base_de_partes`).
2. Peça a lista exportada (planilha ou csv) e monte o `partes.csv` com a primeira linha da seção 5: uma linha por pessoa ou empresa e por caso. Cliente e parte contrária de cada caso; terceiros quando o escritório registrou.
3. Tire o que não é necessário: CPF, endereço, telefone, valor. CNPJ só de empresa. Nome como está no documento do caso.
4. Mostre as primeiras linhas e a contagem ("312 linhas, 140 clientes, 172 partes contrárias, 41 com CNPJ") e grave com o ok.
5. Rode o caso de treino (seção 6) contra a base nova para conferir que o script lê.

### Modo atualizar a base
Depois do aceite, monte as linhas do caso (cliente, partes contrárias, terceiros) e mostre. Com o ok, acrescente ao `partes.csv`. Nunca apague linha: caso encerrado muda só `situacao`.

### Modo treino
Base `assets/partes-de-treino.csv` (a base de `../../docs/casos-ficticios.md`), copiada para `escritorio/07-operacao/_treino/juridico/partes.csv`. Tudo grava em `_treino/`, e o script roda com `--treino`. O teste está na seção 6.

### Modo adaptar
1. Leia `nicho.md` e uma amostra da base.
2. Proponha as palavras genéricas do nicho que não devem contar como nome (no comércio: "comércio", "loja", "distribuidora"; no agro: "agropecuária", "fazenda"), marcadas `[ALTERADO]` em relação à lista do script, e grave com o ok em `aprendizados-juridico.md`.
3. Devolva à `adaptar-juridico` três casos de teste do escritório, anonimizados: um que acusa, um com semelhança fraca, um sem coincidência.

## 4. O script

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/conflito-de-interesses/scripts/checar_conflito.py" \
  "escritorio/04-base/juridico/partes.csv" --caso C-AAAA-NNNN \
  --parte "NOME DO CLIENTE; cliente" --parte "NOME DA PARTE CONTRÁRIA; parte-contraria; CNPJ" \
  --saida "escritorio/07-operacao/juridico/casos/C-AAAA-NNNN/conflito-de-interesses.md"
```

Sem `${CLAUDE_PLUGIN_ROOT}`, troque pelo caminho da pasta desta habilidade. Muitas partes: `--novas partes-do-caso.csv`, com as colunas `nome`, `papel` e `cnpj`. Outras opções: `--data AAAA-MM-DD`, `--treino`. `--help` mostra tudo.

| Como compara | Nível |
|---|---|
| Mesmo CNPJ | coincidência |
| Mesmo nome depois de normalizar: minúsculas, sem acento, sem pontuação, sem sufixo societário (Ltda., ME, EPP, Eireli, S.A., Cia.) e sem "de", "da", "e" | coincidência |
| Mesma raiz de CNPJ (os oito primeiros dígitos: matriz e filial, ou o mesmo grupo) | semelhança |
| Mesmo nome sem as palavras genéricas (restaurante, comércio, serviços, transportes e outras) | semelhança |
| Nomes quase iguais (88% ou mais), o erro de digitação | semelhança |
| A maior parte das palavras que distinguem o nome em comum, em qualquer ordem | semelhança |
| Só o primeiro nome bate com um nome curto da base | fraca |

O papel decide o significado: parte contrária do caso novo que é ou foi cliente, ou novo cliente que foi parte contrária, é "CONFLITO PROVÁVEL". Cliente que volta e parte contrária repetida aparecem para o advogado ver, sem esse rótulo. Linhas da base do mesmo caso são ignoradas.

O script lê vírgula ou ponto e vírgula, com ou sem BOM, UTF-8 ou o padrão do Excel, e papel escrito de vários jeitos ("Cliente (consultivo trabalhista, 2025)", "parte contrária", "contrária"). Sai com código 1 e "ERRO:" quando falta a base, ela está vazia, falta coluna (`nome`, `papel`, `codigo_caso`), nenhuma parte foi informada, a parte vem sem papel, o código do caso está fora do padrão, ou recebe a base de treino sem `--treino`. Sem Python, a pessoa procura cada nome na planilha da base, sem acento e sem o "Ltda.", e lê a coluna `papel`.

## 5. A base de partes

```
nome,cnpj,papel,codigo_caso,area,ano,situacao,observacao
```

| Coluna | O que vai | Exemplo (fictício) |
|---|---|---|
| `nome` | Como está no documento do caso | Restaurante Sabor Mineiro Ltda. |
| `cnpj` | Só de empresa, quando houver | |
| `papel` | `cliente`, `parte-contraria` ou `outra` | cliente |
| `codigo_caso` | O código do caso (C-AAAA-NNNN) | C-2025-0071 |
| `area` | Área da ficha | trabalhista |
| `ano` | Ano de início do caso | 2025 |
| `situacao` | `ativo` ou `encerrado` | encerrado |
| `observacao` | Uma linha, sem dado sensível: tipo de trabalho, apelido conhecido | consultivo trabalhista |

## 6. Exemplo resolvido (treino com o caso 2)

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/conflito-de-interesses/scripts/checar_conflito.py" \
  "escritorio/07-operacao/_treino/juridico/partes.csv" --caso C-2026-0002 \
  --parte "Paulo; cliente" --parte "Restaurante Sabor Mineiro Ltda.; parte-contraria" --treino \
  --saida "escritorio/07-operacao/_treino/juridico/casos/C-2026-0002/conflito-de-interesses.md"
```

O script devolve "ACUSOU: 1 coincidência(s) com conflito provável": o Restaurante Sabor Mineiro Ltda., parte contrária do caso novo, aparece como cliente no caso C-2025-0071. O mesmo acontece com o nome escrito "RESTAURANTE SABOR MINEIRO LTDA - ME", "Sabor Mineiro" ou "Restaurante Sabor Mineyro" (semelhança). "Restaurante Sabor Paulista Ltda." não acusa. A habilidade para e pergunta à advogada. Os casos 1 (Marta contra o INSS) e 3 (Renata) não acusam nada na base de treino.

Se a advogada recusar, a peça P-2026-0002 do treino da `rotina-juridica` não segue: ela decide pelo `/motor-juridico:fila`, que grava `suspensa` no `pecas.csv`.

## 7. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Registro da checagem e a decisão | `escritorio/07-operacao/juridico/casos/<codigo>/conflito-de-interesses.md` |
| Base de partes | `escritorio/04-base/juridico/partes.csv` (fora do Projeto no Claude) |
| Linha em ADVOGADO AGORA ou "para decidir" (no ciclo) | `escritorio/07-operacao/juridico/rotina/AAAA-MM-DD.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções e palavras genéricas aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O registro guarda as partes checadas, o que o script achou, a decisão, quem decidiu e quando. Ele fica no escritório e não vai para o processo nem para o cliente. Sem pasta aberta: a pessoa cola as linhas da base que interessam e a checagem é feita no chat, com o registro em bloco para guardar.

## 8. Solo e equipe

**Solo:** a checagem entra no roteiro de agendar a consulta. Ao saber o nome da parte contrária, roda; se acusar, decide antes de ouvir o caso.

**Equipe:** quem marca a consulta (`quem_atende`) roda a checagem e avisa o advogado responsável só quando acusa. A base é de uma pessoa (a que fecha os contratos), que a atualiza a cada caso aceito. Quando a equipe cresce, peça que o sistema jurídico do escritório seja a fonte e o `partes.csv` seja exportado dele toda semana.

## 9. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Consulta com a parte contrária de um cliente | O escritório ouve informação sigilosa dos dois lados | Checagem antes da consulta, regra 1 |
| "Ltda.", acento ou maiúscula escondendo o mesmo nome | Conflito não visto | Nome normalizado e semelhança |
| Palavra genérica gerando alarme | "Restaurante" de um acusa todos os restaurantes | Palavras genéricas fora da comparação |
| Base vazia lida como "sem conflito" | Falsa segurança | Script sai com erro; checagem fica por fazer |
| Recusa que revela o outro cliente | Quebra de sigilo | Mensagem de recusa sem motivo |
| CPF na base | Dado a mais circulando | Base mínima, CNPJ só de empresa |
| IA decidindo que não há conflito | Responsabilidade que é do advogado | Script aponta; decisão registrada com quem decidiu |

## 10. Próximo passo

- Aceito: `dossie-do-caso`, e a linha da peça no `pecas.csv` (a `rotina-juridica` acompanha).
- Recusado: `mensagens-comerciais`, do motor-comercial (se instalado), com a recusa sem motivo; sem ele, a advogada escreve.
- Base nova ou desatualizada: modo montar a base, e depois atualizar a cada caso aceito.

## Referências desta habilidade

- `scripts/checar_conflito.py`: o script da checagem (só biblioteca padrão). Rode no passo 2 e no modo no ciclo.
- `assets/partes-de-treino.csv`: a base de partes dos casos fictícios. Use no modo treino e para testar uma base nova.
- `references/registro-da-checagem.md`: o modelo do registro com a decisão do advogado e os textos de cada decisão. Leia no passo 4.
