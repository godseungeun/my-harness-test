# 한자원정대 하네스 — 역할

> 게이트: `harness-gates.md` · 산출물: `harness-artifacts.md`

## 한눈에 보기 (주방 비유)

| 역할 | 비유 | 하는 일 |
|---|---|---|
| 총괄 (orchestrator) | 주방장 | 순서대로 일을 시키고 진행표를 적는다 |
| hanja-writer | 요리사 A | 한자정보(S2)만 쓴다 |
| example-writer | 요리사 B | 예문(S3)만 쓴다 |
| judge | 검수원 | 보기만 한다. 이상하면 `needs-human` 표시 |
| `scripts/` | 저울 | 숫자·금지어를 센다. 통과/실패는 저울만 정한다 |

## 역할별 권한

| 역할 | 종류 | 편집 가능 | 도구 |
|---|---|---|---|
| orchestrator | 메인 세션 (`CLAUDE.md`) | `runs/{배치}/notion_done.json`, `runs/{배치}/notion_readback.json` **만** | 서브에이전트 호출, 스크립트 실행, Notion MCP (S1 조회, S5 쓰기) |
| hanja-writer | 서브에이전트 | `runs/{배치}/hanja.json` **만** | Read, Write, WebFetch (네이버 한자사전만) |
| example-writer | 서브에이전트 | `runs/{배치}/examples.json` **만** | Read, Write |
| judge | 서브에이전트, **읽기 전용** | 없음 | Read, Grep, `scripts/judge.py` 실행 |
| `scripts/` | Python 스크립트 | — | 사람이 승인한 뒤에만 수정 |

- 편집 범위는 **파일 1개 단위**다. 허용되지 않은 경로에 Write/Edit를 시도하면 **훅(PreToolUse)이 차단**한다.
- judge는 통과를 판정할 권한이 없다. 스크립트 결과를 전달하고, 스크립트가 셀 수 없는 문제(어려운 맥락, 광고처럼 보이는 표현)에만 **의심 표시**를 한다. 의심 표시된 한자는 `needs-human`으로 간다.
- `input/`, `refs/`, `rules.yaml`, `approval.md`는 **사람만** 수정한다.
- `state.json`, `list.json`, `report.md`, `notion_payload.json`, `retro.md`는 **스크립트만** 쓴다. 총괄도 직접 고칠 수 없다(실패를 통과로 바꾸지 못하게 하려는 것).
- 차단 기록은 `.claude/guard.log`에 한 줄씩 쌓인다.

## Notion 반영 (S5)

- 오케스트레이터가 **지금 연결된 Notion MCP**로 쓴다.
- 쓴 뒤 다시 읽어서 `scripts/`가 승인된 JSON과 대조한다 (G5).

## 자연어 트리거

| 말 | 동작 |
|---|---|
| "8급-01 돌려줘" / "8급 새 배치 시작" | S1부터 시작 |
| "이어서 해줘" | `state.json`을 읽고 멈춘 곳부터 재개 |
| "승인 반영해줘" | `approval.md`로 G4 확인 → 반려는 되돌리고 승인은 S5 |
| "배치 상태 보여줘" | `state.json` 요약 (단계별 한자 수) |
