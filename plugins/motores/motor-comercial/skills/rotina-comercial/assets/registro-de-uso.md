# Modelo do registro de uso

Copiar para `escritorio/05-automacoes/ciclo-comercial/registro-de-uso.md` no modo configurar. O agente, a tarefa agendada ou quem roda à mão acrescenta uma linha por rodada. O dia em que o ciclo não rodou também ganha linha, escrita por quem percebeu.

É deste arquivo que o ciclo e o script de pendências tiram "desde quando ler": a última linha com data e hora que não seja `não rodou` nem `só o resumo`. Por isso a primeira coluna é sempre a data (AAAA-MM-DD) e a segunda a hora (HH:MM).

```markdown
---
documento: Registro de uso · ciclo comercial
versao: 1
revisado_em: AAAA-MM-DD
dono: [FUNÇÃO]
---

# Registro de uso · ciclo comercial

| Data | Hora | Como rodou | Fontes lidas | Itens | Rascunhos | Bloqueados | Pessoa agora | Erros |
|---|---|---|---|---|---|---|---|---|
```

Valores de "Como rodou":
- `agente (tarefa agendada)`: a tarefa chamou `/motor-comercial:ciclo` e o agente rodou;
- `agente (comando)`: alguém rodou `/motor-comercial:ciclo`;
- `à mão`: o ciclo à mão da `rotina-comercial`, no chat;
- `só o resumo`: só o script de pendências, sem triagem nem rascunhos (não conta como rodada completa);
- `não rodou`: o dia ficou sem ciclo.

Exemplo de linhas (Escritório Modelo, fictício):

```
| 2026-03-10 | 08:30 | agente (tarefa agendada) | entrada, contatos.csv | 3 | 1 | 0 | 0 | nenhum |
| 2026-03-11 | 09:20 | à mão | entrada, contatos.csv | 5 | 2 | 0 | 2 | tarefa não rodou: computador desligado |
| 2026-03-12 | 08:30 | agente (tarefa agendada) | entrada, contatos.csv, agenda | 4 | 3 | 1 | 1 | nenhum |
| 2026-03-13 | - | não rodou | - | - | - | - | - | secretária de folga; plano B não acionado |
```

Leitura na revisão do mês: quantos dias rodou pelo agente, quantos à mão, quantos não rodou, e se "Pessoa agora" e a seção "sem resposta além do prazo" do resumo estão caindo. Se não caem, o problema não é o ciclo: é quem responde ou o prazo da ficha.
