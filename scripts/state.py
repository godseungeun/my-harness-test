"""진행 상태 보기와 의심 표시.

사용:
  python3 scripts/state.py status 8급-01             # 단계별 한자 수
  python3 scripts/state.py flag 8급-01 日 "이유"     # judge 의심 표시 → needs-human (통과로는 절대 바꾸지 않음)
  python3 scripts/state.py todo 8급-01 S2            # 그 단계에서 다시 만들어야 할 한자와 사유
"""
import sys
from collections import Counter

from common import die, load_state, save_state


def status(batch):
    state = load_state(batch)
    counts = Counter((e["stage"], e["status"]) for e in state["hanja"].values())
    print(f"{batch} ({len(state['hanja'])}자{' · 연습 실행' if state.get('dry_run') else ''}, 라운드 {state['round']})")
    for (stage, st), n in sorted(counts.items()):
        chars = "".join(c for c, e in state["hanja"].items() if e["stage"] == stage and e["status"] == st)
        print(f"  {stage:5} {st:12} {n:3}자  {chars}")


def flag(batch, char, reason):
    state = load_state(batch)
    e = state["hanja"].get(char) or die(f"{char}: 배치에 없는 한자")
    if e["stage"] != "S4":
        die(f"{char}: S4 단계에서만 의심 표시를 할 수 있습니다 (지금 {e['stage']})")
    e["status"] = "needs-human"
    e["ever_needs_human"] = True
    e["flags"].append(f"judge: {reason}")
    save_state(batch, state)
    print(f"{char} → needs-human ({reason})")


def todo(batch, stage):
    state = load_state(batch)
    for c, e in state["hanja"].items():
        if e["stage"] == stage and e["status"] in ("pending", "fail"):
            print(f"{c}\t{e['status']}\t" + "; ".join(e["reasons"]))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["status"] and len(args) == 2:
        status(args[1])
    elif args[:1] == ["flag"] and len(args) == 4:
        flag(*args[1:])
    elif args[:1] == ["todo"] and len(args) == 3:
        todo(*args[1:])
    else:
        die(__doc__)
