---
name: arte-do-carrossel
description: >-
  Arte do carrossel do curso Marketing Jurídico com Claude (RPC Educação). Transforma o texto aprovado
  pela Banca de Conteúdo em carrossel pronto para postar. Caminho principal: escolhe um modelo da
  biblioteca do curso (Árvore de Links, com 61 modelos do Canva em Elegante, Criativo e Clássico), copia
  o modelo para a conta do Canva do advogado, aplica a identidade fixa dele (cores, fontes, ênfase,
  fotos, assinatura) e monta as lâminas com a skill diagramacao. Sem Canva, usa o motor próprio com os
  6 estilos. Mostra a prévia para o "aprovo", entrega a lista de acabamento e as imagens. Use quando o
  advogado disser "monta a arte", "faz o carrossel com arte", "transforma esse texto em lâminas", "me
  mostra os modelos", "quero esse modelo" (com link ou código), "quero outro modelo", "faz a capa",
  "monta no Canva" ou aceitar a oferta de arte da Banca.
---

# Arte do carrossel

Você transforma texto aprovado em arte com a identidade do advogado, sem cara de IA. **Texto primeiro, arte depois:** nunca monte arte de um texto que não passou pela Banca (orquestrador de copy) e pela Trava OAB.

O princípio da arte: **do modelo vem o layout; a identidade vem sempre da marca do advogado.** Você parte de um carrossel que já existe e foi bem desenhado. Regra sozinha produz design correto e genérico.

Fale de resultado, sem tecniquês: "copiei o modelo para o seu Canva", "troquei as cores pelas suas", "deixei pronto para postar".

## 1. Antes de montar

1. Ache a pasta `meu-marketing-juridico/` e leia `base/imagem.md`: identidade fixa (as 6 constantes), nível do advogado, Mapa do Acervo, preferência de variar ou manter o layout, biblioteca pessoal e "O que nunca aparece". Os modelos já usados estão no topo do `registro-de-pecas.md` (linha "Modelo").
2. Tenha o texto aprovado com a estrutura em blocos, a legenda e o texto alternativo (vêm da Banca).
3. Sem identidade fixa na base: rode antes a fase 2 do rito PICO (skill `rito-pico`). Para o iniciante, ela monta uma identidade mínima em poucos minutos.
4. Veja se o Canva está conectado (ferramentas do Canva nesta sessão).
   - Conectado: caminho principal (seções 2 a 7).
   - Não conectado: diga em uma frase como conectar (Configurações, Conectores, Canva) e ofereça o caminho B (seção 9) enquanto isso.

## 2. Escolher o modelo

A biblioteca do curso é a **Árvore de Links**: https://claude.ai/artifact/Hjt9MKmnwZcu8Troy5SY53 (61 modelos do Canva em três estilos: Elegante, Criativo e Clássico). As descrições de quando escolher cada modelo estão em `assets/catalogo.json`. Regras de escolha em `references/biblioteca.md`.

Três caminhos, conforme o nível do advogado (`references/publicos.md`):
- **Já sei:** o advogado manda o link ou diz o modelo pelo estilo e o número do cartão na Árvore (ex.: "Clássico 44"), ou pelo nome do cartão. Encontre no catálogo pelo campo `na_arvore` ou `nome_na_arvore`. Siga.
- **Me mostra:** mande o link da Árvore para ele navegar e escolher.
- **Sugere:** filtre o catálogo pela base e pela copy e mostre 3 opções, cada uma com uma linha do porquê.

Respeite a preferência de variar ou manter o layout (em `base/imagem.md`), olhando os últimos modelos usados no `registro-de-pecas.md`. Modelo com link pendente ou que não abre: avise e escolha outro.

## 3. Copiar o modelo

Abra o link de modelo pelo conector e crie a cópia na conta do Canva do advogado. O original nunca é editado. Passo a passo técnico em `references/canva.md`. Se o conector não conseguir fazer a cópia, peça ao advogado: "abra este link, clique em Usar modelo e me avise"; depois encontre a cópia na conta dele e siga.

## 4. Aplicar a identidade

Siga `references/identidade.md`:
- troque cada cor do modelo pela cor da marca que cumpre o mesmo papel (fundo, texto, destaque, apoio);
- aplique as 5 constantes obrigatórias (paleta, par de fontes, recurso de ênfase, tratamento de foto, assinatura) e a sexta, se houver;
- tire tudo o que é do modelo e não do advogado: nomes de exemplo, @, sites, logos, ícones de outra profissão, textos em inglês;
- quando a fonte da marca não puder ser aplicada pelo conector, ou quebrar o desenho do modelo, registre na lista de acabamento e mostre como ficou. O advogado pode aprovar a exceção.

## 5. Montar as lâminas

Rode a skill `diagramacao`: ela distribui os blocos pelas lâminas do modelo, mede a densidade, decide título, texto e ênfase, escolhe as fotos pelo Mapa do Acervo, decide onde o texto senta e duplica lâminas quando o texto pede mais do que o modelo tem. Fotos só de `fotos/selecionadas/`, enviadas ao Canva pelo conector. Sem foto, design flat. Nunca imagem gerada.

## 6. Conferir e mostrar

1. Rode o verificador no texto final das lâminas (`PY scripts/verificar_texto.py --texto <arquivo>`; `PY` é `python3` no Mac, `py` no Windows).
2. Confira por `../diagramacao/references/teste.md`.
3. Mostre a prévia de todas as lâminas e diga: "Me diga o que mudar em cada lâmina, ou responda aprovo." Ajuste lâmina a lâmina.
4. **Só salve no Canva depois do "aprovo".** Edição salva não se desfaz. Única exceção: o advogado disse expressamente para seguir sem perguntar (ver `linha-editorial`); aí salve, avise e mostre o resultado no fim.

## 7. Lista de acabamento e entrega

O conector não faz tudo. Feche sempre com a **lista de acabamento**: o que você não conseguiu fazer e como resolver, com mais um comando ou com um clique no Canva. Itens comuns:
- trocar a fonte dos títulos ou do texto pela da marca (no Canva: selecionar o texto, depois Fonte);
- fios e linhas decorativas que não mudam de tamanho nem de lugar;
- lâmina criada do zero com fonte padrão ou sem os enfeites do modelo ("quer que eu refaça duplicando outra lâmina?");
- foto que precisa de recorte fino.

Depois do "aprovo":
1. Exporte em PNG, uma imagem por página.
2. Entregue: as imagens, o link editável do Canva, a legenda, o texto alternativo de cada lâmina e a lista de acabamento.
3. Atualize a rodada no `registro-de-pecas.md` com a linha "Modelo: [na_arvore] · [nome_na_arvore] · Canva: [link da cópia]". É dela que a próxima arte lê os últimos modelos usados.
4. Ofereça o protocolo: "quer que eu prepare a publicação e agende?" (skill `protocolo`).
5. Feche com uma linha de peso, como na skill `uso-do-plano`.

## 8. Favoritos

"Guarda esse modelo" ou "guarda esse jeito": registre em `base/imagem.md`, seção "Biblioteca pessoal", o modelo, o link da cópia aprovada e o que mudou (ex.: "Checklist do escritório: Clássico 07, convite em fundo dourado"). Nas próximas artes, o favorito é o primeiro caminho. Links de modelos que o próprio advogado trouxer entram na mesma seção, com o tipo de carrossel que atendem.

## 9. Caminho B: motor próprio (sem Canva)

Para quem não tem Canva, não conectou ou prefere não usar. O motor desenha as lâminas pelo Google Chrome, em 1080 x 1350, com os 6 estilos do catálogo (`references/catalogo-de-estilos.md`) e a mesma identidade fixa.

1. **Navegador:** se o motor avisar que não achou o Chrome (ou o Edge), diga em uma frase: "para montar a arte eu uso o Google Chrome; instale (é gratuito) e me avise". Comando do motor: `PY scripts/montar_carrossel.py`.
2. **Estilo:** pelo favorito, pelo catálogo visual `assets/catalogo/catalogo.html` (Mac: `open "<caminho>"`; Windows: `start "" "<caminho>"`) ou pela sugestão da tabela do catálogo.
3. **Roteiro:** a skill `diagramacao` monta `carrosseis/AAAA-MM-DD-tema-curto/carrossel.json` no formato de `references/roteiro.md`.
4. **Rodar:** `PY scripts/montar_carrossel.py "<pasta>/carrosseis/<tema>/carrossel.json" --base "<pasta>"`. Com item para CORRIGIR no texto (código 3), mostre o trecho ao advogado com a troca sugerida e peça o "ok"; não corrija em silêncio. Código 1: resolva o que o relatório aponta.
5. **Conferir e mostrar:** abra a `prancha.png` para a primeira olhada e as lâminas com foto em tamanho real; mostre a `prancha.html` para o "aprovo". Ajuste com `--so 3` (ou `--so 3,5`).
6. **Entregar:** depois do "aprovo", rode com `--alta` e entregue a pasta `png/`, a legenda e o texto alternativo.

Sem navegador e sem Canva: entregue o briefing de arte (lâmina a lâmina, o texto, a foto, a posição do título, as cores em código e as fontes) para ele montar à mão. O fluxo não trava.

## Checklist (rode em silêncio)

- [ ] Texto aprovado pela Banca e com parecer da Trava; nada reescrito na arte sem "ok".
- [ ] Modelo escolhido por um dos três caminhos; variar ou manter respeitado.
- [ ] Cópia feita; original intocado.
- [ ] Identidade aplicada por papel; restos do modelo retirados.
- [ ] Diagramação rodada; nenhum texto sobre rosto; nenhum texto de leitura abaixo de 36 px.
- [ ] Fotos reais; sem foto, design flat.
- [ ] Verificador limpo; identificação no fecho.
- [ ] "Aprovo" antes de salvar e exportar; lista de acabamento entregue; registro atualizado.
