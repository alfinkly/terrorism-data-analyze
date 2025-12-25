"""
Decade Comparison Analysis
Analyzes how terrorism has evolved across different decades.
"""

import pandas as pd
import matplotlib.pyplot as plt
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
    df["Decade"] = (df["Year"] // 10) * 10
    df["Decade_Label"] = df["Decade"].astype(str) + "s"
    return df


def analyze_decade_overview(df):
    """Provides overview statistics by decade."""
    decade_stats = df.groupby("Decade_Label").agg(
        {
            "Year": "count",
            "Killed": "sum",
            "Wounded": "sum",
            "Country": "nunique",
            "Group": "nunique",
        }
    )
    decade_stats.columns = [
        "Attacks",
        "Killed",
        "Wounded",
        "Countries_Affected",
        "Active_Groups",
    ]
    decade_stats["Avg_Killed_Per_Attack"] = (
        decade_stats["Killed"] / decade_stats["Attacks"]
    ).round(2)

    print("\n" + "=" * 70)
    print("TERRORISM BY DECADE - OVERVIEW")
    print("=" * 70)
    print(decade_stats.to_string())

    return decade_stats


def plot_decade_attacks(df):
    """Plots attack counts by decade."""
    decade_counts = df["Decade_Label"].value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    cmap = plt.get_cmap("Reds")
    colors = cmap(np.linspace(0.3, 0.9, len(decade_counts)))
    bars = plt.bar(decade_counts.index, decade_counts.values, color=colors)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.xlabel("Decade")
    plt.ylabel("Number of Attacks")
    plt.title("Terrorist Attacks by Decade")
    plt.tight_layout()
    plt.savefig("attacks_by_decade.png", dpi=150)
    plt.show()
    print("Saved: attacks_by_decade.png")


def plot_decade_casualties(df):
    """Plots casualties by decade."""
    decade_casualties = (
        df.groupby("Decade_Label").agg({"Killed": "sum", "Wounded": "sum"}).sort_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(decade_casualties))
    width = 0.35

    bars1 = ax.bar(
        x - width / 2,
        decade_casualties["Killed"],
        width,
        label="Killed",
        color="darkred",
    )
    bars2 = ax.bar(
        x + width / 2,
        decade_casualties["Wounded"],
        width,
        label="Wounded",
        color="orange",
    )

    ax.set_xlabel("Decade")
    ax.set_ylabel("Count")
    ax.set_title("Terrorism Casualties by Decade")
    ax.set_xticks(x)
    ax.set_xticklabels(decade_casualties.index)
    ax.legend()
    plt.tight_layout()
    plt.savefig("casualties_by_decade.png", dpi=150)
    plt.show()
    print("Saved: casualties_by_decade.png")


def analyze_attack_type_evolution(df):
    """Analyzes how attack types have changed across decades."""
    attack_decade = (
        pd.crosstab(df["Decade_Label"], df["AttackType"], normalize="index") * 100
    )

    plt.figure(figsize=(14, 8))
    attack_decade.plot(kind="bar", stacked=True, figsize=(14, 8), colormap="tab20")
    plt.xlabel("Decade")
    plt.ylabel("Percentage")
    plt.title("Evolution of Attack Types by Decade")
    plt.legend(title="Attack Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("attack_type_evolution.png", dpi=150)
    plt.show()
    print("Saved: attack_type_evolution.png")


def analyze_regional_shift(df):
    """Analyzes how terrorism hotspots have shifted across decades."""
    region_decade = (
        pd.crosstab(df["Decade_Label"], df["Region"], normalize="index") * 100
    )

    # Get top 6 regions overall
    top_regions = df["Region"].value_counts().nlargest(6).index.tolist()
    region_decade_top = region_decade[top_regions]

    plt.figure(figsize=(14, 6))
    for region in top_regions:
        plt.plot(
            region_decade_top.index,
            region_decade_top[region],
            marker="o",
            linewidth=2,
            label=region,
        )

    plt.xlabel("Decade")
    plt.ylabel("Percentage of Global Attacks")
    plt.title("Shifting Terrorism Hotspots by Decade")
    plt.legend(title="Region")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("regional_shift_by_decade.png", dpi=150)
    plt.show()
    print("Saved: regional_shift_by_decade.png")


def analyze_weapon_evolution(df):
    """Analyzes how weapon preferences have changed."""
    weapon_decade = (
        pd.crosstab(df["Decade_Label"], df["Weapon_type"], normalize="index") * 100
    )

    plt.figure(figsize=(14, 8))
    weapon_decade.plot(kind="bar", stacked=True, figsize=(14, 8), colormap="Set3")
    plt.xlabel("Decade")
    plt.ylabel("Percentage")
    plt.title("Evolution of Weapon Types by Decade")
    plt.legend(title="Weapon Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("attachments/weapon_evolution.png", dpi=150)
    plt.show()
    print("Saved: weapon_evolution.png")


def analyze_target_evolution(df):
    """Analyzes how target preferences have changed."""
    # Get top 8 target types
    top_targets = df["Target_type"].value_counts().nlargest(8).index.tolist()
    df_top = df[df["Target_type"].isin(top_targets)]

    target_decade = (
        pd.crosstab(df_top["Decade_Label"], df_top["Target_type"], normalize="index")
        * 100
    )

    plt.figure(figsize=(14, 6))
    for target in top_targets:
        if target in target_decade.columns:
            plt.plot(
                target_decade.index,
                target_decade[target],
                marker="s",
                linewidth=2,
                label=target,
            )

    plt.xlabel("Decade")
    plt.ylabel("Percentage of Attacks")
    plt.title("Evolution of Target Types by Decade")
    plt.legend(title="Target Type", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("attachments/target_evolution.png", dpi=150)
    plt.show()
    print("Saved: target_evolution.png")


def run_analysis():
    """Main function to run the entire analysis pipeline."""
    df = load_data()
    if df is None:
        return

    # Prepare data
    df_clean = prepare_data(df)

    # --- Decade Overview ---
    analyze_decade_overview(df_clean)

    # --- Overall Trend Comparison ---
    print("--- Comparing Overall Attack Trends Across Decades ---")
    plot_decade_attacks(df_clean)

    # --- Regional Shift Analysis ---
    print("\n--- Analyzing Regional Shifts in Terrorism Across Decades ---")
    analyze_regional_shift(df_clean)

    # --- Tactical Evolution Analysis ---
    print("\n--- Analyzing Evolution of Attack Types Across Decades ---")
    analyze_attack_type_evolution(df_clean)

    # --- Weapon Preference Analysis ---
    print("\n--- Analyzing Evolution of Weapon Types Across Decades ---")
    analyze_weapon_evolution(df_clean)

    # --- Target Preference Analysis ---
    print("\n--- Analyzing Evolution of Target Types Across Decades ---")
    analyze_target_evolution(df_clean)

    print("\nDecade comparison analysis complete. Plots saved to 'attachments' directory.")


if __name__ == "__main__":
    run_analysis()
