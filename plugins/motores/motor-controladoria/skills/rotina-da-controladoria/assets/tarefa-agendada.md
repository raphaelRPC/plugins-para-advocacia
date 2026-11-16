# Texto das tarefas agendadas e do ciclo à mão

Três jeitos de o ciclo da controladoria rodar. Preencha os colchetes com as fichas (a habilidade faz isso no modo configurar) e copie o bloco inteiro. O ciclo da controladoria roda **duas vezes por dia útil**: de manhã, antes de a equipe começar, e depois do almoço, porque publicação e intimação de portal chegam o dia todo.

## 1. Duas tarefas agendadas que chamam o comando (Cowork ou Claude Code)

Onde colar: no recurso de tarefas agendadas do Claude, se a sua conta tiver. O nome do recurso, o lugar do botão, os horários possíveis, se a tarefa precisa do computador ligado e se ela enxerga a pasta mudam com o plano e a versão: **conferir na configuração da conta**. A tarefa precisa abrir a pasta de trabalho onde está `escritorio/` e ter o plugin motor-controladoria instalado.

Crie duas tarefas iguais, mudando só o nome e a hora:

- **Nome:** Ciclo da controladoria · manhã | Ciclo da controladoria · tarde
- **Quando:** dias úteis, às [HORA DA MANHÃ] e às [HORA DA TARDE] (campo `horario_da_captacao` da ficha da controladoria; exemplo: 08h e 14h). A da manhã termina antes do `horario_da_rotina_diaria` da ficha do escritório.
- **Pasta:** a pasta de trabalho que contém `escritorio/`
- **Texto (copiar daqui para baixo):**

```
/motor-controladoria:ciclo

Pasta: escritorio/, na pasta de trabalho desta tarefa.
Leia desde a última rodada do registro de uso (05-automacoes/ciclo-da-controladoria/registro-de-uso.md). Todo arquivo que está em 07-operacao/controladoria/entrada/ é novo, de qualquer data.
OABs: [OABS DA FICHA]. Tribunais: [TRIBUNAIS DA FICHA]. Dias de segurança: [N] dias úteis.
[APAGUE SE NÃO HOUVER CONECTOR] Conectores, só leitura: [E-MAIL DO TRIBUNAL], [AGENDA]. Não responda, não mova, não apague.
A IA capta e calcula, mas não interpreta. Nenhum prazo vira conferido, cumprido, perdido ou cancelado sem uma pessoa. Nenhum nome em conferido_por. Nada sugerido entra na agenda. Nunca entre em painel de tribunal nem use senha, certificado ou token.
Prazo com data de segurança ou fatal hoje ou no próximo dia útil vai para PESSOA AGORA, no topo do resumo, em qualquer status.
Se o agente do plugin não estiver disponível, rode o mesmo ciclo pela habilidade rotina-da-controladoria, modo "ciclo à mão", com a revisão pela tabela do revisor-de-controladoria, e grave o resumo assim mesmo.
Ao terminar, acrescente a linha da rodada no registro de uso. Se algo falhar, escreva o erro em uma linha que a equipe entenda.
```

Depois de criar, rode cada tarefa uma vez na mão (o recurso costuma ter "rodar agora"; conferir) e veja se apareceram o arquivo do dia em `07-operacao/controladoria/rotina/` e a linha nova no registro de uso.

## 2. O comando, sem tarefa agendada

Quem tem o plugin no Cowork ou no Claude Code e prefere disparar à mão, duas vezes por dia, no mesmo horário:

```
/motor-controladoria:ciclo
```

## 3. Ciclo à mão (chat com Projeto, ou quando o agente falhou)

No chat com Projeto não há agente. Cole no começo do expediente e depois do almoço, na conversa do Projeto (com a pasta aberta, se houver):

```
Roda o ciclo da controladoria de hoje à mão, pela rotina-da-controladoria. Lê desde a última rodada do registro de uso. Primeiro PESSOA AGORA do último resumo, depois a captação, a triagem, a conta dos prazos sugeridos, a revisão pela tabela do revisor, a fila de conferência e o resumo do dia. Não confirma prazo, não agenda o que não foi conferido e não decide providência.
```

### No chat, sem pasta aberta

Sem acesso a arquivos, o ciclo precisa do que chegou e dos registros colados. Exporte as planilhas em CSV (ou copie as linhas) e cole junto. Não cole senha, certificado, token nem print de painel com dado de outro processo.

```
Roda o ciclo da controladoria de hoje, [DATA], à mão. A última rodada foi em [DATA E HORA]. Tribunais: [TRIBUNAIS]. Dias de segurança: [N] dias úteis.
Estas são as publicações que chegaram desde então (planilha, e-mail do tribunal ou o que a pessoa anotou do painel):
[COLE AQUI, SEM CPF E SEM DADO DE SAÚDE]
Este é o registro de prazos:
[COLE AS LINHAS DO PRAZOS.CSV, COM A LINHA DE TÍTULOS]
Este é o calendário dos tribunais (ou diga "sem calendário"):
[COLE A TABELA]
Me devolve PESSOA AGORA, os prazos sugeridos com a conta passo a passo e o trecho literal, o que espera a dupla conferência, as publicações sem caso, as audiências e perícias, as linhas novas dos registros e o resumo.
```

Guarde o resumo que voltar com o nome `AAAA-MM-DD.md` e anote a data e a hora da rodada, para a próxima saber desde quando ler. No chat sem código, a conta do prazo é feita passo a passo na conversa, e a dupla conferência vale do mesmo jeito.

## 4. O que a pessoa solta na pasta de entrada

Em `escritorio/07-operacao/controladoria/entrada/`, com nome `AAAA-MM-DD-HHMM-<origem>.<extensão>` (por exemplo `2026-04-14-0805-email-trt3.eml` ou `2026-04-14-1310-planilha.csv`):

- e-mail do tribunal salvo (.eml ou texto copiado);
- planilha de publicações (csv ou xlsx) ou exportação do sistema jurídico;
- qualquer texto de intimação que alguém recebeu fora das fontes de sempre.

O formato de cada um é o da `captar-publicacoes` (se instalada). O que a pessoa viu nos painéis não vai para a entrada: vai para o registro dos painéis (`07-operacao/controladoria/paineis/AAAA-MM-DD.md`, da `paineis-dos-sistemas`, se instalada). O ciclo lê a entrada e move o arquivo para `entrada/lidos/AAAA-MM-DD/`. Mover não é apagar.
