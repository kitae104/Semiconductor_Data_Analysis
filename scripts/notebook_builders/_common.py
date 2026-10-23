"""학생용·정답 노트북 2종을 하나의 원본 정의에서 만드는 공통 도우미(nbformat + nbclient).

노트북 JSON을 손으로 고치지 않는다. 차시마다 `scripts/notebook_builders/weekXX.py`에 셀을 한 번만 적고,
이 모듈이 두 노트북을 함께 만든다.

- 정답본 = 학생용의 빈칸을 채운 것. code(정답, 학생용)로 한 셀에 두 버전을 같이 적는다.
- 맨 위 마크다운 셀에 제목과 "막혔을 때" 안내가 자동으로 들어간다.
- 저장 뒤 자체 점검: 정답에 TODO/____ 없음, 학생용에 빈칸 1개 이상, `## N단계.` 제목이 두 노트북에서 같고
  1부터 차례대로, read_csv에 encoding="utf-8-sig", ../../data 경로가 실제 파일을 가리킴.
- 정답본은 nbclient로 실행해(작업 폴더 notebooks/solutions) 출력을 저장한다. 실행 시각 메타데이터는 남기지 않고,
  셀 id를 고정해 같은 정의면 같은 파일이 나온다.

차시 스크립트 예(scripts/notebook_builders/week05.py):

    from _common import NotebookPair, md, code, step, look_up

    nb = NotebookPair("week05", "5차시 실습 — 결측값·이상값 정리")
    nb.add(step(1, "데이터 읽기"))
    nb.add(code('import pandas as pd\\n'
                'df = pd.read_csv("../../data/weekly/week05/week05_easy_class_records.csv", encoding="utf-8-sig")\\n'
                'df.head()'))
    nb.add(look_up("평균과 중앙값 차이"))
    nb.add(step(2, "반도체 데이터 실습 — 결측값 세기"))
    nb.add(md("### 문제 1 — 열마다 빈칸이 몇 개인지 세어 보세요."))
    nb.add(code("print(df.isna().sum())",
                "# TODO: 열마다 빈칸 개수를 세어 출력하세요.\\nprint(df.isna().____())"))

    if __name__ == "__main__":
        nb.cli()      # python scripts/notebook_builders/week05.py [--no-execute]
"""
import argparse
import hashlib
import os
import re
import sys

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOTEBOOKS = os.path.join(BASE, "notebooks")

BLANK = "____"
STEP_RE = re.compile(r"^## (\d+)단계\. (.+)$", re.M)
DATA_REF_RE = re.compile(r"\.\./\.\./data/[^\"'\\\s)]+")
READ_CSV_RE = re.compile(r"read_csv\(([^)]*)\)")

STUCK_CELL = """## 막혔을 때

- 결과가 이상하거나 오류가 계속 나면 메뉴에서 **Kernel → Restart Kernel and Run All Cells…**(옛 화면은 Kernel → Restart & Run All)를 눌러 위에서부터 다시 실행하세요. 학생용은 아직 채우지 않은 **첫 빈칸에서 멈춥니다. 정상입니다.** 그 빈칸을 채우고 그 셀부터 Shift + Enter로 이어 가세요.
- 밑줄로 된 빈칸 표시는 채울 자리만 알려 줍니다. 밑줄 개수와 상관없이 밑줄을 모두 지우고 필요한 만큼(글자 하나든 이름 전체든) 씁니다.
- 셀을 지웠거나 망가뜨렸다면 **Edit → Undo**(셀 바깥을 누른 뒤 `z` 키)로 되돌립니다. 안 되면 실습 키트에서 이 노트북 파일만 다시 꺼내 쓰세요(폴더 구조는 그대로 둡니다).
- 빨간 오류 메시지는 **마지막 줄**부터 읽으세요. 오류 이름(`NameError`, `KeyError` …)과 문제가 된 이름이 거기 있습니다."""

# 그래프가 있는 차시의 첫 그래프 셀에 넣는 두 줄(강의 코드와 같게)
MPL_KOREAN = 'plt.rcParams["font.family"] = "Malgun Gothic"\nplt.rcParams["axes.unicode_minus"] = False'


def _show(path):
    try:
        return os.path.relpath(path, BASE)
    except ValueError:  # 다른 드라이브(테스트용 out_root)
        return path


class Cell:
    """한 셀의 두 버전. student가 None이면 두 노트북에 같은 내용이 들어간다."""

    def __init__(self, kind, solution, student=None):
        self.kind = kind
        self.solution = solution.strip("\n")
        self.student = None if student is None else student.strip("\n")

    def text(self, variant):
        if variant == "student" and self.student is not None:
            return self.student
        return self.solution


def md(text, student=None):
    """마크다운 셀. 학생용 문구가 다르면 student에 적는다(예: 학생용에만 힌트 bullet)."""
    return Cell("markdown", text, student)


def code(solution, student=None):
    """코드 셀. student를 주면 학생용에는 그 코드(# TODO: 줄 + ____ 빈칸)가 들어간다."""
    return Cell("code", solution, student)


def step(n, title):
    """`## N단계. 제목` — 두 노트북에서 같아야 하는 뼈대."""
    return md(f"## {n}단계. {title}")


def look_up(query):
    """찾아보기 한 줄(선택). 강의의 찾아보기 상자와 같은 지점에 둔다. query = 강의 상자의 검색어."""
    return md(f'> 찾아보기: "{query}" — 강의 자료의 ChatGPT 질문을 써 보세요.')


class NotebookPair:
    def __init__(self, week, title, out_root=NOTEBOOKS):
        if not re.fullmatch(r"week\d{2}", week):
            raise ValueError(f"week는 'week05' 형식이어야 합니다: {week!r}")
        self.week = week
        self.title = title
        self.out_root = out_root
        self.cells = []

    def add(self, *cells):
        self.cells.extend(cells)
        return self

    # -- 만들기 ---------------------------------------------------------------
    def paths(self):
        return {
            "student": os.path.join(self.out_root, "student", f"{self.week}_student.ipynb"),
            "solution": os.path.join(self.out_root, "solutions", f"{self.week}_solution.ipynb"),
        }

    def _cell_id(self, i):
        return hashlib.md5(f"{self.week}:{i}".encode("utf-8")).hexdigest()[:8]

    def notebook(self, variant):
        # 첫 마크다운 셀 = 제목 + "막혔을 때"(스펙 0-5: 맨 위 셀이 막혔을 때 안내)
        title = f"# {self.title}" + (" (정답)" if variant == "solution" else "")
        cells = [md(title + "\n\n" + STUCK_CELL)] + self.cells
        nb = new_notebook()
        nb.metadata = {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        }
        for i, cell in enumerate(cells):
            maker = new_markdown_cell if cell.kind == "markdown" else new_code_cell
            nb_cell = maker(cell.text(variant))
            nb_cell["id"] = self._cell_id(i)
            nb.cells.append(nb_cell)
        return nb

    # -- 자체 점검 -------------------------------------------------------------
    def self_check(self, student_nb, solution_nb):
        """규칙 위반 목록을 돌려준다(빈 목록이면 통과)."""
        errors, warnings = [], []
        sol_text = "\n".join(c.source for c in solution_nb.cells)
        stu_code = [c.source for c in student_nb.cells if c.cell_type == "code"]
        for word in ("TODO", BLANK):
            if word in sol_text:
                errors.append(f"정답 노트북에 '{word}'가 남아 있음")
        if not any(BLANK in s for s in stu_code):
            errors.append("학생용 노트북에 빈칸(____)이 하나도 없음")
        for cell in self.cells:
            if cell.kind == "code" and cell.student is not None:
                if BLANK not in cell.student and "# TODO" not in cell.student:
                    errors.append(f"학생용 버전이 따로 있는데 빈칸/TODO가 없는 셀: {cell.student[:40]!r}")
                if cell.student.count(BLANK) > 2:
                    warnings.append(f"한 셀에 빈칸이 3개 이상: {cell.student[:40]!r}")

        def steps(nb):
            return [m.groups() for c in nb.cells if c.cell_type == "markdown" for m in STEP_RE.finditer(c.source)]
        stu_steps, sol_steps = steps(student_nb), steps(solution_nb)
        if stu_steps != sol_steps:
            errors.append(f"단계 제목이 다름: 학생용 {stu_steps} / 정답 {sol_steps}")
        numbers = [int(n) for n, _ in sol_steps]
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"단계 번호가 1부터 차례대로가 아님: {numbers}")

        for variant, nb in (("student", student_nb), ("solution", solution_nb)):
            folder = os.path.join(self.out_root, "student" if variant == "student" else "solutions")
            for c in nb.cells:
                if c.cell_type != "code":
                    continue
                for args in READ_CSV_RE.findall(c.source):
                    if "utf-8-sig" not in args:
                        errors.append(f"{variant}: read_csv에 encoding=\"utf-8-sig\" 없음: read_csv({args})")
                for ref in DATA_REF_RE.findall(c.source):
                    if not os.path.exists(os.path.normpath(os.path.join(folder, ref))):
                        errors.append(f"{variant}: 데이터 경로가 없음: {ref}")
        return errors, warnings

    # -- 실행 ------------------------------------------------------------------
    def execute_solution(self, nb, path):
        from nbclient import NotebookClient
        client = NotebookClient(nb, timeout=300, kernel_name="python3", record_timing=False,
                                resources={"metadata": {"path": os.path.dirname(path)}})
        client.execute()
        return nb

    def build(self, execute=True):
        paths = self.paths()
        student_nb, solution_nb = self.notebook("student"), self.notebook("solution")
        errors, warnings = self.self_check(student_nb, solution_nb)
        for w in warnings:
            print(f"[WARN] {self.week}: {w}")
        if errors:
            for e in errors:
                print(f"[FAIL] {self.week}: {e}")
            raise SystemExit(f"{self.week}: 자체 점검 실패 {len(errors)}건 — 노트북을 쓰지 않았습니다.")

        for variant, nb in (("student", student_nb), ("solution", solution_nb)):
            os.makedirs(os.path.dirname(paths[variant]), exist_ok=True)
            nbformat.write(nb, paths[variant])
            print(f"[생성] {_show(paths[variant])}")
        if execute:
            try:
                self.execute_solution(solution_nb, paths["solution"])
            except Exception as e:  # noqa: BLE001
                print(f"[FAIL] {self.week}: 정답 노트북 실행 오류 — 출력 없는 정답본만 저장됨\n{e}")
                raise SystemExit(1)
            nbformat.write(solution_nb, paths["solution"])
            print(f"[실행] {_show(paths['solution'])} 출력 저장")
        n_steps = len(STEP_RE.findall("\n".join(c.source for c in solution_nb.cells if c.cell_type == "markdown")))
        n_blanks = sum(c.source.count(BLANK) for c in student_nb.cells if c.cell_type == "code")
        print(f"[PASS] {self.week}: 자체 점검 통과 (단계 {n_steps}개, 학생용 빈칸 {n_blanks}개)")
        return paths

    def cli(self):
        parser = argparse.ArgumentParser(description=f"{self.week} 학생용·정답 노트북 생성")
        parser.add_argument("--no-execute", action="store_true", help="정답 노트북을 실행하지 않고 저장만")
        args = parser.parse_args()
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8")
        self.build(execute=not args.no_execute)
