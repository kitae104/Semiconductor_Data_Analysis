from .lib import Fig


def flow_fig():
    f = Fig("w10-flow", 330,
            ["① 지난 기록으로 모델 셋을 학습시킨다", "② Test and Score가 모델마다 점수를 매긴다", "③ 기준선과 비교해 쓸 모델을 고른다",
             "④ 새 로트(합격 여부를 아직 모름)를 넣는다", "⑤ Predictions가 합격/불합격 예측을 붙인다", "결과: 학습 → 점수 비교 → 새 데이터 예측 순서로 쓴다"],
            "모델 비교에서 새 데이터 예측까지",
            "위 줄은 <b>지난 기록</b>으로 모델 셋을 만들고 점수를 비교하는 단계, 아래 줄은 고른 모델에 <b>새 데이터</b>를 넣어 예측을 얻는 단계다. 점수는 기준선과 함께 읽고, 예측은 \"원인\"이 아니라 \"확인해 볼 후보\"로 쓴다.",
            "지난 기록이 Tree, Logistic Regression, kNN 세 모델을 거쳐 Test and Score에서 점수가 비교되고 고른 모델에 새 로트를 넣어 Predictions로 예측을 얻는 그림",
            note="")
    f.r(20, 50, 130, 70, "mg-box")
    f.t(85, 80, "지난 기록", "mg-b mg-c"); f.t(85, 100, "(정답 있음)", "mg-s mg-c mg-mu")
    for k, name in enumerate(["Tree", "Logistic Regression", "kNN"]):
        f.chip(240, 38 + 34 * k, 190, 28, name, "mg-blue", "mg-tblue mg-m", size="mg-s")
    f.r(236, 34, 198, 108, "mg-hl", a="mg-only1")
    f.r(510, 50, 190, 70, "mg-box")
    f.t(605, 80, "Test and Score", "mg-b mg-c mg-m", style="font-size:14px"); f.t(605, 100, "모델별 점수 비교", "mg-s mg-c mg-mu")
    f.r(506, 46, 198, 78, "mg-hl", a="mg-only2")
    f.arrow(152, 85, 238, 85, "mg-lnb", "mg-ahb")
    f.arrow(432, 85, 508, 85, "mg-lnb", "mg-ahb")
    f.t(330, 168, "점수가 높고 기준선보다 나은 모델을 고른다", "mg-s mg-b mg-c mg-torange", a="mg-from3")
    f.arrow(335, 144, 335, 196, "mg-lnm", "mg-ah", a="mg-from3")
    # 아래 줄
    f.chip(240, 202, 190, 40, "고른 모델", "mg-blue", "mg-tblue mg-b", a="mg-from3", size="")
    f.r(20, 198, 150, 48, "mg-orange", a="mg-from4")
    f.t(95, 218, "새 로트", "mg-b mg-c mg-torange", a="mg-from4"); f.t(95, 236, "(정답 없음)", "mg-s mg-c mg-mu", a="mg-from4")
    f.arrow(172, 222, 238, 222, "mg-lnb", "mg-ahb", a="mg-from4")
    f.r(510, 198, 190, 48, "mg-green", a="mg-from5")
    f.t(605, 218, "Predictions", "mg-b mg-c mg-m mg-tgreen", a="mg-from5", style="font-size:14px"); f.t(605, 236, "합격/불합격 예측", "mg-s mg-c mg-mu", a="mg-from5")
    f.arrow(432, 222, 508, 222, "mg-lnb", "mg-ahb", a="mg-from5")
    return f


FIGS = [
    ("모델 셋 비교와 새 데이터 예측", flow_fig()),
]
