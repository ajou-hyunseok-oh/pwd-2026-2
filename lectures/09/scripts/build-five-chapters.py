"""Build the current Week 9 deck from its approved outline and teaching blocks."""
import re
import sys
from copy import deepcopy
from pathlib import Path

from five_chapter_content import EXPLANATIONS, RESOURCES as ADAPTED_RESOURCES
from new_resources import RESOURCES as NEW_RESOURCES
from resource_blocks import render_resource
from reused_resources import RESOURCES as REUSED_RESOURCES
from slide_body import BODY, compose


LECTURE = Path(__file__).resolve().parents[1]
DESTINATION = LECTURE / 'current'
sys.path.insert(0, str(LECTURE.parent / 'authoring'))
from deck_builder import build


CONTENT = (
    (
        'turing-test', 'dartmouth', 'symbolic-ai', 'perceptron', 'expert-system',
        'ai-winter', 'machine-learning', 'inference', 'deep-learning', 'backpropagation',
        'alexnet', 'alphago',
    ),
    (
        'language-model', 'tokens', 'attention', 'transformer', 'text-generation',
        'code-completion', 'conversational-development', 'development-prompt', 'code-revision',
        'tool-calling', 'agent-loop', 'mcp',
    ),
    (
        'context-window', 'context-engineering', 'project-instructions', 'agent-skills',
        'specification', 'acceptance-criteria',
    ),
    (
        'task-decomposition', 'automated-tests', 'browser-verification', 'execution-harness',
        'pause-and-resume', 'agent-evals', 'agent-orchestration', 'parallel-integration',
    ),
    (
        'change-review', 'continuous-integration', 'agentic-workflows', 'agentic-engineering',
        'agent-delegation-outlook',
    ),
)
ORIGINAL_RESOURCES = {**REUSED_RESOURCES, **NEW_RESOURCES}


def bilingual(cell):
    ko, en = cell.split(' / ', 1)
    return ko, en


def link_shared_images(columns):
    for column in columns:
        for block in column:
            if block['kind'] == 'figure':
                assert (LECTURE / block['src']).is_file(), block['src']
                block['src'] = '../' + block['src']
            elif block['kind'] == 'resource-row':
                link_shared_images(block['columns'])


def teaching_blocks(ident):
    spec = EXPLANATIONS[ident] if ident in EXPLANATIONS else BODY[ident]
    if ident in ADAPTED_RESOURCES and spec['layout'] == 'wide':
        columns = deepcopy(ADAPTED_RESOURCES[ident]['columns'])
        media, = columns
        blocks = dict(layout='single', columns=[[spec['explanation'], *media]])
    else:
        resources = ADAPTED_RESOURCES[ident] if ident in ADAPTED_RESOURCES else ORIGINAL_RESOURCES[ident]
        blocks = compose(ident, resources)
        blocks['columns'][0][0] = spec['explanation']
    link_shared_images(blocks['columns'])
    return blocks


def lesson():
    outline = (LECTURE / 'materials/week-09-five-chapter-outline.txt').read_text(encoding='utf-8')
    headings, references = outline.split('\n출처 기록\n', 1)
    catalog = dict(re.findall(r'^\[([HLMX]\d\d)\].*\n((?:https?://[^\n]+\n)+)', references, re.M))
    sections = re.split(r'^0([1-5])\. .* · 화면 (\d+)$', headings, flags=re.M)
    cover_ko, cover_en = re.findall(r'^(?:KO|EN) · .* \| (.+)$', sections[0], re.M)
    slides = []

    for start in range(1, len(sections), 3):
        chapter, screen, text = sections[start:start + 3]
        assert int(screen) == len(slides) + 2, chapter
        titles = re.findall(r'^(?:KO|EN) · (.+?) \| ', text, re.M)
        assert len(titles) == 2, chapter
        slides.append(dict(id=f'chapter-{int(chapter):02}', kind='chapter', title=tuple(titles)))
        rows = re.findall(r'^\| (\d\d) \| [^|]+ \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', text, re.M)
        for ident, (number, title, lead, review) in zip(CONTENT[int(chapter) - 1], rows, strict=True):
            assert int(number) == len(slides) + 2, ident
            urls = dict.fromkeys(url for ref in re.findall(r'\b[HLMX]\d\d\b', review)
                                 for url in catalog.get(ref, '').splitlines())
            slides.append(dict(id=ident, kind='content', title=bilingual(title), lead=bilingual(lead),
                               sources=list(urls), **teaching_blocks(ident)))

    assert len(slides) == 48
    return (cover_ko, cover_en), slides


if __name__ == '__main__':
    subtitle, slides = lesson()
    build(DESTINATION, 9, subtitle, slides, render_extra=render_resource,
          stylesheets=('../resources.css', '../body.css', 'lecture.css'))
