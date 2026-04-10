import pandas as pd
import numpy as np
import os

def main():
    
    # STEP 1: LOAD AND EXPLORE
    # ----------------------------
    print("Loading data...")
    
    try:
        # Load the cleaned CSV from Task 2
        
        df = pd.read_csv('data/trends_clean.csv')
    except FileNotFoundError:
        print("Error: data/trends_clean.csv not found. Please run Task 2 first.")
        return

    # Print the shape (rows, columns) of the DataFrame

    print(f"Loaded data: {df.shape}")


    # Print the first 5 rows to verify it loaded correctly

    print("First 5 rows:")
    print(df.head())
    
    # Calculate the average score and comments using Pandas

    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    # Print with comma formatting (e.g., 12,450 instead of 12450.0)

    print(f"\nAverage score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")
    
    
    # STEP 2: BASIC ANALYSIS WITH NUMPY
    # ------------------------------------

    print("\n--- NumPy Stats ---")
    
    # Extract the 'score' column as a NumPy array for fast mathematical operations

    scores_array = df['score'].to_numpy()
    
    # Use NumPy functions to calculate statistics

    np_mean = np.mean(scores_array)
    np_median = np.median(scores_array)
    np_std = np.std(scores_array)
    np_max = np.max(scores_array)
    np_min = np.min(scores_array)
    
    print(f"Mean score   : {np_mean:,.0f}")
    print(f"Median score : {np_median:,.0f}")
    print(f"Std deviation: {np_std:,.0f}")
    print(f"Max score    : {np_max:,.0f}")
    print(f"Min score    : {np_min:,.0f}")
    
    # Find the category with the most stories
    # value_counts() sorts in descending order, so index[0] is the top category

    top_category = df['category'].value_counts().index[0]
    top_category_count = df['category'].value_counts().iloc[0]
    print(f"Most stories in: {top_category} ({top_category_count} stories)")
    
    # Find the specific story with the most comments
    # idxmax() gives us the row index where 'num_comments' is highest

    max_comments_idx = df['num_comments'].idxmax()
    top_story_title = df.loc[max_comments_idx, 'title']
    top_story_comments = df.loc[max_comments_idx, 'num_comments']
    
    print(f"Most commented story: \"{top_story_title}\" — {top_story_comments:,.0f} comments")
    
   
    # STEP 3: ADD NEW COLUMNS
    # ----------------------------
    
    # 1. Calculate 'engagement'
    # Formula: comments / (score + 1). 
    # We add 1 to the score denominator to avoid a "Division by Zero" error just in case!

    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # 2. Calculate 'is_popular'
    # This creates a boolean (True/False) column. It will be True if the story's 
    # score is strictly greater than the overall average score we calculated earlier.

    df['is_popular'] = df['score'] > avg_score
   

    # STEP 4: SAVE THE RESULT
    # ----------------------------

    output_filename = 'data/trends_analysed.csv'
    
    # Save the updated DataFrame back to a new CSV file
    # index=False ensures we don't save the row numbers as an extra column

    df.to_csv(output_filename, index=False)
    
    print(f"\nSaved to {output_filename}")

if __name__ == "__main__":
    main()