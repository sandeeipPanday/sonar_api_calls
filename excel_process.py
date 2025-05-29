import os
import pandas as pd

# Define the directory containing the CSV files
input_directory = "path/to/csv/files"
output_directory = "path/to/output/files"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Process each CSV file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)

        # Ensure proper date-time parsing for "Last Updated At"
        df["Last Updated At"] = pd.to_datetime(df["Last Updated At"], errors='coerce')

        # Drop any rows with invalid dates
        df.dropna(subset=["Last Updated At"], inplace=True)

        # Keep only the latest entry for each project
        latest_entries = df.sort_values("Last Updated At", ascending=False).drop_duplicates(subset=["Project Name"], keep="first")

        # Save the filtered data
        output_file_path = os.path.join(output_directory, filename)
        latest_entries.to_csv(output_file_path, index=False)

print("Processing complete. Filtered files saved in:", output_directory)
