# Modelo do resumo do dia

O arquivo que o ciclo (agente ou à mão) grava em `escritorio/07-operacao/experiencia/rotina/AAAA-MM-DD.md`. As seções de carteira saem do script `carteira.py`. O resto sai da entrada, da fila e dos conectores.

```markdown
---
documento: Ciclo da experiência · AAAA-MM-DD
gerado_em: AAAA-MM-DD HH:MM
como_rodou: agente | agendada | manual
dono: [FUNÇÃO QUE LÊ]
---

# Ciclo da experiência · AAAA-MM-DD ([DIA DA SEMANA])

## PESSOA AGORA
1. [CÓDIGO] [NOME CURTO] · [POR QUÊ, EM UMA FRASE] · [QUEM FALA] · [ATÉ QUANDO]
(reclamação, insatisfeito, compromisso até o próximo dia útil, notícia ruim, aflição, vulnerabilidade; nenhum rascunho com conteúdo)
Do resumo anterior, já resolvidos: [CÓDIGO] · falou em [DATA] · combinado: [O QUÊ E ATÉ QUANDO] (gravado na carteira e no histórico)
Já falaram, com retorno combinado: [CÓDIGO] · retorno em [DATA]

## Compromissos dos próximos 7 dias
- [DATA] · [TIPO] · [CÓDIGO] [NOME CURTO] · preparação: [FEITA | NA FILA | FALTA]

## Sem notícia além da régua
- [CÓDIGO] [NOME CURTO] · [N] dias · rascunho: [NA FILA | BLOQUEADO: MOTIVO]

## Fila para aprovar
| Arquivo | Para | Tipo | Revisor | Prazo |
|---|---|---|---|---|

## Documentos
- [CÓDIGO] [NOME CURTO] · [N] pendentes · [COBRANÇA NA FILA | PARA DECIDIR]

## Resumos do mês
- Por fazer: [N] · na fila: [N] · seguram para depois da ligação: [CÓDIGOS]
- Não recebem (pediram): [CÓDIGOS]

## Para decidir
- [O QUE UMA PESSOA PRECISA DECIDIR: fase, humor, encerramento, passagem sem boas-vindas]

## Registro atualizado
- [CÓDIGO] · [CAMPO]: [ANTES] para [DEPOIS]
(só proximo_contato, motivo_proximo_contato, documentos_pendentes e atualizado_em)

## O que não deu para fazer
- [O QUE E POR QUÊ, EM UMA LINHA: "não achei a carteira", "campo maximo_sem_noticia vazio, usei 30"]
```

Regras de escrita:
- Uma pessoa lê em três minutos. Seção vazia vira uma linha ("Nenhum compromisso na semana.").
- Só código, primeiro nome, área e tipo de caso curto. Nada de telefone, documento, número de processo ou detalhe de saúde.
- Nenhuma mensagem para cliente dentro do resumo: as mensagens estão na fila.
- Cliente com `pediu_para_nao_receber = sim` nunca aparece com rascunho de rotina.
