"""
TrendPulse - Task 1: Data Collection
-----------------------------------
This script fetches top trending stories from Hacker News API.

Features:
- Fetch top story IDs
- Fetch story details
- Handles network errors
- Uses retry mechanism
- Adds timeout to prevent hanging
"""

import requests
import time

# Base URLs
BASE_URL = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{BASE_URL}/topstories.json"
ITEM_URL = f"{BASE_URL}/item/{{}}.json"

# Headers (good practice for APIs)
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}


def safe_get(url, retries=3, timeout=5):
    """
    Makes a GET request safely with retry and timeout.

    Args:
        url (str): API endpoint
        retries (int): number of retry attempts
        timeout (int): request timeout in seconds

    Returns:
        dict/list or None
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()

        except requests.exceptions.Timeout:
            print(f"[Retry {attempt+1}] Timeout occurred...")

        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt+1}] Request failed: {e}")

        time.sleep(1)  # wait before retry

    print("Failed after multiple retries.\n")
    return None


def get_top_story_ids(limit=10):
    """
    Fetch top story IDs.

    Args:
        limit (int): number of stories to fetch

    Returns:
        list
    """
    data = safe_get(TOP_STORIES_URL)

    if not data:
        return []

    return data[:limit]


def get_story_details(story_id):
    """
    Fetch details of a single story.

    Args:
        story_id (int)

    Returns:
        dict
    """
    url = ITEM_URL.format(story_id)
    return safe_get(url)


def main():
    print("Fetching top stories...\n")

    story_ids = get_top_story_ids(10)

    if not story_ids:
        print("Error: Could not fetch story IDs.")
        return

    stories = []

    for story_id in story_ids:
        story = get_story_details(story_id)

        if story:
            stories.append({
                "title": story.get("title", "N/A"),
                "author": story.get("by", "N/A"),
                "score": story.get("score", 0),
                "url": story.get("url", "N/A")
            })

        time.sleep(0.5)  # Prevent API overload

    print("Top Trending Stories:\n")

    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}")
        print(f"   Author : {story['author']}")
        print(f"   Score  : {story['score']}")
        print(f"   URL    : {story['url']}\n")


if __name__ == "__main__":
    main()