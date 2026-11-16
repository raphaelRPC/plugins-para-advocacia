#!/bin/bash
# Instalador da Ilha de edição (Marketing Jurídico com Claude) para Mac.
# Não pede senha e não usa Homebrew: tudo fica em ~/.marketing-juridico/ferramentas, então o próprio Claude consegue rodar.
# Pode rodar de novo quando quiser: o que já está pronto é pulado, e ele continua de onde parou.
#
# Uso:  bash instalar-mac.sh               instala (20 a 40 minutos na primeira vez, conforme a internet)
#       bash instalar-mac.sh --diagnostico só confere o computador e diz o que falta, sem instalar nada
# Registro: ~/marketing-juridico-instalacao.log (termina com "PRONTO!" quando deu tudo certo)

set -u
FERR="${MJ_FERRAMENTAS:-$HOME/.marketing-juridico/ferramentas}"
LOG="${MJ_LOG:-$HOME/marketing-juridico-instalacao.log}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS="$(cd "$AQUI/../scripts" && pwd)"
NODE_VER="v22.14.0"
DIAG=0; [ "${1:-}" = "--diagnostico" ] && DIAG=1

diz() { echo "$*" | tee -a "$LOG"; }
falha() { diz "ERRO: $*"; diz "Veja este registro ($LOG), corrija só essa etapa e rode de novo: ele continua de onde parou."; exit 1; }
baixa() { curl -fL --retry 3 --retry-delay 3 --connect-timeout 20 -sS -o "$2" "$1"; }

[ $DIAG -eq 0 ] && echo "=== instalação $(date '+%d/%m/%Y %H:%M') ===" >> "$LOG"

# ---------- diagnóstico ----------
ARQ="$(uname -m)"; MAC="$(sw_vers -productVersion 2>/dev/null || echo '?')"
LIVRE_GB=$(df -g "$HOME" | awk 'NR==2{print $4}')
diz "Computador: macOS $MAC, chip $ARQ, $LIVRE_GB GB livres"
OK_MAC=1; [ "$(echo "$MAC" | cut -d. -f1)" -lt 12 ] 2>/dev/null && OK_MAC=0
[ $OK_MAC -eq 0 ] && diz "- macOS antigo: precisa do 12 (Monterey) ou mais novo"
[ "${LIVRE_GB:-0}" -lt 5 ] && diz "- pouco espaço: deixe pelo menos 5 GB livres"
curl -fsS --max-time 15 -o /dev/null https://nodejs.org && NET=1 || NET=0
[ $NET -eq 1 ] && diz "- internet: ok" || diz "- internet: sem acesso (precisa para baixar as ferramentas)"

NODE=""; if command -v node >/dev/null 2>&1 && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 18 ] 2>/dev/null; then NODE="$(command -v node)"; fi
[ -x "$FERR/node/bin/node" ] && NODE="$FERR/node/bin/node"
[ -n "$NODE" ] && diz "- Node: ok ($NODE)" || diz "- Node: falta (o instalador baixa uma cópia só para a edição)"
CHROME=""; [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] && CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -n "$CHROME" ] && diz "- Google Chrome: ok" || diz "- Google Chrome: não encontrado (o instalador baixa um navegador só para gravar as animações)"
if xcrun --find swiftc >/dev/null 2>&1; then SWIFT=1; diz "- Recorte da pessoa pelo macOS: ok"; else SWIFT=0; diz "- Recorte da pessoa pelo macOS: indisponível (usa o modelo aberto, que o instalador baixa)"; fi
[ -x "$FERR/node_modules/ffmpeg-static/ffmpeg" ] && diz "- Editor de vídeo (ffmpeg): ok" || diz "- Editor de vídeo (ffmpeg): falta"
[ -x "$FERR/venv/bin/python" ] && diz "- Transcrição e motor (Python): ok" || diz "- Transcrição e motor (Python): falta"
[ -f "$FERR/teste/teste-instalacao.mp4" ] && diz "- Vídeo de teste: já gerado antes"

if [ $DIAG -eq 1 ]; then
  if [ $OK_MAC -eq 1 ] && [ $NET -eq 1 ]; then diz "Compatível. Para instalar: bash \"$0\""; else diz "Ainda não compatível: resolva os itens acima."; fi
  exit 0
fi
[ $OK_MAC -eq 1 ] || falha "macOS 12 ou mais novo é necessário"
[ $NET -eq 1 ] || falha "sem internet"
mkdir -p "$FERR" "$FERR/modelos"

# ---------- 1. Node (só se o computador não tiver) ----------
if [ -z "$NODE" ]; then
  diz "1/6 Baixando o Node (motor das animações)..."
  [ "$ARQ" = "arm64" ] && N="node-$NODE_VER-darwin-arm64" || N="node-$NODE_VER-darwin-x64"
  baixa "https://nodejs.org/dist/$NODE_VER/$N.tar.gz" "$FERR/node.tgz" || falha "não consegui baixar o Node"
  rm -rf "$FERR/node" && mkdir -p "$FERR/node" && tar -xzf "$FERR/node.tgz" -C "$FERR/node" --strip-components 1 && rm "$FERR/node.tgz"
  NODE="$FERR/node/bin/node"
else diz "1/6 Node: já existe"; fi
NPM="$(dirname "$NODE")/npm"; export PATH="$(dirname "$NODE"):$PATH"

# ---------- 2. Editor de vídeo e gravador de animações ----------
if [ ! -x "$FERR/node_modules/ffmpeg-static/ffmpeg" ] || [ ! -d "$FERR/node_modules/puppeteer-core" ]; then
  diz "2/6 Instalando o editor de vídeo e o gravador de animações..."
  (cd "$FERR" && [ -f package.json ] || echo '{"name":"ferramentas-ilha-de-edicao","private":true}' > "$FERR/package.json")
  (cd "$FERR" && "$NPM" install --no-audit --no-fund --loglevel=error ffmpeg-static@5.2.0 puppeteer-core@25.13.0 three@0.186.1 >> "$LOG" 2>&1) || falha "npm install"
else diz "2/6 Editor de vídeo: já instalado"; fi
FF="$FERR/node_modules/ffmpeg-static/ffmpeg"

# ---------- 3. Navegador para gravar animações (só sem Chrome) ----------
if [ -z "$CHROME" ]; then
  CHROME="$(find "$FERR/navegador" -type f -name 'chrome-headless-shell' 2>/dev/null | head -1)"
  if [ -z "$CHROME" ]; then
    diz "3/6 Baixando um navegador só para gravar as animações..."
    (cd "$FERR" && "$(dirname "$NODE")/npx" --yes @puppeteer/browsers install chrome-headless-shell@stable --path "$FERR/navegador" >> "$LOG" 2>&1) || falha "navegador"
    CHROME="$(find "$FERR/navegador" -type f -name 'chrome-headless-shell' | head -1)"
  fi
else diz "3/6 Navegador: usa o Google Chrome"; fi

# ---------- 4. Python, transcrição e motor ----------
if [ ! -x "$FERR/venv/bin/python" ] || ! "$FERR/venv/bin/python" -c "import faster_whisper, PIL, numpy, onnxruntime" 2>/dev/null; then
  diz "4/6 Instalando o Python da edição e a transcrição (pode levar alguns minutos)..."
  if [ ! -x "$FERR/uv/uv" ]; then
    [ "$ARQ" = "arm64" ] && U="uv-aarch64-apple-darwin" || U="uv-x86_64-apple-darwin"
    baixa "https://github.com/astral-sh/uv/releases/latest/download/$U.tar.gz" "$FERR/uv.tgz" || falha "não consegui baixar o uv"
    mkdir -p "$FERR/uv" && tar -xzf "$FERR/uv.tgz" -C "$FERR/uv" --strip-components 1 && rm "$FERR/uv.tgz"
  fi
  export UV_PYTHON_INSTALL_DIR="$FERR/python"
  [ -x "$FERR/venv/bin/python" ] || "$FERR/uv/uv" venv --python 3.12 "$FERR/venv" >> "$LOG" 2>&1 || falha "criar o Python da edição"
  "$FERR/uv/uv" pip install --python "$FERR/venv/bin/python" faster-whisper==1.0.3 requests "huggingface_hub<2" numpy pillow onnxruntime >> "$LOG" 2>&1 || falha "pacotes do Python"
else diz "4/6 Python e transcrição: já instalados"; fi
PY="$FERR/venv/bin/python"

# ---------- 5. Modelos: transcrição (cerca de 1,5 GB) e recorte da pessoa (sem o do macOS) ----------
diz "5/6 Baixando o modelo de transcrição (na primeira vez são cerca de 1,5 GB)..."
"$PY" -W ignore -c "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu', compute_type='int8')" >> "$LOG" 2>&1 || falha "modelo de transcrição"
if [ $SWIFT -eq 0 ] && [ ! -f "$FERR/modelos/u2net_human_seg.onnx" ]; then
  diz "    Baixando o modelo de recorte da pessoa..."
  baixa "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx" "$FERR/modelos/u2net_human_seg.onnx" || falha "modelo de recorte"
fi

# ---------- caminhos para o Claude e o motor ----------
"$PY" - "$FERR" "$NODE" "$FF" "$PY" "$CHROME" "$SCRIPTS" <<'EOF'
import json, sys, os
ferr, node, ff, py, chrome, scripts = sys.argv[1:7]
json.dump({'ferramentas': ferr, 'node': node, 'ffmpeg': ff, 'python': py, 'node_path': os.path.join(ferr, 'node_modules'),
           'chrome': chrome or None, 'scripts': scripts, 'sistema': 'mac'}, open(os.path.join(ferr, 'caminhos.json'), 'w'), indent=1)
EOF

# ---------- 6. Teste: vídeo de 5 segundos ----------
diz "6/6 Gerando o vídeo de teste..."
MJ_FERRAMENTAS="$FERR" "$PY" -W ignore "$SCRIPTS/testar_instalacao.py" "$FERR" 2>&1 | tee -a "$LOG"
if [ -f "$FERR/teste/teste-instalacao.mp4" ] && grep -q "PRONTO!" <(tail -3 "$LOG"); then
  open -R "$FERR/teste/teste-instalacao.mp4" 2>/dev/null
  diz "PRONTO! A Ilha de edição está instalada. Peça ao Claude: \"edita esse vídeo\"."
else
  falha "o vídeo de teste não ficou pronto"
fi
