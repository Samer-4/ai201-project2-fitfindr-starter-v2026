"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable
from mcp_client import call_tool


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. Check session["error"] first — if it isn't None,
        the run ended early and the later fields will still be None.

    Unit 3 flow:
      1. Start a session.
      2. Parse the query.
      3. Search listings.
      4. Stop if the search returns nothing.
      5. Select the first result.
      6. Suggest an outfit.
      7. Create a fit card.
      8. Return the completed session.
    """

    session = new_session(query, wardrobe)

    # Parse the query
    description = query
    size = None
    max_price = None

    words = query.split()

    # Parse a maximum price from a phrase like "under $30"
    if "under" in words:
        index = words.index("under")

        if index + 1 < len(words):
            max_price = float(words[index + 1].replace("$", ""))
            description = " ".join(words[:index])

    # Parse a size from a phrase like "size M"
    words = description.split()

    if "size" in words:
        index = words.index("size")

        if index + 1 < len(words):
            size = words[index + 1]
            description = " ".join(words[:index])

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    # Search for matching listings
    session["search_results"] = call_tool(
    "search_listings",
    {
        "description": session["parsed"]["description"],
        "size": session["parsed"]["size"],
        "max_price": session["parsed"]["max_price"],
    },
    )

    # Branch: stop if nothing was found
    if not session["search_results"]:
        session["error"] = (
            "No matching listings found. Try changing the description, "
            "size, or maximum price."
        )
        return session

    # Select the best search result
    session["selected_item"] = session["search_results"][0]

    # Suggest an outfit using the selected item
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"],
        session["wardrobe"],
    )

    # Create a fit card using the outfit suggestion
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"],
        session["selected_item"],
    )

    return session


# ─────────────────────────────────────────────────────────────────────────────
# UNIT 4 — COME BACK AND ADD:
#
# • Trace calls. One per step:
#   trace.step("search_listings", inputs=..., returned=...)
#   See trace.py. README needs the output.
#
# • A handler for ModelUnavailable so a bad API key produces
#   a useful message instead of a stack trace.
# ─────────────────────────────────────────────────────────────────────────────


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(
            f"  fit_card is {session['fit_card']!r} "
            "— it should still be None here"
        )
        return

    item = session["selected_item"] or {}

    print(
        f"  found:    {item.get('title')} — "
        f"${item.get('price')} on {item.get('platform')}"
    )
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(
        run_agent(
            query="looking for a vintage graphic tee under $30",
            wardrobe=get_example_wardrobe(),
        )
    )

    print("\n=== A query it can't ===")
    _show(
        run_agent(
            query="designer ballgown size XXS under $5",
            wardrobe=get_example_wardrobe(),
        )
    )

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
