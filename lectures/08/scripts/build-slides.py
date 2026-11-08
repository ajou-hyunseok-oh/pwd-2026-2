"""Build this deck from lesson.py using the shared Week 6/7 format."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'authoring'))
from deck_builder import build
from lesson import WEEK, SUBTITLE, SLIDES
from resource_blocks import render_resource

if __name__ == '__main__':
    build(Path(__file__).resolve().parents[1], WEEK, SUBTITLE, SLIDES,
          render_extra=render_resource, stylesheets=('resources.css', 'body.css'))
