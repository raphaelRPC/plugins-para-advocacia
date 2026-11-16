# As fichas que o motor-comercial lê

As habilidades vêm prontas no método e vazias no conteúdo. Elas sabem triar, conduzir a consulta, montar a proposta e fazer o retorno, mas não sabem como o seu escritório fala, quanto cobra, o que é urgente para vocês e o que vocês não atendem. Isso mora em duas fichas:

| Ficha | Onde fica | Modelo | O que guarda |
|---|---|---|---|
| Do escritório | `escritorio/04-base/comum/ficha-do-escritorio.md` | `ficha-do-escritorio-modelo.md` | O que vale para todos os plugins: quem atende, áreas, nicho, tom, rotinas, alertas, ferramentas |
| Comercial | `escritorio/04-base/comum/ficha-comercial.md` | `ficha-comercial-modelo.md` | Primeiro contato, consulta, honorários, retorno e funil |

E duas camadas que deixam tudo mais parecido com o escritório: o perfil do nicho (`04-base/comum/nicho.md`) e os aprendizados (`04-base/comum/aprendizados-comercial.md`). Como cada uma funciona: `adaptar-ao-escritorio.md` e `aprender-com-o-uso.md`.

## Quem preenche

- `/motor-comercial:comecar`: o mínimo, com até 8 perguntas. Se a ficha do escritório já existe (outro plugin motor preencheu), não pergunta de novo.
- `/motor-comercial:ficha`: o resto, por seção, quando o advogado quiser.
- `adaptar-comercial`: o nicho, os materiais reescritos e as rotinas próprias.
- Cada habilidade, na hora: pergunta o campo que falta, uma vez, e oferece gravar.

## Como as habilidades usam as fichas

1. Leem as duas fichas, o nicho e os aprendizados antes de começar.
2. Conferem os campos da seção "Campos da ficha que esta habilidade usa" do SKILL.md.
3. Campo que a tarefa precisa agora e está vazio: perguntam aquele campo e, no fim, oferecem gravar.
4. Campo que a tarefa não precisa agora: seguem sem perguntar.
5. Nunca completam um campo sozinhas.

## Quais campos cada habilidade usa

E = ficha do escritório. C = ficha comercial.

| Habilidade | Precisa | Melhora |
|---|---|---|
| `triar-contato` | E: areas, nao_atendemos, o_que_e_urgente, palavras_de_alerta, horario_de_atendimento · C: primeira_resposta_contato_novo, follow_up | E: casos_mais_comuns, encaminhamos_para, urgencia_vai_para, urgencia_para_o_cliente, quem_atende · C: consulta, valor_da_consulta, vulnerabilidade_e_consulta, informa_valor_da_consulta_por_mensagem, maximo_de_retornos |
| `mensagens-comerciais` | E: tratamento, tom_em_tres_palavras, assinatura_das_mensagens, horario_de_atendimento · C: consulta, como_agenda | E: frase_que_soa_como_a_gente, frases_que_nunca_usamos, emoji, como_o_cliente_fala, urgencia_vai_para · C: fora_do_horario, informa_valor_da_consulta_por_mensagem, valor_da_consulta |
| `roteiro-da-consulta` | E: areas · C: duracao, quem_faz_a_consulta | E: casos_mais_comuns, nicho · C: consulta, valor_da_consulta |
| `proposta-de-honorarios` | E: cidade_uf · C: modelo, formas_de_pagamento, validade_da_proposta | C: valores_de_referencia, entrada_e_parcelas, despesas, quem_aprova_a_proposta, abate_dos_honorarios, diferenciais_verdadeiros |
| `rotina-comercial` | E: quem_atende, horario_de_atendimento, horario_da_rotina_diaria · C: primeira_resposta_contato_novo, follow_up | E: agenda, conectores_no_claude, onde_roda, quem_aprova_rascunhos, E: feriados_e_recessos |
| `adaptar-comercial` | E: nicho, areas, cliente_tipico | E: como_o_cliente_fala, tratamento, tom_em_tres_palavras, sazonalidade, rotinas_proprias |
| `qualificar-contato` | E: areas, nao_atendemos · C: consulta | E: casos_mais_comuns · C: origem_dos_contatos, vulnerabilidade_e_consulta |
| `agenda-da-consulta` | E: horario_de_atendimento · C: como_agenda, formato, duracao, quem_faz_a_consulta | E: dias_e_horarios_fixos, agenda · C: confirmacao_e_lembrete, remarcacao |
| `ata-da-consulta` | C: quem_faz_a_consulta | C: modelo, valores_de_referencia |
| `follow-up` | E: tratamento · C: follow_up, maximo_de_retornos | E: tom_em_tres_palavras · C: motivos_de_perda_comuns, remarcacao, E: feriados_e_recessos |
| `objecoes-comerciais` | C: modelo, entrada_e_parcelas, diferenciais_verdadeiros | C: motivos_de_perda_comuns, consulta |
| `contrato-de-honorarios` | E: nome, cidade_uf, dados_para_documentos, canais, horario_de_atendimento · C: modelo, formas_de_pagamento | C: despesas, entrada_e_parcelas, inadimplencia |
| `passagem-para-o-caso` | E: quem_atende | E: historico_do_cliente, sistema_juridico · X (se houver): quem_cuida_dos_casos, maximo_sem_noticia, resumo_mensal, pagina_do_caso, primeira_resposta_cliente_ativo |
| `painel-do-funil` | C: origem_dos_contatos · E: areas, horario_de_atendimento | C: motivos_de_perda_comuns, primeira_resposta_contato_novo |
| `assistente-de-primeira-resposta` | as duas fichas, com as seções 1 a 3 e 5 da do escritório e 1 e 2 da comercial sem `[A PREENCHER]` | C: seção 5 · E: whatsapp, onde_roda |
| `auditar-conversas-comerciais` | E: tom_em_tres_palavras, frases_que_nunca_usamos · C: primeira_resposta_contato_novo | as duas fichas inteiras |

## Sem pasta aberta

Quem trabalha no chat, sem pasta, cola as fichas nas instruções de um Projeto no Claude (ou como arquivos do Projeto). As habilidades leem dali do mesmo jeito. Quando o advogado aprova uma mudança, a habilidade entrega o trecho novo pronto para colar.
