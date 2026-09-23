---
name: weekly-data-pipeline
description: 주차별 실습 데이터(data/weekly/weekXX/*.csv)와 데이터 설명서(data/data_dictionary/)를 만들거나 고칠 때 반드시 사용한다. CSV에 열을 추가·변경하거나, 새 차시 데이터를 만들거나, 결측값·이상값 같은 의도된 패턴을 심거나, generate_weekly_data.py를 수정하거나, validate_datasets.py 실패를 고칠 때 사용할 것. 시드 고정·재현성 규칙과 데이터사전 형식이 들어 있다. notebook-engineer 에이전트의 스킬.
---

# 주차 데이터 파이프라인

## 절대 규칙

1. **`data/raw/`는 읽기 전용이다**(CLAUDE.md). `반도체_공정_샘플.csv`(200행)와
   `fab.csv`(1,567행 × 590센서)는 절대 수정·덮어쓰기하지 않는다. 참조만 한다.
2. **CSV를 손으로 편집하지 않는다.** 모든 주차 데이터는 `scripts/generate_weekly_data.py`가
   만든다. 손편집한 값은 다음 재생성에서 사라지고, 그 사이 강의 자료의 숫자는 틀린 채 남는다.
3. **시드를 고정한다.** 몇 번을 돌려도 같은 데이터가 나와야 한다. 검증 스크립트가 해시로
   재현성을 확인한다.
4. **`utf-8-sig`로 저장한다.** `save_csv()`가 이미 그렇게 한다. 한글 열 이름을 Excel과
   Pandas 양쪽에서 열기 위한 인코딩이다.
5. **모든 데이터는 교육용 가상 데이터다.** 실제 생산 데이터처럼 서술하지 않는다.

## `generate_weekly_data.py` 구조

```
공통 상수      EQUIPMENT, PROCESS, SHIFT, DEFECT_TYPES
공통 헬퍼      save_csv(df, week, filename)   ← utf-8-sig 저장 + 로그
               lot_ids(rng, n)                ← LOT-0001 형식
               timestamps(rng, n, ...)        ← 정렬된 측정시간
차시별 생성기   gen_week01() … gen_week10()
main()         gen_week01~10 순차 호출
```

각 생성기는 같은 골격을 따른다. **시드는 `100 + 차시번호`** 다(week04 → `104`).

```python
def gen_week04():
    rng = np.random.default_rng(104)          # 시드 고정 — 차시마다 고유
    n = 100
    ts = timestamps(rng, n, periods_hours=800)
    equip = rng.choice(EQUIPMENT, size=n, p=[0.28, 0.28, 0.24, 0.20])
    temp = rng.normal(300, 4, size=n)

    # 의도한 패턴: EQ-02에 불합격이 몰리게 한다 — 학생이 조건 검색으로 "발견"할 대상
    fail_prob = np.where(equip == "EQ-02", 0.28, 0.09)
    passfail = np.array([rng.choice([1, -1], p=[1 - p, p]) for p in fail_prob])

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "설비번호": equip,
        "온도_섭씨": np.round(temp, 1),
        "합격여부": passfail,
    })
    save_csv(df, "week04", "week04_process_filtering.csv")
    return df
```

**`np.random.default_rng(시드)`만 쓴다.** `np.random.seed()`나 `random` 모듈을 섞으면
호출 순서에 따라 결과가 달라져 재현성이 깨진다.

## 데이터는 가르칠 것을 담는다

이 과정의 데이터는 무작위가 아니다. **각 차시가 발견하게 하려는 패턴을 의도적으로 심는다.**

| 차시 | 심는 패턴 | 학생이 발견하는 방법 |
|---|---|---|
| 4 | `EQ-02`에 불합격 집중 | 조건 검색 |
| 5 | 결측값, 중복행, 음수 압력 같은 이상값 | `isna()`, `duplicated()`, 조건 검색 |
| 6 | 설비별 온도 분포 차이 | 박스플롯, 히스토그램 |
| 7 | 설비·공정별 수율 차이, 불량 유형 편중 | `groupby`, 파레토 |
| 8 | 특정 변수와 불합격의 상관 | 상관계수, 산점도 |
| 9~10 | 분류 모델이 학습 가능한 신호 | 모델 학습·평가 |

패턴을 심을 때는 **너무 뚜렷하지도, 너무 약하지도 않게** 한다. 뚜렷하면 분석할 것이 없고,
약하면 학생이 "발견"에 실패해 수업이 무너진다. 심은 뒤 **실제 생성 결과를 확인**하고,
그 실제 수치를 데이터사전과 운영안에 적는다.

```bash
python -c "import pandas as pd; df=pd.read_csv('data/weekly/week04/week04_process_filtering.csv', encoding='utf-8-sig'); eq=df[df['설비번호']=='EQ-02']; print(len(eq), (eq['합격여부']==-1).sum())"
```

## 부호 규약

**섞으면 학생이 반드시 틀린다.**

| 데이터 | 규약 |
|---|---|
| `반도체_공정_샘플.csv` 계열(주차 데이터 대부분) | **1 = 합격, -1 = 불합격** |
| `fab.csv` | **-1 = 정상, 1 = 이상** (반대다) |

핵심 10차시는 `반도체_공정_샘플.csv` 계열을 쓴다. 두 규약의 차이는 1차시와 `docs/glossary.md`에서
설명한다. 새 데이터를 만들 때는 **1 = 합격** 쪽을 따른다.

`fab.csv`는 v2 핵심 경로에서 제외됐다(`docs/restructure-plan.md`). 선택 심화 부록에서 다루더라도
`Sensor0~Sensor589`의 **실제 물리적 의미를 단정하지 않는다**(CLAUDE.md).

## 데이터사전

`data/data_dictionary/weekXX_dictionary.md`. CSV마다 학생이 읽을 설명서다. 고정 형식:

```markdown
# {파일명}.csv 데이터 설명서

## 목적
(이 데이터로 무엇을 실습하는가)

## 가상 상황
(어떤 상황을 가정한 데이터인가)

## 행 하나의 의미
한 행 = (무엇 1건인지)

## 열 설명

| 열 이름 | 쉬운 설명 | 데이터 형식 | 단위 | 예시 | 결측값 가능 여부 |
| --- | --- | --- | --- | --- | --- |
| 온도_섭씨 | 챔버 온도 | 실수 | ℃ | 299.4 | 없음 |

## 정상 범위 (교육용 예시)
(각 수치 열의 정상 범위)

## 의도적으로 포함된 패턴
(무엇을 왜 심었는지 + **실제 생성 결과 수치**)

## 이번 차시 분석 질문
(이 데이터로 답할 질문들)

## 실제 현업 데이터와 다른 점
(가상 데이터임을 명시)
```

**CSV의 모든 열이 "열 설명" 표에 있어야 한다.** 검사 스크립트가 확인하고, 빠지면 WARN이다.
열을 추가하면 데이터사전을 함께 고친다 — 가장 자주 누락되는 작업이다.

"의도적으로 포함된 패턴"에는 **실제 생성 결과 수치**를 적는다. 설계 의도가 아니라 실제 값이다.

## 검증을 함께 갱신한다

`scripts/validate_datasets.py`는 차시별로 필수 열과 값 범위를 확인한다. 데이터 구조를 바꾸면
여기도 고친다. 안 고치면 검증이 옛 구조를 통과시키거나, 새 구조를 실패로 잡는다.

```python
w4 = validate_week("week04", "week04_process_filtering.csv",
                   ["측정시간", "로트번호", "설비번호", "공정명", "온도_섭씨", "압력_Pa", "가스유량_slm", "합격여부"])
if w4 is not None:
    check("week04 합격여부 값 범위", set(w4["합격여부"].unique()) <= {1, -1})
```

## 작업 절차

```bash
# 1. 현재 상태 확인
python -c "import pandas as pd; df=pd.read_csv('data/weekly/week04/week04_process_filtering.csv', encoding='utf-8-sig'); print(df.shape); print(df.dtypes); print(df.head())"

# 2. generate_weekly_data.py의 해당 gen_weekXX() 수정

# 3. 재생성 (전 차시가 다시 생성된다)
python scripts/generate_weekly_data.py

# 4. 의도치 않은 변경이 없는지 확인 — 고친 차시 외에 diff가 나오면 시드/순서가 깨진 것이다
git status --porcelain data/weekly/
git diff --stat data/weekly/

# 5. 데이터사전 갱신 (열 추가·변경 시, 실제 수치 반영)

# 6. 검증
python scripts/validate_datasets.py
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week 4 --quiet
```

4단계가 중요하다. **고치지 않은 차시의 CSV가 바뀌었다면 재현성이 깨진 것이다** — 공통 헬퍼를
고쳤거나 `main()`의 호출 순서가 바뀌었을 가능성이 높다. 되돌린다.

## 파급 추적

데이터를 바꾸면 따라와야 하는 것들. 팀에 먼저 알린 뒤 진행한다.

| 바뀐 것 | 함께 고칠 것 |
|---|---|
| 열 이름 | 노트북 3종, 강의 HTML 코드 블록, 실습지, 퀴즈, 데이터사전, `validate_datasets.py` |
| 행 수·분포 | 강의 본문 수치, 운영안 "핵심 수치", `result_prediction` 퀴즈 답, 데이터사전의 실제 결과 수치 |
| 파일명 | 위 전부 + 노트북 `read_csv` 경로 |
| 새 CSV 추가 | 데이터사전 신규 작성, `validate_datasets.py`에 항목 추가 |

## 실패했을 때

| 증상 | 원인 |
|---|---|
| 재생성할 때마다 결과가 달라짐 | 시드 미고정, `np.random.seed()` 혼용, 호출 순서 변경 |
| 고치지 않은 차시까지 diff | 공통 헬퍼 수정 또는 `main()` 순서 변경 |
| `UnicodeDecodeError` | `encoding="utf-8-sig"` 누락 |
| `KeyError` (첫 열만) | BOM. 읽을 때 `utf-8-sig`를 안 썼다 |
| 검증에서 값 범위 FAIL | 합격여부 부호가 `{1, -1}`이 아님 |
