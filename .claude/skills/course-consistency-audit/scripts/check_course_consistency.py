"""차시 산출물 교차 정합성 검사.

`scripts/validate_datasets.py`(데이터 자체)와 `scripts/validate_notebooks.py`(노트북 실행)가
잡지 못하는 **산출물 사이의 불일치**를 잡는다. 한 차시를 고칠 때 강의 HTML·실습지·퀴즈·운영안·
노트북 3종·주차 데이터·데이터사전 중 일부만 고치고 나머지를 두면 학생이 바로 막히기 때문이다.

검사 항목
  1. 차시별 필수 산출물 8종 존재 여부
  2. quiz.json 스키마(타입별 필수 키, 보기 인덱스 범위, week 번호 일치)
  3. HTML이 참조하는 상대경로(css/js/img/a href) 대상 파일 존재
  4. HTML class 속성이 common.css/print.css 또는 같은 문서의 <style>에 정의되어 있는지
  5. 주차 내비게이션(week-nav) 링크 10개 + current 표시가 해당 차시인지
  6. HTML·노트북이 참조하는 data/weekly CSV 실제 존재
  7. 노트북 규약: student에 TODO 존재, solutions에 TODO 부재, 세 노트북의 단계 제목 정렬
  8. 주차 CSV utf-8-sig 로드 가능 + 데이터사전에 모든 열 이름 등장
  9. 표현 규칙: 인과 단정, 가짜 실시간 표현, fab.csv 센서 의미 단정

사용법
    python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py            # 전 차시
    python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week 4   # 특정 차시
    python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week 4 5 --json

종료 코드: FAIL이 하나라도 있으면 1, 아니면 0. WARN은 종료 코드에 영향을 주지 않는다.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

QUIZ_REQUIRED_KEYS = {
    "multiple_choice": {"question", "options", "answer", "explanation"},
    "chart_choice": {"question", "options", "answer", "explanation"},
    "true_false": {"question", "answer", "explanation"},
    "fill_blank": {"question", "answer"},
    "result_prediction": {"question", "answer"},
    "term_matching": {"question", "pairs"},
    "short_answer": {"question", "sample_answer"},
}

# 상관관계를 인과로 단정하는 표현. CLAUDE.md: 8~10차시는 "원인 후보"로 쓴다.
CAUSAL_PATTERNS = [
    r"원인이다", r"원인입니다", r"원인이 된다", r"때문에 불량이 발생한다",
    r"이것이\s*원인", r"원인임을\s*알\s*수\s*있",
]
# 위 표현이 "단정하면 안 된다"를 가르치려고 인용된 것이면 위반이 아니다.
# 교재 본문은 거의 항상 이 형태이므로, 주변 문맥에 반증 표현이 있으면 통과시킨다.
CAUSAL_SAFEGUARDS = [
    "단정", "아니", "없다", "없습니다", "말고", "말자", "말아", "뜻은", "≠",
    "원인 후보", "성급", "결론 내리지", "착각", "주의",
]
CAUSAL_CONTEXT = 80  # 매치 앞뒤로 살펴볼 글자 수
# 존재하지 않는 실시간 기능처럼 보이게 하는 표현(docs/design-system.md).
FAKE_LIVE_PATTERNS = [r"\bLIVE\b", r"실시간\s*모니터링", r"실시간\s*수집", r"Online\s*<", r">\s*Online\s*<"]
# fab.csv 센서의 물리적 의미 단정(CLAUDE.md 금지).
SENSOR_CLAIM_PATTERNS = [r"Sensor\d+\s*(은|는|이|가)\s*[^<\n]{0,12}(온도|압력|유량|전압|두께)"]

RESULTS: list[tuple[str, str, str, str]] = []  # (scope, name, status, detail)


def record(scope: str, name: str, status: str, detail: str = "") -> bool:
    RESULTS.append((scope, name, status, detail))
    return status == "PASS"


def check(scope: str, name: str, ok: bool, detail: str = "") -> bool:
    return record(scope, name, "PASS" if ok else "FAIL", detail)


def warn_if(scope: str, name: str, ok: bool, detail: str = "") -> bool:
    return record(scope, name, "PASS" if ok else "WARN", detail)


def read(path: str) -> str:
    with io.open(path, encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------- CSS


def defined_css_classes() -> set[str]:
    names: set[str] = set()
    for rel in ("assets/css/common.css", "assets/css/print.css"):
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            continue
        text = re.sub(r"/\*.*?\*/", " ", read(path), flags=re.S)
        names.update(re.findall(r"\.(-?[A-Za-z_][A-Za-z0-9_-]*)", text))
    return names


def inline_style_classes(html: str) -> set[str]:
    names: set[str] = set()
    for block in re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S | re.I):
        names.update(re.findall(r"\.(-?[A-Za-z_][A-Za-z0-9_-]*)", block))
    return names


def used_classes(html: str) -> set[str]:
    names: set[str] = set()
    for attr in re.findall(r'\sclass="([^"]*)"', html):
        names.update(tok for tok in attr.split() if tok)
    return names


# --------------------------------------------------------------------------- HTML


def check_html(scope: str, path: str, css_classes: set[str], week: int | None) -> None:
    rel = os.path.relpath(path, BASE).replace("\\", "/")
    if not os.path.exists(path):
        check(scope, f"{rel} 존재", False)
        return
    html = read(path)
    here = os.path.dirname(path)

    # 3. 상대경로 참조 대상 존재
    refs = re.findall(r'(?:href|src)="([^"#?][^"]*)"', html)
    missing = []
    for ref in refs:
        if ref.startswith(("http://", "https://", "mailto:", "data:", "//", "#")):
            continue
        target = os.path.normpath(os.path.join(here, ref.split("#")[0].split("?")[0]))
        if not os.path.exists(target):
            missing.append(ref)
    check(scope, f"{rel} 상대경로 참조 유효", not missing, f"없는 대상: {sorted(set(missing))[:8]}")

    # 4. class 정의 여부
    known = css_classes | inline_style_classes(html)
    unknown = sorted(c for c in used_classes(html) if c not in known)
    check(scope, f"{rel} class가 공통 CSS에 정의됨", not unknown,
          f"미정의 class: {unknown[:10]} — common.css의 기존 클래스만 쓴다(CLAUDE.md)")

    # 5. 주차 내비게이션
    if week is not None and rel.endswith("/index.html") and "week-nav" in html:
        nav = re.search(r'<nav class="week-nav">(.*?)</nav>', html, flags=re.S)
        if nav:
            links = re.findall(r'<a\s[^>]*href="\.\./week(\d{2})/index\.html"([^>]*)>', nav.group(1))
            weeks = [int(w) for w, _ in links]
            check(scope, f"{rel} week-nav 10차시 링크", weeks == list(range(1, 11)), f"실제: {weeks}")
            current = [int(w) for w, attrs in links if 'class="current"' in attrs]
            check(scope, f"{rel} week-nav current 표시", current == [week], f"실제 current: {current}")
        data_week = re.search(r'id="progressFill"\s+data-week="(\d+)"', html)
        check(scope, f"{rel} progressFill data-week 일치",
              bool(data_week) and int(data_week.group(1)) == week,
              f"실제: {data_week.group(1) if data_week else '없음'}")

    # 6. 참조 CSV 존재
    check_csv_refs(scope, rel, html)

    # 9. 표현 규칙
    check_wording(scope, rel, html, week)


def check_csv_refs(scope: str, rel: str, text: str) -> None:
    refs = set(re.findall(r'data/weekly/week\d{2}/[\w가-힣.\-]+\.csv', text.replace("\\", "/")))
    missing = [r for r in refs if not os.path.exists(os.path.join(BASE, r))]
    if refs:
        check(scope, f"{rel} 참조 주차 CSV 존재", not missing, f"없는 CSV: {sorted(missing)}")


def unguarded_causal_hits(body: str) -> list[str]:
    """인과 단정 표현 중 '단정하면 안 된다'는 반증 문맥이 없는 것만 돌려준다."""
    hits = []
    for pattern in CAUSAL_PATTERNS:
        for m in re.finditer(pattern, body):
            window = body[max(0, m.start() - CAUSAL_CONTEXT):m.end() + CAUSAL_CONTEXT]
            if not any(word in window for word in CAUSAL_SAFEGUARDS):
                hits.append(re.sub(r"\s+", " ", window).strip())
    return hits


def check_wording(scope: str, rel: str, text: str, week: int | None) -> None:
    body = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S | re.I)
    if week is not None and week >= 8:
        hits = unguarded_causal_hits(body)
        warn_if(scope, f"{rel} 인과 단정 표현 없음", not hits,
                f"발견 {len(hits)}건 — 8~10차시는 '원인'이 아니라 '원인 후보'로 쓴다(CLAUDE.md). "
                f"첫 문맥: …{hits[0][:110]}…" if hits else "")
    live = [p for p in FAKE_LIVE_PATTERNS if re.search(p, body)]
    warn_if(scope, f"{rel} 가짜 실시간 표현 없음", not live,
            f"발견: {live} — 예시 일러스트는 '예시' 라벨 + .illustration-note 필요(docs/design-system.md)")
    sensor = [p for p in SENSOR_CLAIM_PATTERNS if re.search(p, body)]
    check(scope, f"{rel} fab.csv 센서 의미 단정 없음", not sensor,
          "Sensor0~589의 물리적 의미는 확인되지 않았으므로 단정 금지(CLAUDE.md)")


# --------------------------------------------------------------------------- quiz


def check_quiz(scope: str, path: str, week: int) -> None:
    rel = os.path.relpath(path, BASE).replace("\\", "/")
    if not check(scope, f"{rel} 존재", os.path.exists(path)):
        return
    try:
        quiz = json.loads(read(path))
    except Exception as exc:  # noqa: BLE001
        check(scope, f"{rel} JSON 파싱", False, str(exc))
        return
    check(scope, f"{rel} JSON 파싱", True)
    check(scope, f"{rel} week 번호 일치", quiz.get("week") == week, f"실제: {quiz.get('week')}")
    check(scope, f"{rel} title 존재", bool(quiz.get("title")))
    questions = quiz.get("questions") or []
    check(scope, f"{rel} 문항 8개 이상", len(questions) >= 8, f"실제: {len(questions)}")

    for i, q in enumerate(questions):
        tag = f"{rel} Q{i + 1}"
        qtype = q.get("type")
        if not check(scope, f"{tag} 알려진 type", qtype in QUIZ_REQUIRED_KEYS, f"실제: {qtype}"):
            continue
        missing = QUIZ_REQUIRED_KEYS[qtype] - set(q)
        check(scope, f"{tag} 필수 키", not missing, f"누락: {sorted(missing)}")
        if qtype in ("multiple_choice", "chart_choice") and isinstance(q.get("options"), list):
            answer = q.get("answer")
            check(scope, f"{tag} answer 인덱스 범위",
                  isinstance(answer, int) and 0 <= answer < len(q["options"]),
                  f"answer={answer}, 보기 {len(q['options'])}개")
        if qtype == "true_false":
            check(scope, f"{tag} answer 불리언", isinstance(q.get("answer"), bool), f"실제: {q.get('answer')!r}")
        if qtype == "term_matching":
            pairs = q.get("pairs") or []
            check(scope, f"{tag} pairs 구조",
                  bool(pairs) and all(isinstance(p, dict) and {"term", "definition"} <= set(p) for p in pairs))


# --------------------------------------------------------------------------- notebooks


def notebook_sources(path: str) -> tuple[list[str], list[str]]:
    nb = json.loads(read(path))
    code, md = [], []
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        (code if cell.get("cell_type") == "code" else md).append(src)
    return code, md


def step_titles(md_cells: list[str]) -> list[str]:
    titles = []
    for src in md_cells:
        for line in src.splitlines():
            m = re.match(r"^##\s+(\d+단계[.．]?\s*.*)$", line.strip())
            if m:
                titles.append(re.sub(r"\s+", " ", m.group(1)).strip())
    return titles


def check_notebooks(scope: str, week: int) -> None:
    paths = {
        "student": os.path.join(BASE, "notebooks", "student", f"week{week:02d}_student.ipynb"),
        "instructor": os.path.join(BASE, "notebooks", "instructor", f"week{week:02d}_instructor.ipynb"),
        "solutions": os.path.join(BASE, "notebooks", "solutions", f"week{week:02d}_solution.ipynb"),
    }
    present = {}
    for kind, path in paths.items():
        rel = os.path.relpath(path, BASE).replace("\\", "/")
        if check(scope, f"{rel} 존재", os.path.exists(path)):
            present[kind] = path

    for kind, path in present.items():
        rel = os.path.relpath(path, BASE).replace("\\", "/")
        try:
            code, md = notebook_sources(path)
        except Exception as exc:  # noqa: BLE001
            check(scope, f"{rel} JSON 파싱", False, str(exc))
            continue
        joined = "\n".join(code)
        has_todo = "TODO" in joined or "____" in joined
        if kind == "student":
            check(scope, f"{rel} 학생용 빈칸(TODO/____) 존재", has_todo,
                  "학생용은 핵심 코드가 비어 있어야 한다(README 9장)")
        else:
            check(scope, f"{rel} 빈칸 잔존 없음", not has_todo, "완성본에 TODO/____가 남아 있다")
        check_csv_refs(scope, rel, joined)
        paths_in_code = set(re.findall(r'"(\.\./\.\./[^"]+)"', joined))
        missing = [p for p in paths_in_code if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), p)))]
        check(scope, f"{rel} 상대경로 대상 존재", not missing, f"없는 대상: {sorted(missing)[:6]}")

    # 세 노트북의 단계 제목이 모두 같아야 한다. 학생용/정답만 비교하면 강사용에서 단계가
    # 통째로 빠진 경우(그 번호를 강사 전용 내용이 차지한 경우)를 놓친다.
    if len(present) >= 2:
        titles = {kind: step_titles(notebook_sources(path)[1]) for kind, path in present.items()}
        base_kind = "student" if "student" in titles else sorted(titles)[0]
        base = titles[base_kind]
        for kind, other in sorted(titles.items()):
            if kind == base_kind:
                continue
            if len(base) != len(other):
                warn_if(scope, f"week{week:02d} 단계 수 일치 ({base_kind} vs {kind})", False,
                        f"{base_kind} {len(base)}개 vs {kind} {len(other)}개")
                continue
            diffs = [f"{i + 1}단계: {a!r} != {b!r}"
                     for i, (a, b) in enumerate(zip(base, other)) if a != b]
            warn_if(scope, f"week{week:02d} 단계 제목 일치 ({base_kind} vs {kind})", not diffs,
                    f"{len(diffs)}건 — " + " / ".join(diffs[:3]))


# --------------------------------------------------------------------------- data


def check_data(scope: str, week: int) -> None:
    folder = os.path.join(BASE, "data", "weekly", f"week{week:02d}")
    if not check(scope, f"data/weekly/week{week:02d}/ 존재", os.path.isdir(folder)):
        return
    csvs = sorted(f for f in os.listdir(folder) if f.endswith(".csv"))
    check(scope, f"week{week:02d} 주차 CSV 존재", bool(csvs))

    dict_path = os.path.join(BASE, "data", "data_dictionary", f"week{week:02d}_dictionary.md")
    rel_dict = os.path.relpath(dict_path, BASE).replace("\\", "/")
    has_dict = check(scope, f"{rel_dict} 존재", os.path.exists(dict_path))
    dict_text = read(dict_path) if has_dict else ""

    for name in csvs:
        path = os.path.join(folder, name)
        try:
            with io.open(path, encoding="utf-8-sig") as f:
                header = f.readline().strip()
        except Exception as exc:  # noqa: BLE001
            check(scope, f"{name} utf-8-sig 로드", False, str(exc))
            continue
        check(scope, f"{name} utf-8-sig 로드", True)
        columns = [c.strip().strip('"') for c in header.split(",") if c.strip()]
        check(scope, f"{name} 열 이름 존재", bool(columns))
        if has_dict:
            absent = [c for c in columns if c not in dict_text]
            warn_if(scope, f"{name} 모든 열이 데이터사전에 설명됨", not absent, f"누락: {absent}")


# --------------------------------------------------------------------------- week


EXC_RE = re.compile(r"\b([A-Z][A-Za-z]*(?:Error|Exception|Warning))\b")
FIGURE_RE = re.compile(r"(\d+(?:\.\d+)?%|\d+건)")
EXC_MSG_RE = re.compile(r"`([A-Z][A-Za-z]*(?:Error|Exception)): ([^`]{3,80})`")


def week_corpus(week: int) -> str:
    """해당 차시의 강의·실습지·노트북 3종을 한 덩어리 문자열로 모은다."""
    parts = []
    folder = os.path.join(BASE, "lectures", f"week{week:02d}")
    for name in ("index.html", "worksheet.html", "quiz.json"):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            parts.append(read(p))
    for kind, suffix in (("student", "student"), ("instructor", "instructor"), ("solutions", "solution")):
        p = os.path.join(BASE, "notebooks", kind, f"week{week:02d}_{suffix}.ipynb")
        if os.path.exists(p):
            code, md = notebook_sources(p)
            parts.extend(code)
            parts.extend(md)
    p = os.path.join(BASE, "data", "data_dictionary", f"week{week:02d}_dictionary.md")
    if os.path.exists(p):
        parts.append(read(p))
    return "\n".join(parts)


def check_guide_claims(scope: str, rel_guide: str, text: str, week: int) -> None:
    """운영안이 단독으로 주장하는 오류 이름·수치를 잡는다.

    전 차시 감사(2026-09-23)에서 차단 18건 중 12건이 운영안 단독 오류였는데 기존 검사가
    한 건도 잡지 못했다. 강사는 이 파일을 보고 시연하므로, 여기 적힌 오류 이름과 수치가
    다른 산출물 어디에도 없다면 강의 중에 실제와 다른 것을 예고하게 된다.
    
    둘 다 WARN이다. 운영안이 강의 본문에 없는 오류까지 대비해 적어두는 것은 정상적인
    역할이라, 스크립트만으로는 "운영안에만 있지만 맞는 것"과 "운영안에만 있고 틀린 것"을
    구분할 수 없다(실제로 3·9·10차시의 TypeError·KeyError·NameError는 직접 실행해보니
    전부 맞는 서술이었다). 이 검사의 목적은 판정이 아니라 **사람이 직접 실행·재계산해봐야
    할 지점을 좁혀주는 것**이다. 확인해서 맞으면 그대로 두면 된다.
    """
    corpus = week_corpus(week)

    orphan_exc = sorted({m for m in EXC_RE.findall(text) if m not in corpus})
    warn_if(scope, f"{rel_guide} 인용 오류 이름이 다른 산출물에 존재", not orphan_exc,
            f"운영안에만 있는 예외: {orphan_exc} — 실제로 그 예외가 나는지 실행해 확인할 것"
            if orphan_exc else "")

    orphan_msg = sorted({f"{a}: {b}" for a, b in EXC_MSG_RE.findall(text)
                         if f"{a}: {b}" not in corpus})
    warn_if(scope, f"{rel_guide} 인용 오류 메시지가 다른 산출물에 존재", not orphan_msg,
            f"운영안에만 있는 오류 메시지: {orphan_msg} — 그 메시지가 실제로 그대로 나오는지"
            " 실행해 확인할 것(라이브러리 버전이 올라가 더 이상 나지 않는 경우가 있다)"
            if orphan_msg else "")

    orphan_fig = sorted({m for m in FIGURE_RE.findall(text) if m not in corpus})
    warn_if(scope, f"{rel_guide} 인용 수치가 다른 산출물에 존재", not orphan_fig,
            f"운영안에만 있는 수치: {orphan_fig} — 데이터로 재계산해 확인할 것"
            if orphan_fig else "")


def check_week(week: int, css_classes: set[str]) -> None:
    scope = f"week{week:02d}"
    folder = os.path.join(BASE, "lectures", scope)
    guide = os.path.join(folder, "instructor-guide.md")
    rel_guide = os.path.relpath(guide, BASE).replace("\\", "/")

    check_html(scope, os.path.join(folder, "index.html"), css_classes, week)
    check_html(scope, os.path.join(folder, "worksheet.html"), css_classes, week)
    check_quiz(scope, os.path.join(folder, "quiz.json"), week)
    if check(scope, f"{rel_guide} 존재", os.path.exists(guide)):
        text = read(guide)
        check_csv_refs(scope, rel_guide, text)
        check_wording(scope, rel_guide, text, week)
        check_guide_claims(scope, rel_guide, text, week)
        for heading in ("수업 흐름", "예상 오개념"):
            warn_if(scope, f"{rel_guide} '{heading}' 섹션", f"## {heading}" in text or heading in text)
    check_notebooks(scope, week)
    check_data(scope, week)


def check_landing(css_classes: set[str]) -> None:
    check_html("site", os.path.join(BASE, "index.html"), css_classes, None)
    for week in range(1, 11):
        link = f"lectures/week{week:02d}/index.html"
        warn_if("site", f"index.html에 {week}차시 링크", link in read(os.path.join(BASE, "index.html")))


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description="차시 산출물 교차 정합성 검사")
    parser.add_argument("--week", "-w", nargs="*", type=int, help="검사할 차시 번호(생략 시 1~10 전체)")
    parser.add_argument("--json", action="store_true", help="결과를 JSON으로 출력")
    parser.add_argument("--quiet", "-q", action="store_true", help="FAIL/WARN만 출력")
    args = parser.parse_args()

    weeks = args.week if args.week else list(range(1, 11))
    css_classes = defined_css_classes()
    if not css_classes:
        record("site", "assets/css/common.css 로드", "FAIL", "공통 CSS를 찾지 못해 class 검사를 건너뛴다")

    check_landing(css_classes)
    for week in weeks:
        check_week(week, css_classes)

    fails = [r for r in RESULTS if r[2] == "FAIL"]
    warns = [r for r in RESULTS if r[2] == "WARN"]

    if args.json:
        print(json.dumps(
            {"total": len(RESULTS), "fail": len(fails), "warn": len(warns),
             "results": [{"scope": s, "check": n, "status": st, "detail": d} for s, n, st, d in RESULTS]},
            ensure_ascii=False, indent=2))
    else:
        for scope, name, status, detail in RESULTS:
            if args.quiet and status == "PASS":
                continue
            suffix = f" — {detail}" if detail and status != "PASS" else ""
            print(f"[{status}] ({scope}) {name}{suffix}")
        print(f"\n검사 {len(RESULTS)}건 · PASS {len(RESULTS) - len(fails) - len(warns)} · "
              f"WARN {len(warns)} · FAIL {len(fails)}")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
