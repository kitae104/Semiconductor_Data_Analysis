from .lib import Fig


def lst():
    f = Fig("w2-list", 270,
            ["① 요일별 낮 기온 7개가 번호 붙은 칸에 들어 있다", "② [0] → 첫 번째 칸(월요일) 21.5 · 번호는 0부터", "③ [2] → 세 번째 칸(수요일) 30.5",
             "④ [-1] → 맨 뒤 칸(일요일) 23.5", "⑤ len(week_temps)는 칸의 개수 7", "결과: 번호(인덱스)로 칸을 찾는다. 번호는 0부터 센다"],
            "리스트 — 번호 붙은 칸",
            "<code>week_temps</code>는 칸 7개짜리 약통이다. 칸 번호는 <b>0부터</b> 시작하고, <code>-1</code>은 맨 뒤 칸이다. 오렌지색 테두리가 지금 꺼내는 칸이다.",
            "7칸짜리 리스트에서 0번, 2번, -1번 칸의 값을 꺼내고 len으로 칸 수 7을 세는 그림")
    days = ["월", "화", "수", "목", "금", "토", "일"]
    vals = [21.5, 23.0, 30.5, 24.0, 22.5, 25.0, 23.5]
    f.t(38, 32, "week_temps = [ … ]", "mg-m mg-b mg-tblue")
    for i, (d, v) in enumerate(zip(days, vals)):
        x = 38 + 92 * i
        f.t(x + 42, 66, d, "mg-s mg-c mg-mu")
        f.r(x, 74, 84, 50, "mg-blue")
        f.t(x + 42, 106, f"{v:.1f}", "mg-m mg-b mg-c mg-tblue")
        f.t(x + 42, 146, str(i), "mg-m mg-b mg-c mg-tblue")
        f.t(x + 42, 164, str(i - 7), "mg-m mg-s mg-c mg-mu")
    f.t(704, 146, "번호", "mg-s mg-e mg-mu")
    f.t(704, 164, "뒤에서", "mg-s mg-e mg-mu")
    for slot, rd in ((1, 0), (2, 2), (3, 6)):
        f.r(38 + 92 * rd - 4, 70, 92, 58, "mg-hl", a=f"mg-only{slot}")
    f.t(40, 208, 'print(week_temps[0])   →   21.5', "mg-m", a="mg-only1")
    f.t(40, 208, 'print(week_temps[2])   →   30.5', "mg-m", a="mg-only2")
    f.t(40, 208, 'print(week_temps[-1])   →   23.5', "mg-m", a="mg-only3")
    f.t(40, 208, 'print(len(week_temps))   →   7', "mg-m", a="mg-only4")
    f.l(38, 178, 38 + 92 * 6 + 84, 178, "mg-lnb", a="mg-only4")
    return f


def append():
    f = Fig("w2-append", 270,
            ["① cart에는 3칸이 있다 → len(cart)는 3", "② cart.append(\"사과\") — 새 값을 보낸다", "③ 값이 맨 뒤 칸에 들어간다",
             "④ 칸이 하나 늘어 4칸이 된다", "⑤ 다시 세면 len(cart)는 4", "결과: append()는 뒤에 붙이고 len()은 칸 수를 센다"],
            "append()와 len() — 뒤에 붙이고 칸 수 세기",
            "<code>append()</code>는 값을 맨 뒤 칸에 붙인다. 점선 칸이 새로 생길 자리이고, <code>len()</code>은 지금 칸이 몇 개인지 센다.",
            "장바구니 리스트에 우유, 빵, 계란이 들어 있고 사과가 위에서 내려와 네 번째 칸에 붙으면 len이 3에서 4로 바뀌는 그림")
    xs = [60 + 150 * i for i in range(4)]
    f.t(60, 30, 'cart = ["우유", "빵", "계란"]', "mg-m mg-b mg-tblue")
    for i, name in enumerate(["우유", "빵", "계란"]):
        f.r(xs[i], 100, 130, 54, "mg-blue")
        f.t(xs[i] + 65, 133, name, "mg-b mg-c mg-tblue")
        f.t(xs[i] + 65, 176, str(i), "mg-m mg-c mg-b mg-tblue")
    f.r(xs[3], 100, 130, 54, "mg-gray mg-dsh")
    f.t(xs[3] + 65, 133, "(빈자리)", "mg-s mg-c mg-mu", a="mg-win02")
    f.t(xs[3] + 65, 176, "3", "mg-m mg-c mg-b mg-tblue", a="mg-from3")
    f.t(300, 56, 'cart.append("사과")', "mg-m mg-b", a="mg-from1")
    with f.g("mg-from1"):
        with f.g("mg-slide2", 0, 74):
            f.chip(xs[3], 26, 130, 54, "사과", "mg-orange", "mg-torange mg-b", size="")
    f.t(60, 218, "len(cart)  →  3", "mg-m mg-b", a="mg-win01")
    f.t(60, 218, "len(cart)  →  4", "mg-m mg-b mg-torange", a="mg-win45")
    return f


def dct():
    f = Fig("w2-dict", 330,
            ["① student는 이름표(키)와 값 쌍으로 된 사물함", "② student[\"이름\"] → 이름표 '이름'을 찾아 값 '지민'", "③ student[\"나이\"] → 15",
             "④ student[\"반\"] → 3", "⑤ 없는 이름표 student[\"키\"] → KeyError", "결과: 번호가 아니라 이름표(키)로 값을 찾는다"],
            "딕셔너리 — 이름표로 찾는 사물함",
            "왼쪽 코드가 이름표를 부르면 같은 줄의 칸에서 값이 나온다. 이름표 목록에 없는 이름표(<code>\"키\"</code>)를 부르면 <code>KeyError</code>가 난다.",
            "student 사물함의 이름표 이름, 나이, 반에 값 지민, 15, 3이 들어 있고 코드가 이름표로 값을 꺼내며 없는 이름표는 KeyError가 나는 그림")
    rows = [("이름", '"지민"', "지민"), ("나이", "15", "15"), ("반", "3", "3"), ("키", "", "")]
    f.t(250, 40, "student = {", "mg-m mg-b mg-tblue")
    for i, (k, v, out) in enumerate(rows):
        y = 56 + 50 * i
        slot = i + 1
        an = f"mg-only{slot}" if i < 3 else "mg-win45"
        if i < 3:
            f.r(250, y, 90, 40, "mg-blue")
            f.t(295, y + 25, k, "mg-b mg-c mg-tblue")
            f.r(340, y, 130, 40, "mg-box")
            f.t(405, y + 25, v, "mg-m mg-c")
        else:
            f.r(250, y, 90, 40, "mg-gray mg-dsh", a="mg-win45")
            f.t(295, y + 25, "(없음)", "mg-s mg-c mg-mu", a="mg-win45")
        f.t(20, y + 26, f'student["{k}"]', "mg-m mg-b", a=an)
        f.arrow(190, y + 20, 246, y + 20, "mg-lnb", "mg-ahb", a=an)
        if i < 3:
            f.r(246, y - 4, 228, 48, "mg-hl", a=an)
            f.arrow(474, y + 20, 520, y + 20, "mg-lng", "mg-ah", a=an)
            f.t(530, y + 27, out, "mg-m mg-b mg-tgreen", a=an)
        else:
            f.t(300, y + 27, "KeyError", "mg-m mg-b mg-tred", a="mg-win45", style="")
    f.t(250, 268, "}", "mg-m mg-b mg-tblue")
    return f


def listdict():
    f = Fig("w2-listdict", 290,
            ["① friends는 딕셔너리 카드 3장이 든 리스트", "② friends[1] → 번호 1번 카드(두 번째 장)를 고른다", "③ 그 카드에서 [\"이름\"] 이름표로 값을 찾는다",
             "④ 결과는 '서준'", "⑤ len(friends)는 카드 장 수 3", "결과: 먼저 번호로 카드를, 다음에 이름표로 값을 찾는다"],
            "딕셔너리의 리스트 — 번호로 카드, 이름표로 값",
            "딕셔너리 한 개가 표의 한 행이고, 키가 열 이름이다. 리스트 번호로 한 행(카드)을 고른 뒤 이름표로 한 칸을 꺼낸다. 4차시의 표(Pandas)가 이 모양을 한 번에 다룬다.",
            "friends 리스트의 0, 1, 2번 카드 중 1번 카드를 고르고 그 카드의 이름 값 서준을 꺼내는 그림")
    people = [("지민", "15", "서울"), ("서준", "16", "부산"), ("하은", "15", "대전")]
    for i, (n, a_, d) in enumerate(people):
        x = 40 + 220 * i
        f.t(x + 90, 36, f"friends[{i}]", "mg-m mg-c mg-b mg-tblue")
        f.r(x, 46, 180, 100, "mg-box")
        for j, (k, v) in enumerate((("이름", n), ("나이", a_), ("동네", d))):
            yy = 54 + 30 * j
            f.r(x + 6, yy, 56, 26, "mg-blue")
            f.t(x + 34, yy + 18, k, "mg-s mg-c mg-tblue mg-b")
            f.r(x + 62, yy, 106, 26, "mg-gray")
            f.t(x + 115, yy + 18, v, "mg-s mg-c")
    f.r(256, 42, 188, 108, "mg-hl", a="mg-win13")
    f.r(262, 50, 170, 34, "mg-hl", a="mg-win23")
    f.t(40, 196, 'friends[1]   →   카드 한 장', "mg-m", a="mg-only1")
    f.t(40, 196, 'friends[1]["이름"]', "mg-m", a="mg-only2")
    f.t(40, 196, 'print(friends[1]["이름"])   →   서준', "mg-m mg-b mg-tgreen", a="mg-only3")
    f.t(40, 196, "print(len(friends))   →   3", "mg-m", a="mg-only4")
    f.l(40, 164, 640, 164, "mg-lnb", a="mg-only4")
    return f


FIGS = [
    ("리스트 — 번호", lst()),
    ("개수 세고", append()),
    ("딕셔너리 — 이름표", dct()),
    ("확인 — 딕셔너리의 리스트", listdict()),
]
