---
documento: Leitura da decisão
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO DE QUEM DECIDE A PROVIDÊNCIA]
codigo: C-AAAA-NNNN
publicacao: PUB-AAAA-NNNNN
prazo: PZ-AAAA-NNNN | sem linha de prazo
tipo_ato: sentenca | acordao | decisao
disponibilizada_em: AAAA-MM-DD
lida_por: ia (leitura para conferir)
conferida_por: [A CONFIRMAR]
treino: sim | nao
---

# Leitura da decisão · [CÓDIGO] · [TIPO DO ATO] · [AAAA-MM-DD]

## Antes de usar (interno)

- Esta leitura é uma ajuda para quem decide. Tudo o que está aqui se confere no teor do ato.
- O recurso que pode caber e o prazo vêm da tabela do escritório e estão `[CONFERIR]`.
- A leitura não diz se vale recorrer. Isso é decisão do advogado com o cliente.
- [OUTRAS PENDÊNCIAS: regra não validada, calendário não conferido, trecho ilegível]

## 1. O dispositivo (trecho literal)

> "[O DISPOSITIVO, COPIADO DO TEOR, SEM MUDAR UMA PALAVRA]"

## 2. O que foi decidido, em uma frase

[EX.: O juiz julgou improcedente o pedido de benefício: o pedido não foi atendido.]

Leitura para o cliente: desfavorável | parcial | favorável | neutra | [A CONFIRMAR]. Na dúvida, desfavorável (ligação).

## 3. O que mudou para o cliente

- O que muda agora: [EX.: o benefício continua sem ser pago]
- O que não muda: [EX.: o processo ainda não acabou; a decisão pode ser revista por recurso, se o advogado e o cliente decidirem]
- Outros pontos do dispositivo: [custas, honorários, justiça gratuita, tutela concedida ou revogada, multa, o que precisa ser cumprido e por quem]

## 4. O recurso que pode caber e o prazo (tabela do escritório, `[CONFERIR]`)

| Recurso ou manifestação que pode caber | Rito | Dias (tabela do escritório) | Contagem | Fonte | Situação |
|---|---|---|---|---|---|
| [EX.: recurso inominado] | [EX.: juizado-federal] | [N] | [úteis] | `regras-de-contagem.md`, "Prazos por ato" | `[CONFERIR]` |
| [OUTRO, SE A TABELA TRAZ] | | `[A CONFIRMAR: quantos dias]` se a tabela não tem a linha | | | `[CONFERIR]` |

A conta da data vem da `calcular-prazo` e vale depois da dupla conferência: [PZ-AAAA-NNNN, status, segurança, fatal].

## 5. O que passar ao jurídico

- O dispositivo e os fundamentos principais, com o trecho de cada um: [TRECHOS]
- Pontos que a estratégia vai precisar olhar (sem dizer o caminho): [EX.: o laudo citado na sentença; o pedido que não foi analisado]
- Documentos: [onde estão]
- O pedido de peça só sai depois da decisão de quem decide, pela `encaminhar-providencia`.

## 6. O que dizer ao cliente

- Caminho: ligação do advogado (desfavorável, parcial, a confirmar) | mensagem lida pelo advogado (favorável, neutra)
- Quem liga e até quando: [RESPONSÁVEL] · [HOJE, ATÉ HH:MM]
- Roteiro: `status-para-o-cliente` do motor-experiencia (se instalado), pelo aviso da `encaminhar-providencia`; sem ele, o roteiro curto abaixo.
- Roteiro curto (H): o que aconteceu em uma frase sem termo técnico; o que muda e o que não muda; "o que dá para fazer" `[A DEFINIR PELO ADVOGADO]`; o prazo para decidir; quando volta a falar.

## 7. Pesquisa de jurisprudência (só se a pessoa pedir)

- No Jus IA, pelo caminho do motor-juridico (se instalado): a pesquisa trazida entra como "não conferida" até alguém ler o inteiro teor.
- Nenhum julgado sai da memória da IA.

## 8. Para decidir

Quem decide: [NOME OU FUNÇÃO, `quem_decide_providencia`]

O que fazemos com esta decisão?

(depois da resposta) decidido por [NOME], na conversa, AAAA-MM-DD HH:MM: [A DECISÃO]
