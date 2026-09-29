"""
TrendPulse - Task 4: Visualizations
--------------------------------------
Loads the analysed CSV from Task 3 and builds 3 charts with Matplotlib,
plus a combined dashboard figure. All charts are saved as PNG files.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def load_data(path="data/trends_analysed.csv"):
    df = pd.read_csv(path)
    os.makedirs("outputs", exist_ok=True)
    return df


def shorten_title(title, max_len=50):
    """Shorten a title to max_len characters, adding '...' if truncated."""
    title = str(title)
    if len(title) > max_len:
        return title[: max_len - 3] + "..."
    return title


def chart1_top_stories(df):
    """Horizontal bar chart of the top 10 stories by score."""
    top10 = df.sort_values("score", ascending=False).head(10)
    # Reverse so the highest score appears at the top of the chart
    top10 = top10.iloc[::-1]

    labels = [shorten_title(t) for t in top10["title"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, top10["score"], color="#4C72B0")
    ax.set_xlabel("Score")
    ax.set_ylabel("Story")
    ax.set_title("Top 10 Stories by Score")
    fig.tight_layout()

    fig.savefig("outputs/chart1_top_stories.png")
    plt.show()
    plt.close(fig)


def chart2_categories(df):
    """Bar chart of story counts per category."""
    counts = df["category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = plt.cm.tab10.colors[: len(counts)]
    ax.bar(counts.index, counts.values, color=colors)
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Stories")
    ax.set_title("Stories per Category")
    fig.tight_layout()

    fig.savefig("outputs/chart2_categories.png")
    plt.show()
    plt.close(fig)


def chart3_scatter(df):
    """Scatter plot of score vs num_comments, coloured by is_popular."""
    fig, ax = plt.subplots(figsize=(8, 6))

    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    ax.scatter(not_popular["score"], not_popular["num_comments"],
               color="gray", label="Not Popular", alpha=0.7)
    ax.scatter(popular["score"], popular["num_comments"],
               color="crimson", label="Popular", alpha=0.7)

    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Comments")
    ax.set_title("Score vs Comments")
    ax.legend()
    fig.tight_layout()

    fig.savefig("outputs/chart3_scatter.png")
    plt.show()
    plt.close(fig)


def dashboard(df):
    """Combine all 3 charts into a single dashboard figure."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # --- Panel 1: Top 10 stories ---
    top10 = df.sort_values("score", ascending=False).head(10).iloc[::-1]
    labels = [shorten_title(t, 30) for t in top10["title"]]
    axes[0].barh(labels, top10["score"], color="#4C72B0")
    axes[0].set_title("Top 10 Stories by Score")
    axes[0].set_xlabel("Score")

    # --- Panel 2: Stories per category ---
    counts = df["category"].value_counts()
    colors = plt.cm.tab10.colors[: len(counts)]
    axes[1].bar(counts.index, counts.values, color=colors)
    axes[1].set_title("Stories per Category")
    axes[1].tick_params(axis="x", rotation=45)

    # --- Panel 3: Score vs comments scatter ---
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                     color="gray", label="Not Popular", alpha=0.7)
    axes[2].scatter(popular["score"], popular["num_comments"],
                     color="crimson", label="Popular", alpha=0.7)
    axes[2].set_title("Score vs Comments")
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard", fontsize=16)
    fig.tight_layout()

    fig.savefig("outputs/dashboard.png")
    plt.show()
    plt.close(fig)


def main():
    df = load_data()
    chart1_top_stories(df)
    chart2_categories(df)
    chart3_scatter(df)
    dashboard(df)
    print("All charts saved to the 'outputs/' folder.")


if __name__ == "__main__":
    main()
