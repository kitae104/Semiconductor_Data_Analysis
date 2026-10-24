"""10차시 노트북 2종(학생용·정답) 빌더 — v3 롤아웃(Orange 중심 마지막 차시, 파이썬 최소 + ChatGPT 보고서 검증).

스펙: _workspace/01_architect_spec.md 「10차시」. 파이썬 PART만 담는다(Orange kNN·Logistic Regression·Predictions는 .ows). 생활 예제 단계 없음.
활성 개념 1개: model.predict(X_new). 재사용: 9차시 모델 코드(완성 셀), 새 열 만들기, 조건으로 세기, f-string.
빼는 것: predict_proba(→ Orange Predictions 확률 열), risk_level, confusion_matrix 코드.
노트북: 막혔을 때 → 1 9차시 모델 다시 만들기(완성) → 2 새 로트 예측하기(강의 PART 2 따라 하기, 학생 빈칸 2개)
→ 3 반도체 데이터 실습(문제 1·2: 시험용 147개 예측, 문제 2는 전이 문제 — 2단계 f-string 모양을 빈칸 없이 직접 쓰기)
→ 4 ChatGPT 보고서 숫자 검증 → 5 과정 회고.
ChatGPT 체험은 코드가 아니라 보고서(글)를 받으므로, 붙여 넣는 칸은 마크다운 셀이고 "응답 예시" 자리에는 숫자 대조용 완성 코드 셀을 둔다.
일부러 틀린 곳 2개를 심은 응답 예시 글(3문장)은 강의와 같은 글자로 4단계 프롬프트 다음에 둔다(리드 결정, 정답은 노트북에 넣지 않음).
강의 HTML의 코드 블록은 이 파일의 셀과 글자 단위로 같아야 한다.

실행: python scripts/notebook_builders/week10.py [--no-execute]
"""
from _common import NotebookPair, code, look_up, md, step

TRAIN = "../../data/weekly/week09/week09_pass_fail_train.csv"
NEW = "../../data/weekly/week09/week09_new_lots_to_predict.csv"

nb = NotebookPair("week10", "10차시 실습 — 모델 평가와 새 데이터 예측")

nb.add(
    step(1, "9차시 모델 다시 만들기"),
    md("9차시 2단계(6개 열 결정 트리)와 같은 코드를 한 셀에 모았습니다(완성 코드). **이 셀을 먼저 실행해야** 아래에서 `model`을 쓸 수 있습니다. "
       "정확도가 9차시와 같은 80.3%인지 확인하세요."),
    code("import pandas as pd\n"
         "from sklearn.model_selection import train_test_split\n"
         "from sklearn.tree import DecisionTreeClassifier\n"
         "from sklearn.metrics import accuracy_score\n"
         "\n"
         f'df = pd.read_csv("{TRAIN}", encoding="utf-8-sig").dropna()\n'
         'features = ["온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"]\n'
         "X = df[features]\n"
         'y = df["합격여부"]\n'
         "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n"
         "\n"
         "model = DecisionTreeClassifier(max_depth=4, random_state=42)\n"
         "model.fit(X_train, y_train)\n"
         "acc = accuracy_score(y_test, model.predict(X_test))\n"
         'print(f"정확도: {round(acc * 100, 1)}%")'),
)

nb.add(
    step(2, "새 로트 예측하기"),
    md("강의 PART 2에서 함께 따라 하는 코드입니다. 오늘의 미션: 아직 검사하지 않은 새 로트 9개의 예측 결과를 보고서로 정리합니다.\n\n"
       "새 로트 파일(교육용 가상 데이터)에는 정답(`합격여부`) 열이 없습니다. 모델이 맞혀야 할 대상입니다. "
       "설비 4대(EQ-01~EQ-04)가 여러 공정 기록을 함께 남겼다(교육용 가상 기록). "
       "`예측` 열도 `합격여부`와 같은 규칙입니다: 1 = 합격, -1 = 불합격.",
       student="강의 PART 2에서 함께 따라 하는 코드입니다. 오늘의 미션: 아직 검사하지 않은 새 로트 9개의 예측 결과를 보고서로 정리합니다.\n\n"
               "새 로트 파일(교육용 가상 데이터)에는 정답(`합격여부`) 열이 없습니다. 모델이 맞혀야 할 대상입니다. "
               "설비 4대(EQ-01~EQ-04)가 여러 공정 기록을 함께 남겼다(교육용 가상 기록). "
               "`예측` 열도 `합격여부`와 같은 규칙입니다: 1 = 합격, -1 = 불합격.\n\n"
               "- `model.predict(…)`에는 학습할 때와 **같은 열 6개**(`features`)를 넣습니다.\n\n"
               "**주의**: 1단계 셀을 실행하지 않았으면 `NameError: name 'model' is not defined`가 납니다. "
               "`new_lots` 전체를 넣거나 열이 하나라도 다르면 `ValueError: The feature names should match those that were passed during fit.`가 납니다."),
    code(f'new_lots = pd.read_csv("{NEW}", encoding="utf-8-sig")\n'
         "print(new_lots.shape)"),
    code('new_lots["예측"] = model.predict(new_lots[features])\n'
         'print(new_lots[["공정명", "설비번호", "온도_C", "예측"]])',
         '# TODO: 예측하는 함수 이름과, 학습 때와 같은 열 목록 변수 이름을 채우세요.\n'
         'new_lots["예측"] = model.____(new_lots[____])\n'
         'print(new_lots[["공정명", "설비번호", "온도_C", "예측"]])'),
    code("print(f\"새 로트 {len(new_lots)}개 중 불합격 예측 {(new_lots['예측'] == -1).sum()}개\")"),
    look_up("kNN 이웃 투표"),
)

nb.add(
    step(3, "반도체 데이터 실습"),
    md("실습지 문제 1~2와 같은 문제입니다. 새 로트는 정답을 아직 모르지만, 9차시에 떼어 둔 시험용 147개는 정답(`y_test`)을 압니다. "
       "모델이 \"불합격\"이라고 한 개수와 실제 불합격 개수를 비교해 봅니다."),

    md("### 문제 1 — 시험용 147개 예측하고 불합격 예측 개수 세기",
       student="### 문제 1 — 시험용 147개 예측하고 불합격 예측 개수 세기\n\n"
               "- `model.predict(…)`에 시험용 X(1단계에서 만든 이름)를 넣습니다. 이미 `features` 열 6개로 되어 있습니다.\n"
               "- `(… == 숫자).sum()`은 True(1)를 더해 개수를 셉니다(7차시 True/False 평균과 같은 원리).\n\n"
               "**주의**: `X_test` 대신 `y_test`(정답)를 넣으면 `ValueError`가 납니다. 모델에는 Feature(X)를 넣습니다."),
    code("test_pred = model.predict(X_test)\n"
         "print((test_pred == -1).sum())",
         "# TODO: 시험용 X 이름과, 불합격을 뜻하는 숫자를 채우세요.\n"
         "test_pred = model.predict(____)\n"
         "print((test_pred == ____).sum())"),

    md("### 문제 2 — 실제 불합격 개수와 함께 한 문장으로 보고하기 (직접 쓰기)",
       student="### 문제 2 — 실제 불합격 개수와 함께 한 문장으로 보고하기 (직접 쓰기)\n\n"
               "- 빈칸이 없습니다. 2단계의 `print(f\"새 로트 …개 중 불합격 예측 …개\")` 줄과 같은 모양으로 직접 씁니다.\n"
               "- 출력 문장: `시험용 147개 중 실제 불합격 …개, 불합격 예측 …개`. 147은 `len(y_test)`로, "
               "실제 불합격은 `y_test`에서, 불합격 예측은 문제 1의 `test_pred`에서 셉니다.\n\n"
               "**주의**: 숫자를 직접 적지 말고 코드로 셉니다. 실제 불합격과 불합격 예측에 같은 변수를 두 번 쓰면 오류 없이 같은 숫자가 두 번 나옵니다. "
               "불합격 예측이 1개로 나오면 새 로트(`new_lots['예측']`)를 센 것입니다. 시험용은 문제 1의 `test_pred`에서 셉니다."),
    code('print(f"시험용 {len(y_test)}개 중 실제 불합격 {(y_test == -1).sum()}개, 불합격 예측 {(test_pred == -1).sum()}개")',
         "# TODO: 여기에 직접 써 보세요 — print(f\"시험용 …개 중 실제 불합격 …개, 불합격 예측 …개\")\n"),
)

nb.add(
    step(4, "ChatGPT 체험 — 보고서의 숫자 검증하기"),
    md("ChatGPT에 아래 프롬프트를 그대로 붙여 넣으세요(강의 자료와 같은 글자입니다).\n\n"
       "> 아래는 교육용 가상 데이터로 만든 반도체 공정 합격/불합격 예측 결과야. 팀장에게 보낼 3문장 보고서를 써 줘. "
       "결과를 원인으로 단정하지 말고 \"원인 후보\"라는 표현을 쓰고, 마지막에 가상 데이터라는 점을 밝혀 줘.\n"
       "> - 결정 트리 정확도(시험용 147개): 80.3%\n"
       "> - 기준선(모두 합격이라고 찍었을 때의 정확도): 78.9%\n"
       "> - Orange Confusion Matrix(결정 트리, 10겹 교차검증, 750건): 실제 불합격 155건 중 114건을 합격으로 예측(놓침)\n"
       "> - 새 로트 9개 예측: 불합격 1개(3번째 로트), 합격 8개"),
    md("**응답 예시 — 실제 AI 응답 아님 · 틀린 곳이 숨어 있음**(ChatGPT를 쓸 수 없으면 이 예시로 틀린 곳을 찾으세요)\n\n"
       "> 새 로트 9개 중 결정 트리가 불합격으로 예측한 로트는 2개이며, 3번째 로트(식각·EQ-04, 온도 289.8도)가 그중 하나입니다. "
       "모델 정확도는 80.3%로 모두 합격이라고 찍는 기준선 78.9%와 큰 차이가 없고, "
       "Orange 교차검증에서는 실제 불합격 155건 중 114건을 합격으로 놓쳤습니다. "
       "3번째 로트는 온도가 낮아서 불합격이 생깁니다(이 결과는 교육용 가상 데이터로 만든 것입니다)."),
    md("ChatGPT가 준 보고서를 이 칸에 붙여 넣으세요(이 칸을 더블클릭하면 고칠 수 있습니다).",
       student="ChatGPT가 준 보고서를 이 칸에 붙여 넣으세요(이 칸을 더블클릭하면 고칠 수 있습니다).\n\n(여기에 붙여 넣기)"),
    md("**숫자 대조** — 위 응답 예시나 내가 받은 보고서의 숫자를 아래 셀의 출력과 하나씩 맞춰 보세요. "
       "`KeyError: '예측'`이 나면 2단계 빈칸 셀을 먼저 채워 실행하세요."),
    code('print(f"정확도: {round(acc * 100, 1)}%")\n'
         'print(f"기준선(모두 합격): {round((y_test == 1).mean() * 100, 1)}%")\n'
         "print(f\"불합격 예측: {(new_lots['예측'] == -1).sum()}개\")\n"
         "print(new_lots[new_lots[\"예측\"] == -1][[\"공정명\", \"설비번호\", \"온도_C\"]])"),
    md("**고친 보고 문장**: 숫자가 틀린 곳과 \"원인\"이라고 단정한 곳을 고쳐 세 문장으로 다시 쓰세요.\n\n"
       "새 로트 9개 중 결정 트리가 불합격으로 예측한 로트는 1개(3번째 로트, 식각·EQ-04)입니다. "
       "모델 정확도는 80.3%로 모두 합격이라고 찍는 기준선 78.9%와 큰 차이가 없어, 이 예측은 어느 로트부터 먼저 살펴볼지 정하는 참고로만 쓰고 "
       "온도 같은 공정 조건은 불합격의 원인 후보로만 봅니다. 이 결과는 교육용 가상 데이터로 만든 것입니다.",
       student="**고친 보고 문장**: 숫자가 틀린 곳과 \"원인\"이라고 단정한 곳을 고쳐 세 문장으로 다시 쓰세요.\n\n"
               "(여기에 고친 보고 문장 쓰기)"),
    look_up("예측 확률의 뜻"),
)

nb.add(
    step(5, "과정 회고 — 10일을 한 문장씩"),
    md("1~10차시에 한 일을 한 문장씩 적어 보세요. 기록 → 표 → 정리 → 그림 → 비교 → 원인 후보 → 예측의 순서입니다.\n\n"
       "- 1~3차시(기록): 공장 기록을 변수·리스트·조건문으로 다뤘다.\n"
       "- 4~5차시(표·정리): CSV를 표로 읽고 빈칸·중복·튀는 값을 정리했다.\n"
       "- 6~7차시(그림·비교): 그래프와 설비별 비교로 합격률이 낮은 곳을 찾았다.\n"
       "- 8차시(원인 후보): 상관계수와 범위 밖 비교로 원인 후보를 골랐다.\n"
       "- 9~10차시(예측): 모델로 합격·불합격을 미리 맞혀 보고, 기준선과 함께 읽었다.",
       student="1~10차시에 한 일을 한 문장씩 적어 보세요. 기록 → 표 → 정리 → 그림 → 비교 → 원인 후보 → 예측의 순서입니다.\n\n"
               "- 1~3차시(기록):\n"
               "- 4~5차시(표·정리):\n"
               "- 6~7차시(그림·비교):\n"
               "- 8차시(원인 후보):\n"
               "- 9~10차시(예측):"),
)

if __name__ == "__main__":
    nb.cli()
