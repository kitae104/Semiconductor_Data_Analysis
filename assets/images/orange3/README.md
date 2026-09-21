# Orange3 화면 캡처 체크리스트

강의 페이지(5~10차시)와 부록 `docs/orange3-guide.html`의 Orange3 캡처 이미지는 모두 이 폴더에 저장한다.

## 동작 방식

- HTML에는 `<img ... data-shot="캡처할 화면 설명">` 형태로 **파일명이 미리 들어가 있다.**
- 파일이 없으면 페이지에 점선 상자(`.photo-slot`)가 뜨고 "캡처할 화면"과 "저장 위치"가 표시된다
  (`assets/js/common.js`).
- 아래 표의 **파일명 그대로** PNG를 이 폴더에 저장하면, HTML 수정 없이 새로고침만으로 이미지가 표시된다.

## 캡처 요령

- **Windows**: `Win + Shift + S` → "창 캡처" 또는 영역 선택 → 그림판 등에 붙여넣고 PNG로 저장.
  (Orange3 위젯 창만 캡처하려면 창을 클릭한 뒤 `Alt + PrtSc`도 가능)
- **Mac**: `Cmd + Shift + 4` 후 `Space` → 캡처할 창 클릭 → 바탕화면에 PNG 저장.
- 형식은 **PNG**, 파일명은 **소문자·밑줄 그대로**(대소문자가 다르면 Vercel 배포에서 이미지가 안 보인다).
- 가로 1200~1600px 정도면 충분하다. 너무 크면(2MB 이상) 줄여서 저장한다.
- 개인 정보(바탕화면 파일명, 사용자 이름이 보이는 경로 등)가 찍히지 않게 Orange3 창만 캡처한다.

## 부록: Orange3 시작하기 (`docs/orange3-guide.html`)

| 파일명 | 캡처할 화면 | 준비 |
|---|---|---|
| `guide_01_download_page.png` | 공식 다운로드 페이지 — 운영체제 탭과 설치 파일 다운로드 버튼 | https://orangedatamining.com/download/ |
| `guide_02_installer.png` | 설치 마법사 화면(Windows) — Next 버튼이 보이는 단계 | 설치 파일 실행 |
| `guide_03_first_launch.png` | 처음 실행 시 나타나는 시작 안내(Welcome) 창 | 설치 후 첫 실행 |
| `guide_04_main_screen.png` | 기본 화면 전체 — 왼쪽 위젯 목록 + 가운데 빈 캔버스 | Welcome 창에서 New |
| `guide_05_file_widget.png` | File 위젯 창 — CSV를 불러와 열 목록(Name·Type·Role)이 보이는 화면 | `data/weekly/week05/week05_dirty_process_data.csv` |
| `guide_06_link.png` | File 위젯과 Data Table 위젯이 연결선으로 이어진 캔버스 | 위와 같음 |
| `guide_07_data_table.png` | Data Table 창 — 표에 빈 칸(결측값)이 보이는 화면 | 위와 같음 |

## 5차시 — `week05_dirty_process_data.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week05_01_canvas.png` | File → Data Table → Feature Statistics 세 위젯을 연결한 캔버스 전체 |
| `week05_02_data_table.png` | Data Table 창 — 빈 칸(결측 셀)이 보이는 부분 |
| `week05_03_feature_statistics.png` | Feature Statistics 창 — 온도_섭씨의 Max 값이 500 이상으로 보이는 부분 |

## 6차시 — `week06_process_visualization.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week06_01_canvas.png` | File 하나에서 Scatter Plot·Box Plot·Distributions로 갈라진 캔버스 |
| `week06_02_scatter_plot.png` | Scatter Plot — X축 온도_섭씨, Y축 두께_nm |
| `week06_03_box_plot.png` | Box Plot — 변수 온도_섭씨, Subgroups 설비번호 |
| `week06_04_distributions.png` | Distributions — 온도_섭씨 히스토그램 |

## 7차시 — `week07_equipment_yield.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week07_01_canvas.png` | File에서 Box Plot과 Bar Chart로 갈라진 캔버스 |
| `week07_02_box_plot.png` | Box Plot — 변수 온도_섭씨, Subgroups 설비번호 |
| `week07_03_bar_chart.png` | Bar Chart — 설비번호별 합격여부 |

## 8차시 — `week08_anomaly_root_cause.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week08_01_canvas.png` | File → Correlations 캔버스 |
| `week08_02_correlations.png` | Correlations — 변수 쌍이 상관계수 크기순으로 정렬된 결과 |

## 9차시 — `week09_pass_fail_train.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week09_01_canvas.png` | File → Tree → Test and Score 캔버스(File은 Test and Score에도 연결) |
| `week09_02_file_target.png` | File 위젯 창 — 검사결과 열의 Type=categorical, Role=target으로 지정한 화면 |
| `week09_03_test_and_score.png` | Test and Score — Tree 모델의 CA(정확도)가 보이는 결과 표 |

## 10차시 — `week09_pass_fail_train.csv` + `week09_new_lots_to_predict.csv`

| 파일명 | 캡처할 화면 |
|---|---|
| `week10_01_canvas.png` | 학습용 File → Tree → Predictions, 새 로트 File → Predictions 캔버스 |
| `week10_02_predictions.png` | Predictions — 새 로트별 예측 결과와 확률 열이 보이는 표 |

## 캡처 자리 추가·변경하기

새 자리를 만들려면 HTML에 아래 블록을 넣고, 이 표에도 한 줄 추가한다(`src`는 페이지 위치 기준 상대 경로).

```html
<figure style="margin:1rem 0;">
  <img class="chart-img" src="../../assets/images/orange3/week05_04_새화면.png" loading="lazy"
       alt="그림 설명" data-shot="캡처할 화면 설명(파일이 없을 때 점선 상자에 표시)">
  <figcaption class="img-caption">그림 5-4. 그림 설명</figcaption>
</figure>
```
