# Texto da tarefa agendada, do ciclo à mão e do pedido de peça

Três jeitos de o ciclo jurídico rodar, e o formato do pedido que alguém solta na pasta de entrada. Preencha os colchetes com as fichas (a habilidade faz isso no modo configurar) e copie o bloco inteiro.

## 1. Tarefa agendada que chama o comando (Cowork ou Claude Code)

Onde colar: no recurso de tarefas agendadas do Claude, se a sua conta tiver. O nome do recurso, o lugar do botão, os horários possíveis, se a tarefa precisa do computador ligado e se ela enxerga a pasta mudam com o plano e a versão: **conferir na configuração da conta**. A tarefa precisa abrir a pasta de trabalho onde está `escritorio/` e ter o plugin motor-juridico instalado.

- **Nome da tarefa:** Ciclo jurídico
- **Quando:** dias úteis, às [HORA] (`horario_da_rotina_diaria`; sugestão: antes da primeira audiência do dia). Se quiser a segunda rodada, uma segunda tarefa depois do almoço.
- **Pasta:** a pasta de trabalho que contém `escritorio/`
- **Texto (copiar daqui para baixo):**

```
/motor-juridico:ciclo

Pasta: escritorio/, na pasta de trabalho desta tarefa.
Limites de etapa da ficha da automação: [EX.: em-analise 5, minuta 2, conferida 2, aprovada 1] dias úteis. Feriados: [LISTA OU "nenhum"].
Leia desde a última rodada do registro de uso (05-automacoes/ciclo-juridico/registro-de-uso.md). Todo arquivo que está em 07-operacao/juridico/entrada/ é novo, de qualquer data.
[APAGUE SE NÃO HOUVER CONECTOR] Conectores, só leitura: [E-MAIL], [PASTA DE ARQUIVOS]. Não responda, não mova, não apague.
Não escolha tese, não aprove, não assine, não protocole. Toda citação sai marcada até ser conferida. Minutas vão para a fila do advogado. ADVOGADO AGORA no topo do resumo.
Se o agente do plugin não estiver disponível, rode o mesmo ciclo pela habilidade rotina-juridica, modo "ciclo à mão", com a revisão pela tabela do revisor-juridico, e grave o resumo assim mesmo.
Ao terminar, acrescente a linha da rodada no registro de uso. Se algo falhar, escreva o erro em uma linha que a equipe entenda.
```

Depois de criar, rode a tarefa uma vez na mão (o recurso costuma ter "rodar agora"; conferir) e veja se apareceram o arquivo do dia em `07-operacao/juridico/rotina/` e a linha nova no registro de uso.

## 2. O comando, sem tarefa agendada

Quem tem o plugin no Cowork ou no Claude Code e prefere disparar à mão, todo dia no mesmo horário:

```
/motor-juridico:ciclo
```

## 3. Ciclo à mão (chat com Projeto, ou quando o agente falhou)

No chat com Projeto não há agente. Cole no começo do dia, na conversa do Projeto (com a pasta aberta, se houver):

```
Roda o ciclo jurídico de hoje à mão, pela rotina-juridica. Lê desde a última rodada do registro de uso. Primeiro ADVOGADO AGORA, depois os pedidos novos, as minutas das peças com tese definida, a conferência, a revisão e o resumo do dia. Não escolhe tese e não protocola nada.
```

### No chat, sem pasta aberta

Sem acesso a arquivos, o ciclo precisa do que chegou e do registro colados. Exporte a planilha de peças em CSV (ou copie as linhas) e cole junto:

```
Roda o ciclo jurídico de hoje, [DATA], à mão. Limites de etapa: [EX.: em-analise 5, minuta 2] dias úteis. A última rodada foi em [DATA E HORA]. Estes são os pedidos de peça que chegaram desde então:
[COLE OS PEDIDOS, ANONIMIZADOS]
Este é o registro de peças:
[COLE AS LINHAS DO PECAS.CSV, COM A PRIMEIRA LINHA]
Me devolve ADVOGADO AGORA, o que está parado, as citações e dados pendentes, as aprovadas sem protocolo, as linhas novas do registro e o resumo.
```

Guarde o resumo que voltar com o nome `AAAA-MM-DD.md` e anote a data e a hora da rodada, para a próxima saber desde quando ler.

## 4. O pedido de peça na pasta de entrada

Nome do arquivo: `AAAA-MM-DD-HHMM-<origem>.md` (por exemplo `2026-04-15-1010-controladoria.md`), em `escritorio/07-operacao/juridico/entrada/`. Uma peça por arquivo. Só o mínimo: o detalhe do caso fica nos documentos de `casos/<codigo>/` e no sistema do escritório.

```markdown
pedido: peça nova | documento novo para peça aberta | decisão do advogado
codigo_caso: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME OU INICIAIS]
area: [UMA DAS ÁREAS DA FICHA]
peca: [TIPO DA PEÇA, COM HÍFEN, EX.: replica]
origem: intimacao | consulta | passagem | advogado | lote
prazo_interno: AAAA-MM-DD (informado por quem pediu; a rotina não calcula prazo processual)
quem_pediu: [FUNÇÃO]
documentos: [ONDE ESTÃO, EX.: casos/C-AAAA-NNNN/documentos/ ou a pasta do sistema]
observacao: [UMA LINHA, SEM DADO SENSÍVEL]
```

O ciclo lê, cria ou atualiza a linha do `pecas.csv` e move o arquivo para `entrada/lidos/AAAA-MM-DD/`. Pedido sem `codigo_caso` ou sem `peca` não vira linha: vai para "o que não deu para fazer", com o nome do arquivo.
