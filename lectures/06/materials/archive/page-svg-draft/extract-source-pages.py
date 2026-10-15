"""Extract original PDF text, vectors, images and fonts without rewriting."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'materials/[PWD Week4] Node.js Express 프레임워크를 이용한 웹 서버 개발.pdf'
OUT = ROOT / 'materials/source-pages'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

def display_font(original):
    # Use the established 05 browser typography. PDF subset fonts lack the
    # webfont metadata needed by browsers; preserve their originals separately.
    if 'Consolas' in original or 'Gulim' in original:
        return 'Consolas, "Liberation Mono", Menlo, monospace'
    if 'Emoji' in original:
        return '"Apple Color Emoji", "Noto Color Emoji", sans-serif'
    if 'Arial' in original:
        return 'Arial, sans-serif'
    return '"Noto Sans KR Variable", "Noto Sans KR", sans-serif'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    (OUT / 'original').mkdir(parents=True, exist_ok=True)
    (OUT / 'fonts').mkdir(exist_ok=True)
    document = pymupdf.open(SOURCE)
    font_records = []
    fonts = {f[0]: f for page in document for f in page.get_fonts(full=True)}
    for xref, record in fonts.items():
        name, extension, _, data = document.extract_font(xref)
        filename = f'fonts/{xref}.{extension}'
        (OUT / filename).write_bytes(data)
        font_records.append(dict(file=filename, family=record[3], sha256=digest(data)))
    rows = []
    for number, page in enumerate(document, 1):
        original = page.get_svg_image(text_as_path=False)
        filename = f'page-{number:02}.svg'
        (OUT / 'original' / filename).write_text(original)
        tree = ET.fromstring(original)
        # Preserve coordinates; only disambiguate document-global SVG identities.
        prefix = f'pdf{number:02}-'
        identities = {n.get('id'): prefix + n.get('id') for n in tree.iter() if n.get('id')}
        for node in tree.iter():
            for key, value in list(node.attrib.items()):
                if key == 'id':
                    node.set(key, identities[value])
                else:
                    for old, new in identities.items():
                        value = value.replace(f'url(#{old})', f'url(#{new})')
                    if value.startswith('#') and value[1:] in identities:
                        value = '#' + identities[value[1:]]
                    node.set(key, value)
        # Mark colors for the shared visual theme. No evidence geometry changes.
        background = tree.find(f'./{{{SVG}}}g/{{{SVG}}}g/{{{SVG}}}path')
        assert background is not None and background.get('fill') == '#ffffff'
        background.set('class', 'wd-source-background')
        for node in tree.findall(f'.//{{{SVG}}}text'):
            original_font = node.get('font-family')
            node.set('data-source-font-family', original_font)
            node.set('font-family', display_font(original_font))
            if float(node.get('font-size', '0')) >= 31:
                node.set('class', 'wd-source-title')
        lines = [line for block in page.get_text('dict')['blocks'] if block['type'] == 0 for line in block['lines']]
        titles = [''.join(s['text'] for s in line['spans']) for line in lines if any(s['size'] >= 23 for s in line['spans'])]
        assert len(titles) == 1, (number, titles)
        title = titles[0]
        tree.set('class', 'wd-source-page')
        tree.set('role', 'img')
        tree.set('aria-label', title)
        tree.set('width', '100%')
        tree.set('height', '100%')
        links = []
        for link in page.get_links():
            if not link.get('uri'):
                continue
            rectangle = link['from']
            anchor = ET.SubElement(tree, f'{{{SVG}}}a', {'href': link['uri'], 'target': '_blank', 'rel': 'noopener noreferrer', 'aria-label': link['uri']})
            ET.SubElement(anchor, f'{{{SVG}}}rect', {'x': str(rectangle.x0), 'y': str(rectangle.y0), 'width': str(rectangle.width), 'height': str(rectangle.height), 'fill': 'transparent'})
            links.append({'url': link['uri'], 'bbox_pt': list(rectangle)})
        formatted = ET.tostring(tree, encoding='unicode') + '\n'
        (OUT / filename).write_text(formatted)
        rows.append(dict(number=number, id='cover' if number == 1 else f'pdf-{number:02}', title=title,
                         source_pages=[number], svg=filename, original_svg='original/' + filename,
                         svg_sha256=digest(formatted.encode()), original_svg_sha256=digest(original.encode()),
                         original_text=page.get_text(), text_runs=sum(1 for _ in tree.iter(f'{{{SVG}}}text')),
                         image_occurrences=len(page.get_image_info(xrefs=True)), vector_paths=len(page.get_drawings()), links=links))
    manifest = dict(source=SOURCE.name, source_sha256=digest(SOURCE.read_bytes()), page_count=len(document), language='ko',
                    content_policy='verbatim PDF pages; formatting only; no content updates', extractor='PyMuPDF ' + pymupdf.VersionBind, fonts=font_records, pages=rows)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'Extracted {len(rows)} original pages, {sum(r["image_occurrences"] for r in rows)} image placements; content unchanged')

if __name__ == '__main__':
    main()
