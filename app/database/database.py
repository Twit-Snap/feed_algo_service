import faiss
import random
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# sentence-transformers/all-MiniLM-L6-v2
# jaimevera1107/all-MiniLM-L6-v2-similarity-es


class VectorialDatabase:
    def __init__(self, model_url: str = "sentence-transformers/all-MiniLM-L6-v2"):
        # Initialize the model for embedding the tweets and the index for the Vect database.
        self.model = SentenceTransformer(model_url)

        self.uuid_hash = {}
        self.tweets = {}

    def __initialize_index(self):
        # Initialize the Tweets and uuid containers.
        # As the vectorial database uses integers for indexing, a copy of the uuids is stored in a dictionary.
        self.uuid_hash = {}
        self.tweets = {}

        _index = faiss.IndexFlatIP(self.model.encode(["Seed"]).shape[1])
        self.index = faiss.IndexIDMap(_index)

    def log_current_status(self):
        if len(self.tweets) > 0:
            print("Current number of tweets in the database: ", len(self.tweets))
        else:
            print("No content was loaded yet to the Database.")

    def add_tweets_to_index(self, tweets_data: List[Tuple[str, str]]):
        self.__initialize_index()
        for tweet_uuid, tweet_content in tweets_data:
            internal_tweet_id = len(self.tweets)
            self.tweets[internal_tweet_id] = tweet_content
            self.uuid_hash[internal_tweet_id] = tweet_uuid
        tweets_embedding = self.model.encode(list(self.tweets.values()))
        self.index.add_with_ids(tweets_embedding, list(self.tweets.keys()))

    def rank_by_tweets_sample(self, tweets_sample: List[str], k: int = 3):
        # If k is 0, no tweets are requested so return an empty dictionary.
        # If index is not initialized due to no twits being loaded, also return an empty dictionary as there's no information to return.
        if k == 0 or len(self.tweets) == 0:
            return {}

        # Make the limit value of k the same as the number of tweets in the database.
        if k > len(self.tweets):
            k = len(self.tweets)

        if len(tweets_sample) == 0:
            # Return random twits due to the lack of information of the user.
            random_tweets = random.sample(list(self.tweets.items()), k)
            return {self.uuid_hash[tweet_id]: tweet_content for tweet_id, tweet_content in random_tweets}

        ranking = {}
        tweets_sample_embedding = self.model.encode(tweets_sample)

        D, I = self.index.search(tweets_sample_embedding, k=k)
        for tweet_id in I[0]:
            tweet_uuid = self.uuid_hash[tweet_id]
            tweet_content = self.tweets[tweet_id]
            ranking[tweet_uuid] = tweet_content
        return ranking


vectorial_db = VectorialDatabase("sentence-transformers/all-MiniLM-L6-v2")
