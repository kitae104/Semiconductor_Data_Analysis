# 강사용 운영 가이드

이 문서는 「반도체 및 반도체 공정 데이터 분석 10차시 과정」을 실제로 운영하는 강사를 위한 가이드다.
차시별 수업 흐름과 발문은 각 `lectures/weekXX/instructor-guide.md`에 있다. 이 문서는 과정 전체를
운영할 때 필요한 공통 정보를 담는다.

## 1. 과정 운영 전 준비

- **환경 준비**: 강사 PC에 `requirements.txt` 설치, Jupyter 커널 등록
  (`python -m ipykernel install --user --name python3`).
- **학생 준비물 안내**: Google 계정(Colab용) 또는 로컬 Python 환경, 노트북/랩톱.
- **자료 배포**: 매 차시 수업 전 `data/weekly/weekXX/`의 CSV와 `notebooks/student/weekXX_student.ipynb`를
  학생들에게 공유한다(클라우드 드라이브, LMS 등).
- **사전 실행 확인**: 매 차시 수업 전 `notebooks/instructor/weekXX_instructor.ipynb`를 처음부터 끝까지
  한 번 실행해보고 이상이 없는지 확인한다.

## 2. 매 차시 공통 수업 흐름

1. 지난 시간 복습
2. 오늘 해결할 문제 소개
3. 반도체 및 데이터 개념 설명
4. 강사 코드 시연
5. 휴식
6. 단계별 따라 하기 실습
7. 도전 실습
8. 결과 정리 및 퀴즈

세부 발문·예상 오개념·오류 대응은 각 차시 `instructor-guide.md`를 그대로 따르되, 학습자 수준과
현장 상황에 맞게 각 단계에 들이는 비중을 조정해도 된다.

## 3. 난이도별 학습자 대응

- **빠른 학습자**: 각 차시 `instructor-guide.md`의 "빠른 학습자용 추가 과제"를 제시한다.
  대부분 다음 차시 개념을 살짝 미리 보여주는 방식으로 설계되어 있다.
- **느린 학습자**: "느린 학습자용 최소 과제"를 기준으로, 핵심 코드 1~2줄과 결과 해석 한 문장만
  완성해도 그 차시 목표를 달성한 것으로 인정한다.
- **결시/보강**: 모든 차시가 `notebooks/instructor/`(시연) + `notebooks/solutions/`(정답) +
  `lectures/weekXX/index.html`(강의 전체 내용)로 자기주도 학습이 가능하도록 설계되어 있다.

## 4. 자주 발생하는 기술적 문제

| 문제 | 원인 | 해결 |
| --- | --- | --- |
| `FileNotFoundError` | CSV 미업로드 또는 경로 오류 | Colab은 파일 업로드 후 파일명만 사용, 로컬은 저장소 구조 유지 |
| `KeyError: '컬럼명'` | 열 이름 오타 | `df.columns`로 정확한 이름 먼저 확인 |
| 한글 깨짐 | 인코딩 문제 | 모든 CSV는 `utf-8-sig`로 저장되어 있음. `pd.read_csv(..., encoding="utf-8-sig")` 확인 |
| Colab 런타임 끊김 | 세션 만료 | 파일 재업로드 후 위에서부터 재실행 |
| 9차시 모델 학습 느림 | 정상 | `DecisionTreeClassifier(max_depth=4)`는 수 초 내 완료되어야 함. 오래 걸리면 `stratify=y` 누락 등 확인 |

## 5. 평가 운영

- 매 차시 `lectures/weekXX/quiz.json`과 `worksheet.html`을 활용해 이해도를 점검한다.
- 정답과 해설은 각 퀴즈 항목에 포함되어 있으며, 단순 정답 확인이 아니라 "왜 그런지"까지 설명하도록
  학생에게 요구한다.
- 10차시 미니 프로젝트는 `lectures/week10/project-report-template.html`을 최종 산출물로 사용한다.
  평가 시 다음을 확인한다.
  - 그래프 3개 이상, 결과 해석 문장 5개 이상, 개선 제안 2개 이상 포함 여부
  - "상관관계만으로 원인이라고 단정할 수 없다"는 표현 등 분석의 한계를 인식했는지 여부

## 6. 콘텐츠 유지보수

- 데이터를 다시 생성해야 할 경우 `python scripts/generate_weekly_data.py`를 실행한다(시드가
  고정되어 있어 항상 동일한 결과가 나온다).
- 노트북을 수정한 뒤에는 반드시 `python scripts/validate_notebooks.py`로 전체 재실행 검증을 한다.
- 새로운 기수를 운영하면서 발견한 오개념·오류 패턴은 각 차시 `instructor-guide.md`의
  "예상 오개념" 항목에 누적해서 업데이트할 것을 권장한다.
