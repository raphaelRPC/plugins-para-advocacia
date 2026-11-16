# Modelos de encaminhamento

Os textos que a `encaminhar-providencia` grava nas pastas de entrada dos plugins irmãos. O script `scripts/montar_encaminhamento.py` monta todos a partir da linha do `prazos.csv`. Use estes modelos à mão quando não houver ambiente que rode código, ou quando a publicação não gerou linha de prazo (por exemplo, a RPV expedida, que é só ciência com providência).

Regras dos quatro modelos:
- Um arquivo por encaminhamento, em texto puro, com o nome `AAAA-MM-DD-HHMM-controladoria-<id do prazo ou da publicação>[-<assunto>].md`, só com minúsculas, números e hífen.
- O mínimo: código, primeiro nome, o que fazer, até quando, quem decidiu. Sem CPF, sem endereço, sem dado de saúde além do nome do documento. Sem número do processo para a experiência (troque por `[PROCESSO]`).
- A linha `decidido_por` (ou o fim da `observacao`, no pedido de peça) traz `<nome>, na conversa, AAAA-MM-DD HH:MM`, com o nome que a própria pessoa disse.
- Estes arquivos são internos. Marcações como `[A CONFIRMAR]` podem aparecer aqui; elas nunca vão para o texto do cliente, que é escrito lá na experiência e aprovado na fila de lá.

## 1. Pedido de peça (entrada do motor-juridico)

Pasta: `escritorio/07-operacao/juridico/entrada/`. Formato do pedido de peça da `rotina-juridica` do motor-juridico: os campos e a ordem não mudam. `prazo_interno` é a data de segurança do prazo. A `observacao` é uma linha só.

```markdown
pedido: peça nova
codigo_caso: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME]
area: [ÁREA DA FICHA]
peca: [TIPO DA PEÇA, COM HÍFEN, EX.: recurso-inominado]
origem: intimacao
prazo_interno: AAAA-MM-DD
quem_pediu: controladoria
documentos: casos/C-AAAA-NNNN/documentos/ e o teor em 07-operacao/controladoria/publicacoes/AAAA-MM-DD/PUB-AAAA-NNNNN.md
observacao: PZ-AAAA-NNNN; [RESUMO DO ATO]; disponibilizada AAAA-MM-DD; fatal AAAA-MM-DD; prazo conferido ([OS DOIS NOMES]); decidido por [NOME], na conversa, AAAA-MM-DD HH:MM
```

Exemplo (treino, linha 1 do lote):

```markdown
pedido: peça nova
codigo_caso: C-2026-0012
cliente_curto: Otávio
area: previdenciario
peca: recurso-inominado
origem: intimacao
prazo_interno: 2026-04-28
quem_pediu: controladoria
documentos: casos/C-2026-0012/documentos/ e o teor em 07-operacao/controladoria/publicacoes/2026-04-14/PUB-2026-00001.md
observacao: PZ-2026-0001; Sentença de improcedência do pedido de benefício por incapacidade; disponibilizada 2026-04-13; fatal 2026-04-30; prazo conferido (estagiária; advogada); decidido por advogada, na conversa, 2026-04-14 10:10; o cliente ainda vai receber a ligação do advogado; recorrer ou não é conversa com ele
```

## 2. Aviso de compromisso (entrada do motor-experiencia, para a preparar-o-cliente)

Pasta: `escritorio/07-operacao/experiencia/entrada/`. Serve para audiência, perícia e sessão.

```markdown
aviso: controladoria
para: preparar-o-cliente (motor-experiencia)
codigo: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME]
assunto: audiencia | pericia | sessao
compromisso: audiencia | pericia | sessao
descricao: [O ATO, EX.: audiência de instrução (redesignada)]
data: AAAA-MM-DD
hora: HHhMM | [A CONFIRMAR]
modalidade: videoconferência | presencial | [A CONFIRMAR]
local_ou_link: [O QUE O ATO DIZ] | [A CONFIRMAR]
para_a_carteira: proximo_compromisso = audiencia; data_compromisso = AAAA-MM-DD; motivo_proximo_contato = compromisso
prazo: PZ-AAAA-NNNN, conferido ([OS DOIS NOMES])
decidido_por: [NOME], na conversa, AAAA-MM-DD HH:MM
urgencia: normal | pessoa agora (hoje ou no próximo dia útil)

## O que o ato diz (trecho literal)

> [O TRECHO]

## Para a preparação (interno, não é texto para o cliente)

- [O QUE A PREPARAÇÃO PRECISA SABER: teste da sala virtual, testemunhas são do advogado, quesitos para conferir]
```

## 3. Tarefa de documento (entrada do motor-experiencia, para a checklist-de-documentos)

```markdown
aviso: controladoria
para: checklist-de-documentos (motor-experiencia)
codigo: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME]
assunto: documento
documento: [O NOME DO DOCUMENTO, COMO O ATO PEDE]
prazo_do_processo: sim, data de segurança AAAA-MM-DD, fatal AAAA-MM-DD
entregar_ate: AAAA-MM-DD | [A DEFINIR: até quando o escritório precisa receber, antes da segurança]
por_que: [POR QUE O CASO PRECISA, EM UMA FRASE]
para_a_carteira: proximo_compromisso = prazo-do-cliente; data_compromisso = AAAA-MM-DD; motivo_proximo_contato = documento
prazo: PZ-AAAA-NNNN, conferido ([OS DOIS NOMES])
decidido_por: [NOME], na conversa, AAAA-MM-DD HH:MM
urgencia: normal | pessoa agora
```

## 4. Aviso de decisão ou de valor (entrada do motor-experiencia, para a status-para-o-cliente)

```markdown
aviso: controladoria
para: status-para-o-cliente (motor-experiencia)
codigo: C-AAAA-NNNN
cliente_curto: [PRIMEIRO NOME]
assunto: decisao | valor
noticia: ruim | parcial | a-confirmar | boa | neutra
caminho: ligação do advogado antes de qualquer mensagem | mensagem pela status-para-o-cliente, lida pelo advogado antes de sair
mensagem_ao_cliente: nenhuma antes da ligação; o registro por escrito só depois dela   (só em ruim, parcial e a-confirmar)
quem_liga: [RESPONSÁVEL]
o_que_aconteceu: [RESUMO DO ATO, SEM DADO SENSÍVEL] (disponibilizada em AAAA-MM-DD)
prazo_que_corre: [PROVIDÊNCIA], data de segurança AAAA-MM-DD, fatal AAAA-MM-DD   (ou "nenhum")
o_que_o_escritorio_faz: [EX.: pedido de peça ao jurídico (recurso-inominado)]
decidido_por: [NOME], na conversa, AAAA-MM-DD HH:MM
urgencia: normal | pessoa agora

## Roteiro de ligação (rascunho interno, H)   (só em ruim, parcial e a-confirmar)

1. O que aconteceu: ...
2. Como dizer: [A DEFINIR PELO ADVOGADO]
3. O que isso significa para o cliente: [A DEFINIR PELO ADVOGADO]
4. O que dá para fazer: [A DEFINIR PELO ADVOGADO]. Prazo processual para decidir: até AAAA-MM-DD (data de segurança).
5. Depois da ligação: a linha `ligacao` no histórico; só então o registro por escrito.
```

Exemplo de valor (treino, linha 9 do lote, sem linha de prazo): a RPV do Jorge (C-2025-0088) expedida. `assunto: valor`, `noticia: boa`, `prazo_que_corre: nenhum`, `o_que_o_escritorio_faz: acompanhamento do valor (acompanhar-valores, se instalada)`, e a linha `cuidado: valor e data de pagamento só conferidos pelo advogado; nunca prometer data`. O Jorge está insatisfeito: uma pessoa fala com ele antes da mensagem, e isso fica na `urgencia`.
