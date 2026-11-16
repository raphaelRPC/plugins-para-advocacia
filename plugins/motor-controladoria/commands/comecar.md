---
description: Liga a controladoria do escritório em cerca de 15 minutos. 8 perguntas para a ficha mínima e um resultado na tela, um lote de dez publicações de treino triadas e com os prazos contados, cada um com uma armadilha (feriado local, manutenção sem certidão, prazo da outra parte, publicação duplicada, ciência tácita). Depois, o calendário dos tribunais e a validação da tabela de regras.
---

# /motor-controladoria:comecar

Você vai colocar a controladoria do escritório para rodar no Claude. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md`, `${CLAUDE_PLUGIN_ROOT}/docs/contagem.md` e `${CLAUDE_PLUGIN_ROOT}/docs/prazos.md`: uma pergunta por vez, nada inventado, nenhum prazo agendado sem a dupla conferência de uma pessoa.

Meta: 8 perguntas sobre o escritório e um resultado visível. Criar a pasta, o ok da ficha e a escolha do próximo passo não contam como pergunta.

## 1. Abertura (duas frases)

"Este plugin capta as publicações, liga cada uma ao caso e faz a conta do prazo com o calendário de cada tribunal, mostrando cada passo. Quem confirma o prazo é sempre uma pessoa, e eu vou te mostrar isso num lote de treino com dez publicações."

## 2. A pasta

1. Procure `escritorio/04-base/comum/`.
   - **`ficha-da-controladoria.md` existe:** não recomece. Mostre quantos campos estão preenchidos e ofereça: completar a ficha (`/motor-controladoria:ficha`), montar os calendários e validar a tabela de regras (`calendario-forense`), captar as publicações de hoje (`captar-publicacoes`) ou ligar o ciclo (`rotina-da-controladoria`).
   - **Só `ficha-do-escritorio.md` existe** (outro plugin motor preencheu): leia e pule a pergunta 1.
   - **Nada existe:** pergunte se pode criar `escritorio/` aqui.
2. Crie só o que o plugin usa (`${CLAUDE_PLUGIN_ROOT}/docs/pasta.md`). Se já existir `escritorio/CLAUDE.md`, acrescente só o bloco "Controladoria" de `pasta.md`.

## 3. As perguntas (uma de cada vez)

Ficha do escritório:
1. "Nome do escritório, cidade e as áreas em que vocês atuam?"

Ficha da controladoria (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-da-controladoria-modelo.md`):
2. "Quem cuida dos prazos hoje, quem faz a segunda conferência e quem decide o que fazer com cada publicação? Se você trabalha sozinho, as três são você, e a segunda conferência é feita em outro turno." (grava `responsavel_controladoria`, `quem_confere` e `quem_decide_providencia`)
3. "Quais OABs o escritório acompanha? Número e estado de cada advogado." (`oabs_monitoradas`)
4. "De onde vêm as publicações hoje: DJEN, e-mail do tribunal, o sistema jurídico, outra planilha?" (`fontes_de_publicacao`)
5. "Em que tribunais e cidades os processos de vocês tramitam?" (`tribunais` e `cidades_dos_juizos`)
6. "Que painéis de sistema alguém abre todo dia com senha ou certificado? PJe, eproc, Domicílio Judicial Eletrônico..." (`paineis_dos_sistemas`)
7. "Quantos dias úteis antes do fatal vocês querem o prazo na agenda? Se não tiver um número, eu sugiro 2." (`dias_de_seguranca`)
8. "Onde fica a agenda de prazos: Google, Outlook, o sistema, uma planilha?" (`onde_fica_a_agenda`)

Todo o resto fica `[A PREENCHER]`. Mostre as fichas, peça ok e grave. Avise em uma linha: "A tabela de regras de contagem vem marcada para conferir. Antes do primeiro prazo real, ela precisa ser validada por quem responde pela controladoria (`calendario-forense`)."

## 4. O resultado: o lote de treino

"Agora o lote de treino." Use o lote de `${CLAUDE_PLUGIN_ROOT}/docs/casos-ficticios.md`, o calendário de treino de `${CLAUDE_PLUGIN_ROOT}/skills/calendario-forense/assets/calendario-de-treino.md` e a tabela de prazos por ato de treino. Tudo grava em `escritorio/07-operacao/_treino/controladoria/`.

1. Rode a `captar-publicacoes` no modo treino (importar o lote).
2. Rode a `triar-publicacoes` nas dez.
3. Rode a `calcular-prazo` nas que pedem prazo.
4. Mostre uma tabela só, na ordem do que vence primeiro: caso, o que o ato pede (com o trecho literal), vencimento, data de segurança, a armadilha que a conta pegou. Embaixo, as que não geraram prazo e por quê (prazo da outra parte, duplicada, sem caso).
5. Diga em uma frase: "Todos estão como `sugerido`. Nenhum vai para a agenda antes da dupla conferência." E mostre, com a linha 1, como a dupla conferência funciona (`dupla-conferencia`, uma pergunta de cada lado).

Diga, sem perguntar: "Se tiver uma armadilha de prazo que já pegou vocês e que eu não procurei, me conte quando quiser: ela vira um aprendizado." (`${CLAUDE_PLUGIN_ROOT}/docs/aprender-com-o-uso.md`).

## 5. Fechamento (quatro linhas)

- Pronto: ficha mínima, a triagem e a conta funcionando no treino.
- Faltam `[N]` campos `[A PREENCHER]`; o primeiro que vai fazer falta é `[CAMPO]`, na habilidade `[HABILIDADE]`.
- Próximos passos, escolha um: os calendários dos tribunais e a validação da tabela de regras (`calendario-forense`, antes do primeiro prazo real); a primeira captação real (`captar-publicacoes`); o ciclo diário rodando (`rotina-da-controladoria`).
- `/motor-controladoria:status` mostra os prazos a qualquer hora.
