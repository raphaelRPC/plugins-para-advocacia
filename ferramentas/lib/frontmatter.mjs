export function lerFrontmatter(texto) {
  const linhas = texto.replace(/\r\n/g, '\n').split('\n');
  if (linhas[0].trim() !== '---') return null;
  const fim = linhas.findIndex((l, i) => i > 0 && l.trim() === '---');
  if (fim < 0) return null;
  const campos = {};
  let chave = null;
  for (const linha of linhas.slice(1, fim)) {
    const m = linha.match(/^([A-Za-z_-]+):\s*(.*)$/);
    if (m) {
      chave = m[1];
      const valor = m[2].trim();
      campos[chave] = /^[>|][-+]?$/.test(valor) ? '' : valor.replace(/^["']|["']$/g, '');
    } else if (chave && /^\s+\S/.test(linha)) {
      campos[chave] = `${campos[chave]} ${linha.trim()}`.trim();
    }
  }
  return campos;
}
