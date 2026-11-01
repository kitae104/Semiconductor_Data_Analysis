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
    burnt = {7, 23, 41, 66, 88}
    f = Fig("w9-baseline", 300,
            ["① 피자 100판 중 95판은 안 탔고 5판이 탔다", "② '무조건 안 탄다'라고만 해도 95판을 맞힌다 → 95%", "③ 모델이 96판을 맞혔다 → 96%",
             "④ 차이는 1%p뿐이다. 탄 5판 중 잡은 수는?", "⑤ 기준선 0판, 모델 2판 — 이 차이를 따로 본다", "결과: 정확도는 기준선과 비교하고, 불량은 따로 센다"],
            "정확도와 기준선 — 점수만 보면 속는다",
            "숫자는 이해를 돕는 <b>예시 값</b>이다. 안 타는 판이 95%인 가게에서는 \"무조건 안 탄다\"만 말해도 정확도가 95%다. 그래서 정확도는 <b>기준선</b>과 비교하고, 잡아야 할 불량(탄 판)을 몇 판 잡았는지를 따로 센다.",
            "100칸 중 5칸이 탄 피자이고 무조건 안 탄다고 찍는 기준선 정확도 95퍼센트와 모델 정확도 96퍼센트를 막대로 비교하는 그림")
    for i in range(100):
        r, c = divmod(i, 10)
        f.r(30 + 22 * c, 46 + 22 * r, 18, 18, "mg-red" if i in burnt else "mg-gray")
    f.t(30, 38, "피자 100판 (빨강 = 탄 판)", "mg-s mg-mu")
    mx = 260
    f.t(300, 80, "기준선: '무조건 안 탄다'", "mg-s mg-b", a="mg-from1")
    f.r(300, 88, mx * 0.95, 26, "mg-gray", a="mg-growx1")
    f.t(300 + mx * 0.95 + 8, 107, "95%", "mg-m mg-b", a="mg-from1")
    f.t(300, 144, "모델", "mg-s mg-b", a="mg-from2")
    f.r(300, 152, mx * 0.96, 26, "mg-blue", a="mg-growx2")
    f.t(300 + mx * 0.96 + 8, 171, "96%", "mg-m mg-b mg-tblue", a="mg-from2")
    f.t(300, 214, "탄 5판 중 잡은 수:", "mg-s mg-b", a="mg-from4")
    f.t(300, 238, "기준선 0판   /   모델 2판", "mg-m mg-s mg-b mg-torange", a="mg-from4")
    return f


def confusion_fig():
    f = Fig("w9-confusion", 330,
            ["① 헷갈림 표: 세로가 실제, 가로가 예측이다", "② 대각선 두 칸(87, 5)은 맞힌 수다", "③ 정확도 = (87 + 5) ÷ 100 = 92%",
             "④ 나머지 두 칸(3, 5)은 헷갈린 수다", "⑤ 실제 불합격인데 합격으로 본 5건 = 놓친 불량", "결과: 정확도와 별개로 '놓친 불량'을 따로 읽는다"],
            "헷갈림 표(Confusion Matrix) 읽는 법",
            "숫자는 이해를 돕는 <b>예시 값</b>이다. 세로 줄은 실제 답, 가로 줄은 모델의 예측이다. 대각선은 맞힌 칸이고, 공장에서는 <b>실제 불합격인데 합격으로 예측한 칸</b>(놓친 불량)을 특히 본다.",
            "실제 합격과 불합격, 예측 합격과 불합격으로 이루어진 2행 2열 표에서 대각선 맞힌 칸과 놓친 불량 칸을 차례로 강조하는 그림")
    f.t(420, 42, "예측 (Predicted)", "mg-b mg-c")
    f.t(20, 172, "실제", "mg-b"); f.t(20, 192, "(Actual)", "mg-s mg-mu")
    heads = ["합격(1)", "불합격(-1)"]
    for j, h in enumerate(heads):
        f.chip(300 + 150 * j, 56, 140, 30, h, "mg-ink", "mg-tw mg-b", size="")
    cells = [[("87", "mg-green", "mg-tgreen"), ("3", "mg-orange", "mg-torange")],
             [("5", "mg-red", "mg-tred"), ("5", "mg-green", "mg-tgreen")]]
    for i, h in enumerate(heads):
        f.chip(150, 94 + 76 * i, 140, 70, f"실제 {h}", "mg-ink", "mg-tw mg-b", size="")
        for j in range(2):
            v, box, tc = cells[i][j]
            f.chip(300 + 150 * j, 94 + 76 * i, 140, 70, v, box, f"{tc} mg-b mg-m", size="mg-l")
    f.r(296, 90, 148, 78, "mg-hl", a="mg-only2"); f.r(446, 168, 148, 78, "mg-hl", a="mg-only2")
    f.r(446, 90, 148, 78, "mg-hl", a="mg-only4"); f.r(296, 168, 148, 78, "mg-hl", a="mg-only4")
    f.r(296, 168, 148, 78, "mg-hl", a="mg-only5")
    f.t(300, 270, "정확도 = 맞힌 수 ÷ 전체 = 92 ÷ 100", "mg-s mg-b", a="mg-win35")
    f.t(604, 212, "놓친 불량", "mg-s mg-b mg-tred", a="mg-from5")
    return f


FIGS = [
    ("결정 트리 —", tree_fig()),
    ("학습용과 시험용", split_fig()),
    ("정확도와 기준선", baseline_fig()),
    ("헷갈림 표(Confusion", confusion_fig()),
]
