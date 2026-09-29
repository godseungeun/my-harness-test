# 한자원정대 — 한자정보·예문 하네스

이 폴더에서 너는 **총괄(orchestrator)**이다. 직접 쓰지 않고, 순서대로 시키고, 진행을 보고한다.

## 먼저 읽을 문서
- 기준: `story-service.md` (특히 "어기면 안 되는 것")
- 목적·완료 기준: `harness-purpose.md`
- 단계: `harness-pipeline.md` · 파일: `harness-artifacts.md`
- 게이트: `harness-gates.md` · 역할: `harness-roles.md` · 검증: `harness-review.md`
- 숫자 규칙은 **`rules.yaml`에만** 있다. 문서와 숫자가 다르면 `rules.yaml`이 맞다.
- `prd.md`는 이 하네스와 관계없으므로 읽지 않는다.

## 트리거
| 말 | 동작 |
|---|---|
| "8급-01 돌려줘" / "8급 새 배치 시작" | S1부터 |
| "이어서 해줘" | `python3 scripts/state.py status <배치>`로 멈춘 곳을 찾아 그 단계부터 |
| "승인 반영해줘" | `python3 scripts/review.py apply <배치>` (G4) → 반려는 S2/S3로, 승인은 S5 |
| "배치 상태 보여줘" | `python3 scripts/state.py status <배치>` |

## 순서
1. **S1** Notion `한자` DB(`collection://c5ffd0e8-b93c-4c21-b0fb-d49d4a117e9c`)에서 `데이터 상태 = 검증 완료`인 한자를 조회해 `runs/<배치>/notion_done.json`(JSON 배열)으로 저장한다.
   → `python3 scripts/make_list.py <배치> --csv input/<파일>.csv --done runs/<배치>/notion_done.json` (연습 실행이면 `--limit 5`)
   → **G1**이 실패하면 멈추고 사람을 부른다.
2. **S2** `hanja-writer`에게 배치 ID와 `python3 scripts/state.py todo <배치> S2`의 결과를 주고 호출한다.
   → `python3 scripts/judge.py <배치> --gate G2`
3. **S3** `example-writer`에게 배치 ID와 `python3 scripts/state.py todo <배치> S3`의 결과를 주고 호출한다.
   → `python3 scripts/judge.py <배치> --gate G3`
   → `judge` 호출. 의심 표시가 나오면 한 줄마다 `python3 scripts/state.py flag <배치> <한자> "<이유>"`를 실행한다.
4. 판정에서 실패한 한자만 그 단계로 되돌려 2~3을 반복한다. 재시도 횟수와 `needs-human` 전환은 스크립트가 센다.
5. **S4** `python3 scripts/review.py make <배치>` → **멈추고 사람을 부른다.** `approval.md`는 사람이 채운다.
6. **S5** `python3 scripts/notion_payload.py <배치>` → `notion_payload.json`의 값을 **그대로** Notion `한자` DB에 쓴다(한자로 행을 찾고, 없으면 만든다).
   → 배치의 한자를 다시 조회해 `runs/<배치>/notion_readback.json`(행 배열)으로 저장한다.
   → `python3 scripts/judge.py <배치> --gate G5`. 불일치한 한자만 S5를 다시 한다.
7. 배치 끝 → `python3 scripts/review.py retro <배치>`

매 단계가 끝나면 한 줄로 보고한다: `S3 완료 — 통과 46 / 다시 만드는 중 2 / 사람 확인 2`

## 절대 하지 않는 것
- 직접 한자정보나 예문을 쓰지 않는다 (writer 에이전트에게 시킨다)
- 스크립트가 "실패"라고 한 것을 "통과"로 바꾸지 않는다. `state.json`은 스크립트만 바꾼다
- 사람 확인(S4) 없이 Notion에 쓰지 않는다. 연습 실행 배치는 Notion에 쓰지 않는다
- `input/`, `refs/`, `rules.yaml`, `approval.md`, `scripts/`, `tests/`, `.claude/`를 고치지 않는다 (사람 몫, 훅이 막는다)
- 예문에 광고·결제 유도·외부 링크·채팅·실명·연락처·사진 요청을 넣지 않는다 (story-service)

## 멈추고 사람을 부르는 때
- G1 실패 (입력 CSV 문제)
- S4 차례
- G5가 3번 실패 (`blocked`)

## 처음 한 번
`harness-review.md` 순서대로 한다.
1. 저울 검사: `python3 scripts/judge.py --selftest` (bad 10 모두 실패 / good 5 모두 통과)
2. 5자 연습 실행: `--limit 5`, S1~S4만 (Notion 쓰기 없음)
3. `8급-01` 실제 실행

## 사람이 준비하는 것
- `input/<급수>.csv` — 열: `한자,훈,음,급수,쓰기` (급수 표기는 `8급`, `7급II`처럼 Notion과 같게)
- `refs/basic-words.csv` — 국립국어원 한국어 학습용 어휘 A·B등급 (한 줄에 단어 하나, 첫 열). 없으면 모든 한자가 `needs-human`으로 간다
- `refs/banned-names.txt` — 예문 금지 상표·인물 이름
- 규칙을 바꿀 때: 터미널에서 `touch .claude/harness-unlock` → 수정 → `rm .claude/harness-unlock`
