"""
TrendPulse - Task 3: Analysis with Pandas & NumPy
----------------------------------------------------
Loads the cleaned CSV from Task 2, explores it, computes statistics
with NumPy, adds new columns, and saves the result for Task 4.
"""

import numpy as np
import pandas as pd


def load_and_explore(path="data/trends_clean.csv"):
    """Load the clean CSV and print basic exploratory info."""
    df = pd.read_csv(path)

    print(f"Loaded data: {df.shape}\n")
    print("First 5 rows:")
    print(df.head(), "\n")

    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()
    print(f"Average score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}\n")

    return df


def numpy_stats(df):
    """Compute and print statistics using NumPy."""
    scores = df["score"].to_numpy()

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)

    print("--- NumPy Stats ---")
    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")
    print(f"Max score    : {max_score:,.0f}")
    print(f"Min score    : {min_score:,.0f}\n")

    # Category with the most stories
    top_category = df["category"].value_counts().idxmax()
    top_category_count = df["category"].value_counts().max()
    print(f"Most stories in: {top_category} ({top_category_count} stories)\n")

    # Story with the most comments
    top_comment_idx = df["num_comments"].to_numpy().argmax()
    top_story = df.iloc[top_comment_idx]
    print(f'Most commented story: "{top_story["title"]}"  — {top_story["num_comments"]:,} comments\n')

    return mean_score


def add_new_columns(df, mean_score):
    """Add 'engagement' and 'is_popular' columns."""
    df["engagement"] = df["num_comments"] / (df["score"] + 1)
    df["is_popular"] = df["score"] > mean_score
    return df


def save_result(df, path="data/trends_analysed.csv"):
    df.to_csv(path, index=False)
    print(f"Saved to {path}")


def main():
    df = load_and_explore()
    mean_score = numpy_stats(df)
    df = add_new_columns(df, mean_score)
    save_result(df)


if __name__ == "__main__":
    main()
