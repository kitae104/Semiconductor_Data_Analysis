import os

import numpy as np
import pandas as pd

from .lib import Fig

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ice = pd.read_csv(os.path.join(BASE, "data", "weekly", "week06", "week06_easy_icecream_daily.csv"), encoding="utf-8-sig")
NOTE = "움직이는 그림 · 이 차시 예제 파일(week06_easy_icecream_daily.csv)의 값"


def which_fig():
    wc = ice["날씨"].value_counts()
    counts, edges = np.histogram(ice["판매량_count"], bins=5)
    xs, ys = ice["최고기온_C"], ice["판매량_count"]
    f = Fig("w6-which", 304,
            ["① 알고 싶은 질문에 따라 고르는 그래프가 다르다", "② 막대: 무리마다 몇 개인가 (plt.bar)", "③ 히스토그램: 값이 어디에 몰렸나 (plt.hist)",
             "④ 산점도: 두 값이 함께 움직이나 (plt.scatter)", "⑤ 가로·세로에 무엇을 놓았는지 xlabel·ylabel로 적는다", "결과: 질문이 그래프 종류를 정한다"],
            "그래프 고르기 — 질문에 맞는 그래프",
            "세 그래프 모두 아이스크림 가게 21일치 기록으로 그렸다. 막대는 <b>종류별 개수</b>, 히스토그램은 <b>한 숫자 열의 분포</b>, 산점도는 <b>숫자 열 두 개의 관계</b>를 볼 때 쓴다.",
            "날씨별 날 수 막대그래프, 판매량 히스토그램, 최고기온과 판매량 산점도 세 가지 그래프를 나란히 보여 주는 그림", note=NOTE)
    panels = [
        (20, "무리마다 몇 개?", "plt.bar()"),
        (250, "값이 어디에 몰렸나?", "plt.hist()"),
        (480, "두 값이 함께 움직이나?", "plt.scatter()"),
    ]
    for i, (x0, q, code) in enumerate(panels):
        f.r(x0, 20, 220, 200, "mg-box")
        f.t(x0 + 110, 42, q, "mg-b mg-c")
        f.t(x0 + 110, 60, code, "mg-m mg-s mg-c mg-tblue")
        f.l(x0 + 24, 190, x0 + 208, 190, "mg-ln")
        f.l(x0 + 24, 76, x0 + 24, 190, "mg-ln")
        f.r(x0 - 3, 17, 226, 206, "mg-hl", a=f"mg-only{i + 1}")
    # 막대
    mx = wc.max()
    for k, (name, v) in enumerate(wc.items()):
        h = 100 * v / mx
        x = 20 + 46 + k * 52
        f.r(x, 190 - h, 36, h, "mg-blue", a="mg-grow1")
        f.t(x + 18, 206, name, "mg-s mg-c")
        f.t(x + 18, 190 - h - 5, str(v), "mg-m mg-s mg-c mg-b mg-tblue", a="mg-from2")
    # 히스토그램
    cm = counts.max()
    for k, v in enumerate(counts):
        h = 100 * v / cm
        f.r(250 + 28 + k * 33, 190 - h, 33, h, "mg-blue", a="mg-grow2")
    f.t(250 + 28, 206, f"{edges[0]:.0f}", "mg-m mg-s mg-mu")
    f.t(250 + 28 + 165, 206, f"{edges[-1]:.0f}", "mg-m mg-s mg-e mg-mu")
    # 산점도
    x0 = 480
    for xv, yv in zip(xs, ys):
        px = x0 + 32 + (xv - xs.min()) / (xs.max() - xs.min()) * 165
        py = 184 - (yv - ys.min()) / (ys.max() - ys.min()) * 100
        f.c(px, py, 3.6, "mg-dot", a="mg-from3")
    f.t(x0 + 110, 238, "x: 최고기온_C  y: 판매량_count", "mg-s mg-c mg-mu", a="mg-from4")
    f.t(20 + 110, 238, "x: 날씨  y: 날 수", "mg-s mg-c mg-mu", a="mg-from4")
    f.t(250 + 110, 238, "x: 판매량_count  y: 날 수", "mg-s mg-c mg-mu", a="mg-from4")
    return f


def hist_fig():
    vals = sorted(ice["판매량_count"].tolist())
    counts, edges = np.histogram(vals, bins=5)
    lo, hi = vals[0], vals[-1]

    def X(v):
        return 60 + (v - lo) / (hi - lo) * 600

    f = Fig("w6-hist", 330,
            [f"① {len(vals)}일치 판매량을 값의 순서대로 눈금 위에 놓는다", "② bins=5 → 눈금을 구간 5개로 나눈다", "③ 점이 자기 구간 칸으로 떨어진다",
             "④ 구간에 쌓인 개수가 막대 높이가 된다", "⑤ 막대가 높은 구간 = 값이 많이 몰린 곳", "결과: 히스토그램은 값을 구간으로 묶어 개수를 센다"],
            "히스토그램 — 값을 구간으로 묶어 세기",
            "<code>bins=5</code>는 값의 범위를 다섯 구간으로 나눈다는 뜻이다. 점 하나가 하루의 판매량이고, 구간마다 쌓인 점의 개수가 막대 높이가 된다.",
            "21일치 판매량 점들이 눈금 위에서 다섯 구간으로 나뉘어 아래로 떨어져 쌓이고 막대가 되는 그림", note=NOTE)
    base, line_y = 250, 76
    f.l(50, line_y, 670, line_y, "mg-ln")
    # 막대(점 뒤에 깔림)
    for k, v in enumerate(counts):
        xa, xb = X(edges[k]) if k else 60, X(edges[k + 1]) if k < 4 else 660
        f.r(xa + 2, base - 20 * v, xb - xa - 4, 20 * v, "mg-blue", a="mg-from4")
        f.t((xa + xb) / 2, base - 20 * v - 6, str(v), "mg-m mg-b mg-c mg-tblue", a="mg-from4")
    # 구간 경계
    for k in range(6):
        xe = 60 if k == 0 else (660 if k == 5 else X(edges[k]))
        f.l(xe, 62, xe, base, "mg-lnm mg-dsh", a="mg-from2")
        f.t(xe, base + 18, f"{edges[k]:.0f}", "mg-m mg-s mg-c mg-mu", a="mg-from2")
    f.l(50, base, 670, base, "mg-ln")
    # 점
    seen = {}
    for v in vals:
        k = min(int(np.searchsorted(edges, v, side="right")) - 1, 4)
        n = seen.get(k, 0)
        seen[k] = n + 1
        xa, xb = X(edges[k]) if k else 60, X(edges[k + 1]) if k < 4 else 660
        tx = (xa + xb) / 2
        ty = base - 10 - 20 * n
        with f.g("mg-slide3", tx - X(v), ty - (line_y - 12)):
            f.c(X(v), line_y - 12, 8, "mg-doto")
    f.t(40, 52, "판매량_count", "mg-m mg-s mg-mu")
    return f


def scatter_fig():
    xs, ys = ice["최고기온_C"], ice["판매량_count"]
    n = len(ice)
    f = Fig("w6-scatter", 320,
            [f"① 첫째 날: ({xs[0]}도, {ys[0]}개) → 점 하나", f"② 둘째 날: ({xs[1]}도, {ys[1]}개) → 점 하나 더", f"③ 셋째 날: ({xs[2]}도, {ys[2]}개)",
             f"④ 넷째 날: ({xs[3]}도, {ys[3]}개)", f"⑤ 다섯째 날: ({xs[4]}도, {ys[4]}개)", f"결과: {n}일을 다 찍으면 점이 이루는 흐름이 보인다"],
            "산점도 — 행 하나가 점 하나",
            f"표의 한 행(하루)에서 <b>최고기온_C는 가로(x)</b>, <b>판매량_count는 세로(y)</b>가 되어 점이 하나 찍힌다. {n}일이면 점이 {n}개이고, 점들이 어떤 방향으로 늘어서는지가 두 값의 관계다.",
            f"기록표의 앞 다섯 행이 차례로 점 하나씩 찍히고 마지막에 {n}일치 점이 모두 나타나는 산점도 그림", note=NOTE)
    cols = [("최고기온_C", 100), ("판매량_count", 110)]
    f.thead(20, 40, cols, h=26)
    for i in range(5):
        f.trow(20, 66 + 26 * i, cols, [xs[i], ys[i]], h=26)
        f.r(16, 62 + 26 * i, 218, 34, "mg-hl", a=f"mg-only{i}")
    f.t(20, 224, "⋮", "mg-b mg-mu")
    f.t(40, 224, f"(모두 {n}행)", "mg-s mg-mu")
    px0, px1, py0, py1 = 330, 690, 220, 40
    f.l(px0, py0, px1, py0, "mg-ln")
    f.l(px0, py0, px0, py1, "mg-ln")
    f.t((px0 + px1) / 2, 252, "최고기온_C", "mg-s mg-c mg-mu")
    f.t(px0 - 8, py1 - 8, "판매량_count", "mg-s mg-mu")

    def P(i):
        return (px0 + 16 + (xs[i] - xs.min()) / (xs.max() - xs.min()) * (px1 - px0 - 32),
                py0 - 14 - (ys[i] - ys.min()) / (ys.max() - ys.min()) * (py0 - py1 - 28))

    for i in range(n):
        x, y = P(i)
        a = "" if i == 0 else (f"mg-from{i}" if i < 5 else "mg-from5")
        f.c(x, y, 5.5 if i < 5 else 4.5, "mg-dot" if i < 5 else "mg-dotm", a=a)
    for i in range(5):
        x, y = P(i)
        f.c(x, y, 11, "mg-hl", a=f"mg-only{i}")
    return f


FIGS = [
    ("히스토그램 —", hist_fig()),
    ("산점도 —", scatter_fig()),
    ("그래프 4줄 틀", which_fig()),
]
