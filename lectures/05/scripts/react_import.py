"""Reuse Lecture 04 with explicitly recorded Week 5 corrections."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

SOURCE = Path(__file__).resolve().parents[2] / '04'
RUNTIME_IMAGES = ('hello-world.png', 'hello-react.png')


def rebase_url(url):
    if urlsplit(url).scheme or url.startswith(('/', '#')):
        return url
    return '../04/' + url


def rebase_assets(markup):
    # Code examples remain byte-for-byte identical to the reviewed source.
    chunks = re.split(r'(<pre\b[\s\S]*?</pre>)', markup)
    for i in range(0, len(chunks), 2):
        chunks[i] = re.sub(r'\b(src|href)="([^"]+)"',
                           lambda m: f'{m[1]}="{rebase_url(m[2])}"', chunks[i])
        chunks[i] = re.sub(r'(\[Sources\]\n)([\s\S]*?)(\n\[/Sources\])',
                           lambda m: m[1] + '\n'.join(rebase_url(url) for url in m[2].splitlines()) + m[3], chunks[i])
    return ''.join(chunks)


def load_react_deck():
    source_html = (SOURCE / 'index.html').read_text()
    sections = re.findall(r'<section\b[^>]*data-wd-slide="([^"]+)"[^>]*>[\s\S]*?</section>', source_html)
    markup = re.findall(r'<section\b[^>]*data-wd-slide="[^"]+"[^>]*>[\s\S]*?</section>', source_html)
    outline = json.loads((SOURCE / 'materials/slide-outline.json').read_text())
    assignment = (SOURCE / 'lecture-content.js').read_text().split('=', 1)[1].strip().removesuffix(';')
    source_messages = json.loads(assignment)
    messages = {locale: {key: value for key, value in source_messages[locale].items() if key.startswith('slide_')}
                for locale in ('ko', 'en')}
    assert len(markup) == len(outline) and sections[0] == 'cover'
    chapter = ('CHAPTER 01 · React 기초', 'CHAPTER 01 · React Fundamentals')
    slides = []
    for number, (source_id, raw, row) in enumerate(zip(sections, markup, outline, strict=True), 1):
        ident = 'chapter-01' if number == 1 else source_id
        raw = raw.replace(' is-active', '', 1)
        raw = raw.replace(f'data-wd-slide="{source_id}"',
                          f'data-wd-slide="{ident}" data-wd-import="04/react" data-wd-source-slide="{source_id}"', 1)
        raw = rebase_assets(raw)
        sources = re.search(r'\[Sources\]\n([\s\S]*?)\n\[/Sources\]', raw)
        references = [('Lecture 04', f'../04/index.html#/{number}')]
        if sources:
            references.extend(('Original source', html.unescape(url)) for url in sources[1].splitlines())
        slides.append(dict(
            id=ident, chapter=chapter, title=tuple(row['title']), lead=tuple(row['subtitle']),
            kind='chapter' if number == 1 else ('subchapter' if row['kind'] == 'chapter' else row['kind']),
            topic_number=None, sources=references,
            import_html=raw,
            import_source=dict(lecture='04', deck='index.html', slide=source_id, number=number)))
    # Approved translation corrections affect only the named locale/key.
    # Every other original message and the Korean HTML fallback stay intact.
    corrections = json.loads((Path(__file__).resolve().parents[1] /
                              'materials/import-text-corrections.json').read_text())
    for correction in corrections:
        locale, key = correction['locale'], correction['key']
        slide = next(s for s in slides if s['id'] == correction['source_slide'])
        assert f'data-wd-i18n="{key}"' in slide['import_html'], key
        assert locale == 'en', 'Current import corrections preserve Korean HTML'
        assert messages[locale][key] == correction['before'], 'Imported source text changed'
        messages[locale][key] = correction['after']
        slide.setdefault('import_text_corrections', []).append(f'{locale}:{key}')
    # Explicit user requests (2026-10-12): replace Week 5 screens 24 and 25.
    from vite_setup import apply_vite_setup
    apply_vite_setup(next(slide for slide in slides if slide['id'] == 'slide-23'), messages)
    from vite_edit import apply_vite_edit
    apply_vite_edit(next(slide for slide in slides if slide['id'] == 'slide-24'), messages)
    slides[0]['import_messages'] = messages
    return slides


def copy_runtime_assets(destination):
    # The unchanged original demo bundle uses document-relative image URLs.
    target = destination / 'materials/images'
    target.mkdir(parents=True, exist_ok=True)
    for name in RUNTIME_IMAGES:
        data = (SOURCE / 'materials/images' / name).read_bytes()
        output = target / name
        if not output.exists() or output.read_bytes() != data:
            output.write_bytes(data)
