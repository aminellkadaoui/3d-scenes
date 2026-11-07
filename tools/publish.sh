#!/bin/bash
# 3D Scenes — publish local changes to GitHub so everyone who installed the plugin gets them.
# Usage:  bash tools/publish.sh "short note about the change"
# What it does: privacy check -> bump patch version -> commit -> push -> refresh the local install.
set -u
cd "$(dirname "$0")/.." || exit 1
NOTE="${1:-knowledge update}"

if [ -z "$(git status --porcelain)" ]; then echo "nothing to publish"; exit 0; fi

# privacy guard: never publish IPs, home paths, tokens or passwords
if git diff HEAD --unified=0 -- . ':!tools/publish.sh' | grep -E '^\+' \
   | grep -qiE '([0-9]{1,3}\.){3}[0-9]{1,3}|/Users/[A-Za-z]|/home/[a-z]|C:\\Users|gh[opsu]_[A-Za-z0-9]{10}|password'; then
  echo "BLOCKED: the changes contain private-looking text (IP / home path / token). Remove it, then publish again."
  git diff HEAD --unified=0 -- . ':!tools/publish.sh' | grep -E '^\+' | grep -iE '([0-9]{1,3}\.){3}[0-9]{1,3}|/Users/[A-Za-z]|/home/[a-z]|C:\\Users|gh[opsu]_|password'
  exit 2
fi

V=$(python3 - <<'PY'
import json
pj="plugins/3d-scenes/.claude-plugin/plugin.json"; mj=".claude-plugin/marketplace.json"
p=json.load(open(pj)); a,b,c=(p["version"].split(".")+["0","0"])[:3]; v=f"{a}.{b}.{int(c)+1}"
p["version"]=v; open(pj,"w").write(json.dumps(p,indent=2,ensure_ascii=False)+"\n")
m=json.load(open(mj)); m.setdefault("metadata",{})["version"]=v
for x in m["plugins"]:
    if x["name"]=="3d-scenes": x["version"]=v
open(mj,"w").write(json.dumps(m,indent=2,ensure_ascii=False)+"\n")
print(v)
PY
)
git add -A
git commit -q -m "v$V: $NOTE" || exit 1
git push -q origin HEAD && echo "published v$V to GitHub" || { echo "push failed (check gh auth)"; exit 1; }

# refresh this machine's installed copy (if the claude CLI is reachable)
CLAUDE="$(command -v claude || ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude 2>/dev/null | sort -V | tail -1)"
if [ -n "$CLAUDE" ] && [ -x "$CLAUDE" ]; then
  "$CLAUDE" plugin marketplace update 3d-scenes >/dev/null 2>&1
  "$CLAUDE" plugin update 3d-scenes@3d-scenes 2>&1 | tail -1
fi
