"""Inventory the supplied PDF without changing its content or embedded artwork.

Requires PyMuPDF and Pillow in the analysis Python environment, and Poppler.
Produces page text, page renders, deduplicated images, links and a source map.
Only rendering/extraction occurs here; technical decisions live in review.ko.md.
"""
import hashlib
import json
from pathlib import Path
import subprocess

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'materials/[PWD Week4] Node.js Express 프레임워크를 이용한 웹 서버 개발.pdf'
OUT = ROOT / 'materials/source-analysis'
# PDF image object identities are tied to the source hash in manifest.json.
ASSETS = {12: ('ajou-footer', 'branding', '반복 학교·학과 로고', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 36: ('client-server-network', 'diagram-part', '클라이언트·네트워크·서버 도식 바탕', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 37: ('response-message-shadow', 'decoration', '응답 메시지 패널의 그림자', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 38: ('response-message',
      'diagram-part',
      'HTTP 200·Access-Control-Allow-Origin 응답 메시지',
      '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 39: ('request-message-shadow', 'decoration', '요청 메시지 패널의 그림자', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 40: ('request-message', 'diagram-part', 'GET·Origin 요청 메시지', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 41: ('json-sample', 'code-image', 'JSON 예시 이미지', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 64: ('backend-ranking-2025',
      'historical-chart',
      'Jan-2025 백엔드 프레임워크 순위 이미지',
      '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 71: ('node-homepage-2025',
      'historical-screenshot',
      'Node.js 홈페이지 소개·다운로드 화면 캡처',
      '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 78: ('nodejs-logo', 'branding', 'Node.js 로고', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 79: ('rocket-turtle-illustration', 'decoration', '로켓을 탄 거북이 삽화', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 97: ('request-icon', 'decoration', 'Request 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 98: ('response-icon', 'decoration', 'Response 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 129: ('cross-icon', 'decoration', '오류 표시 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 130: ('check-icon', 'decoration', '확인 표시 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 152: ('mvc-diagram', 'diagram', 'MVC 요청·응답 관계', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 161: ('mvcs-diagram', 'diagram', 'Service를 추가한 계층 도식', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 168: ('folder-icon', 'decoration', '반복 폴더 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 169: ('file-icon', 'decoration', '반복 파일 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 181: ('tdd-cycle', 'diagram', 'Red·Green·Refactor 반복 도식', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 193: ('express-logo', 'branding', '원본 Express 로고', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 208: ('project-folder-icon', 'decoration', '프로젝트 루트 폴더 아이콘', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화'),
 217: ('render-logo', 'branding', 'Render 로고', '해당 슬라이드 문맥과 구성 요소 보존; 페이지 배치는 05 형식에 맞춰 최적화')}
# Composed PDF graphics include text/vector elements and are not single images.
CROPS = [
    (4, 'client-server-composite', [20, 4, 585, 240], '제목과 요청/응답·JSON을 포함한 원본 상단 합성 도식'),
    (16, 'middleware-pipeline', [105, 271, 615, 365], 'PDF 벡터·텍스트로 구성한 미들웨어 처리 흐름'),
    (19, 'mvcs-file-tree', [132, 94, 588, 338], '아이콘·텍스트가 결합된 원본 MVCS 폴더 트리'),
    (24, 'express-file-tree', [518, 241, 699, 382], '아이콘·텍스트가 결합된 Express 프로젝트 트리'),
]


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    for name in ('text', 'pages', 'images', 'crops', 'contact-sheets'):
        (OUT / name).mkdir(parents=True, exist_ok=True)
    document = pymupdf.open(SOURCE)
    titles = [next("".join(s["text"] for s in line["spans"]) for block in page.get_text("dict")["blocks"] if block["type"] == 0 for line in block["lines"] if any(s["size"] >= 23 for s in line["spans"])) for page in document]
    layout_text = subprocess.check_output(['pdftotext', '-layout', str(SOURCE), '-'], text=True)
    texts = layout_text.split('\f')
    assert len(texts) == len(document) + 1 and not texts[-1].strip()
    (OUT / 'original-layout.txt').write_text(layout_text)
    slide_map = json.loads((ROOT / 'materials/slide-map.json').read_text())
    pages, images, links = [], {}, []
    for number, page in enumerate(document, 1):
        stem = f'page-{number:02}'
        (OUT / 'text' / (stem + '.txt')).write_text(texts[number - 1].strip() + '\n')
        page.get_pixmap(matrix=pymupdf.Matrix(1600 / page.rect.width, 1600 / page.rect.width), alpha=False).save(OUT / 'pages' / (stem + '.png'))
        masks = {image[0]: image[1] for image in page.get_images(full=True)}
        placements = []
        for info in page.get_image_info(xrefs=True):
            xref = info['xref']
            assert xref in ASSETS, f'Unreviewed image object {xref}'
            name, category, description, decision = ASSETS[xref]
            if xref not in images:
                original = document.extract_image(xref)
                raw = f'images/{name}-original.{original["ext"]}'
                (OUT / raw).write_bytes(original['image'])
                pixmap = pymupdf.Pixmap(document, xref)
                if masks.get(xref):
                    pixmap = pymupdf.Pixmap(pixmap, pymupdf.Pixmap(document, masks[xref]))
                combined = f'images/{name}.png'
                pixmap.save(OUT / combined)
                images[xref] = dict(id=name, xref=xref, category=category, description=description,
                                    decision=decision, width=info['width'], height=info['height'],
                                    original=raw, composed_png=combined,
                                    original_sha256=hashlib.sha256(original['image']).hexdigest(),
                                    has_alpha=bool(masks.get(xref)), occurrences=[])
            occurrence = dict(page=number, bbox_pt=[round(v, 3) for v in info['bbox']])
            images[xref]['occurrences'].append(occurrence)
            placements.append(dict(id=name, **occurrence))
        page_links = []
        for link in page.get_links():
            if link.get('uri'):
                item = dict(page=number, url=link['uri'], bbox_pt=list(link['from']))
                links.append(item)
                page_links.append(item)
        pages.append(dict(page=number, title=titles[number-1], text=f'text/{stem}.txt',
                          render=f'pages/{stem}.png', width_pt=page.rect.width, height_pt=page.rect.height,
                          text_characters=len(texts[number-1].strip()), image_occurrences=placements,
                          vector_path_count=len(page.get_drawings()), links=page_links,
                          current_slides=[dict(number=row['number'], id=row['id'], title=row['title'])
                                          for row in slide_map if number in row['source_pages']]))
    crops = []
    for page_no, name, bbox, description in CROPS:
        page = document[page_no - 1]
        filename = f'crops/{name}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(bbox), alpha=False).save(OUT / filename)
        crops.append(dict(page=page_no, id=name, file=filename, bbox_pt=bbox, description=description,
                          content='unaltered crop of the rendered original page'))
    # Review montage only. Source artwork is never redrawn or retouched.
    font = ImageFont.load_default(size=20)
    for start in range(0, len(pages), 9):
        sheet = Image.new('RGB', (1440, 900), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for index, record in enumerate(pages[start:start+9]):
            thumb = Image.open(OUT / record['render'])
            thumb.thumbnail((464, 261))
            x, y = (index % 3)*480 + 8, (index // 3)*300 + 28
            sheet.paste(thumb, (x,y))
            draw.text((x,y-25), f'PDF {record["page"]:02}', fill='black', font=font)
        sheet.save(OUT / 'contact-sheets' / f'pages-{start+1:02}-{min(start+9,len(pages)):02}.png')
    sheet = Image.new('RGB', (1280, 1440), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for index, asset in enumerate(images.values()):
        thumb = Image.open(OUT / asset['composed_png']).convert('RGBA')
        thumb.thumbnail((300, 200))
        x, y = (index % 4)*320 + 10, (index // 4)*240 + 30
        draw.rectangle((x,y,x+300,y+200), fill='white')
        sheet.paste(thumb, (x+(300-thumb.width)//2,y+(200-thumb.height)//2), thumb)
        draw.text((x,y-24), f'XREF {asset["xref"]}', fill='black', font=font)
    sheet.save(OUT / 'contact-sheets/images.png')
    manifest = dict(source=SOURCE.name, source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                    metadata=document.metadata, page_count=len(document),
                    unique_image_objects=len(images), image_occurrence_count=sum(len(p['image_occurrences']) for p in pages),
                    hyperlink_count=len(links), render_width_px=1600,
                    note='Image counts exclude PDF soft masks. Composed vector/text diagrams are inventoried separately.',
                    tools=dict(pymupdf=pymupdf.VersionBind, text_extractor='Poppler pdftotext -layout'),
                    pages=pages, images=list(images.values()), composite_crops=crops, links=links)
    write_json(OUT / 'manifest.json', manifest)
    lines = ['# 원본 PDF 페이지·이미지 목록', '',
             '원본의 텍스트·그림·링크를 추출한 자료다. 내용 판단과 2026년 업데이트는 [검토 보고서](review.ko.md)에 기록한다.', '',
             f'27쪽 · 고유 이미지 {len(images)}개 · 이미지 배치 {manifest["image_occurrence_count"]}회 · 실제 PDF 링크 {len(links)}개', '',
             '이미지 개수는 투명도 마스크를 제외한 PDF 객체 기준이다. 같은 아이콘·로고를 중복 저장하지 않는다. PNG는 원본 이미지와 해당 투명도 마스크를 합친 추출본이다.', '',
             '## 전체 페이지', '', '| PDF | 주제 | 텍스트 | 원본 화면 | 현재 06 화면 |', '| --- | --- | --- | --- | --- |']
    for p in pages:
        targets = ' · '.join(str(s['number']) for s in p['current_slides']) or '표지/목표/구분/Q&A: 별도 검토'
        lines.append(f'| {p["page"]:02} | {p["title"]} | [추출]({p["text"]}) | [1600px PNG]({p["render"]}) | {targets} |')
    lines += ['', '## 이미지 자산', '', '| ID | 원본 쪽 | 크기 | 원본 용도·보존 기준 |', '| --- | --- | --- | --- |']
    for asset in images.values():
        numbers = ', '.join(str(p) for p in sorted({o['page'] for o in asset['occurrences']}))
        lines.append(f'| [{asset["id"]}]({asset["composed_png"]}) | {numbers} | {asset["width"]}×{asset["height"]} | {asset["description"]} · {asset["decision"]} |')
    lines += ['', '## 합성·벡터 도식', '',
              '다음 도식은 이미지 객체 하나로 추출되지 않는다. 원본 페이지의 해당 구역을 그대로 렌더링한 자산이다.', '']
    for c in crops:
        lines.append(f'- PDF {c["page"]}: [{c["description"]}]({c["file"]})')
    lines += ['', '## 원본 전체 미리보기', '']
    for start in (1,10,19):
        name=f'contact-sheets/pages-{start:02}-{start+8:02}.png'
        lines.append(f'![PDF {start}–{start+8}]({name})\n')
    lines += ['## 추출 이미지 미리보기', '', '![중복을 제거한 23개 이미지](contact-sheets/images.png)', '']
    (OUT / 'README.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:manifest[k] for k in ('page_count','unique_image_objects','image_occurrence_count','hyperlink_count')},ensure_ascii=False))


if __name__ == '__main__':
    main()
