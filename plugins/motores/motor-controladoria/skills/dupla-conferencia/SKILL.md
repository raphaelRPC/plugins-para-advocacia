---
name: dupla-conferencia
description: Conduz a dupla conferência de cada prazo antes de ele valer: duas leituras cegas do ato (a segunda sem ver a primeira nem a sugestão da IA) sobre o que o ato pede, o número de dias, o rito e o dobro, e as duas contas independentes do script. Bateu, o prazo vira conferido com os nomes que as próprias pessoas disseram; não bateu, fica sugerido, a divergência vai para a fila e vale a data mais cedo. Registra cada conferência em conferencias/AAAA-MM-DD.md e cobre o escritório de uma pessoa só (segundo turno). Use quando disserem "vamos conferir os prazos", "confere o prazo da Renata", "faz a segunda conferência", "a estagiária contou diferente", "sou eu sozinha, como confiro?". Não use para fazer a primeira conta de um prazo (use calcular-prazo).
---

# Dupla conferência

> Duas leituras do ato, sem uma ver a outra, e duas contas que não dependem uma da outra: o prazo só vale quando tudo bate.

Registros, status e a dupla conferência: `../../docs/prazos.md`. Regras de contagem: `../../docs/contagem.md`. Regras gerais: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 16h. A estagiária conferiu as custas da Renata e contou o vencimento em 2026-04-27, porque o TJMG anunciou manutenção do PJe no dia 24. A advogada leu o mesmo ato, sem ver a resposta dela, e contou 2026-04-24. As duas não batem, e o prazo não vai para a agenda como conferido. O script mostra o motivo: a manutenção não tem certidão e não empurra o prazo. Até a decisão, vale o dia 24.

**Regras fixas desta habilidade:**
1. A IA nunca escreve um nome em `conferido_por`. Só registra a conferência que a própria pessoa diz, na conversa, que fez, com o nome que ela der.
2. A segunda leitura é cega: quem confere vê o trecho literal do ato e responde antes de ver a primeira leitura e a sugestão da IA.
3. Conferido exige as duas leituras iguais e as duas contas do script iguais. Qualquer diferença deixa o prazo `sugerido`, com a divergência na fila.
4. Na divergência, vale a data mais cedo até a pessoa decidir.
5. Prazo com segurança ou fatal hoje ou amanhã é conferido primeiro, antes de qualquer outro item.

## 1. Quando usar

**Use quando:**
- Há prazos `sugerido` em `prazos.csv` e itens `conferir-prazo` na fila com o revisor já passado (`revisor` diferente de `pendente`).
- O `/motor-controladoria:fila` chegou num `item: conferir-prazo`.
- A estagiária e a advogada contaram datas diferentes e alguém precisa decidir.
- O escritório tem uma pessoa só e quer saber como conferir (segundo turno).
- O `/motor-controladoria:comecar` mostra a dupla conferência com a linha 1 do lote de treino, ou alguém treina com a dupla conferência de treino.
- A `adaptar-controladoria` (se instalada) chamou no modo "adaptar".

**Não use quando:**
- O prazo ainda não foi contado: `calcular-prazo`.
- Um lote inteiro de prazos precisa de conferência: `prazos-em-lote` (se instalada), que usa este mesmo método linha por linha.
- O prazo já está conferido e só precisa ir para a agenda: `agenda-de-prazos` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-da-controladoria.md` e `nicho.md`, se existir.
2. **Leia os aprendizados** (`aprendizados-controladoria.md`). Nenhum aprendizado dispensa a segunda leitura.
3. **Ache o prazo:** a linha em `escritorio/07-operacao/controladoria/prazos.csv` e o item em `fila/AAAA-MM-DD/NN-<codigo>-prazo.md`. Item com `revisor: pendente` não pode ser conferido: o revisor passa antes. Item `bloqueado` não aparece.
4. **Ache a base:** `04-base/controladoria/regras-de-contagem.md` e `calendario/`, para as duas contas.
5. **Quem está digitando:** o plugin não tem como saber. Cada pessoa confere na própria conta, ou diz o nome no começo da conversa.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `quem_confere`, `responsavel_controladoria` |
| Melhora | K: `regras_validadas_em` |

Sem `quem_confere`, pergunte: "Quem faz a segunda conferência dos prazos? Se você trabalha sozinho, é você mesmo, em outro turno." e ofereça gravar. Sem ele, nenhum prazo passa de `sugerido`. `responsavel_controladoria` costuma fazer a primeira leitura. `regras_validadas_em` vazio ou com mais de um ano: avise antes de começar que a conta vai sair com "regra ainda não validada pelo escritório".

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Um prazo | A pessoa pede, ou o `/fila` chega no item | O item `conferir-prazo` | Primeira ou segunda leitura gravada; `conferido` ou divergência |
| Segundo turno | Escritório de uma pessoa só | O item com a primeira leitura feita | A segunda leitura da mesma pessoa, em outro turno |
| Decidir divergência | Item com divergência | As duas leituras e as contas | A decisão de quem a ficha diz; nova conta conferida |
| Treino | `comecar`, "é teste" | A dupla conferência de treino | O resultado do gabarito, gravado em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | `nicho.md` e a ficha | As perguntas da leitura para os atos do nicho |

No ciclo, esta habilidade não roda: o agente só deixa o item pronto. A conferência é sempre de uma pessoa.

### Passo 1. Ordem
Liste os prazos `sugerido` que estão prontos para conferir, o que vence primeiro no topo. Os de segurança ou fatal hoje ou amanhã vêm antes de tudo, com a frase "este é para agora".

### Passo 2. Quem confere
Pergunte: "Quem está fazendo esta conferência?". Grave o nome só como a pessoa disse. Se já existe a primeira leitura no item, esta é a segunda.

### Passo 3. A leitura cega
Mostre só: o trecho literal do ato, o tribunal e o órgão, a fonte e a data de partida (disponibilização, envio ou ciência). Não mostre a providência sugerida, o número de dias da IA, as datas nem a outra leitura. Pergunte, nesta ordem, uma por vez:
1. "O que este ato pede?"
2. "Em quantos dias, e de onde vem esse número: do próprio ato ou da tabela do escritório?"
3. "Qual é o rito, e há prazo em dobro?"
4. "Você contou a data? Se contou, qual deu?" (pode responder "não contei")

Grave a resposta no item, num bloco `primeira_conferencia:` ou `segunda_conferencia:`, com o nome e a hora. Na primeira, diga: "Pronto. A segunda leitura é de [quem_confere], sem ver esta resposta." e pare.

### Passo 4. A segunda leitura
- **Outra pessoa:** ela abre a fila (`/motor-controladoria:fila`) ou pede esta habilidade numa conversa nova, e não abre o arquivo do item antes de responder. Repita os passos 2 e 3.
- **Escritório de uma pessoa só** (`quem_confere` diz "eu mesma, em outro turno"): a segunda leitura é em outro turno (por exemplo, a primeira de manhã e a segunda depois do almoço), numa conversa nova, antes da data de segurança. Grave `segunda_por: <nome>; 2º turno`. Na mesma hora da primeira, recuse com calma: "A segunda leitura precisa ser em outro turno. Quer que eu deixe para depois do almoço?".
- **Mesma pessoa sem a ficha permitir:** "A segunda conferência é de outra pessoa. Quem pode fazer?".

### Passo 5. As duas contas
Com as duas leituras gravadas, rode o script da `calcular-prazo` com os dados confirmados:

```
python3 "<pasta da calcular-prazo>/scripts/calcular_prazo.py" \
  --disponibilizacao 2026-04-14 --dias 5 --rito civel --tribunal TJMG \
  --calendario escritorio/04-base/controladoria/calendario/ \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md --seguranca 2 --duplo
```

No Cowork e no Claude Code, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/calcular-prazo`. A conta 1 anda dia a dia; a conta 2 monta a lista de dias úteis e indexa. Se as leituras discordam no número de dias, no rito ou no dobro, rode uma conta para cada leitura e mostre as duas datas. Sem a `calcular-prazo` instalada ou sem código: as duas contas à mão, por duas pessoas, dia por dia, com o calendário na conversa.

### Passo 6. Comparar
Mostre agora, lado a lado: a primeira leitura, a segunda, a sugestão da IA e as duas contas.

| Confere | Bate quando |
|---|---|
| O que o ato pede | As duas pessoas dizem que é o mesmo ato (a IA não decide se dois textos querem dizer a mesma coisa: pergunta) |
| Número de dias e a fonte | Iguais |
| Rito e regra | Iguais |
| Dobro | As duas dizem sim, ou as duas dizem não |
| Data contada à mão | Igual à das contas, quando alguém contou |
| Conta 1 e conta 2 | Mesmo início, vencimento e segurança (o script diz "AS DUAS CONTAS BATEM") |

### Passo 7. Bateu
1. Pergunte: "As duas leituras e as duas contas batem. Posso marcar como conferido, com [nome 1] e [nome 2]?".
2. Com o ok, em `prazos.csv`: `status = conferido`, `conferido_por = <nome 1>; <nome 2>` (ou `<nome>; 2º turno`; na planilha separada por ponto e vírgula, o campo vai entre aspas), `conferido_em = AAAA-MM-DD HH:MM` da segunda leitura, `atualizado_em`. Se as pessoas corrigiram a sugestão da IA (outro número de dias, outro rito), grave também os dados e as datas da conta confirmada e escreva na `observacao`: "corrigido na conferência: <o que mudou>".
3. No item: `status: aprovado`.
4. Registro: uma linha em `escritorio/07-operacao/controladoria/conferencias/AAAA-MM-DD.md`, no modelo de `assets/modelo-do-registro.md`, com `resultado = bateu`.
5. Ofereça a `agenda-de-prazos` (se instalada; sem ela, mostre o texto do compromisso: data de segurança como compromisso, fatal como limite, responsável).

### Passo 8. Não bateu
1. Diga em uma frase onde está a diferença ("a primeira leitura empurrou o vencimento pela manutenção do PJe; a manutenção não tem certidão").
2. O prazo fica `sugerido`. No item: o bloco `divergencia:` com as duas leituras, as datas e a mais cedo, e a linha em `antes_de_enviar`: "divergência: vale [data mais cedo] até a decisão".
3. A data mais cedo vale até a decisão, mas nada entra na agenda antes de `conferido` (regra 1 da `agenda-de-prazos`): nem lembrete provisório, nem compromisso lançado à mão. A divergência fica na fila e no resumo da rotina, com a data mais cedo. Quando essa data (de segurança ou fatal) está a 2 dias úteis ou menos, ela sobe para PESSOA AGORA: "Divergência sem decisão: [id] vence em [data mais cedo]. Quem decide hoje?".
4. Registro com `resultado = divergiu` e `vencimento_final` vazio.
5. Pergunte: "Quem decide esta divergência?" (em geral, quem responde pela controladoria ou a advogada do caso).

### Passo 9. Decidir a divergência
Com quem decide na conversa: mostre as duas leituras, as contas e a regra de `contagem.md` em jogo. A decisão é dela. Com a decisão, rode a conta de novo com os dados decididos (`--duplo`); se as duas contas batem, siga o passo 7 com `conferido_por = <nome 1>; <nome 2>` das leituras e, na `observacao`, "divergência decidida por <nome que a pessoa disse> em AAAA-MM-DD". Registro com `resultado = decidida`.

### Passo 10. Aprender
Pergunte: "O que causou a diferença pode voltar a acontecer?". Exemplos que viram regra: "manutenção anunciada nunca empurra prazo; só certidão", "ciência tácita em feriado: sempre as duas leituras para a advogada". Com o ok, grave em `aprendizados-controladoria.md` (`../../docs/aprender-com-o-uso.md`). Correção que pede dispensar a segunda leitura ("esse tipo de prazo não precisa") não vira regra: explique a regra fixa 3.

### Modo treino
A dupla conferência de `../../docs/casos-ficticios.md`, com o calendário e as regras de treino (`../calendario-forense/assets/`), gravando em `escritorio/07-operacao/_treino/controladoria/`:

| Linha | Primeira leitura (estagiária) | Segunda leitura (advogada) | Contas | Tem que sair |
|---|---|---|---|---|
| 1 · Otávio | recurso inominado, 10 dias, tabela, juizado federal, sem dobro | a mesma | 2026-04-30 e 2026-04-30 | `conferido`, registro `bateu` |
| 4 · Renata | custas, 5 dias pelo ato, cível, sem dobro, contou 2026-04-27 pela manutenção | custas, 5 dias, cível, sem dobro, contou 2026-04-24 | 2026-04-24 e 2026-04-24 | Fica `sugerido`, divergência na fila e no resumo com 2026-04-24 até a decisão (nada na agenda), registro `divergiu` |

No treino, os nomes são os papéis do Escritório Modelo ("estagiária (treino)", "advogada (treino)"), porque não há pessoa real conferindo.

### Modo adaptar
1. Leia `nicho.md`, a tabela de prazos por ato e os aprendizados.
2. Para os atos mais comuns do nicho, proponha uma pergunta a mais na leitura cega quando o ato costuma confundir (por exemplo, "o prazo é para a parte ou para o perito?"; "a intimação é da parte autora ou do INSS?").
3. Marque `[NOVO]` e grave na linha da habilidade em `aprendizados-controladoria.md`, com o ok.

## 4. Formato da saída

```
DUPLA CONFERÊNCIA · PZ-2026-0003 · C-2026-0005 · Renata
Ato: "[trecho literal]"
                     Primeira (estagiária)   Segunda (advogada)   Sugestão da IA
O que pede           custas complementares   custas               recolher custas
Dias e fonte         5, o ato                5, o ato             5, o ato
Rito e dobro         cível, não              cível, não           civel, nao
Data contada         2026-04-27              2026-04-24           2026-04-24
Conta 1 · conta 2    2026-04-24 · 2026-04-24 (AS DUAS CONTAS BATEM)
Resultado: NÃO BATEU. A primeira leitura empurrou pela manutenção sem certidão.
Vale 2026-04-24 (a mais cedo) até a decisão. O prazo continua sugerido.
Registro: conferencias/2026-04-14.md · Fila: divergência no item 03-C-2026-0005-prazo.md
```

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| `status`, `conferido_por`, `conferido_em`, correções e `observacao` | `escritorio/07-operacao/controladoria/prazos.csv` |
| Leituras, divergência e `status: aprovado` | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-prazo.md` |
| Registro do dia | `escritorio/07-operacao/controladoria/conferencias/AAAA-MM-DD.md` (modelo em `assets/modelo-do-registro.md`) |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: as leituras e o resultado saem no chat; a linha do `prazos.csv` e a do registro vão em bloco para colar na planilha. A segunda leitura, nesse caso, é numa conversa nova.

## 6. Solo e equipe

**Solo:** a segunda leitura é sua, em outro turno, numa conversa nova, antes da data de segurança. O que pega quem confere sozinho é a pressa: faça a primeira de manhã, quando chega a publicação, e a segunda depois do almoço, sem abrir a primeira.

**Equipe:** a estagiária faz a primeira leitura; quem está em `quem_confere` faz a segunda. Quem confere não é quem calculou, sempre que der. Divergência não é falha de ninguém: é a conferência funcionando. Quem decide a divergência está na ficha ou é a advogada do caso.

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Segunda leitura que só confirma a primeira | Erro da primeira vira prazo | Leitura cega: só o trecho, antes de qualquer resposta |
| Nome em `conferido_por` sem a pessoa dizer | Conferência que não aconteceu aparece como feita | Regra fixa 1 |
| Prazo agendado com leituras diferentes | Data errada na agenda | Regra fixa 3; fica `sugerido` |
| Divergência resolvida pela data mais tarde | Prazo perdido | Regra fixa 4 |
| Conferência feita na mesma hora pela mesma pessoa | Duas leituras com o mesmo cansaço | Segundo turno, conversa nova |
| Correção da sugestão da IA que se perde | O mesmo erro volta | Registro com `sugestao_ia` e `vencimento_final`, lido pela `auditoria-de-prazos` |

## 8. Próximo passo

- Conferido: `agenda-de-prazos` (se instalada; sem ela, o texto do compromisso para a pessoa lançar).
- Providência do ato ainda não decidida: `encaminhar-providencia` (se instalada; sem ela, o pedido em texto para copiar).
- Muitos prazos para conferir: `prazos-em-lote` (se instalada).
- Todo mês: `auditoria-de-prazos` (se instalada) conta as divergências e as correções.

## Referências desta habilidade

- `assets/modelo-do-registro.md`: o formato de `conferencias/AAAA-MM-DD.md`. Use no passo 7, 8 e 9.
- `../calcular-prazo/scripts/calcular_prazo.py`: as duas contas independentes (`--duplo`). Use no passo 5.
- `../calendario-forense/assets/calendario-de-treino.md` e `regras-de-treino.md`: o material do modo treino.
