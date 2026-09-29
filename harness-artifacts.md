# 한자원정대 하네스 — 산출물

> 파이프라인: `harness-pipeline.md`

## 폴더 구조

```
input/                      ← 사람이 넣는 CSV (hwp를 옮긴 것)
refs/
  unihan-rs-strokes.txt     ← 부수·총획수 대조 (Unihan에서 kRSUnicode, kTotalStrokes만 뽑음)
  basic-words.csv           ← 국립국어원 한국어 학습용 어휘 목록 A·B등급 (사람이 준비)
  banned-names.txt          ← 예문 금지 상표·인물 이름
rules.yaml                  ← 규칙 SSOT (숫자는 여기에만)
scripts/                    ← make_list · judge · review · state · notion_payload · guard(훅)
tests/good/, tests/bad/     ← 저울 검사용 예문 (good 5 / bad 10)
runs/{배치ID}/
  notion_done.json          ← S1 전에 총괄이 Notion에서 조회한 검증 완료 목록
  list.json                 ← S1
  hanja.json                ← S2
  examples.json             ← S3
  report.md                 ← S4 확인 리포트 (스크립트)
  approval.md               ← S4 사람 승인 기록 → 반영 후 approval-r{n}.md 로 보관
  notion_payload.json       ← S5에 쓸 값 (스크립트)
  notion_readback.json      ← S5 뒤 Notion에서 다시 읽은 값 (총괄)
  state.json                ← 재개용 진행 상태 (스크립트만)
  retro.md                  ← 배치 회고
```

## 규칙 SSOT: rules.yaml

```yaml
batch:
  max_size: 50
  id_format: "{grade}-{seq:02d}"
  skip_status: "검증 완료"          # Notion에서 이 상태인 한자는 S1에서 제외

hanja:
  hun_eum_source: input_csv         # 문자열 완전 일치
  radical_strokes_source: unihan    # kRSUnicode, kTotalStrokes 숫자 일치
  nature_values: [상형자, 지사자, 회의자, 형성자]
  nature_source_url_required: true  # 네이버 한자사전 URL

example:
  count_per_hanja: 4
  context_values: [school, home, shop, traffic, weather, etc]
  min_distinct_context: 3
  max_length_with_spaces: 55
  end_marks_exact: 1                # . ? ! 합계 정확히 1개
  target_word_pattern: "한글(漢字)"  # 목표 한자가 든 단어가 정확히 1번
  target_word_list: refs/basic-words.csv   # 없으면 탈락이 아니라 needs-human
  duplicate_word_allowed: true
  style: any

retry:
  max_per_hanja: 3                  # 넘으면 needs-human
```

## 재개 (state.json)

```json
{
  "batch": "8급-01",
  "hanja": {
    "一": { "stage": "S3", "retries": 1, "status": "fail", "reasons": ["length>55: 예문2"] },
    "二": { "stage": "S5", "retries": 0, "status": "done" }
  }
}
```

- `status`: `pending / pass / fail / needs-human / approved / done`
- 다시 실행하면 `done`인 한자는 건너뛰고, 나머지는 기록된 `stage`부터 이어서 처리한다.
- `state.json`은 **스크립트만** 쓴다. 총괄과 생성 에이전트는 읽기만 한다.
