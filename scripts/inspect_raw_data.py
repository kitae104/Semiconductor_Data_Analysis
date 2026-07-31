"""원본 데이터(data/raw)를 읽기 전용으로 분석해 요약 통계를 출력하는 스크립트.
원본 파일은 절대 수정하지 않는다. 실행: python scripts/inspect_raw_data.py
"""
import os
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")


def inspect_sample():
    path = os.path.join(RAW, "반도체_공정_샘플.csv")
    df = pd.read_csv(path, encoding="utf-8-sig")
    print("=== 반도체_공정_샘플.csv ===")
    print("shape:", df.shape)
    print(df.dtypes)
    print("결측값 개수:\n", df.isna().sum())
    if "합격여부" in df.columns:
        print("합격여부 분포:\n", df["합격여부"].value_counts())
    return df


def inspect_fab():
    path = os.path.join(RAW, "fab.csv")
    df = pd.read_csv(path, encoding="utf-8-sig")
    print("\n=== fab.csv ===")
    print("shape:", df.shape)
    sensor_cols = [c for c in df.columns if c.startswith("Sensor") and c != "SensorTime"]
    na_frac = df[sensor_cols].isna().mean()
    stds = df[sensor_cols].std()
    nunique = df[sensor_cols].nunique()
    print("센서 개수:", len(sensor_cols))
    print("결측률 50% 초과 센서 수:", int((na_frac > 0.5).sum()))
    print("값이 거의 변하지 않는 센서 수(std==0):", int((stds.fillna(0) == 0).sum()))
    good = [c for c in sensor_cols if na_frac[c] < 0.05 and (stds[c] or 0) > 0 and nunique[c] > 10]
    print("교육용 후보(결측<5%, std>0, 고유값>10) 센서 수:", len(good))
    if "Pass_Fail" in df.columns:
        print("Pass_Fail 분포:\n", df["Pass_Fail"].value_counts())
    return df, good


if __name__ == "__main__":
    inspect_sample()
    inspect_fab()
