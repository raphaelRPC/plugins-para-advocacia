# A pasta do escritório

Os plugins gravam tudo em `escritorio/`, dentro da pasta de trabalho que o advogado abriu (Cowork, app desktop ou Claude Code). É a mesma pasta para todos os plugins da família e para o `inicio-automacao`: quem usa mais de um tem um lugar só, e um plugin enxerga o que o outro produziu.

Se uma habilidade precisar gravar e a pasta não existir, ela cria só o que vai usar e avisa.

## Estrutura

```
escritorio/
  CLAUDE.md                                   ← instruções fixas da pasta (cada plugin acrescenta o bloco dele)
  04-base/
    comum/
      ficha-do-escritorio.md                  ← comum a todos: quem atende, áreas, nicho, rotinas, tom, alertas, ferramentas
      ficha-comercial.md                      ← motor-comercial: consulta, honorários, follow-up
      ficha-da-experiencia.md                 ← motor-experiencia: régua de atualização, resumo, reclamação, encerramento
      ficha-juridica.md                       ← motor-juridico: peças, padrão visual, citação, protocolo
      aprendizados-juridico.md
      ficha-da-controladoria.md               ← motor-controladoria: quem confere, OABs, fontes, tribunais, dias de segurança, agenda
      aprendizados-controladoria.md
      nicho.md                                ← perfil do nicho (adaptar-comercial ou adaptar-experiencia)
      aprendizados-comercial.md
      aprendizados-experiencia.md
      rotinas-do-escritorio.md                ← as rotinas próprias do escritório que viraram habilidade
    atendimento-e-triagem/
      roteiro-consulta-<area>.md
      checklist-documentos-<tipo-de-caso>.md
    comercial/
      politica-de-honorarios.md
      objecoes.md
      biblioteca-comercial.md                 ← mensagens-comerciais
      modelos/modelo-proposta.md, modelo-contrato.md e modelo-passagem.md
    relacionamento-com-o-cliente/
      biblioteca-de-mensagens.md              ← mensagens ao cliente ativo (o mesmo arquivo do inicio-automacao)
      jornada-<tipo-de-caso>.md               ← jornada-do-cliente: momentos e régua
      glossario-do-cliente.md                 ← termos do processo em linguagem simples
      perguntas-do-caso-<tipo-de-caso>.md     ← cliente-com-ia: o que o cliente vai perguntar, respondido antes
    juridico/
      jurisprudencia/<tema>.md                ← pesquisa trazida do Jus IA, conferida (docs/pesquisa-jus-ia.md do motor-juridico)
      jurisprudencia/rascunhos/               ← pesquisa trazida e ainda não organizada
      jurisprudencia/_como-pesquisamos.md     ← como o escritório pesquisa no Jus IA
      mapas/                                  ← mapa-jurisprudencial (páginas internas)
      teses/<tese>.md                         ← banco-de-teses-vivo
      modelos/<peca>/                         ← as peças boas do escritório, fonte da peca-vira-habilidade (e conferencia.md)
      partes.csv                              ← conflito-de-interesses (tem nomes: fica fora do Projeto no Claude)
      protocolo-<sistema>.md                  ← requisitos do sistema de protocolo, conferidos (preparar-protocolo)
      lgpd/                                   ← mapa de dados, avisos e políticas do escritório (lgpd-do-escritorio)
      padrao-visual.md                        ← timbre, fonte, margens, citações em recuo (e timbre.docx)
      nicho/<habilidade>.md                   ← o que cada habilidade jurídica ajustou para o escritório (modo adaptar)
    controladoria/
      regras-de-contagem.md                   ← a tabela de contagem validada pelo escritório (docs/contagem.md do motor-controladoria)
      calendario/<tribunal>-AAAA.md           ← feriados, recesso, suspensões e indisponibilidades do ano (calendario-forense)
      paineis.md                              ← os painéis dos sistemas que uma pessoa olha, quem e quando (paineis-dos-sistemas)
      providencias.md                         ← o que cada tipo de ato costuma pedir no escritório (providencia-sugerida)
      nicho/<habilidade>.md
    casos-de-teste/<plugin>/casos.md          ← casos reais anonimizados com gabarito (e <habilidade>-testes.md das habilidades próprias)
    habilidades-do-escritorio/                ← habilidades próprias criadas na adaptação, prontas para instalar
  05-automacoes/
    ciclo-comercial/                          ← ficha, registro de uso e plano para erro do agente comercial
    ciclo-da-experiencia/                     ← o mesmo para o agente de suporte
    ciclo-juridico/                           ← o mesmo para o agente jurídico
    ciclo-da-controladoria/                   ← o mesmo para o agente da controladoria
    monitor-de-precedentes/                   ← a vigília semanal dos temas e teses
    assistente-de-primeira-resposta/
  07-operacao/
    comercial/
      contatos.csv                            ← o funil (docs/funil.md do motor-comercial)
      triagens/AAAA-MM-DD.md                  ← triagens do dia, com as qualificações
      consultas/<codigo>-AAAA-MM-DD.md        ← briefing, ata e documentos pedidos antes do contrato
      propostas/<codigo>-proposta-v<n>.md     ← e o .docx
      contratos/<codigo>-contrato-v<n>.md
      passagens/<codigo>.md                   ← o que o comercial entrega ao caso e à experiência
      rotina/AAAA-MM-DD.md                    ← resumo do dia
      painel/AAAA-MM.md
      auditorias/AAAA-MM-DD.md
      entrada/                                ← onde a pessoa solta conversas exportadas e e-mails para o ciclo ler
      fila/AAAA-MM-DD/                        ← rascunhos esperando aprovação (agentes-e-fila.md)
    experiencia/
      carteira.csv                            ← os clientes ativos (docs/carteira.md do motor-experiencia)
      clientes/<codigo>/
        abertura.md                           ← boas-vindas e combinados
        historico.md                          ← o que foi dito ao cliente, por data
        resumos/AAAA-MM.md                    ← resumo-mensal-do-caso
        pagina/                               ← pagina-do-caso (html e pdf)
        documentos.md                         ← checklist-de-documentos do caso
        ligacoes/AAAA-MM-DD.md                ← roteiros de ligação guardados
        andamento-AAAA-MM-DD.md               ← mensagem de andamento feita a pedido (status-para-o-cliente)
        preparacao-<tipo>-AAAA-MM-DD.md       ← orientação de audiência, perícia ou reunião (preparar-o-cliente)
        encerramento.md
        prestacao-de-contas.md                ← e o .docx (encerramento-do-caso)
      mensagens/AAAA-MM-DD.md                 ← triagem das mensagens de clientes do dia
      reclamacoes/<codigo>-AAAA-MM-DD.md
      pesquisas/AAAA-MM.md
      rotina/AAAA-MM-DD.md
      painel/AAAA-MM.md                       ← painel-da-carteira (interno)
      auditorias/AAAA-MM-DD.md
      auditorias/AAAA-MM-DD-conversas/        ← conversas da amostra da auditoria (fora de entrada/, para o ciclo não ler)
      entrada/
      fila/AAAA-MM-DD/
    juridico/
      pecas.csv                               ← a fila de produção (docs/producao.md do motor-juridico)
      casos/<codigo>/                         ← dossiê, leitura dos autos, estratégia, minutas, conferências, protocolo, conflito-de-interesses.md, compliance/
      lgpd/                                   ← pedidos de titular e incidentes (lgpd-do-escritorio)
      precedentes/                            ← avisos do monitor-de-precedentes
      resultados.csv                          ← decisões obtidas por peça e tese (banco-de-teses-vivo)
      lotes/                                  ← pecas-em-lote
      mapas/                                  ← mapas de peça da peca-vira-habilidade
      rotina/AAAA-MM-DD.md
      entrada/
      fila/AAAA-MM-DD/                        ← minutas esperando o advogado
    controladoria/
      publicacoes.csv                         ← tudo o que foi captado (docs/prazos.md do motor-controladoria)
      publicacoes/AAAA-MM-DD/<id>.md          ← o teor de cada publicação, como veio da fonte
      prazos.csv                              ← prazos, audiências e perícias, do sugerido ao cumprido
      processos.csv                           ← a carteira de processos (carteira-de-processos)
      valores.csv                             ← alvarás, RPV, precatórios e depósitos (acompanhar-valores)
      triagens/AAAA-MM-DD.md
      conferencias/AAAA-MM-DD.md              ← a dupla conferência de cada prazo
      decisoes/<codigo>/AAAA-MM-DD.md         ← leitura-da-decisao
      paineis/AAAA-MM-DD.md                   ← o que a pessoa viu nos painéis dos sistemas
      agenda/                                 ← os arquivos .ics gerados (e agenda/anteriores/, as versões trocadas na remarcação)
      ausencias/                              ← planos de cobertura
      auditorias/AAAA-MM.md
      painel/AAAA-MM-DD.html e .md            ← painel-da-controladoria (interno)
      lotes/
      rotina/AAAA-MM-DD.md
      entrada/                                ← planilhas, e-mails e exportações para o ciclo ler (e entrada/lidos/)
      fila/AAAA-MM-DD/                        ← prazos esperando conferência e providências esperando decisão
    _treino/                                  ← tudo o que for feito com casos fictícios
```

- `04-base/` guarda o que vale para todos os casos. Pode ir para um Projeto no Claude, menos `04-base/juridico/partes.csv`, que tem nomes de partes.
- `07-operacao/` guarda o dia a dia e tem dado de cliente, mesmo que mínimo. Fica fora do Projeto.
- O **código do contato** (`C-AAAA-NNNN`) nasce no comercial e segue o mesmo no caso e na experiência.
- `_treino/` nunca entra em painel, rotina ou auditoria.

## O `CLAUDE.md` da pasta

Se não existir, o comando `comecar` do plugin grava este cabeçalho e o bloco dele. Se existir, acrescenta só o bloco do plugin.

```markdown
# [NOME DO ESCRITÓRIO]

Antes de qualquer tarefa nesta pasta, leia `04-base/comum/ficha-do-escritorio.md`.

## Comercial
1. Leia `04-base/comum/ficha-comercial.md` e `04-base/comum/aprendizados-comercial.md`.
2. Nada de promessa de resultado, de orientação jurídica a quem não é cliente ou de valor de ação por mensagem.
3. Registre cada contato novo em `07-operacao/comercial/contatos.csv`, com o mínimo de dados.

## Experiência do cliente
1. Leia `04-base/comum/ficha-da-experiencia.md` e `04-base/comum/aprendizados-experiencia.md`.
2. Mensagem com conteúdo do processo só sai depois que alguém lê. Notícia ruim é por ligação.
3. Registre todo contato com o cliente em `07-operacao/experiencia/clientes/<codigo>/historico.md`.

## Controladoria
1. Leia `04-base/comum/ficha-da-controladoria.md`, `04-base/controladoria/regras-de-contagem.md` e `04-base/comum/aprendizados-controladoria.md`.
2. A IA capta e calcula; o prazo só entra na agenda depois da dupla conferência de uma pessoa.
3. Prazo que vence hoje ou amanhã vai para o topo, para uma pessoa, antes de qualquer outra coisa.
```

## Sem pasta aberta

No chat comum, sem arquivos, a habilidade entrega cada documento num bloco pronto para copiar, com o caminho onde ele ficaria. As fichas e os aprendizados vão para as instruções de um Projeto no Claude. Os registros (`contatos.csv`, `carteira.csv`) viram tabelas que o advogado cola na planilha dele.
