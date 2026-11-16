# Modelo dos casos de teste do escritório (controladoria)

Os casos de teste do escritório trocam o lote fictício por publicações reais anonimizadas, com o gabarito escrito e conferido por duas pessoas do escritório. Ficam em `escritorio/04-base/casos-de-teste/controladoria/casos.md`. Servem para rodar as habilidades antes de usar com publicação nova, depois de cada adaptação, quando a tabela de regras ou o calendário mudam e quando uma habilidade própria muda de versão.

Regras:
- Só material anonimizado: nome por `[CLIENTE]`, CPF por `[DOC]`, processo por `[PROCESSO]` (o número fica fora do caso de teste; o tribunal e o órgão podem ficar, porque a conta depende deles).
- Só em conta profissional ou de equipe.
- O gabarito é das pessoas: as datas do gabarito são contadas à mão por uma pessoa e conferidas por outra, com o calendário do ano. A habilidade pode sugerir, marcado "sugestão", e grava só o que as duas confirmarem.
- Cada caso traz a armadilha que ele testa: é ela que justifica o caso.

```markdown
---
documento: Casos de teste da controladoria
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM RESPONDE PELA CONTROLADORIA]
---

# Casos de teste · controladoria

## Caso K1 · [tipo de ato] · [tribunal]
Material: [o trecho do ato anonimizado, a fonte e a data de disponibilização ou de envio ao portal]
Habilidade: [triar-publicacoes | calcular-prazo | dupla-conferencia | rotina-da-controladoria | habilidade própria]
A armadilha: [o que torna o caso difícil: feriado local, manutenção sem certidão, prazo da outra parte, ciência tácita em dia sem expediente, duplicada, sem caso]
Gabarito: [triagem; dias e de onde vêm; publicada, início, vencimento, segurança; ou "nenhum prazo, porque..."]
Não pode falhar: [a lista, um item por linha]
Gabarito contado por: [função] em AAAA-MM-DD · conferido por: [outra função] em AAAA-MM-DD
```

## Exemplo (Escritório Modelo, fictício, a partir do lote de treino)

```markdown
## Caso K1 · custas · TJMG
Material: "Intime-se a parte autora para recolher as custas complementares no prazo de 5 dias", DJEN, disponibilizada em 2026-04-14
Habilidade: calcular-prazo e rotina-da-controladoria
A armadilha: manutenção do PJe em 2026-04-24 anunciada pelo TJMG, sem certidão
Gabarito: prazo; 5 dias úteis pelo ato; publicada 2026-04-15, início 2026-04-17, vencimento 2026-04-24, segurança 2026-04-22
Não pode falhar: não empurrar para 2026-04-27; pular o feriado de 2026-04-16; sair `sugerido`
Gabarito contado por: estagiária em 2026-04-15 · conferido por: advogada titular em 2026-04-15

## Caso K2 · captação com atraso · TRT3
Material: sentença disponibilizada em 2026-04-09 e só captada em 2026-04-14 (o ciclo não rodou)
Habilidade: rotina-da-controladoria
A armadilha: o prazo já corria desde 2026-04-13
Gabarito: PESSOA AGORA com "captada com atraso"; segurança 2026-04-22, vencimento 2026-04-24
Não pode falhar: aparecer no topo; não aparecer como prazo que vale antes da dupla conferência
Gabarito contado por: estagiária em 2026-04-15 · conferido por: advogada titular em 2026-04-15
```
