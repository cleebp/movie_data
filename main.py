"""
main.py

@author: Brian Clee
@date: 2/14/18

@purpose: Take the movie_data.csv and answer the following questions: 
	1) What are the 5 most popular genres?
	2) What words are characteristic of the movie summaries in those genres
	3) Do we see evidence of Zipf’s law in the summaries
@requirements: Python3.4, pandas, numpy, nltk (and data, see readme)
@arguments: data/movie_data.csv
@run: python3 main.py data/movie_data.csv
"""

# imports
import sys
import time
import os.path
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib

# @function: top_genres
# @purpose: Figure out what the top 5 most popular genres are in our dataset
# @param: (data) movie_data.csv as a pandas dataframe object
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

	# return the list to be used elsewhere, counts aren't needed anymore so no need to return the genre_dict
	return sorted_genres

# @function: genre_properties
# @purpose: Find out what words are characteristic of the movie summaries in the top genres
# @param: (sorted_genres) sorted list of genres in descending order of popularity (we only care about the top 5)
# @param: (data) movie_data.csv as a pandas dataframe object
def genre_properties(sorted_genres, data):
	# create empty genre_tokens dict to hold genre:token lists
	genre_tokens = {}
	# boolean check to see if we have already gone through and tokenized everything
	files_exist = os.path.isfile("data/top_genres.txt")

	# initialize the genre_tokens keys outside of the if statement so that it can be used in both cases
	for i in range(0,5):
		# keys are simply the top 5 genres
		genre_tokens[sorted_genres[i]] = []

	# if for some reason the data files don't exist, lets go through the process of creating them (takes ~3 minutes)
	if not files_exist:
		print("The data files don't exist, beginning tokenization process, grab some coffee...")

		# grab the nltk corpus stopwords
		stopWords = set(stopwords.words('english'))
		# add in some extra noise words we don't care about (I definitely missed a couple)
		noiseWords = ["{{Expand section}}", ",", ".", "(", "[", "{", ")", "]", "}", ":", ";", "&", "'", '"', "'s",
						"``", "''", "n't"]

		# store the start time so we can keep track of how long this process takes
		t1 = time.time()

		# iterate through the dataset, this is largerly the same structure as in top_genres so I won't repeat comments
		for row in data.itertuples(index=True):
			# strip the genre string of quotes and brackets
			genre_str = str(getattr(row, 'genres'))
			genre_str = genre_str[1:-1]
			genre_str = genre_str.replace('"', '')

			# don't need to do any trimming on summary strings like we did for genre strings
			summary_str = str(getattr(row, 'summary'))
			# tokenize the summary string
			tokens_raw = word_tokenize(summary_str)
			# create an empty token list we will fill with filtered tokens
			tokens_processed = []
			# filter the raw token list
			for word in tokens_raw:
				# we only care about words not in the stopWords or noiseWords list
				if word not in stopWords and word not in noiseWords:
					tokens_processed.append(word)

			# for each of the film's genres...
			for genre in genre_str.split(', '):
				# if the genre is in the top 5 genres genre_tokens dict...
				if genre in genre_tokens:
					# then extend the filtered tokens to the end of genre_token's value pair for the current genre
					genre_tokens.get(genre).extend(tokens_processed)

		# grab the stop time and alert the user of progress
		t2 = time.time()
		print("Tokenization completed in " + str(t2-t1) + " seconds.")

		# to make sure we never have to do that again, lets store all of our data in some .txt files
		# first lets store the top 5 genres in the file "top_genres.txt", one genre per line
		# theoretically this step isn't necessary, but if our corpus changes the top 5 genres could change as well
		top_genres_file = open("data/top_genres.txt", "w")
		for i in range(0, 5):
			# grab the genre name
			genre = sorted_genres[i]
			# write it to a line with a newline break
			top_genres_file.write("%s\n" % genre)
			# using that genre name create a file "genre.txt" where we will store all of that genre's tokens list
			genre_file = open("data/%s.txt" % genre, "w")
			# for all of the tokens in that genres value pair from our genre_tokens dict...
			for token in genre_tokens.get(genre):
				# write each token on a newline
				genre_file.write("%s\n" % token)
			# close our genre file inside the for loop since we will use the same variable for all 5 genre files
			genre_file.close()
		# finally close the top_genres file
		top_genres_file.close()

	# in this case the data files already exist and we don't need to do any tokenization, this should be the normal case
	else:
		print("\nThe data files exist, beginning token loading:")
		# first open the file with the top 5 genres listed
		top_genres_file = open("data/top_genres.txt", "r")

		# iterate over each line in the file
		for index, line in enumerate(top_genres_file):
			# initialize the genre_tokens dict with the top 5 genres as keys, and empty lists for tokesn as values
			genre_tokens[sorted_genres[index]] = []

		# close the top genres file for memory
		top_genres_file.close()

		# iterate over each of the genre keys in our genre_tokens dict that we just loaded
		for genre in genre_tokens:
			print("Loading the " + str(genre) + ".txt file...")
			# open the associated file for each genre
			genre_file = open("data/%s.txt" % genre, "r")

			# iterate over each line of the file
			for index, line in enumerate(genre_file):
				# trim the new line characters from the line
				trimmed_line = line.replace("\n", "")
				# append the line (token) to the corresponding token list for the current genre in our genre_tokens dict
				genre_tokens.get(genre).append(trimmed_line)

			# again close our files
			genre_file.close()

		# we are now done loading in our data files and can proceed with addressing the genre characterization
		print("Done loading!\n")

	# encapsulate all these plot creations in a loop, have the loop only run if the plots don't exists...

	genre_fdists = {}
	for genre in genre_tokens.keys():
		print(str(genre) + " tokens: " + str(len(genre_tokens.get(genre))))
		fdist = FreqDist(genre_tokens.get(genre))

		fig_path = str("plots/%s_fdist.png" % genre)
		if not os.path.isfile(fig_path):
			print(str(genre) + " FreqDist plot does not exist, creating and displaying it now...")
			print("To skip this process in the future, save the figure as `plots/Genre Name_fdist`")
			fdist.plot(50, cumulative=True)

		genre_fdists[genre] = fdist

	# list of common words in sorted order
	common_set = []

	for i in range(1,5):
		genre = sorted_genres[i]
		top_current = genre_fdists[genre].most_common(50)
		new_commons = []

		print(genre)

		# special case where common_set doesn't exist yet, so we just compare the first two freq_dists together
		if i is 1:
			prev_genre = sorted_genres[i-1]
			top_prev_raw = genre_fdists[prev_genre].most_common(50)
			top_prev_filtered = []
			for sample in top_prev_raw:
				top_prev_filtered.append(sample[0])

			# list comprehension to create a shared set list between current and previous genre's fdists

			for sample in top_current:
				#new_list = [sample for sample in prev_genre if sample[0] is key]
				#print(new_list)
				if sample[0] in top_prev_filtered:
					new_commons.append(sample[0])

		# normal case where common_set exists, compare current genre's freq_dist against common set
		else:
			for sample in top_current:
				if sample[0] in common_set:
					new_commons.append(sample[0])

		common_set = new_commons

	print(common_set)
	
	# then for each genre list the top unique words

# @function: main
# @purpose: driver function that reads in the dataset and calls all other functions
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

	# now that we have our data, lets get a list of the top genres sorted descending
	sorted_genres = top_genres(data)

	# with the sorted genres list lets find out what properties are associated with the top genres summaries
	genre_properties(sorted_genres, data)

main()