// Formatos de vídeo (as receitas do catálogo de estilos), com as peças que cada um usa.
// pecas: ids de assets/animacoes/pecas.js. corte (seco, respiro, pausas), velocidade e densidade (poucas, medias, cheia):
// o ponto de partida que a prancha do vídeo preenche quando o advogado escolhe este formato. semRosto: o formato não usa
// a imagem da câmera (o motor faz o vídeo com o comando cenas). Mesma informação de references/catalogo-de-estilos.md, em forma de dados.
window.FORMATOS = [
  { id: 'convite', nome: 'Convite', quando: 'Chamar para evento, aula ou material gratuito de conteúdo.', duracao: '40 a 60 s', ritmo: 'cortes por frase, 1,1x',
    estrutura: ['Cartão-convite na abertura', 'Data em título de duas camadas', 'O que a pessoa leva, em rótulos', 'Chamada e o @ no fecho'],
    pecas: ['bilhete', 'titulo', 'rotulos', 'formula', 'aproximacao', 'chamada', 'perfil'], familia: 'editorial', legenda: 'palavra-grande', corte: 'respiro', velocidade: 1.1, densidade: 'medias', imagem: 'bilhete' },
  { id: 'pauta-quente', nome: 'Pauta quente', quando: 'Lei nova, decisão pública ou notícia do dia explicada.', duracao: '40 a 75 s', ritmo: 'cortes por frase',
    estrutura: ['Gancho com a notícia', 'Página oficial grifada em cima', 'O que muda para quem assiste', 'Mito e fato ou marca-texto no ponto principal', 'O @ no fecho'],
    pecas: ['faixa', 'busca', 'marcatexto', 'mitofato', 'linhadotempo', 'perfil'], familia: 'editorial', legenda: 'destaque', corte: 'respiro', velocidade: 1.1, densidade: 'medias', imagem: 'faixa' },
  { id: 'tutorial', nome: 'Tutorial', quando: 'Ensinar a usar uma ferramenta, um sistema ou um passo a passo.', duracao: '45 a 90 s', ritmo: 'cortes por frase',
    estrutura: ['A tela em cima, você embaixo', 'Passos numerados ou trilha', 'Diagrama da regra', 'Chamada no fecho'],
    pecas: ['faixa', 'trilha', 'diagrama', 'prompt', 'comando', 'celular', 'notebook', 'palavra'], familia: 'editorial', legenda: 'destaque', corte: 'respiro', velocidade: 1.1, densidade: 'cheia', imagem: 'faixa' },
  { id: 'dica-unica', nome: 'Dica única', quando: 'Uma dica só, falada direto para a câmera.', duracao: 'cerca de 40 s', ritmo: 'cortes por frase, sem respiro',
    estrutura: ['Título fixo no alto do começo ao fim', 'Legenda abaixo do queixo', 'Print ou página quando cita algo', 'Marca-texto no termo principal'],
    pecas: ['fixo', 'print', 'marcatexto', 'seta', 'perfil'], familia: 'editorial', legenda: 'destaque', corte: 'seco', velocidade: 1.1, densidade: 'poucas', imagem: 'fixo' },
  { id: 'cartaz', nome: 'Cartaz', quando: 'Vídeo curto sem fala, com um texto útil; o conteúdo completo vai na legenda do post.', duracao: '6 a 10 s', ritmo: 'sem cortes',
    estrutura: ['Um plano escurece o vídeo', 'Título e três linhas entram na tela', 'Assinatura com o @'],
    pecas: ['cartaz'], familia: 'editorial', legenda: 'nenhuma', corte: 'pausas', velocidade: 1.0, densidade: 'poucas', imagem: 'cartaz' },
  { id: 'ranking', nome: 'Ranking ou lista', quando: 'Classificar itens: "3 erros", "4 documentos". O 1º lugar fica para o fim.', duracao: '40 a 75 s', ritmo: 'cortes por frase',
    estrutura: ['Barra de capítulos no alto', 'Número de cada item acima da cabeça', 'Do último para o primeiro', 'Chamada no fecho'],
    pecas: ['progresso', 'capitulo-alto', 'capitulo', 'contador', 'rotulos'], familia: 'editorial', legenda: 'acende', corte: 'respiro', velocidade: 1.1, densidade: 'medias', imagem: 'capitulo-alto' },
  { id: 'errado-certo', nome: 'Errado × certo', quando: 'Mostrar o jeito errado e o jeito certo de fazer algo.', duracao: '30 a 60 s', ritmo: 'cortes por frase',
    estrutura: ['O erro comum com tarja ou riscado', 'A cortina revela o certo', 'Mito e fato no ponto central'],
    pecas: ['antesdepois', 'riscado', 'mitofato', 'tarja', 'pb'], familia: 'editorial', legenda: 'destaque', corte: 'respiro', velocidade: 1.1, densidade: 'medias', imagem: 'mitofato' },
  { id: 'comparativo', nome: 'Comparativo', quando: 'Comparar dois institutos ou dois caminhos (cartório × Justiça).', duracao: '25 a 45 s', ritmo: 'sem cortes',
    estrutura: ['Fórmula com os requisitos', 'Barras com os números', 'Cartão com o @'],
    pecas: ['formula', 'barras', 'antesdepois', 'cartao', 'perfil'], familia: 'institucional', legenda: 'destaque', corte: 'pausas', velocidade: 1.0, densidade: 'medias', imagem: 'formula' },
  { id: 'documental', nome: 'Documental', quando: 'Contar a história de uma lei ou de um caso público, com tom de reportagem.', duracao: '45 a 90 s', ritmo: 'cortes por frase',
    estrutura: ['Tom de arquivo na cor', 'Foto que entra em foco com etiqueta e ano', 'Linha do tempo', 'Página oficial grifada', 'Holofote na frase principal'],
    pecas: ['foto', 'linhadotempo', 'faixa', 'citacao', 'holofote', 'janela'], familia: 'revista', legenda: 'discreta', cor: 'arquivo', corte: 'respiro', velocidade: 1.1, densidade: 'medias', imagem: 'cor-arquivo' },
  { id: 'opiniao', nome: 'Opinião e valores', quando: 'Um posicionamento seu, mais longo e calmo.', duracao: '60 a 120 s', ritmo: 'pausas mantidas, 1,0x',
    estrutura: ['Plano único, poucas peças', 'Citação na frase de apoio', 'Holofote na frase principal', 'Assinatura no fecho'],
    pecas: ['citacao', 'holofote', 'assinatura', 'carimbo'], familia: 'revista', legenda: 'discreta', corte: 'pausas', velocidade: 1.0, densidade: 'poucas', imagem: 'holofote' },
  { id: 'minimalista', nome: 'Minimalista premium', quando: 'Pouco na tela e tudo no lugar: autoridade com elegância.', duracao: '30 a 60 s', ritmo: 'cortes por frase, sem respiro',
    estrutura: ['Família Revista com moldura fina', 'Título fixo no alto', 'Legenda palavra por palavra', 'Cor de cinema leve'],
    pecas: ['fixo', 'citacao', 'assinatura'], familia: 'revista', legenda: 'palavra', cor: 'cinema', moldura: true, corte: 'seco', velocidade: 1.1, densidade: 'poucas', imagem: 'moldura' },
  { id: 'bastidor', nome: 'Bastidor do processo', quando: 'Mostrar como você trabalha (por exemplo, o vídeo editado pelo Claude).', duracao: '45 a 90 s', ritmo: 'cortes por frase',
    estrutura: ['Tela dividida: o cru e o editado', 'Edição acontecendo na tela', 'Comando digitado', 'Notebook com a tela real'],
    pecas: ['dividida', 'edicaoaovivo', 'comando', 'notebook', 'palavra'], familia: 'editorial', legenda: 'destaque', corte: 'respiro', velocidade: 1.1, densidade: 'cheia', imagem: 'edicaoaovivo' },
  // vídeo sem rosto: não parte de um vídeo cru; nasce de um roteiro de cenas (da Banca ou de um carrossel aprovado)
  { id: 'sem-rosto', nome: 'Explicação sem rosto', quando: 'Explicar uma regra só com texto, setas e animação, sem você na câmera. A sua voz em off é opcional.', duracao: '15 a 45 s', ritmo: 'tempo de leitura (sem voz) ou a sua fala (com voz)',
    estrutura: ['A dúvida do público', 'A regra, com a lei e a fonte', 'Como funciona, em até 3 passos', 'O cuidado ou o prazo', 'O fecho com o @'],
    pecas: ['busca', 'citacao', 'marcatexto', 'ligacao', 'trilha', 'calendario', 'mitofato', 'ponte', 'palavra', 'perfil'], familia: 'editorial', legenda: 'nenhuma', corte: 'pausas', velocidade: 1.0, densidade: 'cheia', imagem: 'sem-rosto',
    semRosto: true, voz: 'opcional' }
];
window.LEGENDAS = [
  { id: 'destaque', nome: 'Frase com destaque', uso: 'Padrão: a frase e a palavra-chave na cor de destaque.' },
  { id: 'discreta', nome: 'Discreta', uso: 'Opinião e temas sérios: sem cor, mais calma.' },
  { id: 'palavra-grande', nome: 'Palavra grande', uso: 'Mais energia: a palavra-chave cresce.' },
  { id: 'palavra', nome: 'Palavra por palavra', uso: 'Uma palavra por vez, na letra da família.' },
  { id: 'acende', nome: 'Palavra que acende', uso: 'A frase inteira, com a palavra dita acendendo.' },
  { id: 'nenhuma', nome: 'Sem legenda', uso: 'Quando a tela já conta tudo (cartaz).' }
];
window.CORES_VIDEO = [
  { id: 'natural', nome: 'Natural', uso: 'Como foi gravado (só a correção do iPhone).' },
  { id: 'cinema', nome: 'Cinema leve', uso: 'Pele suave, contraste, vinheta e grão discretos.' },
  { id: 'arquivo', nome: 'Tom de arquivo', uso: 'Dessaturado e quente: reportagem, história.' }
];
