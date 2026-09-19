# FabMetric Telemetry 디자인 시스템 도입 — 파일럿 (랜딩 + 1차시)

날짜: 2026-09-19
범위: 파일럿 (`index.html` + `lectures/week01/index.html`), `assets/css/common.css` 토큰/컴포넌트 전면 갱신

## 배경 및 목표

`stitch-reference/stitch_dashboard`(랜딩 페이지 목업)와 `stitch-reference/stitch_lecture`(차시 페이지 목업)에
"FabMetric Telemetry"라는 디자인 시스템(`DESIGN.md`)이 정의되어 있다. 두 목업은 Tailwind CDN으로 만들어졌지만,
`CLAUDE.md`가 새 CSS 프레임워크 도입과 `assets/css/common.css` 외 클래스 사용을 금지하므로 Tailwind를 가져오지
않고 **색상·타이포·그림자·둥근 모서리 토큰만 추출**해 기존 `common.css`에 이식한다.

목표는 두 가지다.
1. 랜딩 페이지와 1차시 강의 페이지를 새 톤으로 재스킨한다.
2. `common.css`의 **기존 CSS 변수명을 그대로 유지**한 채 값만 갱신해서, 이후 2~10차시·`worksheet.html`
   롤아웃 시 HTML을 거의 건드리지 않고 CSS 값만 바꿔도 전체 사이트에 새 디자인이 전파되도록 한다.

## 범위

**포함 (이번 파일럿)**
- `assets/css/common.css`: 색상/타이포/그림자/반경 토큰 갱신 + 헤더·카드·버튼 등 컴포넌트 스타일 값 조정 (구조는 유지)
- `index.html`: Google Fonts(Inter, JetBrains Mono) 로드, 인라인 `<style>` 내 하드코딩 색상값을 토큰 기준으로 정리,
  5번째 줄의 깨진 텍스트(`goekd`) 제거
- `lectures/week01/index.html`: 동일하게 폰트 로드 + 인라인 하드코딩 색상 정리
- 신규 문서 `docs/design-system.md`: 토큰 목록과 다음 세션에서 2~10차시/`worksheet.html`/`instructor-guide.md`에
  롤아웃하는 방법 정리

**제외 (이번 파일럿에서는 손대지 않음, 후속 작업)**
- `lectures/week02~10/index.html`, 모든 `worksheet.html`, `instructor-guide.md` — `common.css`를 공유하므로
  토큰 변경의 영향은 즉시 받지만(자동 재스킨), 각 파일 내부의 하드코딩된 색상이나 레이아웃은 이번에 손대지 않는다.
- 헤더/내비게이션 **구조** (sticky 헤더, week 알약 내비, 좌측 TOC 사이드바, 진행률 바, 맨 위로 버튼의 DOM 구조와 동작) —
  색상·타이포만 교체하고 구조는 그대로 둔다.
- `data/`, `notebooks/`, `scripts/` — 데이터·노트북 관련 작업 없음, 검증 스크립트 실행 불필요.
- 목업의 가짜 실시간 수치(`Lot #WF-882: 98.7%`, 웨이퍼 맵 등)를 그대로 복제하지 않는다 — 실제로 없는
  실시간 텔레메트리 기능처럼 오해될 수 있으므로, 장식용 시각 요소는 기존 콘텐츠(변수 애니메이션, 학습 여정 카드 등)의
  톤만 바꾸는 데 그친다.

## 디자인 토큰 매핑

`common.css`의 기존 변수명은 유지하고 값만 갱신한다. 신규 변수는 최소한으로 추가한다.

| 변수 | 기존 값 | 새 값 | 비고 |
|---|---|---|---|
| `--ink` | `#1e293b` | `#0f172a` | FabMetric navy (on-surface) |
| `--muted` | `#64748b` | (유지) | 이미 일치 |
| `--bg` | `#f8fafc` | (유지) | 이미 일치 |
| `--card` | `#ffffff` | (유지) | 이미 일치 |
| `--line` | `#e2e8f0` | (유지) | 이미 일치 |
| `--blue` | `#2563eb` | (유지) | primary, 이미 일치 |
| `--blue-bg` / `--blue-line` | 기존값 | (유지) | |
| `--blue-hover` *(신규)* | — | `#1d4ed8` | 버튼/링크 hover |
| `--green` | `#16a34a` | `#10b981` | emerald / pass 상태 |
| `--green-bg` | `#f0fdf4` | `#ecfdf5` | |
| `--green-line` | `#bbf7d0` | `#a7f3d0` | |
| `--orange` | `#ea580c` | `#f59e0b` | amber / 주의·drift 상태 |
| `--orange-bg` | `#fff7ed` | `#fffbeb` | |
| `--orange-line` | `#fed7aa` | `#fde68a` | |
| `--red` | `#dc2626` | `#ef4444` | rose / 이상·fault 상태 |
| `--red-bg` / `--red-line` | 기존값 | (유지) | |
| `--purple` | `#7c3aed` | (유지) | tertiary, 이미 일치 |
| `--purple-bg` | `#f5f3ff` | `#faf5ff` | |
| `--purple-line` | `#ddd6fe` | `#e9d5ff` | |
| `--cyan` *(신규)* | — | `#06b6d4` | telemetry cyan accent |
| `--cyan-bg` / `--cyan-line` *(신규)* | — | `#ecfeff` / `#a5f3fc` | |
| `--radius` | `14px` | `16px` | 카드 |
| `--radius-sm` *(신규)* | — | `10px` | 버튼/입력 |
| `--radius-xs` *(신규)* | — | `6px` | 배지/칩 |
| `--shadow-card` *(신규)* | — | `0 1px 3px rgba(15,23,42,.06), 0 1px 2px rgba(15,23,42,.04)` | |
| `--shadow-card-hover` *(신규)* | — | `0 10px 25px -3px rgba(15,23,42,.08), 0 4px 6px -4px rgba(15,23,42,.04)` | |
| `--font` | `"Pretendard","Malgun Gothic","Segoe UI",-apple-system,sans-serif` | `"Inter","Pretendard","Malgun Gothic","Noto Sans KR",-apple-system,sans-serif` | Inter 우선, 한글 폴백 유지 |
| `--font-mono` *(신규)* | (인라인 `"Consolas","D2Coding",monospace`) | `"JetBrains Mono","Consolas","D2Coding",monospace` | 코드/수치용 |

`--maxw`(1180px)는 변경하지 않는다 (레이아웃 폭 유지, 헤더/내비 구조 불변 요구와 일치).

## 컴포넌트 변경

- **헤더(`.site-header`)**: 파란 그라디언트 → 다크 네이비(`#0f172a` 계열) 배경. `week-nav` 알약 내비의 마크업·동작은 그대로,
  `current` 상태 배색만 새 토큰 기준으로 재확인.
- **카드류** (`section.block`, `.week-card`, `.hero-home`, `.term-card`, `.journey .jstep`, `.anim-card`): `box-shadow`를
  `var(--shadow-card)`/`var(--shadow-card-hover)`로, `border-radius`를 `var(--radius)`로 통일.
- **버튼/링크** (`.nav-buttons a`, `.anim-link`, `.links-row a`, `.reveal-btn`): 배경 `var(--blue)`, hover
  `var(--blue-hover)`로 정리. 모서리는 `var(--radius-sm)`.
- **배지/칩/콜아웃/퀴즈/코드블록**: 구조 변경 없이 토큰 값 갱신만 반영(자동 적용).
- **코드 블록**: `font-family`에 `var(--font-mono)` 우선 적용.
- **본문 타이포그래피**: 기존 rem 기반 크기 체계는 유지(레이아웃 리플로우 방지), 폰트 스택만 Inter 우선으로 교체.

## Google Fonts 로딩

`index.html`, `lectures/week01/index.html`의 `<head>`에 다음을 추가한다(참고 목업과 동일한 subset):

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

이후 2~10차시로 롤아웃할 때도 동일한 스니펫을 각 페이지 `<head>`에 추가하면 된다(`docs/design-system.md`에 기록).

## 기타 수정

- `index.html` 5번째 줄 `<meta name="viewport" ... />` 뒤에 붙어 있는 `goekd`라는 깨진 텍스트를 제거한다
  (디자인과 무관한 기존 마크업 손상).

## 검증 계획

데이터/노트북 변경이 없으므로 `scripts/validate_datasets.py`, `scripts/validate_notebooks.py`는 실행 대상이 아니다.
대신 브라우저로 시각 검증한다.

1. `index.html`, `lectures/week01/index.html`을 브라우저 프리뷰로 열어 스크린샷 비교(변경 전/후).
2. 콘솔 에러 없는지 확인(특히 Google Fonts 로드 실패 시 폴백 정상 동작).
3. 모바일 폭(≤640px)에서 헤더/카드/네비 레이아웃 깨짐 없는지 확인.
4. `lectures/week01/index.html`의 TOC 사이드바, 퀴즈 정답 토글, 코드 복사 버튼 등 기존 JS 기능이 재스킨 후에도
   정상 동작하는지 클릭 테스트.
5. 인쇄 스타일(`assets/css/print.css`)이 새 토큰에도 깨지지 않는지 간단히 확인(생략 가능, 구조 변경 없음).

## 후속 롤아웃 (이번 파일럿 이후, 별도 세션)

`docs/design-system.md`에 다음을 남겨 다음 세션이 참고하게 한다.
- 토큰 목록과 의미
- 2~10차시 `index.html`에 Google Fonts 스니펫 추가 + 인라인 하드코딩 색상 점검 체크리스트
- `worksheet.html`은 공통 토큰만 상속(구조 변경 없음) — 별도 작업 불요, 확인만
- `instructor-guide.md`는 마크다운이라 이 디자인 시스템과 무관
