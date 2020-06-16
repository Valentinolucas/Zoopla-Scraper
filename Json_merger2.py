
import json
import os
import pandas as pd
import gzip
import sys
from datetime import date

''' 
The following code merge all the files in a given directory and creates a .csv file with the data

'''
#system argument
# folder = sys.argv[1]
list_dir = os.listdir(os.getcwd())
for folder in list_dir:
    #Unzip the files and add the content to listing.
    listing = []
    list_of_files = os.listdir(os.getcwd() + '\\' + str(folder))
    for file in list_of_files:
        index = list_of_files.index(file)
        with gzip.open(os.getcwd() + '\\' + str(folder) + '\\' + str(list_of_files[index]), 'rb') as f:
                try:
                        content = json.load(f)
                        listing.extend(content['listing'])
                except:
                        pass

    #create dataframe and save
    df = pd.DataFrame(listing)
    df.to_csv(os.getcwd() + '\\' + str(folder) + '\\' +'Master ' + str(date.today()) + '.csv', index = False)
    print(str(folder) + ' Master is done')


