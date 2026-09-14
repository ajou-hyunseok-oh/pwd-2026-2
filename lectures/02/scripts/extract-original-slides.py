"""Preserve approved Week 2 PDF pages as scalable slide images."""

import json
from pathlib import Path

import fitz
from importlib import import_module
cleanup = import_module('pdf-slide-cleanup')


root = Path(__file__).resolve().parents[1]
source = root / "materials" / "[Week 2] 웹 개발 핵심 개념 이해와 웹 프레임워크를 활용한 개발 및 배포.pdf"
output = root / "materials" / "figures"
pages = [(10, "original-rendering-methods"), (11, "original-rendering-performance"),
         (8, "original-semantic-html"), (12, "original-routing-url"),
         (13, "original-routing-types")]
manifest = []
with fitz.open(source) as document:
    for number, slide_id in pages:
        page = document[number - 1]
        filename = f"{slide_id}.svg"
        # Glyph paths preserve the original fonts without requiring font installation.
        (output / filename).write_text(cleanup.without_course_label(page.get_svg_image(text_as_path=True)), encoding="utf-8")
        text = page.get_text().strip()
        manifest.append({"page": number, "id": slide_id, "title": text.splitlines()[1],
                         "image": filename, "text": cleanup.without_course_label_text(text)})
(output / "original-slides.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
