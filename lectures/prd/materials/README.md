# PRD 작성 개요

PRD의 약자와 뜻, 작성할 내용 7항목, 공식 작성 레퍼런스 3개를 한 장에 정리한 보충 학습자료. 표는 수업용 요약이며 자세한 작성 방법은 링크한 공식 원문에서 확인한다.

- [한·영 슬라이드 · 1장](../index.html)
- [배포용 한국어 PDF · 1장](prd-slides.ko.pdf)
- [공식 레퍼런스 안내 · 한국어](references.ko.txt) / [영어](references.en.txt)
- [작성 원본](../scripts/lesson.py)
- [슬라이드와 출처 대응](slide-map.json)
- [공식 자료 확인 기록](references.json)
- [본문·레이아웃 검토 기록](content-review.ko.txt)

이전 구성의 PRD 양식·푸드맵 작성 예시·사례 근거 파일은 보조 자료로 보관하며 현재 한 장 슬라이드에는 사용하지 않는다.

## 재생성

```sh
python3 lectures/prd/scripts/build-slides.py
npm test --prefix packages/web-deck
DECK_PATH=lectures/prd DECK_URL=http://127.0.0.1:48729 PLAYWRIGHT_PATH=/path/to/playwright node packages/web-deck/tests/authoring-layout.cjs
```

공용 작성 하네스와 스타일을 재사용한다. 레이아웃 검사는 저장소 루트 HTTP 서버가 필요하며 `REVIEW_OUTPUT`으로 검토 산출물 경로를 지정한다.
