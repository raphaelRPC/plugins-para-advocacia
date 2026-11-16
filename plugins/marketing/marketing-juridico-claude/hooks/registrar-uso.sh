#!/bin/sh
# Registro de uso do plugin (hook Stop do Claude Code).
# Guarda só o identificador da conversa e o endereço do histórico, uma vez por conversa.
# Nenhum texto da conversa é copiado. Quem soma o uso é o skills/uso-do-plano/scripts/uso.py.
pasta="$HOME/.marketing-juridico/uso"
mkdir -p "$pasta" 2>/dev/null || exit 0
entrada=$(cat)
sessao=$(printf '%s' "$entrada" | grep -o '"session_id" *: *"[^"]*"' | head -1 | sed 's/.*: *"//; s/"$//')
historico=$(printf '%s' "$entrada" | grep -o '"transcript_path" *: *"[^"]*"' | head -1 | sed 's/.*: *"//; s/"$//')
[ -n "$sessao" ] && [ -n "$historico" ] || exit 0
arquivo="$pasta/sessoes.jsonl"
grep -q "\"sessao\":\"$sessao\"" "$arquivo" 2>/dev/null && exit 0
printf '{"quando":"%s","sessao":"%s","historico":"%s"}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$sessao" "$historico" >> "$arquivo"
exit 0
