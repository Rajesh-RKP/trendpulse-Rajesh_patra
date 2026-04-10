import pandas as pd
import glob
import os

def main():
    # find all json files in the data folder
    json_files = glob.glob('data/trends_*.json')
    
    if not json_files:
        print("Error: No JSON files found in the data/ folder. Please run Task 1 first.")
        return
        
    # sort the files so we can grab the most recent one
    latest_file = sorted(json_files)[-1]
    
    # load it into pandas
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")
    
    # drop duplicate posts based on the unique post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")
    
    # drop rows that are missing important info
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # force score and comments to be integers. fill na with 0 for comments just in case
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    df['score'] = df['score'].astype(int)
    
    # get rid of posts with a score less than 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # clean up extra whitespace on titles
    df['title'] = df['title'].astype(str).str.strip()
    
    # create the data directory if it somehow doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        
    output_filename = 'data/trends_clean.csv'
    
    # save to csv, set index to false so we don't save row numbers
    df.to_csv(output_filename, index=False)
    print(f"Saved {len(df)} rows to {output_filename}")
    
    # print the requested category summary
    print("Stories per category:")
    category_counts = df['category'].value_counts()
    
    # loop and print each category count nicely formatted
    for cat, count in category_counts.items():
        print(f"  {cat:<15} {count}")

if __name__ == "__main__":
    main()