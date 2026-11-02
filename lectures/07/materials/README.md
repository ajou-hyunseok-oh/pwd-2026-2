# 07주차 — 데이터베이스 설계와 PostgreSQL · Supabase

6주차 실습 복습은 별도 [Foodmap API 리뷰 슬라이드](../server-review/index.html) 9장으로 제공한다. 06주차의 클라이언트 리뷰 형식을 재사용하며, `pwd-week6`의 실제 코드·HTTP 응답·재시작 결과를 기준으로 작성했다. 작성 원본과 검증 절차는 [리뷰 자료 안내](../server-review/materials/README.md)에 있다.

[강의 슬라이드](../index.html)는 82장 한·영 강의다. 전년도 `[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf`의 DB 기초·설계·무결성·정규화·SQL을 재구성하고, MongoDB·MERN 부분을 PostgreSQL과 Supabase로 교체했다. 49~81번의 Supabase 챕터는 실제 검증한 `pwd-week7` 실습의 SQL·서버·DB·클라이언트 흐름을 설명한다. 앞부분의 제보–맛집 관계 SQL은 별도의 설계 예제이며 이번 실습의 실행 스키마는 `restaurants` 테이블 하나다. 기존 과제 마감과 제출 요구는 현재 과제로 지정하지 않는다.

## Supabase 챕터의 학습 흐름

| 화면 | 설명 범위 | 실습과의 대응 |
| --- | --- | --- |
| 50~53 | 출발·성장·현재 서비스 구성·관리형 DB의 의의 | PostgreSQL 기반 플랫폼을 선택한 이유와 영구 저장 |
| 54~58 | 요청 흐름·저장 범위·프로젝트·SQL 파일·편집기 | Vercel → Render Express → Data API → PostgreSQL |
| 59~64 | 테이블·자료형·IDENTITY·NOT NULL·DEFAULT·배열 | `schema.sql`의 열 정의 10개 |
| 65~68 | 키와 역할·RLS·스키마/테이블/시퀀스 권한 | `schema.sql`의 ALTER·REVOKE·GRANT |
| 69~74 | 함수 정의·실행 환경·행 복원·트랜잭션·번호·호출 권한 | 기존 reset-demo용 함수와 실제 동작 |
| 75~76 | 빈 테이블 조건부 시딩·조회 | `seed.sql` 전체와 확인용 SELECT |
| 77~81 | API 변환·재시작·배포·오류 사례·완료 기준 | 실제 Supabase 4건과 Render·Vercel의 일치 결과 |

실습 안내서는 별도 서버 저장소 `pwd-week7/docs/supabase-practice.ko.md`에 있다. 설치·설정은 해당 저장소 README를, SQL 실행은 `supabase/schema.sql`과 `supabase/seed.sql` 원문을 사용한다. 강의 코드는 전체/발췌/확인용 SQL을 라벨로 구분하며 긴 원본 INSERT의 외부 이미지 URL을 임의 값으로 바꾸지 않는다.

완료된 [실제 검증 기록](supabase-verification.json)은 서버 재시작 및 배포 조회 결과를 보존한다. 강의 작성 중 공개 DB에 새 데이터나 초기화를 실행하지 않았다. 제보·승인·좋아요는 기존 LocalStorage, 이미지 파일은 기존 외부 서버에 있으며 이번에 Storage나 인증 기능을 추가하지 않았다.

## 작성과 재생성

- `../scripts/lesson_content.py`: 한·영 본문과 SQL 예제 원본
- `../scripts/supabase_chapter.py`: 검증된 Supabase 실습 챕터의 한·영 본문·SQL 발췌·공식 근거
- `../scripts/authoring_blocks.py`: 공용 표·절차·원본 그림과 슬라이드별 출처 대응
- `../scripts/extract-source-figures.py`: PDF의 4·5·7·8·11·12·14·16·18·19쪽 그림 영역 개별 추출 (Poppler pdftoppm 필요)
- `source-figures/`: 추출한 원본 그림 12개. 그림을 선택하면 원본 크기로 열림
- `../scripts/build-slides.py`: HTML, `lecture-content.js`, `slide-map.json` 생성
- `../lecture.css`: ERD 표현에 필요한 회차별 스타일
- `slide-map.json`: 화면 번호와 제목 목록
- [내용 검토](content-review.ko.md): 원본 대응과 기술 근거

```sh
python3 lectures/07/scripts/build-slides.py
node packages/web-deck/scripts/code-examples.cjs --write --lecture 07
npm test --prefix packages/web-deck
# 저장소 루트 HTTP 서버와 Playwright 경로 필요
LECTURE=07 DECK_URL=http://127.0.0.1:4305 PLAYWRIGHT_PATH=/path/to/playwright node packages/web-deck/tests/authoring-layout.cjs
```

SQL은 공용 포매터에서 text로 처리한다. 표기 서식 검사는 PostgreSQL 실행 검증을 뜻하지 않는다. 앞부분의 설계 예제는 제보 INSERT에서 반환한 id가 1이고 생성된 식당 id가 1이라는 조건을 코드 라벨에 명시한다. JOIN은 연결된 행이 있을 때 결과가 있다. NOT NULL 열 추가 예제는 빈 식당 테이블을 전제로 한다. 이 예제와 달리 새 Supabase 챕터는 이미 실행·검증한 서버 실습의 실제 SQL을 기준으로 한다. 로컬 PGlite에서 원본 SQL의 6개 검사를 통과했고, 실제 클라우드 연결과 서버 재시작 증거는 별도로 구분한다.

[개념별 시각·코드 자료 조사](visual-research.ko.md)는 51개 개념 화면의 기존 자료·외부 출처·도식 제작 후보를 정리한다. 조사 내용은 아직 슬라이드에 적용하지 않았다.

2025년 자료와 공통인 설명은 원문을 우선 적용했고, 동일 주제의 그림 12개를 해당 개념 화면에 배치했다. 원본 ERD의 0..다수 기호는 원본 설명 및 현재 설계와 달라 기존 0..1 도식을 유지한다. 영어 모드의 일부 원본 그림 안 한국어는 원본 이미지 보존 때문에 그대로이며 영어 대체 텍스트를 제공한다.

데이터베이스 역사 슬라이드는 DBMS 바로 다음에 원본 5쪽의 7개 시기·설명과 그림을 보존한다.

데이터베이스 유형과 데이터베이스 관련 직군은 원본 6~8쪽의 내용과 이미지로 복구했다. 트렌드 슬라이드는 DB-Engines의 [2026년 10월 추이 그래프](https://db-engines.com/en/ranking_trend)와 [순위표](https://db-engines.com/en/ranking)의 화면을 사용한다. 순위는 DBMS의 상대적인 인기도 지표이며 시장 점유율을 뜻하지 않는다. 원본 PDF의 2025년 9월 이미지는 별도로 보존한다.
