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
                             ["공정명", "설비번호", "온도_섭씨", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct", "검사결과"])
    if w9train is not None:
        check("week09_train 검사결과 값 범위(0/1)", set(w9train["검사결과"].unique()) <= {0, 1})
        check("week09_train 결측값 존재(정제 복습용, 의도된 패턴)", w9train.isna().sum().sum() > 0)

    w9new = validate_week("week09", "week09_new_lots_to_predict.csv",
                           ["공정명", "설비번호", "온도_섭씨", "압력_Pa", "가스유량_slm", "두께_nm", "진공도_mTorr", "습도_pct"])
    if w9new is not None:
        check("week09_new 정답 레이블(검사결과) 미포함", "검사결과" not in w9new.columns)

    w10 = validate_week("week10", "week10_mini_project_dataset.csv",
                         ["측정시간", "로트번호", "웨이퍼번호", "설비번호", "공정명", "작업조", "온도_섭씨", "압력_Pa",
                          "진공도_mTorr", "두께_nm", "진동_mm_s", "처리시간_sec", "냉각수온도_섭씨", "습도_pct", "불량유형", "검사결과"])
    if w10 is not None:
        check("week10 검사결과 값 범위(0/1)", set(w10["검사결과"].unique()) <= {0, 1})

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
