# workspace — the engine that maintains LENS.md

`LENS.md` at the root is the only file anyone needs to *use* a lens. This folder is what you need to *change* it: the rules for a change, the checks that fail on drift, and the record of where every lens came from.

## What is here

| File | What it is |
|---|---|
| `LENS_META.md` | The maintainer's half of the catalogue: the witness's claims (§5), the lifecycle and admission rules (§6), the change log and the ancestry ledger (§7). |
| `check_lens.py` | The witness. Reads `../LENS.md` with `LENS_META.md` and fails if any claim in §5 is false. |
| `check_lens_selftest.py` | Watches the witness: mutates a real line for each claim in a temp folder and confirms the witness fails on it. |
| `check_recall.py` | Advisory report: every ancestor state is either echoed in its own lens or dropped with a reason. |
| `statediff.py` | Which ancestor states changed fate between two versions of `LENS.md`. |
| `ancestry_manifest.json` | Derived record of what the source contained — cycles, state machines, compositions. Never edited by hand. |
| `derive_manifest.py` | Rebuilds the manifest from the source, [AI_WAY_OF_BUILDING_V1](https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1). |
| `adapters/claude-skills/` | Optional: two Claude skills that run lenses on that platform (`lens`, `reflex-check`). `LENS.md` itself names no vendor. |

## Check

Python 3, standard library only. From the repository root:

```
python3 workspace/check_lens.py            # LENS.md: OK — … lenses, … routes, claims 1–14, 16–20 hold
python3 workspace/check_lens_selftest.py   # selftest: OK
python3 workspace/check_recall.py          # states=… undecided=0
```

The scripts look for `LENS_META.md` and the manifest beside `LENS.md` first and in this folder second, so a flat copy of everything also works.

## Change a lens

1. Read `LENS_META.md` §6 — admission, merge, *read before deciding*, retirement.
2. Edit `../LENS.md` (the lens) and `LENS_META.md` (a §7 entry; ledger rows if an ancestor's fate moves).
3. Run the three checks above, plus the state diff against the previous version:
   `python3 workspace/statediff.py OLD_LENS.md LENS.md workspace/ancestry_manifest.json`
4. Release only when the witness and the self-test pass and recall shows zero undecided — or §7 says why not.

## Rebuild the ancestry

When the source changes, clone it and re-derive:

```
git clone https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1 v1
python3 workspace/derive_manifest.py v1          # writes workspace/ancestry_manifest.json
python3 workspace/check_lens.py                  # claim 8 fails until every new ancestor has a ledger row
```

*Catalogue version: see the first lines of `LENS.md`.*
