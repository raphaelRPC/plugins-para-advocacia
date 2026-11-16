# A carteira de clientes e a jornada

Depois do contrato, o cliente entra na carteira. Ali o escritório enxerga, cliente por cliente, há quanto tempo ele não tem notícia, o que está para acontecer, o que falta ele mandar e como ele está se sentindo. A carteira é o que permite à rotina dizer "quatro clientes sem notícia há mais de 30 dias" antes de algum deles perguntar.

## A jornada

| Momento | O que o cliente vive | O que o escritório faz | Habilidade |
|---|---|---|---|
| Entrada | Acabou de assinar, ainda inseguro | Boas-vindas, quem cuida, como e quando vai ter notícia | `boas-vindas-do-cliente` |
| Documentos | Não sabe onde conseguir, manda pela metade | Lista com onde conseguir, controle do que chegou | `checklist-de-documentos` |
| Espera | O processo some da vista dele | Régua: aviso de movimentação relevante, resumo mensal, nunca mais que o máximo sem notícia | `jornada-do-cliente`, `status-para-o-cliente`, `resumo-mensal-do-caso`, `pagina-do-caso` |
| Pesquisa sozinho | Lê "conclusos para despacho" no site, pergunta a uma IA | Explica antes, acolhe e corrige quando ele traz a resposta pronta | `cliente-com-ia` |
| Compromisso | Audiência, perícia, reunião: ansiedade | Lembrete e preparação | `preparar-o-cliente` |
| Notícia | Decisão boa ou ruim | Boa: mensagem clara. Ruim: ligação do advogado primeiro | `status-para-o-cliente` |
| Problema | Demora, falha de comunicação, insatisfação | Uma pessoa assume, escuta, corrige, registra | `reclamacao-e-recuperacao` |
| Encerramento | O caso acabou, ganhou ou perdeu | Prestação de contas, o que muda na vida dele, documentos | `encerramento-do-caso` |
| Depois | Vida que segue | Pesquisa, contato sem oferta, porta aberta | `pesquisa-de-satisfacao`, `relacionamento-depois-do-caso` |

O cliente de hoje tem acesso ao processo pela internet e faz perguntas a uma IA antes de perguntar ao advogado. A régua existe para o escritório chegar antes: quando o escritório avisa, explica e mostra o que fez, a pergunta perde o motivo e a percepção de valor sobe.

## O arquivo `carteira.csv`

Fica em `escritorio/07-operacao/experiencia/carteira.csv`, separado por vírgula, com esta primeira linha:

```
codigo,nome_curto,area,tipo_de_caso,responsavel,inicio,fase,ultimo_contato,ultimo_contato_tipo,proximo_contato,motivo_proximo_contato,proximo_compromisso,data_compromisso,documentos_pendentes,humor,reclamacao_aberta,resumo_mensal,pagina_do_caso,satisfacao,pediu_para_nao_receber,encerrado_em,atualizado_em
```

| Coluna | O que vai | Exemplo |
|---|---|---|
| `codigo` | O mesmo código do comercial (C-AAAA-NNNN). Cliente que chegou antes do registro ganha um código novo | C-2026-0001 |
| `nome_curto` | Primeiro nome ou iniciais | Marta |
| `area` | Área da ficha do escritório | previdenciario |
| `tipo_de_caso` | Até 5 palavras, sem dado sensível | restabelecimento de auxílio |
| `responsavel` | Função ou primeiro nome de quem cuida | advogada |
| `inicio` | Data do contrato, AAAA-MM-DD | 2026-03-20 |
| `fase` | `entrada`, `documentos`, `preparacao`, `protocolado`, `aguardando`, `audiencia-pericia`, `decisao`, `recurso`, `cumprimento`, `encerramento`, `encerrado` | aguardando |
| `ultimo_contato` | Data do último contato com o cliente que informou algo (não conta "ok" nem figurinha) | 2026-04-02 |
| `ultimo_contato_tipo` | `mensagem`, `ligacao`, `reuniao`, `resumo`, `pagina` | resumo |
| `proximo_contato` | Data em que o escritório deve falar de novo, pela régua | 2026-05-02 |
| `motivo_proximo_contato` | `boas-vindas`, `ligacao-pendente` (uma pessoa precisa ligar, nada combinado ainda), `resumo-mensal`, `maximo-sem-noticia`, `compromisso`, `documento`, `retorno-combinado`, `pesquisa`, `depois-do-caso` | resumo-mensal |
| `proximo_compromisso` | `audiencia`, `pericia`, `reuniao`, `prazo-do-cliente` ou vazio | pericia |
| `data_compromisso` | AAAA-MM-DD | 2026-04-15 |
| `documentos_pendentes` | Quantos documentos faltam (o detalhe fica em `clientes/<codigo>/documentos.md`) | 2 |
| `humor` | `tranquilo`, `ansioso`, `insatisfeito` ou `a-confirmar` (a última leitura de quem falou com ele) | ansioso |
| `reclamacao_aberta` | `sim` ou `nao` | nao |
| `resumo_mensal` | `sim` ou `nao` (se o cliente recebe) | sim |
| `pagina_do_caso` | `link`, `pdf`, `os-dois` ou `nao` | pdf |
| `satisfacao` | A última nota da pesquisa, de 0 a 10, ou vazio | 9 |
| `pediu_para_nao_receber` | `sim` ou `nao` (resumo e mensagens de rotina; o essencial do caso continua) | nao |
| `encerrado_em` | AAAA-MM-DD, quando encerrar | |
| `atualizado_em` | AAAA-MM-DD | 2026-04-02 |

## Regras da carteira

1. **Sem notícia** quer dizer `ultimo_contato` mais antigo que o `maximo_sem_noticia` da ficha. Conta em dias corridos.
2. **A fase é do jurídico.** Quem conduz o caso atualiza. A IA sugere a fase a partir da movimentação colada e pede confirmação.
3. **Humor não é diagnóstico.** É a leitura de quem falou com o cliente, em uma palavra. Cliente `insatisfeito` ou com `reclamacao_aberta = sim` aparece no topo da rotina.
4. **Mínimo de dados.** Nada de CPF, número do processo, valor da causa, endereço ou dado de saúde. O detalhe do caso fica no sistema do escritório.
5. **Uma linha por cliente e caso.** Cliente com dois casos tem duas linhas, com o mesmo código e o sufixo `-2`.
6. **`pediu_para_nao_receber = sim`** suspende resumo mensal e mensagens de rotina. Notícia relevante do caso continua, porque é dever do advogado informar.
7. **Quem entra:** a `passagem-para-o-caso` do motor-comercial (se instalado) cria a linha. Sem ela, a `boas-vindas-do-cliente` cria. Cliente antigo entra pela importação descrita na `rotina-da-experiencia`.
8. **Treino não entra.** Casos fictícios vão para `escritorio/07-operacao/_treino/experiencia/`.
9. **Os scripts** leem também a planilha salva pelo Excel (ponto e vírgula, com ou sem BOM).
10. **O histórico do cliente** (`clientes/<codigo>/historico.md`) é uma tabela de quatro colunas (`Data e hora | Canal | Quem falou | O que foi dito`), uma linha por contato, o que foi dito em uma frase, sem dado sensível. É dali que sai o `ultimo_contato`. O canal `trabalho-do-escritorio` registra o que o escritório fez sem falar com o cliente (petição protocolada, cálculo conferido, documento pedido): alimenta o resumo mensal e a página do caso, mas nunca muda o `ultimo_contato`.
11. **`documentos_pendentes`** conta os itens do `clientes/<codigo>/documentos.md` com situação `pendente`, `chegou-com-problema` ou `nao-existe`.
