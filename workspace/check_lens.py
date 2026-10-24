#!/usr/bin/env python3
"""check_lens.py — the witness for LENS.md.

Verifies the claims in LENS_META.md §5 against LENS.md and LENS_META.md. Exit 0 when all
hold, 1 otherwise, printing every failure found. No dependencies beyond the standard
library. Run:  python3 workspace/check_lens.py [path/to/LENS.md]   (default: the LENS.md one level above the workspace)
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent   # the workspace: LENS_META.md, the manifest and the scripts live here


def beside(lens_path, name):
    """A maintainer's file: next to LENS.md if it is there (a flat copy, or the self-test's temp
    folder), else in the workspace beside this script (LENS-KIT's layout: LENS.md at the root)."""
    p = Path(lens_path).with_name(name)
    return p if p.exists() else HERE / name


def default_lens():
    return HERE.parent / "LENS.md" if (HERE.parent / "LENS.md").exists() else Path("LENS.md")

# Words that mark a single field of work. A lens section may not contain them.
# Extend only through a §7 change-log entry.
FIELD_WORDS = [
    r"\bcode\b", r"\bcodebase\b", r"\bcommit\b", r"\brepo\b", r"\brepository\b",
    r"\bdeploy\w*", r"\bserver\b", r"\bdatabase\b", r"\bAPI\b", r"\bbug\b",
    r"\bsprint\b", r"\bcloud\b", r"\bcompil\w*", r"\bcertificate\b", r"\bPKI\b",
    r"\bfirewall\b", r"\bcutover\b", r"\bmigration\b", r"\bsoftware\b",
    r"\bbook\b", r"\bchapter\b", r"\bhiring\b", r"\bcustomer\b", r"\bmarket\b",
    # 1.7 — the list had followed its writer's field; widened from what ITR found in the
    # bodies (one field) and with other fields' words. Not "patient"/"diagnosis": SSD's
    # surgical frame is decided (1.6).
    r"\binputs?\b", r"\boutputs?\b", r"\brequests?\b", r"\balgorithm\w*", r"\bencoding\b",
    r"\bdata\b", r"\blogs?\b", r"\btimeouts?\b", r"\bautomated\b",
    r"\binvoice\w*", r"\bcurriculum\b", r"\blesson plan\b", r"\bcourtroom\b", r"\bplaintiff\b",
    r"\bharvest\b", r"\bpayroll\b",
]

def section(text, header_regex, next_header_regex=r"^## "):
    m = re.search(header_regex, text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(next_header_regex, rest, re.M)
    return rest[: n.start()] if n else rest

VENDOR = r"\b(Claude|Anthropic|OpenAI|ChatGPT|GPT-\d\w*|Gemini|Bard|Llama|Mistral|Copilot|DeepSeek)\b|`[a-z][\w-]*` skill\b|\bthe skill (prints|'s shape)"

def main(path):
    # 2.0: the catalogue is two files — LENS.md (drop-in, §0–§4) and LENS_META.md beside it
    # (§5–§7). Every claim reads them as one text; claim 20 reads LENS.md alone.
    core = Path(path).read_text(encoding="utf-8")
    meta_path = beside(path, "LENS_META.md")
    meta = meta_path.read_text(encoding="utf-8") if meta_path.exists() else ""
    text = core + "\n\n" + meta
    failures = []
    # Claim 20 — the drop-in half holds only its front matter and §0–§4, points to the meta file,
    # and names no model vendor, product or tool-specific feature
    if not meta:
        failures.append("claim 20: LENS_META.md not found beside LENS.md or in the workspace")
    for h in re.findall(r"^## (§\d+)\.", core, re.M):
        if h not in ("§0", "§1", "§2", "§3", "§4"):
            failures.append(f"claim 20: LENS.md holds {h}; only §0–§4 belong in the drop-in half")
    if "LENS_META.md" not in core:
        failures.append("claim 20: LENS.md does not point to LENS_META.md")
    for m in re.finditer(VENDOR, core):
        failures.append(f"claim 20: LENS.md names '{m.group(0)}', which belongs to one vendor or tool")

    s2 = section(text, r"^## §2\.")
    s3 = section(text, r"^## §3\.")
    s4 = section(text, r"^## §4\.")
    s7 = section(text, r"^## §7\.")

    # Claim 1 — unique tags in §3
    s3_tags = re.findall(r"^### `([A-Z0-9]+)` — ", s3, re.M)
    dupes = sorted({t for t in s3_tags if s3_tags.count(t) > 1})
    if dupes:
        failures.append(f"claim 1: duplicate tags in §3: {dupes}")
    s3_set = set(s3_tags)

    # Claim 2 — §2 and §3 agree
    s2_tags = re.findall(r"\| `([A-Z0-9]+)` \|$", s2, re.M)
    for t in s2_tags:
        if t not in s3_set:
            failures.append(f"claim 2: §2 routes to `{t}` but §3 has no section")
    for t in s3_set:
        if t not in s2_tags:
            failures.append(f"claim 2: §3 defines `{t}` but §2 has no row")

    # Claim 3 — §4 tags exist
    s4_tags = set()
    for span in re.findall(r"`([^`]+)`", s4):
        s4_tags.update(re.findall(r"\b[A-Z][A-Z0-9]{1,3}\b", span))
    for t in sorted(s4_tags):
        if t not in s3_set:
            failures.append(f"claim 3: §4 cites `{t}` which is not in §3")

    # Claim 4 — no field words inside lens sections (lineage lines excepted:
    # ancestry may name a figure's trade; the lens itself may not)
    for block in re.split(r"^### ", s3, flags=re.M)[1:]:
        tag = block.split("`")[1] if "`" in block else "?"
        body = "\n".join(l for l in block.splitlines() if not l.startswith("- **Lineage:**"))
        for w in FIELD_WORDS:
            hit = re.search(w, body, re.I)
            if hit:
                failures.append(f"claim 4: `{tag}` contains field word '{hit.group(0)}'")

    # Claim 5 — no literal counts of lenses/tags/entries anywhere (small number
    # words are allowed: 'two lenses that ask one question are one lens' is a rule)
    for m in re.finditer(r"\b(\d+|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty)\s+(lenses|tags|entries|seats)\b", text, re.I):
        failures.append(f"claim 5: literal count '{m.group(0)}'")

    # Claim 7 — every tag cited inside a §3 section (tables, Pairs with) exists
    for block in re.split(r"^### ", s3, flags=re.M)[1:]:
        tag = block.split("`")[1] if "`" in block else "?"
        body = block.split("\n", 1)[1] if "\n" in block else ""
        for span in re.findall(r"`([^`]+)`", body):
            for t in re.findall(r"\b[A-Z][A-Z0-9]{1,3}\b", span):
                if t not in s3_set:
                    failures.append(f"claim 7: `{tag}` cites `{t}` which is not in §3")

    # Claims 8–11 — ancestry: manifest → ledger (silence is caught), carried states, compositions, recall
    import json, subprocess
    man_path = beside(path, "ancestry_manifest.json")
    ledger = section(text, r"^### Ancestry ledger", r"^### 0\.")
    rows = re.findall(r"^\| ([^|]+?) \| ((?:kept|folded|not carried)[^|]*?) \| ([^|]*?) \| ([^|]*?) \|$", ledger, re.M)
    names = [r[0].strip() for r in rows]
    for n in sorted({n for n in names if names.count(n) > 1}):
        failures.append(f"claim 8: ancestor '{n}' appears more than once in the ledger")
    def norm(x): return re.sub(r"[^a-z]", "", x.lower())
    if man_path.exists():
        man = json.loads(man_path.read_text(encoding="utf-8"))
        L = [norm(n) for n in names]
        # exact row first; otherwise the longest overlapping row name — and that row may serve
        # only one manifest ancestor, so a shorter name (Lakshman) cannot stand in for a longer
        # one (LakshmanaQueen) that has no row of its own.
        claimed = {}
        for fsm in man["fsms"]:
            k = norm(fsm)
            cands = [l for l in L if l == k] or sorted((l for l in L if k in l or l in k), key=len, reverse=True)
            if not cands:
                failures.append(f"claim 8: manifest ancestor '{fsm}' has no ledger row")
                continue
            row = cands[0]
            if row in claimed and claimed[row] != fsm:
                failures.append(f"claim 8: ledger row '{row}' is claimed by both '{claimed[row]}' and '{fsm}' — one of them has no row of its own")
            claimed[row] = fsm
        # and the other direction: every ledger row names an ancestor the manifest lists, unless it
        # says it is prose-only — so a row cannot outlive its source, or be typed for a machine the
        # source never had (the manifest is derived; the ledger is typed)
        for name, fate, carried, dropped in rows:
            l = norm(name)
            if "prose-only" in carried or "prose-only" in dropped:
                continue
            if l not in claimed and not any(k == l or k in l or l in k for k in (norm(f) for f in man["fsms"])):
                failures.append(f"claim 8: ledger row '{name.strip()}' names no ancestor in the manifest (and is not marked prose-only)")
        comp_sec = section(text, r"^#### Compositions", r"^### ")
        comp_names = [norm(x) for x in re.findall(r"^\| ([^|]+?) \|", comp_sec, re.M)]
        for comp in man["compositions"]:
            key = norm(comp["tag"] or comp["name"])
            if key and not any(key in c for c in comp_names):
                failures.append(f"claim 10: manifest composition '{comp['tag'] or comp['name']}' has no ledger row")
    else:
        failures.append("claim 8: ancestry_manifest.json not found beside LENS.md or in the workspace — run derive_manifest.py")
    for name, fate, carried, dropped in rows:
        for t in re.findall(r"`([A-Z0-9]+)`", fate):
            if t not in s3_set:
                failures.append(f"claim 8: ledger row '{name.strip()}' names `{t}` which is not in §3")
        if fate.strip().startswith(("kept", "folded")) and carried.strip() in ("", "—"):
            failures.append(f"claim 9: '{name.strip()}' is {fate.strip().split()[0]} but carries no state")
    # Claim 17 — every lens is named by a ledger fate: kept or folded into it. Existence is
    # derived for ancestors (claim 8); this makes it hold for lenses too — no lens may enter
    # on a lineage line that no ledger row, and so no manifest ancestor, stands behind (1.5a).
    fated = set()
    for name, fate, carried, dropped in rows:
        if fate.strip().startswith(("kept", "folded")):
            fated.update(re.findall(r"`([A-Z0-9]+)`", fate))
    for t in sorted(s3_set - fated):
        failures.append(f"claim 17: `{t}` is named by no ledger fate — a lens with no recorded ancestor")
    # claim 11 is advisory: run the recall report so it is seen at every release
    rc = beside(path, "check_recall.py")
    if rc.exists() and man_path.exists():
        r = subprocess.run([sys.executable, "-I", str(rc), str(path), str(man_path)], capture_output=True, text=True)
        print("recall:", r.stdout.splitlines()[0] if r.stdout else "(no output)")

    # Claim 12 — every §4 row names what it ends in (fourth column non-empty)
    s4_rows = re.findall(r"^\| ([^|]+?) \| [^|]+ \| [^|]+ \| ([^|]*?) \|$", s4, re.M)
    if not s4_rows:
        failures.append("claim 12: §4 table has no 'Ends in' column")
    for name, ends in s4_rows:
        if name.strip() in ("Name", "---") or set(name.strip()) <= set("-"):
            continue
        if not ends.strip() or ends.strip() == "—":
            failures.append(f"claim 12: composition '{name.strip()}' names nothing it ends in")

    # Claim 13 — every lens carries an Exits line, and it names at least one real stop:
    # a hand-over to an existing tag, or one of the four stated exits.
    EXIT_WORDS = ("ask one thing more", "re-aim", "no lens fits", "nothing should be done", "do nothing", "verdict", "say so")
    for block in re.split(r"^### ", s3, flags=re.M)[1:]:
        tag = block.split("`")[1] if "`" in block else "?"
        m = re.search(r"^- \*\*Exits:\*\* (.+)$", block, re.M)
        if not m:
            failures.append(f"claim 13: `{tag}` has no Exits line")
            continue
        line = m.group(1)
        tags_ok = all(t in s3_set for t in re.findall(r"`([A-Z0-9]{2,4})`", line))
        words_ok = any(w in line.lower() for w in EXIT_WORDS) or re.search(r"`[A-Z0-9]{2,4}`", line)
        if not tags_ok or not words_ok:
            failures.append(f"claim 13: `{tag}` Exits line names no real stop or cites a missing tag")

    # Claim 14 — retired tags are never reused; the §7 "Retired tags" line is the one
    # place a retired tag may be written (claim 6 exempts it)
    retired_line = re.search(r"^\*\*Retired tags[^\n]*$", s7, re.M)
    retired = set(re.findall(r"`([A-Z0-9]+)`", retired_line.group(0))) if retired_line else set()
    for t in sorted(retired & s3_set):
        failures.append(f"claim 14: retired tag `{t}` is in use in §3")
    s7_body = s7.replace(retired_line.group(0), "") if retired_line else s7
    # Claim 6 — every folded lineage in §7 names an existing tag
    for t in set(re.findall(r"`([A-Z0-9]+)`", s7_body)):
        if t not in s3_set:
            failures.append(f"claim 6: §7 refers to `{t}` which is not in §3")

    # Claim 18 — §1's worked example still shows the lens it cites: the §2 situation it
    # quotes is that lens's row, every line it walks begins an item of that lens's Look for,
    # and its exit is one of that lens's exits (1.9: the example drifted silently in 1.6).
    def nz(x): return re.sub(r"[^a-z ]", "", re.sub(r"[*`]", "", x.lower())).split()
    # §1 holds a fenced example whose own "## " line would end section() early: slice to §2
    s1 = text[text.index("## §1."):text.index("## §2.")] if "## §1." in text and "## §2." in text else ""
    ex = re.search(r"```\n(.*?)```", s1, re.S)
    if not ex:
        failures.append("claim 18: §1 has no worked example")
    else:
        body = ex.group(1)
        mt = re.search(r"^## `([A-Z0-9]+)` — ", body, re.M)
        quote = re.search(r"§2 says \*([^*]+)\* → `([A-Z0-9]+)`", s1)
        if not mt or not quote:
            failures.append("claim 18: §1's worked example names no lens or no §2 situation")
        else:
            t = mt.group(1)
            rowtxt = [r for r in re.findall(r"^\| ([^|]+?) \| `([A-Z0-9]+)` \|$", s2, re.M) if r[1] == t]
            if quote.group(2) != t or not rowtxt or nz(rowtxt[0][0]) != nz(quote.group(1)):
                failures.append(f"claim 18: §1's example quotes §2 for `{t}` in words its row does not have")
            blk = [b for b in re.split(r"^### ", s3, flags=re.M)[1:] if b.startswith("`" + t + "`")]
            if blk:
                lf = re.search(r"^- \*\*Look for:\*\* (.+)$", blk[0], re.M).group(1)
                items = [" ".join(nz(i)) for i in lf.split(" · ")]
                exits = " ".join(nz(re.search(r"^- \*\*Exits:\*\* (.+)$", blk[0], re.M).group(1)))
                for line in body.split("\n"):
                    if not line.strip() or line.startswith(("Depth", "## ", "Produces", "  ")):
                        continue
                    if line.startswith("Exit fired:"):
                        e = " ".join(nz(line.split(":", 1)[1]))
                        if e not in exits:
                            failures.append(f"claim 18: §1's example fires an exit `{t}` does not have")
                        continue
                    label = " ".join(nz(line.split(" — ")[0]))
                    if not any(i.startswith(label) for i in items):
                        failures.append(f"claim 18: §1's example walks '{line.split(' — ')[0][:50]}', which begins no item of `{t}`")
    # Claim 19 — a lineage name opens one lens: where the first figure named in two or more
    # Lineage lines is the same, §1 must name the scene for each of those tags (1.9).
    leads = {}
    for b in re.split(r"^### ", s3, flags=re.M)[1:]:
        t = b.split("`")[1]
        m = re.search(r"^- \*\*Lineage:\*\* (?:the )?([A-Z][\w\u0100-\u024f\u1e00-\u1eff]+)", b, re.M)
        if m:
            leads.setdefault(re.sub(r"'s$", "", m.group(1)), []).append(t)
    for name, ts in leads.items():
        if len(ts) > 1:
            line = [l for l in s1.split("\n") if name in l]
            if not line or not all(f"`{t}`" in line[0] for t in ts):
                failures.append(f"claim 19: lineage '{name}' opens {ts} but §1 does not name the scene for each")
    # Claim 16 — the state line is read, not asserted: any state other than BORN
    # requires §7 to name at least one LOOK_ record made on an artefact outside the kit
    state = re.search(r"^state:\s*(\w+)", text, re.M)
    if state and state.group(1) != "BORN" and not re.search(r"LOOK_\d{4}-\d{2}-\d{2}_[A-Z0-9]+_", s7):
        failures.append(f"claim 16: state is {state.group(1)} but §7 names no LOOK_ record outside the kit")

    if failures:
        print("LENS.md: FAIL")
        for f in failures:
            print("  -", f)
        return 1
    print(f"LENS.md: OK — {len(s3_set)} lenses, {len(s2_tags)} routes, claims 1–14, 16–20 hold")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_lens()))
