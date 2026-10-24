"""1차시 노트북 2종(학생용·정답) 빌더 — v3 시범 차시.

스펙: _workspace/01_architect_spec.md 「1차시」. 파이썬 PART만 담는다(Orange는 .ows).
활성 개념 4개: `=`(계산 결과 저장 포함) · print() · f-string({변수}만) · type().
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다(노트북 셀을 이어 붙이면 강의 코드).

실행: python scripts/notebook_builders/week01.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

nb = NotebookPair("week01", "1차시 실습 — 변수와 출력")

# --- 생활 예제(완성 코드, 실행하며 관찰) -------------------------------------------
nb.add(
    step(1, "첫 셀 실행하기(환경 확인)"),
    md("셀을 한 번 클릭하고 **Shift + Enter**를 누르세요. 아래에 문장이 나오면 준비 끝입니다."),
    code('print("파이썬 준비 완료!")'),

    step(2, "변수에 값 저장하기"),
    md("`=`는 \"같다\"가 아니라 \"오른쪽 값을 왼쪽 이름표에 저장하라\"는 뜻입니다."),
    code("coffee_price = 4500\n"
         "cups = 3\n"
         "\n"
         "print(coffee_price)\n"
         "print(cups)"),
    code("total_price = coffee_price * cups\n"
         "print(total_price)"),
    look_up("파이썬 변수 뜻"),

    step(3, "자료형 확인하기 — type()"),
    md("`int` = 정수, `float` = 소수점이 있는 수, `str` = 글자(문자열)."),
    code('rating = 4.5\n'
         'menu = "아메리카노"\n'
         '\n'
         'print(type(cups))\n'
         'print(type(rating))\n'
         'print(type(menu))'),

    step(4, "print()와 f-string으로 문장 만들기"),
    md("f-string은 따옴표 앞에 `f`를 붙이고, 값이 들어갈 자리에 `{변수 이름}`을 씁니다. "
       "**주의**: `f`를 빼먹으면 중괄호가 글자 그대로 나옵니다."),
    code('print("메뉴:", menu, "잔 수:", cups)'),
    code('print(f"{menu} {cups}잔 주문이 들어왔습니다.")'),

    step(5, "계산한 값을 문장에 넣기"),
    md("따뜻한 커피 6잔, 아이스 4잔이 팔렸습니다."),
    code("hot_count = 6\n"
         "ice_count = 4\n"
         "\n"
         "total = hot_count + ice_count\n"
         "ice_rate = ice_count / total * 100\n"
         "print(total, ice_rate)"),
    code('print(f"전체 {total}잔 중 아이스는 {ice_rate}%입니다.")'),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(6, "반도체 데이터로 확인하기 — 공장 기록 40건"),
    md("공장 기록표(교육용 가상 데이터) 40건에서 `합격여부`를 센 결과입니다. 1 = 합격, -1 = 불합격. "
       "Orange의 Distributions 막대 높이와 같은 숫자입니다."),
    code("pass_count = 32\n"
         "fail_count = 8\n"
         "total_count = pass_count + fail_count\n"
         "\n"
         'print(f"오늘 기록 {total_count}건 중 합격은 {pass_count}건, 불합격은 {fail_count}건입니다.")'),
    code("fail_rate = fail_count / total_count * 100\n"
         'print(f"불합격률은 {fail_rate}%입니다.")'),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(7, "반도체 데이터 실습"),
    md("실습지 문제 1~3과 같은 문제입니다."),

    md("### 문제 1 — EQ-03 설비의 기록 수와 불합격 수 담기\n\n설비 EQ-03의 기록은 12건, 그중 불합격은 3건입니다.",
       student="### 문제 1 — EQ-03 설비의 기록 수와 불합격 수 담기\n\n"
               "설비 EQ-03의 기록은 12건, 그중 불합격은 3건입니다. 두 값을 저장하세요. 힌트: 6단계 `pass_count = 32`와 같은 모양"),
    code("eq03_count = 12\n"
         "eq03_fail = 3\n"
         "\n"
         "print(eq03_count)\n"
         "print(eq03_fail)",
         "# TODO: eq03_count에 12, eq03_fail에 3을 저장하세요.\n"
         "eq03_count = ____\n"
         "eq03_fail = ____\n"
         "\n"
         "print(eq03_count)\n"
         "print(eq03_fail)"),

    md("### 문제 2 — f-string으로 EQ-03 보고 문장 만들기",
       student="### 문제 2 — f-string으로 EQ-03 보고 문장 만들기\n\n"
               "`EQ-03 기록 12건 중 불합격은 3건입니다.`를 출력하세요. 힌트: 4단계 `f\"{menu} {cups}잔 …\"`과 같은 모양"),
    code('print(f"EQ-03 기록 {eq03_count}건 중 불합격은 {eq03_fail}건입니다.")',
         "# TODO: 따옴표 앞 글자 하나와 불합격 건수가 든 변수 이름을 채우세요.\n"
         'print(____"EQ-03 기록 {eq03_count}건 중 불합격은 {____}건입니다.")'),

    md("### 문제 3 — EQ-03 불합격률 계산하고 자료형 확인하기",
       student="### 문제 3 — EQ-03 불합격률 계산하고 자료형 확인하기\n\n"
               "불합격률 = 불합격 건수 ÷ 전체 건수 × 100. 힌트: 6단계 `fail_rate` 계산과 같은 모양\n\n"
               "**주의**: 나누는 수는 공장 전체(`total_count`, 40)나 카페의 `total`(10)이 아니라 EQ-03의 기록 수(`eq03_count`, 12)입니다. "
               "다른 변수를 쓰면 오류 없이 엉뚱한 숫자가 나옵니다."),
    code("eq03_rate = eq03_fail / eq03_count * 100\n"
         'print(f"EQ-03 불합격률은 {eq03_rate}%입니다.")',
         "# TODO: 불합격 건수와 전체 건수가 든 변수 이름을 채우세요.\n"
         "eq03_rate = ____ / ____ * 100\n"
         'print(f"EQ-03 불합격률은 {eq03_rate}%입니다.")'),
    code("print(type(eq03_rate))",
         "# TODO: 자료형을 알려 주는 함수 이름을 채우세요.\n"
         "print(____(eq03_rate))"),
)

if __name__ == "__main__":
    nb.cli()
