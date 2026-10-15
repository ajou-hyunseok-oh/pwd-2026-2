"""Freeze real source excerpts so the lecture rebuilds without its sibling repository."""
import argparse
import hashlib
import json
from pathlib import Path
from lesson import EXCERPTS

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--client-root', type=Path, default=ROOT.parents[3] / 'pwd-week5')
args = parser.parse_args()
records = {}
for ident, (name, ranges) in EXCERPTS.items():
    content = (args.client_root / name).read_text()
    lines = content.splitlines()
    selections = []
    for start, end in ranges:
        first = next(i for i, line in enumerate(lines) if start in line)
        last = next(i for i in range(first, len(lines)) if
                    (lines[i].strip() == end if end in ('}', ')') else end in lines[i]))
        selections.append(dict(startLine=first + 1, endLine=last + 1, text='\n'.join(lines[first:last + 1])))
    # Object method excerpts are wrapped in their existing containing declaration.
    text = '\n'.join(selection['text'] for selection in selections)
    if ident == 'get-restaurants':
        text = 'export const restaurantAPI = {\n' + text + '\n};'
    records[ident] = dict(file=name, sha256=hashlib.sha256(content.encode()).hexdigest(), selections=selections, code=text)
(ROOT / 'materials').mkdir(exist_ok=True)
(ROOT / 'materials/code-excerpts.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(f'Frozen {len(records)} source excerpts from {args.client_root}')
