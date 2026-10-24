"""주차별(1~10주) 교육용 실습 데이터를 생성하는 스크립트.

- 모든 데이터는 완전한 교육용 가상 데이터이며, 실제 기업 생산 데이터가 아니다.
- data/raw의 원본 CSV는 읽기 전용으로만 사용하고 절대 덮어쓰지 않는다.
- 시드를 고정해 몇 번을 실행해도 동일한 데이터가 생성된다.
- 자세한 설계 근거는 docs/data-design.md 를 참고한다.

실행: python scripts/generate_weekly_data.py
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")
WEEKLY = os.path.join(BASE, "data", "weekly")
DICT_DIR = os.path.join(BASE, "data", "data_dictionary")

EQUIPMENT = ["EQ-01", "EQ-02", "EQ-03", "EQ-04"]
PROCESS = ["증착", "식각", "포토", "세정", "산화"]
SHIFT = ["A조", "B조", "C조"]
DEFECT_TYPES = ["두께 불량", "파티클", "패턴 불량", "식각 과다", "식각 부족", "오염", "정렬 불량", "전기적 특성 불량"]


# 열 이름 단위 표기 통일(v3, 2026-10-23): 차시를 재작성할 때 그 차시 CSV만 이름을 바꾼다. 값·난수 흐름은 그대로다.
# 생성기 안에서는 옛 이름으로 만들고 저장 직전에 바꾼다. 아직 재작성하지 않은 차시는 여기에 넣지 않는다.
RENAMED_COLUMNS = {
    "week01_semiconductor_process_overview": {"온도_섭씨": "온도_C"},
    "week02_python_basics_1": {"온도_섭씨": "온도_C"},
    "week03_python_basics_2": {"온도_섭씨": "온도_C"},
    "week04_process_filtering": {"온도_섭씨": "온도_C"},
    "week04_easy_cafe_orders": {"가격_원": "가격_KRW", "수량_개": "수량_count"},
    "week06_process_visualization": {"온도_섭씨": "온도_C"},
    "week06_easy_icecream_daily": {"최고기온_섭씨": "최고기온_C", "판매량_개": "판매량_count"},
    "week07_equipment_yield": {"온도_섭씨": "온도_C"},
    "week07_easy_quiz_results": {"풀이시간_초": "풀이시간_sec"},
    "week08_anomaly_root_cause": {"온도_섭씨": "온도_C", "냉각수온도_섭씨": "냉각수온도_C"},
    "week08_easy_weather_sales": {"최고기온_섭씨": "최고기온_C", "아이스크림_판매량_개": "아이스크림판매량_count",
                                  "핫초코_판매량_잔": "핫초코판매량_cup", "냉동고온도_섭씨": "냉동고온도_C"},
    # 9·10차시는 같은 파일을 함께 쓰므로 한 묶음으로 바꾼다
    "week09_pass_fail_train": {"온도_섭씨": "온도_C"},
    "week09_new_lots_to_predict": {"온도_섭씨": "온도_C"},
    "week10_mini_project_dataset": {"온도_섭씨": "온도_C", "냉각수온도_섭씨": "냉각수온도_C"},
    "week09_easy_outdoor_class": {"최고기온_섭씨": "최고기온_C"},
    "week10_easy_outdoor_class_train": {"최고기온_섭씨": "최고기온_C"},
    "week10_easy_outdoor_class_new_days": {"최고기온_섭씨": "최고기온_C"},
    "week05_dirty_process_data": {"온도_섭씨": "온도_C"},
    "week05_easy_class_records": {"수학_점수": "수학점수_pt"},
}


def save_csv(df: pd.DataFrame, week: str, filename: str):
    out_dir = os.path.join(WEEKLY, week)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"[생성] {path}  ({df.shape[0]}행 x {df.shape[1]}열)")
    return path


def lot_ids(rng, n, prefix="LOT"):
    return [f"{prefix}-{i:04d}" for i in rng.choice(np.arange(1, n * 3), size=n, replace=False)]


def timestamps(rng, n, start="2024-03-01", periods_hours=1500):
    base = pd.Timestamp(start)
    offsets = rng.choice(np.arange(0, periods_hours), size=n, replace=(n > periods_hours))
    ts = [base + pd.Timedelta(hours=int(h)) for h in offsets]
    return sorted(ts)


# ---------------------------------------------------------------------------
# Week 01
# ---------------------------------------------------------------------------
def gen_week01():
    rng = np.random.default_rng(101)
    n = 40
    ts = timestamps(rng, n, periods_hours=300)
    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 999, size=n)],
        "웨이퍼번호": rng.integers(1, 26, size=n),
        "공정명": rng.choice(PROCESS, size=n),
        "설비번호": rng.choice(EQUIPMENT, size=n),
        "온도_섭씨": np.round(rng.normal(300, 3, size=n), 1),
        "압력_Pa": np.round(rng.normal(1010, 8, size=n), 1),
    })
    pass_prob = 0.85
    df["합격여부"] = rng.choice([1, -1], size=n, p=[pass_prob, 1 - pass_prob])
    df = df.rename(columns=RENAMED_COLUMNS["week01_semiconductor_process_overview"])  # 값·난수 흐름은 그대로
    save_csv(df, "week01", "week01_semiconductor_process_overview.csv")
    return df


# ---------------------------------------------------------------------------
# Week 02 (신규) — 파이썬 기초 Ⅰ: 변수·리스트·딕셔너리
# ---------------------------------------------------------------------------
def gen_week02():
    rng = np.random.default_rng(102)
    n = 20
    temp = rng.normal(300, 4, size=n)
    # 리스트 최댓값/최솟값 실습을 위해 정상범위(295~305) 이탈 온도 2~3건 삽입
    idx = rng.choice(n, size=3, replace=False)
    temp[idx] = rng.uniform(312, 320, size=3)

    df = pd.DataFrame({
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 200, size=n)],
        "공정명": rng.choice(PROCESS, size=n),
        "설비번호": rng.choice(EQUIPMENT, size=n),
        "온도_섭씨": np.round(temp, 1),
    })
    df["합격여부"] = rng.choice([1, -1], size=n, p=[0.84, 0.16])
    df = df.rename(columns=RENAMED_COLUMNS["week02_python_basics_1"])  # 값·난수 흐름은 그대로
    save_csv(df, "week02", "week02_python_basics_1.csv")
    return df


# ---------------------------------------------------------------------------
# Week 03 (신규) — 파이썬 기초 Ⅱ: 조건문·반복문·함수
# ---------------------------------------------------------------------------
def gen_week03():
    rng = np.random.default_rng(103)
    n = 30
    temp = rng.normal(300, 4, size=n)
    # for + if 실습량 확보를 위해 2주차보다 조금 더 많은 이탈 온도(4~5건) 삽입
    idx = rng.choice(n, size=5, replace=False)
    temp[idx] = rng.uniform(311, 322, size=5)

    df = pd.DataFrame({
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 200, size=n)],
        "공정명": rng.choice(PROCESS, size=n),
        "설비번호": rng.choice(EQUIPMENT, size=n),
        "온도_섭씨": np.round(temp, 1),
    })
    df["합격여부"] = rng.choice([1, -1], size=n, p=[0.82, 0.18])
    df = df.rename(columns=RENAMED_COLUMNS["week03_python_basics_2"])  # 값·난수 흐름은 그대로
    save_csv(df, "week03", "week03_python_basics_2.csv")
    return df


# ---------------------------------------------------------------------------
# Week 04 — Pandas로 읽고 선택하기 (= v1 week03)
# ---------------------------------------------------------------------------
def gen_week04():
    rng = np.random.default_rng(104)
    n = 100
    ts = timestamps(rng, n, periods_hours=800)
    equip = rng.choice(EQUIPMENT, size=n, p=[0.28, 0.28, 0.24, 0.20])
    temp = rng.normal(300, 4, size=n)
    pressure = rng.normal(1012, 8, size=n)
    gas = rng.normal(50, 2, size=n)

    fail_prob = np.where(equip == "EQ-02", 0.28, 0.09)
    passfail = np.array([rng.choice([1, -1], p=[1 - p, p]) for p in fail_prob])

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 400, size=n)],
        "설비번호": equip,
        "공정명": rng.choice(PROCESS, size=n),
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "가스유량_slm": np.round(gas, 2),
        "합격여부": passfail,
    })
    df = df.rename(columns=RENAMED_COLUMNS["week04_process_filtering"])  # 값·난수 흐름은 그대로
    save_csv(df, "week04", "week04_process_filtering.csv")
    return df


# ---------------------------------------------------------------------------
# Week 05 (의도적으로 지저분한 데이터) — 결측값 정리 + Orange3 (= v1 week04)
# ---------------------------------------------------------------------------
def gen_week05():
    rng = np.random.default_rng(105)
    n = 110
    ts = timestamps(rng, n, periods_hours=900)
    equip = rng.choice(EQUIPMENT, size=n)
    process = rng.choice(PROCESS, size=n)
    temp = rng.normal(300, 4, size=n)
    pressure = rng.normal(1012, 8, size=n)
    gas = rng.normal(50, 2, size=n)
    proc_time = rng.normal(120, 5, size=n)
    passfail = rng.choice([1, -1], size=n, p=[0.87, 0.13])

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 400, size=n)],
        "설비번호": equip,
        "공정명": process,
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "가스유량_slm": np.round(gas, 2),
        "처리시간_sec": np.round(proc_time, 1),
        "합격여부": passfail,
    })

    # --- 의도적 오염 주입 ---
    na_targets = rng.choice(n, size=8, replace=False)
    for i, col in zip(na_targets, rng.choice(["온도_섭씨", "압력_Pa", "가스유량_slm"], size=8)):
        df.loc[i, col] = np.nan

    dup_rows = df.sample(3, random_state=104)
    df = pd.concat([df, dup_rows], ignore_index=True)

    weird_date_idx = df.sample(2, random_state=204).index
    date_formats = ["2024/03/05", "03-05-2024 10:00"]
    for i, d in zip(weird_date_idx, date_formats):
        df.loc[i, "측정시간"] = d

    hot_idx = df.sample(2, random_state=304).index
    df.loc[hot_idx, "온도_섭씨"] = rng.uniform(500, 560, size=2)

    negp_idx = df.sample(2, random_state=404).index
    df.loc[negp_idx, "압력_Pa"] = -rng.uniform(10, 50, size=2)

    badgas_idx = df.sample(2, random_state=504).index
    df.loc[badgas_idx, "가스유량_slm"] = rng.choice([-5, 250], size=2)

    typo_idx = df.sample(3, random_state=604).index
    typos = ["중착", "식각 ", "포토공정"]
    for i, t in zip(typo_idx, typos):
        df.loc[i, "공정명"] = t

    miss_label_idx = df.sample(2, random_state=704).index
    df.loc[miss_label_idx, "합격여부"] = np.nan

    df = df.reset_index(drop=True)
    df = df.rename(columns=RENAMED_COLUMNS["week05_dirty_process_data"])  # 값·난수 흐름은 그대로
    save_csv(df, "week05", "week05_dirty_process_data.csv")
    return df


# ---------------------------------------------------------------------------
# Week 06 — 그래프 + Orange3 시각화 (= v1 week05)
# ---------------------------------------------------------------------------
def gen_week06():
    rng = np.random.default_rng(106)
    n = 180
    ts = sorted(pd.Timestamp("2024-03-01") + pd.to_timedelta(rng.choice(range(0, 1400), size=n, replace=False), unit="h"))
    equip = rng.choice(EQUIPMENT, size=n)

    # 시간 흐름에 따른 완만한 온도 드리프트(전체 300 -> 306)
    drift = np.linspace(0, 6, n)
    temp = rng.normal(300, 2.5, size=n) + drift
    # EQ-02는 분산 확대(박스플롯 실습용)
    temp = np.where(equip == "EQ-02", temp + rng.normal(0, 5, size=n), temp)

    pressure = rng.normal(1012, 8, size=n)
    thickness = 100 + (temp - 300) * 0.6 + rng.normal(0, 1.5, size=n)
    vibration = np.where(equip == "EQ-02", rng.normal(0.62, 0.08, size=n), rng.normal(0.5, 0.04, size=n))
    proc_time = rng.normal(120, 5, size=n)

    fail_prob = np.where(equip == "EQ-02", 0.22, 0.08)
    passfail = np.array([rng.choice([1, -1], p=[1 - p, p]) for p in fail_prob])

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 600, size=n)],
        "설비번호": equip,
        "공정명": rng.choice(PROCESS, size=n),
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "두께_nm": np.round(thickness, 2),
        "진동_mm_s": np.round(vibration, 3),
        "처리시간_sec": np.round(proc_time, 1),
        "합격여부": passfail,
    })
    df = df.rename(columns=RENAMED_COLUMNS["week06_process_visualization"])  # 값·난수 흐름은 그대로
    save_csv(df, "week06", "week06_process_visualization.csv")
    return df


# ---------------------------------------------------------------------------
# Week 07 (신규 병합) — 설비 비교 + 수율·불량 분석 (= v1 week06 + week07 압축)
# ---------------------------------------------------------------------------
def gen_week07():
    rng = np.random.default_rng(107)
    n_lots = 75
    wafers_per_lot = 4
    lots = [f"LOT-{i:04d}" for i in range(1, n_lots + 1)]
    low_yield_lots = set(rng.choice(lots, size=5, replace=False))
    eq04_defects = ["두께 불량", "파티클", "패턴 불량"]

    equip_profile = {
        "EQ-01": dict(temp_mean=300, temp_std=2.5, pressure_mean=1010, pressure_std=7, fail_prob=0.05),
        "EQ-02": dict(temp_mean=300, temp_std=7.5, pressure_mean=1010, pressure_std=7, fail_prob=0.10),
        "EQ-03": dict(temp_mean=300, temp_std=3.0, pressure_mean=1028, pressure_std=7, fail_prob=0.08),
        "EQ-04": dict(temp_mean=301, temp_std=4.0, pressure_mean=1012, pressure_std=9, fail_prob=0.20),
    }

    rows = []
    for lot in lots:
        equip = "EQ-04" if lot in low_yield_lots else rng.choice(EQUIPMENT, p=[0.28, 0.26, 0.24, 0.22])
        process = rng.choice(PROCESS)
        shift = rng.choice(SHIFT)
        prof = equip_profile[equip]

        for w in range(1, wafers_per_lot + 1):
            temp = rng.normal(prof["temp_mean"], prof["temp_std"])
            pressure = rng.normal(prof["pressure_mean"], prof["pressure_std"])
            vacuum = rng.normal(5.0, 0.3)
            proc_time = rng.normal(120, 5)

            if lot in low_yield_lots:
                # 로트 수율 80% 미만을 보장하기 위해 4장 중 최소 2장은 강제 불합격
                fail = True if w <= 2 else (rng.random() < 0.3)
            else:
                fail = rng.random() < prof["fail_prob"]

            if fail:
                passfail = -1
                defect = rng.choice(eq04_defects) if (equip == "EQ-04" and rng.random() < 0.6) else rng.choice(DEFECT_TYPES)
            else:
                passfail = 1
                defect = ""

            rows.append({
                "로트번호": lot,
                "웨이퍼번호": w,
                "설비번호": equip,
                "공정명": process,
                "작업조": shift,
                "온도_섭씨": round(temp, 1),
                "압력_Pa": round(pressure, 1),
                "진공도_mTorr": round(vacuum, 2),
                "처리시간_sec": round(proc_time, 1),
                "불량유형": defect,
                "합격여부": passfail,
            })
    df = pd.DataFrame(rows)
    df = df.rename(columns=RENAMED_COLUMNS["week07_equipment_yield"])  # 값·난수 흐름은 그대로
    save_csv(df, "week07", "week07_equipment_yield.csv")
    return df


# ---------------------------------------------------------------------------
# Week 08
# ---------------------------------------------------------------------------
def gen_week08():
    rng = np.random.default_rng(108)
    n = 450
    ts = sorted(pd.Timestamp("2024-03-01") + pd.to_timedelta(rng.choice(range(0, 2200), size=n, replace=False), unit="h"))
    equip = rng.choice(EQUIPMENT, size=n)

    temp = rng.normal(300, 4, size=n)
    # 패턴1: 온도가 높을수록 두께 증가(약한 양의 상관 + 노이즈)
    thickness = 100 + (temp - 300) * 0.5 + rng.normal(0, 2.0, size=n)

    vacuum = rng.normal(5.0, 0.35, size=n)
    # 패턴2: 진공도가 정상범위(4.5~5.5)를 벗어나면 불합격 확률 상승
    vacuum_out = (vacuum < 4.5) | (vacuum > 5.5)

    # 패턴3: EQ-02는 진동이 전반적으로 높음
    vibration = np.where(equip == "EQ-02", rng.normal(0.68, 0.06, size=n), rng.normal(0.5, 0.04, size=n))

    # 패턴4: 냉각수온도 상승 후 공정온도가 뒤따라 상승(순서 있는 8~12행 구간 3곳)
    cooling = rng.normal(20, 1.0, size=n)
    for _ in range(3):
        start = rng.integers(0, n - 15)
        length = rng.integers(8, 13)
        bump = np.linspace(0, rng.uniform(3, 5), length)
        cooling[start:start + length] += bump
        temp[start:start + length] += bump * 0.6

    pressure = rng.normal(1012, 8, size=n)
    humidity = rng.normal(45, 3, size=n)  # 패턴5: 불량과 무관한 대조군 변수

    fail_prob = np.where(vacuum_out, 0.35, 0.08)
    passfail = np.array([rng.choice([1, -1], p=[1 - p, p]) for p in fail_prob])

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 900, size=n)],
        "설비번호": equip,
        "공정명": rng.choice(PROCESS, size=n),
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "진공도_mTorr": np.round(vacuum, 2),
        "두께_nm": np.round(thickness, 2),
        "진동_mm_s": np.round(vibration, 3),
        "냉각수온도_섭씨": np.round(cooling, 2),
        "습도_pct": np.round(humidity, 1),
        "합격여부": passfail,
    })
    df = df.rename(columns=RENAMED_COLUMNS["week08_anomaly_root_cause"])  # 값·난수 흐름은 그대로
    save_csv(df, "week08", "week08_anomaly_root_cause.csv")
    return df


# ---------------------------------------------------------------------------
# Week 09 (전면 교체) — 머신러닝 예측 + Orange3 (반도체_공정_샘플.csv 계열, fab.csv 미사용)
# ---------------------------------------------------------------------------
def _week09_features(rng, n):
    equip = rng.choice(EQUIPMENT, size=n)
    process = rng.choice(PROCESS, size=n)
    temp = rng.normal(300, 5, size=n)
    pressure = rng.normal(1012, 10, size=n)
    vacuum = rng.normal(5.0, 0.4, size=n)
    gas = rng.normal(50, 3, size=n)          # 합격여부와 무관한 변수(대조군)
    humidity = rng.normal(45, 4, size=n)     # 합격여부와 무관한 변수(대조군)
    thickness = 100 + (temp - 300) * 0.55 + rng.normal(0, 2.0, size=n)
    return equip, process, temp, pressure, vacuum, gas, humidity, thickness


def gen_week09():
    rng = np.random.default_rng(109)
    n = 750
    equip, process, temp, pressure, vacuum, gas, humidity, thickness = _week09_features(rng, n)

    # 온도/압력/진공도/두께가 정상범위를 벗어날수록 불합격 확률 상승(8주차 패턴과 동일한 감각)
    risk = (
        (np.abs(temp - 300) > 6).astype(float) * 0.20
        + (np.abs(pressure - 1012) > 18).astype(float) * 0.15
        + ((vacuum < 4.5) | (vacuum > 5.5)).astype(float) * 0.25
        + (np.abs(thickness - 100) > 5).astype(float) * 0.15
    )
    fail_prob = np.clip(0.06 + risk, 0.03, 0.85)
    result = np.array([rng.choice([0, 1], p=[1 - p, p]) for p in fail_prob])  # 난수 순서 유지용 0/1 추첨
    # 2026-10-02: 1~8차시와 같은 규약으로 저장(1=합격, -1=불합격). 추첨 순서는 그대로라 다른 열 값은 바뀌지 않는다.
    passfail = np.where(result == 1, -1, 1)

    df = pd.DataFrame({
        "공정명": process,
        "설비번호": equip,
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "가스유량_slm": np.round(gas, 2),
        "두께_nm": np.round(thickness, 2),
        "진공도_mTorr": np.round(vacuum, 2),
        "습도_pct": np.round(humidity, 1),
        "합격여부": passfail,
    })

    # 결측치 소량 삽입(4~5주차 정제 복습용)
    na_targets = rng.choice(n, size=15, replace=False)
    na_cols = rng.choice(["온도_섭씨", "압력_Pa", "가스유량_slm", "습도_pct"], size=15)
    for i, col in zip(na_targets, na_cols):
        df.loc[i, col] = np.nan

    save_csv(df.rename(columns=RENAMED_COLUMNS["week09_pass_fail_train"]), "week09", "week09_pass_fail_train.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)

    # 예측 실습용 새 로트(정답 라벨 없음)
    n_new = 9
    equip_n, process_n, temp_n, pressure_n, vacuum_n, gas_n, humidity_n, thickness_n = _week09_features(rng, n_new)
    new_df = pd.DataFrame({
        "공정명": process_n,
        "설비번호": equip_n,
        "온도_섭씨": np.round(temp_n, 1),
        "압력_Pa": np.round(pressure_n, 1),
        "가스유량_slm": np.round(gas_n, 2),
        "두께_nm": np.round(thickness_n, 2),
        "진공도_mTorr": np.round(vacuum_n, 2),
        "습도_pct": np.round(humidity_n, 1),
    })
    save_csv(new_df.rename(columns=RENAMED_COLUMNS["week09_new_lots_to_predict"]), "week09", "week09_new_lots_to_predict.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)
    return df, new_df


# ---------------------------------------------------------------------------
# Week 10
# ---------------------------------------------------------------------------
def gen_week10():
    rng = np.random.default_rng(110)
    n = 600
    ts = sorted(pd.Timestamp("2024-03-01") + pd.to_timedelta(rng.choice(range(0, 3000), size=n, replace=False), unit="h"))
    equip = rng.choice(EQUIPMENT, size=n)
    shift = rng.choice(SHIFT, size=n)

    temp = np.empty(n)
    pressure = np.empty(n)
    fail_prob = np.empty(n)
    for i, e in enumerate(equip):
        if e == "EQ-01":
            temp[i] = rng.normal(300, 3)
            pressure[i] = rng.normal(1010, 8)
            fail_prob[i] = 0.06
        elif e == "EQ-02":
            temp[i] = rng.normal(300, 6.5)
            pressure[i] = rng.normal(1010, 8)
            fail_prob[i] = 0.11
        elif e == "EQ-03":
            temp[i] = rng.normal(300, 3.5)
            pressure[i] = rng.normal(1025, 8)
            fail_prob[i] = 0.09
        else:
            temp[i] = rng.normal(301, 4.5)
            pressure[i] = rng.normal(1013, 9)
            fail_prob[i] = 0.16

    vacuum = rng.normal(5.0, 0.35, size=n)
    thickness = 100 + (temp - 300) * 0.45 + rng.normal(0, 2.2, size=n)
    vibration = np.where(equip == "EQ-02", rng.normal(0.63, 0.07, size=n), rng.normal(0.5, 0.05, size=n))
    proc_time = rng.normal(120, 6, size=n)
    cooling = rng.normal(20, 1.2, size=n)
    humidity = rng.normal(45, 3.5, size=n)

    result = np.array([rng.choice([0, 1], p=[1 - p, p]) for p in fail_prob])  # 난수 순서 유지용 0/1 추첨
    defect = np.where(result == 1, rng.choice(DEFECT_TYPES, size=n), "")
    passfail = np.where(result == 1, -1, 1)  # 1~8차시와 같은 규약(1=합격, -1=불합격)

    df = pd.DataFrame({
        "측정시간": [t.strftime("%Y-%m-%d %H:%M") for t in ts],
        "로트번호": [f"LOT-{i:04d}" for i in rng.integers(1, 900, size=n)],
        "웨이퍼번호": rng.integers(1, 26, size=n),
        "설비번호": equip,
        "공정명": rng.choice(PROCESS, size=n),
        "작업조": shift,
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "진공도_mTorr": np.round(vacuum, 2),
        "두께_nm": np.round(thickness, 2),
        "진동_mm_s": np.round(vibration, 3),
        "처리시간_sec": np.round(proc_time, 1),
        "냉각수온도_섭씨": np.round(cooling, 2),
        "습도_pct": np.round(humidity, 1),
        "불량유형": defect,
        "합격여부": passfail,
    })
    save_csv(df.rename(columns=RENAMED_COLUMNS["week10_mini_project_dataset"]), "week10", "week10_mini_project_dataset.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)
    return df


# ===========================================================================
# 생활 예제(easy) 데이터 — 4~10차시 (2026-10-08 추가)
# ---------------------------------------------------------------------------
# 초보자가 먼저 생활 소재(카페·학급·아이스크림·날씨)로 같은 Pandas/scikit-learn 연산을 익힌 뒤
# 같은 모양의 코드를 반도체 데이터에 적용하도록 만든 작은 CSV다.
# - 위의 반도체 데이터 생성기(gen_week01~10)와 난수 흐름을 공유하지 않는다. 각 함수는 자기 시드로
#   새 Generator를 만들거나(6·8·9차시), 손으로 고정한 값을 쓴다(4·5·7·10차시 예보). 그래서 이 절을
#   추가·수정해도 기존 반도체 CSV는 한 바이트도 바뀌지 않는다.
# - 4~8차시 결과값(1/-1) 열은 반도체 `합격여부`와 같은 규약(1 = 좋은 쪽, -1 = 나쁜 쪽)을 따른다.
# ===========================================================================
def gen_easy_week04():
    """카페 주문 12건 — read_csv·열 선택·조건 검색·정렬·loc·그룹 비율 연습용(손으로 고정한 값)."""
    rows = [
        # 주문번호, 매장, 메뉴, 종류, 가격_원, 수량_개, 평가(1=좋아요, -1=별로예요) — 저장 직전 가격_KRW, 수량_count로 바꾼다
        ("C-001", "강남점", "아메리카노", "커피", 4500, 2, 1),
        ("C-002", "홍대점", "카페라테", "커피", 5000, 1, 1),
        ("C-003", "강남점", "녹차", "차", 4800, 1, -1),
        ("C-004", "강남점", "치즈케이크", "디저트", 6500, 1, -1),
        ("C-005", "홍대점", "아메리카노", "커피", 4500, 3, 1),
        ("C-006", "홍대점", "바닐라라테", "커피", 5500, 1, -1),
        ("C-007", "강남점", "캐모마일", "차", 4800, 2, 1),
        ("C-008", "홍대점", "마카롱", "디저트", 2500, 4, 1),
        ("C-009", "강남점", "카페모카", "커피", 5500, 1, 1),
        ("C-010", "홍대점", "초코케이크", "디저트", 6800, 1, -1),
        ("C-011", "강남점", "유자차", "차", 5200, 1, 1),
        ("C-012", "홍대점", "쿠키", "디저트", 2000, 2, 1),
    ]
    df = pd.DataFrame(rows, columns=["주문번호", "매장", "메뉴", "종류", "가격_원", "수량_개", "평가"])
    df = df.rename(columns=RENAMED_COLUMNS["week04_easy_cafe_orders"])
    save_csv(df, "week04", "week04_easy_cafe_orders.csv")
    return df


def gen_easy_week05():
    """학급 학생 기록 15행 — 결측 3칸·완전 중복 1행·입력 실수 이상값 1개를 일부러 심었다(손으로 고정한 값)."""
    nan = np.nan
    rows = [
        # 이름, 반, 키_cm, 몸무게_kg, 수학_점수
        ("김민준", "1반", 165.2, 55.1, 85),
        ("이서연", "1반", 158.4, 48.3, 92),
        ("박지호", "1반", 171.0, 63.5, 78),
        ("최수아", "1반", nan, 50.2, 88),        # 결측: 키를 적지 않음
        ("정도윤", "2반", 1720.0, 66.0, 74),     # 이상값: 172.0을 소수점 없이 1720으로 잘못 입력
        ("강하린", "2반", 160.5, 51.8, 95),
        ("조예준", nan, 168.3, 59.4, 81),        # 결측: 반을 적지 않음(추측할 수 없어 지울 대상)
        ("윤지우", "2반", 155.9, 46.7, 69),
        ("장서준", "2반", 174.6, nan, 90),       # 결측: 몸무게를 적지 않음
        ("임하은", "3반", 162.1, 52.9, 83),
        ("한시우", "3반", 169.8, 61.2, 76),
        ("오유나", "3반", 157.3, 47.5, 98),
        ("서주원", "3반", 176.2, 70.3, 72),
        ("신채원", "3반", 161.7, 53.6, 87),
        ("박지호", "1반", 171.0, 63.5, 78),      # 완전 중복: 3번째 행을 한 번 더 입력
    ]
    df = pd.DataFrame(rows, columns=["이름", "반", "키_cm", "몸무게_kg", "수학_점수"])
    df = df.rename(columns=RENAMED_COLUMNS["week05_easy_class_records"])
    save_csv(df, "week05", "week05_easy_class_records.csv")
    return df


def gen_easy_week06():
    """아이스크림 가게 3주(21일) 일별 기록 — to_datetime·선·막대·히스토그램·산점도·박스플롯 연습용."""
    rng = np.random.default_rng(1006)
    n = 21
    dates = pd.date_range("2024-06-03", periods=n, freq="D")
    day_names = ["월", "화", "수", "목", "금", "토", "일"]
    weather = rng.choice(["맑음", "흐림", "비"], size=n, p=[0.55, 0.28, 0.17])
    # 3주 동안 기온이 서서히 오른다(선 그래프의 오름 추세). 비 오는 날은 3도 낮다.
    temp = np.linspace(24, 31, n) + rng.normal(0, 1.5, size=n)
    temp = np.where(weather == "비", temp - 3, temp)
    # 기온이 높을수록 많이 팔리고(산점도 오른쪽 위), 비 오는 날은 덜 팔린다(박스플롯).
    sales = 40 + (temp - 20) * 9 + rng.normal(0, 8, size=n)
    sales = np.where(weather == "비", sales - 25, sales)
    df = pd.DataFrame({
        "날짜": dates.strftime("%Y-%m-%d"),
        "요일": [day_names[d.weekday()] for d in dates],
        "날씨": weather,
        "최고기온_섭씨": np.round(temp, 1),
        "판매량_개": np.round(sales).astype(int),
    })
    df = df.rename(columns=RENAMED_COLUMNS["week06_easy_icecream_daily"])
    save_csv(df, "week06", "week06_easy_icecream_daily.csv")
    return df


def gen_easy_week07():
    """반별 쪽지시험 문항 기록 24행 — groupby 개수·합·평균, 학생별 정답률, 오답유형 파레토 연습용.

    반도체 7차시와 같은 모양: 반 = 설비번호, 학생 = 로트(문항 4개 = 웨이퍼 4장),
    정답여부(1/-1) = 합격여부, 오답유형(정답이면 빈 값) = 불량유형, 풀이시간_초(저장 시 풀이시간_sec) = 온도_섭씨(저장 시 온도_C).
    """
    rows = [
        # 반, 이름, 문제번호, 풀이시간_초, 오답유형, 정답여부(1=정답, -1=오답)
        ("A반", "지민", 1, 45, "", 1),
        ("A반", "지민", 2, 60, "", 1),
        ("A반", "지민", 3, 52, "", 1),
        ("A반", "지민", 4, 70, "", 1),
        ("A반", "하은", 1, 50, "", 1),
        ("A반", "하은", 2, 65, "", 1),
        ("A반", "하은", 3, 90, "계산 실수", -1),
        ("A반", "하은", 4, 58, "", 1),
        ("B반", "서준", 1, 40, "", 1),
        ("B반", "서준", 2, 55, "", 1),
        ("B반", "서준", 3, 48, "", 1),
        ("B반", "서준", 4, 62, "", 1),
        ("B반", "예린", 1, 85, "문제 잘못 읽음", -1),
        ("B반", "예린", 2, 110, "계산 실수", -1),
        ("B반", "예린", 3, 95, "", 1),
        ("B반", "예린", 4, 120, "개념 부족", -1),
        ("C반", "도윤", 1, 55, "", 1),
        ("C반", "도윤", 2, 80, "계산 실수", -1),
        ("C반", "도윤", 3, 60, "", 1),
        ("C반", "도윤", 4, 75, "", 1),
        ("C반", "시우", 1, 48, "", 1),
        ("C반", "시우", 2, 70, "", 1),
        ("C반", "시우", 3, 66, "", 1),
        ("C반", "시우", 4, 88, "문제 잘못 읽음", -1),
    ]
    df = pd.DataFrame(rows, columns=["반", "이름", "문제번호", "풀이시간_초", "오답유형", "정답여부"])
    df = df.rename(columns=RENAMED_COLUMNS["week07_easy_quiz_results"])
    save_csv(df, "week07", "week07_easy_quiz_results.csv")
    return df


def gen_easy_week08():
    """아이스크림 가게 30일 날씨·판매 기록 — 산점도·상관계수·정상 범위 밖 비교 연습용.

    심은 관계: 기온↔아이스크림(강한 +), 기온↔핫초코(강한 -), 습도(관계없는 비교용 열),
    냉동고온도는 정상 범위(-20~-16℃)를 양쪽으로 벗어난 날에 손님 불만이 몰리는 U자 관계
    (상관계수로는 거의 0으로 나와 놓치는 경우). 반도체 8차시의 진공도-합격여부와 같은 모양이다.
    """
    rng = np.random.default_rng(1008)
    n = 30
    dates = pd.date_range("2024-03-01", periods=n, freq="3D")
    temp = np.linspace(8, 30, n) + rng.normal(0, 2.5, size=n)
    ice = 20 + (temp - 5) * 6 + rng.normal(0, 12, size=n)
    choco = 90 - (temp - 5) * 2.8 + rng.normal(0, 9, size=n)

    # 냉동고: 평소에는 정상 범위 안, 8일은 너무 차갑거나(4일) 너무 따뜻하다(4일).
    # 범위 밖 날짜는 30일에 고르게 흩어 두어(손으로 고정한 행 번호) 기온과 우연히 겹치지 않게 한다.
    freezer = rng.uniform(-19.5, -16.5, size=n)
    too_cold, too_warm = [3, 10, 18, 24], [6, 13, 21, 28]
    freezer[too_cold] = rng.uniform(-23.5, -21, size=4)
    freezer[too_warm] = rng.uniform(-15, -12.5, size=4)
    # 손님평가(1 = 좋음, -1 = 불만): 30행뿐이라 확률로 뽑으면 차이가 흐려질 수 있어 건수를 고정한다.
    # 너무 차가운 날 4일 중 3일, 너무 따뜻한 날 4일 중 3일, 정상 범위 22일 중 2일이 불만.
    review = np.ones(n, dtype=int)
    review[[3, 10, 24]] = -1      # 너무 차가운 날(딱딱해서 안 퍼짐)
    review[[6, 13, 28]] = -1      # 너무 따뜻한 날(녹아서 흐물흐물)
    review[[17, 26]] = -1         # 정상 범위 안이지만 불만(다른 이유)

    # 습도: 관계없는 비교용 열. 무작위 값에서 기온·핫초코·냉동고·평가와 겹치는 부분을 빼서(최소제곱 잔차)
    # 30행뿐인 작은 표에서도 우연히 상관이 생기지 않게 한다. 아이스크림은 일부러 빼서 습도-아이스크림
    # 상관계수가 정확히 0(반올림하면 "-0.0"으로 보임)이 아니라 0.02 같은 자연스러운 작은 값이 되게 했다.
    noise = rng.normal(0, 1, size=n)
    basis = np.column_stack([np.ones(n), temp, choco, freezer, review])
    coef, *_ = np.linalg.lstsq(basis, noise, rcond=None)
    resid = noise - basis @ coef
    humid = 60 + resid / resid.std() * 10

    df = pd.DataFrame({
        "날짜": dates.strftime("%Y-%m-%d"),
        "최고기온_섭씨": np.round(temp, 1),
        "습도_pct": np.round(humid).astype(int),
        "아이스크림_판매량_개": np.round(ice).astype(int),
        "핫초코_판매량_잔": np.round(choco).astype(int),
        "냉동고온도_섭씨": np.round(freezer, 1),
        "손님평가": review,
    })
    df = df.rename(columns=RENAMED_COLUMNS["week08_easy_weather_sales"])  # 값·난수 흐름은 그대로
    save_csv(df, "week08", "week08_easy_weather_sales.csv")
    return df


EASY_OUTDOOR_FEATURES = ["최고기온_섭씨", "습도_pct", "풍속_m_s", "강수량_mm"]


def _easy_outdoor_class_df():
    """야외 체육 수업 진행 여부 120일 — 9·10차시 공용 학습 데이터.

    시드 1142는 다음 조건을 모두 만족하도록 고른 값이다(시드 1009~1199 비교):
    진행 비율 70~80%, max_depth=4 결정트리(random_state=42) 정확도가 "무조건 진행" 기준선보다
    8%p 이상 높음, 관계없는 비교용 열(습도) 중요도 0%, max_depth=8의 test 정확도가 4보다 높지 않음,
    "약한 비" 날의 취소 확률(predict_proba)이 0.3~0.7 사이로 나와 10차시 "애매한 날" 설명이 가능함.
    """
    rng = np.random.default_rng(1142)
    n = 120
    dates = pd.date_range("2024-04-01", periods=n, freq="D")
    temp = np.linspace(15, 31, n) + rng.normal(0, 3.0, size=n)
    humid = rng.normal(62, 12, size=n).clip(25, 95)       # 진행여부와 무관한 비교용 열
    wind = rng.gamma(2.2, 1.9, size=n).clip(0.3, 15)
    rain = np.where(rng.random(n) < 0.3, rng.gamma(1.5, 6, size=n), 0.0)

    # 비(5mm 이상)·강풍(9m/s 이상)·폭염(32도 이상)이면 대부분 취소, 약한 비는 반반, 그 외는 드물게 취소
    p = np.full(n, 0.03)
    p = np.where(rain >= 5, 0.92, p)
    p = np.where((rain > 0) & (rain < 5), 0.5, p)
    p = np.where(wind >= 9, np.maximum(p, 0.85), p)
    p = np.where(temp >= 32, np.maximum(p, 0.8), p)
    label = np.where(rng.random(n) < p, -1, 1)              # 1 = 진행, -1 = 취소

    df = pd.DataFrame({
        "날짜": dates.strftime("%Y-%m-%d"),
        "최고기온_섭씨": np.round(temp, 1),
        "습도_pct": np.round(humid).astype(float),
        "풍속_m_s": np.round(wind, 1),
        "강수량_mm": np.round(rain, 1),
        "진행여부": label,
    })
    # 결측 4칸(5차시 정리 복습용): 기록을 빠뜨린 날
    na_idx = rng.choice(n, size=4, replace=False)
    for i, col in zip(na_idx, ["최고기온_섭씨", "습도_pct", "풍속_m_s", "습도_pct"]):
        df.loc[i, col] = np.nan
    return df


def gen_easy_week09():
    df = _easy_outdoor_class_df()
    save_csv(df.rename(columns=RENAMED_COLUMNS["week09_easy_outdoor_class"]), "week09", "week09_easy_outdoor_class.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)
    return df


def gen_easy_week10():
    """10차시: 9차시와 같은 학습 데이터(10차시 폴더에 따로 저장) + 정답 없는 예보 7일(손으로 고정한 값)."""
    train = _easy_outdoor_class_df()
    save_csv(train.rename(columns=RENAMED_COLUMNS["week10_easy_outdoor_class_train"]), "week10", "week10_easy_outdoor_class_train.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)

    rows = [
        # 날짜, 최고기온_섭씨, 습도_pct, 풍속_m_s, 강수량_mm
        ("2024-07-30", 26.0, 60.0, 3.0, 0.0),    # 맑고 선선함
        ("2024-07-31", 24.5, 85.0, 4.2, 15.0),   # 비가 많이 옴
        ("2024-08-01", 33.5, 55.0, 2.0, 0.0),    # 폭염
        ("2024-08-02", 22.0, 70.0, 10.5, 0.0),   # 강풍
        ("2024-08-03", 27.5, 75.0, 5.0, 3.0),    # 약한 비(애매한 날)
        ("2024-08-04", 30.5, 65.0, 8.5, 0.0),    # 덥고 바람이 꽤 붊(애매한 날)
        ("2024-08-05", 25.0, 50.0, 2.5, 0.0),    # 맑음
    ]
    new_days = pd.DataFrame(rows, columns=["날짜"] + EASY_OUTDOOR_FEATURES)
    save_csv(new_days.rename(columns=RENAMED_COLUMNS["week10_easy_outdoor_class_new_days"]), "week10", "week10_easy_outdoor_class_new_days.csv")  # 열 이름만 바꾼다(값·난수 흐름 그대로)
    return train, new_days


def gen_easy_all():
    gen_easy_week04()
    gen_easy_week05()
    gen_easy_week06()
    gen_easy_week07()
    gen_easy_week08()
    gen_easy_week09()
    gen_easy_week10()


# ===========================================================================
# Orange3 워밍업 데이터 — weekXX_orange_<주제>.csv (2026-10-23 추가)
# ---------------------------------------------------------------------------
# Orange 워밍업은 Orange 내장 데이터(zoo·iris·titanic 등)를 쓰지 않고 여기서 만든 합성 데이터만 쓴다
# (2026-10-23 결정: 1~3차시 생활 소재, 4~10차시 공정 관련 소재).
# - 새 데이터의 열 이름은 "한글 이름_영문/SI 단위"로 짓는다: 기온_C, 강수량_mm, 승차인원_count, PM10_ug_m3, 두께_nm.
# - 생성 함수는 자기 시드로 새 Generator를 만들거나 손으로 고정한 값을 쓴다(기존 CSV 불변).
# - 저장은 save_orange_warmup()으로 한다. 파일명 규칙(weekXX_orange_<주제>.csv)을 강제하고,
#   아래 write_orange_tabs()가 다른 CSV와 똑같이 orange/ 아래 .tab 파생본을 만든다.
# - 새 함수를 만들면 ORANGE_WARMUP_GENERATORS에 추가한다.
# ===========================================================================
# ---------------------------------------------------------------------------
# 웨이퍼 다이 합성기 — 6·7·9·10차시 웨이퍼 데이터와 generate_figures.py가 함께 쓰는 공통 부품
# ---------------------------------------------------------------------------
# 격자: 다이_X, 다이_Y ∈ [-10, 10], X² + Y² ≤ 100 → 웨이퍼 한 장 = 다이 317개.
# 다이 간격 14mm 가정: 중심거리_mm = round(√(X²+Y²) × 14, 1), 최대 140mm(300mm 웨이퍼 반지름 150mm 안쪽).
DIE_PITCH_MM = 14
EDGE_MM = 112     # 이보다 멀면 가장자리(격자 반지름 8 초과, 120다이)
CENTER_MM = 42    # 이 이하면 중심(격자 반지름 3 이하, 29다이)


def die_grid():
    """다이 격자(위쪽 줄부터, 왼쪽에서 오른쪽). (x, y, 중심거리_mm) 배열을 돌려준다."""
    ys, xs = np.meshgrid(np.arange(10, -11, -1), np.arange(-10, 11), indexing="ij")
    x, y = xs.ravel(), ys.ravel()
    keep = x ** 2 + y ** 2 <= 100
    x, y = x[keep], y[keep]
    dist = np.round(np.sqrt(x ** 2 + y ** 2) * DIE_PITCH_MM, 1)
    return x, y, dist


def wafer_fail_mask(rng, pattern, **p):
    """패턴별 불합격 다이(True) 배열. 같은 rng 상태면 같은 맵이 나온다.

    pattern
      "random"  : 다이마다 p_base 확률로 불합격(무작위 불량)
      "count"   : 무작위 다이 n개만 불합격(n 고정)
      "edge"    : 가장자리(> EDGE_MM) p_edge, 안쪽 p_base
      "center"  : 중심(≤ CENTER_MM) p_center, 그 바깥 고리(≤ 70mm) p_ring, 나머지 p_base
      "scratch" : 웨이퍼를 가로지르는 직선 근처(수직 거리 ≤ 0.6칸)의 길이 length칸 구간 p_line, 나머지 p_base
      "mix"     : 중심 n_center개 + 가장자리 n_edge개를 무작위로 고른다(애매한 웨이퍼)
    """
    x, y, dist = die_grid()
    n = len(x)
    base = p.get("p_base", 0.0)
    if pattern == "random":
        return rng.random(n) < base
    if pattern == "count":
        fail = np.zeros(n, dtype=bool)
        fail[rng.choice(n, size=p["n"], replace=False)] = True
        return fail
    if pattern == "edge":
        prob = np.where(dist > EDGE_MM, p["p_edge"], base)
        return rng.random(n) < prob
    if pattern == "center":
        prob = np.where(dist <= CENTER_MM, p["p_center"], np.where(dist <= 70, p.get("p_ring", 0.0), base))
        return rng.random(n) < prob
    if pattern == "scratch":
        theta = rng.uniform(0, np.pi)
        offset = rng.uniform(-3.5, 3.5)
        start = rng.uniform(-6, 6 - p["length"] / 2)
        ux, uy = np.cos(theta), np.sin(theta)
        along = x * ux + y * uy
        perp = -x * uy + y * ux - offset
        on_line = (np.abs(perp) <= 0.6) & (along >= start) & (along <= start + p["length"])
        prob = np.where(on_line, p.get("p_line", 0.85), base)
        return rng.random(n) < prob
    if pattern == "mix":
        fail = np.zeros(n, dtype=bool)
        center_idx = np.flatnonzero(dist <= CENTER_MM)
        edge_idx = np.flatnonzero(dist > EDGE_MM)
        fail[rng.choice(center_idx, size=p["n_center"], replace=False)] = True
        fail[rng.choice(edge_idx, size=p["n_edge"], replace=False)] = True
        return fail
    raise ValueError(f"알 수 없는 패턴: {pattern}")


def wafer_frame(fail):
    """불합격 배열 → 다이 표(다이_X, 다이_Y, 중심거리_mm, 합격여부)."""
    x, y, dist = die_grid()
    return pd.DataFrame({"다이_X": x, "다이_Y": y, "중심거리_mm": dist, "합격여부": np.where(fail, -1, 1)})


def _line_ratio(fx, fy, tol=0.6):
    """불합격 다이 중 '가장 많은 다이를 지나는 한 직선' 위(수직 거리 ≤ tol칸)에 있는 비율(%)."""
    n = len(fx)
    if n <= 2:
        return 100.0 if n else 0.0
    pts = np.column_stack([fx, fy]).astype(float)
    best = 2
    for i in range(n - 1):
        d = pts[i + 1:] - pts[i]                       # i에서 다른 점으로 가는 방향들
        norm = np.hypot(d[:, 0], d[:, 1])
        rel = pts - pts[i]
        perp = np.abs(np.outer(d[:, 0], rel[:, 1]) - np.outer(d[:, 1], rel[:, 0])) / norm[:, None]
        best = max(best, int((perp <= tol).sum(axis=1).max()))
    return round(best / n * 100, 1)


def wafer_summary(fail):
    """다이 맵에서 9·10차시 웨이퍼 요약 특징을 계산한다."""
    x, y, dist = die_grid()
    n_fail = int(fail.sum())
    if n_fail == 0:
        return {"불량다이수_count": 0, "중심불량비율_pct": 0.0, "가장자리불량비율_pct": 0.0, "직선불량비율_pct": 0.0}
    fd = dist[fail]
    return {
        "불량다이수_count": n_fail,
        "중심불량비율_pct": round((fd <= CENTER_MM).mean() * 100, 1),
        "가장자리불량비율_pct": round((fd > EDGE_MM).mean() * 100, 1),
        "직선불량비율_pct": _line_ratio(x[fail], y[fail]),
    }


def save_orange_warmup(df: pd.DataFrame, week: str, topic: str):
    return save_csv(df, week, f"{week}_orange_{topic}.csv")


# --- A-1. 우리 동네 인구 (시드 201) ------------------------------------------
def gen_orange_week01():
    rng = np.random.default_rng(201)
    # 주요연령대 개수를 고정한다: 40~50대 12 · 20~30대 9 · 60대이상 6 · 10대이하 3.
    # 새빛구(새로 지은 아파트 동네)는 6동 중 5동이 20~30대. 나머지 4개 구는 구마다 20~30대 1동.
    ages_by_gu = {
        "햇살구": ["40~50대"] * 3 + ["20~30대", "60대이상", "10대이하"],
        "바람구": ["40~50대"] * 3 + ["20~30대", "60대이상", "60대이상"],
        "강변구": ["40~50대"] * 3 + ["20~30대", "60대이상", "10대이하"],
        "숲속구": ["40~50대"] * 2 + ["20~30대", "60대이상", "60대이상", "10대이하"],
        "새빛구": ["20~30대"] * 5 + ["40~50대"],
    }
    rows = []
    for gu, ages in ages_by_gu.items():
        for i, age in enumerate(rng.permutation(ages), start=1):
            rows.append({
                "구": gu,
                "동": f"{gu[:-1]}{i}동",
                "인구_count": int(rng.integers(8000, 45001)),
                "면적_km2": round(float(rng.uniform(0.8, 6.5)), 1),
                "주요연령대": str(age),
            })
    df = pd.DataFrame(rows)
    save_orange_warmup(df, "week01", "town_population")
    return df


# --- A-2. 지하철 역별 승하차 (시드 202) ----------------------------------------
def gen_orange_week02():
    rng = np.random.default_rng(202)
    stations = [("중앙역", "1호선"), ("시청역", "1호선"), ("대학로역", "1호선"), ("공원역", "1호선"),
                ("시장역", "2호선"), ("병원역", "2호선"), ("터미널역", "2호선"), ("강변역", "2호선")]
    rows = []
    for name, line in stations:
        for t in ["출근", "낮", "퇴근"]:
            ride = int(rng.integers(1000, 4200))
            if t == "퇴근":                       # 퇴근길에는 대부분 역에서 내리는 사람이 더 많다
                alight = int(ride * rng.uniform(1.1, 1.5))
            else:
                alight = int(ride * rng.uniform(0.6, 1.2))
            rows.append({"역이름": name, "노선": line, "시간대": t, "승차인원_count": ride, "하차인원_count": alight})
    df = pd.DataFrame(rows)
    # 심는 값: 승차 최댓값 = 중앙역·출근(6,000을 넘는 유일한 행), 최솟값 = 강변역·낮
    df.loc[(df["역이름"] == "중앙역") & (df["시간대"] == "출근"), "승차인원_count"] = int(rng.integers(9700, 9901))
    df.loc[(df["역이름"] == "강변역") & (df["시간대"] == "낮"), "승차인원_count"] = int(rng.integers(280, 330))
    save_orange_warmup(df, "week02", "subway_ridership")
    return df


# --- A-3. 우리 동네 대기환경 (시드 203) ----------------------------------------
def pm10_grade(pm10):
    """PM10 값 하나로 등급을 판정한다(교육용 구간: 좋음 0~30 · 보통 31~80 · 나쁨 81~150 · 매우나쁨 151 이상)."""
    if pm10 <= 30:
        return "좋음"
    elif pm10 <= 80:
        return "보통"
    elif pm10 <= 150:
        return "나쁨"
    else:
        return "매우나쁨"


def gen_orange_week03():
    rng = np.random.default_rng(203)
    n = 30
    # 등급별 일수를 고정한다: 좋음 7 · 보통 15 · 나쁨 6 · 매우나쁨 2(PM10 > 80인 날 8일)
    pm10 = np.concatenate([
        rng.integers(10, 31, size=7), rng.integers(31, 81, size=15),
        rng.integers(81, 151, size=6), rng.integers(151, 201, size=2),
    ])
    humid = np.concatenate([
        rng.integers(30, 91, size=22),
        rng.integers(71, 89, size=3),       # PM10 > 80이면서 습도 > 70인 날 3일
        rng.integers(40, 69, size=5),
    ])
    order = rng.permutation(n)
    pm10, humid = pm10[order], humid[order]
    temp = np.clip(np.linspace(9, 23, n) + rng.normal(0, 1.2, size=n), 8, 24)
    df = pd.DataFrame({
        "날짜": pd.date_range("2024-04-01", periods=n, freq="D").strftime("%Y-%m-%d"),
        "PM10_ug_m3": pm10,
        "PM2_5_ug_m3": np.round(pm10 * rng.uniform(0.4, 0.6, size=n)).astype(int),
        "기온_C": np.round(temp, 1),
        "습도_pct": humid,
    })
    df["등급"] = [pm10_grade(v) for v in df["PM10_ug_m3"]]
    save_orange_warmup(df, "week03", "air_quality")
    return df


# --- A-4. 반도체 8대 공정 흐름표 (난수 없음, 손으로 고정) --------------------------
def gen_orange_week04():
    rows = [
        # 공정순서, 공정명, 구분, 반복여부, 하는일, 생활비유, 주요설비, 대표측정값, 측정단위
        (1, "웨이퍼 제조", "전공정", "한 번", "규소를 녹여 둥근 기둥(잉곳)을 만들고 얇게 잘라 원판을 만든다",
         "피자 도우(웨이퍼) 만들기", "단결정 성장로·절단기", "웨이퍼 지름", "mm"),
        (2, "산화", "전공정", "여러 번", "웨이퍼 표면을 산소와 반응시켜 얇은 산화막(보호막)을 키운다",
         "철이 녹슬듯 표면에 얇은 막 키우기", "산화로", "산화막 두께", "nm"),
        (3, "포토", "전공정", "여러 번", "빛으로 회로 그림을 웨이퍼 위에 옮겨 찍는다",
         "사진 인화처럼 도우 위에 회로 그림 찍기", "노광기", "패턴 선폭", "nm"),
        (4, "식각", "전공정", "여러 번", "필요 없는 부분을 깎아 내 회로 모양만 남긴다",
         "판화처럼 그림 밖 부분 깎아 내기", "식각 장비", "식각률", "nm/min"),
        (5, "증착/이온주입", "전공정", "여러 번", "얇은 막을 쌓고, 이온을 넣어 전기가 통하는 성질을 바꾼다",
         "토핑을 층층이 올리고 소스를 스며들게 하기", "증착 장비·이온주입기", "막 두께", "nm"),
        (6, "금속 배선", "전공정", "여러 번", "층마다 금속 선을 깔아 회로 사이를 이어 전기가 흐르게 한다",
         "층마다 재료 사이를 전선처럼 잇기", "금속 증착 장비", "배선 저항", "Ω"),
        (7, "EDS(전기 검사)", "후공정", "한 번", "자르기 전 웨이퍼 상태에서 칩 하나하나에 전기를 넣어 제대로 동작하는지 검사한다",
         "자르기 전, 조각(칩)마다 전기로 검사", "테스터", "불량 칩 수", "count"),
        (8, "패키징", "후공정", "한 번", "칩을 잘라 외부와 연결하고 보호 껍데기를 씌운다",
         "조각을 하나씩 포장 상자에 담기", "패키징 장비", "외관 불량 수", "count"),
    ]
    df = pd.DataFrame(rows, columns=["공정순서", "공정명", "구분", "반복여부", "하는일", "생활비유",
                                     "주요설비", "대표측정값", "측정단위"])
    save_orange_warmup(df, "week04", "process_flow")
    return df


# --- A-5. 클린룸 환경 모니터링 (시드 205) --------------------------------------
def gen_orange_week05():
    rng = np.random.default_rng(205)
    rows = []
    for t in pd.date_range("2024-03-04 00:00", periods=24, freq="h"):
        for zone in ["A구역", "B구역", "C구역"]:
            mean = 1300 if zone == "B구역" else 1000      # B구역이 조금 높다(선택 관찰용)
            rows.append({
                "측정시간": t.strftime("%Y-%m-%d %H:%M"),
                "구역": zone,
                "파티클_count_per_m3": float(np.clip(round(rng.normal(mean, 250)), 500, 2000)),
                "온도_C": round(float(rng.normal(22.0, 0.25)), 1),
                "습도_pct": round(float(rng.normal(45, 1.5)), 1),
                "차압_Pa": round(float(rng.normal(12, 1.0)), 1),
            })
    df = pd.DataFrame(rows)
    # 결측(파티클 4 · 습도 3 · 차압 2)과 튀는 값(파티클 99,999 센서 오류 코드 1 · 차압 -5.0 1)을 서로 다른 행에 심는다
    picks = rng.choice(len(df), size=11, replace=False)
    df.loc[picks[0:4], "파티클_count_per_m3"] = np.nan
    df.loc[picks[4:7], "습도_pct"] = np.nan
    df.loc[picks[7:9], "차압_Pa"] = np.nan
    df.loc[picks[9], "파티클_count_per_m3"] = 99999
    df.loc[picks[10], "차압_Pa"] = -5.0
    df["파티클_count_per_m3"] = df["파티클_count_per_m3"].astype("Int64")   # 정수로 저장(빈칸은 빈칸)
    save_orange_warmup(df, "week05", "cleanroom_env")
    return df


# --- A-6. 웨이퍼 맵 한 장 (시드 206) -------------------------------------------
def week06_wafer_map():
    """A-6 웨이퍼 W-0601의 불합격 배열(가장자리형). generate_figures.py도 이 함수를 쓴다."""
    return wafer_fail_mask(np.random.default_rng(206), "edge", p_edge=0.5, p_base=0.03)


def gen_orange_week06():
    df = wafer_frame(week06_wafer_map())
    df.insert(0, "웨이퍼ID", "W-0601")
    save_orange_warmup(df, "week06", "wafer_map")
    return df


# --- A-7. 식각 설비 3대의 웨이퍼 12장 (시드 207) --------------------------------
WEEK07_WAFERS = [
    # 웨이퍼ID, 설비번호, 불량패턴, 합성기 설정
    ("W-01", "식각-1", "없음", ("random", {"p_base": 0.04})),
    ("W-02", "식각-1", "없음", ("random", {"p_base": 0.04})),
    ("W-03", "식각-1", "없음", ("random", {"p_base": 0.04})),
    ("W-04", "식각-1", "없음", ("random", {"p_base": 0.04})),
    ("W-05", "식각-2", "없음", ("random", {"p_base": 0.04})),
    ("W-06", "식각-2", "스크래치형", ("scratch", {"length": 24, "p_line": 0.95, "p_base": 0.04})),
    ("W-07", "식각-2", "없음", ("random", {"p_base": 0.04})),
    ("W-08", "식각-2", "없음", ("random", {"p_base": 0.04})),
    ("W-09", "식각-3", "가장자리형", ("edge", {"p_edge": 0.42, "p_base": 0.03})),
    ("W-10", "식각-3", "가장자리형", ("edge", {"p_edge": 0.42, "p_base": 0.03})),
    ("W-11", "식각-3", "가장자리형", ("edge", {"p_edge": 0.42, "p_base": 0.03})),
    ("W-12", "식각-3", "가장자리형", ("edge", {"p_edge": 0.42, "p_base": 0.03})),
]


def week07_wafer_maps():
    """A-7 웨이퍼 12장: (웨이퍼ID, 설비번호, 불량패턴, 불합격 배열). generate_figures.py도 이 함수를 쓴다."""
    rng = np.random.default_rng(207)
    return [(wid, eq, pat, wafer_fail_mask(rng, kind, **params)) for wid, eq, pat, (kind, params) in WEEK07_WAFERS]


def gen_orange_week07():
    frames = []
    for wid, eq, pat, fail in week07_wafer_maps():
        f = wafer_frame(fail)
        f.insert(0, "웨이퍼ID", wid)
        f.insert(1, "설비번호", eq)
        f.insert(5, "불량패턴", pat)
        frames.append(f)
    df = pd.concat(frames, ignore_index=True)
    save_orange_warmup(df, "week07", "wafer_lots")
    return df


# --- A-8. 식각 챔버 센서 기록 (시드 208) ---------------------------------------
def _decorrelate(values, target, keep):
    """values에서 target과 겹치는 부분을 빼고(최소제곱 잔차) 원래 평균·표준편차로 되돌린다.
    keep만큼 target 방향을 남겨 상관계수가 정확히 0이 아니라 0에 가까운 작은 값이 되게 한다."""
    zt = (target - target.mean()) / target.std()
    resid = values - values.mean()
    resid = resid - (resid @ zt) / (zt @ zt) * zt
    resid = resid / resid.std() + keep * zt
    return values.mean() + resid / resid.std() * values.std()


def gen_orange_week08():
    rng = np.random.default_rng(208)
    n = 200
    rf = rng.normal(500, 40, size=n)
    gas = rng.normal(100, 8, size=n)
    hours = (np.arange(n) * 2) % 200          # 2시간마다 기록, 200시간 쓰면 세정 → 다시 0(톱니 모양)

    def z(v):
        return (v - v.mean()) / v.std()

    # 교육용 가상 관계: 식각률은 RF파워·가스유량이 클수록 크고 누적사용시간이 길수록 작다(+ 잡음)
    etch = 250 + 25 * (0.8 * z(rf) + 0.3 * z(gas) - 0.5 * z(hours) + rng.normal(0, 0.12, size=n))
    pressure = _decorrelate(rng.normal(30, 3, size=n), etch, keep=0.04)   # 식각률과 거의 무관한 열
    temp = _decorrelate(rng.normal(60, 1.5, size=n), etch, keep=-0.03)    # 식각률과 거의 무관한 열
    df = pd.DataFrame({
        "측정시간": pd.date_range("2024-03-01 00:00", periods=n, freq="2h").strftime("%Y-%m-%d %H:%M"),
        "RF파워_W": np.round(rf, 1),
        "챔버압력_mTorr": np.round(pressure, 2),
        "가스유량_sccm": np.round(gas, 1),
        "누적사용시간_hr": hours,
        "챔버온도_C": np.round(temp, 2),
        "식각률_nm_min": np.round(etch, 1),
    })
    save_orange_warmup(df, "week08", "chamber_sensor")
    return df


# --- A-9. 웨이퍼 맵 패턴 분류 (시드 209) / A-10. 새 웨이퍼 10장 (시드 210) -----------
def _pattern_wafer(rng, label):
    """A-9 학습용 웨이퍼 한 장. 패턴 세기를 웨이퍼마다 달리해 일부가 헷갈리게 한다(완벽 분류 방지)."""
    if label == "정상":
        return wafer_fail_mask(rng, "count", n=int(rng.integers(3, 9)))
    if label == "중심형":
        return wafer_fail_mask(rng, "center", p_center=rng.uniform(0.15, 0.6), p_ring=rng.uniform(0.0, 0.1),
                               p_base=0.008)
    if label == "가장자리형":
        return wafer_fail_mask(rng, "edge", p_edge=rng.uniform(0.08, 0.5), p_base=0.008)
    return wafer_fail_mask(rng, "scratch", length=float(rng.uniform(5, 18)), p_line=0.85, p_base=0.008)


WEEK09_LABELS = ["정상"] * 120 + ["중심형"] * 40 + ["가장자리형"] * 40 + ["스크래치형"] * 40


def week09_wafer_maps():
    """A-9 웨이퍼 240장: (웨이퍼ID, 불량패턴, 불합격 배열). 섞은 순서대로 P-001부터 번호를 붙인다."""
    rng = np.random.default_rng(209)
    labels = [WEEK09_LABELS[i] for i in rng.permutation(len(WEEK09_LABELS))]
    return [(f"P-{i:03d}", lab, _pattern_wafer(rng, lab)) for i, lab in enumerate(labels, start=1)]


def gen_orange_week09():
    rows = [{"웨이퍼ID": wid, **wafer_summary(fail), "불량패턴": lab} for wid, lab, fail in week09_wafer_maps()]
    df = pd.DataFrame(rows)
    save_orange_warmup(df, "week09", "wafer_patterns")
    return df


# 의도 패턴(운영안에만 적는다. 데이터·그림에는 넣지 않는다):
# N-01 정상, N-02 가장자리형, N-03 중심형, N-04 애매(중심+가장자리), N-05 스크래치형,
# N-06 정상, N-07 애매(중심+가장자리), N-08 가장자리형, N-09 중심형, N-10 애매(중심+가장자리)
WEEK10_NEW = [
    ("N-01", ("count", {"n": 5})),
    ("N-02", ("edge", {"p_edge": 0.45, "p_base": 0.008})),
    ("N-03", ("center", {"p_center": 0.6, "p_ring": 0.08, "p_base": 0.008})),
    ("N-04", ("mix", {"n_center": 4, "n_edge": 5})),
    ("N-05", ("scratch", {"length": 14, "p_line": 0.85, "p_base": 0.008})),
    ("N-06", ("count", {"n": 6})),
    ("N-07", ("mix", {"n_center": 5, "n_edge": 3})),
    ("N-08", ("edge", {"p_edge": 0.35, "p_base": 0.008})),
    ("N-09", ("center", {"p_center": 0.5, "p_ring": 0.05, "p_base": 0.008})),
    ("N-10", ("mix", {"n_center": 3, "n_edge": 4})),
]


def week10_wafer_maps():
    """A-10 새 웨이퍼 10장: (웨이퍼ID, 불합격 배열). generate_figures.py도 이 함수를 쓴다."""
    rng = np.random.default_rng(210)
    return [(wid, wafer_fail_mask(rng, kind, **params)) for wid, (kind, params) in WEEK10_NEW]


def gen_orange_week10():
    df = pd.DataFrame([{"웨이퍼ID": wid, **wafer_summary(fail)} for wid, fail in week10_wafer_maps()])
    save_orange_warmup(df, "week10", "new_wafers")
    return df


ORANGE_WARMUP_GENERATORS = [
    gen_orange_week01, gen_orange_week02, gen_orange_week03, gen_orange_week04, gen_orange_week05,
    gen_orange_week06, gen_orange_week07, gen_orange_week08, gen_orange_week09, gen_orange_week10,
]


# ===========================================================================
# Orange3용 .tab 파생본 — data/weekly/weekXX/orange/<같은 이름>.tab (2026-10-23 추가)
# ---------------------------------------------------------------------------
# Orange 3.35는 utf-8-sig CSV의 BOM을 첫 열 이름에 붙여 읽고('﻿측정시간'),
# 1/-1 합격여부를 숫자(연속형)로 잡는다. 그래서 Orange 실습은 이 파생본을 연다.
# - 저장된 CSV를 다시 읽어 글자 그대로 옮긴다(난수를 다시 뽑지 않는다).
# - Orange 3행 헤더: 열 이름 / 형식(c 연속, d 범주, s 문자열, time 시간) / 역할(class, meta).
# - UTF-8(BOM 없음), 탭 구분, 결측은 빈 칸.
# - CSV를 지운 경우 남은 .tab도 지운다.
# ===========================================================================
ORANGE_DIR = "orange"
# 결과 열(1/-1) → 범주형 목표(class). 값 순서 "1 -1"이라 막대·색이 합격(좋은 쪽)부터 나온다.
ORANGE_CLASS_COLUMNS = {"합격여부", "진행여부", "정답여부", "평가", "손님평가"}
# 행을 구별하는 열 → meta(표에는 보이지만 분석·모델 입력에서 빠진다)
ORANGE_META_COLUMNS = {"로트번호", "웨이퍼번호", "이름", "주문번호", "측정시간", "날짜"}
# 결과가 나온 뒤에만 채워지는 열(불합격일 때만 값이 있음) → 범주형 meta.
# 입력(attribute)에 두면 9·10차시 모델이 이 열로 정답을 그대로 맞혀 버린다(정답 누설).
ORANGE_RESULT_DETAIL_COLUMNS = {"불량유형", "오답유형"}
# 특정 파일만 예외로 지정: {"파일 이름(확장자 제외)": {"열": ("형식", "역할")}}  (열은 원래 이름·바꾼 이름 모두 가능)
ORANGE_ROLE_OVERRIDES = {
    # 9·10차시: 파이썬 모델이 숫자 열 6개만 쓰므로 Orange도 같은 입력으로 맞춘다(스펙 0-11)
    "week09_pass_fail_train": {"공정명": ("d", "meta"), "설비번호": ("d", "meta")},
    "week09_new_lots_to_predict": {"공정명": ("d", "meta"), "설비번호": ("d", "meta")},
    # Orange 워밍업 데이터(스펙 부록 A). 이름·설명 열은 표에서만 보는 meta
    "week01_orange_town_population": {"동": ("s", "meta")},
    "week02_orange_subway_ridership": {"역이름": ("s", "meta")},
    "week04_orange_process_flow": {c: ("s", "meta") for c in ["하는일", "생활비유", "주요설비", "대표측정값"]},
    "week06_orange_wafer_map": {"웨이퍼ID": ("s", "meta")},
    # 7차시 웨이퍼ID·불량패턴은 Pivot Table·Select Rows에 쓰도록 일반 범주형(기본 규칙)으로 둔다
    "week09_orange_wafer_patterns": {"웨이퍼ID": ("s", "meta"), "불량패턴": ("정상 중심형 가장자리형 스크래치형", "class")},
    "week10_orange_new_wafers": {"웨이퍼ID": ("s", "meta")},
}

# 차시별 열 이름 바꾸기(.tab에만 적용, CSV는 그대로): {"week05": {"온도_섭씨": "온도_C"}}
# 기존 CSV 열 이름을 단위 표기 규칙으로 차시마다 옮겨 갈 때 쓴다. 역할 규칙은 원래 이름과 바꾼 이름 어느 쪽으로도 찾는다.
# 아직 적용한 차시는 없다.
ORANGE_COLUMN_RENAMES = {}

_ISO_TIME = r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}(:\d{2})?)?$"


def _orange_column_header(names, raw, parsed):
    """(형식, 역할)과 .tab에 쓸 값 목록을 돌려준다. names = {원래 열 이름, 바꾼 열 이름}."""
    filled = raw[raw != ""]
    if names & ORANGE_CLASS_COLUMNS:
        # 결측이 섞이면 pandas가 1.0/-1.0으로 저장한다 → 범주 이름은 1/-1로 통일
        values = raw.map(lambda v: v if v == "" else str(int(float(v))))
        kinds = set(values[values != ""])
        return ("1 -1" if kinds <= {"1", "-1"} else "d"), "class", values
    if names & ORANGE_RESULT_DETAIL_COLUMNS:
        return "d", "meta", raw
    role = "meta" if names & ORANGE_META_COLUMNS else ""
    if pd.api.types.is_numeric_dtype(parsed):
        return "c", role, raw
    if len(filled) and filled.str.match(_ISO_TIME).all():
        return "time", role, raw
    if names & ORANGE_META_COLUMNS:
        return "s", "meta", raw
    return "d", role, raw


def write_orange_tab(csv_path):
    """CSV 하나를 Orange용 .tab으로 옮긴다."""
    raw = pd.read_csv(csv_path, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    parsed = pd.read_csv(csv_path, encoding="utf-8-sig")
    stem = os.path.splitext(os.path.basename(csv_path))[0]
    overrides = ORANGE_ROLE_OVERRIDES.get(stem, {})
    renames = ORANGE_COLUMN_RENAMES.get(os.path.basename(os.path.dirname(csv_path)), {})

    names, types, flags, columns = [], [], [], []
    for col in raw.columns:
        new = renames.get(col, col)
        typ, flag, values = _orange_column_header({col, new}, raw[col], parsed[col])
        typ, flag = overrides.get(new, overrides.get(col, (typ, flag)))
        names.append(new)
        types.append(typ)
        flags.append(flag)
        columns.append(values)

    out_dir = os.path.join(os.path.dirname(csv_path), ORANGE_DIR)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, stem + ".tab")
    lines = ["\t".join(names), "\t".join(types), "\t".join(flags)]
    lines += ["\t".join(row) for row in zip(*columns)]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[Orange] {path}")
    return path


def write_orange_tabs():
    """data/weekly/week*/ 의 모든 CSV(새로 추가된 CSV 포함)에 대해 .tab을 만든다. main() 끝에서 부른다."""
    for week in sorted(os.listdir(WEEKLY)):
        wdir = os.path.join(WEEKLY, week)
        if not os.path.isdir(wdir):
            continue
        stems = set()
        for f in sorted(os.listdir(wdir)):
            if f.endswith(".csv"):
                write_orange_tab(os.path.join(wdir, f))
                stems.add(f[:-4])
        odir = os.path.join(wdir, ORANGE_DIR)
        if os.path.isdir(odir):
            for f in os.listdir(odir):
                if f.endswith(".tab") and f[:-4] not in stems:
                    os.remove(os.path.join(odir, f))
                    print(f"[Orange 삭제] {os.path.join(odir, f)} (원본 CSV 없음)")


def main():
    gen_week01()
    gen_week02()
    gen_week03()
    gen_week04()
    gen_week05()
    gen_week06()
    gen_week07()
    gen_week08()
    gen_week09()
    gen_week10()
    gen_easy_all()  # 생활 예제 데이터(별도 시드·고정 값) — 반도체 데이터 뒤에 만들어 기존 결과에 영향 없음
    for gen in ORANGE_WARMUP_GENERATORS:  # Orange 워밍업 데이터(별도 시드·고정 값) — 마찬가지로 맨 뒤
        gen()
    write_orange_tabs()  # 모든 CSV를 저장한 뒤 Orange용 .tab 파생본을 만든다
    print("\n모든 주차 데이터 생성 완료.")


if __name__ == "__main__":
    main()
