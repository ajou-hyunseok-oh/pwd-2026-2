"""Extract only the two selected historical evidence regions, never PDF pages."""
from pathlib import Path
import hashlib
import json
from urllib.request import urlopen
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT.parents[1] / 'tmp/pdfs/week09-placement'
TARGET = ROOT / 'assets/new'
TARGET.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
SPECS = [
    ('dartmouth', 0, (150, 155, 462, 323), 'dartmouth-proposal-heading.png',
     'https://www-formal.stanford.edu/jmc/history/dartmouth.pdf'),
    ('alexnet', 7, (246, 81, 292, 156.8), 'alexnet-leopard-predictions.png',
     'https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf'),
]
records = []
for name, page, rect, filename, url in SPECS:
    path = TMP / (name + '.pdf')
    if not path.exists():
        with urlopen(url, timeout=30) as response:
            path.write_bytes(response.read())
    doc = pymupdf.open(path)
    pix = doc[page].get_pixmap(matrix=pymupdf.Matrix(5, 5), clip=pymupdf.Rect(rect), alpha=False)
    pix.save(TARGET / filename)
    records.append(dict(file='assets/new/' + filename, url=url, pdf_page=page + 1,
                        crop_points=rect, source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        output_sha256=hashlib.sha256((TARGET / filename).read_bytes()).hexdigest(),
                        width=pix.width, height=pix.height,
                        transformation='원본 영역 발췌·비율 유지; 내용 합성·확률 변경 없음'))
(ROOT / 'materials/new-resource-research/extracted-assets.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print('Extracted two selected evidence regions.')
