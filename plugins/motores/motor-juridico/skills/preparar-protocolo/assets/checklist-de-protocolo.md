# Modelo do checklist de protocolo

Copiar para `escritorio/07-operacao/juridico/casos/<codigo>/protocolo/<peca>-AAAA-MM-DD.md` no passo 2, preenchido com a ficha jurídica, a linha do `pecas.csv` e o checklist do sistema. O checklist é interno: não vai para o processo nem para o cliente.

```markdown
---
documento: Checklist de protocolo · [PEÇA] · [CÓDIGO]
peca_id: P-AAAA-NNNN
codigo_caso: C-AAAA-NNNN
sistema: [PJe | eproc | e-SAJ | Projudi | outro]
prazo_interno: AAAA-MM-DD
preparado_em: AAAA-MM-DD HH:MM
preparado_por: a pedido | ciclo
status: preparado            # preparado | conferido-pela-pessoa | protocolado
---

# Protocolo · [PEÇA] · [NOME CURTO]

## 1. A peça pode ir?
- Etapa: aprovada · Citações: verde · Dados: ok
- Relatório de conferência: `casos/[CÓDIGO]/conferencias/[ARQUIVO]`
- Versão final: `casos/[CÓDIGO]/minutas/[PEÇA]-v[N].md`, sem nenhuma marcação (script, `--minuta`)

## 2. Arquivos, na ordem
| Nº | Arquivo | O que é | Citado na peça como | Situação |
|---|---|---|---|---|
| 01 | 01-[PEÇA].pdf | a peça final | | |
| 02 | 02-procuracao.pdf | procuração | doc. 1 | |

## 3. Resultado do script
(colar aqui a saída do `conferir_pasta.py`: PRONTA ou CORRIGIR ANTES, e o que corrigir)

## 4. O que conferir no sistema (a pessoa)
- [ ] Formato e tamanho aceitos pelo [SISTEMA] [CONFERIR]
- [ ] Tipo de petição e tipo de cada documento na lista do sistema [CONFERIR]
- [ ] Sigilo: [NÃO SE APLICA | o advogado decidiu pedir segredo de justiça; marcar no sistema] [CONFERIR]

## 5. Custas
- [ ] [GUIA EMITIDA POR (guia_de_custas), PAGA, COMPROVANTE EM 0N-comprovante-de-custas.pdf | GRATUIDADE PEDIDA NA PEÇA]

## 6. Quem faz (sigla H)
- Assina: [quem_assina], com [assinatura], no próprio sistema
- Protocola: [quem_protocola]
- A IA não recebe senha, PIN, token nem certificado, e não entra no sistema.

## 7. Depois do protocolo
- Sistema: · Número: · Data e hora:
- Comprovante: `casos/[CÓDIGO]/protocolo/[PEÇA]-AAAA-MM-DD-comprovante.pdf`
- `pecas.csv`: protocolada (registrar_protocolo.py, com o ok)
- Histórico do cliente (motor-experiencia, se instalado): linha `trabalho-do-escritorio`, sem número
```
