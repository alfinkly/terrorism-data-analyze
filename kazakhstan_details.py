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
    plt.savefig("attachments/kazakhstan_weapon_types.png")
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
    plt.savefig("attachments/kazakhstan_terrorist_groups.png")
    plt.show()

    # Print the top 3 groups
    top_groups = kaz_df["Group"].value_counts().nlargest(3)
    print("\n--- Top 3 Terrorist Groups in Kazakhstan ---")
    print(top_groups)


def run_analysis():
    """
    Main function to run the detailed analysis for Kazakhstan.
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
        # Filter data for Kazakhstan
        df_kazakhstan = df[df["Country"] == "Kazakhstan"].copy()

        if df_kazakhstan.empty:
            print("No data found for Kazakhstan in the dataset.")
            return

        print(f"Found {len(df_kazakhstan)} total records for Kazakhstan.")

        # --- Analyze Weapon Types ---
        analyze_kazakhstan_weapon_types(df_kazakhstan)


        # --- Analyze Terrorist Groups ---
        analyze_kazakhstan_terrorist_groups(df_kazakhstan)

        print("\nDetailed analysis for Kazakhstan complete. Plots saved to 'attachments' directory.")


if __name__ == "__main__":
    run_analysis()
