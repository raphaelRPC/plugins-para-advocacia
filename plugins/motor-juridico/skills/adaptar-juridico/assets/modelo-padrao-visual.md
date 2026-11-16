---
documento: Padrão visual das peças
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
origem: [de onde saiu: entrevista, peça boa lida pelo script padrao_do_docx.py, ou os dois]
---

# Padrão visual · [NOME DO ESCRITÓRIO]

> Como toda peça do escritório sai no papel. A `minutar-peca` (e o script de .docx dela) lê as linhas "chave: valor" da seção 1 exatamente com estes nomes. Medidas em centímetros, com vírgula ou ponto. Valor sem resposta fica `[A PREENCHER]`, e o script usa o padrão dele, com aviso.

## 1. O que o script de .docx lê

- fonte: [A PREENCHER] (ex.: Times New Roman, Garamond, Arial)
- corpo: [A PREENCHER] (ex.: 12)
- espacamento: [A PREENCHER] (entre linhas do texto; ex.: 1,5)
- alinhamento: [A PREENCHER] (opções: justificado | esquerda)
- recuo_primeira_linha: [A PREENCHER] (ex.: 2; 0 para sem recuo)
- margem_superior: [A PREENCHER] (ex.: 3)
- margem_inferior: [A PREENCHER] (ex.: 2)
- margem_esquerda: [A PREENCHER] (ex.: 3)
- margem_direita: [A PREENCHER] (ex.: 2)
- recuo_citacao: [A PREENCHER] (recuo da citação longa; ex.: 4)
- corpo_citacao: [A PREENCHER] (ex.: 10)
- espacamento_citacao: [A PREENCHER] (ex.: 1)
- timbre: [A PREENCHER] (caminho de um .docx com o papel timbrado, relativo a esta pasta, ex.: timbre.docx; ou "sem timbre")

## 2. O que a habilidade segue ao escrever

- titulos: [A PREENCHER] (ex.: em maiúsculas, numerados "1. DOS FATOS", sem sublinhado)
- numeracao_dos_paragrafos: [A PREENCHER] (ex.: 1.1, 1.2 dentro de cada título; ou sem numeração)
- pedidos: [A PREENCHER] (ex.: numerados, cada um com o fundamento e os fatos ao lado)
- documentos: [A PREENCHER] (ex.: "(doc. 3)" no fim da frase)
- fecho: [A PREENCHER] (ex.: "Nestes termos, pede deferimento." ou sem fecho)
- assinatura: [A PREENCHER] (ex.: nome, OAB/UF e número, sem cargo)
- o_que_nunca_aparece: [A PREENCHER] (ex.: negrito no meio do parágrafo, latim, "data venia", caixa alta em frase inteira)

## Histórico

(data, o que mudou, quem pediu)

---

## Exemplo preenchido (Escritório Modelo, fictício)

```markdown
- fonte: Times New Roman
- corpo: 12
- espacamento: 1,5
- alinhamento: justificado
- recuo_primeira_linha: 2
- margem_superior: 3
- margem_inferior: 2
- margem_esquerda: 3
- margem_direita: 2
- recuo_citacao: 4
- corpo_citacao: 10
- espacamento_citacao: 1
- timbre: sem timbre
- titulos: em maiúsculas, numerados "1. DOS FATOS"
- numeracao_dos_paragrafos: 1.1, 1.2 dentro de cada título
- pedidos: numerados, cada um com o fundamento e os fatos ao lado
- documentos: "(doc. 3)" no fim da frase
- fecho: sem fecho
- assinatura: advogada titular, OAB/MG e número
- o_que_nunca_aparece: latim, adjetivo sobre a outra parte, negrito no meio do parágrafo
```
