# 07주차 — 데이터베이스 설계와 PostgreSQL · Supabase

6주차 실습 복습은 별도 [Foodmap API 리뷰 슬라이드](../server-review/index.html) 9장으로 제공한다. 06주차의 클라이언트 리뷰 형식을 재사용하며, `pwd-week6`의 실제 코드·HTTP 응답·재시작 결과를 기준으로 작성했다. 작성 원본과 검증 절차는 [리뷰 자료 안내](../server-review/materials/README.md)에 있다.

[강의 슬라이드](../index.html)는 56장 한·영 강의다. 전년도 `[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf`의 DB 기초·설계·무결성·정규화를 재구성하고, 10~35번의 제목·순서를 유지하면서 11~35번 본문 25장에 실제 값의 표·관계·판정·분리 전후 도식을 보강했다. 36~44번은 제공된 PostgreSQL 조사 문서를 바탕으로 개요·대중화 배경과 학생 수준의 활용 사례를 소개한다. 기존 41~49번의 전문 내용 9장은 기초 사례 4장으로 추렸다. 45~55번은 제공된 조사 문서를 바탕으로 신설한 Supabase 챕터, 56번은 05·06주차 형식의 실습 안내다. 설계 장의 제보·맛집·메뉴·지역 사례는 개념용 예제이며 이번 실습의 실행 스키마는 `restaurants` 테이블 하나다.

## 10~35쪽의 구체적 사례

- 11~18: 요구사항·단계별 산출물, 엔티티와 인스턴스, 속성과 도메인, 관계와 최소·최대 참여, 실제 논리 테이블
- 19~24: 중복 이름과 기본 키, 외래 키의 허용·거부, 인덱스 접근 경로, 필드가 포함된 ERD, 제약 위반과 무결성
- 25~35: 이름 변경 이상, 함수 종속·키 판정, 식당별 메뉴와 지역 코드의 종속, 1NF·2NF·3NF 분리 전후, 3NF만 만족하는 BCNF 반례

2NF·3NF의 원본 그림은 PDF 18쪽에서 별도 추출해 해당 장의 보조 사례로 배치한다. 주된 데이터 표는 기존 FoodMap 사례를 이어 쓰며 한·영 텍스트와 강조가 가능한 HTML이다. [사례 검산 기록](design-example-verification.json)은 선언한 함수 종속에 따른 후보 키·정규형, 분해 후 원래 행의 복원, 전화번호 보존, 외래 키 입력 판정을 확인한다.

설계 챕터의 핵심 용어는 한글 모드의 개념 정의와 판정 표에 `엔티티(Entity)`, `기본 키(Primary Key, PK)`, `함수 종속(Functional Dependency)` 형식으로 영문을 병기한다. 설계 단계·속성·관계·키·무결성·변경 이상·종속 관계·정규형을 포함하며, 같은 장에서 반복되는 모든 용어에 병기를 되풀이하지 않는다.

## 36~44쪽 PostgreSQL 소개

| 화면 | 설명 범위 | 자료 구성 |
| --- | --- | --- |
| 36 | PostgreSQL 챕터 표지 | 기술적 특징과 대중화 배경 |
| 37~40 | 개요·역사·사용 현황·라이선스 | 공식 로고, 활용 표, 연혁, 채택 모형, 비용 구분 |
| 41 | 함께 처리하는 데이터 변경 | 주문·재고의 트랜잭션과 성공·취소 결과 표 |
| 42 | JSON 부가 정보 저장 | 식당의 기본 정보, 부가 속성의 의미와 JSON 값 |
| 43 | 필요한 기능의 확장 | PostGIS의 주변 식당 거리 도식과 검색 결과 표 |
| 44 | 관리형 PostgreSQL | 직접 설치·관리형 서비스 비교와 관리 화면 연결 |

[제공된 조사 문서](postgresql-research.ko.txt)는 참고 원문으로 보관한다. 41쪽 이후는 내부 원리나 도구 목록보다 학생들이 이해할 수 있는 목적과 사례를 중심으로 정리했다. ACID의 네 성질, MVCC·격리 수준, JSONB 저장 내부·성능 비교, pgvector·RAG, 언어별 드라이버·ORM, MySQL 상세 비교, VACUUM·분산 운영 설명은 제외했다.

[챕터 자료 안내](postgresql/README.md)와 [이미지·도식·기술 출처](postgresql/source-manifest.json)에 공식 자료와 그림의 제작 방식을 기록했다. 공식 로고 원본은 유지하고, 주문 처리·JSON·주변 식당 검색은 한·영 표와 도식으로 구성했다.

## 45~55쪽 Supabase 챕터와 실습의 연결

| 화면 | 설명 범위 | 사례·자료 |
| --- | --- | --- |
| 45 | Supabase 챕터 표지 | PostgreSQL을 활용한 백엔드 개발 |
| 46~49 | 개요·반복 작업·출발과 성장·주요 기능 | 공식 로고, DBMS와 플랫폼의 관계, 역할 비교, 연혁, 기능별 활용 표 |
| 50 | 테이블과 자동 API | 식당 행→Data API→JSON 응답의 대응 |
| 51 | 사용자 로그인 | 인증 흐름과 로그인 전후 화면 표시 |
| 52 | 행별 데이터 접근 | 개인 메모의 소유자별 허용·제외 |
| 53~55 | 대중화·AI 개발 도구·무료 시작 | 도입 요인 표, 개발·검증 흐름, 확인 날짜를 표시한 요금 조건 |
| 56 | 실습 안내 · pwd-week7 | 기존 FoodMap의 목표·요구사항·마감·제출물·README 링크 |

[제공된 Supabase 조사 문서](supabase/research.ko.md)는 참고 원문으로 보관한다. 문서의 10장 구성안·회원제 게시판 과제는 제안 자료이며 현재 수업의 새 요구사항으로 적용하지 않는다. [챕터 자료 안내](supabase/README.md)와 [공식 근거·이미지 출처](supabase/source-manifest.json)에 재구성 범위와 출처를 기록했다. 전문적인 내부 구성, RAG·임베딩, 외부 추정 매출·성장률은 제외하고 한 개념의 정의·역할과 쉬운 사례를 연결한다.

상세 실습은 [pwd-week7 README](https://github.com/ajou-hyunseok-oh/pwd-week7#readme)와 해당 저장소 `docs/supabase-practice.ko.md`에서 진행한다. SQL 실행은 `supabase/schema.sql`과 `supabase/seed.sql` 원문을 사용한다. 마지막 안내의 마감은 README에 명시된 **2026년 11월 8일 23:59 한국시간**이며, 제출물은 서버·클라이언트 GitHub URL, Render API URL, Vercel 서비스 URL이다.

완료된 [실제 검증 기록](supabase-verification.json)은 서버 재시작 및 배포 조회 결과를 보존한다. 강의 작성 중 공개 DB에 새 데이터나 초기화를 실행하지 않았다. 제보·승인·좋아요는 기존 LocalStorage, 이미지 파일은 기존 외부 서버에 있으며 이번에 Storage나 인증 기능을 추가하지 않았다.

## 작성과 재생성

- `../scripts/lesson_content.py`: DB 기초·설계의 한·영 본문과 각 챕터 조합
- `../scripts/postgres_chapter.py`: 제공 조사 문서를 학생 수준으로 추린 36~44번 PostgreSQL 소개와 공식 근거
- `../scripts/supabase_chapter.py`: 45~55번 Supabase 챕터의 한·영 본문·사례·공식 근거
- `../scripts/practice_guide.py`: 05주차 형식을 재사용한 실습 안내 한 장과 README 기준 제출 정보
- `../scripts/authoring_blocks.py`: 공용 표·절차·원본 그림과 슬라이드별 출처 대응
- `../scripts/design_examples.py`: 11~35번의 한·영 사례 데이터·도식과 본문 간결화
- `../scripts/example_blocks.py`: 실제 값 표·관계·흐름·공간 SVG·코드 블록의 렌더링
- `../scripts/check-design-examples.py`: 실제 사례 데이터·함수 종속·후보 키·정규형·분해 검산
- `../scripts/extract-source-figures.py`: PDF의 4·5·7·8·11·12·14·16·18·19쪽 그림 영역 개별 추출 (Poppler pdftoppm 필요)
- `source-figures/`: 추출한 원본 그림과 2026년 트렌드 자료. 그림을 선택하면 원본 크기로 열림
- `../scripts/build-slides.py`: HTML, `lecture-content.js`, `slide-map.json` 생성
- `../lecture.css`: ERD·사례 표·도식에 필요한 회차별 스타일
- `slide-map.json`: 화면 번호와 제목 목록
- [내용 검토](content-review.ko.md): 원본 대응과 기술 근거
- [10~35쪽 보강 분석](design-slides-review.ko.md): 각 장의 학습 공백, 구체적 데이터·도식 보강안, 원본 PDF 활용 판정

```sh
python3 lectures/07/scripts/build-slides.py
python3 lectures/07/scripts/check-design-examples.py --write
node packages/web-deck/scripts/code-examples.cjs --write --lecture 07
npm test --prefix packages/web-deck
# 저장소 루트 HTTP 서버와 Playwright 경로 필요
LECTURE=07 DECK_URL=http://127.0.0.1:4305 PLAYWRIGHT_PATH=/path/to/playwright node packages/web-deck/tests/authoring-layout.cjs
```

기존 SQL·CRUD 설명 구간은 PostgreSQL 소개로 대체했다. 현재 챕터의 JSON 예제는 공용 JSON 포매터·구문 검사로 확인한다. 설계 사례의 함수 종속·분해 검산, 소개용 공간 도식의 거리 판정, 실제 PostgreSQL·Supabase 실행 검증은 서로 다른 범위다. 이전 실습의 PGlite SQL 검사와 클라우드·재시작 증거는 기존 검토 기록에 보존한다.

[개념별 시각·코드 자료 조사](visual-research.ko.md)는 이전 51개 개념 화면의 자료·외부 출처·도식 후보 조사다. 최신 [10~35쪽 보강 분석](design-slides-review.ko.md)에 따라 이 구간의 사례를 실제 강의에 반영했다.

2025년 자료와 공통인 설명은 원문을 우선 적용했고, 관련 그림을 해당 개념 화면에 배치했다. 원본 ERD의 0..다수 기호는 원본 설명 및 현재 설계와 달라 기존 0..1 관계를 유지하고 PK·FK 필드를 보강한다. 영어 모드의 일부 원본 그림 안 한국어는 원본 이미지 보존 때문에 그대로이며 영어 대체 텍스트를 제공한다.

데이터베이스 역사 슬라이드는 DBMS 바로 다음에 원본 5쪽의 7개 시기·설명과 그림을 보존한다.

데이터베이스 유형과 데이터베이스 관련 직군은 원본 6~8쪽의 내용과 이미지로 복구했다. 트렌드 슬라이드는 DB-Engines의 [2026년 10월 추이 그래프](https://db-engines.com/en/ranking_trend)와 [순위표](https://db-engines.com/en/ranking)의 화면을 사용한다. 순위는 DBMS의 상대적인 인기도 지표이며 시장 점유율을 뜻하지 않는다. 원본 PDF의 2025년 9월 이미지는 별도로 보존한다.
