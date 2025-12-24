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
    plt.savefig("kazakhstan_attacks_by_city.png")
    plt.show()


if __name__ == "__main__":
    file_to_use = "gtd.xlsx"
    gtd_df = load_data(file_to_use)

    if gtd_df is not None:
        gtd_df.rename(
            columns={
                "iyear": "Year",
                "imonth": "Month",
                "iday": "Day",
                "country_txt": "Country",
                "provstate": "state",
                "region_txt": "Region",
                "attacktype1_txt": "AttackType",
                "target1": "Target",
                "nkill": "Killed",
                "nwound": "Wounded",
                "summary": "Summary",
                "gname": "Group",
                "targtype1_txt": "Target_type",
                "weaptype1_txt": "Weapon_type",
                "motive": "Motive",
            },
            inplace=True,
        )

        # Rank countries by number of attacks
        attack_ranking = rank_countries_by_metric(gtd_df, "Attacks")
        print("--- Top 10 Countries by Number of Attacks ---")
        print(attack_ranking.head(10))
        kaz_attack_rank = attack_ranking[attack_ranking["Country"] == "Kazakhstan"]
        if not kaz_attack_rank.empty:
            print(f"\nKazakhstan's Rank (Attacks): {kaz_attack_rank.index[0] + 1}")

        # Rank countries by casualties
        casualties_ranking = rank_countries_by_metric(gtd_df, "Casualties")
        print("\n--- Top 10 Countries by Casualties (Killed + Wounded) ---")
        print(casualties_ranking.head(10))
        kaz_casualties_rank = casualties_ranking[
            casualties_ranking["Country"] == "Kazakhstan"
        ]
        if not kaz_casualties_rank.empty:
            print(
                f"\nKazakhstan's Rank (Casualties): {kaz_casualties_rank.index[0] + 1}"
            )

        # Detailed analysis for Kazakhstan
        analyze_kazakhstan_data(gtd_df)
