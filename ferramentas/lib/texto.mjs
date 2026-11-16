const NORMALIZAVEL = /\.(md|txt|json|py|sh|html|css|js|mjs|yml|yaml|svg)$/i;

export function ehTextoNormalizavel(caminho) {
  return NORMALIZAVEL.test(caminho);
}

export function paraLF(dados) {
  const saida = Buffer.alloc(dados.length);
  let j = 0;
  for (let i = 0; i < dados.length; i++) {
    if (dados[i] === 0x0d && dados[i + 1] === 0x0a) continue;
    saida[j++] = dados[i];
  }
  return saida.subarray(0, j);
}
