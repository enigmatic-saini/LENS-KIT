#!/usr/bin/env python3
"""check_recall.py — advisory: is every ancestor state either decided (dropped with a reason in the
ledger) or echoed IN THE LENS ITS ROW NAMES?

For every state in ancestry_manifest.json: if its ledger row names it as dropped, it is decided.
Otherwise the state's content words must echo in the text of the lens(es) the row's fate cites —
not in §3 at large (echo on borrowed words from other lenses proved nothing: 1.1). A state echoes
when at least three of its content words, or a quarter of them, appear in that lens. Exit code is
always 0: this report informs the ledger; it does not gate.
Run:  python3 check_recall.py [LENS.md] [manifest.json]
"""
import json, re, sys
from pathlib import Path


def classify(lens_path, man_path):
    """Return ({(ancestor, state): 'echoed'|'decided'|'undecided'}, per-ancestor tags)."""
    text = Path(lens_path).read_text(encoding="utf-8")
    meta = Path(lens_path).with_name("LENS_META.md")
    if "### Ancestry ledger" not in text and meta.exists():   # 2.0: the ledger lives beside
        text += "\n\n" + meta.read_text(encoding="utf-8")
    s3 = text[text.index("## §3."):text.index("## §4.")]
    blocks = {b.split("`")[1]: set(re.findall(r"[a-z]{4,}", b.lower())) for b in re.split(r"^### ", s3, flags=re.M)[1:]}
    man = json.loads(Path(man_path).read_text(encoding="utf-8"))
    ledger_sec = text[text.index("### Ancestry ledger"):] if "### Ancestry ledger" in text else ""
    rows = {}
    for name, fate, carried, dropped in re.findall(r"^\| ([^|]+?) \| ((?:kept|folded|not carried)[^|]*?) \| ([^|]*?) \| ([^|]*?) \|$", ledger_sec, re.M):
        names = set(re.findall(r"\b[A-Z][A-Za-z_āṛṇṣ]+\b", dropped.split("—")[0]) if "—" in dropped else [])
        if dropped.strip().startswith("all states"):
            names = {"*"}
        rows[re.sub(r"[^a-z]", "", name.lower())] = (set(re.findall(r"`([A-Z0-9]+)`", fate)), names)
    out, tags_of = {}, {}
    for name, fsm in sorted(man["fsms"].items()):
        key = re.sub(r"[^a-z]", "", name.lower())
        cands = [k for k in rows if k == key] or sorted((k for k in rows if k in key or key in k), key=len, reverse=True)
        tags, dd = rows[cands[0]] if cands else (set(), set())
        tags_of[name] = sorted(tags)
        lw = set().union(*(blocks.get(t, set()) for t in tags)) if tags else set()
        for st in fsm["states"]:
            if "*" in dd or st["name"] in dd:
                out[(name, st["name"])] = "decided"; continue
            w = words(st["name"].replace("_", " ") + " " + st["description"])
            hit = w & lw
            out[(name, st["name"])] = "echoed" if w and (len(hit) >= 3 or len(hit) / len(w) >= 0.25) else "undecided"
    return out, tags_of, man

STOP = set("""the and that this with from into what when which where there their they them then than
have has had been being were was are for not but can could would should will may might must
each every some more most less very also only just like into over under about after before
state system cycle cycles phase round rounds engineering code creative work your you our its
his her she him who whom whose been does did done make made making thing things
here there without cannot never always itself something anything""".split())

def words(s):
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOP}

if __name__ == "__main__":
    lens_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("LENS.md")
    man_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("ancestry_manifest.json")
    out, tags_of, man = classify(lens_path, man_path)
    total = len(out); echoed = sum(v == "echoed" for v in out.values()); decided = sum(v == "decided" for v in out.values())
    print(f"states={total} echoed-in-own-lens={echoed} decided-dropped={decided} undecided={total-echoed-decided}   ('!' = trap/terminal state)")
    for name, fsm in sorted(man["fsms"].items()):
        missing = [("!" if (st["trap"] or st["terminal"]) else " ") + st["name"] for st in fsm["states"] if out[(name, st["name"])] == "undecided"]
        if missing:
            print(f"- {name} → {' '.join(tags_of[name]) or '(no tag)'} ({len(missing)}/{len(fsm['states'])} no echo): " + ", ".join(missing))
