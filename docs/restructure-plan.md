# 커리큘럼 재구성 계획 (v1 → v2)

이 문서는 [`docs/curriculum.md`](curriculum.md)의 v2 구성으로 넘어가면서, 기존에 이미 만들어진
`lectures/`, `notebooks/`, `data/weekly/`, `data/data_dictionary/` 산출물 중 무엇을 재사용하고
무엇을 새로 만들어야 하는지 정리한 작업 지도다. **이번 세션에서는 이 매핑만 확정하고, 실제 파일
재작성/이동은 하지 않았다.** 이후 세션에서 주차별로 순서대로 진행한다.

## 왜 바꾸는가

- v1은 프로그래밍 완전 초보자에게 파이썬 기초 없이 바로 Pandas부터 시작해 진입장벽이 높았다.
- v1의 9주차(`fab.csv`, 590개 센서)는 난이도가 급격히 올라가는 구간이었고, 반도체 산업 이해와도
  직접 관련이 적었다.
- Orange3 같은 노코드 도구로 같은 데이터를 다시 확인해보면, 코드 문법에 막혀도 개념은 놓치지 않게
  도와줄 수 있다.

## v1 → v2 주차 매핑

| v2 주차 | 제목 | 대응되는 v1 주차 | 데이터 재사용 여부 |
| --- | --- | --- | --- |
| 1 | 반도체 공정과 데이터 처음 만나기 | v1 1주차 | 그대로 재사용 |
| 2 | 파이썬 기초 Ⅰ(변수·리스트·딕셔너리) | (신규, v1 2주차 일부 개념만 계승) | v1 2주차 데이터를 축소·재구성 |
| 3 | 파이썬 기초 Ⅱ(조건문·반복문·함수) | (신규, v1 2주차 일부 개념만 계승) | v1 2주차 데이터 재사용(2주차와 동일 계열) |
| 4 | Pandas로 읽고 선택하기 | v1 3주차 | 그대로 재사용 |
| 5 | 결측값 정리 + Orange3 | v1 4주차 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 6 | 그래프 + Orange3 | v1 5주차 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 7 | 설비·공정 비교 + 수율 분석 | v1 6주차 + v1 7주차(압축 병합) | 기존 2개 데이터 중 선택 또는 병합해 신규 구성 필요 |
| 8 | 이상과 원인 후보 + Orange3 | v1 8주차 | 그대로 재사용(Orange3는 동일 CSV로 진행) |
| 9 | 머신러닝 예측 + Orange3 | v1 9주차(전면 교체) | **신규 데이터 필요** — `반도체_공정_샘플.csv` 계열로 교체, `fab.csv` 파생 데이터는 더 이상 핵심 경로에서 사용하지 않음 |
| 10 | 미니 프로젝트 | v1 10주차 | 기존 데이터에서 fab.csv 기반 요소만 제거하고 재사용 |

## 각 항목별 TODO (다음 세션에서 순서대로 진행 권장)

1. ~~**데이터 설계 개정**~~ — ✅ 완료. `docs/data-design.md`를 v2 주차 구성에 맞게 다시 썼다.
   - 2·3주차용 축소 데이터 스펙 확정(`week02_python_basics_1.csv`, `week03_python_basics_2.csv`)
   - 7주차 병합 데이터 스펙 확정(`week07_equipment_yield.csv` — v1 6·7주차 열 병합)
   - 9주차 신규 데이터 스펙 확정(`week09_pass_fail_train.csv` + `week09_new_lots_to_predict.csv`,
     `반도체_공정_샘플.csv` 계열, fab.csv 미사용, seed 규칙 유지)
   - 10주차 데이터에서 fab.csv 기반 열/패턴 제거(원래도 fab.csv 열을 쓰지 않았으므로 명시만 추가)
   - **아직 안 한 것**: 이 스펙대로 실제 CSV를 생성하는 스크립트 작업(TODO 2)은 착수 전.
2. ~~**`scripts/generate_weekly_data.py` 개정**~~ — ✅ 완료. `gen_week02()`~`gen_week09()`를 v2 스펙에
   맞게 재작성하고 `python scripts/generate_weekly_data.py`로 `data/weekly/`를 재생성했다. 기존 시드
   규칙(`seed = 100 + 주차번호`)과 `utf-8-sig` 저장 규칙은 그대로 유지했다.
   - **과도기 상태(의도적)**: `week02`~`week07`, `week09` 폴더에는 v1 시절 파일명(예:
     `week02_basic_process_values.csv`, `week06_equipment_comparison.csv`,
     `week09_fab_beginner.csv` 등)이 새 v2 파일과 **함께 남아 있다**. `lectures/`·`notebooks/`가
     아직 v1 파일명을 참조하므로, 지금 지우면 기존 강의자료가 바로 깨진다. TODO 3·5에서 해당 주차의
     강의자료·노트북을 v2로 재작성한 뒤 옛 파일을 정리한다.
   - fab.csv 기반 `SELECTED_SENSORS`/`BEGINNER_ALIAS`/`gen_week09()`의 fab 파생 로직은 스크립트에서
     완전히 제거했다(9주차는 이제 `반도체_공정_샘플.csv` 계열 신규 데이터만 생성).
3. 🔶 **`lectures/weekXX/` 재작성** — **개요(skeleton) 단계까지 완료.** 2·3·4·5·6·7·9·10주차의
   `index.html`을 v2 제목·학습 목표·다룰 이론/실습 목차·데이터 파일명만 채운 개요 페이지로
   교체했다(상세 설명·예제 코드·단계별 실습·퀴즈는 아직 없음 — 각 페이지 상단에 "작성 상태"
   안내 박스로 명시). 내용이 아직 확정 전이라 이동/수정 가능성이 있어 우선 목차 수준으로만
   배치하기로 결정(사용자 지시). 1주차는 이미 v2와 동일해 그대로 두었고, 8주차는 기존 상세
   내용을 유지한 채 Orange3 Correlations 절만 추가했다.
   - **아직 안 한 것**: worksheet.html·quiz.json·instructor-guide.md는 이번 라운드에서 건드리지
     않았다(2~7·9·10주차는 v1 시절 파일이 그대로 남아 있어 새 index.html과 내용이 어긋날 수 있음
     — 상세 콘텐츠를 확정할 때 함께 재작성 필요).
4. **Orange3 안내 자료 신규 작성** — 5·6·8·9주차 공통으로 쓸 "Orange3 설치 및 기본 사용법" 섹션(또는
   별도 부록 문서)이 필요하다. 설치 방법, 기본 화면 구성, File/Data Table/Scatter Plot/Correlations/
   Test and Score/Predictions 위젯 사용법을 다룬다. (각 주차 개요 페이지에는 어떤 위젯을 쓸지만
   1줄로 표시해뒀다.)
5. 🔶 **`notebooks/{student,instructor,solutions}/` 재작성** — **개요(skeleton) 단계까지 완료.**
   2·3·4·5·6·7·9·10주차의 student/instructor/solutions 노트북(24개)을 모두 마크다운 셀만으로
   구성된 개요로 교체했다 — 다룰 실습 단계 목록 + (해당 시) Orange3 메모 + 데이터 경로만 있고
   실제 코드 셀은 없다. `python scripts/validate_notebooks.py` 63건 모두 통과(코드 셀이 없어
   instructor/solutions 실행 체크도 trivial하게 통과, solutions에는 'TODO' 문자열 없음 확인).
   1·8주차 노트북은 건드리지 않았다(이미 v2 데이터와 호환).
   - **아직 안 한 것**: 실제 코드 셀(`# TODO` 빈칸 포함)과 실행 결과, 설명은 상세 내용 확정 후 작성.
6. **`data/data_dictionary/weekXX_dictionary.md` 재작성** — 데이터가 바뀌는 2·3·7·9·10주차는 새로
   쓰고, 나머지는 주차 번호만 맞춰 재배치한다. (아직 착수 전 — v1 그대로.)
7. **`fab.csv` 취급 방침** — `data/raw/fab.csv`는 삭제하지 않고 그대로 둔다(원본 읽기 전용 원칙
   유지). 다만 핵심 10주 경로에서는 참조하지 않으며, 원할 경우 강사용 "9주차 이후 심화 부록"으로만
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
- `index.html` — 주차 카드 제목/설명 갱신 + "진행 안내" 배너를 스켈레톤 단계에 맞게 갱신
- `CLAUDE.md` — fab.csv/9주차 관련 규칙을 v2 기준으로 일반화
- `docs/data-design.md` — v2 주차 구성에 맞게 전체 재작성(TODO 1 완료)
- `scripts/generate_weekly_data.py` — v2 스펙대로 재작성(TODO 2 완료)
- `data/weekly/week02`~`week10`(9주차 포함) — v2 스펙 CSV 생성(v1 파일은 과도기 동안 함께 보존)
- `scripts/validate_datasets.py` — v2 파일명·스펙 기준으로 갱신(TODO 8 중 데이터셋 검증만 완료)
- `lectures/week02,03,04,05,06,07,09,10/index.html` — 제목·학습목표·다룰 내용 개요만 담은 skeleton으로 교체(TODO 3 skeleton 단계 완료), `lectures/week08/index.html`에 Orange3 절 추가
- `notebooks/{student,instructor,solutions}/week{02,03,04,05,06,07,09,10}_*.ipynb`(24개) — 마크다운
  개요 skeleton으로 교체(TODO 5 skeleton 단계 완료)
- 저장소를 git으로 초기화하고(`git init`) v1 상태를 첫 커밋으로 보존(안전한 되돌리기용)

`data/data_dictionary/`와 각 주차의 `worksheet.html`·`quiz.json`·`instructor-guide.md`는 **아직 v1
상태 그대로**다. 다음 단계는 이번에 배치한 lectures/notebooks 개요(skeleton)를 사용자가 검토·확정한
뒤, 그 확정된 목차를 기준으로 상세 설명·예제 코드·퀴즈·데이터 설명서를 실제로 채우는 것이다.
