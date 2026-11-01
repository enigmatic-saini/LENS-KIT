# LENS

**One file — [`LENS.md`](LENS.md) — a catalogue of lenses for reviewing anything, for people and models.**

A lens adds no knowledge. It fixes where to look from, which question is asked first, in what order, and when to stop looking. The reasoning stays with whoever holds it — a person, or any model. The same lens serves a trust hierarchy, a test suite, a book chapter or a hiring plan without changing a word, because it holds nothing that belongs to any of them.

## Drop it in

`LENS.md` is one self-contained Markdown file. It names no vendor, carries nothing a maintainer needs, and reads the same everywhere: nine rules, one worked example, a routing table, the lenses, and the named reading orders.

| Where | How |
|---|---|
| **A chat** | Attach the file, or paste it, and say which lens to run. |
| **An assistant's custom instructions** (Copilot, ChatGPT, Claude, Gemini…) | Upload it as a knowledge file or paste it as an instruction, with the one line below above it. |
| **A system prompt** | Paste the whole file, or §1 plus the lenses you cite. |
| **A repository** | Copy it to the root or to `docs/` and point your contributors or your agent's instruction file at it. |
| **A team, no AI at all** | Print §2. Run a lens in a review by reading its *Look for* items aloud, in order. |

**The one line to put above it:**

> When I ask you to review, decide or plan, use LENS.md: pick the lens from §2 (start with `TRG` if unsure), walk its *Look for* items in order, mark each finding seen, told or guessed, stop when an exit fires, and give the result in the shape the lens produces.

Add your own context to that line if it helps, e.g. *"Most artefacts I bring are designs, policies and vendor proposals."*

## Use it

1. **Pick.** Find your situation in **§2** — five families: *Begin, See, Guard, Move, Hold*. Take its tag (`RR`, `SHD`, `ES`…). If nothing fits, start with **`TRG`**, which names the lens to use.
2. **Look.** Read that lens in **§3**. Walk every *Look for* item in its written order; for each, say what you see or "nothing seen".
3. **Mark what each finding rests on.** *seen* (in the thing itself), *told* (someone said so), *guessed*. A verdict rests on *seen* only.
4. **Stop on the exit.** Every lens names its exits. When one fires, stop.
5. **Deliver what it produces** — each lens names the shape of its result.

**Depth:** *glance* (first question and exits — does the lens apply?), *look* (default — every item), *deep* (every item, then re-aim once and look again).
**Combine:** write tags in order — `×` means look through both before concluding, `→` means the left result feeds the right. Named reading orders are in **§4**, e.g. `AHR × OE × VD × SHD → SMR` to compare two options and decide.
**Record:** a kept look holds four things — the depth, each item with what was seen and what it rests on, the exit, what the lens produces. §1's worked example shows one way to write it; the layout is yours.
**Name it:** cite the tag in anything that persists; in conversation the lineage name is fine ("run the Radha lens").

## Ask for it in words

- "Run `TRG` on this proposal, then the lens it names."
- "Look at this design through `SHD` and `NEG`, at *look* depth."
- "`ES` on our incident runbook — can it be stopped, and has that been tried?"
- "Run the Saraswati lens on this README."
- "Run the Adversaries order on this plan."

## Changing the catalogue

Everything used to maintain `LENS.md` lives in [`workspace/`](workspace/): the maintainer's notes, change log and charter (`LENS_META.md`), the checks that fail on drift, and the ancestry record. See [`workspace/README.md`](workspace/README.md). You never need that folder to *use* a lens.

The lenses descend from the review cycles of [AI_WAY_OF_BUILDING_V1](https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1).
