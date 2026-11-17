// Monta, a partir da fonte, os repositórios de entrega de cada ticket (tickets.json).
// Cada entrega leva só os plugins do seu ticket, cortados na edição certa, com
// marketplace, README, CHANGELOG e guias próprios. Nada da equipe vai junto.
import { readFileSync, writeFileSync, mkdirSync, rmSync, copyFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { listarArquivos } from './arquivos.mjs';
import { ehTextoNormalizavel, paraLF } from './texto.mjs';
import { lerCatalogo } from './catalogo.mjs';
import { lerEdicoes, habilidadesDaEdicao, arquivosDaEdicao } from './edicoes.mjs';
import { criarZip } from './zip.mjs';
import { conferirSaida, zipDoPlugin } from './montagem.mjs';
import { regraCatalogo, regraHabilidades, regraReferencias, regraTexto, regraFimDeLinha } from './regras.mjs';
import { regraReadme } from './readme.mjs';

const ROTULOS = { fundacao: 'Fundação', motores: 'Motores do escritório', marketing: 'Marketing jurídico' };
const REPOSITORIO_FONTE = 'plugins-para-advocacia';
const FALLBACK = /se instalad|se existir|se houver/i;

export function lerTickets(raiz) {
  return JSON.parse(readFileSync(join(raiz, 'tickets.json'), 'utf8'));
}

function habilidadesDe(arquivos) {
  return [...new Set(arquivos.filter(r => /^skills\/[^/]+\/SKILL\.md$/.test(r)).map(r => r.split('/')[1]))];
}

export function selecionar(raiz, nomeTicket) {
  const config = lerTickets(raiz);
  const ticket = config.tickets[nomeTicket];
  if (!ticket) throw new Error(`ticket desconhecido: ${nomeTicket} (existem: ${Object.keys(config.tickets).join(', ')})`);
  const edicoes = lerEdicoes(raiz);
  const { dados, plugins } = lerCatalogo(raiz);
  const escolhidos = Object.entries(ticket.plugins).map(([nome, edicao]) => {
    const p = plugins.find(x => x.nome === nome);
    if (!p) throw new Error(`${nomeTicket}: o plugin "${nome}" não está no catálogo`);
    if (!config.plugins[nome]) throw new Error(`tickets.json: falta a descrição de "${nome}" em "plugins"`);
    const temEdicoes = Boolean(edicoes.plugins[nome]);
    if (edicao && !temEdicoes) throw new Error(`${nomeTicket}: "${nome}" não tem edições; use null`);
    if (!edicao && temEdicoes) throw new Error(`${nomeTicket}: "${nome}" tem edições; diga qual (${edicoes.edicoes.join(', ')})`);
    const permitidas = edicao ? habilidadesDaEdicao(edicoes, nome, edicao) : null;
    const arquivos = arquivosDaEdicao(listarArquivos(p.dir), permitidas);
    return { ...p, edicao, arquivos, habilidades: habilidadesDe(arquivos) };
  });
  escolhidos.sort((a, b) => plugins.findIndex(x => x.nome === a.nome) - plugins.findIndex(x => x.nome === b.nome));
  const total = escolhidos.reduce((s, p) => s + p.habilidades.length, 0);
  return { nome: nomeTicket, config, ticket, dados, escolhidos, todos: plugins, total };
}

// ---------- textos gerados ----------

export function processarGuia(texto, ctx) {
  let t = texto.replace(/<!-- so-fonte:inicio -->[\s\S]*?<!-- so-fonte:fim -->\n?/g, '');
  t = t.replace(/<!-- grupos:inicio -->[\s\S]*?<!-- grupos:fim -->\n?/g, ctx.grupos);
  t = t.split(`raphaelRPC/${REPOSITORIO_FONTE}`).join(`${ctx.dono}/${ctx.repositorio}`);
  t = t.split(REPOSITORIO_FONTE).join(ctx.repositorio);
  t = t.split('motor-comercial').join(ctx.exemplo);
  return t.replace(/\n{3,}/g, '\n\n');
}

function textoDosGrupos(sel) {
  const linhas = ['## Os plugins deste pacote', ''];
  for (const p of sel.escolhidos) linhas.push(`- **${ROTULOS[p.grupo]}:** \`${p.nome}\`. ${sel.config.plugins[p.nome].quer}.`);
  return linhas.join('\n') + '\n';
}

export function filtrarChangelog(texto, presentes) {
  const saida = ['# Mudanças', '', 'Cada versão lista o que mudou em cada plugin deste repositório.', ''];
  let secao = null;
  let itens = [];
  const fechar = () => { if (secao && itens.length) saida.push(secao, '', ...itens, ''); };
  for (const linha of texto.split('\n')) {
    if (linha.startsWith('## [')) { fechar(); secao = linha; itens = []; continue; }
    const citados = [...linha.matchAll(/`([a-z0-9-]+)`/g)].map(m => m[1]);
    if (secao && /^- `/.test(linha) && citados.length && citados.every(c => presentes.includes(c))) itens.push(linha);
  }
  fechar();
  return saida.join('\n').replace(/\n+$/, '\n');
}

function diagramaDosMotores(nomes) {
  const tem = n => nomes.includes(n);
  const nos = {
    'inicio-automacao': 'F[inicio-automacao<br/>cultura, setores, POPs]',
    'motor-comercial': 'C[motor-comercial<br/>do contato ao contrato]',
    'motor-experiencia': 'E[motor-experiencia<br/>do contrato ao encerramento]',
    'motor-juridico': 'J[motor-juridico<br/>peças e protocolo]',
    'motor-controladoria': 'K[motor-controladoria<br/>publicações e prazos]',
  };
  const id = n => nos[n].split('[')[0];
  const linhas = ['```mermaid', 'flowchart LR', '    P[(pasta escritorio/)]'];
  for (const n of Object.keys(nos)) if (tem(n)) linhas.push(`    ${nos[n]}`);
  if (tem('inicio-automacao')) linhas.push('    F --> P');
  if (tem('motor-comercial') && tem('motor-experiencia')) linhas.push('    C -->|passagem-para-o-caso| E');
  if (tem('motor-controladoria') && tem('motor-juridico')) linhas.push('    K -->|providência| J');
  if (tem('motor-controladoria') && tem('motor-experiencia')) linhas.push('    K -->|aviso ao cliente| E');
  for (const n of ['motor-comercial', 'motor-experiencia', 'motor-juridico', 'motor-controladoria']) if (tem(n)) linhas.push(`    ${id(n)} --- P`);
  linhas.push('```');
  return linhas.join('\n');
}

function secaoDosMotores(sel) {
  const motores = sel.escolhidos.filter(p => p.grupo === 'motores');
  if (!motores.length) return '';
  const titulo = motores.length > 1 ? 'Como os motores trabalham juntos' : 'Como o motor trabalha';
  const linhas = ['', `## ${titulo}`, '', diagramaDosMotores(sel.escolhidos.map(p => p.nome)), ''];
  if (motores.length > 1) linhas.push('- Os motores leem e gravam na **mesma pasta `escritorio/`** e usam o **mesmo código de cliente**: um enxerga o que o outro produziu.');
  linhas.push(
    `- ${motores.length > 1 ? 'Cada motor tem' : 'O motor tem'} cinco comandos: \`comecar\` (liga o setor com até 8 perguntas), \`ficha\` (completa o contexto), \`ciclo\` (roda o dia), \`fila\` (mostra o que espera aprovação) e \`status\`.`,
    '- Um **agente** roda o ciclo do dia e deixa tudo numa **fila de aprovação**. Um **revisor** confere cada rascunho contra as regras de ética e as fichas antes de ele entrar na fila.',
    '- Tudo o que é feito com casos fictícios fica em `escritorio/07-operacao/_treino/`, longe dos registros reais.',
    '',
  );
  return linhas.join('\n');
}

export function gerarReadme(modelo, sel, versao) {
  const { config, ticket, escolhidos, total } = sel;
  const escolha = escolhidos.map(p => `| ${config.plugins[p.nome].quer} | \`${p.nome}\` | ${config.plugins[p.nome].comecar} |`).join('\n');
  const linhasPlugins = [];
  let grupoAtual = null;
  for (const p of escolhidos) {
    if (p.grupo !== grupoAtual) { linhasPlugins.push(`| **${ROTULOS[p.grupo]}** | | |`); grupoAtual = p.grupo; }
    linhasPlugins.push(`| [\`${p.nome}\`](plugins/${p.grupo}/${p.nome}) | ${p.versao} | ${p.habilidades.length} |`);
  }
  const temInicio = escolhidos.some(p => p.nome === 'inicio-automacao');
  const temMotor = escolhidos.some(p => p.grupo === 'motores');
  const ordem = temInicio && temMotor
    ? '`inicio-automacao` primeiro, depois o motor do setor que mais dói hoje, depois os outros.'
    : 'comece pelo plugin do que mais toma tempo hoje.';
  const valores = {
    RESUMO: `${escolhidos.length} plugins · ${total} habilidades · versão do pacote **${versao}**`,
    DONO: config.dono,
    REPOSITORIO: ticket.repositorio,
    EXEMPLO: ticket.exemplo,
    TABELA_ESCOLHA: escolha,
    ORDEM: ordem,
    TABELA_PLUGINS: linhasPlugins.join('\n'),
    MOTORES: secaoDosMotores(sel),
  };
  return modelo.replace(/\{\{([A-Z_]+)\}\}/g, (m, chave) => {
    if (!(chave in valores)) throw new Error(`modelo do README: marcador desconhecido {{${chave}}}`);
    return valores[chave];
  });
}

// ---------- montagem ----------

function gravar(destino, rel, dados) {
  const alvo = join(destino, rel);
  mkdirSync(dirname(alvo), { recursive: true });
  writeFileSync(alvo, ehTextoNormalizavel(rel) ? paraLF(dados) : dados);
}

export function montarEntrega(raiz, sel, versao, destino) {
  const { config, ticket, dados, escolhidos } = sel;
  mkdirSync(destino, { recursive: true });
  for (const p of escolhidos) {
    const base = p.source.replace(/^\.\//, '');
    for (const rel of p.arquivos) gravar(destino, `${base}/${rel}`, readFileSync(join(p.dir, rel)));
  }
  const nomes = escolhidos.map(p => p.nome);
  const catalogo = {
    ...dados,
    name: ticket.repositorio,
    metadata: { ...dados.metadata, version: versao, description: `Plugins do Claude para escritórios de advocacia: ${nomes.join(', ')}.` },
    plugins: dados.plugins.filter(e => nomes.includes(e.name)),
  };
  gravar(destino, '.claude-plugin/marketplace.json', Buffer.from(JSON.stringify(catalogo, null, 2) + '\n'));
  const modelo = readFileSync(join(raiz, 'modelos', 'README-entrega.md'), 'utf8');
  gravar(destino, 'README.md', Buffer.from(gerarReadme(modelo, sel, versao)));
  gravar(destino, 'CHANGELOG.md', Buffer.from(filtrarChangelog(readFileSync(join(raiz, 'CHANGELOG.md'), 'utf8'), nomes)));
  const ctx = { dono: config.dono, repositorio: ticket.repositorio, exemplo: ticket.exemplo, grupos: textoDosGrupos(sel) };
  for (const rel of listarArquivos(join(raiz, 'guia')).filter(r => !r.startsWith('equipe/'))) {
    const texto = readFileSync(join(raiz, 'guia', rel), 'utf8');
    gravar(destino, `guia/${rel}`, Buffer.from(rel.endsWith('.md') ? processarGuia(texto, ctx) : texto));
  }
  copyFileSync(join(raiz, '.gitattributes'), join(destino, '.gitattributes'));
}

// ---------- conferências ----------

export function conferirVazamento(destino, sel) {
  const permitidos = sel.escolhidos.map(p => `plugins/${p.grupo}/${p.nome}/`);
  const fixos = new Set(['.claude-plugin/marketplace.json', 'README.md', 'CHANGELOG.md', '.gitattributes']);
  return listarArquivos(destino)
    .filter(rel => !(fixos.has(rel) || (rel.startsWith('guia/') && !rel.startsWith('guia/equipe/')) || permitidos.some(p => rel.startsWith(p))))
    .map(rel => `${sel.nome}: ${rel} não pertence a esta entrega`);
}

export function conferirComandosAusentes(destino, sel) {
  const ausentes = sel.todos.map(p => p.nome).filter(n => !sel.escolhidos.some(p => p.nome === n));
  const erros = [];
  for (const p of sel.escolhidos) {
    const base = join(destino, 'plugins', p.grupo, p.nome);
    for (const rel of listarArquivos(base).filter(r => r.endsWith('.md'))) {
      readFileSync(join(base, rel), 'utf8').split('\n').forEach((linha, i) => {
        // Linha de tabela é referência (lista dos motores), não instrução de rodar.
        if (FALLBACK.test(linha) || linha.trimStart().startsWith('|')) return;
        for (const a of ausentes) {
          if (linha.includes(`/${a}:`)) erros.push(`${sel.nome}: ${p.nome}/${rel}:${i + 1} manda rodar um comando de ${a}, que não está nesta entrega (use "se instalado" na mesma linha)`);
        }
      });
    }
  }
  return erros;
}

export function conferirEntrega(destino, sel) {
  const erros = [];
  if (sel.total < sel.ticket.promessa) erros.push(`${sel.nome}: ${sel.total} habilidades, abaixo da promessa de ${sel.ticket.promessa}`);
  erros.push(...conferirVazamento(destino, sel));
  erros.push(...regraCatalogo(destino).map(e => `${sel.nome}: ${e}`));
  for (const p of lerCatalogo(destino).plugins.filter(x => existsSync(x.dir))) {
    erros.push(...[...regraHabilidades(p), ...regraReferencias(p), ...regraTexto(p), ...regraFimDeLinha(p)].map(e => `${sel.nome}: ${e}`));
  }
  erros.push(...regraReadme(destino).map(e => `${sel.nome}: ${e}`));
  erros.push(...conferirComandosAusentes(destino, sel));
  for (const rel of listarArquivos(destino).filter(r => /\.(md|json)$/.test(r) && !r.startsWith('plugins/'))) {
    const texto = readFileSync(join(destino, rel), 'utf8');
    if (texto.includes(REPOSITORIO_FONTE)) erros.push(`${sel.nome}: ${rel} cita o repositório da equipe (${REPOSITORIO_FONTE})`);
    if (/<!-- (so-fonte|grupos):/.test(texto)) erros.push(`${sel.nome}: ${rel} ficou com marcador de montagem`);
  }
  return erros;
}

// Citações por nome a habilidades que não vieram nesta entrega: não quebram nada
// (o texto já prevê a ausência na maior parte), mas a equipe deve conferir.
export function relatorioDeReferencias(destino, sel) {
  const presentes = new Set(sel.escolhidos.flatMap(p => p.habilidades));
  const ausentes = [...new Set(sel.todos.flatMap(p => habilidadesDe(listarArquivos(p.dir))))]
    .filter(h => !presentes.has(h) && h.includes('-'));
  const achados = [];
  for (const p of sel.escolhidos) {
    const base = join(destino, 'plugins', p.grupo, p.nome);
    for (const rel of listarArquivos(base).filter(r => /\.(md|py|json)$/.test(r) && r !== 'README.md')) {
      readFileSync(join(base, rel), 'utf8').split('\n').forEach((linha, i) => {
        if (FALLBACK.test(linha)) return;
        const citadas = ausentes.filter(h => new RegExp(`(^|[^a-z0-9-])${h}([^a-z0-9-]|$)`).test(linha));
        if (citadas.length) achados.push(`| ${p.nome}/${rel}:${i + 1} | ${citadas.map(c => `\`${c}\``).join(', ')} |`);
      });
    }
  }
  return [
    `# Citações a habilidades que não vieram no ${sel.nome}`,
    '',
    'Não bloqueiam a publicação. Confira se o texto já diz o que fazer quando a habilidade não existe.',
    '',
    `Total: ${achados.length}`,
    '',
    '| Onde | Habilidade citada |',
    '|---|---|',
    ...achados,
    '',
  ].join('\n');
}

export function montarTodas(raiz, versao, saidaPedida, apenas) {
  const saida = conferirSaida(raiz, saidaPedida);
  const nomes = apenas ? [apenas] : Object.keys(lerTickets(raiz).tickets);
  const selecoes = nomes.map(n => selecionar(raiz, n));
  rmSync(saida, { recursive: true, force: true });
  mkdirSync(saida, { recursive: true });
  const resultado = [];
  const somas = [];
  for (const sel of selecoes) {
    const pasta = join(saida, sel.nome);
    const destino = join(pasta, 'repositorio');
    montarEntrega(raiz, sel, versao, destino);
    const erros = conferirEntrega(destino, sel);
    writeFileSync(join(pasta, 'relatorio-de-referencias.md'), relatorioDeReferencias(destino, sel));
    const zips = join(pasta, 'zips');
    mkdirSync(join(zips, 'plugins'), { recursive: true });
    const internos = [];
    for (const p of lerCatalogo(destino).plugins) {
      const rel = `plugins/${p.nome}-${p.versao}.zip`;
      writeFileSync(join(zips, rel), zipDoPlugin(p, null));
      internos.push(rel);
    }
    const pacote = `${sel.ticket.repositorio}-v${versao}.zip`;
    writeFileSync(join(zips, pacote), criarZip([
      { caminho: 'LEIA-ME.md', dados: readFileSync(join(destino, 'guia', 'comece-aqui.md')) },
      ...internos.map(rel => ({ caminho: rel, dados: readFileSync(join(zips, rel)) })),
    ]));
    for (const rel of [pacote, ...internos]) {
      somas.push(`${createHash('sha256').update(readFileSync(join(zips, rel))).digest('hex')}  ${sel.nome}/zips/${rel}`);
    }
    resultado.push({ ticket: sel.nome, repositorio: sel.ticket.repositorio, plugins: sel.escolhidos.length, habilidades: sel.total, promessa: sel.ticket.promessa, erros });
  }
  writeFileSync(join(saida, 'SHA256SUMS.txt'), somas.join('\n') + '\n');
  return resultado;
}

// Para o npm run checar: tickets.json coerente com o catálogo e com as promessas.
export function regraTickets(raiz) {
  if (!existsSync(join(raiz, 'tickets.json'))) return [];
  const erros = [];
  for (const nome of Object.keys(lerTickets(raiz).tickets)) {
    try {
      const sel = selecionar(raiz, nome);
      if (sel.total < sel.ticket.promessa) erros.push(`tickets.json: ${nome} tem ${sel.total} habilidades, abaixo da promessa de ${sel.ticket.promessa}`);
      if (!sel.escolhidos.some(p => p.nome === sel.ticket.exemplo)) erros.push(`tickets.json: o exemplo de ${nome} (${sel.ticket.exemplo}) não está no ticket`);
    } catch (e) {
      erros.push(`tickets.json: ${e.message}`);
    }
  }
  return erros;
}
