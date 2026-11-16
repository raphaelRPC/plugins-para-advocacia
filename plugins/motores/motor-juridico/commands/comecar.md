---
description: Liga a produção jurídica do escritório em cerca de 15 minutos. 8 perguntas para a ficha mínima e um resultado na tela, a conferência de uma minuta de treino com erros escondidos (citação inventada, nome de outro cliente, data divergente). Depois, as peças boas do escritório viram habilidades próprias.
---

# /motor-juridico:comecar

Você vai colocar a produção jurídica do escritório para rodar no Claude. Siga `${CLAUDE_PLUGIN_ROOT}/docs/regras.md` e `${CLAUDE_PLUGIN_ROOT}/docs/citacoes.md`: uma pergunta por vez, nada inventado, nenhuma citação sem conferência.

Meta: 8 perguntas sobre o escritório e um resultado visível. Criar a pasta, o ok da ficha e a escolha do próximo passo não contam como pergunta.

## 1. Abertura (duas frases)

"As habilidades deste plugin montam o dossiê, minutam no padrão do escritório e conferem cada citação e cada dado antes de a peça chegar até você. Vou te fazer oito perguntas e a gente vê a conferência trabalhando numa minuta de treino."

## 2. A pasta

1. Procure `escritorio/04-base/comum/`.
   - **`ficha-juridica.md` existe:** não recomece. Mostre quantos campos estão preenchidos e ofereça: completar a ficha (`/motor-juridico:ficha`), transformar uma peça boa em habilidade (`peca-vira-habilidade`), trazer uma pesquisa do Jus IA para a base (`trazer-pesquisa`) ou ligar o ciclo (`rotina-juridica`).
   - **Só `ficha-do-escritorio.md` existe** (outro plugin motor preencheu): leia e pule as perguntas 1 e 2.
   - **Nada existe:** pergunte se pode criar `escritorio/` aqui.
2. Crie só o que o plugin usa (`${CLAUDE_PLUGIN_ROOT}/docs/pasta.md`). Se já existir `escritorio/CLAUDE.md`, acrescente só um bloco "Jurídico" com três linhas: ler as fichas e os aprendizados; toda citação marcada até ser conferida; tese, aprovação, assinatura e protocolo são do advogado.

## 3. As perguntas (uma de cada vez)

Ficha do escritório:
1. "Nome do escritório, cidade e as áreas em que vocês atuam?"
2. "Quem trabalha nas peças: quem faz a primeira minuta, quem revisa e quem assina?"

Ficha jurídica (modelo `${CLAUDE_PLUGIN_ROOT}/docs/ficha-juridica-modelo.md`):
3. "Quais são as peças que mais saem do escritório? Pode dizer as cinco principais."
4. "Onde ficam as peças boas de vocês, as que servem de modelo?"
5. "Em que tribunais e juízos os casos de vocês mais tramitam?"
6. "Como a peça precisa sair: fonte, citação em recuo, jeito de numerar os pedidos, o que vocês nunca escrevem?"
7. "Onde fica a lista de clientes e de partes contrárias de casos anteriores (sistema jurídico, planilha)? É dela que sai o aviso de conflito de interesses." (grava em `base_de_partes`; se não houver lista, grave "não há" e avise que o conflito vai ser conferido só com o que o advogado disser)
8. "Em que sistemas vocês protocolam?"

Todo o resto fica `[A PREENCHER]`. A pesquisa de jurisprudência já vem como Jus IA e a validade da conferência como 90 dias (muda em `/motor-juridico:ficha`). Mostre as fichas, peça ok e grave.

## 4. O resultado: a conferência de uma minuta de treino

"Agora a conferência trabalhando." Use o caso 1 de `${CLAUDE_PLUGIN_ROOT}/docs/casos-ficticios.md` e a minuta `${CLAUDE_PLUGIN_ROOT}/skills/conferir-peca/assets/minuta-com-erros.md`. Tudo grava em `escritorio/07-operacao/_treino/juridico/`.

1. Rode a `conferir-peca` na minuta.
2. Rode a `conferir-citacoes` na mesma minuta.
3. Mostre uma tabela só, com os achados em ordem de gravidade: o nome de outro cliente, a súmula que não existe, a data divergente, o valor da causa diferente, o pedido sem fundamento, o documento que não existe. Diga em uma frase quantos dos dez erros escondidos foram achados.

Diga, sem perguntar: "Se tiver um erro que vocês costumam pegar na revisão e que eu não procurei, me conte quando quiser: ele vira um aprendizado." (`${CLAUDE_PLUGIN_ROOT}/docs/aprender-com-o-uso.md`).

## 5. Fechamento (quatro linhas)

- Pronto: ficha mínima e a conferência funcionando.
- Faltam `[N]` campos `[A PREENCHER]`; o primeiro que vai fazer falta é `[CAMPO]`, na habilidade `[HABILIDADE]`.
- Próximos passos, escolha um: a peça que mais sai virando habilidade própria (`peca-vira-habilidade`, com 3 a 5 peças boas); a primeira pesquisa do Jus IA guardada na base (`trazer-pesquisa`); o ciclo diário rodando (`rotina-juridica`).
- `/motor-juridico:status` mostra a fila de peças a qualquer hora.
