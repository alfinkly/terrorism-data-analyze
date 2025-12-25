"""
Success Rate Analysis
Analyzes attack success rates by type, region, weapon, and terrorist group.
"""

import pandas as pd
import matplotlib.pyplot as plt

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
            "success": "Success",
            "gname": "Group",
            "targtype1_txt": "Target_type",
            "weaptype1_txt": "Weapon_type",
        },
        inplace=True,
    )
    return df


def analyze_success_by_attack_type(df):
    """Analyzes success rates by attack type."""
    success_by_type = df.groupby("AttackType").agg(
        {"Success": ["sum", "count", "mean"]}
    )
    success_by_type.columns = ["Successful", "Total", "Success_Rate"]
    success_by_type = success_by_type.sort_values("Success_Rate", ascending=False)

    plt.figure(figsize=(12, 6))
    cmap = plt.get_cmap("RdYlGn")
    colors = cmap(success_by_type["Success_Rate"])
    bars = plt.barh(
        success_by_type.index, success_by_type["Success_Rate"] * 100, color=colors
    )
    plt.xlabel("Success Rate (%)")
    plt.title("Attack Success Rate by Attack Type")
    plt.xlim(0, 100)
    for bar, rate in zip(bars, success_by_type["Success_Rate"]):
        plt.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{rate * 100:.1f}%",
            va="center",
        )
    plt.tight_layout()
    plt.savefig("success_by_attack_type.png", dpi=150)
    plt.show()
    print("Saved: success_by_attack_type.png")

    print("\n" + "=" * 60)
    print("SUCCESS RATE BY ATTACK TYPE")
    print("=" * 60)
    for attack_type, row in success_by_type.iterrows():
        print(
            f"{attack_type}: {row['Success_Rate'] * 100:.1f}% ({int(row['Successful']):,}/{int(row['Total']):,})"
        )


def analyze_success_by_region(df):
    """Analyzes success rates by region."""
    success_by_region = df.groupby("Region").agg({"Success": ["sum", "count", "mean"]})
    success_by_region.columns = ["Successful", "Total", "Success_Rate"]
    success_by_region = success_by_region.sort_values("Success_Rate", ascending=False)

    plt.figure(figsize=(12, 6))
    cmap = plt.get_cmap("RdYlGn")
    colors = cmap(success_by_region["Success_Rate"])
    plt.barh(
        success_by_region.index, success_by_region["Success_Rate"] * 100, color=colors
    )
    plt.xlabel("Success Rate (%)")
    plt.title("Attack Success Rate by Region")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig("success_by_region.png", dpi=150)
    plt.show()
    print("Saved: success_by_region.png")


def analyze_success_by_weapon(df):
    """Analyzes success rates by weapon type."""
    success_by_weapon = df.groupby("Weapon_type").agg(
        {"Success": ["sum", "count", "mean"]}
    )
    success_by_weapon.columns = ["Successful", "Total", "Success_Rate"]
    success_by_weapon = success_by_weapon.sort_values("Success_Rate", ascending=False)

    plt.figure(figsize=(12, 6))
    cmap = plt.get_cmap("RdYlGn")
    colors = cmap(success_by_weapon["Success_Rate"])
    plt.barh(
        success_by_weapon.index, success_by_weapon["Success_Rate"] * 100, color=colors
    )
    plt.xlabel("Success Rate (%)")
    plt.title("Attack Success Rate by Weapon Type")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig("success_by_weapon.png", dpi=150)
    plt.show()
    print("Saved: success_by_weapon.png")


def analyze_success_trends(df):
    """Analyzes how success rates have changed over time."""
    yearly_success = df.groupby("Year")["Success"].mean() * 100

    plt.figure(figsize=(14, 5))
    plt.plot(
        yearly_success.index, yearly_success.values, linewidth=2, color="steelblue"
    )
    plt.fill_between(yearly_success.index, yearly_success.values, alpha=0.3)
    plt.axhline(
        y=yearly_success.mean(),
        color="red",
        linestyle="--",
        label=f"Average: {yearly_success.mean():.1f}%",
    )
    plt.xlabel("Year")
    plt.ylabel("Success Rate (%)")
    plt.title("Attack Success Rate Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("attachments/success_trends.png", dpi=150)
    plt.show()
    print("Saved: success_trends.png")


def analyze_top_groups_success(df, min_attacks=50):
    """Analyzes success rates of major terrorist groups."""
    df_known = df[df["Group"] != "Unknown"]

    group_stats = df_known.groupby("Group").agg({"Success": ["sum", "count", "mean"]})
    group_stats.columns = ["Successful", "Total", "Success_Rate"]
    group_stats = group_stats[group_stats["Total"] >= min_attacks]
    group_stats = group_stats.nlargest(20, "Total")
    group_stats = group_stats.sort_values("Success_Rate", ascending=True)

    plt.figure(figsize=(12, 8))
    cmap = plt.get_cmap("RdYlGn")
    colors = cmap(group_stats["Success_Rate"])
    plt.barh(group_stats.index, group_stats["Success_Rate"] * 100, color=colors)
    plt.xlabel("Success Rate (%)")
    plt.title(f"Success Rate of Major Terrorist Groups (min {min_attacks} attacks)")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig("attachments/success_by_group.png", dpi=150)
    plt.show()
    print("Saved: success_by_group.png")


def run_analysis():
    """Main function to run the entire analysis pipeline."""
    df = load_data()
    if df is None:
        return

    # Prepare data
    df_clean = prepare_data(df)

    # --- Analysis by Attack Type ---
    analyze_success_by_attack_type(df_clean)

    # --- Analysis by Region ---
    analyze_success_by_region(df_clean)

    # --- Analysis by Weapon Type ---
    analyze_success_by_weapon(df_clean)

    # --- Analysis by Top Terrorist Groups ---
    analyze_top_groups_success(df_clean)

    # --- Temporal Analysis of Success Rates ---
    analyze_success_trends(df_clean)

    print("\nSuccess rate analysis complete. Plots saved to 'attachments' directory.")


if __name__ == "__main__":
    run_analysis()

