# Modelo do resumo mensal do caso

Grave em `escritorio/07-operacao/experiencia/clientes/<codigo>/resumos/AAAA-MM.md`. O mesmo arquivo serve para os três formatos: a mensagem (o texto do cliente, copiado), o .docx (pelo `scripts/resumo_para_docx.py`, que tira o cabeçalho e o "Antes de enviar") e a página do caso (a `pagina-do-caso`, se instalada, lê daqui).

O bloco entre `<!-- antes-de-enviar -->` e `<!-- /antes-de-enviar -->` é interno: conferências, pendências e marcações ficam só ali. O texto do cliente, abaixo dele, não leva nenhuma marcação.

```markdown
---
documento: Resumo mensal · [CÓDIGO] · AAAA-MM
versao: 1
revisado_em: AAAA-MM-DD
dono: [QUEM LÊ ANTES DE ENVIAR]
formato: mensagem | docx | pagina
status: rascunho          # rascunho | aprovado | enviado | descartado
---

<!-- antes-de-enviar -->
## Antes de enviar (interno, não vai ao cliente)
- Quem lê: [FUNÇÃO, DE quem_le_antes_de_enviar]
- Fontes: movimentações de [DATAS]; histórico até [DATA] (contatos e trabalho do escritório); jornada [ARQUIVO OU "sem jornada"]
- Conferir: [O QUE PRECISA SER CHECADO: termo traduzido, data de ato marcado, o que o escritório fez]
- Pendências: [A CONFIRMAR: ...] [CONFERIR: ...]
- Notícia ruim no mês: [NENHUMA | LIGAÇÃO FEITA EM AAAA-MM-DD | LIGAÇÃO PENDENTE: o resumo espera]
- Fora do resumo de propósito: [EX.: "valor do cálculo, ainda não conferido"]
<!-- /antes-de-enviar -->

# Resumo de [MÊS POR EXTENSO] · [NOME CURTO]

**Em que pé está:** [FASE EM PALAVRAS SIMPLES, UMA FRASE]

**O que aconteceu no processo:** [MOVIMENTAÇÕES DO MÊS EXPLICADAS PELO GLOSSÁRIO, OU "o processo ficou aguardando [O QUÊ], o que é normal nesta etapa"]

**O que o escritório fez:** [AS LINHAS DE TRABALHO DO ESCRITÓRIO DO HISTÓRICO NO MÊS, EM PALAVRAS DO CLIENTE: "conferimos o processo em DD/MM", "pedimos ao INSS a cópia do processo", "cumprimos o prazo para responder a empresa"]

**O que vem agora:** [PRÓXIMA ETAPA, SEM DATA DE DECISÃO; DATA SÓ DE ATO JÁ MARCADO]

**O que depende de você:** [DOCUMENTO, PRESENÇA OU DECISÃO, COM PRAZO; OU "nada por enquanto"]

**Quando a gente volta a falar:** [O PRÓXIMO RESUMO, ATÉ O DIA N DE MÊS; E "se acontecer algo importante antes, a gente te avisa"]

[ASSINATURA]
```

Regras:
- No texto do cliente, só primeiro nome, tipo de caso e fase. Nunca CPF, número do processo, valor da causa, endereço, nome da outra parte ou dado de saúde.
- Cada parte em uma ou duas frases. O resumo inteiro cabe numa tela de celular.
- "O que o escritório fez" só com o que aconteceu: as linhas `trabalho-do-escritorio` do `historico.md` ou o que o advogado disser. Se não há nenhuma no mês, a parte sai, e o "Antes de enviar" registra o porquê.
- O script do .docx não cria o arquivo enquanto houver pendência entre colchetes no texto do cliente (sai com código 2 e lista o que falta); com `--forcar`, cria e avisa.
- Campos entre colchetes acima são do modelo: no resumo pronto, nenhum sobra no texto do cliente.
- O `status` diz se o resumo do mês está feito: só `enviado` conta (ou `aprovado`, quando o escritório não registra o envio e a rotina roda com `--sem-registro-de-envio`). `rascunho` e `descartado` contam como por fazer no `lote_do_mes.py` e no `carteira.py` da `rotina-da-experiencia`. Quem envia muda para `enviado` no mesmo dia.
