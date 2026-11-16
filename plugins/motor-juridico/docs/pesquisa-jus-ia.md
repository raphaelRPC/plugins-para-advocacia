# Pesquisa no Jus IA e a base de jurisprudência do escritório

A pesquisa de jurisprudência do plugin é feita no **Jus IA**. O advogado pesquisa lá, traz o resultado para o Claude, e o plugin organiza, confere e guarda na base do escritório. Com o tempo, a base vira o acervo próprio do escritório: os julgados que o escritório já conferiu e usa, por tema, prontos para a próxima peça.

## Como trazer uma pesquisa

1. Pesquise o tema no Jus IA, do jeito que você já pesquisa.
2. Traga para o Claude o que voltou: a resposta, os julgados com número, tribunal, órgão, relator e data, e o link de cada um. Pode colar o texto, exportar o que a ferramenta permitir ou salvar a página. Conferir na configuração da sua conta o que dá para exportar.
3. Rode a habilidade `trazer-pesquisa` (ou diga "guarda essa pesquisa na base"). Ela:
   - separa cada julgado numa ficha;
   - marca o que precisa ser conferido no inteiro teor (`citacoes.md`);
   - pergunta a que tema e a que tese do escritório a pesquisa serve;
   - grava em `04-base/juridico/jurisprudencia/<tema>.md`.
4. A conferência de cada julgado na fonte acontece na `conferir-citacoes`, na hora de usar ou num lote de conferência.

Se no futuro o Jus IA estiver conectado à sua conta do Claude, as habilidades usam o conector para pesquisar direto, sempre com a mesma conferência. Conferir na configuração da conta.

## O arquivo de cada tema

```markdown
---
documento: Jurisprudência · [TEMA]
versao: 1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
teses_do_escritorio: [nomes das teses de 04-base/juridico/teses/ que usam este tema]
---

# [TEMA]

## Como o tema está hoje (resumo do escritório)
(3 a 6 linhas, escritas pelo advogado ou aprovadas por ele: corrente que prevalece, divergências, o que mudou)

## Julgados

### [TRIBUNAL] · [CLASSE E NÚMERO] · [DATA DO JULGAMENTO]
- Órgão e relator:
- Tese em uma frase:
- Trecho útil (entre aspas só se conferido palavra por palavra):
- Para que serve no escritório: (a favor de qual tese, contra qual argumento)
- Fonte: Jus IA, pesquisa de AAAA-MM-DD, link
- Conferência no inteiro teor: AAAA-MM-DD · verde | amarelo | vermelho | não conferido
- Situação: vigente | superado em parte | superado | `[CONFERIR]`

## Histórico do tema
(data, o que mudou, quem atualizou)
```

## Regras da base

1. **Só entra com fonte.** Julgado sem número, tribunal e data, ou sem link para conferir, não entra.
2. **Conferido tem data.** A conferência vale pelo prazo de `validade_da_conferencia` da ficha jurídica (padrão: 90 dias). A `monitor-de-precedentes` avisa quando um tema precisa de pesquisa nova.
3. **Contra também entra.** Julgado contrário à tese do escritório fica no tema, marcado "contra". É ele que a `advogado-do-diabo` usa.
4. **Sem dado de cliente.** A base guarda o julgado, não o caso do escritório.
5. **A base é do escritório.** Ela fica em `04-base/` e pode ir para o Projeto no Claude, para todas as habilidades consultarem.
