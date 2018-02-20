"""
main.py

@author: Brian Clee
@date: 2/14/18

@purpose: Take the movie_data.csv and answer the following questions: 
	1) What are the 5 most popular genres?
	2) What words are characteristic of the movie summaries in those genres
	3) Do we see evidence of Zipf’s law in the summaries
@requirements: Python3.4, pandas, numpy, nltk (and data, see readme), matplotlib
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
from matplotlib import pyplot as plt

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
	print("The top 5 genres in the movie_data.csv dataset are:")
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
		print("\nThe data files don't exist, beginning tokenization process, grab some coffee...")

		# grab the nltk corpus stopwords
		stopWords = set(stopwords.words('english'))
		# add in some extra noise words we don't care about (I definitely missed a couple)
		noiseWords = ["{{Expand section}}", ",", ".", "(", "[", "{", ")", "]", "}", ":", ";", "&", "'", '"', "'s",
						"``", "''", "n't", "`", '’']

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
		print("Tokenization completed in " + str(t2-t1) + " seconds.\n")

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

	# lets create a dict genre_fdicts that will store the genre:freq dist pairs for each genre
	genre_fdists = {}
	print("Creating frequency distributions for each genre:")
	# for each of our top genres
	for genre in genre_tokens.keys():
		# print out the genre and number of tokens it has
		print("Total " + str(genre) + " tokens to consider: " + str(len(genre_tokens.get(genre))) + "...")
		# calculate the Frequency Distribution of all the genres tokens
		fdist = FreqDist(genre_tokens.get(genre))
		# add the genre:freqdist pair to our genre_fdists dict
		genre_fdists[genre] = fdist

		# next lets do some plotting of the top 50 most frequent tokens
		fig_path = str("plots/%s_fdist.png" % genre)
		# we only want to handle plotting if for some reason the plots don't exist
		if not os.path.isfile(fig_path):
			# alert the user of what's happening since matplotlib allows the user to specify bounds through a GUI
			print(str(genre) + " FreqDist plot does not exist, creating and displaying it now...")
			# alert the user of how to save the plot so this process is no longer run
			print("To skip this process in the future, save the figure as `plots/Genre Name_fdist`")
			# plot the top 50 freq dist samples
			fdist.plot(50, cumulative=True)

	print("Done calculating frequency distributions!\n")

	# now that we have the freq dists for each genre, lets do some more analytics
	# to begin lets find & store the common set of tokens that is shared between all genre's top 50 freq dist samples
	common_set = []
	print("Finding the common set of words across all genre frequency distributions:")
	# loop through the genres starting with the second (this logic is explained below)
	for i in range(0, 5):
		# grab the current genre from our sorted_genres list that was passed into this function
		genre = sorted_genres[i]
		# find the top 50 most common samples in our current genres freq dist
		top_current = genre_fdists[genre].most_common(50)
		# initialize an empty temporary list that will overwrite our common_set list
		new_commons = []

		print("Now computing common set additions from " + str(genre) + " genre...")

		# inner loop to compare each genre against every other genre O(n^2), further work could be done to improve this
		for j in range(0, 5):
			# if the genre we are comparing against is the current genre then skip it
			if j is i:
				continue

			# grab the genre to compare against's name
			compare_genre = sorted_genres[j]
			# grab the compare genre's frequency distribution
			top_compare_raw = genre_fdists[compare_genre].most_common(50)
			# since the most_common function returns a tuple (sample, count) lets strip out just the sample
			top_compare_filtered = []
			# for all the sample tuples...
			for sample in top_compare_raw:
				# grab just the sample name
				top_compare_filtered.append(sample[0])

			# now lets actually compare the current genre's samples against the compare genre's samples
			for sample in top_current:
				# if the current sample name is in the top 50 sample names from the compare genre...
				if sample[0] in top_compare_filtered:
					# then add it to the new_commons list
					new_commons.append(sample[0])

			# now we need to update the common_set list with samples that aren't already in it
			for sample in new_commons:
				# if the sample from new_commons doesn't exist in the common_set list...
				if sample not in common_set:
					# then add the sample to common_set
					common_set.append(sample)

	print("A common set has been found! Across all genres " + str(len(common_set)) + " words are shared, they are:")
	print(common_set)

	# then for each genre list the top unique words
	print("\nComputing the unique sets for each genre...")
	for genre in genre_tokens.keys():
		unique_set = []
		top_current = genre_fdists[genre].most_common(50)

		for sample in top_current:
			if sample[0] not in common_set:
				unique_set.append(sample[0])

		print(str(genre) + "'s unique set: " + str(unique_set))

# @function: zipfs
# @purpose: Investigate all of the summaries and see if it exhibits properties of zipfs law
# @param: (data) movie_data.csv as a pandas dataframe object
def zipfs(data):
	# create empty summary_tokens list to hold tokens from every summary
	summary_tokens = []
	# boolean check to see if we have already gone through and tokenized everything
	files_exist = os.path.isfile("data/summary_tokens.txt")

	# if the data files don't exist, lets go through the process of creating them (takes ~3 minutes)
	if not files_exist:
		print("\nThe summary_tokens file doesn't exist, beginning tokenization process, grab some coffee...")

		# store the start time so we can keep track of how long this process takes
		t1 = time.time()

		# for zipfs law we will take out punctuation, but not stop words
		noiseWords = ["{{Expand section}}", ",", ".", "(", "[", "{", ")", "]", "}", ":", ";", "&", "'", '"', "'s",
						"``", "''", "n't", "`", '’']

		# iterate through the dataset, this is largely the same structure as in top_genres so I won't repeat comments
		for row in data.itertuples(index=True):
			# grab the summary string for tokenization
			summary_str = str(getattr(row, 'summary'))

			# tokenize the summary string
			tokens = word_tokenize(summary_str)

			# check to see if the token is in our noiseTokens list...
			for token in tokens:
				# if its not a noise word...
				if token not in noiseWords:
					# then add the token to our summary_tokens list
					summary_tokens.append(token)

		# grab the stop time and alert the user of progress
		t2 = time.time()
		print("Tokenization completed in " + str(t2 - t1) + " seconds.\n")

		# next lets write our summary tokens to the "summary_tokens.txt" file
		summary_file = open("data/summary_tokens.txt", "w")
		# go through each token in the summary_tokens list
		for token in summary_tokens:
			# write each token on a newline
			summary_file.write("%s\n" % token)

		# close our file for memory
		summary_file.close()

	# the summary_tokens file already exists and we don't need to do any tokenization, this should be the normal case
	else:
		print("\nThe summary_tokens file exists, beginning token loading...")
		# open the summary_tokens.txt file
		summary_file = open("data/summary_tokens.txt", "r")

		# iterate over each line in the file
		for index, line in enumerate(summary_file):
			# trim the new line characters from the line
			trimmed_line = line.replace("\n", "")
			# append the line (token) to the summary_tokens list
			summary_tokens.append(trimmed_line)

		# close the summary file for memory
		summary_file.close()

		# we are now done loading the summary file and can proceed with addressing zipfs law
		print("Done loading!\n")

	print("Creating frequency distribution from " + str(len(summary_tokens)) + " summary tokens...")
	# create the frequency distribution of our summary tokens
	summary_fdist = FreqDist(summary_tokens)
	print("Frequency distribution computed!")

	# caclulate the frequency of our summary_fdist by grabbing the values and sorting descending (plot trends downwards)
	freqs = sorted(summary_fdist.values(), reverse=True)
	# calculate the ranks via our frequencies
	ranks = range(1, len(freqs) + 1)

	print("\nNow plotting the ranks/frequencies of the summary frequency distribution to demonstrate zipfs law...")
	print("A plot should be displayed shortly, close the plot to finish script execution.")

	# use a loglog plot (log of both axis) from our ranks by freqs
	plt.loglog(ranks, freqs)
	plt.xlabel('frequency (f)', fontsize=12, fontweight='bold')
	plt.ylabel('rank (r)', fontsize=12, fontweight='bold')
	plt.grid(True)
	# display the plot
	plt.show()

# @function: main
# @purpose: driver function that reads in the dataset and calls all other functions
def main():
	# check to make sure our dataset was passed in, graceful exit if it wasn't
	if len(sys.argv) is not 2:
		print("Error. Please provide this script with the movie dataset as an argument:")
		print("python3 main.py movie_data.csv")
		sys.exit(1)

	# take the argument and assume its our dataset (this should have more validation checking in the future)
	data = sys.argv[1]
	# read the dataset with pandas and overwrite the old variable to save space
	data = pd.read_csv(data)

	# now that we have our data, lets get a list of the top genres sorted descending
	sorted_genres = top_genres(data)

	# with the sorted genres list lets find out what properties are associated with the top genres summaries
	genre_properties(sorted_genres, data)

	# finally lets see if the corpus of movie summaries exhibits properties of zipfs law
	zipfs(data)

	print("\nExiting gracefully...")
	sys.exit(0)

main()