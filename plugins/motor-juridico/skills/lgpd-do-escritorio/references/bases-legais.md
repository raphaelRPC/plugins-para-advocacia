# Bases legais, dado sensível e retenção

Leia no modo bases legais e no modo retenção. Toda citação abaixo segue `docs/citacoes.md`: nasce marcada e só perde a marca quando alguém confere no texto compilado da Lei 13.709/2018 (LGPD) no portal oficial da legislação federal, ou na página da ANPD para as resoluções. A IA não completa inciso, número de resolução, data ou prazo de memória: o que está aqui é o mapa do que conferir. A decisão da base de cada tratamento é do encarregado.

## 1. As bases que mais aparecem num escritório

| Base | Citação (a conferir) | Quando serve no escritório | Cuidado |
|---|---|---|---|
| Execução de contrato ou procedimento preliminar a pedido do titular | `art. 7º, V, da Lei 13.709/2018 [CONFERIR: inciso e redação vigente]` | Dados do cliente para a consulta, a proposta, o contrato e a condução do caso | Vale para o titular que contrata; não cobre a parte contrária |
| Exercício regular de direitos em processo judicial, administrativo ou arbitral | `art. 7º, VI, da Lei 13.709/2018 [CONFERIR]` | Dados da parte contrária, de testemunhas e de terceiros que aparecem no caso; guarda depois do fim para defesa futura | Só o necessário para o processo |
| Cumprimento de obrigação legal ou regulatória | `art. 7º, II, da Lei 13.709/2018 [CONFERIR]` | Dados fiscais, trabalhistas da equipe, o que a lei manda guardar | Dizer qual obrigação `[CONFERIR]` |
| Legítimo interesse | `art. 7º, IX, e art. 10 da Lei 13.709/2018 [CONFERIR]` | Base de partes para conflito de interesses; registro de contatos que não fecharam, por um tempo curto | Pede o teste da seção 3, registrado. Nunca para dado sensível |
| Consentimento | `art. 7º, I, e art. 8º da Lei 13.709/2018 [CONFERIR]` | Newsletter, depoimento, foto em divulgação | Pode ser revogado a qualquer momento; não use para o que o caso precisa |
| Proteção do crédito | `art. 7º, X, da Lei 13.709/2018 [CONFERIR]` | Cobrança de honorários | Só o necessário para cobrar |

Quando duas bases cabem, mostre as duas ao encarregado e diga o que muda. A pergunta que decide: "Se o titular pedir para parar, o escritório ainda precisa desse dado?". Se precisa, consentimento é a base errada.

## 2. Dado sensível, criança e adolescente

- **Dado sensível** (saúde, origem racial ou étnica, religião, opinião política, filiação sindical, vida sexual, genético, biométrico) tem lista própria de bases: `art. 11 da Lei 13.709/2018 [CONFERIR]`. No escritório, a mais comum é o exercício regular de direitos, inclusive em contrato e em processo: `art. 11, II, "d" [CONFERIR: alínea e redação]`. Legítimo interesse não serve para dado sensível `[CONFERIR]`.
- **Criança e adolescente:** `art. 14 da Lei 13.709/2018 [CONFERIR: melhor interesse e as regras de consentimento do responsável]`. No caso de família, o dado da criança entra só no que a peça precisa, e nunca em divulgação.
- **Laudo, relatório médico, perícia:** no mapa, a linha diz onde fica, quem acessa e que só entra na IA em conta profissional, com o mínimo (`regras.md`, seção 6).

## 3. O teste do legítimo interesse (para registrar no mapa)

| Pergunta | Resposta do escritório |
|---|---|
| Qual é o interesse do escritório, em uma frase? | |
| O tratamento é necessário para isso? Dá para fazer com menos dados? | |
| O titular esperaria esse uso? | |
| Que risco ou incômodo isso traz ao titular? | |
| Que salvaguardas o escritório adota (prazo curto, acesso restrito, aviso)? | |
| Conclusão do encarregado, com data | |

Referência para conferir: `art. 10 da Lei 13.709/2018 [CONFERIR]` e o material orientativo da ANPD sobre legítimo interesse `[CONFERIR: se existe e a versão vigente]`.

## 4. Outras citações que os documentos usam

| Assunto | Citação (a conferir) |
|---|---|
| Direitos do titular | `art. 18 da Lei 13.709/2018 [CONFERIR]` |
| Prazo e forma de resposta ao titular | `art. 19 da Lei 13.709/2018 [CONFERIR]` e a regulamentação da ANPD sobre direitos do titular `[CONFERIR: se existe e o que muda]` |
| Fim do tratamento e o que pode ser conservado | `arts. 15 e 16 da Lei 13.709/2018 [CONFERIR]` |
| Registro das operações | `art. 37 da Lei 13.709/2018 [CONFERIR]` |
| Encarregado | `art. 41 da Lei 13.709/2018 [CONFERIR]` e a regulamentação da ANPD sobre o encarregado `[CONFERIR: número e data]` |
| Segurança | `art. 46 da Lei 13.709/2018 [CONFERIR]` |
| Comunicação de incidente | `art. 48 da Lei 13.709/2018 [CONFERIR]` e a resolução da ANPD sobre comunicação de incidente de segurança `[CONFERIR: número, data, prazo e conteúdo]` |
| Agente de pequeno porte | A resolução da ANPD sobre agentes de tratamento de pequeno porte `[CONFERIR: se o escritório se enquadra e o que muda para ele]` |
| Dado que sai do país (nuvem, IA) | `art. 33 da Lei 13.709/2018 [CONFERIR]` e a regulamentação da ANPD sobre transferência internacional `[CONFERIR]` |
| Sigilo profissional | Estatuto da Advocacia (Lei 8.906/1994), dispositivos sobre sigilo `[CONFERIR: artigo e redação]`; Código de Ética e Disciplina da OAB, capítulo do sigilo profissional `[CONFERIR: artigos]` |

## 5. Modelo da política de retenção

O prazo é decisão do escritório. A coluna "fundamento" sugere o que conferir; o encarregado e o advogado titular decidem e anotam a fonte.

```markdown
---
documento: Política de retenção e descarte
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [ENCARREGADO]
---

# Retenção e descarte · [NOME DO ESCRITÓRIO]

| Categoria | Onde fica | Prazo | Fundamento | Como descartar | Quem descarta |
|---|---|---|---|---|---|
| Contato que não virou cliente (mensagens, triagem) | WhatsApp, `07-operacao/comercial/` | [A DEFINIR] | legítimo interesse, prazo curto [CONFERIR] | apagar conversa e linha do registro | [FUNÇÃO] |
| Consulta sem contrato (anotações, documentos recebidos) | [ONDE] | [A DEFINIR] | [CONFERIR] | devolver ou apagar | [FUNÇÃO] |
| Contrato e honorários | [ONDE] | [A DEFINIR] | prazo de prescrição da cobrança e guarda fiscal [CONFERIR com o contador e o advogado] | | |
| Documentos do cliente no caso | [ONDE] | até o fim do caso e [A DEFINIR] depois | devolução ao cliente no fim do caso, regras do Código de Ética [CONFERIR] | devolver ao cliente; apagar cópias | |
| Peças, autos e conferências | `07-operacao/juridico/casos/` | [A DEFINIR] | exercício regular de direitos, defesa futura [CONFERIR] | | |
| Base de partes (conflito) | `04-base/juridico/partes.csv` | enquanto servir à checagem [A DEFINIR] | legítimo interesse e dever ético [CONFERIR] | mudar situação; apagar linha só por decisão | |
| Financeiro e fiscal | [ONDE] | [A DEFINIR] | legislação fiscal [CONFERIR com o contador] | | |
| Dados da equipe | [ONDE] | [A DEFINIR] | legislação trabalhista e previdenciária [CONFERIR] | | |
| Pasta de entrada do plugin (`entrada/lidos/`) | `07-operacao/*/entrada/lidos/` | 7 dias (agentes-e-fila.md) ou o que a regra de uso de IA definir | mínimo necessário | apagar | [FUNÇÃO] |
| Treino com casos fictícios | `07-operacao/_treino/` | quando não servir mais | não tem dado real | apagar | |

## Descarte
- Uma vez por [A DEFINIR], a habilidade lista o que venceu; a pessoa apaga e registra em `07-operacao/juridico/lgpd/descartes.md` (categoria, quantidade, data, quem).
- Cópia de segurança: [A DEFINIR] (o descarte vale também para o backup, no prazo do backup).
- Papel: fragmentar; nunca no lixo comum.

## Histórico
```
