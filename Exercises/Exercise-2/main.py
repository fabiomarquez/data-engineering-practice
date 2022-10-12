# Author: Fábio Marquez de Carvalho Júnior
# Date: 26/04/2022

# Objectives:
# Web scrap/pull down the contents of https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/
# Analyze it's structure, determine how to find the corresponding file to 2022-02-07 14:03
# Build the URL required to download this file, and write the file locally
# Open the file with Pandas and find the records with the highest HourlyDryBulbTemperature
# Print this to stdout/command line/terminal

import requests
import pandas as pd

url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/'

def main():
    req = requests.get(url)
    data = req.text # type string
    
    splited_data = data.split('2022-02-07 14:03')

    splited_tags = splited_data[0].rsplit('<tr><td><a href="', 1)

    splited_id = splited_tags[1].split('.csv')[0]

    csv_url = f'{url}{splited_id}.csv'
    print(f'Downloading data from {csv_url}')

    csv_data = requests.get(csv_url)

    with open('data.csv', 'wb') as file:
        for chunk in csv_data:
            file.write(chunk)

    df = pd.read_csv(filepath_or_buffer = 'data.csv', sep = ',')

    max_value = max(df.HourlyDryBulbTemperature)

    record = df[df.HourlyDryBulbTemperature == max_value]

    response = record.to_dict(orient='records')

    for key, value in response[0].items():
        print(key, ':', value)

if __name__ == '__main__':
    main()
