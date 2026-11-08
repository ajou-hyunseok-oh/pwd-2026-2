"""Place selected Week 10 assets before writing the full Week 9 slide bodies.

Eleven direct/adapted mappings and five structure references are implemented.
Original rasters/tables remain unchanged in the audit. All teaching adaptations
are editable and bilingual; no new standalone code example is introduced here.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = next((ROOT/'materials').glob('[[]PWD Week10]*.pdf')).name


def pair(ko, en=None):
    return (ko, ko if en is None else en)


def table(head, rows):
    return dict(kind='resource-wide-table' if len(head)==4 else 'table', head=head, rows=rows)


def note(ko, en):
    return dict(kind='resource-note', text=pair(ko,en))


def flow(items, caption, repeat=None):
    return dict(kind='resource-flow', items=[dict(title=a,body=b) for a,b in items], caption=caption, repeat=repeat)


def box(rect, title, body=None):
    return dict(rect=rect,title=title,body=body)


def edge(path, **opts):
    return dict(d=path,**opts)


def label(x,y,text,small=False):
    return dict(x=x,y=y,text=text,small=small)


def diagram(size, description, boxes, edges, routes, caption, labels=(), dots=()):
    return dict(kind='resource-diagram',size=size,description=description,
                boxes=boxes,edges=edges,routes=routes,caption=caption,labels=labels,dots=dots)


def resource(assets, pages, correction, blocks, *, refs=()):
    return dict(assets=assets.split(),pages=pages,correction=correction,layout='single',columns=[blocks],
                sources=[f'materials/{PDF} · PDF {", ".join(map(str,pages))}쪽',*refs])


RESOURCES = {
    'turing-test': resource('T04', [4],
        '역할 표를 편집형 한영 표로 변환. 판정 범위를 문자 대화에서 관찰한 행동으로 한정. 그림 I04-test는 같은 관계의 대안으로 보관.', [
        table([pair('참여자·기준','Participant / criterion'),pair('역할과 관찰 대상','Role and observation')], [
            [pair('질문자','Interrogator'),pair('상대의 정체를 모르는 상태에서 문자로 질문','Ask text questions without knowing the respondent’s identity')],
            [pair('응답자 A · 사람','Respondent A · Human'),pair('질문에 문자로 응답','Respond to questions in text')],
            [pair('응답자 B · 기계','Respondent B · Machine'),pair('같은 대화 조건에서 문자로 응답','Respond in text under the same conversational conditions')],
            [pair('판별 기준','Assessment'),pair('문자 응답으로 사람과 기계를 구별할 수 있는지 관찰','Observe whether text responses allow the two to be distinguished')],
        ]), note('평가 범위: 대화에서 나타난 행동 · 의식이나 모든 과제의 해결 능력을 증명하는 기준으로 확대 불가',
                 'Scope: behavior observed in conversation · This does not establish consciousness or competence on every task'),
    ]),
    'perceptron': resource('I05-unit', [5],
        '오른쪽 입력·가중치·합산·판단 구조를 편집형 도식으로 재구성. 두 입력으로 단순화하고 임곗값 비교를 명시. 생물학 용어·일반 활성 함수 표기·XOR 보조 그림 제외.', [
        diagram((1060,300),pair('두 입력을 가중합한 뒤 임곗값과 비교하는 퍼셉트론','A perceptron compares a weighted sum of two inputs with a threshold'),[
            box((10,45,140,65),pair('입력 1','Input 1')),
            box((10,195,140,65),pair('입력 2','Input 2')),
            box((200,45,180,65),pair('× 가중치 1','× Weight 1')),
            box((200,195,180,65),pair('× 가중치 2','× Weight 2')),
            box((425,120,190,65),pair('가중합','Weighted sum')),
            box((660,112.5,190,80),pair('임곗값 비교','Threshold'),pair('기준 이상인지 판단','Compare with cutoff')),
            box((910,112.5,140,80),pair('출력','Output'),pair('0 또는 1','0 or 1')),
        ], [edge('M150 78 H195'),edge('M150 228 H195'),edge('M380 78 H400 V145 H420'),
            edge('M380 228 H400 V160 H420'),edge('M615 152 H655'),edge('M850 152 H905')], [
            pair('입력 1 × 가중치 1, 입력 2 × 가중치 2','Multiply each input by its weight'),
            pair('두 곱의 합으로 가중합 계산','Add the weighted inputs'),
            pair('가중합을 임곗값과 비교해 0 또는 1 출력','Compare the sum with the threshold to output 0 or 1'),
        ],pair('입력 두 개를 사용하는 단일 퍼셉트론의 판단 구조','Decision structure of a single perceptron with two inputs')),
    ]),
    'expert-system': resource('I06', [6],
        '사용자·인터페이스·추론 엔진·지식 베이스·결과의 구성과 모든 연결을 유지한 편집형 도식. 한국어 비트맵의 영문 전용 문제를 해소.', [
        diagram((1040,390),pair('지식 베이스와 추론 엔진을 연결한 전문가 시스템','An expert system connects a knowledge base and an inference engine'),[
            box((10,125,160,80),pair('사용자','User'),pair('증상 입력','Enter symptoms')),
            box((225,125,185,80),pair('인터페이스','Interface')),
            box((465,125,210,80),pair('추론 엔진','Inference engine'),pair('적용할 규칙 선택','Select applicable rules')),
            box((795,20,230,80),pair('지식 베이스','Knowledge base'),pair('분야의 사실·규칙','Domain facts and rules')),
            box((795,240,230,80),pair('결과·판단','Result / decision'),pair('원인 후보','Possible causes')),
        ], [edge('M170 165 H220'),edge('M410 165 H460'),edge('M675 145 H720 V50 H790'),
            edge('M795 80 H750 V185 H680'),edge('M675 195 H710 V280 H790'),
            edge('M910 320 V360 H90 V210')], [
            pair('사용자 → 인터페이스 → 추론 엔진: 증상 전달','User → Interface → Inference engine: provide symptoms'),
            pair('추론 엔진 ↔ 지식 베이스: 사실과 규칙 조회·적용','Inference engine ↔ Knowledge base: consult and apply facts and rules'),
            pair('추론 엔진 → 결과·판단 → 사용자: 원인 후보 전달','Inference engine → Result → User: return possible causes'),
        ],pair('분야의 지식을 보관하는 부분과 규칙을 적용하는 부분의 분리','Separate stored domain knowledge from the process that applies its rules')),
    ]),
    'ai-winter': resource('I03', [3],
        '실측값처럼 보이는 곡선을 시기별 개략 시간선으로 정리. 1990년 머신러닝 최초 등장 표기와 미학습 딥러닝·생성형 AI 구간 제거.', [
        flow([
            (pair('1950~1960년대','1950s–1960s'),pair('초기 연구의 성과\n지능 구현에 대한 기대','Early research results\nExpectations for machine intelligence')),
            (pair('1970년대','1970s'),pair('성과와 기대의 차이\n일부 연구 지원의 위축','Gap between results and expectations\nReduced support in some areas')),
            (pair('1980년대','1980s'),pair('전문가 시스템의 확산\n상용화에 대한 기대','Spread of expert systems\nCommercial expectations')),
            (pair('1980년대 말 이후','Late 1980s onward'),pair('유지 비용과 적용 한계\n관심·투자의 위축','Maintenance costs and practical limits\nDeclining interest and investment')),
        ],pair('기대와 연구 지원 변화의 개략적 흐름 · 분야·지역에 따라 다른 시기와 배경',
                'A qualitative timeline of expectations and research support · Timing and causes varied across fields and regions')),
    ]),
    'neural-network': resource('I08-network', [8],
        '단일 퍼셉트론과 2입력·2은닉·1출력 연결 구조를 보존한 편집형 도식. 한영 라벨을 분리하고 역전파·손실 용어는 추가하지 않음.', [
        diagram((1020,340),pair('단일 퍼셉트론과 여러 층으로 연결한 신경망 비교','A single perceptron and a network of connected layers'),[],[
            edge('M77 112 L220 184'),edge('M77 248 L220 196'),
            edge('M527 110 H672'),edge('M527 112 L672 248'),
            edge('M527 248 L672 112'),edge('M527 250 H672'),
            edge('M712 112 L867 184'),edge('M712 248 L867 196'),
            edge('M330 185 H420'),
        ],[
            pair('단일 퍼셉트론: 두 입력을 하나의 계산 단위로 전달','Single perceptron: two inputs feed one computational unit'),
            pair('다층 신경망: 입력층 → 은닉층 → 출력층','Multilayer network: input layer → hidden layer → output layer'),
            pair('각 층의 출력을 다음 층의 입력으로 전달','Each layer’s outputs become inputs to the next layer'),
        ],pair('입력·가중치 계산 단위를 층으로 연결한 구조','Layers connect units that process weighted inputs'), labels=[
            label(150,40,pair('단일 퍼셉트론','Single perceptron')),
            label(690,40,pair('다층 신경망','Multilayer network')),
            label(60,305,pair('입력','Inputs')),label(240,305,pair('출력','Output')),
            label(510,305,pair('입력층','Input layer')),label(695,305,pair('은닉층','Hidden layer')),
            label(890,305,pair('출력층','Output layer')),
        ], dots=[(60,110,17),(60,250,17),(240,190,20),(510,110,17),(510,250,17),
                  (695,110,20),(695,250,20),(890,190,20)]),
    ]),
    'deep-learning': resource('I07', [7],
        'AI⊃ML⊃DL 포함 관계를 편집형 중첩 도식으로 유지. 뇌 유사성 대신 데이터 학습·여러 층 표현 학습으로 정의 교정. I09의 미학습 손실·함수·RNN 오기 자료는 대안에서 제외.', [
        dict(kind='resource-sets',levels=[
            dict(title=pair('인공지능','Artificial intelligence'),body=pair('인간의 지능과 관련된 과제를 기계로 수행하는 연구 분야','A field that studies machines performing tasks associated with human intelligence')),
            dict(title=pair('머신러닝','Machine learning'),body=pair('데이터에서 판단 기준을 얻는 접근','An approach that learns decision criteria from data')),
            dict(title=pair('딥러닝','Deep learning'),body=pair('여러 층의 신경망으로 과제에 필요한 표현을 학습','Learning useful representations with multiple neural network layers')),
        ],caption=pair('AI ⊃ 머신러닝 ⊃ 딥러닝 · 딥러닝도 데이터로 학습하는 접근에 포함',
                       'AI ⊃ Machine learning ⊃ Deep learning · Deep learning is one approach to learning from data')),
    ]),
    'transformer': resource('I10-flow', [10],
        '토큰·임베딩·어텐션·표현 변환 구도를 유지. 순서 정보와 층 반복을 보완하고 FFN을 역할로 풀어 표기. 원본 수식과 토큰 생성 반복은 넣지 않음.', [
        diagram((1020,290),pair('토큰 표현과 어텐션을 연결한 Transformer의 주요 처리 단계','Main Transformer stages connect token representations and attention'),[
            box((5,90,120,80),pair('토큰','Tokens')),
            box((170,90,200,80),pair('임베딩','Embeddings'),pair('순서 정보 함께','With position info')),
            box((420,90,170,80),pair('어텐션','Attention'),pair('관련 정보 반영','Mix related info')),
            box((635,90,180,80),pair('표현 변환','Transform'),pair('각 위치별 처리','At each position')),
            box((860,90,155,80),pair('출력 표현','Output'),pair('문맥 반영','Contextual')),
        ],[edge('M125 130 H165'),edge('M370 130 H415'),edge('M590 130 H630'),edge('M815 130 H855'),
           edge('M420 185 V205 H815 V185',arrow=False)], [
            pair('입력 토큰을 임베딩으로 표현하고 순서 정보 전달','Represent input tokens as embeddings and supply position information'),
            pair('어텐션으로 관련 위치의 정보를 반영','Use attention to incorporate information from related positions'),
            pair('각 위치의 표현을 변환하며 여러 층에서 반복','Transform each position’s representation across multiple layers'),
            pair('문맥을 반영한 출력 표현 구성','Produce representations that incorporate context'),
        ],pair('어텐션 중심의 주요 처리 단계 · 모델의 전체 구성 요소를 생략한 개략도',
                'Main attention-based processing stages · A simplified view of the model'),
        labels=[label(617,245,pair('여러 층에서 반복','Repeat across layers'),True)]),
    ]),
    'text-generation': resource('I11-flow', [11,12],
        '중복 원본은 한 번만 사용. 다음 단어를 다음 토큰으로 교정하고 선택한 토큰을 입력에 추가하는 되돌림 명시. 확률 수식·최댓값 고정 선택 설명 제외.', [
        diagram((1040,310),pair('다음 토큰을 선택해 입력에 붙이는 문장 생성 반복','Text generation repeatedly selects a token and appends it to the context'),[
            box((10,75,220,90),pair('현재 토큰열','Current tokens'),pair('토큰화한 입력·생성 결과','Tokenized input + output')),
            box((275,75,220,90),pair('LLM 계산','LLM computation'),pair('다음 토큰의 가능성','Next-token probabilities')),
            box((540,75,220,90),pair('토큰 선택','Select a token'),pair('선택 방식에 따른 결과','Selection method')),
            box((805,75,220,90),pair('입력 뒤에 추가','Append to context'),pair('선택한 토큰 연결','Add the selected token')),
        ],[edge('M230 120 H270'),edge('M495 120 H535'),edge('M760 120 H800'),edge('M915 165 V240 H120 V170')],[
            pair('문자 입력을 토큰화해 현재 토큰열 구성','Tokenize the text input to form the current context'),
            pair('LLM이 다음 토큰의 가능성을 계산','The LLM computes next-token probabilities'),
            pair('선택한 토큰을 입력 뒤에 추가','Append the selected token to the context'),
            pair('변경된 토큰열로 다시 계산하며 종료 조건까지 반복','Compute again with the extended context until a stopping condition'),
        ],pair('선택 방식에 따라 달라질 수 있는 출력 · 일반적인 생성 요청 동안 동일한 모델 가중치 사용',
                'Outputs can vary with the selection method · Ordinary generation uses the same model weights'),
        labels=[label(520,280,pair('종료 조건까지 생성 토큰을 포함한 입력으로 재계산','Repeat with the appended token until a stopping condition'),True)]),
    ]),
    'development-prompt': resource('T17', [17],
        '요소·설명·예시 3열을 재사용. 서비스 기획 예시를 문자열 제목 검사로 통일. 역할 지정은 선택임을 표시하고 반환 형식·공백·길이 조건 명시.', [
        table([pair('요소','Element'),pair('역할','Purpose'),pair('제목 검사 요청의 예','Example title-validation request')],[
            [pair('목표','Goal'),pair('만들 동작 지정','State the requested behavior'),pair('제목 검사 함수 작성','Write a title-validation function')],
            [pair('역할 · 선택','Role · Optional'),pair('응답 관점 지정','Set a response perspective'),pair('코드 검토자의 관점','A code reviewer’s perspective')],
            [pair('맥락','Context'),pair('입력과 사용 범위','Define input and scope'),pair('게시글 제목 · 문자열 입력','A post title supplied as a string')],
            [pair('형식','Format'),pair('반환할 결과 지정','Specify the result'),pair('유효 여부를 true / false로 반환','Return true or false for validity')],
            [pair('제약조건','Constraints'),pair('판단 기준 구체화','Make the decision rule explicit'),pair('앞뒤 공백 제거 후 1~20글자 허용','Trim outer whitespace, then allow 1–20 characters')],
        ]),
    ]),
    'few-shot-prompting': resource('T19', [19],
        '원본 비교표의 예시 유무 구도 재사용. 두 조건의 과제와 요청을 동일하게 유지하고 제목 입출력 예시만 추가. 높은 정확도 보장 표현 제거.', [
        note('공통 요청: 문자열 제목의 앞뒤 공백 제거 후 길이가 1~20글자이면 true, 그 외에는 false를 반환하는 함수 작성',
             'Shared request: write a function that trims a string title and returns true for 1–20 characters, otherwise false'),
        table([pair('비교 항목','Criterion'),pair('제로샷','Zero-shot'),pair('퓨샷','Few-shot')],[
            [pair('과제와 조건','Task and constraints'),pair('위의 공통 요청','The shared request above'),pair('위의 공통 요청','The shared request above')],
            [pair('입력·기대 출력 예시','Input / expected output'),pair('추가 예시 없음','No additional examples'),pair('" 공지 " → true\n공백 3개 → false','" Notice " → true\nThree spaces → false')],
            [pair('모델에 전달하는 정보','Information supplied'),pair('조건을 설명한 지시','An instruction stating the constraints'),pair('같은 지시 + 소수의 입출력 예시','The same instruction + a few input/output examples')],
            [pair('요청 시 가중치 학습','Weight training at request time'),pair('추가 학습 없음','No additional training'),pair('추가 학습 없음','No additional training')],
        ]),
    ]),
    'code-revision': resource('I22 T22-steps', [22],
        '원본 단계표의 순서에 맞춰 결과 확인부터 시작. 요약 길이 사례를 공백 제목의 실제값·기대값 및 수정 후 재실행으로 교체. 사람이 실행·결과 전달하는 범위 유지.', [
        flow([
            (pair('실행 결과 확인','Observe the result'),pair('입력: 공백 3개\n실제 true · 기대 false','Input: three spaces\nActual true · Expected false')),
            (pair('원인 검토','Inspect the cause'),pair('공백 처리 누락\n길이만 비교한 조건','Missing whitespace trimming\nOnly length was checked')),
            (pair('수정 요청','Request a revision'),pair('입력·실제값·기대값 전달\n앞뒤 공백 처리 명시','Provide input, actual and expected results\nSpecify trimming')),
            (pair('수정 후 재실행','Run the revision'),pair('공백 제목 → false\n정상 제목 → true','Whitespace-only title → false\nValid title → true')),
        ],pair('개발자가 코드를 실행하고 결과를 대화에 전달하는 수정 사례',
                'An example where the developer executes the code and reports results in the conversation'),
        repeat=pair('기대 결과와 다르면 관찰한 결과를 바탕으로 다시 수정','If results still differ, revise again using the observed results')),
    ]),
    'project-instructions': resource('T21', [21],
        '시스템 프롬프트 표의 반복 규칙 구성만 참고. 실제 프로젝트 지침 예시로 새로 구체화하고 시스템 메시지 우선순위와 실행 권한을 동일시하지 않음.', [
        note('AGENTS.md / CLAUDE.md에 기록할 공통 지침의 예','Example shared instructions for AGENTS.md / CLAUDE.md'),
        table([pair('항목','Item'),pair('게시글 프로젝트의 반복 규칙','Recurring rule for the post project')],[
            [pair('작업 범위','Scope'),pair('게시글 기능과 관련된 파일의 변경','Changes to files related to the post feature')],
            [pair('목표','Objective'),pair('앞뒤 공백 제거 후 1~20글자라는 제목 조건 유지','Preserve the title rule: 1–20 characters after trimming')],
            [pair('작성 규칙','Conventions'),pair('기존 파일 구조와 이름 규칙 유지','Follow the existing file structure and naming conventions')],
            [pair('보고 형식','Report format'),pair('변경 파일 · 확인 결과 · 남은 문제','Changed files, verification results, and remaining issues')],
            [pair('제약조건','Constraints'),pair('관련 없는 기능의 변경 제외','Keep unrelated features outside the change')],
        ]),note('파일의 적용 범위는 도구·위치에 따라 결정 · 실제 실행 권한은 실행 환경에서 관리',
                'Instruction scope depends on the tool and file location · The execution environment controls actual permissions'),
    ]),
    'implementation-plan': resource('T24', [24],
        'PRD에서 작업 순서를 만드는 발상 참고. TaskMaster 제품·CLI 대신 현재 게시글 사례의 선후 의존 관계로 구체화. MCP 오기와 제품 설정은 옮기지 않음.', [
        flow([
            (pair('제목 검사 함수','Title validation'),pair('공백 처리·허용 길이\n입력의 유효 여부','Whitespace handling and length limits\nInput validity')),
            (pair('서버의 입력·저장 처리','Server validation and storage'),pair('제목 검사 결과 확인\n허용한 제목만 저장','Use the validation result\nStore only accepted titles')),
            (pair('화면의 결과 표시','Display the result'),pair('서버 응답 확인\n성공·실패 안내','Read the server response\nShow success or failure')),
        ],pair('앞 작업의 결과를 사용하는 순서에 따라 구현 계획 구성',
                'Order the implementation around the results needed by subsequent work')),
    ]),
    'task-decomposition': resource('T24', [24],
        '작업 목록을 생성·관리한다는 발상을 현재 사례의 입력·완료 결과·확인 방법 표로 구체화. 작업 분해 전에 병렬화나 자동 테스트를 전제하지 않음.', [
        table([pair('작업','Task'),pair('입력·전제','Input / prerequisite'),pair('완료 결과','Deliverable'),pair('확인 방법','Verification')],[
            [pair('제목 검사','Validate title'),pair('문자열 제목\n공백·길이 조건','String title\nWhitespace and length rules'),pair('유효 여부 반환','Return validity'),pair('빈 값·공백·정상 제목의 결과 비교','Compare empty, whitespace-only, and valid titles')],
            [pair('서버 처리','Server handling'),pair('제목 검사 결과\n저장 요청','Validation result\nSave request'),pair('허용한 제목 저장\n성공·실패 응답','Store accepted titles\nReturn success or failure'),pair('잘못된 입력의 저장 여부와 실패 응답 확인','Check rejected input is not saved and failures are reported')],
            [pair('화면 표시','Display feedback'),pair('사용자 입력\n서버 응답','User input\nServer response'),pair('성공·실패 안내','Success or failure feedback'),pair('응답과 화면 표시의 일치 확인','Compare the response with the displayed feedback')],
        ]),
    ]),
    'implementation-verification-loop': resource('I22 T22-steps', [22],
        '4.9의 반복 구도를 에이전트 구현·테스트·브라우저 검증으로 확장. 남은 작업 진행·실패 수정 후 재검증·전체 완료의 분기를 구분. 아직 미학습인 Hooks·하네스는 넣지 않음.', [
        diagram((1040,380),pair('구현 후 검증 결과에 따라 종료하거나 수정하는 반복','An implementation loop stops or revises according to verification results'),[
            box((10,70,220,90),pair('작은 작업 구현','Implement a task'),pair('명세·완료 기준 유지','Keep the agreed criteria')),
            box((285,70,220,90),pair('검증 실행','Run checks'),pair('테스트·브라우저 확인','Tests + browser checks')),
            box((560,70,200,90),pair('결과 판단','Assess results'),pair('완료 기준과 대조','Compare with criteria')),
            box((820,70,200,90),pair('완료','Complete'),pair('모든 완료 기준 충족','All criteria satisfied')),
            box((560,250,300,80),pair('실패 근거로 수정','Revise from evidence'),pair('관찰한 원인 해결','Address the observed cause')),
        ],[edge('M230 115 H280'),edge('M505 115 H555'),edge('M760 115 H815'),
           edge('M660 160 V245'),edge('M560 290 H395 V165'),edge('M660 70 V30 H120 V65')],[
            pair('명세와 완료 기준에 따라 작은 작업 구현','Implement a small task against the specification and acceptance criteria'),
            pair('자동화 테스트와 필요한 브라우저 검증 실행','Run automated tests and necessary browser checks'),
            pair('모든 완료 기준 충족 시 종료','Stop when all acceptance criteria are satisfied'),
            pair('현재 검사를 통과하고 남은 작업이 있으면 다음 작업 구현','If current checks pass and work remains, implement the next task'),
            pair('실패 시 관찰 근거로 수정하고 다시 검증','On failure, revise using the evidence and verify again'),
        ],pair('해결할 수 없는 원인이나 실행 제한은 근거와 함께 기록',
                'Record evidence for unresolved causes or execution limits'),labels=[
            label(790,95,pair('충족','Pass'),True),label(690,210,pair('실패','Fail'),True),
            label(390,20,pair('현재 검사 통과 · 남은 작업 진행','Checks pass · Continue remaining work'),True),
        ]),
    ]),
    'developer-judgment': resource('T14-time', [14],
        '과거/현재/미래라는 단정적 전망을 자동화 범위와 개발자의 판단 비교로 재구성. 프롬프트 디자이너로의 대체 주장을 제거하고 현재 원고의 범위·검증·통합 판단 반영.', [
        table([pair('작업 범위','Work scope'),pair('AI가 수행하는 작업','Work performed by AI'),pair('개발자가 판단할 내용','Developer judgment')],[
            [pair('코드 작성','Code writing'),pair('요청 조건에 따른 코드 제안','Propose code from the stated requirements'),pair('동작·제약이 충분히 명확한지 확인','Determine whether behavior and constraints are clear enough')],
            [pair('구현·검증','Implementation and checks'),pair('파일 수정과 검사 실행','Edit files and execute checks'),pair('변경 범위와 실제 검증 근거 검토','Review the scope of changes and actual verification evidence')],
            [pair('병렬·지속 작업','Parallel and persistent work'),pair('분담 작업과 후속 단계 진행','Carry out assigned tasks and subsequent steps'),pair('작업 경계·통합 비용·실행 한도 결정','Decide task boundaries, integration costs, and execution limits')],
            [pair('결과 수용','Accept the result'),pair('변경사항과 실행 결과 보고','Report changes and execution results'),pair('명세·코드 차이·실제 동작을 대조해 수용 판단','Accept based on the specification, code diff, and actual behavior')],
        ]),
    ]),
}

assert len(RESOURCES)==16
