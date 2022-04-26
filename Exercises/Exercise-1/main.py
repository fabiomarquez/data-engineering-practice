# Author: Fábio Marquez de Cravalho Júnior
# Date: 25/04/2022

# Objectives:

# Create the directory downloads if it doesn't exist
# Download the files one by one
# Split out the filename from the URI, so the file keeps its original filename
# Each file is a zip, extract the csv from the zip and delete the zip file
# For extra credit, download the files in an async manner using the Python package aiohttp
# Also try using ThreadPoolExecutor in Python to download the files
# Write unit tests to improve your skills


import requests
import os
from zipfile import ZipFile

download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

def get_filename(url):
  first_delimiter = '.com/'
  second_delimiter = '.zip'
  start = url.find(first_delimiter) + len(first_delimiter)
  end = url.find(second_delimiter)
  name = url[start:end]
  return name

def download_file(url, path):
  file = requests.get(url)
  file_name = get_filename(url)
  print(f'Downloading {file_name}...')

  with open(f'{path}/{file_name}.zip', "wb") as content:
      content.write(file.content)

  print(f'{file_name} downloaded succesfully!')

  return file_name

def extract_file(path, file_name):
  
  with ZipFile(f'{path}/{file_name}.zip', 'r') as f:
      f.extractall(path)

  print(f'{file_name} extracted succesfully!')


def main():
    
    # Creating a folder named downloads if it not exists already
    if 'downloads' not in os.listdir():
        os.mkdir('downloads')
    
    path = 'downloads'

    count = 1

    for url in download_uris:
        
        print(f' STEP {count} OF {len(download_uris)} '.center(30, '#'))

        try:
            file_name = download_file(url, path)
        except Exception as e:
            print(f'Unable to download! Error: {e}')

        try:
            extract_file(path, file_name) 
        except Exception as e:
            print(f'Unable to extract! Error: {e}')
            
        try:
            os.remove(f'{path}/{file_name}.zip')
            print(f'{file_name} deleted succesfully!')
        except Exception as e:
            print(f'Unable to remove the file! Error: {e}')

        count += 1

if __name__ == '__main__':
    main()
