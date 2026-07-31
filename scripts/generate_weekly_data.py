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
    gas = rng.normal(50, 3, size=n)          # 검사결과와 무관/약한 변수(대조군)
    humidity = rng.normal(45, 4, size=n)     # 검사결과와 무관/약한 변수(대조군)
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
    result = np.array([rng.choice([0, 1], p=[1 - p, p]) for p in fail_prob])  # 0=합격, 1=불합격

    df = pd.DataFrame({
        "공정명": process,
        "설비번호": equip,
        "온도_섭씨": np.round(temp, 1),
        "압력_Pa": np.round(pressure, 1),
        "가스유량_slm": np.round(gas, 2),
        "두께_nm": np.round(thickness, 2),
        "진공도_mTorr": np.round(vacuum, 2),
        "습도_pct": np.round(humidity, 1),
        "검사결과": result,
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

    result = np.array([rng.choice([0, 1], p=[1 - p, p]) for p in fail_prob])  # 0=정상, 1=이상
    defect = np.where(result == 1, rng.choice(DEFECT_TYPES, size=n), "")

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
        "검사결과": result,
    })
    save_csv(df, "week10", "week10_mini_project_dataset.csv")
    return df


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
    print("\n모든 주차 데이터 생성 완료.")


if __name__ == "__main__":
    main()
