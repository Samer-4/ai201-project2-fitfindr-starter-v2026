# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
The search tool uses keyword matching, so different phrasings of a valid query
may not always match the wording or style tags in the listings. A 4 of 5 target
allows for one search miss while still requiring the full tool sequence to work
reliably for matching queries.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
Unlike matching quality, this behavior is controlled by a deterministic branch
in the planning loop. Whenever `search_listings` returns an empty list, the
agent should always follow the same stop path, so 5 of 5 is a reasonable target.

---

## 3. The selected item stays consistent between tools

Given a query that returns at least one listing, the item stored in
`session["selected_item"]` has the same listing ID as the `new_item` received
by `suggest_outfit` — in 5 of 5 tries.

**Why this target:**  
The session is the source of truth between tool calls, and listing IDs are
unique and directly comparable. Unlike model-generated text, passing state
between tools is deterministic, so the selected item's ID should remain
consistent in every run.

---

## 4. The fit card preserves the selected listing's details

Given a successful run, the fit card correctly includes the selected item's
price and platform without changing or inventing either detail — in at least
4 of 5 tries.

**Why this target:**  
The fit card is model-generated, so its wording can vary between runs even when
the input is the same. However, the price and platform come directly from the
selected listing and should remain grounded in that data. A 4 of 5 target allows
for occasional model variation while requiring these important listing details
to be preserved reliably.

---

## 5. Outfit suggestions use the user's existing wardrobe

Given a successful run with a non-empty wardrobe, the outfit suggestion clearly
uses at least one item from the user's provided wardrobe alongside the selected
marketplace item — in at least 4 of 5 tries.

**Why this target:**  
The purpose of `suggest_outfit` is to show how a new marketplace item can work
with clothing the user already owns. Because the suggestion is model-generated,
the exact outfit can vary, but at least 4 of 5 runs should ground the
recommendation in an actual wardrobe item rather than inventing an entirely new
outfit.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
