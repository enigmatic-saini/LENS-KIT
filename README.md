# LENS Kit

A lens adds no knowledge. It fixes which question is asked first, from where, in what order — and when to stop looking. The same lens steers a person or a model through a trust hierarchy, a test suite, a book chapter or a hiring plan without changing a word.

## What is here

| File | What it is |
|---|---|
| `LENS.md` | **The catalogue** — the only file a reader needs. Drop it into any project and any model's instructions. Holds the charter (§0), how to use it (§1), the routing table (§2), every lens (§3) and the named compositions (§4). |
| `LENS_META.md` | The maintainer's half: the witness's claims (§5), lifecycle and admission rules (§6), the change log and the ancestry ledger (§7). Not needed to *run* a lens. |
| `check_lens.py` | The witness. Checks both files against the claims in §5 and fails on drift. |
| `check_lens_selftest.py` | Watches the witness: mutates a real line for each claim and confirms the witness fails on it. |
| `check_recall.py` | Advisory report: every ancestor state is either echoed in its own lens or dropped with a reason. |
| `statediff.py` | Shows which ancestor states changed fate between two versions of `LENS.md`. |
| `ancestry_manifest.json` | Derived record of what the source kit contained (cycles, state machines, compositions). Produced by `derive_manifest.py`, never edited by hand. |
| `derive_manifest.py` | Rebuilds the manifest from the source kit when the ancestry changes. |
| `adapters/claude-skills/` | Optional: two Claude skills that run lenses on that platform (`lens`, `reflex-check`). `LENS.md` itself names no vendor. |

## Use

Pick a situation in §2 of `LENS.md`, take its tag, and look through that lens in §3. If no row fits, start with `TRG`. Cite tags in anything that persists.

## Check

Python 3, standard library only. Keep the files side by side.

```
python3 check_lens.py LENS.md          # LENS.md: OK — 46 lenses, 46 routes, claims 1–14, 16–20 hold
python3 check_lens_selftest.py LENS.md # selftest: OK
python3 check_recall.py LENS.md ancestry_manifest.json
```

## Change

A change to a lens follows `LENS_META.md` §6 and is logged in §7; run all three checks before it is released.

*Version 2.1.*
