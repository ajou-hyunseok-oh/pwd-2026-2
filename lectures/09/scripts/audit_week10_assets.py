"""Review Week 10 PDF resources against the 76 Week 9 slide paragraphs.

Reuses the Week 8 audit convention: original assets, provenance, and a separate
reuse plan. --extract needs PyMuPDF; report generation and --check use stdlib.
This does not create teaching assets or change the presentation.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'materials/week10-asset-audit'


def asset(ident, pages, name, kind, decision, note, **selector):
    return dict(id=ident, pages=pages, name=name, kind=kind, decision=decision,
                reuse_note=note, selector=selector)


ASSETS = [
    asset('I02', [2], 'LLM·서비스 로고 합성 이미지', 'image', '제외',
          '개념 관계가 없는 장식 이미지. 1.1에서 아직 배우지 않은 LLM·서비스 이름을 먼저 보여주지 않음.', xref=24),
    asset('I03', [3], 'AI의 세 차례 봄을 나타낸 시간선', 'image', '수정',
          '2.1에서 초기 기대와 위축의 반복을 설명하는 바탕. 측정 그래프가 아닌 개략도임을 명시. 1990년대 머신러닝 등장 표기는 채택하지 않고, 아직 배우지 않은 딥러닝·생성형 AI 구간은 가림 또는 생략. 단순 잘라내기만으로 역사 교정이 끝나지는 않음.', xref=31),
    asset('I04-poster', [4], '이미테이션 게임 영화 포스터', 'image', '제외',
          '인물 소개 장식으로는 쓸 수 있지만 튜링 테스트의 참여자·관찰 방식 이해에는 기여가 작음.', xref=39),
    asset('I04-test', [4], '문자 대화로 사람과 기계를 판별하는 그림', 'image', '수정',
          '1.2에서 질문자와 두 응답자의 관계 설명. 그림의 판별 실패=지능 있음이라는 단정은 행동 평가의 한 사례로 교정. 한글이 이미지에 포함되어 EN 라벨 대안 필요. 하단의 기존 출처 표시는 보존.', xref=40),
    asset('I05-unit', [5], '생물학적 뉴런과 퍼셉트론', 'image', '수정',
          '1.5에서 오른쪽 입력→가중치→합산→활성 함수의 흐름을 발췌. 이 수업의 단일 퍼셉트론은 임곗값과 비교해 출력함을 설명. x0·w0 등의 수식과 생물학 용어를 모두 선수 지식으로 요구하지 않음. 생물학적 뉴런과 동일하다는 설명은 피함.', xref=48),
    asset('I05-boundary', [5], 'OR·XOR 분류 경계 비교', 'image', '보조 후보',
          '1.5에서 단일 직선으로 나눌 수 있는 점 배치와 없는 배치의 대비가 필요할 때만 사용. OR/XOR 이름을 이미 배웠다고 가정하지 않으며 오른쪽 곡선을 퍼셉트론의 출력 경계로 설명하지 않음. 주자료 I05-unit을 우선.', xref=49),
    asset('I06', [6], '전문가 시스템의 지식·추론 흐름', 'image', '재사용',
          '1.6의 주자료. 사용자→인터페이스→추론 엔진↔지식 베이스→결과→사용자 연결로 구성 요소의 역할 설명. 원본 화살표 보존. 현대 LLM 에이전트 반복을 설명하는 그림으로 전용하지 않음.', xref=57),
    asset('I07', [7], 'AI·머신러닝·딥러닝 포함 관계', 'image', '수정',
          '2.10에서 세 개념을 모두 설명한 뒤 포함 관계를 정리하는 보조 자료. 2.2에는 딥러닝이 아직 미도입이므로 배치하지 않음. 내부의 인간 뇌와 유사하다는 설명은 여러 층 신경망으로 표현을 학습한다는 정의로 정리. 512×256 원본의 작은 글씨를 크게 확대하지 않음.', xref=65),
    asset('I08-xor', [8], 'XOR 평면 변형 비유', 'image', '제외',
          '분류 표현을 바꾸는 비유이며 역전파의 오차 영향 계산을 설명하지 않음. 2.9의 역전파 그림으로 사용하지 않음. 2.8은 더 단순한 I08-network가 적합. 그림에 길벗 저작권 문구가 포함됨.', xref=74),
    asset('I08-person', [8], '제프리 힌튼 인물·약력 이미지', 'image', '제외',
          '인물 사진과 당시 나이는 현재 신경망 구조·역전파 학습 목표를 설명하지 않음.', xref=75),
    asset('I08-network', [8], '단일 퍼셉트론에서 다층 신경망으로', 'image', '재사용',
          '2.8의 주자료. 앞서 배운 계산 단위가 입력층·은닉층·출력층으로 연결됨을 보여줌. 가중치 갱신이나 역전파는 이 그림에 없으므로 2.9의 완성 자료로 간주하지 않음.', xref=76),
    asset('I09', [9], '두 은닉층과 손실 계산이 있는 신경망', 'image', '보조 후보',
          '2.10에서 여러 층을 강조해야 할 때의 대안. 원본 페이지의 RNN 구조 캡션은 그림의 전방향 연결과 맞지 않으므로 제거·교정. 784·128·64·10, relu, softmax, cross-entropy는 현재 선수 범위를 넘어 단순 층 이름으로 정리하고 손실 영역은 생략. I08-network의 재활용보다 수정량이 많음.', xref=85),
    asset('I10-flow', [10], '임베딩·Self-Attention·FFN 흐름', 'image', '수정',
          '3.5에서 이미 배운 임베딩과 어텐션을 연결하는 단순 구조도 바탕. 입력 단어를 입력 토큰으로 바꾸고 순서 정보와 층 반복을 보완. FFN은 표현 변환이라는 역할로 풀어 설명. 원본 전체 Transformer 구조도나 3.9의 토큰 생성 반복으로 소개하지 않음.', xref=92),
    asset('I10-formula', [10], 'Scaled dot-product attention 수식', 'image', '제외',
          '3.4에서 Q/K/V, 전치, 차원, softmax를 먼저 정의해야 하므로 현재 개념 중심 흐름에 맞지 않음. 수식 장식으로 배치하지 않음.', xref=93),
    asset('I11-flow', [11, 12], '입력·토큰화·LLM·문장 생성 흐름', 'image', '수정',
          '3.9의 주자료 바탕. 다음 단어를 다음 토큰으로 교정하고 선택한 토큰을 입력 뒤에 붙여 다시 계산하는 되돌림을 보완. 11·12쪽은 같은 이미지이므로 한 번만 추출. 3.2에 전체 그림을 앞당겨 배치하지 않음.', xref=101),
    asset('I11-formula', [11, 12], '조건부 확률 표기와 최빈 단어 설명', 'image', '제외',
          '현재 슬라이드에서는 기호 정의 비용이 설명 이득보다 큼. 항상 가장 가능성 높은 단어를 생성한다는 부연도 일반화하지 않음. 11·12쪽 중복은 한 번만 추출.', xref=102),
    asset('I18', [18], '문제·단계별 사고·최종 답변 3단계', 'image', '제외',
          '현재 구조에 독립 CoT 슬라이드가 없음. 5.6의 추론 모델을 단순한 단계별로 생각하라 프롬프트와 같다고 설명할 수 없고, 공개된 설명을 실제 내부 사고 기록으로 제시하지 않음.', xref=141),
    asset('I22', [22], '프롬프트 디버깅 반복', 'image', '수정',
          '4.9에서 실행 결과를 근거로 수정하는 반복의 바탕. 시작점을 결과 확인으로 정리하고 코드 실행·실제값/기대값·재실행을 명시. 원본의 ③→④→①→② 순서는 단계표 T22-steps와 대조. 7.7에서는 자동 검증과 종료 조건이 추가되어야 하므로 구조 참고만 가능.', xref=163),
    asset('T04', [4], '튜링 테스트의 역할 표', 'table', '수정',
          '1.2의 대안 주자료. 질문자·기계·인간 역할은 편집 가능한 표로 재사용. 마지막 행의 성공은 이 문자 대화 판별의 범위로 한정하고 의식·보편 지능의 증명으로 해석하지 않게 설명. I04-test와 둘 다 크게 배치하지 않음.', rect=[30,162,391,286], shape=[5,2]),
    asset('T09', [9], '딥러닝 유형·모델·응용 표', 'table', '제외',
          'CNN·RNN/LSTM·GAN을 소개하는 표. 현재 2.10에서 아직 정의하지 않은 모델 계열을 늘리므로 다층 표현 설명에는 채택하지 않음.', rect=[42,263,361,363], shape=[4,3]),
    asset('T13', [13], 'ChatGPT·Claude·Gemini 비교표', 'table', '제외',
          '작년 제품 버전과 강점 일반화가 들어 있는 비교표. 현재 76장에는 제품 순위 비교 장이 없으며 모델과 서비스의 차이를 설명하는 자료로도 부정확할 수 있음.', rect=[71,231,649,371], shape=[4,4]),
    asset('T14-time', [14], '웹 개발의 과거·현재·미래 표', 'table', '구조 참고',
          '8.10에서 자동화 범위와 개발자의 판단을 대비하는 구도만 참고. 개발자가 프롬프트 디자이너가 된다는 단정 대신 명세·검증·통합 판단을 현재 문단에 맞춰 새로 써야 하므로 직접 재사용으로 계산하지 않음.', rect=[45,81,675,195], shape=[4,3]),
    asset('T14-area', [14], '개발·디자인·운영의 변화 표', 'table', '제외',
          '영역별 전망을 나열하지만 개발자의 수용 판단 근거를 설명하지 않음. T14-time과 중복되며 현재 사례와 연결이 약함.', rect=[411,220,682,369], shape=[6,2]),
    asset('T16', [16], '프롬프트 기법 여섯 가지 표', 'table', '제외',
          'CoT·Role·System·Debug를 한 번에 나열하는 개요. 현재 단일 개념 순서와 맞지 않아 4.6에 전체 표를 넣지 않음. 해당 개념은 T17·T19·T22를 각각 활용.', rect=[60,138,660,298], shape=[6,2]),
    asset('T17', [17], 'Goal·Role·Context·Format·Constraints', 'table', '수정',
          '4.6의 주자료. 요소·설명·예시의 3열 구조를 그대로 활용하고 제목 검사 조건으로 예시 통일. 목표·입력 맥락·출력·제약을 중심으로 정리하며 Role 지정이 필수이거나 정확도를 보장한다는 인상을 주지 않음.', rect=[38,230,682,378], shape=[6,3]),
    asset('T19', [19], 'Zero-shot·Few-shot 비교표', 'table', '수정',
          '4.7의 주자료. 예시 없음/있음의 대비를 활용하되 높은 정확도 보장 표현은 교정. 같은 페이지의 원본 두 프롬프트는 일반 요약/감정 후기라는 목표도 달라 공정한 비교가 아님. 같은 제목 검사 조건에 입출력 예시만 추가하도록 교체.', rect=[381,150,697,274], shape=[5,3]),
    asset('T20', [20], '역할 지정 전후 프롬프트 비교', 'table', '제외',
          '4.6의 주자료 T17에 역할 행이 이미 있음. 전문가 역할 문구만으로 전문성이 생긴다는 인상을 줄 수 있고 별도 역할 프롬프트 장은 없으므로 제외.', rect=[91,276,629,358], shape=[3,3]),
    asset('T21', [21], '시스템 프롬프트 구성 요소 표', 'table', '구조 참고',
          '6.3에서 반복 규칙을 문서로 남긴다는 발상만 참고. 시스템 메시지와 AGENTS.md/CLAUDE.md의 적용 방식·우선순위를 동일시하지 않음. 실제 지침 파일 예시는 원본에 없어 별도 작성이 필요.', rect=[375,95,708,243], shape=[6,3]),
    asset('T22-errors', [22], '출력 오류·원인·해결 방법 표', 'table', '수정',
          '4.9의 보조 후보. 오류 관찰을 수정 요청으로 바꾸는 열 구도를 활용하되 과도한 요약·형식 오류를 제목 함수의 입력·실제값·기대값으로 바꿈. 오류 원인을 항상 프롬프트 탓으로 단정하지 않음.', rect=[352,127,708,243], shape=[5,3]),
    asset('T22-steps', [22], '결과 확인부터 개선·재시도까지의 단계표', 'table', '수정',
          '4.9에서 I22를 읽기 쉬운 편집형 순환 도식으로 옮길 때 단계 순서의 기준. 소프트웨어 사례의 실제 실행 결과와 정상 입력 재확인을 넣음. 7.7의 자동 반복에는 도구·테스트·종료 조건을 추가해야 함.', rect=[352,266,708,389], shape=[5,3]),
    asset('T24', [24], 'TaskMaster 기능·PRD·CLI 명령 이름 표', 'table', '구조 참고',
          '7.3/7.4에서 PRD→작업 생성→진행 관리라는 발상을 참고. 실제 프로젝트의 계획·작업 목록과 실행 가능한 명령 예제는 없음. MCP를 Model Control Protocol로 풀어 쓴 것은 Model Context Protocol로 교정해야 하며, 이 한 행을 5.9의 프로토콜 도식으로 간주하지 않음. 명령·저장소 주소를 현재 도구 사용법으로 복사하지 않음.', rect=[30,138,515,311], shape=[7,2]),
    asset('T25', [25], 'React 기본 처리와 React Hook Form 비교', 'table', '제외',
          '이번 이론 흐름에 필요하지 않은 라이브러리 비교. useState·setState 이름만 있고 구현 코드가 없음. 7.8의 에이전트 Hooks 설명에 React Hook Form을 연결하지 않음.', rect=[286,181,704,337], shape=[6,3]),
    asset('T26', [26], 'Tailwind CSS 기능 표', 'table', '제외',
          '스타일 라이브러리 소개로 현재 AI 개발 개념의 이해를 돕지 않음. 기존 설정 설명을 현재 버전의 실습 지침으로 전용하지 않음.', rect=[127,156,594,329], shape=[7,2]),
    asset('T27', [27], 'shadcn/ui 특징 표', 'table', '제외',
          '컴포넌트 라이브러리 소개로 현재 선수 범위에 불필요. UI 예제 코드·실행 화면이 있는 자료가 아님.', rect=[29,173,474,321], shape=[6,2]),
]


def mapping(number, status, assets, pages, plan, constraint=''):
    return dict(outline_number=number, status=status, assets=assets.split(),
                text_pages=pages, use=plan, prerequisite_or_correction=constraint)


# Status means coverage of the actual slide paragraph, not a keyword match.
SLIDE_MAP = [
    mapping('1.1','설명 활용','',[3], '원본 AI 정의를 도입 설명에 참고. 현재 문단의 정해진 규칙/다양한 표현 과제 대비는 별도 간단한 사례로 표현.', 'I02의 LLM 서비스 로고는 아직 소개하지 않음.'),
    mapping('1.2','수정 활용','I04-test T04',[4], '질문자·인간·기계와 문자 대화 관계를 설명. 그림 또는 역할 표 중 하나를 주자료로 선택.', '판별 결과를 의식·보편 지능의 증명으로 일반화하지 않음.'),
    mapping('1.3','대응 없음','',[], '다트머스 제안·연구 모임의 자료나 그림이 없음. 사건과 연구 목표를 짧게 제시하면 충분.'),
    mapping('1.4','대응 없음','',[], '사실→규칙→결론의 구체 예는 원본에 없음.', 'I06 전체는 전문가 시스템 소개보다 앞서지 않게 1.6에 배치.'),
    mapping('1.5','수정 활용','I05-unit I05-boundary',[5], '입력·가중치·합산·판단 부분을 주자료로 사용. 분류 경계 비교는 필요할 때만 보조.', 'XOR 용어·신경 생물학·역전파를 설명 없이 도입하지 않음.'),
    mapping('1.6','직접 활용','I06',[6], '장비 증상→규칙 적용→원인 후보 사례를 기존 구성도에 대응.', '원본 구조를 보존하고 지식 베이스/추론 엔진의 역할을 각각 설명.'),
    mapping('2.1','수정 활용','I03',[3], '초기 기대와 위축을 개략 시간선으로 설명.', '실측 그래프가 아님. 1990년 ML 최초 등장 인상을 교정하고 뒷 시기의 미학습 용어는 생략.'),
    mapping('2.2','설명 활용','',[7], '명시적 규칙 작성과 데이터로 기준을 얻는다는 정의 참고.', 'I07 전체 포함 관계 그림은 딥러닝 설명 뒤 2.10에 사용.'),
    mapping('2.3','대응 없음','',[], '현재 예측→평가→내부 값 조정의 반복을 보여주는 원본 도식 없음.', 'I08-network는 연결 구조이며 학습 과정 그림이 아님.'),
    mapping('2.4','대응 없음','',[], '학습된 모델과 새 메시지의 입력/출력을 구분하는 자료 없음.', '전문가 시스템의 추론 엔진을 학습된 모델의 추론과 동일시하지 않음.'),
    mapping('2.5','설명 활용','',[7], '입력·정답을 주는 지도학습 정의와 예 참고. 메시지/스팸 정답 쌍은 별도 구성 필요.'),
    mapping('2.6','설명 활용','',[7], '정답 없이 구조를 찾는 비지도학습 설명 참고. 문의 묶음의 구체 사례는 원본에 없음.'),
    mapping('2.7','설명 활용','',[7], '보상을 통한 학습 정의 참고. 행동·환경·상태·보상 연결 그림은 원본에 없음.'),
    mapping('2.8','직접 활용','I08-network',[8], '단일 계산 단위를 층으로 연결하는 구조를 설명.', 'I08-xor의 평면 변형이나 I09의 softmax/손실 표기는 추가하지 않음.'),
    mapping('2.9','설명 활용','',[8], '역전파 이름과 역사 설명만 참고. 오차 영향의 역방향 계산은 별도 표현 필요.', 'I08-xor는 역전파가 아니며, 영향 계산과 가중치 갱신은 구분.'),
    mapping('2.10','수정 활용','I07 I09 I08-network',[7,9], 'I08-network의 층을 다시 짚고 I07의 포함 관계로 정리. I09는 여러 은닉층을 강조해야 할 때만 선택.', 'I07 정의 정리. I09 RNN 캡션 교정 및 미학습 수치·손실 세부 제거. 그림 세 개를 한꺼번에 넣지 않음.'),
    mapping('2.11','대응 없음','',[], 'AlexNet의 이미지 입력·분류 결과·성과 자료는 없음. T09의 CNN 이름만으로 설명할 수 없음.'),
    mapping('2.12','대응 없음','',[], 'AlphaGo의 학습·신경망 평가·탐색 관계 자료 없음.'),
    mapping('3.1','설명 활용','',[11], '언어의 다음 표현 가능성을 다룬다는 설명만 참고. 짧은 문장과 여러 후보 예는 별도 구성.', 'I11-flow 전체에는 아직 배우지 않은 토큰화·LLM이 들어 있음.'),
    mapping('3.2','대응 없음','',[], 'I11-flow에 토큰화라는 상자는 있지만 실제 문장 분할·식별 번호 예시는 없음.', '단어=토큰이라고 가정하지 않음. 전체 생성 흐름은 3.9.'),
    mapping('3.3','대응 없음','',[], 'I10-flow의 임베딩 상자만으로 식별 번호와 수치 표현의 차이를 설명할 수 없음.'),
    mapping('3.4','설명 활용','',[10], '주변 표현의 관련도를 반영한다는 설명 참고. 지시어와 대상 관계를 보여주는 예시는 별도 필요.', 'I10-formula는 선행 선형대수·Q/K/V 정의가 없어 제외.'),
    mapping('3.5','수정 활용','I10-flow',[10], '토큰 표현→어텐션→표현 변환을 연결해 Transformer 구조를 설명.', '순서 정보·층 반복 보완. 생성 루프를 여기서 먼저 설명하지 않음.'),
    mapping('3.6','대응 없음','',[], '데이터 자체에서 입력과 예측 목표를 만드는 자료 없음.'),
    mapping('3.7','설명 활용','',[11], '대량 텍스트의 패턴을 학습한다는 설명 참고. 사전 학습 단계와 이후 활용의 구분 도식은 없음.'),
    mapping('3.8','설명 활용','',[11], 'LLM의 정의·규모 설명 참고. 모델/대화 서비스의 구분 자료는 원본에 없음.', 'T13의 제품 비교표로 BERT/GPT 계열의 학습 목표를 설명하지 않음.'),
    mapping('3.9','수정 활용','I11-flow',[11,12], '한 번 추출한 생성 흐름에 토큰 선택→입력에 추가→다시 계산을 보완.', '단어를 토큰으로 교정. 항상 최댓값 선택이라는 I11-formula 부연은 제외.'),
    mapping('3.10','대응 없음','',[], '지침·대화·문서·출력과 컨텍스트 한도를 나타낸 자료 없음.'),
    mapping('3.11','설명 활용','',[12], '그럴듯한 생성과 실제 이해/근거를 구분하는 원문 문제의식만 참고.', '제공하지 않은 문서에 대한 허위 응답 사례는 없음. 의식 유무의 단정으로 치환하지 않음.'),
    mapping('3.12','대응 없음','',[], '검색→관련 문서→질문과 함께 생성하는 RAG 도식 없음.'),
    mapping('4.1','대응 없음','',[], '코드 모델의 실제 입력·생성 코드 예시는 없음. 서비스 이름만으로 대체하지 않음.'),
    mapping('4.2','대응 없음','',[], '편집기의 코드 제안·채택 화면 또는 코드 조각 없음.'),
    mapping('4.3','대응 없음','',[], '요청·응답 학습 데이터와 가중치 추가 조정의 관계 자료 없음.'),
    mapping('4.4','대응 없음','',[], '응답 선호·평가 데이터가 모델 학습에 반영되는 자료 없음.'),
    mapping('4.5','설명 활용','',[14,17], '자연어로 작업을 요청한다는 설명 활용. 사람이 코드 반영·실행 결과 전달을 하는 실제 대화는 없음.', 'TaskMaster 자동화를 기본 대화형 지원의 수행 방식으로 소개하지 않음.'),
    mapping('4.6','수정 활용','T17',[17], '요소·설명·예시 표의 예시를 제목 검사 요청으로 통일.', '역할 지정만 강조하지 않고 입력 문자열·공백 처리·1~20글자·결과 형식을 구체화.'),
    mapping('4.7','수정 활용','T19',[19], '같은 요청에 입력/기대 출력 예시 유무만 바꾼 비교에 활용.', '원본 식당 요약/감정 후기 비교는 목표도 달라 교체. 현재 입력 추가와 가중치 학습을 구분.'),
    mapping('4.8','대응 없음','',[], '제목 검사 함수나 실행 가능한 JavaScript 구현은 원본에 없음.', '후속 제작 시 공통 함수 한 개를 만들고 4.9→5.5→7.5에 재사용.'),
    mapping('4.9','수정 활용','I22 T22-steps T22-errors',[22], '결과 확인→원인 검토→수정 요청→재실행 순서와 전후 비교 구도를 재사용.', '입력·실제 결과·기대 결과를 제시. 세 자료는 대안/보조이며 모두 배치하지 않음.'),
    mapping('5.1','대응 없음','',[], '모델의 이름·인자 요청과 외부 실행·결과 반환을 분리한 도식 없음.'),
    mapping('5.2','대응 없음','',[], '읽기·쓰기·외부 전송 권한과 실행 환경의 경계 자료 없음.'),
    mapping('5.3','대응 없음','',[], '목표·도구 행동·관찰·다음 행동/종료가 연결된 에이전트 도식 없음.', 'I06 전문가 시스템 및 I22 사람이 수행하는 프롬프트 수정과 구분.'),
    mapping('5.4','대응 없음','',[], '파일 읽기·편집·터미널 실행의 실제 개발 도구 화면/결과 없음. TaskMaster 이름 소개는 대체 자료가 아님.'),
    mapping('5.5','대응 없음','',[], '에이전트가 제목 함수를 읽고 수정·재실행한 기록이나 코드 없음.', '4.8/4.9와 같은 함수·입력·요구를 유지하고 수행 주체 차이만 보여줄 예정.'),
    mapping('5.6','대응 없음','',[], '추가 계산을 사용하는 추론 모델을 설명하는 적합한 자료 없음.', 'I18의 단계별 프롬프트를 모델 학습·추론 메커니즘과 동일시하지 않음.'),
    mapping('5.7','대응 없음','',[], '코드 설명과 오류 화면을 함께 해석하는 멀티모달 예시 없음.'),
    mapping('5.8','대응 없음','',[], '관찰→클릭/입력→바뀐 화면 확인의 사례 없음.'),
    mapping('5.9','대응 없음','',[], 'MCP 명칭 한 행은 있으나 클라이언트·서버·기능·요청/결과 구조 자료 없음.', '24쪽 Model Control Protocol 오기는 채택하지 않음.'),
    mapping('6.1','대응 없음','',[], '함수·화면·요청 처리 파일의 연결을 보여주는 프로젝트 자료 없음.'),
    mapping('6.2','대응 없음','',[], '필요한 지침·코드·도구 결과를 선별하고 시점에 맞게 제공하는 자료 없음. T17 Context 한 행은 작업 맥락 설계 사례가 아님.'),
    mapping('6.3','구조 참고','T21',[21], '반복 규칙을 정리한다는 구성만 참고. 실제 지침 파일 예시는 별도 작성 필요.', '시스템 프롬프트와 프로젝트 파일의 적용·권한을 동일시하지 않음.'),
    mapping('6.4','대응 없음','',[], 'SKILL.md·참고 자료·스크립트의 묶음과 필요 시 사용 흐름 없음.'),
    mapping('6.5','대응 없음','',[], '변경 파일·실행 명령·결과·남은 문제를 보존하는 작업 기록 없음.'),
    mapping('6.6','대응 없음','',[], '긴 이력→핵심 요약→원문 재조회 관계 자료 없음.'),
    mapping('6.7','대응 없음','',[], '현재 게시글 사례의 지침·코드·절차·진행 기록을 연결한 자료 없음.'),
    mapping('7.1','설명 활용','',[24], 'PRD를 작업 생성의 입력으로 사용한다는 설명 참고. 제목·저장·실패 동작의 실제 명세는 없음.'),
    mapping('7.2','대응 없음','',[], '입력별 관찰 가능한 완료 기준이나 검증 증거 자료 없음.'),
    mapping('7.3','구조 참고','T24',[24], 'PRD에서 작업 순서를 만드는 발상 참고. 검사 함수→서버 저장→화면 표시의 계획은 별도 작성.', '특정 TaskMaster CLI 명령·현재 지원 상태를 그대로 강의하지 않음.'),
    mapping('7.4','구조 참고','T24',[24], '작업 목록으로 분해하는 발상 참고. 각 작업의 입력·결과·확인 방법을 현재 사례로 구체화해야 함.', '원본에 분해된 실제 작업 목록·의존성 도식은 없음.'),
    mapping('7.5','대응 없음','',[], '제목 경계값의 기대/실제 비교 코드나 실행 결과 없음.'),
    mapping('7.6','대응 없음','',[], '게시글 입력·등록·성공/실패 화면 또는 브라우저 자동 검증 코드 없음.'),
    mapping('7.7','구조 참고','I22 T22-steps',[22], '4.9에서 쓴 반복 구도를 다시 활용하는 출발점. 자동 테스트·브라우저 검증·종료 조건을 새로 연결해야 함.', '사람의 프롬프트 재요청을 에이전트 자동 검증과 동일시하지 않음.'),
    mapping('7.8','대응 없음','',[], '도구 실행 사건과 Hook 동작의 연결 자료 없음. React Hook Form 표는 무관.'),
    mapping('7.9','대응 없음','',[], '모델·도구·환경·진행 상태·검사·실행 한도의 전체 실행 구조 자료 없음.'),
    mapping('7.10','대응 없음','',[], '코드 diff와 명세·검사 결과를 대조하는 리뷰 자료 없음.'),
    mapping('7.11','대응 없음','',[], '현재 게시글 기능의 명세부터 최종 검증까지 연결한 실제 기록 없음.'),
    mapping('8.1','대응 없음','',[], '작업별 변경 범위와 요청/응답 계약을 분리한 자료 없음.'),
    mapping('8.2','대응 없음','',[], '위임 목표·별도 맥락·결과 반환 구조 없음.'),
    mapping('8.3','대응 없음','',[], '여러 에이전트의 역할·진행 상태·조정 관계 자료 없음.'),
    mapping('8.4','대응 없음','',[], '같은 커밋에서 나뉘는 브랜치와 변경 이력 자료 없음.'),
    mapping('8.5','대응 없음','',[], '하나의 저장소·별도 작업 디렉터리·브랜치 대응 도식/명령 없음.'),
    mapping('8.6','대응 없음','',[], '개별 변경→통합→충돌 해결→통합 검증 자료 없음.'),
    mapping('8.7','대응 없음','',[], '목표·완료 근거·허용 범위·예산/중단 조건을 유지하는 자료 없음.'),
    mapping('8.8','대응 없음','',[], '기록 복구→현재 파일/환경 확인→남은 작업 선택의 재개 자료 없음.'),
    mapping('8.9','대응 없음','',[], '정해진 시점의 시작 조건과 결과 보고를 보여주는 예약 실행 자료 없음.'),
    mapping('8.10','구조 참고','T14-time',[14], '자동화 범위가 넓어져도 개발자의 명세·검증·통합 판단이 필요하다는 대비 구도 참고.', '원본의 개발자 역할 예측은 현재 문단에 맞춰 전면 정리해야 함.'),
]

PAGE_NOTES = {
    1: '2025학년도 10주차 표지. 현재 2026학년도 9주차 표지로 재사용하지 않음.',
    2: '서비스 로고 합성 그림은 장식이라 제외.',
    3: 'AI 정의와 봄·겨울 시간선. 시기·용어 및 개략 그래프라는 범위 조정 후 2.1에 활용.',
    4: '튜링 테스트 관계 그림과 역할 표 후보. 영화 포스터 제외. 판별 결과의 의미 교정.',
    5: '퍼셉트론 입력·가중치·판단 그림 우선. OR/XOR 분류 경계는 보조 후보.',
    6: '전문가 시스템 구조도 직접 활용 우선.',
    7: '학습 방식 정의는 설명 참고. 포함 관계 그림은 2.10으로 이동.',
    8: '단일/다층 연결 그림 직접 활용. 인물 사진·XOR 평면 변형은 제외. 역전파 과정 그림은 없음.',
    9: '신경망 그림과 유형 표. RNN 캡션 오류·미도입 손실 용어를 교정해야 하며 주자료로는 8쪽 우선.',
    10: 'Transformer 흐름 골격 활용. 어텐션 수식 제외.',
    11: 'LLM 생성 흐름 활용. 다음 토큰과 반복 경로 보완. 확률 수식은 제외.',
    12: '11쪽 그림 두 개의 반복. 별도 이미지 두 개로 다시 세지 않음. 언어 유창성과 근거의 구분만 참고.',
    13: '작년 AI 서비스 비교표. 현재 제품 안내나 개념 도식으로 채택하지 않음.',
    14: '개발 변화 표 두 개. 자동화와 개발자의 판단 대비 구도만 참고.',
    15: 'Prompt Thinking 챕터 표지. 별도 애셋 없음.',
    16: '프롬프트 기법 목록 표. 현재 개념 순서에 맞게 각 주제의 개별 원본을 선택.',
    17: '프롬프트 구성 요소·예시 표. 4.6의 우선 재사용 자료.',
    18: 'CoT 사과 나누기 프롬프트와 3단계 그림. 추론 모델의 작동 증거가 아니므로 제외.',
    19: '제로샷/퓨샷 비교표와 프롬프트 예. 과제 조건을 같게 고쳐 4.7에 활용.',
    20: '역할 프롬프트 전후 비교표. 4.6의 요소 표와 중복되므로 제외.',
    21: '시스템 프롬프트 표·System/User/AI 예시. 반복 규칙의 발상만 참고; 프로젝트 지침 파일 예시는 없음.',
    22: '프롬프트 수정 루프·오류 표·단계 표·Before/After 요청. 4.9에 공통 코드 사례로 바꾸어 활용.',
    23: '과제 연계 라이브러리 챕터 표지. 별도 애셋 없음.',
    24: 'TaskMaster 기능 표와 명령 이름. PRD/작업 분해 설명만 참고. MCP 풀네임 오류. 실행 코드 블록 없음.',
    25: 'React Hook Form 비교표. API 이름만 있고 구현 코드 없음. 현재 AI 흐름에서는 제외.',
    26: 'Tailwind CSS 표. 현재 강의의 개념 설명 범위 밖.',
    27: 'shadcn/ui 표. 현재 강의의 개념 설명 범위 밖.',
    28: '작년 과제 평가·제출 기한. 현재 본문 사례로 복사하지 않음.',
    29: 'Q&A. 별도 내용 애셋 없음.',
}

PRIORITIES = [
    '1순위: I06→1.6, I08-network→2.8. 구조가 현재 문단과 잘 맞아 가장 적은 준비로 활용 가능.',
    '2순위: I04-test 또는 T04→1.2, I05-unit→1.5. 평가 의미와 수식 라벨만 현재 범위에 맞게 정리.',
    '3순위: I10-flow→3.5, I11-flow→3.9. 기존 상자·화살표 구도를 사용하고 토큰·순서 정보·생성 반복을 보완.',
    '4순위: T17→4.6, T19→4.7, I22/T22-steps→4.9. 예시를 제목 검사로 통일해 이후 에이전트·테스트 사례까지 연결.',
    '선택: I03→2.1, I07→2.10. 오류 교정·미학습 용어 정리·번역 비용을 고려해 단순 표/도식과 비교.',
    '후순위: I09·T21·T24·T14-time. 수정량 또는 내용 추가가 커서 준비 완료 자료로 계산하지 않음.',
]

GAPS = [
    '1~2장: 사실/규칙/결론, 학습과 추론, 학습 방식의 입력·정답·보상, 역전파, AlexNet·AlphaGo 사례. 개념 관계는 간단한 편집형 도식으로 충분하며 모든 장에 외부 이미지는 필요 없음.',
    '3장: 토큰 분할·임베딩·문맥 관련도, 자기지도 목표, 컨텍스트 범위·환각·검색 증강. 같은 짧은 문장 사례를 단계적으로 확장하면 준비를 줄일 수 있음.',
    '4~7장 공통 코드: 문자열 제목의 앞뒤 공백 제거 후 1~20글자 허용. 함수 한 개와 고정 입력 집합을 생성→사람의 수정→에이전트 수정→자동 테스트에 반복 사용. 원본에 이 코드는 없으며 이번 조사에서 새로 작성하지 않음.',
    '5~7장 실행 흐름: 도구 요청/실행/결과, 권한, 작업 반복, 프로젝트 지침·스킬·기록, 검증·Hooks·하네스. 원본에 실제 구조가 없으므로 같은 게시글 프로젝트의 파일·실행 기록에서 후속 준비.',
    '8장: 작업 분리·위임·팀·브랜치·worktree·통합, 목표 유지·재개·예약 시작. 원본 자료가 없어 새 자료가 필요한 영역. 동일한 작업/상태 표시를 단계적으로 확장할 수 있음.',
]


def source_pdf():
    paths = list((ROOT / 'materials').glob('[[]PWD Week10]*.pdf'))
    assert len(paths) == 1
    return paths[0]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract():
    import pymupdf
    folder = OUT / 'source-assets'
    folder.mkdir(parents=True, exist_ok=True)
    pdf = source_pdf()
    doc = pymupdf.open(pdf)
    assert len(doc) == 29 and list(doc[0].rect) == [0,0,720,405]
    manifest = []
    for item in ASSETS:
        page = doc[item['pages'][0]-1]
        selector = item['selector']
        info = dict(id=item['id'], pages=item['pages'], files=[])
        stem = f'p{item["pages"][0]:02}-{item["id"].lower()}'
        if item['kind'] == 'image':
            xref = selector['xref']
            img = next(row for row in page.get_images(full=True) if row[0] == xref)
            original = doc.extract_image(xref)
            if img[1]:
                pix = pymupdf.Pixmap(pymupdf.Pixmap(doc,xref), pymupdf.Pixmap(doc,img[1]))
                path = folder / f'{stem}.png'
                pix.save(path)
            else:
                assert original['ext'] == 'jpeg'
                path = folder / f'{stem}.jpg'
                path.write_bytes(original['image'])
            info.update(xref=xref, width=img[2], height=img[3], has_alpha=bool(img[1]),
                        placements=[dict(page=n, rects=[list(r) for r in doc[n-1].get_image_rects(xref)])
                                    for n in item['pages']])
            info['files'].append(path.relative_to(OUT).as_posix())
        else:
            rect = pymupdf.Rect(selector['rect'])
            path = folder / f'{stem}-source.png'
            page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=rect,alpha=False).save(path)
            text_path = folder / f'{stem}-source.txt'
            text_path.write_text(page.get_text(clip=rect), encoding='utf-8')
            tables = page.find_tables(clip=rect, vertical_strategy='lines_strict',
                                      horizontal_strategy='lines_strict').tables
            assert len(tables) == 1, item['id']
            cells = tables[0].extract()
            assert [len(cells),len(cells[0])] == selector['shape'], item['id']
            assert all(len(row)==selector['shape'][1] for row in cells)
            cells_path = folder / f'{stem}-cells.json'
            cells_path.write_text(json.dumps(cells,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
            info.update(pdf_rect=list(rect), render_dpi=216, table_cells=cells)
            info['files'] += [p.relative_to(OUT).as_posix() for p in (path,text_path,cells_path)]
        info['sha256'] = {name:sha(OUT/name) for name in info['files']}
        manifest.append(info)
    placements = [(n+1,img[0]) for n,p in enumerate(doc) for img in p.get_images(full=True)
                  if (img[2],img[3]) != (409,55)]
    expected = [(n,a['selector']['xref']) for a in ASSETS if a['kind']=='image' for n in a['pages']]
    assert sorted(placements) == sorted(expected), 'Unreviewed embedded image'
    inventory = dict(source=pdf.name, source_sha256=sha(pdf), pdf_pages=len(doc),
                     image_placements=len(placements), excluded_decoration='409×55 학교 로고, 전 29쪽',
                     assets=manifest,
                     pages=[dict(number=n+1,text=p.get_text(),note=PAGE_NOTES[n+1]) for n,p in enumerate(doc)])
    (OUT/'extraction.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')


def report():
    paragraphs_path = ROOT/'materials/paragraph-outline.json'
    outline = json.loads(paragraphs_path.read_text())
    slides = [dict(chapter=ch['number'],**s) for ch in outline['chapters'] for s in ch['slides']]
    assert [s['outline_number'] for s in slides] == [m['outline_number'] for m in SLIDE_MAP]
    assert len(slides)==76 and len({s['id'] for s in slides})==76
    assert set(PAGE_NOTES)==set(range(1,30))
    ids = {a['id'] for a in ASSETS}
    assert len(ids)==len(ASSETS)==34
    for row in SLIDE_MAP:
        assert set(row['assets'])<=ids
        assert all(1<=n<=29 for n in row['text_pages'])
        assert row['status'] in {'직접 활용','수정 활용','구조 참고','설명 활용','대응 없음'}
    extraction = json.loads((OUT/'extraction.json').read_text())
    assert extraction['source_sha256']==sha(source_pdf())
    indexed = {a['id']:a for a in extraction['assets']}
    assert set(indexed)==ids
    for a in ASSETS:
        e=indexed[a['id']]
        assert a['pages']==e['pages']
        if a['kind']=='image':
            assert a['selector']['xref']==e['xref']
        else:
            assert a['selector']['rect']==e['pdf_rect']
        for name,digest in e['sha256'].items():
            assert sha(OUT/name)==digest, name
    rows = [dict(**s,**{k:v for k,v in m.items() if k!='outline_number'}) for s,m in zip(slides,SLIDE_MAP)]
    counts = dict(Counter(r['status'] for r in rows))
    status_order = ['직접 활용','수정 활용','구조 참고','설명 활용','대응 없음']
    data = dict(stage='existing-source-asset-audit', date='2026-11-07',
                source=extraction['source'], source_sha256=extraction['source_sha256'],
                paragraph_outline_sha256=sha(paragraphs_path), pdf_pages=29,
                scope='76개 문단을 기준으로 작성한 원본 조사·재사용 계획의 기록. 현재 반영 상태는 ../resource-placements.json 참조.',
                counts=counts, asset_counts=dict(Counter(a['kind'] for a in ASSETS)),
                image_placements=extraction['image_placements'], executable_code_blocks=0,
                visual_review='29쪽 전체 렌더와 후보 원본 이미지, 표 개별 추출본 대조. 자동 표 검출의 장식/텍스트 상자 오탐을 제외하고 16개 표 영역을 지정.',
                assets=[dict(**a,targets=[r['outline_number'] for r in rows if a['id'] in r['assets']],
                             extraction=indexed[a['id']]) for a in ASSETS],
                slides=rows, page_review=PAGE_NOTES, priorities=PRIORITIES, gaps=GAPS)
    lines = ['9주차 · PWD Week10 기존 자료 재사용 조사', '',
             '검토일: 2026-11-07 / 원본 PDF 29쪽 / 현재 본문 설계 8개 챕터·76장',
             '조사·추출 당시의 판단 기록. 현재 슬라이드 반영 상태는 ../resource-placements.ko.txt 참조.',
             f'원본: {extraction["source"]}',
             '쪽수는 PDF의 1부터 센 페이지. 1.2 등의 번호는 현재 챕터 내부 설계 번호이며 HTML 페이지 번호가 아님.', '',
             '핵심 판단',
             '- 원본은 초기 AI·신경망·LLM 흐름과 프롬프트 비교 자료에 강점. 기존 도식·표의 구도를 활용하면 1~4장 준비를 줄일 수 있음.',
             '- 학교 로고 제외 고유 이미지 18개(배치 20회), 텍스트/벡터 표 16개를 개별 추출. 11·12쪽의 동일 이미지 2개는 중복 추출하지 않음.',
             '- 실행 가능한 코드 블록은 0개. 18~22쪽의 프롬프트 예시와 24~27쪽의 명령/API 이름은 구현 코드가 아님.',
             '- 5~8장의 도구 호출·프로젝트 맥락·검증·병렬 작업·지속 실행을 설명하는 완성 도식/코드가 원본에 없음. 관련 단어가 있다는 이유만으로 대응 자료로 계산하지 않음.',
             '- 원본 추출본에는 지적한 오류와 미학습 용어가 그대로 남아 있음. 수정 활용/구조 참고는 준비 완료 또는 덱 반영을 뜻하지 않음.', '',
             '76장 대응 결과',
             *[f'- {k}: {counts.get(k,0)}장' for k in status_order],
             '직접 활용: 해당 개념에 맞는 기존 구조를 사용. 수정 활용: 기존 그림/표가 있고 라벨·범위·사례를 고쳐 사용.',
             '구조 참고: 비교/절차의 발상만 활용하고 설명 요소는 상당 부분 새로 구성. 설명 활용: 관련 원문 텍스트만 활용.',
             '대응 없음: 현재 문단의 관계·사례를 설명할 적합한 원본이 없음. 모든 장에 새 이미지가 필요하다는 뜻은 아님.',
             '직접 활용 판단은 개념 적합성 기준. 한글 라벨이 박힌 이미지의 EN 대응과 발표 크기 가독성은 화면 제작 때 별도 처리.', '',
             '챕터별 대응 요약',
             '| 챕터 | 본문 수 | 직접 | 수정 | 구조 참고 | 설명 | 대응 없음 |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    for ch in outline['chapters']:
        cr=[r for r in rows if r['chapter']==ch['number']]
        cc=Counter(r['status'] for r in cr)
        lines.append(f'| {ch["number"]}. {ch["title"][0]} | {len(cr)} | '+ ' | '.join(str(cc[k]) for k in status_order)+' |')
    lines += ['', '준비 비용을 줄이는 우선순위', *['- '+p for p in PRIORITIES], '',
              '추출·편집 원칙',
              '- 원본 이미지는 압축 원본을 보존하고 투명 마스크가 있는 1개는 알파를 결합해 PNG로 보존. 그림 안 출처·저작권 표시는 제거하지 않음.',
              '- 표는 부분 PNG, 텍스트, 셀 JSON으로 추출. PNG는 원문 대조용이며 최종 강의에는 수정·번역 가능한 공용 표/도식으로 반영.',
              '- 전체 페이지 렌더는 검토용으로만 사용. 원본 PDF 페이지 전체를 강의 슬라이드로 붙이지 않음.',
              '- 이미지 안 한글이 많은 자료는 KO/EN 공용 구조와 별도 라벨로 구성하는 편이 후속 수정 비용이 낮음. 이번 단계에서는 재작성하지 않음.',
              '- 출처 기준은 이 PDF. 그림 속 한국일보/길벗 등의 표시는 보존하지만 개별 원문 URL·이용 조건은 확인되지 않은 상태이며 임의로 기재하지 않음.',
              '- 제품 버전/지원 기능/명령은 이번에 최신 조사하지 않음. 원본을 현재 도구 매뉴얼로 사용하는 경우는 후속 시연 준비에서 공식 자료로 확인.', '',
              '원본 자료별 판단']
    for a in data['assets']:
        e=a['extraction']
        size=f' / {e["width"]}×{e["height"]}' if 'width' in e else ''
        target=', '.join(a['targets']) or '현재 본문에 배치하지 않음'
        lines += ['',f'{a["id"]} · PDF {",".join(map(str,a["pages"]))}쪽 · {a["name"]} · {a["decision"]}{size}',
                  '대응: '+target,a['reuse_note'], '원본 추출 파일: '+', '.join(e['files'])]
    lines += ['', '현재 76개 슬라이드와의 대응']
    for ch in outline['chapters']:
        lines += ['',f'{ch["number"]:02}. {ch["title"][0]}','',
                  '| 현재 장 | 타이틀 | 분류 | 원본 자료 | 이해를 돕는 활용 방법 | 선수 개념·수정 조건 |',
                  '| --- | --- | --- | --- | --- | --- |']
        for r in rows:
            if r['chapter']!=ch['number']:
                continue
            refs=', '.join(r['assets']) or '시각/코드 없음'
            if r['text_pages']:
                refs+='; PDF '+','.join(map(str,r['text_pages']))+'쪽 설명'
            lines.append(f'| {r["outline_number"]} | {r["title"][0]} | {r["status"]} | {refs} | {r["use"]} | {r["prerequisite_or_correction"]} |')
    lines += ['', 'PDF 전체 페이지 검토 기록', '']
    lines += [f'{p:02}쪽: {note}' for p,note in PAGE_NOTES.items()]
    lines += ['', '후속 자료 준비가 필요한 부분', *['- '+g for g in GAPS], '',
              '재현과 확인',
              '추출: uv run --with pymupdf --no-project python lectures/09/scripts/audit_week10_assets.py --extract',
              '보고서 생성: python3 lectures/09/scripts/audit_week10_assets.py',
              '일치 확인: python3 lectures/09/scripts/audit_week10_assets.py --check',
              'extraction.json에 PDF 해시·원본 좌표·이미지 해상도·표 셀·전체 페이지 텍스트·추출 파일 해시 보존.',
              'audit.json에 76개 문단과 원본 자료의 대응·이유·수정 조건 보존. source-assets의 미수정 추출본은 비교용.',
              '현재 문단 원고의 정의·선수 관계를 판단 기준으로 사용. 개념/최신 기술 근거는 ../paragraph-outline.json의 챕터별 출처 참조.']
    return {'audit.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n',
            'reuse-review.ko.txt':'\n'.join(lines)+'\n'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.extract:
        extract()
    for name,content in report().items():
        path=OUT/name
        if args.check:
            assert path.read_text()==content, f'Regenerate {path}'
        else:
            path.write_text(content,encoding='utf-8')
    print(f'Week 10 source audit: {len(ASSETS)} assets, {len(SLIDE_MAP)} slide mappings, 29 pages reviewed.')
