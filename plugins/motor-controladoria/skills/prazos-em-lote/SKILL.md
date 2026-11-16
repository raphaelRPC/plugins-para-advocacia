---
name: prazos-em-lote
description: Faz a conta e a dupla conferência de um lote inteiro de prazos, linha por linha. O script de conta refaz cada prazo aberto de prazos.csv com as duas contas independentes e compara com o registro; uma planilha de leitura cega vai para duas pessoas, e outro script compara as duas leituras. Só vira conferido a linha em que as duas leituras, as duas contas e o registro batem, com os nomes que as pessoas disserem; as linhas que divergem ficam separadas, com a data mais cedo. Serve também para recontar tudo depois de uma indisponibilidade certificada ou de mudança no calendário. Use quando disserem "confere os prazos da semana de uma vez", "recalcula todos os prazos do TJMG", "saiu portaria nova, refaz as contas", "temos 80 prazos para conferir". Não use para um prazo só (use calcular-prazo e dupla-conferencia).
---

# Prazos em lote

> A conta e a conferência de muitos prazos de uma vez, sem amostra: cada linha passa pelas duas contas e pelas duas leituras, e o que diverge sai separado.

Registros, status e a dupla conferência: `../../docs/prazos.md`. Regras de contagem: `../../docs/contagem.md`. Regras gerais: `../../docs/regras.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Segunda, 8h. O escritório voltou do recesso com 74 prazos sugeridos, e o TRT3 publicou na sexta uma portaria suspendendo os prazos de um dia. Conferir um por um levaria a manhã inteira. O lote refaz as 74 contas com o calendário novo, mostra as 6 que mudaram com a portaria, e a advogada e a estagiária preenchem cada uma a sua planilha de leitura, sem ver a da outra. Às 11h, 66 estão conferidos; as 8 que divergem estão na fila, cada uma com a data mais cedo.

**Regras fixas desta habilidade:**
1. Sem amostra: todo prazo do lote tem as duas contas e as duas leituras. O lote acelera o trabalho, não dispensa nenhuma conferência.
2. A IA nunca escreve um nome em `conferido_por`. Só registra os nomes que as próprias pessoas dizem, na conversa, que preencheram cada leitura.
3. Linha que diverge (entre as leituras, entre as contas ou com o registro) fica `sugerido`, separada, e vale a data mais cedo até a pessoa decidir.
4. O script de conta nunca muda status: com `--gravar`, só preenche data em branco e anota divergência na `observacao` de linhas `sugerido`, e guarda a cópia de antes.
5. Prazo com segurança ou fatal hoje ou amanhã sai do lote e vai para PESSOA AGORA, conferido primeiro, um por um.

## 1. Quando usar

**Use quando:**
- Há muitos prazos `sugerido` para conferir (volta de férias, segunda-feira, depois de um ciclo grande).
- O calendário mudou (portaria, suspensão, indisponibilidade certificada) e as contas abertas precisam ser refeitas.
- A tabela de regras foi validada ou mudou, e os prazos abertos precisam ser conferidos contra ela.
- A `triagem-em-massa` (se instalada) gerou muitos prazos de atos iguais: a triagem é por grupo, mas a conta e a conferência continuam uma por prazo.
- A `adaptar-controladoria` (se instalada) chamou no modo "adaptar".

**Não use quando:**
- É um prazo só: `calcular-prazo` e `dupla-conferencia`.
- O que falta é triar as publicações: `triar-publicacoes` ou `triagem-em-massa` (se instaladas).
- O prazo já está `cumprido`, `perdido` ou `cancelado`: o lote não mexe; a análise do mês é da `auditoria-de-prazos` (se instalada).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/`: `ficha-do-escritorio.md`, `ficha-da-controladoria.md` e `nicho.md`, se existir.
2. **Leia os aprendizados** (`aprendizados-controladoria.md`). Nenhum aprendizado troca a conferência linha por linha por amostra.
3. **Ache os registros:** `escritorio/07-operacao/controladoria/prazos.csv` e `publicacoes.csv`. Sem eles, não há lote: diga isso, sem "nada a apontar".
4. **Ache a base:** `04-base/controladoria/regras-de-contagem.md` e a pasta `calendario/`. Tribunal do lote sem calendário: as linhas dele saem "não contadas", com o motivo.
5. **Conta de IA:** prazo de cliente só em conta profissional ou de equipe. Em conta pessoal, só o treino.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `quem_confere`, `dias_de_seguranca` |
| Melhora | K: `regras_validadas_em` |

Sem `quem_confere`, pergunte: "Quem faz a segunda leitura deste lote?". Sem `dias_de_seguranca`, o script usa 2 dias úteis e avisa; pergunte uma vez e ofereça gravar. `regras_validadas_em` vazio: todo o lote sai com "regra ainda não validada pelo escritório", e vale dizer isso antes de começar.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Conferir o lote | Muitos `sugerido` | `prazos.csv`, `publicacoes.csv` | As contas, as duas leituras comparadas, os `conferido` e as separadas |
| Recontar | Calendário ou regra mudou | `prazos.csv` | As contas refeitas e as linhas que mudaram, para conferir de novo |
| Treino | "é teste" | O lote de treino | As contas do gabarito e a divergência da linha 4, em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | `nicho.md` | Como separar o lote do nicho (por tribunal, por ato, por responsável) |

No ciclo, esta habilidade não roda: o agente sugere e a conferência é das pessoas. O agente pode chamar só a conta do passo 2 para o resumo, sem `--gravar`.

### Passo 1. O lote
Pergunte: "Quais prazos entram no lote: todos os sugeridos, os de um tribunal, ou os de uma semana?". Monte a lista e tire do lote, antes de tudo, os de segurança ou fatal hoje ou amanhã: "Estes [N] vão primeiro, um por um, pela dupla-conferencia."

### Passo 2. As contas do lote
Rode o script da `calcular-prazo`:

```
python3 "<pasta da calcular-prazo>/scripts/calcular_prazo.py" \
  --csv escritorio/07-operacao/controladoria/prazos.csv \
  --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv \
  --calendario escritorio/04-base/controladoria/calendario/ \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md --seguranca 2 \
  --saida escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-contas.md
```

No Cowork e no Claude Code, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/calcular-prazo`. Para cada prazo aberto (`tipo = prazo`, status `sugerido`, `conferido` ou `agendado`), o script refaz as duas contas e compara com o registro. Como ele acha o ponto de partida de cada linha:

| A linha tem | O script parte de |
|---|---|
| `regra` com `intimacao-portal` | `disponibilizada_em` da publicação, como data de envio (ciência tácita) |
| `regra` com `publicacao-diario`, ou publicação de DJEN, e-mail, planilha ou sistema | `disponibilizada_em` da publicação |
| Nenhum dos dois (ciência informada, Domicílio Judicial Eletrônico) | `publicada_em` do prazo, como a data da ciência |

O tribunal vem da publicação; sem ela, do número do processo (sem conferir dígito verificador); sem os dois, a linha sai "não contada". `dias` é sempre o número antes de dobrar, e `em_dobro = sim` dobra. Código 2: há linha que diverge ou cujas contas não batem.

Sem a `calcular-prazo` instalada ou sem código: o lote vira uma lista, e cada prazo é contado à mão pela regra da `calcular-prazo`, um por vez.

### Passo 3. Mostrar as contas
Mostre o resumo (ok, diverge do registro, registro em branco, contas não batem, erro) e, em cima, as separadas, cada uma com o motivo. Prazo `conferido` ou `agendado` cuja conta mudou (por exemplo, com a portaria nova) vai para PESSOA AGORA se a data nova for mais cedo que a da agenda: "A agenda está com [data]; a conta nova dá [data mais cedo]."

### Passo 4. Preencher o que está em branco
Se há linhas `sugerido` com datas em branco, pergunte: "Posso preencher as datas em branco no prazos.csv?". Com o ok, rode o passo 2 com `--gravar`. O script guarda a cópia de antes em `07-operacao/controladoria/lotes/` e anota as divergências na `observacao`. Nenhum status muda.

### Passo 5. As planilhas de leitura cega
Gere a planilha da leitura:

```
python3 "<pasta desta habilidade>/scripts/comparar_leituras.py" modelo \
  --prazos escritorio/07-operacao/controladoria/prazos.csv \
  --publicacoes escritorio/07-operacao/controladoria/publicacoes.csv \
  --saida escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-leitura-1.csv
```

Rode de novo com `--saida ...-leitura-2.csv`. No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/prazos-em-lote`. A planilha não traz a sugestão da IA: só o prazo, o caso e o caminho do teor. Cada pessoa abre o teor de cada linha e preenche `o_que_pede`, `dias`, `fonte_dos_dias` (ato ou tabela), `rito`, `dobro` e, se contou, `data_contada`. Diga: "Cada uma preenche a sua, sem ver a outra e sem abrir a fila antes."

### Passo 6. Comparar as leituras
Com as duas planilhas prontas:

```
python3 "<pasta desta habilidade>/scripts/comparar_leituras.py" comparar \
  escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-leitura-1.csv \
  escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-leitura-2.csv \
  --prazos escritorio/07-operacao/controladoria/prazos.csv \
  --saida escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-leituras.md
```

| Situação | Quer dizer | Caminho |
|---|---|---|
| `bate` | As duas leituras iguais e iguais à sugestão | Segue para o passo 7 |
| `bate, corrige a IA` | As duas leituras iguais entre si e diferentes da sugestão | Sai do lote: a conta é refeita com os dados das leituras pela `dupla-conferencia` (passo 5 dela) |
| `confirmar` | Palavras diferentes para o que o ato pede, ou fonte diferente | As duas pessoas dizem se é o mesmo; sim, volta para `bate` |
| `diverge` | Dias, rito, dobro ou data contada diferentes, ou leitura em branco | Separada: fica `sugerido`, divergência na fila, data mais cedo |

### Passo 7. Conferido, linha por linha
Para as linhas `bate` em que a conta do passo 2 também deu `ok`, pergunte: "Quem preencheu a leitura 1, e quem preencheu a leitura 2?". Com os nomes que as pessoas disserem e o ok, em cada linha de `prazos.csv`: `status = conferido`, `conferido_por = <nome 1>; <nome 2>` (ou `<nome>; 2º turno`), `conferido_em` com a hora da segunda planilha, `atualizado_em`. No item da fila de cada uma: `status: aprovado`. Uma linha por prazo em `conferencias/AAAA-MM-DD.md`, no modelo da `dupla-conferencia` (`../dupla-conferencia/assets/modelo-do-registro.md`), com `resultado = bateu`.

### Passo 8. As separadas
Para cada linha separada: o item da fila ganha o bloco `divergencia:` com as duas leituras e as datas, e a linha `divergência: vale [data mais cedo] até a decisão` em `antes_de_enviar`. Registro com `resultado = divergiu`. Ofereça decidir agora, uma por uma, pela `dupla-conferencia` (passo 9 dela).

### Passo 9. Aprender
Pergunte: "Teve algum tipo de prazo que divergiu mais de uma vez neste lote?". Padrão repetido vira regra curta (por exemplo, "intimação do portal do TRT3: sempre conferir a data de envio no painel") e, com o ok, entra em `aprendizados-controladoria.md` (`../../docs/aprender-com-o-uso.md`).

### Modo treino
Com o material de `../../docs/casos-ficticios.md`, em `escritorio/07-operacao/_treino/controladoria/`:
1. Monte `prazos.csv` com as linhas 1, 3, 4, 8 e 10 do lote, como a `calcular-prazo` sugeriu, e `publicacoes.csv` com as publicações delas.
2. Rode o passo 2 com o calendário e as regras de treino (`../calendario-forense/assets/`) e `--hoje 2026-04-14`: as cinco contas batem com o gabarito (30/04, 24/04, 24/04, 11/05, 24/04).
3. Na leitura, a estagiária escreve `data_contada` 2026-04-27 na linha 4 e a advogada 2026-04-24: a linha 4 sai `diverge` e fica `sugerido`, com 2026-04-24 valendo até a decisão. As outras viram `conferido` com os papéis do treino.

### Modo adaptar
1. Leia `nicho.md`, a ficha e os aprendizados.
2. Proponha como cortar o lote do escritório (por tribunal, por responsável, por ato que se repete) e o melhor dia para o lote (por exemplo, segunda de manhã, depois do ciclo).
3. Marque `[NOVO]` e grave na linha da habilidade em `aprendizados-controladoria.md`, com o ok.

## 4. Formato da saída

```
LOTE DE PRAZOS · AAAA-MM-DD · N prazos
PESSOA AGORA: [prazos de hoje ou amanhã, fora do lote]
Contas: ok N · diverge do registro N · registro em branco N · contas não batem N · não contadas N
Leituras: bate N · corrige a IA N · confirmar N · diverge N
Conferidos agora: N (nomes que as pessoas disseram: [nome 1]; [nome 2])
Separadas: [id · caso · motivo · data que vale até a decisão]
Arquivos: lotes/AAAA-MM-DD-contas.md · lotes/AAAA-MM-DD-leituras.md · conferencias/AAAA-MM-DD.md
```

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Relatório das contas | `escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-contas.md` |
| Planilhas de leitura e comparação | `escritorio/07-operacao/controladoria/lotes/AAAA-MM-DD-leitura-1.csv`, `-leitura-2.csv`, `-leituras.md` |
| Cópia do registro antes do `--gravar` | `escritorio/07-operacao/controladoria/lotes/prazos-antes-do-lote-AAAA-MM-DD-HHMMSS.csv` |
| Datas em branco, `conferido`, nomes e `observacao` | `escritorio/07-operacao/controladoria/prazos.csv` |
| Divergências | Os itens `NN-<codigo>-prazo.md` da fila |
| Registro das conferências | `escritorio/07-operacao/controladoria/conferencias/AAAA-MM-DD.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |

Sem pasta aberta: o lote vira uma tabela no chat, as duas leituras são feitas em conversas separadas e as linhas vão em bloco para colar na planilha.

## 6. Solo e equipe

**Solo:** o lote ajuda na segunda-feira e na volta das férias. Preencha a leitura 1 de manhã e a 2 em outro turno, sem abrir a primeira. Se o lote passa de 30 prazos, divida em dois dias, sempre começando pelos que vencem primeiro.

**Equipe:** a estagiária roda as contas e gera as planilhas; ela e a advogada preenchem cada uma a sua. Quem decide as separadas está na ficha. O lote é bom para mostrar onde a equipe mais diverge: leve isso para a reunião do mês com a `auditoria-de-prazos` (se instalada).

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Conferir o lote por amostra | Um prazo errado passa no meio de cem certos | Regra fixa 1: todas as linhas |
| Planilha de leitura com a sugestão da IA | A leitura vira confirmação | `comparar_leituras.py modelo` não leva dias, datas nem providência |
| Recontar e sobrescrever o registro | Histórico perdido, data conferida trocada sem ninguém ver | `--gravar` só preenche branco, anota e guarda a cópia |
| Portaria nova sem recontar o que já está na agenda | Prazo agendado com data mais tarde que a real | Passo 3: conferido com data nova mais cedo vai para PESSOA AGORA |
| Lote que esconde o prazo de amanhã | Prazo urgente esperando a vez | Passo 1: hoje e amanhã saem do lote |
| Nomes preenchidos pela IA | Conferência que ninguém fez | Regra fixa 2 |

## 8. Próximo passo

- Separadas: `dupla-conferencia`, uma por uma (passo 9 dela).
- Conferidos: `agenda-de-prazos` (se instalada; sem ela, a lista de compromissos em texto para a pessoa lançar).
- Calendário que gerou divergência: `calendario-forense`.
- Fim do mês: `auditoria-de-prazos` (se instalada).

## Referências desta habilidade

- `scripts/comparar_leituras.py`: `modelo` gera a planilha da leitura cega (passo 5); `comparar` compara as duas leituras linha por linha (passo 6).
- `../calcular-prazo/scripts/calcular_prazo.py --csv`: as duas contas de cada prazo do lote (passos 2 e 4).
- `../dupla-conferencia/assets/modelo-do-registro.md`: o formato do registro das conferências (passo 7).
