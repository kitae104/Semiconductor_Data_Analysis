"""강의용 이해 그림을 데이터에서 만드는 스크립트(스펙 부록 B).

- 생성된 주차 데이터(data/weekly/...)를 **읽기만** 한다. 데이터는 generate_weekly_data.py가 만든다.
  9·10차시처럼 웨이퍼 다이 맵이 CSV에 없는 그림은 생성기와 같은 합성 함수(같은 시드)를 불러 다시 그린다.
- 출력: assets/images/generated/weekXX_<주제>.png. 강의에는 .chart-img + .img-caption으로 넣는다.
- 같은 데이터면 몇 번을 돌려도 같은 그림(바이트 동일)이 나온다(난수 미사용, PNG 메타데이터 고정).
- 모든 그림에 "가상 데이터" 표기를 넣는다. 10차시 새 웨이퍼 그림에는 정답 패턴을 넣지 않는다.

실행:
    python scripts/generate_figures.py              # 전부
    python scripts/generate_figures.py week01 week05  # 이름에 이 글자가 든 그림만
"""
import os
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_weekly_data as gen  # noqa: E402  (합성 함수만 쓰고 데이터는 만들지 않는다)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEEKLY = os.path.join(BASE, "data", "weekly")
OUT = os.path.join(BASE, "assets", "images", "generated")

# docs/design-system.md 색 토큰
INK, MUTED, LINE, GRID = "#111827", "#5b6472", "#d9dde3", "#eef0f3"
BLUE, BLUE_BG = "#0b6e69", "#e8f3f2"
GREEN, GREEN_BG = "#1f7a44", "#edf6f0"
ORANGE, ORANGE_BG = "#b25e09", "#fbf3e8"
RED, RED_BG = "#b42318", "#fdf0ef"
GRAY_BG = "#f3f4f6"
PASS_COLOR, FAIL_COLOR = "#bfdcc9", RED
ORANGE_PASS = "#46befa"  # Orange 3.35 합격여부(1) 기본 색 RGB(70,190,250) — Orange 화면과 같은 색이 필요한 그림용
NOTE = "교육용 가상 데이터"

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.edgecolor"] = LINE
plt.rcParams["axes.labelcolor"] = INK
plt.rcParams["xtick.color"] = MUTED
plt.rcParams["ytick.color"] = MUTED


def read(week, name):
    return pd.read_csv(os.path.join(WEEKLY, week, name), encoding="utf-8-sig")


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=120, facecolor="white", metadata={"Software": None})
    plt.close(fig)
    print(f"[그림] {os.path.relpath(path, BASE)}")
    return path


def note(fig, text=NOTE):
    fig.text(0.995, 0.01, text, ha="right", va="bottom", fontsize=9, color=MUTED)


def draw_wafer(ax, x, y, fail, highlight=None, title=None, rings=False, pass_color=PASS_COLOR):
    """다이 격자를 정사각형으로 그린다. 불합격 = 빨강, 합격 = 옅은 초록(pass_color로 바꿀 수 있음)."""
    ax.add_patch(Circle((0, 0), 10.9, facecolor=GRAY_BG, edgecolor=MUTED, lw=1.2))
    boxes = [Rectangle((xi - 0.45, yi - 0.45), 0.9, 0.9) for xi, yi in zip(x, y)]
    colors = np.where(fail, FAIL_COLOR, pass_color)
    ax.add_collection(PatchCollection(boxes, facecolor=colors, edgecolor="white", lw=0.3))
    if rings:  # 가장자리 고리: 중심에서 8칸(112mm)보다 먼 다이를 나누는 선
        ax.add_patch(Circle((0, 0), 8.0, fill=False, edgecolor=INK, lw=1.5, ls="--"))
    if highlight is not None:
        hx, hy = highlight
        ax.add_patch(Rectangle((hx - 0.5, hy - 0.5), 1.0, 1.0, fill=False, edgecolor=INK, lw=2))
    ax.set_xlim(-11.5, 11.5)
    ax.set_ylim(-11.5, 11.5)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=11, color=INK)


# ---------------------------------------------------------------------------
# 1차시
# ---------------------------------------------------------------------------
def fig_week01_process_flow():
    """8대 공정 흐름도. 글자가 작아 보이지 않도록 4칸씩 두 줄로 놓고 글자를 키웠다.
    "여러 번" 되풀이하는 단계(②~⑥)는 같은 색 + "여러 번 되풀이" 표시로 묶는다(원천: A-4)."""
    df = read("week04", "week04_orange_process_flow.csv")
    per_row, w, h, gap, row_gap = 4, 2.3, 3.0, 0.45, 0.9
    y_bottom = 1.9
    y_rows = [y_bottom + h + row_gap, y_bottom]
    fig, ax = plt.subplots(figsize=(10.5, 9.0))
    pos = []
    for i, row in df.iterrows():
        r, c = divmod(i, per_row)
        x0, y0 = c * (w + gap), y_rows[r]
        pos.append((x0, y0))
        repeat = row["반복여부"] == "여러 번"
        face, edge = (BLUE_BG, BLUE) if repeat else ("white", MUTED)
        ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=face, edgecolor=edge, lw=2.2))
        ax.text(x0 + w / 2, y0 + h - 0.22, row["구분"], ha="center", va="center", fontsize=12.5, color=MUTED)
        ax.text(x0 + w / 2, y0 + h - 0.72, f"{row['공정순서']}", ha="center", va="center", fontsize=15,
                fontweight="bold", color="white",
                bbox=dict(boxstyle="circle,pad=0.3", fc=BLUE if repeat else MUTED, ec="none"))
        name = row["공정명"].replace("(", "\n(")
        two = "\n" in name        # 이름이 두 줄이면 글자를 조금 줄여 설명과 겹치지 않게 한다
        ax.text(x0 + w / 2, y0 + h - (1.42 if two else 1.35), name, ha="center", va="center",
                fontsize=16.5 if two else 19, fontweight="bold", color=INK, linespacing=1.05)
        ax.text(x0 + w / 2, y0 + (1.0 if two else 1.2), textwrap.fill(row["생활비유"], 11), ha="center", va="top",
                fontsize=14, color=INK, linespacing=1.35)
        if repeat:
            ax.text(x0 + w / 2, y0 + 0.22, "여러 번 되풀이", ha="center", va="center", fontsize=12.5,
                    fontweight="bold", color=BLUE)
    arrow = dict(arrowstyle="-|>", color=MUTED, lw=2.2, mutation_scale=22)
    for i in range(len(df) - 1):
        (xa, ya), (xb, yb) = pos[i], pos[i + 1]
        if i % per_row != per_row - 1:      # 같은 줄: 오른쪽 화살표
            ax.annotate("", xy=(xb - 0.03, ya + h / 2), xytext=(xa + w + 0.03, ya + h / 2), arrowprops=arrow)
        else:                                # 줄 바꿈: 아래로 내려와 왼쪽으로 꺾어 다음 줄 첫 칸으로
            xs, xe = xa + w / 2, xb + w / 2
            ymid = ya - row_gap / 2
            ax.plot([xs, xs, xe], [ya - 0.03, ymid, ymid], color=MUTED, lw=2.2, solid_capstyle="round")
            ax.annotate("", xy=(xe, yb + h + 0.03), xytext=(xe, ymid), arrowprops=arrow)
    circled = "①②③④⑤⑥⑦⑧"
    front = df.index[df["구분"] == "전공정"]
    back = df.index[df["구분"] == "후공정"]
    rep = df.index[df["반복여부"] == "여러 번"]
    lines = [
        (f"{circled[df.loc[rep.min(), '공정순서'] - 1]} ~ {circled[df.loc[rep.max(), '공정순서'] - 1]} 단계(색이 있는 칸)는 층을 쌓을 때마다 여러 번 되풀이한다", BLUE),
        (f"전공정 {circled[df.loc[front.min(), '공정순서'] - 1]}~{circled[df.loc[front.max(), '공정순서'] - 1]}: 웨이퍼를 만들고 그 위에 회로 만들기", INK),
        (f"후공정 {circled[df.loc[back.min(), '공정순서'] - 1]}~{circled[df.loc[back.max(), '공정순서'] - 1]}: 검사하고 포장하기 (전공정·후공정 분류는 자료마다 조금 다를 수 있음)", INK),
    ]
    for k, (text, color) in enumerate(lines):
        ax.text(0, 1.2 - k * 0.5, text, ha="left", va="center", fontsize=13, color=color)
    ax.set_xlim(-0.2, per_row * (w + gap) - gap + 0.2)
    ax.set_ylim(-0.1, y_rows[0] + h + 0.15)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.04)
    fig.suptitle("반도체 8대 공정 한눈에 보기 (생활 비유)", fontsize=20, fontweight="bold", color=INK, y=0.985)
    note(fig, "공정 이름과 비유는 이해를 돕기 위한 단순화 · 교육용 자료")
    return save(fig, "week01_process_flow.png")


def fig_week01_wafer_to_chip():
    """둥근 웨이퍼의 다이 격자와 다이 하나 확대: 칩 1개 = 다이 1개(원천: A-6 격자)."""
    df = read("week06", "week06_orange_wafer_map.csv")
    x, y = df["다이_X"].to_numpy(), df["다이_Y"].to_numpy()
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 5.4), gridspec_kw={"width_ratios": [1.15, 1]})
    ax.add_patch(Circle((0, 0), 10.9, facecolor=GRAY_BG, edgecolor=MUTED, lw=1.2))
    boxes = [Rectangle((xi - 0.45, yi - 0.45), 0.9, 0.9) for xi, yi in zip(x, y)]
    ax.add_collection(PatchCollection(boxes, facecolor=BLUE_BG, edgecolor=BLUE, lw=0.4))
    ax.add_patch(Rectangle((3 - 0.5, 2 - 0.5), 1.0, 1.0, facecolor=ORANGE, edgecolor=INK, lw=1.5))
    ax.set_xlim(-11.5, 11.5)
    ax.set_ylim(-11.5, 11.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"웨이퍼 1장 = 다이(작은 네모) {len(x)}개", fontsize=12, color=INK)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.add_patch(Rectangle((2.2, 2.6), 5.2, 5.2, facecolor=ORANGE_BG, edgecolor=ORANGE, lw=2.2))
    for i in range(1, 5):
        ax2.plot([2.2 + i * 1.04, 2.2 + i * 1.04], [2.6, 7.8], color=ORANGE_BG, lw=0)
    ax2.text(4.8, 5.2, "칩 1개\n= 다이 1개", ha="center", va="center", fontsize=16, color=INK, fontweight="bold")
    ax2.text(4.8, 1.6, "웨이퍼를 다이 단위로 잘라 포장하면\n우리가 쓰는 반도체 칩이 된다", ha="center", va="center",
             fontsize=11, color=MUTED, linespacing=1.4)
    ax2.text(4.8, 8.8, "피자 도우(웨이퍼)를 조각(칩)으로 나누는 것과 비슷하다", ha="center", fontsize=10.5, color=BLUE)
    fig.add_artist(matplotlib.patches.ConnectionPatch(xyA=(3.5, 2.5), coordsA=ax.transData, xyB=(2.2, 7.8),
                                                      coordsB=ax2.transData, color=MUTED, lw=1, ls="--"))
    fig.add_artist(matplotlib.patches.ConnectionPatch(xyA=(3.5, 1.5), coordsA=ax.transData, xyB=(2.2, 2.6),
                                                      coordsB=ax2.transData, color=MUTED, lw=1, ls="--"))
    fig.suptitle("웨이퍼에서 칩으로", fontsize=15, color=INK)
    note(fig, "다이 간격·개수는 교육용 가상 격자")
    return save(fig, "week01_wafer_to_chip.png")


# ---------------------------------------------------------------------------
# 3·5·6·7·8차시
# ---------------------------------------------------------------------------
def fig_week03_pm10_grade_bands():
    """날짜별 PM10 막대 + 등급 구간 배경색(원천: A-3)."""
    df = read("week03", "week03_orange_air_quality.csv")
    fig, ax = plt.subplots(figsize=(12, 4.8))
    bands = [(0, 30, "좋음", BLUE_BG), (30, 80, "보통", GREEN_BG), (80, 150, "나쁨", ORANGE_BG), (150, 210, "매우나쁨", RED_BG)]
    for lo, hi, label, color in bands:
        ax.axhspan(lo, hi, color=color, zorder=0)
        # 등급 이름은 축 오른쪽 바깥에 둔다(안쪽에 두면 마지막 날 막대에 가려진다)
        ax.text(1.008, (lo + min(hi, 205)) / 2, label, transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=10, color=MUTED)
    colors = [RED if v > 150 else ORANGE if v > 80 else MUTED for v in df["PM10_ug_m3"]]
    ax.bar(range(len(df)), df["PM10_ug_m3"], color=colors, zorder=2, width=0.7)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels([d[-2:] for d in df["날짜"]], fontsize=8)
    ax.set_xlabel("2024년 4월 날짜")
    ax.set_ylabel("PM10 (µg/m³)")
    ax.set_ylim(0, 210)
    ax.set_xlim(-0.6, len(df) - 0.4)
    ax.set_title("하루 측정값을 기준 구간에 비춰 등급을 정한다", fontsize=13, color=INK)
    note(fig, "우리 동네 대기환경 · 교육용 가상 측정값")
    return save(fig, "week03_pm10_grade_bands.png")


def fig_week05_cleanroom_particles():
    """구역별 파티클 추이. 99,999는 축 밖 화살표 + '센서 오류', 빈칸은 끊긴 선(원천: A-5)."""
    df = read("week05", "week05_orange_cleanroom_env.csv")
    fig, ax = plt.subplots(figsize=(12, 5))
    top = 2600
    colors = {"A구역": BLUE, "B구역": ORANGE, "C구역": "#6b7280"}
    for zone, g in df.groupby("구역"):
        hours = pd.to_datetime(g["측정시간"]).dt.hour.to_numpy()
        v = g["파티클_count_per_m3"].to_numpy(dtype=float)
        shown = np.where(v > top, np.nan, v)
        ax.plot(hours, shown, marker="o", ms=4, lw=1.6, color=colors[zone], label=zone)
        for h in hours[np.isnan(v)]:   # 빈 시각: 값처럼 읽히지 않게 세로 점선으로만 표시
            ax.axvline(h, color=colors[zone], ls=":", lw=1.4)
        for h, val in zip(hours[v > top], v[v > top]):
            ax.annotate(f"{int(val):,}\n이 기록의 오류 코드(축 밖)", xy=(h, top - 40), xytext=(h + 1.2, top - 420),
                        fontsize=10, color=RED, arrowprops=dict(arrowstyle="-|>", color=RED))
    fig.text(0.005, 0.01, "세로 점선: 기록이 빈 시각(선이 끊김)", ha="left", va="bottom", fontsize=9.5,
            color=MUTED)
    ax.set_ylim(450, top)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel("측정 시각(시)")
    ax.set_ylabel("파티클 (개/m³)")
    ax.grid(axis="y", color=GRID)
    ax.legend(frameon=False, ncol=3, loc="upper right")
    ax.set_title("클린룸 공기 속 먼지 입자 수 — 하루 동안", fontsize=13, color=INK)
    note(fig, "클린룸 환경 모니터링 · 교육용 가상 데이터(실제 등급 기준 아님)")
    return save(fig, "week05_cleanroom_particles.png")


def fig_week06_wafer_map_reading():
    """웨이퍼 맵 읽는 법: 합격/불합격 색(Orange와 같은 하늘색/빨강), 가장자리 고리, X·Y 축(원천: A-6)."""
    df = read("week06", "week06_orange_wafer_map.csv")
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    draw_wafer(ax, df["다이_X"], df["다이_Y"], df["합격여부"] == -1, rings=True, pass_color=ORANGE_PASS)
    ax.axis("on")
    ax.set_xticks(range(-10, 11, 5))
    ax.set_yticks(range(-10, 11, 5))
    ax.set_xlabel("다이_X")
    ax.set_ylabel("다이_Y")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.legend(handles=[Rectangle((0, 0), 1, 1, color=ORANGE_PASS, label="합격 다이(1)"),
                       Rectangle((0, 0), 1, 1, color=FAIL_COLOR, label="불합격 다이(-1)")],
              loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=10.5)
    ax.annotate("가장자리 고리\n(112mm 바깥)", xy=(-5.66, 5.66), xytext=(-11.4, 11.4), fontsize=9.5, color=INK,
                ha="left", va="top", arrowprops={"arrowstyle": "-", "color": INK, "lw": 1})
    ax.set_title("웨이퍼 맵 읽는 법 — W-0601", fontsize=13, color=INK, pad=28)
    note(fig)
    return save(fig, "week06_wafer_map_reading.png")


# 강의에 싣는 노트북 실행 결과 그림: 정답 노트북에 저장된 출력(image/png)을 그대로 꺼낸다.
# 셀은 코드 첫머리로 찾는다(셀이 늘거나 순서가 바뀌어도 같은 그림). 노트북 빌더를 먼저 돌린다.
NOTEBOOK_CHARTS = {
    "week06": [
        ('plt.bar(counts.index, counts)', "week06_nb_easy_bar_weather.png"),
        ('plt.hist(ice["판매량_count"], bins=5)', "week06_nb_easy_hist_sales.png"),
        ('plt.scatter(ice["최고기온_C"], ice["판매량_count"])', "week06_nb_easy_scatter_temp_sales.png"),
        ('process_counts = df["공정명"].value_counts()', "week06_nb_bar_process.png"),
        ('plt.hist(df["두께_nm"], bins=10)', "week06_nb_hist_thickness.png"),
        ('plt.scatter(df["온도_C"], df["압력_Pa"])', "week06_nb_scatter_temp_pressure.png"),
        ('plt.bar(eq_counts.index, eq_counts)', "week06_nb_bar_equipment.png"),
        ('plt.hist(df["온도_C"], bins=10)', "week06_nb_hist_temperature.png"),
        ('plt.scatter(df["온도_C"], df["두께_nm"])', "week06_nb_scatter_temp_thickness.png"),
        ('fail = df[df["합격여부"] == -1]', "week06_nb_ai_scatter_fail.png"),
    ],
}


def export_notebook_charts(week):
    import base64
    import json

    path = os.path.join(BASE, "notebooks", "solutions", f"{week}_solution.ipynb")
    with open(path, encoding="utf-8") as f:
        cells = [c for c in json.load(f)["cells"] if c["cell_type"] == "code"]
    for head, name in NOTEBOOK_CHARTS[week]:
        found = [c for c in cells if "".join(c["source"]).startswith(head)]
        if len(found) != 1:
            raise SystemExit(f"[그림] {week} 셀 '{head}'이(가) {len(found)}개 — 1개여야 한다")
        pngs = [o["data"]["image/png"] for o in found[0].get("outputs", []) if "image/png" in o.get("data", {})]
        if len(pngs) != 1:
            raise SystemExit(f"[그림] {week} 셀 '{head}'의 그림 출력이 {len(pngs)}개 — 빌더로 정답 노트북을 다시 실행한다")
        out = os.path.join(OUT, name)
        with open(out, "wb") as f:
            f.write(base64.b64decode("".join(pngs[0]) if isinstance(pngs[0], list) else pngs[0]))
        print(f"[그림] {os.path.relpath(out, BASE)}")


def fig_week06_notebook_charts():
    """6차시 강의의 노트북 실행 결과 그림 10장(정답 노트북 출력에서)."""
    export_notebook_charts("week06")


def fig_week07_wafer_maps_by_equipment():
    """3행(설비) × 4열(웨이퍼) 작은 웨이퍼 맵, 칸마다 수율(원천: A-7)."""
    df = read("week07", "week07_orange_wafer_lots.csv")
    fig, axes = plt.subplots(3, 4, figsize=(12, 9.6))
    for r, (eq, g) in enumerate(df.groupby("설비번호")):
        for c, (wid, w) in enumerate(g.groupby("웨이퍼ID")):
            yld = (w["합격여부"] == 1).mean() * 100
            draw_wafer(axes[r, c], w["다이_X"], w["다이_Y"], w["합격여부"] == -1, title=f"{wid}  수율 {yld:.1f}%")
        axes[r, 0].text(-13, 0, eq, rotation=90, ha="center", va="center", fontsize=13, color=INK)
    fig.suptitle("식각 설비 3대에서 나온 웨이퍼 12장", fontsize=15, color=INK)
    note(fig)
    return save(fig, "week07_wafer_maps_by_equipment.png")


def fig_week08_correlation_signs():
    """산점도 3개: RF파워(+), 누적사용시간(-), 챔버온도(≈0)와 식각률, 칸마다 r(원천: A-8)."""
    df = read("week08", "week08_orange_chamber_sensor.csv")
    pairs = [("RF파워_W", "RF파워 (W)"), ("누적사용시간_hr", "누적 사용 시간 (시간)"), ("챔버온도_C", "챔버 온도 (℃)")]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=True)
    for ax, (col, label) in zip(axes, pairs):
        r = df[col].corr(df["식각률_nm_min"])
        ax.scatter(df[col], df["식각률_nm_min"], s=14, color=BLUE, alpha=0.7)
        ax.set_xlabel(label)
        ax.set_title(f"r = {r:+.2f}", fontsize=13, color=INK)
        ax.grid(color=GRID)
    axes[0].set_ylabel("식각률 (nm/min)")
    fig.suptitle("상관계수의 부호: 같이 오르는지(+), 반대로 움직이는지(-), 관계가 거의 없는지(0)", fontsize=13, color=INK)
    note(fig, "식각 챔버 센서 기록 · 교육용 가상 관계(실제 장비 법칙 아님)")
    fig.tight_layout(rect=(0, 0.03, 1, 0.93))
    return save(fig, "week08_correlation_signs.png")


def fig_week08_vacuum_u_shape():
    """진공도 구간별 불합격률 막대 3개(4.5 미만 / 연습용 기준 안 / 5.5 초과) + 기준선(원천: week08_anomaly_root_cause)."""
    df = read("week08", "week08_anomaly_root_cause.csv")
    v, fail = df["진공도_mTorr"], df["합격여부"] == -1
    groups = [("4.5 미만", v < 4.5), ("4.5~5.5\n(연습용 기준 안)", (v >= 4.5) & (v <= 5.5)), ("5.5 초과", v > 5.5)]
    base = fail.mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for i, (label, m) in enumerate(groups):
        rate = fail[m].mean() * 100
        ax.bar(i, rate, color=MUTED if i == 1 else RED, width=0.6, zorder=2)
        label_txt = f"{rate:.1f}%\n({int(fail[m].sum())}/{int(m.sum())}건)"
        if i == 1:  # 가운데 막대는 기준선보다 낮아 글자를 막대 안에 둔다(점선과 겹치지 않게)
            ax.text(i, rate / 2, label_txt, ha="center", va="center", fontsize=11, color="white", zorder=4)
        else:
            ax.text(i, rate + 0.8, label_txt, ha="center", va="bottom", fontsize=11, color=INK)
    ax.axhline(base, color=BLUE, linestyle="--", linewidth=1.2, zorder=3)
    ax.text(0.5, base + 0.6, f"기준선 {base:.1f}%", ha="center", va="bottom", fontsize=10, color=BLUE)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[0] for g in groups])
    ax.set_xlabel("진공도_mTorr 구간")
    ax.set_ylabel("불합격률 (%)")
    ax.set_ylim(0, 36)
    ax.grid(axis="y", color=GRID, zorder=0)
    ax.set_title("진공도는 낮은 쪽과 높은 쪽 모두에서 불합격률이 높다", fontsize=13, color=INK)
    note(fig, "공정 센서 기록 450건 · 연습용 기준(실제 공정 규격 아님) · 교육용 가상 데이터")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return save(fig, "week08_vacuum_u_shape.png")


# ---------------------------------------------------------------------------
# 9·10차시 — 합성 함수로 같은 웨이퍼 맵을 다시 만든다
# ---------------------------------------------------------------------------
def fig_week09_wafer_pattern_examples():
    """정상·중심형·가장자리형·스크래치형 예시 웨이퍼 4장(A-9에서 패턴별 첫 웨이퍼)."""
    x, y, _ = gen.die_grid()
    first = {}
    for wid, label, fail in gen.week09_wafer_maps():
        first.setdefault(label, (wid, fail))
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.2))
    for ax, label in zip(axes, ["정상", "중심형", "가장자리형", "스크래치형"]):
        wid, fail = first[label]
        draw_wafer(ax, x, y, fail, title=f"{label}  ({wid}, 불량 다이 {int(fail.sum())}개)")
    fig.suptitle("웨이퍼 맵 불량 패턴 4가지", fontsize=15, color=INK)
    note(fig)
    return save(fig, "week09_wafer_pattern_examples.png")


def fig_week10_new_wafer_maps():
    """새 웨이퍼 10장 맵. 정답 패턴은 넣지 않는다(A-10)."""
    x, y, _ = gen.die_grid()
    fig, axes = plt.subplots(2, 5, figsize=(15, 6.6))
    for ax, (wid, fail) in zip(axes.ravel(), gen.week10_wafer_maps()):
        draw_wafer(ax, x, y, fail, title=f"{wid}  (불량 다이 {int(fail.sum())}개)")
    fig.suptitle("새로 들어온 웨이퍼 10장 — 모델은 어떤 패턴이라고 답할까?", fontsize=15, color=INK)
    note(fig)
    return save(fig, "week10_new_wafer_maps.png")


FIGURES = [
    fig_week01_process_flow, fig_week01_wafer_to_chip, fig_week03_pm10_grade_bands,
    fig_week05_cleanroom_particles, fig_week06_wafer_map_reading, fig_week06_notebook_charts,
    fig_week07_wafer_maps_by_equipment,
    fig_week08_correlation_signs, fig_week08_vacuum_u_shape, fig_week09_wafer_pattern_examples, fig_week10_new_wafer_maps,
]


def main():
    keys = sys.argv[1:]
    for fn in FIGURES:
        if not keys or any(k in fn.__name__ for k in keys):
            fn()


if __name__ == "__main__":
    main()
