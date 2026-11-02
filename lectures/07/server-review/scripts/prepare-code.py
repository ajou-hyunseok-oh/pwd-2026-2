"""Freeze verbatim source ranges; keep the review build independent of pwd-week6."""
import argparse
import hashlib
import json
from pathlib import Path
from lesson import EXCERPTS

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--server-root', type=Path, default=ROOT.parents[3] / 'pwd-week6')
args = parser.parse_args()
records = {}
for ident, (name, ranges) in EXCERPTS.items():
    content = (args.server_root / name).read_text()
    lines = content.splitlines()
    selections = []
    # Keep disjoint excerpts in source order, including the matching closing brace.
    cursor = 0
    for start, end in ranges:
        first = next(i for i in range(cursor, len(lines)) if
                     (lines[i].strip() == start if ident == 'build' else start in lines[i]))
        last = next(i for i in range(first, len(lines)) if
                    (lines[i].strip() == end if end in ('}', '});') else end in lines[i]))
        selections.append(dict(startLine=first + 1, endLine=last + 1, text='\n'.join(lines[first:last + 1])))
        cursor = last + 1
    records[ident] = dict(file=name, sha256=hashlib.sha256(content.encode()).hexdigest(),
                         language='bash' if ident == 'build' else 'typescript',
                         selections=selections, code='\n\n'.join(s['text'] for s in selections))
(ROOT / 'materials').mkdir(exist_ok=True)
(ROOT / 'materials/code-excerpts.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(f'Frozen {len(records)} source excerpts from {args.server_root}')
