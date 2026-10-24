# 강의 HTML 마크업 규격

`lectures/weekXX/index.html`과 `worksheet.html`의 골격과 컴포넌트 전문.
**여기 없는 클래스는 쓰지 않는다** — `assets/css/common.css`에 정의된 것만 유효하다
(CLAUDE.md: 새 CSS 프레임워크 도입 금지).

## 목차

- [페이지 골격](#페이지-골격)
- [히어로](#히어로)
- [PART 섹션](#part-섹션)
- [콜아웃](#콜아웃)
- [찾아보기 상자](#찾아보기-상자)
- [코드 블록](#코드-블록)
- [용어 카드](#용어-카드)
- [표](#표)
- [정답 토글](#정답-토글)
- [내비게이션 버튼](#내비게이션-버튼)
- [이미지와 차트](#이미지와-차트)
- [랜딩 전용 컴포넌트](#랜딩-전용-컴포넌트)
- [전체 클래스 목록](#전체-클래스-목록)
- [자주 저지르는 실수](#자주-저지르는-실수)

---

## 페이지 골격

### 강의 자료 `index.html`

`{N}`은 차시 번호(1~10), `{NN}`은 두 자리(01~10)다. 상대경로는 `lectures/weekNN/` 기준이다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{N}차시. {제목}</title>
<link rel="icon" href="../../assets/images/site/chip-favicon.png" type="image/png">
<link rel="stylesheet" href="../../assets/css/common.css">
<link rel="stylesheet" href="../../assets/css/print.css">
<style>
  /* 이 페이지에만 필요한 스타일(예: 개념도 SVG)만. 전역 스타일은 design-steward 영역 */
</style>
</head>
<body>
<header class="site-header">
  <div class="header-row">
    <a class="brand" href="../../index.html"><img src="../../assets/images/site/chip-macro-logo.jpg" alt="" aria-hidden="true" class="brand-logo" width="34" height="34" /> 반도체 데이터 분석 10차시 과정
      <small>Semiconductor Process Data Analysis</small>
    </a>
    <nav class="week-nav">
      <a href="../week01/index.html">1차시</a>
      <!-- … 10차시까지 모두. 현재 차시에만 class="current" … -->
      <a href="../week{NN}/index.html" class="current">{N}차시</a>
    </nav>
  </div>
  <div class="progress-track"><div class="progress-fill" id="progressFill" data-week="{N}"></div></div>
</header>

<main class="page">
  <div class="hero">…</div>
  <section class="block">…</section>
  <!-- 섹션 반복 -->
</main>

<footer class="site-footer">반도체 및 반도체 공정 데이터 분석 10차시 과정 · {N}차시 · 교육용 자료(가상 데이터 사용)</footer>
<script src="../../assets/js/common.js"></script>
<script src="../../assets/js/quiz.js"></script>
</body>
</html>
```

**검사에서 잡히는 것**: `week-nav`는 1~10차시 링크가 모두 있어야 하고 `current`는 정확히
현재 차시 하나여야 한다. `data-week`도 차시 번호와 일치해야 한다. 진행률 표시줄이 이 값을 쓴다.

### 실습지 `worksheet.html`

더 단순하다. 주차 내비 대신 강의로 돌아가는 링크 하나, 진행률 표시줄 없음, 스크립트는
정답 토글이 있을 때만 필요하다.

```html
<header class="site-header">
  <div class="header-row">
    <a class="brand" href="../../index.html"><img src="../../assets/images/site/chip-macro-logo.jpg" alt="" aria-hidden="true" class="brand-logo" width="34" height="34" /> 반도체 데이터 분석 10차시 과정</a>
    <nav class="week-nav"><a href="index.html">← {N}차시 강의로</a></nav>
  </div>
</header>
<main class="page">
  <div class="hero">
    <span class="badge purple">{N}차시 실습지</span>
    <h1>{제목} — 실습지</h1>
  </div>
  <section class="block">
    <h2>1. 용어 연결 문제</h2>
    …
  </section>
</main>
```

---

## 히어로

강의 자료는 `blue` 배지 + 오늘의 질문, 실습지는 `purple` 배지.

```html
<div class="hero">
  <span class="badge blue">{N}차시</span>
  <h1>{제목}</h1>
  <p class="today-question">오늘의 질문: <b>"{한 문장 질문}"</b></p>
</div>
```

배지 색: `blue`(강의) · `purple`(실습/도전) · `green`(정상/합격) · `warn`(주의) · `danger`(이상).

**오늘의 미션(v3)** — 오늘의 질문 바로 아래 한 줄, 그 아래 오늘 끝에 Orange로 볼 그림 자리.

```html
<p class="lede"><b>오늘의 미션</b> — 입사 첫날, 공장 기록표 40건을 받았다. 합격·불합격이 몇 건인지 한 문장으로 보고하자.</p>
<img class="chart-img" src="../../assets/images/orange3/week01_mission.png"
     alt="오늘 끝에 Orange3로 보게 될 합격·불합격 막대" data-shot="2_process_done.ows의 Distributions 창 — 합격여부 막대 두 개">
```

---

## PART 섹션

v3(2026-10-23) 강의는 PART 세 개다. **"오늘 수업 구성" 표와 "실습 파일 받기·노트북 열기" 단계는 두지 않는다**(2026-10-24,
실습 환경에 파일·노트북이 미리 배치돼 있다). 시간 열도 두지 않는다.

PART 머리 섹션은 `section.block > h2` 구조를 지켜 자동 목차에 잡히게 한다.

```html
<section class="block" id="part1">
  <h2><span class="step-badge">PART 1</span> 파이썬 — 변수와 출력</h2>
  <p>개념은 생활 예제로 배우고, 공장 기록은 "반도체 데이터로 확인하기"에서 다룬다.</p>
</section>
<!-- 이어서 개념 섹션들, 반도체 데이터로 확인하기, 실습 따라 하기 -->
<section class="block" id="part2">
  <h2><span class="step-badge">PART 2</span> Orange3 — 표를 눈으로 보기</h2>
  …위젯 이름표 표, 워밍업, 반도체, 파이썬 결과와 비교…
</section>
<section class="block" id="part3">
  <h2><span class="step-badge">PART 3</span> 실습지</h2>
  …
</section>
```

9·10차시는 `id="part1"`이 Orange3, `id="part2"`가 파이썬 최소 + ChatGPT 체험이다(id는 위치 기준).

**위젯 이름표** — PART 2(9·10차시는 PART 1) 첫머리의 표. 영어 이름은 Orange 3.35 화면 그대로 쓴다.

```html
<div class="tablewrap">
  <table>
    <thead><tr><th>위젯(화면 이름)</th><th>한국어 뜻</th><th>오늘 하는 일</th></tr></thead>
    <tbody><tr><td><code>Distributions</code></td><td>분포 막대</td><td>합격·불합격이 각각 몇 건인지 막대로 본다</td></tr></tbody>
  </table>
</div>
```

---

## 콜아웃

강조 상자. 5종이고 각각 의미가 정해져 있다 — 색을 장식으로 쓰지 않는다.

```html
<div class="callout concept"><b>개념</b> — 설명</div>
<div class="callout practice"><b>해보기</b> — 실습 지시</div>
<div class="callout success"><b>확인</b> — 잘 됐을 때의 모습</div>
<div class="callout warn"><b>주의</b> — 헷갈리기 쉬운 점</div>
<div class="callout danger"><b>하지 말 것</b> — 오류로 이어지는 행동</div>
```

| 클래스 | 용도 |
|---|---|
| `concept` | 개념 설명, 비유 |
| `practice` | 학생이 지금 손을 움직여야 할 것 |
| `success` | 정상 결과, 성공 기준 |
| `warn` | 주의, 흔한 혼동 |
| `danger` | 오류, 금지 |

---

## 찾아보기 상자

v3(2026-10-23) 신규. 기존 `callout concept` + `tag`만 쓴다(새 클래스 없음). 확인 포인트는 정답 토글과 같은 규칙 —
`reveal-btn` **바로 다음 형제**가 `answer-box`여야 열린다. 버튼 글자는 "~ 보기"로 끝낸다.

```html
<div class="callout concept">
  <b class="tag">찾아보기</b>
  <p>AI 답은 틀릴 수 있으니 확인 포인트와 비교하세요. 개인정보·실제 회사 데이터는 넣지 마세요.</p>
  <p><b>검색어</b> <code>웨이퍼 왜 둥근가</code></p>
  <div class="code-block">
    <div class="code-label"><span>ChatGPT에 물어보기 — 복사해서 붙여 넣기</span><button class="copy-btn">복사</button></div>
    <pre style="white-space:pre-wrap;"><code>반도체를 처음 배우는 사람에게 웨이퍼가 왜 둥근지 3문장으로 쉽게 설명해줘.</code></pre>
  </div>
  <button class="reveal-btn">확인 포인트 보기</button>
  <div class="answer-box">좋은 답이라면 "실리콘 덩어리(잉곳)를 둥글게 키운 뒤 얇게 자른다"는 내용이 들어 있다.</div>
</div>
```

- 한 상자에 질문이 여러 개면 검색어·복사 블록 묶음을 반복하고, 확인 포인트 토글은 상자 끝에 하나만 둔다.
- 검사 스크립트가 차시당 상자 수(3~6)를 센다 — 태그 글자는 정확히 `찾아보기`로 쓴다.

---

## 코드 블록

복사 버튼은 `common.js`가 `.code-block` 안의 `.copy-btn`과 `pre code`를 찾아 연결한다.
이 구조를 벗어나면 복사가 동작하지 않는다.

```html
<div class="code-block">
  <div class="code-label"><span>Python</span><button class="copy-btn">복사</button></div>
  <pre><code>import pandas as pd

df = pd.read_csv("../../data/weekly/week04/week04_process_filtering.csv", encoding="utf-8-sig")
print(df.head())</code></pre>
</div>
```

- 라벨에 설명을 덧붙일 수 있다: `<span>Python — 특정 설비만 찾기</span>`
- `<code>` 안은 **HTML 이스케이프**가 필요하다: `<` → `&lt;`, `&` → `&amp;`
- 경로는 노트북 기준(`../../data/...`)으로 쓴다. 학생이 노트북에 그대로 붙여넣기 때문이다.

---

## 용어 카드

네 칸이 고정이다. 비전공자에게는 "쉬운 비유"와 "자주 하는 오해"가 실제로 가장 큰 도움이 된다.

```html
<div class="term-grid">
  <div class="term-card">
    <h4>DataFrame</h4><div class="en">DataFrame</div>
    <dl>
      <dt>한 줄 설명</dt><dd>Pandas가 CSV를 읽어 만든 행·열 구조의 표.</dd>
      <dt>쉬운 비유</dt><dd>엑셀 시트, 또는 딕셔너리가 여러 개 담긴 리스트.</dd>
      <dt>데이터에서의 예</dt><dd><code>df = pd.read_csv(...)</code></dd>
      <dt>자주 하는 오해</dt><dd>리스트·딕셔너리와 완전히 다른 개념이라고 생각하기 쉽다. 사실 개념적으로 매우 비슷하다.</dd>
    </dl>
  </div>
</div>
```

---

## 표

가로 스크롤 래퍼로 감싼다. 좁은 화면에서 표가 페이지를 밀어내는 것을 막는다.

```html
<div class="tablewrap">
  <table>
    <thead><tr><th>열</th><th>설명</th></tr></thead>
    <tbody><tr><td>온도_섭씨</td><td>공정 온도</td></tr></tbody>
  </table>
</div>
```

수업 흐름 표에는 `.timetable`을 쓸 수 있다.

---

## 정답 토글

`quiz.js`가 `.reveal-btn`의 **바로 다음 형제**가 `.answer-box`일 때만 동작시킨다.
사이에 다른 요소를 끼우면 열리지 않는다.

```html
<div class="quiz-item">
  <p><b>Q1.</b> DataFrame에서 열 두 개를 함께 선택하는 올바른 코드는?</p>
  <button class="reveal-btn">정답 보기</button>
  <div class="answer-box">정답: <code>df[["온도_섭씨", "압력_Pa"]]</code> — 여러 열은 리스트로 감싼다.</div>
</div>
```

---

## 내비게이션 버튼

섹션 끝의 이전/다음 차시 이동.

```html
<div class="nav-buttons">
  <a href="../week03/index.html">← 이전 차시: 3차시</a>
  <a href="../week05/index.html">다음 차시: 5차시 →</a>
</div>
```

`.btn-primary` / `.btn-secondary` / `.btn-row`는 **히어로·CTA용**이다. `.nav-buttons`와
섞어 중첩하지 않는다.

---

## 이미지와 차트

5~10차시는 `assets/images/weekNN/`에 실제 matplotlib 산출물이 있다. **직접 그린 SVG보다
실제 결과 이미지를 우선 쓴다** — 진짜 산출물이기 때문이다.

```html
<img class="chart-img" src="../../assets/images/week06/nb_hist_temperature.png" alt="온도 분포 히스토그램">
<p class="img-caption">6차시 실습에서 생성한 온도 히스토그램</p>
```

**예시 일러스트레이션**(실제 데이터가 아닌 것)은 반드시 셋을 지킨다:
① 제목·라벨에 "예시" 표기 ② `LIVE`/`실시간` 표현 금지 ③ 섹션 상단에 고지

```html
<p class="illustration-note">예시 일러스트레이션 · 실제 데이터 아님</p>
```

---

## 랜딩 전용 컴포넌트

아래는 `index.html`(루트) 전용이다. 차시 페이지에 쓰지 않는다.

| 클래스 | 용도 |
|---|---|
| `.hero-home`, `.hero-with-stats`, `.stat-panel` | 랜딩 히어로와 스탯 패널 |
| `.tab-strip` | 헤더 안 페이지 내 앵커 내비 |
| `.outcome-grid` / `.outcome-card` | 학습 목표 카드 3열 |
| `.telemetry-grid` / `.telemetry-card` | 대시보드형 미리보기 (예시 고지 필수) |
| `.journey`, `.jstep`, `.journey-arrow` | 과정 흐름도 |
| `.cta-banner` | 하단 다크 CTA (인쇄 시 `print.css`가 숨김) |
| `.footer-status` / `.chip` | 푸터 상태 칩 — **검증 가능한 사실만** |

`.stat-panel`에는 **본문에 실제로 등장하는 값만** 넣는다. `.footer-status`에는 "Online" 같은
가짜 가동 상태를 넣지 않는다(`docs/design-system.md`).

차시 페이지에는 `.breadcrumb`와 `.section-kicker`를 쓸 수 있다.

```html
<span class="section-kicker"><span class="dot"></span>PANDAS BASICS</span>
```

---

## 전체 클래스 목록

`common.css`에 정의된 것 전부. 이 밖의 클래스를 쓰면 검사에서 FAIL이다.

**레이아웃**: `page` `page-body` `page-content` `block` `hero` `hero-home` `hero-with-stats`
`hero-stats` `hero-side-img` `hero-bg-chart` `site-header` `site-footer` `header-row` `brand`
`brand-group` `brand-logo` `brand-text` `week-nav` `breadcrumb` `tab-strip` `progress-track`
`progress-fill` `nav-buttons` `btn-row` `btn-primary` `btn-secondary` `on-dark` `cta-banner`
`footer-status` `chip`

**콘텐츠**: `callout`(+`concept` `practice` `success` `warn` `danger`) `code-block` `code-label`
`copy-btn` `copied` `term-grid` `term-card` `en` `tablewrap` `timetable` `goal-list` `explain-list`
`pt-list` `step` `step-badge` `badge`(+`blue` `green` `purple` `warn` `danger` `accent`)
`section-kicker` `dot` `lede` `today-question` `mono` `num` `tag` `sep`

**퀴즈·정답**: `quiz-item` `reveal-btn` `reveal-init` `answer-box` `shown` `revealed` `q` `options`

**이미지·도해**: `chart-img` `img-caption` `photo-slot` `illustration-note` `concept-panel`
`cp-visual` `cp-info` `oflow-wrap` `oflow-svg` `oflow-note` `obox` `oarrow` `oarrowhead` `okicker`
`olabel` `osub` `data-preview`

**랜딩**: `outcome-grid` `outcome-card` `telemetry-grid` `telemetry-card` `tstats` `tsub`
`stat-panel` `stat` `journey` `jstep` `journey-arrow` `jcode` `jnum` `j1` `j2` `j3` `j4`
`toc-box` `toc-head` `toc-title` `toc-list` `toc-toggle` `collapsed` `home` `current`

정확한 최신 목록은 직접 확인한다:

```bash
grep -oE '\.[a-zA-Z][a-zA-Z0-9_-]*' assets/css/common.css | sort -u
```

---

## 자주 저지르는 실수

| 실수 | 결과 |
|---|---|
| `common.css`에 없는 클래스 작명 | 스타일이 안 먹고 검사에서 FAIL |
| `.code-block` 구조를 바꿈 | 복사 버튼이 동작하지 않음 |
| `.reveal-btn`과 `.answer-box` 사이에 요소를 끼움 | 정답 토글이 열리지 않음 |
| `section.block > h2`를 안 씀 | 자동 목차에서 누락 |
| `week-nav`의 `current`를 안 옮김 | 다른 차시가 현재로 표시 |
| `data-week`를 안 고침 | 진행률 표시줄이 틀림 |
| `<code>` 안에 `<`를 그대로 씀 | HTML이 깨짐 |
| 없는 이미지를 참조 | 검사에서 FAIL (상대경로 대상 없음) |
| 강의 코드와 노트북 코드가 다름 | 수업 중에 학생이 막힘 |
