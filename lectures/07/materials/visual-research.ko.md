# 7주차 개념별 시각·코드 자료 조사

현재 56장 덱의 10~35쪽을 한 장씩 검토한 보강안은 [10~35쪽 보강 분석](design-slides-review.ko.md)에 있다. 아래는 2026-11-01 조사 당시의 자료 목록과 번호를 보존한 기록이다.

조사일: 2026-11-01. 대상: 조사 당시 58장 덱의 실제 개념 설명 51장. 표지·학습 목표·4개 챕터·Q&A는 제외한다. 아래 번호는 조사 당시 화면 번호이며 이후 역사 슬라이드 추가로 현재 번호와 다를 수 있다. 현재 번호는 `slide-map.json`을 확인한다. 본 문서는 **자료 조사 및 적용 후보**이며, 새 이미지를 슬라이드에 삽입하거나 실제 Supabase 계정의 화면을 캡처한 결과가 아니다.

## 읽는 방법과 수집 범위

- **기존**: 7주차에 이미 들어 있는 표·단계·도식·SQL. 원본은 `../scripts/lesson_content.py`와 `../scripts/authoring_blocks.py`.
- **제작 후보**: 조사한 개념과 기존 FoodMap 사례를 바탕으로 새로 만들 수 있는 도식·표. 아래에 구성 요소와 목적을 구체화했지만 아직 제작하지 않았다.
- **출처**: 실제 확인한 PDF 또는 외부 자료. 외부 이미지는 참고 링크이며, 사용 허가를 확인하거나 라이선스를 충족하기 전에는 복제해 넣지 않는다. 제안된 도식은 원자료에서 발견한 이미지와 구분한다.
- 2025년 [원본 PDF](<./[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf>)는 로컬 보유. 11·12쪽에 설계 그림, 16쪽에 ERD가 있다. 16쪽의 제보→맛집 선은 도식상 0..다수이나 문장은 0..1이므로 그대로 재사용하지 않는다.

### 확인한 자료

| 코드 | 실제 수집한 자료·위치 | 참고 범위 |
|---|---|---|
| A | [2025 원본 PDF](<./[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf>) | 4·6·10~19쪽의 기초·설계와 도식 |
| B | [PostgreSQL 아키텍처 기초](https://www.postgresql.org/docs/current/tutorial-arch.html), [관계형 개념](https://www.postgresql.org/docs/current/tutorial-concepts.html), [테이블 기초](https://www.postgresql.org/docs/current/ddl-basics.html) | 서버·클라이언트, 테이블·행·열 설명 |
| C | [PostgreSQL 제약조건](https://www.postgresql.org/docs/current/ddl-constraints.html), [인덱스 소개](https://www.postgresql.org/docs/current/indexes-intro.html) | PK·FK·제약 코드와 인덱스 접근 설명 |
| D | [CMU 함수 종속 강의 PDF 1쪽](https://www.cs.cmu.edu/~christos/courses/dbms-F09/slides/17NormI.pdf#page=1), [CMU 정규형 강의 PDF 1쪽](https://www.cs.cmu.edu/~natassa/courses/15-415/S03/notes/18Norm6up.pdf#page=1) | 중복 표·함수 종속 및 BCNF 판정의 실제 강의 예. 외부 그림 재사용 권리는 미확인 |
| E | [BCcampus Database Design, 정규화](https://opentextbc.ca/dbdesign01/chapter/chapter-12-normalization/) | 1NF~BCNF의 표, Figure 12.1 종속 도식, 학생·전공·지도교수 BCNF 예. 책은 별도 표시를 제외하고 CC BY 4.0; 이미지별 표시와 귀속 확인 필요. 본문 BCNF의 ‘결정자가 후보 키’ 표현은 C·D의 슈퍼키 기준으로 보정 |
| F | PostgreSQL 공식 튜토리얼: [테이블 생성](https://www.postgresql.org/docs/current/tutorial-table.html) · [행 추가](https://www.postgresql.org/docs/current/tutorial-populate.html) · [조회](https://www.postgresql.org/docs/current/tutorial-select.html) · [JOIN](https://www.postgresql.org/docs/current/tutorial-join.html) · [수정](https://www.postgresql.org/docs/current/tutorial-update.html) · [삭제](https://www.postgresql.org/docs/current/tutorial-delete.html) · [자료형](https://www.postgresql.org/docs/current/datatype.html) | 실제 SQL 예와 일부 조회 결과 표. 프로젝트 사례에 맞춘 새 데이터와 결과는 별도 검증 필요 |
| G | [Supabase 아키텍처 문서](https://supabase.com/docs/guides/getting-started/architecture)와 [공식 아키텍처 SVG](https://supabase.com/docs/img/supabase-architecture--light.svg), [Database 제품 페이지](https://supabase.com/database) | 실제 아키텍처 그림과 Table/SQL Editor 제품 화면 예시. 링크로 수집, 이용 조건 미확인 |
| I | [Microsoft Learn 개념 모델](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/entity-data-model-key-concepts) · [Book–Publisher–Author 실제 도식](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/media/entity-data-model-key-concepts/conceptual-model-entity-types-associations.gif) | 엔티티·속성·관계의 실제 도식. FoodMap 사례로 자체 재구성할 참고 자료이며 이미지 이용 조건 미확인 |
| H | [Supabase 테이블·데이터](https://supabase.com/docs/guides/database/tables), [데이터베이스 접속](https://supabase.com/docs/guides/database/connecting-to-postgres), [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [프로젝트 지역](https://supabase.com/docs/guides/platform/regions) | 프로젝트/테이블/접근·RLS의 실제 설명과 정책 예제 |

## 04~08: 데이터베이스 기초

| 화면 | 현재 상태 | 수집 자료와 구체적 적용 후보 | 출처 |
|---|---|---|---|
| 04 데이터베이스 | 설명 | 사용자 세 명 → 공유 FoodMap 데이터 모음. 같은 데이터에 여러 사용자가 접근하는 관계를 표현 | A 4쪽 |
| 05 DBMS | 설명 | 웹 앱 → DBMS → 저장 데이터, 요청·결과를 양방향 화살표로 표현 | A 4쪽, B 아키텍처 |
| 06 관계형 데이터베이스 | 설명 | 사용자·제보 두 표와 공통 식별값 연결선. 후속 키 장의 상세 문법은 제외 | A 6쪽, B 관계형 개념 |
| 07 테이블·행·열 | **기존 표** | 식당 표에서 한 행·한 열·한 셀을 각각 강조하고 범례 추가 | B 테이블 기초 |
| 08 데이터베이스 유형 | **기존 비교표** | 관계형 테이블과 문서형 구조의 작은 모식도를 비교표 옆에 배치. 기능의 차이는 제품별로 다름 | A 6·20쪽 |

## 10~23: 설계·관계·무결성

| 화면 | 현재 상태 | 수집 자료와 구체적 적용 후보 | 출처 |
|---|---|---|---|
| 10 데이터베이스 설계 | 설명 | 요구사항 문장 → 모델 → 데이터 구조 도식. 원본 11쪽의 현실세계·개념·논리·DB 그림 참고 | A 10~11쪽 |
| 11 데이터베이스 설계 절차 | **기존 3단계 흐름** | 기존 개념→논리→물리 단계 유지. 원본 12쪽의 전체 생명주기는 참고용으로 분리 | A 11~12쪽 |
| 12 개념적 설계 | 설명 | ‘사용자가 맛집을 제보’라는 문장 → 사용자·제보·맛집 관계 스케치 | A 13쪽, I 개념 모델 도식 |
| 13 엔티티 | 설명 | 식당이라는 종류 상자에서 개별 식당 두 개 카드로 분기 | A 13쪽 |
| 14 속성 | 설명 | 식당 카드의 이름·주소·평점에 화살표, 평점 1~5 범위 표시 | A 13쪽 |
| 15 관계 | 설명 | 사용자 한 명 → ‘작성’ → 제보 두 개 | A 13쪽 |
| 16 카디널리티 | 설명 | 1:1·1:N·N:M의 양쪽 개수 모식도와 필수·선택 표기 | A 13쪽, 16쪽 범례 |
| 17 논리적 설계 | 설명 | 식당 엔티티·속성 → restaurants 테이블의 열로 대응 | A 14쪽, B 테이블 기초 |
| 18 기본 키 | 설명 | 식당 표의 id 열 강조. 이름 중복은 가능하지만 id 중복·NULL은 거부하는 사례 | C 제약조건 |
| 19 외래 키 | 설명 | restaurants.submission_id → submissions.id 값 연결. 존재하지 않는 값의 거부 표시 | C 외래 키 |
| 20 물리적 설계 | 설명 | 동일 테이블에 대해 순차 탐색과 인덱스 탐색 경로 비교. 실제 선택은 쿼리 플래너와 상황에 따라 달라짐 | A 15쪽, C 인덱스 |
| 21 ERD | **기존 관계 도식** | 제보 1건당 맛집 0..1, 맛집당 제보 1이라는 양방향 표기 강화. 원본 오류 수정 유지 | A 16쪽, C 외래 키 |
| 22 제약조건 | 설명 | 필수값·고유값·허용 범위 각각의 입력 → 허용/거부 비교표 | A 17쪽, C 제약조건 |
| 23 데이터 무결성 | 설명 | 개체·참조·도메인 무결성별 정상 데이터와 위반 데이터 비교 | A 17쪽, C 제약조건 |

## 24~34: 정규화와 선수 개념

| 화면 | 현재 상태 | 수집 자료와 구체적 적용 후보 | 출처 |
|---|---|---|---|
| 24 정규화 | 설명 | 같은 식당 이름이 두 행에 중복된 표 → 일부만 수정한 불일치 → 테이블 분리 | A 18쪽, D 함수 종속 PDF 1쪽 |
| 25 함수 종속 | 설명 | 두 행에서 같은 식당 ID가 같은 이름을 결정하는 `식당 ID → 식당 이름` 연결 | D 함수 종속 PDF 3쪽 |
| 26 슈퍼키 | 설명 | 식당 ID와 `(식당 ID, 이름)` 두 조합을 구별되는 열 강조로 표시 | D 정규형 PDF 1쪽 |
| 27 후보 키 | 설명 | 슈퍼키 조합에서 불필요한 이름을 제거해 식당 ID만 남기는 최소성 표시 | D 정규형 PDF 1쪽 |
| 28 주요 속성 | 설명 | 식당 ID·메뉴 ID가 복합 후보 키인 예시에서 두 열과 식당 이름 열을 구분 | D 정규형 PDF |
| 29 부분 종속 | 설명 | `(식당 ID, 메뉴 ID)` 중 식당 ID → 식당 이름 화살표. 복합 후보 키라는 전제를 표시 | E Figure 12.1 참고 |
| 30 이행 종속 | 설명 | 식당 ID → 지역 코드 → 지역 이름을 두 개의 화살표로 표시 | E Figure 12.1 참고 |
| 31 제1정규형 | 설명 | 한 셀의 여러 전화번호 → 식당 ID·전화번호가 있는 여러 행의 전후 표 | E 1NF 예시 |
| 32 제2정규형 | **기존 분리 결과 표** | 분리 전 식당 ID·메뉴 ID·이름·가격 표와 부분 종속 화살표를 추가 | E 2NF 예시 |
| 33 제3정규형 | **기존 분리 결과 표** | 식당 ID·지역 코드·지역 이름의 분리 전 표에서 지역 테이블로 분리되는 선 | E 3NF 예시 |
| 34 BCNF | 설명 | X→A에서 X가 슈퍼키인지 판단하는 간결한 조건 도식. 추가 예제는 후보 키·업무 규칙을 함께 검증 | D BCNF 정의. E의 학생·전공·지도교수 표는 참고 사례 |

E의 Figure 12.1에서 `FD`는 해당 그림에 한해 full dependency의 약어이므로, 함수 종속(functional dependency) 약어와 혼동하지 않게 재구성한다.

## 36~47: PostgreSQL과 SQL

| 화면 | 현재 상태 | 수집 자료와 구체적 적용 후보 | 출처 |
|---|---|---|---|
| 36 PostgreSQL | 설명 | 애플리케이션 → PostgreSQL DBMS → 테이블의 관계도. 플랫폼 로고는 장식보다 기능 구분에 필요한 경우만 | B 아키텍처 |
| 37 SQL | 설명 | SQL 요청 → DBMS → 결과 구조와 정의·조회·변경의 구분 표 | F PostgreSQL 튜토리얼 |
| 38 PostgreSQL 자료형 | 설명 | `text`, `integer`, `boolean`, `timestamptz`와 예시 값의 대응 표 | F 자료형 |
| 39 테이블 생성 | **기존 SQL** | 기존 CREATE TABLE 코드의 열 이름·타입·제약에 색상 또는 괄호로 대응 표시 | F 테이블 생성, C 제약조건 |
| 40 제보 테이블 생성 | **기존 SQL** | 기존 코드와 `submissions`의 id·name 열을 가진 빈 표 연결 | F 테이블 생성 |
| 41 제보와 맛집 관계 | **기존 SQL** | 두 테이블의 `submission_id`→`id` 선과 NOT NULL·UNIQUE 라벨. 빈 테이블 전제 유지 | C 외래 키·고유 제약 |
| 42 제보 데이터 추가 | **기존 SQL** | INSERT 전 빈 표 → 삽입된 행과 RETURNING id 결과. 결과는 예시로 명시 | F 행 추가 |
| 43 데이터 추가 | **기존 SQL** | id 1 제보를 참조하는 식당 행이 추가되는 전후 표. 제보 id 조건 유지 | F 행 추가, C 외래 키 |
| 44 데이터 조회 | **기존 SQL** | 원본 표에서 WHERE와 일치하는 행만 남는 결과 표 | F 조회 |
| 45 JOIN | **기존 SQL** | 두 표의 일치하는 id를 연결하고 하나의 결과 행을 보여주는 표. 별칭은 원본 SQL과 일치 | F JOIN 예제와 결과 표 |
| 46 데이터 수정 | **기존 SQL** | id 1 행의 주소 변경 전·후 강조. 조건 없는 UPDATE는 전체 행에 영향 | F 수정 |
| 47 데이터 삭제 | **기존 SQL** | 조건에 일치하는 행만 제거되는 전후 표. 조건 없는 DELETE는 전체 행에 영향 | F 삭제 |

SQL은 현재 `text` 코드 블록이다. id 1이라는 예제 조건과 빈 테이블 전제를 유지하고, 삽입·조회 결과 그림은 실제 PostgreSQL에서 확인하기 전까지 예시 결과로 취급한다.

## 49~57: Supabase와 FoodMap

| 화면 | 현재 상태 | 수집 자료와 구체적 적용 후보 | 출처 |
|---|---|---|---|
| 49 Supabase | 설명 | G의 실제 공식 SVG를 참고하여 PostgreSQL 중심으로 Auth·Storage·Data API만 남긴 간략 구조도 제작 | G 공식 아키텍처 문서·SVG |
| 50 Supabase 프로젝트 | 설명 | 조직 → 프로젝트 → PostgreSQL·관련 서비스 포함 관계, 지역·암호는 프로젝트 설정으로 표시 | H 프로젝트 지역, G 아키텍처 |
| 51 데이터베이스 구축 절차 | **기존 단계 흐름** | 프로젝트 → 테이블/열 → 키/제약 → 샘플 조회 → 권한/RLS 검증 흐름으로 보강 | H 테이블·RLS |
| 52 Table Editor | 설명 | G 제품 페이지의 실제 테이블 화면 참고. FoodMap 예시 행·열·PK가 보이는 별도 모식화 화면 제작 | G Database 제품 화면, H 테이블 |
| 53 SQL Editor | 설명 | G 제품 페이지의 SQL Editor를 참고해 코드 입력 영역과 실행 결과 영역의 모식화 화면 제작 | G Database 제품 화면, H 테이블 |
| 54 데이터베이스 접근 | 설명 | 브라우저 → Data API → PostgreSQL, 서버 → DB 연결 두 경로. 공개 키와 서버 비밀 자격 증명 역할 표시 | H 접속 문서 |
| 55 행 수준 보안 | 설명 | 소유자 A/B/A 세 행 → 요청자 A에게 A 두 행만 허용하는 전후 표. 권한과 정책을 함께 표시 | H RLS 정책 설명 |
| 56 Supabase의 RLS 설정 | 설명 | Table Editor 생성 시 기본 활성 ↔ SQL 생성 시 직접 활성. 두 경로 모두 권한·정책 및 API 역할 테스트 | H 테이블·RLS |
| 57 FoodMap 데이터베이스 설계 | 설명 | 제보 1 — 0..1 맛집 도식에 FK·NOT NULL·UNIQUE 표시. 승인 여부는 별도 업무 로직 | A 16쪽, C 제약조건 |

제품 페이지와 공식 SVG는 링크로만 수집했다. 대시보드 모식화 그림을 만들 경우 실제 캡처가 아닌 예시 화면으로 표시하고 실제 키·연결 문자열·계정 정보를 넣지 않는다.

## 우선 적용 제안

1. **관계와 제약:** 18~19·21·41·45·57. 하나의 FoodMap 데이터로 키·ERD·JOIN을 일관되게 연결.
2. **정규화:** 24~34. 같은 표의 변경 이상·종속·분리 전후를 단계적으로 재사용. BCNF는 별도 예제의 키를 검증.
3. **SQL 실행 결과:** 42~47. 기존 코드와 표의 전후 상태를 맞추고 실제 PostgreSQL 실행 결과 확인.
4. **Supabase 접근과 보안:** 49·52~56. 공식 화면과 구조를 참고한 모식도 및 RLS 허용·거부 표.

모든 페이지에 그림을 강제하지 않는다. 이미 충분한 표·코드가 있는 페이지는 중복 삽입보다 강조나 보완 여부를 결정한다.
