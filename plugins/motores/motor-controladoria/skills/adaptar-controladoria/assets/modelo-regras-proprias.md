# Modelo das regras próprias da controladoria

A `adaptar-controladoria` usa este modelo na parte B. Cada regra que o escritório pratica ("nenhum prazo é cumprido no último dia", "recurso também na agenda do sócio") ganha uma linha, uma classe e um destino. A classe decide por onde a regra passa antes de valer.

## As classes

| Classe | O que a regra muda | Destino | Por onde passa |
|---|---|---|---|
| contagem | A data fatal: o que conta como dia útil, quando começa o prazo, número de dias por ato, prazo em dobro, ciência | `04-base/controladoria/regras-de-contagem.md` (linha nova com chave própria, ou a seção "Prazos por ato") e o calendário | **Validação da tabela de regras pela `calendario-forense`**, por quem responde pela controladoria, com `validada_por` e `validada_em`. Antes disso, não vale |
| segurança | Só a meta interna: quantos dias antes do fatal, por tipo de ato | K: `dias_de_seguranca` e `regras_proprias` | Ok da pessoa; a `calcular-prazo` lê |
| agenda | Onde e para quem o prazo vai: agenda do sócio, lembrete a mais | K: `regras_proprias` e `lembretes` | Ok da pessoa; a `agenda-de-prazos` lê |
| conferência | Quem confere o quê: recurso sempre com o sócio, prazo de hoje com duas pessoas presentes | K: `quem_confere` e `regras_proprias` | Ok da pessoa; a `dupla-conferencia` lê |
| triagem e providência | O que costuma ser feito com cada ato | `04-base/controladoria/providencias.md` | `providencia-sugerida` (se instalada), com a pessoa |
| painéis | Quem abre qual sistema e quando | `04-base/controladoria/paineis.md` | `paineis-dos-sistemas` (se instalada) |

## Regras que não entram

- Regra que deixa a data fatal **mais tarde** do que a tabela validada ("a gente conta do dia em que abriu", "manutenção sempre empurra"): na dúvida, vale a data mais cedo. A habilidade explica e propõe a versão segura (por exemplo, "indisponibilidade só empurra com certidão").
- Regra que tira uma pessoa do caminho ("se as duas contas baterem, pode agendar sem conferir"): a dupla conferência é de pessoas.
- Regra que põe senha, certificado ou token com a IA.
- Número de dias de recurso ou manifestação "de cabeça": vem do ato ou da tabela do escritório, validada.

## O formato

O quadro fica em `escritorio/04-base/controladoria/nicho/adaptar-controladoria.md`. A frase curta de cada regra em uso vai também para o campo `regras_proprias` da ficha da controladoria, que é o que as outras habilidades leem.

```markdown
---
documento: Regras próprias da controladoria
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELA CONTROLADORIA]
---

# Regras próprias da controladoria

| # | A regra, nas palavras do escritório | Classe | Destino | Situação | Validada por e quando |
|---|---|---|---|---|---|
| R1 | [frase curta, com verbo] | contagem / segurança / agenda / conferência / triagem e providência / painéis | [arquivo e campo] | proposta / em validação / em uso / recusada (motivo) | [nome, AAAA-MM-DD] |
```

## Exemplo (Escritório Modelo, fictício)

```markdown
| R1 | Nenhum prazo é cumprido no último dia: recurso com 3 dias úteis de segurança | segurança | K: regras_proprias ("recurso: 3 dias úteis de segurança"); dias_de_seguranca segue 2 para o resto | em uso | advogada titular, 2026-04-15 |
| R2 | Todo recurso também na agenda da advogada titular | agenda | K: regras_proprias | em uso | advogada titular, 2026-04-15 |
| R3 | Feriado municipal de Contagem nos processos da vara de lá | contagem | calendário do TJMG do ano, linha com vale_para TJMG e a fonte | em validação | (calendario-forense) |
| R4 | "Manutenção do PJe sempre empurra o prazo" | contagem | (nenhum) | recusada: só a indisponibilidade certificada empurra o vencimento; sem certidão, vale a data mais cedo | advogada titular, 2026-04-15 |
```
