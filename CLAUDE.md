# CLAUDE.md

이 저장소는 「반도체 및 반도체 공정 데이터 분석 10차시 과정」교육 콘텐츠입니다.
전체 소개는 `README.md`, 커리큘럼 설계는 `docs/curriculum.md`를 참고하세요.

## 작업 시 반드시 지킬 규칙

- `data/raw/`의 원본 CSV(`반도체_공정_샘플.csv`, `fab.csv`)는 **절대 수정하지 않는다**. 읽기 전용.
- 새 실습 데이터를 만들 때는 `scripts/generate_weekly_data.py`에 시드를 고정한 로직으로 추가하고,
  `data/weekly/weekXX/`에 `utf-8-sig` 인코딩으로 저장한다.
- 데이터나 노트북을 수정한 뒤에는 반드시 `python scripts/validate_datasets.py`와
  `python scripts/validate_notebooks.py`를 실행해 회귀가 없는지 확인한다.
- 모든 HTML 강의 자료는 `assets/css/common.css`의 기존 클래스만 재사용한다(새 CSS 프레임워크 도입 금지).
- `fab.csv`(`Sensor0~Sensor589`)는 v2 커리큘럼의 핵심 10차시 경로에서 제외되었다(배경:
  `docs/restructure-plan.md`). 강사 선택 심화 부록 등에서 다루더라도 `Sensor0~Sensor589`의 실제
  물리적 의미를 절대 단정하지 않는다.
- 상관관계·모델 예측 결과를 다루는 콘텐츠(8·9·10차시)에서는 "원인"이 아니라 "원인 후보"라는
  표현을 사용한다.
- 커리큘럼 구성은 `docs/curriculum.md`(v2)를 기준으로 하며, v1 대비 변경 배경과 각 문서/폴더의
  최신화 여부는 `docs/restructure-plan.md`를 참고한다.

## 자주 쓰는 명령

```bash
python scripts/generate_weekly_data.py   # 차시별 데이터 재생성(재현 가능)
python scripts/validate_datasets.py      # 데이터 검증
python scripts/validate_notebooks.py     # 노트북 실행 검증(nbclient, kernel_name="python3")
```

Windows 환경에서는 `python`을 사용한다(`python3`는 Microsoft Store 스텁으로 연결되어 동작하지 않는다).

## 하네스: 강의 콘텐츠 제작

**목표:** 한 차시를 이루는 8종 산출물(강의 HTML·실습지·퀴즈·운영안·노트북 3종·데이터+데이터사전)을
함께 움직이고 실제로 검증해, 일부만 고쳐 어긋나는 일을 막는다.

**트리거:** 차시 콘텐츠 개선·보완, 전 차시 품질 감사, 사이트/디자인 개편 요청 시
`course-build` 스킬을 사용하라. 단순 사실 질문("이 파일 어디 있어?")은 직접 응답 가능.

**추가 명령:**

```bash
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py           # 전 차시 교차 정합성 검사
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week 4  # 특정 차시
```

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-09-23 | 초기 구성 — 에이전트 6, 스킬 8, 교차 정합성 검사 스크립트 | 전체 | - |
| 2026-09-23 | 검사 스크립트를 노트북 3종 전수 비교로 확장 | skills/course-consistency-audit | student↔solutions만 비교해 강사용 단계 누락 8차시를 놓쳤음 |
| 2026-09-23 | 단위·물리량 정합성 절 신설, "원인 후보" 과다 적용 규칙·Spec/UCL 용어·부호 적용 단위·유입 지점 규정 추가 | skills/semiconductor-content-guard | 스킬 실행 테스트에서 판정 근거를 못 찾은 사례 발견 |
| 2026-09-23 | 검수 절차 grep 명령을 셸·확장자 비의존으로 교체 | skills/semiconductor-content-guard | 중괄호 확장이 PowerShell에서 0건 침묵 실패, `.md`·`.json` 누락 |
| 2026-09-23 | 출력 프로토콜에 "파일 생성 금지 시 응답 메시지로" 단서 추가 | agents/domain-reviewer | "파일 수정 안 함" 원칙과 충돌 |
