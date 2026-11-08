# 8주차 도입부 — 7주차 FoodMap DB 실습 리뷰

[한·영 슬라이드](../index.html)는 표지 포함 16장이다. 2026학년도 2학기·8주차 표지와 05의 공용 디자인을 사용한다. 8주차 인증·보안 강의와 별도 덱이며 강의 목록에서 바로 선택한다.

06의 [클라이언트 리뷰](../../../06/client-review/index.html), 07의 [서버 리뷰](../../../07/server-review/index.html)의 개념 설명·실제 코드·관찰 결과 대조, 설명·코드의 두 열 배치, 비교 표와 실행 순서를 재사용했다. 사용자의 README 개발 흐름 평가를 반영해 **DB 준비 → 코드 구현 → 연결 검증 → 영구 저장 검증 → React 연동**으로 재작성했다.

## 구성과 README 대응

| 화면 | 제목 | README·코드 대응 |
| --- | --- | --- |
| 1 | 표지 | 8주차 강의·7주차 실습 리뷰 |
| 2 | 맛집 데이터의 저장 위치 | 프로젝트 소개·완료 목표, 6·7주차 비교 |
| 3 | 맛집 테이블의 저장 규칙 | Step 4-1, CREATE TABLE 전체 |
| 4 | DB에 접근할 서버 권한 준비 | Step 4-1, RLS·REVOKE·GRANT·서버 역할 |
| 5 | 초기 데이터와 초기화의 차이 | Step 4-2, seed 조건·기존 행 보존 |
| 6 | DB 행과 등록 입력의 타입 | Step 6-2, RestaurantRow·RestaurantInsert·Database 역할 |
| 7 | 서버의 Supabase 연결 설정 | Step 5·6-3·6-6, dotenv → process.env → SDK |
| 8 | DB 행을 기존 API 형식으로 변환 | Step 6-4, fromDatabase 준비 |
| 9 | DB 목록 조회와 HTTP 응답 | Step 6-5·6-7·6-8, 조회·변환·Controller의 JSON 응답 |
| 10 | 요청 입력을 DB 행으로 구성 | Step 6-5·6-7, payload → row |
| 11 | 새 맛집의 DB 등록 | Step 6-5·6-7, insert·반환 행·201 응답 |
| 12 | DB 요청의 실패 처리 | Step 6-1·6-3, 정상 처리의 400·404·503 분기 |
| 13 | 서버 구현 후 연결 검증 | Step 7→8, typecheck·test·build → db:check → 서버·API 조회 |
| 14 | 재시작 후 데이터 보존 확인 | Step 9, 개발 서버 종료·빌드 서버 실행·같은 ID 비교 |
| 15 | React 화면까지 데이터 연동 확인 | Step 10, 실제 클라이언트 getData·useQuery·필터와 성공 기준 |
| 16 | 현재 API의 사용자 권한 검사 범위 | DB 설정과 별개인 API 호출자 확인의 현재 한계 |

DB 권한은 테이블 준비 직후에 배치했다. `.env` 로딩은 README의 파일 작성 번호보다 런타임 준비 관계를 우선해 SDK 설정 장에 함께 설명한다. Model 변환은 Service 사용 전에 준비하며, 등록은 입력 행 구성과 DB 저장으로 나눈다. 기존 오류 장에 섞여 있던 연결 점검은 구현 뒤·영구 저장 검증 앞으로 옮겼다. 마지막에는 DB 설정을 반복하지 않고 사용자 로그인·관리자 권한 검사의 현재 범위를 짚는다.

프로젝트 생성·패키지 설치·Git·배포 대시보드 조작은 반복하지 않는다. 세션·JWT·인증 미들웨어 구현은 8주차 본 강의에서 다룬다.

## 작성 원본과 실행 범위

- 서버 원본: `pwd-week7`, 커밋 `9954b9715ce0fe12ca15ac35dcd802e95c9bece1`
- 클라이언트 원본: `pwd-week7-client`, 커밋 `6f8237fb43822576ad11970696c3779c6530b858`
- `../scripts/lesson.py`: 한영 제목·리드·본문·배치·출처
- `../scripts/excerpts.py`: 서버·클라이언트 실제 파일의 발췌 범위
- `code-excerpts.json`: 16개 발췌의 원본·행 번호·SHA-256, 두 저장소의 커밋
- `sql-evidence.json`: 원본 schema/seed SQL을 PGlite 임시 디스크 DB에서 실행한 결과·소스 해시
- `slide-map.json`: 화면 번호·제목·출처
- `content-review.ko.md`: 개발 순서·내용·검증 범위 기록
- `../scripts/build-slides.py`: 공통 생성기에 코드 서식·실행 결과 블록을 추가하는 진입점

TypeScript 코드는 실제 구현에서 발췌하고 공용 Prettier 설정으로 공백·줄바꿈만 정리한다. SQL 권한 코드는 비공백 토큰을 보존하면서 긴 줄만 개행한다. 불연속 발췌의 원본 범위는 숨김 노트에 기록한다. DB 타입 코드는 전체 Row·Insert를 유지하며 해당 장의 코드 열을 조금 넓혀 공용 글자 크기를 유지한다.

화면의 결과는 **로컬 SQL 실행 결과**다. SDK→Supabase Data API의 실제 HTTP 응답이나 클라우드 재시작 캡처가 아니다. 13장은 실제 연결의 확인 절차, 14장은 서버 재시작 절차와 별도로 수행한 로컬 DB 종료·재개방 결과, 15장은 실제 클라이언트 코드와 README의 화면 확인 기준이다. 검증하지 않은 클라우드·화면 결과를 성공했다고 표시하지 않는다.

일반 맛집 API는 DB를 사용하지만 `sync-demo`는 별도 메모리 스냅샷을 사용한다. 인기 목록 정렬은 현재 Service에서 수행한다. 제보·화면 좋아요는 localStorage를 유지한다. DB의 likes 열을 화면 좋아요 연동으로 설명하지 않는다. 수정·삭제 API나 사용자 인증이 구현되었다고 설명하지 않는다.

## 재생성·검증

동결한 코드·SQL 근거를 사용하므로 재생성에는 실습 저장소나 DB 연결이 필요 없다. `packages/web-deck`의 개발 의존성은 필요하다.

```sh
python3 lectures/08/lab-review/scripts/build-slides.py
python3 lectures/08/lab-review/scripts/build-slides.py --check
node packages/web-deck/scripts/code-examples.cjs --check --lecture 08
npm test --prefix packages/web-deck
```

원본 변경 시 발췌와 SQL 근거를 함께 갱신한다. 기본 원본은 이 저장소의 형제 폴더 `pwd-week7`·`pwd-week7-client`다. 다른 위치는 `--server-root`·`--client-root`와 `SERVER_ROOT`로 지정한다. SQL 실행에는 서버 저장소에 설치한 PGlite가 필요하다.

```sh
python3 lectures/08/lab-review/scripts/prepare-code.py
node lectures/08/lab-review/scripts/capture-sql.cjs
python3 lectures/08/lab-review/scripts/build-slides.py
```

실습 원본 검사는 `pwd-week7`에서 `npm test`·`npm run typecheck`를 사용한다. Jest의 DB 응답 대역 28건과 PGlite SQL 6건이며 클라우드 연결 검사는 포함하지 않는다.

화면 검사는 저장소 루트의 로컬 HTTP 서버에서 수행한다. 직접 실행한 서버는 검사 후 종료하고 프로세스 종료·포트 해제를 확인한다.

```sh
DECK_PATH=lectures/08/lab-review DECK_URL=http://127.0.0.1:4318 \
  PLAYWRIGHT_PATH=/path/to/playwright REVIEW_OUTPUT=/tmp/pwd-week8-lab-review-v2 \
  node packages/web-deck/tests/authoring-layout.cjs
```

공식 API 설명은 숨김 노트에 보관한다. 최초 작성 시 [Supabase Data API](https://supabase.com/docs/guides/api), [서버 키와 역할](https://supabase.com/docs/guides/getting-started/api-keys), [JavaScript select](https://supabase.com/docs/reference/javascript/select), [PostgreSQL identity](https://www.postgresql.org/docs/current/ddl-identity-columns.html)를 확인했다. 이번 재작성의 기준은 같은 커밋의 README·실제 소스와 사용자의 개발 흐름 평가다.
