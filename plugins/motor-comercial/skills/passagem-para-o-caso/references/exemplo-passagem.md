# Exemplo resolvido: passagem do caso 1 do Escritório Modelo

Caso fictício 1 de `../../../docs/casos-ficticios.md` (Marta, auxílio-doença cortado), depois da proposta e do contrato das habilidades `proposta-de-honorarios` e `contrato-de-honorarios`. Valores de exemplo. Feito com caso fictício, tudo grava em `escritorio/07-operacao/_treino/`.

## O que a habilidade encontrou

| Fonte | Caminho (no treino) | O que tirou dela |
|---|---|---|
| Registro | `_treino/comercial/contatos.csv` | C-2026-0001, Marta, previdenciário, etapa `fechado` (a advogada marcou em 2026-03-20) |
| Consulta | `_treino/comercial/consultas/C-2026-0001-2026-03-12.md` | "Mando a lista de documentos até segunda"; "o pedido sai em até 10 dias depois que os documentos chegarem"; Marta tem medo da perícia |
| Proposta aceita | `_treino/comercial/propostas/C-2026-0001-proposta-v1.md` | Escopo de seis itens, quatro exclusões, "a cada etapa, você recebe notícia por WhatsApp" |
| Contrato | `_treino/comercial/contratos/C-2026-0001-contrato-v1.md` | Entrada de 465 em 2026-03-20 e 4 parcelas de 271,25 todo dia 10; sem êxito |
| Fila | `_treino/comercial/fila/2026-03-16/02-C-2026-0001-envio-de-proposta.md` | Mensagem de envio, `status: enviado` |

## As perguntas que a habilidade fez (uma por vez, só o que faltava)

1. "Quem vai cuidar do caso e quem fala com a Marta no dia a dia?" Resposta: a advogada titular cuida; a secretária fala com ela.
2. "Ela disse como prefere ser contatada?" Resposta: WhatsApp, por texto; notícia importante por ligação.

## A ficha de passagem (trechos)

```markdown
---
documento: Ficha de passagem
codigo: C-2026-0001
versao: 1
revisado_em: 2026-03-20
dono: secretária
status: rascunho
---

# Passagem · C-2026-0001 · Marta

## 1. Em três linhas

Marta, previdenciário. Contratou o pedido administrativo para voltar a receber o auxílio-doença.
Primeiro passo do escritório: mandar a lista de documentos até 2026-03-23, como foi prometido na consulta.

## 2. Quem cuida

| Papel | Quem |
|---|---|
| Responsável pelo caso | advogada titular |
| Fala com o cliente no dia a dia | secretária |
| Substituto | advogada titular |
| Quem mais pode falar pela cliente | ninguém |

## 4. Valores e pagamento

- Modelo: fixo · total 1.550, consulta abatida
- Forma escolhida: entrada de 465 em 2026-03-20 e 4 parcelas de 271,25, todo dia 10
- Êxito: não há
- Quem acompanha os pagamentos: secretária

## 5. O que foi prometido ou combinado com o cliente

| Quando | Onde | O que foi dito | Quem cumpre | Até quando |
|---|---|---|---|---|
| 2026-03-12 | consulta | Mandar a lista de documentos | secretária | 2026-03-23 |
| 2026-03-16 | proposta | Notícia a cada etapa, por WhatsApp | secretária | sempre |
| 2026-03-12 | consulta | Preparar a Marta antes da perícia | advogada titular | antes da perícia |

## 6. Prazos ditos ao cliente

Na consulta: "o pedido sai em até 10 dias depois que os documentos chegarem". Prazo do escritório, não de decisão: pode ser cumprido. Nada foi dito sobre quando o INSS decide.

## 7. Documentos pendentes

| Documento | Onde a cliente consegue | Pedido em | Combinado para |
|---|---|---|---|
| Laudos e exames atuais | Com o médico que a acompanha | 2026-03-12 | 2026-03-30 |
| Carteira de trabalho | Aplicativo da carteira digital | 2026-03-12 | 2026-03-30 |
| Extrato de contribuições | Aplicativo ou site do INSS, ou agência | 2026-03-12 | 2026-03-30 |

## 8. Como a cliente prefere ser contatada

- WhatsApp, por texto · tratamento por "você"
- Notícia importante: por ligação, antes da mensagem

## 9. Humor e cuidados

- Humor ao fechar: ansioso
- O que preocupa: "tenho medo da perícia"
- Cuidados: questão de saúde envolvida; detalhes com a advogada. Na preparação da perícia, perguntar se alguém pode acompanhá-la.
```

## O que a checagem pegou

- A ata dizia "a doença dela é [detalhe]". A passagem ficou com "questão de saúde envolvida; detalhes com a advogada". O detalhe fica no sistema do escritório.
- Uma anotação de corredor dizia "a advogada falou que em dois meses ela volta a receber". Não está em nenhuma fonte. A habilidade perguntou à advogada; ela disse que não falou isso. Não entrou na passagem.

## A linha da carteira

O escritório usa o motor-experiencia (existe `escritorio/07-operacao/experiencia/`), mas a carteira de treino ainda não existia. Primeiro, o script só mostrou: a primeira linha de colunas que seria criada e a linha da Marta.

```
python3 "<pasta desta habilidade>/scripts/linha_da_carteira.py" "escritorio/07-operacao/_treino/experiencia/carteira.csv" codigo=C-2026-0001 nome_curto=Marta area=previdenciario "tipo_de_caso=restabelecimento de auxílio" responsavel=advogada inicio=2026-03-20 ultimo_contato=2026-03-20 ultimo_contato_tipo=mensagem proximo_contato=2026-03-23 motivo_proximo_contato=retorno-combinado documentos_pendentes=3 humor=ansioso resumo_mensal=sim atualizado_em=2026-03-20
```

A advogada deu o ok, e o mesmo comando rodou de novo com `--gravar --criar` no fim. A carteira nasceu com a primeira linha e esta:

```
C-2026-0001,Marta,previdenciario,restabelecimento de auxílio,advogada,2026-03-20,entrada,2026-03-20,mensagem,2026-03-23,retorno-combinado,,,3,ansioso,nao,sim,,,nao,,2026-03-20
```

`proximo_contato` é a primeira data prometida (a lista de documentos até segunda), por isso `retorno-combinado`. Sem essa promessa, a linha sairia com `boas-vindas` no dia seguinte à assinatura. `pagina_do_caso` ficou vazio: a ficha da experiência do Escritório Modelo não diz se usa a página.

## O registro do funil

A etapa continua `fechado`. Mudam `responsavel` (advogada), `proximo_passo` ("passagem feita; boas-vindas com a secretária"), `data_proximo_passo` (2026-03-23) e `atualizado_em`.

## O aviso a quem cuida

```
PASSAGEM · C-2026-0001 · Marta · previdenciário
Fechou em 2026-03-20. Cuida: advogada titular. Dia a dia: secretária.
Primeiro passo: boas-vindas e lista de documentos até segunda, 2026-03-23 (prometido na consulta).
Prometido: notícia a cada etapa por WhatsApp; preparação antes da perícia.
Faltam 3 documentos. Humor: ansiosa com a perícia.
Ficha completa: 07-operacao/comercial/passagens/C-2026-0001.md
```
