import { deflateRawSync, inflateRawSync, crc32 } from 'node:zlib';

const HORA = 0;
const DIA = ((2026 - 1980) << 9) | (1 << 5) | 1; // 01/01/2026, para o zip sair sempre igual

export function criarZip(entradas) {
  const partes = [];
  const central = [];
  let offset = 0;
  for (const e of entradas) {
    const nome = Buffer.from(e.caminho, 'utf8');
    const comprimido = deflateRawSync(e.dados);
    const crc = crc32(e.dados);

    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6); // nomes em UTF-8
    local.writeUInt16LE(8, 8);
    local.writeUInt16LE(HORA, 10);
    local.writeUInt16LE(DIA, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(comprimido.length, 18);
    local.writeUInt32LE(e.dados.length, 22);
    local.writeUInt16LE(nome.length, 26);
    local.writeUInt16LE(0, 28);
    partes.push(local, nome, comprimido);

    const c = Buffer.alloc(46);
    c.writeUInt32LE(0x02014b50, 0);
    c.writeUInt16LE(0x031e, 4); // feito em Unix, versão 3.0: o modo vale
    c.writeUInt16LE(20, 6);
    c.writeUInt16LE(0x0800, 8);
    c.writeUInt16LE(8, 10);
    c.writeUInt16LE(HORA, 12);
    c.writeUInt16LE(DIA, 14);
    c.writeUInt32LE(crc, 16);
    c.writeUInt32LE(comprimido.length, 20);
    c.writeUInt32LE(e.dados.length, 24);
    c.writeUInt16LE(nome.length, 28);
    const modo = e.executavel ? 0o100755 : 0o100644;
    c.writeUInt32LE((modo << 16) >>> 0, 38);
    c.writeUInt32LE(offset, 42);
    central.push(c, nome);

    offset += 30 + nome.length + comprimido.length;
  }
  const diretorio = Buffer.concat(central);
  const fim = Buffer.alloc(22);
  fim.writeUInt32LE(0x06054b50, 0);
  fim.writeUInt16LE(entradas.length, 8);
  fim.writeUInt16LE(entradas.length, 10);
  fim.writeUInt32LE(diretorio.length, 12);
  fim.writeUInt32LE(offset, 16);
  return Buffer.concat([...partes, diretorio, fim]);
}

export function lerZip(zip) {
  const fim = zip.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
  const total = zip.readUInt16LE(fim + 10);
  let p = zip.readUInt32LE(fim + 16);
  const saida = [];
  for (let i = 0; i < total; i++) {
    const tamanho = zip.readUInt32LE(p + 20);
    const n = zip.readUInt16LE(p + 28);
    const extra = zip.readUInt16LE(p + 30);
    const comentario = zip.readUInt16LE(p + 32);
    const modo = zip.readUInt32LE(p + 38) >>> 16;
    const local = zip.readUInt32LE(p + 42);
    const caminho = zip.subarray(p + 46, p + 46 + n).toString('utf8');
    const inicio = local + 30 + zip.readUInt16LE(local + 26) + zip.readUInt16LE(local + 28);
    saida.push({ caminho, dados: inflateRawSync(zip.subarray(inicio, inicio + tamanho)), modo });
    p += 46 + n + extra + comentario;
  }
  return saida;
}
