"""모션 그래픽(인라인 SVG) 조립용 도우미.

그림 하나를 Fig 객체로 만들고 html()로 <figure class="mg"> 조각을 얻는다.
애니메이션 클래스(mg-fromN / mg-onlyN / mg-winAB / mg-slideN / mg-growN)는 assets/css/common.css에 정의돼 있다.
기본 상태(애니메이션이 없을 때)가 곧 마지막 장면이 되도록 그린다.
"""
import math
import os
import re
from contextlib import contextmanager
from html import escape

W = 720
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "weekly")


def link_data_files(text):
    """안내 문장 속 데이터 파일 이름(weekNN_*.csv)에 data/weekly 파일 링크를 건다."""
    def repl(m):
        name = m.group(1)
        wk = name[:6]
        if os.path.exists(os.path.join(DATA_DIR, wk, name)):
            return f'<a href="../../data/weekly/{wk}/{name}" target="_blank" rel="noopener">{name}</a>'
        return name
    return re.sub(r"(week\d{2}_[A-Za-z0-9_]+\.csv)", repl, text)


def _cls(*parts):
    return " ".join(p for p in parts if p)


def fmt(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Fig:
    def __init__(self, fid, h, narr, label, caption, alt, note=None):
        assert len(narr) in (6, 8), f"{fid}: 장면 설명은 6개 또는 8개여야 한다"
        self.fid, self.h, self.narr = fid, h, narr
        self.label, self.caption, self.alt = label, caption, alt
        self.n = len(narr)
        self.pre = "mg" if self.n == 6 else "mg8"  # 8장면 그림은 mg8-fromN / mg8-onlyN 클래스를 쓴다
        # 안내 문구("움직이는 그림 · 예시 그림 …")는 달지 않는다. 데이터 파일 출처처럼 꼭 필요한 말만 note로 남긴다.
        self.note = re.sub(r"^움직이는 그림 · ", "", note or "")
        self.out = []

    # ---- 기본 도형 ----
    def raw(self, s):
        self.out.append(s)

    def t(self, x, y, s, c="", a="", style=""):
        st = f' style="{style}"' if style else ""
        self.out.append(f'<text x="{fmt(x)}" y="{fmt(y)}" class="{_cls(c, a)}"{st}>{escape(str(s))}</text>')

    def r(self, x, y, w, h, c="mg-box", a="", rx=0):
        r = f' rx="{rx}"' if rx else ""
        self.out.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}"{r} class="{_cls(c, a)}"/>')

    def c(self, x, y, rad, c="mg-dot", a=""):
        self.out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(rad)}" class="{_cls(c, a)}"/>')

    def l(self, x1, y1, x2, y2, c="mg-ln", a=""):
        self.out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" class="{_cls(c, a)}"/>')

    def poly(self, pts, c="mg-box", a=""):
        p = " ".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
        self.out.append(f'<polygon points="{p}" class="{_cls(c, a)}"/>')

    def path(self, d, c="mg-ln", a=""):
        self.out.append(f'<path d="{d}" class="{_cls(c, a)}"/>')

    def arrow(self, x1, y1, x2, y2, c="mg-ln", head="mg-ah", a="", size=9):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - size * math.cos(ang), y2 - size * math.sin(ang)
        px, py = -math.sin(ang) * size * 0.5, math.cos(ang) * size * 0.5
        if a:
            self.out.append(f'<g class="{a}">')
        self.l(x1, y1, bx, by, c)
        self.poly([(x2, y2), (bx + px, by + py), (bx - px, by - py)], head)
        if a:
            self.out.append("</g>")

    @contextmanager
    def g(self, a="", dx=None, dy=None):
        st = ""
        if dx is not None or dy is not None:
            st = f' style="--dx:{fmt(dx or 0)}px;--dy:{fmt(dy or 0)}px"'
        self.out.append(f'<g class="{a}"{st}>')
        yield
        self.out.append("</g>")

    # ---- 칸 도우미 ----
    def chip(self, x, y, w, h, s, box="mg-box", tc="", a="", size="mg-s"):
        """글자가 든 상자(가운데 정렬)."""
        if a:
            self.out.append(f'<g class="{a}">')
        self.r(x, y, w, h, box)
        self.t(x + w / 2, y + h / 2 + 5, s, _cls("mg-c", size, tc))
        if a:
            self.out.append("</g>")

    def thead(self, x, y, cols, h=26):
        cx = x
        for name, w in cols:
            self.r(cx, y, w, h, "mg-ink")
            self.t(cx + w / 2, y + h / 2 + 4.5, name, "mg-c mg-tw mg-b mg-s")
            cx += w

    def trow(self, x, y, cols, vals, h=24, box="mg-box", tcs=None):
        cx = x
        for i, ((name, w), v) in enumerate(zip(cols, vals)):
            b = box[i] if isinstance(box, (list, tuple)) else box
            tc = tcs[i] if tcs else ""
            self.r(cx, y, w, h, b)
            self.t(cx + w / 2, y + h / 2 + 4.5, v, _cls("mg-c mg-s", tc))
            cx += w

    # ---- 마무리 ----
    def narration(self):
        y = self.h - 38
        self.r(14, y, W - 28, 30, "mg-gray")
        for i, s in enumerate(self.narr):
            self.t(28, y + 20, s, f"{self.pre}-only{i} mg-b", style="font-size:14px")

    def html(self):
        self.narration()
        body = "\n".join("    " + s for s in self.out)
        sty = ' style="--mg-t:20s"' if self.n == 8 else ""
        note = f'  <p class="illustration-note">{link_data_files(escape(self.note))}</p>\n' if self.note else ""
        return (
            f"<!-- mg:{self.fid} -->\n"
            f'<figure class="mg"{sty}>\n'
            f"{note}"
            f'  <svg class="mg-svg" viewBox="0 0 {W} {self.h}" role="img" aria-label="{escape(self.alt, quote=True)}">\n'
            f"{body}\n"
            f"  </svg>\n"
            f'  <figcaption class="img-caption"><b>{escape(self.label)}</b> {self.caption}</figcaption>\n'
            f"</figure>\n"
            f"<!-- /mg:{self.fid} -->"
        )
