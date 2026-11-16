---
name: preparar-protocolo
description: >
  Prepara o protocolo de uma peça aprovada pelo advogado: o checklist pelo sistema da ficha
  (PJe, eproc, e-SAJ, Projudi), a peça final sem nenhuma marcação, os documentos nomeados no
  padrão do escritório e na ordem, tamanho e formato (sempre a conferir no próprio sistema), guia
  de custas e quem assina. Um script confere a pasta dos arquivos sem abrir o conteúdo. Depois
  que a pessoa protocola, registra número, data e comprovante no pecas.csv e na pasta do caso, e
  a linha de trabalho do escritório no histórico do cliente do motor-experiencia (se instalado).
  Use quando o advogado disser "prepara o protocolo", "confere a pasta antes de eu protocolar",
  "os arquivos estão no padrão?", "protocolei, registra", "o que falta para protocolar".
  Não use para conferir citações ou dados da peça (use conferir-citacoes e conferir-peca) nem
  para calcular prazo processual (é da controladoria).
---

# Preparar o protocolo

> A peça aprovada só chega inteira ao processo se a pasta estiver certa: peça final limpa, documentos na ordem, nomes no padrão, arquivos que o sistema aceita. A IA confere tudo isso. A pessoa assina e protocola.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção, etapas e `pecas.csv`: `../../docs/producao.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Sexta, 17h20. O divórcio da Renata foi aprovado na terça. A advogada abre o sistema para protocolar e o upload trava: a matrícula do imóvel passa do tamanho, o esboço do acordo está em .docx e a certidão se chama "Certidão de casamento.PDF". Ela renomeia, converte e divide às pressas, com o certificado na mão. Na quinta, o checklist e o script teriam apontado os três.

**Regras fixas desta habilidade:**
1. Assinar, usar o certificado digital, digitar senha ou PIN e clicar em protocolar são sempre da pessoa (sigla H). A IA nunca recebe senha, token ou certificado, e o checklist nunca põe esses passos como tarefa dela.
2. Só peça `aprovada` pelo advogado, com citações `verde` e dados `ok`, vai para o checklist de protocolo. A peça final não tem nenhuma marcação entre colchetes.
3. Requisito de arquivo (formato, tamanho, resolução, assinatura, ordem que o sistema exige) é sempre `[CONFERIR]` no próprio sistema. A habilidade não afirma regra de sistema de tribunal de memória.
4. O script lê só o nome, o tamanho e os primeiros bytes de cada arquivo. Não abre documento do cliente.
5. Número do processo e comprovante entram só no `pecas.csv` e em `casos/<codigo>/protocolo/`. O histórico do cliente leva a frase sem número.

## 1. Quando usar

**Use quando:**
- Uma peça chegou a `aprovada` e alguém vai protocolar (modo checklist).
- A pessoa juntou os arquivos numa pasta e quer saber se estão no padrão (modo conferir a pasta).
- A pessoa protocolou e quer registrar número, data e comprovante (modo registrar).
- O `agente-juridico` ou a `rotina-juridica` chamou para as aprovadas do dia (modo no ciclo).
- O `/motor-juridico:fila` aprovou uma peça e ofereceu o protocolo.
- Teste com o caso fictício da Renata (modo treino), ou a `adaptar-juridico` pediu o checklist do escritório (modo adaptar).

**Não use quando:**
- A peça ainda não foi aprovada: o caminho é a fila do advogado (`/motor-juridico:fila`). Peça em `minuta`, `conferida` ou `revisada` não tem checklist de protocolo.
- O pedido é conferir citação ou dado da peça: `conferir-citacoes` e `conferir-peca`.
- O pedido é calcular ou controlar o prazo processual: é da controladoria do escritório, fora deste plugin.

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`), `nicho.md` se existir e os aprendizados (`aprendizados-juridico.md`). A seção 5 da ficha jurídica (Protocolo) é a base do checklist.
2. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Em que sistema esta peça vai ser protocolada?", depois "Como vocês nomeiam os arquivos?".
3. **Leia a linha da peça** no `escritorio/07-operacao/juridico/pecas.csv` e o último relatório em `casos/<codigo>/conferencias/`. Etapa diferente de `aprovada`, citação diferente de `verde` ou dado diferente de `ok`: pare e diga o que falta, sem checklist.
4. **Leia o checklist do sistema** em `references/checklist-por-sistema.md`. Se o escritório já adaptou o dele (`04-base/juridico/protocolo-<sistema>.md`), ele vale mais.
5. **Conta e dados.** Os documentos a protocolar têm dado do cliente. A pessoa indica a pasta; a habilidade não pede para colar documento no chat e não lê o conteúdo.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `sistemas`, `nome_dos_arquivos`, `assinatura` |
| Melhora | J: `limite_de_tamanho`, `guia_de_custas`, `quem_protocola` |

Também lê, se preenchido, J: `quem_assina`, para o checklist dizer quem assina. Campo que falta e a peça pede: pergunte aquele campo, uma vez, e ofereça gravar. Sem `limite_de_tamanho`, o script mostra os tamanhos sem comparar e o checklist manda conferir no sistema.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| Checklist | Peça aprovada | O id da peça | O checklist preenchido, gravado em `casos/<codigo>/protocolo/` |
| Conferir a pasta | Arquivos juntados | O caminho da pasta | O relatório do script, no chat e no checklist |
| Registrar | Depois do protocolo | Sistema, número, data e hora, comprovante | `pecas.csv` em `protocolada`, comprovante na pasta do caso, linha no histórico do cliente |
| No ciclo | O agente chama | As aprovadas do `pecas.csv` | Checklist gravado e item na fila, sem mostrar nada |
| Treino | Caso fictício | A peça P-2026-0003 da Renata | O mesmo, em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Ficha, sistemas e tribunais do escritório | O checklist do escritório por sistema, para aprovar |

Pedido direto ("confere esta pasta"): não faça entrevista. Rode o script e mostre.

### Passo 1. Conferir que a peça pode ir
Mostre em uma linha: id, código, peça, etapa, citações, dados, prazo interno. Só segue com `aprovada`, `verde` e `ok`. Diferente disso: "Esta peça ainda não pode ir para protocolo: [motivo]. O advogado resolve pela fila." e pare.

### Passo 2. Montar o checklist
Preencha `assets/checklist-de-protocolo.md` com a ficha e o checklist do sistema (`references/checklist-por-sistema.md`):
- **Peça final:** a versão aprovada em `casos/<codigo>/minutas/`, o PDF gerado pela pessoa a partir dela, nenhuma marcação (o script confere a versão em .md com `--minuta`).
- **Documentos:** a lista que a peça cita (o "doc. N" de cada um), com o nome no padrão de `nome_dos_arquivos` e a ordem. Documento citado na peça sem arquivo, ou arquivo sem citação na peça: aponte.
- **Arquivos:** formato, tamanho por arquivo e total, sempre `[CONFERIR]` no próprio sistema, com o valor de `limite_de_tamanho` se houver.
- **Custas:** quem emite a guia e quando (`guia_de_custas`), ou o pedido de gratuidade que está na peça. Se o juízo exige comprovante junto: `[CONFERIR]`.
- **Sigilo:** se a peça trata de saúde, criança ou outro tema que pede segredo de justiça, o lembrete de marcar no sistema `[CONFERIR]` e a decisão do advogado.
- **Quem faz:** quem assina (`quem_assina`, com `assinatura`) e quem protocola (`quem_protocola`). Os dois passos são H.

### Passo 3. Conferir a pasta
Pergunte: "Em que pasta estão os arquivos que vão ser protocolados?". Rode o script (seção 4) com `nome_dos_arquivos`, a lista de documentos do passo 2 em `--esperados` e o limite, se houver. Mostre o relatório e ponha o resultado no checklist. "CORRIGIR ANTES": a pessoa corrige e o script roda de novo. A habilidade não renomeia, não converte e não apaga arquivo.

### Passo 4. Mostrar e gravar
Mostre o checklist com o relatório. Com o ok, grave em `escritorio/07-operacao/juridico/casos/<codigo>/protocolo/<peca>-AAAA-MM-DD.md`, com `status: preparado`. A etapa da peça continua `aprovada`.

### Passo 5. A pessoa protocola
Diga: "Agora é com [quem_protocola]: assinar com o certificado no sistema e protocolar. Quando terminar, me passe o sistema, o número, a data e a hora do comprovante." A habilidade não acompanha o login nem a assinatura.

### Passo 6. Registrar o protocolo
Com os dados do comprovante:
1. Rode `scripts/registrar_protocolo.py` sem `--gravar` e mostre o antes e o depois da linha. Com o ok, rode com `--gravar`. O script recusa peça que não está `aprovada` ou que já está `protocolada`.
2. Peça o comprovante e grave em `casos/<codigo>/protocolo/<peca>-AAAA-MM-DD-comprovante.pdf` (a pessoa salva o arquivo; a habilidade diz o nome). No checklist, `status: protocolado`, com sistema, número, data e hora.
3. **Histórico do cliente**, se o motor-experiencia estiver instalado (existe `07-operacao/experiencia/carteira.csv` ou a pasta `clientes/<codigo>/`): acrescente em `07-operacao/experiencia/clientes/<codigo>/historico.md` a linha de trabalho do escritório, no formato de `motor-experiencia/docs/carteira.md` (regra 10): `| AAAA-MM-DD HH:MM | trabalho-do-escritorio | [função] | Protocolamos [a peça, em linguagem simples]. |`. Sem número do processo, sem dado sensível. Essa linha alimenta o resumo mensal e a página do caso e não muda o `ultimo_contato`. Sem o motor-experiencia, nada aqui.
4. Se a fila tem o item do protocolo, o status vira `enviado`.

### Passo 7. Aprender
Pergunte: "O sistema recusou ou pediu alguma coisa que o checklist não tinha?". Cada resposta vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Se for regra do sistema ("PDF acima de N MB não sobe no eproc do TRF"), proponha gravar também no checklist do escritório (`04-base/juridico/protocolo-<sistema>.md`) e no `limite_de_tamanho`, com a fonte e a data em que a pessoa viu, e linha no histórico da ficha.

### Modo no ciclo
1. O agente passa as peças `aprovadas`. Não pergunte nada e não mostre nada.
2. Para cada uma: passos 1 e 2. Se os arquivos já estão em `casos/<codigo>/protocolo/<peca>-arquivos/`, rode o script nessa pasta; fora de `escritorio/`, o ciclo não lê, e o checklist diz "pasta a conferir pela pessoa".
3. Grave o checklist com `status: preparado` e um item na fila (`07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-protocolo.md`, formato de `agentes-e-fila.md`) com `tipo: protocolo`, `revisor: pendente`, o prazo interno e, em `antes_de_enviar`, o que falta (arquivo fora do padrão, custas, quem assina). O `revisor-juridico` bloqueia checklist que ponha assinatura, senha ou certificado como tarefa da IA.
4. Nunca protocolar, nunca mover a etapa, nunca registrar protocolo sem a pessoa.
5. Devolva ao agente: quantos checklists, quantos com pendência, campos da ficha que faltaram.

### Modo treino
A peça P-2026-0003 (Renata, C-2026-0005, divórcio consensual, `aprovada`) do `pecas.csv` de treino da `rotina-juridica`, em `_treino/juridico/rotina-juridica/pecas.csv` (se instalada; sem ela, monte a linha com os dados de `../../docs/casos-ficticios.md`). Tudo grava em `escritorio/07-operacao/_treino/juridico/`, e o registro usa `--treino`. Para o script, monte uma pasta de treino com arquivos vazios ou de texto com nomes de propósito errados (seção 5).

### Modo adaptar
1. Leia a ficha jurídica (`sistemas`, `tribunais_principais`, `nome_dos_arquivos`, `limite_de_tamanho`, `guia_de_custas`) e `references/checklist-por-sistema.md`.
2. Monte o checklist do escritório para cada sistema que ele usa, com os itens do escritório (procuração sempre em 02, comprovante de custas antes dos documentos, e o que mais ele disser). Requisito de sistema continua `[CONFERIR]` até a pessoa conferir no próprio sistema e dizer onde viu.
3. Marque cada mudança `[ALTERADO]` e grave em `04-base/juridico/protocolo-<sistema>.md` com o ok.

## 4. Os scripts

### 4.1 Conferir a pasta

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/preparar-protocolo/scripts/conferir_pasta.py" \
  "CAMINHO/DA/PASTA" --nomes "01-peticao.pdf, 02-procuracao.pdf, 03-documentos-pessoais.pdf" \
  --esperados "peticao, procuracao, documentos-pessoais" --limite-mb 5 \
  --minuta "escritorio/07-operacao/juridico/casos/C-AAAA-NNNN/minutas/<peca>-v<n>.md"
```

Sem `${CLAUDE_PLUGIN_ROOT}`, troque pelo caminho da pasta desta habilidade. `--nomes` recebe o campo `nome_dos_arquivos` como está; dele saem a largura do número, o separador e a extensão. `--limite-mb` recebe o valor de `limite_de_tamanho` (o número que a pessoa conferiu no sistema). Outras opções: `--limite-total-mb`. `--help` mostra tudo.

| Confere | Aponta |
|---|---|
| Nome | Fora do padrão (acento, espaço, maiúscula, sem número, número de outra largura, sublinhado), com a sugestão de nome; número que parece CPF ou processo no nome |
| Ordem | Número repetido, buraco, não começa em 01, a peça não é a primeira; com `--esperados`, documento sem arquivo, fora da ordem, ou arquivo fora do checklist |
| Tamanho | Acima do limite por arquivo ou do total `[CONFERIR]`; arquivo vazio |
| PDF | Extensão diferente de .pdf; arquivo com nome de .pdf que não é PDF por dentro |
| Sobra | Arquivo oculto ou temporário, subpasta |
| Minuta | Com `--minuta` (.md ou .txt), qualquer marcação entre colchetes que sobrou |

Sai com código 1 e "ERRO:" quando a pasta não existe, está vazia ou um valor não dá para ler. Com a pasta lida, a primeira linha diz "PRONTA PARA A PESSOA PROTOCOLAR" ou "CORRIGIR ANTES". Sem Python, a pessoa confere à mão a mesma tabela.

### 4.2 Registrar o protocolo

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/preparar-protocolo/scripts/registrar_protocolo.py" \
  "escritorio/07-operacao/juridico/pecas.csv" --id P-AAAA-NNNN --sistema PJe \
  --numero "[O NÚMERO DO COMPROVANTE]" --data "AAAA-MM-DD HH:MM" --quem advogada
```

Mostra o antes e o depois e a linha do histórico; com `--gravar`, grava, mantendo o separador, o BOM e a codificação da planilha, e deixa a cópia anterior em `pecas.csv.bak`. Recusa, com código 1: peça que não existe ou aparece duas vezes, que não está `aprovada`, que já está `protocolada`, com citações ou dados pendentes, número vazio ou marcação, data que não dá para ler, e o registro de treino sem `--treino`.

## 5. Exemplo resolvido (treino)

Renata, P-2026-0003, divórcio consensual, PJe, aprovada em 2026-04-14. Na pasta de treino `escritorio/07-operacao/_treino/juridico/casos/C-2026-0005/protocolo/divorcio-consensual-arquivos/` estão: `01-peticao.pdf`, `02-procuracao.pdf`, `03-Certidão de casamento.PDF`, `04-documento-do-carro.pdf` (que não é PDF por dentro), `05-matricula-do-imovel.pdf` (6,7 MB), `06-esboco-do-acordo.docx` e `.DS_Store`. Com `--nomes "01-peticao.pdf, 02-procuracao.pdf"` e `--limite-mb 5` (valor de exemplo), o script devolve "CORRIGIR ANTES" e aponta: o arquivo oculto; a certidão com acento, espaço e maiúscula, sugestão `03-certidao-de-casamento.pdf`; o documento do carro que não é PDF; a matrícula acima de 5 MB `[CONFERIR]`; o acordo em .docx.

O esboço do acordo é o documento em que a partilha do carro aparece em duas versões (`../../docs/casos-ficticios.md`, caso 3). Se a minuta aprovada cita a versão final, o checklist pergunta: "Qual versão do acordo vai? A peça cita a de [DATA]." Quem decide é a advogada.

Depois que a advogada protocola, o registro em treino:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/preparar-protocolo/scripts/registrar_protocolo.py" \
  "escritorio/07-operacao/_treino/juridico/rotina-juridica/pecas.csv" --id P-2026-0003 --sistema PJe \
  --numero "0000000-00.2026.8.13.0000 (exemplo)" --data "2026-04-17 15:40" --quem advogada --treino
```
E a linha do histórico de treino: `| 2026-04-17 15:40 | trabalho-do-escritorio | advogada | Protocolamos o pedido de divórcio consensual. |`

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Checklist do protocolo (e o resultado do script) | `escritorio/07-operacao/juridico/casos/<codigo>/protocolo/<peca>-AAAA-MM-DD.md` |
| Comprovante (a pessoa salva) | `escritorio/07-operacao/juridico/casos/<codigo>/protocolo/<peca>-AAAA-MM-DD-comprovante.pdf` |
| Linha da peça | `escritorio/07-operacao/juridico/pecas.csv`: `protocolada`, `protocolo_sistema`, `protocolo_numero`, `protocolo_data`, `atualizado_em` |
| Linha de trabalho do escritório | `escritorio/07-operacao/experiencia/clientes/<codigo>/historico.md` (motor-experiencia, se instalado) |
| Item na fila (modo no ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/NN-<codigo>-protocolo.md` |
| Checklist do escritório por sistema (modo adaptar) | `escritorio/04-base/juridico/protocolo-<sistema>.md` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

Sem pasta aberta: o checklist vem no chat, com o caminho onde ficaria; o script não roda, e a pessoa confere a tabela da seção 4.1 à mão; a linha do `pecas.csv` vem como tabela para colar na planilha.

## 7. Solo e equipe

**Solo:** o checklist é a lista da véspera. Junte a pasta no dia em que a peça foi aprovada e rode o script; no dia do protocolo, só assinar e enviar.

**Equipe:** o estagiário ou a secretária junta a pasta e roda o script; quem assina (`quem_assina`) recebe a pasta "PRONTA" e protocola, ou quem protocola (`quem_protocola`) faz o upload e a advogada assina no sistema, conforme a ficha. O registro depois do protocolo é de quem protocolou, no mesmo dia.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Protocolar minuta com `[CONFERIR]` esquecido | Marca interna dentro do processo | Só peça aprovada; o script procura marcação na versão final |
| Upload recusado na hora | Correria com o certificado na mão e prazo correndo | Script confere nome, formato e tamanho na véspera |
| Documento na ordem errada ou faltando | Juiz manda emendar; cliente acha que o escritório errou | `--esperados` com a lista que a peça cita |
| CPF no nome do arquivo | Dado pessoal exposto no processo e na pasta | Script aponta número que parece CPF ou processo |
| Regra de sistema dita de memória | Checklist com limite errado | Requisito de sistema sempre `[CONFERIR]` no próprio sistema |
| IA com senha ou certificado | Risco de segurança e de responsabilidade | Assinatura e protocolo são H; o revisor bloqueia |
| Protocolo feito e não registrado | Rotina cobra peça já protocolada; cliente sem notícia | Registro no `pecas.csv` e linha no histórico do cliente |
| Número do processo na página do cliente | Dado a mais na página | Histórico sem número; o número fica só no `pecas.csv` |

## 9. Próximo passo

- Peça protocolada com o motor-experiencia instalado: `status-para-o-cliente` ou `resumo-mensal-do-caso`, do motor-experiencia, para o cliente saber; quem lê e envia é a pessoa.
- O sistema recusou um arquivo: corrigir e rodar o script de novo; a regra nova vai para o checklist do escritório (passo 7).
- Próxima peça do mesmo caso: `rotina-juridica` mostra o que vem.

## Referências desta habilidade

- `references/checklist-por-sistema.md`: os itens de protocolo por sistema (PJe, eproc, e-SAJ, Projudi), todos com o requisito a conferir no próprio sistema. Leia no passo 2 e no modo adaptar.
- `assets/checklist-de-protocolo.md`: o modelo do checklist que grava em `casos/<codigo>/protocolo/`. Use no passo 2.
- `scripts/conferir_pasta.py`: confere a pasta dos arquivos sem abrir o conteúdo. Rode no passo 3.
- `scripts/registrar_protocolo.py`: registra o protocolo no `pecas.csv`, com prévia antes de gravar. Rode no passo 6.
