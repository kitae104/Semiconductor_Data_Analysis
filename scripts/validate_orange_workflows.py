"""Orange3 워크플로(.ows) 검증 스크립트.

orange3/week*/*.ows 전부에 대해 확인한다.
1. 파싱: Orange 캔버스 읽기 함수로 열리고, 모든 위젯이 Orange 3.35 위젯 목록에 있다.
2. 이식성: File 위젯 경로가 prefix(basedir / sample-datasets) + 상대경로로 저장돼 있고,
   다른 PC의 절대경로가 남아 있지 않다. 그 상대경로가 .ows 폴더(또는 Orange 내장 데이터 폴더) 기준으로 실제 파일을 가리킨다.
3. 데이터: Orange.data.Table로 열리고, 열 이름에 BOM이 없으며, 결과 열(합격여부 등)이 범주형이다.
4. 짝: weekXX_N_주제_start.ows와 _done.ows가 함께 있고 같은 데이터를 연다. _start에는 안내 메모가 있다.
5. 실행: 화면 없이(QT_QPA_PLATFORM=offscreen) 워크플로를 통째로 띄워 신호를 흘려 보낸다.
   File이 데이터를 내보내는지, (_done에서) 모든 연결선에 데이터가 흐르는지, 위젯 오류가 없는지 본다.
   연결선마다 흐른 행 수를 출력한다(강의·운영안에 적을 Orange 쪽 실제 수치).

실행: python scripts/validate_orange_workflows.py [--week 5]
      (Orange 파이썬이 아니면 Orange 파이썬으로 스스로 다시 실행된다)
FAIL이 하나라도 있으면 종료 코드 1.
"""
import argparse
import glob
import os
import re
import sys
import time

sys.dont_write_bytecode = True  # scripts/__pycache__를 남기지 않는다
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _orange_env import ensure_orange_python  # noqa: E402

ensure_orange_python(__file__)

from AnyQt.QtWidgets import QApplication  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWS_ROOT = os.path.join(BASE, "orange3")
OWS_NAME = re.compile(r"^(week\d{2})_(\d+)_([a-z0-9_]+)_(start|done)\.ows$")
# generate_weekly_data.py의 ORANGE_CLASS_COLUMNS와 같은 목록: Orange에서 범주형이어야 하는 결과 열
CLASS_COLUMNS = {"합격여부", "진행여부", "정답여부", "평가", "손님평가"}
FILE_QNAME = "Orange.widgets.data.owfile.OWFile"

RESULTS = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    RESULTS.append((name, status, detail))
    print(f"[{status}] {name}" + (f" - {detail}" if detail and status == "FAIL" else ""))
    return condition


def info(text):
    print(f"       {text}")


def file_nodes(desc):
    """파싱된 .ows에서 File 노드와 저장된 설정(dict)을 꺼낸다."""
    from orangecanvas.scheme.readwrite import loads
    out = []
    for node in desc.nodes:
        if node.qualified_name == FILE_QNAME:
            props = loads(node.data.data, node.data.format) if node.data else {}
            out.append((node, props))
    return out


def resolve_recent(rp, ows_dir):
    from Orange.widgets.data.owfile import get_sample_datasets_dir
    if rp.prefix == "basedir":
        return os.path.normpath(os.path.join(ows_dir, rp.relpath))
    if rp.prefix == "sample-datasets":
        return os.path.normpath(os.path.join(get_sample_datasets_dir(), rp.relpath))
    return None


def check_static(path, registry):
    """파싱·위젯 존재·File 경로·데이터 로드. File이 여는 경로 목록을 돌려준다."""
    from Orange.data import Table
    from orangecanvas.scheme.readwrite import parse_ows_stream
    name = os.path.relpath(path, BASE).replace("\\", "/")
    ows_dir = os.path.dirname(path)
    try:
        with open(path, "rb") as f:
            desc = parse_ows_stream(f)
    except Exception as e:  # noqa: BLE001
        check(f"{name} 파싱", False, repr(e))
        return None, None
    check(f"{name} 파싱", True)
    missing = [n.qualified_name for n in desc.nodes if not registry.has_widget(n.qualified_name)]
    check(f"{name} 위젯이 모두 Orange 위젯 목록에 있음({len(desc.nodes)}개)", not missing, f"없음: {missing}")

    data_paths = []
    files = file_nodes(desc)
    check(f"{name} File 위젯 1개 이상", len(files) > 0)
    for node, props in files:
        paths = props.get("recent_paths") or []
        if not check(f"{name} [{node.title}] 저장된 경로 있음", bool(paths)):
            continue
        rp = paths[0]
        check(f"{name} [{node.title}] 경로가 이식 가능(prefix={rp.prefix}, relpath={rp.relpath})",
              rp.prefix in ("basedir", "sample-datasets") and rp.relpath and not os.path.isabs(rp.relpath)
              and not os.path.isabs(rp.abspath or ""),
              f"abspath={rp.abspath!r}")
        check(f"{name} [{node.title}] source=LOCAL_FILE", props.get("source", 0) == 0, str(props.get("source")))
        target = resolve_recent(rp, ows_dir)
        if not check(f"{name} [{node.title}] 경로가 실제 파일을 가리킴", target is not None and os.path.exists(target),
                     str(target)):
            continue
        data_paths.append(target)
        try:
            table = Table(target)
        except Exception as e:  # noqa: BLE001
            check(f"{name} [{node.title}] Orange.data.Table 로드", False, repr(e))
            continue
        names = [v.name for v in table.domain.variables + table.domain.metas]
        check(f"{name} [{node.title}] 데이터 로드 {len(table)}행, 열 이름에 BOM 없음",
              not any(n.startswith("﻿") for n in names), str(names[:3]))
        not_disc = [v.name for v in table.domain.variables + table.domain.metas
                    if v.name in CLASS_COLUMNS and not v.is_discrete]
        check(f"{name} [{node.title}] 결과 열(합격여부 등)이 범주형", not not_disc, f"연속형으로 읽힘: {not_disc}")
    if name.endswith("_start.ows"):
        check(f"{name} 안내 메모(캔버스 주석) 있음", any(a.type == "text" for a in desc.annotations))
    return desc, data_paths


def run_workflow(path, registry, timeout=60.0):
    """워크플로를 화면 없이 띄워 신호를 흘려 보내고 결과를 확인한다."""
    from orangewidget.workflow.widgetsscheme import WidgetsScheme
    from orangecanvas.scheme.readwrite import scheme_load
    app = QApplication.instance()
    name = os.path.relpath(path, BASE).replace("\\", "/")
    scheme = WidgetsScheme()
    scheme.set_runtime_env("basedir", os.path.dirname(path))
    errors = []
    with open(path, "rb") as f:
        scheme_load(scheme, f, registry=registry, error_handler=errors.append)
    check(f"{name} 캔버스 불러오기 오류 없음", not errors, "; ".join(map(str, errors)))
    sm, wm = scheme.signal_manager, scheme.widget_manager

    def busy():
        if sm.has_pending():
            return True
        for node in scheme.nodes:
            w = wm.widget_for_node(node)
            if w is None or (hasattr(w, "isBlocking") and w.isBlocking()):
                return True
        return False

    # File은 QTimer로 데이터를 읽고, 몇몇 위젯은 스레드로 계산한다 → 조용해질 때까지 이벤트를 돌린다.
    start, quiet_since = time.time(), None
    while time.time() - start < timeout:
        app.processEvents()
        time.sleep(0.02)
        if busy():
            quiet_since = None
        elif quiet_since is None:
            quiet_since = time.time()
        elif time.time() - quiet_since > 0.7:
            break
    check(f"{name} 신호 처리 완료", not busy(), f"{timeout}초 안에 끝나지 않음")

    is_done = name.endswith("_done.ows")
    for node in scheme.nodes:
        w = wm.widget_for_node(node)
        errs = [str(m.formatted) for m in w.Error.active]
        check(f"{name} [{node.title}] 위젯 오류 없음", not errs, "; ".join(errs))
        warns = [str(m.formatted) for m in w.Warning.active]
        if warns:
            info(f"[{node.title}] 경고: {'; '.join(warns)}")
        if node.description.qualified_name == FILE_QNAME:
            check(f"{name} [{node.title}] 데이터를 내보냄", getattr(w, "data", None) is not None,
                  "; ".join(str(m.formatted) for m in w.Information.active))
    for link in scheme.links:
        values = [v for v in sm.link_contents(link).values() if v is not None]
        label = f"{link.source_node.title} → {link.sink_node.title}"
        if values:
            v = values[-1]
            size = f"{len(v)}행" if hasattr(v, "__len__") else type(v).__name__
            info(f"{label}: {size}")
        if is_done:
            check(f"{name} 연결선에 데이터가 흐름: {label}", bool(values))

    scheme.clear()
    scheme.deleteLater()
    app.processEvents()


def main():
    parser = argparse.ArgumentParser(description="Orange3 워크플로(.ows) 검증")
    parser.add_argument("--week", type=int, help="이 차시만 검사(예: 5)")
    parser.add_argument("--no-run", action="store_true", help="위젯을 띄워 실행하는 검사는 건너뜀")
    args = parser.parse_args()

    from _orange_env import check_orange_version, widget_registry
    app = QApplication.instance() or QApplication([])  # noqa: F841
    check_orange_version()
    registry = widget_registry()

    pattern = f"week{args.week:02d}" if args.week else "week*"
    paths = sorted(glob.glob(os.path.join(OWS_ROOT, pattern, "*.ows")))
    check(f"검사할 .ows 파일 있음({len(paths)}개)", bool(paths), os.path.join(OWS_ROOT, pattern))
    stray = sorted(glob.glob(os.path.join(OWS_ROOT, "*.ows")))
    check("orange3/ 바로 아래에 옛 .ows가 남아 있지 않음", not stray, ", ".join(os.path.basename(p) for p in stray))

    pairs = {}
    for path in paths:
        fname = os.path.basename(path)
        m = OWS_NAME.match(fname)
        if not check(f"{fname} 파일 이름 규칙(weekXX_N_주제_start|done.ows)", bool(m)):
            continue
        check(f"{fname} 차시 폴더와 이름이 맞음", m.group(1) == os.path.basename(os.path.dirname(path)))
        print(f"\n=== {os.path.relpath(path, BASE)} ===")
        _, data_paths = check_static(path, registry)
        pairs.setdefault((os.path.dirname(path), m.group(1), m.group(2), m.group(3)), {})[m.group(4)] = data_paths
        if not args.no_run:
            run_workflow(path, registry)

    print("\n=== start/done 짝 ===")
    for (_, week, n, topic), kinds in sorted(pairs.items()):
        key = f"{week}_{n}_{topic}"
        if check(f"{key} start/done 짝이 모두 있음", set(kinds) == {"start", "done"}, str(sorted(kinds))):
            check(f"{key} start와 done이 같은 데이터를 엶", kinds["start"] == kinds["done"],
                  f"start {kinds['start']} / done {kinds['done']}")

    total = len(RESULTS)
    failed = sum(1 for _, s, _ in RESULTS if s == "FAIL")
    print(f"\n총 {total}건 중 {total - failed}건 통과, {failed}건 실패")
    for name, status, detail in RESULTS:
        if status == "FAIL":
            print(f"  FAIL {name} {detail}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
