---
name: acompanhar-valores
description: >
  Acompanha os valores judiciais do escritório (alvará, RPV, precatório e depósito judicial) em
  valores.csv, do pedido ao levantamento e ao repasse: a etapa, a data, o próximo passo e quem
  faz; por script, o que está parado (para conferir no portal do tribunal), o valor levantado sem
  repasse registrado, o prazo interno de hoje, o aviso ao cliente que falta e as publicações que
  falam de valor e ainda não têm linha. O aviso ao cliente vai pela experiência, com aprovação.
  Nunca calcula valor devido nem promete data de pagamento. Use quando disserem "saiu a RPV do
  Jorge", "como estão os alvarás", "o que tem para levantar", "o cliente quer saber quando cai o
  dinheiro". Não use para calcular valor (é da pessoa e do cálculo do processo) nem para
  prestação de contas (use encerramento-do-caso, do motor-experiencia).
---

# Acompanhar valores

> Todo valor que o processo manda pagar tem uma linha, uma etapa e alguém que confere. O cliente sabe o que aconteceu e o que vem depois, sem data prometida e sem conta feita pela IA.

Regras: `../../docs/regras.md`. Publicações e prazos: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela de campos em `../../docs/ficha-da-controladoria.md`. Fila e entrada da experiência: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Aprendizados e adaptação: `../../docs/aprender-com-o-uso.md` e `../../docs/adaptar-ao-escritorio.md`.

O Jorge está insatisfeito: acha que o processo parou. Na segunda, sai a publicação "Expeça-se a requisição de pequeno valor". É a melhor notícia do ano para ele, e quase ninguém percebe, porque não há prazo para contar. Com a linha em `valores.csv`, a RPV ganha etapa, data e quem confere no portal, e o aviso ao cliente vai para a experiência no mesmo dia, sem prometer quando o dinheiro cai.

**Regras fixas desta habilidade:**
1. Nunca calcula, atualiza nem confere valor devido. O registro não tem coluna de valor; o valor fica no documento do tribunal e no sistema do escritório.
2. Nunca promete nem estima data de pagamento, nem para o cliente nem no registro. "Parado há N dias" é lembrete para conferir o portal, nunca previsão.
3. Nada vai para o cliente sem uma pessoa aprovar. Notícia ruim (suspensão, cancelamento, impugnação) vai por ligação.
4. Levantar, repassar e prestar contas são da pessoa. Valor levantado sem repasse registrado sobe para PESSOA AGORA.
5. O portal do tribunal e o banco são abertos por uma pessoa, com a própria senha ou certificado; a IA nunca acessa.

## 1. Quando usar

**Use quando:**
- Uma publicação fala de RPV, precatório, alvará, depósito ou levantamento (modo nova linha).
- Alguém conferiu o portal e a etapa mudou (modo atualizar).
- A equipe quer a lista do que está parado, do que tem para levantar e do que falta avisar (modo lista, por script).
- O cliente pergunta "quando cai o dinheiro?" e alguém precisa responder sem prometer (modo cliente perguntou).

**Não use quando:**
- O pedido é calcular o valor, atualizar a conta ou conferir o cálculo do processo: é da pessoa e do cálculo do caso, fora deste plugin.
- O pedido é a prestação de contas ao cliente: `encerramento-do-caso`, do motor-experiencia (se instalado); sem ele, a pessoa faz pelo modelo do escritório.
- O ato pede prazo (impugnar cálculo, manifestar sobre a requisição): é prazo, pela `calcular-prazo` e pela dupla conferência; esta habilidade acompanha o valor, não o prazo.

## 2. Antes de começar

1. **Leia as fichas** (`escritorio/04-base/comum/ficha-do-escritorio.md`, `ficha-da-controladoria.md`), `nicho.md` se existir e `aprendizados-controladoria.md`.
2. **Confira se o escritório acompanha valores** (`acompanha_valores`). Se for "não", diga em uma linha que a habilidade fica desligada e pergunte se querem ligar.
3. **Ache o registro:** `escritorio/07-operacao/controladoria/valores.csv`. Sem ele, ofereça criar só com a linha de títulos da seção 4.
4. **Conta de IA.** O registro tem número de processo e nome curto do cliente. Em conta pessoal, só o treino.
5. **Sem ficha:** ofereça `/motor-controladoria:comecar`. Para seguir, pergunte só: "O escritório acompanha alvarás, RPV, precatórios ou depósitos judiciais?".

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `acompanha_valores` |
| Melhora | E: `areas` |

Pela área, a habilidade adapta exemplos e vocabulário (RPV e precatório no previdenciário contra o INSS; depósito e alvará no trabalhista e no cível). Também lê, se preenchido, E: `feriados_e_recessos` para o prazo interno. Campo vazio: pergunte aquele campo, uma vez, e ofereça gravar.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz |
|---|---|---|
| Nova linha | Publicação que fala de valor | Passos 1 a 4 |
| Atualizar | A etapa mudou no portal | Passo 5 |
| Lista | "O que está parado?", rotina semanal | Passo 6, por script |
| Cliente perguntou | "Quando cai?" | Passo 7 |
| No ciclo | O agente ou a rotina chama | O script com `--publicacoes`; linhas novas só como sugestão no resumo, em PARA DECIDIR; nada vai para cliente |
| Treino | Teste ou "é fictício" | Com `assets/valores-de-treino.csv`, grava em `_treino/controladoria/valores/` |
| Adaptar | A `adaptar-controladoria` chama | O caminho de cada tipo nos tribunais do escritório e os limites de "parado", com `[ALTERADO]` |

### Passo 1. Ler o ato
Mostre o trecho literal da publicação (por exemplo, "Expeça-se a requisição de pequeno valor em favor da parte autora") e pergunte: "Qual é o tipo e a etapa? Pelo trecho, parece [tipo] [etapa]." A sugestão vai marcada "sugestão"; quem diz é a pessoa.

### Passo 2. Ver se o ato pede prazo
Se o ato abre prazo (manifestar sobre o cálculo, impugnar), diga: "Este ato também tem prazo: vai para a calcular-prazo e a dupla conferência." O valor e o prazo são linhas diferentes.

### Passo 3. Abrir a linha
Com o ok, grave a linha em `valores.csv` (seção 4): `id` (V, o ano e um número), código, primeiro nome, processo, tribunal, tipo, etapa, `etapa_em`, `proximo_passo` (o que conferir e onde, em poucas palavras), `quem_faz`, `prazo_interno` (se alguém combinou uma data para conferir), `publicacao_id`, `cliente_avisado_em` vazio, `observacao` e `atualizado_em`. O caminho de cada tipo está em `references/etapas-dos-valores.md`, tudo `[CONFERIR]`.

### Passo 4. Avisar o cliente
Pergunte: "Avisamos o cliente agora? É notícia boa, neutra ou ruim?". Com o motor-experiencia instalado, grave o aviso na entrada da experiência, no formato de `references/etapas-dos-valores.md`, seção 4 (pela `encaminhar-providencia`, se instalada). A mensagem diz o que aconteceu, o que quer dizer, o que vem depois e o que depende do cliente; nunca data de pagamento, nunca valor calculado. Notícia ruim vira roteiro de ligação. Sem o motor-experiencia, mostre o texto para a pessoa enviar. Depois do envio, a pessoa grava a data em `cliente_avisado_em`.

### Passo 5. Atualizar a etapa
Quando a pessoa conferiu o portal ou o banco: "Em que etapa está, desde quando?". Mude `etapa`, `etapa_em`, `proximo_passo` e `atualizado_em`, e acrescente uma linha curta na `observacao`. Etapa nova que o cliente precisa saber (expedido, depositado, levantado, suspenso): volte ao passo 4.

### Passo 6. A lista por script
Rode com o caminho da pasta desta habilidade e o do registro. No plugin instalado, a pasta é `${CLAUDE_PLUGIN_ROOT}/skills/acompanhar-valores`:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/acompanhar-valores/scripts/valores.py" \
  "escritorio/07-operacao/controladoria/valores.csv" --data AAAA-MM-DD \
  --publicacoes "escritorio/07-operacao/controladoria/publicacoes.csv"
```

Outras opções: `--parado "expedido=30, depositado=10"` (dias corridos por etapa; padrão no topo do script), `--feriados` (o campo da ficha, como está), `--saida`, `--treino` (obrigatório para `_treino/`). O script mostra: PESSOA AGORA (prazo interno vencido, de hoje ou do próximo dia útil; levantado sem repasse além do limite; depositado sem levantamento além do limite; suspenso), aviso ao cliente pendente (etapa nova depois do último aviso), parados, a contagem por etapa, os próximos passos por quem faz, as publicações que falam de valor sem linha (sugestão) e o registro a corrigir. Lê csv de vírgula ou ponto e vírgula, com ou sem BOM, datas AAAA-MM-DD ou DD/MM/AAAA, tipo e etapa sem diferenciar maiúscula nem acento. Coluna de valor que alguém acrescentar é ignorada, com aviso. Sai com código 1 e "ERRO:" quando falta o arquivo ou coluna obrigatória, a data é inválida ou o registro é de treino sem `--treino`. Nunca diz que está tudo em dia sem ter lido linhas.

### Passo 7. O cliente perguntou "quando cai?"
Mostre a linha e responda à pessoa, para ela falar com o cliente: a etapa, desde quando, o que vem depois e onde se confere. Ofereça o rascunho pela experiência (`status-para-o-cliente`, do motor-experiencia, se instalado) com a frase-base: "O pagamento segue o calendário do tribunal, e nós avisamos assim que o valor estiver disponível." Nunca uma data, nem "deve sair em".

### Passo 8. Aprender
Pergunte: "Alguma etapa ou caminho que funciona diferente no tribunal de vocês?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Caminho que muda de vez vai para o modo adaptar.

## 4. O registro `valores.csv`

```
id,codigo_caso,cliente_curto,processo,tribunal,tipo,etapa,etapa_em,proximo_passo,quem_faz,prazo_interno,publicacao_id,cliente_avisado_em,observacao,atualizado_em
```

| Coluna | O que vai | Exemplo (treino) |
|---|---|---|
| `id` | V, o ano e um número sequencial | V-2026-0001 |
| `codigo_caso` | O código do cliente, o mesmo dos outros plugins | C-2025-0088 |
| `cliente_curto` | Primeiro nome ou iniciais | Jorge |
| `processo` | O número do processo | 0000909-99.2023.4.06.3800 |
| `tribunal` | Sigla | TRF6 |
| `tipo` | `alvara`, `rpv`, `precatorio`, `deposito-judicial` | rpv |
| `etapa` | `pedido`, `deferido`, `expedido`, `transmitido`, `depositado`, `levantado`, `repassado`, `suspenso`, `cancelado` | expedido |
| `etapa_em` | AAAA-MM-DD, a data da etapa atual | 2026-04-13 |
| `proximo_passo` | O que conferir ou fazer, e onde | conferir no portal do TRF6 a transmissão da requisição |
| `quem_faz` | Primeiro nome ou função | estagiária |
| `prazo_interno` | AAAA-MM-DD combinada para conferir, ou vazio | |
| `publicacao_id` | A publicação que abriu ou mudou a linha | PUB-2026-00009 |
| `cliente_avisado_em` | AAAA-MM-DD do último aviso enviado, depois do envio | |
| `observacao` | Uma linha por mudança, sem dado sensível | cliente insatisfeito: boa notícia pela experiência sem prometer data |
| `atualizado_em` | AAAA-MM-DD | 2026-04-14 |

Obrigatórias para o script: `id`, `codigo_caso`, `tipo`, `etapa`, `etapa_em`. Regras do registro: uma linha por valor; nada é apagado (o que deixou de existir vira `cancelado`, com o motivo); sem CPF, conta bancária ou valor; treino em `_treino/`.

## 5. Exemplo resolvido (treino)

Copie `assets/valores-de-treino.csv` para `escritorio/07-operacao/_treino/controladoria/valores/valores.csv`. É a linha 9 do lote de `casos-ficticios.md`: a RPV do Jorge (C-2025-0088), expedida em 2026-04-13. Rode em 2026-04-14:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/acompanhar-valores/scripts/valores.py" \
  "escritorio/07-operacao/_treino/controladoria/valores/valores.csv" --data 2026-04-14 --treino
```

O que tem que sair: nada em PESSOA AGORA; em "Aviso ao cliente pendente", o Jorge (RPV expedida em 2026-04-13, último aviso: nenhum); nada parado; o próximo passo da estagiária (conferir a transmissão no portal do TRF6). O rascunho da experiência para o Jorge, que está insatisfeito, é boa notícia e pede ligação: o que aconteceu (a requisição de pagamento foi expedida), o que quer dizer, o que vem depois (o tribunal paga no calendário dele) e que o escritório avisa quando o valor estiver disponível. Nenhuma data, nenhum valor.

Com o lote inteiro (`--publicacoes` apontando para as publicações de treino da `rotina-da-controladoria`) e o `valores.csv` só com a linha de títulos, a sugestão é a PUB-2026-00009 do Jorge: "abrir linha? tipo e etapa [A CONFIRMAR] pela pessoa". Nenhuma outra publicação do lote fala de valor.

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Registro de valores | `escritorio/07-operacao/controladoria/valores.csv`, com o ok |
| Aviso ao cliente | `escritorio/07-operacao/experiencia/entrada/AAAA-MM-DD-HHMM-controladoria.md` (motor-experiencia, se instalado); sem ele, no chat |
| Lista por script | No chat; no ciclo, uma linha em PARA DECIDIR do resumo (`07-operacao/controladoria/rotina/AAAA-MM-DD.md`) |
| Treino | `escritorio/07-operacao/_treino/controladoria/valores/` |
| Correções que viraram regra | `escritorio/04-base/comum/aprendizados-controladoria.md` |

Sem pasta aberta: a linha nova vem como tabela para colar na planilha, e o aviso como texto para a pessoa enviar.

## 7. Solo e equipe

**Solo:** a lista de valores roda junto com o resumo da semana. Os dois itens que mais importam são o levantado sem repasse (dinheiro do cliente com o escritório) e o aviso que ficou para depois.

**Equipe:** quem confere o portal (`quem_faz`) atualiza a etapa; quem decide levantar e repassar é o advogado responsável; quem fala com o cliente é quem a ficha do escritório diz. O financeiro do escritório, se existir, recebe a lista de levantados para a prestação de contas.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| RPV expedida sem ninguém acompanhar | Valor depositado esquecido, cliente sem notícia | Linha aberta pela publicação; parado vira lembrete |
| Data de pagamento prometida ao cliente | Cliente cobra uma data que o tribunal não deu | Regra fixa 2; frase-base sem data |
| Valor calculado pela IA na mensagem | Número errado vira expectativa e conflito | Sem coluna de valor; coluna acrescentada é ignorada |
| Valor levantado e não repassado | Problema ético e de confiança | PESSOA AGORA depois do limite |
| Boa notícia que não chega ao cliente insatisfeito | O cliente acha que nada aconteceu | Aviso pendente até `cliente_avisado_em` |
| Senha do portal ou do banco com a IA | Risco de segurança | Regra fixa 5: a pessoa abre e conta o que viu |

## 9. Próximo passo

- Aviso ao cliente: `status-para-o-cliente`, do motor-experiencia (se instalado), pela entrada da experiência.
- Ato que também abre prazo: `calcular-prazo` e `dupla-conferencia`.
- Valor repassado e caso no fim: `encerramento-do-caso`, do motor-experiencia (se instalado), para a prestação de contas.
- Lista no resumo de todo dia: `rotina-da-controladoria` (o ciclo pode chamar o script com `--publicacoes`).

## Referências desta habilidade

- `scripts/valores.py`: a lista por script (só biblioteca padrão). Rode no passo 6 e no ciclo.
- `assets/valores-de-treino.csv`: a RPV do Jorge, do lote de treino. Use na seção 5.
- `references/etapas-dos-valores.md`: as etapas, o caminho de cada tipo (`[CONFERIR]`), o que nunca vai ao cliente e o formato do aviso para a experiência. Leia nos passos 3 a 5.
