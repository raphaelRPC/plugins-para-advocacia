# Diretrizes de foto e Mapa do Acervo

Como o Claude lê, classifica e escolhe as fotos do ensaio do advogado. Base: as diretrizes de foto de Filipe Nascimento (RPC Educação), com os acréscimos de leitura individual da estrutura do carrossel v2. O Mapa do Acervo é feito uma vez, na Fase 2 do Rito, e fica em `base/mapa-do-acervo.md`; a arte consulta o mapa em vez de abrir foto por foto, o que também economiza o plano.

Toda foto tem **um tipo** (o que ela é visualmente) e **uma função** (o papel que cumpre no post). O tipo ajuda a achar a foto; a função decide onde ela entra.

## 1. As três funções

| Função | O que comunica | Quando usar |
|---|---|---|
| **Autoridade** | Firmeza, seriedade, competência técnica | Temas técnicos e institucionais, capas, lâminas de credibilidade, regra, número, mito e fato |
| **Conexão** | Proximidade, humanidade, identificação | Quando o post fala da pessoa, das experiências, dos valores; o fecho |
| **Prova e processo** | O trabalho e a rotina por dentro (bastidor) | Mostrar método, preparo e cuidado: passo a passo, tutorial, checklist |

Ressalva de OAB: prova e processo **nunca** é prova de resultado que vende. É método e credibilidade, sem promessa e sem expor cliente, parte ou processo. Foto com terceiros entra como bastidor, nunca como resultado.

Cada foto recebe uma função principal (o grupo em que aparece no mapa). Se servir a outra, entra como secundária no fim da linha (`também: Conexão`). A foto aparece no mapa uma vez só.

## 2. Os nove tipos

| # | Tipo | Como reconhecer | Sensação | Função mais comum |
|---|---|---|---|---|
| 1 | Retrato posado clássico | olhar para a câmera, postura composta, enquadramento central, fundo limpo | firmeza, institucional | Autoridade |
| 2 | Retrato espontâneo | riso, olhar fora da câmera, gesto no meio do movimento | humaniza, aproxima | Conexão |
| 3 | Foto em ação ou bastidor | fazendo algo do trabalho: lendo, escrevendo, falando, estudando | processo, entrega | Prova e processo |
| 4 | Plano de detalhe | recorte fechado em mãos, objetos, livros, caneta; rosto ausente ou parcial | foco, sensibilidade | Prova e processo |
| 5 | Contemplativa ou introspectiva | olhar perdido, janela, pausa | pausa, intimidade | Conexão |
| 6 | Editorial ou estilizada | luz marcada, pose de personalidade, composição de revista | força visual, impacto | Autoridade |
| 7 | Ambiente profissional | o escritório com a pessoa inserida nele | credibilidade, contexto | Autoridade ou Prova e processo |
| 8 | Foto com pessoas | equipe, sócios, colegas em cena | colaboração | Prova e processo ou Conexão |
| 9 | Cena da locação | o lugar sem a pessoa: fachada, corredor, sala vazia, rua | contexto, respiro | Conexão (respiro visual) |

Tipo 8: nunca expõe cliente, parte ou caso. Equipe e colegas sim; quem é atendido, não.

## 3. A leitura de cada foto (o que vai no mapa)

Para cada foto, preencha:

| Campo | Valores | Para que serve |
|---|---|---|
| tipo e função | os 9 tipos e as 3 funções | que post e que lâmina |
| leitura | uma frase: enquadramento, postura, expressão, cenário, luz, e o uso ("serve de capa para...", "boa para a lâmina de...") | escolha rápida |
| expressão | séria, sorriso contido, sorriso aberto, falando ou gesticulando, introspectiva | a emoção da lâmina |
| olhar | para a câmera, para a esquerda, para a direita, para baixo, para um objeto | de que lado o texto senta |
| plano | detalhe, fechado (rosto), médio (cintura), americano (joelho), aberto (corpo e ambiente) | que modo de foto |
| orientação | em pé, deitada, quadrada | foto deitada não entra sangrada nem em janela |
| rosto | terço de cima, do meio ou de baixo; esquerda, centro ou direita | onde o texto nunca pode ficar |
| área livre | cima, baixo, esquerda, direita ou nenhuma (fundo calmo: parede, céu, roupa escura) | onde o texto pode ficar |
| ensaio | sessão, roupa, luz (quente, fria, natural, estúdio) | coerência dentro do carrossel |

Critérios da frase de leitura: descreva o que se vê antes do que se sente; feche com o uso; diga o limite ("sem área livre para texto", "rosto ocupa o quadro todo", "fundo com informação demais").

**Não usar (até tratar):** documento, tela ou pessoa de fora identificável; logomarca ou símbolo oficial da OAB ao fundo (Provimento 205/2021, art. 5º, § 2º); brasão ou marca de terceiro em destaque; foto tecnicamente comprometida. Para ler o acervo sem abrir foto por foto, use a folha de fotos (`ver_fotos.py` da skill `arte-do-carrossel`, no plugin de carrossel) e abra em tamanho real só as que ficarem em dúvida.

## 4. A cesta do ensaio

Ensaio só de retratos faz o rosto aparecer em toda lâmina com foto, e o texto passa a disputar espaço com ele. Oriente o próximo ensaio para uma cesta mínima: cerca de **40% retratos**, **40% detalhe e ambiente** (mesa, mãos, livros, agenda, fachada, janela) e **20% bastidor**. E nenhuma foto com o logo da OAB. A linha de lacunas do mapa vira o briefing desse ensaio.

## 5. Formato do Mapa do Acervo

Agrupado por função principal, uma linha por foto:

```
### MAPA DO ACERVO DE FOTOS
Atualizado em: AAAA-MM-DD

AUTORIDADE
- [arquivo] · [tipo] · [leitura] · expressão: … · olhar: … · plano: … · orientação: … · rosto: … · área livre: … · ensaio: … · também: [função]

CONEXÃO
- …

PROVA E PROCESSO
- …

NÃO USAR (até tratar)
- [arquivo] · [motivo]

LACUNAS
- Tipos ausentes neste ensaio: [lista]
```

O trecho `também:` só aparece quando existe função secundária. Exemplo de linha:

```
- capa-01.jpg · retrato posado clássico · meio corpo, olhar direto, terno escuro sobre parede neutra; capa de tema técnico, mito e fato · expressão: séria · olhar: câmera · plano: médio · orientação: em pé · rosto: terço de cima, centro · área livre: baixo · ensaio: estúdio, terno azul, luz de estúdio
```
