import os

import numpy as np
import pandas as pd

from .lib import Fig

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
shop = pd.read_csv(os.path.join(BASE, "data", "weekly", "week08", "week08_easy_weather_sales.csv"), encoding="utf-8-sig")


def corr_fig():
    n = 24
    rng = np.random.default_rng(3)
    x = rng.uniform(-1, 1, n)
    x = (x - x.mean()) / x.std()
    z = rng.normal(size=n)
    z = z - z.mean()
    z = z - (z @ x / n) * x
    z = z / z.std()
    rs = [0.0, -0.9, 0.5, 0.95]
    states = [r * x + np.sqrt(1 - r * r) * z for r in rs]
    real = [float(np.corrcoef(x, y)[0, 1]) for y in states]
    px0, px1, py0, py1 = 50, 410, 232, 30

    def P(xv, yv):
        return (px0 + (xv + 2.6) / 5.2 * (px1 - px0), py0 - (yv + 2.6) / 5.2 * (py0 - py1))

    f = Fig("w8-corr", 300,
            ["① 점이 흩어져 있다: 함께 움직이지 않는다", "② 오른쪽 아래로 모인다: 거꾸로 움직인다", "③ 오른쪽 위로 느슨하게 모인다",
             "④ 한 줄에 가깝게 모인다: 강하게 함께 움직인다", "⑤ 부호는 방향, 크기는 얼마나 한 줄인가", "결과: r은 함께 움직이는 정도를 -1~1로 말해 준다"],
            "상관계수 r — 점이 한 줄에 모일수록 1(또는 -1)에 가깝다",
            "같은 24개 점이 모양을 바꾸며 상관계수 r이 변하는 모습이다. r은 <b>함께 움직이는 정도</b>만 알려 줄 뿐 원인이 무엇인지는 말해 주지 않는다. 원인은 \"원인 후보\"로 좁혀 가며 따로 확인한다.",
            "점 24개가 흩어진 모양에서 오른쪽 아래로 모인 모양, 느슨한 오른쪽 위 모양, 한 줄에 가까운 오른쪽 위 모양으로 바뀌며 상관계수가 0, -0.9, 0.5, 0.95로 변하는 그림")
    f.l(px0, py0, px1, py0, "mg-ln")
    f.l(px0, py0, px0, py1, "mg-ln")
    f.t((px0 + px1) / 2, 256, "열 A", "mg-s mg-c mg-mu")
    f.t(px0 - 4, py1 - 8, "열 B", "mg-s mg-mu")
    for i in range(n):
        x0, y0 = P(x[i], states[0][i])
        gs = []
        stack = []
        cur = (x0, y0)
        a = f
        # 중첩 이동: state0 → 1 → 2 → 3
        opens = 0
        for s in (1, 2, 3):
            nx, ny = P(x[i], states[s][i])
            f.out.append(f'<g class="mg-slide{s}" style="--dx:{nx - cur[0]:.1f}px;--dy:{ny - cur[1]:.1f}px">')
            cur = (nx, ny)
            opens += 1
        f.c(x0, y0, 5.5, "mg-dot")
        f.out.append("</g>" * opens)
    labels = [
        (0, "mg-only0", "r ≈ 0.00", "관계가 거의 없다", "mg-tblue"),
        (1, "mg-only1", "r ≈ -0.90", "한쪽이 커지면 다른 쪽은 작아진다", "mg-tred"),
        (2, "mg-only2", "r ≈ 0.50", "대체로 함께 커지지만 느슨하다", "mg-torange"),
        (3, "mg-win35", "r ≈ 0.95", "함께 커지고, 거의 한 줄이다", "mg-tgreen"),
    ]
    for k, a, big, desc, col in labels:
        f.t(450, 110, big, f"mg-m mg-b {col}", a=a, style="font-size:30px")
        f.t(450, 142, desc, "mg-s", a=a)
    f.t(450, 190, "r이 클수록 한 줄에 가깝다", "mg-s mg-mu", a="mg-win45")
    f.t(450, 210, "(1에 가깝다 / -1에 가깝다 모두 강하다)", "mg-s mg-mu", a="mg-win45")
    return f


def baseline_fig():
    n = len(shop)
    bad = (shop["손님평가"] == -1).tolist()
    out = ((shop["냉동고온도_C"] < -20) | (shop["냉동고온도_C"] > -16)).tolist()
    nb, no = sum(bad), sum(out)
    nob = sum(1 for b, o in zip(bad, out) if b and o)
    base = round(nb / n * 100, 1)
    rate = round(nob / no * 100, 1)
    f = Fig("w8-baseline", 300,
            [f"① {n}일 중 손님 불만(-1)인 날이 {nb}일 → 기준선 {base}%", f"② 냉동고 온도가 범위 밖인 날 {no}일에 테두리를 둘렀다", f"③ 그 {no}일 중 불만인 날은 {nob}일 → {rate}%",
             "④ 두 비율을 막대로 나란히 놓는다", "⑤ 범위 밖에서 불만이 더 많다 → 원인 후보", "결과: 기준선과 비교해야 \"높다\"고 말할 수 있다"],
            "기준선과 비교하기 — 전체 비율 vs 조건 비율",
            f"빨간 칸은 손님 불만인 날, 오렌지 테두리는 냉동고 온도가 범위 밖인 날이다. 전체의 불만 비율(<b>기준선</b> {base}%)과 범위 밖 날의 불만 비율({rate}%)을 나란히 놓고 비교한다. 비교 결과는 \"원인 후보\"이지 원인이 확정된 것은 아니다.",
            f"30일 중 불만인 날은 빨간 칸, 냉동고 온도가 범위 밖인 날은 오렌지 테두리로 표시하고 기준선 {base}퍼센트와 범위 밖 불만 비율 {rate}퍼센트를 막대로 비교하는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week08_easy_weather_sales.csv)의 값")
    for i in range(n):
        r, c = divmod(i, 10)
        x, y = 30 + 36 * c, 52 + 44 * r
        f.r(x, y, 30, 34, "mg-box")
        if bad[i]:
            f.r(x, y, 30, 34, "mg-red", a="mg-from1")
        if out[i]:
            f.r(x - 3, y - 3, 36, 40, "mg-hl", a="mg-from2")
    f.t(30, 40, "날짜 순서대로 30일 (한 칸 = 하루)", "mg-s mg-mu")
    f.t(420, 66, f"불만 {nb}/{n} = {base}%  (기준선)", "mg-m mg-s mg-b mg-tred", a="mg-from1")
    f.t(420, 92, f"범위 밖 {no}일 중 불만 {nob}일 = {rate}%", "mg-m mg-s mg-b mg-torange", a="mg-from3")
    mx = 240
    f.t(420, 140, "기준선", "mg-s mg-b", a="mg-from4")
    f.r(420, 148, mx * base / 100, 24, "mg-red", a="mg-growx4")
    f.t(420 + mx * base / 100 + 8, 166, f"{base}%", "mg-m mg-s mg-b mg-tred", a="mg-from4")
    f.t(420, 196, "냉동고 온도 범위 밖인 날", "mg-s mg-b", a="mg-from4")
    f.r(420, 204, mx * rate / 100, 24, "mg-orange", a="mg-growx4")
    f.t(420 + mx * rate / 100 + 8, 222, f"{rate}%", "mg-m mg-s mg-b mg-torange", a="mg-from4")
    return f


FIGS = [
    ("기준선 —", baseline_fig()),
    ("산점도와 상관계수", corr_fig()),
]
