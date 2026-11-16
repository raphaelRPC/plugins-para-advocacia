# Causas mais comuns e o ajuste de cada uma

A reclamação quase nunca nasce de uma pessoa mal-intencionada. Nasce de um combinado que o método não sustenta. Por isso o ajuste vai para o método (jornada, ficha, biblioteca, rotina), e não para "prestar mais atenção".

Use esta tabela no passo 9. Escolha a causa principal (uma) e, se houver, uma secundária. Causa que não está aqui: escreva em uma frase e marque "causa nova".

| Causa | Como reconhecer no registro | Ajuste típico | Destino |
|---|---|---|---|
| Régua não rodou | Cliente passou do `maximo_sem_noticia` sem ninguém ver | Ligar a rotina diária ou o ciclo; cliente além da régua no topo do resumo | `rotina-da-experiencia` (se instalada), ficha da automação |
| Fase sem contato na jornada | A fase do caso (ex.: cumprimento, aguardando perícia) não tem momento de contato previsto | Momento de contato novo na jornada daquele tipo de caso, com frequência `[A DEFINIR]` | `jornada-<tipo-de-caso>.md` |
| "Te retorno" sem dono nem hora | Mensagem com "vou ver e te retorno", sem prazo, sem retorno | Resposta-ponte sempre com hora; o retorno vira `proximo_contato` na carteira | biblioteca (`recebi-retorno-ate`), aprendizado |
| Queixa leve não registrada | Houve uma reclamação antes ("está demorando") que ninguém tratou como reclamação | Toda queixa, mesmo leve, abre registro e tem dono | aprendizado, ficha (`quem_assume_reclamacao`) |
| Expectativa criada sem combinado | Cliente esperava algo que ninguém prometeu por escrito (prazo, valor, frequência de contato) | Boas-vindas e página do caso dizendo o que esperar; a consulta e a proposta sem promessa | `boas-vindas-do-cliente`; `roteiro-da-consulta` do motor-comercial (se instalado) |
| Termo ou fase mal explicada | Cliente leu no site do tribunal ou ouviu de uma IA e entendeu errado | Explicar antes da pergunta; glossário do cliente; perguntas do caso respondidas | `cliente-com-ia`, `status-para-o-cliente` (se instaladas) |
| Notícia ruim por mensagem | O cliente soube de algo ruim por texto, sem ligação | `nunca_por_mensagem` na ficha; revisor bloqueia | ficha, aprendizado |
| Pessoa errada respondendo | Pergunta jurídica respondida por quem não conduz o caso, ou sem revisão | `quem_cuida_dos_casos` e `quem_le_antes_de_enviar` claros | ficha |
| Documento ou compromisso esquecido | Cliente cobrado em cima da hora, ou foi à audiência sem saber o que levar | Lembretes da `lembrete_de_compromisso` e cobrança de documentos pela régua | `preparar-o-cliente`, `checklist-de-documentos` (se instaladas) |
| Falha jurídica | Prazo perdido, peça errada, recurso não interposto | Vai para o titular e para a revisão do processo de trabalho do escritório; o ajuste aqui é jurídico `[CONFERIR]` | titular |

## Depois do ajuste: quem mais está na mesma situação

Toda causa de método atinge mais de um cliente. Depois de aprovar o ajuste, procure na carteira os clientes com a mesma condição. Exemplos:

- "Régua não rodou" ou "fase sem contato": ativos com `ultimo_contato` além do `maximo_sem_noticia`, ou na mesma fase e tipo de caso.
- "Queixa leve não registrada": ativos com `humor = insatisfeito` e `reclamacao_aberta = nao`.
- "Documento esquecido": ativos com `documentos_pendentes` acima de zero e `proximo_contato` vencido.

Para cada um, a pessoa decide se o escritório se antecipa (uma notícia, uma ligação). A habilidade lista; a pessoa escolhe; o rascunho de cada mensagem sai pela habilidade certa e vai para a fila.
