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
- Google Colab/Jupyter에서 CSV를 열고 Pandas로 조회·정리한다.
- 결측값·중복값·이상값을 찾고 정제한다.
- 그래프로 공정 상태를 확인하고 설비별·공정별 차이를 비교한다.
- 수율과 불량률을 계산하고, 공정 이상의 원인 후보를 데이터로 탐색한다.
- 간단한 머신러닝으로 합격/불합격을 예측하는 모델을 직접 만들고, 새 데이터를 예측해본다.
- Orange3로 같은 분석을 코드 없이 다시 확인하며 개념을 다진다.
- 분석 결과를 비전공자도 이해할 수 있는 문장으로 설명한다.

## 3. 10차시 전체 목차 (v2)

> 최초 설계(v1) 대비 앞부분에 파이썬 기초 2차시를 추가하고, 마지막 예측 실습은 `fab.csv` 대신
> `반도체_공정_샘플.csv` 계열 데이터로 단순화했다. 변경 배경과 v1→v2 매핑은
> [`docs/restructure-plan.md`](docs/restructure-plan.md)를 참고하세요.

| 차시 | 제목 | 핵심 주제 |
| --- | --- | --- |
| 1 | 반도체 공정과 데이터 처음 만나기 | 반도체/웨이퍼 개념, Colab, Pandas 첫 조회 |
| 2 | 파이썬 기초 Ⅰ | 변수·자료형·리스트·딕셔너리 |
| 3 | 파이썬 기초 Ⅱ | 조건문·반복문·함수 |
| 4 | Pandas로 공정 데이터 읽고 선택하기 | read_csv, 열 선택, 조건 검색, 정렬 |
| 5 | 결측값과 이상한 데이터 정리하기 | 결측값·중복값·이상값 정제 + Orange3로 훑어보기 |
| 6 | 그래프로 공정 상태 이해하기 | 선/막대/히스토그램/산점도/박스플롯 + Orange3 시각화 |
| 7 | 설비·공정 비교와 수율·불량 분석 | groupby 집계, 수율/불량률, 파레토 |
| 8 | 공정 이상과 원인 후보 찾기 | 이상탐지, 상관관계 + Orange3 Correlations |
| 9 | 머신러닝으로 합격/불합격 예측하기 | 반도체_공정_샘플.csv 기반 분류 모델, 예측 체험 + Orange3 |
| 10 | 반도체 공정 데이터 분석 미니 프로젝트 | 종합 프로젝트, 최종 보고서 |

자세한 설계 근거는 [`docs/curriculum.md`](docs/curriculum.md), v1→v2 재구성 계획은
[`docs/restructure-plan.md`](docs/restructure-plan.md), 데이터 생성 규칙(현재 v1 기준, 개정 예정)은
[`docs/data-design.md`](docs/data-design.md), 전체 용어는 [`docs/glossary.md`](docs/glossary.md)를 참고하세요.

## 4. 폴더 구조

```text
semiconductor-data-analysis-course/
├─ index.html                 # 전체 과정 목차
├─ README.md, CLAUDE.md, requirements.txt
├─ assets/                    # 공통 CSS/JS/이미지
├─ data/
│  ├─ raw/                    # 원본 CSV(읽기 전용, 수정 금지)
│  ├─ processed/
│  ├─ weekly/week01~week10/   # 차시별 실습 데이터
│  └─ data_dictionary/        # 차시별 데이터 설명서
├─ notebooks/
│  ├─ student/                # 학생용(TODO 포함)
│  ├─ instructor/             # 강사 시연용(완성본 + 설명)
│  └─ solutions/               # 정답본(완성본)
├─ lectures/week01~week10/    # HTML 강의자료, 실습지, 퀴즈, 운영안
├─ scripts/                   # 데이터 생성·검증 스크립트
├─ reports/                   # 원본 데이터 분석, 검증 리포트
└─ docs/                      # 커리큘럼, 데이터 설계, 용어집, 운영 가이드
```

## 5. Python 환경 설치 방법

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Jupyter에서 노트북을 실행하려면 커널을 등록하세요.
python -m ipykernel install --user --name python3 --display-name "Python 3"
```

### Orange3 설치 (5~10차시용)

Orange3는 클릭만으로 데이터를 분석하는 별도 데스크톱 프로그램으로, 파이썬 패키지와는 독립적으로
설치합니다.

```bash
pip install orange3
python -m Orange.canvas   # 설치 후 실행
```

또는 [orangedatamining.com](https://orangedatamining.com)에서 운영체제별 설치 파일을 내려받아 설치할
수도 있습니다. 설치 이후 캔버스 화면 구성, 위젯을 놓고 연결하는 법, 5~10차시에서 실제로 쓰는 위젯
(File, Data Table, Feature Statistics, Scatter Plot, Box Plot, Distributions, Bar Chart,
Correlations, Tree, Test and Score, Predictions) 사용법은
[`docs/orange3-guide.html`](docs/orange3-guide.html)에 한 곳에 정리했습니다. 차시별로 어떤 위젯을
"먼저" 쓰는지는 [`docs/curriculum.md`](docs/curriculum.md)의 5~10차시 설명을 참고하세요.

## 6. Google Colab 사용 방법

1. [colab.research.google.com](https://colab.research.google.com)에 접속해 새 노트북을 만들거나,
   `notebooks/student/weekXX_student.ipynb`를 업로드합니다(파일 → 노트북 업로드).
2. 왼쪽 폴더 아이콘 → 업로드 아이콘을 눌러 해당 차시의 CSV
   (`data/weekly/weekXX/*.csv`)를 업로드합니다.
3. 노트북 안의 `pd.read_csv("../../data/weekly/...")` 경로를 Colab에서는
   파일명만 있는 상대경로(예: `"week01_semiconductor_process_overview.csv"`)로 바꿔서 실행하세요.

## 7. Jupyter Notebook(로컬) 사용 방법

```bash
jupyter notebook notebooks/student/week01_student.ipynb
```

로컬 실행 시에는 노트북 안의 상대경로(`../../data/weekly/...`)가 그대로 작동합니다
(저장소 구조를 그대로 유지한 채 실행해야 합니다).

## 8. 실습 데이터 생성 방법

모든 차시 데이터는 시드가 고정된 스크립트로 재현 가능하게 생성됩니다. 원본 CSV(`data/raw/`)는
절대 덮어쓰지 않습니다.

```bash
python scripts/inspect_raw_data.py       # 원본 데이터 프로파일링(읽기 전용)
python scripts/generate_weekly_data.py   # 차시별 실습 데이터 재생성(data/weekly/*)
python scripts/validate_datasets.py      # 데이터 검증
python scripts/validate_notebooks.py     # 노트북 실행 검증
```

## 9. HTML 강의 자료 실행 방법

`index.html`을 브라우저로 열면 전체 목차로 이동할 수 있습니다. 별도 서버 없이 파일을 직접 열어도
핵심 내용이 모두 표시되도록 만들어졌습니다(이미지·CSS·JS는 모두 상대경로의 로컬 파일).

```bash
# 예: 기본 브라우저로 열기(Windows)
start index.html
```

## 10. 강사용 자료와 학생용 자료의 차이

| 구분 | 위치 | 특징 |
| --- | --- | --- |
| 학생용 | `notebooks/student/` | 핵심 코드 일부가 `# TODO`로 비어 있어 직접 채워야 함 |
| 강사용 | `notebooks/instructor/` | 완성된 코드 + 예상 결과 + 설명 포인트 + 오류 대처법 |
| 정답 | `notebooks/solutions/` | 학생용의 모든 TODO가 채워진 완성본 |
| 강의 운영안 | `lectures/weekXX/instructor-guide.md` | 수업 흐름, 발문, 예상 오개념, 난이도별 과제 |

## 11. 데이터 출처 및 교육용 가공 안내

- 원본 참고 자료: `반도체_공정_샘플.csv`(200행), `fab.csv`(1,567행 × 590센서, SECOM 유형의
  고차원 센서 데이터)를 `data/raw/`에 원본 그대로 보존했습니다.
- 1~10차시 핵심 데이터는 모두 `반도체_공정_샘플.csv`의 열 구조·값 범위를 참고해 **완전히 새로
  생성한 가상 데이터**입니다. 특히 9차시 머신러닝 예측 실습도 `반도체_공정_샘플.csv` 계열 데이터를
  사용합니다(v1에서 사용하던 `fab.csv` 파생 데이터는 v2에서 핵심 경로에서 제외 — 배경은
  [`docs/restructure-plan.md`](docs/restructure-plan.md) 참고).
- `fab.csv`는 원할 경우 강사가 9차시 이후 선택 심화 부록으로만 다룰 수 있으며, 이 경우에도 센서
  이름에는 실제 의미가 확인되지 않았다는 점을 반드시 명시해야 합니다(`CLAUDE.md` 참고).
- 반도체_공정_샘플.csv의 합격/불합격 부호(1=합격/-1=불합격)와 fab.csv의 부호(-1=정상/1=이상)가
  서로 다르다는 점은 1차시와 용어집에서 설명합니다.

## 12. 주의사항

- 이 과정은 전문 데이터 과학자 양성이 아니라, 반도체 공정 데이터를 스스로 열어보고 해석할 수 있는
  능력을 기르는 것을 목표로 합니다.
- 모든 상관관계·예측 결과는 "원인 후보"로 조심스럽게 표현하며, 확정된 인과관계로 단정하지 않습니다.
- 실습 데이터는 교육 목적의 가상 데이터이므로, 실제 현업 의사결정에 사용해서는 안 됩니다.

## 13. 라이선스 안내

이 교육 자료와 생성된 실습 데이터는 교육 목적으로 자유롭게 사용·수정할 수 있습니다.
`data/raw/`의 원본 CSV는 별도로 제공받은 참고 자료이므로, 재배포 전 출처 및 사용 조건을 확인하세요.
