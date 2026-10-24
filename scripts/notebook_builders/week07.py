"""7차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「7차시」. 파이썬 PART만 담는다(Orange Pivot Table은 .ows).
활성 개념 2개: 비교로 새 열 만들기(df["합격"] = df["합격여부"] == 1) · groupby().mean().
재사용: value_counts + plt.bar(6차시), sort_values·조건 검색(4차시). 노출 전용: .round(1).
빼는 것: 학생별·풀이시간 묶음, 로트별 수율 실습 문항(→ 반도체 확인 완성 코드), 설비별 평균 온도.
xticks(rotation=45)는 문제 3 막대 한 줄에만 노출(불량 유형 이름 7개가 겹침). 문제 3 막대는 학생용에서 빈 전이 셀이다.
4단계 작업조 groupby에 빈칸 하나(PART 1 직접 쓰기), 맨 아래 과제 1 빈 셀(정답본에 풀이).
반도체 확인(4단계)은 불합격 열 · 작업조별 불합격률 · 불합격률 20% 넘는 로트 수(21 = 수율 80% 미만)이고,
실습 문제는 합격 열 · 전체 합격률 88.0 / 설비별 합격률(EQ-04 75.0) / 불량 유형 막대(두께 불량 11)로 겹치지 않게 했다.
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week07.py [--no-execute]
"""
from _common import MPL_KOREAN, NotebookPair, code, look_up, md, step

nb = NotebookPair("week07", "7차시 실습 — 설비·공정 비교와 수율·불량 분석")

# --- 생활 예제: 반별 쪽지시험 24문항(완성 코드, 실행하며 관찰) -------------------------------
nb.add(
    step(1, "정답 열 만들기 — 비교로 새 열"),
    md("세 반 학생 6명의 쪽지시험 기록(교육용 가상 데이터)입니다. `정답여부`는 1 = 정답, -1 = 오답입니다."),
    code('import pandas as pd\n'
         '\n'
         'quiz = pd.read_csv("../../data/weekly/week07/week07_easy_quiz_results.csv", encoding="utf-8-sig")\n'
         'print(quiz.shape)'),
    code("quiz.head()"),
    md("`quiz[\"정답여부\"] == 1`은 행마다 True/False를 만듭니다. 이것을 새 열 `정답`에 저장합니다. "
       "True는 1, False는 0으로 계산되므로 **평균 × 100 = 정답률(%)**입니다."),
    code('quiz["정답"] = quiz["정답여부"] == 1\n'
         'print(quiz["정답"].sum())\n'
         'print(quiz["정답"].mean() * 100)'),

    step(2, "묶어서 비교하기 — groupby"),
    md("`groupby(\"반\")`은 같은 반끼리 묶고, 뒤의 `[\"정답\"].mean()`은 묶음마다 평균을 냅니다. `.round(1)`은 소수 첫째 자리까지 반올림입니다."),
    code('class_rate = quiz.groupby("반")["정답"].mean() * 100\n'
         'print(class_rate.round(1))'),
    code('print(class_rate.sort_values())'),
    look_up("반도체 수율 뜻"),

    step(3, "오답 유형 줄 세우기"),
    md("오답(-1)인 행만 고른 뒤 `오답유형`을 셉니다. 많은 순으로 세워 막대로 그리면 \"무엇부터 고칠지\"가 보입니다(6차시 막대 4줄 틀)."),
    code('wrong_counts = quiz[quiz["정답여부"] == -1]["오답유형"].value_counts()\n'
         'print(wrong_counts)'),
    code("import matplotlib.pyplot as plt\n" + MPL_KOREAN + "\n"
         "\n"
         "plt.bar(wrong_counts.index, wrong_counts)\n"
         'plt.xlabel("오답유형")\n'
         'plt.ylabel("오답 수")\n'
         "plt.show()"),
    look_up("파레토 차트"),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(4, "반도체 데이터로 확인하기 — 웨이퍼 300장"),
    md("로트 75개 × 웨이퍼 4장 = 300장의 공정 기록(교육용 가상 데이터)입니다. 1~2단계와 같은 코드에서 표 이름과 열 이름만 바뀝니다. "
       "오늘은 비교 결과를 \"원인\"이 아니라 \"원인 후보\"로 말합니다.\n\n"
       "`합격여부`: 1 = 합격, -1 = 불합격. 설비 4대가 여러 공정 기록을 함께 남긴 교육용 가상 기록입니다.",
       student="로트 75개 × 웨이퍼 4장 = 300장의 공정 기록(교육용 가상 데이터)입니다. 1~2단계와 같은 코드에서 표 이름과 열 이름만 바뀝니다. "
               "오늘은 비교 결과를 \"원인\"이 아니라 \"원인 후보\"로 말합니다.\n\n"
               "`합격여부`: 1 = 합격, -1 = 불합격. 설비 4대가 여러 공정 기록을 함께 남긴 교육용 가상 기록입니다.\n\n"
               "- 빈칸 하나: 2단계 `\"반\"`이 있던 자리에 작업조 열 이름을 넣습니다. 열 이름은 따옴표로 감쌉니다 — 따옴표가 없으면 `NameError`가 납니다."),
    code('df = pd.read_csv("../../data/weekly/week07/week07_equipment_yield.csv", encoding="utf-8-sig")\n'
         'print(df.shape)'),
    code('df["불합격"] = df["합격여부"] == -1\n'
         'shift_fail = df.groupby("작업조")["불합격"].mean() * 100\n'
         'print(shift_fail.round(1))',
         'df["불합격"] = df["합격여부"] == -1\n'
         '# TODO: 작업조별로 묶도록 열 이름을 채우세요(2단계 "반"이 있던 자리).\n'
         'shift_fail = df.groupby(____)["불합격"].mean() * 100\n'
         'print(shift_fail.round(1))'),
    code('lot_fail = df.groupby("로트번호")["불합격"].mean() * 100\n'
         'print((lot_fail > 20).sum())'),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(5, "반도체 데이터 실습"),
    md("4단계 셀을 먼저 실행한 뒤 풀어요. 실습지 문제 1~3과 같은 문제입니다. "
       "오늘의 미션: 어느 설비의 합격률(이 기록에서 수율 대신 쓰는 값)이 가장 낮은지, 가장 많은 불량 유형은 무엇인지 보고합니다."),

    md("### 문제 1 — 합격 열 만들고 전체 합격률 구하기",
       student="### 문제 1 — 합격 열 만들고 전체 합격률 구하기\n\n"
               "- 힌트: 1단계 `quiz[\"정답\"] = quiz[\"정답여부\"] == 1`과 같은 모양\n\n"
               "**주의**: `==`(같은가?)를 `=`로 바꾸면 오류 없이 `합격여부` 열이 모두 1로 덮어써집니다 — 그랬다면 고친 뒤 4단계부터 다시 실행하세요. "
               "`합격여부`(1/-1)를 그대로 평균 내면 오류 없이 엉뚱한 숫자(0.76)가 나옵니다 — 새로 만든 `합격` 열의 평균을 냅니다. "
               "결과가 12.0이면 4단계를 따라 `-1`(불합격)을 쓴 것입니다 — 합격은 `1`."),
    code('df["합격"] = df["합격여부"] == 1\n'
         'print(df["합격"].mean() * 100)',
         '# TODO: 합격을 뜻하는 숫자와, 평균을 내는 함수 이름을 채우세요.\n'
         'df["합격"] = df["합격여부"] == ____\n'
         'print(df["합격"].____() * 100)'),

    md("### 문제 2 — 설비별 합격률 비교하기",
       student="### 문제 2 — 설비별 합격률 비교하기\n\n"
               "- 힌트: 2단계 `quiz.groupby(\"반\")[\"정답\"].mean() * 100`과 같은 모양. 묶는 열은 `설비번호`, 평균 낼 열은 문제 1의 `합격`.\n\n"
               "**주의**: `groupby(\"설비번호\")` 뒤 대괄호 `[\"합격\"]`를 빼먹으면 다른 열까지 평균을 내려다 `TypeError`가 납니다. "
               "평균 낼 열은 문제 1에서 새로 만든 `합격`입니다 — `합격여부`를 넣으면 오류 없이 엉뚱한 값(EQ-04가 50.0)이 나옵니다. "
               "문제 1을 건너뛰면 `KeyError: 'Column not found: 합격'`, 첫 셀이 실패한 채 둘째 셀을 실행하면 `NameError: name 'eq_rate' is not defined`가 납니다."),
    code('eq_rate = df.groupby("설비번호")["합격"].mean() * 100\n'
         'print(eq_rate.round(1))',
         '# TODO: 묶을 열 이름과 평균 낼 열 이름을 채우세요.\n'
         'eq_rate = df.groupby(____)[____].mean() * 100\n'
         'print(eq_rate.round(1))'),
    code("print(eq_rate.round(1).sort_values())",
         "# TODO: 작은 값부터 줄 세우는 함수 이름을 채우세요.\n"
         "print(eq_rate.round(1).____())"),

    md("### 문제 3 — 불량 유형 줄 세우기",
       student="### 문제 3 — 불량 유형 줄 세우기\n\n"
               "- 힌트: 3단계 `wrong_counts`와 같은 모양. 고르는 조건은 `합격여부`가 -1, 세는 열은 `불량유형`.\n\n"
               "- 이어서 직접 쓰기(전이 문제, 빈칸 없음): 바로 아래 빈 셀에 3단계 막대 코드(4줄 틀)를 보고 `defect_counts`로 막대그래프를 직접 쓰세요. "
               "x축 이름 `\"불량유형\"`, y축 이름 `\"불량 건수\"`. 이름이 겹치면 `plt.bar(…)` 다음 줄에 `plt.xticks(rotation=45)`를 넣습니다.\n\n"
               "**주의**: `1`을 쓰면 오류 없이 빈 결과 `Series([], Name: count, dtype: int64)`가 나옵니다 — 불합격은 `-1`. "
               "첫 셀이 실패한 채 막대 셀을 실행하면 `NameError: name 'defect_counts' is not defined`가 납니다."),
    code('defect_counts = df[df["합격여부"] == -1]["불량유형"].value_counts()\n'
         'print(defect_counts)',
         '# TODO: 불합격을 뜻하는 숫자와, 셀 열 이름을 채우세요.\n'
         'defect_counts = df[df["합격여부"] == ____][____].value_counts()\n'
         'print(defect_counts)'),
    code("plt.bar(defect_counts.index, defect_counts)\n"
         "plt.xticks(rotation=45)   # 이름이 길어 겹치지 않게 45도 기울이기\n"
         'plt.xlabel("불량유형")\n'
         'plt.ylabel("불량 건수")\n'
         "plt.show()",
         '# TODO: 직접 쓰기 — 강의 "오답 유형 줄 세우기"의 막대 4줄 틀을 보고 defect_counts로 막대그래프를 그리세요.\n'),
    look_up("비교만으로 원인을 단정할 수 없는 이유"),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(6, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> pandas Series eq_rate(설비별 합격률 %)가 있어. 합격률이 90% 미만인 설비는 \"원인 후보 — 더 살펴보기\", "
       "아니면 \"연습용 기준 이상\"이라고 한 줄씩 출력하는 짧은 코드를 만들어 줘. 90%는 연습용 기준이야.\n\n"
       "아래는 받은 코드의 예시입니다. `.items()`는 이름과 값을 한 쌍씩 꺼냅니다(처음 보는 함수). "
       "실행해서 문제 2의 결과와 같은 설비가 표시되는지 확인하세요. "
       "`eq_rate`는 문제 2에서 만드는 변수라, 문제 2를 먼저 풀어야 실행됩니다(안 풀었으면 `NameError: name 'eq_rate' is not defined`)."),
    code('for eq, rate in eq_rate.items():\n'
         '    if rate < 90:\n'
         '        print(f"{eq} 합격률 {round(rate, 1)}% → 원인 후보 — 더 살펴보기")\n'
         '    else:\n'
         '        print(f"{eq} 합격률 {round(rate, 1)}% → 연습용 기준 이상")'),
)

# --- 과제 1(강의 "과제" 절 — 노트북 맨 아래 빈 셀) -------------------------------------------
nb.add(
    md("## 과제 1 — 공정별 합격률 구하기(다음 차시까지)\n\n"
       "문제 2와 같은 모양으로 `공정명`별 합격률을 구해 `sort_values()`로 줄 세웁니다. "
       "가장 낮은 공정의 불합격 기록이 어느 설비에 몰려 있는지도 4차시 조건 검색과 `value_counts()`로 세어 보고, "
       "\"공정 차이와 설비 차이를 떼어 볼 수 있는가\"를 한 문장으로 적습니다."),
    code('proc_rate = df.groupby("공정명")["합격"].mean() * 100\n'
         'print(proc_rate.round(1).sort_values())\n'
         '\n'
         'dep = df[df["공정명"] == "증착"]\n'
         'print(dep[dep["합격여부"] == -1]["설비번호"].value_counts())',
         '# TODO: 과제 1 코드를 여기에 직접 쓰세요.\n'),
    md("증착이 76.9%로 가장 낮지만 불합격 12장 중 7장이 EQ-04 기록이라 설비 차이와 섞여 있습니다. "
       "이 기록은 로트마다 설비 하나·공정 하나만 적어 두어, 공정만의 원인 후보로 좁힐 수 없습니다.",
       student="(여기에 한 문장을 적으세요.)"),
)

if __name__ == "__main__":
    nb.cli()
