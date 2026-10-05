# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is a shopping and styling agent that helps a user find a marketplace
item and build an outfit around it. The user describes what they are looking
for, optionally including a size and maximum price. FitFindr searches the
available listings, selects the best result, suggests an outfit using pieces
from the user's existing wardrobe, and creates a short fit-card caption. If no
listing matches the search, the agent stops and tells the user what they can
change in their query.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **Purpose:** Search marketplace listings for items matching a description, with optional size and maximum price filters.
- **Inputs:** `description: str`, `size: str | None`, `max_price: float | None`
- **Returns:** `list[dict]` of matching listings, ordered with the best matches first.
- **Empty case:** Returns an empty list `[]` when no listings match.

### `suggest_outfit`

- **What it does:** Suggests an outfit for a selected marketplace item using pieces from the user's existing wardrobe.
- **Inputs:** `new_item: dict`, `wardrobe: dict`
- **Returns:** `str` containing a non-empty outfit suggestion.
- **When it has nothing:** If the wardrobe is empty, returns general styling advice for the new item instead of referencing owned pieces.

### `create_fit_card`

- **What it does:** Creates a short fit-card caption describing the completed outfit and selected marketplace item.
- **Inputs:** `outfit: str`, `new_item: dict`
- **Returns:** `str` containing a 2–4 sentence fit-card caption that mentions the item, price, platform, and a specific vibe.
- **When it has nothing:** If the outfit is empty, returns a descriptive message explaining that a fit card could not be created because no outfit suggestion was provided.
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

After `search_listings()` runs:

- If the search returns no results, store a useful message in the session and stop the agent. Do not call `suggest_outfit()`.
- If the search returns results, select the first result, store it in the session, and pass that selected item to `suggest_outfit()`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** The query is parsed using string splitting. The
agent looks for `under` followed by a price and `size` followed by a size value,
then removes those parts from the remaining description.

**What moves through the session:** The parsed query is stored in
`session["parsed"]`, then the search results are stored in
`session["search_results"]`. The first result becomes
`session["selected_item"]`, which is read by `suggest_outfit()`. Its result is
stored in `session["outfit_suggestion"]` and then read by `create_fit_card()`,
whose final result is stored in `session["fit_card"]`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit Recommendation:**

*   **Top:** Y2K Baby Tee — Butterfly Print (New Item)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Black cropped zip hoodie
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:**
This outfit balances proportions and plays into the Y2K aesthetic. The fitted silhouette of the baby tee pairs effortlessly with the relaxed, baggy fit of the dark wash jeans. Layering the black cropped zip hoodie on top keeps the midriff-baring Y2K vibe alive while adding warmth and streetwear edge. Finally, the chunky white sneakers tie the look together by echoing the white in the baby tee, complemented by the practical black crossbody bag.

  Fit card: Channel total Y2K nostalgia with this fitted butterfly baby tee, available now on Depop for just $18.00. Paired with baggy dark wash jeans, a cropped zip hoodie, and chunky white sneakers, this look effortlessly balances fitted and relaxed streetwear proportions.

0 model calls this session, 2 served from cache

**The three tools, tested one at a time**

```
```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe; item={'title':'Y2K Baby Tee — Butterfly Print','category':'tops','colors':['white','pink'],'style_tags':['y2k','vintage','graphic tee','cottagecore']}; print(suggest_outfit(item, get_example_wardrobe()))"

**Outfit Recommendation:**

*   **Top:** Y2K Baby Tee — Butterfly Print (New item)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Footwear:** Chunky white sneakers
*   **Outerwear:** Black cropped zip hoodie (worn open or carried)
*   **Accessories:** Black crossbody bag

**Why it works:**
This look leans directly into the Y2K aesthetic. The fitted silhouette of the baby tee creates a flattering, balanced contrast against the relaxed, baggy fit of the dark wash jeans. The chunky white sneakers tie in the casual streetwear vibe, while the black crossbody bag and optional cropped zip hoodie add effortless everyday functionality.

```
```
$ python -c "from tools import create_fit_card; item={'title':'Y2K Baby Tee — Butterfly Print','price':18.0,'platform':'depop'}; print(create_fit_card('Pair the baby tee with baggy dark-wash jeans and chunky white sneakers for a Y2K streetwear look.', item))"

Channel ultimate Y2K streetwear energy with this effortless everyday look. Pair the Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans and chunky white sneakers. Grab this piece now for just $18.00 exclusively on depop.

```
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- **What I asked for:** I used Wispr Flow to verbally explain my ideas and reasoning to an LLM, then asked the LLM to help organize and format my responses so they matched the structure required by the assignment.
- **What came back:** The LLM turned my explanations into properly structured Markdown and code while preserving the ideas I had described and helping avoid formatting and syntax errors.
- **What I changed:** I reviewed the generated responses and adjusted the wording and formatting so they more closely reflected my own reasoning and the specific requirements of the assignment.

**Moment 2**

- **What I asked for:** I used AI to help design the prompt for `suggest_outfit()` so the model would combine the selected marketplace item with the user's existing wardrobe.
- **What came back:** The initial prompt instructed the model to use at least one provided wardrobe item and not invent clothing that the user owns. Testing produced an outfit using actual pieces from the example wardrobe.
- **What I changed:** I added a separate empty-wardrobe path so the model gives general styling advice without claiming that the user owns any additional clothing.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
