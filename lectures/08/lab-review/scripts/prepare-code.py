"""Freeze actual lab code so slide regeneration does not require its repository."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from excerpts import EXCERPTS

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--server-root', type=Path, default=ROOT.parents[3] / 'pwd-week7')
parser.add_argument('--client-root', type=Path, default=ROOT.parents[3] / 'pwd-week7-client')
args = parser.parse_args()
repositories = {}
for origin, source_root in [('server', args.server_root), ('client', args.client_root)]:
    repositories[origin] = dict(
        repository=f'https://github.com/ajou-hyunseok-oh/pwd-week7' + ('-client' if origin == 'client' else ''),
        commit=subprocess.check_output(['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True).strip())
records = {}
for ident, (name, language, ranges) in EXCERPTS.items():
    origin = 'client' if name.startswith('client:') else 'server'
    name = name.removeprefix('client:')
    source_root = args.client_root if origin == 'client' else args.server_root
    content = (source_root / name).read_text()
    lines, cursor, selections = content.splitlines(), 0, []
    for selection in ranges:
        start, end = selection[:2]
        first = next(i for i in range(cursor, len(lines)) if start in lines[i])
        first += selection[2] if len(selection) > 2 else 0
        last = next(i for i in range(first, len(lines)) if end in lines[i])
        selections.append(dict(startLine=first + 1, endLine=last + 1,
                               text='\n'.join(lines[first:last + 1])))
        cursor = last + 1
    records[ident] = dict(file=name, origin=origin, language=language,
                         sha256=hashlib.sha256(content.encode()).hexdigest(),
                         selections=selections,
                         code='\n\n'.join(s['text'] for s in selections))
snapshot = dict(repository='https://github.com/ajou-hyunseok-oh/pwd-week7',
                commit=repositories['server']['commit'], repositories=repositories,
                excerpts=records)
(ROOT / 'materials/code-excerpts.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
print(f'Frozen {len(records)} code excerpts')
