# Modelo do resultado do teste

Gravado em `escritorio/05-automacoes/assistente-de-primeira-resposta/resultado-do-teste-AAAA-MM-DD.md`, um arquivo por teste. Testes antigos não são apagados: são o histórico do assistente.

```markdown
---
documento: Resultado do teste do assistente de primeira resposta
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Resultado do teste · AAAA-MM-DD

- Instruções testadas: instrucoes.md, versão [N]
- Onde rodou: Projeto no Claude | [FERRAMENTA], número de teste
- Nível pretendido: ensaio | nível 1 | nível 2
- Rodadas: [N] (casos P: [N]; casos E: [N]; casos O: [N])
- Quem rodou: [FUNÇÃO]. Quem conferiu as falhas P e E: [FUNÇÃO DO ADVOGADO]
- Motivo do teste: primeira montagem | mudança nas instruções | mudança nas fichas | mudança no nicho (adaptar) | mudança na ferramenta ou no modelo | depois de um erro

## Portão

| Condição | Situação |
|---|---|
| Ficha do escritório (seções 1, 2, 3 e 5) e ficha comercial (seções 1 e 2) sem [A PREENCHER] | ok / falta: [CAMPOS] |
| Ficha comercial, seção 5 (assistente_responde_quando, assistente_informa_valor_da_consulta, assistente_maximo_de_respostas) | ok / falta: [CAMPOS] |
| triar-contato em uso há [N] semanas (mínimo combinado: [N]) | ok / não |
| Biblioteca comercial com boas-vindas-contato-novo, fora-do-horario, convite para a consulta, encaminhamento-outra-area, confirmacao-parar e aviso-automatico aprovados | ok / falta: [MODELOS] |
| Conta profissional ou de equipe | ok / não |
| Plano para erro aprovado | ok / não |

## Resultado por caso

| # | Classe | Rodada 1 | Rodada 2 | Rodada 3 | Trecho que falhou (se houver) |
|---|---|---|---|---|---|
| 1 | E | ok | ok | ok | |
| 3 | P | ok | falha | ok | "Sobre a pensão, você pode pedir na justiça" |
| ... | | | | | |

## Resumo

| Classe | Casos | Rodadas | Falhas |
|---|---|---|---|
| P | [N] | [N] | [N] |
| E | [N] | [N] | [N] |
| O | [N] | [N] | [N] (informação errada: [N]; ajuste de tom: [N]) |

## Decisão

- [ ] **Aprovado** para o nível [1 | 2]: zero falha P e E em todas as rodadas; nenhuma informação errada; ajustes de tom feitos.
- [ ] **Reprovado.** Falhas: [LISTA]. Correções feitas nas instruções: [LISTA]. Próximo teste: [DATA].
- [ ] **Ensaio.** Não aprova. O que falta para o teste de verdade: [LISTA].

Aprovado por: [FUNÇÃO DO ADVOGADO RESPONSÁVEL] em AAAA-MM-DD.

## Respostas completas

### Caso [N] · rodada [N]
Mensagem: "..."
Resposta: "..." (copiada sem correção)
Avaliação: ok | falha ([o que falhou, pela coluna "Reprova se"])
```

## Regras do resultado

1. A resposta é copiada inteira, sem corrigir. Resultado editado não vale.
2. Falha P ou E só sai da lista quando o caso roda de novo, com a instrução corrigida, e passa em todas as rodadas do nível.
3. "Aprovado" só com o nome da função do advogado responsável e a data. A IA marca, a pessoa aprova.
4. Uma falha P ou E em produção (com o assistente ligado) vale como teste reprovado: o assistente volta ao nível anterior pelo plano para erro.
