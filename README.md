# 반도체 및 반도체 공정 데이터 분석 10차시 과정

프로그래밍 경험이 거의 없는 일반인을 위한, 반도체 공정과 데이터 분석을 함께 배우는 10차시 교육 과정입니다.
모든 실습 데이터는 교육용으로 생성한 **가상 데이터**이며, 실제 기업의 생산 데이터가 아닙니다.

전체 목차는 [`index.html`](index.html)에서 확인할 수 있습니다.

## 1. 교육 대상

- 프로그래밍 경험이 거의 없는 일반인
- 반도체 산업에 관심이 있지만 데이터 분석은 처음인 사람
- 전문 데이터 과학자가 아니라, "데이터로 공정 상태를 설명할 수 있는 사람"이 되고 싶은 학습자

## 2. 교육 목표

10차시 과정을 마치면 다음을 할 수 있습니다.

- 반도체·웨이퍼·공정의 기본 개념을 설명한다.
- 변수·리스트·딕셔너리·조건문·반복문·함수 등 파이썬 기초를 익힌다.
- Jupyter Notebook에서 CSV를 열고 Pandas로 조회·정리한다.
- 결측값·중복값·이상값을 찾고 정제한다.
- 그래프로 공정 상태를 확인하고 설비별·공정별 차이를 비교한다.
- 수율과 불량률을 계산하고, 공정 이상의 원인 후보를 데이터로 탐색한다.
- 간단한 머신러닝으로 합격/불합격을 예측하는 모델을 직접 만들고, 새 데이터를 예측해본다.
- Orange3에서 위젯을 이어 같은 데이터를 코드 없이 살펴보고, 파이썬 결과와 비교한다.
- 분석 결과를 비전공자도 이해할 수 있는 문장으로 설명한다.

## 3. 10차시 전체 목차 (v3)

### 수업 구조

매 차시는 세 부분으로 진행합니다. 강의 HTML에는 PART마다 앵커(`#part1`·`#part2`·`#part3`)가 있습니다.

| | 1~8차시 | 9·10차시 (순서 예외) |
| --- | --- | --- |
| PART 1 | **파이썬** — 생활 예제로 개념 → 반도체 데이터로 확인하기 | **Orange3** — 모델을 먼저 눈으로 본다 |
| PART 2 | **Orange3** — 워밍업 데이터 → 반도체 데이터 → 파이썬 결과와 비교 | **파이썬 최소 + ChatGPT 체험** — 같은 결과를 코드 몇 줄로 확인하고, AI가 준 코드·문장을 실제 숫자로 검증 |
| PART 3 | **실습지** — 파이썬 3문제 + Orange 1문제 + 해석 문장 1 | **실습지** — 파이썬 2문제 + Orange 2문제 + 해석 문장 1 |

9·10차시는 모델을 먼저 Orange3 화면으로 본 뒤 코드로 확인하도록 PART 1과 PART 2의 순서를 바꿨습니다.

### 차시별 내용

| 차시 | 제목 | 파이썬 | Orange3(워밍업 → 반도체) |
| --- | --- | --- | --- |
| 1 | 반도체 공정과 데이터 처음 만나기 + 변수·출력 | `=`, `print`, f-string, `type` | 우리 동네 인구 → 공정 기록 (File, Data Table, Distributions) |
| 2 | 리스트와 딕셔너리 | 리스트·인덱스, `len`/`append`, `max`/`min`/`sum`, 딕셔너리 | 지하철 역별 승하차 → 설비 온도 (Column Statistics) |
| 3 | 리스트·딕셔너리로 배우는 조건문·반복문·함수 | `if`/`else`, `for`로 세기, `def` 하나 | 우리 동네 대기환경 → 기록 30건 (Select Rows) |
| 4 | Pandas 가장 기본적인 부분 | `read_csv`, 열 선택, 조건 검색, `sort_values` | 반도체 8대 공정 흐름표 → 공정 기록 100건 (Select Columns) |
| 5 | 데이터 훑어보기와 정리(EDA) | `describe`, `isna().sum()`, `dropna`, `drop_duplicates` | 클린룸 환경 모니터링 → 지저분한 공정 기록 (Impute) |
| 6 | 그래프로 공정 상태 이해하기 | 그래프 틀, 막대, 히스토그램, 산점도 | 웨이퍼 맵 한 장 → 공정 기록 180건 (Scatter Plot, Box Plot) |
| 7 | 설비·공정 비교와 수율·불량 분석 | 비교로 새 열, `groupby().mean()` | 식각 설비 3대의 웨이퍼 12장 → 설비·수율 (Pivot Table) |
| 8 | 공정 이상과 원인 후보 찾기 | `corr`, 상관계수 읽기, 범위 밖 조건 | 식각 챔버 센서 기록 → 이상·원인 후보 (Correlations) |
| 9 | 머신러닝 예측 모델 만들기 | Feature/Label, `train_test_split`, `fit`, `accuracy_score` | 웨이퍼 맵 패턴 분류 → 합격/불합격 학습 데이터 (Tree, Tree Viewer, Test and Score, Confusion Matrix) |
| 10 | 모델 평가와 새 데이터 예측 | `predict` | 웨이퍼 패턴 + 새 웨이퍼 10장 → 새 로트 9개 (kNN, Logistic Regression, Predictions) |

자세한 설계 근거는 [`docs/curriculum.md`](docs/curriculum.md), v1 → v2 → v3 변경 배경은
[`docs/restructure-plan.md`](docs/restructure-plan.md), 데이터 생성 규칙은
[`docs/data-design.md`](docs/data-design.md), 전체 용어는 [`docs/glossary.md`](docs/glossary.md)를 참고하세요.

## 4. 폴더 구조

```text
semiconductor-data-analysis-course/
├─ index.html                 # 전체 과정 목차
├─ README.md, CLAUDE.md, requirements.txt
├─ assets/                    # 공통 CSS/JS/이미지(Orange 화면 캡처는 assets/images/orange3/)
├─ data/
│  ├─ raw/                    # 원본 CSV(읽기 전용, 수정 금지)
│  ├─ processed/
│  ├─ weekly/week01~week10/   # 차시별 실습 데이터(CSV)
│  │  └─ orange/              # 같은 데이터를 Orange용으로 바꾼 .tab 파일
│  └─ data_dictionary/        # 차시별 데이터 설명서
├─ notebooks/
│  ├─ student/                # 학생용(TODO 포함)
│  └─ solutions/              # 정답본(완성본, 강사 시연용)
├─ orange3/week01~week10/     # Orange 워크플로(_start.ows / _done.ows)
├─ lectures/week01~week10/    # HTML 강의자료, 실습지, 퀴즈, 운영안
├─ scripts/                   # 데이터·그림·워크플로·노트북 생성과 검증 스크립트
├─ reports/                   # 원본 데이터 분석, 검증 리포트
└─ docs/                      # 커리큘럼, Orange3 안내, 용어집, 운영 가이드
```

## 5. 개발 환경(과정 제작·검증용)

수강생 실습 환경에는 프로그램과 실습 파일이 이미 준비돼 있습니다. 아래는 이 저장소의 데이터·노트북을 다시 만들고 검증할 때만 필요합니다.

```bash
python -m venv .venv
# Windows: .venv\Scriptsctivate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Jupyter에서 노트북을 실행하려면 커널을 등록하세요.
python -m ipykernel install --user --name python3 --display-name "Python 3"
```

Orange3의 캔버스 화면 구성, 위젯을 놓고 연결하는 법, 차시별로 쓰는 위젯과 그 위젯이 들어 있는 묶음은
[`docs/orange3-guide.html`](docs/orange3-guide.html)에 정리했습니다.

## 6. 파일 여는 법

노트북은 CSV 파일 이름만 쓰므로 CSV가 노트북과 같은 곳에 있어야 합니다. 저장소의 `notebooks/` 폴더에서 바로 열면 CSV가 없어
오류가 나며, 검증 스크립트는 CSV를 임시 폴더에 모아 그곳에서 실행합니다.

### Orange 워크플로(.ows) 열기

- `orange3/weekXX/`에는 차시마다 워크플로 4개가 있습니다. ① 워밍업 데이터, ② 반도체 데이터 각각
  `_start.ows`(데이터가 연결된 File 위젯 하나 + 한국어 안내 메모)와 `_done.ows`(완성본)입니다.
  수업은 `_start.ows`에서 시작하고, 막히면 `_done.ows`를 열어 따라잡습니다.
- `.ows` 파일을 더블클릭합니다. 열리지 않으면 Orange를 먼저 실행하고 **File → Open**에서 고릅니다.
- File 위젯에 "파일을 찾을 수 없다"는 오류가 나면 `.ows`를 원래 폴더에서 다시 열고, 그래도 안 되면 File 위젯의
  폴더 아이콘으로 `orange` 폴더의 `.tab` 파일을 직접 고릅니다.

### `data/weekly/weekXX/orange/*.tab`

Orange가 여는 데이터입니다. 같은 차시 CSV에서 생성 스크립트가 만든 파생 파일로 값은 CSV와 같고, 열마다 Orange가 쓸 종류
(숫자·범주·결과 열·참고용 meta)가 정해져 있습니다. 예를 들어 `합격여부`는 숫자가 아니라 범주(결과 열)로 읽혀 Orange가
합격·불합격 막대를 바로 그립니다. 직접 고치지 말고 CSV 생성 로직을 고친 뒤 다시 생성합니다.
Orange 내장 데이터(zoo·iris·titanic 등)는 쓰지 않고, 워밍업도 직접 만든 가상 데이터(`weekXX_orange_<주제>.csv`)만 씁니다.

## 7. 스크립트

모든 차시 데이터와 그림은 시드가 고정된 스크립트로 재현 가능하게 생성됩니다. 원본 CSV(`data/raw/`)는
절대 덮어쓰지 않습니다.

| 스크립트 | 하는 일 |
| --- | --- |
| `scripts/inspect_raw_data.py` | 원본 데이터 프로파일링(읽기 전용) |
| `scripts/generate_weekly_data.py` | 차시별 실습 데이터(CSV)와 Orange용 `.tab` 재생성(`data/weekly/*`, `utf-8-sig`) |
| `scripts/validate_datasets.py` | 데이터 검증 |
| `scripts/generate_figures.py` | 강의용 이해 그림(공정 흐름도·웨이퍼 맵 등)을 데이터에서 생성(`assets/images/generated/`) |
| `scripts/build_orange_workflows.py` | 차시별 `_start.ows`·`_done.ows` 생성(Orange 파이썬으로 실행) |
| `scripts/validate_orange_workflows.py` | `.ows` 파싱·상대경로·데이터 로드·화면 없이 위젯 실행 검증 |
| `scripts/notebook_builders/weekXX.py` | 학생용·정답 노트북 2종을 한 정의에서 생성(노트북 JSON은 손으로 고치지 않음) |
| `scripts/validate_notebooks.py` | 노트북 실행 검증 |
| `scripts/build_data_dictionary_html.py` | 데이터 설명서 `.md` → 강의 디자인 `.html` 변환 |

```bash
python scripts/generate_weekly_data.py
python scripts/validate_datasets.py
python scripts/generate_figures.py
python scripts/build_orange_workflows.py      # Orange 파이썬으로 스스로 다시 실행된다
python scripts/validate_orange_workflows.py
python scripts/notebook_builders/week01.py    # 차시마다
python scripts/validate_notebooks.py
```

## 8. HTML 강의 자료 실행 방법

`index.html`을 브라우저로 열면 전체 목차로 이동할 수 있습니다. 별도 서버 없이 파일을 직접 열어도
핵심 내용이 모두 표시되도록 만들어졌습니다(이미지·CSS·JS는 모두 상대경로의 로컬 파일).

```bash
# 예: 기본 브라우저로 열기(Windows)
start index.html
```

## 9. 강사용 자료와 학생용 자료의 차이

| 구분 | 위치 | 특징 |
| --- | --- | --- |
| 학생용 | `notebooks/student/` | 맨 위 "막혔을 때" 안내, 반도체 실습 문제가 `____` 빈칸으로 비어 있어 직접 채워야 함 |
| 정답 | `notebooks/solutions/` | 학생용의 모든 빈칸이 채워진 완성본(실행 결과 저장). 강사 시연에도 사용 |
| Orange 워크플로 | `orange3/weekXX/` | `_start.ows`로 시작, `_done.ows`는 완성본(따라잡기·정답) |
| 강의 운영안 | `lectures/weekXX/instructor-guide.md` | 수업 흐름(순서와 "여기서 쉬기"), 발문, 예상 오개념 |
| 공통 운영 가이드 | [`docs/instructor-operation-guide.md`](docs/instructor-operation-guide.md) | 전 차시 공통 v3 운영 방법 |

## 10. 데이터 출처 및 교육용 가공 안내

- 원본 참고 자료: `반도체_공정_샘플.csv`(200행), `fab.csv`(1,567행 × 590센서, SECOM 유형의
  고차원 센서 데이터)를 `data/raw/`에 원본 그대로 보존했습니다.
- 1~10차시 핵심 데이터는 모두 `반도체_공정_샘플.csv`의 열 구조·값 범위를 참고해 **완전히 새로
  생성한 가상 데이터**입니다. 9차시 머신러닝 예측 실습도 `반도체_공정_샘플.csv` 계열 데이터를
  사용합니다(`fab.csv` 파생 데이터는 핵심 경로에서 제외 — 배경은
  [`docs/restructure-plan.md`](docs/restructure-plan.md) 참고).
- Orange 워밍업 데이터(`weekXX_orange_<주제>.csv`)도 시드를 고정해 직접 만든 가상 데이터입니다.
  열 이름은 한국어 이름 + 영문/SI 단위(`온도_C`, `PM10_ug_m3`, `승차인원_count` 등)로 씁니다.
- `fab.csv`는 원할 경우 강사가 9차시 이후 선택 심화 부록으로만 다룰 수 있으며, 이 경우에도 센서
  이름에는 실제 의미가 확인되지 않았다는 점을 반드시 명시해야 합니다(`CLAUDE.md` 참고).
- 실습 데이터의 `합격여부`는 전 차시 1=합격/-1=불합격입니다. `fab.csv`의 부호(-1=정상/1=이상)와
  서로 다르다는 점은 용어집에서 설명합니다.

## 11. 주의사항

- 이 과정은 전문 데이터 과학자 양성이 아니라, 반도체 공정 데이터를 스스로 열어보고 해석할 수 있는
  능력을 기르는 것을 목표로 합니다.
- 모든 상관관계·예측 결과는 "원인 후보"로 조심스럽게 표현하며, 확정된 인과관계로 단정하지 않습니다.
- 실습 데이터는 교육 목적의 가상 데이터이므로, 실제 현업 의사결정에 사용해서는 안 됩니다.

## 12. 라이선스 안내

이 교육 자료와 생성된 실습 데이터는 교육 목적으로 자유롭게 사용·수정할 수 있습니다.
`data/raw/`의 원본 CSV는 별도로 제공받은 참고 자료이므로, 재배포 전 출처 및 사용 조건을 확인하세요.
