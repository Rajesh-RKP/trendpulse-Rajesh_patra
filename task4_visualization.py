import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    print("Setting up outputs folder and loading data...")
    
    # make sure outputs folder exists before saving charts
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        
    try:
        # load the csv from the previous task
        df = pd.read_csv('data/trends_analysed.csv')
    except FileNotFoundError:
        print("Error: data/trends_analysed.csv not found. Please run Task 3 first.")
        return

    print("Generating Chart 1: Top 10 Stories...")
    
    # sort by score to grab the top 10 rows
    top_10 = df.sort_values('score', ascending=False).head(10).copy()
    
    # function to truncate long titles so they fit on the chart nicely
    def shorten_title(title):
        return str(title)[:47] + "..." if len(str(title)) > 50 else str(title)
        
    top_10['short_title'] = top_10['title'].apply(shorten_title)
    
    # plot horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top_10['short_title'], top_10['score'], color='skyblue')
    plt.gca().invert_yaxis() # flip it so the highest score is at the top
    
    plt.title('Top 10 Stories by Score')
    plt.xlabel('Score (Upvotes)')
    plt.ylabel('Story Title')
    plt.tight_layout() 
    
    # save plot to file
    plt.savefig('outputs/chart1_top_stories.png')
    plt.close() 
    
    print("Generating Chart 2: Stories per Category...")
    
    # count stories per category
    category_counts = df['category'].value_counts()
    
    plt.figure(figsize=(8, 6))
    
    # custom colors for the bars
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0']
    plt.bar(category_counts.index, category_counts.values, color=colors)
    
    plt.title('Number of Stories per Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Stories')
    plt.tight_layout()
    
    plt.savefig('outputs/chart2_categories.png')
    plt.close()
    
    print("Generating Chart 3: Score vs Comments...")
    
    plt.figure(figsize=(9, 6))
    
    # split data based on the is_popular flag from task 3
    popular_df = df[df['is_popular'] == True]
    normal_df = df[df['is_popular'] == False]
    
    # plot normal stories
    plt.scatter(normal_df['score'], normal_df['num_comments'], 
                color='blue', alpha=0.6, label='Normal Stories')
                
    # plot popular stories over them
    plt.scatter(popular_df['score'], popular_df['num_comments'], 
                color='red', alpha=0.7, label='Popular Stories')
    
    plt.title('Story Score vs. Number of Comments')
    plt.xlabel('Score (Upvotes)')
    plt.ylabel('Number of Comments')
    plt.legend() 
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plt.savefig('outputs/chart3_scatter.png')
    plt.close()
    
    print("Generating Bonus Dashboard...")
    
    # setup a 2x2 grid for the subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('TrendPulse Dashboard', fontsize=18, fontweight='bold')
    
    # top left chart
    axes[0, 0].barh(top_10['short_title'], top_10['score'], color='skyblue')
    axes[0, 0].invert_yaxis()
    axes[0, 0].set_title('Top 10 Stories by Score')
    axes[0, 0].set_xlabel('Score')
    
    # top right chart
    axes[0, 1].bar(category_counts.index, category_counts.values, color=colors)
    axes[0, 1].set_title('Stories per Category')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].tick_params(axis='x', rotation=45) 
    
    # bottom left chart
    axes[1, 0].scatter(normal_df['score'], normal_df['num_comments'], color='blue', alpha=0.5, label='Normal')
    axes[1, 0].scatter(popular_df['score'], popular_df['num_comments'], color='red', alpha=0.5, label='Popular')
    axes[1, 0].set_title('Score vs Comments')
    axes[1, 0].set_xlabel('Score')
    axes[1, 0].set_ylabel('Comments')
    axes[1, 0].legend()
    
    # remove the extra empty 4th box so the dashboard looks cleaner
    fig.delaxes(axes[1, 1])
    
    plt.tight_layout()
    plt.savefig('outputs/dashboard.png')
    plt.close()
    
    print("All charts generated and saved in the outputs/ folder!")
    print("Pipeline Complete! 🎉")

if __name__ == "__main__":
    main()