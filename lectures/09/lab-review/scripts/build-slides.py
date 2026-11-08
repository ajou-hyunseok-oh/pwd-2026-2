"""Build this deck from lesson.py using the shared Week 6/7 format."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'authoring'))
from deck_builder import build
from lesson import WEEK, SUBTITLE, SLIDES

if __name__ == '__main__':
    build(Path(__file__).resolve().parents[1], WEEK, SUBTITLE, SLIDES)
