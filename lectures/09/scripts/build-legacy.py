"""Build the archived 85-slide Week 9 deck from lesson.py."""
import sys
from pathlib import Path
from copy import deepcopy

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'authoring'))
from deck_builder import build
from lesson import WEEK, SUBTITLE, SLIDES
from resource_blocks import render_resource

if __name__ == '__main__':
    def relocate(value):
        if isinstance(value, dict):
            if value.get('kind') == 'figure':
                value['src'] = '../' + value['src']
            for child in value.values():
                relocate(child)
        elif isinstance(value, list):
            for child in value:
                relocate(child)

    slides = deepcopy(SLIDES)
    relocate(slides)
    build(Path(__file__).resolve().parents[1] / 'legacy', WEEK, SUBTITLE, slides,
          render_extra=render_resource, stylesheets=('../resources.css','../body.css'))
