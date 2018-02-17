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
# @return: a list with the genres sorted in descending order by count
def top_genres(data):
	# first create an empty dictionary we will populate with key:values as genre:count
	genre_dict = {}

	# loop through the given pandas dataframe, use itertuples to retain the dtypes
	for row in data.itertuples(index=True):
		# grab the current row's genres cell and store it in genre_str
		genre_str = str(getattr(row, 'genres'))
		# each genre list begins..ends with [..], lets trim those off
		genre_str = genre_str[1:-1]
		# each genre is also encapsulated in quotes like "genre", lets find and replace those pesky quotes
		genre_str = genre_str.replace('"', '')
		
		# we now have a nicely formatted list of genres, lets split that string on commas and loop through each genre
		for genre in genre_str.split(', '):
			# if the genre already exists in our dictionary...
			if genre in genre_dict:
				# ... find and increment its count
				genre_dict[genre] = genre_dict.get(genre) + 1
			# if the genre doesnt exist in our dictionary...
			else:
				# add it to the dictionary and initialize its count at 1
				genre_dict[genre] = 1

	# we now have an unsorted dict of genres:counts, lets sort it using sorted (returns a list of genres descending)
	sorted_genres = sorted(genre_dict, key=genre_dict.get, reverse=True)
	for i in range(0,5):
		# grab the i'th genre from the sorted_genres list
		genre = sorted_genres[i]
		# find that genre's count from the genre_dict dictionary
		count = genre_dict.get(genre)
		# print out the genre and its count (i+1 for readability of top 5 since lists start at 0)
		print(str(i+1) + ". " + str(genre) + ": " + str(count))

main()