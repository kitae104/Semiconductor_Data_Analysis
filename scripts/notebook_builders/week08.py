"""8차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「8차시」. 파이썬 PART만 담는다(Orange Correlations는 .ows).
활성 개념 3개: corr() · 상관계수 읽기(부호·크기) · 범위 밖 조건 `|` 한 틀.
재사용: 산점도 4줄 틀(6차시), 조건 검색·한 번 더 고르기(4차시), f-string. 노출 전용: round().
빼는 것: `&`(범위 안은 4차시 "한 번 더 고르기"로), for로 corr 반복, round 다수.
반도체 확인(6단계)은 압력-두께 r 0.09 · 온도 295~305 밖 92건 불합격률 9.8% vs 안 11.5%(원인 후보 아님)이고,
실습 문제는 기준선 11.1%(문제 1) · 온도-두께 0.71 vs 습도-두께 -0.01(문제 2) · 진공도 범위 밖 78건 25.6%(문제 3)로 겹치지 않게 했다.
문제 2 둘째 셀(습도-두께)은 전이 문제 — 학생용은 주석 한 줄만 있는 빈 셀(실습지 문제 2와 같은 글자).
8~10차시는 "원인"이 아니라 "원인 후보"로 말한다(CLAUDE.md).
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week08.py [--no-execute]
"""
from _common import MPL_KOREAN, NotebookPair, code, look_up, md, step

nb = NotebookPair("week08", "8차시 실습 — 공정 이상과 원인 후보 찾기")

# --- 생활 예제: 아이스크림 가게 30일 날씨·판매(완성 코드, 실행하며 관찰) -----------------------
nb.add(
    step(1, "데이터 읽고 기준선 구하기"),
    md("아이스크림 가게 30일 기록(교육용 가상 데이터)입니다. `손님평가`는 1 = 좋음, -1 = 불만. "
       "**기준선** = 전체에서 불만인 날의 비율입니다. 나중에 \"특정 조건에서 더 높은가?\"를 이 숫자와 비교합니다."),
    code('import pandas as pd\n'
         '\n'
         'shop = pd.read_csv("../../data/weekly/week08/week08_easy_weather_sales.csv", encoding="utf-8-sig")\n'
         'print(shop.shape)'),
    code("shop.head()"),
    code('bad_all = shop[shop["손님평가"] == -1]\n'
         'base_rate = round(len(bad_all) / len(shop) * 100, 1)\n'
         'print(base_rate)'),

    step(2, "산점도와 상관계수 — corr()"),
    md("산점도로 모양을 먼저 보고, `corr()`로 \"얼마나 한 줄로 함께 움직이나\"를 -1~1 숫자로 잽니다. "
       "+면 함께 오르고, -면 한쪽이 오를 때 다른 쪽이 내려가며, 0에 가까우면 한 방향으로 함께 움직이는(곧은 띠) 관계가 거의 없습니다."),
    code("import matplotlib.pyplot as plt\n" + MPL_KOREAN + "\n"
         "\n"
         'plt.scatter(shop["최고기온_C"], shop["아이스크림판매량_count"])\n'
         'plt.xlabel("최고기온_C")\n'
         'plt.ylabel("아이스크림판매량_count")\n'
         "plt.show()"),
    code('r_ice = shop["최고기온_C"].corr(shop["아이스크림판매량_count"])\n'
         'print(round(r_ice, 2))'),
    code('r_choco = shop["최고기온_C"].corr(shop["핫초코판매량_cup"])\n'
         'print(round(r_choco, 2))'),
    look_up("상관계수 읽는 법"),

    step(3, "관계없는 열과 나란히 비교하기"),
    md("상관계수 하나만 보면 큰지 작은지 감이 오지 않습니다. 관계없을 것 같은 열(습도)과 나란히 놓고 비교합니다."),
    code('r_humid = shop["습도_pct"].corr(shop["아이스크림판매량_count"])\n'
         'print(round(r_humid, 2))'),

    step(4, "범위 밖 값 찾기 — 상관계수가 놓치는 경우"),
    md("냉동고는 -20~-16℃가 연습용 기준입니다. 너무 차가워도, 너무 따뜻해도 문제라서 상관계수로는 0에 가깝게 나올 수 있습니다. "
       "먼저 산점도로 모양을 봅니다. \"범위 밖\"은 `|`(또는)로 두 조건을 잇습니다. **조건마다 괄호 `( )`로 감쌉니다.** "
       "`|`는 한국어 키보드에서 엔터 위 `₩` 키를 Shift와 함께 누릅니다.",
       student="냉동고는 -20~-16℃가 연습용 기준입니다. 너무 차가워도, 너무 따뜻해도 문제라서 상관계수로는 0에 가깝게 나올 수 있습니다. "
               "먼저 산점도로 모양을 봅니다. \"범위 밖\"은 `|`(또는)로 두 조건을 잇습니다. **조건마다 괄호 `( )`로 감쌉니다.** "
               "`|`는 한국어 키보드에서 엔터 위 `₩` 키를 Shift와 함께 누릅니다.\n\n"
               "- 직접 쓰기(빈칸 없음): 바로 아래 셀에 2단계 산점도 4줄과 같은 모양으로 x = `냉동고온도_C`, y = `손님평가` 산점도를 그립니다. "
               "아래 줄(-1, 불만) 점이 어디에 몰려 있는지 봅니다."),
    code('plt.scatter(shop["냉동고온도_C"], shop["손님평가"])\n'
         'plt.xlabel("냉동고온도_C")\n'
         'plt.ylabel("손님평가")\n'
         "plt.show()",
         "# TODO: 2단계 산점도 4줄과 같은 모양으로, x = 냉동고온도_C, y = 손님평가 산점도를 직접 그리세요.\n"),
    code('r_freezer = shop["냉동고온도_C"].corr(shop["손님평가"])\n'
         'print(round(r_freezer, 2))'),
    code('freezer_out = shop[(shop["냉동고온도_C"] < -20) | (shop["냉동고온도_C"] > -16)]\n'
         'bad_out = freezer_out[freezer_out["손님평가"] == -1]\n'
         'print(len(freezer_out), len(bad_out))'),
    code('out_rate = round(len(bad_out) / len(freezer_out) * 100, 1)\n'
         'print(out_rate)'),

    step(5, "원인 후보 문장 쓰기"),
    md("숫자를 문장으로 옮깁니다. \"원인이다\"가 아니라 **\"원인 후보다\"**라고 씁니다 — 함께 움직이는 것만으로는 원인을 확정할 수 없습니다. "
       "이 문장의 \"높다\"와 \"원인 후보다\"는 숫자를 보고 사람이 정한 결론을 코드에 적은 것입니다. 숫자가 바뀌면 문장이 맞는지 다시 확인합니다."),
    code('print(f"냉동고 온도가 범위 밖인 날 불만률은 {out_rate}%로, 기준선 {base_rate}%보다 높다. 냉동고 온도는 불만의 원인 후보다.")'),
    look_up("상관관계 인과관계 차이"),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(6, "반도체 데이터로 확인하기 — 공정 센서 기록 450건"),
    md("공정 센서 기록 450건(교육용 가상 데이터)입니다. 2~4단계와 같은 코드에서 표 이름과 열 이름만 바뀝니다. "
       "온도 295~305℃는 이 과정의 연습용 기준입니다(실제 공정 규격 아님). "
       "`합격여부`: 1 = 합격, -1 = 불합격. 설비 4대가 여러 공정 기록을 함께 남긴 교육용 가상 기록입니다."),
    code('df = pd.read_csv("../../data/weekly/week08/week08_anomaly_root_cause.csv", encoding="utf-8-sig")\n'
         'print(df.shape)'),
    code('r_press = df["압력_Pa"].corr(df["두께_nm"])\n'
         'print(round(r_press, 2))'),
    code('temp_out = df[(df["온도_C"] < 295) | (df["온도_C"] > 305)]\n'
         'temp_out_fail = temp_out[temp_out["합격여부"] == -1]\n'
         'print(len(temp_out), round(len(temp_out_fail) / len(temp_out) * 100, 1))'),
    md("범위 **안**은 4차시처럼 한 번 고른 표에서 한 번 더 고릅니다. "
       "범위 안 비율은 참고용이고, 오늘 보고서의 비교 기준은 **기준선**(전체 불합격률) 하나입니다 — 7단계 문제 1에서 구합니다."),
    code('temp_in = df[df["온도_C"] >= 295]\n'
         'temp_in = temp_in[temp_in["온도_C"] <= 305]\n'
         'temp_in_fail = temp_in[temp_in["합격여부"] == -1]\n'
         'print(len(temp_in), round(len(temp_in_fail) / len(temp_in) * 100, 1))'),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(7, "반도체 데이터 실습"),
    md("6단계 셀을 먼저 실행한 뒤 풀어요. 실습지 문제 1~3과 같은 문제입니다. "
       "오늘의 미션: 불합격과 관련 있어 보이는 공정 값을 찾아 \"원인 후보\" 보고서 한 줄을 씁니다."),

    md("### 문제 1 — 불합격 기준선 구하기",
       student="### 문제 1 — 불합격 기준선 구하기\n\n"
               "- 힌트: 1단계 `bad_all`·`base_rate`와 같은 모양. 불합격은 `합격여부`가 -1.\n\n"
               "**주의**: 나누는 수는 전체 기록 수 `len(df)`입니다. 1단계의 `shop`과 헷갈리면 오류 없이 100%가 넘는 숫자가 나옵니다. "
               "`88.9`가 나오면 불합격(-1) 대신 합격(1)을 센 것입니다."),
    code('fail_all = df[df["합격여부"] == -1]\n'
         'base_rate = round(len(fail_all) / len(df) * 100, 1)\n'
         'print(base_rate)',
         '# TODO: 불합격을 뜻하는 숫자와, 나누는 표 이름을 채우세요.\n'
         'fail_all = df[df["합격여부"] == ____]\n'
         'base_rate = round(len(fail_all) / len(____) * 100, 1)\n'
         'print(base_rate)'),

    md("### 문제 2 — 온도-두께와 습도-두께 상관계수 비교하기",
       student="### 문제 2 — 온도-두께와 습도-두께 상관계수 비교하기\n\n"
               "- 힌트: 2·3단계 `shop[\"최고기온_C\"].corr(shop[\"아이스크림판매량_count\"])`와 같은 모양\n"
               "- 이어서 직접 쓰기(전이 문제, 빈칸 없음): 두 번째 셀은 빈칸이 없습니다. 첫 셀과 같은 모양으로 `습도_pct`와 `두께_nm`의 상관계수를 직접 씁니다.\n\n"
               "**주의**: `corr()`는 숫자 열끼리만 계산합니다. `설비번호`처럼 글자 열을 넣으면 오류가 납니다. "
               "`KeyError: '습도'`처럼 나오면 열 이름을 줄여 쓴 것입니다 — 정확한 이름은 `습도_pct`. "
               "두 열 모두 `df`에서 꺼냅니다. 힌트의 `shop`이 남아 `shop[\"습도_pct\"].corr(df[\"두께_nm\"])`처럼 쓰면 오류 없이 `0.29`가 나옵니다"
               "(가게 기록과 공장 기록을 행 번호끼리 짝지어 계산한 엉뚱한 값)."),
    code('r_temp = df["온도_C"].corr(df["두께_nm"])\n'
         'print(round(r_temp, 2))',
         '# TODO: 상관계수를 구하는 함수 이름을 채우세요.\n'
         'r_temp = df["온도_C"].____(df["두께_nm"])\n'
         'print(round(r_temp, 2))'),
    code('r_humid = df["습도_pct"].corr(df["두께_nm"])\n'
         'print(round(r_humid, 2))',
         '# TODO: 위 셀과 같은 모양으로, 습도_pct와 두께_nm의 상관계수를 r_humid에 담고 소수 둘째 자리로 출력하세요.\n'),

    md("### 문제 3 — 진공도가 범위 밖일 때 불합격률",
       student="### 문제 3 — 진공도가 범위 밖일 때 불합격률\n\n"
               "- 진공도 연습용 기준은 4.5~5.5 mTorr입니다. 4.5보다 작거나 5.5보다 크면 범위 밖입니다.\n"
               "- 힌트: 6단계 `temp_out`과 같은 모양\n\n"
               "**주의**\n"
               "- 두 조건을 각각 괄호로 감싸지 않으면 오류가 납니다. `|` 대신 `or`를 쓰면 `ValueError`가 납니다. `|`는 엔터 위 `₩` 키를 Shift와 함께 누릅니다.\n"
               "- `&`(그리고)를 쓰면 `0 0`이 나오고 다음 셀에서 `ZeroDivisionError`가 납니다 — 4.5보다 작으면서 5.5보다 큰 값은 없습니다.\n"
               "- `78 58`이 나오면 불합격(-1) 대신 합격(1)을 센 것입니다.\n"
               "- 첫 셀이 실패한 채 둘째 셀을 실행하면 `NameError: name 'vac_out_fail' is not defined`가 납니다. 첫 셀부터 고치세요.\n"
               "- 둘째 셀은 두 숫자(범위 밖 불합격률, 기준선)만 출력합니다. 불합격률이 `4.4`로 나오면 `df`로 나눈 것입니다(범위 밖 표 `vac_out`으로 나눕니다). "
               "기준선이 `26.7`로 나오면 문제 1 셀을 실행하지 않아 1단계 가게 기록의 `base_rate`가 남아 있는 것입니다.\n"
               "- 높은지 낮은지, 원인 후보인지는 실습지 문제 5에서 직접 문장으로 씁니다."),
    code('vac_out = df[(df["진공도_mTorr"] < 4.5) | (df["진공도_mTorr"] > 5.5)]\n'
         'vac_out_fail = vac_out[vac_out["합격여부"] == -1]\n'
         'print(len(vac_out), len(vac_out_fail))',
         '# TODO: "또는"을 뜻하는 기호와 불합격을 뜻하는 숫자를 채우세요.\n'
         'vac_out = df[(df["진공도_mTorr"] < 4.5) ____ (df["진공도_mTorr"] > 5.5)]\n'
         'vac_out_fail = vac_out[vac_out["합격여부"] == ____]\n'
         'print(len(vac_out), len(vac_out_fail))'),
    code('vac_rate = round(len(vac_out_fail) / len(vac_out) * 100, 1)\n'
         'print(vac_rate, base_rate)',
         '# TODO: 범위 밖 불합격률 = 범위 밖 불합격 수 ÷ 범위 밖 기록 수 × 100. 나누는 표 이름을 채우세요.\n'
         'vac_rate = round(len(vac_out_fail) / len(____) * 100, 1)\n'
         'print(vac_rate, base_rate)'),
    look_up("원인 후보 확인하는 방법"),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(8, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> pandas 표 df에서 온도_C, 압력_Pa, 진공도_mTorr, 두께_nm, 습도_pct 다섯 열끼리의 상관계수를 한 번에 표로 보여 주는 "
       "짧은 코드를 만들어 줘. 소수 둘째 자리까지.\n\n"
       "아래는 받은 코드의 예시입니다. 4차시의 여러 열 고르기(대괄호 두 겹) 뒤에 `corr()`를 붙였습니다. "
       "실행해서 문제 2의 두 숫자를 표에서 찾아보세요. 이 표에는 `합격여부`가 없어 진공도와 불합격의 관계는 처음부터 나올 수 없습니다. 진공도 줄이 0에 가까운 것은 진공도가 다른 센서와 따로 움직였다는 뜻입니다."),
    code('cols = ["온도_C", "압력_Pa", "진공도_mTorr", "두께_nm", "습도_pct"]\n'
         'print(df[cols].corr().round(2))'),
)

if __name__ == "__main__":
    nb.cli()
