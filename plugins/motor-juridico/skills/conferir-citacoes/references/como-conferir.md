# Como conferir cada tipo de citação

Complemento de `../../docs/citacoes.md` (a regra) para o passo 4 da `conferir-citacoes`. Leia na hora de conferir, tipo por tipo. Nada aqui substitui a fonte: o que está escrito são as perguntas que a conferência responde.

## 1. O que cada conferência responde

| Tipo | Onde | As perguntas | Fica verde quando |
|---|---|---|---|
| Lei e artigo | Texto compilado no portal oficial (federal, estadual, municipal) | O artigo existe nesse diploma? A redação citada é a vigente na data dos fatos e na data da peça? Houve revogação, veto ou nova redação? O parágrafo e o inciso são os certos? | Existe, está vigente nas duas datas e a peça usa para o que o texto diz |
| Trecho de lei entre aspas | O mesmo texto compilado, salvo em `conferencias/fontes/` | Bate palavra por palavra? (o script compara com `--fontes`) | O script diz "bate" e a redação é a vigente |
| Súmula | Página de súmulas do tribunal | Existe com esse número nesse tribunal? Foi cancelada, revisada ou superada? O enunciado é o que a peça diz? | Existe, não foi cancelada, enunciado igual |
| Tema de repercussão geral ou de repetitivo, IRDR, IAC | Página de temas do tribunal | O número é desse tribunal? Já tem tese firmada ou está pendente? Houve modulação, revisão, suspensão de processos? A tese diz o que a peça diz? | Tese firmada, vigente, e a peça usa a tese do jeito que ela foi fixada |
| Julgado | Pesquisa no Jus IA e inteiro teor no portal do tribunal | Existe? Número, classe, órgão, relator e data certos? A ementa e o voto dizem o que a peça diz? Não foi reformado depois? | Os cinco dados batem e o inteiro teor sustenta a frase da peça |
| Doutrina | O livro ou o artigo, com edição e página | A obra existe nessa edição? A página é a certa? A frase está lá? | Obra, edição, página e frase conferidas por quem tem o livro |
| Menção vaga | Não tem onde conferir | "Entendimento pacífico" de quem, em qual julgado? | Nunca: troque por julgado ou precedente conferido, ou tire a frase |

## 2. Como decidir a cor

1. **Verde** só com a fonte aberta na conversa, na base dentro da validade, ou num texto oficial salvo. "Acho que é isso" não é verde.
2. **Amarelo** quando existe mas não está como a peça diz: a redação mudou, o número está trocado, a peça diz mais do que o julgado diz, a súmula foi revisada, o precedente foi superado em parte, as aspas não batem, a frase é vaga.
3. **Vermelho** quando não existe, foi cancelada, revogada, reformada, ou diz o contrário. No treino, o número inventado de `../../docs/casos-ficticios.md`.
4. **Cinza** quando a fonte não abriu agora (portal fora do ar, sem acesso, livro que ninguém tem à mão). A marca fica e a peça não vai para protocolo.
5. **Na dúvida entre duas cores, a pior.**

## 3. A peça diz o que a fonte diz?

É a pergunta que mais falha. Três testes rápidos:
- **Generalização:** o julgado decidiu um caso com um detalhe que o nosso não tem (por exemplo, perícia anulada porque o perito não era especialista, e a peça cita para "toda perícia que não analisou o relatório")? Amarelo, com a distinção escrita.
- **Força:** a peça diz "é pacífico" e a base tem um julgado a favor e um contra? Amarelo, e a frase fica do tamanho da prova.
- **Tempo:** o julgado é anterior a uma mudança de lei ou a uma tese vinculante sobre o mesmo ponto? Amarelo ou vermelho, conforme o que mudou.

## 4. O texto oficial salvo

Para conferir aspas palavra por palavra, salve o trecho do portal num arquivo de texto em `07-operacao/juridico/casos/<codigo>/conferencias/fontes/<diploma>-art-<n>.txt`, com o cabeçalho:

```
# Fonte: [DIPLOMA], art. [N]
# Copiado do texto compilado em: [URL DO PORTAL OFICIAL]
# Consultado em AAAA-MM-DD
[o texto do artigo, copiado do portal, sem mexer]
```

Quem copia é a pessoa, ou o Claude com o portal aberto na conversa. Nunca de memória. O arquivo vale para aquela conferência; na próxima peça, abra o portal de novo.

## 5. Doutrina

O script não reconhece doutrina com segurança (cada escritório cita de um jeito). No passo 3, leia a peça procurando nome de autor, "ensina", "leciona", "segundo [AUTOR]", "apud", edição e página, e acrescente cada uma ao registro. Sem a obra à mão, a citação fica cinza. Obra de `doutrina_de_referencia` da ficha jurídica: confira se a edição citada é a que o escritório usa.
