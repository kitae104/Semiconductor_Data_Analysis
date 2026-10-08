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

    save_csv(df, "week09", "week09_pass_fail_train.csv")

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
    save_csv(new_df, "week09", "week09_new_lots_to_predict.csv")
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
    save_csv(df, "week10", "week10_mini_project_dataset.csv")
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
        # 주문번호, 매장, 메뉴, 종류, 가격_원, 수량_개, 평가(1=좋아요, -1=별로예요)
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
    save_csv(df, "week06", "week06_easy_icecream_daily.csv")
    return df


def gen_easy_week07():
    """반별 쪽지시험 문항 기록 24행 — groupby 개수·합·평균, 학생별 정답률, 오답유형 파레토 연습용.

    반도체 7차시와 같은 모양: 반 = 설비번호, 학생 = 로트(문항 4개 = 웨이퍼 4장),
    정답여부(1/-1) = 합격여부, 오답유형(정답이면 빈 값) = 불량유형, 풀이시간_초 = 온도_섭씨.
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
    save_csv(df, "week09", "week09_easy_outdoor_class.csv")
    return df


def gen_easy_week10():
    """10차시: 9차시와 같은 학습 데이터(10차시 폴더에 따로 저장) + 정답 없는 예보 7일(손으로 고정한 값)."""
    train = _easy_outdoor_class_df()
    save_csv(train, "week10", "week10_easy_outdoor_class_train.csv")

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
    save_csv(new_days, "week10", "week10_easy_outdoor_class_new_days.csv")
    return train, new_days


def gen_easy_all():
    gen_easy_week04()
    gen_easy_week05()
    gen_easy_week06()
    gen_easy_week07()
    gen_easy_week08()
    gen_easy_week09()
    gen_easy_week10()


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
    print("\n모든 주차 데이터 생성 완료.")


if __name__ == "__main__":
    main()
