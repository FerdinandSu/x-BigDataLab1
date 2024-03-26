import csv
import pandas as pd


data = pd.read_csv('movies.csv')
d = data.drop(['homepage', 'original_title', 'overview', 'spoken_languages', 'keywords', 'production_companies', 'status', 'tagline',
              'vote_average', 'vote_count', 'id', 'cast', 'release_date', 'production_countries', 'popularity'], axis=1)
d.to_csv('movies1.csv', index=False)
