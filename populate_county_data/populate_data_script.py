import pandas as pd

csv_file_path = 'RDC_Inventory_Core_Metrics_County.csv'
dataframe = pd.read_csv(csv_file_path, header=0, usecols=['county_fips', 'county_name'], dtype={'county_fips': str})

for row in dataframe.itertuples(index=False):
    print(f"Fips: {row.county_fips}, Name: {row.county_name}")