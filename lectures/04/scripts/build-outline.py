"""Build the two complete Week 4 lecture decks."""
from pathlib import Path
import argparse, json, re, runpy
from slide_body import render_body
from html import escape
root = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--period',choices=('1','2','all'),default='all')
args=parser.parse_args()
if args.period!='2': runpy.run_path(str(root/'scripts/react-body.py'))
if args.period!='1': runpy.run_path(str(root/'scripts/build-design.py'))
react_body=json.loads((root/'materials/react-body.json').read_text())
react_sources=json.loads((root/'materials/react-sources.json').read_text())
design_sources=json.loads((root/'materials/design-sources.json').read_text())
# The approved title table includes covers and chapters in their actual order.
rows = re.findall(r'^\| (\d{2}) \| (표지|챕터|본문) \| (.*?) \| (.*?) \|$', (root/'materials/week-04-react-titles.ko.txt').read_text(), re.M)
en = [
('React Fundamentals','Origins, UI Design Philosophy, Screen Updates, and First Run'),
('Introducing React and Its Origins','The Role, Background, and Adoption of React'),
('The Role and Scope of React','A JavaScript Library for Building Web User Interfaces'),
('The Origins of React','Growing Interface Complexity and Changing Data'),
('React at Facebook','UI Composition in the 2020 Facebook.com Redesign'),
('Key Milestones in React','Changes in Development and Learning Since Its Public Release'),
('React Usage in Developer Surveys','Professional Developer Responses in 2025 and Survey Interpretation'),
('React UI Design Philosophy','UI Elements, Reuse, and the Relationship Between Data and Presentation'),
('Component-Based UI Composition','Dividing a Product Search Interface by Responsibility'),
('Component Reuse and Consistency','Different Product Data Displayed with the Same Row Component'),
('Data Changes and UI Output','Product Lists and Result Counts That Follow Search Criteria'),
('Imperative and Declarative Programming','React Declaratively Describes the UI for the Current State'),
('jQuery and React Code Comparison','DOM Update Commands and UI Declarations for the Same Counter'),
('Extending React UI Design with React Native','Shared Concepts and Platform Differences at Shopify'),
('UI Updates in React','UI Calculation, DOM Updates, and Input Preservation'),
('DOM and Virtual DOM','The Browser Document and an In-Memory UI Representation'),
('The React UI Update Process','Calculating, Comparing, and Applying UI Changes'),
('UI Updates and Input Preservation','Typed Text Retained While a Clock Updates'),
('DOM Updates and Performance','Update Responsibilities and Actual Changes in jQuery and React'),
('Web Services Using React','Select an Icon to Explore the Service in a New Tab'),
('Project Setup and Hello World','From a Development Environment to the First React Screen'),
('React Development Tools','Node.js, npm, Vite, and Environment Checks'),
('Creating and Running a React Project','Project Scaffolding, Package Installation, and the Dev Server'),
('Hello World and Live Updates','Changes in App.tsx Reflected in the Browser')]
assert len(rows) == len(en) == 24
bodies=iter(react_body)
react_slides=[]
for (_, kind, title, subtitle), (et, es) in zip(rows,en):
    s=dict(kind={'표지':'cover','챕터':'chapter','본문':'topic'}[kind],title=[title,et],subtitle=[subtitle,es])
    if kind=='본문': s['body']=next(bodies)
    react_slides.append(s)
assert next(bodies,None) is None
slides=[]
def add(kind,title,subtitle,label):
    slides.append(dict(kind=kind,title=title,subtitle=subtitle,label=label))
design=json.loads((root/'materials/design-slides.json').read_text())
add('period',design[0]['title'],design[0]['lead'],['2교시','Period 2'])
leads=json.loads((root/'materials/design-chapters.json').read_text())
previous=None
for s in design[1:]:
    c=s['chapter']
    if c and c!=previous:
        j=int(c[0][:2])-1
        add('chapter',[v.split(' · ',1)[1] for v in c],leads[j],[f'2교시 · CHAPTER {j+5:02}',f'Period 2 · CHAPTER {j+5:02}'])
        previous=c
    add('topic',s['title'],s['lead'],['2교시','Period 2'])
    slides[-1]['body']=s
assert len(slides)==30
decks = [('index.html', 'lecture-content.js', react_slides), ('ai-design.html', 'period-2-content.js', slides)]
if args.period!='all': decks=[decks[int(args.period)-1]]
for filename, content_file, deck_slides in decks:
    slides = deck_slides
    slides[0]['kind'] = 'cover'
    messages={'ko':{},'en':{}}
    parts=[]
    for i,s in enumerate(slides):
        s.pop('label', None)
        keys={}
        for field in s:
            if field not in ('title','subtitle'): continue
            key=f'slide_{i+1:02}_{field}'
            keys[field]=key
            for k,locale in enumerate(messages): messages[locale][key]=s[field][k]
        tag='h1' if s['kind']=='cover' else 'h2'
        heading_class='wd-slide-heading' if s['kind']=='topic' else ''
        lead_class='wd-slide-lead' if s['kind']=='topic' else 'week4-subtitle'
        body=render_body(s.get('body',{}),f'slide_{i+1:02}',messages,react_sources if filename=='index.html' else design_sources)
        suffix='<p class="week4-source">LECTURE 04</p>' if s['kind']=='cover' else ''
        parts.append(f'''          <section class="wd-slide week4-slide week4-{s['kind']}{' design-slide' if filename=='ai-design.html' else ''}{' wd-slide--content' if s['kind']=='topic' else ''}{' is-active' if i==0 else ''}" data-wd-slide="{'cover' if i==0 else f'slide-{i+1:02}'}" role="region">
                <{tag} class="{heading_class}" data-wd-i18n="{keys['title']}">{escape(s['title'][0])}</{tag}>
                <p class="{lead_class}" data-wd-i18n="{keys['subtitle']}">{escape(s['subtitle'][0])}</p>
                {body}
                {suffix}
              </section>''')
    for k, locale in enumerate(messages):
        messages[locale]['page_title'] = '04 | ' + slides[0]['title'][k]
        messages[locale]['ui_deck_label'] = slides[0]['title'][k]
    parts=['\n'.join(line.rstrip() for line in part.splitlines() if line.strip()) for part in parts]
    (root/'materials'/('slide-outline.json' if filename=='index.html' else 'period-2-outline.json')).write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
    (root/content_file).write_text('window.LECTURE_CONTENT = '+json.dumps(messages,ensure_ascii=False,indent=2)+';\n')
    (root/filename).write_text('''<!doctype html>
    <html class="wd-page" lang="ko">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
        <title data-wd-i18n="page_title">'''+escape(messages['ko']['page_title'])+'''</title>
        <link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
        <link rel="stylesheet" href="lecture.css">
'''+('        <link rel="stylesheet" href="design.css">\n' if filename=='ai-design.html' else '        <link rel="stylesheet" href="react-cleanup.css">\n')+'''
      </head>
      <body class="wd-page-body" data-lecture="04">
        <main class="wd-deck" data-web-deck>
          <div class="wd-viewport" data-wd-viewport>
            <div class="wd-stage" data-wd-stage>
    '''+ '\n\n'.join(parts)+'''
            </div>
          </div>
        </main>
        <script src="'''+content_file+'''"></script>
        <script src="../shared/lecture-deck.js"></script>
        <script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
        <script src="../../packages/web-deck/web-deck.js"></script>
'''+('        <script src="assets/react-demos.js"></script>\n' if filename=='index.html' else '')+'''      </body>
    </html>
    ''')
    print(f'Built {len(slides)} complete slides')
    output = root / filename
    output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines()).rstrip() + '\n')
