"""Build the canonical Week 9 deck."""
import runpy
from pathlib import Path

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('build-five-chapters.py')), run_name='__main__')
