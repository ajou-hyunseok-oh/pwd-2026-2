# 08회차 — 웹 서비스 인증과 운영

- [8주차 강의](../index.html): 2026학년도 2학기·8주차 표지 1장, 챕터 표지 6장, 설명·자료를 완성한 본문 37장, 총 44장. KO/EN 지원
- [7주차 실습 리뷰](../lab-review/index.html): `pwd-week7` README의 개발 흐름에 맞춘 한·영 16장. DB 준비 → 코드 구현 → 연결 검증 → 영구 저장 → React 연동 순서. [구성·재생성·검증](../lab-review/materials/README.md)
- 본문 37장 작성 완료. 확정 문단을 `개념 - 짧은 정의`와 세부 글머리표로 구성하고, 기존 PDF 계보 12장·신규 자료 25장의 도식·표·코드·화면 예시와 함께 배치. 개념 설명 → 관계·조건 → 사례의 흐름을 유지
- [챕터 내부 제목·서브타이틀 설계안](week-08-titles.ko.txt): 확정한 본문 37장의 선수 개념 위치와 FoodMap 연결 사례. 1.1 등의 설계 번호와 실제 화면 번호는 구분
- 제목 설계 원본: `../scripts/title_outline.py` · [한영 제목 및 선수 관계](title-outline.json). `python3 lectures/08/scripts/title_outline.py`로 검토 자료 생성, `--check`로 재생성 일치 확인
- [슬라이드별 한 문단 원고와 흐름 평가](week-08-paragraphs.ko.txt): 37장 각각의 한국어 검토 문단, 챕터별 연결 평가와 선행 개념 점검 기록. 완성 본문과의 대응은 아래 본문 원고에서 확인
- [완성 본문 원고](week-08-body.ko.txt) · [한영 본문·확정 문단·선수 관계 대응](slide-bodies.json): 37장 각각의 정의·세부 설명과 자료 배치. 원본은 `../scripts/slide_body.py`; `python3 lectures/08/scripts/body_review.py --check`로 본문 대응·자료 동반·선수 순서·기록 일치 확인
- 문단 원본: `../scripts/paragraph_outline.py` · [구조화된 문단과 검토 기록](paragraph-outline.json). `python3 lectures/08/scripts/paragraph_outline.py`로 생성, `--check`로 제목 대응·순서·단일 문단 형식·재생성 일치 확인
- [PWD Week6 기존 애셋 재사용 조사](week6-asset-audit/reuse-review.ko.txt): PDF 31쪽의 이미지·도식·코드·표와 최초 본문 60장의 대응, 수정 조건, 학습 순서 점검. [구조화된 조사 결과](week6-asset-audit/audit.json)
- [원본 요소 추출본](week6-asset-audit/source-assets/): 로고 제외 이미지 13개, 독립 코드 영역 2개, 인라인 코드·식 4개, 표 3개. 원본 오류·잘림을 보존한 검토용 자료. 수업용 수정은 원본 추출 파일을 덮어쓰지 않고 별도 작성 원본에서 처리. [추출 이력·표 셀·원문 기록](week6-asset-audit/extraction.json)
- 조사 원본: `../scripts/audit_week6_assets.py`. `python3 lectures/08/scripts/audit_week6_assets.py --check`로 대응·원본/추출본 해시·보고서 일치 확인. 재추출은 PyMuPDF가 설치된 Python으로 같은 스크립트에 `--extract` 지정
- [전체 자료 반영 기록](resource-placements.ko.txt) · [구조화된 대응](resource-placements.json): 기존 PDF 계보 12장과 신규 25장 각각의 화면 번호·자료 반영 상태·수정 내용
- [페이지별 레퍼런스 문서](slide-references.html) · [텍스트](slide-references.ko.txt) · [구조화된 레퍼런스](slide-references.json): 본문 37장 각각의 화면 번호·설계 번호·자료 설명·원본 PDF 페이지·공식 문서 링크. 출처는 슬라이드 본문과 숨김 노트에 넣지 않고 이 문서에서 관리
- 레퍼런스 원본: `../scripts/slide_references.py`. `python3 lectures/08/scripts/slide_references.py --check`로 페이지 대응·자료 출처·재생성 일치 확인
- [44장 신규 자료 조사](new-resource-research/research.ko.txt) · [구조화된 조사](new-resource-research/research.json): 공식 문서 31개를 바탕으로 슬라이드별 도식·표·화면·코드 후보, 선수 개념, 수정 범위, 제작 우선순위 정리. 2026-11-07 조사 후 현재 강의에 반영
- [코드 후보 5개](new-resource-research/code-candidates.ko.txt): RLS SELECT·서버 입력 검증·매개변수 쿼리·React 텍스트 출력·DB 열 추가. 실행 전제와 예상 결과를 함께 기록한 이론용 발췌
- [외부 도식 원본 3개](new-resource-research/reference-figures/): MDN CORS 2개와 Supabase 환경 분리 1개. 원본 수정 없이 보관. 강의에는 필수 관계를 한영 HTML 도식으로 재구성하고 불필요한 헤더·Git 브랜치 흐름 제거. [출처·해시](new-resource-research/reference-figures/sources.json)
- 신규 조사 원본: `../scripts/research_new_resources.py`. `python3 lectures/08/scripts/research_new_resources.py --check`로 이전 60장 구성의 신규 자료 44장 조사·도식 원본 보관 상태 확인
- 자료 편집 원본: `../scripts/reused_resources.py`(기존 PDF 계보 12장) · `../scripts/new_resources.py`(신규 25장). 시퀀스·분기·시간축·화면·환경·관측 차트는 `../scripts/resource_blocks.py`의 편집 가능한 HTML 블록, 도식 기본 배치는 `../resources.css`, 본문과 자료의 조합·모바일 배치는 `../body.css`. 코드·표는 공용 작성 블록 사용
- 편집 원본: `../scripts/lesson.py`에서 `chapters.py`·`title_outline.py`·`slide_body.py`·두 자료 원본 조합. 실습 리뷰는 `../lab-review/scripts/lesson.py`
- 반영 기록 생성: `python3 lectures/08/scripts/resource_placements.py`; `--check`로 기존 PDF 계보 12장·신규 25장의 배치 대응 확인
- 생성: 저장소 루트에서 `python3 lectures/08/scripts/build-slides.py`, `python3 lectures/08/lab-review/scripts/build-slides.py`
- [공통 작성 틀과 블록 사용법](../../authoring/scaffolds.md) · [작성 하네스](../../authoring/README.md)


## 챕터 3 초심자 구성 (2026-11-09)

본문 8장을 5장으로 통합. 현재 전체 덱은 본문 37장·표지와 챕터 7장, 총 44장이다.

| 화면 | 제목 | 실습에서 확인할 용어·흐름 |
| --- | --- | --- |
| 22 | 외부 인증 제공자 | Google·네이버, Supabase Auth, 브라우저 SDK의 역할 |
| 23 | OAuth와 OIDC의 역할 | 접근 권한 위임, 인증 결과, 두 외부 토큰의 목적 |
| 24 | 소셜 로그인의 전체 흐름 | 콜백, 인가 코드, SDK 세션, 로그인 시작과 복귀 처리 |
| 25 | 인증 계정과 FoodMap 사용자 정보 | auth.users, profiles, UUID, 제보 작성자 연결 |
| 26 | 로그인 이후의 API 요청 | Bearer, Authorization, 토큰 검증, 프로필 조회 |

활성 작성 원본은 `../scripts/chapter03_content.py`. 기존 로그인 선택 화면을 유지하며 일반론 대신 8주차 서버·클라이언트 코드 경로를 확인해 작성했다. 외부 로그인 실환경 시연 결과를 뜻하지 않는다.

[보충 자료](chapter03-supplement.ko.txt)에 state·PKCE·클레임 검증·계정 연결 심화 범위를 분리했다. 기존 PDF 추출·신규 자료 조사는 60장 시점의 역사 기록이며 해당 생성기는 이전 제목 구성을 사용한다. 현재 본문 37장의 배치·출처·번호는 활성 생성 자료를 기준으로 확인한다.


## 챕터 4 초심자 구성 (2026-11-09)

본문 8장을 5장으로 통합. 현재 전체 덱은 본문 37장과 표지·챕터 7장, 총 44장이다.

| 화면 | 제목 | 실제 구현 연결 |
| --- | --- | --- |
| 28 | 인증과 인가 | 사용자 확인과 관리자 작업 허용 판단 |
| 29 | 사용자 역할과 허용 기능 | user·admin과 실제 라우트의 기능별 권한 |
| 30 | 본인 정보의 처리 | 검증된 req.auth.id로 본인 프로필 수정 |
| 31 | 서버의 권한 검사 흐름 | isAuthenticated → requireAdmin → controller.create |
| 32 | API 키와 데이터베이스 접근 | 사용자 토큰 → Express 인가 → 서버 Secret key로 DB 요청 |

활성 원본은 `../scripts/chapter04_content.py`. 용어 정의를 먼저 설명하고 실제 코드 흐름을 도식으로 연결한다. 기능 비교는 표를 사용한다. 일반 사용자의 자기 제보 조회·수정과 사용자별 RLS SQL은 현재 구현으로 설명하지 않는다.

[챕터 4 보충 자료](chapter04-supplement.ko.txt)에 범용 소유자 정책·RLS 정책 작성·DB 역할·오류 응답의 심화 조건을 분리했다. 챕터 5의 승인 상태·트랜잭션은 유지한다.

## 챕터 5 초심자 구성 (2026-11-09)

본문 7장을 5장으로 통합. 정의를 먼저 설명하고 실제 제보·승인 처리 흐름을 그 아래 도식으로 배치했다.

| 화면 | 제목 | 실제 구현 연결 |
| --- | --- | --- |
| 34 | 사용자 제보와 관리자 업무 | 제보 작성 → pending 저장 → 관리자 검토 |
| 35 | 제보의 처리 상태 | pending → approved 또는 rejected · 검토자와 시각 |
| 36 | 제보 승인의 구현 흐름 | 관리자 화면 → Express 권한 검사 → RPC → DB 승인 → 목록 갱신 |
| 37 | 승인 작업의 트랜잭션 | 맛집 생성과 제보 상태·검토 기록의 전부 반영 또는 취소 |
| 38 | 중복 승인 요청의 처리 | 대기 시 생성 · 승인 완료 시 기존 맛집 반환 · 거절 시 거부 |

활성 원본은 `../scripts/chapter05_content.py`. `submissions.routes.ts`·`submissions.service.ts`·`supabase/schema.sql`과 클라이언트 `SubmissionsPage.jsx`를 읽어 대조했다. 실환경 DB 변경을 실행한 결과가 아니다.

[챕터 5 보충 자료](chapter05-supplement.ko.txt)에 별도 공개 상태·전체 감사 로그·행 잠금·고유 제약·범용 멱등성 키를 분리했다. [내용·검증 기록](chapter05-content-review.json)에서 확인 범위를 기록한다.

## 챕터 6 초심자 구성 (2026-11-09)

본문 10장을 5장으로 통합. 정의를 먼저 배치하고 실제 설정·빌드·배포·동작 확인 흐름을 그 아래 도식으로 연결했다.

| 화면 | 제목 | 실제 구현 연결 |
| --- | --- | --- |
| 40 | 로컬 환경과 배포 환경 | 로컬 Vite·Express와 배포 Vercel·Render·Supabase의 역할 |
| 41 | 환경변수와 연결 설정 | .env.local·.env와 배포 서비스의 별도 설정 |
| 42 | 빌드와 배포의 실행 흐름 | React → dist 파일 제공 / TypeScript → dist/server.js 실행 |
| 43 | 배포 주소와 로그인 복귀 설정 | VITE_API_BASE_URL·CLIENT_URL·Site URL·Redirect URLs |
| 44 | 배포 후 동작 확인 | /health → 맛집 조회 → 로그인 → 제보·승인과 목록 반영 |

활성 원본은 `../scripts/chapter06_content.py`. 클라이언트 설정·API·로그인 코드·vercel.json, 서버 설정·/health·package.json 및 두 실습서의 배포 절차를 대조했다. 실제 배포나 DB 변경을 실행한 결과가 아니다. 별도 검증 환경이나 환경별 DB가 자동으로 구성된다고 설명하지 않으며, 현재 실습의 키·환경변수 이름을 사용한다.

[챕터 6 보충 자료](chapter06-supplement.ko.txt)에 검증 환경·데이터 분리·마이그레이션·지표·백업·롤백·복원 범위를 분리했다. [내용·화면 검토 기록](chapter06-content-review.json)에 실제 확인 범위를 기록한다.

## 보안 챕터의 다음 주 분리 (2026-11-09)

사용자 요청에 따라 기존 챕터 6 「웹 공격과 방어 원리」의 표지와 본문 10장(기존 화면 39~49)을 이번 주 발표·목차·한영 번역·본문 및 자료 목록에서 제외했다. 입력 검증·SQL 인젝션·XSS·출처·사이트·동일 출처 정책·CORS·CSRF·쿠키 보호 속성·로그인 시도 제한은 다음 주 강의 범위다. 작성 원본과 과거 조사 기록은 재사용을 위해 보존한다. 다음 주 덱에는 아직 추가하지 않았다.

이번 주에는 로그인·인증·권한 검사와 제보 승인에 필요한 내용을 유지한다. 기존 챕터 7은 현재 챕터 6으로 표시하며 39페이지에서 시작한다. 안정적인 링크를 위해 내부 ID `chapter-07`은 보존한다. 전체 44장(표지 1 + 챕터 6 + 본문 37).

## 확정한 챕터

| 화면 | 챕터 | 제목 |
| --- | --- | --- |
| 2 | 01 | 사용자 인증의 원리 |
| 10 | 02 | 로그인 상태의 유지 |
| 21 | 03 | 외부 인증과 소셜 로그인 |
| 27 | 04 | 권한과 데이터 접근 제어 |
| 33 | 05 | 관리자 시스템과 운영 업무 |
| 39 | 06 | 환경 분리와 서비스 운영 |

사용자 확인 → 로그인 상태 유지 → 외부 인증 활용 → 권한 판단 → 관리자 업무 → 환경 분리와 운영의 학습 순서다. 기존 공용 챕터 디자인의 번호·제목·짧은 학습 범위를 재사용한다.

이 순서와 작성 하네스에 따라 본문 37장의 한영 설명을 완성했다. 제목·문단 원고와 각 자료의 선수 관계를 유지하며, 단순 비교는 설명 아래의 넓은 표, 요청 흐름·코드는 설명 옆의 사례 영역에 배치했다. 검증 조건·입력 결과처럼 밀도가 높은 장은 문장 중복을 줄이고 표와 설명을 나누어 구성했다. 일반 토큰 시퀀스를 2.7의 JWT 검증으로 구체화하며, 챕터 3은 실제 Supabase Auth·SDK 구현 경로를 설명하며 state·PKCE 내부 처리는 보충 자료로 분리한다. 신규 자료도 사용자·제보·URL·환경을 이어 사용한다. 실습 절차는 별도 실습 세션에서 다룬다.

검증: 공용 `npm test --prefix packages/web-deck`, 생성 결과 `--check`, 원본 조사 및 반영 기록 `--check`를 사용한다. 실제 KO/EN 전체 화면·인쇄·390px 모바일 검사는 `packages/web-deck/tests/authoring-layout.cjs`로 수행하며, 자료 배치 단계의 기록은 [자료 검토](resource-layout-review.json), 본문 완성 단계의 내용·화면·인쇄·모바일 검토는 [본문 검토](body-layout-review.json)에 보관한다.


## 지정 범위 표현 보완 (2026-11-09)

챕터 1~2의 한영 본문·도식은 유지했다. 챕터 3은 외부 제공자 토큰과 Supabase 액세스 토큰을 구분하고, 30페이지는 isAuthenticated의 역할을 설명했다. 32페이지의 RLS 정의·우회 경로는 챕터 4 보충 자료에 두고 사용자 토큰·브라우저 키·서버 키를 구분했다. 36~38페이지는 요청 경로(:id는 선택한 제보 ID)·한 요청의 트랜잭션·재요청 시 기존 맛집 반환으로 각각 설명한다. 멱등성 용어는 챕터 5 보충 자료에 두었다. 40페이지 도식에 Vercel·Render·Supabase의 역할을 명시하고 44페이지의 Network를 브라우저 개발자 도구의 요청 확인 탭으로 풀어 설명했다.

전체 44장·본문 37장 유지. [검토 기록](focused-refinement-review.json)에 변경한 11개 화면의 한영 발표·인쇄·모바일 66뷰와 앞 챕터 보존 확인을 기록했다.


## 영문 최종 용어·표현 검토 (2026-11-09)

전체 44장의 영문 제목·본문·도식·표·코드 라벨을 검토하고 한국어 내용·순서·코드 예제를 유지했다. 제보는 `submission`, JWT 정보 항목은 `claims`, 토큰 갱신은 `token refresh`, 서버에 상태를 보관하는 세션은 `server-side session`, 트랜잭션 성공·취소는 `commit`·`roll back`으로 용어를 맞췄다. `Authentication`·`Authorization`과 외부 제공자 토큰·Supabase 액세스 토큰 구분을 유지하며 코드의 경로·필드·함수 이름은 번역하지 않았다.

표지·브라우저 제목·목차의 8주차 강의명은 「웹 서비스 인증과 운영 / Web Service Authentication and Operations」이며 보안/Security 표기가 없다. [영문 최종 검토 기록](english-final-review.json)에 영문 수정 내역·용어 기준·전체 화면 검증과 실행하지 못한 검사 범위를 기록한다.


## 8주차 공개 준비 (2026-11-09)

공개 목록에 08을 추가하고 루트 캘린더 제목을 「웹 서비스 인증과 운영」으로 확정했다. 검증 도구 설치 후 전체 npm test(코드 173블록·344언어 변형과 작성 하네스 포함), 공개용 사이트 빌드와 링크·44장 확인을 통과했다. 이전 검토 기록의 prettier 미설치 제한은 공개 준비 단계에서 해소했다. [공개 검토 기록](publication-review.json)을 참조한다.
