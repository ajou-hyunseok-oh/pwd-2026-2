# 02회차 실행 예제 / Week 2 Examples

ZIP을 풀었다면 `examples` 폴더에서, 저장소를 받았다면 `lectures/02/examples`에서 실행합니다. Node.js와 npm이 필요합니다.

```powershell
node --version
npm --version
npm ci
npm run build
npm run dev
```

[예제 목록](http://localhost:4183)에서 실행 화면과 전체 소스를 엽니다. 초기 상태로 돌아가려면 새로고침하고, 서버를 종료하려면 터미널에서 Ctrl+C를 누릅니다. 포트가 사용 중이면 PowerShell에서 `$env:PORT='4184'`를 설정한 뒤 `npm run dev`를 실행하고 해당 주소를 사용합니다.

| 폴더 | 확인할 내용 |
| --- | --- |
| `portfolio/` | Home·About·Projects 링크, 소개 문구 변경, 새 문단 추가 |
| `rendering/` | 너비·배경색·display 변경, CSS 상속과 직접 지정, 이미지 공간 예약 |
| `generation/` | CSR의 초기 응답과 DOM, SSR의 요청 시 HTML 생성, SSG의 빌드 결과 |
| `routing/` | 쿼리 값에 따른 DOM 갱신, 뒤로/앞으로 이동, 직접 URL 접근 |
| `components/` | React의 ProjectCard 정의, 두 입력 title, Vite 프로젝트 파일 |

각 폴더의 `en/`은 같은 예제의 영어 버전입니다. React 카드 예제는 두 언어가 같은 코드를 사용합니다.

SSR은 `server.mjs`가 실행되는 로컬 주소에서 확인합니다. 정적 웹 호스팅의 `generation/ssr.html`은 실행 방법을 안내합니다. CSR·SSG·페이지 이동 예제와 미리 빌드한 React 화면은 정적 호스팅에서도 열립니다.

React 소스를 수정하며 실행하려면 별도 터미널에서 다음을 실행합니다. 예제는 React 19.3.0, Vite 8.3.0과 잠금 파일을 사용하며 Node.js 24.12.0에서 검증했습니다.

```powershell
cd components
npm ci
npm run dev
```

[React 개발 화면](http://localhost:4175)을 엽니다. `npm run build`는 `components/dist/`에 배포 파일을 생성합니다. `node_modules`는 설치 결과이므로 Git이나 제출물에 포함하지 않습니다.

## English

Open a terminal in the extracted `examples` folder (or `lectures/02/examples` in the repository). Run the commands at the top, then open [the catalog](http://localhost:4183). Reload a page to reset it. Press Ctrl+C to stop the server. Every catalog entry includes the running example and its source files.

The `/en/` directories contain English equivalents. SSR requires the local Node server; static hosting displays setup instructions for that route. CSR, SSG, navigation examples and the built React preview also work on static hosting. For React development, run the commands in the `components` folder and open port 4175. Dependencies are pinned in the lockfiles; do not submit `node_modules`.
