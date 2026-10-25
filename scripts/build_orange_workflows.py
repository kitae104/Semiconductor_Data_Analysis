"""차시별 Orange3 워크플로(.ows)를 선언형 정의(WORKFLOWS)에서 생성하는 스크립트.

- Orange 3.35 파이썬으로 실행한다. `python scripts/build_orange_workflows.py`로 실행해도
  Orange 파이썬(환경변수 ORANGE_PYTHON 또는 기본 설치 경로)으로 스스로 다시 실행된다.
- 출력: orange3/weekXX/weekXX_<번호>_<주제>_start.ows / _done.ows
  - _start: 데이터가 이미 연결된 File 위젯 + 다음에 붙일 위젯을 안내하는 캔버스 메모
  - _done : 위젯 체인 전체(막혔을 때 따라잡기·정답)
- File 위젯 경로는 이식 가능하게 저장한다(다른 PC·키트 압축 해제 위치에서도 열리게).
  - 과정 데이터: RecentPath(prefix="basedir", relpath="../../data/weekly/weekXX/orange/<이름>.tab")
    (basedir = .ows 파일이 있는 폴더. Orange가 워크플로를 열 때 정해 준다)
  - Orange 내장 데이터: RecentPath(prefix="sample-datasets", relpath="zoo.tab")
- 위젯 설정은 기본값을 쓰고, 필요한 것(Distributions 변수, Select Rows 조건 등)만 지정한다.
  지정한 설정은 실제 위젯을 화면 없이 만들어 데이터를 넣고 값을 바꾼 뒤 Orange 방식 그대로 저장한다.

실행:
    python scripts/build_orange_workflows.py            # 정의된 전 차시
    python scripts/build_orange_workflows.py --week 5   # 5차시만
검증: python scripts/validate_orange_workflows.py
"""
import argparse
import os
import sys

sys.dont_write_bytecode = True  # scripts/__pycache__를 남기지 않는다
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _orange_env import ensure_orange_python  # noqa: E402

ensure_orange_python(__file__)

from AnyQt.QtWidgets import QApplication  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "orange3")

# 위젯 정식 이름(qualified name). 정의를 짧게 쓰기 위한 별칭이다.
FILE = "Orange.widgets.data.owfile.OWFile"
TABLE = "Orange.widgets.data.owtable.OWTable"
STATS = "Orange.widgets.data.owfeaturestatistics.OWFeatureStatistics"
IMPUTE = "Orange.widgets.data.owimpute.OWImpute"
SELECT_ROWS = "Orange.widgets.data.owselectrows.OWSelectRows"
SELECT_COLS = "Orange.widgets.data.owselectcolumns.OWSelectAttributes"
DISTRIBUTIONS = "Orange.widgets.visualize.owdistributions.OWDistributions"
SCATTER = "Orange.widgets.visualize.owscatterplot.OWScatterPlot"
BOXPLOT = "Orange.widgets.visualize.owboxplot.OWBoxPlot"
PIVOT = "Orange.widgets.data.owpivot.OWPivot"
CORRELATIONS = "Orange.widgets.data.owcorrelations.OWCorrelations"
TREE = "Orange.widgets.model.owtree.OWTreeLearner"
TREE_VIEWER = "Orange.widgets.visualize.owtreeviewer.OWTreeGraph"
KNN = "Orange.widgets.model.owknn.OWKNNLearner"
LOGREG = "Orange.widgets.model.owlogisticregression.OWLogisticRegression"
TEST_SCORE = "Orange.widgets.evaluate.owtestandscore.OWTestAndScore"
CONFUSION = "Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix"
PREDICTIONS = "Orange.widgets.evaluate.owpredictions.OWPredictions"
# Test and Score의 Number of folds 목록은 [2, 3, 5, 10, 20]이고 기본은 셋째(5겹)다. 10겹 = 목록 번호 3
TEN_FOLDS = {"n_folds": 3}


def sample(name):
    """Orange 내장 데이터(zoo.tab, iris.tab ...). 지원은 남겨 두지만 과정에서는 쓰지 않는다
    (2026-10-23 결정: 워밍업도 generate_weekly_data.py가 만든 합성 데이터만 쓴다)."""
    return {"prefix": "sample-datasets", "relpath": name}


def weekly(week, stem):
    """과정 데이터의 Orange용 파생본 data/weekly/weekXX/orange/<stem>.tab (generate_weekly_data.py가 만든다)."""
    return {"prefix": "basedir", "relpath": f"../../data/weekly/{week}/orange/{stem}.tab"}


# ---------------------------------------------------------------------------
# 워크플로 정의
# ---------------------------------------------------------------------------
# 차시 키("week01") → 워크플로 목록. 워크플로 하나가 _start/_done 두 파일이 된다.
#   n, topic   : 파일 이름 weekXX_<n>_<topic>_start.ows
#   title      : 워크플로 제목(Orange 정보 창에 보인다)
#   nodes      : id, widget(정식 이름), title(캔버스 표시 이름), data(File만), settings(선택)
#                settings 값이 열 이름 문자열이면 그 열(Variable)로 바꿔 넣는다.
#                Select Rows: {"conditions": [(열, 연산자 이름, [값...]), ...]}
#                Impute     : {"default_method": "Average", "methods": {열: "Drop"}}
#   links      : (보내는 id, 받는 id) 또는 (보내는 id, 받는 id, 출력 이름, 입력 이름)
#                출력/입력을 생략하면 Orange가 제안하는 기본 연결을 쓴다.
#   start      : _start 파일에 남길 노드 id(기본: File 노드만)
#   start_note / done_note : 캔버스 메모. 줄마다 ①②③ 번호로 다음 동작을 안내한다.
#   position   : (x, y)를 주지 않으면 File에서 떨어진 단계에 따라 왼쪽 → 오른쪽으로 놓는다.
# 번호: ① 워밍업 데이터(weekXX_orange_*.csv), ② 반도체 데이터. 워밍업 데이터가 정해지기 전에도
# 반도체 워크플로는 ②로 둔다(나중에 ①을 넣어도 파일 이름이 바뀌지 않게).
WORKFLOWS = {
    "week01": [
        {
            "n": 1, "topic": "town",
            "title": "1차시 ① 우리 동네 인구로 Orange 캔버스 첫 만남",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week01", "week01_orange_town_population")},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)"},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "주요연령대"}},
            ],
            "links": [("file", "table"), ("file", "dist")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 우리 동네 인구 데이터(30개 동)가 이미 들어 있습니다.",
                "② 왼쪽 Data 묶음에서 Data Table(표 보기)을 끌어 와 File의 오른쪽 끝과 선으로 이으세요. 행과 열이 몇 개인지 세어 보세요.",
                "③ Visualize 묶음에서 Distributions(분포 막대)를 끌어 와 File과 잇고, 왼쪽 열 목록에서 주요연령대를 고르세요.",
            ],
            "done_note": [
                "완성본: File → Data Table(표 보기), File → Distributions(분포 막대, 주요연령대).",
                "가장 높은 막대가 가장 흔한 값입니다. 30줄을 다 읽지 않아도 막대 하나로 보입니다.",
                "더 해 보기: Distributions의 Split by에서 구를 고르면 구마다 막대가 나뉩니다.",
            ],
        },
        {
            "n": 2, "topic": "process",
            "title": "1차시 ② 반도체 공정 데이터 둘러보기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week01", "week01_semiconductor_process_overview")},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)"},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "합격여부"}},
            ],
            "links": [("file", "table"), ("file", "dist")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 반도체 공정 데이터(40행)가 들어왔는지 확인하세요.",
                "② Data Table(표 보기)을 File에 이어 행과 열을 살펴보세요.",
                "③ Distributions(분포 막대)를 File에 잇고 열 목록에서 합격여부를 고르세요. (1 = 합격, -1 = 불합격)",
            ],
            "done_note": [
                "완성본: File → Data Table(표 보기), File → Distributions(분포 막대, 합격여부).",
                "합격(1)과 불합격(-1) 막대의 높이를 파이썬에서 센 개수와 비교해 보세요.",
            ],
        },
    ],
    "week02": [
        {
            "n": 1, "topic": "subway",
            "title": "2차시 ① 지하철 역별 승하차로 최고·최저·평균 읽기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week02", "week02_orange_subway_ridership")},
                {"id": "stats", "widget": STATS, "title": "Column Statistics (열 통계)"},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("승차인원_count", -1)]}},
            ],
            "links": [("file", "stats"), ("file", "table")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 지하철 8개 역 × 3시간대 승하차 기록(24행)이 이미 들어 있습니다.",
                "② 왼쪽 Data 묶음에서 Column Statistics(열 통계)를 끌어 와 File과 이으세요. 승차인원_count 줄의 Mean(평균)과 Max(최고)를 비교하세요.",
                "③ Data Table(표 보기)을 File에 잇고, 승차인원_count 열 이름을 두 번 눌러 큰 값부터 정렬하세요. 맨 위 행은 어느 역·시간대인가요?",
            ],
            "done_note": [
                "완성본: File → Column Statistics(열 통계), File → Data Table(표 보기, 승차인원_count 큰 값부터).",
                "Max가 Mean보다 훨씬 큽니다. 평균만 보면 유난히 붐비는 한 곳이 안 보입니다 — 최고·최저를 같이 보세요.",
            ],
        },
        {
            "n": 2, "topic": "temps",
            "title": "2차시 ② 설비 온도 기록 20건 요약하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week02", "week02_python_basics_1")},
                {"id": "stats", "widget": STATS, "title": "Column Statistics (열 통계)"},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("설비번호", 1)]}},
            ],
            "links": [("file", "stats"), ("file", "table")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 week02_python_basics_1.tab이 들어왔는지 확인하세요.",
                "② File에 Column Statistics(열 통계)를 잇고 온도_C 행의 Mean과 Max.를 읽으세요.",
                "③ File에 Data Table(표 보기)을 잇고 설비번호 열 머리를 한 번 눌러 정렬하세요. 같은 설비의 행이 한데 모입니다. EQ-02 행을 찾으세요.",
            ],
            "done_note": [
                "완성본: File → Column Statistics(열 통계), File → Data Table(표 보기, 설비번호 순).",
                "EQ-02 행 4개의 온도를 노트북 6단계의 eq02_temps와 견주어 보세요. 같은 표라도 어느 범위를 담았는지에 따라 평균이 다릅니다.",
            ],
        },
    ],
    "week03": [
        {
            "n": 1, "topic": "air",
            "title": "3차시 ① 우리 동네 대기환경에서 조건으로 날 고르기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week03", "week03_orange_air_quality")},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [("PM10_ug_m3", "is greater than", ["80"])]}},
                {"id": "table", "widget": TABLE, "title": "Data Table (고른 날)"},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "등급"}},
            ],
            "links": [("file", "select"), ("select", "table", "Matching Data", "Data"), ("file", "dist")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 4월 한 달(30일)의 대기환경 기록이 이미 들어 있습니다.",
                "② 왼쪽 Transform 묶음에서 Select Rows(행 고르기)를 끌어 와 File과 잇고, 이미 있는 조건 한 줄을 PM10_ug_m3 is greater than 80으로 바꾸세요.",
                "③ Select Rows에 Data Table(표 보기)을 이어 고른 날이 며칠인지, 그날들의 등급이 무엇인지 보세요.",
                "④ Visualize 묶음의 Distributions(분포 막대)를 File에 잇고 등급을 고르세요.",
            ],
            "done_note": [
                "완성본: File → Select Rows(PM10_ug_m3 is greater than 80) → Data Table, File → Distributions(등급).",
                "더 해 보기: Select Rows에 조건 습도_pct is greater than 70을 하나 더 넣으면 남는 날이 줄어듭니다.",
            ],
        },
        {
            "n": 2, "topic": "records",
            "title": "3차시 ② 설비 기록 30건을 온도 규칙으로 고르기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week03", "week03_python_basics_2")},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [("설비번호", "is", ["EQ-04"]), ("온도_C", "is outside", ["295", "305"])]}},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)"},
            ],
            "links": [("file", "select"), ("select", "table", "Matching Data", "Data")],
            "start_note": [
                "① File을 더블클릭해 설비 기록(30행)이 들어왔는지 확인하세요.",
                "② Transform 묶음의 Select Rows를 File에 잇고 더블클릭하세요. 이미 있는 조건 한 줄을 설비번호 is EQ-04로 바꾸세요.",
                "③ Select Rows에 Data Table을 이어 몇 행인지 세어 보세요.",
                "④ Add Condition으로 온도_C is outside 295, 305를 더하세요(왼쪽 칸 295, 오른쪽 칸 305).",
            ],
            "done_note": [
                "완성본: File → Select Rows(설비번호 is EQ-04, 온도_C is outside 295, 305 — 한 위젯에 조건 두 줄) → Data Table.",
                "범위 밖이라고 모두 불합격은 아닙니다. Data Table의 합격여부 열을 함께 보세요.",
            ],
        },
    ],
    "week04": [
        {
            "n": 1, "topic": "flow",
            "title": "4차시 ① 반도체 8대 공정 흐름표에서 되풀이되는 단계 고르기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week04", "week04_orange_process_flow")},
                {"id": "cols", "widget": SELECT_COLS, "title": "Select Columns (열 고르기)",
                 "settings": {"columns": {"attribute": ["공정순서", "공정명", "반복여부"],
                                          "meta": ["하는일", "생활비유"]}}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [("반복여부", "is", ["여러 번"])]}},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("공정순서", 1)]}},
            ],
            "links": [("file", "cols"), ("cols", "select"), ("select", "table", "Matching Data", "Data")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 반도체 8대 공정 흐름표(8행)가 이미 들어 있습니다.",
                "② 왼쪽 Transform 묶음에서 Select Columns(열 고르기)를 끌어 와 File과 잇고, 공정순서·공정명·반복여부만 Features에 남기세요(하는일·생활비유는 Metas).",
                "③ Select Columns에 Select Rows(행 고르기)를 잇고 조건을 반복여부 is 여러 번으로 만드세요.",
                "④ Select Rows에 Data Table(표 보기)을 잇고 공정순서 열 이름을 눌러 순서대로 보세요. 몇 단계가 남았나요?",
            ],
            "done_note": [
                "완성본: File → Select Columns(공정순서·공정명·반복여부 + 하는일·생활비유) → Select Rows(반복여부 is 여러 번) → Data Table.",
                "8단계 중 5단계(②~⑥)가 남습니다. 칩 하나를 만들 때 이 단계들이 층마다 되풀이됩니다.",
            ],
        },
        {
            "n": 2, "topic": "filtering",
            "title": "4차시 ② 공정 기록 100건에서 설비 한 대의 불합격 고르기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week04", "week04_process_filtering")},
                {"id": "cols", "widget": SELECT_COLS, "title": "Select Columns (열 고르기)",
                 "settings": {"columns": {"attribute": ["설비번호", "온도_C"], "class": ["합격여부"]}}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [("설비번호", "is", ["EQ-02"]), ("합격여부", "is", ["-1"])]}},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("온도_C", -1)]}},
            ],
            "links": [("file", "cols"), ("cols", "select"), ("select", "table", "Matching Data", "Data")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 기록(100행)이 들어왔는지 확인하세요.",
                "② Select Columns(열 고르기)를 File에 잇고 설비번호·온도_C만 Features에, 합격여부는 Target에 남기세요.",
                "③ Select Columns에 Select Rows(행 고르기)를 잇고 Add Condition으로 설비번호 is EQ-01을 만드세요. Select Rows에 Data Table(표 보기)을 이어 왼쪽 Info 칸에서 행 수를 읽으세요.",
                "④ Select Rows로 돌아가 Add Condition으로 합격여부 is -1을 더하고, Data Table의 행 수를 다시 읽으세요. 온도_C 열 머리글을 눌러 큰 값부터 놓으세요.",
                "⑤ 실습지 문제 4에서는 같은 순서로 EQ-02를 골라 봅니다.",
            ],
            "done_note": [
                "완성본: File → Select Columns(설비번호·온도_C·합격여부) → Select Rows(설비번호 is EQ-02, 합격여부 is -1) → Data Table(온도_C 큰 값부터).",
                "조건 하나(EQ-02)일 때와 둘(EQ-02 + 불합격)일 때 남는 행 수를 파이썬 결과와 비교하세요.",
            ],
        },
    ],
    "week05": [
        {
            "n": 1, "topic": "cleanroom",
            "title": "5차시 ① 클린룸 환경 기록에서 빈칸·튀는 값 다루기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week05", "week05_orange_cleanroom_env")},
                {"id": "stats", "widget": STATS, "title": "Column Statistics (정리 전)"},
                {"id": "impute", "widget": IMPUTE, "title": "Impute (빈칸 채우기)",
                 "settings": {"default_method": "Average"}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [
                     ("파티클_count_per_m3", "is below", ["10000"]),
                     ("차압_Pa", "is at least", ["0"]),
                 ]}},
                {"id": "stats_after", "widget": STATS, "title": "Column Statistics (정리 후)"},
                {"id": "filled", "widget": TABLE, "title": "Data Table (채운 뒤)"},
            ],
            "links": [("file", "stats"), ("file", "impute"), ("impute", "select"),
                      ("select", "stats_after", "Matching Data", "Data"), ("impute", "filled")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 클린룸 기록(72행)이 들어왔는지 확인하세요.",
                "② Column Statistics(열 통계)를 File에 이어 빈칸 수(Missing)와 파티클의 가장 큰 값(Max)을 찾으세요.",
                "③ Impute(빈칸 채우기)를 File에 잇고, Impute에 Data Table을 이어 빈칸이 어떤 값으로 채워졌는지 보세요.",
                "④ Impute에 Select Rows(파티클 is below 10000, 차압 is at least 0) → Column Statistics를 이어 정리 전과 비교하세요.",
            ],
            "done_note": [
                "완성본: Impute는 빈칸을 그 열의 평균으로 채웁니다. 99,999(센서 오류 코드)가 섞인 채로 평균을 내면 채운 값도 크게 튑니다.",
                "Select Rows는 파티클 10,000 미만, 차압 0 이상인 행만 남깁니다. 튀는 값부터 확인해야 하는 이유를 Data Table(채운 뒤)에서 찾아보세요.",
            ],
        },
        {
            "n": 2, "topic": "dirty_process",
            "title": "5차시 ② 지저분한 공정 데이터 정리하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week05", "week05_dirty_process_data")},
                {"id": "stats", "widget": STATS, "title": "Column Statistics (정리 전)"},
                {"id": "impute", "widget": IMPUTE, "title": "Impute (빈칸 채우기)",
                 "settings": {"default_method": "Average", "methods": {"합격여부": "Drop"}}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [
                     ("온도_C", "is at most", ["400"]),
                     ("압력_Pa", "is at least", ["0"]),
                     ("가스유량_slm", "is at least", ["0"]),
                     ("가스유량_slm", "is below", ["200"]),
                 ]}},
                {"id": "table", "widget": TABLE, "title": "Data Table (정리 결과)"},
                {"id": "stats_after", "widget": STATS, "title": "Column Statistics (정리 후)"},
            ],
            "links": [("file", "stats"), ("file", "impute"), ("impute", "select"),
                      ("select", "table", "Matching Data", "Data"),
                      ("select", "stats_after", "Matching Data", "Data")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 데이터(113행)가 들어왔는지 확인하세요.",
                "② Column Statistics(열 통계)를 File에 이어 빈칸(Missing)과 Min·Max가 이상한 열을 찾으세요.",
                "③ Impute(빈칸 채우기) → Select Rows(행 고르기) → Data Table 순서로 이어 이상값을 걸러 내세요.",
                "④ Select Rows에 Column Statistics를 하나 더 이어 정리 전과 비교하세요.",
            ],
            "done_note": [
                "완성본: Impute는 숫자 빈칸을 평균으로 채우고, 합격여부가 빈 행은 지웁니다(Remove instances).",
                "Select Rows 조건: 온도_C ≤ 400, 압력_Pa ≥ 0, 0 ≤ 가스유량_slm < 200.",
                "Column Statistics(정리 전)와 (정리 후)의 Min·Max·Mean을 비교하고, 남은 행 수를 파이썬 결과와 비교하세요.",
            ],
        },
    ],
    "week06": [
        {
            "n": 1, "topic": "wafermap",
            "title": "6차시 ① 웨이퍼 맵 한 장 — 표의 X·Y를 점으로 찍기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week06", "week06_orange_wafer_map")},
                {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (산점도)",
                 "settings": {"attr_x": "다이_X", "attr_y": "다이_Y", "attr_color": "합격여부"}},
                {"id": "box", "widget": BOXPLOT, "title": "Box Plot (상자 그림)",
                 "settings": {"attribute": "중심거리_mm", "group_var": "합격여부"}},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "중심거리_mm", "cvar": "합격여부"}},
            ],
            "links": [("file", "scatter"), ("file", "box"), ("file", "dist")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 웨이퍼 한 장의 다이 317개 검사 기록이 이미 들어 있습니다.",
                "② Visualize 묶음에서 Scatter Plot(산점도)을 끌어 와 File과 잇고, Axis x = 다이_X, Axis y = 다이_Y, Color = 합격여부로 고르세요.",
                "③ Box Plot(상자 그림)을 File에 잇고 변수 중심거리_mm, Subgroups 합격여부를 고르세요.",
                "④ (더 해 보기) Distributions(분포 막대)를 File에 잇고 중심거리_mm를 고르세요.",
            ],
            "done_note": [
                "완성본: File → Scatter Plot(다이_X·다이_Y, 색 합격여부), File → Box Plot(중심거리_mm, Subgroups 합격여부),",
                "        File → Distributions(중심거리_mm, Split by 합격여부).",
                "둥근 웨이퍼 모양이 보이고, 불합격 점이 가장자리 고리에 몰립니다.",
            ],
        },
        {
            "n": 2, "topic": "process",
            "title": "6차시 ② 공정 기록 180건을 그래프로 보기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week06", "week06_process_visualization")},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "온도_C", "cvar": None}},
                {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (산점도)",
                 "settings": {"attr_x": "온도_C", "attr_y": "두께_nm", "attr_color": "합격여부"}},
                {"id": "box", "widget": BOXPLOT, "title": "Box Plot (상자 그림)",
                 "settings": {"attribute": "온도_C", "group_var": "설비번호"}},
            ],
            "links": [("file", "dist"), ("file", "scatter"), ("file", "box")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 기록(180행)이 들어왔는지 확인하세요.",
                "② 강사 화면 보기: Distributions(분포 막대) — 온도_C, Split by None. 학생은 따라 누르지 않습니다.",
                "③ 강사 화면 보기: Scatter Plot(산점도) — 학생은 따라 누르지 않습니다.",
                "④ 실습지 문제 4: Box Plot(상자 그림)을 File에 잇고 변수 온도_C, Subgroups 설비번호를 고르세요. 상자가 가장 긴 설비는?",
            ],
            "done_note": [
                "완성본: File → Distributions(온도_C), File → Scatter Plot(온도_C·두께_nm, 색 합격여부), File → Box Plot(온도_C, Subgroups 설비번호).",
                "파이썬으로 그린 히스토그램·산점도와 모양을 비교하고, 파이썬으로 그리지 않은 상자 그림에서 설비마다 퍼짐이 어떻게 다른지 보세요.",
            ],
        },
    ],
    "week07": [
        {
            "n": 1, "topic": "waferlots",
            "title": "7차시 ① 식각 설비 3대의 웨이퍼 12장 — 수율과 불량 위치",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week07", "week07_orange_wafer_lots")},
                {"id": "pivot", "widget": PIVOT, "title": "Pivot Table (피벗 표)",
                 "settings": {"row_feature": "설비번호", "col_feature": "합격여부"}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (식각-3만)",
                 "settings": {"conditions": [("설비번호", "is", ["식각-3"])]}},
                {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (웨이퍼 맵)",
                 "settings": {"attr_x": "다이_X", "attr_y": "다이_Y", "attr_color": "합격여부"}},
            ],
            "links": [("file", "pivot"), ("file", "select"),
                      ("select", "scatter", "Matching Data", "Data")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 식각 설비 3대가 처리한 웨이퍼 12장의 다이 검사 기록(3,804행)이 들어 있습니다.",
                "② Transform 묶음에서 Pivot Table(피벗 표)을 끌어 와 File과 잇고, Rows = 설비번호, Columns = 합격여부로 고르세요(값은 Count).",
                "③ Select Rows(행 고르기)를 File에 잇고, 이미 있는 첫 줄의 열을 설비번호로, 값을 ②의 표에서 불합격(-1) 칸이 가장 큰 설비로 바꾸세요(줄을 새로 추가하지 않습니다).",
                "④ Select Rows에 Scatter Plot(산점도)을 잇고 x = 다이_X, y = 다이_Y, Color = 합격여부로 웨이퍼 맵을 그리세요.",
            ],
            "done_note": [
                "완성본: File → Pivot Table(Rows 설비번호, Columns 합격여부, Count), File → Select Rows(설비번호 is 식각-3) → Scatter Plot(다이_X·다이_Y, 색 합격여부).",
                "Pivot Table이 세는 것은 다이 수입니다(웨이퍼 수가 아님). 수율이 가장 낮은 설비의 웨이퍼를 그림으로 열어 불량 위치를 보세요 — 원인 후보를 좁히는 단서입니다.",
            ],
        },
        {
            "n": 2, "topic": "yield",
            "title": "7차시 ② 설비별 합격·불합격 비교하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week07", "week07_equipment_yield")},
                {"id": "pivot", "widget": PIVOT, "title": "Pivot Table (피벗 표)",
                 "settings": {"row_feature": "설비번호", "col_feature": "합격여부"}},
                {"id": "box", "widget": BOXPLOT, "title": "Box Plot (상자 그림)",
                 "settings": {"attribute": "온도_C", "group_var": "설비번호"}},
            ],
            "links": [("file", "pivot"), ("file", "box")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 웨이퍼 기록(300행)이 들어왔는지 확인하세요.",
                "② (실습지 문제 4) Pivot Table(피벗 표)을 File에 잇고 Rows = 설비번호, Columns = 합격여부로 고르세요. 설비마다 -1(불합격) 칸과 Total 칸의 숫자를 읽으세요.",
                "③ (강사 시연) Box Plot(상자 그림)을 File에 잇고 Variable 온도_C, Subgroups 설비번호를 고르세요.",
            ],
            "done_note": [
                "완성본: File → Pivot Table(Rows 설비번호, Columns 합격여부, Count), File → Box Plot(온도_C, Subgroups 설비번호).",
                "파이썬 groupby로 계산한 설비별 합격률과 Pivot Table 칸의 비율을 비교하세요. 합격률이 낮은 설비는 원인 후보이지, 원인으로 확정된 것은 아닙니다.",
            ],
        },
    ],
    "week08": [
        {
            "n": 1, "topic": "chamber",
            "title": "8차시 ① 식각 챔버 센서 기록 — 함께 움직이는 값 줄 세우기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week08", "week08_orange_chamber_sensor")},
                {"id": "corr", "widget": CORRELATIONS, "title": "Correlations (상관 순위)"},
                {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (산점도)",
                 "settings": {"attr_x": "RF파워_W", "attr_y": "식각률_nm_min"}},
            ],
            "links": [("file", "corr"), ("file", "scatter")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 식각 챔버 센서 기록(200행)이 이미 들어 있습니다.",
                "② Unsupervised 묶음에서 Correlations(상관 순위)를 끌어 와 File과 이으세요. 맨 위 쌍과 부호(-)가 붙은 쌍을 찾으세요.",
                "③ Visualize 묶음의 Scatter Plot(산점도)을 File에 잇고 x = RF파워_W, y = 식각률_nm_min으로 고르세요.",
            ],
            "done_note": [
                "완성본: File → Correlations(Pearson), File → Scatter Plot(RF파워_W · 식각률_nm_min).",
                "부호가 -이면 한쪽이 오를 때 다른 쪽은 내려갑니다. 이 관계는 교육용 가상 관계이며, 함께 움직인다고 원인인 것은 아닙니다(원인 후보).",
            ],
        },
        {
            "n": 2, "topic": "anomaly",
            "title": "8차시 ② 공정 센서 기록에서 상관 순위 보기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week08", "week08_anomaly_root_cause")},
                {"id": "corr", "widget": CORRELATIONS, "title": "Correlations (상관 순위)"},
                {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (산점도)",
                 "settings": {"attr_x": "온도_C", "attr_y": "두께_nm", "attr_color": "합격여부"}},
            ],
            "links": [("file", "corr"), ("file", "scatter")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 센서 기록(450행)이 들어왔는지 확인하세요.",
                "② (실습지 문제 4) Unsupervised 묶음의 Correlations(상관 순위)를 File에 잇고 1위 쌍과 값을 읽으세요. 이어서 목록 위 Filter 칸에 진공도를 입력해, 진공도가 들어간 쌍 중 크기가 가장 큰 값을 읽으세요. 합격여부는 숫자 열이 아니라 목록에 없습니다.",
                "③ (강사 화면) Scatter Plot(산점도)을 File에 잇고 x = 온도_C, y = 두께_nm, Color = 합격여부로 고르세요.",
                "④ (강사 화면) Scatter Plot의 Find Informative Projections 버튼을 누르고 Start를 눌러, 합격·불합격 색이 잘 갈리는 두 열 짝을 보세요.",
            ],
            "done_note": [
                "완성본: File → Correlations(Pearson), File → Scatter Plot(온도_C · 두께_nm, 색 합격여부).",
                "Correlations 1위를 파이썬 corr() 결과와 비교하세요. 합격여부는 이 목록에 없어 진공도와 불합격의 관계는 처음부터 나오지 않습니다 — 원인 후보는 범위 밖 불합격률 같은 다른 방법으로도 확인합니다.",
            ],
        },
    ],
    "week09": [
        {
            "n": 1, "topic": "patterns",
            "title": "9차시 ① 웨이퍼 맵 패턴을 결정 트리로 분류하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week09", "week09_orange_wafer_patterns")},
                {"id": "tree", "widget": TREE, "title": "Tree (결정 트리)", "settings": {"max_depth": 4}},
                {"id": "viewer", "widget": TREE_VIEWER, "title": "Tree Viewer (트리 보기)", "settings": {"show_intermediate": True}},
                {"id": "score", "widget": TEST_SCORE, "title": "Test and Score (평가)", "settings": dict(TEN_FOLDS)},
                {"id": "cm", "widget": CONFUSION, "title": "Confusion Matrix (헷갈림 표)"},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "불량패턴", "cvar": None}},
            ],
            "links": [("file", "tree"), ("tree", "viewer"), ("file", "score"), ("tree", "score", "Learner", "Learner"),
                      ("score", "cm"), ("file", "dist")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 웨이퍼 240장의 불량 모양 요약(불량패턴이 목표 열)이 들어 있습니다.",
                "② Model 묶음의 Tree(결정 트리)를 File에 잇고, Limit the maximal tree depth를 4로 바꾸세요. Visualize 묶음의 Tree Viewer(트리 보기)를 Tree에 이으세요. Tree Viewer 왼쪽 Show details in non-leaves에 체크하세요.",
                "③ Evaluate 묶음의 Test and Score(평가)를 File에 잇고, Tree도 Test and Score에 이으세요. Cross validation의 Number of folds를 10으로 고르세요.",
                "④ Confusion Matrix(헷갈림 표)를 Test and Score에 잇고 어떤 패턴끼리 헷갈렸는지 보세요.",
                "⑤ (더 해 보기) Distributions(분포 막대)를 File에 잇고 불량패턴을 고르세요.",
            ],
            "done_note": [
                "완성본: File → Tree(깊이 4) → Tree Viewer, File → Test and Score(10겹, ← Tree) → Confusion Matrix, File → Distributions(불량패턴).",
                "Tree Viewer의 첫 갈림길과 Test and Score의 CA(정확도)를 읽으세요. 맞혔다고 원인을 아는 것은 아닙니다 — 갈림길의 열은 모델이 패턴을 나누는 데 쓴 단서일 뿐, 불량 모양의 원인이 아닙니다.",
            ],
        },
        {
            "n": 2, "topic": "passfail",
            "title": "9차시 ② 공정 기록으로 합격·불합격 예측하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week09", "week09_pass_fail_train")},
                {"id": "dist", "widget": DISTRIBUTIONS, "title": "Distributions (분포 막대)",
                 "settings": {"var": "합격여부", "cvar": None}},
                {"id": "tree", "widget": TREE, "title": "Tree (결정 트리)", "settings": {"max_depth": 4}},
                {"id": "viewer", "widget": TREE_VIEWER, "title": "Tree Viewer (트리 보기)", "settings": {"show_intermediate": True}},
                {"id": "score", "widget": TEST_SCORE, "title": "Test and Score (평가)", "settings": dict(TEN_FOLDS)},
                {"id": "cm", "widget": CONFUSION, "title": "Confusion Matrix (헷갈림 표)"},
            ],
            "links": [("file", "dist"), ("file", "tree"), ("tree", "viewer"), ("file", "score"),
                      ("tree", "score", "Learner", "Learner"), ("score", "cm")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 기록(750행, 목표 열 합격여부)이 들어왔는지 확인하세요.",
                "② Distributions(분포 막대)를 File에 잇고 합격여부를 고르세요(Split by는 None). 합격이 전체의 몇 %인가요? 이것이 기준선입니다.",
                "③ Tree(결정 트리, 깊이 4) → Tree Viewer를 이으세요. Tree Viewer 왼쪽 Show details in non-leaves에 체크하세요.",
                "④ Test and Score(평가, Number of folds 10)를 File과 Tree에 잇고, Confusion Matrix를 Test and Score에 이으세요. Confusion Matrix의 Show가 Number of instances인지 보세요.",
            ],
            "done_note": [
                "완성본: File → Distributions(합격여부), File → Tree(깊이 4) → Tree Viewer, File → Test and Score(10겹, ← Tree) → Confusion Matrix.",
                "CA를 기준선(무조건 합격이라고 찍었을 때의 정확도)과 비교하세요. Confusion Matrix에서 실제 불합격(-1)인데 합격(1)으로 예측한 칸을 찾으세요.",
            ],
        },
    ],
    "week10": [
        {
            "n": 1, "topic": "newwafers",
            "title": "10차시 ① 모델 세 가지 비교하고 새 웨이퍼 10장 예측하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (학습: 웨이퍼 240장)",
                 "data": weekly("week09", "week09_orange_wafer_patterns")},
                {"id": "tree", "widget": TREE, "title": "Tree (결정 트리)", "settings": {"max_depth": 4}},
                {"id": "knn", "widget": KNN, "title": "kNN (이웃 투표)"},
                {"id": "logreg", "widget": LOGREG, "title": "Logistic Regression (로지스틱 회귀)"},
                {"id": "score", "widget": TEST_SCORE, "title": "Test and Score (평가)", "settings": dict(TEN_FOLDS)},
                {"id": "new", "widget": FILE, "title": "File (새 웨이퍼 10장)",
                 "data": weekly("week10", "week10_orange_new_wafers")},
                {"id": "pred", "widget": PREDICTIONS, "title": "Predictions (예측)"},
            ],
            "links": [("file", "tree"), ("file", "knn"), ("file", "logreg"), ("file", "score"),
                      ("tree", "score", "Learner", "Learner"), ("knn", "score", "Learner", "Learner"),
                      ("logreg", "score", "Learner", "Learner"),
                      ("new", "pred", "Data", "Data"), ("tree", "pred", "Model", "Predictors"),
                      ("knn", "pred", "Model", "Predictors"), ("logreg", "pred", "Model", "Predictors")],
            "start": ["file", "new"],
            "start_note": [
                "① 위 File은 9차시 웨이퍼 240장(학습용), 아래 File은 정답이 없는 새 웨이퍼 10장입니다. 둘 다 이미 들어 있습니다.",
                "② Model 묶음에서 Tree(깊이 4)·kNN·Logistic Regression을 끌어 와 각각 위 File에 이으세요.",
                "③ Test and Score(평가, Number of folds 10)를 위 File에 잇고, 세 모델을 모두 Test and Score에 이으세요. CA를 비교하세요.",
                "④ Predictions(예측)를 아래 File에 잇고, 세 모델도 Predictions에 이으세요. 모델끼리 답이 갈리는 웨이퍼를 찾으세요.",
                "⑤ 새 데이터에는 정답 열이 없어 처음에는 확률이 안 보입니다. Predictions 표 위의 Show probabilities for를 Classes known to the model로 바꾸세요.",
            ],
            "done_note": [
                "완성본: File(학습) → Tree·kNN·Logistic Regression → Test and Score(10겹), 세 모델 → Predictions ← File(새 웨이퍼).",
                "모델끼리 의견이 갈리는 웨이퍼는 사람이 다시 봐야 할 웨이퍼입니다. 예측은 판단을 돕는 도구입니다.",
            ],
        },
        {
            "n": 2, "topic": "newlots",
            "title": "10차시 ② 새 로트 9개의 합격·불합격 예측하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (학습: 공정 기록 750행)",
                 "data": weekly("week09", "week09_pass_fail_train")},
                {"id": "tree", "widget": TREE, "title": "Tree (결정 트리)", "settings": {"max_depth": 4}},
                {"id": "knn", "widget": KNN, "title": "kNN (이웃 투표)"},
                {"id": "logreg", "widget": LOGREG, "title": "Logistic Regression (로지스틱 회귀)"},
                {"id": "score", "widget": TEST_SCORE, "title": "Test and Score (평가)", "settings": dict(TEN_FOLDS)},
                {"id": "cm", "widget": CONFUSION, "title": "Confusion Matrix (헷갈림 표)"},
                {"id": "new", "widget": FILE, "title": "File (새 로트 9개)",
                 "data": weekly("week09", "week09_new_lots_to_predict")},
                {"id": "pred", "widget": PREDICTIONS, "title": "Predictions (예측)"},
            ],
            "links": [("file", "tree"), ("file", "knn"), ("file", "logreg"), ("file", "score"),
                      ("tree", "score", "Learner", "Learner"), ("knn", "score", "Learner", "Learner"),
                      ("logreg", "score", "Learner", "Learner"), ("score", "cm"),
                      ("new", "pred", "Data", "Data"), ("tree", "pred", "Model", "Predictors")],
            "start": ["file", "new"],
            "start_note": [
                "① 위 File은 9차시 공정 기록(학습용), 아래 File은 검사 전인 새 로트 9개입니다. 둘 다 이미 들어 있습니다.",
                "② (강사 시연) Tree(깊이 4)·kNN·Logistic Regression을 위 File에 잇고, Test and Score(10겹)에 세 모델을 모두 이으세요. Confusion Matrix도 이으세요.",
                "③ Predictions(예측)를 아래 File에 잇고 Tree를 Predictions에 이으세요. 9개 중 불합격(-1)으로 예측된 로트가 있나요?",
                "④ 새 데이터에는 정답 열이 없어 처음에는 확률이 안 보입니다. Predictions 표 위의 Show probabilities for를 Classes known to the model로 바꾸세요.",
            ],
            "done_note": [
                "완성본: File(학습) → Tree·kNN·Logistic Regression → Test and Score(10겹) → Confusion Matrix, Tree → Predictions ← File(새 로트).",
                "세 모델의 CA를 기준선과 함께 읽으세요. 예측은 '어느 로트부터 먼저 살펴볼지' 정하는 참고 도구이지 확정 판정이 아닙니다.",
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# 생성 로직
# ---------------------------------------------------------------------------
X0, DX, Y0, DY = 120, 180, 320, 140   # 노드 배치(왼쪽 → 오른쪽, 갈래는 아래로)
NOTE_RECT = (40.0, 30.0, 760.0, 190.0)


def ows_name(week, wf, kind):
    return f"{week}_{wf['n']}_{wf['topic']}_{kind}.ows"


def _auto_positions(wf):
    """File에서 몇 단계 떨어졌는지(depth)로 x를 정한다. 첫째 자식은 부모와 같은 줄에 두어
    한 줄로 이어지는 체인이 곧게 보이게 하고, 둘째 갈래부터는 아래 새 줄로 내린다."""
    parents = {}
    for link in wf["links"]:
        parents.setdefault(link[1], []).append(link[0])
    depth = {}

    def d(nid):
        if nid not in depth:
            depth[nid] = 0 if nid not in parents else 1 + max(d(p) for p in parents[nid])
        return depth[nid]

    row, used_first_child = {}, set()
    next_row = 0
    pos = {}
    for node in wf["nodes"]:
        nid = node["id"]
        parent = parents.get(nid, [None])[0]
        if parent in row and parent not in used_first_child:
            row[nid] = row[parent]
            used_first_child.add(parent)
        else:
            row[nid] = next_row
        next_row = max(next_row, row[nid] + 1)
        pos[nid] = node.get("position", (float(X0 + DX * d(nid)), float(Y0 + DY * row[nid])))
    return pos


def _input_table(wf, nid, ows_dir):
    """nid 위젯에 실제로 들어갈 표의 열 구성. 위쪽에 Select Columns가 있으면 그 열 구성으로 줄인다
    (Select Rows 같은 위젯 설정은 들어오는 열 구성에 맞춰 저장돼야 캔버스에서 되살아난다)."""
    from Orange.data import Table, Domain
    nodes = {n["id"]: n for n in wf["nodes"]}
    chain, cur = [], nid
    while nodes[cur]["widget"] != FILE:
        ups = [link[0] for link in wf["links"] if link[1] == cur]
        if not ups or ups[0] in chain:
            raise ValueError(f"{wf['topic']}: '{nid}' 노드 위쪽에서 File 위젯을 찾을 수 없습니다")
        cur = ups[0]
        chain.append(cur)
    table = Table(resolve_data_path(nodes[cur]["data"], ows_dir))
    for up in reversed(chain[:-1]):
        spec = nodes[up]
        roles = (spec.get("settings") or {}).get("columns")
        if spec["widget"] == SELECT_COLS and roles:
            d = table.domain
            pick = [[d[n] for n in roles.get(r, [])] for r in ("attribute", "class", "meta")]
            table = table.transform(Domain(pick[0], pick[1], pick[2]))
    return table


def resolve_data_path(data, ows_dir):
    """File 노드의 data 정의를 실제 파일 경로로 바꾼다(검증·설정 생성용)."""
    from Orange.widgets.data.owfile import get_sample_datasets_dir
    if data["prefix"] == "sample-datasets":
        return os.path.normpath(os.path.join(get_sample_datasets_dir(), data["relpath"]))
    return os.path.normpath(os.path.join(ows_dir, data["relpath"]))


def file_properties(data):
    from orangewidget.utils.filedialogs import RecentPath
    from Orange.widgets.data.owfile import OWFile
    # abspath에는 파일 이름만 둔다. 다른 PC의 절대경로가 남지 않게 하고, 경로를 못 찾았을 때
    # File 위젯 목록에 파일 이름이 빨간색으로 보이게 하기 위함이다. 실제 위치는 prefix + relpath로 찾는다.
    abspath = "" if data["prefix"] == "sample-datasets" else os.path.basename(data["relpath"])
    return {
        "recent_paths": [RecentPath(abspath, data["prefix"], data["relpath"])],
        "source": OWFile.LOCAL_FILE,
        "recent_urls": [],
        "url": "",
        "sheet_names": {},
        "controlAreaVisible": True,
        "context_settings": [],
        "__version__": OWFile.settings_version,
    }


def _apply_select_rows(widget, settings, data):
    ops = widget.Operators
    conditions = settings.pop("conditions", None)
    if conditions is not None:
        widget.remove_all_rows()
        for name, op_name, values in conditions:
            var = data.domain[name]
            names = [op[1] for op in ops[type(var)]]
            if op_name not in names:
                raise ValueError(f"Select Rows: '{name}'에 쓸 수 없는 연산자 '{op_name}' (가능: {names})")
            if var.is_discrete:
                # 범주형 값은 화면 목록("" + 값들)의 번호로 저장된다 → 값 이름을 1부터 센 번호로 바꾼다
                unknown = [v for v in values if v not in var.values]
                if unknown:
                    raise ValueError(f"Select Rows: '{name}'에 없는 값 {unknown} (가능: {list(var.values)})")
                values = [str(var.values.index(v) + 1) for v in values]
            widget.add_row(var, names.index(op_name), list(values))
        widget.conditions_changed()
    return settings


def _apply_impute(widget, settings, data):
    from Orange.widgets.data.owimpute import Method
    default = settings.pop("default_method", None)
    if default is not None:
        widget.set_default_method(int(Method[default]))
    for name, method in settings.pop("methods", {}).items():
        names = [v.name for v in widget.varmodel]
        index = widget.varmodel.index(names.index(name))
        widget.set_method_for_indexes([index], Method[method])
    return settings


def _apply_select_columns(widget, settings, data):
    """{"columns": {"attribute": [...], "class": [...], "meta": [...]}} — 적지 않은 열은 Ignored(available)로 보낸다."""
    roles = settings.pop("columns", None)
    if roles is not None:
        all_vars = list(data.domain.variables + data.domain.metas)
        named = {v.name: v for v in all_vars}
        listed = [n for names in roles.values() for n in names]
        unknown = [n for n in listed if n not in named]
        if unknown:
            raise ValueError(f"Select Columns: 데이터에 없는 열 {unknown}")
        widget.used_attrs[:] = [named[n] for n in roles.get("attribute", [])]
        widget.class_attrs[:] = [named[n] for n in roles.get("class", [])]
        widget.meta_attrs[:] = [named[n] for n in roles.get("meta", [])]
        widget.available_attrs[:] = [v for v in all_vars if v.name not in listed]
        widget.update_domain_role_hints()
        widget.commit.now() if hasattr(widget.commit, "now") else widget.commit()
    return settings


ADAPTERS = {
    SELECT_ROWS: _apply_select_rows,
    IMPUTE: _apply_impute,
    SELECT_COLS: _apply_select_columns,
}


def widget_properties(qualified_name, settings, data):
    """위젯을 화면 없이 만들고 데이터를 넣은 뒤 settings를 반영해 Orange 형식으로 저장할 값을 얻는다."""
    from Orange.data import Variable
    module, cls_name = qualified_name.rsplit(".", 1)
    cls = getattr(__import__(module, fromlist=[cls_name]), cls_name)
    widget = cls()
    try:
        handlers = [sig.handler for sig in cls.get_signals("inputs") if sig.name == "Data"]
        if handlers:
            getattr(widget, handlers[0])(data)   # 위젯마다 이름이 다르다(set_data, set_train_data …)
            widget.handleNewSignals()
        elif any(isinstance(v, str) for v in settings.values()) or qualified_name in ADAPTERS:
            # 'Data' 입력이 없는 위젯(Tree Viewer 등)은 열 이름이 필요 없는 일반 설정만 저장할 수 있다
            raise ValueError(f"{qualified_name}: 'Data' 입력이 없어 열 이름 설정을 만들 수 없습니다")
        rest = dict(settings)
        adapter = ADAPTERS.get(qualified_name)
        if adapter:
            rest = adapter(widget, rest, data)
        for key, value in rest.items():
            current = getattr(widget, key)
            if isinstance(value, str) and (current is None or isinstance(current, Variable)):
                value = data.domain[value]
            setattr(widget, key, value)
        widget.storeSpecificSettings()
        props = widget.settingsHandler.pack_data(widget)
    finally:
        widget.onDeleteWidget()
        widget.deleteLater()
    props.pop("savedWidgetGeometry", None)
    return props


def build_scheme(week, wf, kind, registry, ows_dir):
    from Orange.data import Table
    from orangecanvas.scheme import Scheme, SchemeNode, SchemeLink, SchemeTextAnnotation

    keep = None
    if kind == "start":
        keep = set(wf.get("start") or [n["id"] for n in wf["nodes"] if n["widget"] == FILE])
    positions = _auto_positions(wf)
    label = "시작" if kind == "start" else "완성"
    scheme = Scheme(title=f"{wf['title']} ({label})",
                    description="교육용 가상 데이터 실습 워크플로. "
                                "data/weekly 폴더와 orange3 폴더를 키트의 폴더 구조 그대로 두고 여세요.")
    nodes = {}
    for spec in wf["nodes"]:
        if keep is not None and spec["id"] not in keep:
            continue
        desc = registry.widget(spec["widget"])
        if spec["widget"] == FILE:
            props = file_properties(spec["data"])
        elif spec.get("settings"):
            props = widget_properties(spec["widget"], spec["settings"], _input_table(wf, spec["id"], ows_dir))
        else:
            props = None
        node = SchemeNode(desc, title=spec["title"], position=positions[spec["id"]], properties=props)
        scheme.add_node(node)
        nodes[spec["id"]] = node

    for link in wf["links"]:
        src, dst = link[0], link[1]
        if src not in nodes or dst not in nodes:
            continue
        if len(link) == 4:
            out_ch, in_ch = link[2], link[3]
        else:
            proposals = scheme.propose_links(nodes[src], nodes[dst])
            if not proposals:
                raise ValueError(f"{ows_name(week, wf, kind)}: {src} → {dst} 연결할 수 있는 채널이 없습니다")
            out_ch, in_ch, _ = max(proposals, key=lambda p: p[2])
        scheme.add_link(SchemeLink(nodes[src], out_ch, nodes[dst], in_ch))

    note = wf["start_note"] if kind == "start" else wf["done_note"]
    scheme.add_annotation(SchemeTextAnnotation(NOTE_RECT, "\n".join(note), font={"size": 16}))
    return scheme


def write_ows(scheme, path):
    import logging
    from orangecanvas.scheme.readwrite import scheme_to_ows_stream
    # 위젯 설정(Context, RecentPath)은 파이썬 리터럴로 못 쓰므로 Orange 캔버스처럼 pickle로 저장한다.
    # 그때 남기는 "Using pickle fallback" 경고·추적 로그는 정상 동작이라 숨긴다.
    logging.getLogger("orangecanvas.scheme.readwrite").setLevel(logging.ERROR)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        scheme_to_ows_stream(scheme, f, pretty=True, pickle_fallback=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--week", type=int, help="이 차시만 생성(예: 5)")
    args = parser.parse_args()

    from _orange_env import check_orange_version, widget_registry
    app = QApplication.instance() or QApplication([])  # noqa: F841  위젯 생성에 필요
    check_orange_version()
    registry = widget_registry()

    weeks = [f"week{args.week:02d}"] if args.week else sorted(WORKFLOWS)
    for week in weeks:
        if week not in WORKFLOWS:
            print(f"[건너뜀] {week}: WORKFLOWS에 정의가 없습니다")
            continue
        ows_dir = os.path.join(OUT, week)
        written = set()
        for wf in WORKFLOWS[week]:
            for kind in ("start", "done"):
                path = os.path.join(ows_dir, ows_name(week, wf, kind))
                write_ows(build_scheme(week, wf, kind, registry, ows_dir), path)
                written.add(os.path.basename(path))
                print(f"[생성] {os.path.relpath(path, BASE)}")
        # 정의에서 빠진(이름이 바뀐) 옛 .ows는 지운다
        for f in os.listdir(ows_dir):
            if f.endswith(".ows") and f not in written:
                os.remove(os.path.join(ows_dir, f))
                print(f"[삭제] {os.path.relpath(os.path.join(ows_dir, f), BASE)} (정의에 없음)")
    print("\nOrange 워크플로 생성 완료. 검증: python scripts/validate_orange_workflows.py")


if __name__ == "__main__":
    main()
