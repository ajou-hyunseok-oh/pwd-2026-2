from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

lecture = Path(__file__).resolve().parents[1]
root = lecture / 'examples'
target = lecture / 'materials' / 'week2-examples.zip'
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for file in sorted(root.rglob('*')):
        if file.is_file() and 'node_modules' not in file.relative_to(root).parts:
            archive.write(file, 'examples/' + file.relative_to(root).as_posix())
print(f'Packaged {target.name}: {target.stat().st_size:,} bytes')
