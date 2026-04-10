import requests
import time
import json
import os
from datetime import datetime

def main():


    # CONFIGURATION & CONSTANTS
    # -----------------------------
    
    # Adding a custom User-Agent header as requested

    HEADERS = {"User-Agent": "TrendPulse/1.0"}
    

    # Mapping categories to their specific keywords (case-insensitive later)
    
    CATEGORIES = {
        "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
        "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
        "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
        "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
        "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
    }
    
   
   
    # STEP 1: FETCH TOP STORY IDs
    # --------------------------------
    
    print("Fetching top 500 story IDs from HackerNews...")
    try:
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_stories_url, headers=HEADERS, timeout=10)
        response.raise_for_status() # Raise an exception for bad HTTP status codes
        top_ids = response.json()[:500] # Slice the list to ensure we only get the first 500
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return # Exit script safely if the main feed fails

    # Initialize storage variables
    final_stories = []
    used_ids = set() # Keeps track of stories already assigned to prevent duplicates
    
    # A dictionary cache to store API responses. 
    # Because we loop by category, we check the same IDs multiple times.
    # Caching them prevents us from spamming the HN API and making thousands of requests!
    story_cache = {} 

  
  
    # STEP 2: ITERATE CATEGORIES & EXTRACT FIELDS
    # ---------------------------------------------
    
    # We loop over categories first to satisfy the "one sleep per category loop" rule

    for category_name, keywords in CATEGORIES.items():
        print(f"Collecting stories for category: {category_name}...")
        category_count = 0
        
        for story_id in top_ids:
            # Stop if we hit 30 stories for this specific category (30 * 5 categories = 150 total)

            if category_count >= 30:
                break 
                
            # Skip if this story was already caught by an earlier category

            if story_id in used_ids:
                continue 
                
            # Fetch the story details if it's not already in our memory cache

            if story_id not in story_cache:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = requests.get(story_url, headers=HEADERS, timeout=10)
                    story_response.raise_for_status()
                    story_cache[story_id] = story_response.json()
                    
                    # Print progress so the script doesn't look like it's frozen

                    if len(story_cache) % 50 == 0:
                        print(f"  ...fetched {len(story_cache)} unique stories from API so far...")

                except Exception as e:
                    print(f"Failed to fetch story {story_id}: {e} - Moving on...")
                    story_cache[story_id] = None # Mark as None so we don't try fetching it again
                    
            story = story_cache[story_id]
            
            # Ensure the story object is valid and has a title before processing

            if not story or 'title' not in story:
                continue
                
            # Convert title to lowercase for case-insensitive matching

            title_lower = story.get('title', '').lower()
            
            # Check if any keyword exists as a substring in the title

            if any(kw.lower() in title_lower for kw in keywords):
                # We have a match! Extract only the requested fields

                extracted_story = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category_name,
                    "score": story.get("score", 0), # Default to 0 if missing
                    "num_comments": story.get("descendants", 0), # HN uses 'descendants' for comments
                    "author": story.get("by", "Unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                final_stories.append(extracted_story)
                used_ids.add(story_id) # Mark as used
                category_count += 1
                
        # Sleep for 2 seconds at the end of every category loop (Rule requirement)

        print(f"Finished {category_name}. Found {category_count} stories. Sleeping for 2 seconds...")
        time.sleep(2)
        


    # STEP 3: SAVE TO JSON FILE
    # ---------------------------
    
    # Create the data folder if it doesn't currently exist

    if not os.path.exists('data'):

        os.makedirs('data')
        
    # Format current date as YYYYMMDD

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    try:
        # Save as formatted JSON

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_stories, f, indent=4)
            
        # Expected console output requirement

        print(f"Collected {len(final_stories)} stories. Saved to {filename}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

if __name__ == "__main__":
    main()