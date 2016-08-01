# To run locally:
# python similar_movies_cosine.py --items=ml-100k/u.item ml-100k/u.data > ../Data/output/similar_movies_out.txt

# To run on a single EMR node:
# python similar_movies_cosine.py -r emr --items=ml-100k/u.item ml-100k/u.data > ../Data/output/similar_movies_out.txt

# To run on 4 EMR nodes:
# python similar_movies_cosine.py -r emr --num-ec2-instances=4 --items=ml-100k/u.item ml-100k/u.data ../Data/output/similarity-4-nodes.txt

from mrjob.job import MRJob
from mrjob.step import MRStep
from math import sqrt
from itertools import combinations

class SimilarMoviesRecommendation(MRJob):
    
    def configure_options(self):
        super(SimilarMoviesRecommendation, self).configure_options()
        self.add_file_option('--items', help='Path to u.item')
    
    def load_movie_names(self):
        # Load database of movie names.
        self.movieNames = {}

        with open("u.item") as f:
            for line in f:
                fields = line.split('|')
                self.movieNames[int(fields[0])] = fields[1].decode('utf-8', 'ignore')
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper_prepare_input,
                    reducer=self.reducer_user_movies),
            MRStep(mapper=self.mapper_pair_movieRatings,
                    reducer=self.reducer_get_similarity_scores),
            MRStep(mapper=self.mapper_sort_movie_similarities,
                    mapper_init=self.load_movie_names,
                    reducer=self.reducer_output_similarities)]
    
    def mapper_prepare_input(self, key, line):
#         prepare input in format userId => movieId,rating 
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield userID, (movieID,float(rating))
        
    def reducer_user_movies(self, userId, movieRatingsPair):
#         Group all movie,rating pairs per usr
        movieRatingsCollection = []
        for movieId,rating in movieRatingsPair:
            movieRatingsCollection.append((movieId,rating))
            
        yield userId, movieRatingsCollection
        
    def mapper_pair_movieRatings(self, userId, ratingsCollection):
#         Output all pairs of movies viewed by same user
        for item1, item2 in combinations(ratingsCollection,2):
            movieId1 = item1[0]
            rating1 = item1[1]
            movieId2 = item2[0]
            rating2 = item2[1]
            
#             This makes similarity bi-lateral
            yield(movieId1,movieId2),(rating1,rating2)
            yield(movieId2,movieId1),(rating2,rating1)
    
    
    def get_cosine_similarity_score(self,ratingPairs):
        
        numPairs = 0
        sumxx = sumyy = sumxy = 0
        
        for ratingX,ratingY in ratingPairs:
            sumxx += ratingX * ratingX
            sumyy += ratingY * ratingY
            sumxy += ratingX * ratingY
            numPairs += 1
        
        numerator = sumxy
        denominator = sqrt(sumxx) * sqrt(sumyy)
        
        score = 0
        if (denominator):
            score = (numerator/(float(denominator)))
        
        return (score, numPairs)
    
    def reducer_get_similarity_scores(self, moviePair, ratingPairs):
        
        score, numPairs = self.get_cosine_similarity_score(ratingPairs)
        
        if (numPairs>10 and score > 0.95):
            yield moviePair, (score,numPairs)
                
    def mapper_sort_movie_similarities(self, moviePair, similarityMatrixPair):
        score, numberOfRatings = similarityMatrixPair
        movieId1,movieId2 = moviePair
        
        yield (self.movieNames[int(movieId1)], score), \
        (self.movieNames[int(movieId2)], numberOfRatings)
    
    def reducer_output_similarities(self, movieScore, similarN):
        movie1, score = movieScore
        for movie2, n in similarN:
            yield movie1, (movie2,score,n)


if __name__ == "__main__":
    SimilarMoviesRecommendation.run()