// Instala cada entrega montada numa configuração do Claude Code isolada (pasta temporária),
// como um participante faria, e confere se todos os plugins entram ativados.
// Uso: node ferramentas/testar_entregas.mjs [--saida entregas-geradas]
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, readdirSync, existsSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const args = process.argv.slice(2);
const i = args.indexOf('--saida');
const saida = resolve(i >= 0 ? args[i + 1] : join(import.meta.dirname, '..', 'entregas-geradas'));
if (!existsSync(saida)) { console.error(`ERRO: ${saida} não existe; rode antes npm run entregas`); process.exit(1); }

try { execFileSync('claude', ['--version'], { stdio: 'pipe' }); }
catch { console.log('Claude Code não encontrado: teste de instalação pulado.'); process.exit(0); }

let falhas = 0;
for (const ticket of readdirSync(saida).filter(n => existsSync(join(saida, n, 'repositorio')))) {
  const repo = join(saida, ticket, 'repositorio');
  const catalogo = JSON.parse(readFileSync(join(repo, '.claude-plugin', 'marketplace.json'), 'utf8'));
  const config = mkdtempSync(join(tmpdir(), `claude-${ticket}-`));
  const rodar = (...a) => execFileSync('claude', a, { encoding: 'utf8', stdio: 'pipe', env: { ...process.env, CLAUDE_CONFIG_DIR: config } });
  try {
    rodar('plugin', 'validate', repo);
    rodar('plugin', 'marketplace', 'add', repo);
    for (const p of catalogo.plugins) rodar('plugin', 'install', `${p.name}@${catalogo.name}`);
    const lista = rodar('plugin', 'list');
    const faltando = catalogo.plugins.filter(p => !lista.includes(`${p.name}@${catalogo.name}`));
    if (faltando.length) throw new Error(`não apareceram instalados: ${faltando.map(p => p.name).join(', ')}`);
    console.log(`${ticket}: ${catalogo.plugins.length} plugins instalados e ativados a partir de ${catalogo.name}`);
  } catch (e) {
    falhas++;
    console.error(`ERRO ${ticket}: ${(e.stderr || e.stdout || e.message).toString().trim().split('\n').slice(-3).join(' | ')}`);
  } finally {
    rmSync(config, { recursive: true, force: true });
  }
}
if (falhas) process.exit(1);
