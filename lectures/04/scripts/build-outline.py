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
('React Fundamentals','Origins and UI Design Philosophy'),
('React Origins',''),
('The Origins of React','The Challenge of Keeping the UI in Sync with Changing Data'),
('The Role of React','A JavaScript library for building web interfaces that reflect data'),
('Facebook.com Redesign','React UI · CSS · JS · Data · Navigation'),
('The Evolution of React',''),
('React Usage',''),
('Web Services Using React','Select an Icon to Explore the Service in a New Tab'),
('React UI Design Philosophy','UI Elements, Reuse, and the Relationship Between Data and Presentation'),
('React UI Design Philosophy','Compose the UI from components and describe its appearance for the current data and state'),
('Component-Based UI Composition','Component boundaries and nesting in a product search screen'),
('Component Reuse and Consistency','One ProductRow component displays six products'),
('Data Changes and UI Output','Stock filter selected → Two unavailable products removed → Results 6 → 4'),
('Imperative and Declarative Programming','Two Ways to Update the Same Counter'),
('Extending React UI Design Across Environments',''),
('UI Updates in React','Virtual DOM Concepts and the UI Update Process'),
('What Is the Virtual DOM?','An In-Memory UI Representation Distinct from the Real DOM'),
('Direct DOM Updates and React','Stock Filter Changes the Result Count from 6 to 4'),
('The React UI Update Process','State Change → UI Calculation and Comparison → DOM Commit'),
('Virtual DOM Benefits and Limits','Update Responsibility and the Cost of UI Calculation'),
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
        lead_markup=f'<p class="{lead_class}" data-wd-i18n="{keys["subtitle"]}">{escape(s["subtitle"][0])}</p>' if s['subtitle'][0] else ''
        body=render_body(s.get('body',{}),f'slide_{i+1:02}',messages,react_sources if filename=='index.html' else design_sources)
        suffix='<p class="week4-source">LECTURE 04</p>' if s['kind']=='cover' else ''
        parts.append(f'''          <section class="wd-slide week4-slide week4-{s['kind']}{' design-slide' if filename=='ai-design.html' else ''}{' wd-slide--content' if s['kind']=='topic' else ''}{' is-active' if i==0 else ''}" data-wd-slide="{'cover' if i==0 else f'slide-{i+1:02}'}" role="region">
                <{tag} class="{heading_class}" data-wd-i18n="{keys['title']}">{escape(s['title'][0])}</{tag}>
                {lead_markup}
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
