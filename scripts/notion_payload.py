"""S5 준비: 승인된 한자의 Notion 속성 값을 만든다. 오케스트레이터는 이 값만 그대로 쓴다.

사용: python3 scripts/notion_payload.py 8급-01   → runs/8급-01/notion_payload.json
"""
import sys

from common import batch_dir, die, load_rules, load_state, read_json, write_json


def main(batch):
    rules = load_rules()
    state = load_state(batch)
    if state.get("dry_run"):
        die("연습 실행 배치는 Notion에 쓰지 않습니다.")
    d = batch_dir(batch)
    hanja = read_json(d / "hanja.json")["hanja"]
    examples = read_json(d / "examples.json")["examples"]
    payload = {}
    for c, e in state["hanja"].items():
        if e["stage"] != "S5" or e["status"] not in ("approved",):
            continue
        h = hanja[c]
        props = {
            "한자": c, "훈": h["hun"], "음": h["eum"], "훈음": h["hun_eum"], "급수": state["grade"],
            "부수": h["radical"], "부수 훈음": h["radical_hun_eum"], "총획수": h["total_strokes"],
            "성격": h["nature"], "성격 이야기": h["nature_story"], "구성 요소": h.get("components") or "",
            "쓰기 출제": h["writing"], "데이터 상태": rules["batch"]["skip_status"],
        }
        for n, ex in enumerate(examples[c], start=1):
            props[f"예문{n}"] = ex["sentence"]
            props[f"예문{n} context"] = ex["context"]
        payload[c] = props
    write_json(d / "notion_payload.json", payload)
    print(f"S5 준비 — {len(payload)}자 → {d}/notion_payload.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        die(__doc__)
    main(sys.argv[1])
