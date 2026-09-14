"""Remove only the original PDF's top-right course label from exported SVGs."""
import re

LABEL = "2025학년도 2학기 실전웹서비스개발"


def without_course_label(svg):
    # Original label baseline: y=13.47; x=598.43..711.59, in a 720x405 page.
    # Delete glyph uses rather than covering the page with a colored rectangle.
    def keep_or_remove(match):
        transform = re.search(r'transform="matrix\(([^)]+)\)"', match[0])
        if transform:
            values = [float(value) for value in transform[1].split(',')]
            if len(values) == 6 and 598 <= values[4] <= 712 and abs(values[5] - 13.47) < .02:
                return ''
        return match[0]
    return re.sub(r'<use\b[^>]*data-text="[^>]*?/>', keep_or_remove, svg)


def without_course_label_text(text):
    return text.replace(LABEL + '\n', '').replace(LABEL, '').strip()
