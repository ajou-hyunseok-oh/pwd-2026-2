# 06주차 클라이언트 코드 리뷰

[한·영 슬라이드](../index.html)는 표지 포함 8장이다. 05주차의 공용 스타일과 2026학년도 2학기·6주차 표지를 사용한다. 기존 06주차의 PDF 기반 Express 강의 27장은 별도로 유지한다. 강의 목록의 06주차에서 두 덱을 선택할 수 있다.

`pwd-week5`의 README 예제가 아닌 실제 `src/` 구현을 기준으로 작성했다. 실제 앱의 홈·목록·한식 필터·상세·제보 입력과 완료·제보 관리·인기 화면을 캡처했다. 각 이미지를 클릭하면 원래 크기로 확인할 수 있다. 캡처는 내용에 맞는 화면 상단을 사용하며 브라우저 화면을 재구성하지 않는다.

설명·코드와 화면을 다시 대조해 캡처 범위를 교정했다. 라우팅 장은 Header·목록·footer가 함께 보이는 화면, 폼 장은 실제 메뉴 입력란과 저장 완료 화면, 서비스 장은 `getRestaurants()`가 반환하는 맛집 관리 표를 사용한다. 마지막 장은 같은 제보 URL을 연 두 독립 브라우저의 1건·0건 비교로 브라우저별 저장의 한계를 보여준다. 프로젝트 장의 홈 화면은 App의 렌더링 결과이며 진입 파일이나 폴더 구조 자체의 화면으로 설명하지 않는다.

필터 캡처는 CSS 전환이 끝난 뒤 한식 버튼 활성·전체 버튼 비활성·한식 카드 1개를 함께 확인한다. 이전 캡처는 카드가 먼저 바뀌고 버튼의 0.3초 색상 전환이 끝나기 전에 촬영되어 화면 상태가 어긋났으므로 교체했다. 화면의 요소를 확인하는 이 절차는 레이아웃 검사와 별도로 수행한다.

1. 표지
2. React 프로젝트의 실행 구조
3. 공통 레이아웃과 페이지 라우팅
4. 목록과 카드의 컴포넌트 분리
5. 조회 데이터와 화면 상태
6. 제보 폼의 저장 흐름
7. 서비스 함수의 데이터 접근
8. 서버가 맡을 데이터 책임

현재 코드는 HTTP 요청 없이 브라우저 저장소에서 동작한다. `restaurantAPI`·`submissionAPI`라는 이름만으로 서버가 연결된 것으로 설명하지 않는다. 제보 폼은 `useForm`과 직접 `await` 호출을 사용한다. 좋아요는 서비스 계층을 거치지 않고 카드에서 별도 저장한다. 인기 목록은 `rating` 내림차순으로 최대 5개를 반환하며, 화면 제목과 달리 주간 집계는 구현되어 있지 않다. 서버 책임 표는 향후 변경 범위이며 현재 앱에 구현된 기능이 아니다.

## 작성 원본

- `../scripts/lesson.py`: 제목·설명·배치·코드 발췌 범위
- `code-excerpts.json`: 실제 소스 발췌, 원본 파일 SHA-256과 행 번호
- `screens/`: 실제 앱 화면의 PNG
- `capture-manifest.json`: 캡처 조건·소스 해시·행동 검증 결과
- `slide-map.json`: 슬라이드별 스크린샷·캡션·코드 발췌·출처 대응

코드와 화면의 스냅샷을 함께 보관하므로 이 강의 저장소만으로 슬라이드를 다시 생성할 수 있다. 원본 클라이언트 변경 사항을 반영할 때는 화면 캡처와 코드 추출을 함께 갱신한다. 소스 발췌는 공용 Prettier 설정으로 들여쓰기와 줄바꿈만 정리한다. 페이지의 전체 구현을 복사하지 않으며, 각 코드의 라벨에 발췌 범위를 표시한다.

## 재생성

저장소 루트에서 실행한다. `packages/web-deck`의 개발 의존성이 필요하다.

```sh
python3 lectures/06/client-review/scripts/build-slides.py
python3 lectures/06/client-review/scripts/build-slides.py --check
npm test --prefix packages/web-deck
```

원본 앱을 다시 캡처할 때는 별도 터미널에서 `pwd-week5`의 Vite 서버를 실행한다.

```sh
# pwd-week5에서 실행
npm run dev -- --host 127.0.0.1 --port 5176 --strictPort
```

강의 저장소에서 코드 추출·캡처·슬라이드 생성을 실행한다. 캡처는 새 브라우저 컨텍스트에만 제보와 좋아요를 저장하며 사용자의 기존 브라우저 데이터나 클라이언트 소스를 수정하지 않는다. 기본 클라이언트 경로는 이 저장소와 같은 상위 폴더의 `pwd-week5`다. 다른 위치는 `--client-root`와 `CLIENT_ROOT`로 지정한다.

```sh
python3 lectures/06/client-review/scripts/prepare-code.py
PLAYWRIGHT_PATH=/path/to/playwright node lectures/06/client-review/scripts/capture-app.cjs
python3 lectures/06/client-review/scripts/build-slides.py
```

저장소 루트 HTTP 서버를 실행한 뒤 기존 05주차와 같은 화면 검사를 사용한다.

```sh
DECK_PATH=lectures/06/client-review DECK_URL=http://127.0.0.1:4306 PLAYWRIGHT_PATH=/path/to/playwright node packages/web-deck/tests/authoring-layout.cjs
```

공용 `npm test`는 기존 회차 덱을 검사한다. 이 하위 덱은 생성물 대조와 위 `DECK_PATH` 화면 검사로 별도 확인한다.
