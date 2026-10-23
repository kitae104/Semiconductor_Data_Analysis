"""2차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「2차시」. 파이썬 PART만 담는다(Orange Feature Statistics는 .ows).
활성 개념 4개: 리스트·인덱스 · len()/append() · max()/min()/sum() · 딕셔너리.
노출 전용: 딕셔너리의 리스트(5단계 구경, 완성 코드), round()(평균을 소수 첫째 자리로 — 5차시와 같은 방식).
빼는 것: 슬라이싱 실습, 딕셔너리 값 바꾸기·키 추가, 딕셔너리의 리스트 실습 문제.
반도체 확인(6단계)은 EQ-02, 실습 문제 1~3은 EQ-03(오늘의 미션)으로 숫자가 겹치지 않게 했다.
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week02.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

nb = NotebookPair("week02", "2차시 실습 — 리스트와 딕셔너리")

# --- 생활 예제(코드 속 값, 완성 코드를 실행하며 관찰) ---------------------------------------
nb.add(
    step(1, "리스트 만들고 인덱스로 꺼내기"),
    md("리스트는 대괄호 `[ ]` 안에 값을 쉼표로 늘어놓은 것입니다. 칸 번호(인덱스)는 **0부터** 셉니다."),
    code("week_temps = [21.5, 23.0, 30.5, 24.0, 22.5, 25.0, 23.5]   # 월~일 낮 기온\n"
         "print(week_temps)"),
    code("print(week_temps[0])    # 첫 번째 값(월요일)\n"
         "print(week_temps[2])    # 세 번째 값(수요일)\n"
         "print(week_temps[-1])   # 마지막 값(일요일)"),
    look_up("파이썬 리스트 인덱스 0부터"),

    step(2, "개수 세고 값 추가하기 — len(), append()"),
    code('cart = ["우유", "빵", "계란"]\n'
         "print(len(cart))"),
    code('cart.append("사과")\n'
         "print(cart)\n"
         "print(len(cart))"),

    step(3, "최고·최저·평균 구하기 — max(), min(), sum()"),
    code("print(max(week_temps))\n"
         "print(min(week_temps))\n"
         "print(sum(week_temps))"),
    md("평균 = 합계 ÷ 개수입니다. `round(값, 1)`은 소수 첫째 자리까지 반올림합니다."),
    code("average = round(sum(week_temps) / len(week_temps), 1)\n"
         'print(f"이번 주 평균 기온은 {average}도입니다.")'),

    step(4, "딕셔너리 만들고 키로 꺼내기"),
    md("딕셔너리는 중괄호 `{ }` 안에 `\"이름표\": 값`을 쌍으로 적습니다. 꺼낼 때는 대괄호에 이름표(키)를 씁니다."),
    code("student = {\n"
         '    "이름": "지민",\n'
         '    "나이": 15,\n'
         '    "반": 3,\n'
         "}\n"
         "print(student)"),
    code('print(student["이름"])\n'
         'print(student["반"])\n'
         '# print(student["혈액형"])   # 없는 이름표 → KeyError'),
    look_up("파이썬 리스트와 딕셔너리 차이"),

    step(5, "(구경) 딕셔너리의 리스트 — 표의 한 행 = 딕셔너리 하나"),
    md("실행해서 모양만 보세요. 4차시에 배우는 표(Pandas)가 이런 모양을 한 번에 다룹니다."),
    code("friends = [\n"
         '    {"이름": "지민", "나이": 15, "동네": "서울"},\n'
         '    {"이름": "서준", "나이": 16, "동네": "부산"},\n'
         '    {"이름": "하은", "나이": 15, "동네": "대전"},\n'
         "]\n"
         "print(len(friends))\n"
         'print(friends[1]["이름"])'),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(6, "반도체 데이터로 확인하기 — EQ-02 설비 온도"),
    md("`week02_python_basics_1.csv`(교육용 가상 데이터)에서 설비 EQ-02의 온도 4개를 옮겨 적었습니다. "
       "1~4단계와 같은 코드에서 이름과 값만 바뀝니다."),
    code("eq02_temps = [302.5, 299.8, 298.8, 305.6]\n"
         "print(len(eq02_temps))\n"
         "print(max(eq02_temps))\n"
         "print(min(eq02_temps))"),
    code("eq02_avg = round(sum(eq02_temps) / len(eq02_temps), 1)\n"
         'print(f"EQ-02 평균 온도는 {eq02_avg}도입니다.")'),
    code('first = {"로트번호": "LOT-0122", "설비번호": "EQ-02", "온도_C": 302.5}\n'
         'print(first["온도_C"])'),
    look_up("반도체 로트 뜻"),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(7, "반도체 데이터 실습"),
    md("실습지 문제 1~3과 같은 문제입니다. 오늘의 미션: 팀장이 준 EQ-03 설비 온도 7개를 정리해 보고합니다."),

    md("### 문제 1 — EQ-03 온도 리스트의 첫 값·마지막 값·개수",
       student="### 문제 1 — EQ-03 온도 리스트의 첫 값·마지막 값·개수\n\n"
               "- 첫 값은 몇 번 칸일까요? 인덱스는 0부터 셉니다. 마지막 값은 `-1`번 칸입니다(1단계).\n"
               "- 개수는 2단계의 함수로 셉니다."),
    code("eq03_temps = [303.8, 303.4, 292.2, 308.5, 307.5, 298.5, 304.0]\n"
         "print(eq03_temps[0])\n"
         "print(eq03_temps[-1])",
         "eq03_temps = [303.8, 303.4, 292.2, 308.5, 307.5, 298.5, 304.0]\n"
         "# TODO: 첫 값과 마지막 값의 칸 번호를 채우세요.\n"
         "print(eq03_temps[____])\n"
         "print(eq03_temps[____])"),
    code("print(len(eq03_temps))",
         "# TODO: 리스트의 개수를 세는 함수 이름을 채우세요.\n"
         "print(____(eq03_temps))"),

    md("### 문제 2 — EQ-03 최고·최저·평균 온도",
       student="### 문제 2 — EQ-03 최고·최저·평균 온도\n\n"
               "- 힌트: 3단계의 `max()`, `min()`, `sum()`과 같은 모양입니다.\n\n"
               "**주의**: 6단계의 `eq02_temps`가 아니라 `eq03_temps`를 넣습니다. 다른 리스트를 쓰면 오류 없이 다른 숫자가 나옵니다."),
    code("print(max(eq03_temps))\n"
         "print(min(eq03_temps))",
         "# TODO: 가장 큰 값과 가장 작은 값을 구하는 함수 이름을 채우세요.\n"
         "print(____(eq03_temps))\n"
         "print(____(eq03_temps))"),
    code("eq03_avg = round(sum(eq03_temps) / len(eq03_temps), 1)\n"
         'print(f"EQ-03 평균 온도는 {eq03_avg}도입니다.")',
         "# TODO: 합계를 구하는 함수 이름을 채우세요.\n"
         "eq03_avg = round(____(eq03_temps) / len(eq03_temps), 1)\n"
         'print(f"EQ-03 평균 온도는 {eq03_avg}도입니다.")'),

    md("### 문제 3 — `report` 딕셔너리로 묶고 평균 꺼내기",
       student="### 문제 3 — `report` 딕셔너리로 묶고 평균 꺼내기\n\n"
               "- 문제 2에서 구한 평균은 `eq03_avg`에 들어 있습니다.\n"
               "- 키로 꺼낼 때는 따옴표까지 씁니다(4단계 `student[\"이름\"]`).\n\n"
               "**주의**: 딕셔너리는 중괄호 `{ }`로 감쌉니다(대괄호로 감싸면 `SyntaxError`). 문제 2 셀을 먼저 실행해야 `eq03_avg`가 있습니다."),
    code("report = {\n"
         '    "설비번호": "EQ-03",\n'
         '    "최고": max(eq03_temps),\n'
         '    "최저": min(eq03_temps),\n'
         '    "평균": eq03_avg,\n'
         "}\n"
         "print(report)",
         "# TODO: \"평균\" 이름표에 문제 2에서 구한 평균 변수를 채우세요.\n"
         "report = {\n"
         '    "설비번호": "EQ-03",\n'
         '    "최고": max(eq03_temps),\n'
         '    "최저": min(eq03_temps),\n'
         '    "평균": ____,\n'
         "}\n"
         "print(report)"),
    code('print(report["평균"])',
         "# TODO: 평균을 꺼내는 이름표(따옴표 포함)를 채우세요.\n"
         "print(report[____])"),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(8, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> 파이썬 리스트 eq03_temps = [303.8, 303.4, 292.2, 308.5, 307.5, 298.5, 304.0]에서 "
       "295 이상 305 이하 범위를 벗어난 값만 골라 개수와 함께 출력하는 짧은 코드를 만들어 줘.\n\n"
       "아래는 받은 코드의 예시입니다. `for`와 `if`는 3차시에 배웁니다. 지금은 실행해서 결과만 확인하세요. "
       "295~305는 이 과정에서 쓰는 연습용 기준입니다."),
    code("eq03_temps = [303.8, 303.4, 292.2, 308.5, 307.5, 298.5, 304.0]\n"
         "\n"
         "out_of_range = []\n"
         "for t in eq03_temps:\n"
         "    if t < 295 or t > 305:\n"
         "        out_of_range.append(t)\n"
         "\n"
         'print(f"범위 밖 온도: {out_of_range}")\n'
         'print(f"범위 밖 개수: {len(out_of_range)}개")'),
)

if __name__ == "__main__":
    nb.cli()
