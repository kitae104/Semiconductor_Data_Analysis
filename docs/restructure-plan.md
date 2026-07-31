# 커리큘럼 재구성 계획 (v1 → v2)

이 문서는 [`docs/curriculum.md`](curriculum.md)의 v2 구성으로 넘어가면서, 기존에 이미 만들어진
`lectures/`, `notebooks/`, `data/weekly/`, `data/data_dictionary/` 산출물 중 무엇을 재사용하고
무엇을 새로 만들어야 하는지 정리한 작업 지도다. **이번 세션에서는 이 매핑만 확정하고, 실제 파일
재작성/이동은 하지 않았다.** 이후 세션에서 차시별로 순서대로 진행한다.

## 왜 바꾸는가

- v1은 프로그래밍 완전 초보자에게 파이썬 기초 없이 바로 Pandas부터 시작해 진입장벽이 높았다.
- v1의 9차시(`fab.csv`, 590개 센서)는 난이도가 급격히 올라가는 구간이었고, 반도체 산업 이해와도
  직접 관련이 적었다.
- Orange3 같은 노코드 도구로 같은 데이터를 다시 확인해보면, 코드 문법에 막혀도 개념은 놓치지 않게
  도와줄 수 있다.

## v1 → v2 차시 매핑

| v2 차시 | 제목 | 대응되는 v1 차시 | 데이터 재사용 여부 |
| --- | --- | --- | --- |
| 1 | 반도체 공정과 데이터 처음 만나기 + 변수·출력 | v1 1차시 + (신규) 변수·출력 | 그대로 재사용 |
| 2 | 리스트와 딕셔너리 | (신규, v1 2차시 일부 개념만 계승) | v1 2차시 데이터를 축소·재구성 |
| 3 | 리스트·딕셔너리로 배우는 조건문·반복문·함수 | (신규, v1 2차시 일부 개념만 계승) | v1 2차시 데이터 재사용(2차시와 동일 계열) |
| 4 | Pandas 가장 기본적인 부분 | v1 3차시 | 그대로 재사용 |
| 5 | 데이터 훑어보기와 정리(EDA), Orange3 먼저 확인 | v1 4차시 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 6 | 그래프로 공정 상태 이해하기, Orange3 먼저 확인 | v1 5차시 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 7 | 설비·공정 비교 + 수율 분석, Orange3 먼저 확인(신규 추가) | v1 6차시 + v1 7차시(압축 병합) | 기존 2개 데이터 중 선택 또는 병합해 신규 구성 필요 |
| 8 | 이상과 원인 후보 찾기, Orange3 먼저 확인 | v1 8차시 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 9 | 머신러닝 예측 모델 만들기, Orange3 먼저 확인 | v1 9차시(전면 교체) 앞부분 | **신규 데이터 필요** — `반도체_공정_샘플.csv` 계열로 교체, `fab.csv` 파생 데이터는 더 이상 핵심 경로에서 사용하지 않음 |
| 10 | 모델 평가와 새 데이터 예측, Orange3 재확인 | v1 9차시(전면 교체) 뒷부분 — **미니 프로젝트(구 v1 10차시)는 별도 차시로 남기지 않음** | 9차시 학습 데이터·새 로트 예측 데이터 재사용 |

> **2026-07-31 후속 조정**: 위 매핑을 확정한 뒤, 세 가지를 추가로 반영했다 — ①"주/주차" 용어를
> 전부 "차시"로 통일, ②Orange3 순서를 "코드 후 재확인"에서 "Orange3 먼저 → 코드로 확인"으로 반전,
> ③1~3차시 내용 재배분(1차시에 변수·출력 병합, 2차시는 리스트/딕셔너리 전용, 3차시는 리스트/딕셔너리
> 활용 조건문·반복문·함수)과 7차시 Orange3 신규 추가, 9~10차시를 머신러닝 전용 2개 차시로 확장(구
> 10차시 미니 프로젝트는 폐기). `data/weekly/week10/week10_mini_project_dataset.csv`는 삭제하지
> 않고 "선택 심화용" 데이터로 남겨뒀다(핵심 10차시 흐름에서는 더 이상 사용하지 않음).

## 각 항목별 TODO (다음 세션에서 순서대로 진행 권장)

1. ~~**데이터 설계 개정**~~ — ✅ 완료. `docs/data-design.md`를 v2 차시 구성에 맞게 다시 썼다.
   - 2·3차시용 축소 데이터 스펙 확정(`week02_python_basics_1.csv`, `week03_python_basics_2.csv`)
   - 7차시 병합 데이터 스펙 확정(`week07_equipment_yield.csv` — v1 6·7차시 열 병합)
   - 9차시 신규 데이터 스펙 확정(`week09_pass_fail_train.csv` + `week09_new_lots_to_predict.csv`,
     `반도체_공정_샘플.csv` 계열, fab.csv 미사용, seed 규칙 유지)
   - 10차시 데이터에서 fab.csv 기반 열/패턴 제거(원래도 fab.csv 열을 쓰지 않았으므로 명시만 추가)
   - **아직 안 한 것**: 이 스펙대로 실제 CSV를 생성하는 스크립트 작업(TODO 2)은 착수 전.
2. ~~**`scripts/generate_weekly_data.py` 개정**~~ — ✅ 완료. `gen_week02()`~`gen_week09()`를 v2 스펙에
   맞게 재작성하고 `python scripts/generate_weekly_data.py`로 `data/weekly/`를 재생성했다. 기존 시드
   규칙(`seed = 100 + 차시번호`)과 `utf-8-sig` 저장 규칙은 그대로 유지했다.
   - **과도기 상태(의도적)**: `week02`~`week07`, `week09` 폴더에는 v1 시절 파일명(예:
     `week02_basic_process_values.csv`, `week06_equipment_comparison.csv`,
     `week09_fab_beginner.csv` 등)이 새 v2 파일과 **함께 남아 있다**. `lectures/`·`notebooks/`가
     아직 v1 파일명을 참조하므로, 지금 지우면 기존 강의자료가 바로 깨진다. TODO 3·5에서 해당 차시의
     강의자료·노트북을 v2로 재작성한 뒤 옛 파일을 정리한다.
   - fab.csv 기반 `SELECTED_SENSORS`/`BEGINNER_ALIAS`/`gen_week09()`의 fab 파생 로직은 스크립트에서
     완전히 제거했다(9차시는 이제 `반도체_공정_샘플.csv` 계열 신규 데이터만 생성).
3. 🔶 **`lectures/weekXX/` 재작성** — **개요(skeleton) 단계까지 완료.** 2·3·4·5·6·7·9·10차시의
   `index.html`을 v2 제목·학습 목표·다룰 이론/실습 목차·데이터 파일명만 채운 개요 페이지로
   교체했다(상세 설명·예제 코드·단계별 실습·퀴즈는 아직 없음 — 각 페이지 상단에 "작성 상태"
   안내 박스로 명시). 내용이 아직 확정 전이라 이동/수정 가능성이 있어 우선 목차 수준으로만
   배치하기로 결정(사용자 지시). 1차시는 이미 v2와 동일해 그대로 두었고, 8차시는 기존 상세
   내용을 유지한 채 Orange3 Correlations 절만 추가했다.
   - **아직 안 한 것**: worksheet.html·quiz.json·instructor-guide.md는 이번 라운드에서 건드리지
     않았다(2~7·9·10차시는 v1 시절 파일이 그대로 남아 있어 새 index.html과 내용이 어긋날 수 있음
     — 상세 콘텐츠를 확정할 때 함께 재작성 필요).
4. **Orange3 안내 자료 신규 작성** — 5~10차시 공통으로 쓸 "Orange3 설치 및 기본 사용법" 섹션(또는
   별도 부록 문서)이 필요하다. 설치 방법, 기본 화면 구성, File/Data Table/Scatter Plot/Box Plot/
   Correlations/Tree/Test and Score/Predictions 위젯 사용법을 다룬다. (각 차시 개요 페이지에는 어떤
   위젯을 "먼저" 쓸지만 1줄로 표시해뒀다 — 5~9차시는 "① Orange3 먼저 → ② 파이썬" 순서, 10차시는
   9차시에서 만든 모델을 Predictions 위젯으로 재확인하는 순서다.)
5. 🔶 **`notebooks/{student,instructor,solutions}/` 재작성** — **개요(skeleton) 단계까지 완료.**
   2·3·4·5·6·7·9·10차시의 student/instructor/solutions 노트북(24개)을 모두 마크다운 셀만으로
   구성된 개요로 교체했다 — 다룰 실습 단계 목록 + (해당 시) Orange3 메모 + 데이터 경로만 있고
   실제 코드 셀은 없다. `python scripts/validate_notebooks.py` 63건 모두 통과(코드 셀이 없어
   instructor/solutions 실행 체크도 trivial하게 통과, solutions에는 'TODO' 문자열 없음 확인).
   1·8차시 노트북은 건드리지 않았다(이미 v2 데이터와 호환).
   - **아직 안 한 것**: 실제 코드 셀(`# TODO` 빈칸 포함)과 실행 결과, 설명은 상세 내용 확정 후 작성.
6. **`data/data_dictionary/weekXX_dictionary.md` 재작성** — 데이터가 바뀌는 2·3·7·9·10차시는 새로
   쓰고, 나머지는 차시 번호만 맞춰 재배치한다. (아직 착수 전 — v1 그대로.)
7. **`fab.csv` 취급 방침** — `data/raw/fab.csv`는 삭제하지 않고 그대로 둔다(원본 읽기 전용 원칙
   유지). 다만 핵심 10차시 경로에서는 참조하지 않으며, 원할 경우 강사용 "9차시 이후 심화 부록"으로만
   별도 언급한다. 이 부록을 다룰 때도 `CLAUDE.md`의 "Sensor0~589 실제 의미 단정 금지" 규칙은 그대로
   적용한다. (`generate_weekly_data.py`에는 더 이상 fab.csv 파생 로직이 없으므로, 부록을 만들려면
   별도 스크립트/노트북에서 `data/raw/fab.csv`를 직접 읽어야 한다.)
8. **검증 스크립트 갱신** — 🔶 부분 완료. `scripts/validate_datasets.py`는 v2 파일명·스펙 기준으로
   갱신해 43건 모두 통과 확인했다. `scripts/validate_notebooks.py`는 구조 자체(파일 존재·nbformat
   유효성·실행 성공·TODO 잔존 여부)는 스켈레톤 노트북에도 그대로 통하므로 아직 손대지 않았다 —
   63건 모두 통과 중이다. 다만 지금은 셀 안에 "무엇을 배웠는지" 검증할 내용이 없으므로, 상세
   코드가 채워지면 데이터 로딩·계산 결과를 확인하는 체크를 추가로 넣는 것을 고려한다.
9. **`README.md` / `index.html` / `CLAUDE.md`** — curriculum.md와 함께 1차 갱신했고, `index.html`의
   "진행 안내" 배너는 이번 라운드(데이터 재생성 + 개요 스켈레톤)에 맞춰 다시 갱신했다. 실제 상세
   콘텐츠가 채워지는 대로 세부 문구(파일명, 통계 수치 등)를 다시 맞춘다.

## 지금까지 실제로 변경한 파일

- `docs/curriculum.md` — v2 전체 재작성(이 문서가 가리키는 최신 구성)
- `docs/restructure-plan.md` — 신규 작성(이 문서)
- `README.md` — 목차 표·교육 목표 문구 갱신
- `index.html` — 차시 카드 제목/설명 갱신 + "진행 안내" 배너를 스켈레톤 단계에 맞게 갱신
- `CLAUDE.md` — fab.csv/9차시 관련 규칙을 v2 기준으로 일반화
- `docs/data-design.md` — v2 차시 구성에 맞게 전체 재작성(TODO 1 완료)
- `scripts/generate_weekly_data.py` — v2 스펙대로 재작성(TODO 2 완료)
- `data/weekly/week02`~`week10`(9차시 포함) — v2 스펙 CSV 생성(v1 파일은 과도기 동안 함께 보존)
- `scripts/validate_datasets.py` — v2 파일명·스펙 기준으로 갱신(TODO 8 중 데이터셋 검증만 완료)
- `lectures/week02,03,04,05,06,07,09,10/index.html` — 제목·학습목표·다룰 내용 개요만 담은 skeleton으로 교체(TODO 3 skeleton 단계 완료)
- `notebooks/{student,instructor,solutions}/week{02,03,04,05,06,07,09,10}_*.ipynb`(24개) — 마크다운
  개요 skeleton으로 교체(TODO 5 skeleton 단계 완료)
- 저장소를 git으로 초기화하고(`git init`) v1 상태를 첫 커밋으로 보존(안전한 되돌리기용)

### 2026-07-31 후속 라운드 — 용어 변경 + 차시 재배치 + Orange3 순서 반전

- **전 저장소 "주/주차" → "차시" 용어 변경** — docs, README, CLAUDE.md, index.html, `lectures/`,
  `notebooks/`, `data/data_dictionary/`, `reports/` 등 88개 파일에서 "1주차→1차시", "10주 과정→10차시
  과정", "매주→매 차시", "다음/이번/첫 주→다음/이번/첫 차시" 패턴을 스크립트로 일괄 치환했다.
  "범주/자주/주간/일주일/간주" 등 관련 없는 단어는 건드리지 않았다(사전에 grep으로 확인). 폴더/파일
  이름(`lectures/week01/`, `data/weekly/week01/`, `week01_*.csv` 등)은 내부 관리용 영어 표기라 그대로
  두었다 — 화면에 보이는 한글 설명만 바뀌었다.
- **`docs/curriculum.md` 전면 재작성** — 위 "v1 → v2 차시 매핑" 표와 각 차시 섹션에 반영된 새 구성으로
  다시 썼다. 5~10차시 전체에 "Orange3 먼저 → 파이썬으로 확인" 순서 원칙을 명시했다.
- **`lectures/week02,03,04,05,06,07,09,10/index.html` 재생성(2차 skeleton)** — 새 차시별 주제 배분과
  Orange3 우선 순서를 반영해 다시 만들었다. Orange3가 있는 차시는 "① Orange3로 먼저 훑어보기" 절이
  "② 파이썬으로 확인하기"(이론/실습) 절보다 앞에 온다.
- **`lectures/week01/index.html`** — 1차시 학습 목표에 "변수·`print()` 출력" 항목을 추가하고, "🐍
  파이썬 시작하기 — 변수와 출력" 개요 절을 새로 넣었다(상세 예제는 추후). "다음 차시 예고" 문구를
  2차시가 이제 "리스트·딕셔너리" 전용임에 맞게 수정했다.
- **`lectures/week08/index.html`** — 기존 상세 콘텐츠는 그대로 두고, Orange3 Correlations 절을 코드
  시연 섹션들 앞으로 옮겨 "① Orange3로 먼저 훑어보기 → ② 파이썬으로 확인하기" 순서로 바꿨다. 오래된
  "4차시 + 7차시 연결" 문구도 "5차시 + 7차시 연결"로 바로잡았다(5차시가 결측값 정리 차시).
- **`notebooks/{student,instructor,solutions}/week{02,03,04,05,06,07,09,10}_*.ipynb`(24개) 재생성** —
  새 차시별 실습 단계와 Orange3 순서를 반영해 마크다운 개요를 다시 썼다. 10차시 노트북은 더 이상
  미니 프로젝트가 아니라 "9차시 모델로 새 로트 예측 + Orange3 재확인" 내용으로 바뀌었다.
- **`index.html`** — 차시 카드 10개의 제목/설명을 새 구성에 맞게 갱신하고, 카드 번호 배지를 영어
  "WEEK 0N"에서 "N차시"로 바꿨다(용어 통일). "진행 안내" 배너도 Orange3 범위(5~10차시)와 순서 원칙,
  10차시가 더 이상 미니 프로젝트가 아니라는 점을 반영해 다시 썼다.
- `python scripts/validate_datasets.py`(43/43)와 `python scripts/validate_notebooks.py`(63/63) 모두
  0건 실패로 재확인했다.

`data/data_dictionary/`와 3~10차시(1·2차시 제외)의 `worksheet.html`·`quiz.json`·
`instructor-guide.md`는 **아직 v1 상태 그대로**다(용어 변경만 반영되고 내용은 예전 구성). 다음
단계는 이번에 배치한 lectures/notebooks 개요(skeleton)를 사용자가 검토·확정한 뒤, 그 확정된
목차를 기준으로 상세 설명·예제 코드·퀴즈·데이터 설명서를 실제로 채우는 것이다.

### 후속 진행 — 1·2차시 상세 콘텐츠 완성 + 시간 정보 제거 정책

- **1차시**: `lectures/week01/index.html`의 "파이썬 시작하기" 절을 개요에서 전체 내용으로
  확장했다(변수·자료형·print·f-string·input(), SVG 다이어그램 2개, 실습 섹션, 퀴즈 3문항 추가,
  과제 섹션 신설). `worksheet.html`에 3문제, `notebooks/*/week01_*.ipynb`에 7~10단계 실습 셀
  추가, `instructor-guide.md` 갱신 — 1차시는 이제 lectures/worksheet/notebooks/instructor-guide
  모두 상세 콘텐츠 완료 상태다.
- **2차시**: `lectures/week02/index.html`을 개요에서 전체 내용으로 교체했다(리스트/딕셔너리 개념,
  SVG 다이어그램 3개, 실습 섹션, 퀴즈 5문항, 과제 섹션). `worksheet.html`·`quiz.json`(v1의
  Pandas 섞인 내용 → 리스트/딕셔너리 전용으로 전면 재작성), `notebooks/*/week02_*.ipynb`(11단계
  실제 코드 노트북으로 전면 교체), `instructor-guide.md`(v1의 다른 주제 내용 → 실제 2차시 범위로
  전면 재작성)까지 모두 완료 — 2차시도 1차시와 동일하게 전 영역 완료 상태다.
- **시간 정보 제거 정책(전체 적용)**: "N차시 · 2시간 수업" 배지, `instructor-guide.md`의
  "N~M분" 시간표를 모든 차시(1~10)에서 제거했다(배지는 즉시 제거, 시간표는 시간 없는
  "## 수업 흐름" 번호 목록으로 전환). `docs/curriculum.md`, `docs/instructor-operation-guide.md`,
  `README.md`, `index.html`의 시간 관련 문구도 함께 정리했다. **앞으로 작성하는 모든 차시 콘텐츠는
  처음부터 시간/분 정보를 포함하지 않는다.**
- 3~10차시는 여전히 개요(skeleton) 또는 v1 상태다. 다음 차시를 요청받으면 1·2차시와 동일한
  패턴(lectures 전체 내용 + worksheet + quiz.json + notebooks 3종 + instructor-guide, 시간 정보
  없이)으로 진행한다.

### 후속 진행 — 3~10차시 전체 상세 콘텐츠 완성 (2026-07-31)

- **3~7·9·10차시**: 1·2차시와 동일한 패턴(lectures 전체 내용 + worksheet.html + quiz.json +
  notebooks 3종 + instructor-guide.md, 시간 정보 없이)으로 전부 상세 콘텐츠를 완성했다. 8차시는
  이전 세션에 이미 완료 상태임을 재확인했다. 이로써 **1~10차시 전 구간이 skeleton이 아닌 상세
  콘텐츠 완료 상태**가 되었다.
  - 모든 수치(합격률, 표준편차, 상관계수, 결측값 개수, 모델 정확도/혼동행렬/특성 중요도 등)는
    `scripts/generate_weekly_data.py`로 재생성한 현재 CSV를 직접 pandas/sklearn/matplotlib로
    계산해 검증한 실제 값이며, 예전 v1 문서에 남아 있던 근사치·오기(예: 5차시 결측값 "약 8건"→
    실제 10건, 7차시 "저수율 로트가 모두 EQ-04"→실제로는 5개 중 4개)는 발견 즉시 바로잡았다.
  - 6차시는 matplotlib 차트 5종을 실제로 생성해 `assets/images/week06/`에 PNG로 커밋했고, 7차시는
    구 v1 파레토 이미지를 실제 데이터로 재생성해 `assets/images/week07/pareto_defects.png`를
    덮어썼다.
  - 7차시는 구 v1의 6차시(설비 비교)와 7차시(수율·파레토) 두 데이터/문서를 하나로 병합했다.
  - 9~10차시는 fab.csv(590센서) 경로를 완전히 폐기하고 `week09_pass_fail_train.csv` +
    `week09_new_lots_to_predict.csv` 기반으로 전면 재작성했다 — 9차시는 "정확도의 함정"(모델
    정확도 78.2% < 항상-합격 기준선 78.9%)을 의도적 교훈으로 제시했고, 10차시는 `predict_proba()`로
    "예측은 같아도 확신의 정도는 다르다"를 보여준 뒤 10개 차시 전체를 되짚는 표와 "과정을 마치며"
    절로 마무리했다(마지막 차시이므로 "다음 차시 예고" 없음).
  - `lectures/week10/project-report-template.html`은 구 미니 프로젝트용 파일로 어떤 페이지에서도
    참조하지 않는 고아 파일이었다. 사용자 확인 후 삭제했고, `docs/instructor-operation-guide.md`의
    "10차시 미니 프로젝트" 평가 항목도 실제 10차시(9차시 모델로 새 로트 예측 + `predict_proba`)
    평가 기준으로 함께 고쳤다.
- **`data/data_dictionary/*.md` 재정비** — worksheet.html 등과 동일하게 차시 번호가 밀린 채
  방치돼 있던 것을 발견해 2·3·4·5·6·7·9·10차시 전부 다시 썼다(TODO 6 완료). 8차시는 이미
  정확해 손대지 않았다. 10차시 파일은 삭제하지 않고 "선택 심화용" 안내문을 추가해, v2의 실제
  10차시 핵심 데이터가 `week09_new_lots_to_predict.csv`임을 명확히 했다.
- `python scripts/validate_datasets.py`(43/43)와 `python scripts/validate_notebooks.py`(63/63)
  모두 0건 실패로 최종 재확인했다.
- **남은 항목**: `index.html`의 "진행 안내" 배너가 아직 "skeleton" 단계 문구를 담고 있다면
  갱신 필요(전 차시 상세 완료를 반영). `lectures/week10/project-report-template.html` 고아 파일
  정리 여부는 사용자 판단 필요.
