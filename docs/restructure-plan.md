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
2. **`scripts/generate_weekly_data.py` 개정** — 위 스펙에 맞게 `gen_week02()`~`gen_week10()` 재작성.
   기존 시드 규칙(`seed = 100 + 주차번호`)과 `utf-8-sig` 저장 규칙은 그대로 유지.
3. **`lectures/weekXX/` 재작성** — v2 순서에 맞게 각 주차 HTML(18섹션)·worksheet·quiz·instructor-guide를
   다시 쓴다. 기존 v1 8주차(`instructor-guide.md`, `quiz.json`)는 새 8주차와 내용이 거의 겹치므로
   재사용 비중이 크다.
4. **Orange3 안내 자료 신규 작성** — 5·6·8·9주차 공통으로 쓸 "Orange3 설치 및 기본 사용법" 섹션(또는
   별도 부록 문서)이 필요하다. 설치 방법, 기본 화면 구성, File/Data Table/Scatter Plot/Correlations/
   Test and Score/Predictions 위젯 사용법을 다룬다.
5. **`notebooks/{student,instructor,solutions}/` 재작성** — 주차 번호와 내용이 바뀌므로 전체 재작성이
   필요하다. 9주차는 `fab.csv` 대신 새 데이터로 `train_test_split`~`predict()`까지 다시 구성한다.
6. **`data/data_dictionary/weekXX_dictionary.md` 재작성** — 데이터가 바뀌는 2·3·7·9·10주차는 새로
   쓰고, 나머지는 주차 번호만 맞춰 재배치한다.
7. **`fab.csv` 취급 방침** — `data/raw/fab.csv`는 삭제하지 않고 그대로 둔다(원본 읽기 전용 원칙
   유지). 다만 핵심 10주 경로에서는 참조하지 않으며, 원할 경우 강사용 "9주차 이후 심화 부록"으로만
   별도 언급한다. 이 부록을 다룰 때도 `CLAUDE.md`의 "Sensor0~589 실제 의미 단정 금지" 규칙은 그대로
   적용한다.
8. **검증 스크립트 갱신** — `scripts/validate_datasets.py`, `scripts/validate_notebooks.py`의 주차별
   체크 항목을 새 데이터/노트북 구성에 맞게 갱신한다.
9. **`README.md` / `index.html` / `CLAUDE.md`** — 이번 세션에서 curriculum.md와 함께 1차 갱신했다.
   실제 콘텐츠가 재작성되는 대로 세부 문구(파일명, 통계 수치 등)를 다시 맞춘다.

## 지금까지 실제로 변경한 파일

- `docs/curriculum.md` — v2 전체 재작성(이 문서가 가리키는 최신 구성)
- `docs/restructure-plan.md` — 신규 작성(이 문서)
- `README.md` — 목차 표·교육 목표 문구 갱신
- `index.html` — 주차 카드 제목/설명 갱신
- `CLAUDE.md` — fab.csv/9주차 관련 규칙을 v2 기준으로 일반화
- `docs/data-design.md` — v2 주차 구성에 맞게 전체 재작성(TODO 1 완료)

`lectures/`, `notebooks/`, `data/weekly/`, `data/data_dictionary/`, `scripts/generate_weekly_data.py`는
**아직 v1 상태 그대로**다. 다음 단계는 TODO 2(`scripts/generate_weekly_data.py` 개정 및 실제 CSV
재생성)이며, 그 다음 세션에서 이어서 진행한다.
