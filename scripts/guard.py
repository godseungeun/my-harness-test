"""PreToolUse 훅: 역할별 편집 범위를 강제한다. 막으면 exit 2 + 이유를 Claude에게 돌려준다.

- hanja-writer   → runs/<배치>/hanja.json 만, WebFetch는 hanja.dict.naver.com 만
- example-writer → runs/<배치>/examples.json 만
- judge          → 편집 불가, Bash는 `python3 scripts/judge.py ... --check` 와 `--selftest` 만
- 메인 세션(총괄) → 사람 몫 파일과 스크립트가 쓰는 파일은 편집 불가
                    (runs/<배치>/notion_done.json, notion_readback.json 만 직접 씀)
- 사람이 규칙을 바꿀 때: 터미널에서 `touch .claude/harness-unlock` → 끝나면 삭제
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parent.parent)
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

WRITER_ALLOW = {
    "hanja-writer": re.compile(r"^runs/[^/]+/hanja\.json$"),
    "example-writer": re.compile(r"^runs/[^/]+/examples\.json$"),
}
MAIN_ALLOW_IN_RUNS = re.compile(r"^runs/[^/]+/(notion_done|notion_readback)\.json$")
PROTECTED = re.compile(r"^(input/|refs/|scripts/|tests/|\.claude/|rules\.yaml$|CLAUDE\.md$|runs/)")
BASH_WRITE = re.compile(r"(>|\btee\b|\bsed\s+-i|\bmv\b|\bcp\b|\brm\b|\btouch\b|\bperl\s+-i|python3?\s+-c|\bchmod\b|\bln\b)")
# 출력 버리기(>/dev/null)와 출력 합치기(2>&1)는 파일을 바꾸지 않으므로 검사 전에 지운다
HARMLESS_REDIRECT = re.compile(r"\d?>>?\s*(/dev/null\b|&\d)")
BASH_PROTECTED = re.compile(r"(input/|refs/|scripts/|tests/|\.claude/|rules\.yaml|CLAUDE\.md|runs/|state\.json|approval)")


def rel(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None  # 프로젝트 밖


def deny(role, tool, target, why):
    try:
        with open(ROOT / ".claude" / "guard.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')}\t{role}\t{tool}\t{target}\t{why}\n")
    except OSError:
        pass
    print(f"[하네스 가드] 차단: {why} (역할: {role}, 대상: {target})", file=sys.stderr)
    sys.exit(2)


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    role = data.get("agent_type") if data.get("agent_id") else "main"
    role = role or "main"
    if (ROOT / ".claude" / "harness-unlock").exists():
        sys.exit(0)

    if tool in EDIT_TOOLS:
        target = inp.get("file_path") or inp.get("notebook_path") or ""
        r = rel(target)
        if role in WRITER_ALLOW:
            if r is None or not WRITER_ALLOW[role].match(r):
                deny(role, tool, target, f"{role}는 자기 파일만 쓸 수 있습니다")
        elif role == "judge":
            deny(role, tool, target, "judge는 읽기 전용입니다")
        elif r is not None and PROTECTED.match(r) and not MAIN_ALLOW_IN_RUNS.match(r):
            deny(role, tool, target, "사람 몫이거나 스크립트가 쓰는 파일입니다")

    elif tool == "Bash":
        cmd = inp.get("command", "")
        if role == "judge":
            if not re.fullmatch(r"\s*python3 scripts/judge\.py (\S+ --gate G[235] --check|--selftest)\s*", cmd):
                deny(role, tool, cmd, "judge는 `judge.py ... --check`와 `--selftest`만 실행할 수 있습니다")
        elif role in WRITER_ALLOW:
            deny(role, tool, cmd, "writer는 Bash를 쓸 수 없습니다")
        else:
            is_script = re.fullmatch(r"\s*python3 scripts/\w+\.py[^;&|>`$]*", cmd)
            checked = HARMLESS_REDIRECT.sub(" ", cmd)
            if not is_script and BASH_WRITE.search(checked) and BASH_PROTECTED.search(checked):
                deny(role, tool, cmd, "보호된 파일을 셸로 바꾸려 했습니다. scripts/ 의 스크립트를 쓰세요")

    elif tool == "WebFetch":
        url = inp.get("url", "")
        if role == "hanja-writer" and not url.startswith("https://hanja.dict.naver.com/"):
            deny(role, tool, url, "hanja-writer는 네이버 한자사전만 조회합니다")
        if role in ("example-writer", "judge"):
            deny(role, tool, url, f"{role}는 웹을 조회하지 않습니다")

    sys.exit(0)


if __name__ == "__main__":
    main()
