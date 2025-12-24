import pandas as pd
import os

def create_mini_dataset(input_file, output_file, num_rows=1000):
    """
    Creates a smaller version of an Excel file.

    Args:
        input_file (str): Path to the input Excel file.
        output_file (str): Path to the output Excel file.
        num_rows (int): Number of rows to include in the smaller file.
    """
    try:
        df = pd.read_excel(input_file)
        print(f"Successfully read {input_file}")

        # The first row is the header, so we take num_rows of data
        mini_df = df.head(num_rows)

        mini_df.to_excel(output_file, index=False)
        print(f"Successfully created {output_file} with {num_rows} rows.")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Use absolute paths
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(workspace_dir, 'gtd.xlsx')
    output_path = os.path.join(workspace_dir, 'gtd-mini.xlsx')

    create_mini_dataset(input_path, output_path, num_rows=1000)

