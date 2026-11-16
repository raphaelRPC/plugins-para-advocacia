# Modelo do registro de uso

Copiar para `escritorio/05-automacoes/ciclo-da-experiencia/registro-de-uso.md` no modo configurar. O ciclo acrescenta uma linha a cada rodada. O dia em que ele não rodou também ganha linha, escrita por quem percebeu.

```markdown
---
documento: Registro de uso · ciclo da experiência
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Registro de uso · ciclo da experiência

| Data | Hora | Como rodou | Leu desde | Clientes ativos | Pessoa agora | Sem notícia | Rascunhos (ajustados · bloqueados) | Erros |
|---|---|---|---|---|---|---|---|---|
```

Valores de "Como rodou": `agente`, `agendada`, `manual`, `manual (agendada falhou)`, `não rodou`.

Exemplo de linhas (Escritório Modelo, treino):

```
| 2026-04-10 | 08:00 | agendada | 2026-04-09 08:00 | 8 | 3 | 2 | 6 (1 · 1) | nenhum |
| 2026-04-13 | 09:10 | manual (agendada falhou) | 2026-04-10 08:00 | 8 | 1 | 1 | 4 (0 · 0) | computador desligado na sexta à noite |
| 2026-04-14 | - | não rodou | - | - | - | - | - | secretária de folga; plano B não acionado |
```

Na revisão do mês: quantos dias rodou, quantos à mão, quantos não rodou, e se a coluna "Sem notícia" está caindo. Se não cai, o problema não é o ciclo: é quem aprova a fila ou a régua da ficha.
