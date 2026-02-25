"""
Created on Monday Feb 23 2026

@author yorl
"""


import os
import os.path
import wget
import pandas as pd
import numpy as np
import requests
import glob



dwn_url = ""


# This is the input file path for the excel file containing the url's 
input_path = "C:/Users/SPAC-49/Documents/Specialisterne/Softwareudvikling/Uge 4/test data/test-data.xlsx"

ID = "BRnum"

try:
    df = pd.read_excel(input_path, sheet_name=0)
    #print(df)
    print(df["Pdf_URL"][2])
except:
    print("GODDAMNIT")
finally:
    print("test ended")





# This is the output file path 
output_path = "output/"

for j in range(len(df)):
    
    try:
        file_name = df["BRnum"][j]
        url_link = df["Pdf_URL"][j]
        #print(file_name + ".pdf")
    except:
        print("lol")
    finally:
        pass

    if type(url_link) is float:
        print("Nan")
        pass
    elif type(url_link) is str:
        print(url_link)
        try:
            response = requests.get(url_link)
            if response.status_code == 200:
                #os.path and os goes here
                # this is where you'd take data and store as a pdf in output path 
                print("200")
            else:
                print("404")
            pass
        except:
            pass
    else:
        print("fail")
    





# function for filtering rows with no url's
# function goes here

# we gotta check if it has already been downloaded
# duplicate check
# not sure how to check that
duplicate_check = ""


