"""S4 사람 확인 + G4 + 회고.

사용:
  python3 scripts/review.py make 8급-01    # report.md, approval.md 만들기 (S4 시작)
  python3 scripts/review.py apply 8급-01   # 사람이 채운 approval.md 확인 (G4)
  python3 scripts/review.py retro 8급-01   # retro.md 만들기 (배치 끝)
"""
import random
import re
import sys

from common import batch_dir, die, load_rules, load_state, read_json, save_state, write_json

HEADER = "| 한자 | 확인 이유 | 결정 | 되돌릴 단계 | 메모 |"
RULE = "|---|---|---|---|---|"


def waiting(state):
    """S4 전에 아직 기계 단계에 남은 한자."""
    return {c: e for c, e in state["hanja"].items()
            if e["stage"] in ("S2", "S3") and e["status"] in ("pending", "fail")}


def make(batch):
    rules = load_rules()
    state = load_state(batch)
    d = batch_dir(batch)
    busy = waiting(state)
    if busy:
        die(f"아직 S2/S3에서 다시 만드는 중인 한자가 있습니다: {''.join(busy)}")
    if (d / "approval.md").exists():
        die(f"{d}/approval.md 가 이미 있습니다. 사람이 채운 뒤 'apply'를 실행하세요.")

    s4 = {c: e for c, e in state["hanja"].items() if e["stage"] == "S4"}
    stuck = {c: e for c, e in state["hanja"].items() if e["stage"] in ("S2", "S3") and e["status"] == "needs-human"}
    must = [c for c, e in s4.items() if e["status"] == "needs-human"]
    rest = sorted(c for c, e in s4.items() if e["status"] != "needs-human")
    rng = random.Random(f"{batch}-r{state['round']}")
    sample = sorted(rng.sample(rest, min(rules["review"]["sample_size"], len(rest))))

    hanja = read_json(d / "hanja.json")["hanja"] if (d / "hanja.json").exists() else {}
    examples = read_json(d / "examples.json")["examples"] if (d / "examples.json").exists() else {}

    lines = [f"# {batch} 확인 리포트 (라운드 {state['round']})", "",
             f"- S4 도착 {len(s4)}자 · 사람 확인 필요 {len(must)}자 · 표본 {len(sample)}자",
             f"- 표본에서 반려가 {rules['review']['full_review_if_rejects_gte']}자 이상이면 배치 전체를 확인합니다.", ""]
    if stuck:
        lines += ["## ⚠️ 자동 생성 실패 (사람이 직접 고쳐야 함)", "",
                  "아래 한자는 재시도를 모두 써서 멈췄습니다. `hanja.json`이나 `examples.json`을 직접 고친 뒤 \"이어서 해줘\"라고 하면 다시 판정합니다.", ""]
        for c, e in stuck.items():
            lines.append(f"- **{c}** ({e['stage']}): " + "; ".join(e["reasons"]))
        lines.append("")
    lines += ["## 확인 대상", ""]
    for c in must + sample:
        h, e = hanja.get(c, {}), state["hanja"][c]
        why = "사람 확인: " + "; ".join(e["flags"] + e["reasons"]) if c in must else "표본"
        lines += [f"### {c} — {h.get('hun_eum', '')} · {why}", "",
                  f"- 부수 {h.get('radical')} ({h.get('radical_hun_eum')}) · {h.get('total_strokes')}획 · 쓰기 {'O' if h.get('writing') else 'X'}",
                  f"- 성격: **{h.get('nature')}** — [네이버 한자사전]({h.get('nature_source_url')})",
                  f"- 성격 이야기: {h.get('nature_story')}",
                  f"- 구성 요소: {h.get('components') or '—'}"]
        for n, ex in enumerate(examples.get(c, []), start=1):
            lines.append(f"- 예문{n} `{ex.get('context')}` {ex.get('sentence')}")
        lines.append("")
    (d / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    rows = [f"| {c} | 사람 확인 | | | |" for c in must] + [f"| {c} | 표본 | | | |" for c in sample]
    (d / "approval.md").write_text(
        f"# {batch} 승인 (라운드 {state['round']})\n\n"
        "`결정` 칸에 **승인** 또는 **반려**를 적어 주세요. 반려하면 `되돌릴 단계`에 **S2**(한자정보) 또는 **S3**(예문)를 적고, 메모에 이유를 적어 주세요.\n\n"
        + HEADER + "\n" + RULE + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"S4 준비 — 확인 대상 {len(must) + len(sample)}자 (사람 확인 {len(must)}, 표본 {len(sample)})"
          + (f" · 자동 생성 실패 {len(stuck)}자" if stuck else "") + f" → {d}/approval.md 를 채워 주세요")


def parse_approval(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and len(cells[0]) == 1 and re.match(r"[㐀-鿿豈-﫿]", cells[0]):
            rows.append(dict(zip(["char", "why", "decision", "back", "memo"], cells)))
    return rows


def apply(batch):
    rules = load_rules()
    state = load_state(batch)
    d = batch_dir(batch)
    path = d / "approval.md"
    if not path.exists():
        die("approval.md 가 없습니다. 먼저 'make'를 실행하세요.")
    rows = parse_approval(path)
    errors = []
    for r in rows:
        if r["decision"] not in ("승인", "반려"):
            errors.append(f"{r['char']}: 결정 칸이 비었거나 '{r['decision']}'")
        elif r["decision"] == "반려" and r["back"] not in ("S2", "S3"):
            errors.append(f"{r['char']}: 반려는 되돌릴 단계(S2/S3)가 필요")
        if r["char"] not in state["hanja"] or state["hanja"][r["char"]]["stage"] != "S4":
            errors.append(f"{r['char']}: S4 단계 한자가 아님")
    if errors:
        print("G4 실패 — approval.md를 마저 채워 주세요:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    listed = {r["char"] for r in rows}
    sample_rejects = sum(1 for r in rows if r["why"] == "표본" and r["decision"] == "반려")
    s4_rest = sorted(c for c, e in state["hanja"].items() if e["stage"] == "S4" and c not in listed)
    if sample_rejects >= rules["review"]["full_review_if_rejects_gte"] and s4_rest:
        with path.open("a", encoding="utf-8") as f:
            f.write("".join(f"| {c} | 전체 확인 | | | |\n" for c in s4_rest))
        print(f"G4 — 표본 반려 {sample_rejects}자 → 배치 전체 확인이 필요합니다. approval.md에 {len(s4_rest)}자를 추가했습니다.")
        sys.exit(3)

    approved = rejected = 0
    for r in rows:
        e = state["hanja"][r["char"]]
        if r["decision"] == "승인":
            e.update(stage="S5", status="approved", reasons=[], flags=[])
            approved += 1
        else:
            e.update(stage=r["back"], status="pending", retries=0, reasons=[f"사람 반려: {r['memo']}"], flags=[])
            e["rejected"] += 1
            rejected += 1
    for c in s4_rest:
        state["hanja"][c].update(stage="S5", status="approved")
        approved += 1
    path.rename(d / f"approval-r{state['round']}.md")
    state["round"] += 1
    save_state(batch, state)
    print(f"G4 완료 — 승인 {approved} / 반려 {rejected}" + (" · 연습 실행이라 S5(Notion)는 건너뜁니다" if state.get("dry_run") else ""))


def retro(batch):
    rules = load_rules()
    state = load_state(batch)
    entries = state["hanja"].values()
    n = len(state["hanja"])
    retries = sum(e["total_retries"] for e in entries)
    human = sum(1 for e in entries if e["ever_needs_human"])
    rejected = sum(1 for e in entries if e["rejected"])
    done = sum(1 for e in entries if e["status"] == "done")
    alert = rejected / n > rules["retro"]["reject_ratio_alert"] if n else False
    text = (f"# {batch} 회고\n\n| 항목 | 값 |\n|---|---|\n"
            f"| 한자 수 | {n} |\n| 검증 완료 | {done}/{n} |\n| 다시 만든 횟수 (합계) | {retries} |\n"
            f"| 사람 확인으로 간 한자 | {human} |\n| 사람이 반려한 한자 | {rejected} ({rejected / n:.0%}) |\n\n"
            + ("⚠️ 반려가 20%를 넘었습니다. 다음 배치 전에 `rules.yaml`을 사람과 함께 다시 봅니다.\n" if alert else ""))
    (batch_dir(batch) / "retro.md").write_text(text, encoding="utf-8")
    print(f"회고 — 다시 만들기 {retries} / 사람 확인 {human} / 반려 {rejected}" + (" ⚠️ 반려 20% 초과" if alert else ""))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("make", "apply", "retro"):
        die(__doc__)
    {"make": make, "apply": apply, "retro": retro}[sys.argv[1]](sys.argv[2])
