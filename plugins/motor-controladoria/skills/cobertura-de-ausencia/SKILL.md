---
name: cobertura-de-ausencia
description: >
  Plano de férias, licença ou viagem na controladoria: lista por script os prazos, audiências,
  perícias e sessões que vencem antes de sair, no período e nos primeiros dias úteis da volta,
  de quem sai (ou de todos, no recesso do escritório); define quem assume cada um e quem faz a
  segunda conferência; diz o que fazer antes de sair (conferir o sugerido, agendar o conferido,
  passar a pauta); registra a passagem em ausencias/ e, na volta, monta a devolução do que foi
  cumprido e do que entrou. Use quando disserem "vou tirar férias", "a advogada entra de
  licença", "quem cuida dos prazos dela?", "o recesso do escritório", "voltei, o que aconteceu
  com os meus prazos?". Não use para o resumo do dia (use rotina-da-controladoria) nem para
  conferir um prazo (use dupla-conferencia).
---

# Cobertura de ausência

> Ninguém sai de férias deixando prazo sem dono. Cada prazo, audiência e perícia do período tem quem assume, conferido antes da saída, e a volta começa pela devolução.

Regras: `../../docs/regras.md`. Prazos e status: `../../docs/prazos.md`. Contagem e dia útil: `../../docs/contagem.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela de campos em `../../docs/ficha-da-controladoria.md`. Fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Aprendizados e adaptação: `../../docs/aprender-com-o-uso.md` e `../../docs/adaptar-ao-escritorio.md`.

A advogada sai na sexta para uma semana fora. Na segunda, a publicação de um recurso chega com o nome dela como responsável, e a estagiária não sabe se pode conferir com outra pessoa nem em que agenda lançar. Na quarta, vence a data de segurança de três prazos que ninguém conferiu antes da saída. Com o plano, cada um desses prazos tem um nome ao lado desde a quinta anterior.

**Regras fixas desta habilidade:**
1. Quem assume é decisão das pessoas (quem sai e quem fica). A habilidade lista, sugere pela ficha e registra; não designa ninguém sozinha.
2. Prazo `sugerido` não passa de mão como se valesse: a dupla conferência é feita antes de sair, ou a passagem diz quem confere e quando.
3. A troca de `responsavel` no `prazos.csv` é feita linha a linha, com o ok de quem sai e de quem assume. O status nunca muda por causa da ausência.
4. Painel de tribunal continua com uma pessoa: quem assume abre com a própria senha ou certificado. Senha e certificado de quem sai nunca passam pela IA nem pelo plano.
5. Treino nunca entra no registro real.

## 1. Quando usar

**Use quando:**
- Alguém vai sair de férias, licença ou viagem e tem prazo, audiência ou perícia em nome dele (modo planejar).
- O escritório vai entrar em recesso próprio, ou metade da equipe sai na mesma semana (modo recesso, todos os responsáveis).
- Alguém saiu sem aviso (doença, urgência de família) e a equipe precisa saber hoje o que era dele (modo de surpresa).
- Quem saiu voltou e precisa saber o que aconteceu no período (modo devolução).

**Não use quando:**
- O pedido é o resumo do dia: `rotina-da-controladoria`.
- O pedido é conferir um prazo: `dupla-conferencia`, ou o `/motor-controladoria:fila`.
- O pedido é ver a carga da equipe toda na semana: `painel-da-controladoria` (se instalada).
- O pedido é mudar a data de um prazo: a data só muda pela `calcular-prazo` e pela dupla conferência.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-controladoria.md`), `nicho.md` se existir e `aprendizados-controladoria.md`. O campo `cobertura_de_ausencia` diz quem costuma assumir; `responsaveis_por_area` diz quem cumpre em cada área; `quem_confere` diz se quem sai é também quem faz a segunda conferência.
2. **Ache o registro:** `escritorio/07-operacao/controladoria/prazos.csv` (e o `publicacoes.csv` ao lado, para saber o tribunal de cada prazo).
3. **Calendários:** `escritorio/04-base/controladoria/calendario/`, para o último dia útil antes de sair e a janela da volta. Sem calendário, o plano avisa.
4. **Planos anteriores** em `07-operacao/controladoria/ausencias/`, se houver: a última devolução diz o que deu errado da outra vez.
5. **Sem ficha:** ofereça `/motor-controladoria:comecar`. Para seguir, pergunte só: "Quem assume os prazos de quem sai de férias?" (`cobertura_de_ausencia`).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `cobertura_de_ausencia` |
| Melhora | K: `responsaveis_por_area` |

Também lê, se preenchidos, K: `quem_confere`, `paineis_dos_sistemas` e `lembretes`, para a seção de passagem. Campo vazio: pergunte aquele campo, uma vez, e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Planejar | Saída marcada | Passos 1 a 9, com tempo para conferir antes de sair |
| Recesso | O escritório ou vários saem juntos | O script sem `--responsavel`, por responsável; depois, os passos 3 a 9 para cada um |
| De surpresa | Alguém saiu sem aviso | `--de` igual a hoje; primeiro o que vence até o próximo dia útil, depois o resto |
| Devolução | Quem saiu voltou | Passo 10 |
| Treino | Teste ou "é fictício" | Com `assets/prazos-de-treino.csv`, grava em `_treino/controladoria/ausencias/` |
| Adaptar | A `adaptar-controladoria` chama | A janela da volta, quem assume por área e o que a passagem leva, no jeito do escritório, com `[ALTERADO]` |

Pedido direto ("o que é da advogada na semana que vem?"): não faça entrevista. Rode o script e mostre.

### Passo 1. Quem sai e quando
Pergunte: "Quem vai sair, e de que dia a que dia?" (o primeiro e o último dia fora). Data como AAAA-MM-DD.

### Passo 2. Rodar o script
Rode com o caminho da pasta desta habilidade e o do registro. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/cobertura-de-ausencia`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/cobertura-de-ausencia/scripts/cobertura.py" \
  "escritorio/07-operacao/controladoria/prazos.csv" \
  --responsavel "[QUEM SAI]" --de AAAA-MM-DD --ate AAAA-MM-DD --data AAAA-MM-DD
```

Outras opções: `--assume "[NOME]"` (do campo `cobertura_de_ausencia`, depois da resposta do passo 3), `--confere "[NOME]"`, `--volta N` (dias úteis depois da volta que entram no plano, padrão 3), `--publicacoes`, `--calendario`, `--feriados`, `--saida`, `--devolucao`, `--treino` (obrigatório para `_treino/`). Sem `--responsavel`, o script lista o período de todos, por responsável. O nome é comparado sem diferenciar maiúscula nem acento. O script lê csv de vírgula ou ponto e vírgula, com ou sem BOM, e datas AAAA-MM-DD ou DD/MM/AAAA. Sai com código 1 e "ERRO:" quando falta o arquivo ou coluna obrigatória, o registro não tem nenhuma linha, uma data é inválida, `--ate` vem antes de `--de` ou o registro é de treino sem `--treino`. Nunca diz que o período está livre sem ter lido linhas.

O plano tem: **antes de sair** (segurança ou fatal de hoje até o último dia útil antes da saída), **no período**, **na volta** (os primeiros dias úteis), **pendências do registro** (fatal passada sem cumprimento, prazo sem data, prazo sem responsável que vence até a volta), **passagem** e o espaço da **devolução**.

### Passo 3. Quem assume
Mostre a lista do período e pergunte: "Quem assume estes prazos? Pela ficha, costuma ser [cobertura_de_ausencia]." Se a ficha divide por área (`responsaveis_por_area`), sugira por área, marcado "sugestão". Prazo que a pessoa quer resolver antes de sair (protocolar antes) sai da coluna "quem assume" com a anotação "cumprir antes de sair". Rode o script de novo com `--assume`.

### Passo 4. Quem confere
Se quem sai é o `quem_confere` (ou é a única pessoa que confere), pergunte: "Quem faz a segunda conferência enquanto [nome] estiver fora?". Sem resposta, `[A DEFINIR]` no plano e o aviso: nenhum prazo novo do período passa de `sugerido` sem alguém para conferir.

### Passo 5. Antes de sair
Para cada linha, o script diz o que fazer:
- `sugerido` do período: dupla conferência antes de sair (`dupla-conferencia`, se instalada; sem ela, os passos de `prazos.md`). Quem assume não recebe data sem conferência.
- `conferido` sem agenda: agendar já na agenda de quem assume (`agenda-de-prazos`, se instalada; sem ela, o texto do compromisso para a pessoa lançar).
- `agendado`: o compromisso passa para a agenda de quem assume, com os lembretes da ficha (remarcação pela `agenda-de-prazos`, se instalada).
- audiência e perícia: confirmar data, hora e link, quem vai, e o aviso ao cliente de quem estará lá (preparar-o-cliente, do motor-experiencia, se instalado, pela entrada da experiência; sem ele, o texto para a pessoa enviar).

### Passo 6. Painéis e publicações
Pergunte: "Quem abre os painéis dos sistemas enquanto [nome] estiver fora?". Quem assume abre com a própria senha ou certificado e registra pela `paineis-dos-sistemas` (se instalada). Publicação nova do período com o nome de quem saiu: a triagem põe o `responsavel` de quem assumiu, e o plano diz isso.

### Passo 7. Mostrar e combinar
Mostre o plano inteiro às duas pessoas (quem sai e quem assume). Pergunte: "Está combinado assim?". Ajuste o que pedirem. A passagem é H: a habilidade prepara, as pessoas combinam.

### Passo 8. Gravar e trocar o responsável
Com o ok, grave em `escritorio/07-operacao/controladoria/ausencias/<quem-sai>-AAAA-MM-DD.md` (o nome em minúsculas, sem acento, com hífen; a data é a da saída). Depois pergunte: "Troco o responsável destes prazos no registro, linha a linha?". Com o ok das duas pessoas, mude só `responsavel`, `atualizado_em` e acrescente em `observacao` "cobertura de [quem sai] de AAAA-MM-DD a AAAA-MM-DD". O status não muda.

### Passo 9. Avisar
Uma linha para o resumo do dia (PARA DECIDIR, se faltar alguém) e, se a equipe usa, um item `item: aviso` na fila (`NN-aviso-cobertura.md`) com o caminho do plano. Nada vai para cliente sem uma pessoa aprovar.

### Passo 10. Devolução (na volta)
Rode o script com `--devolucao`, com as mesmas datas e o `--assume`, e `--saida` apontando para o plano (a devolução é acrescentada no fim dele):
- o que venceu no período e como ficou (cumprido, com a data; em aberto com a fatal passada vai para PESSOA AGORA, e só a pessoa registra `perdido`);
- o que entrou durante a ausência com quem assumiu: devolver ou manter é decisão das duas pessoas.
Com o ok, devolva o `responsavel` linha a linha, como no passo 8.

### Passo 11. Aprender
Pergunte: "Alguma coisa ficou sem dono, ou foi passada tarde demais?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md` (por exemplo: "prazo de recurso do período é protocolado antes de sair, nunca passado"). Regra que vale sempre para ausências pode subir para `cobertura_de_ausencia` ou `regras_proprias` na ficha.

## 4. Exemplo resolvido (treino)

Copie `assets/prazos-de-treino.csv` para `escritorio/07-operacao/_treino/controladoria/ausencias/prazos.csv`. A advogada do Escritório Modelo sai de 2026-04-20 a 2026-04-24; hoje é 2026-04-14:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/cobertura-de-ausencia/scripts/cobertura.py" \
  "escritorio/07-operacao/_treino/controladoria/ausencias/prazos.csv" \
  --responsavel advogada --de 2026-04-20 --ate 2026-04-24 --data 2026-04-14 \
  --assume "advogada parceira" --treino
```

Com o calendário de treino da `calendario-forense` (se instalada), o que tem que sair: último dia útil antes de sair 2026-04-17 (2026-04-16 é o feriado de treino); volta 2026-04-27, janela até 2026-04-29. **No período:** Camila (PZ-2026-0003), Renata (PZ-2026-0004) e Paulo (PZ-2026-0006), segurança 2026-04-22 e fatal 2026-04-24, todos `sugerido`, com "fazer a dupla conferência antes de sair". **Na volta:** Otávio (PZ-2026-0001), segurança 2026-04-28. Fora do plano: Marta (2026-05-07 e 2026-05-11) e a audiência do Paulo (2026-05-20). Nenhuma data sai como se valesse.

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Plano de cobertura, com a passagem combinada | `escritorio/07-operacao/controladoria/ausencias/<quem-sai>-AAAA-MM-DD.md` |
| Devolução | No fim do mesmo arquivo, na volta |
| Troca de responsável | `prazos.csv`, colunas `responsavel`, `observacao` e `atualizado_em`, linha a linha, com o ok |
| Aviso na fila (se a equipe usa) | `07-operacao/controladoria/fila/AAAA-MM-DD/NN-aviso-cobertura.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/ausencias/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: o plano sai no chat, com a lista feita à mão a partir das linhas coladas, e a troca de responsável vira a tabela para a pessoa colar na planilha.

## 6. Solo e equipe

**Solo:** sem ninguém para assumir, o plano serve para outra coisa: o que precisa ser cumprido antes de sair, o colega de confiança que pode ser substabelecido para uma audiência (decisão do advogado, com `[CONFERIR]` na forma), e as datas que caem na volta. Recesso do escritório que não coincide com o dos tribunais é o caso mais perigoso: rode sem `--responsavel` e olhe o período inteiro.

**Equipe:** o plano é combinado entre quem sai e quem assume, com uma terceira pessoa sabendo (a de `responsavel_controladoria`). Quem assume recebe o plano antes da saída, nunca no primeiro dia. Se uma pessoa assume a carteira de duas, rode o `painel-da-controladoria` (se instalada) para ver a carga somada.

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Prazo do período sem dono | Ninguém olha até a fatal | Cada linha do período com "quem assume" |
| Sugerido passado como certo | Quem assume cumpre por uma data que ninguém conferiu | Dupla conferência antes de sair, marcada na linha |
| Quem confere sai junto | Nenhum prazo novo passa de `sugerido` na semana | Passo 4 pergunta quem confere no período |
| Prazo da volta esquecido | O primeiro dia de volta começa com prazo vencendo | Janela da volta no plano |
| Senha de quem saiu repassada | Risco de segurança e de responsabilidade | Regra fixa 4: quem assume usa o próprio acesso |
| Volta sem saber o que aconteceu | Prazo cumprido duas vezes ou não cumprido | Devolução por script, linha a linha |
| Script sem registro dizendo que o período está livre | Férias tranquilas com prazo na mesa | Código 1 sem arquivo ou sem linha |

## 8. Próximo passo

- Sugeridos do período: `dupla-conferencia` ou `/motor-controladoria:fila`.
- Agenda de quem assume: `agenda-de-prazos` (se instalada).
- Aviso ao cliente sobre quem cuida no período: `encaminhar-providencia` (se instalada), pela entrada do motor-experiencia (se instalado).
- Painéis no período: `paineis-dos-sistemas` (se instalada).
- Carga somada de quem assume: `painel-da-controladoria` (se instalada).

## Referências desta habilidade

- `scripts/cobertura.py`: o plano e a devolução por script (cópia própria da leitura de registros e calendários). Rode nos passos 2, 3 e 10.
- `assets/prazos-de-treino.csv`: o registro do lote de treino, para o exemplo da seção 4.
