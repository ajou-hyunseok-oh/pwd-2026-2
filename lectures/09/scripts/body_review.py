"""Export completed slide prose beside its approved paragraph and learning scope."""
import argparse
import json
from pathlib import Path

from lesson import SLIDES
from paragraph_outline import document
from slide_body import BODY

REVIEWS = [
    '1장: 지능 과제→평가→공동 연구→기호·수치 접근의 관계 유지. 퍼셉트론에는 학습 최적화 수식 대신 입력·가중합·임곗값의 역할만 설명.',
    '2장: 모델·학습·추론 뒤에 학습 신호의 유형을 배치. 학습 방식과 신경망 구조를 구분하고 역전파의 영향 계산과 실제 가중치 갱신을 분리. AlexNet·AlphaGo는 앞서 배운 구조·학습의 사례로 설명.',
    '3장: 토큰 ID→벡터 표현→문맥 관련도→Transformer 순서 유지. 학습 병렬 계산과 순차 생성, 현재 문맥과 저장 기록, 유창함과 사실 근거를 각각 구분. 임의 벡터·연결선·생성 예시는 측정 결과로 표시하지 않음.',
    '4장: 코드 제안에서 개발자가 수락·적용·실행하는 흐름을 설명. 지시 튜닝·선호 학습의 가중치 변경과 요청 시 퓨샷 예시 제공을 구분. 제목 함수는 문자열·trim·길이 1~20·boolean의 공통 조건 유지.',
    '5장: 도구 요청→외부 실행→권한→에이전트 반복의 선수 관계 유지. 일반 모델 추론과 추론 모델을 구분하고 화면 해석과 실제 조작을 별도 설명. MCP에는 호스트 내부 클라이언트와 서버의 연결만 설명.',
    '6장: 프로젝트 정보→정보 선별→공통 지침→재사용 절차→현재 기록→문맥 요약의 역할 구분. 코드의 현재 상태와 검증 근거를 다시 읽는 관계를 설명하며 스킬을 재학습이나 MCP로 설명하지 않음.',
    '7장: 동작 명세→관찰 가능한 완료 기준→계획·작업 분해→함수·브라우저 검사→반복·Hooks·하네스→리뷰의 순서 유지. 개별 함수 검사와 저장·화면의 통합 검증을 구분. 실제 서비스가 없는 브라우저 발췌를 실행 완료로 주장하지 않음.',
    '8장: 독립 범위와 연결 계약을 먼저 설명한 뒤 위임·협업·이력·작업 폴더·통합을 도입. 병렬화·목표 유지·중단 재개·예약 시작을 구분. 완료 보고보다 코드 차이와 실제 동작을 근거로 수용하도록 설명.',
]


def outputs():
    root=Path(__file__).resolve().parents[1]
    slides={s['id']:(n,s) for n,s in enumerate(SLIDES,2)}
    rows=[]; seen=set()
    lines=['9주차 · 완성 본문과 문단 대응','',
           '본문 76장 · 한영 정의와 글머리표 · 기존 자료 16장 + 새 자료 60장.',
           '확정 제목·순서·문단의 맥락을 유지하고 설명과 사례의 배치를 조정.',
           '출처: slide-references.html · 화면 검토: body-layout-review.json','',
           '챕터별 내용·선수 관계 검토','',*REVIEWS,'']
    for chapter in document()['chapters']:
        for item in chapter['slides']:
            ident=item['id']; number,slide=slides[ident]
            assert all(req.startswith('prior-') or req in seen for req in item['requires']),ident
            seen.add(ident)
            groups=BODY[ident]['explanation']['items']
            assert groups and all(g['details'] for g in groups)
            assert any(b['kind']=='concepts' for col in slide['columns'] for b in col)
            assert any(b['kind']!='concepts' for col in slide['columns'] for b in col)
            assert not slide.get('sources') and not slide.get('note')
            row=dict(slide_number=number,outline_number=item['outline_number'],id=ident,
                     title=item['title'],requires=item['requires'],
                     approved_paragraph_ko=item['paragraph_ko'],body_groups=groups,
                     composition=BODY[ident]['layout'],
                     resource_blocks=[[b['kind'] for b in col if b['kind']!='concepts'] for col in slide['columns']])
            rows.append(row)
            lines += [f'{number}페이지 · {item["outline_number"]} · {item["title"][0]}',
                      '확정 문단: '+item['paragraph_ko'],'','발표용 본문:']
            for group in groups:
                lines += [group['term'][0],*['  • '+detail[0] for detail in group['details']]]
            lines += ['','자료 배치: '+row['composition'],'']
    assert len(rows)==len(BODY)==76
    data=dict(stage='completed-bilingual-bodies',slide_count=85,content_count=76,
              languages=['ko','en'],references='slide-references.html',review='body-layout-review.json',
              chapter_review=REVIEWS,slides=rows)
    return {root/'materials/slide-bodies.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n',
            root/'materials/week-09-body.ko.txt':'\n'.join(lines)+'\n'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for path,content in outputs().items():
        if args.check: assert path.read_text()==content,f'Stale {path}'
        else: path.write_text(content)
    print('Week 9 bodies: 76 bilingual explanations with resources and approved prerequisites.')
