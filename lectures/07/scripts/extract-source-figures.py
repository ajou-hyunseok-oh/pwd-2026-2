"""Extract diagram regions from the 2025 reference PDF without page chrome.

Requires Poppler pdftoppm. Coordinates are PDF points with a bottom-left origin.
Crops are rendered from complete pages so separate vector labels and connectors
stay aligned with raster diagram elements. No generated slide files are changed.
"""
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / 'materials/[PWD 5] Database 기본 개념 및 MERN Stack 개발환경의 이해.pdf'
OUT = ROOT / 'materials/source-figures'
SCALE = 3  # 216 DPI; original PDF pages are 720 x 405 points.
# name, page, (left, bottom, right, top), in PDF points
FIGURES = [
    ('database-sharing', 4, (443, 94, 696, 347)),
    ('design-objective', 11, (125, 24, 592, 302)),
    ('design-process-lifecycle', 12, (382, 14, 682, 359)),
    ('logical-model-mapping', 14, (417, 111, 674, 251)),
    ('erd-cardinality-legend', 16, (420, 42, 554, 302)),
    ('erd-company-example', 16, (590, 42, 684, 302)),
    ('normalization-diagrams', 18, (380, 198, 701, 367)),
    ('sql-example', 19, (338, 48, 676, 274)),
]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, number, (left, bottom, right, top) in FIGURES:
        # Source page 4 contains a high-resolution illustration (2048 px).
        # Retain nearly all of its detail; the remaining crops use 216 DPI.
        scale = 8 if name == 'database-sharing' else SCALE
        x, y = round(left*scale), round((405-top)*scale)
        width, height = round((right-left)*scale), round((top-bottom)*scale)
        run(['pdftoppm', '-f', str(number), '-l', str(number), '-singlefile',
             '-r', str(72*scale), '-x', str(x), '-y', str(y), '-W', str(width),
             '-H', str(height), '-png', str(PDF), str(OUT/name)], check=True)
        print(f'{name}.png: page {number}, {width}x{height}')
    # Page 5 has a self-contained 600 × 724 JPEG timeline as its second
    # image object; extract the JPEG bytes directly instead of re-rendering it.
    with TemporaryDirectory(prefix='pwd7-history-') as temp_dir:
        prefix = str(Path(temp_dir) / 'page5')
        run(['pdfimages', '-f', '5', '-l', '5', '-j', str(PDF), prefix], check=True)
        image = Path(temp_dir) / 'page5-001.jpg'
        if not image.exists():
            raise FileNotFoundError('The page 5 history illustration was not found')
        copyfile(image, OUT / 'database-history.jpg')
        print('database-history.jpg: page 5, original 600x724 JPEG')

    # Pages 7 and 8 each embed the original graphics as JPEGs. Preserve
    # those exact bytes: the first object on each page is the school logo.
    with TemporaryDirectory(prefix='pwd7-trends-') as temp_dir:
        prefix = str(Path(temp_dir) / 'page7')
        run(['pdfimages', '-f', '7', '-l', '7', '-j', str(PDF), prefix], check=True)
        for image_name, output_name in [
            ('page7-001.jpg', 'database-trends-2025-chart.jpg'),
            ('page7-002.jpg', 'database-trends-2025-ranking.jpg'),
        ]:
            image = Path(temp_dir) / image_name
            if not image.exists():
                raise FileNotFoundError(f'The page 7 image {image_name} was not found')
            copyfile(image, OUT / output_name)
            print(f'{output_name}: page 7, original JPEG')
    with TemporaryDirectory(prefix='pwd7-careers-') as temp_dir:
        prefix = str(Path(temp_dir) / 'page8')
        run(['pdfimages', '-f', '8', '-l', '8', '-j', str(PDF), prefix], check=True)
        image = Path(temp_dir) / 'page8-001.jpg'
        if not image.exists():
            raise FileNotFoundError('The page 8 careers image was not found')
        copyfile(image, OUT / 'database-careers.jpg')
        print('database-careers.jpg: page 8, original JPEG')

if __name__ == '__main__':
    main()
