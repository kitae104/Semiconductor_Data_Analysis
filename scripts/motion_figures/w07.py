import os
import random

import pandas as pd

from .lib import Fig

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
quiz = pd.read_csv(os.path.join(BASE, "data", "weekly", "week07", "week07_easy_quiz_results.csv"), encoding="utf-8-sig")
quiz["정답"] = quiz["정답여부"] == 1
NOTE = "움직이는 그림 · 이 차시 예제 파일(week07_easy_quiz_results.csv)의 값"


def ratio_fig():
    n, k = len(quiz), int(quiz["정답"].sum())
    rate = k / n
    classes = list(dict.fromkeys(quiz["반"]))
    per = n // len(classes)
    f = Fig("w7-ratio", 300,
            [f"① 쪽지시험 {n}문항의 결과를 한 칸씩 늘어놓았다", "② 정답은 초록, 오답은 빨강으로 칠한다", f"③ 정답 {k}개 ÷ 전체 {n}개 = {rate:.2f}",
             f"④ {rate:.2f} × 100 = {rate * 100:.1f} (%)", "⑤ 수율도 같은 식: 합격 웨이퍼 ÷ 만든 웨이퍼", f"결과: 정답률 = 정답 ÷ 전체 × 100 = {rate * 100:.1f}%"],
            "비율 — 무엇 중에 무엇인가",
            "비율은 <b>(조건에 맞는 것의 수) ÷ (전체 수)</b>다. 정답률의 분모는 전체 문항이다. 반도체 수율도 분모는 만든 웨이퍼 전체, 분자는 합격한 웨이퍼다. 파이썬에서는 True/False 열에 <code>.mean()</code>을 쓰면 한 번에 계산된다.",
            f"쪽지시험 {n}문항 중 정답 {k}개가 초록 칸으로 표시되고 정답을 전체로 나눠 {rate * 100:.1f}퍼센트를 구하는 그림", note=NOTE)
    for ri, cl in enumerate(classes):
        y = 50 + 52 * ri
        f.t(20, y + 25, cl, "mg-b mg-mu")
        sub = quiz[quiz["반"] == cl]
        for j, (_, r) in enumerate(sub.iterrows()):
            x = 70 + 38 * j
            f.r(x, y, 32, 36, "mg-gray")
            f.r(x, y, 32, 36, "mg-green" if r["정답"] else "mg-red")
    # 처음에는 회색이었다가 색이 칠해진다: 회색 칸을 위에 덧그려 slot0에서만 보이게 한다
    for ri, cl in enumerate(classes):
        y = 50 + 52 * ri
        for j in range(per):
            f.r(70 + 38 * j, y, 32, 36, "mg-gray", a="mg-only0")
    f.r(432, 46, 270, 150, "mg-box")
    f.t(446, 74, "정답", "mg-s mg-mu"); f.t(494, 74, "■", "mg-tgreen"); f.t(512, 74, "초록", "mg-s mg-mu")
    f.t(570, 74, "오답", "mg-s mg-mu"); f.t(618, 74, "■", "mg-tred"); f.t(636, 74, "빨강", "mg-s mg-mu")
    f.t(446, 112, f"정답 {k}개  /  전체 {n}개", "mg-m mg-b", a="mg-from2")
    f.t(446, 142, f"{k} ÷ {n} = {rate:.2f}", "mg-m mg-b mg-tblue", a="mg-from3")
    f.t(446, 172, f"{rate:.2f} × 100 = {rate * 100:.1f} %", "mg-m mg-b mg-torange", a="mg-from4")
    return f


def groupby_fig():
    n = len(quiz)
    classes = list(dict.fromkeys(quiz["반"]))
    rates = quiz.groupby("반")["정답"].agg(["sum", "count", "mean"])
    f = Fig("w7-groupby", 300,
            [f"① {n}문항이 반 구분 없이 섞여 있다", "② groupby(\"반\") — 같은 반끼리 모은다", f"③ {classes[0]}: 정답 {int(rates.loc[classes[0], 'sum'])}/{int(rates.loc[classes[0], 'count'])} → {rates.loc[classes[0], 'mean'] * 100:.1f}%",
             f"④ {classes[1]}: 정답 {int(rates.loc[classes[1], 'sum'])}/{int(rates.loc[classes[1], 'count'])} → {rates.loc[classes[1], 'mean'] * 100:.1f}%",
             f"⑤ {classes[2]}: 정답 {int(rates.loc[classes[2], 'sum'])}/{int(rates.loc[classes[2], 'count'])} → {rates.loc[classes[2], 'mean'] * 100:.1f}%", "결과: groupby는 묶음마다 같은 계산을 한 번에 한다"],
            "groupby — 묶어서 비교하기",
            "칸 안의 글자는 반이고, 초록은 정답, 빨강은 오답이다. <code>groupby(\"반\")</code>이 같은 반끼리 모으고, 뒤의 <code>[\"정답\"].mean()</code>이 묶음마다 정답률을 계산한다.",
            "섞여 있던 24문항이 A반, B반, C반으로 나뉘어 모이고 반마다 정답률이 계산되는 그림", note=NOTE)
    rnd = random.Random(7)
    order = list(range(n))
    rnd.shuffle(order)
    # 원래 행 i가 pile 위치 order.index(i)에 놓인다
    pos = {row: p for p, row in enumerate(order)}
    seen = {c: 0 for c in classes}
    for i in range(n):
        r = quiz.iloc[i]
        g = classes.index(r["반"])
        j = seen[r["반"]]
        seen[r["반"]] += 1
        p = pos[i]
        px, py = 30 + 36 * (p % 6), 50 + 36 * (p // 6)
        gx, gy = 372 + 36 * j, 56 + 62 * g
        with f.g("mg-slide1", gx - px, gy - py):
            f.r(px, py, 30, 30, "mg-green" if r["정답"] else "mg-red")
            f.t(px + 15, py + 20, r["반"][0], "mg-b mg-c mg-s")
    for g, cl in enumerate(classes):
        f.t(330, 56 + 62 * g + 20, cl, "mg-b mg-c mg-s", a="mg-from1")
        f.t(668, 56 + 62 * g + 20, f"{rates.loc[cl, 'mean'] * 100:.1f}%", "mg-m mg-b mg-torange mg-s", a=f"mg-from{g + 2}")
    f.t(30, 42, "섞여 있는 문항", "mg-s mg-mu", a="mg-win01")
    return f


def pareto_fig():
    wrong = quiz[quiz["정답여부"] == -1]["오답유형"].value_counts()
    tot = int(wrong.sum())
    f = Fig("w7-pareto", 270,
            [f"① 틀린 문항(-1) {tot}개만 고른다", "② 오답유형별로 센다 — value_counts()", "③ 많은 순서로 줄을 세운다",
             "④ 가장 긴 줄이 먼저 고칠 후보", "⑤ 막대그래프로 그리면 한눈에 보인다", "결과: 많은 것부터 고치면 효과가 가장 크다"],
            "오답 유형 줄 세우기 — 무엇부터 고칠까",
            "틀린 문항 하나가 칸 하나이고, 같은 유형끼리 줄을 이루면 그 길이가 막대 길이다. <code>value_counts()</code>는 이미 많은 순서로 세어 준다.",
            "오답 6개가 오답유형별로 줄을 이루고 계산 실수가 가장 긴 줄로 맨 위에 놓이는 그림", note=NOTE)
    for i, (name, v) in enumerate(wrong.items()):
        y = 46 + 56 * i
        f.t(20, y + 26, name, "mg-b", a=f"mg-from{i + 1}")
        for j in range(int(v)):
            f.r(190 + 44 * j, y, 38, 38, "mg-red", a=f"mg-from{i + 1}")
        f.t(190 + 44 * v + 6, y + 26, f"{int(v)}건", "mg-m mg-b mg-tred", a=f"mg-from{i + 1}")
    f.r(12, 40, 400, 50, "mg-hl", a="mg-win45")
    f.t(430, 76, "먼저 고칠 후보", "mg-b mg-torange", a="mg-win45")
    return f


FIGS = [
    ("수율과 정답률", ratio_fig()),
    ("groupby —", groupby_fig()),
    ("오답 유형", pareto_fig()),
]
