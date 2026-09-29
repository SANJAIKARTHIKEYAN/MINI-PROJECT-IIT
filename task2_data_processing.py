"""
TrendPulse - Task 2: Clean the Data & Save as CSV
---------------------------------------------------
Loads the raw JSON produced by Task 1, cleans it with Pandas,
and saves a tidy CSV file for use in Task 3.
"""

import os
import glob
import pandas as pd


def find_latest_json_file(data_dir="data"):
    """Find the most recently created trends_*.json file in the data folder."""
    pattern = os.path.join(data_dir, "trends_*.json")
    json_files = [f for f in glob.glob(pattern) if not f.endswith("clean.csv")]
    if not json_files:
        raise FileNotFoundError(
            f"No trends_*.json file found in '{data_dir}/'. Run Task 1 first."
        )
    # Pick the most recently modified file
    return max(json_files, key=os.path.getmtime)


def load_data(json_path):
    """Load the raw JSON file into a Pandas DataFrame."""
    df = pd.read_json(json_path)
    print(f"Loaded {len(df)} stories from {json_path}")
    return df


def clean_data(df):
    """Clean the raw DataFrame: dedupe, drop nulls, fix types, filter low scores, strip whitespace."""

    # 1. Remove duplicate stories (same post_id)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # 2. Drop rows missing post_id, title, or score
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # 3. Fix data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # 4. Strip extra whitespace from titles
    df["title"] = df["title"].str.strip()

    # 5. Remove low-quality stories (score < 5)
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    return df.reset_index(drop=True)


def save_clean_csv(df, out_path="data/trends_clean.csv"):
    """Save the cleaned DataFrame to CSV and print a summary."""
    df.to_csv(out_path, index=False)
    print(f"\nSaved {len(df)} rows to {out_path}")

    print("\nStories per category:")
    category_counts = df["category"].value_counts()
    for category, count in category_counts.items():
        print(f"  {category:<15}{count}")


def main():
    json_path = find_latest_json_file()
    df = load_data(json_path)
    df_clean = clean_data(df)
    save_clean_csv(df_clean)


if __name__ == "__main__":
    main()
