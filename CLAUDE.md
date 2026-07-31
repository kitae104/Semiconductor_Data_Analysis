# CLAUDE.md

이 저장소는 「반도체 및 반도체 공정 데이터 분석 10주 과정」교육 콘텐츠입니다.
전체 소개는 `README.md`, 커리큘럼 설계는 `docs/curriculum.md`를 참고하세요.

## 작업 시 반드시 지킬 규칙

- `data/raw/`의 원본 CSV(`반도체_공정_샘플.csv`, `fab.csv`)는 **절대 수정하지 않는다**. 읽기 전용.
- 새 실습 데이터를 만들 때는 `scripts/generate_weekly_data.py`에 시드를 고정한 로직으로 추가하고,
  `data/weekly/weekXX/`에 `utf-8-sig` 인코딩으로 저장한다.
- 데이터나 노트북을 수정한 뒤에는 반드시 `python scripts/validate_datasets.py`와
  `python scripts/validate_notebooks.py`를 실행해 회귀가 없는지 확인한다.
- 모든 HTML 강의 자료는 `assets/css/common.css`의 기존 클래스만 재사용한다(새 CSS 프레임워크 도입 금지).
- `fab.csv`(`Sensor0~Sensor589`)는 v2 커리큘럼의 핵심 10주 경로에서 제외되었다(배경:
  `docs/restructure-plan.md`). 강사 선택 심화 부록 등에서 다루더라도 `Sensor0~Sensor589`의 실제
  물리적 의미를 절대 단정하지 않는다.
- 상관관계·모델 예측 결과를 다루는 콘텐츠(8·9·10주차)에서는 "원인"이 아니라 "원인 후보"라는
  표현을 사용한다.
- 커리큘럼 구성은 `docs/curriculum.md`(v2)를 기준으로 하며, v1 대비 변경 배경과 각 문서/폴더의
  최신화 여부는 `docs/restructure-plan.md`를 참고한다.

## 자주 쓰는 명령

```bash
python scripts/generate_weekly_data.py   # 주차별 데이터 재생성(재현 가능)
python scripts/validate_datasets.py      # 데이터 검증
python scripts/validate_notebooks.py     # 노트북 실행 검증(nbclient, kernel_name="python3")
```

Windows 환경에서는 `python`을 사용한다(`python3`는 Microsoft Store 스텁으로 연결되어 동작하지 않는다).
