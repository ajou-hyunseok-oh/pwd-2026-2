# Foodmap API 별도 실행 예제

이 예제는 철회된 50장 재구성 초안을 위해 추가했던 자료다. 현재 원본 보존 강의의 본문이나 원본 코드가 아니다. 원본 PDF를 대신하는 작성 기준으로 사용하지 않는다.

초안의 MVC/MVCS·검증·오류 처리·테스트를 위한 별도 소스다. 2026-10-15 재검토 기준 Node.js 24.22.0 LTS, Express 5.3.0, cors 2.8.6을 사용한다. Node 버전은 `.node-version`과 `engines: 24.x`, 패키지 버전은 `package-lock.json`으로 관리한다. 데이터는 프로세스 메모리에만 보관하며 앱을 새로 만들거나 서버를 재시작하면 초기화한다.

```sh
cd lectures/06/examples
npm ci
npm test
npm start
```

서버 기본 주소는 `http://localhost:3000`이다. 허용된 브라우저 개발 출처는 `http://localhost:5173`이다. 기본 데이터는 `{ "id": 1, "name": "Campus Noodles" }` 한 건이다.

| 요청 | 결과 |
| --- | --- |
| `GET /health` | 200 · `{ "status": "ok" }` |
| `GET /foods` | 200 · 맛집 배열 |
| `GET /foods/1` | 200 · 개별 맛집 |
| `POST /foods` | JSON의 `name`으로 생성 · 201 · `Location: /foods/:id` |
| 잘못된 식별값·빈 이름·잘못된 JSON | 400 · JSON 오류 |
| 없는 리소스·라우트 | 404 · JSON 오류 |
| 처리 중 예상하지 못한 오류 | 500 · 공개용 오류 메시지 |

```sh
curl -i http://localhost:3000/foods
curl -i -X POST http://localhost:3000/foods \
  -H 'Content-Type: application/json' \
  -d '{"name":"Campus Rice"}'
curl -i http://localhost:3000/foods/2
```

HTTP 메서드 슬라이드의 PUT·DELETE는 설계 의미를 비교하는 사례다. 이 실행 예제의 구현 범위는 목록·상세·생성이다. 프런트엔드에서는 응답 상태를 확인한 뒤 JSON을 읽고 React 상태에 반영한다. JSON POST의 CORS 사전 요청은 `cors` 미들웨어가 처리한다.

`server.cjs`는 실행 설정과 포트 대기, `src/app.cjs`는 앱 조합을 담당한다. 라우트 → 컨트롤러 → 서비스 → 모델 순서로 연결하며 생성 시 의존 객체를 전달한다. 테스트는 새 앱과 모델을 만들어 서로의 데이터에 영향을 주지 않게 실행한다.

Render에 이 저장소를 연결할 경우 Root Directory는 `lectures/06/examples`, Build Command는 `npm ci`, Start Command는 `npm start`, Health Check Path는 `/health`다. 환경변수 `NODE_VERSION=24.22.0`과 `CLIENT_ORIGIN=실제 프런트엔드 출처`를 지정한다. 서버는 Render가 제공한 `PORT`를 읽고 `0.0.0.0`에서 대기한다. 별도 저장소로 예제 폴더만 옮겼다면 Root Directory는 해당 저장소 루트다.

무료 웹 서비스는 15분간 요청이 없으면 중지하며, 다음 요청 때 재기동 대기 시간이 발생할 수 있다. 무료 인스턴스 시간은 워크스페이스당 월 750시간을 공유한다. 무료 인스턴스의 로컬 파일은 재시작·재배포·유휴 중지 때 보존되지 않으며 영구 디스크와 여러 인스턴스로의 확장은 지원하지 않는다. 이는 [현재 무료 서비스 조건](https://render.com/docs/free)을 확인한 안내이며 2026년에 새로 생긴 정책이라는 뜻은 아니다.

현재 강의의 코드는 원본 PDF에서 보존하므로 이 소스를 변경해도 강의 본문을 바꾸지 않는다.
