# Quando o ciclo da controladoria não roda

Leia no modo configurar (para combinar o plano) e no modo "não rodou". Na controladoria, um ciclo que falha em silêncio custa prazo: a publicação disponibilizada no dia em que o ciclo parou só aparece quando alguém roda de novo, com dias já corridos. Um ciclo à mão feito todo dia é melhor do que uma tarefa que roda quatro dias em cinco.

## 1. Como perceber

| Sinal | Onde olhar |
|---|---|
| Não existe `07-operacao/controladoria/rotina/AAAA-MM-DD.md` de hoje até [HORA COMBINADA] | a pasta da rotina |
| O registro de uso não tem linha de hoje, ou tem `não rodou` | `05-automacoes/ciclo-da-controladoria/registro-de-uso.md` |
| O resumo diz "O ciclo não roda há mais de dois dias úteis" | "Desde a última rodada", no fim do resumo |
| PESSOA AGORA tem "captada com atraso" | o prazo já corria quando a publicação entrou: o ciclo, a busca ou a planilha falhou em algum dia |
| O resumo existe, mas "O que não deu para fazer" tem "DJEN não consultado" ou erro de planilha | o fim do resumo |
| O script parou com "ERRO:" (arquivo não encontrado, coluna faltando, registro de treino) | a mensagem do script |
| O `/motor-controladoria:status` mostra dois dias úteis sem ciclo | o comando de status |
| Alguém descobre uma intimação no painel que não estava no resumo | o registro dos painéis do dia foi feito? |

## 2. Causas comuns e o que fazer

| Causa | O que fazer |
|---|---|
| Computador desligado ou app fechado na hora da tarefa (conferir na configuração da conta se a tarefa depende disso) | Rodar o comando ou o ciclo à mão agora. Se acontece toda semana, mudar o horário da tarefa. |
| A tarefa perdeu acesso à pasta, ou o plugin não está instalado onde a tarefa roda | Abrir a tarefa, escolher a pasta de novo, conferir o plugin. Rodar uma vez na mão para testar. |
| Sem internet no ambiente: a busca no DJEN não roda | Exportar as publicações pela consulta pública do CNJ ou pelo e-mail do tribunal, soltar na entrada e rodar de novo. |
| Agente de plugin indisponível (chat com Projeto) | Ciclo à mão, pela `rotina-da-controladoria`, com a tabela do revisor. |
| `prazos.csv` ou `publicacoes.csv` aberto e travado na planilha, ou salvo com outro nome | Fechar a planilha e rodar de novo. Os nomes são sempre esses dois. |
| Planilha salva pelo Excel (ponto e vírgula, acento, data DD/MM/AAAA) | O script lê. Se disser que faltam colunas, a primeira linha mudou: copie a de `docs/prazos.md` do plugin. |
| Calendário do ano novo que ninguém montou | O resumo avisa em destaque. Montar pela `calendario-forense` antes de confiar no "próximo dia útil". |
| Ninguém abriu os painéis (férias, audiência fora) | O ciclo não substitui o painel. Quem cobre a ausência (`cobertura_de_ausencia` da ficha) abre e registra. |
| Ninguém para conferir (quem confere está fora) | Os prazos ficam `sugerido` e sobem em PESSOA AGORA quando chegam perto. A `cobertura-de-ausencia` (se instalada) define quem confere no período. |

## 3. O plano combinado (preencher na configuração)

1. **Até [HORA]**, se não houver resumo do dia, [FUNÇÃO] roda `/motor-controladoria:ciclo` ou o ciclo à mão (`assets/tarefa-agendada.md`, seções 2 e 3).
2. **Se nem isso for possível** (sem Claude, sem computador), [FUNÇÃO] abre a planilha e faz o mínimo, à mão, em 10 minutos:
   - filtra `data_seguranca` e `vencimento` até o próximo dia útil, em qualquer status, e avisa quem cumpre;
   - consulta o DJEN pela consulta pública do CNJ, pelas OABs da ficha, desde a última rodada, e anota as publicações novas;
   - abre os painéis dos sistemas e anota as intimações sem ciência.
3. **Na rodada seguinte**, o ciclo lê desde a última rodada registrada. O que já corria aparece como "captada com atraso" em PESSOA AGORA.
4. **Registro:** a rodada sem ciclo entra no registro de uso como `não rodou`, com a causa; a rodada em que só o script rodou entra como `só o resumo`.
5. **Dois dias úteis seguidos** sem ciclo: o dono da ficha da automação revisa o jeito de rodar.

## 4. O que nunca fazer para compensar

- Marcar prazo como `conferido` sem as duas conferências para "pôr em dia".
- Agendar prazo `sugerido` porque "está quase certo".
- Pular a conferência do calendário porque o resumo atrasou.
- Usar a data mais tarde quando havia dúvida, para ganhar tempo.
- Apagar linha do registro para o resumo ficar menor.
- Aumentar a janela de PESSOA AGORA ou tirar um critério para que nada apareça.
- Marcar a rodada como feita quando só o resumo saiu.
