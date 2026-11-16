# O agente do ciclo e a fila de aprovação

Cada plugin traz um **agente** que roda o ciclo do dia sozinho e um **revisor** que confere tudo o que o agente escreveu. O agente prepara. O revisor barra o que não pode sair. Uma pessoa aprova na fila. Nada vai para cliente sem essa pessoa.

Quem orquestra é o comando `ciclo`: ele chama o agente, depois chama o revisor sobre os rascunhos que o agente gravou, e só então mostra o resultado. Um agente não chama o outro.

| Plugin | Agente do ciclo | Revisor | Comando que roda o ciclo |
|---|---|---|---|
| motor-comercial | `agente-comercial` | `revisor-comercial` | `/motor-comercial:ciclo` |
| motor-experiencia | `agente-de-suporte` | `revisor-de-suporte` | `/motor-experiencia:ciclo` |
| motor-juridico | `agente-juridico` | `revisor-juridico` | `/motor-juridico:ciclo` |
| motor-controladoria | `agente-de-controladoria` | `revisor-de-controladoria` | `/motor-controladoria:ciclo` |

## Onde o agente roda

Nos arquivos de agente e de comando, `${CLAUDE_PLUGIN_ROOT}` é a pasta do plugin. Se a variável não aparecer expandida, a pasta do plugin é a que contém a pasta `agents/` onde o arquivo do agente está.

- **Cowork e Claude Code:** o comando `ciclo` chama o agente do plugin. Pode rodar todo dia, sozinho, por uma tarefa agendada que chama o comando (texto pronto na habilidade de rotina do plugin). Conferir na configuração da conta se tarefas agendadas e agentes de plugin estão disponíveis.
- **Chat com Projeto:** não há agente. A habilidade de rotina (`rotina-comercial`, `rotina-da-experiencia`, `rotina-juridica` ou `rotina-da-controladoria`) faz o mesmo ciclo, passo a passo, quando o advogado pede.

## O ciclo

Rode o ciclo no começo do expediente e de novo depois do almoço (duas tarefas agendadas, ou duas vezes à mão). O ciclo é um lote: ele não substitui olhar as mensagens ao longo do dia. O que chega com sinal de urgência entre um ciclo e outro é triado na hora, a pedido, pela habilidade de triagem do plugin.

1. **Coletar.** Lê o que chegou desde a última rodada (a data fica no registro de uso):
   - a pasta `07-operacao/<plugin>/entrada/`, onde a pessoa solta as conversas exportadas, os e-mails salvos ou um texto colado (formato e destino na seção "A pasta de entrada");
   - os conectores que a ficha do escritório lista (e-mail, agenda), só para leitura;
   - os registros (`contatos.csv`, `carteira.csv`) e os arquivos do dia.
2. **Separar o que para tudo.** Sinal de violência, ameaça, risco à vida, prisão, criança em risco, prazo de hoje ou amanhã: o agente não escreve nada para o cliente, põe no topo do resumo como "PESSOA AGORA" (no motor-juridico, "ADVOGADO AGORA") e segue com o resto.
3. **Fazer o trabalho S.** Classificar, preencher as linhas do registro (só as etapas que a IA pode mover), calcular prazos e pendências.
4. **Rascunhar o trabalho A.** Cada mensagem ou documento para cliente vira um arquivo na fila, com `revisor: pendente`.
5. **Revisar** (o comando `ciclo` chama o revisor depois do agente). O revisor lê cada rascunho com `revisor: pendente` contra as regras (`regras.md`), as fichas, o nicho e os aprendizados, e grava no próprio arquivo: `revisor: ok`, `revisor: ajustado: <o que mudou>` (com o texto novo), `revisor: conferir: <o que o advogado precisa conferir>` (vai para a fila, mas só pode ser aprovado depois da conferência) ou `status: bloqueado` com `revisor: bloqueado: <motivo>` (o item não aparece para aprovar e entra no resumo em "PESSOA AGORA" ou "PARA DECIDIR"). Nada é apagado.
6. **Resumir.** Depois da revisão, o comando `ciclo` fecha o resumo que o agente começou: acrescenta a linha "Revisão: N ok, N ajustados, N para conferir, N bloqueados" e põe cada bloqueado em "PESSOA AGORA" ou "PARA DECIDIR", com o motivo do revisor. O resumo fica em `07-operacao/<plugin>/rotina/AAAA-MM-DD.md`: pessoa agora (no jurídico, advogado agora), para decidir, fila para aprovar, registro atualizado, o que não deu para fazer e por quê.
7. **Registrar.** Uma linha no registro de uso da automação (`05-automacoes/ciclo-<plugin>/registro-de-uso.md`): data, hora, o que leu, quantos itens, quantos bloqueados, erros.

## A pasta de entrada

- **Nome do arquivo:** `AAAA-MM-DD-HHMM-<origem>.txt` ou `.md` (por exemplo `2026-04-10-0805-whatsapp.txt`). Texto puro: conversa exportada, e-mail copiado, anotação de ligação. Áudio entra transcrito.
- **Novo** é o arquivo que ainda está em `entrada/`, de qualquer data. O limite de tempo da última rodada vale só para conectores e registros. Depois de lido, o agente move para `entrada/lidos/AAAA-MM-DD/` e registra no registro de uso. Mover não é apagar.
- **Dado bruto.** O que está em `entrada/` e em `lidos/` pode ter dado de cliente. O resumo do dia lembra a pessoa de apagar `lidos/` com mais de 7 dias (ou o prazo que a regra de uso de IA do escritório definir). Quem apaga é a pessoa.
- **Primeiro ciclo:** sem `contatos.csv`, o agente comercial cria o arquivo só com a linha de títulos de `funil.md` e segue. Sem `carteira.csv`, o agente de suporte para e avisa que a carteira precisa ser importada pela `rotina-da-experiencia`.

## A fila de aprovação

Cada rascunho é um arquivo em `07-operacao/<plugin>/fila/AAAA-MM-DD/NN-<codigo>-<tipo>.md` (no motor-juridico, o que não é de um caso, como pesquisa para a base ou aviso de precedente, usa `NN-base-<tema>.md`; no motor-controladoria, o item de um grupo da triagem em massa usa `NN-grupo-gNN-providencia.md` e o aviso sem caso `NN-aviso-<assunto>.md`):

```markdown
---
status: pendente          # pendente | aprovado | enviado | descartado | bloqueado
codigo: C-2026-0001
para: Marta (contato novo)
canal: whatsapp
tipo: convite-consulta-paga  # a chave do modelo na biblioteca (no jurídico, a peça)
item: minuta              # só no motor-juridico: minuta (para aprovar) | interno (dossiê, estratégia: para ler e decidir)
                          # no motor-controladoria: conferir-prazo | decidir-providencia | aviso
motivo: triagem 09h10, previdenciário, benefício cortado
revisor: pendente         # pendente | ok | ajustado: o que mudou | conferir: o que conferir | bloqueado: motivo
prazo: até 11h10 (primeira resposta da ficha)
antes_de_enviar:          # conferências internas, uma por linha; nunca vão no texto
  - conferir com a advogada o horário de quinta
---

[o texto pronto para copiar]
```

- **Aprovar:** a pessoa lê, ajusta se quiser e muda o status para `aprovado` (ou usa o comando `fila` do plugin, que mostra os pendentes um por um e grava a decisão).
- **Enviar:** quem envia é a pessoa, pelo canal oficial. Com conector de e-mail, o agente pode deixar o rascunho na caixa de rascunhos, nunca enviar. Depois de enviado, o status vira `enviado` e o registro é atualizado (`primeira_resposta`, histórico do cliente).
- **Descartar:** status `descartado` e o campo `motivo_descarte: <uma linha>` no cabeçalho. Se o motivo é uma correção ("nunca mandamos isso para quem é idoso"), vira proposta de aprendizado.
- Rascunho com `revisor: pendente` não pode ser aprovado: passa pelo revisor antes. Com `revisor: conferir`, a pessoa confere o ponto indicado antes de aprovar. Com `status: bloqueado`, não aparece para aprovar.
- **O que conta como contato com o cliente.** Depois de enviado, só atualiza o `ultimo_contato` da carteira o que informou algo do caso (status, resumo, página, ligação, reunião, boas-vindas). Resposta-ponte ("recebi, te retorno até"), cortesia, lembrete de documento e pesquisa entram no histórico, mas não zeram o "sem notícia". A linha de trabalho do escritório (canal `trabalho-do-escritorio`) também não.
- **Bloqueado:** o item fica no resumo do dia, em PESSOA AGORA ou PARA DECIDIR (no motor-juridico, ADVOGADO AGORA ou PARA DECIDIR). Quando o motivo for resolvido (o campo foi preenchido, a advogada decidiu), a pessoa pede pelo comando `fila` para voltar o item a `pendente`, com `revisor: pendente`, ou descarta.
- **Ajustado na fila:** texto que a pessoa mudou volta a passar pela tabela do revisor antes de ser aprovado.
- **Descartado:** a linha do registro também muda. O comando `fila` pergunta o que acontece com o contato (outro rascunho, ligação, encaminhado, perdido) e atualiza `proximo_passo`, com o ok.
- **Campos do envio** (`{...}`): a pessoa preenche antes de enviar; a fila não deixa marcar `enviado` com chaves no texto.
- **PESSOA AGORA também sai da lista** (no motor-juridico, ADVOGADO AGORA, com as decisões de tese e de caso; o comando `fila` do jurídico diz como). Depois que a pessoa falou com o contato ou cliente, o comando `fila` pergunta, item por item do último resumo: "Já falou? O que ficou combinado?". Com a resposta, grava a hora do contato (`primeira_resposta` no comercial, `ultimo_contato` na experiência quando informou algo do caso), no comercial troca o `proximo_passo` que começa com `pessoa agora:` ou `pessoa liga:` pelo combinado, com data; na experiência grava `proximo_contato` com a data combinada e `motivo_proximo_contato = retorno-combinado`; e registra no histórico. Sem isso, o item continua no topo do resumo seguinte.
- Rascunho `pendente` há mais de um dia útil aparece no topo do resumo seguinte.

## O que o agente nunca faz

1. Enviar mensagem, e-mail ou documento para cliente.
2. Mover contato ou cliente para `fechado`, `perdido`, `recusado`, `encaminhado`, `sem-caso` ou `encerrado`.
3. Escrever para quem está em parada imediata ou pediu para parar.
4. Ler ou gravar fora de `escritorio/` e dos conectores que a ficha lista.
5. Decidir valor, estratégia, ou se vale entrar com a ação.
6. Apagar arquivo. Quando algo está errado, marca e avisa.

## Quando o ciclo falha

O agente registra o erro no registro de uso e no resumo, em uma linha que a pessoa entende ("não achei o contatos.csv; o ciclo de hoje não atualizou o funil"). Se o ciclo não rodou, a habilidade de rotina do plugin faz o mesmo à mão. Dois dias seguidos sem ciclo aparecem no comando `status`.
