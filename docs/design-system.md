# 디자인 시스템 — FabMetric Telemetry

`assets/css/common.css`가 정의하는 공통 디자인 토큰·컴포넌트와, 다른 차시/`worksheet.html`로 새
디자인을 롤아웃할 때 따라야 할 절차를 정리한다. 배경: `stitch-reference/`의 목업(`DESIGN.md`,
`code.html`, `screen.png`)과 `docs/superpowers/specs/2026-09-19-fabmetric-design-system-pilot-design.md`.

파일럿은 두 단계로 진행됐다.
1. **1단계(재스킨)** — 랜딩 + 1차시의 색상/타이포/그림자/라운드 값만 새 토큰으로 교체 (구조는 유지).
2. **2단계(구조 재구성)** — stitch 레퍼런스와의 시각적 간극이 커서, 랜딩 + 1차시의 레이아웃 자체를
   stitch 구성(탭 스트립, 대시보드형 미리보기 카드, 아웃컴 카드, 스탯 패널 등)에 맞춰 다시 짰다.
   아래 "재사용 가능한 컴포넌트" 목록은 이 2단계에서 추가된 것들이다.

## 토큰 목록 (`assets/css/common.css` `:root`)

| 변수 | 값 | 용도 |
|---|---|---|
| `--blue` / `--blue-bg` / `--blue-line` / `--blue-hover` | `#2563eb` / `#eff6ff` / `#bfdbfe` / `#1d4ed8` | 개념/주요 액션 |
| `--green` / `--green-bg` / `--green-line` | `#10b981` / `#ecfdf5` / `#a7f3d0` | 정상/합격/성공 |
| `--orange` / `--orange-bg` / `--orange-line` | `#f59e0b` / `#fffbeb` / `#fde68a` | 주의/확인 필요 |
| `--red` / `--red-bg` / `--red-line` | `#ef4444` / `#fef2f2` / `#fecaca` | 이상/불량/오류 |
| `--purple` / `--purple-bg` / `--purple-line` | `#7c3aed` / `#faf5ff` / `#e9d5ff` | 실습/도전 |
| `--cyan` / `--cyan-bg` / `--cyan-line` | `#06b6d4` / `#ecfeff` / `#a5f3fc` | 텔레메트리 보조 강조(필요할 때만) |
| `--ink` | `#0f172a` | 본문/제목 색 |
| `--muted` | `#64748b` | 보조 텍스트 |
| `--on-dark` / `--on-dark-muted` | `#e2e8f0` / `#94a3b8` | 다크 카드(`.telemetry-card` 등) 위의 본문/보조 텍스트 |
| `--bg` / `--card` / `--line` | `#f8fafc` / `#ffffff` / `#e2e8f0` | 배경/카드/테두리 |
| `--radius` / `--radius-sm` / `--radius-xs` | `16px` / `10px` / `6px` | 카드 / 버튼·입력 / 배지·칩 |
| `--shadow-card` / `--shadow-card-hover` | (common.css 참고) | 카드 기본/hover 그림자 |
| `--shadow-glow-cyan` | (common.css 참고) | 다크 카드 hover 강조(`.telemetry-card:hover`) |
| `--font` | Inter 우선, Pretendard/맑은고딕/Noto Sans KR 폴백 | 본문 폰트 |
| `--font-mono` | JetBrains Mono 우선, Consolas/D2Coding 폴백 | 코드/수치 폰트 |
| `--maxw` | `1180px` | 페이지 본문 최대 폭 |

## 재사용 가능한 컴포넌트 (2단계에서 추가, `common.css`)

레이아웃 구조까지 롤아웃할 때 참고할 클래스들. 전부 위 토큰만 사용하며 새 프레임워크는 없다.

| 클래스 | 용도 | 사용 예 |
|---|---|---|
| `.tab-strip` | 헤더 안 페이지 내 앵커 내비(랜딩 전용) | `index.html`의 `<nav class="tab-strip">` |
| `.breadcrumb` | 헤더 아래 위치 표시(차시 페이지 전용) | `week01/index.html`의 `<nav class="breadcrumb">` |
| `.section-kicker` | 섹션 제목 위 작은 라벨(대문자 영문, 점 아이콘) | `<span class="section-kicker"><span class="dot"></span>...</span>` |
| `.hero-with-stats` + `.stat-panel` | 히어로 옆 2단 그리드로 스탯 패널 배치(860px 이하에서 1단으로 stack) | 반드시 **본문에 이미 등장하는 실제 예제값**만 넣는다 — 실시간처럼 보이는 가짜 수치 금지 |
| `.outcome-grid` / `.outcome-card` | 3열 핵심 학습 목표 카드 | 기존 `.goal-list`를 지우지 말고 카드 아래에 그대로 둔다 |
| `.concept-panel` (`.cp-visual` / `.cp-info`) | 기존 SVG 개념도를 2단(그림+설명)으로 감싸는 패널 | 새 그림을 만들 필요 없이 기존 SVG를 그대로 옮겨 넣으면 됨 |
| `.step-badge` | `STEP 01/02/03` 같은 단계 배지 | 실제 손 실습 흐름을 따라가는 섹션에만, 전체 섹션에 남발하지 않는다 |
| `.telemetry-grid` / `.telemetry-card` | 다크 카드 그리드(대시보드형 미리보기) | **반드시 "예시" 라벨과 `.illustration-note`를 함께 표시** — 아래 "이미지·일러스트레이션 사용 원칙" 참고 |
| `.btn-row`, `.btn-primary`, `.btn-secondary` (`.on-dark` 변형 포함) | 히어로/CTA용 버튼 쌍 | `.nav-buttons`(진행 버튼)와는 별개 — 혼용해 중첩하지 않는다 |
| `.cta-banner` | 하단 다크 CTA 배너 | `print.css`에서 이미 인쇄 시 숨김 처리됨 |
| `.footer-status` (`.chip`) | 푸터 상태 칩 | **실제로 검증 가능한 사실만**(`Python 3.11+`, `10차시 · 4부 구성`) — "Online" 같은 가짜 가동 상태 금지 |

## 이미지·일러스트레이션 사용 원칙

- `assets/images/weekNN/`에는 5~10차시 실습에서 실제로 생성한 matplotlib 차트 PNG가 있다(흰 배경,
  한글 라벨). 랜딩 페이지 등에서 "미리보기"용으로 쓸 때는 **이 실제 이미지를 우선 사용**한다 —
  직접 그린 SVG보다 낫다(진짜 결과물이므로). `index.html`의 "🎬 강의 자료 미리보기" 섹션에 6/7/10차시
  차트 3개를 예시로 추가해뒀다(`.anim-card img`), 다른 차시로 확장할 때 같은 패턴을 따르면 된다.
- 반대로 `.telemetry-card`(웨이퍼 맵/수율 추이 등 대시보드형 프리뷰)는 **실제로 없는 실시간 기능처럼
  보일 위험**이 있어 직접 그린 SVG로 만들었다. 이런 요소를 추가/확장할 때는 반드시
  ① 제목·서브라벨에 "예시"를 붙이고, ② `LIVE`/`실시간` 같은 표현을 쓰지 않으며, ③ 섹션 상단에
  `.illustration-note`로 "예시 일러스트레이션 · 실제 데이터 아님"을 명시한다.
- 배경 이미지로 쓸 때(`background-image`)는 저해상도 차트를 낮은 투명도(5~10%)로만 사용하고, 그
  위에 얹히는 텍스트의 대비가 WCAG AA를 넘는지 확인한다 — `index.html`의 `.hero-home`이 예시다.
- **일반 스톡/장식 이미지**(`images/image1.jpg` ~ `image10.jpg` 등, 저장소 루트의 `images/` 폴더에
  사용자가 제공)를 쓸 때:
  - 출처가 불분명하거나 촬영자 워터마크가 박힌 이미지(예: `images/image1.jpg`)는 **쓰지 않는다** —
    저작권 확인 없이 교육 사이트에 올리면 안 된다.
  - 원본은 보통 수 MB로 커서 그대로 쓰면 안 된다. `assets/images/site/`에 최적화(리사이즈+압축)한
    사본을 두고 그것만 참조한다. 예시 스크립트(Python Pillow):
    ```python
    from PIL import Image
    im = Image.open("images/imageN.jpg")
    w, h = im.size
    maxw = 1600  # 배경용은 1600, 인라인용은 900 정도
    if w > maxw:
        im = im.resize((maxw, int(h * maxw / w)), Image.LANCZOS)
    im.save("assets/images/site/이름.jpg", "JPEG", quality=80, optimize=True)
    ```
  - 현재 `assets/images/site/`에 있는 것: `chip-die-grid.jpg`(다크 칩 격자, `.cta-banner` 배경 텍스처),
    `pcb-macro.jpg`(실제 PCB 매크로 사진, 1차시 "반도체 개념 이해하기"에 인라인 삽입),
    `ai-circuit.jpg`(회로+AI 컨셉 이미지, 1차시 "AI로 한 걸음 더" 섹션 헤더 이미지).
  - `<img>`로 삽입할 때 `width`/`height` HTML 속성과 함께 CSS `max-width`만 주면 **비율이 깨진다** —
    반드시 `height:auto`도 같이 지정한다(`style="max-width:520px; height:auto;"`처럼).
  - `images/` 폴더 자체(원본, 최적화 전)는 git에 커밋하지 않았다 — 용량이 크고 일부는 미사용/라이선스
    불명확이라 로컬 작업용으로만 남겨뒀다.

## 다른 페이지에 롤아웃하는 절차

각 차시 `index.html`(2~10차시)에 적용할 때:

1. `<head>`의 `<link rel="stylesheet" href="../../assets/css/common.css">` 위에 Google Fonts 3줄을 추가한다
   (`lectures/week01/index.html` 참고).
2. 페이지 내 `<style>` 블록에서 하드코딩된 hex 색상(`#0f172a`, `#fff` 등)이나 `"Courier New", monospace`
   같은 모노 폰트 스택이 있는지 `grep -n "#[0-9a-fA-F]\{3,6\}"`로 찾아 해당하는 `var(--...)` 토큰으로
   교체한다.
3. `--green`/`--orange`가 바뀌었으므로, 이 색을 rgba()로 하드코딩해 그림자 tint 등에 쓴 부분이 있다면
   새 rgb 값(`16,185,129` / `245,158,11`)으로 다시 계산한다.
4. 구조까지 맞추고 싶다면(선택) 위 "재사용 가능한 컴포넌트" 표를 참고해 브레드크럼·아웃컴 카드·
   개념 패널·STEP 배지를 추가한다 — `week01/index.html`을 템플릿으로 삼는다. `.hero`를
   `.hero-with-stats`로 감쌀 경우, `assets/js/common.js`가 이미 이 래퍼 구조를 지원하도록 고쳐져
   있으니 별도 JS 수정은 필요 없다.
5. 브라우저 프리뷰(`static-preview`, `http://localhost:8743/lectures/weekNN/index.html`)로 확인한다.
   이 세션에서 브라우저 탭이 CSS/JS를 공격적으로 캐싱해 수정이 반영 안 된 것처럼 보이는 문제를 겪었다
   — 확인할 땐 URL에 `?v=<임의값>` 같은 쿼리를 붙여 새로고침하거나, `fetch(url,{cache:'no-store'})`로
   서버가 실제로 새 내용을 주는지 먼저 확인한다.
6. TOC/퀴즈/복사 버튼 등 기존 인터랙션이 그대로 동작하는지 확인한다.
7. 파일 하나 끝날 때마다 커밋한다(한 커밋에 여러 차시를 묶지 않는다).

`worksheet.html`은 대부분 `common.css` 클래스만 상속하므로 보통 손댈 곳이 없다 — 위 2~3번 방식으로
하드코딩 색상 유무만 확인하면 된다. `instructor-guide.md`는 마크다운 문서라 이 디자인 시스템과 무관하다.
