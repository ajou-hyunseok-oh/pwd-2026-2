"""Build the bilingual Week 3 lecture with approved headings from materials/slide-draft.json."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
chapters = json.loads((ROOT / "materials/slide-draft.json").read_text(encoding="utf-8"))
messages = {"ko": {}, "en": {}}
body_data = json.loads((ROOT / "materials/lesson-body.json").read_text(encoding="utf-8"))


def text(key, ko, en):
    messages["ko"][key] = ko
    messages["en"][key] = en
    return f'data-wd-i18n="{key}">{html.escape(ko)}'

def localized(tag, key, value, attrs=""):
    return f'<{tag} {attrs} {text(key, value["ko"], value["en"])}</{tag}>'

def render_concepts(items, key):
    result = '<ul class="week3-points week3-code-concepts">'
    for n, item in enumerate(items):
        ik = f"{key}_concept_{n}"
        result += '<li class="week3-point-group">' + localized("strong", ik, item)
        result += '<div class="week3-point-details">'
        for d, detail in enumerate(item["details"]):
            result += localized("p", f"{ik}_detail_{d}", detail)
        result += '</div></li>'
    return result + '</ul>'

def render_body(source, key):
    body = body_data["slides"][str(int(source))]
    panels = []
    for index, panel in enumerate(body["panels"]):
        pk = f"{key}_panel_{index}"
        content = localized("h3", pk + "_label", panel["label"])
        kind = panel["kind"]
        if kind == "code":
            value = panel["code"]
            displayed = panel.get("displayCode", {"ko": value, "en": value})
            content += localized("pre", pk + "_code", displayed,
                f'class="wd-code" data-wd-code="{panel["language"]}" data-wd-code-width="56"')
            if panel.get("errors"):
                message = " · ".join("TS" + str(n) for n in panel["errors"])
                content += localized("p", pk + "_diagnostic", {
                    "ko": "타입 오류: " + message, "en": "Type error: " + message}, 'class="week3-diagnostic"')
            if "output" in panel:
                content += localized("p", pk + "_output_label", {"ko": "실행 결과", "en": "Output"}, 'class="week3-output-label"')
                content += '<samp class="week3-output">' + html.escape(panel["output"]) + '</samp>'
            elif panel.get("runtimeError"):
                content += localized("p", pk + "_runtime", {"ko": "실행 시 " + panel["runtimeError"], "en": "Runtime: " + panel["runtimeError"]}, 'class="week3-diagnostic"')
        elif kind in ("points", "flow"):
            tag = "ol" if kind == "flow" else "ul"
            content += f'<{tag} class="week3-{kind}">'
            for n, item in enumerate(panel["items"]):
                if item.get("details"):
                    content += '<li class="week3-point-group">'
                    content += localized("strong", f"{pk}_item_{n}", item)
                    content += '<div class="week3-point-details">'
                    for d, detail in enumerate(item["details"]):
                        content += localized("p", f"{pk}_item_{n}_detail_{d}", detail)
                    content += '</div></li>'
                else:
                    content += localized("li", f"{pk}_item_{n}", item)
            content += f'</{tag}>'
        elif kind == "table":
            content += '<table class="week3-table"><thead><tr>'
            for n, item in enumerate(panel["headers"]):
                content += localized("th", f"{pk}_head_{n}", item, 'scope="col"')
            content += '</tr></thead><tbody>'
            for r, row in enumerate(panel["rows"]):
                content += '<tr>'
                for c, item in enumerate(row):
                    content += localized("td", f"{pk}_cell_{r}_{c}", item)
                content += '</tr>'
            content += '</tbody></table>'
        if panel.get("explanation"):
            content += localized("p", pk + "_explanation", panel["explanation"], 'class="week3-explanation"')
        if panel.get("concepts"):
            content += render_concepts(panel["concepts"], pk)
        panels.append(f'<div class="week3-panel week3-panel--{kind}">{content}</div>')
    result = f'<div class="week3-body week3-body--{body["layout"]}">' + ''.join(panels) + '</div>'
    if body.get("takeaway"):
        result += localized("p", key + "_takeaway", body["takeaway"], 'class="week3-takeaway"')
    # Source references stay in authoring metadata and the instructor review.
    # Student slides display the actual code, without reference-link footers.
    return result

slides = []
text("page_title", "03 | JavaScript / TypeScript 기초", "03 | JavaScript / TypeScript Basics")
slides.append(f'''          <section class="wd-slide week3-slide week3-cover is-active" data-wd-slide="cover" role="region">
            <div>
              <p class="week3-eyebrow" {text("cover_eyebrow", "2026학년도 2학기 실전웹서비스개발", "Practical Web Service Development · Fall 2026")}</p>
              <h1 {text("cover_title", "실전 웹서비스개발 – 3주차", "Practical Web Service Development – Week 3")}</h1>
              <p class="week3-cover__subtitle" {text("cover_subtitle", "JavaScript와 TypeScript의 문법을 통한 실행 흐름과 코드 구조 이해", "Learn JavaScript and TypeScript syntax and understand code flow and structure.")}</p>
            </div>
            <p class="week3-source">LECTURE 03</p>
          </section>''')
outline = ["# 3주차 슬라이드 초안: 타이틀 · 서브타이틀 · 챕터 구분", "",
    "확정된 타이틀, 서브타이틀, 챕터 구분의 목록. 본문·코드·도식은 index.html에 작성.", "",
    "## 적용 규칙", "",
    "- 제목은 가르칠 핵심 개념을 명확히 나타내는 명사구. 예제의 용도를 개념과 동등하게 나열하지 않음.",
    "- 서브타이틀은 학습 내용을 설명하는 한 줄 명사형 표현. '~한다.' 종결과 문장 끝 마침표는 사용하지 않음. 키워드 나열이나 제목 반복 대신 배울 관계·동작을 구체적으로 기술.",
    "- 설명에는 실제 개념·처리 과정·인과관계 사용. 의문형 제목, 제작 메모, 다음 내용 예고 제외.",
    "- 나열은 ` · `, 처리 흐름은 ` → `로 표기. 한·영에 동일한 문체와 구조 적용.",
    "- 1·2주차의 독립 챕터 표지 형식 적용. 기존 구성안의 상단 챕터 표식 방식 대신 번호·제목·서브타이틀로 챕터 구분.",
    "- 기존 주제 사이에 배열과 객체 개념 추가. 강의 표지 1장 + 챕터 표지 7장 + 주제 41장 + 번호 없는 실습 개요 1장 = 총 50장.",
    "- 주제 번호(sourcePage)는 본문 검증용 식별자. 실제 슬라이드 번호와 구분.",
    "- 2026-09-19: pwd-week3 기본 계산기에 맞춰 예제와 관련 제목·서브타이틀 갱신.",
    "- 초안 원본: `slide-draft.json`. 전체 재생성: `node lectures/03/scripts/build-slides.cjs`.", "",
    "## 강의 표지", "", "| 슬라이드 | 타이틀 | 서브타이틀 |", "|---|---|---|",
    "| 01 | 실전 웹서비스개발 – 3주차 | JavaScript와 TypeScript의 문법을 통한 실행 흐름과 코드 구조 이해 |"]
for chapter in chapters:
    if chapter.get("kind") == "practice":
        key = "practice"
        def practice_list(field):
            return '<ul>' + ''.join(localized("li", f"{key}_{field}_{i}", value) for i, value in enumerate(chapter[field])) + '</ul>'
        reference = html.escape(chapter["referenceUrl"], quote=True)
        slides.append(f'''          <section class="wd-slide wd-slide--content week3-slide week3-practice" data-wd-slide="practice-overview" role="region">
            <h2 class="wd-slide-heading" {text(key + "_title", chapter["title"], chapter["titleEn"])}</h2>
            <p class="wd-slide-lead" {text(key + "_subtitle", chapter["subtitle"], chapter["subtitleEn"])}</p>
            <div class="week3-body week3-body--equal">
              <div class="week3-practice-box">
                <h3 {text(key + "_goals", "학습 목표", "Learning Goals")}</h3>
                {practice_list("goals")}
                <h3 {text(key + "_requirements", "요구사항", "Requirements")}</h3>
                {practice_list("requirements")}
                <p><span {text(key + "_reference", "참고", "Reference")}</span>: <a href="{reference}" target="_blank" rel="noopener">{reference}</a></p>
              </div>
              <div class="week3-practice-result">
              <div class="week3-practice-box">
                <h3 {text(key + "_deadline_label", "과제 마감일", "Assignment Deadline")}</h3>
                {localized("p", key + "_deadline", chapter["deadline"], 'class="week3-practice-deadline"')}
                {practice_list("deliverables")}
                {localized("p", key + "_submission", chapter["submissionNote"])}
              </div>
              <figure class="week3-practice-preview">
                <img src="./materials/week3_result.png" alt="48 + 19 = 67" width="1038" height="1552">
                {localized("figcaption", key + "_result_caption", {"ko": "계산기 실행 결과", "en": "Calculator Result"})}
              </figure>
              </div>
            </div>
          </section>''')
        outline.extend(["", "## 실습 개요 (챕터 번호 없음)", "",
            "| 슬라이드 | 타이틀 | 서브타이틀 |", "|---|---|---|",
            f'| {len(slides):02} | {chapter["title"]} | {chapter["subtitle"]} |'])
        continue
    number = f'{chapter["number"]:02}'
    key = f"chapter_{number}"
    slides.append(f'''          <section class="wd-slide week3-slide week3-section" data-wd-slide="chapter-{number}" role="region">
            <p class="week3-section__number">{number}</p>
            <h2 {text(key + "_title", chapter["title"], chapter["titleEn"])}</h2>
            <p class="week3-section__lead" {text(key + "_subtitle", chapter["subtitle"], chapter["subtitleEn"])}</p>
          </section>''')
    outline.extend(["", f'## 챕터 {number}. {chapter["title"]}', "",
        "| 슬라이드 | 구분 / 원안 번호 | 타이틀 | 서브타이틀 |", "|---|---|---|---|",
        f'| {len(slides):02} | 챕터 표지 | {chapter["title"]} | {chapter["subtitle"]} |'])
    for topic in chapter["topics"]:
        source = f'{topic["sourcePage"]:02}'
        key = f"topic_{source}"
        slides.append(f'''          <section class="wd-slide wd-slide--content week3-slide" data-wd-slide="topic-{source}" data-chapter="{number}" role="region">
            <h2 class="wd-slide-heading" {text(key + "_title", topic["title"], topic["titleEn"])}</h2>
            <p class="wd-slide-lead" {text(key + "_subtitle", topic["subtitle"], topic["subtitleEn"])}</p>
            {render_body(source, key)}
          </section>''')
        outline.append(f'| {len(slides):02} | {source} | {topic["title"]} | {topic["subtitle"]} |')
assert len(slides) == 50
markup = '''<!doctype html>
<html class="wd-page" lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title data-wd-i18n="page_title">03 | JavaScript / TypeScript 기초</title>
    <link rel="stylesheet" href="../../packages/web-deck/web-deck.css">
    <link rel="stylesheet" href="./lecture.css">
    <link rel="stylesheet" href="./code-theme.css">
  </head>
  <body class="wd-page-body" data-lecture="03">
    <main class="wd-deck" data-web-deck>
      <div class="wd-viewport" data-wd-viewport>
        <div class="wd-stage" data-wd-stage>
''' + "\n\n".join(slides) + '''
        </div>
      </div>
    </main>
    <script src="lecture-content.js"></script>
    <script src="../shared/lecture-deck.js"></script>
    <script src="../../packages/web-deck/vendor/prism/prism.js" data-manual></script>
    <script src="../../packages/web-deck/web-deck.js"></script>
  </body>
</html>
'''
(ROOT / "index.html").write_text(markup, encoding="utf-8")
(ROOT / "lecture-content.js").write_text("window.LECTURE_CONTENT = " + json.dumps(messages, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
(ROOT / "materials/week-03-slide-draft.ko.md").write_text("\n".join(outline) + "\n", encoding="utf-8")
print(f"Week 3: {len(slides)} slides with KO/EN content")
