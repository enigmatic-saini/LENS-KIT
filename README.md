# LENS

**One file — [`LENS.md`](LENS.md) — that you drop into any project or any model's instructions.**

A lens adds no knowledge. It fixes which question is asked first, from where, in what order, and when to stop looking. The same lens steers a person or an AI model through a trust hierarchy, a test suite, a book chapter or a hiring plan without changing a word. The model or person brings the knowledge; the lens decides where to look from.

## Drop it in

`LENS.md` is self-contained, plain Markdown and names no vendor, so it works the same everywhere.

| Where | How |
|---|---|
| **A repository** | Copy `LENS.md` to the root, or to `docs/`. Point your contributors or your agent's instruction file at it. |
| **An AI assistant's custom instructions** (Copilot, ChatGPT, Claude, Gemini…) | Upload or paste `LENS.md` as a knowledge file or instruction, and add one line of introduction (below). |
| **A system prompt** | Paste the file, or the sections you need (§1 *How to use* plus the lenses you cite). |
| **A team, no AI at all** | Print §2 *Routing table*; run a lens in a review meeting by reading its *Look for* items aloud, in order. |

**A one-line introduction to put above it:**

> When I ask you to review, decide or plan, use LENS.md: pick the lens from §2 (start with `TRG` if unsure), walk its *Look for* items in order, mark each finding seen, told or guessed, stop when an exit fires, and give the result in the shape the lens produces.

Add your own context to that line if it helps, e.g. *"I am an enterprise security architect; most artefacts I bring are designs, policies and vendor proposals."*

## Use it

1. **Pick.** Find your situation in **§2** — five families: *Begin, See, Guard, Move, Hold*. Take its tag (`RR`, `SHD`, `ES`…). If nothing fits, start with **`TRG`** (Triage), which names the lens to use.
2. **Look.** Read that lens in **§3**. Walk every *Look for* item in its written order; for each, say what you see or "nothing seen".
3. **Tag what each finding rests on.** *seen* (in the thing itself), *told* (someone said so), *guessed*. A verdict rests on *seen* only.
4. **Stop on the exit.** Every lens names its exits — ask one thing more, re-aim, say nothing should be done, or no lens fits. When one fires, stop.
5. **Deliver what it produces** — each lens names the shape of its result, and nothing after it.

**Depth:** *glance* (first question and exits — does the lens apply?), *look* (default — every item), *deep* (every item, then re-aim once and look again).
**Combine:** write tags in order — `×` means look through both before concluding, `→` means the left result feeds the right. Named reading orders are in **§4**, e.g. `AHR × OE × VD × SHD → SMR` to compare two options and decide.
**Cite tags** in anything that persists; in conversation the lineage name is fine ("run the Radha lens").

A worked example — one lens, one artefact, stopping at its exit — is in §1 of `LENS.md`.

## Ask for it in words

- "Run `TRG` on this proposal, then the lens it names."
- "Look at this design through `SHD` and `NEG`, at *look* depth."
- "`ES` on our incident runbook — can it be stopped, and has that been tried?"
- "Run the Saraswati lens on this README."

## Changing the catalogue

Everything used to maintain `LENS.md` lives in [`workspace/`](workspace/): the maintainer's notes and change log (`LENS_META.md`), the checks that fail on drift, and the ancestry record. See [`workspace/README.md`](workspace/README.md). You never need that folder to *use* a lens.

The lenses descend from the review cycles of [AI_WAY_OF_BUILDING_V1](https://github.com/enigmatic-saini/AI_WAY_OF_BUILDING_V1).
