import pandas as pd
from countryinfo import CountryInfo

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

def get_population(country_name):
    """
    Gets the population of a country.
    """
    try:
        # Handle special cases for country names
        if country_name == 'Russia':
            country_name = 'Russian Federation'
        elif country_name == 'South Korea':
            country_name = 'Korea, Republic of'
        elif country_name == 'West Bank and Gaza Strip':
            return 5044000 # Approximate population

        country = CountryInfo(country_name)
        return country.population()
    except (KeyError, ValueError):
        return None

def rank_by_attacks_per_capita(df):
    """
    Ranks countries by terrorist attacks per capita.
    """
    attacks_by_country = df['Country'].value_counts().reset_index()
    attacks_by_country.columns = ['Country', 'AttackCount']

    attacks_by_country['Population'] = attacks_by_country['Country'].apply(get_population)

    # Remove countries where population could not be found
    attacks_by_country.dropna(subset=['Population'], inplace=True)

    attacks_by_country['AttacksPerCapita'] = (attacks_by_country['AttackCount'] / attacks_by_country['Population']) * 1000000 # Attacks per million people

    # Sort by attacks per capita
    ranked_df = attacks_by_country.sort_values(by='AttacksPerCapita', ascending=False)

    return ranked_df

if __name__ == "__main__":
    file_to_use = 'gtd.xlsx'
    gtd_df = load_data(file_to_use)

    if gtd_df is not None:
        gtd_df.rename(columns={'country_txt':'Country'}, inplace=True)

        per_capita_ranking = rank_by_attacks_per_capita(gtd_df)

        print("--- Top 20 Countries by Attacks Per Capita (per million people) ---")
        print(per_capita_ranking.head(20))

        kaz_rank = per_capita_ranking[per_capita_ranking['Country'] == 'Kazakhstan']

        if not kaz_rank.empty:
            # Get the rank by finding the index in the sorted dataframe
            rank_value = per_capita_ranking.index.get_loc(kaz_rank.index[0]) + 1
            print(f"\nKazakhstan's Rank (Attacks Per Capita): {rank_value}")
        else:
            print("\nCould not determine Kazakhstan's rank.")

