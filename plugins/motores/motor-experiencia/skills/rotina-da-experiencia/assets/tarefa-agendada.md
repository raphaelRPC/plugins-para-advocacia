# Tarefa agendada, pedido de toda manhã e chat sem pasta

Três jeitos de o ciclo rodar. A habilidade preenche os colchetes com as fichas no modo configurar.

## 1. Tarefa agendada (Cowork ou Claude Code)

Onde colar: no recurso de tarefas agendadas do Claude, se a conta tiver. O nome do recurso, os horários possíveis e se ele precisa do computador ligado mudam com o plano e a versão: conferir na configuração da conta. A tarefa precisa ter acesso à pasta de trabalho onde está `escritorio/`.

- **Nome da tarefa:** Ciclo da experiência
- **Quando:** dias úteis, às [HORA] (sugestão: 30 minutos antes de abrir o WhatsApp)
- **Pasta:** a pasta de trabalho que contém `escritorio/`
- **Texto (copiar daqui para baixo):**

```
/motor-experiencia:ciclo

Rode o ciclo do dia da experiência do cliente nesta pasta, com a data de hoje.
Critérios da ficha da automação (05-automacoes/ciclo-da-experiencia/ficha.md): máximo sem notícia [N] dias; documentos [N] dias; resumo no dia [N]; feriados [LISTA OU "nenhum"].
Não envie nada a ninguém. Grave a fila, o resumo do dia em 07-operacao/experiencia/rotina/ e a linha do registro de uso.
Se o agente de suporte não estiver disponível, rode a habilidade rotina-da-experiencia no modo rodar.
```

Depois de criar, rode a tarefa uma vez na mão (o recurso costuma ter "rodar agora"; conferir) e veja se o arquivo do dia apareceu em `07-operacao/experiencia/rotina/`.

## 2. Pedido de toda manhã (sem tarefa agendada)

Para quem não tem tarefa agendada e para o dia em que ela não rodou. Cole no Claude, na pasta de trabalho, no começo do dia:

```
Roda o ciclo da experiência de hoje (/motor-experiencia:ciclo, ou a rotina-da-experiencia no modo rodar). Me mostra PESSOA AGORA primeiro, depois a fila para aprovar. Grava o resumo do dia e a linha do registro de uso.
```

## 3. No chat com Projeto, sem pasta aberta

Não há agente nem script. Exporte a carteira em CSV (ou copie as linhas da planilha) e cole junto com o pedido:

```
Ciclo da experiência à mão, data de hoje [AAAA-MM-DD]. Use a habilidade rotina-da-experiencia, regras da seção 4. Máximo sem notícia [N] dias. Segue a carteira:
[COLE AQUI AS LINHAS, COM A PRIMEIRA LINHA DE TÍTULOS]
Segue também o que chegou de clientes desde ontem:
[COLE AQUI AS MENSAGENS, SEM CPF, TELEFONE OU NÚMERO DE PROCESSO]
```

A resposta vem no chat: PESSOA AGORA, o retrato da carteira e os rascunhos, cada um com quem lê antes de enviar. As linhas da carteira que mudaram vêm prontas para colar na planilha.
