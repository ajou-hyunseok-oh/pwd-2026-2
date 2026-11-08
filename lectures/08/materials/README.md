# 08회차 — 웹 서비스 인증과 보안

- [8주차 강의](../index.html): 2026학년도 2학기·8주차 표지 1장, 챕터 표지 7장, 설명·자료를 완성한 본문 60장, 총 68장. KO/EN 지원
- [7주차 실습 리뷰](../lab-review/index.html): `pwd-week7` README의 개발 흐름에 맞춘 한·영 16장. DB 준비 → 코드 구현 → 연결 검증 → 영구 저장 → React 연동 순서. [구성·재생성·검증](../lab-review/materials/README.md)
- 본문 60장 작성 완료. 확정 문단을 `개념 - 짧은 정의`와 세부 글머리표로 구성하고, 기존 PDF 활용 16장·신규 자료 44장의 도식·표·코드·화면 예시와 함께 배치. 개념 설명 → 관계·조건 → 사례의 흐름을 유지
- [챕터 내부 제목·서브타이틀 설계안](week-08-titles.ko.txt): 확정한 본문 60장의 선수 개념 위치와 FoodMap 연결 사례. 1.1 등의 설계 번호와 실제 화면 번호는 구분
- 제목 설계 원본: `../scripts/title_outline.py` · [한영 제목 및 선수 관계](title-outline.json). `python3 lectures/08/scripts/title_outline.py`로 검토 자료 생성, `--check`로 재생성 일치 확인
- [슬라이드별 한 문단 원고와 흐름 평가](week-08-paragraphs.ko.txt): 60장 각각의 한국어 검토 문단, 챕터별 연결 평가와 선행 개념 점검 기록. 완성 본문과의 대응은 아래 본문 원고에서 확인
- [완성 본문 원고](week-08-body.ko.txt) · [한영 본문·확정 문단·선수 관계 대응](slide-bodies.json): 60장 각각의 정의·세부 설명과 자료 배치. 원본은 `../scripts/slide_body.py`; `python3 lectures/08/scripts/body_review.py --check`로 본문 대응·자료 동반·선수 순서·기록 일치 확인
- 문단 원본: `../scripts/paragraph_outline.py` · [구조화된 문단과 검토 기록](paragraph-outline.json). `python3 lectures/08/scripts/paragraph_outline.py`로 생성, `--check`로 제목 대응·순서·단일 문단 형식·재생성 일치 확인
- [PWD Week6 기존 애셋 재사용 조사](week6-asset-audit/reuse-review.ko.txt): PDF 31쪽의 이미지·도식·코드·표와 현재 60장의 대응, 수정 조건, 학습 순서 점검. [구조화된 조사 결과](week6-asset-audit/audit.json)
- [원본 요소 추출본](week6-asset-audit/source-assets/): 로고 제외 이미지 13개, 독립 코드 영역 2개, 인라인 코드·식 4개, 표 3개. 원본 오류·잘림을 보존한 검토용 자료. 수업용 수정은 원본 추출 파일을 덮어쓰지 않고 별도 작성 원본에서 처리. [추출 이력·표 셀·원문 기록](week6-asset-audit/extraction.json)
- 조사 원본: `../scripts/audit_week6_assets.py`. `python3 lectures/08/scripts/audit_week6_assets.py --check`로 대응·원본/추출본 해시·보고서 일치 확인. 재추출은 PyMuPDF가 설치된 Python으로 같은 스크립트에 `--extract` 지정
- [전체 자료 반영 기록](resource-placements.ko.txt) · [구조화된 대응](resource-placements.json): 기존 PDF 활용 16장과 신규 44장 각각의 화면 번호·자료 반영 상태·수정 내용
- [페이지별 레퍼런스 문서](slide-references.html) · [텍스트](slide-references.ko.txt) · [구조화된 레퍼런스](slide-references.json): 본문 60장 각각의 화면 번호·설계 번호·자료 설명·원본 PDF 페이지·공식 문서 링크. 출처는 슬라이드 본문과 숨김 노트에 넣지 않고 이 문서에서 관리
- 레퍼런스 원본: `../scripts/slide_references.py`. `python3 lectures/08/scripts/slide_references.py --check`로 페이지 대응·자료 출처·재생성 일치 확인
- [44장 신규 자료 조사](new-resource-research/research.ko.txt) · [구조화된 조사](new-resource-research/research.json): 공식 문서 31개를 바탕으로 슬라이드별 도식·표·화면·코드 후보, 선수 개념, 수정 범위, 제작 우선순위 정리. 2026-11-07 조사 후 현재 강의에 반영
- [코드 후보 5개](new-resource-research/code-candidates.ko.txt): RLS SELECT·서버 입력 검증·매개변수 쿼리·React 텍스트 출력·DB 열 추가. 실행 전제와 예상 결과를 함께 기록한 이론용 발췌
- [외부 도식 원본 3개](new-resource-research/reference-figures/): MDN CORS 2개와 Supabase 환경 분리 1개. 원본 수정 없이 보관. 강의에는 필수 관계를 한영 HTML 도식으로 재구성하고 불필요한 헤더·Git 브랜치 흐름 제거. [출처·해시](new-resource-research/reference-figures/sources.json)
- 신규 조사 원본: `../scripts/research_new_resources.py`. `python3 lectures/08/scripts/research_new_resources.py --check`로 미배치 44장 대응·제목·화면 번호·선수 관계·출처 연결·도식 원본 해시·재생성 일치 확인
- 자료 편집 원본: `../scripts/reused_resources.py`(기존 16장) · `../scripts/new_resources.py`(신규 44장). 시퀀스·분기·시간축·화면·환경·관측 차트는 `../scripts/resource_blocks.py`의 편집 가능한 HTML 블록, 도식 기본 배치는 `../resources.css`, 본문과 자료의 조합·모바일 배치는 `../body.css`. 코드·표는 공용 작성 블록 사용
- 편집 원본: `../scripts/lesson.py`에서 `chapters.py`·`title_outline.py`·`slide_body.py`·두 자료 원본 조합. 실습 리뷰는 `../lab-review/scripts/lesson.py`
- 반영 기록 생성: `python3 lectures/08/scripts/resource_placements.py`; `--check`로 기존 16장·신규 44장의 배치 대응 확인
- 생성: 저장소 루트에서 `python3 lectures/08/scripts/build-slides.py`, `python3 lectures/08/lab-review/scripts/build-slides.py`
- [공통 작성 틀과 블록 사용법](../../authoring/scaffolds.md) · [작성 하네스](../../authoring/README.md)

## 확정한 챕터

| 화면 | 챕터 | 제목 |
| --- | --- | --- |
| 2 | 01 | 사용자 인증의 원리 |
| 10 | 02 | 로그인 상태의 유지 |
| 21 | 03 | 외부 인증과 소셜 로그인 |
| 30 | 04 | 권한과 데이터 접근 제어 |
| 39 | 05 | 관리자 시스템과 운영 업무 |
| 47 | 06 | 웹 공격과 방어 원리 |
| 58 | 07 | 환경 분리와 서비스 운영 |

사용자 확인 → 로그인 상태 유지 → 외부 인증 활용 → 권한 판단 → 관리자 업무 → 공격과 방어 → 환경 분리와 운영의 학습 순서다. 기존 공용 챕터 디자인의 번호·제목·짧은 학습 범위를 재사용한다.

이 순서와 작성 하네스에 따라 본문 60장의 한영 설명을 완성했다. 제목·문단 원고와 각 자료의 선수 관계를 유지하며, 단순 비교는 설명 아래의 넓은 표, 요청 흐름·코드는 설명 옆의 사례 영역에 배치했다. 검증 조건·입력 결과처럼 밀도가 높은 장은 문장 중복을 줄이고 표와 설명을 나누어 구성했다. 동일한 쿠키 예제를 2.2→6.9에서 확장하고, 일반 토큰 시퀀스를 2.7의 JWT 검증으로 구체화하며, OAuth 도식은 3.4→3.5→3.6 순서로 보호 요소를 추가한다. 신규 자료도 사용자·제보·URL·환경을 이어 사용한다. 실습 절차는 별도 실습 세션에서 다룬다.

검증: 공용 `npm test --prefix packages/web-deck`, 생성 결과 `--check`, 원본 조사 및 반영 기록 `--check`를 사용한다. 실제 KO/EN 전체 화면·인쇄·390px 모바일 검사는 `packages/web-deck/tests/authoring-layout.cjs`로 수행하며, 자료 배치 단계의 기록은 [자료 검토](resource-layout-review.json), 본문 완성 단계의 내용·화면·인쇄·모바일 검토는 [본문 검토](body-layout-review.json)에 보관한다.
