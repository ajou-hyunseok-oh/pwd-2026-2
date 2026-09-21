# 03회차 자료

## 현재 강의와 실습

[3주차 HTML 강의](../index.html)는 [pwd-week3 기본 계산기](https://github.com/ajou-hyunseok-oh/pwd-week3)의 실제 코드를 사용합니다. 학생은 HTML·CSS와 TypeScript 세 파일을 직접 작성하고, 컴파일한 JavaScript를 브라우저에서 실행한 뒤 GitHub Pages로 배포합니다.

- [계산기 실습 안내](calculator-practice-guide.ko.md): 공개 저장소의 단계별 README와 완료 기준
- [강의와 실습 코드 연결](calculator-lecture-map.ko.md): 개념별 파일·함수와 읽기 순서
- [제목·서브타이틀 목록](week-03-slide-draft.ko.md): 50장 실제 번호와 주제 번호
- [출처와 검증 기록](content-review.ko.md): 소스 기준, 발췌, 검사 결과

계산기 실습은 챕터 번호 없이 마지막 한 장의 실습 개요로 안내합니다. 학습 목표·요구사항·참고 저장소와 마감일·제출물을 2주차 실습 개요 형식으로 배치합니다.

## 작성 원본

- `slide-draft.json`: 제목·서브타이틀. 2026-09-21 최종 검토에서 고차 함수 부제와 영문 용어를 보완했고 `approved-headings.sha256`에 현재 기준을 기록했습니다.
- `../scripts/lesson-body.py`: 한·영 본문, 예제, 출력과 검증 메타데이터.
- `practice-source/`: 공개 실습의 TypeScript 세 파일 스냅샷. [기준 커밋](https://github.com/ajou-hyunseok-oh/pwd-week3/tree/a321051435d95970ac6e082b933fd49464b7e974)과 동일합니다.
- `lesson-body.json`: 생성·포맷된 중간 데이터.
- `../scripts/build-slides.cjs`: 본문 생성 → 코드 포맷 → HTML·번역·제목 목록 생성.

실제 코드는 슬라이드 안에 검은 배경·녹색 Consolas 코드 블록으로 표시합니다. 코드 제목과 설명은 개념 중심으로 작성하고, 출처를 강조하는 문구와 링크는 화면에 표시하지 않습니다. 독립된 줄 주석은 생략하고 실행 구문은 유지합니다. 근거 확인용 파일·줄 메타데이터와 출처는 작성 원본과 검토 문서에 보관합니다. 강의를 다시 빌드할 때 형제 폴더의 실습 저장소가 필요하지 않습니다. 소스가 변경되면 스냅샷과 발췌 범위, 기준 커밋, 검증 시나리오를 함께 검토합니다.

## 생성과 검증

Node.js, npm, Python 3가 필요합니다. 생성기는 기본적으로 `python3`를 사용하며 `PYTHON` 환경변수로 실행 파일을 바꿀 수 있습니다.

```sh
npm ci --prefix packages/web-deck
node lectures/03/scripts/build-slides.cjs
node lectures/03/scripts/check-practice.cjs
npm test --prefix packages/web-deck
```

강의 검증 도구는 `packages/web-deck`의 TypeScript 5.9.3을 사용합니다. 학생이 실행할 프로젝트는 외부 `pwd-week3`입니다. 학생 명령은 `npm run check`, `npm run build`, `npm run watch`입니다.

실제 실습 저장소와 스냅샷까지 비교하려면:

```sh
WEEK3_PRACTICE_ROOT=/path/to/pwd-week3 node lectures/03/scripts/check-practice.cjs
```

독립 예제의 일반 스크립트·모듈 문법과 선언형 화면 비교의 React TSX를 검증합니다. 임시 검증 폴더에 React와 타입 선언이 필요하며 Vue는 사용하지 않습니다.

```sh
npm install --prefix /tmp/pwd-week3-code-review react@19.1.1 @types/react@19.1.13 --ignore-scripts --no-audit --no-fund
WEEK3_CHECK_ROOT=/tmp/pwd-week3-code-review node lectures/03/scripts/check-examples.cjs
```

## 브라우저 검증

저장소 루트에서 `python3 -m http.server 4304 --bind 127.0.0.1`을 실행합니다. 별도 터미널에서 Chrome과 설치된 Playwright를 사용합니다.

```sh
PLAYWRIGHT_PATH=/path/to/playwright node lectures/03/scripts/check-slides.cjs
```

`DECK_URL`로 서버 주소를 바꿀 수 있습니다. 한·영 50장씩 화면·인쇄 총 200개 상태, 모바일 100개 이동, 코드 테마와 미처리 예외를 검사합니다. 캡처와 `audit.json`은 OS 임시 폴더의 `week3-slide-review`에 저장합니다.

## 실습 기준

학생 실습과 실행·제출 기준은 공개 `pwd-week3` README를 따릅니다. 폐기된 실습 프로젝트는 강의 예제나 검증 도구의 의존성으로 사용하지 않습니다.
