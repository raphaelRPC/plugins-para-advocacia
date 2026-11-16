# Fase 2 · I de Imagem

Objetivo: traduzir o posicionamento em sinais que o cliente vê antes de ler, para que vídeo e carrossel saiam com a identidade do advogado. Saídas: `base/imagem.md` (modelo em `assets/imagem.md`), `base/mapa-do-acervo.md` (modelo em `assets/mapa-do-acervo.md`) e fotos organizadas.

Imagem é a reprodução visual do posicionamento: cores, tipografia, fotos, ambiente. O critério é sempre o posicionamento, nunca o gosto do momento. A identidade é fixa; o layout de cada carrossel pode variar.

## Parte 0 · O nível do advogado

Descubra em que perfil ele está, por duas ou três perguntas ou pelo que o acervo mostra. O nível decide como a identidade começa, de onde vem o layout e quanto o plugin sugere. Registre em `base/imagem.md`, seção "Nível".

| Perfil | O que ele tem | Como começa a identidade | De onde vem o layout | Papel do plugin |
|---|---|---|---|---|
| Iniciante | nenhuma identidade, nenhuma referência | identidade mínima nesta fase: 2 cores e 2 fontes, a partir do posicionamento e da sensação que o perfil deve provocar | biblioteca do curso, filtrada pelo perfil | **sugere**: escolhe com ele por 3 ou 4 perguntas ou mostrando 3 opções |
| Intermediário | logo, cartão, cores, mas não sabe mexer no Canva | extraída do cartão ou do logo (foto do material) e montada como kit de marca no Canva | biblioteca do curso, com modelos que combinam com a identidade dele | **me mostra**: o foco é a consistência entre as artes |
| Avançado | estilo próprio, olho treinado, quer agilidade | já tem; o plugin só registra a pasta de referências dele | as referências e os modelos dele | **já sei**: segue com fidelidade; só intervém em OAB e nas proibições absolutas |
| Escritório com designer ou agência | manual de marca e modelos do designer | segue o manual à risca | os modelos do designer | só preenche e entrega o link editável para o designer ajustar |
| Escritório com vários advogados | uma marca, vários autores | a do escritório, igual para todos | modelos-mestres do escritório | troca as fotos e a assinatura de cada autor, com a OAB de quem assina a peça |
| Sem Canva ou no Canva gratuito | sem conta, sem conector ou sem kit de marca | registrada na base, aplicada pelo motor | os 6 estilos do catálogo do plugin | caminho B: motor próprio |
| Mudando de identidade | está trocando de marca | a nova, com a data da troca | o mesmo do nível dele | troca a identidade e marca a data, para o perfil não misturar as duas fases |

O nível pode subir com o tempo: o iniciante que aprova vários modelos passa a ter uma biblioteca pessoal e uma identidade mais definida.

## Parte A · Canva

No plugin de carrossel, o caminho principal da arte é o Canva: o Claude parte de um carrossel de referência, aplica a identidade e monta as lâminas (skill `arte-do-carrossel`). Para ligar: no aplicativo do Claude, Configurações, Conectores, procurar "Canva", conectar e fazer login; teste listando os kits de marca da conta.

- **Kit de marca:** é o que leva as fontes da marca para o Canva (o conector troca cores, textos e fotos, mas não troca fonte). Montar um kit com fontes próprias exige plano pago do Canva. Com kit, registre o nome dele na base.
- **Sem Canva, sem conector ou sem querer usar:** o carrossel sai pelo caminho B, o motor próprio do plugin, com a mesma identidade. Nada trava.

## Parte B · A identidade (um bloco numerado)

1. Você já tem identidade visual (manual, logo, cores definidas)? Se sim, mande o arquivo ou diga onde está; se tiver kit de marca no Canva, qual é.
2. Se não tem: quais sensações a sua marca precisa passar ao seu público (ex.: segurança, acolhimento, firmeza, proximidade)?
3. Mande 2 ou 3 referências visuais que você admira (Pinterest, Behance, revistas, marcas fora do direito). Perfis de colegas não servem como referência.
4. Como você se veste para atender e como é o seu ambiente de trabalho real?

Com isso, monte a **identidade fixa**, as constantes que fazem alguém reconhecer o perfil sem ler o nome, qualquer que seja o layout:

| # | Constante | O que fica igual | |
|---|---|---|---|
| 1 | Paleta | as cores da marca, cada uma no seu papel (fundo, texto, destaque, apoio), em código (ex.: #8E1B2B) | obrigatória |
| 2 | Par de fontes | uma para título, uma para texto (nomes do Google Fonts ou do kit de marca) | obrigatória |
| 3 | Recurso de ênfase | um só, sempre o mesmo (ex.: itálico na cor de destaque, ou marca-texto) | obrigatória |
| 4 | Tratamento de foto | a mesma cor, o mesmo contraste, o mesmo grão | obrigatória |
| 5 | Assinatura | posição do @, rodapé, formato da numeração e a lâmina final com nome e OAB no mesmo desenho | obrigatória |
| 6 | Elemento gráfico próprio | um fio, um selo ou uma forma que se repete e cria memória visual | opcional |

Proponha a paleta de 3 a 4 cores (60, 30 e 10: fundo, apoio, destaque), dizendo em uma linha por que cada cor conversa com o posicionamento, e o par de fontes (serifa tende a comunicar seriedade; sem serifa, proximidade). Sem identidade prévia, ofereça 3 combinações prontas e peça para escolher. Confira o contraste: texto de leitura a 4,5:1 sobre o fundo. Ajuste até o "aprovo" e registre na seção "Identidade fixa" de `base/imagem.md`.

## Parte C · As fotos e o Mapa do Acervo

1. Peça as fotos reais que ele tem (ensaio, celular, escritório, rotina) em `fotos/originais/`.
2. Leia o acervo pelas diretrizes de `references/diretrizes-de-foto.md`: tipo, função e os campos de leitura de cada foto (expressão, olhar, plano, orientação, rosto, área livre, ensaio). Copie as boas para `fotos/selecionadas/`, com nomes por função (`capa-01`, `retrato-01`, `ambiente-01`).
3. Escreva `base/mapa-do-acervo.md` no formato da seção 5 das diretrizes, com a lista "Não usar" (logo da OAB, terceiro identificável, documento legível) e as lacunas.
4. Se o ensaio é quase só retrato, oriente a cesta do próximo ensaio (40% retratos, 40% detalhe e ambiente, 20% bastidor).
5. Sem fotos: o carrossel sai em design flat (fundo da identidade e texto). Imagem gerada por IA é proibida, assim como cenário, escritório, livros ou rosto que não existem.

## Parte D · O que nunca aparece (OAB)

Registre no `base/imagem.md`:
- ostentação: carro, viagem, hotel, relógio ou bens em destaque (Prov. 205/2021, art. 6º, parágrafo único);
- logomarca ou símbolos oficiais da OAB (art. 5º, § 2º);
- prints de decisão, alvará ou valores (arts. 4º, § 2º, e 6º);
- em peça impulsionada, destaque para tamanho ou estrutura do escritório (art. 6º).

## Fechamento

1. Pergunte a preferência de layout e registre: **variar** (layout diferente a cada carrossel, sem repetir os dois últimos) ou **manter por série** (todo mito e fato num layout, todo checklist em outro). Ele muda quando quiser.
2. Se a skill `arte-do-carrossel` estiver disponível, gere uma capa de teste com uma frase do posicionamento, na identidade aprovada. Sem ela, a capa de teste fica para a chegada do plugin de carrossel.
3. Verifique que `base/imagem.md` e `base/mapa-do-acervo.md` existem e estão preenchidos. Marque a Fase 2 e siga: "A sua imagem está registrada. Agora a produção."
