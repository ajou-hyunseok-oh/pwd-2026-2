"""Prepare original per-slide text, code, tables and artwork for Week 05 layouts."""
import hashlib
import json
import re
from pathlib import Path
import shutil
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'materials/[PWD Week4] Node.js Express 프레임워크를 이용한 웹 서버 개발.pdf'
OUT = ROOT / 'materials/elements'
CROPS = {
    4: [('webservice-diagram', [151, 3, 578, 238])],
    10: [('http-exchange', [340, 166, 702, 292])],
    14: [('rest-examples', [438, 190, 687, 258])],
    16: [('middleware-pipeline', [107, 273, 613, 363])],
    19: [('mvcs-tree', [133, 94, 588, 311])],
    23: [('project-tree', [34, 148, 325, 359])],
    24: [('express-tree', [518, 241, 699, 382])],
}
CODES = {
    11: [('http-request', [42, 65, 679, 198], 'text')],
    12: [('http-response', [42, 63, 679, 231], 'text')],
    13: [('json-object', [438, 70, 710, 193], 'json'), ('json-transform', [411, 228, 710, 329], 'javascript')],
    16: [('middleware-code', [436, 166, 714, 240], 'javascript')],
    22: [('node-http', [34, 210, 305, 361], 'javascript'), ('express-http', [380, 210, 651, 361], 'javascript')],
    23: [('install-express', [35, 70, 409, 132], 'bash'), ('hello-world', [395, 210, 666, 361], 'javascript')],
}
RAW_ASSETS = {
    6: ['backend-ranking-2025'], 7: ['node-homepage-2025'],
    8: ['nodejs-logo', 'rocket-turtle-illustration'],
    17: ['mvc-diagram'], 18: ['mvcs-diagram'], 20: ['tdd-cycle'],
    22: ['express-logo', 'cross-icon', 'check-icon'],
    24: ['project-folder-icon'], 25: ['render-logo'],
}
TABLES = {6:4, 11:3, 15:4}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def contains(rect, bbox):
    return pymupdf.Rect(rect).contains(pymupdf.Rect(bbox).tl + (pymupdf.Rect(bbox).br - pymupdf.Rect(bbox).tl) * .5)

def main():
    (OUT / 'images').mkdir(parents=True, exist_ok=True)
    (OUT / 'code').mkdir(exist_ok=True)
    document = pymupdf.open(PDF)
    inventory = json.loads((ROOT / 'materials/source-analysis/manifest.json').read_text())
    raw_assets = {a['id']:a for a in inventory['images']}
    pages, all_assets, all_codes = [], [], []
    for number, page in enumerate(document, 1):
        lines = []
        for bi, block in enumerate(page.get_text('dict')['blocks']):
            if block['type'] != 0:
                continue
            for li, line in enumerate(block['lines']):
                runs = [dict(text=s['text'], bold='Bold' in s['font'], italic='Italic' in s['font'], color=s['color']) for s in line['spans']]
                lines.append(dict(id=f'p{number:02}-b{bi:02}-l{li:02}', block=bi,
                                  text=''.join(r['text'] for r in runs), runs=runs,
                                  bbox=list(line['bbox']), size=max(s['size'] for s in line['spans']),
                                  baseline=line['spans'][0]['origin'][1]))
        title_line = next(l for l in lines if l['size'] >= 23)
        title = title_line['text'].strip()
        assets, codes, regions, tables = [], [], [], []
        for ident, bbox in CROPS.get(number, []):
            # Isolate the complete composed diagram, excluding a page title that
            # overlaps the extraction rectangle. Its actual diagram stays intact.
            clip_document = pymupdf.open(stream=document.tobytes(), filetype='pdf')
            clip_page = clip_document[number-1]
            if number == 4:
                clip_page.add_redact_annot(pymupdf.Rect(title_line['bbox']), fill=None, cross_out=False)
                clip_page.apply_redactions(images=0, graphics=0, text=0)
            file = f'images/{ident}.png'
            clip_page.get_pixmap(matrix=pymupdf.Matrix(4,4), clip=pymupdf.Rect(bbox), alpha=False).save(OUT / file)
            clip_document.close()
            record = dict(id=ident, page=number, file=file, bbox=bbox, method='unaltered composed PDF region', sha256=sha((OUT/file).read_bytes()))
            assets.append(record); regions.append((bbox, 'image', ident))
        for ident in RAW_ASSETS.get(number, []):
            asset = raw_assets[ident]
            file = f'images/{ident}.png'
            shutil.copyfile(ROOT/'materials/source-analysis'/asset['composed_png'], OUT/file)
            placements = [o['bbox_pt'] for o in asset['occurrences'] if o['page']==number]
            record = dict(id=ident, page=number, file=file, bbox=placements[0], method='original embedded image and alpha', sha256=sha((OUT/file).read_bytes()))
            assets.append(record)
            # Embedded image labels can also be separately extractable glyphs.
            for bbox in placements:
                regions.append((bbox, 'image', ident))
        for ident, bbox, language in CODES.get(number, []):
            selected = [l for l in lines if contains(bbox,l['bbox']) and any(r['color']==65280 for r in l['runs'])]
            selected.sort(key=lambda l:(round(l['baseline'],1),l['bbox'][0]))
            output, previous = [], None
            for line in selected:
                if previous is not None and line['baseline']-previous > line['size']*1.8:
                    output.append('')
                output.append(line['text'])
                previous=line['baseline']
            code='\n'.join(output).strip('\n')
            file=f'code/{ident}.{dict(javascript="js",json="json",bash="sh",text="txt")[language]}'
            (OUT/file).write_text(code+'\n')
            record=dict(id=ident,page=number,file=file,language=language,code=code,bbox=bbox,line_ids=[l['id'] for l in selected],sha256=sha((OUT/file).read_bytes()))
            codes.append(record); regions.append((bbox,'code',ident))
        if number in TABLES:
            candidates=[t for t in page.find_tables().tables if t.row_count==5 and t.col_count==TABLES[number]]
            assert len(candidates)==1,(number,len(candidates))
            table=candidates[0]
            record=dict(id=f'table-{number:02}',page=number,bbox=list(table.bbox),rows=table.extract())
            tables.append(record);regions.append((record['bbox'],'table',record['id']))
        units, classifications, pending_bullet = [], [], None
        for line in lines:
            text=line['text'].strip()
            if '2025학년도 2학기 실전웹서비스개발' in text or line['bbox'][1]<20 and line['size']<10:
                role='template'
            elif line['id']==title_line['id']:
                role='title'
            else:
                role=next((kind+':'+ident for bbox,kind,ident in regions if contains(bbox,line['bbox'])), 'prose')
            classifications.append(dict(id=line['id'],role=role,text=line['text']))
            if role!='prose' or not text:
                continue
            if text in ('●','○'):
                pending_bullet=(text,line['block'])
                continue
            bullet=pending_bullet[0] if pending_bullet and pending_bullet[1]==line['block'] else None
            pending_bullet=None
            heading=(line['size']>=13 and all(r['bold'] for r in line['runs'] if r['text'].strip())) or bool(re.match(r'^\d\. ',text))
            if units and not bullet and not heading and units[-1]['block']==line['block'] and not units[-1]['heading']:
                unit=units[-1]
                if not unit['text'].endswith((' ','\n')):
                    unit['text']+=' ';unit['runs'].append(dict(text=' ',bold=False,italic=False,color=0))
                unit['text']+=line['text'];unit['runs']+=line['runs'];unit['line_ids'].append(line['id'])
            else:
                units.append(dict(id=f'p{number:02}-u{len(units)+1:02}',block=line['block'],text=line['text'],runs=line['runs'],bullet=bullet,heading=heading,line_ids=[line['id']]))
        for unit in units:
            line_boxes=[l['bbox'] for l in lines if l['id'] in unit['line_ids']]
            unit['links']=[link['uri'] for link in page.get_links() if link.get('uri') and any(pymupdf.Rect(box).intersects(link['from']) for box in line_boxes)]
        pages.append(dict(number=number,title=title,units=units,assets=assets,codes=codes,tables=tables,classifications=classifications))
        all_assets+=assets;all_codes+=codes
    manifest=dict(source=PDF.name,source_sha256=sha(PDF.read_bytes()),page_count=len(document),
                  format='week-05',semester='2026학년도 2학기',week=6,pages=pages,
                  asset_count=len(all_assets),code_count=len(all_codes))
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (OUT/'text-inventory.txt').write_text('\n\n'.join(f'PAGE {p["number"]:02} {p["title"]}\n'+'\n'.join(f'{u["id"]} [{u["bullet"] or "heading" if u["heading"] else u["bullet"] or "text"}] {u["text"]}' for u in p['units']) for p in pages)+'\n')
    print(f'Prepared {len(pages)} pages, {len(all_assets)} contextual image placements, {len(all_codes)} code samples, {sum(len(p["tables"]) for p in pages)} tables')

if __name__=='__main__':
    main()
