from .lib import Fig

BW, BH = 152, 78
# (x, y, w, 제목, 설명, 상자, 글자색, 등장 클래스) — 위 줄은 왼→오, 아래 줄은 오→왼(뱀 모양)
STEPS = [
    (20, 44, BW, "팀장의 문제", "어느 로트부터 점검?", "mg-box", "", ""),
    (196, 44, BW, "1. 계획 묻기", "AI: 위젯 순서 제안", "mg-orange", "mg-torange", "mg8-from1"),
    (372, 44, BW, "2. 점검과 정리", "빈칸·튀는 값 정리", "mg-blue", "mg-tblue", "mg8-from2"),
    (548, 44, BW, "3. 지난 기록 비교", "설비·작업조별 합격률", "mg-blue", "mg-tblue", "mg8-from3"),
    (548, 184, BW, "4. 새 로트 예측", "모델로 먼저 볼 로트", "mg-blue", "mg-tblue", "mg8-from4"),
    (372, 184, BW, "5. 해석 초안 확인", "숫자·원인 직접 확인", "mg-orange", "mg-torange", "mg8-from5"),
    (20, 184, 328, "결론 보고 문장", "먼저 볼 로트와 확인한 숫자로 쓴다", "mg-green", "mg-tgreen", "mg8-from6"),
]


def ai_steps_fig():
    f = Fig("w10-ai-steps", 340,
            ["출발: 팀장의 문제 — 새 로트 10개 중 어느 것부터 점검할까?",
             "단계 1: AI에게 Orange 위젯 순서를 묻는다 — 파일은 올리지 않는다",
             "단계 2: Orange로 빈칸·튀는 값을 점검하고 정리한다",
             "단계 3: 지난 기록에서 설비별·작업조별 합격률을 비교한다",
             "단계 4: 모델로 새 로트를 예측해 먼저 볼 로트를 고른다",
             "단계 5: AI 해석 초안의 숫자·원인 표현을 Orange 화면과 맞춰 고친다",
             "결론: 확인한 숫자로 보고 문장을 쓴다 (원인 단정 → 근거 확인)",
             "결과: AI는 계획과 초안만, 실행과 확인은 내가 Orange로 한다"],
            "AI와 함께 분석하는 5단계",
            "주황 칸은 AI가 주는 <b>초안</b>, 파란 칸은 내가 Orange로 하는 <b>확인</b>이다. 숫자는 늘 Orange 화면에서 읽고, 초안의 원인 단정은 근거 수치가 있으면 \"원인 후보\"로 고치고, 근거가 없으면 뺀다. 교육용 가상 데이터로 한 연습이다.",
            "팀장의 문제 새 로트 10개 중 어느 것부터 점검할까에서 시작해 AI에게 계획 묻기, Orange로 점검과 정리, 지난 기록 비교, 새 로트 예측, AI 해석 초안 확인을 거쳐 결론 보고 문장에 이르는 뱀 모양 흐름 그림")
    # 범례
    f.r(330, 9, 14, 14, "mg-orange"); f.t(350, 21, "AI가 주는 초안", "mg-s mg-mu")
    f.r(470, 9, 14, 14, "mg-blue"); f.t(490, 21, "내가 하는 확인", "mg-s mg-mu")
    f.r(610, 9, 14, 14, "mg-green"); f.t(630, 21, "결과", "mg-s mg-mu")
    for k, (x, y, w, title, sub, box, tc, a) in enumerate(STEPS):
        with f.g(a):
            f.r(x, y, w, BH, box)
            f.t(x + w / 2, y + 33, title, "mg-b mg-c " + tc, style="font-size:16px")
            f.t(x + w / 2, y + 57, sub, "mg-s mg-c mg-mu")
        f.r(x - 4, y - 4, w + 8, BH + 8, "mg-hl", a=f"mg8-only{k}")
    # 화살표(뱀 모양)
    f.arrow(174, 83, 194, 83, "mg-lnb", "mg-ahb", a="mg8-from1")
    f.arrow(350, 83, 370, 83, "mg-lnb", "mg-ahb", a="mg8-from2")
    f.arrow(526, 83, 546, 83, "mg-lnb", "mg-ahb", a="mg8-from3")
    f.arrow(624, 124, 624, 182, "mg-lnb", "mg-ahb", a="mg8-from4")
    f.arrow(546, 223, 526, 223, "mg-lnb", "mg-ahb", a="mg8-from5")
    f.arrow(370, 223, 350, 223, "mg-lnb", "mg-ahb", a="mg8-from6")
    # 단계별 주의점
    f.t(272, 146, "파일은 올리지 않고 열 설명만", "mg-s mg-c mg-torange", a="mg8-from1")
    f.t(448, 284, "AI 숫자는 지어낸 것일 수 있다", "mg-s mg-c mg-tred", a="mg8-from5")
    f.t(184, 284, "원인 단정 → 근거 확인", "mg-s mg-b mg-c mg-tblue", a="mg8-from6")
    return f


FIGS = [
    ("AI와 함께 분석하는 5단계", ai_steps_fig()),
]
