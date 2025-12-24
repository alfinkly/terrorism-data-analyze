"""
Terrorist Group Analysis
Deep dive into terrorist organizations: activity patterns, methods, and evolution.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration
USE_FULL_DATASET = True


def load_data():
    """Loads the terrorism data from Excel file."""
    file_path = "gtd.xlsx" if USE_FULL_DATASET else "gtd-mini.xlsx"
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None


def prepare_data(df):
    """Renames columns and prepares data for analysis."""
    df.rename(
        columns={
            "iyear": "Year",
            "imonth": "Month",
            "iday": "Day",
            "country_txt": "Country",
            "region_txt": "Region",
            "attacktype1_txt": "AttackType",
            "target1": "Target",
            "nkill": "Killed",
            "nwound": "Wounded",
            "gname": "Group",
            "targtype1_txt": "Target_type",
            "weaptype1_txt": "Weapon_type",
        },
        inplace=True,
    )

    df["Killed"] = pd.to_numeric(df["Killed"], errors="coerce").fillna(0)
    df["Wounded"] = pd.to_numeric(df["Wounded"], errors="coerce").fillna(0)
    df["Casualties"] = df["Killed"] + df["Wounded"]
    return df


def analyze_most_active_groups(df, top_n=20):
    """Analyzes the most active terrorist groups."""
    df_known = df[df["Group"] != "Unknown"]

    group_stats = df_known.groupby("Group").agg(
        {
            "Year": ["count", "min", "max"],
            "Killed": "sum",
            "Wounded": "sum",
            "Country": "nunique",
        }
    )
    group_stats.columns = [
        "Attacks",
        "First_Year",
        "Last_Year",
        "Killed",
        "Wounded",
        "Countries",
    ]
    group_stats["Active_Years"] = (
        group_stats["Last_Year"] - group_stats["First_Year"] + 1
    )
    group_stats["Attacks_Per_Year"] = (
        group_stats["Attacks"] / group_stats["Active_Years"]
    ).round(1)

    top_groups = group_stats.nlargest(top_n, "Attacks")

    plt.figure(figsize=(12, 10))
    cmap = plt.get_cmap("Reds")
    colors = cmap(np.linspace(0.3, 0.9, len(top_groups)))
    plt.barh(top_groups.index, top_groups["Attacks"], color=colors)
    plt.xlabel("Number of Attacks")
    plt.title(f"Top {top_n} Most Active Terrorist Groups")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("most_active_groups.png", dpi=150)
    plt.show()
    print("Saved: most_active_groups.png")

    print("\n" + "=" * 70)
    print(f"TOP {top_n} MOST ACTIVE TERRORIST GROUPS")
    print("=" * 70)
    for group, row in top_groups.iterrows():
        print(f"\n{group}")
        print(
            f"  Attacks: {int(row['Attacks']):,} | Active: {int(row['First_Year'])}-{int(row['Last_Year'])}"
        )
        print(f"  Killed: {int(row['Killed']):,} | Countries: {int(row['Countries'])}")

    return top_groups


def analyze_group_activity_timeline(df, groups=None):
    """Plots activity timeline for major groups."""
    df_known = df[df["Group"] != "Unknown"]

    if groups is None:
        groups = df_known["Group"].value_counts().nlargest(10).index.tolist()

    df_top = df_known[df_known["Group"].isin(groups)]
    yearly_activity = pd.crosstab(df_top["Year"], df_top["Group"])

    plt.figure(figsize=(14, 8))
    for group in groups:
        if group in yearly_activity.columns:
            plt.plot(
                yearly_activity.index, yearly_activity[group], linewidth=2, label=group
            )

    plt.xlabel("Year")
    plt.ylabel("Number of Attacks")
    plt.title("Activity Timeline of Major Terrorist Groups")
    plt.legend(title="Group", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("group_activity_timeline.png", dpi=150)
    plt.show()
    print("Saved: group_activity_timeline.png")


def analyze_group_methods(df, top_n=10):
    """Analyzes preferred attack methods of major groups."""
    df_known = df[df["Group"] != "Unknown"]
    top_groups = df_known["Group"].value_counts().nlargest(top_n).index.tolist()

    df_top = df_known[df_known["Group"].isin(top_groups)]
    method_pivot = (
        pd.crosstab(df_top["Group"], df_top["AttackType"], normalize="index") * 100
    )

    plt.figure(figsize=(14, 10))
    sns.heatmap(
        method_pivot,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        cbar_kws={"label": "% of Attacks"},
    )
    plt.title("Attack Methods by Terrorist Group (%)")
    plt.tight_layout()
    plt.savefig("group_methods_heatmap.png", dpi=150)
    plt.show()
    print("Saved: group_methods_heatmap.png")


def analyze_group_targets(df, top_n=10):
    """Analyzes preferred targets of major groups."""
    df_known = df[df["Group"] != "Unknown"]
    top_groups = df_known["Group"].value_counts().nlargest(top_n).index.tolist()
    top_targets = df_known["Target_type"].value_counts().nlargest(8).index.tolist()

    df_filtered = df_known[
        df_known["Group"].isin(top_groups) & df_known["Target_type"].isin(top_targets)
    ]
    target_pivot = (
        pd.crosstab(df_filtered["Group"], df_filtered["Target_type"], normalize="index")
        * 100
    )

    plt.figure(figsize=(14, 10))
    sns.heatmap(
        target_pivot,
        annot=True,
        fmt=".0f",
        cmap="Blues",
        cbar_kws={"label": "% of Attacks"},
    )
    plt.title("Target Preferences by Terrorist Group (%)")
    plt.tight_layout()
    plt.savefig("group_targets_heatmap.png", dpi=150)
    plt.show()
    print("Saved: group_targets_heatmap.png")


def analyze_group_geographic_spread(df, top_n=15):
    """Analyzes geographic spread of major groups."""
    df_known = df[df["Group"] != "Unknown"]

    group_geo = df_known.groupby("Group").agg(
        {"Country": "nunique", "Region": "nunique", "Year": "count"}
    )
    group_geo.columns = ["Countries", "Regions", "Attacks"]
    group_geo = group_geo[group_geo["Attacks"] >= 100]  # Filter for significant groups
    group_geo = group_geo.nlargest(top_n, "Countries")

    fig, ax = plt.subplots(figsize=(12, 8))
    x = np.arange(len(group_geo))
    width = 0.35

    bars1 = ax.barh(
        x - width / 2,
        group_geo["Countries"],
        width,
        label="Countries",
        color="steelblue",
    )
    bars2 = ax.barh(
        x + width / 2, group_geo["Regions"], width, label="Regions", color="orange"
    )

    ax.set_yticks(x)
    ax.set_yticklabels(group_geo.index)
    ax.set_xlabel("Count")
    ax.set_title("Geographic Spread of Terrorist Groups")
    ax.legend()
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("group_geographic_spread.png", dpi=150)
    plt.show()
    print("Saved: group_geographic_spread.png")

    print("\n" + "=" * 60)
    print("MOST GEOGRAPHICALLY SPREAD GROUPS")
    print("=" * 60)
    for group, row in group_geo.iterrows():
        print(
            f"{group}: {int(row['Countries'])} countries, {int(row['Regions'])} regions"
        )


def analyze_central_asia_groups(df):
    """Analyzes terrorist groups active in Central Asia."""
    ca_df = df[df["Region"] == "Central Asia"]
    ca_df = ca_df[ca_df["Group"] != "Unknown"]

    if ca_df.empty:
        print("No known group data for Central Asia.")
        return

    group_stats = ca_df.groupby("Group").agg(
        {"Year": ["count", "min", "max"], "Killed": "sum", "Country": "nunique"}
    )
    group_stats.columns = ["Attacks", "First_Year", "Last_Year", "Killed", "Countries"]
    group_stats = group_stats.sort_values("Attacks", ascending=False)

    plt.figure(figsize=(12, 6))
    cmap = plt.get_cmap("Reds")
    colors = cmap(np.linspace(0.3, 0.9, len(group_stats)))
    plt.barh(group_stats.index, group_stats["Attacks"], color=colors)
    plt.xlabel("Number of Attacks")
    plt.title("Terrorist Groups in Central Asia")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("central_asia_groups.png", dpi=150)
    plt.show()
    print("Saved: central_asia_groups.png")

    print("\n" + "=" * 60)
    print("TERRORIST GROUPS IN CENTRAL ASIA")
    print("=" * 60)
    for group, row in group_stats.iterrows():
        print(f"{group}: {int(row['Attacks'])} attacks, {int(row['Killed'])} killed")


if __name__ == "__main__":
    df = load_data()
    if df is not None:
        df = prepare_data(df)

        analyze_most_active_groups(df)
        analyze_group_activity_timeline(df)
        analyze_group_methods(df)
        analyze_group_targets(df)
        analyze_group_geographic_spread(df)
        analyze_central_asia_groups(df)
