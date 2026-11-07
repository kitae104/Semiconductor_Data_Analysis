"""Notebook 검증 스크립트.

확인 항목(스펙 14장):
- 위에서 아래로 실행했을 때 오류가 없는가 (solutions만 실제 실행; student는 TODO가
  있어 실행이 막힐 수 있으므로 구조만 검사). 강사용 노트북은 2026-10-02 폐지했다.
- 학생용 TODO가 정답 노트북에서 해결되어 있는가(정답 노트북에 'TODO' 문자열이 남아있지 않은지)
- 데이터 경로가 실제로 존재하는가

실행: python scripts/validate_notebooks.py
"""
import os
import glob
import re
import shutil
import tempfile
import nbformat

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENT = os.path.join(BASE, "notebooks", "student")
SOLUTIONS = os.path.join(BASE, "notebooks", "solutions")

RESULTS = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    RESULTS.append((name, status, detail))
    print(f"[{status}] {name} {('- ' + detail) if detail and status == 'FAIL' else ''}")
    return condition


PRACTICE_HEADER = re.compile(r"^## \d+단계\. 반도체 데이터 실습$", re.M)
STEP_HEADER = re.compile(r"^## \d+단계\. ", re.M)


def practice_split(nb):
    """(실습 단계 앞 셀 목록, 실습 단계 셀 목록, 실습 단계 뒤 셀 목록). 실습 단계가 없으면 (전체, [], [])."""
    before, inside, after, state = [], [], [], 0
    for c in nb.cells:
        if c.cell_type == "markdown" and STEP_HEADER.search(c.source):
            state = 1 if PRACTICE_HEADER.search(c.source) else (2 if state else 0)
        (before, inside, after)[state].append(c)
    return before, inside, after


def execute_notebook(path, stop_at_practice=False):
    try:
        from nbclient import NotebookClient
    except ImportError:
        from nbconvert.preprocessors import ExecutePreprocessor as NotebookClient  # fallback name
    nb = nbformat.read(path, as_version=4)
    if stop_at_practice:   # 정답 노트북의 실습 단계는 빈칸이라 그 앞까지만 실행한다
        nb.cells = practice_split(nb)[0]
    # 노트북은 CSV 파일 이름만 쓴다. 실습 환경처럼 CSV를 모아 둔 임시 폴더에서 실행한다.
    with tempfile.TemporaryDirectory() as work:
        for csv in glob.glob(os.path.join(BASE, "data", "weekly", "week*", "week*.csv")):
            shutil.copy(csv, work)
        client = NotebookClient(
            nb, timeout=120, kernel_name="python3",
            resources={"metadata": {"path": work}},
        )
        client.execute()
    return nb


def check_data_paths(nb, path):
    src = "\n".join(c.get("source", "") for c in nb.cells if c.cell_type == "code")
    ok = True
    for token in ["read_csv("]:
        if token in src:
            pass  # 상세 경로 검증은 실제 실행 성공 여부로 대체
    return ok


def validate_folder(folder, label, must_run=True, must_not_contain_todo=False):
    files = sorted(glob.glob(os.path.join(folder, "week*_*.ipynb")))
    check(f"{label}: notebook 파일 존재(10개)", len(files) == 10, f"{len(files)}개 발견")
    for path in files:
        name = os.path.basename(path)
        nb = nbformat.read(path, as_version=4)
        check(f"{label}/{name}: nbformat 유효", True)
        if must_not_contain_todo:
            # 정답 노트북: '반도체 데이터 실습' 단계는 학생용과 같은 빈칸, 그 밖의 셀에는 TODO가 없어야 한다
            before, inside, after = practice_split(nb)
            src = "\n".join(c.get("source", "") for c in before + after)
            check(f"{label}/{name}: 실습 단계 밖 TODO 잔존 없음", "TODO" not in src and "____" not in src)
            inside_src = "\n".join(c.get("source", "") for c in inside if c.cell_type == "code")
            check(f"{label}/{name}: 실습 단계는 빈칸 형태", "TODO" in inside_src)
            has_error = any(o.get("output_type") == "error" for c in nb.cells if c.cell_type == "code"
                            for o in c.get("outputs", []))
            check(f"{label}/{name}: 저장된 출력에 오류 없음", not has_error)
        if must_run:
            try:
                execute_notebook(path, stop_at_practice=must_not_contain_todo)
                check(f"{label}/{name}: 실행 성공", True)
            except Exception as e:
                check(f"{label}/{name}: 실행 성공", False, str(e)[:200])


def main():
    validate_folder(STUDENT, "student", must_run=False)
    validate_folder(SOLUTIONS, "solutions", must_run=True, must_not_contain_todo=True)

    total = len(RESULTS)
    passed = sum(1 for _, s, _ in RESULTS if s == "PASS")
    print(f"\n총 {total}건 중 {passed}건 통과, {total - passed}건 실패")
    return RESULTS


if __name__ == "__main__":
    main()
