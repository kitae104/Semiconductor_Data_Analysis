# 화면 캡처 체크리스트 (v3)

강의(1~10차시 `index.html`·`worksheet.html`), 수강 전 준비(`docs/setup.html`), 부록(`docs/orange3-guide.html`)에 들어갈
Orange3·Jupyter 화면 캡처 목록이다. Orange 화면은 이 폴더(`assets/images/orange3/`)에, 설치 안내 화면은
`assets/images/setup/`에 저장한다. 표의 "파일" 열이 저장할 경로 그대로다.

> 이 목록은 2026-10-24 기준으로 각 페이지의 `<img data-shot="…">`를 모두 모은 것이다. 8~10차시는 수정이 이어지고 있을 수 있으니,
> 캡처 직전에 그 페이지를 다시 확인한다. 같은 목록이 `_workspace/09_capture_list.md`에도 있다.

## 동작 방식

- HTML에는 `<img ... data-shot="캡처할 화면 설명">` 형태로 **파일 경로가 미리 들어가 있다.**
- 파일이 없으면 페이지에 점선 상자(`.photo-slot`)가 뜨고 "캡처 예정 — 화면 설명"과 저장 경로가 표시된다
  (`assets/js/common.js`).
- 아래 표의 **파일 경로 그대로** PNG를 저장하면, HTML 수정 없이 새로고침만으로 이미지가 표시된다.
- 정합성 검사(`check_course_consistency.py`)는 파일이 없는 캡처 자리를 실패가 아니라 "캡처 대기" 경고로 표시한다.
- 한 파일이 강의 앞쪽(오늘의 미션)과 PART 2에 두 번 쓰이는 경우가 있다. 표에는 자리마다 한 줄씩 적었고, 요약표의
  "서로 다른 파일" 열이 실제로 찍을 장 수다.

## 캡처 요령

- **Orange 3.35**에서 찍는다. 키트를 새로 풀어 `_start.ows`/`_done.ows`를 열고, 화면 설명에 적힌 위젯 설정(Split by, 조건 값,
  정렬 등)을 그대로 맞춘다. 설명에 숫자가 적혀 있으면 화면 숫자가 같은지 확인하고, 다르면 찍지 말고 알린다
  (저장된 위젯 설정이 새 위젯에 적용됐을 수 있다 — Orange를 새 설정으로 띄우거나 `_done.ows`를 다시 연다).
- **Windows**: `Win + Shift + S` → "창 캡처" 또는 영역 선택 → 그림판 등에 붙여넣고 PNG로 저장.
  (Orange3 위젯 창만 캡처하려면 창을 클릭한 뒤 `Alt + PrtSc`도 가능)
- **Mac**: `Cmd + Shift + 4` 후 `Space` → 캡처할 창 클릭 → 바탕화면에 PNG 저장.
- 형식은 **PNG**, 파일명은 **소문자·밑줄 그대로**(대소문자가 다르면 배포 사이트에서 이미지가 안 보인다).
- 가로 1200~1600px 정도면 충분하다. 너무 크면(2MB 이상) 줄여서 저장한다.
- 개인 정보(바탕화면 파일명, 사용자 이름이 보이는 경로 등)가 찍히지 않게 필요한 창만 캡처한다.

## 요약 — 구역별 캡처 수

| 구역 | 캡처 자리 | 서로 다른 파일 | 파일 있음 | 캡처 필요 |
| --- | --- | --- | --- | --- |
| 1차시 | 9 | 8 | 0 | 8 |
| 2차시 | 6 | 5 | 0 | 5 |
| 3차시 | 8 | 7 | 0 | 7 |
| 4차시 | 6 | 6 | 0 | 6 |
| 5차시 | 10 | 10 | 0 | 10 |
| 6차시 | 8 | 8 | 0 | 8 |
| 7차시 | 7 | 7 | 0 | 7 |
| 8차시 | 7 | 7 | 0 | 7 |
| 9차시 | 8 | 8 | 0 | 8 |
| 10차시 | 6 | 6 | 0 | 6 |
| 수강 전 준비 (`docs/setup.html`) | 6 | 6 | 0 | 6 |
| 부록 Orange3 시작하기 (`docs/orange3-guide.html`) | 4 | 4 | 2 | 2 |
| **합계** | 85 | 82 | 2 | 80 |

## 1차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week01_07_process_distributions.png` | `lectures/week01/index.html`:70 | 오늘 끝에 Orange에서 보게 될 화면 — 공장 기록표의 합격(1)·불합격(-1) 막대 두 개. 막대 높이가 미션의 답이다 | **없음** |
| 2 | `assets/images/orange3/week01_01_town_start_canvas.png` | `lectures/week01/index.html`:480 | Orange 화면 — 시작 파일(week01_1_town_start.ows)을 열면 가운데 캔버스에 File 위젯 하나와 안내 메모가 보인다 | **없음** |
| 3 | `assets/images/orange3/week01_02_town_file.png` | `lectures/week01/index.html`:484 | File 위젯 창 — 위에 파일 이름, 아래에 열 다섯 개(구·동·인구_count·면적_km2·주요연령대)가 보이면 데이터가 들어온 것이다 | **없음** |
| 4 | `assets/images/orange3/week01_03_town_data_table.png` | `lectures/week01/index.html`:488 | Data Table 창 — 왼쪽 Info 칸에 '30 instances', '4 features', '1 meta attribute'가 보이고 오른쪽에 동네 표가 펼쳐진다 | **없음** |
| 5 | `assets/images/orange3/week01_04_town_distributions.png` | `lectures/week01/index.html`:496 | Distributions 창 — 주요연령대 막대 네 개. 가장 높은 막대(40~50대)에 마우스를 올리면 툴팁에 개수가 뜬다 | **없음** |
| 6 | `assets/images/orange3/week01_05_town_split_by_gu.png` | `lectures/week01/index.html`:504 | Split by를 구로 바꾼 Distributions 창 — 20~30대 막대 안에서 새빛구 색이 가장 큰 부분을 차지한다 | **없음** |
| 7 | `assets/images/orange3/week01_06_process_data_table.png` | `lectures/week01/index.html`:517 | 공장 기록표의 Data Table 창 — 왼쪽 Info 칸에 '40 instances', '4 features', 'Target with 2 values', '3 meta attributes'가 보인다 | **없음** |
| 8 | `assets/images/orange3/week01_07_process_distributions.png` | `lectures/week01/index.html`:528 | 공장 기록표의 Distributions 창 — 합격(1)·불합격(-1) 막대 두 개. 불합격 막대에 마우스를 올리면 툴팁에 개수와 비율이 뜬다 | **없음** |
| 9 | `assets/images/orange3/week01_08_process_split_by_process.png` | `lectures/week01/index.html`:536 | Split by를 공정명으로 바꾼 화면 — 불합격(-1) 막대에 마우스를 올리면 툴팁 표에 공정마다 개수가 뜬다. 세정이 가장 많다 | **없음** |

## 2차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week02_04_temps_data_table_by_equipment.png` | `lectures/week02/index.html`:70 | week02_2_temps_done.ows의 Data Table (표 보기) 창 — 설비번호 열 머리를 한 번 눌러 정렬한 상태. EQ-01 1행, EQ-02 4행, EQ-03 7행, EQ-04 8행이 차례로 모여 보이고, 왼쪽 Info 칸의 20 instances가 보이게 | **없음** |
| 2 | `assets/images/orange3/week02_01_subway_start_canvas.png` | `lectures/week02/index.html`:467 | week02_1_subway_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 ①~③ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week02_02_subway_feature_statistics.png` | `lectures/week02/index.html`:471 | week02_1_subway_done.ows의 Feature Statistics (열 통계) 창 — 승차인원_count 행의 Mean 2876.58, Median 2632, Min. 314, Max. 9872가 한 줄에 보이게(하차인원_count 행도 함께) | **없음** |
| 4 | `assets/images/orange3/week02_03_subway_data_table_sorted.png` | `lectures/week02/index.html`:479 | week02_1_subway_done.ows의 Data Table (표 보기) 창 — 승차인원_count 열이 큰 값부터 정렬되어 맨 위 행 중앙역 · 1호선 · 출근 · 9872와 그 아래 강변역 · 출근 · 4000, 시장역 · 낮 · 3969가 보이게 | **없음** |
| 5 | `assets/images/orange3/week02_05_temps_feature_statistics.png` | `lectures/week02/index.html`:491 | week02_2_temps_done.ows의 Feature Statistics (열 통계) 창 — 온도_C 행의 Mean 303.8, Median 303.6, Min. 292.2, Max. 317.9, Missing 0이 한 줄에 보이고, 위아래에 공정명·설비번호(글자 열, Mean 칸 빈칸) 행도 보이게 | **없음** |
| 6 | `assets/images/orange3/week02_04_temps_data_table_by_equipment.png` | `lectures/week02/index.html`:499 | week02_2_temps_done.ows의 Data Table (표 보기) 창 — 설비번호 열 머리를 한 번 눌러 정렬한 상태. EQ-01 1행, EQ-02 4행, EQ-03 7행, EQ-04 8행이 차례로 모여 보이고, 왼쪽 Info 칸의 20 instances가 보이게 | **없음** |

## 3차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week03_06_records_select_rows_eq04.png` | `lectures/week03/index.html`:64 | PART 2에서 만들 Select Rows (행 고르기) 창 — 조건 두 줄 '설비번호 is EQ-04', '온도_C is outside 295, 305' | **없음** |
| 2 | `assets/images/orange3/week03_01_air_start_canvas.png` | `lectures/week03/index.html`:515 | week03_1_air_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 ①~④ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week03_02_air_select_rows.png` | `lectures/week03/index.html`:519 | week03_1_air_done.ows의 Select Rows (행 고르기) 창 — Conditions 칸에 'PM10_ug_m3 · is greater than · 80' 한 줄과 아래 Add Condition 버튼이 보이게 | **없음** |
| 4 | `assets/images/orange3/week03_03_air_data_table.png` | `lectures/week03/index.html`:523 | week03_1_air_done.ows에서 Select Rows 뒤 Data Table (표 보기) 창 — 왼쪽 Info 칸의 행 수와 오른쪽 표의 등급 열이 함께 보이게 | **없음** |
| 5 | `assets/images/orange3/week03_04_air_two_conditions.png` | `lectures/week03/index.html`:531 | week03_1_air_done.ows의 Select Rows 창에 조건 두 줄(PM10_ug_m3 is greater than 80, 습도_pct is greater than 70)을 건 상태와, 그 뒤 Data Table을 나란히 | **없음** |
| 6 | `assets/images/orange3/week03_05_air_distributions.png` | `lectures/week03/index.html`:539 | week03_1_air_done.ows의 Distributions (분포 막대) 창 — Variable 등급, Split by None. 막대 네 개(나쁨 · 매우나쁨 · 보통 · 좋음)가 가나다순으로 놓인 모습 | **없음** |
| 7 | `assets/images/orange3/week03_06_records_select_rows_eq04.png` | `lectures/week03/index.html`:555 | week03_2_records_start.ows에 Select Rows를 이어 조건 두 줄('설비번호 · is · EQ-04', '온도_C · is outside · 295 and 305')을 건 Select Rows (행 고르기) 창 | **없음** |
| 8 | `assets/images/orange3/week03_07_records_data_table_eq04.png` | `lectures/week03/index.html`:558 | 위 Select Rows 뒤 Data Table (표 보기) 창 — 왼쪽 Info 칸의 행 수와, 오른쪽 표 4행(LOT-0141 314.1 · LOT-0034 318.4 · LOT-0197 291.0 · LOT-0085 307.0)과 합격여부 열(1, 1, 1, -1)이 보이게 | **없음** |

## 4차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week04_01_flow_table_all.png` | `lectures/week04/index.html`:41 | week04_1_flow_start.ows의 File에 Data Table을 이어 연 창 — 공정 흐름표 8행 전체(공정순서 1~8)와 반복여부 열이 보이게 | **없음** |
| 2 | `assets/images/orange3/week04_02_flow_start_canvas.png` | `lectures/week04/index.html`:465 | week04_1_flow_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 위쪽 ①~④ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week04_03_flow_select_columns.png` | `lectures/week04/index.html`:471 | week04_1_flow_done.ows의 Select Columns (열 고르기) 창 — 왼쪽 Ignored에 구분·측정단위·주요설비·대표측정값, 오른쪽 Features에 공정순서·공정명·반복여부, Metas에 하는일·생활비유가 보이게 | **없음** |
| 4 | `assets/images/orange3/week04_04_flow_data_table.png` | `lectures/week04/index.html`:476 | week04_1_flow_done.ows의 Select Rows 뒤 Data Table (표 보기) 창 — 왼쪽 Info 칸의 행 수와, 공정순서 오름차순으로 놓은 표(하는일·생활비유 열 포함)가 보이게 | **없음** |
| 5 | `assets/images/orange3/week04_05_filtering_select_columns.png` | `lectures/week04/index.html`:503 | week04_2_filtering_done.ows의 Select Columns (열 고르기) 창 — 왼쪽 Ignored에 측정시간·로트번호·공정명·압력_Pa·가스유량_slm, 오른쪽 Features에 설비번호·온도_C, Target에 합격여부가 보이게 | **없음** |
| 6 | `assets/images/orange3/week04_06_filtering_eq01_rows.png` | `lectures/week04/index.html`:508 | week04_2_filtering_start.ows에 Select Columns → Select Rows → Data Table을 이은 상태에서, Select Rows (행 고르기) 창의 조건 두 줄(설비번호 is EQ-01, 합격여부 is -1)과 Data Table (표 보기) 창(왼쪽 Info 행 수 2, 온도_C 큰 값부터 303.0 · 301.2)을 나란히 | **없음** |

## 5차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week05_01_mission_before_after.png` | `lectures/week05/index.html`:41 | week05_2_dirty_process_done.ows에서 Feature Statistics (정리 전) 창과 Feature Statistics (정리 후) 창을 나란히 띄운 화면 — 두 창 모두 온도_C 행의 Mean(정리 전 304.94, 정리 후 300.75)이 보이게 | **없음** |
| 2 | `assets/images/orange3/week05_02_cleanroom_start.png` | `lectures/week05/index.html`:376 | week05_1_cleanroom_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 위쪽 ①~④ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week05_03_cleanroom_stats_before.png` | `lectures/week05/index.html`:437 | week05_1_cleanroom_done.ows의 Feature Statistics (정리 전) 창 — 파티클_count_per_m3 행의 Max 99999와 Missing 4, 습도_pct 행 Missing 3, 차압_Pa 행 Min -5.0과 Missing 2가 보이게 | **없음** |
| 4 | `assets/images/orange3/week05_04_cleanroom_filled_table.png` | `lectures/week05/index.html`:443 | week05_1_cleanroom_done.ows의 Data Table (채운 뒤) 창 — 파티클_count_per_m3 열에서 2543.66으로 채워진 칸 하나 이상이, 위아래 행의 1,000 안팎 값과 함께 보이게 | **없음** |
| 5 | `assets/images/orange3/week05_05_cleanroom_stats_after.png` | `lectures/week05/index.html`:454 | week05_1_cleanroom_done.ows의 Feature Statistics (정리 후) 창 — 파티클_count_per_m3 행의 Mean 1180.0과 Max 2543.66이 보이고, 창 아래 상태 표시줄에 들어온 행 수 70이 보이게 | **없음** |
| 6 | `assets/images/orange3/week05_06_process_stats_before.png` | `lectures/week05/index.html`:466 | week05_2_dirty_process_done.ows의 Feature Statistics (정리 전) 창 — 온도_C 행의 Missing 3과 Max 557.73, 압력_Pa 행 Min -42.91, 가스유량_slm 행 Min -5와 Max 250이 보이게 | **없음** |
| 7 | `assets/images/orange3/week05_07_process_impute.png` | `lectures/week05/index.html`:472 | week05_2_dirty_process_done.ows의 Impute (빈칸 채우기) 창 — 위쪽 Default Method가 Average/Most frequent이고, 아래쪽 Individual Attribute Settings의 왼쪽 열 목록에서 합격여부를 고른 채 오른쪽 버튼 Remove instances with unknown values가 선택된 상태 | **없음** |
| 8 | `assets/images/orange3/week05_08_process_select_rows.png` | `lectures/week05/index.html`:477 | week05_2_dirty_process_done.ows의 Select Rows (행 고르기) 창 — 조건 네 줄(온도_C is at most 400, 압력_Pa is at least 0, 가스유량_slm is at least 0, 가스유량_slm is below 200)이 모두 보이게 | **없음** |
| 9 | `assets/images/orange3/week05_09_process_table_after.png` | `lectures/week05/index.html`:482 | week05_2_dirty_process_done.ows의 Data Table (정리 결과) 창 — 왼쪽 Info 칸의 행 수 105가 보이게 | **없음** |
| 10 | `assets/images/orange3/week05_10_process_stats_after.png` | `lectures/week05/index.html`:485 | week05_2_dirty_process_done.ows의 Feature Statistics (정리 후) 창 — 온도_C 행의 Mean 300.75(또는 300.7), Min 291.3, Max 310.9가 보이게 | **없음** |

## 6차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week06_01_mission_wafer_map.png` | `lectures/week06/index.html`:41 | week06_1_wafermap_done.ows의 Scatter Plot (산점도) 창 — Axis x 다이_X, Axis y 다이_Y, Color는 (Same color)로 바꿔 모든 점을 한 색으로. 점 317개가 둥근 웨이퍼 모양으로 보이고 합격·불합격 색은 보이지 않게(창을 정사각형에 가깝게 맞춰 원이 납작해 보이지 않게) | **없음** |
| 2 | `assets/images/orange3/week06_02_wafermap_start.png` | `lectures/week06/index.html`:434 | week06_1_wafermap_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 ①~④ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week06_03_wafer_scatter.png` | `lectures/week06/index.html`:445 | week06_1_wafermap_done.ows의 Scatter Plot (산점도) 창 전체 — 왼쪽 설정 칸의 Axis x 다이_X, Axis y 다이_Y, Color 합격여부와 오른쪽 그림(둥근 웨이퍼, 가장자리 빨간 점)이 함께 보이게 | **없음** |
| 4 | `assets/images/orange3/week06_04_wafer_box.png` | `lectures/week06/index.html`:454 | week06_1_wafermap_done.ows의 Box Plot (상자 그림) 창 — Variable 중심거리_mm, Subgroups 합격여부. 상자 두 개(1, -1)와 상자 아래 숫자(1: 62.6 · 88.5 · 112.0 / -1: 119.2 · 126.8 · 132.8)가 보이게 | **없음** |
| 5 | `assets/images/orange3/week06_05_wafer_distributions.png` | `lectures/week06/index.html`:461 | week06_1_wafermap_done.ows의 Distributions (분포 막대) 창 — Variable 중심거리_mm, Split by 합격여부. 오른쪽(먼 거리) 막대에 빨간 불합격 부분이 커지는 모습이 보이게 | **없음** |
| 6 | `assets/images/orange3/week06_06_process_distributions.png` | `lectures/week06/index.html`:470 | week06_2_process_done.ows의 Distributions (분포 막대) 창 — Variable 온도_C, Split by None. 온도 막대 전체 모양이 보이게 | **없음** |
| 7 | `assets/images/orange3/week06_07_process_scatter.png` | `lectures/week06/index.html`:477 | week06_2_process_done.ows의 Scatter Plot (산점도) 창 전체 — 왼쪽 Axis x 온도_C, Axis y 두께_nm, Color 합격여부와 오른쪽 점 180개가 보이게 | **없음** |
| 8 | `assets/images/orange3/week06_08_process_box.png` | `lectures/week06/worksheet.html`:127 | week06_2_process_done.ows의 Box Plot (상자 그림) 창 — Variable 온도_C, Subgroups 설비번호. 상자 네 개와 위아래 숫자가 보이고, EQ-02 상자(300.6 · 303.4 · 307.3, 위 EQ-02: 303.735 ± 5.30)가 가장 긴 모습이 보이게 | **없음** |

## 7차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week07_01_mission_etch3_wafermap.png` | `lectures/week07/index.html`:41 | week07_1_waferlots_done.ows의 Scatter Plot 창(오른쪽 그림만, 창 제목·왼쪽 설정 칸은 잘라 낸다) — 설비 한 대의 웨이퍼 4장, Axis x 다이_X, Axis y 다이_Y, Color 합격여부. 둥근 웨이퍼 모양 점들이 보이게(창을 정사각형에 가깝게 맞춰 원이 납작해 보이지 않게) | **없음** |
| 2 | `assets/images/orange3/week07_02_waferlots_start.png` | `lectures/week07/index.html`:424 | week07_1_waferlots_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 ①~④ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week07_03_waferlots_pivot.png` | `lectures/week07/index.html`:430 | week07_1_waferlots_done.ows의 Pivot Table (피벗 표) 창 전체 — 왼쪽 Rows 설비번호, Columns 합격여부, Aggregations Count 체크와 오른쪽 표(설비 3줄 + Total 줄, 1 / -1 / Total 칸)가 함께 보이게 | **없음** |
| 4 | `assets/images/orange3/week07_04_etch3_select_rows.png` | `lectures/week07/index.html`:442 | week07_1_waferlots_done.ows의 Select Rows (식각-3만) 창 — 조건 한 줄(설비번호 is 식각-3)과 창 아래 상태 표시줄의 행 수(3804 → 1268)가 보이게 | **없음** |
| 5 | `assets/images/orange3/week07_05_etch3_scatter.png` | `lectures/week07/index.html`:447 | week07_1_waferlots_done.ows의 Scatter Plot (웨이퍼 맵) 창 전체 — 왼쪽 설정 칸의 Axis x 다이_X, Axis y 다이_Y, Color 합격여부와 오른쪽 그림(둥근 웨이퍼, 가장자리 고리의 빨간 점)이 함께 보이게 | **없음** |
| 6 | `assets/images/orange3/week07_06_yield_boxplot.png` | `lectures/week07/index.html`:471 | week07_2_yield_done.ows의 Box Plot (상자 그림) 창 — Variable 온도_C, Subgroups 설비번호. 상자 네 개(EQ-01 298.40~301.65, EQ-02 295.85~304.70, EQ-03 296.55~301.30, EQ-04 298.80~304.60)와 상자 아래 숫자가 보이게 | **없음** |
| 7 | `assets/images/orange3/week07_07_yield_pivot.png` | `lectures/week07/worksheet.html`:138 | week07_2_yield_done.ows의 Pivot Table (피벗 표) 창 전체 — 왼쪽 Rows 설비번호, Columns 합격여부, Aggregations Count 체크와 오른쪽 표(EQ-01 102.0 / 2.0 / 104.0, EQ-02 45.0 / 7.0 / 52.0, EQ-03 51.0 / 5.0 / 56.0, EQ-04 66.0 / 22.0 / 88.0, Total 264.0 / 36.0 / 300.0)가 함께 보이게 | **없음** |

## 8차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week08_01_mission_anomaly_scatter.png` | `lectures/week08/index.html`:52 | week08_2_anomaly_done.ows의 Scatter Plot (산점도) 창의 그림 부분 — Axis x 온도_C, Axis y 두께_nm, Color 합격여부로 고른 산점도 전체가 보이게 | **없음** |
| 2 | `assets/images/orange3/week08_02_chamber_start.png` | `lectures/week08/index.html`:487 | week08_1_chamber_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 위쪽 ①~③ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week08_03_chamber_correlations.png` | `lectures/week08/index.html`:493 | week08_1_chamber_done.ows의 Correlations (상관 순위) 창 전체 — 위쪽 Pearson correlation과 (All combinations), 목록 위쪽 다섯 줄이 보이게 | **없음** |
| 4 | `assets/images/orange3/week08_04_chamber_scatter.png` | `lectures/week08/index.html`:507 | week08_1_chamber_done.ows의 Scatter Plot (산점도) 창 전체 — 왼쪽 Axis x RF파워_W, Axis y 식각률_nm_min과 오른쪽 그림이 함께 보이게 | **없음** |
| 5 | `assets/images/orange3/week08_05_anomaly_scatter.png` | `lectures/week08/index.html`:521 | week08_2_anomaly_done.ows의 Scatter Plot (산점도) 창 전체 — 왼쪽 Axis x 온도_C, Axis y 두께_nm, Color 합격여부와 오른쪽 그림이 함께 보이게 | **없음** |
| 6 | `assets/images/orange3/week08_06_anomaly_projections.png` | `lectures/week08/index.html`:529 | week08_2_anomaly_done.ows의 Scatter Plot에서 Find Informative Projections 창을 열고 Start를 누른 뒤 — 목록 위쪽 다섯 줄이 보이게 | **없음** |
| 7 | `assets/images/orange3/week08_07_anomaly_correlations.png` | `lectures/week08/worksheet.html`:135 | week08_2_anomaly_done.ows의 Correlations (상관 순위) 창 전체 — 맨 위 Pearson correlation과 (All combinations), 목록 위쪽 다섯 줄이 보이게 | **없음** |

## 9차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week09_01_mission_score_vs_baseline.png` | `lectures/week09/index.html`:41 | week09_2_passfail_done.ows의 Distributions (분포 막대) 창과 Test and Score (평가) 창을 나란히 띄운 화면 — 왼쪽은 합격여부 막대 두 개(Split by None), 오른쪽은 Tree 한 줄과 CA 열이 보이게 | **없음** |
| 2 | `assets/images/orange3/week09_02_patterns_start.png` | `lectures/week09/index.html`:257 | week09_1_patterns_start.ows를 연 캔버스 전체 — File (파일 불러오기) 위젯 하나와 위쪽 ①~⑤ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week09_03_patterns_tree_viewer.png` | `lectures/week09/index.html`:277 | week09_1_patterns_done.ows의 Tree Viewer (트리 보기) 창 전체 — 왼쪽 Show details in non-leaves에 체크한 상태로, 뿌리 상자와 그 아래 두 갈래, 그리고 가장자리불량비율_pct > 35.3 쪽의 '가장자리형 100%, 40/40' 상자가 함께 보이게(Zoom으로 줄여서) | **없음** |
| 4 | `assets/images/orange3/week09_04_patterns_confusion.png` | `lectures/week09/index.html`:294 | week09_1_patterns_done.ows의 Confusion Matrix (헷갈림 표) 창 전체 — 왼쪽 Learners의 Tree, Show: Number of instances, 표의 네 줄(정상 119·1·0·0 / 중심형 4·33·0·3 / 가장자리형 0·0·40·0 / 스크래치형 4·1·1·34)이 보이게 | **없음** |
| 5 | `assets/images/orange3/week09_05_passfail_distributions.png` | `lectures/week09/index.html`:325 | week09_2_passfail_done.ows의 Distributions (분포 막대) 창 전체 — 왼쪽 Variable 합격여부, Split by None, 오른쪽 막대 두 개(1 = 595, -1 = 155)가 보이게 | **없음** |
| 6 | `assets/images/orange3/week09_06_passfail_tree_viewer.png` | `lectures/week09/index.html`:338 | week09_2_passfail_done.ows의 Tree Viewer (트리 보기) 창 — Show details in non-leaves에 체크한 상태로, 뿌리 상자(1 · 79.3%, 595/750 · 온도_C)와 바로 아래 두 갈래(≤ 293.8: -1 · 56.0%, 42/75 / > 293.8: 1 · 83.2%, 561/674), 그 아래 > 306.0 상자(1 · 53.8%, 43/80)가 보이게 | **없음** |
| 7 | `assets/images/orange3/week09_07_patterns_root_and_score.png` | `lectures/week09/worksheet.html`:113 | week09_1_patterns_done.ows의 Tree Viewer (트리 보기) 뿌리 부분(Show details in non-leaves 체크, 정상 · 50.0%, 120/240 · 불량다이수_count, 아래 선의 ≤ 11 / > 11)과 Test and Score (평가) 창(Number of folds 10, Tree 줄 CA 0.942)을 나란히 | **없음** |
| 8 | `assets/images/orange3/week09_08_passfail_score_confusion.png` | `lectures/week09/worksheet.html`:147 | week09_2_passfail_done.ows의 Test and Score (평가) 창(Number of folds 10, Tree 줄 CA 0.783)과 Confusion Matrix (헷갈림 표) 창(Actual 1 줄 546 · 49, Actual -1 줄 114 · 41)을 나란히 | **없음** |

## 10차시

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/week10_01_mission_canvas.png` | `lectures/week10/index.html`:42 | week10_2_newlots_done.ows를 연 캔버스 전체 — 위 File (학습: 공정 기록 750행)에서 Tree·kNN·Logistic Regression을 거쳐 Test and Score → Confusion Matrix로, 아래 File (새 로트 9개)에서 Predictions로 이어진 선이 모두 보이게(위젯 창은 열지 않은 상태) | **없음** |
| 2 | `assets/images/orange3/week10_02_newwafers_start.png` | `lectures/week10/index.html`:168 | week10_1_newwafers_start.ows를 연 캔버스 전체 — 위 File (학습: 웨이퍼 240장), 아래 File (새 웨이퍼 10장) 두 위젯과 ①~⑤ 안내 메모가 보이게 | **없음** |
| 3 | `assets/images/orange3/week10_03_newwafers_test_and_score.png` | `lectures/week10/index.html`:176 | week10_1_newwafers_done.ows의 Test and Score (평가) 창 — 왼쪽 Number of folds 10, 오른쪽 표에 Tree·kNN·Logistic Regression 세 줄의 CA(0.942·0.900·0.971)가 보이게 | **없음** |
| 4 | `assets/images/orange3/week10_04_newwafers_predictions.png` | `lectures/week10/index.html`:188 | week10_1_newwafers_done.ows의 Predictions (예측) 창 — Show probabilities for를 Classes known to the model로 바꾼 상태. 웨이퍼 10줄과 Tree·kNN·Logistic Regression 세 열이 보이고, N-04와 N-10 줄의 답이 모델마다 다른 것이 보이게 | **없음** |
| 5 | `assets/images/orange3/week10_05_newlots_test_and_score.png` | `lectures/week10/index.html`:221 | week10_2_newlots_done.ows의 Test and Score (평가) 창 — 왼쪽 Number of folds 10, 오른쪽 표에 Tree·kNN·Logistic Regression 세 줄의 CA(0.783·0.769·0.793)가 보이게 | **없음** |
| 6 | `assets/images/orange3/week10_06_newlots_confusion_lr.png` | `lectures/week10/index.html`:238 | week10_2_newlots_done.ows의 Confusion Matrix (헷갈림 표) 창 — 왼쪽 목록에서 Logistic Regression (로지스틱 회귀)을 고른 상태. 실제 1 행 595 · 0, 실제 -1 행 155 · 0, 예측 -1 열 합계 0이 보이게 | **없음** |

## 수강 전 준비 (`docs/setup.html`)

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/setup/setup_01_python_path.png` | `docs/setup.html`:68 | 파이썬 설치 첫 화면 — 아래쪽 'Add python.exe to PATH' 체크 상자에 체크하고 Install Now를 누르기 직전 | **없음** |
| 2 | `assets/images/setup/setup_02_orange_first_run.png` | `docs/setup.html`:111 | Orange3 첫 실행 화면 — 시작 안내 창(Welcome)이 떠 있는 상태 또는 왼쪽 위젯 목록과 빈 캔버스 | **없음** |
| 3 | `assets/images/setup/setup_03_kit_folders.png` | `docs/setup.html`:143 | 파일 탐색기 — 압축을 푼 semiconductor_kit 폴더 안에 data, notebooks, orange3 폴더와 README_학생용.txt가 보이는 화면 | **없음** |
| 4 | `assets/images/setup/setup_04_jupyter_week01.png` | `docs/setup.html`:169 | Jupyter 화면 — week01_student.ipynb를 열고 첫 셀을 실행해 '파이썬 준비 완료!'가 출력된 모습 | **없음** |
| 5 | `assets/images/setup/setup_05_ows_open.png` | `docs/setup.html`:185 | Orange — week01_1_town_start.ows를 연 캔버스(File 위젯 1개와 안내 메모)와, File 위젯을 더블클릭해 데이터 30행이 들어온 창 | **없음** |
| 6 | `assets/images/setup/setup_06_file_not_found.png` | `docs/setup.html`:202 | Orange File 위젯 창 — 파일 이름이 빨간색이고 'File not found' 오류가 보이는 화면, 폴더 아이콘 위치 표시 | **없음** |

## 부록 Orange3 시작하기 (`docs/orange3-guide.html`)

| # | 파일 | 페이지(줄) | 캡처할 화면(`data-shot`) | 있음? |
| --- | --- | --- | --- | --- |
| 1 | `assets/images/orange3/guide_01_main_screen.png` | `docs/orange3-guide.html`:216 | Orange3 기본 화면 전체 — 왼쪽 위젯 목록과 가운데 빈 캔버스가 보이는 창 | 있음 |
| 2 | `assets/images/orange3/guide_02_file_widget.png` | `docs/orange3-guide.html`:269 | File 위젯 창 — data/weekly/week05/orange/week05_dirty_process_data.tab을 불러와 열 목록(Name·Type·Role)이 보이고, 합격여부의 Role이 target인 화면 | 있음 · **재캡처 필요**(현재 캡처는 예전 CSV — `온도_섭씨`, 합격여부 numeric. `.tab`을 연 화면으로) |
| 3 | `assets/images/orange3/guide_03_link.png` | `docs/orange3-guide.html`:291 | 캔버스 — File 위젯과 Data Table 위젯이 연결선(Data)으로 이어진 모습 | 있음 |
| 4 | `assets/images/orange3/guide_04_data_table.png` | `docs/orange3-guide.html`:301 | Data Table 창 — week05_dirty_process_data.tab 내용이 표로 보이고 빈 칸(결측값)이 있는 화면 | 있음 · 재캡처 권장(현재 캡처는 예전 CSV를 연 화면) |

## 미사용 PNG (어느 페이지도 참조하지 않음)

v3 재작성 전(v2) 5~10차시 캡처다. 지금 강의·부록 어디에서도 쓰지 않는다. **미사용(삭제 가능)** — 지우지 않고 남겨 두었다.

| 파일 | 상태 |
| --- | --- |
| `assets/images/orange3/week05_01_canvas.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week05_02_data_table.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week05_03_feature_statistics.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week06_01_canvas.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week06_02_scatter_plot.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week06_03_box_plot.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week06_04_distributions.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week07_01_canvas.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week07_02_box_plot.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week07_03_distributions.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week08_01_canvas.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week08_02_correlations.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week09_01_canvas.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week09_03_test_and_score.png` | 미사용(삭제 가능) |
| `assets/images/orange3/week10_01_canvas.png` | 미사용(삭제 가능) |

## 캡처 자리 추가·변경하기

새 자리를 만들려면 HTML에 아래 블록을 넣고, 이 표에도 한 줄 추가한다(`src`는 페이지 위치 기준 상대 경로).

```html
<figure style="margin:1rem 0;">
  <img class="chart-img" src="../../assets/images/orange3/week05_11_새화면.png" loading="lazy"
       alt="그림 설명" data-shot="캡처할 화면 설명(파일이 없을 때 점선 상자에 표시)">
  <figcaption class="img-caption">그림 설명</figcaption>
</figure>
```
