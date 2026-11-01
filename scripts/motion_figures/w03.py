from .lib import Fig


def ifelse():
    f = Fig("w3-ifelse", 330,
            ["① body_temp = 36.5 가 질문 앞에 선다", "② 36.0 ≤ 36.5 ≤ 37.5 → 참(True): 위쪽 길", "③ 실행 결과: 정상 체온입니다.",
             "④ 이번에는 body_temp = 38.2", "⑤ 37.5를 넘으니 거짓(False): else 쪽 길", "결과: 질문 하나로 두 길 중 한 길만 실행된다"],
            "if / else — 질문하고 갈림길 고르기",
            "값이 질문(조건)을 만나 <b>참</b>이면 if 쪽, <b>거짓</b>이면 else 쪽 길로 간다. 두 길 중 한 길만 실행된다. 36.5와 38.2가 차례로 지나간다.",
            "체온 36.5가 조건 36.0 이상 37.5 이하를 통과해 정상 체온 상자로 가고, 38.2는 조건에 걸려 다시 재 보세요 상자로 가는 갈림길 그림")
    f.poly([(300, 70), (410, 130), (300, 190), (190, 130)], "mg-blue")
    f.t(300, 124, "36.0 <= body_temp", "mg-m mg-s mg-c mg-tblue")
    f.t(300, 144, "<= 37.5 ?", "mg-m mg-s mg-c mg-tblue")
    f.chip(520, 50, 170, 50, "정상 체온입니다.", "mg-green", "mg-tgreen mg-b", size="")
    f.chip(520, 190, 170, 50, "다시 재 보세요.", "mg-orange", "mg-torange mg-b", size="")
    f.arrow(352, 100, 516, 76, "mg-lng", "mg-ah")
    f.t(380, 78, "참 (if)", "mg-s mg-tgreen mg-b")
    f.arrow(352, 160, 516, 214, "mg-lnr", "mg-ah")
    f.t(376, 200, "거짓 (else)", "mg-s mg-tred mg-b")
    f.arrow(120, 130, 188, 130, "mg-ln", "mg-ah")
    f.r(516, 46, 178, 58, "mg-hl", a="mg-only2")
    f.r(516, 186, 178, 58, "mg-hl", a="mg-only5")
    f.t(30, 100, "body_temp", "mg-m mg-s mg-mu")
    with f.g("mg-slide0", 245, 0):
        with f.g("mg-slide1", 175, -55):
            f.chip(20, 112, 70, 36, "36.5", "mg-ink", "mg-tw mg-m mg-b", size="")
    with f.g("mg-from3"):
        with f.g("mg-slide3", 245, 0):
            with f.g("mg-slide4", 175, 85):
                f.chip(20, 112, 70, 36, "38.2", "mg-ink", "mg-tw mg-m mg-b", size="")
    return f


def forloop():
    f = Fig("w3-for", 340,
            ["① scores에서 하나씩 꺼낸다: 72 → 80 이상? 아니오", "② 85 → 80 이상? 예 → pass_count 1", "③ 90 → 예 → pass_count 2",
             "④ 64 → 아니오 → pass_count 그대로 2", "⑤ 88 → 예 → pass_count 3", "결과: for가 끝나면 pass_count = 3"],
            "for — 하나씩 꺼내 개수 세기",
            "<code>for score in scores:</code>는 리스트에서 값을 하나씩 꺼내 <code>score</code>라 부르고, 들여쓴 줄을 매번 실행한다. 80점 이상일 때만 <code>pass_count</code>가 1 늘어난다.",
            "scores 리스트의 72, 85, 90, 64, 88을 화살표가 하나씩 가리키며 80점 이상이면 pass_count가 늘어나 최종 3이 되는 그림")
    scores = [72, 85, 90, 64, 88]
    for i, s in enumerate(scores):
        x = 40 + 104 * i
        f.r(x, 44, 90, 50, "mg-box")
        f.t(x + 45, 76, str(s), "mg-m mg-b mg-c mg-l")
        f.t(x + 45, 36, f"scores[{i}]", "mg-m mg-s mg-c mg-mu")
        if s >= 80:
            a = f"mg-from{i}" if i else ""
            f.r(x, 44, 90, 50, "mg-green", a=a)
            f.t(x + 45, 76, str(s), "mg-m mg-b mg-c mg-l mg-tgreen", a=a)
        f.poly([(x + 45, 104), (x + 36, 120), (x + 54, 120)], "mg-ahb", a=f"mg-only{i}")
    for i, s in enumerate(scores):
        ok = s >= 80
        f.t(40, 170, f"score = {s}", "mg-m mg-b", a=f"mg-only{i}")
        f.t(40, 200, f"{s} >= 80 ?  →  {'예 (True)' if ok else '아니오 (False)'}", "mg-m " + ("mg-tgreen" if ok else "mg-tred"), a=f"mg-only{i}")
    f.t(40, 170, "다 꺼냈다 — for 끝", "mg-b", a="mg-only5")
    counts = [0, 1, 2, 2, 3, 3]
    f.r(440, 150, 240, 100, "mg-orange")
    f.t(560, 176, "pass_count", "mg-m mg-b mg-c mg-torange")
    for i, c_ in enumerate(counts):
        f.t(560, 232, str(c_), "mg-m mg-b mg-c mg-torange", a=f"mg-only{i}", style="font-size:40px")
    return f


def function():
    f = Fig("w3-function", 320,
            ["① 판정 규칙에 judge_score라는 이름을 붙여 둔다", "② 85를 넣으면 규칙이 실행된다", "③ 결과로 '합격'이 돌아온다 (return)",
             "④ 같은 이름에 64를 넣는다", "⑤ 이번에는 '불합격'이 돌아온다", "결과: 이름만 부르면 같은 규칙을 몇 번이고 쓴다"],
            "함수 — 규칙에 이름을 붙여 다시 쓰기",
            "<code>def</code>로 규칙(점수가 80 이상이면 합격)에 이름을 붙여 두면, 값만 바꿔 넣어 같은 규칙을 몇 번이고 쓸 수 있다. 상자 안에서 규칙이 실행되고 <code>return</code>이 결과를 내보낸다.",
            "judge_score 상자에 85를 넣으면 합격이, 64를 넣으면 불합격이 나오는 입력과 출력 그림")
    f.r(250, 40, 220, 200, "mg-blue")
    f.t(360, 66, "judge_score(point)", "mg-m mg-b mg-c mg-tblue")
    f.t(360, 108, "point >= 80 이면", "mg-s mg-c")
    f.t(360, 128, 'return "합격"', "mg-m mg-s mg-c mg-tgreen")
    f.t(360, 162, "아니면", "mg-s mg-c")
    f.t(360, 182, 'return "불합격"', "mg-m mg-s mg-c mg-tred")
    f.t(150, 100, "입력", "mg-s mg-c mg-mu")
    f.t(580, 100, "출력", "mg-s mg-c mg-mu")
    f.arrow(130, 118, 248, 118, "mg-lnm", "mg-ah")
    f.arrow(472, 118, 590, 118, "mg-lnm", "mg-ah")
    f.arrow(130, 198, 248, 198, "mg-lnm", "mg-ah")
    f.arrow(472, 198, 590, 198, "mg-lnm", "mg-ah")
    f.r(246, 36, 228, 208, "mg-hl", a="mg-only1")
    f.r(246, 36, 228, 208, "mg-hl", a="mg-only4")
    with f.g("mg-from2"):
        f.chip(594, 100, 100, 36, "합격", "mg-green", "mg-tgreen mg-b", size="")
    with f.g("mg-from4"):
        f.chip(594, 180, 100, 36, "불합격", "mg-red", "mg-tred mg-b", size="")
    with f.g("mg-slide0", 90, 0):
        f.chip(20, 100, 60, 36, "85", "mg-ink", "mg-tw mg-m mg-b", size="")
    with f.g("mg-from3"):
        with f.g("mg-slide3", 90, 0):
            f.chip(20, 180, 60, 36, "64", "mg-ink", "mg-tw mg-m mg-b", size="")
    f.t(40, 270, 'judge_score(85)  →  "합격"        judge_score(64)  →  "불합격"', "mg-m mg-s mg-mu")
    return f


FIGS = [
    ("if/else — 둘 중", ifelse()),
    ("for — 하나씩", forloop()),
    ("함수 — 판정", function()),
]
