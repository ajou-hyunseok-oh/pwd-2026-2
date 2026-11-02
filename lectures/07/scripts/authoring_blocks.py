"""Selected visual blocks and source correspondence for the Week 7 deck."""
from urllib.parse import quote

PDF = 'materials/' + quote('[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf')
PG = 'https://www.postgresql.org/docs/current/ddl-constraints.html'
SUPA = 'https://supabase.com/docs/guides/database/'
PAGES = {
    'database': [4], 'dbms': [4], 'database-history': [5], 'db-types': [6], 'database-trends-2025': [7], 'database-careers': [8],
    'design-purpose': [10, 11], 'design-stages': [11, 12], 'conceptual': [13],
    'entity': [13], 'attributes': [13], 'relationship': [13], 'cardinality': [13, 16],
    'logical': [14], 'primary-key': [14], 'foreign-key': [14, 17], 'physical': [15],
    'erd': [16], 'constraints': [17], 'integrity': [17], 'normalization': [18],
    'functional-dependency': [18], 'superkey': [18], 'candidate-key': [18],
    'prime-attribute': [18], 'partial-dependency': [18], 'transitive-dependency': [18],
    'first-normal-form': [18], 'second-normal-form': [18], 'third-normal-form': [18], 'bcnf': [18],
}
POSTGRES = {'primary-key', 'foreign-key', 'constraints', 'integrity'}
SUPABASE = {'supabase'}

def enrich(slides):
    by_id = {s['id']: s for s in slides}
    for s in slides:
        pages = PAGES.get(s['id'], [])
        sources = [f'{PDF}#page={p}' for p in pages]
        if s['id'] in POSTGRES:
            sources.append(PG)
        if s['id'] in SUPABASE:
            sources.append(SUPA + 'overview')
        s['source_pages'] = pages
        s['sources'] = list(dict.fromkeys(sources + s.get('source_urls', [])))
    def block(ident, kind, ko, en):
        by_id[ident]['ko'][kind] = ko
        by_id[ident]['en'][kind] = en
    block('design-stages','steps',
          [['개념적 설계','대상·속성·관계 식별'],['논리적 설계','테이블·키·제약으로 구조화'],['물리적 설계','저장·접근 구조 결정']],
          [['Conceptual','Identify entities, attributes, and relationships'],['Logical','Structure tables, keys, and constraints'],['Physical','Determine storage and access structures']])
    block('second-normal-form','table',
          {'head':['분리된 테이블','속성'], 'rows':[['식당','식당 ID · 식당 이름'],['식당 메뉴','식당 ID · 메뉴 ID · 가격']]},
          {'head':['Decomposed table','Attributes'], 'rows':[['Restaurant','Restaurant ID · restaurant name'],['Restaurant menu','Restaurant ID · menu ID · price']]})
    block('third-normal-form','table',
          {'head':['분리된 테이블','속성'], 'rows':[['식당','식당 ID · 지역 코드'],['지역','지역 코드 · 지역 이름']]},
          {'head':['Decomposed table','Attributes'], 'rows':[['Restaurant','Restaurant ID · region code'],['Region','Region code · region name']]})
    # Source graphics are isolated PDF regions; the erroneous 0..N FoodMap
    # mark is deliberately not imported, while the original ERD legend is kept.
    by_id['dbms']['sources'].append('https://www.postgresql.org/docs/current/tutorial-arch.html')
    by_id['dbms']['diagram'] = 'dbms_architecture'
    by_id['db-types']['note'] = ('2025 원문 표현 그대로 보존. 관계형의 비정형 처리와 NoSQL의 트랜잭션·확장 특성은 제품과 상황별로 다르다.')
    by_id['db-types']['sources'].extend(['https://www.postgresql.org/docs/current/datatype-json.html', 'https://www.mongodb.com/docs/manual/core/transactions/'])
    by_id['database-trends-2025']['sources'].extend(['https://db-engines.com/en/ranking', 'https://db-engines.com/en/ranking_trend', 'https://db-engines.com/en/ranking_definition'])
    by_id['database-trends-2025']['note'] = ('DB-Engines 2026년 10월 화면. 순위는 DBMS의 상대적인 인기도 지표이며 시장 점유율을 뜻하지 않는다.')
    figures = {
        'database-trends-2025': [('database-trends-2026-10-chart.jpg', '2026년 10월 DB-Engines의 데이터베이스 인기도 추이 그래프', 'DB-Engines database popularity trends through October 2026'), ('database-trends-2026-10-ranking.jpg', '2026년 10월 DB-Engines 데이터베이스 인기도 순위 1위에서 10위까지의 표', 'DB-Engines database popularity ranks 1 through 10 in October 2026')],
        'database-careers': [('database-careers.jpg', '데이터 관련 채용 직군과 분야 목록', 'List of data-related job openings and areas')],
        'database-history': [('database-history.jpg', '1962년부터 2010년까지 데이터베이스 발전을 표시한 연대표', 'Timeline of database developments from 1962 to 2010')],
        'database': [('database-sharing.png', '데이터를 공유하고 보안과 무결성을 관리하는 데이터베이스 그림', 'Database sharing, security, and integrity illustration')],
        'design-purpose': [('design-objective.png', '현실 세계, 개념적 모델, 논리적 모델, 데이터베이스 사이의 설계 관계', 'Design relationships between the real world, conceptual model, logical model, and database')],
        'design-stages': [('design-process-lifecycle.png', '개념적·논리적·물리적 설계와 요구사항 분석, 설계, 구현, 운영, 감시 및 개선의 생명주기', 'Conceptual, logical, and physical design alongside requirements, design, implementation, operation, and monitoring')],
        'logical': [('logical-model-mapping.png', '엔티티에서 테이블, 속성에서 열, 관계에서 키로의 대응', 'Mapping entities to tables, attributes to columns, and relationships to keys')],
        'cardinality': [('erd-cardinality-legend.png', '일대일, 일대다, 필수와 선택 참여를 보여주는 ERD 관계 기호 범례', 'ERD symbols for one, many, mandatory and optional participation'), ('erd-company-example.png', 'Company, Employee, Projects의 관계 예시', 'Example relationships among Company, Employee, and Projects')],
        'normalization': [('normalization-diagrams.png', '수강 등록 데이터의 2차와 3차 정규화 전후 테이블 구조', 'Second- and third-normal-form decomposition for course registration tables')],
    }
    for ident, items in figures.items():
        slide = by_id[ident]
        # The original design lifecycle figure replaces the equivalent steps.
        if ident == 'design-stages':
            slide['ko'].pop('steps', None)
            slide['en'].pop('steps', None)
        slide['source_figures'] = [dict(src=filename if filename.startswith('../') else 'materials/source-figures/' + filename,
                                        alt=(ko_alt, en_alt),
                                        caption=('별도 스키마 SQL 예시', 'SQL example using a separate schema') if ident == 'sql' else None)
                                   for filename, ko_alt, en_alt in items]
    return slides
