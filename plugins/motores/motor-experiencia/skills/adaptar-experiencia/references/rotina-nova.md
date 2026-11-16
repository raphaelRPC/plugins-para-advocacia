# Rotina nova vira habilidade

Leia no modo rotina nova. Caminho curto, para rotinas pequenas do suporte ao cliente. Quem usa o plugin `inicio-automacao` pode fazer o caminho completo (POP, teste, versão) pela `pop-para-skill` dele.

## 1. A entrevista (uma pergunta por vez)

1. "Que rotina é essa? Me conta a última vez que vocês fizeram."
2. "O que dispara? Um fato (contrato assinado, audiência marcada), uma data (toda sexta, dia 5) ou um pedido?"
3. "O que se faz, passo a passo? Quem faz cada passo?"
4. "Com que material? Uma mensagem, um roteiro, uma lista, uma ligação?"
5. "Quem aprova antes de chegar ao cliente?"
6. "O que nunca pode acontecer nessa rotina?" (exemplo: ligar para quem pediu para não receber; falar de decisão antes da advogada)
7. "Quando ela deve parar e chamar uma pessoa?"

Peça a cena concreta quando a resposta vier vaga. "Não sei" vira `[A DEFINIR]`, com a pergunta que resolve.

## 2. Escrever a rotina

Acrescente em `escritorio/04-base/comum/rotinas-do-escritorio.md` (crie com cabeçalho se não existir):

```markdown
## [NOME DA ROTINA]
- Dispara quando: [GATILHO]
- Quem é dono: [FUNÇÃO]
- Habilidade: 04-base/habilidades-do-escritorio/[nome]/SKILL.md
- No ciclo do agente: [SIM, COMO ITEM DA FILA | NÃO]

| Passo | O que se faz | Quem | S, A ou H |
|---|---|---|---|

- Nunca: [O QUE NUNCA PODE ACONTECER]
- Para e chama uma pessoa quando: [SINAL]
```

Todo passo que fala com cliente é A ou H. Na dúvida, a sigla mais humana.

## 3. Gerar a habilidade

1. Escolha o nome com o advogado: curto, verbo ou substantivo, minúsculas sem acento, hífen entre palavras (ex.: `ligacao-de-boas-vindas`).
2. Preencha `assets/modelo-habilidade-do-escritorio.md` e grave em `escritorio/04-base/habilidades-do-escritorio/<nome>/SKILL.md`.
3. Material longo (roteiro, modelo de mensagem) vai em `references/` ou `assets/` dentro da pasta da habilidade, e o SKILL.md diz quando ler.

## 4. Testar com três casos

| Caso | O que conferir |
|---|---|
| O comum | A rotina sai como o escritório faz |
| O com exceção | A exceção que o advogado citou é tratada |
| O que deve parar | A habilidade para e chama a pessoa, sem escrever nada ao cliente |

Rode os três no chat, mostre o resultado e ajuste. Grave os casos na seção 5 da habilidade (o que deve acontecer) e o resultado de cada rodada no registro dos testes, `escritorio/04-base/casos-de-teste/experiencia/<nome>-testes.md`, no formato de `assets/modelo-registro-dos-testes.md`. Na linha `Resultado:`, só `passou` ou `falhou (o que falhou)`; o texto do modelo deixado como está não conta como passou.

## 5. Empacotar

A partir da pasta da `adaptar-experiencia`:

```
python3 scripts/empacotar_habilidade.py escritorio/04-base/habilidades-do-escritorio/<nome> \
  --testes escritorio/04-base/casos-de-teste/experiencia/<nome>-testes.md
```

O script confere nome, tamanho dos caminhos, frontmatter, descrição, as seções obrigatórias, os arquivos citados e os três resultados do registro (só `Resultado: passou` conta), e gera `escritorio/04-base/habilidades-do-escritorio/<nome>.zip`. Para instalar: Personalizar > Habilidades > Enviar (conferir na configuração da conta).

## 6. Pôr no ciclo

Se o agente de suporte está em uso e a rotina tem gatilho que a carteira enxerga (contrato novo, compromisso, data), ofereça registrar na ficha da automação do ciclo (`05-automacoes/ciclo-da-experiencia/ficha.md`, seção "Rotinas próprias no ciclo"). Até o agente ler essa seção, a rotina roda a pedido ou à mão no ciclo.

## Exemplo: ligação de boas-vindas no dia seguinte

- Dispara quando: a boas-vindas foi enviada ontem (linha no histórico).
- Passos: a secretária liga no dia útil seguinte (H), pergunta se as mensagens chegaram e se ficou alguma dúvida, confirma o canal e quem mais pode receber informação; registra uma linha no histórico (S); atualiza `humor` na carteira pela leitura da ligação (H).
- Nunca: falar de estratégia ou de prazo de decisão na ligação; ligar para cliente de família sem confirmar o canal seguro.
- Para e chama a advogada quando: o cliente demonstra dúvida sobre o contrato, insatisfação ou situação de vulnerabilidade.
