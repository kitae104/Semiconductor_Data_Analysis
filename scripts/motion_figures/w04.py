import os

import pandas as pd

from .lib import Fig

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cafe = pd.read_csv(os.path.join(BASE, "data", "weekly", "week04", "week04_easy_cafe_orders.csv"), encoding="utf-8-sig")


def table_fig():
    n_rows, n_cols = cafe.shape
    f = Fig("w4-table", 336,
            ["① cafe 표: 주문 한 건이 한 줄, 항목이 한 칸", "② 세로 한 줄 = 열(column): 같은 종류의 값", "③ 가로 한 줄 = 행(row): 기록 한 건",
             f"④ cafe.shape → ({n_rows}, {n_cols}) : {n_rows}행 {n_cols}열", f"⑤ cafe.columns → 열 이름 {n_cols}개", "결과: 표는 행(기록)과 열(항목)로 읽는다"],
            "표 읽기 — 행과 열, shape",
            f"CSV를 <code>read_csv()</code>로 읽으면 행과 열이 있는 표(DataFrame)가 된다. 그림은 <code>cafe.head()</code>처럼 앞 5행만 보여 주고, 전체는 {n_rows}행이다.",
            f"카페 주문 표에서 가격 열 한 줄을 열로, 주문 한 건의 가로 한 줄을 행으로 표시하고 shape가 {n_rows}행 {n_cols}열임을 보여 주는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week04_easy_cafe_orders.csv)의 값")
    cols = [("주문번호", 76), ("매장", 62), ("메뉴", 96), ("종류", 62), ("가격_KRW", 90), ("수량_count", 96), ("평가", 56)]
    x0, y0, rh = 30, 44, 26
    f.thead(x0, y0, cols, h=28)
    col_x = {}
    cx = x0
    for name, w in cols:
        col_x[name] = (cx, w)
        cx += w
    for i in range(5):
        r = cafe.iloc[i]
        vals = [r["주문번호"], r["매장"], r["메뉴"], r["종류"], f'{r["가격_KRW"]:,}', r["수량_count"], r["평가"]]
        f.trow(x0, y0 + 28 + rh * i, cols, vals, h=rh)
    f.t(x0 + 10, y0 + 28 + rh * 5 + 20, "⋮", "mg-b mg-mu")
    f.t(x0 + 36, y0 + 28 + rh * 5 + 20, f"(모두 {n_rows}행)", "mg-s mg-mu")
    # 열 강조
    cx_, cw = col_x["가격_KRW"]
    f.r(cx_ - 2, y0 - 2, cw + 4, 28 + rh * 5 + 4, "mg-hl", a="mg-only1")
    f.t(cx_ + cw / 2, y0 - 10, "열 (column)", "mg-s mg-b mg-c mg-torange", a="mg-only1")
    # 행 강조
    ry = y0 + 28 + rh * 2
    f.r(x0 - 2, ry - 2, sum(w for _, w in cols) + 4, rh + 4, "mg-hl", a="mg-only2")
    f.t(x0 + sum(w for _, w in cols) + 12, ry + 18, "행 = 주문 1건", "mg-s mg-b mg-torange", a="mg-only2")
    # shape, columns
    f.t(x0, 252, f"print(cafe.shape)   →   ({n_rows}, {n_cols})", "mg-m mg-b", a="mg-win35")
    f.t(x0 + 360, 252, f"{n_rows}행 × {n_cols}열", "mg-b mg-tblue", a="mg-win35")
    f.t(x0, 280, f"print(cafe.columns)   →   열 이름 {n_cols}개 (주문번호 … 평가)", "mg-m mg-b", a="mg-win45")
    return f


def select_fig():
    f = Fig("w4-select", 440,
            ["① cafe 표에서 필요한 열만 꺼낸다", "② cafe[\"가격_KRW\"] — 대괄호 한 겹: 열 하나", "③ 결과는 번호 붙은 한 줄 목록이다",
             "④ cafe[[\"메뉴\",\"가격_KRW\",\"평가\"]] — 대괄호 두 겹", "⑤ 안쪽 [ ]는 열 이름을 담은 리스트다", "결과: 한 겹은 열 하나, 두 겹은 여러 열의 표"],
            "열 고르기 — 대괄호 한 겹, 두 겹",
            "표의 위쪽에서 오렌지색 테두리가 고른 열이다. 아래 결과를 보면 한 겹은 <b>한 줄 목록</b>이, 두 겹은 <b>고른 열만 있는 작은 표</b>가 나온다.",
            "카페 주문 표에서 가격 열 하나를 고르면 한 줄 목록이 되고 메뉴, 가격, 평가 세 열을 고르면 작은 표가 되는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week04_easy_cafe_orders.csv)의 값")
    cols = [("메뉴", 100), ("종류", 64), ("가격_KRW", 90), ("수량_count", 96), ("평가", 56)]
    x0, y0, rh = 30, 40, 24
    f.thead(x0, y0, cols, h=26)
    xs, cx = [], x0
    for _, w in cols:
        xs.append(cx)
        cx += w
    rows = cafe.iloc[:5]
    for i, (_, r) in enumerate(rows.iterrows()):
        f.trow(x0, y0 + 26 + rh * i, cols, [r["메뉴"], r["종류"], f'{r["가격_KRW"]:,}', r["수량_count"], r["평가"]], h=rh)
    th = 26 + rh * 5
    f.r(xs[2] - 2, y0 - 2, cols[2][1] + 4, th + 4, "mg-hl", a="mg-win12")
    for k in (0, 2, 4):
        f.r(xs[k] - 2, y0 - 2, cols[k][1] + 4, th + 4, "mg-hl", a="mg-win34")
    # 결과 1: 한 줄 목록
    f.t(30, 214, 'cafe["가격_KRW"]', "mg-m mg-b", a="mg-from1")
    f.t(30, 232, "한 줄 목록(번호 + 값)", "mg-s mg-mu", a="mg-from1")
    with f.g("mg-from1"):
        for i in range(5):
            yy = 242 + 24 * i
            f.r(30, yy, 30, 24, "mg-gray"); f.t(45, yy + 17, str(i), "mg-m mg-s mg-c mg-mu")
            f.r(60, yy, 90, 24, "mg-box"); f.t(105, yy + 17, f'{rows.iloc[i]["가격_KRW"]:,}', "mg-s mg-c")
    # 결과 2: 작은 표
    f.t(260, 214, 'cafe[["메뉴", "가격_KRW", "평가"]]', "mg-m mg-b", a="mg-from3")
    f.t(260, 232, "고른 열만 있는 작은 표", "mg-s mg-mu", a="mg-from3")
    with f.g("mg-from3"):
        small = [("메뉴", 100), ("가격_KRW", 90), ("평가", 56)]
        f.thead(260, 242, small, h=24)
        for i in range(5):
            r = rows.iloc[i]
            f.trow(260, 266 + rh * i, small, [r["메뉴"], f'{r["가격_KRW"]:,}', r["평가"]], h=rh)
    return f


def filter_fig():
    n = len(cafe)
    mask = (cafe["종류"] == "커피").tolist()
    k = sum(mask)
    f = Fig("w4-filter", 130 + 22 * n,
            ["① cafe 표에서 종류가 커피인 주문만 찾고 싶다", "② cafe[\"종류\"] == \"커피\" → 행마다 True/False", "③ True인 행(초록)만 통과한다",
             "④ 통과한 행이 새 표 coffee가 된다", f"⑤ coffee.shape → ({k}, {cafe.shape[1]})", "결과: 조건이 True인 행만 남겨 새 표를 만든다"],
            "조건 검색 — True인 행만 남기기",
            f"<code>cafe[\"종류\"] == \"커피\"</code>는 행마다 True/False 줄을 만든다. 그 줄을 <code>cafe[ ... ]</code> 안에 넣으면 True인 행만 새 표로 나온다. 그림은 열 3개만 보여 준다.",
            f"카페 주문 {n}건 중 종류가 커피인 {k}건만 True가 되어 오른쪽 새 표로 옮겨 가는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week04_easy_cafe_orders.csv)의 값")
    cols = [("메뉴", 96), ("종류", 60), ("가격_KRW", 84)]
    mcol = [("종류 == 커피", 100)]
    x0, y0, rh = 20, 28, 22
    f.thead(x0, y0, cols, h=26)
    f.thead(x0 + 240, y0, mcol, h=26)
    rx = 430
    f.thead(rx, y0, cols, h=26)
    f.r(rx, y0 + 26, 240, rh * k, "mg-gray mg-dsh", a="mg-from3")
    f.t(rx, y0 - 8, "coffee (새 표)", "mg-m mg-s mg-b mg-tblue", a="mg-from3")
    j = 0
    for i in range(n):
        r = cafe.iloc[i]
        y = y0 + 26 + rh * i
        vals = [r["메뉴"], r["종류"], f'{r["가격_KRW"]:,}']
        f.trow(x0, y, cols, vals, h=rh)
        f.chip(x0 + 240, y, 100, rh, "True" if mask[i] else "False", "mg-green" if mask[i] else "mg-red", "mg-tgreen mg-b" if mask[i] else "mg-tred", a="mg-from1")
        if mask[i]:
            ty = y0 + 26 + rh * j
            with f.g("mg-from2"):
                with f.g("mg-slide3", rx - x0, ty - y):
                    f.trow(x0, y, cols, vals, h=rh, box="mg-green")
            j += 1
    f.t(rx, y0 + 26 + rh * k + 22, f"coffee.shape → ({k}, {cafe.shape[1]})", "mg-m mg-s mg-b", a="mg-from4")
    return f


def sort_fig():
    sel = cafe.iloc[[0, 1, 2, 3, 5]].reset_index(drop=True)
    order = sel["가격_KRW"].rank(ascending=False, method="first").astype(int) - 1
    f = Fig("w4-sort", 330,
            ["① 정렬 전: 주문 번호 순서로 놓여 있다", "② sort_values(\"가격_KRW\", ascending=False)", "③ 줄 전체가 가격이 큰 순서로 자리를 바꾼다",
             "④ 가장 비싼 행이 맨 위로 온다", "⑤ ascending=True면 작은 값부터 정렬한다", "결과: 한 열의 순서대로 행 전체가 따라 움직인다"],
            "정렬 — sort_values()",
            "정렬해도 <b>행은 통째로</b> 움직인다. 메뉴 이름과 가격이 짝을 유지한 채 자리만 바뀐다. 막대 길이는 가격이다. 그림은 가격이 서로 다른 5건만 뽑았다.",
            "카페 주문 5건이 가격이 큰 순서로 줄 전체가 자리를 바꿔 치즈케이크가 맨 위로 오는 그림",
            note="움직이는 그림 · 이 차시 예제 파일(week04_easy_cafe_orders.csv) 중 5건")
    rh = 38
    f.t(60, 34, "메뉴", "mg-s mg-b mg-mu"); f.t(210, 34, "가격_KRW", "mg-s mg-b mg-mu")
    f.t(520, 34, "", "mg-s")
    f.t(300, 34, "막대 길이 = 가격", "mg-s mg-mu")
    f.t(700, 34, "정렬 전: 주문 순서", "mg-s mg-b mg-e mg-tblue", a="mg-win01")
    f.t(700, 34, "정렬 후: 비싼 순서", "mg-s mg-b mg-e mg-torange", a="mg-win25")
    f.t(50, 270, 'cafe.sort_values("가격_KRW", ascending=False)', "mg-m mg-s mg-b", a="mg-from1")
    mx = sel["가격_KRW"].max()
    for i, r in sel.iterrows():
        y = 46 + rh * i
        dy = (order[i] - i) * rh
        with f.g("mg-slide2", 0, dy):
            f.r(50, y, 130, rh - 6, "mg-box"); f.t(115, y + 23, r["메뉴"], "mg-c")
            f.r(180, y, 100, rh - 6, "mg-blue"); f.t(230, y + 23, f'{r["가격_KRW"]:,}', "mg-m mg-c mg-b mg-tblue")
            f.r(290, y, 320 * r["가격_KRW"] / mx, rh - 6, "mg-orange")
    f.r(44, 40, 574, rh - 2, "mg-hl", a="mg-only3")
    return f


FIGS = [
    ("CSV 파일 읽기 — read_csv", table_fig()),
    ("열 고르기 — 대괄호", select_fig()),
    ("조건 검색 — 원하는", filter_fig()),
    ("정렬하기 — sort_values", sort_fig()),
]
