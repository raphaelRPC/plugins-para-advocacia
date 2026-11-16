---
documento: Providências de costume (treino)
versao: 1
revisado_em: 2026-04-14
dono: treino
validada_por: treino (tabela fictícia, não vale para caso real)
treino: sim
---

# Providências de costume · Escritório Modelo (treino)

Tabela do Escritório Modelo de `../../../docs/casos-ficticios.md`, para testar a `providencia-sugerida` com o lote de treino. É inventada para o treino e não diz o que um escritório real deve fazer. Cada escritório monta a sua com a própria pessoa que decide (`assets/providencias-modelo.md`).

| chave | tipo_ato | o_que_o_teor_diz | area | rito | providencia_de_costume | peca | aviso_ao_cliente | quem_decide | observacao |
|---|---|---|---|---|---|---|---|---|---|
| sentenca-improcedente-jef | sentenca | "julgo improcedente" | previdenciario | juizado-federal | Estudar o recurso inominado e ligar para o cliente antes | recurso-inominado | ligacao | advogada titular | Recorrer ou não é conversa com o cliente |
| sentenca-improcedente-trabalhista | sentenca | "julgo improcedente", "julgo improcedentes os pedidos" | trabalhista | trabalhista | Estudar o recurso ordinário e ligar para o cliente antes | recurso-ordinario | ligacao | advogada titular | Recorrer ou não é conversa com o cliente |
| pauta-audiencia | despacho | "designo audiência", "redesigno a audiência" | todas | todos | Registrar na pauta, conferir data e hora, preparar o cliente | nenhuma | preparacao | advogada titular | Testemunhas: decisão da advogada |
| custas-complementares | despacho, intimacao | "recolher as custas", "custas complementares" | familia | civel | Recolher as custas e juntar a guia | peticao-de-juntada | nenhum | advogada titular | Quem paga: o combinado no contrato `[A CONFIRMAR]`; processo em segredo de justiça: o teor não sai do registro |
| juntar-documento-do-cliente | despacho, intimacao | "juntar", "relatório médico", "documento atualizado" | previdenciario | juizado-federal | Pedir o documento ao cliente hoje e juntar com petição | peticao-de-juntada | documento | advogada titular | Começa a pedir no dia da publicação |
| manifestar-documentos | intimacao | "manifeste-se sobre os documentos" | trabalhista | trabalhista | Ler os documentos juntados e manifestar | manifestacao | nenhum | advogada titular | Ciência tácita do portal: a pessoa decide a data |
| rpv-expedida | despacho | "expeça-se a requisição de pequeno valor" | previdenciario | juizado-federal | Acompanhar o valor até o levantamento | nenhuma | mensagem | advogada titular | Sem promessa de data de pagamento |
| prazo-da-outra-parte | despacho, intimacao | "intime-se o INSS", "intime-se a parte ré" | todas | todos | Só ciência | nenhuma | nenhum | advogada titular | O prazo é da outra parte: nenhuma linha em prazos.csv |
