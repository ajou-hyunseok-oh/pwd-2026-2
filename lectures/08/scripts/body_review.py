"""Export the completed prose next to its approved paragraph and prerequisites."""
import argparse
import json
from pathlib import Path

from lesson import SLIDES
from paragraph_outline import document
from slide_body import BODY


def outputs():
    root = Path(__file__).resolve().parents[1]
    slides = {slide['id']: (number, slide) for number, slide in enumerate(SLIDES, 2)}
    rows = []
    lines = ['8주차 · 완성 본문과 문단 대응', '',
             '본문 60장 · 한영 정의와 글머리표 · 기존 자료 16장 + 신규 자료 44장.',
             '확정 문단과 선수 개념은 보존하고 설명·자료의 배치를 슬라이드별로 구성.',
             '출처: slide-references.html · 화면 검토: body-layout-review.json', '']
    seen = set()
    for chapter in document()['chapters']:
        for item in chapter['slides']:
            ident = item['id']
            number, slide = slides[ident]
            assert all(req.startswith('prior-') or req in seen for req in item['requires']), ident
            seen.add(ident)
            groups = BODY[ident]['explanation']['items']
            assert groups and all(g['details'] for g in groups), ident
            assert any(b['kind'] == 'concepts' for col in slide['columns'] for b in col), ident
            assert any(b['kind'] != 'concepts' for col in slide['columns'] for b in col), ident
            assert not slide.get('sources') and not slide.get('note'), ident
            row = dict(slide_number=number, outline_number=item['outline_number'], id=ident,
                       title=item['title'], requires=item['requires'],
                       approved_paragraph_ko=item['paragraph_ko'],
                       body_groups=groups, composition=BODY[ident]['layout'],
                       resource_blocks=[[b['kind'] for b in col if b['kind'] != 'concepts']
                                        for col in slide['columns']])
            rows.append(row)
            lines += [f'{number}페이지 · {item["outline_number"]} · {item["title"][0]}',
                      '확정 문단: ' + item['paragraph_ko'], '', '발표용 본문:']
            for group in groups:
                lines.append(group['term'][0])
                lines.extend('  • ' + detail[0] for detail in group['details'])
            lines += ['', '자료 배치: ' + row['composition'], '']
    assert len(rows) == len(BODY) == 60
    data = dict(stage='completed-bilingual-bodies', slide_count=68, content_count=60,
                languages=['ko', 'en'], references='slide-references.html',
                review='body-layout-review.json', slides=rows)
    return {root/'materials/slide-bodies.json': json.dumps(data, ensure_ascii=False, indent=2)+'\n',
            root/'materials/week-08-body.ko.txt': '\n'.join(lines)+'\n'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in outputs().items():
        if args.check:
            assert path.read_text() == content, f'Stale {path}'
        else:
            path.write_text(content)
    print('Week 8 bodies: 60 bilingual explanations with resources and approved prerequisites.')
