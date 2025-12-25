import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_path):
    """
    Loads the terrorism data from an Excel file.
    """
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None


def rank_countries_by_metric(df, metric, ascending=False):
    """
    Ranks countries by a given metric (e.g., number of attacks, casualties).
    """
    if metric == "Attacks":
        ranking = df["Country"].value_counts().reset_index()
        ranking.columns = ["Country", "Count"]
    elif metric == "Casualties":
        # Ensure 'Killed' and 'Wounded' are numeric, fill NaNs with 0
        df["Killed"] = pd.to_numeric(df["Killed"], errors="coerce").fillna(0)
        df["Wounded"] = pd.to_numeric(df["Wounded"], errors="coerce").fillna(0)
        df["Casualties"] = df["Killed"] + df["Wounded"]
        ranking = (
            df.groupby("Country")["Casualties"]
            .sum()
            .sort_values(ascending=ascending)
            .reset_index()
        )
    else:
        print(f"Metric '{metric}' not supported.")
        return None

    return ranking


def analyze_kazakhstan_data(df):
    """
    Performs a detailed analysis of terrorism data for Kazakhstan.
    """
    kaz_df = df[df["Country"] == "Kazakhstan"].copy()

    if kaz_df.empty:
        print("No data available for Kazakhstan.")
        return

    print("\n--- Analysis for Kazakhstan ---")

    # Ranking of attack types in Kazakhstan
    plt.figure(figsize=(10, 6))
    sns.countplot(
        y="AttackType", data=kaz_df, order=kaz_df["AttackType"].value_counts().index
    )
    plt.title("Attack Types in Kazakhstan")
    plt.xlabel("Number of Attacks")
    plt.ylabel("Attack Type")
    plt.tight_layout()
    plt.savefig("kazakhstan_attack_types.png")
    plt.show()

    # Ranking of target types in Kazakhstan
    plt.figure(figsize=(10, 6))
    sns.countplot(
        y="Target_type", data=kaz_df, order=kaz_df["Target_type"].value_counts().index
    )
    plt.title("Target Types in Kazakhstan")
    plt.xlabel("Number of Attacks")
    plt.ylabel("Target Type")
    plt.tight_layout()
    plt.savefig("kazakhstan_target_types.png")
    plt.show()

    # Ranking of cities by attacks in Kazakhstan
    plt.figure(figsize=(10, 6))
    sns.countplot(y="city", data=kaz_df, order=kaz_df["city"].value_counts().index)
    plt.title("Attacks by City in Kazakhstan")
    plt.xlabel("Number of Attacks")
    plt.ylabel("City")
    plt.tight_layout()
    plt.savefig("attachments/kazakhstan_attacks_by_city.png")
    plt.show()


def run_analysis():
    """
    Main function to run the Kazakhstan rankings analysis.
    """
    file_path = "gtd.xlsx"
    df = load_data(file_path)

    if df is not None:
        # Rename columns for consistency
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

        # --- Rank by Number of Attacks ---
        print("--- Ranking Countries by Number of Attacks ---")
        attacks_rank_df = rank_countries_by_metric(df, "Attacks")
        # find_and_display_kazakhstan_rank(attacks_rank_df, "Rank by Attacks", "Number of Attacks")
        # plot_top_countries(
        #     attacks_rank_df,
        #     "Number of Attacks",
        #     "Top 20 Countries by Number of Terrorist Attacks",
        #     "attachments/top_20_countries_by_attacks.png",
        # )

        # --- Rank by Total Casualties ---
        print("\n--- Ranking Countries by Total Casualties ---")
        casualties_rank_df = rank_countries_by_metric(df, "Casualties")
        # find_and_display_kazakhstan_rank(casualties_rank_df, "Rank by Casualties", "Total Casualties")
        # plot_top_countries(
        #     casualties_rank_df,
        #     "Total Casualties",
        #     "Top 20 Countries by Total Casualties from Terrorism",
        #     "attachments/top_20_countries_by_casualties.png",
        # )

        # --- Detailed analysis for Kazakhstan ---
        analyze_kazakhstan_data(df)

        print("\nAnalysis complete. Plots and rankings have been generated.")


if __name__ == "__main__":
    run_analysis()
