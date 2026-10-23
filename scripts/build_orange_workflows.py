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
                {"id": "stats", "widget": STATS, "title": "Feature Statistics (열 통계)"},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("승차인원_count", -1)]}},
            ],
            "links": [("file", "stats"), ("file", "table")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭하면 지하철 8개 역 × 3시간대 승하차 기록(24행)이 이미 들어 있습니다.",
                "② 왼쪽 Data 묶음에서 Feature Statistics(열 통계)를 끌어 와 File과 이으세요. 승차인원_count 줄의 Mean(평균)과 Max(최고)를 비교하세요.",
                "③ Data Table(표 보기)을 File에 잇고, 승차인원_count 열 이름을 두 번 눌러 큰 값부터 정렬하세요. 맨 위 행은 어느 역·시간대인가요?",
            ],
            "done_note": [
                "완성본: File → Feature Statistics(열 통계), File → Data Table(표 보기, 승차인원_count 큰 값부터).",
                "Max가 Mean보다 훨씬 큽니다. 평균만 보면 유난히 붐비는 한 곳이 안 보입니다 — 최고·최저를 같이 보세요.",
            ],
        },
        {
            "n": 2, "topic": "temps",
            "title": "2차시 ② 설비 온도 기록 20건 요약하기",
            "nodes": [
                {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
                 "data": weekly("week02", "week02_python_basics_1")},
                {"id": "stats", "widget": STATS, "title": "Feature Statistics (열 통계)"},
                {"id": "table", "widget": TABLE, "title": "Data Table (표 보기)",
                 "settings": {"stored_sort": [("설비번호", 1)]}},
            ],
            "links": [("file", "stats"), ("file", "table")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 설비 온도 기록(20행)이 들어왔는지 확인하세요.",
                "② Feature Statistics(열 통계)를 File에 이어 온도_C의 Min·Max·Mean을 읽으세요.",
                "③ Data Table(표 보기)을 File에 잇고 설비번호 열 이름을 눌러 정렬하세요. EQ-03 행만 모아 보고 그중 가장 높은 온도를 찾으세요.",
            ],
            "done_note": [
                "완성본: File → Feature Statistics(열 통계), File → Data Table(표 보기, 설비번호 순).",
                "표 전체의 Max와 EQ-03 행들 중 최고 온도를 비교하세요. 어느 범위를 담았는지에 따라 답이 다릅니다.",
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
                {"id": "stats", "widget": STATS, "title": "Feature Statistics (정리 전)"},
                {"id": "impute", "widget": IMPUTE, "title": "Impute (빈칸 채우기)",
                 "settings": {"default_method": "Average"}},
                {"id": "select", "widget": SELECT_ROWS, "title": "Select Rows (행 고르기)",
                 "settings": {"conditions": [
                     ("파티클_count_per_m3", "is below", ["10000"]),
                     ("차압_Pa", "is at least", ["0"]),
                 ]}},
                {"id": "stats_after", "widget": STATS, "title": "Feature Statistics (정리 후)"},
                {"id": "filled", "widget": TABLE, "title": "Data Table (채운 뒤)"},
            ],
            "links": [("file", "stats"), ("file", "impute"), ("impute", "select"),
                      ("select", "stats_after", "Matching Data", "Data"), ("impute", "filled")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 클린룸 기록(72행)이 들어왔는지 확인하세요.",
                "② Feature Statistics(열 통계)를 File에 이어 빈칸 수(Missing)와 파티클의 가장 큰 값(Max)을 찾으세요.",
                "③ Impute(빈칸 채우기)를 File에 잇고, Impute에 Data Table을 이어 빈칸이 어떤 값으로 채워졌는지 보세요.",
                "④ Impute에 Select Rows(파티클 is below 10000, 차압 is at least 0) → Feature Statistics를 이어 정리 전과 비교하세요.",
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
                {"id": "stats", "widget": STATS, "title": "Feature Statistics (정리 전)"},
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
                {"id": "stats_after", "widget": STATS, "title": "Feature Statistics (정리 후)"},
            ],
            "links": [("file", "stats"), ("file", "impute"), ("impute", "select"),
                      ("select", "table", "Matching Data", "Data"),
                      ("select", "stats_after", "Matching Data", "Data")],
            "start_note": [
                "① File(파일 불러오기)을 더블클릭해 공정 데이터(113행)가 들어왔는지 확인하세요.",
                "② Feature Statistics(열 통계)를 File에 이어 빈칸(Missing)과 Min·Max가 이상한 열을 찾으세요.",
                "③ Impute(빈칸 채우기) → Select Rows(행 고르기) → Data Table 순서로 이어 이상값을 걸러 내세요.",
                "④ Select Rows에 Feature Statistics를 하나 더 이어 정리 전과 비교하세요.",
            ],
            "done_note": [
                "완성본: Impute는 숫자 빈칸을 평균으로 채우고, 합격여부가 빈 행은 지웁니다(Remove instances).",
                "Select Rows 조건: 온도_C ≤ 400, 압력_Pa ≥ 0, 0 ≤ 가스유량_slm < 200.",
                "Feature Statistics(정리 전)와 (정리 후)의 Min·Max·Mean을 비교하고, 남은 행 수를 파이썬 결과와 비교하세요.",
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


def _root_file(wf, nid):
    nodes = {n["id"]: n for n in wf["nodes"]}
    seen = set()
    while nodes[nid]["widget"] != FILE:
        seen.add(nid)
        ups = [link[0] for link in wf["links"] if link[1] == nid]
        if not ups or ups[0] in seen:
            raise ValueError(f"{wf['topic']}: '{nid}' 노드 위쪽에서 File 위젯을 찾을 수 없습니다")
        nid = ups[0]
    return nodes[nid]


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


ADAPTERS = {
    SELECT_ROWS: _apply_select_rows,
    IMPUTE: _apply_impute,
}


def widget_properties(qualified_name, settings, data):
    """위젯을 화면 없이 만들고 데이터를 넣은 뒤 settings를 반영해 Orange 형식으로 저장할 값을 얻는다."""
    from Orange.data import Variable
    module, cls_name = qualified_name.rsplit(".", 1)
    cls = getattr(__import__(module, fromlist=[cls_name]), cls_name)
    widget = cls()
    try:
        handlers = [sig.handler for sig in cls.get_signals("inputs") if sig.name == "Data"]
        if not handlers:
            raise ValueError(f"{qualified_name}: 'Data' 입력이 없어 설정을 만들 수 없습니다")
        getattr(widget, handlers[0])(data)   # 위젯마다 이름이 다르다(set_data, set_train_data …)
        widget.handleNewSignals()
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
            root = _root_file(wf, spec["id"])
            table = Table(resolve_data_path(root["data"], ows_dir))
            props = widget_properties(spec["widget"], spec["settings"], table)
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
