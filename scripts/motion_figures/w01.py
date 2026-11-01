from .lib import Fig


def types():
    f = Fig("w1-types", 270,
            ["① 상자 세 개에 값이 하나씩 들어 있다", "② type(cups) → int (정수)", "③ type(rating) → float (소수점 있는 수)",
             "④ type(menu) → str (글자, 따옴표로 감쌈)", "⑤ 종류에 따라 할 수 있는 일이 다르다", "결과: type()은 값의 종류 이름표를 알려 준다"],
            "값의 종류 확인하기 — type()",
            "상자 세 개를 차례로 <code>type()</code>에 넣어 본다. 숫자(int·float)는 계산할 수 있고, 글자(str)는 문장에 넣어 쓴다.",
            "cups 상자의 3은 int, rating 상자의 4.5는 float, menu 상자의 아메리카노는 str라는 종류 이름표가 차례로 붙는 그림")
    cols = [(130, "cups", "3", "int", "정수", "type(cups)"), (360, "rating", "4.5", "float", "소수점이 있는 수", "type(rating)"),
            (590, "menu", '"아메리카노"', "str", "글자(문자열)", "type(menu)")]
    for i, (cx, name, val, kind, desc, code) in enumerate(cols):
        f.t(cx, 36, name, "mg-m mg-b mg-c mg-tblue")
        f.r(cx - 80, 46, 160, 56, "mg-blue")
        f.t(cx, 82, val, "mg-m mg-l mg-b mg-c mg-tblue")
        f.r(cx - 86, 40, 172, 68, "mg-hl", a=f"mg-only{i + 1}")
        f.t(cx, 134, "print(" + code + ")", "mg-m mg-s mg-c", a=f"mg-only{i + 1}")
        f.arrow(cx, 108, cx, 150, "mg-lnb", "mg-ahb", a=f"mg-from{i + 1}")
        f.chip(cx - 50, 154, 100, 30, kind, "mg-orange", "mg-torange mg-m mg-b", a=f"mg-from{i + 1}", size="")
        f.t(cx, 204, desc, "mg-s mg-c mg-mu", a=f"mg-from{i + 1}")
    return f


def fstring():
    f = Fig("w1-fstring", 350,
            ["① 상자 menu와 cups에 값이 들어 있다", "② {menu} 자리에 menu 상자의 값이 들어간다", "③ {cups} 자리에는 cups 상자의 값이 들어간다",
             "④ 나머지 글자는 그대로 이어 붙는다", "⑤ f를 빼면 중괄호가 글자 그대로 나온다", "결과: f-string은 {이름} 자리에 상자 값을 채운다"],
            "f-string — 문장 속 빈칸에 값 채우기",
            "따옴표 앞 <code>f</code>가 있으면 <code>{menu}</code>, <code>{cups}</code> 자리에 같은 색 상자의 값이 들어간다. 맨 아래처럼 <code>f</code>를 빼먹으면 값이 아니라 중괄호 글자가 그대로 보인다.",
            "menu 상자의 아메리카노와 cups 상자의 3이 f-string의 중괄호 자리에 채워져 한 문장이 되고, f를 빼면 중괄호가 그대로 출력되는 그림")
    f.r(60, 20, 200, 48, "mg-orange"); f.t(72, 38, "menu", "mg-m mg-s mg-torange"); f.t(72, 58, '"아메리카노"', "mg-m mg-b mg-torange")
    f.r(300, 20, 120, 48, "mg-green"); f.t(312, 38, "cups", "mg-m mg-s mg-tgreen"); f.t(312, 58, "3", "mg-m mg-b mg-tgreen")
    f.r(60, 20, 200, 48, "mg-hl", a="mg-only1"); f.r(300, 20, 120, 48, "mg-hl", a="mg-only2")
    # 템플릿
    f.r(40, 96, 640, 46, "mg-box")
    f.t(56, 125, 'print(f"', "mg-m")
    f.chip(132, 106, 70, 26, "{menu}", "mg-orange", "mg-torange mg-m", size="")
    f.chip(210, 106, 70, 26, "{cups}", "mg-green", "mg-tgreen mg-m", size="")
    f.t(290, 125, '잔 주문이 들어왔습니다.")', "")
    f.r(128, 102, 78, 34, "mg-hl", a="mg-only1"); f.r(206, 102, 78, 34, "mg-hl", a="mg-only2")
    f.arrow(160, 68, 160, 100, "mg-lnm", "mg-ah", a="mg-only1"); f.arrow(360, 68, 245, 100, "mg-lnm", "mg-ah", a="mg-only2")
    # 출력
    f.r(40, 172, 640, 46, "mg-gray"); f.t(52, 164, "출력", "mg-s mg-mu mg-b")
    f.t(60, 202, "아메리카노", "mg-b mg-torange", a="mg-from1")
    f.t(146, 202, "3", "mg-b mg-tgreen", a="mg-from2")
    f.t(157, 202, "잔 주문이 들어왔습니다.", "", a="mg-from3")
    # f 없는 경우
    f.t(40, 252, 'f 없이 print("{menu} {cups}잔 …")', "mg-m mg-s mg-mu", a="mg-from4")
    f.r(40, 260, 640, 36, "mg-red", a="mg-from4"); f.t(60, 284, "{menu} {cups}잔 주문이 들어왔습니다.", "mg-m mg-tred", a="mg-from4")
    return f


def oflow():
    f = Fig("w1-oflow", 260,
            ["① File 위젯이 표 파일을 읽어 온다", "② 연결선을 따라 표가 Data Table로 흘러간다", "③ Data Table: 표 그대로 펼쳐 본다",
             "④ 이어서 Distributions로 흘러간다", "⑤ Distributions: 열의 값을 막대로 본다", "결과: 선을 이으면 표가 다음 위젯으로 흘러간다"],
            "Orange3 — 위젯을 선으로 이으면 표가 흘러간다",
            "위젯은 한 가지 일을 하는 상자이고, 선은 표가 지나가는 길이다. 표(작은 격자)가 선을 따라 흘러가면서 위젯마다 다른 모습으로 보인다. 선을 끊으면 흐름도 멈춘다.",
            "File, Data Table, Distributions 세 위젯이 선으로 이어져 있고 작은 표가 File에서 Data Table로, 다시 Distributions로 이동하는 그림")
    xs = [60, 290, 520]
    names = [("File", "표 파일을 읽는다"), ("Data Table", "표로 보여 준다"), ("Distributions", "막대로 보여 준다")]
    for x, (n, d) in zip(xs, names):
        f.r(x, 70, 140, 64, "mg-box")
        f.t(x + 70, 98, n, "mg-b mg-c mg-m")
        f.t(x + 70, 120, d, "mg-s mg-c mg-mu")
    for x1, x2 in ((200, 290), (430, 520)):
        f.l(x1, 102, x2 - 10, 102, "mg-lnb mg-flow")
        f.poly([(x2, 102), (x2 - 11, 96), (x2 - 11, 108)], "mg-ahb")
    f.r(60, 70, 140, 64, "mg-hl", a="mg-only0"); f.r(290, 70, 140, 64, "mg-hl", a="mg-only2"); f.r(520, 70, 140, 64, "mg-hl", a="mg-only4")
    # 표 조각(작은 격자)이 연결선을 따라 한 칸씩 흘러간다
    def packet(x):
        f.r(x, 86, 30, 32, "mg-orange")
        f.l(x, 96.7, x + 30, 96.7, "mg-ln"); f.l(x, 107.3, x + 30, 107.3, "mg-ln")
        f.l(x + 15, 86, x + 15, 118, "mg-ln")
    with f.g("mg-slide1", 44, 0):
        packet(204)
    with f.g("mg-from3"):
        with f.g("mg-slide3", 44, 0):
            packet(434)
    # 설명
    f.t(130, 170, "열과 행으로 된 표", "mg-s mg-c mg-mu")
    f.t(360, 170, "행·열 개수 확인", "mg-s mg-c mg-mu", a="mg-from2")
    f.t(590, 170, "값이 몇 개씩인지 확인", "mg-s mg-c mg-mu", a="mg-from4")
    return f


def overview():
    """모래에서 칩까지 — 6단계 한눈에 보기."""
    f = Fig("w1-sand2chip", 262,
            ["1. 원료는 모래 속의 규소(실리콘)다", "2. 규소를 녹여 굳혀 기둥(잉곳)을 만든다", "3. 기둥을 얇게 썰어 웨이퍼 원판을 만든다",
             "4. 웨이퍼 위에 회로를 층층이 쌓는다 (8대 공정)", "5. 웨이퍼를 잘라 칩(다이)을 떼어 낸다", "결과: 포장하면 우리가 아는 반도체 칩이 된다"],
            "모래에서 칩까지 — 여섯 단계 한눈에 보기",
            "단계가 하나씩 이어 붙으며 모래가 칩이 되는 길을 보여 준다. 아래 '공정 지도'의 ①은 이 그림의 모래~웨이퍼, ②~⑥은 회로 쌓기, ⑦~⑧은 검사와 칩 자르기·포장에 해당한다. 전기 검사(EDS)는 자르기 전에 한다(교육용 단순화).",
            "모래, 실리콘 기둥(잉곳), 얇은 웨이퍼 원판, 회로가 쌓인 웨이퍼, 잘라 낸 칩, 포장된 칩이 화살표로 이어지는 그림")
    cxs = [70, 186, 302, 418, 534, 650]
    names = [("모래", "원료는 규소"), ("잉곳", "굳힌 실리콘 기둥"), ("웨이퍼", "얇게 썬 원판"),
             ("회로 쌓기", "층층이 회로를"), ("칩 자르기", "다이를 떼어 냄"), ("패키지", "껍데기에 포장")]
    f.raw('<defs><clipPath id="w1-sand-clip"><circle cx="418" cy="80" r="37"/></clipPath></defs>')
    for i, cx in enumerate(cxs):
        a = f"mg-from{i}" if i else ""
        with f.g(a):
            if i:
                f.arrow(cx - 76, 80, cx - 44, 80, "mg-ln", "mg-ah")
            if i == 0:
                f.poly([(cx - 36, 110), (cx - 8, 64), (cx + 6, 76), (cx + 36, 110)], "mg-orange")
                for dx, dy in ((-18, 100), (-4, 92), (12, 102), (24, 106), (0, 78)):
                    f.c(cx + dx, dy, 2.6, "mg-doto")
            elif i == 1:
                f.path(f"M{cx - 26},60 L{cx - 26},104 A26,8 0 0 0 {cx + 26},104 L{cx + 26},60 Z", "mg-gray")
                f.raw(f'<ellipse cx="{cx}" cy="60" rx="26" ry="8" class="mg-gray"/>')
            elif i == 2:
                for k in (3, 2, 1, 0):
                    f.raw(f'<ellipse cx="{cx}" cy="{66 + k * 13}" rx="36" ry="9" class="mg-gray"/>')
            elif i == 3:
                f.c(cx, 80, 38, "mg-blue")
                f.raw('<g clip-path="url(#w1-sand-clip)">')
                for g in range(-3, 4):
                    f.l(cx + g * 12, 40, cx + g * 12, 120, "mg-lnm")
                    f.l(cx - 40, 80 + g * 12, cx + 40, 80 + g * 12, "mg-lnm")
                f.raw("</g>")
            elif i == 4:
                for r in range(3):
                    for c in range(3):
                        f.r(cx - 32 + c * 22, 50 + r * 22, 18, 18, "mg-green")
                f.r(cx + 8, 72, 18, 18, "mg-hl")
            else:
                f.r(cx - 22, 58, 44, 44, "mg-ink")
                f.r(cx - 9, 71, 18, 18, "mg-box")
                for k in range(4):
                    f.r(cx - 30, 62 + k * 10, 8, 5, "mg-box")
                    f.r(cx + 22, 62 + k * 10, 8, 5, "mg-box")
            f.t(cx, 142, names[i][0], "mg-b mg-c")
            f.t(cx, 162, names[i][1], "mg-s mg-c mg-mu")
        f.r(cx - 54, 30, 108, 146, "mg-hl", a=f"mg-only{i}")
    f.t(360, 200, "원료  →  재료(웨이퍼)  →  회로 만들기  →  완성품", "mg-s mg-c mg-mu")
    return f


STEP_NAMES = ["웨이퍼", "산화", "포토", "식각", "증착·주입", "금속 배선", "EDS", "패키징"]
STEP_TEXT = [
    ("① 웨이퍼 제조", ["실리콘 덩어리를", "얇고 둥글게 썬다.", "피자 도우 만들기"]),
    ("② 산화", ["표면을 산소와 반응", "시켜 얇은 보호막", "(산화막)을 키운다."]),
    ("③ 포토", ["빛으로 회로 그림을", "웨이퍼에 옮긴다.", "사진 인화와 비슷"]),
    ("④ 식각", ["그림 밖 필요 없는", "부분을 깎아 낸다.", "판화 새기기와 비슷"]),
    ("⑤ 증착 / 이온주입", ["얇은 막을 한 겹 쌓고", "알갱이(이온)를 넣어", "전기 성질을 바꾼다."]),
    ("⑥ 금속 배선", ["금속 선을 깔아 회로", "사이를 잇는다.", "②~⑥은 층마다 되풀이"]),
    ("⑦ EDS 전기 검사", ["자르기 전, 칩마다", "전기를 넣어 본다.", "초록 합격 · 빨강 불합격"]),
    ("⑧ 패키징", ["칩을 잘라 보호", "껍데기에 담고", "바깥과 연결한다."]),
]
GAPS = [(430, 476), (544, 590)]   # 회로 그림에서 열리는 자리(오른쪽 단면 그림 공통)


def _base(f):
    f.r(350, 222, 310, 32, "mg-gray")
    f.t(356, 243, "실리콘 기판", "mg-s mg-mu")


def _blocks(f):
    for x1, x2 in ((350, 430), (476, 544), (590, 660)):
        f.r(x1, 208, x2 - x1, 14, "mg-blue")


def _scene(f, k):
    if k == 0:
        f.c(505, 172, 58, "mg-gray")
        f.l(486, 229, 524, 229, "mg-lnm")
        f.t(505, 262, "위에서 본 웨이퍼", "mg-s mg-c mg-mu")
    elif k == 1:
        _base(f)
        f.r(350, 208, 310, 14, "mg-blue")
        for x in (390, 450, 510, 570, 630):
            f.c(x, 150, 4, "mg-dotm")
            f.c(x + 20, 172, 4, "mg-dotm")
        for x in (450, 570):
            f.arrow(x, 158, x, 202, "mg-lnm", "mg-ah")
        f.t(505, 133, "산소", "mg-s mg-c mg-mu")
        f.t(505, 200, "산화막", "mg-s mg-c mg-tblue mg-b")
    elif k == 2:
        _base(f)
        f.r(350, 208, 310, 14, "mg-blue")
        f.r(350, 194, 310, 14, "mg-orange")
        f.t(352, 190, "빛에 반응하는 막", "mg-s mg-torange")
        for x1, x2 in ((350, 430), (476, 544), (590, 660)):
            f.r(x1, 150, x2 - x1, 8, "mg-ink")
        f.t(352, 144, "마스크(회로 그림 판)", "mg-s mg-mu")
        for x in (453, 567):
            f.r(x - 23, 194, 46, 14, "mg-red")
            f.arrow(x, 160, x, 192, "mg-lnb mg-flow", "mg-ahb")
        f.t(505, 128, "빛", "mg-s mg-c mg-tblue mg-b")
    elif k == 3:
        _base(f)
        _blocks(f)
        for x1, x2 in GAPS:
            f.r(x1, 208, x2 - x1, 14, "mg-ln mg-dsh")
            f.t((x1 + x2) / 2, 198, "깎임", "mg-s mg-c mg-tred mg-b")
        f.t(505, 160, "회로 그림대로 남긴 부분(파랑)과", "mg-s mg-c mg-mu")
        f.t(505, 178, "깎아 낸 자리(점선)", "mg-s mg-c mg-mu")
    elif k == 4:
        _base(f)
        _blocks(f)
        for x1, x2 in GAPS:
            cx = (x1 + x2) / 2
            f.r(x1 + 2, 198, x2 - x1 - 4, 24, "mg-green")
            f.arrow(cx, 132, cx, 192, "mg-lnb", "mg-ahb")
            for dx in (-12, 0, 12):
                f.c(cx + dx, 234, 2.8, "mg-dot")
                f.c(cx + dx / 2, 245, 2.8, "mg-dot")
            f.t(cx, 126, "이온", "mg-s mg-c mg-tblue mg-b")
        f.t(505, 190, "증착(막 쌓기)", "mg-s mg-c mg-tgreen mg-b")
    elif k == 5:
        _base(f)
        _blocks(f)
        for x1, x2 in GAPS:
            f.r(x1 + 2, 198, x2 - x1 - 4, 24, "mg-green")
        f.r(440, 178, 140, 14, "mg-orange")
        f.r(445, 192, 34, 8, "mg-orange")
        f.r(541, 192, 34, 8, "mg-orange")
        f.t(510, 172, "금속 선(배선)", "mg-s mg-c mg-torange mg-b")
        f.r(350, 128, 310, 22, "mg-ln mg-dsh")
        f.t(505, 144, "다음 층도 같은 방식으로 쌓는다", "mg-s mg-c mg-mu")
    elif k == 6:
        f.c(505, 172, 58, "mg-gray")
        for i in range(-3, 4):
            for j in range(-3, 4):
                if (i * 14) ** 2 + (j * 14) ** 2 <= 46 ** 2:
                    bad = (i * 5 + j * 3 + 7) % 9 == 0
                    f.r(505 + i * 14 - 5.5, 172 + j * 14 - 5.5, 11, 11, "mg-red" if bad else "mg-green")
        f.l(594, 150, 522, 155, "mg-ln")
        f.c(520, 155, 3.5, "mg-dotm")
        f.t(596, 146, "탐침(전기 넣기)", "mg-s mg-mu")
        f.r(600, 206, 11, 11, "mg-green")
        f.t(616, 216, "합격", "mg-s")
        f.r(600, 228, 11, 11, "mg-red")
        f.t(616, 238, "불합격", "mg-s")
        f.t(505, 262, "웨이퍼 위 칩을 하나씩 검사", "mg-s mg-c mg-mu")
    else:
        f.r(372, 172, 28, 28, "mg-green")
        f.t(386, 216, "칩(다이)", "mg-s mg-c")
        f.arrow(412, 186, 458, 186, "mg-ln", "mg-ah")
        f.r(470, 150, 90, 70, "mg-ink")
        for q in range(5):
            f.r(460, 156 + q * 13, 10, 6, "mg-box")
            f.r(560, 156 + q * 13, 10, 6, "mg-box")
        f.t(515, 191, "칩", "mg-tw mg-b mg-c mg-l")
        f.t(515, 242, "패키지(보호 껍데기)", "mg-s mg-c")
        f.t(626, 186, "완성", "mg-b mg-tgreen mg-c")


def process8():
    """8대 공정 — 단계가 하나씩 진행되며 웨이퍼 단면이 바뀌는 모션 그래픽."""
    narr = ["① 실리콘 덩어리를 얇고 둥글게 썰어 웨이퍼를 만든다", "② 웨이퍼 표면에 얇은 산화막(보호막)을 키운다",
            "③ 빛을 비춰 회로 그림을 웨이퍼에 옮긴다", "④ 그림대로 필요 없는 부분을 깎아 낸다",
            "⑤ 막을 한 겹 쌓고, 이온을 넣어 전기 성질을 바꾼다", "⑥ 금속 선을 깔아 회로를 잇는다 (②~⑥ 되풀이)",
            "⑦ 자르기 전에 칩마다 전기로 검사한다", "⑧ 칩을 잘라 포장한다 — 반도체 칩 완성"]
    f = Fig("w1-process8", 316, narr,
            "공정 지도 — 8단계가 하나씩 진행",
            "위쪽 단계 표시가 ①부터 ⑧까지 하나씩 켜지고, 아래 그림이 그 단계의 웨이퍼 모습(단면)으로 바뀐다. 파랑은 전공정, 초록은 후공정이다. ②~⑥은 회로를 한 층 쌓을 때마다 되풀이한다(교육용 단순화). 전공정·후공정 분류는 자료마다 조금 다를 수 있다.",
            "반도체 8대 공정을 웨이퍼 제조, 산화, 포토, 식각, 증착과 이온주입, 금속 배선, EDS 전기 검사, 패키징 순서로 하나씩 보여 주고, 각 단계마다 웨이퍼 단면 또는 위에서 본 모습이 바뀌는 그림. ②~⑥은 층마다 되풀이한다")
    f.c(32, 9, 5, "mg-dot")
    f.t(42, 14, "전공정 ①~⑥ — 웨이퍼 위에 회로를 만든다", "mg-s")
    f.c(404, 9, 5, "mg-dotg")
    f.t(414, 14, "후공정 ⑦~⑧ — 검사하고 포장한다", "mg-s")
    xs = [29 + k * 84 for k in range(8)]
    for k, x in enumerate(xs):
        f.r(x, 46, 74, 54, "mg-box")
        f.r(x, 46, 74, 54, "mg-blue" if k < 6 else "mg-green", a=f"mg8-from{k}" if k else "")
        f.t(x + 37, 68, "①②③④⑤⑥⑦⑧"[k], "mg-c mg-b mg-l")
        f.t(x + 37, 90, STEP_NAMES[k], "mg-c mg-s")
        f.r(x - 3, 43, 80, 60, "mg-hl", a=f"mg8-only{k}")
        if k:
            f.poly([(x - 8, 67), (x - 8, 79), (x - 2, 73)], "mg-ah", a=f"mg8-from{k}")
    c2, c6 = xs[1] + 37, xs[5] + 37
    with f.g("mg8-from5"):
        f.path(f"M{c6},46 L{c6},37 L{c2},37 L{c2},45", "mg-ln mg-dsh")
        f.poly([(c2, 46), (c2 - 5, 38), (c2 + 5, 38)], "mg-ah")
        f.t((c2 + c6) / 2, 32, "②~⑥ 층마다 되풀이", "mg-s mg-c mg-torange mg-b")
    f.r(24, 112, 672, 160, "mg-box")
    f.l(330, 124, 330, 260, "mg-lnm")
    for k, (title, lines) in enumerate(STEP_TEXT):
        with f.g(f"mg8-only{k}"):
            f.t(44, 142, title, "mg-b mg-l")
            for j, ln in enumerate(lines):
                f.t(44, 170 + j * 22, ln, "mg-mu" if j == 2 else "")
            _scene(f, k)
    return f


FIGS = [
    ("자료형 —", types()),
    ("print()와 f-string", fstring()),
    ("Orange3로 무엇을", oflow()),
    ("모래에서 칩까지", overview()),
    ("공정 지도 — 칩이 만들어지는 8단계", process8()),
]
