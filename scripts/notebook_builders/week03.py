"""3차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃.

스펙: _workspace/01_architect_spec.md 「3차시」. 파이썬 PART만 담는다(Orange Select Rows는 .ows).
활성 개념 3개: 비교 연산자 + if/else · for로 개수 세기 · def/return 하나(check_range — "범위 안"/"범위 밖", 합격 판정이 아님).
노출 전용: 없음(elif·+=는 뺐다).
빼는 것: elif 사슬 실습, 누적 합·평균, 두 번째 함수, zip, 반복 중 append 실습.
반도체 확인(6단계)은 EQ-04 기록 8건(범위 밖 4 · 그중 불합격 1), 실습 문제는 EQ-03 온도(문제 2)와
기록 30건 전체(문제 3: 범위 밖 12 · 그중 불합격 3 — Orange Select Rows와 비교)로 숫자가 겹치지 않게 했다.
문제 2는 전이 문제(빈칸 없이 직접 쓰기). AI 단계는 문제 3의 check_range를 써서 문제 3 전에는 답이 보이지 않는다.
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week03.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

# week03_python_basics_2.csv(교육용 가상 데이터)를 옮겨 적은 값 — 3차시는 아직 파일을 코드로 읽지 않는다(4차시 Pandas부터)
EQ04_RECORDS = """eq04_records = [
    {"로트번호": "LOT-0196", "설비번호": "EQ-04", "온도_C": 302.6, "합격여부": 1},
    {"로트번호": "LOT-0141", "설비번호": "EQ-04", "온도_C": 314.1, "합격여부": 1},
    {"로트번호": "LOT-0034", "설비번호": "EQ-04", "온도_C": 318.4, "합격여부": 1},
    {"로트번호": "LOT-0110", "설비번호": "EQ-04", "온도_C": 303.0, "합격여부": 1},
    {"로트번호": "LOT-0031", "설비번호": "EQ-04", "온도_C": 301.8, "합격여부": 1},
    {"로트번호": "LOT-0004", "설비번호": "EQ-04", "온도_C": 295.8, "합격여부": 1},
    {"로트번호": "LOT-0197", "설비번호": "EQ-04", "온도_C": 291.0, "합격여부": 1},
    {"로트번호": "LOT-0085", "설비번호": "EQ-04", "온도_C": 307.0, "합격여부": -1},
]"""
RECORDS = """records = [
    {"로트번호": "LOT-0049", "설비번호": "EQ-03", "온도_C": 304.4, "합격여부": 1},
    {"로트번호": "LOT-0186", "설비번호": "EQ-02", "온도_C": 294.9, "합격여부": 1},
    {"로트번호": "LOT-0196", "설비번호": "EQ-04", "온도_C": 302.6, "합격여부": 1},
    {"로트번호": "LOT-0015", "설비번호": "EQ-01", "온도_C": 295.2, "합격여부": 1},
    {"로트번호": "LOT-0037", "설비번호": "EQ-03", "온도_C": 304.3, "합격여부": 1},
    {"로트번호": "LOT-0186", "설비번호": "EQ-03", "온도_C": 293.8, "합격여부": -1},
    {"로트번호": "LOT-0026", "설비번호": "EQ-02", "온도_C": 297.2, "합격여부": 1},
    {"로트번호": "LOT-0141", "설비번호": "EQ-04", "온도_C": 314.1, "합격여부": 1},
    {"로트번호": "LOT-0032", "설비번호": "EQ-01", "온도_C": 320.3, "합격여부": 1},
    {"로트번호": "LOT-0178", "설비번호": "EQ-02", "온도_C": 303.4, "합격여부": 1},
    {"로트번호": "LOT-0195", "설비번호": "EQ-02", "온도_C": 293.8, "합격여부": -1},
    {"로트번호": "LOT-0034", "설비번호": "EQ-04", "온도_C": 318.4, "합격여부": 1},
    {"로트번호": "LOT-0136", "설비번호": "EQ-01", "온도_C": 297.7, "합격여부": 1},
    {"로트번호": "LOT-0110", "설비번호": "EQ-04", "온도_C": 303.0, "합격여부": 1},
    {"로트번호": "LOT-0119", "설비번호": "EQ-03", "온도_C": 296.7, "합격여부": 1},
    {"로트번호": "LOT-0057", "설비번호": "EQ-03", "온도_C": 308.0, "합격여부": 1},
    {"로트번호": "LOT-0069", "설비번호": "EQ-01", "온도_C": 299.9, "합격여부": 1},
    {"로트번호": "LOT-0170", "설비번호": "EQ-03", "온도_C": 298.8, "합격여부": 1},
    {"로트번호": "LOT-0031", "설비번호": "EQ-04", "온도_C": 301.8, "합격여부": 1},
    {"로트번호": "LOT-0185", "설비번호": "EQ-03", "온도_C": 299.5, "합격여부": 1},
    {"로트번호": "LOT-0004", "설비번호": "EQ-04", "온도_C": 295.8, "합격여부": 1},
    {"로트번호": "LOT-0176", "설비번호": "EQ-03", "온도_C": 297.8, "합격여부": 1},
    {"로트번호": "LOT-0160", "설비번호": "EQ-01", "온도_C": 300.7, "합격여부": 1},
    {"로트번호": "LOT-0016", "설비번호": "EQ-03", "온도_C": 306.3, "합격여부": 1},
    {"로트번호": "LOT-0093", "설비번호": "EQ-03", "온도_C": 301.1, "합격여부": 1},
    {"로트번호": "LOT-0102", "설비번호": "EQ-03", "온도_C": 312.4, "합격여부": 1},
    {"로트번호": "LOT-0197", "설비번호": "EQ-04", "온도_C": 291.0, "합격여부": 1},
    {"로트번호": "LOT-0046", "설비번호": "EQ-02", "온도_C": 316.6, "합격여부": 1},
    {"로트번호": "LOT-0004", "설비번호": "EQ-01", "온도_C": 299.9, "합격여부": 1},
    {"로트번호": "LOT-0085", "설비번호": "EQ-04", "온도_C": 307.0, "합격여부": -1},
]"""
EQ03_TEMPS = "[304.4, 304.3, 293.8, 296.7, 308.0, 298.8, 299.5, 297.8, 306.3, 301.1, 312.4]"

nb = NotebookPair("week03", "3차시 실습 — 조건문·반복문·함수")

# --- 생활 예제(코드 속 값, 완성 코드를 실행하며 관찰) ---------------------------------------
nb.add(
    step(1, "비교 연산자와 if"),
    md("비교 연산자(`>`, `<=`, `==`, `!=`)의 결과는 `True`(참) 또는 `False`(거짓)입니다. "
       "`=`는 저장, `==`는 \"같은가?\" 질문입니다."),
    code('score = 85\n'
         'subject = "수학"\n'
         '\n'
         'print(score > 80)\n'
         'print(score <= 80)\n'
         'print(subject == "수학")\n'
         'print(subject != "수학")'),
    code('if score > 80:\n'
         '    print("80점을 넘었습니다!")\n'
         'print("채점 끝")'),
    look_up("파이썬 들여쓰기 이유"),

    step(2, "if/else로 둘 중 하나 고르기"),
    md("`36.0 <= body_temp <= 37.5`는 \"36.0 이상이고 37.5 이하인가?\"를 한 번에 묻습니다. `if`와 `else` 줄 끝에는 콜론 `:`을 붙입니다."),
    code('body_temp = 36.5\n'
         '\n'
         'if 36.0 <= body_temp <= 37.5:\n'
         '    print("정상 체온입니다.")\n'
         'else:\n'
         '    print("다시 재 보세요.")'),

    step(3, "for로 하나씩 꺼내 개수 세기"),
    code('scores = [72, 85, 90, 64, 88]\n'
         '\n'
         'for score in scores:\n'
         '    print(score)'),
    md("세는 변수는 `for` 바깥에서 0으로 시작합니다."),
    code('pass_count = 0\n'
         '\n'
         'for score in scores:\n'
         '    if score >= 80:\n'
         '        pass_count = pass_count + 1\n'
         '\n'
         'print(f"80점 이상인 학생은 {pass_count}명입니다.")'),
    md("같은 코드에 `print` 한 줄을 넣으면 한 바퀴 돌 때마다 `pass_count`가 어떻게 바뀌는지 보입니다."),
    code('pass_count = 0\n'
         '\n'
         'for score in scores:\n'
         '    if score >= 80:\n'
         '        pass_count = pass_count + 1\n'
         '    print(f"{score}점 | 80점 이상? {score >= 80} | pass_count = {pass_count}")'),

    step(4, "함수 만들기 — def와 return"),
    md("`def`로 판정 규칙에 이름을 붙이고, `return`으로 결과를 돌려줍니다. 정의만 하면 아무것도 실행되지 않고, "
       "이름을 불러야(`judge_score(85)`) 실행됩니다. `judge_score(85)`로 부르면 85가 괄호 안 이름 `point`에 들어갑니다."),
    code('def judge_score(point):\n'
         '    if point >= 80:\n'
         '        return "합격"\n'
         '    else:\n'
         '        return "불합격"\n'
         '\n'
         'print(judge_score(85))\n'
         'print(judge_score(64))'),

    step(5, "함수와 for 함께 쓰기"),
    code('for score in scores:\n'
         '    result = judge_score(score)\n'
         '    print(f"{score}점 → {result}")'),
    code('fail_count = 0\n'
         '\n'
         'for score in scores:\n'
         '    if judge_score(score) == "불합격":\n'
         '        fail_count = fail_count + 1\n'
         '\n'
         'print(f"불합격 판정을 받은 학생: {fail_count}명")'),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(6, "반도체 데이터로 확인하기 — EQ-04 기록 8건"),
    md("`week03_python_basics_2.csv`(교육용 가상 데이터)에서 설비 EQ-04의 기록 8건을 딕셔너리의 리스트로 옮겨 적었습니다. "
       "`합격여부`는 그 공정 뒤 검사에서 나온 실제 결과(행마다)로, `1` = 합격, `-1` = 불합격입니다. "
       "295~305도는 이 과정에서 쓰는 연습용 기준입니다."),
    code(EQ04_RECORDS + "\n"
         "print(len(eq04_records))"),
    code('out_count = 0\n'
         '\n'
         'for record in eq04_records:\n'
         '    if 295 <= record["온도_C"] <= 305:\n'
         '        print(record["로트번호"], record["온도_C"], "범위 안")\n'
         '    else:\n'
         '        print(record["로트번호"], record["온도_C"], "범위 밖 / 합격여부", record["합격여부"])\n'
         '        out_count = out_count + 1\n'
         '\n'
         'print(f"EQ-04 기록 8건 중 범위 밖은 {out_count}건입니다.")'),
    look_up("공정 규격 스펙 뜻"),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(7, "반도체 데이터 실습"),
    md("실습지 문제 1~3과 같은 문제입니다. 범위 295~305도는 연습용 기준입니다."),

    md("### 문제 1 — 온도 하나 판정하기",
       student="### 문제 1 — 온도 하나 판정하기\n\n"
               "- 온도가 295 이상 305 이하이면 `범위 안입니다.`, 아니면 `범위 밖입니다.`를 출력합니다.\n"
               "- 힌트: 2단계 `36.0 <= body_temp <= 37.5`와 같은 모양\n\n"
               "**주의**: `if`와 `else` 줄 끝의 콜론 `:`, 그 아래 줄의 들여쓰기(스페이스 4칸)를 지우지 마세요."),
    code('temperature = 293.8\n'
         '\n'
         'if 295 <= temperature <= 305:\n'
         '    print("범위 안입니다.")\n'
         'else:\n'
         '    print("범위 밖입니다.")',
         'temperature = 293.8\n'
         '\n'
         '# TODO: 범위의 아래 끝과 위 끝 숫자를 채우세요.\n'
         'if ____ <= temperature <= ____:\n'
         '    print("범위 안입니다.")\n'
         'else:\n'
         '    print("범위 밖입니다.")'),

    md("### 문제 2 — EQ-03 온도 중 범위 안인 값 세기 (직접 쓰기)",
       student="### 문제 2 — EQ-03 온도 중 범위 안인 값 세기 (직접 쓰기)\n\n"
               "- 빈칸이 없습니다. 리스트 아래에 세는 코드를 직접 씁니다.\n"
               "- 힌트: 3단계 `pass_count` 코드와 같은 모양. 세는 변수 이름은 `in_count`로, 조건은 문제 1의 `295 <= temp <= 305`로 바꿉니다.\n\n"
               "**주의**: 3단계의 `pass_count`를 그대로 베끼면 3단계 값이 섞여 오류 없이 엉뚱한 숫자가 나옵니다. "
               "`in_count = 0`을 `for` 안으로 옮기면 매번 0으로 돌아갑니다."),
    code('eq03_temps = ' + EQ03_TEMPS + '\n'
         '\n'
         'in_count = 0\n'
         '\n'
         'for temp in eq03_temps:\n'
         '    if 295 <= temp <= 305:\n'
         '        in_count = in_count + 1\n'
         '\n'
         'print(f"EQ-03 온도 {len(eq03_temps)}개 중 범위 안은 {in_count}개입니다.")',
         'eq03_temps = ' + EQ03_TEMPS + '\n'
         '\n'
         '# TODO: 여기에 직접 써 보세요 — in_count를 0으로 시작 → for → if → 1 늘리기 → print\n'),

    md("### 문제 3 — `check_range`로 기록 30건 살펴보기",
       student="### 문제 3 — `check_range`로 기록 30건 살펴보기\n\n"
               "- `check_range(temp)`는 온도가 295~305이면 `\"범위 안\"`, 아니면 `\"범위 밖\"`을 돌려줍니다(4단계 `judge_score`와 같은 모양).\n"
               "- 기록 30건 중 연습용 기준 밖인 기록을 세고, 그중 실제 검사 결과(`합격여부`)가 -1인 기록도 셉니다. "
               "범위 밖이라고 모두 불합격은 아닙니다.\n\n"
               "**주의**: `\"범위 밖\"`의 따옴표를 빼먹으면 `SyntaxError`가 납니다. 비교는 `==`(등호 두 개)입니다."),
    code('def check_range(temp):\n'
         '    if 295 <= temp <= 305:\n'
         '        return "범위 안"\n'
         '    else:\n'
         '        return "범위 밖"\n'
         '\n'
         'print(check_range(301.0))\n'
         'print(check_range(312.6))',
         '# TODO: 결과를 돌려주는 낱말을 채우세요.\n'
         'def check_range(temp):\n'
         '    if 295 <= temp <= 305:\n'
         '        ____ "범위 안"\n'
         '    else:\n'
         '        ____ "범위 밖"\n'
         '\n'
         'print(check_range(301.0))\n'
         'print(check_range(312.6))'),
    code(RECORDS + "\n"
         "print(len(records))"),
    md("함수에 넣는 값은 `temp`가 아니라 지금 꺼낸 기록의 온도 `record[\"온도_C\"]`입니다.",
       student="함수에 넣는 값은 `temp`가 아니라 지금 꺼낸 기록의 온도 `record[\"온도_C\"]`입니다. "
               "위 함수 셀을 먼저 실행하지 않으면 `NameError: name 'check_range' is not defined`가 납니다."),
    code('out_total = 0\n'
         '\n'
         'for record in records:\n'
         '    if check_range(record["온도_C"]) == "범위 밖":\n'
         '        out_total = out_total + 1\n'
         '\n'
         'print(f"연습용 기준 밖 기록: {out_total}건")',
         'out_total = 0\n'
         '\n'
         '# TODO: 함수에 넣을 온도 값(딕셔너리에서 꺼내기)과 비교할 글자를 채우세요.\n'
         'for record in records:\n'
         '    if check_range(____) == ____:\n'
         '        out_total = out_total + 1\n'
         '\n'
         'print(f"연습용 기준 밖 기록: {out_total}건")'),
    code('real_fail = 0\n'
         '\n'
         'for record in records:\n'
         '    if check_range(record["온도_C"]) == "범위 밖":\n'
         '        if record["합격여부"] == -1:\n'
         '            real_fail = real_fail + 1\n'
         '\n'
         'print(f"그중 실제 검사에서 불합격(-1)인 기록: {real_fail}건")',
         'real_fail = 0\n'
         '\n'
         '# TODO: 실제 불합격을 뜻하는 숫자를 채우세요.\n'
         'for record in records:\n'
         '    if check_range(record["온도_C"]) == "범위 밖":\n'
         '        if record["합격여부"] == ____:\n'
         '            real_fail = real_fail + 1\n'
         '\n'
         'print(f"그중 실제 검사에서 불합격(-1)인 기록: {real_fail}건")'),
    look_up("온도만 보고 불량 판단 문제점"),
)

# --- AI로 한 걸음 더(문제 3의 check_range를 써서, 문제 3을 풀기 전에는 답이 보이지 않게) ---------
nb.add(
    step(8, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> records 리스트(딕셔너리마다 \"온도_C\" 키가 있음)에서 check_range 함수가 \"범위 밖\"을 돌려주는 기록만 골라, "
       "305보다 높은 것과 295보다 낮은 것이 각각 몇 건인지 세는 짧은 파이썬 코드를 만들어 줘. if와 for만 써 줘.\n\n"
       "아래는 받은 코드의 예시입니다. 문제 3을 푼 뒤 실행하고, 높음 + 낮음이 문제 3의 개수와 같은지 확인하세요."),
    code('# 문제 3을 푼 뒤 실행하세요.\n'
         'high = 0\n'
         'low = 0\n'
         '\n'
         'for record in records:\n'
         '    temp = record["온도_C"]\n'
         '    if check_range(temp) == "범위 밖":\n'
         '        if temp > 305:\n'
         '            high = high + 1\n'
         '        if temp < 295:\n'
         '            low = low + 1\n'
         '\n'
         'print(f"높음 {high}건, 낮음 {low}건")'),
)

if __name__ == "__main__":
    nb.cli()
