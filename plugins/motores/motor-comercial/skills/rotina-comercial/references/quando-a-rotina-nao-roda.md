# Quando o ciclo não roda

Leia no modo configurar (para combinar o plano) e no modo "não rodou". Um ciclo que roda quatro dias em cinco e ninguém percebe o quinto é pior do que um ciclo à mão feito todo dia: a equipe confia que alguém olhou.

## 1. Como perceber

| Sinal | Onde olhar |
|---|---|
| Não existe `07-operacao/comercial/rotina/AAAA-MM-DD.md` de hoje até [HORA COMBINADA] | a pasta da rotina |
| O registro de uso não tem linha de hoje, ou tem `não rodou` | `05-automacoes/ciclo-comercial/registro-de-uso.md` |
| O resumo de hoje existe, mas "O que não deu para fazer" tem erro de leitura | o fim do resumo |
| O script parou com "ERRO:" (arquivo não encontrado, coluna faltando, registro de treino) | a mensagem do script, no resumo ou no chat |
| O `/motor-comercial:status` mostra dois dias seguidos sem ciclo | o comando de status |
| Um contato reclama que ninguém respondeu e ele não apareceu no resumo | confira se ele estava no registro ou na pasta de entrada |

## 2. Causas comuns e o que fazer

| Causa | O que fazer |
|---|---|
| Computador desligado ou app fechado na hora da tarefa (conferir na configuração da conta se a tarefa depende disso) | Rodar o comando ou o ciclo à mão. Se acontece toda semana, mudar o horário da tarefa. |
| A tarefa perdeu acesso à pasta, ou o plugin não está instalado onde a tarefa roda | Abrir a tarefa, escolher a pasta de novo, conferir o plugin. Rodar uma vez na mão para testar. |
| Agente de plugin indisponível no ambiente (chat com Projeto) | Ciclo à mão, pela `rotina-comercial`. |
| Recurso de tarefas agendadas indisponível no plano | Comando ou ciclo à mão, com dono e horário fixos. |
| `contatos.csv` aberto e travado na planilha, ou salvo com outro nome | Fechar a planilha e rodar de novo. O nome é sempre `contatos.csv`. |
| Planilha salva pelo Excel (ponto e vírgula, acento, data DD/MM/AAAA) | O script lê. Se ele disser que faltam colunas, a primeira linha mudou: copie a de `docs/funil.md` do plugin. |
| Pasta de entrada vazia porque ninguém exportou as conversas | O ciclo roda só com o registro e diz isso. Combine quem solta as conversas na pasta, e quando. |
| Conector de e-mail ou agenda desconectado | O resumo sai sem essa parte e diz isso. Reconectar (conferir na configuração da conta). |
| Ninguém estava para ler (folga, férias, audiência longe) | O `substituto` da ficha lê. Sem substituto, o ciclo do dia seguinte lê desde a última rodada e cobre os dois dias. |

## 3. O plano combinado (preencher na configuração)

1. **Até [HORA]**, se não houver resumo do dia, [FUNÇÃO] roda `/motor-comercial:ciclo` ou o ciclo à mão (`assets/tarefa-agendada.md`, seções 2 e 3).
2. **Se nem isso for possível** (sem Claude, sem computador), [FUNÇÃO] abre a planilha e faz o mínimo, à mão, em 5 minutos:
   - lê a pasta de entrada e o canal procurando ameaça, violência, prisão e prazo de hoje ou amanhã, e liga para quem cuida da urgência;
   - filtra `primeira_resposta` vazia em `novo` e `triado`, ordena por `entrada` e responde os mais antigos, urgência alta primeiro;
   - filtra `data_proximo_passo` até hoje e faz ou remarca cada um;
   - confere a agenda do dia.
3. **No dia seguinte**, o ciclo lê desde a última rodada registrada e cobre os dias sem ciclo, inclusive fim de semana. O que venceu aparece como vencido.
4. **Registro:** o dia sem ciclo entra no registro de uso como `não rodou`, com a causa; o dia em que só o script rodou entra como `só o resumo`.
5. **Dois dias seguidos** sem ciclo: o dono da ficha da automação revisa o jeito de rodar (horário, pasta, plano, ou voltar ao ciclo à mão).

## 4. O que nunca fazer para compensar

- Mandar mensagem em lote para "pôr em dia" quem ficou sem resposta. Cada um recebe a resposta certa, pela triagem e pela biblioteca, e quem pediu para parar continua fora.
- Pular a separação de PESSOA AGORA para andar mais rápido.
- Apagar linha do registro para o resumo ficar menor.
- Mudar o prazo da ficha para que nada apareça como estourado. Prazo muda por decisão do escritório, com linha no histórico da ficha.
- Marcar o dia como rodado quando só o resumo saiu.
