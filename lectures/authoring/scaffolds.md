# 8·9주차 슬라이드 작성 틀

6주차 `client-review`·7주차 `server-review`의 **전주 실습 리뷰 / 해당 주 강의** 분리와 05~07의 공통 디자인을 재사용한다. 기본 작성 틀은 3장(주차 표지 → 단원 표지 → 빈 본문)이며, 대괄호 문구는 입력 자리다. 8주차 강의는 확정한 60개 본문 제목과 재사용 자료를 배치한 68장, 9주차 강의는 76개 본문 제목과 재사용 자료를 우선 배치한 85장이다. 8주차의 실습 리뷰는 README의 개발 흐름과 실제 `pwd-week7`·클라이언트 코드·SQL 근거를 담은 한·영 16장이며, 9주차의 실습 리뷰는 기본 작성 틀을 유지한다. 최신 작성 범위는 각 덱의 자료 안내에서 확인한다.

| 회차 | 전주 실습 리뷰 | 해당 주 강의 |
| --- | --- | --- |
| 8주차 | [7주차 실습 리뷰](../08/lab-review/index.html) | [8주차 강의](../08/index.html) |
| 9주차 | [8주차 실습 리뷰](../09/lab-review/index.html) | [9주차 강의](../09/index.html) |

## 원본과 생성 결과

- 각 덱의 `scripts/lesson.py`: 주차·표지 부제·슬라이드 순서·한영 본문·출처의 편집 원본
- 각 덱의 `scripts/build-slides.py`: [공통 생성기](deck_builder.py)를 호출하는 진입점
- 생성 결과: `index.html`, `lecture-content.js`, `materials/slide-map.json`
- 공통 디자인: `packages/web-deck/web-deck.css` + `authoring.css`. 회차별 CSS 복사본 없이 동일한 형식 적용

슬라이드를 추가할 때 `SLIDES` 안의 항목을 복제하고 `id`를 고유하게 변경한다. `kind='chapter'`는 단원 표지, `kind='content'`는 본문이다. 단원 번호·슬라이드 맵·번역·한국어 HTML 기본값은 함께 생성된다. 제목과 학습 순서는 확정한 자료를 기준으로 입력하며, 본문 작성 전 [작성 하네스](README.md)를 적용한다. 생성된 HTML만 직접 수정하지 않는다.

표지에는 2026학년도 2학기·현재 주차·`LECTURE NN`을 자동 적용한다. 실습 리뷰의 부제에는 전주 번호를 사용한다. 현재의 일반 부제는 주제 확정 후 `SUBTITLE`에서 바꾼다. 제목에 적합한 독립 개념 하나를 정한 뒤 제목·리드·본문을 작성한다.

## 글머리표와 본문 형식

- `concepts`: `dt > strong`의 **개념 - 짧은 정의**, `dd > ul > li`의 들여쓴 세부 설명
- `wd-lesson-concepts--bulleted`: 세부 설명에 원형 글머리표 적용. 이전 강의에는 자동 적용하지 않는 선택 클래스
- 나열은 ` · `, 처리 순서는 ` → `. 코드·URL·식별자의 기호는 보존
- 비교는 `table`, 순서는 `steps`, 코드 사례는 `code`, 이미지·도식·실행 화면은 `figure`
- 항목 수와 코드 유무는 내용에 맞게 선택. 불필요한 자리 표시 블록·대괄호 문구는 실제 작성 시 제거
- 출처와 제작 메모는 `sources`·`note`에 입력. 숨김 노트와 슬라이드 맵으로 보관

`layout`은 `single`(열 1개), `split`(동일 폭 2열), `code`(설명 열이 조금 넓은 2열), `visual`(첫 열이 넓은 2열) 중 선택한다. `columns`의 각 목록이 한 열이며, 한 열에 블록 여러 개를 배치할 수 있다. 모바일에서는 한 열로 배치된다.

개별 회차의 편집 가능한 도식은 `build(..., render_extra=..., stylesheets=(... ,))`로 확장할 수 있다. 추가 렌더러는 `(item, key, tr)`를 받고 지원하지 않는 종류는 `None`을 반환한다. 모든 화면 문자열은 공용 `tr` 바인딩을 사용하며, 전용 CSS는 해당 덱에서만 불러온다. 08의 `resource_blocks.py`·`resources.css`가 원본 시퀀스와 로그인 화면을 재구성한 사례다. 공용 블록·기존 덱의 기본 출력에는 영향을 주지 않는다.

## 선택 블록

아래 예시는 `lesson.py`의 `columns` 안에 넣을 수 있는 **자료 입력 틀**이다. 실제 강의 내용이나 실행 가능한 예제를 뜻하지 않는다. 모든 화면 문구는 `(한국어, 영어)` 쌍으로 작성한다.

```python
# 개념 설명 — 개수는 필요한 만큼만 지정
dict(kind='concepts', items=[
    dict(term=('[개념] - [짧은 정의]', '[Concept] - [Short Definition]'),
         details=[('[세부 설명]', '[Supporting Detail]')]),
])

# 코드 — 확정한 예제를 입력한 뒤 실제 언어로 변경
dict(kind='code', label=('[파일명 · 역할]', '[File · Role]'),
     language='text', width=64,
     text=('[코드]', '[Code]'))

# 비교 표 — 각 행의 셀 수는 머리글과 동일
dict(kind='table',
     head=[('[비교 기준]', '[Criterion]'), ('[대상]', '[Subject]')],
     rows=[[( '[항목]', '[Item]'), ('[설명]', '[Description]')]])

# 실행 순서 — 공통 번호 목록 사용
dict(kind='steps', items=[
    dict(title=('[단계]', '[Step]'), body=('[처리 내용]', '[Operation]')),
])

# 이미지 — 파일 경로는 해당 덱 기준, 실제 파일을 먼저 추가
dict(kind='figure', src='materials/images/figure.png',
     alt=('[이미지 설명]', '[Image Description]'),
     caption=('[그림 제목]', '[Figure Caption]'))
```

코드는 검정 배경·녹색·Consolas 우선, 0.7rem / 1.45를 공통 적용한다. `width`는 32~80자이며, 설명을 줄이기 위해 글자 크기를 축소하지 않는다. 비교·그림·코드는 개념 설명에 필요한 경우에만 선택한다.

## 생성과 확인

저장소 루트에서 실행한다.

```sh
python3 lectures/08/scripts/build-slides.py
python3 lectures/08/lab-review/scripts/build-slides.py
python3 lectures/09/scripts/build-slides.py
python3 lectures/09/lab-review/scripts/build-slides.py
npm test --prefix packages/web-deck
```

각 생성기의 `--check`는 파일을 쓰지 않고 원본과 생성 결과의 일치를 확인한다. 본문 장수가 바뀌면 기존 회차와 마찬가지로 `packages/web-deck/tests/validate.cjs`의 해당 회차 장수도 갱신한다. 코드를 추가한 경우 공용 포매터로 서식을 확인하고, 포매터가 고친 결과를 `lesson.py`의 원문에도 반영해 재생성이 유지되게 한다.

```sh
node packages/web-deck/scripts/code-examples.cjs --write --lecture 08
node packages/web-deck/scripts/code-examples.cjs --write --lecture 09
```

위 포매터는 회차의 메인 덱과 `lab-review`를 함께 검사한다. 공용 `npm test`에도 네 덱의 작성 형식과 코드 검사가 포함된다.

로컬 HTTP 서버를 실행한 뒤 각 덱의 KO/EN 발표·인쇄·모바일을 공용 검사기로 확인한다. `PLAYWRIGHT_PATH`에는 설치된 Playwright 경로를 지정한다.

```sh
python3 -m http.server 4305
# 다른 터미널, 아래 DECK_PATH를 네 덱으로 각각 변경
DECK_PATH=lectures/08 DECK_URL=http://127.0.0.1:4305 \
  PLAYWRIGHT_PATH=/path/to/playwright \
  node packages/web-deck/tests/authoring-layout.cjs
```

나머지 경로는 `lectures/08/lab-review`, `lectures/09`, `lectures/09/lab-review`다. 발표 화면에서 키보드 이동·한영 전환·홈 링크·PDF 인쇄를 확인한다. 초안 준비만으로 본문 내용 검토를 완료한 것으로 기록하지 않는다. 공개 여부는 기존 `released-lectures.txt`가 관리한다.
