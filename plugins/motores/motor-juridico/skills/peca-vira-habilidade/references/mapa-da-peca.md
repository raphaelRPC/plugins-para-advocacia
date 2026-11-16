# O mapa da peça (formato)

O mapa é o coração da habilidade própria. Ele diz, de uma peça que o escritório faz sempre: o que é fixo, o que muda de um cliente para outro, que teses entram, que trechos se repetem, como o escritório escreve e quando parar. A habilidade gerada lê o mapa a cada peça; a `pecas-em-lote` (se instalada) monta o lote a partir dele; o script de empacotamento confere o formato. Por isso os títulos e as colunas abaixo têm estes nomes exatos.

O mapa fica dentro da habilidade gerada, em `escritorio/04-base/habilidades-do-escritorio/<peca>/references/mapa-da-peca.md`. Um exemplo preenchido está em `references/exemplo/mapa-da-peca.md`.

## O molde

```markdown
---
documento: Mapa da peça
peca: [nome-da-peca, igual ao nome da habilidade]
area: [uma das areas da ficha do escritório, sem acento]
versao: 1
revisado_em: AAAA-MM-DD
dono: [função de quem responde pela peça]
---

# Mapa da peça · [Nome da peça por extenso]

## 1. Origem
| Peça | O que era | Por que entrou |
|---|---|---|
| P1 | [tipo, ano, juízo, resultado se houver; sem nome de cliente] | [o que ela tem de bom] |

## 2. Estrutura
| Ordem | Parte | Fixa ou condicional | Observação |
|---|---|---|---|
| 1 | Endereçamento | fixa | |

## 3. Variáveis
| variavel | tipo | origem | obrigatoria | exemplo | regra |
|---|---|---|---|---|---|
| genero | genero | cliente | sim | f | f ou m; define "a autora" ou "o autor" |

### Valores do escritório
- [variavel com origem ficha]: [valor que vale para toda peça]

## 4. Teses
| tese | quando entra | arquivo | citações |
|---|---|---|---|

## 5. Trechos padrão
### T1 · [nome curto]
[o texto, igual ao do escritório]

## 6. Escolhas de estilo
- [uma escolha por linha, como o advogado disse]

## 7. Exceções e quando parar
| Situação | O que a habilidade faz |
|---|---|

## 8. Modelo da peça
<!-- modelo: inicio -->
[o texto da peça, com {{variavel}} no lugar do que muda]
<!-- modelo: fim -->

## 9. Citações
| Citação | Onde aparece no modelo | Marca |
|---|---|---|

## 10. Histórico
| Data | Versão | O que mudou | Por quê |
|---|---|---|---|
```

## As colunas das variáveis

| Coluna | O que vai |
|---|---|
| `variavel` | Nome em minúsculas, sem acento, com sublinhado (`data_cessacao`). É o nome que aparece no modelo e o título da coluna na planilha do lote |
| `tipo` | `texto`, `data` (sai DD/MM/AAAA), `mes` (sai MM/AAAA), `valor` (sai R$ 1.234,56), `numero`, `genero` (f ou m), `opcao(a/b/c)` (só os valores da lista), `lista` (itens separados por ponto e vírgula; sai "a, b e c") |
| `origem` | `cliente` (documento ou fala do cliente), `dossie` (o dossiê do caso), `advogado` (decisão do advogado no caso), `ficha` (vale para toda peça: o valor fica em "Valores do escritório") |
| `obrigatoria` | `sim` ou `nao`. Variável obrigatória vazia barra a peça |
| `exemplo` | Um valor de exemplo, sempre fictício |
| `regra` | O cuidado daquela variável, em uma frase ("se dois documentos dão datas diferentes, para") |

## A escrita do modelo

| Escreva | Quer dizer |
|---|---|
| `{{data_cessacao}}` | O valor da variável, no formato do tipo |
| `{{genero:A autora\|O autor}}` | O primeiro texto quando `genero` é `f`, o segundo quando é `m` |
| `{{#se pedir_tutela=sim}}` ... `{{/se}}` | O trecho só entra quando a variável tem aquele valor. Um bloco não fica dentro de outro |
| `{QUALIFICAÇÃO COMPLETA}` | Campo de quem protocola (chave simples): sai do sistema do escritório na hora, nunca do chat nem da planilha |
| `[CONFERIR: ...]` | Toda citação do modelo, até a conferência na fonte (`../../docs/citacoes.md`) |

Regras do modelo:
1. **Toda citação nasce marcada.** O modelo leva a marca; a peça só perde a marca depois da `conferir-citacoes`. Citação conferida e guardada na base há menos de `validade_da_conferencia` pode ir sem marca para a peça, nunca para o modelo.
2. **Dado de identificação não é variável de planilha.** Nome completo, CPF, endereço e número de benefício saem do sistema do escritório no protocolo, como chave simples. O modelo e a planilha guardam o mínimo.
3. **Toda variável do modelo está na tabela, e toda variável obrigatória da tabela está no modelo.** O script de empacotamento confere.
4. **Exceção que muda a tese não é bloco condicional.** Se a exceção muda o caminho do caso, a habilidade para e leva ao advogado (seção 7).
5. **O modelo é do escritório.** Ele sai das peças boas e das decisões do advogado no mapa; o que a habilidade sugerir vai marcado "sugestão" até o ok.
