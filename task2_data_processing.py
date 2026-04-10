import pandas as pd
import glob
import os

def main():
    # =====================================================================
    # STEP 1: LOAD THE JSON FILE
    # =====================================================================
    
    # We use glob to find the JSON file created by Task 1 in the data folder.
    # This is helpful because the filename changes based on the current date!
    json_files = glob.glob('data/trends_*.json')
    
    if not json_files:
        print("Error: No JSON files found in the data/ folder. Please run Task 1 first.")
        return
        
    # Sort the files alphabetically (which sorts them by date based on our naming convention)
    # and grab the last one in the list (the most recent one)
    latest_file = sorted(json_files)[-1]
    
    # Load the JSON data into a Pandas DataFrame
    df = pd.read_json(latest_file)
    
    # Print the initial row count to the console
    print(f"Loaded {len(df)} stories from {latest_file}")
    
    # =====================================================================
    # STEP 2: CLEAN THE DATA
    # =====================================================================
    
    # 1. Duplicates - Remove any rows where the post_id is identical to an earlier one
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")
    
    # 2. Missing values - Drop rows if they are missing critical information
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # 3. Data types - Ensure score and num_comments are whole numbers (integers).
    # We use fillna(0) on num_comments just in case some valid stories have 0 comments (null/NaN)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    df['score'] = df['score'].astype(int)
    
    # 4. Low quality - Filter the DataFrame to only keep stories with a score of 5 or higher
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # 5. Whitespace - Strip leading and trailing spaces from the story titles
    # We convert to string first to prevent errors if a title accidentally got parsed as a number
    df['title'] = df['title'].astype(str).str.strip()
    
    # =====================================================================
    # STEP 3: SAVE AS CSV
    # =====================================================================
    
    # Ensure the data directory exists (just in case)
    if not os.path.exists('data'):
        os.makedirs('data')
        
    output_filename = 'data/trends_clean.csv'
    
    # Save the cleaned DataFrame to a CSV file. 
    # index=False prevents pandas from saving the row numbers as a separate column.
    df.to_csv(output_filename, index=False)
    
    # Print final confirmation
    print(f"Saved {len(df)} rows to {output_filename}")
    
    # Print the category summary exactly as requested in the prompt
    print("Stories per category:")
    
    # value_counts() automatically counts occurrences of each category
    category_counts = df['category'].value_counts()
    
    # Loop through the counts and print them with nice formatting
    # The :<15 pads the category string with spaces to align the numbers neatly!
    for cat, count in category_counts.items():
        print(f"  {cat:<15} {count}")

if __name__ == "__main__":
    main()