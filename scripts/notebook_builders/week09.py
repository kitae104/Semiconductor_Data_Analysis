"""9차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃(Orange 중심 차시, 파이썬 최소 + ChatGPT 체험).

스펙: _workspace/01_architect_spec.md 「9차시」. 파이썬 PART만 담는다(Orange Tree·Test and Score는 .ows). 생활 예제 단계 없음.
활성 개념 4개: Feature/Label(X, y) · train_test_split · DecisionTreeClassifier().fit · accuracy_score.
재사용: read_csv·dropna(5차시). 노출 전용: model.predict(정확도 계산 안에서 — 10차시 활성 개념).
빼는 것: 생활 예제 단계, confusion_matrix, feature_importances_, zip, 기준선 코드(기준선 78.9%는 값으로만).
노트북: 막혔을 때 → 1 읽고 빈칸 정리 → 2 결정 트리 모델 만들기(강의 PART 2 따라 하기, 6개 열 80.3%)
→ 3 ChatGPT 코드 실행·검증(빈 셀 + 응답 예시 셀 + stratify 빼 보기 셀) → 4 반도체 데이터 실습(문제 1·2: 온도_C 한 열 모델 78.2%).
ChatGPT 체험이 PART 2 안에 있어서 3·4단계를 강의 순서(PART 2 → PART 3)대로 두었다(Run All 순서 = 수업 순서).
PART 2가 수동적이지 않게 1·2단계에 학생 빈칸 4개(dropna, "합격여부", fit, y_test)를 두고, 실습 문제는 다른 Feature(온도_C 한 열)로
숫자가 겹치지 않게 했다. 문제 2는 전이 문제(2단계 코드 모양을 빈칸 없이 직접 쓰기).
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week09.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

DATA = "../../data/weekly/week09/week09_pass_fail_train.csv"

# ChatGPT 응답 예시(완성 코드). "직접 바꿔 보기" 정답 셀은 이 코드에서 나누는 줄의 stratify=y만 뺀 것이다.
SPLIT_LINE = "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
RESPONSE_EXAMPLE = ("# 1) 데이터 읽기와 빈칸 정리\n"
                    "import pandas as pd\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "from sklearn.metrics import accuracy_score\n"
                    "\n"
                    f'data = pd.read_csv("{DATA}", encoding="utf-8-sig").dropna()\n'
                    "# 2) 입력(X)과 정답(y) 나누기\n"
                    'X = data[["온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"]]\n'
                    'y = data["합격여부"]\n'
                    "# 3) 학습용·시험용으로 나누고 결정 트리 학습\n"
                    + SPLIT_LINE +
                    "clf = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_tr, y_tr)\n"
                    "# 4) 정확도 출력\n"
                    'print("정확도:", accuracy_score(y_te, clf.predict(X_te)))')
NO_STRATIFY = RESPONSE_EXAMPLE.replace(
    SPLIT_LINE, "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n")
assert NO_STRATIFY != RESPONSE_EXAMPLE

nb = NotebookPair("week09", "9차시 실습 — 머신러닝 예측 모델 만들기")

nb.add(
    step(1, "데이터 읽고 빈칸 정리하기"),
    md("공정 기록 750행(교육용 가상 데이터)입니다. `합격여부`: 1 = 합격, -1 = 불합격. "
       "설비 4대(EQ-01~EQ-04)가 여러 공정 기록을 함께 남겼다(교육용 가상 기록). "
       "빈칸(NaN)이 있으면 모델 종류에 따라 오류가 나거나 결과가 달라지므로, 5차시의 `dropna()`로 빈칸 행을 먼저 지웁니다.",
       student="공정 기록 750행(교육용 가상 데이터)입니다. `합격여부`: 1 = 합격, -1 = 불합격. "
               "설비 4대(EQ-01~EQ-04)가 여러 공정 기록을 함께 남겼다(교육용 가상 기록). "
               "빈칸(NaN)이 있으면 모델 종류에 따라 오류가 나거나 결과가 달라지므로, 빈칸 행을 먼저 지웁니다.\n\n"
               "- 빈칸 행 지우기는 5차시에 배운 함수입니다. 결과가 `(735, 9)`이면 맞습니다."),
    code('import pandas as pd\n'
         '\n'
         f'df = pd.read_csv("{DATA}", encoding="utf-8-sig")\n'
         'print(df.shape)'),
    code("print(df.isna().sum())"),
    code("df = df.dropna()\n"
         "print(df.shape)",
         "# TODO: 빈칸이 있는 행을 지우는 함수 이름을 채우세요.\n"
         "df = df.____()\n"
         "print(df.shape)"),
)

nb.add(
    step(2, "결정 트리 모델 만들기"),
    md("강의 PART 2에서 함께 따라 하는 코드입니다. 오늘의 미션: 검사 전에 합격/불합격을 미리 맞히는 모델을 만들고, "
       "\"무조건 합격\"이라고 찍는 것(기준선)보다 나은지 비교합니다.",
       student="강의 PART 2에서 함께 따라 하는 코드입니다. 오늘의 미션: 검사 전에 합격/불합격을 미리 맞히는 모델을 만들고, "
               "\"무조건 합격\"이라고 찍는 것(기준선)보다 나은지 비교합니다.\n\n"
               "- X(Feature) = 모델이 보고 판단할 열 6개, y(Label) = 맞혀야 할 정답 열 `합격여부`.\n"
               "- 비교 기준: 시험용 147개를 모두 \"합격\"이라고 찍으면 정확도는 78.9%입니다(기준선).\n\n"
               "**주의**: X에 `합격여부`를 넣으면 정답을 보고 맞히는 셈이라 정확도가 100%에 가깝게 나옵니다(정답 누설). "
               "`공정명`·`설비번호`는 글자 열이라 오늘은 넣지 않습니다."),
    code('features = ["온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"]\n'
         'X = df[features]\n'
         'y = df["합격여부"]\n'
         'print(X.shape, y.shape)',
         'features = ["온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"]\n'
         'X = df[features]\n'
         '# TODO: 정답(Label) 열 이름을 채우세요.\n'
         'y = df[____]\n'
         'print(X.shape, y.shape)'),
    code("from sklearn.model_selection import train_test_split\n"
         "\n"
         "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
         "print(len(X_train), len(X_test))"),
    look_up("결정 트리 스무고개"),
    code("from sklearn.tree import DecisionTreeClassifier\n"
         "\n"
         "model = DecisionTreeClassifier(max_depth=4, random_state=42)\n"
         "model.fit(X_train, y_train)",
         "from sklearn.tree import DecisionTreeClassifier\n"
         "\n"
         "model = DecisionTreeClassifier(max_depth=4, random_state=42)\n"
         "# TODO: 학습시키는 함수 이름을 채우세요.\n"
         "model.____(X_train, y_train)"),
    code("from sklearn.metrics import accuracy_score\n"
         "\n"
         "acc = accuracy_score(y_test, model.predict(X_test))\n"
         'print(f"정확도: {round(acc * 100, 1)}%")',
         "from sklearn.metrics import accuracy_score\n"
         "\n"
         "# TODO: 채점에 쓰는 정답은 시험용 y입니다. 그 이름을 채우세요.\n"
         "acc = accuracy_score(____, model.predict(X_test))\n"
         'print(f"정확도: {round(acc * 100, 1)}%")'),
    md("이 모델은 시험용 불합격 31개 중 9개만 잡고 22개를 합격으로 놓쳤습니다. '무조건 합격'은 31개를 모두 놓칩니다. "
       "정확도가 비슷해도 하는 일은 다릅니다 — 실습지 문제 4에서 Orange 헷갈림 표로 같은 것을 셉니다."),
    look_up("정확도의 함정 불균형 데이터"),
)

nb.add(
    step(3, "ChatGPT 체험 — 받은 코드 실행하고 숫자 검증하기"),
    md("ChatGPT에 아래 프롬프트를 그대로 붙여 넣으세요(강의 자료와 같은 글자입니다).\n\n"
       f"> {DATA} 파일을 pandas로 읽어(encoding=\"utf-8-sig\") 빈칸이 있는 행을 지우고, "
       "온도_C·압력_Pa·가스유량_slm·두께_nm·진공도_mTorr·습도_pct 여섯 열로 합격여부(1 = 합격, -1 = 불합격)를 예측하는 결정 트리를 만들어 줘. "
       "train_test_split(test_size=0.2, random_state=42, stratify=y)와 DecisionTreeClassifier(max_depth=4, random_state=42)를 쓰고 "
       "시험용 정확도를 출력해 줘. 10줄 이내, 한국어 주석으로. 교육용 가상 데이터야."),
    code("# ChatGPT가 준 코드를 여기에 붙여 넣고 실행하세요."),
    md("**응답 예시(실제 AI 응답 아님)** — ChatGPT를 쓸 수 없으면 아래 셀을 실행하세요."),
    code(RESPONSE_EXAMPLE),
    md("**검증**: 받은 코드의 정확도가 2단계에서 직접 만든 숫자(6개 열 모델)와 같은가요? 응답 예시는 `0.8027…`처럼 0~1 사이 소수로 찍습니다 — "
       "× 100 하면 80.3%로 같습니다. 숫자가 다르면 AI가 빠뜨린 조건(`dropna`, `test_size`, `random_state`, `stratify`, `max_depth`, 열 6개)을 하나씩 찾아보세요."),
    md("**직접 바꿔 보기**: 위 응답 예시 셀을 복사해 아래 셀에 붙여 넣고, `stratify=y`만 지운 뒤 실행해 보세요. "
       "오류 없이 숫자만 달라집니다. 강의 \"응답 예시 실행 결과\" 표와 비교하세요."),
    code(NO_STRATIFY,
         "# TODO: 응답 예시를 붙여 넣고 stratify=y만 지워서 실행해 보세요."),
)

nb.add(
    step(4, "반도체 데이터 실습"),
    md("실습지 문제 1~2와 같은 문제입니다. Orange Tree Viewer의 첫 갈림길은 `온도_C`였습니다. "
       "그렇다면 `온도_C` 한 열만 보는 모델은 6개 열 모델(2단계)이나 기준선(78.9%)과 비교해 어떨까요?"),
    md("4단계 숫자가 실습지와 다르면 Kernel → Restart Kernel and Run All Cells… 로 처음부터 다시 실행합니다"
       "(3단계에 붙여 넣은 코드가 df·y를 바꿨을 수 있다)."),

    md("### 문제 1 — `온도_C` 한 열로 Feature 만들고, 학습용·시험용으로 나누기",
       student="### 문제 1 — `온도_C` 한 열로 Feature 만들고, 학습용·시험용으로 나누기\n\n"
               "- 2단계 `features`처럼 열 이름을 리스트(대괄호)에 넣습니다. 열이 하나여도 리스트로 씁니다.\n"
               "- 나누는 줄은 2단계와 같고, 이름에만 `1`을 붙였습니다. y는 2단계의 `y`를 그대로 씁니다.\n\n"
               "**주의**: 열 이름은 따옴표로 감쌉니다. `X1 = df[features]`로 쓰면 오류 없이 6개 열이 들어가 2단계와 같은 모델이 됩니다. "
               "`(735,)`가 나오면 대괄호가 빠진 것입니다(`temp_features = \"온도_C\"`). "
               "그대로 학습하면 `ValueError: Expected a 2-dimensional container but got <class 'pandas.Series'> instead.`로 시작하는 오류가 납니다."),
    code('temp_features = ["온도_C"]\n'
         'X1 = df[temp_features]\n'
         'print(X1.shape)',
         '# TODO: 온도 열 이름 하나를 리스트에 넣고, 그 리스트 변수 이름으로 X1을 만드세요.\n'
         'temp_features = [____]\n'
         'X1 = df[____]\n'
         'print(X1.shape)'),
    code("X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y, test_size=0.2, random_state=42, stratify=y)\n"
         "print(len(X1_train), len(X1_test))"),

    md("### 문제 2 — 결정 트리 학습하고 정확도 구하기 (직접 쓰기)",
       student="### 문제 2 — 결정 트리 학습하고 정확도 구하기 (직접 쓰기)\n\n"
               "- 빈칸이 없습니다. 2단계의 학습·정확도 코드와 같은 모양으로 직접 씁니다.\n"
               "- 모델 이름은 `model1`, 정확도 이름은 `acc1`, 데이터는 문제 1의 `X1_train`·`y1_train`·`X1_test`·`y1_test`로 바꿉니다. "
               "설정(`max_depth=4, random_state=42`)은 그대로 둡니다.\n"
               "- 출력 문장은 `온도_C 한 열 정확도: …%`로 씁니다. 2단계 정확도(6개 열), 기준선 78.9%와 비교하세요.\n\n"
               "**주의**: `X_test`(6개 열)와 `X1_test`(1개 열)를 섞어 쓰면 `ValueError`가 납니다. "
               "`fit`을 실행하기 전에 정확도 줄을 실행하면 `NotFittedError`가 납니다. "
               "82.7%가 나오면 학습용(`X1_train`, `y1_train`)으로 채점한 것입니다. 이미 본 문제라 점수가 부풀려집니다. "
               "채점은 시험용(`X1_test`, `y1_test`)으로 합니다. "
               "80.3%가 나오면 문제 1의 `X1`에 6개 열이 들어갔거나, 정확도 줄에 `model`·`X_test`가 그대로 남은 것입니다."),
    code("model1 = DecisionTreeClassifier(max_depth=4, random_state=42)\n"
         "model1.fit(X1_train, y1_train)\n"
         "acc1 = accuracy_score(y1_test, model1.predict(X1_test))\n"
         'print(f"온도_C 한 열 정확도: {round(acc1 * 100, 1)}%")',
         "# TODO: 여기에 직접 써 보세요 — model1 만들기 → fit(X1_train, y1_train) → acc1 구하기 → print\n"),
)

if __name__ == "__main__":
    nb.cli()
