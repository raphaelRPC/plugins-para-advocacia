# Quando o ciclo não roda

Leia no modo configurar (para combinar o plano) e no modo "não rodou". Um ciclo que roda quatro dias em cinco e ninguém percebe o quinto é pior do que um ciclo à mão feito todo dia: a equipe confia que alguém olhou a fila de peças.

## 1. Como perceber

| Sinal | Onde olhar |
|---|---|
| Não existe `07-operacao/juridico/rotina/AAAA-MM-DD.md` de hoje até [HORA COMBINADA] | a pasta da rotina |
| O registro de uso não tem linha de hoje, ou tem `não rodou` | `05-automacoes/ciclo-juridico/registro-de-uso.md` |
| O script avisa "o ciclo não roda desde" | os avisos no topo do resumo |
| O resumo existe, mas "O que não deu para fazer" tem erro de leitura | o fim do resumo |
| O script parou com "ERRO:" (arquivo não encontrado, coluna faltando, registro de treino) | a mensagem do script |
| O `/motor-juridico:status` mostra dois dias úteis sem ciclo | o comando de status |
| A advogada descobre uma peça com prazo interno amanhã que não estava no resumo | confira se o pedido chegou na entrada e virou linha no registro |

## 2. Causas comuns e o que fazer

| Causa | O que fazer |
|---|---|
| Computador desligado ou app fechado na hora da tarefa (conferir na configuração da conta se a tarefa depende disso) | Rodar o comando ou o ciclo à mão. Se acontece toda semana, mudar o horário da tarefa. |
| A tarefa perdeu acesso à pasta, ou o plugin não está instalado onde a tarefa roda | Abrir a tarefa, escolher a pasta de novo, conferir o plugin. Rodar uma vez na mão para testar. |
| Agente de plugin indisponível no ambiente (chat com Projeto) | Ciclo à mão, pela `rotina-juridica`, com a tabela do revisor. |
| `pecas.csv` aberto e travado na planilha, ou salvo com outro nome | Fechar a planilha e rodar de novo. O nome é sempre `pecas.csv`. |
| Planilha salva pelo Excel (ponto e vírgula, acento, data DD/MM/AAAA) | O script lê. Se disser que faltam colunas, a primeira linha mudou: copie a de `docs/producao.md` do plugin. |
| Pedido de peça que não chegou à entrada (ficou no e-mail, no grupo da equipe) | Combinar de novo quem solta o pedido na entrada, e quando. O ciclo não lê o que não está lá. |
| Habilidade que o agente chama não está instalada (edição essencial sem a `preparar-protocolo`, por exemplo) | O resumo diz o que não foi feito. A pessoa faz aquele passo à mão ou instala a edição seguinte. |
| Ninguém para ler (férias, audiência fora) | O `substituto` da ficha lê ADVOGADO AGORA. Sem substituto, o ciclo seguinte lê desde a última rodada e cobre os dias. |

## 3. O plano combinado (preencher na configuração)

1. **Até [HORA]**, se não houver resumo do dia, [FUNÇÃO] roda `/motor-juridico:ciclo` ou o ciclo à mão (`assets/tarefa-agendada.md`, seções 2 e 3).
2. **Se nem isso for possível** (sem Claude, sem computador), [FUNÇÃO] abre a planilha e faz o mínimo, à mão, em 5 minutos:
   - filtra `prazo_interno` até o próximo dia útil e etapa antes de `aprovada`, e avisa o advogado;
   - filtra `etapa = aprovada` e confere com quem protocola;
   - lê a pasta de entrada procurando pedido com prazo de hoje ou amanhã.
3. **No dia seguinte**, o ciclo lê desde a última rodada registrada. O que venceu aparece como vencido.
4. **Registro:** o dia sem ciclo entra no registro de uso como `não rodou`, com a causa; o dia em que só o script rodou entra como `só o resumo`.
5. **Dois dias úteis seguidos** sem ciclo: o dono da ficha da automação revisa o jeito de rodar.

## 4. O que nunca fazer para compensar

- Minutar em lote, sem tese definida, para "pôr em dia" as peças paradas.
- Pular a conferência de citações para a peça andar mais rápido.
- Mover uma peça para `aprovada` ou `protocolada` sem o advogado.
- Apagar linha do registro para o resumo ficar menor.
- Aumentar o limite de etapa para que nada apareça como parado. Limite muda por decisão do escritório, com linha no histórico da ficha da automação.
- Marcar o dia como rodado quando só o resumo saiu.
