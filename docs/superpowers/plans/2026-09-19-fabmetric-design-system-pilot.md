# FabMetric Telemetry 디자인 시스템 파일럿 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 랜딩 페이지(`index.html`)와 1차시 강의 페이지(`lectures/week01/index.html`)를 "FabMetric Telemetry" 디자인
톤으로 재스킨하고, `assets/css/common.css`의 디자인 토큰을 갱신해 이후 다른 차시로 쉽게 롤아웃할 수 있게 한다.

**Architecture:** `assets/css/common.css`의 기존 CSS 변수명(`--blue`, `--ink`, `--radius` 등)은 그대로 두고 값만
FabMetric Telemetry 스펙으로 교체한다. 새 변수(`--cyan`, `--blue-hover`, `--radius-sm`, `--radius-xs`,
`--shadow-card`, `--shadow-card-hover`, `--font-mono`)를 최소한으로 추가한다. 이 공유 CSS 파일이 모든 페이지에
링크되어 있으므로 값 갱신만으로 전체 사이트가 즉시 재스킨되며, 이번 파일럿에서는 랜딩 페이지와 1차시 페이지에
남아있는 인라인 하드코딩 색상만 손으로 정리한다. Tailwind 등 새 프레임워크는 도입하지 않는다.

**Tech Stack:** 순수 HTML/CSS (프레임워크 없음), Google Fonts(Inter, JetBrains Mono) 웹폰트 링크.

**Spec:** [docs/superpowers/specs/2026-09-19-fabmetric-design-system-pilot-design.md](../specs/2026-09-19-fabmetric-design-system-pilot-design.md)

## Global Constraints

- CSS 변수명은 그대로 유지하고 **값만** 갱신한다 — 2~10차시 롤아웃 시 HTML을 거의 건드리지 않는 것이 목표.
- 새 CSS 프레임워크(Tailwind 등) 도입 금지, `assets/css/common.css`의 기존 클래스 체계만 확장한다 (`CLAUDE.md`).
- 헤더/내비게이션의 **구조**(DOM 마크업, sticky 동작, TOC 사이드바, 진행률 바, 맨 위로 버튼)는 변경하지 않는다 —
  색상·타이포·그림자·라운드만 교체한다.
- stitch-reference 목업의 가짜 실시간 수치(`Lot #WF-882: 98.7%` 등)를 그대로 복제하지 않는다.
- 이번 파일럿 범위는 `assets/css/common.css` + `index.html` + `lectures/week01/index.html` 3개 파일뿐이다.
  다른 차시(`week02`~`week10`), 모든 `worksheet.html`, `instructor-guide.md`는 이번 계획에 포함하지 않는다.
- 데이터/노트북 변경이 없으므로 `python scripts/validate_datasets.py`, `python scripts/validate_notebooks.py`는
  이번 작업에서 실행 대상이 아니다.
- 검증은 내장 브라우저 프리뷰(`.claude/launch.json`의 `static-preview` 구성, `python -m http.server 8743`)로
  스크린샷/콘솔/인터랙션을 확인하는 방식으로 진행한다(자동화 테스트 스위트 없음).

---

## Task 1: `assets/css/common.css` 디자인 토큰 + 컴포넌트 갱신

**Files:**
- Modify: `assets/css/common.css:1-331`

**Interfaces:**
- Produces: 이후 모든 태스크와 향후 롤아웃이 참조할 CSS 변수 — `--blue`, `--blue-hover`(신규), `--green`,
  `--orange`, `--red`, `--purple`, `--cyan`(신규) 및 각 `-bg`/`-line` 짝, `--ink`, `--muted`, `--bg`, `--card`,
  `--line`, `--radius`, `--radius-sm`(신규), `--radius-xs`(신규), `--shadow-card`(신규),
  `--shadow-card-hover`(신규), `--maxw`, `--font`, `--font-mono`(신규).

- [ ] **Step 1: `:root` 토큰 블록 교체**

`assets/css/common.css`의 6~21번째 줄(`:root{ ... }`)을 아래로 교체한다.

```css
:root{
  --blue:#2563eb;      --blue-bg:#eff6ff;      --blue-line:#bfdbfe;      --blue-hover:#1d4ed8;
  --green:#10b981;     --green-bg:#ecfdf5;     --green-line:#a7f3d0;
  --orange:#f59e0b;    --orange-bg:#fffbeb;    --orange-line:#fde68a;
  --red:#ef4444;       --red-bg:#fef2f2;       --red-line:#fecaca;
  --purple:#7c3aed;    --purple-bg:#faf5ff;    --purple-line:#e9d5ff;
  --cyan:#06b6d4;       --cyan-bg:#ecfeff;      --cyan-line:#a5f3fc;

  --ink:#0f172a;
  --muted:#64748b;
  --bg:#f8fafc;
  --card:#ffffff;
  --line:#e2e8f0;
  --radius:16px;
  --radius-sm:10px;
  --radius-xs:6px;
  --shadow-card:0 1px 3px rgba(15,23,42,.06), 0 1px 2px rgba(15,23,42,.04);
  --shadow-card-hover:0 10px 25px -3px rgba(15,23,42,.08), 0 4px 6px -4px rgba(15,23,42,.04);
  --maxw:1180px;
  --font: "Inter","Pretendard","Malgun Gothic","Noto Sans KR",-apple-system,sans-serif;
  --font-mono: "JetBrains Mono","Consolas","D2Coding",monospace;
}
```

- [ ] **Step 2: 헤더 배경을 다크 네이비로 교체**

`.site-header` 규칙(34번째 줄 부근)에서:

```css
.site-header{
  background:linear-gradient(135deg,var(--blue) 0%,#1d4ed8 100%);
```

를 다음으로 교체한다(그 아래 `color:#fff; padding:...` 등 나머지 줄은 그대로 둔다):

```css
.site-header{
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
```

- [ ] **Step 3: `.toc-box`, `section.block` 그림자를 토큰으로 교체**

`.toc-box` 규칙에서 `box-shadow:0 2px 10px rgba(15,23,42,.04);` → `box-shadow:var(--shadow-card);`

`section.block` 규칙에서 `box-shadow:0 2px 10px rgba(15,23,42,.04);` → `box-shadow:var(--shadow-card);`

- [ ] **Step 4: `.term-card` 라운드를 토큰으로 교체**

```css
.term-card{
  border:1px solid var(--purple-line); background:var(--purple-bg); border-radius:12px; padding:1rem 1.1rem;
}
```

의 `border-radius:12px;`를 `border-radius:var(--radius);`로 교체.

- [ ] **Step 5: `.journey .jstep` 라운드/hover 그림자를 토큰으로 교체**

```css
.journey .jstep{
  border-radius:14px; padding:1rem 1rem 1.1rem; border:1px solid; position:relative;
  transition:transform .2s ease, box-shadow .2s ease;
}
.journey .jstep:hover{transform:translateY(-4px); box-shadow:0 10px 22px rgba(15,23,42,.1);}
```

를 다음으로 교체:

```css
.journey .jstep{
  border-radius:var(--radius); padding:1rem 1rem 1.1rem; border:1px solid; position:relative;
  transition:transform .2s ease, box-shadow .2s ease;
}
.journey .jstep:hover{transform:translateY(-4px); box-shadow:var(--shadow-card-hover);}
```

- [ ] **Step 6: `.hero-home` 라운드, `.hero-stats .stat` 그림자를 토큰으로 교체**

`.hero-home` 규칙의 `border-radius:18px;` → `border-radius:var(--radius);`

`.hero-stats .stat` 규칙의 `box-shadow:0 1px 4px rgba(15,23,42,.05);` → `box-shadow:var(--shadow-card);`

- [ ] **Step 7: 버튼류 라운드 + hover 색상을 토큰으로 정리**

```css
.nav-buttons a{
  text-decoration:none; padding:.7rem 1.2rem; border-radius:10px; font-weight:700; font-size:.92rem;
  background:var(--blue); color:#fff; flex:1; text-align:center; min-width:140px;
}
.nav-buttons a.disabled{background:#cbd5e1; pointer-events:none;}
.nav-buttons a.home{background:var(--purple);}
```

를 다음으로 교체:

```css
.nav-buttons a{
  text-decoration:none; padding:.7rem 1.2rem; border-radius:var(--radius-sm); font-weight:700; font-size:.92rem;
  background:var(--blue); color:#fff; flex:1; text-align:center; min-width:140px;
  transition:background .15s ease;
}
.nav-buttons a:hover{background:var(--blue-hover);}
.nav-buttons a.disabled{background:#cbd5e1; pointer-events:none;}
.nav-buttons a.home{background:var(--purple);}
.nav-buttons a.home:hover{background:#6d28d9;}
```

`.reveal-btn` 규칙의 `border-radius:8px;` → `border-radius:var(--radius-sm);`

`.copy-btn` 규칙의 `border-radius:6px;` → `border-radius:var(--radius-xs);`

- [ ] **Step 8: 코드 블록 폰트를 `--font-mono`로 교체**

```css
.code-block code{font-family:"Consolas","D2Coding",monospace;}
```

를

```css
.code-block code{font-family:var(--font-mono);}
```

로 교체.

- [ ] **Step 9: 파일 검증 — 브라우저로 기존 페이지가 새 톤으로 렌더링되는지 확인**

`mcp__Claude_Browser__preview_start`를 `{"name": "static-preview"}`로 실행해 정적 서버를 띄운 뒤,
`mcp__Claude_Browser__navigate`로 `http://localhost:8743/index.html`을 연다.
`mcp__Claude_Browser__computer`(`action: "screenshot"`)로 헤더가 다크 네이비로, 카드 그림자/라운드가
바뀌었는지 눈으로 확인한다. `mcp__Claude_Browser__read_console_messages`로 CSS 파싱 에러 등 콘솔 에러가
없는지 확인한다(Google Fonts는 아직 로드 전이라 폴백 폰트로 보이는 것이 정상 — Task 2에서 처리).

- [ ] **Step 10: 커밋**

```bash
git add assets/css/common.css
git commit -m "$(cat <<'EOF'
FabMetric Telemetry 디자인 토큰으로 common.css 갱신

색상/라운드/그림자/폰트 변수 값을 새 디자인 스펙으로 교체하고
헤더·카드·버튼·코드블록 컴포넌트를 토큰 기준으로 재스킨한다.
변수명은 유지해 이후 차시 롤아웃 시 HTML 변경을 최소화한다.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `index.html` (랜딩 페이지) 재스킨

**Files:**
- Modify: `index.html:1-1113`

**Interfaces:**
- Consumes: Task 1에서 갱신한 `--blue`, `--green`, `--orange`, `--purple`, `--ink`, `--card`, `--radius`,
  `--shadow-card`, `--font-mono` 등 `common.css` 토큰.

- [ ] **Step 1: `<head>`의 손상된 텍스트 제거 + Google Fonts 로드**

```html
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />goekd
        <title>반도체 및 반도체 공정 데이터 분석 과정</title>
        <link rel="icon" href="assets/images/logo.svg" type="image/svg+xml" />
        <link rel="stylesheet" href="assets/css/common.css" />
        <link rel="stylesheet" href="assets/css/print.css" />
```

를 다음으로 교체(뒤에 붙어있던 `goekd` 제거, 폰트 링크 3줄 추가):

```html
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>반도체 및 반도체 공정 데이터 분석 과정</title>
        <link rel="icon" href="assets/images/logo.svg" type="image/svg+xml" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
            rel="stylesheet"
        />
        <link rel="stylesheet" href="assets/css/common.css" />
        <link rel="stylesheet" href="assets/css/print.css" />
```

- [ ] **Step 2: `.week-card` 하드코딩 색상/라운드를 토큰으로 정리**

```css
            .week-card {
                display: block;
                text-decoration: none;
                color: inherit;
                background: #fff;
                border: 1px solid var(--line);
                border-left: 4px solid var(--line);
                border-radius: 14px;
                padding: 1.2rem 1.3rem;
                box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
                transition:
                    transform 0.18s ease,
                    box-shadow 0.18s ease,
                    border-color 0.18s ease;
            }
```

를 다음으로 교체:

```css
            .week-card {
                display: block;
                text-decoration: none;
                color: inherit;
                background: var(--card);
                border: 1px solid var(--line);
                border-left: 4px solid var(--line);
                border-radius: var(--radius);
                padding: 1.2rem 1.3rem;
                box-shadow: var(--shadow-card);
                transition:
                    transform 0.18s ease,
                    box-shadow 0.18s ease,
                    border-color 0.18s ease;
            }
```

- [ ] **Step 3: `.week-card h3` 색상을 토큰으로 정리**

```css
            .week-card h3 {
                margin: 0.35rem 0 0.5rem;
                font-size: 1.08rem;
                color: #0f172a;
            }
```

의 `color: #0f172a;`를 `color: var(--ink);`로 교체.

- [ ] **Step 4: phase 2/3 hover 그림자 색을 새 green/orange 값에 맞게 재계산**

`--green`이 `#16a34a`(rgb 22,163,74) → `#10b981`(rgb 16,185,129)로, `--orange`가 `#ea580c`(rgb 234,88,12) →
`#f59e0b`(rgb 245,158,11)로 바뀌었으므로, 하드코딩된 hover 그림자 tint도 맞춰 바꾼다(그대로 두면 카드
테두리 색과 그림자 색이 어긋나 보인다).

```css
            .week-card.p2:hover {
                border-color: var(--green-line);
                box-shadow: 0 10px 24px rgba(22, 163, 74, 0.16);
            }
```

의 `rgba(22, 163, 74, 0.16)`을 `rgba(16, 185, 129, 0.16)`으로 교체.

```css
            .week-card.p3:hover {
                border-color: var(--orange-line);
                box-shadow: 0 10px 24px rgba(234, 88, 12, 0.16);
            }
```

의 `rgba(234, 88, 12, 0.16)`을 `rgba(245, 158, 11, 0.16)`으로 교체.

(p1/blue, p4/purple은 값이 바뀌지 않았으므로 그대로 둔다.)

- [ ] **Step 5: `.links-row a` 하드코딩 배경을 토큰으로 정리**

```css
            .links-row a {
                font-size: 0.85rem;
                text-decoration: none;
                background: #fff;
                color: var(--blue);
                border: 1px solid var(--blue-line);
                border-radius: 8px;
                padding: 0.45rem 0.85rem;
```

를 다음으로 교체:

```css
            .links-row a {
                font-size: 0.85rem;
                text-decoration: none;
                background: var(--card);
                color: var(--blue);
                border: 1px solid var(--blue-line);
                border-radius: var(--radius-sm);
                padding: 0.45rem 0.85rem;
```

- [ ] **Step 6: `.anim-card` 하드코딩 색상/라운드/그림자를 토큰으로 정리**

```css
            .anim-card {
                background: #fff;
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 1.1rem 1rem 1.3rem;
                box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
```

를 다음으로 교체:

```css
            .anim-card {
                background: var(--card);
                border: 1px solid var(--line);
                border-radius: var(--radius);
                padding: 1.1rem 1rem 1.3rem;
                box-shadow: var(--shadow-card);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
```

- [ ] **Step 7: SVG 텍스트 색상(`list-svg`, `loop-svg`)을 토큰으로 정리**

```css
            .list-svg .val {
                fill: #0f172a;
                font-weight: 700;
                font-family: "Courier New", monospace;
            }
```

의 `fill: #0f172a;`를 `fill: var(--ink);`로 교체.

```css
            .loop-svg .val {
                fill: #0f172a;
                font-weight: 700;
                font-family: "Courier New", monospace;
                font-size: 13px;
            }
```

의 `fill: #0f172a;`를 `fill: var(--ink);`로 교체.

- [ ] **Step 8: 브라우저 검증**

`mcp__Claude_Browser__navigate`로 `http://localhost:8743/index.html`을 새로고침한다(정적 서버는 Task 1에서
이미 띄워둔 것을 재사용, 껐다면 `preview_start`로 다시 시작).

1. `mcp__Claude_Browser__computer`(`action: "screenshot"`)로 전체 페이지 캡처 — 헤더 네이비, 히어로/카드의
   새 라운드·그림자, Inter 폰트가 적용됐는지 확인.
2. `mcp__Claude_Browser__read_console_messages`(`onlyErrors: true`)로 콘솔 에러 없는지 확인(Google Fonts
   로드 실패 시에도 페이지가 깨지지 않는지 함께 확인).
3. `mcp__Claude_Browser__resize_window`(`preset: "mobile"`)로 전환 후 다시 스크린샷 — 헤더/카드/히어로가
   좁은 화면에서 깨지지 않는지 확인. 확인 후 `resize_window`(`preset: "desktop"`)로 반드시 되돌린다.
4. `mcp__Claude_Browser__find`로 "1차시부터 시작하기" 버튼을 찾아 `computer`(`action: "left_click"`)로 클릭,
   `lectures/week01/index.html`로 정상 이동하는지 확인.

- [ ] **Step 9: 커밋**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
랜딩 페이지를 FabMetric Telemetry 톤으로 재스킨

깨진 메타 태그 텍스트를 제거하고 Google Fonts(Inter/JetBrains Mono)를
로드한다. 인라인 스타일의 하드코딩 색상·라운드·그림자를 common.css
토큰 기준으로 정리하고, green/orange hover 그림자 tint를 새 팔레트에
맞게 재계산한다.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `lectures/week01/index.html` 재스킨

**Files:**
- Modify: `lectures/week01/index.html:1-35`

**Interfaces:**
- Consumes: Task 1의 `common.css` 토큰(`--ink`, `--card`, `--font-mono` 등).

- [ ] **Step 1: `<head>`에 Google Fonts 로드 추가**

```html
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1차시. 반도체 공정과 데이터 처음 만나기</title>
<link rel="stylesheet" href="../../assets/css/common.css">
<link rel="stylesheet" href="../../assets/css/print.css">
```

를 다음으로 교체:

```html
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1차시. 반도체 공정과 데이터 처음 만나기</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/css/common.css">
<link rel="stylesheet" href="../../assets/css/print.css">
```

- [ ] **Step 2: `flow-svg` 하드코딩 색상을 토큰으로 정리**

```css
  .flow-svg .fbox{fill:#fff;stroke:var(--line);stroke-width:2;}
  .flow-svg .fbox.active{stroke:var(--purple);fill:var(--purple-bg);}
  .flow-svg .flabel{fill:#0f172a;font-weight:700;}
```

를 다음으로 교체:

```css
  .flow-svg .fbox{fill:var(--card);stroke:var(--line);stroke-width:2;}
  .flow-svg .fbox.active{stroke:var(--purple);fill:var(--purple-bg);}
  .flow-svg .flabel{fill:var(--ink);font-weight:700;}
```

- [ ] **Step 3: 브라우저 검증**

`mcp__Claude_Browser__navigate`로 `http://localhost:8743/lectures/week01/index.html`을 연다.

1. `mcp__Claude_Browser__computer`(`action: "screenshot"`)로 전체 페이지 캡처 — 헤더 네이비, 히어로 배지,
   콜아웃, 코드 블록이 새 톤으로 보이는지 확인.
2. `mcp__Claude_Browser__read_console_messages`(`onlyErrors: true`)로 콘솔 에러 확인.
3. TOC 사이드바 링크를 `mcp__Claude_Browser__find`("학습 목표" 등)로 찾아 클릭해 스크롤 이동이 정상
   동작하는지 확인(공통 JS, `assets/js/common.js` — 이번 작업에서 손대지 않았으므로 동작해야 정상).
4. `mcp__Claude_Browser__find`("복사")로 코드 블록의 복사 버튼을 찾아 클릭, `copy-btn.copied` 상태(초록
   배경)로 바뀌는지 `read_page`로 확인.
5. 퀴즈 섹션까지 스크롤해 "정답 확인" 버튼을 클릭, 정답 박스가 펼쳐지는지 확인(`assets/js/quiz.js` 동작
   유지 확인).
6. `mcp__Claude_Browser__resize_window`(`preset: "mobile"`)로 전환 후 스크린샷 — TOC가 상단으로 접히고
   레이아웃이 깨지지 않는지 확인 후 `preset: "desktop"`으로 되돌린다.

- [ ] **Step 4: 커밋**

```bash
git add lectures/week01/index.html
git commit -m "$(cat <<'EOF'
1차시 강의 페이지를 FabMetric Telemetry 톤으로 재스킨

Google Fonts(Inter/JetBrains Mono)를 로드하고 flow-svg의 하드코딩
색상을 common.css 토큰 기준으로 정리한다.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: `docs/design-system.md` 작성 (롤아웃 가이드)

**Files:**
- Create: `docs/design-system.md`

**Interfaces:**
- Consumes: Task 1~3에서 확정된 토큰 목록과 패턴.
- Produces: 다음 세션이 2~10차시/`worksheet.html`로 롤아웃할 때 참고할 체크리스트.

- [ ] **Step 1: 문서 작성**

`docs/design-system.md`를 아래 내용으로 생성한다.

```markdown
# 디자인 시스템 — FabMetric Telemetry

`assets/css/common.css`가 정의하는 공통 디자인 토큰과, 다른 차시/`worksheet.html`로 새 디자인을
롤아웃할 때 따라야 할 절차를 정리한다. 배경: `stitch-reference/`의 목업(`DESIGN.md`, `code.html`,
`screen.png`)과 `docs/superpowers/specs/2026-09-19-fabmetric-design-system-pilot-design.md`.

## 토큰 목록 (`assets/css/common.css` `:root`)

| 변수 | 값 | 용도 |
|---|---|---|
| `--blue` / `--blue-bg` / `--blue-line` / `--blue-hover` | `#2563eb` / `#eff6ff` / `#bfdbfe` / `#1d4ed8` | 개념/주요 액션 |
| `--green` / `--green-bg` / `--green-line` | `#10b981` / `#ecfdf5` / `#a7f3d0` | 정상/합격/성공 |
| `--orange` / `--orange-bg` / `--orange-line` | `#f59e0b` / `#fffbeb` / `#fde68a` | 주의/확인 필요 |
| `--red` / `--red-bg` / `--red-line` | `#ef4444` / `#fef2f2` / `#fecaca` | 이상/불량/오류 |
| `--purple` / `--purple-bg` / `--purple-line` | `#7c3aed` / `#faf5ff` / `#e9d5ff` | 실습/도전 |
| `--cyan` / `--cyan-bg` / `--cyan-line` | `#06b6d4` / `#ecfeff` / `#a5f3fc` | 텔레메트리 보조 강조(신규, 필요할 때만) |
| `--ink` | `#0f172a` | 본문/제목 색 |
| `--muted` | `#64748b` | 보조 텍스트 |
| `--bg` / `--card` / `--line` | `#f8fafc` / `#ffffff` / `#e2e8f0` | 배경/카드/테두리 |
| `--radius` / `--radius-sm` / `--radius-xs` | `16px` / `10px` / `6px` | 카드 / 버튼·입력 / 배지·칩 |
| `--shadow-card` / `--shadow-card-hover` | (common.css 참고) | 카드 기본/hover 그림자 |
| `--font` | Inter 우선, Pretendard/맑은고딕/Noto Sans KR 폴백 | 본문 폰트 |
| `--font-mono` | JetBrains Mono 우선, Consolas/D2Coding 폴백 | 코드/수치 폰트 |

## 다른 페이지에 롤아웃하는 절차

각 차시 `index.html`(2~10차시)에 적용할 때:

1. `<head>`의 `<link rel="stylesheet" href="../../assets/css/common.css">` 위에 Google Fonts 3줄을 추가한다
   (`lectures/week01/index.html` 참고).
2. 페이지 내 `<style>` 블록에서 하드코딩된 hex 색상(`#0f172a`, `#fff` 등)이 있는지
   `grep -n "#[0-9a-fA-F]\{3,6\}"`로 찾아 해당하는 `var(--...)` 토큰으로 교체한다.
3. `--green`/`--orange`가 바뀌었으므로, 이 색을 rgba()로 하드코딩해 그림자 tint 등에 쓴 부분이 있다면
   새 rgb 값(`16,185,129` / `245,158,11`)으로 다시 계산한다.
4. 브라우저 프리뷰(`static-preview`, `http://localhost:8743/lectures/weekNN/index.html`)로 스크린샷 확인 +
   TOC/퀴즈/복사 버튼 등 기존 인터랙션이 그대로 동작하는지 확인한다.
5. 파일 하나 끝날 때마다 커밋한다(한 커밋에 여러 차시를 묶지 않는다).

`worksheet.html`은 대부분 `common.css` 클래스만 상속하므로 보통 손댈 곳이 없다 — 위 2~3번 방식으로
하드코딩 색상 유무만 확인하면 된다. `instructor-guide.md`는 마크다운 문서라 이 디자인 시스템과 무관하다.
```

- [ ] **Step 2: 커밋**

```bash
git add docs/design-system.md
git commit -m "$(cat <<'EOF'
디자인 시스템 롤아웃 가이드 문서 추가

FabMetric Telemetry 토큰 목록과 2~10차시/worksheet 롤아웃 절차를
정리해 다음 세션이 참고할 수 있게 한다.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```
