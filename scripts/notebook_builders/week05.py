"""5차시 노트북 2종(학생용·정답) 빌더 — v3 시범 차시.

스펙: _workspace/01_architect_spec.md 「5차시」. 파이썬 PART만 담는다(Orange Impute는 .ows).
활성 개념 4개: describe() · isna().sum() · dropna() · drop_duplicates()(+ duplicated().sum()). 범위 조건은 4차시 재사용.
빼는 것: fillna(), median(), for로 열 순회(→ Orange Impute가 빈칸 채우기를 맡는다).
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week05.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

nb = NotebookPair("week05", "5차시 실습 — 데이터 훑어보기와 정리(EDA)")

# --- 생활 예제: 반 학생 기록(완성 코드, 실행하며 관찰) -------------------------------------
nb.add(
    step(1, "숫자 요약 보기 — describe()"),
    md("반 학생 15명의 기록(교육용 가상 데이터)입니다. 빈칸 3칸, 똑같이 두 번 적은 행 1개, 잘못 적은 키 1개가 섞여 있습니다."),
    code('import pandas as pd\n'
         '\n'
         'students = pd.read_csv("../../data/weekly/week05/week05_easy_class_records.csv", encoding="utf-8-sig")\n'
         'print(students.shape)'),
    code("print(students.describe())"),
    code('before_count = len(students)\n'
         'before_height = round(students["키_cm"].mean(), 1)\n'
         'print(before_count, before_height)'),

    step(2, "빈칸 세고 지우기 — isna(), dropna()"),
    md("`isna().sum()`은 열마다 빈칸(NaN) 개수를 셉니다. `dropna()`는 빈칸이 하나라도 있는 행을 지웁니다. "
       "**주의**: 지운 결과를 `students =`로 다시 저장해야 남습니다."),
    code("print(students.isna().sum())"),
    code("students = students.dropna()\n"
         "print(students.shape)"),

    step(3, "중복 행 찾고 지우기 — duplicated(), drop_duplicates()"),
    code("print(students.duplicated().sum())"),
    code("students = students.drop_duplicates()\n"
         "print(students.shape)"),

    step(4, "튀는 값 찾기 — 범위 조건"),
    md("사람 키가 250cm를 넘는 일은 거의 없습니다. 오늘은 250cm를 넘으면 잘못 적은 값으로 보고, 4차시에 배운 조건 검색으로 찾아봅니다."),
    code('tall = students[students["키_cm"] > 250]\n'
         'print(tall)'),

    step(5, "튀는 값 빼고 전후 비교하기"),
    code('students = students[students["키_cm"] <= 250]\n'
         'print(students.shape)'),
    code('after_height = round(students["키_cm"].mean(), 1)\n'
         'print("정리 전 평균 키:", before_height)\n'
         'print("정리 후 평균 키:", after_height)'),
    look_up("평균과 중앙값 차이"),
)

# --- 반도체 데이터로 확인하기(강의 같은 이름 절과 같은 완성 코드) ----------------------------
nb.add(
    step(6, "반도체 데이터로 확인하기 — 지저분한 공장 기록"),
    md("공정 기록 113행(교육용 가상 데이터)에 빈칸·중복·튀는 값을 일부러 섞었습니다. 1~3단계와 같은 코드에서 표 이름만 바뀝니다."),
    code('df = pd.read_csv("../../data/weekly/week05/week05_dirty_process_data.csv", encoding="utf-8-sig")\n'
         'print(df.shape)'),
    code("print(df.describe())"),
    code("print(df.isna().sum())"),
    code("print(df.duplicated().sum())"),
    code('hot = df[df["온도_C"] > 400]\n'
         'print(hot)'),
)

# --- 반도체 데이터 실습(실습지 문제 1~3과 같은 번호, PART 3에서 채운다) -----------------------
nb.add(
    step(7, "반도체 데이터 실습"),
    md("6단계 셀을 먼저 실행한 뒤 풀어요. 실습지 문제 1~3과 같은 문제입니다."),

    md("### 문제 1 — 압력 열 요약하고 빈칸 세기",
       student="### 문제 1 — 압력 열 요약하고 빈칸 세기\n\n"
               "`압력_Pa` 열 하나만 요약하고, 그 열의 빈칸 수를 세세요. 힌트: 1·2단계와 같은 함수"),
    code('print(df["압력_Pa"].describe())',
         "# TODO: 숫자 요약을 보여 주는 함수 이름을 채우세요.\n"
         'print(df["압력_Pa"].____())'),
    code('print(df["압력_Pa"].isna().sum())',
         "# TODO: 빈칸인지 확인하는 함수 이름을 채우세요.\n"
         'print(df["압력_Pa"].____().sum())'),

    md("### 문제 2 — 빈칸 행과 중복 행 지우고 행 수 확인하기",
       student="### 문제 2 — 빈칸 행과 중복 행 지우고 행 수 확인하기\n\n"
               "정리한 표는 `clean`에 담습니다. 원래 표 `df`는 문제 3에서 비교할 때 씁니다.\n\n"
               "**주의**: 함수 뒤 괄호 `()`를 빼먹으면 표가 아니라 함수가 저장됩니다."),
    code("clean = df.dropna()\n"
         "print(clean.shape)",
         "# TODO: 빈칸이 있는 행을 지우는 함수 이름을 채우세요.\n"
         "clean = df.____()\n"
         "print(clean.shape)"),
    code("clean = clean.drop_duplicates()\n"
         "print(clean.shape)",
         "# TODO: 중복 행을 지우는 함수 이름을 채우세요.\n"
         "clean = clean.____()\n"
         "print(clean.shape)"),

    md("### 문제 3 — 평소 범위를 크게 벗어난 값 빼고 평균 온도 비교하기",
       student="### 문제 3 — 평소 범위를 크게 벗어난 값 빼고 평균 온도 비교하기\n\n"
               "남길 범위(교육용 기준): 온도 400 이하, 압력 0 이상, 가스유량 0 이상 200 미만. 540도·557도 같은 온도는 이 기록의 평소 범위(295~305도)에서 크게 벗어난 값입니다. 힌트: 5단계 `<=` 조건과 같은 모양\n\n"
               "**주의**: 부등호 방향을 반대로 쓰면 정상 행이 지워지고 튀는 값만 남습니다."),
    code('clean = clean[clean["온도_C"] <= 400]\n'
         'clean = clean[clean["압력_Pa"] >= 0]\n'
         'clean = clean[clean["가스유량_slm"] >= 0]\n'
         'clean = clean[clean["가스유량_slm"] < 200]\n'
         'print(clean.shape)',
         "# TODO: 온도는 400 이하, 압력은 0 이상만 남도록 비교 기호를 채우세요.\n"
         'clean = clean[clean["온도_C"] ____ 400]\n'
         'clean = clean[clean["압력_Pa"] ____ 0]\n'
         'clean = clean[clean["가스유량_slm"] >= 0]\n'
         'clean = clean[clean["가스유량_slm"] < 200]\n'
         'print(clean.shape)'),
    code('print("정리 전 평균 온도:", round(df["온도_C"].mean(), 1))\n'
         'print("정리 후 평균 온도:", round(clean["온도_C"].mean(), 1))',
         "# TODO: 정리한 표 이름을 채우세요.\n"
         'print("정리 전 평균 온도:", round(df["온도_C"].mean(), 1))\n'
         'print("정리 후 평균 온도:", round(____["온도_C"].mean(), 1))'),
)

# --- AI로 한 걸음 더 ----------------------------------------------------------------
nb.add(
    step(8, "AI로 한 걸음 더"),
    md("ChatGPT에 이렇게 물어봤습니다.\n\n"
       "> week05_dirty_process_data.csv를 pandas로 읽어서(encoding=\"utf-8-sig\"), 열마다 빈칸 개수와 "
       "빈칸 비율(%)을 한 줄씩 출력하는 짧은 코드를 만들어 줘.\n\n"
       "아래는 받은 코드의 예시입니다. `for`는 3차시에 배운 반복문입니다. 실행해서 6단계 `isna().sum()` 결과와 같은지 확인하세요."),
    code('import pandas as pd\n'
         '\n'
         'data = pd.read_csv("../../data/weekly/week05/week05_dirty_process_data.csv", encoding="utf-8-sig")\n'
         '\n'
         'for col in data.columns:\n'
         '    count = data[col].isna().sum()\n'
         '    rate = count / len(data) * 100\n'
         '    print(f"{col}: 빈칸 {count}개 ({rate:.1f}%)")'),
)

if __name__ == "__main__":
    nb.cli()
