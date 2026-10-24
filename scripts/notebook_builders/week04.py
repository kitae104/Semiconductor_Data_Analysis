"""4차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「4차시」. 파이썬 PART만 담는다(Orange Select Columns·Select Rows는 .ows).
활성 개념 4개: read_csv(+ head/shape/columns) · 열 선택 · 조건 검색(한 번 더 고르기 포함) · sort_values.
노출 전용: loc 한 줄(3단계 구경 셀).
빼는 것: loc 활성, iloc, crosstab, 비율 계산 단계(카페), EQ-04 비교 문항.
반도체 확인(7단계)은 읽기·(100, 8)·열 이름·EQ-01(31건 중 불합격 2)·전체 불합격률 13.0%이고,
실습 문제는 세 열 고르기(문제 1)·EQ-02 25건 → 불합격 5건 → 20.0%(문제 2)·온도 상위 5건(문제 3)으로 숫자가 겹치지 않게 했다.
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week04.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

nb = NotebookPair("week04", "4차시 실습 — Pandas 가장 기본적인 부분")

# --- 생활 예제: 카페 주문 12건(완성 코드, 실행하며 관찰) -----------------------------------
nb.add(
    step(1, "CSV 파일 읽기 — read_csv"),
    md("카페 주문 12건(교육용 가상 데이터)입니다. `pd.read_csv(\"파일 경로\", encoding=\"utf-8-sig\")`로 표를 읽어 `cafe`에 담습니다."),
    code('import pandas as pd\n'
         '\n'
         'cafe = pd.read_csv("../../data/weekly/week04/week04_easy_cafe_orders.csv", encoding="utf-8-sig")\n'
         'cafe.head()'),
    look_up("CSV 파일이란"),

    step(2, "표의 크기와 열 이름 확인하기 — shape, columns"),
    md("`shape`는 (행 수, 열 수)입니다. 괄호 `()` 없이 씁니다."),
    code("print(cafe.shape)"),
    code("print(cafe.columns)"),

    step(3, "열 선택하기"),
    md("열 하나는 대괄호 한 겹 `cafe[\"열\"]`, 여러 열은 **대괄호 두 겹** `cafe[[\"열1\", \"열2\"]]`입니다."),
    code('print(cafe["가격_KRW"].head())'),
    code('print(cafe[["메뉴", "가격_KRW", "평가"]].head())'),
    md("(구경) `loc`은 행 번호와 열 이름으로 칸 하나를 꺼냅니다. 실행해서 결과만 보세요."),
    code('print(cafe.loc[0, "가격_KRW"])'),

    step(4, "조건 검색 — 원하는 행만 골라내기"),
    md("`cafe[\"종류\"] == \"커피\"`는 행마다 True/False를 만들고, 그것을 다시 `cafe[ ]`에 넣으면 True인 행만 남습니다."),
    code('check = cafe["종류"] == "커피"\n'
         'print(check.head())'),
    code('coffee = cafe[cafe["종류"] == "커피"]\n'
         'print(coffee.shape)'),
    code('pricey = cafe[cafe["가격_KRW"] > 5000]\n'
         'print(len(pricey))',
         '# TODO: "5000원보다 비싼"을 뜻하는 비교 기호를 채우세요.\n'
         'pricey = cafe[cafe["가격_KRW"] ____ 5000]\n'
         'print(len(pricey))'),
    look_up("pandas 조건 검색"),

    step(5, "골라낸 표에서 한 번 더 고르기"),
    md("고른 표(`pricey`)에서 다시 조건을 걸면 두 조건을 모두 만족하는 행이 남습니다.\n\n"
       "`평가`: 1 = 좋아요, -1 = 별로예요(반도체 데이터의 `합격여부` 1 = 합격, -1 = 불합격과 같은 표기)."),
    code('pricey_bad = pricey[pricey["평가"] == -1]\n'
         'print(len(pricey_bad))'),

    step(6, "정렬하기 — sort_values"),
    md("`ascending=False`는 큰 값부터(내림차순)입니다. 빼면 작은 값부터 정렬합니다."),
    code('cafe.sort_values("가격_KRW", ascending=False).head(5)'),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(7, "반도체 데이터로 확인하기 — 공정 기록 100건"),
    md("공정 기록 100건(교육용 가상 데이터)입니다. 1~5단계와 같은 코드에서 파일 이름·표 이름·열 이름만 바뀝니다. "
       "`합격여부`: 1 = 합격, -1 = 불합격."),
    code('df = pd.read_csv("../../data/weekly/week04/week04_process_filtering.csv", encoding="utf-8-sig")\n'
         'print(df.shape)',
         'df = pd.read_csv("../../data/weekly/week04/week04_process_filtering.csv", encoding="utf-8-sig")\n'
         '# TODO: 표의 (행 수, 열 수)를 보여 주는 이름을 채우세요.\n'
         'print(df.____)'),
    code("print(df.columns)"),
    code('eq01 = df[df["설비번호"] == "EQ-01"]\n'
         'eq01_fail = eq01[eq01["합격여부"] == -1]\n'
         'print(len(eq01), len(eq01_fail))'),
    code('fail = df[df["합격여부"] == -1]\n'
         'print(len(fail) / len(df) * 100)'),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(8, "반도체 데이터 실습"),
    md("7단계 셀을 먼저 실행한 뒤 풀어요. 실습지 문제 1~3과 같은 문제입니다. "
       "오늘의 미션: EQ-02에서 불합격이 몇 건인지 찾아 보고합니다."),

    md("### 문제 1 — 설비번호·온도_C·합격여부 세 열만 고르기",
       student="### 문제 1 — 설비번호·온도_C·합격여부 세 열만 고르기\n\n"
               "- 힌트: 3단계 `cafe[[\"메뉴\", \"가격_KRW\", \"평가\"]]`와 같은 모양. 고른 표는 `small`에 담습니다.\n\n"
               "**주의**: 여러 열을 고를 때 대괄호를 한 겹만 쓰면 `KeyError`가 납니다. 열 이름은 `온도_C`(대문자 C)입니다. "
               "위 셀이 실패하면 `small.head()`에서 `NameError: name 'small' is not defined`가 납니다 — 위 셀부터 고칩니다."),
    code('small = df[["설비번호", "온도_C", "합격여부"]]\n'
         'print(small.shape)',
         '# TODO: 대괄호 안에 세 열 이름이 든 리스트를 채우세요.\n'
         'small = df[____]\n'
         'print(small.shape)'),
    code("small.head()"),

    md("### 문제 2 — EQ-02 기록 고르고, 그중 불합격 세기",
       student="### 문제 2 — EQ-02 기록 고르고, 그중 불합격 세기\n\n"
               "- 힌트: 7단계 EQ-01 코드와 같은 모양. 설비 이름과 불합격 숫자만 바뀝니다.\n\n"
               "**주의**: 두 번째 줄은 `df`가 아니라 고른 표 `eq02`에서 다시 고릅니다. `df`에서 고르면 오류 없이 전체 불합격 13건이 나옵니다.\n\n"
               "- `합격여부`는 숫자라 `-1`에 따옴표를 붙이지 않습니다(`\"-1\"`로 쓰면 오류 없이 0건). 설비번호 `\"EQ-02\"`는 글자라 따옴표를 붙입니다.\n"
               "- 불합격률의 분모를 `df`로 쓰면 오류 없이 5.0%가 나옵니다 — EQ-02 건수(`eq02`)로 나눕니다.\n"
               "- 첫 셀이 실패하면 둘째 셀에서 `NameError: name 'eq02_fail' is not defined`가 납니다 — 첫 셀부터 고칩니다."),
    code('eq02 = df[df["설비번호"] == "EQ-02"]\n'
         'eq02_fail = eq02[eq02["합격여부"] == -1]\n'
         'print(len(eq02), len(eq02_fail))',
         '# TODO: 고를 설비 이름과 불합격을 뜻하는 숫자를 채우세요.\n'
         'eq02 = df[df["설비번호"] == ____]\n'
         'eq02_fail = eq02[eq02["합격여부"] == ____]\n'
         'print(len(eq02), len(eq02_fail))'),
    code('eq02_rate = len(eq02_fail) / len(eq02) * 100\n'
         'print(f"EQ-02 불합격률은 {eq02_rate}%입니다.")',
         '# TODO: 불합격률 = 불합격 건수 ÷ EQ-02 건수 × 100. 나누는 표 이름을 채우세요.\n'
         'eq02_rate = len(eq02_fail) / len(____) * 100\n'
         'print(f"EQ-02 불합격률은 {eq02_rate}%입니다.")'),

    md("### 문제 3 — 온도가 높은 기록 5건 보기",
       student="### 문제 3 — 온도가 높은 기록 5건 보기\n\n"
               "- 빈칸이 없습니다. 아래 빈 셀에 코드를 직접 씁니다.\n"
               "- 힌트: 6단계 `cafe.sort_values(\"가격_KRW\", ascending=False).head(5)`에서 표 이름과 열 이름만 바꿉니다.\n\n"
               "**주의**: `ascending=True`로 쓰면 오류 없이 온도가 **낮은** 5건이 나옵니다."),
    code('df.sort_values("온도_C", ascending=False).head(5)',
         '# TODO: 6단계 cafe.sort_values(...) 코드와 같은 모양으로, 온도_C가 큰 기록 5건을 보는 코드를 직접 쓰세요.\n'),
    look_up("불량률 계산 분모"),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(9, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> pandas 표 df에 \"공정명\"과 \"합격여부\"(1 = 합격, -1 = 불합격) 열이 있어. 공정명마다 기록 수와 불합격 건수를 "
       "한 줄씩 출력하는 짧은 코드를 만들어 줘. 오늘 배운 조건 검색만 써 줘.\n\n"
       "아래는 받은 코드의 예시입니다. `for`는 3차시에 배웠습니다. 실행해서 불합격 건수를 모두 더하면 7단계 전체 불합격 13건(100건 중 13.0%)과 같은지 확인하세요."),
    code('for name in ["산화", "포토", "식각", "증착", "세정"]:\n'
         '    part = df[df["공정명"] == name]\n'
         '    part_fail = part[part["합격여부"] == -1]\n'
         '    print(f"{name}: 기록 {len(part)}건, 불합격 {len(part_fail)}건")'),
)

if __name__ == "__main__":
    nb.cli()
