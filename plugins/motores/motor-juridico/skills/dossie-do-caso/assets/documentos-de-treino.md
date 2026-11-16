---
documento: Documentos de treino do dossiê (casos 1 e 2)
versao: 1
revisado_em: 2026-04-10
dono: motor-juridico
---

# Documentos de treino · casos 1 e 2

Textos fictícios dos documentos descritos em `../../docs/casos-ficticios.md`, para treinar a `dossie-do-caso`. Nenhuma pessoa, empresa, número ou benefício daqui existe. Os dados identificáveis já vêm trocados pelas marcações das regras (`[DOC]`, `[CONTATO]`, `[ENDEREÇO]`). Valores são de exemplo.

Para treinar em etapas, copie cada documento para um arquivo próprio em `escritorio/07-operacao/_treino/juridico/casos/<codigo>/documentos/` (por exemplo `d1-carta-de-cessacao.txt`) e rode o índice do lote. Não leia o gabarito (seção 4.7 do SKILL.md) antes de terminar.

## Caso 1 · Marta · C-2026-0001

### D1 · d1-carta-de-cessacao.txt

```
INSTITUTO NACIONAL DO SEGURO SOCIAL
Comunicação de cessação de benefício
Belo Horizonte, 02/03/2026

Segurada: Marta [DOC]
Benefício: auxílio por incapacidade temporária, NB [DOC]

Comunicamos que o benefício acima foi cessado em 28/02/2026, em razão da não
constatação de incapacidade para o trabalho ou para a atividade habitual na perícia
médica realizada em 20/02/2026.

Caso não concorde, a segurada pode apresentar pedido de prorrogação ou recurso nos
prazos informados no canal de atendimento.
```

### D2 · d2-decisao-prorrogacao.txt

```
INSTITUTO NACIONAL DO SEGURO SOCIAL
Comunicação de decisão
Belo Horizonte, 12/03/2026

Segurada: Marta [DOC]
Assunto: pedido de prorrogação do benefício NB [DOC]

Informamos que o pedido de prorrogação apresentado em 03/03/2026 foi indeferido.
Motivo: não foi constatada incapacidade para o trabalho ou para a atividade habitual.
O benefício permanece cessado desde 05/03/2026.
```

### D3 · d3-cnis.txt

```
EXTRATO PREVIDENCIÁRIO (resumo)
Filiada: Marta [DOC]

Vínculos
Seq. 3  Lanchonete Ponto Certo Ltda. (fictícia)  início 03/06/2019  última remuneração 09/2025
        Ocupação: auxiliar de cozinha
Seq. 2  Padaria Trigo Bom Ltda. (fictícia)       01/2016 a 12/2018
Seq. 1  contribuinte individual                   03/2014 a 11/2015

Benefícios
Auxílio por incapacidade temporária  DIB 18/09/2025  DCB 28/02/2026

Contribuições em dia. Sem indicadores de pendência.
```

### D4 · d4-relatorio-medico-2026-01-20.txt

```
RELATÓRIO MÉDICO
Belo Horizonte, 20/01/2026

Paciente: Marta [DOC]

Paciente em acompanhamento neste serviço desde 08/2025 por dor lombar crônica com
irradiação para membro inferior esquerdo, com exame de imagem compatível com hérnia
discal lombar (CID informado no original).

Segue sem condição para atividade com esforço físico, carregamento de peso e longos
períodos em pé. Não há previsão de melhora no momento. Mantém tratamento com
medicação e fisioterapia.

Paciente relata também acompanhamento psicológico por ansiedade desde 2024.

Dr. [NOME DO MÉDICO], CRM [DOC]
```

### D5 · d5-resumo-pericia-administrativa.txt

```
RESUMO DA PERÍCIA MÉDICA
Data do exame: 20/02/2026
Segurada: Marta [DOC]

Queixa: dor lombar.
Documentos médicos apresentados: exame de imagem de 08/2025.
Exame físico: marcha sem alterações, sem sinais de comprometimento neurológico.
Conclusão: há capacidade para a atividade habitual. Benefício não prorrogado.
```

### D6 · d6-carteira-de-trabalho.txt

```
CARTEIRA DE TRABALHO (páginas enviadas: identificação e contrato de trabalho)

Empregador: Lanchonete Ponto Certo Ltda. (fictícia)
Admissão: 03/06/2019
Cargo: auxiliar de cozinha
Descrição anotada: preparo de alimentos, limpeza da cozinha, recebimento e
carregamento de mercadorias.
Saída: (página não enviada)
```

## Caso 2 · Paulo · C-2026-0002

### T1 · t1-termo-de-rescisao.txt

```
TERMO DE RESCISÃO DO CONTRATO DE TRABALHO
Empregador: Restaurante Sabor Mineiro Ltda. (fictício)
Empregado: Paulo [DOC]

Data de admissão: 01/03/2022
Data do afastamento: 09/03/2026
Causa: dispensa sem justa causa pelo empregador
Aviso prévio: indenizado

Verbas: saldo de salário, aviso prévio indenizado, férias vencidas e proporcionais
com um terço, 13º salário proporcional, FGTS do mês e multa de 40%.
Total líquido: a pagar

Assinaturas: empregador (assinado); empregado (assinado); campo de quitação em branco.
```

### T2 · t2-carteira-de-trabalho.txt

```
CARTEIRA DE TRABALHO (página do contrato)

Empregador: Restaurante Sabor Mineiro Ltda. (fictício)
Admissão: 02/05/2022
Cargo: cozinheiro
Remuneração inicial: R$ 2.100,00 (valor de exemplo)
```

### T3 · t3-holerites.txt

```
DEMONSTRATIVO DE PAGAMENTO · Restaurante Sabor Mineiro Ltda. (fictício)

Competência 12/2025: salário R$ 2.400,00; horas extras 50% (18 h) R$ 294,55
Competência 01/2026: salário R$ 2.400,00; horas extras 50% (22 h) R$ 360,00
Competência 02/2026: salário R$ 2.400,00; sem horas extras
(valores de exemplo)
```

### T4 · t4-mensagens-com-o-gerente.txt

```
Conversa exportada (WhatsApp), trechos

20/03/2026 18:02  Paulo: e o meu acerto? já tem 10 dias
20/03/2026 18:40  Gerente: o acerto sai no fim do mes, pode ficar tranquilo
20/03/2026 18:41  Gerente: melhoras pro seu menino, soube que ele ta internado
20/03/2026 18:45  Paulo: obrigado. trabalho aí desde o comecinho de março de 2022, nunca faltei
02/04/2026 09:15  Paulo: o fim do mes passou e nada
02/04/2026 11:30  Gerente: semana que vem resolvo
```
