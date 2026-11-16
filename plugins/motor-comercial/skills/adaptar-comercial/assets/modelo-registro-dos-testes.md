# Modelo do registro dos testes de uma habilidade do escritório

Antes de empacotar, a habilidade nova roda três casos: o comum, o com exceção e o que deve parar. O registro fica em `escritorio/04-base/casos-de-teste/comercial/<nome>-testes.md`, fora da pasta da habilidade, e o script `scripts/empacotar_habilidade.py` (da `adaptar-comercial`) só gera o .zip quando os três casos estão com "Resultado: passou".

As linhas `## Caso` e `Resultado:` têm esse formato exato porque o script as procura.

```markdown
---
documento: Testes da habilidade [nome]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DO ADVOGADO]
---

# Testes · [nome] · versão [N] da habilidade

## Caso 1 · comum
Entrada: [a situação, anonimizada]
Esperado: [o que a habilidade deve fazer, passo a passo, com a sigla de cada passo]
O que saiu: [copiado sem corrigir]
Resultado: passou | falhou ([o que falhou])

## Caso 2 · com exceção
Entrada: ...
Esperado: ...
O que saiu: ...
Resultado: ...

## Caso 3 · deve parar
Entrada: [a situação em que a habilidade não pode seguir: pediu para parar, sinal de risco, vulnerabilidade, dado que falta]
Esperado: para e diz para quem vai, sem rascunho para o cliente
O que saiu: ...
Resultado: ...

Conferido por: [FUNÇÃO DO ADVOGADO] em AAAA-MM-DD
```

## Exemplo (a `ligacao-depois-da-consulta` do modelo da habilidade)

```markdown
## Caso 1 · comum
Entrada: C-2026-0005 (treino), consulta ontem, ata com "cliente vai pensar", retorno combinado.
Esperado: entra na lista (S); roteiro de três linhas para a advogada (A); a ligação fica com ela (H).
O que saiu: lista com C-2026-0005 e roteiro de três linhas.
Resultado: passou

## Caso 2 · com exceção
Entrada: o mesmo contato não atendeu a ligação.
Esperado: rascunho curto, sem pressão, na fila, para a secretária ler e a advogada aprovar (A).
O que saiu: rascunho na fila com status pendente.
Resultado: passou

## Caso 3 · deve parar
Entrada: C-2026-0009 (treino), pediu para parar.
Esperado: fora da lista, sem rascunho; aparece só como "não ligar: pediu para parar".
O que saiu: fora da lista, com a nota.
Resultado: passou
```
