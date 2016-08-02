# This is a small script to fetch relevant and required list of movies from output file from hadoop cluster(s)
# Running command:
# python filter-similar-movies.py ../Data/output/similarity-16-nodes.txt > ../Data/output/filtered_movies.txt 
#NOTE:: (../Data/output/similarity-16-nodes.txt is output file from main MRJob[similar_movies_cosine_1m])
 

from mrjob.job import MRJob
import sys

class FilterSimilarMovies(MRJob):
    
    def mapper(self, key, line):
        (movieName, result) = line.split('\t')
        if (movieName == '"Shawshank Redemption, The (1994)"'): ## Put movie of your choice here
            (paranth, similarMovie, values) = result.split('"')
            (space,similarityScore,Ratings) = values.split(',')
            cleanRatings = Ratings.split(']')
            totalRating = int(cleanRatings[0])
            if(totalRating > 500):
                yield similarityScore, (similarMovie,totalRating)
    
    def reducer(self, similarityScore, values):
        for value in values:
            yield similarityScore,value

if __name__ == "__main__":
    FilterSimilarMovies.run()