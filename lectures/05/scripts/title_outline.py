"""Approved titles for Lecture 05; origin IDs refer to the archived 61-slide map."""
import json
from pathlib import Path


def concept(ident, ko, en, subko, suben, *origins):
    return dict(id='concept-' + ident, title=(ko, en), lead=(subko, suben),
                source_slide_ids=list(origins))


CHAPTERS = [
    dict(number=2, title=('컴포넌트와 JSX', 'Components and JSX'),
         lead=('함수 컴포넌트에서 시작해 상품 목록 화면을 구성하는 방법',
               'Build a product list UI starting with function components'), concepts=[
        concept('function-component', '함수 컴포넌트', 'Function Components',
                'UI를 계산하고 반환하는 함수의 구조', 'The structure of a function that computes and returns UI', 'topic-05'),
        concept('component-lifecycle', '함수 컴포넌트 생명주기', 'Function Component Lifecycle',
                'UI 계산·DOM 반영·외부 동기화로 이어지는 함수 컴포넌트의 처리 흐름', 'How function components calculate UI, commit DOM changes, and synchronize externally', 'topic-05'),
        concept('jsx', 'JSX', 'JSX',
                'JavaScript 코드 안에서 화면 구조를 표현하는 문법', 'Syntax for expressing UI structure in JavaScript', 'topic-03'),
        concept('jsx-expressions', 'JSX의 표현식', 'Expressions in JSX',
                '중괄호 안의 JavaScript 계산 결과를 화면에 넣는 방법', 'Insert the result of a JavaScript expression using braces', 'topic-03'),
        concept('jsx-tags', 'JSX 태그 작성 규칙', 'JSX Tag Rules',
                '요소를 빠짐없이 닫고 중첩 구조를 맞추는 규칙', 'Close every element and maintain proper nesting', 'topic-04'),
        concept('jsx-attributes', 'JSX 속성', 'JSX Attributes',
                'JavaScript 방식의 속성 이름과 값으로 요소를 설정하는 방법', 'Configure elements with JavaScript attribute names and values', 'topic-04'),
        concept('fragment', 'Fragment', 'Fragment',
                '추가 DOM 요소 없이 여러 형제 요소를 묶는 구조', 'Group sibling elements without an extra DOM element', 'topic-04'),
        concept('props', 'Props', 'Props',
                '컴포넌트에 전달하는 입력 데이터', 'Input data passed to a component', 'topic-05'),
        concept('component-separation', '컴포넌트 분리', 'Separating Components',
                '역할을 명확히 나누고 재사용·조합하기 쉬운 UI 구성', 'Build UI with clear responsibilities, reuse, and composition', 'topic-06'),
        concept('component-files', '컴포넌트 파일 분리', 'Component Files',
                '분리한 컴포넌트를 export와 import로 연결하는 방법', 'Connect extracted components with export and import', 'topic-06'),
        concept('children', 'children', 'children',
                '컴포넌트 태그 사이의 내용을 내부에 배치하는 Props', 'The prop used to place content passed between component tags', 'topic-06'),
        concept('conditional-rendering', '조건부 렌더링', 'Conditional Rendering',
                '조건의 결과에 따라 표시할 UI를 선택하는 방법', 'Choose the UI to display based on a condition', 'topic-07'),
        concept('list-rendering', '목록 렌더링', 'Rendering Lists',
                'map으로 배열의 각 데이터를 반복되는 UI 요소로 표현하는 방법', 'Use map to express each array item as a repeated UI element', 'topic-07'),
        concept('list-key', '목록 항목의 key', 'Keys in Lists',
                '목록 변경 전후에 같은 항목을 식별하는 기준', 'Identify the same item across changes to a list', 'topic-07'),
        concept('static-product-ui', '상품 목록의 정적 구현', 'A Static Product UI',
                '사용자 동작을 연결하기 전에 화면 구조와 내용을 완성하는 단계', 'Complete the UI structure and content before connecting user interactions', 'topic-06', 'topic-07'),
    ]),
    dict(number=3, title=('상태 기반 화면 갱신', 'State-Based UI Updates'),
         lead=('사용자 입력에 따라 컴포넌트의 화면을 변경하는 원리',
               'How components update their UI in response to user input'), concepts=[
        concept('event-handler', '이벤트 핸들러', 'Event Handlers',
                '사용자 행동이 발생했을 때 실행할 함수를 연결하는 방법', 'Connect a function to run when a user action occurs', 'topic-08'),
        concept('state', 'State', 'State',
                'useState로 컴포넌트가 기억할 값을 관리하는 방법', 'Manage values a component remembers with useState', 'topic-08'),
        concept('render', 'Render', 'Render',
                '현재 입력과 상태를 바탕으로 다음 UI를 계산하는 단계', 'Calculate the next UI from the current inputs and state', 'topic-09'),
        concept('commit', 'Commit', 'Commit',
                '계산된 UI에 맞춰 필요한 DOM 변경을 반영하는 단계', 'Apply the DOM changes needed to match the calculated UI', 'topic-09'),
        concept('state-snapshot', '상태 스냅샷', 'State Snapshots',
                '하나의 렌더에서 고정된 상태 값을 참조하는 방식', 'Refer to the state values fixed for a particular render', 'topic-10'),
        concept('state-updater', '함수형 상태 업데이트', 'State Updater Functions',
                '이전 상태를 입력으로 다음 상태를 계산하는 방법', 'Calculate the next state from the previous state', 'topic-10'),
        concept('state-immutability', '상태의 불변성', 'State Immutability',
                '기존 값을 직접 바꾸지 않고 새 값으로 상태를 교체하는 원칙', 'Replace state with a new value while leaving the existing value unchanged', 'topic-11'),
        concept('derived-values', '파생값', 'Derived Values',
                '기존 상태에서 계산할 수 있는 값을 별도 상태 없이 구하는 방법', 'Calculate a value from existing state without storing another state variable', 'topic-12'),
        concept('controlled-inputs', '제어 입력', 'Controlled Inputs',
                '입력값과 선택 여부를 React 상태와 연결하는 방법', 'Connect input values and checkbox selection to React state', 'topic-12'),
        concept('lifting-state', '상태 끌어올리기', 'Lifting State Up',
                '여러 컴포넌트가 같은 상태를 함께 사용하도록 관리하는 방법', 'Manage shared state used by multiple components', 'topic-12'),
        concept('state-preservation', 'Props 변경과 상태 보존', 'Prop Changes and State Preservation',
                'Props가 바뀌어도 같은 컴포넌트의 상태는 초기화되지 않음', 'Changing props does not reset the state of the same component', 'topic-13'),
        concept('state-reset-key', 'key를 이용한 상태 초기화', 'Resetting State with a Key',
                'key 변경으로 컴포넌트를 새 인스턴스로 구분하는 방법', 'Use a changed key to identify a new component instance', 'topic-13'),
    ]),
    dict(number=4, title=('Hooks', 'Hooks'),
         lead=('함수 컴포넌트에서 React 기능을 사용하는 방법',
               'Use React features in function components'), concepts=[
        concept('hook-introduction', 'Hook', 'Hooks',
                '함수 컴포넌트에서 React 기능을 사용하고 관련 로직을 재사용하는 방법', 'Use React features in function components and reuse related logic', 'topic-14'),
        concept('hook-rules', 'Hook의 호출 규칙', 'Rules of Hooks',
                '렌더마다 일관된 Hook 호출 순서를 유지하기 위한 제약', 'Constraints that keep Hook calls in a consistent order across renders', 'topic-14'),
        concept('ref', 'Ref', 'Refs',
                '값을 바꿔도 렌더를 요청하지 않는 참조 저장 공간', 'Store a reference whose updates do not request a render', 'topic-15'),
        concept('effect', 'Effect', 'Effects',
                'DOM 반영 후 외부 시스템과 동기화를 시작하고 중지하는 작업', 'Start and stop synchronization with an external system after DOM commit', 'topic-16'),
        concept('effect-dependencies', 'Effect 의존성', 'Effect Dependencies',
                '의존성 배열에 넣은 값이 바뀌면 Effect를 다시 실행', 'Rerun the Effect when a value in the dependency array changes', 'topic-17'),
        concept('effect-cleanup', 'Effect 정리 함수', 'Effect Cleanup',
                '이전 Effect에서 시작한 외부 연결을 해제하는 함수', 'Release an external connection established by the previous Effect', 'topic-17'),
        concept('custom-hook', '커스텀 Hook', 'Custom Hooks',
                '반복되는 Hook 로직을 함수로 추출해 재사용하는 방법', 'Extract repeated Hook logic into a reusable function', 'topic-18'),
        concept('more-hooks', '추가로 알아둘 Hook', 'More Hooks to Learn',
                '공유 데이터·상태 관리·성능·화면 제어에 활용하는 Hook', 'Hooks for shared data, state management, performance, and UI control', 'topic-18'),
    ]),

]


def load_title_slides(body_slides):
    """Build the common ordered skeleton while retaining the cover and imports."""
    prefix = []
    for slide in body_slides:
        if prefix and 'import_html' not in slide:
            break
        prefix.append(slide)
    assert len(prefix) == 25, 'Keep the Week 5 cover and all 24 original React slides'
    archive = Path(__file__).resolve().parents[1] / 'materials/pre-concept-slide-map.json'
    original_rows = json.loads(archive.read_text())
    original = {slide['id']: (slide['number'], slide) for slide in original_rows}
    covered = set()
    slides = prefix.copy()
    for chapter in CHAPTERS:
        number = chapter['number']
        chapter_id = f'chapter-{number:02}'
        common = dict(chapter=(f'CHAPTER {number:02} · {chapter["title"][0]}',
                               f'CHAPTER {number:02} · {chapter["title"][1]}'),
                      blocks=[], topic_number=None, sources=[])
        slides.append(dict(common, id=chapter_id, kind='chapter', title=chapter['title'],
                           lead=chapter['lead'], source_slide_ids=[chapter_id],
                           source_pages=[original[chapter_id][0]]))
        for item in chapter['concepts']:
            for field in ('title', 'lead'):
                assert len(item[field]) == 2 and all(text.strip() for text in item[field])
            assert item['source_slide_ids'], item['id']
            assert all(origin in original for origin in item['source_slide_ids']), item['id']
            covered.update(item['source_slide_ids'])
            sources = list(dict.fromkeys(tuple(source) for origin in item['source_slide_ids']
                                         for source in original[origin][1].get('sources', [])))
            slides.append(dict(common, **item, kind='topic', sources=sources,
                               source_pages=[original[origin][0] for origin in item['source_slide_ids']]))
    retained_chapters = {f'CHAPTER {chapter["number"]:02}' for chapter in CHAPTERS}
    assert covered == {slide['id'] for slide in original_rows[len(prefix):]
                       if slide['kind'] == 'topic' and slide['chapter'].split(' · ')[0] in retained_chapters}, 'Retained topic coverage differs'
    slides.append(dict(
        id='appendix-react-ecosystem', kind='topic', chapter=('부록', 'Appendix'),
        title=('React 생태계', 'React Ecosystem'),
        lead=('원본 PDF 18쪽', 'Original PDF page 18'),
        source_slide_ids=[], source_pages=[], blocks=[], topic_number=None, sources=[]))
    slides.append(dict(
        id='practice-week5', kind='topic', chapter=('실습', 'Practice'),
        title=('실습 안내 · pwd-week5', 'Lab Guide · pwd-week5'),
        lead=('React로 아주 캠퍼스 푸드맵 구현 및 Vercel 배포', 'Build Ajou Campus Foodmap with React and deploy to Vercel'),
        source_slide_ids=[], source_pages=[], blocks=[], topic_number=None, sources=[]))
    assert len({slide['id'] for slide in slides}) == len(slides), 'Duplicate slide ID'
    assert [chapter['number'] for chapter in CHAPTERS] == list(range(2, 5))
    return slides


def write_title_materials(root: Path, slides):
    """Generate a readable Korean review table and the bilingual machine-readable map."""
    rows = []
    for number, slide in enumerate(slides, 1):
        if 'source_slide_ids' not in slide:
            continue
        rows.append(dict(number=number, id=slide['id'], kind=slide['kind'],
                         title=list(slide['title']), subtitle=list(slide['lead']),
                         source_slide_ids=slide['source_slide_ids'], source_pages=slide['source_pages']))
    body_count = sum(row['kind'] == 'topic' for row in rows)
    document = dict(stage='titles-only', policy='../../authoring/one-concept.md',
                    preserved_pages=[1, 25], total_slides=len(slides), concept_slides=body_count, slides=rows)
    root.joinpath('materials/title-outline.json').write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    lines = [
        '5주차 · 1개념 1슬라이드 · 확정 제목과 서브타이틀',
        f'2026-10-10 · 총 {len(slides)}장 = 보존 25 + 챕터 표지 {len(CHAPTERS)} + 본문 {body_count}',
        '1–25: 강의 표지와 04 React 원본 24장 보존',
        '새 번호는 index.html과 titles.html 공통. 기존 번호는 분할 전 61장 기준.',
        '기존 번호의 원본 기록: pre-concept-slide-map.json / 제목 검토용 화면: ../titles.html',
        '작성 원본: ../scripts/title_outline.py / 원칙: ../../authoring/one-concept.md',
        '', '| 새 번호 | 기존 번호 | 유형 | 제목 | 서브타이틀 |', '| --- | --- | --- | --- | --- |',
    ]
    for row in rows:
        kind = '챕터' if row['kind'] == 'chapter' else '본문'
        origins = ', '.join(str(number) for number in row['source_pages'])
        lines.append(f'| {row["number"]:02} | {origins} | {kind} | {row["title"][0]} | {row["subtitle"][0]} |')
    root.joinpath('materials/week-05-titles.ko.txt').write_text('\n'.join(lines) + '\n')
