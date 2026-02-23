"""
Created on Monday Feb 23 2026

@author yorl
"""


import wget
import pandas as pd
import numpy
import requests



dwn_url = ""


# This is the input file path for the excel file containing the url's 
input_path = "\Data\test-data.xlsx"

# This is the output file path 
output_path = ""

ID = "BRnum"

df = pd.read_excel(input_path, sheet_name=0, index_col=ID)

# function for filtering rows with no url's
# function goes here

# we gotta check if it has already been downloaded
# duplicate check
# not sure how to check that
duplicate_check = ""

#try:
#
#except :

with open(input_path, 'r') as dummy_data:
    

    pass