"""Record the exact source-to-slide placement and adaptation decisions."""
import argparse
import json
from pathlib import Path

from audit_week6_assets import ASSETS, SLIDE_MAP
from lesson import SLIDES
from reused_resources import RESOURCES
from new_resources import RESOURCES as NEW_RESOURCES
from title_outline import proposal


def outputs():
    root = Path(__file__).resolve().parents[1]
    audit = {row['outline_number']: row for row in SLIDE_MAP}
    assets = {item['id']: item for item in ASSETS}
    numbers = {item['id']: i for i, item in enumerate(SLIDES, 2)}
    rows = []
    for chapter in proposal()['chapters']:
        for item in chapter['concepts']:
            number = item['outline_number']
            legacy = {'identity-provider':'3.1','oauth-delegation':'3.2','authorization-code':'3.4','account-link':'3.7','social-session':'3.8','api-access':'4.5','api-keys':'4.7','workflow-state':'5.3','approval-flow':'5.2','admin-transaction':'5.5','idempotency':'5.6','environments':'7.1','environment-config':'7.2','deployment':'7.5','deployment-urls':'7.2','monitoring':'7.7'}
            source_number = f"{chapter.get('source_number', chapter['number'])}.{number.split('.')[1]}"
            source = audit[legacy.get(item['id'], source_number)]
            media = RESOURCES.get(item['id'])
            new_media = NEW_RESOURCES.get(item['id'])
            assert bool(media) != bool(new_media), item['id']
            expected = chapter['number'] != 6 and source['status'] in ('직접 활용', '수정 활용')
            assert bool(media) == expected, number
            if media:
                assert set(media['assets']) <= set(source['assets']), number
                assert all(assets[ident]['decision'] not in ('제외', '보류') for ident in media['assets'])
            rows.append(dict(outline_number=number, slide_number=numbers[item['id']], id=item['id'],
                             title=item['title'][0], status='기존 PDF 자료 배치' if media else '신규 자료 배치',
                             assets=media['assets'] if media else [],
                             pages=media['pages'] if media else [],
                             correction=media['correction'] if media else '신규 조사에 따른 편집 가능한 자료 배치. 자료·출처는 slide-references.html 참조.',
                             original_audit_status=source['status']))
    assert len(rows) == 37 and sum(bool(row['assets']) for row in rows) == 12
    assert len(NEW_RESOURCES) == 25 and not RESOURCES.keys() & NEW_RESOURCES.keys()
    data = dict(stage='completed-bodies-and-resources', deck_slide_count=44,
                resource_slide_count=37, reused_resource_slide_count=12, new_resource_slide_count=25,
                title_only_slide_count=0, reference_document='slide-references.html', slides=rows,
                deferred_assets={'I13': 'I11 시퀀스와 C13 객체를 2.3의 주자료로 선택. 저장 위치 그림은 중복을 피하기 위해 대안으로 보관.',
                                 'C15-signature': '학습 순서와 개념 범위에 따라 조사 시 보류한 수식.'})
    lines = ['8주차 · 전체 자료 반영 기록', '',
             '확정한 본문 제목 37장 + 표지 1장 + 챕터 6장 = 전체 44장.',
             '기존 PDF 계보 12장 + 신규 자료 25장 = 본문 37장 모두 자료 배치.',
             '페이지별 출처: slide-references.html · 슬라이드 본문과 숨김 노트에는 출처를 삽입하지 않음.',
             '확정 문단에 따른 설명 본문 작성 완료. 문단·본문 대응은 slide-bodies.json, 화면 검토는 body-layout-review.json 참조.',
             '시퀀스와 로그인 화면은 원본 요소·흐름을 편집 가능한 HTML로 재구성. 코드·표는 네이티브 텍스트.',
             '원본 전체 이미지를 유지한 자료: I06 인증/인가, I15 JWT 세 부분. 나머지 원본 추출본도 조사 폴더에 그대로 보존.',
             '보류: I13 저장 위치 그림은 I11 시퀀스의 대안. I04/I05/I07/I08과 C15-signature는 조사 판단대로 미사용.', '',
             '| 설계 번호 | 화면 | 제목 | 상태 | 원본 애셋 | 수정·학습 범위 |',
             '| --- | --- | --- | --- | --- | --- |']
    for row in rows:
        lines.append(f'| {row["outline_number"]} | {row["slide_number"]} | {row["title"]} | {row["status"]} | {", ".join(row["assets"])} | {row["correction"]} |')
    lines += ['', '내용 검토', '',
              '- 1.4에서 외부 로그인 버튼을 제거하고 3.1에 배치. 원본 이메일은 예시 값으로 교체.',
              '- 1.7의 해시·솔트는 1.5~1.6 이후. 세션 기억 단계는 제외.',
              '- 2.2에는 쿠키 전달만, 2.3에는 서버 세션 조회만. role·보호 속성·환경 분기 제외.',
              '- 2.4 일반 토큰 → 2.6 구조 → 2.7 JWT 검증. 같은 원본 시퀀스에 학습한 검증 항목 추가.',
              '- 챕터 3: 용어와 책임 분리 → OAuth/OIDC → SDK 로그인·복귀 → 같은 UUID의 프로필 → 토큰 첨부 API 요청.',
              '- OAuth 도식은 단계별 개념 자료이며 배포용 전체 보안 구현이 아님. 클라이언트 인증 등 구현 세부는 실습 범위.',
              '- 6.9 SameSite는 출처·사이트·CSRF 이후. 7.2에서만 환경 설정 코드 사용.',
              '- 임의 placeholder를 실제 토큰·비밀키라고 제시하지 않음. ID 토큰은 OIDC 조건부, PKCE는 S256 변환·제공자 비교 명시.',
              '- 신규 계보 자료: 같은 사용자·제보·URL·환경을 이어 사용. 선수 개념과 예시 범위는 신규 조사에 기록.',
              '- 활성 코드 예시: 입력 검증·매개변수 쿼리·React 텍스트 출력·DB 열 추가. RLS 정책 SQL은 보충 자료로 분리.',
              '- DB/인증 연동 코드는 이론용 발췌. 실제 서비스와 운영 DB를 변경하지 않음.',
              '', '제작 원본: scripts/slide_body.py · scripts/reused_resources.py · scripts/new_resources.py · scripts/resource_blocks.py · resources.css · body.css',
              '생성: python3 lectures/08/scripts/build-slides.py',
              '기록 검증: python3 lectures/08/scripts/resource_placements.py --check']
    return {
        root/'materials/resource-placements.json': json.dumps(data, ensure_ascii=False, indent=2)+'\n',
        root/'materials/resource-placements.ko.txt': '\n'.join(lines)+'\n',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, text in outputs().items():
        if args.check:
            assert path.read_text() == text, f'Stale {path}'
        else:
            path.write_text(text)
    print('Week 8 resources: 12 reused + 25 new = 37 content slides, 44 total slides.')
