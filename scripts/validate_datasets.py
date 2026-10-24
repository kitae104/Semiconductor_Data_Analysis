"""주차별 데이터 검증 스크립트.

확인 항목(스펙 14장):
- CSV가 정상적으로 열리는가 (인코딩 포함)
- 필수 열이 존재하는가
- 합격/불합격 값이 문서 설명과 일치하는가
- 주차별 의도한 결측값/이상값이 존재하는가
- 수율 계산이 올바른가 (week07)
- 데이터가 재현 가능한가 (동일 스크립트 재실행 시 동일 결과인지 해시로 확인)
- Orange용 .tab 파생본(weekXX/orange/)이 CSV마다 있고 행 수·열 이름·값이 CSV와 같은가

실행: python scripts/validate_datasets.py
결과는 콘솔에 출력되고, 요약이 reports/validation-report.html 생성 시 사용된다.
"""
import os
import sys
import hashlib
import pandas as pd

sys.dont_write_bytecode = True  # scripts/__pycache__를 남기지 않는다
from generate_weekly_data import ORANGE_COLUMN_RENAMES, ORANGE_CLASS_COLUMNS as ONE_MINUS_ONE  # noqa: E402  (scripts/ 폴더의 생성 스크립트, 실행하지 않고 상수만 읽음)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEEKLY = os.path.join(BASE, "data", "weekly")

RESULTS = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    RESULTS.append((name, status, detail))
    print(f"[{status}] {name} {('- ' + detail) if detail and status == 'FAIL' else ''}")
    return condition


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def validate_week(week, filename, required_cols, encoding="utf-8-sig"):
    path = os.path.join(WEEKLY, week, filename)
    ok = check(f"{filename} 파일 존재", os.path.exists(path), path)
    if not ok:
        return None
    try:
        df = pd.read_csv(path, encoding=encoding)
    except Exception as e:
        check(f"{filename} 정상 로드(인코딩 포함)", False, str(e))
        return None
    check(f"{filename} 정상 로드(인코딩 포함)", True)
    missing = [c for c in required_cols if c not in df.columns]
    check(f"{filename} 필수 열 존재", len(missing) == 0, f"누락: {missing}")
    return df


def validate_easy():
    """생활 예제(easy) 데이터 검증 — 4~10차시. 강의가 인용하는 심은 패턴과 실제 수치를 함께 확인한다."""
    print("\n=== 생활 예제(easy) 데이터 ===")

    e4 = validate_week("week04", "week04_easy_cafe_orders.csv",
                       ["주문번호", "매장", "메뉴", "종류", "가격_KRW", "수량_count", "평가"])
    if e4 is not None:
        check("easy04 크기 12행 x 7열", e4.shape == (12, 7), str(e4.shape))
        check("easy04 평가 값 범위(1/-1)", set(e4["평가"].unique()) <= {1, -1})
        check("easy04 조건 검색 건수(커피 5, 가격>5000 5, 별로예요 4, 가격>5000&별로예요 3)",
              (e4["종류"] == "커피").sum() == 5 and (e4["가격_KRW"] > 5000).sum() == 5
              and (e4["평가"] == -1).sum() == 4
              and ((e4["가격_KRW"] > 5000) & (e4["평가"] == -1)).sum() == 3)
        bad_rate = e4.groupby("종류")["평가"].apply(lambda s: (s == -1).mean())
        check("easy04 별로예요 비율 1위는 디저트(의도된 패턴)", bad_rate.idxmax() == "디저트", str(bad_rate.to_dict()))

    e5 = validate_week("week05", "week05_easy_class_records.csv",
                       ["이름", "반", "키_cm", "몸무게_kg", "수학점수_pt"])
    if e5 is not None:
        check("easy05 15행", len(e5) == 15, str(len(e5)))
        check("easy05 결측 3칸(반·키·몸무게 각 1)",
              e5.isna().sum().sum() == 3 and e5["반"].isna().sum() == 1
              and e5["키_cm"].isna().sum() == 1 and e5["몸무게_kg"].isna().sum() == 1,
              str(e5.isna().sum().to_dict()))
        check("easy05 완전 중복 1행", e5.duplicated().sum() == 1, str(e5.duplicated().sum()))
        check("easy05 입력 실수 이상값(키 250cm 초과) 1건", (e5["키_cm"] > 250).sum() == 1)
        cleaned = e5.dropna(subset=["반"]).copy()
        for col in ["키_cm", "몸무게_kg"]:
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
        cleaned = cleaned.drop_duplicates()
        cleaned = cleaned[cleaned["키_cm"] <= 250]
        check("easy05 강의 순서로 정리하면 12행", len(cleaned) == 12, str(len(cleaned)))

    e6 = validate_week("week06", "week06_easy_icecream_daily.csv",
                       ["날짜", "요일", "날씨", "최고기온_C", "판매량_count"])
    if e6 is not None:
        check("easy06 21행", len(e6) == 21, str(len(e6)))
        try:
            d = pd.to_datetime(e6["날짜"], format="%Y-%m-%d")
            check("easy06 날짜가 YYYY-MM-DD로 변환되고 하루 간격", (d.diff().dropna() == pd.Timedelta(days=1)).all())
        except Exception as e:  # noqa: BLE001
            check("easy06 날짜가 YYYY-MM-DD로 변환되고 하루 간격", False, str(e))
        r = e6["최고기온_C"].corr(e6["판매량_count"])
        check("easy06 기온-판매량 강한 양의 관계(r>0.8)", r > 0.8, f"r={r:.2f}")
        med = e6.groupby("날씨")["판매량_count"].median()
        check("easy06 비 오는 날 판매량 중앙값이 가장 낮음(박스플롯 패턴)", med.idxmin() == "비", str(med.to_dict()))

    e7 = validate_week("week07", "week07_easy_quiz_results.csv",
                       ["반", "이름", "문제번호", "풀이시간_sec", "오답유형", "정답여부"])
    if e7 is not None:
        check("easy07 24행(3반 x 2명 x 4문항)", len(e7) == 24, str(len(e7)))
        check("easy07 정답여부 값 범위(1/-1)", set(e7["정답여부"].unique()) <= {1, -1})
        check("easy07 오답유형은 오답(-1)일 때만 채워짐",
              (e7["오답유형"].notna() == (e7["정답여부"] == -1)).all())
        ok = e7["정답여부"] == 1
        cls = ok.groupby(e7["반"]).mean() * 100
        check("easy07 반별 정답률 A 87.5 / B 62.5 / C 75.0",
              cls.round(1).to_dict() == {"A반": 87.5, "B반": 62.5, "C반": 75.0}, str(cls.to_dict()))
        stu = ok.groupby(e7["이름"]).mean() * 100
        check("easy07 학생별 정답률 80% 미만 4명, 최저는 예린 25%",
              (stu < 80).sum() == 4 and stu.idxmin() == "예린" and stu.min() == 25.0, str(stu.to_dict()))
        wc = e7[e7["정답여부"] == -1]["오답유형"].value_counts()
        check("easy07 오답유형 파레토 1위 계산 실수(3건)", wc.index[0] == "계산 실수" and wc.iloc[0] == 3, str(wc.to_dict()))

    e8 = validate_week("week08", "week08_easy_weather_sales.csv",
                       ["날짜", "최고기온_C", "습도_pct", "아이스크림판매량_count", "핫초코판매량_cup", "냉동고온도_C", "손님평가"])
    if e8 is not None:
        check("easy08 30행", len(e8) == 30, str(len(e8)))
        check("easy08 손님평가 값 범위(1/-1)", set(e8["손님평가"].unique()) <= {1, -1})
        r_ice = e8["최고기온_C"].corr(e8["아이스크림판매량_count"])
        r_choco = e8["최고기온_C"].corr(e8["핫초코판매량_cup"])
        r_hum = e8["습도_pct"].corr(e8["아이스크림판매량_count"])
        r_fz = e8["냉동고온도_C"].corr(e8["손님평가"])
        check("easy08 기온-아이스크림 강한 양의 관계(r>0.8)", r_ice > 0.8, f"r={r_ice:.2f}")
        check("easy08 기온-핫초코 강한 음의 관계(r<-0.8)", r_choco < -0.8, f"r={r_choco:.2f}")
        check("easy08 습도-아이스크림 관계 없음(|r|<0.1)", abs(r_hum) < 0.1, f"r={r_hum:.2f}")
        fz = e8["냉동고온도_C"]
        out = e8[(fz < -20) | (fz > -16)]
        inn = e8[(fz >= -20) & (fz <= -16)]
        out_rate = (out["손님평가"] == -1).mean()
        in_rate = (inn["손님평가"] == -1).mean()
        check("easy08 냉동고 범위 밖 불만률이 범위 안보다 큼(U자 패턴, 밖 8건 중 6 / 안 22건 중 2)",
              len(out) == 8 and (out["손님평가"] == -1).sum() == 6 and (inn["손님평가"] == -1).sum() == 2,
              f"밖 {out_rate:.1%}, 안 {in_rate:.1%}")
        check("easy08 냉동고-손님평가 상관계수는 0에 가까움(|r|<0.2, 상관계수가 놓치는 경우)",
              abs(r_fz) < 0.2, f"r={r_fz:.2f}")

    feature_cols = ["최고기온_C", "습도_pct", "풍속_m_s", "강수량_mm"]
    e9 = validate_week("week09", "week09_easy_outdoor_class.csv", ["날짜"] + feature_cols + ["진행여부"])
    if e9 is not None:
        check("easy09 120행", len(e9) == 120, str(len(e9)))
        check("easy09 진행여부 값 범위(1/-1)", set(e9["진행여부"].unique()) <= {1, -1})
        check("easy09 결측 4칸(정리 복습용)", e9.isna().sum().sum() == 4, str(e9.isna().sum().to_dict()))
        d9 = e9.dropna()
        major = (d9["진행여부"] == 1).mean()
        check("easy09 다수 클래스(진행) 비율 70~80%", 0.70 <= major <= 0.80, f"{major:.1%}")
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.tree import DecisionTreeClassifier
            X, y = d9[feature_cols], d9["진행여부"]
            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            model = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_tr, y_tr)
            acc = model.score(X_te, y_te)
            base = (y_te == 1).mean()
            check("easy09 결정트리(max_depth=4) 정확도가 '무조건 진행' 기준선보다 높음",
                  acc > base, f"정확도 {acc:.1%}, 기준선 {base:.1%}")
            hum = dict(zip(feature_cols, model.feature_importances_))["습도_pct"]
            check("easy09 관계없는 비교용 열(습도) 중요도 0%", hum == 0, f"{hum:.1%}")
        except ImportError as e:
            check("easy09 모델 검증(scikit-learn 필요)", False, str(e))

    e10 = validate_week("week10", "week10_easy_outdoor_class_train.csv", ["날짜"] + feature_cols + ["진행여부"])
    if e10 is not None and e9 is not None:
        check("easy10 학습 데이터가 9차시 easy 데이터와 같은 내용", e10.equals(e9))
    e10n = validate_week("week10", "week10_easy_outdoor_class_new_days.csv", ["날짜"] + feature_cols)
    if e10n is not None:
        check("easy10 예보 데이터 5~8행", 5 <= len(e10n) <= 8, str(len(e10n)))
        check("easy10 예보 데이터에 정답(진행여부) 없음", "진행여부" not in e10n.columns)


def validate_orange_warmups():
    """Orange 워밍업 데이터(weekXX_orange_*.csv, 스펙 부록 A) — 행 수·열 이름과 심은 패턴(aha 확인)을 실측으로 확인한다."""
    print("\n=== Orange 워밍업 데이터 ===")
    a1 = validate_week("week01", "week01_orange_town_population.csv", ["구", "동", "인구_count", "면적_km2", "주요연령대"])
    if a1 is not None:
        vc = a1["주요연령대"].value_counts().to_dict()
        check("A-1 30행, 동 30개 고유", len(a1) == 30 and a1["동"].nunique() == 30, str(a1.shape))
        check("A-1 주요연령대 40~50대 12 · 20~30대 9 · 60대이상 6 · 10대이하 3",
              vc == {"40~50대": 12, "20~30대": 9, "60대이상": 6, "10대이하": 3}, str(vc))
        top = a1.groupby("구")["주요연령대"].agg(lambda s: s.value_counts().idxmax())
        check("A-1 20~30대가 가장 많은 구는 새빛구뿐", list(top[top == "20~30대"].index) == ["새빛구"], str(top.to_dict()))
    a2 = validate_week("week02", "week02_orange_subway_ridership.csv", ["역이름", "노선", "시간대", "승차인원_count", "하차인원_count"])
    if a2 is not None:
        ride = a2["승차인원_count"]
        check("A-2 24행", len(a2) == 24, str(len(a2)))
        check("A-2 승차 최댓값 = 중앙역·출근, 6,000 초과는 그 1행",
              a2.loc[ride.idxmax(), ["역이름", "시간대"]].tolist() == ["중앙역", "출근"] and (ride > 6000).sum() == 1)
        check("A-2 승차 최솟값 = 강변역·낮", a2.loc[ride.idxmin(), ["역이름", "시간대"]].tolist() == ["강변역", "낮"])
        check("A-2 승차 평균 2,500~3,000, 최댓값이 평균의 3배 이상",
              2500 <= ride.mean() <= 3000 and ride.max() >= 3 * ride.mean(), f"평균 {ride.mean():.1f}")
    a3 = validate_week("week03", "week03_orange_air_quality.csv", ["날짜", "PM10_ug_m3", "PM2_5_ug_m3", "기온_C", "습도_pct", "등급"])
    if a3 is not None:
        pm = a3["PM10_ug_m3"]
        check("A-3 등급 좋음 7 · 보통 15 · 나쁨 6 · 매우나쁨 2",
              a3["등급"].value_counts().to_dict() == {"보통": 15, "좋음": 7, "나쁨": 6, "매우나쁨": 2})
        check("A-3 PM10 > 80 8일, 그중 습도 > 70 3일", (pm > 80).sum() == 8 and ((pm > 80) & (a3["습도_pct"] > 70)).sum() == 3)
        grade = pd.cut(pm, [-1, 30, 80, 150, 10 ** 6], labels=["좋음", "보통", "나쁨", "매우나쁨"]).astype(str)
        check("A-3 등급이 PM10 구간 규칙과 일치", (grade == a3["등급"]).all())
    a4 = validate_week("week04", "week04_orange_process_flow.csv",
                       ["공정순서", "공정명", "구분", "반복여부", "하는일", "생활비유", "주요설비", "대표측정값", "측정단위"])
    if a4 is not None:
        check("A-4 8행, 반복여부 '여러 번' 5행(②~⑥ — 금속 배선도 여러 층)", len(a4) == 8
              and list(a4.loc[a4["반복여부"] == "여러 번", "공정순서"]) == [2, 3, 4, 5, 6])
    a5 = validate_week("week05", "week05_orange_cleanroom_env.csv", ["측정시간", "구역", "파티클_count_per_m3", "온도_C", "습도_pct", "차압_Pa"])
    if a5 is not None:
        p = a5["파티클_count_per_m3"]
        na = a5.isna().sum()
        check("A-5 72행, 결측 파티클 4 · 습도 3 · 차압 2(서로 다른 행)",
              len(a5) == 72 and (na["파티클_count_per_m3"], na["습도_pct"], na["차압_Pa"]) == (4, 3, 2)
              and a5.isna().any(axis=1).sum() == 9, str(na.to_dict()))
        check("A-5 튀는 값 파티클 99,999 1행 · 차압 -5.0 1행", (p == 99999).sum() == 1 and (a5["차압_Pa"] == -5.0).sum() == 1)
        normal = p[p < 10000].mean()
        check("A-5 평균으로 채운 값(99,999 포함 평균)이 정상 평균의 2배 이상", p.mean() >= 2 * normal,
              f"채움 {p.mean():.1f} / 정상 {normal:.1f}")
    a6 = validate_week("week06", "week06_orange_wafer_map.csv", ["웨이퍼ID", "다이_X", "다이_Y", "중심거리_mm", "합격여부"])
    if a6 is not None:
        fail = a6["합격여부"] == -1
        check("A-6 다이 317개, 불합격 55~75개, 그중 85% 이상 가장자리",
              len(a6) == 317 and 55 <= fail.sum() <= 75 and (a6.loc[fail, "중심거리_mm"] > 112).mean() >= 0.85,
              f"불합격 {fail.sum()}")
    a7 = validate_week("week07", "week07_orange_wafer_lots.csv", ["웨이퍼ID", "설비번호", "다이_X", "다이_Y", "중심거리_mm", "불량패턴", "합격여부"])
    if a7 is not None:
        y = (a7["합격여부"] == 1).groupby(a7["설비번호"]).mean() * 100
        check("A-7 3,804행, 식각-3 수율이 가장 낮고 최고와 10%p 이상 차이",
              len(a7) == 3804 and y.idxmin() == "식각-3" and y.max() - y.min() >= 10, str(y.round(1).to_dict()))
    a8 = validate_week("week08", "week08_orange_chamber_sensor.csv",
                       ["측정시간", "RF파워_W", "챔버압력_mTorr", "가스유량_sccm", "누적사용시간_hr", "챔버온도_C", "식각률_nm_min"])
    if a8 is not None:
        r = a8.drop(columns="측정시간").corr()["식각률_nm_min"]
        check("A-8 상관 RF +0.75~0.85 · 누적사용시간 -0.6~-0.4 · 가스 +0.2~0.4 · 압력·온도 |r|<0.1",
              0.75 <= r["RF파워_W"] <= 0.85 and -0.6 <= r["누적사용시간_hr"] <= -0.4 and 0.2 <= r["가스유량_sccm"] <= 0.4
              and abs(r["챔버압력_mTorr"]) < 0.1 and abs(r["챔버온도_C"]) < 0.1, str(r.round(3).to_dict()))
    feats = ["불량다이수_count", "중심불량비율_pct", "가장자리불량비율_pct", "직선불량비율_pct"]
    a9 = validate_week("week09", "week09_orange_wafer_patterns.csv", ["웨이퍼ID"] + feats + ["불량패턴"])
    if a9 is not None:
        check("A-9 240행(정상 120 · 중심형 40 · 가장자리형 40 · 스크래치형 40)",
              a9["불량패턴"].value_counts().to_dict() == {"정상": 120, "중심형": 40, "가장자리형": 40, "스크래치형": 40})
        normal = a9[a9["불량패턴"] == "정상"]["불량다이수_count"]
        check("A-9 정상 웨이퍼 불량 다이 3~8개", normal.between(3, 8).all())
    a10 = validate_week("week10", "week10_orange_new_wafers.csv", ["웨이퍼ID"] + feats)
    if a10 is not None:
        check("A-10 10행, 정답 열(불량패턴) 없음", len(a10) == 10 and "불량패턴" not in a10.columns)
    # A-9 Tree 교차검증 정확도와 A-10 모델 의견 갈림은 Orange가 필요해 validate_orange_workflows 쪽 실측 보고로 확인한다.


def validate_orange_tabs():
    """Orange용 .tab 파생본 검증 — CSV마다 하나, BOM 없음, 3행 헤더, 행 수·열·값이 CSV와 같음."""
    print("\n=== Orange용 .tab 파생본 ===")
    for week in sorted(os.listdir(WEEKLY)):
        wdir = os.path.join(WEEKLY, week)
        if not os.path.isdir(wdir):
            continue
        for f in sorted(os.listdir(wdir)):
            if not f.endswith(".csv"):
                continue
            stem = f[:-4]
            tab = os.path.join(wdir, "orange", stem + ".tab")
            if not check(f"{stem}.tab 파일 존재", os.path.exists(tab), tab):
                continue
            with open(tab, "rb") as fh:
                head = fh.read(3)
            check(f"{stem}.tab BOM 없음", head != b"\xef\xbb\xbf")
            csv = pd.read_csv(os.path.join(wdir, f), encoding="utf-8-sig", dtype=str, keep_default_na=False)
            t = pd.read_csv(tab, sep="\t", encoding="utf-8", dtype=str, keep_default_na=False, skiprows=[1, 2])
            types = pd.read_csv(tab, sep="\t", encoding="utf-8", dtype=str, keep_default_na=False, nrows=2)
            renames = ORANGE_COLUMN_RENAMES.get(week, {})
            csv = csv.rename(columns=renames)  # .tab에서만 바꾼 열 이름(generate_weekly_data.ORANGE_COLUMN_RENAMES)
            check(f"{stem}.tab 열 이름이 CSV와 같음(차시별 이름 바꾸기 반영)", list(t.columns) == list(csv.columns),
                  f"tab {list(t.columns)} / csv {list(csv.columns)}")
            check(f"{stem}.tab 행 수가 CSV와 같음({len(csv)}행)", len(t) == len(csv), str(len(t)))
            if list(t.columns) != list(csv.columns) or len(t) != len(csv):
                continue
            diff = []
            for col in csv.columns:
                a, b = csv[col], t[col]
                if types.loc[1, col] == "class" and col in ONE_MINUS_ONE:  # 결과 열은 1.0 → 1로 정리해 저장한다
                    a = a.map(lambda v: v if v == "" else str(int(float(v))))
                    check(f"{stem}.tab {col} 범주형 1/-1(class)", types.loc[0, col] == "1 -1", types.loc[0, col])
                if not a.equals(b):
                    diff.append(col)
            check(f"{stem}.tab 값이 CSV와 같음", not diff, f"다른 열: {diff}")


def main():
    w1 = validate_week("week01", "week01_semiconductor_process_overview.csv",
                        ["측정시간", "로트번호", "웨이퍼번호", "공정명", "설비번호", "온도_C", "압력_Pa", "합격여부"])
    if w1 is not None:
        check("week01 합격여부 값 범위", set(w1["합격여부"].unique()) <= {1, -1})

    w2 = validate_week("week02", "week02_python_basics_1.csv",
                       ["로트번호", "공정명", "설비번호", "온도_C", "합격여부"])
    if w2 is not None:
        eq03 = w2.loc[w2["설비번호"] == "EQ-03", "온도_C"]
        check("week02 20행, 온도 최저 292.2 · 최고 317.9", len(w2) == 20 and w2["온도_C"].min() == 292.2
              and w2["온도_C"].max() == 317.9, f"{len(w2)}행")
        check("week02 EQ-03 7건, 최고 308.5 · 최저 292.2(강의·실습지 수치)",
              len(eq03) == 7 and eq03.max() == 308.5 and eq03.min() == 292.2, str(eq03.tolist()))

    w3 = validate_week("week03", "week03_python_basics_2.csv",
                       ["로트번호", "공정명", "설비번호", "온도_C", "합격여부"])
    if w3 is not None:
        out = ~w3["온도_C"].between(295, 305)
        fail = w3["합격여부"] == -1
        check("week03 30행, 범위(295~305) 밖 12건, 그중 불합격 3건, 범위 안 불합격 0건",
              len(w3) == 30 and out.sum() == 12 and (out & fail).sum() == 3 and (~out & fail).sum() == 0,
              f"밖 {out.sum()}, 밖·불합격 {(out & fail).sum()}, 안·불합격 {(~out & fail).sum()}")
        eq04 = w3[w3["설비번호"] == "EQ-04"]
        eq03 = w3[w3["설비번호"] == "EQ-03"]
        check("week03 EQ-04 8건 중 범위 밖 4건(불합격 1) · EQ-03 11건 중 범위 안 7건(강의·실습 수치)",
              len(eq04) == 8 and (~eq04["온도_C"].between(295, 305)).sum() == 4
              and ((~eq04["온도_C"].between(295, 305)) & (eq04["합격여부"] == -1)).sum() == 1
              and len(eq03) == 11 and eq03["온도_C"].between(295, 305).sum() == 7)

    w4 = validate_week("week04", "week04_process_filtering.csv",
                       ["측정시간", "로트번호", "설비번호", "공정명", "온도_C", "압력_Pa", "가스유량_slm", "합격여부"])
    if w4 is not None:
        check("week04 합격여부 값 범위", set(w4["합격여부"].unique()) <= {1, -1})
        eq02 = w4[w4["설비번호"] == "EQ-02"]
        eq01 = w4[w4["설비번호"] == "EQ-01"]
        check("week04 (100, 8), 불합격 13건(13.0%), EQ-02 25건 중 불합격 5건, EQ-01 31건 중 불합격 2건(강의·실습 수치)",
              w4.shape == (100, 8) and (w4["합격여부"] == -1).sum() == 13 and len(eq02) == 25
              and (eq02["합격여부"] == -1).sum() == 5 and len(eq01) == 31 and (eq01["합격여부"] == -1).sum() == 2)

    w5 = validate_week("week05", "week05_dirty_process_data.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_C", "압력_Pa", "가스유량_slm", "처리시간_sec", "합격여부"])
    if w5 is not None:
        check("week05 결측값 존재(의도된 패턴)", w5.isna().sum().sum() > 0)
        check("week05 중복 행 존재(의도된 패턴)", w5.duplicated().sum() > 0)
        check("week05 음수 압력 존재(의도된 이상값)", (w5["압력_Pa"] < 0).sum() > 0)

    w6 = validate_week("week06", "week06_process_visualization.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_C", "압력_Pa", "두께_nm", "진동_mm_s", "처리시간_sec", "합격여부"])
    if w6 is not None:
        vc = w6["설비번호"].value_counts().to_dict()
        sd = w6.groupby("설비번호")["온도_C"].std()
        check("week06 180행, 설비별 EQ-04 50 · EQ-01 47 · EQ-03 46 · EQ-02 37, 온도 표준편차 최대 EQ-02(강의·실습 수치)",
              len(w6) == 180 and vc == {"EQ-04": 50, "EQ-01": 47, "EQ-03": 46, "EQ-02": 37} and sd.idxmax() == "EQ-02",
              f"{vc} / {sd.round(2).to_dict()}")
        check("week06 온도-두께 강한 양의 관계(r>0.7), 온도-압력 관계 약함(|r|<0.2)",
              w6["온도_C"].corr(w6["두께_nm"]) > 0.7 and abs(w6["온도_C"].corr(w6["압력_Pa"])) < 0.2)

    w7 = validate_week("week07", "week07_equipment_yield.csv",
                        ["로트번호", "웨이퍼번호", "설비번호", "공정명", "작업조", "온도_C", "압력_Pa", "진공도_mTorr", "처리시간_sec", "불량유형", "합격여부"])
    if w7 is not None:
        rate = w7.groupby("설비번호")["합격여부"].apply(lambda s: (s == -1).mean())
        check("week07 EQ-04 불량률이 가장 높음(의도된 패턴)", rate.idxmax() == "EQ-04", str(rate.to_dict()))
        yield_by_lot = w7.groupby("로트번호")["합격여부"].apply(lambda s: (s == 1).mean())
        check("week07 저수율(80% 미만) 로트 존재(의도된 패턴)", (yield_by_lot < 0.8).sum() >= 5, str((yield_by_lot < 0.8).sum()))
        ok = w7["합격여부"] == 1
        eq = (ok.groupby(w7["설비번호"]).mean() * 100).round(1).to_dict()
        top = w7[w7["합격여부"] == -1]["불량유형"].value_counts()
        check("week07 300행, 전체 합격률 88.0%, 설비별 EQ-01 98.1 · EQ-02 86.5 · EQ-03 91.1 · EQ-04 75.0, 80% 미만 로트 21, 불량 1위 두께 불량 11(강의·실습 수치)",
              len(w7) == 300 and round(ok.mean() * 100, 1) == 88.0
              and eq == {"EQ-01": 98.1, "EQ-02": 86.5, "EQ-03": 91.1, "EQ-04": 75.0}
              and (yield_by_lot < 0.8).sum() == 21 and top.index[0] == "두께 불량" and top.iloc[0] == 11, f"{eq}")

    w8 = validate_week("week08", "week08_anomaly_root_cause.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_C", "압력_Pa", "진공도_mTorr", "두께_nm", "진동_mm_s", "냉각수온도_C", "습도_pct", "합격여부"])
    if w8 is not None:
        fail = w8["합격여부"] == -1
        vac = w8["진공도_mTorr"]
        vac_out = (vac < 4.5) | (vac > 5.5)
        tmp_out = (w8["온도_C"] < 295) | (w8["온도_C"] > 305)
        check("week08 450행, 기준선 11.1%, 온도-두께 r 0.71 · 습도-두께 r -0.01, 진공도 범위 밖 78건 25.6% · 안 8.1%(강의·실습 수치)",
              len(w8) == 450 and round(fail.mean() * 100, 1) == 11.1
              and round(w8["온도_C"].corr(w8["두께_nm"]), 2) == 0.71 and round(w8["습도_pct"].corr(w8["두께_nm"]), 2) == -0.01
              and vac_out.sum() == 78 and round(fail[vac_out].mean() * 100, 1) == 25.6 and round(fail[~vac_out].mean() * 100, 1) == 8.1)
        check("week08 반도체 확인 수치: 압력-두께 r 0.09, 온도 범위 밖 92건 불합격률 9.8% · 안 11.5%",
              round(w8["압력_Pa"].corr(w8["두께_nm"]), 2) == 0.09 and tmp_out.sum() == 92
              and round(fail[tmp_out].mean() * 100, 1) == 9.8 and round(fail[~tmp_out].mean() * 100, 1) == 11.5)

    w9train = validate_week("week09", "week09_pass_fail_train.csv",
                             ["공정명", "설비번호", "온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct", "합격여부"])
    if w9train is not None:
        check("week09_train 합격여부 값 범위(1/-1)", set(w9train["합격여부"].unique()) <= {1, -1})
        check("week09_train 결측값 존재(정제 복습용, 의도된 패턴)", w9train.isna().sum().sum() > 0)

    w9new = validate_week("week09", "week09_new_lots_to_predict.csv",
                           ["공정명", "설비번호", "온도_C", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"])
    if w9new is not None:
        check("week09_new 정답 레이블(합격여부) 미포함", "합격여부" not in w9new.columns)

    w10 = validate_week("week10", "week10_mini_project_dataset.csv",
                         ["측정시간", "로트번호", "웨이퍼번호", "설비번호", "공정명", "작업조", "온도_C", "압력_Pa",
                          "진공도_mTorr", "두께_nm", "진동_mm_s", "처리시간_sec", "냉각수온도_C", "습도_pct", "불량유형", "합격여부"])
    if w10 is not None:
        check("week10 합격여부 값 범위(1/-1)", set(w10["합격여부"].unique()) <= {1, -1})

    validate_easy()
    validate_orange_warmups()
    validate_orange_tabs()

    print("\n=== 재현성(hash) 확인: 스크립트를 다시 실행해 동일 파일인지 비교하세요 ===")
    for week in sorted(os.listdir(WEEKLY)):
        wdir = os.path.join(WEEKLY, week)
        if not os.path.isdir(wdir):
            continue
        for f in sorted(os.listdir(wdir)):
            if os.path.isfile(os.path.join(wdir, f)):
                print(f"{week}/{f}: md5={file_hash(os.path.join(wdir, f))}")
        odir = os.path.join(wdir, "orange")
        if os.path.isdir(odir):
            for f in sorted(os.listdir(odir)):
                print(f"{week}/orange/{f}: md5={file_hash(os.path.join(odir, f))}")

    total = len(RESULTS)
    passed = sum(1 for _, s, _ in RESULTS if s == "PASS")
    print(f"\n총 {total}건 중 {passed}건 통과, {total - passed}건 실패")
    return RESULTS


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")   # 출력을 파일로 돌려도 Windows 기본 인코딩(cp949) 때문에 죽지 않게
    main()
