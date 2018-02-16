"""
main.py

@author: Brian Clee
@date: 2/14/18

@purpose:
@requirements: Python3.4, pandas, numpy, nltk (and data, see readme)
@arguments: 
"""

# imports
import sys
import pandas as pd
import numpy as np
#import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# @function: main
# @purpose: driver function that reads in the dataset and calls all other functions
# @note: normally I would put this last but I moved it to the top for readability, its still called on the last line of the file
def main():
	# check to make sure our dataset was passed in, graceful exit if it wasn't
	if len(sys.argv) is not 2:
		print("Error. Please provide this script with the movie dataset as an argument:")
		print("python3 main.py movie_data.csv")
		sys.exit(0)

	# take the argument and assume its our dataset (this should have more validation checking in the future)
	data = sys.argv[1]
	# read the dataset with pandas and overwrite the old variable to save space
	data = pd.read_csv(data)

	# now that we have our data, lets answer that first question...
	top_genres(data)

# @function: top_genres
# @purpose: Figure out what the top 5 most popular genres are in our dataset
def top_genres(data):
	# code goes here
	print("huzzah!")

main()