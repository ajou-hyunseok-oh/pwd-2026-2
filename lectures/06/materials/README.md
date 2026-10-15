# 06주차 — Node.js Express 프레임워크를 이용한 웹 서버 개발

06주차 도입에 사용하는 [클라이언트 코드 리뷰 · 8장](../client-review/index.html)을 별도 덱으로 제공한다. `pwd-week5`의 실제 실행 화면과 코드 발췌로 프로젝트 구성·라우팅·컴포넌트·조회와 필터·제보 폼·서버로 옮길 데이터 책임을 설명한다. [코드 리뷰 자료 안내](../client-review/materials/README.md)에 작성 원본과 재생성·검증 경로를 기록한다.

[강의 슬라이드](../index.html)는 **05주차 디자인·본문 정리 형식**으로 작성한 27장 한영 강의다. 제목·학습 내용·순서·코드·표·그림·실습은 제공된 `[PWD Week4] Node.js Express 프레임워크를 이용한 웹 서버 개발.pdf`를 따른다. 표지는 **2026학년도 2학기·6주차·LECTURE 06**이다.

PDF 페이지 전체를 표시하지 않는다. 원본의 텍스트·이미지·합성 도식·코드·표를 먼저 개별 추출하고, 05와 같은 제목·정의/세부 설명·글머리·표·검정/녹색 Consolas 코드 블록에 슬라이드별로 배치했다. 새 개념·제목·예제를 추가하지 않았다.

원문 210개 텍스트 단위와 원본 이미지 요소를 포함하는 19개 그림 배치, 코드 9개, 비교표 3개를 연결한다. HTTP 응답의 상태 코드 비교도 별도 HTML 표로 표시한다. 합성 그림은 여러 원본 이미지·벡터·라벨을 함께 포함하므로 그림 배치 수는 PDF 이미지 객체 수와 다르다. 반복 학교 로고와 2025년 머리말은 05의 표지·공용 발표 틀로 대체했다. 모든 학습용 이미지의 해당 페이지 맥락을 유지한다.

실습 목표·필수 구현·Foodmap 사례·기존 URL은 원본 그대로다. 원본의 9월 28일 마감도 날짜를 추정해 바꾸지 않고 **원본 자료 표기**로 구분한다. 현재 수업의 새 마감일을 확정한 표기가 아니다. Express 5.1.0 등 본문의 기술 값도 유지하며 [업데이트 검토](source-analysis/review.ko.md)는 별도 제안이다.

## 작성 경로

| 경로 | 역할 |
| --- | --- |
| `../scripts/prepare-assets.py` | PDF의 원문·코드·비교표·원본 이미지·합성 도식 준비 |
| `elements/manifest.json` | 페이지별 텍스트 단위·자산·코드·표·출처 좌표와 해시 |
| `elements/images/` | 원본 추출 이미지와 내용별 합성 그림 |
| `elements/code/` | 원본에서 추출한 코드·HTTP 메시지 |
| `elements/text-inventory.txt` | 원문 단위별 식별자와 내용 |
| `../scripts/lesson.py` | 원본 요소를 슬라이드별 레이아웃으로 조합 |
| `../scripts/translations.py` | 원문과 같은 범위의 영문 번역 |
| `../scripts/build-slides.py` | 05 형식의 HTML·번역·제목표·슬라이드 맵 생성 |
| `../scripts/check-source.py` | 원문 누락/대체·그림 맥락·코드·표 전체·제목·현재 표지·05 형식 확인 |

[제목표](week-06-titles.ko.txt), [제목 미리보기](../titles.html), [슬라이드 맵](slide-map.json)은 실제 덱과 같은 순서다. 원본 전체 분석은 [자료 목록](source-analysis/README.md)에 있다. `archive/page-svg-draft/`의 페이지 전체 SVG와 `archive/reconstructed-draft/`의 50장 초안은 현재 덱의 입력이나 디자인 기준으로 사용하지 않는다. `../examples/`는 별도 실행 예제이며 원본 실습을 대체하지 않는다.

## 생성과 확인

```sh
# 준비 단계: source-analysis-requirements.txt의 PyMuPDF 환경
python lectures/06/scripts/prepare-assets.py
# 이후 생성과 기본 대조는 Python 표준 라이브러리 사용
python3 lectures/06/scripts/build-slides.py
python3 lectures/06/scripts/check-source.py
npm test --prefix packages/web-deck
# PDF의 문자와 이미지 배치까지 직접 대조
python lectures/06/scripts/check-source.py --pdf
```

저장소 루트 HTTP 서버와 Playwright를 준비한 뒤 05와 같은 화면 검사를 실행한다.

```sh
DECK_URL=http://127.0.0.1:4306 PLAYWRIGHT_PATH=/path/to/playwright node lectures/06/scripts/check-slides.cjs
```

원본에서 가져온 코드는 내용과 주석을 유지하며 공용 포매터로 재작성하지 않는다. 공용 코드 글꼴·크기·행간·색은 05와 같다. 이미지 클릭 시 추출한 큰 그림을 열 수 있다. 실제 검토 결과는 [검토 기록](content-review.ko.md)에 남긴다.
