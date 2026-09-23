---
name: course-build
description: 반도체 데이터 분석 10차시 강의 콘텐츠를 만들고 고치고 점검하는 전체 워크플로우를 조율한다. 차시(week01~week10) 내용 개선·보완·수정, 차시 신설·부록 추가, 강의 HTML·실습지·퀴즈·강사 운영안 작성, 노트북 3종과 주차 데이터 갱신, 노트북 실행 오류 수정, 전 차시 품질 감사, 랜딩/디자인 개편, "N차시 고쳐줘", "설명 보강해줘", "예제 추가해줘", "퀴즈 늘려줘", "노트북이 안 돌아가", "오탈자·오류 찾아줘", "전체 점검해줘", "디자인 바꿔줘", "11차시 추가" 같은 요청에 반드시 이 스킬을 사용할 것. 후속 요청("다시 실행", "재실행", "업데이트", "수정", "보완", "N차시만 다시", "이전 결과 기반으로", "QA에서 지적된 것 고쳐줘")에도 사용한다. 차시 산출물과 무관한 일(단순 사실 질문, git 작업, requirements.txt 같은 환경 설정, README·CLAUDE.md 단독 수정, 파이썬 문법 질문)은 직접 처리한다.
---

# 강의 콘텐츠 제작 오케스트레이터

이 저장소는 프로그래밍 경험이 거의 없는 일반인을 위한 「반도체 및 반도체 공정 데이터 분석
10차시 과정」이다. 한 차시는 **8종 산출물**로 이뤄지고, 이들은 서로를 참조한다.

| # | 산출물 | 경로 | 담당 |
|---|---|---|---|
| 1 | 강의 자료 | `lectures/weekXX/index.html` | content-writer |
| 2 | 실습지 | `lectures/weekXX/worksheet.html` | content-writer |
| 3 | 퀴즈 | `lectures/weekXX/quiz.json` | content-writer |
| 4 | 강사 운영안 | `lectures/weekXX/instructor-guide.md` | content-writer |
| 5 | 학생용 노트북 | `notebooks/student/weekXX_student.ipynb` | notebook-engineer |
| 6 | 강사용 노트북 | `notebooks/instructor/weekXX_instructor.ipynb` | notebook-engineer |
| 7 | 정답 노트북 | `notebooks/solutions/weekXX_solution.ipynb` | notebook-engineer |
| 8 | 주차 데이터 + 데이터사전 | `data/weekly/weekXX/`, `data/data_dictionary/weekXX_dictionary.md` | notebook-engineer |

**이 워크플로우가 존재하는 이유**: 한 곳만 고치면 반드시 다른 곳이 어긋난다. 강의 자료의 코드를
고치고 노트북을 두면 학생이 수업 중에 막히고, 퀴즈를 두면 정답이 틀어진다. 8종을 함께 움직이고
실제로 검증하는 것이 이 하네스의 목적이다.

## 실행 모드: 하이브리드

| Phase | 모드 | 이유 |
|---|---|---|
| Phase 2 (스펙) | 단일 서브 에이전트 | 스펙은 한 사람이 일관되게 써야 한다 |
| Phase 3 (제작) | **에이전트 팀** | 작성자·엔지니어가 코드/수치를 실시간으로 맞춰야 한다 |
| Phase 4 (검증) | **에이전트 팀** (제작 팀 유지) | 지적 → 수정 → 재검증이 왕복한다 |
| 전 차시 감사 | 서브 에이전트 팬아웃 | 10차시가 서로 독립이다. 조율 오버헤드가 순손해다 |

모든 `Agent` 호출에 **`model: "opus"`** 를 명시한다.

## Phase 0. 컨텍스트 확인

작업을 시작하기 전에 `_workspace/`를 확인해 실행 모드를 정한다.

| 상황 | 모드 | 행동 |
|---|---|---|
| `_workspace/` 없음 | **초기 실행** | Phase 1부터 전체 진행 |
| `_workspace/` 있음 + 부분 수정 요청 | **부분 재실행** | 해당 에이전트만 재호출. 기존 보고서를 입력으로 준다 |
| `_workspace/` 있음 + 새 차시/새 요청 | **새 실행** | 기존 `_workspace/`를 `_workspace_prev/`로 옮기고 새로 시작 |
| QA FAIL 후속 요청 | **부분 재실행** | `_workspace/06_qa_report.md`의 FAIL 목록을 담당자에게 배분 |

```bash
ls _workspace/ 2>/dev/null || echo "초기 실행"
git status --porcelain          # 작업 중이던 변경이 남아 있는지 확인
```

`_workspace/`는 감사 추적용으로 **보존한다**(삭제하지 않는다). `.gitignore` 확인 후 필요하면 추가.

## Phase 1. 작업 유형 판별

요청을 아래 넷 중 하나로 분류한다. 유형에 따라 소집할 팀원이 다르다 —
**모든 작업에 6명을 다 부르지 않는다.**

| 유형 | 트리거 예 | 소집 팀원 |
|---|---|---|
| **A. 차시 개선** | "4차시 loc/iloc 설명 보강", "7차시 예제 추가" | architect, content-writer, notebook-engineer, domain-reviewer, consistency-qa |
| **B. 전 차시 감사** | "전체 점검", "오류 찾아줘" | (팬아웃 서브) + domain-reviewer, consistency-qa |
| **C. 디자인 개편** | "랜딩 바꿔줘", "카드 레이아웃 개선" | design-steward, consistency-qa (+ 본문 글 변경 시 content-writer) |
| **D. 차시 신설** | "11차시 추가", "fab.csv 부록" | 유형 A 전원 |

애매하면 좁은 쪽으로 분류하고 사용자에게 한 줄로 확인한다. 범위를 임의로 넓히지 않는다.

**유형 B와 C의 상세 절차는 `references/workflows.md`를 읽는다.** 아래 Phase 2~5는 유형 A/D 기준이다.

## Phase 2. 스펙 확정 (단일 서브 에이전트)

```
Agent(subagent_type: "general-purpose", model: "opus",
      prompt: ".claude/agents/curriculum-architect.md 를 읽고 그 역할로 수행하라.
               .claude/skills/curriculum-spec/SKILL.md 를 먼저 읽어라.
               요청: {사용자 요청 원문}
               대상 차시: week{XX}
               산출물: _workspace/01_architect_spec.md")
```

스펙이 나오면 **리드가 직접 읽고** 다음을 확인한 뒤 진행한다.

- 영향 산출물 목록에 빠진 게 없는가 (특히 퀴즈와 데이터사전 — 가장 자주 누락된다)
- 새 개념 예산(3~5개)을 넘기지 않는가
- "검증 기준"이 실제로 확인 가능한 문장인가

스펙에 사용자 판단이 필요한 항목이 있으면 **여기서 멈추고 묻는다.** 제작을 시작한 뒤 방향을
되돌리는 것이 훨씬 비싸다.

## Phase 3. 제작 (에이전트 팀)

```
TeamCreate(team_name: "week{XX}-build",
           members: ["content-writer", "notebook-engineer", "domain-reviewer", "consistency-qa"])
```

작업 순서와 의존 관계를 `TaskCreate`로 건다.

1. **notebook-engineer 먼저 시작한다.** 코드와 데이터가 확정돼야 content-writer가 실을 코드와
   수치가 정해진다. 반대로 하면 강의 자료의 코드를 두 번 쓰게 된다.
2. notebook-engineer가 확정 코드·실제 출력을 `_workspace/03_notebook_report.md`에 쓰고
   `SendMessage`로 content-writer에게 알린다.
3. content-writer가 4종을 작성한다. 새 반도체 용어를 도입하면 domain-reviewer에게 즉시 묻는다.
4. **consistency-qa는 각 산출물이 끝날 때마다 그 부분을 검증한다.** 전부 끝난 뒤 한 번 도는
   방식은 어디서 깨졌는지 추적을 어렵게 한다.

**데이터 전달**: 태스크 기반(조율) + 파일 기반(`_workspace/` 산출물) + 메시지 기반(실시간 확인).
파일명 규약은 `{순번}_{에이전트}_{산출물}.md`다.

## Phase 4. 검증 (같은 팀 유지)

1. **domain-reviewer** → `_workspace/05_domain_review.md`
2. **consistency-qa** → `_workspace/06_qa_report.md`. 반드시 아래 셋을 실제로 실행한다.
   ```bash
   python scripts/validate_datasets.py
   python scripts/validate_notebooks.py
   python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week {N}
   ```
3. FAIL·차단 항목을 담당자에게 배분 → 수정 → **해당 차시 전체 재검증**.
4. 통과할 때까지 3~4를 반복한다. 단, 같은 항목이 3회 고쳐도 통과하지 않으면 멈추고 사용자에게
   상황과 선택지를 보고한다 — 무한 루프에 빠지지 않는다.

**통과 기준**: 자동 검사 FAIL 0건, domain-reviewer 차단 0건, 스펙의 "검증 기준" 전부 충족.
WARN은 문맥 판정 후 남길 수 있으나, 남긴 이유를 리포트에 적는다.

## Phase 5. 마무리

```
TeamDelete   # 팀 정리
```

1. 사용자에게 보고한다 — **변경한 파일 목록, 검증 명령의 실제 출력, 남긴 WARN과 그 이유,
   처리하지 못한 항목.** 검증 출력 없이 "완료했습니다"라고 쓰지 않는다.
2. 커밋은 사용자가 요청할 때만 한다.
3. **피드백을 청한다**: "결과에서 고칠 부분이 있나요? 팀 구성이나 순서를 바꾸고 싶은 점은요?"
4. 피드백이 오면 아래 경로로 반영하고 `CLAUDE.md`의 변경 이력에 기록한다.

| 피드백 | 수정 대상 |
|---|---|
| 결과물 품질 | 해당 에이전트의 스킬 |
| 역할 누락 | `.claude/agents/` 에이전트 정의 |
| 순서 문제 | 이 오케스트레이터 |
| 트리거 누락 | 스킬 `description` |

## 에러 핸들링

| 상황 | 대응 |
|---|---|
| 에이전트가 산출물 없이 끝남 | 1회 재시도. 재실패 시 그 부분 없이 진행하고 **최종 보고에 누락을 명시** |
| 두 에이전트의 결론이 상충 | 어느 쪽도 지우지 않고 둘 다 기록한 뒤 curriculum-architect에게 판정 요청 |
| 검증 스크립트가 환경 문제로 실패 | 콘텐츠 실패와 구분해 보고. 조용히 건너뛰지 않는다 |
| 원본 데이터 수정 시도 감지 | 즉시 중단. `data/raw/`는 읽기 전용이다(CLAUDE.md) |
| 요청 범위가 작업 중 커짐 | 확장분을 별도 항목으로 분리해 사용자에게 진행 여부를 묻는다 |

## 절대 규칙 (CLAUDE.md)

- `data/raw/`의 `반도체_공정_샘플.csv`, `fab.csv`는 **수정 금지**.
- 새 실습 데이터는 `scripts/generate_weekly_data.py`에 **시드 고정** 로직으로 추가하고
  `data/weekly/weekXX/`에 `utf-8-sig`로 저장한다.
- 데이터·노트북 수정 후 `validate_datasets.py`와 `validate_notebooks.py`를 **반드시 실행**한다.
- HTML은 `assets/css/common.css`의 **기존 클래스만** 재사용한다(새 CSS 프레임워크 금지).
- `fab.csv`의 `Sensor0~Sensor589`의 **실제 물리적 의미를 단정하지 않는다.**
- 8·9·10차시에서는 "원인"이 아니라 **"원인 후보"**로 쓴다.
- 커리큘럼 기준은 `docs/curriculum.md`(v2), 변경 배경은 `docs/restructure-plan.md`.
- Windows에서는 `python3`가 아니라 **`python`**을 쓴다.

## 테스트 시나리오

**정상 흐름** — "4차시에 loc/iloc 연습 문제를 2개 더 넣어줘"
Phase 0에서 `_workspace/` 없음 → 초기 실행. Phase 1에서 유형 A. architect가 3차시 함수 개념과의
연결을 확인하고 스펙 작성(영향: 강의 HTML, 실습지, 퀴즈, 학생·정답 노트북). notebook-engineer가
문제용 코드를 짜 실행하고 실제 출력 확정 → content-writer가 강의 실습 섹션·실습지·퀴즈에 반영 →
QA가 세 스크립트 실행 + 강의 코드 ↔ 노트북 코드 대조 → FAIL 0건 → 보고 + 피드백 요청.

**에러 흐름** — 위 작업 중 `validate_notebooks.py`가 `week04_student.ipynb`에서 `KeyError: '두께_nm'`
로 실패. QA가 이를 **환경이 아닌 콘텐츠 실패**로 분류하고 notebook-engineer에게 전달. 확인 결과
새 문제가 4차시 CSV에 없는 열을 참조. notebook-engineer는 열을 임의로 추가하지 않고
curriculum-architect에게 보고 — architect가 "4차시는 열 선택·조건 검색까지만 다룬다"는 범위를
근거로 기존 열을 쓰도록 스펙을 수정. content-writer와 notebook-engineer가 함께 고치고 QA가
4차시 전체를 재검증해 통과. 최종 보고에 이 우회 사실을 적는다.
