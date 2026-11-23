WEEK = 10
SUBTITLE = (
    'AI 모델 평가 · 지침과 스킬',
    'AI Model Evaluation · Instructions & Skills',
)


def table_block(head, rows):
    return dict(kind='table', head=head, rows=rows)


def link_table_block(head, rows):
    return dict(kind='link-table', head=head, rows=rows)


def concepts_block(*items):
    return dict(kind='concepts', items=[dict(term=t, details=list(d)) for t, d in items])


def code_block(label, text, width=58, language='text'):
    return dict(kind='code', label=label, language=language, width=width, text=text)


SLIDES = [
    dict(
        id='supplement',
        kind='chapter',
        title=('AI 모델 평가와 지침·스킬 설계', 'AI Model Evaluation, Instructions, and Skills'),
        lead=(
            '모델 성능 검증 방법 · 주요 벤치마크 · 지침과 스킬',
            'How to evaluate models, top benchmarks, instructions, and skills',
        ),
    ),
    dict(
        id='how-to-evaluate',
        kind='content',
        title=('AI 모델 성능 평가 방법', 'How to Evaluate AI Models'),
        lead=(
            'AI 모델의 품질·비용·신뢰성을 함께 판단하는 일반 기준',
            'General criteria for judging AI model capability, cost, and reliability',
        ),
        layout='single',
        columns=[[
            concepts_block(
                (
                    ('다차원 평가 - 사용 목적에 따른 품질 · 비용 · 속도의 균형',
                     'Multi-dimensional evaluation - quality, cost, and speed'),
                    [
                        ('종합 순위보다 과제 성격(대화 · 추론 · 코딩)별 역량 우선 확인',
                         'Check task fit (chat, reasoning, coding) over aggregate ranks'),
                        ('정확도와 함께 실제 토큰 단가 · 응답 지연 시간 비교 필수',
                         'Compare accuracy alongside token pricing and latency'),
                    ],
                ),
                (
                    ('점수의 신뢰성 - 기출 암기, 측정 조건, 발표 주체 확인',
                     'Score reliability - contamination, test setups, and bias'),
                    [
                        ('학습 기출이 포함되면 점수가 부풀려지므로 신규·비공개 평가 대조',
                         'Cross-check fresh or private evals to catch data leakage'),
                        ('추론 시간 · 도구 · 재시도 횟수 등 동일 조건 여부와 홍보용 점수 확인',
                         'Match reasoning effort and tools; watch for vendor bias'),
                    ],
                ),
            ),
            table_block(
                [('평가 관점', 'Dimension'), ('핵심 확인 사항', 'What to Verify')],
                [
                    [('과제 적합성', 'Task Fit'),
                     ('대화 품질 · 논리 추론 · 코드 수정 등 목적별 실제 해결력',
                      'Actual capability on chat, reasoning, and multi-file coding')],
                    [('오염 방지 신뢰성', 'Contamination Control'),
                     ('컷오프 이후 신규 출제 문제나 비공개 과제의 일반화 수준',
                      'Generalization on post-cutoff or private evaluation sets')],
                    [('비용과 응답 속도', 'Cost & Speed'),
                     ('초당 출력 토큰(tok/s) · 첫 응답 지연 · 백만 토큰당 단가',
                      'Throughput (tok/s), time-to-first-token, and price per 1M tokens')],
                    [('평가 조건 공정성', 'Fair Conditions'),
                     ('블라인드 비교 · 동일 추론 설정(effort) 및 도구 환경 적용 여부',
                      'Blind testing with matched effort and tool setups')],
                ],
            ),
        ]],
        sources=[
            'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents',
            'https://arxiv.org/abs/2211.09110',
            'https://arxiv.org/abs/2406.19314',
            'https://arxiv.org/abs/2403.04132',
            'https://arxiv.org/abs/2504.20879',
            'https://arxiv.org/abs/2411.12990',
            'https://artificialanalysis.ai/methodology',
            'https://platform.openai.com/docs/guides/reasoning',
        ],
    ),
    dict(
        id='benchmark-sites',
        kind='content',
        title=('주요 AI 벤치마크 사이트', 'Major AI Benchmark Platforms'),
        lead=(
            '전 세계 개발자·연구자가 모델 비교 시 가장 많이 참고하는 3대 기준 사이트',
            'Three independent benchmark platforms trusted by developers and labs',
        ),
        layout='single',
        columns=[[
            concepts_block((
                ('대중적 표준화 - 정적 시험(MMLU 등) 포화로 독립 실전 지표에 인용 집중',
                 'Shared industry standards - live independent benchmarks replace saturated static tests'),
                [
                    ('마케팅 수치 대신 대규모 블라인드 투표 · API 실측 · 오염 방지 신규 출제 기준으로 검증',
                     'Verify claims via large-scale blind votes, live API metrics, and fresh post-cutoff tasks'),
                ],
            )),
            link_table_block(
                [('플랫폼', 'Platform'),
                 ('공식 주소', 'Official URL'),
                 ('평가 대상', 'Focus'),
                 ('가장 많이 참고하는 근거', 'Why Developers Trust It')],
                [
                    [('LMArena', 'LMArena'),
                     dict(label=('arena.ai', 'arena.ai'), href='https://arena.ai/leaderboard'),
                     ('인간 선호도', 'Human preference'),
                     ('수백만 건의 블라인드 A/B 투표와 Elo로 체감 품질 검증',
                      'Millions of blind A/B votes and Elo ratings gauge utility')],
                    [('Artificial Analysis', 'Artificial Analysis'),
                     dict(label=('artificialanalysis.ai', 'artificialanalysis.ai'), href='https://artificialanalysis.ai/'),
                     ('지능 · 속도 · 비용', 'Quality, speed, cost'),
                     ('API 처리량(tok/s)과 비용 실측으로 서비스 도입 표준 인용',
                      'Live API throughput and pricing guide production choices')],
                    [('LiveBench 2.0', 'LiveBench 2.0'),
                     dict(label=('livebench.ai', 'livebench.ai'), href='https://livebench.ai/'),
                     ('오염 방지 추론', 'Contamination-free'),
                     ('학습 오염 차단을 위해 컷오프 이후 신규 문제 지속 출제',
                      'Regularly adds post-cutoff tasks to prevent contamination')],
                ],
            ),
        ]],
        sources=[
            'https://arena.ai/leaderboard',
            'https://artificialanalysis.ai/',
            'https://livebench.ai/',
        ],
    ),
    dict(
        id='model-eval-visual',
        kind='content',
        title=('주요 AI 모델별 평가 비교', 'Benchmark Comparison of Major AI Models'),
        lead=(
            '3대 벤치마크(Artificial Analysis · LiveBench 2.0 · LMArena Text) 각 사 최고 모델 비교',
            'Top model per provider across Artificial Analysis, LiveBench 2.0, and LMArena Text (Nov 2026)',
        ),
        layout='single',
        columns=[[dict(
            kind='model-eval-board',
            groups=[
                dict(
                    title=('종합 지능 · Artificial Analysis Index', 'Composite · Artificial Analysis Index'),
                    bars=[
                        dict(label=('Claude Fable 5.2', 'Claude Fable 5.2'), value=('65', '65'), pct=65, top=True, icon='assets/claude.svg'),
                        dict(label=('GPT-6.2 Astra', 'GPT-6.2 Astra'), value=('62', '62'), pct=62, icon='assets/openai.svg'),
                        dict(label=('Gemini 4 Neon', 'Gemini 4 Neon'), value=('61', '61'), pct=61, icon='assets/gemini.svg'),
                    ],
                ),
                dict(
                    title=('오염 방지 종합 · LiveBench 2.0', 'Contamination-Free · LiveBench 2.0'),
                    bars=[
                        dict(label=('Gemini 4 Neon', 'Gemini 4 Neon'), value=('87.4', '87.4'), pct=87.4, top=True, icon='assets/gemini.svg'),
                        dict(label=('Claude Fable 5.2', 'Claude Fable 5.2'), value=('84.9', '84.9'), pct=84.9, icon='assets/claude.svg'),
                        dict(label=('GPT-6.2 Astra', 'GPT-6.2 Astra'), value=('84.9', '84.9'), pct=84.9, icon='assets/openai.svg'),
                    ],
                ),
                dict(
                    title=('인간 선호도 · LMArena Text (arena.ai)', 'Human Preference · LMArena Text'),
                    bars=[
                        dict(label=('Gemini 4 Carbon', 'Gemini 4 Carbon'), value=('1,527', '1,527'), pct=85, top=True, icon='assets/gemini.svg'),
                        dict(label=('Claude Opus 5.5', 'Claude Opus 5.5'), value=('1,507', '1,507'), pct=71, icon='assets/claude.svg'),
                        dict(label=('GPT-5.6 Sol', 'GPT-5.6 Sol'), value=('1,485', '1,485'), pct=57, icon='assets/openai.svg'),
                    ],
                ),
            ],
            caption=(
                '출처 기준: Artificial Analysis · LiveBench 2.0 · LMArena Text (2026-11-23 공개 수치, Elo 막대는 1400 기준)',
                'Verified Nov 23, 2026: Artificial Analysis, LiveBench 2.0, LMArena Text (Elo scaled from 1400)',
            ),
            cards=[
                dict(
                    provider=('Anthropic', 'Anthropic'),
                    tier=('1M 문맥 · 다중 파일 강점', '1M Context · Multi-file'),
                    models=('Fable 5.2 ($8/$40) · Opus 5.5 ($4/$20) · Sonnet 5.5 ($2/$10)',
                            'Fable 5.2 ($8/$40) · Opus 5.5 ($4/$20) · Sonnet 5.5 ($2/$10)'),
                    strength=('적응형 사고 · 다중 파일 리팩토링 · Claude Code 기반 에이전트',
                              'Adaptive thinking, multi-file refactoring, and Claude Code'),
                    icon='assets/claude.svg',
                ),
                dict(
                    provider=('OpenAI', 'OpenAI'),
                    tier=('고난도 코딩 · OS 제어', 'Complex Coding · OS Control'),
                    models=('GPT-6.2 Astra ($8/$40) · GPT-6.2 Sol ($2/$10)',
                            'GPT-6.2 Astra ($8/$40) · GPT-6.2 Sol ($2/$10)'),
                    strength=('고난도 디버깅 · 터미널 · 브라우저/OS 제어 · Codex 통합',
                              'Complex debugging, CLI, browser/OS control, and Codex'),
                    icon='assets/openai.svg',
                ),
                dict(
                    provider=('Google', 'Google'),
                    tier=('1M 통합 문맥 · 멀티모달', '1M Context · Multimodal'),
                    models=('Gemini 4 Carbon ($4/$20) · Neon ($3/$15) · Argon',
                            'Gemini 4 Carbon ($4/$20) · Neon ($3/$15) · Argon'),
                    strength=('네이티브 멀티모달 · LiveBench/Text 1위 · 고속 에이전트 실행',
                              'Native multimodal, LiveBench/Text #1, and fast execution'),
                    icon='assets/gemini.svg',
                ),
            ],
        )]],
        sources=[
            'https://artificialanalysis.ai/leaderboards/models',
            'https://livebench.ai/',
            'https://arena.ai/leaderboard/chat/text',
            'https://openai.com',
            'https://www.anthropic.com',
            'https://deepmind.google',
        ],
    ),
    dict(
        id='model-selection',
        kind='content',
        title=('상황별 AI 모델 선택 가이드', 'Choosing Claude, ChatGPT, or Gemini'),
        lead=(
            '웹서비스 개발 중 Claude · ChatGPT · Gemini를 어떤 상황에 쓰면 좋은지 정리',
            'When to choose Claude, ChatGPT, or Gemini for web development',
        ),
        layout='single',
        columns=[[
            concepts_block(
                (
                    ('제공사별 강점 - 개발 작업 성격에 따른 역할 구분',
                     'Strengths by family - match models to tasks'),
                    [
                        ('Claude는 다중 파일 편집, ChatGPT는 터미널·디버깅에 적합',
                         'Claude for multi-file edits; ChatGPT for debugging & CLI'),
                        ('Gemini는 시안·화면 이해와 대용량 코드 탐색에 강점',
                         'Gemini excels at visual UI tasks and large repo context'),
                    ],
                ),
                (
                    ('단계별 모델 분리 - 난이도와 비용에 맞춘 모델 전환',
                     'Tier pairing - match model tier to task difficulty'),
                    [
                        ('구조 설계와 원인 불명 버그는 최상위 플래그십으로 해결',
                         'Use flagship models for architecture and tricky bugs'),
                        ('단순 기능·테스트·PR 정리는 실속형 모델로 빠르게 처리',
                         'Use fast, lower-cost models for CRUD, tests, and PRs'),
                    ],
                ),
            ),
            table_block(
                [('기준 모델', 'Model Family'),
                 ('주요 선택 모델', 'Recommended Models'),
                 ('추천 사용 상황 (웹서비스 개발)', 'Best Web Dev Use Cases')],
                [
                    [('Claude (Anthropic)', 'Claude (Anthropic)'),
                     ('Fable 5.2 · Opus/Sonnet 5.5', 'Fable 5.2, Opus/Sonnet 5.5'),
                     ('프론트·백엔드 다중 파일 리팩토링, 아키텍처 설계',
                      'Multi-file refactoring and architecture design')],
                    [('ChatGPT (OpenAI)', 'ChatGPT (OpenAI)'),
                     ('GPT-6.2 Astra · GPT-6.2 Sol', 'GPT-6.2 Astra, GPT-6.2 Sol'),
                     ('난해한 서버·로직 디버깅, 터미널·OS 자동화 제어',
                      'Complex server debugging, CLI, and OS automation')],
                    [('Gemini (Google)', 'Gemini (Google)'),
                     ('Gemini 4 Carbon · Neon', 'Gemini 4 Carbon, Neon'),
                     ('UI 시안·스크린샷 구현, 브라우저 QA, 1M 코드 탐색',
                      'Mockup-to-UI, browser QA, and 1M-token repo search')],
                    [('실속 · 고속 조합', 'Cost-Effective Tier'),
                     ('Sonnet 5.5 · Sol · Neon', 'Sonnet 5.5, Sol, Neon'),
                     ('일상 CRUD 구현, 테스트 코드 작성, 빠른 PR 리뷰',
                      'Routine CRUD, unit tests, and quick PR reviews')],
                ],
            ),
        ]],
        sources=[
            'https://www.anthropic.com',
            'https://openai.com',
            'https://deepmind.google',
        ],
    ),
    dict(
        id='instructions-structure',
        kind='content',
        title=('저장소 지침 작성 구조', 'Repository Instruction Structure'),
        lead=(
            'OpenAI · Claude · Gemini의 지침 파일 탐색 계층과 조건부 규칙',
            'Discovery hierarchy and conditional rules across OpenAI, Claude, and Gemini',
        ),
        layout='single',
        columns=[[
            concepts_block(
                (
                    ('계층 병합 - 전역에서 현재 디렉터리로 이어지는 규칙 적용',
                     'Hierarchical loading - from global down to folder rules'),
                    [
                        ('오픈 표준 AGENTS.md를 중심으로 도구별 전용 파일이 병행 동작',
                         'The open AGENTS.md format works alongside tool-specific files'),
                        ('작업 위치에 가까운 하위 파일이 상위 전역 규칙을 구체화 · 재정의',
                         'Subdirectory files refine or override broader global rules'),
                    ],
                ),
                (
                    ('조건부 규칙 - 파일 경로 · 호출 조건에 따른 선택적 로딩',
                     'Conditional rules - loading guidance only when relevant'),
                    [
                        ('Claude는 .claude/rules의 paths 글롭으로 접근 파일별 규칙 주입',
                         'Claude loads .claude/rules using paths globs on file access'),
                        ('Antigravity는 .agents/rules의 트리거 모드로 적용 시점 제어',
                         'Antigravity activates .agents/rules via trigger modes'),
                    ],
                ),
            ),
            table_block(
                [('플랫폼', 'Platform'),
                 ('지침 파일 · 조건부 규칙', 'Files & Rules')],
                [
                    [('OpenAI Codex', 'OpenAI Codex'),
                     ('~/.codex/AGENTS.md · AGENTS.override.md (32 KiB)',
                      '~/.codex/AGENTS.md, AGENTS.override.md (32 KiB)')],
                    [('Claude Code', 'Claude Code'),
                     ('CLAUDE.md · CLAUDE.local.md · .claude/rules (paths:) · MEMORY.md',
                      'CLAUDE.md, CLAUDE.local.md, .claude/rules (paths:), MEMORY.md')],
                    [('Gemini CLI', 'Gemini CLI'),
                     ('~/.gemini/GEMINI.md · 프로젝트 GEMINI.md · @file',
                      '~/.gemini/GEMINI.md, project GEMINI.md, @file')],
                    [('Antigravity', 'Antigravity'),
                     ('AGENTS.md · GEMINI.md · .agents/rules (24KB / 20K 토큰)',
                      'AGENTS.md, GEMINI.md, .agents/rules (24 KB / 20K tokens)')],
                ],
            ),
        ]],
        sources=[
            'https://agents.md/',
            'https://developers.openai.com/codex/guides/agents-md/',
            'https://code.claude.com/docs/en/memory',
            'https://geminicli.com/docs/cli/gemini-md/',
            'https://antigravity.google/docs/rules',
        ],
    ),
    dict(
        id='instructions-authoring',
        kind='content',
        title=('지침 작성 모범 사례', 'Best Practices for Writing Instructions'),
        lead=(
            '문맥 비대화를 막고 규칙 준수율과 안전성을 높이는 작성 기준',
            'Preventing context bloat while improving adherence and safety',
        ),
        layout='code',
        columns=[
            [concepts_block(
                (
                    ('간결한 지도 역할 - 모든 작업에 필수인 정보만 150~200줄 내 유지',
                     'Concise map - keep universal rules within 150–200 lines'),
                    [
                        ('빌드 · 테스트 명령과 코드에서 추론 불가한 제약만 선별 기재',
                         'Include build/test commands and constraints not inferable from code'),
                        ('세부 문서는 본문에 복사하지 않고 경로 포인터로 연결',
                         'Link to deeper docs by path instead of pasting full text'),
                    ],
                ),
                (
                    ('권고와 강제의 분리 - 보안 경계는 지침 대신 시스템 도구로 차단',
                     'Advice vs. enforcement - use hooks and permissions'),
                    [
                        ('Markdown 지침은 권고이므로 비밀파일 · 위험 명령 차단에 한계',
                         'Markdown rules are advisory and cannot enforce security boundaries'),
                        ('절대 금지는 PreToolUse 훅 · 권한 설정 · 샌드박스 규칙으로 강제',
                         'Block secrets and risky commands via hooks and permissions'),
                    ],
                ),
            )],
            [code_block(
                ('AGENTS.md / CLAUDE.md · 간결한 지침 예시',
                 'AGENTS.md / CLAUDE.md · concise instruction example'),
                (
                    '# Project Guidelines\n'
                    '- Package manager: pnpm (do not use npm)\n'
                    '- Verify changes: `pnpm test` before commit\n'
                    '- API schemas: follow `docs/api.md`\n\n'
                    '# Hard Boundaries\n'
                    '- Block `.env` reads via permissions/hooks',
                    '# Project Guidelines\n'
                    '- Package manager: pnpm (do not use npm)\n'
                    '- Verify changes: `pnpm test` before commit\n'
                    '- API schemas: follow `docs/api.md`\n\n'
                    '# Hard Boundaries\n'
                    '- Block `.env` reads via permissions/hooks',
                ),
                width=54,
            )],
        ],
        sources=[
            'https://code.claude.com',
            'https://developers.openai.com/api/docs/guides/prompt-engineering',
            'https://antigravity.google',
        ],
    ),
    dict(
        id='skills-structure',
        kind='content',
        title=('에이전트 스킬 작성 표준', 'Agent Skills Authoring Standard'),
        lead=(
            'agentskills.io 오픈 규격과 점진적 공개 3단계 구조',
            'The open agentskills.io specification and three-stage progressive disclosure',
        ),
        layout='code',
        columns=[
            [concepts_block(
                (
                    ('패키지 디렉터리 - SKILL.md와 선택적 실행 · 참고 자원의 묶음',
                     'Skill package - SKILL.md with scripts and references'),
                    [
                        ('공통 경로 .agents/skills/<name>/ 또는 도구별 .claude · .gemini/skills/',
                         'Stored in .agents/skills/<name>/ or .claude/.gemini/skills/'),
                        ('scripts/(코드) · references/(참고 문서) · assets/(템플릿) 분리',
                         'Separate scripts/ (code), references/ (docs), and assets/ (templates)'),
                    ],
                ),
                (
                    ('점진적 공개 - 필요 시점에만 본문과 자원을 불러 문맥 절약',
                     'Progressive disclosure - load details on demand'),
                    [
                        ('시작 시 name · description만 등록하고 일치 시 SKILL.md 본문 로딩',
                         'Register name and description at startup; load SKILL.md body on match'),
                        ('실행 시 필요한 scripts/ · references/ · assets/ 파일만 추가 로딩',
                         'Load scripts/, references/, or assets/ only when needed'),
                    ],
                ),
            )],
            [code_block(
                ('.agents/skills/pr-review/SKILL.md · 표준 형식',
                 '.agents/skills/pr-review/SKILL.md · standard format'),
                (
                    '---\n'
                    'name: pr-review\n'
                    'description: >\n'
                    '  Review PRs for test and security gaps.\n'
                    '  Use when asked to review diffs.\n'
                    '  Do not use for trivial typo fixes.\n'
                    'compatibility: Requires git and Node.js 22+\n'
                    '---\n\n'
                    '1. Inspect diff and run `scripts/check.sh`.\n'
                    '2. Check items in `references/checklist.md`.',
                    '---\n'
                    'name: pr-review\n'
                    'description: >\n'
                    '  Review PRs for test and security gaps.\n'
                    '  Use when asked to review diffs.\n'
                    '  Do not use for trivial typo fixes.\n'
                    'compatibility: Requires git and Node.js 22+\n'
                    '---\n\n'
                    '1. Inspect diff and run `scripts/check.sh`.\n'
                    '2. Check items in `references/checklist.md`.',
                ),
                width=54,
            )],
        ],
        sources=[
            'https://agentskills.io/',
            'https://developers.openai.com/codex/skills',
            'https://code.claude.com',
            'https://geminicli.com/docs/skills/',
        ],
    ),
    dict(
        id='skills-best-practices',
        kind='content',
        title=('좋은 스킬 설계 원칙', 'Principles for Designing Effective Skills'),
        lead=(
            '발견 정확도 · 문맥 효율 · 반복 검증을 높이는 작성법',
            'Authoring rules for discovery accuracy, lean context, and evaluation',
        ),
        layout='code',
        columns=[
            [concepts_block(
                (
                    ('트리거 description - 할 일과 제외 상황을 함께 명시',
                     'Trigger description - state scope and exclusions'),
                    [
                        ('실행할 작업과 "쓰지 말아야 할 상황"을 적어 오작동 방지',
                         'State matching tasks and when to skip to avoid misfires'),
                        ('"PROACTIVELY" 강제 문구나 도구 전용 변수 의존 지양',
                         'Avoid pushy "PROACTIVELY" or vendor-only variables'),
                    ],
                ),
                (
                    ('반복 검사 분리 - 정해진 계산·검증은 스크립트로 위임',
                     'Separate fixed checks - delegate exact steps to scripts'),
                    [
                        ('파싱·포맷·응답 검사는 scripts/로, 판단은 모델이 담당',
                         'Run parsing and checks in scripts/; leave reasoning to AI'),
                    ],
                ),
                (
                    ('평가 기반 보완 - 스킬 없이 먼저 실행 후 최소 규칙 추가',
                     'Eval-driven - test baseline first, add minimal rules'),
                    [
                        ('스킬 없이 실행해 실패한 부분만 보강하고 다시 검증',
                         'Test without the skill, fix real gaps, and retest'),
                    ],
                ),
            )],
            [code_block(
                ('SKILL.md 작성 사례 · 나쁜 예시 vs 표준 이식형 예시',
                 'SKILL.md example · vendor-locked vs. portable'),
                (
                    '# Bad: pushy prompt + vendor-specific variables\n'
                    'description: USE PROACTIVELY on every edit!\n'
                    'Run: python ${CLAUDE_SKILL_DIR}/check.py $ARGUMENTS\n\n'
                    '# Good: clear trigger + exclusion + relative path\n'
                    'description: >\n'
                    '  Validate REST routes and error codes on API edits.\n'
                    '  Do not use for CSS styling or docs changes.\n'
                    'Run: node scripts/verify-api.mjs',
                    '# Bad: pushy prompt + vendor-specific variables\n'
                    'description: USE PROACTIVELY on every edit!\n'
                    'Run: python ${CLAUDE_SKILL_DIR}/check.py $ARGUMENTS\n\n'
                    '# Good: clear trigger + exclusion + relative path\n'
                    'description: >\n'
                    '  Validate REST routes and error codes on API edits.\n'
                    '  Do not use for CSS styling or docs changes.\n'
                    'Run: node scripts/verify-api.mjs',
                ),
                width=56,
            )],
        ],
        sources=[
            'https://agentskills.io/',
            'https://code.claude.com',
            'https://antigravity.google',
        ],
    ),
    dict(
        id='foodmap-instructions',
        kind='content',
        title=('푸드맵 서버의 지침 (AGENTS.md)', 'FoodMap Server Instructions (AGENTS.md)'),
        lead=(
            'ajou-foodmap-server의 구조·검증 명령·인증/DB 제약을 고정하는 실제 적용 예시',
            'Concrete architecture, verification, and security rules in ajou-foodmap-server',
        ),
        layout='code',
        columns=[
            [concepts_block(
                (
                    ('공통 지도 - AGENTS.md 기준과 Claude·Gemini 연결',
                     'Shared map - link AGENTS.md to Claude & Gemini'),
                    [
                        ('Express 라우트·미들웨어·schema.sql 경계와 검증 명령 명시',
                         'List routes, middleware, schema.sql, and npm checks'),
                        ('CLAUDE.md(@AGENTS.md)·GEMINI.md로 중복 없이 참조',
                         'Import AGENTS.md from CLAUDE.md and GEMINI.md'),
                    ],
                ),
                (
                    ('보안 제약 - 인증/DB 불변 규칙과 시스템 차단 분리',
                     'Security - auth/SQL invariants and tool-level blocks'),
                    [
                        ('토큰 검증·미들웨어 순서·RLS 및 LAST_ADMIN 잠금 유지',
                         'Verify JWTs via getUser(), guard order, RLS, LAST_ADMIN'),
                        ('.env 비밀키는 settings.json·.geminiignore로 차단',
                         'Block .env secrets via settings.json and .geminiignore'),
                    ],
                ),
            )],
            [code_block(
                ('ajou-foodmap-server/AGENTS.md (+ 도구 차단 설정) 발췌',
                 'ajou-foodmap-server/AGENTS.md (+ tool blocks) excerpt'),
                (
                    '# Ajou FoodMap Server Guidelines (AGENTS.md)\n'
                    '## Map & Checks (npm only · Node 24)\n'
                    '- Code: src/routes/, src/middleware/, supabase/schema.sql\n'
                    '- Tests: tests/ (Jest API + PGlite SQL)\n'
                    '- Verify: npm run typecheck && npm test && npm run build\n\n'
                    '## Core Invariants\n'
                    '- Verify JWT via db.auth.getUser() + active profiles row\n'
                    '- Order: isAuthenticated -> requireAdmin (401 / 403)\n'
                    '- Keep SUPABASE_SECRET_KEY stateless & RLS (service_role)\n\n'
                    '# Tool Blocks (.claude/settings.json · .geminiignore)\n'
                    '- Deny Read/Edit/Write on .env* (allow .env.example)',
                    '# Ajou FoodMap Server Guidelines (AGENTS.md)\n'
                    '## Map & Checks (npm only · Node 24)\n'
                    '- Code: src/routes/, src/middleware/, supabase/schema.sql\n'
                    '- Tests: tests/ (Jest API + PGlite SQL)\n'
                    '- Verify: npm run typecheck && npm test && npm run build\n\n'
                    '## Core Invariants\n'
                    '- Verify JWT via db.auth.getUser() + active profiles row\n'
                    '- Order: isAuthenticated -> requireAdmin (401 / 403)\n'
                    '- Keep SUPABASE_SECRET_KEY stateless & RLS (service_role)\n\n'
                    '# Tool Blocks (.claude/settings.json · .geminiignore)\n'
                    '- Deny Read/Edit/Write on .env* (allow .env.example)',
                ),
                width=58,
            )],
        ],
        note='실제 ajou-foodmap-server 저장소에 작성된 AGENTS.md·CLAUDE.md·GEMINI.md·차단 설정을 수업 설명용으로 요약한 예시.',
        sources=[
            'https://agents.md/',
            'https://code.claude.com/docs/en/memory',
            'https://geminicli.com/docs/cli/gemini-md/',
        ],
    ),
    dict(
        id='foodmap-skills',
        kind='content',
        title=('푸드맵 서버의 스킬 (SKILL.md)', 'FoodMap Server Skills (SKILL.md)'),
        lead=(
            'ajou-foodmap-server의 라우트 권한 검증 절차를 패키징한 실제 스킬 예시',
            'Packaging ajou-foodmap-server route-guard checks into a portable skill',
        ),
        layout='code',
        columns=[
            [concepts_block(
                (
                    ('조건부 호출 - 라우트·인증 수정 시에만 절차 로딩',
                     'Scoped trigger - load steps only on route/auth edits'),
                    [
                        ('AGENTS.md를 가볍게 두고 권한 수정 시에만 스킬 본문 로딩',
                         'Keep AGENTS.md lean; load checks only on auth edits'),
                        ('문서·시드 데이터만 고칠 때는 제외해 엉뚱한 호출 방지',
                         'Skip docs or SQL seed edits to prevent misfires'),
                    ],
                ),
                (
                    ('검사 분리 - 역할 매트릭스 문서와 자동 검사 스크립트',
                     'Split checks - role matrix docs and static script'),
                    [
                        ('20개 API 401/403 표는 references/role-matrix.md에 분리',
                         'Keep the 20-endpoint 401/403 table in role-matrix.md'),
                        ('가드 순서·CORS 검사는 verify-route-guards.mjs로 실행',
                         'Check guards/CORS via scripts/verify-route-guards.mjs'),
                    ],
                ),
            )],
            [code_block(
                ('ajou-foodmap-server/.agents/skills/server-auth-route-check/SKILL.md',
                 'ajou-foodmap-server/.agents/skills/server-auth-route-check/SKILL.md'),
                (
                    '---\n'
                    'name: server-auth-route-check\n'
                    'description: >\n'
                    '  Verify Express guards (isAuthenticated, requireAdmin),\n'
                    '  401/403 matrix, CORS, and Jest API tests for FoodMap.\n'
                    '  Use when editing src/routes/, src/middleware/, app.ts.\n'
                    '  Do not use for docs-only or SQL seed data changes.\n'
                    'compatibility: Requires Node.js 24+ and npm\n'
                    '---\n\n'
                    '1. Compare routes against `references/role-matrix.md`.\n'
                    '2. Run `scripts/verify-route-guards.mjs` (7 guard checks).\n'
                    '3. Run `npm run typecheck`, `npm test`, `npm run build`.',
                    '---\n'
                    'name: server-auth-route-check\n'
                    'description: >\n'
                    '  Verify Express guards (isAuthenticated, requireAdmin),\n'
                    '  401/403 matrix, CORS, and Jest API tests for FoodMap.\n'
                    '  Use when editing src/routes/, src/middleware/, app.ts.\n'
                    '  Do not use for docs-only or SQL seed data changes.\n'
                    'compatibility: Requires Node.js 24+ and npm\n'
                    '---\n\n'
                    '1. Compare routes against `references/role-matrix.md`.\n'
                    '2. Run `scripts/verify-route-guards.mjs` (7 guard checks).\n'
                    '3. Run `npm run typecheck`, `npm test`, `npm run build`.',
                ),
                width=58,
            )],
        ],
        note='실제 ajou-foodmap-server/.agents/skills/server-auth-route-check/SKILL.md(.claude/skills/ 동일 미러) 및 SQL 스킬 구조를 요약한 예시.',
        sources=[
            'https://agentskills.io/',
            'https://developers.openai.com/codex/skills',
            'https://code.claude.com',
        ],
    ),
]
