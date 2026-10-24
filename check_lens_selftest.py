#!/usr/bin/env python3
"""check_lens_selftest.py — who watches the watcher.

Mutates a *real* row or line of LENS.md in a temp folder (with the manifest and recall script
beside it) and asserts that check_lens.py fails on the intended claim. Exit 0 when every case
fires on its claim; 1 otherwise. Run beside LENS.md:  python3 check_lens_selftest.py [LENS.md]
"""
import re, shutil, subprocess, sys, tempfile
from pathlib import Path

here = Path(sys.argv[1]).resolve().parent if len(sys.argv) > 1 else Path(".").resolve()
core_src = (here / (Path(sys.argv[1]).name if len(sys.argv) > 1 else "LENS.md")).read_text(encoding="utf-8")
# 2.0: the catalogue is two files; cases mutate the joined text, which is split back at the marker
SPLIT = "\n\n<<<LENS_META>>>\n\n"
meta_src = (here / "LENS_META.md").read_text(encoding="utf-8") if (here / "LENS_META.md").exists() else ""
src = core_src + SPLIT + meta_src

def first_line(pattern):
    m = re.search(pattern, src, re.M)
    assert m, pattern
    return m.group(0)

def row(prefix):
    return first_line(r"^\| " + re.escape(prefix) + r" \|[^\n]*$")

cases = [
    # (claim, description, mutate(text) -> text)
    ("claim 1",  "duplicate tag in §3",          lambda t: t.replace("### `OE` — Rent", "### `RR` — Rent", 1)),
    ("claim 2",  "orphan §2 route",              lambda t: t.replace(first_line(r"^\| [^|]+ \| `LKM` \|$"), "", 1)),
    ("claim 3",  "§4 cites a missing tag",       lambda t: t.replace("`AND × NEG × RDY`", "`AND × NEG × ZZZ`", 1)),
    ("claim 4",  "field word in a lens body",    lambda t: t.replace("- **Asks:** Is the ground solid before anything is built on it?", "- **Asks:** Is the codebase ground solid before anything is built on it?", 1)),
    ("claim 4",  "another field's word (1.7)", lambda t: t.replace("- **Asks:** Is the ground solid before anything is built on it?", "- **Asks:** Is the ground solid before the invoice is built on it?", 1)),
    ("claim 5",  "literal count",                lambda t: t.replace("## §0. Charter", "## §0. Charter\n\nThere are forty lenses here.", 1)),
    ("claim 6",  "retired tag backticked in §7", lambda t: t.replace("become words: NS1 → `FND`", "become words: `NS1` → `FND`", 1)),
    ("claim 7",  "lens cites a missing tag",     lambda t: t.replace("hand to `SR` for watching", "hand to `SRX` for watching", 1)),
    ("claim 8",  "ancestor with no ledger row",  lambda t: t.replace(row("Raktabija"), "", 1)),
    ("claim 8",  "shorter name shadows longer",  lambda t: t.replace(row("Lakshmana (queen)"), "", 1)),
    ("claim 8",  "row with no ancestor",         lambda t: t.replace(row("Raktabija"), row("Raktabija") + "\n" + row("Raktabija").replace("| Raktabija |", "| Ghost machine |", 1), 1)),
    ("claim 9",  "kept row carries nothing",     lambda t: t.replace(row("Sushruta"), " | ".join(c if i != 2 else "—" for i, c in enumerate(row("Sushruta").split(" | "))), 1)),
    ("claim 10", "composition with no row",      lambda t: t.replace(first_line(r"^\| T4R Ratification[^\n]*$"), "", 1)),
    ("claim 12", "composition ends in nothing",  lambda t: t.replace("| one decision record from `SMR` |", "| — |", 1)),
    ("claim 13", "Exits line names no stop",     lambda t: re.sub(r"^- \*\*Exits:\*\* \*the count rises with effort\*.*$", "- **Exits:** nothing real", t, count=1, flags=re.M)),
    ("claim 13", "Exits line missing",           lambda t: re.sub(r"^- \*\*Exits:\*\* \*the symptom cannot be classified\*.*\n", "", t, count=1, flags=re.M)),
    ("claim 14", "retired tag reused",           lambda t: t.replace("`FND`", "`NS1`")),
    ("claim 17", "lens with no ledger ancestor", lambda t: t.replace("## §4. Compositions", "### `ZZQ` — Ghost lens\n\n- **Lineage:** none recorded.\n- **Asks:** What is here?\n- **Look for:** what is here.\n- **Exits:** otherwise the verdict.\n- **Produces:** a list.\n\n## §4. Compositions", 1).replace(first_line(r"^\| [^|]+ \| `LKM` \|$"), first_line(r"^\| [^|]+ \| `LKM` \|$") + "\n| Is there a ghost? | `ZZQ` |", 1)),
    ("claim 18", "worked example walks an item its lens lacks", lambda t: t.replace("proportion — ten minutes for three items", "balance — ten minutes for three items", 1)),
    ("claim 18", "worked example quotes a stale §2 row", lambda t: t.replace("§2 says *", "§2 says *Plainly, ", 1)),
    ("claim 19", "shared lineage with no scene named", lambda t: t.replace("Mira in the court is `MIR`", "Mira in the court is the rebel", 1)),
    ("claim 20", "a vendor named in the drop-in half", lambda t: t.replace("- **Lineage:** the LLM reviewer who wrote", "- **Lineage:** Claude, the LLM reviewer who wrote", 1)),
    ("claim 20", "a maintainer's section back in the drop-in half", lambda t: t.replace("## Kept with this file", "## §5. Witness notes\n\n## Kept with this file", 1)),
    ("claim 16", "state advanced with no LOOK",   lambda t: re.sub(r"LOOK_\d{4}-\d{2}-\d{2}_[A-Z0-9]+_", "LOOK-", t)),
]

bad = 0
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    for f in ("ancestry_manifest.json", "check_recall.py", "check_lens.py"):
        shutil.copy(here / f, d / f)
    for claim, desc, mut in cases:
        mutated = mut(src)
        if mutated == src:
            print(f"  ?? {claim} ({desc}): mutation did not apply"); bad += 1; continue
        core_m, _, meta_m = mutated.partition(SPLIT)
        (d / "LENS.md").write_text(core_m, encoding="utf-8")
        (d / "LENS_META.md").write_text(meta_m, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", str(d / "check_lens.py"), str(d / "LENS.md")], capture_output=True, text=True)
        fired = claim + ":" in r.stdout
        print(f"  {'ok' if fired else '!!'} {claim} ({desc})")
        if not fired:
            bad += 1
print("selftest:", "OK" if not bad else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
