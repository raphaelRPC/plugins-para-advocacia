# As fichas que o motor-controladoria lê

As habilidades vêm prontas no método e vazias no conteúdo. Elas sabem captar, triar, contar e conferir, mas não sabem quem cuida dos prazos no seu escritório, de onde vêm as publicações, em que tribunais vocês atuam e onde fica a agenda. Isso mora em duas fichas e em dois arquivos de regras:

| Arquivo | Onde fica | Modelo | O que guarda |
|---|---|---|---|
| Ficha do escritório | `escritorio/04-base/comum/ficha-do-escritorio.md` | `ficha-do-escritorio-modelo.md` | O que vale para todos os plugins: quem atende, áreas, tom, rotinas, alertas, ferramentas |
| Ficha da controladoria | `escritorio/04-base/comum/ficha-da-controladoria.md` | `ficha-da-controladoria-modelo.md` | Quem cuida e quem confere, fontes, tribunais, dias de segurança, agenda |
| Regras de contagem | `escritorio/04-base/controladoria/regras-de-contagem.md` | `contagem.md` | A tabela de contagem validada pelo escritório e os prazos por ato |
| Calendários | `escritorio/04-base/controladoria/calendario/<tribunal>-AAAA.md` | a `calendario-forense` | Feriados, recesso, suspensões e indisponibilidades de cada tribunal no ano |

Os aprendizados ficam em `04-base/comum/aprendizados-controladoria.md` (`aprender-com-o-uso.md`).

## Quem preenche

- `/motor-controladoria:comecar`: o mínimo, com até 8 perguntas. Se a ficha do escritório já existe, não pergunta de novo.
- `/motor-controladoria:ficha`: o resto, por seção.
- `calendario-forense`: os calendários e a validação da tabela de regras.
- `adaptar-controladoria`: as regras próprias, as rotinas e as habilidades próprias.
- Cada habilidade, na hora: pergunta o campo que falta, uma vez, e oferece gravar.

## Quais campos cada habilidade usa

E = ficha do escritório. K = ficha da controladoria.

| Habilidade | Precisa | Melhora |
|---|---|---|
| `captar-publicacoes` | K: oabs_monitoradas, fontes_de_publicacao | K: horario_da_captacao |
| `triar-publicacoes` | K: tribunais | E: areas · K: responsaveis_por_area, carteira_de_processos |
| `calendario-forense` | K: tribunais, cidades_dos_juizos | K: calendario_conferido_em, regras_validadas_por |
| `calcular-prazo` | K: dias_de_seguranca, tribunais | K: prazo_em_dobro, regras_proprias, responsaveis_por_area |
| `dupla-conferencia` | K: quem_confere, responsavel_controladoria | K: regras_validadas_em |
| `agenda-de-prazos` | K: onde_fica_a_agenda, dias_de_seguranca | K: lembretes, responsaveis_por_area |
| `encaminhar-providencia` | K: quem_decide_providencia | E: quem_atende · K: responsaveis_por_area |
| `rotina-da-controladoria` | E: horario_da_rotina_diaria · K: responsavel_controladoria | E: onde_roda, conectores_no_claude, feriados_e_recessos · K: horario_da_captacao |
| `adaptar-controladoria` | E: areas · K: tribunais | E: nicho, rotinas_proprias · K: regras_proprias |
| `leitura-da-decisao` | E: areas | K: quem_decide_providencia |
| `providencia-sugerida` | E: areas · K: quem_decide_providencia | K: regras_proprias |
| `audiencias-e-pericias` | K: onde_fica_a_agenda | K: lembretes, responsaveis_por_area |
| `carteira-de-processos` | K: carteira_de_processos | K: processo_parado_dias |
| `paineis-dos-sistemas` | K: paineis_dos_sistemas | K: responsavel_controladoria |
| `cobertura-de-ausencia` | K: cobertura_de_ausencia | K: responsaveis_por_area |
| `auditoria-de-prazos` | K: responsavel_controladoria | K: dias_de_seguranca |
| `painel-da-controladoria` | K: responsaveis_por_area | K: dias_de_seguranca |
| `triagem-em-massa` | K: tribunais, quem_decide_providencia | E: areas |
| `acompanhar-valores` | K: acompanha_valores | E: areas |
| `prazos-em-lote` | K: quem_confere, dias_de_seguranca | K: regras_validadas_em |

## Sem pasta aberta

Quem trabalha no chat, sem pasta, cola as fichas e a tabela de regras nas instruções de um Projeto no Claude. As publicações entram coladas na conversa ou como arquivo, e as habilidades entregam o que gravariam em blocos prontos para copiar. Os registros (`publicacoes.csv`, `prazos.csv`) viram tabelas que a pessoa cola na planilha dela. Os scripts de contagem precisam de um ambiente que rode código (Cowork ou Claude Code); no chat sem código, a conta é feita passo a passo na conversa e a dupla conferência vale do mesmo jeito.
