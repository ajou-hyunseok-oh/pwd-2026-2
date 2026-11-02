# PostgreSQL 소개 챕터 자료

[제공된 2026년 11월 조사 문서](../postgresql-research.ko.txt)를 바탕으로 36~44쪽을 구성한다. 41쪽 이후의 전문 내용 9장을 학생 수준의 기초 사례 4장으로 줄였다. 전체 강의는 56장이며, 45~55쪽의 별도 Supabase 챕터와 56쪽 실습 안내가 이어진다.

| 화면 | 제목 | 사례·시각 자료 |
| --- | --- | --- |
| 36 | PostgreSQL | 챕터 표지 |
| 37 | PostgreSQL 개요 | 공식 Slonik 이미지, 애플리케이션 연결, 활용 분야 표 |
| 38 | PostgreSQL의 발전 | POSTGRES→Postgres95→PostgreSQL 흐름, 기능 발전 연혁 |
| 39 | PostgreSQL의 사용 현황 | 2025 설문 지표의 의미, 채택·생태계의 설명 모형 |
| 40 | PostgreSQL 라이선스 | 소프트웨어·인프라·유지보수 비용 구분 |
| 41 | 함께 처리하는 데이터 변경 | 주문·재고를 묶은 트랜잭션과 성공·취소 결과 |
| 42 | JSON 부가 정보 저장 | 식당 기본 열, 부가 속성 해석 표, details JSON 값 |
| 43 | 필요한 기능의 확장 | PostGIS로 이해하는 반경 500m 거리 도식과 결과 표 |
| 44 | 관리형 PostgreSQL | 직접 설치·관리형 비교와 웹 관리 화면의 역할 |

## 학습 범위 조정

41~44쪽은 데이터베이스 설계 장에서 배운 행·열·자료형을 바탕으로 기능의 목적과 구체적 결과를 이해하는 수준이다. 트랜잭션은 함께 반영·함께 취소하는 의미, JSONB는 추가 정보를 담는 자료형, PostGIS는 주변 검색 기능의 예, 관리형 서비스는 설치·운영 도구와 개발자 역할로 한정했다.

ACID 네 성질·MVCC·격리 수준·잠금, JSONB의 이진 저장·인덱스·성능 비교, 여러 확장 목록·pgvector·RAG, 언어별 드라이버·ORM 목록, MySQL 상세 비교, VACUUM·복제·분산 쓰기는 본문에서 제외했다. 원문 조사 문서와 이전 검토 기록은 참고 자료로 보존한다. 이 PostgreSQL 범위 정리에서는 36~40쪽을 유지했다. 이후 Supabase 구간은 별도 챕터로 확장했다.

## 이미지와 도식

`elephant.png`는 [PostgreSQL 공식 보도자료](https://www.postgresql.org/about/press/presskit18/)의 [Slonik PNG](https://www.postgresql.org/media/img/about/press/elephant.png) 원본이다. 색·윤곽·구성 요소를 변경하지 않고 소개 화면의 기술 식별 이미지로 사용한다. PostgreSQL 및 Slonik은 PostgreSQL Community Association of Canada의 상표이며, [상표 정책](https://www.postgresql.org/about/policies/trademarks/)과 원본 해시를 [출처 목록](source-manifest.json)에 기록했다.

그 외 표와 도식은 제공 문서와 공식 설명을 바탕으로 자체 구성했다. 공간 SVG는 좌표 단위를 미터로 둔 모식도이며 원점에서 A(0,-300)·C(0,400)는 반경 500m 안, B(600,0)는 밖이다. 실제 지도나 위경도 측정 결과가 아니다. 근거는 [PostGIS ST_DWithin](https://postgis.net/docs/ST_DWithin.html)이다.

## 내용 확인

- 37~40쪽: 기존 공식 역사·릴리스 노트·2025 Stack Overflow 설문·라이선스 근거 유지. 설문과 시장점유율을 구별하고 미확인 비율을 제시하지 않음
- 트랜잭션: [공식 입문 문서](https://www.postgresql.org/docs/current/tutorial-transactions.html)의 전부 반영·전부 취소를 주문·재고 사례로 단순화. 두 변경을 같은 트랜잭션에 넣는 조건이며 자동으로 모든 업무 규칙이 보장된다는 의미가 아님
- JSONB: [공식 JSON 자료형 설명](https://www.postgresql.org/docs/current/datatype-json.html)을 바탕으로 열의 값과 속성을 구별. JSON은 자바스크립트 객체와 비슷한 표기지만 저장 예제의 모든 키는 JSON 문법에 맞는 큰따옴표 사용
- 확장: PostGIS 한 가지로 기능 추가의 의미 설명. 거리 도식의 실제 값과 검색 결과 표를 대응
- 관리형 서비스: [Supabase Database](https://supabase.com/docs/guides/database/overview)와 [Amazon RDS for PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)의 운영 도구를 소개하고 데이터 설계·권한은 개발자 역할로 구별. 백업·요금의 세부 조건은 서비스·설정에 따라 차이

각 장의 숨김 노트와 [출처 목록](source-manifest.json)에 근거를 보존했다. 공식 자료 확인 날짜는 2026-11-02다. 모든 사례는 강의 설명용이며 실습 DB나 실행 스키마를 변경하지 않았다.
