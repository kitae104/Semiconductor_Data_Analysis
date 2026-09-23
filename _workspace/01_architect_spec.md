# 작업 스펙 — 전 차시(week01~week09) / 작업 유형: 감사 지적 해소

## 배경

### 사용자 요청 원문
> "전 차시 감사에서 나온 WARN 11건을 하네스로 문제 없도록 수정해줘. 단, 아직 사진은 추가하기 전이라
> 사진·이미지·디자인 개편 관련 작업은 범위에서 제외."

### 기계 검사 결과(입력, 재확인 불필요)
`_workspace/00_machine_audit.txt` — 검사 733건 · PASS 722 · WARN 11 · FAIL 0.

### 현재 상태에서 직접 확인한 사실

**사실 1 — 감사 WARN 8건(데이터사전 누락)의 원인은 "사전 누락"이 아니라 "v1 잔재 CSV"다.**
WARN이 붙은 8개 CSV 전부가 `lectures/`, `notebooks/`, `scripts/`, `data/data_dictionary/`,
`docs/data-design.md`, `index.html`, `README.md` 어디에서도 **참조되지 않는다**(파일명 전수 grep 결과,
유일한 언급은 `docs/restructure-plan.md`의 "과도기 상태" 설명뿐).

| 폴더 | 현재 CSV | 판정 |
|---|---|---|
| week02 | `week02_basic_process_values.csv` / `week02_python_basics_1.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week03 | `week03_process_filtering.csv` / `week03_python_basics_2.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week04 | `week04_dirty_process_data.csv` / `week04_process_filtering.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week05 | `week05_process_visualization.csv` / `week05_dirty_process_data.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week06 | `week06_equipment_comparison.csv` / `week06_process_visualization.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week07 | `week07_yield_defect_analysis.csv` / `week07_equipment_yield.csv` | 앞=v1 잔재, 뒤=v2 정본 |
| week09 | `week09_fab_beginner.csv`, `week09_fab_selected_sensors.csv` / `week09_pass_fail_train.csv`, `week09_new_lots_to_predict.csv` | 앞 2개=v1 잔재, 뒤 2개=v2 정본 |

v2에서 파이썬 기초 2차시가 앞에 추가되어 차시가 한 칸씩 밀렸기 때문에, v1의 `weekN` 파일이
v2의 `week(N+1)` 폴더 정본과 **같은 폴더에 공존**하는 모양이 됐다(예: v1 `week03_process_filtering.csv`
↔ v2 `week04_process_filtering.csv`).

**사실 2 — 생성·검증 스크립트는 이미 v2만 안다.**
- `scripts/generate_weekly_data.py`의 `save_csv()` 호출은 정확히 11개이며, 위 표의 "v2 정본"과 1:1로 일치한다.
  삭제 대상 8개를 만드는 코드는 **이미 제거돼 있다**(`gen_week09()`에 fab 파생 로직 없음,
  `SELECTED_SENSORS`/`BEGINNER_ALIAS` 상수 부재).
- `scripts/validate_datasets.py`의 `validate_week()` 호출도 v2 정본 11개만 검증한다. 삭제 대상은 검증 대상이 아니다.
- 따라서 **파일을 지워도 두 스크립트는 그대로 통과하며, 재생성해도 되살아나지 않는다.**

**사실 3 — `week09_fab_beginner.csv`는 CLAUDE.md 절대 규칙을 파일 자체가 위반하고 있다.**
헤더가 `SensorTime, Chamber_Temperature_edu, Chamber_Pressure_edu, Gas_Flow_edu, RF_Power_edu,
Vacuum_Level_edu, Cooling_Water_Temperature_edu, Vibration_edu, Process_Time_edu, 주요센서_A, 주요센서_B, 검사결과`이고,
같은 행의 값이 `week09_fab_selected_sensors.csv`의 `Sensor59, Sensor103, Sensor510, Sensor348,
Sensor431, Sensor434, Sensor430, Sensor435` 값과 소수점 자리만 다를 뿐 동일하다.
즉 이 파일은 **`Sensor59 = 챔버 온도`라고 열 이름으로 단정한 결과물**이다.
CLAUDE.md: "`Sensor0~Sensor589`의 실제 물리적 의미를 절대 단정하지 않는다."
추가로 `SensorTime`이 `2008-07-19 11:55:00`처럼 SECOM 원본 시각을 그대로 담고 있어,
"이 과정의 데이터는 전부 교육용 가상 데이터"라는 과정 전제와도 어긋난다.
`week09_fab_selected_sensors.csv`는 `Pass_Fail = -1`(정상) 부호를, `week09_fab_beginner.csv`는
`검사결과 = 0`을 쓰고 있어 v2 정본(`검사결과` 0=합격/1=불합격)과 부호 규약이 섞이는 혼동 위험도 있다.

**사실 4 — 묶음 2(노트북 단계 제목)는 solutions 쪽만 제목이 짧게 잘려 있는 형태다.**
세 노트북의 `## N단계` 제목을 전수 비교한 결과:

| 차시 | 불일치 단계 | student(정본 후보) | solutions(현재) |
|---|---|---|---|
| week01 | 4단계 | `4단계(도전). 나만의 자기소개 만들기` | `4단계. 나만의 자기소개 만들기` |
| week06 | 2·3·4·5·6단계 | `2단계. 선 그래프 — 시간에 따른 온도 변화` 외 4건(설명형) | `2단계. 선 그래프` 외 4건(축약형) |
| week08 | 4단계 | `4단계. 온도와 두께의 관계(산점도 + 상관계수)` | `4단계. 온도와 두께의 관계` |

student를 정본으로 삼는 근거(추측 아님, 같은 저장소 안의 기존 규약):
- week08의 나머지 단계(5·6·7단계)는 **이미 student의 설명형 제목 그대로 solutions에도 들어가 있다**
  (`5단계. 습도(대조군)와 불합격의 관계 확인하기`, `6단계(도전). EQ-02의 진동 값 비교하기`).
  즉 설명형 + `(도전)` 표기가 student↔solutions 공통 규약이고, 어긋난 7개 줄이 예외다.
- `(도전)`은 학습자에게 난이도를 알리는 표시이므로 정답 노트북에서만 사라질 이유가 없다.
- week01의 instructor 노트북도 `(도전)`을 쓴다 — solutions 한 곳만 다르다.

**사실 5 — instructor 노트북에는 감사가 잡지 않는 별개의 차이가 있다(이번 범위 밖).**
감사 하네스는 student↔solutions만 비교한다(`check_course_consistency.py`의
`warn_if(... "학생용/정답 단계 제목 정렬" ...)`). 확인해 보니 instructor에는 **내용 자체가 다른 단계**가 있다:
week06 8단계 = `오류 대처 방법`(student/solutions는 `오늘의 학습을 한 문장으로 정리하기`),
week08 7단계 = `냉각수온도 → 공정온도 시차 패턴(확장)`. 이것은 강사용 추가 콘텐츠로 보이며,
맞추려면 콘텐츠를 지우거나 옮겨야 한다 → **감사 지적 해소가 아니라 콘텐츠 변경이므로 이번 범위에서 제외한다.**

---

## 묶음 3 판정 (요청받은 판단 항목)

### 결론: **(b) 쓰이지 않는 v1 잔재다 — 파일 제거가 맞다.**
그리고 이 판정은 week09 2개 파일에 그치지 않고, **묶음 1의 나머지 6개 파일에도 똑같이 적용된다.**
(즉 묶음 1과 묶음 3은 원인이 같은 하나의 문제다.)

### 근거
1. **참조 0건.** 8개 파일 모두 강의 HTML·실습지·퀴즈·운영안·노트북 3종·데이터사전 어디서도 참조되지 않는다.
2. **생성 로직 없음.** `generate_weekly_data.py`가 더 이상 만들지 않는다 → "재현 가능한 데이터"라는
   저장소 원칙(CLAUDE.md)을 만족하지 못하는 출처 불명 파일로 남아 있다.
3. **검증 대상 아님.** `validate_datasets.py`가 검사하지 않는다 → 깨져도 아무도 모른다.
4. **문서가 이미 삭제를 예고했다.** `docs/restructure-plan.md` TODO 2:
   "…`lectures/`·`notebooks/`가 아직 v1 파일명을 참조하므로, 지금 지우면 기존 강의자료가 바로 깨진다.
   TODO 3·5에서 해당 차시의 강의자료·노트북을 v2로 재작성한 뒤 옛 파일을 정리한다."
   → TODO 3·5는 완료됐고(현재 lectures/notebooks는 v2 파일명만 참조), **정리 조건이 이미 충족됐다.**
5. **(a)를 택할 수 없는 이유.** 데이터사전을 채우려면 `Chamber_Temperature_edu` 같은 열을 설명해야 하는데,
   열 이름 자체가 `Sensor59`의 의미를 단정한 결과다(사실 3). "의미를 단정하지 않는 방식으로 쓴다"는
   요청 조건을 지키려면 열 이름과 모순되는 사전을 쓰게 된다 — **CLAUDE.md 절대 규칙과 충돌하므로 불가.**
6. **(c)를 택할 수 없는 이유.** `restructure-plan.md` TODO 7이 선택 심화 부록 방침을 이미 정해 뒀다:
   "…부록을 만들려면 별도 스크립트/노트북에서 `data/raw/fab.csv`를 직접 읽어야 한다."
   즉 부록 경로는 **원본 직접 읽기**이지 이 파생 CSV 보존이 아니다. 게다가 부록용으로 남기더라도
   `week09_fab_beginner.csv`는 센서 의미 단정 위반이라 그대로 둘 수 없다.
   (`data/raw/fab.csv` 원본은 읽기 전용으로 **그대로 둔다** — 삭제 대상이 아니다.)

### (b)를 택할 때 함께 고쳐야 할 것 — 전수 목록
확인 결과 **추가로 고칠 코드는 없다.** 근거와 함께 하나씩:

| 함께 고쳐야 할 후보 | 실제 필요 여부 | 근거 |
|---|---|---|
| `scripts/generate_weekly_data.py` | **불필요** | `save_csv()` 11건에 삭제 대상 없음. fab 파생 로직 이미 제거됨 |
| `scripts/validate_datasets.py` | **불필요** | `validate_week()` 11건에 삭제 대상 없음 |
| `scripts/validate_notebooks.py` | **불필요** | 노트북이 삭제 대상을 로드하지 않음 |
| `data/data_dictionary/week02~09_dictionary.md` | **불필요** | 사전에 삭제 대상 파일명이 아예 없음(`week09_dictionary.md`는 v2 2파일만 설명) |
| `lectures/weekXX/*`(4종 × 10차시) | **불필요** | 참조 0건 |
| `notebooks/{student,instructor,solutions}/*` | **불필요** | 참조 0건 |
| `docs/data-design.md`, `docs/curriculum.md`, `README.md`, `index.html` | **불필요** | 삭제 대상 파일명 언급 0건 |
| `docs/restructure-plan.md` | **필요 (변경 D-1)** | "과도기 상태(의도적) … 함께 남아 있다"가 삭제 후 사실과 달라진다 |
| `reports/raw-data-profile.html`, `reports/validation-report.html` | **범위 밖(보고)** | 두 파일에 삭제 대상 파일명이 있으나 실행일이 박힌 **과거 기록 문서**다. 아래 "건드리지 않을 것" 참조 |
| `data/raw/fab.csv` | **손대지 않음** | CLAUDE.md 읽기 전용 |

---

## 앞뒤 차시 연결 확인

| 항목 | 내용 |
|---|---|
| 선수 지식(이전 차시에서 배운 것) | **변경 없음.** 이번 작업은 학습 내용을 한 글자도 바꾸지 않는다. 삭제 대상 8개 CSV는 어느 차시의 실습 흐름에도 등장하지 않으므로(참조 0건) 선수 지식 사슬에 관여하지 않는다. 노트북 수정도 `## N단계` 제목 줄 7개뿐이고 코드·설명 셀은 그대로다 |
| 이번 차시가 다음 차시에 넘겨야 할 것 | **변경 없음.** 9→10차시 연결은 `week09_pass_fail_train.csv`(모델 학습)와 `week09_new_lots_to_predict.csv`(10차시가 예측할 신규 로트)로 유지되며 둘 다 삭제 대상이 아니다. 4→5차시(`week04_process_filtering.csv` → `week05_dirty_process_data.csv`) 등 나머지 연결도 v2 정본만 사용하므로 영향 없음 |
| 이번 변경이 깨뜨릴 위험이 있는 연결 | ① **숨은 참조** — 전수 grep으로 0건 확인했으나, 작업자는 삭제 후 grep을 한 번 더 돌려 확인한다(검증 기준 V-5). ② **과거 기록 문서와의 불일치** — `reports/` 2개 문서가 삭제된 파일을 언급하게 된다. 학습 경로 밖이고 날짜가 박힌 기록이므로 수정하지 않고 리드에게 보고만 한다. ③ **week06 solutions 8단계 / week08 solutions 6·7단계는 instructor와 계속 다르다** — 하네스 검사 범위 밖이며 의도된 강사 전용 콘텐츠로 판단해 유지한다. ④ **폴더 내 파일 혼동 해소(긍정적 영향)** — 비전공자 학습자가 `data/weekly/week03/`을 열면 지금은 CSV가 2개라 어느 것을 읽어야 하는지 알 수 없다. 삭제 후 각 폴더는 그 차시가 실제로 쓰는 파일만 갖는다(week09만 2개) |

---

## 변경 스펙

### 묶음 1+3 — v1 잔재 CSV 제거 (WARN 8건 해소)

| # | 변경 내용 | 이유 | 영향 산출물 | 담당 |
|---|---|---|---|---|
| A-1 | `data/weekly/week02/week02_basic_process_values.csv` 삭제 | 참조 0건 v1 잔재. `week02_python_basics_1.csv`가 v2 정본 | 주차 데이터 1개 삭제(다른 산출물 변경 없음) | notebook-engineer |
| A-2 | `data/weekly/week03/week03_process_filtering.csv` 삭제 | 참조 0건 v1 잔재. v2 정본은 `week03_python_basics_2.csv`(4차시의 `week04_process_filtering.csv`와 혼동 유발) | 주차 데이터 1개 삭제 | notebook-engineer |
| A-3 | `data/weekly/week04/week04_dirty_process_data.csv` 삭제 | 참조 0건 v1 잔재. v2 정본은 `week04_process_filtering.csv`(정제 데이터는 5차시 `week05_dirty_process_data.csv`) | 주차 데이터 1개 삭제 | notebook-engineer |
| A-4 | `data/weekly/week05/week05_process_visualization.csv` 삭제 | 참조 0건 v1 잔재. v2 정본은 `week05_dirty_process_data.csv`(시각화 데이터는 6차시) | 주차 데이터 1개 삭제 | notebook-engineer |
| A-5 | `data/weekly/week06/week06_equipment_comparison.csv` 삭제 | 참조 0건 v1 잔재. v2 정본은 `week06_process_visualization.csv` | 주차 데이터 1개 삭제 | notebook-engineer |
| A-6 | `data/weekly/week07/week07_yield_defect_analysis.csv` 삭제 | 참조 0건 v1 잔재. v2 정본은 `week07_equipment_yield.csv` | 주차 데이터 1개 삭제 | notebook-engineer |
| A-7 | `data/weekly/week09/week09_fab_beginner.csv` 삭제 | 참조 0건 v1 잔재 + **CLAUDE.md 위반**(열 이름이 `Sensor59`를 `Chamber_Temperature_edu`로 단정) + SECOM 원본 시각 포함 | 주차 데이터 1개 삭제 | notebook-engineer |
| A-8 | `data/weekly/week09/week09_fab_selected_sensors.csv` 삭제 | 참조 0건 v1 잔재. v2 9차시는 `week09_pass_fail_train.csv` + `week09_new_lots_to_predict.csv`만 쓴다. `Pass_Fail=-1` 부호가 v2 `검사결과=0/1`과 섞여 혼동 유발 | 주차 데이터 1개 삭제 | notebook-engineer |

삭제 방식: `git rm`으로 이력에 남긴다(복원 가능). **8개 파일만** 지우고 같은 폴더의 v2 정본은 건드리지 않는다.
삭제 후 `data/weekly/` 전체는 `generate_weekly_data.py`가 만드는 11개와 정확히 일치해야 한다.

### 묶음 2 — 노트북 학생용/정답 단계 제목 정렬 (WARN 3건 해소)

정본은 **student 노트북**이다(사실 4의 근거). solutions 노트북의 `## N단계` **마크다운 헤딩 줄만** 고치고,
그 외 마크다운 본문·코드 셀·실행 결과는 한 글자도 바꾸지 않는다.

| # | 변경 내용 | 이유 | 영향 산출물 | 담당 |
|---|---|---|---|---|
| B-1 | `notebooks/solutions/week01_solution.ipynb`: `## 4단계. 나만의 자기소개 만들기` → `## 4단계(도전). 나만의 자기소개 만들기` | student·instructor가 모두 `(도전)` 표기. 난이도 표시가 정답본에서만 빠질 이유 없음 | 정답 노트북 1개(제목 1줄) | notebook-engineer |
| B-2 | `notebooks/solutions/week06_solution.ipynb`: 2~6단계 제목을 student와 동일한 설명형으로 교체 — `2단계. 선 그래프 — 시간에 따른 온도 변화`, `3단계. 막대그래프 — 설비별 측정 건수`, `4단계. 히스토그램 — 온도 분포`, `5단계. 산점도 — 온도와 두께의 관계`, `6단계. 박스플롯 — 설비별 온도 분포` | 축약형은 "무엇을 그리는지"만 알려주고 "무엇을 보려고 그리는지"를 지운다. 같은 저장소의 week08 규약(설명형 유지)과도 어긋남 | 정답 노트북 1개(제목 5줄) | notebook-engineer |
| B-3 | `notebooks/solutions/week08_solution.ipynb`: `## 4단계. 온도와 두께의 관계` → `## 4단계. 온도와 두께의 관계(산점도 + 상관계수)` | 같은 노트북의 5·6·7단계는 이미 student 제목 그대로다. 4단계만 예외 | 정답 노트북 1개(제목 1줄) | notebook-engineer |

주의(B-2·B-3): 제목에 쓰이는 `—`(em dash)와 괄호를 student와 **글자 단위로 동일**하게 넣는다.
하네스는 공백만 정규화(`\s+` → 1칸)하고 나머지는 완전 일치를 요구한다.

### 묶음 D — 문서 상태 갱신 (감사 WARN 항목은 아니지만, 삭제와 함께 처리해야 사실이 맞음)

| # | 변경 내용 | 이유 | 영향 산출물 | 담당 |
|---|---|---|---|---|
| D-1 | `docs/restructure-plan.md` TODO 2의 "**과도기 상태(의도적)**: … v1 시절 파일명이 새 v2 파일과 **함께 남아 있다** … TODO 3·5에서 … 옛 파일을 정리한다" 단락을, "**정리 완료**: v1 잔재 CSV 8개를 삭제했고, `data/weekly/`는 `generate_weekly_data.py`가 생성하는 11개 파일과 일치한다"는 사실 기술로 교체(삭제한 8개 파일명을 목록으로 남길 것) | 이 단락이 삭제 후 유일하게 사실과 어긋나는 문서 서술이 된다. 커리큘럼 설계 문서와 실제 파일이 다르면 다음 세션이 다시 잔재를 만든다 | `docs/restructure-plan.md` 1개 단락 | notebook-engineer 작성 → content-writer 문장 검토 |

**D-1은 A-1~A-8 삭제를 끝낸 뒤에 쓴다**(먼저 쓰면 문서가 거짓이 되는 구간이 생긴다).

---

## 새 개념 예산

**이번 작업의 새 개념: 0개.** 새로 등장하는 파이썬 함수·개념·용어가 없다(예산 3~5개 대비 0개, 적합).

근거: 변경은 (1) 어디서도 참조되지 않는 데이터 파일 삭제, (2) 정답 노트북 제목 줄 7개를 학생용과 일치시키기,
(3) 설계 문서 1개 단락의 상태 기술 갱신뿐이다. 강의 HTML·실습지·퀴즈·운영안·데이터사전·코드 셀은 열지 않는다.
따라서 차시별 난이도 계단, 선수 지식 사슬, Orange3 → 파이썬 순서, "결과 해석 문장 쓰기" 활동에 아무 영향이 없다.

---

## 건드리지 않을 것

작업자는 아래 항목에 **손대지 않는다.** 필요해 보이면 고치지 말고 리드에게 보고한다.

1. **사진·이미지·`assets/`·디자인 일체** — 사용자가 명시적으로 범위에서 제외했다(사진 추가 전).
   `assets/css/common.css`, `assets/js/*`, `assets/img/*`, HTML의 class·레이아웃·색상·히어로·아이콘,
   design-steward 영역 전부. 감사에서 디자인 관련 FAIL/WARN은 **0건**이므로 고칠 이유도 없다.
2. **`data/raw/`** — `반도체_공정_샘플.csv`, `fab.csv` 읽기 전용(CLAUDE.md). `fab.csv`는 **삭제하지 않는다.**
   이번에 지우는 것은 `data/weekly/week09/`의 파생 CSV 2개뿐이다.
3. **`data/weekly/`의 v2 정본 11개 CSV** — 내용·열·행 수·인코딩 모두 그대로. 값 재생성도 하지 않는다
   (검증 목적의 `generate_weekly_data.py` 재실행은 허용하되, 실행 후 `git diff`가 비어 있어야 한다).
4. **강의 HTML·실습지·quiz.json·instructor-guide.md(10차시 전부)** — 이번 감사 지적과 무관하다.
   `lectures/week09/quiz.json`의 fab.csv 관련 문항(9차시가 fab.csv를 쓰지 않는다는 O/X)은 **현재 서술이
   정확하므로 수정 대상이 아니다.**
5. **`scripts/generate_weekly_data.py`, `scripts/validate_datasets.py`, `scripts/validate_notebooks.py`** —
   이미 v2 기준이다. 삭제 대상 파일을 만들지도 검사하지도 않으므로 코드 변경 없음.
6. **instructor 노트북 3종(week01/06/08)** — 하네스는 student↔solutions만 비교한다.
   week06 8단계(`오류 대처 방법`), week08 6·7단계(`EQ-02의 진동 값 확인`, `냉각수온도 → 공정온도 시차 패턴(확장)`)는
   강사 전용 콘텐츠로 보이며, 맞추려면 콘텐츠를 옮기거나 지워야 한다 → **콘텐츠 변경이므로 제외.**
   (리드 판단이 필요하면 별도 작업으로 올린다.)
7. **student·solutions 노트북의 코드 셀·설명 셀·실행 출력** — 바꾸는 것은 `## N단계` 헤딩 줄 7개뿐이다.
   노트북을 재실행해 출력을 갱신하지 않는다(diff가 커져 검증이 불가능해진다).
8. **`reports/raw-data-profile.html`, `reports/validation-report.html`** — 실행일이 박힌 **과거 기록 문서**다
   (`raw-data-profile.html`은 "실행일 2026-07-31"). 삭제된 파일을 언급하지만, 그때의 사실을 적은 기록이므로
   소급 수정하지 않는다. **리드 보고 사항**: v2 기준 보고서 재발행이 필요한지는 이번 작업 밖에서 판단한다.
9. **`docs/curriculum.md`, `docs/data-design.md`, `README.md`, `index.html`, `CLAUDE.md`** — 삭제 대상 파일명
   언급이 0건이고 학습 내용 변경도 없으므로 열지 않는다. 갱신이 필요한 문서는 `docs/restructure-plan.md` 하나뿐이다(D-1).
10. **콘텐츠 개선 일체** — 설명 보강, 예제 추가, 퀴즈 문항 추가, 용어 카드 추가 등. 이번 작업은 감사 지적 해소다.

---

## 검증 기준

consistency-qa는 아래 9개를 순서대로 확인한다. **전부 PASS여야 작업 종료**다.

| # | 확인 방법 | 합격 조건 |
|---|---|---|
| V-1 | `python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py` | 마지막 줄이 **`FAIL 0` 그리고 `WARN 0`**. 총 검사 건수는 733 → **709**로 줄어든다(CSV 8개 × 검사 3종[utf-8-sig 로드 / 열 이름 존재 / 데이터사전 설명] = 24건 감소가 감소의 **유일한** 이유). 709가 아니면 의도하지 않은 산출물이 사라진 것이므로 FAIL 처리 |
| V-2 | `python scripts/validate_datasets.py` | FAIL 0건. 검사 건수가 작업 전(43건)과 **동일**해야 한다(감소하면 v2 정본을 잘못 지운 것) |
| V-3 | `python scripts/validate_notebooks.py` | FAIL 0건, 검사 63건 유지 |
| V-4 | `ls data/weekly/week01` … `week10` | 존재하는 CSV가 정확히 11개이고, `generate_weekly_data.py`의 `save_csv()` 목록과 파일명이 1:1로 일치한다. week09 폴더에는 `week09_pass_fail_train.csv`, `week09_new_lots_to_predict.csv` **2개만** 있다. 파일명에 `fab`가 들어간 파일이 `data/weekly/` 아래에 0개다 |
| V-5 | 8개 파일명(`week02_basic_process_values`, `week03_process_filtering`, `week04_dirty_process_data`, `week05_process_visualization`, `week06_equipment_comparison`, `week07_yield_defect_analysis`, `week09_fab_beginner`, `week09_fab_selected_sensors`)을 `lectures/ notebooks/ scripts/ data/ docs/ index.html README.md` 대상으로 grep | 매치가 **`docs/restructure-plan.md`의 D-1 "정리 완료" 문단 안에서만** 나온다. 그 밖의 매치 0건 |
| V-6 | `python scripts/generate_weekly_data.py` 재실행 → `git status data/weekly/` | 삭제한 8개 파일이 **되살아나지 않는다**. 그리고 v2 정본 11개의 `git diff`가 **0바이트**다(시드 고정이므로 내용이 바뀌면 안 된다) |
| V-7 | `git status` / `git diff --stat` | 변경된 파일이 정확히 **12개**다 — 삭제(D) 8건 + 수정(M) `notebooks/solutions/week01_solution.ipynb`, `week06_solution.ipynb`, `week08_solution.ipynb`, `docs/restructure-plan.md`. 그 밖의 파일 변경 0건(특히 `assets/`, `lectures/`, `notebooks/student/`, `notebooks/instructor/`, `data/raw/` 변경 0건) |
| V-8 | 세 차시(01/06/08)의 student와 solutions에서 `^##\s+\d+단계` 제목 목록을 각각 뽑아 비교 | 리스트가 **완전히 같다**(week01 8개, week06 12개, week08 11개 — 개수와 순서와 문자열 전부). 하네스의 "학생용/정답 단계 제목 정렬" 3건이 WARN → PASS |
| V-9 | 수정한 solutions 노트북 3개의 `git diff` | 변경된 줄이 **제목 줄뿐**이다 — week01 1줄, week06 5줄, week08 1줄(총 7줄). 코드 셀·`outputs`·`execution_count` 변경 0줄. solutions에 `TODO`/`____` 잔존 0건(V-1이 함께 검사) |

### 검증 실패 시 되돌리는 법
`git checkout -- <path>`, 삭제 취소는 `git restore --staged --worktree data/weekly/`. 원본 데이터는 손대지 않았으므로
`python scripts/generate_weekly_data.py`로 v2 정본 11개를 언제든 재현할 수 있다.

---

## 리드 보고 사항 (판단 요청, 이번 작업에서는 진행하지 않음)

1. **`reports/` 2개 문서의 v1 서술** — `raw-data-profile.html`("9차시만 `fab.csv`에서 선별한 10~20개 센서를 다룬다",
   `week09_fab_selected_sensors.csv`·`week09_fab_beginner.csv` 언급)과 `validation-report.html`("9차시는 fab.csv 원본을
   … 파생 파일 2종만 사용했다")은 v2와 어긋난다. 날짜가 박힌 기록 문서라 소급 수정하지 않았다.
   v2 기준 보고서 재발행 여부는 별도 판단이 필요하다.
2. **instructor 노트북의 단계 구성 차이**(week06 8단계, week08 6·7단계) — 하네스 범위 밖이지만,
   세 노트북을 완전히 정렬할지 강사 전용 단계를 허용할지는 팀 규약으로 정해 두는 편이 낫다.
3. **`docs/implementation-plan.md`의 v1 서술** — "fab.csv 직접 노출 금지 | 9차시에서만 … 선별된 10~20개 센서로 축소한
   파생 파일만 사용"은 v1 시점 계획이다. 이번 범위 밖이라 두었으나, v1 문서임을 문서 머리에 명시할지 판단이 필요하다.
