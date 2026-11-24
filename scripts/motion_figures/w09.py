from .lib import Fig

TEST_IDX = [3, 9, 12, 17]


def split_fig():
    f = Fig("w9-split", 350,
            ["① 지난 기록 20건이 한 줄로 있다", "② 무작위로 20%(4건)를 시험용으로 정한다", "③ 16건은 학습용, 4건은 시험용으로 갈라 둔다",
             "④ 학습용으로만 규칙을 찾는다 (fit)", "⑤ 시험용으로 채점한다 (accuracy_score)", "결과: 학습에 쓴 기록과 채점에 쓰는 기록을 따로 둔다"],
            "학습용·시험용 나누기 — 연습문제와 모의고사",
            "모델이 이미 본 기록으로 채점하면 점수가 부풀려진다. 그래서 기록 일부(여기서는 20%)를 <b>시험용</b>으로 떼어 두고, 나머지 <b>학습용</b>으로만 규칙을 찾은 뒤 시험용으로 채점한다. 칸 하나가 기록 한 건이다.",
            "기록 20칸 중 4칸을 시험용으로 뽑아 오른쪽 상자로, 나머지 16칸은 학습용 상자로 나누고 학습용으로 모델을 만든 뒤 시험용으로 채점하는 그림")
    train_pos, test_pos = [], []
    for i in range(20):
        (test_pos if i in TEST_IDX else train_pos).append(i)
    # 상자
    f.r(30, 150, 290, 112, "mg-blue", a="mg-from2")
    f.t(40, 144, "학습용 (train) 16건 — 연습문제", "mg-s mg-b mg-tblue", a="mg-from2")
    f.r(440, 150, 250, 112, "mg-orange", a="mg-from2")
    f.t(450, 144, "시험용 (test) 4건 — 모의고사", "mg-s mg-b mg-torange", a="mg-from2")
    for i in range(20):
        x, y = 40 + 32 * i, 56
        if i in TEST_IDX:
            j = test_pos.index(i)
            tx, ty = 470 + 38 * (j % 2) + 40, 160 + 44 * (j // 2)
            cls = "mg-orange"
        else:
            j = train_pos.index(i)
            tx, ty = 40 + 34 * (j % 8), 160 + 44 * (j // 8)
            cls = "mg-blue"
        with f.g("mg-slide2", tx - x, ty - y):
            f.r(x, y, 26, 34, cls)
            f.t(x + 13, y + 22, str(i + 1), "mg-m mg-s mg-c")
        if i in TEST_IDX:
            f.r(x - 3, 53, 32, 40, "mg-hl", a="mg-only1")
    # 모델
    f.r(340, 176, 80, 60, "mg-ink", a="mg-from3")
    f.t(380, 211, "모델", "mg-b mg-c mg-tw", a="mg-from3")
    f.arrow(322, 206, 338, 206, "mg-lnb", "mg-ahb", a="mg-from3")
    f.t(380, 258, "fit: 규칙 찾기", "mg-s mg-b mg-c mg-tblue", a="mg-from3")
    f.arrow(438, 206, 422, 206, "mg-lnr", "mg-ah", a="mg-from4")
    f.t(380, 278, "채점", "mg-s mg-b mg-c mg-torange", a="mg-from4")
    return f


def tree_fig():
    f = Fig("w9-tree", 352,
            ["① 질문을 차례로 던져 기록을 나눈다 (스무고개)", "② 첫 질문: 오븐 220도 ≤ 230도? → 예", "③ 다음 질문: 반죽 두께 5mm ≥ 4mm? → 예",
             "④ 끝 상자(잎)의 '안 탈 것 같음'이 예측이 된다", "⑤ 답이 다르면 다른 길로 내려가 다른 잎에 닿는다", "결과: 질문의 답을 따라 내려가면 예측이 나온다"],
            "결정 트리 — 스무고개로 나누기",
            "<b>맨 위 질문(뿌리)</b>에서 시작해 \"예/아니요\"를 따라 내려가면 <b>끝 상자(잎)</b>에서 예측이 나온다. 초록 길은 오븐 220도·반죽 두께 5mm인 피자 한 판이 지나간 길이다.",
            "오븐 온도 질문에서 시작해 반죽 두께 질문을 거쳐 안 탈 것 같음이라는 잎에 도착하는 결정 트리 그림",
            note="")
    # 기록 카드
    f.r(20, 40, 190, 58, "mg-gray")
    f.t(32, 62, "새 피자 한 판", "mg-s mg-b mg-mu")
    f.t(32, 84, "오븐 220도 · 반죽 두께 5mm", "mg-s")
    # 노드
    def node(cx, cy, w, h, text, cls="mg-blue", tc="mg-tblue"):
        f.r(cx - w / 2, cy - h / 2, w, h, cls)
        f.t(cx, cy + 5, text, f"mg-c mg-b {tc}", style="font-size:14px")

    # 선(먼저 그려서 노드 아래에 깔기)
    f.l(360, 80, 190, 150, "mg-lnm"); f.l(360, 80, 540, 150, "mg-lnm")
    f.l(190, 176, 110, 250, "mg-lnm"); f.l(190, 176, 290, 250, "mg-lnm")
    f.l(360, 80, 190, 150, "mg-lng", a="mg-from1"); f.l(190, 176, 110, 250, "mg-lng", a="mg-from2")
    f.t(250, 108, "예", "mg-b mg-tgreen"); f.t(470, 108, "아니요", "mg-b mg-tred")
    f.t(134, 204, "예", "mg-b mg-tgreen"); f.t(262, 204, "아니요", "mg-b mg-tred")
    node(360, 58, 250, 44, "오븐 온도가 230도 이하인가?")
    node(190, 163, 230, 44, "반죽 두께가 4mm 이상인가?")
    node(540, 163, 150, 40, "탈 것 같음", "mg-red", "mg-tred")
    node(110, 272, 150, 40, "안 탈 것 같음", "mg-green", "mg-tgreen")
    node(290, 272, 130, 40, "탈 것 같음", "mg-red", "mg-tred")
    f.r(231, 33, 258, 50, "mg-hl", a="mg-only1")
    f.r(70, 140, 240, 50, "mg-hl", a="mg-only2")
    f.r(30, 250, 160, 44, "mg-hl", a="mg-win35")
    f.t(500, 52, "← 뿌리: 첫 질문", "mg-s mg-mu")
    f.t(612, 214, "잎: 예측이 적힌", "mg-s mg-mu"); f.t(612, 232, "끝 상자", "mg-s mg-mu")
    f.l(560, 184, 600, 210, "mg-lnm")
    return f


def baseline_fig():
    """정확도·불합격 재현율·정밀도 — 10문제 시험 예제(정답 O 7개·X 3개)."""
    ans = ["O"] * 10
    for i in (2, 5, 8):
        ans[i] = "X"                   # 정답지: X(잡아야 할 불량) 3개
    guess = ["O"] * 10                 # 찍기: 전부 O
    model = ["O"] * 10
    for i in (0, 2, 5, 6):
        model[i] = "X"                 # 모델: X라고 한 4개 중 진짜 X는 2개(2·5번), 8번 X는 놓침
    f = Fig("w9-baseline", 340,
            ["① 시험 10문제. 정답은 O가 7개, 잡아야 할 X가 3개다",
             "② 안 풀고 전부 O만 찍어도 7문제를 맞힌다 → 정확도 70%",
             "③ 공부한 모델도 7문제를 맞혔다 → 정확도 70%. 점수는 똑같다!",
             "④ X 재현율: 진짜 X 3개 중 2개를 찾았다 → 2 ÷ 3 ≈ 67%",
             "⑤ X 정밀도: 모델이 X라고 한 4개 중 2개가 진짜 → 2 ÷ 4 = 50%",
             "결과: 정확도가 같아도 재현율·정밀도를 보면 모델의 일이 보인다"],
            "정확도·재현율·정밀도 — 10문제 시험으로 보기",
            "숫자는 이해를 돕는 <b>예시 값</b>이다. <b>정확도 = 맞힌 문제 수 ÷ 전체</b>다. 정답이 거의 O인 시험에서는 아무것도 안 풀고 \"전부 O\"만 써도 70점이 나오는데, 이 점수가 <b>기준선</b>이다. "
            "그래서 잡아야 할 X만 따로 본다. <b>재현율 = 진짜 X 중 찾아낸 비율</b>, <b>정밀도 = X라고 한 것 중 진짜 X인 비율</b>이다. "
            "반도체에서는 합격이 O, 잡아야 할 불합격이 X에 해당한다.",
            "10문제 시험에서 정답은 O 7개와 X 3개이고, 전부 O라고 찍은 답안과 공부한 모델의 답안이 모두 7문제를 맞혀 정확도 70퍼센트로 같지만, "
            "모델은 진짜 X 3개 중 2개를 찾아 재현율 67퍼센트이고 X라고 한 4개 중 2개가 진짜여서 정밀도 50퍼센트임을 보여 주는 그림")
    X0, STEP, W, H = 30, 58, 50, 40
    rows = [("정답지", ans, 46, None),
            ("찍기 — 안 풀고 전부 O", guess, 106, ("mg-from1", "70%")),
            ("공부한 모델", model, 166, ("mg-from2", "70%"))]
    for i in (2, 5, 8):                # ④ 진짜 X 칸 강조 / ⑤ 모델이 X라고 한 칸 강조
        f.r(X0 + STEP * i - 4, 36, W + 8, 178, "mg-hl", a="mg-only3")
    for i in (0, 2, 5, 6):
        f.r(X0 + STEP * i - 4, 36, W + 8, 178, "mg-hl", a="mg-only4")
    for name, marks, y, extra in rows:
        a = extra[0] if extra else None
        f.t(X0, y - 8, name, "mg-s mg-b" if extra else "mg-s mg-mu", a=a)
        for i, m in enumerate(marks):
            x = X0 + STEP * i
            if extra is None:
                cls, tc = ("mg-red", "mg-tred") if m == "X" else ("mg-gray", "mg-mu")
                label = m
            else:
                ok = m == ans[i]
                cls, tc = ("mg-green", "mg-tgreen") if ok else ("mg-red", "mg-tred")
                label = m + (" ✓" if ok else " ✗")
            f.r(x, y, W, H, cls, a=a)
            f.t(x + W / 2, y + H / 2 + 6, label, f"mg-c mg-b {tc}", a=a, style="font-size:15px")
        if extra:
            f.t(X0 + STEP * 10 + 2, y + H / 2 + 7, extra[1], "mg-m mg-b", a=a)
    f.t(X0, 236, "재현율 = 찾아낸 진짜 X ÷ 진짜 X 전체", "mg-s mg-b", a="mg-only3")
    f.t(X0, 262, "모델 2 ÷ 3 ≈ 67%  /  찍기 0 ÷ 3 = 0%", "mg-m mg-b mg-torange", a="mg-only3", style="font-size:16px")
    f.t(X0, 236, "정밀도 = 진짜 X ÷ 모델이 X라고 한 문제", "mg-s mg-b", a="mg-only4")
    f.t(X0, 262, "모델 2 ÷ 4 = 50%  /  찍기는 X라고 한 적이 없어 계산 불가", "mg-m mg-b mg-torange", a="mg-only4", style="font-size:16px")
    f.t(X0, 236, "정확도 70% · 재현율 67% · 정밀도 50%", "mg-m mg-b", a="mg-from5", style="font-size:18px")
    f.t(X0, 262, "점수가 같아도, 모델은 X를 찾아내고 대신 헛짚기도 한다", "mg-s mg-b mg-torange", a="mg-from5")
    return f


def confusion_fig():
    """헷갈림 표 읽는 법 — 8장면(mg8-*). 빈 틀 → 로트 카드 4장으로 4칸 이름 → 예시 숫자 → 정확도 → 놓친 불합격."""
    f = Fig("w9-confusion", 352,
            ["① 빈 표: 왼쪽은 실제 답, 위쪽은 모델의 예측이다",
             "② 실제 합격 · 예측 합격 → '맞힌 합격' 칸",
             "③ 실제 불합격 · 예측 불합격 → '잡은 불합격' 칸",
             "④ 실제 합격 · 예측 불합격 → '괜한 의심' 칸",
             "⑤ 실제 불합격 · 예측 합격 → '놓친 불합격' 칸",
             "⑥ 로트 100개를 넣고 칸마다 센다. 정확도 = (88 + 6) ÷ 100 = 94%",
             "⑦ 불합격 재현율: 실제 불합격 10개 중 6개를 잡았다 → 60%",
             "⑧ 불합격 정밀도: 불합격이라 한 8개 중 6개가 진짜 → 75%"],
            "헷갈림 표(Confusion Matrix) 읽는 법",
            "숫자는 <b>그림 속 예시 숫자</b>이고 실제 데이터 값이 아니다. 로트 하나는 왼쪽 <b>실제 답</b>과 위쪽 <b>예측</b>이 만나는 칸에 들어간다. "
            "대각선은 맞힌 칸이다. 공장에서는 정확도만 보지 않고, 실제 불합격 줄에서 <b>불합격 재현율</b>(찾아낸 비율)을, 예측 불합격 줄에서 <b>불합격 정밀도</b>(맞는 의심의 비율)를 함께 본다.",
            "빈 2행 2열 표에 로트 카드 4장이 차례로 들어가 맞힌 합격, 잡은 불합격, 괜한 의심, 놓친 불합격이라는 칸 이름이 붙고, "
            "예시 숫자 88, 2, 4, 6이 채워진 뒤 정확도 94퍼센트를 계산하고, 실제 불합격 줄에서 불합격 재현율 60퍼센트, 예측 불합격 줄에서 불합격 정밀도 75퍼센트를 차례로 계산하는 그림")
    X0, CW = 190, 170          # 칸 왼쪽 x, 칸 폭
    Y0, CH = 94, 84            # 칸 위쪽 y, 칸 높이
    HX, HW = 40, 142           # 실제 이름표
    cx = [X0 + CW * j for j in range(2)]
    cy = [Y0 + (CH + 6) * i for i in range(2)]
    # 머리글: 위 = 예측, 왼쪽 = 실제
    f.t(X0 + CW, 40, "모델의 예측 (Predicted) →", "mg-b mg-c", style="font-size:15px")
    f.t(HX + HW / 2, 66, "실제 답 (Actual) ↓", "mg-b mg-c", style="font-size:14px")
    for j, h in enumerate(["예측 합격", "예측 불합격"]):
        f.r(cx[j] + 2, 52, CW - 4, 36, "mg-ink")
        f.t(cx[j] + CW / 2, 76, h, "mg-c mg-tw mg-b", style="font-size:16px")
    for i, h in enumerate(["실제 합격", "실제 불합격"]):
        f.r(HX, cy[i], HW, CH, "mg-ink")
        f.t(HX + HW / 2, cy[i] + CH / 2 + 6, h, "mg-c mg-tw mg-b", style="font-size:16px")
    # 칸: (행, 열, 이름, 상자, 글자색, 이름이 붙는 장면, 예시 숫자)
    cells = [(0, 0, "맞힌 합격", "mg-green", "mg-tgreen", 1, "88"),
             (1, 1, "잡은 불합격", "mg-green", "mg-tgreen", 2, "6"),
             (0, 1, "괜한 의심", "mg-orange", "mg-torange", 3, "2"),
             (1, 0, "놓친 불합격", "mg-red", "mg-tred", 4, "4")]
    for i, j, name, box, tc, k, v in cells:
        x, y = cx[j] + 2, cy[i]
        f.r(x, y, CW - 4, CH, "mg-box")
        with f.g(f"mg8-from{k}"):
            f.r(x, y, CW - 4, CH, box)
            f.t(x + (CW - 4) / 2, y + 28, name, f"mg-c mg-b {tc}", style="font-size:17px")
        f.t(x + (CW - 4) / 2, y + 68, v, f"mg-c mg-b mg-m {tc}", a="mg8-from5", style="font-size:30px")
        # 이 칸에 로트 카드가 들어가는 장면: 행 이름표·열 이름표·칸을 함께 강조
        f.r(x - 4, y - 4, CW + 4, CH + 8, "mg-hl", a=f"mg8-only{k}")
        f.r(HX - 4, cy[i] - 4, HW + 8, CH + 8, "mg-hl", a=f"mg8-only{k}")
        f.r(cx[j] - 2, 48, CW + 4, 44, "mg-hl", a=f"mg8-only{k}")
    # 오른쪽 카드 자리(x 560~706)
    KX, KW = 562, 144

    def card(scene, lines, head="로트 카드 1장", box="mg-gray"):
        with f.g(f"mg8-only{scene}"):
            f.r(KX, Y0, KW, 150, box, rx=8)
            f.t(KX + KW / 2, Y0 + 28, head, "mg-c mg-b mg-mu", style="font-size:14px")
            for n, (s, tc) in enumerate(lines):
                f.t(KX + KW / 2, Y0 + 62 + 30 * n, s, f"mg-c mg-b {tc}", style="font-size:16px")

    card(0, [("어느 칸에", ""), ("들어갈까?", "")], head="로트 하나는")
    for i, j, name, box, tc, k, v in cells:
        card(k, [("실제: " + ("합격" if i == 0 else "불합격"), ""),
                 ("예측: " + ("합격" if j == 0 else "불합격"), ""),
                 ("→ " + name, tc)])
    card(5, [("실제 합격 90", ""), ("실제 불합격 10", ""), ("정확도 94%", "mg-tgreen")], head="로트 100개 (예시)")
    card(6, [("잡음 6 ÷ 실제 10", ""), ("= 60%", "mg-tred"), ("놓침 4건", "mg-tred")], head="불합격 재현율", box="mg-red")
    card(7, [("잡음 6 ÷ 예측 8", ""), ("= 75%", "mg-torange"), ("괜한 의심 2건", "mg-torange")], head="불합격 정밀도", box="mg-orange")
    ROWW = cx[1] + CW - HX + 4
    # ⑥ 정확도 줄
    f.t(X0 + CW, 304, "정확도 = 맞힌 수 ÷ 전체 = (88 + 6) ÷ 100 = 94%", "mg-c mg-b", a="mg8-only5", style="font-size:15px")
    # ⑦ 재현율: 실제 불합격 줄(두 칸)
    f.r(HX - 4, cy[1] - 4, ROWW, CH + 8, "mg-hl", a="mg8-only6")
    f.t(X0 + CW, 304, "재현율 = 잡은 불합격 ÷ 실제 불합격 = 6 ÷ (6 + 4) = 60%", "mg-c mg-b", a="mg8-only6", style="font-size:15px")
    # ⑧ 정밀도: 예측 불합격 줄(두 칸)
    f.r(cx[1] - 2, 48, CW + 4, cy[1] + CH + 4 - 48, "mg-hl", a="mg8-only7")
    f.t(X0 + CW, 304, "정밀도 = 잡은 불합격 ÷ 예측 불합격 = 6 ÷ (6 + 2) = 75%", "mg-c mg-b", a="mg8-only7", style="font-size:15px")
    return f


FIGS = [
    ("결정 트리 —", tree_fig()),
    ("학습용과 시험용", split_fig()),
    ("정확도와 기준선", baseline_fig()),
    ("헷갈림 표(Confusion", confusion_fig()),
]
