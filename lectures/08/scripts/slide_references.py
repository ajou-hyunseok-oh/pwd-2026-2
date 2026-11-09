"""Generate a separate page-by-page reference document for all 60 content slides."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote

from lesson import SLIDES
from new_resources import RESOURCES as NEW
from research_new_resources import ROWS, SOURCES
from reused_resources import RESOURCES as REUSED, PDF
from title_outline import proposal
from chapter03_content import SOURCES as CHAPTER3_SOURCES
from chapter04_content import SOURCES as CHAPTER4_SOURCES
from chapter05_content import SOURCES as CHAPTER5_SOURCES
from chapter06_content import SOURCES as CHAPTER6_SOURCES

ROOT = Path(__file__).resolve().parents[1]


def outputs():
    numbers = {s['id']: n for n, s in enumerate(SLIDES, 2)}
    research = {r['outline_number']: r for r in ROWS}
    sources = {s['id']: s for s in SOURCES}
    rows = []
    for chapter in proposal()['chapters']:
        for s in chapter['concepts']:
            ident = s['id']
            refs = []
            if chapter['number'] in (3,4,5,6):
                refs = [dict(label=label, url=url, type='official-document', use='초심자 실습 흐름과 용어 검토') for label, url in {3:CHAPTER3_SOURCES,4:CHAPTER4_SOURCES,5:CHAPTER5_SOURCES,6:CHAPTER6_SOURCES}[chapter['number']]]
                adaptation = s['example']
                origin = '실제 8주차 프로젝트 코드와 공식 문서 기반'
                assets = [f'chapter{chapter["number"]:02}_content.py']
            elif ident in REUSED:
                resource = REUSED[ident]
                for page in resource['pages']:
                    refs.append(dict(label=f'PWD Week6 원본 PDF · {page}쪽',
                                     url=quote(PDF)+'#page='+str(page),
                                     type='local-pdf', use='원본 요소의 재사용·수정'))
                for url in resource['sources'][1:]:
                    refs.append(dict(label=url, url=url, type='official-document',
                                     use='원본의 기술 내용 검토·수정 근거'))
                adaptation = resource['correction']
                origin = '기존 PDF 자료 수정·재사용'
                assets = resource['assets']
            else:
                assert ident in NEW
                source_number = f"{chapter.get('source_number', chapter['number'])}.{s['outline_number'].split('.')[1]}"
                r = research[source_number]
                for sid in r['source_ids']:
                    src = sources[sid]
                    refs.append(dict(label=src['title'], url=src['url'], type='official-document',
                                     section=src['section'], use=src['use']))
                for filename in r['figure_files']:
                    refs.append(dict(label='보관한 도식 원본 · '+filename,
                                     url='new-resource-research/reference-figures/'+filename,
                                     type='archived-figure', use='배치·흐름 참조. 강의에는 한영 편집 가능한 도식으로 재구성'))
                adaptation = r['specification']+' '+r['reuse_plan']
                origin = '공식 문서 기반의 FoodMap 강의용 재구성'
                assets = [r['candidate']]
            rows.append(dict(slide_number=numbers[ident], outline_number=s['outline_number'],
                             id=ident, title=s['title'][0], chapter=chapter['number'],
                             origin=origin, assets=assets, adaptation=adaptation, references=refs))
    assert len(rows) == 37 and all(r['references'] for r in rows)
    assert all(not s.get('sources') and not s.get('note') for s in SLIDES)
    for r in rows:
        for ref in r['references']:
            assert ref['url'].startswith(('https://', quote(PDF), 'new-resource-research/'))
    data = dict(updated_on='2026-11-07', numbering='표지·챕터 표지를 포함한 실제 화면의 1부터 시작하는 번호',
                slide_count=44, content_count=37, reference_location='이 문서만 사용. 슬라이드 본문·숨김 노트에 출처 없음.', slides=rows)
    intro = ['8주차 · 페이지별 자료 레퍼런스', '',
             '표지·챕터 표지를 포함한 화면 번호 기준. 설계 번호(예: 4.6)를 함께 표시.',
             '본문 37장의 자료 출처와 수정 내용을 기록. 표지 1장과 챕터 표지 6장은 별도 외부 자료 없음.',
             'FoodMap 데이터·화면·정책·관측값은 강의용 사례이며 원문 자료의 실제 화면·측정 결과가 아님.',
             '레퍼런스는 이 문서에서 관리하며 슬라이드 화면과 숨김 노트에는 삽입하지 않음.', '']
    lines = list(intro)
    e = html.escape
    sections = []
    for r in rows:
        heading = f'{r["slide_number"]}페이지 · {r["outline_number"]} · {r["title"]}'
        lines += [heading, f'자료 유형: {r["origin"]}', f'자료: {", ".join(r["assets"])}',
                  f'수정·적용: {r["adaptation"]}']
        refs = []
        for ref in r['references']:
            lines += [f'- {ref["label"]}: {ref["url"]}', f'  적용 근거: {ref.get("section", ref["use"])}']
            refs.append('<li><a href="'+e(ref['url'], quote=True)+'">'+e(ref['label'])+'</a><p>'+e(ref.get('section', ref['use']))+'</p></li>')
        lines.append('')
        sections.append(f'<section id="page-{r["slide_number"]}"><h2>{e(heading)}</h2><p class="origin">{e(r["origin"])}</p>'+
                        f'<p><strong>자료:</strong> {e(", ".join(r["assets"]))}</p><p><strong>수정·적용:</strong> {e(r["adaptation"])}</p>'+
                        '<ul>'+''.join(refs)+'</ul></section>')
    toc = ''.join(f'<a href="#page-{r["slide_number"]}">{r["slide_number"]}. {e(r["title"])}</a>' for r in rows)
    markup = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>8주차 · 페이지별 자료 레퍼런스</title>
<style>
body{font-family:system-ui,sans-serif;line-height:1.7;color:#243c30;background:#f8f7f3;margin:0;padding:2rem}
main{max-width:1050px;margin:auto}h1{font-size:2rem}h2{font-size:1.25rem;margin:0 0 .6rem}
a{color:#205e42;text-underline-offset:.2em;overflow-wrap:anywhere}nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem 1.4rem;margin:2rem 0;font-size:.9rem}
section{border-top:1px solid #bccac0;padding:1.5rem 0;scroll-margin-top:1rem}p{margin:.5rem 0}.origin,li p{color:#56665c;font-size:.9rem}li{margin:.6rem 0}
@media(max-width:700px){body{padding:1.2rem}nav{grid-template-columns:1fr}}@media print{nav{display:none}section{break-inside:avoid}a{color:inherit}}
</style></head><body><main>'''+f'<h1>{e(intro[0])}</h1>'+''.join('<p>'+e(s)+'</p>' for s in intro[2:] if s)+\
        '<nav aria-label="페이지별 목차">'+toc+'</nav>'+''.join(sections)+'</main></body></html>\n'
    return {
        ROOT/'materials/slide-references.json': json.dumps(data, ensure_ascii=False, indent=2)+'\n',
        ROOT/'materials/slide-references.ko.txt': '\n'.join(lines)+'\n',
        ROOT/'materials/slide-references.html': markup,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in outputs().items():
        if args.check:
            assert path.read_text() == content, f'Stale {path}'
        else:
            path.write_text(content)
    print('Week 8 references: 37 content pages, sources separated from deck HTML and notes.')
