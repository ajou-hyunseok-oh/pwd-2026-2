"""Bilingual resources for the 60 researched Week 9 slides.

References and adaptation history are exported separately by slide_references.py.
Illustrative examples are labelled; measured output comes from the checked code.
"""
from reused_resources import pair as P, table as T, note as N, flow, diagram, box, edge, label


def R(*blocks, right=None):
    return dict(layout='single' if right is None else 'split',
                columns=[list(blocks)] if right is None else [list(blocks), right])


def F(items, ko, en, repeat=None):
    return flow([(P(a,b),P(c,d)) for a,b,c,d in items], P(ko,en), repeat)


def C(label_ko, label_en, ko, en=None, language='javascript', width=64):
    return dict(kind='code', label=P(label_ko,label_en), text=P(ko,en), language=language, width=width)


def G(items, ko, en):
    return dict(kind='resource-groups', items=[dict(title=P(a,b), body=P(c,d)) for a,b,c,d in items], caption=P(ko,en))


def S(value, result, caption, *, state='normal'):
    return dict(kind='resource-screen',value=value,result=result,caption=caption,state=state)


def IMG(src, ko, en, caption_ko, caption_en):
    return dict(kind='figure',src=src,alt=P(ko,en),caption=P(caption_ko,caption_en))


TITLE = """function isValidTitle(input) {
  const title = input.trim();
  return title.length >= 1 && title.length <= 20;
}"""
BEFORE = """function isValidTitle(input) {
  return input.length >= 1 && input.length <= 20;
}"""

RESOURCES = {
    'artificial-intelligence': R(
        T([P('과제','Task'),P('입력','Input'),P('필요한 처리','Required processing')],[
            [P('정해진 수 비교','Compare fixed numbers'),P('10 > 5'),P('주어진 연산 규칙 적용','Apply a specified operation')],
            [P('문의 의도 파악','Interpret an inquiry'),P('“배송은 언제 오나요?”\n“택배 도착일을 알려주세요”','“When will it arrive?”\n“Tell me the delivery date.”'),P('서로 다른 표현에서 같은 의도 파악','Recognize the same intent across expressions')],
        ]),
        N('인식·언어 이해·문제 해결처럼 표현과 상황이 달라지는 과제를 다루는 연구',
          'Research on perception, language understanding, and problem solving across changing situations')),
    'dartmouth': R(
        IMG('assets/new/dartmouth-proposal-heading.png','1955년 연구 제안서의 제목·작성자·날짜','Title, authors, and date of the 1955 research proposal',
            '공동 연구의 목표를 제시한 제안서','A proposal defining a shared research agenda'),
        right=[F([
            ('1955년','1955','연구 목표 제안','Propose research goals'),
            ('1956년 여름','Summer 1956','다트머스 연구 모임','Meet at Dartmouth'),
        ],'완성 기술의 발표가 아닌 연구 분야의 출발','The start of a research field, rather than a finished technology')]),
    'symbolic-ai': R(F([
        ('사실','Fact','A는 선분 3개로 둘러싸인 평면 도형','A is enclosed by three straight sides'),
        ('규칙','Rule','변 3개인 다각형 → 삼각형','A polygon with three sides → triangle'),
        ('결론','Conclusion','A는 삼각형','A is a triangle'),
    ],'기호로 표현한 사실과 명시적 규칙을 연결하는 분류 예시','A classification example linking symbolic facts with an explicit rule')),
    'machine-learning': R(T([P('기준을 얻는 방식','How criteria are obtained'),P('준비하는 것','What is provided'),P('판단에 사용하는 것','What makes the decision')],[
        [P('사람이 규칙 작성','People write rules'),P('메시지를 분류할 조건','Conditions for classifying messages'),P('조건을 실행하는 프로그램','A program executing the conditions')],
        [P('데이터로 학습','Learn from data'),P('메시지와 분류 사례','Example messages and classifications'),P('사례에서 기준을 학습한 모델','A model that learns criteria from examples')],
    ]),N('데이터에서 반복되는 관계를 이용해 새로운 입력의 결과를 예측','Use relationships in data to predict results for new inputs')),
    'training': R(F([
        ('예측','Predict','메시지 → 분류 결과','Message → predicted class'),
        ('비교','Compare','예측과 실제 분류의 차이','Difference from the known class'),
        ('조정','Adjust','차이를 줄이도록 내부 값 변경','Change internal values to reduce error'),
    ],'학습 데이터의 반복 처리 · 처음 보는 데이터에서의 성능은 별도 확인','Repeated use of training data · performance on unseen data requires a separate check',P('다음 사례로 반복','Repeat with another example'))),
    'inference': R(F([
        ('새 메시지','New message','아직 분류하지 않은 입력','An input not yet classified'),
        ('학습된 모델','Trained model','학습한 내부 값을 사용','Use learned internal values'),
        ('예측 결과','Prediction','광고 또는 일반 메시지','Advertisement or regular message'),
    ],'한 번의 추론 요청은 학습한 값의 갱신과 구분','An inference request is distinct from updating learned values'),
        N('학습: 판단 기준 조정 · 추론: 학습한 기준으로 새 입력 처리','Training: adjust criteria · inference: apply learned criteria to a new input')),
    'supervised-learning': R(T([P('학습 메시지','Training message'),P('제공된 정답','Provided label')],[
        [P('“무료 쿠폰을 받으세요”','“Get a free coupon”'),P('광고','Advertisement')],
        [P('오늘만 특별 할인','Special discount today'),P('광고','Advertisement')],
        [P('“내일 회의는 2시입니다”','“Tomorrow’s meeting is at 2”'),P('일반','Regular')],
        [P('“과제 제출을 확인했습니다”','“Your assignment was received”'),P('일반','Regular')],
    ]),N('입력과 정답의 관계를 학습한 뒤 새 메시지에 적용 · 설명용 데이터','Learn the relationship between inputs and labels, then apply it to new messages · illustrative data')),
    'unsupervised-learning': R(G([
        ('그룹 A','Group A','“배송은 언제 오나요?”\n“택배 위치를 알려주세요”','“When will it arrive?”\n“Where is my package?”'),
        ('그룹 B','Group B','결제가 되지 않아요\n카드를 바꾸고 싶어요','Payment did not go through\nI want to change my card'),
        ('그룹 C','Group C','비밀번호를 잊었어요\n계정 이름을 바꾸고 싶어요','I forgot my password\nI want to rename my account'),
    ],'정답 없이 유사한 문의를 묶은 설명용 결과','Illustrative grouping of similar inquiries without supplied labels'),
        N('그룹을 만든 뒤 사람이 해석한 의미: 배송 · 결제 · 계정','Meanings assigned by a person after grouping: delivery · payment · account')),
    'reinforcement-learning': R(F([
        ('에이전트','Agent','격자에서 이동 방향 선택','Choose a direction on a grid'),
        ('환경','Environment','행동에 따라 위치 변화','Update the position after the action'),
        ('상태·보상','State and reward','새 위치와 행동 결과 전달','Return the new position and reward'),
    ],'설명용 보상 규칙: 도착 +1 · 그 외 0 · 여러 행동에 걸친 누적 보상 추구','Illustrative rewards: +1 at the goal, 0 otherwise · seek cumulative reward across actions',
    P('결과를 이용해 이후 행동 선택을 개선','Use outcomes to improve later action choices'))),
    'backpropagation': R(diagram((1020,320),P('출력에서 입력 방향으로 오차의 영향을 계산','Compute error sensitivity backward through the network'),[
        box((10,70,170,80),P('입력','Input')),
        box((240,70,200,80),P('은닉층','Hidden layer')),
        box((500,70,200,80),P('출력','Output')),
        box((760,70,245,80),P('목표와 비교','Compare to target')),
    ],[edge('M180 110 H235'),edge('M440 110 H495'),edge('M700 110 H755'),
       edge('M880 150 V220 H605 V155'),edge('M600 220 H340 V155')],[
        P('입력 → 은닉층 → 출력: 순방향 계산','Input → Hidden layer → Output: forward computation'),
        P('출력과 목표의 차이에서 시작해 오차의 영향 계산','Start at the output error and calculate sensitivity'),
        P('계산한 영향을 이용하는 가중치 갱신은 별도 단계','Updating weights using those sensitivities is a separate step'),
    ],P('역전파: 영향 계산 · 가중치 갱신: 계산 결과를 이용한 조정','Backpropagation computes sensitivities · a subsequent update adjusts weights'),
    labels=[label(600,268,P('역방향으로 영향 계산','Calculate sensitivities backward'),True)])),
    'alexnet': R(IMG('assets/new/alexnet-leopard-predictions.png','표범 사진과 상위 다섯 예측 라벨·확률 막대','A leopard image with its five predicted labels and probability bars',
        '입력 사진 · 실제 분류 · 상위 예측 후보','Input image · correct class · top predictions'),
        right=[T([P('예측 순위','Rank'),P('후보','Label')],[
            [P('1'),P('표범 · leopard','Leopard')],[P('2'),P('재규어 · jaguar','Jaguar')],
            [P('3'),P('치타 · cheetah','Cheetah')],[P('4'),P('눈표범 · snow leopard','Snow leopard')],
            [P('5'),P('이집트 고양이 · Egyptian cat','Egyptian cat')],
        ]),N('2012년 논문의 이미지 분류 사례 · 학습 데이터와 여러 층의 표현·계산 자원의 결합','An image-classification example from 2012 · combines training data, layered representations, and compute')]),
    'alphago': R(G([
        ('후보 수 선택','Candidate moves','정책 신경망: 유망한 다음 수','Policy network: promising moves'),
        ('국면 평가','Position evaluation','가치 신경망: 어느 쪽에 유리한지','Value network: likely outcome'),
        ('탐색과 선택','Search and selection','이후 전개를 고려해 다음 수 선택','Consider continuations and choose a move'),
    ],'바둑판 상태를 신경망과 탐색으로 처리','Process a board position using neural networks and search'),
        N('2016 AlphaGo의 학습: 사람 기보에서 시작 → 자기 대국으로 개선','Training in the 2016 AlphaGo system: learn from human games → improve through self-play')),
    'language-model': R(G([
        ('문맥','Context','오늘 수업에서는 …','In today’s class, …'),
        ('가능한 표현 A','Possible continuation A','인공지능을 배운다','we study artificial intelligence'),
        ('가능한 표현 B','Possible continuation B','함수를 작성한다','we write functions'),
    ],'문맥에 이어질 여러 표현의 가능성을 다루는 모델','A model of possible expressions given a context'),
        N('예시 문장 · 실제 모델의 확률 측정값이 아닌 가능한 후속 표현','Illustrative sentences · possible continuations, not measured model probabilities')),
    'tokens': R(dict(kind='resource-tokens', text=P('unhappiness!'),items=[('un','359'),('h','71'),('appiness','67391'),('!','0')],
        caption=P('cl100k_base의 실제 분할 결과 · 조각마다 대응하는 식별 번호','Actual cl100k_base tokenization · each piece has an identifier')),
        N('토큰은 단어 전체·일부·문장부호 등이 될 수 있음 · 모델의 인코딩에 따라 다른 분할','Tokens may be words, word parts, or punctuation · splitting depends on the model’s encoding')),
    'embeddings': R(F([
        ('식별 번호','Token ID','359 → 항목을 구분하는 번호','359 → identifies an entry'),
        ('벡터 표현','Vector','[0.2, −0.4, 0.7]','[0.2, −0.4, 0.7]'),
        ('순서 정보','Position information','어느 위치의 입력인지 함께 전달','Also supply the input position'),
    ],'벡터는 차원을 줄인 임의 예시 · 토큰 ID의 크기가 의미의 크기는 아님','The reduced vector is illustrative · the magnitude of an ID is not semantic meaning')),
    'attention': R(diagram((1040,270),P('문맥에서 관련된 표현을 함께 참조','Refer to related expressions in context'),[
        box((10,50,430,80),P('민수는 우산을 폈다','Minsu opened an umbrella')),
        box((550,50,480,80),P('비가 그것 위로 떨어졌다','Rain fell onto it')),
    ],[edge('M790 135 V200 H225 V135',both=True)],[
        P('그것이 가리키는 대상을 이해할 때 앞 문장의 우산을 참조','Refer to umbrella in the earlier sentence when interpreting it'),
        P('관련 위치의 정보를 반영해 문맥에 맞는 표현 구성','Use information from related positions to form contextual representations'),
    ],P('관련성 설명용 연결선 · 실제 어텐션 가중치나 내부 사고의 기록은 아님','Illustrative relationship · not measured attention weights or an internal reasoning trace'),
    labels=[label(510,240,P('그것 ↔ 우산','it ↔ umbrella'),True)])),
    'self-supervision': R(T([P('원문에서 만든 과제','Task made from the text'),P('입력','Input'),P('학습 목표','Learning target')],[
        [P('일부 가리기','Mask a portion'),P('오늘은 [가림] 온다','It is [masked] today'),P('비가','raining')],
        [P('다음 표현 예측','Predict what follows'),P('오늘은 비가','Today, rain is'),P('온다','falling')],
    ]),N('정답을 따로 작성하는 대신 원문에서 입력과 목표를 구성 · 두 방식은 학습 목표의 예','Derive inputs and targets from the original text · these are two example learning objectives')),
    'pretraining': R(F([
        ('다양한 자료','Diverse text','문서 · 설명문 · 대화','Documents · explanations · dialogue'),
        ('자기지도 과제','Self-supervised tasks','원문에서 입력과 목표 구성','Derive inputs and targets'),
        ('반복 학습','Repeated training','모델 내부 값 조정','Adjust model parameters'),
        ('기본 모델','Base model','여러 과제의 바탕이 되는 능력','Capabilities for many later tasks'),
    ],'문장을 그대로 찾는 검색 저장소와 구분되는 모델 학습','Model training is distinct from a store that retrieves original sentences')),
    'large-language-model': R(T([P('계열 예시','Model family'),P('학습 목표 예시','Example objective'),P('주요 활용','Common use')],[
        [P('BERT'),P('양쪽 문맥에서 가린 표현 예측','Predict masked text from both sides'),P('문맥에 따른 언어 표현','Contextual language representations')],
        [P('GPT'),P('앞 문맥에서 다음 표현 예측','Predict the next token from preceding text'),P('텍스트 생성','Text generation')],
    ]),N('규모·데이터·계산 자원을 늘린 언어 모델 · 모델과 사용자 인터페이스를 제공하는 서비스는 구분','Language models scaled with data and compute · a model is distinct from a service with a user interface')),
    'context-window': R(dict(kind='resource-context',items=[P('지침','Instructions'),P('앞 대화','History'),P('문서','Documents'),P('현재 질문','Current question'),P('출력 공간','Output space')],
        caption=P('한 요청에서 처리할 수 있는 문맥의 한도 · 영역 비율은 개략 표현','A limit on the context processed in one request · segment proportions are schematic')),
        N('대화가 길어질수록 함께 담을 정보를 선택할 필요 · 파일 저장이나 영구 기억과는 다른 범위','Long conversations require selecting what to include · this is distinct from file storage or permanent memory')),
    'hallucinations': R(T([P('입력 문서','Provided document'),P('생성된 답변 예','Illustrative answer'),P('문서와 대조','Compare with the document')],[
        [P('모임은 금요일에 진행','The meeting is on Friday'),P('금요일 14시에 진행','It starts at 14:00 on Friday'),P('14시라는 정보의 근거 없음','No support for the time 14:00')],
    ]),N('유창한 문장과 근거 있는 내용은 별도 · 실제 모델 응답이 아닌 설명용 사례','Fluency does not establish factual support · a teaching example, not a captured model response')),
    'rag': R(F([
        ('질문','Question','모임은 몇 시인가요?','What time is the meeting?'),
        ('관련 문서 검색','Retrieve a document','문서 A: 금요일 15시','Document A: Friday at 15:00'),
        ('문맥에 추가','Add to context','질문 + 문서 A의 내용','Question + document A'),
        ('근거를 이용한 답변','Answer with evidence','금요일 15시 · 문서 A','Friday at 15:00 · document A'),
    ],'창작 문서의 설명용 흐름 · 잘못 검색한 문서나 해석 오류는 여전히 확인 필요','Illustrative documents and flow · retrieval and interpretation can still be wrong')),
    'code-model': R(C('생성할 코드의 문맥','Context for code generation',
        '// 제목이 비어 있는지 확인\nfunction hasTitle(title) {\n  return title.length > 0;\n}',
        '// Check whether a title is nonempty\nfunction hasTitle(title) {\n  return title.length > 0;\n}'),
        N('설명과 앞선 코드에서 이어질 코드를 생성하는 사례 · 실행 여부와 정확성은 별도 확인','An example of generating code from a description and preceding code · execution and correctness need verification'),
        N('2021년 Codex: 코드 생성 모델 · 현재 Codex: 개발 에이전트 제품','Codex in 2021: a code-generation model · Codex today: a coding-agent product')),
    'code-completion': R(dict(kind='resource-editor',prefix=P('function hasTitle(title) {'),suggestion=P('  return title.length > 0;'),suffix=P('}'),
        caption=P('자동 완성의 편집기 모식도 · 흐린 부분은 아직 수락하지 않은 제안','Schematic editor · faded text is an unaccepted suggestion')),
        F([('제안 표시','Show suggestion','앞 코드와 주석에 따른 후보','A candidate based on code and comments'),
           ('개발자 선택','Developer decision','수락 · 수정 · 거절','Accept · edit · reject')],
          '제안을 적용하고 실행할 책임을 가진 개발자','The developer chooses what to apply and run')),
    'instruction-tuning': R(F([
        ('요청·응답 쌍','Request–response pairs','사람이 작성한 바람직한 응답','Demonstrations of desired responses'),
        ('추가 학습','Additional training','응답을 목표로 내부 값 갱신','Update parameters using the responses'),
        ('지시를 따르는 모델','Instruction-following model','새 요청의 의도에 맞춘 응답','Respond to a new request’s intent'),
    ],'학습 데이터로 모델을 조정하는 단계 · 사용 중 프롬프트 수정과 구분','A training stage that changes the model · distinct from editing a prompt at use time')),
    'human-feedback': R(F([
        ('여러 답변','Candidate answers','같은 요청의 답변 A · B','Answers A and B to the same request'),
        ('사람의 비교','Human comparison','정확성 · 요구 충족을 평가','Judge correctness and instruction following'),
        ('학습에 반영','Use as a learning signal','선호 정보로 응답 경향 조정','Adjust behavior using preference data'),
    ],'시범 답안의 모방과 선호 비교는 서로 다른 학습 자료','Demonstrated responses and preference comparisons provide different training data'),
        N('피드백 수집과 모델 갱신은 별도 절차 · 개별 클릭이 즉시 가중치를 바꾸는 구조는 아님','Feedback collection and model updates are separate procedures · a click does not imply an immediate parameter update')),
    'conversational-development': R(F([
        ('개발자 요청','Developer request','조건과 관련 코드 전달','Provide requirements and code'),
        ('모델 제안','Model proposal','코드와 설명 반환','Return code and an explanation'),
        ('개발자 실행','Developer execution','코드 적용 후 동작 확인','Apply the code and check behavior'),
        ('결과 전달','Report the result','관찰한 문제와 수정 요청','Describe the issue and request a revision'),
    ],'파일 적용과 실행은 개발자가 담당하는 대화형 개발 과정','A conversational workflow where the developer applies and runs code',P('수정한 제안을 다시 확인','Check the revised proposal'))),
    'title-validation-case': R(C('문자열 입력 · boolean 반환','String input · boolean result',TITLE),
        T([P('입력','Input'),P('기대 결과','Expected')],[
            [P('공지사항','Notice'),P('true')],[P('빈 문자열','Empty string'),P('false')],[P('공백 3개','Three spaces'),P('false')],
        ]),N('앞뒤 공백 제거 후 1~20글자 · 예제의 길이는 JavaScript UTF-16 단위','Trim outer whitespace, then allow length 1–20 · length uses JavaScript UTF-16 units')),
    'tool-calling': R(F([
        ('모델의 요청','Model request','도구 이름과 인자 생성','Generate a tool name and arguments'),
        ('외부 실행','External execution','애플리케이션이 도구 실행','The application runs the tool'),
        ('결과 반환','Return a result','도구의 출력을 모델에 전달','Send the tool output to the model'),
    ],'호출 요청을 만드는 모델과 실제 실행하는 애플리케이션의 역할 구분','Separate the model’s request from the application’s execution'),
        C('가상의 파일 읽기 도구 요청','Illustrative file-reading tool request',
          '{\n  "name": "read_file",\n  "arguments": { "path": "src/title.js" }\n}',language='json')),
    'tool-permissions': R(T([P('요청','Request'),P('환경의 범위','Environment scope'),P('실행 결과','Execution decision')],[
        [P('프로젝트 파일 읽기','Read a project file'),P('읽기 허용','Reading allowed'),P('파일 내용 반환','Return file content')],
        [P('코드 수정','Edit code'),P('읽기만 허용','Read-only'),P('수정 제한','Editing restricted')],
        [P('외부 서버 접속','Access a remote server'),P('네트워크 제한','Network restricted'),P('정책에 따라 차단·승인 요청','Block or request approval under policy')],
    ]),N('설명용 권한 구성 · 기술적 실행 경계와 승인 정책은 별도 제어','Illustrative permissions · technical boundaries and approval policy are separate controls')),
    'agent-loop': R(diagram((1040,310),P('도구의 결과를 보고 다음 행동을 정하는 반복','Choose the next action from observed tool results'),[
        box((10,65,220,85),P('목표·현재 상태','Goal and state')),
        box((275,65,220,85),P('행동 선택','Choose an action')),
        box((540,65,220,85),P('도구 실행','Run a tool')),
        box((805,65,220,85),P('결과 관찰','Observe results')),
    ],[edge('M230 108 H270'),edge('M495 108 H535'),edge('M760 108 H800'),edge('M915 150 V225 H385 V155')],[
        P('목표와 현재 상태를 바탕으로 행동 선택','Choose an action from the goal and current state'),
        P('도구 실행 후 결과를 관찰해 다음 행동 결정','Observe the tool result and choose what to do next'),
        P('완료하거나 진행이 불가능하면 종료·상태 보고','Stop and report when complete or unable to proceed'),
    ],P('결과에 따른 작업 반복 · 모델 가중치의 학습과는 별도','A work loop driven by results · separate from learning model parameters'),
    labels=[label(650,270,P('계속 진행 / 완료·진행 불가 시 종료','Continue / stop when done or blocked'),True)])),
    'development-tools': R(T([P('개발 작업','Development task'),P('도구 범주','Tool capability'),P('얻는 결과','Result')],[
        [P('현재 코드 확인','Inspect current code'),P('파일 읽기·검색','Read and search files'),P('함수와 관련 파일의 내용','Functions and related file content')],
        [P('변경 적용','Apply a change'),P('파일 편집','Edit files'),P('수정된 코드','Modified code')],
        [P('동작 확인','Check behavior'),P('터미널 명령 실행','Run terminal commands'),P('실행 결과·오류','Output and errors')],
    ]),N('Claude Code·Codex가 제공하는 개발 도구의 공통 범주 · 세부 도구 이름과 권한은 환경별 차이','Common development capabilities in Claude Code and Codex · tool names and permissions vary by environment')),
    'agent-repair-case': R(C('수정 전 · 공백 처리 누락','Before repair · missing whitespace handling',BEFORE),
        C('수정 후','After repair',TITLE),right=[
        T([P('입력','Input'),P('수정 전','Before'),P('수정 후','After')],[
            [P('공백 3개','Three spaces'),P('true'),P('false')],[P('공지사항','Notice'),P('true'),P('true')],
        ]),N('읽기 → 같은 입력 실행 → 코드 수정 → 재실행','Read → run the input → edit → rerun'),
        N('표는 실제 코드 실행값 · 순서는 에이전트 작업의 설명용 모형','Values are actual code outputs · the sequence illustrates an agent workflow')]),
    'reasoning-models': R(F([
        ('입력','Input','문제와 현재의 근거','The problem and available evidence'),
        ('응답 전 추론 계산','Reasoning before response','대안 검토 · 여러 단계의 처리','Consider alternatives and multiple steps'),
        ('답변·행동','Answer or action','검토 결과를 이용한 출력','Produce output using the computation'),
    ],'어려운 과제에 더 많은 계산을 사용할 수 있는 모델','Models can use additional computation on difficult tasks'),
        N('추가 계산에는 시간·토큰 비용 발생 · 내부 사고를 재현한 대화록이 아닌 처리 구조','Additional computation uses time and tokens · this shows a process, not an internal thought transcript')),
    'multimodal-models': R(C('화면과 함께 제공하는 코드 발췌','Code supplied alongside a screen image',
        '.error {\n  height: 20px;\n  overflow: hidden;\n}',language='css'),
        right=[S(P('공백 3개','Three spaces'),P('제목을 입력하세요. 앞뒤 공백을 제외한 제목이 필요합니다.','Enter a title. Outer whitespace does not count.'),
                 P('오류 안내 일부가 잘린 화면 모식도','Schematic screen with a clipped error message'),state='clipped'),
               N('텍스트 코드 + 화면 이미지 → 함께 해석할 입력','Code text + screen image → inputs interpreted together')]),
    'computer-use': R(S(P('공지사항','Notice'),P('등록 준비','Ready to submit'),P('조작 대상 화면의 모식도','Schematic view of the interface to control')),
        right=[F([
            ('화면 관찰','Observe','입력 칸과 버튼 확인','Locate the field and button'),
            ('행동 실행','Act','제목 입력 · 등록 클릭','Enter a title and click Submit'),
            ('새 화면 확인','Check','변경된 상태 관찰','Observe the updated state'),
        ],'관찰과 실제 조작·결과 확인의 반복','Repeat observation, action, and outcome checking')]),
    'mcp': R(diagram((1040,350),P('앱의 MCP 클라이언트와 서버 연결','Connections between an app’s MCP clients and servers'),[
        box((10,95,210,90),P('AI 앱 · Host','AI app · Host')),
        box((300,30,220,80),P('Client A')),
        box((300,220,220,80),P('Client B')),
        box((700,30,325,80),P('문서 Server','Document server')),
        box((700,220,325,80),P('파일 Server','File server')),
    ],[edge('M220 125 H255 V70 H295'),edge('M220 160 H255 V260 H295'),
       edge('M525 70 H695',both=True),edge('M525 260 H695',both=True)],[
        P('Host 내부의 Client가 각 Server와 연결','Clients within the host connect to individual servers'),
        P('기능 목록 확인 → 요청 → 결과 반환','Discover capabilities → request → return a result'),
        P('Server는 로컬 또는 원격에서 실행','Servers may run locally or remotely'),
    ],P('Model Context Protocol · 도구·문맥의 통신 규약이며 실행 권한 자체는 별도','Model Context Protocol · a protocol for tools and context, separate from execution permissions'),
    labels=[label(800,165,P('기능 발견 · 요청 · 결과','Discover · request · result'),True)])),
    'project-context': R(T([P('파일 예시','Example file'),P('역할','Role'),P('연결','Relationship')],[
        [P('src/title.js'),P('제목 조건 판단','Validate title conditions'),P('UI와 서버가 사용하는 기준','Criteria used by UI and server')],
        [P('PostForm.jsx'),P('입력과 결과 표시','Input and result display'),P('등록 요청 → 서버','Submission request → server')],
        [P('server/posts.js'),P('제목 확인과 저장 처리','Title validation and storage'),P('처리 결과 → UI','Result → UI')],
        [P('package.json'),P('실행 명령과 의존성','Commands and dependencies'),P('작업 환경의 실행 진입점','Entry points for running the project')],
    ]),N('게시글 프로젝트의 설명용 파일 지도 · 코드·호출 관계·실행 방법을 함께 파악','An illustrative post-project file map · understand code, calls, and how to run it')),
    'context-engineering': R(F([
        ('전체 프로젝트','Whole project','코드 · 문서 · 기록 · 리소스','Code · docs · records · assets'),
        ('현재 작업에 맞춰 선택','Select for the task','제목 규칙 · 관련 코드 · 실행 방법','Title rules · related code · commands'),
        ('현재 문맥','Current context','필요한 정보를 필요한 때 제공','Supply useful information when needed'),
    ],'모든 파일의 일괄 입력보다 관련 정보의 선택과 적시 조회','Select relevant information and retrieve it at the right time')),
    'agent-skills': R(C('반복 절차를 묶은 스킬 폴더 예시','Illustrative skill folder for a reusable procedure',
        'title-check/\n  SKILL.md\n  references/\n    cases.txt\n  scripts/\n    check-title.mjs',language='text'),
        right=[F([
            ('이름·설명','Name and description','어떤 작업에 쓰는지 판단','Decide when it is useful'),
            ('절차 본문','Instructions','선택한 SKILL.md 읽기','Read the selected SKILL.md'),
            ('보조 자료','Supporting resources','필요한 자료·스크립트 사용','Use references and scripts as needed'),
        ],'프로젝트의 상시 규칙과 구분되는 특정 작업의 반복 절차','A reusable task procedure, distinct from standing project rules')]),
    'progress-notes': R(T([P('구분','Field'),P('남기는 기록','Recorded information')],[
        [P('변경','Changed'),P('제목 검사에 앞뒤 공백 제거 추가','Added outer-whitespace trimming')],
        [P('실행 근거','Execution evidence'),P('공백 3개 → false · 정상 제목 → true','Three spaces → false · normal title → true')],
        [P('미완료','Incomplete'),P('서버 저장 · UI 성공/실패 표시 미확인','Storage and UI success/failure states not yet checked')],
        [P('재개 위치','Resume point'),P('변경 파일 · 실행 명령 · 결과 파일 위치','Changed files · commands · result-file paths')],
    ]),N('완료 여부의 근거와 아직 확인하지 않은 범위를 분리해 기록','Record evidence of completion separately from unverified work')),
    'context-compaction': R(F([
        ('긴 작업 이력','Long work history','대화와 반복된 도구 출력','Conversation and repeated tool output'),
        ('핵심 요약','Essential summary','목표 · 결정 · 현재 상태 · 남은 일','Goal · decisions · state · remaining work'),
        ('원본 재조회','Reopen original files','필요한 세부는 저장된 위치에서 확인','Read details from their saved locations'),
    ],'요약으로 문맥을 줄이되 필요한 세부를 다시 확인할 경로 유지','Reduce context while preserving a way to recover necessary detail'),
        N('요약 과정에서 중요한 정보가 빠질 수 있으므로 현재 파일과 근거 재확인','A summary may omit important information; recheck current files and evidence')),
    'project-context-case': R(T([P('자료','Resource'),P('역할','Role'),P('제목 수정 작업에서의 용도','Use in the title task')],[
        [P('AGENTS.md / CLAUDE.md'),P('프로젝트 지침','Project guidance'),P('수정 범위와 공통 규칙 확인','Check scope and conventions')],
        [P('src/title.js'),P('현재 코드','Current code'),P('실제 구현과 문제 확인','Inspect implementation and bug')],
        [P('SKILL.md'),P('반복 절차','Reusable procedure'),P('작업 순서와 자료 참조','Follow steps and consult resources')],
        [P('progress.txt'),P('진행 상태','Progress state'),P('확인한 결과와 남은 일 파악','Read verified results and remaining work')],
    ]),N('파일명은 제품·프로젝트별 예시 · 각 자료가 제공하는 정보의 역할 구분','Filenames vary by product and project · distinguish each resource’s role')),
    'specification': R(T([P('명세 항목','Specification item'),P('조건','Requirement')],[
        [P('입력','Input'),P('문자열 제목','A string title')],
        [P('유효 범위','Valid range'),P('앞뒤 공백 제거 후 길이 1~20','Length 1–20 after trimming outer whitespace')],
        [P('잘못된 입력','Invalid input'),P('유효하지 않은 제목은 저장하지 않음','Do not store an invalid title')],
        [P('저장 실패','Storage failure'),P('오류 표시 · 성공으로 표시하지 않음','Show an error; do not show success')],
    ]),N('구현 방식보다 먼저 정하는 기능의 동작 조건','Behavioral requirements defined before implementation choices')),
    'acceptance-criteria': R(T([P('상황','Situation'),P('기대 동작','Expected behavior'),P('확인할 근거','Evidence to check')],[
        [P('공백 제목 등록','Submit whitespace'),P('저장하지 않음','Do not store'),P('거부 결과 · 저장 기록 없음','Rejection and no stored record')],
        [P('정상 제목 등록','Submit a valid title'),P('저장 후 성공 표시','Show success after saving'),P('저장된 제목 · 화면 표시','Stored title and UI message')],
        [P('서버 저장 실패','Storage fails'),P('오류 표시','Show an error'),P('실패 응답 · 성공 표시 없음','Failure response and no success message')],
    ]),N('작업 전에 정하는 완료 기준 · 아직 모든 기능이 통과했다는 결과가 아님','Completion criteria set before work · these are criteria, not claimed passing results')),
    'automated-tests': R(C('입력과 고정 기대값의 비교','Compare inputs with fixed expectations',
        "import assert from 'node:assert/strict';\n\nassert.equal(isValidTitle(''), false);\nassert.equal(isValidTitle('   '), false);\nassert.equal(isValidTitle('A'), true);\nassert.equal(isValidTitle('A'.repeat(20)), true);\nassert.equal(isValidTitle('A'.repeat(21)), false);"),
        right=[T([P('검사 범위','Check'),P('수정 후 결과','After repair')],[
            [P('빈 값 · 공백','Empty · whitespace'),P('거부','Rejected')],
            [P('1 · 20글자','Length 1 · 20'),P('허용','Accepted')],
            [P('21글자','Length 21'),P('거부','Rejected')],
            [P('전체 예제 8건','All 8 example cases'),P('8건 통과','8 passed')],
        ]),N('isValidTitle을 불러온 실행 환경의 발췌 · 기대값을 바꾸지 않고 같은 검사를 반복','Excerpt with isValidTitle loaded · repeat the checks without changing expectations')]),
    'browser-verification': R(C('Playwright · 실행 중인 예제 앱에 적용하는 발췌','Playwright excerpt for a running example app',
        "await page.getByLabel('제목').fill('공지사항');\nawait page\n  .getByRole('button', { name: '등록', exact: true })\n  .click();\nawait expect(page.getByRole('status')).toHaveText('등록 완료');",
        "await page.getByLabel('Title').fill('Notice');\nawait page\n  .getByRole('button', { name: 'Submit', exact: true })\n  .click();\nawait expect(page.getByRole('status')).toHaveText('Submitted');"),
        right=[T([P('관찰 범위','Observation'),P('확인하는 것','What is verified')],[
            [P('화면','UI'),P('입력 · 클릭 · 성공/오류 표시','Input · click · success/error display')],
            [P('요청·응답','Request and response'),P('등록 요청과 서버의 처리 결과','Submission and server response')],
            [P('저장 결과','Stored result'),P('실제 저장·재조회한 데이터','Data actually stored and retrieved')],
        ]),N('화면 표시 확인만으로 실제 저장을 검증한 것은 아님','A UI message alone does not verify persistent storage')]),
    'agent-hooks': R(F([
        ('이벤트 발생','Event occurs','도구 사용 전·후 등 지정한 시점','A configured point before or after tool use'),
        ('등록한 명령 실행','Run a configured command','검사·정리 같은 반복 동작','Repeated checks or formatting'),
        ('결과 처리','Handle the result','출력·오류를 작업 흐름에 전달','Return output or errors to the workflow'),
    ],'Claude Code 예: PostToolUse의 Edit/Write 이후 검사 · 차단 여부는 이벤트·설정에 따름','Claude Code example: check after Edit/Write in PostToolUse · blocking depends on the event and configuration'),
        N('에이전트 수명 주기의 Hooks · React Hooks와는 다른 기능','Hooks in an agent’s lifecycle · distinct from React Hooks')),
    'execution-harness': R(diagram((1040,370),P('모델의 작업 실행을 관리하는 하네스','A harness manages execution around a model'),[
        box((380,145,280,80),P('모델','Model'),P('다음 행동 판단','Choose the next action')),
        box((10,25,270,80),P('도구·환경','Tools and runtime')),
        box((760,25,270,80),P('작업 상태','Work state')),
        box((10,270,270,80),P('검사 결과','Check results')),
        box((760,270,270,80),P('한도·중단 조건','Limits and stopping')),
    ],[edge('M280 65 H330 V185 H375'),edge('M760 65 H710 V185 H665'),
       edge('M280 310 H330 V200 H375'),edge('M665 200 H710 V310 H755')],[
        P('도구와 실행 환경을 연결하고 상태 관리','Connect tools and runtime; manage state'),
        P('결과에 따라 다음 호출·재시도·종료를 관리','Manage the next call, retry, or stop based on results'),
        P('모델의 추론과 모델 밖의 실행 기반을 구분','Distinguish model reasoning from the surrounding execution infrastructure'),
    ],P('모델·도구·상태·검사·한도를 연결하는 실행 기반','Execution infrastructure connecting model, tools, state, checks, and limits'))),
    'change-review': R(C('변경 전','Before',BEFORE),C('변경 후','After',TITLE),right=[
        T([P('리뷰 기준','Review criterion'),P('확인 근거','Evidence')],[
            [P('요구 충족','Meets requirements'),P('공백 제거 · 길이 판단','Trimming and length checks')],
            [P('동작 유지','Preserves behavior'),P('정상·경계 입력의 실행 결과','Normal and boundary-case outputs')],
            [P('변경 범위','Scope of change'),P('요구와 무관한 변경 유무','Any unrelated changes')],
        ]),N('코드 차이와 검사 결과를 함께 보는 개발자의 판단','Developer judgment considers both the code diff and check results')]),
    'post-feature-case': R(F([
        ('조건 정의','Define behavior','명세 · 완료 기준','Specification · acceptance criteria'),
        ('순차 구현','Implement in order','함수 → 서버 → 화면','Function → server → UI'),
        ('동작 검증','Verify behavior','단위 검사 + 전체 등록 동작','Unit checks + full submission flow'),
        ('변경 리뷰','Review changes','코드 차이와 완료 근거 대조','Compare changes with completion evidence'),
    ],'같은 게시글 기능을 조건·구현·검증·리뷰로 연결한 개발 절차','One post feature connected through requirements, implementation, verification, and review')),
    'independent-tasks': R(C('먼저 합의하는 요청·응답 계약 예','Agree on the request/response contract first',
        'POST /posts\n요청: { "title": "공지사항" }\n성공: 201\n제목 오류: 400\n저장 실패: 500',
        'POST /posts\nRequest: { "title": "Notice" }\nSuccess: 201\nInvalid title: 400\nStorage failure: 500',language='text'),
        right=[G([
            ('UI 작업','UI task','입력 · 요청 · 성공/실패 표시','Input · request · success/error display'),
            ('서버 작업','Server task','제목 검증 · 저장 · 응답','Title validation · storage · response'),
        ],'공유 계약을 유지하면서 나눌 수 있는 작업 범위','Work can be separated while preserving the shared contract')]),
    'subagents': R(F([
        ('주 에이전트','Main agent','목표 · 범위 · 필요한 문맥 전달','Provide goal, scope, and context'),
        ('서브에이전트','Subagent','제목 규칙 검사처럼 한정된 과제','A bounded task such as checking title rules'),
        ('근거와 결과 반환','Return findings','파일 위치 · 관찰 결과 · 남은 문제','File locations · observations · open issues'),
    ],'작은 작업의 위임 구조 · 반드시 병렬 실행이나 파일 수정을 뜻하지 않음','Delegating a bounded task does not necessarily imply parallel execution or file edits')),
    'agent-teams': R(diagram((1040,340),P('공유 작업 목록과 메시지로 조정하는 팀','A team coordinates through shared tasks and messages'),[
        box((380,20,280,75),P('조정자','Coordinator')),
        box((10,215,270,80),P('UI 작업자','UI worker')),
        box((380,215,280,80),P('공유 작업 목록','Shared tasks')),
        box((760,215,270,80),P('서버 작업자','Server worker')),
    ],[edge('M450 95 V140 H145 V210'),edge('M590 95 V140 H895 V210'),
       edge('M285 255 H375',both=True),edge('M665 255 H755',both=True),edge('M145 215 V175 H895 V210',both=True)],[
        P('조정자가 작업을 나누고 전체 결과를 종합','A coordinator divides work and combines results'),
        P('작업자는 공유 목록으로 진행 상태를 확인','Workers consult a shared task list'),
        P('메시지로 요청·응답 계약의 변경을 공유','Messages communicate changes to the request/response contract'),
    ],P('Claude Code의 Agent Teams는 실험 기능 · 제품별 제공 상태와 동작에 차이','Agent Teams in Claude Code is experimental · availability and behavior differ by product'))),
    'git-branches': R(diagram((1040,320),P('공통 커밋에서 갈라지는 변경 이력','Commit histories diverging from a shared commit'),[
        box((10,120,240,85),P('공통 커밋 A','Shared commit A'),P('main')),
        box((520,20,280,85),P('UI 변경 B','UI change B'),P('feature/ui')),
        box((520,220,280,85),P('서버 변경 C','Server change C'),P('feature/server')),
    ],[edge('M250 145 H380 V63 H515'),edge('M250 180 H380 V263 H515')],[
        P('공통 커밋 A에서 UI 변경 B와 서버 변경 C로 이력 분기','History diverges from A into UI change B and server change C'),
        P('브랜치 이름은 특정 커밋을 가리키는 참조','A branch name is a reference pointing to a commit'),
    ],P('변경 이력의 분리 · 브랜치 생성은 별도 작업 폴더 생성과 구분','Separate change histories · creating a branch does not create a working directory'))),
    'git-worktrees': R(G([
        ('repo/','repo/','main\n기준 작업 폴더','main\nMain working directory'),
        ('post-ui/','post-ui/','feature/ui\nUI 작업 폴더','feature/ui\nUI working directory'),
        ('post-server/','post-server/','feature/server\n서버 작업 폴더','feature/server\nServer working directory'),
    ],'같은 저장소를 공유하며 서로 다른 브랜치를 별도 폴더에 체크아웃','Share one repository while checking out different branches in separate directories'),
        C('커밋이 있는 예제 저장소에서 실행하는 명령','Command for an example repository with an existing commit',
          'git worktree add -b feature/ui ../post-ui',language='bash'),
        N('작업 파일 분리와 DB·포트·외부 서비스의 격리는 별도','Separate working files do not isolate databases, ports, or external services')),
    'parallel-integration': R(F([
        ('각 작업 결과','Separate results','UI 코드 + 서버 코드','UI code + server code'),
        ('변경 통합','Integrate changes','파일 충돌과 코드 관계 확인','Resolve conflicts and check relationships'),
        ('통합 검증','Verify together','공유 계약과 전체 동작 재검사','Recheck the contract and full behavior'),
    ],'병합 성공과 기능의 정상 동작은 별도 확인','A successful merge does not establish correct behavior'),
        T([P('UI의 가정','UI assumption'),P('서버의 응답','Server response'),P('통합 문제','Integration issue')],[
            [P('200만 성공으로 처리','Only 200 counts as success'),P('201 Created'),P('저장했지만 UI는 실패로 표시','Saved, but the UI reports failure')],
        ])),
    'persistent-goals': R(T([P('목표의 구성','Goal component'),P('게시글 기능의 예','Post-feature example')],[
        [P('완료할 결과','Outcome'),P('제목 조건과 등록 성공/실패 동작 충족','Meet title and submission behavior requirements')],
        [P('완료 근거','Evidence'),P('코드 검사 · 요청/저장/화면 확인','Code checks and request/storage/UI evidence')],
        [P('범위·한도','Scope and limits'),P('허용 파일·도구 · 실행 예산','Allowed files/tools and execution budget')],
        [P('중단 조건','Stopping condition'),P('완료 · 사용자 중단 · 한도 · 해결 불가','Complete · user pause · limit · blocker')],
    ]),N('결과 확인 → 미완료이면 다음 작업 · 완료하면 종료 · 지원 환경에서 사용하는 Codex Goals의 예','Check results → continue if incomplete, stop when done · an example of Codex Goals in a supported environment')),
    'pause-and-resume': R(F([
        ('중단 전 기록','Record before stopping','목표 · 변경 · 확인 결과 · 미완료','Goal · changes · evidence · open work'),
        ('재개 시 대조','Recheck on resume','현재 파일·폴더·실행 환경 확인','Inspect current files, directory, and runtime'),
        ('남은 작업 진행','Continue work','유효한 근거에서 다음 작업 선택','Choose work from current evidence'),
    ],'상태가 바뀌었다면 이전 검사도 다시 확인 · 모든 프로세스의 자동 복원을 뜻하지 않음','Recheck old results if state changed · resumption does not imply restoring every process')),
    'scheduled-automation': R(F([
        ('예약 시점','Scheduled time','월요일 09:00 · Asia/Seoul','Monday 09:00 · Asia/Seoul'),
        ('실행 조건','Execution conditions','프로젝트 · 도구 · 권한 확인','Check project, tools, and permissions'),
        ('작업과 결과','Work and results','검사 실행 후 결과 기록·검토','Run checks, record and review results'),
    ],'예약 예시 · 로컬 프로젝트 작업에는 컴퓨터와 앱의 실행이 필요','Illustrative schedule · local project tasks require the computer and app to be running'),
        T([P('기능','Mechanism'),P('결정하는 것','What it determines')],[
            [P('Hooks'),P('작업 중 어떤 이벤트에 반응할지','Which event during work triggers an action')],
            [P('지속 목표','Persistent goal'),P('어떤 결과까지 계속할지','Which outcome to work toward')],
            [P('예약','Schedule'),P('언제 작업을 시작할지','When work starts')],
        ])),
}

assert len(RESOURCES) == 60

# The client objects are components inside the host, not separate AI apps.
RESOURCES['mcp']['columns'][0][0]['frames'] = [
    dict(rect=(0,5,555,325), text=P('Host 내부','Inside the host'))
]


def describe_resource(ident):
    """Describe placed blocks, rather than claiming every research candidate was used."""
    kinds = {'code':'코드 발췌', 'figure':'발췌 이미지', 'resource-context':'문맥 구성도',
             'resource-diagram':'관계도', 'resource-editor':'편집기 모식도',
             'resource-flow':'단계도', 'resource-groups':'역할·사례 비교',
             'resource-screen':'화면 모식도', 'resource-tokens':'토큰 분할표', 'table':'표'}
    parts = []
    for column in RESOURCES[ident]['columns']:
        for block in column:
            if block['kind']=='resource-note':
                continue
            if block['kind']=='table':
                title=' / '.join(cell[0] for cell in block['head'])
            else:
                title=(block.get('label') or block['caption'])[0]
            parts.append(kinds[block['kind']]+' — '+title)
    return '실제 배치 자료: '+'; '.join(parts)+'.'
