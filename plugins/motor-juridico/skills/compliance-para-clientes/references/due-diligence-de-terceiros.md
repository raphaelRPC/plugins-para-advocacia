# Due diligence de terceiros

Leia no modo due diligence. A checagem é proporcional ao risco do terceiro. O escritório organiza, analisa e recomenda; a empresa decide se contrata. Toda consulta a fonte é feita pela pessoa, e toda norma citada fica `[CONFERIR]`.

## 1. Classe do terceiro

| Classe | Quando | Profundidade |
|---|---|---|
| Alta | Fala com o poder público em nome da empresa (despachante, representante), recebe valor alto ou fora do padrão, é fornecedor único de item crítico, trata dado sensível da empresa | Questionário completo, fontes públicas, entrevista, cláusulas e monitoramento |
| Média | Fornecedor recorrente de valor relevante, prestador com acesso a instalações ou a dados pessoais | Questionário curto e fontes públicas |
| Baixa | Compra eventual, de valor baixo, sem contato com poder público | Cadastro básico |

Os limites de "valor alto" e "recorrente" são da empresa `[A DEFINIR]`.

## 2. Questionário (enviado pela empresa ao terceiro)

1. Razão social, CNPJ, endereço, sócios e administradores.
2. Há agente público entre sócios, administradores ou parentes próximos deles? `[CONFERIR: o conceito de agente público e de parentesco que a empresa vai usar]`
3. A empresa responde ou respondeu a processo, autuação ou investigação nos últimos [A DEFINIR] anos? Quais?
4. Tem programa de integridade, código de conduta ou política anticorrupção? Pode enviar?
5. Vai subcontratar alguém para este serviço? Quem?
6. Vai tratar dados pessoais da empresa ou dos clientes dela? Como protege?
7. Licenças e autorizações do setor em dia? `[CONFERIR: quais o setor exige]`

## 3. Fontes públicas e oficiais (a pessoa consulta)

| Fonte | O que procurar |
|---|---|
| Cadastro da empresa na Receita Federal | Situação cadastral, sócios, atividade `[CONFERIR: acesso e o que a consulta mostra]` |
| Cadastros públicos de empresas punidas ou impedidas de contratar com o poder público | Sanções em vigor `[CONFERIR: quais cadastros e onde consultar]` |
| Consulta processual dos tribunais | Processos relevantes, com o cuidado de não concluir só pela existência do processo |
| Órgão do setor (licença, autuações) | Licenças válidas e autuações `[CONFERIR: onde o órgão publica]` |
| Notícias | Fato concreto, com a fonte; boato não entra |

A habilidade não promete consulta automática a nenhum cadastro. O que a pessoa trouxer entra com a fonte e a data da consulta.

## 4. Sinais de alerta

- Recusa ou demora para responder o questionário.
- Sócio ou parente agente público ligado ao objeto do contrato.
- Pedido de pagamento em dinheiro, em conta de terceiro, no exterior sem motivo, ou adiantado sem justificativa.
- Comissão ou preço muito fora do mercado, segundo a própria empresa.
- Sanção em vigor em cadastro público, autuação recente relacionada ao objeto, licença vencida.
- Endereço ou atividade que não batem com o serviço.
- Subcontratação não informada.

Cada sinal entra com a evidência (resposta do questionário, consulta com data). Sem evidência, não é sinal: é pergunta a fazer.

## 5. Modelo do parecer

```
---
documento: Due diligence · [TERCEIRO] · AAAA-MM-DD
versao: 0.1 · dono: [ADVOGADO]
antes_de_enviar:
  - fontes consultadas pela pessoa, com data: [LISTA]
  - normas citadas a conferir: [LISTA]
---

1. Quem é o terceiro e o que ele vai fazer para a empresa
2. Classe de risco (alta, média, baixa) e por quê
3. O que foi checado (questionário, fontes, entrevista)
4. O que foi achado: sinal · evidência · por que importa
5. Opções para a empresa:
   a) contratar;
   b) contratar com condições: [CLÁUSULAS, GARANTIAS, MONITORAMENTO];
   c) não contratar.
6. A recomendação do escritório, com a razão em duas linhas
7. Quando checar de novo
```

O parecer diz o que o escritório viu e recomenda. A decisão é da empresa, e quem assina o parecer é o advogado.
