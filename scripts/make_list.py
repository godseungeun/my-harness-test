"""S1 목록화 + G1 입력 게이트.

사용: python3 scripts/make_list.py 8급-01 --csv input/8급.csv [--done runs/8급-01/notion_done.json] [--limit 5]

- CSV 열: 한자,훈,음,급수,쓰기   (쓰기: Y/N, O/X, 1/0, TRUE/FALSE, 예/아니오)
- --done: Notion에서 `검증 완료`인 한자 목록 (JSON 배열). 오케스트레이터가 만든다.
- --limit: 연습 실행(dry run)용. 앞에서 N자만 쓰고 Notion 반영을 막는다.
"""
import argparse
import csv
import re
import sys

from common import ROOT, batch_dir, die, load_rules, new_entry, parse_batch_id, read_json, write_json

REQUIRED = ["한자", "훈", "음", "급수", "쓰기"]
TRUE_VALUES = {"y", "o", "1", "true", "예", "yes"}
FALSE_VALUES = {"n", "x", "0", "false", "아니오", "no", ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--done")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    rules = load_rules()
    grade, seq = parse_batch_id(args.batch, rules)
    out = batch_dir(args.batch)
    if (out / "list.json").exists():
        die(f"{out}/list.json 이 이미 있습니다. 새로 만들지 않습니다. 이어서 하려면 state.json 기준으로 재개하세요.")

    errors = []
    with open(ROOT / args.csv if not args.csv.startswith("/") else args.csv, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            die(f"G1 실패: CSV에 필수 열이 없습니다: {missing}")
        rows = [r for r in reader if (r.get("급수") or "").strip() == grade]

    if not rows:
        errors.append(f"CSV에 급수 '{grade}' 행이 없습니다")
    seen = set()
    for i, r in enumerate(rows, start=2):
        for c in ["한자", "훈", "음", "급수"]:
            if not (r.get(c) or "").strip():
                errors.append(f"{i}행: '{c}' 빈칸")
        ch = (r.get("한자") or "").strip()
        if len(ch) != 1:
            errors.append(f"{i}행: 한자는 한 글자여야 합니다 ('{ch}')")
        if ch in seen:
            errors.append(f"{i}행: 한자 중복 '{ch}'")
        seen.add(ch)
        for c in ["훈", "음"]:
            if not re.fullmatch(r"[가-힣 ]+", (r.get(c) or "").strip() or "x"):
                errors.append(f"{i}행: '{c}'는 한글만 ('{r.get(c)}')")
        if (r.get("쓰기") or "").strip().lower() not in TRUE_VALUES | FALSE_VALUES:
            errors.append(f"{i}행: '쓰기' 값을 알 수 없습니다 ('{r.get('쓰기')}')")

    done = set(read_json(args.done)) if args.done else set()
    candidates = [r for r in rows if r["한자"].strip() not in done]
    size = rules["batch"]["max_size"]
    chunk = candidates[(seq - 1) * size: seq * size]
    if args.limit:
        chunk = chunk[: args.limit]
    if rows and not chunk:
        errors.append(f"{args.batch}: 처리할 한자가 없습니다 (남은 한자 {len(candidates)}자)")
    if len(chunk) > size:
        errors.append(f"배치 크기 {len(chunk)} > {size}")
    if any(r["한자"].strip() in done for r in chunk):
        errors.append("배치에 이미 검증 완료된 한자가 들어 있습니다")

    if errors:
        print("G1 실패 — 입력 CSV를 사람이 고쳐야 합니다. AI는 CSV를 고치지 않습니다.", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)
    items = [{"char": r["한자"].strip(), "hun": r["훈"].strip(), "eum": r["음"].strip(), "grade": grade,
              "writing": r["쓰기"].strip().lower() in TRUE_VALUES} for r in chunk]
    write_json(out / "list.json", {"batch": args.batch, "grade": grade, "hanja": items})
    write_json(out / "state.json", {"batch": args.batch, "grade": grade, "dry_run": bool(args.limit),
                                    "round": 1, "hanja": {i["char"]: new_entry() for i in items}})
    print(f"S1 완료 — {args.batch}: {len(items)}자 (남은 새 한자 {len(candidates)}자, 제외된 검증 완료 {len(done)}자)"
          + (" · 연습 실행" if args.limit else ""))


if __name__ == "__main__":
    main()
