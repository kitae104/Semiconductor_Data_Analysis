---
name: course-consistency-audit
description: 차시 산출물 8종(강의 HTML·실습지·퀴즈·운영안·노트북 3종·데이터+데이터사전)이 서로 어긋나지 않는지 검증할 때 반드시 사용한다. 콘텐츠·노트북·데이터를 수정한 뒤 회귀 확인, 전 차시 품질 점검, "검증해줘", "확인해줘", "점검해줘", "다 맞나 봐줘", validate 스크립트 실패 조사, 커밋 전 최종 확인에 사용할 것. 번들된 교차 정합성 검사 스크립트와 자동 검사가 못 잡는 수동 대조 항목이 들어 있다. consistency-qa 에이전트의 기본 스킬.
---

# 차시 산출물 정합성 검증

한 차시는 8종 산출물로 이뤄지고 서로를 참조한다. **일부만 고치고 나머지를 두면 학생이 수업
중에 막힌다.** 이 스킬은 그 어긋남을 찾는다.

## 실행하지 않고 통과라고 쓰지 않는다

이 스킬의 규칙은 하나로 요약된다 — **모든 판정은 실제 명령의 실제 출력에 근거한다.**
출력을 보고서에 그대로 붙여 넣는다. 붙여 넣을 출력이 없으면 그 항목은 검증되지 않은 것이다.

## 세 가지를 모두 돌린다

```bash
# 1. 데이터 검증 — 열 구조, 값 범위, 의도된 패턴, 재현성 해시
python scripts/validate_datasets.py

# 2. 노트북 실행 검증 — nbclient로 실제 실행 (kernel_name="python3")
python scripts/validate_notebooks.py

# 3. 교차 정합성 검사 — 산출물 사이의 경계면
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week {N}
```

Windows에서는 `python3`가 아니라 **`python`**을 쓴다(CLAUDE.md).
하나라도 건너뛰었으면 **그 사실을 보고서에 명시한다** — 조용히 빼면 통과로 오해된다.

## 교차 정합성 검사 스크립트

번들 경로: `.claude/skills/course-consistency-audit/scripts/check_course_consistency.py`. 기존 두 검증 스크립트가 못 보는 **산출물 사이**를 본다.

```bash
# 전 차시
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py

# 특정 차시 (여러 개 가능)
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week 4 5

# FAIL/WARN만
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --quiet

# JSON (다른 도구로 넘길 때)
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --json
```

종료 코드: **FAIL이 하나라도 있으면 1**, 아니면 0. WARN은 0이다.

### 잡는 것

| # | 항목 |
|---|---|
| 1 | 차시별 필수 산출물 8종 존재 |
| 2 | `quiz.json` 스키마 — 타입별 필수 키, `answer` 인덱스 범위, `week` 번호 일치, 문항 수 |
| 3 | HTML이 참조하는 상대경로(css/js/img/href) 대상 파일 존재 |
| 4 | HTML `class`가 `common.css`/`print.css` 또는 같은 문서 `<style>`에 정의됨 |
| 5 | `week-nav` 10차시 링크 + `current` 표시 + `data-week` 일치 |
| 6 | HTML·노트북이 참조하는 `data/weekly` CSV 실제 존재 |
| 7 | 노트북 규약 — 학생용에 빈칸 존재, 정답·강사본에 빈칸 부재, 단계 제목 정렬 |
| 8 | 주차 CSV `utf-8-sig` 로드 + 데이터사전에 모든 열 등장 |
| 9 | 표현 규칙 — 인과 단정(부정 문맥 제외), 가짜 실시간, 센서 의미 단정 |

### FAIL과 WARN

| 등급 | 의미 | 처리 |
|---|---|---|
| **FAIL** | 명백히 깨진 것 — 없는 파일, 잘못된 인덱스, 미정의 class | 반드시 고친다 |
| **WARN** | 문맥 판정이 필요한 것 — 데이터사전 열 누락, 단계 제목 차이, 표현 경고 | 판정 후 남길 수 있다 |

**표현 관련 WARN은 domain-reviewer에게 판정을 넘긴다.** 스크립트는 앞뒤 80자에 반증 표현이
있는지로 부정 문맥을 걸러내지만, 경계가 모호한 경우는 사람이 읽어야 한다.

WARN을 남기기로 했으면 **남긴 이유를 리포트에 적는다.** 이유 없이 남은 WARN은 다음 세션에서
다시 조사된다.

## 자동 검사가 못 잡는 것 — 손으로 읽는다

스크립트는 **형태**를 본다. **의미**는 못 본다. 아래 네 경계면은 반드시 사람이 대조한다.

### 1. 강의 코드 ↔ 노트북 코드

학생은 강의 화면을 보며 노트북을 친다. 둘이 다르면 수업이 멈춘다. **글자 단위로** 같아야 한다.

```bash
# 강의 자료의 코드 블록 추출
python - <<'PY'
import re, io
html = io.open('lectures/week04/index.html', encoding='utf-8').read()
for i, m in enumerate(re.findall(r'<pre><code>(.*?)</code></pre>', html, re.S), 1):
    code = m.replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
    print(f'--- 강의 블록 {i} ---'); print(code)
PY

# 노트북 코드 셀 추출
python - <<'PY'
import json, io
nb = json.load(io.open('notebooks/solutions/week04_solution.ipynb', encoding='utf-8'))
for i, c in enumerate([c for c in nb['cells'] if c['cell_type']=='code'], 1):
    print(f'--- 노트북 셀 {i} ---'); print(''.join(c['source']))
PY
```

흔한 불일치: 변수명, `encoding="utf-8-sig"` 누락, 파일 경로, 출력 print 유무.

### 2. 강의 수치 ↔ 운영안 "핵심 수치" ↔ 노트북 실제 출력

강사가 수업 중 읽는 숫자다. 틀리면 교실에서 바로 드러난다.

```bash
python -c "import pandas as pd; df=pd.read_csv('data/weekly/week04/week04_process_filtering.csv', encoding='utf-8-sig'); print(df.shape); print(df['설비번호'].value_counts()); print(df.groupby('설비번호')['합격여부'].apply(lambda s:(s==-1).sum()))"
grep -n -A8 "핵심 수치" lectures/week04/instructor-guide.md
```

데이터사전의 "의도적으로 포함된 패턴"에 적힌 실제 수치도 같이 본다.

### 3. 퀴즈 ↔ 강의에서 실제로 가르친 내용

**가장 흔한 지적이다.** 퀴즈를 늘릴 때 "이 정도는 알겠지" 싶은 것이 들어간다.
각 문항이 묻는 것이 강의 본문에 실제로 나오는지 확인한다.

```bash
python - <<'PY'
import json, io, re
quiz = json.load(io.open('lectures/week04/quiz.json', encoding='utf-8'))
html = re.sub(r'<[^>]+>', ' ', io.open('lectures/week04/index.html', encoding='utf-8').read())
for i, q in enumerate(quiz['questions'], 1):
    print(f"Q{i} [{q['type']}] {q['question'][:70]}")
PY
```

출력된 문항을 하나씩 강의 본문과 대조한다. 정답이 실제로 맞는지도 여기서 본다 —
스크립트는 인덱스 범위만 보지 정답의 참/거짓은 모른다.

### 4. 실습지 문제 ↔ 학생용 노트북 TODO

실습지는 "무엇을 해야 하는지", 노트북은 "어디에 쓰는지"다. 둘이 어긋나면 학생이 둘 다 못 푼다.

```bash
grep -oE '<h2>[^<]+</h2>' lectures/week04/worksheet.html
python -c "import json,io; nb=json.load(io.open('notebooks/student/week04_student.ipynb',encoding='utf-8')); [print(''.join(c['source'])) for c in nb['cells'] if c['cell_type']=='code' and 'TODO' in ''.join(c['source'])]"
```

## 점진적으로 검증한다

전부 끝난 뒤 한 번 도는 방식은 **어디서 깨졌는지 추적을 어렵게 한다.** 각 산출물이 완성될
때마다 그 부분을 검증한다.

| 완성된 것 | 즉시 돌릴 것 |
|---|---|
| 데이터 | `validate_datasets.py` |
| 노트북 | `validate_notebooks.py` + 경계면 1 |
| 강의 HTML / 실습지 | `check_course_consistency.py --week N` + 경계면 1, 4 |
| 퀴즈 | `check_course_consistency.py --week N` + 경계면 3 |
| 운영안 | 경계면 2 |

## 수정 후 재검증

**고친 부분만 보지 않고 해당 차시 전체를 다시 돌린다.** 한 곳을 고치다 다른 곳을 깨는 것이
이 프로젝트에서 가장 흔한 회귀다. 디자인 변경이었다면 전 차시를 돌린다.

이전 실행 출력을 재사용해 "여전히 통과"라고 쓰지 않는다.

## 실패 판별

| 증상 | 분류 |
|---|---|
| `ModuleNotFoundError`, `NoSuchKernel` | **환경 문제** — `pip install -r requirements.txt`, `python -m ipykernel install --user --name python3` |
| `python3` 실행 안 됨 | **환경 문제** — Windows에서는 `python`을 쓴다 |
| `KeyError`, `FileNotFoundError`, 값 범위 FAIL | **콘텐츠 문제** — 담당자에게 넘긴다 |
| 미정의 class, 깨진 참조 | **콘텐츠 문제** |

환경 문제를 콘텐츠 문제로 보고하면 엉뚱한 곳을 고치게 된다. 반대도 마찬가지다.

**이번 변경 때문인지 기존 문제인지**는 `git diff --name-only`로 판별한다. 기존 문제라면
그 사실을 적고, 고칠지는 사용자에게 묻는다.

## 고치지 않는다

발견하고 담당자에게 넘긴다 — 콘텐츠는 content-writer, 노트북·데이터는 notebook-engineer,
CSS·이미지·랜딩은 design-steward, 표현 판정은 domain-reviewer.
QA가 직접 고치면 그 수정은 아무도 검증하지 않는다.
