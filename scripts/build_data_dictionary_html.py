"""
데이터 설명서(data/data_dictionary/weekXX_dictionary.md)를 강의 페이지와 같은 디자인의 HTML로 변환한다.

- 원본은 .md 이다. 설명서를 고친 뒤에는 이 스크립트를 다시 실행해 .html 을 갱신한다.
- 결과: data/data_dictionary/weekXX_dictionary.html (assets/css/common.css 의 기존 클래스만 사용)
- 외부 패키지 없이 동작하도록, 설명서에서 쓰는 마크다운 문법(제목·문단·목록·표·인용·굵게·인라인 코드·링크)만
  직접 변환한다.

사용법:
    python scripts/build_data_dictionary_html.py
"""
import html
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(BASE, "data", "data_dictionary")
WEEKS = range(1, 11)


# ---------- 인라인 변환 ----------
def inline(text):
    """인라인 코드 → 이스케이프 → 굵게·링크 순서로 변환한다."""
    codes = []

    def keep_code(m):
        codes.append("<code>" + html.escape(m.group(1)) + "</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def _link(m):
    label, href = m.group(1), m.group(2)
    # 다른 설명서(.md)를 가리키는 링크는 변환된 .html 로 연결한다.
    href = re.sub(r"(week\d{2}_dictionary)\.md$", r"\1.html", href)
    return f'<a href="{html.escape(href)}">{label}</a>'


# ---------- 블록 변환 ----------
LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_table(lines):
    head = split_row(lines[0])
    rows = [split_row(l) for l in lines[2:]]
    out = ['<div class="tablewrap"><table class="timetable">', "<thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_callout(text, kind="concept"):
    """'**라벨**: 내용' 형태면 라벨을 콜아웃 태그로 올린다."""
    m = re.match(r"^\*\*(.+?)\*\*\s*[:：]\s*(.*)$", text, re.S)
    if m:
        return (f'<div class="callout {kind}"><b class="tag">{inline(m.group(1))}</b>'
                f"{inline(m.group(2))}</div>")
    return f'<div class="callout {kind}">{inline(text)}</div>'


def render_blocks(lines):
    """## 아래 본문 줄들을 HTML 블록 목록으로 변환한다."""
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>")
            i += 1
        elif s.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(render_table(tbl))
        elif s.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(render_callout(" ".join(quote)))
        elif LIST_RE.match(line):
            ordered = LIST_RE.match(line).group(2)[0].isdigit()
            items = []
            while i < n and lines[i].strip():
                m = LIST_RE.match(lines[i])
                if m:
                    items.append(m.group(3).strip())
                else:  # 앞 항목이 다음 줄로 이어지는 경우
                    items[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if ordered else "ul"
            cls = "goal-list" if ordered else "pt-list"
            out.append(f'<{tag} class="{cls}">'
                       + "".join(f"<li>{inline(t)}</li>" for t in items) + f"</{tag}>")
        else:
            para = []
            while i < n and lines[i].strip() and not LIST_RE.match(lines[i]) \
                    and not lines[i].strip().startswith(("|", ">", "#")):
                para.append(lines[i].strip())
                i += 1
            text = " ".join(para)
            if text.startswith("**") and re.match(r"^\*\*.+?\*\*\s*[:：]", text):
                out.append(render_callout(text))
            else:
                out.append(f"<p>{inline(text)}</p>")
    return "\n".join(out)


def parse(md):
    """(제목, 머리말 줄, [(절 제목, 본문 줄)]) 로 나눈다."""
    title, intro, sections = "", [], []
    for line in md.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            sections.append((line[3:].strip(), []))
        elif sections:
            sections[-1][1].append(line)
        else:
            intro.append(line)
    return title, intro, sections


# ---------- 페이지 조립 ----------
def week_nav(week):
    links = []
    for w in WEEKS:
        cur = ' class="current"' if w == week else ""
        links.append(f'      <a href="week{w:02d}_dictionary.html"{cur}>{w}차시</a>')
    return "\n".join(links)


def hero_subtitle(title):
    """'a.csv / b.csv 데이터 설명서 (선택 심화용)' → 파일 목록과 꼬리말을 분리한다."""
    m = re.match(r"^(.*?)\s*데이터 설명서\s*(.*)$", title)
    files, tail = (m.group(1), m.group(2)) if m else (title, "")
    names = [f.strip() for f in files.split("/") if f.strip()]
    code = " · ".join(f"<code>{html.escape(f)}</code>" for f in names)
    return code + (f" <span>{html.escape(tail)}</span>" if tail else "")


def build_page(week, md):
    title, intro, sections = parse(md)
    ww = f"{week:02d}"
    intro_html = render_blocks(intro)
    body = "\n\n".join(
        f'  <section class="block">\n    <h2>{inline(h)}</h2>\n{render_blocks(lines)}\n  </section>'
        for h, lines in sections)
    prev_link = (f'<a href="week{week - 1:02d}_dictionary.html">← {week - 1}차시 데이터 설명서</a>'
                 if week > 1 else '<a class="disabled">← 이전 없음</a>')
    next_link = (f'<a href="week{week + 1:02d}_dictionary.html">{week + 1}차시 데이터 설명서 →</a>'
                 if week < 10 else '<a class="disabled">다음 없음 →</a>')
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{week}차시 데이터 설명서</title>
<link rel="icon" href="../../assets/images/site/chip-favicon.png" type="image/png">
<link rel="stylesheet" href="../../assets/css/common.css">
<link rel="stylesheet" href="../../assets/css/print.css">
</head>
<body>
<!-- 자동 생성 파일: {os.path.basename(DICT_DIR)}/week{ww}_dictionary.md 를 고친 뒤
     python scripts/build_data_dictionary_html.py 로 다시 만든다. 이 파일을 직접 고치지 않는다. -->
<header class="site-header">
  <div class="header-row">
    <a class="brand" href="../../index.html"><img src="../../assets/images/site/chip-macro-logo.jpg" alt="" aria-hidden="true" class="brand-logo" width="34" height="34" /> 반도체 데이터 분석 10차시 과정
      <small>Semiconductor Process Data Analysis</small>
    </a>
    <nav class="week-nav">
{week_nav(week)}
    </nav>
  </div>
  <div class="progress-track"><div class="progress-fill" id="progressFill" data-week="{week}"></div></div>
</header>

<nav class="breadcrumb" aria-label="현재 위치">
  <a href="../../index.html">홈</a>
  <span class="sep">›</span>
  <a href="../../lectures/week{ww}/index.html">{week}차시 강의</a>
  <span class="sep">›</span>
  <span class="current">데이터 설명서</span>
</nav>

<main class="page">

  <div class="hero">
    <span class="badge blue">{week}차시 · 데이터 설명서</span>
    <h1>{week}차시 실습 데이터 설명서</h1>
    <p class="today-question">대상 파일: {hero_subtitle(title)}</p>
  </div>

{intro_html}

{body}

  <div class="nav-buttons">
    {prev_link}
    <a class="home" href="../../lectures/week{ww}/index.html">{week}차시 강의로 돌아가기</a>
    {next_link}
  </div>

</main>

<button id="backToTop" title="맨 위로">↑</button>
<footer class="site-footer">반도체 및 반도체 공정 데이터 분석 10차시 과정 · {week}차시 데이터 설명서 · 교육용 자료(가상 데이터 사용)</footer>

<script src="../../assets/js/common.js"></script>
</body>
</html>
"""


def main():
    for week in WEEKS:
        src = os.path.join(DICT_DIR, f"week{week:02d}_dictionary.md")
        if not os.path.exists(src):
            print(f"[건너뜀] {src} 없음")
            continue
        with open(src, encoding="utf-8") as f:
            md = f.read()
        dst = src[:-3] + ".html"
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(build_page(week, md))
        print(f"[생성] {os.path.relpath(dst, BASE)}")


if __name__ == "__main__":
    main()
