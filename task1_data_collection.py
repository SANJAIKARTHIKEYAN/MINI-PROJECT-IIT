"""
TrendPulse - Task 1: Fetch Data from API
------------------------------------------
Fetches the top trending stories from the HackerNews public API,
categorises them into 5 topics based on keyword matching in the title,
and saves the results to a JSON file.
"""

import requests
import time
import json
import os
from datetime import datetime

# --- Constants -------------------------------------------------------------

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

NUM_IDS_TO_FETCH = 500       # how many top story ids to pull
STORIES_PER_CATEGORY = 25    # cap per category

# Category -> list of keywords (checked case-insensitively against the title)
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

# We keep the order stable so a story only ever lands in ONE category
# (the first category, in this order, whose keyword is found in the title).
CATEGORY_ORDER = ["technology", "worldnews", "sports", "science", "entertainment"]


def get_top_story_ids():
    """Fetch the list of top story IDs from HackerNews."""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()[:NUM_IDS_TO_FETCH]
    except requests.RequestException as e:
        print(f"Failed to fetch top story IDs: {e}")
        return []


def fetch_story_details(story_id):
    """Fetch a single story's details. Returns None on failure."""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def categorize_title(title):
    """Return the first matching category for a title, or None if no match."""
    if not title:
        return None
    title_lower = title.lower()
    for category in CATEGORY_ORDER:
        keywords = CATEGORY_KEYWORDS[category]
        if any(keyword.lower() in title_lower for keyword in keywords):
            return category
    return None


def build_story_record(story, category):
    """Extract the required fields from a raw HackerNews story object."""
    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score"),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat(timespec="seconds"),
    }


def main():
    story_ids = get_top_story_ids()
    if not story_ids:
        print("No story IDs retrieved. Exiting.")
        return

    # Cache so each story is only ever fetched once, even though we
    # loop over the id list once per category below.
    story_cache = {}

    def get_story(story_id):
        if story_id not in story_cache:
            story_cache[story_id] = fetch_story_details(story_id)
        return story_cache[story_id]

    all_stories = []

    # Process one category at a time, collecting up to STORIES_PER_CATEGORY
    # matching stories, then pause before moving to the next category.
    for category in CATEGORY_ORDER:
        collected_for_category = []

        for story_id in story_ids:
            if len(collected_for_category) >= STORIES_PER_CATEGORY:
                break

            story = get_story(story_id)
            if story is None or story.get("type") != "story":
                continue

            assigned_category = categorize_title(story.get("title"))
            if assigned_category == category:
                collected_for_category.append(build_story_record(story, category))

        all_stories.extend(collected_for_category)
        print(f"Collected {len(collected_for_category)} stories for category '{category}'")

        # One sleep per category loop (not per individual story fetch)
        time.sleep(2)

    # --- Save to JSON --------------------------------------------------
    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, indent=2)

    print(f"Collected {len(all_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
