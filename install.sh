#!/usr/bin/env bash
# Install the fable skills as plain skill folders, without the plugin system.
#
#   ./install.sh                    copy into ~/.claude/skills (all your projects)
#   ./install.sh --project <dir>    copy into <dir>/.claude/skills (that repository only)
#
#   --always-on                     also add a short instruction to CLAUDE.md
#                                   (~/.claude/CLAUDE.md, or <dir>/CLAUDE.md) so that
#                                   the playbook is loaded on every task
#
# Re-running upgrades in place: each fable-* skill folder at the destination is
# replaced. Nothing else at the destination is touched.
set -euo pipefail

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
project_dir=""
always_on=0

while [ $# -gt 0 ]; do
  case "$1" in
    --project)
      [ $# -ge 2 ] || { echo "error: --project needs a directory" >&2; exit 2; }
      project_dir="$2"; shift 2 ;;
    --always-on) always_on=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -n "$project_dir" ]; then
  [ -d "$project_dir" ] || { echo "error: not a directory: $project_dir" >&2; exit 2; }
  project_dir="$(cd "$project_dir" && pwd)"
  skills_dest="$project_dir/.claude/skills"
  instructions_file="$project_dir/CLAUDE.md"
else
  config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  skills_dest="$config_dir/skills"
  instructions_file="$config_dir/CLAUDE.md"
fi

[ -d "$source_dir" ] || { echo "error: skills folder not found beside this script: $source_dir" >&2; exit 1; }

mkdir -p "$skills_dest"
count=0
for skill in "$source_dir"/fable-*/; do
  name="$(basename "$skill")"
  rm -rf "${skills_dest:?}/$name"
  cp -R "$skill" "$skills_dest/$name"
  count=$((count + 1))
done
echo "Installed $count skills into $skills_dest"

if [ "$always_on" -eq 1 ]; then
  if [ -f "$instructions_file" ] && grep -q 'fable-playbook:start' "$instructions_file"; then
    echo "Always-on instruction already present in $instructions_file"
  else
    mkdir -p "$(dirname "$instructions_file")"
    [ -s "$instructions_file" ] && printf '\n' >> "$instructions_file"
    cat >> "$instructions_file" <<'EOF'
<!-- fable-playbook:start -->
## Working method

Follow the `fable-playbook` skill on every task. Load it at the start of each new task, before reading files or running commands, unless it is already in context. It scales its process to the size of the task and points to the specialist `fable-*` skills.
<!-- fable-playbook:end -->
EOF
    echo "Added the always-on instruction to $instructions_file"
  fi
else
  echo "Tip: re-run with --always-on to have the playbook loaded on every task."
fi
