"""Record and verify the source assets actually placed in the Week 9 deck."""
import argparse
import json
from pathlib import Path

from audit_week10_assets import ASSETS, SLIDE_MAP
from lesson import SLIDES
from reused_resources import RESOURCES
from new_resources import RESOURCES as NEW_RESOURCES, describe_resource
from title_outline import proposal


DEFERRED = {
    'I04-test': '1.2는 같은 역할·관찰 관계를 담은 T04 표 선택. 이미지의 단정적 판정 문구·작은 한글 라벨을 그대로 옮기지 않음.',
    'I05-boundary': '1.5의 주자료 I05-unit에 집중. OR/XOR 이름과 분류 경계의 추가 설명이 필요한 보조 후보는 보관.',
    'I09': '2.10에는 I07 포함 관계 선택. 2.8에서 이미 본 연결 구조에 손실 함수·노드 수·RNN 오기까지 추가하지 않음.',
    'T22-errors': '4.9는 I22와 T22-steps를 하나의 반복 도식으로 통합. 오류 유형 표까지 중복 배치하지 않음.',
}

REVIEW = [
    '1.2: 문자 대화에서 역할·판별 기준만 설명. 의식·모든 과제의 능력을 증명한다고 쓰지 않음.',
    '1.5: 두 입력·가중치·합산·임곗값으로 단순화. 단일 계산 단위 이후에 층 연결을 도입하도록 역전파·손실 수식 제외.',
    '1.6: 사용자→인터페이스→추론 엔진, 추론 엔진↔지식 베이스, 추론 엔진→결과→사용자의 원본 연결 보존.',
    '2.1: 개략 시간선임을 명시. 시기를 ML 최초 등장으로 잘못 표현하지 않고 뒤 장의 딥러닝·생성형 AI는 생략.',
    '2.8: 원본의 단일 단위와 2입력·2은닉·1출력 연결을 유지. 역전파의 영향 계산과 혼동할 그림 제외.',
    '2.10: AI·머신러닝·딥러닝을 모두 배운 뒤 포함 관계 배치. 인간 뇌와 같다는 표현 교정.',
    '3.5: 3.2~3.4의 토큰·임베딩·어텐션을 연결. 순서 정보·여러 층 반복은 구조 설명이며 3.9의 생성 반복과 구분.',
    '3.9: 다음 단어를 다음 토큰으로 교정. 토큰 선택→입력에 추가→다시 계산 경로와 종료 조건 명시.',
    '4.6~4.7: 문자열 입력, trim 후 1~20글자, boolean 결과를 같은 조건으로 사용. 퓨샷에만 예시 추가하며 요청 시 가중치 학습으로 설명하지 않음.',
    '4.9: 실행 결과는 실제 프로젝트에서 수행했다고 주장하지 않는 설명용 사례. 개발자가 관찰한 입력·실제값·기대값을 전달하는 범위.',
    '6.3: T21의 구성만 참고해 반복 지침 예시로 작성. 파일의 적용 범위와 실제 실행 권한 구분. 보고 형식 예시는 다음 장의 진행 기록 체계를 먼저 정의하지 않음.',
    '7.3~7.4: 명세·완료 기준 뒤에 구현 순서와 작업 단위를 배치. 새 라이브러리·MCP 설정·병렬화·자동 테스트를 앞당겨 사용하지 않음.',
    '7.7: 테스트·브라우저 검증을 배운 뒤 반복 도식에 포함. 전체 완료 시 종료, 현재 검사 통과 후 남은 작업 진행, 실패 수정 후 재검증의 경로를 구분. Hooks·하네스는 미리 정의하지 않음.',
    '8.10: 원본의 단정적 미래 예측 대신 이미 배운 작업 범위·통합 비용·검증 근거·실행 한도의 판단을 비교.',
    '원본 비트맵/표는 조사 폴더에 그대로 보존. 수업용 도식은 원본 관계를 편집형 HTML/SVG로 재구성. 한글 이미지가 영문 화면에 남지 않도록 모든 표시 문구에 공용 번역 적용.',
    '설명 활용 13장과 대응 없음 47장에는 새 자료 60개를 추가. 메시지 분류→제목 검사→게시글 프로젝트의 공통 사례와 확정한 선수 순서를 유지.',
    '원본 발췌 2개 외에는 네이티브 도식·표·코드 중심으로 구성. 설명용 화면·도구 호출과 실제 실행한 함수·토큰 결과를 구분.',
    '출처는 materials/slide-references.html에 실제 화면 번호별로 기록. 슬라이드 본문과 숨김 노트에는 출처를 삽입하지 않음.',
]


def outputs():
    root = Path(__file__).resolve().parents[1]
    audit = {r['outline_number']:r for r in SLIDE_MAP}
    assets = {a['id']:a for a in ASSETS}
    numbers = {s['id']:i for i,s in enumerate(SLIDES,2)}
    rows = []
    for chapter in proposal()['chapters']:
        for item in chapter['concepts']:
            old = audit[item['outline_number']]
            media = RESOURCES.get(item['id'])
            assert bool(media)==(old['status'] in ('직접 활용','수정 활용','구조 참고')),item['id']
            if media:
                assert set(media['assets'])<=set(old['assets']),item['id']
                assert all(assets[a]['decision']!='제외' for a in media['assets'])
                assert set(media['pages'])<=set(n for a in media['assets'] for n in assets[a]['pages'])
            assert bool(media) != (item['id'] in NEW_RESOURCES),item['id']
            rows.append(dict(outline_number=item['outline_number'],slide_number=numbers[item['id']],
                             id=item['id'],title=item['title'][0],
                             status='기존 자료 배치' if media else '새 자료 배치',
                             origin='reused' if media else 'new',
                             assets=media['assets'] if media else [],pages=media['pages'] if media else [],
                             original_audit_status=old['status'],
                             correction=media['correction'] if media else describe_resource(item['id'])))
    assert len(rows)==76 and sum(bool(r['assets']) for r in rows)==16
    counts={status:sum(bool(r['assets']) and r['original_audit_status']==status for r in rows)
            for status in ['직접 활용','수정 활용','구조 참고']}
    used=sorted({a for r in rows for a in r['assets']})
    data=dict(stage='all-resources-placed',deck_slide_count=85,resource_slide_count=76,
              reused_resource_slide_count=16,new_resource_slide_count=60,
              title_only_slide_count=0,placed_by_audit_status=counts,used_asset_ids=used,
              resource_format='편집형 HTML/SVG 도식·네이티브 표·코드·개별 발췌 이미지·한영 라벨',
              slides=rows,deferred_assets=DEFERRED,content_review=REVIEW)
    lines=['9주차 · 전체 자료 반영 기록','',
           '본문 제목 76장 + 챕터 8장 + 주차 표지 1장 = 한영 전체 85장.',
           '직접 활용 2장·수정 활용 9장·구조 참고 5장, 합계 16개 본문에 자료 배치.',
           '새 자료 60장 추가. 76개 본문 전체에 맥락별 시각 자료·표·코드 배치.',
           '페이지별 출처와 실제 재구성 범위는 slide-references.html에서 관리.',
           '구조 참고 5장은 원본에 완성 자료가 있었던 것이 아니라 원본 구성과 확정 문단을 함께 사용한 적용 예시.',
           '실습 리뷰 덱과 원본 추출 파일은 유지. 현재 예시는 실제 실습 구현·실행 기록을 뜻하지 않음.','',
           '| 설계 번호 | 화면 | 제목 | 상태 | 원본 자료 | 수정·학습 범위 |',
           '| --- | --- | --- | --- | --- | --- |']
    for row in rows:
        lines.append(f'| {row["outline_number"]} | {row["slide_number"]} | {row["title"]} | {row["status"]} | {", ".join(row["assets"])} | {row["correction"]} |')
    lines += ['','보조·대안 자료의 선택','']+[f'- {k}: {v}' for k,v in DEFERRED.items()]
    lines += ['- 조사에서 제외한 자료는 배치하지 않음. 원본 34개 자료의 추출 파일과 제외 이유는 week10-asset-audit/에 보존.',
              '', '내용·학습 순서 검토', '']+['- '+s for s in REVIEW]
    lines += ['','제작 원본: scripts/reused_resources.py · scripts/new_resources.py · scripts/resource_blocks.py · resources.css',
              '구성 원본: scripts/chapters.py · scripts/title_outline.py · scripts/lesson.py',
              '생성: python3 lectures/09/scripts/build-slides.py',
              '기록 검증: python3 lectures/09/scripts/resource_placements.py --check']
    return {root/'materials/resource-placements.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n',
            root/'materials/resource-placements.ko.txt':'\n'.join(lines)+'\n'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for path,content in outputs().items():
        if args.check:
            assert path.read_text()==content,f'Stale {path}'
        else:
            path.write_text(content)
    print('Week 9 resources: 16 reused + 60 new = 76 content slides, 85 total slides.')
