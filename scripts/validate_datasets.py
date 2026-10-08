"""주차별 데이터 검증 스크립트.

확인 항목(스펙 14장):
- CSV가 정상적으로 열리는가 (인코딩 포함)
- 필수 열이 존재하는가
- 합격/불합격 값이 문서 설명과 일치하는가
- 주차별 의도한 결측값/이상값이 존재하는가
- 수율 계산이 올바른가 (week07)
- 데이터가 재현 가능한가 (동일 스크립트 재실행 시 동일 결과인지 해시로 확인)

실행: python scripts/validate_datasets.py
결과는 콘솔에 출력되고, 요약이 reports/validation-report.html 생성 시 사용된다.
"""
import os
import hashlib
import pandas as pd

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
                       ["주문번호", "매장", "메뉴", "종류", "가격_원", "수량_개", "평가"])
    if e4 is not None:
        check("easy04 크기 12행 x 7열", e4.shape == (12, 7), str(e4.shape))
        check("easy04 평가 값 범위(1/-1)", set(e4["평가"].unique()) <= {1, -1})
        check("easy04 조건 검색 건수(커피 5, 가격>5000 5, 별로예요 4, 가격>5000&별로예요 3)",
              (e4["종류"] == "커피").sum() == 5 and (e4["가격_원"] > 5000).sum() == 5
              and (e4["평가"] == -1).sum() == 4
              and ((e4["가격_원"] > 5000) & (e4["평가"] == -1)).sum() == 3)
        bad_rate = e4.groupby("종류")["평가"].apply(lambda s: (s == -1).mean())
        check("easy04 별로예요 비율 1위는 디저트(의도된 패턴)", bad_rate.idxmax() == "디저트", str(bad_rate.to_dict()))

    e5 = validate_week("week05", "week05_easy_class_records.csv",
                       ["이름", "반", "키_cm", "몸무게_kg", "수학_점수"])
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
                       ["날짜", "요일", "날씨", "최고기온_섭씨", "판매량_개"])
    if e6 is not None:
        check("easy06 21행", len(e6) == 21, str(len(e6)))
        try:
            d = pd.to_datetime(e6["날짜"], format="%Y-%m-%d")
            check("easy06 날짜가 YYYY-MM-DD로 변환되고 하루 간격", (d.diff().dropna() == pd.Timedelta(days=1)).all())
        except Exception as e:  # noqa: BLE001
            check("easy06 날짜가 YYYY-MM-DD로 변환되고 하루 간격", False, str(e))
        r = e6["최고기온_섭씨"].corr(e6["판매량_개"])
        check("easy06 기온-판매량 강한 양의 관계(r>0.8)", r > 0.8, f"r={r:.2f}")
        med = e6.groupby("날씨")["판매량_개"].median()
        check("easy06 비 오는 날 판매량 중앙값이 가장 낮음(박스플롯 패턴)", med.idxmin() == "비", str(med.to_dict()))

    e7 = validate_week("week07", "week07_easy_quiz_results.csv",
                       ["반", "이름", "문제번호", "풀이시간_초", "오답유형", "정답여부"])
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
                       ["날짜", "최고기온_섭씨", "습도_pct", "아이스크림_판매량_개", "핫초코_판매량_잔", "냉동고온도_섭씨", "손님평가"])
    if e8 is not None:
        check("easy08 30행", len(e8) == 30, str(len(e8)))
        check("easy08 손님평가 값 범위(1/-1)", set(e8["손님평가"].unique()) <= {1, -1})
        r_ice = e8["최고기온_섭씨"].corr(e8["아이스크림_판매량_개"])
        r_choco = e8["최고기온_섭씨"].corr(e8["핫초코_판매량_잔"])
        r_hum = e8["습도_pct"].corr(e8["아이스크림_판매량_개"])
        r_fz = e8["냉동고온도_섭씨"].corr(e8["손님평가"])
        check("easy08 기온-아이스크림 강한 양의 관계(r>0.8)", r_ice > 0.8, f"r={r_ice:.2f}")
        check("easy08 기온-핫초코 강한 음의 관계(r<-0.8)", r_choco < -0.8, f"r={r_choco:.2f}")
        check("easy08 습도-아이스크림 관계 없음(|r|<0.1)", abs(r_hum) < 0.1, f"r={r_hum:.2f}")
        fz = e8["냉동고온도_섭씨"]
        out = e8[(fz < -20) | (fz > -16)]
        inn = e8[(fz >= -20) & (fz <= -16)]
        out_rate = (out["손님평가"] == -1).mean()
        in_rate = (inn["손님평가"] == -1).mean()
        check("easy08 냉동고 범위 밖 불만률이 범위 안보다 큼(U자 패턴, 밖 8건 중 6 / 안 22건 중 2)",
              len(out) == 8 and (out["손님평가"] == -1).sum() == 6 and (inn["손님평가"] == -1).sum() == 2,
              f"밖 {out_rate:.1%}, 안 {in_rate:.1%}")
        check("easy08 냉동고-손님평가 상관계수는 0에 가까움(|r|<0.2, 상관계수가 놓치는 경우)",
              abs(r_fz) < 0.2, f"r={r_fz:.2f}")

    feature_cols = ["최고기온_섭씨", "습도_pct", "풍속_m_s", "강수량_mm"]
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


def main():
    w1 = validate_week("week01", "week01_semiconductor_process_overview.csv",
                        ["측정시간", "로트번호", "웨이퍼번호", "공정명", "설비번호", "온도_섭씨", "압력_Pa", "합격여부"])
    if w1 is not None:
        check("week01 합격여부 값 범위", set(w1["합격여부"].unique()) <= {1, -1})

    validate_week("week02", "week02_python_basics_1.csv",
                  ["로트번호", "공정명", "설비번호", "온도_섭씨", "합격여부"])

    validate_week("week03", "week03_python_basics_2.csv",
                  ["로트번호", "공정명", "설비번호", "온도_섭씨", "합격여부"])

    validate_week("week04", "week04_process_filtering.csv",
                  ["측정시간", "로트번호", "설비번호", "공정명", "온도_섭씨", "압력_Pa", "가스유량_slm", "합격여부"])

    w5 = validate_week("week05", "week05_dirty_process_data.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_섭씨", "압력_Pa", "가스유량_slm", "처리시간_sec", "합격여부"])
    if w5 is not None:
        check("week05 결측값 존재(의도된 패턴)", w5.isna().sum().sum() > 0)
        check("week05 중복 행 존재(의도된 패턴)", w5.duplicated().sum() > 0)
        check("week05 음수 압력 존재(의도된 이상값)", (w5["압력_Pa"] < 0).sum() > 0)

    w6 = validate_week("week06", "week06_process_visualization.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_섭씨", "압력_Pa", "두께_nm", "진동_mm_s", "처리시간_sec", "합격여부"])

    w7 = validate_week("week07", "week07_equipment_yield.csv",
                        ["로트번호", "웨이퍼번호", "설비번호", "공정명", "작업조", "온도_섭씨", "압력_Pa", "진공도_mTorr", "처리시간_sec", "불량유형", "합격여부"])
    if w7 is not None:
        rate = w7.groupby("설비번호")["합격여부"].apply(lambda s: (s == -1).mean())
        check("week07 EQ-04 불량률이 가장 높음(의도된 패턴)", rate.idxmax() == "EQ-04", str(rate.to_dict()))
        yield_by_lot = w7.groupby("로트번호")["합격여부"].apply(lambda s: (s == 1).mean())
        check("week07 저수율(80% 미만) 로트 존재(의도된 패턴)", (yield_by_lot < 0.8).sum() >= 5, str((yield_by_lot < 0.8).sum()))

    w8 = validate_week("week08", "week08_anomaly_root_cause.csv",
                        ["측정시간", "로트번호", "설비번호", "공정명", "온도_섭씨", "압력_Pa", "진공도_mTorr", "두께_nm", "진동_mm_s", "냉각수온도_섭씨", "습도_pct", "합격여부"])

    w9train = validate_week("week09", "week09_pass_fail_train.csv",
                             ["공정명", "설비번호", "온도_섭씨", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct", "합격여부"])
    if w9train is not None:
        check("week09_train 합격여부 값 범위(1/-1)", set(w9train["합격여부"].unique()) <= {1, -1})
        check("week09_train 결측값 존재(정제 복습용, 의도된 패턴)", w9train.isna().sum().sum() > 0)

    w9new = validate_week("week09", "week09_new_lots_to_predict.csv",
                           ["공정명", "설비번호", "온도_섭씨", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"])
    if w9new is not None:
        check("week09_new 정답 레이블(합격여부) 미포함", "합격여부" not in w9new.columns)

    w10 = validate_week("week10", "week10_mini_project_dataset.csv",
                         ["측정시간", "로트번호", "웨이퍼번호", "설비번호", "공정명", "작업조", "온도_섭씨", "압력_Pa",
                          "진공도_mTorr", "두께_nm", "진동_mm_s", "처리시간_sec", "냉각수온도_섭씨", "습도_pct", "불량유형", "합격여부"])
    if w10 is not None:
        check("week10 합격여부 값 범위(1/-1)", set(w10["합격여부"].unique()) <= {1, -1})

    validate_easy()

    print("\n=== 재현성(hash) 확인: 스크립트를 다시 실행해 동일 파일인지 비교하세요 ===")
    for week in sorted(os.listdir(WEEKLY)):
        wdir = os.path.join(WEEKLY, week)
        if not os.path.isdir(wdir):
            continue
        for f in sorted(os.listdir(wdir)):
            print(f"{week}/{f}: md5={file_hash(os.path.join(wdir, f))}")

    total = len(RESULTS)
    passed = sum(1 for _, s, _ in RESULTS if s == "PASS")
    print(f"\n총 {total}건 중 {passed}건 통과, {total - passed}건 실패")
    return RESULTS


if __name__ == "__main__":
    main()
