"""Extract the original rendering diagram from page 9 of the Week 2 PDF."""

from pathlib import Path

import fitz


lecture_root = Path(__file__).resolve().parents[1]
source = lecture_root / "materials" / "[Week 2] 웹 개발 핵심 개념 이해와 웹 프레임워크를 활용한 개발 및 배포.pdf"

with fitz.open(source) as document:
    page = document[8]
    # The other embedded image on this page is the small university logo.
    diagram = max(page.get_images(full=True), key=lambda item: item[2] * item[3])
    original = document.extract_image(diagram[0])
    output = lecture_root / "materials" / "figures" / f"browser-rendering-original.{original['ext']}"
    output.write_bytes(original["image"])
    print(f"Extracted page 9 diagram: {output.name} ({original['width']} x {original['height']})")
