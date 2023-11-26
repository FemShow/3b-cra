import pandas as pd

# Define the file path
input_file_path = '/Users/femisokoya/Documents/GitHub/3b-cra/melted1_results.csv'
output_file_path = '/Users/femisokoya/Documents/GitHub/3b-cra/cra-convert.csv'

# Read the CSV file
df = pd.read_csv(input_file_path)

# List of columns to convert to 2 decimal point
columns_to_convert = [
    'Change'
]

# Convert Change columns to 2 decimal point floats
df[columns_to_convert] = df[columns_to_convert].round(2).astype(float)

# convert the year column
df['Year'] = df['Year'].str.replace(r'-(\d{2})$', r'-20\1', regex=True)

# Iterate through 'Value' and 'Change' columns
for col in ['Value', 'Change']:
    # Create a new column with '-obsStatus' suffix
    obs_status_col = col + '-obsStatus'

    # Insert the new column after the current column
    col_index = df.columns.get_loc(col)
    df.insert(col_index + 1, obs_status_col, '')

    # Fill 'z' where there is a '' or null in the corresponding column
    df.loc[df[col].isna() | (df[col] == ''), obs_status_col] = 'z'

# Save the result to a new CSV file
df.to_csv(output_file_path, index=False)
