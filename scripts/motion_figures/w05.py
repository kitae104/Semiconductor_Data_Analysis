import os

import pandas as pd

from .lib import Fig

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
stu = pd.read_csv(os.path.join(BASE, "data", "weekly", "week05", "week05_easy_class_records.csv"), encoding="utf-8-sig")
COLS = [("이름", 70), ("반", 50), ("키_cm", 76), ("몸무게_kg", 86), ("수학점수_pt", 96)]


def cell(v):
    if pd.isna(v):
        return "NaN"
    if isinstance(v, float):
        return f"{v:.1f}"
    return str(v)


def dropna_fig():
    sub = stu.iloc[:9]
    bad = [i for i in range(len(sub)) if sub.iloc[i].isna().any()]
    na = stu.isna().sum()
    f = Fig("w5-dropna", 340,
            ["① 표에 빈칸(NaN)이 섞여 있다", "② isna().sum() → 열마다 빈칸 개수", "③ 빈칸이 든 행을 빨간색으로 표시했다",
             "④ dropna() → 빈칸이 든 행을 지운다", "⑤ 남은 행이 위로 붙는다", "결과: 빈칸(값 없음)은 0이 아니라서 세고 지운다"],
            "빈칸 세고 지우기 — isna(), dropna()",
            "빈칸은 pandas에서 <code>NaN</code>(값 없음)으로 읽힌다. <code>isna().sum()</code>이 열마다 빈칸 수를 세고, <code>dropna()</code>는 빈칸이 하나라도 든 행을 통째로 지운다. 그림은 앞 9행만 보여 준다.",
            "학생 기록 표에서 NaN이 든 세 행이 표시된 뒤 dropna로 지워지고 남은 행이 위로 붙는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week05_easy_class_records.csv) 앞 9행")
    x0, y0, rh = 20, 40, 24
    f.thead(x0, y0, COLS, h=26)
    shift = 0
    for i in range(len(sub)):
        y = y0 + 26 + rh * i
        vals = [cell(v) for v in sub.iloc[i]]
        if i in bad:
            with f.g("mg-win02"):
                f.trow(x0, y, COLS, vals, h=rh)
            with f.g("mg-win12"):
                boxes = ["mg-red" if v == "NaN" else "mg-orange" for v in vals]
                f.trow(x0, y, COLS, vals, h=rh, box=boxes, tcs=["mg-tred mg-b" if v == "NaN" else "" for v in vals])
            shift += 1
        else:
            with f.g("mg-slide3", 0, -rh * shift):
                f.trow(x0, y, COLS, vals, h=rh)
    # 오른쪽: isna().sum()
    f.t(440, 54, "students.isna().sum()", "mg-m mg-b", a="mg-from1")
    with f.g("mg-from1"):
        for j, (name, _) in enumerate(COLS):
            y = 68 + 26 * j
            n = int(na[name])
            f.r(440, y, 110, 24, "mg-gray"); f.t(450, y + 17, name, "mg-m mg-s")
            f.r(550, y, 50, 24, "mg-red" if n else "mg-box")
            f.t(575, y + 17, str(n), "mg-m mg-s mg-c mg-b" + (" mg-tred" if n else ""))
    f.t(440, 226, "빈칸이 든 행은 3개", "mg-b mg-tred", a="mg-win24")
    f.t(440, 226, "students.dropna() → 3개 행이 사라진다", "mg-m mg-s mg-b mg-tblue", a="mg-from3")
    return f


def dup_fig():
    f = Fig("w5-dup", 280,
            ["① 똑같은 행(박지호)이 두 번 들어 있다", "② duplicated() → 앞 행과 모든 칸이 같으면 True", "③ duplicated().sum() → 중복 행 1개",
             "④ drop_duplicates() → 두 번째 행을 지운다", "⑤ 처음 나온 행은 그대로 남는다", "결과: 같은 기록을 두 번 세지 않도록 하나만 남긴다"],
            "중복 행 찾고 지우기 — duplicated(), drop_duplicates()",
            "<code>duplicated()</code>는 <b>모든 칸이 같은</b> 행에 True를 붙이고, <code>drop_duplicates()</code>는 나중에 나온 같은 행을 지운다. 그림은 중복이 있는 앞뒤 행만 골라 보여 준다.",
            "학생 기록 표에서 박지호 행이 두 번 나타나 두 번째 행이 True로 표시된 뒤 삭제되는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week05_easy_class_records.csv) 중 일부 행")
    x0, y0, rh = 20, 40, 26
    f.thead(x0, y0, COLS, h=26)
    with f.g("mg-win12"):
        f.thead(x0 + 378, y0, [("duplicated()", 110)], h=26)
    idx = [0, 1, 2, None, 14]
    for k, i in enumerate(idx):
        y = y0 + 26 + rh * k
        if i is None:
            f.t(x0 + 20, y + 18, "⋮", "mg-b mg-mu")
            f.t(x0 + 60, y + 18, "(사이 행 생략)", "mg-s mg-mu")
            continue
        vals = [cell(v) for v in stu.iloc[i]]
        dup = i == 14
        if dup:
            with f.g("mg-win02"):
                f.trow(x0, y, COLS, vals, h=rh)
            with f.g("mg-win12"):
                f.chip(x0 + 378, y, 110, rh, "True", "mg-red", "mg-tred mg-b", size="")
        else:
            f.trow(x0, y, COLS, vals, h=rh)
            with f.g("mg-win12"):
                f.chip(x0 + 378, y, 110, rh, "False", "mg-box", "mg-mu", size="")
    f.r(x0 - 3, y0 + 26 + rh * 2 - 3, 378 + 6, rh + 6, "mg-hl", a="mg-win24")
    f.r(x0 - 3, y0 + 26 + rh * 4 - 3, 378 + 6, rh + 6, "mg-hl", a="mg-win23")
    f.t(520, y0 + 26 + rh * 2 + 18, "모든 칸이 같다", "mg-s mg-b mg-torange", a="mg-win24")
    f.arrow(500, y0 + 26 + rh * 2 + 22, 500, y0 + 26 + rh * 4 + 4, "mg-lnm", "mg-ah", a="mg-win23")
    f.t(x0, 236, "students.duplicated().sum()   →   1", "mg-m mg-b", a="mg-only2")
    f.t(x0, 236, "students.drop_duplicates()   →   첫 번째 행만 남는다", "mg-m mg-b mg-tblue", a="mg-from3")
    return f


def outlier_fig():
    rows = stu.dropna().drop_duplicates()
    hs = rows["키_cm"].tolist()
    mean_before = round(sum(hs) / len(hs), 1)
    ok = [h for h in hs if h <= 250]
    mean_after = round(sum(ok) / len(ok), 1)
    out = [h for h in hs if h > 250][0]

    def X(v):
        return 60 + (v - 150) * 460 / 30

    f = Fig("w5-outlier", 300,
            [f"① 키 {len(hs)}명을 cm 눈금 위에 점으로 놓았다", f"② 혼자 멀리 떨어진 점 {out:.1f} — 입력 실수로 보이는 튀는 값", "③ 범위 조건 키_cm > 250 으로 찾는다",
             "④ 조건에 걸린 행을 빼면 점이 한곳에 모인다", f"⑤ 평균이 {mean_before}에서 {mean_after}로 돌아온다", "결과: 튀는 값은 평균을 크게 흔든다"],
            "튀는 값 찾고 빼기 — 범위 조건",
            f"한 사람만 {out:.1f}cm로 적혀 있어 평균이 {mean_before}cm까지 올라갔다. <code>키_cm &gt; 250</code>처럼 <b>있을 수 없는 범위</b>를 조건으로 찾아 빼면 평균이 {mean_after}cm로 돌아온다. 눈금 중간의 // 표시는 \"여기서 건너뛰었다\"는 뜻이다.",
            f"키 값 점들이 150에서 180 사이에 모여 있고 {out:.1f}만 멀리 떨어져 있다가 제거되자 평균이 {mean_after}로 돌아오는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week05_easy_class_records.csv)의 값")
    ay = 170
    f.l(50, ay, 540, ay, "mg-ln")
    for v in (150, 160, 170, 180):
        f.l(X(v), ay - 4, X(v), ay + 4, "mg-ln")
        f.t(X(v), ay + 22, str(v), "mg-m mg-s mg-c mg-mu")
    f.l(560, ay, 700, ay, "mg-ln")
    f.t(550, ay + 5, "//", "mg-b mg-c mg-mu")
    f.t(40, ay + 44, "키_cm", "mg-m mg-s mg-mu")
    for v in hs:
        if v > 250:
            continue
        f.c(X(v), ay - 18, 8, "mg-dot")
    # 튀는 값
    with f.g("mg-win03"):
        f.c(650, ay - 18, 8, "mg-dotr")
    f.t(650, ay + 22, f"{out:.1f}", "mg-m mg-s mg-c mg-tred", a="mg-win03")
    f.r(630, ay - 40, 40, 44, "mg-hl", a="mg-win13")
    f.t(650, ay - 52, "튀는 값", "mg-s mg-b mg-c mg-tred", a="mg-win13")
    f.l(600, 60, 600, ay + 6, "mg-lnr mg-dsh", a="mg-win23")
    f.t(600, 52, "기준 250", "mg-s mg-b mg-c mg-tred", a="mg-win23")
    # 평균
    f.t(40, 52, f"정리 전 평균  {mean_before}", "mg-m mg-b mg-tred", a="mg-win03")
    f.t(40, 52, f"정리 후 평균  {mean_after}", "mg-m mg-b mg-tgreen", a="mg-win45")
    f.poly([(X(mean_after), ay - 6), (X(mean_after) - 8, ay - 22), (X(mean_after) + 8, ay - 22)], "mg-ahb", a="mg-win45")
    f.t(X(mean_after), ay - 62, "평균", "mg-s mg-b mg-c mg-tblue", a="mg-win45")
    return f


FIGS = [
    ("빈칸 세고 지우기", dropna_fig()),
    ("중복 행 찾고 지우기", dup_fig()),
    ("튀는 값 찾고 빼기", outlier_fig()),
]
