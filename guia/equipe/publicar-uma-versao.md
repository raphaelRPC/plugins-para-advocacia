# Publicar uma versão

1. Para cada plugin que mudou: `node ferramentas/versao.mjs subir <plugin> <patch|minor|major> "<o que mudou>"`.
2. `npm run testar` e `npm run checar`: tudo tem que passar.
3. `node ferramentas/versao.mjs fechar X.Y.Z`.
4. Commit, depois `git tag vX.Y.Z` e `git push origin main vX.Y.Z`.
5. Em uns minutos aparece em Releases um **rascunho** com os zips. Abra, confira as notas e clique em **Publish release**.

Sem GitHub Actions (por exemplo, sem minutos no plano). Rode antes `npm run testar` e `npm run checar`. Depois, na raiz do repositório:

```
npm run zips -- --versao X.Y.Z
node ferramentas/versao.mjs notas X.Y.Z > notas.md
gh release create vX.Y.Z dist/*.zip dist/plugins/*.zip dist/SHA256SUMS.txt --draft --notes-file notas.md
```

## Compartilhar enquanto o repositório é privado

- **Com quem tem acesso ao repositório:** mande o link do release.
- **Com quem não tem:** baixe o zip do pacote no release e mande pelo Hub ou pelo Drive.
- O release nunca fica público enquanto o repositório for privado.
