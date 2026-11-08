"""Export page-by-page references outside the Week 9 lecture and its notes."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote

from lesson import SLIDES
from new_resources import RESOURCES as NEW, describe_resource
from reused_resources import RESOURCES as REUSED, PDF
from research_new_resources import PLANS, SOURCES
from title_outline import proposal

ROOT = Path(__file__).resolve().parents[1]

ADAPTATIONS = {
    'alexnet': 'Figure 4 왼쪽의 표범 사례 하나를 발췌. 사진·정답·상위 5개 라벨·확률 막대를 유지하고 한영 후보 명칭을 별도 표로 추가. 확률 수치는 새로 만들지 않음. 원본 그림의 데이터는 ILSVRC-2010; 논문 발표 연도는 2012.',
    'dartmouth': 'PDF 1쪽 제목·작성자·날짜 부분만 발췌. 1955년 제안과 1956년 모임을 네이티브 흐름으로 구분. 페이지 전체는 사용하지 않음.',
    'backpropagation': '2.8에서 배운 층 연결을 역할별 상자로 단순화하고 역방향의 영향 계산을 추가. 역전파와 별도 가중치 갱신을 구분.',
    'multimodal-models': '오류 메시지 일부가 보이는 설명용 화면과 CSS 발췌. 실제 서비스·제품 캡처나 모델의 실제 진단 결과가 아님.',
    'computer-use': '게시글 화면의 편집 가능한 모식도와 관찰·행동·확인 절차. 실제 제품 화면이나 실행 기록이 아님.',
    'browser-verification': 'page/expect 및 실행 중인 예제 앱을 전제로 하는 Playwright 발췌. 저장소의 실제 게시글 서비스 구현·DB 검증 완료를 뜻하지 않음. 요청·응답·저장 확인 범위를 표로 분리.',
    'git-worktrees': '폴더·브랜치 관계와 명령을 제시. 현재 저장소에서는 이 명령을 실행하지 않았으며 실제 사용 시 기존 커밋·겹치지 않는 브랜치/경로 필요.',
}


def outputs():
    concepts = {s['id']: (c['number'],s) for c in proposal()['chapters'] for s in c['concepts']}
    all_slides = [dict(id='cover',kind='cover',title=('9주차 표지','Week 9 cover')),*SLIDES]
    rows = []
    for number, slide in enumerate(all_slides,1):
        ident = slide['id']
        refs, artifacts = [], []
        row = dict(slide_number=number,id=ident,kind=slide['kind'],title=slide['title'][0],
                   slide_link='../index.html#/'+str(number),outline_number=None,
                   origin='외부 자료 없음',adaptation='주차·챕터의 제목과 범위',references=refs,assets=artifacts)
        if ident in concepts:
            chapter,s = concepts[ident]
            row.update(chapter=chapter,outline_number=s['outline_number'])
            if ident in REUSED:
                resource = REUSED[ident]
                refs += [dict(label=f'PWD Week10 원본 PDF · {page}쪽',url=quote(PDF)+'#page='+str(page),
                              type='local-pdf',section='원본 요소 재사용·수정',use=resource['correction']) for page in resource['pages']]
                refs += [dict(label=url,url=url,type='official-document',section='내용 검토·수정 근거',use='보완 근거')
                         for url in resource['sources'][1:] if url.startswith('https://')]
                artifacts += resource['assets']
                row.update(origin='기존 PDF 자료 재사용·수정',adaptation=resource['correction'])
            else:
                assert ident in NEW
                p = PLANS[s['outline_number']]
                for sid in p['source_ids']:
                    src = SOURCES[sid]
                    refs.append(dict(label=src['label'],url=src['url'],type=src['kind'],
                                     section=src['locator'],use=src['finding'],checked_on=src['checked_on']))
                for rel in p['local_files']:
                    refs.append(dict(label='공통 예제 · '+Path(rel).name,
                                     url='new-resource-research/'+rel,type='local-example',
                                     section='실행 가능한 코드·실측 출력 또는 명시된 설명용 발췌',use='게시글 제목 공통 사례'))
                artifacts.append(describe_resource(ident))
                row.update(origin='공식 자료를 참고한 강의용 재구성',
                           adaptation=ADAPTATIONS.get(ident,describe_resource(ident))+' '+p['learning_guard_ko'])
            row['body_resource_status'] = '배치 완료'
            assert refs
        rows.append(row)
    assert len(rows)==85 and sum(r['kind']=='content' for r in rows)==76
    assert all(not s.get('sources') and not s.get('note') for s in SLIDES)
    extracted=json.loads((ROOT/'materials/new-resource-research/extracted-assets.json').read_text())
    for item in extracted:
        ident='dartmouth' if 'dartmouth' in item['file'] else 'alexnet'
        row=next(r for r in rows if r['id']==ident)
        row['extracted_asset']=item
        row['references'].append(dict(label='슬라이드에 배치한 개별 발췌 이미지',url='../'+item['file'],
                                     type='local-image',section=f'PDF {item["pdf_page"]}쪽의 지정 영역 발췌',use=item['transformation']))
    data=dict(updated_on='2026-11-07',slide_count=85,content_count=76,
              reused_resource_count=16,new_resource_count=60,
              numbering='표지·챕터를 포함한 실제 화면의 1부터 시작하는 페이지 번호',
              source_location='이 문서에서만 관리. 강의 본문·숨김 노트에는 출처 없음.',slides=rows)
    intro=['9주차 · 페이지별 자료 레퍼런스',
           '표지·챕터 표지를 포함한 실제 화면 번호 기준. 설계 번호를 함께 표시.',
           '본문 76장: 기존 PDF 재사용 16장 + 새 자료 60장. 표지 9장은 외부 자료 없음.',
           '원본 발췌, 개념을 참고한 재작성, 설명용 화면, 실제 코드 실행값을 각 페이지에 구분.',
           '레퍼런스 링크와 수정 기록은 이 문서에서 관리하며 강의 본문과 숨김 노트에는 삽입하지 않음.']
    e=html.escape
    lines=[intro[0],'',*intro[1:],'']
    sections=[]
    for r in rows:
        heading=f'{r["slide_number"]}페이지 · '+(r['outline_number']+' · ' if r['outline_number'] else '')+r['title']
        lines += [heading,'자료 유형: '+r['origin'],'수정·적용: '+r['adaptation']]
        links=[]
        for ref in r['references']:
            lines += ['- '+ref['label']+': '+ref['url'],'  확인 위치: '+ref['section']]
            links.append('<li><a href="'+e(ref['url'],quote=True)+'">'+e(ref['label'])+'</a><p>'+e(ref['section'])+'</p></li>')
        lines.append('')
        sections.append(f'<section id="page-{r["slide_number"]}" data-kind="{r["kind"]}"><h2><a href="{r["slide_link"]}">{e(heading)}</a></h2><p class="origin">{e(r["origin"])}</p><p>{e(r["adaptation"])}</p><ul>'+''.join(links)+'</ul></section>')
    toc=''.join(f'<a href="#page-{r["slide_number"]}">{r["slide_number"]}. {e(r["title"])}</a>' for r in rows)
    markup='''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>9주차 · 페이지별 자료 레퍼런스</title>
<style>
body{font-family:system-ui,sans-serif;line-height:1.7;color:#243c30;background:#f8f7f3;margin:0;padding:2rem}
main{max-width:1050px;margin:auto}h1{font-size:2rem}h2{font-size:1.25rem;margin:0 0 .6rem}
a{color:#205e42;text-underline-offset:.2em;overflow-wrap:anywhere}nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem 1.4rem;margin:2rem 0;font-size:.9rem}
section{border-top:1px solid #bccac0;padding:1.5rem 0;scroll-margin-top:1rem}p{margin:.5rem 0}.origin,li p{color:#56665c;font-size:.9rem}li{margin:.6rem 0}
section[data-kind="cover"],section[data-kind="chapter"]{background:#eef3ee;padding:1rem}
@media(max-width:700px){body{padding:1.2rem}nav{grid-template-columns:1fr}}@media print{nav{display:none}section{break-inside:avoid}a{color:inherit}}
</style></head><body><main>'''+f'<h1>{e(intro[0])}</h1>'+''.join('<p>'+e(s)+'</p>' for s in intro[1:])+\
        '<nav aria-label="페이지별 목차">'+toc+'</nav>'+''.join(sections)+'</main></body></html>\n'
    return {ROOT/'materials/slide-references.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n',
            ROOT/'materials/slide-references.ko.txt':'\n'.join(lines)+'\n',
            ROOT/'materials/slide-references.html':markup}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for path,value in outputs().items():
        if args.check:
            assert path.read_text()==value,f'Stale {path}'
        else:
            path.write_text(value)
    print('Week 9 references: 85 pages; 76 content resources; no in-slide sources.')
