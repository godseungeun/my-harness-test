"""하네스 공용 함수: 규칙 읽기, 경로, 상태 파일, 대조 데이터."""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


# ---------- rules.yaml (PyYAML 없이 읽는 작은 파서) ----------

def _strip_comment(line):
    out, quote = [], None
    for ch in line:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#":
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        items, buf, quote = [], "", None
        for ch in text[1:-1]:
            if quote:
                buf += ch
                if ch == quote:
                    quote = None
            elif ch in "'\"":
                quote = ch
                buf += ch
            elif ch == ",":
                items.append(buf)
                buf = ""
            else:
                buf += ch
        if buf.strip():
            items.append(buf)
        return [_scalar(i) for i in items]
    if text in ("true", "false"):
        return text == "true"
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def load_rules(path=None):
    path = Path(path or ROOT / "rules.yaml")
    rules, section = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        if not line.strip():
            continue
        key, _, value = line.strip().partition(":")
        if not line.startswith(" "):
            section = rules.setdefault(key, {})
        else:
            section[key] = _scalar(value)
    return rules


# ---------- 배치 ----------

def parse_batch_id(batch_id, rules):
    m = re.fullmatch(r"(.+)-(\d{2})", batch_id)
    if not m or m.group(1) not in rules["batch"]["grades"]:
        die(f"배치 ID 형식이 틀렸습니다: {batch_id} (예: 8급-01, 급수는 {rules['batch']['grades']})")
    return m.group(1), int(m.group(2))


def batch_dir(batch_id):
    return RUNS / batch_id


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state(batch_id):
    path = batch_dir(batch_id) / "state.json"
    if not path.exists():
        die(f"{path} 가 없습니다. 먼저 S1(make_list.py)을 실행하세요.")
    return read_json(path)


def save_state(batch_id, state):
    write_json(batch_dir(batch_id) / "state.json", state)


def new_entry():
    return {"stage": "S2", "status": "pending", "retries": 0, "total_retries": 0,
            "reasons": [], "flags": [], "ever_needs_human": False, "rejected": 0, "s5_attempts": 0}


# ---------- 대조 데이터 ----------

_UNIHAN = None


def unihan():
    """{'弟': {'radical': '弓', 'strokes': {7}}} 형태."""
    global _UNIHAN
    if _UNIHAN is None:
        path = ROOT / "refs" / "unihan-rs-strokes.txt"
        if not path.exists():
            die(f"{path} 가 없습니다.")
        data = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            code, field, value = line.split("\t")
            ch = chr(int(code[2:], 16))
            entry = data.setdefault(ch, {})
            if field == "kRSUnicode":
                num = int(value.split()[0].split(".")[0].rstrip("'"))
                entry["radical"] = unicodedata.normalize("NFKC", chr(0x2F00 + num - 1))
            elif field == "kTotalStrokes":
                entry["strokes"] = {int(v) for v in value.split()}
        _UNIHAN = data
    return _UNIHAN


def load_word_list(path):
    path = ROOT / path if not Path(path).is_absolute() else Path(path)
    if not path.exists():
        return None
    words = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        first = line.split(",")[0].strip()
        if first and not first.startswith("#"):
            words.add(first)
    return words


def load_banned_names(rules):
    path = ROOT / rules["forbidden"]["names_file"]
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def forbidden_hits(text, rules, banned_names=()):
    hits = []
    lower = text.lower()
    for word in list(rules["forbidden"]["words"]) + list(banned_names):
        if word.lower() in lower:
            hits.append(f"forbidden:{word}")
    for pattern in rules["forbidden"]["patterns"]:
        if re.search(pattern, text):
            hits.append(f"forbidden:/{pattern}/")
    return hits
