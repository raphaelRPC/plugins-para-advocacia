# Biblioteca de modelos

## Onde está

- **Árvore de Links (vitrine):** https://claude.ai/artifact/Hjt9MKmnwZcu8Troy5SY53. É a página que o advogado navega, com a miniatura e o link de modelo de cada carrossel, nos três estilos. O endereço não muda quando a biblioteca é atualizada.
- **Catálogo (para você):** `../assets/catalogo.json`. Tem, para cada modelo, o link de modelo, o lugar na Árvore (`na_arvore`, ex.: "Clássico 07") e as descrições: `quando_escolher`, `quando_evitar`, `tipos_carrossel`, `tom`, `publico`, `foto`, `fotos_tipo`, `densidade`, `aguenta_longa`, `riscos_oab`, `observacoes`.

Para sugerir, use o catálogo. Para mostrar ao advogado, mande a Árvore. Se o catálogo não tiver um modelo que aparece na Árvore (a biblioteca cresceu), trate o modelo pelo nome e pela miniatura da Árvore e avise que ele ainda não tem descrição.

## Os três estilos

| Estilo | Quando escolher |
|---|---|
| Elegante | Advogado que quer ser percebido como sofisticado, seguro e de alto padrão, com presença de revista. A maioria dos modelos vive da foto em tela cheia: funciona melhor para quem tem ensaio fotográfico. Família de alto padrão, sucessões e patrimônio, empresarial para sócios e executivos, imobiliário, consultoria personalizada. Tom A e B |
| Criativo | Advogado que quer humanizar o perfil, mostrar rotina e bastidor e falar de igual para igual. Colagem, recortes, notas, marca-texto, cores mais vivas; pede fotos variadas. Empreendedores, startups, criadores, consumidor, trabalhista do lado do empregado, famílias jovens. Tom B e C. Evite em temas pesados (penal, violência, luto) |
| Clássico | Quando o conteúdo é o protagonista: explicativo, lista, checklist, passo a passo, mito e fato, perguntas frequentes. Grade limpa e hierarquia clara; vários funcionam só com fundo e texto, o que serve ao iniciante sem ensaio. Tributário, empresarial, previdenciário, trabalhista, contratos, direito público. Tom A e B. A escolha mais segura para o primeiro carrossel |

## Como sugerir 3 modelos

1. **Filtre pelo advogado:** `publico` contém o nível dele (mapa dos 7 públicos em `publicos.md`); `tom` contém a dose de tom dele, deduzida da seção "Voz" de `base/posicionamento.md` (A sóbrio e institucional, B próximo com toques humanos, C descontraído; se não der para deduzir, pergunte); `foto` compatível com o Mapa do Acervo (sem fotos boas: só `opcional` ou `nao_usa`).
2. **Filtre pela copy:** `tipos_carrossel` contém o tipo da peça, pelo mapa abaixo; blocos LONGOS na estrutura pedem `aguenta_longa: true`; estrutura com muitos TÓPICOS pede `densidade` `media` ou `longa`.

| Tipo na Banca | Procure em `tipos_carrossel` |
|---|---|
| Explicativo | explicativo, dicas, novidade legal |
| Tutorial com print | passo a passo |
| Mito e fato | mito e fato |
| Checklist, lista de documentos | checklist, lista |
| Lista de erros ou critérios | lista, dicas |
| Bastidor | bastidor |
| Apresentação, quem sou | apresentação |
| Reflexão, insight | reflexão |
| Perguntas frequentes, regra com a lei | perguntas frequentes, citação de lei, explicativo |
3. **Filtre pelo histórico:** se a preferência for variar, tire os dois últimos modelos usados; se for manter por série, o modelo da série vem primeiro.
4. **Leia** `quando_escolher` e `quando_evitar` dos que sobraram e escolha os 3 que mais combinam com o posicionamento e a oferta da base.
5. **Mostre** cada opção com o lugar na Árvore, o nome e uma linha do porquê. Inclua o alerta de `riscos_oab` quando houver (ex.: modelo de depoimentos vira lâmina de perguntas frequentes).

## Variar ou manter

Preferência do advogado, guardada em `base/imagem.md`: **variar** (layout diferente a cada carrossel, sem repetir os dois últimos) ou **manter por série** (todo mito e fato no mesmo modelo, todo checklist em outro). Pergunte uma vez, na primeira arte, se a base não tiver. A identidade vale nos dois casos.

## Cuidados

- Copie sempre pelo `link_modelo`. O `design_id` do catálogo é o original da biblioteca: nunca o copie nem o edite.
- Na biblioteca pessoal do advogado, só entram modelos que ele tem direito de usar: modelos do Canva, modelos comprados, designs dele ou do designer dele. Carrossel de outro advogado ou criador tirado do Instagram fica fora.
- Os textos, nomes e marcas dos modelos são exemplos do Canva: nada do texto original fica.

## Para a equipe do curso: atualizar a biblioteca

Quando a equipe acrescenta modelos (pedido "atualiza a biblioteca"):
1. O design novo entra na pasta do Canva da biblioteca, na subpasta do estilo (ELEGANTE, CRIATIVOS ou CLÁSSICO). Uma pasta nova vira um estilo novo.
2. A equipe gera o link de modelo do design (Canva, Compartilhar, link de modelo).
3. Leia o design pelo conector (páginas e miniaturas) e escreva a entrada do catálogo no mesmo formato das outras, com a descrição vinda do que se vê nas lâminas.
4. Republique a Árvore de Links no mesmo endereço e gere uma versão nova do catálogo, com `versao` e `atualizado_em` novos.
