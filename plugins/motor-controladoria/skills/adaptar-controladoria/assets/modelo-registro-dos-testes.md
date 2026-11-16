# Modelo do registro dos testes de uma habilidade do escritório (controladoria)

Antes de empacotar, a habilidade nova roda três casos: o comum, o com exceção e o que deve parar. O registro fica em `escritorio/04-base/casos-de-teste/controladoria/<nome>-testes.md`, fora da pasta da habilidade. O `scripts/empacotar_habilidade.py` desta habilidade só gera o .zip com os três casos em "Resultado: passou" e o "Conferido por:" preenchido.

As linhas `## Caso`, `O que saiu:`, `Resultado:` e `Conferido por:` têm este formato exato porque o script as procura.

```markdown
---
documento: Testes da habilidade [nome]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Testes · [nome] · versão [N] da habilidade

## Caso 1 · comum
Entrada: [a situação, anonimizada ou fictícia]
Esperado: [o que a habilidade deve fazer, com a sigla S, A ou H de cada passo]
O que saiu: [copiado do que a habilidade entregou, sem corrigir]
Resultado: passou | falhou ([o que falhou])

## Caso 2 · com exceção
Entrada: ...
Esperado: ...
O que saiu: ...
Resultado: ...

## Caso 3 · deve parar
Entrada: [a situação em que a habilidade não pode seguir: prazo de hoje ou amanhã, publicação sem caso, número de dias que não vem do ato nem da tabela, calendário que falta, pedido para confirmar prazo]
Esperado: para, diz por quê e para quem vai, sem confirmar nada
O que saiu: ...
Resultado: ...

Conferido por: [FUNÇÃO] em AAAA-MM-DD
```

A linha "Resultado: passou | falhou" do modelo não conta: o caso precisa ter rodado e alguém escolhido uma das duas.
