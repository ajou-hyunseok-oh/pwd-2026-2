# 05회차 자료 — React Framework의 이해

[강의 슬라이드](../index.html)는 **65장 한·영 HTML 강의**입니다. 강의 표지 1장, 04의 「React 기초」 24장, 챕터 02~04의 표지 3장과 개념별 본문 35장, 생태계 부록 1장, 실습 안내 1장으로 구성합니다. 현재 본문 범위는 React 기초·컴포넌트·JSX·상태·Hooks입니다.

| 화면 번호 | 구간 | 구성 |
| --- | --- | --- |
| 1 | 강의 표지 | 1장 |
| 2–25 | 01. React 기초 | 04 원본 24장 · 아래의 05 전용 예외 적용 |
| 26–41 | 02. 컴포넌트와 JSX | 챕터 표지 1장 + 본문 15장 |
| 42–54 | 03. 상태 기반 화면 갱신 | 챕터 표지 1장 + 본문 12장 |
| 55–63 | 04. Hooks | 챕터 표지 1장 + 본문 8장 |
| 64 | React 생태계 부록 | 원본 PDF 이미지 + 우측 package.json 오버레이 |
| 65 | 실습 안내 | pwd-week5 · 아주 캠퍼스 푸드맵 |

슬라이드 번호는 **강의 표지와 챕터 표지를 포함한 화면 번호**입니다. [slide-map.json](slide-map.json)에 현재 번호·안정적인 ID·제목·서브타이틀·출처를 기록합니다. 본문 개념은 `concept-*` ID로 식별합니다. 과거 기록의 화면 번호는 해당 기록 작성 당시의 덱을 기준으로 하므로 현재 번호와 구분합니다.

## 작성 원본과 기준

[공통 작성 하네스](../../authoring/README.md), [1개념 1슬라이드 원칙](../../authoring/one-concept.md), [개념 설명 작성 기준](../../authoring/body-explanation.md)을 적용합니다. 확정된 제목·순서·범위·사례를 유지하고, 본문의 개념·구성 요소·관계를 코드와 실행 결과에 대조합니다. 설명·코드·표·흐름·실행 이미지는 해당 개념에 맞춰 선택합니다.

| 작성 원본 | 역할 |
| --- | --- |
| `../scripts/title_outline.py` | 확정 제목·서브타이틀·과거 주제 대응 |
| `../scripts/slide_body.py` | 35개 개념의 한·영 본문·예제·공식 출처 |
| `../scripts/lesson.py` | 강의 표지·가져온 24장·본문·부록·실습의 조합 |
| `../scripts/react_import.py` | 04 원본과 번역 가져오기, 05 전용 예외 적용 |
| `../scripts/vite_setup.py` | 화면 24의 Vite 대화형 메뉴와 실제 선택 로그 |
| `../scripts/vite_edit.py` | 화면 25의 Hello, World! 전체 교체 코드 |
| `../scripts/practice_guide.py` | 화면 65의 실습 요구사항·마감·제출물 |
| `../scripts/build-slides.py` | HTML·번역·슬라이드 맵·제목 자료 생성 |

[확정 제목표](week-05-titles.ko.txt)와 [제목만 보기](../titles.html)는 실제 덱과 같은 순서입니다. [title-outline.json](title-outline.json)은 제목의 한·영 데이터와 과거 주제 대응을 담습니다. [pre-concept-slide-map.json](pre-concept-slide-map.json)은 분할 전 61장 덱의 기록이며 현행 번호표가 아닙니다.

04의 [React 기초](../../04/index.html)와 `[PWD Week 3] React 프레임워크를 이용한 웹 프론트엔드 개발.pdf`를 참고 자료로 보존합니다. API 설명의 공식 문서 출처는 각 슬라이드의 숨김 노트와 슬라이드 맵에 기록합니다.

## 첫 번째 챕터의 원본 보존과 예외

04의 24장 전체를 같은 순서로 사용하며, 04 원본 파일은 유지합니다. 05에서만 다음 예외를 적용합니다.

- 화면 4 · `slide-03`: 한국어와 의미가 달랐던 영어 문장 1개 교정. [교정 명세](import-text-corrections.json)에 원문·교정문·키를 기록하고 나머지 문구·구조·디자인 유지.
- 화면 24 · `slide-23`: Vite 대화형 선택 로그와 각 선택 항목의 의미로 교체. [실제 메뉴 기록](vite-create-console.txt) 보관.
- 화면 25 · `slide-24`: `src/App.tsx` 전체를 [Hello, World! 코드](vite-hello-App.tsx)로 교체하고 실제 실행 이미지 표시. `main.tsx`·`index.css`는 생성 기본값 유지.

04의 CSS 2개와 데모 실행 파일을 재사용합니다. 정적 상대 주소만 조정하고, 문서 기준 주소를 사용하는 Hello World 이미지 2개는 원본과 같은 바이트로 복사합니다. 원본 표지의 `LECTURE 04` 표기도 보존합니다. [최초 Vite 생성 코드](vite-default-App.tsx)와 과거 화면 캡처는 이력 자료입니다.

## 코드와 실행 조건

공용 `pre[data-wd-code]` 코드 블록은 **41개**입니다. 가져온 원본 구간 3개, 화면 24·25의 교체 블록 각 1개, 개념 본문 29장에 있는 36개를 합한 수입니다. 화면 64의 package.json은 별도 SVG 오버레이이므로 이 수에 포함하지 않습니다. 코드는 검정 배경·녹색 글자·Consolas 우선의 공용 서식을 사용합니다.

코드 라벨의 `.tsx`와 `.jsx`를 구분합니다. TSX는 JSX를 포함한 TypeScript 예제이고, JSX는 JavaScript 예제입니다. JSX 예제를 TypeScript 파일에 복사할 때는 Props 등에 필요한 타입을 추가해야 합니다. 컴포넌트 파일 분리 예제의 `ProductRow.tsx`와 `App.tsx`는 함께 사용합니다. 조건부 렌더링 예제의 `product`는 전달받는 입력이며, 반환된 상품 행에는 `table`·`tbody` 문맥이 필요합니다.

표시된 실행 결과는 해당 장에 적힌 초기 상태와 사용자 행동을 기준으로 읽습니다. 개발 모드의 루트 StrictMode에서는 Render·Effect의 추가 확인 실행이 발생할 수 있으므로 콘솔 결과의 실행 조건을 함께 확인합니다.

## 부록과 실습

화면 64는 사용자 요청에 따라 원본 PDF 18쪽의 이미지와 배치를 유지하고, 우측 package.json만 최신 확인 버전으로 표시합니다. 작성 데이터는 [react-ecosystem-right-package.json](react-ecosystem-right-package.json), 버전 확인 기록은 [ecosystem-right-versions-2026.json](ecosystem-right-versions-2026.json)입니다. 원본 이미지의 한국어·학기 표기와 좌측 설명은 원본 보존 범위이며 영어 모드에서도 같은 이미지를 사용합니다.

화면 65의 실습 자료는 [pwd-week5 README](https://github.com/ajou-hyunseok-oh/pwd-week5#readme)입니다. 가상 맛집 목록, 필터·좋아요·인기 TOP 5·제보, 현재 브라우저의 저장 기능과 Vercel 배포를 안내합니다. 제출물은 GitHub 저장소 URL과 Vercel 서비스 URL이며, 마감은 **2026년 10월 18일 23:59 KST**입니다. 요구사항과 일정은 `practice_guide.py`의 한·영 데이터에서 함께 관리합니다.

## 생성과 검증

저장소 루트에서 실행합니다.

```sh
python3 lectures/05/scripts/build-slides.py
node packages/web-deck/scripts/code-examples.cjs --write --lecture 05
python3 lectures/05/scripts/build-slides.py --titles-only
npm test --prefix packages/web-deck
```

`npm test`는 구조·번역·한국어 HTML 기본값·코드 서식과 구문·작성 계약·가져오기 계약을 검사합니다. 문장의 의미와 기술적 정확성은 별도로 검토해야 합니다.

Chrome과 Playwright가 있는 환경에서 저장소 루트의 정적 서버를 실행한 뒤 브라우저 검사를 수행합니다.

```sh
python3 -m http.server 4305 --bind 127.0.0.1
```

별도 터미널에서 실행합니다.

```sh
node lectures/05/scripts/check-slides.cjs
node lectures/05/scripts/check-react-import.cjs
node lectures/05/scripts/check-examples.cjs
```

`PLAYWRIGHT_PATH`로 Playwright 패키지 경로를 지정할 수 있습니다. 예제 실행 검사는 기본적으로 `lectures/04/scripts/node_modules`의 React·React DOM·Vite를 사용하며, `REACT_MODULES`로 변경합니다. TypeScript 검사에는 `@types/react`가 필요하고, `REACT_TYPES`는 해당 패키지를 포함한 `node_modules/@types` 경로입니다. 코드 원문은 현재 생성된 슬라이드에서 추출하며 별도 예제 복사본을 유지하지 않습니다.

- `check-slides.cjs`: KO/EN 전체 65장의 실제 번역 텍스트·alt 등 속성 적용, 발표·1280×720 인쇄·390px 모바일 배치, 코드 넘침·잘림·겹침과 브라우저 오류 확인.
- `check-react-import.cjs`: 화면 24·25를 제외한 22장의 KO/EN × 발표/인쇄/모바일 대조. 화면 4의 영어 한 문장 교정만 동일하게 보정한 뒤 나머지 텍스트·요소 배치·이미지 비교. 가져온 검색·필터·경계 표시·DOM 유지·언어 전환 데모 확인.
- `check-examples.cjs`: 현재 React 주 예제 29개와 클래스 방식 보조 예제 1개의 실행, TSX 타입·모듈 연결, 상태 갱신·스냅샷·불변성·제어 입력·상태 공유와 초기화·Hook·Ref·Effect의 동작 확인. 일반 동작은 StrictMode를 사용하지 않는 환경에서 검사하며, 화면 45·60·61의 개발 StrictMode 결과는 별도 검사.

배치 검사의 기본 출력은 시스템 임시 폴더 `pwd-lecture-05/review`이며, `DECK_URL`과 `REVIEW_OUTPUT`으로 서버 주소와 산출물 경로를 변경할 수 있습니다. 원본 대조 검사의 기본 출력은 시스템 임시 폴더 `pwd-react-import`입니다. 예제 실행 검사는 기본적으로 `pwd-lecture-05/review/examples.json`에 결과를 저장하며 `REVIEW_OUTPUT`으로 출력 폴더를 변경합니다. 검사 명령이나 범위의 기재는 통과 결과를 뜻하지 않습니다.

## 검토 기록

현행 세부 교정과 실제 실행 결과는 [2026-10-12 세부 검토 기록](detail-review-2026-10-12.ko.txt)을 기준으로 확인합니다. [누적 검토 기록](content-review.ko.txt), [생명주기 검토](lifecycle-verification.ko.txt), [학습 흐름 검토](learning-flow-review.ko.txt), [실습 안내 검토](practice-guide-review.ko.txt)는 작성 당시의 판단과 검사 이력으로 보존합니다. 과거 번호·구성·예제·검사 결과를 현재 65장 덱의 상태로 해석하지 않습니다. `images/`의 과거 자료와 `capture-practice.cjs`도 이력으로 유지합니다.
