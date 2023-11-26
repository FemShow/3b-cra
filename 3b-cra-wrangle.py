import pandas as pd
import numpy as np

# Read the Excel file into a DataFrame, skipping the first 4 rows and reading the first 31 rows
df = pd.read_excel("/Users/femisokoya/Documents/GitHub/CRA/Companies_Register_Activities_2021-22.xls",
                           sheet_name='Table_A1',
                           skiprows=3,
                           nrows=61)

# Melt the DataFrame with 'Corporate body type' as id_vars
melted_df = pd.melt(df, id_vars=['All Companies'], var_name='Year', value_name='Value')

# Check for specific country strings in the 'All Companies' column
country_values = melted_df['All Companies'].str.contains('England and Wales|Scotland|Northern Ireland|United Kingdom', case=False, na=False)

# Create a new column named 'Countries' in position 1
melted_df.insert(1, 'Countries', '')

# Set the values in the 'Countries' column based on the condition
melted_df.loc[country_values, 'Countries'] = melted_df.loc[country_values, 'All Companies']

# Fill the NaN values in the 'Countries' column with the forward-filled values
melted_df['Countries'] = melted_df['Countries'].replace('', np.nan).ffill()


# Check for float values in the 'Value' column with non-zero decimal parts
float_values = melted_df['Value'].apply(lambda x: isinstance(x, float) and x % 1 != 0)

# Create a new column named 'Change' in position 4
melted_df.insert(4, 'Change', np.nan)

# Set the values in the 'Change' column based on the condition
melted_df.loc[float_values, 'Change'] = melted_df.loc[float_values, 'Value']

# Delete the entries in the 'Value' column where 'Change' column has a value
melted_df.loc[float_values, 'Value'] = np.nan



# Save the modified DataFrame to a CSV file
melted_df.to_csv('/Users/femisokoya/Documents/GitHub/3b-cra/melted1_results.csv', index=False)

# Print the modified DataFrame to verify the changes
print(melted_df.head())