# Modelo do plano para erro

Gravado em `escritorio/05-automacoes/assistente-de-primeira-resposta/plano-para-erro.md`. Fica pronto e aprovado antes de o assistente ligar, e é relido a cada teste. O plano responde a uma pergunta: o assistente errou com uma pessoa de verdade, e agora?

```markdown
---
documento: Plano para erro do assistente de primeira resposta
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
aprovado_por: [FUNÇÃO DO ADVOGADO RESPONSÁVEL]
---

# Plano para erro · assistente de primeira resposta

## 1. Quem cuida

- Dono do assistente (acompanha, pausa, corrige): [FUNÇÃO]
- Substituto: [FUNÇÃO]
- Advogado que fala com a pessoa afetada: [FUNÇÃO]
- Como o dono fica sabendo: [EX.: revisão diária das conversas automáticas às 9h; aviso da equipe; reclamação do cliente]

## 2. Como pausar

- Nível 2 (ferramenta): [ONDE FICA O BOTÃO OU A OPÇÃO DE PAUSA, conferir na configuração da ferramenta]. Quem tem acesso: [FUNÇÕES]. Tempo para pausar: [EX.: até 15 minutos depois de saber do erro].
- Nível 1 (Projeto no Claude): parar de usar o Projeto e voltar a responder pela biblioteca comercial.
- Ao pausar, volta a valer: a mensagem de fora do horário em texto fixo (nível 0), se a ferramenta ou o WhatsApp Business tiver essa opção (conferir na configuração), ou a resposta manual no horário.

## 3. O que fazer, por tipo de erro

| Erro | Gravidade | Pausa? | Com a pessoa afetada | Prazo |
|---|---|---|---|---|
| Não passou para pessoa um sinal de violência, ameaça, risco à vida ou criança em risco | crítica | Sim, na hora | O advogado assume a conversa na hora, pelo caminho de urgência | Imediato |
| Deu orientação jurídica, valor de ação ou honorário, ou prometeu resultado ou prazo | crítica | Sim, na hora | Uma pessoa escreve corrigindo, com texto aprovado pelo advogado: o que foi dito por engano e qual é o caminho certo (a consulta) | No mesmo dia |
| Disse ou deu a entender que era pessoa ou advogado | crítica | Sim, na hora | Uma pessoa se apresenta e esclarece que a mensagem anterior era automática | No mesmo dia |
| Pediu ou aceitou documento, senha ou dado sensível | crítica | Sim, na hora | Uma pessoa orienta a não mandar mais por ali; o dado recebido é tratado conforme a regra de dados do escritório | No mesmo dia |
| Mandou mensagem para quem pediu para parar | crítica | Sim | Pedido de desculpas curto, por uma pessoa, e registro de `pediu_para_parar = sim` | No mesmo dia |
| Disse valor de consulta a quem está em situação de vulnerabilidade | alta | Sim, até corrigir a seção 5 | Uma pessoa liga e segue o que a ficha prevê em `vulnerabilidade_e_consulta` | No mesmo dia útil |
| Informação errada (horário, prazo, se a consulta é paga) | alta | Sim, até corrigir a instrução | Uma pessoa corrige a informação | No mesmo dia útil |
| Continuou conversando depois da passagem, ou passou do limite de respostas | alta | Se repetir | Uma pessoa assume a conversa | No mesmo dia útil |
| Tom fora da ficha, mensagem longa, frase da lista do que nunca usamos | média | Não | Nenhuma, se não houve dano | Na revisão semanal |

## 4. Depois de corrigir com a pessoa

1. Registrar o incidente na seção 6 deste arquivo (sem dado do cliente: código do contato e o trecho anonimizado).
2. Achar a causa: instrução faltando, sinal fora da lista, ficha desatualizada, mudança na ferramenta ou no modelo.
3. Corrigir as instruções e subir a versão.
4. Acrescentar o caso à bateria (ele não sai mais dela).
5. Rodar de novo todos os casos P e E, nas rodadas do nível.
6. Religar só com o teste aprovado, e com o ok do advogado responsável.

## 5. Dado pessoal

Se o erro expôs dado de alguém (mandou dado de um cliente para outro, repetiu documento, guardou senha), o responsável pelo tratamento de dados do escritório avalia se é incidente de segurança e o que a LGPD (Lei 13.709/2018) pede nesse caso `[CONFERIR]`. Até essa avaliação, o assistente fica pausado.

## 6. Registro de incidentes

| Data | Código do contato | O que aconteceu (anonimizado) | Gravidade | O que foi feito com a pessoa | Correção nas instruções | Novo teste |
|---|---|---|---|---|---|---|

## 7. Acompanhamento de rotina

- Primeiras 4 semanas ligado: [FUNÇÃO] lê todas as conversas automáticas do dia anterior, todo dia útil [ou uma amostra de N, A DEFINIR].
- Depois: amostra semanal de [N] conversas, e a auditoria mensal (`auditar-conversas-comerciais`, se instalada).
- A cada mudança de ferramenta, de modelo de IA, das fichas ou do nicho: novo teste dos casos P e E antes de seguir.
```

## Como a habilidade preenche

- Pergunte, uma por vez: "Quem vai ser o dono do assistente, a pessoa que acompanha e pausa?"; "Onde fica a opção de pausar na ferramenta? Se não souber, a gente confere na configuração dela antes de ligar."; "Quem fala com a pessoa quando o assistente errar com ela?".
- O que ficar sem resposta vira `[A DEFINIR]`, e o assistente não liga no nível 2 com `[A DEFINIR]` nas seções 1 e 2 deste plano.
- O texto de correção para a pessoa afetada é escrito pelo advogado, na hora, com o caso na frente. O plano não traz texto pronto de pedido de desculpas para não virar resposta automática a um erro.
