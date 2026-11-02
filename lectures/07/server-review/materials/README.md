# 07주차 — 6주차 Foodmap API 실습 리뷰

[한·영 슬라이드](../index.html)는 표지 포함 9장이다. 06주차의 [5주차 클라이언트 리뷰](../../../06/client-review/index.html)에서 표지·공용 스타일·설명과 코드의 두 열 배치·실행 결과 대조 방식을 재사용했다. 표지는 2026학년도 2학기·7주차이며, 복습 대상은 6주차다. 기존 07주차 DB 이론 덱과 분리한다.

내용은 실제 `pwd-week6` 소스(커밋 `1694d566e1518aa996653ddbf2a92724524f6a05`)와 실행 결과를 기준으로 한다. 철회된 `lectures/06/examples`를 실습 원본으로 사용하지 않는다. API 서버에는 UI가 없으므로 06주차 리뷰의 클라이언트 화면 대신 실제 HTTP 상태·응답을 배치했다. 실행 결과는 `samp`, 소스 코드는 공용 `pre.wd-code`로 구분한다.

| 화면 | 제목 | 코드·관찰 대상 |
| --- | --- | --- |
| 1 | 표지 | 7주차 강의·6주차 실습 리뷰 |
| 2 | 서버 실행 준비 | 앱 생성·포트 대기·/health로 시작 확인 |
| 3 | 클라이언트의 목록 조회 요청 | README의 Axios 연동 예제·GET /api/restaurants 출발 |
| 4 | Express의 요청 수신 | 같은 GET 요청의 공통 미들웨어·맛집 Router 연결 |
| 5 | Router와 Controller의 요청 연결 | 목록 경로 선택·getAllRestaurants 호출 |
| 6 | Service의 목록 조회와 응답 완료 | 메모리 목록 → HTTP JSON → 클라이언트 데이터까지 완결 |
| 7 | 생성 요청에서 달라지는 처리 | GET과 비교한 입력 변환·필수 값 확인·추가·201 응답 |
| 8 | 실패했을 때의 처리 | 정상 요청의 400·404 분기와 비동기 오류 전달 |
| 9 | 메모리 저장의 한계 | 성공한 변경의 재시작 후 소멸·DB 영구 저장의 필요성 |

## 설명의 진행 기준

서버 시작은 요청 수신 전의 준비 과정으로 한 번 설명한다. 3~6장은 GET /api/restaurants 한 요청이 클라이언트 → 미들웨어 → Router·Controller → Service → 응답 수신으로 진행한다. 같은 흐름도에서 현재 위치를 강조하고, 6장에서 Service의 배열·Controller의 JSON·Axios가 읽는 본문을 연결해 조회를 마무리한다.

7장은 같은 구조에 추가되는 생성 처리만 GET과 비교한다. 8장은 정상 흐름에서 갈라지는 실패 경로만 설명한다. 계층의 역할을 처음부터 다시 소개하지 않는다. 9장은 완료된 요청의 저장 수명으로 범위를 바꾸어 DB 강의에 연결한다. 각 장에서 설명·비교는 왼쪽, 코드·요청·실행 결과는 오른쪽에 배치한다.

## 내용의 범위

- 서버의 현재 구현과 README의 클라이언트 적용 예제를 구분한다. 3장 코드는 README 발췌로 표시하며, 현재 `pwd-week5`에 HTTP 연동이 적용되어 있다고 주장하지 않는다.
- 이번 연동의 맛집 조회·생성은 서버 API, 제보·좋아요는 브라우저 저장소다. 서버의 맛집 수정·삭제 API는 없으며 README는 해당 버튼을 비활성화하도록 안내한다.
- `getAllRestaurants()`는 요청마다 파일을 읽지 않는다. 메모리 캐시를 복사하며 20ms 타이머로 비차단 지연을 시뮬레이션한다. 실제 I/O 비교 성능이나 DB 응답 시간으로 설명하지 않는다.
- 생성 시 필수 값의 존재를 확인한다. 임의 JSON 전체에 대한 완전한 런타임 타입 검증으로 설명하지 않는다.
- 공유 여부와 영구 저장은 다르다. 동일 프로세스의 별도 HTTP 요청은 생성한 맛집을 조회할 수 있지만 새 프로세스는 JSON 시드만 복원한다.

## 작성 원본과 근거

- `../scripts/lesson.py`: 제목·설명·레이아웃·코드 발췌 범위
- `code-excerpts.json`: 실제 소스 발췌, 행 번호, 전체 파일 SHA-256
- `runtime-evidence.json`: 임시 API 프로세스의 요청 14건·상태·전체 응답·소스 해시·실행 조건
- `slide-map.json`: 슬라이드별 제목·리드·코드·실행 결과·출처 대응
- `../scripts/build-slides.py`: HTML·KO/EN·슬라이드 맵 생성
- [내용·화면 검토](content-review.ko.md): 설명과 코드·응답의 대응 및 검증 범위

6장은 목록 응답의 id·name만 발췌하고, 7장은 생성 응답의 id·recommendedMenu만 발췌한다. 전체 응답은 실행 근거에 보관한다. 실행 근거의 14개 요청 중 시작 확인·목록·생성·실패·재시작 결과를 본문에 선택해 사용한다. 9장의 목록 수는 실제 배열 길이이며 상세 HTTP 상태와 구분한다. 원본 발췌는 공용 Prettier 설정으로 공백·줄바꿈만 정리한다.

## 영어 번역·용어 설명

2026-11-02 검토를 반영했다. CORS의 전체 이름과 출처, MVCS의 구성 역할, Promise·await·메모리 캐시, Axios, 시드, 프로세스·영구 저장, next(error)·stack trace를 본문에서 짧게 설명한다. 메뉴 입력 처리는 ‘입력 형식 통일’로 표현해 DB 정규화와 구분한다.

영문에는 불필요하게 어려운 app factory·projection 대신 앱 생성 함수·발췌 필드를 직접 나타내는 표현을 사용한다. 사용자의 배포 슬라이드 제거와 설명 흐름 재구성 지시를 반영했으며, 현재는 표지 포함 9장이다. 요청 흐름도의 단계와 강조 위치도 한영에서 일치한다.

## 재생성·검사

저장소 루트에서 실행한다. 기본 재생성은 동결한 코드와 응답을 사용하므로 실습 저장소나 실행 서버가 필요하지 않다. `packages/web-deck`의 개발 의존성은 필요하다.

```sh
python3 lectures/07/server-review/scripts/build-slides.py
python3 lectures/07/server-review/scripts/build-slides.py --check
node lectures/07/server-review/scripts/check-review.cjs
npm test --prefix packages/web-deck
```

원본 실습이 변경되었다면 코드와 실행 근거를 함께 갱신한다. 기본 원본 경로는 이 저장소와 같은 상위 폴더의 `pwd-week6`다. 다른 위치는 `--server-root`와 `SERVER_ROOT`로 지정한다.

```sh
python3 lectures/07/server-review/scripts/prepare-code.py
node lectures/07/server-review/scripts/capture-runtime.cjs
python3 lectures/07/server-review/scripts/build-slides.py
SERVER_ROOT=/path/to/pwd-week6 node lectures/07/server-review/scripts/check-review.cjs
```

실행 기록은 `tsx`로 실제 소스의 새 프로세스를 두 번 구동한다. OS가 배정한 로컬 포트를 사용하며 생성은 임시 프로세스 메모리에만 반영한다. 원본·시드 파일의 해시가 실행 전후 일치하는지 확인하고 프로세스를 종료한다. 외부 Render API나 사용자의 실행 중인 서버에 접근하지 않는다.

저장소 루트 HTTP 서버를 실행한 뒤 발표·인쇄·모바일 검사를 실행한다. 공용 `npm test`의 번호별 덱 검사에는 이 하위 덱이 포함되지 않으므로 위 전용 검사와 아래 화면 검사를 함께 실행한다.

```sh
DECK_PATH=lectures/07/server-review DECK_URL=http://127.0.0.1:4307 PLAYWRIGHT_PATH=/path/to/playwright REVIEW_OUTPUT=/tmp/pwd-week7-server-review node packages/web-deck/tests/authoring-layout.cjs
```

강의 목록에 이 리뷰와 DB 이론 덱 링크를 제공한다. `released-lectures.txt`의 공개 주차 목록은 변경하지 않는다.
