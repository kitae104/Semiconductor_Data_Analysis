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
