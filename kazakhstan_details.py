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


def analyze_kazakhstan_weapon_types(df):
    """
    Analyzes and plots the types of weapons used in terrorist attacks in Kazakhstan.
    """
    kaz_df = df[df["Country"] == "Kazakhstan"].copy()

    if kaz_df.empty:
        print("No data available for Kazakhstan.")
        return

    print("\n--- Weapon Types Analysis for Kazakhstan ---")

    plt.figure(figsize=(12, 8))
    sns.countplot(
        y="Weapon_type", data=kaz_df, order=kaz_df["Weapon_type"].value_counts().index
    )
    plt.title("Weapon Types Used in Attacks in Kazakhstan")
    plt.xlabel("Number of Incidents")
    plt.ylabel("Weapon Type")
    plt.tight_layout()
    plt.savefig("kazakhstan_weapon_types.png")
    plt.show()

    # Print the top 3 weapon types
    top_weapons = kaz_df["Weapon_type"].value_counts().nlargest(3)
    print("\n--- Top 3 Weapon Types in Kazakhstan ---")
    print(top_weapons)


def analyze_kazakhstan_terrorist_groups(df):
    """
    Analyzes and plots the terrorist groups operating in Kazakhstan.
    """
    kaz_df = df[df["Country"] == "Kazakhstan"].copy()

    # Exclude 'Unknown' groups for a more meaningful analysis
    kaz_df = kaz_df[kaz_df["Group"] != "Unknown"]

    if kaz_df.empty:
        print("No data available for known terrorist groups in Kazakhstan.")
        return

    print("\n--- Terrorist Groups Analysis for Kazakhstan ---")

    plt.figure(figsize=(12, 8))
    sns.countplot(y="Group", data=kaz_df, order=kaz_df["Group"].value_counts().index)
    plt.title("Terrorist Groups Operating in Kazakhstan")
    plt.xlabel("Number of Attacks")
    plt.ylabel("Group")
    plt.tight_layout()
    plt.savefig("kazakhstan_terrorist_groups.png")
    plt.show()

    # Print the top 3 groups
    top_groups = kaz_df["Group"].value_counts().nlargest(3)
    print("\n--- Top 3 Terrorist Groups in Kazakhstan ---")
    print(top_groups)


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

        analyze_kazakhstan_weapon_types(gtd_df)
        analyze_kazakhstan_terrorist_groups(gtd_df)
