# Modelo do registro dos testes de uma habilidade do escritório

Antes de empacotar, a habilidade nova roda três casos: o comum, o com exceção e o que deve parar. O registro fica em `escritorio/04-base/casos-de-teste/juridico/<nome>-testes.md`, fora da pasta da habilidade. Os scripts de empacotamento (o `scripts/empacotar_habilidade.py` desta habilidade, para rotinas, e o da `peca-vira-habilidade`, para peças) só geram o .zip com os três casos em "Resultado: passou" e o "Conferido por:" preenchido.

As linhas `## Caso`, `O que saiu:`, `Resultado:` e `Conferido por:` têm este formato exato porque os scripts as procuram. Na habilidade de peça, o título diz também "versão N da habilidade", igual à versão do mapa.

```markdown
---
documento: Testes da habilidade [nome]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DO ADVOGADO]
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
Entrada: [a situação em que a habilidade não pode seguir: sem tese definida, área diferente, dado que falta, prazo interno de hoje, dado sensível que não deve ir à peça]
Esperado: para, diz por quê e para quem vai, sem minuta
O que saiu: ...
Resultado: ...

Conferido por: [FUNÇÃO DO ADVOGADO] em AAAA-MM-DD
```

A linha "Resultado: passou | falhou" do modelo não conta: o caso precisa ter rodado e alguém escolhido uma das duas.
