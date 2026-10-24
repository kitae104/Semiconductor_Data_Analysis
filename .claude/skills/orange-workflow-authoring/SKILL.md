---
name: orange-workflow-authoring
description: 차시별 Orange3 워크플로(orange3/weekXX/*.ows)와 Orange용 데이터(data/weekly/weekXX/orange/*.tab)를 만들거나 고칠 때 반드시 사용한다. 새 차시의 _start/_done 워크플로를 추가하거나, 위젯 체인·설정(Distributions 변수, Select Rows 조건, Impute 방법)을 바꾸거나, File 위젯 경로가 다른 PC에서 깨지거나, Orange에서 합격여부가 숫자로 보이거나 열 이름에 BOM이 붙거나, validate_orange_workflows.py 실패를 고칠 때 사용할 것. Orange 3.35.0 기준. notebook-engineer 에이전트의 스킬.
---

# Orange3 워크플로 작성

Orange 3.35.0(이 PC 설치본) 기준으로 만들고 검증한다. `.ows`는 손으로 만들거나 Orange 화면에서 저장해
커밋하지 않는다. **`scripts/build_orange_workflows.py`의 선언형 정의(`WORKFLOWS`)에서 생성한다.**
Orange 화면에서 저장하면 File 경로가 그 PC의 절대경로로 바뀌어 다른 PC에서 깨진다(옛 `orange3/ch05~07.ows`가
`C:/Users/USER/Downloads/...`를 담고 있어 삭제한 이유).

## 파일 배치

| 무엇 | 경로 | 누가 만드나 |
|---|---|---|
| 워크플로 | `orange3/weekXX/weekXX_<N>_<주제>_start.ows`, `_done.ows` | `build_orange_workflows.py` |
| Orange용 데이터 | `data/weekly/weekXX/orange/<CSV와 같은 이름>.tab` | `generate_weekly_data.py`(CSV마다 자동) |
| Orange 워밍업 CSV | `data/weekly/weekXX/weekXX_orange_<주제>.csv` | `generate_weekly_data.py`의 `save_orange_warmup()` |
| 공통 도우미 | `scripts/_orange_env.py`(Orange 파이썬 찾기·재실행, 위젯 레지스트리) | — |

차시당 워크플로 2개(①워밍업 데이터, ②반도체 데이터) × start/done = `.ows` 4개가 기본이다.
번호는 고정이다. 워밍업이 아직 없어도 반도체 워크플로는 `_2_`로 둔다(나중에 ①을 넣어도 이름이 바뀌지 않게).
`<주제>`는 영문 소문자·숫자·밑줄(`cleanroom`, `dirty_process`). 검사 스크립트가 이름 규칙을 확인한다.

**Orange 내장 데이터(zoo·iris·titanic 등)는 쓰지 않는다**(2026-10-23 사용자 결정). 워밍업도 전부
`generate_weekly_data.py`가 만든 합성 데이터다 — 1~3차시는 생활 소재(인구·지하철·대기 환경 등),
4~10차시는 공정 관련 소재(클린룸 모니터링, 웨이퍼 맵 다이 격자 등). 코드에는 `sample()`/`sample-datasets`
지원이 남아 있지만 정의에서 쓰지 않는다.

## Orange 파이썬

프로젝트 `python`에는 Orange가 없다. Orange 전용 스크립트는 Orange 설치본의 파이썬으로 돈다.

- 기본 경로 `C:/Users/PC/AppData/Local/Programs/Orange/python.exe`(Python 3.9). 다른 PC는 환경변수 `ORANGE_PYTHON`.
- `python scripts/build_orange_workflows.py`처럼 프로젝트 `python`으로 실행해도 `_orange_env.ensure_orange_python()`이
  Orange 파이썬으로 스스로 다시 실행한다. `QT_QPA_PLATFORM=offscreen`이 기본이라 창이 뜨지 않는다.
- Orange 파이썬은 3.9다. 두 Orange 스크립트에서는 3.10+ 문법(`match`, `X | Y` 타입 표기)을 쓰지 않는다.

## 데이터: CSV가 아니라 .tab을 연다

Orange 3.35로 과정 CSV(`utf-8-sig`)를 그대로 열면 두 가지가 틀린다(실측).

1. 첫 열 이름에 BOM이 붙는다: `'\ufeff측정시간'`.
2. `합격여부`(1/-1)가 숫자(연속형)로 잡혀 Distributions가 히스토그램이 되고 목표 열로 쓸 수 없다.

그래서 `generate_weekly_data.py`의 `write_orange_tabs()`가 **모든 CSV를 저장한 뒤** 같은 이름의 `.tab`을 만든다.

- 저장된 CSV를 다시 읽어 **글자 그대로** 옮긴다(난수를 다시 뽑지 않는다). 기존 CSV는 한 바이트도 바뀌지 않는다.
- UTF-8(BOM 없음), 탭 구분, 결측은 빈 칸. Orange 3행 헤더(열 이름 / 형식 / 역할).
- 역할 규칙(같은 파일 맨 위 상수):

| 상수 | 열 | Orange에서 |
|---|---|---|
| `ORANGE_CLASS_COLUMNS` | 합격여부·진행여부·정답여부·평가·손님평가 | 범주형 목표(class), 값 순서 `1 -1`(좋은 쪽이 첫 막대·첫 색) |
| `ORANGE_META_COLUMNS` | 로트번호·웨이퍼번호·이름·주문번호·측정시간·날짜 | meta(표에 보이지만 분석·모델 입력에서 빠짐). ISO 날짜면 time, 아니면 문자열 |
| `ORANGE_RESULT_DETAIL_COLUMNS` | 불량유형·오답유형 | 범주형 meta. 불합격일 때만 값이 있어 입력에 두면 9·10차시 모델이 정답을 그대로 맞힌다(정답 누설) |
| (나머지) | 숫자 → `c`, 글자 → `d` | |
| `ORANGE_ROLE_OVERRIDES` | 파일별 예외 `{"파일이름": {"열": ("d", "meta")}}`. 예: 9차시 공정명·설비번호 → meta(파이썬 모델과 같은 숫자 6열) | |
| `ORANGE_COLUMN_RENAMES` | 차시별 열 이름 바꾸기 `{"week05": {"온도_섭씨": "온도_C"}}` — **.tab에만** 적용, CSV는 그대로. 역할 규칙·예외는 원래 이름과 바꾼 이름 어느 쪽으로도 찾는다. `validate_datasets.py`도 이 표를 읽어 비교한다. 현재 비어 있음 | |

- 결측이 있는 결과 열은 pandas가 `1.0/-1.0`으로 저장한다. `.tab`에는 `1/-1`로 정리해 쓴다.
- CSV를 지우면 남은 `.tab`도 지운다.
- **새 데이터의 열 이름은 "한글 이름_영문/SI 단위"** 로 짓는다: `기온_C`, `강수량_mm`, `승차인원_count`,
  `PM10_ug_m3`, `두께_nm`. 기존 CSV 열(`온도_섭씨` 등)은 차시별로 옮길 때 `ORANGE_COLUMN_RENAMES`(Orange 쪽)
  또는 생성기 수정(파이썬 쪽, 강의·노트북·데이터사전 파급 — `weekly-data-pipeline` 스킬)으로 바꾼다.
- 새 CSV는 따로 등록할 필요 없이 `write_orange_tabs()`가 `data/weekly/week*/`의 모든 CSV를 찾아 `.tab`을 만든다.
- 워밍업 데이터는 생성 함수를 만들어 `save_orange_warmup(df, "week02", "subway")`로 저장하고
  `ORANGE_WARMUP_GENERATORS`에 추가한다. 자기 시드(`np.random.default_rng(...)`)나 손으로 고정한 값만 쓴다.
  데이터사전과 `validate_datasets.py` 항목도 함께 추가한다(`weekly-data-pipeline` 스킬).

## 워크플로 추가하기

`build_orange_workflows.py`의 `WORKFLOWS`에 항목을 더한다. 코드 수정 없이 딕셔너리만 늘리면 된다.

```python
"week06": [
    {
        "n": 1, "topic": "cleanroom",
        "title": "6차시 ① 클린룸 모니터링 데이터로 그래프 맛보기",
        "nodes": [
            {"id": "file", "widget": FILE, "title": "File (파일 불러오기)",
             "data": weekly("week06", "week06_orange_cleanroom")},
            {"id": "scatter", "widget": SCATTER, "title": "Scatter Plot (산점도)",
             "settings": {"attr_x": "온도_C", "attr_y": "습도_pct"}},
        ],
        "links": [("file", "scatter")],
        "start_note": ["① File을 더블클릭해 ...", "② Visualize에서 Scatter Plot을 끌어 와 File과 이으세요."],
        "done_note": ["완성본: File → Scatter Plot(산점도)."],
    },
    # ② 반도체: "data": weekly("week06", "week06_process_visualization")
],
```

| 키 | 뜻 |
|---|---|
| `data` | File 노드만. `weekly("week05", "<CSV 이름에서 .csv 뺀 것>")`. (`sample(...)`은 Orange 내장용으로 남아 있지만 쓰지 않는다) |
| `settings` | 기본값과 다른 것만. 값이 열 이름 문자열이고 위젯 속성이 Variable이면 그 열로 바꿔 넣는다 |
| Select Rows | `{"conditions": [("압력_Pa", "is at least", ["0"]), ...]}` — 연산자 이름은 Orange 화면 글자 그대로 |
| Impute | `{"default_method": "Average", "methods": {"합격여부": "Drop"}}` — `Method` 이름(Leave, Average, Drop …) |
| `links` | `(보내는 id, 받는 id)`면 Orange가 제안하는 기본 연결. 출력을 골라야 하면 `(..., "Matching Data", "Data")` |
| `start` | `_start`에 남길 노드 id. 기본은 File 노드만 |
| `position` | 생략하면 자동 배치: File에서의 단계 수로 x, 첫째 자식은 부모와 같은 줄, 갈래는 아래 줄 |

새 위젯 별칭이 필요하면 파일 위쪽 상수에 정식 이름을 추가한다. 정식 이름은 Orange 파이썬에서 확인한다.

```bash
"$ORANGE_PYTHON" -c "import sys; sys.path.insert(0,'scripts'); from _orange_env import widget_registry; [print(w.name, '|', w.qualified_name) for w in widget_registry().widgets()]"
```

위젯 설정은 실제 위젯을 화면 없이 만들어 데이터를 넣고, 값을 바꾼 뒤 `settingsHandler.pack_data()`로
Orange와 같은 형식(Context 포함)으로 저장한다. 그래서 열 이름이 데이터에 없으면 생성 단계에서 바로 실패한다.
새 위젯 종류에 문자열·Variable로 표현되지 않는 설정이 필요하면 `ADAPTERS`에 함수 하나를 더한다
(`_apply_select_rows`, `_apply_impute` 참고).

## 경로 이식성 규칙

| 데이터 | 저장 형태 |
|---|---|
| 과정 데이터 | `RecentPath(abspath="<파일 이름만>", prefix="basedir", relpath="../../data/weekly/weekXX/orange/<이름>.tab")` |
| Orange 내장(지원만, 미사용) | `RecentPath(abspath="", prefix="sample-datasets", relpath="zoo.tab")` |

- `basedir`는 Orange가 워크플로를 열 때 **.ows 파일이 있는 폴더**로 정한다. `relpath`는 거기서부터 상대경로다.
  Orange는 스스로 `../`가 든 relpath를 쓰지 않지만, `RecentPath.resolve()`가 `os.path.join(basedir, relpath)`로
  찾으므로 동작한다(실측).
- `abspath`에 절대경로를 넣지 않는다. 파일 이름만 두면 경로를 못 찾았을 때 File 목록에 그 이름이 빨간색으로 보인다.
- 학생이 Orange에서 워크플로를 **다시 저장하면** 키트 밖 데이터는 절대경로로 바뀐다(Orange 동작). 그 PC에서는
  계속 열리지만 폴더를 옮기면 깨진다. 강의·운영안에는 "막히면 `_done.ows`를 다시 열기"로 안내한다.
- `.ows`의 relpath는 **`orange3/`와 `data/` 폴더 구조가 그대로일 때만** 동작한다(2026-10-25부터 학생용 키트 zip은 두지 않는다. 노트북은 CSV 파일 이름만 쓴다).

## start / done 규약

- `_start.ows`: File 위젯(데이터가 이미 들어 있음) + 캔버스 메모. 학생이 다음 위젯을 이어 붙인다.
- `_done.ows`: 위젯 체인 전체. 막혔을 때 따라잡기·정답.
- 두 파일은 같은 데이터를 연다(검사 항목).

## 캔버스 메모 문체

- 한 줄에 동작 하나, `①②③` 번호로 시작한다. 위젯은 "영어 이름(우리말 이름표)"로 쓴다: `Data Table(표 보기)`.
  노드 제목도 같은 형식이다: `File (파일 불러오기)`.
- 어디를 누르는지 쓴다: "더블클릭", "왼쪽 Data 묶음에서 끌어 와", "열 목록에서 합격여부를 고르세요".
- `_done` 메모는 "완성본:"으로 시작해 체인과 확인할 수치를 쓴다.
- 시간·분 표기를 쓰지 않는다. 이모지를 쓰지 않는다. 8~10차시는 "원인 후보" 표현을 쓴다.
- fab.csv(Sensor0~589)는 쓰지 않는다.

## 검증

```bash
python scripts/generate_weekly_data.py && git diff --stat data/weekly/   # 기존 CSV 불변(새 orange/ 파일만 생김)
python scripts/validate_datasets.py                                      # .tab 존재·BOM 없음·행 수·열·값이 CSV와 같음
python scripts/build_orange_workflows.py [--week N]
python scripts/validate_orange_workflows.py [--week N]                   # 파싱·위젯 목록·경로·데이터·위젯 기동·start/done 짝
```

`validate_orange_workflows.py`는 워크플로를 화면 없이 통째로 띄워 신호를 흘려 보내고, **연결선마다 흐른 행 수**를
출력한다. 강의·운영안에 적는 Orange 쪽 수치는 이 출력에서 가져온다(예: 5차시 ② 113 → 111 → 105행).
FAIL이 있으면 종료 코드 1.

## 실측한 함정

| 증상 | 원인 / 대처 |
|---|---|
| Orange에서 첫 열 이름이 `\ufeff측정시간` | CSV를 직접 열었다. `orange/*.tab`을 연다 |
| Distributions에 합격여부가 히스토그램으로 나옴 | 연속형으로 읽힘. `.tab` 헤더 `1 -1` + `class` |
| `Data Table → 다음 위젯`으로 이었더니 아무것도 안 나옴 | Data Table의 기본 출력은 `Selected Data`라 행을 고르기 전에는 비어 있다. **File에서 갈래로** 잇는다 |
| 5차시 `"식각 "`(뒤 공백 오타)가 Orange에서는 `식각`과 합쳐짐 | Orange 읽기가 앞뒤 공백을 지운다. pandas는 8종, Orange는 7종으로 보인다 |
| Impute에 중앙값이 없음 | 3.35의 Impute는 Average/Most frequent만 있다. 이상값이 있으면 평균이 끌려간다(예: 이상값 1720이 섞인 키 열에서 빈칸이 276.571로 채워져 ≤250 조건에 다시 걸려 지워짐). 평균은 Impute에 **들어온 전체 행**으로 계산한다 — 같은 위젯에서 `Drop`으로 지우는 행과 중복 행도 포함되므로 pandas에서 `dropna` 뒤에 구한 평균과 다르다. 강의·운영안에는 Orange가 실제로 보여 주는 값(276.571)만 쓴다 |
| 목표 열(합격여부)이 빈 행은 어떻게 되나 | 3.35 실측(깨끗한 설정): Impute(Average)는 목표 열 빈칸도 **최빈값으로 채운다**(5차시 113행 유지, 빈 합격여부 2칸이 "1"=합격 → Select Rows 뒤 107행). 파이썬 `dropna`처럼 지우려면 아래 개별 설정에서 그 열만 `Remove instances with unknown values`(빌더 `{"합격여부": "Drop"}`) → 111 → 105행. 위쪽 Default Method에서 Remove를 고르면 모든 열 기준으로 지워 104 → 98행 |
| 새 위젯인데 예전 설정이 되살아남(실측이 엇갈림) | 위젯은 바꾼 설정·"이 열 구성이면 이 설정" 문맥을 사용자 폴더에 저장해 같은 열 구성의 데이터가 오면 새 위젯에도 되살린다. 스크립트끼리 이 저장소가 섞이면 '새 위젯' 실측이 틀린다(2026-10-23 105/107 오측정). Orange 스크립트는 `_orange_env.isolate_widget_settings()`(임시 폴더)를 위젯 import 전에 부른다 — `ensure_orange_python()`이 자동으로 부른다. 실측 스크립트를 따로 쓰면 직접 부른다 |
| Select Rows 범위 조건과 빈칸 | 조건 열이 빈 행은 조건을 통과하지 못해 **지워진다**(5차시 Impute 없이 113 → 99 = 빈칸 8행 + 범위 밖 6행) |
| Select Rows가 빈 칸 행을 지움 | 범위 조건은 결측을 통과시키지 않는다. 빈 칸을 먼저 Impute하고 거른다 |
| 9·10차시 Tree 정확도가 비정상적으로 100% | 불량유형 같은 결과 열이 입력에 들어갔다. meta로 둔다 |
| 저장 시 "Using pickle fallback" 경고 | 위젯 설정(Context, RecentPath)은 파이썬 리터럴로 못 써서 Orange도 pickle로 저장한다. 정상이라 빌드 스크립트가 로그를 숨긴다 |
| 위젯 설정에 Method enum이 pickle됨 | `set_default_method(int(Method[...]))`처럼 int로 넣는다 |
| 검증에서 File이 데이터를 안 내보냄 | File은 `QTimer`로 늦게 읽는다. 이벤트 루프를 돌리며 조용해질 때까지 기다린다(검증 스크립트가 처리) |
| Test and Score 기본 교차검증이 5겹 | 3.35 위젯 기본값은 Number of folds = 5(목록 [2, 3, 5, 10, 20]의 셋째), random_state 42. 10겹이 필요하면 `settings`에 `n_folds: 3`(목록 번호)을 넣는다 |
| 생성 데이터 실측에 Orange 학습기가 필요할 때 | 위젯 기본값과 같은 학습기: `TreeLearner(binarize=True, max_depth=…, min_samples_leaf=2, min_samples_split=5, sufficient_majority=0.95)`, `KNNLearner(n_neighbors=5)`, `LogisticRegressionLearner(C=1)`, `CrossValidation(k=…, stratified=True, random_state=42)` |
| `python3`로 실행 실패 | Windows는 `python`(CLAUDE.md). Orange 스크립트는 자동으로 Orange 파이썬으로 다시 실행된다 |
