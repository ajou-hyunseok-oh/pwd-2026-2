"""Copy PDF pages 15–44; change only the assignment deadline's day glyph."""
import json
import re
from pathlib import Path
import fitz
from importlib import import_module
cleanup = import_module('pdf-slide-cleanup')

root = Path(__file__).resolve().parents[1]
source = root / "materials" / "[Week 2] 웹 개발 핵심 개념 이해와 웹 프레임워크를 활용한 개발 및 배포.pdf"
output = root / "materials" / "figures"
manifest = []
with fitz.open(source) as document:
    assert "웹 프레임워크를 활용한 개발" in document[14].get_text()
    for number in range(15, len(document) + 1):
        page = document[number - 1]
        text = page.get_text().strip()
        svg = page.get_svg_image(text_as_path=True)
        if number == 43:
            old, new = "9월 14일", "9월 12일"
            rects = page.search_for(old)
            assert len(rects) == 1
            rect = rects[0]
            # Reuse the same embedded font's existing '2' glyph. Preserve all
            # other paths, positioning, color, time of day and source PDF bytes.
            matches = []
            for match in re.finditer(r'<use data-text="4"[^>]+/>', svg):
                coords = re.search(r'transform="matrix\(([^)]+)\)"', match[0])[1].split(',')
                x, y = map(float, coords[-2:])
                if rect.contains(fitz.Point(x, y)):
                    matches.append(match)
            assert len(matches) == 1
            target = matches[0]
            glyph = re.search(r'xlink:href="([^"]+)"', target[0])[1]
            prefix = glyph.rsplit('_', 1)[0] + '_'
            replacement = re.search(r'<use data-text="2" xlink:href="(' + re.escape(prefix) + r'[^" ]+)"', svg)[1]
            changed = target[0].replace('data-text="4"', 'data-text="2"').replace(glyph, replacement)
            svg = svg[:target.start()] + changed + svg[target.end():]
            text = text.replace(old, new)
        slide_id = f"original-framework-{number}"
        filename = slide_id + ".svg"
        (output / filename).write_text(cleanup.without_course_label(svg), encoding="utf-8")
        manifest.append({"page": number, "id": slide_id, "title": text.splitlines()[1],
                         "image": filename, "text": cleanup.without_course_label_text(text)})
(output / "framework-slides.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Exported {len(manifest)} original pages; assignment deadline: September 12.")
