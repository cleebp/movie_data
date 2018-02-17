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
	# read through csv and store genre as a key in a dict and its value is the count in the csv
	# if genre not in genre_dict: add it and make value 1 > if genre_dict.has_key(genre) > genre_dict[genre] = 1
	# if it is, find it and increment its value by 1 > genre_dict[genre] = genre_dict.get(genre) + 1
	# once finished with entire dataset sort the dict by values descending
	# return top 5 genres in a list
	genre_dict = {}
	for row in data.itertuples(index=True):
		"""
			dev notes: current implementation results in: 
				genres: ["Children's/Family", "Children's", "Animal Picture", "Family-Oriented Adventure", "Adventure", "Family Film"]
				genre: [
				genre: "
				genre: C
				...
			obviously there are a couple issues..
			- cant parse the individual list items, its seeing the entire thing as a string no matter what i try
			> might have to do some nltk here to get around this (say something like tokens are "..", then check the genre_dict for tokens)

		"""
		print("\n=== new row ===")
		print("row: " + str(row))
		print("genres: " + str(getattr(row, 'genres')))
		genre_list = list(getattr(row, 'genres'))
		for genre in genre_list:
			print("genre: " + str(genre))
			if genre in genre_dict:
				genre_dict[genre] = genre_dict.get(genre) + 1
			else:
				genre_dict[genre] = 1
	print(genre_dict)

main()