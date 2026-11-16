# Canva pelo conector: o passo a passo técnico

Testado em outubro de 2026 com o modelo Clássico de serifa em verde e o texto de pensão: cópia, troca de texto, troca de cores, exclusão de elementos, lâmina nova e reordenação funcionaram. A cópia a partir de um link de modelo, numa conta de outra pessoa, também funcionou.

## 1. Conector

Confira se as ferramentas do Canva estão disponíveis na sessão. Se não estiverem, diga em uma frase como conectar (Configurações, Conectores, procurar "Canva", conectar e fazer login). Sem conector, vá para o caminho B.

## 2. Copiar o modelo

1. Link curto (`canva.link/...`): resolva o endereço com a ferramenta de resolver link curto.
2. Faça a cópia na conta do advogado a partir do endereço que o link de modelo resolveu (ferramenta de copiar design). Nunca use o `design_id` do catálogo: ele é o original da biblioteca. Dê à cópia o nome do tema ("Carrossel · pensão · 2026-10").
3. Se não der para copiar pelo conector: peça ao advogado para abrir o link e clicar em "Usar modelo"; depois encontre a cópia na conta dele (busca de designs pelo nome) e siga.
4. Nunca abra edição no design original.

## 3. Ler e editar

1. Abra a edição da cópia lendo o design com transação aberta e o conteúdo das páginas: você recebe cada elemento com posição, tamanho, cor, fonte e um identificador.
2. Edite página por página. Depois de cada página, olhe a miniatura que volta e confira o documento antes de seguir.

| O que fazer | Como | Limite |
|---|---|---|
| Trocar texto | substituir o texto do elemento | o Canva reacomoda o texto mais longo no mesmo centro; confira se não colou no elemento de baixo |
| Mudar cor, tamanho, peso, itálico, alinhamento | formatar o texto | **a família da fonte não muda** pelo conector: vai para a lista de acabamento |
| Mudar a cor de fundo da página | inserir um retângulo do tamanho da lâmina (1080 x 1350) com a cor da marca e mandar para trás | não esqueça de mandar para trás, senão ele cobre tudo |
| Mudar a cor de fios e linhas | atualizar a cor do traço | fios **não mudam de lugar nem de tamanho**: se atrapalham, apague ou registre no acabamento |
| Tirar nome de exemplo, ícone, logo | excluir o elemento | confira se não era o único enfeite que dava equilíbrio à lâmina |
| Mover e redimensionar texto | posicionar e redimensionar o elemento | para texto, informe só a largura |
| Trocar foto | enviar a foto do advogado (pedir endereço de envio, mandar os bytes do arquivo num POST com `Content-Type: application/octet-stream`, guardar o identificador) e preencher o espaço de foto do modelo (ainda não testado num modelo com foto) | um endereço de envio por foto; endereço usado ou vencido não se reutiliza |
| Lâmina a mais | primeiro tente duplicar uma lâmina parecida do próprio modelo (copiar só aquela página e juntar ao design; ainda não testado); se não der, adicione página com a cor de fundo e monte o texto | lâmina criada do zero sai com a fonte padrão e sem as setas dos fios: vai para a lista de acabamento |
| Ordem das lâminas | reordenar a página antes ou depois de outra | o fecho fica sempre por último |

## 4. Prévia, "aprovo" e salvar

1. Mostre a miniatura de todas as páginas.
2. Ajuste o que o advogado pedir, lâmina a lâmina.
3. **Só salve (commit) depois do "aprovo".** Edição salva não se desfaz. Se ele desistir, descarte a edição.

## 5. Exportar

Confira os formatos disponíveis e exporte em PNG, uma imagem por página (sem juntar as páginas). Entregue as imagens, o link editável, a legenda, o texto alternativo e a lista de acabamento.

## Conferir antes de mostrar

- Texto igual ao aprovado, acentos certos, nenhum travessão.
- Nenhum resto do modelo (nome de exemplo, @, site, ícone de outra profissão, texto em inglês).
- Cores só da paleta; título sem estourar a área; texto fora do rosto.
- Identificação (nome e OAB/UF) no fecho.
- Nada da lista "O que nunca aparece" e nada da tabela 2 de `../../banca-de-conteudo/references/sem-cara-de-ia.md`.
