---
documento: Ficha da controladoria
versao: 0.1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
---

# Ficha da controladoria · [NOME DO ESCRITÓRIO]

> O que o motor-controladoria precisa saber além da ficha do escritório: quem cuida dos prazos e quem confere, de onde vêm as publicações, em que tribunais o escritório atua, quantos dias antes do fatal o prazo entra na agenda e onde fica essa agenda. Campo sem resposta fica `[A PREENCHER]`. Os marcados (mínimo) são os que o `/motor-controladoria:comecar` pergunta.

## 1. Quem cuida

- responsavel_controladoria: [A PREENCHER] (mínimo; quem capta, tria e distribui; ex.: a estagiária, toda manhã)
- quem_confere: [A PREENCHER] (mínimo; quem faz a segunda conferência de cada prazo; no escritório de uma pessoa só: "eu mesma, em outro turno")
- responsaveis_por_area: [A PREENCHER] (quem cumpre o prazo em cada área; ex.: previdenciário: advogada titular)
- quem_decide_providencia: [A PREENCHER] (mínimo; quem diz o que fazer com a publicação; ex.: a advogada responsável pelo caso)

## 2. De onde vêm as publicações

- oabs_monitoradas: [A PREENCHER] (mínimo; número e UF de cada advogado do escritório; ex.: 000000/MG)
- fontes_de_publicacao: [A PREENCHER] (mínimo; opções: djen | e-mail do tribunal | exportação do sistema jurídico | planilha de outro serviço | outra)
- horario_da_captacao: [A PREENCHER] (ex.: 08h e 14h, dias úteis)
- paineis_dos_sistemas: [A PREENCHER] (mínimo; os painéis que uma pessoa abre com a própria senha ou certificado; ex.: PJe do TRT3 e do TRF6, eproc, Domicílio Judicial Eletrônico)

## 3. Tribunais e calendário

- tribunais: [A PREENCHER] (mínimo; onde os processos tramitam; ex.: JEF de BH, TRF6, TRT3, TJMG)
- cidades_dos_juizos: [A PREENCHER] (para os feriados locais; ex.: Belo Horizonte, Contagem)
- calendario_conferido_em: [A PREENCHER] (a data da última conferência dos calendários do ano)

## 4. Regras de prazo

- dias_de_seguranca: 2 dias úteis (padrão; quantos dias úteis antes do fatal o prazo entra na agenda como meta)
- regras_validadas_por: [A PREENCHER] (quem validou a tabela de `regras-de-contagem.md`)
- regras_validadas_em: [A PREENCHER]
- prazo_em_dobro: [A PREENCHER] (o escritório atende Fazenda, Defensoria ou litisconsortes em autos físicos? ex.: "não; só a parte contrária (INSS) tem dobro")
- regras_proprias: [A PREENCHER] (ex.: prazo de recurso sempre na agenda do sócio também; nenhum prazo é cumprido no último dia)

## 5. Agenda e lembretes

- onde_fica_a_agenda: [A PREENCHER] (mínimo; opções: Google Agenda | Outlook | sistema jurídico | planilha; o plugin gera arquivo .ics para importar)
- lembretes: [A PREENCHER] (ex.: 5 dias úteis antes, 2 dias úteis antes e no dia)
- cobertura_de_ausencia: [A PREENCHER] (quem assume os prazos de quem sai de férias ou licença)

## 6. Processos e valores

- carteira_de_processos: [A PREENCHER] (onde está a lista de processos ativos; ex.: sistema jurídico, planilha)
- processo_parado_dias: [A PREENCHER] (ex.: 90; processo sem movimentação há mais dias que isso aparece no resumo)
- acompanha_valores: [A PREENCHER] (opções: sim | não; alvarás, RPV, precatórios e depósitos judiciais)

## Histórico da ficha

(uma linha por mudança: data, campo, o que mudou, quem pediu)
