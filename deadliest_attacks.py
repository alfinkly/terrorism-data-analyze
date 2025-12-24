"""
Deadliest Attacks Analysis
Analyzes the most lethal terrorist incidents in history and by region.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
            "city": "City",
        },
        inplace=True,
    )

    df["Killed"] = pd.to_numeric(df["Killed"], errors="coerce").fillna(0)
    df["Wounded"] = pd.to_numeric(df["Wounded"], errors="coerce").fillna(0)
    df["Casualties"] = df["Killed"] + df["Wounded"]
    return df


def analyze_deadliest_attacks(df, top_n=20):
    """Analyzes and displays the deadliest attacks in history."""
    print(f"\n{'=' * 60}")
    print(f"TOP {top_n} DEADLIEST TERRORIST ATTACKS IN HISTORY")
    print("=" * 60)

    deadliest = df.nlargest(top_n, "Killed")[
        [
            "Year",
            "Country",
            "City",
            "Group",
            "AttackType",
            "Target",
            "Killed",
            "Wounded",
        ]
    ]

    for i, (_, row) in enumerate(deadliest.iterrows(), 1):
        print(f"\n{i}. {row['Country']}, {row['City']} ({int(row['Year'])})")
        print(f"   Group: {row['Group']}")
        print(f"   Attack Type: {row['AttackType']}")
        print(f"   Killed: {int(row['Killed'])}, Wounded: {int(row['Wounded'])}")

    return deadliest


def plot_deadliest_by_region(df):
    """Plots average casualties per attack by region."""
    region_stats = (
        df.groupby("Region")
        .agg({"Killed": ["sum", "mean"], "Wounded": ["sum", "mean"], "Year": "count"})
        .round(2)
    )
    region_stats.columns = [
        "Total_Killed",
        "Avg_Killed",
        "Total_Wounded",
        "Avg_Wounded",
        "Total_Attacks",
    ]
    region_stats["Avg_Casualties"] = (
        region_stats["Avg_Killed"] + region_stats["Avg_Wounded"]
    )
    region_stats = region_stats.sort_values("Avg_Casualties", ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Average casualties per attack
    ax1 = axes[0]
    colors = sns.color_palette("Reds_r", len(region_stats))
    bars = ax1.barh(region_stats.index, region_stats["Avg_Casualties"], color=colors)
    ax1.set_xlabel("Average Casualties per Attack")
    ax1.set_title("Deadliness by Region (Avg Casualties per Attack)")
    ax1.invert_yaxis()

    # Total casualties
    ax2 = axes[1]
    region_stats_total = region_stats.sort_values("Total_Killed", ascending=False)
    ax2.barh(
        region_stats_total.index,
        region_stats_total["Total_Killed"],
        color="darkred",
        alpha=0.7,
        label="Killed",
    )
    ax2.barh(
        region_stats_total.index,
        region_stats_total["Total_Wounded"],
        left=region_stats_total["Total_Killed"],
        color="orange",
        alpha=0.7,
        label="Wounded",
    )
    ax2.set_xlabel("Total Casualties")
    ax2.set_title("Total Casualties by Region")
    ax2.legend()
    ax2.invert_yaxis()

    plt.tight_layout()
    plt.savefig("deadliest_by_region.png", dpi=150)
    plt.show()
    print("\nSaved: deadliest_by_region.png")

    return region_stats


def plot_deadliest_groups(df, top_n=15):
    """Plots the deadliest terrorist groups."""
    # Exclude Unknown
    df_known = df[df["Group"] != "Unknown"]

    group_stats = df_known.groupby("Group").agg(
        {"Killed": "sum", "Wounded": "sum", "Year": "count"}
    )
    group_stats.columns = ["Total_Killed", "Total_Wounded", "Total_Attacks"]
    group_stats["Total_Casualties"] = (
        group_stats["Total_Killed"] + group_stats["Total_Wounded"]
    )
    group_stats = group_stats.nlargest(top_n, "Total_Killed")

    plt.figure(figsize=(12, 8))
    y_pos = range(len(group_stats))

    plt.barh(
        y_pos, group_stats["Total_Killed"], color="darkred", alpha=0.8, label="Killed"
    )
    plt.barh(
        y_pos,
        group_stats["Total_Wounded"],
        left=group_stats["Total_Killed"],
        color="orange",
        alpha=0.8,
        label="Wounded",
    )

    plt.yticks(y_pos, group_stats.index)
    plt.xlabel("Total Casualties")
    plt.title(f"Top {top_n} Deadliest Terrorist Groups")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("deadliest_groups.png", dpi=150)
    plt.show()
    print("Saved: deadliest_groups.png")

    print(f"\n{'=' * 60}")
    print(f"TOP {top_n} DEADLIEST TERRORIST GROUPS")
    print("=" * 60)
    for i, (group, row) in enumerate(group_stats.iterrows(), 1):
        print(f"{i:2}. {group}")
        print(
            f"    Attacks: {int(row['Total_Attacks']):,} | Killed: {int(row['Total_Killed']):,} | Wounded: {int(row['Total_Wounded']):,}"
        )


def analyze_lethality_trends(df):
    """Analyzes how attack lethality has changed over time."""
    yearly_stats = df.groupby("Year").agg(
        {"Killed": ["sum", "mean"], "Wounded": ["sum", "mean"], "Country": "count"}
    )
    yearly_stats.columns = [
        "Total_Killed",
        "Avg_Killed",
        "Total_Wounded",
        "Avg_Wounded",
        "Attacks",
    ]

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # Total casualties over time
    ax1 = axes[0]
    ax1.fill_between(
        yearly_stats.index,
        yearly_stats["Total_Killed"],
        color="darkred",
        alpha=0.7,
        label="Killed",
    )
    ax1.fill_between(
        yearly_stats.index,
        yearly_stats["Total_Killed"],
        yearly_stats["Total_Killed"] + yearly_stats["Total_Wounded"],
        color="orange",
        alpha=0.7,
        label="Wounded",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Total Casualties")
    ax1.set_title("Total Terrorism Casualties Over Time")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Average lethality per attack
    ax2 = axes[1]
    ax2.plot(
        yearly_stats.index,
        yearly_stats["Avg_Killed"],
        color="darkred",
        linewidth=2,
        label="Avg Killed per Attack",
    )
    ax2.plot(
        yearly_stats.index,
        yearly_stats["Avg_Wounded"],
        color="orange",
        linewidth=2,
        label="Avg Wounded per Attack",
    )
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Average per Attack")
    ax2.set_title("Attack Lethality Trend Over Time")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("lethality_trends.png", dpi=150)
    plt.show()
    print("Saved: lethality_trends.png")


if __name__ == "__main__":
    df = load_data()
    if df is not None:
        df = prepare_data(df)

        analyze_deadliest_attacks(df)
        plot_deadliest_by_region(df)
        plot_deadliest_groups(df)
        analyze_lethality_trends(df)
