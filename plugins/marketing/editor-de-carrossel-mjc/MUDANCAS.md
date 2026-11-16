# Mudanças · versão 1.1.0 (29/10/2026)

Reconfiguração do Plugin Editor de Carrossel - MJC (antes `carrossel-juridico-claude`) conforme a página "Carrossel Jurídico v2" e as decisões do Filipe depois dela (Árvore de Links no lugar do GitHub, Copywriter dentro do plugin, só o modo completo, skills primeiro). Uma linha por mudança, na ordem da tabela de correções da página.

## Feito nesta versão

1. Teste técnico do Canva: cópia, troca de texto e cores, exclusão de elementos, lâmina nova e reordenação testadas na conta do Filipe; cópia por link de modelo testada em outra conta (Daniel). Achados em `skills/arte-do-carrossel/references/canva.md`.
2. Nova ordem: a Banca escreve o texto inteiro e a estrutura em blocos; a arte só depois da Trava; o "aprovo" do carrossel passa para a prévia da arte. `banca-de-conteudo/SKILL.md`, `linha-editorial/SKILL.md`, `arte-do-carrossel/SKILL.md`.
3. Copywriter dentro do plugin: `orquestrador-copy`, `repertorio-textual`, `arquitetura-de-copy`, `gatilhos-mentais`, `polimento-textual`, `humanizar-texto`, `figuras-de-linguagem` copiadas do plugin Copywriter. Alterações nelas: uma nota "Neste plugin" no começo de cada uma (o autor é sempre advogado; ler `copy-juridica.md` antes) e as frases de exemplo que usavam travessão ou "não é X, é Y" reescritas.
4. Regras sem duplicar: `banca-de-conteudo/references/copy-juridica.md` (novo) diz quem cuida de quê, a tabela de gatilhos e OAB, as 3 capas, a estrutura em blocos e o convite por tipo; a lista de vícios saiu de `ganchos-e-linguagem.md` e foi para a `humanizar-texto`.
5. Canva como caminho principal da arte: escolha do modelo, cópia, identidade, montagem, prévia, lista de acabamento. `arte-do-carrossel/SKILL.md` reescrita; `references/canva.md` reescrita com o passo a passo técnico testado.
6. Biblioteca de modelos: Árvore de Links (https://claude.ai/artifact/Hjt9MKmnwZcu8Troy5SY53) como vitrine e `arte-do-carrossel/assets/catalogo.json` (novo, 61 modelos com links de modelo e descrições) para a escolha. Regras em `references/biblioteca.md` (novo). Substitui o repositório no GitHub previsto na página v2.
7. Identidade fixa com as 6 constantes, tradução por papel e exceção aprovada pelo advogado: `arte-do-carrossel/references/identidade.md` (novo); seção nova em `rito-pico/assets/imagem.md`.
8. Os 7 públicos e o papel do plugin em cada um: `arte-do-carrossel/references/publicos.md` (novo); nível definido na fase 2 do rito.
9. Skill nova `diagramacao`, com `sistema.md`, `principios.md`, `densidade.md`, `foto-e-texto.md`, `ritmo.md` e `teste.md`.
10. Texto fora do rosto, regra de onde o texto senta e leitura de cada foto: `diagramacao/references/foto-e-texto.md` e Mapa do Acervo em `rito-pico/references/fase-2-imagem.md`.
11. Título só por degraus da escala e "se não cabe, muda a estrutura": `diagramacao/references/sistema.md` e `densidade.md`.
12. Preferência de variar ou manter o layout: perguntada na fase 2, guardada na base, usada na escolha do modelo.
13. Capa com 3 opções e os critérios do gancho marcados: `banca-de-conteudo/SKILL.md` e `copy-juridica.md`.
14. Máximo de 3 tipos de lâmina no miolo: `diagramacao/references/ritmo.md`.
15. Mapa do Acervo com os campos novos e a cesta de fotos: `rito-pico/references/fase-2-imagem.md` e `assets/imagem.md`.
16. Exceção do C04 à regra de "metade com foto": `arte-do-carrossel/references/catalogo-de-estilos.md`.
17. Legenda e texto alternativo: a Banca gera junto com o texto; a arte entrega com as imagens.
18. C06 Pasta: título da capa sem justificação. `assets/estilos/C06-pasta/estilo.css`.
19. Mito riscado só em frase curta e de peso leve; foto deitada só em cartão, moldura ou metade: regras na diagramação.
20. Convite pelo tipo de carrossel, sem repetir o anterior: `copy-juridica.md`, seção 6.
21. Conferência com a capa e as lâminas com foto em tamanho real, mais a conferência de identidade e de restos do modelo: `diagramacao/references/teste.md`.
22. Número da lâmina na prancha do motor passa para fora da lâmina (não cobre mais o @). `scripts/montar_carrossel.py`.
23. Sem foto, design flat; caminho de imagem composta removido: `sem-cara-de-ia.md`, `diagramacao`, `rito-pico`.
24. Verificador: travessão e "não é X, é Y" seguem CORRIGIR no texto do plugin; com `--autor advogado`, viram CONFERIR (o plugin avisa e respeita). `scripts/verificar_texto.py`.
25. Rito PICO: fase 2 reescrita (Canva, nível, identidade fixa, Mapa do Acervo, escolha de modelos na Árvore); tabela de skills atualizada no `rito-pico/SKILL.md`.
26. README e `plugin.json` (versão 1.1.0) atualizados.
27. Revisão de coerência: números iguais em todas as skills (capa até 20 palavras com o subtítulo, títulos só em degraus, lista com até 5 itens e 25 palavras, ênfase no máximo duas); Canva gratuito segue o caminho principal; mapa dos filtros da biblioteca (tom, 7 públicos, tipos da Banca); aviso de nunca copiar pelo `design_id`; conferência no Canva pela miniatura e pelo conteúdo da página.
28. Uso do plano: `uso-do-plano/scripts/uso.py` passa a contar a arte do carrossel, a diagramação e as skills do Copywriter, e aceita os dois nomes de plugin.

## Fica para a próxima versão (caminho B, motor próprio)

- Escala 1,5, régua de 8, margem 104 e corpo 40 (mínimo 36) no CSS dos 6 estilos.
- Variantes de densidade (curta, média, longa) e layout de lâmina sem título em cada estilo.
- Campos `faixa` e `posicao_texto` no motor; título só por degraus no ajuste automático.
- Limites de palavras lidos do `estilo.json` no verificador.
- Mito riscado no CSS do C02 e do C05.
- Recorte e zoom de print; arquivo de texto alternativo junto dos PNG.
- Campos novos do Mapa do Acervo na folha do `ver_fotos.py`.
- Exemplos realistas em `assets/exemplos/`, separados do exemplo do catálogo.

## A testar

- Duplicar uma lâmina do próprio modelo pelo conector (copiar a página e juntar ao design), no lugar de criar do zero.
- Troca de foto num modelo que tenha foto.
- Fluxo completo com a marca e as fotos de outro advogado, de preferência um de cada nível.
