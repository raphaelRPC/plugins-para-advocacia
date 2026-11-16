# Modelo do registro de uso

Copiar para `escritorio/05-automacoes/ciclo-juridico/registro-de-uso.md` no modo configurar. O agente, a tarefa agendada ou quem roda à mão acrescenta uma linha por rodada. O dia em que o ciclo não rodou também ganha linha, escrita por quem percebeu.

É deste arquivo que o ciclo e o script de pendências tiram "desde quando ler": a última linha com data e hora que não seja `não rodou` nem `só o resumo`. Por isso a primeira coluna é sempre a data (AAAA-MM-DD) e a segunda a hora (HH:MM).

```markdown
---
documento: Registro de uso · ciclo jurídico
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Registro de uso · ciclo jurídico

| Data | Hora | Como rodou | Fontes lidas | Peças abertas | Itens na fila | Bloqueados | Advogado agora | Para pesquisar no Jus IA | Erros |
|---|---|---|---|---|---|---|---|---|---|
```

Valores de "Como rodou":
- `agente (tarefa agendada)`: a tarefa chamou `/motor-juridico:ciclo` e o agente rodou;
- `agente (comando)`: alguém rodou `/motor-juridico:ciclo`;
- `à mão`: o ciclo à mão da `rotina-juridica`, no chat;
- `só o resumo`: só o script de pendências, sem análise nem minuta (não conta como rodada completa);
- `não rodou`: o dia ficou sem ciclo.

Exemplo de linhas (Escritório Modelo, fictício):

```
| 2026-04-14 | 08:00 | agente (tarefa agendada) | entrada, pecas.csv | 3 | 1 | 0 | 1 | 2 | nenhum |
| 2026-04-15 | 08:40 | à mão | entrada, pecas.csv | 3 | 1 | 1 | 2 | 3 | tarefa não rodou: computador desligado |
| 2026-04-16 | - | não rodou | - | - | - | - | - | - | advogada em audiência fora; plano B não acionado |
```

Leitura na revisão do mês: quantos dias rodou pelo agente, quantos à mão, quantos não rodou, e se "Advogado agora" e "Peças paradas" estão caindo. Se não caem, o problema não é o ciclo: é a decisão de tese que espera, ou o limite de etapa que não cabe na rotina do escritório.
