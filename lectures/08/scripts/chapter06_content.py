"""Beginner-facing configuration, build, deployment and verification flow."""
from chapter03_content import P, G, B, concept, Q, M
from chapter04_content import flow
from chapter05_content import branches

RETIRED = ('secret-management','environment-data','db-migration','backup','rollback','restore')
CHAPTER = dict(number=6, source_number=7,
    connection='로그인·권한 검사·제보 승인을 로컬에서 실행한 뒤 배포 주소에서 같은 기능 확인.',
    scope='실행 환경 → 환경변수 → 빌드·배포 → 주소와 로그인 복귀 → 기능 확인. 별도 검증 환경·마이그레이션·백업·복원·지표 분석은 보충 자료.',
    concepts=[
        concept('environments', P('로컬 환경과 배포 환경','Local and Deployed Environments'), P('내 컴퓨터 실행과 외부 주소 제공의 구분','Running on your computer and serving a public address'), 'admin-system prior-deploy', '로컬 브라우저·Express와 배포 Vercel·Render·Supabase의 역할'),
        concept('environment-config', P('환경변수와 연결 설정','Environment Variables and Connection Settings'), P('실행 위치에 맞춘 API·Supabase 연결값','API and Supabase settings for each execution environment'), 'environments api-keys', '클라이언트 .env.local·서버 .env → 배포 서비스의 환경변수'),
        concept('deployment', P('빌드와 배포의 실행 흐름','The Build and Deployment Flow'), P('화면 파일 생성과 API 서버 실행의 구분','Building frontend assets and running the API server'), 'environment-config prior-web', 'React → Vite build → dist → Vercel / TypeScript → build → dist/server.js → Render npm start'),
        concept('deployment-urls', P('배포 주소와 로그인 복귀 설정','Deployment URLs and Login Redirects'), P('API 연결 주소와 인증 후 돌아올 주소의 구분','Distinguish the API base URL from the authentication redirect URL'), 'deployment authorization-code', 'VITE_API_BASE_URL·CLIENT_URL·Site URL·Redirect URLs와 /auth/callback 연결'),
        concept('monitoring', P('배포 후 동작 확인','Verifying the Deployed Service'), P('서버 응답부터 로그인·제보·승인까지 확인','Verify server responses, login, submissions and approval'), 'deployment-urls idempotency', '/health → 맛집 조회 → 로그인 → 제보 → 승인 / Network·서버 로그로 오류 위치 확인'),
    ])

BODY = {
    'environments': B('wide',
        G(P('실행 환경 - 프로그램이 동작하는 장소와 설정','Runtime environment - where a program runs and the configuration it uses'),
          P('화면·API 서버의 실행 위치와 연결할 Supabase 프로젝트 확인','Identify where the UI and API run and which Supabase project they use')),
        G(P('로컬·배포 환경 - 내 컴퓨터 실행과 외부 접속의 구분','Local and deployed environments - development on your computer and hosted access'),
          P('로컬은 개발 서버 실행 · 배포는 외부 서비스의 주소로 제공','Run development servers locally; serve deployed software from hosted URLs'))),
    'environment-config': B('wide',
        G(P('환경변수 - 코드 밖에서 전달하는 이름과 설정값','Environment variable - a named setting supplied outside the code'),
          P('API 주소·Supabase 프로젝트 연결값을 실행 위치별로 지정','Set API addresses and Supabase connections for each environment')),
        G(P('.env 파일 - 로컬 환경변수를 저장하는 파일','.env file - a file containing local environment variables'),
          P('클라이언트는 .env.local · 서버는 .env · 배포 서비스에는 별도 등록','Use .env.local for the client and .env for the server; configure deployment environment variables separately'))),
    'deployment': B('wide',
        G(P('빌드(build) - 소스를 실행·제공할 파일로 변환','Build - compile and bundle source code into deployable files'),
          P('npm run build로 생성 · dist는 빌드 결과를 저장하는 폴더','Run npm run build; dist is the build output directory')),
        G(P('배포(deployment) - 코드·설정을 외부 실행 환경에 반영','Deployment - release code and settings to a hosted environment'),
          P('Vercel은 화면 파일 제공 · Render는 Express 서버 프로세스 실행','Vercel serves UI files; Render runs the Express server process'))),
    'deployment-urls': B('wide',
        G(P('API 기본 주소 - 업무 요청을 보낼 서버의 주소','API base URL - the server address for service requests'),
          P('VITE_API_BASE_URL은 Render 주소 · /api는 요청 코드에서 추가','VITE_API_BASE_URL points to Render; request code adds /api')),
        G(P('로그인 복귀 주소 - 인증 후 브라우저가 돌아올 화면 주소','Redirect URL - where the browser returns after authentication'),
          P('Vercel 주소의 /auth/callback · Supabase의 Redirect URLs에 등록','Use the Vercel URL with /auth/callback and register it in Supabase Redirect URLs'))),
    'monitoring': B('wide',
        G(P('상태 확인 요청(health check) - 서버의 응답 가능 여부 확인','Health check - check whether the server responds'),
          P('실습의 /health는 DB를 조회하지 않음 · 업무 기능은 별도 확인','This project’s /health does not query the DB; verify service features separately')),
        G(P('Network·로그 - 요청 확인 탭과 서버 실행 기록','Network panel and logs - HTTP requests and server activity'),
          P('Network는 브라우저 개발자 도구의 요청 확인 탭 · 로그는 서버가 실행 중 남긴 기록','The browser’s Network panel shows HTTP requests; server logs record runtime events'))),
}

MEDIA = {
    'environments': [[branches(P('FoodMap의 실행 구성','FoodMap service components'), P('Vercel: 화면 제공 · Render: Express 서버 실행\nSupabase: 사용자 인증·DB','Vercel: serve the UI · Render: run Express\nSupabase: user authentication and DB'), [
        (P('로컬 환경','Local environment'),P('내 브라우저 → 개발 화면 :5173\nExpress 서버 :3000 → Supabase','Browser → local dev server :5173\nExpress server :3000 → Supabase')),
        (P('배포 환경','Deployed environment'),P('브라우저 → Vercel 화면\nRender의 Express → Supabase','Browser → Vercel UI\nExpress on Render → Supabase')),
    ], P('같은 Supabase 프로젝트를 설정하면 데이터 공유 · 주소 변경만으로 DB가 분리되지는 않음','Using the same Supabase project shares data; changing service URLs does not separate the DB'))]],
    'environment-config': [[dict(kind='resource-workspaces', caption=P('같은 Supabase 프로젝트 지정 · 키는 브라우저용과 서버용 구분','Use the same Supabase project; use separate browser and server keys'), panes=[
        dict(title=P('클라이언트 · Vite','Client · Vite'), role=P('.env.local → Vercel 환경변수','.env.local → Vercel environment variables'), rows=[
            P('VITE_API_BASE_URL → Express 서버 주소','VITE_API_BASE_URL → Express server URL'),
            P('VITE_SUPABASE_URL → Supabase 주소','VITE_SUPABASE_URL → Supabase URL'),
            P('VITE_SUPABASE_PUBLISHABLE_KEY → 브라우저용 키','VITE_SUPABASE_PUBLISHABLE_KEY → Browser key')]),
        dict(title=P('서버 · Express','Server · Express'), role=P('.env → Render 환경변수','.env → Render environment variables'), rows=[
            P('SUPABASE_URL → 같은 Supabase 프로젝트','SUPABASE_URL → The same Supabase project'),
            P('SUPABASE_SECRET_KEY → 서버 전용 키','SUPABASE_SECRET_KEY → Server-only key'),
            P('CLIENT_URL → 접속할 화면의 기본 주소','CLIENT_URL → Client origin')]),
    ])]],
    'deployment': [[flow([
        (P('클라이언트 빌드','Build the client'),P('React 소스\nnpm run build','React source\nnpm run build')),
        (P('dist 생성','Build output: dist'),P('HTML·JavaScript·CSS 파일','HTML, JavaScript and CSS files')),
        (P('Vercel에서 제공','Serve on Vercel'),P('브라우저가 화면 파일 요청','The browser requests UI files')),
    ],P('클라이언트 설정 변경 → 로컬 개발 서버 재시작 / 배포는 새 빌드로 반영','Client configuration changes → restart the dev server locally or rebuild the deployment')),
    flow([
        (P('서버 빌드','Build the server'),P('TypeScript 소스\nnpm run build','TypeScript source\nnpm run build')),
        (P('실행 파일 생성','Compile to JavaScript'),P('dist/server.js 등 JavaScript','JavaScript including dist/server.js')),
        (P('Render에서 실행','Run on Render'),P('npm start\nAPI 요청 대기','npm start\nListen for API requests')),
    ],P('서버 설정 변경 → 프로세스 재시작으로 반영 · DB 준비 SQL 실행은 빌드와 별도','Server setting changes → restart the process · Database setup SQL runs separately from the build'))]],
    'deployment-urls': [[Q([P('Vercel 화면','Vercel UI'),P('Render 서버','Render server'),P('Supabase Auth','Supabase Auth')],[
        M(0,1,'VITE_API_BASE_URL → Render 주소','VITE_API_BASE_URL → Render URL'),
        M(1,1,'CLIENT_URL에 Vercel 기본 주소 등록','Set CLIENT_URL to the Vercel origin',focus=True),
        M(0,2,'인증 요청 · 복귀 주소 지정','Request login with a return URL'),
        M(2,0,'등록한 Vercel 주소의 /auth/callback으로 복귀','Return to /auth/callback on the registered Vercel URL',reply=True),
    ],P('Supabase Site URL: Vercel 기본 주소 · Redirect URLs: 그 주소의 /auth/callback','Supabase Site URL: Vercel app URL · Redirect URLs: the app URL with /auth/callback'))]],
    'monitoring': [[flow([
        (P('서버 응답','Server response'),P('GET /health\n200 · status: ok','GET /health\n200 · status: ok')),
        (P('맛집 조회','Restaurant list'),P('GET /api/restaurants\nDB 데이터 표시','GET /api/restaurants\nDisplay DB data')),
        (P('로그인','Login'),P('이메일·Google·네이버\n내 프로필 확인','Email, Google, Naver\nConfirm own profile')),
        (P('제보·승인','Submission and approval'),P('일반 사용자 제보\n관리자 승인 → 맛집 확인','User submits restaurant details\nAdmin approves → verify the restaurant')),
    ],P('새로고침·로그아웃·재로그인도 확인 · 실패 시 Network와 서버 로그에서 중단 위치 확인','Also test refresh, logout and login again · Locate failures with Network and server logs'))]],
}

PARAGRAPHS = {
    'environments':'첫 도식에 Vercel=화면 제공, Render=Express 서버 실행, Supabase=사용자 인증·DB를 바로 표시한다. 실행 환경은 프로그램이 동작하는 장소와 설정이다. 로컬 환경에서는 학생의 컴퓨터에서 Vite 개발 화면과 Express 서버를 실행한다. 배포 환경에서는 Vercel이 화면 파일을 제공하고 Render가 Express를 실행한다. 브라우저 SDK는 Supabase Auth로 인증을 요청하고 업무 요청은 Express를 거쳐 Supabase DB로 처리한다. 로컬과 배포 환경에 같은 Supabase 프로젝트를 설정하면 인증 계정과 업무 데이터를 공유할 수 있다. 별도 검증 환경이나 환경별 DB가 자동 구성된다고 설명하지 않는다. 도식의 화살표는 업무 요청 경로의 요약이며 Auth 직접 통신은 챕터3에서 배운 경로다.',
    'environment-config':'환경변수는 코드 밖에서 전달하는 이름과 설정값이며 .env 파일은 로컬 값을 저장하는 파일이다. 클라이언트는 .env.local의 VITE_API_BASE_URL·VITE_SUPABASE_URL·VITE_SUPABASE_PUBLISHABLE_KEY를 Vite에서 읽는다. 서버는 dotenv/config로 .env를 읽고 SUPABASE_URL·SUPABASE_SECRET_KEY·CLIENT_URL을 사용한다. 배포 서비스의 환경변수는 로컬 파일과 별도로 등록한다. 클라이언트와 서버의 Supabase URL은 같은 프로젝트를 가리키고 키는 각 실행 주체에 맞는 종류를 사용한다. Secret key를 VITE_ 변수에 넣지 않는다. 키 유출 대응 심화는 다음 주 보안 강의 범위다.',
    'deployment':'빌드는 소스를 실행·제공할 파일로 변환하는 과정이고 dist는 빌드 결과 폴더다. npm run build는 각 프로젝트의 package.json에 정의한 명령으로 클라이언트는 Vite 정적 파일을 만들고 서버는 TypeScript를 JavaScript로 변환한다. 현재 서버 빌드에는 copy-data.ts 실행도 포함되며 본문은 주 흐름을 발췌한다. Vercel은 dist의 화면 파일을 제공하고 Render는 npm start로 node dist/server.js를 실행해 API 요청을 받는다. 개발에서는 npm run dev를 사용한다. 클라이언트 설정 변경은 개발 서버 재시작 또는 배포 재빌드, 서버 실행값 변경은 프로세스 재시작으로 반영한다. Supabase SQL은 DB에서 별도 실행하므로 Git 업로드나 빌드만으로 테이블·함수가 바뀌지 않는다.',
    'deployment-urls':'API 기본 주소는 업무 요청을 보낼 Express 주소이며 VITE_API_BASE_URL에는 본인의 Render HTTPS 기본 주소를 넣는다. api.jsx가 /api/... 경로를 붙이므로 기본 주소에 /api를 중복 추가하지 않는다. CLIENT_URL은 화면의 프로토콜·호스트·포트로 이뤄진 기본 주소이며 경로나 끝 슬래시 없이 Vercel 주소를 등록한다. Supabase Site URL은 배포 화면 기본 주소이고 Redirect URLs에는 해당 주소의 /auth/callback을 등록한다. authApi.js는 window.location.origin에 /auth/callback을 붙여 redirectTo로 보낸다. vercel.json의 rewrite는 직접 접근도 index.html로 연결한다. 외부 제공자에서 Supabase로 돌아오는 콜백과 Supabase에서 Vercel로 돌아오는 주소는 다르다. 이 장은 배포 설정 적용이며 OAuth 전체 흐름과 CORS 원리는 반복하지 않는다.',
    'monitoring':'Network는 브라우저 개발자 도구의 요청 확인 탭으로 풀어 설명하며 로그는 서버 실행 기록과 구분한다. 상태 확인 요청 health check는 서버 응답 여부를 확인하는 요청이다. 현재 app.ts의 /health는 {status:ok}를 반환하고 Supabase를 조회하지 않으므로 이 성공만으로 DB·Auth·승인 정상 여부를 판단할 수 없다. 공개 맛집 조회로 업무 DB 요청을 확인하고 이메일·Google·네이버 로그인과 내 프로필 확인, 일반 사용자의 제보 및 관리자의 승인 후 맛집 반영을 점검한다. 새로고침·로그아웃·재로그인도 확인한다. 브라우저 Network는 요청 주소·HTTP 상태와 응답을, Render 로그는 서버 실행과 오류 기록을 확인하는 도구다. 별도 함수에 기록하지 않은 모든 요청이 서버 로그에 자동 남는다고 설명하지 않는다. p95와 실패율 차트·상관관계 분석은 보충 자료다. 실제 배포 실행 결과가 아닌 구현 코드와 실습서의 점검 경로를 도식화했다.',
}
SOURCES = [
    ('Vite Environment Variables','https://vite.dev/guide/env-and-mode'),
    ('Vite Production Build','https://vite.dev/guide/build'),
    ('Supabase Redirect URLs','https://supabase.com/docs/guides/auth/redirect-urls'),
    ('Render Express Deployment','https://render.com/docs/deploy-node-express-app'),
    ('Vercel Vite','https://vercel.com/docs/frameworks/frontend/vite'),
]
REVIEW = dict(assessment='본문 10장을 로컬·배포 환경 → 환경변수 → 빌드·배포 → 주소 설정 → 동작 확인의 5장으로 통합.',boundary='로컬과 배포가 같은 Supabase를 공유할 수 있는 실제 실습 구조. 별도 검증 환경·마이그레이션·백업·복원·지표 분석은 보충 자료. 보안 심화는 다음 주.',caution='서버·클라이언트 소스와 실습서를 읽어 대조한 설명. 실환경 배포·로그인·DB 변경 실행 결과가 아님.')
