# Movie Data

Using the `movie_data.csv` which contains text summaries of ~42K movies scraped from wikipedia, this project seeks to answer the following questions:
- What are the 5 most popular genres?
- What words are characteristic of the movie summaries in those genres
- Do we see evidence of [Zipf’s law](https://simple.wikipedia.org/wiki/Zipf%27s_law) in the summaries

## Database properties

The database has the following properties for all movies:
- `id`: unique integer ID for each film
- `title`: string title
- `genres`: list of strings for genres of each film, for instance `[“Space western”, “Horror”]`
- `summary`: unstructured text summary scraped from the film’s wikipedia page

The database has the following properties for some films:
- `release_date`: can be in the form `mm/dd/yy` or simply `yyyy`, present for most films
- `box_office_revenue`: integer of the USD, only present for a few films
- `runtime`: integer of the total running minutes, present for most films

## Author

Brian Clee
bpclee@ncsu.edu
