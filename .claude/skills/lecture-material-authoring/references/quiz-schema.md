# quiz.json 스키마와 작성 기준

`lectures/weekXX/quiz.json`의 구조. 검사 스크립트가 타입별 필수 키와 인덱스 범위를 확인하므로,
여기서 벗어나면 FAIL이다.

## 최상위 구조

```json
{
  "week": 4,
  "title": "Pandas 가장 기본적인 부분",
  "questions": [ ... ]
}
```

| 키 | 타입 | 규칙 |
|---|---|---|
| `week` | 숫자 | 폴더 번호와 **일치해야 한다**(`week04/` → `4`). 문자열이 아니다 |
| `title` | 문자열 | 차시 제목. 강의 자료 `<h1>`과 같게 쓴다 |
| `questions` | 배열 | **8개 이상**. 현재 차시들은 9~13개다 |

## 문항 타입 7종

### `multiple_choice` — 객관식

```json
{
  "type": "multiple_choice",
  "question": "DataFrame에서 열 두 개를 함께 선택하는 올바른 코드는?",
  "options": ["df[\"온도_섭씨\", \"압력_Pa\"]", "df[[\"온도_섭씨\", \"압력_Pa\"]]", "df(\"온도_섭씨\", \"압력_Pa\")", "df.column(\"온도_섭씨\", \"압력_Pa\")"],
  "answer": 1,
  "explanation": "여러 열을 선택할 때는 대괄호 안에 리스트를 한 번 더 감싸야 한다."
}
```

필수 키: `question` `options` `answer` `explanation`.
**`answer`는 0부터 세는 인덱스다.** 위 예에서 정답은 두 번째 보기다. 보기 개수를 넘으면 FAIL.

오답 보기는 **실제로 학생이 저지르는 실수**로 만든다. 무작위로 틀린 보기는 학습 가치가 없다.
위 예의 오답 셋은 전부 실제 초심자 오류다 — 대괄호 하나, 소괄호, 없는 메서드.

### `chart_choice` — 그래프 선택

스키마는 `multiple_choice`와 같고 타입만 다르다. 어떤 그래프가 적절한지 묻는 문항에 쓴다.

```json
{
  "type": "chart_choice",
  "question": "합격/불합격처럼 범주별 개수를 비교하기에 가장 알맞은 그래프는?",
  "options": ["선 그래프", "막대그래프", "산점도"],
  "answer": 1,
  "explanation": "막대그래프는 범주형 데이터의 개수 비교에 적합하다."
}
```

### `true_false` — 참/거짓

```json
{
  "type": "true_false",
  "question": "df.sort_values(\"온도_섭씨\")는 기본적으로 온도가 높은 순서(내림차순)로 정렬한다.",
  "answer": false,
  "explanation": "ascending 옵션을 주지 않으면 기본값은 오름차순이다. 내림차순은 ascending=False를 써야 한다."
}
```

필수 키: `question` `answer` `explanation`. **`answer`는 JSON 불리언**(`true`/`false`)이다 —
문자열 `"true"`가 아니다. 거짓 문항의 `explanation`에는 **올바른 사실**을 반드시 적는다.

### `fill_blank` — 빈칸 채우기

```json
{
  "type": "fill_blank",
  "question": "값을 변수에 저장할 때 pass_count ____ 34 처럼 쓰는 기호는 무엇인가?",
  "answer": "="
}
```

필수 키: `question` `answer`. `explanation`은 선택. 빈칸은 `____`(밑줄 4개)로 표시한다.

### `result_prediction` — 결과 예측

코드나 계산의 결과를 예측하게 한다. 이 과정의 성격상 **계산 과정을 `explanation`에 보여준다.**

```json
{
  "type": "result_prediction",
  "question": "합격 34건, 불합격 6건일 때 불합격 비율(%)은?",
  "answer": "15%",
  "explanation": "6 ÷ 40 × 100 = 15%"
}
```

필수 키: `question` `answer`. **여기 쓰는 숫자는 실제 데이터의 실제 값이어야 한다.**
지어낸 숫자를 쓰면 학생이 직접 계산했을 때 안 맞는다.

### `term_matching` — 용어 연결

```json
{
  "type": "term_matching",
  "question": "용어와 설명을 연결하시오.",
  "pairs": [
    { "term": "웨이퍼", "definition": "칩을 만드는 둥근 원판" },
    { "term": "FAB",   "definition": "반도체를 생산하는 공장" },
    { "term": "로트",   "definition": "함께 관리되는 웨이퍼 묶음" }
  ]
}
```

필수 키: `question` `pairs`. 각 pair는 `term`과 `definition`을 모두 가져야 한다.
`answer`나 `explanation`은 없다. 용어 정의는 `docs/glossary.md`와 어긋나지 않게 쓴다.

### `short_answer` — 서술형

```json
{
  "type": "short_answer",
  "question": "오늘 배운 내용을 바탕으로, 이 데이터를 처음 보는 사람에게 한 문장으로 설명해보시오.",
  "sample_answer": "이번 공정 기록 40건 중 34건(85%)이 합격했고, 6건(15%)이 불합격했다."
}
```

필수 키: `question` `sample_answer`(`answer`가 아니다).

이 과정의 목표가 "데이터로 공정 상태를 **설명할 수 있는 사람**"이므로, **모든 차시에
결과 해석 서술형을 최소 1개 넣는다.** `sample_answer`는 학생이 도달해야 할 수준을 보여주는
모범 답안이다 — 구체적 숫자를 포함한 한두 문장으로 쓴다.

## 구성 기준

| 기준 | 내용 |
|---|---|
| 문항 수 | 8개 이상 |
| 타입 다양성 | 3종 이상 섞는다. 객관식만 10개는 지루하고 얕다 |
| 서술형 | 결과 해석 서술형 1개 이상 필수 |
| 난이도 배치 | 쉬운 것 → 어려운 것 순서로 배열한다 |
| 범위 | **강의에서 실제로 가르친 것만 묻는다** |

마지막 항목이 가장 자주 어긋난다. 퀴즈를 늘릴 때 "이 정도는 알겠지" 싶은 것을 넣기 쉬운데,
비전공자 대상에서는 가르치지 않은 것은 모른다. 문항을 추가하면 **강의 자료에서 그 내용을
다룬 위치를 확인**한다. 없으면 강의 자료에 먼저 넣거나 문항을 뺀다.

## 8~10차시 표현 주의

상관관계·모델 결과를 다루는 문항에서는 "원인"이 아니라 **"원인 후보"**로 쓴다(CLAUDE.md).

```json
{
  "type": "true_false",
  "question": "온도와 불량률의 상관계수가 높으면 온도가 불량의 원인이라고 결론지을 수 있다.",
  "answer": false,
  "explanation": "상관관계는 함께 움직인다는 뜻일 뿐이다. 온도는 '원인 후보'이며, 원인으로 확정하려면 추가 확인이 필요하다."
}
```

이처럼 **"원인이다"라는 표현은 그것이 틀렸음을 가르치는 문항에서만** 쓴다.

## 검증

```bash
python .claude/skills/course-consistency-audit/scripts/check_course_consistency.py --week {N} --quiet
```

잡히는 것: JSON 파싱 오류, `week` 불일치, 문항 수 부족, 알 수 없는 타입, 필수 키 누락,
`answer` 인덱스 범위 초과, `true_false`의 `answer`가 불리언이 아님, `pairs` 구조 오류.

잡히지 **않는** 것(사람이 확인해야 한다): 정답이 실제로 맞는지, 강의에서 가르친 내용인지,
`result_prediction`의 숫자가 실제 데이터와 맞는지.
