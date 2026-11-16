# As fichas que o motor-juridico lê

As habilidades vêm prontas no método e vazias no conteúdo. Elas sabem montar o dossiê, conferir citação, minutar e preparar o protocolo, mas não sabem quais peças o seu escritório faz, como elas devem sair, quem assina e onde vocês protocolam. Isso mora em duas fichas:

| Ficha | Onde fica | Modelo | O que guarda |
|---|---|---|---|
| Do escritório | `escritorio/04-base/comum/ficha-do-escritorio.md` | `ficha-do-escritorio-modelo.md` | O que vale para todos os plugins: quem atende, áreas, tom, rotinas, alertas, ferramentas |
| Jurídica | `escritorio/04-base/comum/ficha-juridica.md` | `ficha-juridica-modelo.md` | Peças, quem redige, revisa e assina, padrão visual, citação, protocolo, compliance |

E a base do escritório, que é o que o plugin amplifica: os modelos em `04-base/juridico/modelos/`, as teses em `04-base/juridico/teses/`, a jurisprudência trazida do Jus IA em `04-base/juridico/jurisprudencia/` e as habilidades próprias em `04-base/habilidades-do-escritorio/`. Os aprendizados ficam em `04-base/comum/aprendizados-juridico.md` (`aprender-com-o-uso.md`).

## Quem preenche

- `/motor-juridico:comecar`: o mínimo, com até 8 perguntas. Se a ficha do escritório já existe, não pergunta de novo.
- `/motor-juridico:ficha`: o resto, por seção.
- `adaptar-juridico`: as áreas, o padrão visual, as rotinas próprias e a primeira habilidade própria.
- Cada habilidade, na hora: pergunta o campo que falta, uma vez, e oferece gravar.

## Quais campos cada habilidade usa

E = ficha do escritório. J = ficha jurídica.

| Habilidade | Precisa | Melhora |
|---|---|---|
| `trazer-pesquisa` | J: pesquisa_de_jurisprudencia | J: tribunais_principais, validade_da_conferencia |
| `conferir-citacoes` | J: validade_da_conferencia | J: tribunais_principais, doutrina_de_referencia |
| `conferir-peca` | E: areas · J: pecas_mais_feitas | J: estilo, pedidos, nome_dos_arquivos |
| `minutar-peca` | E: areas · J: quem_redige, fonte_e_corpo, citacao_em_recuo | J: estilo, pedidos, tamanho_preferido, timbre, onde_estao_os_modelos |
| `peca-vira-habilidade` | J: onde_estao_os_modelos, pecas_mais_feitas | J: estilo, pedidos, tamanho_preferido |
| `dossie-do-caso` | E: areas | E: nicho · J: tribunais_principais |
| `estrategia-do-caso` | E: areas · J: quem_assina | J: tribunais_principais |
| `rotina-juridica` | E: horario_da_rotina_diaria · J: quem_redige, quem_revisa | E: onde_roda, quem_aprova_rascunhos, conectores_no_claude, feriados_e_recessos |
| `adaptar-juridico` | E: areas · J: pecas_mais_feitas, onde_estao_os_modelos | E: nicho, rotinas_proprias · J: estilo, timbre |
| `banco-de-teses-vivo` | E: areas · J: tribunais_principais | J: validade_da_conferencia |
| `leitura-dos-autos` | E: areas | J: tribunais_principais |
| `comparar-versoes` | E: areas | J: estilo |
| `mapa-jurisprudencial` | J: pesquisa_de_jurisprudencia, tribunais_principais | J: validade_da_conferencia |
| `advogado-do-diabo` | E: areas | J: tribunais_principais, validade_da_conferencia |
| `preparar-protocolo` | J: sistemas, nome_dos_arquivos, assinatura, quem_assina | J: limite_de_tamanho, guia_de_custas, quem_protocola |
| `conflito-de-interesses` | J: base_de_partes | E: quem_atende |
| `lgpd-do-escritorio` | J: encarregado_lgpd | E: conta_de_ia, historico_do_cliente, sistema_juridico, conectores_no_claude |
| `pecas-em-lote` | J: pecas_em_massa, quem_revisa | J: nome_dos_arquivos |
| `monitor-de-precedentes` | J: validade_da_conferencia, pesquisa_de_jurisprudencia | E: horario_da_rotina_diaria |
| `compliance-para-clientes` | J: atende_empresas | E: areas |
| `sustentacao-oral` | J: tribunais_principais | J: estilo, tamanho_preferido |

## Sem pasta aberta

Quem trabalha no chat, sem pasta, cola as fichas nas instruções de um Projeto no Claude, e as peças boas e a base de jurisprudência como arquivos do Projeto. As habilidades leem dali do mesmo jeito e entregam o que gravariam em blocos prontos para copiar.
