---
name: providencia-sugerida
description: >
  Monta com quem decide a tabela do escritório "tipo de ato, providência de costume"
  (04-base/controladoria/providencias.md), a partir das peças que o escritório já faz, e usa
  essa tabela para sugerir, em cada publicação triada, a providência e a peça de costume, com
  o trecho literal do ato e o aviso ao cliente que costuma vir junto. Sempre como sugestão
  para a pessoa decidir na fila; nunca decide, nunca encaminha. Use quando a pessoa disser "o
  que a gente costuma fazer com isso?", "monta a tabela de providências", "o que essa
  publicação pede?", "sugere a providência das publicações de hoje", "sempre que sai
  sentença de improcedência no JEF a gente recorre, guarda isso". Não use para encaminhar o
  que já foi decidido (use encaminhar-providencia) nem para ler uma sentença ou acórdão por
  inteiro (use leitura-da-decisao).
---

# Providência sugerida

> O escritório já sabe o que fazer com a maior parte das publicações: está na cabeça de quem decide. A tabela tira isso da cabeça, e a sugestão chega pronta para a pessoa dizer sim, não ou outra coisa.

Regras comuns: `../../docs/regras.md`. Registros e triagem: `../../docs/prazos.md`. Fichas: `../../docs/ficha-da-controladoria.md`. Fila e ciclo: `../../docs/agentes-e-fila.md`. Onde gravar: `../../docs/pasta.md`. Treino: `../../docs/casos-ficticios.md`. Nicho: `../../docs/adaptar-ao-escritorio.md`. Correções: `../../docs/aprender-com-o-uso.md`.

Segunda, 8h30, catorze publicações triadas. A estagiária sabe que sentença de improcedência no JEF "costuma virar recurso", mas não sabe se a advogada quer ligar antes, se a peça tem nome no jurídico, se a intimação para juntar relatório médico pede também uma mensagem para a cliente. Com a tabela, cada item da fila chega com o trecho do ato, a linha do costume que bateu e a pergunta para a advogada: "O que fazemos com esta publicação?".

**Regras fixas desta habilidade:**
1. A habilidade sugere e nunca decide. A sugestão vai para a fila como `item: decidir-providencia`, e só a pessoa de `quem_decide_providencia` diz o que fazer.
2. A sugestão vem da tabela do escritório, nunca da memória da IA. Sem linha que bata, a sugestão é "sem costume registrado", e a pessoa decide do zero.
3. Toda sugestão leva o trecho literal do ato que bateu com a linha da tabela. Sem trecho, não há sugestão.
4. Prazo da outra parte, duplicada e publicação sem caso não ganham sugestão de providência: vão para ciência ou para a pessoa, como a triagem marcou.
5. Número de dias e recurso cabível não moram nesta tabela: vêm do ato ou da tabela de prazos por ato do escritório, sempre `[CONFERIR]`.

## 1. Quando usar

**Use quando:**
- O escritório ainda não tem a tabela de providências, ou quer revisá-la (modo montar).
- Publicações foram triadas e precisam de sugestão antes de a pessoa decidir (modo sugerir).
- A pessoa decidiu algo que vale para as próximas vezes ("sempre que...") e quer guardar (modo guardar).
- O `agente-de-controladoria` grava os itens `decidir-providencia` na fila (modo no ciclo).
- Treino com o lote de `../../docs/casos-ficticios.md` e a tabela `assets/providencias-de-treino.md`.

**Não use quando:**
- A pessoa já decidiu: `encaminhar-providencia` (se instalada). Sem ela, o texto do pedido vai para a pessoa copiar.
- O ato é sentença, acórdão ou decisão que precisa ser lido por inteiro: `leitura-da-decisao` (se instalada) primeiro; a sugestão vem depois.
- O pedido é dizer se vale recorrer: decisão do advogado com o cliente. A tabela registra o costume, não a estratégia do caso.
- O pedido é calcular o prazo: `calcular-prazo`.

## 2. Antes de começar

1. Leia as fichas (`escritorio/04-base/comum/ficha-do-escritorio.md` e `ficha-da-controladoria.md`), `nicho.md` e `aprendizados-controladoria.md`, se existirem.
2. Sem fichas: ofereça `/motor-controladoria:comecar`. Para seguir agora, pergunte só: "Quem decide o que fazer com cada publicação aqui?".
3. Leia a tabela do escritório (`escritorio/04-base/controladoria/providencias.md`). Sem ela, o modo é montar (ou, no treino, `assets/providencias-de-treino.md`).
4. Leia as publicações triadas em `escritorio/07-operacao/controladoria/publicacoes.csv` (triagem `prazo`, `audiencia`, `pericia`, `urgente`, ou `ciencia` com algo a acompanhar) e o teor de cada uma em `publicacoes/AAAA-MM-DD/`.
5. Com o motor-juridico instalado, leia os nomes das peças que o escritório faz: as pastas de `escritorio/04-base/juridico/modelos/` e a coluna `peca` de `escritorio/07-operacao/juridico/pecas.csv`. São esses nomes que a tabela usa.

### Campos da ficha que esta habilidade usa

- **Precisa:** E: `areas` · K: `quem_decide_providencia`.
- **Melhora:** K: `regras_proprias`.
- Lê também, se preenchidos: E: `casos_mais_comuns`, `nicho`; K: `responsaveis_por_area`, `tribunais`.

`quem_decide_providencia` vazio: pergunte uma vez ("Quem decide o que fazer com cada publicação: a advogada responsável pelo caso, o sócio, outra pessoa?") e ofereça gravar. Sem resposta, a coluna `quem_decide` da sugestão fica `[A PREENCHER]`, e o item vai para PARA DECIDIR.

## 3. Fluxo

### Modos

| Modo | Quando | O que faz | Saída |
|---|---|---|---|
| Montar | Sem tabela, ou revisão | Entrevista com quem decide, linha por linha | `04-base/controladoria/providencias.md` |
| Sugerir | Publicações triadas | Uma sugestão por publicação, com o trecho e a linha da tabela | No chat, para a pessoa decidir |
| Guardar | "sempre que..." | Linha nova ou ajustada na tabela | `providencias.md`, nova versão |
| No ciclo | O agente chama | Sugestões na fila, sem perguntar | `fila/AAAA-MM-DD/NN-<codigo>-providencia.md` |
| Treino | Lote de treino | Sugerir com a tabela de treino | `escritorio/07-operacao/_treino/controladoria/` |
| Adaptar | `adaptar-controladoria` | A tabela reescrita para o nicho | `04-base/controladoria/nicho/providencia-sugerida.md` |

### Modo montar (A, a pessoa decide cada linha)
1. Comece pelo que já existe: "Quais são as peças que vocês mais fazem depois de uma intimação?". Mostre a lista das peças do motor-juridico, se houver, e as áreas da ficha.
2. Para cada área, percorra os atos que mais chegam, um por vez, com a pergunta exata: "Quando sai [ato] em [área], o que vocês costumam fazer, e o cliente fica sabendo como?". Exemplo: "Quando sai uma sentença de improcedência no JEF, o que vocês costumam fazer, e o cliente fica sabendo como?".
3. Peça a cena concreta quando vier vago ("depende" vira "e na última sentença assim, o que foi feito?"). "Depende do caso" é uma resposta válida: a linha fica com `providencia_de_costume = a pessoa decide caso a caso`.
4. Anote as palavras do ato que identificam a situação (`o_que_o_teor_diz`), a peça com o nome do jurídico, o aviso ao cliente e quem decide.
5. Mostre a tabela no formato de `assets/providencias-modelo.md`. Com o ok, grave em `escritorio/04-base/controladoria/providencias.md`, com `validada_por` e a versão.

### Modo sugerir
1. **Separar o que não ganha sugestão (S).** Triagem `ciencia` de prazo da outra parte, `duplicada`, `sem-caso`: não sugira providência; diga o motivo em uma linha.
2. **Ler o ato (S).** Do teor, tire o trecho literal que diz o que o ato pede.
3. **Procurar a linha (S).** Compare o `tipo_ato` e as palavras do trecho com `o_que_o_teor_diz`, a `area` e o `rito` de cada linha. Bateu uma: essa é a sugestão. Bateram duas: mostre as duas e diga a diferença. Nenhuma: "sem costume registrado".
4. **Montar a sugestão (A).** Para cada publicação: o trecho literal, a chave da linha, a providência de costume, a peça, o aviso ao cliente, quem decide e o prazo que corre (da linha `sugerido` ou `conferido` do `prazos.csv`, com a data de segurança). Notícia ruim no ato: o aviso sugerido é `ligacao`, mesmo que a linha diga outra coisa.
5. **Perguntar (H).** "O que fazemos com esta publicação?". Mostre a sugestão como o costume, nunca como a resposta. A pessoa pode aceitar, mudar ou decidir outra coisa.
6. **Registrar a decisão.** Com a resposta, grave no item da fila a linha `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` e o que foi decidido, e chame a `encaminhar-providencia` (se instalada).

### Modo guardar
Quando a pessoa disser "sempre que..." ou decidir diferente da tabela pela segunda vez no mesmo tipo de ato, proponha a linha nova ou o ajuste, mostre com `[NOVO]` ou `[ALTERADO]` e grave só com o ok, subindo a versão e anotando no "Histórico" da tabela.

### Passo final. Aprender
Pergunte: "A sugestão de hoje ajudou, ou alguma linha da tabela está errada?". Correção de comportamento ("Para custas, a sugestão sempre lembra de ver o contrato de honorários") vira regra curta em `aprendizados-controladoria.md`, com o ok. Correção de costume vai para a tabela (modo guardar).

### No ciclo (o agente chama)
1. Não pergunte nada. Para cada publicação triada que pede decisão, rode o modo sugerir até o passo 4.
2. Grave um item por publicação em `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-providencia.md`, no formato da seção 5, com `revisor: pendente`.
3. Sem tabela do escritório: a sugestão é "sem costume registrado" e o resumo lembra, uma vez por semana, que a tabela ainda não foi montada.
4. Nunca grave `decidido por` e nunca chame a `encaminhar-providencia` no ciclo.

### Modo adaptar
Leia `nicho.md` e os aprendizados. Reescreva as linhas para os atos típicos do nicho (por exemplo, no previdenciário: exigência do INSS, perícia marcada, benefício implantado), mantendo as colunas. Marque cada mudança `[ALTERADO]` e grave em `escritorio/04-base/controladoria/nicho/providencia-sugerida.md` só com o ok; a tabela do escritório muda só pelo modo guardar.

## 4. Exemplos resolvidos (Escritório Modelo, lote de 2026-04-14, tabela de treino)

| Linha | Caso | Trecho literal | Chave que bateu | Sugestão (a advogada decide) |
|---|---|---|---|---|
| 1 | Otávio · C-2026-0012 | "JULGO IMPROCEDENTE o pedido" | `sentenca-improcedente-jef` | Estudar o recurso inominado (`recurso-inominado`); ligar para o Otávio antes; segurança 2026-04-28 |
| 2 | Paulo · C-2026-0002 | "redesigno a audiência de instrução para o dia 20/05/2026, às 14h" | `pauta-audiencia` | Pauta, conferência da data e da hora, preparação do Paulo; nenhuma peça |
| 3 | Camila · C-2026-0010 | "julgo IMPROCEDENTES os pedidos formulados" | `sentenca-improcedente-trabalhista` | Estudar o recurso ordinário; ligar para a Camila antes; o prazo ainda está `sugerido` |
| 4 | Renata · C-2026-0005 | "recolher as custas complementares no prazo de 5 dias" | `custas-complementares` | Recolher e juntar a guia; quem paga `[A CONFIRMAR]` no contrato. Processo em segredo de justiça: o teor fica no registro e nada dele sai sem autorização da advogada |
| 5 | Marta · C-2026-0001 | "Intime-se o INSS para, em 5 dias" | `prazo-da-outra-parte` | Só ciência: nenhuma providência |
| 8 | Marta · C-2026-0001 | "juntar relatório médico atualizado" | `juntar-documento-do-cliente` | Pedir à Marta hoje; juntar com petição; aviso de documento |
| 9 | Jorge · C-2025-0088 | "Expeça-se a requisição de pequeno valor" | `rpv-expedida` | Acompanhar o valor; mensagem lida pela advogada, sem data de pagamento; o Jorge está insatisfeito, uma pessoa fala antes |
| 10 | Paulo · C-2026-0002 | "manifeste-se sobre os documentos juntados, em 5 dias" | `manifestar-documentos` | Manifestação; a data da ciência tácita é decisão da pessoa |

As linhas 6 (duplicada) e 7 (sem caso) não ganham sugestão. O que não pode falhar: nenhuma linha decidida pela IA; a 5 sem providência; o trecho literal em cada sugestão.

## 5. Formato da saída

**No chat (modo sugerir):**
```
PROVIDÊNCIA SUGERIDA · [código] · [PUB] · [tipo_ato] · quem decide: [nome]
Trecho literal: "[...]"
Costume (providencias.md, [chave]): [providência] · peça: [peça] · cliente: [aviso]
Prazo que corre: [PZ] · segurança [data] · fatal [data] · [status]
O que fazemos com esta publicação?
```

**Na fila (no ciclo):**
```markdown
---
status: pendente
codigo: C-2026-0012
para: advogada titular (decidir a providência)
canal: interno
tipo: decidir-providencia
item: decidir-providencia
motivo: PUB-2026-00001, sentença de improcedência disponibilizada em 2026-04-13
revisor: pendente
prazo: decidir antes da data de segurança 2026-04-28, com tempo para a peça
antes_de_enviar:
  - o prazo PZ-2026-0001 está sugerido: a data vale depois da dupla conferência
---

Trecho literal: "Ante o exposto, JULGO IMPROCEDENTE o pedido, com resolução do mérito."
Costume do escritório (sentenca-improcedente-jef): estudar o recurso inominado (recurso-inominado) e ligar para o cliente antes.
Esta é uma sugestão. O que fazemos com esta publicação?
```

## 6. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| A tabela do escritório | `escritorio/04-base/controladoria/providencias.md` |
| Sugestões no ciclo | `escritorio/07-operacao/controladoria/fila/AAAA-MM-DD/NN-<codigo>-providencia.md` (`item: decidir-providencia`) |
| A decisão da pessoa | No mesmo item: `decidido por <nome>, na conversa, AAAA-MM-DD HH:MM` |
| Tabela adaptada ao nicho | `escritorio/04-base/controladoria/nicho/providencia-sugerida.md` |
| Aprendizados | `escritorio/04-base/comum/aprendizados-controladoria.md` |
| Treino | `escritorio/07-operacao/_treino/controladoria/` (a tabela de treino fica em `assets/`) |

A tabela não tem dado de cliente e pode ir para o Projeto no Claude. Sem pasta aberta: a tabela e as sugestões no chat, em bloco para copiar.

## 7. Solo e equipe

**Solo:** a tabela começa pequena, com as cinco situações que mais chegam, e cresce pelo modo guardar. A sugestão poupa a releitura do ato: a decisão continua sendo sua.

**Equipe:** quem capta e tria roda as sugestões; quem decide (`quem_decide_providencia`) responde na fila. A tabela é revisada quando a auditoria mostrar muitas decisões diferentes do costume (`auditoria-de-prazos`, se instalada).

## 8. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| A IA decide a providência | Peça que ninguém pediu, ou recurso que o cliente não quer | Regra fixa 1; a fila pergunta |
| Sugestão de memória | Costume que não é o do escritório | Regra fixa 2; só a tabela |
| Sugestão sem o trecho do ato | A pessoa decide sem ler | Regra fixa 3 |
| Providência para prazo da outra parte | Trabalho em prazo que não é do escritório | Regra fixa 4 |
| Costume que muda e ninguém registra | A tabela envelhece | Modo guardar e o passo "Aprender" |
| Notícia ruim sugerida como mensagem | Cliente lê sozinho | Notícia ruim sempre com aviso `ligacao` |

## 9. Próximo passo

- A decisão tomada: `encaminhar-providencia` (se instalada) leva ao jurídico, à experiência ou ao responsável.
- Sentença, acórdão ou decisão longa: `leitura-da-decisao` (se instalada), antes da sugestão.
- O prazo da providência: `calcular-prazo` e `dupla-conferencia`.

## Referências desta habilidade

- `assets/providencias-modelo.md`: o modelo vazio da tabela do escritório, com as regras das colunas. Modo montar.
- `assets/providencias-de-treino.md`: a tabela do Escritório Modelo, para o treino com o lote. Modo treino e exemplos da seção 4.
