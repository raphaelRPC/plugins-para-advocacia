# Importar a carteira atual do escritório

Leia no modo importar. O objetivo é trazer para a `carteira.csv` todos os clientes com caso em andamento, com o mínimo de dados, para o ciclo começar a enxergar quem está sem notícia já no primeiro dia. Formato da carteira: `docs/carteira.md` do plugin.

## 1. De onde vêm os clientes

| O escritório tem | Como importar |
|---|---|
| Planilha (Excel, Google Planilhas) | Exportar em CSV. O script lê vírgula ou ponto e vírgula, com ou sem BOM |
| Sistema jurídico | Exportar a lista de processos ativos em CSV ou planilha, só com as colunas do mínimo |
| Só o WhatsApp e a memória | Lista colada no chat, uma linha por cliente (seção 4) |

Pergunte uma vez: "Quantos clientes ativos, mais ou menos?". Acima de 50, importe por área, uma de cada vez, e rode `--conferir` a cada lote.

## 2. O mínimo por cliente

| Coluna da carteira | Se não souber |
|---|---|
| `codigo` | Gerar (seção 3) |
| `nome_curto` | Iniciais |
| `area` | Uma das `areas` da ficha do escritório |
| `tipo_de_caso` | Até 5 palavras, sem dado sensível ("aposentadoria por idade", não "aposentadoria por câncer") |
| `responsavel` | Função ("advogada", "secretaria") |
| `fase` | Uma da lista de `docs/carteira.md`; na dúvida entre duas, a anterior, e a pessoa confirma depois |
| `ultimo_contato` | A data do último contato que informou algo do caso (status, resumo, ligação, reunião, boas-vindas). Um "ok", uma resposta-ponte, um lembrete de documento ou uma pesquisa não contam (`docs/agentes-e-fila.md`). Data aproximada ("começo do mês passado" vira o dia 1 daquele mês) vem com a nota "data aproximada" no histórico |

O resto (`inicio`, `proximo_compromisso`, `data_compromisso`, `documentos_pendentes`, `humor`, `resumo_mensal`, `pediu_para_nao_receber`) pode ficar vazio na importação. Duas perguntas valem a pena para todos de uma vez: "Algum cliente tem audiência, perícia ou reunião marcada nas próximas semanas?" e "Algum está insatisfeito ou reclamou recentemente?". As respostas entram em `data_compromisso` e `humor`.

## 3. Código de quem não tem

- Cliente que veio pelo motor-comercial mantém o código do `contatos.csv` (`C-AAAA-NNNN`).
- Cliente antigo ganha código novo: `C-` + o ano do contrato (ou o ano atual, se não souber) + o próximo número livre daquele ano.
- Antes de numerar, leia os códigos que já existem na `carteira.csv` e, se o motor-comercial estiver instalado, no `07-operacao/comercial/contatos.csv`. Nunca repita.
- Cliente com dois casos: duas linhas, o mesmo código, a segunda com o sufixo `-2`.

## 4. Lista colada

Peça neste formato, uma linha por cliente:

```
primeiro nome; área; tipo de caso; quem cuida; fase; último contato
```

Exemplo (Escritório Modelo, fictício):

```
Marta; previdenciário; restabelecimento de auxílio; advogada; aguardando; 05/03/2026
Renata; família; divórcio consensual; secretária; documentos; 01/04/2026
```

Linha incompleta: monte o que dá e marque o que falta na coluna de observação do quadro que você mostra, nunca dentro do csv.

## 5. Mapa das colunas (planilha)

Leia a primeira linha da planilha e mostre o mapa antes de converter:

| Coluna da planilha | Vai para | Observação |
|---|---|---|
| [NOME DA COLUNA] | [COLUNA DA CARTEIRA OU "não entra"] | [EX.: "tirar o sobrenome"] |

Não entram nunca: CPF, RG, número do processo, número de benefício, telefone, e-mail, endereço, valor da causa, honorários, dado de saúde, nome da outra parte. Se a planilha tem essas colunas, diga em uma linha que ficaram de fora e por quê. O detalhe continua no sistema do escritório.

## 6. Gravar e conferir

1. Mostre as linhas da carteira num quadro, com a observação de cada uma. Peça o ok.
2. Grave em `escritorio/07-operacao/experiencia/carteira.csv` (se o arquivo existe, acrescente; não sobrescreva).
3. Para cada cliente, crie `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` no formato de tabela de `docs/carteira.md`, regra 10 (quatro colunas, uma linha por contato, uma frase, sem dado sensível), com a linha da importação:

```markdown
---
documento: Histórico · C-AAAA-NNNN
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM ACOMPANHA O CLIENTE]
---

# Histórico · C-AAAA-NNNN · [NOME CURTO]

| Data e hora | Canal | Quem falou | O que foi dito |
|---|---|---|---|
| AAAA-MM-DD | importação | [FUNÇÃO DE QUEM IMPORTOU] | cliente trazido para a carteira; último contato que informou algo do caso em AAAA-MM-DD (data exata, aproximada ou sem data real) |
```

A linha da importação é registro interno: não conta como contato com o cliente e não muda o `ultimo_contato`. Se a `boas-vindas-do-cliente` estiver instalada, o modelo dela (`../boas-vindas-do-cliente/assets/historico-modelo.md`) segue a mesma tabela; sem ela, use o bloco acima.
4. Rode `python3 scripts/carteira.py <carteira.csv> --conferir` e corrija o que aparecer em "Registro a corrigir".
5. Rode o retrato do dia. Na primeira vez, muitos clientes aparecem sem notícia. Isso é o retrato real, e o primeiro trabalho do ciclo.
6. Sugira, sem pressa, refazer a entrada de quem nunca recebeu o combinado de comunicação, pela `boas-vindas-do-cliente` (modo cliente antigo).

## 7. Erros comuns

| Erro | Como evitar |
|---|---|
| Importar processos encerrados | Só casos em andamento; encerrado entra com `fase = encerrado`, se o escritório quiser o histórico |
| Data do último contato inventada | Data aproximada vem marcada no histórico; sem ideia nenhuma, use o dia da importação e marque "sem data real" |
| Planilha com nome completo e CPF colada inteira | Ler só a primeira linha, mostrar o mapa e converter só as colunas que entram |
| Código repetido com o comercial | Ler os dois arquivos antes de numerar |
| Importar e mandar mensagem para todos no mesmo dia | Ninguém recebe mensagem pela importação; quem está sem notícia entra na fila do ciclo, com leitura |
