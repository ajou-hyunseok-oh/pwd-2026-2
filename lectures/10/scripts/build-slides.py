import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'authoring'))
from deck_builder import build
from lesson import WEEK, SLIDES
from ai_security import SLIDES as AI_SLIDES
SUBTITLE = ('AI 시대의 웹 서비스 보안', 'Web Service Security in the AI Era')
SLIDES = AI_SLIDES + SLIDES
if __name__ == '__main__': build(Path(__file__).resolve().parents[1], WEEK, SUBTITLE, SLIDES)
