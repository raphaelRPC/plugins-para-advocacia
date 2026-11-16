---
name: captar-publicacoes
description: Capta as publicações e intimações do escritório e põe tudo num registro só. Busca no DJEN (a consulta pública do CNJ) pelas OABs da ficha, importa planilha (csv ou xlsx), e-mail do tribunal salvo (.eml ou texto colado), exportação do sistema jurídico e o registro do que a pessoa viu nos painéis. Normaliza para o publicacoes.csv, guarda o teor de cada ato, dá ids sequenciais, marca as duplicadas (mesmo processo, data e teor) e aponta o que chegou atrasado. Roda a pedido, no ciclo desde a última rodada e no treino com o lote de dez publicações. Use quando a pessoa disser "puxa as publicações de hoje", "o que saiu no DJEN", "importa essa planilha de intimações", "chegou e-mail do tribunal", "joga essas publicações no registro". Não use para classificar o ato e ligar ao caso (use triar-publicacoes) nem para contar o prazo (use calcular-prazo).
---

# Captar as publicações

> Tudo o que saiu para o escritório, de todas as fontes, num registro só, com o teor guardado e sem nada repetido.

Regras: `../../docs/regras.md`. O caminho da publicação e as colunas de `publicacoes.csv`: `../../docs/prazos.md`. A contagem: `../../docs/contagem.md`. Fichas: `../../docs/ficha-da-controladoria-modelo.md` e a tabela em `../../docs/ficha-da-controladoria.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Terça, 8h10. A estagiária abre o DJEN no navegador, depois o e-mail do TRT3, depois a planilha que o sistema exporta, e copia tudo numa lista à mão. A sentença do Otávio aparece duas vezes, por duas fontes. A sentença da Camila, disponibilizada na quinta, ninguém viu até hoje. Com a captação num registro só, a sentença repetida vira `duplicada` e a da Camila sobe para o topo com o aviso "captada com atraso".

**Regras fixas desta habilidade:**
1. A IA nunca entra em painel de tribunal e nunca usa senha, certificado digital ou token. O DJEN é consulta pública; o que está nos painéis chega pelo registro que a pessoa faz (`paineis-dos-sistemas`, se instalada).
2. Nada se perde: publicação sem data, sem teor ou com número fora do padrão entra assim mesmo, com o aviso, para a pessoa. Nada é apagado do registro.
3. Duplicada é a mesma publicação vinda de duas fontes (mesmo processo, mesma data, mesmo teor). Ela fica no registro como `duplicada`, apontando para a original, e nunca gera segundo prazo.
4. Captar não é triar: aqui ninguém diz o que o ato pede nem de que caso é. Toda linha nova entra `nao-triada`.
5. Fonte fora do ar não vira "nada novo": o resumo diz "DJEN não consultado" e manda importar a planilha.

## 1. Quando usar

**Use quando:**
- É hora da captação do dia (`horario_da_captacao` da ficha) e a pessoa pede as publicações (modo "a pedido").
- O `agente-de-controladoria` roda o ciclo (modo "no ciclo"): DJEN desde a última rodada, a pasta de entrada e o registro dos painéis.
- Chegou uma planilha, uma exportação do sistema jurídico, um e-mail do tribunal ou um texto colado (modo "importar").
- O `/motor-controladoria:comecar` ou a pessoa quer treinar com o lote de dez publicações (modo "treino").
- A `adaptar-controladoria` (se instalada) pede as fontes e o formato das exportações do escritório (modo "adaptar").

**Não use quando:**
- O pedido é dizer o que o ato pede e de que caso é: `triar-publicacoes`.
- O pedido é a conta do prazo: `calcular-prazo`.
- São centenas de publicações por dia para triar: capte aqui e agrupe na `triagem-em-massa` (se instalada; sem ela, triagem uma a uma na `triar-publicacoes`).
- O pedido é montar o roteiro dos painéis: `paineis-dos-sistemas` (se instalada; sem ela, a pessoa anota num texto o que viu e cola aqui).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-da-controladoria.md`) e `nicho.md`, se existir.
2. **Leia os aprendizados** (`escritorio/04-base/comum/aprendizados-controladoria.md`), em especial os da `captar-publicacoes` (fonte que costuma falhar, coluna que a exportação muda de nome).
3. **Veja o registro:** `escritorio/07-operacao/controladoria/publicacoes.csv`. Sem ele, o script cria só com a linha de títulos de `prazos.md` na primeira gravação.
4. **Veja a última rodada** em `escritorio/05-automacoes/ciclo-da-controladoria/registro-de-uso.md`. É dela que sai o "desde quando" da busca.
5. **Conta de IA:** publicação real tem nome de parte e número de processo. Só em conta profissional ou de equipe (`regras.md`, seção 6). Em conta pessoal, só o treino.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | K: `oabs_monitoradas`, `fontes_de_publicacao` |
| Melhora | K: `horario_da_captacao` |

`oabs_monitoradas` (número e UF de cada advogado) é o que a busca no DJEN usa. Sem ele, pergunte: "Quais OABs o escritório acompanha? Número e estado de cada advogado." e ofereça gravar. `fontes_de_publicacao` diz o que procurar além do DJEN (e-mail do tribunal, exportação do sistema, planilha de outro serviço). `horario_da_captacao` diz quando a captação deve estar pronta; sem ele, a rotina roda no começo do expediente e depois do almoço.

## 3. Fluxo

### Modos

| Modo | Quando | Entrada | Saída |
|---|---|---|---|
| A pedido | A pessoa pede as publicações de hoje | OABs da ficha e as datas | Linhas novas em `publicacoes.csv`, mostradas no chat |
| Importar | Chegou arquivo ou texto | csv, xlsx, .eml, .txt, registro de painel | O mesmo, só daquela fonte |
| No ciclo | O agente chama | DJEN desde a última rodada, `entrada/`, painel do dia | Registro gravado, `entrada/lidos/`, números para o resumo. Não mostra nada |
| Treino | Comecar ou pedido de treino | `assets/lote-de-treino.csv` e o registro de painel de treino | Dez linhas em `_treino/` |
| Adaptar | A `adaptar-controladoria` chama | Ficha, nicho, exemplos de exportação | Mapa de colunas e fontes do escritório, para aprovar |

Pedido direto ("importa esta planilha"): não faça entrevista. Rode, mostre e pergunte só o que faltar.

### Passo 1. Desde quando
Pergunte, se a pessoa não disse: "Busco desde a última rodada, em [data do registro de uso], até hoje?". Sem registro de uso, pergunte: "Desde que dia eu busco? Se não souber, sugiro a data da última vez que alguém olhou as publicações." A busca começa **no dia** da última rodada, não no seguinte: o que foi disponibilizado depois que a rodada rodou entra agora, e o que já estava no registro não entra de novo.

### Passo 2. Buscar no DJEN
Com internet (Cowork ou Claude Code), rode:

```
python3 "<pasta desta habilidade>/scripts/captar_djen.py" \
  --ficha escritorio/04-base/comum/ficha-da-controladoria.md \
  --de AAAA-MM-DD --ate AAAA-MM-DD \
  --saida escritorio/07-operacao/controladoria/entrada/AAAA-MM-DD-HHMM-djen.csv
```

No Cowork e no Claude Code, a pasta desta habilidade é `${CLAUDE_PLUGIN_ROOT}/skills/captar-publicacoes`. `--oab 123456/MG` (pode repetir) vale no lugar de `--ficha`; `--registro-de-uso <arquivo>` vale no lugar de `--de`. A consulta é a pública do CNJ, por OAB, UF e datas de disponibilização, página por página; os nomes dos parâmetros e o limite por página seguem a documentação pública do CNJ `[CONFERIR]` quando ela mudar. A mesma comunicação que aparece para duas OABs do escritório sai uma vez só.

**Sem internet ou com erro**, o script sai com código 1 e a orientação. Diga à pessoa: "Não consegui consultar o DJEN agora. Pode fazer a consulta pública no navegador (ou exportar do sistema) e salvar a planilha em `entrada/`? Eu importo em seguida." Registre "DJEN não consultado" no resumo. Nunca siga como se não houvesse publicação.

### Passo 3. Importar o que chegou
Rode o importador sobre a planilha do DJEN, a pasta `entrada/` e o registro dos painéis do dia:

```
python3 "<pasta desta habilidade>/scripts/importar_publicacoes.py" \
  escritorio/07-operacao/controladoria/entrada \
  escritorio/07-operacao/controladoria/paineis/AAAA-MM-DD.md \
  --registro escritorio/07-operacao/controladoria \
  --data AAAA-MM-DD --ultima-rodada AAAA-MM-DD
```

Sem `--gravar`, ele só mostra o que faria. O que ele lê:
- **Planilha** `.csv` (vírgula ou ponto e vírgula, com ou sem BOM, utf-8 ou cp1252) e `.xlsx` (só com o `openpyxl`; sem ele, a pessoa salva como csv). As colunas são achadas pelo nome, com apelidos ("Nº do Processo", "Data de disponibilização", "Texto"). Obrigatórias: processo, data de disponibilização e teor. Falta uma: o script para e diz quais nomes aceita.
- **E-mail salvo** `.eml` e **texto colado** `.txt` ou `.md`: uma publicação por número de processo. A data de disponibilização vem só do bloco daquele processo, nunca de outro bloco nem do texto geral do e-mail. Sem data no bloco, usa a data do e-mail (cabeçalho Date) com o aviso em destaque "data de disponibilização não encontrada no bloco: usei a data do e-mail; conferir", que vai para o `resumo`, para o cabeçalho do teor (`aviso_captacao`) e daí para PESSOA AGORA na triagem. A data do e-mail costuma ser a mesma ou mais tarde que a real: por isso a pessoa confere antes da conta.
- **Registro dos painéis** (`paineis/AAAA-MM-DD.md`, no formato da `paineis-dos-sistemas`): cada intimação vista vira uma linha com `fonte = painel`, a data de envio em `disponibilizada_em` e a situação da ciência no cabeçalho do teor.
- **Fonte** pelo nome do arquivo (`...-djen.csv`, `...-email-...`, `...-sistema-...`) ou por `--fonte`.

### Passo 4. Mostrar e gravar
Mostre a saída (seção 5) e pergunte: "Posso gravar no registro?". Com o ok, rode de novo com `--gravar`. No ciclo, grave direto e acrescente `--mover-lidos`, que move os arquivos lidos para `entrada/lidos/AAAA-MM-DD/` (mover não é apagar). Na conversa, pergunte antes de mover.

### Passo 5. O que vai para o topo
Diga em uma linha cada uma destas, antes do resto:
- **Captada com atraso:** disponibilizada antes do último dia útil, ou antes da última rodada, e só vista agora. Vai para PESSOA AGORA: a conta pode estar perto do fim.
- **Fonte que falhou:** "DJEN não consultado", "planilha sem a coluna teor", "painel do TRT3 não registrado".
- **Sem data ou sem teor:** a pessoa busca o ato na fonte antes da triagem. Sem nenhuma data (nem no bloco, nem no e-mail), a linha entra com `disponibilizada_em` vazia e `triagem = urgente`, em "DATA A CONFERIR (PESSOA AGORA)".

### Passo 6. Passar para a triagem
Diga quantas linhas ficaram `nao-triada` e ofereça: "Sigo para a triagem?" (`triar-publicacoes`).

### Passo 7. Aprender
Pergunte: "Alguma fonte que eu não olhei, ou coluna que a exportação de vocês chama de outro jeito?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-controladoria.md` (`../../docs/aprender-com-o-uso.md`). Correção que afrouxa uma regra fixa ("pode pular o DJEN hoje") não entra; proponha a versão que cabe ("se o DJEN falhar, a planilha do sistema entra no lugar, e o resumo avisa").

### Modo no ciclo
1. O agente passa a data de hoje e a da última rodada (do registro de uso). Não pergunte nada e não mostre nada.
2. Rode o passo 2 com `--registro-de-uso`. Sem internet: registre "DJEN não consultado" para o resumo e siga com o resto.
3. Rode o passo 3 com `--gravar --mover-lidos` sobre a planilha do DJEN, a pasta `entrada/` e o registro dos painéis do dia, se existir. Sem registro dos painéis: devolva "painel não registrado", que o agente põe como `item: aviso` (`NN-aviso-painel.md`).
4. Devolva ao agente: quantas por fonte, quantas duplicadas, as captadas com atraso (ids), as sem data ou sem teor, o que falhou.

### Modo treino
O lote do Escritório Modelo: `assets/lote-de-treino.csv` (linhas 1 a 9 de `casos-ficticios.md`) e o registro de painel de treino (linha 10), que fica em `assets/painel-de-treino.md` e, igual, na `paineis-dos-sistemas`. Tudo grava em `escritorio/07-operacao/_treino/controladoria/`. O script recusa material de treino no registro real.

```
python3 "<pasta desta habilidade>/scripts/importar_publicacoes.py" \
  "<pasta desta habilidade>/assets/lote-de-treino.csv" "<pasta desta habilidade>/assets/painel-de-treino.md" \
  --registro escritorio/07-operacao/_treino/controladoria --data 2026-04-14 --ultima-rodada 2026-04-08 --treino --gravar
```

O teste passa quando: entram dez linhas (`PUB-2026-00001` a `00010`: djen 8, email 1, painel 1); a linha 6 sai `duplicada de PUB-2026-00001`; a linha 3 (disponibilizada em 2026-04-09) sai em "captada com atraso"; a linha 10 traz a data de envio 2026-04-06 e `painel_ciencia: sem-ciencia`; rodar de novo não acrescenta nada ("já estavam no registro: 10"). Para testar a busca sem rede: `captar_djen.py --simular "<pasta desta habilidade>/assets/lote-de-treino.csv" --de 2026-04-08 --ate 2026-04-14 --saida <arquivo>` devolve as oito linhas do DJEN.

### Modo adaptar
1. Leia a ficha, `nicho.md` e um exemplo de cada exportação que o escritório usa (sem dado de cliente: só a linha de títulos e uma linha inventada).
2. Proponha: o mapa de colunas de cada exportação (o nome lá e a coluna aqui), o nome de arquivo de cada fonte na pasta `entrada/`, o horário da captação e o que fazer quando cada fonte falha.
3. Marque cada item `[NOVO]` ou `[ALTERADO]` e pergunte: "É assim que chega para vocês?".
4. Com o ok, grave em `escritorio/04-base/controladoria/nicho/captar-publicacoes.md`.

## 4. As fontes e o que cada uma traz

| Fonte | Como chega | O que costuma faltar | Cuidado |
|---|---|---|---|
| DJEN | `captar_djen.py`, consulta pública por OAB | Publicação em nome de advogado que não está na ficha | Toda OAB do escritório na ficha, inclusive de quem entrou há pouco |
| E-mail do tribunal | `.eml` ou texto colado em `entrada/` | A data de disponibilização | Usar a data do e-mail só com aviso |
| Exportação do sistema | `.csv` ou `.xlsx` em `entrada/` | O teor inteiro (às vezes vem cortado) | Teor cortado: buscar o ato na fonte |
| Planilha de outro serviço | `.csv` ou `.xlsx` | Coluna com nome diferente | Mapa de colunas no modo adaptar |
| Painel do sistema | Registro da pessoa (`paineis/AAAA-MM-DD.md`) | A situação da ciência | A IA não abre painel; abrir dá ciência |

Fins de semana e feriados: a busca cobre o intervalo inteiro, e o que saiu na sexta à tarde entra na segunda. A data que vale para a conta é a da disponibilização, nunca a da captação.

## 5. Formato da saída

```
CAPTAÇÃO · AAAA-MM-DD · [gravado | SIMULAÇÃO]
Lidas: N · entram: N (djen N, email N, painel N) · duplicadas: N · já estavam no registro: N
CAPTADAS COM ATRASO (PESSOA AGORA): [id · disponibilizada · tribunal · processo]
DATA A CONFERIR (PESSOA AGORA): [id · tribunal · processo · sem data | data do e-mail, não do bloco]
ENTRAM: [id · fonte · disponibilizada · tribunal · processo · nao-triada | duplicada de ...]
AVISOS: [sem data, sem teor, tribunal tirado do número, fonte que falhou]
DJEN: [consultado de ... a ... | não consultado: motivo]
Próximo passo: triar-publicacoes
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| O registro das publicações | `escritorio/07-operacao/controladoria/publicacoes.csv` |
| O teor de cada publicação, como veio | `escritorio/07-operacao/controladoria/publicacoes/AAAA-MM-DD/<id>.md` (a data é a da captação) |
| A planilha do DJEN | `escritorio/07-operacao/controladoria/entrada/AAAA-MM-DD-HHMM-djen.csv` |
| Arquivos já lidos | `escritorio/07-operacao/controladoria/entrada/lidos/AAAA-MM-DD/` |
| Mapa das fontes (modo adaptar) | `escritorio/04-base/controladoria/nicho/captar-publicacoes.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-controladoria.md` |

No registro, só linhas novas: `nao-triada`, ou `duplicada` com `triada_por = ia` e o id da original no `resumo`. `publicada_em` fica vazia (é a `calcular-prazo` que conta). O teor tem nome de parte e número do processo: fica em `07-operacao/`, fora do Projeto no Claude. O resumo do dia lembra a pessoa de apagar `entrada/lidos/` com mais de 7 dias (ou o prazo da regra de uso de IA do escritório); quem apaga é a pessoa. Sem pasta aberta: as linhas saem numa tabela para colar na planilha, e o teor em blocos, com o caminho de cada um.

## 7. Solo e equipe

**Solo:** rode a captação no começo do expediente e depois do almoço, mesmo nos dias sem audiência. A sexta à tarde é a que mais escapa. Se você atua em mais de um estado, confira se todas as suas inscrições estão em `oabs_monitoradas`.

**Equipe:** quem capta é o `responsavel_controladoria` da ficha (em geral, a estagiária ou a secretária). Advogado novo no escritório entra na ficha no primeiro dia. Quando a captação falhar, a regra é avisar a advogada responsável no mesmo turno, sem esperar o dia seguinte.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Captação à mão em três telas | Publicação que ninguém viu | Um registro só, de todas as fontes |
| A mesma sentença por duas fontes | Dois prazos, duas peças, confusão na agenda | `duplicada` apontando para a original |
| DJEN fora do ar tratado como "nada novo" | Prazo correndo sem ninguém saber | Código 1, "DJEN não consultado" e a planilha no lugar |
| Publicação de quinta vista na terça | Prazo já pela metade | "Captada com atraso" no topo |
| Linha sem data ou sem teor descartada | Ato perdido | Entra com aviso, para a pessoa |
| IA abrindo painel com a senha de alguém | Ciência dada sem querer, dado exposto | Regra fixa 1: a pessoa registra, a IA lê o registro |
| Treino misturado ao registro real | Prazo fictício na agenda | O script recusa treino fora de `_treino/` |

## 9. Próximo passo

- As linhas `nao-triada`: `triar-publicacoes`, que liga ao caso pela carteira e sugere a triagem com o trecho literal.
- Centenas no mesmo dia: `triagem-em-massa` (se instalada; sem ela, a `triar-publicacoes` em lotes de 30).
- Processo que publicou e não está na carteira: `carteira-de-processos` (se instalada; sem ela, a pessoa diz de quem é o processo na triagem).
- O ciclo do dia inteiro: `rotina-da-controladoria` ou `/motor-controladoria:ciclo`.

## Referências desta habilidade

- `scripts/captar_djen.py`: a busca na consulta pública do DJEN por OAB e datas, com `--simular` para teste sem rede. Rode no passo 2 e no ciclo.
- `scripts/importar_publicacoes.py`: importa csv, xlsx, e-mail, texto e registro de painel para `publicacoes.csv`, guarda o teor, dá ids, marca duplicadas e aponta atrasos. Rode no passo 3, no ciclo e no treino.
- `assets/lote-de-treino.csv`: as nove publicações do DJEN e do e-mail do Escritório Modelo (linhas 1 a 9 de `casos-ficticios.md`). Use no modo treino.
- `assets/painel-de-treino.md`: o registro de painel de treino (linha 10), cópia do que está na `paineis-dos-sistemas`, para o treino funcionar sem ela. Use no modo treino.
