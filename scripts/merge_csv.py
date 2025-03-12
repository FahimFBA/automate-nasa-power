import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
import shutil
import pandas as pd


# Custom print for user feedback with emojis
def print_progress(message, emoji="✅"):
    print(f"{emoji} {message}")


def create_cleaned_dir(data_dir, cleaned_dir):
    # Check if the cleaned directory exists, if not, create it
    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)
        print_progress(f"Created cleaned directory: {cleaned_dir}")
    else:
        print(f"⚠️ {cleaned_dir} already exists!")


def clean_and_copy_csv_files(data_dir, cleaned_dir):
    # Loop through all CSV files in the data directory
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(data_dir, file_name)
            cleaned_file_path = os.path.join(cleaned_dir, file_name)

            # Copy the CSV file to the cleaned directory
            shutil.copy(file_path, cleaned_file_path)

            print_progress(f"Cleaning file: {file_name}")

            # Open the CSV file and remove the header (parameters and unwanted lines)
            with open(cleaned_file_path, 'r') as file:
                lines = file.readlines()

            # Flag to indicate if we've reached the end of the header
            in_header = False
            cleaned_lines = []

            # Loop through the lines to remove header content
            for line in lines:
                if "-BEGIN HEADER-" in line:
                    in_header = True  # Start skipping lines after this
                if in_header:
                    if "-END HEADER-" in line:
                        in_header = False  # Stop skipping lines after this
                    continue  # Skip the header lines
                cleaned_lines.append(line)  # Add only the actual data lines

            # Write the cleaned content back to the file
            with open(cleaned_file_path, 'w') as file:
                file.writelines(cleaned_lines)

            print_progress(f"Finished cleaning: {file_name}", "✔️")


def merge_csv_files(cleaned_dir, merged_dir, output_file):
    # Initialize a list to hold the dataframes
    df_list = []

    print_progress("Merging CSV files...")

    # Loop through all CSV files in the cleaned directory
    for file_name in os.listdir(cleaned_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(cleaned_dir, file_name)
            try:
                # Read each CSV file and append the dataframe to the list
                df = pd.read_csv(file_path, on_bad_lines='skip', header=0)
                df_list.append(df)
                print_progress(f"Added file: {file_name}", "📄")
            except pd.errors.ParserError as e:
                print(
                    f"⚠️ Skipping file {file_name} due to parsing error: {e}")

    if df_list:
        # Merge all the dataframes into one
        merged_df = pd.concat(df_list, ignore_index=True)

        # Ensure merged directory exists
        if not os.path.exists(merged_dir):
            os.makedirs(merged_dir)
            print_progress(f"Created merged directory: {merged_dir}")

        # Ensure output file path is inside 'data/merged/'
        output_path = os.path.join(merged_dir, output_file)

        # Save the merged dataframe to the output file
        merged_df.to_csv(output_path, index=False)
        print_progress(f"Merged file saved as {output_path}", "🎉")
    else:
        print("⚠️ No valid CSV files to merge.")


def main():
    data_dir = 'data'  # Path to your downloaded data directory
    # Create 'cleaned' subdirectory inside data/
    cleaned_dir = os.path.join(data_dir, 'cleaned')
    # Create 'merged' subdirectory inside data/
    merged_dir = os.path.join(data_dir, 'merged')
    output_file = 'merged_data.csv'  # Name of the merged CSV file

    # Step 1: Create cleaned directory
    create_cleaned_dir(data_dir, cleaned_dir)

    # Step 2: Copy and clean CSV files
    clean_and_copy_csv_files(data_dir, cleaned_dir)

    # Step 3: Merge the cleaned CSV files and save inside 'data/merged/'
    merge_csv_files(cleaned_dir, merged_dir, output_file)


if __name__ == '__main__':
    main()
