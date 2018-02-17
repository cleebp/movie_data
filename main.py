"""
main.py

@author: Brian Clee
@date: 2/14/18

@purpose: Take the movie_data.csv and answer the following questions: 
	1) What are the 5 most popular genres?
	2) What words are characteristic of the movie summaries in those genres
	3) Do we see evidence of Zipf’s law in the summaries
@requirements: Python3.4, pandas, numpy, nltk (and data, see readme)
@arguments: movie_data.csv
"""

# imports
import sys
import pandas as pd
import numpy as np
#import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# @function: main
# @purpose: driver function that reads in the dataset and calls all other functions
# @note: normally I would put this last but I moved it to the top for readability, its still called on the last line
#   of the file, the inner C programmer in me is kind of appalled by this...
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
# @param: dataset csv as a pandas dataframe object
# @return: a list with the top 5 genres in descending order
def top_genres(data):
	genre_dict = {}
	for row in data.itertuples(index=True):
		genre_str = str(getattr(row, 'genres'))
		genre_str = genre_str[1:-1]
		genre_str = genre_str.replace('"', '')
		for genre in genre_str.split(', '):
			if genre in genre_dict:
				genre_dict[genre] = genre_dict.get(genre) + 1
			else:
				genre_dict[genre] = 1

	sorted_genres = sorted(genre_dict, key=genre_dict.get, reverse=True)
	for i in range(0,5):
		print(str(sorted_genres[i]) + ": " + str(genre_dict[sorted_genres[i]]))

main()