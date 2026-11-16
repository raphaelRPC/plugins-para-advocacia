# Instalador da Ilha de edição (Marketing Jurídico com Claude) para Windows 10 e 11.
# Não pede senha de administrador: tudo fica em %USERPROFILE%\.marketing-juridico\ferramentas, então o próprio Claude consegue rodar.
# Pode rodar de novo quando quiser: o que já está pronto é pulado, e ele continua de onde parou.
#
# Uso:  powershell -ExecutionPolicy Bypass -File instalar-windows.ps1               instala (20 a 40 minutos na primeira vez)
#       powershell -ExecutionPolicy Bypass -File instalar-windows.ps1 -Diagnostico  só confere o computador e diz o que falta
# Registro: %USERPROFILE%\marketing-juridico-instalacao.log (termina com "PRONTO!" quando deu tudo certo)

param([switch]$Diagnostico)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$FERR = if ($env:MJ_FERRAMENTAS) { $env:MJ_FERRAMENTAS } else { Join-Path $env:USERPROFILE '.marketing-juridico\ferramentas' }
$LOG = if ($env:MJ_LOG) { $env:MJ_LOG } else { Join-Path $env:USERPROFILE 'marketing-juridico-instalacao.log' }
$SCRIPTS = (Resolve-Path (Join-Path $PSScriptRoot '..\scripts')).Path
$NODE_VER = 'v22.14.0'

function Diz($t) { Write-Host $t; Add-Content -Path $LOG -Value $t -Encoding UTF8 }
function Falha($t) { Diz "ERRO: $t"; Diz "Veja este registro ($LOG), corrija só essa etapa e rode de novo: ele continua de onde parou."; exit 1 }
function Baixa($url, $dest) {
  for ($i = 1; $i -le 3; $i++) {
    try { Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing; return } catch { Start-Sleep -Seconds 3 }
  }
  throw "não consegui baixar $url"
}
function Roda($exe, [string[]]$argumentos) {
  # aviso escrito na saída de erro não é falha: só o código de saída conta
  $ErrorActionPreference = 'Continue'
  $saida = & $exe @argumentos 2>&1; $saida | Out-File -FilePath $LOG -Append -Encoding UTF8
  if ($LASTEXITCODE -ne 0) { throw "$exe terminou com erro $LASTEXITCODE" }
}

if (-not $Diagnostico) { Add-Content -Path $LOG -Value "=== instalação $(Get-Date -Format 'dd/MM/yyyy HH:mm') ===" -Encoding UTF8 }

# ---------- diagnóstico ----------
$versao = [Environment]::OSVersion.Version
$arq = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { 'x64' }
$livre = [math]::Floor((Get-PSDrive -Name ($env:USERPROFILE.Substring(0, 1))).Free / 1GB)
Diz "Computador: Windows $($versao.Major).$($versao.Build), $arq, $livre GB livres"
$okWin = $versao.Major -ge 10
if (-not $okWin) { Diz '- Windows antigo: precisa do 10 ou do 11' }
if ($livre -lt 5) { Diz '- pouco espaço: deixe pelo menos 5 GB livres' }
$net = $true; try { Invoke-WebRequest -Uri 'https://nodejs.org' -UseBasicParsing -TimeoutSec 15 | Out-Null } catch { $net = $false }
if ($net) { Diz '- internet: ok' } else { Diz '- internet: sem acesso (precisa para baixar as ferramentas)' }

$NODE = $null
$n = Get-Command node -ErrorAction SilentlyContinue
if ($n) { try { if ([int](& node -p "process.versions.node.split('.')[0]") -ge 18) { $NODE = $n.Source } } catch {} }
if (Test-Path "$FERR\node\node.exe") { $NODE = "$FERR\node\node.exe" }
if ($NODE) { Diz "- Node: ok ($NODE)" } else { Diz '- Node: falta (o instalador baixa uma cópia só para a edição)' }
$navs = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")
$CHROME = $navs | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if ($CHROME) { Diz "- Navegador para as animações: ok ($CHROME)" } else { Diz '- Navegador: não encontrado (o instalador baixa um só para gravar as animações)' }
if (Test-Path "$FERR\node_modules\ffmpeg-static\ffmpeg.exe") { Diz '- Editor de vídeo (ffmpeg): ok' } else { Diz '- Editor de vídeo (ffmpeg): falta' }
if (Test-Path "$FERR\venv\Scripts\python.exe") { Diz '- Transcrição e motor (Python): ok' } else { Diz '- Transcrição e motor (Python): falta' }
if (Test-Path "$FERR\modelos\u2net_human_seg.onnx") { Diz '- Recorte da pessoa: ok' } else { Diz '- Recorte da pessoa: falta o modelo' }

if ($Diagnostico) {
  if ($okWin -and $net) { Diz 'Compatível. Para instalar: powershell -ExecutionPolicy Bypass -File instalar-windows.ps1' } else { Diz 'Ainda não compatível: resolva os itens acima.' }
  exit 0
}
if (-not $okWin) { Falha 'Windows 10 ou 11 é necessário' }
if (-not $net) { Falha 'sem internet' }
New-Item -ItemType Directory -Force -Path $FERR, "$FERR\modelos" | Out-Null

try {
  # ---------- 1. Node (só se o computador não tiver) ----------
  if (-not $NODE) {
    Diz '1/6 Baixando o Node (motor das animações)...'
    $nome = "node-$NODE_VER-win-$arq"
    Baixa "https://nodejs.org/dist/$NODE_VER/$nome.zip" "$FERR\node.zip"
    Expand-Archive -Path "$FERR\node.zip" -DestinationPath "$FERR\node-tmp" -Force
    if (Test-Path "$FERR\node") { Remove-Item -Recurse -Force "$FERR\node" }
    Move-Item "$FERR\node-tmp\$nome" "$FERR\node"; Remove-Item -Recurse -Force "$FERR\node-tmp", "$FERR\node.zip"
    $NODE = "$FERR\node\node.exe"
  } else { Diz '1/6 Node: já existe' }
  $nodeDir = Split-Path $NODE; $env:Path = "$nodeDir;$env:Path"
  $NPM = Join-Path $nodeDir 'npm.cmd'; $NPX = Join-Path $nodeDir 'npx.cmd'

  # ---------- 2. Editor de vídeo e gravador de animações ----------
  if (-not (Test-Path "$FERR\node_modules\ffmpeg-static\ffmpeg.exe") -or -not (Test-Path "$FERR\node_modules\puppeteer-core")) {
    Diz '2/6 Instalando o editor de vídeo e o gravador de animações...'
    if (-not (Test-Path "$FERR\package.json")) { '{"name":"ferramentas-ilha-de-edicao","private":true}' | Out-File "$FERR\package.json" -Encoding ascii }
    Push-Location $FERR; try { Roda $NPM @('install', '--no-audit', '--no-fund', '--loglevel=error', 'ffmpeg-static@5.2.0', 'puppeteer-core@25.13.0', 'three@0.186.1') } finally { Pop-Location }
  } else { Diz '2/6 Editor de vídeo: já instalado' }
  $FF = "$FERR\node_modules\ffmpeg-static\ffmpeg.exe"

  # ---------- 3. Navegador (só sem Chrome e sem Edge) ----------
  if (-not $CHROME) {
    $CHROME = Get-ChildItem -Path "$FERR\navegador" -Recurse -Filter 'chrome-headless-shell.exe' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    if (-not $CHROME) {
      Diz '3/6 Baixando um navegador só para gravar as animações...'
      Push-Location $FERR; try { Roda $NPX @('--yes', '@puppeteer/browsers', 'install', 'chrome-headless-shell@stable', '--path', "$FERR\navegador") } finally { Pop-Location }
      $CHROME = Get-ChildItem -Path "$FERR\navegador" -Recurse -Filter 'chrome-headless-shell.exe' | Select-Object -First 1 -ExpandProperty FullName
    }
  } else { Diz '3/6 Navegador: já existe' }

  # ---------- 4. Python, transcrição e motor ----------
  $PY = "$FERR\venv\Scripts\python.exe"
  $pronto = $false
  if (Test-Path $PY) { $ErrorActionPreference = 'Continue'; & $PY -c "import faster_whisper, PIL, numpy, onnxruntime" 2>$null; $pronto = ($LASTEXITCODE -eq 0); $ErrorActionPreference = 'Stop' }
  if (-not $pronto) {
    Diz '4/6 Instalando o Python da edição e a transcrição (pode levar alguns minutos)...'
    if (-not (Test-Path "$FERR\uv\uv.exe")) {
      $u = if ($arq -eq 'arm64') { 'uv-aarch64-pc-windows-msvc' } else { 'uv-x86_64-pc-windows-msvc' }
      Baixa "https://github.com/astral-sh/uv/releases/latest/download/$u.zip" "$FERR\uv.zip"
      Expand-Archive -Path "$FERR\uv.zip" -DestinationPath "$FERR\uv" -Force; Remove-Item "$FERR\uv.zip"
    }
    $env:UV_PYTHON_INSTALL_DIR = "$FERR\python"
    if (-not (Test-Path $PY)) { Roda "$FERR\uv\uv.exe" @('venv', '--python', '3.12', "$FERR\venv") }
    Roda "$FERR\uv\uv.exe" @('pip', 'install', '--python', $PY, 'faster-whisper==1.0.3', 'requests', 'huggingface_hub<2', 'numpy', 'pillow', 'onnxruntime')
  } else { Diz '4/6 Python e transcrição: já instalados' }

  # ---------- 5. Modelos: transcrição (cerca de 1,5 GB) e recorte da pessoa ----------
  Diz '5/6 Baixando o modelo de transcrição (na primeira vez são cerca de 1,5 GB)...'
  Roda $PY @('-W', 'ignore', '-c', "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu', compute_type='int8')")
  if (-not (Test-Path "$FERR\modelos\u2net_human_seg.onnx")) {
    Diz '    Baixando o modelo de recorte da pessoa...'
    Baixa 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx' "$FERR\modelos\u2net_human_seg.onnx"
  }

  # ---------- caminhos para o Claude e o motor ----------
  [ordered]@{ ferramentas = $FERR; node = $NODE; ffmpeg = $FF; python = $PY; node_path = "$FERR\node_modules"; chrome = $CHROME; scripts = $SCRIPTS; sistema = 'windows' } |
    ConvertTo-Json | Out-File "$FERR\caminhos.json" -Encoding utf8

  # ---------- 6. Teste: vídeo de 5 segundos ----------
  Diz '6/6 Gerando o vídeo de teste...'
  $env:MJ_FERRAMENTAS = $FERR; $env:PYTHONIOENCODING = 'utf-8'
  $ErrorActionPreference = 'Continue'
  $saida = & $PY -W ignore "$SCRIPTS\testar_instalacao.py" $FERR 2>&1; $saida | ForEach-Object { Diz "$_" }
  $ErrorActionPreference = 'Stop'
} catch { Falha $_.Exception.Message }

if ((Test-Path "$FERR\teste\teste-instalacao.mp4") -and (($saida | Out-String) -match 'PRONTO!')) {
  Start-Process explorer.exe "/select,`"$FERR\teste\teste-instalacao.mp4`""
  Diz 'PRONTO! A Ilha de edição está instalada. Peça ao Claude: "edita esse vídeo".'
} else { Falha 'o vídeo de teste não ficou pronto' }
