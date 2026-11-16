# Quando o ciclo não roda

Leia no modo configurar (para combinar o plano) e no modo não rodou (para achar a causa).

## 1. Sinais

- Não há arquivo de hoje em `07-operacao/experiencia/rotina/`.
- O registro de uso não tem linha de hoje.
- O `/motor-experiencia:status` avisa dois dias úteis sem ciclo.
- A fila tem rascunho `pendente` há mais de um dia útil.
- Um cliente pergunta "e aí?" e estava na seção "sem notícia" de ontem: o ciclo rodou, mas ninguém leu.

## 2. Causas prováveis

| Sinal | Causa provável | O que fazer |
|---|---|---|
| Nenhum arquivo e nenhuma linha | Tarefa agendada não disparou (computador desligado, app fechado, sessão expirada) | Rodar à mão hoje; conferir na configuração da conta se a tarefa precisa do computador ligado |
| Linha no registro com erro "não achei a carteira" | A carteira mudou de lugar ou de nome | Devolver para `07-operacao/experiencia/carteira.csv` ou corrigir o caminho na tarefa |
| Erro "faltam colunas obrigatórias" | A planilha foi salva com outros títulos | Corrigir a primeira linha (formato em `docs/carteira.md`) e rodar `carteira.py --conferir` |
| Erro "só a linha de títulos" | A carteira foi apagada ou esvaziada ao salvar | Recuperar a versão anterior; nunca recriar de memória |
| Resumo existe, fila cheia de pendentes | Ninguém aprovou | Combinar de novo quem aprova e em que horário (`quem_aprova_rascunhos`) |
| Agente indisponível | Ambiente sem agentes de plugin (chat com Projeto) | Ciclo à mão pela rotina, modo rodar |
| Critério "padrão do script" no retrato | Campo da ficha vazio | Preencher o campo pelo `/motor-experiencia:ficha` |

## 3. O plano combinado (copiar para a ficha da automação)

```
Se até [HORA] não houver o resumo de hoje em 07-operacao/experiencia/rotina/:
1. [FUNÇÃO] roda o pedido de toda manhã (assets/tarefa-agendada.md, seção 2).
2. Se o Claude não estiver disponível, [FUNÇÃO] abre a carteira na planilha e olha, nesta ordem: reclamação aberta e insatisfeito; compromisso até o próximo dia útil; último contato mais antigo que [N] dias.
3. Registra o dia no registro de uso como "manual" ou "não rodou", com a causa.
4. Dois dias úteis seguidos sem ciclo: [DONO DA FICHA] revê o jeito de rodar.
```

## 4. O que nunca fazer para compensar

- Mandar de uma vez, sem leitura, os rascunhos acumulados de vários dias.
- Mandar mensagem de rotina para todo mundo "para zerar" a seção sem notícia: quem está insatisfeito ou em fase de decisão precisa de uma pessoa antes.
- Aumentar o `maximo_sem_noticia` para o retrato ficar limpo. O prazo muda na ficha, por decisão do escritório, e o cliente continua sem notícia.
- Recriar a carteira de memória quando ela some.
