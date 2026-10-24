#!/usr/bin/env python3
"""derive_manifest.py — build ancestry_manifest.json from the SOURCE, never by hand.

Walks the ancestor repository and records everything a catalogue could drop:
  - every cycle (both heading styles in the catalogue file + every routing-table row)
  - every state machine: states, trap/terminal states, transitions
  - every named composition
  - every working-set tag
Run:  python3 derive_manifest.py <source-repo-root> [out.json]
The source is https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1 (clone it and pass its root). Any
state machine present in fsms/atlas-fsms/ but not committed there is listed as added beside the source.
The output is data about the source; the lens catalogue never reads it as instructions.
"""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("ancestry_manifest.json")

# ---------- cycles from the catalogue file (two heading styles + routing table) ----------
atlas = (root / "ATLAS.md").read_text(encoding="utf-8")
cycles = {}
for m in re.finditer(r"^#{3,4} (.+?)\s*(?:—|\(|$)", atlas, re.M):
    heading = m.group(0)
    name = m.group(1).strip()
    tag = re.search(r"Tag: `([A-Za-z0-9\*/]+)`", heading)
    if tag or "Cycle" in heading or "Deep" in heading:
        cycles.setdefault(name, {"tags": set(), "source": "heading"})
        if tag:
            cycles[name]["tags"].add(tag.group(1))
for m in re.finditer(r"^\| ([^|]+?) \| ([^|]+?) \| [^|]*\| `([A-Z0-9\*]{1,5})` \| ([^|]+?) \|$", atlas, re.M):
    situation, cname, tag, guardian = (x.strip() for x in m.groups())
    cycles.setdefault(cname, {"tags": set(), "source": "routing"})
    cycles[cname]["tags"].add(tag)
    cycles[cname].setdefault("situations", []).append(situation)
for v in cycles.values():
    v["tags"] = sorted(v["tags"])

# ---------- working-set tags + named compositions from CYCLES.md ----------
cyc = (root / "CYCLES.md").read_text(encoding="utf-8")
working_set = re.findall(r"^## \d+\. `([A-Z0-9]+)` — (.+?) \(", cyc, re.M)
compositions = []
for m in re.finditer(r"^### `([A-Z0-9]+)` — (.+?) \((.+?)\)$", cyc, re.M):
    compositions.append({"tag": m.group(1), "name": m.group(2), "formula": m.group(3), "where": "CYCLES.md"})
# compositions named elsewhere: Guru Council, grand audits, drishti-stack precedents
for name, formula, where in [
    ("Guru Council", "ASD BUD GKD TLD OSD CKD PJD KBD ARD SSD SRD VKD NGD TVD", "ATLAS.md"),
    ("Nav Shakti Grand", "NS1..NS9", "ATLAS.md"),
    ("Dwaraka Grand", "AB* (8 queens)", "ATLAS.md"),
]:
    compositions.append({"tag": None, "name": name, "formula": formula, "where": where})
ds = (root / "DRISHTI_STACK.md").read_text(encoding="utf-8")
for m in re.finditer(r"^([A-Za-z][A-Za-z +→;:,\-]+→[A-Za-z +→;:,\-]+)$", ds, re.M):
    compositions.append({"tag": None, "name": "drishti stack precedent", "formula": m.group(1).strip(), "where": "DRISHTI_STACK.md"})

# ---------- state machines ----------
fsms = {}
for f in sorted((root / "fsms" / "atlas-fsms").glob("*Fsm.toml")):
    t = f.read_text(encoding="utf-8", errors="replace")
    states = []
    for m in re.finditer(r'\[\[states\]\]\s*\nname\s*=\s*"([^"]+)"\s*\ndescription\s*=\s*"([^"]*)"(.*?)(?=\n\[\[|\Z)', t, re.S):
        block = m.group(3)
        states.append({
            "name": m.group(1),
            "description": m.group(2)[:300],
            "initial": bool(re.search(r"is_initial\s*=\s*true", block)),
            "terminal": bool(re.search(r"is_terminal\s*=\s*true", block)),
            "trap": bool(re.search(r"trap|collapse|relapse|temptation|crisis|lost|error|bhaya|bhrama", m.group(1), re.I)),
        })
    transitions = re.findall(r'event\s*=\s*"([^"]+)"', t)
    fsms[f.stem.replace("Fsm", "")] = {"file": str(f.relative_to(root)), "states": states, "transitions": transitions}

def source_of(root):
    """Name the source by its repository and commit, not by a local path, and list any state
    machines present in the folder but not in that commit (ancestors added beside the source)."""
    import subprocess
    def git(*a):
        r = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    url = git("remote", "get-url", "origin")
    if not url:
        return {"repo": root.name}
    url = re.sub(r"\.git$", "", re.sub(r"https://[^@/]+@", "https://", url))
    added = sorted(git("ls-files", "--others", "--", "fsms/atlas-fsms").split())
    return {"repo": url, "commit": git("rev-parse", "HEAD"), "added_beside_source": added}

manifest = {
    "source": source_of(root),
    "cycles": cycles,
    "working_set": [{"tag": t, "name": n} for t, n in working_set],
    "compositions": compositions,
    "fsms": fsms,
}
out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"cycles={len(cycles)} working_set={len(working_set)} compositions={len(compositions)} fsms={len(fsms)} "
      f"states={sum(len(v['states']) for v in fsms.values())} traps={sum(s['trap'] or s['terminal'] for v in fsms.values() for s in v['states'])}")
