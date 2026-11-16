# Fase 7 · Rotinas (o sistema trabalhando sozinho)

Objetivo: deixar ligadas as rotinas que fazem o bastidor do marketing nos dias e horários escolhidos pelo advogado, com tudo entrando na caixa de aprovação. Saída: arquivos em `rotinas/`, tarefas agendadas criadas, `pautas.md` com pautas reais e a pasta `aprovacoes/` funcionando.

Explique em duas frases: a partir de agora, o sistema pesquisa, prepara, edita e confere sozinho. Você só abre a caixa de aprovação e decide.

## Passos

1. **Fontes do Informativo:** confirme as fontes do `base/posicionamento.md`. Se estiverem rasas, sugira a partir da lista de fontes jurídicas da skill `informativo-diario` (`references/fontes-juridicas.md` dela) e peça a escolha de 3 a 6.
2. **Gere o Informativo** (`informativo-diario.md`) pelo modelo da skill `informativo-diario` (`references/modelo-rotina.md` dela) e rode uma vez agora para semear `pautas.md` e o painel. Mostre as pautas.
3. **Configure as rotinas** com a skill `rotinas`, seção 1: apresente o catálogo, recomende o conjunto inicial (Informativo da manhã, Pauta da semana, Conferência da fila, Balanço da semana), pergunte quais ligar e os horários, gere os arquivos e crie as tarefas agendadas.
4. **Ilha de edição:** só ofereça ligar se o plugin de vídeo estiver instalado e o advogado já tiver editado um vídeo (Fase 3, Parte B).
5. **Mostre a caixa de aprovação:** crie `aprovacoes/`, explique os tipos de item e os comandos ("o que tem para eu aprovar?", "aprovo o item 2", "ajusta o item 1: ...", "descarta o item 3").
6. **Combine o ritual de aprovação:** sugira um momento fixo da semana (ex.: segunda depois do almoço, 20 minutos) para abrir a caixa e aprovar as minutas da semana, e um momento diário curto para aprovar pacotes prontos.

## Fechamento

Verifique: os arquivos de rotina existem e estão completos? As tarefas foram criadas (ou o advogado sabe criar)? `pautas.md` tem pauta com fonte? Marque a Fase 7 e faça o encerramento do Rito (ver `SKILL.md`).
