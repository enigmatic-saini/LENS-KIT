# LENS

**One file — [`LENS.md`](LENS.md) — a catalogue of lenses for reviewing, deciding and planning anything, for people and models.**

A lens adds no knowledge. It fixes where to look from, which question comes first, in what order, and when to stop. The thinking stays with whoever holds it. The file is written so that one lens reads the same on a trust hierarchy, a test suite, a book chapter or a hiring plan; it names no vendor and carries nothing a maintainer needs.

## Drop it in, say the lens, read the look

Put this line in your assistant's instructions, or at the top of a chat, and attach or paste `LENS.md` under it:

> When I ask you to review, decide or plan, use LENS.md: pick the lens from §2 (start with `TRG` if unsure), walk its *Look for* items in order, mark each finding seen, told or guessed, stop when an exit fires, and give the result in the shape the lens produces.

Then ask in words:

- "Run `TRG` on this proposal, then the lens it names."
- "Look at this design through `SHD` and `NEG`, at *look* depth."
- "`ES` on our incident runbook — can it be stopped, and has that been tried?"
- "Run the Saraswati lens on this README."
- "Run the Adversaries order on this plan."

## What comes back

This is what a fresh session returned, given only `LENS.md`, the line above, and *"Run the Saraswati lens on this README"* — the previous version of this page:

```
Depth: look

## `SRD` — Front page
the polluted page — "Print §2. Run a lens by reading its Look for items
  aloud": §2 is the routing table; the Look for items are in §3. A team
  printing §2 alone has nothing to read aloud [seen]
one reader — the person dropping the file in, held throughout [seen]
a working example for every concept — none on this page. A newcomer never
  sees what a look produces [seen]
Exit fired: a concept has no working example → the result of a look is not
  yet taught; that is the finding.
Produces: fix "Print §2" → "§2 to choose, §3 to run"; show four lines of a
  finished look under the instructions.
```

Both corrections are on this page now. A look names where it stood, walks the lens's items in order, says what each finding rests on, stops at the first exit, and ends in the shape that lens produces. `LENS.md` §1 holds the full rules and a complete worked record; the layout of a record is yours, its four parts are not.

## Where it goes

| Where | How |
|---|---|
| **A chat** | Attach the file, or paste it, with the line above. |
| **An assistant's custom instructions** | Upload it as a knowledge file, or paste it, with the line above. |
| **A system prompt** | Paste the whole file, or §1 plus the lenses you cite. |
| **A repository** | Copy it to the root or to `docs/`; point your contributors or your agent's instruction file at it. |
| **A team, no AI at all** | Print §2 to choose a lens and §3 to run it: read its *Look for* items aloud, in order, and stop at the exit. |

## Changing the catalogue

Everything used to maintain `LENS.md` lives in [`workspace/`](workspace/): the maintainer's notes, change log and charter (`LENS_META.md`), the checks that fail on drift, and the ancestry record. You never need that folder to use a lens. The lenses descend from the review cycles of [AI_WAY_OF_BUILDING_V1](https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1).
