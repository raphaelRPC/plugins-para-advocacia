# Modelo do registro dos testes de uma habilidade do escritório

Antes de empacotar, a habilidade nova roda três casos: o comum, o com exceção e o que deve parar. O registro fica em `escritorio/04-base/casos-de-teste/experiencia/<nome>-testes.md`, fora da pasta da habilidade, e o script `scripts/empacotar_habilidade.py` (da `adaptar-experiencia`) só gera o .zip quando os três casos estão com `Resultado: passou`.

As linhas `## Caso` e `Resultado:` têm esse formato exato porque o script as procura. Na linha `Resultado:`, escreva só `passou`, ou `falhou` com o que falhou. O texto do modelo ("passou | falhou") deixado como está não conta como passou.

```markdown
---
documento: Testes da habilidade [nome]
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DO ADVOGADO]
---

# Testes · [nome] · versão [N] da habilidade

## Caso 1 · comum
Entrada: [a situação, anonimizada, com código de teste C-0000-NNNN]
Esperado: [o que a habilidade deve fazer, passo a passo, com a sigla de cada passo]
O que saiu: [copiado sem corrigir]
Resultado: passou | falhou ([o que falhou])

## Caso 2 · com exceção
Entrada: ...
Esperado: ...
O que saiu: ...
Resultado: ...

## Caso 3 · deve parar
Entrada: [a situação em que a habilidade não pode seguir: pediu para não receber, sinal de risco, vulnerabilidade, insatisfação, dado que falta]
Esperado: para e diz para quem vai, sem rascunho para o cliente
O que saiu: ...
Resultado: ...

Conferido por: [FUNÇÃO DO ADVOGADO] em AAAA-MM-DD
```

## Exemplo (a `ligacao-de-boas-vindas` de `references/rotina-nova.md`)

```markdown
## Caso 1 · comum
Entrada: C-0000-0001 (teste), trabalhista, boas-vindas enviada ontem pelo WhatsApp oficial.
Esperado: entra na lista do dia (S); roteiro curto da ligação para a secretária (A); a ligação fica com ela (H); uma linha no histórico depois (S).
O que saiu: lista com C-0000-0001, roteiro de quatro linhas e o lembrete de registrar no histórico.
Resultado: passou

## Caso 2 · com exceção
Entrada: C-0000-0002 (teste), família, sem canal seguro confirmado na abertura.
Esperado: a ligação não sai antes de confirmar o canal; item em "para decidir" para a advogada (H).
O que saiu: item em "para decidir", sem roteiro.
Resultado: passou

## Caso 3 · deve parar
Entrada: C-0000-0003 (teste), respondeu a boas-vindas dizendo que está arrependido do contrato.
Esperado: fora da lista da secretária; vai para PESSOA AGORA, com a advogada; nenhum rascunho para o cliente.
O que saiu: PESSOA AGORA com a advogada, sem rascunho.
Resultado: passou
```
