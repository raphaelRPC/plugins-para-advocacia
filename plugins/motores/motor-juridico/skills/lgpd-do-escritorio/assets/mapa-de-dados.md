# Modelo do mapa de dados do escritório

Copiar para `escritorio/04-base/juridico/lgpd/mapa-de-dados.md` no modo mapa. Uma seção por atividade. O mapa leva categorias, nunca dados de uma pessoa ("relatório médico de segurados", não "o laudo da Marta"). A base legal entra proposta e marcada (`references/bases-legais.md`) e vira decidida só com o encarregado.

```markdown
---
documento: Mapa de dados do escritório
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [ENCARREGADO]
---

# Mapa de dados · [NOME DO ESCRITÓRIO]

Encarregado: [encarregado_lgpd] · Conta de IA: [conta_de_ia] · Onde roda: [onde_roda]

## [ATIVIDADE]
| Campo | Resposta |
|---|---|
| Dados | (categorias: nome, contato, documentos pessoais, relatório médico, holerites) |
| De quem (titulares) | (contato, cliente, parte contrária, testemunha, criança, equipe, fornecedor) |
| Dado sensível ou de criança? | sim: [QUAL] / não |
| Para quê | (uma frase) |
| Base legal proposta | (citação marcada) · decidida por: [A DEFINIR] em [A DEFINIR] |
| Onde fica | (sistema, pasta, WhatsApp, papel, IA) |
| Quem acessa | (funções) |
| Compartilha com | (contador, correspondente, perito, tribunal, nuvem) |
| Entra na IA? | não / sim, em [CONTA], com [O MÍNIMO] |
| Sai do país? | não / sim: [SERVIÇO] [CONFERIR] |
| Retenção | ver a política (`politica-de-retencao.md`), categoria [NOME] |
| O que corrigir | (dono e data [A DEFINIR]) |
```

## As atividades de um escritório (percorra uma por vez)

| Atividade | Dados que costumam aparecer | Atenção |
|---|---|---|
| Contato que ainda não é cliente | nome, telefone, assunto, mensagem | Quem não fechou: prazo curto |
| Consulta | relato, documentos que a pessoa trouxe | Pode ter dado sensível antes do contrato |
| Contrato e honorários | dados de qualificação, valores, forma de pagamento | Cláusula de dados no contrato |
| Condução do caso | documentos do cliente, dados da parte contrária, de testemunhas e de terceiros, laudos | Sensível e criança; sigilo profissional |
| Comunicação com o cliente | conversas, áudios, resumos, página do caso | Celular de quem? Grupo separado? |
| Financeiro | dados de pagamento, notas, cobrança | Contador recebe o quê? |
| Equipe | dados de contratação, ponto, saúde ocupacional | Base própria, fora dos casos |
| Fornecedores e parceiros | correspondentes, peritos, tradutores | O que eles recebem e como devolvem |
| Divulgação e site | formulário, newsletter, depoimento, foto | Consentimento; Provimento 205/2021 [CONFERIR] |
| Uso de IA | o que entra nas conversas, nos Projetos, nos conectores | Conta profissional, mínimo, dado sensível só com autorização (`regras.md`, seção 6) |
| Base de partes e conflito | nome, papel, caso, CNPJ | Fora do Projeto no Claude |
| Pasta de entrada e treino do plugin | conversas exportadas, casos fictícios | `entrada/lidos/` com prazo; treino sem dado real |

## O que corrigir (resumo do mapa)

| # | O que | Onde | Dono | Até |
|---|---|---|---|---|
