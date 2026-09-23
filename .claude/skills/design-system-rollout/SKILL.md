---
name: design-system-rollout
description: 사이트 디자인·레이아웃을 바꾸거나 전 차시에 롤아웃할 때 반드시 사용한다. assets/css/common.css의 토큰·컴포넌트 수정, 랜딩 index.html 개편, 히어로·카드·버튼 레이아웃 변경, 이미지 추가·최적화, 인쇄 스타일 조정, "디자인 바꿔줘", "더 보기 좋게", "카드 레이아웃 개선", "모바일에서 깨져" 같은 요청에 사용할 것. 토큰 목록, 컴포넌트 사용 조건, 이미지·정직성 규칙, 전 차시 롤아웃 절차가 들어 있다. design-steward 에이전트의 기본 스킬.
---

# 디자인 시스템 롤아웃

디자인 시스템 이름은 **FabMetric Telemetry**이고, 계약서는 `docs/design-system.md`다.
토큰·컴포넌트를 바꾸면 그 문서를 함께 갱신한다 — 안 그러면 다음 세션의 작성자가 무엇을
써도 되는지 알 수 없다.

## 제약이 먼저다

1. **새 CSS 프레임워크를 도입하지 않는다**(CLAUDE.md). Tailwind·Bootstrap을 끌어오지 않고,
   빌드 단계를 추가하지 않는다.
2. **서버 없이 파일을 직접 열어도 동작해야 한다.** 모든 CSS·JS·이미지는 상대경로 로컬 파일이다.
   CDN 링크나 절대경로를 넣지 않는다.
3. **새 클래스보다 토큰 재사용을 먼저 검토한다.** `:root` 변수로 표현되면 클래스를 만들지 않는다.
   클래스가 늘수록 랜딩 + 강의 10 + 실습지 10에 롤아웃할 표면이 늘어난다.
4. **기존 클래스의 의미를 바꾸지 않는다.** 10개 차시가 이미 쓰고 있다. 필요하면 변형 클래스를
   추가한다(`.btn-primary.on-dark`처럼). 불가피하게 바꿨다면 전 차시를 재검증한다.

## 토큰 (`assets/css/common.css`의 `:root`)

| 변수 | 값 | 용도 |
|---|---|---|
| `--blue` / `--blue-bg` / `--blue-line` / `--blue-hover` | `#2563eb` / `#eff6ff` / `#bfdbfe` / `#1d4ed8` | 개념·주요 액션 |
| `--green` / `--green-bg` / `--green-line` | `#10b981` / `#ecfdf5` / `#a7f3d0` | 정상·합격·성공 |
| `--orange` / `--orange-bg` / `--orange-line` | `#f59e0b` / `#fffbeb` / `#fde68a` | 주의·확인 필요 |
| `--red` / `--red-bg` / `--red-line` | `#ef4444` / `#fef2f2` / `#fecaca` | 이상·불량·오류 |
| `--purple` / `--purple-bg` / `--purple-line` | `#7c3aed` / `#faf5ff` / `#e9d5ff` | 실습·도전 |
| `--cyan` / `--cyan-bg` / `--cyan-line` | `#06b6d4` / `#ecfeff` / `#a5f3fc` | 텔레메트리 보조 강조 |
| `--ink` / `--muted` | `#0f172a` / `#64748b` | 본문·제목 / 보조 텍스트 |
| `--on-dark` / `--on-dark-muted` | `#e2e8f0` / `#94a3b8` | 다크 배경 위 텍스트 |
| `--bg` / `--card` / `--line` | `#f8fafc` / `#ffffff` / `#e2e8f0` | 배경 / 카드 / 테두리 |
| `--radius` / `--radius-sm` / `--radius-xs` | `16px` / `10px` / `6px` | 카드 / 버튼·입력 / 배지·칩 |
| `--shadow-card` / `--shadow-card-hover` | — | 카드 기본 / hover |
| `--font` | Inter → Pretendard → 맑은고딕 → Noto Sans KR | 본문 |
| `--font-mono` | JetBrains Mono → Consolas → D2Coding | 코드·수치 |
| `--maxw` | `1180px` | 본문 최대 폭 |

**색은 의미를 가진다.** 초록은 정상/합격, 빨강은 이상/불량이다. 장식으로 색을 고르면
학생이 색에서 잘못된 신호를 읽는다.

## 정직성 규칙 — 가장 중요한 부분

이것은 교육 사이트이지 공정 모니터링 시스템이 아니다. 실제로 없는 기능이 있는 것처럼
보이면 거짓말이 된다.

| 금지 | 대신 |
|---|---|
| `LIVE`, `실시간`, `실시간 모니터링`, `Online` 배지 | 상태 표현을 쓰지 않거나 "예시"로 표기 |
| 그럴듯하게 지어낸 대시보드 수치 | 본문에 **실제로 등장하는 값**만 |
| 검증 불가능한 푸터 칩 | `Python 3.11+`, `10차시 · 4부 구성` 같은 사실만 |

`.telemetry-card`처럼 대시보드형 프리뷰를 만들 때는 **셋을 모두** 지킨다.

1. 제목·서브라벨에 "예시" 표기
2. `LIVE`/`실시간` 표현 금지
3. 섹션 상단에 고지

```html
<p class="illustration-note">예시 일러스트레이션 · 실제 데이터 아님</p>
```

`.stat-panel`(히어로 옆 스탯)도 마찬가지다 — 본문에 이미 나오는 예제값만 넣는다.

## 컴포넌트별 사용 조건

| 클래스 | 어디에 | 조건 |
|---|---|---|
| `.tab-strip` | 랜딩 헤더 전용 | 차시 페이지에 쓰지 않는다 |
| `.breadcrumb` | 차시 페이지 헤더 아래 | |
| `.section-kicker` | 섹션 제목 위 작은 라벨 | 대문자 영문 + `.dot` |
| `.hero-with-stats` + `.stat-panel` | 히어로 2단 그리드 | **실제 예제값만**. 860px 이하 1단 |
| `.outcome-grid` / `.outcome-card` | 3열 학습 목표 카드 | 기존 `.goal-list`를 지우지 말고 카드 아래 둔다 |
| `.concept-panel`(`.cp-visual`/`.cp-info`) | 개념도 2단 패널 | 기존 SVG를 그대로 옮겨 넣으면 된다 |
| `.step-badge` | `STEP 01` 단계 배지 | 실제 손 실습 흐름에만. 전 섹션 남발 금지 |
| `.telemetry-grid` / `.telemetry-card` | 대시보드형 프리뷰 | **"예시" 라벨 + `.illustration-note` 필수** |
| `.btn-row` / `.btn-primary` / `.btn-secondary`(+`.on-dark`) | 히어로·CTA | `.nav-buttons`와 중첩하지 않는다 |
| `.cta-banner` | 하단 다크 CTA | `print.css`가 인쇄 시 숨긴다 |
| `.footer-status` / `.chip` | 푸터 상태 칩 | **검증 가능한 사실만** |

## 이미지

1. **실제 산출물을 우선 쓴다.** `assets/images/weekNN/`에 5~10차시 실습에서 실제로 생성한
   matplotlib 차트 PNG가 있다(흰 배경, 한글 라벨). 직접 그린 SVG보다 낫다 — 진짜 결과물이다.
2. **출처가 불분명하거나 워터마크가 있는 이미지는 쓰지 않는다.** 저장소 루트 `images/`의
   일부가 여기 해당한다. 저작권 확인 없이 교육 사이트에 올리지 않는다.
3. **원본을 그대로 참조하지 않는다.** 보통 수 MB다. `assets/images/site/`에 리사이즈·압축한
   사본을 두고 그것만 참조한다.

```python
from PIL import Image
im = Image.open("images/imageN.jpg")
w, h = im.size
maxw = 1600   # 배경용 1600, 인라인용 900
if w > maxw:
    im = im.resize((maxw, int(h * maxw / w)), Image.LANCZOS)
im.save("assets/images/site/이름.jpg", "JPEG", quality=80, optimize=True)
```

4. **배경 이미지 위 텍스트는 대비를 확인한다.** 저해상도 차트를 낮은 투명도(5~10%)로 깔고,
   그 위 텍스트가 WCAG AA를 넘는지 본다. `index.html`의 `.hero-home`이 예시다.

## 롤아웃 절차

디자인 변경이 반쯤 적용된 상태가 가장 나쁘다 — 사이트가 두 모습으로 갈라진다.

```
1. 범위·기준 확정      참조 목업이 있는가? 불만 지점이 무엇인가? 어디까지 적용하는가?
2. 시범 적용           랜딩 또는 대표 차시 1개
3. 사용자 확인         ← 반드시 멈춘다
4. 전 차시 롤아웃      강의 10 + 실습지 10
5. 전 차시 재검증
6. docs/design-system.md 갱신
```

3단계를 건너뛰고 20개 파일에 적용한 뒤 방향이 틀렸음을 아는 것이 최악이다.
요청이 "더 모던하게"처럼 시각적으로만 정의됐다면, 추측으로 전면 개편하지 말고 **작은 범위에서
2안을 만들어 보여주고 선택받는다.**

시범 적용 상태로 작업이 끝나면 **그 사실과 남은 차시를 반드시 보고한다.**

## 검증

```bash
# 미정의 class, 깨진 상대경로 참조를 전 차시에서 확인
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --quiet
```

| 확인 항목 | 방법 |
|---|---|
| 미정의 class / 깨진 참조 | 위 스크립트 (FAIL로 잡힌다) |
| 서버 없이 열리는가 | `index.html`을 파일로 직접 열어본다 |
| 인쇄 | `print.css` 검토. **실습지는 실제로 인쇄해 쓴다** |
| 좁은 화면 | `common.css`의 기존 미디어 쿼리 경계(860px 등) |
| 대비 | 배경 이미지 위 텍스트가 WCAG AA를 넘는가 |
| 기능 | 복사 버튼, 정답 토글, 자동 목차, 진행률 표시줄이 여전히 동작하는가 |

마지막 항목을 잊기 쉽다. `common.js`는 `.code-block > .copy-btn` + `pre code`,
`main.page > section.block > h2`, `#progressFill[data-week]`를 찾고, `quiz.js`는
`.reveal-btn`의 **바로 다음 형제** `.answer-box`를 찾는다. 마크업 구조를 바꾸면 이들이 조용히
죽는다 — 스타일은 멀쩡해 보이므로 눈으로는 안 잡힌다.

## 본문 글은 건드리지 않는다

이 스킬의 범위는 **틀**이다. 마크업 구조는 고치되 본문 문장은 content-writer에게 넘긴다.
디자인 작업 중에 글을 고치면 그 글은 도메인 검수를 받지 않는다.
