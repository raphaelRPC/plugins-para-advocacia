# Aprender com o uso

As habilidades melhoram quando guardam o que o advogado corrige. A primeira mensagem sai no padrão do plugin com o tom da ficha. A décima já sai com as dez correções anteriores.

## O arquivo

Um arquivo por plugin, em `escritorio/04-base/comum/`: `aprendizados-comercial.md` (motor-comercial), `aprendizados-experiencia.md` (motor-experiencia) `aprendizados-juridico.md` (motor-juridico) e `aprendizados-controladoria.md` (motor-controladoria). Regra que vale para mais de um (por exemplo, uma frase que o escritório nunca usa) vai para a ficha do escritório, no campo certo. Se o arquivo não existir, a habilidade cria com este cabeçalho:

```markdown
---
documento: Aprendizados [comercial | da experiência | jurídicos | da controladoria]
versao: 1
revisado_em: AAAA-MM-DD
dono: [A PREENCHER]
---

# Aprendizados [comercial | da experiência | jurídicos | da controladoria]

Regras que o escritório ensinou às habilidades. Valem mais do que o padrão do plugin. Uma linha por regra.

| Data | Habilidade | Regra | Exemplo (anonimizado) | Situação |
|---|---|---|---|---|
```

Situação: `em uso`, `em teste` (vale, mas o advogado quer ver de novo) ou `retirada` (não apague a linha, só mude a situação). Regra que subiu para a ficha vira `retirada` com a nota "incorporada à ficha: <campo>".

## Quando propor um aprendizado

Ao fim de cada tarefa, se o advogado corrigiu alguma coisa, a habilidade transforma a correção numa regra curta e pergunta: "Quer que eu guarde isto para as próximas vezes?". Exemplos de correção que vira regra:

| O advogado disse | A regra guardada |
|---|---|
| "Tira esse 'prezado', ninguém fala assim aqui" | Não abrir mensagem com "prezado" ou "prezada". |
| "Pedido de pensão com criança sempre vem para mim" | Triagem de alimentos com criança envolvida vai para o advogado titular, prioridade alta. |
| "Na proposta, o parcelamento é sempre sem juros até 6 vezes" | Proposta: parcelamento sem juros em até 6 vezes. |
| "Esse cliente não respondeu, mas não manda mais nada, ele pediu" | Contato que pediu para não receber mensagens sai do follow-up e fica registrado. |

Regras de guarda:
1. **Só com o ok.** Nada entra sem o advogado aprovar a frase.
2. **Uma regra por linha,** com verbo e objeto. Nada de "melhorar o tom".
3. **Sem dado de cliente.** O exemplo vai anonimizado.
4. **Conflito com a ficha:** se a regra contradiz um campo da ficha, pergunte qual vale e atualize os dois.
5. **Conflito com a ética** (seção 4 das regras): a habilidade explica por que não pode guardar e propõe uma versão que cabe.

## Revisão

Quando o arquivo passar de 30 linhas `em uso`, ou a cada mês, a habilidade que estiver rodando oferece uma revisão: juntar regras repetidas, subir para a ficha o que virou política do escritório (por exemplo, o parcelamento vai para `entrada_e_parcelas`) e retirar o que não vale mais. As habilidades de auditoria (`auditar-conversas-comerciais` e `auditar-conversas`), quando instaladas, fazem isso a partir de conversas reais.
