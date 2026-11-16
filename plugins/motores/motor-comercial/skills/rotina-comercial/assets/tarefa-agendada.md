# Texto da tarefa agendada e do ciclo à mão

Três jeitos de o ciclo comercial rodar. Preencha os colchetes com as fichas (a habilidade faz isso no modo configurar) e copie o bloco inteiro.

## 1. Tarefa agendada que chama o comando (Cowork ou Claude Code)

Onde colar: no recurso de tarefas agendadas do Claude, se a sua conta tiver. O nome do recurso, o lugar do botão, os horários possíveis, se a tarefa precisa do computador ligado e se ela enxerga a pasta mudam com o plano e a versão: **conferir na configuração da conta**. A tarefa precisa abrir a pasta de trabalho onde está `escritorio/` e ter o plugin motor-comercial instalado.

- **Nome da tarefa:** Ciclo comercial
- **Quando:** dias úteis, às [HORA] (`horario_da_rotina_diaria`; sugestão: 30 minutos antes do início do atendimento)
- **Pasta:** a pasta de trabalho que contém `escritorio/`
- **Texto (copiar daqui para baixo):**

```
/motor-comercial:ciclo

Pasta: escritorio/, na pasta de trabalho desta tarefa.
Critérios da ficha: expediente [HH:MM-HH:MM]; primeira resposta ao contato novo em [N] horas úteis; régua de quem não agendou em [EX.: 2, 7 e 15] dias corridos; proposta parada com [N] dias corridos; feriados [LISTA OU "nenhum"].
Leia desde a última rodada do registro de uso (05-automacoes/ciclo-comercial/registro-de-uso.md), inclusive sábado, domingo e feriado.
[APAGUE SE NÃO HOUVER CONECTOR] Conectores, só leitura: [E-MAIL], [AGENDA]. Não responda, não arquive, não marque como lido, não crie nem mude compromisso.
Não envie nada a ninguém. Rascunhos vão para a fila. PESSOA AGORA no topo do resumo.
Se o agente do plugin não estiver disponível, rode o mesmo ciclo pela habilidade rotina-comercial, modo "ciclo à mão", e grave o resumo assim mesmo.
Ao terminar, acrescente a linha da rodada no registro de uso. Se algo falhar, escreva o erro em uma linha que a equipe entenda.
```

Depois de criar, rode a tarefa uma vez na mão (o recurso costuma ter "rodar agora"; conferir) e veja se apareceram o arquivo do dia em `07-operacao/comercial/rotina/` e a linha nova no registro de uso.

## 2. O comando, sem tarefa agendada

Quem tem o plugin no Cowork ou no Claude Code e prefere disparar à mão, todo dia no mesmo horário:

```
/motor-comercial:ciclo
```

## 3. Ciclo à mão (chat com Projeto, ou quando o agente falhou)

No chat com Projeto não há agente. Cole no começo do dia, na conversa do Projeto (com a pasta aberta, se houver):

```
Roda o ciclo comercial de hoje à mão, pela rotina-comercial. Lê desde a última rodada do registro de uso. Primeiro PESSOA AGORA, depois a triagem do que chegou, os rascunhos para eu aprovar e o resumo do dia. Não envia nada.
```

### No chat, sem pasta aberta

Sem acesso a arquivos, o ciclo precisa do que chegou e do registro colados. Exporte a planilha de contatos em CSV (ou copie as linhas) e cole junto:

```
Roda o ciclo comercial de hoje, [DATA], à mão. Critérios: expediente [HH:MM-HH:MM]; contato novo em [N] horas úteis; régua de quem não agendou em [N, N, N] dias corridos; proposta parada com [N] dias. A última rodada foi em [DATA E HORA]. Estas são as mensagens que chegaram desde então:
[COLE AS MENSAGENS, ANONIMIZADAS]
Este é o registro:
[COLE AS LINHAS DO CONTATOS.CSV, COM A PRIMEIRA LINHA]
Me devolve PESSOA AGORA, os rascunhos para aprovar, as linhas novas do registro e o resumo.
```

Guarde o resumo que voltar com o nome `AAAA-MM-DD.md` e anote a data e a hora da rodada, para a próxima saber desde quando ler.
