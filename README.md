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

### Baseline Evaluation

- Command: `python run_eval.py --label before`
- Date: October 12, 2026
- Test configuration: 5 tries per criterion, caching disabled
- Total executions: 30 (25 criterion runs + 5 diagnostic runs)
- Model calls: 50
- Crashes: 0
- Results: `results/run_2026-10-12_1124_before.md`

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Three-tool completion | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty-search handling | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected-item consistency | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5)* |
| 4. Price and platform accuracy | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Existing wardrobe usage | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

*Criterion 3 was verified separately using five deterministic runs with `unittest.mock.patch`. The original evaluation traces did not explicitly capture the item ID received by `suggest_outfit`.

### Evidence From Actual Runs

**Criterion 1 — Three-tool completion**

Source: `agent.py::run_agent`, Try 1

The agent retrieved 10 listings, called `suggest_outfit`, and generated a 326-character fit card.

**Criterion 2 — Empty-search handling**

Source: `agent.py::run_agent`, Try 1

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

No matching listings found. Try changing the description,
size, or maximum price.
```

No downstream tools were called.

**Criterion 3 — Selected-item consistency**

Source: `agent.py::run_agent`, separate mocked verification

```text
Try 1: PASS (lst_002 → lst_002)
Try 2: PASS (lst_002 → lst_002)
Try 3: PASS (lst_002 → lst_002)
Try 4: PASS (lst_002 → lst_002)
Try 5: PASS (lst_002 → lst_002)
```

Both model-dependent functions were mocked to verify the actual item ID passed into `suggest_outfit` without additional API calls.

**Criterion 4 — Price and platform accuracy**

Source: `tools.py::create_fit_card`, Try 2

Selected listing: Y2K Baby Tee — Butterfly Print, $18.00, Depop.

```text
Channel the ultimate Y2K streetwear vibe by pairing this
Y2K Baby Tee — Butterfly Print with baggy dark-wash jeans,
a vintage black denim jacket, chunky white sneakers, and
a black crossbody bag. You can find this piece on Depop
for just $18.00. It's an effortless look that balances a
fitted silhouette with relaxed proportions for everyday
retro style.
```

All five fit cards preserved the correct $18.00 price and Depop platform.

**Criterion 5 — Existing wardrobe usage**

Source: `tools.py::suggest_outfit`, Try 1

```text
Top: Y2K Baby Tee — Butterfly Print (New Item)
Bottoms: Baggy straight-leg jeans, dark wash
Outerwear: Vintage black denim jacket
Shoes: Chunky white sneakers
Accessories: Black crossbody bag
```

The outfit uses four verified wardrobe items: `w_001`, `w_006`, `w_007`, and `w_010`. All five runs included these existing pieces.

### Baseline Observations

All five criteria met their predefined targets. The evaluation also identified an issue outside the original criteria: some generated fit cards described items as "exclusively" available on Depop, although the listing data did not establish exclusivity.

This indicates that the model can preserve required facts while introducing unsupported claims. The issue is a candidate for the measured improvement in Milestone 5.

The five criteria were tested using the same matching query for the successful-path scenarios, so these results do not establish reliability across different listings or query types.


## Verdicts and Diagnoses


### Criterion Results

**Criterion 1 — Three-tool completion: MET (5/5)**

All five runs successfully executed `search_listings` through MCP, followed by `suggest_outfit` and `create_fit_card`. Each run produced a non-empty fit card.

No failures were observed. However, all five runs used the same query, so this does not establish reliability across different search phrases.

**Criterion 2 — Empty-search handling: MET (5/5)**

All five runs returned an empty search result and stopped before calling `suggest_outfit`.

The agent consistently returned an actionable message recommending changes to the description, size, or maximum price. No failures were observed.

**Criterion 3 — Selected-item consistency: MET (5/5)**

Five separate mocked tests confirmed that the ID stored in `session["selected_item"]` matched the ID received by `suggest_outfit`.

All five comparisons returned `lst_002 == lst_002`.

This was verified through a separate deterministic test because the original evaluation traces did not record the IDs passed between tools. The model-dependent functions were mocked for these tests.

**Criterion 4 — Price and platform accuracy: MET (5/5)**

All five generated fit cards correctly preserved the selected listing's price ($18.00) and platform (Depop).

No failures occurred against the original criterion.

However, one generated caption described the item as available "exclusively on depop." The dataset established the platform but did not establish exclusivity.

This is an unsupported claim introduced during `create_fit_card`, indicating that preserving required details does not guarantee that every generated claim is grounded.

**Criterion 5 — Existing wardrobe usage: MET (5/5)**

All five outfit suggestions referenced the selected marketplace item alongside existing wardrobe pieces.

The suggestions consistently included:
- Baggy straight-leg jeans, dark wash (`w_001`)
- Vintage black denim jacket (`w_006`)
- Chunky white sneakers (`w_007`)
- Black crossbody bag (`w_010`)

No failures were observed against the criterion.

### Overall Diagnosis

All five predefined acceptance criteria were met.

The main issue identified outside the original criteria was an unsupported exclusivity claim in the generated fit card.

- **Affected stage:** `create_fit_card`
- **Failure mechanism:** The language model introduced a marketplace availability claim not supported by the listing data.
- **Likely cause:** The generation prompt does not explicitly prohibit exclusivity claims.
- **Proposed improvement:** Update the fit-card prompt to prohibit unsupported availability or exclusivity claims, then rerun the same evaluations.

The original acceptance criteria will remain unchanged. The improvement will be evaluated using the same five scenarios and targets.


## Loop Trace

Command: `python app.py ask 'vintage graphic tee under $30' --trace`

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: **Outfit Recommendation:**  *   **Top:** Y2K Baby Tee — Butterfly Print (New Item) *   **Bottoms:** Baggy stra…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channel total Y2K nostalgia with this fitted butterfly baby tee, available now on Depop for just $18.00. Paire…
```

**Happy path**

Command: `python app.py ask 'vintage graphic tee under $30' --trace`

The agent successfully executes the following sequence:

```text
[1] search_listings (via MCP) -> 10 matching listings
[2] suggest_outfit -> outfit using existing wardrobe items
[3] create_fit_card -> completed fit-card caption
```

**Empty search**

Command: `python app.py ask 'designer ballgown size XXS under $5' --trace`

```text
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
```

The agent stops after the MCP search and returns:

```text
No matching listings found. Try changing the description, size, or maximum price.
```

Neither `suggest_outfit` nor `create_fit_card` is called.

**On the MCP move:**

I moved `search_listings` behind an MCP server in `mcp_server.py`, exposing its typed inputs through `FastMCP`.

In `agent.py::run_agent`, I replaced the direct search function call with `mcp_client.call_tool("search_listings", ...)`.

The search continues to return matching listing dictionaries, and the empty-search branch behaves as before. The difference is that search now runs through the MCP client/server boundary rather than being called directly.

**Failure-mode testing**

- **Empty search:** Tested an impossible query. The agent stopped before the model-dependent tools and returned an actionable message.
- **Empty wardrobe:** Tested with `--empty-wardrobe`. The agent produced general styling advice rather than pretending the user owned additional clothing.
- **Invalid model key:** Temporarily tested with an invalid Gemini API key and caching disabled. The application returned a `ModelUnavailable` message explaining how to correct `GEMINI_API_KEY`. The valid key was restored afterward.


---

## The Improvement

**What I changed:**

Added one instruction to the `create_fit_card()` prompt in `tools.py`:

> Do not claim the item is exclusive to a platform or make availability claims unless explicitly supported by the listing.

No other agent logic or acceptance criteria were changed for this improvement.

**Which failure it was meant to fix:**

The baseline evaluation revealed an unsupported claim that the selected item was available "exclusively on depop." The listing data included the platform but provided no evidence of exclusivity.

The issue originated during fit-card generation, where the language model introduced a claim beyond the supplied listing information.

### Run Log — After

- Command: `python run_eval.py --label after`
- Date: October 12, 2026
- Results: `results/run_2026-10-12_1148_after.md`
- Total runs: 30
- Model calls: 50
- Crashes: 0
- Cache: disabled

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Three-tool completion | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty-search handling | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected-item consistency | 5/5 | Not logged | Not logged | Not logged | Not logged | Not logged | Not directly verified in after-run |
| 4. Price and platform accuracy | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Existing wardrobe usage | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criterion 3 was verified through five separate mocked tests before the improvement, all passing. The prompt change only affected `create_fit_card()`, not item selection or the arguments to `suggest_outfit()`. However, the after-run trace still does not explicitly expose the item ID passed between tools, so the after-run itself cannot independently establish the five ID comparisons.

Criterion 5 outputs showed the new marketplace item being combined with existing wardrobe pieces. The full generated outfits are preserved in the after-run results file.

### Before and After Comparison

| Measurement | Before | After |
|---|---|---|
| Successful three-tool flow | 5/5 | 5/5 |
| Correct early stopping | 5/5 | 5/5 |
| Correct price and platform | 5/5 | 5/5 |
| Unsupported exclusivity claims in Criterion 4 | 1/5 | 0/5 |
| Unverified availability language in Criterion 4 | Not fully assessed | 3/5 |

**Did it help, and how do I know:**

The original acceptance criteria continued to perform well after the change.

Within the Criterion 4 samples, unsupported exclusivity claims decreased from one before the improvement to zero afterward.

However, three after-run captions still used phrases implying current availability, such as "available now" or "grab this piece now," without a separate availability check.

The prompt change therefore appears to have improved exclusivity wording, but it did not completely prevent unsupported availability claims. Because the sample is small and generation is stochastic, the results do not prove causation or broad reliability.

---

## What's Still Broken

All five original criteria met their targets in the baseline evaluation, although Criterion 3 required a separate mocked test because the evaluation trace did not capture the item ID handoff.

The remaining limitations are:

1. **Unsupported availability claims:** `tools.py::create_fit_card()` sometimes produces phrases such as "available now" even though the listing data does not independently verify current availability. A future improvement would add output validation or a more structured generation process.

2. **Limited scenario diversity:** Most successful-path evaluations use the same vintage graphic tee query and example wardrobe. Additional queries, listing types, and wardrobe configurations would provide a stronger reliability assessment.

3. **Incomplete ID observability:** `trace.py` summarizes dictionary keys rather than recording the selected and received item IDs. Future tests should explicitly assert or record these identifiers during each evaluation run.

4. **Model-dependent output variability:** Prompt changes can reduce errors without guaranteeing their elimination. Larger evaluation sets and automated grounding checks would make comparisons more reliable.

I stopped after one targeted prompt change to preserve the assignment's before/after comparison and avoid introducing additional unmeasured changes.

---

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
