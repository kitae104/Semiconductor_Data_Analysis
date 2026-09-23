# 작업 유형별 상세 워크플로우

`SKILL.md`의 Phase 1에서 유형 B(전 차시 감사) 또는 C(디자인 개편)로 분류됐을 때 읽는다.
유형 A(차시 개선)·D(차시 신설)는 `SKILL.md`의 Phase 2~5를 그대로 따른다.

## 목차

- [유형 B. 전 차시 품질 감사](#유형-b-전-차시-품질-감사)
- [유형 C. 사이트·디자인 개편](#유형-c-사이트디자인-개편)
- [유형 D. 차시 신설 시 추가 고려](#유형-d-차시-신설-시-추가-고려)
- [_workspace 파일 규약](#_workspace-파일-규약)

---

## 유형 B. 전 차시 품질 감사

**실행 모드: 서브 에이전트 팬아웃 → 리드 종합.** 10개 차시는 서로 독립이라 팀 통신이 필요 없다.
10명이 서로 메시지를 주고받으면 조율 비용만 늘고 결과는 나아지지 않는다.

### B-1. 기계 검사 먼저

사람 눈을 쓰기 전에 스크립트로 잡히는 것부터 걷어낸다. 감사 에이전트가 이미 잡힌 문제를
다시 찾느라 시간을 쓰지 않게 한다.

```bash
python scripts/validate_datasets.py
python scripts/validate_notebooks.py
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --quiet
```

결과를 `_workspace/00_machine_audit.md`에 저장하고, 차시별로 쪼개 각 감사 에이전트의 입력으로 준다.

### B-2. 차시별 팬아웃

10개를 한 번에 띄우지 말고 **3~4개씩 나눠 보낸다.** 한 번에 전부 띄우면 결과를 종합할 때
맥락이 섞이고, 중간에 기준을 고칠 기회를 잃는다. 첫 묶음 결과를 보고 감사 기준이 적절한지
점검한 뒤 나머지를 보낸다.

```
Agent(subagent_type: "general-purpose", model: "opus", run_in_background: true,
      prompt: ".claude/agents/domain-reviewer.md 를 읽고 그 역할로 수행하라.
               .claude/skills/semiconductor-content-guard/SKILL.md 와
               .claude/skills/curriculum-spec/SKILL.md 를 먼저 읽어라.
               감사 대상: week{XX} 산출물 8종 전부.
               기계 검사 결과(이미 확인된 항목이므로 중복 보고하지 말 것):
               {해당 차시의 00_machine_audit.md 발췌}
               산출물: _workspace/audit_week{XX}.md — domain-reviewer 출력 형식을 따르되
               아래 감사 축을 모두 다룰 것.")
```

**감사 축 5가지** (각 에이전트에게 그대로 전달한다):

| 축 | 확인할 것 |
|---|---|
| 도메인 정확성 | 반도체 용어가 맞게 쓰였는가. `docs/glossary.md`와 어긋나지 않는가 |
| 표현 안전성 | 인과 단정, 가짜 실시간, 센서 의미 단정, 가상 데이터 고지 누락 |
| 교육 설계 | 선수 지식이 실제로 앞 차시에서 다뤄졌는가. 새 개념이 3~5개를 넘지 않는가 |
| 산출물 정합 | 강의 코드 ↔ 노트북 코드, 강의 수치 ↔ 운영안 수치, 퀴즈 ↔ 가르친 내용, 실습지 ↔ 학생용 TODO |
| 접근성 | 비전공자가 막힐 지점. 설명 없이 등장하는 용어, "간단히/당연히/그냥" 같은 표현 |

### B-3. 종합

리드가 `_workspace/audit_summary.md`로 묶는다. 차시별로 나열하지 말고 **패턴으로 묶는다** —
"3·5·7차시에서 데이터사전에 열 설명 누락"이 "3차시 …, 5차시 …, 7차시 …"보다 고치기 쉽다.

```markdown
# 전 차시 품질 감사 요약

## 한눈에 보기
| 차시 | 차단 | 수정 권장 | 제안 |
|---|---|---|---|

## 반복되는 패턴 (우선 처리 대상)
| # | 패턴 | 해당 차시 | 근본 원인 | 권장 조치 |
|---|---|---|---|---|

## 차시별 개별 항목
(차단 → 수정 권장 → 제안 순)

## 권장 처리 순서
(차단 항목부터. 각각 유형 A 워크플로우로 처리)
```

### B-4. 수정으로 넘기기

감사는 **발견까지**다. 발견한 것을 바로 고치기 시작하면 감사 범위가 무너지고, 고친 것이
검증되지 않는다. 요약을 사용자에게 보고하고 **어느 항목을 고칠지 확인받은 뒤**, 각 항목을
유형 A 워크플로우(스펙 → 제작 → 검증)로 처리한다.

---

## 유형 C. 사이트·디자인 개편

**실행 모드: 에이전트 팀** (design-steward + consistency-qa, 본문 글이 바뀌면 content-writer).

### C-1. 범위와 기준 확정

디자인 요청은 "더 모던하게" 같은 형태로 오기 쉽다. 추측으로 전면 개편하지 말고 다음을 먼저 정한다.

- **참조가 있는가**: `stitch-reference/`의 목업, 사용자가 준 이미지, 기존 차시 중 마음에 드는 것
- **불만 지점이 무엇인가**: 특정 컴포넌트인가, 전체 인상인가, 인쇄 결과인가
- **적용 범위**: 랜딩만인가, 전 차시인가, 실습지 포함인가

없으면 **작은 범위에서 2안을 만들어 보여주고 선택받는다.** 10개 차시에 롤아웃한 뒤 방향이
틀렸음을 알게 되는 것이 최악이다.

### C-2. 시범 적용 → 검토 → 롤아웃

```
1. design-steward가 랜딩 또는 대표 차시 1개에 적용
2. 사용자에게 보여주고 방향 확인  ← 반드시 여기서 멈춘다
3. 승인되면 전 차시(강의 10 + 실습지 10)에 롤아웃
4. consistency-qa가 전 차시 재검증
```

3단계를 건너뛰면 사이트가 두 가지 모습으로 갈라진다. 시범 적용 상태로 작업이 끝나면
그 사실을 반드시 보고한다.

### C-3. 검증

디자인 변경은 조용히 깨진다. 아래를 모두 확인한다.

```bash
# 미정의 class, 깨진 상대경로 참조를 전 차시에서 확인
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --quiet
```

| 확인 항목 | 방법 |
|---|---|
| 미정의 class / 깨진 참조 | 위 스크립트 (FAIL로 잡힌다) |
| 인쇄 레이아웃 | `print.css` 검토. 실습지는 실제로 인쇄해 쓴다 |
| 서버 없이 열리는가 | `index.html`을 파일로 직접 열어 확인 — 모든 자산이 상대경로여야 한다 |
| 대비(WCAG AA) | 배경 이미지 위 텍스트 |
| 좁은 화면 | `common.css`의 기존 미디어 쿼리(860px 등) 경계에서 깨지지 않는지 |

### C-4. 문서 갱신

`docs/design-system.md`는 디자인의 계약서다. 토큰이나 컴포넌트를 추가·변경했으면 여기를 갱신하지
않은 채 끝내지 않는다 — 다음 세션의 content-writer가 무엇을 써도 되는지 알 수 없게 된다.

---

## 유형 D. 차시 신설 시 추가 고려

유형 A와 같은 흐름이되 다음이 추가된다. 빠뜨리면 새 차시가 사이트에서 고립된다.

| 항목 | 내용 |
|---|---|
| 커리큘럼 문서 | `docs/curriculum.md`에 차시 절 추가, `README.md` 목차 표 갱신 |
| 주차 내비게이션 | 전 차시 `week-nav`에 링크 추가 (10차시 고정이 아니게 된다 — 검사 스크립트의 `range(1, 11)`도 함께 고친다) |
| 진행률 | `common.js`의 `/ 10` 분모 |
| 랜딩 | `index.html`의 차시 카드 |
| 데이터 | `scripts/generate_weekly_data.py`에 시드 고정 생성 로직, `validate_datasets.py`에 검증 항목 |
| 검사 스크립트 | `check_course_consistency.py`의 주차 범위 |

`fab.csv` 기반 선택 심화 부록을 만드는 경우, 핵심 10차시 경로와 **분리**하고
`Sensor0~Sensor589`의 물리적 의미를 단정하지 않는다(CLAUDE.md).

---

## `_workspace` 파일 규약

파일명은 `{순번}_{에이전트}_{산출물}.md`다. 순번이 있어야 나중에 읽을 때 흐름이 보인다.

| 파일 | 작성자 |
|---|---|
| `00_machine_audit.md` | 리드(기계 검사 결과) |
| `01_architect_spec.md` | curriculum-architect |
| `02_writer_report.md` | content-writer |
| `03_notebook_report.md` | notebook-engineer |
| `04_design_report.md` | design-steward |
| `05_domain_review.md` | domain-reviewer |
| `06_qa_report.md` | consistency-qa |
| `audit_week{XX}.md`, `audit_summary.md` | 감사 팬아웃(유형 B) |

`_workspace/`는 사후 검증·감사 추적을 위해 **보존한다.** 새 작업을 시작할 때는 지우지 말고
`_workspace_prev/`로 옮긴다. 저장소에 커밋할 필요는 없으므로 `.gitignore`에 추가해도 된다.
