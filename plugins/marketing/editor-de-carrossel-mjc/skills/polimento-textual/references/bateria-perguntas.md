# Polimento textual: rascunho central

Etapa 2 do plugin de copy. Uma skill que obriga a IA a se questionar, bater de frente com o próprio texto e defender ou reescrever cada escolha. O princípio veio de uma observação de uso: o modelo entrega texto melhor quando é confrontado, criticado e apontado. Esta skill institucionaliza o confronto.

---

## PARTE 1: O princípio (por que o confronto funciona)

A IA gera pelo caminho estatisticamente mais provável e para na primeira versão aceitável. Crítica externa força a reavaliação: o modelo abandona o caminho padrão e procura um menos óbvio. A skill simula internamente o crítico que o usuário seria.

### A regra de ouro das perguntas

Pergunta aberta recebe autoelogio. Pergunta que pressupõe o defeito obriga a encontrá-lo.

Errado: "O texto está claro?" (resposta provável: sim)
Certo: "Qual é o trecho mais confuso? Cite as palavras exatas."

Toda pergunta da bateria abaixo segue este formato: já afirma que o defeito existe e exige localização precisa. Nunca perguntar "se", sempre perguntar "qual" e "onde".

### As três proibições do crítico interno

1. **Proibido responder "está tudo bem".** Todo texto tem um trecho mais fraco que os outros; o trabalho é achá-lo.
2. **Proibido acatar todas as críticas.** Ceder a tudo é tão covarde quanto não criticar. Crítica injusta se rebate com argumento.
3. **Proibido crítica genérica.** Toda crítica cita as palavras exatas do trecho e diz o que há de errado nelas. "O texto podia ser mais direto" não vale; "a frase X esconde o agente na voz passiva" vale.

### O tique de compensação (vigiar o substituto)

Quando um tique é proibido, o modelo compensa com o vizinho. Proibido o travessão, entra o picote: frases curtas demais, todas terminando em ponto, em sequência. "Fechar o notebook eu já fazia. Escutar pede mais. Pede tempo." O ritmo vira metralhadora e o texto segue soando de máquina, com outra assinatura.

A regra: fragmento é tempero, prosa é o prato. Três frases curtas seguidas acendem o alerta. Os substitutos que devolvem o fluxo: vírgula, dois-pontos, ponto e vírgula, conectivos falados ("e", "mas", "aí", "que", "porque", "só que"), interjeições ("olha", "pois é", "ora") e figuras de linguagem que criam ritmo dentro da frase, como a anáfora intencional, a gradação e a antítese.

Picotado: "Escutar pede mais. Pede tempo. Pede porta fechada."
Fluido: "Escutar pede mais: pede tempo e uma porta que feche de verdade."

---

## PARTE 2: A mecânica (o tribunal do texto)

1. **O texto na mesa.** Recebido do usuário ou recém-escrito.
2. **Acusação.** O crítico interno responde a bateria de perguntas da Parte 3, camada por camada, citando trecho exato em cada resposta.
3. **Julgamento.** Para cada defeito apontado, uma decisão obrigatória: reescrever ou defender. Defender exige argumento ("a repetição de 'intimide' é ênfase intencional, mantida"). Empate não existe.
4. **Reescrita** dos trechos condenados.
5. **Segunda acusação, mais curta.** Sobre a versão reescrita: "aponte os 3 trechos que ainda são os mais fracos". Três, obrigatoriamente, mesmo que o texto tenha melhorado; força o olhar relativo.
6. **Julgamento final e entrega.**

O ciclo de acusação roda no máximo duas vezes. Mais que isso, o modelo começa a piorar o texto pra ter o que corrigir.

---

## PARTE 3: A bateria de perguntas (pelas camadas da língua)

### Camada 1: Intenção e leitor (pragmática)

- O que o leitor deve fazer, sentir ou entender ao terminar? Responda em uma frase. Se a resposta tem duas frases, o texto tem dois objetivos e um deles precisa morrer.
- Qual é a única ideia central? Qual frase do texto não serve a ela?
- Qual frase existe pra impressionar o autor em vez de servir o leitor?
- Em que trecho exato o leitor desiste? Todo texto tem um ponto de abandono; localize.

### Camada 2: Sentido (semântica)

- Qual palavra está aproximada em vez de exata? Qual seria a exata?
- Qual frase é verdadeira mas não prova nada? Teste: se ninguém no mundo discordaria dela, ela não diz nada.
- Qual afirmação não se sustenta com fato? Ou entra o fato, ou sai a afirmação.
- Onde há ambiguidade não intencional (o leitor pode entender outra coisa)?
- Qual abstração está escondendo uma coisa concreta que o autor sabe dizer?

### Camada 3: Construção da frase (sintaxe)

- Em qual frase a palavra mais forte está enterrada no meio? As posições de força são o início e, principalmente, o fim.
- Onde a voz passiva esconde quem faz a ação? "Foi decidido que" esconde quem decidiu.
- Qual frase carrega subordinadas demais e pede divisão em duas?
- Qual palavra sai sem nenhuma perda de sentido? Corte. Repita a pergunta até doer.
- Qual negação pode virar afirmação? "Não é difícil" é mais fraco que "é simples".

### Camada 4: Costura (coesão e progressão)

- Qual parágrafo repete o anterior com outra roupa em vez de avançar?
- Se os parágrafos forem embaralhados, o leitor percebe? Se não percebe, a ordem é arbitrária e a estrutura é fraca.
- Qual pronome ou retomada ("isso", "esse ponto", "tal coisa") aponta pra uma referência que não é óbvia?
- Qual primeira frase de parágrafo não ganha o direito de existir (não puxa o leitor pra dentro)?
- Onde a transição depende de conectivo em vez de depender da lógica? Se tirar o conectivo e a junção quebrar, o problema é a ordem das ideias.

### Camada 5: Escolha de palavra (léxico e registro)

- Onde o registro muda sem intenção (começa falado e escorrega pro formal, ou o contrário)?
- Qual repetição é eco acidental e qual é ênfase? Eco se corta, ênfase se mantém.
- Quais palavras deste texto qualquer pessoa usaria? Qual palavra só este autor usaria? Se nenhuma é só do autor, o texto é de ninguém.
- Qual verbo fraco com substantivo ("fazer uma análise", "dar uma olhada") pode virar verbo forte ("analisar", "olhar")?

### Camada 6: Som e ritmo (prosódia)

- Lido em voz alta, onde a língua tropeça? O tropeço aponta o defeito que o olho não vê.
- Onde o fôlego acaba antes do ponto final?
- Onde há eco de terminação em frases vizinhas ("-mente... -mente", "-ção... -ção", "-ando... -ando")?
- Os tamanhos de frase variam ou marcham no mesmo passo? Conte as palavras de três frases seguidas; se forem quase iguais, o ritmo é de máquina.
- Onde há três ou mais frases curtas seguidas terminando em ponto (picote)? Qual par se une com vírgula, dois-pontos, ponto e vírgula ou conectivo?
- Qual fragmento sem verbo pode voltar pra dentro da frase anterior sem perder força?
- Há rima acidental ou cacofonia ("por cada", "ela tinha", "boca dela")?

### Camada 7: Substância (a camada da honestidade)

- Qual frase é feita, caberia no texto de qualquer pessoa e não custa nada a quem escreve?
- Cadê o número, o nome, a data, a cena? Localize o parágrafo mais pobre de matéria concreta.
- Qual detalhe só o autor poderia saber? Se não existe nenhum, o texto não tem dono.
- Se o parágrafo final for cortado, o texto piora? Se não piora, corte.
- O que aqui foi inventado pra preencher espaço? Invenção de fato é defeito grave; se falta matéria, a resposta é pedir ao autor, nunca fabricar.

---

## PARTE 4: Formato de resposta da skill

1. **Acusação:** lista de defeitos, cada um citando o trecho exato e a camada violada
2. **Julgamento:** veredito por item (reescrever ou defender, com o argumento da defesa quando houver)
3. **Versão polida**
4. **Resumo:** o que mudou, agrupado por camada

Se o usuário pedir só a versão final, entregar a versão polida com resumo de 3 linhas.

---

## PARTE 5: Integração com as outras skills

Ordem de operação no plugin de carrossel:

1. Escrever (skill de estrutura do carrossel, etapa 3)
2. **Polir (esta skill):** força, precisão, costura, ritmo
3. Humanizar (skill humanizar-texto): remover assinatura de IA e frase feita
4. Releitura final em voz alta

As duas skills atacam problemas diferentes: humanizar-texto remove o que denuncia máquina; polimento-textual remove o que é fraco mesmo sendo humano. Um texto pode passar na humanização e ainda ser mole; pode ser forte e ainda cheirar a IA. Por isso são duas passadas.
