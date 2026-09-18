"""Package the actual SvelteKit course source without Git metadata or installs."""
import hashlib
import json
import os
import subprocess
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

lecture = Path(__file__).resolve().parents[1]
default_source = lecture.parents[2] / 'pwd-2026-practices' / 'pwd-week2'
source = Path(os.environ.get('SVELTE_PRACTICE_ROOT', default_source)).resolve()
files = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z']).decode('utf-8').split('\0')
commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
target = lecture / 'materials' / 'pwd-week2.zip'
provenance = {'source': 'pwd-week2', 'commit': commit, 'files': []}

with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for relative in sorted(f for f in files if f):
        file = (source / relative).resolve()
        if not file.is_relative_to(source) or not file.is_file():
            raise ValueError(f'Invalid source file: {relative}')
        if any(part in {'.git', 'node_modules', '.svelte-kit', '.vercel'} for part in Path(relative).parts) or file.name.startswith('.env'):
            raise ValueError(f'Unexpected generated or environment file: {relative}')
        data = file.read_bytes()
        info = ZipInfo('pwd-week2/' + relative, date_time=(2026, 9, 14, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        archive.writestr(info, data)
        provenance['files'].append({'path': relative, 'sha256': hashlib.sha256(data).hexdigest()})
    info = ZipInfo('pwd-week2/README.en.md', date_time=(2026, 9, 14, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    archive.writestr(info, (lecture / 'materials' / 'practice-guide.en.md').read_bytes())

provenance['archiveSha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
(lecture / 'materials' / 'final-review' / 'practice-package.json').write_text(json.dumps(provenance, indent=2) + '\n', encoding='utf-8')
print(f'Packaged {len(provenance["files"])} source files and English guide: {target.name}')
