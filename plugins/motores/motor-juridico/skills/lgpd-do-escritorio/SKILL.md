---
name: lgpd-do-escritorio
description: >
  A LGPD dentro do próprio escritório de advocacia: o mapa dos dados que o escritório trata
  (contatos, clientes, partes contrárias, testemunhas, equipe, fornecedores, uso de IA), a base
  legal de cada tratamento, o aviso de privacidade e os avisos à equipe, a resposta a pedido de
  titular, o roteiro de incidente de segurança, e a política de retenção e descarte. Toda citação
  da lei e da regulamentação nasce marcada para conferir. Use quando o advogado disser "monta o
  mapa de dados do escritório", "qual a base legal para guardar isso?", "preciso de um aviso de
  privacidade", "um ex-cliente pediu para apagar os dados", "mandaram o laudo para o grupo
  errado", "quanto tempo guardo os documentos?". Não use para LGPD de cliente empresa (use
  compliance-para-clientes) nem para conferir citações de uma peça (use conferir-citacoes).
---

# LGPD do escritório

> O escritório que trata dado de saúde, de criança e de renda de centenas de pessoas precisa saber o que guarda, por que guarda, por quanto tempo e o que fazer quando algo vaza. A habilidade monta o mapa e os documentos. O encarregado e o advogado decidem.

Regras do plugin: `../../docs/regras.md` (seção 6, dados de cliente). Citação: `../../docs/citacoes.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

Quarta, 16h. O estagiário manda o relatório médico da Marta para o grupo de WhatsApp da família de outro cliente, por engano. Ele apaga em dois minutos, mas três pessoas já viram. Ninguém sabe se isso precisa ser comunicado, a quem, em quanto tempo, nem quem decide. O roteiro de incidente, feito antes, diz: conter, registrar, avaliar o risco e levar ao encarregado hoje.

**Regras fixas desta habilidade:**
1. Toda citação da LGPD (Lei 13.709/2018), da regulamentação da ANPD e das normas da advocacia nasce marcada `[CONFERIR: ...]`, como manda `citacoes.md`. Só perde a marca quando alguém confere no texto oficial.
2. A habilidade propõe; o encarregado (`encarregado_lgpd`) e o advogado decidem: a base legal final, o aviso publicado, a resposta ao titular, a comunicação de incidente, o descarte.
3. Sigilo profissional vem junto com a LGPD. Pedido de dados que envolva o caso de um cliente (inclusive da parte contrária) vai para o advogado antes de qualquer resposta.
4. Nenhum prazo de retenção sai da cabeça da IA. Prazo é `[A DEFINIR]` pelo escritório, com o fundamento `[CONFERIR]`.
5. Incidente com dado sensível para a habilidade de rascunhar e vai para uma pessoa agora, no mesmo dia.

## 1. Quando usar

**Use quando:**
- O escritório quer saber que dados trata e onde estão (modo mapa).
- Precisa da base legal de um tratamento ("posso guardar a base de partes antigas?") (modo bases legais).
- Precisa do aviso de privacidade do site, do WhatsApp ou da cláusula do contrato, ou do aviso à equipe (modo avisos).
- Um titular pediu acesso, correção, cópia ou eliminação de dados (modo pedido de titular).
- Aconteceu ou pode ter acontecido um incidente: envio errado, celular perdido, acesso indevido, conta invadida (modo incidente).
- O escritório quer a política de retenção e o descarte do ano (modo retenção e descarte).
- Revisão anual, treino com o Escritório Modelo, ou a `adaptar-juridico` pediu (modos revisão, treino, adaptar).

**Não use quando:**
- O cliente é uma empresa que quer o programa de privacidade dela: `compliance-para-clientes` (se instalada; sem ela, o advogado conduz como consultivo).
- O pedido é conferir as citações de uma peça: `conferir-citacoes`.
- O pedido é uma ação judicial sobre LGPD para cliente: é peça, pelo caminho normal (`dossie-do-caso`, `estrategia-do-caso`).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`), `nicho.md` se existir e os aprendizados (`aprendizados-juridico.md`). O nicho diz quais dados sensíveis aparecem mais (saúde no previdenciário, criança na família, renda no consumidor).
2. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Quem responde por dados no escritório?".
3. **Leia o que existir** em `escritorio/04-base/juridico/lgpd/` (o mapa, a política, o aviso). Se o escritório usa o plugin `inicio-automacao`, leia também `escritorio/01-cultura/regra-de-uso-de-ia.md`: ela já diz o que entra na IA.
4. **Leia `references/bases-legais.md`** antes de propor base legal, e `references/pedido-de-titular-e-incidente.md` antes dos modos pedido e incidente.
5. **Conta de IA.** O mapa não leva dado de pessoa: leva categorias ("relatório médico de segurados"). Pedido de titular e incidente podem ter nome e dado: só em conta profissional, com o mínimo, e com a anonimização de `regras.md`, seção 6.

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `encarregado_lgpd` |
| Melhora | E: `conta_de_ia`, ferramentas (seção 6 da ficha do escritório: `historico_do_cliente`, `sistema_juridico`, `agenda`, `whatsapp`, `conectores_no_claude`, `onde_roda`) |

Campo que falta e a tarefa pede: pergunte aquele campo, uma vez, e ofereça gravar. Sem `encarregado_lgpd`, todo documento sai com "Encarregado: `[A DEFINIR]`" e o fim da tarefa avisa que essa é a primeira decisão a tomar.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Mapa | Primeira vez, ou revisão | O mapa de dados, por atividade (`assets/mapa-de-dados.md`) |
| Bases legais | Depois do mapa, ou uma pergunta só | A base proposta por linha, marcada, para o encarregado decidir |
| Avisos | Site, WhatsApp, contrato, equipe | O aviso com o cabeçalho interno "Antes de publicar" (`assets/aviso-de-privacidade.md`) |
| Pedido de titular | Chegou um pedido | Registro, prazo e a resposta-base para a pessoa revisar |
| Incidente | Algo vazou ou pode ter vazado | O roteiro do dia e o registro (`assets/registro-de-incidente.md`) |
| Retenção e descarte | Política, ou o descarte do ano | A tabela de retenção e a lista do que descartar, para aprovar |
| No ciclo | Pedido ou incidente chegou pela entrada | Linha em ADVOGADO AGORA e, no pedido, a resposta-base na fila |
| Revisão | Uma vez por ano, ou quando muda ferramenta | O mapa e a política atualizados, com `[ALTERADO]` |
| Treino | Escritório Modelo | Tudo em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | O mapa do nicho, para aprovar |

Pergunta direta ("posso guardar o WhatsApp do contato que não fechou?"): não faça entrevista. Responda pela linha do mapa (ou monte a linha), com a base proposta e a marca, e pergunte só o que falta.

### Modo mapa
**Passo 1.** Explique em uma frase: "Vou passar por cada atividade do escritório e perguntar que dados entram, de quem, para quê, onde ficam e por quanto tempo."
**Passo 2.** Percorra as atividades de `assets/mapa-de-dados.md`, uma por vez: contato que ainda não é cliente; consulta; contrato e honorários; condução do caso (documentos do cliente, dados da parte contrária e de testemunhas); comunicação com o cliente; financeiro; equipe; fornecedores e parceiros; divulgação e site; uso de IA; base de partes e conflito. Para cada uma, pergunte só: "Que dados entram aqui?", depois "Onde ficam e quem acessa?". Peça a cena concreta quando vier vago ("fica no drive" vira "em que pasta, e quem tem o link?").
**Passo 3.** Marque o dado sensível (saúde, criança ou adolescente, biometria, origem racial, religião, filiação sindical, vida sexual, opinião política) e o que vai para fora do escritório (sistema na nuvem, IA, contador, correspondente).
**Passo 4.** Aponte, sem julgar: dado que ninguém sabe por que guarda, pasta com link aberto, dado sensível em conta pessoal, documento que fica no celular de alguém. Cada ponto vira uma linha em "O que corrigir", com dono e data `[A DEFINIR]`.
**Passo 5.** Mostre o mapa e grave com o ok em `04-base/juridico/lgpd/mapa-de-dados.md`.
**Passo 6. Aprender** (abaixo).

### Modo bases legais
1. Para cada linha do mapa, proponha a base legal pela tabela de `references/bases-legais.md`, com a citação marcada (`art. 7º, V, da Lei 13.709/2018 [CONFERIR: inciso e redação vigente]`) e uma frase do porquê.
2. Dado sensível: proponha pela lista própria do dado sensível (`art. 11 [CONFERIR]`), nunca pela lista geral.
3. Quando duas bases cabem, mostre as duas e diga o que muda (consentimento pode ser revogado; obrigação legal não). Legítimo interesse pede o teste de balanceamento (`references/bases-legais.md`, seção 3) registrado.
4. A decisão é do encarregado: grave a base escolhida, quem decidiu e a data na linha do mapa. A marca da citação sai só depois da conferência no texto oficial (`conferir-citacoes`, se instalada; sem ela, o encarregado confere no portal da legislação federal e anota a data).

### Modo avisos
1. Pergunte: "Onde o aviso vai aparecer? Site, primeira mensagem do WhatsApp, contrato, formulário, equipe?".
2. Preencha `assets/aviso-de-privacidade.md` com o mapa e a ficha: quem é o escritório, que dados, para quê, com quem compartilha, por quanto tempo, como pedir, quem é o encarregado e o contato dele. Linguagem simples, frases curtas, no tom da ficha.
3. As conferências ficam no cabeçalho interno "Antes de publicar": a citação de cada direito e base, o contato do encarregado, a política de retenção. O texto ao público cita a lei pelo nome e não leva marcação.
4. Versão curta para o WhatsApp (até 3 linhas, com o link do aviso completo) e a cláusula para o contrato de honorários (a `contrato-de-honorarios`, do motor-comercial, se instalado, recebe a cláusula).
5. Texto que vai a público segue o Provimento 205/2021 do CFOAB `[CONFERIR]`: informativo, sem propaganda. Mostre e grave com o ok; quem publica é a pessoa.

### Modo pedido de titular
Siga `references/pedido-de-titular-e-incidente.md`, seção 1:
1. **Registrar** em `07-operacao/juridico/lgpd/pedidos/AAAA-MM-DD-NN.md`: data de chegada, canal, quem pediu (iniciais), o que pediu, o prazo `[CONFERIR: prazo de resposta da lei e da regulamentação]`.
2. **Identificar** quem pede: titular, representante, parte contrária, terceiro. Parte contrária ou terceiro pedindo dados de um caso: para e vai para o advogado (regra fixa 3).
3. **Achar os dados** pelo mapa: onde a pessoa aparece.
4. **Ver o que pode e o que não pode**: dado guardado por obrigação legal ou para defesa em processo (`art. 16 [CONFERIR]`), sigilo profissional, dado de terceiro misturado.
5. **Rascunhar a resposta** pela base da referência, curta e sem juridiquês, com as conferências no cabeçalho "Antes de enviar". A pessoa revisa e envia pelo canal oficial.
6. **Fechar o registro** com a data da resposta e o que foi feito.

### Modo incidente
Siga `references/pedido-de-titular-e-incidente.md`, seção 2. A ordem não muda:
1. **Conter agora** (pessoa): apagar o envio errado onde der, trocar senha, revogar link, bloquear o aparelho.
2. **Avisar hoje** o encarregado e o advogado responsável. A habilidade não espera o fim do roteiro para isso.
3. **Registrar** em `07-operacao/juridico/lgpd/incidentes/AAAA-MM-DD.md` (`assets/registro-de-incidente.md`): o que aconteceu, quando o escritório soube, que dados, de quantos titulares, se há dado sensível, o que já foi feito.
4. **Avaliar o risco** com as perguntas da referência. A conclusão é do encarregado.
5. **Decidir a comunicação** à ANPD e aos titulares: é do encarregado e do advogado, no prazo da regulamentação `[CONFERIR: art. 48 da Lei 13.709/2018 e a resolução da ANPD sobre comunicação de incidente, prazo e conteúdo vigentes]`. A habilidade prepara o rascunho da comunicação; quem envia é a pessoa.
6. **Corrigir a causa** e registrar o aprendizado.

### Modo retenção e descarte
1. Para cada categoria do mapa, monte a linha de `references/bases-legais.md`, seção 4: o prazo fica `[A DEFINIR]` pelo escritório, com o fundamento sugerido `[CONFERIR]` (prazo de prescrição, guarda fiscal, devolução de documentos ao cliente no fim do caso).
2. Mostre a política e grave com o ok em `04-base/juridico/lgpd/politica-de-retencao.md`.
3. **Descarte do ano:** a partir da política, liste o que venceu, por categoria e lugar (pasta, sistema, celular, papel), sem abrir documento. Inclua o que é do próprio plugin: `entrada/lidos/` com mais de 7 dias, `_treino/` que não serve mais, rascunhos descartados da fila.
4. Quem apaga é a pessoa. A habilidade registra o que foi descartado, quando e por quem em `07-operacao/juridico/lgpd/descartes.md`, sem nomes de titulares (categoria e quantidade).

### Modo no ciclo
O `agente-juridico` não roda o mapa. Se chegar à `entrada/` um pedido de titular ou o relato de um incidente:
- **Pedido de titular:** registro aberto (passo 1 do modo), linha em ADVOGADO AGORA com o prazo, e a resposta-base na fila (`fila/AAAA-MM-DD/NN-<codigo>-pedido-titular.md`, com `revisor: pendente`). Pedido da parte contrária ou de terceiro: nenhum rascunho.
- **Incidente:** linha em ADVOGADO AGORA, sem rascunho, com "avisar o encarregado hoje".

### Modo treino
Escritório Modelo (`../../docs/casos-ficticios.md`), com dois casos de mentira: o envio errado do relatório médico da Marta (C-2026-0001) e o pedido do Jorge (C-2025-0088, cliente encerrado) para apagar os dados dele. Tudo grava em `escritorio/07-operacao/_treino/juridico/lgpd/`. O que não pode falhar: no incidente, avisar o encarregado antes de qualquer rascunho, dado de saúde marcado, comunicação decidida por pessoa; no pedido do Jorge, separar o que pode ser apagado do que fica por obrigação ou defesa `[CONFERIR]`, e a decisão com o advogado.

### Modo adaptar
Leia `nicho.md` e proponha as linhas do mapa típicas do nicho (previdenciário: CNIS, laudos, perícias; família: dados de criança, renda, partilha; trabalhista: holerites, cartões de ponto, atestados), marcadas `[ALTERADO]`. Grave no mapa com o ok.

### Aprender (último passo de todo modo)
Pergunte: "Alguma coisa nesse mapa ou nesse documento não é assim no escritório?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Decisão que virou política (por exemplo, "contato que não fechou sai do WhatsApp em 6 meses") vai para a política de retenção, com linha no histórico.

## 4. O que cada documento leva

| Documento | Seções | Quem decide |
|---|---|---|
| Mapa de dados | Por atividade: dados, titulares, sensível, finalidade, base legal, onde fica, quem acessa, compartilha com, IA, retenção, o que corrigir | Encarregado |
| Política de retenção | Por categoria: prazo `[A DEFINIR]`, fundamento `[CONFERIR]`, como descartar, quem descarta | Encarregado e advogado titular |
| Aviso de privacidade | Quem somos, que dados, para quê, com quem, por quanto tempo, direitos, como pedir, encarregado | Encarregado; publica a pessoa |
| Aviso à equipe | O que entra na IA, o que nunca entra (`regras.md`, seção 6), onde guardar, o que fazer num incidente | Advogado titular |
| Registro de pedido | Chegada, quem pede, o que pede, prazo, dados achados, o que pode, resposta, data | Encarregado; responde a pessoa |
| Registro de incidente | O que, quando soube, dados, titulares, sensível, contenção, risco, comunicação, causa | Encarregado e advogado |

Todo documento leva no topo `documento`, `versao`, `revisado_em` e `dono` (`regras.md`, seção 7). As citações seguem `citacoes.md`: marcadas até a conferência; no texto público, só o nome da lei, e a conferência no cabeçalho interno.

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Mapa de dados (com as bases legais decididas) | `escritorio/04-base/juridico/lgpd/mapa-de-dados.md` |
| Política de retenção | `escritorio/04-base/juridico/lgpd/politica-de-retencao.md` |
| Aviso de privacidade, versão curta e cláusula | `escritorio/04-base/juridico/lgpd/aviso-de-privacidade.md` |
| Aviso à equipe | `escritorio/04-base/juridico/lgpd/aviso-a-equipe.md` |
| Pedidos de titular | `escritorio/07-operacao/juridico/lgpd/pedidos/AAAA-MM-DD-NN.md` |
| Incidentes | `escritorio/07-operacao/juridico/lgpd/incidentes/AAAA-MM-DD.md` |
| Registro de descartes | `escritorio/07-operacao/juridico/lgpd/descartes.md` |
| Resposta ao titular (no ciclo) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/` |
| Treino | `escritorio/07-operacao/_treino/juridico/lgpd/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

O mapa, a política e os avisos não têm dado de pessoa e podem ir para o Projeto no Claude. Pedidos e incidentes têm, e ficam em `07-operacao/`, fora do Projeto. Sem pasta aberta: cada documento vem no chat, em bloco, com o caminho onde ficaria.

## 6. Solo e equipe

**Solo:** o advogado é o encarregado de fato. Comece pelo mapa das três atividades com mais dado sensível e pelo roteiro de incidente; o resto entra na revisão do ano.

**Equipe:** o encarregado (`encarregado_lgpd`) é dono do mapa e decide as bases; cada pessoa da equipe recebe o aviso à equipe e sabe o primeiro passo de um incidente (conter e avisar). Pedido de titular que chega a qualquer pessoa vai ao encarregado no mesmo dia.

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Artigo da LGPD citado de memória | Documento com base errada | Toda citação marcada até a conferência |
| Consentimento como base para tudo | Cliente revoga e o escritório não pode mais defender o caso | Tabela de bases, com o que muda em cada uma |
| Apagar tudo a pedido de ex-cliente | Escritório sem prova numa cobrança ou numa ação futura | Separar o que fica por obrigação ou defesa `[CONFERIR]`, com o advogado |
| Responder à parte contrária sobre o cliente | Quebra de sigilo profissional | Pedido de terceiro vai ao advogado, sem rascunho |
| Incidente resolvido em silêncio | Prazo de comunicação perdido | Avisar o encarregado no mesmo dia; decisão registrada |
| Prazo de guarda inventado | Política que não se sustenta | Prazo `[A DEFINIR]` com fundamento `[CONFERIR]` |
| Dado sensível na conta pessoal de IA | Exposição de saúde e de criança | Linha "uso de IA" no mapa e o aviso à equipe |

## 8. Próximo passo

- Mapa pronto: bases legais, depois o aviso de privacidade e a política de retenção.
- Cláusula de dados no contrato: `contrato-de-honorarios`, do motor-comercial (se instalado).
- Citações marcadas dos documentos: `conferir-citacoes`.
- Cliente empresa pedindo o mesmo trabalho: `compliance-para-clientes` (se instalada).

## Referências desta habilidade

- `references/bases-legais.md`: as bases legais com as citações marcadas, o dado sensível, o teste do legítimo interesse e o modelo da política de retenção. Leia no modo bases legais e no modo retenção.
- `references/pedido-de-titular-e-incidente.md`: o passo a passo do pedido de titular, com a resposta-base, e o roteiro de incidente, com as perguntas de risco. Leia nos modos pedido e incidente.
- `assets/mapa-de-dados.md`: o modelo do mapa, com as atividades de um escritório. Use no modo mapa.
- `assets/aviso-de-privacidade.md`: o modelo do aviso, da versão curta, da cláusula e do aviso à equipe. Use no modo avisos.
- `assets/registro-de-incidente.md`: o modelo do registro de incidente. Use no modo incidente.
