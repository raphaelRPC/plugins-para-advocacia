# Linha de status (Claude Code)

A linha de status é a faixa de informação no rodapé do Claude Code. O Claude Code entrega a ela, a cada resposta, o percentual usado da sessão de 5 horas e da semana, com o horário em que cada um zera (campo `rate_limits`, documentado em code.claude.com/docs/en/statusline). Esse é o único lugar onde um plugin recebe o percentual oficial do plano.

## Limites

- Só nos planos Pro e Max, e só depois da primeira resposta de cada conversa.
- Um plugin não liga a linha de status sozinho: ela fica no `~/.claude/settings.json` do advogado. Por isso o comando pede o "sim" e guarda uma cópia (`settings.json.antes-da-linha-de-status`).
- Não existe no Cowork nem no aplicativo. Lá, o percentual oficial está em Configurações > Uso.
- O percentual é do plano inteiro: inclui o que ele usou no aplicativo, no Cowork e em outras conversas no mesmo período.

## O que o comando faz

`uso.py configurar-linha-de-status --aplicar`:
1. copia o `uso.py` para `~/.marketing-juridico/uso/uso.py` (o endereço do plugin muda a cada atualização; a cópia fica fixa);
2. grava em `settings.json` o `statusLine` com o Python atual e esse arquivo;
3. a cada resposta, imprime `Sessão 34% (zera 15h20) · Semana 12% (zera sex 09h00) · Conversa 41% cheia` e anota em `~/.marketing-juridico/uso/limites.jsonl` quando o percentual muda (com o identificador da conversa).

"Conversa 41% cheia" é quanto da janela de contexto (o tanto de texto que o Claude consegue considerar de uma vez) a conversa já ocupa. Perto de cheia, vale começar uma conversa nova pelo andamento.

## Desfazer

Copiar `settings.json.antes-da-linha-de-status` de volta para `settings.json`, ou apagar o bloco `statusLine`. Com o "sim" dele.

## Depois de atualizar o plugin

Se a linha mudar de formato numa versão nova, rode `--aplicar` de novo para atualizar a cópia.
