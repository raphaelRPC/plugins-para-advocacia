# Modelo do registro de uso

Copiar para `escritorio/05-automacoes/ciclo-da-controladoria/registro-de-uso.md` no modo configurar. O agente, a tarefa agendada ou quem roda à mão acrescenta uma linha por rodada (duas por dia útil, quando o ciclo roda de manhã e à tarde). O dia em que o ciclo não rodou também ganha linha, escrita por quem percebeu.

É deste arquivo que o ciclo, a captação e o script de pendências tiram "desde quando ler": a última linha com data que não seja `não rodou` nem `só o resumo`. Por isso a primeira coluna é sempre a data (AAAA-MM-DD) e a segunda a hora (HH:MM).

```markdown
---
documento: Registro de uso · ciclo da controladoria
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Registro de uso · ciclo da controladoria

| Data | Hora | Como rodou | Fontes lidas | Publicações captadas | Prazos sugeridos | Itens na fila | Bloqueados | Pessoa agora | Erros |
|---|---|---|---|---|---|---|---|---|---|
```

Valores de "Como rodou":
- `agente (tarefa agendada)`: a tarefa chamou `/motor-controladoria:ciclo` e o agente rodou;
- `agente (comando)`: alguém rodou `/motor-controladoria:ciclo`;
- `à mão`: o ciclo à mão da `rotina-da-controladoria`, no chat;
- `só o resumo`: só o script de pendências, sem captação nem conta (não conta como rodada completa);
- `não rodou`: a rodada ficou sem ciclo.

Exemplo de linhas (Escritório Modelo, fictício):

```
| 2026-04-08 | 14:00 | agente (tarefa agendada) | djen, entrada | 2 | 1 | 1 | 0 | 0 | nenhum |
| 2026-04-09 | - | não rodou | - | - | - | - | - | - | computador desligado; plano B não acionado |
| 2026-04-14 | 08:00 | à mão | djen, entrada, painéis | 10 | 5 | 8 | 0 | 3 | DJEN consultado desde 2026-04-09 |
```

Leitura na revisão do mês: quantas rodadas pelo agente, quantas à mão, quantas não rodaram, e se "Pessoa agora" está caindo. A linha de 2026-04-09 mostra por que a Camila chegou com atraso: o ciclo parou e ninguém percebeu. Se "Pessoa agora" não cai, olhe a captação com atraso (o ciclo parou?) e a dupla conferência que espera (quem confere tem horário?).
