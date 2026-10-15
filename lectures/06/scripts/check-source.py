"""Verify PDF content coverage and Week 05 formatting without fixing page geometry."""
import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'materials/elements'
def norm(value):return re.sub(r'\s+','',value)
class Content(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.depth=0;self.active=[];self.units=[];self.codes=[];self.assets=[];self.links=[];self.tables={};self.table=None;self.cell=None;self.page=None;self.titles=[];self.title=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='section':self.page=int(a['data-source-page'])
        if tag not in ('img','meta','link','br','input','hr'):self.depth+=1
        if 'data-source-unit' in a:
            row=dict(id=a['data-source-unit'],page=self.page,text='',depth=self.depth);self.units.append(row);self.active.append(row)
        if 'data-source-code' in a:
            row=dict(id=a['data-source-code'],page=self.page,text='',depth=self.depth);self.codes.append(row);self.active.append(row)
        if 'data-source-asset' in a:self.assets.append(dict(id=a['data-source-asset'],page=self.page,src=a['src']))
        if 'data-source-link' in a:self.links.append((self.page,a['href']))
        if 'data-source-table' in a:self.table=a['data-source-table'];self.tables[self.table]=[]
        if self.table and tag=='tr':self.tables[self.table].append([])
        if self.table and tag in ('th','td'):self.cell=[]
        if tag in ('h1','h2'):self.title=dict(page=self.page,text='');self.titles.append(self.title)
    def handle_endtag(self,tag):
        if tag in ('h1','h2'):self.title=None
        if self.table and tag in ('th','td') and self.cell is not None:
            self.tables[self.table][-1].append(''.join(self.cell));self.cell=None
        if tag=='table':self.table=None
        self.active=[r for r in self.active if r['depth']!=self.depth]
        self.depth-=1
    def handle_data(self,data):
        for row in self.active:row['text']+=data
        if self.cell is not None:self.cell.append(data)
        if self.title is not None:self.title['text']+=data

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--pdf',action='store_true');args=parser.parse_args()
    m=json.loads((OUT/'manifest.json').read_text());pdf=ROOT/'materials'/m['source']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['source_sha256']
    markup=(ROOT/'index.html').read_text();parsed=Content();parsed.feed(markup)
    assert 'data-wd-format="week-05"' in markup and 'packages/web-deck/authoring.css' in markup
    assert 'wd-source-canvas' not in markup and '<svg' not in markup,'Whole PDF page rendering is not a Week 05 layout'
    assert '2026학년도 2학기 실전웹서비스개발' in markup and '실전 웹서비스개발 – 6주차' in markup and 'LECTURE 06' in markup
    expected_units={u['id']:(p['number'],u) for p in m['pages'] for u in p['units']}
    counts=Counter(u['id'] for u in parsed.units)
    assert set(counts)==set(expected_units),('Missing or extra source text',set(expected_units)-set(counts),set(counts)-set(expected_units))
    assert all(c==1 for c in counts.values()),('Duplicated source text',counts)
    for shown in parsed.units:
        page,u=expected_units[shown['id']]
        assert shown['page']==page and norm(shown['text'])==norm(u['text']),(shown['id'],'Source text changed')
    expected_assets={(p['number'],a['id']):a for p in m['pages'] for a in p['assets']}
    assert Counter((a['page'],a['id']) for a in parsed.assets)==Counter({key:1 for key in expected_assets})
    for shown in parsed.assets:
        source=expected_assets[(shown['page'],shown['id'])];file=OUT/source['file']
        assert hashlib.sha256(file.read_bytes()).hexdigest()==source['sha256']
        assert shown['src']=='materials/elements/'+source['file']
    expected_codes={c['id']:c for p in m['pages'] for c in p['codes']}
    assert Counter(c['id'] for c in parsed.codes)==Counter({key:1 for key in expected_codes})
    for shown in parsed.codes:
        source=expected_codes[shown['id']]
        assert shown['page']==source['page'] and shown['text']==source['code'],shown['id']
        assert hashlib.sha256((OUT/source['file']).read_bytes()).hexdigest()==source['sha256']
    expected_tables={t['id']:t for p in m['pages'] for t in p['tables']}
    assert set(parsed.tables)==set(expected_tables)
    for ident,table in expected_tables.items():
        assert [[norm(v) for v in row] for row in parsed.tables[ident]]==[[norm(v) for v in row] for row in table['rows']],ident
    assert Counter(parsed.links)==Counter((p['number'],url) for p in m['pages'] for u in p['units'] for url in u['links'])
    for source,title in zip(m['pages'],parsed.titles):
        expected='실전 웹서비스개발 – 6주차' if source['number']==1 else source['title']
        assert title['page']==source['number'] and title['text']==expected
    assert len(parsed.titles)==m['page_count']
    if args.pdf:
        import pymupdf
        document=pymupdf.open(pdf)
        inventory=json.loads((ROOT/'materials/source-analysis/manifest.json').read_text())
        for record,page,original in zip(m['pages'],document,inventory['pages']):
            actual={}
            for bi,block in enumerate(page.get_text('dict')['blocks']):
                if block['type']==0:
                    for li,line in enumerate(block['lines']):actual[f'p{record["number"]:02}-b{bi:02}-l{li:02}']=''.join(s['text'] for s in line['spans'])
            assert {c['id']:c['text'] for c in record['classifications']}==actual
            covered=[ident for u in record['units'] for ident in u['line_ids']]
            prose=[c['id'] for c in record['classifications'] if c['role']=='prose' and c['text'].strip() not in ('●','○','')]
            assert Counter(covered)==Counter(prose)
            for unit in record['units']:
                assert norm(unit['text'])==norm(''.join(actual[ident] for ident in unit['line_ids'])),unit['id']
            for code in record['codes']:
                assert norm(code['code'])==norm(''.join(actual[ident] for ident in code['line_ids'])),code['id']
            for table in record['tables']:
                actual_tables=[t for t in page.find_tables().tables if t.row_count==len(table['rows']) and t.col_count==len(table['rows'][0])]
                assert any(t.extract()==table['rows'] for t in actual_tables),table['id']
            regions=[a['bbox'] for a in record['assets']]
            for image in original['image_occurrences']:
                if image['id']=='ajou-footer':continue # Week 05 cover/chrome replaces the PDF's repeated footer.
                center=pymupdf.Rect(image['bbox_pt']).tl+(pymupdf.Rect(image['bbox_pt']).br-pymupdf.Rect(image['bbox_pt']).tl)*.5
                assert any(pymupdf.Rect(r).contains(center) for r in regions),(record['number'],image['id'],'Unplaced source image')
    subprocess.run([sys.executable,str(ROOT/'scripts/build-slides.py'),'--check'],check=True)
    print(f'Source + format: {m["page_count"]} original-title slides, {len(expected_units)} text units, {len(expected_assets)} contextual images, {len(expected_codes)} original code blocks, {len(expected_tables)} complete tables; Week 05 format and 2026/06 cover checked')
if __name__=='__main__':main()
