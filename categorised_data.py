import pandas as pd

# Load the original data
input_file = "sonar_issues_report.csv"  # Replace with your actual CSV filename
df = pd.read_csv(input_file)

# Extract unique values from Column A
unique_values = df["A"].unique()

# Create a new Excel file
output_file = "categorized_sonar_issues.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for value in unique_values:
        # Filter data for each unique value
        subset = df[df["A"] == value][["A", "B"]]
        
        # Write to a separate sheet named after the unique value
        subset.to_excel(writer, sheet_name=str(value), index=False)

print(f"Excel file '{output_file}' created successfully with categorized sheets.")
