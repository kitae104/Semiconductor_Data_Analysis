---
name: notebook-authoring
description: 학생용·강사용·정답 노트북 3종(notebooks/student|instructor|solutions/weekXX_*.ipynb)을 작성·수정할 때 반드시 사용한다. 노트북에 실습 단계를 추가하거나, TODO 빈칸을 만들거나, 코드 셀을 고치거나, 세 노트북의 내용을 맞추거나, validate_notebooks.py 실패를 고칠 때 사용할 것. 3종 대응 규칙, TODO 빈칸 규약, 경로·인코딩 규칙, 실행 검증 절차가 들어 있다. notebook-engineer 에이전트의 기본 스킬.
---

# 노트북 3종 작성

한 차시에는 노트북이 셋 있고, **같은 흐름을 공유한다.**

| 노트북 | 경로 | 성격 |
|---|---|---|
| 학생용 | `notebooks/student/weekXX_student.ipynb` | 핵심 코드가 `# TODO`/`____`로 비어 있다 |
| 정답 | `notebooks/solutions/weekXX_solution.ipynb` | 학생용의 모든 빈칸을 채운 완성본 |
| 강사용 | `notebooks/instructor/weekXX_instructor.ipynb` | 완성본 + 설명 포인트 + 예상 결과 + 어려워할 부분 |

셋이 어긋나면 수업 중에 강사와 학생이 다른 화면을 본다. **정답본은 학생용의 빈칸을 채운 것**이고,
**강사용은 거기에 설명을 더한 것**이다. 이 관계를 항상 유지한다.

## 단계 제목이 뼈대다

세 노트북 모두 `## N단계. {제목}` 형식의 마크다운 셀로 단계를 나눈다.
**단계 제목은 세 노트북에서 동일해야 한다.** 검사 스크립트가 학생용과 정답본의 단계 제목을
대조한다.

```markdown
## 1단계. 데이터 읽기
```

강사용은 같은 제목 아래 설명을 덧붙인다 — 제목 자체를 바꾸지 않는다.

```markdown
## 3단계. 열 선택하기
**어려워할 부분**: 여러 열 선택 시 대괄호 두 번(`[[ ]]`).
```

단계는 **강의 자료의 "실습 흐름"과 실습지 문제 순서에 대응**한다. 셋이 같은 순서여야
학생이 세 자료를 오가며 따라올 수 있다.

## TODO 빈칸 규약

학생용에만 빈칸이 있다. 두 가지 방식을 쓰고, 보통 함께 쓴다.

```python
# TODO: read_csv로 CSV 파일을 읽어 df에 저장하세요.
df = pd.____("../../data/weekly/week04/week04_process_filtering.csv", encoding="utf-8-sig")
```

| 규칙 | 이유 |
|---|---|
| `# TODO:` 주석으로 **무엇을 할지** 한국어로 적는다 | 빈칸만 있으면 무엇을 채워야 할지 모른다 |
| `____`(밑줄 4개)로 채울 자리를 표시한다 | 어디를 고쳐야 하는지 보인다 |
| **한 셀에 빈칸 1~2개**를 넘지 않는다 | 여러 개가 동시에 비면 어디서 틀렸는지 모른다 |
| 빈칸은 **그 단계의 핵심**만 | `import pandas as pd`를 비우지 않는다 |
| 빈칸이 아닌 부분은 그대로 실행되게 둔다 | 학생이 부분적으로라도 결과를 본다 |

**정답·강사 노트북에 `TODO`나 `____`가 남으면 검사에서 FAIL이다.** 반대로 학생용에 빈칸이
하나도 없어도 FAIL이다.

## 경로와 인코딩

노트북은 `notebooks/{종류}/`에서 실행되므로 데이터는 **`../../data/weekly/weekXX/`** 다.

```python
import pandas as pd

df = pd.read_csv("../../data/weekly/week04/week04_process_filtering.csv", encoding="utf-8-sig")
```

| 규칙 | 이유 |
|---|---|
| 상대경로만 쓴다 | 저장소를 어디에 두든 동작한다. 절대경로는 다른 PC에서 깨진다 |
| `encoding="utf-8-sig"` | 주차 CSV가 `utf-8-sig`로 저장돼 있다. 빼면 첫 열 이름에 BOM이 붙어 `KeyError`가 난다 |
| 한글 열 이름 | 대부분의 주차 CSV가 한글 열을 쓴다. `df["온도_섭씨"]` 형태 |

**그래프에 한글이 깨질 때**는 폰트를 지정한다. 이 과정은 한글 라벨을 쓴다.

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"   # Windows
plt.rcParams["axes.unicode_minus"] = False
```

## 코드는 강의 자료와 글자 단위로 같게

학생은 강의 화면을 보며 노트북을 친다. 둘이 다르면 수업이 멈춘다.

**노트북이 원본이다.** 여기서 코드를 확정하고 실제로 실행해 출력을 얻은 뒤,
그것을 content-writer에게 넘겨 강의 자료·운영안에 싣게 한다. 반대 순서로 하면 강의 자료의
코드가 돌지 않는 채로 배포된다.

`_workspace/03_notebook_report.md`에 확정 코드와 **실제 출력**을 함께 적는다.

## 데이터를 바꿔야 할 때

1. **`data/raw/`는 절대 수정하지 않는다**(CLAUDE.md). `반도체_공정_샘플.csv`, `fab.csv`는 읽기 전용.
2. CSV를 손으로 편집하지 않는다. **`scripts/generate_weekly_data.py`에 시드 고정 로직으로**
   추가·수정하고 재생성한다. 손편집한 데이터는 다음 재생성에서 사라진다.
3. 저장은 `utf-8-sig`.
4. 열을 바꾸면 **데이터사전**(`data/data_dictionary/weekXX_dictionary.md`)에 설명을 추가한다.
   검사가 CSV의 모든 열이 데이터사전에 나오는지 확인한다.
5. 파급을 팀에 알린다 — 강의 HTML 코드 블록, 실습지, 퀴즈, 운영안 수치, `validate_datasets.py`.

절차 상세는 `weekly-data-pipeline` 스킬을 읽는다.

## 실행 검증

**쓰고 나서 반드시 돌린다.** 이것이 이 역할의 존재 이유다.

```bash
python scripts/validate_datasets.py
python scripts/validate_notebooks.py
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week {N} --quiet
```

Windows에서는 `python3`가 아니라 **`python`**을 쓴다 — `python3`는 Microsoft Store 스텁이다
(CLAUDE.md).

`validate_notebooks.py`는 `nbclient`로 `kernel_name="python3"` 커널을 써서 실제로 실행한다.
커널이 없으면 이렇게 등록한다.

```bash
python -m ipykernel install --user --name python3 --display-name "Python 3"
```

**커널 문제를 노트북의 kernelspec을 바꿔 덮지 않는다.** 환경 문제는 환경에서 고친다.

빠르게 한 노트북만 돌려볼 때:

```bash
python -c "import nbformat; from nbclient import NotebookClient; nb=nbformat.read(r'notebooks/solutions/week04_solution.ipynb', as_version=4); NotebookClient(nb, kernel_name='python3', timeout=300).execute(); print('OK')"
```

## 실패했을 때

| 증상 | 확인할 것 |
|---|---|
| `KeyError: '열이름'` | `encoding="utf-8-sig"` 누락(BOM), 또는 열 이름이 실제 CSV와 다름 |
| `FileNotFoundError` | 상대경로 깊이(`../../`), 파일명 오타, 데이터 미생성 |
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `NoSuchKernel` | 위 `ipykernel install` |
| 한글 깨짐 | matplotlib 폰트 설정 |
| 정답본에서 실행 오류 | 빈칸을 잘못 채웠거나, 학생용과 흐름이 어긋남 |

**실패를 숨기고 넘어가지 않는다.** 오류 전문을 보고서에 싣고, 원인이 데이터인지 코드인지
환경인지 구분해 적는다. 학생이 만날 법한 오류라면 content-writer에게 넘겨 운영안
"실습 중 오류 대응"에 넣게 한다 — 실제로 겪은 오류가 가장 좋은 교보재다.

## 끝내기 전 자가 점검

- [ ] 세 노트북의 `## N단계.` 제목이 같은가
- [ ] 학생용에 빈칸이 있고, 정답·강사본에는 `TODO`/`____`가 없는가
- [ ] 모든 `read_csv`에 `encoding="utf-8-sig"`가 있는가
- [ ] 경로가 `../../data/weekly/...` 상대경로인가
- [ ] 세 검증 명령을 **실제로 실행**했고 출력을 보고서에 실었는가
- [ ] 강의 자료에 실릴 확정 코드와 실제 출력을 보고서에 적었는가
