---
documento: Providências de costume
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
validada_por: [A PREENCHER]
treino: nao
---

# Providências de costume · [NOME DO ESCRITÓRIO]

O que este escritório costuma fazer com cada tipo de ato. A tabela é a memória do escritório, montada com quem decide as providências a partir das peças que o escritório já faz. Ela serve para **sugerir**: quem decide cada publicação continua sendo a pessoa de `quem_decide_providencia`.

Regras da tabela:
- Uma linha por situação que se repete. A `chave` é única, em minúsculas e com hífen.
- `o_que_o_teor_diz` traz as palavras do ato que identificam a situação ("julgo improcedente", "intime-se a parte autora para juntar"), não uma interpretação.
- `peca` é o nome da peça como o motor-juridico (se instalado) usa em `pecas.csv`, com hífen, ou `nenhuma`.
- `aviso_ao_cliente`: `ligacao` (notícia ruim, parcial ou que pede decisão do cliente), `mensagem` (lida pelo advogado antes de sair), `documento` (pedir ao cliente), `preparacao` (audiência, perícia) ou `nenhum`.
- Número de dias não mora aqui: vem do ato ou da tabela de prazos por ato (`regras-de-contagem.md`).
- Linha que ninguém confirmou fica com `[A CONFIRMAR]` na coluna `observacao` e não é usada como costume.

| chave | tipo_ato | o_que_o_teor_diz | area | rito | providencia_de_costume | peca | aviso_ao_cliente | quem_decide | observacao |
|---|---|---|---|---|---|---|---|---|---|
| [A PREENCHER] | | | | | | | | | |

## Histórico

(uma linha por mudança: data, chave, o que mudou, quem decidiu)
