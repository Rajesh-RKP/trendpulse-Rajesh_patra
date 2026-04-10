import pandas as pd
import numpy as np

def main():
    print("Loading data...")
    
    try:
        # load our clean csv from task 2
        df = pd.read_csv('data/trends_clean.csv')
    except FileNotFoundError:
        print("Error: data/trends_clean.csv not found. Please run Task 2 first.")
        return

    # print dimensions of the dataframe
    print(f"Loaded data: {df.shape}")
    
    print("First 5 rows:")
    print(df.head())
    
    # calculate averages using pandas built-in mean function
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    # print formatting to include commas for thousands
    print(f"\nAverage score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")
    
    print("\n--- NumPy Stats ---")
    
    # turn the score column into a numpy array for processing
    scores_array = df['score'].to_numpy()
    
    # calc stats using numpy methods
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
    
    # get the category with the most posts
    top_category = df['category'].value_counts().index[0]
    top_category_count = df['category'].value_counts().iloc[0]
    print(f"Most stories in: {top_category} ({top_category_count} stories)")
    
    # find the row with the most comments and pull its title/count
    max_comments_idx = df['num_comments'].idxmax()
    top_story_title = df.loc[max_comments_idx, 'title']
    top_story_comments = df.loc[max_comments_idx, 'num_comments']
    
    print(f"Most commented story: \"{top_story_title}\" — {top_story_comments:,.0f} comments")
    
    # calculate engagement: comments per upvote. add 1 to score to prevent zero division
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # boolean flag if the post scored higher than average
    df['is_popular'] = df['score'] > avg_score
    
    output_filename = 'data/trends_analysed.csv'
    
    # save our new columns back to a csv
    df.to_csv(output_filename, index=False)
    
    print(f"\nSaved to {output_filename}")

if __name__ == "__main__":
    main()