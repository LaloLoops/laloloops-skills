#!/usr/bin/env bash
# Wrapper around the locally-installed Graph::Easy `graph-easy` CLI.
# Pins PERL5LIB to the self-contained local-lib install so it works
# regardless of PATH / which perl is active.
set -euo pipefail

GE_BIN="$HOME/.local/perl5/bin/graph-easy"
export PERL5LIB="$HOME/.local/perl5/lib/perl5${PERL5LIB:+:$PERL5LIB}"

if [[ ! -x "$GE_BIN" ]]; then
  echo "graph-easy not found at $GE_BIN" >&2
  echo "Install it with:  brew install cpanminus && cpanm -n -l \"\$HOME/.local/perl5\" Graph::Easy" >&2
  exit 127
fi

# Default to Unicode boxart unless the caller passes their own --as=.
has_as=0
for a in "$@"; do [[ "$a" == --as=* ]] && has_as=1; done
if [[ $has_as -eq 0 ]]; then
  exec "$GE_BIN" --as=boxart "$@"
else
  exec "$GE_BIN" "$@"
fi
