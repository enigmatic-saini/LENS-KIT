---
name: "lens"
description: "Run a lens, a lineage (Radha, Kabir, Khatu Shyam…) or a composition from LENS.md on an artefact; use when the user says run/use/apply a lens, the appropriate lens, or a combination."
---

# lens

A lens adds no knowledge; it fixes which question is asked first, from where, in what order, and when to stop. LENS.md is the only definition of any lens. Since LENS.md 2.0 the file carries its own rules for running a lens and its own record shape (§1); this skill follows them on this platform and adds nothing to them. LENS_META.md (the witness, lifecycle, change log and ancestry ledger) is the maintainer's half and is not needed to run a lens.

## 0. Precondition

LENS.md must be in context — attached, a project doc, or pasted. If it is not, ask for it and stop. Never reconstruct, summarise or extend a lens from memory; a lens that is not in the file does not exist.

## 1. Route

- If the request names a lens by tag or by lineage name ("Radha", "Kabir", "Khatu Shyam"), use that lens. A lineage name opens the lens whose Lineage line it begins; where one figure opens two, §1 of LENS.md names the scene (Mira in the palace or in the court; Shiva's third eye, or the same eye on the boundary) — use the scene, and ask once if the request does not say which. Resolve silently otherwise.
- Otherwise run `TRG` first and show its verdict — *Primary / Follow-up / Mission* — then look through the primary lens. Do not start a follow-up until the primary's exit has fired.
- "Run the appropriate lens or combination" means: `TRG`, then obey its verdict.
- A named composition (§4) is a reading order: run its lenses left to right; `×` means look through both before concluding, `→` means the left result feeds the right. It ends in the one thing its *Ends in* column names.
- Escalate, then consolidate: one lens; if it cannot settle the matter, a pair; then four; only then the whole table. End with one consolidated verdict, not a pile of findings.

## 2. Depth

State the depth at the top of every look. If the person did not say, use *look*.

- **glance** — the lens's first question and its exits only. Says whether the lens applies. Produces no verdict.
- **look** (default) — every Look-for item in its written order.
- **deep** — every item; then re-aim once from what was found and walk the items again.

## 3. Look

- Walk the lens's **Look for** items in their written order. For each, say what you see or say "nothing seen". Never skip an item because it seems irrelevant — that is itself a finding.
- Every finding carries the tag, the Look-for item that surfaced it, and what it rests on:
  - `[seen]` — evidence in the artefact itself
  - `[told]` — someone said so; not checked in the artefact
  - `[guessed]` — inference with no evidence either way
  A verdict may rest on `[seen]` findings only. `[told]` and `[guessed]` are reported, never counted. A seeing on record — a reading made earlier and not repeated — names that record and counts only as far as it held; what the looking brought rather than the thing is `[guessed]`.
- A finding you cannot trace to a line of the lens is yours, not the lens's: mark it `(mine)` or drop it.
- Use only words the artefact shares with every other artefact. If you reach for a term that belongs to one field, the lens is leaking — reword.
- Stop when the lens's exit fires and name the exit: *ask one thing more* / *re-aim* / *nothing should be done* / *no lens fits*. Do not keep looking because you have more to say. If no exit fired, you are not done.
- Deliver the **Produces** artefact in the shape the lens names, and nothing after it. No advice, no next steps, unless a lens asked for them.

## 4. Stance

- You are not the doer; the lens is. Say "`SHD` sees…", not "I think…". Reverse without defending when a better lens sees differently.
- Non-doership is not non-responsibility: a wrong look is yours to repair, and you say so.
- When a stack is declared (`active → authority → intent ; consult: …`), the active lens looks hardest, the authority sets the rules, the intent is what the result must serve, consults are heard, not obeyed.

## 5. Output shape

The record's shape is LENS.md §1's; this is it, printed. It is also the shape of a kept record, saved as `LOOK_<date>_<tag>_<topic>.md` when the person wants the look to outlive the conversation.

```
Depth: glance | look | deep
TRG verdict (if routed): Primary · Follow-up · Mission

## `TAG` — Name
<Look for item 1> — <seen / nothing seen> [seen|told|guessed]
…
Exit fired: <which>
Produces: <artefact in the shape the lens names; rests on [seen] only>

(repeat per lens in the order run)

Ends in: <the one thing the composition names>   (only if more than one lens ran)
```

## 6. Never

- Never edit LENS.md as a side effect of a review. If a lens seems wrong or missing, say so to the person as a proposal for the catalogue's change log; changes are made only when asked, follow LENS_META.md §6, and are checked by `check_lens.py` with LENS_META.md beside it.
- Never add a lens, a tag, or a "Look for" line in conversation.
- Never let a verdict rest on `[told]` or `[guessed]`.