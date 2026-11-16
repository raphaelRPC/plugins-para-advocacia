# Modelos da matriz de riscos e do plano de ação

Use nos modos mapa de riscos e plano de ação. A matriz não usa percentual: usa os critérios combinados com a empresa. O plano não tem ação sem dono, prazo e evidência.

## 1. Matriz de riscos

```markdown
---
documento: Mapa de riscos · [EMPRESA]
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [ADVOGADO]
antes_de_enviar:
  - critérios de probabilidade e impacto confirmados com a empresa em AAAA-MM-DD
  - normas do setor a conferir: [LISTA]
---

# Mapa de riscos · [EMPRESA]

## Critérios combinados com a empresa
| Nível | Probabilidade (o que quer dizer aqui) | Impacto (o que quer dizer aqui) |
|---|---|---|
| alto | [EX.: já aconteceu ou acontece todo mês] | [EX.: perda do maior cliente, interdição, risco a pessoa] |
| médio | [EX.: pode acontecer no ano] | [EX.: multa relevante, retrabalho grande] |
| baixo | [EX.: nunca aconteceu, controle forte] | [EX.: ajuste interno] |

## Riscos
| # | Processo | O que pode acontecer | Controle que existe | Probabilidade | Impacto | Prioridade | Norma a conferir |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
```

Prioridade: alto com alto primeiro; depois alto com médio; o resto entra no plano em ordem.

## 2. Plano de ação

```markdown
---
documento: Plano de ação · [EMPRESA]
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [DONO DO PROGRAMA NA EMPRESA]
---

# Plano de ação · [EMPRESA]

| # | Risco (do mapa) | Ação | Dono na empresa | Prazo | Evidência | Situação |
|---|---|---|---|---|---|---|
| 1 | | | [FUNÇÃO] | AAAA-MM-DD ou [A DEFINIR] | | a fazer · em andamento · feito · atrasado |

## Acompanhamento
| Data | O que mudou | Quem informou |
|---|---|---|
```

## Treino (fictício, Restaurante Sabor Mineiro Ltda.)

Três linhas de exemplo para conferir o formato (números e situações inventados):

| # | Risco | Ação | Dono | Prazo | Evidência |
|---|---|---|---|---|---|
| 1 | Contrato com o aplicativo de entrega exige programa de integridade `[CONFERIR: a cláusula do contrato]` | Aprovar o código de conduta e a política de relação com terceiros | sócio administrador | [A DEFINIR] | código assinado e enviado ao aplicativo |
| 2 | Fornecedor de carnes autuado `[CONFERIR: a autuação e a norma sanitária]` | Due diligence do fornecedor e cláusula de conformidade sanitária nos contratos | gerente de compras | [A DEFINIR] | parecer de due diligence; contrato aditado |
| 3 | Dados de clientes do delivery sem aviso de privacidade `[CONFERIR: obrigações da LGPD para o porte]` | Aviso de privacidade e nomeação do encarregado | sócio administrador | [A DEFINIR] | aviso publicado; nomeação registrada |
