# A conferência de coerência e de requisitos

A parte da `conferir-peca` que o script não faz. Leia nos passos 4 a 6. O script acha o que é mecânico (nome que não é do caso, data divergente, doc. que não existe). Aqui ficam as perguntas que pedem leitura: a peça conta a história do dossiê, pede o que os fatos sustentam e cumpre o que o escritório e o rito exigem.

## 1. A matriz pedido, fundamento, fato e prova

Monte uma tabela com cada pedido da peça:

| Pedido | Fundamento (item do direito) | Fato (item dos fatos) | Prova (doc.) | Situação |
|---|---|---|---|---|
| 3. restabelecimento desde a cessação | II.2 e II.3 | 2, 3 e 4 | docs. 1, 2, 4 e 5 | ok |
| 6. dano moral | nenhum | nenhum | nenhum | pedido sem fundamento: o advogado decide |

E o caminho de volta, a partir do dossiê (`casos/<codigo>/dossie.md`, da `dossie-do-caso`, se existir):

| Fato importante do dossiê | Está na peça? | Tem pedido ou argumento? | Situação |
|---|---|---|---|
| A perícia não enfrentou o relatório do médico assistente | fatos 4, direito II.3 | pedido 5 | ok |
| As datas de cessação divergem entre dois documentos | fatos 2 | a peça precisa escolher e explicar | o advogado decide qual data e se explica a divergência |
| Falta relatório médico posterior à cessação | não | não | lacuna: pedir ao cliente antes do protocolo |

Situações possíveis: `ok`, `pedido sem fundamento`, `fato sem pedido`, `prova faltando`, `contradição com o dossiê`, `lacuna`. Nenhuma é resolvida pela IA sozinha: a matriz mostra, o advogado decide o que fica.

## 2. Sobra de outro caso

O script acha nome em papel de parte e código de outro caso. Na leitura, procure também:
- fato que não está no dossiê (uma doença, um vínculo, uma cidade que não são do caso);
- outro tipo de benefício, de ação ou de rito no meio do texto;
- outra vara, outra comarca, outro tribunal no endereçamento ou no fecho;
- nome de empresa ou de parte contrária de outro caso (cruze com a base de partes, se a ficha indicar `base_de_partes`);
- data de fato muito antiga ou futura para o caso.

Cada achado vai para o relatório como alerta "sobra de outro caso", com a linha.

## 3. Requisitos formais

A habilidade não traz a lista de requisitos de cada peça como regra: requisito legal de peça fica `[CONFERIR]` na norma e no regimento. Os pontos abaixo são a lista de perguntas; o escritório confirma e guarda a lista da peça no modo adaptar.

| Ponto | Pergunta | Como entra no relatório |
|---|---|---|
| Endereçamento | O juízo e a competência estão certos para o caso? | `[CONFERIR]` competência e valor de alçada |
| Qualificação | As partes estão qualificadas como o rito pede? Os dados que entram pelo sistema do escritório estão marcados? | `[CONFERIR]` requisito da qualificação |
| Valor da causa | Existe, é um só, tem cálculo que o sustenta? | o script confere se é um só; o cálculo fica `[CONFERIR]` |
| Pedidos | Estão numerados, certos e determinados, cada um com o fundamento? | padrão da ficha (`pedidos`) |
| Provas | A peça diz quais provas quer produzir? | `[CONFERIR]` o requisito no rito |
| Opções do rito | Audiência de conciliação, juízo 100% digital, prioridade de tramitação: o rito pede manifestação? | `[CONFERIR]` no rito e no regimento |
| Documentos | Os documentos indispensáveis estão na lista? | lista do escritório para a peça |
| Assinatura | Quem assina está na ficha (`quem_assina`)? | a assinatura é da pessoa, nunca da IA |

## 4. O padrão da ficha jurídica

| Campo | O que conferir |
|---|---|
| `estilo` | Frases curtas, sem latim desnecessário, sem adjetivação vazia, o que o escritório nunca escreve |
| `pedidos` | Pedidos numerados, com o fundamento ao lado, do jeito da ficha |
| `citacao_em_recuo` | Citação longa em recuo, no corpo que a ficha diz |
| `tamanho_preferido` | A peça passou do tamanho do escritório? Aponte onde cortar, sem cortar fato importante |
| `nome_dos_arquivos` | A lista de documentos bate com o jeito de nomear os anexos para o protocolo |

Fora do padrão é ajuste, não bloqueio: vai para o relatório como "padrão" e o revisor ajusta.

## 5. Dado sensível

Saúde, criança, renda, vida íntima: entra na peça só o que o pedido precisa. O relatório aponta o excesso ("o diagnóstico completo aparece três vezes; o pedido precisa só da limitação para o esforço físico") e o advogado decide. CPF, endereço e número de documento entram pelo sistema do escritório, não pela conversa.

## 6. Como fechar o `dados`

- `ok`: nenhum alerta aberto. Alerta que o advogado decidiu manter (por exemplo, um documento da lista que a peça não cita de propósito) vai para o relatório com "decidido por: [função], AAAA-MM-DD".
- `com-alerta`: qualquer alerta do script ou da leitura ainda aberto.
- `nao-conferidos`: a conferência não rodou.
