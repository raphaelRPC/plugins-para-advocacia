---
name: paineis-dos-sistemas
description: O roteiro diário dos painéis que só uma pessoa abre, com a própria senha ou certificado (PJe, eproc, e-SAJ, Projudi, Domicílio Judicial Eletrônico), e o registro do que ela viu. Monta com a pessoa o roteiro (qual sistema, quem olha, quando, o que olhar, quem substitui), gera o registro do dia em branco, confere o registro preenchido (sistema que ninguém olhou, intimação sem trecho, sem data de envio ou sem a situação da ciência) e aponta a ciência tácita prevista que vence em até 2 dias úteis. O registro entra na captação como qualquer outra fonte. A IA nunca acessa painel, nunca usa senha, certificado ou token. Use quando a pessoa disser "monta o roteiro dos painéis", "olhei o PJe, registra", "tem intimação sem ciência no portal". Não use para buscar no DJEN (use captar-publicacoes) nem para contar o prazo da intimação (use calcular-prazo).
---

# Painéis dos sistemas

> O que está atrás de senha chega à controladoria pelo registro de quem olhou, com a data de envio de cada intimação e a ciência à vista.

Regras: `../../docs/regras.md`. A ciência tácita, o Domicílio Judicial Eletrônico e a indisponibilidade: `../../docs/contagem.md`. O caminho da publicação: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 8h40. A estagiária abre o PJe do TRT3 com o certificado dela e vê uma intimação do processo do Paulo, enviada em 2026-04-06, ainda sem ciência: "Manifeste-se sobre os documentos juntados, em 5 dias". Ela não abre: anota a data de envio, a situação e o trecho no registro do dia. O registro mostra que a ciência tácita cai em 2026-04-16, daqui a dois dias, e a decisão de abrir agora ou esperar vai para a advogada.

**Regras fixas desta habilidade:**
1. A IA nunca acessa painel de tribunal e nunca recebe senha, certificado digital, token ou código de acesso, nem na conversa nem em arquivo. Se alguém colar uma senha, a habilidade avisa, não repete e pede para trocar a senha.
2. A ciência tácita é decisão da pessoa. Abrir ou esperar, e quando, é dela; a habilidade mostra a data prevista e a dúvida, nunca decide.
3. Abrir a intimação pode dar ciência `[CONFERIR]` como cada sistema registra. Quem olha registra sem abrir, a não ser que a pessoa responsável mande abrir; se abriu, registra a data e a hora da abertura.
4. Sem trecho, sem data de envio ou sem a situação da ciência, a intimação volta para quem olhou. Registro incompleto não vira "nada novo".
5. Painel do roteiro que ninguém registrou no dia é aviso, para a pessoa.

## 1. Quando usar

**Use quando:**
- O escritório vai montar o roteiro dos painéis (modo "roteiro").
- Começa o dia e a pessoa vai olhar os painéis: a habilidade dá o registro em branco (modo "registro do dia").
- A pessoa olhou e quer registrar ou conferir o que viu (modo "conferir").
- O `agente-de-controladoria` roda o ciclo e precisa saber se os painéis foram registrados (modo "no ciclo").
- Alguém vai sair de férias e outra pessoa assume os painéis (modo "roteiro", campo substituto).
- A pessoa quer treinar com o registro de treino (modo "treino").
- A `adaptar-controladoria` (se instalada) pede os sistemas e as regras do escritório (modo "adaptar").

**Não use quando:**
- O pedido é a busca no DJEN, que é pública: `captar-publicacoes`.
- O pedido é a conta do prazo da intimação: `calcular-prazo` (`--envio-portal` para a ciência tácita, `--ciencia` para a data da abertura, `--domicilio` para o Domicílio Judicial Eletrônico).
- O pedido é registrar indisponibilidade certificada do sistema: `calendario-forense`.
- O pedido é o plano de quem cobre os prazos nas férias: `cobertura-de-ausencia` (se instalada; sem ela, o substituto do roteiro cobre só os painéis).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-controladoria.md`), em especial os da `paineis-dos-sistemas` (sistema que costuma cair, painel que mostra a data de outro jeito).
3. **Veja o roteiro** (`escritorio/04-base/controladoria/paineis.md`) e o registro de hoje (`escritorio/07-operacao/controladoria/paineis/AAAA-MM-DD.md`), se existirem.
4. **Veja a tabela de regras** (`escritorio/04-base/controladoria/regras-de-contagem.md`), linha `intimacao-portal`: o prazo de ciência em dias corridos vem dela.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `paineis_dos_sistemas` |
| Melhora | K: `responsavel_controladoria` |

`paineis_dos_sistemas` diz quais painéis alguém abre com senha ou certificado. Sem ele, pergunte: "Que painéis de sistema alguém abre todo dia com senha ou certificado? PJe, eproc, e-SAJ, Projudi, Domicílio Judicial Eletrônico..." e ofereça gravar. `responsavel_controladoria` é quem olha, se o roteiro não disser outra pessoa.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Roteiro | Primeira vez, ou mudou sistema ou pessoa | Ficha e conversa | `04-base/controladoria/paineis.md`, com o ok |
| Registro do dia | Antes de olhar | O roteiro | O registro em branco, com os sistemas do roteiro |
| Conferir | Depois de olhar | O registro preenchido | O que falta, a ciência tácita prevista, PESSOA AGORA |
| No ciclo | O agente pede | O roteiro e o registro do dia | Lista para o resumo e avisos. Não mostra nada |
| Treino | Pedido de treino | `assets/roteiro-de-treino.md` e `assets/painel-de-treino.md` | A conferência do registro de treino |
| Adaptar | A `adaptar-controladoria` chama | Ficha e nicho | Roteiro e regras do escritório, para aprovar |

### Passo 1. O roteiro (uma vez)
Comece de `assets/roteiro-modelo.md`. Pergunte, um painel de cada vez:
1. "Qual sistema e de qual tribunal?" (PJe do TRT3, eproc do TRF4, e-SAJ do TJSP, Projudi, Domicílio Judicial Eletrônico).
2. "Quem olha, com a própria senha ou certificado?"
3. "Em que dias e horários?" (pelo menos uma vez por dia útil; no começo do expediente é o mais comum).
4. "O que essa pessoa procura lá?" (intimações sem ciência com a data de envio, pautas, perícias, manutenção anunciada).
5. "Quem olha quando ela falta?"
Mostre o roteiro e pergunte: "Posso gravar?". Com o ok, grave em `escritorio/04-base/controladoria/paineis.md`, com a tabela `sistema | tribunal | quem_olha | quando | o_que_olhar | substituto`.

### Passo 2. O registro do dia em branco

```
python3 "<pasta desta habilidade>/scripts/conferir_painel.py" modelo \
  --roteiro escritorio/04-base/controladoria/paineis.md --data AAAA-MM-DD --quem <função>
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/paineis-dos-sistemas`. Grave a saída em `escritorio/07-operacao/controladoria/paineis/AAAA-MM-DD.md` e diga à pessoa o que preencher (seção 4). Quem não usa pasta copia o bloco, preenche e cola de volta na conversa.

### Passo 3. A pessoa olha os painéis
A IA não acompanha a tela. A pessoa abre cada sistema, olha, e preenche no registro: a situação de cada sistema (`olhado`, `nao-olhado`, `fora-do-ar`), e uma linha por intimação ou comunicação nova, com o processo, a data de envio, a situação da ciência (`sem-ciencia`, `aberta`, `tacita`), a data da abertura se abriu, o prazo que o painel mostra (se mostra) e o trecho do ato copiado como está.

### Passo 4. Conferir o registro

```
python3 "<pasta desta habilidade>/scripts/conferir_painel.py" conferir \
  escritorio/07-operacao/controladoria/paineis/AAAA-MM-DD.md \
  --roteiro escritorio/04-base/controladoria/paineis.md \
  --regras escritorio/04-base/controladoria/regras-de-contagem.md --hoje AAAA-MM-DD
```

O script aponta: sistema do roteiro que não foi registrado; sistema fora do ar (com o lembrete de guardar a certidão de indisponibilidade, se o tribunal publicar, para a `calendario-forense`); intimação sem trecho, sem data de envio ou sem situação; aberta sem a data da abertura; e a ciência tácita prevista de cada intimação `sem-ciencia` (envio mais o prazo de ciência da tabela, em dias corridos), com PESSOA AGORA para a que cai em até 2 dias úteis. A data que vale para o prazo é a da `calcular-prazo`, com o calendário do tribunal: se a ciência cair em dia sem expediente, ela mostra as duas leituras e fica com a mais cedo.

### Passo 5. A decisão da ciência
Para cada intimação com ciência tácita perto, pergunte à pessoa responsável: "A intimação do processo [número] foi enviada em [data] e a ciência tácita prevista é [data]. Vocês abrem antes ou esperam?". Grave a resposta no registro, em "O que ficou para decidir", com o nome de quem decidiu, só se a pessoa disser na conversa. Se abrirem, a linha passa a `aberta`, com a data da abertura, e a conta muda.

### Passo 6. Levar para a captação
Ofereça: "Levo o registro para a captação?" (`captar-publicacoes`, que importa o registro como fonte `painel`, uma linha por intimação). Depois, a `triar-publicacoes` tria como prazo do escritório e monta os dados para a conta.

### Passo 7. Aprender
Pergunte: "Algum painel que mostra as coisas de outro jeito, ou um cuidado que vocês têm e eu não pedi?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md`. Pedido que fere uma regra fixa ("eu te passo a senha e você olha") não entra: explique que senha, certificado e token nunca passam pela IA e proponha "o registro de cinco minutos por sistema".

### Modo no ciclo
1. O agente pergunta se os painéis de hoje foram registrados. Não pergunte nada e não mostre nada.
2. Sem registro do dia: devolva "painel não registrado" com a lista do roteiro, que o agente põe como `item: aviso` (`NN-aviso-painel.md`) e em PESSOA AGORA se houver intimação sem ciência registrada ontem.
3. Com registro: rode o passo 4 e devolva ao agente o que falta corrigir, os sistemas não olhados e as ciências tácitas em até 2 dias úteis (PESSOA AGORA). A captação do registro é da `captar-publicacoes`, no mesmo ciclo.

### Modo treino
O roteiro do Escritório Modelo (`assets/roteiro-de-treino.md`: PJe do TRT3 e do TJMG, e o sistema do JEF) e o registro que a estagiária fez em 2026-04-14 (`assets/painel-de-treino.md`, a linha 10 do lote de `casos-ficticios.md`):

```
python3 "<pasta desta habilidade>/scripts/conferir_painel.py" conferir \
  "<pasta desta habilidade>/assets/painel-de-treino.md" \
  --roteiro "<pasta desta habilidade>/assets/roteiro-de-treino.md" \
  --regras "<pasta da calendario-forense>/assets/regras-de-treino.md" --hoje 2026-04-14
```

O teste passa quando: os três sistemas aparecem olhados; a intimação do Paulo (TRT3, enviada em 2026-04-06, sem ciência) sai em PESSOA AGORA com a ciência tácita prevista em 2026-04-16; nada vai para "corrigir". Na `calcular-prazo`, a conta pela data mais cedo dá início em 2026-04-17, vencimento em 2026-04-24 e segurança em 2026-04-22, com a dúvida da ciência em dia sem expediente (o feriado de treino) para a pessoa.

### Modo adaptar
1. Leia a ficha, `nicho.md` e o roteiro, se existir.
2. Proponha: os sistemas de cada tribunal da ficha, os horários que cabem na rotina do escritório, o que olhar em cada sistema para o nicho (por exemplo, perícias marcadas no JEF para o previdenciário), e as regras próprias do escritório para abrir intimação.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "Falta algum painel que alguém olha e não está aqui?".
4. Com o ok, grave no roteiro (`04-base/controladoria/paineis.md`).

## 4. O registro do dia

Formato de `07-operacao/controladoria/paineis/AAAA-MM-DD.md` (é este que a `captar-publicacoes` lê):

```markdown
---
documento: Registro dos painéis
data: AAAA-MM-DD
quem_registrou: [função]
treino: nao
---

# Painéis de AAAA-MM-DD

## Sistemas olhados

| sistema | tribunal | quem | hora | situacao | observacao |
|---|---|---|---|---|---|

## Intimações e comunicações vistas

| sistema | tribunal | orgao | processo | enviada_em | ciencia | aberta_em | prazo_no_painel | tipo_ato | trecho |
|---|---|---|---|---|---|---|---|---|---|

## O que ficou para decidir

- [a ciência a abrir ou esperar, o sistema fora do ar, quem decidiu e quando]
```

| Coluna | O que vai |
|---|---|
| `situacao` | `olhado`, `nao-olhado` ou `fora-do-ar` |
| `enviada_em` | AAAA-MM-DD do envio da intimação no portal |
| `ciencia` | `sem-ciencia`, `aberta` ou `tacita` |
| `aberta_em` | AAAA-MM-DD HH:MM da abertura, quando abriu |
| `prazo_no_painel` | O que o painel mostra como prazo, se mostra. Serve para conferir, nunca como conta |
| `trecho` | O texto do ato, copiado como está |

Domicílio Judicial Eletrônico: a ciência tem regra própria (`domicilio-eletronico`, em `contagem.md`) e não é calculada aqui. A pessoa registra a data da ciência que o painel mostra em `aberta_em`, e a conta parte dela. Nunca entram no registro: senha, certificado, token, código de acesso, print da tela de login.

## 5. Formato da saída

```
REGISTRO DOS PAINÉIS · AAAA-MM-DD · conferido em AAAA-MM-DD
Sistemas registrados: N · intimações registradas: N
PESSOA AGORA
  - [sistema não registrado | fora do ar | ciência tácita prevista em até 2 dias úteis]
CIÊNCIA TÁCITA PREVISTA: [data · intimação · enviada em]
CORRIGIR NO REGISTRO: [sem trecho, sem envio, sem situação, aberta sem data]
Próximo passo: captar-publicacoes com o registro
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| O roteiro dos painéis | `escritorio/04-base/controladoria/paineis.md` |
| O registro de cada dia | `escritorio/07-operacao/controladoria/paineis/AAAA-MM-DD.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/paineis/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

O roteiro não tem dado de cliente e pode ir para o Projeto no Claude. O registro tem número de processo: fica em `07-operacao/`. `publicacoes.csv` e `prazos.csv` não mudam aqui; o registro entra pela `captar-publicacoes`. Sem pasta aberta: o registro em branco sai num bloco, a pessoa preenche e cola de volta, e a conferência sai no chat.

## 7. Solo e equipe

**Solo:** o roteiro é curto, mas o registro vale do mesmo jeito: cinco minutos por sistema, toda manhã, com a data de envio anotada. A intimação de portal sem ciência é a que mais vence sem ninguém perceber.

**Equipe:** quem olha é quem tem o certificado ou o acesso; quem decide abrir ou esperar é a advogada responsável. Cada pessoa usa a própria senha e o próprio certificado, nunca o de outra. Nas férias, o substituto do roteiro assume no primeiro dia, e o registro diz quem olhou.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Senha do PJe colada na conversa | Acesso exposto | Regra fixa 1: nunca entra; troca de senha |
| Intimação aberta só para "dar uma olhada" | Ciência dada sem querer, prazo começa | Regra fixa 3: registrar sem abrir |
| Data de envio não anotada | Ciência tácita sem conta | Coluna `enviada_em` obrigatória |
| Ciência tácita decidida pela IA | Prazo contado do dia errado | Regra fixa 2: a pessoa decide |
| Painel que ninguém olhou contado como "nada novo" | Intimação vencendo no escuro | Regra fixa 5: aviso no resumo |
| Prazo do painel usado como conta | Erro do sistema vira erro do escritório | `prazo_no_painel` só confere |

## 9. Próximo passo

- O registro preenchido: `captar-publicacoes`, que importa como fonte `painel`.
- A conta da intimação: `calcular-prazo`, com `--envio-portal`, `--ciencia` ou `--domicilio`.
- Sistema fora do ar com certidão: `calendario-forense` registra a indisponibilidade certificada.
- Férias de quem olha: `cobertura-de-ausencia` (se instalada; sem ela, o substituto do roteiro).

## Referências desta habilidade

- `scripts/conferir_painel.py`: `modelo` (o registro do dia em branco, a partir do roteiro) e `conferir` (o que falta no registro e a ciência tácita prevista). Rode nos passos 2 e 4, no ciclo e no treino.
- `assets/roteiro-modelo.md`: o roteiro em branco, para o passo 1.
- `assets/roteiro-de-treino.md`: o roteiro do Escritório Modelo. Use no modo treino.
- `assets/painel-de-treino.md`: o registro de 2026-04-14 do Escritório Modelo (a linha 10 do lote de treino). Use no modo treino e como exemplo do formato.
