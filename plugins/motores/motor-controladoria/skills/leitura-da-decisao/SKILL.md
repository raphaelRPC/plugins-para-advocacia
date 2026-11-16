---
name: leitura-da-decisao
description: >
  Lê a sentença, o acórdão ou a decisão que chegou na publicação e organiza para quem decide:
  o dispositivo em trecho literal, o que foi decidido em uma frase, o que mudou para o cliente,
  o recurso que pode caber e o prazo pela tabela do escritório (tudo marcado para conferir), o
  que passar ao jurídico e como o cliente fica sabendo, com notícia ruim sempre por ligação.
  Nunca diz se vale recorrer. Use quando a pessoa disser "saiu a sentença do Otávio, o que
  ela diz?", "lê esse acórdão", "o que mudou com essa decisão?", "cabe recurso?", "qual o
  prazo do recurso?", "como eu conto isso para a cliente?". Não use para decidir a
  estratégia ou se vale recorrer (use estrategia-do-caso, do motor-juridico, se instalado)
  nem para escrever o recurso (use o motor-juridico, se instalado).
---

# Leitura da decisão

> O dispositivo copiado do jeito que está, o que ele muda para o cliente em linguagem simples e o que a tabela do escritório diz sobre o recurso. Quem decide se recorre é o advogado, com o cliente.

Regras comuns: `../../docs/regras.md`. Contagem e prazos por ato: `../../docs/contagem.md`. Registros: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Terça, 9h. Duas sentenças de improcedência no lote, a do Otávio no JEF e a da Camila no TRT3. A estagiária precisa saber o que mandar para a advogada; a advogada precisa ver o dispositivo sem ler a sentença inteira de novo, o recurso que a tabela do escritório aponta e até quando; e ninguém pode mandar mensagem para o Otávio ou para a Camila antes de a advogada ligar.

**Regras fixas desta habilidade:**
1. Nunca diz se vale recorrer, se a decisão está certa ou qual a chance do recurso. Mostra o que foi decidido e o que pode caber; a decisão é do advogado com o cliente.
2. O dispositivo vem em trecho literal, copiado do teor. Resumo nenhum substitui o trecho.
3. O recurso que pode caber e o número de dias vêm da tabela do escritório (`regras-de-contagem.md`, "Prazos por ato"), sempre `[CONFERIR]`. Sem linha na tabela: `[A CONFIRMAR: quantos dias]`. Nunca da memória.
4. Desfavorável, parcial ou na dúvida: o cliente fica sabendo por ligação do advogado, nunca por mensagem.
5. Pesquisa de jurisprudência, se a pessoa pedir, é só no Jus IA, e o que vier entra como não conferido.

## 1. Quando usar

**Use quando:**
- A triagem marcou uma publicação como sentença, acórdão ou decisão (liminar, tutela, decisão interlocutória que muda o caso).
- A pessoa pergunta o que a decisão diz, o que mudou ou o que pode caber.
- A advogada vai decidir a providência e quer a leitura antes (a `providencia-sugerida` vem depois).
- O `agente-de-controladoria` grava um `decidir-providencia` de decisão (modo no ciclo).
- Treino com as linhas 1 e 3 do lote de `../../docs/casos-ficticios.md`.

**Não use quando:**
- O pedido é a estratégia (recorrer, fazer acordo, desistir): `estrategia-do-caso` do motor-juridico (se instalado). Sem ele, a decisão é conversa do advogado.
- O pedido é escrever o recurso: motor-juridico (se instalado), pelo pedido de peça da `encaminhar-providencia`.
- O pedido é a mensagem ao cliente: `status-para-o-cliente` do motor-experiencia (se instalado). Notícia ruim é ligação.
- O ato é despacho de rotina, sem decisão: `triar-publicacoes` e `providencia-sugerida` resolvem.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` e `aprendizados-controladoria.md`, se existirem.
2. Sem fichas: ofereça `/motor-controladoria:comecar`. Para seguir agora, pergunte só: "Em que áreas o escritório atua?".
3. Leia o teor em `escritorio/07-operacao/controladoria/publicacoes/AAAA-MM-DD/<id>.md`, a linha da publicação em `publicacoes.csv` e a linha do prazo em `prazos.csv`, se houver.
4. Leia a tabela de regras do escritório (`escritorio/04-base/controladoria/regras-de-contagem.md`), seção "Prazos por ato", e veja se está validada (`validada_por`). Sem validação, o aviso "regra ainda não validada pelo escritório" vai no cabeçalho interno.
5. Dados: decisão com dado de saúde, de criança ou de processo em segredo de justiça só com autorização expressa do advogado responsável. Na leitura, o mínimo ("laudo concluiu pela capacidade"), nunca o diagnóstico.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas`.
- **Melhora:** K: `quem_decide_providencia`.
- Lê também, se preenchidos: E: `nicho`, `como_o_cliente_fala`; K: `responsaveis_por_area`, `regras_validadas_por`.

`quem_decide_providencia` vazio: pergunte uma vez ("Quem decide o que fazer com esta decisão?") e ofereça gravar; sem resposta, a seção "Para decidir" fica `[A PREENCHER]`.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| A pedido | A pessoa traz a decisão | A leitura completa, mostrada antes de gravar | `decisoes/<codigo>/AAAA-MM-DD.md` |
| Rápido | "cabe recurso? qual o prazo?" | Só as seções 1, 2 e 4 do modelo | No chat |
| No ciclo | O agente chama | A leitura, sem perguntar, e o item para decidir | O arquivo e `fila/AAAA-MM-DD/NN-<codigo>-providencia.md` |
| Treino | Linhas 1 e 3 do lote | O mesmo, em `_treino/` | `escritorio/07-operacao/_treino/controladoria/decisoes/` |
| Adaptar | `adaptar-controladoria` | O jeito de explicar o que mudou, no vocabulário do nicho | `04-base/controladoria/nicho/leitura-da-decisao.md` |

### Passo 1. Achar o dispositivo (S)
No teor, ache a parte que decide ("Ante o exposto", "Isso posto", "Pelo exposto", "ACORDAM", "defiro", "indefiro") e copie o trecho inteiro, sem mudar uma palavra. Se o teor está cortado ou ilegível, pare e peça o teor completo: sem dispositivo, não há leitura.

### Passo 2. O que foi decidido (S, conferido por H)
Uma frase, sem termo técnico. Classifique a leitura para o cliente: desfavorável (improcedente, negado, extinto sem resolver o pedido, laudo contrário), parcial (procedente em parte), favorável (procedente, concedido), neutra (decisão de andamento). Na dúvida entre duas, a mais cuidadosa: parcial vale como desfavorável para o caminho (ligação).

### Passo 3. O que mudou para o cliente (A)
O que muda agora, o que não muda e os outros pontos do dispositivo (custas, honorários, justiça gratuita, tutela, multa, o que precisa ser cumprido e por quem). Sem previsão de resultado, de prazo de decisão ou de chance do recurso.

### Passo 4. O recurso que pode caber e o prazo (S, `[CONFERIR]`)
Procure na tabela "Prazos por ato" do escritório as linhas do rito do caso para o tipo de ato. Mostre cada uma com os dias, a contagem e a fonte, todas `[CONFERIR]`. Não tem linha: `[A CONFIRMAR: qual recurso e quantos dias]`, para a pessoa. A data vem da `calcular-prazo` (se ainda não há linha em `prazos.csv`, chame-a; sem ela, a conta passo a passo de `contagem.md`), e vale depois da dupla conferência. Diga, em uma linha: "A leitura não diz se vale recorrer."

### Passo 5. O que passar ao jurídico (A)
Os trechos dos fundamentos principais e os pontos que a estratégia vai precisar olhar, sem indicar o caminho. O pedido de peça só sai depois da decisão (passo 8), pela `encaminhar-providencia`.

### Passo 6. Como o cliente fica sabendo (H)
Desfavorável, parcial ou a confirmar: ligação do advogado, com o roteiro da `status-para-o-cliente` (se instalada), que recebe o aviso pela `encaminhar-providencia` com `--aviso decisao --noticia ruim`. Sem a experiência, o roteiro curto do modelo, para quem liga. Favorável ou neutra: mensagem lida pelo advogado antes de sair, sem comemorar o que ainda pode mudar.

### Passo 7. Pesquisa (só se pedirem)
Se a pessoa pedir jurisprudência sobre o ponto da decisão: a pesquisa é no Jus IA, pelo caminho do motor-juridico (se instalado; `trazer-pesquisa`), e tudo o que vier entra como não conferido. Sem o motor-juridico, a pessoa pesquisa no Jus IA e traz o resultado; nenhum julgado sai da memória da IA.

### Passo 8. Mostrar e perguntar (H)
Mostre a leitura no formato de `assets/modelo-da-leitura.md`, com o cabeçalho interno. Pergunte a quem decide: "O que fazemos com esta decisão?". Com a resposta, grave na seção 8 a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` e chame a `encaminhar-providencia` (se instalada) para o pedido de peça e o aviso ao cliente. Correção da leitura feita pela pessoa: preencha `conferida_por` com o nome que ela disser.

### Passo 9. Aprender
Pergunte: "Alguma coisa na leitura você explicaria de outro jeito?". Cada correção vira uma regra curta ("Em sentença do JEF, sempre mostrar se houve condenação em honorários na primeira instância") e, com o ok, entra em `aprendizados-controladoria.md`. Linha de recurso que faltou na tabela: ofereça levá-la para a validação da tabela pela `calendario-forense` (se instalada).

### No ciclo (o agente chama)
1. Não pergunte nada. Faça os passos 1 a 5 e grave a leitura em `decisoes/<codigo>/AAAA-MM-DD.md`.
2. Grave o item `decidir-providencia` na fila, com o dispositivo literal, a leitura para o cliente e a linha da tabela, e `revisor: pendente`.
3. Desfavorável ou parcial: linha em PESSOA AGORA ("sentença desfavorável do C-2026-0012: a advogada liga antes de qualquer mensagem"). Nenhum aviso é encaminhado antes da decisão.
4. Nunca grave `decidido por` nem `conferida_por` no ciclo.

### Modo adaptar
Leia `nicho.md` (como o cliente fala, o que ele entende por "perdeu" ou "ganhou") e os aprendizados. Reescreva os exemplos das seções 2 e 3 do modelo no vocabulário do nicho, marque cada mudança `[ALTERADO]` e grave em `escritorio/04-base/controladoria/nicho/leitura-da-decisao.md` só com o ok.

## 4. Exemplos resolvidos (Escritório Modelo, tabela de treino)

**Linha 1 · Otávio · C-2026-0012 · TRF6, JEF · disponibilizada 2026-04-13.**
- Dispositivo: "Ante o exposto, JULGO IMPROCEDENTE o pedido, com resolução do mérito. Sem custas e honorários nesta instância."
- Em uma frase: o pedido de benefício não foi atendido. Leitura para o cliente: desfavorável.
- O que mudou: o benefício continua sem ser pago; não há custas nem honorários nesta instância; o processo ainda não acabou.
- Recurso que pode caber (tabela de treino): recurso inominado, juizado-federal, 10 dias úteis `[CONFERIR]`. Conta: publicada 2026-04-14, início 2026-04-15, fatal 2026-04-30, segurança 2026-04-28 (PZ-2026-0001, depois da dupla conferência). Embargos de declaração no juizado federal: a tabela de treino não tem a linha, então `[A CONFIRMAR: quantos dias]`.
- Cliente: ligação da advogada antes de qualquer mensagem.
- Para decidir: "O que fazemos com esta decisão?". No treino, a advogada decide pelo recurso e liga; a `encaminhar-providencia` faz o pedido de peça e o aviso de decisão com `noticia: ruim`.

**Linha 3 · Camila · C-2026-0010 · TRT3 · disponibilizada 2026-04-09, captada só em 2026-04-14.**
- Dispositivo: "Ante o exposto, julgo IMPROCEDENTES os pedidos formulados na reclamação trabalhista. Concedo à reclamante os benefícios da justiça gratuita. Custas pela reclamante, dispensadas."
- Leitura para o cliente: desfavorável. Outros pontos: justiça gratuita concedida; custas dispensadas.
- Recurso que pode caber (tabela de treino): recurso ordinário, trabalhista, 8 dias úteis `[CONFERIR]`; fatal 2026-04-24, segurança 2026-04-22 (PZ-2026-0003, ainda `sugerido`). Captada com atraso: vai para o topo do resumo.
- Cliente: ligação da advogada; a Camila já perguntou "saiu alguma coisa?", e a resposta é o convite para a ligação, sem o resultado.

O que não pode falhar: nenhuma frase do tipo "vale recorrer" ou "a sentença errou"; o dispositivo literal; os dias marcados `[CONFERIR]`; nenhuma mensagem com o resultado.

## 5. Formato da saída

O documento de `assets/modelo-da-leitura.md`. No modo rápido, no chat:
```
DECISÃO · [código] · [tipo] · disponibilizada [data] · leitura: [desfavorável | parcial | favorável | neutra]
Dispositivo: "[trecho literal]"
Pode caber (tabela do escritório, CONFERIR): [recurso] · [dias] [contagem] · segurança [data] · fatal [data] · [status]
Cliente: [ligação | mensagem lida pelo advogado]
A leitura não diz se vale recorrer. O que fazemos com esta decisão?
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A leitura | `escritorio/07-operacao/controladoria/decisoes/<codigo>/AAAA-MM-DD.md` (data da disponibilização) |
| Item para decidir (no ciclo) | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-providencia.md` |
| A decisão da pessoa | Seção 8 da leitura e o item da fila: `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` |
| Jeito de explicar adaptado | `escritorio/04-base/controladoria/nicho/leitura-da-decisao.md` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/decisoes/<codigo>/` |

A leitura tem dado do caso: fica em `07-operacao/`, fora do Projeto no Claude. Sem pasta aberta: o documento no chat, em bloco para copiar, com o caminho.

## 7. Solo e equipe

**Solo:** leia a decisão no mesmo dia em que chega, decida a providência e ligue para o cliente antes de ele ver no site. A leitura poupa a releitura; a decisão continua sua.

**Equipe:** a controladoria prepara a leitura; quem decide (`quem_decide_providencia`) confere o dispositivo e decide; o advogado responsável liga; o jurídico recebe o pedido de peça.

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| "Vale recorrer" dito pela IA | Decisão de caso fora do advogado | Regra fixa 1 |
| Resumo no lugar do dispositivo | Leitura errada do que foi decidido | Regra fixa 2 |
| Prazo de recurso de memória | Data errada para a peça | Regra fixa 3; tabela do escritório e `[CONFERIR]` |
| Sentença ruim por mensagem | O cliente lê sozinho a pior notícia | Regra fixa 4 |
| Julgado inventado na leitura | Citação que não existe | Regra fixa 5; só Jus IA e não conferido |
| Ponto acessório esquecido (custas, tutela revogada) | Cliente surpreendido depois | Seção "outros pontos do dispositivo" |
| Decisão lida tarde | Prazo curto para conversar com o cliente | Leitura no dia; captada com atraso vai para o topo |

## 9. Próximo passo

- A decisão de quem decide: `encaminhar-providencia` (se instalada) para o pedido de peça e o aviso ao cliente.
- O prazo do recurso: `calcular-prazo` e `dupla-conferencia`.
- A estratégia: `estrategia-do-caso` do motor-juridico (se instalado).
- A ligação: `status-para-o-cliente` do motor-experiencia (se instalado).

## Referências desta habilidade

- `assets/modelo-da-leitura.md`: o documento da leitura, com o cabeçalho interno e as oito seções. Passo 8 e o modo no ciclo.
