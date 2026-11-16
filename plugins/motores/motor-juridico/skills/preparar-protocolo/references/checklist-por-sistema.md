# Checklist de protocolo por sistema

Leia no passo 2 da habilidade e no modo adaptar. Os sistemas de processo eletrônico mudam de versão, e cada tribunal configura o seu: limite de tamanho, formatos aceitos, tipos de documento da lista, ordem exigida e o jeito de assinar variam de um tribunal para outro e de um ano para outro. Por isso **todo requisito de arquivo abaixo é `[CONFERIR]` no próprio sistema**, no manual do tribunal ou na tela de envio, e só perde a marca quando a pessoa conferiu e anotou onde viu (no checklist do escritório, `04-base/juridico/protocolo-<sistema>.md`).

Nenhum item aqui é tarefa da IA no sistema. A IA prepara a pasta e a lista; a pessoa entra no sistema, assina e protocola.

## O que vale para todos

| Item | O que conferir | Quem |
|---|---|---|
| Peça aprovada | Etapa `aprovada`, citações `verde`, dados `ok`, relatório de conferência em `casos/<codigo>/conferencias/` | IA confere o registro (S) |
| Peça final limpa | Nenhuma marcação entre colchetes na versão final; o PDF gerado dessa versão | IA confere o .md (S); a pessoa gera o PDF (A) |
| Documentos citados | Cada "doc. N" da peça tem arquivo, e cada arquivo é citado | IA confere (A) |
| Nome e ordem | Padrão de `nome_dos_arquivos`; peça em primeiro | Script (S) |
| Formato | PDF, e se o sistema exige PDF pesquisável ou outra especificação `[CONFERIR]` | Script vê a extensão; a pessoa confere a regra (A) |
| Tamanho | Por arquivo e total `[CONFERIR]`; arquivo grande dividido em partes nomeadas (`05-matricula-parte-1.pdf`) | Script (S) |
| Custas | Guia emitida por quem a ficha diz (`guia_de_custas`), paga, comprovante na pasta; ou o pedido de gratuidade na peça `[CONFERIR se o juízo pede algo junto]` | A pessoa (A) |
| Procuração | Na pasta, atual, com os poderes que a peça pede `[CONFERIR]` | A pessoa (A) |
| Sigilo | Peça com saúde, criança ou outro tema sensível: o advogado decide se pede segredo de justiça e como marcar no sistema `[CONFERIR]` | Advogado (H) |
| Assinatura | Certificado de quem assina (`quem_assina`, `assinatura`), no próprio sistema | Pessoa (H) |
| Protocolo e comprovante | Clicar em enviar, salvar o comprovante, anotar número, data e hora | Pessoa (H) |

## PJe

| Item | Conferir no sistema |
|---|---|
| Acesso | Certificado digital de quem assina e o perfil de advogado no tribunal certo (cada tribunal tem o seu PJe) `[CONFERIR]` |
| Petição inicial | Cadastro de classe, assunto, partes e polo antes do envio dos arquivos; dados que o sistema pede de cada parte `[CONFERIR]` |
| Petição no processo | O tipo de petição na lista do sistema e o tipo de cada documento anexo `[CONFERIR]` |
| Arquivos | Formato aceito, tamanho máximo por arquivo e se a peça pode ir no editor do sistema ou só em PDF `[CONFERIR]` |
| Ordem | A ordem em que os anexos aparecem e se dá para reordenar antes de assinar `[CONFERIR]` |
| Comprovante | Onde fica o recibo do protocolo e como salvar `[CONFERIR]` |

## eproc

| Item | Conferir no sistema |
|---|---|
| Acesso | Login e certificado de quem assina, e o cadastro do advogado no tribunal `[CONFERIR]` |
| Petição inicial | Classe, assunto, partes e o que o sistema pede de cada uma; competência escolhida no cadastro `[CONFERIR]` |
| Petição no processo | O tipo de petição e de cada documento na lista do sistema; a movimentação que a peça gera `[CONFERIR]` |
| Arquivos | Formato aceito e tamanho máximo por arquivo e por envio `[CONFERIR]` |
| Ordem | Como o sistema numera e ordena os anexos `[CONFERIR]` |
| Comprovante | Onde fica o recibo do protocolo e como salvar `[CONFERIR]` |

## e-SAJ

| Item | Conferir no sistema |
|---|---|
| Acesso | Certificado digital de quem assina e o cadastro no portal do tribunal `[CONFERIR]` |
| Petição inicial | Formulário de cadastro (foro, competência, classe, assunto, partes, valor da causa) e o que é obrigatório `[CONFERIR]` |
| Petição intermediária | O tipo de petição e a categoria de cada documento `[CONFERIR]` |
| Custas | Se o sistema exige o vínculo da guia paga no próprio peticionamento `[CONFERIR]` |
| Arquivos | Formato, tamanho máximo e se o sistema assina cada arquivo separado `[CONFERIR]` |
| Comprovante | O protocolo gerado e onde salvar `[CONFERIR]` |

## Projudi

| Item | Conferir no sistema |
|---|---|
| Acesso | Login, certificado e o cadastro do advogado no tribunal, que varia por estado `[CONFERIR]` |
| Petição inicial | Cadastro de partes, classe e assunto, e o que é obrigatório `[CONFERIR]` |
| Petição no processo | O tipo de juntada e de cada documento `[CONFERIR]` |
| Arquivos | Formato e tamanho máximo `[CONFERIR]` |
| Comprovante | Onde fica o recibo e como salvar `[CONFERIR]` |

## Outro sistema

Sistema que não está aqui (do tribunal administrativo, de um conselho, de um órgão público): o checklist usa a tabela "O que vale para todos" e a pessoa preenche, com a fonte, os itens de acesso, cadastro, arquivos e comprovante do sistema dela. Grave em `04-base/juridico/protocolo-<sistema>.md`.

## Como o checklist do escritório guarda o que foi conferido

```markdown
| Item | Regra do sistema | Onde a pessoa viu | Conferido em |
|---|---|---|---|
| Tamanho por arquivo | [O QUE O SISTEMA DIZ] | [TELA, MANUAL OU PÁGINA DO TRIBUNAL] | AAAA-MM-DD |
```

Item conferido há mais de 6 meses, ou o sistema mudou de versão: volta a `[CONFERIR]`.
