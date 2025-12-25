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


def plot_attacks_by_region(df):
    """
    Plots the number of terrorist attacks by region.
    """
    plt.figure(figsize=(12, 8))
    sns.countplot(y="Region", data=df, order=df["Region"].value_counts().index)
    plt.title("Number of Terrorist Attacks by Region")
    plt.xlabel("Number of Attacks")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig("attacks_by_region.png")
    plt.show()


def plot_attacks_over_time_comparison(df):
    """
    Plots the number of terrorist attacks over time for the world, Central Asia, and Kazakhstan.
    """
    world_attacks = df.groupby("Year").size()

    central_asia_df = df[df["Region"] == "Central Asia"]
    central_asia_attacks = central_asia_df.groupby("Year").size()

    kazakhstan_df = df[df["Country"] == "Kazakhstan"]
    kazakhstan_attacks = kazakhstan_df.groupby("Year").size()

    plt.figure(figsize=(15, 7))
    plt.plot(world_attacks.index, world_attacks.values, label="World")
    plt.plot(
        central_asia_attacks.index, central_asia_attacks.values, label="Central Asia"
    )
    plt.plot(kazakhstan_attacks.index, kazakhstan_attacks.values, label="Kazakhstan")

    plt.title("Number of Terrorist Attacks Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Attacks")
    plt.legend()
    plt.grid(True)
    plt.savefig("attachments/attacks_over_time_comparison.png")
    plt.show()


def run_analysis():
    # For development, use the smaller dataset
    # file_to_use = 'gtd-mini.xlsx'
    # For final analysis, you would switch to 'gtd.xlsx'
    file_to_use = "gtd.xlsx"

    gtd_df = load_data(file_to_use)

    if gtd_df is not None:
        # Rename columns for easier access
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

        # The user wants to focus on continents, but the dataset has 'region'.
        # Let's start by analyzing the regions first.
        plot_attacks_by_region(gtd_df)

        # Now, let's do the time-series comparison
        plot_attacks_over_time_comparison(gtd_df)


if __name__ == "__main__":
    run_analysis()
