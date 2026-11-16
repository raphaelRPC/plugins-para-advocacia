# Adaptar ao escritório: contexto, nicho e rotinas

Os plugins chegam com o método pronto e o conteúdo genérico. Um escritório de previdenciário rural e um de trabalhista patronal usam as mesmas habilidades, mas falam com clientes diferentes, recebem perguntas diferentes e têm rotinas diferentes. A adaptação acontece em quatro camadas, da mais rápida para a mais profunda.

| Camada | O que guarda | Onde fica | Quem escreve |
|---|---|---|---|
| 1. Fichas | Fatos e decisões: quem atende, horários, valores, prazos, tom | `04-base/comum/ficha-*.md` | O comando `comecar` (mínimo), o comando `ficha` (completo) e cada habilidade, na hora em que falta um campo |
| 2. Nicho | O jeito do cliente e do tipo de caso: vocabulário, dúvidas típicas, aflições, documentos, sazonalidade, cuidados | `04-base/comum/nicho.md` | A habilidade de adaptação do plugin (`adaptar-comercial`, `adaptar-experiencia`, `adaptar-juridico` ou `adaptar-controladoria`) |
| 3. Materiais adaptados | Roteiros, bibliotecas de mensagens, jornada, régua, casos de teste reescritos para o nicho | `04-base/` | A habilidade de adaptação, que chama cada habilidade no modo "adaptar" |
| 4. Rotinas próprias | O que o escritório faz sempre do mesmo jeito e nenhuma habilidade cobre | `04-base/comum/rotinas-do-escritorio.md` e `04-base/habilidades-do-escritorio/<nome>/` | A habilidade de adaptação, no modo "rotina nova" |

E uma quinta, contínua: **os aprendizados** (`aprender-com-o-uso.md`), que guardam cada correção.

## O perfil do nicho (`nicho.md`)

Formato fixo, para todas as habilidades lerem do mesmo jeito:

```markdown
---
documento: Perfil do nicho
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
---

# Nicho · [NOME DO NICHO]

## Quem é o cliente
(idade, região, leitura, canal preferido, como chega ao escritório, o que ele já tentou antes)

## Como ele fala
| O cliente diz | Quer dizer | Como responder |
|---|---|---|

## Os casos que chegam
| Tipo de caso | Frequência (estimativa) | O que o cliente quer ouvir | O que ele precisa entender |
|---|---|---|---|

## As perguntas que ele faz (antes e depois do contrato)
(as dez mais comuns, do jeito que chegam)

## Os momentos de aflição
(quando o cliente costuma se desesperar: carta do INSS, audiência, perícia, depósito que não cai)

## Documentos típicos
(por tipo de caso, com onde o cliente consegue)

## Sazonalidade e ritmo
(meses cheios e vazios, tempo típico de cada fase `[CONFERIR]`)

## Cuidados do nicho
(vulnerabilidades frequentes, temas sensíveis, o que nunca dizer a esse público)

## O que este nicho pesquisa sozinho
(o que o cliente costuma perguntar a uma IA ou procurar na internet, e o erro mais comum que ele traz)
```

Regras do nicho:
1. **Do escritório, não da internet.** O perfil sai de entrevista com o advogado e de mensagens reais anonimizadas. Os plugins não trazem perfis de nicho prontos: nicho é amplo, e cada escritório descreve o seu. A habilidade pergunta, organiza e só grava o que o advogado confirmar.
2. **Sem estatística.** Frequência é estimativa do advogado, marcada assim.
3. **Prazo de fase** (quanto tempo um tipo de processo leva) fica `[CONFERIR]` e nunca vai para mensagem ao cliente como promessa.

## Rotina nova vira habilidade

Quando o escritório tem uma rotina própria ("toda sexta mandamos um áudio curto para os clientes com audiência na semana seguinte"), a habilidade de adaptação:

1. entrevista: o que dispara, o que se faz, com que material, quem aprova, o que nunca pode acontecer;
2. escreve a rotina em `rotinas-do-escritorio.md`, com S, A e H em cada passo;
3. gera uma habilidade nova em `04-base/habilidades-do-escritorio/<nome>/SKILL.md`, no mesmo formato das habilidades do plugin (com "Campos da ficha que esta habilidade usa" e o passo "Aprender");
4. testa a habilidade com três casos (o comum, o com exceção, o que deve parar);
5. empacota em `.zip` para instalar (Personalizar > Habilidades > Enviar; conferir na configuração da conta) e, se o agente do ciclo estiver em uso, oferece incluir a rotina no ciclo.

Quem usa o plugin `inicio-automacao` pode fazer o caminho completo (POP, teste, versão) pela `pop-para-skill`. A adaptação faz o caminho curto, para rotinas pequenas.

## Quando adaptar de novo

- O escritório entrou num nicho novo ou mudou de público.
- Os aprendizados passaram de 30 linhas em uso.
- Na revisão trimestral do escritório.
