"""6차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「6차시」. 파이썬 PART만 담는다(Orange Scatter Plot·Box Plot은 .ows).
활성 개념 4개: 그래프 4줄 틀(그리기 → xlabel → ylabel → show) · 막대(value_counts + plt.bar) · plt.hist · plt.scatter.
빼는 것: 선 그래프·to_datetime, plt.boxplot / df.boxplot(→ Orange Box Plot), groupby().describe(), axhline, xticks.
반도체 확인(5단계)은 공정명별 건수 · 두께 히스토그램 · 온도-압력 산점도(관계 없음),
실습 문제는 설비별 건수 · 온도 히스토그램 · 온도-두께 산점도(관계 뚜렷)로 같은 열을 반복하지 않게 했다.
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week06.py [--no-execute]
"""
from _common import MPL_KOREAN, NotebookPair, code, look_up, md, step

nb = NotebookPair("week06", "6차시 실습 — 그래프로 공정 상태 이해하기")

# --- 생활 예제: 아이스크림 가게 21일(완성 코드, 실행하며 관찰) -----------------------------
nb.add(
    step(1, "준비하기 — 라이브러리와 데이터"),
    md("아이스크림 가게 3주(21일) 기록(교육용 가상 데이터)입니다. 첫 셀의 두 줄 `plt.rcParams[...]`는 그래프의 한글이 깨지지 않게 합니다(Windows)."),
    code("import pandas as pd\n"
         "import matplotlib.pyplot as plt\n"
         "\n" + MPL_KOREAN),
    code('ice = pd.read_csv("week06_easy_icecream_daily.csv", encoding="utf-8-sig")\n'
         'ice.head()'),

    step(2, "막대그래프 — 날씨별 날 수"),
    md("그래프는 늘 **4줄 틀**입니다: ① 그리기 ② x축 이름 ③ y축 이름 ④ `plt.show()`. "
       "막대는 먼저 `value_counts()`로 개수를 센 뒤 그립니다."),
    code('counts = ice["날씨"].value_counts()\n'
         'print(counts)'),
    code('plt.bar(counts.index, counts)\n'
         'plt.xlabel("날씨")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()'),
    md("### 직접 해 보기 — 요일별 날 수",
       student="### 직접 해 보기 — 요일별 날 수\n\n"
               "- 세는 열 이름을 따옴표와 함께 넣으세요. 나머지 줄은 위와 같은 4줄 틀입니다."),
    code('day_counts = ice["요일"].value_counts()\n'
         'plt.bar(day_counts.index, day_counts)\n'
         'plt.xlabel("요일")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()',
         '# TODO: 세는 열 이름을 따옴표와 함께 채우세요.\n'
         'day_counts = ice[____].value_counts()\n'
         'plt.bar(day_counts.index, day_counts)\n'
         'plt.xlabel("요일")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()'),
    look_up("막대그래프 히스토그램 차이"),

    step(3, "히스토그램 — 판매량이 몰린 구간"),
    md("히스토그램은 숫자 열 하나를 구간으로 나눠 각 구간에 몇 개가 있는지 막대로 보여 줍니다. `bins`는 구간 수입니다."),
    code('plt.hist(ice["판매량_count"], bins=5)\n'
         'plt.xlabel("판매량_count")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()'),
    md("### 직접 해 보기 — 구간 10개로 다시 그리기"),
    code('plt.hist(ice["판매량_count"], bins=10)\n'
         'plt.xlabel("판매량_count")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()',
         '# TODO: 구간 수 10을 채우세요.\n'
         'plt.hist(ice["판매량_count"], bins=____)\n'
         'plt.xlabel("판매량_count")\n'
         'plt.ylabel("날 수")\n'
         'plt.show()'),

    step(4, "산점도 — 기온과 판매량"),
    md("산점도는 두 숫자 열을 x·y로 놓고 행마다 점 하나를 찍습니다. 점이 오른쪽 위로 올라가면 \"함께 커진다\"는 뜻입니다."),
    code('plt.scatter(ice["최고기온_C"], ice["판매량_count"])\n'
         'plt.xlabel("최고기온_C")\n'
         'plt.ylabel("판매량_count")\n'
         'plt.show()'),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(5, "반도체 데이터로 확인하기 — 공정 기록 180건"),
    md("공정 기록 180건(교육용 가상 데이터)입니다. 2~4단계와 같은 4줄 틀에서 표 이름과 열 이름만 바뀝니다."),
    code('df = pd.read_csv("week06_process_visualization.csv", encoding="utf-8-sig")\n'
         'print(df.shape)'),
    code('process_counts = df["공정명"].value_counts()\n'
         'plt.bar(process_counts.index, process_counts)\n'
         'plt.xlabel("공정명")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()'),
    code('plt.hist(df["두께_nm"], bins=10)\n'
         'plt.xlabel("두께_nm")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()'),
    code('plt.scatter(df["온도_C"], df["압력_Pa"])\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("압력_Pa")\n'
         'plt.show()'),
    look_up("박막 두께가 중요한 이유"),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(6, "반도체 데이터 실습"),
    md("5단계 셀을 먼저 실행한 뒤 풀어요. 실습지 문제 1~3과 같은 문제입니다. "
       "오늘의 미션: 다음 회의에서 쓸 그래프 3장 — 설비별 건수, 온도 분포, 온도와 두께의 관계."),

    md("### 문제 1 — 설비별 기록 건수 막대그래프",
       student="### 문제 1 — 설비별 기록 건수 막대그래프\n\n"
               "- 힌트: 5단계 공정명 막대와 같은 모양. 세는 열만 `설비번호`로 바뀝니다.\n\n"
               "**주의**: `value_counts()` 없이 `plt.bar(df[\"설비번호\"])`처럼 열을 바로 넣으면 "
               "`TypeError: bar() missing 1 required positional argument: 'height'`가 납니다."),
    code('eq_counts = df["설비번호"].value_counts()\n'
         'print(eq_counts)',
         '# TODO: 값마다 개수를 세는 함수 이름을 채우세요.\n'
         'eq_counts = df["설비번호"].____()\n'
         'print(eq_counts)'),
    code('plt.bar(eq_counts.index, eq_counts)\n'
         'plt.xlabel("설비번호")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()',
         '# TODO: 막대그래프를 그리는 함수 이름을 채우세요.\n'
         'plt.____(eq_counts.index, eq_counts)\n'
         'plt.xlabel("설비번호")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()'),

    md("### 문제 2 — 온도가 몰린 구간(히스토그램)",
       student="### 문제 2 — 온도가 몰린 구간(히스토그램)\n\n"
               "- 힌트: 5단계 두께 히스토그램과 같은 모양(`bins=10`)\n\n"
               "**주의**: 열 이름은 따옴표 안에 씁니다(`df[\"온도_C\"]`). 5단계 코드를 그대로 옮겨 `df[\"두께_nm\"]`을 넣으면 "
               "오류 없이 두께 그래프가 나옵니다 — x축 숫자가 94~108 근처면 열 이름을 다시 보세요. "
               "마지막 줄 `plt.show()`를 빼먹으면 그래프 위에 `Text(...)` 글자 줄이 함께 보입니다."),
    code('plt.hist(df["온도_C"], bins=10)\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()',
         '# TODO: 히스토그램 함수 이름과 그릴 열 이름을 채우세요.\n'
         'plt.____(df[____], bins=10)\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("기록 건수")\n'
         'plt.show()'),

    md("### 문제 3 — 온도와 두께의 관계(산점도)",
       student="### 문제 3 — 온도와 두께의 관계(산점도)\n\n"
               "- 힌트: 5단계 온도-압력 산점도와 같은 모양. y축 열만 `두께_nm`으로 바뀝니다.\n\n"
               "**주의**: x와 y 순서를 바꾸면 오류 없이 그래프가 옆으로 누운 모양이 됩니다. x = 온도_C, y = 두께_nm."),
    code('plt.scatter(df["온도_C"], df["두께_nm"])\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("두께_nm")\n'
         'plt.show()',
         '# TODO: 산점도 함수 이름과 y축에 놓을 열 이름을 채우세요.\n'
         'plt.____(df["온도_C"], df[____])\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("두께_nm")\n'
         'plt.show()'),
    look_up("상자그림 읽는 법"),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(7, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> pandas 표 df에 \"온도_C\", \"두께_nm\", \"합격여부\"(1 = 합격, -1 = 불합격) 열이 있어. 온도-두께 산점도를 그리는데 "
       "불합격 점만 빨간색으로 겹쳐 그리는 짧은 matplotlib 코드를 만들어 줘.\n\n"
       "아래는 받은 코드의 예시입니다. 4차시 조건 검색으로 불합격 행을 고른 뒤 같은 산점도 위에 한 번 더 찍었습니다. "
       "`color`·`label`·`plt.legend()`는 처음 보는 옵션입니다. 실행해서 빨간 점이 어디에 있는지 보세요."),
    code('fail = df[df["합격여부"] == -1]\n'
         '\n'
         'plt.scatter(df["온도_C"], df["두께_nm"], label="전체")\n'
         'plt.scatter(fail["온도_C"], fail["두께_nm"], color="red", label="불합격")\n'
         'plt.xlabel("온도_C")\n'
         'plt.ylabel("두께_nm")\n'
         'plt.legend()\n'
         'plt.show()'),
)

if __name__ == "__main__":
    nb.cli()
