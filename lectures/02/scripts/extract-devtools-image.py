"""Extract the unchanged right-hand image from original Week 2 PDF page 14."""
from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[1]
source = root / "materials" / "[Week 2] 웹 개발 핵심 개념 이해와 웹 프레임워크를 활용한 개발 및 배포.pdf"
with fitz.open(source) as document:
    page = document[13]
    target = max(page.get_images(full=True), key=lambda image: image[2] * image[3])
    image = document.extract_image(target[0])
    (root / "materials" / "figures" / f"devtools-original.{image['ext']}").write_bytes(image['image'])
