"""
Seasonal Patterns Analysis
Analyzes monthly, weekly, and seasonal trends in terrorist attacks.
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

    # Filter out invalid months (0 means unknown)
    df = df[df["Month"] > 0]

    # Add season
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    df["Season"] = df["Month"].apply(get_season)

    return df


def analyze_monthly_patterns(df):
    """Analyzes attack frequency by month."""
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    monthly_attacks = df["Month"].value_counts().sort_index()
    monthly_casualties = df.groupby("Month")["Killed"].sum()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Attacks by month
    ax1 = axes[0]
    cmap = plt.get_cmap("RdYlBu_r")
    colors = cmap(np.linspace(0.2, 0.8, 12))
    bars = ax1.bar(month_names, monthly_attacks.values, color=colors)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Number of Attacks")
    ax1.set_title("Terrorist Attacks by Month (All Years)")
    ax1.axhline(
        y=monthly_attacks.mean(),
        color="red",
        linestyle="--",
        label=f"Average: {monthly_attacks.mean():,.0f}",
    )
    ax1.legend()

    # Casualties by month
    ax2 = axes[1]
    ax2.bar(month_names, monthly_casualties.values, color="darkred", alpha=0.7)
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Total Killed")
    ax2.set_title("Terrorism Deaths by Month (All Years)")
    ax2.axhline(
        y=monthly_casualties.mean(),
        color="orange",
        linestyle="--",
        label=f"Average: {monthly_casualties.mean():,.0f}",
    )
    ax2.legend()

    plt.tight_layout()
    plt.savefig("monthly_patterns.png", dpi=150)
    plt.show()
    print("Saved: monthly_patterns.png")

    print("\n" + "=" * 50)
    print("MONTHLY ATTACK DISTRIBUTION")
    print("=" * 50)
    for i, (month, count) in enumerate(zip(month_names, monthly_attacks.values), 1):
        pct = count / monthly_attacks.sum() * 100
        print(f"{month}: {count:,} attacks ({pct:.1f}%)")


def analyze_seasonal_patterns(df):
    """Analyzes attack patterns by season."""
    season_order = ["Winter", "Spring", "Summer", "Autumn"]

    seasonal_stats = (
        df.groupby("Season")
        .agg({"Year": "count", "Killed": "sum", "Wounded": "sum"})
        .reindex(season_order)
    )
    seasonal_stats.columns = ["Attacks", "Killed", "Wounded"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]

    # Pie chart for attacks
    ax1 = axes[0]
    ax1.pie(
        seasonal_stats["Attacks"],
        labels=season_order,
        autopct="%1.1f%%",
        colors=colors,
        explode=[0.02] * 4,
    )
    ax1.set_title("Attack Distribution by Season")

    # Bar chart for casualties
    ax2 = axes[1]
    x = np.arange(len(season_order))
    width = 0.35
    ax2.bar(
        x - width / 2, seasonal_stats["Killed"], width, label="Killed", color="darkred"
    )
    ax2.bar(
        x + width / 2, seasonal_stats["Wounded"], width, label="Wounded", color="orange"
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(season_order)
    ax2.set_ylabel("Count")
    ax2.set_title("Casualties by Season")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("seasonal_patterns.png", dpi=150)
    plt.show()
    print("Saved: seasonal_patterns.png")

    print("\n" + "=" * 50)
    print("SEASONAL STATISTICS")
    print("=" * 50)
    print(seasonal_stats.to_string())


def analyze_regional_seasonal_patterns(df):
    """Analyzes how seasonal patterns vary by region."""
    # Get top 6 regions by attack count
    top_regions = df["Region"].value_counts().nlargest(6).index.tolist()
    df_top = df[df["Region"].isin(top_regions)]

    season_order = ["Winter", "Spring", "Summer", "Autumn"]

    # Create pivot table
    pivot = pd.crosstab(df_top["Region"], df_top["Season"])[season_order]
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    plt.figure(figsize=(12, 6))
    pivot_pct.plot(
        kind="bar", width=0.8, color=["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
    )
    plt.xlabel("Region")
    plt.ylabel("Percentage of Attacks")
    plt.title("Seasonal Attack Distribution by Region")
    plt.legend(title="Season")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("regional_seasonal_patterns.png", dpi=150)
    plt.show()
    print("Saved: regional_seasonal_patterns.png")


def analyze_heatmap_month_year(df):
    """Creates a heatmap of attacks by month and year."""
    # Filter to recent decades for clarity
    df_recent = df[df["Year"] >= 1990]

    pivot = pd.crosstab(df_recent["Year"], df_recent["Month"])

    plt.figure(figsize=(14, 10))
    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        annot=False,
        fmt="d",
        xticklabels=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )
    plt.xlabel("Month")
    plt.ylabel("Year")
    plt.title("Terrorist Attacks Heatmap (1990-Present)")
    plt.tight_layout()
    plt.savefig("attachments/attacks_heatmap.png", dpi=150)
    plt.show()
    print("Saved: attacks_heatmap.png")


def analyze_day_patterns(df):
    """Analyzes attack patterns by day of month."""
    # Filter out invalid days (0 means unknown)
    df_valid = df[df["Day"] > 0]

    daily_attacks = df_valid["Day"].value_counts().sort_index()

    plt.figure(figsize=(14, 5))
    plt.bar(daily_attacks.index, daily_attacks.values, color="steelblue", alpha=0.7)
    plt.axhline(
        y=daily_attacks.mean(),
        color="red",
        linestyle="--",
        label=f"Average: {daily_attacks.mean():,.0f}",
    )
    plt.xlabel("Day of Month")
    plt.ylabel("Number of Attacks")
    plt.title("Terrorist Attacks by Day of Month")
    plt.xticks(range(1, 32))
    plt.legend()
    plt.tight_layout()
    plt.savefig("attachments/daily_patterns.png", dpi=150)
    plt.show()
    print("Saved: daily_patterns.png")

    # Find notable days
    print("\n" + "=" * 50)
    print("NOTABLE DAYS")
    print("=" * 50)
    print(
        f"Most attacks on day: {daily_attacks.idxmax()} ({daily_attacks.max():,} attacks)"
    )
    print(
        f"Fewest attacks on day: {daily_attacks.idxmin()} ({daily_attacks.min():,} attacks)"
    )


def run_analysis():
    """Main function to run the entire analysis pipeline."""
    df = load_data()
    if df is None:
        return

    # Prepare data
    df_clean = prepare_data(df)

    # --- Monthly and Quarterly Analysis ---
    analyze_monthly_patterns(df_clean)

    # --- Day of the Week Analysis ---
    analyze_day_patterns(df_clean)

    # --- Seasonal Analysis (Meteorological Seasons) ---
    analyze_seasonal_patterns(df_clean)

    # --- Heatmap of Year vs. Month ---
    analyze_heatmap_month_year(df_clean)

    # --- Regional Seasonal Analysis ---
    analyze_regional_seasonal_patterns(df_clean)

    print("\nSeasonal patterns analysis complete. Plots saved to 'attachments' directory.")


if __name__ == "__main__":
    run_analysis()
