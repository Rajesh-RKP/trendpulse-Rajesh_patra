import requests
import time
import json
import os
from datetime import datetime

def main():
    # setup custom user agent so hacker news doesn't block the requests
    HEADERS = {"User-Agent": "TrendPulse/1.0"}
    
    # keywords mapped to categories for filtering titles later
    CATEGORIES = {
        "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
        "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
        "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
        "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
        "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    }
    
    print("Fetching top 500 story IDs from HackerNews...")
    try:
        # grab the top story ids
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, headers=HEADERS, timeout=10)
        response.raise_for_status() 
        top_ids = response.json()[:500] # just need the first 500
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return 

    final_stories = []
    # use a set to track ids so we don't accidentally add the same story to two categories
    used_ids = set() 
    
    # dictionary to cache api responses. this prevents spamming the api 
    # for the same story id while looping through different categories
    story_cache = {} 

    # loop through categories first to manage the sleep timer rule
    for category_name, keywords in CATEGORIES.items():
        print(f"Collecting stories for category: {category_name}...")
        category_count = 0
        
        for story_id in top_ids:
            # stop if we hit 30 stories for this category (aiming for 150 total)
            if category_count >= 30:
                break 
                
            # skip if already processed
            if story_id in used_ids:
                continue 
                
            # fetch the post if we haven't seen it yet
            if story_id not in story_cache:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = requests.get(story_url, headers=HEADERS, timeout=10)
                    story_response.raise_for_status()
                    story_cache[story_id] = story_response.json()
                    
                    # print a little progress update so the console doesn't look frozen
                    if len(story_cache) % 50 == 0:
                        print(f"  ...fetched {len(story_cache)} unique stories from API so far...")

                except Exception as e:
                    print(f"Failed to fetch story {story_id}: {e} - Moving on...")
                    story_cache[story_id] = None 
                    
            story = story_cache[story_id]
            
            # make sure the post isn't empty and actually has a title
            if not story or 'title' not in story:
                continue
                
            # force lowercase for easier keyword matching
            title_lower = story.get('title', '').lower()
            
            # check if any of our category keywords are in the title string
            if any(kw.lower() in title_lower for kw in keywords):
                # found a match, pull out only the fields we care about
                extracted_story = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category_name,
                    "score": story.get("score", 0), # fallback to 0
                    "num_comments": story.get("descendants", 0), # descendants = comments in HN api
                    "author": story.get("by", "Unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                final_stories.append(extracted_story)
                used_ids.add(story_id)
                category_count += 1
                
        # sleep 2 seconds between categories per the requirements
        print(f"Finished {category_name}. Found {category_count} stories. Sleeping for 2 seconds...")
        time.sleep(2)
        
    # make the data dir if missing
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # build the filename with today's date
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    try:
        # dump everything to json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_stories, f, indent=4)
            
        print(f"Collected {len(final_stories)} stories. Saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

if __name__ == "__main__":
    main()