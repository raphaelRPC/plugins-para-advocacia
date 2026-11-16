# Modelo do registro de incidente

Copiar para `escritorio/07-operacao/juridico/lgpd/incidentes/AAAA-MM-DD.md` no modo incidente. O registro descreve o que aconteceu sem copiar os dados vazados. Fica no escritório, fora do Projeto no Claude.

```markdown
---
documento: Registro de incidente · AAAA-MM-DD
versao: 1
revisado_em: AAAA-MM-DD
dono: [ENCARREGADO]
status: aberto            # aberto | avaliado | comunicado | encerrado
---

# Incidente · AAAA-MM-DD

## O que aconteceu
- Quando aconteceu: AAAA-MM-DD HH:MM (ou "não se sabe")
- Quando o escritório soube: AAAA-MM-DD HH:MM, por [FUNÇÃO]
- Em uma frase: (ex.: relatório médico de um cliente enviado a um grupo de WhatsApp de outra família)

## Dados e titulares
- Categorias de dados:
- Dado sensível, de criança ou de processo em segredo: sim / não
- Quantos titulares:
- Códigos dos casos envolvidos (sem nomes):

## Contenção
| Hora | O que foi feito | Quem |
|---|---|---|

## Avaliação de risco
(as perguntas de references/pedido-de-titular-e-incidente.md, seção 2, respondidas)
Conclusão do encarregado: risco relevante / não relevante, porque [...] · Em: AAAA-MM-DD

## Comunicação
- À ANPD: sim / não · decidido por [ENCARREGADO] em AAAA-MM-DD · prazo e forma [CONFERIR: art. 48 da Lei 13.709/2018 e resolução da ANPD] · enviado em AAAA-MM-DD
- Aos titulares: sim / não · como (ligação, mensagem) · em AAAA-MM-DD

## Causa e correção
- Causa:
- O que muda (dono e data):
- Aprendizado guardado em `aprendizados-juridico.md`: sim / não

## Histórico
```

## Treino (Escritório Modelo, fictício)

Incidente de treino: em 2026-04-15, às 16h, o estagiário envia o relatório médico da Marta (C-2026-0001) ao grupo de WhatsApp de outra família cliente. Ele apaga a mensagem em dois minutos; três pessoas viram. O que o treino precisa mostrar: contenção registrada (apagar, pedir a quem viu que apague), aviso à advogada titular no mesmo dia, dado de saúde marcado, avaliação de risco respondida, a decisão de comunicar com o encarregado e o rascunho da comunicação à Marta com a recomendação de ligação antes. Grava em `escritorio/07-operacao/_treino/juridico/lgpd/incidentes/`.
