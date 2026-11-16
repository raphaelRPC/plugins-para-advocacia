# As fichas que o motor-experiencia lê

As habilidades vêm prontas no método e vazias no conteúdo. Elas sabem dar as boas-vindas, traduzir o andamento, montar o resumo e a página do caso, preparar o cliente para a audiência e cuidar de uma reclamação. O que elas não sabem é como o seu escritório cuida de quem já é cliente: quem responde, de quanto em quanto tempo o cliente tem notícia, o que nunca vai por mensagem. Isso mora em duas fichas:

| Ficha | Onde fica | Modelo | O que guarda |
|---|---|---|---|
| Do escritório | `escritorio/04-base/comum/ficha-do-escritorio.md` | `ficha-do-escritorio-modelo.md` | O que vale para todos os plugins: quem atende, áreas, nicho, tom, rotinas, alertas, ferramentas |
| Da experiência | `escritorio/04-base/comum/ficha-da-experiencia.md` | `ficha-da-experiencia-modelo.md` | Resposta ao cliente, régua de atualização, página do caso, compromissos, documentos, reclamação, satisfação, encerramento |

E duas camadas que deixam tudo mais parecido com o escritório: o perfil do nicho (`04-base/comum/nicho.md`) e os aprendizados (`04-base/comum/aprendizados-experiencia.md`). Como funcionam: `adaptar-ao-escritorio.md` e `aprender-com-o-uso.md`.

## Quem preenche

- `/motor-experiencia:comecar`: o mínimo, com até 8 perguntas. Se a ficha do escritório já existe, não pergunta de novo.
- `/motor-experiencia:ficha`: o resto, por seção.
- `adaptar-experiencia`: o nicho, a jornada e as mensagens reescritas, as rotinas próprias.
- Cada habilidade, na hora: pergunta o campo que falta, uma vez, e oferece gravar.

## Quais campos cada habilidade usa

E = ficha do escritório. X = ficha da experiência.

| Habilidade | Precisa | Melhora |
|---|---|---|
| `jornada-do-cliente` | E: areas, casos_mais_comuns · X: avisa_movimentacao_relevante, maximo_sem_noticia | E: nicho · X: resumo_mensal, lembrete_de_compromisso, nunca_por_mensagem |
| `boas-vindas-do-cliente` | E: tratamento, canais, horario_de_atendimento · X: quem_cuida_dos_casos, primeira_resposta_cliente_ativo | X: resumo_mensal, maximo_sem_noticia, como_o_cliente_manda |
| `status-para-o-cliente` | E: tratamento, tom_em_tres_palavras · X: quem_le_antes_de_enviar | E: como_o_cliente_fala, frases_que_nunca_usamos, assinatura_das_mensagens · X: nunca_por_mensagem |
| `resumo-mensal-do-caso` | X: resumo_mensal, quem_le_antes_de_enviar | E: tom_em_tres_palavras · X: pagina_do_caso, identidade_visual |
| `rotina-da-experiencia` | E: horario_da_rotina_diaria · X: maximo_sem_noticia, primeira_resposta_cliente_ativo, resumo_mensal | E: agenda, conectores_no_claude, onde_roda, quem_aprova_rascunhos · X: lembrete_de_compromisso, cobranca_de_documentos |
| `adaptar-experiencia` | E: nicho, areas, cliente_tipico | E: como_o_cliente_fala, rotinas_proprias, sazonalidade |
| `triar-mensagem-do-cliente` | E: o_que_e_urgente, palavras_de_alerta · X: quem_cuida_dos_casos, primeira_resposta_cliente_ativo | X: resposta_ponte, ponte_em_pessoa_agora, nunca_por_mensagem |
| `pagina-do-caso` | X: pagina_do_caso, quem_aprova_publicar | E: canais, cliente_tipico · X: identidade_visual, tamanho_do_texto, telefone_oficial, quando_atualiza_a_pagina |
| `cliente-com-ia` | E: tratamento, areas | E: nicho, como_o_cliente_fala |
| `checklist-de-documentos` | E: areas, casos_mais_comuns · X: como_o_cliente_manda | X: cobranca_de_documentos |
| `preparar-o-cliente` | X: lembrete_de_compromisso | X: preparacao, cadencia_da_preparacao · E: nicho |
| `reclamacao-e-recuperacao` | X: quem_assume_reclamacao, prazo_de_retorno_da_reclamacao | X: o_que_o_escritorio_oferece |
| `encerramento-do-caso` | X: prestacao_de_contas | X: guarda_de_documentos, pesquisa_quando, contato_depois_do_caso |
| `pesquisa-de-satisfacao` | X: pesquisa_quando, nota_baixa | X: perguntas_da_pesquisa, intervalo_entre_pesquisas, espera_depois_de_noticia_ruim, pede_avaliacao_publica, indicacao |
| `painel-da-carteira` | X: maximo_sem_noticia | X: a ficha inteira |
| `auditar-conversas` | E: tom_em_tres_palavras, frases_que_nunca_usamos · X: primeira_resposta_cliente_ativo | as duas fichas inteiras |
| `relacionamento-depois-do-caso` | X: contato_depois_do_caso | X: pede_avaliacao_publica |

## Sem pasta aberta

Quem trabalha no chat, sem pasta, cola as fichas nas instruções de um Projeto no Claude. As habilidades leem dali do mesmo jeito e entregam o trecho novo pronto para colar.
