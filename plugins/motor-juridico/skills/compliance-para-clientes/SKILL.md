---
name: compliance-para-clientes
description: >
  O serviço consultivo de compliance para cliente empresa: diagnóstico por entrevista e
  documentos, mapa de riscos sem percentual inventado, desenho do programa de integridade,
  políticas no jeito da empresa, due diligence de terceiros (fornecedores, parceiros,
  representantes) e plano de ação com dono, prazo e evidência. Toda norma do setor e toda
  citação legal entram marcadas para conferir. Use quando o advogado disser "um cliente quer um
  programa de compliance", "faz o diagnóstico de integridade da empresa", "monta o mapa de
  riscos", "preciso de um código de conduta", "checa esse fornecedor", "plano de ação do
  compliance". Não use para a LGPD do próprio escritório (use lgpd-do-escritorio) nem para
  conflito de interesses (use conflito-de-interesses).
---

# Compliance para clientes

> A empresa que pede compliance quer saber onde está exposta e o que fazer primeiro. O escritório entrevista, lê os documentos, mostra os riscos em linguagem de negócio e entrega um plano que a empresa consegue cumprir. A norma de cada setor é conferida na fonte, sempre.

Regras do plugin: `../../docs/regras.md`. Citação: `../../docs/citacoes.md`. Produção e pasta do caso: `../../docs/producao.md`. Fichas: `../../docs/ficha-do-escritorio-modelo.md`, `../../docs/ficha-juridica-modelo.md` e a tabela de campos em `../../docs/ficha-juridica.md`. Onde gravar: `../../docs/pasta.md`. Ciclo e fila: `../../docs/agentes-e-fila.md`. Casos de treino: `../../docs/casos-ficticios.md`. Adaptação e aprendizados: `../../docs/adaptar-ao-escritorio.md` e `../../docs/aprender-com-o-uso.md`.

O sócio de um restaurante com 35 empregados (número de exemplo) liga: o maior aplicativo de entrega pediu o "programa de integridade" da empresa para renovar o contrato, e um fornecedor de carnes foi autuado. Ele quer um documento até o fim do mês. Um código de conduta copiado da internet não responde à pergunta do aplicativo nem ao fornecedor. O diagnóstico de uma semana mostra os três riscos que importam e o plano diz quem faz o quê.

**Regras fixas desta habilidade:**
1. Toda norma do setor (sanitária, financeira, ambiental, de saúde, de concorrência, regulatória) entra `[CONFERIR]`, com a pergunta do que conferir. A IA não afirma requisito setorial de memória.
2. Toda citação legal segue `citacoes.md`: marcada até a conferência no texto oficial. Lei Anticorrupção (Lei 12.846/2013), o decreto que a regulamenta e a LGPD também.
3. Risco se mede com critérios combinados com a empresa (baixo, médio, alto), nunca com percentual ou estatística inventada. A classificação final é do advogado.
4. Nenhum documento diz que a empresa "está em conformidade" ou "tem selo". O escritório entrega diagnóstico, programa e plano; a empresa adota, cumpre e comprova.
5. O que sai para o cliente leva as conferências num cabeçalho interno "Antes de enviar", nunca no texto, e passa pelo advogado antes de sair.

## 1. Quando usar

**Use quando:**
- Um cliente empresa contratou (ou vai contratar) o consultivo de compliance e o trabalho começa (modo abrir o trabalho).
- É hora da entrevista e da leitura dos documentos (modo diagnóstico).
- O diagnóstico acabou e é preciso mostrar onde a empresa está exposta (modo mapa de riscos).
- A empresa quer o programa, o código de conduta ou uma política (modos programa e políticas).
- A empresa vai contratar ou já contrata um terceiro sensível (modo due diligence de terceiros).
- O plano precisa de dono e prazo, ou o acompanhamento mensal (modo plano de ação).
- Treino com o caso fictício, ou a `adaptar-juridico` pediu (modos treino e adaptar).

**Não use quando:**
- O assunto é a LGPD do próprio escritório: `lgpd-do-escritorio` (se instalada).
- O pedido é checar se o escritório pode atender a empresa: `conflito-de-interesses` (se instalada; sem ela, o advogado confere na base do escritório) antes de começar.
- A empresa já tem um processo (autuação, ação, processo administrativo): é caso contencioso, pelo caminho normal (`dossie-do-caso`, `estrategia-do-caso`). O compliance pode vir depois.
- O pedido é a proposta de honorários do consultivo: `proposta-de-honorarios`, do motor-comercial (se instalado).

## 2. Antes de começar

1. **Leia as fichas** em `escritorio/04-base/comum/` (`ficha-do-escritorio.md`, `ficha-juridica.md`), `nicho.md` se existir e os aprendizados (`aprendizados-juridico.md`).
2. **Confira `atende_empresas`.** Se for `não`, diga: "A ficha diz que o escritório não atende empresas. Quer mudar isso ou seguir mesmo assim só desta vez?". Sem resposta, não siga.
3. **Sem ficha:** ofereça `/motor-juridico:comecar`. Se o advogado quiser seguir, pergunte só: "Vocês atendem empresas no consultivo?".
4. **Conflito antes de tudo.** A empresa e as partes que ela vai citar (sócios, fornecedores, concorrentes) passam pela `conflito-de-interesses` (se instalada) antes da entrevista.
5. **Leia os modelos do escritório** em `04-base/juridico/modelos/compliance/`, se existirem. O modelo do escritório vale mais do que os deste plugin.
6. **Dados.** A empresa vai mandar dados de empregados, clientes e terceiros. Peça o mínimo (estrutura, processos, contratos-modelo), em conta profissional, e marque o que não deveria ter vindo (`regras.md`, seção 6).

### Campos da ficha que esta habilidade usa

| | Campos |
|---|---|
| Precisa | J: `atende_empresas` |
| Melhora | E: `areas` |

Campo que falta e a tarefa pede: pergunte aquele campo, uma vez, e ofereça gravar. Sem `areas`, a habilidade não sugere quais riscos o escritório pode tratar internamente e quais vão para parceiro.

## 3. Fluxo

### Modos

| Modo | Quando | Saída |
|---|---|---|
| Abrir o trabalho | Contrato fechado ou prestes a fechar | A ficha do trabalho: empresa, setor, porte, escopo, contatos, prazo |
| Diagnóstico | Primeira etapa | Roteiro de entrevista, lista de documentos, relatório do diagnóstico |
| Mapa de riscos | Depois do diagnóstico | A matriz de riscos com critérios combinados |
| Programa | A empresa quer o programa | O desenho do programa por pilar |
| Políticas | Código de conduta ou política específica | A minuta da política, no jeito da empresa |
| Due diligence de terceiros | Contratar ou revisar um terceiro | Questionário, sinais de alerta, classificação e parecer para a empresa decidir |
| Plano de ação | Depois do mapa, e todo mês | O plano com dono, prazo e evidência; o acompanhamento |
| No ciclo | Plano de ação em andamento | Itens vencidos no resumo e o rascunho do lembrete à empresa na fila |
| Treino | Caso fictício | Tudo em `_treino/` |
| Adaptar | A `adaptar-juridico` chama | Roteiro e riscos para o setor dos clientes do escritório |

Pedido direto ("faz a due diligence deste fornecedor"): não faça entrevista. Execute com o que veio, mostre e pergunte só o que falta.

### Modo abrir o trabalho
1. Pergunte, uma por vez: "Qual é a empresa e o que ela faz?", "Quantas pessoas trabalham lá, mais ou menos?", "O que fez a empresa pedir compliance agora?" (exigência de cliente, contrato com o poder público, autuação, investidor, crescimento), "Quem na empresa vai ser o contato do trabalho?".
2. Combine o escopo com o advogado: só diagnóstico, diagnóstico e programa, ou um pedaço (uma política, uma due diligence).
3. Marque o setor e a norma setorial que vai precisar de conferência: "Setor: alimentação. Norma sanitária `[CONFERIR: quais normas de vigilância sanitária se aplicam ao estabelecimento e ao município]`."
4. Grave a ficha do trabalho em `casos/<codigo>/compliance/trabalho.md`, com o ok.

### Modo diagnóstico
1. Monte o roteiro pela `references/roteiro-do-diagnostico.md`, só com os pilares do escopo e com as perguntas adaptadas ao setor e ao porte.
2. Monte a lista de documentos a pedir (contrato social, organograma, contratos-modelo com clientes e fornecedores, políticas que já existem, canais de reclamação, relação com o poder público). Mostre ao advogado antes de mandar; quem envia o pedido à empresa é a pessoa.
3. Depois da entrevista (anotações, transcrição ou ata coladas), organize: o que a empresa faz hoje, o que falta, o que contradiz (o que foi dito e o que o documento mostra), o que não dá para saber ainda.
4. Escreva o relatório do diagnóstico no formato da seção 4.1: linguagem de negócio, frase curta, cada achado com a evidência (documento ou trecho da entrevista) e o que falta conferir.

### Modo mapa de riscos
1. Combine os critérios com a empresa antes de classificar: o que é impacto alto para ela (multa, perda de contrato, interdição, dano à reputação, risco a pessoa) e o que é probabilidade alta (acontece todo mês, já aconteceu, nunca aconteceu).
2. Para cada processo do diagnóstico (compras, vendas, relação com fiscalização e poder público, pessoas, dados, terceiros, financeiro, setor), liste os riscos com: o que pode acontecer, em que processo, o controle que existe, probabilidade e impacto pelos critérios combinados, e a norma `[CONFERIR]`.
3. Ordene por prioridade (alto e alto primeiro). Proponha; o advogado confirma a classificação. Nenhum percentual.
4. Grave a matriz em `casos/<codigo>/compliance/mapa-de-riscos.md` (modelo em `assets/plano-de-acao.md`, seção 1).

### Modo programa
1. Para cada pilar de `references/roteiro-do-diagnostico.md` (seção 2), escreva: o que a empresa já tem, o que o programa propõe, quem é dono na empresa, o que comprova que funciona. Do tamanho da empresa: o restaurante de 35 pessoas não precisa da estrutura de uma indústria de 3 mil.
2. Os parâmetros de avaliação do programa estão na regulamentação da Lei 12.846/2013 `[CONFERIR: o decreto vigente e o artigo dos parâmetros do programa de integridade]`. A habilidade usa como lista de conferência, nunca como garantia de que o programa será aceito.
3. Contrato com o poder público ou exigência de cliente: confira a exigência específica `[CONFERIR: a cláusula do contrato, o edital ou a lei de licitações aplicável]`.
4. Grave em `casos/<codigo>/compliance/programa.md`.

### Modo políticas
1. Pergunte: "Qual política, e o que motivou?" Comece pelas que respondem aos riscos altos do mapa.
2. Use a estrutura de `assets/politica-modelo.md` e escreva com os fatos da empresa (nomes de área, valores de alçada que a empresa informar, canais que existem). Valor de alçada, prazo e regra interna vêm da empresa ou ficam `[A DEFINIR]`.
3. Norma que a política cita: marcada `[CONFERIR]` no cabeçalho interno; no texto ao cliente, só o nome da norma.
4. Mostre ao advogado; com o ok, grave em `casos/<codigo>/compliance/politicas/<nome>-v<n>.md`. O .docx sai pelo script de documento da `minutar-peca` (se instalada; sem ela, a pessoa copia o .md para o modelo de documento do escritório), sem o cabeçalho interno.

### Modo due diligence de terceiros
Siga `references/due-diligence-de-terceiros.md`:
1. **Classifique o terceiro** pelo que ele faz para a empresa (fala com o poder público em nome dela, recebe valor alto, toca dado sensível, é fornecedor crítico).
2. **Questionário** proporcional à classe, enviado pela empresa.
3. **Fontes públicas e oficiais**: a pessoa consulta os cadastros públicos que a referência lista `[CONFERIR: quais estão disponíveis e como acessar]` e traz o resultado. A habilidade não promete consulta automática.
4. **Sinais de alerta**: os da referência, cada um com a evidência.
5. **Parecer** para a empresa decidir: contratar, contratar com condições (cláusulas, garantias, monitoramento), não contratar. A decisão é da empresa; a recomendação, do advogado.
6. Terceiro pessoa física: só o necessário, pela LGPD `[CONFERIR: base legal com o encarregado da empresa]`. Grave em `casos/<codigo>/compliance/due-diligence/<terceiro>-AAAA-MM-DD.md`, com o nome do terceiro só no arquivo, nunca no resumo do dia.

### Modo plano de ação
1. Para cada risco alto e médio do mapa: a ação, o dono na empresa (função), o prazo combinado com ela, a evidência que comprova (política aprovada, registro de capacitação, contrato revisado) e a situação.
2. Mostre ao advogado e à empresa; o prazo é da empresa. Grave em `casos/<codigo>/compliance/plano-de-acao.md` (`assets/plano-de-acao.md`, seção 2).
3. **Acompanhamento mensal:** leia o plano, liste o vencido e o que vence nos próximos 30 dias, e rascunhe a mensagem à empresa com o que falta, curta e sem cobrança agressiva.

### Modo no ciclo
O `agente-juridico` pode ler os planos de ação em andamento (`casos/*/compliance/plano-de-acao.md`): item vencido vira linha em "para decidir" no resumo, e o rascunho do lembrete à empresa vai para a fila (`fila/AAAA-MM-DD/NN-<codigo>-compliance.md`, com `revisor: pendente`). O ciclo não muda a classificação de risco nem o prazo, e não escreve à empresa sobre achado novo de risco: isso é do advogado.

### Modo treino
Restaurante Sabor Mineiro Ltda. (C-2025-0071, fictício), que já foi cliente do consultivo trabalhista em `../../docs/casos-ficticios.md`. Situação de treino: o aplicativo de entrega exige programa de integridade, um fornecedor de carnes foi autuado, a empresa guarda dados de clientes do delivery. Números de exemplo: 35 empregados, 12 fornecedores. Tudo grava em `escritorio/07-operacao/_treino/juridico/casos/C-2025-0071/compliance/`. O que não pode falhar: norma sanitária e exigência do aplicativo `[CONFERIR]`; nenhum percentual de risco; o fornecedor autuado com sinal de alerta e parecer para a empresa decidir; o plano com dono e prazo `[A DEFINIR]` pela empresa; nenhuma frase de "empresa em conformidade".

### Modo adaptar
1. Leia `nicho.md` e as `areas` da ficha. Pergunte: "Que tipo de empresa vocês atendem mais?".
2. Proponha o roteiro e a lista de riscos típicos desse setor, com cada norma setorial `[CONFERIR]`, marcados `[ALTERADO]` em relação à referência.
3. Com o ok, grave em `04-base/juridico/modelos/compliance/roteiro-<setor>.md`.

### Aprender (último passo de todo modo)
Pergunte: "O que a empresa ou você mudaria neste documento?". Cada correção vira uma regra curta e, com o ok, entra em `aprendizados-juridico.md` (`../../docs/aprender-com-o-uso.md`). Uma política ou um roteiro que funcionou bem pode virar modelo do escritório em `04-base/juridico/modelos/compliance/` e, com três trabalhos parecidos, habilidade própria pela `peca-vira-habilidade` (se instalada).

## 4. O formato das entregas

### 4.1 Relatório do diagnóstico

```
---
documento: Diagnóstico de integridade · [EMPRESA]
versao: 0.1 · revisado_em: AAAA-MM-DD · dono: [ADVOGADO]
antes_de_enviar:
  - normas citadas a conferir: [LISTA, CADA UMA COM O QUE CONFERIR]
  - achados que dependem de documento ainda não recebido: [LISTA]
---

1. O que motivou o trabalho (duas linhas)
2. Como foi feito (entrevistas com [FUNÇÕES], documentos lidos, período)
3. O que a empresa já faz bem
4. Os achados, por processo: achado · evidência · por que importa · o que falta saber
5. Os riscos que mais pedem atenção (os três primeiros do mapa)
6. Próximos passos propostos
```

### 4.2 Escrita para a empresa
Linguagem de negócio, sem latim, frase curta. Cada recomendação diz o que fazer, quem faz e como se comprova. Termo técnico explicado na primeira vez ("due diligence, a checagem do terceiro antes de contratar"). Norma pelo nome no texto; o que conferir, no cabeçalho interno.

## 5. O que entrega e onde grava

| Entrega | Caminho |
|---|---|
| Ficha do trabalho | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/trabalho.md` |
| Diagnóstico | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/diagnostico.md` |
| Mapa de riscos | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/mapa-de-riscos.md` |
| Programa | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/programa.md` |
| Políticas | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/politicas/<nome>-v<n>.md` (e o .docx) |
| Due diligence | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/due-diligence/<terceiro>-AAAA-MM-DD.md` |
| Plano de ação | `escritorio/07-operacao/juridico/casos/<codigo>/compliance/plano-de-acao.md` |
| Lembrete à empresa (no ciclo e no acompanhamento) | `escritorio/07-operacao/juridico/fila/AAAA-MM-DD/` |
| Modelos que o escritório aprovou | `escritorio/04-base/juridico/modelos/compliance/` |
| Treino | `escritorio/07-operacao/_treino/juridico/` |
| Correções aprovadas | `escritorio/04-base/comum/aprendizados-juridico.md` |

Se o trabalho tiver uma linha no `pecas.csv` (por exemplo, `peca = programa-de-integridade`), as etapas são as mesmas de `producao.md`: a IA leva até `conferida`; o advogado revisa e aprova. Sem pasta aberta: cada entrega vem no chat, em bloco, com o caminho onde ficaria.

## 6. Solo e equipe

**Solo:** comece pelo diagnóstico e pelo plano de ação; o programa completo vem por partes, na ordem dos riscos. Uma política bem feita para o risco mais alto vale mais do que dez genéricas.

**Equipe:** o estagiário organiza documentos e o questionário de terceiros; o advogado conduz a entrevista, classifica os riscos e assina o parecer. Na empresa, um dono do programa, com nome e função na ficha do trabalho.

## 7. Erros que esta habilidade evita

| Erro | Consequência | Como evita |
|---|---|---|
| Código de conduta genérico | Documento que não responde ao risco real da empresa | Diagnóstico antes; política a partir do mapa |
| Requisito setorial dito de memória | Plano em cima de norma errada ou revogada | Norma do setor sempre `[CONFERIR]` |
| "Risco de 70%" | Número sem base que vira promessa | Critérios combinados, sem percentual |
| "A empresa está em conformidade" | Responsabilidade que o escritório não pode assumir | Entrega diagnóstico, programa e plano; a empresa comprova |
| Due diligence que decide pela empresa | Advogado assume a decisão de negócio | Parecer com opções; a empresa decide |
| Dados de empregados e terceiros além do necessário | Exposição e risco de LGPD no próprio trabalho | Pedido mínimo; nome do terceiro só no arquivo dele |
| Plano sem dono | Nada acontece depois da entrega | Dono, prazo e evidência em cada ação |

## 8. Próximo passo

- Diagnóstico pronto: mapa de riscos e plano de ação, nesta habilidade.
- Política aprovada: .docx pela `minutar-peca` (se instalada) e a entrega pela pessoa.
- Empresa com processo em andamento: `dossie-do-caso` e `estrategia-do-caso`.
- Proposta do consultivo: `proposta-de-honorarios`, do motor-comercial (se instalado).

## Referências desta habilidade

- `references/roteiro-do-diagnostico.md`: as perguntas por pilar e por processo, a lista de documentos a pedir e os pilares do programa. Leia nos modos diagnóstico e programa.
- `references/due-diligence-de-terceiros.md`: classes de terceiro, questionário, fontes públicas a conferir, sinais de alerta e o modelo do parecer. Leia no modo due diligence.
- `assets/plano-de-acao.md`: os modelos da matriz de riscos e do plano de ação. Use nos modos mapa de riscos e plano de ação.
- `assets/politica-modelo.md`: a estrutura de uma política e a lista das políticas mais pedidas. Use no modo políticas.
