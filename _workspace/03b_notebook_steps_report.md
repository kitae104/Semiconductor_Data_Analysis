# 노트북·데이터 작업 보고 — 묶음 2 (노트북 3종 단계 정합, week01~week10)

담당: notebook-engineer / 범위: `notebooks/` 만. `data/`, `data/data_dictionary/`, `scripts/`,
`lectures/`, `assets/` 는 손대지 않았다(동시 작업 중인 에이전트 영역).

## 변경한 파일

| 파일 | 변경 요약 |
|---|---|
| `notebooks/solutions/week01_solution.ipynb` | 4단계 제목에 `(도전)` 추가 — student/instructor에 맞춤 |
| `notebooks/instructor/week02_instructor.ipynb` | 10단계에 `(도전)` 추가 / `11단계. 오류 대처 방법` → `## 오류 대처 방법`(번호 제거) / `11단계. 오늘의 학습을 한 문장으로 정리하기` 신규 추가 |
| `notebooks/instructor/week03_instructor.ipynb` | `9단계. 오류 대처 방법` → `## 오류 대처 방법` / `9단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/instructor/week04_instructor.ipynb` | `8단계. 오류 대처 방법` → `## 오류 대처 방법` / `8단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/instructor/week05_instructor.ipynb` | `7단계. 오류 대처 방법` → `## 오류 대처 방법` / `7단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/instructor/week06_instructor.ipynb` | 2~6단계 제목에 부제 복원 / `8단계. 오류 대처 방법` → `## 오류 대처 방법` / `8단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/solutions/week06_solution.ipynb` | 2~6단계 제목에 부제 복원(student 기준) |
| `notebooks/instructor/week07_instructor.ipynb` | `7단계. 오류 대처 방법` → `## 오류 대처 방법` / `7단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/solutions/week08_solution.ipynb` | 4단계 제목 `온도와 두께의 관계` → `온도와 두께의 관계(산점도 + 상관계수)` |
| `notebooks/instructor/week08_instructor.ipynb` | 4·5·6단계 제목을 student에 맞춤 / `7단계. 냉각수온도 → 공정온도 시차 패턴(확장)` → `## 냉각수온도 → 공정온도 시차 패턴(확장, 강사 시연)`(번호 제거) / `7단계. 오늘의 분석을 한 문장으로 정리하기` 추가 |
| `notebooks/instructor/week09_instructor.ipynb` | `7단계. 오류 대처 방법` → `## 오류 대처 방법` / `7단계. 오늘의 학습을 한 문장으로 정리하기` 추가 |
| `notebooks/instructor/week10_instructor.ipynb` | `6단계. 오류 대처 방법` → `## 오류 대처 방법` / `7단계(회고). 10차시 되짚기` → `6단계(회고). 10차시 되짚기` (단계 11개 → 10개, student와 일치) |

**삭제한 강사 전용 내용은 없다.** `오류 대처 방법`·`확장 실습(빠른 학습자용)`·week08의 시차 패턴
확장 시연은 모두 원문 그대로 남아 있고, **단계 번호만 떼어** week08 instructor가 이미 쓰고 있던
`## 오류 대처 방법`(번호 없음) 관례에 맞췄다. 해당 셀 아래의 코드 셀도 그대로다.

## 처리 원칙 (두 성격의 문제)

### (가) 단순 제목 표현 차이 → 더 설명적인 쪽(student)으로 통일

- week01 4단계 `(도전)`, week02 10단계 `(도전)`, week08 6단계 `(도전)`
- week06 2~6단계 부제(`— 시간에 따른 온도 변화` 등), week08 4·5단계 부제

제목 줄만 고쳤고 셀 본문·코드는 건드리지 않았다.

### (나) 강사용에 단계 자체가 빠진 것 → 추가

week02~09 강사용 8개 노트북에 "오늘의 학습/분석을 한 문장으로 정리하기" 단계가 없었다.
`docs/curriculum.md` 「차시 간 연결 원칙」("결과 해석 문장 쓰기는 1~10차시 매 차시 포함되는 고정
활동")에 따라 **학생용과 같은 번호·같은 제목**으로 추가했고, 강사용답게 다음을 붙였다.

- `**진행 방법**` — 이 차시에서 학생이 문장을 못 쓸 때 던질 질문
- `**설명 포인트**` — 고정 활동인 이유(과정 목표와의 연결), 최소 2~3분 확보
- `> (예시 답안) …` — 정답 노트북의 문장을 그대로 사용(세 노트북의 모범답안 일치 유지)

week01은 학생용에도 "정리하기"가 없으므로 **새로 만들지 않았다**(제목 1건만 수정).
week10은 학생용의 `6단계(회고). 10차시 되짚기`가 그 역할이므로 추가 없이 번호만 맞췄다.

8차시 예시 답안은 CLAUDE.md에 따라 **"원인"이 아니라 "원인 후보"**로 쓰여 있고, 강사 노트에
학생이 "원인이다"라고 말하면 그 자리에서 교정하라는 지시를 넣었다.

## 확정된 단계 목록 (세 노트북 완전 일치)

```
week01: OK (8단계)    week06: OK (12단계)
week02: OK (15단계)   week07: OK (11단계)
week03: OK (13단계)   week08: OK (11단계)
week04: OK (12단계)   week09: OK (11단계)
week05: OK (11단계)   week10: OK (10단계)
ALL IDENTICAL: True
```

(student / solutions / instructor 세 노트북의 `## N단계.` 제목 리스트를 직접 추출해 3자 비교)

## 실행 검증 결과

### check_course_consistency.py --quiet

작업 전 (단계 관련 WARN 12건 포함, 총 WARN 20건):

```
[WARN] (week01) week01 단계 제목 일치 (student vs solutions) — 1건
[WARN] (week02) week02 단계 제목 일치 (student vs instructor) — 2건
[WARN] (week03) week03 단계 제목 일치 (student vs instructor) — 1건
[WARN] (week04) week04 단계 제목 일치 (student vs instructor) — 1건
[WARN] (week05) week05 단계 제목 일치 (student vs instructor) — 1건
[WARN] (week06) week06 단계 제목 일치 (student vs instructor) — 6건
[WARN] (week06) week06 단계 제목 일치 (student vs solutions) — 5건
[WARN] (week07) week07 단계 제목 일치 (student vs instructor) — 1건
[WARN] (week08) week08 단계 제목 일치 (student vs instructor) — 4건
[WARN] (week08) week08 단계 제목 일치 (student vs solutions) — 1건
[WARN] (week09) week09 단계 제목 일치 (student vs instructor) — 1건
[WARN] (week10) week10 단계 수 일치 (student vs instructor) — student 10개 vs instructor 11개
검사 743건 · PASS 723 · WARN 20 · FAIL 0
```

작업 후 (출력 전문):

```
[WARN] (week02) week02_basic_process_values.csv 모든 열이 데이터사전에 설명됨 — 누락: ['측정시간', '압력_Pa']
[WARN] (week03) week03_process_filtering.csv 모든 열이 데이터사전에 설명됨 — 누락: ['측정시간', '압력_Pa', '가스유량_slm']
[WARN] (week04) week04_dirty_process_data.csv 모든 열이 데이터사전에 설명됨 — 누락: ['처리시간_sec']
[WARN] (week05) week05_process_visualization.csv 모든 열이 데이터사전에 설명됨 — 누락: ['두께_nm', '진동_mm_s']
[WARN] (week06) week06_equipment_comparison.csv 모든 열이 데이터사전에 설명됨 — 누락: ['작업조', '진공도_mTorr']
[WARN] (week07) week07_yield_defect_analysis.csv 모든 열이 데이터사전에 설명됨 — 누락: ['검사수량', '양품수량', '불량수량', '수율_pct']
[WARN] (week09) week09_fab_beginner.csv 모든 열이 데이터사전에 설명됨 — 누락: ['SensorTime', 'Chamber_Temperature_edu', 'Chamber_Pressure_edu', 'Gas_Flow_edu', 'RF_Power_edu', 'Vacuum_Level_edu', 'Cooling_Water_Temperature_edu', 'Vibration_edu', 'Process_Time_edu', '주요센서_A', '주요센서_B']
[WARN] (week09) week09_fab_selected_sensors.csv 모든 열이 데이터사전에 설명됨 — 누락: ['SensorTime', 'Sensor59', 'Sensor103', 'Sensor510', 'Sensor348', 'Sensor431', 'Sensor434', 'Sensor430', 'Sensor435', 'Sensor21', 'Sensor28', 'Sensor436', 'Sensor129', 'Sensor210', 'Sensor298', 'Sensor163', 'Pass_Fail']

검사 743건 · PASS 735 · WARN 8 · FAIL 0
```

**단계 관련 WARN 0건.** 남은 8건은 전부 `data/data_dictionary/` 열 설명 누락으로, 다른
에이전트가 동시 작업 중인 묶음이다(이 작업 범위 밖, 이 작업으로 늘거나 줄지 않았다).

### scripts/validate_notebooks.py

```
[PASS] student: notebook 파일 존재(10개)
[PASS] student/week01_student.ipynb: nbformat 유효
... (student week01~week10 각 nbformat 유효)
[PASS] instructor: notebook 파일 존재(10개)
[PASS] instructor/week01_instructor.ipynb: nbformat 유효
[PASS] instructor/week01_instructor.ipynb: 실행 성공
... (instructor week01~week10 각 nbformat 유효 + 실행 성공)
[PASS] solutions: notebook 파일 존재(10개)
[PASS] solutions/week01_solution.ipynb: nbformat 유효
[PASS] solutions/week01_solution.ipynb: TODO 잔존 없음
[PASS] solutions/week01_solution.ipynb: 실행 성공
... (solutions week01~week10 각 nbformat 유효 + TODO 잔존 없음 + 실행 성공)

총 63건 중 63건 통과, 0건 실패
```

종료 코드 0. 커널(`python3`) 정상, 실행 오류 없음.

비치명 경고 1건: `zmq/_future.py RuntimeWarning: Proactor event loop does not implement
add_reader family of methods required for zmq ...` — Windows asyncio/pyzmq 조합에서 항상 나오는
환경 경고로, 수정 전에도 동일하게 출력되며 검증 결과에 영향이 없다.

### JSON 구조 확인

전체 30개 노트북을 `json.load`로 파싱해 통과. 셀 `id` 누락·중복 없음(신규 셀 9개 포함).
파일은 기존과 동일하게 **CRLF + indent=1 + ensure_ascii=False**로 저장해 불필요한 diff가 없다.
`git diff --stat -- notebooks/` 기준 12개 파일 126 삽입 / 27 삭제.

## 학생용 빈칸 / 표현 규칙

- 학생용 노트북은 이번 작업에서 **한 줄도 수정하지 않았다** — 빈칸(`TODO`/`____`) 그대로.
- 정답·강사 노트북에 추가한 셀은 전부 **마크다운**이며 `TODO`/`____`를 포함하지 않는다.
  `validate_notebooks.py`의 "TODO 잔존 없음" 10건 PASS로 확인.
- 8차시 추가 문구는 "원인 후보" 표현을 사용(CLAUDE.md). 정합성 검사의 인과 단정 항목도 PASS.

## 데이터 변경이 있었다면 그 파급

`data/`·`scripts/` **미변경**. 데이터 재생성 불필요, `validate_datasets.py` 회귀 대상 아님.

다만 **강사용 노트북의 단계 번호가 바뀐 차시가 있어** 다른 산출물 담당자가 확인해야 한다.

| 차시 | 바뀐 것 | 확인이 필요한 곳 |
|---|---|---|
| week02~09 강사용 | `오류 대처 방법`이 단계 번호를 잃음(내용 동일) | `lectures/weekXX/instructor-guide.md`가 "N단계. 오류 대처"를 번호로 참조하고 있는지 |
| week10 강사용 | 회고가 `7단계(회고)` → `6단계(회고)` | 위와 같음 + 운영안 시간 배분표에 단계 번호가 적혀 있는지 |
| week06 / week08 | 2~6단계·4~6단계 제목에 부제 추가(강사용·정답본) | 강의 HTML의 "실습 흐름" 목록, 실습지 문제 제목이 짧은 제목을 쓰고 있다면 동일하게 부제 반영 |

→ **content-writer에게 요청**: 위 3줄만 `lectures/` 쪽에서 대조해 달라. `lectures/`는 내 수정
범위가 아니라 직접 고치지 않았다.

## 확정된 코드 예제 (content-writer가 그대로 실어야 하는 것)

이번 작업은 **마크다운 단계 제목·강사 노트만 수정**했고 코드 셀은 한 줄도 바꾸지 않았다.
따라서 content-writer가 새로 반영해야 할 확정 코드/출력 수치는 없다
(기존 `_workspace/03_notebook_report.md`의 수치가 그대로 유효).
