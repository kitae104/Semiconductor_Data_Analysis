"""학생용 실습 키트(zip)를 만드는 스크립트.

노트북의 `../../data/...` 경로와 .ows File 위젯의 상대경로는 폴더 구조가 그대로일 때만 동작한다.
그래서 노트북·데이터·Orange 워크플로를 저장소와 같은 폴더 구조로 묶는다.

- dist/student_kit.zip : notebooks/student, data/weekly(orange/ 포함), orange3, docs/setup.html(있으면) + 그 페이지가 쓰는 assets(CSS·JS·로고·캡처), README_학생용.txt
- dist/weekXX_kit.zip  : 그 차시 학생 노트북, 그 차시 데이터(+노트북·.ows가 참조하는 다른 차시 데이터), orange3/weekXX
- --with-solutions     : 정답 노트북(notebooks/solutions)도 넣는다(강사용).
- --check              : 만든 zip을 임시 폴더에 풀어 노트북의 ../../data 경로와 .ows File 경로가
                         압축 푼 폴더 안에서 실제 파일을 가리키는지 확인한다. 실패하면 종료 코드 1.

zip 안의 파일 시각을 고정해 내용이 같으면 몇 번 만들어도 같은 zip이 나온다.

실행:
    python scripts/build_student_kit.py
    python scripts/build_student_kit.py --check
    python scripts/build_student_kit.py --with-solutions --check
"""
import argparse
import base64
import glob
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(BASE, "dist")
ROOT_DIR = "semiconductor_kit"          # zip 안 최상위 폴더(압축을 풀면 이 폴더 하나가 생긴다)
FIXED_TIME = (2024, 3, 1, 0, 0, 0)
SKIP_PARTS = {".ipynb_checkpoints", "__pycache__"}

NB_DATA_REF = re.compile(r"\.\./\.\./data/[^\"'\\\s)]+")
OWS_DATA_REF = re.compile(rb"\.\./\.\./data/[A-Za-z0-9_./-]+")
ABS_PATH = re.compile(rb"[A-Za-z]:[\\/]|/Users/|/home/")
FILE_QNAME = "Orange.widgets.data.owfile.OWFile"
KIT_PAGES = ["docs/setup.html"]                               # 키트에 넣는 안내 페이지
HTML_REF = re.compile(r'(?:href|src)="(\.\./[^"#?]+)"')

README = """반도체 공정 데이터 분석 — 학생용 실습 키트

이 폴더의 구조를 바꾸지 마세요.
노트북과 Orange 파일은 서로의 위치를 기준으로 데이터를 찾습니다.
파일을 하나씩 꺼내 다른 곳으로 옮기면 데이터를 찾지 못합니다.

[폴더 안내]
- notebooks/student/      주피터 노트북 (weekXX_student.ipynb)
- data/weekly/weekXX/     실습 데이터 (CSV)
  - orange/               Orange에서 여는 같은 데이터 (.tab)
- orange3/weekXX/         Orange 워크플로
  - ..._start.ows         시작 파일 (데이터가 이미 연결된 File 위젯에서 출발)
  - ..._done.ows          완성본 (막혔을 때 열어 보기)
{setup_line}
[사용법]
1. 압축을 푼 폴더를 그대로 둡니다.
2. 노트북: Jupyter에서 notebooks/student 폴더의 weekXX_student.ipynb를 엽니다.
3. Orange: Orange 3.35에서 File > Open으로 orange3/weekXX 폴더의 _start.ows를 엽니다.
4. File 위젯에 빨간 글씨가 보이거나 데이터가 비어 있으면,
   압축을 푼 폴더 구조가 바뀌지 않았는지 먼저 확인하세요.

이 키트의 모든 데이터는 교육용 가상 데이터이며 실제 기업 생산 데이터가 아닙니다.
"""


def rel(path):
    return os.path.relpath(path, BASE).replace("\\", "/")


def walk_files(*patterns):
    out = []
    for pattern in patterns:
        for path in glob.glob(os.path.join(BASE, pattern), recursive=True):
            if os.path.isfile(path) and not (SKIP_PARTS & set(rel(path).split("/"))):
                out.append(rel(path))
    return sorted(set(out))


def ows_file_nodes(xml_bytes):
    """.ows에서 File 노드의 저장된 설정(pickle을 base64로 푼 바이트)을 꺼낸다. Orange 없이 읽는다."""
    root = ET.fromstring(xml_bytes)
    file_ids = {n.get("id") for n in root.iter("node") if n.get("qualified_name") == FILE_QNAME}
    out = []
    for prop in root.iter("properties"):
        if prop.get("node_id") in file_ids:
            data = prop.text or ""
            out.append(base64.decodebytes(data.encode("ascii")) if prop.get("format") == "pickle" else data.encode())
    return file_ids, out


def data_refs(relpath):
    """노트북·.ows가 참조하는 data/ 경로(저장소 기준)."""
    path = os.path.join(BASE, relpath)
    here = os.path.dirname(relpath)
    if relpath.endswith(".ipynb"):
        with open(path, encoding="utf-8") as f:
            refs = NB_DATA_REF.findall(f.read())
    elif relpath.endswith(".ows"):
        with open(path, "rb") as f:
            _, props = ows_file_nodes(f.read())
        refs = [m.decode() for p in props for m in OWS_DATA_REF.findall(p)]
    else:
        refs = []
    return sorted({os.path.normpath(os.path.join(here, r)).replace("\\", "/") for r in refs})


def page_assets(relpath):
    """키트에 넣는 HTML(docs/setup.html)이 키트 안에서도 디자인대로 보이도록 필요한 assets 파일.
    공통 CSS 전부 + 그 페이지가 href/src로 가리키는 assets 파일 중 저장소에 실제로 있는 것
    (아직 캡처하지 않은 data-shot 그림은 없으면 건너뛴다). 웹 글꼴은 CSS가 인터넷에서 불러온다."""
    if not os.path.exists(os.path.join(BASE, relpath)):
        return []
    with open(os.path.join(BASE, relpath), encoding="utf-8") as f:
        refs = HTML_REF.findall(f.read())
    here = os.path.dirname(relpath)
    out = walk_files("assets/css/*.css")
    for ref in refs:
        target = os.path.normpath(os.path.join(here, ref)).replace("\\", "/")
        if target.startswith("assets/") and os.path.isfile(os.path.join(BASE, target)):
            out.append(target)
    return out


def kit_files(weeks, with_solutions):
    """키트에 넣을 저장소 기준 파일 목록. weeks=None이면 전체."""
    if weeks is None:
        files = walk_files("notebooks/student/*.ipynb", "data/weekly/**/*.csv", "data/weekly/**/*.tab",
                           "orange3/week*/*.ows", "docs/setup.html")
        if with_solutions:
            files += walk_files("notebooks/solutions/*.ipynb")
    else:
        files = []
        for w in weeks:
            files += walk_files(f"notebooks/student/{w}_student.ipynb", f"data/weekly/{w}/**/*.csv",
                                f"data/weekly/{w}/**/*.tab", f"orange3/{w}/*.ows", "docs/setup.html")
            if with_solutions:
                files += walk_files(f"notebooks/solutions/{w}_solution.ipynb")
        # 다른 차시 데이터를 쓰는 노트북·워크플로(예: 10차시가 9차시 데이터 사용)를 위해 참조 파일과 그 .tab도 넣는다
        extra = []
        for f in files:
            for ref in data_refs(f):
                extra.append(ref)
                stem, ext = os.path.splitext(ref)
                if ext == ".csv":
                    tab = f"{os.path.dirname(ref)}/orange/{os.path.basename(stem)}.tab"
                    if os.path.exists(os.path.join(BASE, tab)):
                        extra.append(tab)
        files += [e for e in extra if os.path.exists(os.path.join(BASE, e))]
    for page in KIT_PAGES:
        if page in files:
            files += page_assets(page)
    return sorted(set(files))


def write_zip(zip_path, files, setup_included):
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    setup_line = "- docs/setup.html          수강 전 준비(설치·키트 사용법) 안내\n" if setup_included else ""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        def add(arcname, data):
            info = zipfile.ZipInfo(f"{ROOT_DIR}/{arcname}", date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)

        add("README_학생용.txt", README.format(setup_line=setup_line).encode("utf-8"))
        for f in files:
            with open(os.path.join(BASE, f), "rb") as fh:
                add(f, fh.read())


def check_zip(zip_path, with_solutions):
    """압축을 풀어 경로가 풀린 폴더 안에서 해석되는지 확인한다. 실패 목록을 돌려준다."""
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        root = os.path.join(tmp, ROOT_DIR)
        if not os.path.exists(os.path.join(root, "README_학생용.txt")):
            fails.append("README_학생용.txt 없음")
        has_solutions = bool(glob.glob(os.path.join(root, "notebooks", "solutions", "*.ipynb")))
        if has_solutions != with_solutions:
            fails.append(f"정답 노트북 포함 여부가 옵션과 다름(포함={has_solutions})")
        n_nb = n_ows = n_ref = 0
        for nb in glob.glob(os.path.join(root, "notebooks", "**", "*.ipynb"), recursive=True):
            n_nb += 1
            with open(nb, encoding="utf-8") as f:
                for ref in sorted(set(NB_DATA_REF.findall(f.read()))):
                    n_ref += 1
                    if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(nb), ref))):
                        fails.append(f"{os.path.relpath(nb, root)}: {ref} 없음")
        for ows in glob.glob(os.path.join(root, "orange3", "**", "*.ows"), recursive=True):
            n_ows += 1
            name = os.path.relpath(ows, root)
            with open(ows, "rb") as f:
                file_ids, props = ows_file_nodes(f.read())
            if len(props) != len(file_ids):
                fails.append(f"{name}: 설정이 없는 File 위젯이 있음")
            for p in props:
                if ABS_PATH.search(p):
                    fails.append(f"{name}: File 설정에 절대경로가 남아 있음")
                refs = [m.decode() for m in OWS_DATA_REF.findall(p)]
                if not refs and b"sample-datasets" not in p:
                    fails.append(f"{name}: File 경로가 ../../data/... 도 Orange 내장 데이터도 아님")
                for ref in refs:
                    n_ref += 1
                    if b"basedir" not in p:
                        fails.append(f"{name}: {ref} 경로의 prefix가 basedir가 아님")
                    if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(ows), ref))):
                        fails.append(f"{name}: {ref} 없음")
        n_asset = 0
        for page in KIT_PAGES:
            path = os.path.join(root, page)
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as f:
                for ref in sorted(set(HTML_REF.findall(f.read()))):
                    target = os.path.normpath(os.path.join(os.path.dirname(page), ref)).replace("\\", "/")
                    if not target.startswith("assets/"):
                        continue
                    n_asset += 1
                    # 저장소에 있는 파일은 키트에도 있어야 한다(없는 것은 아직 캡처 전인 data-shot 자리)
                    if os.path.isfile(os.path.join(BASE, target)) and not os.path.exists(os.path.join(root, target)):
                        fails.append(f"{page}: {ref} 없음")
            for css in walk_files("assets/css/*.css"):
                if not os.path.exists(os.path.join(root, css)):
                    fails.append(f"{page}: {css} 없음")
        print(f"       노트북 {n_nb}개, .ows {n_ows}개, 데이터 경로 {n_ref}개, 안내 페이지 assets 경로 {n_asset}개 확인")
    return fails


def human(n):
    return f"{n / 1024:.1f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.2f} MB"


def main():
    parser = argparse.ArgumentParser(description="학생용 실습 키트(zip) 만들기")
    parser.add_argument("--with-solutions", action="store_true", help="정답 노트북도 넣기(강사용)")
    parser.add_argument("--check", action="store_true", help="압축을 풀어 경로가 해석되는지 확인")
    args = parser.parse_args()

    setup = os.path.exists(os.path.join(BASE, "docs", "setup.html"))
    if not setup:
        print("[알림] docs/setup.html이 아직 없어 키트에서 빠집니다.")
    weeks = sorted({os.path.basename(p) for p in glob.glob(os.path.join(BASE, "data", "weekly", "week*"))})
    suffix = "_with_solutions" if args.with_solutions else ""
    targets = [(os.path.join(DIST, f"student_kit{suffix}.zip"), None)]
    targets += [(os.path.join(DIST, f"{w}_kit{suffix}.zip"), [w]) for w in weeks]

    all_fails = []
    for zip_path, wk in targets:
        files = kit_files(wk, args.with_solutions)
        write_zip(zip_path, files, setup)
        print(f"[생성] {rel(zip_path)}  파일 {len(files) + 1}개, {human(os.path.getsize(zip_path))}")
        if args.check:
            fails = check_zip(zip_path, args.with_solutions)
            for f in fails:
                print(f"[FAIL] {rel(zip_path)}: {f}")
            if not fails:
                print(f"[PASS] {rel(zip_path)} 압축 해제 후 경로 해석")
            all_fails += fails
    if args.check:
        print(f"\n키트 검사: {len(targets)}개 zip, 실패 {len(all_fails)}건")
        sys.exit(1 if all_fails else 0)


if __name__ == "__main__":
    main()
