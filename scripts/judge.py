"""판정 스크립트 (저울). 통과/실패는 이 스크립트만 정한다.

사용:
  python3 scripts/judge.py 8급-01 --gate G2          # 판정 + state.json 갱신
  python3 scripts/judge.py 8급-01 --gate G3 --check  # 판정만 (judge 에이전트용, 파일을 바꾸지 않음)
  python3 scripts/judge.py 8급-01 --gate G5          # Notion 다시 읽은 값 대조
  python3 scripts/judge.py --selftest                # 저울 검사 (tests/bad 10 실패, tests/good 5 통과)
"""
import argparse
import re
import sys
from pathlib import Path

from common import (ROOT, batch_dir, die, forbidden_hits, load_banned_names, load_rules, load_state,
                    load_word_list, read_json, save_state, unihan)

WORD_RE = re.compile(r"([가-힣]+)\(([㐀-鿿豈-﫿]+)\)")


# ---------- G2 한자정보 ----------

def check_hanja(item, info, rules, banned):
    """item: list.json 항목, info: hanja.json 항목. 실패 사유 목록을 돌려준다."""
    if not info:
        return ["missing: hanja.json에 없음"]
    r, reasons = rules["hanja"], []
    fields = ["hun", "eum", "hun_eum", "radical", "radical_hun_eum", "total_strokes", "nature",
              "nature_story", "nature_source_url", "writing"]
    for f in fields:
        if info.get(f) in (None, ""):
            reasons.append(f"empty:{f}")
    if info.get("hun") != item["hun"]:
        reasons.append(f"hun_mismatch: CSV '{item['hun']}' ≠ '{info.get('hun')}'")
    if info.get("eum") != item["eum"]:
        reasons.append(f"eum_mismatch: CSV '{item['eum']}' ≠ '{info.get('eum')}'")
    if info.get("hun_eum") != f"{item['hun']} {item['eum']}":
        reasons.append(f"hun_eum_format: '{info.get('hun_eum')}' ≠ '{item['hun']} {item['eum']}'")
    if info.get("writing") is not item["writing"]:
        reasons.append(f"writing_mismatch: CSV {item['writing']} ≠ {info.get('writing')}")
    ref = unihan().get(item["char"])
    if not ref:
        reasons.append("unihan_missing: 대조 데이터 없음")
    else:
        if info.get("radical") != ref.get("radical"):
            reasons.append(f"radical_mismatch: Unihan '{ref.get('radical')}' ≠ '{info.get('radical')}'")
        if info.get("total_strokes") not in ref.get("strokes", set()):
            reasons.append(f"strokes_mismatch: Unihan {sorted(ref.get('strokes', []))} ≠ {info.get('total_strokes')}")
    nature = info.get("nature")
    if nature not in r["nature_values"]:
        reasons.append(f"nature_value: '{nature}'")
    comps = (info.get("components") or "").strip()
    if nature in r["components_required_for"] and not comps:
        reasons.append("components_required: 회의자·형성자는 구성 요소 필요")
    if nature not in r["components_required_for"] and comps:
        reasons.append("components_not_allowed: 상형자·지사자는 구성 요소 비움")
    if not str(info.get("nature_source_url", "")).startswith(r["nature_source_url_prefix"]):
        reasons.append("source_url: 네이버 한자사전 URL 아님")
    reasons += forbidden_hits(str(info.get("nature_story", "")), rules, banned)
    return reasons


# ---------- G3 예문 ----------

def check_examples(char, examples, rules, banned, words):
    """실패 사유 목록과 needs-human 표시 목록을 돌려준다."""
    r, reasons, flags = rules["example"], [], []
    examples = examples or []
    if len(examples) != r["count_per_hanja"]:
        reasons.append(f"count: {len(examples)} ≠ {r['count_per_hanja']}")
    contexts = [e.get("context") for e in examples]
    for c in contexts:
        if c not in r["context_values"]:
            reasons.append(f"context_value: '{c}'")
    if len(set(contexts)) < r["min_distinct_context"]:
        reasons.append(f"context_distinct: {len(set(contexts))}종 < {r['min_distinct_context']}")
    for n, e in enumerate(examples, start=1):
        s = e.get("sentence", "")
        tag = f"예문{n}"
        if len(s) > r["max_length_with_spaces"]:
            reasons.append(f"length: {tag} {len(s)}자 > {r['max_length_with_spaces']}")
        marks = sum(s.count(m) for m in r["end_marks"])
        if marks != r["end_marks_exact"]:
            reasons.append(f"end_mark: {tag} 끝맺음 부호 {marks}개")
        found = WORD_RE.findall(s)
        if len(found) != r["target_word_count_exact"]:
            reasons.append(f"pattern_count: {tag} 한글(漢字) {len(found)}번")
        else:
            hangul, hanja = found[0]
            if char not in hanja:
                reasons.append(f"pattern_target: {tag} '{hanja}'에 {char} 없음")
            if len(hangul) != len(hanja):
                reasons.append(f"pattern_length: {tag} '{hangul}'와 '{hanja}' 글자 수 다름")
            if e.get("word_hangul") != hangul or e.get("word_hanja") != hanja:
                reasons.append(f"word_field: {tag} word_hangul/word_hanja가 문장과 다름")
            if words is not None and hangul not in words:
                flags.append(f"word_not_in_list: {tag} '{hangul}'")
        reasons += [f"{h} ({tag})" for h in forbidden_hits(s, rules, banned)]
    if words is None:
        flags.append("word_list_missing: refs/basic-words.csv 없음")
    return reasons, flags


# ---------- 상태 갱신 ----------

def apply_result(entry, reasons, next_stage, rules, flags=()):
    if not reasons:
        entry.update(stage=next_stage, retries=0, reasons=[], flags=list(flags))
        entry["status"] = "needs-human" if flags else "pending"
        if flags:
            entry["ever_needs_human"] = True
        return "pass"
    entry["retries"] += 1
    entry["total_retries"] += 1
    entry["reasons"] = reasons
    if entry["retries"] > rules["retry"]["max_per_hanja"]:
        entry["status"] = "needs-human"
        entry["ever_needs_human"] = True
        return "needs-human"
    entry["status"] = "fail"
    return "fail"


def run_gate(batch, gate, check_only):
    rules = load_rules()
    banned = load_banned_names(rules)
    state = load_state(batch)
    d = batch_dir(batch)
    items = {i["char"]: i for i in read_json(d / "list.json")["hanja"]}
    stage = {"G2": "S2", "G3": "S3"}[gate]
    targets = [c for c, e in state["hanja"].items()
               if e["stage"] == stage and e["status"] in ("pending", "fail", "needs-human")]
    if not targets:
        print(f"{gate}: 판정할 한자가 없습니다 ({stage} 단계 대기 0자)")
        return 0

    if gate == "G2":
        path = d / "hanja.json"
        data = read_json(path)["hanja"] if path.exists() else {}
        results = {c: (check_hanja(items[c], data.get(c), rules, banned), []) for c in targets}
        next_stage = "S3"
    else:
        path = d / "examples.json"
        data = read_json(path)["examples"] if path.exists() else {}
        words = load_word_list(rules["example"]["target_word_list"])
        results = {c: check_examples(c, data.get(c), rules, banned, words) for c in targets}
        next_stage = "S4"

    counts = {"pass": 0, "fail": 0, "needs-human": 0}
    for c, (reasons, flags) in results.items():
        mark = "통과" if not reasons else "실패"
        print(f"{c}\t{mark}\t" + "; ".join(reasons + flags))
        if check_only:
            counts["pass" if not reasons else "fail"] += 1
        else:
            outcome = apply_result(state["hanja"][c], reasons, next_stage, rules, flags)
            key = "needs-human" if state["hanja"][c]["status"] == "needs-human" else outcome
            counts[key] += 1
    if not check_only:
        save_state(batch, state)
    print(f"{gate} {'검사' if check_only else '완료'} — 통과 {counts['pass']} / 다시 만들기 {counts['fail']} / 사람 확인 {counts['needs-human']}")
    return 1 if counts["fail"] else 0


# ---------- G5 Notion 대조 ----------

def run_g5(batch, check_only):
    rules = load_rules()
    state = load_state(batch)
    d = batch_dir(batch)
    payload = read_json(d / "notion_payload.json")
    readback_path = d / "notion_readback.json"
    if not readback_path.exists():
        die(f"{readback_path} 가 없습니다. Notion에서 다시 읽은 행을 저장하세요.")
    rows = read_json(readback_path)
    by_char = {}
    for row in rows:
        by_char.setdefault(row.get("한자"), []).append(row)

    def norm(key, value):
        if key == "쓰기 출제":
            return value in (True, "__YES__", "true")
        if key == "총획수":
            return int(float(value)) if value not in (None, "") else None
        return (value or "").strip() if isinstance(value, str) or value is None else value

    ok = fail = 0
    for char, props in payload.items():
        entry = state["hanja"][char]
        found = by_char.get(char, [])
        reasons = []
        if len(found) != 1:
            reasons.append(f"rows: Notion에 '{char}' 행이 {len(found)}개")
        else:
            for key, want in props.items():
                if norm(key, found[0].get(key)) != norm(key, want):
                    reasons.append(f"{key}: Notion '{found[0].get(key)}' ≠ '{want}'")
        print(f"{char}\t{'일치' if not reasons else '불일치'}\t" + "; ".join(reasons))
        if check_only:
            continue
        if reasons:
            fail += 1
            entry["s5_attempts"] += 1
            entry["reasons"] = reasons
            if entry["s5_attempts"] > rules["retry"]["s5_max"]:
                entry["status"] = "blocked"
        else:
            ok += 1
            entry.update(stage="done", status="done", reasons=[])
    if not check_only:
        save_state(batch, state)
    blocked = [c for c, e in state["hanja"].items() if e["status"] == "blocked"]
    print(f"G5 완료 — 일치 {ok} / 불일치 {fail}" + (f" / 멈춤(사람 필요) {len(blocked)}: {''.join(blocked)}" if blocked else ""))
    return 1 if fail else 0


# ---------- 저울 검사 ----------

def selftest():
    rules = load_rules()
    words = load_word_list(ROOT / "tests" / "basic-words.csv")
    problems, total = [], 0
    for kind in ("good", "bad"):
        for path in sorted((ROOT / "tests" / kind).glob("*.json")):
            total += 1
            case = read_json(path)
            reasons, flags = check_examples(case["char"], case["examples"], rules, [], words)
            if kind == "good" and (reasons or flags):
                problems.append(f"{path.name}: 통과해야 하는데 실패 — {reasons + flags}")
            if kind == "bad":
                expected = case["expect_rule"]
                if not any(r.startswith(expected) for r in reasons):
                    problems.append(f"{path.name}: '{expected}'로 실패해야 하는데 — {reasons or '통과됨'}")
    good = len(list((ROOT / "tests" / "good").glob("*.json")))
    bad = len(list((ROOT / "tests" / "bad").glob("*.json")))
    if problems:
        print("저울 검사 실패:")
        for p in problems:
            print(" -", p)
        return 1
    print(f"저울 검사 통과 — good {good}/{good} 통과, bad {bad}/{bad} 실패로 잡음")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", nargs="?")
    ap.add_argument("--gate", choices=["G2", "G3", "G5"])
    ap.add_argument("--check", action="store_true", help="판정만 하고 state.json을 바꾸지 않음")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.batch or not args.gate:
        die("사용: judge.py <배치ID> --gate G2|G3|G5 [--check]")
    sys.exit(run_g5(args.batch, args.check) if args.gate == "G5" else run_gate(args.batch, args.gate, args.check))


if __name__ == "__main__":
    main()
